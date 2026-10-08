# TSIC-25 — Acquisition System Certification

This gate certifies the reviewed cross-repository acquisition chain:

`World Intelligence → TADS → SDEA → ReconOS → FadeReach`

## Authority model

- **TSIC** — ecosystem integration contracts and certification.
- **World Intelligence** — source/artifact/observation/evidence/entity/event/temporal/change/signal intelligence semantics.
- **TADS** — target/account/demand decisioning.
- **SDEA** — engineering-acquisition interpretation and recommendation.
- **ReconOS** — technical/OSINT enrichment and confidence.
- **FadeReach** — outreach execution within consent/suppression boundaries.
- **Agent Platform** — governed consequential execution authority.

No downstream acquisition system can grant execution authority.

## Feedback topology

The commercial loop is explicitly represented as:

`World Intelligence → TADS → SDEA → ReconOS → FadeReach → Sales → FDSE → Outcome → Evidence → Economic Attribution → Evaluation → TADS/SDEA`

Feedback is learning input. It is not an authorization channel and cannot bypass policy or approval boundaries.

## Certification

Run:

```bash
python scripts/acquisition_system_certification.py
```

The gate verifies:

1. immutable reviewed revisions for all five systems;
2. reachability of each reviewed repository revision;
3. presence of each system's executable TSIC conformance gate;
4. each conformance gate's pinned TSIC adapter revision;
5. canonical adapter ownership and execution-authority invariants;
6. the acquisition feedback topology.

Passing this gate certifies the reviewed contract baseline, not live production deployment or commercial performance.
