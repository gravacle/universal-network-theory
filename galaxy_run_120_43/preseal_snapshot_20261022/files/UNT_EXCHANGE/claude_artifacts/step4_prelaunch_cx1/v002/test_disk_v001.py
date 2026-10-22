import ast,hashlib,importlib.util,json,types
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).parent;D=HERE/'disk_v001';p=D/'step4_guard_cx1v008.py';sp=importlib.util.spec_from_file_location('diskguard',p);G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
root=HERE/'disk_fixture_v001';root.mkdir();volume=root.parent
plan={'launcher_log':str(root/'launcher.log'),'calls':[{'case':'A','outdir':str(root/'A'),'receipt':str(root/'A.json'),'monitor_log':str(root/'A.log'),'output_cap_bytes':100},{'case':'B','outdir':str(root/'B'),'receipt':str(root/'B.json'),'monitor_log':str(root/'B.log'),'output_cap_bytes':150}]}
checks=[]
def check(name,fn,expected=None):
 try:fn();ok=expected is None;detail='accepted'
 except Exception as e:detail=str(e);ok=expected is not None and expected in detail
 checks.append({'name':name,'passed':ok,'detail':detail})
def measure(n):return patch.object(G.os,'statvfs',return_value=types.SimpleNamespace(f_bavail=n,f_frsize=1))
with patch.object(G,'OUTPUT_ROOT',root),patch.object(G,'OUTPUT_VOLUME',volume),patch.object(G.os.path,'ismount',return_value=True):
 with measure(G.DISK_RESERVE_BYTES+250):check('batch_exact_boundary',lambda:G.disk_admission(plan))
 with measure(G.DISK_RESERVE_BYTES+249):check('batch_below_bound',lambda:G.disk_admission(plan),'DISK_BATCH_BOUND')
 with measure(G.DISK_RESERVE_BYTES+100):check('start_exact_boundary',lambda:G.disk_admission(plan,plan['calls'][0]))
 with measure(G.DISK_RESERVE_BYTES+99):check('start_below_bound',lambda:G.disk_admission(plan,plan['calls'][0]),'DISK_START_BOUND')
 with patch.object(G.os,'statvfs',side_effect=OSError('stub unreadable')):check('unreadable_df_equivalent',lambda:G.disk_admission(plan),'DISK_READING_UNAVAILABLE')
 bad=json.loads(json.dumps(plan));bad['calls'][0]['outdir']='/private/tmp/another_volume/A'
 check('wrong_output_volume_path',lambda:G.disk_admission(bad),'OUTPUT_OUTSIDE_DECLARED_ROOT')
 with patch.object(G.os.path,'ismount',return_value=False):check('unmounted_external',lambda:G.disk_admission(plan),'DECLARED_OUTPUT_VOLUME_UNMOUNTED')
 original=Path.stat
 def device_mismatch(self,*a,**kw):
  st=original(self,*a,**kw)
  if self==root:return types.SimpleNamespace(st_mode=st.st_mode,st_dev=st.st_dev+1)
  return st
 with patch.object(Path,'stat',device_mismatch):check('nested_other_volume',lambda:G.disk_admission(plan),'WRONG_OUTPUT_VOLUME')
# Source wiring checks; never execute a launcher entrypoint or worker.
ls=(D/'step4_launcher_cx1v009.py').read_text();gs=p.read_text()
check('launcher_prestart_wiring',lambda:exec("assert 'disk=G.disk_admission(plan,pending[0])' in ls and 'G.disk_admission(plan,c)' in ls"))
check('guard_batch_wiring',lambda:exec("assert 'if disk_batch:disk_admission(plan)' in gs"))
r={'scope':'TESTED actual disk helper with inert filesystem and stub statvfs/df-equivalent readings; launcher wiring inspected only. Real External1 and scientific execution UNTESTED.','checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'hashes':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [*sorted(D.glob('*.py')),Path(__file__)]}}
with (HERE/'DISK_TEST_RESULTS_V001.json').open('x') as f:json.dump(r,f,indent=2)
print(json.dumps(r,indent=2));raise SystemExit(not all(c['passed'] for c in checks))
