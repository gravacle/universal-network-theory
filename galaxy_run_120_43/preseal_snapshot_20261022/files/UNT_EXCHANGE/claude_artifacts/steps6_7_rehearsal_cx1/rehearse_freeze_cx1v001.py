"""0603 synthetic-only two-pass rehearsal; no scientific solver or real target access."""
import os,sys,json,hashlib,types,time,datetime,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RUN=ROOT/('run_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
RUN.mkdir()
def load(p,name):
 m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(Path(p).read_bytes(),str(p),'exec'),m.__dict__);return m
R=load(ROOT.parent/'freeze_score_readiness_cx3/v003g/review_v003g_cx3v001.py','rehearsal_helpers')
R.RUN=RUN
R.ALLOWED.add(str(Path(__file__).resolve()))
sys.addaudithook(R.audit)
write=R.write_x;sha=R.sha_file;canon=R.canon
trace=[]
def mark(step,t,**kw):
 trace.append(dict(step=step,wall_seconds=time.monotonic()-t,**kw));print(step,kw,flush=True)
t=time.monotonic();F=R.load(R.V003E,'rehearsal_freeze');E=R.load(R.ENGINE,'rehearsal_engine');W=R.W;W.F=F
world=R.build_world(RUN)
for k,v in world.items():setattr(W,k,v)
R.QIDS=[x['query_id'] for x in W.slots['query_block']['rows']]
qm=RUN/'SYNTHETIC_QUERY_RADII.json';write(qm,{'rows':copy.deepcopy(W.slots['query_block']['rows'])});W.qm=str(qm)
mode=F.apply_coordinate_mode(coordinates=W.coords,coordinate_mode={'mode':'DDO154_DISTANCE_FIXED_AT_REGISTERED','free_coordinates':['a','b'],'fixed_engine_coordinates':{'D_ddo':R.DC}})
assert mode['ok'],mode
W.fs=F.make_freeze_coordinate_spec(coordinates=mode['coordinates']);assert W.fs['ok']
run=E.run_calibration_region(forward=R.forward_ddo,coordinates=W.fs['engine_coordinates'],observation_region_path=W.region,observation_region_sha256=sha(W.region),u_seed=None,budget=700,rel_step=.05,min_step=1e-4,max_halvings=3,null_tolerance=1e-6,repair_iterations=8,max_repair_step=.25,march_step=.05,bisection_steps=4,design_count=8,global_design_count=24,max_march_rounds=4,hull_growth_tol=.01,ddo154_distance={'name':'D_ddo','modulus_half_width_multiple':1.},rng_seed=7)
assert run['status']=='COMPLETE'
W.rec=E.write_calibration_record(run=run,record_path=str(RUN/'CALIBRATION_RECORD.json'),registry_path=str(RUN/'CALIBRATION_REGISTRY.jsonl'))
W.sel=F.select_representative_points(exploration=run,interior_count=5,spec=W.fs['spec']);assert W.sel['ok']
mark('synthetic_calibration_and_selection',t,members=len(W.sel['points']))
# Collect every selected theta and sensitivity plan for every possible reference.
# Thus no root roster or reference choice is needed before raw custody is complete.
t=time.monotonic();S=F._spec_from(W.fs['spec'],[]);thetas={}
for p in W.sel['points']:
 th=F._theta_ngc_from_engine(S,p['theta_natural']);thetas[canon(th)]=th
 for e in F._sensitivity_plan(S,dict(u=p['u'],theta_ngc=th),W.sel['admitted_region']['near_null_directions'],{'mode':'box_ends'}):thetas[canon(e['theta_ngc'])]=e['theta_ngc']
gate=R.gate_file('DELIBERATE_Q20',['SYNTHETIC_REHEARSAL_GATE'],[R.QIDS[19]])
W.root_gatepins=[gate]
pattern=lambda th:{0:('QUERY_INSIDE_INNERMOST_NODE',None),1:('QUERY_INSIDE_INNERMOST_NODE',None),19:('SYNTHETIC_REHEARSAL_GATE',gate)}
rawdir=RUN/'first_pass_raw';rawdir.mkdir();rawpins={};inventory=[]
for delta in (0.,6.5,-4.):
 fn=R.make_forward(pattern,delta)
 for i,(key,th) in enumerate(thetas.items()):
  p=rawdir/('RAW_%s_%03d.json'%(str(delta).replace('-','m'),i));write(p,fn(th));pin={'path':str(p),'sha256':sha(p)};rawpins[delta,key]=pin
  inventory.append(dict(alternative={0.:'BR_A_F10_PRIMARY',6.5:'ORIGINAL_K',-4.:'STAGE0_GRID_OUTER'}[delta],theta=th,raw=pin))
write(RUN/'FIRST_PASS_COMPLETE.json',dict(scope='SYNTHETIC_ONLY',targets_opened=False,root_rosters_registered=False,raw=inventory))
mark('step5_synthetic_raw_custody',t,raw_count=len(inventory))
t=time.monotonic();replay_count=[0]
def replay_factory(pattern,delta=0.,raw_dir=None,saved=None):
 def replay(theta):
  pin=rawpins[delta,canon(theta)];assert sha(pin['path'])==pin['sha256'];obj=json.loads(Path(pin['path']).read_bytes());replay_count[0]+=1
  if raw_dir is not None:
   p=raw_dir/('REPLAY_%03d.json'%len(saved));write(p,obj);saved.append(str(p))
  return obj
 return replay
R.make_forward=replay_factory
res=R.pipeline(F,'SECOND_PASS_FREEZE',pattern)
write(RUN/'FREEZE_CALL_RESULTS.json',{k:v for k,v in res.items() if k not in ('doc','folder')})
assert res.get('w',{}).get('ok'),res
assert res['vf']['ok'] and res['vr']['ok']
mark('step6_register_replay_freeze',t,replay_count=replay_count[0],manifest_sha256=res['logged']['manifest_file_sha256'])
t=time.monotonic();targets=R.make_targets(res['doc'],res['folder']);sc=R.score(F,res,targets);write(RUN/'LADDER_SYNTHETIC.json',sc);assert sc['ok'],sc
mark('step7_ladder_synthetic_targets',t)
write(RUN/'TRACE.json',dict(scope='SYNTHETIC_ONLY_NOT_SCIENCE',steps=trace,reads=sorted(R.READS),denied=R.DENIED,source_pins=[{'path':str(p),'sha256':sha(p)} for p in (Path(__file__),Path(R.__file__),R.V003E,R.ENGINE,R.SLOTS)],freeze=res['w'],root_pins=res['root_pins']))
print('RESULT_DIR',RUN,flush=True)
