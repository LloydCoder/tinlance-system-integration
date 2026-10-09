#!/usr/bin/env python3
from __future__ import annotations
import json,os,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def get(url):
 req=urllib.request.Request(url,headers={'Accept':'application/json','User-Agent':'tsic-threatfade-web-certifier'})
 with urllib.request.urlopen(req,timeout=5) as r:
  if r.status!=200: raise SystemExit(f'FAIL live engine HTTP {r.status}: {url}')
  return json.load(r)
def main():
 base=os.environ.get('THREATFADE_BASE_URL','').rstrip('/')
 web=Path(os.environ['THREATFADE_WEB_DIR'])
 if not base or not (web/'lib/api/models.ts').is_file(): raise SystemExit('FAIL missing live engine URL or web schemas')
 health=get(base+'/health'); version=get(base+'/version'); ready=get(base+'/ready')
 required_health={'status','tool','version','company','timestamp'}
 required_version={'name','version','company','license'}
 assert required_health.issubset(health), f'engine health schema drift: {sorted(required_health-set(health))}'
 assert required_version.issubset(version), f'engine version schema drift: {sorted(required_version-set(version))}'
 assert health['status']=='ok' and health['tool']=='ThreatFade'
 assert version['version']==health['version'] and isinstance(health['timestamp'],str)
 assert ready['status']=='ready' and ready['checks']['config'] is True
 models=(web/'lib/api/models.ts').read_text(encoding='utf-8')
 for field in sorted(required_health|required_version): assert field in models, 'web Zod contract missing '+field
 truth=json.loads((web/'content/engine-truth.json').read_text(encoding='utf-8'))
 assert truth['engineRepository']=='https://github.com/LloydCoder/tinlance-threatfade'
 assert truth['status'] in {'development','beta','production'}
 print(json.dumps({'status':'pass','engine_version':health['version'],'health_contract':'matched','version_contract':'matched','readiness':'ready','web_schema':'matched','truth_status':truth['status']},sort_keys=True))
if __name__=='__main__': main()
