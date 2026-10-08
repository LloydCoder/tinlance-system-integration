import json
from pathlib import Path
def main():
 b=json.loads((Path(__file__).parents[1]/"policies/observability-baseline.json").read_text())
 assert b["authority"]=="tsic" and b["otel_semantic_conventions"]
 assert len(b["canonical_fields"])>=14
 assert {"trace_id","correlation_id","event_id","evidence_id"}<=set(b["canonical_fields"])
 assert {"trace_context_is_propagated","correlation_is_stable","semantic_convention_version_is_pinned"}<=set(b["invariants"])
 print("PASS TSIC-36 observability certification")
if __name__=="__main__": main()
