"""Additional immutable-synthetic probes; imports only builder sources."""
import copy,importlib.util,json,os
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;I=HERE.parent
sp=importlib.util.spec_from_file_location('Lextra',I/'step4_launcher_cx1v005.py');L=importlib.util.module_from_spec(sp);sp.loader.exec_module(L);G=L.G
sp=importlib.util.spec_from_file_location('Bextra',I/'step4_bind_cx1v004.py');B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
BASE=HERE/'SYNTH_V004';OUT=HERE/'EXTRA_V002';OUT.mkdir()
P=G.decode((BASE/'001plan.json').read_bytes());C=G.decode((BASE/'001admission.json').read_bytes());checks=[]
def put(name,obj):
 p=OUT/name;b=obj.encode() if isinstance(obj,str) else json.dumps(obj,sort_keys=True,allow_nan=False).encode()
 with p.open('xb') as f:f.write(b)
 return G.pin(p)
def run(name,fn,err=None):
 try:v=fn();ok=err is None and v is not False;d=repr(v)[:120]
 except Exception as e:ok=err is not None and err in str(e);d=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':d})
def altered(name,edit):
 p,c=copy.deepcopy(P),copy.deepcopy(C);edit(p,c)
 pr=put(name+'plan.json',p);c['plan']=pr;cr=put(name+'admission.json',c)
 return pr,cr,p,c
def good(f):return G.validate(f[0],L.__file__,config_ref=f[1])[0]['binding_status']=='ROOT_BOUND'
for name,edit,why in [
 ('output_alias',lambda p,c:p['calls'][0].update(receipt=p['calls'][0]['outdir']+'/../'+Path(p['calls'][0]['outdir']).name),'ALIASED_OUTPUTS'),
 ('nested_output',lambda p,c:p['calls'][0].update(monitor_log=p['calls'][0]['outdir']+'/nested.log'),'NESTED_OUTPUTS'),
 ('wrong_guard',lambda p,c:p.update(guard=p['launcher']),'LAUNCHER_GUARD_IDENTITY'),
 ('first_memory_bypass',lambda p,c:(p['route_a_admission'].update(first_case_memory_exemption=True),c['route_a_admission'].update(first_case_memory_exemption=True)),'FIRST_MEMORY_BYPASS_REFUSED'),
 ('too_many_tokens',lambda p,c:(p['route_a_admission'].update(max_active=7),c['route_a_admission'].update(max_active=7)),'ROUTE_A_CAP_REQUIRED'),
 ('missing_PRELAUNCH',lambda p,c:(p['calls'][0].update(prelaunch=None),c['calls']['SYNTH'].update(prelaunch=None)),'PIN_REQUIRED'),
 ('wrong_role_ref',lambda p,c:p['calls'][0].update(driver={'path':C['context_module']['path'],'sha256':G.REF_SHA},driver_role='PRODUCTION_R5'),'REFERENCE_DRIVER_SCOPE'),
]:
 f=altered(name,edit);run(name,lambda f=f:good(f),why)
# A new immutable file with changed bytes, against the original published source hash.
changed=put('changed_source.py','SOURCE_CHANGED=True\n')
def edit_source(p,c):
 c['sources'][changed['path']]=C['context_module']['sha256']
f=altered('source_bytes_changed',edit_source);run('source_bytes_changed',lambda:good(f),'PIN_BYTES_CHANGED')
# Signed prelaunch string alone is insufficient; native report must match byte-for-byte.
false_pre=put('false_PRELAUNCH.json',{'verdict':'PASS','ok':True})
def editpre(p,c):p['calls'][0]['prelaunch']=false_pre;c['calls']['SYNTH']['prelaunch']=false_pre
f=altered('bare_pass_PRELAUNCH',editpre);run('bare_pass_PRELAUNCH',lambda:good(f),'PRELAUNCH_REPLAY_MISMATCH')
# DIII probes use real driver byte identities but a narrowly mocked pure normalize
# function: no import of scientific solver or run trees.
REF=G.pin('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py')
class FakeDriver:
 @staticmethod
 def normalize_spec(s):return s
oldload=G.load
def fake_driver_load(ref,cfg,name):return FakeDriver if name=='_step4_diii_driver' else oldload(ref,cfg,name)
for label,driver,role,uv in [('r5',P['calls'][0]['driver'],'PRODUCTION_R5',None),('ref',REF,'REFERENCE_V009GEO',None),('uv_false',REF,'REFERENCE_V009GEO',{'enabled':False}),('uv_zero',REF,'REFERENCE_V009GEO',{'enabled':0})]:
 p,c=copy.deepcopy(P),copy.deepcopy(C);call=p['calls'][0];call.update(family='DECIDING_III',tail_on=False,driver=driver,driver_role=role,distance_Mpc=3.8);p['batch']='DIII'
 spec={'galaxy':'DDO154','admit':{},'physical':{'distance_Mpc':3.8},'numerics':{}}
 if uv is not None:spec['numerics']['uv_tail']=uv
 call['spec']=put(label+'tailoff_spec.json',spec)
 policy={'schema':'UNT_STEP4_DIII_POLICY_CX1V001','authority':G.AUTHORITY,'post_adoption_only':True,'verdict':'PASS','status':'TESTED','cases':{'SYNTH':{'spec':call['spec'],'driver':driver}}}
 c['tail_off_policy']=put(label+'tailoff_policy.json',policy);c['sources'][driver['path']]=driver['sha256']
 sr=G.doc(c['source_review']);sr['approved_sources']=c['sources'];c['source_review']=put(label+'source_review.json',sr)
 with patch.object(G,'load',fake_driver_load):
  try:pre=G.native_preflight(c,call)
  except Exception as e:pre={'expected_refusal':str(e)}
  call['prelaunch']=put(label+'PRELAUNCH.json',pre);c['calls']['SYNTH']={k:call[k] for k in ('spec','driver','prelaunch')}
  pr=put(label+'plan.json',p);c['plan']=pr;cr=put(label+'admission.json',c);f=(pr,cr,p,c)
  run('DIII_'+label,lambda f=f:good(f),None if uv is None else 'ONLY_REGISTERED_DIII_TAIL_OFF_OMISSION_ALLOWED')
# The exclusive binder verifies scientific/native synthetic gates before any write.
candidate=copy.deepcopy(C);candidate['plan']=None;ref=put('candidate.json',candidate)
a=OUT/'BOUND_PLAN.json';b=OUT/'BOUND_ADMISSION.json';d=OUT/'ROOT_COMMAND.sh'
run('binder_nominal',lambda:B.bind(BASE/'001plan.json',ref['path'],a,b,d)['plan']==G.pin(a))
run('binder_outputs_immutable',lambda:B.bind(BASE/'001plan.json',ref['path'],a,b,d),'EXCLUSIVE_PACKET_OUTPUT_REQUIRED')
run('bound_admission_revalidates',lambda:G.validate(G.pin(a),L.__file__,config_ref=G.pin(b))[0]['binding_status']=='ROOT_BOUND')
run('binder_does_not_export_authority',lambda:'export UNT_STEP4' not in d.read_text() and 'UNT_STEP4_ADMISSION_SHA256=' not in d.read_text())
# Real missing-admission CLI path cannot reach subprocess creation.
with patch.dict(os.environ,{'UNT_STEP4_ADMISSION_PATH':'','UNT_STEP4_ADMISSION_SHA256':''}),patch.object(L.subprocess,'Popen',side_effect=AssertionError('UNEXPECTED_PROCESS')) as proc,patch.object(L.sys,'argv',['launcher',str(BASE/'001plan.json'),'--execute-root-only']):
 run('main_before_adoption_no_process',L.main,'PUBLISHED_STEP4_ADMISSION_PENDING')
 run('main_missing_admission_zero_Popen',lambda:proc.call_count==0)
# Single machine lock tested only on owned synthetic inode; no production lockfile.
with patch.object(L,'LOCK',OUT/'LOCK'):
 fd=L.acquire_lock()
 try:run('concurrent_batch_lock_refused',L.acquire_lock,'ANOTHER_STEP4_BATCH_ACTIVE')
 finally:os.close(fd)
 fd=L.acquire_lock();os.close(fd);run('completed_batch_lock_reusable_without_deletion',lambda:(OUT/'LOCK').is_file())
result={'label':'TESTED synthetic and mocked-only; no scientific launch; production native preflight UNTESTED','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'scientific_processes_created':0,'sources':{p.name:G.pin(p) for p in (I/'step4_guard_cx1v005.py',I/'step4_launcher_cx1v005.py',I/'step4_bind_cx1v004.py',Path(__file__))}}
with (OUT/'RESULTS.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x for x in checks if not x['passed']]}))
raise SystemExit(0 if result['passed']==result['total'] else 1)
