# Tinlance Web Intelligence integration boundary

## Authority model

Tinlance Web Intelligence (TWI) is the web acquisition subsystem. It owns web search and fetch,
isolated browser capture, source evidence acquisition, and web-source change monitoring. It is not
an execution authority, identity provider, policy engine, MCP authority, or temporal world model.

- **Agent Platform** owns caller identity, authorization, risk policy, human approval, execution,
  budgets, audit, and the authoritative MCP surface.
- **TWI** performs policy-bounded acquisition and emits source-backed candidate evidence.
- **World Intelligence** validates and ingests candidate evidence, then owns canonical entity/event/
  relationship resolution, temporal world state, cross-source correlation, and world-level signals.
- **TSIC** owns the cross-repository contract, registry, dependency graph, and conformance gate.

## Registered flow

1. Agent Platform invokes TWI through a governed HTTPS adapter. It mints a short-lived TWI-audience
   token for the authenticated tenant and subject; the inbound MCP bearer token is never passed
   through to TWI.
2. TWI searches, fetches, or captures a source in an isolated worker and retains source provenance.
3. Citation verification checks that a quoted excerpt matches an authorized captured artifact. It
   does not claim that the statement is objectively true.
4. Source-evidence export is a consequential Platform operation. The Platform must require a
   human approval bound to tenant, run, action, resource, exact intent fingerprint, and an
   idempotency key before dispatch.
5. TWI sends the versioned twi-source-evidence-intake envelope to World Intelligence. World
   Intelligence stores it as candidate evidence; the intake operation does not create canonical
   world state.
6. TSIC validates the system registration, authority boundaries, adapter direction, contract
   version, and TSIC-16 interoperability scope.

## Contract invariants

- The intake schema is closed (additionalProperties: false) and requires source identity,
  tenant reference, source job, source URL, retrieval time, media type, artifact digest, quote
  digest, verifier version, and report digest.
- Source URLs must be redacted before storage. Credentials and sensitive query values are rejected.
- The World Intelligence intake uses a dedicated source-evidence service credential, separate from
  its query API token.
- Idempotency is scoped by tenant. Replays with the same key and different payloads conflict.
- TWI does not own canonical entities, events, relationships, temporal world state, or identity.
- TWI tool definitions do not bypass the Platform's approval verifier or execution evidence.

Run python3 scripts/certify_twi_integration.py to validate the local registry and contract
invariants. The repository CI runs this certification in addition to the existing TSIC gates.
