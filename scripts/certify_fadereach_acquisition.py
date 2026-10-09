#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={'tenant_id','source_id','artifact_id','observation_id','evidence_id','signal_id','opportunity_id','trace_id','campaign_id','outreach_action_id','provider_event_id','reply_id','meeting_id','revenue_event_id'}
def main():
 b=json.loads((ROOT/'policies/fadereach-acquisition-baseline.json').read_text())
 a=json.loads((ROOT/'integrations/fadereach/adapter.json').read_text())
 assert b['authority']=='tsic' and b['target']=='fadereach'
 assert len(b['repository']['ref'])==40
 assert REQUIRED.issubset(b['handoff_lineage'])
 assert b['execution_gate']['requires_cross_repository_contract_execution'] is True
 assert a['target_system']=='fadereach' and a['authority']['execution_authority']=='agent-platform'
 assert {'suppression_and_consent_controls_are_preserved','duplicate_actions_are_idempotent','provider_failures_are_recoverable'}.issubset(set(a['invariants']))
 print('PASS TSIC-04 baseline contract: FadeReach pinned, lineage complete, execution authority preserved')
if __name__=='__main__': main()
