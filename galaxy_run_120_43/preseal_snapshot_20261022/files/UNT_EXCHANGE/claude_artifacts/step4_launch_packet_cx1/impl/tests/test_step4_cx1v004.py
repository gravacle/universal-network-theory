"""Synthetic admission/call adapters and mocked process seam. No scientific launch."""
import copy,hashlib,importlib.util,json,os,sys
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;IMPL=HERE.parent
sp=importlib.util.spec_from_file_location('launcher',IMPL/'step4_launcher_cx1v005.py');L=importlib.util.module_from_spec(sp);sp.loader.exec_module(L);G=L.G
OUT=HERE/'SYNTH_V004';OUT.mkdir()
checks=[];seq=0
R5=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py')
MON=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py')
def put(name,data):
    p=OUT/name
    b=data.encode() if isinstance(data,str) else json.dumps(data,sort_keys=True,allow_nan=False).encode()
    with p.open('xb') as f:f.write(b)
    return G.pin(p)
def check(name,fn,expected=None):
    try:
        value=fn();ok=expected is None and value is not False;detail='returned '+repr(value)[:90]
    except Exception as e:ok=expected is not None and expected in str(e);detail=type(e).__name__+': '+str(e)
    checks.append({'name':name,'passed':ok,'detail':detail})

def build(mut=None,policy_empty=False):
    global seq
    seq+=1;tag=f'{seq:03d}'
    cb=put(tag+'caseblock.json',{'cases':{'C4T':{'tail':True,'drivers_allowed':[G.R5_SHA]}}})
    prereg=put(tag+'prereg.json',{'binding_inputs':{'case_block':cb}})
    compare=put(tag+'compare.py','SCHEMA_REPORT="UNT_KMAX_TAIL_COMPARISON_C2V007_SYNTH"\n')
    add=put(tag+'addendum.md','SYNTHETIC NOT SCIENTIFIC\n')
    report={'schema':'UNT_KMAX_TAIL_COMPARISON_C2V007_SYNTH','test_mode':False,'decision':{'tests_read':True,'outcome':'ADOPT_TAIL'},'prereg':prereg,'case_block':cb,'script_sha256':compare['sha256']}
    if mut and mut[0]=='report':report[mut[1]]=mut[2]
    verdict=put(tag+'verdict.json',report)
    seal=put(tag+'seal.json',{'sealed_by':G.AUTHORITY,'prereg':prereg,'compare':compare,'frozen_addendum':add,'driver':G.pin(R5)})
    v={'seal':seal,'verdict':verdict,'prereg':prereg,'compare':compare,'addendum':add,'case_block':cb}
    context=put(tag+'context.py','''class O: pass
class Context:
 def __init__(self,cfg): self.cfg=cfg
 def certificate_policy_gate(self):
  b=self.cfg.get('test_policy_pass',True);return {'ok':b,'reasons':[] if b else ['POLICY_REFUSED']}
 def certificate_check(self,spec,phase):
  b=self.cfg.get('test_certificate_pass',True);return {'ok':b,'blockers':[] if b else ['CERT_REFUSED'],'phase':phase,'point':spec['physical']}
 def sensitivity_gate(self,spec):
  b=spec['physical']['distance_Mpc'] in self.cfg.get('test_allowed_distances',[4.04]);return {'ok':b,'reasons':[] if b else ['WRONG_D'],'distance':spec['physical']['distance_Mpc']}
 def prelaunch_check(self,spec):return spec
def validate_block(block):return True
''')
    tpl=(compare['sha256'],prereg['sha256'],add['sha256'],report['schema'],verdict['sha256'])
    policy=put(tag+'policy.py','APPROVED_V007_SEALS='+repr(frozenset() if policy_empty else frozenset([tpl]))+'\ndef check_numerics(*a,**k):return {}, {"ok":True,"reasons":[],"synthetic_adapter":True}\n')
    adapter=put(tag+'synthetic_direct_adapter.py','DIRECT_CONTEXT_API="UNT_STEP4_DIRECT_PREFLIGHT_CX1V001"\ndef build(C,config,**kw):return C.Context(config)\n')
    cert_source=put(tag+'cert_source.py','SYNTHETIC_CERTIFICATE_STUB=True\n')
    registry=put(tag+'registry.json',{'synthetic':True,'points':{'p':'test'}})
    cr=put(tag+'policy_review.json',{'synthetic':True,'verdict':'PASS'})
    config={'numerics':{'verdict_artifact':verdict,'sealed_prereg':prereg,'compare':compare,'block':{'route_a':{'column_workers':8}}},'tail_readiness':{'certificate_registry':registry,'certificate_policy_review':cr,'custody_deriver':cert_source,'state_enumerator':cert_source,'approved_certificate_producers':[cert_source]}}
    if mut and mut[0]=='config':config[mut[1]]=mut[2]
    configref=put(tag+'C1.json',config)
    spec={'galaxy':'DDO154','admit':{},'physical':{'distance_Mpc':4.04},'numerics':{'uv_tail':{'enabled':True}}}
    if mut and mut[0]=='spec':spec[mut[1]]=mut[2]
    sr=put(tag+'spec.json',spec)
    call={'case':'SYNTH','family':'TAIL_REANCHOR','tail_on':True,'driver_role':'PRODUCTION_R5','driver':G.pin(R5),'spec':sr,'spec_status':'ROOT_FINAL','pending':[],'distance_Mpc':spec['physical']['distance_Mpc'],'outdir':str(OUT/(tag+'run')),'receipt':str(OUT/(tag+'receipt.json')),'monitor_log':str(OUT/(tag+'monitor.log')),'wall_cap_s':60,'rss_cap_bytes':1024,'output_cap_bytes':2048}
    rule={'max_active':3,'minimum_free_percent':25,'poll_seconds':60,'source':'/usr/bin/memory_pressure','ramp':'previous_first_completed_route_a_iteration','first_case_memory_exemption':False}
    plan={'schema':'UNT_STEP4_LAUNCH_PLAN_CX1V001','binding_status':'ROOT_BOUND','batch':'HEADLINE','launcher':G.pin(L.__file__),'guard':G.pin(G.__file__),'monitor':G.pin(MON),'launcher_log':str(OUT/(tag+'launcher.log')),'route_a_admission':rule,'calls':[call]}
    sources={r['path']:r['sha256'] for r in (plan['launcher'],plan['guard'],plan['monitor'],G.pin(R5),context,policy,cert_source,compare,adapter)}
    review=put(tag+'source_review.json',{'schema':'UNT_STEP4_SOURCE_REVIEW_CX1V001','status':'TESTED','verdict':'PASS','reviewer':'SYNTHETIC_INDEPENDENT_REVIEWER','blocking_findings':[],'approved_sources':sources})
    cfg={'schema':'UNT_STEP4_ADMISSION_CX1V001','status':'ROOT_AUTHORIZED','authority':G.AUTHORITY,'sources':sources,'source_review':review,'v007':v,'config':configref,'context_module':context,'direct_context':adapter,'adoption_policy':policy,'route_a_admission':rule,'core_priority':{'normal_qos_required':True,'step2_route_a_inactive':True,'campaign_inactive':True,'background_noncritical_lanes':True,'sleep_assertion_required':True},'case_order':['SYNTH'],'caps':{'SYNTH':{k:call[k] for k in ('wall_cap_s','rss_cap_bytes','output_cap_bytes')}}}
    # A nominal expected record is made with the native synthetic adapters. Negative
    # variants below deliberately retain a nominal record and must refuse replay.
    try:pre=G.native_preflight(cfg,call)
    except Exception as e:pre={'synthetic_expected_refusal':str(e)}
    call['prelaunch']=put(tag+'PRELAUNCH.json',pre)
    cfg['calls']={'SYNTH':{k:call[k] for k in ('spec','driver','prelaunch')}}
    if mut and mut[0]=='call':call[mut[1]]=mut[2]
    if mut and mut[0]=='plan':plan[mut[1]]=mut[2]
    pr=put(tag+'plan.json',plan);cfg['plan']=pr
    if mut and mut[0]=='cfg':cfg[mut[1]]=mut[2]
    ar=put(tag+'admission.json',cfg)
    return pr,ar,plan,cfg

def validate_fixture(f):return G.validate(f[0],L.__file__,config_ref=f[1])[0]['binding_status']=='ROOT_BOUND'
nom=build();check('nominal_full_guard_native_synthetic_adapters',lambda:validate_fixture(nom))
for name,mut,reason in [
 ('forged_test_mode',('report','test_mode',True),'SEALED_ADOPT_TAIL_REQUIRED'),
 ('forged_decision',('report','decision',{'tests_read':True,'outcome':'REJECT'}),'SEALED_ADOPT_TAIL_REQUIRED'),
 ('tests_not_read',('report','decision',{'tests_read':False,'outcome':'ADOPT_TAIL'}),'SEALED_ADOPT_TAIL_REQUIRED'),
 ('certificate_policy_false',('config','test_policy_pass',False),'NATIVE_GATE_REFUSED'),
 ('certificate_prelaunch_false',('config','test_certificate_pass',False),'NATIVE_GATE_REFUSED'),
 ('wrong_distance_sensitivity',('spec','physical',{'distance_Mpc':3.8}),'NATIVE_GATE_REFUSED'),
 ('null_certificate_registry',('config','tail_readiness',{'certificate_registry':None}),'PIN_REQUIRED'),
 ('unbound_plan',('plan','binding_status','UNBOUND'),'UNBOUND_PLAN_REFUSED'),
 ('pending_spec',('call','pending',['MISSING']),'PENDING_SPEC_REFUSED'),
 ('zero_wall',('call','wall_cap_s',0),'POSITIVE_INTEGER_CAPS_REQUIRED'),
 ('bool_wall',('call','wall_cap_s',True),'POSITIVE_INTEGER_CAPS_REQUIRED'),
 ('unapproved_cap',('call','rss_cap_bytes',4096),'ROOT_CAPS_BINDING'),
 ('missing_core_priority',('cfg','core_priority',{}),'CORE_PRIORITY_ATTESTATION_REQUIRED'),
 ('wrong_root_authority',('cfg','authority',{'identity':'Codex1'}),'ROOT_STEP4_AUTHORITY_REQUIRED'),
 ('missing_call_allowlist',('cfg','calls',{}),'ROOT_CALL_BINDING'),
]:
    f=build(mut);check(name,lambda f=f:validate_fixture(f),reason)
f=build(policy_empty=True);check('unreviewed_seal_tuple',lambda:validate_fixture(f),'REVIEWED_SEAL_TUPLE_PENDING')
with patch.dict(os.environ,{'UNT_STEP4_ADMISSION_PATH':'','UNT_STEP4_ADMISSION_SHA256':''}):check('pre_adoption_missing_admission',lambda:G.validate(nom[0],L.__file__),'PUBLISHED_STEP4_ADMISSION_PENDING')
bad=copy.deepcopy(nom[1]);bad['sha256']='0'*64;check('forged_env_hash',lambda:G.validate(nom[0],L.__file__,config_ref=bad),'PIN_BYTES_CHANGED')
check('NaN_json_refused',lambda:G.decode('{"x": NaN}'),'NONFINITE_JSON')
check('overflow_json_refused',lambda:G.decode('{"x":1e999}'),'NONFINITE_JSON')
check('duplicate_json_keys_refused',lambda:G.decode('{"x":1,"x":2}'),'DUPLICATE_JSON_KEY')
# Literal guard must reject protected names before attempting any file read.
for name in ('UVT_BAD','KMAX_A2F10_C5H_RUN_V001','NGC3198_observed.csv'):
    check('protected_'+name,lambda name=name:G.safe_path(str(OUT/name)),'PROTECTED_PATH_REFUSED')
check('authority_metadata_filename_allowed',lambda:G.safe_path(str(OUT/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026_10_17_V005_ADDENDUM.md')))
# Ramp and cap boundaries; the first item gets no memory exemption.
for name,kw,want in [
 ('first_low_memory',dict(active_route_a=0,free=24,previous_iteration=False,first=True,max_active=3),False),
 ('first_unknown_memory',dict(active_route_a=0,free=None,previous_iteration=False,first=True,max_active=3),False),
 ('first_good',dict(active_route_a=0,free=25,previous_iteration=False,first=True,max_active=3),True),
 ('ramp_wait',dict(active_route_a=1,free=80,previous_iteration=False,first=False,max_active=3),False),
 ('ramp_ready',dict(active_route_a=2,free=25,previous_iteration=True,first=False,max_active=3),True),
 ('cap_full',dict(active_route_a=3,free=80,previous_iteration=True,first=False,max_active=3),False)]:
    check(name,lambda kw=kw,want=want:L.decision(**kw) is want)
for name,content,want in [('partial','{"stage":"iteration_completed","iteration":0}',False),('complete','{"stage":"iteration_completed","iteration":0}\n',True),('bool_iteration','{"stage":"iteration_completed","iteration":true}\n',False)]:
    ref=put(name+'.jsonl',content);check(name,lambda ref=ref,want=want:L.first_iteration(ref['path']) is want)
ref=put('malformed.jsonl','{bad}\n');check('malformed_progress',lambda:L.first_iteration(ref['path']),'Expecting property name')
# The fence blocks processes and mutations even when invoked by preflight adapters.
for name,fn,reason in [('process',lambda:L.subprocess.Popen(['/usr/bin/true']),'PREFLIGHT_PROCESS_OR_NETWORK_REFUSED'),('write',lambda:(OUT/'forbidden-write').open('x'),'PREFLIGHT_WRITE_REFUSED')]:
    def probe(fn=fn):
        with G.fence():return fn()
    check('fence_'+name,probe,reason)
# Main->worker seam keeps the existing launcher log but refuses existing call paths.
f=build();plan=f[2]
with Path(plan['launcher_log']).open('xb'):pass
class Proc:
    pid=12345
    def __init__(self,kind):self.kind=kind;self.n=0
    def poll(self):
        if self.kind=='assertion':return None
        self.n+=1;return 0
spawns=[]
def spawn(argv,**kw):
    spawns.append(argv)
    if argv[0]=='/usr/bin/caffeinate':return Proc('assertion')
    return Proc('monitor')
# Supply completed synthetic receipt/progress through readers after mock start.
with patch.dict(os.environ,{'UNT_STEP4_ADMISSION_PATH':f[1]['path'],'UNT_STEP4_ADMISSION_SHA256':f[1]['sha256']}),patch.object(L,'runtime_settings',lambda:None),patch.object(L,'acquire_lock',lambda:os.open('/dev/null',os.O_RDONLY)),patch.object(L.subprocess,'Popen',spawn),patch.object(L,'memory_free',lambda:80),patch.object(L,'route_a_finished',lambda p:True),patch.object(L,'first_iteration',lambda p:True),patch.object(L.time,'sleep',lambda n:None):
    oldraw=G.raw
    def read(p):return b'{"status":"FINISHED"}' if str(p)==plan['calls'][0]['receipt'] else oldraw(p)
    with patch.object(G,'raw',read):check('worker_existing_own_log_positive',lambda:L.worker(f[0])==0)
check('worker_spawn_order_assertion_before_monitor',lambda:len(spawns)==2 and spawns[0][0]=='/usr/bin/caffeinate' and spawns[1][:2]==['/usr/bin/taskpolicy','-B'])
# Save source unchanged checks and exact tested scope.
result={'schema':'UNT_STEP4_SYNTHETIC_TESTS_CX1V001','label':'TESTED synthetic admission and mocked process seam; actual scientific launch/native production preflight UNTESTED','checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'scientific_processes_created':0,'sources':{p.name:G.pin(p) for p in (IMPL/'step4_guard_cx1v005.py',IMPL/'step4_launcher_cx1v005.py',IMPL/'step4_bind_cx1v004.py',Path(__file__))}}
with (OUT/'RESULTS.json').open('x') as o:json.dump(result,o,indent=2,allow_nan=False)
print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x for x in checks if not x['passed']]}))
raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
