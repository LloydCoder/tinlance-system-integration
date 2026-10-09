# TSIC-15 — Observability and Trace Context Contract

## Purpose

Provide a stable correlation spine across tenant-scoped workflows, agents, executions, delivery, evidence, and economic attribution without creating a parallel authorization or execution authority.

## Standards baseline

- W3C Trace Context: `traceparent` version `00` is encoded as `00-{trace-id}-{parent-id}-{trace-flags}`.
- OpenTelemetry semantic conventions are pinned to `1.37.0` in both the observability baseline and trace-context contract.
- Machine-readable contract: `contracts/telemetry/trace-context.json`.
- Canonical fields/invariants: `policies/observability-baseline.json`.

## Required trace invariants

- Trace IDs are exactly 32 lowercase hexadecimal characters; span IDs are exactly 16 lowercase hexadecimal characters.
- All-zero trace and span IDs are invalid.
- IDs in `traceparent` must match the explicit `trace_id` and `span_id` fields.
- Correlation must survive system boundaries and allow execution events to join to evidence and economic attribution.
- Tenant context is mandatory for tenant-scoped events and comes from verified server-side identity context.
- Baggage is allowlist-only, size bounded, and must not carry credentials, tokens, secrets, or other sensitive values.
- Sampling flags are telemetry hints, never authorization, policy, approval, or execution capabilities.
- Logs and spans must not contain secrets. Redaction is not a substitute for avoiding secret collection.

## Validation

```bash
python3 scripts/certify_observability.py
python3 scripts/forensic_audit_phase15.py
```

The dedicated workflow tests valid and invalid trace contexts and verifies the cross-system field spine. This certifies repository contract conformance, not the availability or correctness of a live telemetry backend.
