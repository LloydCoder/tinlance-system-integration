import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/provider-adapter-boundary.schema.json"
CONTRACT_PATH = ROOT / "contracts/models/provider-adapter-boundary.json"
RULES_PATH = ROOT / "integrations/adapters/rules.json"


def test_provider_adapter_boundary_contract_matches_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(contract)


def test_provider_adapter_rules_preserve_authority_and_transport_safety() -> None:
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))["rules"]
    required = {
        "adapter_must_not_own_authorization",
        "adapter_must_propagate_identity",
        "adapter_must_emit_trace_context",
        "adapter_must_validate_contract_version",
        "adapter_must_not_store_secrets",
        "adapter_must_emit_audit_evidence_reference",
        "adapter_endpoint_must_come_from_trusted_configuration",
        "adapter_must_reject_redirects",
        "adapter_must_bound_payloads_and_timeouts",
        "adapter_must_propagate_valid_w3c_traceparent",
        "adapter_must_not_persist_or_log_secrets",
        "adapter_must_not_forward_tenant_or_agent_ids_to_external_model_providers_by_default",
        "adapter_must_not_automatically_retry_ambiguous_billed_operations",
    }
    assert required <= set(rules)
