import copy,fcntl,hashlib,json,os,tempfile,types
from pathlib import Path
from planned_binding_cx1v001 import bind_planned
from snapshot_cx1v001 import Refusal
b=Path(tempfile.mkdtemp(prefix='binding_',dir=Path(__file__).parent/'inert_fixtures')).resolve()
ctx={'config_sha256':'a'*64,'cache_id':'cache','gate_digest':'b'*64};cases=[]
def write(p,obj):
 raw=json.dumps(obj).encode();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()},raw
for mode in ['pending_exact','no_match','unheld','before_plan','wrong_theta','wrong_mapper','duplicate','already_ingested','local_output']:
 d=b/mode;work=d/'campaign';work.mkdir(parents=True);lp=work/'ORCHESTRATOR.lock';fd=os.open(lp,os.O_RDWR|os.O_CREAT|os.O_EXCL,0o600);fcntl.flock(fd,fcntl.LOCK_EX)
 lock=types.SimpleNamespace(held=mode!='unheld',_fd=fd,path=lp)
 try:
  sp,raw=write(d/'spec.json',{'inert':True});drv={'path':str(d/'driver'),'sha256':'c'*64}
  call={'call_index':0,'theta':[1],'key':'key','spec':{'inert':True},'spec_sha256':sp['sha256']}
  wd=work/'waves/wave_0001';pp,_=write(wd/'WAVE_PLAN.json',{'wave':1,**ctx,'calls':[call]})
  out=work/'output' if mode=='local_output' else d/'direct_output'
  dp,_=write(d/'direct_plan.json',{'calls':[{'case':'seed','spec':sp,'driver':drv,'outdir':str(out),'receipt':str(d/'receipt'),'monitor_log':str(d/'log')}],'launcher_log':str(d/'launchlog')})
  e={'theta_key':'key','spec':sp,'driver':drv,'direct_plan':dp,'case':'seed','runtime_environment':drv,'envelope_phase':'INERT'}
  rp,_=write(d/'register.json',{'schema':'CX1_SPECULATIVE_REGISTER_V001','context':ctx,'entries':[] if mode=='no_match' else [e]})
  if mode=='before_plan':pp={'path':str(work/'waves/wave_0002/WAVE_PLAN.json'),'sha256':pp['sha256']}
  if mode=='already_ingested':write(wd/'WAVE_RESULT.json',{})
  mapped={'key':'key','spec':call['spec'],'sha256':sp['sha256'],'raw':raw if mode!='wrong_mapper' else b'{}'}
  try:
   got=bind_planned(lock=lock,work_dir=work,wave=2 if mode=='before_plan' else 1,call_index=0,context=ctx,plan_pin=pp,register_pin=rp,mapped=mapped,theta_key=lambda t:'wrong' if mode=='wrong_theta' else 'key',driver_pin=drv,cached_keys={'key'} if mode=='duplicate' else set())
   assert mode in ('pending_exact','no_match'),mode
   assert got['registered']==(mode=='pending_exact')
   assert not out.exists()
  except Refusal:
   assert mode not in ('pending_exact','no_match'),mode
  cases.append(mode)
 finally:
  fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r={'status':'PASS','blocking_count':0,'scope':'Locked planned binding prerequisite with inert mapper/context and real fixture flock','tested':cases,'untested':['Parent orchestration integration','Certificates/runtime/acceptance/status','Root registration authentication','Whole-engine replay']}
p=b/'TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)
