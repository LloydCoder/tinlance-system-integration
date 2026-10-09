# TSIC-11 — BugFlow Integration

## Purpose

Certify the integration boundary between TSIC's canonical ecosystem contracts and BugFlow's application-security testing and vulnerability-intelligence capabilities. TSIC owns integration contracts and certification; BugFlow owns domain testing and finding generation; Agent Platform remains the sole generic consequential execution authority.

## Reviewed dependency

- Repository: `LloydCoder/bugflow-elite`
- Immutable reviewed revision: `c9ef8b5f7ef87aaaf23b943a498f39ce8697d07b`
- Baseline: `policies/bugflow-baseline.json`
- Adapter: `integrations/bugflow/adapter.json`

The integration workflow checks out the reviewed revision by full commit SHA, disables persisted checkout credentials, compiles Python sources, runs the BugFlow test suite, validates TSIC contract bindings, and runs the post-phase forensic audit.

## Required contract bindings

| TSIC contract | BugFlow surface | Direction |
|---|---|---|
| `identity-context` | Tenant/application context | Inbound |
| `event-envelope` | Finding and test-evidence events | Bidirectional |
| `delivery-semantics` | Replayable test-execution evidence | Bidirectional |
| `trace-context` | Scan/finding correlation | Bidirectional |
| `economic-attribution` | Testing cost attribution | Inbound |

## Non-negotiable authority and safety invariants

- Testing and findings do not confer execution authority.
- Findings retain source provenance and evidence lineage.
- Tenant context is immutable across the integration boundary.
- TSIC remains the authority for ecosystem contracts and certification.
- Agent Platform remains the generic consequential execution authority.
- BugFlow runs only against explicitly authorized scope; scope checks, resource limits, and human disclosure approval remain mandatory.
- A successful integration check is not a claim that a target is vulnerable or that a disclosure has been approved.

## Certification and audit

Run from the TSIC repository root:

```bash
python3 scripts/certify_bugflow.py
python3 scripts/forensic_audit_phase11.py
```

The dedicated GitHub Actions workflow additionally runs BugFlow's Python compilation and test suite. TSIC-11 may be marked completed only after all required checks pass on the same commit and the forensic audit is green.

## Recovery and re-certification

The integration uses immutable revision pins and evidence-producing checks. If the upstream BugFlow revision changes, update the baseline and workflow pin together, rerun the full workflow, and reconcile this document. A failed or unavailable upstream check must fail closed; it must not be represented as a certified integration.
