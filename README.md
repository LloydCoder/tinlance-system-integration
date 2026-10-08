# Tinlance System Integration & Conformance (TSIC)

**The canonical integration control plane for defining, validating, and certifying interoperability across the Tinlance system-of-systems.**

TSIC is a control-plane and conformance repository. It does not replace domain runtimes, authorization engines, agent execution, or application logic.

## Current serial certification

The active continuation is **TSIC-31 through TSIC-41**:

- TSIC-31 — FAS + FAS-Bench Integration & Certification
- TSIC-32 — ThreatFade
- TSIC-33 — BugFlow
- TSIC-34 — Hezqara
- TSIC-35 — Economic Attribution
- TSIC-36 — Closed-Loop Intelligence
- TSIC-37 — Ecosystem Observability
- TSIC-38 — MCP/A2A Interoperability
- TSIC-39 — Production System-of-Systems
- TSIC-40 — Tinlance.com Commercial/AaaS
- TSIC-41 — Autonomous Revenue Operating Loop

FAS-Bench is deliberately independent from the FAS production execution path. It evaluates FAS and supplies reproducible certification evidence; it cannot become a production dependency.

## Verification

```bash
python3 scripts/final_certification.py
```

The final gate executes every serial certification script, then performs a forensic scan across JSON, Markdown, Python, YAML, adapters, policies, workflows, and certification records.

## Architecture

TSIC governs integration contracts and certification. Agent Platform remains the generic consequential execution authority. Agent OS owns workspace/lifecycle/orchestration. Domain systems retain domain authority. Commercial/AaaS and autonomous-revenue surfaces consume certified capabilities and evidence without acquiring execution authority.

See `docs/certification/TSIC-31-41-certification-record.md` and `docs/architecture/serial-integration-31-41.md`.
