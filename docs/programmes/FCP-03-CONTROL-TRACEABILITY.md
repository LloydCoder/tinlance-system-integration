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
| A. Programme governance | TSIC strategy; Platform issue #275; ruleset `fcp03-default-branch` on each core repository | API read-back of ruleset objects and `GET /rules/branches/main` on 2026-11-11 | E2 repository-administration evidence. All five default branches now evaluate `deletion`, `non_fast_forward`, `pull_request` and strict `required_status_checks`. Ruleset IDs: Platform `27050541` (13 contexts), Agent OS `27050544` (7), SDK `27050546` (6), TADL `27050548` (5), TSIC `27050549` (32). Enforcement `active`. `bypass_actors` empty. Classic branch `protected` flag read back `true`. Prior same-day audit had found them unprotected; this read-back supersedes that finding. | Independent approving review. Required approving review count is 0 because the only collaborator on each repository is `LloydCoder`; a count of 1 would be an unsatisfiable solo-maintainer gate. CODEOWNERS review is not enabled. No second reviewer exists. |
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
| All five core repos have enforced branch governance | **PARTIAL — rulesets active, review gate open** | Second independent reviewer before approving-review count can be raised above 0; issue #275 stays open for that residual |
| Network/DNS destination enforcement | **PARTIAL — E2/E3 ephemeral only** | A non-shared host or path where default-deny DNS/egress survives reboot and fails closed. The existing shared SSM hosts cannot hold that boundary without disrupting co-resident services. See [FCP-03-NETWORK-PERSISTENCE-FEASIBILITY-2026-11-11.md](FCP-03-NETWORK-PERSISTENCE-FEASIBILITY-2026-11-11.md). No persistent policy was installed. |
| Identity, proof, key custody and revocation | **PARTIAL — E1/E2** | Deployed issuer/secret service and measured rotation/revocation |
| Runtime/host isolation | **PARTIAL — E1/E3** | Approved host, production-equivalent isolation and independent assessment |
| Durable DB/outbox/backup/restore | **PARTIAL — E2** | Deployed topology, independent backup, clean restore, measured RPO/RTO |
| Observability and operations | **PARTIAL — E1/E2** | Live telemetry, alert receipts, SLOs, runbooks, exercises, named owners |
| Independent assessment | **NOT STARTED / NOT EVIDENCED** | Independent assessor report and retest |
| Formal FCP-03 acceptance | **NOT ACCEPTED** | TSIC evidence review and programme-owner go/no-go |

## Ordered execution queue

1. A — rulesets are active and read back. Remaining governance work is an independent approving reviewer, not ruleset administration.
2. B — blocked on a non-shared persistent fail-closed path. Do not install host-wide policy on the current SSM hosts. Ephemeral namespace evidence stays E3.
3. C — production workload identity, external secrets and revocation.
4. D — approved runtime/host, isolation, sustained tests and attestation.
5. E — durable services, independent backup and measured restore.
6. F — live telemetry, SLOs, verified alerting and incident exercises.
7. G — independent assessment, findings, retests and formal FCP-03 acceptance.
8. Unlock FCP-04 only after step 7 is formally accepted; continue FCP-05 through FCP-10 strictly serially.

## Explicit blockers

- No approved production-equivalent zero-incremental-AWS-spend environment has been evidenced. The 2026-11-11 all-region read-only inventory found 0 AWS Network Firewall deployments, 0 Route 53 Resolver DNS Firewall rule groups and 0 associations across 17 enabled regions. That inventory was not repeated in the persistence feasibility pass: this execution had no AWS credentials.
- A persistent fail-closed DNS/egress boundary was not installed. Host-wide firewall, security-group, or NACL changes on the three existing SSM hosts would affect co-resident services (including `tinlance-w5-postgres`, and the production-labelled Tinlyt API and FusionOps/ThreatFade hosts) and can strand SSM. The repository lab deletes its namespaces on exit by design. A namespace-only systemd unit would not govern other processes and was not deployed. Details: [FCP-03-NETWORK-PERSISTENCE-FEASIBILITY-2026-11-11.md](FCP-03-NETWORK-PERSISTENCE-FEASIBILITY-2026-11-11.md).
- The three SSM-managed instances used for E3 tests are controlled test hosts, not approved Agent Platform production workloads. The programme owner designated them as test instances, but AWS names/tags still label the Tinlyt API and FusionOps/ThreatFade hosts as production; reconcile this asset metadata before using it as evidence of production-equivalent status.
- Repository administration was available through the authenticated owner credential in this execution. Active rulesets were created and read back. See the governance read-back section below. This does not close independent review.
- Independent assessor participation and signed assurance artifacts are not present. The implementing agent must not certify this work as independently assessed.
- No live production deployment or measured operational RPO/RTO/alert-delivery evidence has been supplied.

**No control is marked E4 or E5 in this register.** This is intentional: current evidence supports repository/ephemeral/controlled-host qualification, not production-equivalent deployment or independent assurance.

## Governance read-back — 2026-11-11

The following was read back from the GitHub API after ruleset creation. It is repository-administration evidence (E2), not production-network, identity, runtime, recovery, or independent-assurance evidence.

| Repository | Ruleset | Enforcement | Bypass actors | Required PR contexts | `main` protected |
|---|---:|---|---|---:|---|
| `LloydCoder/tinlance-agent-platform` | 27050541 | active | none | 13 | true |
| `LloydCoder/tinlance-agent-os` | 27050544 | active | none | 7 | true |
| `LloydCoder/tinlance-agent-platform-sdk` | 27050546 | active | none | 6 | true |
| `LloydCoder/tinlance-agent-developer` | 27050548 | active | none | 5 | true |
| `LloydCoder/tinlance-system-integration` | 27050549 | active | none | 32 | true |

Every ruleset targets `~DEFAULT_BRANCH` and includes deletion denial, non-fast-forward denial, pull request required, stale-review dismissal, conversation resolution, and strict required status checks. `GET /repos/{owner}/{repo}/rules/branches/main` returned exactly those four rule types on each repository.

Required contexts are only checks whose workflows run on every pull request to `main`. Path-filtered workflows are not required, because GitHub would otherwise wait forever on pull requests that do not touch those paths. That includes the FCP-03 Linux DNS/egress lab, the OpenBao integration, CloudFormation cfn-lint/Checkov, and the persistent-computer suites. Supply-chain attestation jobs that run only on push to `main` are also not PR-required. TSIC Scorecard does not run on pull request, so it is not required; Agent OS `Scorecard analysis` does run on pull request and is required. Two TSIC workflows both publish the check name `observability`, so a ruleset cannot distinguish them.

Secret scanning and push protection were already enabled. Dependabot alerts and Dependabot security updates were enabled on all five repositories during this change. A same-time read returned 0 open Dependabot alerts; that is not a claim that dependency risk is zero. A settings patch requested secret-scanning validity checks and non-provider patterns; the subsequent read-back still showed both disabled, so they are not claimed as enabled.

No AWS API credential was present in the execution environment. No AWS resource was created or modified.

**FCP-03 remains ACTIVE / NOT ACCEPTED.** Ruleset activation does not satisfy network, identity, runtime, recovery, observability, or independent-assessment exit criteria. FCP-04 remains gated.
