# Tinlance System Integration & Conformance (TSIC)

TSIC is the canonical system-of-systems integration, contract, interoperability, compatibility, conformance, verification, and certification layer for the Tinlance ecosystem.

Phase 0 establishes the repository operating model, ecosystem registry, authority model, integration boundaries, contract conventions, security/observability principles, and deterministic validation gates.

TSIC does not replace any domain system or execution runtime. It verifies that independently authoritative systems integrate correctly.

## Core principle

> Distributed implementation + explicit authority + canonical contracts + executable verification.

## Layout

- catalog/ — systems, capabilities, dependencies
- contracts/ — normative integration promises
- schemas/ — reusable machine-readable shapes
- apis/ — OpenAPI/AsyncAPI/MCP integration descriptions
- integrations/ — system-specific boundaries
- conformance/ — acceptance requirements
- compatibility/ — version compatibility policy
- manifests/ — ecosystem machine-readable control-plane metadata
- docs/ — architecture, governance, security, operations, ADRs
- tooling/ — deterministic validation

## Phase 0 gate

```bash
python3 tooling/validate_phase0.py
python3 tooling/security_scan.py
```
