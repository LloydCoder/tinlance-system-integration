#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    "manifests/ecosystem.json",
    "catalog/capabilities/authority.json",
    "catalog/dependencies/graph.json",
    "catalog/services/registry.json",
    "catalog/contracts/registry.json",
    "catalog/economics/cost-centers.json",
    "catalog/architecture/canonical.json",
    "catalog/authority/reconciliation.json",
    "contracts/common/identity-context.json",
    "contracts/agents/registration.json",
    "contracts/events/envelope.json",
    "contracts/events/delivery-semantics.json",
    "contracts/telemetry/trace-context.json",
    "contracts/models/routing-authority.json",
    "contracts/agents/interoperability-gate.json",
    "contracts/economics/attribution.json",
    "integrations/adapters/registry.json",
    "workflows/canonical.json",
    "reliability/failure-matrix.json",
    "policies/ecosystem-lock.json",
]

missing = [p for p in required if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("FAIL missing artifacts: " + ",".join(missing))

markers = [
    f"conformance/requirements/phase{i}.json" for i in range(1, 11)
] + ["conformance/requirements/phase11.json"]
missing = [p for p in markers if not (ROOT / p).is_file()]
if missing:
    raise SystemExit("FAIL missing conformance phases: " + ",".join(missing))

json_files = list(ROOT.rglob("*.json"))
for path in json_files:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"FAIL invalid JSON {path}: {exc}") from exc

eco = json.loads((ROOT / "manifests/ecosystem.json").read_text())
systems = eco["systems"]
ids = [item["id"] for item in systems]
if len(ids) != len(set(ids)):
    raise SystemExit("FAIL duplicate systems")

expected_repositories = {
    "tsic": "LloydCoder/tinlance-system-integration",
    "agent-platform": "LloydCoder/tinlance-agent-platform",
    "agent-platform-sdk": "LloydCoder/tinlance-agent-platform-sdk",
    "agent-os": "LloydCoder/tinlance-agent-os",
    "agent-developer": "LloydCoder/tinlance-agent-developer",
    "tads": "LloydCoder/tinlance-tads",
    "sdea": "LloydCoder/tinlance-sdea",
    "reconos": "LloydCoder/reconos-ofe",
    "fadereach": "LloydCoder/fadereach",
    "fas": "LloydCoder/fas",
    "fdse": "LloydCoder/tinlance-fdse",
    "fdse-toolkit": "LloydCoder/Tinlance-FDSE-toolkit",
    "world-intelligence": "LloydCoder/tinlance-world-intelligence",
    "hezqara": "LloydCoder/hezqara",
    "bugflow": "LloydCoder/bugflow-elite",
    "threatfade": "LloydCoder/tinlance-threatfade",
}
for system_id, repository in expected_repositories.items():
    actual = next((item.get("repository") for item in systems if item["id"] == system_id), None)
    if actual != repository:
        raise SystemExit(
            f"FAIL stale repository mapping for {system_id}: {actual!r} != {repository!r}"
        )

roles = {item["id"]: item.get("governance_role") for item in systems}
if roles.get("tsic") != "ecosystem_integration_authority":
    raise SystemExit("FAIL TSIC governance role")
if roles.get("agent-developer") != "developer_validation_consumer":
    raise SystemExit("FAIL TADL governance role")
if roles.get("agent-platform") != "execution_authority":
    raise SystemExit("FAIL Agent Platform governance role")

authority = json.loads((ROOT / "catalog/capabilities/authority.json").read_text())
owners = {}
for item in authority["capabilities"]:
    old = owners.get(item["capability"])
    if old and old != item["owner"]:
        raise SystemExit("FAIL conflicting authority: " + item["capability"])
    owners[item["capability"]] = item["owner"]
if any(item["owner"] not in ids for item in authority["capabilities"]):
    raise SystemExit("FAIL unregistered authority owner")

reconciliation = json.loads(
    (ROOT / "catalog/authority/reconciliation.json").read_text()
)
rule_ids = {item["id"] for item in reconciliation["rules"]}
required_rules = {"AUTH-007", "AUTH-008", "AUTH-009", "AUTH-010"}
if not required_rules <= rule_ids:
    raise SystemExit("FAIL authority reconciliation is missing P0 governance rules")

canonical = json.loads((ROOT / "catalog/architecture/canonical.json").read_text())
canonical_ids = {item["id"] for item in canonical["systems"]}
if canonical_ids != set(ids):
    raise SystemExit("FAIL canonical architecture differs from ecosystem manifest")

authority_caps = {item["capability"] for item in authority["capabilities"]}
for system in canonical["systems"]:
    for capability in system["authority"]:
        if capability not in authority_caps:
            raise SystemExit(
                "FAIL canonical authority not registered: " + capability
            )

services = json.loads((ROOT / "catalog/services/registry.json").read_text())
service_ids = {item["id"] for item in services["services"]}
if len(service_ids) != len(services["services"]):
    raise SystemExit("FAIL duplicate service IDs")
if any(item["system"] not in ids for item in services["services"]):
    raise SystemExit("FAIL service references unregistered system")

contracts = json.loads((ROOT / "catalog/contracts/registry.json").read_text())
contract_ids = {item["id"] for item in contracts["contracts"]}
required_contracts = {
    "identity-context",
    "agent-registration",
    "event-envelope",
    "delivery-semantics",
    "trace-context",
    "model-routing-authority",
    "agent-interoperability-gate",
    "economic-attribution",
    "adapter-rules",
    "failure-matrix",
    "ecosystem-lock",
    "canonical-workflows",
}
if not required_contracts <= contract_ids:
    raise SystemExit("FAIL incomplete contract registry")

dependencies = json.loads((ROOT / "catalog/dependencies/graph.json").read_text())
if any(
    edge["from"] not in ids or edge["to"] not in ids
    for edge in dependencies["edges"]
):
    raise SystemExit("FAIL dependency references unregistered system")

adapters = json.loads((ROOT / "integrations/adapters/registry.json").read_text())
adapter_ids = {item["id"] for item in adapters["adapters"]}
if len(adapter_ids) != len(adapters["adapters"]):
    raise SystemExit("FAIL duplicate adapter IDs")
if any(
    item["from"] not in ids or item["to"] not in ids
    for item in adapters["adapters"]
):
    raise SystemExit("FAIL adapter references unregistered system")

workflows = json.loads((ROOT / "workflows/canonical.json").read_text())
if any(
    item["steps"][0] not in ids or item["steps"][-1] not in ids
    for item in workflows["workflows"]
):
    raise SystemExit("FAIL workflow endpoint not registered")
expected_workflows = {"acquisition-engineering", "transformation", "agent-development"}
if {item["id"] for item in workflows["workflows"]} != expected_workflows:
    raise SystemExit("FAIL canonical workflow set")

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path == ROOT / "tooling/forensic_audit.py":
        continue
    if path.suffix.lower() in {".md", ".json", ".py", ".yml", ".yaml"}:
        text = path.read_text(encoding="utf-8", errors="strict")
        if "TODO" in text or "TBD" in text:
            raise SystemExit(f"FAIL unresolved placeholder in {path}")
        if re.search(
            r"-----BEGIN (?:RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----", text
        ):
            raise SystemExit(f"FAIL private key marker in {path}")

for command in [
    ["python3", "tooling/run_reference_workflow.py"],
    ["python3", "tooling/recovery_cert.py"],
    ["python3", "tooling/ecosystem_lock.py"],
]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(
            "FAIL " + command[-1] + ": " + result.stderr.strip()
        )

print(
    f"PASS TSIC-18 P0 forensic audit: {len(ids)} systems, "
    f"{len(owners)} capabilities, {len(json_files)} JSON files, "
    "repository mappings and authority governance reconciled"
)
