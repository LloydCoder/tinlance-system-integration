# Persistent Agent Computer — Phase 2 Feasibility and Benchmark Plan

**Status:** Approved test design; execution requires an authorized non-production KVM-capable environment  
**Date:** 2026-11-05

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

