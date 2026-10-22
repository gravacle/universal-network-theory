"""Joined natural request and root observation on inert plan, register and START."""
from pathlib import Path
import tempfile,json,hashlib,copy,types,fcntl,os
from natural_registered_observation_cx1v003 import observe
import natural_registered_observation_cx1v003 as observer
from invocation_plan_binding_cx1v002 import PYTHON
from terminal_association_cx1v001 import SCHEMA
from inflight_policy_cx1v001 import decide
from envelope_observation_adapter_cx1v002 import build
from snapshot_cx1v001 import Refusal
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='natural_terminal_chain_',dir=b/'inert_fixtures'));old=b/'inert_fixtures/observation_entry_zn2194gv'
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,obj):
 p=c/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True)
 return pin(p)
root=json.loads((old/'inert_root_binding.json').read_bytes());reg=json.loads(Path(root['register']['path']).read_bytes());spec={'inert':True};sp=write('selected_spec.json',spec);raw=Path(sp['path']).read_bytes();key=reg['entries'][0]['key'];reg['entries'][0]['spec']=sp
root['schema']='CX1_IMPORTER_ROOT_BINDING_V002'
monitor=pin(b.parent/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py');launcher=pin(b.parent/'s1_successors_c2/step4_launcher_c2v015.py')
root['runtime']['monitor']=monitor;root['runtime']['output_root']=str(c)
# Only hash the fixed executable bytes; do not run it or capture actual packages/environment.
identity=dict(realpath=str(Path(PYTHON).resolve(strict=True)),sha256=hashlib.sha256(Path(PYTHON).read_bytes()).hexdigest())
record=json.loads(Path(reg['entries'][0]['runtime_capture']['path']).read_bytes());record['interpreter']=identity;record['monitor']=dict(realpath=monitor['path'],sha256=monitor['sha256'])
direct=write('synthetic_direct_capture.json',record);campaign=write('synthetic_campaign_capture.json',record);root['runtime']['campaign_capture']=campaign
for e in reg['entries']:
 e['runtime_capture']=direct;e['launcher']=launcher;e['call_root']=str(c/Path(e['call_root']).name)
rp=write('register.json',reg);root['register']=rp
launch=json.loads(Path(root['runtime']['direct_launch']['path']).read_bytes());launch.update(register=rp,runtime_capture=direct,interpreter=identity);root['runtime']['direct_launch']=write('launch.json',launch)
binding=json.loads(Path(root['binding']['path']).read_bytes());binding.update(register=rp,campaign_capture=campaign,interpreter=identity);root['binding']=write('stageb.json',binding)
caps=dict(wall_cap_s=11,rss_cap_bytes=22,output_cap_bytes=33,poll_s=2.0);selected=reg['entries'][0];d=Path(selected['call_root'])
call=dict(point_key=key,row=selected['row'],spec=sp,driver=root['runtime']['driver'],spec_status='ROOT_FINAL',pending=[],outdir=str(d/'out'),receipt=str(d/'RECEIPT.json'),monitor_log=str(d/'monitor.log'),**{k:v for k,v in caps.items() if k!='poll_s'})
root['direct_plan']=write('synthetic_direct_plan.json',dict(schema='UNT_STEP4_LAUNCH_PLAN_CX1V001',binding_status='ROOT_BOUND',launcher=launcher,monitor=monitor,calls=[call]))
required=[rp,root['runtime']['driver'],root['runtime']['monitor'],root['policy'],root['entry']]
for e in reg['entries']:required.extend(e[k] for k in ('spec','launcher','guard','binder','dbp','runtime_capture'))
required=list({(p['path'],p['sha256']):p for p in required}.values());parent=b.parent/'pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py';m,_=build(parent.read_bytes(),str(parent))
def signed(name,obj):
 obj=copy.deepcopy(obj);obj.pop('body_sha256',None);obj['body_sha256']=m.sha_b(m.canon(obj).encode('ascii'));return write(name,obj),obj
pp,ps=signed('pinset.json',dict(schema=m.SCHEMA_PINSET,phase='L2_DIRECT',pins=required,excluded=[],unresolved_pins=[]));start=m.observe(ps,pp['sha256'],pp['path']);start['label']='start';ss,_=signed('synthetic_start.json',start);root['envelope']=dict(tool=pin(parent),start=ss,pinset=pp);rb=write('root.json',root)
work=c/'work';wd=work/'waves/wave_0001';wd.mkdir(parents=True);theta={'inert':1};plan=dict(wave=1,**root['context'],calls=[dict(call_index=0,key=key,theta=theta,spec=spec,spec_sha256=sp['sha256'])])
with (wd/'WAVE_PLAN.json').open('x') as f:json.dump(plan,f)
fd=os.open(work/'ORCHESTRATOR.lock',os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);lock=types.SimpleNamespace(held=True,_fd=fd,path=work/'ORCHESTRATOR.lock')
ctx=types.SimpleNamespace(work_dir=work,**root['context'],driver=root['runtime']['driver'],cfg={'monitor':root['runtime']['monitor']},mapper=types.SimpleNamespace(build=lambda theta:dict(key=key,spec=spec,sha256=sp['sha256'],raw=raw)))
a=dict(ctx=ctx,lock=lock,wave=1,call_index=0,plan_pin=pin(wd/'WAVE_PLAN.json'),theta_key=lambda theta:key,root_binding_pin=rb,expected_policy=root['policy'],expected_entry=root['entry']);passed=[]
try:
 got=observe(**a);assert got['registered'] and decide(**got)=='HOLD_UNKNOWN_EXTERNAL_STATE';passed.append('whole helper chain: missing receipt holds')
 d.mkdir();pins=dict(spec=sp,driver=ctx.driver,monitor=monitor,python=PYTHON);cmd=[PYTHON,'-I','-B',ctx.driver['path'],'run','--spec',sp['path'],'--outdir',str(d/'out')]
 side=dict(schema=SCHEMA+'_LAUNCH',utc='2026-10-21T12:30:00Z',command=cmd,pins=pins,caps=caps,child_pid=123,retries_allowed=0)
 receipt=dict(schema=SCHEMA,utc_start=side['utc'],utc_end='2026-10-21T12:31:00Z',command=cmd,pins=pins,caps=caps,child_pid=123,retries=0,status='FINISHED',exit_code=0,stop_reason=None,result=None)
 receipt['receipt_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 write(str(d.relative_to(c))+'/RECEIPT.json',receipt);write(str(d.relative_to(c))+'/RECEIPT.json.launch.json',side)
 got=observe(**a);assert decide(**got)=='HOLD_UNCLASSIFIED_OUTCOME';passed.append('whole helper chain: FINISHED remains unclassified')
 # Inject fresh-boundary refusal without modifying any existing fixture file.
 original_snapshot=observer.Snapshot
 for label,target in [('root binding',rb['path']),('direct plan',root['direct_plan']['path'])]:
  created=[]
  def snapshot_factory():
   obj=original_snapshot();created.append(obj)
   if len(created)==2:
    original_pin=obj.pin
    def checked_pin(p):
     if p['path']==target:raise Refusal('INJECTED_FRESH_PIN_CHANGE')
     return original_pin(p)
    obj.pin=checked_pin
   return obj
  observer.Snapshot=snapshot_factory
  try:
   try:observe(**a)
   except Refusal as exc:
    assert str(exc)=='INJECTED_FRESH_PIN_CHANGE';passed.append(label+' fresh-boundary refusal propagates')
   else:raise AssertionError(label)
  finally:observer.Snapshot=original_snapshot
 for name,changes in [('unrequested',dict(call_index=1)),('foreign code',{})]:
  if name=='foreign code':ctx.driver=dict(ctx.driver,sha256='0'*64)
  try:observe(**dict(a,**changes))
  except Refusal:passed.append(name+' refuses')
  else:raise AssertionError(name)
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Real producer records, package capture and root adoption; all records synthetic; mapper/theta_key remain inert doubles','Full executor installation','Concurrent plan mutation injection','Consumer freeze'],pins=[pin(p) for p in [Path(__file__),b/'natural_registered_observation_cx1v003.py',b/'natural_request_cx1v001.py']])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'TEST_REPORT.json')
