# Security Policy

## Scope

TSIC is a public integration-control repository. Do not submit production secrets, private keys, customer data, PHI, regulated operational records, credentials, or sensitive infrastructure details.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting / Security Advisories for this repository when available. Do not open a public issue for an unpatched vulnerability.

If private reporting is unavailable, contact **hello@tinlance.com** with:
- a concise description;
- affected path, version, or commit;
- reproduction steps or proof of concept;
- impact assessment;
- suggested mitigation, if known.

Do not include live credentials or customer data.

## Response expectations

| Stage | Target |
|---|---|
| Acknowledgement | Within 3 business days |
| Initial triage | Within 7 business days |
| Mitigation plan | As soon as practical after triage |
| Public disclosure | Coordinated with the reporter after remediation or an agreed disclosure date |

These are maintainer targets, not contractual guarantees.

## Security controls

The repository uses least-privilege GitHub Actions permissions, deterministic secret-pattern scanning, OpenSSF Scorecard-oriented supply-chain controls, CODEOWNERS review coverage, machine-readable conformance gates, explicit identity propagation contracts, compatibility policy, and ecosystem-lock policy.

## Supported versions

Security fixes target the current main branch unless a release explicitly declares another supported line.

## Disclosure

Do not disclose a vulnerability publicly until the maintainer and reporter have agreed on an appropriate disclosure path and timing.
