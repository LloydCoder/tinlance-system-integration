# TSIC Documentation

This index organizes the repository using a practical Diátaxis model while preserving the existing normative architecture and certification documents.

## Tutorials

- [Repository quick start](../README.md#quick-start)
- [End-to-end integration](operations/e2e-integration.md)

## How-to guides

- [Phase 0 runbook](operations/phase0-runbook.md)
- [P0 ecosystem reconciliation](operations/p0-ecosystem-reconciliation.md)
- [TSIC-18 ecosystem reconciliation](integration/TSIC-18-ECOSYSTEM-RECONCILIATION.md)
- [Failure and recovery certification](operations/failure-recovery-certification.md)
- [Adapter fabric](integrations/adapter-fabric.md)
- [Agent Platform reference adapter](../integrations/agent-platform/reference-adapter.v1.schema.json)
- [Ecosystem lock](governance/ecosystem-lock.md)

## Explanation

- [Architecture overview](architecture/overview.md)
- [Canonical system model](architecture/canonical-system-model.md)
- [Authority model](architecture/authority-model.md)
- [Authority reconciliation](architecture/authority-reconciliation.md)
- [Ecosystem conformance authority](architecture/decision-records/ADR-0003-ecosystem-conformance-authority.md)
- [Identity and agent registration](architecture/identity-and-agent-registration.md)
- [Integration topology](architecture/integration-topology.md)
- [Trust boundaries](architecture/trust-boundaries.md)
- [Model and agent interoperability](architecture/model-and-agent-interoperability.md)
- [Attribution spine](economics/attribution-spine.md)
- [Threat model](security/threat-model.md)

## Reference

- [Event and trace fabric](contracts/event-and-trace-fabric.md)
- [Service and contract registry](architecture/service-contract-registry.md)
- [TSIC-10 ThreatFade Web ↔ Engine certification](certification/TSIC-10-threatfade-web-engine.md)
- [TSIC-11 BugFlow integration certification](certification/TSIC-11-bugflow-integration.md)
- [Production system-of-systems certification](certification/production-system-of-systems.md)
- [TSIC-18–38 certification record](certification/TSIC-18-38-certification-record.md)
- [2026 standards baseline](standards/2026-baseline.md)
- [Compatibility](../compatibility/README.md)
- [Conformance requirements](../conformance/README.md)

## Repository structure

The root README is the visitor-oriented entry point. JSON under catalog/, contracts/, schemas/, manifests/, workflows/, policies/, and reliability/ is normative or machine-readable and should be changed deliberately.

When a contract changes, update the corresponding reference documentation and compatibility evidence.
