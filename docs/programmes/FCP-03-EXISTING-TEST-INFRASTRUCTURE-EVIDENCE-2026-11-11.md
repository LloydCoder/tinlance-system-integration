# FCP-03 Existing Test-Infrastructure Validation Evidence

**Execution date:** 2026-11-11  
**Agent Platform source:** `fab182b6c3083c024cde1ec6fd63366b7750ca61`  
**TSIC traceability base:** `fdfcfc01da1dd96398d3e57e9c29dd98f7ae6cd6`  
**Disposition:** E3 controlled-host evidence only; FCP-03 remains ACTIVE / INCOMPLETE.

## Scope and safety boundary

The programme-owner instruction was to use existing test infrastructure. Validation used the existing EC2 instance `tinlyt-test-runtime` (`i-0bdb9c7cb13b1c9b8`, `eu-west-1`, `t4g.medium`, Amazon Linux 2023, ARM64) through Systems Manager. No EC2, VPC, subnet, route-table, security-group, IAM, Network Firewall, DNS Firewall, KMS, S3, NAT or other AWS resource was created or modified.

The other product-named SSM-managed instances were only inspected non-disruptively. No application process, product data, shared VPC, shared database or existing W5 PostgreSQL container was modified.

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
