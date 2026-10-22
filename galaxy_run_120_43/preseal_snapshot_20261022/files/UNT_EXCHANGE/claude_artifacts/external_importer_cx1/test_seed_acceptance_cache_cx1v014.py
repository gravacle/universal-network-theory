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
    receipt_obj['receipt_sha256']=hashlib.sha256(MON.canonical(receipt_obj).encode()).hexdigest()
    receipt = wjson(call / 'RECEIPT.json', receipt_obj)"""
assert source.count(old)==1;source=source.replace(old,new)
source=source.replace("res_ref = wjson(out / 'result.json', result)","result['speeds_km_s']={r['id']:r['speed_km_s'] for r in result['rows']}\n    res_ref = wjson(out / 'result.json', result)")
monpath=root.parent/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
monraw=monpath.read_bytes();assert hashlib.sha256(monraw).hexdigest()=='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
monitor=types.ModuleType('_seed_monitor');monitor.__file__=str(monpath);exec(compile(monraw,str(monpath),'exec'),monitor.__dict__)
driver_path=root.parent/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py'
driver_pin={'path':str(driver_path),'sha256':hashlib.sha256(driver_path.read_bytes()).hexdigest()}
F={'__file__':str(fixture),'__name__':'_seed_fixture','INERT_ROOT':root/'inert_fixtures','MON':monitor,'DRIVER_PIN':driver_pin}
exec(compile(source,str(fixture),'exec'),F)
case=F['RUN'];put=F['wjson'];G=F['GUARD_B1']
c=F['make_call']('SEED');call=c.call;result=c.result;spec=c.spec;sp=F['ref'](call/'out/inputs/call_spec.json');rp=c.result_ref
work=case/'WORK';wd=work/'waves/wave_0001';wd.mkdir(parents=True)
# The unmodified engine and actual Probe produce this natural seed request.
probe_fixture=root/'test_whole_engine_replay_cx1v001.py'
probe_source=probe_fixture.read_text().split('class Cache:',1)[0]
probe_source=probe_source.replace("'INERT_%02d'","'r%02d'")
P={'__file__':str(probe_fixture),'__name__':'_natural_seed_probe'}
exec(compile(probe_source,str(probe_fixture),'exec'),P)
miss=P['probe'].run(types.SimpleNamespace(forward=lambda key:None),'plan')
assert not miss['complete'] and len(miss['misses'])==1,miss
natural=miss['misses'][0];theta=natural['theta'];key=natural['key'];theta_key=P['g']['theta_key']
plan_call={'call_index':0,'key':key,'theta':theta,'spec':spec,'spec_sha256':sp['sha256']}
plan={'wave':1,'config_sha256':'c'*64,'cache_id':'d'*64,'gate_digest':'e'*64,'calls':[plan_call]}
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
 with load_acceptance(snapshot=load_snapshot,record_pin=dep_record_pin,expected_enumerator=base_record['deps']['enumerator'],expected_guard=base_record['deps']['guard'],expected_producers=record_policy['approved_certificate_producers'],output_roots=[case],allow_synthetic=True) as loaded:
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
  active_policy=dict(loaded.policy,receipt=c.receipt,prelaunch_bundle=c.point.prelaunch,packet_binding_reviews=F['AnyReview']())
  acceptance,accpin=loaded.handoff.accept_call(call_dir=call,spec=spec,deps=loaded.deps,policy=active_policy,records_dir=case/'accepted_records'/key/'PASS_001',initial_rings_ref=rings,final_next_gas_ref=gas)
  assert max(load_snapshot.read_counts.values())==1
 checks.append('D021 loader invokes actual selected producers with explicit H55 science seams and single-read snapshot')
 assert acceptance['reading']=='ACCEPTED',acceptance
 checks.append('committed seed plan precedes real acceptance handoff with H55 scientific seams')
 bound=acceptance['bundle'];inv=F['run_enum'](c);identity=c.point.identity;custody=F['CUSTODY']
 # Exact existing wrapper IO and monitor setup, no old fixture or tests run.
 helper=root/'test_wrapper_certificate_snapshot_cx1v001.py';text=helper.read_text()
 wrapper=root.parent/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py';wr=wrapper.read_bytes()
 assert hashlib.sha256(wr).hexdigest()=='7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229'
 exec(compile(text[text.index("W=types.ModuleType"):text.index('def codefile')],str(helper),'exec'),globals())
 def codefile(name,text):
  p=case/name
  with p.open('x') as f:f.write(text)
  return F['ref'](p)
 deriver=codefile('synthetic_custody.py','def derive_custody(**kw):return '+repr(custody)+'\n')
 enumerator=codefile('synthetic_inventory.py','def consumed_states(**kw):return '+repr(inv)+'\n')
 record={'identity':identity,'bundle':c.point.prelaunch,'eps_certificate':c.point.eps_slot,'lo_certificate':c.point.rho_slot}
 W.__dict__.update(Path=Path,json=json,O=O,M=M,G=G,Error=ValueError,DRIVER_SHA=driver_pin['sha256'],validate_block=lambda n:None,point_identity=lambda s:identity)
 from certificate_spec_adapter_cx1v001 import build_checker
 W.__dict__['__builtins__']=__builtins__
 W.certificate_check=build_checker(wr,str(wrapper),W)
 ctx=types.SimpleNamespace(numerics=spec['numerics'],cfg={'tail_readiness':{'custody_deriver':deriver,'state_enumerator':enumerator,'approved_certificate_producers':policy['approved_certificate_producers']},'monitor':F['ref'](monpath)},M=monitor,certificate_policy_gate=lambda:{'ok':True},certificate_record=lambda ident:record)
 ctx.work_dir=work;ctx.config_sha256=plan['config_sha256'];ctx.cache_id=plan['cache_id'];ctx.gate_digest=plan['gate_digest'];ctx.driver=driver_pin
 mapped={'key':key,'spec':spec,'raw':Path(sp['path']).read_bytes(),'sha256':sp['sha256']}
 ctx.mapper=types.SimpleNamespace(build=lambda theta,recovery=None:mapped);ctx.prelaunch_check=lambda spec:None
 ctx.certificate_check=types.MethodType(W.certificate_check,ctx)
 candidate={'call_index':0,'call_dir':str(call),'key':key,'theta':theta,'spec':sp,'receipt':c.receipt,'acceptance':accpin,'bundle':bound,'case':'seed','row':'seed'}
 candidate['direct_plan']=put(case/'direct_plan.json',{'calls':[{'case':'seed','point_key':key,'row':'seed','spec':sp,'driver':driver_pin,'outdir':str(call/'out'),'receipt':str(call/'RECEIPT.json'),'monitor_log':str(call/'monitor.log')}],'launcher_log':str(case/'batch.log')})
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
 orch=types.SimpleNamespace(ctx=ctx,check_identity_now=lambda:[],_external_parent_theta_key=theta_key,cache=types.SimpleNamespace(entries={}),executor=real_executor)
 mods=[W,O,M,G,monitor]
 from direct_handoff_writer_cx1v001 import write_handoff
 W.TAILSTATES_PREFIX='ACCEPTANCE_TAILSTATES_'
 W.TAILSTATES_RE=re.compile(r'ACCEPTANCE_TAILSTATES_C2V002_A([0-9]{3})')
 ap=next(n for n in ast.parse(wr).body if isinstance(n,ast.FunctionDef) and n.name=='acceptance_passes')
 exec(compile(ast.Module(body=[ap],type_ignores=[]),str(wrapper),'exec'),W.__dict__)
 from direct_valid_leg_cx1v002 import complete
 accept_source=root.parent/'eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py'
 legargs=dict(lock=lock,modules=mods,wrapper=W,accept_entry_pin=F['ref'](accept_source),deps_pin=dep_record_pin,records_root=case/'accepted_records',wave_dir=wd,plan=plan,candidate=candidate)
 completed=complete(orch,**legargs)
 assert completed['verified']['classification']=='VALID'
 candidate=completed['candidate']
 beforepasses=W.acceptance_passes(call)
 repeated=complete(orch,**dict(legargs,candidate=candidate))
 assert repeated['candidate']==candidate and W.acceptance_passes(call)==beforepasses
 checks.append('actual VALID leg discovers the existing record, writes the handoff and repeats without a second producer pass')
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
 ex=make_executor_type(Parent,Scheduler)(ctx)
 ex._external_orch=orch;ex._external_lock=lambda:lock;ex._external_modules=mods
 ex._external_candidate_inventory=lambda:[copy.deepcopy(candidate)]
 observation=dict(natural_plan_committed=True,registered=True,identity_bound=True,runtime_environment_bound=True,envelope_valid=True,direct_state='TERMINAL',outcome='COMPLETED_VALID',acceptance=acceptance['reading'])
 ex._external_observe=lambda candidate,ca:dict(observation)
 ex._external_pause=lambda:None;ex._external_max_polls=1;orch.executor=ex
 records,meta=ex.execute(wd,plan,False,None)
 assert records[0]['call_dir']==str(call) and meta['external_import_count']==1 and ctx.C is base
 assert ex.classify(plan_call,records[0])[0]=='VALID' and not (wd/'campaign').exists()
 checks.append('actual parent executor plus current lazy hook/wait/admission selects produced evidence without a local launch')
 from snapshot_cx1v001 import Refusal
 def must_refuse(label,fn):
  try:fn()
  except (Refusal,ValueError,FileNotFoundError):checks.append(label)
  else:raise AssertionError(label)
 negative=put(case/'negative_acceptance.json',dict(acceptance,reading='INCOMPLETE'))
 original=copy.deepcopy(ex._external_selected[0]);ex._external_selected[0]['acceptance']=negative
 must_refuse('fresh ingest rejects a nonaccepted acceptance record',lambda:ex.classify(plan_call,records[0]))
 ex._external_selected[0]=original
 must_refuse('unrequested call refuses admission',lambda:V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=dict(candidate,call_index=1)))
 must_refuse('wrong theta refuses admission',lambda:V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=dict(candidate,theta={'x':2.0})))
 observation['runtime_environment_bound']=False
 must_refuse('runtime mismatch refuses before scheduling',lambda:ex.execute(wd,plan,False,None))
 observation['runtime_environment_bound']=True;observation['direct_state']='RUNNING'
 must_refuse('in-flight wait limit holds without duplicate launch',lambda:ex.execute(wd,plan,False,None))
 observation['direct_state']='TERMINAL';observation['outcome']='COMPLETED_INVALID'
 must_refuse('speculative invalid remains unimported',lambda:ex.execute(wd,plan,False,None))
 observation['outcome']='COMPLETED_VALID'
 records,meta=ex.execute(wd,plan,False,None)
 assert ex.classify(plan_call,records[0])[0]=='VALID' and not orch.cache.entries and ctx.C is base
 checks.append('negative controls leave no cache admission or scheduler mutation')
 # Reuse existing actual parent/cache setup, not its fixture or test body.
 cachetest=root/'test_cache_phase_checkpoint_replay_cx1v001.py';cachetext=cachetest.read_text()
 setup=cachetext[cachetext.index('from cache_verify_scope_cx1v003 import make_verifier'):cachetext.index('\npassed=[]')]
 setup=setup.replace("ctx.row_ids=['INERT_A','INERT_B']","ctx.row_ids=F['ROW_IDS']")
 setup=setup.replace("'canonical','collect_evidence'","'decode_ck_float','canonical','collect_evidence'")
 setup=setup.replace('theta_key=G.digest','theta_key=theta_key')
 exec(compile(setup,str(cachetest),'exec'),globals())
 O.CK_FLOAT='f'
 ev=O.collect_evidence(call/'out',result,ctx.row_ids,ctx.taxonomy);assert not ev['errors'],ev
 fin,why=O.finish_binding(rp['path'],rp['sha256']);assert not why
 receipt_path=call/'RECEIPT.json';receipt=json.loads(receipt_path.read_bytes())
 pv=dict(execution_origin='DIRECT_EXTERNAL',result_path=rp['path'],result_sha256=rp['sha256'],spec_sha256=sp['sha256'],receipt_path=str(receipt_path),receipt_file_sha256=F['ref'](receipt_path)['sha256'],receipt_sha256_self=receipt['receipt_sha256'],finish=fin,evidence_files=ev['files'],taxonomy=O.tax_record(out,ctx.taxonomy))
 pv.update(got['provenance'])
 forward=O.forward_from_result(result,'VALID',None,'INERT',ctx.row_ids)
 stored,new=cache.put(key=key,theta=theta,classification='VALID',failure_class=None,source='WAVE',provenance=pv,forward=forward)
 assert new;checks.append('actual parent/wrapper cache put validates produced acceptance lineage')
 disk=cache.entries_dir/(key+'.json');before=disk.read_bytes()
 reopened=W.Cache();reopened.ctx=ctx;reopened.entries_dir=cache.entries_dir;reopened.open(create=False)
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
 append(**phase_args,kind='CONSUME',subject=key);publish_checkpoint()
 assert reopened.forward(key)==forward
 append(**phase_args,kind='FINAL_INVALIDATE',subject='');publish_checkpoint()
 from snapshot_cx1v001 import Refusal
 try:reopened.forward(key)
 except Refusal:checks.append('final invalidation refuses replay of the accepted seed')
 else:raise AssertionError('invalidation bypass')
 assert disk.read_bytes()==before;checks.append('invalidation preserves cached evidence bytes')
finally:
 fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
report={'status':'PASS','tested':checks,'scope':__doc__,'seams':['H55 synthetic science environments and evidence exporter','synthetic Context identity, policy, mapper and custody/inventory modules','synthetic VALID taxonomy; real parent/wrapper classifier','exclusive writer double instead of parent atomic unlink writer','unauthed fixture phase checkpoint resolver','synthetic observer authentication and scheduler boundary'],'untested':['full installed campaign engine integration','installed runtime/register/envelope entry','real root-supplied record installation; synthetic D021 record tested','root-authenticated phase publication and campaign freeze'],'fixture':F['ref'](fixture),'test':F['ref'](__file__),'acceptance':accpin,'output':str(case)}
print(put(case/'SEED_INTEGRATION_REPORT.json',report))
