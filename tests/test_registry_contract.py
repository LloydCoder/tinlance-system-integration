import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/registry/v1/registry-manifest.schema.json"
CONTRACT = ROOT / "contracts/registry/registry-contract.json"


def valid_registry():
    repos = [
        {"id": "developer", "repository": "LloydCoder/tinlance-agent-developer", "reviewed_sha": "a" * 40, "role": "artifact validator"},
        {"id": "os", "repository": "LloydCoder/tinlance-agent-os", "reviewed_sha": "b" * 40, "role": "lifecycle orchestration"},
        {"id": "platform", "repository": "LloydCoder/tinlance-agent-platform", "reviewed_sha": "c" * 40, "role": "sole execution authority"},
        {"id": "platform_sdk", "repository": "LloydCoder/tinlance-agent-platform-sdk", "reviewed_sha": "d" * 40, "role": "typed API"},
        {"id": "tsic", "repository": "LloydCoder/tinlance-system-integration", "reviewed_sha": "e" * 40, "role": "conformance authority"},
    ]
    return {
        "schema_version": "registry-manifest/v1",
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
        }],
        "agents": [{
            "agent_id": "reference.enterprise",
            "owner_repository_id": "platform",
            "version": "1.0.0",
            "capabilities": ["agent.execute"],
            "required_contracts": {"governed-execution.v1": "1.0"},
            "authority_mode": "delegated_only",
        }],
        "contracts": [{
            "contract_id": "governed-execution.v1",
            "version": "1.0",
            "schema_path": "schemas/governed-execution/v1/schema.json",
            "owner_repository_id": "platform",
            "compatibility": "versioned_immutable",
        }],
        "compatibility_rules": [{
            "consumer_id": "agent-os.runtime",
            "contract_id": "governed-execution.v1",
            "supported_versions": ["1.0"],
            "reject_unknown": True,
            "reject_stale": True,
            "reject_missing": True,
        }],
    }


def test_registry_schema_and_contract_are_versioned():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert schema["properties"]["schema_version"]["const"] == "registry-manifest/v1"
    assert contract["format"] == "tinlance-canonical-ecosystem-registry/v1"
    assert contract["schema"] == "schemas/registry/v1/registry-manifest.schema.json"


def test_registry_schema_accepts_complete_registration_and_rejects_missing_contract():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    registry = valid_registry()
    assert validator.is_valid(registry)
    broken = json.loads(json.dumps(registry))
    broken["services"][0].pop("contract_ids")
    assert not validator.is_valid(broken)


def test_registry_schema_forbids_authority_mode_drift_and_non_sha_pins():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    registry = valid_registry()
    registry["services"][0]["authority_mode"] = "shared_execution_authority"
    assert not validator.is_valid(registry)
    registry = valid_registry()
    registry["repositories"][0]["reviewed_sha"] = "main"
    assert not validator.is_valid(registry)
