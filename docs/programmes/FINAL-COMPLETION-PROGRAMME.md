# Tinlance Agent Systems — Final Completion Programme

**Programme ID:** FCP  
**Version:** 1.0  
**Baseline:** 2026-11-08  
**Programme authority:** TSIC (system-of-systems programme governance and conformance evidence)  
**Execution authority:** Tinlance Agent Platform  
**Status:** FCP-00 accepted; FCP-01 is the next eligible phase. Overall programme completion and production certification remain outstanding.

## 1. Mission

Complete Tinlance Agent Systems as a model-independent, secure, persistent, autonomous agent ecosystem for individuals, developers, businesses and enterprises.

The target is an operating environment in which users can create, configure, own, deploy, coordinate and govern persistent AI agents and agent teams. Agents must be able to use authorized applications, tools and local/cloud computers; retain governed memory; execute durable multi-step work; run scheduled and event-driven routines; collaborate; recover from failures; and produce verifiable evidence.

This programme consolidates, but does not renumber or replace, the existing Platform M0–M29 roadmap, ecosystem P0–P10 matrix, TSIC-00…TSIC-19 certification sequence, or persistent-computer W2–W6 acceptance sequence.

## 2. Product benchmark set

The four primary product benchmarks are:

1. **OpenMausBot** — local-first persistent agents, desktop agent roster, computer execution and agent handoffs.
2. **Rakazo** — self-hosted AI teammates, per-agent memory/tools/prompts, BYOM and background routines.
3. **ChatGPT Dots** — persistent personal agents, personalization, connected applications and proactive ongoing tasks.
4. **Grok Bot** — conversational intelligence, research, tool use and agentic task execution.

Additional engineering references include OpenHands, Orkas, Dify, Langflow, n8n, LangGraph, Microsoft Agent Framework and CrewAI. These are capability references, not architectural authorities or products to clone.

## 3. Non-negotiable architecture and authority

- **Agent Platform:** sole consequential execution and authorization authority: identity, authentication, authorization, policy, approvals, runtime, tool/MCP mediation, sandbox, secrets, budgets, evidence, audit and observability.
- **Agent OS:** agent/workspace/task lifecycle, orchestration, durable state, memory orchestration, scheduling, delegation, teams and channels.
- **Platform SDK:** typed, versioned client contracts; it transports authoritative Platform decisions and cannot grant authority.
- **TADL / Agent Developer:** agent declarations, schemas, configuration, validation, skills, packaging and developer experience.
- **TSIC:** system registries, integration contracts, compatibility, conformance, evidence lineage and certification. TSIC is not an execution runtime.

Authority invariant: **TADL declares → OS composes → SDK transports → Platform authorizes and executes → TSIC verifies.**

Models, prompts, memory, retrieved content, tool output, registry metadata, MCP metadata, A2A messages and evaluation outcomes never independently grant authority. Persistent computers are execution environments, not security principals. Restore must not restore revoked permissions, expired credentials or stale worker authority.

## 4. FCP phase sequence

### FCP-00 — Forensic baseline and programme reconciliation
Inventory all in-scope repositories, default-branch heads, open/closed PRs and issues, exact merge SHAs, CI evidence, dependency locks, canonical docs and acceptance records. Resolve contradictory status statements. Publish a traceability matrix and residual-risk register. No implementation is marked complete without evidence.

### FCP-01 — Contracts and ecosystem conformance
Validate Platform/OS/SDK/TADL/TSIC contracts, tenant and identity propagation, authorization, approvals, event durability, trace/evidence lineage, registry governance, model/tool routing, adapters, budgets, MCP/A2A and end-to-end recovery. Reconcile exact immutable SHAs and TSIC evidence.

### FCP-02 — Persistent computers and durable execution
Complete W2–W6 in sequence. W2–W4 are accepted only for ephemeral CI feasibility at the baseline. W5 requires a genuine continuous eight-hour soak, supervisor fencing at every consequential command boundary, restarts, lease expiry/revocation, quotas, audit continuity, crash recovery and cleanup. W6 requires consistent snapshots, integrity/provenance, clean-host restore, storage reattachment, identity preservation, fencing continuity, stale-worker revocation, credential refresh, replay prevention, interrupted-restore recovery, corrupt snapshot rejection and cross-tenant denial.

### FCP-03 — Production security and infrastructure qualification
Qualify deployed durable DB/outbox/queue, secret manager, trusted supervisor and sandbox runtime, telemetry, backup/restore, incident response and named operational ownership. Close production network egress, DNS, hardware/microcode, CPU/SMT, cgroups, encrypted profile storage, live identity/revocation and independent security-review blockers. Mocks and interfaces do not establish deployment.

### FCP-04 — Agent workforce runtime and autonomous orchestration
Deliver persistent agent identities, lifecycle, workspaces, model/provider selection and BYOM, durable task state, multi-step execution, agent teams, delegation, handoffs, retries, cancellation, interruption/resume, human escalation, budgets and recovery.

### FCP-05 — Connected applications, tools and interoperability
Deliver real MCP/A2A and application integrations, OAuth/delegated authorization, webhooks, event triggers, browser/computer tools, research, email/calendar/files/CRM/developer/cloud connectors. Enforce origin and destination validation, SSRF/DNS-rebinding protection, tenant propagation, capability attenuation, credential isolation, revocation and cross-agent audit causality.

### FCP-06 — Persistent memory, learning and skills
Deliver user-, agent- and workspace-scoped memory, retrieval, provenance, access controls, retention/deletion, demonstration-to-skill workflows, skill authoring/testing/versioning and controlled promotion. Memory and learned skills cannot elevate privileges or bypass Platform policy.

### FCP-07 — Proactive agents, routines and autonomous work
Deliver durable schedules, recurring routines, event-driven execution, background monitoring, conditional workflows, proactive research, notifications, reports, goal tracking, escalation and user pause/resume/revoke controls. Failures and missed executions must be visible; consequential actions remain approval- and policy-governed.

### FCP-08 — Personal and enterprise agent experience
Deliver agent roster/contact model, persistent conversations/projects/history, agent creation/configuration, model/tool/skill/memory management, browser/desktop/terminal/filesystem experiences, local/cloud computers, agent teams, approvals, personal workspaces, proactive assistance, web/desktop/mobile channels, voice/multimodal interfaces, enterprise tenant administration, RBAC, policy, audit, compliance, fleet and budget controls.

### FCP-09 — Economics, reliability, observability and release engineering
Benchmark Firecracker/gVisor/Kata; startup/snapshot/restore latency; p50/p95/p99; concurrency/noisy neighbours; CPU/memory/storage/network; per-tenant/workspace-hour/execution costs; spend caps; exhaustion/leak/teardown and billing reconciliation. Operationalize OpenTelemetry, traces, security-event correlation, SLOs, error budgets, alerts, incident exercises, RTO/RPO, signed artifacts, SBOM, provenance, immutable dependencies, migrations, rollback and release recovery.

### FCP-10 — Independent certification, GA and final acceptance
Complete independent penetration/red-team assessment, tenant-isolation and authorization testing, persistent-computer and browser/network security, credential/secret protection, snapshot/restore security, agent delegation/interoperability, memory/skill security, performance/economics, production recovery, operational ownership, release assurance and end-user/enterprise acceptance. TSIC issues final conformance evidence. No unresolved critical security blocker; high-risk exceptions require accountable written acceptance.

## 5. Baseline findings — 2026-11-08

### Repositories in scope

- `LloydCoder/tinlance-agent-platform`
- `LloydCoder/tinlance-agent-os`
- `LloydCoder/tinlance-agent-platform-sdk`
- `LloydCoder/tinlance-agent-developer` (TADL)
- `LloydCoder/tinlance-system-integration` (TSIC)

Adjacent product: `LloydCoder/tinlance-tads` is Target / Account / Demand Signal Intelligence, not a core Agent Systems implementation repository.

### Exact default-branch baseline SHAs

These are the observed `main` heads before the FCP-00 documentation PRs:

| Repository | Observed `main` SHA |
|---|---|
| Agent Platform | `bf115673a7250fca082d9e81d45ab9eb4208fd6b` |
| Agent OS | `aafce0b0d8029e6bac1cf335af24d3da8c6455e0` |
| Platform SDK | `e418f9de6639779381a0cebc746991a52a8df1ce` |
| TADL / Agent Developer | `b8f9e6e1fe34e59352e7fae553f81865b53b9f99` |
| TSIC | `b490b761fed638232bd47bea3b3792e0c2695a18` |

### Live open-work inventory

At the baseline audit, live repository-scoped searches returned no open PRs or ordinary open issues in Agent Platform, Agent OS, Platform SDK or TADL. TSIC has one open umbrella issue: [#102](https://github.com/LloydCoder/tinlance-system-integration/issues/102). TADS has two open dependency PRs, #43 (pytest) and #44 (mypy); they are tracked separately and are not FCP blockers.

### Persistent-computer evidence

- W2: accepted for ephemeral CI feasibility.
- W3: accepted for ephemeral CI feasibility; PR [#197](https://github.com/LloydCoder/tinlance-agent-platform/pull/197) merged as `2c3903c4fee096aa285014d9dc8aa6b1e5f809ea`.
- W4: accepted for ephemeral CI adversarial feasibility; PR [#200](https://github.com/LloydCoder/tinlance-agent-platform/pull/200) merged as `20d1b31683060e96b3e66594fa8f3b2c2f630bde`.
- W5: durable PostgreSQL workspace lease implementation merged in PR [#201](https://github.com/LloydCoder/tinlance-agent-platform/pull/201), merge `d4fe2537499d30c74d0129bccc33b84f088b4eef`; NULL-safe fencing correction merged in PR [#202](https://github.com/LloydCoder/tinlance-agent-platform/pull/202), merge `bf115673a7250fca082d9e81d45ab9eb4208fd6b`. PR-head CI, CodeQL, Secret Scan, R10 and Reference Agents runs were observed successful on both inspected heads. **W5 acceptance is still open** pending the genuine eight-hour soak and trusted-supervisor enforcement evidence.
- W6: snapshot/restore acceptance remains outstanding.

### Existing roadmap status

- Platform M0–M29: documented as repository implementation complete. This is not external production certification.
- Ecosystem P0–P10: current-release section records repository-level certification through P10; the phase-matrix opening paragraph had stale P10-in-progress wording and is reconciled separately.
- TSIC TSIC-00…TSIC-19 remains its own system-of-systems certification namespace.
- W2–W6 remains the persistent-computer acceptance namespace.

### Production residuals carried forward

1. Provider-attested host SKU, firmware, microcode, SMT and CPU mitigation evidence.
2. Independent TCP/443 destination enforcement.
3. Explicit DNS query-name policy.
4. Trusted supervisor enforcement of fencing at every consequential command boundary.
5. Durable encrypted browser-profile storage.
6. Production cgroups and resource isolation.
7. Live identity, workload identity and revocation propagation.
8. Production backup/restore and disaster recovery.
9. Production telemetry, SLOs and incident response.
10. Independent security assessment and accountable residual-risk acceptance.

W2–W4 ephemeral acceptance does not close these production residuals. W5 PR merges do not constitute the eight-hour soak. P0–P10 and M0–M29 repository completion do not establish a deployed production service.

## 6. FCP-00 closeout record — accepted 2026-11-08

FCP-00 is accepted after the live baseline audit, documentation reconciliation, issue correction, exact-head validation, merge and post-merge verification.

### Reconciliation changes

| Repository | PR | Merge commit | Post-merge workflows |
|---|---|---|---:|
| Agent Platform | [#203](https://github.com/LloydCoder/tinlance-agent-platform/pull/203) | `15caa3ebd65e5f569347aa5db01bb90af6e65c6a` | 6/6 successful |
| TADL | [#105](https://github.com/LloydCoder/tinlance-agent-developer/pull/105) | `5e28c5f0b923b3eeef44f3714dfacea1c1c49220` | 8/8 successful |
| TSIC | [#110](https://github.com/LloydCoder/tinlance-system-integration/pull/110) | `dd5de47d0f0cf33379273bbe50073ec97934f25c` | 34/34 successful |

PR-head validation was also green: Platform 5/5, TADL 5/5 and TSIC 33/33 workflows. The TSIC PR included the cross-repository integration and certification workflows. No failed workflow was observed on these exact heads or the listed merge commits.

### Canonical records reconciled

- Platform persistent-computer acceptance now records W4 as merged/accepted for ephemeral CI feasibility and W5 lease implementation PRs #201/#202 as merged, while retaining the eight-hour soak as outstanding.
- TADL phase matrix now consistently records P0–P10 as repository/reference-scope certified, including P10 recovery. External production deployment remains unverified.
- TSIC issue [#102](https://github.com/LloydCoder/tinlance-system-integration/issues/102) now reflects W2–W4 ephemeral acceptance, W5 implementation versus soak distinction, W6 outstanding work and production residuals.
- This master programme is linked from the TSIC README and is the cross-repository FCP reference.

### FCP-00 exit checklist

- [x] All five core repositories identified and accessible.
- [x] Exact pre-reconciliation default-branch baseline SHAs recorded.
- [x] Open PR and issue inventory completed.
- [x] W3/W4/W5 merge dispositions verified.
- [x] W5 eight-hour soak explicitly retained as outstanding.
- [x] W6 and production residuals explicitly retained as outstanding.
- [x] Platform, TADL and TSIC documentation inconsistencies reconciled.
- [x] TSIC issue #102 updated without falsely closing acceptance.
- [x] Required PR-head workflows green.
- [x] All three documentation PRs merged.
- [x] Post-merge mainline workflows green: Platform 6/6, TADL 8/8, TSIC 34/34.
- [x] Core repositories have no remaining open PRs; TSIC #102 remains the open persistent-computer acceptance tracker.

**Disposition:** FCP-00 complete. Proceed serially to FCP-01. This closeout does not claim W5/W6, production certification, product completion or final FCP completion.

## 7. Requirements-to-repository ownership

| Capability | Primary owner | Required conformance |
|---|---|---|
| Execution authority, policy, approvals, runtime, sandbox, secrets, budgets, evidence | Agent Platform | TSIC |
| Agent lifecycle, workspaces, task orchestration, memory orchestration, schedules, delegation | Agent OS | Platform + SDK + TSIC |
| Typed contracts and client behavior | Platform SDK | Platform + OS + TSIC |
| Agent declarations, schemas, skills, authoring and packaging | TADL | Platform + OS + SDK + TSIC |
| System contracts, lock, compatibility, integration and certification | TSIC | All in-scope repositories |

## 8. Competitive acceptance scenarios

Validate the four benchmarks with reproducible end-to-end tasks:

1. Create a persistent agent with identity, role and instructions.
2. Configure a model/provider and authorized tools.
3. Assign a local or cloud computer.
4. Complete multi-step research and execution.
5. Delegate subtasks to other agents and reconcile results.
6. Preserve agent and workspace state across restart.
7. Execute an approved recurring background routine.
8. Respond to an authorized external event.
9. Retrieve memory with provenance and access controls.
10. Create, test and promote a skill under controlled governance.
11. Recover from worker/process/host failure.
12. Revoke access during active execution and prove stale workers cannot act.
13. Restore a workspace without restoring stale authority.
14. Produce verifiable action/evidence/audit lineage.
15. Operate the experience across supported web, desktop and mobile channels.

Every scenario records exact code/model/configuration, permissions, expected and actual result, evidence, security outcome, latency, cost, and failure/recovery behavior. No unsupported superiority claims.

## 9. Serial execution and release protocol

1. Only the first uncertified FCP phase may be active.
2. Inspect exact current repository and dependency SHAs before implementation.
3. Research the technical, standards and security requirements.
4. Reproduce defects with tests before fixes; implement with regression coverage.
5. Run focused tests, full suites, security checks and all required workflows.
6. Review diffs for authority-boundary, tenant-isolation, privacy and supply-chain regressions.
7. Merge only after all required exact-head checks are green and acceptance criteria are met.
8. Verify the merge SHA and post-merge mainline workflows.
9. Reconcile documentation, locks, manifests and dependency pins.
10. Record evidence, residual risks and phase disposition before proceeding.

A missing provider attestation, physical host, independent reviewer or production service is a blocked gate, not a reason to substitute mocks or claim completion.

## 10. Definition of final completion

FCP is complete only when all three are true:

- **Infrastructure:** Platform, identity, authorization, sandbox, persistent computers, recovery and production dependencies are implemented and production-qualified.
- **Product:** persistent personal and enterprise agents can use memory, tools, computers, integrations, schedules, teams and proactive workflows through a usable experience.
- **Independent assurance:** cross-repository conformance, security, recovery, economics, operations and release evidence are independently accepted and TSIC publishes final certification.

A green workflow is necessary but insufficient. Final completion is not claimed by this baseline document.
