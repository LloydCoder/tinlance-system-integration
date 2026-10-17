# Phase 0 Forensic Baseline — 2026-10-17

## Status

**Audit status: IN PROGRESS — NOT CERTIFIED GREEN.**

This document records an evidence-bounded baseline for the Tinlance Agent System. It is not a production-readiness certificate. No claim is made here that the full live system, external infrastructure, or all cross-repository paths have been exercised.

## Scope

Core repositories:
- `LloydCoder/tinlance-agent-platform` — governed execution and authority plane.
- `LloydCoder/tinlance-agent-os` — orchestration and lifecycle plane.
- `LloydCoder/tinlance-agent-platform-sdk` — typed client contract.
- `LloydCoder/tinlance-agent-developer` — artifact validation and packaging plane.
- `LloydCoder/tinlance-system-integration` — ecosystem integration and conformance authority.

Evidence reviewed on 2026-10-17 included repository README files, TADL's `ecosystem.lock.json`, TSIC's `catalog/phases/registry.json`, GitHub Actions run metadata for default-branch commits, and open pull-request metadata. Evidence is bounded to the records actually retrieved; it is not a full source-code or live-infrastructure audit.

## Architecture invariants

1. Agent Platform is the sole authority for identity, tenancy, authorization, policy, approvals, budgets, governed execution, secrets/tool authority, and authoritative evidence.
2. Agent OS coordinates workspaces, sessions, tasks, workflows, memory and lifecycle; it must not independently grant execution authority.
3. SDK is a typed client surface and must not grant authority.
4. TADL validates/packages agent artifacts and does not become a runtime authorization authority.
5. TSIC defines integration contracts and certifies conformance; it is not a substitute runtime.
6. Protocol adapters (including MCP/A2A) must not bypass the Platform authority boundary.

## Observed evidence

### Default-branch workflow snapshot

The following successful workflow records were returned by GitHub queries. These are dated records, not a claim that every workflow was rerun on 2026-10-17.

| Repository | Commit prefix | Observed successful workflows | Run date |
|---|---|---|---|
| Agent Platform | `c347795f` | CI, R10 Certification, CodeQL, Secret Scan, Reference Agents | 2026-10-09 |
| Agent OS | `8da4acec` | CI, CodeQL; later scheduled CodeQL/Scorecard runs | 2026-10-08 to 2026-10-13 |
| Platform SDK | `615eef52` | CI, Security; later dependency-maintenance workflows | 2026-10-08 to 2026-10-14 |
| TADL | `25fac21a` | Ecosystem Integration, Security, CodeQL, Release Attestations | 2026-10-08 to 2026-10-14 |
| TSIC | `619db9e2` | TSIC-17 Production System-of-Systems E2E, FAS, BugFlow, Acquisition, Observability, Transformation Route certifications | 2026-10-11 to 2026-10-15 |

These results support the existence of repository-level CI and certification automation. They do not independently prove that production dependencies are deployed or that a real end-to-end workflow has been exercised against production infrastructure.

### Ecosystem lock reconciliation

TADL's current `ecosystem.lock.json` records baseline `tsic-19-agent-system-2026-10-08` and pins:
- TADL: `4fac75ba9f14d438d045b877685b2695b4da2c5b`
- Agent OS: `8da4aceca56ff58792b81545f3992c5e4493bda4`
- Agent Platform: `4f524c51f24ace3fa96b5f2fbd716d0270c16aae`
- Platform SDK: `615eef529831fdfbe37e050e45d9a1a8c4472291`
- TSIC integration authority ref: `bdb5b7f9f2295562ad8681c591a8a927500b4d8c`

The observed current default-branch heads differ from the TADL and Platform pins. A pin may intentionally identify a reviewed release baseline; this is not inherently an error. Phase 0 must decide explicitly whether the pinned baseline is still the certified release baseline or whether a new lock is required. No silent substitution of default-branch heads is acceptable.

### Phase ledger

TSIC `catalog/phases/registry.json` currently marks TSIC-00 through TSIC-19 completed and says it was last reconciled on 2026-10-09. The registry's completion rule requires implementation, cross-system execution, security/authority checks, failure/recovery/idempotency, evidence lineage, documentation reconciliation, dedicated CI certification and a post-phase forensic audit.

The ledger is a declaration of status. The retrieved evidence does not establish every one of those requirements for every phase. Reconciliation must attach or link the underlying evidence, and phase statuses must not be treated as a substitute for it.

### Open pull requests

Open PRs observed:
- Agent Platform: #96, #97
- Agent OS: #127, #128, #129
- Platform SDK: #41, #42, #43, #44
- TADL: none returned
- TSIC: #55, #56, #57, #58

These are mostly dependency updates. Review each PR's diff, security impact, required checks, and current head SHA before merging. SDK PR #44 was identified in the audit snapshot as needing a specific Security-workflow review on its PR revision; verify the current check state before making a decision. Do not infer that a PR failure means the default branch is failing.

## Unverified production assertions

The following must remain **unverified** until direct evidence is attached:
- live Platform endpoint health and authentication/authorization behavior;
- real durable persistence and outbox/inbox delivery under restart/failure;
- external secret resolution and secret non-disclosure;
- isolated execution/sandbox behavior and tenant separation;
- live OS → SDK → Platform → tool → evidence workflow;
- production telemetry and end-to-end trace correlation;
- backup restoration and recovery objectives;
- operational alerting, incident ownership and response drills;
- real MCP/A2A access with authorization propagation;
- production capacity, queue bounds, budgets and cost enforcement.

## Phase 0 blockers and required actions

| ID | Required action | Required evidence / exit condition |
|---|---|---|
| P0-01 | Reconcile the TADL ecosystem lock with reviewed source revisions | Explicit release-baseline decision; reviewed lock or documented intentional pin; compatibility checks run against exact SHAs |
| P0-02 | Reconcile TSIC phase statuses with evidence | Each completed phase links implementation, cross-system, security, recovery, evidence-lineage and CI records; unsupported claims are reopened |
| P0-03 | Review open PRs and current required checks | PR inventory with risk, check state, merge decision and resulting SHA; no blind merges |
| P0-04 | Establish a reproducible live integration test environment | Documented deployment topology, version pins, test identities, secrets handling, test-data boundaries and teardown |
| P0-05 | Execute critical end-to-end and adversarial tests | Real user-to-task-to-Platform-governed-tool-to-evidence path; tenant-isolation, denied-action, approval, retry, cancellation and failure-recovery results |
| P0-06 | Reconcile architecture and API contracts | One source of truth for identity, authorization, event envelope, trace context, registries, routing, SDK wire contract and MCP/A2A boundaries |
| P0-07 | Publish auditable evidence bundle | Commit SHAs, workflow run IDs, test results, deployment identifiers, traces, known limitations and reviewer sign-off |

## Phase 0 exit gate

Phase 0 (TSIC-00 / forensic baseline) is **not complete** until all of the following are true:

- [ ] Reviewed commit baseline and ecosystem lock are consistent and enforced by CI.
- [ ] Phase registry claims are reconciled against retrievable implementation, test, and certification evidence; unsupported completion claims are explicitly downgraded or reopened.
- [ ] Open PRs have been reviewed; relevant blockers are fixed or tracked with a justified disposition.
- [ ] Required structural, security, and repository-level CI workflows pass on the exact candidate commit.
- [ ] The deterministic cross-repository reference workflow passes against the exact reviewed SHAs.
- [ ] Production dependency status is explicitly classified as deployed, not deployed, or unverified; reference CI is never described as production proof.
- [ ] The phase 0 audit report and source-of-truth documentation are reconciled and committed.
- [ ] A post-phase audit signs off with no unresolved **Phase 0** critical blocker.

The following are mandatory for the later production-readiness gate (P10), not prerequisites for the structural TSIC-00 baseline itself: live deployed end-to-end execution, production identity and secret services, tenant-isolation attacks against deployed infrastructure, external sandbox verification, disaster-recovery drills, production telemetry, capacity/load tests, and operational incident-response evidence. These remain explicitly **unverified** until evidence is collected. Phase 0 may not mark them complete or imply they have passed.

## Explicit limitations of this baseline

This document is a source-backed triage baseline, not a complete implementation audit. It does not claim that source files, every test, all workflow jobs, external cloud resources, or the live production endpoints were exhaustively inspected. No phase is certified green by this document alone.

## Source records

- [TSIC repository](https://github.com/LloydCoder/tinlance-system-integration)
- [TSIC phase registry](https://github.com/LloydCoder/tinlance-system-integration/blob/main/catalog/phases/registry.json)
- [TADL ecosystem lock](https://github.com/LloydCoder/tinlance-agent-developer/blob/main/ecosystem.lock.json)
- [Agent Platform repository](https://github.com/LloydCoder/tinlance-agent-platform)
- [Agent OS repository](https://github.com/LloydCoder/tinlance-agent-os)
- [Platform SDK repository](https://github.com/LloydCoder/tinlance-agent-platform-sdk)
- [TADL repository](https://github.com/LloydCoder/tinlance-agent-developer)


## Additional code-level findings from Phase 0 review

### Certification workflow revision drift

The current `.github/workflows/agent-system-e2e.yml` checks out these cross-repository revisions:
- TADL: `25fac21a8912bf58f0a9fc65e6ed1cbede70bbee`
- Agent OS: `8da4aceca56ff58792b81545f3992c5e4493bda4`
- Platform SDK: `615eef529831fdfbe37e050e45d9a1a8c4472291`
- Agent Platform: `9125f46f526030fdeced492b6df281c4745f77e9`

These TADL and Platform revisions differ from the TADL ecosystem lock's pinned TADL `4fac75ba...` and Platform `4f524c51...` revisions. The OS and SDK revisions match the observed lock. This creates a material reproducibility ambiguity: a green cross-repository workflow may certify a different combination from the declared ecosystem release lock.

**Required remediation:** make the workflow consume the reviewed canonical lock (or assert its checked-out SHAs against that lock), and fail closed on drift. If a deliberately separate certification baseline is required, give it a separately versioned, reviewed manifest and explain the difference. Do not simply replace pins with branch heads.

### Reference integration is not production integration

The inspected TSIC-01 workflow starts `scripts/agent_system_platform_server.py`, probes a reference Platform endpoint, then runs the vertical slice. It sets deterministic fixture credentials such as `token-tsic` and `tenant-tsic`. This is useful for deterministic CI conformance, but it is a reference/test environment—not evidence that the external production Platform, real identity provider, production secret store, deployed sandbox, or production telemetry are healthy.

The SDK's `tests/test_live_platform.py` is explicitly skipped unless `TINLANCE_PLATFORM_TEST_URL`, `TINLANCE_PLATFORM_TEST_TOKEN`, `TINLANCE_PLATFORM_TEST_TENANT`, and `TINLANCE_PLATFORM_TEST_SUBJECT` are supplied. The current evidence reviewed here does not show that these live-test inputs were present in the relevant CI run.

**Required remediation:** keep deterministic reference tests, and add a separate protected deployment-smoke/integration gate that reports whether a real deployment was tested. Missing live credentials must produce a clearly reported `not_run` / `unverified` status, never an implied production pass. Do not store live credentials in source or logs.

### Phase 0 validator scope

`tooling/validate_phase0.py` checks foundation files, parses JSON, checks duplicate system IDs and authority owners, and checks the presence of selected later-phase artifacts. `scripts/certify_phase0.py` checks registry/graph/lock invariants and the TSIC-00 phase sequence. These are valuable deterministic structural gates. By design, they do not establish external deployment health, actual provider authentication, production data durability, or live cross-tenant denial behavior.

**Required remediation:** preserve these fast structural checks and make the separation between structural conformance, simulated E2E, deployed smoke tests and production-readiness evidence explicit in certification outputs and phase status.

### Phase 0 implementation tasks added to the blocker register

| ID | Severity | Remediation | Acceptance test |
|---|---|---|---|
| P0-08 | Critical | Eliminate untracked cross-repository revision combinations in TSIC E2E | Workflow verifies every checked-out SHA against one reviewed lock/baseline and fails on drift |
| P0-09 | Critical | Separate reference E2E certification from deployed integration certification | CI clearly distinguishes `reference_pass`, `live_pass`, `not_run` and `failed`; no production claim follows from reference pass alone |
| P0-10 | High | Make live Platform test coverage/status visible in certification | Protected live-test workflow records commit, deployment identifier, test outcome and safe evidence; absent configuration is explicitly unverified |
| P0-11 | High | Align certification status semantics with test scope | Phase registry/report states exactly which structural, simulated, deployed and production gates passed |

These findings mean Phase 0 remains open. They should be implemented and tested before a green Phase 0 certification is considered.
