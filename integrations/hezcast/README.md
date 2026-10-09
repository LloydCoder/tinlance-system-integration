# HezCast TSIC Integration

HezCast Engine is pinned to `f658308b982e4f5a790fc367fe7483c16cc632c3` for this reviewed integration baseline. HezCast owns content generation and package validation; it does not own generic execution authority or external publishing authorization.

Publishing to Telegram or other external platforms is a consequential side effect and must pass through Agent Platform with verified tenant context, scoped short-lived credentials, policy/approval checks, idempotency, and audit evidence. Do not expose provider credentials to browser clients or let content-generation success imply publication authorization.

The canonical adapter is `adapter.json`. TSIC owns the integration contract and certification record.
