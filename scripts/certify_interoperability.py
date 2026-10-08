import json
from pathlib import Path
def main():
 b=json.loads((Path(__file__).parents[1]/"policies/interoperability-baseline.json").read_text())
 assert b["authority"]=="tsic"
 assert b["mcp_specification"]=="2026-07-28"
 assert b["a2a_specification"]=="1.0.0"
 assert b["boundaries"]["mcp"]=="agent-to-tool/context integration"
 assert b["boundaries"]["a2a"]=="agent-to-agent communication"
 assert {"identity_and_authorization_are_explicit","capabilities_are_versioned","delegation_is_bounded","trace_context_is_propagated"}<=set(b["invariants"])
 print("PASS TSIC-37 interoperability certification")
if __name__=="__main__": main()
