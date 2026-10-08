#!/usr/bin/env python3
"""TSIC-41 autonomous revenue operating loop certification."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=json.loads((ROOT/"policies/autonomous-revenue-baseline.json").read_text())
    w=json.loads((ROOT/"workflows/canonical.json").read_text())
    required=set(p["invariants"])
    assert required >= {
        "revenue_actions_are_policy_governed",
        "outreach_is_consent_and_compliance_bounded",
        "economic_attribution_is_end_to_end",
        "human_approval_is_required_for_high_impact_actions",
        "closed_loop_feedback_cannot_mutate_authority_boundaries",
    }
    wf={x["id"]:x["steps"] for x in w["workflows"]}
    assert "acquisition-feedback" in wf
    assert "economic-attribution" in wf["acquisition-feedback"]
    print("PASS TSIC-41 autonomous revenue operating loop certification")
if __name__=="__main__": main()
