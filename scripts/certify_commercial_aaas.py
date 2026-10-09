#!/usr/bin/env python3
"""Certify the canonical Tinlance.com Agent-as-a-Service catalog and safety gates."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit("FAIL TSIC-18: " + message)


def main() -> None:
    baseline = load("policies/commercial-aaas-baseline.json")
    catalog = load("catalog/capabilities/aaas-offers.json")
    capabilities = load("catalog/capabilities/authority.json")
    manifest = load("manifests/ecosystem.json")
    workflows = load("workflows/canonical.json")
    phases = load("catalog/phases/registry.json")
    if baseline.get("authority") != "tsic" or catalog.get("authority") != "tsic":
        fail("TSIC must remain canonical AaaS contract and certification authority")
    required_invariants = {
        "commercial_surface_does_not_replace_domain_authority",
        "aaas_offers_bind_to_certified_agent_execution",
        "pricing_and_entitlement_are_traceable",
        "customer_tenant_context_is_preserved",
        "delivery_evidence_is_attributable_to_workflow_and_customer",
        "aaas_offers_are_machine_readable_and_unique",
        "all_offer_systems_and_capabilities_are_registered",
        "public_prices_are_not_invented",
        "entitlements_are_tenant_scoped_and_policy_gated",
        "external_publishing_is_agent_platform_authorized",
        "fas_bench_is_evaluation_only",
        "healthcare_scope_and_clinician_review_boundaries_are_preserved",
    }
    if not required_invariants <= set(baseline.get("invariants", [])):
        fail("commercial baseline invariant missing")

    offers = catalog.get("offers", [])
    offer_ids = [offer.get("id") for offer in offers]
    if len(offers) < 5 or len(offer_ids) != len(set(offer_ids)):
        fail("offer catalog is empty, too small, or contains duplicate IDs")
    systems = {item["id"] for item in manifest["systems"]}
    capability_owners = {item["capability"]: item["owner"] for item in capabilities["capabilities"]}
    if catalog["default_pricing"] != {"model": "quote_required", "public_price": None, "currency": None}:
        fail("default public pricing must remain quote-required until approved")
    if catalog["commercial_surface"]["public_route"] != "/agent-as-a-service":
        fail("canonical public AaaS route drifted")
    if catalog["commercial_surface"]["generated_catalog_path"] != "apps/web/lib/platform/aaas-offers.generated.json":
        fail("website generated catalog path drifted")

    for offer in offers:
        if not all(offer.get(key) for key in ("name", "buyer_problem", "summary", "runtime_systems", "required_capabilities", "evidence_required", "limitations")):
            fail(f"offer {offer.get('id')} lacks required product and evidence metadata")
        runtime = set(offer["runtime_systems"])
        evaluation = set(offer.get("evaluation_systems", []))
        if not runtime <= systems or not evaluation <= systems:
            fail(f"offer {offer['id']} references unregistered systems")
        if "agent-platform" not in runtime:
            fail(f"offer {offer['id']} lacks generic execution authority")
        if "fas-bench" in runtime or ("fas-bench" in evaluation and "fas-bench" in runtime):
            fail(f"offer {offer['id']} incorrectly uses FAS-Bench as runtime")
        if not set(offer["required_capabilities"]) <= set(capability_owners):
            fail(f"offer {offer['id']} references unregistered capabilities")
        for capability in offer["required_capabilities"]:
            if capability_owners[capability] not in runtime | evaluation:
                fail(f"offer {offer['id']} omits owning system for capability {capability}")
        if offer.get("commercial_posture") != "assessment_led" or offer.get("availability") != "assessment_required":
            fail(f"offer {offer['id']} overstates availability")
        if offer.get("pricing") != {"model": "quote_required", "public_price": None, "currency": None}:
            fail(f"offer {offer['id']} contains unapproved public pricing")
        entitlement = offer.get("entitlements", {})
        if not all(entitlement.get(key) is True for key in ("tenant_scoped", "approval_required", "usage_budget_required", "region_policy_required")):
            fail(f"offer {offer['id']} lacks mandatory entitlement controls")
        if offer.get("authority", {}).get("generic_execution") != "agent-platform":
            fail(f"offer {offer['id']} creates or omits generic execution authority")

    by_id = {offer["id"]: offer for offer in offers}
    content = by_id["content-to-outreach-agent"]
    if content["safety_boundaries"].get("direct_external_publishing_allowed") is not False:
        fail("HezCast must not directly own external publishing authority")
    if content["authority"].get("external_publishing") != "agent-platform":
        fail("external publishing must be Agent Platform authorized")
    healthcare = by_id["governed-healthcare-workforce"]["safety_boundaries"]
    if healthcare.get("diagnosis_or_triage") is not False or healthcare.get("clinical_treatment_decisions") is not False or healthcare.get("ai_scribe_requires_clinician_review") is not True:
        fail("healthcare scope or clinician review boundary drifted")
    security = by_id["security-detection-and-assurance-agent"]
    if "fas-bench" not in security["evaluation_systems"] or "fas-bench" in security["runtime_systems"]:
        fail("FAS-Bench must remain evaluation-only")
    if "acquisition-engineering" not in {item["id"] for item in workflows["workflows"]}:
        fail("canonical acquisition workflow missing")
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    if status["TSIC-17"] != "completed" or status["TSIC-18"] not in {"in_progress", "completed"}:
        fail("serial phase dependency is not satisfied")
    print(f"PASS TSIC-18 commercial/AaaS: {len(offers)} offers, registered capabilities, quote-only pricing, tenant entitlements, and safety boundaries")


if __name__ == "__main__":
    main()
