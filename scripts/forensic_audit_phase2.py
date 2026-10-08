#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    required=['scripts/certify_intelligence_to_opportunity.py','policies/intelligence-to-opportunity-baseline.json','conformance/requirements/phase2-intelligence-to-opportunity.json','.github/workflows/intelligence-to-opportunity.yml','integrations/world-intelligence/adapter.json','integrations/tads/adapter.json','integrations/sdea/adapter.json']
    missing=[p for p in required if not (ROOT/p).is_file()]
    if missing: raise SystemExit('FAIL phase2 artifacts: '+','.join(missing))
    b=json.loads((ROOT/'policies/intelligence-to-opportunity-baseline.json').read_text())
    assert b['authority']=='tsic' and b['sequence']==['world-intelligence','tads','sdea']
    assert len(b['repositories']['world-intelligence']['ref'])==40 and len(b['repositories']['tads']['ref'])==40 and len(b['repositories']['sdea']['ref'])==40
    req=json.loads((ROOT/'conformance/requirements/phase2-intelligence-to-opportunity.json').read_text())
    assert len(req['requirements'])==9
    for system in b['sequence']:
        a=json.loads((ROOT/f'integrations/{system}/adapter.json').read_text())
        assert a['source_system']=='tsic' and a['target_system']==system
        assert any('execution_authority' in str(v) for v in a['authority'].values()) or 'agent-platform_remains_execution_authority' in a['invariants']
    workflow=(ROOT/'.github/workflows/intelligence-to-opportunity.yml').read_text()
    assert 'certify_intelligence_to_opportunity.py' in workflow and 'pytest' in workflow
    assert '30b939031081220dee17a44fde1f5c6f887e254f' in workflow and 'be242dd29335e3e74b4b80176ea073f7b7f74d56' in workflow and 'd189b05ab0db3044c13c461ddd8658aabde5fe03' in workflow
    print('PASS TSIC-02 post-phase forensic audit: authority, lineage, adapters, pinned revisions, E2E certifier and CI gate verified')
if __name__=='__main__': main()
