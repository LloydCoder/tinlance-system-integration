#!/usr/bin/env python3
"""Certify the reviewed Tinlance Acquisition System baseline."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "identity-context",
    "event-envelope",
    "delivery-semantics",
    "trace-context",
    "economic-attribution",
}


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    baseline = load_json("policies/acquisition-system-baseline.json")
    manifest = load_json("manifests/ecosystem.json")
    registry = load_json("catalog/contracts/registry.json")

    if baseline["authority"] != "tsic":
        raise AssertionError("TSIC is not the acquisition baseline authority")
    if baseline["sequence"] != ["world-intelligence", "tads", "sdea", "reconos", "fadereach"]:
        raise AssertionError("canonical acquisition sequence drifted")
    if len(baseline["tsic"]["ref"]) != 40:
        raise AssertionError("invalid reviewed TSIC revision")

    systems = {item["id"]: item for item in manifest["systems"]}
    registered_contracts = {item["id"] for item in registry["contracts"]}
    if not registered_contracts >= REQUIRED:
        raise AssertionError("TSIC registry is missing a required acquisition contract")

    for system_id in baseline["sequence"]:
        reviewed = baseline["systems"][system_id]
        system = systems.get(system_id)
        if system is None:
            raise AssertionError(f"missing manifest system: {system_id}")
        if system["repository"] != reviewed["repository"]:
            raise AssertionError(f"repository mapping drift: {system_id}")
        if len(reviewed["ref"]) != 40:
            raise AssertionError(f"invalid reviewed SHA: {system_id}")

        adapter = load_json(f"integrations/{system_id}/adapter.json")
        if adapter["source_system"] != "tsic" or adapter["target_system"] != system_id:
            raise AssertionError(f"adapter endpoint drift: {system_id}")
        bindings = {item["tsic_contract"] for item in adapter["contract_bindings"]}
        if bindings != REQUIRED:
            raise AssertionError(f"contract binding drift: {system_id}")
        if "tsic_remains_integration_authority" not in adapter["invariants"]:
            raise AssertionError(f"TSIC authority invariant missing: {system_id}")
        execution_invariants = {
            "agent-platform-remains-execution-authority",
            "agent-platform_remains_execution_authority",
        }
        if not execution_invariants.intersection(adapter["invariants"]):
            raise AssertionError(f"execution authority invariant missing: {system_id}")

    print("PASS TSIC-25 Acquisition System certification")


if __name__ == "__main__":
    main()
