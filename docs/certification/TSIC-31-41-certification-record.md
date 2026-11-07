# Historical TSIC-31–41 Certification Record

> **Superseded numbering.** This record is retained to preserve historical certification evidence. It is not the canonical continuation of the current TSIC phase sequence. The canonical master sequence is TSIC-00 through TSIC-19 in [catalog/phases/registry.json](../../catalog/phases/registry.json).

The table below records the former numbering and its conceptual mapping to the current canonical sequence. It does not independently certify current phase status.

| Historical gate | Historical boundary | Current canonical phase |
|---|---|---|
| TSIC-31 | FAS + FAS-Bench | TSIC-05 |
| TSIC-32 | ThreatFade | TSIC-09 |
| TSIC-33 | BugFlow | TSIC-11 |
| TSIC-34 | HEZQARA | TSIC-12 |
| TSIC-35 | Economic Attribution | TSIC-13 |
| TSIC-36 | Closed-Loop Intelligence | TSIC-14 |
| TSIC-37 | Ecosystem Observability | TSIC-15 |
| TSIC-38 | MCP/A2A Interoperability | TSIC-16 |
| TSIC-39 | Production System-of-Systems | TSIC-17 |
| TSIC-40 | Tinlance.com Commercial/AaaS | TSIC-18 |
| TSIC-41 | Autonomous Revenue Operating Loop | TSIC-19 |

## FAS-Bench boundary

FAS is the production forensic-analysis authority. FAS-Bench is an independent evaluation and benchmarking layer. FAS-Bench MUST NOT be a runtime dependency of FAS. A benchmark outage, corpus defect, or harness defect MUST NOT prevent production forensic analysis.

Certification evaluates evidence-first semantics, observation/evidence/finding/verdict separation, provenance integrity, T0–T5 handling, SARIF interpretation, finding/verdict quality, regression resistance, reproducibility, false-positive/false-negative behavior, and deterministic evaluation.

## Production and commercial boundaries

TSIC remains the integration and certification authority. Agent Platform remains consequential generic execution authority. Agent OS owns workspace/lifecycle/orchestration. FDSE owns delivery orchestration. Domain systems retain domain authority. Commercial/AaaS surfaces bind to governed capabilities and do not become a second execution authority.

The historical TSIC-40 and TSIC-41 labels are commercial/control-plane certification concepts, not permission to bypass policy, consent, tenant isolation, approval, audit, or domain-specific compliance requirements.

## Re-certification and evidence use

A historical record can establish what was asserted and evidenced at its recorded baseline. It must not be reused as proof for a later commit or deployment. Any material authority, contract, adapter, benchmark corpus/harness, canonical workflow, economic field, interoperability baseline, commercial entitlement rule, or production-control change requires the affected current gate to be re-evaluated using evidence tied to the exact revision.

For current evidence scope and limitations, see [the November 7 main-branch evidence snapshot](../audits/current-main-evidence-2026-11-07.md).
