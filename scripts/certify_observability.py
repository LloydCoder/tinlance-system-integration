#!/usr/bin/env python3
"""Certify W3C trace context integrity and ecosystem observability semantics."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACE_ID = re.compile(r"^[0-9a-f]{32}$")
SPAN_ID = re.compile(r"^[0-9a-f]{16}$")
TRACEPARENT = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")
SENSITIVE_BAGGAGE_KEYS = {"authorization", "token", "password", "secret", "api_key", "access_token"}


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def valid_context(context: dict) -> bool:
    trace_id = context.get("trace_id", "")
    span_id = context.get("span_id", "")
    parent = context.get("traceparent", "")
    match = TRACEPARENT.fullmatch(parent) if isinstance(parent, str) else None
    if not isinstance(trace_id, str) or not TRACE_ID.fullmatch(trace_id) or trace_id == "0" * 32:
        return False
    if not isinstance(span_id, str) or not SPAN_ID.fullmatch(span_id) or span_id == "0" * 16:
        return False
    if not match or match.group(1) != trace_id or match.group(2) != span_id:
        return False
    baggage = context.get("baggage", "")
    if not isinstance(baggage, str) or len(baggage.encode("utf-8")) > 8192:
        return False
    for item in baggage.split(","):
        if not item.strip():
            continue
        key = item.split("=", 1)[0].strip().lower()
        if key in SENSITIVE_BAGGAGE_KEYS or any(word in key for word in ("password", "secret", "token", "credential")):
            return False
    return True


def main() -> None:
    baseline = load("policies/observability-baseline.json")
    contract = load("contracts/telemetry/trace-context.json")
    economics = load("policies/economic-attribution-baseline.json")
    phases = load("catalog/phases/registry.json")
    assert baseline["authority"] == "tsic"
    assert baseline["otel_semantic_conventions"] == "1.37.0"
    fields = set(baseline["canonical_fields"])
    assert len(fields) >= 14
    assert {"trace_id", "span_id", "correlation_id", "event_id", "evidence_id", "tenant_id", "execution_id"} <= fields
    assert set(contract["required"]) == {"trace_id", "span_id", "traceparent"}
    assert contract["rules"]["semantic_convention_version"] == baseline["otel_semantic_conventions"]
    assert contract["rules"]["preserve_trace_across_system_boundaries"] is True
    assert contract["rules"]["never_log_secrets"] is True
    assert contract["rules"]["baggage_allowlist_only"] is True
    assert contract["rules"]["sampling_flags_never_grant_authorization"] is True
    assert {"trace_context_is_propagated", "correlation_is_stable", "semantic_convention_version_is_pinned",
            "trace_and_span_ids_are_nonzero_lowercase_hex", "traceparent_ids_match_context_fields",
            "baggage_is_allowlisted_and_secret_free", "sampling_flags_are_not_authorization"} <= set(baseline["invariants"])
    assert {"trace_id", "evidence_id", "idempotency_key"} <= set(economics["canonical_fields"])

    trace_id = "0123456789abcdef0123456789abcdef"
    span_id = "0123456789abcdef"
    valid = {"trace_id": trace_id, "span_id": span_id, "traceparent": f"00-{trace_id}-{span_id}-01",
             "tenant_id": "tenant-1", "execution_id": "exec-1", "evidence_id": "evidence-1",
             "baggage": "region=eu,service=fdse"}
    assert valid_context(valid), "valid trace context rejected"
    assert not valid_context({**valid, "trace_id": "0" * 32}), "all-zero trace ID accepted"
    assert not valid_context({**valid, "span_id": "0" * 16}), "all-zero span ID accepted"
    assert not valid_context({**valid, "traceparent": f"00-{'f' * 32}-{span_id}-01"}), "traceparent mismatch accepted"
    assert not valid_context({**valid, "trace_id": trace_id.upper()}), "uppercase trace ID accepted"
    assert not valid_context({**valid, "baggage": "access_token=do-not-log"}), "sensitive baggage accepted"
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    assert status["TSIC-14"] == "completed"
    assert status["TSIC-15"] in {"in_progress", "completed"}
    print("PASS TSIC-15 observability: W3C trace integrity, semantic-version pin, tenant/evidence correlation, and secret-safe baggage")


if __name__ == "__main__":
    main()
