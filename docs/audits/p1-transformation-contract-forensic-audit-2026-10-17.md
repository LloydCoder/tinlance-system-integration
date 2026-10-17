# P1 Forensic Audit — Transformation Contract

**Status: BLOCKED — NOT CERTIFIED GREEN.**

The canonical sequence defines P1 as the four-repository `transformation/v1` contract. Its own certification rule requires each repository change to be green and merged, followed by validation against the reviewed ecosystem baseline. P2 must not begin until this gate passes.

## Evidence reviewed

- TADL schema and example: `schemas/transformation/v1/transformation.schema.json`, `schemas/examples/transformation.v1.json`.
- TADL phase contract and conformance gate: `docs/ecosystem/P1-TRANSFORMATION.md`, `scripts/ecosystem_phase_conformance.py`.
- OS model/tests: `src/tinlance_agent_os/transformation.py`, `tests/test_transformation.py`.
- SDK model/tests: `src/tinlance_agent_platform_sdk/transformation.py`, `tests/test_transformation.py`.
- Platform model/tests: `packages/contracts/src/tinlance_agent_platform_contracts/transformation.py`, `tests/contracts/test_transformation.py`.
- Refreshed ecosystem lock/manifest merged in TADL PR #47.

## Findings

### P1-01 — Transformation schema was absent from the default schema-contract suite

The schema existed, but `tests/contract/schema-contracts.test.mjs` did not load it or validate the canonical transformation example.

**Remediation:** TADL PR [#48](https://github.com/LloydCoder/tinlance-agent-developer/pull/48) adds schema inventory coverage, example validation, required-provenance regression coverage, and contradictory-outcome rejection. It is not merged until the full CI/security/ecosystem suite passes.

### P1-02 — Outcome consistency was not enforced by the schema

The schema permitted `status="achieved"` with `achieved=false`, and also permitted `achieved=true` with a non-achieved status.

**Remediation:** PR #48 adds a schema-level `oneOf` invariant and regression tests.

### P1-03 — Agent OS Transformation model drops canonical fields

The main OS model omitted required data such as success criteria, principal identity, requested capabilities, governance, idempotency, constraints, execution timestamps, outputs, evidence, outcome metrics, and provenance.

**Remediation in progress:** branch `phase/p1-transformation-contract-2026-10-17` expands the model and tests. CI and merge evidence are outstanding.

### P1-04 — Platform Transformation model drops canonical fields

The main Platform model omitted success criteria, capability reasons, constraints, approvals, idempotency, timestamps, complete metric objects, and provenance.

**Remediation in progress:** Platform PR [#99](https://github.com/LloydCoder/tinlance-agent-platform/pull/99) expands the typed model, payload serializer and tests. CI and merge evidence are outstanding.

### P1-05 — SDK serialization does not satisfy the canonical schema

The SDK's `as_payload()` emits an empty constraints object and omits the schema-required `provenance` object, including `declared_by` and `recorded_at`. It also permits `achieved=true` with a non-achieved status. An SDK-produced payload therefore cannot reliably validate against the canonical schema.

This is a hard blocker. Do not weaken the canonical schema or fabricate provenance in a downstream validator. The SDK must preserve provenance and constraints, serialize every required field, and enforce the same outcome invariant.

### P1-06 — P1 certification baseline is stale

`docs/ecosystem/P1-TRANSFORMATION.md` still identifies baseline `p1-2026-10-07` and older repository revisions. It must be updated to exact reviewed SHAs after implementation PRs are merged.

## Required implementation order

1. Merge TADL schema coverage and outcome invariants only after all required checks pass.
2. Complete OS model serialization and lifecycle tests.
3. Complete Platform authority-side model serialization and tests.
4. Complete SDK provenance/constraints serialization and outcome consistency.
5. Add an ecosystem gate that serializes an actual SDK Transformation and validates it against the TADL schema; validating only the example is insufficient.
6. Update the P1 certification record and reviewed lock to the exact merged SHAs.
7. Run full cross-repository conformance and post-phase forensic audit.

## P1 exit gate

- [ ] Canonical schema and example are tested; contradictory outcomes fail.
- [ ] OS, SDK and Platform preserve the complete required contract without field loss.
- [ ] A real SDK-produced payload validates against the canonical schema.
- [ ] Four-repository P1 PRs pass CI/security and are merged at exact reviewed SHAs.
- [ ] P1 docs, manifest and lock agree on the certified baseline.
- [ ] No unresolved P1 blocker remains.

## Verdict

P1 is **not complete**. The SDK serialization gap is a hard blocker, and the OS/Platform changes remain unmerged. P2 must not start until P1 passes this gate.


## CI evidence update — 2026-10-17

- **TADL PR #48**, head `ee1619b2bf7055ecd93e546304a9c487a1984106`: CI, Security and Secret Scan passed; Ecosystem Integration failed in the full finite-phase certification gate. The failure explicitly reports the SDK serializer missing `provenance`, `declared_by`, and `recorded_at`, dropping caller-supplied constraints, and permitting `achieved=true` with a non-achieved status. CodeQL was still in progress at the time of this update.
- **Platform PR #99**, head `98ac6151a6ab3911c14fe4e246835a1c0c5c1bf2`: CodeQL, Secret Scan, R10 Certification, and Reference Agents passed; CI failed the Ruff format check on the new transformation contract module. The formatting defect must be corrected and the complete suite rerun.
- **Agent OS P1 branch** `phase/p1-transformation-contract-2026-10-17`: implementation and tests are present, but no PR/CI certification has been established in this evidence snapshot.
- **SDK P1 implementation**: no change has been merged or verified. The cross-repository gate correctly remains red until this serializer is fixed.

These results confirm the P1 gate is blocking for substantive reasons. No P1 implementation PR should be merged as a phase-completion claim until all four repository implementations and the ecosystem conformance gate pass.
