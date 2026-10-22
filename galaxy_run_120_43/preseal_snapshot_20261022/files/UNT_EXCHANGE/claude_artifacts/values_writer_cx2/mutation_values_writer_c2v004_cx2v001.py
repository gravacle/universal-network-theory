"""Synthetic mutation spot checks. New copies only; invokes the port or gate suite on each mutant."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
MUTANTS=[
 ('M01_eps_broadcast','port',"bound = sr['bound_km_s']","bound = [1.0] * len(sr['bound_km_s'])"),
 ('M02_apply_inclination','port',"'eps_km_s': eps,","'eps_km_s': [None if e is None else e * (co['inclination']['sin_ratio'] or 1.0) for e in eps],"),
 ('M03_route_ignored','gate',"if rec.get('route') != NGC_ACCEPTANCE_ROUTE:","if False:"),
 ('M04_phase1_gate_removed','gate',"and (kind != 'phase1_values' or (acc is not None and acc['counts_for_member_valid'] is True))","and True"),
 ('M05_flagged_accepted','gate',"MEMBER_ACCEPTANCE_READINGS = ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT')","MEMBER_ACCEPTANCE_READINGS = ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT', 'ACCEPTED_PASS_FLAGGED')"),
 ('M06_schema_ignored','gate',"if not isinstance(rec, dict) or rec.get('schema') not in ACCEPTANCE_SCHEMAS:","if not isinstance(rec, dict):"),
 ('M07_handoff_ignored','gate',"if not is_pin(h) or h['sha256'] not in ACCEPTANCE_HANDOFFS:","if not is_pin(h):"),
 ('M08_call_binding_ignored','gate',"if rec.get('result') != c['result_pin'] or rec.get('call_dir') != str(c['call']):","if False:"),
 ('M09_reading_gate_removed','gate',"'counts_for_member_valid': g5 and rd in MEMBER_ACCEPTANCE_READINGS,","'counts_for_member_valid': g5,"),
]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--module',required=True);ap.add_argument('--port',required=True);ap.add_argument('--gate',required=True);ap.add_argument('--work',required=True);a=ap.parse_args()
 root=Path(a.work);root.mkdir(parents=True,exist_ok=False);src=Path(a.module).read_text();rows=[]
 for name,kind,old,new in MUTANTS:
  count=src.count(old)
  if count!=1:
   rows.append({'name':name,'applied':False,'site_count':count,'killed':False});print(name,'NOT_APPLIED',count,flush=True);continue
  d=root/name;d.mkdir();p=d/'mutant.py'
  with p.open('x') as f:f.write(src.replace(old,new,1))
  run=subprocess.run([sys.executable,'-I','-B',getattr(a,kind),'--module',str(p),'--work',str(d/'test')],capture_output=True,text=True)
  result=d/'test'/('RESULT_GATE_TESTS_CX2V001.json' if kind=='gate' else 'RESULTS_PORTED_SUITE_CX2V001.json')
  data=json.loads(result.read_bytes()) if result.exists() else {}
  fails=[x for x in data.get('tests',data.get('results',[])) if not x.get('ok',False)]
  killed=run.returncode!=0 and bool(fails) and not any(x.get('test')=='SUITE CRASH' for x in fails)
  rows.append({'name':name,'kind':kind,'applied':True,'killed':killed,'exit':run.returncode,
    'mutant':{'path':str(p),'sha256':sha(p)},'result':{'path':str(result),'sha256':sha(result)} if result.exists() else None,
    'failures':fails[:5],'stderr_tail':run.stderr[-500:]})
  print(name,'KILLED' if killed else 'SURVIVED_OR_INFRA_ERROR',flush=True)
 summary={'schema':'CX2_VALUES_WRITER_MUTATIONS_V001','date_u':subprocess.check_output(['/bin/date','-u'],text=True).strip(),
  'module':{'path':a.module,'sha256':sha(a.module)},'port_sha256':sha(a.port),'gate_sha256':sha(a.gate),'script_sha256':sha(__file__),
  'n':len(rows),'killed':sum(x['killed'] for x in rows),'mutants':rows,'label':'TESTED','synthetic_only':True}
 out=root/'RESULT_MUTATIONS_CX2V001.json'
 with out.open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
 print('%d/%d killed'%(summary['killed'],summary['n']))
 return 0 if summary['killed']==summary['n'] else 1
if __name__=='__main__':sys.exit(main())
