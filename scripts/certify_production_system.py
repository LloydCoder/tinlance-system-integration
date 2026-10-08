#!/usr/bin/env python3
"""TSIC-39 production system-of-systems certification."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    p=load("policies/production-system-baseline.json")
    eco=load("manifests/ecosystem.json")
    ids={x["id"] for x in eco["systems"]}
    for boundary in ["agent-platform","agent-os","fdse","fas","tsic"]:
        assert boundary in ids or boundary=="tsic", f"missing registered boundary: {boundary}"
    assert len(p["required_boundaries"])==6
    assert "no_duplicate_consequential_execution_authority" in p["invariants"]
    print("PASS TSIC-39 production system-of-systems certification")
if __name__=="__main__": main()
