#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def main():
 b=load('policies/threatfade-web-baseline.json'); a=load('integrations/threatfade-web/adapter.json'); m=load('manifests/ecosystem.json')
 systems={x['id']:x for x in m['systems']}
 assert b['authority']=='tsic' and b['engine']['repository']=='LloydCoder/tinlance-threatfade' and b['web']['repository']=='LloydCoder/tinlance-threatfade-web'
 assert len(b['engine']['ref'])==40 and len(b['web']['ref'])==40
 assert systems['threatfade-web']['governance_role']=='product_analyst_commercial_authority'
 assert a['source_system']=='threatfade' and a['target_system']=='threatfade-web'
 assert a['authority']['detection_and_analyst_authority']=='threatfade'
 assert a['authority']['product_and_analyst_presentation']=='threatfade-web'
 assert a['authority']['independent_evaluation']=='fas-bench'
 assert 'analyst_authorization_is_enforced_by_engine' in b['invariants']
 assert 'browser_never_receives_engine_credentials' in b['invariants']
 print('PASS TSIC-10 contract: ThreatFade Engine and ThreatFade Web are distinct authorities with explicit boundaries')
if __name__=='__main__': main()
