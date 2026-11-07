# Current Main-Branch Evidence Snapshot — 2026-11-07

## Scope

This record captures repository-level evidence observed on 2026-11-07 before the documentation and governance remediation branch was created. It supplements, but does not replace, the historical phase evidence ledger.

- Repository: `LloydCoder/tinlance-system-integration`
- Default branch: `main`
- Reviewed commit: `906c8027d2e5c4c43de1b136e2c8e147bc13425c`
- Commit verification: GitHub reported the merge commit as verified.
- Repository tree: 296 tracked files at the reviewed commit; 70 Markdown files, 47 under `docs/`.
- Canonical phase registry: 20 entries, TSIC-00 through TSIC-19.
- Production status: not established by this repository-level snapshot.

## Workflow evidence

| Workflow | Run ID | Result | Scope |
|---|---:|---|---|
| TSIC CI | 42358834176 | Success | Repository CI at the reviewed main commit |
| OpenSSF Scorecard | 42358834338 | Success | Scorecard analysis at the reviewed main commit |

Run links:

- [TSIC CI run 42358834176](https://github.com/LloydCoder/tinlance-system-integration/actions/runs/42358834176)
- [OpenSSF Scorecard run 42358834338](https://github.com/LloydCoder/tinlance-system-integration/actions/runs/42358834338)

A successful workflow means that workflow's configured checks passed. It does not establish production deployment, customer usage, service availability, third-party certification, or completion of separate runtime programmes.

## OpenSSF Scorecard snapshot

The reported aggregate score was **5.7/10**. Relevant individual results:

| Check | Result |
|---|---:|
| Security-Policy | 10/10 |
| Code-Review | 0/10 |
| Binary-Artifacts | 10/10 |
| Dependency-Update-Tool | 10/10 |
| Maintained | 0/10 |
| Token-Permissions | 10/10 |
| Pinned-Dependencies | 5/10 |
| Dangerous-Workflow | 10/10 |
| License | 9/10 |
| Vulnerabilities | 10/10 |
| CII-Best-Practices | 0/10 |
| SAST | 0/10 |
| Branch-Protection | 0/10 |
| Fuzzing | 0/10 |
| Contributors | 3/10 |

Checks reported as not applicable are not zero scores. The Scorecard workflow passing means the analysis completed; it does not mean the repository achieved a high score.

## Historical phase evidence

`catalog/phases/evidence-ledger.json` records a reviewed baseline at commit `9d4361a16ae1a5570eee49d6baf499f61e222a20`, reviewed 2026-10-17. Its per-phase workflow records refer to that exact historical SHA. They remain historical evidence and must not be relabeled as evidence for the November 7 main commit.

The ledger explicitly sets `production_status` to `unverified` and each phase record sets `production_claim` to false. Preserve those limitations.

## Separate Persistent Agent Computer work

Persistent Agent Computer W2 acceptance is a separate runtime programme. Repository-level TSIC CI and Scorecard do not certify its production readiness. The current acceptance tracker and platform PRs remain the sources for runtime-specific evidence. In particular, do not infer that candidate isolation substrates, independent rootfs reproducibility, or production economics have been completed from this repository's green workflows.

## Reconciliation rule

For each future evidence update, record:

1. Exact repository commit SHA.
2. Exact workflow run ID and URL.
3. Workflow conclusion and relevant job/step results.
4. Evidence scope: structural, contract, reference E2E, deployed integration, or production.
5. Explicit limitations and whether a production claim is made.

Do not copy an old run ID onto a new commit or change the historical ledger's reviewed SHA to make the evidence appear current.
