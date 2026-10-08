#!/usr/bin/env python3
"""Certify the reviewed Tinlance Acquisition System baseline."""
from __future__ import annotations
import json
from urllib.request import Request, urlopen

ROOT="https://raw.githubusercontent.com/LloydCoder/tinlance-system-integration/main"

def fetch(path):
    req=Request(f"{ROOT}/{path}",headers={"Accept":"application/json","User-Agent":"tinlance-tsic-certifier"})
    with urlopen(req,timeout=15) as res: return json.load(res)

def main():
    b=fetch("policies/acquisition-system-baseline.json")
    m=fetch("manifests/ecosystem.json")
    r=fetch("catalog/contracts/registry.json")
    assert b["authority"]=="tsic"
    assert b["sequence"]==["world-intelligence","tads","sdea","reconos","fadereach"]
    systems={x["id"]:x for x in m["systems"]}
    for sid in b["sequence"]:
        assert sid in systems
        assert systems[sid]["repository"]==b["systems"][sid]["repository"]
        assert systems[sid]["repository"] is not None
    required={"identity-context","event-envelope","delivery-semantics","trace-context","economic-attribution"}
    assert {x["id"] for x in r["contracts"]} >= required
    for sid in b["required_adapters"]:
        adapter=fetch(f"integrations/{sid}/adapter.json")
        assert adapter["source_system"]=="tsic" and adapter["target_system"]==sid
        assert {x["tsic_contract"] for x in adapter["contract_bindings"]}==required
        assert "tsic_remains_integration_authority" in adapter["invariants"]
        assert "agent-platform-remains-execution-authority" in adapter["invariants"] or "agent-platform_remains_execution_authority" in adapter["invariants"]
    print("PASS TSIC-25 Acquisition System certification")
if __name__=="__main__": main()
