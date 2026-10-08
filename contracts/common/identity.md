# Canonical Identity Context

Cross-system requests/events MUST carry enough context to establish actor, tenant, trace, and causality where applicable.

Canonical fields:
tenant_id, organization_id, workspace_id, actor_id, agent_id, service_id, execution_id, trace_id, correlation_id, causation_id.

A system MUST NOT silently replace a caller's tenant or authorization context. Agent Platform remains authoritative for execution-time authorization.
