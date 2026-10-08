#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(path: str):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def main():
    eco=load("manifests/ecosystem.json")
    graph=load("catalog/dependencies/graph.json")
    lock=load("policies/ecosystem-lock.json")
    phases=load("catalog/phases/registry.json")
    req=load("conformance/requirements/phase0-final.json")

    systems={x["id"]:x for x in eco["systems"]}
    assert eco["ecosystem"]["integration_authority"]=="tsic"
    assert len(systems)==len(eco["systems"])
    assert systems["tsic"]["governance_role"]=="ecosystem_integration_authority"
    assert systems["agent-platform"]["governance_role"]=="execution_authority"
    assert systems["fas-bench"]["governance_role"]=="independent_evaluation_authority"
    assert systems["threatfade-web"]["repository"]=="LloydCoder/tinlance-threatfade-web"
    assert systems["fde-mastery"]["repository"]=="LloydCoder/fde-mastery"
    assert systems["tinlance-com"]["repository"]=="LloydCoder/Tinlance"

    nodes={x["system"]:x for x in graph["nodes"]}
    assert set(nodes)==set(systems)
    assert len(nodes)==len(graph["nodes"])
    for node in graph["nodes"]:
        assert node["ci_gate"].startswith("TSIC-")
        assert node["contract_version"]

    for edge in graph["edges"]:
        assert edge["from"] in systems and edge["to"] in systems
        assert edge["from"]!=edge["to"]

    assert lock["authority"]=="tsic"
    assert lock["release_invariants"]["single_generic_consequential_execution_authority"]=="agent-platform"
    assert lock["release_invariants"]["fas_bench_is_not_a_fas_runtime_dependency"]=="true"

    seq=phases["sequence"]
    assert len(seq)==20
    assert [x["id"] for x in seq]==[f"TSIC-{i:02d}" for i in range(20)]
    assert seq[0]["entry_condition"]=="repository_authority_established"
    assert all(x["entry_condition"]=="previous_phase_green" for x in seq[1:])
    assert phases["completion_rule"]

    assert req["phase"]=="TSIC-00"
    assert len(req["requirements"])>=8

    print(f"PASS TSIC-00 authority lock: systems={len(systems)} nodes={len(nodes)} edges={len(graph['edges'])} phases={len(seq)}")

if __name__=="__main__":
    main()
