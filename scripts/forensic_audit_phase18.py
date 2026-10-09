#!/usr/bin/env python3
"""Post-phase audit for commercial AaaS catalog, entitlements, and authority boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "catalog/capabilities/aaas-offers.json",
        "catalog/capabilities/authority.json",
        "manifests/ecosystem.json",
        "policies/commercial-aaas-baseline.json",
        "scripts/certify_commercial_aaas.py",
        "scripts/verify_aaas_site_sync.py",
        ".github/workflows/commercial-aaas-certification.yml",
        "docs/integrations/aaas-catalog.md",
        "catalog/phases/registry.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-18 artifacts: " + ", ".join(missing))
    catalog = load("catalog/capabilities/aaas-offers.json")
    capabilities = load("catalog/capabilities/authority.json")
    manifest = load("manifests/ecosystem.json")
    phases = load("catalog/phases/registry.json")
    system_ids = {item["id"] for item in manifest["systems"]}
    capability_ids = {item["capability"] for item in capabilities["capabilities"]}
    offers = catalog["offers"]
    ids = [item["id"] for item in offers]
    if len(ids) != len(set(ids)) or not offers:
        raise SystemExit("FAIL AaaS offer IDs are empty or duplicated")
    for offer in offers:
        if not set(offer["runtime_systems"]) <= system_ids or not set(offer.get("evaluation_systems", [])) <= system_ids:
            raise SystemExit(f"FAIL unregistered system in offer {offer['id']}")
        if not set(offer["required_capabilities"]) <= capability_ids:
            raise SystemExit(f"FAIL unregistered capability in offer {offer['id']}")
        if "agent-platform" not in offer["runtime_systems"]:
            raise SystemExit(f"FAIL Agent Platform missing from offer {offer['id']}")
        if "fas-bench" in offer["runtime_systems"]:
            raise SystemExit(f"FAIL FAS-Bench runtime dependency in offer {offer['id']}")
        if offer["pricing"]["public_price"] is not None:
            raise SystemExit(f"FAIL unapproved public price in offer {offer['id']}")
    content = next(item for item in offers if item["id"] == "content-to-outreach-agent")
    if content["authority"]["external_publishing"] != "agent-platform" or content["safety_boundaries"]["direct_external_publishing_allowed"]:
        raise SystemExit("FAIL HezCast external publishing boundary drift")
    healthcare = next(item for item in offers if item["id"] == "governed-healthcare-workforce")
    if healthcare["safety_boundaries"]["diagnosis_or_triage"] or healthcare["safety_boundaries"]["clinical_treatment_decisions"] or not healthcare["safety_boundaries"]["ai_scribe_requires_clinician_review"]:
        raise SystemExit("FAIL healthcare scope/clinician review boundary drift")
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    if status["TSIC-17"] != "completed" or status["TSIC-18"] not in {"in_progress", "completed"}:
        raise SystemExit("FAIL serial phase dependency is not satisfied")
    workflow = (ROOT / ".github/workflows/commercial-aaas-certification.yml").read_text(encoding="utf-8")
    for marker in ("scripts/certify_commercial_aaas.py", "scripts/verify_aaas_site_sync.py", "scripts/forensic_audit_phase18.py", "LloydCoder/Tinlance", "0ef4e270a9b20325b7064413e66d895e78e67490", "persist-credentials: false"):
        if marker not in workflow:
            raise SystemExit(f"FAIL commercial AaaS workflow missing gate: {marker}")
    print("PASS TSIC-18 forensic audit: offer registry, registered systems/capabilities, quote-only pricing, entitlement, publishing and healthcare boundaries")


if __name__ == "__main__":
    main()
