# TSIC-14 — Closed-Loop Intelligence

## Purpose

Certify the governed feedback loop from world intelligence and acquisition decisioning through enrichment, outreach, delivery, outcome capture, evidence, economic attribution, evaluation, and bounded learning.

## Canonical sequence

`world-intelligence → tads → sdea → reconos → fadereach → fdse → outcome → evidence → economic-attribution → evaluation → tads → sdea`

The machine-readable source is `workflows/canonical.json`; `policies/closed-loop-baseline.json` locks the expected order and required invariants.

## Non-negotiable boundaries

- Outcomes must be traceable to originating signals and opportunities.
- Evidence and economic attribution must remain distinct but linked through immutable execution, trace, and evidence identifiers.
- Successful delivery is not, by itself, proof of business outcome or recognized revenue.
- Replay must be idempotent; duplicate outcome or attribution events must not double count.
- Evaluation remains separate from production execution authority.
- Learning may update targeting/decisioning in TADS and SDEA; it must not rewrite Agent Platform policy, authorization, approval, budget, or execution authority.
- Human approval and opt-out boundaries for outreach and consequential actions remain intact.

## Certification

```bash
python3 scripts/certify_closed_loop.py
python3 scripts/forensic_audit_phase14.py
```

The dedicated workflow checks the canonical sequence and the post-phase audit. A green contract gate does not claim a real customer conversion or production revenue unless corresponding source evidence exists.
