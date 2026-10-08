#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())
def main():
 b=load("policies/hezqara-baseline.json"); a=load("integrations/hezqara/adapter.json"); r=load("catalog/contracts/registry.json")
 req={"identity-context","event-envelope","delivery-semantics","trace-context","economic-attribution"}
 assert len(b["hezqara"]["ref"])==40
 assert {x["id"] for x in r["contracts"]}>=req
 assert {x["tsic_contract"] for x in a["contract_bindings"]}==req
 assert set(b["invariants"])==set(a["invariants"])
 assert a["authority"]=={"integration_contracts":"tsic","healthcare_workforce":"hezqara","execution_authority":"agent-platform"}
 print("PASS TSIC-33 Hezqara certification")
if __name__=="__main__": main()
