# P0 — Ecosystem Reconciliation Runbook

## Objective

Establish one authoritative system-of-systems registry and one unambiguous conformance authority before implementing cross-repository adapters.

## P0 gates

1. Every known GitHub-backed Tinlance system has a canonical repository mapping.
2. TSIC is the ecosystem integration/conformance authority.
3. TADL remains a developer validation consumer and never grants execution authority.
4. Agent Platform remains the sole governed execution authority.
5. Agent OS remains the workspace/lifecycle/orchestration authority.
6. System-local CI remains valid but cannot override TSIC ecosystem contracts.
7. Canonical architecture, authority, services, dependencies, adapters, workflows, and contract registries reference only registered systems.
8. Repository mapping and governance-role drift is CI-detectable.
9. No unresolved placeholder or private-key marker is present in normative repository artifacts.
10. Reference workflow, recovery certification, ecosystem lock, and forensic audit all pass.

## Completion evidence

The P0 completion gate is the forensic_audit.py result plus the repository CI workflow. P0 is incomplete until the PR checks are green on the branch and the merge commit.

## Next phase

Only after this gate is green should TSIC-18.1 implement the reusable integration/adapter contract harness and the first Agent Platform adapter.
