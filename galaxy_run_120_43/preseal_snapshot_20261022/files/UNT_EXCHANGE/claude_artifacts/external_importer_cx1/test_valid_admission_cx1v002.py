"""Combined admission prototype with explicitly synthetic context/taxonomy.
The real wrapper certificate method, guard and monitor remain in the fixture.
"""
import copy,fcntl,os,types,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
helper=root/'test_wrapper_certificate_snapshot_cx1v001.py'
text=helper.read_text().split("baseline=W.certificate_check",1)[0]
text=text.replace("driver_sha='a'*64", "driver_pin=put(case/'inert_driver.json',{'inert_driver':True});driver_sha=driver_pin['sha256']")
text=text.replace("'driver':{'sha256':driver_sha}","'driver':driver_pin")
text=text.replace("'status':'FINISHED','driver_status':'COMPLETED','pins'","'status':'FINISHED','driver_status':'COMPLETED','exit_code':0,'stop_reason':None,'pins'")
exec(compile(text,str(helper),'exec'),globals())
import valid_admission_cx1v001 as V
from custody_guard_cx1v002 import HANDOFF
from snapshot_cx1v001 import Refusal
work=case/'WORK';work.mkdir();wd=work/'waves/wave_0001';wd.mkdir(parents=True)
theta={'x':1.0};key=G.digest(theta)
plan_call={'call_index':0,'key':key,'theta':theta,'spec':spec,'spec_sha256':sp['sha256']}
plan={'wave':1,'config_sha256':'c'*64,'cache_id':'d'*64,'gate_digest':'e'*64,'calls':[plan_call]}
put(wd/'WAVE_PLAN.json',plan)
passdir=call/'ACCEPTANCE_TAILSTATES_C2V002_A001';passdir.mkdir()
acceptance={'schema':'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001','handoff':HANDOFF,'call_dir':str(call),
 'tailstate_dir':str(passdir),'reading':'ACCEPTED','outputs_are_evidence':True,'guard':{'ok':True},
 'step4_stop_for_root_ruling':False,'result':rp,'bundle':bound}
accpin=put(case/'acceptance.json',acceptance)
receipt_path=call/'RECEIPT.json'
candidate={'call_index':0,'call_dir':str(call),'key':key,'theta':theta,'spec':sp,
 'receipt':{'path':str(receipt_path),'sha256':hashlib.sha256(receipt_path.read_bytes()).hexdigest()},'acceptance':accpin,'bundle':bound}
ctx.work_dir=work;ctx.config_sha256=plan['config_sha256'];ctx.cache_id=plan['cache_id'];ctx.gate_digest=plan['gate_digest']
ctx.driver=driver_pin;ctx.cfg['monitor']={'path':str(monpath),'sha256':hashlib.sha256(monraw).hexdigest()}
mapped={'key':key,'spec':spec,'raw':(call/'spec.json').read_bytes(),'sha256':sp['sha256']}
ctx.mapper=types.SimpleNamespace(build=lambda theta:mapped)
ctx.prelaunch_check=lambda spec:None # declared: no full policy/context gates in this fixture

def classify(c,rec):
 cert=W.certificate_check(ctx,c['spec'],'acceptance',result=result,call_dir=rec['call_dir'])
 if not cert['ok']:return 'INFRA','CERTIFICATE',None,{'tail_certificates':cert}
 return 'VALID',None,{'valid':True,'speeds_km_s':{}},{'call_dir':str(call),'result_path':rp['path'],'result_sha256':rp['sha256'],'tail_certificates':cert}
orch=types.SimpleNamespace(ctx=ctx,check_identity_now=lambda:[],_external_parent_theta_key=G.digest,
 cache=types.SimpleNamespace(entries={}),executor=types.SimpleNamespace(classify=classify))
lockpath=work/'ORCHESTRATOR.lock';fd=os.open(lockpath,os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600)
fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
lock=types.SimpleNamespace(held=True,_fd=fd,path=lockpath)
mods=[W,O,M,G,monitor]
passed=[]
try:
 got=V.validate_valid(orch,lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate)
 assert got['classification']=='VALID' and got['provenance']['execution_origin']=='DIRECT_EXTERNAL'
 assert got['provenance']['call_dir']==str(call)
 assert not (wd/'campaign').exists() and not (work/'cache').exists()
 passed.append('combined valid prerequisites and real certificate checks; no cache or wave-call write')
 def refuse(name,**kw):
  args=dict(lock=lock,chain_modules=mods,wave_dir=wd,plan=plan,candidate=candidate);args.update(kw)
  try:V.validate_valid(orch,**args)
  except Refusal:passed.append(name)
  else:raise AssertionError(name)
 lock.held=False;refuse('unheld lock');lock.held=True
 refuse('unrequested index',candidate=dict(candidate,call_index=1))
 refuse('wrong theta',candidate=dict(candidate,theta={'x':2.0}))
 refuse('changed supplied plan',plan=dict(plan,cache_id='f'*64))
 orch.cache.entries[key]={};refuse('duplicate cached key');orch.cache.entries.clear()
 badacc=put(case/'failed_acceptance.json',dict(acceptance,reading='NON_LAPSE_TAIL_MATERIAL'))
 refuse('negative acceptance not mapped to invalid',candidate=dict(candidate,acceptance=badacc))
finally:
 fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
report={'status':'PASS','blocking_count':0,'scope':'Combined validation prototype with synthetic context and classifier; no production entry',
 'tested':passed,'substitutions':['fixture identity/policy/custody/enumerator from wrapper test','prelaunch_check no-op','check_identity_now empty','synthetic theta hash','classifier uses real certificate_check but synthetic VALID forward/taxonomy','manually held fixture flock'],
 'untested':['production Context/mapper/taxonomy','parent run lock integration','cache write/revalidation','whole engine','F6 admission'],
 'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [root/'valid_admission_cx1v001.py',root/'test_wrapper_certificate_snapshot_cx1v001.py',Path(__file__)]]}
with (case/'ADMISSION_TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'ADMISSION_TEST_REPORT.json')
