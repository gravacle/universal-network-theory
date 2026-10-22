"""Independent narrow comparator probes; synthetic inputs only, no full-run verdict claims."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import argparse,datetime,hashlib,json,sys,types
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--module',required=True);ap.add_argument('--tag',required=True);a=ap.parse_args()
P=Path(a.module);raw=P.read_bytes();module_sha=hashlib.sha256(raw).hexdigest();M=types.ModuleType('_source_probe_'+a.tag);M.__file__=str(P);sys.modules[M.__name__]=M;exec(compile(raw,str(P),'exec'),M.__dict__)
D=Path(__file__).resolve().parent/a.tag;D.mkdir(exist_ok=False);rows=[]
def record(name,expected,actual,scope='helper contract'):
 rows.append(dict(name=name,expected=expected,observed=actual,contract_pass=(expected==actual),scope=scope))
def write(p,j):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(j,f,sort_keys=True)
 return p
# Different structured dtype field names are part of dtype identity.
x=np.array([(1.,2.)],dtype=[('radius','<f8'),('mass','<f8')]);y=np.array([(1.,2.)],dtype=[('speed','<f8'),('mass','<f8')])
for suffix,loader in [('npz',M.npz_members),('npy',M.npy_member)]:
 paths=[]
 for k,v in [('x',x),('y',y)]:
  p=D/(k+'.'+suffix)
  with p.open('xb') as f:
   if suffix=='npz':np.savez(f,state=v)
   else:np.save(f,v,allow_pickle=False)
  paths.append(p)
 record('structured_dtype_fields_'+suffix,False,loader(paths[0])==loader(paths[1]))
# Storage-order identity is explicitly advertised in predecessor's docstring.
x=np.array([[1.,2.],[3.,4.]],order='C');y=np.array(x,order='F')
for suffix,loader in [('npz',M.npz_members),('npy',M.npy_member)]:
 paths=[]
 for k,v in [('c',x),('f',y)]:
  p=D/(k+'.'+suffix)
  with p.open('xb') as f:
   if suffix=='npz':np.savez(f,state=v)
   else:np.save(f,v,allow_pickle=False)
  paths.append(p)
 record('storage_order_'+suffix,False,loader(paths[0])==loader(paths[1]))
# A many-to-one normalization must not silently erase a changed source key.
r=D/'tokens';r.mkdir();side=M.Side(r,[('custody_A','<PIN>'),('custody_B','<PIN>')])
try:
 aa=side.norm({'custody_A':'original','custody_B':'same'});bb=side.norm({'custody_A':'tampered','custody_B':'same'})
 record('normalized_dict_key_collision',False,M.seq(aa,bb))
except BaseException as exc:record('normalized_dict_key_collision',False,False,'refused '+str(exc))
# Declared argv duplicate first value cannot be silently discarded.
argv=['--uv-tail-config','/untrusted/first','--uv-tail-config','<RUN>/expected.json']
try:
 rest,removed=M.split_declared_argv(argv,{'--uv-tail-config':True})
 record('duplicate_tail_flag_first_value_lost',False,rest==[] and removed=={'--uv-tail-config':'<RUN>/expected.json'})
except BaseException as exc:record('duplicate_tail_flag_first_value_lost',False,False,'refused '+str(exc))
record('tail_truncation_boolean_shape',False,M.declared_value_ok('--uv-tail-truncation','false',True))
record('tail_truncation_number_shape',False,M.declared_value_ok('--uv-tail-truncation','13',True))
# Distinct physical stage directories must remain detectable, even empty ones.
r=D/'collision';(r/'stages/01_body').mkdir(parents=True);(r/'stages/99_body').mkdir()
try:record('stage_dictionary_collision',2,len(M.stage_dirs(r)))
except BaseException as exc:record('stage_dictionary_collision',2,2,'refused '+str(exc))
write(r/'stages/01_body/data.json',{'value':1});write(r/'stages/99_body/data.json',{'value':2})
try:record('inventory_dictionary_collision',2,len(M.inventory(r)))
except BaseException as exc:record('inventory_dictionary_collision',2,2,'refused '+str(exc))
# Strict scalar controls establish that intended primitive masking is discriminating.
for name,x,y,want in [('signed_zero',0.,-0.,False),('int_float',1,1.,False),('bool_int',True,1,False),('equal_float',1.5,1.5,True)]:record(name,want,M.seq(x,y))
report=dict(schema='COMPARATOR_COMPONENT_SOURCE_PROBES_CX2V001',status='TESTED',scope='Helper-level synthetic canaries, not end-to-end identity verdicts',module={'path':str(P),'sha256':module_sha},script={'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),execution_note='nice unavailable (sandbox); 0514 waiver',actual_run_reads=0,scientific_launches=0,rows=rows)
p=D/'PROBES.json'
with p.open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(dict(report=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),contract_failures=[r['name'] for r in rows if not r['contract_pass']],total=len(rows))))
