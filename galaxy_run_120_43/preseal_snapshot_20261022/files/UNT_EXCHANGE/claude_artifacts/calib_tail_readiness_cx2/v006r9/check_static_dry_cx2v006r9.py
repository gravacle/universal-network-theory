"""0557 final candidate: normalization, closed gates and one zero-stage dry plan."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import contextlib,copy,hashlib,importlib.util,io,itertools,json,platform,resource,sys
from pathlib import Path
R=Path(__file__).resolve().parent;H=R.parent
platform.platform=lambda *a,**kw:'CX2 no subprocess '+repr(os.uname())
platform._Processor.get=staticmethod(lambda:os.uname().machine)
def guard(event,args):
 if event in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','socket.connect'):raise RuntimeError('NO_LAUNCH_OR_NETWORK '+event)
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.path.realpath(os.fsdecode(args[0]))
  if 'KMAX_A2F10_C5H_RUN_V001' in p or '/runs_ext/UVT_' in p or '/.codex/' in p:raise RuntimeError('FORBIDDEN_PATH '+p)
  if 'NGC3198' in p and any(t in p.lower() for t in ('target','observed','rotmod')):raise RuntimeError('FORBIDDEN_TARGET '+p)
sys.addaudithook(guard)
def pin(p):p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def jx(p,d):
 with p.open('x') as f:json.dump(d,f,sort_keys=True,indent=1,allow_nan=False);f.write('\n')
 return pin(p)
wp=R/'calibration_orchestrator_cx2v006r9.py';raw=wp.read_bytes()
spec=importlib.util.spec_from_file_location('_cx2r9_final_static',wp);M=importlib.util.module_from_spec(spec);sys.modules[spec.name]=M;exec(compile(raw,str(wp),'exec'),M.__dict__)
cfgpath=R/'RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json';cfg=json.loads(cfgpath.read_bytes());local=copy.deepcopy(cfg)
local['work_dir']=str(R/'UNCREATED_STATIC_CONTEXT');local['work_dir_volume']=None;local['work_dir_identity']={'resolved':local['work_dir'],'volume':None,'volume_uuid':None,'symlinks':[]}
ctx=M.Context(local);checks=[]
def ck(n,v):checks.append({'name':n,'status':'TESTED','pass':bool(v)})
ck('all scientific gates closed',not ctx.gates_ok())
ck('headline capability normalization',ctx.gates['driver_capability']['layer1_normalize_ok'])
ck('registered config anchor equals immutable template',M.M.registered_anchor(cfg['anchor'])['physical']==cfg['anchor']['physical'])
ck('actual reanchor remains pending',cfg['anchor']['result'] is None and cfg['anchor']['receipt'] is None and cfg['anchor']['use'] is False)
ck('review registration empty',not M.S.REGISTERED_DISTINCT_REVIEW_SHA256)
ck('A68 comparator disabled',M.S.COMPARATOR_A68_REVIEWED is False)
ck('fresh gates remain closed',not ctx.fresh_gates()['deciding_test']['ok'])
coords=json.loads((H/'DDO154_COORDINATES_CX2V006.json').read_bytes());by={c['name']:c for c in coords['engine_coordinates']};template=json.loads(Path(coords['call_spec_mapping']['template']['path']).read_bytes());plans=[]
for bits in itertools.product((0,1),repeat=3):
 th={n:by[n]['upper' if b else 'lower'] for n,b in zip(('common_scale_s','gamma_over_Eref','ell_F_m'),bits)}
 for mode,d in [('HEADLINE',4.04),('LOW',by['distance_Mpc']['lower']),('HIGH',by['distance_Mpc']['upper'])]:
  s=copy.deepcopy(template);s['numerics']=copy.deepcopy(cfg['numerics']['block']);s['physical'].update(common_scale_s=th['common_scale_s'],gamma=th['gamma_over_Eref']*by['Eref_base_J']['trial_value'],ell_F_m=th['ell_F_m'],distance_Mpc=d)
  plans.append(('CORNER_'+''.join(map(str,bits))+'_'+mode,s))
for edge in ('lower','upper'):
 s=copy.deepcopy(template);s['numerics']=copy.deepcopy(cfg['numerics']['block']);s['physical']['distance_Mpc']=by['distance_Mpc'][edge];plans.append(('DISTANCE_'+edge,s))
for row in json.loads((H/'WAVE_FIXTURE_V001.json').read_bytes())['rows']:
 if row['K_big']!=128:continue
 for wave in row['waves']:
  for i,c in enumerate(wave['calls']):
   s=copy.deepcopy(template);s['numerics']=copy.deepcopy(cfg['numerics']['block']);s['physical']=copy.deepcopy(c['physical']);plans.append((wave['name']+'_'+str(i),s))
for name,s in plans:
 n=ctx.D.normalize_spec(copy.deepcopy(s));g=ctx.sensitivity_gate(s)
 ck('normalize physical '+name,n['physical']==s['physical'])
 ck('full A32 hull '+name,all(v==M.HULL for v in n['numerics']['brackets']['rule']['fs_absolute_overrides'].values()))
 ck('exact distance gate '+name,g['ok']==(s['physical']['distance_Mpc']==4.04))
 if s['physical']['distance_Mpc']!=4.04:
  try:ctx.prelaunch_check(s);ok=False
  except M.Error as e:ok='SENSITIVITY_DECIDING_III_REQUIRED' in str(e)
  ck('prelaunch refuses sensitivity '+name,ok)
out=R/'static_dry_v001';out.mkdir();s=copy.deepcopy(template);s['physical']=copy.deepcopy(cfg['anchor']['physical']);s['numerics']=copy.deepcopy(cfg['numerics']['block']);s['label']='0557 final r9 registered anchor static/dry only'
p=jx(out/'ANCHOR_SPEC.json',s)
with contextlib.redirect_stdout(io.StringIO()):ret=ctx.D.cmd_dry_run(p['path'],str(out/'ANCHOR_DRY'))
rp=out/'ANCHOR_DRY/DRYRUN_REPORT.json';d=json.loads(rp.read_bytes());su=d['summary'];bad=[x for x in su['refusals_beyond_pending_inputs'] if not x.startswith('PENDING_UV_TAIL_CERTIFICATE:')]
ck('actual dry plan zero stages',ret==0 and d['executed_stages']==0 and not su['pin_problems'] and not su['binding_blockers'] and not su['unexplained_refusals'] and not bad)
result={'schema':'DDO154_FINAL_R9_STATIC_DRY_CX2V001','status':'TESTED','launches_performed':0,'passed':sum(c['pass'] for c in checks),'total':len(checks),'normalizations':len(plans),'actual_dry_plans':1,'executed_stages':d['executed_stages'],'checks':checks,'candidate':pin(wp),'core':pin(M.M.__file__),'sensitivity_policy':pin(M.S.__file__),'config':pin(cfgpath),'source':pin(__file__),'dry_spec':p,'dry_report':pin(rp),'max_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'limits':['No solver or scientific certificate execution.','Synthetic contexts use local workdir identity; real config unchanged.','All scientific gates remain closed; A68 successor and actual anchor evidence pending.']}
jx(R/'STATIC_DRY_RESULTS_CX2V006R9.json',result);print(json.dumps({k:result[k] for k in ('passed','total','normalizations','actual_dry_plans','executed_stages','max_rss_bytes_macos')}))
