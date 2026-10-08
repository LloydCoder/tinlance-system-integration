#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base=["README.md","LICENSE","SECURITY.md","CONTRIBUTING.md","GOVERNANCE.md","CODEOWNERS","VERSION",".github/workflows/ci.yml","manifests/ecosystem.json","catalog/capabilities/authority.json","catalog/dependencies/initial.json","schemas/ecosystem-manifest.schema.json","schemas/authority.schema.json","schemas/dependency.schema.json","schemas/conformance.schema.json","conformance/requirements/phase0.json"]
missing=[p for p in base if not (ROOT/p).is_file()]
if missing: raise SystemExit("FAIL missing foundation: "+", ".join(missing))
for p in ROOT.rglob("*.json"):
    if ".git" in p.parts: continue
    try: json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: raise SystemExit(f"FAIL invalid JSON {p}: {e}")
eco=json.loads((ROOT/"manifests/ecosystem.json").read_text(encoding="utf-8"))
ids=[x["id"] for x in eco["systems"]]
if len(ids)!=len(set(ids)): raise SystemExit("FAIL duplicate system IDs")
if eco["ecosystem"]["integration_authority"]!="tsic": raise SystemExit("FAIL TSIC authority mismatch")
auth=json.loads((ROOT/"catalog/capabilities/authority.json").read_text(encoding="utf-8"))
seen={}
for x in auth["capabilities"]:
    if x["capability"] in seen and seen[x["capability"]]!=x["owner"]: raise SystemExit("FAIL conflicting owner: "+x["capability"])
    seen[x["capability"]]=x["owner"]
if any(x["owner"] not in ids for x in auth["capabilities"]): raise SystemExit("FAIL unregistered authority owner")
def gate(marker, paths):
    if (ROOT/marker).is_file():
        miss=[p for p in paths if not (ROOT/p).is_file()]
        if miss: raise SystemExit(f"FAIL {marker}: missing "+", ".join(miss))
gate("conformance/requirements/phase1.json",["catalog/architecture/canonical.json","catalog/authority/reconciliation.json","schemas/canonical-architecture.schema.json","schemas/authority-reconciliation.schema.json","docs/architecture/canonical-system-model.md","docs/architecture/authority-reconciliation.md"])
gate("conformance/requirements/phase2.json",["contracts/common/identity-context.json","contracts/agents/registration.json","schemas/identity-context.schema.json","schemas/agent-registration.schema.json","docs/architecture/identity-and-agent-registration.md"])
gate("conformance/requirements/phase3.json",["contracts/events/envelope.json","contracts/events/delivery-semantics.json","contracts/telemetry/trace-context.json","schemas/event-envelope.schema.json","schemas/delivery-semantics.schema.json","schemas/trace-context.schema.json","docs/contracts/event-and-trace-fabric.md"])
gate("conformance/requirements/phase4.json",["catalog/services/registry.json","catalog/contracts/registry.json","catalog/dependencies/graph.json","docs/architecture/service-contract-registry.md"])
gate("conformance/requirements/phase5.json",["contracts/models/routing-authority.json","contracts/agents/interoperability-gate.json","docs/architecture/model-and-agent-interoperability.md"])
gate("conformance/requirements/phase6.json",["integrations/adapters/registry.json","integrations/adapters/rules.json","docs/integrations/adapter-fabric.md"])
print(f"PASS TSIC gates through TSIC-11; systems={len(ids)} capabilities={len(seen)}")
