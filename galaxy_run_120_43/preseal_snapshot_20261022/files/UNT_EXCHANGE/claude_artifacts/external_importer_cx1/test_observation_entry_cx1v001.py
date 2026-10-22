"""Actual isolated CLI with inert root binding and synthetic START; no production phase."""
from pathlib import Path
import sys,json,hashlib,tempfile,subprocess,copy
from envelope_observation_adapter_cx1v002 import build
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='observation_entry_',dir=b/'inert_fixtures'));old=b/'inert_fixtures/registered_runtime__y4kw_c9'
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,obj):
 p=c/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True)
 return pin(p)
root=json.loads((old/'root_binding.json').read_bytes());policy=json.loads((b/'IMPORTER_POLICY_DRAFT_CX1V003.json').read_bytes());policy['components']['importer_root_binding_cx1v001.py']=pin(b/'importer_root_binding_cx1v001.py')
pp=write('inert_policy.json',policy);entry=pin(b/'importer_observation_entry_cx1v001.py')
freeze=write('inert_freeze.json',dict(schema='CX1_IMPORTER_FREEZE_V001',utc='2026-10-21T11:00:00Z',policy=pp,entry=entry))
runtime=root['runtime'];runtime['freeze']=freeze
launch=json.loads(Path(runtime['direct_launch']['path']).read_bytes());launch['freeze']=freeze;runtime['direct_launch']=write('inert_launch.json',launch)
binding=json.loads(Path(root['binding']['path']).read_bytes());binding['freeze']=freeze;root['binding']=write('inert_stageb.json',binding)
root['policy']=pp;root['entry']=entry
reg=json.loads(Path(root['register']['path']).read_bytes());required=[root['register'],runtime['driver'],runtime['monitor'],pp,entry]
for row in reg['entries']:required.extend(row[k] for k in ['spec','launcher','guard','binder','dbp','runtime_capture'])
required=list({(p['path'],p['sha256']):p for p in required}.values())
parent=b.parent/'pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py';m,_=build(parent.read_bytes(),str(parent))
def signed(name,obj):
 obj=copy.deepcopy(obj);obj.pop('body_sha256',None);obj['body_sha256']=m.sha_b(m.canon(obj).encode('ascii'));return write(name,obj),obj
pspin,ps=signed('inert_pinset.json',dict(schema=m.SCHEMA_PINSET,phase='L2_DIRECT',pins=required,excluded=[],unresolved_pins=[]))
start=m.observe(ps,pspin['sha256'],pspin['path']);start['label']='start';sp,_=signed('synthetic_start.json',start)
root['envelope']=dict(tool=pin(parent),start=sp,pinset=pspin);rp=write('inert_root_binding.json',root)
request=dict(schema='CX1_OBSERVATION_REQUEST_V001',policy=pp,entry=entry,root_binding=rp,context=root['context'],key=reg['entries'][0]['key'],spec=reg['entries'][0]['spec']);request_pin=write('inert_request.json',request)
def run(p):return subprocess.run([sys.executable,'-I','-B',entry['path'],'--request',p['path'],'--request-sha256',p['sha256']],capture_output=True,text=True)
before=set(c.iterdir());ok=run(request_pin);assert ok.returncode==0,ok.stderr
result=json.loads(ok.stdout);assert result['status']=='PREREQUISITES_ONLY' and result['registered'] and result['admission_authorized'] is False and result['launch_authorized'] is False and result['final_END'] is False
assert set(c.iterdir())==before
passed=['actual isolated CLI verifies pinned bootstrap and joint evidence','CLI writes no fixture files and returns prerequisites only']
bad=run(dict(request_pin,sha256='0'*64));assert bad.returncode==2;passed.append('wrong root request digest refuses')
foreign=copy.deepcopy(request);foreign['entry']['sha256']='0'*64;fp=write('foreign_entry_request.json',foreign);bad=run(fp);assert bad.returncode==2;passed.append('foreign entry bytes refuse')
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Root real request/authorship/adoption','Production installation','Natural-plan/liveness/acceptance observer','Durable final invalidation and consumer freeze'],pins=[pin(p) for p in [Path(__file__),Path(entry['path']),b/'pinned_helper_loader_cx1v001.py',Path(request_pin['path'])]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'TEST_REPORT.json')
