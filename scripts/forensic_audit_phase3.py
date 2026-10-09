#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    required=['scripts/certify_reconos_acquisition.py','policies/reconos-acquisition-baseline.json','conformance/requirements/phase3-reconos.json','.github/workflows/reconos-acquisition.yml','integrations/reconos/adapter.json']
    missing=[p for p in required if not (ROOT/p).is_file()]
    if missing: raise SystemExit('FAIL phase3 artifacts: '+','.join(missing))
    b=json.loads((ROOT/'policies/reconos-acquisition-baseline.json').read_text())
    assert b['authority']=='tsic' and b['target']=='reconos' and len(b['repository']['ref'])==40
    a=json.loads((ROOT/'integrations/reconos/adapter.json').read_text())
    assert a['source_system']=='tsic' and a['target_system']=='reconos'
    assert 'external_data_is_untrusted' in b['invariants'] and 'agent-platform-remains-execution-authority' in b['invariants']
    workflow=(ROOT/'.github/workflows/reconos-acquisition.yml').read_text()
    assert 'forensic_audit_phase3.py' in workflow and 'source_owned_certifier' in workflow
    assert b['repository']['ref']=='4b95e18f21ac7d5b820267f5f09780aa450606ae'
    req=json.loads((ROOT/'conformance/requirements/phase3-reconos.json').read_text()); assert len(req['requirements'])==9
    print('PASS TSIC-03 post-phase forensic audit: ReconOS boundary, lineage, deduplication, authority and pinned CI verified')
if __name__=='__main__': main()
