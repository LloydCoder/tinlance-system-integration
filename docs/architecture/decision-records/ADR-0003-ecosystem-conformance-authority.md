# ADR-0003: Ecosystem Conformance Authority

Status: Accepted
Date: 2026-10-08

## Decision

TSIC is the canonical authority for Tinlance system-of-systems integration, cross-repository contracts, compatibility policy, ecosystem conformance requirements, and certification evidence.

The Tinlance Agent Developer Layer (TADL) remains authoritative only for its developer-plane concerns: artifact declaration, schema validation, packaging, evaluation metadata, signing/provenance primitives, and developer-facing validation.

TADL is therefore a **conformance consumer** of TSIC's ecosystem contracts. TADL may enforce stricter local invariants, but it must not redefine or contradict a TSIC ecosystem contract.

## Rationale

Two independent ecosystem conformance authorities would create competing definitions of compatibility, reviewed baselines, and certification status. That would allow a repository-local gate to pass while the canonical ecosystem gate rejects the same integration.

This decision preserves local autonomy while establishing one ecosystem-level source of truth.

## Consequences

- TSIC owns the canonical ecosystem registry and compatibility baseline.
- TADL's local conformance harness remains useful and is retained.
- TADL must consume TSIC contracts rather than publish a competing ecosystem contract.
- Future cross-repository certification records must identify both the TSIC baseline and the local repository baseline.
- A local CI pass is not equivalent to ecosystem certification.
