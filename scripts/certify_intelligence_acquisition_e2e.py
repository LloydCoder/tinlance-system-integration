#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys, urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID
ROOT=Path(__file__).resolve().parents[1]
def get_json(url,token):
    req=urllib.request.Request(url,headers={'Authorization':f'Bearer {token}','X-Request-ID':'tsic-02-001'})
    with urllib.request.urlopen(req,timeout=5) as response: return json.loads(response.read().decode())
def main():
    base=os.environ.get('WORLD_INTELLIGENCE_URL'); token=os.environ.get('WORLD_INTELLIGENCE_BEARER_TOKEN')
    if not base or not token: raise SystemExit('World Intelligence endpoint and credential are required')
    fixture=json.loads((ROOT/'fixtures/intelligence/acquisition-signal.json').read_text())
    payload=get_json(base+'/v1/signals?limit=10',token); items=payload['items']; assert len(items)==1
    signal=items[0]; assert signal['signal_id']==fixture['signal_id']; assert signal['entity_id']==fixture['entity_id']
    assert fixture['evidence_id'] in signal['evidence_ids']
    evidence_id=fixture['evidence_id']; evidence_uuid=UUID(evidence_id)
    sys.path.insert(0,str(ROOT/'../world-intelligence')); sys.path.insert(0,str(ROOT/'../tinlance-tads/src')); sys.path.insert(0,str(ROOT/'../tinlance-sdea/src'))
    from packages.contracts.observation import Observation, ObservationStatus
    from packages.contracts.evidence import Evidence, EvidenceStatus
    from packages.provenance.record import ProvenanceRecord
    from packages.contracts.signal import Signal as WorldSignal
    from tads_signals import DetectedSignal, SignalKind, SignalState
    from tads_opportunities import OpportunityResult
    from tads_integrations import OpportunityHandoff as TADSHandoff
    from tinlance_sdea.signals import SignalRecord
    from tinlance_sdea.capability import Capability, CapabilityMapping
    from tinlance_sdea.opportunity import OpportunityRecord, make_handoff
    from tinlance_sdea.acquisition import AcquisitionMode, recommend
    observed=datetime.fromisoformat(fixture['observed_at'].replace('Z','+00:00'))
    observation=Observation(fixture['observation_id'],fixture['artifact_id'],fixture['source_id'],fixture['entity_id'],'adopted',fixture['attributes']['technology'],observed,observed,status=ObservationStatus.VALIDATED,provenance_id='prov-55555555-5555-4555-8555-555555555555')
    evidence=Evidence(evidence_id,fixture['observation_id'],fixture['artifact_id'],fixture['source_id'],'fingerprint-tsic-02',EvidenceStatus.VALIDATED,0.91,observed,'prov-55555555-5555-4555-8555-555555555555')
    provenance=ProvenanceRecord('prov-55555555-5555-4555-8555-555555555555',fixture['entity_id'],'activity-ingest-001','world-intelligence-fixture',observed,fixture['artifact_id'])
    world_signal=WorldSignal(fixture['signal_id'],'wi-modernization-v1','1',observed,'high',fixture['explanation'],(evidence_id,))
    detected=DetectedSignal(SignalKind.TECHNOLOGY,'security-platform-modernization',SignalState.VALIDATED,fixture['strength'],fixture['freshness'],fixture['reliability'],fixture['observation_id'],(evidence_id,),(fixture['explanation'],))
    assert detected.quality>0.7 and world_signal.evidence_ids==(evidence_id,)
    opportunity_id='55555555-5555-4555-8555-555555555555'
    tads_result=OpportunityResult(fixture['entity_id'],0.92,0.91,0.9,0.0,0.91,0.9,'security-platform modernization requires engineering capability','FDE security platform engineering',('technology modernization','fresh evidence'),(),(evidence_id,))
    handoff=TADSHandoff(opportunity_id,fixture['entity_id'],0.91,0.9,tads_result.hypothesis,(evidence_id,),'CISO / VP Engineering','platform security modernization','immediate',datetime.now(UTC)+timedelta(days=14),'handoff-tsic-02',audit_correlation_id=fixture['trace_id'])
    assert handoff.schema_version=='tads.fadereach.v1'
    sdea_signal=SignalRecord(id=UUID(fixture['signal_id']),entity_id=fixture['entity_id'],signal_type=fixture['signal_type'],source_event_id=fixture['event_id'],occurred_at=observed,observed_at=observed,evidence_ids=(evidence_uuid,),attributes={'technology':fixture['attributes']['technology'],'change':fixture['attributes']['change']})
    capability=Capability(fixture['capability_id'],'Platform Security Engineering','1.0.0')
    mapping=CapabilityMapping(source='tsic-02',capability_id=capability.id,confidence=0.91,rationale='world signal and TADS hypothesis map to platform security engineering')
    sdea_opportunity=OpportunityRecord(id=UUID(opportunity_id),entity_id=fixture['entity_id'],capability_id=capability.id,confidence=0.9,evidence_ids=(evidence_uuid,),rationale='TADS evidence-backed hypothesis promoted into SDEA opportunity intelligence')
    recommendation=recommend(UUID(opportunity_id),AcquisitionMode.FDE,0.9,'bounded engineering delivery fits the capability need')
    sdea_handoff=make_handoff(UUID(opportunity_id),fixture['entity_id'],capability.id,0.9,(evidence_uuid,),sdea_opportunity.rationale)
    assert recommendation.requires_human_approval is True
    assert sdea_handoff.evidence_ids==(evidence_uuid,)
    assert mapping.capability_id==sdea_opportunity.capability_id
    lineage={fixture['source_id'],fixture['artifact_id'],fixture['observation_id'],evidence_id,fixture['event_id'],fixture['signal_id'],opportunity_id,fixture['trace_id']}
    assert len(lineage)==8
    print(json.dumps({'status':'pass','world_intelligence':'http_signal_read','tads':'signal_to_opportunity_handoff','sdea':'opportunity_to_recommendation','evidence_id':evidence_id,'trace_id':fixture['trace_id'],'human_approval_required':recommendation.requires_human_approval}))
if __name__=='__main__': main()
