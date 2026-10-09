#!/usr/bin/env python3
"""Validate the canonical economic attribution contract and representative records."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validate_record(record: dict, schema: dict) -> bool:
    if not isinstance(record, dict) or schema.get("additionalProperties") is not False:
        return False
    props = schema["properties"]
    if set(record) - set(props) or set(schema["required"]) - set(record):
        return False
    for key, value in record.items():
        spec = props[key]
        kind = spec.get("type")
        if kind == "string":
            if not isinstance(value, str) or len(value) < spec.get("minLength", 0):
                return False
            if "enum" in spec and value not in spec["enum"]:
                return False
            if "pattern" in spec and not re.fullmatch(spec["pattern"], value):
                return False
        elif kind == "number":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False
            if value < spec.get("minimum", float("-inf")) or value > spec.get("maximum", float("inf")):
                return False
    if record.get("entry_type") == "cost" and "revenue_amount" in record:
        return False
    if record.get("entry_type") == "revenue" and "cost_amount" in record:
        return False
    return True


def main() -> None:
    baseline = load("policies/economic-attribution-baseline.json")
    schema = load("contracts/economics/attribution.json")
    phases = load("catalog/phases/registry.json")
    fields = baseline["canonical_fields"]
    required_fields = {
        "entry_id", "tenant_id", "organization_id", "workspace_id", "account_id",
        "signal_id", "opportunity_id", "agent_id", "service_id", "execution_id",
        "delivery_id", "trace_id", "evidence_id", "cost_center", "entry_type",
        "amount", "currency", "cost_amount", "cost_currency", "revenue_amount",
        "revenue_currency", "delivery_route", "idempotency_key", "occurred_at",
    }
    assert baseline["authority"] == "tsic"
    assert required_fields <= set(fields), f"missing canonical fields: {sorted(required_fields - set(fields))}"
    assert len(fields) == len(set(fields)), "duplicate canonical fields"
    assert schema["schema_version"] == "2.0.0"
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert set(schema["properties"]) <= set(fields), "schema fields missing from canonical registry"
    assert set(schema["required"]) <= set(schema["properties"])
    assert schema["properties"]["entry_type"]["enum"] == ["cost", "revenue"]
    assert schema["properties"]["amount"]["minimum"] == 0
    assert schema["properties"]["currency"]["pattern"] == "^[A-Z]{3}$"
    assert schema["properties"]["allocation_ratio"]["maximum"] == 1
    assert schema["properties"]["allocation_ratio"]["minimum"] == 0

    required_invariants = {
        "attribution_is_traceable", "cost_and_revenue_are_distinct",
        "delivery_route_is_explicit", "entry_type_disambiguates_cost_from_revenue",
        "currency_is_iso4217", "amount_nonnegative", "source_evidence_required",
        "idempotency_key_prevents_duplicate_attribution",
    }
    assert required_invariants <= set(baseline["invariants"])

    sample = {
        "entry_id": "entry-1", "entry_type": "cost", "tenant_id": "tenant-1",
        "organization_id": "org-1", "workspace_id": "workspace-1",
        "execution_id": "exec-1", "agent_id": "agent-1", "service_id": "svc-1",
        "cost_center": "engineering", "currency": "USD", "amount": 1.25,
        "meter_type": "model", "trace_id": "trace-1", "evidence_id": "evidence-1",
        "occurred_at": "2026-10-09T00:00:00Z", "idempotency_key": "cost:exec-1:1",
    }
    assert validate_record(sample, schema), "valid cost record rejected"
    revenue = {**sample, "entry_id": "entry-2", "entry_type": "revenue", "meter_type": "recurring"}
    assert validate_record(revenue, schema), "valid revenue record rejected"
    assert not validate_record({**sample, "amount": -0.01}, schema), "negative amount accepted"
    assert not validate_record({**sample, "currency": "usd"}, schema), "noncanonical currency accepted"
    assert not validate_record({**sample, "unexpected": "value"}, schema), "unknown property accepted"
    assert not validate_record({**sample, "revenue_amount": 2}, schema), "mixed cost/revenue record accepted"
    assert not validate_record({**revenue, "cost_amount": 1}, schema), "mixed revenue/cost record accepted"

    status = {item["id"]: item["status"] for item in phases["sequence"]}
    assert status["TSIC-12"] == "completed"
    assert status["TSIC-13"] in {"in_progress", "completed"}
    print("PASS TSIC-13 economic attribution: schema, valid/invalid records, cost/revenue separation, provenance, idempotency and serial gate")


if __name__ == "__main__":
    main()
