#!/usr/bin/env python3
"""Final structural audit for TSIC-17 production system-of-systems conformance."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    required = [
        "manifests/ecosystem.json",
        "integrations/hezcast/adapter.json",
        "catalog/dependencies/graph.json",
        "catalog/services/registry.json",
        "catalog/capabilities/authority.json",
        "catalog/contracts/registry.json",
        "catalog/phases/registry.json",
        "policies/production-system-baseline.json",
        "scripts/certify_production_system.py",
        ".github/workflows/production-system-e2e.yml",
        ".github/workflows/production-system-certification.yml",
        "reliability/failure-matrix.json",
        "policies/ecosystem-lock.json",
        "docs/certification/production-system-of-systems.md",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("FAIL missing TSIC-17 artifacts: " + ", ".join(missing))
    manifest = load("manifests/ecosystem.json")
    graph = load("catalog/dependencies/graph.json")
    services = load("catalog/services/registry.json")
    capabilities = load("catalog/capabilities/authority.json")
    phases = load("catalog/phases/registry.json")
    baseline = load("policies/production-system-baseline.json")
    failure_matrix = load("reliability/failure-matrix.json")
    lock = load("policies/ecosystem-lock.json")
    manifest_ids = {item["id"] for item in manifest["systems"]}
    graph_ids = {item["system"] for item in graph["nodes"]}
    if "hezcast" not in manifest_ids or "hezcast" not in graph_ids:
        raise SystemExit("FAIL HezCast missing from ecosystem manifest or dependency graph")
    if manifest_ids != graph_ids:
        raise SystemExit("FAIL manifest/dependency graph system sets diverge")
    if not graph["edges"] or any(edge["from"] not in graph_ids or edge["to"] not in graph_ids for edge in graph["edges"]):
        raise SystemExit("FAIL dependency graph has missing nodes or no edges")
    if len([item for item in manifest["systems"] if item.get("governance_role") == "execution_authority"]) != 1:
        raise SystemExit("FAIL generic execution authority is not unique")
    adapter = load("integrations/hezcast/adapter.json")
    service_ids = {item["id"] for item in services["services"]}
    if "hezcast" not in service_ids:
        raise SystemExit("FAIL HezCast missing from service registry")
    capability_owners = {item["capability"]: item["owner"] for item in capabilities["capabilities"]}
    if capability_owners.get("content_generation") != "hezcast" or capability_owners.get("external_content_publishing") != "agent-platform":
        raise SystemExit("FAIL HezCast content/publishing capability ownership drift")
    if adapter["authority"].get("external_publishing_execution") != "agent-platform":
        raise SystemExit("FAIL HezCast must not own external publishing execution authority")
    if manifest["ecosystem"]["integration_authority"] != "tsic" or graph["authority"] != "tsic":
        raise SystemExit("FAIL TSIC is not the canonical integration authority")
    if not baseline["required_boundaries"] or not failure_matrix:
        raise SystemExit("FAIL production boundaries or recovery evidence are missing")
    if not lock:
        raise SystemExit("FAIL ecosystem lock is empty")
    sequence = phases["sequence"]
    if [item["id"] for item in sequence] != [f"TSIC-{index:02d}" for index in range(20)]:
        raise SystemExit("FAIL canonical phase sequence is not contiguous")
    status = {item["id"]: item["status"] for item in sequence}
    if status["TSIC-16"] != "completed" or status["TSIC-17"] not in {"in_progress", "completed"}:
        raise SystemExit("FAIL serial phase dependency is not satisfied")
    workflow = (ROOT / ".github/workflows/production-system-e2e.yml").read_text(encoding="utf-8")
    for marker in ("scripts/certify_production_system.py", "scripts/forensic_audit_phase17.py", "persist-credentials: false"):
        if marker not in workflow:
            raise SystemExit(f"FAIL production E2E workflow missing gate: {marker}")
    print("PASS TSIC-17 forensic audit: manifest/graph parity, unique execution authority, ecosystem lock, recovery matrix and serial registry verified")


if __name__ == "__main__":
    main()
