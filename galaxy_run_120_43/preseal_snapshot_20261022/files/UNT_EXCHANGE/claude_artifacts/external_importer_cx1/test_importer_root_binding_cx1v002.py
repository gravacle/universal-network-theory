from pathlib import Path
import tempfile,json,copy,hashlib
from snapshot_cx1v001 import Snapshot,Refusal
from importer_root_binding_cx1v002 import load
b=Path(__file__).parent;c=Path(tempfile.mkdtemp(prefix='root_plan_',dir=b/'inert_fixtures'))
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,o):
 p=c/n
 with p.open('x') as f:json.dump(o,f)
 return pin(p)
root=json.loads((b/'inert_fixtures/observation_entry_zn2194gv/inert_root_binding.json').read_bytes())
root['schema']='CX1_IMPORTER_ROOT_BINDING_V002';root['direct_plan']=write('inert_plan.json',{'inert':True})
a=dict(expected_policy=root['policy'],expected_entry=root['entry'],context=root['context'])
cases=[('valid',lambda x:None,True),('missing plan',lambda x:x.pop('direct_plan'),False),('bad plan pin',lambda x:x['direct_plan'].update(sha256='0'*64),False),('legacy schema',lambda x:x.update(schema='CX1_IMPORTER_ROOT_BINDING_V001'),False),('extra field',lambda x:x.update(candidate_override={}),False),('foreign policy',lambda x:x['policy'].update(sha256='0'*64),False),('foreign context',lambda x:x['context'].update(cache_id='0'*64),False)]
passed=[]
for i,(name,change,expected) in enumerate(cases):
 o=copy.deepcopy(root);change(o);p=write(str(i)+'.json',o)
 try:
  s=Snapshot();v=load(s,binding_pin=p,**a);ok=True
  assert v['direct_plan_pin']==root['direct_plan'] and all(n==1 for n in s.read_counts.values())
 except Refusal:ok=False
 assert ok==expected,name
 passed.append(dict(name=name,status='PASS'))
with (c/'TEST_REPORT.json').open('x') as f:json.dump(passed,f,indent=2)
print(c/'TEST_REPORT.json')
