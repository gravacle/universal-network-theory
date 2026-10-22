"""Inert whole-engine/actual-Probe replay; not production admission integration."""
import ast, hashlib, json, math, sys, tempfile, types
from pathlib import Path
B=Path(__file__).parent
A=B.parent
EP=A/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py'
PP=A/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py'
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
er=EP.read_bytes();pr=PP.read_bytes()
assert hashlib.sha256(er).hexdigest()=='6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3'
assert hashlib.sha256(pr).hexdigest()=='c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'
E=types.ModuleType('inert_engine');E.__file__=str(EP)
exec(compile(er,str(EP),'exec'),E.__dict__)
tree=ast.parse(pr)
names={'Probe','_ProbeStop','canonical','sha256_bytes','theta_key'}
nodes=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
g=dict(types=types,sys=sys,json=json,hashlib=hashlib,math=math,OrchestratorError=ValueError,
 SCHEMA_THETA_KEY='DDO154_CALIBRATION_THETA_KEY_C2V001',SINGLE_FAMILIES=('seed','repair'),PLACEHOLDER_REASON='ORCHESTRATOR_PROBE_PLACEHOLDER_NOT_AN_EVALUATION')
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(PP),'exec'),g)
root=Path(tempfile.mkdtemp(prefix='wholeengine_',dir=B/'inert_fixtures'))
def write(p,obj):
 with p.open('x') as f:json.dump(obj,f,sort_keys=True,allow_nan=False)
rows=[dict(id='INERT_%02d'%i,reference_radius_kpc=i+1,observed_speed_km_s=10.,quoted_random_sigma_km_s=1.,conditional_random_acceptance_low_km_s=8.,conditional_random_acceptance_high_km_s=12.) for i in range(12)]
obs=root/'INERT_OBSERVATIONS.json'
write(obs,dict(rows=rows,statistical_choice='SYNTHETIC FIXTURE ONLY',forward_coordinates={},distance_summary=dict(modulus_mag=25.,distance_central_Mpc=1.,reported68_low_Mpc=.9,reported68_high_Mpc=1.1,scope='INERT')))
def coord(name,lo,hi,value,role='free',scope='shared',transform='linear',units='fixture'):
 return dict(name=name,lower=lo,upper=hi,trial_value=value,role=role,scope=scope,transform=transform,units=units,sensitivity='NONE')
kw=dict(coordinates=[coord('x',-1,1,0),coord('D_ddo',.9,1.1,1,'fixed','DDO154','log','Mpc')],observation_region_path=str(obs),observation_region_sha256=pin(obs)['sha256'],u_seed=[.5],budget=80,rel_step=.05,min_step=1e-4,max_halvings=2,null_tolerance=1e-6,repair_iterations=3,max_repair_step=.25,march_step=.05,bisection_steps=2,design_count=3,global_design_count=3,max_march_rounds=1,hull_growth_tol=.01,ddo154_distance=dict(name='D_ddo',modulus_half_width_multiple=1),rng_seed=17)
ctx=types.SimpleNamespace(E=E,run_kwargs=lambda:kw,branch_bound=lambda fam:6 if fam[0]=='jacobian' else 80)
probe=g['Probe'](ctx)
class Cache:
 def __init__(self):self.data={}
 def forward(self,key):return self.data.get(key)
def answer(theta):return dict(valid=True,speeds_km_s={r['id']:10+3*theta['x'] for r in rows},reasons=[])
# Independent direct run collects an external result bank without admitting it to the probe cache.
bank={}
def direct(theta):
 a=answer(theta);bank[g['theta_key'](theta)]=a;return a
baseline=E.run_calibration_region(forward=direct,**kw)
assert baseline.get('ok'),baseline
bankpath=root/'INERT_EXTERNAL_BANK.json';write(bankpath,bank)
bank=json.loads(bankpath.read_bytes())
def replay(imported,label):
 cache=Cache();plans=[]
 for i in range(200):
  r=probe.run(cache,'plan')
  if r['complete']:
   check=probe.run(cache,'replay');assert check['complete'];return plans,check['run']
  assert r['misses'],r
  plan=r['misses'];plans.append(plan)
  # Durable fixture plan precedes all by-reference bank reads/admissions.
  pp=root/('%s_PLAN_%03d.json'%(label,i));write(pp,plan)
  assert json.loads(pp.read_bytes())==plan
  for m in plan:
   a=bank[m['key']] if imported else answer(m['theta'])
   cache.data[m['key']]=a
 raise AssertionError('replay did not terminate')
localplans,localrun=replay(False,'local')
importplans,importrun=replay(True,'import')
assert localplans==importplans
assert localrun==importrun==baseline
bulk=Cache();bulk.data=bank.copy();br=probe.run(bulk,'plan')
assert br['complete'] and not br['misses'] and localplans
report=dict(status='PASS',blocking_count=0,scope='Synthetic whole engine and actual Probe; fixture plan/cache only',tested=['Unmodified full engine direct versus local request replay versus lazy external-bank replay: exact full run equality','Actual Probe request lists equal across local/lazy replay','Preloaded-bank negative control eliminates natural requests'],waves=len(localplans),bank_entries=len(bank),engine_status=baseline.get('status'),untested=['Production WAVE_PLAN writer, executor, cache, custody, acceptance, wait and root authentication integration','Multiple dimensional/scenario coverage'],pins=[pin(EP),pin(PP),pin(Path(__file__)),pin(obs),pin(bankpath)])
write(root/'TEST_REPORT.json',report)
print(json.dumps(dict(report=str(root/'TEST_REPORT.json'),waves=len(localplans),status='PASS')))
