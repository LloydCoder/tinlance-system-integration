#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=[
"manifests/ecosystem.json","catalog/capabilities/authority.json","catalog/dependencies/graph.json",
"catalog/services/registry.json","catalog/contracts/registry.json","catalog/architecture/canonical.json",
"catalog/authority/reconciliation.json","catalog/phases/registry.json","policies/ecosystem-lock.json",
"schemas/ecosystem-manifest.schema.json","schemas/dependency-graph.schema.json","schemas/ecosystem-lock.schema.json",
"conformance/requirements/phase0-final.json"]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
    missing=[p for p in REQUIRED if not (ROOT/p).is_file()]
    if missing: raise SystemExit('FAIL missing artifacts: '+','.join(missing))
    for p in ROOT.rglob('*.json'):
        if '.git' in p.parts: continue
        try: json.loads(p.read_text(encoding='utf-8'))
        except Exception as e: raise SystemExit(f'FAIL invalid JSON {p}: {e}')
    eco=load('manifests/ecosystem.json'); systems={x['id']:x for x in eco['systems']}
    if len(systems)!=len(eco['systems']): raise SystemExit('FAIL duplicate system IDs')
    if eco['ecosystem']['integration_authority']!='tsic': raise SystemExit('FAIL TSIC authority mismatch')
    expected={'tsic':'LloydCoder/tinlance-system-integration','agent-platform':'LloydCoder/tinlance-agent-platform','agent-platform-sdk':'LloydCoder/tinlance-agent-platform-sdk','agent-os':'LloydCoder/tinlance-agent-os','agent-developer':'LloydCoder/tinlance-agent-developer','world-intelligence':'LloydCoder/tinlance-world-intelligence','tads':'LloydCoder/tinlance-tads','sdea':'LloydCoder/tinlance-sdea','reconos':'LloydCoder/reconos-ofe','fadereach':'LloydCoder/fadereach','fas':'LloydCoder/fas','fas-bench':'LloydCoder/fas-bench','fdse':'LloydCoder/tinlance-fdse','fde-mastery':'LloydCoder/fde-mastery','fdse-toolkit':'LloydCoder/Tinlance-FDSE-toolkit','threatfade':'LloydCoder/tinlance-threatfade','threatfade-web':'LloydCoder/tinlance-threatfade-web','bugflow':'LloydCoder/bugflow-elite','hezqara':'LloydCoder/hezqara','hezcast':'Tinlance/hezcast-engine','tinlance-com':'LloydCoder/Tinlance'}
    for sid,r in expected.items():
        if systems.get(sid,{}).get('repository')!=r: raise SystemExit(f'FAIL repository mapping for {sid}')
    roles={x['id']:x['governance_role'] for x in eco['systems']}
    if roles.get('agent-platform')!='execution_authority' or roles.get('fas-bench')!='independent_evaluation_authority': raise SystemExit('FAIL authority roles')
    auth=load('catalog/capabilities/authority.json'); owners={}
    for x in auth['capabilities']:
        if x['owner'] not in systems: raise SystemExit('FAIL unregistered authority owner')
        if x['capability'] in owners and owners[x['capability']]!=x['owner']: raise SystemExit('FAIL conflicting authority')
        owners[x['capability']]=x['owner']
    for s in eco['systems']:
        for c in s['authority']:
            if owners.get(c)!=s['id']: raise SystemExit('FAIL authority mismatch: '+c)
    graph=load('catalog/dependencies/graph.json'); nodes={x['system']:x for x in graph['nodes']}
    if set(nodes)!=set(systems): raise SystemExit('FAIL graph node set differs from ecosystem')
    for e in graph['edges']:
        if e['from'] not in systems or e['to'] not in systems: raise SystemExit('FAIL graph edge references unknown system')
    canonical=load('catalog/architecture/canonical.json')
    if {x['id'] for x in canonical['systems']}!=set(systems): raise SystemExit('FAIL canonical architecture differs from ecosystem')
    services=load('catalog/services/registry.json')
    if len({x['id'] for x in services['services']})!=len(services['services']): raise SystemExit('FAIL duplicate service IDs')
    if any(x['system'] not in systems for x in services['services']): raise SystemExit('FAIL service references unknown system')
    contracts=load('catalog/contracts/registry.json'); cids={x['id'] for x in contracts['contracts']}
    required={'identity-context','agent-registration','event-envelope','delivery-semantics','trace-context','model-routing-authority','agent-interoperability-gate','economic-attribution','adapter-rules','failure-matrix','ecosystem-lock','canonical-workflows','ecosystem-manifest','dependency-graph','tsic-phase-registry'}
    if not required<=cids: raise SystemExit('FAIL incomplete contract registry')
    phases=load('catalog/phases/registry.json')['sequence']
    if [x['id'] for x in phases]!=[f'TSIC-{i:02d}' for i in range(20)]: raise SystemExit('FAIL canonical phase sequence')
    if any(x['entry_condition']!='previous_phase_green' for x in phases[1:]): raise SystemExit('FAIL serial phase gate')
    adapters=load('integrations/adapters/registry.json'); aids={x['id'] for x in adapters['adapters']}
    if 'fas-to-fas-bench-evaluation' not in aids: raise SystemExit('FAIL FAS-Bench adapter')
    if any(x['from'] not in systems or x['to'] not in systems for x in adapters['adapters']): raise SystemExit('FAIL adapter references unknown system')
    lock=load('policies/ecosystem-lock.json')
    if lock['authority']!='tsic' or lock['release_invariants'].get('single_generic_consequential_execution_authority')!='agent-platform': raise SystemExit('FAIL lock invariants')
    for cmd in [['python3','scripts/certify_phase0.py'],['python3','tooling/run_reference_workflow.py'],['python3','tooling/recovery_cert.py'],['python3','tooling/ecosystem_lock.py']]:
        r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        if r.returncode: raise SystemExit('FAIL '+cmd[-1]+': '+r.stdout+' '+r.stderr)
    print(f'PASS TSIC-00 forensic audit: systems={len(systems)} nodes={len(nodes)} edges={len(graph["edges"])} adapters={len(aids)} phases={len(phases)}')
if __name__=='__main__': main()
