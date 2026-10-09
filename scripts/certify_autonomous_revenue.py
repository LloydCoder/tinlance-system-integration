#!/usr/bin/env python3
"""Certify the governed TSIC-19 autonomous revenue operating loop."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))
def fail(message: str) -> None:
    raise SystemExit("FAIL TSIC-19: " + message)
def main() -> None:
    baseline = load("policies/autonomous-revenue-baseline.json")
    canonical = load("workflows/canonical.json")
    economics = load("contracts/economics/attribution.json")
    offers = load("catalog/capabilities/aaas-offers.json")
    phases = load("catalog/phases/registry.json")
    required_invariants = {
        "revenue_actions_are_policy_governed", "outreach_is_consent_and_compliance_bounded",
        "economic_attribution_is_end_to_end", "human_approval_is_required_for_high_impact_actions",
        "closed_loop_feedback_cannot_mutate_authority_boundaries", "consent_and_suppression_checked_before_outreach",
        "tenant_entitlement_and_usage_budget_checked_before_execution", "agent_platform_authorizes_all_consequential_actions",
        "outcomes_are_not_inferred_from_delivery", "cost_and_revenue_records_are_separate_and_idempotent",
        "revenue_recognition_requires_source_evidence", "feedback_updates_tads_and_sdea_only",
        "learning_cannot_change_execution_authority", "fas_bench_is_evaluation_only",
        "healthcare_non_diagnostic_boundaries_are_preserved", "external_publishing_requires_agent_platform_authorization",
    }
    if baseline.get("authority") != "tsic" or not required_invariants <= set(baseline.get("invariants", [])):
        fail("baseline authority or required invariant missing")
    workflows = {item["id"]: item["steps"] for item in canonical["workflows"]}
    steps = workflows.get("autonomous-revenue", [])
    if steps != baseline.get("required_workflow_steps"):
        fail("canonical autonomous-revenue sequence diverges from baseline")
    positions = {step: index for index, step in enumerate(steps)}
    for step in ("entitlement", "consent-and-suppression", "policy-approval", "budget-check"):
        if positions[step] >= positions["fadereach"]:
            fail(f"{step} must be checked before outreach")
    if positions["agent-platform"] > positions["fadereach"] or positions["agent-platform"] > positions["fdse"]:
        fail("Agent Platform authorization must precede consequential execution")
    if not (positions["outcome"] < positions["evidence"] < positions["economic-attribution"] < positions["revenue-recognition"] < positions["evaluation"]):
        fail("outcome/evidence/attribution/revenue/evaluation order is invalid")
    if steps[-2:] != ["tads", "sdea"]:
        fail("feedback must return to TADS and SDEA only")
    if "agent-platform" in steps[-2:] or "fas-bench" in steps:
        fail("feedback must not mutate execution authority and FAS-Bench must remain evaluation-only")
    required_economic_fields = {"entry_id", "entry_type", "tenant_id", "execution_id", "currency", "amount", "trace_id", "evidence_id", "occurred_at", "idempotency_key"}
    if not required_economic_fields <= set(economics["required"]):
        fail("economic ledger is missing attribution, provenance, or idempotency fields")
    if len(economics.get("allOf", [])) < 2:
        fail("cost/revenue separation rules are missing")
    if any("fas-bench" in item.get("runtime_systems", []) for item in offers["offers"]):
        fail("FAS-Bench may not be a production runtime dependency")
    content_offer = next(item for item in offers["offers"] if item["id"] == "content-to-outreach-agent")
    if content_offer["authority"]["external_publishing"] != "agent-platform":
        fail("external publishing authority boundary drifted")
    healthcare = next(item for item in offers["offers"] if item["id"] == "governed-healthcare-workforce")
    if healthcare["safety_boundaries"]["diagnosis_or_triage"] or healthcare["safety_boundaries"]["clinical_treatment_decisions"]:
        fail("healthcare offer exceeds approved scope")
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    if status["TSIC-18"] != "completed" or status["TSIC-19"] not in {"in_progress", "completed"}:
        fail("serial phase dependency is not satisfied")
    print("PASS TSIC-19 autonomous revenue: consent, entitlement, authorization, evidence, economic attribution, revenue recognition and bounded feedback")
if __name__ == "__main__":
    main()
