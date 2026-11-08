# Tinlance Agent Systems — Final Completion Programme

**Programme ID:** FCP  
**Version:** 1.0  
**Baseline:** 2026-11-08  
**Programme authority:** TSIC (system-of-systems programme governance and conformance evidence)  
**Execution authority:** Tinlance Agent Platform  
**Status:** FCP-00 and FCP-01 accepted; FCP-02 (persistent computers and durable execution) is active. Overall programme completion and production certification remain outstanding.

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

## 7. FCP-01 closeout record — accepted 2026-11-08

FCP-01 reconciled the exact reviewed repository references, canonical ecosystem lock, manifest, registry provenance and cross-repository conformance checks. The phase was merged only after the complete exact-head CI, security, secret-scan, CodeQL and ecosystem integration workflows passed. Post-merge mainline checks were then inspected.

### Merged implementation and reconciliation

| Repository | Change | Merge commit | Post-merge validation |
|---|---|---|---|
| Agent Platform | [PR #204](https://github.com/LloydCoder/tinlance-agent-platform/pull/204) aligns reference-agent SDK dependency to the exact locked SDK SHA | `b2b5d61c7094ca3f31121ce33a4222d3fe994835` | 6/6 workflows successful |
| TADL / Agent Developer | [PR #106](https://github.com/LloydCoder/tinlance-agent-developer/pull/106) refreshes exact pins, aligns manifest and registry provenance, and corrects conformance expectations to the canonical Platform contract | `0b27b6bad966884961fb0e90055ca58837a87558` | 8/8 workflows successful |
| Tinlyt / TWI | [PR #154](https://github.com/LloydCoder/tinlance-web-intelligence/pull/154) aligns OpenTelemetry API, SDK and OTLP exporter to 1.45.2 | `48a89f64a77d125e07ac9816b73738e4e6106dc8` | 2/2 workflows successful |

TADL PR #106's complete exact-head gate passed: CI, Security, Secret Scan, CodeQL and Ecosystem Integration. The cross-repository integration job exercised the pinned TADL, Agent OS, SDK, Platform, TWI and World Intelligence revisions, including P0–P10 conformance and P10 recovery. The first run exposed two real drift defects: stale idempotency error casing in P2 conformance and stale repository/provenance SHAs in the P5 registry. Both were corrected against the canonical Platform contract and immutable ecosystem lock; the final exact-head workflow set was fully green before merge.

Platform PR #204's exact-head Reference Agents, R10 Certification, CI, CodeQL and Secret Scan workflows all passed. The post-merge Platform mainline had 6/6 successful workflows. TWI PR #154's post-merge CI and OpenSSF Scorecard workflows both passed.

### Reviewed immutable integration baseline

| Component | Reviewed SHA |
|---|---|
| Agent Platform | `b2b5d61c7094ca3f31121ce33a4222d3fe994835` |
| Agent OS | `aafce0b0d8029e6bac1cf335af24d3da8c6455e0` |
| Platform SDK | `e418f9de6639779381a0cebc746991a52a8df1ce` |
| TADL / Agent Developer | `0b27b6bad966884961fb0e90055ca58837a87558` |
| TSIC authority | `f021d09cddd68d731c88cd5209c33789e78b4ae5` |
| Tinlyt / TWI | `48a89f64a77d125e07ac9816b73738e4e6106dc8` |
| World Intelligence | `57d326553c0bbebe4d0ad5cb947e7cab38f947ab` |

The TADL registry's repository reviewed SHAs, supply-chain reviewed SHAs and commit provenance URIs now match the immutable dependency lock. The P10 manifest retains its contract-surface meaning and explicitly distinguishes repository/reference-scope certification from deployed production assurance. The Platform reference-agent package metadata now pins the same SDK commit as the ecosystem lock.

### FCP-01 exit checklist

- [x] Exact immutable references inspected across Platform, OS, SDK, TADL, TSIC, TWI and World Intelligence.
- [x] Platform reference-agent SDK pin reconciled with the ecosystem lock.
- [x] TADL ecosystem lock and manifest aligned.
- [x] P2 conformance assertions aligned with canonical Platform error semantics.
- [x] P5 registry reviewed SHAs, supply-chain SHAs and provenance URIs aligned with the lock.
- [x] P0–P10 and P10 recovery cross-repository conformance passed on the final exact PR head.
- [x] Required CI, security, CodeQL, secret-scan and integration workflows green before merge.
- [x] Platform PR #204, TADL PR #106 and TWI PR #154 merged.
- [x] Post-merge mainline validation green for the three affected repositories.
- [x] No open PRs or ordinary open issues remain in Platform, OS, SDK, TADL or TSIC at the closeout check; TSIC #102 remains the open W5/W6 and production acceptance tracker.

**Disposition:** FCP-01 complete for repository/reference-scope contracts and ecosystem conformance. This does not certify deployed production infrastructure, W5 eight-hour persistence, W6 snapshot/restore, or final product experience.

## 8. FCP-02 execution record — active

FCP-02 begins with W5 because W2–W4 are already accepted for ephemeral CI feasibility. Platform PRs #201 and #202 have merged the durable PostgreSQL workspace-lease implementation and NULL-safe fencing correction. The database layer now provides tenant-scoped leases, forced RLS, append-only lease events, monotonic fencing tokens, and acquire/renew/assert/revoke/release procedures.

**W5 remains open.** The trusted supervisor has not yet been evidenced enforcing the current fencing token at every consequential command boundary and terminating/reaping stale workers. The genuine continuous eight-hour soak has not been run or independently inspected. It must use a dedicated controlled persistent host or registered self-hosted runner; the GitHub-hosted job limit is insufficient. It must cover real browser/profile persistence across process and supervisor restarts, lease renewal/expiry/revocation, stale-worker fencing, quota behavior, audit continuity, crash recovery and cleanup.

**Infrastructure constraint:** existing production instances for FusionOps, ThreatFade and Tinlyt are out of scope and must not be repurposed. No new paid AWS resource is to be created without verified credit coverage and a bounded cost plan. The W5 host must be separately tagged, least-privilege and isolated from existing product infrastructure.

W6 must not begin until W5 acceptance is complete. Production security, economics and independent assurance remain later gates.

## 9. Requirements-to-repository ownership

| Capability | Primary owner | Required conformance |
|---|---|---|
| Execution authority, policy, approvals, runtime, sandbox, secrets, budgets, evidence | Agent Platform | TSIC |
| Agent lifecycle, workspaces, task orchestration, memory orchestration, schedules, delegation | Agent OS | Platform + SDK + TSIC |
| Typed contracts and client behavior | Platform SDK | Platform + OS + TSIC |
| Agent declarations, schemas, skills, authoring and packaging | TADL | Platform + OS + SDK + TSIC |
| System contracts, lock, compatibility, integration and certification | TSIC | All in-scope repositories |

## 10. Competitive acceptance scenarios

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

## 11. Serial execution and release protocol

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

## 12. Definition of final completion

FCP is complete only when all three are true:

- **Infrastructure:** Platform, identity, authorization, sandbox, persistent computers, recovery and production dependencies are implemented and production-qualified.
- **Product:** persistent personal and enterprise agents can use memory, tools, computers, integrations, schedules, teams and proactive workflows through a usable experience.
- **Independent assurance:** cross-repository conformance, security, recovery, economics, operations and release evidence are independently accepted and TSIC publishes final certification.

A green workflow is necessary but insufficient. Final completion is not claimed by this baseline document.


## 6. FCP-00 live reconciliation addendum — 2026-11-08

This addendum supersedes the baseline's point-in-time repository-head and open-work inventory for current programme tracking. The original baseline SHAs above remain historical evidence and are not rewritten.

### Current observed default-branch heads

| Repository | Current `main` SHA | Current head summary |
|---|---|---|
| Agent Platform | `ced3b972087186e4d9d448d5bd2080e8c02bb3cd` | W5 supervisor crash-containment follow-up merged (#207) |
| Agent OS | `aafce0b0d8029e6bac1cf335af24d3da8c6455e0` | Remote endpoint network policy fails closed |
| Platform SDK | `e418f9de6639779381a0cebc746991a52a8df1ce` | PyPI publishing action dependency update |
| TADL / Agent Developer | `409a0bda27ba3db48e696f665bda7d4e6355e4d3` | FCP-02 trusted supervisor baseline pinned (#107) |
| TSIC | `4248f5c048c09284edb03d917b7955c28adff04a` | FCP-01 acceptance recorded; FCP-02 active (#112) |
| TADS (adjacent) | `be242dd29335e3e74b4b80176ea073f7b7f74d56` | Separate intelligence product; not an FCP core repository |

### Current open-work inventory

Repository-scoped GitHub searches observed:
- Agent Platform: 0 open PRs; 0 open issues.
- Agent OS: 0 open PRs; 0 open issues.
- Platform SDK: 0 open PRs; 0 open issues.
- TADL / Agent Developer: 0 open PRs; 0 open issues.
- TSIC: 0 open PRs; 1 open umbrella acceptance issue, [#102](https://github.com/LloydCoder/tinlance-system-integration/issues/102).
- TADS: 2 open dependency PRs (#43 pytest and #44 mypy); TADS is adjacent and is not part of the FCP core implementation sequence.

### W5 supervisor evidence refresh

Platform PR [#207](https://github.com/LloydCoder/tinlance-agent-platform/pull/207) merged to Platform `main` as `ced3b972087186e4d9d448d5bd2080e8c02bb3cd`. It adds Linux parent-death signal containment (`PR_SET_PDEATHSIG=SIGKILL`) and a parent-PID race check, with regression coverage proving that a child command cannot continue its delayed side effect after forced supervisor termination. Exact-head CI (Python 3.12–3.14, SQL, TSIC conformance), CodeQL, Secret Scan, R10, Reference Agents and host-feasibility passed. All six observed post-merge workflows—CI, CodeQL, Secret Scan, R10, Reference Agents and Supply Chain Attestation—passed on the merge SHA.

**W5 remains unaccepted.** The trusted supervisor implementation is now merged, but the continuous eight-hour controlled-host soak remains outstanding. The infrastructure audit found no dedicated Agent Platform soak host; existing FusionOps, ThreatFade and Tinlyt instances remain out of scope. AWS budget configuration is absent and estimated Cost Explorer data does not prove promotional-credit coverage. No compute was provisioned. W6 must remain sequenced after verified W5 soak evidence.

### Current programme disposition

- FCP-00: baseline and live repository reconciliation recorded; continue updating evidence when repository heads or open-work state changes.
- FCP-01: accepted per TSIC #112.
- FCP-02: active; W2–W4 accepted only for ephemeral CI feasibility; W5 implementation slices merged, eight-hour soak outstanding; W6 not started.
- FCP-03–FCP-10: not started under the serial programme sequence.
- TSIC #102 remains open and is the canonical acceptance tracker. Green repository CI does not close the controlled-host soak, production qualification or independent security-review gates.


## 7. FCP-00 post-merge verification refresh — 2026-11-08

This is the latest programme snapshot after Platform PRs #210 and #211 and TSIC PR #113 merged. It supersedes Section 6's observed-main-head table for present-state tracking; Section 6 remains the historical snapshot taken before those merges.

### Verified default-branch heads

| Repository | `main` SHA | Verified head |
|---|---|---|
| Agent Platform | `b130013c702ca70d711153e9824b2d4e955ce2c8` | W5 thread-safe exec-guard implementation and acceptance documentation merged |
| Agent OS | `aafce0b0d8029e6bac1cf335af24d3da8c6455e0` | Remote endpoint network policy fails closed |
| Platform SDK | `e418f9de6639779381a0cebc746991a52a8df1ce` | PyPI publishing action dependency update |
| TADL / Agent Developer | `409a0bda27ba3db48e696f665bda7d4e6355e4d3` | FCP-02 trusted supervisor baseline pinned |
| TSIC | `e8ee021bc06f1032b0ecc29c4828c4bd50a9ecdf` | FCP-00 live reconciliation and W5 evidence record merged |
| TADS (adjacent) | `be242dd29335e3e74b4b80176ea073f7b7f74d56` | Separate intelligence product; excluded from FCP core sequence |

### Post-merge workflow verification

- Platform PR [#210](https://github.com/LloydCoder/tinlance-agent-platform/pull/210), merge SHA `255b4ea75e9d6a8d231fbb60f2c7d3165aea5b6f`: all 14 post-merge check runs passed, including Python 3.12–3.14, quality/coverage, R10, SQL, TSIC conformance, CodeQL, Secret Scan, host feasibility and attestation.
- Platform PR [#211](https://github.com/LloydCoder/tinlance-agent-platform/pull/211), merge SHA `b130013c702ca70d711153e9824b2d4e955ce2c8`: all 14 post-merge check runs passed.
- TSIC PR [#113](https://github.com/LloydCoder/tinlance-system-integration/pull/113), merge SHA `e8ee021bc06f1032b0ecc29c4828c4bd50a9ecdf`: all 34 post-merge check runs passed.

### Core open-work inventory after merges

- Agent Platform, Agent OS, Platform SDK and TADL: no open PRs or issues observed.
- TSIC: no open PRs; issue [#102](https://github.com/LloydCoder/tinlance-system-integration/issues/102) remains open as the single canonical Phase 2 acceptance tracker.
- TADS: two open development-dependency PRs (#43 mypy and #44 pytest); these are outside the Agent Systems FCP boundary and are not prerequisites for FCP progression.

### FCP-00 disposition and FCP-02 gate

**FCP-00 baseline/reconciliation is complete for this snapshot.** The six repository heads, core open-work inventory, merged implementation evidence and post-merge workflow results are recorded above.

FCP-01 remains accepted. FCP-02 remains active and incomplete: W5 has merged durable lease, trusted-supervisor, parent-death containment and thread-safe exec-guard implementation slices, but the required uninterrupted eight-hour controlled-host soak has not been run or independently inspected. The infrastructure audit found no dedicated Agent Platform soak host; the existing FusionOps, ThreatFade and Tinlyt hosts remain out of scope. AWS budget configuration was empty and promotional-credit coverage could not be verified, so no compute was provisioned.

W6 remains gated behind W5 acceptance. FCP-03 through FCP-10 remain unstarted in the serial sequence. Green CI and merged code are necessary but do not replace the controlled-host soak, production qualification, independent security review or formal go/no-go evidence.
