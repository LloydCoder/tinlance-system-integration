# Security Policy

## Scope

This repository defines integration contracts, registries, conformance tooling, and certification evidence for the Tinlance system-of-systems. Security reports may concern this repository's code, schemas, workflows, dependency configuration, or documented integration boundaries.

Do not submit credentials, private keys, customer data, personal data, protected health information (PHI), or confidential production records in public issues or pull requests.

## Supported versions

Security fixes are developed against the current default branch (`main`). A release is supported only if its release notes explicitly state a support period.

## Reporting a vulnerability

**Do not open a public GitHub issue for an unpatched vulnerability.**

Use [GitHub private vulnerability reporting](https://github.com/LloydCoder/tinlance-system-integration/security/advisories/new) when enabled. If that facility is unavailable, email **hello@tinlance.com** with the subject `SECURITY: TSIC vulnerability report`.

Include, where safe:

- A concise description and affected component or path.
- Affected commit, version, or workflow.
- Reproduction steps or a proof of concept.
- Expected security impact and realistic attack prerequisites.
- Suggested mitigation, if known.

Do not attach live credentials, customer records, or PHI. Use a minimal sanitized reproduction.

## Response targets

These are maintainer service targets, not contractual guarantees.

| Activity | Target |
|---|---|
| Acknowledge receipt | Within 3 business days |
| Initial triage and severity assessment | Within 7 business days |
| Mitigation or remediation plan | Communicated after triage, with priority based on severity and exploitability |
| Coordinated disclosure | Agree timing with the reporter after a fix or mitigation is available |

If the report is urgent and the initial contact receives no response, follow up through the same private channel. Do not disclose details publicly while coordination is active.

## Handling and disclosure

The maintainer will validate the report, determine affected versions and boundaries, coordinate a fix, and prepare an advisory where appropriate. Credit will be given to reporters who request it and consent to public attribution.

## Security controls and limitations

The repository includes least-privilege workflow permissions, dependency-update configuration, secret-pattern checks, conformance validation, and security policy documentation. Automated checks are not a guarantee that the repository is free of vulnerabilities. A successful CI run is not a substitute for security review, penetration testing, or production assurance.
