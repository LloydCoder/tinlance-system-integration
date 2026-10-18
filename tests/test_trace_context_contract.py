import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/trace-context/v1/trace-context.schema.json"
CONTRACT = ROOT / "contracts/tracing/trace-context.json"


def test_trace_context_contract_and_schema_are_versioned_and_aligned():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert schema["properties"]["schema_version"]["const"] == "trace-context/v1"
    assert contract["format"] == "tinlance-trace-context/v1"
    assert contract["schema"] == "schemas/trace-context/v1/trace-context.schema.json"
    assert "trace context is observability metadata and never grants identity" in " ".join(
        contract["invariants"]
    )


def test_trace_context_schema_accepts_safe_linked_context_and_rejects_secret_fields():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    payload = {
        "schema_version": "trace-context/v1",
        "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
        "span_id": "00f067aa0ba902b7",
        "correlation_id": "corr-1",
        "request_id": "req-1",
        "tenant_id": "tenant-a",
        "operation": "platform.execute",
        "started_at": "2026-10-18T05:00:00Z",
        "data_classification": "internal",
        "safe_attributes": {"service": "platform", "outcome": "succeeded", "attempt": 1},
        "evidence_refs": [
            {"evidence_id": "evidence:1", "kind": "policy-decision", "sha256": "a" * 64}
        ],
    }
    assert validator.is_valid(payload)
    zero_trace = dict(payload, trace_id="0" * 32)
    assert not validator.is_valid(zero_trace)
    zero_span = dict(payload, span_id="0" * 16)
    assert not validator.is_valid(zero_span)
    payload["authorization"] = "Bearer secret"
    assert not validator.is_valid(payload)
