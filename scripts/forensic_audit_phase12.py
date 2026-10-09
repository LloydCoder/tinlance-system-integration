#!/usr/bin/env python3
"""Deterministic post-phase audit for TSIC-12 governed healthcare integration."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "policies/hezqara-baseline.json",
        "integrations/hezqara/adapter.json",
        "scripts/certify_hezqara.py",
        ".github/workflows/hezqara-certification.yml",
        ".github/workflows/hezqara-integration-e2e.yml",
        "catalog/phases/registry.json",
        "catalog/contracts/registry.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-12 artifacts: " + ", ".join(missing))

    baseline = load("policies/hezqara-baseline.json")
    adapter = load("integrations/hezqara/adapter.json")
    contracts = load("catalog/contracts/registry.json")
    phases = load("catalog/phases/registry.json")
    target = baseline.get("hezqara", {})

    if target.get("repository") != "LloydCoder/hezqara":
        raise SystemExit("FAIL unexpected Hezqara repository authority")
    ref = target.get("ref", "")
    if len(ref) != 40 or any(c not in "0123456789abcdef" for c in ref):
        raise SystemExit("FAIL Hezqara baseline must pin a full immutable commit SHA")
    if adapter.get("source_system") != "tsic" or adapter.get("target_system") != "hezqara":
        raise SystemExit("FAIL Hezqara adapter direction is invalid")
    expected_authority = {
        "integration_contracts": "tsic",
        "healthcare_workforce": "hezqara",
        "execution_authority": "agent-platform",
    }
    if adapter.get("authority") != expected_authority:
        raise SystemExit("FAIL healthcare authority boundary drift")

    required_contracts = {
        "identity-context",
        "event-envelope",
        "delivery-semantics",
        "trace-context",
        "economic-attribution",
    }
    registered = {item["id"] for item in contracts.get("contracts", [])}
    bound = {item["tsic_contract"] for item in adapter.get("contract_bindings", [])}
    if not required_contracts <= registered or bound != required_contracts:
        raise SystemExit("FAIL canonical healthcare contract bindings are incomplete or divergent")

    invariants = set(baseline.get("invariants", []))
    if invariants != set(adapter.get("invariants", [])):
        raise SystemExit("FAIL Hezqara baseline and adapter invariants diverge")
    required_invariants = {
        "clinician_review_remains_required_for_ai_scribe_drafts",
        "healthcare_workforce_does_not_grant_generic_execution_authority",
        "provenance_is_preserved",
        "tenant_context_is_immutable",
        "tsic_remains_integration_authority",
        "agent-platform-remains-execution-authority",
    }
    if not required_invariants <= invariants:
        raise SystemExit("FAIL healthcare safety/authority invariant missing")

    workflow = (ROOT / ".github/workflows/hezqara-integration-e2e.yml").read_text(encoding="utf-8")
    for marker in (
        ref,
        "persist-credentials: false",
        "pytest -q tests ../tests/security",
        "npm run lint",
        "npm run type-check",
        "npm run build",
        "scripts/certify_hezqara.py",
        "scripts/forensic_audit_phase12.py",
    ):
        if marker not in workflow:
            raise SystemExit(f"FAIL TSIC-12 workflow missing required gate: {marker}")

    sequence = {item.get("id"): item.get("status") for item in phases.get("sequence", [])}
    if sequence.get("TSIC-11") != "completed":
        raise SystemExit("FAIL TSIC-11 must be completed before TSIC-12")
    if sequence.get("TSIC-12") not in {"in_progress", "completed"}:
        raise SystemExit("FAIL TSIC-12 phase registry state is inconsistent")

    print(
        "PASS TSIC-12 forensic audit: immutable Hezqara pin, canonical contracts, "
        "tenant/provenance/clinician-review invariants, frontend/backend gates, and serial dependency verified"
    )


if __name__ == "__main__":
    main()
