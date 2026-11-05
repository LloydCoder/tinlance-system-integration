# Agent Workforce Parity Remediation Plan

**Status:** Active execution plan — Phase 0 certified green; Phase 1 architecture baseline reviewed and accepted for Phase 2; Phases 2–5 remain gated  
**Owner:** Tinlance Agent System  
**Canonical planning authority:** Tinlance System Integration & Conformance (TSIC)  
**Baseline inspected:** 2026-11-05  
**Primary objective:** establish a reviewable, evidence-led path to Grok Bot and ChatGPT Dots capability parity without weakening Tinlance's execution-authority boundaries.

---

## 1. Executive decision

Tinlance should extend its existing Agent Platform / Agent OS / SDK / TADL architecture. It should not introduce a second execution authority or rebuild the current control plane.

The remediation programme has two gates before production implementation:

1. **TSIC authority and certification reconciliation.** Establish one explicit, reproducible, immutable compatibility baseline across TSIC, Agent Platform, Agent OS, Platform SDK and TADL. Resolve the purpose and overlap of the existing certification workflows and ensure live cross-repository evidence is not confused with contract-only conformance.
2. **Cloud-computer architecture approval.** Define and threat-model a persistent, isolated computer/workspace service, its lifecycle contract, ownership boundaries, provider abstraction, data/secret/network controls and production acceptance criteria. Evaluate isolation technologies before selecting one.

This pull request is deliberately documentation-only. It does not change runtime code, CI workflows, manifests, repository pins, infrastructure, credentials or production deployments.

## 2. Scope and non-goals

### In scope

- TSIC canonical authority, revision pins, adapter contracts and certification workflow reconciliation.
- Cloud-computer architecture for persistent agent workspaces.
- Agent OS / Platform / SDK / TADL ownership and contract boundaries.
- Grok Bot and ChatGPT Dots parity requirements.
- Security, reliability, cost, evidence, testing and operational acceptance gates.
- Ordered remediation phases and explicit exit criteria.

### Not in scope

- Implementing a cloud-computer provider.
- Selecting AWS, another cloud provider, Firecracker, gVisor, Kata Containers or a container-only runtime as the final production choice.
- Changing production code or deploying infrastructure.
- Claiming product parity from schemas, interfaces, unit tests or reference-only E2E fixtures.
- Granting Agent OS, SDK, TADL, a browser worker or a computer provider independent execution authority.

## 3. Repository baseline and evidence

The following immutable main-branch heads were observed during this inspection:

| Repository | Inspected main SHA | Commit date (UTC) |
|---|---|---|
| [tinlance-system-integration](https://github.com/LloydCoder/tinlance-system-integration) | `b8848be64e8cd559ce315a1b521c1d1f9aa16306` | 2026-11-05 |
| [tinlance-agent-platform](https://github.com/LloydCoder/tinlance-agent-platform) | `8a5d8d7ad00a759a96649fb0fb97adc78743788b` | 2026-11-05 |
| [tinlance-agent-os](https://github.com/LloydCoder/tinlance-agent-os) | `eeeaf83cf35e3ba7387ec7838165862132c71204` | 2026-11-05 |
| [tinlance-agent-platform-sdk](https://github.com/LloydCoder/tinlance-agent-platform-sdk) | `e418f9de6639779381a0cebc746991a52a8df1ce` | 2026-11-05 |
| [tinlance-agent-developer (TADL)](https://github.com/LloydCoder/tinlance-agent-developer) | `1e6f11f0d6e4a396028c6a3475425410be2cdd71` | 2026-10-21 |

These are observed branch heads, not a claim that all five revisions have passed a single mutually compatible certification run.

### 3.1 Existing ownership model — preserve it

| Concern | Authoritative owner | Required invariant |
|---|---|---|
| Identity, tenant authority, authorization, policy, approvals, budgets, consequential tool execution, sandbox policy and authoritative evidence | Agent Platform | Sole generic consequential execution authority |
| Organization/project/environment/workspace lifecycle, sessions, tasks, scheduling, orchestration and presentation | Agent OS | Coordinates work; cannot grant authority |
| Typed developer client and transport contracts | Platform SDK | Client surface only; cannot authorize side effects |
| Agent, capability, skill and workflow authoring, packaging and developer validation | TADL | Developer validation is not execution authorization |
| Ecosystem registry, cross-repository contracts, compatibility policy, conformance and certification evidence | TSIC | Certification/control plane only; does not execute domain work |
| Compute provider and isolated host substrate | To be designed | Executes only a Platform-authorized run under an OS-managed workspace lifecycle |

The existing TSIC ADR-0003 already establishes TSIC as the ecosystem conformance authority and TADL as a conformance consumer. This plan operationalizes that decision; it does not replace it.

Evidence:
- TSIC [ADR-0003](https://github.com/LloydCoder/tinlance-system-integration/blob/main/docs/architecture/decision-records/ADR-0003-ecosystem-conformance-authority.md)
- Platform [ADR-001](https://github.com/LloydCoder/tinlance-agent-platform/blob/main/docs/adr/ADR-001-agent-platform-boundaries.md)
- OS [Platform integration contract](https://github.com/LloydCoder/tinlance-agent-os/blob/main/docs/architecture/agent-platform-integration.md)

## 4. TSIC reconciliation workstream — blocking gate

### 4.1 Current evidence and discrepancies to reconcile

The current TSIC main branch contains both:

- `.github/workflows/agent-system-e2e.yml`: a live reference vertical-slice workflow that checks out exact commits, verifies the TADL ecosystem lock, installs the four repositories, runs tests, starts a reference Platform server, executes a governed cross-repository flow and invokes `scripts/forensic_audit_phase1.py`.
- `.github/workflows/agent-system-certification.yml`: a separate workflow that materializes repositories from `policies/agent-system-baseline.json`, runs TADL TSIC conformance and ecosystem/finite-phase conformance. Its current steps do not invoke the live `certify_agent_system_e2e.py` vertical slice.

The distinction may be intentional, but the names and certification reporting must make it unambiguous. A contract-only or repository-conformance pass must never be reported as a live end-to-end execution certification.

The following revision sources coexist and must be reconciled explicitly:

1. TADL `ecosystem.lock.json` pins four repository refs and a TSIC authority ref.
2. TSIC `policies/agent-system-baseline.json` pins a separate TSIC ref and four separate repository refs.
3. TSIC `.github/workflows/agent-system-e2e.yml` checks out a pinned TADL lock-source revision and four separately pinned repository revisions.
4. TSIC `.github/workflows/agent-system-certification.yml` materializes the revisions in the TSIC Agent System baseline.
5. Each repository has its own local TSIC conformance script and integration documentation.

A difference between a branch head and a pinned release is not automatically a defect: an immutable lock may intentionally certify an earlier reviewed release. The defect to prevent is an undocumented, unreviewed or ambiguous compatibility relationship between the lock sources and the certification result.


### 4.1.1 Execution findings recorded on 2026-11-05

- TSIC PR [#88](https://github.com/LloydCoder/tinlance-system-integration/pull/88) merged the ThreatFade Web dependency-security and E2E remediation. Its merge commit is `e6d1c00b8db486720fe2d08ad65337bc6963804b`.
- ThreatFade Web security PR [#99](https://github.com/LloydCoder/tinlance-threatfade-web/pull/99) was merged at `f1c38d8ec87cd1873583af12f7a0d551aa72fe63`; TSIC PR [#93](https://github.com/LloydCoder/tinlance-system-integration/pull/93) then reconciled the immutable TSIC-10 web pin and BugFlow integration baseline. PR #93 merged at `b8848be64e8cd559ce315a1b521c1d1f9aa16306`.
- The post-merge exact-SHA check-run set for `b8848be64e8cd559ce315a1b521c1d1f9aa16306` contains 33/33 completed-success checks. TSIC-10 run `42080733666` passed all engine, web, Playwright, live API, schema/authority and forensic-audit steps; TSIC-28 transformation route run `42080733534` also passed. This supersedes the earlier `a9cdee...` 33/33 observation as the latest inspected TSIC main certification baseline.
- TSIC main subsequently reconciled Agent System certification to the immutable TADL P10 release lock in `a9cdee82a81582fa98da9a4f4f92067540e2a9d0`. Both Agent System workflows now consume the pinned TADL lock source; the contract/finite-phase workflow verifies exact SHA equality and the live reference E2E emits a machine-readable manifest.
- The exact TSIC main revision `a9cdee82a81582fa98da9a4f4f92067540e2a9d0` reported 33/33 check runs successful. TSIC-10 job `42071032720` passed every step, including engine security/detection tests, web format/lint/typecheck/unit tests/dependency audit, production build, Playwright E2E, live engine health/version and schema validation, TSIC authority validation and post-phase forensic audit.
- The 12 cancelled workflow runs in the same recent history were older superseded commits; they are not failures on the certified SHA. The latest exact-SHA check-run set is the certification evidence.
- Current branch heads listed in Section 3 are inspection references only. The P10 lock deliberately pins the reviewed compatibility set and does not silently follow branch heads.
- Phase 0 is closed for the Agent System baseline and TSIC-10 reconciliation scope. This does not claim deployed persistent-computer production readiness or completion of the Agent Workforce parity programme.

### 4.2 Required TSIC deliverables

**TSIC-R1 — Canonical baseline decision**

Publish one canonical Agent System certification baseline record that identifies:

- TSIC contract revision;
- TADL revision;
- Agent OS revision;
- Platform SDK revision;
- Agent Platform revision;
- API and schema versions;
- required integration/adapter revisions;
- test suite and workflow revision;
- baseline creation, review and supersession metadata.

A baseline must be immutable after certification. Updating any component creates a new candidate baseline and requires compatibility review. Do not silently move refs to branch heads.

**TSIC-R2 — Workflow purpose and authority**

Document the distinct purpose of each workflow. Either:
- retain two workflows with explicit names and separate result labels (for example, repository/contract conformance versus live vertical-slice certification); or
- consolidate them into one serial certification pipeline with separately reported gates.

Do not leave duplicate workflows whose names imply equivalent E2E assurance while exercising different scopes.

**TSIC-R3 — Pin consistency checks**

Add a deterministic validator that:
- parses the canonical TSIC baseline;
- parses the TADL ecosystem lock;
- verifies each repository identity and immutable 40-character commit SHA;
- verifies the TSIC authority revision expected by the baseline;
- verifies each workflow checks out the exact refs it claims to certify;
- verifies the adapter and schema revisions used by those commits;
- fails on missing, extra, ambiguous or conflicting authority sources;
- emits a machine-readable certification manifest containing every tested SHA.

Do not require a certified SHA to equal the latest branch head. Require it to equal the explicitly approved baseline.

**TSIC-R4 — Certification evidence semantics**

Separate these states in machine-readable results:
- `static_contract_conformance`;
- `repository_test_conformance`;
- `reference_vertical_slice_passed`;
- `live_deployed_integration_passed`;
- `production_operational_acceptance_passed`.

A reference server backed by in-memory stores is valuable integration evidence, but it is not proof of deployed production persistence, isolation, recovery or service-level objectives.

**TSIC-R5 — Forensic audit correctness**

The current main branch contains both `.github/workflows/agent-system-e2e.yml` and the forensic script's required path, and that workflow invokes the forensic script. Therefore the earlier claim that the current main branch had a stale workflow-path mismatch is not supported by the inspected main-branch contents and must not be carried forward as a confirmed defect.

Before modifying the forensic gate:
- retrieve the exact head SHA and job logs for the historical failed run;
- reproduce the failure against that exact SHA;
- compare its required paths with the tree at that SHA;
- distinguish historical failure from current-main status;
- add a regression test for the actual defect, if one is reproduced.

**TSIC-R6 — Four-repository live vertical slice**

The certification must prove, in one causal trace:
1. TADL validates the agent artifact.
2. OS creates workspace/session/task context.
3. SDK propagates tenant, principal, API version, trace and idempotency context.
4. Platform authenticates and authorizes the principal and tenant.
5. Platform applies policy, budget and approval controls.
6. A governed action executes through Platform.
7. Cancellation and failure behavior are exercised.
8. Events and authoritative evidence are retrieved and correlated to the same run.
9. Retries do not duplicate consequential side effects.
10. A tampered or mismatched tenant, principal, capability, revision or evidence reference fails closed.

The reference vertical slice is necessary but insufficient for production certification.

### 4.3 TSIC exit criteria

TSIC reconciliation is complete only when:
- one canonical, reviewed baseline is identified;
- all four repositories consume the same declared TSIC contract authority;
- every certification workflow has a precise assurance label and scope;
- CI validates all lock and workflow pins;
- the exact tested SHAs are emitted as an artifact;
- the reference vertical slice passes on the exact candidate baseline;
- forensic audit passes against the same revision;
- no local repository claims ecosystem certification solely from its local CI.

## 5. Persistent cloud-computer architecture — design gate

### 5.1 Product requirement

A Tinlance persistent agent computer is a resumable, policy-governed execution workspace that gives an agent controlled access to:
- a filesystem and durable workspace data;
- a shell/terminal and process environment;
- a browser session and browser automation interface;
- approved network destinations;
- explicitly granted application connectors;
- durable checkpoints and recoverable task state.

It must support create, start, resume, suspend, snapshot, restore, rotate credentials, drain and terminate lifecycle operations. A browser tab, remote MCP endpoint or short-lived subprocess alone is not a persistent cloud computer.

### 5.2 Proposed logical architecture

This is a target design for review, not an approved implementation or provider selection.

```text
Personal Agent / Agent Workforce UX
                 |
              Agent OS
  workspace + session + task + schedule
                 |
        Platform SDK (typed client)
                 |
       Agent Platform (authority)
  identity / policy / approval / budget
  run lifecycle / evidence / audit
                 |
      Compute Control Adapter
  provision / attest / lease / drain
  suspend / snapshot / restore / delete
                 |
        Isolated Compute Fabric
  +----------------+------------------+
  | Persistent VM  | Sandboxed worker  |
  | or microVM     | / browser worker  |
  +----------------+------------------+
                 |
     Workspace storage + artifact store
                 |
       Egress proxy / DNS controls
                 |
    Explicitly approved external systems
```

**Authority rule:** the compute fabric is an execution substrate, not an authorization authority. It must accept a scoped, short-lived, Platform-issued execution grant bound to tenant, workspace, agent, run, capability, resource limits, policy version, expiry and idempotency identity. It must not infer authority from a workspace ID, agent profile, MCP message or model-generated instruction.

### 5.3 Ownership boundaries

| Component | Responsibility | Must not do |
|---|---|---|
| Agent OS | Workspace and computer lifecycle intent; session/task association; user-visible status; schedule and resume requests | Authorize tools, approve actions, mint broad credentials or write authoritative evidence |
| Agent Platform | Identity, policy, approval, budgets, execution grants, sandbox policy, secret access policy, run authority, evidence/audit | Become coupled to a specific cloud vendor or UI framework |
| Platform SDK | Typed APIs for lifecycle requests, status, events and evidence references | Hold privileged long-lived host credentials or bypass Platform |
| TADL | Declare computer requirements in a versioned agent/workflow artifact | Select or weaken security policy at runtime |
| TSIC | Canonical contracts, provider compatibility, certification and cross-repository evidence | Provision computers or execute workloads |
| Compute provider adapter | Translate approved lifecycle and execution contracts into provider operations; attest state and return opaque resource references | Decide whether an agent action is authorized |
| Browser worker | Isolated browser process/profile; navigation and interaction under policy; produce traceable artifacts | Reuse browser profiles or credentials across tenants |

### 5.4 Provider and isolation decision

Do not select the isolation technology based on convenience or a single benchmark. Run a documented threat-model and benchmark exercise.

Candidate classes:
- **Hardware-virtualized microVMs (Firecracker-class):** strongest candidate for hostile multi-tenant agent workloads and persistent computer isolation; assess startup latency, snapshot/restore, networking, storage, operations and cost.
- **gVisor:** candidate for a lower-overhead application-kernel sandbox with a different compatibility and syscall profile; assess escape resistance, compatibility and resource isolation.
- **Kata Containers or equivalent VM-backed OCI runtimes:** candidate where OCI/Kubernetes operations and stronger per-workload isolation are required.
- **Hardened containers:** only as a lower-risk tier where threat model, trust assumptions and blast radius justify them; not the default for arbitrary user-supplied code or hostile browser content.

The Platform's existing ADR-007 explicitly requires comparison of container, gVisor, Kata/microVM and remote-sandbox approaches against a threat model before production selection. Preserve that decision gate.

External technical references:
- [gVisor security architecture](https://gvisor.dev/docs/architecture_guide/intro/)
- [gVisor production guide](https://gvisor.dev/docs/user_guide/production/)
- [gVisor security model](https://github.com/google/gvisor/blob/master/g3doc/architecture_guide/security.md)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [CISA and partner guidance on careful adoption of agentic AI services](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/41544ff)

### 5.5 Mandatory security controls

The architecture and implementation must address at minimum:

**Tenant and workload isolation**
- Separate compute identity, process namespace, filesystem, browser profile, network identity and encryption context by tenant/workspace.
- No shared writable browser profile, home directory, cookie jar, SSH agent, credential cache or host mount across tenants.
- No host Docker socket, privileged container, host PID namespace or unrestricted device access inside an agent workspace.
- Explicit CPU, memory, process, disk, I/O, concurrency, wall-clock and egress quotas.
- Defend against noisy-neighbour exhaustion and cross-tenant side channels within the documented threat model.

**Network and browser security**
- Default-deny outbound network with policy-enforced egress proxy.
- DNS rebinding, private/link-local/loopback address, cloud metadata endpoint and IPv6 bypass protections.
- Redirect revalidation, destination allowlists, protocol restrictions and response-size limits.
- Browser download quarantine, MIME/type validation, archive/decompression limits and malware scanning.
- Treat web pages, downloaded files, DOM content, browser prompts and tool output as untrusted input; resist prompt injection and goal hijacking.
- No direct host networking or unrestricted browser-to-private-network access.

**Identity, secrets and approvals**
- Short-lived, audience-bound, least-privilege credentials.
- Secrets delivered just in time and never persisted in workspace snapshots, logs, browser profiles or model context.
- Platform authorization re-evaluated at each consequential action, not only at computer creation.
- Separate read-only, reversible and irreversible action classes.
- Human approval for policy-defined sensitive or irreversible actions.
- Credential rotation and immediate revocation on tenant offboarding, compromise, run cancellation or policy change.

**Persistence, evidence and privacy**
- Encrypt durable volumes and snapshots; bind encryption keys to tenant/workspace policy.
- Snapshot restore must revalidate identity, policy, image provenance, secret expiry and workspace generation.
- Keep authoritative evidence outside the guest-controlled filesystem.
- Record resource identity, image digest, policy version, execution grant, run ID, trace ID, lifecycle transitions and evidence references.
- Redact sensitive payloads; apply retention, deletion and legal-hold policies.
- Prevent snapshots from resurrecting revoked credentials, old approvals or expired authority.

**Supply chain and host security**
- Signed and provenance-verified base images, browser builds and extensions.
- SBOM, vulnerability scanning, image promotion and rollback.
- Hardened host OS, minimal host services, patch SLAs, secure boot/attestation where supported.
- Separate control plane from guest data plane; protect provider credentials and management APIs.
- Incident isolation, forensic preservation and tenant-specific containment procedures.

Threat mapping must include OWASP agentic risks such as goal hijack, tool misuse, identity/privilege abuse, supply-chain compromise, unexpected code execution, memory/context poisoning, insecure inter-agent communication, cascading failures, human-agent trust exploitation and rogue-agent behavior.

### 5.6 Lifecycle and API contract to design

The design review must define versioned, typed contracts for:

- `ComputerProfile`: requested image, resource tier, persistence class, browser capability, network profile, region/data residency and retention class.
- `ComputerInstance`: opaque provider reference, tenant/workspace binding, state, image digest, attestation, resource allocation and generation.
- `ComputerLease`: owner, expiry, renewal policy, concurrency limit and fencing token.
- `ExecutionGrant`: Platform-issued scoped authority, run/capability binding, policy version, resource limits, expiry and revocation state.
- `ComputerOperation`: idempotent lifecycle operation with request ID, idempotency key, expected generation and terminal result.
- `ComputerEvidence`: immutable reference to lifecycle, browser, process, artifact and execution evidence held outside the guest.

Required operations: `provision`, `start`, `resume`, `suspend`, `snapshot`, `restore`, `renew_lease`, `rotate_credentials`, `drain`, `terminate`, `get_status`.

Every mutating operation must be authenticated, authorized, tenant-bound, idempotent, auditable and safe under duplicate delivery. State transitions must be explicit and fenced against stale workers.

### 5.7 Reliability and operational model

Design for:
- host crash and compute loss;
- worker crash during an action;
- duplicate queue delivery;
- lease expiry and split-brain prevention;
- provider API outage and rate limiting;
- snapshot corruption and restore failure;
- storage/network partition;
- credential expiry during a run;
- browser crash and hung downloads;
- regional capacity exhaustion;
- tenant suspension and emergency revocation.

Define RPO/RTO by persistence tier, not as one global promise. A restored computer may resume non-consequential work only after reconciliation; consequential actions require fresh Platform authorization and idempotency checks.

### 5.8 Cost and capacity controls

The architecture review must produce a cost model covering:
- provisioned versus active compute time;
- vCPU, memory and disk allocation;
- persistent volume and snapshot storage;
- browser concurrency;
- egress and artifact transfer;
- image build and registry storage;
- idle suspension and wake-up latency;
- observability and evidence retention;
- regional redundancy and recovery.

Require per-tenant and per-agent budgets, quotas, idle suspension, maximum session duration, concurrency caps and an explicit cost attribution trail. Do not promise always-on unlimited computers without a measured unit-economic model.

## 6. Cross-repository implementation map

Production implementation begins only after TSIC baseline reconciliation and architecture approval.

| Repository | Planned implementation responsibility | Acceptance evidence |
|---|---|---|
| TSIC | Canonical schemas, baseline, provider adapter contract, threat-model requirements, certification profile and compatibility matrix | Lock validator, schema validation, pinned integration certification and machine-readable evidence |
| Agent Platform | Execution grants, policy-bound compute operations, provider trust/attestation, sandbox policy, revocation, budgets, evidence and audit | Negative authorization tests, tenant isolation tests, revocation tests, idempotency/replay tests and recovery evidence |
| Agent OS | Workspace-to-computer lifecycle, leases, state machine, session/task binding, scheduler resume/suspend and user-visible status | Lifecycle contract tests, crash recovery, stale-generation fencing and multi-workspace isolation |
| Platform SDK | Typed lifecycle/status/events/evidence clients, retries and idempotency contracts | API compatibility, serialization, timeout/retry and contract tests |
| TADL | Versioned computer requirements and skill/workflow declarations; validation of requested capabilities and risk class | Schema validation, compatibility tests, policy rejection tests and artifact provenance |
| Provider adapter / infrastructure | Provider-specific provisioning, image pipeline, storage, networking, browser workers and host operations | Infrastructure tests, isolation tests, image provenance, DR tests and production telemetry |

No repository may duplicate Platform authorization or become a second execution authority.

## 7. Competitive parity backlog

The following is the target capability set. Status must be updated only with code, CI, deployment or user-visible product evidence.

| Capability | Existing Tinlance evidence | Remediation |
|---|---|---|
| Persistent agent identity and memory | OS lifecycle and memory modules | Validate deployed durability, retention and cross-tenant isolation |
| Persistent cloud computer | No complete provider/provisioner verified | Design and implement the computer fabric |
| Browser and desktop interaction | No complete general-purpose computer-use runtime verified | Isolated browser worker, controlled interaction API and evidence capture |
| Shell and filesystem | OS local/remote runtime primitives | Bind to isolated persistent computer with quotas and durable storage |
| Multi-agent delegation | OS team/workflow and Platform coordination foundations | Prove parallel live runs, messaging, handoff, failure recovery and shared context without shared authority |
| Scheduled background execution | OS scheduler and event/workflow primitives | Prove deployed workers, durable delivery, misfire handling and end-to-end recovery |
| Connected applications | MCP and connector contracts | Deliver authenticated production connectors with scoped credentials and revocation |
| Demonstration-to-skill learning | TADL constrained learning proposal/evaluation primitives | Record user-approved demonstrations, synthesize versioned skills, evaluate and require approval before publication |
| Proactive research and monitoring | Scheduling, TWI integration and evidence foundations | Persistent objectives, source verification, monitor lifecycle and alert delivery |
| Personal agent experience | OS and developer surfaces | Product UX, onboarding, preferences, permissions, timeline and user controls |
| Enterprise workforce management | Workspace fabric and Platform governance | Tenant administration, policies, quotas, audit views and deployment operations |

Parity claims must be capability-specific. A feature is not “complete” until it is available through the intended product surface, works end-to-end and passes the relevant security and operational gates.

## 8. Ordered programme and phase gates

### Phase 0 — Baseline and TSIC authority reconciliation

**Status: COMPLETE.** Latest inspected TSIC main baseline `b8848be64e8cd559ce315a1b521c1d1f9aa16306` has 33/33 completed-success check runs.

**Evidence:** exact-SHA check-run set 33/33 success; TSIC-10 run `42080733666` and TSIC-28 run `42080733534` completed successfully; PR #93 merged as `b8848be64e8cd559ce315a1b521c1d1f9aa16306`; PR #99's reviewed ThreatFade Web security release is pinned by TSIC; Phase 1 architecture PR #92 merged as `b221315db23f7612a93255599be3afe802a36a66` and its 33 workflow runs completed successfully. Earlier `a9cdee...` evidence remains historical, not the latest baseline.

**Deliverables**
- Canonical immutable Agent System baseline.
- Workflow purpose/assurance taxonomy.
- Lock and pin consistency validator.
- Corrected historical failure analysis.
- Certification evidence manifest.
- Cross-repository contract and adapter revision map.

**Exit gate**
- All baseline refs and workflow checkouts reconcile.
- CI emits tested SHA manifest.
- Reference E2E and forensic gates pass on the exact baseline.
- No ambiguous or conflicting conformance authority.

### Phase 1 — Cloud-computer architecture approval

**Status: COMPLETE — architecture and trust-boundary baseline reviewed and accepted.** The ADR, 20-scenario threat model, trust-boundary diagram, provider benchmark plan and proposal-only lifecycle schemas are reviewed in PR #92. This closes architecture approval only; it does not claim that a provider-backed computer runtime has been implemented or deployed.

**Deliverables**
- Architecture decision record.
- Threat model and trust-boundary diagram.
- Isolation technology comparison and benchmark plan.
- Lifecycle/API contract proposal.
- Data classification, retention and snapshot policy.
- Network/egress and secret-delivery design.
- Cost model and capacity assumptions.
- Failure model, SLO proposal and production acceptance matrix.

**Exit gate**
- Platform, OS, SDK, TADL and TSIC ownership reviewed.
- Security review covers OWASP agentic risks and tenant escape paths.
- No unresolved authority-boundary violation.
- Architecture direction and tiering approved; final provider/isolation selection is made only after Phase 2 comparative measurements.

### Phase 2 — Provider and isolation feasibility spike

**Deliverables**
- Non-production prototype in an explicitly approved isolated environment.
- Comparative measurements for startup, suspend/resume, snapshot/restore, browser compatibility, isolation, density and cost.
- Adversarial test report.
- Operational runbook and failure injection results.

**Exit gate**
- No production customer data or credentials.
- No production deployment.
- Security and cost acceptance signed off.
- Architecture decision updated with measured results.

### Phase 3 — Governed computer lifecycle MVP

**Deliverables**
- Versioned TSIC contracts.
- Platform execution grants and policy integration.
- OS lifecycle and lease state machine.
- SDK typed client.
- TADL computer profile declaration.
- One provider adapter.
- Isolated filesystem, shell and browser execution.
- External evidence and audit references.

**Exit gate**
- Full cross-repository E2E on immutable SHAs.
- Tenant isolation, authorization, revocation and replay tests pass.
- Crash recovery and snapshot restore pass.
- No secrets or authoritative evidence exposed to guest workspace.

### Phase 4 — Workforce, learning and proactive operation

**Deliverables**
- Parallel agents and delegated task ownership.
- Durable agent messaging and coordination.
- Demonstration capture and skill synthesis.
- Scheduled skill execution.
- Connected application catalog.
- Proactive research and monitoring.
- User approvals and activity timeline.

**Exit gate**
- End-to-end workflows pass with fault injection.
- Skills are versioned, evaluated and permission-bounded.
- Cross-agent trust and cascading failure tests pass.
- User can inspect and revoke ongoing work.

### Phase 5 — Product and production certification

**Deliverables**
- Personal Agent and Agent Workforce experiences.
- Enterprise administration and governance.
- Production deployment, SLOs, support and incident processes.
- Security assessment and penetration test.
- Capacity, load, cost and DR evidence.
- TSIC production certification.

**Exit gate**
- Production infrastructure is independently evidenced.
- Security, reliability, privacy and economic controls pass.
- User-visible parity scenarios pass on the released product.
- Certification reports exact tested artifacts and deployed versions.

## 8.1 Phase 1 architecture package (2026-11-05)

The Phase 1 design package is authored in this branch:
- `docs/architecture/decision-records/ADR-0004-persistent-agent-computer.md` — authority model, isolation tiers, persistence/snapshot semantics, lifecycle, control/data plane and acceptance gates.
- `docs/architecture/persistent-agent-computer-threat-model.md` — assets, trust boundaries, 20 threat scenarios, fail-closed abuse cases and Phase 2 security tests.
- `docs/architecture/persistent-agent-computer-benchmark-plan.md` — comparable Firecracker/gVisor/Kata benchmark, adversarial gates, measurement plan and decision rubric.
- `contracts/proposals/computer/v1/computer-lifecycle.schema.json` — proposal-only typed lifecycle/profile/grant/instance/evidence shapes; explicitly not yet canonical.

Forensic distinction: Platform currently has a bubblewrap-based local sandbox adapter, not a persistent cloud-computer service. OS has workspace-fabric and remote-runtime primitives, not a provider-backed VM lifecycle. Platform P6 explicitly leaves deployment-owned database, queue, object storage, KMS, isolated workers, telemetry and DR to a real deployment. The new architecture does not mislabel these primitives as cloud-computer implementation.


## 9. Required test and evidence matrix

| Test domain | Required scenarios |
|---|---|
| Identity and tenancy | Cross-tenant access, workspace reassignment, stale credentials, tenant suspension |
| Authorization | Unapproved action, revoked grant, privilege escalation, stale policy version |
| Isolation | Filesystem escape, process escape, host socket access, metadata endpoint access, cross-workspace access |
| Network | DNS rebinding, redirect to private IP, IPv6 bypass, proxy bypass, exfiltration |
| Browser | Prompt injection, malicious extension, download abuse, cookie leakage, cross-profile reuse |
| Secrets | Snapshot leakage, log leakage, environment leakage, expiry, revocation and rotation |
| Lifecycle | Duplicate provision, concurrent resume, stale lease, terminate during run, restore after revocation |
| Reliability | Host crash, queue redelivery, storage outage, regional failure, corrupted snapshot |
| Multi-agent | Forged peer identity, unauthorized delegation, poisoned shared context, cascading retries |
| Evidence | Missing evidence, forged reference, broken trace lineage, guest tampering, retention/deletion |
| Economics | Quota exhaustion, idle leak, runaway browser, noisy neighbor, budget enforcement |
| Supply chain | Unsigned image, compromised extension, vulnerable base image, provenance mismatch |

Every test result must record:
- test ID and requirement ID;
- repository and immutable commit SHA;
- environment and provider configuration;
- policy and image digest;
- tenant/workspace/run identity (synthetic test identities only);
- trace and evidence references;
- result, logs and artifact checksums;
- reviewer and timestamp.

## 10. Security and design review checklist

Before Phase 1 approval, reviewers must answer:

- Is the Platform still the sole consequential execution authority?
- Are compute lifecycle and execution grants distinct?
- Can a guest forge or replay a grant?
- Can an agent access another tenant's filesystem, browser profile, secrets or network?
- Can browser content or a tool result influence privileged control-plane behavior?
- Can a snapshot resurrect credentials, approvals or revoked authority?
- Are egress and cloud metadata protections enforced outside the guest?
- Are provider credentials isolated from agent processes?
- Can the control plane revoke a running computer and prove termination?
- Is evidence retained outside guest control?
- Are retries and recovery safe for irreversible actions?
- Are cost limits enforced before and during execution?
- Can the service be operated, patched, monitored and recovered without relying on a user's local machine?

A “no” or “unknown” on a critical question blocks production acceptance.

## 11. Decision requests for reviewers

Reviewers are asked to approve or amend these decisions:

1. TSIC remains the sole ecosystem conformance and certification authority.
2. Agent Platform remains the sole generic consequential execution authority.
3. Agent OS owns workspace/computer lifecycle intent and orchestration, not authorization.
4. A persistent computer is a governed execution substrate, not an autonomous authority.
5. Isolation technology remains undecided until threat-model and benchmark evidence is reviewed.
6. TSIC reconciliation and architecture approval are mandatory gates before production implementation.
7. This plan is documentation-only; no production code or infrastructure change is included.

## 12. Source inventory

### Canonical Tinlance sources inspected

- TSIC [README](https://github.com/LloydCoder/tinlance-system-integration/blob/main/README.md)
- TSIC [ADR-0003: Ecosystem Conformance Authority](https://github.com/LloydCoder/tinlance-system-integration/blob/main/docs/architecture/decision-records/ADR-0003-ecosystem-conformance-authority.md)
- TSIC [Agent System baseline](https://github.com/LloydCoder/tinlance-system-integration/blob/main/policies/agent-system-baseline.json)
- TSIC [Agent System E2E workflow](https://github.com/LloydCoder/tinlance-system-integration/blob/main/.github/workflows/agent-system-e2e.yml)
- TSIC [Agent System certification workflow](https://github.com/LloydCoder/tinlance-system-integration/blob/main/.github/workflows/agent-system-certification.yml)
- TSIC [Phase 1 requirements](https://github.com/LloydCoder/tinlance-system-integration/blob/main/conformance/requirements/phase1.json)
- TSIC [Agent System E2E certifier](https://github.com/LloydCoder/tinlance-system-integration/blob/main/scripts/certify_agent_system_e2e.py)
- TSIC [Phase 1 forensic audit](https://github.com/LloydCoder/tinlance-system-integration/blob/main/scripts/forensic_audit_phase1.py)
- TADL [ecosystem lock](https://github.com/LloydCoder/tinlance-agent-developer/blob/main/ecosystem.lock.json)
- TADL [TSIC conformance validator](https://github.com/LloydCoder/tinlance-agent-developer/blob/main/scripts/tsic_conformance.py)
- Platform [ADR-002: Runtime architecture](https://github.com/LloydCoder/tinlance-agent-platform/blob/main/docs/adr/ADR-002-runtime-architecture.md)
- Platform [ADR-007: Sandbox boundary](https://github.com/LloydCoder/tinlance-agent-platform/blob/main/docs/adr/ADR-007-sandbox.md)
- Platform [ADR-012: Deployment](https://github.com/LloydCoder/tinlance-agent-platform/blob/main/docs/adr/ADR-012-deployment.md)
- Platform [P6 Production Runtime Contract](https://github.com/LloydCoder/tinlance-agent-platform/blob/main/docs/production-runtime/P6-PRODUCTION-RUNTIME-CONTRACT.md)
- OS [remote runtime](https://github.com/LloydCoder/tinlance-agent-os/blob/main/src/tinlance_agent_os/remote_runtime.py)
- OS [workspace fabric](https://github.com/LloydCoder/tinlance-agent-os/blob/main/src/tinlance_agent_os/workspace_fabric.py)
- OS [Platform integration contract](https://github.com/LloydCoder/tinlance-agent-os/blob/main/docs/architecture/agent-platform-integration.md)

### External security and isolation references

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [gVisor security architecture](https://gvisor.dev/docs/architecture_guide/intro/)
- [gVisor production guide](https://gvisor.dev/docs/user_guide/production/)
- [CISA and partner guidance on careful adoption of agentic AI services](https://content.govdelivery.com/accounts/USDHSCISA/bulletins/41544ff)

---

**Review rule:** approve this plan before implementation begins. Any production implementation PR must reference the accepted plan, the approved TSIC baseline and the applicable phase acceptance criteria.
