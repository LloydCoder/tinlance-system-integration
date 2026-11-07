# Contributing to TSIC

Thank you for helping improve Tinlance System Integration & Conformance (TSIC). Contributions should make ecosystem integration more explicit, testable, secure, and maintainable without creating duplicate authority.

## Before starting

1. Read the [README](README.md), [governance model](GOVERNANCE.md), and relevant architecture documents.
2. Search existing issues, pull requests, contracts, and ADRs before proposing a new abstraction.
3. For a material architecture or authority change, open an issue first and include the problem, owner, alternatives, compatibility impact, and migration plan.
4. Never include secrets, customer information, personal data, PHI, private keys, or production evidence that you are not authorized to publish.

## Contribution workflow

1. Fork the repository.
2. Create a focused branch from `main`, for example `docs/clarify-event-contracts` or `feat/adapter-validation`.
3. Make a small, reviewable change. Keep normative registries, schemas, validators, and documentation consistent.
4. Run the relevant checks listed below.
5. Commit using Conventional Commits where practical.
6. Push the branch and open a pull request against `main`.
7. Complete review feedback and ensure all required CI checks pass before merge.

## Local setup

Core checks use Python 3 and the standard library. Schema-dependent checks use the pinned dependency in `requirements-ci.txt`.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-ci.txt
```

On Windows, create the environment with `py -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1`.

## Validation

Run the checks relevant to the files changed. Before opening a broad conformance or architecture PR, run the repository's full local gate set:

```bash
python scripts/certify_phase0.py
python tooling/validate_phase0.py
python scripts/validate_twi_integration.py
python scripts/validate_event_contract.py
python tooling/run_reference_workflow.py
python tooling/recovery_cert.py
python tooling/forensic_audit.py
python tooling/security_scan.py
python scripts/certify_economic_attribution.py
python scripts/certify_interoperability.py
python scripts/acquisition_system_certification.py
python scripts/final_certification.py
```

The event-contract validator requires the dependencies in `requirements-ci.txt`. The CI workflow is authoritative for the current gate sequence; if this list and CI diverge, update this guide in the same change.

## Engineering standards

### Architecture and authority

- TSIC owns ecosystem registries, integration contracts, compatibility, conformance, and certification evidence.
- Agent Platform remains the sole generic consequential execution authority.
- Agent OS owns workspace, environment, lifecycle, and orchestration above Platform.
- Domain systems retain their declared domain authority.
- FAS-Bench is an independent evaluation authority, not a FAS runtime dependency.
- Do not duplicate authorization, policy, approval, execution, or audit authority in adapters or domain-facing clients.

### Contracts and compatibility

- Prefer explicit, versioned, machine-readable contracts.
- Validate JSON against the relevant JSON Schema.
- Preserve tenant, identity, trace, and provenance context across boundaries.
- Document delivery guarantees, idempotency, retries, replay, ordering, and failure behavior.
- Treat unknown or authority-shaped input as untrusted unless a contract explicitly permits it.
- For breaking changes, document the affected consumers, migration steps, deprecation window, and compatibility decision.
- Update contract registries, schemas, fixtures, validators, docs, and evidence together.

### Python and tooling

- Follow existing Python style and avoid unnecessary dependencies.
- Keep validators deterministic and fail with actionable messages.
- Do not weaken or skip a check solely to make CI green.
- Add regression coverage for behavioral changes.
- Avoid tests that depend on live external services unless the workflow explicitly provisions them.

### Documentation

- Use relative links for files within this repository.
- Label historical and superseded material clearly.
- Distinguish proposed, implemented, tested, integrated, verified, and production-deployed states.
- Never describe a reference workflow as production certification.
- Keep the root README focused on visitor onboarding; put detailed architecture and operations material under `docs/`.

## Commit messages

Use Conventional Commits where practical:

- `docs: clarify TSIC phase authority`
- `fix: reject invalid event envelope`
- `feat: add adapter conformance rule`
- `test: cover replay idempotency boundary`
- `ci: add static analysis workflow`

## Pull request checklist

- [ ] The change has a clear owner and does not create duplicate authority.
- [ ] Relevant scripts and tests pass locally.
- [ ] CI is green.
- [ ] Normative JSON, schemas, fixtures, and registries are consistent.
- [ ] Compatibility and migration impact are documented.
- [ ] Architecture changes include or update an ADR.
- [ ] Documentation and navigation are updated.
- [ ] No secrets or restricted data are included.
- [ ] Evidence statements identify exact commits and workflow runs.

## Review and merge

All changes are subject to maintainer review. CODEOWNERS identifies the current owner. A green CI run is necessary but does not replace human review, security review, or production acceptance evidence.

For security-sensitive contributions, follow [SECURITY.md](SECURITY.md) and coordinate privately before opening a public PR.
