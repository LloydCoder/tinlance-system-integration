# Governance

## Purpose and scope

Tinlance System Integration & Conformance (TSIC) is the ecosystem integration and conformance authority. It governs cross-system identity, registries, integration contracts, compatibility policy, conformance requirements, verification tooling, and certification evidence.

TSIC does not own or execute domain runtime behavior. It must not become a second agent runtime, authorization service, approval engine, or domain business application.

## Authority boundaries

| System | Authority |
|---|---|
| TSIC | Ecosystem integration contracts, registries, compatibility, conformance, certification evidence |
| Agent Platform | Generic consequential execution authority, identity/authorization, policy, approvals, runtime, tool/MCP access, sandbox, secrets, budgets, evidence, audit, observability |
| Agent OS | Workspace, environment, lifecycle, and orchestration above Agent Platform |
| Agent Platform SDK | Developer client surface; no independent authority grant |
| TADS / SDEA / ReconOS / FadeReach / FDSE / FDE Mastery | Their declared developer, acquisition, engineering delivery, and methodology domains |
| FAS | Production forensic/evidence analysis |
| FAS-Bench | Independent evaluation and benchmarking; not a FAS runtime dependency |
| ThreatFade Engine | Detection and analysis domain |
| ThreatFade Web | Product, analyst, research, and commercial surface |
| Other domain systems | Their declared domain authority |

A route or adapter describes how systems interact; it does not transfer authority. If two systems appear to own the same consequential capability, the integration is blocked until the owner and contract are resolved.

## Maintainer model

The current repository ownership model is single-maintainer. [CODEOWNERS](CODEOWNERS) identifies `@LloydCoder` as the current code owner. This file is a review-routing declaration; it does not itself enforce approval requirements.

The maintainer is responsible for:
- Reviewing and merging changes.
- Maintaining canonical registries and contracts.
- Approving architecture decisions and compatibility changes.
- Coordinating security reports and community enforcement.
- Publishing release and certification evidence.
- Keeping governance and ownership records accurate.

## Decision process

1. **Routine changes:** documentation corrections, non-breaking validator improvements, and low-risk maintenance may be proposed directly through a pull request.
2. **Normative contract changes:** require a compatibility analysis, affected-consumer list, versioning decision, fixtures, validator updates, and migration guidance.
3. **Architecture or authority changes:** require an issue or design proposal and an Architecture Decision Record (ADR) describing context, decision, alternatives, consequences, and migration.
4. **Security-sensitive changes:** follow the private reporting process in [SECURITY.md](SECURITY.md); do not disclose exploit details in public review.
5. **Certification changes:** identify exact source commits, workflow run IDs, artifacts, scope, limitations, and whether evidence is reference-only or production-derived.

The maintainer records accepted material decisions in `docs/architecture/decision-records/` and updates the relevant registries and documentation.

## Review and release

All pull requests require maintainer review. The repository's CODEOWNERS file identifies the expected reviewer. Required reviews and status checks must be enforced through GitHub branch protection or repository rulesets; a CODEOWNERS file alone is not an enforcement mechanism.

A release must identify an immutable source revision, version, change summary, compatibility impact, and verification evidence. Signed tags and provenance attestations should be used when the release process is enabled. No release or production certification should be implied solely by a version file or green CI.

## Conflicts and appeals

Technical disagreements should be documented in the relevant issue or ADR with evidence and alternatives. Security and conduct concerns must use private channels. The maintainer makes the final repository decision and should document material decisions and their rationale.

## Succession

If repository ownership or maintainer responsibility changes, update CODEOWNERS, repository settings, security contact routing, and this document together. Do not leave security or review responsibilities assigned to an inactive account.
