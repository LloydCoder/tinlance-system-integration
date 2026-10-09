# TSIC Production System-of-Systems Certification

Certification is a repository-level conformance gate, not a claim that every external production deployment is reachable from CI. TSIC-17 certifies the canonical integration control plane, contracts, registries, reference workflows, recovery matrix, ecosystem lock and repository integrity. Live environment certification remains an operational deployment concern and must consume these same contracts.

## Certification gates

1. Architecture and authority reconciliation.
2. Identity and agent registration.
3. Event, delivery and trace fabric.
4. Service, dependency and contract registry parity.
5. Model routing and MCP/A2A interoperability.
6. Adapter fabric and explicit contract ownership.
7. Economic attribution with distinct cost/revenue semantics.
8. Ecosystem lock and dependency governance.
9. Executable reference workflows.
10. Failure/replay/recovery and idempotency.
11. Unique generic consequential execution authority.
12. Evidence-bounded production claims.
13. Final forensic audit of canonical machine-readable sources and phase ordering.

## HezCast content and publishing boundary

HezCast Engine is registered as a content-generation system. Script, voice, video, captions, and post-bundle generation remain in the HezCast domain. Publishing to Telegram or any other external channel is a consequential side effect and must be mediated by Agent Platform with tenant-bound authorization, scoped credentials, policy/approval checks, idempotency, and audit evidence. The HezCast adapter does not confer publish authority on HezCast or on a commercial AaaS offer.

## Required authority model

- Agent Platform is the sole generic consequential execution authority.
- Agent OS owns workspace, environment, lifecycle, and orchestration, but cannot grant execution authority.
- FDSE owns delivery orchestration; FDE Mastery and domain systems retain domain execution semantics.
- FAS owns evidence-first analysis; FAS-Bench remains independent evaluation authority and is not a FAS runtime dependency.
- TSIC owns system-of-systems contracts, dependency graph, compatibility, conformance, and certification evidence.
- Commercial/AaaS surfaces bind to certified capabilities and cannot create a second execution authority.

## Certification commands

```bash
python3 scripts/certify_production_system.py
python3 scripts/forensic_audit_phase17.py
```

The dedicated workflow checks graph/manifest parity, authority uniqueness, the canonical TSIC-00..19 phase sequence, ecosystem lock, recovery matrix, and the post-phase audit. A green repository gate is not proof of production reachability, external deployment health, customer outcomes, regulatory certification, or revenue.
