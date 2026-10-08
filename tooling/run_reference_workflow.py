#!/usr/bin/env python3
import json,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/"workflows/canonical.json").read_text())
required={"tenant_id":"tenant-demo","organization_id":"org-demo","workspace_id":"ws-demo","actor_id":"actor-demo","execution_id":str(uuid.uuid4()),"trace_id":"0"*32,"correlation_id":str(uuid.uuid4())}
for wf in cfg["workflows"]:
    if len(wf["steps"])<2: raise SystemExit("workflow too short: "+wf["id"])
    if wf["id"]=="acquisition-engineering" and wf["steps"][-1]!="fde": raise SystemExit("engineering route invalid")
    if wf["id"]=="transformation" and "transformation" not in wf["steps"]: raise SystemExit("transformation route missing")
    if wf["id"]=="agent-development" and wf["steps"][0]!="agent-developer": raise SystemExit("agent developer missing")
print(json.dumps({"status":"pass","workflows":len(cfg["workflows"]),"identity_fields":len(required)}))
