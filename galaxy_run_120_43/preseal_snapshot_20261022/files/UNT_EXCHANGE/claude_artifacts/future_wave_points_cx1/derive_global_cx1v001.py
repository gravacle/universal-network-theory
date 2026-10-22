from pathlib import Path
import types, json, hashlib, copy, sys
import numpy as np
A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'); W=Path('/private/tmp/cx1_0815_global001');W.mkdir()
pins=[]
def read(p):
 p=Path(p);raw=p.read_bytes();pins.append({'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()});return raw
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(read(p),str(p),'exec'),m.__dict__);return m
E=module(A/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py','dry_engine')
M=module(A/'calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py','dry_core')
O=M.O
coords=json.loads(read(A/'calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json'))
cfg=json.loads(read(A/'sched_s45_c2/v004a/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004A.json'))
cs=O.Context._apply_coordinate_mode(coords['engine_coordinates'],{'mode':O.MODE_D_FIXED,'fixed_engine_coordinates':{'distance_Mpc':4.04}})
es=E.make_coordinate_spec(coordinates=cs);assert es['ok']
seedpath=A/'step4_launch_readiness_c4/dryplans/specs_v001/specs/CAMPAIGN_W1_SEED.json'
base=json.loads(read(seedpath));base['numerics']=copy.deepcopy(cfg['numerics']['block'])
ctx=types.SimpleNamespace(E=E,es=es,base=base,base_sha256=O.sha256_bytes(O.canonical(base)),inclination_deg=66.0,cfg={'tail_readiness':{'certificate_registry':None}})
u=O.Context._engine_trial_u(ctx);mapper=M.Mapper(ctx)
seed=mapper.build(E.to_natural(spec=es,u=u)['theta_natural'])
assert seed['certificate_point_key']=='6944e210d071c17b502fd5188ea8967503dbf9bb1d5530b67d0b151da02b13cd',seed['certificate_point_key']
# Only the branch enumerator and actual coordinate conversion run. Evaluation
# validation/response use inert stubs; no observation file or forward is read.
E._common_eval_checks=lambda *a:([],{'n':3,'varying':es['varying_names']})
E._speeds_vector=lambda e,ids:np.array([e['synthetic_value']])
allpoints={};scenarios=[]
for depth in range(3):
 for failing in ['plus','minus']:
  captured=[]
  def evaluate(**kw):
   uu=kw['u'];theta=E.to_natural(spec=es,u=uu)['theta_natural'];built=mapper.build(theta)
   purpose=kw['purpose'];delta=np.array(uu)-np.array(u);j=int(np.argmax(np.abs(delta)));step=float(delta[j]);valid=purpose=='seed' or (abs(step)<0.05*0.5**depth*1.01 and not (depth>0 and abs(step)>0.05*0.5**depth*1.01))
   # Fail earlier levels on selected side only; reach exact later branch.
   if purpose!='seed':valid=not (abs(step)>0.05*0.5**depth*1.01 and ((step>0)==(failing=='plus')))
   rec={'index':len(kw['log']),'valid':valid,'admitted':True,'reasons':[],'exception':None,'synthetic_value':1.0+sum(uu)}
   kw['counter']['used']+=1;kw['log'].append(rec)
   if purpose!='seed':
    row={'theta':theta,'call_key':built['key'],'key':built['certificate_point_key'],'u':list(uu),'axis':j,'signed_step':step,'spec':built['spec'],'raw':built['raw'].decode(),'pending_spec_sha256':built['sha256']}
    allpoints[built['key']]=row;captured.append(built['key'])
   return rec
  E._evaluate_point=evaluate
  p=coords['engine_parameters'];result=E.finite_difference_jacobian(forward=lambda _:None,spec=es,region={'row_ids':['inert']},u0=u,rel_step=p['rel_step'],min_step=p['min_step'],max_halvings=p['max_halvings'],budget=120,log=[])
  scenarios.append({'depth':depth,'failed_side':failing,'status':result['status'],'requested':captured})
assert len(allpoints)==18,len(allpoints)
# Execute the original nested global_design body with inert custody/evaluation.
import ast
tree=ast.parse(Path(E.__file__).read_text())
node=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='global_design')
global_points=[]
def evaluate_global(uu,purpose):
 theta=E.to_natural(spec=es,u=uu)['theta_natural'];built=mapper.build(theta)
 global_points.append({'theta':theta,'call_key':built['key'],'key':built['certificate_point_key'],'u':list(uu),'spec':built['spec'],'raw':built['raw'].decode(),'pending_spec_sha256':built['sha256']})
 return {'admitted':False}
genv=dict(E.__dict__,n=3,rng_seed=coords['engine_parameters']['rng_seed'],global_design_count=coords['engine_parameters']['global_design_count'],out={'global_design':{'skipped_duplicate':0,'evaluated':0,'n_admitted':0}},already_evaluated=lambda _:False,need_budget=lambda:None,evaluate=evaluate_global)
exec(compile(ast.Module(body=[node],type_ignores=[]),E.__file__,'exec'),genv)
genv['global_design'](True)
output={'scope':'Original global_design AST with no duplicates/budget exhaustion and inert responses; fixed conditional candidate pool','points':global_points,'sources':pins}
with (W/'DERIVATION_GLOBAL.json').open('x') as f:json.dump(output,f,indent=2)
print('Global design conditional pool:',len(global_points))
