#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
 b=load('policies/fde-vertical-baseline.json'); a=load('integrations/fde-mastery/adapter.json'); f=load('integrations/fdse/adapter.json')
 assert b['authority']=='tsic' and b['routes']==['engineering','transformation']
 assert b['fdse']['repository']=='LloydCoder/tinlance-fdse' and len(b['fdse']['ref'])==40
 assert b['fde_mastery']['repository']=='LloydCoder/fde-mastery' and len(b['fde_mastery']['ref'])==40
 assert a['source_system']=='fdse' and a['target_system']=='fde-mastery'
 assert a['authority']['execution_authority']=='agent-platform'
 assert 'fde_mastery' in f['target_system'] or f['target_system']=='fdse'
 required={'identity-context','event-envelope','delivery-semantics','trace-context','economic-attribution'}
 assert {x['tsic_contract'] for x in a['contract_bindings']}==required
 assert 'engineering_and_transformation_are_distinct_routes' in b['invariants']
 assert 'customer_approval_is_required_for_consequential_changes' in b['invariants']
 print('PASS TSIC-07 FDE Mastery baseline: routes, authority, handoff lineage and economic attribution verified')
if __name__=='__main__': main()
