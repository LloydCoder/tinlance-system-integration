# TSIC Documentation

This index organizes TSIC documentation by the four Diátaxis concerns: learning, task completion, conceptual understanding, and precise reference. Normative contracts and registries remain authoritative over explanatory prose.

## Tutorials

- [Repository quick start](../README.md#quick-start) — clone the repository and run the core checks.
- [End-to-end integration](operations/e2e-integration.md) — understand and run the reference integration workflow.

## How-to guides

- [Phase 0 runbook](operations/phase0-runbook.md)
- [P0 ecosystem reconciliation](operations/p0-ecosystem-reconciliation.md)
- [Failure and recovery certification](operations/failure-recovery-certification.md)
- [Adapter fabric](integrations/adapter-fabric.md)
- [Ecosystem lock](governance/ecosystem-lock.md)
- [TSIC-18 ecosystem reconciliation](integration/TSIC-18-ECOSYSTEM-RECONCILIATION.md)

## Explanation

- [Architecture overview](architecture/overview.md)
- [Canonical system model](architecture/canonical-system-model.md)
- [Authority model](architecture/authority-model.md)
- [Authority reconciliation](architecture/authority-reconciliation.md)
- [Integration topology](architecture/integration-topology.md)
- [Identity and agent registration](architecture/identity-and-agent-registration.md)
- [Trust boundaries](architecture/trust-boundaries.md)
- [Model and agent interoperability](architecture/model-and-agent-interoperability.md)
- [Event and trace fabric](contracts/event-and-trace-fabric.md)
- [Attribution spine](economics/attribution-spine.md)
- [Threat model](security/threat-model.md)
- [Persistent Agent Computer threat model](architecture/persistent-agent-computer-threat-model.md)
- [Persistent Agent Computer benchmark plan](architecture/persistent-agent-computer-benchmark-plan.md)
- [Persistent Agent Computer ADR-0004](architecture/decision-records/ADR-0004-persistent-agent-computer.md)

## Reference

- [Ecosystem manifest](../manifests/ecosystem.json)
- [Capability authority catalog](../catalog/capabilities/authority.json)
- [Canonical phase registry](../catalog/phases/registry.json)
- [Contract registry](../catalog/contracts/registry.json)
- [Service registry](../catalog/services/registry.json)
- [Dependency graph](../catalog/dependencies/graph.json)
- [Canonical workflows](../workflows/canonical.json)
- [Ecosystem lock policy](../policies/ecosystem-lock.json)
- [Service and contract registry](architecture/service-contract-registry.md)
- [TSIC-10 ThreatFade Web ↔ Engine](certification/TSIC-10-threatfade-web-engine.md)
- [TSIC-11 BugFlow integration](certification/TSIC-11-bugflow-integration.md)
- [TSIC-12 HEZQARA governed healthcare](certification/TSIC-12-hezqara-governed-healthcare.md)
- [TSIC-14 Closed-Loop Intelligence](integration/TSIC-14-closed-loop-intelligence.md)
- [TSIC-15 trace context](observability/trace-context-contract.md)
- [TSIC-17 Production System-of-Systems](certification/production-system-of-systems.md)
- [TSIC-18 AaaS catalog](integrations/aaas-catalog.md)
- [TSIC-19 Autonomous Revenue Operating Loop](certification/autonomous-revenue-operating-loop.md)
- [2026 standards baseline](standards/2026-baseline.md)
- [Compatibility guidance](../compatibility/README.md)
- [Conformance requirements](../conformance/README.md)

## Certification and historical evidence

- [Current main-branch evidence snapshot](audits/current-main-evidence-2026-11-07.md)
- [Historical TSIC-31–41 numbering note](architecture/serial-integration-31-41.md)
- [Historical TSIC-31–41 certification record](certification/TSIC-31-41-certification-record.md)
- [Historical TSIC-18–38 certification record](certification/TSIC-18-38-certification-record.md)
- [Persistent Agent Computer Phase 2 tracker](https://github.com/LloydCoder/tinlance-system-integration/issues/102)

## Source-of-truth rules

1. `catalog/phases/registry.json` is the sole canonical TSIC phase registry.
2. `manifests/`, `catalog/`, `contracts/`, `schemas/`, `workflows/`, `policies/`, and `conformance/` contain machine-readable artifacts; follow their schemas and local documentation to determine normative status.
3. Historical records preserve prior evidence and numbering. They do not supersede current registries.
4. Evidence must identify its exact commit, workflow run, scope, and limitations.
5. Reference workflow success does not prove production deployment, availability, or operational assurance.
6. Agent Platform remains the sole generic consequential execution authority. TSIC governs integration and conformance; it is not an execution runtime.
