# TSIC-12 — Hezqara Governed Healthcare Integration

## Purpose

Certify the ecosystem boundary for Hezqara's governed healthcare administrative workforce. Hezqara remains a healthcare operations system, not an EHR replacement or a diagnosis, triage, symptom-checker, treatment-decision, or prescribing engine. AI Scribe output remains a draft requiring clinician review, editing, and approval.

## Reviewed immutable revision

- Repository: `LloydCoder/hezqara`
- Reviewed commit: `e1f5749fc334262eaf63cf25837b629ca86b09b6`
- Baseline: `policies/hezqara-baseline.json`
- Adapter: `integrations/hezqara/adapter.json`

The dedicated integration workflow checks out the immutable reviewed commit without persisting credentials; compiles and tests the backend; checks backend dependency consistency; runs frontend lint, type-check, and production build; then validates the TSIC contract and runs the post-phase forensic audit. The upstream HEZQARA CI and production-proving workflows provide additional repository-level evidence.

## Required contract bindings

| TSIC contract | Hezqara surface | Direction |
|---|---|---|
| `identity-context` | Clinic, patient, and workforce context | Inbound |
| `event-envelope` | Governed clinical workflow and provenance events | Bidirectional |
| `delivery-semantics` | Reviewable governed workflow transitions | Bidirectional |
| `trace-context` | Workflow provenance correlation | Bidirectional |
| `economic-attribution` | Workflow and cost attribution | Inbound |

## Non-negotiable invariants

- Verified server-side tenant context and database RLS remain authoritative; client-supplied tenant identifiers do not grant authority.
- Clinician review/edit/approval remains mandatory for AI Scribe drafts.
- Healthcare workforce capabilities do not grant generic consequential execution authority.
- Provenance is preserved through the integration boundary.
- TSIC owns integration contracts; Hezqara owns healthcare workflow semantics; Agent Platform owns generic execution authority.
- CI evidence is not a certification of HIPAA, GDPR, NDPA, SOC 2, ISO 27001, FHIR/SMART conformance, clinical efficacy, or production readiness.

## Certification commands

```bash
python3 scripts/certify_hezqara.py
python3 scripts/forensic_audit_phase12.py
```

The phase may be marked completed only when the dedicated workflow is green and the forensic audit passes on the same repository revision.

## Re-certification

Any change to the Hezqara pin, tenant/clinic authorization, RLS policies, clinician review boundary, workflow provenance, contract registry, or adapter invalidates this certification until the affected gates are rerun.
