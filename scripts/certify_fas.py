#!/usr/bin/env python3
"""Certify the TSIC evidence-analysis boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load("policies/fas-baseline.json")
    adapter = load("integrations/fas/adapter.json")
    registry = load("catalog/contracts/registry.json")
    required = {"identity-context","event-envelope","delivery-semantics","trace-context","economic-attribution"}

    if len(baseline["fas"]["ref"]) != 40:
        raise AssertionError("invalid reviewed FAS revision")
    if {item["id"] for item in registry["contracts"]} < required:
        raise AssertionError("evidence contract registry incomplete")
    if {item["tsic_contract"] for item in adapter["contract_bindings"]} != required:
        raise AssertionError("FAS contract bindings drifted")
    if set(baseline["invariants"]) != set(adapter["invariants"]):
        raise AssertionError("FAS evidence authority invariants drifted")
    if adapter["authority"] != {
        "integration_contracts":"tsic",
        "evidence_analysis":"fas",
        "execution_authority":"agent-platform",
    }:
        raise AssertionError("FAS authority boundary drifted")
    print("PASS TSIC-30 FAS certification")


if __name__ == "__main__":
    main()
