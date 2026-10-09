# TSIC-10 — ThreatFade Web ↔ ThreatFade Engine

## Purpose

Certify that ThreatFade Web consumes the ThreatFade Engine as the source of detection and analyst truth while preserving distinct product, domain, and execution authorities.

## Reviewed immutable revisions

- ThreatFade Engine: `LloydCoder/tinlance-threatfade@4691ead86fadd1c95767886d7fb15bacbed012fe`
- ThreatFade Web: `LloydCoder/tinlance-threatfade-web@f2865a034794f706bd57e4427a4e698942c95b54`

The integration workflow checks out both reviewed revisions without persisting checkout credentials. It runs engine architecture and analyst tests; web truth, documentation, growth, format, lint, typecheck, unit, dependency audit, build and browser E2E checks; starts the live engine API; verifies health/version and API payloads against web schemas and canonical truth; then runs the authority contract certifier and post-phase forensic audit.

## Authority boundaries

- ThreatFade Engine owns detection, response analysis, and analyst truth.
- ThreatFade Web owns product presentation, analyst workflow, research surface, and commercial workflow.
- FAS-Bench remains independent evaluation authority, not a runtime dependency of the engine.
- Agent Platform remains the generic consequential execution authority.
- TSIC owns ecosystem contracts and certification, not domain execution.

## Security invariants

- Analyst authorization is enforced by the engine, not inferred from the browser.
- Browser clients never receive engine credentials.
- Web proxying is restricted by path allowlists, timeouts, redirect rejection, and response-size limits.
- Playground input is untrusted and resource-bounded.
- Product claims must reconcile to engine truth; a presentation-layer claim is not evidence of detection.

## Certification evidence

- Dedicated workflow: [TSIC-10 ThreatFade Web Engine Integration E2E](../../.github/workflows/threatfade-web-engine-e2e.yml)
- Contract certifier: `scripts/certify_threatfade_web.py`
- Live API/schema certifier: `scripts/certify_threatfade_web_live.py`
- Forensic audit: `scripts/forensic_audit_phase10.py`

The TSIC-10 E2E workflow is re-running against the reviewed dependency-remediation revision after CI exposed an upstream workflow-file formatting defect. Phase status is controlled by the canonical phase registry and must be re-certified when relevant contracts or dependencies change.
