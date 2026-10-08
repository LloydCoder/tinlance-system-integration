# Event, Delivery and Trace Fabric

TSIC uses a CloudEvents-compatible envelope for domain events, W3C Trace Context for distributed tracing and OpenTelemetry semantic conventions for telemetry. CloudEvents 1.0.2 is the current released core specification; W3C Trace Context standardizes propagation of tracing context; OpenTelemetry provides the telemetry API/SDK/data model and semantic conventions. Durable event publication requires an outbox; consumers require idempotency and replay-safe processing.

References: CloudEvents, W3C Trace Context, OpenTelemetry, AsyncAPI 3.0.0.