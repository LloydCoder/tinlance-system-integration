# Persistent Agent Computer — Phase 2 Feasibility and Benchmark Plan

**Status:** Approved test design; KVM prerequisite, direct and jailed Firecracker guest boots, and jailer process-confinement smoke verified on ephemeral CI runners; adversarial, comparative benchmark and recovery gates remain pending  
**Date:** 2026-11-06

## 1. Objective

Compare Firecracker-class microVMs, gVisor and Kata Containers for Tinlance persistent agent computers. The benchmark is not a popularity contest and must not turn vendor documentation into a security guarantee. It must use identical workload, host, guest, network, storage, policy and adversarial test profiles.

## 2. Candidate matrix

| Dimension | Firecracker-class microVM | gVisor | Kata Containers |
|---|---|---|---|
| Isolation model | Hardware virtualization and dedicated guest kernel | Userspace application kernel intercepts guest syscalls | Lightweight VM per pod/container via supported hypervisor |
| Best-fit hypothesis | Hostile, persistent, multi-tenant agent computers | Restricted untrusted workloads where syscall compatibility/performance is acceptable | Kubernetes/OCI-integrated VM-backed workload isolation |
| Persistence | Guest disk plus VM memory/state snapshots; hardware/software compatibility constraints | Container/workspace persistence; checkpoint/restore depends on runtime configuration | Guest VM and container lifecycle; runtime-specific persistence |
| Host requirements | KVM and supported virtualization hardware | Linux host kernel; supported platform mode and host controls | Hardware virtualization or supported hypervisor |
| Operational complexity | High: VMM lifecycle, jailer, TAP, image, disk, snapshot and host fleet | Medium: runtime integration, syscall compatibility, host cgroups/network | High: Kubernetes/containerd plus hypervisor/guest lifecycle |
| Key risks to test | VMM attack surface, host jail, snapshot uniqueness, CPU compatibility, network reattachment | syscall compatibility, performance, host cgroup/network dependence, sandbox policy | hypervisor support, pod lifecycle, storage, network and density |
| Initial role | Preferred candidate for T2 | T1 candidate | T3 candidate |

## 3. Test environment requirements

- Disposable, non-production, KVM-capable hosts with matching CPU features; no customer workloads.
- Fixed host OS/kernel/microcode, runtime versions, guest kernel, image digest and CPU/memory profiles.
- Synthetic tenant/workspace identities and generated test data.
- Separate control plane and guest network; default-deny egress proxy; metadata/private/control-plane deny rules.
- Encrypted workspace volume and snapshot store; synthetic secret canaries.
- Metrics and logs collected outside the guest.
- Explicit hourly/monthly spend ceiling, automatic teardown and owner.
- No use of production credentials, real customer data or production networks.

## 4. Workload profiles

| Profile | CPU / memory | Workload | Network |
|---|---:|---|---|
| W1 minimal agent | 1 vCPU / 512 MiB | shell, small Python/Node task, filesystem | denied |
| W2 developer workspace | 2 vCPU / 2 GiB | package install, build, unit tests, git operations | allowlisted package mirror only |
| W3 browser research | 2 vCPU / 2 GiB | Chromium, 5 tabs, DOM capture and bounded downloads | proxy allowlist |
| W4 hostile artifact | 2 vCPU / 2 GiB | untrusted archive/parser/build script and fuzz corpus | denied or controlled sink |
| W5 long-lived session | 2 vCPU / 4 GiB | persistent terminal/browser state over 8 hours | proxy allowlist |
| W6 recovery | same as W2/W3 | forced worker/host termination, snapshot and restore | re-established after restore |

## 5. Measurements

Collect p50/p95/p99 and sample counts, not only averages:

- Provision-to-ready and first-command latency.
- Browser cold start and navigation/interaction latency.
- CPU, memory, disk IOPS/throughput and network throughput.
- Concurrent density at fixed resource envelope and noisy-neighbour degradation.
- Suspend, snapshot, restore and reattach latency.
- Snapshot bytes, storage cost, restore compatibility and corruption behavior.
- Host CPU overhead and operational resource consumption.
- Egress policy enforcement latency and denial correctness.
- Per-computer active/idle/storage/egress cost.
- Failure recovery, lease fencing and duplicate operation behavior.

Each run records host model, CPU flags, kernel, runtime and image digests, config, test commit, raw metrics, logs, trace IDs and artifact hashes.

## 6. Security and adversarial gates

A candidate fails regardless of performance if it:
- permits cross-tenant file, process, browser, network or key access;
- permits guest access to host management sockets or provider credentials;
- reaches metadata, loopback, private or control-plane networks through any IPv4/IPv6, DNS, redirect or proxy bypass;
- accepts forged, stale, replayed, wrong-audience or revoked grants;
- resumes after policy, tenant, approval or credential revocation without reconciliation;
- permits duplicate restore or stale worker to create a second active successor;
- persists synthetic secret canaries into snapshots, images, logs or evidence payloads;
- allows guest to modify authoritative audit/evidence;
- bypasses CPU, memory, disk, process, bandwidth or cost quotas.

A failure is a blocker, not a score penalty.

## 7. Decision rubric

First apply hard security gates. Among candidates that pass:

| Criterion | Weight |
|---|---:|
| Isolation and threat-model fit | 30% |
| Lifecycle/recovery correctness | 20% |
| Browser and developer-workload compatibility | 15% |
| Operational complexity and reliability | 10% |
| Density and performance | 10% |
| Unit economics | 10% |
| Portability and lock-in | 5% |

No weighted score can override a failed hard security gate. Publish raw data and confidence intervals; document unsupported features and sample size.

## 8. Cost and capacity model

For each profile and persistence tier, calculate monthly unit cost as:

\`compute_active + compute_idle + reserved_host_capacity + workspace_storage + snapshot_storage + image_storage + egress + artifact_transfer + browser_concurrency + telemetry_and_evidence + KMS_and_secret_operations + backup_DR + operations\`.

Record active and idle cost separately, attribute every provider usage record to tenant/workspace/profile/instance/run, and model minimum warm capacity, idle suspension, regional reserve and peak concurrency. Capacity is bounded by allocatable CPU, memory, disk IOPS, network, browser slots and failure headroom. Do not assume nominal host capacity is fully schedulable.

## 9. Phase 2 exit criteria

- Reproducible benchmark harness and environment manifest.
- At least three runs per candidate/profile with sufficient samples for p95 comparisons.
- Adversarial suite passes for the selected candidate; all findings triaged.
- Restore/recovery behavior is understood and safe.
- Unit cost model includes active, idle, storage, snapshot, egress, observability and operations.
- Architecture decision updated with measured evidence and selected candidate or an explicit no-go.
- Environment teardown and spend reconciliation verified.

## 10. Primary technical references

The benchmark must validate the installed release and host configuration; documentation is a design input, not proof that a candidate is safe or compatible.

- [Firecracker production host setup](https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md) — KVM and CPU virtualization are prerequisites; production hardening includes the jailer or equivalent restrictions, seccomp, dedicated unprivileged identities, cgroup resource limits, host patching and hardware/side-channel mitigations.
- [Firecracker snapshot support](https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/snapshot-support.md) — snapshots comprise guest memory, VM state and separately managed disks; network/vsock sessions may not survive restore; host resources and CPU/software compatibility constrain restore. The harness must test reattachment, generation changes, single-successor semantics and cross-host compatibility rather than assume portability.
- [Firecracker snapshot versioning](https://github.com/firecracker-microvm/firecracker/blob/main/docs/snapshotting/versioning.md) — snapshot format compatibility is distinct from binary version compatibility and depends on host kernel, device model and CPU features.
- [gVisor security architecture](https://gvisor.dev/docs/architecture_guide/intro/) and [production guide](https://gvisor.dev/docs/user_guide/production/) — gVisor is an application-kernel boundary, not a VM; platform choice and workload-specific I/O/network overhead require measurement.
- [gVisor compatibility guide](https://gvisor.dev/docs/user_guide/compatibility/) — syscall and kernel-surface compatibility is incomplete by design; test the actual Python, Node, browser, build and developer workloads in the benchmark matrix.
- [Kata Containers virtualization architecture](https://kata-containers.github.io/kata-containers/design/virtualization/) and [installation requirements](https://github.com/kata-containers/kata-containers/blob/main/docs/install/README.md) — Kata uses a VM boundary behind an OCI/containerd lifecycle; supported hypervisor and hardware/nested-virtualization requirements must be verified with the target host's supported diagnostic tooling.



## 11. Execution evidence log — 2026-11-06

### Host prerequisite and VMM API smoke

- Agent Platform PR [#163](https://github.com/LloydCoder/tinlance-agent-platform/pull/163) merged at `61c255c700594b9f6b626a7fe3254c7fd4a92213`.
- Exact tested branch commit: `208e12ff871e5c7987f6e47e58c375b86ab47bba`.
- Host-feasibility workflow run: [42168071508](https://github.com/LloydCoder/tinlance-agent-platform/actions/runs/42168071508).
- Evidence artifact: [persistent-computer-host-feasibility-42168071508](https://github.com/LloydCoder/tinlance-agent-platform/actions/runs/42168071508/artifacts/13479114687), artifact SHA-256 `f0a9614dce876fc69010f5dd341a10131deef71edf1d9272762619213cda6c5a`.
- Runner: ephemeral GitHub-hosted Ubuntu 24.04.5, x86_64, kernel `7.0.0-1017-azure`.
- Probe: KVM device present and accessible; CPU virtualization present; cgroup v2, unprivileged user namespaces and seccomp filter support present; container-sandbox prerequisites reported ready; `seccomp_active=false` for the probe process.
- Firecracker: release v1.17.0 archive SHA-256 `06094a1108ae9e82aa4c23a775aa92758f53f1175d422270d9d6162cb9ade558` verified; VMM API socket responded to `GET /version` with the expected v1.17.0 version.
- No AWS resources were provisioned or modified. The existing AWS test host inspected for this programme does not expose `/dev/kvm` and is not a valid Firecracker host.

### What this evidence proves — and does not prove

**Proven:** an ephemeral KVM-capable runner exposes the required host prerequisites; pinned Firecracker v1.17.0 boots the guest both directly and through the upstream jailer; the jailed process runs under a dedicated unprivileged identity with zero effective capabilities, `NoNewPrivs`, seccomp mode 2 on every observed Firecracker thread, PID/mount namespace separation, a dedicated chroot root, and enforced cgroup v2 CPU/memory/PID limits.

**Not proven:** hostile guest escape resistance or cross-tenant adversarial access denial; egress/metadata/private-network policy; gVisor or Kata compatibility; browser operation; suspend/resume; snapshot/restore; lease fencing; network reattachment; density; statistically meaningful p95 latency; unit economics; or operational recovery.

The host probe's `seccomp_active=false` field describes the probe/runner process, not the Firecracker VMM. The separately inspected jailed Firecracker process reported seccomp mode 2 on all four observed threads. These are smoke-level host checks, not production security certification. The GitHub-hosted runner is ephemeral validation infrastructure, not an approved persistent-computer fleet.

### Remaining Phase 2 gates

1. [x] Boot a pinned, provenance-verified guest kernel and root filesystem under Firecracker; capture boot and guest-ready evidence (direct-VMM smoke only; not jailer certification).
2. [x] Exercise Firecracker through the upstream jailer with cgroups, namespaces, seccomp, unprivileged identity, chroot and resource limits. Evidence is a three-boot process-confinement smoke, not a production certification.
3. Execute comparable Firecracker, gVisor and Kata workload profiles on a controlled KVM-capable environment; record at least three runs per candidate/profile and p50/p95/p99 with sample counts.
4. Run the full adversarial suite, including tenant separation, filesystem/process escape, metadata/private-network denial, DNS/redirect/IPv6/proxy bypass, grant revocation, snapshot secret leakage and duplicate-restore fencing.
5. Verify suspend/resume, snapshot/restore, host/worker failure recovery, network/vsock reattachment and teardown.
6. Produce a fully attributed active/idle/storage/snapshot/egress/telemetry/operations cost model and verify environment teardown and spend reconciliation.
7. Update ADR-0004 with measured results and an explicit go/no-go. Do not select a production provider from the host smoke alone.

**Phase 2 remains OPEN.** The KVM prerequisite, direct guest-boot, and jailer host-confinement smoke gates are closed. Adversarial, comparative, recovery, cost and production go/no-go gates remain open.



### Guest boot smoke — 2026-11-06

- Agent Platform PR [#166](https://github.com/LloydCoder/tinlance-agent-platform/pull/166) merged at `f578cca7130a079ebff7602b56af520fb1aa6db5`.
- Tested PR head: `12aed58fc2a4901e4fa28e7b8c61780faaab1b26`; all 20 exact-head check runs completed successfully, including Python 3.12/3.13/3.14, quality, R10 adversarial certification, TSIC conformance, SQL, CodeQL, secret scanning, Reference Agents and the KVM guest-boot workflow.
- Guest boot workflow run: [42171110389](https://github.com/LloydCoder/tinlance-agent-platform/actions/runs/42171110389).
- Evidence artifact: [firecracker-guest-boot-42171110389](https://github.com/LloydCoder/tinlance-agent-platform/actions/runs/42171110389/artifacts).
- Runner: ephemeral GitHub-hosted Ubuntu 24.04, x86_64, KVM-capable; no persistent AWS resource was provisioned or modified.
- Firecracker release: v1.17.0; release archive SHA-256 `06094a1108ae9e82aa4c23a775aa92758f53f1175d422270d9d6162cb9ade558`.
- Guest kernel source key: `firecracker-ci/20261105-6ea6634994fa-0/x86_64/vmlinux-6.18.56`; SHA-256 `af348226aa2a25b846156150d5cdb5dae3bf2a022f1db176e3a2b9a3249817bf`.
- Guest rootfs source key: `firecracker-ci/20261105-6ea6634994fa-0/x86_64/ubuntu-24.04.squashfs`; source squashfs SHA-256 is pinned in `tests/fixtures/firecracker-guest-assets.json`; generated ext4 rootfs SHA-256 for this run: `19901f0f56f796e4bf5918f3ad95149cd10ece9faabf213b17bb2ef0c7a367c2`.
- Result: 3/3 fresh guest instances reached the explicit `TINLANCE_GUEST_READY` init marker with no virtual NIC configured and a read-only root drive. Median boot-to-marker: 1,089.4 ms; maximum: 1,092.9 ms.

**Evidence interpretation:** this closes the pinned guest-boot smoke gate. It does not prove jailer execution, production host hardening, hostile-tenant isolation, cgroup enforcement under adversarial load, network policy, snapshot/restore safety, lease fencing, or provider suitability. Three samples are a smoke check and are not sufficient for p95 comparisons. The benchmark plan remains open.


### Jailer host-confinement smoke — 2026-11-06

- Agent Platform PR [#167](https://github.com/LloydCoder/tinlance-agent-platform/pull/167) merged at `a9f68a5dabf895fbb81975615e4425b42f9da01a`.
- Tested head: `d3b5d9783a04da3fd3c2e1a59bd1573cae10c06e`; all 20 exact-head check runs completed successfully.
- Ephemeral KVM workflow: [42173261878](https://github.com/LloydCoder/tinlance-agent-platform/actions/runs/42173261878).
- Result: 3/3 fresh guests booted through Firecracker v1.17.0 and the upstream jailer. Median boot-to-ready: 1,158.5 ms; maximum: 1,159.0 ms.
- Process evidence: UID 999 / GID 987; effective capabilities `0000000000000000`; `NoNewPrivs=1`; process seccomp mode 2; all four observed Firecracker threads reported seccomp mode 2; PID and mount namespaces were distinct from the host.
- Chroot boundary was verified by matching the jailed process root inode to the dedicated chroot root (`66305:9450344`).
- Cgroup v2 limits were read back from the live process cgroup: `cpu.max=100000 100000`, `memory.max=805306368`, `pids.max=128`.
- The guest root drive was read-only and no virtual NIC was configured. The runner was ephemeral GitHub-hosted KVM; no AWS resources were provisioned, modified or left running.

**Evidence interpretation:** this closes the upstream-jailer process-confinement smoke gate. It does not certify production host configuration or prove hostile escape resistance, cross-tenant adversarial isolation, egress policy, snapshot/restore, fencing or recovery. The three boot samples remain smoke measurements, not p95 evidence.
