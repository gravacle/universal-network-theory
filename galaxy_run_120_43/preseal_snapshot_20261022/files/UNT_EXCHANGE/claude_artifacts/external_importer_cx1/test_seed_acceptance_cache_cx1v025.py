"""Single inert seed integration; real acceptance/adapters/guard, handoff, admission and cache.
Scientific producer seams inherit the published H55 fixture; no production installation claim.
"""
import ast,copy,fcntl,hashlib,json,os,re,sys,types
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
fixture=root.parent/'s4_acceptance_c2/acceptance_q2/tests/test_acceptance_q2_c2v004.py'
raw=fixture.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='085cafbe8c7abebe15a0364eefa53dccb80214cd58c2d51e974b02c3d85ce4d4'
source=raw.decode().split("safe('W_suite'",1)[0]
# Reuse only fixture definitions, never the broad suite. All output is new and inert.
source=source.replace("not Path(os.path.abspath(p)).is_relative_to(ITEM)","not Path(os.path.abspath(p)).is_relative_to(INERT_ROOT)")
source=source.replace("RUN = ITEM / 'tests' / (os.environ.get('Q2_RUN_TAG', 'dev_v004') + '_run_' + UTC)","RUN = INERT_ROOT / ('seed_acceptance_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))")
source=source.replace("'retries': 1 if 'retried' in variant else 0}","'result_path':res_ref['path'], 'retries': 1 if 'retried' in variant else 0}")
old="receipt = wjson(call / 'RECEIPT.json', {'status': 'FINISHED', 'driver_status': 'COMPLETED', 'result': {'sha256': res_ref['sha256']}})"
new="""receipt_obj={'schema':MON.RECEIPT_SCHEMA,'status':'FINISHED','driver_status':'COMPLETED','exit_code':0,'stop_reason':None,'pins':{'spec':spec_ref,'driver':DRIVER_PIN},'result':res_ref}
    auth_python='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
    caps=dict(wall_cap_s=11,rss_cap_bytes=22,output_cap_bytes=33,poll_s=2.0)
    pins=dict(spec=spec_ref,driver=DRIVER_PIN,monitor=MONITOR_PIN,python=auth_python)
    command=[auth_python,'-I','-B',DRIVER_PIN['path'],'run','--spec',spec_ref['path'],'--outdir',str(out)]
    side=dict(schema=MON.RECEIPT_SCHEMA+'_LAUNCH',utc='2026-10-21T12:30:00Z',command=command,pins=pins,caps=caps,child_pid=123,retries_allowed=0)
    wjson(call/'RECEIPT.json.launch.json',side)
    receipt_obj.update(utc_start=side['utc'],utc_end='2026-10-21T12:31:00Z',command=command,pins=pins,caps=caps,child_pid=123,retries=0)
    receipt_obj['receipt_sha256']=hashlib.sha256(MON.canonical(receipt_obj).encode()).hexdigest()
    receipt = wjson(call / 'RECEIPT.json', receipt_obj)"""
assert source.count(old)==1;source=source.replace(old,new)
source=source.replace("res_ref = wjson(out / 'result.json', result)","result['speeds_km_s']={r['id']:r['speed_km_s'] for r in result['rows']}\n    res_ref = wjson(out / 'result.json', result)")
monpath=root.parent/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
monraw=monpath.read_bytes();assert hashlib.sha256(monraw).hexdigest()=='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
monitor=types.ModuleType('_seed_monitor');monitor.__file__=str(monpath);exec(compile(monraw,str(monpath),'exec'),monitor.__dict__)
driver_path=root.parent/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py'
driver_pin={'path':str(driver_path),'sha256':hashlib.sha256(driver_path.read_bytes()).hexdigest()}
F={'__file__':str(fixture),'__name__':'_seed_fixture','INERT_ROOT':root/'inert_fixtures','MON':monitor,'DRIVER_PIN':driver_pin,'MONITOR_PIN':{'path':str(monpath),'sha256':hashlib.sha256(monraw).hexdigest()}}
exec(compile(source,str(fixture),'exec'),F)
case=F['RUN'];put=F['wjson']
guard_path=root.parent/'eps_rule_successor_cx2/integration/guard/certificate_guard_b1_a296_cx2v003.py'
G=types.ModuleType('_seed_a296_guard');G.__file__=str(guard_path);sys.modules[G.__name__]=G
exec(compile(guard_path.read_bytes(),str(guard_path),'exec'),G.__dict__)
# The unmodified engine and actual Probe produce this natural seed request.
probe_fixture=root/'test_whole_engine_replay_cx1v001.py'
probe_source=probe_fixture.read_text().split('class Cache:',1)[0]
probe_source=probe_source.replace("'INERT_%02d'","'r%02d'")
P={'__file__':str(probe_fixture),'__name__':'_natural_seed_probe'}
exec(compile(probe_source,str(probe_fixture),'exec'),P)
miss=P['probe'].run(types.SimpleNamespace(forward=lambda key:None),'plan')
assert not miss['complete'] and len(miss['misses'])==1,miss
natural=miss['misses'][0];theta=natural['theta'];key=natural['key'];theta_key=P['g']['theta_key']
c=F['make_call']('DDO154_JACOBIAN_R28_%s_A1'%key[:16]);call=c.call;result=c.result;spec=c.spec;sp=F['ref'](call/'out/inputs/call_spec.json');rp=c.result_ref
work=case/'WORK';wd=work/'waves/wave_0001';wd.mkdir(parents=True)
importer_pin=F['ref'](root/'importer_entry_cx1v001.py')
components={};pending=['importer_installation_cx1v004','pinned_helper_loader_cx1v002','importer_entry_cx1v001']
while pending:
 name=pending.pop()
 if name+'.py' in components:continue
 path=root/(name+'.py');components[name+'.py']=F['ref'](path)
 for node in ast.walk(ast.parse(path.read_bytes())):
  names=[]
  if isinstance(node,ast.Import):names=[a.name.split('.')[0] for a in node.names]
  elif isinstance(node,ast.ImportFrom) and node.module:names=[node.module.split('.')[0]]
  pending.extend(n for n in names if (root/(n+'.py')).exists())
policy_pin=F['ref'](root/'IMPORTER_POLICY_CX1V007_F2.json')
assert policy_pin['sha256']=='6c8439ec0425baba87c1a600a81db8e7f9ed947c77a212e42d5c08bb35241383'
frozen_policy=json.loads(Path(policy_pin['path']).read_bytes())
assert frozen_policy['components']==components
config_pin=put(case/'SYNTHETIC_ENTRY_CONFIG.json',{'synthetic':True,'scope':'Context gate fixture only'})
freeze_pin=put(case/'SYNTHETIC_ENTRY_FREEZE.json',dict(schema='CX1_IMPORTER_FREEZE_V001',utc='2026-10-21T11:00:00Z',policy=policy_pin,entry=importer_pin))
plan_call={'call_index':0,'key':key,'theta':theta,'spec':spec,'spec_sha256':sp['sha256']}
plan={'wave':1,'config_sha256':config_pin['sha256'],'cache_id':'d'*64,'gate_digest':'e'*64,'calls':[plan_call]}
put(wd/'WAVE_PLAN.json',plan)
lockpath=work/'ORCHESTRATOR.lock';fd=os.open(lockpath,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
lock=types.SimpleNamespace(held=True,_fd=fd,path=lockpath)
checks=['unmodified engine and actual Probe generate the single seed request before plan commit']
try:
 F['prepare'](c,ev={'b1':True,'b1_evidence':True})
 rings,gas=F['derived'](c)
 policy=F['policy'](c,**F['b1_policy']([F['B1_EV']['sha256'],F['ROWP_SHA']]))
 # Production source loader, with only the disclosed H55 science seams adapted for inert input.
 from acceptance_loader_cx1v002 import load_acceptance
 from snapshot_cx1v001 import Snapshot
 base_record=json.loads((root/'inert_fixtures/accept_loader_az7jd41r/SYNTHETIC_ACCEPT_DEPS.json').read_bytes())
 policy['approved_certificate_producers'].append(base_record['policy']['approved_certificate_producers'][-1])
 record_policy={k:copy.deepcopy(policy[k]) for k in base_record['policy']}
 synthetic_record=dict(base_record,policy=record_policy,status='ROOT_FILLED')
 dep_record_pin=put(case/'SYNTHETIC_D021_DEPS.json',synthetic_record)
 load_snapshot=Snapshot()
 from contextlib import contextmanager
 @contextmanager
 def inert_acceptance_loader(**kwargs):
  with load_acceptance(**kwargs) as loaded:
   en=loaded.deps['enumerator'];cur=F['CUR']
   en.D.consumed_states=lambda **kw:copy.deepcopy(cur['discovery'])
   en.X.validate_graph=lambda **kw:{'ok':True,'blockers':[],'controls':[cur['control']]}
   en.C.derive_details=lambda **kw:{'point_sha256':cur['details']['point_sha256'],'custody_sha256':cur['details']['custody_sha256'],'modules':{},'row_contract':{'prereg':F['prereg']}}
   en.A.compute_i1t=F['stub_compute'];en.A.verify_product=lambda r,p:p.v
   en.A.verify_point=lambda spec,r,p,details:None;en.A.verify_occurrence=F['stub_occurrence']
   loaded.deps['evidence'].export_lo_source=F['stub_export'];loaded.deps['evidence'].R.replay_state=F['stub_replay']
   loaded.deps['lo_core'].PR.point_context=lambda spec:{'details':cur['details']}
   lo_globals=loaded.deps['lo_adapter'].__globals__;real_lo_env=lo_globals['_real_env']
   def inert_lo_env():
    e=real_lo_env();e.derive_details=lambda spec:copy.deepcopy(cur['details'])
    e.point_context=lambda spec:{'synthetic_point_context':cur['details']['point_sha256']}
    e.produce_current_lo=F['stub_produce_current_lo'];e.validate_config=F['stub_validate'];return e
   lo_globals['_real_env']=inert_lo_env
   srb_globals=loaded.deps['srb_adapter'].__globals__;real_srb_env=srb_globals['_real_env']
   def inert_srb_env():
    e=real_srb_env();e.derive_details=lambda spec:copy.deepcopy(cur['details']);return e
   srb_globals['_real_env']=inert_srb_env
   loaded.policy['packet_binding_reviews']=F['AnyReview']()
   native_accept=loaded.handoff.accept_call
   loaded.handoff.accept_call=lambda **kw:native_accept(**dict(kw,initial_rings_ref=rings,final_next_gas_ref=gas))
   yield loaded
 inv=F['run_enum'](c);identity=c.point.identity;custody=F['CUSTODY']
 # Exact existing wrapper IO and monitor setup, no old fixture or tests run.
 helper=root/'test_wrapper_certificate_snapshot_cx1v001.py';text=helper.read_text()
 wrapper=root.parent/'eps_rule_successor_cx2/integration/campaign/calibration_orchestrator_q5b1_ledger_a296_cx2v001.py';wr=wrapper.read_bytes()
 assert hashlib.sha256(wr).hexdigest()=='cb1f5e73753b69d1e8b6067c746b8fcda89d94d6bc4f34fb0a78f927e07cca04'
 exec(compile(text[text.index("W=types.ModuleType"):text.index('def codefile')],str(helper),'exec'),globals())
 def codefile(name,text):
  p=case/name
  with p.open('x') as f:f.write(text)
  return F['ref'](p)
 deriver=codefile('synthetic_custody.py','def derive_custody(**kw):return '+repr(custody)+'\n')
 enumerator=codefile('synthetic_inventory.py','def consumed_states(**kw):return '+repr(inv)+'\n')
 record={'identity':identity,'bundle':c.point.prelaunch,'eps_certificate':c.point.eps_slot,'lo_certificate':c.point.rho_slot}
 W.__dict__.update(Path=Path,json=json,O=O,M=M,G=G,Error=ValueError,DRIVER_SHA=driver_pin['sha256'],validate_block=lambda n:None,point_identity=lambda s:identity)
 from certificate_spec_adapter_cx1v004 import build_checker
 W.__dict__['__builtins__']=__builtins__
 W.certificate_check=build_checker(wr,str(wrapper),W,expected_sha256=F['ref'](wrapper)['sha256'])
 ctx=types.SimpleNamespace(numerics=spec['numerics'],cfg={'tail_readiness':{'custody_deriver':deriver,'state_enumerator':base_record['deps']['enumerator'],'approved_certificate_producers':policy['approved_certificate_producers']},'monitor':F['ref'](monpath)},M=monitor,certificate_policy_gate=lambda:{'ok':True},certificate_record=lambda ident:record)
 ctx.work_dir=work;ctx.config_sha256=plan['config_sha256'];ctx.cache_id=plan['cache_id'];ctx.gate_digest=plan['gate_digest'];ctx.driver=driver_pin
 mapped={'key':key,'spec':spec,'raw':Path(sp['path']).read_bytes(),'sha256':sp['sha256']}
 ctx.mapper=types.SimpleNamespace(build=lambda theta,recovery=None:mapped);ctx.prelaunch_check=lambda spec:None
 ctx.certificate_check=types.MethodType(W.certificate_check,ctx)
 native_checker=ctx.certificate_check
 def diagnostic_checker(*args,**kwargs):
  checked=native_checker(*args,**kwargs)
  if not checked.get('ok'):print('INERT_CHECKER_REFUSAL',checked)
  return checked
 ctx.certificate_check=diagnostic_checker
 candidate={'call_index':0,'call_dir':str(call),'key':key,'theta':theta,'spec':sp,'receipt':c.receipt,'case':'seed','row':28}
 candidate['direct_plan']=put(case/'direct_plan.json',{'schema':'UNT_STEP4_LAUNCH_PLAN_CX1V001','binding_status':'ROOT_BOUND','launcher':F['ref'](root.parent/'s1_successors_c2/step4_launcher_c2v015.py'),'monitor':F['ref'](monpath),'calls':[{'spec_status':'ROOT_FINAL','pending':[],'wall_cap_s':11,'rss_cap_bytes':22,'output_cap_bytes':33,'case':'seed','point_key':key,'row':28,'spec':sp,'driver':driver_pin,'outdir':str(call/'out'),'receipt':str(call/'RECEIPT.json'),'monitor_log':str(call/'monitor.log')}],'launcher_log':str(case/'batch.log')})
 # Join the real observer and D022 callback to this immutable inert call.
 authroot=json.loads((root/'inert_fixtures/observation_entry_zn2194gv/inert_root_binding.json').read_bytes())
 reg=json.loads(Path(authroot['register']['path']).read_bytes())
 authroot['policy']=policy_pin;authroot['entry']=importer_pin;authroot['runtime']['freeze']=freeze_pin
 authroot['schema']='CX1_IMPORTER_ROOT_BINDING_V002';authroot['context']={k:plan[k] for k in ('config_sha256','cache_id','gate_digest')}
 authroot['direct_plan']=candidate['direct_plan'];authroot['runtime'].update(driver=driver_pin,monitor=F['ref'](monpath),output_root=str(call.parent))
 python_path=Path('/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
 interpreter=dict(realpath=str(python_path.resolve()),sha256=hashlib.sha256(python_path.read_bytes()).hexdigest())
 capture=json.loads(Path(reg['entries'][0]['runtime_capture']['path']).read_bytes())
 capture.update(interpreter=interpreter,driver=dict(realpath=driver_pin['path'],sha256=driver_pin['sha256']),monitor=dict(realpath=str(monpath),sha256=F['ref'](monpath)['sha256']))
 direct_capture=put(case/'SYNTHETIC_DIRECT_CAPTURE.json',capture);campaign_capture=put(case/'SYNTHETIC_CAMPAIGN_CAPTURE.json',capture)
 authroot['runtime']['campaign_capture']=campaign_capture
 reg['entries'][0].update(key=key,spec=sp,call_root=str(call))
 launcher=F['ref'](root.parent/'s1_successors_c2/step4_launcher_c2v015.py')
 for e in reg['entries']:
  e.update(runtime_capture=direct_capture,launcher=launcher)
  if e['key']!=key:e['call_root']=str(call.parent/Path(e['call_root']).name)
 regpin=put(case/'SYNTHETIC_REGISTER.json',reg);authroot['register']=regpin
 launch=json.loads(Path(authroot['runtime']['direct_launch']['path']).read_bytes());launch.update(register=regpin,runtime_capture=direct_capture,interpreter=interpreter,freeze=freeze_pin)
 authroot['runtime']['direct_launch']=put(case/'SYNTHETIC_LAUNCH.json',launch)
 binding=json.loads(Path(authroot['binding']['path']).read_bytes());binding.update(register=regpin,campaign_capture=campaign_capture,interpreter=interpreter,context=authroot['context'],freeze=freeze_pin)
 authroot['binding']=put(case/'SYNTHETIC_BINDING.json',binding)
 required=[regpin,driver_pin,F['ref'](monpath),authroot['policy'],authroot['entry'],frozen_policy['runtime_capture']['producer']]
 for e in reg['entries']:required.extend(e[k] for k in ('spec','launcher','guard','binder','dbp','runtime_capture'))
 required=list({(p['path'],p['sha256']):p for p in required}.values())
 from final_envelope_evidence_cx1v001 import comparator
 envpath=Path(authroot['envelope']['tool']['path']);envraw=envpath.read_bytes();env_tool=comparator(envraw,str(envpath))
 nodes=[n for n in ast.parse(envraw).body if isinstance(n,ast.FunctionDef) and n.name in ('write_signed','_fsync_dir')]
 env_tool.os=os;exec(compile(ast.Module(body=nodes,type_ignores=[]),str(envpath),'exec'),env_tool.__dict__)
 envdir=case/'ENVELOPE_L2_DIRECT';envdir.mkdir()
 def signed_env(name,obj):
  path=envdir/name;env_tool.write_signed(str(path),obj);return F['ref'](path),json.loads(path.read_bytes())
 pspin,ps=signed_env('PINSET.json',dict(schema=env_tool.SCHEMA_PINSET,phase='L2_DIRECT',pins=required,excluded=[],unresolved_pins=[]))
 start=env_tool.observe(ps,pspin['sha256'],pspin['path']);start['label']='start'
 startpin,startobj=signed_env('START.json',start)
 authroot['envelope'].update(start=startpin,pinset=pspin)
 authpin=put(case/'SYNTHETIC_ROOT_BINDING.json',authroot)
 # Real parent classifier and wrapper certificate layer; only taxonomy is synthetic.
 pt=ast.parse(parent_raw)
 selected={'canonical','decode_ck_float','collect_evidence','tax_record','forward_from_result','normalize_campaign_status'}
 funcs=[n for n in pt.body if isinstance(n,ast.FunctionDef) and n.name in selected]
 O.re=re;O.ast=ast;O.CK_FLOAT='f';O.CACHED_CLASSES=('VALID','MODEL_INVALID');O.OrchestratorError=ValueError
 exec(compile(ast.Module(body=funcs,type_ignores=[]),str(parent),'exec'),O.__dict__)
 pc=next(n for n in pt.body if isinstance(n,ast.ClassDef) and n.name=='CampaignExecutor')
 methods=[n for n in pc.body if isinstance(n,ast.FunctionDef) and n.name in ('__init__','campaign_dict','execute','classify')]
 cls=ast.ClassDef(name='SeedParentExecutor',bases=[],keywords=[],body=methods,decorator_list=[])
 exec(compile(ast.fix_missing_locations(ast.Module(body=[cls],type_ignores=[])),str(parent),'exec'),O.__dict__)
 from classifier_spec_adapter_cx1v001 import build_classifier
 O.SeedParentExecutor._classify=build_classifier(parent_raw,str(parent),O)
 W.OldExecutor=O.SeedParentExecutor
 wc=next(n for n in ast.parse(wr).body if isinstance(n,ast.ClassDef) and n.name=='CampaignExecutor')
 exec(compile(ast.Module(body=[wc],type_ignores=[]),str(wrapper),'exec'),W.__dict__)
 ctx.row_ids=F['ROW_IDS'];taxout=dict(rule='INERT',code=None,**{'class':'VALID','judgment_call':False})
 ctx.taxonomy=types.SimpleNamespace(sha256='a'*64,classify=lambda result,evidence:taxout)
 real_executor=W.CampaignExecutor(ctx)
 # Load unchanged empty-seal native chain through the actual entry bootstrap.
 placeholder=root.parent/'eps_rule_successor_cx2/integration/campaign/placeholder_chain_a296_cx2v001/v006r12_c4'
 chain=case/'SYNTHETIC_ENTRY_CHAIN';(chain/'v006r12_c4').mkdir(parents=True);(chain/'v006r8').mkdir()
 for name in ('adoption_policy_cx2v006r12_c4.py','calibration_core_cx2v006r12_c4.py','calibration_orchestrator_cx2v006r12_c4_q5b1.py'):
  with (chain/'v006r12_c4'/name).open('xb') as f:f.write((placeholder/name).read_bytes())
 sens=root.parent/'calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py'
 with (chain/'v006r8'/sens.name).open('xb') as f:f.write(sens.read_bytes())
 native_wrapper=F['ref'](chain/'v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py')
 scheduler_path=root.parent/'calibration_orchestrator_c2/v005/campaign_c2v005.py'
 ctx.C=types.ModuleType('_inert_no_launch_boundary');ctx.C.__file__=str(scheduler_path)
 ctx.E=P['E'];ctx.executor_kind='campaign'
 fixture_context=types.ModuleType('_cx1_seed_context');fixture_context.ctx=ctx;sys.modules[fixture_context.__name__]=fixture_context
 fixture_entry_text="""# SYNTHETIC Context gate seam, not a production entry.
from pathlib import Path
import types,sys,hashlib
WRAPPER = Path(WRAPPER_PATH)
WRAPPER_SHA = WRAPPER_HASH
def load_wrapper():
 raw=WRAPPER.read_bytes();assert hashlib.sha256(raw).hexdigest()==WRAPPER_SHA
 m=types.ModuleType('_cx1_seed_native_wrapper');m.__file__=str(WRAPPER);sys.modules[m.__name__]=m
 exec(compile(raw,str(WRAPPER),'exec'),m.__dict__)
 class SyntheticContext(m.Context):
  def __new__(cls,path):return sys.modules['_cx1_seed_context'].ctx
 m.Context=SyntheticContext;m.O.Context=SyntheticContext
 return m
def check_patch(m):
 assert m.O.Context is m.Context and m.O.Orchestrator is m.Orchestrator
 return m.O
""".replace('WRAPPER_PATH',repr(native_wrapper['path'])).replace('WRAPPER_HASH',repr(native_wrapper['sha256']))
 fixture_entry=codefile('SYNTHETIC_BOOTSTRAP_ENTRY.py',fixture_entry_text)
 accept_source=root.parent/'eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py'
 invocation=put(case/'SYNTHETIC_INVOCATION.json',dict(schema='CX1_IMPORTER_INVOCATION_V001',status='ROOT_BOUND',actor='Claude2',policy=policy_pin,entry=importer_pin,root_binding=authpin,campaign_entry=fixture_entry,wrapper=native_wrapper,config=config_pin,acceptance_deps=dep_record_pin,acceptance_entry=F['ref'](accept_source),scheduler=F['ref'](scheduler_path),records_root=str(case/'accepted_records'),max_polls=1,poll_seconds=1,run=dict(max_waves=1,new_campaign=False)))
 from importer_entry_cx1v001 import build
 orch,invocation_doc=build(invocation)
 W=sys.modules['_cx1_seed_native_wrapper'];O=W.O;M=W.M;G=W.G
 mods=[W,O,M,G,monitor,W.S]
 # Explicit fixture science/identity seams, same scope as the earlier seed test.
 W.point_identity=lambda spec:identity;W.validate_block=lambda n:None
 ctx.certificate_check=types.MethodType(W.Context.certificate_check,ctx)
 ctx.check_cached_certificate=types.MethodType(W.Context.check_cached_certificate,ctx)
 orch.check_identity_now=lambda:[]
 # Register the already kernel-held fixture lock through the actual tracker.
 # Native acquire writes holder bytes, forbidden in this no-overwrite test.
 tracked=O.Lock(work);tracked.held=True;tracked._fd=fd
 native_acquire=O.Lock.__bases__[0].acquire
 O.Lock.__bases__[0].acquire=lambda self:True
 try:assert tracked.acquire()
 finally:O.Lock.__bases__[0].acquire=native_acquire
 lock=tracked
 checks.append('actual frozen policyV007 plus isolated entry install native classes with explicit Context and lock-IO seams')
 from direct_handoff_writer_cx1v001 import write_handoff
 native_load_module=O.load_pinned_module
 def inert_inventory_loader(pin,name,label):
  if pin==base_record['deps']['enumerator']:
   O.read_pinned(pin,label)
   m=types.ModuleType(name);m.__file__=enumerator['path'];m.consumed_states=lambda **kw:F['run_enum'](c);return m
  return native_load_module(pin,name,label)
 O.load_pinned_module=inert_inventory_loader
 # The entry helper loader keeps private helper modules; bind the declared
 # H55 science loader on the private leg reached by the installed factory.
 ex=orch.executor
 observe_fn=type(ex)._observe_valid
 private_complete=observe_fn.__globals__['complete']
 private_complete.__globals__['load_acceptance']=inert_acceptance_loader
 legargs=dict(lock=lock,modules=mods,wrapper=W,accept_entry_pin=F['ref'](accept_source),deps_pin=dep_record_pin,records_root=case/'accepted_records',wave_dir=wd,plan=plan,candidate=candidate)
 complete=private_complete
 completed=complete(orch,**legargs)
 assert completed['verified']['classification']=='VALID'
 candidate=completed['candidate']
 accpin=candidate['acceptance'];bound=candidate['bundle'];acceptance=json.loads(Path(accpin['path']).read_bytes())
 assert acceptance['reading']=='ACCEPTED'
 checks.append('first acceptance pass runs inside actual VALID leg through D021 loader, with explicit H55 science seams')
 beforepasses=W.acceptance_passes(call)
 repeated=complete(orch,**dict(legargs,candidate=candidate))
 assert repeated['candidate']==candidate and W.acceptance_passes(call)==beforepasses
 checks.append('actual VALID leg produces acceptance, writes handoff and restarts without another pass')
 import valid_admission_cx1v002 as V
 got=V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate)
 assert got['classification']=='VALID';checks.append('actual VALID admission and parent/wrapper classification check produced evidence under held parent lock')

 # Exercise the current lazy hook with its actual bounded wait and admission.
 from executor_hook_cx1v006 import make_executor_type
 base=types.ModuleType('_seed_no_launch_scheduler')
 def forbidden_launch(**kw):raise AssertionError('unexpected local launch')
 base.run_campaign=forbidden_launch;ctx.C=base
 Parent=W.CampaignExecutor
 ctx.max_concurrent=1;ctx.process_budget=1;ctx.stage_aware=False;ctx.python=sys.executable
 ctx.cfg.update(driver=driver_pin,per_call={'inert':True},campaign_wall_cap_s=100)
 class Scheduler:
  @staticmethod
  def run_campaign(_admitted_external,**kw):
   assert kw['campaign']['calls']==[{'spec':spec}] and kw['campaign']['driver']==driver_pin
   assert kw['campaign_dir']==str(wd/'campaign') and kw['resume'] is False
   assert set(_admitted_external)=={0}
   return {'ok':True,'calls':[dict(_admitted_external[0])],'status':'INERT_NO_LAUNCH','launched':0}
 ex=orch.executor
 # Replace only the scheduler IO boundary: no native launch/status-file writes.
 execute_fn=next(cls.__dict__['execute'] for cls in type(ex).__mro__ if 'execute' in cls.__dict__)
 closed=dict(zip(execute_fn.__code__.co_freevars,(cell.cell_contents for cell in execute_fn.__closure__)))
 closed['scheduler'].run_campaign=Scheduler.run_campaign
 orch.executor=ex
 records,meta=ex.execute(wd,plan,False,None)
 assert records[0]['call_dir']==str(call) and meta['external_import_count']==1 and ctx.C is base
 assert ex.classify(plan_call,records[0])[0]=='VALID' and not (wd/'campaign').exists()
 checks.append('actual parent executor plus current lazy hook/wait/admission selects produced evidence without a local launch')
 from snapshot_cx1v001 import Refusal
 def must_refuse(label,fn):
  try:fn()
  except BaseException as exc:
   assert type(exc).__name__ in ('Refusal','ValueError','FileNotFoundError'),(label,exc)
   checks.append(label)
  else:raise AssertionError(label)
 negative=put(case/'negative_acceptance.json',dict(acceptance,reading='INCOMPLETE'))
 original=copy.deepcopy(ex._external_selected[0]);ex._external_selected[0]['acceptance']=negative
 must_refuse('fresh ingest rejects a nonaccepted acceptance record',lambda:ex.classify(plan_call,records[0]))
 ex._external_selected[0]=original
 must_refuse('unrequested call refuses admission',lambda:V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=dict(candidate,call_index=1)))
 must_refuse('wrong theta refuses admission',lambda:V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=dict(candidate,theta={'x':2.0})))
 original_driver=ctx.driver;ctx.driver=dict(ctx.driver,sha256='0'*64)
 must_refuse('authenticated runtime/code mismatch refuses before scheduling',lambda:ex.execute(wd,plan,False,None))
 ctx.driver=original_driver
 records,meta=ex.execute(wd,plan,False,None)
 assert ex.classify(plan_call,records[0])[0]=='VALID' and not orch.cache.entries and ctx.C is base
 checks.append('negative controls leave no cache admission or scheduler mutation')
 # Actual installed native cache. Exclusive writer is the declared IO seam.
 def exclusive_cache_writer(path,obj):
  with open(path,'x') as f:json.dump(obj,f)
 O.write_json_atomic_x=exclusive_cache_writer
 cache=orch.cache;cache.entries_dir.mkdir(parents=True)
 out=taxout
 ev=O.collect_evidence(call/'out',result,ctx.row_ids,ctx.taxonomy);assert not ev['errors'],ev
 fin,why=O.finish_binding(rp['path'],rp['sha256']);assert not why
 receipt_path=call/'RECEIPT.json';receipt=json.loads(receipt_path.read_bytes())
 pv=dict(execution_origin='DIRECT_EXTERNAL',result_path=rp['path'],result_sha256=rp['sha256'],spec_sha256=sp['sha256'],receipt_path=str(receipt_path),receipt_file_sha256=F['ref'](receipt_path)['sha256'],receipt_sha256_self=receipt['receipt_sha256'],finish=fin,evidence_files=ev['files'],taxonomy=O.tax_record(out,ctx.taxonomy))
 pv.update(got['provenance'])
 forward=O.forward_from_result(result,'VALID',None,'INERT',ctx.row_ids)
 stored,new=cache.put(key=key,theta=theta,classification='VALID',failure_class=None,source='WAVE',provenance=pv,forward=forward)
 assert new;checks.append('actual parent/wrapper cache put validates produced acceptance lineage')
 disk=cache.entries_dir/(key+'.json');before=disk.read_bytes()
 reopened=type(cache)(ctx);reopened.open(create=False)
 assert reopened.forward(key)==forward;checks.append('persisted accepted seed reopens and replays through actual cache verification')

 # Compare complete engine runs with only the verified external seed imported.
 # Remaining points are explicit inert oracle responses, not scientific calls.
 def oracle(th):
  return dict(valid=True,speeds_km_s={rid:v+3*(th['x']-theta['x']) for rid,v in forward['speeds_km_s'].items()},reasons=[])
 baseline=P['E'].run_calibration_region(forward=oracle,**P['kw'])
 def replay(use_external,label):
  data={};plans=[];external_reads=0
  proxy=types.SimpleNamespace(forward=lambda k:data.get(k))
  for i in range(200):
   request=P['probe'].run(proxy,'plan')
   if request['complete']:
    replayed=P['probe'].run(proxy,'replay');assert replayed['complete']
    return plans,replayed['run'],external_reads
   assert request['misses']
   plans.append(request['misses'])
   planfile=case/('%s_natural_%03d.json'%(label,i));put(planfile,request['misses'])
   assert json.loads(planfile.read_bytes())==request['misses']
   for req in request['misses']:
    if use_external and req['key']==key:
     data[key]=reopened.forward(key);external_reads+=1
    else:data[req['key']]=oracle(req['theta'])
  raise AssertionError('engine replay did not terminate')
 localplans,localrun,_=replay(False,'local')
 importplans,importrun,external_reads=replay(True,'import')
 assert external_reads==1 and localplans==importplans and localrun==importrun==baseline
 checks.append('full unmodified engine run and natural request sequence equal with the verified seed imported lazily exactly once')
 assert reopened.forward(key)==forward
 end=copy.deepcopy(startobj);end['label']='end';end['created_epoch_ns']+=1;end['files'][0]['mtime_ns']+=1
 endpin,endobj=signed_env('END.json',end)
 verdict=env_tool.compare_saved(startobj,endobj)
 final=dict(schema=env_tool.SCHEMA_COMPARE,phase='L2_DIRECT',pin_set=startobj['pin_set'],unresolved_pins_not_checked=0,**verdict)
 for name,pin_,obj in [('start',startpin,startobj),('end',endpin,endobj)]:final[name]=dict(path=pin_['path'],file_sha256=pin_['sha256'],body_sha256=obj['body_sha256'],created_utc=obj.get('created_utc'))
 signed_env('COMPARE.json',final)
 from snapshot_cx1v001 import Refusal
 try:reopened.forward(key)
 except W.CertificateRefusal:checks.append('final invalidation refuses replay of the accepted seed through native BaseException boundary')
 else:raise AssertionError('invalidation bypass')
 assert disk.read_bytes()==before;checks.append('invalidation preserves cached evidence bytes')
finally:
 fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
report={'status':'PASS','tested':checks,'scope':__doc__,'seams':['H55 synthetic science environments and evidence exporter','synthetic Context identity, policy, mapper and custody/inventory modules','synthetic VALID taxonomy; real parent/wrapper classifier','exclusive writer double instead of parent atomic unlink writer','synthetic root runtime records checked by actual observer and D022 callback','synthetic entry Context constructor and parent lock acquire IO','synthetic scheduler boundary'],'untested':['native Context scientific gates, native lock IO and native scheduler IO (explicit inert seams)','real root-supplied record installation; synthetic D021 record tested','root-authenticated phase publication and campaign freeze'],'fixture':F['ref'](fixture),'test':F['ref'](__file__),'acceptance':accpin,'output':str(case)}
print(put(case/'SEED_INTEGRATION_REPORT.json',report))
