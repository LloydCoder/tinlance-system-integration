# FCP-03 Control-to-Test-to-Evidence Traceability

**Snapshot:** 2026-11-11  
**Disposition:** FCP-03 ACTIVE / INCOMPLETE; FCP-04–FCP-10 GATED  
**Canonical strategy:** [FCP-03 Provider-Neutral Closure Strategy](FCP-03-PROVIDER-NEUTRAL-CLOSURE-STRATEGY.md)  
**Programme tracker:** [TSIC issue #102](https://github.com/LloydCoder/tinlance-system-integration/issues/102)

This register maps the adopted closure strategy to repository implementation, test harnesses and evidence classes. It deliberately distinguishes implementation and CI qualification from deployed production evidence. Paths are relative to `LloydCoder/tinlance-agent-platform` unless stated otherwise.

## Evidence scale

- **E0:** design/specification only.
- **E1:** static or repository-level tests.
- **E2:** ephemeral CI integration.
- **E3:** controlled-host evidence.
- **E4:** production-equivalent deployed evidence with operational telemetry and recovery.
- **E5:** independent assessor evidence and signed dispositions.

The highest evidence level listed is the highest substantiated by the current repository and audit record, not the target level.

## Control traceability

| Workstream / control | Implementation or contract | Tests / workflows | Current substantiated evidence | Missing exit evidence |
|---|---|---|---|---|
| A. Programme governance | TSIC strategy; Platform issue #275; five-repository default-branch policy | Exact repository workflow inventory; branch/ruleset read-back still required | E0–E2; current live inventory shows all five default branches reported unprotected in prior audit | Active rulesets, exact required contexts, bypass restriction and read-back on all five repositories |
| B. Browser hostname authorization | `packages/sandbox/src/tinlance_agent_platform_sandbox/egress_proxy.py`; browser egress policy | `tests/unit/test_browser_egress.py`; `tests/unit/test_browser_egress_network.py`; browser W3/W4 workflows | E1–E2 | Production network enforcement independent of proxy; deployed policy and operational evidence |
| B. DNS and packet enforcement | `scripts/fcp03_linux_dns_egress_lab.sh`; `scripts/fcp03_namespace_enforcement_probe.sh`; Linux qualification workflow | `.github/workflows/fcp03-linux-dns-egress.yml`; hosted Linux namespace/DNS/nftables adversarial suite; fixed script re-run on three existing SSM-managed test hosts (ARM64 and x86_64) on 2026-11-11 | E2 plus E3 controlled-host evidence: the fixed two-namespace DNS/nftables/TLS lab passed on `tinlyt-test-runtime`, `tinlyt-api-production` and the FusionOps/ThreatFade host. UDP/TCP DNS, NXDOMAIN, TLS hostname validation, direct DNS, DoH, DoT, QUIC, metadata, rebinding and IPv6 checks passed; aggregate drop counter 8 on each host; host firewall/routes and Docker state unchanged; temporary resources/packages cleaned. PR #295 fixed a `pipefail`/SIGPIPE readiness race and merged as `889ee771c81c3526ce0cc5778b5de7e5eae3bee4`; exact-head workflows 14/14 passed. SSM commands `d064043c-6bce-4d40-b564-eb9450cf9a08`, `a22073a0-7e6e-43ab-ba93-ecea789c4960`, `64890655-d98c-4da4-9d8b-e76f0cac4898`; see [expanded existing test-infrastructure evidence](FCP-03-EXISTING-TEST-INFRASTRUCTURE-EVIDENCE-2026-11-11.md). | Approved production-equivalent deployment, packet/flow evidence from the selected E4 environment, policy attribution, tenant non-interference and operational failure/recovery evidence |
| B. Historical AWS deployment candidate | `infra/aws/fcp03-dns-firewall-lab/`, `infra/aws/fcp03-egress-lab/`, ADR-018 | `tests/unit/test_fcp03_dns_firewall_lab_template.py`, `tests/unit/test_fcp03_cloudformation_template.py`, `tests/unit/test_fcp03_egress_preflight.py` | E1 only; no AWS stack deployment is claimed | Not required as AWS specifically; any selected provider-neutral equivalent must satisfy the same control outcome at E4 |
| C. Workload identity and proof | `packages/identity/src/tinlance_agent_platform_identity/` including DPoP, JWT verifier, federation, token security and revocation | `tests/test_identity_dpop.py`, `tests/test_identity_dpop_binding.py`, `tests/test_identity_jwt.py`, `tests/test_identity_resolver.py`, `tests/test_identity_service_tokens.py` | E1–E2 | Dedicated deployed issuer/JWKS, real workload trust, measured rotation/revocation propagation, outage and recovery evidence |
| C. External secrets | `packages/secrets/src/tinlance_agent_platform_secrets/openbao.py`; `docs/FCP-03-OPENBAO-SECRET-PROVIDER.md` | `tests/test_openbao_secret_provider.py`; `tests/test_openbao_secret_provider_integration.py`; `.github/workflows/fcp03-openbao-integration.yml` | E1–E2 against disposable OpenBao dev server and least-privilege test token | Production HA/seal/unseal, workload identity, TLS, audit delivery, key rotation, backup/restore, revocation and operator ownership |
| D. Runtime isolation | `packages/sandbox/src/tinlance_agent_platform_sandbox/` including Bubblewrap, browser, exec guard, supervisor and host capability checks | `tests/unit/test_sandbox_host_capabilities.py`, browser W3/W4, Firecracker jailer/guest boot and gVisor/Kata qualification workflows; 2026-11-11 live host capability probe | E1–E3; `tinlyt-test-runtime` has cgroup v2, user namespaces, Bubblewrap and nftables, but no KVM/Firecracker/gVisor/Kata device/runtime; the SSM process did not have an active seccomp filter and AppArmor was unavailable. It remains a controlled test runner only. | Approved production-equivalent host, provider/firmware trust and attestation, selected isolation boundary, sustained adversarial soak, resource ceiling and independent review |
| E. Transactional durability | `database/migrations/014_p10_workspace_leases.sql`, `015_workspace_restore_ledger.sql`; durability package | `tests/test_postgres_outbox_publisher.py`, `tests/test_postgres_restore_ledger.py`, `tests/test_postgres_snapshot_catalog.py`, `tests/test_postgres_workspace_leases.py`; PostgreSQL 17 CI service and disposable host run; existing PostgreSQL 16.15 test service validation | E1–E3; PostgreSQL 17: all 16 migrations, all 13 SQL acceptance scripts and both live adapter tests (2/2) passed. PostgreSQL 16.15: all 16 migrations and 12/13 SQL scripts passed in a disposable database; the concurrency script was intentionally skipped because its hard-coded `dbname=postgres` target would hit the shared service DB. A separate disposable custom-format dump/restore recovered all 34 platform tables, 26 platform functions and a seeded tenant row; source/target DBs were dropped and no test roles remained. | Deployed production-equivalent DB/queue, independent encrypted backup, clean isolated restore, measured RPO/RTO, operational recovery owner |
| F. Telemetry and incident correlation | `packages/observability/src/tinlance_agent_platform_observability/`; M13.8 contract | `tests/test_observability_otel.py`, `tests/test_m13_8_observability.py` | E1–E2 | Live collector/exporters, durable retention, dashboards, verified alert delivery, observed SLO windows, incident exercises and named on-call ownership |
| G. Independent security assurance | `security/M4-RUNTIME-THREAT-MODEL.md`, `security/M7-SANDBOX-THREAT-MODEL.md`, `tests/test_m29_independent_assurance.py`; ASVS 5.0 assessment basis | Repository certification tests are internal engineering evidence only | E0–E1 | Independent assessor engagement, scope, source/config review, signed findings, critical remediation, retest and risk acceptance |

## Repository and workflow evidence boundaries

The following existing workflows provide useful repeatable qualification but are not substitutes for production deployment:

- `FCP-03 Linux DNS and Egress Qualification` — isolated hosted Linux namespace, resolver and nftables mechanics.
- `FCP-03 OpenBao Secret Provider Integration` — disposable development server, tenant-scoped KV policy and adapter integration.
- PostgreSQL 17 ephemeral integration tests — outbox, snapshot catalog, restore ledger and tenant RLS behavior.
- Browser W3/W4 and Firecracker/gVisor/Kata workflows — CI/hosted-runner feasibility and adversarial regression evidence.

Workflow success must be bound to exact commit SHA, workflow run, artifact digest, environment and test scope. A workflow name alone is not evidence.

## Exit readiness matrix

| Exit criterion | Current disposition | Minimum next proof |
|---|---|---|
| All five core repos have enforced branch governance | **BLOCKED** | Admin-applied rulesets and API read-back; issue #275 |
| Network/DNS destination enforcement | **PARTIAL — E2/E3 only** | Approved E4 deployment and adversarial packet/flow evidence |
| Identity, proof, key custody and revocation | **PARTIAL — E1/E2** | Deployed issuer/secret service and measured rotation/revocation |
| Runtime/host isolation | **PARTIAL — E1/E3** | Approved host, production-equivalent isolation and independent assessment |
| Durable DB/outbox/backup/restore | **PARTIAL — E2** | Deployed topology, independent backup, clean restore, measured RPO/RTO |
| Observability and operations | **PARTIAL — E1/E2** | Live telemetry, alert receipts, SLOs, runbooks, exercises, named owners |
| Independent assessment | **NOT STARTED / NOT EVIDENCED** | Independent assessor report and retest |
| Formal FCP-03 acceptance | **NOT ACCEPTED** | TSIC evidence review and programme-owner go/no-go |

## Ordered execution queue

1. A — governance and evidence reconciliation; obtain ruleset administration path.
2. B — provider-neutral network/DNS E4 environment and adversarial evidence.
3. C — production workload identity, external secrets and revocation.
4. D — approved runtime/host, isolation, sustained tests and attestation.
5. E — durable services, independent backup and measured restore.
6. F — live telemetry, SLOs, verified alerting and incident exercises.
7. G — independent assessment, findings, retests and formal FCP-03 acceptance.
8. Unlock FCP-04 only after step 7 is formally accepted; continue FCP-05 through FCP-10 strictly serially.

## Explicit blockers

- No approved production-equivalent zero-incremental-AWS-spend environment has been evidenced. The 2026-11-11 all-region read-only inventory found 0 AWS Network Firewall deployments, 0 Route 53 Resolver DNS Firewall rule groups and 0 associations across 17 enabled regions.
- The three SSM-managed instances used for E3 tests are controlled test hosts, not approved Agent Platform production workloads. The programme owner designated them as test instances, but AWS names/tags still label the Tinlyt API and FusionOps/ThreatFade hosts as production; reconcile this asset metadata before using it as evidence of production-equivalent status.
- The connected GitHub tool exposes repository read operations and PR/file writes, but no repository-administration ruleset mutation action. The account collaborator permission is admin, yet this integration cannot perform the ruleset write/read-back needed for closure.
- Independent assessor participation and signed assurance artifacts are not present.
- No live production deployment or measured operational RPO/RTO/alert-delivery evidence has been supplied.

**No control is marked E4 or E5 in this register.** This is intentional: current evidence supports repository/ephemeral/controlled-host qualification, not production-equivalent deployment or independent assurance.
