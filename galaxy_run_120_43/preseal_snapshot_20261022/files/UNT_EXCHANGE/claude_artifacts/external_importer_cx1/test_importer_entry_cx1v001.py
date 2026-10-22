"""SYNTHETIC empty-seal chain installation; no context gates or campaign run.
Copies unchanged placeholder source bytes into a new inert tree. The two-line
synthetic entry fixture binds that tree; it is not a republished campaign entry.
"""
import ast,copy,hashlib,json,os,sys,tempfile,types
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from importer_entry_cx1v001 import build,strict
from snapshot_cx1v001 import Refusal
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
# Actual bootstrap loads a synthetic entry with an explicit Context-gate seam.
importer=pin(root/'importer_entry_cx1v001.py')
components={};pending=['importer_installation_cx1v004','pinned_helper_loader_cx1v002','importer_entry_cx1v001']
while pending:
 name=pending.pop()
 if name+'.py' in components:continue
 source=root/(name+'.py');components[name+'.py']=pin(source)
 for node in ast.walk(ast.parse(source.read_bytes())):
  names=[]
  if isinstance(node,ast.Import):names=[a.name.split('.')[0] for a in node.names]
  elif isinstance(node,ast.ImportFrom) and node.module:names=[node.module.split('.')[0]]
  pending.extend(n for n in names if (root/(n+'.py')).exists())
pp=put(case/'SYNTHETIC_POLICY_V007.json',dict(schema='CX1_IMPORTER_POLICY_V007',status='FROZEN_REVIEW_CANDIDATE',components=components))
cfg=dict(cache_id='b'*64,gate_digest='c'*64,work_dir=str(case/'WORK'),monitor=pin(art/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'),campaign=pin(scheduler),tail_readiness=dict(state_enumerator=dep['deps']['enumerator'],approved_certificate_producers=dep['policy']['approved_certificate_producers']))
cp=put(case/'SYNTHETIC_CONFIG.json',cfg)
engine=art/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py'
# These fixture definitions never replace or edit published production sources.
entry_text="""# SYNTHETIC Context gate seam for bootstrap integration only.
from pathlib import Path
import types,sys,json,hashlib
WRAPPER = Path(WRAPPER_PATH)
WRAPPER_SHA = WRAPPER_HASH
def module(path,name):
 m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
 exec(compile(Path(path).read_bytes(),str(path),'exec'),m.__dict__)
 return m
def load_wrapper():
 assert hashlib.sha256(WRAPPER.read_bytes()).hexdigest()==WRAPPER_SHA
 m=module(WRAPPER,'_synthetic_bootstrap_wrapper')
 class SyntheticContext(m.Context):
  def __init__(self,path):
   raw=Path(path).read_bytes();self.cfg=json.loads(raw)
   self.config_sha256=hashlib.sha256(raw).hexdigest()
   self.cache_id=self.cfg['cache_id'];self.gate_digest=self.cfg['gate_digest']
   self.work_dir=Path(self.cfg['work_dir']);self.executor_kind='campaign'
   self.E=module(ENGINE_PATH,'_synthetic_bootstrap_engine')
   self.M=module(self.cfg['monitor']['path'],'_synthetic_bootstrap_monitor')
   self.C=module(self.cfg['campaign']['path'],'_synthetic_bootstrap_scheduler')
 m.Context=SyntheticContext;m.O.Context=SyntheticContext
 return m
def check_patch(m):
 assert m.O.Context is m.Context and m.O.Orchestrator is m.Orchestrator
 return m.O
""".replace('WRAPPER_PATH',repr(wp['path'])).replace('WRAPPER_HASH',repr(wp['sha256'])).replace('ENGINE_PATH',repr(str(engine)))
cep=write(case/'SYNTHETIC_BOOTSTRAP_CAMPAIGN_ENTRY.py',entry_text.encode())
rb['policy']=pp;rb['entry']=importer;rb['context']=dict(config_sha256=cp['sha256'],cache_id=cfg['cache_id'],gate_digest=cfg['gate_digest'])
rb['runtime']['freeze']=put(case/'SYNTHETIC_BOOTSTRAP_FREEZE.json',dict(schema='CX1_IMPORTER_FREEZE_V001',utc='2026-10-21T11:00:00Z',policy=pp,entry=importer))
rp=put(case/'SYNTHETIC_BOOTSTRAP_ROOT.json',rb)
request=dict(schema='CX1_IMPORTER_INVOCATION_V001',status='ROOT_BOUND',actor='Claude2',policy=pp,entry=importer,root_binding=rp,campaign_entry=cep,wrapper=wp,config=cp,acceptance_deps=dp,acceptance_entry=args['accept_entry_pin'],scheduler=pin(scheduler),records_root=str(case/'records'),max_polls=1,poll_seconds=1,run=dict(max_waves=1,new_campaign=False))
request_pin=put(case/'SYNTHETIC_REQUEST.json',request)
orch,bound=build(request_pin)
assert orch.executor._external_orch is orch and orch.ctx.config_sha256==cp['sha256']
assert not (case/'WORK').exists() and not (case/'records').exists()
checks=['actual isolated bootstrap verifies invocation, all helper bytes, root published-chain pins and config','native empty-seal wrapper/engine plus explicit synthetic Context gate seam installed','native orchestrator and Probe created without run, records or work-dir writes']
def refuse(label,pin_):
 try:build(pin_)
 except BaseException as exc:
  if isinstance(exc,(KeyboardInterrupt,SystemExit)):raise
  checks.append(dict(case=label,reason=str(exc)))
 else:raise AssertionError(label)
refuse('wrong invocation hash',dict(request_pin,sha256='0'*64))
for key,value in [('actor','Codex1'),('status','TEMPLATE'),('max_polls',True),('poll_seconds',0)]:
 bad=copy.deepcopy(request);bad[key]=value
 refuse('invalid '+key,put(case/('BAD_'+key+'.json'),bad))
bad=copy.deepcopy(request);bad['wrapper']['sha256']='0'*64
refuse('wrong published wrapper bytes',put(case/'BAD_WRAPPER.json',bad))
try:strict(b'{"x":1,"x":2}')
except ValueError:checks.append('duplicate invocation key refused')
else:raise AssertionError('duplicate key')
report=dict(status='PASS',tested=checks,scope=__doc__,test=pin(Path(__file__)),entry=importer,request=request_pin,untested=['production Context gates and root approval','native run/lock IO','full installed entry execution and engine replay'])
print(put(case/'BOOTSTRAP_REPORT.json',report))
