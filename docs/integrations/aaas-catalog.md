# TSIC-18 — Tinlance.com Commercial and Agent-as-a-Service

## Purpose

Expose a public, assessment-led catalog of governed agent offers while keeping the commercial surface separate from domain authority, execution authority, entitlement, and evidence. The canonical registry is `catalog/capabilities/aaas-offers.json`; Tinlance.com consumes a generated snapshot that must be checked for exact semantic parity.

## Offer catalog

The catalog defines seven offer families:

- Governed Agent Infrastructure
- Signal-to-Outcome Acquisition Agent
- Content-to-Outreach Agent
- Security Detection and Assurance Agent
- Governed Healthcare Operations Workforce
- Engineering and Transformation Workforce
- Evidence-First Assurance Agent

Every offer is assessment-led and marked `assessment_required`. Public prices are intentionally omitted until an approved commercial pricing and entitlement model exists. Catalog inclusion does not imply that a customer environment has been provisioned or that customer outcomes have been achieved.

## Commercial safety invariants

- Agent Platform remains the sole generic consequential execution authority.
- All offers require tenant-scoped entitlements, approval, usage budgets, and region/jurisdiction policy.
- HezCast generates content; external publishing requires Agent Platform authorization, scoped credentials, policy checks, idempotency, and audit evidence.
- FAS-Bench remains independent evaluation authority and never a production runtime dependency.
- Hezqara remains outside diagnosis, triage, symptom-checker, treatment-decision and prescribing use cases; AI Scribe drafts require clinician review/edit/approval.
- Revenue, conversion, ROI, security outcomes, and delivery claims require source evidence. Successful execution or message delivery alone is not proof of business outcome.

## Website binding

- Canonical route: `/agent-as-a-service`
- Generated snapshot: `apps/web/lib/platform/aaas-offers.generated.json` in `LloydCoder/Tinlance`
- Primary CTA: technical assessment with the selected offer prefilled
- Machine-readable discovery: sitemap and `llms.txt`

The TSIC-18 cross-repository workflow checks the generated snapshot against the canonical catalog at Tinlance commit `0ef4e270a9b20325b7064413e66d895e78e67490`, and verifies that the route, desktop/mobile navigation, sitemap, `llms.txt`, and offer-prefilled assessment CTA are present before the phase can be certified.

## Certification

```bash
python3 scripts/certify_commercial_aaas.py
python3 scripts/forensic_audit_phase18.py
```

This is contract and catalog conformance, not a claim that every offer is already provisioned, commercially available in every jurisdiction, or approved for every customer environment.
