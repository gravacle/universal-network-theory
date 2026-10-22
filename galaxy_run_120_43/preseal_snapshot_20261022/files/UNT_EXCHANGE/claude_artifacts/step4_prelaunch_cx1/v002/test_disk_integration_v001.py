"""Actual guard validation and worker loop; inert adapters and mocked process seam."""
import ast,contextlib,hashlib,importlib.util,io,json,os,types
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).parent;BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl')
sp=importlib.util.spec_from_file_location('launcher_disk',BASE/'step4_launcher_cx1v009.py');L=importlib.util.module_from_spec(sp);sp.loader.exec_module(L);G=L.G
OUT=HERE/'disk_integration_fixtures_v001';OUT.mkdir();seq=0
R5=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py');MON=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py')
source=BASE/'tests/test_step4_cx1v007.py';tree=ast.parse(source.read_bytes());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('put','build')],type_ignores=[]),str(source),'exec'))
checks=[]
for mode in ('positive','batch_low','start_low','unreadable','wrong_volume'):
 f=build();plan=f[2];cfg=f[3];cap=plan['calls'][0]['output_cap_bytes'];spawns=[];output=io.StringIO()
 class Proc:
  pid=12345
  def __init__(self,kind):self.kind=kind
  def poll(self):return None if self.kind=='assertion' else 0
 def spawn(argv,**kw):spawns.append(argv);return Proc('assertion' if '-w' in argv else 'monitor')
 raw=G.raw
 def read(p):return b'{"status":"FINISHED"}' if str(p)==plan['calls'][0]['receipt'] else raw(p)
 free=G.DISK_RESERVE_BYTES+cap-(1 if mode in ('batch_low','start_low') else 0)
 with contextlib.ExitStack() as stack:
  for target,attr,value in [(G,'OUTPUT_ROOT',OUT),(G,'OUTPUT_VOLUME',HERE),(G.os.path,'ismount',lambda p:True),(L,'runtime_settings',lambda:None),(L,'normal_qos',lambda:None),(L,'acquire_lock',lambda:os.open('/dev/null',os.O_RDONLY)),(L.subprocess,'Popen',spawn),(L,'memory_free',lambda:80),(L,'route_a_finished',lambda p:True),(L,'first_iteration',lambda p:True),(L.time,'sleep',lambda n:None),(G,'raw',read)]:stack.enter_context(patch.object(target,attr,value))
  if mode=='unreadable':stack.enter_context(patch.object(G.os,'statvfs',side_effect=OSError('stub unreadable')))
  else:stack.enter_context(patch.object(G.os,'statvfs',return_value=types.SimpleNamespace(f_bavail=free,f_frsize=1)))
  if mode=='wrong_volume':stack.enter_context(patch.object(G,'OUTPUT_ROOT',OUT/'other_root'))
  stack.enter_context(patch.dict(os.environ,{'UNT_STEP4_ADMISSION_PATH':f[1]['path'],'UNT_STEP4_ADMISSION_SHA256':f[1]['sha256']}))
  stack.enter_context(contextlib.redirect_stdout(output))
  try:
   if mode=='batch_low':
    try:G.validate(f[0],L.__file__,config_ref=f[1]);raise AssertionError('accepted low batch')
    except G.Refusal as e:assert str(e)=='DISK_BATCH_BOUND';rc=1
   else:
    if mode=='positive':G.validate(f[0],L.__file__,config_ref=f[1])
    with Path(plan['launcher_log']).open('xb'):pass
    rc=L.worker(f[0])
   monitors=[a for a in spawns if '-w' not in a]
   assert rc==(0 if mode=='positive' else 1)
   assert len(monitors)==(1 if mode=='positive' else 0)
   ok=True;detail='rc=%s mocked monitors=%s'%(rc,len(monitors))
  except Exception as e:ok=False;detail=type(e).__name__+': '+str(e)
 checks.append({'name':mode,'passed':ok,'detail':detail,'worker_log':output.getvalue()})
r={'scope':'Actual guard.validate and launcher.worker with synthetic native adapters, stub disk readings and mocked all subprocess creation. No scientific process; production integration UNTESTED.','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(L.__file__),Path(G.__file__),source]}}
with (HERE/'DISK_INTEGRATION_RESULTS_V001.json').open('x') as f:json.dump(r,f,indent=2)
print(json.dumps({'passed':r['passed'],'total':r['total'],'checks':[{k:v for k,v in c.items() if k!='worker_log'} for c in checks]}));raise SystemExit(not all(c['passed'] for c in checks))
