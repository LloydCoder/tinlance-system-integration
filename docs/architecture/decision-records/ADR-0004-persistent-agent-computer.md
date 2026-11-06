# ADR-0004 — Persistent agent computer architecture

**Status:** Accepted architecture direction; provider and isolation implementation remain gated by Phase 2 evidence  
**Date:** 2026-11-05  
**Owners:** Agent Platform (authority), Agent OS (lifecycle), TSIC (contract and certification)  
**Supersedes:** No existing ADR. This record operationalizes Platform ADR-007 without selecting a production provider.

## Context

Tinlance needs a resumable computer for agent work: durable workspace files, terminal/process execution, browser sessions, approved network access, checkpoints and lifecycle operations. Existing repository primitives are useful but do not constitute a persistent, multi-tenant cloud-computer service:

- Platform's current sandbox package constructs a Linux bubblewrap command and enforces command/path/network/timeout policy. It is a local sandbox adapter, not a remote persistent VM service or a production hostile-tenant isolation proof.
- Agent OS owns workspace, remote endpoint and process coordination primitives. Those are lifecycle/orchestration capabilities, not authorization or host isolation.
- Platform P6 explicitly separates repository semantics from deployment-owned database, queue, object storage, KMS, sandbox workers, telemetry and DR evidence.
- Platform ADR-007 already requires comparative threat-model-based evaluation of containers, gVisor, Kata/microVM and remote sandboxes.

The architecture must preserve the existing authority model and avoid treating a computer provider as a second execution authority.

## Decision

Adopt a **Platform-governed, OS-orchestrated, provider-neutral persistent-computer architecture** with separate control-plane and guest data-plane responsibilities.

1. **Agent Platform is the sole authority.** It authenticates the caller, evaluates tenant and subject policy, capability, approval, budget and risk, issues/revokes narrowly scoped execution grants, and owns consequential run state, authoritative evidence and audit.
2. **Agent OS owns lifecycle intent.** It binds a computer to an organization/project/environment/workspace/session/task, requests lifecycle transitions, manages leases and presents state. OS identifiers and lifecycle state never confer execution authority.
3. **Platform SDK exposes typed clients only.** It carries API version, principal/tenant context, trace context, request identity and idempotency keys. It does not mint or widen grants.
4. **TADL declares requirements.** A validated, versioned computer profile may request capabilities and resource classes but cannot select a weaker runtime policy or grant access.
5. **TSIC owns canonical contracts and certification.** Provider adapters and local repositories consume TSIC contracts; TSIC does not provision or execute computers.
6. **Provider adapters are untrusted execution substrates.** They accept only Platform-authorized, short-lived, audience-bound grants and return signed/verified lifecycle and attestation evidence. They cannot approve actions, create broad credentials or write authoritative evidence.
7. **Guest workloads are treated as hostile.** Browser content, downloads, model output, tool output, user code and restored guest state are untrusted.

### Workload isolation tiers

| Tier | Workload | Candidate isolation | Policy |
|---|---|---|---|
| T0 | Trusted control-plane services | Dedicated service/process boundary | Never co-locate with agent guest workloads |
| T1 | Short-lived, restricted, low-risk deterministic tasks | Hardened container or gVisor; bubblewrap only for local/developer execution | Default-deny network, no privileged mounts, no cross-tenant reuse |
| T2 | Untrusted code, arbitrary browser automation, persistent multi-tenant computer | Per-instance hardware-virtualized microVM (Firecracker-class) is the preferred Phase 2 candidate | Dedicated guest kernel and disk identity; strict host jail, egress mediation, quotas and attestation |
| T3 | Kubernetes/OCI-centric environments where operational integration dominates | Kata Containers with a supported hypervisor | Must meet the same tenant, grant, egress, evidence and recovery gates |

This is a tiered architecture decision, **not** a claim that one technology is already selected or production-certified. Phase 2 must benchmark Firecracker-class microVMs, gVisor and Kata under the same workload and adversarial test plan. A hardened container alone is not an acceptable default for hostile, persistent, multi-tenant computers.

### Persistence model

Separate durable user data from resumable execution state:

- **Workspace volume:** encrypted, tenant/workspace-bound durable filesystem and user artifacts; the system of record for files.
- **Guest image:** immutable, signed, digest-pinned base image promoted through a controlled pipeline.
- **Memory/VM snapshot:** optional acceleration/checkpoint artifact, never the sole durable workspace record and never assumed portable across arbitrary host CPU/kernel configurations.
- **Control-plane state:** Platform/OS records for grants, leases, generation, run, policy, approvals and evidence remain outside the guest.
- **Secrets:** fetched just-in-time from an external secret service; never written to snapshots, images, workspace volumes, logs or model context.

A restored computer starts in a quarantined/reconciliation state. Before user code or consequential work resumes, the control plane must validate image and snapshot provenance, tenant/workspace generation, policy version, lease/fencing token, grant revocation, secret expiry, approval validity and outstanding operation/idempotency state. All consequential actions require fresh Platform authorization.

### Snapshot safety rules

Snapshotting is an optimization with security and compatibility constraints, not a generic clone primitive:

- Snapshot files and attached disks are encrypted, tenant-bound, integrity-checked and access-controlled outside the guest.
- A snapshot is restored into one active successor by default. Concurrent or repeated resume from the same state is prohibited unless a separately reviewed uniqueness protocol proves safe re-keying and deduplication.
- VMGenID reseeding is not sufficient to refresh application-level cached IDs, random tokens, credentials, approvals or idempotency state.
- Re-establish network and vsock sessions after restore; do not assume live connections survive.
- Reconfigure telemetry and logging after restore.
- Pin compatible Firecracker binary, snapshot format, CPU model/features, guest kernel, device layout and host compatibility profile.
- Never restore a snapshot into a different tenant or workspace identity.
- Revoke old grants and rotate guest-facing credentials before unquarantining the successor.

### Control/data plane

- Control plane: Platform API, OS lifecycle service, durable lease/state store, provider adapter, policy decision, approval service, secret broker, evidence/audit and telemetry.
- Guest data plane: isolated microVM or sandbox, workspace volume, browser, terminal/processes and bounded virtual network.
- Host management: provider credentials, hypervisor API sockets, host filesystems, KVM, tap devices, image signing keys and metadata services. None are exposed directly to guest processes.
- Network egress: host-enforced, default-deny proxy with DNS and destination validation at connect time and after redirects; block loopback, link-local, private, metadata, control-plane and management networks unless a narrowly scoped explicit policy permits a route.
- Management API: local Unix socket with strict owner/mode and per-instance isolation; never expose the hypervisor management socket to a guest or public network.

## Lifecycle contract

The proposed lifecycle is:

`requested → provisioning → ready → leased → running → suspending → suspended → restoring → reconciling → ready`

Terminal or exceptional states: `failed`, `draining`, `terminating`, `terminated`, `quarantined`.

Every mutation carries tenant/workspace identity, request ID, idempotency key, expected generation and caller context. State transitions use compare-and-swap/fencing so stale workers cannot overwrite a newer generation. Duplicate delivery returns the original operation result; it must not create a second instance or repeat a consequential action.

Required operations: `provision`, `start`, `resume`, `suspend`, `snapshot`, `restore`, `renew_lease`, `rotate_credentials`, `drain`, `terminate`, `get_status`.

The proposal schemas in `contracts/proposals/computer/v1/` are design artifacts, not yet canonical public API contracts. Phase 3 promotes them only after Phase 2 evidence and TSIC contract review.

## Security and operational requirements

- Tenant isolation across compute identity, guest kernel, filesystem, browser profile, network identity, storage encryption and evidence.
- No host Docker socket, host PID namespace, privileged container, host device passthrough or broad host mounts in guest.
- CPU, memory, process, disk, I/O, bandwidth, concurrency, wall-clock and cost quotas enforced outside the guest.
- Platform authorization re-evaluated at every consequential operation; grants bind tenant, subject, agent, workspace, run, capability, policy revision, resource envelope, audience, expiry, nonce and idempotency identity.
- Human approval for configured sensitive or irreversible operations; revocation must stop active work and invalidate outstanding grants.
- Signed images, SBOM, provenance, vulnerability gates, controlled promotion and rollback.
- External authoritative evidence with trace/run lineage; guest output cannot forge or overwrite it.
- RPO/RTO and availability targets are persistence-tier-specific and are not promised until measured.
- Production acceptance requires incident response, patch SLAs, host attestation where supported, backup/restore, DR, cost attribution and security assessment.

## Capacity and cost model

Phase 1 defines the accounting model, not provider prices. Monthly cost per tenant/workspace must include: allocated vCPU-hours and memory-hours; host reserve/idle capacity; encrypted workspace volume GiB-month; snapshot bytes and retention; image registry/build storage; egress and artifact transfer; browser concurrency; telemetry/evidence retention; KMS/secret operations; backup/DR and on-call operations. Report both active-hour and idle-hour unit cost. Charge attribution must bind tenant, workspace, profile, instance, run and provider usage record.

Capacity planning must use allocatable host resources after reserving headroom for host OS, hypervisor, control plane and failure recovery. Density is determined by the most constrained resource and measured noisy-neighbour behavior, not CPU count alone. Enforce per-tenant concurrency, resource and spend ceilings before provisioning and continuously during execution. Idle suspension thresholds and minimum warm capacity are benchmark outputs, not assumptions.

## Reliability objectives to baseline

Define SLOs separately for control-plane API availability, provision-to-ready latency, resume latency, lease renewal, cancellation/revocation latency, evidence durability, snapshot success, restore success and termination/deletion verification. Define RPO/RTO separately for ephemeral, workspace-durable and checkpointed persistence classes. Numeric commitments are deliberately deferred until Phase 2 measurements, cost modelling and operational ownership are available.

## Consequences

**Positive:** preserves authority separation, supports provider portability, makes persistence/recovery explicit and provides a security tier for hostile workloads.

**Trade-offs:** microVM operations require KVM-capable hosts, a hardened host fleet, image lifecycle, network/storage orchestration and specialized operations. Snapshots are hardware/software sensitive and require careful single-successor semantics. gVisor can be operationally simpler but has a distinct syscall compatibility and performance profile; it does not replace host cgroup/network controls.

**Not decided here:** cloud provider, region, instance family, Kubernetes adoption, final isolation runtime, production SLOs, pricing or deployment. These require Phase 2 measurements and separately approved infrastructure.

## Acceptance gates

- Phase 1: threat model, lifecycle contracts, trust boundaries, data/secret/snapshot policy, provider comparison and benchmark plan reviewed.
- Phase 2: non-production measurements and adversarial test evidence; no customer data or production credentials.
- Phase 3: versioned TSIC contracts and full cross-repository E2E with tenant isolation, grant revocation, replay, recovery and evidence gates.
- Phase 5: deployed production, load/DR, security assessment and operational certification.

## Phase 2 evidence update — 2026-11-06

The initial host prerequisite and Firecracker VMM API smoke have been superseded by additional evidence recorded in the [Phase 2 benchmark plan](../persistent-agent-computer-benchmark-plan.md#11-execution-evidence-log--2026-11-06) and the Platform [persistent-computer runtime benchmark](https://github.com/LloydCoder/tinlance-agent-platform/blob/main/docs/production-runtime/PERSISTENT-COMPUTER-RUNTIME-BENCHMARK.md).

**Closed feasibility gates (CI-hosted, ephemeral KVM runners):**
- Pinned Firecracker v1.17.0 guest boots reached the explicit ready marker in 3/3 samples, with read-only root drive and no non-loopback network interface.
- Upstream-jailer smoke completed 3/3 jailed boots. The evidence recorded a dedicated unprivileged UID/GID, zero effective capabilities, `NoNewPrivs`, seccomp mode 2 on all observed VMM threads, PID/mount namespace separation, dedicated chroot identity and live cgroup v2 CPU/memory/PID limits.
- An aligned non-root W1 comparison completed 30 samples each for Firecracker, gVisor and Kata. It is a feasibility/startup-cost signal, not a controlled cross-runtime performance ranking.

**Phase 2 remains OPEN.** These CI results are not production isolation certification and do not establish hostile-tenant escape resistance, cross-tenant isolation, egress/metadata denial, browser compatibility, W2–W6 workload compatibility, snapshot/restore correctness, single-successor fencing, host-failure recovery, capacity/density, statistically controlled performance or production unit economics. The benchmark plan is the source of truth for exact workflow IDs, artifact digests, limitations and remaining gates.

The existing AWS test host previously inspected does not expose `/dev/kvm`. Read-only account inspection on 2026-11-06 found an active promotional AWS credit with USD 28.32 remaining and EC2 among its applicable services; this is not a spend authorization or proof that every required ancillary service is covered. The connected AWS identity resolves to the account root principal. **No AWS resources were provisioned or modified.** Do not use root credentials to provision the compute fleet; a least-privilege deployment identity, explicit cost cap/budget, network design and teardown control are required before cloud infrastructure can be created.

The architecture direction remains accepted and provider-neutral. Do not select a production provider or begin Phase 3 until the remaining Phase 2 hard security, lifecycle/recovery, comparative workload and economic gates are closed and ADR-0004 records a reviewed go/no-go decision.

## References

- Platform ADR-007: `docs/adr/ADR-007-sandbox.md`
- Platform ADR-002: `docs/adr/ADR-002-runtime-architecture.md`
- Platform P6 production runtime contract: `docs/production-runtime/P6-PRODUCTION-RUNTIME-CONTRACT.md`
- Agent OS workspace fabric and remote runtime
- Firecracker design, production host and snapshot documentation
- gVisor security architecture and production guide
- Kata Containers virtualization architecture
- OWASP Top 10 for Agentic Applications 2026
- CISA/ASD/NSA/CCCS/NCSC guidance on careful adoption of agentic AI services
