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
