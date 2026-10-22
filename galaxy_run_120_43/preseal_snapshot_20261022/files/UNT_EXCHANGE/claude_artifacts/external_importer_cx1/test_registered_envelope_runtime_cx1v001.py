"""Actual register/runtime/envelope guards joined on inert evidence; synthetic START only."""
from pathlib import Path
import runpy,json,hashlib,copy
from snapshot_cx1v001 import Snapshot,Refusal
from registered_envelope_runtime_cx1v001 import check
from envelope_observation_adapter_cx1v002 import build
b=Path(__file__).resolve().parent;g=runpy.run_path(str(b/'test_registered_runtime_cx1v004.py'));c=g['c'];write=g['write'];context=g['context']
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
p=c/'JOINT_INERT'
with p.open('x') as f:f.write('INERT dependency bytes')
dummy=pin(p);runtime=copy.deepcopy(g['runtime']);runtime['captured_utc']='2026-10-21T12:00:00Z'
dp=write('joint_direct.json',runtime);cp=write('joint_campaign.json',runtime)
entries=copy.deepcopy(g['entries'])
for e in entries:
 for field in ('spec','launcher','guard','binder','dbp'):e[field]=dummy
 e['runtime_capture']=dp
rp=write('joint_register.json',dict(schema='SPECULATIVE_REGISTER_L2_V001',entries=entries))
freeze=write('joint_freeze.json',dict(schema='CX1_IMPORTER_FREEZE_V001',utc='2026-10-21T11:00:00Z',policy=dummy,entry=dummy))
identity={k:runtime['interpreter'][k] for k in ('realpath','sha256')}
lp=write('joint_launch.json',dict(schema='SPECULATIVE_LAUNCH_L2_V001',utc='2026-10-21T13:00:00Z',register=rp,runtime_capture=dp,interpreter=identity,freeze=freeze))
bp=write('joint_binding.json',dict(schema='SPECULATIVE_REGISTER_BINDING_L2_V001',register=rp,context=context,campaign_capture=cp,utc='2026-10-21T13:00:00Z',interpreter=identity,freeze=freeze))
policy=dict(campaign_capture=cp,freeze=freeze,direct_launch=lp,producer=runtime['producer'],output_root=str(c),**{name:dict(path=runtime[name]['realpath'],sha256=runtime[name]['sha256']) for name in ('driver','monitor')})
parent=b.parent/'pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py';m,_=build(parent.read_bytes(),str(parent))
required=[rp,dummy,dp,policy['driver'],policy['monitor']]
def signed(name,obj):
 obj=copy.deepcopy(obj);obj.pop('body_sha256',None);obj['body_sha256']=m.sha_b(m.canon(obj).encode('ascii'));return write(name,obj),obj
def envelope(name,pins):
 pp,ps=signed(name+'_pinset.json',dict(schema=m.SCHEMA_PINSET,phase='L2_DIRECT',pins=pins,excluded=[],unresolved_pins=[]))
 start=m.observe(ps,pp['sha256'],pp['path']);start['label']='start'
 sp,_=signed(name+'_synthetic_start.json',start)
 return dict(tool=pin(parent),start=sp,pinset=pp)
ep=envelope('full',required)
args=dict(register_pin=rp,binding_pin=bp,context=context,key=entries[0]['key'],spec_pin=dummy,runtime_policy=policy,envelope_policy=ep)
s=Snapshot();before=set(c.iterdir());result=check(s,**args)
assert result['registered'] and not result['admission_authorized'] and result['envelope']['final_END'] is False
assert set(c.iterdir())==before and all(n==1 for n in s.read_counts.values())
passed=['joint actual checks pass without writes; each Snapshot path read once','original envelope excludes later campaign capture but binds direct capture','prerequisites never authorize admission or final END']
for label,omitted in [('direct_capture',dp),('register',rp),('code',dummy)]:
 bad=envelope(label,[p for p in required if p!=omitted])
 try:check(Snapshot(),**dict(args,envelope_policy=bad))
 except Refusal as e:assert 'REQUIRED_PIN_MISSING' in str(e)
 else:raise AssertionError(label)
 passed.append(label+' missing coverage refuses')
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Root authentication/installation','Liveness and acceptance observer','Live mutation','Final-phase consumer freeze'],pins=[pin(p) for p in [Path(__file__),b/'registered_envelope_runtime_cx1v001.py',b/'registered_runtime_cx1v005.py',b/'envelope_observation_guard_cx1v001.py',parent]])
with (c/'JOINT_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'JOINT_REPORT.json')
