#!/usr/bin/env python3
"""Validate the canonical P3 CloudEvents envelope and delivery semantics."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/event-envelope.schema.json"
FIXTURE = ROOT / "contracts/events/examples/execution-completed.json"
DELIVERY = ROOT / "contracts/events/delivery-semantics.json"


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    event = json.loads(FIXTURE.read_text(encoding="utf-8"))
    semantics = json.loads(DELIVERY.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(event), key=lambda err: list(err.path))
    if errors:
        raise SystemExit("FAIL canonical event fixture: " + "; ".join(e.message for e in errors))

    invalid = []
    bad = copy.deepcopy(event)
    bad.pop("tenantid")
    invalid.append(("missing tenant scope", bad))
    bad = copy.deepcopy(event)
    bad["datacontenttype"] = "text/plain"
    invalid.append(("wrong content type", bad))
    bad = copy.deepcopy(event)
    bad["traceid"] = "0" * 32
    invalid.append(("invalid all-zero trace id", bad))
    bad = copy.deepcopy(event)
    bad["tenant_id"] = "spoofed-extension"
    invalid.append(("non-CloudEvents extension spelling", bad))
    bad = copy.deepcopy(event)
    bad["authorization"] = "allow"
    invalid.append(("unknown authority-shaped property", bad))
    for label, candidate in invalid:
        if not list(validator.iter_errors(candidate)):
            raise SystemExit(f"FAIL invalid event unexpectedly accepted: {label}")

    if semantics.get("delivery", {}).get("delivery_guarantee") != "at-least-once":
        raise SystemExit("FAIL delivery guarantee must explicitly be at-least-once")
    if semantics.get("delivery", {}).get("deduplication_key") != ["source", "id"]:
        raise SystemExit("FAIL consumer deduplication must use CloudEvents source + id")
    if semantics.get("delivery", {}).get("outbox_required_for_durable_publish") is not True:
        raise SystemExit("FAIL durable publication requires outbox")
    if semantics.get("delivery", {}).get("inbox_required_for_idempotent_consume") is not True:
        raise SystemExit("FAIL idempotent consumers require inbox")
    delivery = semantics.get("delivery", {})
    retry = delivery.get("retry", {})
    if not all(retry.get(key) is True for key in ("exponential_backoff", "bounded", "jitter")):
        raise SystemExit("FAIL retry policy must be bounded exponential backoff with jitter")
    if delivery.get("dead_letter") is not True or delivery.get("replay") is not True:
        raise SystemExit("FAIL poison events require dead-letter and explicit replay semantics")
    lease = delivery.get("lease", {})
    if lease.get("owner_bound") is not True or lease.get("expires") is not True:
        raise SystemExit("FAIL outbox leases must be owner-bound and expiring")
    if lease.get("stale_ack_rejected") is not True:
        raise SystemExit("FAIL stale lease acknowledgements must be rejected")
    ordering = semantics.get("ordering", {})
    if ordering.get("default") != "not_guaranteed":
        raise SystemExit("FAIL base outbox ordering must be documented as not guaranteed")
    if ordering.get("explicit_ordering_key_required") is not True:
        raise SystemExit("FAIL ordered delivery requires explicit ordering metadata")
    print("PASS P3 event contract: schema, tenant scope, trace identity, unknown-field rejection, retries, leases, and ordering semantics")


if __name__ == "__main__":
    main()
