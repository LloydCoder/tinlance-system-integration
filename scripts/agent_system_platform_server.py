#!/usr/bin/env python3
from __future__ import annotations
from uuid import uuid4
import os
from tests.support.reference_gateway import ReferencePlatformGateway, StaticPrincipalResolver
from tinlance_agent_platform_agents import AgentRegistry
from tinlance_agent_platform_api import AgentPlatformAPI
from tinlance_agent_platform_api.http import serve
from tinlance_agent_platform_contracts import AgentDefinition, Principal
from tinlance_agent_platform_events import InMemoryEventStore
from tinlance_agent_platform_evidence import InMemoryEvidenceStore
import threading, time, os, sys
TENANT='tenant-tsic'; SUBJECT='subject-tsic'; TOKEN=os.environ.get('TSIC_PLATFORM_TOKEN','token-tsic')
APPROVER_TOKEN=os.environ.get('TSIC_PLATFORM_APPROVER_TOKEN','approver-tsic-token'); PORT=18765
registry=AgentRegistry()
gateway=ReferencePlatformGateway(agents=registry,events=InMemoryEventStore(),evidence=InMemoryEvidenceStore(),approver_subjects=frozenset({'approver-tsic'}))
gateway.register_agent(AgentDefinition(uuid4(),TENANT,'tsic-reference-agent','1.0.0',SUBJECT,'default',frozenset({'repository.read','security.scan'}),'a'*64))
class DiagnosticGateway(ReferencePlatformGateway):
    def handle(self, request):
        try:
            return super().handle(request)
        except Exception as exc:
            print(f'gateway_error={type(exc).__name__}:{exc}',file=sys.stderr,flush=True)
            raise

gateway.__class__=DiagnosticGateway
class DiagnosticAPI(AgentPlatformAPI):
    def dispatch(self, request):
        try:
            return super().dispatch(request)
        except Exception as exc:
            print(f'api_error={request.operation}:{request.payload}:{type(exc).__name__}:{exc}',file=sys.stderr,flush=True)
            raise

resolver=StaticPrincipalResolver({TOKEN:Principal(SUBJECT,'user',TENANT,scopes=frozenset({'platform','repository.read','security.scan'})),'token-tsic':Principal(SUBJECT,'user',TENANT,scopes=frozenset({'platform','repository.read','security.scan'})),'tsic-reference-token':Principal(SUBJECT,'user',TENANT,scopes=frozenset({'platform','repository.read','security.scan'})),APPROVER_TOKEN:Principal('approver-tsic','user',TENANT,scopes=frozenset({'platform'}))})
server=serve(DiagnosticAPI(gateway),resolver)
thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
print(f'http://127.0.0.1:{server.server_address[1]}/v1/agent-platform',flush=True)
try:
    while True: time.sleep(1)
except KeyboardInterrupt: pass
finally: server.shutdown(); server.server_close(); thread.join(timeout=2)
