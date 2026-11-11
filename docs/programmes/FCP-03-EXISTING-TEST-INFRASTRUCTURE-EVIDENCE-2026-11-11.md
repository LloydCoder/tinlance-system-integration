# FCP-03 Existing Test-Infrastructure Validation Evidence

**Execution date:** 2026-11-11  
**Agent Platform source:** `889ee771c81c3526ce0cc5778b5de7e5eae3bee4` (PR #295 merge; fixed lab script)  
**TSIC traceability base:** `8fd1a059fdb79dddd67195590ae315479fe6f3f7`  
**Disposition:** E3 controlled-host evidence only; FCP-03 remains ACTIVE / INCOMPLETE.

## Scope and safety boundary

The initial validation used the existing EC2 instance `tinlyt-test-runtime` (`i-0bdb9c7cb13b1c9b8`, `eu-west-1`, `t4g.medium`, Amazon Linux 2023, ARM64) through Systems Manager. Following the programme-owner instruction to use all existing test instances, the same isolated namespace lab was subsequently run on the existing Tinlyt API and FusionOps/ThreatFade SSM-managed hosts. No EC2, VPC, subnet, route-table, security-group, IAM, Network Firewall, DNS Firewall, KMS, S3, NAT or other AWS resource was created or modified.

No application process, product data, shared VPC, shared database or existing W5 PostgreSQL container was modified. AWS resource names/tags on two of the hosts still contain `production` labels despite the programme owner's test-instance designation; this asset metadata discrepancy is recorded below and should be reconciled.

The host initially had nftables, iproute2, Bubblewrap, Docker, OpenSSL and Python. The small Amazon Linux package `dnsmasq 2.90` was installed to run the existing repository lab; the system dnsmasq service remained inactive. The lab's own cleanup verified that temporary namespaces, veths, processes and files were removed.

## Network and DNS enforcement lab

Exact source: `scripts/fcp03_linux_dns_egress_lab.sh`  
Exact source commit: `fab182b6c3083c024cde1ec6fd63366b7750ca61`  
SSM command: `63d97f53-f9a5-4a30-956c-76238282cc86`  
Result: **PASS**

The repository script created two temporary network namespaces connected by a private veth pair. The worker's default route terminated at the isolated resolver namespace; the resolver had no default route and forwarding disabled.

Observed controls:

- Allowed DNS queries passed over UDP and TCP.
- Blocked DNS names returned NXDOMAIN.
- DNS rebinding and metadata names were resolved as test cases, then independently blocked at the packet layer.
- Approved local HTTPS passed certificate-chain and hostname validation.
- Direct DNS UDP/TCP, direct-IP HTTPS/DoH, DoT/TCP 853, QUIC/UDP 443, metadata destination and the rebinding destination were blocked.
- IPv6 egress was blocked by nftables.
- IPv4/aggregate output drop counter: 8 packets; IPv6 drop counter: 7 packets.
- Resolver query logs correlated the positive and negative DNS test names.
- Host nftables rules, IPv4/IPv6 default routes and existing Docker container state were unchanged.
- Temporary network namespaces and veth interfaces were removed.

The script itself emitted:
`FCP03_LINUX_DNS_EGRESS_INTEGRATION=PASS`,
`FCP03_HOST_FIREWALL_AND_ROUTES_UNCHANGED=PASS`,
`FCP03_EXISTING_DOCKER_STATE_UNCHANGED=PASS`,
`FCP03_TEMPORARY_RESOURCES_CLEANED=PASS`,
`AWS_NETWORK_FIREWALL_ACCEPTANCE=NOT_TESTED`,
`PRODUCTION_ACCEPTANCE=NOT_TESTED`.

This is a controlled-host Linux enforcement result. It does not prove AWS Network Firewall, Route 53 DNS Firewall, a deployed production egress boundary, cross-tenant production isolation or independent assurance.

## Runtime and host capability probe

The host exposes cgroup v2, user namespaces, Bubblewrap, nftables and Docker. It does not expose KVM or a usable Firecracker microVM path; gVisor/Kata runtime binaries were not present. AppArmor was unavailable. Seccomp filtering support was detected, but the SSM diagnostic process itself did not have an active seccomp filter. This is not a provider attestation or production host-trust statement.

## PostgreSQL durability qualification

A disposable PostgreSQL 17 container was run on an internal-only Docker network with an ephemeral data filesystem and resource limits. The test applied all 16 current migrations and executed all 13 SQL acceptance scripts. The host connected to the container over its isolated Docker bridge and ran `tests/integration/test_postgres_durability_live.py`: **2 passed**.

The temporary container and Docker network were removed automatically. The existing `tinlance-w5-postgres` container and its database were not used or modified.

## Current-main quality evidence

On the exact Agent Platform source commit above:

- Full Python suite: **1,083 passed, 5 skipped, 8 subtests passed**.
- Total package coverage: **85.65%**, above the 85% gate.
- `compileall`, Ruff lint, Ruff format (406 files), mypy (140 source files) and `pip check` passed.
- Supplemental `pip-audit` against the reused test-runner environment reported no known vulnerabilities. This is not a substitute for a clean CI dependency resolution.
- CycloneDX generated an environment SBOM with 73 components.
- The five full-suite skips included the two live PostgreSQL tests (subsequently run and passed separately) and three OpenBao service tests. The merged Agent Platform PR #291 records successful disposable OpenBao integration and six successful post-merge workflows.

## Live AWS topology boundary

Read-only inventory of the test-host VPC showed a public-address/default-internet-route configuration, broad instance security-group egress and an enabled IMDSv2 endpoint. No Network Firewall, Route 53 DNS Firewall association or VPC endpoint was present in the inspected VPC/regions. The existing test host is therefore a controller/test runner, not a production worker or production-equivalent cloud egress boundary.

The existing account-wide inventory recorded in TSIC issue #102 remains: 17 enabled regions, zero Network Firewall deployments and zero Route 53 Resolver DNS Firewall associations.

## Evidence classification and remaining acceptance

**Highest evidence level: E3. No E4 or E5 evidence is created by this run.**

Still required for FCP-03:

1. Approved production-equivalent environment and deployed network/DNS enforcement with operational packet/flow evidence.
2. Deployed workload identity, live issuer/JWKS verification, key custody, rotation and measured revocation.
3. Approved host/runtime trust, selected isolation boundary, sustained adversarial soak and independent review.
4. Production durability services, independent encrypted backup, clean restore and measured RPO/RTO.
5. Live telemetry, verified alert delivery, SLO windows, incident exercises and named operations ownership.
6. Active branch rulesets and read-back across all five core repositories.
7. Independent assessor scope, signed findings, remediation retest and risk acceptance.

**FCP-03 remains ACTIVE / NOT ACCEPTED. FCP-04–FCP-10 remain serially gated.**


## Expanded existing-infrastructure validation — 2026-11-11 follow-up

### Scope update and asset inventory

Following the initial run, the programme owner explicitly directed use of the existing test instances. The fixed FCP-03 namespace lab was executed on all three SSM-managed instances:

| Existing host | EC2 instance | Architecture | SSM command | Result |
|---|---|---|---|---|
| `tinlyt-test-runtime` | `i-0bdb9c7cb13b1c9b8` | ARM64 | `d064043c-6bce-4d40-b564-eb9450cf9a08` | PASS |
| `tinlyt-api-production` | `i-0dc730ed647b24ab5` | x86_64 | `a22073a0-7e6e-43ab-ba93-ecea789c4960` | PASS |
| FusionOps / ThreatFade host | `i-0bfd1525cdf71dd28` | x86_64 | `64890655-d98c-4da4-9d8b-e76f0cac4898` | PASS |

The standalone EC2 instance named/tagged for ThreatFade is not SSM-managed and has no instance profile. No SSH channel was used or provisioned, so no command was run on that instance. The ThreatFade service running on the FusionOps host was included in the health and post-test checks.

**Asset metadata discrepancy:** the programme owner identified these systems as test instances, but AWS resource names/tags still describe the Tinlyt API host and FusionOps/ThreatFade host as production. The lab used only isolated temporary namespaces and temporary packages; no product service, data, VPC, security group, route table, instance profile or production application configuration was changed. The metadata should be reconciled in the asset register so that test designation and cloud labels agree.

### DNS/egress lab defect and correction

The first run on the FusionOps/ThreatFade host exposed an intermittent exit status 141. The cause was a `dig | grep -q` readiness pipeline under `set -o pipefail`: grep could close the pipe after matching and cause the producer to exit with SIGPIPE.

Agent Platform PR [#295](https://github.com/LloydCoder/tinlance-agent-platform/pull/295) changed the readiness loop to capture the complete DNS answer before comparing it and added a regression test. The regression test was demonstrated RED against base `fab182b6c3083c024cde1ec6fd63366b7750ca61`, then GREEN on the corrected branch. The PR merged as `889ee771c81c3526ce0cc5778b5de7e5eae3bee4`; exact PR-head workflows passed **14/14**.

The fixed script at PR head `0de72385e8920cde0a952fa4a9a0bb388e3ea0aa` then passed on all three SSM-managed hosts. On every host:

- DNS allowlist passed over UDP and TCP; blocked name returned NXDOMAIN.
- Approved local HTTPS passed certificate-chain and hostname validation.
- Direct DNS UDP/TCP, DoH endpoint IP/TCP 443, DoT/TCP 853, QUIC/UDP 443, metadata destination and DNS-rebinding destination were blocked.
- IPv6 egress was blocked; IPv6 drop counters were 6–7 packets; aggregate output drop counter was 8 packets.
- Resolver query-log correlation passed.
- Host firewall/default routes and Docker state were unchanged.
- Temporary namespaces/veths and test packages were cleaned.

The lab emitted `AWS_NETWORK_FIREWALL_ACCEPTANCE=NOT_TESTED` and `PRODUCTION_ACCEPTANCE=NOT_TESTED`. These remain E3 controlled-host results, not AWS firewall or E4 evidence.

### Existing application health and host boundary

On the FusionOps/ThreatFade host, `fusionops.service` and `threatfade.service` remained active with `NRestarts=0` after the lab. Their local health endpoints returned HTTP 200. A peer-host connectivity probe found the database port 5432 and API ports 8000/8080 unreachable from the other private host; HTTP port 80 was reachable. This is a narrow reachability observation only, not a tenant-isolation certification.

### PostgreSQL 16.15 compatibility and recovery drill

The existing PostgreSQL 16.15 service on `tinlyt-api-production` was used only with disposable databases. The shared `postgres` database was not modified.

- Created a disposable database, applied all **16 migrations**, and ran **12 of 13** SQL acceptance scripts successfully.
- The P8 concurrency script was deliberately skipped because it hard-codes a dblink connection to `dbname=postgres`; running it unchanged would have exercised the shared service database rather than the disposable database.
- No test roles remained after the disposable database was dropped.
- A separate custom-format dump/restore drill created a disposable source DB, applied all 16 migrations, seeded one tenant row, dumped **198,118 bytes**, restored into a second disposable DB and verified **34 platform tables**, **26 platform functions** and the tenant row.
- Both source and target databases were dropped. PostgreSQL remained accepting connections.

This is E3 local PostgreSQL compatibility and logical dump/restore evidence. It is not an independent encrypted backup, off-host retention, point-in-time recovery, cross-AZ/region restore, or measured production RPO/RTO.

### Full suite and security/governance inventory

On the fixed DNS-lab branch head:

- Full Python suite: **1,084 passed, 5 skipped, 8 subtests passed** in 57.59 seconds.
- Regression test: 1 passed; Ruff check/format and shell syntax passed.
- The 5 skips were two live PostgreSQL adapter tests without a configured test URL and three OpenBao service tests without a configured local service. The PostgreSQL adapter tests had passed separately against the disposable PostgreSQL 17 container in the earlier section; the merged OpenBao integration workflow remains the E2 evidence for that adapter.

Read-only AWS inventory was repeated across **17 enabled regions**: 0 Network Firewall deployments, 0 Route 53 Resolver DNS Firewall rule groups and 0 associations. The three SSM instance profiles each trust EC2 and attach only `AmazonSSMManagedInstanceCore`; no dedicated FCP-03 workload identity role exists. The only account OIDC provider returned by IAM inventory is the GitHub Actions provider, not an Agent Platform workload issuer.

### Cleanup verification

After validation:

- All three hosts had zero FCP-03 network namespaces.
- Temporary dnsmasq packages were absent; temporary nftables packages were absent on the two x86_64 hosts. The pre-existing nftables package on `tinlyt-test-runtime` was retained.
- The only running Docker container on `tinlyt-test-runtime` remained the pre-existing `tinlance-w5-postgres`; no FCP-03 Docker network or container remained.
- The disposable OpenBao container, network and pulled image were removed after its local integration setup was not completed.
- PostgreSQL 16 disposable databases were dropped; the service remained healthy.
- FusionOps and ThreatFade services remained active with no restart-count increase.

No AWS resource was created. No VPC, route table, security group, IAM role/profile, DNS resolver association, Network Firewall, KMS, S3, NAT, application service or shared database configuration was modified.

### Updated disposition

The expanded test-infrastructure work strengthens E3 evidence for DNS/packet mechanics, host-safe execution and PostgreSQL 16 compatibility/recovery. It does **not** create E4/E5 evidence. FCP-03 remains ACTIVE / NOT ACCEPTED; FCP-04–FCP-10 remain serially gated.
