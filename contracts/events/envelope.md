# Event Contract Baseline

Tinlance events should use CloudEvents-compatible metadata plus Tinlance correlation metadata and a domain payload.

Canonical schema: `schemas/event-envelope.schema.json`, aligned to TADL `event-envelope/v1` and CloudEvents core 1.0.2.

Required core metadata: `specversion`, `id`, `source`, `type`, `time`, `subject`, `datacontenttype`, tenant (`tenantid`), execution (`executionid`), trace (`traceid`), correlation (`correlationid`), and JSON `data`. Optional extension attributes include `dataschema`, `causationid`, `dataclassification`, and `idempotencykey`; all extension names follow CloudEvents lowercase attribute-name rules.

Delivery is at least once, not exactly once. Durable publishers use an outbox with expiring leases, bounded retry/backoff, dead-letter and audited replay. Consumers use a durable inbox keyed by tenant, consumer, source and event ID; same identity with a different payload digest is a conflict. Journal state and outbox insertion must share one database transaction.

Transport is intentionally not fixed; do not claim a production broker deployment without direct evidence.
