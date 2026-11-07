# Trust Boundaries

Boundaries exist between tenants, external customer systems, Tinlance systems, agents, tools/MCP servers, third-party APIs, developer surfaces, and production infrastructure.

Crossing a boundary requires explicit identity, authorization, validation, provenance, and audit expectations.

## Persistent agent computer boundaries

| Boundary | Crossing | Required invariant |
|---|---|---|
| B1 | User/agent/model ↔ Agent OS | Intent and retrieved content are untrusted; OS orchestrates lifecycle but cannot grant execution authority. |
| B2 | Agent OS ↔ Agent Platform API/SDK | Authenticated tenant/workspace/run context; Platform performs policy, approval and authorization. |
| B3 | Platform ↔ provider adapter | Only short-lived, audience-bound, one-time Platform grants authorize provider operations. |
| B4 | Host/hypervisor ↔ guest | Per-workload isolation, jailer, seccomp, namespaces, cgroups, non-root identity, no host credentials or management sockets in guest. |
| B5 | Guest ↔ workspace/object storage | Tenant/workspace-scoped encrypted volumes; no shared writable mounts; quota and lifecycle enforcement outside guest. |
| B6 | Guest/browser ↔ egress | Host-enforced proxy policy; destination validation at connect; deny metadata, private, loopback, link-local and control-plane routes; revalidate redirects and DNS. |
| B7 | Guest output ↔ evidence/audit | Guest output is untrusted evidence input; authoritative audit, signing and retention remain outside guest. |
| B8 | Snapshot/backup ↔ restore controller | Restore revalidates tenant, policy, grants, approvals, credentials and generation; fencing prevents multiple active successors. |
| B9 | Agent ↔ peer agent/MCP/A2A | Signed identity/delegation, audience/scope binding, provenance and replay protection. |

Only B2's authenticated Platform request and B3's Platform-issued grant can authorize consequential execution. TADL can declare requested capabilities but cannot grant them. Provider adapters and guests are untrusted execution substrates; guest output never becomes authoritative audit.

### Current evidence boundary (2026-11-07)

- PR #185 and PR #187 provide the merged Firecracker W2 workspace and rootfs-normalization implementation. Independent-build reproducibility remains open because identical-input PR #190 builds differed only in volatile `var/cache/ldconfig/aux-cache`; a regression test and second no-cache build comparison are required.
- PR #187's Firecracker direct-VMM, gVisor and Kata W2 artifacts reported 30 samples each and the same normalized rootfs digest. These are ephemeral functional/reproducibility results, not production isolation certification.
- A separate W1 jailer smoke proves process-level seccomp mode 2 across observed threads, no-new-privileges, zero effective capabilities, PID/mount namespaces, chroot identity and cgroup limits. It is W1 evidence only.
- PR #190 is the pending W2 jailer gate. It adds a dedicated loopback-only network namespace, offline npm package installation and package/toolchain provenance checks. W2 is not complete until exact-head workflows pass and all artifacts are independently inspected.
- W3 egress/browser policy, W4 adversarial and cross-tenant tests, W5 eight-hour persistence, W6 snapshot/restore/fencing, production economics and independent review remain open.

See the [Persistent Agent Computer Threat Model](persistent-agent-computer-threat-model.md), [ADR-0004](decision-records/ADR-0004-persistent-agent-computer.md), [benchmark plan](persistent-agent-computer-benchmark-plan.md) and [TSIC issue #102](https://github.com/LloydCoder/tinlance-system-integration/issues/102).
