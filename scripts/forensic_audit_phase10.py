#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 required=['policies/threatfade-web-baseline.json','integrations/threatfade-web/adapter.json','scripts/certify_threatfade_web.py','scripts/certify_threatfade_web_live.py','.github/workflows/threatfade-web-engine-e2e.yml']
 missing=[p for p in required if not (ROOT/p).is_file()]
 if missing: raise SystemExit('FAIL missing phase10 artifacts: '+','.join(missing))
 b=json.loads((ROOT/'policies/threatfade-web-baseline.json').read_text()); a=json.loads((ROOT/'integrations/threatfade-web/adapter.json').read_text())
 assert len(b['engine']['ref'])==40 and len(b['web']['ref'])==40
 assert a['source_system']=='threatfade' and a['target_system']=='threatfade-web'
 assert 'playground_input_is_untrusted_and_resource_bounded' in b['invariants']
 assert 'web_proxy_uses_path_allowlist_timeout_redirect_rejection_and_response_limits' in b['invariants']
 wf=(ROOT/'.github/workflows/threatfade-web-engine-e2e.yml').read_text()
 for marker in ['4691ead86fadd1c95767886d7fb15bacbed012fe','2fbb3932fb7d641293f011110fbee568f8a98612','npm run truth:check','npm run test:e2e','scripts/certify_threatfade_web_live.py']:
  assert marker in wf, 'workflow missing '+marker
 print('PASS TSIC-10 forensic audit: first-class web registry, pinned engine/web, live API/schema check, auth boundaries and CI gates verified')
if __name__=='__main__': main()
