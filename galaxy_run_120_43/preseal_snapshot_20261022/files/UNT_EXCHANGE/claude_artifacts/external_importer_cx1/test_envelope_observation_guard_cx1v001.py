"""Synthetic signed START/pinset tests; no real phase output or launch."""
from pathlib import Path
import sys,tempfile,json,hashlib,copy
b=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/external_importer_cx1');sys.path.insert(0,str(b))
from envelope_observation_adapter_cx1v002 import build
from envelope_observation_guard_cx1v001 import check_observation
from snapshot_cx1v001 import Snapshot,Refusal
parent=b.parent/'pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py'
m,_=build(parent.read_bytes(),str(parent))
c=Path(tempfile.mkdtemp(prefix='signed_observation_',dir=b/'inert_fixtures'))
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,obj,sign=True):
 obj=copy.deepcopy(obj)
 if sign:
  obj.pop('body_sha256',None);obj['body_sha256']=m.sha_b(m.canon(obj).encode('ascii'))
 p=c/name
 with p.open('x') as f:json.dump(obj,f,sort_keys=True)
 return pin(p),obj
f=c/'inert.txt'
with f.open('x') as out:out.write('inert fixture')
required=[pin(f)]
pp,ps=write('synthetic_pinset.json',dict(schema=m.SCHEMA_PINSET,phase='L2_DIRECT',pins=required,excluded=[],unresolved_pins=[]))
start=m.observe(ps,pp['sha256'],pp['path']);start['label']='start'
sp,start=write('synthetic_start.json',start)
def run(s=sp,p=pp,r=required):
 before=sorted(x.name for x in c.iterdir())
 result=check_observation(Snapshot(),tool_pin=pin(parent),start_pin=s,pinset_pin=p,required_pins=r)
 assert sorted(x.name for x in c.iterdir())==before
 return result
result=run();assert result['final_END'] is False and result['observation_label']=='observation'
passed=['valid synthetic signed START plus fresh observation; no writes']
for field,value,expected in [('phase','OTHER','ENVELOPE_PHASE'),('label','observation','START_LABEL'),('body_sha256','0'*64,'ENVELOPE_BODY_SHA'),('pin_set',{},'START_PINSET_BINDING')]:
 bad=copy.deepcopy(start);bad[field]=value
 bp,_=write('bad_'+field+'.json',bad,sign=field!='body_sha256')
 try:run(s=bp)
 except Refusal as exc:assert expected in str(exc),str(exc)
 else:raise AssertionError(field)
 passed.append(field+' mismatch refuses')
for name,r,expected in [('missing',[dict(path=str(c/'absent'),sha256='a'*64)],'REQUIRED_PIN_MISSING'),('duplicate',required*2,'DUPLICATE_REQUIRED_PIN'),('empty',[],'REQUIRED_COVERAGE')]:
 try:run(r=r)
 except Refusal as exc:assert expected in str(exc),str(exc)
 else:raise AssertionError(name)
 passed.append(name+' coverage refuses')
report=dict(status='PASS',blocking_count=0,tested=passed,untested=['Root provenance/authenticity of caller-supplied pins','Live concurrent mutation','Final END invalidation and consumed-campaign freeze','Production integration'],pins=[pin(parent),pin(b/'envelope_observation_adapter_cx1v002.py'),pin(b/'envelope_observation_guard_cx1v001.py'),pin(Path(__file__))])
with (c/'TEST_REPORT.json').open('x') as out:json.dump(report,out,indent=2)
print(c/'TEST_REPORT.json')
