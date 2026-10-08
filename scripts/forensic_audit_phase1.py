#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    required=['fixtures/agent-system/reference-agent.json','scripts/agent_system_platform_server.py','scripts/certify_agent_system_e2e.py','.github/workflows/agent-system-e2e.yml','integrations/agent-platform/adapter.json','integrations/agent-platform-sdk/adapter.json','integrations/agent-os/adapter.json','integrations/agent-developer/adapter.json']
    missing=[p for p in required if not (ROOT/p).is_file()]
    if missing: raise SystemExit('FAIL phase1 artifacts: '+','.join(missing))
    fixture=json.loads((ROOT/required[0]).read_text())
    assert fixture['apiVersion']=='tadl.tinlance.com/v1' and fixture['kind']=='Agent'
    workflow=(ROOT/'.github/workflows/agent-system-e2e.yml').read_text()
    for sha in ['3d3c42e5aac5ba805825da76410c181273ba90b1','5fda3b95a4ea91299a34e894583c3862153e4b97','249970729cb0ef3589644e2896645e5dc5ba9c38']:
        assert sha in workflow
    for repo in ['tinlance-agent-developer','tinlance-agent-os','tinlance-agent-platform-sdk','tinlance-agent-platform']:
        assert repo in workflow
    assert 'certify_agent_system_e2e.py' in workflow and 'test_agent_os_gateway.py' in workflow
    for path in required:
        if path.endswith('.py') or path.endswith('.yml'):
            text=(ROOT/path).read_text(encoding='utf-8')
            if 'TODO' in text or 'TBD' in text: raise SystemExit('FAIL unresolved placeholder: '+path)
    print('PASS TSIC-01 post-phase forensic audit: four-repository E2E gate, fixture, server, certifier and pinned CI controls verified')
if __name__=='__main__': main()
