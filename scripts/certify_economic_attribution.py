import json
from pathlib import Path
def main():
 b=json.loads((Path(__file__).parents[1]/"policies/economic-attribution-baseline.json").read_text())
 assert b["authority"]=="tsic"
 assert len(b["canonical_fields"])>=20
 for x in ["tenant_id","account_id","signal_id","opportunity_id","agent_id","execution_id","delivery_id","trace_id","evidence_id","cost_amount","revenue_amount","delivery_route"]:
  assert x in b["canonical_fields"]
 assert set(["attribution_is_traceable","cost_and_revenue_are_distinct","delivery_route_is_explicit"])<=set(b["invariants"])
 print("PASS TSIC-34 economic attribution certification")
if __name__=="__main__": main()
