#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
required=[
"README.md","LICENSE","SECURITY.md","CONTRIBUTING.md","GOVERNANCE.md","CODEOWNERS","VERSION",
".github/workflows/ci.yml","manifests/ecosystem.json","catalog/capabilities/authority.json",
"catalog/dependencies/initial.json","schemas/ecosystem-manifest.schema.json","schemas/authority.schema.json",
"schemas/dependency.schema.json","schemas/conformance.schema.json","conformance/requirements/phase0.json",
"docs/architecture/overview.md","docs/architecture/authority-model.md","docs/architecture/integration-topology.md",
"docs/architecture/trust-boundaries.md","docs/architecture/decision-records/ADR-0001-tsic-authority.md",
"docs/architecture/decision-records/ADR-0002-contracts.md","docs/standards/2026-baseline.md"
]
missing=[p for p in required if not (ROOT/p).is_file()]
if missing: raise SystemExit("FAIL missing: "+", ".join(missing))
for p in ROOT.rglob("*.json"):
    if ".git" in p.parts: continue
    try: json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: raise SystemExit(f"FAIL invalid JSON {p}: {e}")
eco=json.loads((ROOT/"manifests/ecosystem.json").read_text())
ids=[x["id"] for x in eco["systems"]]
if len(ids)!=len(set(ids)): raise SystemExit("FAIL duplicate system IDs")
if eco["ecosystem"]["integration_authority"]!="tsic": raise SystemExit("FAIL TSIC authority mismatch")
authority=json.loads((ROOT/"catalog/capabilities/authority.json").read_text())
seen={}
for x in authority["capabilities"]:
    if x["capability"] in seen and seen[x["capability"]]!=x["owner"]: raise SystemExit(f"FAIL conflicting owner: {x['capability']}")
    seen[x["capability"]]=x["owner"]
if any(x["owner"] not in ids for x in authority["capabilities"]): raise SystemExit("FAIL unregistered authority owner")
print(f"PASS Phase 0: {len(ids)} systems, {len(seen)} capabilities, all JSON valid, required docs present.")
