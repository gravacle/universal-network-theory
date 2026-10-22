"""Joined natural request and root observation on inert plan, register and START."""
from pathlib import Path
import tempfile,json,hashlib,copy,types,fcntl,os
from natural_registered_observation_cx1v001 import observe
from inflight_policy_cx1v001 import decide
from envelope_observation_adapter_cx1v002 import build
from snapshot_cx1v001 import Refusal
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='natural_observation_',dir=b/'inert_fixtures'));old=b/'inert_fixtures/observation_entry_zn2194gv'
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,obj):
 p=c/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True)
 return pin(p)
root=json.loads((old/'inert_root_binding.json').read_bytes());reg=json.loads(Path(root['register']['path']).read_bytes());spec={'inert':True};sp=write('selected_spec.json',spec);raw=Path(sp['path']).read_bytes();key=reg['entries'][0]['key'];reg['entries'][0]['spec']=sp
rp=write('register.json',reg);root['register']=rp
launch=json.loads(Path(root['runtime']['direct_launch']['path']).read_bytes());launch['register']=rp;root['runtime']['direct_launch']=write('launch.json',launch)
binding=json.loads(Path(root['binding']['path']).read_bytes());binding['register']=rp;root['binding']=write('stageb.json',binding)
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
 got=observe(**a);assert got['registered'] and decide(**got)=='HOLD_UNKNOWN_EXTERNAL_STATE';passed.append('actual joined prerequisites pass but unknown liveness holds')
 for name,changes in [('unrequested',dict(call_index=1)),('foreign code',{})]:
  if name=='foreign code':ctx.driver=dict(ctx.driver,sha256='0'*64)
  try:observe(**dict(a,**changes))
  except Refusal:passed.append(name+' refuses')
  else:raise AssertionError(name)
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Live receipt/liveness and acceptance classification','Full executor installation','Concurrent plan mutation injection','Consumer freeze'],pins=[pin(p) for p in [Path(__file__),b/'natural_registered_observation_cx1v001.py',b/'natural_request_cx1v001.py']])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'TEST_REPORT.json')
