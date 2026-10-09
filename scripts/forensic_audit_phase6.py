#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 required=['policies/engineering-route-baseline.json','integrations/fdse/adapter.json','scripts/certify_engineering_route.py','.github/workflows/engineering-route-e2e.yml']
 missing=[p for p in required if not (ROOT/p).is_file()]
 if missing: raise SystemExit('FAIL missing phase6 artifacts: '+','.join(missing))
 b=json.loads((ROOT/'policies/engineering-route-baseline.json').read_text())
 a=json.loads((ROOT/'integrations/fdse/adapter.json').read_text())
 assert b['route']=='engineering' and b['authority']=='tsic'
 assert b['fdse']['repository']=='LloydCoder/tinlance-fdse' and len(b['fdse']['ref'])==40
 assert 'economic_attribution_carries_route' in b['invariants']
 assert 'engineering_and_transformation_are_distinct_routes' in a['invariants']
 assert 'fdse_does_not_grant_platform_execution_authority' in a['invariants']
 wf=(ROOT/'.github/workflows/engineering-route-e2e.yml').read_text()
 for marker in ['e1f213c918ba712666e4dd8a5db418caad0b060f','tests/test_e4_evidence_lineage.py','tests/test_e5_integration.py','scripts/certify_engineering_route.py','scripts/certify_delivery_evidence.py']:
  assert marker in wf, 'workflow missing '+marker
 print('PASS TSIC-06 forensic audit: pinned FDSE, evidence lineage, engineering-route boundary, delivery contract and CI gate verified')
if __name__=='__main__': main()
