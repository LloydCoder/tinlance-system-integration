# Tinlance Agent Systems — Final Completion Programme

**Programme ID:** FCP  
**Version:** 1.0  
**Baseline:** 2026-11-08  
**Programme authority:** TSIC (system-of-systems programme governance and conformance evidence)  
**Execution authority:** Tinlance Agent Platform  
**Status (reconciled 2026-11-09):** FCP-00 and FCP-01 accepted; FCP-02 repository/controlled-host W5 and W6 implementation acceptance recorded with production enablement residuals retained; FCP-03 is active and incomplete. FCP-04–FCP-10 remain gated. Overall programme completion and production certification remain outstanding.

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


## 8. FCP-02 W5/W6 acceptance and FCP-03 infrastructure audit — 2026-11-09

This addendum supersedes earlier W5/W6 statements in Sections 5, 8 and the prior live reconciliation snapshots. Earlier sections remain historical records of what was known at their timestamps.

### W5 — accepted for controlled-host functional soak

The isolated Tinlyt test host `tinlyt-test-runtime` (EC2 `i-0bdb9c7cb13b1c9b8`, `t4g.medium`, `eu-west-1`) completed the continuous eight-hour soak against Platform commit `fe2f31837b67fcb5332591e31289fe2f0f23f3bb`.

- 28,800.03 seconds continuous elapsed; 96/96 browser/profile cycles.
- Chromium 156.0.8078.4; maximum adjacent cycle gap 304.82 seconds.
- 96 successful quota settlements; lease-event audit count 52→149 and quota ledger 14→206.
- Lease expiry and revocation invalidated fence 1; replacement ownership advanced to fence 2.
- Nine supervisor-death probes; every child started and no child produced a post-crash side effect.
- cgroup-v2 memory.max 2 GiB, pids.max 128; memory peak 356,220,928 bytes; final pids.current 1.
- Cleanup verified; no residual Chromium, worker or Bubblewrap processes.
- Artifact: `/opt/tinlance-w5/artifacts/w5-soak.json`; SHA-256 `798579f881ec884594753bd65a519dffb4bf1f0927a6db2836688f66c3a342e7`.

**Qualification:** Chromium's internal sandbox was disabled in this harness. Outer Bubblewrap user/PID/mount/network namespaces, dropped capabilities and the no-guest-network boundary were active. W5 is accepted for controlled-host functional soak only; it does not establish renderer-seccomp assurance or production certification.

### W6 — accepted for repository implementation scope

- Platform PR #223 merged as `9344315a9c867157f10bcfeb29369b86497f7f27`.
- Platform PR #222 merged as `1bd86c24f0dd35baa8d5536d5c6f0197fe6ccf15`; recorded mainline gates passed: CI, CodeQL, Secret Scan, Supply Chain Attestation, Reference Agents and R10 Certification.
- Platform documentation PR #224 merged as `ced90d12bc8cd7a2a61110399e56d4e7e2297d62`.
- Implementation includes tenant/workspace-bound authenticated manifests, path/type/mode/size validation, credential exclusions, KMS envelope-encryption and separate HMAC-signing adapters, immutable conditional S3/SSE-KMS adapter, tenant-scoped PostgreSQL catalog and restore ledger, forced RLS, append-only events, one-shot restore claims, newer-fence restore, private staging/atomic publication and credential-reference refresh.
- Validation recorded: 15 migrations and 13 PostgreSQL 17 SQL acceptance tests; focused snapshot/KMS/S3/catalog/ledger tests; a real PostgreSQL-backed clean-host restore drill under a newer fence; credential-reference refresh; successful completion; and revoke-before-publication failure with no destination and durable failure event.

**Production enablement remains open:** production KMS encryption/HMAC keys, S3 bucket policy/versioning/Object Lock/retention, workload identity/IAM, durable lifecycle reconciliation, monitoring, replication and cross-AZ/region disaster-recovery drills have not been provisioned or qualified.

### FCP-03 — production security and infrastructure qualification is now the active phase

A read-only AWS inventory and network-policy inspection was performed on 2026-11-09. It found:

1. The isolated W5 host remains running in `eu-west-1`, tagged as test-only. Its security group has no ingress but permits all outbound protocols to `0.0.0.0/0`; its subnet uses the default network ACL and a default route to an Internet Gateway. This is not an independent destination-level egress enforcement point.
2. The W5 host's attached KMS key is the AWS-managed default EBS encryption key, not a dedicated snapshot encryption or HMAC-signing key.
3. No S3 buckets were returned by the account-level bucket inventory. No production snapshot object store was identified.
4. AWS Budgets returned zero configured budgets. This is a cost-governance gap; it does not prove promotional-credit coverage.
5. Tinlyt API production's security group has no ingress but permits all outbound protocols to `0.0.0.0/0`.
6. The ThreatFade instance's security group currently allows inbound TCP/22, TCP/80 and TCP/443 from `0.0.0.0/0`. This is an adjacent product security finding, not an Agent Platform authorization to modify ThreatFade. It must be triaged separately by its owner.
7. FusionOps, ThreatFade and Tinlyt production hosts were not modified. The test host was not modified during this read-only audit.

The current Platform repository already contains a DNS-resolving HTTPS CONNECT proxy and W4 namespace/firewall test harness. The documented residual remains: W4's network layer permits public unicast TCP/443, while hostname allowlisting is enforced by the proxy process; DNS query names are not independently allowlisted. A compromised proxy process therefore lacks an independent destination-level hostname enforcement boundary. Production FCP-03 must close this with a trusted enforcement point and explicit DNS policy, not merely rely on application proxy validation.

### FCP-03 work sequence and gates

1. Establish a production deployment architecture and threat model for destination-bound egress, DNS policy, workload identity, cgroups, encrypted profile storage, snapshot KMS/S3, audit, monitoring and operational ownership.
2. Implement a trusted destination-level egress enforcement design that is independent of the browser proxy process; add explicit DNS query-name policy and adversarial tests for DNS rebinding, mixed answers, alternate resolvers, DNS tunnelling, IPv6, NAT64, metadata and proxy compromise.
3. Define and test least-privilege production KMS encryption/HMAC keys, S3 bucket policy/versioning/retention/Object Lock, workload identity and PostgreSQL grants as infrastructure code. Do not provision production resources until the cost ceiling, credit coverage and rollback plan are verifiable.
4. Qualify provider-attested host SKU, firmware, microcode, SMT and CPU mitigation state; implement production cgroup limits and encrypted persistent profile storage.
5. Integrate live identity/revocation, telemetry/SLOs, alerting, incident response, restore reconciliation, backup and cross-AZ/region recovery drills.
6. Obtain independent security review and accountable residual-risk acceptance. ADR-0004 go/no-go must be evidence-based.

**FCP-03 is active, not accepted.** No production resources were created or changed by this audit. Existing production product instances remain out of scope for experiments.

### Current core repository open-work inventory — 2026-11-09

GitHub repository-scoped searches observed no open PRs in Agent Platform, Agent OS, Platform SDK, TADL or TSIC. No open issues were observed in Agent Platform, Agent OS, Platform SDK or TADL. TSIC issue #102 remains the single open umbrella acceptance tracker. This is a point-in-time inventory and must be refreshed before final certification.

### Programme disposition

- FCP-00: baseline/reconciliation accepted; this addendum records the W5/W6 evidence and current infrastructure snapshot.
- FCP-01: accepted for repository/reference-scope contracts and ecosystem conformance.
- FCP-02: W5 controlled-host functional soak and W6 repository implementation accepted; production enablement, security/economics residuals and final Phase 2 certification remain open.
- FCP-03: active; production security and infrastructure qualification.
- FCP-04–FCP-10: remain sequenced and unstarted until preceding gates are accepted.

A green workflow or merged implementation is necessary but insufficient for production qualification or final completion.


## 9. FCP-03 egress architecture forensic correction — 2026-11-09

This addendum records the post-ADR-018 AWS documentation review and supersedes the egress-policy implementation details in Section 8 where more precise AWS service prerequisites are now known.

### Platform documentation correction

- Platform PR [#229](https://github.com/LloydCoder/tinlance-agent-platform/pull/229) merged as `a3290f237961507a64d2d565636c96a2bfc00cf5`.
- PR head `fd5e563ea2e9e5cb66fa3f65af1a690cdc5f9c37`: all 14 check runs passed, including Python 3.12–3.14, quality/coverage, SQL, TSIC conformance, R10 adversarial certification, CodeQL and TruffleHog.
- Post-merge mainline on `a3290f237961507a64d2d565636c96a2bfc00cf5`: all 14 check runs passed, including Supply Chain Attestation. The five observed post-merge workflows (CI, Secret Scan, Reference Agents, R10 Certification and CodeQL) also succeeded.
- Platform `main` is now `a3290f237961507a64d2d565636c96a2bfc00cf5`.

### Additional AWS resolved-IP validation requirements

The original ADR-018 described `AWS_ROUTE_53_RESOLVED_DOMAIN` rule matching but omitted mandatory deployment prerequisites and important scope semantics. The merged correction now requires:

1. Network Firewall policy-level `Route53ResolvedIPValidation` with the exact `DNSFirewallRuleGroupId`; rule-level resolved-domain rules are inactive without it and can surface `ROUTE53_RESOLVED_IP_VALIDATION_MISSING`.
2. The referenced Route 53 Resolver DNS Firewall rule group must be associated with the worker VPCs, and worker DNS must use the VPC Resolver. The rule group must be dedicated to one firewall/policy-isolation domain: all associated VPCs contribute to a shared resolved-IP pool, so an address resolved in one associated VPC can be treated as resolved for the others.
3. Resolved-IP cache is Availability-Zone scoped. Worker traffic must reach its same-AZ firewall endpoint. Unsupported AZ flows must be observed using `DnsAzUnavailableFlows`; resolved-domain rules can drop in unsupported AZs even when policy-level validation is in alert mode.
4. Start policy-level validation in `ALERT` mode for approximately 24 hours, monitor `route53_resolved_ip`, `DnsUnresolvedFlows`, `DnsResolutionErrorFlows` and `DnsAzUnavailableFlows`, then promote to `DROP` or explicitly approved `REJECT`. DNS expiry behavior must not silently continue in the enforced profile.
5. Explicitly scope `SourceIPRanges`; an empty list disables policy-level source validation. Enabling/disabling resolved-IP validation or changing the DNS Firewall rule-group ID may restart the stateful engine, so connection-drain/stream-exception behavior is part of rollout acceptance.

These details are based on current AWS Network Firewall and Route 53 Resolver documentation:
- https://docs.aws.amazon.com/network-firewall/latest/developerguide/route53-resolved-ip-validation.html
- https://docs.aws.amazon.com/network-firewall/latest/developerguide/route53-resolved-ip-validation-policy-setting.html
- https://docs.aws.amazon.com/network-firewall/latest/developerguide/route53-resolved-ip-validation-how-it-works.html
- https://docs.aws.amazon.com/network-firewall/latest/developerguide/route53-resolved-ip-validation-troubleshooting.html
- https://docs.aws.amazon.com/network-firewall/latest/developerguide/route53-resolved-ip-validation-recommendations.html

### Cost-gate verification

Read-only Billing/Cost Explorer checks found zero configured AWS Budgets. Cost Explorer showed approximately `-$14.4186 USD` of credit-type records applied during 2026-11-01 to 2026-11-10; this is not a remaining-credit balance, proof of eligible service coverage, or evidence of credit expiry. The remaining-credit balance must be verified from the AWS Billing Credits page. The AWS Price List API returned EU (Ireland) base meters of $0.395 per Network Firewall endpoint-hour, $0.065/GB processing, $0.489 per advanced-inspection endpoint-hour, and $0.16 per DNS Firewall Advanced association-hour, before ancillary costs.

**Provisioning gate remains BLOCKED.** No disposable VPC, Network Firewall, NAT Gateway, DNS Firewall association, KMS key, S3 bucket or other paid resource was created. Verified remaining eligible credit, expiry, a hard spend ceiling, budget alarms and automated teardown are still required before the disposable VPC experiment. No production resource or adjacent FusionOps, ThreatFade or Tinlyt service was modified.

### Current disposition

- FCP-00 and FCP-01 remain accepted.
- FCP-02 W5 controlled-host functional soak and W6 repository implementation remain accepted within their stated scope; production qualification remains open.
- FCP-03 remains active and blocked at the paid disposable-network-test gate pending verified credit coverage and cost controls. ADR-018 is an architecture decision, not deployment evidence.
- FCP-04–FCP-10 remain strictly sequenced behind prior phase acceptance.


## 10. FCP-03 live governance and preflight hardening refresh — 2026-11-09

This addendum records the latest read-only AWS governance check and merged repository fixes. It supersedes prior point-in-time open-work and governance summaries where they conflict. No AWS resources or account settings were changed.

### Merged Agent Platform hardening

- PR [#247](https://github.com/LloydCoder/tinlance-agent-platform/pull/247) merged as `40ae96b452529aceec1aec1968652ae828dd1b0d`. It rejects malformed and repeated AWS pagination continuation tokens in the read-only inventory collector. Exact PR head `40990922bcd1c1c990825fd727c5802c2d0f4cc5` passed all 14 reported checks; all six post-merge push workflows succeeded.
- PR [#248](https://github.com/LloydCoder/tinlance-agent-platform/pull/248) merged as `cf40caf4177ac75d9d24e7030677f054d88cfb6a`. It requires the exact worker security-group egress tuple set: TCP/443 plus UDP/53 and TCP/53 to the VPC resolver; additional, missing, duplicate, noncanonical and malformed entries fail closed. Exact PR head `732a151b839d9ab6125a0ca5d31b2bfa3ca4fce7` and post-merge SHA each passed 14/14 checks.
- TSIC PR [#116](https://github.com/LloydCoder/tinlance-system-integration/pull/116) merged as `42c4e31b3d024dbbd05c16abf0922b40845c73f6`; its post-merge mainline passed 34/34 checks. It reconciles FCP phase status and acceptance boundaries.

### New test-first finding — PR #249

The worker route evaluator rejected routes whose targets bypassed the firewall, but accepted extra or duplicate route entries when their target was `local` or the expected firewall endpoint. A route inventory must match the complete intended route set, not merely have individually permitted targets.

- Added regression tests for an extra local-target route and duplicate default route.
- The first test-only CI run reproduced both failures: 2 failed, 925 passed.
- Implementation now requires exactly the VPC primary CIDR local route plus the default IPv4 route to the same-AZ firewall endpoint, rejects duplicate entries and fails closed on extra/missing routes.
- The inventory fixture was corrected to include the VPC local route returned by AWS.
- The first implementation CI run exposed this fixture mismatch and then a Ruff formatting issue; both were corrected before final validation.
- Agent Platform PR [#249](https://github.com/LloydCoder/tinlance-agent-platform/pull/249) merged as `4e9148c08891df7b9bf684e038e6741a70a7aba1`.
- Final PR head `c9df400634608978c38d59ce3b3b3d0aac533a21`: all 14/14 checks passed, including Python 3.12–3.14, quality/coverage, SQL, TSIC conformance, R10 adversarial certification, CodeQL and TruffleHog.
- Post-merge mainline validation on `4e9148c08891df7b9bf684e038e6741a70a7aba1` has been queued and remains pending at the time of this documentation update. Do not count the post-merge gate as green until all checks complete successfully.

### Read-only AWS governance recheck

Account `381661387870`, region-specific reads as applicable, 2026-11-09:

- STS caller identity returned the root principal ARN `arn:aws:iam::381661387870:root`. Root access is not an acceptable long-term deployment identity.
- `budgets:DescribeBudgets` returned zero budgets; `DescribeBudgetActionsForAccount` returned zero actions.
- Billing, Operations and Security alternate contacts each returned `ResourceNotFoundException`; none is configured.
- The existing `tinlyt-test-runtime` instance `i-0bdb9c7cb13b1c9b8` remains running in eu-west-1a as a t4g.medium with public IP, the existing Tinlyt SSM profile, IMDS endpoint enabled (IMDSv2 required, hop limit 1), no ingress and unrestricted IPv4 egress.
- This instance remains a Tinlyt test/controller host and is not an isolated untrusted worker. Do not alter its networking or repurpose it for the disposable worker lab. Existing FusionOps, ThreatFade and Tinlyt infrastructure remains out of scope for FCP experiments.

### Current blockers and safe disposition

1. Establish a least-privilege deployment identity and remove routine dependence on root.
2. Configure and verify a hard spend ceiling, budget alerts/actions and accountable billing/operations/security contacts.
3. Verify the remaining eligible promotional-credit balance, expiry and service coverage in the Billing console; Cost Explorer credit application records are not a remaining-credit balance.
4. Only then authorize a bounded disposable VPC/firewall experiment with explicit teardown and rollback. Do not create Network Firewall, NAT Gateway, DNS Firewall, KMS, S3 or other billable resources before these controls are evidenced.
5. Preserve the current test controller and production product infrastructure unchanged.
6. Continue live packet/flow and DNS bypass tests only in the isolated disposable worker trust zone. Static inventory/preflight tests are not live enforcement proof.

**FCP-03 remains active and blocked at the governance/provisioning gate.** The merged #247/#248 code improves read-only inventory and static policy validation; it does not prove deployed AWS packet/flow enforcement, workload identity, production storage, host qualification, operations, economics or independent security acceptance.

### Updated phase disposition

- FCP-00: accepted.
- FCP-01: accepted for repository/reference-scope conformance.
- FCP-02: W5 controlled-host functional soak and W6 repository implementation accepted within their documented scope; production enablement and security residuals remain.
- FCP-03: active; governance and cost gate blocked; live enforcement and production qualification outstanding.
- FCP-04–FCP-10: gated; do not begin before FCP-03 formal acceptance.

A green CI run is necessary but cannot substitute for live deployed evidence or independent acceptance.


## 11. FCP-03 worker route-table isolation hardening — 2026-11-09

### Exact worker route inventory — merged and post-merge green

Agent Platform PR [#249](https://github.com/LloydCoder/tinlance-agent-platform/pull/249) merged as `4e9148c08891df7b9bf684e038e6741a70a7aba1`.

- The test-only PR head `5da0a8c6ab73541eca4410005a223e826b7eac71` reproduced two failures (2 failed, 925 passed): an extra route with target `local` and a duplicate default route were accepted.
- The implementation now requires the exact worker route set: one VPC-primary-CIDR local route and one IPv4 default route to the same-AZ firewall endpoint. Extra, missing and duplicate routes fail closed.
- Final PR head `c9df400634608978c38d59ce3b3b3d0aac533a21`: 14/14 checks passed.
- Exact merge SHA `4e9148c08891df7b9bf684e038e6741a70a7aba1`: 14/14 post-merge checks passed.

### Dedicated worker route-table association — merged and post-merge green

Agent Platform PR [#250](https://github.com/LloydCoder/tinlance-agent-platform/pull/250) merged as `5376812ef111060fbfa42d021c961bfa28e2ea40`.

- Test-only head `392bd93c6a86898a7ad13c384678e781629ae890` reproduced two failures (2 failed, 927 passed): a shared route table and a missing/implicit main-table association were accepted.
- The read-only AWS inventory now records all explicit subnet associations for the worker route table.
- The evaluator requires the route table to be explicitly associated with exactly the worker subnet. Shared route tables and implicit main route tables fail closed.
- A collector regression test proves that a second subnet association is surfaced and rejected.
- Final PR head `9adfb58f4f6793548070c49016ca9513ae693147`: 14/14 checks passed.
- Exact merge SHA `5376812ef111060fbfa42d021c961bfa28e2ea40`: 14/14 post-merge checks passed.

Both changes are read-only inventory/preflight logic and regression tests. They do not change AWS networking, create resources, or prove live packet/flow enforcement. The route-table contract is deliberately scoped to the disposable worker subnet and does not authorize changes to existing Tinlyt, FusionOps or ThreatFade infrastructure.

### Updated FCP-03 disposition

- Repository-level worker egress preflight now checks exact security-group egress, exact worker route inventory and a dedicated worker route-table association.
- These static checks reduce inventory ambiguity and prevent known unsafe topology snapshots from passing.
- The live AWS provisioning gate remains blocked by root-principal access, absent AWS Budgets/actions, missing Billing/Operations/Security alternate contacts and unverified eligible credit balance/expiry.
- Live Network Firewall/Route 53 DNS Firewall deployment, packet/flow bypass tests, production identity, KMS/S3, host qualification, operations, economics and independent security acceptance remain outstanding.

**FCP-03 remains active and incomplete.** FCP-04–FCP-10 remain gated. No live cloud infrastructure was modified.

## 12. FCP-03 duplicate-route and ingress-inventory preflight review — merged 2026-11-09

Agent Platform PR [#253](https://github.com/LloydCoder/tinlance-agent-platform/pull/253) was merged as `923eaede4fbb57b2fa02355c638d522256ee2465`.

- Final PR head: `05c0e3fbe8e3b8c3a8d9afa663d9d479000f6268`.
- The change rejects duplicate entries in firewall-subnet and NAT-return route inventories, requiring the exact expected route set with no duplicate route pairs.
- The AWS inventory now captures worker security-group ingress across IPv4 CIDRs, IPv6 CIDRs, prefix-list references and security-group references. Preflight fails closed when ingress inventory is absent/malformed or when any ingress rule exists.
- Regression tests cover duplicate firewall/NAT route entries, non-empty worker ingress, and missing/malformed ingress inventory.
- The disposable egress-lab README now documents the ingress inventory requirement and the separately configured zero-threshold account budget.
- Exact PR-head checks: 27/27 completed successfully. The required CI, CodeQL, Secret Scan, R10 Certification and Reference Agents workflows all concluded successfully.
- Exact post-merge Agent Platform mainline checks: 14/14 completed successfully.
- Earlier head `774f54c6bf35da1839d25d9007a9e1e4d98e085e` had aggregate workflow failures and incomplete job visibility. The final head was re-run through the complete workflow set; all required checks passed before merge.
- No AWS resources or account settings were changed by PR #253 itself. The separate zero-threshold cost alert is documented below.

**Acceptance boundary:** this is merged static inventory/preflight hardening. It does not prove deployed AWS packet/flow enforcement, DNS Firewall behavior, bypass resistance, cross-tenant isolation, production identity, host/storage qualification, operational readiness, economics or independent security acceptance. FCP-03 remains active and incomplete; FCP-04–FCP-10 remain gated.

### Canonical documentation reconciliation

TSIC documentation PR [#119](https://github.com/LloydCoder/tinlance-system-integration/pull/119) was merged as `81bcb0851b32538647d6214182446b723b549caf`. Its exact PR-head workflows and post-merge mainline check-runs each completed 34/34 successfully.

### Zero-spend budget configuration — 2026-11-09

- AWS Budgets monitoring and notifications are free of charge according to the [official AWS Budgets pricing page](https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/). No action-enabled budget was created.
- A monthly cost budget, `Tinlance-Strict-Zero-Spend`, was created and verified through `DescribeBudgets`, `DescribeNotificationsForBudget` and `DescribeSubscribersForNotification`.
- AWS rejected a literal USD 0.00 `BudgetLimit` (`budget limit must be larger than 0`). The smallest accepted configured limit was USD 0.01. Both actual and forecast notifications use an absolute USD 0.00 threshold (`GREATER_THAN`), with credits and discounts excluded so promotional credits do not mask gross usage.
- Subscriber address is `hello@tinlance.com`. Read-after-write verification reports both actual and forecast notifications in `ALARM` state because gross costs/forecast exceed the zero threshold. Latest `DescribeBudgets` reports gross actual spend of USD 15.005 and gross forecast of USD 29.746 (credits and discounts excluded). Cost Explorer for 2026-11-01 through 2026-11-10 (estimated) groups approximately USD 15.004548 of usage and USD -15.004548 of credits, leaving net cost approximately USD -0.00000004. Latest `GetCredits` reports an initial USD 100.00 promotion, remainingAmount USD 28.32 and conservative estimatedAmount USD 13.32; credit application is after discounts. The gross forecast and estimated credit balance are not a hard guarantee that future charges remain covered. AWS documentation says newly added email subscribers must verify the address before receiving notifications; confirmation is not visible in the available API response and remains unverified.
- No budget actions, SNS topics, AWS compute, networking, KMS, S3 or other billable resources were created. This budget does not enforce a hard spending ceiling and does not authorize any AWS spend.

**Disposition unchanged:** FCP-03 remains active and incomplete. The zero-spend alert is a governance improvement only; it does not resolve root-principal access, missing alternate contacts, unverified email delivery, live packet/flow evidence or production qualification.


## 13. FCP-03 incomplete security-group ingress inventory correction — merged 2026-11-09

Agent Platform PR [#254](https://github.com/LloydCoder/tinlance-agent-platform/pull/254) was merged as `8a9e872cdb3ccee935baf9d7095154b2bb4f4141`.

- Final PR head: `acabffae5f07230f6bdeb78cec5ea6c367aadcb2`.
- Test-first evidence on head `6217ac26576d671f20e0e08f08c5bd92374a417b`: 2 expected failures and 937 passes. The missing-`IpPermissions` test proved that incomplete AWS inventory had been silently treated as an empty ingress list; the malformed-string test exposed an unhandled `AttributeError`.
- The collector now returns an invalid/incomplete inventory result for missing or malformed security-group permissions, malformed nested source collections, and permission records with no recognizable source. The preflight therefore fails closed rather than treating unknown ingress as no ingress.
- Regression coverage verifies IPv6 CIDRs, prefix-list references, security-group references, missing permissions and malformed permissions. The fixture now models a valid no-ingress security group with explicit `IpPermissions: []`.
- Exact PR-head check-runs: 27/27 completed successfully. Required CI, CodeQL, Secret Scan, R10 Certification and Reference Agents workflows all passed.
- Exact post-merge Agent Platform mainline checks: 14/14 completed successfully.
- No AWS resources or account settings were modified by PR #254.

**Account governance confirmation (read-only, 2026-11-09):** the connected AWS caller remains the account root principal; no dedicated least-privilege FCP-03 deployment identity is established. Existing Tinlyt-specific identities are not reused or modified. AWS Account Management `GetAlternateContact` access is denied because trusted access is not enabled, so Billing/Operations/Security alternate contacts could not be verified. The required accountable contact details are not present in the project record; no contact values were invented or written.

**Live AWS inventory confirmation (read-only, 2026-11-09):** `DescribeRegions` returned 17 enabled regions. Across all 17, `ListFirewalls` returned zero AWS Network Firewall deployments and `ListFirewallRuleGroupAssociations` returned zero Route 53 Resolver DNS Firewall associations. No disposable egress lab is deployed. **Acceptance boundary:** this is merged fail-closed inventory hardening. It does not prove live packet/flow enforcement, DNS Firewall behavior, bypass resistance, cross-tenant isolation or production qualification. FCP-03 remains active and incomplete; FCP-04–FCP-10 remain gated.


## 14. FCP-03 incomplete security-group egress inventory correction — merged 2026-11-09

Agent Platform PR [#257](https://github.com/LloydCoder/tinlance-agent-platform/pull/257) was merged as `ebda5c520875bef7fc5dd5c8a9ca9e9444b40ed2`.

- Final PR head: `ca6f975faf63fb35c51390d8ec0e47523b99f2f0`.
- Forensic review found that the egress collector normalized each attached security group independently but silently skipped a group when its `IpPermissionsEgress` collection was absent. If another attached group happened to supply the expected rules, the combined snapshot could look complete while omitting a potentially permissive group.
- The collector now validates every attached group and every permission/source collection. Missing or malformed groups, permissions, nested CIDR/reference collections, and permissions with no recognized source return an incomplete inventory (`None`); the existing preflight rejects that snapshot. A valid explicit empty permission list remains distinguishable from missing inventory.
- A regression test models two attached groups: one has the expected rules and the other lacks `IpPermissionsEgress`. The complete snapshot is rejected instead of silently accepting the partial inventory.
- Exact PR-head workflows: CI, Reference Agents, R10 Certification, CodeQL and Secret Scan all completed successfully (5/5). CI passed Python 3.12, 3.13 and 3.14 quality/coverage, SQL isolation and TSIC conformance.
- Exact post-merge Agent Platform mainline check-runs: 14/14 completed successfully on merge SHA `ebda5c520875bef7fc5dd5c8a9ca9e9444b40ed2`.
- No AWS resource, account setting, network route, security group or existing Tinlyt/FusionOps/ThreatFade infrastructure was modified.

**Cost and acceptance boundary:** the governing constraint is USD 0 in new AWS charges; continue using existing infrastructure only and do not provision new billable AWS resources. The current read-only inventory records zero Network Firewall deployments and zero Route 53 Resolver DNS Firewall associations. Therefore the disposable AWS packet/flow lab cannot be truthfully marked deployed or accepted under the present infrastructure inventory. Static preflight and IaC checks remain useful but do not substitute for live packet/flow evidence. FCP-03 remains active and incomplete; FCP-04–FCP-10 remain gated.


## 15. FCP-03 verified-identity control-character validation — merged 2026-11-09

Agent Platform PR [#262](https://github.com/LloydCoder/tinlance-agent-platform/pull/262) was merged as `a76330c2662b315c357c1b5ebeb9c5a220709c11`.

- Final PR head: `f1e070ed43d246c960ba20e30441aa1ac25bc457`.
- Forensic review found that the shared `VerifiedAgentIdentity` contract checked trimming and non-empty identity values but did not reject embedded C0 control characters or DEL. The JWT verifier already rejected these in several claims, but tenant IDs, roles, scopes and nonces could cross the shared contract boundary with NUL characters; other identity adapters could also construct the contract directly.
- The shared contract now rejects C0 controls, spaces and DEL in subject, tenant, token ID, principal type, client ID, scopes, roles and nonce. This keeps the rule provider-neutral and prevents identity data from crossing into tenant authorization, persistence, audit and telemetry in malformed form.
- Regression tests use actual NUL characters in tenant, role, scope, nonce and client claims and assert rejection.
- Exact PR-head workflows: CI, Reference Agents, R10 Certification, CodeQL and Secret Scan all completed successfully (5/5). CI passed Python 3.12, 3.13 and 3.14 quality/coverage, SQL isolation and TSIC conformance.
- Exact post-merge Agent Platform mainline check-runs: 14/14 completed successfully on merge SHA `a76330c2662b315c357c1b5ebeb9c5a220709c11`.
- No AWS resources, account settings or existing product infrastructure were modified.

**Acceptance boundary:** this is shared identity-contract hardening, not live production identity acceptance. Production issuer/JWKS trust, workload identity, KMS/HSM key custody, rotation/revocation operations, dedicated least-privilege AWS identity and operational evidence remain production gates. FCP-03 remains active and incomplete; FCP-04–FCP-10 remain gated.


## 16. FCP-03 read-only IAM identity separation inventory — 2026-11-09

A fresh read-only IAM inventory was performed after PR #262. The AWS API calls completed successfully for STS caller identity, OIDC provider inventory, all eight IAM roles, the OIDC provider details, and attached/inline policies for every Tinlance/Tinlyt/Agent/Platform-matching role.

- The active AWS API caller is the account root principal; the connector does not currently operate through a dedicated FCP-03 role.
- Exactly one IAM OIDC provider is present: `token.actions.githubusercontent.com`. Its tags identify it as Tinlyt-owned and scoped to the Tinlyt web-intelligence repository.
- The matching roles found are `TinlytFusionOpsSSMRole`, `TinlytGitHubActionsDeployRole`, `TinlytRuntimeSSMRole` and `TinlytTestRuntimeSSMRole`. No FCP-03 or Agent Platform deployment/auditor role was found.
- `TinlytGitHubActionsDeployRole` is restricted to Tinlyt release tags and has no attached or inline resource permissions. The SSM roles are EC2 service-trusted and carry `AmazonSSMManagedInstanceCore`; they are not FCP-03 identities.
- The existing Tinlyt OIDC provider and roles were not reused, modified or expanded. No IAM resource was created or changed during this inventory.

**Disposition:** FCP-03 still lacks an independent workload/deployment identity. Creating a dedicated identity must preserve the Tinlyt boundary and use a separately approved trust design; do not broaden the Tinlyt trust policy, reuse its release role, or fall back to root credentials. IAM identity setup itself is not the same as live proof-of-possession, production key custody, or live AWS egress acceptance. FCP-03 remains active; FCP-04–FCP-10 remain gated.


## 17. FCP-03 malformed inventory collection fail-closed hardening — 2026-11-09

### Agent Platform PR #263
- [PR #263](https://github.com/LloydCoder/tinlance-agent-platform/pull/263) merged as `906ae5df82c149a09a2cc70798819a5c80b6c832`.
- Forensic review found that the topology preflight's string-collection helper silently filtered malformed members. For example, an inventory list containing a valid subnet ID plus a non-string value could be reduced to the valid subset and incorrectly accepted.
- The helper now rejects the entire collection when any member is non-string or empty; it no longer turns incomplete/malformed source data into an apparently valid allowlist, route-table association, source-range set, target-type set, or status set.
- Repeated completion statuses remain supported because AWS legitimately reports one COMPLETE status per associated rule/domain-list resource; duplicate strings are not treated as malformed.
- Five regression cases cover malformed worker/firewall subnet associations, stateful target types, DNS allowlist domains, and Route 53 resolved-IP source ranges.
- Exact PR-head checks: 14/14 successful. Exact post-merge mainline checks: 14/14 successful.
- Full quality matrix includes Python 3.12, 3.13 and 3.14; Ruff, formatting, mypy, full pytest and 85% coverage gate, pip-audit, CycloneDX SBOM, SQL isolation, TSIC conformance, R10 adversarial certification, CodeQL, secret scan and attestation.
- Full platform test suite: 950 passed, 36 warnings; coverage threshold met.

**Disposition:** This closes a static inventory parser fail-open. It does not establish live AWS packet/flow enforcement or create a dedicated production identity. The live network inventory remains without Network Firewall deployments or Route 53 Resolver DNS Firewall associations; account caller remains root and no FCP-03-specific role exists. FCP-03 remains active/incomplete; FCP-04–FCP-10 remain gated.


## 18. FCP-03 AWS collector normalization fail-closed hardening — 2026-11-09

### Agent Platform PR #264
- [PR #264](https://github.com/LloydCoder/tinlance-agent-platform/pull/264) merged as `ee866ba15c7e783f5cda0717059beafd461f2c4b`.
- Forensic review found that the read-only AWS collector silently discarded malformed records before the topology preflight could validate them. A valid security record mixed with an invalid record could therefore be normalized into an apparently valid policy.
- Fixed Route 53 resolved-IP validation range normalization: malformed or incomplete address-definition members are represented as invalid inventory, not silently omitted.
- Fixed Network Firewall stateful domain targets and target types: mixed malformed collections are preserved as invalid so the preflight rejects them.
- Fixed Route 53 Resolver DNS firewall collection: malformed associations, statuses, rules, domain-list metadata and domain values are no longer silently filtered; invalid data reaches the preflight as an invalid collection.
- Fixed worker, firewall and NAT route-table association normalization so malformed association members cannot disappear from the dedicated-route-table check.
- Fixed worker NACL normalization: malformed entries or unknown ingress/egress direction invalidate both rule inventories instead of being skipped.
- Fixed VPC CIDR association normalization and worker security-group ID inventory so malformed extra records invalidate the corresponding security evidence.
- Five adversarial regression tests cover malformed Route 53 validation ranges, stateful target types, DNS domain-list entries, route-table associations and NACL entries.
- Exact PR-head workflows: 14/14 successful. Exact post-merge mainline workflows: 14/14 successful.
- Full platform suite: 955 passed, 36 warnings; coverage gate passed. Python 3.12/3.13/3.14, Ruff, formatting, mypy, pip-audit, CycloneDX SBOM, SQL isolation, TSIC conformance, R10 adversarial certification, CodeQL, secret scan and attestation all green.

**Disposition:** This hardens the read-only collector and normalized inventory path; it does not provision or verify production enforcement. FCP-03 remains active/incomplete because live AWS Network Firewall/DNS Firewall enforcement, a dedicated least-privilege identity, production host isolation/attestation, durable production services/DR, operational acceptance and independent security review remain outstanding. FCP-04–FCP-10 remain gated.


## 19. FCP-03 Network ACL inventory fail-closed hardening — merged 2026-11-09

### Agent Platform PR #265
- [PR #265](https://github.com/LloydCoder/tinlance-agent-platform/pull/265) merged as `78ec89166bfc6c93983cd92276307cd053900cd1`.
- Forensic review found that the read-only NACL collector skipped non-mapping records while searching a subnet-scoped DescribeNetworkAcls response. If one valid matching ACL appeared alongside a malformed record, the malformed record could be silently ignored and the valid ACL accepted.
- The collector now fails closed on any malformed ACL record, missing/non-list association inventory, or malformed association member in the subnet-scoped response. It does not select a valid-looking ACL from an incomplete result set.
- A missing `Entries` property is now treated as incomplete inventory, not normalized to an empty list. A present empty list remains a real empty ruleset and is rejected by the topology policy because it does not match the required NACL rules.
- Regression tests cover a malformed ACL record alongside a valid matching ACL and a missing `Entries` property.
- Exact PR-head checks: 14/14 successful (Python 3.12/3.13/3.14, quality/coverage, SQL isolation, TSIC conformance, R10 adversarial certification, CodeQL, secret scan and attestation).
- Exact post-merge Agent Platform mainline check-runs: 14/14 successful on merge SHA `78ec89166bfc6c93983cd92276307cd053900cd1`.
- No AWS resources, account settings, or existing Tinlyt/FusionOps/ThreatFade infrastructure were modified.

**Disposition:** This closes a static NACL inventory fail-open only. It does not provide live Network Firewall/DNS Firewall packet and flow enforcement evidence. The current read-only account inventory still shows no Network Firewall deployment or Route 53 Resolver DNS Firewall association; the AWS API caller remains root and no dedicated FCP-03 identity exists. FCP-03 remains active/incomplete; FCP-04–FCP-10 remain gated.


## 20. FCP-03 ENI/firewall-mapping inventory hardening and existing-infrastructure census — 2026-11-09

### Agent Platform PR #266
- [PR #266](https://github.com/LloydCoder/tinlance-agent-platform/pull/266) merged as `e1a7644249e7ec94fb6799ba223813ebead5d1f0`.
- The collector previously filtered malformed IPv6 address members from ENI responses. A malformed address could disappear from the snapshot and be mistaken for an empty IPv6 inventory. The collector now preserves incomplete ENI/IPv6 data as an explicit fail-closed signal.
- The collector previously filtered malformed Network Firewall subnet-mapping records while resolving a fallback subnet from the remaining mappings. It now refuses to resolve the firewall subnet from an incomplete mapping collection.
- Regression tests cover malformed IPv6 address data and a malformed firewall subnet mapping alongside a valid mapping.
- Exact PR-head workflows: 14/14 successful. Exact post-merge Agent Platform mainline check-runs: 14/14 successful on merge SHA `e1a7644249e7ec94fb6799ba223813ebead5d1f0`.
- No AWS resources or existing product infrastructure were modified.

### Read-only existing-infrastructure census
A fresh read-only EC2/VPC inventory covered all 17 enabled regions. All API calls succeeded; no infrastructure was created or modified.

- Four EC2 instances are running in total: three in `eu-north-1` (FusionOps production, ThreatFade, and Tinlyt API production) and one in `eu-west-1` (Tinlyt test runtime).
- Every running instance is associated with an existing product/service. There is no identified spare or isolated FCP-03 worker host.
- Zero NAT Gateways and zero VPC endpoints were returned in all 17 enabled regions.
- The separate all-region Network Firewall and Route 53 Resolver DNS Firewall inventory still shows zero firewall deployments and zero DNS Firewall associations.
- The existing Tinlyt test runtime is product test infrastructure, not a dedicated FCP-03 worker; the controller/product instances must not be repurposed or modified for this lab.

**Cost and isolation disposition:** The user's constraint remains USD 0 in new AWS charges and use of existing infrastructure only. The current account has no spare isolated compute, NAT gateway, VPC endpoint, Network Firewall or DNS Firewall deployment from which to build and validate the required production egress chain. Repurposing the four running product instances would violate the product-isolation boundary. Provisioning the missing network/compute resources would violate the no-new-AWS-charge constraint. Consequently, live AWS packet/flow enforcement remains blocked; static CI and collector hardening do not substitute for production packet-level evidence.

FCP-03 remains active/incomplete. FCP-04–FCP-10 remain gated.


## 21. FCP-03 exact worker security-group egress allowlist regression — merged 2026-11-09

### Agent Platform PR #267
- [PR #267](https://github.com/LloydCoder/tinlance-agent-platform/pull/267) merged as `921eabfa8372b99c92c0a794d25e9f2d92758d81`.
- Added an exact CloudFormation regression requiring the worker security group to have no ingress and exactly three egress rules: inspected TCP/443 to the firewall-routed path, and UDP/TCP DNS only to the VPC resolver.
- Exact equality prevents later additions of UDP/443 (QUIC), TCP/853 (DoT), external DNS, IPv6, prefix-list or security-group-reference egress rules from being silently accepted by the template test suite.
- Exact PR-head workflows: 14/14 successful. Exact post-merge Agent Platform mainline check-runs: 14/14 successful on merge SHA `921eabfa8372b99c92c0a794d25e9f2d92758d81`.
- Test-only change; no AWS resources, account settings or product infrastructure were modified.

**Disposition:** This strengthens the static infrastructure-as-code regression boundary. It does not prove live AWS packet/flow enforcement, DNS bypass resistance or production identity. FCP-03 remains active/incomplete; FCP-04–FCP-10 remain gated.
