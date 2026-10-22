import sys,copy,json,hashlib,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from invocation_plan_binding_cx1v002 import bind
from snapshot_cx1v001 import Snapshot
from request_guard_cx1v002 import Refusal
B=Path(__file__).parent;A=B.parent
f=Path(tempfile.mkdtemp(prefix='invocation_',dir=B/'inert_fixtures'))
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
l=pin(A/'s1_successors_c2/step4_launcher_c2v015.py');m=pin(A/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py')
d={'path':'/inert/driver','sha256':'a'*64};sp={'path':'/inert/spec','sha256':'b'*64}
e=dict(launcher=l,spec=sp,key='c'*64,row=28,call_root=str(f/'D'))
c=dict(point_key=e['key'],row=28,spec=sp,driver=d,spec_status='ROOT_FINAL',pending=[],outdir=e['call_root']+'/out',receipt=e['call_root']+'/RECEIPT.json',monitor_log=e['call_root']+'/monitor.log',wall_cap_s=11,rss_cap_bytes=22,output_cap_bytes=33)
p=dict(schema='UNT_STEP4_LAUNCH_PLAN_CX1V001',binding_status='ROOT_BOUND',launcher=l,monitor=m,calls=[c])
cases=[('float wall',lambda x:x['calls'][0].update(wall_cap_s=11.0),False),('float row',lambda x:x['calls'][0].update(row=28.0),False),('valid',lambda x:None,True),('template',lambda x:x.update(binding_status='TEMPLATE_UNBOUND'),False),('duplicate',lambda x:x['calls'].append(copy.deepcopy(c)),False),('foreign spec',lambda x:x['calls'][0].update(spec=d),False),('foreign output',lambda x:x['calls'][0].update(outdir='/inert/other'),False),('pending',lambda x:x['calls'][0].update(pending=['WAIT']),False),('boolean cap',lambda x:x['calls'][0].update(rss_cap_bytes=True),False),('negative wall',lambda x:x['calls'][0].update(wall_cap_s=-1),False),('template residue',lambda x:x.update(template_metadata={}),False),('foreign monitor',lambda x:x.update(monitor=d),False)]
results=[]
for i,(name,change,expected) in enumerate(cases):
 obj=copy.deepcopy(p);change(obj);q=f/('%02d.json'%i)
 with q.open('x') as h:json.dump(obj,h)
 try:
  out=bind(Snapshot(),plan_pin=pin(q),entry=e,driver=d,monitor=m);ok=True
  assert out['caps']==dict(wall_cap_s=11,rss_cap_bytes=22,output_cap_bytes=33,poll_s=2.0)
 except Refusal:ok=False
 assert ok==expected,name
 results.append(dict(name=name,status='PASS'))
with (f/'TEST_REPORT.json').open('x') as h:json.dump(results,h,indent=2)
print(f/'TEST_REPORT.json')
