#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=[
"manifests/ecosystem.json","catalog/capabilities/authority.json","catalog/dependencies/graph.json",
"catalog/services/registry.json","catalog/contracts/registry.json","catalog/economics/cost-centers.json",
"catalog/architecture/canonical.json","catalog/authority/reconciliation.json",
"contracts/common/identity-context.json","contracts/agents/registration.json","contracts/events/envelope.json",
"contracts/events/delivery-semantics.json","contracts/telemetry/trace-context.json",
"contracts/models/routing-authority.json","contracts/agents/interoperability-gate.json",
"contracts/economics/attribution.json","integrations/adapters/registry.json","workflows/canonical.json",
"reliability/failure-matrix.json","policies/ecosystem-lock.json"
]
missing=[p for p in required if not (ROOT/p).is_file()]
if missing: raise SystemExit("FAIL missing artifacts: "+",".join(missing))
markers=[f"conformance/requirements/phase{i}.json" for i in range(1,11)]+["conformance/requirements/phase11.json"]
missing=[p for p in markers if not (ROOT/p).is_file()]
if missing: raise SystemExit("FAIL missing conformance phases: "+",".join(missing))
json_files=list(ROOT.rglob("*.json"))
for p in json_files:
    try: json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: raise SystemExit(f"FAIL invalid JSON {p}: {e}")
eco=json.loads((ROOT/"manifests/ecosystem.json").read_text())
ids=[x["id"] for x in eco["systems"]]
if len(ids)!=len(set(ids)): raise SystemExit("FAIL duplicate systems")
auth=json.loads((ROOT/"catalog/capabilities/authority.json").read_text())
owners={}
for x in auth["capabilities"]:
    old=owners.get(x["capability"])
    if old and old!=x["owner"]: raise SystemExit("FAIL conflicting authority: "+x["capability"])
    owners[x["capability"]]=x["owner"]
if any(x["owner"] not in ids for x in auth["capabilities"]): raise SystemExit("FAIL unregistered authority owner")
canon=json.loads((ROOT/"catalog/architecture/canonical.json").read_text())
canon_ids={x["id"] for x in canon["systems"]}
if canon_ids != set(ids): raise SystemExit("FAIL canonical architecture differs from ecosystem manifest")
auth_caps={x["capability"] for x in auth["capabilities"]}
for s in canon["systems"]:
    for cap in s["authority"]:
        if cap not in auth_caps: raise SystemExit("FAIL canonical authority not registered: "+cap)
services=json.loads((ROOT/"catalog/services/registry.json").read_text())
service_ids={x["id"] for x in services["services"]}
if len(service_ids)!=len(services["services"]): raise SystemExit("FAIL duplicate service IDs")
if any(x["system"] not in ids for x in services["services"]): raise SystemExit("FAIL service references unregistered system")
contracts=json.loads((ROOT/"catalog/contracts/registry.json").read_text())
contract_ids={x["id"] for x in contracts["contracts"]}
required_contracts={"identity-context","agent-registration","event-envelope","delivery-semantics","trace-context","model-routing-authority","agent-interoperability-gate","economic-attribution","adapter-rules","failure-matrix","ecosystem-lock","canonical-workflows"}
if not required_contracts <= contract_ids: raise SystemExit("FAIL incomplete contract registry")
deps=json.loads((ROOT/"catalog/dependencies/graph.json").read_text())
if any(e["from"] not in ids or e["to"] not in ids for e in deps["edges"]): raise SystemExit("FAIL dependency references unregistered system")
adapters=json.loads((ROOT/"integrations/adapters/registry.json").read_text())
adapter_ids={x["id"] for x in adapters["adapters"]}
if len(adapter_ids)!=len(adapters["adapters"]): raise SystemExit("FAIL duplicate adapter IDs")
if any(x["from"] not in ids or x["to"] not in ids for x in adapters["adapters"]): raise SystemExit("FAIL adapter references unregistered system")
if any(x["steps"][0] not in ids or x["steps"][-1] not in ids for x in wf["workflows"]): raise SystemExit("FAIL workflow endpoint not registered")
wf=json.loads((ROOT/"workflows/canonical.json").read_text())
expected={"acquisition-engineering","transformation","agent-development"}
if {x["id"] for x in wf["workflows"]}!=expected: raise SystemExit("FAIL canonical workflow set")
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts: continue
    if p != ROOT/"tooling/forensic_audit.py" and p.suffix.lower() in {".md",".json",".py",".yml",".yaml"}:
        t=p.read_text(encoding="utf-8",errors="strict")
        if "TODO" in t or "TBD" in t: raise SystemExit(f"FAIL unresolved placeholder in {p}")
        if re.search(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----",t): raise SystemExit(f"FAIL private key marker in {p}")
for cmd in [["python3","tooling/run_reference_workflow.py"],["python3","tooling/recovery_cert.py"],["python3","tooling/ecosystem_lock.py"]]:
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    if r.returncode: raise SystemExit("FAIL "+cmd[-1]+": "+r.stderr.strip())
print(f"PASS TSIC-17 forensic audit: {len(ids)} systems, {len(owners)} capabilities, {len(json_files)} JSON files, all phase gates present")
