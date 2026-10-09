#!/usr/bin/env python3
"""Certify MCP/A2A compatibility contracts and authority boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load("policies/interoperability-baseline.json")
    gate = load("contracts/agents/interoperability-gate.json")
    registration = load("contracts/agents/registration.json")
    phases = load("catalog/phases/registry.json")
    assert baseline["authority"] == "tsic"
    assert baseline["mcp_specification"] == "2026-07-28"
    assert baseline["a2a_specification"] == "1.0.0"
    assert baseline["boundaries"]["mcp"] == "agent-to-tool/context integration"
    assert baseline["boundaries"]["a2a"] == "agent-to-agent communication"
    assert gate["schema_version"] == "1.1.0"
    assert gate["protocols"]["mcp"]["specification"] == baseline["mcp_specification"]
    assert gate["protocols"]["a2a"]["specification"] == baseline["a2a_specification"]
    assert gate["protocols"]["mcp"]["authorization_authority"] == "agent-platform"
    assert gate["protocols"]["a2a"]["authorization_authority"] == "agent-platform"
    assert gate["boundaries"]["tsic"] == "ecosystem integration/certification"
    assert gate["boundaries"]["agent_platform"].startswith("identity, authorization")
    rules = gate["rules"]
    required_rules = {
        "capability_discovery_required", "capabilities_must_be_versioned",
        "identity_propagation_required", "policy_check_required", "tenant_context_required",
        "delegation_must_be_scoped_and_expiring", "trace_context_required",
        "idempotency_and_replay_protection_required", "audit_required",
        "protocol_metadata_is_untrusted", "protocol_support_never_grants_execution_authority",
        "tool_arguments_are_untrusted", "remote_response_size_and_timeout_limits_required",
    }
    assert required_rules <= set(rules)
    assert all(rules[key] is True for key in required_rules)
    assert registration["authority"] == "agent-platform"
    assert {"agent_id", "agent_version", "capabilities", "risk_class", "lifecycle_state"} <= set(registration["required"])
    assert "mcp_and_a2a_are_complementary" in baseline["invariants"]
    assert "tool_calls_are_authorized_by_agent_platform" in baseline["invariants"]
    assert "remote_delegation_has_scope_and_expiry" in baseline["invariants"]
    assert "protocol_metadata_is_untrusted_input" in baseline["invariants"]

    # Negative cases: protocol support or metadata must never create execution authority.
    assert gate["protocols"]["mcp"]["authorization_authority"] != "mcp"
    assert gate["protocols"]["a2a"]["authorization_authority"] != "a2a"
    assert gate["rules"]["protocol_support_never_grants_execution_authority"] is True
    assert gate["rules"]["delegation_must_be_scoped_and_expiring"] is True
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    assert status["TSIC-15"] == "completed"
    assert status["TSIC-16"] in {"in_progress", "completed"}
    print("PASS TSIC-16 interoperability: pinned MCP/A2A specs, explicit authz, bounded delegation, untrusted metadata and audit")


if __name__ == "__main__":
    main()
