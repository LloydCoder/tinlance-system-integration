#!/usr/bin/env python3
"""Post-phase audit for trace context, correlation, and telemetry safety."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "policies/observability-baseline.json",
        "contracts/telemetry/trace-context.json",
        "policies/economic-attribution-baseline.json",
        "scripts/certify_observability.py",
        ".github/workflows/observability-e2e.yml",
        ".github/workflows/observability-certification.yml",
        "docs/observability/trace-context-contract.md",
        "catalog/phases/registry.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-15 artifacts: " + ", ".join(missing))
    baseline = load("policies/observability-baseline.json")
    trace = load("contracts/telemetry/trace-context.json")
    economics = load("policies/economic-attribution-baseline.json")
    phases = load("catalog/phases/registry.json")
    if baseline["otel_semantic_conventions"] != trace["rules"]["semantic_convention_version"]:
        raise SystemExit("FAIL OpenTelemetry semantic convention version drift")
    fields = set(baseline["canonical_fields"])
    if not {"tenant_id", "execution_id", "trace_id", "span_id", "correlation_id", "event_id", "evidence_id"} <= fields:
        raise SystemExit("FAIL canonical observability correlation fields missing")
    if not {"trace_id", "evidence_id", "idempotency_key"} <= set(economics["canonical_fields"]):
        raise SystemExit("FAIL economics cannot correlate to execution evidence")
    rules = trace["rules"]
    if not (rules["never_log_secrets"] and rules["baggage_allowlist_only"] and rules["sampling_flags_never_grant_authorization"]):
        raise SystemExit("FAIL telemetry secret/authority boundary missing")
    workflow = (ROOT / ".github/workflows/observability-e2e.yml").read_text(encoding="utf-8")
    for marker in ("scripts/certify_observability.py", "scripts/forensic_audit_phase15.py", "persist-credentials: false"):
        if marker not in workflow:
            raise SystemExit(f"FAIL observability E2E workflow missing gate: {marker}")
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    if status["TSIC-14"] != "completed" or status["TSIC-15"] not in {"in_progress", "completed"}:
        raise SystemExit("FAIL serial phase dependency is not satisfied")
    print("PASS TSIC-15 forensic audit: telemetry version parity, trace/evidence/economics correlation, and secret/authority boundaries verified")


if __name__ == "__main__":
    main()
