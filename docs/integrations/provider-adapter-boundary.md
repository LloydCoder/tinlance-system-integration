# Provider Adapter Boundary Contract

Canonical ecosystem P7 adds explicit provider-adapter invariants without changing TSIC's independent TSIC-00–19 certification numbering.

The versioned contract in `contracts/models/provider-adapter-boundary.json` is schema-validated by `schemas/provider-adapter-boundary.schema.json`. It applies to model-provider adapters and is a stricter specialization of the general adapter fabric rules.

- Provider endpoint selection must come from trusted operator configuration, never untrusted task/model/event content.
- Remote connections use HTTPS; redirects and URL-embedded credentials are rejected.
- Requests and responses have finite time and byte limits and must use the declared JSON contract.
- W3C `traceparent` must be validated before forwarding; a bare trace ID is not a valid substitute.
- Credentials are injected through a provider interface and must not be persisted, logged or echoed in errors.
- Tenant and agent identifiers are not forwarded to external model providers by default.
- Retryability may be classified, but ambiguous billed or consequential operations are not automatically retried without proven idempotency.
- Adapters never grant authority. Identity, authorization, policy, approvals, budgets and consequential execution remain Platform-owned.

This contract defines required behavior; it does not prove that any live provider, production credential, secret manager, egress policy or deployment is active.
