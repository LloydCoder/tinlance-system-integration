#!/usr/bin/env python3
"""Post-phase audit for TSIC-19 autonomous revenue control and attribution."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))
def main() -> None:
    required = ["policies/autonomous-revenue-baseline.json","workflows/canonical.json","contracts/economics/attribution.json","catalog/capabilities/aaas-offers.json","scripts/certify_autonomous_revenue.py","scripts/verify_aaas_site_sync.py",".github/workflows/autonomous-revenue-e2e.yml","docs/certification/autonomous-revenue-operating-loop.md","catalog/phases/registry.json"]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-19 artifacts: " + ", ".join(missing))
    baseline = load("policies/autonomous-revenue-baseline.json")
    canonical = load("workflows/canonical.json")
    phases = load("catalog/phases/registry.json")
    steps = {item["id"]: item["steps"] for item in canonical["workflows"]}.get("autonomous-revenue", [])
    if steps != baseline["required_workflow_steps"]:
        raise SystemExit("FAIL canonical revenue workflow and baseline diverge")
    if steps[-2:] != ["tads", "sdea"]:
        raise SystemExit("FAIL autonomous learning target escaped TADS/SDEA")
    if not (steps.index("consent-and-suppression") < steps.index("fadereach") and steps.index("policy-approval") < steps.index("fadereach") and steps.index("budget-check") < steps.index("fadereach")):
        raise SystemExit("FAIL consent/policy/budget gates are not upstream of outreach")
    if not (steps.index("outcome") < steps.index("evidence") < steps.index("economic-attribution") < steps.index("revenue-recognition") < steps.index("evaluation")):
        raise SystemExit("FAIL outcome/evidence/economic/revenue/evaluation order is invalid")
    workflow = (ROOT / ".github/workflows/autonomous-revenue-e2e.yml").read_text(encoding="utf-8")
    for marker in ("scripts/certify_autonomous_revenue.py","scripts/forensic_audit_phase19.py","scripts/verify_aaas_site_sync.py","LloydCoder/Tinlance","persist-credentials: false"):
        if marker not in workflow:
            raise SystemExit(f"FAIL autonomous revenue workflow missing gate: {marker}")
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    if status["TSIC-18"] != "completed" or status["TSIC-19"] not in {"in_progress", "completed"}:
        raise SystemExit("FAIL serial phase dependency is not satisfied")
    print("PASS TSIC-19 forensic audit: bounded feedback, consent, policy, economics and revenue lineage verified")
if __name__ == "__main__":
    main()
