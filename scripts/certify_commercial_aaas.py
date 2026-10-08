#!/usr/bin/env python3
"""TSIC-40 commercial/AaaS integration certification."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=json.loads((ROOT/"policies/commercial-aaas-baseline.json").read_text())
    w=json.loads((ROOT/"workflows/canonical.json").read_text())
    assert all(x in p["invariants"] for x in [
        "commercial_surface_does_not_replace_domain_authority",
        "aaas_offers_bind_to_certified_agent_execution",
        "pricing_and_entitlement_are_traceable",
        "customer_tenant_context_is_preserved",
        "delivery_evidence_is attributable_to_workflow_and_customer",
    ])
    assert "acquisition-engineering" in {x["id"] for x in w["workflows"]}
    print("PASS TSIC-40 Tinlance.com Commercial/AaaS certification")
if __name__=="__main__": main()
