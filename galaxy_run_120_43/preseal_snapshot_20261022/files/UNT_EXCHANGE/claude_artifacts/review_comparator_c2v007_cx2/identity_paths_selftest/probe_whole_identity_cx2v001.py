"""Independent full-main B-ID and path/inventory canaries. Reuses our prior owned Tree only.
All fixture mutations are in memory before exclusive publication. No actual run read.
"""
import os,sys,unicodedata
from pathlib import Path
ATTEMPTS=[];FIFO_READS=[]
def deny(p):
 if isinstance(p,(str,bytes,os.PathLike)):
  s=unicodedata.normalize('NFC',os.fsdecode(p)).casefold().replace('/system/volumes/data','')
  if any(x in s+'/' for x in ('/runs/','/runs_ext/','/.codex/','/out/identity','/gates_v007/records/')) or 'kmax_a2f10_c5h_run' in s or ('ngc3198' in s and any(t in s for t in ('target','observed','rotmod'))):ATTEMPTS.append(s);raise RuntimeError('PROTECTED_PATH')
def audit(e,a):
 if e=='open':
  deny(a[0])
  if isinstance(a[0],(str,bytes,os.PathLike)) and str(a[0]).endswith('/owned_fifo'):FIFO_READS.append(str(a[0]));raise RuntimeError('FIFO_OPEN')
 if e.startswith(('subprocess.','socket.')) or e in ('os.remove','os.rename','os.rmdir','os.system','os.exec','os.posix_spawn'):raise RuntimeError('FORBIDDEN_ACTION')
sys.addaudithook(audit)
for n in ('stat','lstat','readlink','listdir','scandir'):
 f=getattr(os,n)
 def wrap(p,*a,_f=f,**k):deny(p);return _f(p,*a,**k)
 setattr(os,n,wrap)
import contextlib,copy,datetime,hashlib,io,json,types,numpy as np
ROOT=Path(__file__).resolve().parent;A=ROOT.parent.parent
TARGET=A/'tail_scheme_impl_c2/gates_v007/run_identity_compare_c2v007.py';PIN='06ff52d636c640ebe9a92a4b2cf54620a01514992019e2b2f2dca1529f7dc188'
FACTORY=A/'review_comparator_c2v005_cx2/invocation/invocation_canaries_cx2v003.py';FPIN='711580269ba37be0fc6c4e7206c27ca5427d56b7a558e1247cff8e44172ce72e'
OUT=ROOT/('whole_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')+'_'+str(os.getpid()));OUT.mkdir()
PINS=[];rows=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def load(p,h,name):
 raw=Path(p).read_bytes();assert hashlib.sha256(raw).hexdigest()==h;PINS.append({'path':str(p),'sha256':h})
 m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(raw,str(p),'exec'),m.__dict__);return m
M=load(TARGET,PIN,'whole_identity_comparator');F=load(FACTORY,FPIN,'own_old_tree')
protected=OUT/'owned_protected';protected.mkdir();M.guarded_resolve.__defaults__=(str(protected),'owned_protected_marker')
cm=M.load_cm();PINS.append({'path':M.CKPT[0],'sha256':M.CKPT[1]})
REL='stages/07_route_a/checkpoint/IDENTITY.json'
def reseal(t,b):
 b.pop('payload_sha256',None);b['payload_sha256']=cm._sha(cm._canonical(b));t.files[REL]=('raw',cm._canonical(b)+b'\n')
def complete(t):
 b=json.loads(t.files[REL][1]);ident=b['identity']
 ident.update(format=cm.FORMAT,code={'solver':{'path':M.CKPT[0],'sha256':M.CKPT[1]},'checkpoint':{'path':M.CKPT[0],'sha256':M.CKPT[1]},'modules':{'source_module':None}},fixed_source={'selection':'EVALUATED','fixed_positions_and_integrated_columns':'FIXED_TERM_INPUT','supplied_fixed_source_fourier_J':None},environment={'python':'owned-synthetic','numpy':np.__version__,'platform':sys.platform,'machine':'owned-synthetic','byteorder':sys.byteorder},inputs_sha256={k:cm.digest(np.array([1.,2.])) for k in ('fixed_positions_m','fixed_integrated_columns_J','initial_gas_fourier_J','fixed_source_fourier_J','gas_columns')},shapes={'gas_column_count':1,'source_fourier':[2]},controls={'tolerance':cm.encode(0.00025)})
 ident['inputs_sha256']['fourier_arguments']={'owned':cm.digest(1)}
 b['identity_sha256']=cm._sha(cm._canonical(ident));reseal(t,b)
def modify(t,fn,redigest=True):
 b=json.loads(t.files[REL][1]);fn(b)
 if redigest and 'identity_sha256' in b:b['identity_sha256']=cm._sha(cm._canonical(b['identity']))
 reseal(t,b)
def case(driver,name,mut=None,expected='FAIL',owner=None,gate='Z2',post=None):
 M.DRIVER[:]=M.DRIVERS[driver];M.DRIVER_RAW[:]=[None,None];drv=M.load_driver()
 d=OUT/(driver+'_'+name);d.mkdir();r=F.Tree(d/'REF','REF',gate,M,drv,cm);n=F.Tree(d/'NEW','NEW',gate,M,drv,cm)
 if gate=='Z2':complete(r);complete(n)
 tok,_,probs=M.derive_tokens(gate,M.driver_env(Path(r.obj('start.json')['driver']).read_bytes(),r.obj('start.json')['driver']),M.driver_env(M.driver_raw(),M.DRIVER[0]));assert not probs
 if mut:mut(r,n)
 for t in (r,n):t.obj('finish.json')['result_sha256']=F.sha(F.raw_json(t.obj('result.json')))
 r.publish();n.publish()
 if post:post(r,n)
 tp=d/'TOKENS.json';F.jfile(tp,{'declared':tok});rp=d/'REPORT.json';err=None
 try:
  with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):code=M.main(['--gate',gate,'--driver',driver,'--reference',str(r.root),'--new',str(n.root),'--tokens',str(tp),'--out',str(rp)])
 except BaseException as e:err=type(e).__name__+':'+str(e);code=None
 rep=json.loads(rp.read_bytes()) if rp.exists() else {};f=rep.get('failing',[]);v=rep.get('verdict','NO_REPORT');ok=v==('PASS_BITWISE_EQUAL' if expected=='PASS' else 'FAIL') and (owner is None or owner in f) and 'COMPARATOR_EXCEPTION' not in f
 rows.append(dict(driver=driver,name=name,expected=expected,owner=owner,actual=v,failing=f,exception=err,expectation_met=ok,owner_detail=rep.get('checks',{}).get(owner) if owner else None,report=pin(rp) if rp.exists() else None))
 print(driver,name,v,f,flush=True)
for driver in ('r4','r5'):
 case(driver,'P00_full_identity_positive',expected='PASS')
 for field in ('format','code','controls','environment','fixed_source','inputs_sha256','shapes'):
  def change(r,n,field=field):
   def f(b):
    if field=='format':b['identity'][field]='changed-format'
    else:b['identity'][field]['owned_mutation']=17
   modify(n,f)
  case(driver,'I_'+field,change,owner='RA_IDENTITY')
 for path in ('solver','checkpoint','modules'):
  case(driver,'I_code_'+path,lambda r,n,path=path:modify(n,lambda b:b['identity']['code'].__setitem__(path,{'path':'/owned/static.py','sha256':'d'*64})),owner='RA_IDENTITY')
 case(driver,'I_unknown_nested',lambda r,n:modify(n,lambda b:b['identity'].update(unregistered={'x':1})),owner='RA_IDENTITY')
 case(driver,'I_unknown_outer',lambda r,n:modify(n,lambda b:b.update(unregistered={'x':1})),owner='RA_IDENTITY')
 case(driver,'I_unknown_outer_equal_both',lambda r,n:[modify(t,lambda b:b.update(unregistered={'x':1})) for t in (r,n)],owner='RA_IDENTITY')
 case(driver,'I_forged_identity_one',lambda r,n:modify(n,lambda b:b.update(identity_sha256='0'*64),False),owner='RA_IDENTITY')
 case(driver,'I_forged_identity_both',lambda r,n:[modify(t,lambda b:b.update(identity_sha256='0'*64),False) for t in (r,n)],owner='RA_IDENTITY')
 case(driver,'I_forged_caller_one',lambda r,n:modify(n,lambda b:b['identity']['caller'].update(sha256='0'*64)),owner='RA_IDENTITY')
 case(driver,'I_forged_caller_both',lambda r,n:[modify(t,lambda b:b['identity']['caller'].update(sha256='0'*64)) for t in (r,n)],owner='RA_IDENTITY')
 case(driver,'I_missing_identity_both',lambda r,n:[modify(t,lambda b:b.pop('identity_sha256'),False) for t in (r,n)],owner='RA_IDENTITY')
 case(driver,'I_missing_caller_digest_both',lambda r,n:[modify(t,lambda b:b['identity']['caller'].pop('sha256')) for t in (r,n)],owner='RA_IDENTITY')
 case(driver,'I_wrong_payload_one',lambda r,n:n.files.__setitem__(REL,('raw',n.files[REL][1].replace(b'"payload_sha256":"',b'"payload_sha256":"x'))),owner='RA_IDENTITY')
 case(driver,'P01_B0P_positive',expected='PASS',gate='B0P_RERUN')
 case(driver,'N_existing_stage_paths',lambda r,n:[t.obj('result.json').update(owned=str(t.root/'stages/11_reference/value')) for t in (r,n)],expected='PASS',gate='B0P_RERUN')
 case(driver,'N_absent_stage_paths',lambda r,n:[r.obj('result.json').update(owned=str(r.root/'stages/81_reference/value')),n.obj('result.json').update(owned=str(n.root/'stages/83_reference/value'))],owner='RESULT',gate='B0P_RERUN')
 case(driver,'N_absent_stage_keys',lambda r,n:[r.obj('result.json').update(owned={str(r.root/'stages/81_reference/value'):1}),n.obj('result.json').update(owned={str(n.root/'stages/83_reference/value'):1})],owner='RESULT',gate='B0P_RERUN')
 for sub in ('inputs/empty','stages/11_reference/output/empty','stages/11_reference/attempt_empty'):
  case(driver,'D_empty_'+sub.replace('/','_'),owner='INVENTORY',gate='B0P_RERUN',post=lambda r,n,sub=sub:(n.root/sub).mkdir(parents=True))
 case(driver,'D_fifo',owner='INVENTORY',gate='B0P_RERUN',post=lambda r,n:os.mkfifo(n.root/'owned_fifo'))
 for sub in ('stages/11_reference/stdout.txt','stages/11_reference/stderr.txt','stages/11_reference/subdir/stdout.txt','stages/11_reference/subdir/deeper/stderr.txt','inputs/stdout.txt'):
  case(driver,'L_'+sub.replace('/','_'),lambda r,n,sub=sub:[r.files.update({sub:('raw',b'one')}),n.files.update({sub:('raw',b'two')})],owner='BYTES_EQUAL',gate='B0P_RERUN')
 for digit in ('٠١','０１','0１'):
  case(driver,'N_unicode_'+str(ord(digit[0]))+'_'+str(ord(digit[-1])),owner='STAGE_SET',gate='B0P_RERUN',post=lambda r,n,digit=digit:(n.root/'stages'/(digit+'_extra')).mkdir())
for p in PINS:assert sha(p['path'])==p['sha256']
rep=dict(schema='CX2_C2V007_WHOLE_IDENTITY_V001',date_u=os.environ['CX2_DATE_U'],execution_note='nice unavailable (sandbox); 0514 waiver',source_pins=PINS,script=pin(__file__),source_before_after_equal=True,rows=rows,passed=sum(r['expectation_met'] for r in rows),total=len(rows),blocked_access_attempts=ATTEMPTS,fifo_open_attempts=FIFO_READS,scientific_launches=0,limitations=['Full comparator on wholly invented protocol fixtures; no scientific identity assertion.','Old own Tree reused, with complete synthetic identity fields/digests added independently. Protected root defaults replaced only with owned scratch.','All nonproduction comparisons use static driver/custody source pins; no actual run tree opened.'])
p=OUT/'RESULTS_WHOLE_IDENTITY.json';F.jfile(p,rep);print(json.dumps({'result':pin(p),'passed':rep['passed'],'total':rep['total'],'unexpected':[r['driver']+':'+r['name'] for r in rows if not r['expectation_met']]}))
