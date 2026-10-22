"""Successor templates matching the guarded launcher interface; never execute."""
import hashlib, importlib.util, json, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
FILES={'guard':'step4_guard_cx1v005.py','launcher':'step4_launcher_cx1v005.py','binder':'step4_bind_cx1v004.py','direct_context':'step4_direct_preflight_cx1v001.py'}
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,v):
 b=(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(b)
def main():
 out=HERE/'templates_v002'
 if out.exists():raise ValueError('EXCLUSIVE_OUTPUT_DIRECTORY_REQUIRED')
 refs={k:pin(HERE/'impl'/v) for k,v in FILES.items()};plans=[];checks={}
 report=json.loads((HERE/'templates_v001/TEMPLATE_VERIFICATION_CX1V001.json').read_bytes())
 for r in report['plans']:
  p=Path(r['path']);assert pin(p)==r;d=json.loads(p.read_bytes());batch=d['batch']
  oldcalls=d['calls']
  d.update(schema='UNT_STEP4_LAUNCH_PLAN_CX1V001',binding_status='UNBOUND',launcher=refs['launcher'],guard=refs['guard'],launcher_log=None,source_template=r,build_tools=refs)
  d['route_a_admission']={'max_active':3,'minimum_free_percent':25,'poll_seconds':60,'source':'/usr/bin/memory_pressure','ramp':'previous_first_completed_route_a_iteration','first_case_memory_exemption':False}
  d['ramp_proposal_status']='REQUIRES_ROOT_ADMISSION; cap3 is a proposal from Claude4 metadata'
  checks[batch+':calls_unchanged']=d['calls']==oldcalls
  checks[batch+':unbound']=d['binding_status']=='UNBOUND' and all(c['pending'] and c['spec_status']!='ROOT_FINAL' for c in d['calls'])
  checks[batch+':root_fields_null']=d['launcher_log'] is None and all(all(c[k] is None for k in ('prelaunch','outdir','receipt','monitor_log','wall_cap_s','rss_cap_bytes','output_cap_bytes')) for c in d['calls'])
  plans.append(d)
 sp=importlib.util.spec_from_file_location('_template_guard',refs['guard']['path']);G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
 out.mkdir()
 for d in plans:
  p=out/(d['batch']+'_PLAN_TEMPLATE_CX1V002.json');write(p,d);r=pin(p)
  # Synthetic candidate authority is supplied only in memory, never published.
  fake={'schema':'UNT_STEP4_ADMISSION_CX1V001','authority':G.AUTHORITY,'status':'ROOT_AUTHORIZED','plan':r}
  try:G.validate(r,refs['launcher']['path'],_candidate_config=fake)
  except G.Refusal as e:checks[d['batch']+':actual_guard_refuses_unbound']=str(e)=='UNBOUND_PLAN_REFUSED'
  else:checks[d['batch']+':actual_guard_refuses_unbound']=False
 assert all(v is True for v in checks.values()),checks
 result={'date_u':subprocess.check_output(['date','-u'],text=True).strip(),'label':'TESTED template interface and refusal; production UNTESTED','checks':checks,'verdict':'PASS','checks_passed':len(checks),'direct_calls':sum(len(x['calls']) for x in plans),'plans':[pin(out/(d['batch']+'_PLAN_TEMPLATE_CX1V002.json')) for d in plans],'implementation':refs,'generator':pin(Path(__file__)),'predecessor_check':pin(HERE/'templates_v001/TEMPLATE_VERIFICATION_CX1V001.json'),'scientific_processes_started':0}
 write(out/'TEMPLATE_VERIFICATION_CX1V002.json',result);print(json.dumps({'verdict':'PASS','checks':len(checks),'direct_calls':result['direct_calls'],'report':pin(out/'TEMPLATE_VERIFICATION_CX1V002.json')},indent=1))
if __name__=='__main__':main()
