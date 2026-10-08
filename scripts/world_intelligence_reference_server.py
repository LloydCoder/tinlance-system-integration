#!/usr/bin/env python3
import json, os, threading, time
from pathlib import Path
from runtime.config import RuntimeConfig
from runtime.server import WorldIntelligenceServer
ROOT=Path(__file__).resolve().parents[1]
fixture=json.loads((ROOT/'fixtures/intelligence/acquisition-signal.json').read_text())
token=os.environ.get('WORLD_INTELLIGENCE_BEARER_TOKEN','tsic-world-token')
stores={'signals':[{'signal_id':fixture['signal_id'],'entity_id':fixture['entity_id'],'signal_type':fixture['signal_type'],'rule_id':'wi-modernization-v1','rule_version':'1','generated_at':fixture['observed_at'],'severity':'high','explanation':fixture['explanation'],'evidence_ids':[fixture['evidence_id']]}],'evidence':[{'evidence_id':fixture['evidence_id'],'observation_id':fixture['observation_id'],'artifact_id':fixture['artifact_id'],'source_id':fixture['source_id'],'status':'validated','quality_score':0.91,'observed_at':fixture['observed_at']}],'provenance':[{'provenance_id':'prov-55555555-5555-4555-8555-555555555555','entity_id':fixture['entity_id'],'activity_id':'activity-ingest-001','agent_id':'world-intelligence-fixture','generated_at':fixture['observed_at'],'used_artifact_id':fixture['artifact_id']}]}
cfg=RuntimeConfig(host='127.0.0.1',port=0,bearer_token=token,require_auth=True,storage_mode='memory')
server=WorldIntelligenceServer(('127.0.0.1',0),cfg,stores=stores)
thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
print(f'http://127.0.0.1:{server.server_address[1]}',flush=True)
try:
    while True: time.sleep(1)
except KeyboardInterrupt: pass
finally: server.shutdown(); server.server_close(); thread.join(timeout=2)
