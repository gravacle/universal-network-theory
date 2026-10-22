"""Codex2 dispatch 0511 Lane B independent source/AST and JSON comparator audit.
No source module import, no subprocess, no scientific replay, no run directories.
Numerical tests deliberately remain unexecuted if the environment cannot honor nice 10.
All outputs use exclusive creation. stdlib only.
"""
import ast,copy,datetime,hashlib,json,os,re
from pathlib import Path
EX=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
BASE=EX/'tail_scheme_impl_c2'
OUT=EX/'review_v010r4_cx2'
READ={}; CHECKS=[]; FINDINGS=[]
def read(p):
 p=Path(p)
 s=str(p.resolve())
 if '/runs_ext/UVT_' in s or 'KMAX_A2F10_C5H_RUN_V001' in s or 'session' in s and '/.codex/' in s: raise RuntimeError('forbidden path')
 b=p.read_bytes();READ[str(p)]=hashlib.sha256(b).hexdigest();return b.decode()
def tree(p):return ast.parse(read(p),filename=str(p))
def check(name,ok,detail=None):
 CHECKS.append(dict(name=name,status='TESTED',passed=bool(ok),detail=detail))
def dump(x):return ast.dump(x,include_attributes=False)
def function(t,name):return next(n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
def constant(t,name):return ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id==name for k in n.targets)))
def extracted(t,names,env):
 ns=dict(env);z=ast.Module(body=[copy.deepcopy(n) for n in t.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[])
 exec(compile(ast.fix_missing_locations(z),'<source-extracted-json-functions>','exec'),ns);return ns
# Byte pins explicitly supplied by assignment.
pins={
BASE/'module/owned_uv_tail_lapse_v001.py':'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22',
BASE/'module/uv_tail_source_roster_c2v001.py':'4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2',
BASE/'module/posix_libm_bessel_jn_provider_c2v001.py':'d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171',
BASE/'nodes_v001/lib/owned_uv_tail_nodes_v001.py':'c8a04fb55f6c388c7cc5b735cb0e19222836c49acfce46d846198951593be551',
BASE/'driver_r4/galaxy_m0_forward_c2v010.py':'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'}
for p,want in pins.items():read(p);check('input_pin:'+p.name,READ[str(p)]==want)
# RO1 actual source predicate: compile only the guard expression, not a module or solve.
expected=('NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH','DEGENERATE_RADIAL_EULER: zero exact denominator; no unique speed','NON_TIMELIKE_COLUMN')
class SubValueError(ValueError):pass
ro1_summary=[]
for stem in ['ddo_composite_stable_cached_binding_v002','ngc_composite_full_coupled_binding_v002']:
 p=EX/'ro1_readout_c2'/(stem+'_uvtail_ro1_c2v002.py');t=tree(p)
 msgs=constant(t,'RO1_MESSAGES');check(stem+':message_set_exact',msgs==expected)
 fun=function(t,'evaluate')
 catches=[n for n in ast.walk(fun) if isinstance(n,ast.ExceptHandler) and isinstance(n.type,ast.Name) and n.type.id=='ValueError']
 catch=next(n for n in catches if any(isinstance(x,ast.If) and 'RO1_MESSAGES' in ast.unparse(x.test) for x in n.body))
 guard=next(x for x in catch.body if isinstance(x,ast.If) and 'RO1_MESSAGES' in ast.unparse(x.test))
 expr=compile(ast.Expression(copy.deepcopy(guard.test)),str(p),'eval')
 errors=[ValueError(m) for m in expected]+[ValueError('DEGENERATE_RADIAL_EULER'),ValueError(expected[0]+' '),ValueError(expected[0].lower()),SubValueError(expected[0]),RuntimeError(expected[0]),ValueError(expected[0],'x'),TypeError(expected[0]),ValueError('other')]
 states=[None,{}, {'converged_finite_fixed_point':False},{'converged_finite_fixed_point':1},{'converged_finite_fixed_point':True}]
 passed=0
 for e in errors:
  for s in states:
   caught=not eval(expr,{'type':type,'ValueError':ValueError,'str':str,'isinstance':isinstance,'dict':dict,'RO1_MESSAGES':msgs},{'exc':e,'solved':s})
   wanted=type(e) is ValueError and str(e) in expected and type(s) is dict and s.get('converged_finite_fixed_point') is True
   assert caught==wanted;passed+=1
 check(stem+':predicate_adversaries',True,{'cases':passed,'guard':ast.unparse(guard.test)})
 solve=function(fun,'solve')
 assign=next(n for n in solve.body if isinstance(n,ast.Assign) and any(isinstance(q,ast.Subscript) and ast.unparse(q)=="ro1['solved']" for q in n.targets))
 call_assign=next(n for n in solve.body if isinstance(n,ast.Assign) and any(isinstance(q,ast.Name) and q.id=='answer' for q in n.targets))
 check(stem+':solved_set_after_return',assign.lineno>call_assign.end_lineno,{'solve_call_line':call_assign.lineno,'set_solved_line':assign.lineno,'guard_line':guard.lineno})
 ro1_summary.append({'file':str(p),'cases':passed})
# AST tail-OFF specialization for serial solver: remove only uv_tail=None branch work and added kw-only parameter.
class Off(ast.NodeTransformer):
 def visit_FunctionDef(self,n):
  n=self.generic_visit(n)
  if n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant) and isinstance(n.body[0].value.value,str):n.body=n.body[1:]
  if any(a.arg=='uv_tail' for a in n.args.kwonlyargs):
   idx=next(i for i,a in enumerate(n.args.kwonlyargs) if a.arg=='uv_tail');n.args.kwonlyargs.pop(idx);n.args.kw_defaults.pop(idx)
  return n
 def visit_If(self,n):
  if ast.unparse(n.test)=='uv_tail is not None':return [self.visit(x) for x in n.orelse]
  return self.generic_visit(n)
parent=EX/'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py'
child=BASE/'route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py'
a,b=tree(parent),tree(child)
for name in [n.name for n in a.body if isinstance(n,ast.FunctionDef)]:
 x=Off().visit(copy.deepcopy(function(a,name)));y=Off().visit(copy.deepcopy(function(b,name)))
 check('serial_solver_off_ast:'+name,dump(x)==dump(y))
# B0 map adversaries execute extracted JSON/string functions only (no source import or subprocess).
b0p=BASE/'driver_r4/gates/b0_plan_identity_c2v002.py';t=tree(b0p)
neutral=constant(t,'RO1_NON_ARMED')
prep=(EX/'kmax_prereg_v005_c2/extension_c5c6/prep_successor/ddo_actual_initial_source_preparation_v009.py','b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc')
ns=extracted(t,{'ext_feature_map','driver_needle_map','ro1_key_map','compare','apply','sha_b'},dict(json=json,re=re,hashlib=hashlib,RO1_NON_ARMED=neutral,PREP_V009=prep))
canon=lambda x:(json.dumps(x,indent=1,allow_nan=False)+'\n').encode()
for label,change in [('armed',{'armed':True}),('fired',{'fired':True}),('events',{'events':[{'refusal':expected[0]}]}),('wrong_rule',{'rule':'RO2'})]:
 r=dict(neutral,**change);mapped,n=ns['ro1_key_map'](canon({'classification':'CONVERGED','ro1':r,'scientific_value':42}))
 check('B0_preserves_changed_RO1:'+label,json.loads(mapped).get('ro1')==r and n==0)
r,n=ns['ro1_key_map'](canon({'classification':'CONVERGED','ro1':neutral,'scientific_value':42}))
check('B0_removes_exact_neutral_RO1_only',json.loads(r)=={'classification':'CONVERGED','scientific_value':42} and n==1)
for pin in ['wrong-pin',prep[1]]:
 raw={'static_pins':{str(prep[0]):pin,'other':'retain'},'scientific_value':42}
 z,applied=ns['ext_feature_map'](canon(raw));z=json.loads(z)
 check('B0_prep_map:'+pin[:9],z['scientific_value']==42 and z['static_pins']['other']=='retain' and ((str(prep[0]) not in z['static_pins'])==(pin==prep[1])))
# In-memory file stores: both missing directories, and changed scientific payload.
ns['files']=lambda _:{}
empty=ns['compare'](Path('/not-read/parent'),Path('/not-read/new'),[],None)
check('B0_empty_outputs_false_positive_reproduced',empty['identical'] and empty['files_parent']==0 and empty['files_v010']==0,empty)
FINDINGS.append(dict(id='B0-EMPTY',severity='SHOULD_FIX',status='TESTED',claim='B0 compare returns identical for zero files on both sides. main admits equal nonzero exits and equal terminal error, so positive specs can pass after identical pre-report failures.',reproducer='Extracted compare() in-memory empty files(); no driver ran.'))
store={'parent':{'DRYRUN_REPORT.json':canon({'scientific_value':42})},'new':{'DRYRUN_REPORT.json':canon({'scientific_value':43})}}
ns['files']=lambda p:copy.deepcopy(store[str(p)])
res=ns['compare']('parent','new',[],None)
check('B0_scientific_scalar_change_rejected',not res['identical'],res['differ'])
# Source-level geometry/sign invariants; no floating point or scientific evaluations.
lt=tree(BASE/'module/owned_uv_tail_lapse_v001.py');nt=tree(BASE/'nodes_v001/lib/owned_uv_tail_nodes_v001.py')
check('tail_c0_is_outer_minus_kept',ast.unparse(function(lt,'_c0_D').body[-1])=='return cO - cC')
grid=ast.unparse(function(lt,'_grid'))
check('tail_corner_subtracts_kept_adds_outer',"sign=-1" in grid and "sign=+1" in grid)
ctx=ast.unparse(function(nt,'ext_context'))
check('nodes_rejects_straddling_panels',"an ext panel straddles the kept edge" in ctx)
check('nodes_checks_inner_nodes_weights_exact',"np.array_equal(ax_e[inner], ax_k)" in ctx and "np.array_equal(w_e[inner], w_k)" in ctx)
check('nodes_mask_is_tensor_complement',"mask3 = ~(inner[:, None, None] & inner[None, :, None] & inner[None, None, :])" in ctx)
amp=ast.unparse(function(nt,'amplitudes'))
check('nodes_symbol_positive_inverse_4gamma_k2','return lambda_scale * dk / (2 * math.pi) ** 3 * S / (4.0 * gamma_eff * k2)' in amp)
build=ast.unparse(function(lt,'build'))
check('continuum_symbol_positive_inverse_4gamma','pref = config[\'lambda_scale\'] / (4.0 * gamma_eff * (2.0 * math.pi) ** 3)' in build)
rs=tree(BASE/'module/uv_tail_source_roster_c2v001.py')
ring=ast.unparse(function(rs,'ring_transform'))
check('roster_ring_J_negative_mc2','-c_m_s * c_m_s * np.einsum' in ring)
# Record each direct source's lapse call sites. Does not walk outputs or imported source trees.
coverage=[]
paths=list((BASE/'route_a').glob('*.py'))+list((BASE/'route_b/stages').glob('*.py'))+list((BASE/'driver_r4/route_b').glob('*.py'))+[BASE/'route_b/uvt_route_b_binding_c2v001.py']
for p in sorted(paths):
 tx=read(p);ts=ast.parse(tx)
 sites=[]
 for n in ast.walk(ts):
  if isinstance(n,ast.Call):
   f=ast.unparse(n.func)
   if any(k in f for k in ['lapse','boundary','uvt.jets','line_jets','offset_fields','bind_offset','begin_iteration','complete_iteration','TailBoundary']):sites.append({'line':n.lineno,'call':f})
 coverage.append({'path':str(p),'sites':sorted(sites,key=lambda x:x['line'])})
# Pin all the direct files inspected manually, without trusting existing hash manifests.
manual=[BASE/'driver_r4/BUILD_DRIVER_C2V010_R4.json',BASE/'driver_r4/DIFF_V009EXT_R4.diff',BASE/'driver_r4/tests/test_v010_r4_c2v001.py',EX/'ro1_readout_c2/RO1_IMPL_V002.md',BASE/'route_a/diffs/facade_uvtail_c2v001_vs_2caca496.diff',BASE/'route_a/diffs/solver_uvtail_c2v001_vs_44d9c23c.diff',BASE/'route_a/diffs/solver_parallel_uvtail_c2v001_vs_aed4dd59.diff',BASE/'route_b/diffs/DIFF_ddo_saved_root_body_array_root_v002_gal_c2v005_TO_UVT_C2V001.diff',BASE/'route_b/diffs/DIFF_ddo_body_source_offset_root_v003_gal_c2v005_TO_UVT_C2V001.diff']
for p in manual:read(p)
record={'schema':'CODEX2_0511_LANE_B_SOURCE_AUDIT_V001','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'execution':{'scientific_launches':0,'source_modules_imported':0,'subprocesses':0,'numpy_imported':False,'nice_requested':10,'effective_nice':os.getpriority(os.PRIO_PROCESS,0),'numerical_replays':'UNTESTED: nice 10 refused by sandbox'},'checks':CHECKS,'findings':FINDINGS,'coverage':coverage,'input_sha256':READ}
with (OUT/'EVIDENCE_V001.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'checks':len(CHECKS),'passed':sum(x['passed'] for x in CHECKS),'failed':[x['name'] for x in CHECKS if not x['passed']],'files_hashed':len(READ),'effective_nice':record['execution']['effective_nice'],'findings':FINDINGS},indent=2))
