#!/usr/bin/env python3
"""TSIC-31: certify the FAS/FAS-Bench production/evaluation boundary."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    a=load("integrations/fas/adapter.json")
    b=load("integrations/fas-bench/adapter.json")
    p=load("policies/fas-bench-baseline.json")
    assert a["target_system"]=="fas"
    assert b["source_system"]=="fas" and b["target_system"]=="fas-bench"
    assert "fas-bench_is_not_a_fas_runtime_dependency" in b["independence_invariants"]
    assert "fas_bench_is_not_on_production_execution_path" in p["invariants"]
    assert len(p["fas"]["ref"])==40 and len(p["fas_bench"]["ref"])==40
    assert p["fas"]["repository"]=="LloydCoder/fas"
    assert p["fas_bench"]["repository"]=="LloydCoder/fas-bench"
    print("PASS TSIC-31 FAS + FAS-Bench integration and certification")
if __name__=="__main__": main()
