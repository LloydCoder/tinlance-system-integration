#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/"reliability/failure-matrix.json").read_text())
required={"timeout","duplicate_event","invalid_identity","wrong_tenant","revoked_agent","crash"}
seen={x["id"] for x in m["scenarios"]}
missing=required-seen
if missing: raise SystemExit("missing recovery scenarios: "+",".join(sorted(missing)))
if any(not x.get("response") for x in m["scenarios"]): raise SystemExit("scenario without response")
print(f"PASS recovery certification scenarios={len(seen)}")
