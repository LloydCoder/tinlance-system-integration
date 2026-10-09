#!/usr/bin/env python3
"""Certify the canonical signal-to-outcome feedback loop without authority escalation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    workflows = load("workflows/canonical.json")
    baseline = load("policies/closed-loop-baseline.json")
    economics = load("policies/economic-attribution-baseline.json")
    phases = load("catalog/phases/registry.json")
    workflow = next(item for item in workflows["workflows"] if item["id"] == baseline["workflow_id"])
    steps = workflow["steps"]
    expected = [
        "world-intelligence", "tads", "sdea", "reconos", "fadereach", "fdse",
        "outcome", "evidence", "economic-attribution", "evaluation", "tads", "sdea",
    ]
    assert steps == expected, "canonical acquisition-feedback order drifted"
    assert baseline["workflow_steps"] == steps, "baseline and canonical workflow disagree"
    assert baseline["authority"] == "tsic"
    assert steps.index("outcome") < steps.index("evidence") < steps.index("economic-attribution") < steps.index("evaluation")
    assert steps[-2:] == ["tads", "sdea"], "learning must feed decisioning, not execution authority"
    assert "agent-platform" not in steps[-2:], "feedback must not rewrite execution authority"
    assert "idempotency_key" in economics["canonical_fields"]
    assert "evidence_id" in economics["canonical_fields"]
    invariants = set(baseline["invariants"])
    assert {
        "outcome_is_traceable_to_signal",
        "evidence_and_economics_are_preserved",
        "learning_updates_decisioning_not_authority",
        "human_approval_boundaries_are_preserved",
        "feedback_requires_outcome_evidence",
        "replay_is_idempotent",
        "evaluation_is_separate_from_production_authority",
        "economic_attribution_is_not_inferred_from_delivery_success",
    } <= invariants
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    assert status["TSIC-13"] == "completed"
    assert status["TSIC-14"] in {"in_progress", "completed"}
    print("PASS TSIC-14 closed-loop certification: ordered feedback, evidence/economics lineage, replay idempotency and no authority escalation")


if __name__ == "__main__":
    main()
