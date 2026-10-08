#!/usr/bin/env python3
"""Certify the TSIC transformation delivery route."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load("policies/transformation-route-baseline.json")
    adapter = load("integrations/fdse/adapter.json")
    registry = load("catalog/contracts/registry.json")

    if baseline["authority"] != "tsic" or baseline["route"] != "transformation":
        raise AssertionError("transformation route baseline authority/route drift")
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

    invariants = set(adapter["invariants"])
    if "delivery_route_is_explicit" not in invariants:
        raise AssertionError("delivery route is not explicit")
    if "engineering_and_transformation_are_distinct_routes" not in invariants:
        raise AssertionError("engineering/transformation distinction missing")
    if "fdse_does_not_grant_platform_execution_authority" not in invariants:
        raise AssertionError("FDSE execution boundary drifted")
    if "evidence_and_outcomes_are_preserved" not in invariants:
        raise AssertionError("delivery evidence/outcome boundary drifted")
    required_baseline_invariants = {
        "delivery_route_is_explicit",
        "transformation_route_is_distinct_from_engineering",
        "portfolio_transformation_semantics_are_preserved",
        "economic_attribution_carries_route",
    }
    if not required_baseline_invariants <= set(baseline["invariants"]):
        raise AssertionError("transformation baseline invariants drifted")

    print("PASS TSIC-28 Transformation route certification")


if __name__ == "__main__":
    main()
