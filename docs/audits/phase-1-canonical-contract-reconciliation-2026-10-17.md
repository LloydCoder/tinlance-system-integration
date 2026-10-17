# Phase 1 — Canonical Architecture and Contract Reconciliation

**Status: IN PROGRESS — NOT CERTIFIED GREEN.**

Phase 0 was merged in TSIC PR #59 at `9d1d77a3bb1c7f12805d202cc7953e5c4d6d0bc6`. The reviewed ecosystem lock refresh was merged in TADL PR #47 at `cccff78ba88dcc2b9a5e22c14bf9175fbd81d105`. Phase 1 begins from that baseline and may not be marked complete until its implementation and conformance evidence pass.

## Scope

- Canonical authority map and system boundaries.
- Contract registry/version consistency.
- Platform HTTP/SDK/OS request boundary semantics.
- Trace-context representation and propagation semantics.
- Distinction between request identity, workspace context, execution identity, and event metadata.
- Explicit ownership of model/tool routing and external side-effect execution.

## Findings

### P1-01 — W3C trace context was represented incorrectly at the Platform HTTP boundary

TSIC's `contracts/telemetry/trace-context.json` requires a 32-character trace ID, a 16-character span ID, and a W3C `traceparent`; it also requires the identifiers to agree. The Platform HTTP adapter validated `traceparent` syntax but passed the entire header value into `APIRequest.trace_id`. That made a field named `trace_id` contain the full four-part header instead of the trace ID alone.

**Remediation in progress:** Platform PR [#98](https://github.com/LloydCoder/tinlance-agent-platform/pull/98) extracts the trace ID and span ID separately, preserves the original `traceparent`, and adds a focused extraction test. This item remains open until PR #98's exact head has green CI/security/conformance checks and is merged.

### P1-02 — Identity context combines fields from different context scopes

TSIC's `contracts/common/identity-context.json` currently lists `tenant_id`, `organization_id`, `workspace_id`, `actor_id`, `execution_id`, `trace_id`, and `correlation_id` as one required set. The Platform wire request instead binds `tenant_id` and `subject_id` to the authenticated principal and carries `request_id` plus optional W3C trace context. Agent OS has a workspace/task context; the Platform's principal and execution context are not identical to it.

This is a contract-model ambiguity, not proof that the Platform should become the owner of workspace identity. The canonical model must distinguish:
- authenticated request context (Platform principal, tenant, request ID, optional trace context);
- OS workspace/task context (OS-owned identifiers propagated as non-authoritative context);
- execution/evidence context (Platform-owned run/execution/evidence identifiers);
- event envelope context (the fields required for a specific event type).

**Disposition:** resolve the normative context scopes and versioning in Phase 1, then implement identity and tenant-binding adversarial tests in Phase 2. No layer may promote caller-supplied workspace or correlation metadata into authorization.

### P1-03 — Event envelope mapping needs an explicit boundary

The TSIC event envelope is CloudEvents-compatible and defines event identity, source, type, time, subject and data. Platform SDK/OS event models currently use a normalized shape such as `event_id`, `event_type`, `occurred_at`, `platform_run_id`, and `payload`. The adapter mapping is valid only if the canonical envelope-to-client mapping is explicit and the required fields are preserved. A tenant ID must never be substituted for a workspace ID.

**Disposition:** carry this as a Phase 3 event-contract acceptance gate. Phase 1 must make the mapping and ownership boundary explicit in the canonical architecture; Phase 3 must implement and test it end to end.

### P1-04 — Routing and execution authority must remain singular

TSIC defines Platform as the model-routing and governed-execution authority. OS and SDK may provide intent, task context, typed requests and user-facing orchestration, but must not independently authorize or execute consequential actions. External content, tool output, memory and peer-agent messages remain untrusted data.

**Acceptance:** architecture and adapter declarations explicitly distinguish routing requests from routing decisions, and execution requests from authorization decisions.

## Required changes

1. Keep Platform as the sole generic consequential execution authority.
2. Make request, workspace, execution and event context scopes explicit in canonical contracts.
3. Preserve exact contract versions and reviewed commit pins; fail closed on drift.
4. Normalize W3C trace context at the Platform boundary and verify that `trace_id`, `span_id` and `traceparent` are distinct, valid and consistent.
5. Define event-envelope-to-SDK/OS mapping without conflating tenant and workspace identifiers.
6. Preserve an explicit distinction between reference integration success and deployed production evidence.

## Phase 1 exit gate

- [ ] Platform PR #98 is merged after all required checks pass on the exact head SHA.
- [ ] Canonical architecture and context-scope documentation are reconciled.
- [ ] Contract registry versions agree with their normative contract files.
- [ ] The four-repository lock still points to a tested, compatible baseline.
- [ ] Cross-repository reference E2E passes against the reviewed lock.
- [ ] Authority-boundary, compatibility and trace-context tests pass.
- [ ] No critical architecture/contract ambiguity remains in Phase 1 scope.
- [ ] Post-phase forensic audit records commit SHAs, workflow runs, evidence and remaining deferred gates.

## Explicit limitations

This phase audit does not certify deployed production identity, external secret management, durable event infrastructure, sandbox isolation, production telemetry, backup/restore, or incident response. Those require their own later-phase and production evidence.
