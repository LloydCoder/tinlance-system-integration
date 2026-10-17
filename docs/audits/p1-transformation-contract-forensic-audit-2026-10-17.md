# P1 Forensic Audit — Transformation Contract

**Status: BLOCKED — NOT CERTIFIED.** Component repositories now have green checks for the reviewed main revisions, but P1 is not complete until the canonical lock and cross-repository round-trip contract are reconciled.

## Canonical phase authority

TADL `docs/ecosystem/PHASE-MATRIX.md` is the ecosystem phase matrix: P1 is the cross-repository `transformation/v1` contract; P2 is governed execution; P3 is identity/authority. The separate TSIC PR #61 attempted to redefine P1 as broad architecture/trace-context reconciliation and depended on an out-of-sequence trace change. It was closed without merge. Trace-context work is deferred to the phase that owns it.

## Evidence reviewed

Canonical contract:
- `schemas/transformation/v1/transformation.schema.json`
- `schemas/examples/transformation.v1.json`
- `docs/architecture/PHASE-14-TRANSFORMATION.md`
- `docs/ecosystem/PHASE-MATRIX.md`
- `scripts/ecosystem_phase_conformance.py`

Implementation models:
- Agent OS: `src/tinlance_agent_os/transformation.py`, `tests/test_transformation.py`
- Platform SDK: `src/tinlance_agent_platform_sdk/transformation.py`, `tests/test_transformation.py`
- Platform: `packages/contracts/src/tinlance_agent_platform_contracts/transformation.py`, `tests/contracts/test_transformation.py`
- TADL schema tests: `tests/contract/schema-contracts.test.mjs`

## Findings

### P1-01 — Schema coverage and outcome consistency are now implemented

TADL PR #48 is merged. The canonical schema is in the default schema-contract suite, the example is validated, provenance is required, and schema-level `oneOf` logic rejects contradictory `status` / `achieved` values.

### P1-02 — The Platform Transformation contract implementation is now merged

Platform PR #99 is merged. Its final head passed CI, CodeQL, Secret Scan, R10 Certification, and Reference Agents checks. The typed payload includes governance, constraints, execution metadata, outputs, evidence, outcomes, and provenance.

### P1-03 — Current OS and SDK models include the required top-level payload fields

The current OS and SDK models serialize provenance, constraints, idempotency, execution metadata, outputs/evidence, and outcome data. SDK outcome validation rejects inconsistent achieved states. The previous statement that the SDK omits provenance/constraints was based on an outdated baseline and is withdrawn.

### P1-04 — Platform model drops optional canonical context provenance

The canonical schema permits `context.source_refs`, and the SDK/OS models can carry source references in context. The current Platform Transformation model only serializes `workspace_ref` and `task_ref`; it has no field for context source references. A payload that contains this supported optional field cannot round-trip through the Platform model without losing data.

**Required fix:** add validated `context_source_refs` (or an equivalent typed context object) to the Platform contract model and serializer, then add a round-trip regression test proving those references survive. Do not silently move the field to another section; context source references and provenance source references have distinct semantics.

### P1-05 — OS lifecycle versioning preserves stale provenance

The OS `with_execution()` method increments the Transformation version but reuses the original provenance object and provides no way to set provenance for the new version. The canonical model describes versioned, append-oriented records; each newly recorded version needs provenance that identifies when/by whom that version was recorded.

**Required fix:** allow an explicit new provenance value for the new version, or construct it through a documented trusted recording boundary. Do not silently rewrite the prior version's provenance. Add tests proving the previous version remains unchanged and the new version carries its own timestamp/source attribution.

### P1-06 — The reviewed ecosystem lock is stale relative to the implementations being certified

The current `ecosystem.lock.json` pins older revisions:
- TADL: `25fac21a8912bf58f0a9fc65e6ed1cbede70bbee`
- Agent OS: `dd2119e4ace0bd0ca5dbae083badbb5d9909670b`
- Platform SDK: `61712794078b967aa84e3db21dd006b19136bcba`
- Platform: `c294acad0489e1165e2a3d89dcbcf24c21639d5e`

The current reviewed main revisions at this audit were:
- TADL: `818ca441d0708187152beb501ea0abe634417f07`
- Agent OS: `502161b863042ca40f823f9c5e3a0ac2f6677746`
- Platform SDK: `8a41d6dce2fe778ab25c33dfa315328d06ec4908`
- Platform: `5bfe29305be3aa77af2a1ec002bd146caaa105b5`

The four component main revisions above had green CI/security/conformance checks at review time. A green workflow against an old lock does not certify the newer implementation revisions. Refresh the reviewed lock and manifest after the required model fixes, then rerun the complete ecosystem gate against the exact locked SHAs.

### P1-07 — Real SDK serialization gate exists, but the lock must point at the intended SDK revision

The TADL ecosystem gate now constructs a real SDK Transformation, serializes it, and validates that payload against the canonical schema. This is the correct kind of test; validating only a fixture/example would be insufficient. Its result is only meaningful for the SDK revision actually checked out by the lock, which is currently stale.

## Current CI evidence

The following exact revisions had successful repository workflows at review time:

- TADL `818ca441d0708187152beb501ea0abe634417f07`: CI, CodeQL, Security, Secret Scan, Scorecard, Release Attestations, Ecosystem Integration — all success.
- Agent OS `502161b863042ca40f823f9c5e3a0ac2f6677746`: CI, CodeQL, OpenSSF Scorecard — all success.
- Platform SDK `8a41d6dce2fe778ab25c33dfa315328d06ec4908`: CI and Security — success.
- Platform `5bfe29305be3aa77af2a1ec002bd146caaa105b5`: CI, CodeQL, Secret Scan, R10 Certification, Reference Agents — all success.

These results establish repository-level workflow status only. They do not prove external production infrastructure is deployed.

## Required implementation order

1. Add context source-reference preservation to the Platform Transformation model and test.
2. Update OS lifecycle transitions so every new Transformation version has correct version-specific provenance without mutating prior versions.
3. Run OS, SDK and Platform contract tests and all repository security/CI workflows on exact candidate heads.
4. Refresh the reviewed ecosystem lock/manifest to the exact candidate SHAs and reconcile the P1 certification record.
5. Run the full TADL ecosystem gate, including serialization of a real SDK payload against the canonical schema.
6. Audit the resulting merged SHAs and confirm there is no P1 contract loss or stale pin.

## P1 exit gate

- [x] Canonical schema and example are included in TADL schema tests.
- [x] Schema rejects contradictory outcome states.
- [x] TADL real-SDK-payload validation gate exists.
- [x] Component CI/security checks are green on the revisions listed above.
- [ ] Platform preserves supported `context.source_refs`.
- [ ] OS lifecycle versions carry correct new-version provenance while preserving old versions.
- [ ] Reviewed lock/manifest pins the intended tested implementation revisions.
- [ ] Full cross-repository conformance passes against that refreshed lock.
- [ ] Post-phase audit records final merged SHAs and workflow evidence.

## Verdict

P1 remains **blocked** by two concrete round-trip/lifecycle gaps and a stale reviewed lock. Do not start P2 until these fixes are merged and the refreshed cross-repository gate is green.
