# TSIC-19 — Autonomous Revenue Operating Loop

## Purpose

Close the acquisition-to-revenue feedback loop while keeping execution authority, consent, customer entitlements, economic attribution and revenue recognition explicit. "Autonomous" means a governed workflow can progress through approved steps; it does not mean the system may bypass policy, customer consent, human approval, or financial controls.

## Canonical sequence

`world-intelligence → tads → sdea → reconos → entitlement → consent-and-suppression → policy-approval → budget-check → agent-platform → fadereach → fdse → outcome → evidence → economic-attribution → revenue-recognition → evaluation → tads → sdea`

## Non-negotiable controls

- Tenant entitlement, jurisdiction/region policy, usage budget, consent and suppression checks happen before outreach or other consequential actions.
- Agent Platform remains the sole generic consequential execution authority and evaluates identity, policy, approval, scope and budget at execution time.
- FadeReach performs governed outreach; HezCast content generation never grants direct external publishing authority.
- Outcome, evidence, economic attribution and revenue recognition are separate stages. Delivery success is not proof of conversion, recognized revenue, ROI, or customer value.
- Cost and revenue are distinct typed ledger records, each with tenant, execution, trace, evidence, timestamp and idempotency keys. Duplicate/replayed events must not double count.
- Revenue recognition requires authoritative source evidence from the applicable billing/contracting system; it must not be inferred from MRR/ACV estimates or delivery events.
- Evaluation results can update targeting and decisioning in TADS/SDEA only. They cannot mutate Agent Platform authorization, approval, budget, sandbox, or execution authority.
- FAS-Bench remains independent evaluation authority, not a production runtime dependency.
- Healthcare offers remain non-diagnostic and AI Scribe outputs require clinician review, edit and approval.

## Certification

```bash
python3 scripts/certify_autonomous_revenue.py
python3 scripts/forensic_audit_phase19.py
python3 scripts/verify_aaas_site_sync.py --site-root tinlance-site
```

The dedicated workflow also checks the generated Tinlance.com AaaS catalog snapshot against the canonical TSIC offer registry. A green contract gate is not proof of actual revenue, customer conversion, or production readiness; those require source evidence.
