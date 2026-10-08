#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())
def main():
 b=load("policies/threatfade-baseline.json"); a=load("integrations/threatfade/adapter.json"); r=load("catalog/contracts/registry.json")
 assert len(b["threatfade"]["ref"])==40
 req={"identity-context","event-envelope","delivery-semantics","trace-context","economic-attribution"}
 assert {x["id"] for x in r["contracts"]}>=req
 assert {x["tsic_contract"] for x in a["contract_bindings"]}==req
 assert set(b["invariants"])==set(a["invariants"])
 assert a["authority"]=={"integration_contracts":"tsic","threat_detection_response":"threatfade","execution_authority":"agent-platform"}
 print("PASS TSIC-31 ThreatFade certification")
if __name__=="__main__": main()
