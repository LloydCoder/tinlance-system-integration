#!/usr/bin/env python3
"""Certify the TWI -> World Intelligence source-evidence integration boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL TWI integration: {message}")


def main() -> None:
    manifest = load("manifests/ecosystem.json")
    systems = {item["id"]: item for item in manifest["systems"]}
    twi = systems.get("web-intelligence")
    require(twi is not None, "web-intelligence is not registered")
    require(
        twi["repository"] == "LloydCoder/tinlance-web-intelligence",
        "repository identity drift",
    )
    require(
        twi["governance_role"] == "web_intelligence_acquisition_authority",
        "governance role drift",
    )
    allowed_authority = {
        "web_search_and_fetch",
        "browser_capture",
        "source_evidence_acquisition",
        "source_change_monitoring",
    }
    require(set(twi["authority"]) == allowed_authority, "TWI authority set drift")
    forbidden_authority = {
        "identity",
        "authorization",
        "policy",
        "runtime",
        "mcp",
        "sandbox",
        "secrets",
        "budgets",
        "audit",
        "world_intelligence",
        "canonical_world_state",
        "execution",
    }
    require(not (set(twi["authority"]) & forbidden_authority), "TWI claims a forbidden authority")

    graph = load("catalog/dependencies/graph.json")
    nodes = {item["system"]: item for item in graph["nodes"]}
    require(nodes.get("web-intelligence", {}).get("ci_gate") == "TSIC-16", "TWI MCP gate drift")
    edges = {(item["from"], item["to"], item["reason"]) for item in graph["edges"]}
    require(
        ("agent-platform", "web-intelligence", "governed_web_acquisition") in edges,
        "Platform -> TWI governed acquisition edge missing",
    )
    require(
        ("web-intelligence", "world-intelligence", "candidate_source_evidence_intake") in edges,
        "TWI -> World Intelligence candidate evidence edge missing",
    )

    services = {item["id"]: item for item in load("catalog/services/registry.json")["services"]}
    require(
        services.get("web-intelligence", {}).get("protocols") == ["https"],
        "TWI must be registered as an HTTPS service, not an independent MCP authority",
    )
    contracts = {
        item["id"]: item
        for item in load("catalog/contracts/registry.json")["contracts"]
    }
    require(
        contracts.get("twi-source-evidence-intake", {}).get("version") == "1.0.0",
        "source evidence intake contract version missing",
    )
    adapters = {
        item["id"]: item
        for item in load("integrations/adapters/registry.json")["adapters"]
    }
    require(
        adapters.get("agent-platform-to-web-intelligence", {}).get("transport") == "governed-api",
        "Platform adapter must use governed API access",
    )
    require(
        adapters.get("web-intelligence-to-world-intelligence-source-evidence", {}).get("transport")
        == "contracted-api",
        "source evidence adapter contract missing",
    )
    phase16 = next(
        item for item in load("catalog/phases/registry.json")["sequence"]
        if item["id"] == "TSIC-16"
    )
    require("web-intelligence" in phase16["systems"], "TWI is absent from TSIC-16 scope")

    authority = load("catalog/capabilities/authority.json")["capabilities"]
    owned = {item["capability"] for item in authority if item["owner"] == "web-intelligence"}
    require(owned == allowed_authority, "capability ownership does not match TWI authority")

    contract = load("contracts/integrations/twi-source-evidence-v1.json")
    required = set(contract["required"])
    require(contract["additionalProperties"] is False, "intake contract must reject unknown fields")
    require(contract["properties"]["schema_version"].get("const") == "1.0.0", "contract version drift")
    require(
        contract["properties"]["source_system"].get("const") == "tinlance-web-intelligence",
        "source system identity drift",
    )
    require(
        {"tenant_ref", "source_url", "artifact_sha256", "quote_sha256", "verifier_version", "report_sha256"}
        <= required,
        "provenance-critical fields are missing",
    )
    require(
        "canonical_observation" not in contract["properties"]
        and "world_state" not in contract["properties"],
        "TWI intake must remain candidate evidence, not canonical world state",
    )
    print(
        "PASS TWI integration: registered authority boundary, Platform-governed API, "
        "versioned source evidence contract, and TSIC-16 conformance"
    )


if __name__ == "__main__":
    main()
