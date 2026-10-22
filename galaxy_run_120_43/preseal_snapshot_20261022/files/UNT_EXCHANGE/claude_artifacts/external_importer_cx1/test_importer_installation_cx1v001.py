"""SYNTHETIC empty-seal chain installation; no context gates or campaign run.
Copies unchanged placeholder source bytes into a new inert tree. The two-line
synthetic entry fixture binds that tree; it is not a republished campaign entry.
"""
import ast,copy,hashlib,json,os,sys,tempfile,types
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from importer_installation_cx1v002 import install
root=Path(__file__).parent;art=root.parent
case=Path(tempfile.mkdtemp(prefix='installed_chain_',dir=root/'inert_fixtures'))
def fence(event,args):
 if event in ('os.remove','os.unlink','os.rename','os.rmdir','shutil.rmtree','subprocess.Popen','os.system','socket.connect'):raise PermissionError('INERT_NO_LAUNCH_OR_MUTATION')
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0]));parts=[x.lower() for x in p.parts]
  if any(x in ('runs','runs_ext','unt_internal_runs','unt_step4_runs') or 'ngc3198' in x or x.startswith('uvt_') for x in parts):raise PermissionError('FORBIDDEN_READ')
  mode=args[1];flags=args[2]
  writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT))
  if writing and (not p.is_relative_to(case) or not flags&os.O_EXCL):raise PermissionError('NONEXCLUSIVE_OR_OUTSIDE')
sys.addaudithook(fence)
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def put(p,obj):
 with p.open('x') as f:json.dump(obj,f,sort_keys=True);f.write('\n')
 return pin(p)
def write(p,data):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(data)
 return pin(p)
placeholder=art/'eps_rule_successor_cx2/integration/campaign/placeholder_chain_a296_cx2v001/v006r12_c4'
base=case/'SYNTHETIC_EMPTY_SEAL_CHAIN'
for name in ['adoption_policy_cx2v006r12_c4.py','calibration_core_cx2v006r12_c4.py','calibration_orchestrator_cx2v006r12_c4_q5b1.py']:
 write(base/'v006r12_c4'/name,(placeholder/name).read_bytes())
sens=art/'calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py'
assert pin(sens)['sha256']=='8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f'
write(base/'v006r8'/sens.name,sens.read_bytes())
wp=pin(base/'v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py')
ep=write(case/'SYNTHETIC_ENTRY_BINDING.py',('from pathlib import Path\nWRAPPER = Path('+repr(wp['path'])+')\nWRAPPER_SHA = '+repr(wp['sha256'])+'\n').encode())
before=dict(sys.modules)
W=types.ModuleType('_synthetic_published_wrapper');W.__file__=wp['path'];sys.modules[W.__name__]=W
exec(compile(Path(wp['path']).read_bytes(),wp['path'],'exec'),W.__dict__)
modules=[v for k,v in sys.modules.items() if k not in before and isinstance(v,types.ModuleType) and str(getattr(v,'__file__','')).startswith(str(art))]
O=W.O;native_context_init=W.Context.__init__;native_run=W.Orchestrator.run;native_put=W.Cache.put
rb=json.loads((root/'inert_fixtures/observation_entry_zn2194gv/inert_root_binding.json').read_bytes())
rb['schema']='CX1_IMPORTER_ROOT_BINDING_V002';rb['direct_plan']=put(case/'SYNTHETIC_DIRECT_PLAN.json',{'synthetic':True})
rbpin=put(case/'SYNTHETIC_ROOT_BINDING.json',rb)
dep=json.loads((root/'inert_fixtures/accept_loader_az7jd41r/SYNTHETIC_ACCEPT_DEPS.json').read_bytes());dep['status']='ROOT_FILLED'
dp=put(case/'SYNTHETIC_FILLED_DEPS.json',dep)
scheduler=art/'calibration_orchestrator_c2/v005/campaign_c2v005.py'
args=dict(wrapper_pin=wp,campaign_entry_pin=ep,chain_modules=modules,root_binding_pin=rbpin,policy_pin=rb['policy'],entry_pin=rb['entry'],deps_pin=dp,accept_entry_pin=pin(art/'eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py'),scheduler_pin=pin(scheduler),records_root=case/'acceptance',pause=lambda:None,max_polls=1)
installed=install(W,**args)
assert W.Context.__init__ is native_context_init and installed['Orchestrator'].run is native_run and installed['Cache'].put is native_put
assert O.CampaignExecutor is installed['Executor'] and O.Lock is installed['Lock']
checks=['unchanged empty-seal wrapper/core/policy sources load with actual A296 guard','root-published wrapper binding verified from synthetic entry bytes','native Context constructor, orchestrator run and cache put unchanged','private executor/cache/lock installation complete']
engine=art/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py'
E=types.ModuleType('_synthetic_installed_engine');E.__file__=str(engine);sys.modules[E.__name__]=E
exec(compile(engine.read_bytes(),str(engine),'exec'),E.__dict__)
ctx=types.SimpleNamespace(work_dir=case/'WORK',executor_kind='campaign',E=E,C=installed['scheduler'],cfg={'tail_readiness':{'state_enumerator':dep['deps']['enumerator'],'approved_certificate_producers':dep['policy']['approved_certificate_producers']}},**rb['context'])
orch=installed['Orchestrator'](ctx)
assert isinstance(orch.executor,installed['Executor']) and orch.executor._external_orch is orch and isinstance(orch.cache,installed['Cache'])
checks.append('native orchestrator and actual engine Probe construct with authenticated synthetic root context')
try:installed['phase_use'](ctx,{})
except W.CertificateRefusal:checks.append('missing parent lock raises native BaseException certificate refusal')
else:raise AssertionError('missing lock accepted')
bad=copy.copy(ctx);bad.config_sha256='0'*64
try:installed['Orchestrator'](bad)
except ValueError:checks.append('root context mismatch refuses before orchestrator construction')
else:raise AssertionError('context mismatch')
try:install(W,**args)
except ValueError:checks.append('double installation refuses')
else:raise AssertionError('double install')
report=dict(status='PASS',tested=checks,scope=__doc__,test=pin(Path(__file__)),installer=pin(root/'importer_installation_cx1v002.py'),wrapper=wp,untested=['real root published chain (not yet exists)','native Context gates and work identity (synthetic context supplied)','parent lock acquisition/release (not executed due no-overwrite constraint)','first acceptance and full installed campaign replay'])
print(put(case/'INSTALLATION_REPORT.json',report))
