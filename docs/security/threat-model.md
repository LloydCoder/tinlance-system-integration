# TSIC Threat Model

Primary threats: incorrect authority assignment, cross-tenant access, contract drift, stale API inventory, malicious events, secret leakage, unsafe tool/MCP exposure, replay/duplication, provenance loss, and compromised dependencies.

Controls: registry validation, contract tests, identity/authorization requirements, security scanning, immutable evidence references, and runtime conformance suites.

## Persistent agent computer

The persistent-computer workload has a dedicated threat model and phase-gated evidence record:

- [Persistent Agent Computer Threat Model](../architecture/persistent-agent-computer-threat-model.md) — assets, B1-B9 trust boundaries, PC-01–PC-20 threats, abuse cases and residual risks.
- [ADR-0004 — Persistent Agent Computer Architecture](../architecture/decision-records/ADR-0004-persistent-agent-computer.md) — authority, lifecycle, isolation, persistence and production decision gates.
- [Phase 2 Feasibility and Benchmark Plan](../architecture/persistent-agent-computer-benchmark-plan.md) — workload profiles, measurements, adversarial gates, evidence and cost model.
- [Canonical Phase 2 tracker](https://github.com/LloydCoder/tinlance-system-integration/issues/102).

**Current status (2026-11-07):** The W2 rootfs normalizer implementation is merged, but independent-build reproducibility is not accepted: two identical-input PR #190 builds differed only in volatile `var/cache/ldconfig/aux-cache`. A regression test and independent no-cache rebuild comparison are pending in [platform PR #190](https://github.com/LloydCoder/tinlance-agent-platform/pull/190). W2 jailer execution passed 3/3 and direct Firecracker/gVisor each passed 30 workloads on the current exact-head run; Kata W2 and the reproducibility fix remain pending. W3 browser/egress, W4 adversarial and cross-tenant isolation, W5 eight-hour persistence, W6 snapshot/restore, production economics and independent security review remain open. The W1 jailer smoke and W2 direct-VMM smoke are not substitutes for W2 jailed acceptance or production certification.

No production provider is selected, no production isolation claim is made, and no cloud resources have been provisioned.
