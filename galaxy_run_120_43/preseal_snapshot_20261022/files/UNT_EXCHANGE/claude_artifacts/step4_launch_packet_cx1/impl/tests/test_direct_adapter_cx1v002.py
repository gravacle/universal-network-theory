"""Actual C4 structural compatibility and real r5 normalization; no science runs."""
import ast,copy,importlib.util,json,os,re,types
from pathlib import Path
I=Path(__file__).resolve().parent.parent;OUT=I/'tests/DIRECT_V002';OUT.mkdir()
def module(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
G=module(I/'step4_guard_cx1v005.py','gd');A=module(I/'step4_direct_preflight_cx1v001.py','ad')
ART=I.parents[1];ORCH=ART/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py'
checks=[]
def check(name,fn,expected=None):
 try:v=fn();ok=expected is None and v is not False;detail=repr(v)[:130]
 except Exception as e:ok=expected is not None and expected in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
def put(name,obj):
 p=OUT/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True,allow_nan=False)
 return G.pin(p)
# Actual 29 tail-on and four tail-off C4 source specs; hashes verified before reads.
for batch in ('HEADLINE','DIII','SENS_LO','SENS_HI'):
 p=I.parent/'templates_v001'/f'{batch}_PLAN_TEMPLATE_CX1V001.json'
 for c in G.decode(p.read_bytes())['calls']:
  check('C4_structural_'+batch+'_'+c['case'],lambda c=c:G.spec_structure(c,G.doc(c['spec'])))
# Execute unmodified pure native O.Context.prelaunch_check and its three helper
# functions extracted by AST; do not execute campaign Context initialization.
tree=ast.parse(ORCH.read_bytes());chosen=[]
for n in tree.body:
 if isinstance(n,ast.FunctionDef) and n.name in ('diff_paths','lint_override_keys','relative_paths'):chosen.append(n)
 if isinstance(n,ast.ClassDef) and n.name=='Context':pre=next(x for x in n.body if isinstance(x,ast.FunctionDef) and x.name=='prelaunch_check')
chosen.append(pre)
env={'copy':copy,'os':os,'canonical':G.canonical,'OVERRIDE_KEY_RE':re.compile(r'0|[1-9][0-9]*'),'OrchestratorError':G.Refusal,'DECLARED_CHANGED_PATHS':('label','physical.common_scale_s','physical.gamma','physical.ell_F_m','physical.distance_Mpc','numerics.uv_tail.eps_certificate','numerics.uv_tail.lo_certificate')}
exec(compile(ast.Module(body=chosen,type_ignores=[]),str(ORCH),'exec'),env)
class Parent:
 def __init__(self,*a):raise AssertionError('CAMPAIGN_CONSTRUCTOR_MUST_NOT_RUN')
 prelaunch_check=env['prelaunch_check']
class Native(Parent):
 pass
O=types.SimpleNamespace(SCHEMA_CONFIG='DDO154_CALIBRATION_ORCHESTRATOR_CONFIG_C2V005',CONFIG_KEYS={'schema','synthetic_test','driver','coordinate_spec','numerics','anchor','work_dir_volume'},SCHEMA_SPEC='DDO154_CALIBRATION_COORDINATE_SPEC_C2V001',SPEC_MAPPING_ID='C2V001_PHYS4_GAMMA_EQ_GE_TIMES_EREF',**{k:env[k] for k in ('diff_paths','lint_override_keys','relative_paths')})
anchor_calls=[]
def registered(a):anchor_calls.append(a);G.require(a=={'synthetic_anchor_registration':True},'ANCHOR_STUB_REFUSED')
C=types.SimpleNamespace(O=O,M=types.SimpleNamespace(registered_anchor=registered),Context=Native,validate_block=lambda n:G.require(n.get('uv_tail',{}).get('enabled') is True,'BLOCK_REQUIRED'))
template=G.pin(ART/'step4_launch_readiness_c4/dryplans/post_adoption_probe_v001/specs_PROVISIONAL/TAIL_REANCHOR.PROVISIONAL.json')
coord=put('coordinate.json',{'schema':O.SCHEMA_SPEC,'call_spec_mapping':{'mapping_id':O.SPEC_MAPPING_ID,'template':template},'ddo154_forward_constants':{'inclination_deg':{'value':66.0}}})
driver=G.pin(ART/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py')
spec=G.doc(template)
config={'schema':O.SCHEMA_CONFIG,'synthetic_test':False,'driver':driver,'coordinate_spec':coord,'numerics':{'block':spec['numerics']},'anchor':{'synthetic_anchor_registration':True},'work_dir_volume':'/Volumes/External1'}
libs=[ART/'tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',ART/'tail_scheme_impl_c2/module/uv_tail_source_roster_c2v001.py',ART/'tail_scheme_impl_c2/module/posix_libm_bessel_jn_provider_c2v001.py']
cfg={'sources':{driver['path']:driver['sha256'],**{G.pin(p)['path']:G.pin(p)['sha256'] for p in libs}}}
with G.fence(cfg['sources']):ctx=A.build(C,config,guard=G.globals_api(),admission=cfg)
check('direct_context_has_exact_four_attrs',lambda:set(ctx.__dict__)=={'cfg','numerics','D','norm_base'})
check('campaign_constructor_not_called',lambda:isinstance(ctx,Native) and len(anchor_calls)==1)
check('native_prelaunch_method_inherited_unchanged',lambda:ctx.prelaunch_check.__func__ is env['prelaunch_check'])
with G.fence(cfg['sources']):check('real_r5_normalization_native_prelaunch',lambda:ctx.prelaunch_check(copy.deepcopy(spec))==ctx.norm_base)
bad=copy.deepcopy(spec);bad['physical']['inclination_deg']=65.0
with G.fence(cfg['sources']):check('real_r5_bad_inclination_refused',lambda:ctx.prelaunch_check(bad),'DRIVER_REFUSES_SPEC')
bad=copy.deepcopy(spec);bad['coefficients']['path']='relative.npz'
with G.fence(cfg['sources']):check('native_A7_relative_path_refused',lambda:ctx.prelaunch_check(bad),'A7_GUARD')
bad=copy.deepcopy(spec);bad['reference_compare']=not bool(spec.get('reference_compare'))
with G.fence(cfg['sources']):check('native_undeclared_normalized_delta_refused',lambda:ctx.prelaunch_check(bad),'normalized spec differs')
for name,field,value,reason in [('synthetic_context','synthetic_test',True,'DIRECT_C1_NON_SYNTHETIC_REQUIRED'),('wrong_driver','driver',{'path':driver['path'],'sha256':'0'*64},'DIRECT_C1_R5_REQUIRED'),('missing_anchor','anchor',{},'ANCHOR_STUB_REFUSED')]:
 c=copy.deepcopy(config);c[field]=value
 with G.fence(cfg['sources']):check(name,lambda c=c:A.build(C,c,guard=G.globals_api(),admission=cfg),reason)
result={'label':'TESTED actual33Claude4 structural specimens and native parent prelaunch plus realr5normalizer; anchor registration stubbed; full certificate/adoption production preflight UNTESTED','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'scientific_processes_created':0,'sources':[G.pin(x) for x in (I/'step4_guard_cx1v005.py',I/'step4_direct_preflight_cx1v001.py',ORCH,Path(__file__))]}
with (OUT/'RESULTS.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x for x in checks if not x['passed']]}))
raise SystemExit(0 if result['passed']==result['total'] else 1)
