"""Validate TWI's TSIC integration manifest, registry links, and authority boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    adapter = read_json("integrations/tinlance-web-intelligence/adapter.json")
    ecosystem = read_json("manifests/ecosystem.json")
    services = read_json("catalog/services/registry.json")
    adapters = read_json("integrations/adapters/registry.json")
    schema = read_json("schemas/ecosystem-manifest.schema.json")

    assert adapter["target_system"] == "tinlance-web-intelligence"
    authority = adapter["authority"]
    assert authority["web_discovery_and_acquisition"] == "tinlance-web-intelligence"
    assert authority["identity_authorization_policy_approval_execution_audit"] == "agent-platform"
    assert authority["world_state_semantics_and_canonical_entities"] == "world-intelligence"
    forbidden = {"identity", "authorization", "policy", "approval", "execution", "audit"}
    assert not forbidden.intersection(adapter.get("owned_authorities", []))

    systems = {item["id"]: item for item in ecosystem["systems"]}
    assert systems["tinlance-web-intelligence"]["repository"] == (
        "LloydCoder/tinlance-web-intelligence"
    )
    assert "web_intelligence_acquisition_authority" in schema["$defs"]["system"]["properties"][
        "governance_role"
    ]["enum"]
    service_ids = {item["id"] for item in services["services"]}
    assert "tinlance-web-intelligence" in service_ids
    edge_ids = {item["id"] for item in adapters["adapters"]}
    assert {"agent-platform-to-twi", "twi-to-world-intelligence"}.issubset(edge_ids)

    invariants = set(adapter["invariants"])
    required = {
        "agent-platform_is_the_sole_identity_authorization_policy_approval_execution_and_audit_authority",
        "world-intelligence_owns_canonical_entities_events_relationships_and_temporal_world_state",
        "web_content_is_untrusted_data_not_authority",
        "source_evidence_export_is_idempotent_and_approval_gated_by_platform",
        "tsic_remains_the_cross_repository_contract_and_conformance_authority",
    }
    assert required.issubset(invariants)
    assert any(binding["tsic_contract"] == "delivery-semantics"
               for binding in adapter["contract_bindings"])
    assert any(binding["tsic_contract"] == "trace-context"
               for binding in adapter["contract_bindings"])
    print("TWI TSIC integration manifest and authority boundary verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
