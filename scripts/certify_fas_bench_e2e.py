#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(args,cwd,allowed=(0,)):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
 if p.returncode not in allowed: raise SystemExit(f'command failed ({p.returncode}): {args}\nstdout={p.stdout[-4000:]}\nstderr={p.stderr[-4000:]}')
 return p
def main():
 fas=Path(os.environ.get('TSIC_FAS_DIR',ROOT/'../fas')).resolve()
 bench=Path(os.environ.get('TSIC_FAS_BENCH_DIR',ROOT/'../fas-bench')).resolve()
 if not (fas/'pyproject.toml').is_file() or not (bench/'pyproject.toml').is_file(): raise SystemExit('FAS and FAS-Bench checkouts are required')
 with tempfile.TemporaryDirectory(prefix='tsic-fas-bench-') as td:
  work=Path(td); sample=work/'sample'; sample.mkdir(); (sample/'app.py').write_text('print(\"safe sample\")\n',encoding='utf-8')
  config=work/'fas-config.json'; config.write_text(json.dumps({'database_url':f'sqlite:///{work}/fas.db','object_store_path':str(work/'objects')}),encoding='utf-8')
  analysis=run([sys.executable,'-m','fas.cli','--config',str(config),'--format','json','analyze',str(sample)],fas,allowed=(0,2))
  payload=json.loads(analysis.stdout)
  analysis_obj=payload.get('analysis',payload)
  analysis_id=str(analysis_obj.get('id',''))
  status=str(analysis_obj.get('status',''))
  if not analysis_id or not status: raise SystemExit('FAS output missing analysis ID/status')
  digest=hashlib.sha256(analysis.stdout.encode()).hexdigest()
  # Fail closed: this smoke fixture is not sufficient evidence for a security verdict.
  submission={'benchmark_version':'0.1.0','schema_version':'0.1','submission_id':'SUB-TSIC-FAS-001','case_id':'FAS-001','system':{'system_name':'fas','system_version':'tsic-pinned','runtime':'python','tooling':['fas.cli']},'verdict':{'benchmark_version':'0.1.0','schema_version':'0.1','verdict':'UNKNOWN','reason_code':'UNKNOWN_INSUFFICIENT_EVIDENCE','confidence':0,'rationale':'FAS smoke artifact did not establish case-specific evidence; fail closed.','claim_ids':[],'evidence_ids':[],'attack_path_ids':[]},'findings':[],'claims':[],'evidence':[],'attack_paths':[],'impact':{},'remediation':None,'verification':None,'metadata':{'producer':'TSIC FAS adapter','fas_analysis_id':analysis_id,'fas_analysis_status':status,'fas_artifact_sha256':digest,'correlation_id':'tsic-05-smoke-001'}}
  sub=work/'submission.json'; sub.write_text(json.dumps(submission,sort_keys=True),encoding='utf-8')
  ev=run(['fas-bench','evaluate','finding','--case','FAS-001','--submission',str(sub),'--strict','--json'],bench,allowed=(0,1,2))
  try: result=json.loads(ev.stdout)
  except json.JSONDecodeError as e: raise SystemExit(f'FAS-Bench did not return JSON: {ev.stdout[-2000:]}') from e
  if not isinstance(result,dict) or not result: raise SystemExit('FAS-Bench returned an empty evaluation result')
  combined={'schema_version':'1.0.0','producer':'tsic-fas-bench-adapter','fas_analysis_id':analysis_id,'fas_status':status,'fas_artifact_sha256':digest,'submission_id':submission['submission_id'],'case_id':'FAS-001','evaluator':'fas-bench','evaluator_exit_code':ev.returncode,'evaluation_result':result,'fail_closed_expected':True}
  out=Path(os.environ.get('TSIC_EVALUATION_OUTPUT',ROOT/'artifacts/fas-bench/evaluation-artifact.json'))
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(combined,indent=2,sort_keys=True)+'\n',encoding='utf-8')
  print(json.dumps({'status':'pass','fas_analysis_id':analysis_id,'fas_status':status,'artifact_sha256':digest,'evaluator':'fas-bench','evaluation_exit_code':ev.returncode,'result_keys':sorted(result.keys()),'fail_closed':'UNKNOWN'}))
if __name__=='__main__': main()
