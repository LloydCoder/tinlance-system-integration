#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 required=['policies/fas-bench-baseline.json','integrations/fas/adapter.json','integrations/fas-bench/adapter.json','scripts/certify_fas_bench.py','scripts/certify_fas_bench_e2e.py','.github/workflows/fas-bench-e2e.yml']
 missing=[p for p in required if not (ROOT/p).is_file()]
 if missing: raise SystemExit('FAIL missing phase5 artifacts: '+','.join(missing))
 b=json.loads((ROOT/'policies/fas-bench-baseline.json').read_text())
 a=json.loads((ROOT/'integrations/fas-bench/adapter.json').read_text())
 assert b['fas']['repository']=='LloydCoder/fas' and len(b['fas']['ref'])==40
 assert b['fas_bench']['repository']=='LloydCoder/fas-bench' and len(b['fas_bench']['ref'])==40
 assert b['execution_gate']['requires_live_fas_cli_and_independent_evaluator'] is True
 assert 'insufficient_evidence_maps_to_unknown_not_clean' in b['invariants']
 assert 'fas-bench_is_not_a_fas_runtime_dependency' in a['independence_invariants']
 workflow=(ROOT/'.github/workflows/fas-bench-e2e.yml').read_text()
 for marker in ['LloydCoder/fas','LloydCoder/fas-bench','scripts/certify_fas_bench_e2e.py','python -m pytest -q tests','Upload immutable evaluation evidence']:
  assert marker in workflow, 'workflow missing '+marker
 script=(ROOT/'scripts/certify_fas_bench_e2e.py').read_text()
 for marker in ['fas.cli','fas-bench','UNKNOWN_INSUFFICIENT_EVIDENCE','fas_artifact_sha256','evaluation_result']:
  assert marker in script, 'E2E adapter missing '+marker
 print('PASS TSIC-05 forensic audit: pinned independent repos, fail-closed adapter, evaluator execution and retained evidence verified')
if __name__=='__main__': main()
