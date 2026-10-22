"""Read-only spec verification and exclusive non-executable step-4 templates; never launches."""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ART=HERE.parent
C4=ART/'step4_launch_readiness_c4'
R5='b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
REF='237ef3d41daf4d99b0aafed3e90b27b095a741a9f66ea06ea34f3e44876d47bb'
def pin(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def readpin(ref):
 if pin(ref['path'])!=ref:raise ValueError('PIN_MISMATCH:'+ref['path'])
 return json.loads(Path(ref['path']).read_bytes())
def write(p,x):
 data=(json.dumps(x,indent=2,allow_nan=False,sort_keys=True)+'\n').encode()
 with p.open('xb') as f:f.write(data)
def prepare(out):
 out=Path(out)
 if out.parent.resolve()!=HERE.resolve() or out.exists() or out.is_symlink():raise ValueError('NEW_OWNED_DIRECTORY_REQUIRED')
 dry=C4/'dryplans/DRYPLANS_C4V002.json';inv=C4/'inventory/INVENTORY_C4V001.json';order=C4/'launch_order/LAUNCH_ORDER_C4V001.json'
 d=json.loads(dry.read_bytes());inventory=json.loads(inv.read_bytes())
 rows=[r for r in d['records'] if r['family']!='CAMPAIGN_W1']
 if len(rows)!=33 or len({r['name'] for r in rows})!=33:raise ValueError('DIRECT_ROSTER_DEFECT')
 batches={'HEADLINE':[],'DIII':[],'SENS_LO':[],'SENS_HI':[]};checks={};refs=[pin(dry),pin(inv),pin(order)]
 monitor=inventory['orchestrator']['monitor'];checks['monitor_pin']=pin(monitor['path'])==monitor
 for r in rows:
  case=r['name'];spec=readpin(r['spec']);checks[case+':spec']=True
  dr=pin(r['driver']['path']);checks[case+':driver']=dr==r['driver']
  tail=r['tail_on'];distance=spec['physical']['distance_Mpc']
  if type(distance) not in (int,float) or not math.isfinite(distance):raise ValueError('DISTANCE')
  if r['family']=='DECIDING_III':
   batch='DIII';role='REFERENCE_V009GEO' if case.endswith('_V009GEO') else 'NEW_R5'
   checks[case+':driver_role']=(dr['sha256']==(REF if role=='REFERENCE_V009GEO' else R5))
   checks[case+':tail_off']=tail is False and spec['numerics'].get('uv_tail') is None
  elif r['family'] in ('SENS_CORNER','SENS_DISTANCE'):
   batch='SENS_LO' if distance<4.04 else 'SENS_HI';role='PRODUCTION_R5'
   checks[case+':driver_role']=dr['sha256']==R5
   checks[case+':tail_on']=tail is True and isinstance(spec['numerics'].get('uv_tail'),dict)
  else:
   batch='HEADLINE';role='PRODUCTION_R5';checks[case+':driver_role']=dr['sha256']==R5
   checks[case+':tail_on']=tail is True and isinstance(spec['numerics'].get('uv_tail'),dict)
   checks[case+':headline_D']=distance==4.04
  provisional=None
  if r.get('post_adoption_probe'):
   q=r['post_adoption_probe'];provisional={'path':q['path'],'sha256':q['sha256']};readpin(provisional);checks[case+':provisional_pin']=True
  batches[batch].append({'case':case,'family':r['family'],'driver_role':role,'driver':dr,'spec':r['spec'],'post_adoption_provisional_spec':provisional,'tail_on':tail,'distance_Mpc':distance,'spec_status':'CLAUDE4_DRY_ONLY_PENDING_FINAL_ROOT_BINDING','prelaunch':None,'outdir':None,'receipt':None,'monitor_log':None,'wall_cap_s':None,'rss_cap_bytes':None,'output_cap_bytes':None,'pending':['SEALED_ADOPT_TAIL','ROOT_STEP4_ADMISSION','FINAL_SPEC_AND_PRELAUNCH','ROOT_CAPS_AND_OUTPUT_PATHS']+(['PER_D_SENSITIVITY_REGISTRATION'] if batch.startswith('SENS') else []),'source_record':r['record']})
 checks['batch_counts']={k:len(v) for k,v in batches.items()}=={'HEADLINE':11,'DIII':4,'SENS_LO':9,'SENS_HI':9}
 for edge in ('LOW','HIGH'):
  pair=[r for r in batches['DIII'] if '_'+edge+'_' in r['case']]
  checks['DIII_'+edge+'_pair_same_bytes']=len(pair)==2 and pair[0]['spec']['sha256']==pair[1]['spec']['sha256']
  checks['DIII_'+edge+'_same_distance']=len({r['distance_Mpc'] for r in pair})==1
 if not all(v is True for v in checks.values()):raise ValueError('CHECKS_FALSE:'+str([k for k,v in checks.items() if v is not True]))
 def sortkey(c):
  n=c['case']
  if n.startswith('DECIDING_III'):return (0 if '_LOW_' in n else 1,0 if n.endswith('V009GEO') else 1)
  if n=='TAIL_REANCHOR':return (0,n)
  if n=='WORKERS_8_CANDIDATE_ANCHOR':return (1,n)
  if n=='HEADLINE_TRIAL':return (2,n)
  return (4 if n.startswith('SENS_DISTANCE') else 3,n)
 plans={}
 for key,calls in batches.items():
  calls.sort(key=sortkey)
  plans[key]={'schema':'UNT_STEP4_PLAN_TEMPLATE_CX1V001','status':'UNBOUND_REFUSE_EXECUTION','batch':key,'author':'Codex1 build lane; Claude2 alone launches','sources':refs,'launcher':None,'guard':None,'monitor':monitor,'step4_admission':None,'root_config':None,'seal':None,'calls':calls,'route_a_admission':{'max_active':3,'minimum_free_percent':25.0,'poll_seconds':60,'first_case_exception':calls[0]['case'],'ramp':'previous_first_completed_route_a_iteration','status':'PROPOSAL_PENDING_ROOT_ADMISSION'},'runtime_constraints':{'single_thread_blas':True,'normal_qos_at_root_launch':True,'sleep_assertion':'caffeinate -i -w <launcher_pid>','step2_route_a_inactive_required':True,'campaign_inactive_required':True,'one_step4_batch_at_a_time':True,'root_selected_internal_ssd_outputs':True},'limitations':['Every call including DIII requires sealed ADOPT_TAIL under0620.','Claude4 owns final specs; provisional/dry files are not admitted scientific inputs.','Null paths, caps and evidence are mandatory refusal, not defaults.','The proposed route-A cap3 is not root adoption; root chooses a reviewed cap before binding.','Campaign launches and unregistered post-calibration S1 are outside this direct-run packet.','v009geo is proposed only as the explicitly registered tail-OFF reference, never a production fallback.']}
 out.mkdir()
 for k,v in plans.items():write(out/(k+'_PLAN_TEMPLATE_CX1V001.json'),v)
 report={'schema':'UNT_STEP4_TEMPLATE_VERIFICATION_CX1V001','date_u':subprocess.check_output(['date','-u'],text=True).strip(),'label':'TESTED pins/roster only; production UNTESTED','verdict':'PASS','checks':checks,'checks_passed':len(checks),'direct_calls':33,'batch_counts':{k:len(v) for k,v in batches.items()},'launches':0,'sources':refs,'plans':[pin(out/(k+'_PLAN_TEMPLATE_CX1V001.json')) for k in plans],'generator':pin(__file__)}
 write(out/'TEMPLATE_VERIFICATION_CX1V001.json',report)
 print(json.dumps({'verdict':'PASS','checks':len(checks),'batch_counts':report['batch_counts'],'report':pin(out/'TEMPLATE_VERIFICATION_CX1V001.json')},indent=1))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',required=True);prepare(a.parse_args().out)
