"""D002 in-memory observation tests on inert files; no phase writes or real START/END."""
from pathlib import Path
import tempfile,os,json,hashlib,copy
from envelope_observation_adapter_cx1v002 import build
b=Path(__file__).resolve().parent;parent=b.parent/'pinned_input_envelope_c2v003/pinned_input_envelope_c2v003.py'
m,_=build(parent.read_bytes(),str(parent));c=Path(tempfile.mkdtemp(prefix='envelope_observation_',dir=b/'inert_fixtures'))
a=c/'inert_a.txt';alias=c/'inert_alias.txt'
with a.open('xb') as f:f.write(b'INERT ENVELOPE BYTES')
os.link(a,alias);sha=hashlib.sha256(a.read_bytes()).hexdigest()
ps={'phase':'L2_DIRECT','pins':[{'path':str(p),'sha256':sha} for p in [a,alias]],'excluded':[],'unresolved_pins':[],'body_sha256':'a'*64}
reads=[];original=m.read_once
m.read_once=lambda path,*args,**kwargs:(reads.append(str(path)) or original(path,*args,**kwargs))
before={p.name for p in c.iterdir()}
first=m.observe(ps,'b'*64,'/INERT/PINSET.json');assert len(reads)==1 and first['counts']['n_alias_files']==1
start=copy.deepcopy(first);start['label']='start' # synthetic fixture only
reads.clear();fresh=m.observe(ps,'b'*64,'/INERT/PINSET.json');assert len(reads)==1
assert fresh['label']=='observation' and not m.compare_observation(start,fresh)['problems']
assert {p.name for p in c.iterdir()}==before
passed=['hardlinked inode read once per observation','unchanged observation compares equal','no filesystem writes during observation/compare']
for name in ['sha','inode','status','alias_resolution','ctime']:
 changed=copy.deepcopy(fresh)
 if name=='sha':changed['files'][0]['sha256_from_bytes']='c'*64
 elif name=='inode':changed['files'][0]['ino']=changed['files'][0].get('ino',0)+1
 elif name=='status':changed['pins'][0]['status']='mismatch';changed['pins'][0]['match']=False
 elif name=='alias_resolution':changed['pins'][0]['realpath']=str(alias) if changed['pins'][0]['realpath']==str(a) else str(a)
 else:changed['files'][0]['ctime_ns']+=1
 problems=m.compare_observation(start,changed)['problems'];assert problems,name
 passed.append('synthetic '+name+' difference invalidates')
report=dict(status='PASS',blocking_count=0,tested=passed,scope=__doc__,untested=['Root START/pinset authentication wrapper','Live concurrent filesystem mutation','Final phase invalidation and consumption freeze'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [b/'envelope_observation_adapter_cx1v002.py',parent,Path(__file__)]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
