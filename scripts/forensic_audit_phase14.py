#!/usr/bin/env python3
"""Post-phase audit for acquisition feedback and closed-loop intelligence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "workflows/canonical.json",
        "policies/closed-loop-baseline.json",
        "policies/economic-attribution-baseline.json",
        "scripts/certify_closed_loop.py",
        ".github/workflows/closed-loop-e2e.yml",
        ".github/workflows/closed-loop-certification.yml",
        "docs/economics/attribution-spine.md",
        "catalog/phases/registry.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-14 artifacts: " + ", ".join(missing))
    canonical = load("workflows/canonical.json")
    baseline = load("policies/closed-loop-baseline.json")
    phases = load("catalog/phases/registry.json")
    workflows = {item["id"]: item["steps"] for item in canonical["workflows"]}
    steps = workflows.get("acquisition-feedback", [])
    if steps != baseline.get("workflow_steps"):
        raise SystemExit("FAIL baseline and canonical closed-loop sequence diverge")
    if not (steps.index("outcome") < steps.index("evidence") < steps.index("economic-attribution") < steps.index("evaluation")):
        raise SystemExit("FAIL outcome/evidence/economics/evaluation order is invalid")
    if steps[-2:] != ["tads", "sdea"]:
        raise SystemExit("FAIL learning feedback target must remain acquisition decisioning")
    if "agent-platform" in steps[-2:]:
        raise SystemExit("FAIL closed-loop learning must not alter execution authority")
    invariants = set(baseline.get("invariants", []))
    required_invariants = {
        "outcome_is_traceable_to_signal",
        "evidence_and_economics_are_preserved",
        "learning_updates_decisioning_not_authority",
        "human_approval_boundaries_are_preserved",
        "feedback_requires_outcome_evidence",
        "replay_is_idempotent",
        "evaluation_is_separate_from_production_authority",
        "economic_attribution_is_not_inferred_from_delivery_success",
    }
    if not required_invariants <= invariants:
        raise SystemExit("FAIL closed-loop safety invariant missing")
    workflow = (ROOT / ".github/workflows/closed-loop-e2e.yml").read_text(encoding="utf-8")
    for marker in ("scripts/certify_closed_loop.py", "scripts/forensic_audit_phase14.py", "persist-credentials: false"):
        if marker not in workflow:
            raise SystemExit(f"FAIL closed-loop E2E workflow missing gate: {marker}")
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    if status["TSIC-13"] != "completed" or status["TSIC-14"] not in {"in_progress", "completed"}:
        raise SystemExit("FAIL serial phase dependency is not satisfied")
    print("PASS TSIC-14 forensic audit: canonical order, provenance, idempotency, human approval and authority boundaries verified")


if __name__ == "__main__":
    main()
