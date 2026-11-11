# FCP-03 network persistence feasibility — 2026-11-11

**Question:** Can an existing test environment hold a persistent, fail-closed DNS and egress boundary without affecting unrelated services?

**Answer:** Not on the hosts already used, and not from this execution. No persistent boundary was installed. FCP-03 remains ACTIVE / NOT ACCEPTED. This is not E4 evidence and not acceptance.

## What was checked

- The enforced lab is [scripts/fcp03_linux_dns_egress_lab.sh](https://github.com/LloydCoder/tinlance-agent-platform/blob/a530a46094bd397ae4d37399db489b140cdf0586/scripts/fcp03_linux_dns_egress_lab.sh) at Agent Platform `a530a46094bd397ae4d37399db489b140cdf0586`.
- Prior E3 runs and co-residency facts are in [FCP-03-EXISTING-TEST-INFRASTRUCTURE-EVIDENCE-2026-11-11.md](FCP-03-EXISTING-TEST-INFRASTRUCTURE-EVIDENCE-2026-11-11.md).
- This execution had no AWS CLI and no AWS credentials. GitHub Actions secret names were not readable (HTTP 403). No SSM command was sent. No host, security group, route table, or network ACL was read or modified live. The earlier 17-region inventory was not repeated.

## Why the current hosts cannot hold the boundary

The lab is deliberately ephemeral. It creates two network namespaces, applies nftables only inside the worker namespace, and deletes those namespaces on exit (`trap cleanup EXIT`). Its pass criteria require the host nftables ruleset, IPv4 and IPv6 default routes, and existing Docker state to be unchanged, and require the temporary namespaces to be gone. A passing run therefore proves the opposite of persistence: nothing remains after the process exits, and nothing survives reboot.

A persistent boundary on these machines would have to live in one of the shared enforcement points:

| Enforcement point | Persistence | Effect on unrelated services | Decision |
|---|---|---|---|
| Host nftables, routes, or firewalld | Survives reboot if saved | Shared with every process on the instance, including SSM, Docker, and co-resident products | Do not install |
| Instance security group or subnet NACL | Survives reboot | Shared with every flow from that instance or subnet, including SSM | Do not change |
| AWS Network Firewall or Route 53 DNS Firewall | Survives reboot | New billable resources; prior inventory found none deployed | Do not create |
| Extra network namespace plus a systemd unit | Survives reboot only for processes started inside that namespace | Host firewall, routes, and other processes stay unchanged if forwarding stays off and host nftables is not edited | Not installed |

Co-residency makes the first three rows disruption, not a test:

- `tinlyt-test-runtime` (`i-0bdb9c7cb13b1c9b8`) was left running the existing `tinlance-w5-postgres` container. A host-wide default-deny would cut that database off, and a mistake can also cut off SSM, which is the only management path used so far.
- The Tinlyt API host and the FusionOps/ThreatFade host still carry production names and tags. The programme forbids changing those products to obtain a green test.

The namespace-plus-systemd option would not govern the host's real egress path. Processes outside the namespace, including the existing PostgreSQL container and any product service, would remain fail-open. Calling that a host or production boundary would be false. It would also still be E3 on a test runner, not an approved production-equivalent worker. It was not installed, because this execution cannot reach SSM.

## Minimum requirement before this control can close

1. A workload host or network path that does not also carry Tinlyt, FusionOps, ThreatFade, the W5 PostgreSQL container, or the SSM control path.
2. Default-deny egress and controlled DNS on that path, surviving process restart and host reboot.
3. Fail-closed behavior: if policy enforcement is down, the workload has no egress. A host that simply keeps its old open path is not fail-closed.
4. Adversarial packet or flow evidence after a restart, tied to the policy revision. The existing namespace transcript does not meet this, because the policy is deleted before the script exits.
5. No new AWS resources and no change to shared networks.

Until that environment exists, network and DNS enforcement stays **PARTIAL — E2/E3 ephemeral only**. Do not promote the cleaned-up namespace lab to a persistent control, and do not begin FCP-04.
