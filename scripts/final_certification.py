#!/usr/bin/env python3
"""Final TSIC-41 forensic certification."""
from __future__ import annotations
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PHASE_SCRIPTS=[
"scripts/certify_phase0.py",
"tooling/validate_phase0.py","tooling/run_reference_workflow.py","tooling/recovery_cert.py",
"tooling/ecosystem_lock.py","tooling/forensic_audit.py","tooling/security_scan.py",
"scripts/certify_acquisition_system.py","scripts/certify_engineering_route.py","scripts/certify_transformation_route.py",
"scripts/certify_delivery_evidence.py","scripts/certify_fas.py","scripts/certify_fas_bench.py",
"scripts/certify_threatfade.py","scripts/certify_bugflow.py","scripts/certify_hezqara.py",
"scripts/certify_economic_attribution.py","scripts/certify_closed_loop.py","scripts/certify_observability.py",
"scripts/certify_interoperability.py","scripts/certify_production_system.py","scripts/certify_commercial_aaas.py",
"scripts/certify_autonomous_revenue.py"]
REQUIRED_POLICIES=[
"policies/agent-system-baseline.json","policies/acquisition-system-baseline.json","policies/engineering-route-baseline.json",
"policies/transformation-route-baseline.json","policies/delivery-evidence-baseline.json","policies/fas-baseline.json",
"policies/fas-bench-baseline.json","policies/threatfade-baseline.json","policies/bugflow-baseline.json",
"policies/hezqara-baseline.json","policies/economic-attribution-baseline.json","policies/closed-loop-baseline.json",
"policies/observability-baseline.json","policies/interoperability-baseline.json","policies/production-system-baseline.json",
"policies/commercial-aaas-baseline.json","policies/autonomous-revenue-baseline.json"]
PRIVATE_KEY=re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA|PRIVATE) KEY-----")
def run(script):
 r=subprocess.run([sys.executable,script],cwd=ROOT,capture_output=True,text=True)
 if r.returncode: raise SystemExit(f"FAIL {script}: {r.stdout.strip()} {r.stderr.strip()}")
 print(r.stdout.strip())
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def forensic_scan():
 for p in REQUIRED_POLICIES:
  if not (ROOT/p).is_file(): raise SystemExit(f"FAIL missing final policy: {p}")
 seen=set()
 for path in (ROOT/"integrations").rglob("*.json"):
  obj=load(str(path.relative_to(ROOT)))
  aid=obj.get("adapter_id")
  if aid:
   if aid in seen: raise SystemExit(f"FAIL duplicate adapter ID: {aid}")
   seen.add(aid)
 for path in ROOT.rglob("*"):
  if not path.is_file() or ".git" in path.parts or path in {ROOT/"scripts/final_certification.py",ROOT/"tooling/forensic_audit.py"}: continue
  if path.suffix.lower() not in {".md",".json",".py",".yml",".yaml",".txt"}: continue
  t=path.read_text(encoding="utf-8",errors="strict")
  if "TODO" in t or "TBD" in t: raise SystemExit(f"FAIL unresolved placeholder: {path}")
  if PRIVATE_KEY.search(t): raise SystemExit(f"FAIL private-key marker: {path}")
 wf=load("workflows/canonical.json")
 expected={"acquisition-engineering","transformation","agent-development","acquisition-feedback","commercial-aaas","autonomous-revenue"}
 if {x["id"] for x in wf["workflows"]}!=expected: raise SystemExit("FAIL final canonical workflow set")
 eco=load("manifests/ecosystem.json")
 systems={x["id"]:x for x in eco["systems"]}
 assert "fas-bench" in systems and systems["fas-bench"]["governance_role"]=="independent_evaluation_authority"
 assert systems["fas-bench"]["repository"]=="LloydCoder/fas-bench"
 print(f"PASS final forensic repository scan: adapters={len(seen)} policies={len(REQUIRED_POLICIES)} systems={len(systems)}")
def main():
 for script in PHASE_SCRIPTS: run(script)
 forensic_scan()
 print("PASS TSIC-31..41 FINAL SYSTEM-OF-SYSTEMS FORENSIC CERTIFICATION")
if __name__=="__main__": main()
