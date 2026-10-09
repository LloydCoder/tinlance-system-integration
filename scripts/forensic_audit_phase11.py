#!/usr/bin/env python3
"""Deterministic post-phase audit for TSIC-11 BugFlow integration."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "policies/bugflow-baseline.json",
        "integrations/bugflow/adapter.json",
        "scripts/certify_bugflow.py",
        ".github/workflows/bugflow-certification.yml",
        ".github/workflows/bugflow-integration-e2e.yml",
        "catalog/phases/registry.json",
        "catalog/contracts/registry.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-11 artifacts: " + ", ".join(missing))

    baseline = load("policies/bugflow-baseline.json")
    adapter = load("integrations/bugflow/adapter.json")
    contracts = load("catalog/contracts/registry.json")
    phases = load("catalog/phases/registry.json")
    bugflow = baseline["bugflow"]

    if bugflow["repository"] != "LloydCoder/bugflow-elite":
        raise SystemExit("FAIL unexpected BugFlow repository authority")
    ref = bugflow.get("ref", "")
    if len(ref) != 40 or any(c not in "0123456789abcdef" for c in ref):
        raise SystemExit("FAIL BugFlow baseline must pin a full immutable commit SHA")
    if adapter.get("target_system") != "bugflow":
        raise SystemExit("FAIL adapter target must be BugFlow")
    authority = adapter.get("authority", {})
    expected_authority = {
        "integration_contracts": "tsic",
        "application_security_testing": "bugflow",
        "execution_authority": "agent-platform",
    }
    if authority != expected_authority:
        raise SystemExit("FAIL BugFlow authority boundary drift")
    if adapter.get("source_system") != "tsic":
        raise SystemExit("FAIL TSIC must remain the adapter source authority")

    required_contracts = {
        "identity-context",
        "event-envelope",
        "delivery-semantics",
        "trace-context",
        "economic-attribution",
    }
    registered = {item["id"] for item in contracts.get("contracts", [])}
    bound = {item["tsic_contract"] for item in adapter.get("contract_bindings", [])}
    if not required_contracts <= registered:
        raise SystemExit("FAIL required contracts missing from canonical registry")
    if bound != required_contracts:
        raise SystemExit("FAIL BugFlow adapter bindings differ from required contract set")

    invariants = set(baseline.get("invariants", []))
    if invariants != set(adapter.get("invariants", [])):
        raise SystemExit("FAIL baseline and adapter invariants diverge")
    if not {
        "testing_is_not_execution_authority",
        "findings_retain_provenance",
        "tenant_context_is_immutable",
        "tsic_remains_integration_authority",
        "agent-platform-remains-execution-authority",
    } <= invariants:
        raise SystemExit("FAIL critical BugFlow safety invariants missing")

    workflow = (ROOT / ".github/workflows/bugflow-integration-e2e.yml").read_text(encoding="utf-8")
    for marker in (
        ref,
        "python -m compileall -q .",
        "python -m pytest tests/",
        "scripts/certify_bugflow.py",
        "scripts/forensic_audit_phase11.py",
        "persist-credentials: false",
    ):
        if marker not in workflow:
            raise SystemExit(f"FAIL TSIC-11 workflow missing required gate: {marker}")

    sequence = phases.get("sequence", [])
    current = {item.get("id"): item.get("status") for item in sequence}
    if current.get("TSIC-10") != "completed":
        raise SystemExit("FAIL TSIC-10 must be completed before TSIC-11")
    if current.get("TSIC-11") not in {"in_progress", "completed"}:
        raise SystemExit("FAIL TSIC-11 phase registry state is inconsistent")

    print(
        "PASS TSIC-11 forensic audit: immutable BugFlow pin, canonical contracts, "
        "authority boundaries, provenance/tenant invariants, CI gates, and serial phase dependency verified"
    )


if __name__ == "__main__":
    main()
