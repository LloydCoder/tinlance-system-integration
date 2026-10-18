# Canonical Event Envelope — P3

The integration envelope follows the CloudEvents 1.0 JSON event format. CloudEvents required attributes are preserved as named by the specification: `specversion`, `id`, `source`, and `type`. The event timestamp is `time`; JSON content type is `datacontenttype`. Tinlance extension attributes use lowercase alphanumeric names without underscores so they remain valid CloudEvents extension names.

## Required attributes

- `specversion`: exactly `1.0`.
- `id`: non-empty producer-scoped event identifier.
- `source`: URI-reference identifying the producer context.
- `type`: stable event type name.
- `time`: RFC 3339 timestamp.
- `datacontenttype`: `application/json`.
- `tenantid`: immutable tenant scope from authenticated Platform context, never trusted from event payload.
- `executionid`: optional execution/run reference when the event concerns a governed execution.
- `traceid`: valid 32-character lowercase W3C trace identifier.
- `correlationid`: workflow/request correlation identifier.
- `data`: domain payload; always untrusted input to consumers.

Optional controlled attributes include `subject`, `dataschema`, `organizationid`, `workspaceid`, `actorid`, `agentid`, `spanid`, `causationid`, and `dataclassification`.

## Delivery semantics

- Durable publication requires an outbox row written atomically with the state transition it describes.
- Consumers persist an inbox/deduplication record in the same transaction as their business effect.
- Delivery is at-least-once, not exactly-once. Deduplicate on the pair `source + id`.
- Retries are bounded, exponentially backed off with jitter, and eventually dead-letter poison events.
- Acknowledgement happens only after the consumer transaction commits.
- Lease ownership and expiry are enforced; stale workers cannot acknowledge another worker's lease.
- Ordering is not guaranteed unless a per-aggregate ordering key is explicitly configured.
- Replay is explicit, tenant-scoped, bounded, and auditable.
- Events, payloads, metadata, model output, and event names never grant authorization or bypass Platform policy.

## Security and privacy

The Platform is the authority for tenant identity and consequential execution. Consumers must derive tenant scope from authenticated execution context, reject mismatches, validate schema and size limits, avoid logging secrets/credentials/PII unnecessarily, and treat all event data as untrusted. Trace context from untrusted callers is parsed/validated and must not be used as an authorization signal.

## Canonical schema

See `schemas/event-envelope.schema.json` and the positive/negative fixtures exercised by the TSIC CI event-contract validator.
