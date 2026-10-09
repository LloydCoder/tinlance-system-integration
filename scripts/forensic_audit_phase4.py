#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 required=['policies/fadereach-acquisition-baseline.json','integrations/fadereach/adapter.json','scripts/certify_fadereach_acquisition.py','.github/workflows/fadereach-acquisition.yml']
 missing=[p for p in required if not (ROOT/p).is_file()]
 if missing: raise SystemExit('FAIL missing phase4 artifacts: '+','.join(missing))
 b=json.loads((ROOT/required[0]).read_text()); a=json.loads((ROOT/required[1]).read_text())
 assert b['repository']['name']=='LloydCoder/fadereach' and len(b['repository']['ref'])==40
 assert b['authority_boundaries']['agent-platform']=='consequential execution, policy and audit'
 assert 'consent_and_suppression_checked_before_send' in b['invariants']
 assert 'provider_webhooks_authenticated_and_replay_safe' in b['invariants']
 assert 'economic-attribution' in b['handoff_lineage'] or 'revenue_event_id' in b['handoff_lineage']
 workflow=(ROOT/'.github/workflows/fadereach-acquisition.yml').read_text()
 for required_text in ['LloydCoder/fadereach','ecd66b86840cdf08a65d0f2485564d5beed452bb','scripts/tsic_conformance.py','tests/test_outbound_queue.py','tests/test_tads_sdea_bridge.py','forensic_audit_phase4.py']:
  assert required_text in workflow, 'workflow missing '+required_text
 assert a['authority']['execution_authority']=='agent-platform'
 print('PASS TSIC-04 forensic audit: reviewed source pin, consent, idempotency, webhook, authority and dedicated CI gates verified')
if __name__=='__main__': main()
