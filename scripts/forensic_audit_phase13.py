#!/usr/bin/env python3
"""Post-phase audit for the canonical economic attribution spine."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "policies/economic-attribution-baseline.json",
        "contracts/economics/attribution.json",
        "scripts/certify_economic_attribution.py",
        ".github/workflows/economic-attribution-certification.yml",
        "docs/economics/attribution-spine.md",
        "catalog/phases/registry.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-13 artifacts: " + ", ".join(missing))
    baseline = load("policies/economic-attribution-baseline.json")
    schema = load("contracts/economics/attribution.json")
    registry = load("catalog/phases/registry.json")
    fields = set(baseline["canonical_fields"])
    properties = set(schema["properties"])
    if schema["additionalProperties"] is not False or not set(schema["required"]) <= properties:
        raise SystemExit("FAIL economic attribution schema is not closed or required fields are invalid")
    if not properties <= fields:
        raise SystemExit("FAIL schema fields are not reconciled to canonical field registry")
    if not {"cost_amount", "revenue_amount", "cost_currency", "revenue_currency", "entry_type"} <= fields:
        raise SystemExit("FAIL cost/revenue separation fields missing")
    if not {"evidence_id", "trace_id", "idempotency_key", "tenant_id"} <= fields:
        raise SystemExit("FAIL evidence, trace, idempotency, or tenant fields missing")
    if "entry_type_disambiguates_cost_from_revenue" not in baseline["invariants"]:
        raise SystemExit("FAIL cost/revenue disambiguation invariant missing")
    workflow = (ROOT / ".github/workflows/economic-attribution-certification.yml").read_text(encoding="utf-8")
    for marker in ("scripts/certify_economic_attribution.py", "scripts/forensic_audit_phase13.py", "persist-credentials: false"):
        if marker not in workflow:
            raise SystemExit(f"FAIL economic attribution workflow missing gate: {marker}")
    status = {item["id"]: item["status"] for item in registry["sequence"]}
    if status["TSIC-12"] != "completed" or status["TSIC-13"] not in {"in_progress", "completed"}:
        raise SystemExit("FAIL serial phase dependency is not satisfied")
    print("PASS TSIC-13 forensic audit: closed schema, canonical field parity, cost/revenue separation, provenance, idempotency and CI evidence")
    

if __name__ == "__main__":
    main()
