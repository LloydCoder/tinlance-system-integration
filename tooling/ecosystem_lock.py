#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
eco=json.loads((ROOT/"manifests/ecosystem.json").read_text())
auth=json.loads((ROOT/"catalog/capabilities/authority.json").read_text())
ids={x["id"] for x in eco["systems"]}
owners={}
for x in auth["capabilities"]:
    if x["capability"] in owners and owners[x["capability"]]!=x["owner"]: raise SystemExit("duplicate authority")
    if x["owner"] not in ids: raise SystemExit("unregistered authority owner")
    owners[x["capability"]]=x["owner"]
print("PASS ecosystem lock")
