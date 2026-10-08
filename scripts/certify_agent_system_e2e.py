#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('TSIC_PLATFORM_URL')
def main():
    if not BASE: raise SystemExit('TSIC_PLATFORM_URL is required')
    tadl=ROOT/'../agent-developer'
    fixture=ROOT/'fixtures/agent-system/reference-agent.json'
    result=subprocess.run(['node','cli/tadl.mjs','agent','validate',str(fixture)],cwd=tadl,capture_output=True,text=True)
    if result.returncode: raise SystemExit('TADL validation failed: '+result.stdout+result.stderr)
    sys.path.insert(0,str(ROOT/'../agent-os/src')); sys.path.insert(0,str(ROOT/'../agent-platform-sdk/src'))
    from tinlance_agent_platform_sdk import AgentPlatform
    from tinlance_agent_os.platform_adapter import AgentPlatformAdapter
    from tinlance_agent_os.transport import HttpPlatformTransport, PlatformRequestContext, StaticAccessTokenProvider
    from tinlance_agent_os.daemon_service import LocalOSService
    from tinlance_agent_os.store import StateStore
    sdk=AgentPlatform(base_url=BASE,bearer_token=os.environ['TSIC_PLATFORM_TOKEN'],tenant_id=os.environ['TSIC_PLATFORM_TENANT'],subject_id=os.environ['TSIC_PLATFORM_SUBJECT'])
    assert sdk.health().ready is True
    agents=sdk.agents.list(); assert agents
    agent_id=agents[0].agent_id
    transport=HttpPlatformTransport(BASE,StaticAccessTokenProvider(os.environ['TSIC_PLATFORM_TOKEN']),allow_insecure_localhost=True)
    context=PlatformRequestContext(os.environ['TSIC_PLATFORM_TENANT'],os.environ['TSIC_PLATFORM_SUBJECT'],'tsic-agent-system-01','00-11111111111111111111111111111111-2222222222222222-01')
    adapter=AgentPlatformAdapter(transport,context)
    with tempfile.TemporaryDirectory() as directory:
        service=LocalOSService(StateStore(Path(directory)/'state.db'),adapter)
        workspace=service.create_workspace(context.subject_id)
        session=service.create_session(workspace.workspace_id,context.subject_id,agent_id)
        task=service.create_task(workspace.workspace_id,session.session_id,agent_id,'inspect repository')
        run=service.dispatch(task); assert run.state=='running'
        approval=service.request_approval(run.run_id,'security.scan','repo:tsic','governed integration test'); assert approval.approval_id
        assert service.events(run.run_id); assert service.evidence(run.run_id)
        assert service.cancel(run.run_id).state=='cancelled'
    print(json.dumps({'status':'pass','tadl':'validated','sdk':'executed','agent_os':'executed','platform':'executed','evidence':'observed','approval':'requested','cancellation':'verified'}))
if __name__=='__main__': main()
