# Ecosystem Authority Lock

TSIC-00 is the root governance gate for the Tinlance system-of-systems. It establishes one canonical machine-readable registry for systems, repositories, authorities, dependency edges, contract versions and downstream certification gates.

## Non-negotiable invariants

1. TSIC is the ecosystem integration and certification authority, not an execution authority.
2. Agent Platform is the sole generic consequential execution authority.
3. Every system must be registered before it can participate in a canonical workflow.
4. Every dependency edge must terminate at registered systems.
5. Every registered system has a single declared governance role and explicit authority.
6. FAS-Bench remains independent from FAS production execution.
7. ThreatFade Web is distinct from the ThreatFade Engine: the engine owns detection/analysis; the web surface owns product, analyst, research and commercial presentation.
8. FDE Mastery is a first-class delivery system; FDSE remains the delivery-orchestration boundary.
9. Commercial/AaaS surfaces consume certified capabilities and never grant consequential execution authority.
10. Downstream certification is blocked until its upstream gate is green.

## Change control

Breaking contract changes require compatibility evidence. Authority changes require architecture review. New systems and repositories require registry and conformance evidence. Commercial claims require certified capability evidence.

## Provenance

Integration evidence should preserve identifiers, producer/version information, timestamps, correlation context and derivation relationships. W3C PROV is used as a conceptual interoperability reference for entities, activities, agents and derivations.

## Supply-chain integrity

CI workflows should use least-privilege permissions and immutable action references. Where third-party GitHub Actions are used, full-length commit-SHA pinning is the preferred control for immutable execution.

The machine-readable sources are manifests/ecosystem.json, catalog/dependencies/graph.json, catalog/phases/registry.json, and policies/ecosystem-lock.json.
