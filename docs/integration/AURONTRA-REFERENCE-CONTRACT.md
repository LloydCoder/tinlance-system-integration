# Aurontra Reference Integration Contract

**Status:** Reference contract registered for conformance development; not production certification.  
**Product repository:** `LloydCoder/AURONTRA`  
**TSIC authority:** `LloydCoder/tinlance-system-integration`

## Responsibility boundaries

- Aurontra owns IT-resilience domain workflows, service-desk assistance, telemetry analysis, remediation intent planning, threat analysis, and product-facing evidence consumption.
- Tinlance Agent Platform remains the sole generic consequential execution authority for identity, authorization, policy, approvals, sandbox, secrets, tool execution, and authoritative execution evidence.
- TSIC owns cross-system contract definitions, registry records, compatibility policy, conformance requirements, and certification evidence.
- The Agent Platform SDK is a client surface; its use does not confer authority.

## Contract bindings

| TSIC contract | Aurontra surface | Required invariant |
|---|---|---|
| `identity-context` | Verified tenant and subject context | Tenant identity comes from verified server-side state, never request JSON. |
| `event-envelope` | Telemetry, findings, remediation, verification evidence | Preserve provenance, schema version, tenant binding, event identity, and trace context. |
| `delivery-semantics` | Durable job/outbox and replay handling | At-least-once delivery must be idempotent; do not claim exactly-once semantics. |
| `trace-context` | API, worker, and governed action correlation | Preserve trace/correlation identifiers without leaking secrets or PII. |
| `agent-registration` | Service identity and capability references | Registered capabilities are references only; Platform policy and approvals remain authoritative. |

## Fail-closed behavior

- Missing or mismatched tenant identity, unsupported contract versions, stale evidence, invalid signatures, replay conflicts, or absent independent verifiers must fail closed.
- Platform submission success is not proof that a business postcondition occurred.
- A threat finding or heuristic score is not proof of containment. Containment claims require fresh, target-bound independent verification evidence.
- No local shell, service manager, firewall, or other side-effect fallback is permitted in Aurontra.
- Registering this reference contract does not enable production flags or certify live integration.

## Conformance gates still required

1. Validate the ecosystem manifest and adapter registry against TSIC schemas and repository CI.
2. Add automated contract tests for identity context, event envelope/version, idempotency/replay, trace propagation, and sanitized failures.
3. Exercise the exact reviewed SDK/API contract in isolated tests and verify Platform non-executable/approval-gated states.
4. Prove the independent verification ingress binds tenant, device, finding, action, execution, and fresh evidence.
5. Complete failure/retry/reconciliation tests for worker/outbox and unknown Platform outcomes.
6. Run controlled sandbox integration only after a safe test tenant and credentials are provisioned.
7. Publish a forensic audit tied to exact commits and CI runs before declaring the integration phase complete.

Until these gates pass, this record is a reference contract only; Aurontra's production data plane, remediation submission, and threat containment must remain disabled.
