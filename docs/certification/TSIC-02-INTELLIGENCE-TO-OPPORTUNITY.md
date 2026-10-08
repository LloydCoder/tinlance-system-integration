# TSIC-02 — World Intelligence → TADS → SDEA

## Certification boundary

TSIC-02 proves an executable intelligence-to-opportunity path across the three authoritative systems.

```
World Intelligence
source → artifact → observation → evidence → world signal
                                      ↓
TADS
validated evidence → signal detection → opportunity scoring
                                      ↓
SDEA
signal IDs → demand hypothesis → capability need → qualified opportunity
```

The path is advisory. No signal, hypothesis, score, capability need, or opportunity grants consequential execution authority.

## Required lineage

`tenant_id → source_id → artifact_id → observation_id → evidence_id → signal_id → demand_hypothesis_id → capability_need_id → opportunity_id`

External content is untrusted data. Observation, evidence, intelligence and authority remain distinct epistemic layers.

## Gate

- Cross-repository execution: `scripts/certify_intelligence_to_opportunity.py`
- CI: `.github/workflows/intelligence-to-opportunity.yml`
- Post-phase forensic audit: `scripts/forensic_audit_phase2.py`
- Acceptance requirements: `conformance/requirements/phase2-intelligence-to-opportunity.json`

Certification is not complete until all three referenced CI test suites, the executable vertical slice, and the post-phase forensic audit are green.
