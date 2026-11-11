# FCP-03 Provider-Neutral Closure Strategy

**Status:** Adopted closure strategy; implementation and acceptance remain in progress  
**Authority:** TSIC programme governance; Agent Platform remains the sole authorization and execution authority  
**Effective date:** 2026-11-11  
**Decision:** AWS-specific deployment assumptions are no longer mandatory FCP-03 exit criteria. The underlying security, operational, durability, and independent-assurance outcomes are not waived.

## 1. Decision

FCP-03 will close against provider-neutral, evidence-based security and production-readiness outcomes. AWS provisioning is not a prerequisite and no new AWS resource or charge is authorized by this strategy.

An equivalent provider-neutral control is acceptable only when deployed in an approved production-equivalent environment, enforcement is demonstrated, failure behavior is tested, evidence is independently reviewable, and residual risk is explicitly dispositioned.

This is an architecture and qualification decision, not a declaration that FCP-03 is complete. FCP-03 remains ACTIVE / INCOMPLETE. FCP-04 through FCP-10 remain GATED.

## 2. Non-negotiable boundaries

1. Zero new AWS spend. Do not create AWS infrastructure, consume promotional credits, or incur new AWS charges for FCP-03. Existing credits and forecasts are not authorization or a spend cap.
2. No collateral changes. Do not alter Tinlyt/TWI, FusionOps, ThreatFade, shared VPCs, production data, shared databases, or existing product runtime hosts to make FCP-03 tests pass.
3. No implicit production-host approval. Existing tinlyt-test-runtime remains a controlled test runner only. It is not an Agent Platform production worker or an egress enforcement boundary.
4. No evidence inflation. Unit tests, static IaC validation, ephemeral CI, local namespace tests, container smoke tests, and operator attestations cannot independently prove production deployment, sustained operation, provider/host trust, or independent security.
5. Authority remains centralized. Agent Platform is the sole consequential authorization and execution authority. Agent OS orchestrates lifecycle; SDK transports typed contracts; TADL declares; TSIC verifies. No model, prompt, memory, skill, tool output, registry record, or worker identity can independently grant authority.
6. Serial phase control. FCP-03 must be accepted before FCP-04 starts. No parallel phase advancement.

## 3. Provider-neutral reference architecture

The architecture defines control outcomes and replaceable implementations. Named technologies are candidate implementations, not mandatory vendor dependencies.

| Control plane | Required outcome | Candidate implementation patterns |
|---|---|---|
| Workload identity | Short-lived workload identity, audience binding, cryptographic proof, rotation, revocation, tenant binding | SPIFFE/SPIRE or equivalent issuer; signed JWT/SVID; DPoP or mTLS sender constraint |
| Secrets and key custody | External secret management, restricted access, rotation, audit, recoverability, separation of duties | OpenBao/Vault-compatible service; HSM/KMS-backed custody where available; sealed/encrypted backup |
| Network egress | Default-deny destination policy, controlled DNS, no direct resolver bypass, IPv4/IPv6 parity, metadata denial, tenant isolation, observable drops | Linux network namespaces, nftables, Unbound RPZ or equivalent policy resolver, explicit proxy/egress gateway |
| Workload isolation | Trusted supervisor, per-workload isolation, resource ceilings, filesystem and process boundaries, reliable termination/fencing | Firecracker microVM, gVisor, Kata, or separately assessed equivalent |
| Durable state | Transactional database/outbox, tenant isolation, queue/reconciliation, encrypted durable workspace, backup and tested restore | PostgreSQL with RLS and WAL/PITR; independent encrypted backup repository; durable queue |
| Observability and operations | Correlated traces/logs/metrics, security events, SLOs, verified alerts, runbooks, incident exercises | OpenTelemetry Collector, Prometheus-compatible metrics, Alertmanager or equivalent |
| Governance and assurance | Protected default branches, required checks, review controls, signed evidence, independent assessment | GitHub rulesets/branch protection; ASVS 5.0-based assessment; TSIC conformance evidence |

Implementations may differ, but security properties and tests may not be weakened.

## 4. Closure workstreams — execute in order

### A. Evidence and governance foundation

- Reconcile the canonical FCP-03 tracker, architecture decisions, repository heads, PRs, workflows, test artifacts, and residual-risk register.
- Define a control-to-test-to-evidence traceability matrix. Every exit criterion identifies its owner, implementation, test, evidence artifact, freshness, and acceptance authority.
- Inspect current required workflow names before configuring branch rulesets. Require PRs, independent review where available, exact CI/security/conformance checks, conversation resolution, and denial of force-push/deletion. Restrict and document emergency bypass.
- Verify protections by reading back active rulesets on all five core repositories.
- Keep the governance blocker open until protections are active and verified. If the connected GitHub integration lacks repository-administration write access, an authorized administrator must apply and verify rulesets.

**Exit evidence:** reconciled SHA inventory; traceability matrix; ruleset read-back; named control owners; no undocumented acceptance gaps.

### B. Network and DNS enforcement

- Implement a default-deny workload network boundary with explicit approved destinations and ports.
- Force DNS through the controlled resolver; reject direct external DNS, unauthorized DoT, DoH endpoints, QUIC bypass, direct-IP bypass, IPv6 bypass, DNS rebinding, and metadata destinations.
- Validate IPv4 and IPv6, route changes, resolver failure, controller failure, policy update/revocation, and tenant-to-tenant non-interference.
- Demonstrate that denied destinations cannot be reached through alternate interfaces, inherited host routes, proxy bypass, local routes, or resolver manipulation.
- Capture resolver decisions, firewall counters, packet/flow evidence, timestamps, policy revision, workload identity, and test correlation IDs.
- Distinguish endpoint reachability probes from complete protocol tests. A TCP/443 block to a known DoH endpoint is not a complete HTTP/2 DoH transaction test; a local TLS test does not prove TLS SNI inspection.

**Exit evidence:** reproducible adversarial test suite; positive and negative packet/flow captures; policy and counter snapshots; failure-mode evidence; independent review of bypass coverage.

### C. Identity, secrets, and revocation

- Deploy a dedicated workload identity issuer or equivalent, independent of Tinlyt identities and user/root credentials.
- Verify issuer/JWKS trust, signature and algorithm allowlists, issuer/audience/subject/tenant constraints, token expiry, nonce/proof binding, and replay resistance.
- Use short-lived credentials; implement rotation, revocation, stale-worker fencing, and measurable revocation propagation.
- Protect signing/encryption keys through an external secrets and key-custody boundary. Define recovery, key rotation, operator separation, and audit.
- Prove fail-closed behavior for issuer outage, malformed claims, stale JWKS, key rotation overlap, revoked identity, unavailable revocation service, and clock skew.

**Exit evidence:** deployed issuer and secret service configuration; end-to-end token/proof tests; rotation/revocation latency measurements; access audit; recovery drill; independent review.

### D. Runtime isolation and host assurance

- Select an approved production-equivalent host and runtime; do not promote the existing Tinlyt test runner by assumption.
- Document host trust boundary, CPU architecture, firmware/microcode and mitigation evidence available from the provider/operator. Record unavailable attestations as explicit residual risk.
- Enforce cgroups/resource ceilings, read-only or scoped filesystems, process/user isolation, network isolation, supervisor ownership, and reliable worker termination.
- Evaluate Firecracker, gVisor, Kata, or equivalent against the workload threat model. A container-only boundary must not be described as a microVM boundary.
- Verify persistent-computer/browser renderer isolation, profile encryption, lease fencing at every consequential command boundary, restart/recovery, snapshot lifecycle, and cleanup.
- Run sustained soak and adversarial tests on the approved environment, including resource exhaustion, noisy-neighbour behavior, supervisor death, stale worker, privilege boundary, and cross-tenant attacks.

**Exit evidence:** host/runtime inventory and trust statement; deployed configuration; sustained test artifacts; resource-limit measurements; isolation assessment; explicit limitations and residual-risk disposition.

### E. Durable persistence and recovery

- Deploy a production-equivalent transactional database/outbox and queue/reconciliation path with tenant isolation and least-privilege service identities.
- Encrypt data in transit and at rest; protect workspace profiles, snapshots, backups, and key material.
- Establish independent backup storage and retention. Demonstrate point-in-time recovery and clean-environment restore without reviving revoked credentials, permissions, or stale worker authority.
- Test interrupted backup/restore, corrupt snapshot, replay, cross-tenant restore, credential refresh, fencing continuity, and recovery of queue/outbox state.
- Measure and publish actual RPO/RTO from repeated drills; do not substitute design targets for measurements.

**Exit evidence:** deployed topology/configuration; backup integrity and restore logs; measured RPO/RTO; retention and access-control proof; recovery owner sign-off.

### F. Observability and operational readiness

- Instrument the execution path with correlated traces, metrics, structured security logs, and durable audit events.
- Define service and security SLOs, error budgets, capacity thresholds, noisy-neighbour limits, and actionable alert conditions.
- Route alerts to named, verified recipients and prove delivery. A configured recipient is not evidence of delivery.
- Publish incident runbooks for identity compromise, secret leakage, network-policy failure, tenant-isolation alert, runtime escape suspicion, data loss, queue backlog, and cost anomaly.
- Exercise incident detection, containment, revocation, rollback, recovery, communications, and post-incident evidence preservation.
- Assign named operational owners and on-call/escalation responsibilities.

**Exit evidence:** live dashboards; alert-delivery receipts; SLO definitions and observed windows; incident exercise reports; runbooks; named owners.

### G. Independent assurance and final FCP-03 decision

- Commission an assessor independent of implementation, with written scope covering identity, authorization, network/DNS, runtime isolation, secrets, tenant boundaries, persistence/restore, observability, and operations.
- Use OWASP ASVS 5.0 as one control catalogue where applicable, supplemented by threat-model-specific tests and architecture review. Automated scanners alone are insufficient.
- Require a signed report with scope, methods, evidence reviewed, findings, severity, exceptions, limitations, and retest results.
- Resolve all critical findings. High-risk exceptions require explicit, accountable written acceptance; no silent waivers.
- Conduct a final TSIC evidence review and publish a go/no-go decision against every exit criterion.

**Exit evidence:** assessor engagement and scope; signed assessment; finding dispositions and retests; residual-risk acceptance; TSIC acceptance record; exact mainline SHAs and post-merge checks.

## 5. FCP-03 exit criteria

FCP-03 is accepted only when all criteria below are evidenced:

- [ ] All five core repositories have verified branch governance and required checks.
- [ ] Network and DNS enforcement passes approved-destination, bypass, IPv4/IPv6, metadata, tenant-isolation, and fail-closed tests in an approved production-equivalent environment.
- [ ] Workload identity, proof-of-possession, key custody, rotation, and revocation are deployed and measured.
- [ ] Runtime isolation, host trust limitations, resource ceilings, persistent-computer security, and sustained operation are independently reviewed.
- [ ] Durable database/outbox/queue, encrypted workspace and backup, clean restore, and measured RPO/RTO are operational.
- [ ] Observability, SLOs, verified alert delivery, incident runbooks, exercises, and named ownership are operational.
- [ ] Capacity, noisy-neighbour, reliability, and operating-cost evidence is complete and reconciled without new AWS spend.
- [ ] Independent security assessment is complete; critical findings are resolved and all remaining risks have accountable dispositions.
- [ ] TSIC has reconciled exact repository SHAs, artifacts, workflow results, and signed acceptance.
- [ ] Programme owner records formal FCP-03 acceptance. Only then may FCP-04 begin.

A checkbox is not complete because a document describes a future action. It requires the linked evidence artifact and reviewer disposition.

## 6. Evidence classification

Every evidence item must carry one of these classifications:

- **E0 — Design:** architecture, threat model, control specification, runbook draft.
- **E1 — Static/repository:** source tests, static analysis, IaC validation, schema and policy validation.
- **E2 — Ephemeral integration:** CI services, temporary namespaces, containers, protocol and failure probes.
- **E3 — Controlled-host:** tests on an existing, bounded test host with documented scope and cleanup.
- **E4 — Production-equivalent deployed:** deployed service, operational telemetry, sustained tests, verified recovery, and named ownership.
- **E5 — Independent:** assessor-reviewed evidence, findings, retests, and signed disposition.

E0–E3 can establish implementation feasibility and expose defects. They cannot substitute for E4/E5 where the exit criterion requires deployed or independent evidence.

## 7. Zero-AWS-spend execution policy

- No new AWS provisioning, deployment, resource creation, paid tests, or promotional-credit consumption for this strategy.
- Do not assume credits, free tiers, budgets, or alarms provide a hard spend ceiling.
- Prefer existing approved non-AWS infrastructure, self-hosted open-source components, local deterministic tests, and existing CI capacity where usage is already covered.
- Before using any existing host, verify ownership, authorization, workload separation, resource limits, network boundaries, data classification, and no interference with product workloads.
- If no suitable production-equivalent environment is available at zero incremental cost, record the dependency as blocked and seek a separately approved environment; do not downgrade acceptance criteria or repurpose protected product infrastructure.
- Record any non-AWS third-party costs before commitment. This decision prohibits new AWS spend; it does not silently authorize other spend.

## 8. Explicitly retained blockers and dependencies

1. An approved production-equivalent host/runtime and durable service environment with no new AWS spend.
2. Dedicated workload identity issuer, external secret management, and measurable revocation.
3. Deployed destination-level network/DNS enforcement and adversarial packet/flow evidence.
4. Production-equivalent persistence, independent backups, and measured recovery.
5. Live telemetry, verified alert routing, incident exercises, and named owners.
6. Independent assessor availability, scope, report, and retest.
7. Independent approving review on the five core repositories. Default-branch rulesets were activated and read back on 2026-11-11 (see the control traceability register). Required approving review count remains 0 until a second reviewer exists. Do not treat the ruleset read-back as independent assessment.
8. Exact post-merge mainline validation and canonical tracker reconciliation.

## 9. Phase governance

- This strategy changes the method of satisfying FCP-03, not the phase sequence or exit bar.
- FCP-03 remains ACTIVE / INCOMPLETE until the checklist is satisfied and formally accepted.
- FCP-04–FCP-10 remain GATED.
- TSIC issue #102 remains open as the canonical acceptance tracker.
- No production deployment, independent assessment, or phase acceptance is claimed by this document.
