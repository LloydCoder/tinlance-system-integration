#!/usr/bin/env python3
"""Final TSIC-38 forensic certification."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_SCRIPTS = [
    "tooling/validate_phase0.py",
    "tooling/run_reference_workflow.py",
    "tooling/recovery_cert.py",
    "tooling/ecosystem_lock.py",
    "tooling/forensic_audit.py",
    "tooling/security_scan.py",
    "scripts/certify_acquisition_system.py",
    "scripts/certify_engineering_route.py",
    "scripts/certify_transformation_route.py",
    "scripts/certify_delivery_evidence.py",
    "scripts/certify_fas.py",
    "scripts/certify_threatfade.py",
    "scripts/certify_bugflow.py",
    "scripts/certify_hezqara.py",
    "scripts/certify_economic_attribution.py",
    "scripts/certify_closed_loop.py",
    "scripts/certify_observability.py",
    "scripts/certify_interoperability.py",
]
REQUIRED_POLICIES = [
    "policies/agent-system-baseline.json",
    "policies/acquisition-system-baseline.json",
    "policies/engineering-route-baseline.json",
    "policies/transformation-route-baseline.json",
    "policies/delivery-evidence-baseline.json",
    "policies/fas-baseline.json",
    "policies/threatfade-baseline.json",
    "policies/bugflow-baseline.json",
    "policies/hezqara-baseline.json",
    "policies/economic-attribution-baseline.json",
    "policies/closed-loop-baseline.json",
    "policies/observability-baseline.json",
    "policies/interoperability-baseline.json",
]
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----")


def run(script: str) -> None:
    result = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(f"FAIL {script}: {result.stdout.strip()} {result.stderr.strip()}")
    print(result.stdout.strip())


def load(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def forensic_scan() -> None:
    for policy in REQUIRED_POLICIES:
        if not (ROOT / policy).is_file():
            raise SystemExit(f"FAIL missing final policy: {policy}")

    seen_adapters: set[str] = set()
    for path in (ROOT / "integrations").rglob("*.json"):
        obj = load(str(path.relative_to(ROOT)))
        adapter_id = obj.get("adapter_id")
        if adapter_id:
            if adapter_id in seen_adapters:
                raise SystemExit(f"FAIL duplicate adapter ID: {adapter_id}")
            seen_adapters.add(adapter_id)

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path in {ROOT / "scripts/final_certification.py", ROOT / "tooling/forensic_audit.py"}:
            continue
        if path.suffix.lower() not in {".md", ".json", ".py", ".yml", ".yaml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="strict")
        if "TODO" in text or "TBD" in text:
            raise SystemExit(f"FAIL unresolved placeholder: {path}")
        if PRIVATE_KEY.search(text):
            raise SystemExit(f"FAIL private-key marker: {path}")

    workflow = load("workflows/canonical.json")
    expected = {"acquisition-engineering", "transformation", "agent-development", "acquisition-feedback"}
    if {item["id"] for item in workflow["workflows"]} != expected:
        raise SystemExit("FAIL final canonical workflow set")

    print(f"PASS forensic repository scan: adapters={len(seen_adapters)} policies={len(REQUIRED_POLICIES)}")


def main() -> None:
    for script in PHASE_SCRIPTS:
        run(script)
    forensic_scan()
    print("PASS TSIC-38 FINAL PRODUCTION SYSTEM-OF-SYSTEMS FORENSIC CERTIFICATION")


if __name__ == "__main__":
    main()
