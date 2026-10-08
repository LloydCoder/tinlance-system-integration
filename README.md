# Tinlance System Integration & Conformance (TSIC)

**The canonical integration control plane for defining, validating, and certifying interoperability across the Tinlance system-of-systems.**

TSIC is a control-plane and conformance repository. It does not replace domain runtimes, authorization engines, agent execution, or application logic.

## Canonical serial certification sequence

The authoritative ecosystem sequence is **TSIC-00 through TSIC-19**:

- TSIC-00 — Ecosystem Authority & Dependency Lock
- TSIC-01 — Tinlance Agent System E2E
- TSIC-02 — World Intelligence → TADS → SDEA
- TSIC-03 — ReconOS Integration
- TSIC-04 — FadeReach Acquisition Execution
- TSIC-05 — FAS + FAS-Bench Integration & Certification
- TSIC-06 — FDSE Engineering Route
- TSIC-07 — FDE Mastery Integration
- TSIC-08 — FDSE Toolkit / Delivery Evidence
- TSIC-09 — ThreatFade Engine
- TSIC-10 — ThreatFade Web ↔ ThreatFade Engine
- TSIC-11 — BugFlow Integration
- TSIC-12 — HEZQARA Governed Healthcare Integration
- TSIC-13 — Economic Attribution
- TSIC-14 — Closed-Loop Intelligence
- TSIC-15 — Ecosystem Observability
- TSIC-16 — MCP / A2A Interoperability
- TSIC-17 — Production System-of-Systems
- TSIC-18 — Tinlance.com Commercial & AaaS
- TSIC-19 — Autonomous Revenue Operating Loop

The previous TSIC-31–41 numbering is retained only as historical continuation/certification records; it is not the master ecosystem phase numbering.

## Authority model

- **Agent Platform** is the sole generic consequential execution authority.
- **Agent OS** owns workspace, environment, lifecycle and orchestration.
- **Agent Platform SDK** is the developer client surface and never grants authority.
- **Agent Developer** consumes governed developer capabilities.
- **TSIC** owns ecosystem contracts, registries, compatibility policy, conformance and certification evidence; it does not execute domain work.
- **FAS** is production evidence-analysis authority.
- **FAS-Bench** is independent evaluation authority and MUST NOT become a FAS runtime dependency.
- **ThreatFade Engine** is detection/analysis authority.
- **ThreatFade Web** is the product/analyst/research/commercial surface and does not replace ThreatFade Engine authority.
- **FDSE** owns delivery orchestration across both Engineering and Transformation routes.
- **FDE Mastery** owns the FDE methodology/domain execution surface.
- **Commercial/AaaS surfaces** bind to certified capabilities and do not create a second execution authority.

## Phase gate rule

A phase is complete only when implementation, cross-system execution, security and authority boundaries, failure/recovery/idempotency, evidence lineage, documentation reconciliation, dedicated CI certification, and a post-phase forensic audit are green.

Downstream phases are not certifiable until the immediately preceding phase is green.

## Verification

TSIC-00 authority lock:

```bash
python3 scripts/certify_phase0.py
```

The repository's CI additionally runs the existing conformance, recovery, security, integration, serial certification, and forensic gates.

## Canonical machine-readable sources

- `manifests/ecosystem.json` — system and authority registry
- `catalog/dependencies/graph.json` — canonical dependency graph
- `catalog/phases/registry.json` — canonical TSIC-00..19 sequence
- `policies/ecosystem-lock.json` — deny-oriented ecosystem governance
- `conformance/requirements/phase0-final.json` — TSIC-00 acceptance requirements

## Evidence and provenance

TSIC uses explicit provenance and evidence lineage rather than treating a downstream assertion as proof of an upstream event. This is aligned with the W3C PROV model of entities, activities, agents and derivations, and with modern software supply-chain provenance practices.

## Historical records

See `docs/certification/TSIC-31-41-certification-record.md` for the superseded historical numbering and its certification evidence. Do not use that numbering as the canonical phase registry.
