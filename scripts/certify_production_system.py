#!/usr/bin/env python3
"""Certify ecosystem-wide registration, dependency integrity, and authority uniqueness."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load("policies/production-system-baseline.json")
    ecosystem = load("manifests/ecosystem.json")
    graph = load("catalog/dependencies/graph.json")
    services = load("catalog/services/registry.json")
    capabilities = load("catalog/capabilities/authority.json")
    contracts = load("catalog/contracts/registry.json")
    phases = load("catalog/phases/registry.json")
    systems = ecosystem["systems"]
    system_ids = [item["id"] for item in systems]
    system_set = set(system_ids)
    assert len(system_ids) == len(system_set), "duplicate ecosystem system IDs"
    assert ecosystem["ecosystem"]["integration_authority"] == "tsic"
    assert graph["authority"] == "tsic"
    graph_nodes = graph["nodes"]
    node_ids = [item["system"] for item in graph_nodes]
    node_set = set(node_ids)
    assert len(node_ids) == len(node_set), "duplicate dependency graph nodes"
    assert node_set <= system_set, f"graph nodes missing from ecosystem manifest: {sorted(node_set - system_set)}"
    assert system_set <= node_set, f"manifest systems missing graph nodes: {sorted(system_set - node_set)}"
    for edge in graph["edges"]:
        assert edge["from"] in node_set, f"unknown dependency source: {edge['from']}"
        assert edge["to"] in node_set, f"unknown dependency target: {edge['to']}"
        assert edge["from"] != edge["to"], f"self dependency: {edge['from']}"
        assert edge.get("reason"), f"dependency edge missing rationale: {edge}"

    roles = [item.get("governance_role") for item in systems]
    assert roles.count("execution_authority") == 1, "generic execution authority must be unique"
    platform = next(item for item in systems if item["id"] == "agent-platform")
    assert platform["governance_role"] == "execution_authority"
    assert "authorization" in platform["authority"] and "policy" in platform["authority"]
    sdk = next(item for item in systems if item["id"] == "agent-platform-sdk")
    assert sdk["governance_role"] == "developer_client_surface"
    assert "authorization" not in sdk["authority"]

    required_boundaries = {
        "agent-platform-execution-authority",
        "agent-os-workspace-lifecycle-authority",
        "fdse-delivery-orchestration-authority",
        "fas-evidence-analysis-authority",
        "domain-system-authority",
        "tsic-integration-certification-authority",
        "hezcast-content-generation-authority",
        "agent-platform-governed-publishing-authority",
    }
    assert set(baseline["required_boundaries"]) == required_boundaries
    assert baseline["authority"] == "tsic"
    required_contracts = {"identity-context", "event-envelope", "delivery-semantics", "trace-context", "economic-attribution"}
    hezcast = next(item for item in systems if item["id"] == "hezcast")
    assert hezcast["repository"] == "LloydCoder/hezcast-engine"
    assert hezcast["governance_role"] == "content_generation_authority"
    assert "content_generation" in hezcast["authority"]
    assert "external_content_publishing" not in hezcast["authority"]
    assert any(edge["from"] == "hezcast" and edge["to"] == "agent-platform" and edge["reason"] == "governed_external_publishing" for edge in graph["edges"])
    assert any(edge["from"] == "hezcast" and edge["to"] == "fadereach" and edge["reason"] == "content_bundle_handoff" for edge in graph["edges"])
    assert any(service["id"] == "hezcast" and service["system"] == "hezcast" and {"https", "events", "artifacts"} <= set(service["protocols"]) for service in services["services"])
    capability_owners = {item["capability"]: item["owner"] for item in capabilities["capabilities"]}
    assert capability_owners.get("content_generation") == "hezcast"
    hezcast_saas = next(item for item in systems if item["id"] == "hezcast-saas")
    assert hezcast_saas["repository"] == "LloydCoder/hezcast-saas"
    assert hezcast_saas["governance_role"] == "content_product_experience_authority"
    assert capability_owners.get("content_product_experience") == "hezcast-saas"
    assert any(edge["from"] == "hezcast-saas" and edge["to"] == "hezcast" and edge["reason"] == "content_generation_api_client" for edge in graph["edges"])
    assert capability_owners.get("external_content_publishing") == "agent-platform"
    adapter = load("integrations/hezcast/adapter.json")
    assert adapter["authority"]["content_generation"] == "hezcast"
    assert adapter["authority"]["external_publishing_execution"] == "agent-platform"
    assert adapter["authority"]["commercial_entitlement"] == "tinlance-com"
    assert "external_publish_requires_agent_platform_authorization" in adapter["invariants"]
    registered_contracts = {item["id"] for item in contracts["contracts"]}
    assert required_contracts <= registered_contracts

    sequence = phases["sequence"]
    ids = [item["id"] for item in sequence]
    expected_ids = [f"TSIC-{index:02d}" for index in range(20)]
    assert ids == expected_ids, "canonical TSIC phase sequence must be contiguous TSIC-00..19"
    status = {item["id"]: item["status"] for item in sequence}
    assert status["TSIC-16"] == "completed"
    assert status["TSIC-17"] in {"in_progress", "completed"}
    assert all(status[f"TSIC-{index:02d}"] == "completed" for index in range(17)), "upstream serial gates must be completed"
    required_invariants = {
        "no_duplicate_consequential_execution_authority",
        "all_cross-system_events_are_traceable",
        "all_registered_systems_have_contracts_or_explicit_non_runtime_model_status",
        "recovery_is_replay_safe",
        "dependency_graph_endpoints_are_registered",
        "generic_execution_authority_is_unique",
        "phase_registry_is_contiguous_and_serial",
        "all_production_claims_are_evidence_bounded",
        "contracts_and_adapters_have_explicit_owners",
    }
    assert required_invariants <= set(baseline["invariants"])
    print("PASS TSIC-17 production system-of-systems certification: graph/manifest parity, unique execution authority, contract registry and serial phase gates")


if __name__ == "__main__":
    main()
