# TSIC-18 Ecosystem Reconciliation

## Purpose

TSIC-18 is the transition from a certified TSIC control plane to executable cross-repository adoption.

### Authority law

- **TSIC** is the canonical Tinlance ecosystem integration and certification authority.
- **TADL** is the developer-plane artifact validation and evaluation consumer.
- **Agent Platform** remains the sole authority for governed execution: identity, tenancy, authorization, policy, approvals, budgets, sandbox/tool authority, secrets, execution, authoritative evidence and audit.
- **Agent OS** owns workspace, environment, lifecycle and orchestration composition, but never grants execution authority.
- **Platform SDK** is a typed transport/client surface and never authorizes.
- Domain systems retain their declared domain authority and must consume, not duplicate, platform authority.

## Baseline reconciliation

The Agent Developer ecosystem lock is a reviewed release baseline. It is not a live branch pointer. TSIC is the source of truth for ecosystem certification; TADL may consume TSIC contracts and expose developer-local conformance gates.

The four-repository agent baseline is:

1. Agent Developer — developer validation consumer.
2. Agent OS — operating environment and lifecycle plane.
3. Platform SDK — typed developer API surface.
4. Agent Platform — sole governed execution and authority plane.

## Conformance precedence

`TSIC contract → system implementation → system-local tests → cross-repository conformance → certification evidence`

A system-local green workflow does not constitute ecosystem certification.

## Integration status model

Each system must expose one of:

- `declared` — registered in TSIC but not yet cross-repository adopted.
- `contracted` — TSIC contracts are consumed by the system.
- `verified` — executable cross-repository conformance passes.
- `certified` — TSIC certification evidence is current for the reviewed baseline.
- `drifted` — previously certified baseline has changed and requires re-certification.

## Phase gates

### Gate 18.0

- authority boundaries are unambiguous;
- repository identities are canonical;
- reviewed SHAs are explicit;
- contract/version precedence is documented;
- no duplicate ecosystem integration authority is introduced.

### Gate 18.1

- reference adapter exists;
- canonical identity, tenant, event, trace, contract, idempotency, evidence and economic fields are represented;
- negative/security cases are executable;
- Agent Platform remains authoritative.

### Gate 18.2+

Each participating repository must pass its own CI plus the TSIC cross-repository gate before the next integration phase begins.

## Production-claim boundary

Passing a TSIC repository workflow proves repository-level conformance against the reviewed fixtures and contracts. It does not prove that an external production deployment is reachable, healthy or correctly configured.

## Current integration order

`Agent Platform → Platform SDK → Agent OS → Agent Developer → Agent System certification → World Intelligence → TADS → SDEA → ReconOS → FadeReach → Acquisition certification → FDSE → Engineering/FDE → Transformation → FDSE Toolkit → domain systems → economics → closed-loop intelligence → observability → MCP/A2A → production certification`
