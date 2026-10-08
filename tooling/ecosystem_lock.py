#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
    eco=load('manifests/ecosystem.json'); ids={x['id'] for x in eco['systems']}
    auth=load('catalog/capabilities/authority.json'); owners={}
    for x in auth['capabilities']:
        if x['owner'] not in ids: raise SystemExit('FAIL unregistered authority owner')
        if x['capability'] in owners and owners[x['capability']]!=x['owner']: raise SystemExit('FAIL conflicting authority')
        owners[x['capability']]=x['owner']
    graph=load('catalog/dependencies/graph.json')
    if {x['system'] for x in graph['nodes']}!=ids: raise SystemExit('FAIL graph does not cover ecosystem')
    if any(x['from'] not in ids or x['to'] not in ids for x in graph['edges']): raise SystemExit('FAIL graph references unknown system')
    lock=load('policies/ecosystem-lock.json')
    if lock['authority']!='tsic': raise SystemExit('FAIL lock authority')
    if lock['release_invariants']['single_generic_consequential_execution_authority']!='agent-platform': raise SystemExit('FAIL execution authority')
    phases=load('catalog/phases/registry.json')['sequence']
    if len(phases)!=20 or [x['id'] for x in phases]!=[f'TSIC-{i:02d}' for i in range(20)]: raise SystemExit('FAIL canonical phases')
    print(f'PASS ecosystem lock: systems={len(ids)} edges={len(graph["edges"])} phases={len(phases)}')
if __name__=='__main__': main()
