import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/registry/v2/registry-manifest.schema.json").read_text())
CONTRACT = json.loads((ROOT / "contracts/registry/registry-contract.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def lifecycle(state="active", reason=None, replacement_id=None):
    return {
        "state": state,
        "changed_at": "2026-10-18T00:00:00Z",
        "reason": reason,
        "replacement_id": replacement_id,
    }


def repository(repo_id, repo_name, sha):
    return {
        "id": repo_id,
        "repository": repo_name,
        "reviewed_sha": sha,
        "role": "test fixture",
        "publisher": {
            "publisher_id": "LloydCoder",
            "identity_uri": "https://github.com/LloydCoder",
            "identity_status": "unverified",
        },
        "lifecycle": lifecycle(),
        "supply_chain": {
            "reviewed_sha": sha,
            "provenance_uri": f"https://github.com/{repo_name}/commit/{sha}",
            "sbom_uri": f"https://github.com/{repo_name}/attestations",
            "signature_uri": f"https://github.com/{repo_name}/attestations",
            "verification_status": "pending",
        },
    }


def valid_registry():
    repos = [
        repository("developer", "LloydCoder/tinlance-agent-developer", "a" * 40),
        repository("os", "LloydCoder/tinlance-agent-os", "b" * 40),
        repository("platform", "LloydCoder/tinlance-agent-platform", "c" * 40),
        repository("platform_sdk", "LloydCoder/tinlance-agent-platform-sdk", "d" * 40),
        repository("tsic", "LloydCoder/tinlance-system-integration", "e" * 40),
    ]
    return {
        "schema_version": "registry-manifest/v2",
        "registry_id": "tinlance.agent.ecosystem",
        "baseline_id": "test-baseline",
        "repositories": repos,
        "services": [{
            "service_id": "agent-platform.api",
            "owner_repository_id": "platform",
            "version": "1.0.0",
            "api_version": "1.1",
            "contract_ids": ["governed-execution.v1"],
            "capabilities": ["agent.execute"],
            "authority_mode": "sole_consequential_execution",
            "enabled": True,
            "lifecycle": lifecycle(),
        }],
        "agents": [{
            "agent_id": "reference.enterprise",
            "owner_repository_id": "platform",
            "version": "1.0.0",
            "capabilities": ["agent.execute"],
            "required_contracts": {"governed-execution.v1": "1.0"},
            "authority_mode": "delegated_only",
            "lifecycle": lifecycle(),
        }],
        "contracts": [{
            "contract_id": "governed-execution.v1",
            "version": "1.0",
            "schema_path": "contracts/governed-execution.json",
            "owner_repository_id": "platform",
            "compatibility": "versioned_immutable",
            "lifecycle": lifecycle(),
        }],
        "compatibility_rules": [{
            "consumer_id": "agent-platform.api",
            "contract_id": "governed-execution.v1",
            "supported_versions": ["1.0"],
            "reject_unknown": True,
            "reject_stale": True,
            "reject_missing": True,
        }],
    }


def test_v2_registry_schema_accepts_explicit_unverified_supply_chain_state():
    errors = list(VALIDATOR.iter_errors(valid_registry()))
    assert errors == []


@pytest.mark.parametrize("state,reason,replacement", [
    ("quarantined", None, None),
    ("revoked", "", None),
    ("deprecated", "superseded", None),
])
def test_lifecycle_fails_closed_when_required_reason_or_replacement_is_missing(state, reason, replacement):
    registry = valid_registry()
    registry["services"][0]["lifecycle"] = lifecycle(state, reason, replacement)
    assert list(VALIDATOR.iter_errors(registry))


def test_missing_sbom_or_signature_reference_is_rejected():
    registry = valid_registry()
    del registry["repositories"][0]["supply_chain"]["sbom_uri"]
    assert list(VALIDATOR.iter_errors(registry))


def test_registry_contract_explicitly_preserves_non_authority_and_supply_chain_rules():
    invariants = " ".join(CONTRACT["invariants"]).lower()
    assert "registry metadata alone never establishes cryptographic trust" in invariants
    assert "quarantined" in invariants and "revoked" in invariants and "deprecated" in invariants
