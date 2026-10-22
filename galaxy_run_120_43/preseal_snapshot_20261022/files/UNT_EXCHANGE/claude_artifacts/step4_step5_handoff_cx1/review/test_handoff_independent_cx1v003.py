"""Independent inert writer/custody/filler checks. Production science never asserted."""
import builtins,copy,hashlib,io,json,os,stat,sys,types
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parent;I=R.parent/'impl';OUT=R/'CONTROLS_INDEPENDENT_V003';OUT.mkdir();checks=[];pins={}
def read(p):b=Path(p).read_bytes();pins[str(p)]=hashlib.sha256(b).hexdigest();return b
def pin(p):read(p);return {'path':str(p),'sha256':pins[str(p)]}
def load(p,name):m=types.ModuleType(name);m.__file__=str(p);exec(compile(read(p),str(p),'exec'),m.__dict__);return m
def check(name,fn,error=None):
 try:v=fn();ok=error is None and v is not False;detail=repr(v)[:170]
 except BaseException as e:ok=error is not None and error in str(e);detail=type(e).__name__+': '+str(e)
 checks.append({'name':name,'passed':ok,'detail':detail})
W=load(I/'write_step4_step5_handoff_cx1v008.py','independent_handoff_writer');base=I/'tests/CONTROLS_V005/nominal_synthetic';a=json.loads(read(base/'authority.json'));r=json.loads(read(a['record_pin']['path']));ap=pin(base/'authority.json')
def put(p,obj):
 b=W.encoded(obj) if not isinstance(obj,bytes) else obj
 with p.open('xb') as f:f.write(b)
 return pin(p)
def case(name,mutator):
 d=OUT/name;d.mkdir();rr=copy.deepcopy(r);aa=copy.deepcopy(a);mutator(rr,aa,d);aa['record_pin']=put(d/'record.json',rr);authority=put(d/'authority.json',aa);return d,authority

def run_case(name,mutator,error):
 d,aa=case(name,mutator);check(name,lambda:W.write_point(aa['path'],aa['sha256'],d/'out',synthetic_dry_only=True),error);check(name+' no output',lambda:not (d/'out').exists())
# Unpublished or stale digest fails before any dependency is opened.
opened=[];origopen=builtins.open

def track(p,*args,**kw):opened.append(str(p));return origopen(p,*args,**kw)
with patch.object(builtins,'open',track):
 check('wrong external authority digest',lambda:W.prepare(ap['path'],'0'*64,OUT/'bad_authority',synthetic_dry_only=True),'PIN_BYTES_CHANGED')
check('wrong digest reads only authority',lambda:opened==[str(W.safe_path(ap['path']))])
check('synthetic input refuses production mode',lambda:W.prepare(ap['path'],ap['sha256'],OUT/'wrong_mode'),'EXTERNAL_ROOT_PUBLICATION_REQUIRED')
run_case('prelaunch is not scientific admission',lambda rr,aa,d:rr.update(status='PRELAUNCH'),'SCIENTIFIC_ADMITTED_POINT_REQUIRED')
run_case('no admitted point',lambda rr,aa,d:rr.update(point=None),'CONSUMER_COORDINATE_CONTRACT')
run_case('native three u preserved refusal',lambda rr,aa,d:rr['point']['u'].pop(),'CONSUMER_COORDINATE_CONTRACT')
run_case('boolean selected index refuses',lambda rr,aa,d:rr['point'].update(log_index=False),'CONSUMER_COORDINATE_CONTRACT')

def seal_bad(rr,aa,d):
 s=json.loads(read(rr['v007']['seal']['path']));s['sealed_by']={};rr['v007']['seal']=put(d/'unsealed.json',s)
run_case('missing sealed V007',seal_bad,'SEALED_V007_REQUIRED')
def forged_science(rr,aa,d):
 e=json.loads(read(rr['scientific_evidence_pin']['path']));e['model_values'][0]=999;rr['scientific_evidence_pin']=put(d/'science.json',e)
run_case('forged scientific membership refuses producer replay',forged_science,'PRODUCER_SCIENTIFIC_VERIFICATION_REQUIRED')
# Recursive target field in a record must reject before opening producer or any record refs.
for key in ('observed_velocities','target_values','rotation_curve','v_obs'):
 d,aa=case('nested_'+key,lambda rr,aa,d,key=key:rr['provenance'].update(extra=[{'nested':{key:[1.]}}]));seen=[]
 def traced(p,*args,**kw):seen.append(str(p));return origopen(p,*args,**kw)
 with patch.object(builtins,'open',traced):check('recursive target '+key,lambda:W.prepare(aa['path'],aa['sha256'],d/'out',synthetic_dry_only=True),'TARGET_FIELD_REFUSED')
 forbidden={str(W.safe_path(a['producer_pin']['path'])),str(W.safe_path(a['rule_pin']['path']))}|{str(W.safe_path(x['path'])) for x in r['v007'].values()}
 check('target rejected before dependencies '+key,lambda:not forbidden.intersection(seen))
# Virtual lexical and symlink targets: real protected metadata is never reached.
for value in ('/virtual/UVT_NEVER/file','/virtual/KMAX_A2F10_C5H_RUN_V001/file','/virtual/NGC3198_observed_velocities.json'):
 probes=[]
 def deny(*x,**kw):probes.append(x);raise AssertionError('METADATA_BEFORE_REFUSAL')
 with patch.object(os,'stat',deny),patch.object(os,'lstat',deny),patch.object(os,'readlink',deny),patch.object(Path,'resolve',deny):
  check('lexical protected refusal '+value,lambda:W.safe_path(value),'PATH_REFUSED')
 check('zero lexical metadata '+value,lambda:probes==[])
probes=[]
def lstat(p):
 p=str(p);probes.append(p);assert 'UVT_NEVER' not in p;return types.SimpleNamespace(st_mode=stat.S_IFLNK if p=='/virtual/alias' else stat.S_IFDIR)
with patch.object(os,'lstat',lstat),patch.object(os,'readlink',return_value='/virtual/UVT_NEVER/record.json'):
 check('symlink protected target refusal',lambda:W.safe_path('/virtual/alias'),'PROTECTED_PATH_REFUSED')
check('zero symlink target metadata',lambda:probes==['/virtual','/virtual/alias'])
# Each source opens at most once. Late backing-record changes cannot change emitted point.
record_path=str(W.safe_path(a['record_pin']['path']));opens={};record_reads=[]
class Reader:
 def __init__(self,f):self.f=f
 def __enter__(self):return self
 def __exit__(self,*x):self.f.close()
 def read(self,*x):
  record_reads.append(1);return self.f.read(*x) if len(record_reads)==1 else b'{"later":"changed"}'
def lateopen(p,*args,**kw):
 name=str(p);opens[name]=opens.get(name,0)+1;f=origopen(p,*args,**kw);return Reader(f) if name==record_path else f
with patch.object(builtins,'open',lateopen):payload,receipt=W.prepare(ap['path'],ap['sha256'],OUT/'snapshot_output',synthetic_dry_only=True)
check('every dependency byte snapshot opened once',lambda:all(n==1 for n in opens.values()))
check('record late read cannot change emitted bytes',lambda:len(record_reads)==1 and json.loads(payload['TARGET_FREE_EXPORT_CX1V001.json'])['admitted_points']==[r['point']])
check('snapshot custody hashes match actual bytes',lambda:all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in receipt['source_snapshots'].items()))
# Fence operates at actual producer module execution and preserves metadata functions.
stat_before=os.stat
with W.pure_producer_fence():
 check('producer file read denied',lambda:open('/private/tmp/NO_PRODUCER_READ','rb'),'PRODUCER_IO_OR_PROCESS_REFUSED')
 check('producer stat denied before OS',lambda:os.stat('/private/tmp/NO_PRODUCER_STAT'),'PRODUCER_METADATA_REFUSED')
check('producer fence restored',lambda:os.stat is stat_before and W.PRODUCER_ACTIVE is False)
with W.pure_producer_fence():
 for event in ('os.chmod','os.chown','os.utime','os.setxattr','os.removexattr','os.truncate','os.putenv','os.link','os.symlink','shutil.copyfile','ctypes.dlopen','subprocess.Popen','socket.connect'):
  check('inert producer audit '+event,lambda event=event:sys.audit(event,'INERT_NO_OPERATION'),'PRODUCER_IO_OR_PROCESS_REFUSED')
check('producer fence restored after inert audit controls',lambda:os.stat is stat_before and W.PRODUCER_ACTIVE is False)
# Real selected writer then real selected filler, in synthetic mode only.
wr=W.write_point(ap['path'],ap['sha256'],OUT/'handoff',synthetic_dry_only=True);hp=wr['handoff_pin'];F=load(Path(W.FILLER['path']),'actual_selected_filler')
fr=F.fill(hp['path'],hp['sha256'],OUT/'filled',True)
check('actual writer to selected filler',lambda:len(fr['outputs'])==4 and fr['launch_authorized'] is False and fr['mode']=='SYNTHETIC_DRY_ONLY')
check('synthetic output cannot claim adopted V007',lambda:json.loads(Path(hp['path']).read_bytes())['v007_adoption_pin'] is None)
check('certificates remain pending in synthetic specs',lambda:set(fr['pending_certificates'])=={'eps_certificate','lo_certificate'})
check('filler source point matches emitted point',lambda:all(x['source_point']['point_canonical_sha256']==W.digest(W.canonical(r['point'])) for x in fr['outputs']))
check('writer exclusive no overwrite',lambda:W.write_point(ap['path'],ap['sha256'],OUT/'handoff',synthetic_dry_only=True),'NEW_OUTPUT_DIRECTORY_REQUIRED')
read(__file__)
report={'status':'TESTED','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'writer_pin':pin(Path(W.__file__)),'selected_filler_pin':W.FILLER,'filled_directory':str(OUT/'filled'),'driver_selection':fr['driver_selection'],'handoff_pin':hp,'fixture_authority_pin':ap,'sha256_from_bytes':pins,'limits':['All point/adoption/certificate inputs are owned synthetic fixtures.','Real production authority and producer verification remain UNTESTED.','No scientific process or target/protected data access.','Actual selected filler ran; dry plan recorded separately.']}
with (OUT/'RESULTS.json').open('x') as f:json.dump(report,f,indent=2)
print(json.dumps({'passed':report['passed'],'total':report['total'],'failures':[x for x in checks if not x['passed']],'sha256':hashlib.sha256((OUT/'RESULTS.json').read_bytes()).hexdigest()}))
raise SystemExit(0 if report['passed']==report['total'] else 1)
