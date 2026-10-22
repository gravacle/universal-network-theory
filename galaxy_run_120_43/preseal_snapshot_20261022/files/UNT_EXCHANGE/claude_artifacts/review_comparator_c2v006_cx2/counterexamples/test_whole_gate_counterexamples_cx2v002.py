"""Own tiny whole-gate comparator canaries. Synthetic B0P trees; no actual runs read."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import contextlib,copy,datetime,hashlib,io,json,sys,types,warnings,zipfile,argparse
from pathlib import Path
import numpy as np
_g=Path(__file__).resolve().parent/'guard_cx2v001.py';_b=_g.read_bytes();assert hashlib.sha256(_b).hexdigest()=='b6c741172795a8ee2e769063a80faefc9795ee27b338ae0ab9990a620a7848a1';exec(compile(_b,str(_g),'exec'),globals())
ap=argparse.ArgumentParser();ap.add_argument('--driver',choices=('r4','r5'),required=True);a=ap.parse_args()
P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v006/run_identity_compare_c2v006.py');EXPECTED='097286d762dd171361e7ff5bbb98b3d48029e790de5869b28aa6218098491e48'
raw=P.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
M=types.ModuleType('_cx2_v5_whole_gate');M.__file__=str(P);sys.modules[M.__name__]=M;exec(compile(raw,str(P),'exec'),M.__dict__)
M.DRIVER[:]=list(M.DRIVERS[a.driver]);drv=M.load_driver()
D=Path(__file__).resolve().parent/('whole_gate_'+a.driver+'_v001');D.mkdir(exist_ok=False);rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,j,raw=False):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:f.write(j if raw else json.dumps(j,sort_keys=True,indent=1))
 return p
RO1=dict(rule='RO1',armed=False,fired=False,events=[],worker_sha256=None,binding_sha256=None)
def tree(root,tag,mutation=None,legacy=True):
 root.mkdir(parents=True)
 script=drv.SCRIPTS['body'];req=dict(name='body',kind='body',script=str(script[0]),script_sha256=script[1],argv=[])
 write(root/'stages/00_body/request.json',req)
 result=dict(status='COMPLETED',valid=True,driver_sha256=M.DRIVER[1],speeds_km_s={'synthetic':1.},route_a_outcome=dict(ro1=copy.deepcopy(RO1)),extra={('<RUN>/x' if legacy else 'plain/x'):'same'})
 if mutation=='key_collision' and tag=='ref' and not legacy:result['extra']={str(root)+'/x':'same'}
 if mutation=='key_collision' and tag=='new':result['extra']={str(root)+'/x':'tampered','<RUN>/x':'same'}
 if mutation=='ordinary_result_change' and tag=='new':result['extra']['<RUN>/x' if legacy else 'plain/x']='tampered'
 if mutation=='ordinary_result_extra' and tag=='new':result['extra']['extra_leaf']='tampered'
 if mutation=='duplicate_json_key' and tag=='new':
  text=json.dumps(result,sort_keys=True);text=text.replace('"valid": true','"valid": false, "valid": true');write(root/'result.json',text,raw=True)
 else:write(root/'result.json',result)
 write(root/'start.json',dict(driver=M.DRIVER[0],driver_sha256=M.DRIVER[1]))
 write(root/'finish.json',dict(status='COMPLETED',valid=True,result_path=str(root/'result.json'),result_sha256=sha(root/'result.json')))
 if mutation in ('structured_npz','structured_npy'):
  names=['radius','mass'] if tag=='ref' else ['speed','mass'];v=np.array([(1.,2.)],dtype=[(n,'<f8') for n in names]);suf=mutation.rsplit('_',1)[-1]
  with (root/('stages/00_body/state.'+suf)).open('xb') as f:
   if suf=='npz':np.savez(f,state=v)
   else:np.save(f,v,allow_pickle=False)
 if mutation=='npz_storage_order':
  v=np.array([[1.,2.],[3.,4.]],order='C' if tag=='ref' else 'F')
  with (root/'stages/00_body/state.npz').open('xb') as f:np.savez(f,state=v)
 if mutation=='npy_storage_order':
  v=np.array([[1.,2.],[3.,4.]],order='C' if tag=='ref' else 'F')
  with (root/'stages/00_body/state.npy').open('xb') as f:np.save(f,v,allow_pickle=False)
 if mutation=='duplicate_npz_member':
  good=io.BytesIO();np.save(good,np.array([1.,2.]),allow_pickle=False)
  bad=io.BytesIO();np.save(bad,np.array([900.,-123.]),allow_pickle=False)
  with (root/'stages/00_body/state.npz').open('xb') as f:
   with zipfile.ZipFile(f,'w') as z:
    if tag=='new':z.writestr('state.npy',bad.getvalue())
    with warnings.catch_warnings():
     warnings.simplefilter('ignore',UserWarning);z.writestr('state.npy',good.getvalue())

owners={'ordinary_result_change':'RESULT','ordinary_result_extra':'RESULT','key_collision':'NORM_INJECTIVE','structured_npz':'STAGES','structured_npy':'STAGES','npz_storage_order':'STAGES','npy_storage_order':'STAGES','duplicate_json_key':'STRICT_PARSE','duplicate_npz_member':'STRICT_PARSE'}
for legacy in (True,False):
 for name in ['baseline']+list(owners):
  tag=('exact_original' if legacy else 'clean_baseline')+'_'+name
  d=D/tag;ref=d/'ref';new=d/'new';tree(ref,'ref',name,legacy);tree(new,'new',name,legacy)
  tok=write(d/'tokens.json',{'declared':[]});out=d/'REPORT.json'
  with contextlib.redirect_stdout(io.StringIO()):code=M.main(['--driver',a.driver,'--gate','B0P_RERUN','--reference',str(ref),'--new',str(new),'--tokens',str(tok),'--out',str(out)])
  rep=json.loads(out.read_bytes());actual=rep['verdict']=='PASS_BITWISE_EQUAL'
  should_pass=name=='baseline' and not legacy
  owner=owners.get(name,'NORM_INJECTIVE' if legacy else None)
  own=rep['checks'].get(owner,{}) if owner else {}
  owner_ok=(owner is None or own.get('pass') is False)
  if name=='key_collision':
   owner_ok=owner_ok and any(x.get('kind')=='KEY_COLLISION' and set(x.get('raw_keys',[]))=={str(new)+'/x','<RUN>/x'} for x in own.get('detail',{}).get('new',[]))
  if name=='duplicate_json_key':owner_ok=owner_ok and 'DUPLICATE_JSON_KEY' in json.dumps(own)
  if name=='duplicate_npz_member':owner_ok=owner_ok and 'DUPLICATE_NPZ_MEMBER' in json.dumps(own)
  if name=='baseline' and legacy:owner_ok=owner_ok and rep['failing']==['NORM_INJECTIVE']
  # Clean controls must not carry the unrelated reserved-marker defect.
  clean_ok=legacy or name=='key_collision' or rep['checks'].get('NORM_INJECTIVE',{}).get('pass') is True
  ok=actual==should_pass and owner_ok and clean_ok and 'COMPARATOR_EXCEPTION' not in rep['failing']
  rows.append(dict(name=tag,should_pass=should_pass,actual_pass=actual,expectation_met=ok,exit_code=code,owner=owner,owner_detail=own,failing=rep['failing'],clean_norm_ok=clean_ok,report={'path':str(out),'sha256':sha(out)}))
assert sha(P)==EXPECTED
report=dict(schema='COMPARATOR_V006_INDEPENDENT_COUNTEREXAMPLES_CX2V001',status='TESTED',date_u=os.environ.get('CX2_DATE_U'),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),execution_note='nice unavailable (sandbox); 0514 waiver',source={'path':str(P),'sha256':EXPECTED},script={'path':str(Path(__file__)),'sha256':sha(Path(__file__))},selected_driver=a.driver,before_after_source_hash_equal=True,scope='Original 0553 source-audit fixture logic with exact-original and clean-key controls. No builder port imported. Actual scientific run comparisons UNTESTED',scientific_launches=0,actual_run_reads=0,rows=rows,passed=sum(r['expectation_met'] for r in rows),total=len(rows),blocked_attempts=AUDIT_BLOCKED)
p=D/'RESULTS.json'
with p.open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(dict(results=str(p),sha256=sha(p),passed=report['passed'],total=report['total'],unexpected=[r for r in rows if not r['expectation_met']])))
