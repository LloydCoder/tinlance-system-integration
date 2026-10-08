# Agent Platform TSIC Adapter

This directory contains the canonical TSIC reference adapter contract for the Tinlance Agent Platform.

The adapter is a contract boundary, not a second runtime. Agent Platform remains authoritative for identity, authorization, policy, runtime, tools/MCP, sandbox, secrets, budgets, evidence, audit, and observability. TSIC owns only the integration contract, compatibility requirements, and certification evidence.

## Contract bindings

| TSIC contract | Agent Platform surface |
|---|---|
| identity-context | RequestContext / Principal |
| agent-registration | agent registry |
| event-envelope | events / outbox |
| delivery-semantics | idempotent consequential operations |
| trace-context | observability trace metadata |
| agent-interoperability-gate | MCP/A2A authority gate |
| economic-attribution | execution/cost attribution metadata |

## Required invariants

- The adapter never grants authority.
- Tenant context is immutable across the boundary.
- Agent Platform remains the authoritative authenticated-principal source.
- Consequential operations are idempotent.
- Trace and correlation context are preserved.
- Authoritative evidence remains Platform-owned.
