# Canonical System Model

TSIC freezes the Tinlance system-of-systems topology. The registry is authoritative for system identity; the authority catalog is authoritative for capability ownership. TSIC governs integration contracts, compatibility and conformance, but never becomes a second agent runtime or authorization service.

## Canonical routes

- Agent: Agent Developer -> Agent OS -> Platform SDK -> Agent Platform.
- Engineering: World Intelligence -> TADS -> SDEA -> ReconOS -> FadeReach -> Sales -> FDSE -> FDE.
- Transformation: World Intelligence -> TADS -> Transformation -> FDSE -> FDE.
- Web intelligence: Agent Platform (governed caller) -> Tinlance Web Intelligence (web acquisition) -> World Intelligence (canonical temporal state).
- Persistent compute: Agent Platform (authority and policy) -> Persistent Agent Computer (workspace/runtime lifecycle) -> candidate Firecracker, gVisor or Kata isolation substrate.

Routes define integration topology; they do not transfer authority between systems.

## Persistent compute authority boundary

The Persistent Agent Computer is a governed execution substrate beneath Agent Platform, not a second authorization authority.

- **Agent Platform** remains authoritative for identity, tenant/workspace/run authorization, policy, approvals, capability grants, budgets, secret release, audit and evidence.
- **Agent OS** orchestrates task and workspace lifecycle but cannot independently grant consequential execution authority.
- **Persistent Agent Computer** manages workspace lifecycle, runtime provisioning, isolation enforcement, leases, storage attachment, browser lifecycle and snapshot/restore only under Platform-issued grants.
- **Firecracker, gVisor and Kata** are candidate isolation substrates. No production provider/runtime choice is implied by the W2 feasibility results.
- **Guest code and guest output are untrusted.** Guests receive scoped, short-lived capabilities only; they never receive Platform master credentials or unrestricted provider credentials.
- **TSIC** owns integration contracts, compatibility, conformance and certification evidence. It does not run the guest or become a second runtime.

The current Phase 2 work is non-production feasibility and acceptance. The W2 rootfs normalizer is merged, but independent-build reproducibility remains blocked by a volatile ldconfig auxiliary cache found in PR #190's forensic build comparison. W2 jailer execution passed 3/3; the rootfs fix, independent rebuild comparison and remaining runtime checks are tracked in [platform PR #190](https://github.com/LloydCoder/tinlance-agent-platform/pull/190). See [ADR-0004](decision-records/ADR-0004-persistent-agent-computer.md), the [threat model](persistent-agent-computer-threat-model.md) and [benchmark plan](persistent-agent-computer-benchmark-plan.md).
