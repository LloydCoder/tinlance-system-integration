#!/usr/bin/env python3
"""Post-phase audit for MCP/A2A version, authorization, and delegation boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "policies/interoperability-baseline.json",
        "contracts/agents/interoperability-gate.json",
        "contracts/agents/registration.json",
        "scripts/certify_interoperability.py",
        ".github/workflows/interoperability-e2e.yml",
        ".github/workflows/ci.yml",
        "docs/architecture/model-and-agent-interoperability.md",
        "catalog/phases/registry.json",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-16 artifacts: " + ", ".join(missing))
    baseline = load("policies/interoperability-baseline.json")
    gate = load("contracts/agents/interoperability-gate.json")
    phases = load("catalog/phases/registry.json")
    if baseline["mcp_specification"] != gate["protocols"]["mcp"]["specification"]:
        raise SystemExit("FAIL MCP specification version drift")
    if baseline["a2a_specification"] != gate["protocols"]["a2a"]["specification"]:
        raise SystemExit("FAIL A2A specification version drift")
    for protocol in ("mcp", "a2a"):
        if gate["protocols"][protocol]["authorization_authority"] != "agent-platform":
            raise SystemExit(f"FAIL {protocol} may not become authorization authority")
    if gate["rules"]["protocol_support_never_grants_execution_authority"] is not True:
        raise SystemExit("FAIL protocol support must not grant execution authority")
    if not gate["rules"]["delegation_must_be_scoped_and_expiring"]:
        raise SystemExit("FAIL remote delegation must be bounded")
    workflow = (ROOT / ".github/workflows/interoperability-e2e.yml").read_text(encoding="utf-8")
    for marker in ("scripts/certify_interoperability.py", "scripts/forensic_audit_phase16.py", "persist-credentials: false"):
        if marker not in workflow:
            raise SystemExit(f"FAIL interoperability E2E workflow missing gate: {marker}")
    status = {item["id"]: item["status"] for item in phases["sequence"]}
    if status["TSIC-15"] != "completed" or status["TSIC-16"] not in {"in_progress", "completed"}:
        raise SystemExit("FAIL serial phase dependency is not satisfied")
    print("PASS TSIC-16 forensic audit: protocol pin parity, Agent Platform authorization, bounded delegation, and fail-closed contract gates verified")


if __name__ == "__main__":
    main()
