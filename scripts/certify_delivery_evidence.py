#!/usr/bin/env python3
"""Certify the TSIC delivery-evidence/reporting boundary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load("policies/delivery-evidence-baseline.json")
    adapter = load("integrations/fdse-toolkit/adapter.json")
    registry = load("catalog/contracts/registry.json")

    if baseline["authority"] != "tsic":
        raise AssertionError("TSIC is not delivery-evidence certification authority")
    if len(baseline["fdse_toolkit"]["ref"]) != 40:
        raise AssertionError("invalid reviewed FDSE Toolkit revision")

    required = {"identity-context","event-envelope","delivery-semantics","trace-context","economic-attribution"}
    if {item["id"] for item in registry["contracts"]} < required:
        raise AssertionError("delivery contract registry incomplete")
    if {item["tsic_contract"] for item in adapter["contract_bindings"]} != required:
        raise AssertionError("FDSE Toolkit contract bindings drifted")

    if set(baseline["invariants"]) != set(adapter["invariants"]):
        raise AssertionError("FDSE Toolkit authority invariants drifted")
    if adapter["authority"]["integration_contracts"] != "tsic":
        raise AssertionError("TSIC integration authority drifted")
    if adapter["authority"]["delivery_reporting"] != "fdse-toolkit":
        raise AssertionError("FDSE Toolkit reporting authority drifted")
    if adapter["authority"]["execution_authority"] != "agent-platform":
        raise AssertionError("execution authority drifted")

    print("PASS TSIC-29 delivery evidence certification")


if __name__ == "__main__":
    main()
