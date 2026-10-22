"""Own tiny whole-gate comparator canaries. Synthetic B0P trees; no actual runs read."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import contextlib,copy,datetime,hashlib,io,json,sys,types
from pathlib import Path
import numpy as np
P=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/gates_v005/run_identity_compare_c2v005.py');EXPECTED='6f656c68e51f457704dafd19c1a9e6b632e237f4959017ee376c18ad173b076b'
raw=P.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
M=types.ModuleType('_cx2_v5_whole_gate');M.__file__=str(P);sys.modules[M.__name__]=M;exec(compile(raw,str(P),'exec'),M.__dict__)
M.DRIVER[:]=list(M.DRIVERS['r5']);drv=M.load_driver()
D=Path(__file__).resolve().parent/'v005_whole_gate_v001';D.mkdir(exist_ok=False);rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,j,raw=False):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:f.write(j if raw else json.dumps(j,sort_keys=True,indent=1))
 return p
RO1=dict(rule='RO1',armed=False,fired=False,events=[],worker_sha256=None,binding_sha256=None)
def tree(root,tag,mutation=None):
 root.mkdir(parents=True)
 script=drv.SCRIPTS['body'];req=dict(name='body',kind='body',script=str(script[0]),script_sha256=script[1],argv=[])
 write(root/'stages/00_body/request.json',req)
 result=dict(status='COMPLETED',valid=True,driver_sha256=M.DRIVER[1],speeds_km_s={'synthetic':1.},route_a_outcome=dict(ro1=copy.deepcopy(RO1)),extra={'<RUN>/x':'same'})
 if mutation=='key_collision' and tag=='new':result['extra']={str(root)+'/x':'tampered','<RUN>/x':'same'}
 if mutation=='ordinary_result_change' and tag=='new':result['extra']['<RUN>/x']='tampered'
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
for name,should_pass in [('baseline',True),('ordinary_result_change',False),('ordinary_result_extra',False),('key_collision',False),('structured_npz',False),('structured_npy',False),('npz_storage_order',False),('npy_storage_order',False),('duplicate_json_key',False)]:
 d=D/name;ref=d/'ref';new=d/'new';tree(ref,'ref',name);tree(new,'new',name);tok=write(d/'tokens.json',{'declared':[]});out=d/'REPORT.json'
 with contextlib.redirect_stdout(io.StringIO()):code=M.main(['--driver','r5','--gate','B0P_RERUN','--reference',str(ref),'--new',str(new),'--tokens',str(tok),'--out',str(out)])
 rep=json.loads(out.read_bytes());actual=rep['verdict']=='PASS_BITWISE_EQUAL'
 rows.append(dict(name=name,should_pass=should_pass,actual_pass=actual,expectation_met=actual==should_pass,exit_code=code,failing=rep['failing'],report={'path':str(out),'sha256':sha(out)}))
assert sha(P)==EXPECTED
report=dict(schema='COMPARATOR_V005_WHOLE_GATE_SOURCE_CANARIES_CX2V001',status='TESTED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),execution_note='nice unavailable (sandbox); 0514 waiver',source={'path':str(P),'sha256':EXPECTED},script={'path':str(Path(__file__)),'sha256':sha(Path(__file__))},before_after_source_hash_equal=True,scope='Small whole-gate synthetic B0P trees; actual scientific run comparisons UNTESTED',scientific_launches=0,actual_run_reads=0,rows=rows)
p=D/'RESULTS.json'
with p.open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(dict(results=str(p),sha256=sha(p),rows=rows)))
