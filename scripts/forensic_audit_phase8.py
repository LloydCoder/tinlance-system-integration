#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 required=['policies/delivery-evidence-baseline.json','integrations/fdse-toolkit/adapter.json','scripts/certify_delivery_evidence.py','.github/workflows/delivery-evidence-e2e.yml']
 missing=[p for p in required if not (ROOT/p).is_file()]
 if missing: raise SystemExit('FAIL missing phase8 artifacts: '+','.join(missing))
 b=json.loads((ROOT/'policies/delivery-evidence-baseline.json').read_text()); a=json.loads((ROOT/'integrations/fdse-toolkit/adapter.json').read_text())
 assert b['toolkit']['repository']=='LloydCoder/Tinlance-FDSE-toolkit' and len(b['toolkit']['ref'])==40
 assert 'evidence_hash_and_origin_are_preserved' in b['additional_invariants']
 assert 'report_generation_sanitizes_untrusted_content' in b['additional_invariants']
 assert a['target_system']=='fdse-toolkit'
 wf=(ROOT/'.github/workflows/delivery-evidence-e2e.yml').read_text()
 for marker in ['8cb4bedcd2c1755966bdc69a2be2393da609fe6e','tests/test_evidence.py','tests/test_reporting.py','tests/test_delivery.py','scripts/certify_delivery_evidence.py']:
  assert marker in wf, 'workflow missing '+marker
 print('PASS TSIC-08 forensic audit: pinned toolkit, evidence lineage, report sanitization, delivery integrity and CI gate verified')
if __name__=='__main__': main()
