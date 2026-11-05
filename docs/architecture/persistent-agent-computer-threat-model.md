# Persistent Agent Computer — Threat Model

**Status:** Phase 1 design baseline  
**Date:** 2026-11-05  
**Scope:** Multi-tenant persistent agent computers, browser/terminal execution, workspace storage, provider control plane and recovery.

## 1. Security objectives

1. Prevent cross-tenant access to compute, memory, files, browser sessions, network, secrets and evidence.
2. Ensure only Agent Platform can authorize consequential execution.
3. Prevent guest compromise from becoming host or control-plane compromise.
4. Prevent prompt injection and untrusted tool/browser content from changing policy or authority.
5. Preserve integrity and causal lineage of runs, grants, operations and evidence.
6. Ensure revocation, cancellation, expiry and tenant suspension reach running computers.
7. Prevent replay, duplicate provisioning, split-brain leases and duplicate side effects after recovery.
8. Bound resource consumption and financial exposure.
9. Ensure snapshots and backups cannot resurrect stale authority or secrets.
10. Support forensic investigation without relying on guest-controlled logs.

## 2. Assets and trust boundaries

### Assets
- Platform signing keys, grant issuer, policy and approval state.
- Tenant, subject, agent, workspace, run and capability identities.
- Provider credentials, hypervisor API sockets, host kernel/KVM and host metadata.
- Guest kernel, memory, image, filesystem, browser profile, cookies and downloads.
- Workspace volumes, VM snapshots, backups, artifact objects and encryption keys.
- Egress policy, DNS resolver, proxy identity and network routes.
- Lifecycle operation journal, leases, fencing tokens, idempotency records.
- Audit events, evidence references, trace context, logs and telemetry.
- User approvals, connector tokens and secret material.

### Trust boundaries
- B1: user/agent/model ↔ OS orchestration.
- B2: OS ↔ Platform API/SDK.
- B3: Platform control plane ↔ provider adapter.
- B4: provider host/hypervisor ↔ guest microVM/container.
- B5: guest ↔ workspace volume/object store.
- B6: guest/browser ↔ egress proxy and external internet.
- B7: guest output ↔ evidence/audit service.
- B8: snapshot/backup store ↔ restore controller.
- B9: agent ↔ peer agent/MCP/A2A connector.

Only B2's authenticated Platform request and B3's Platform-issued grant can authorize an execution. B4-B9 are untrusted data and execution boundaries.

## 2.1 Trust-boundary diagram

```mermaid
flowchart TB
    U[User / Agent / Model] -->|intent and untrusted content| OS[Agent OS: lifecycle orchestration]
    OS -->|authenticated request, tenant/workspace context| PL[Agent Platform: policy, approvals, grants]
    PL -->|short-lived audience-bound grant| AD[Provider adapter: untrusted substrate]
    AD -->|provision / lifecycle operations| HV[Host, hypervisor and isolated guest]
    HV -->|bounded I/O through host enforcement| EG[Egress proxy and network policy]
    HV -->|workspace data only| WV[Encrypted tenant/workspace volume]
    HV -->|untrusted result and evidence candidate| EV[External evidence intake]
    PL -->|authoritative audit and run evidence| AUD[Platform evidence / audit store]
    TSIC[TSIC: canonical contracts and certification] -. validates contracts and evidence .-> PL
    TADL[TADL: declarative profile validation] -. requests capabilities only .-> OS
    SDK[Platform SDK: typed client] -. transports context; no authority .-> PL

    classDef authority fill:#e8f3ff,stroke:#245b8a,color:#102b44;
    classDef untrusted fill:#fff0e8,stroke:#a64b1f,color:#4a2412;
    classDef evidence fill:#eaf7ed,stroke:#357348,color:#153b20;
    class PL,TSIC authority;
    class HV,AD,EG untrusted;
    class AUD,EV evidence;
```

The provider adapter and guest are untrusted. Only Platform-issued grants authorize execution; guest output is evidence input, never authoritative audit. TSIC certifies contracts and does not provision or execute workloads.

## 3. Threat actors and assumptions

- Malicious tenant with valid account attempting cross-tenant escape or resource abuse.
- Compromised or prompt-injected agent attempting unauthorized actions.
- Malicious website, document, browser extension, package, repository or downloaded artifact.
- Compromised guest process attempting host escape or metadata/credential theft.
- Malicious or compromised provider worker/operator.
- Stale or compromised OS worker replaying operations or grants.
- Supply-chain attacker compromising base image, hypervisor binary, browser or extension.
- External attacker exploiting public control-plane or egress-facing services.

Assumptions: cloud/provider host and hardware have residual trust; no sandbox is an absolute guarantee. Host OS, hypervisor, firmware, KVM, control plane and identity services require patching, monitoring and incident response. Side-channel and hardware attacks remain residual risks.

## 4. Threat scenarios and required controls

| ID | Threat | Impact | Required preventive controls | Detection/recovery evidence |
|---|---|---|---|---|
| PC-01 | Guest escapes container or sandbox into host | Host compromise, cross-tenant data exposure | Per-instance microVM for hostile tier; jailed VMM; seccomp; namespaces; cgroups; no privileged mounts/devices | Host integrity telemetry, canary tests, isolate host, preserve forensic image |
| PC-02 | Guest reaches another tenant's disk or browser profile | Confidentiality and integrity breach | Dedicated volume/key/profile per tenant-workspace; no shared writable mounts; access checks outside guest | Cross-tenant negative tests, storage audit, revoke tenant leases |
| PC-03 | Guest accesses cloud metadata/provider credentials | Provider account takeover | Block metadata IPs at host egress; no host creds in guest; scoped workload identity; proxy deny rules | Egress alerts, credential rotation, host quarantine |
| PC-04 | DNS rebinding, redirect or IPv6 bypass reaches private/control-plane network | SSRF, lateral movement | Resolve and validate each connection; pin policy at connect; revalidate redirects; block RFC1918, loopback, link-local, ULA, metadata and control-plane routes | Egress policy logs, adversarial SSRF suite, route revocation |
| PC-05 | Prompt injection in page/document/tool output requests privileged action | Unauthorized side effect | Treat retrieved content as data; capability allowlist; Platform reauthorization; approval gates; content/action separation | Tool decision trace, policy denial and approval evidence |
| PC-06 | Forged/replayed execution grant | Unauthorized execution | Audience-bound signed grant, short expiry, unique nonce, run/capability/tenant binding, one-time consumption and revocation | Replay tests, grant ledger, deny and alert |
| PC-07 | OS worker or guest bypasses Platform and directly executes host action | Authority bypass | Provider adapter accepts only Platform grant; no direct provider API from OS/TADL/SDK; CI architecture invariants | Negative integration tests, trace correlation |
| PC-08 | Snapshot resurrects expired secret, approval, token or stale idempotency state | Stale authority, duplicate side effect | No secrets in snapshots; restore quarantine; rotate credentials; reconcile policy, approvals, leases and idempotency; one successor per snapshot | Restore-after-revocation tests, secret scans, grant ledger |
| PC-09 | Snapshot cloned twice reuses app-level randomness or identity | Duplicate identity, cryptographic misuse | Single-successor restore; generation/fencing; guest re-key protocol; dedupe app identifiers; no blind clone fan-out | Concurrent restore race tests, uniqueness checks |
| PC-10 | Compromised image/browser/extension | Guest compromise or supply-chain execution | Signed images, provenance/SBOM, pinned digests, vulnerability scanning, allowlisted extensions, promotion and rollback | Image attestation, scan reports, incident rollback |
| PC-11 | Malicious download/archive exhausts disk or parser | RCE, decompression bomb, resource exhaustion | Quarantine downloads; MIME/type validation; archive limits; malware scan; CPU/memory/disk quotas | Download audit, bomb tests, quota events |
| PC-12 | Queue redelivery or lease split-brain starts two workers | Duplicate side effects and corruption | Durable operation journal, idempotency key, compare-and-swap generation, lease fencing, single-writer ownership | Duplicate delivery/failover tests, operation ledger |
| PC-13 | Noisy tenant exhausts host, browser slots or egress | Availability and cost impact | Per-tenant quotas, cgroups, concurrency caps, fair scheduling, idle suspend, budget enforcement | Saturation tests, per-tenant cost and SLO telemetry |
| PC-14 | Guest tampers with logs/evidence | Loss of accountability | Evidence outside guest; append-only/immutable records; signed references and trace lineage | Evidence tamper tests, independent audit store |
| PC-15 | Secret appears in logs, browser storage or snapshot | Credential theft | JIT secret broker, short TTL, memory-only injection where feasible, redaction, no snapshot persistence, revocation | DLP/secret scanning, canary credentials, rotation proof |
| PC-16 | Revocation does not terminate active work | Continued unauthorized action | Platform revocation event, provider kill/fence, bounded heartbeat and lease, deny next operation immediately | Revocation latency SLO, kill verification and audit |
| PC-17 | Hypervisor management socket/API exposed | Host VM control | Per-instance Unix socket, strict permissions, host-only namespace, never guest-mounted or internet-exposed | Host config scan, socket access tests |
| PC-18 | Side-channel/hardware exploit crosses isolation | Confidentiality or integrity loss | Hardware/host patching, tenant placement policy, dedicated hosts for highest risk, microcode lifecycle; document residual risk | Vulnerability tracking, placement evidence, incident response |
| PC-19 | Peer agent/MCP message forges identity or scope | Unauthorized delegation | Signed identity context, Platform-issued delegation, audience and scope binding, provenance and replay protection | Forged-peer tests, delegation audit |
| PC-20 | Termination leaves disk/snapshot/key accessible | Data remanence | Cryptographic erase/key revocation, storage lifecycle, asynchronous deletion verification and retention policy | Deletion evidence, restore denial test |

## 5. Abuse cases that must fail closed

- Tenant A supplies Tenant B's workspace ID, volume ID, snapshot ID, lease ID or evidence reference.
- Guest attempts `169.254.169.254`, localhost, RFC1918, IPv6 ULA/link-local, DNS rebinding or redirect to private address.
- Grant has wrong audience, tenant, subject, agent, workspace, run, capability, policy revision, expiry, nonce or idempotency key.
- Grant is replayed, already consumed, revoked or issued before a policy change.
- A restore occurs after tenant suspension, grant revocation, approval withdrawal or credential rotation.
- Two workers attempt to renew or mutate the same generation concurrently.
- A provider reports `ready` without a valid instance identity, image digest and attestation.
- Guest tries to mount host paths, access host sockets/devices, change cgroups or read host credentials.
- Browser content tells the agent to ignore policy, reveal secrets, use another tenant's identity or execute a side effect.
- Guest forges audit events or uploads a false evidence reference.
- Snapshot is restored on incompatible hardware, CPU features, host kernel or snapshot format.
- Budget is exhausted or lease expires during an action.

## 6. Required Phase 2 adversarial and performance tests

- MicroVM/container escape-oriented configuration review and host boundary checks.
- Tenant-to-tenant filesystem, volume, browser profile, key and network isolation.
- SSRF/DNS rebinding/redirect/IPv6 and cloud metadata denial.
- Grant forgery, wrong-audience, replay, expiry, revocation and policy-version tests.
- Snapshot restore after secret expiry, approval withdrawal, policy change and tenant suspension.
- Duplicate restore, concurrent lease renewal, stale generation and queue redelivery.
- Host crash, worker crash, storage loss, network partition, corrupt snapshot and provider API outage.
- Malicious browser page, extension, archive, MIME confusion and decompression bomb.
- Quota exhaustion, noisy-neighbour and idle cost leak.
- Provision/start/suspend/resume/snapshot/restore/terminate latency, density and cost.
- Image signature, provenance, SBOM, vulnerability and rollback tests.

All test subjects and credentials must be synthetic. No customer data, production credentials or production deployment are permitted in Phase 2.

## 7. Residual risk and production blockers

Residual risks include hypervisor/host/firmware vulnerabilities, hardware side channels, provider operator access, snapshot implementation defects and external network abuse. These require documented risk acceptance, defense in depth and operational controls; they cannot be eliminated by application-level tests.

Phase 2 is blocked until an explicitly authorized non-production environment provides KVM-capable compute, isolated networking, encrypted storage, image registry and controlled cost ceilings. No infrastructure is created by this design document.

## 8. Standards and source mapping

- OWASP Top 10 for Agentic Applications 2026: goal hijack, tool misuse, identity/privilege abuse, supply-chain compromise, unexpected code execution, memory/context poisoning, insecure inter-agent communication, cascading failures, human-agent trust exploitation and rogue-agent behavior.
- CISA/ASD/NSA/CCCS/NCSC guidance: least privilege, layered defense, identity, human oversight, threat modeling, continuous monitoring and security assessment.
- OWASP ASVS 5.0 and OWASP Top 10: application/control-plane validation and secure implementation.
- NIST SP 800-190: container security risks and controls; NIST zero-trust principles for explicit identity and per-request authorization.

## 9. Phase 1 review checklist

- [x] Platform sole authority; OS lifecycle only.
- [x] TADL cannot grant runtime privileges.
- [x] Provider cannot approve or authorize actions.
- [x] Tenant and workspace isolation defined across all planes.
- [x] Network and metadata protections defined outside guest.
- [x] Secrets and evidence kept outside guest persistence.
- [x] Snapshot restore revalidates identity, policy, approvals and credentials.
- [x] Idempotency, generation and fencing defined.
- [x] RPO/RTO and SLOs remain unpromised until measured.
- [x] Phase 2 requires explicit non-production infrastructure authorization.

**Review disposition (2026-11-05):** All ten design assertions were checked against the Phase 1 ADR, Platform ADR-007 and P6 deployment contract, OS remote-runtime/workspace-fabric ownership, Platform SDK authority statement, TADL immutable ecosystem lock and TSIC Agent System baseline. This is an architecture/documentation review, not a claim that Phase 2 infrastructure or runtime controls are implemented. Phase 2 remains blocked pending a separately authorized KVM-capable non-production environment and spend ceiling.
