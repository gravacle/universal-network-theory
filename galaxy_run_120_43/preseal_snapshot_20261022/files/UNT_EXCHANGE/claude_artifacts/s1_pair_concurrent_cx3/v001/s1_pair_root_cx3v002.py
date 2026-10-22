"""Root-only S1 pair handoff, A274/0838. Default DRY; actual launch belongs only to Claude2.
Preserves registration-in-force, real filled-spec replay, separate per-case native preflights,
step-2/campaign-state attestation, inactive process-table check, exclusive prelaunch/outcome records.
C14's single-call and campaign-window scheduling restrictions are superseded by A274.
The pair launcher holds the original machine lock, ramp and disk checks for both calls.
"""
import argparse,hashlib,json,os,subprocess,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
GUARD={'path':str(HERE/'step4_guard_c2v014_s1pair_cx3v001.py'),'sha256':'1274a39a19a7d8540858b8f45be0b683e776fa4fc1386bec10871bb0342ac6cc'}
LAUNCHER={'path':str(HERE/'step4_launcher_c2v015_s1pair_cx3v001.py'),'sha256':'2e41da3746053f073d3c775de29c5c8df156deaa861e2b774ee88d7ab96808aa'}
LIB={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2/s1_path_lib_c2v002c.py','sha256':'99e2be175e546992c70984435bc480e1eddb90b052fda65ddcbfe8780bdbd27e'}
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
BLAS={k:'1' for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS')}
def modules():
 out=[]
 for p in (GUARD,LIB):
  raw=Path(p['path']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=p['sha256']:raise PermissionError('S1_PAIR_BOOTSTRAP_HASH_MISMATCH')
  m=types.ModuleType(Path(p['path']).stem);m.__file__=p['path'];exec(compile(raw,p['path'],'exec'),m.__dict__);out.append(m)
 return out

def run(plan_ref,admission_ref,registration_ref,v6_ref,launch_cfg_ref,*,mode='dry',confirm=None,record_path=None):
 G,L=modules()
 out={'schema':'UNT_S1_PAIR_PRELAUNCH_DECISION_CX3V001','module':{'path':str(Path(__file__).resolve()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'mode':mode,'plan':plan_ref,'admission':admission_ref,'registration':registration_ref,'v006':v6_ref,'launch_config':launch_cfg_ref,'decision':None,'checks':{},'production':'UNTESTED until root execution'}
 try:
  G.require(mode in ('dry','launch'),'MODE_REQUIRED')
  if mode=='launch':
   G.require(confirm==plan_ref.get('sha256'),'LAUNCH_CONFIRMATION_REQUIRED')
   G.require(isinstance(record_path,str) and bool(record_path),'PRELAUNCH_RECORD_REQUIRED')
   G.require(os.environ.get('UNT_STEP4_ADMISSION_PATH')==admission_ref.get('path') and os.environ.get('UNT_STEP4_ADMISSION_SHA256')==admission_ref.get('sha256'),'PUBLISHED_ADMISSION_ENV_MISMATCH')
  L.registration_in_force(registration_ref,v6_ref);out['checks']['registration']='PASS'
  lcfg=L.pinned_json(launch_cfg_ref,'LAUNCH_CONFIG')
  G.require(lcfg.get('schema')==L.SCHEMA_LAUNCH_CFG,'LAUNCH_CONFIG_SCHEMA')
  G.require(lcfg.get('campaign_state') in ('ACTIVE','INACTIVE'),'CAMPAIGN_STATE_REQUIRED')
  G.require(lcfg.get('step2_route_a_state')=='INACTIVE','STEP2_ROUTE_A_NOT_INACTIVE')
  plan,cfg=G.validate(plan_ref,LAUNCHER['path'],config_ref=admission_ref)
  G.require(plan.get('guard')==GUARD and plan.get('launcher')==LAUNCHER,'S1_PAIR_PACKET_PINS')
  G.require(cfg.get('s1_overlap',{}).get('replay_module')==LIB,'S1_PAIR_REPLAY_LIBRARY_REQUIRED')
  inactive=lcfg['campaign_state']=='INACTIVE'
  G.require(cfg.get('core_priority')==(G.CORE_PRIORITY_INACTIVE if inactive else G.CORE_PRIORITY_S1_OVERLAP),'S1_PAIR_CAMPAIGN_STATE_BINDING')
  fill=L.pinned_json(plan['s1']['fill_record'],'FILL_RECORD')
  G.require(fill.get('schema')==L.SCHEMA_FILL and fill.get('dry') is False,'S1_PAIR_WRITTEN_FILL_REQUIRED')
  replay,st=L.replay_specs(fill)
  for c in plan['calls']:
   case=c['case'];raw=G.verify(c['spec']);spec=G.decode(raw)
   G.require(c['driver']==L.const_pin('DRIVER') and c['tail_on'] is True,'S1_PAIR_R5_TAIL_ON')
   G.require(fill['cases'][case]['spec']==c['spec'] and replay[case]==raw,'S1_PAIR_FILLED_SPEC_REPLAY')
   G.require(spec['numerics']['composite_grid_spec']['breaks_inverse_kpc'][-1]==L.CASE_K[case] and L.canonical(spec['numerics']['composite_grid_spec'])==L.canonical(L.cb_numerics(st,L.CASE_CB[case])['composite_grid_spec']),'S1_PAIR_CASE_GRID')
  out['checks']['filled_specs_and_native_preflights']='PASS'
  if inactive:
   trees=L.campaign_route_a_trees(L._process_table(),None)
   G.require(not trees,'S1_CAMPAIGN_ROUTE_A_TREE_WHILE_ATTESTED_INACTIVE')
   out['checks']['inactive_process_table']='PASS'
  else:out['checks']['inactive_process_table']='NOT_APPLICABLE_ROOT_ACTIVE'
  argv=[PYTHON,'-I','-B',LAUNCHER['path'],plan_ref['path'],'--execute-root-only']
  out.update(decision='ADMITTED' if mode=='dry' else 'LAUNCHING',cases=list(G.S1_OVERLAP_CASES),launch_argv=argv,campaign_state=lcfg['campaign_state'])
  if record_path is not None:
   out['record']=L.write_exclusive(record_path,L.record_bytes(out))
  if mode=='launch':
   try:
    p=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,text=True,env={**os.environ,**BLAS})
    result={'returncode':p.returncode,'stdout':p.stdout[-8000:],'stderr':p.stderr[-8000:]}
    out['decision']='LAUNCHED' if p.returncode==0 else 'LAUNCHER_REFUSED'
   except Exception as e:result={'exception':type(e).__name__+': '+str(e)};out['decision']='SPAWN_FAILED'
   out['launcher_result']=result
   outcome={'schema':'UNT_S1_PAIR_LAUNCH_OUTCOME_CX3V001','module':out['module'],'record':out['record'],'plan':plan_ref,'decision':out['decision'],'launcher_result':result,'completion':'Launcher return is not scientific completion; root tracks both receipts.'}
   try:out['outcome_record']=L.write_exclusive(record_path+'.outcome.json',L.record_bytes(outcome))
   except Exception as e:out['outcome_record_error']=type(e).__name__+': '+str(e)
  return out
 except Exception as e:
  out['decision']='REFUSED';out['refusal']={'code':str(getattr(e,'code',None) or e),'type':type(e).__name__}
  if record_path is not None and 'record' not in out:
   try:out['record']=L.write_exclusive(record_path,L.record_bytes(out))
   except Exception as r:out['record_error']=type(r).__name__+': '+str(r)
  return out

def pin_arg(s):
 path,sep,h=s.rpartition('@')
 if not sep:raise argparse.ArgumentTypeError('absolute path@sha256 required')
 return {'path':path,'sha256':h}
def main():
 a=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
 for n in ('plan','registration','v6','launch-config'):a.add_argument('--'+n,required=True,type=pin_arg)
 a.add_argument('--record');a.add_argument('--launch',action='store_true');a.add_argument('--confirm')
 x=a.parse_args();p=os.environ.get('UNT_STEP4_ADMISSION_PATH','');h=os.environ.get('UNT_STEP4_ADMISSION_SHA256','')
 out=run(x.plan,{'path':p,'sha256':h},x.registration,x.v6,x.launch_config,mode='launch' if x.launch else 'dry',confirm=x.confirm,record_path=x.record)
 print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['decision'] in ('ADMITTED','LAUNCHED') else 3
if __name__=='__main__':raise SystemExit(main())
