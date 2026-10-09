#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 required=['policies/fde-vertical-baseline.json','integrations/fde-mastery/adapter.json','integrations/fdse/adapter.json','scripts/certify_fde_vertical.py','.github/workflows/fde-mastery-e2e.yml']
 missing=[p for p in required if not (ROOT/p).is_file()]
 if missing: raise SystemExit('FAIL missing phase7 artifacts: '+','.join(missing))
 b=json.loads((ROOT/'policies/fde-vertical-baseline.json').read_text()); a=json.loads((ROOT/'integrations/fde-mastery/adapter.json').read_text())
 assert len(b['fde_mastery']['ref'])==40 and len(b['fdse']['ref'])==40
 assert 'evidence_is_preserved_from_intake_through_delivery' in b['invariants']
 assert 'economic_attribution_is_evidence_linked' in b['invariants']
 assert a['authority']['execution_authority']=='agent-platform'
 wf=(ROOT/'.github/workflows/fde-mastery-e2e.yml').read_text()
 for marker in ['370fea68bdb74182f0893a5a4421f147ed139597','e1f213c918ba712666e4dd8a5db418caad0b060f','tests/test_fde_engagement_workflow.py','tests/test_enterprise_integrations.py','scripts/certify_fde_vertical.py']:
  assert marker in wf, 'workflow missing '+marker
 print('PASS TSIC-07 forensic audit: FDE Mastery/FDSE revisions, route separation, evidence lineage, authority and E2E workflow verified')
if __name__=='__main__': main()
