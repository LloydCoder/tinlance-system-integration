# Model Routing and Agent Interoperability

Agent Platform is the execution authority for model routing and governed tool execution. Agent OS and domain systems may request a route but may not create an unregistered execution router. MCP and A2A are complementary interoperability protocols; neither creates an authorization bypass.

## Pinned protocol baselines

- **MCP:** `2026-07-28`, the current specification revision. [Official specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/).
- **A2A:** `1.0.0`, the released Agent2Agent protocol specification. [Official A2A specification](https://a2a-protocol.org/v1.0.0/specification/).
- Machine-readable authority gate: `contracts/agents/interoperability-gate.json`.
- Canonical version and invariant baseline: `policies/interoperability-baseline.json`.

MCP standardizes agent-to-tool and context integration; A2A standardizes communication and task delegation between independent agents. A system may support one or both, but support is not itself a grant of capabilities or permission.

## Enterprise security invariants

- Identity, tenant context, authorization, policy, approval, budgets, sandboxing, and consequential execution remain under Agent Platform authority.
- Capabilities are explicitly registered and versioned. Discovery metadata is untrusted input and must not be treated as authorization.
- Remote delegation is scoped, expiring, auditable, and constrained by the caller's authority. Delegation cannot amplify privileges.
- Tool arguments, remote agent messages, resource content, and returned artifacts are untrusted data.
- Trace context and evidence lineage survive protocol boundaries; duplicate requests and replay are handled idempotently.
- Remote calls use authenticated transport, bounded timeouts and response sizes, and explicit failure handling.
- TSIC owns ecosystem contract and compatibility certification; it does not become a second execution authority.

## Certification

```bash
python3 scripts/certify_interoperability.py
python3 scripts/forensic_audit_phase16.py
```

The dedicated workflow verifies version pins, authority assignments, delegation controls, and negative cases. It certifies TSIC contract conformance, not full certification of every third-party MCP or A2A implementation.
