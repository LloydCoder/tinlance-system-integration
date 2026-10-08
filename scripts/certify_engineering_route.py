#!/usr/bin/env python3
"""Certify the TSIC engineering delivery route."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load("policies/engineering-route-baseline.json")
    adapter = load("integrations/fdse/adapter.json")
    registry = load("catalog/contracts/registry.json")

    if baseline["authority"] != "tsic" or baseline["route"] != "engineering":
        raise AssertionError("engineering route baseline authority/route drift")
    if len(baseline["fdse"]["ref"]) != 40:
        raise AssertionError("invalid reviewed FDSE revision")

    required = {
        "identity-context",
        "event-envelope",
        "delivery-semantics",
        "trace-context",
        "economic-attribution",
    }
    if {item["id"] for item in registry["contracts"]} < required:
        raise AssertionError("delivery contract registry incomplete")
    if {item["tsic_contract"] for item in adapter["contract_bindings"]} != required:
        raise AssertionError("FDSE contract bindings drifted")

    required_invariants = {
        "delivery_route_is_explicit",
        "engineering_and_transformation_are_distinct_routes",
        "fdse_does_not_grant_platform_execution_authority",
        "evidence_and_outcomes_are_preserved",
        "tsic_remains_integration_authority",
        "agent-platform_remains-execution-authority",
    }
    if not required_invariants <= set(adapter["invariants"]):
        raise AssertionError("engineering route adapter authority invariants drifted")
    if "economic_attribution_carries_route" not in baseline["invariants"]:
        raise AssertionError("engineering route baseline lost economic attribution")

    print("PASS TSIC-27 Engineering route certification")


if __name__ == "__main__":
    main()
