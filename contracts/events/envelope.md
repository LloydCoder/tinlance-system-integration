# Event Contract Baseline

Tinlance events should use CloudEvents-compatible metadata plus Tinlance correlation metadata and a domain payload.

Minimum integration metadata:
event identity, event type/version, source, subject, event time, tenant context, trace/correlation context, causation where applicable, schema reference, domain payload.

Transport is intentionally not fixed in Phase 0.
