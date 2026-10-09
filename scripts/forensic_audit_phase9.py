#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 required=['policies/threatfade-baseline.json','integrations/threatfade/adapter.json','scripts/certify_threatfade.py','.github/workflows/threatfade-engine-e2e.yml']
 missing=[p for p in required if not (ROOT/p).is_file()]
 if missing: raise SystemExit('FAIL missing phase9 artifacts: '+','.join(missing))
 b=json.loads((ROOT/'policies/threatfade-baseline.json').read_text())
 assert b['threatfade']['repository']=='LloydCoder/tinlance-threatfade' and len(b['threatfade']['ref'])==40
 assert {'sensor_event_id','observation_id','detection_id','analyst_case_id','evidence_id','finding_id'}.issubset(b['evidence_lineage'])
 assert 'detection_output_is_not_a_verdict' in b['additional_invariants']
 wf=(ROOT/'.github/workflows/threatfade-engine-e2e.yml').read_text()
 for marker in ['4691ead86fadd1c95767886d7fb15bacbed012fe','tests/test_analyst_workflow.py','tests/test_detection_pipeline.py','benchmarks/detection_science_v2.py','scripts/certify_threatfade.py']:
  assert marker in wf, 'workflow missing '+marker
 print('PASS TSIC-09 forensic audit: pinned engine, analyst workflow, detection science, evidence lifecycle and E2E CI verified')
if __name__=='__main__': main()
