"""Guarded saved-iterate residual refinement; original canonical targets unchanged."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V002'
FAILED_STEM='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001'
MAX_CYCLES=3;RESTART_CAP=160
RECOVERY=None
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='0f963eb60621fdf2efd28ef58f2931387ef7b168540ecfd71b79443ae332e05d'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
SIGMA=1.;C=1.98;TOL=2e-11;LINEAR_TOL=1e-10;CAP=600;BASE_CONTROLS=18
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(canonical_rate_physical=False,CMC_preservation_qualified=False,full_constraints_qualified=False,physical_metric_qualified=False,source_history_qualified=False,exterior_qualified=False,galaxy_velocity_qualified=False)
PINS={'CROSS_U_CANONICAL_NODAL_METRIC_RATE_ADMISSION_V001.md': '2aeab0e5845b673576eafe635693db0494e3f352b439cbee9310bf7c78c32b95', 'cross_u_weak_nodal_metric_temporal_cmc_v001.py': 'e11bb7ec123971998fbdd64d1e2171627aae9202804d1c625202f412b5f85b6c', 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001.md': '60de28cc558734f648fc3845ebf18ab47b10f0cf9d06a89142e59268951baf7a', 'READONLY_CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_SAVED_AUDIT.json': 'a3066b6cf48187e3fd577672aeeb89e03aa9174a6fb520f6bbdf018132cf2781', 'cross_u_weak_nodal_native_legendre_v001.py': 'e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001.md': '2c9da869068cf3d2ae9269395b111ec1d0e71f26e0ffef6ff0afb50e40995a0e', 'READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json': 'af16bda38df395882c54ca2b57bd7d9ed36cc3aae39b437687bc35930423d56d', 'cross_u_weak_canonical_spatial_euler_loads_v003.py': '4f239074b5345709f493b3633f7dd376fa7ac97dbb23bf20825eabde2ed56b79', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003.md': 'de6ae873e7cf783c4bdfbc20eeb0d5de82c27ea7dc709ba8832ed4c4ec7aba2b', 'READONLY_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_SAVED_AUDIT.json': '80b7fac6e83d178bc2eb706853d301bbf258e0fe9f22caa0423e28010eac66e2', 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RESULT.json': '2210b4993989d6cb432d9981cc8819f1c21c394ded9d349f6d34b009adb92528', 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RECEIPT.json': 'f74d4d67ba87838b4902dc53eebd38812c9b723870ef57528144a7b3a22151cf', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json': 'e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RECEIPT.json': '00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RESULT.json': '981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_RECEIPT.json': '822c82d59631ebef6f87c0847829370792338a1dcb741c325843d1c8f07e3af2', 'authoring_cross_u_canonical_nodal_metric_rate_solve_v001_567_4a6529b7.py': '4a6529b77ae5800228d0fb8123dda14d614c1ae48602e4d151ccbeedd1c31171', 'authoring_CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_567_4c363396.md': '4c3633968ea7500aeb56a1fc16e1639fdde773f5b48e8c3221cd2551a8e7d1a8', 'READONLY_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_567_STATIC_REVIEW.json': '914c4e46cf117d44289236bdef7c43fa855b52a71bd2c833a4b2b037852bee19'}
PARENTS=[{'stem': 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001', 'pid': 30671, 'controls': 49, 'result_sha256': '2210b4993989d6cb432d9981cc8819f1c21c394ded9d349f6d34b009adb92528', 'receipt_sha256': 'f74d4d67ba87838b4902dc53eebd38812c9b723870ef57528144a7b3a22151cf'}, {'stem': 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001', 'pid': 28469, 'controls': 21, 'result_sha256': 'e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5', 'receipt_sha256': '00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae'}, {'stem': 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003', 'pid': 36387, 'controls': 36, 'result_sha256': '981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770', 'receipt_sha256': '822c82d59631ebef6f87c0847829370792338a1dcb741c325843d1c8f07e3af2'}]

def now():return datetime.now(timezone.utc).isoformat()

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Unsupported/nonfinite metadata '+type(v).__name__)

def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def publish(n,raw):
 p=path(n)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;OUTPUTS[n]=sha(p);return OUTPUTS[n]

def json_file(n,v):return publish(n,encode(v))

def check(label,actual,expected,envelope):
 a=np.asarray(actual);b=np.asarray(expected);e=np.asarray(envelope);k=len(CHECKS)
 CONTEXT.update(control=label,ordinal=k)
 for n,v in (('actual',a),('expected',b),('envelope',e)):RAW[f'control_{k:03d}_{label}_{n}']=v.copy()
 assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));row=dict(ordinal=k,name=label,error=error,tolerance=TOL,passed=error<=TOL);CHECKS.append(row)
 assert row['passed'],(label,error)

def checkpoint(tag,arrays,meta,failed=False):
 schema={}
 for k,a in arrays.items():
  assert isinstance(a,np.ndarray) and a.dtype.kind in 'fiub'
  finite=bool(np.all(np.isfinite(a)));assert failed or finite,k
  schema[k]=dict(shape=list(a.shape),dtype=str(a.dtype),finite=finite)
 md=json.loads(encode(dict(meta,owner=OWNER,qualification=FLAGS,schema=schema,failed=failed)).decode())
 text=encode(md).decode();name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);OUTPUTS[name]=sha(p);rec=dict(file=name,sha256=OUTPUTS[name],metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert str(f['metadata_json'])==text and set(f.files)==set(arrays)|{'metadata_json'}
  for k,a in arrays.items():assert f[k].shape==a.shape and f[k].dtype==a.dtype and np.array_equal(f[k],a,equal_nan=True),k
 return rec

def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('input changed',n)
 assert sha(__file__)==OWNER['source_sha256']
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for n,s in r['metadata']['schema'].items():assert list(f[n].shape)==s['shape'] and str(f[n].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[n])))==s['finite']
 if strict:
  assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}

def seal_actual():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)

def read_pair(rec,names):
 assert sha(path(rec['file']))==rec['sha256'] and sha(path(rec['commit_file']))==rec['commit_sha256']
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={};metadata_key='metadata' if rec['file'].startswith(BAND+'_') else 'metadata_json'
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{metadata_key}
  assert json.loads(str(f[metadata_key]))==rec['metadata']
  for n in names:
   a=f[n].copy();RAW['loaded_'+n]=a
   s=rec['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a)),n
   out[n]=a
 return out

def resolve_record(ref):
 assert sha(path(ref['file']))==ref['sha256'] and sha(path(ref['commit_file']))==ref['commit_sha256']
 out=json.loads(path(ref['commit_file']).read_text())
 assert out['file']==ref['file'] and out['sha256']==ref['sha256']
 return dict(out,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def capture(name,a):
 AVAILABLE[name]=a.copy();return a

def finite_real(name,a):
 capture(name,a);assert a.dtype.kind=='f' and np.all(np.isfinite(a)),name
 return a

def native_mask():
 m=np.ones((3,87,45),dtype=bool);m[:,0]=False;m[1,:,0]=False;return m

def lift_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,0,0,:]=0;y[...,1,0,:]=y[...,1,1,:];y[...,1,:,0]=0;y[...,2,0,:]=y[...,2,1,:];return y

def restrict_velocity(x):
 assert x.shape[-3:]==(3,87,45)
 y=x.copy();y[...,1,1,:]+=y[...,1,0,:];y[...,2,1,:]+=y[...,2,0,:];y[..., :,0,:]=0;y[...,1,:,0]=0;return y

def evaluate_velocity(x,geo,jet=0):
 # Covector phi value R²N; radial derivative is 2RN+R²NR.
 y=lift_velocity(x);out=np.zeros(x.shape[:-3]+(4,86,44,3))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   h=geo['hats'][iq,a,jet];factor=np.broadcast_to(h[...,None],(86,44,3)).copy();factor[...,2]=R**2*h
   if jet==1:factor[...,2]+=2*R*geo['hats'][iq,a,0]
   out[...,iq,:,:,:]+=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)*factor
 return out.reshape(x.shape[:-3]+(15136,3))

def scatter_velocity(field,geo):
 assert field.shape[-2:]==(15136,3)
 f=field.reshape(field.shape[:-2]+(4,86,44,3));out=np.zeros(field.shape[:-2]+(3,87,45))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);wq=geo['dv'][iq].reshape(86,44)/R
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   factor=np.broadcast_to(geo['hats'][iq,a,0][...,None],(86,44,3)).copy();factor[...,2]*=R**2
   out[..., :,i:86+i,j:44+j]+=np.moveaxis(f[...,iq,:,:,:]*wq[...,None]*factor,-1,-3)
 return restrict_velocity(out)

def scatter_velocity_independent(field,geo):
 out=np.zeros(field.shape[:-2]+(3,87,45));prefix=field.shape[:-2];groups=int(math.prod(prefix)) if prefix else 1;fo=field.reshape(groups,15136,3);oo=out.reshape(groups,3,87,45)
 for iq in range(4):
  R=geo['R'][iq];wq=geo['dv'][iq]/R;f=fo[:,iq*3784:(iq+1)*3784]
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for c in range(3):
    scale=R**2 if c==2 else np.ones_like(R)
    val=f[...,c]*wq*geo['hats'][iq,a,0].reshape(3784)*scale
    for k in range(groups):np.add.at(oo[k,c],(geo['cell_i']+i,geo['cell_j']+j),val[k])
 return restrict_velocity(out)

def point_action(v,b):
 mixed=v[1:]+np.einsum('jpik,pk->jpi',b['L'],v[0],optimize=True);modes=np.einsum('jpik,jpk->jpi',b['D'],mixed,optimize=True)
 U=np.einsum('pik,pk->pi',b['M0'],v[0],optimize=True)+np.einsum('jpki,jpk->pi',b['L'],modes,optimize=True)
 return np.concatenate((U[None],modes))

def point_action_envelope(v,b):
 mixed=abs(v[1:])+np.einsum('jpik,pk->jpi',b['eL'],abs(v[0]),optimize=True);modes=np.einsum('jpik,jpk->jpi',b['eD'],mixed,optimize=True)
 U=np.einsum('pik,pk->pi',b['eM0'],abs(v[0]),optimize=True)+np.einsum('jpki,jpk->pi',b['eL'],modes,optimize=True)
 return np.concatenate((U[None],modes))

def original_action(x,b,g):return scatter_velocity(point_action(evaluate_velocity(x,g),b),g)

def original_envelope(x,b,g):return scatter_velocity(point_action_envelope(evaluate_velocity(abs(x),g),b),g)

def metric_mask():
 m=np.ones((6,87,45),dtype=bool);m[:,0]=False;m[3:5,:,0]=False;return m

def lift_metric(x):
 assert x.shape[-3:]==(6,87,45)
 y=x.copy();y[..., :,0,:]=y[..., :,1,:];y[...,3:5,:,0]=0;return y

def restrict_metric(x):
 assert x.shape[-3:]==(6,87,45)
 y=x.copy();y[..., :,1,:]+=y[..., :,0,:];y[..., :,0,:]=0;y[...,3:5,:,0]=0;return y

def metric_value_matrix(R):
 # Physical local order RR,ZZ,phiphi,RZ,Rphi,Zphi. Coefficient order a,b,c,d,e,f.
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 return F

def metric_R_matrix(R):
 F=np.zeros(R.shape+(6,6));F[...,0,1]=2*R;F[...,2,0]=2*R;F[...,3,3]=1;F[...,4,2]=3*R**2;F[...,5,4]=2*R
 return F

def evaluate_metric(x,geo,jet=0):
 y=lift_metric(x);out=np.zeros(x.shape[:-3]+(4,86,44,6))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);F=metric_value_matrix(R)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   h=geo['hats'][iq,a,jet];factor=h[...,None,None]*F
   if jet==1:factor+=geo['hats'][iq,a,0][...,None,None]*metric_R_matrix(R)
   vals=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)
   out[...,iq,:,:,:]+=np.einsum('...ijb,ijab->...ija',vals,factor,optimize=True)
 return out.reshape(x.shape[:-3]+(15136,6))

def scatter_metric(field,geo):
 assert field.shape[-2:]==(15136,6)
 f=field.reshape(field.shape[:-2]+(4,86,44,6));out=np.zeros(field.shape[:-2]+(6,87,45))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44);F=metric_value_matrix(R)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   val=np.einsum('...ija,ijab->...ijb',f[...,iq,:,:,:],F,optimize=True)*wq[...,None]*geo['hats'][iq,a,0][...,None]
   out[..., :,i:86+i,j:44+j]+=np.moveaxis(val,-1,-3)
 return restrict_metric(out)

def scatter_metric_independent(field,geo):
 out=np.zeros(field.shape[:-2]+(6,87,45));prefix=field.shape[:-2];ng=int(math.prod(prefix)) if prefix else 1;fo=field.reshape(ng,15136,6);oo=out.reshape(ng,6,87,45)
 for iq in range(4):
  R=geo['R'][iq];F=metric_value_matrix(R);wq=geo['dv'][iq]/R;f=fo[:,iq*3784:(iq+1)*3784]
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for c in range(6):
    val=np.sum(f*F[:, :,c][None],axis=-1)*wq*geo['hats'][iq,a,0].reshape(3784)
    for k in range(ng):np.add.at(oo[k,c],(geo['cell_i']+i,geo['cell_j']+j),val[k])
 return restrict_metric(out)

def scalar_lift(x):
 assert x.shape[-2:]==(87,45)
 y=x.copy();y[...,0,:]=y[...,1,:];return y

def scalar_scatter(field,geo):
 assert field.shape[-1]==15136
 f=field.reshape(field.shape[:-1]+(4,86,44));out=np.zeros(field.shape[:-1]+(87,45))
 for iq in range(4):
  wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):out[...,i:86+i,j:44+j]+=wq*geo['hats'][iq,a,0]*f[...,iq,:,:]
 out[...,1,:]+=out[...,0,:];out[...,0,:]=0;return out

def point_metric_tensor(k):
 # k represents a symmetric metric VELOCITY; offdiagonal k values are actual hdot_ij.
 out=np.zeros(k.shape[:-1]+(3,3));out[...,0,0]=k[...,0];out[...,1,1]=k[...,1];out[...,2,2]=k[...,2]
 for a,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):out[...,i,j]=out[...,j,i]=k[...,a]
 return out

def tensor_velocity_coordinates(hdot):
 return np.stack((hdot[...,0,0],hdot[...,1,1],hdot[...,2,2],hdot[...,0,1],hdot[...,0,2],hdot[...,1,2]),axis=-1)

def trace_CMC_actions(k,ih,N,mu,g):
 tensor=point_metric_tensor(k);tr=np.einsum('pij,...pij->...p',ih,tensor,optimize=True)/(2*N)
 return scalar_scatter(mu*tr,g)

def admission():
 pins={str(path(n).resolve()):h for n,h in PINS.items()};parents={}
 for n,h in pins.items():assert sha(path(n))==h,('direct input changed',n)
 for spec in PARENTS:
  stem=spec['stem'];result=json.loads(path(stem+'_RESULT.json').read_text());rc=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['closed']>rc['owner']['started'] and rc['owner']==result['owner']
  assert rc['owner']['owner']=='root' and rc['owner']['pid']==spec['pid'] and rc['result_sha256']==spec['result_sha256'] and rc.get('error_sha256') is None
  assert len(result['controls'])==spec['controls'] and all(x['passed'] for x in result['controls']) and all(v is False for v in result['qualification'].values())
  for mapping in (rc['input_sha256'],rc['output_sha256']):
   for n,h in mapping.items():
    key=str(path(n).resolve());assert key not in pins or pins[key]==h;assert sha(path(n))==h;pins[key]=h
  for ref in result['checkpoints']:
   assert rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
   assert resolve_record(ref)==ref and ref['metadata']['owner']==rc['owner'] and ref['metadata']['failed'] is False
  assert {p.name for p in BASE.glob(stem+'_*.npz')}=={r['file'] for r in result['checkpoints']}
  assert {p.name for p in BASE.glob(stem+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in result['checkpoints']}
  parents[stem]=result
 for n in ('READONLY_CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_SAVED_AUDIT.json','READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json','READONLY_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_SAVED_AUDIT.json'):
  audit=json.loads(path(n).read_text());assert audit['status']=='SAVED_PACKET_AUDIT_PASS'
 return pins,parents

def unique_record(result,kind):
 rows=[r for r in result['checkpoints'] if r['metadata']['kind']==kind];assert len(rows)==1;return rows[0]

def require_schema(rec,spec):
 for name,shape in spec.items():assert rec['metadata']['schema'][name]==dict(shape=list(shape),dtype='float64',finite=True),(rec['file'],name)

def load_saved_system(parents):
 metric=parents[PARENTS[0]['stem']];weak=parents[PARENTS[1]['stem']];force=parents[PARENTS[2]['stem']]
 mr=metric['cases'][0];fr=force['cases'][0];assert mr['sigma']==fr['sigma']==1.
 geometry=unique_record(weak,'genuine_affine_native_temporal_basis');gr=read_pair(geometry,('geometry_R','geometry_dv','geometry_hats','geometry_cell_i','geometry_cell_j','native_independent_mask','r_kpc','z_kpc'))
 g=dict(R=gr['geometry_R'],dv=gr['geometry_dv'],hats=gr['geometry_hats'],cell_i=gr['geometry_cell_i'],cell_j=gr['geometry_cell_j'],r=gr['r_kpc'],z=gr['z_kpc'])
 assert g['R'].shape==g['dv'].shape==(4,3784) and np.all(g['R']>0) and np.all(g['dv']>0) and g['hats'].shape==(4,4,3,86,44)
 assert np.array_equal(gr['native_independent_mask'],native_mask())
 coeff=unique_record(weak,'complete_fixed_metric_native99_mass_coefficients')
 nr=('mixing_L','modal_D','Maxwell_M0','operation_eL','operation_eD','operation_eM0','input_g','input_U','input_z')
 nc=read_pair(coeff,nr);b=dict(L=nc['mixing_L'],D=nc['modal_D'],M0=nc['Maxwell_M0'],eL=nc['operation_eL'],eD=nc['operation_eD'],eM0=nc['operation_eM0'])
 pre=read_pair(unique_record(weak,'preconditioner_only_positive_node_block'),('kinetic_congruence_scale',));native_scale=pre['kinetic_congruence_scale']
 assert native_scale.shape==(33,3,87,45) and np.all(native_scale>0)
 chunks=[]
 for iq,(mc,fc) in enumerate(zip(mr['columns'],fr['columns'])):
  CONTEXT.update(stage='saved_current_canonical_column',column=iq)
  mn=('B','B_envelope','T_total','T_total_envelope','current_ih','current_N','current_sqrt_h','saved_Lie_beta_h','saved_Lie_beta_h_envelope')
  require_schema(mc,dict(B=(3784,99,6),B_envelope=(3784,99,6),T_total=(3784,6,6),T_total_envelope=(3784,6,6),current_ih=(3784,3,3),current_N=(3784,),current_sqrt_h=(3784,)))
  m=read_pair(mc,mn)
  fn=('seed_g','seed_U','seed_z','seed_chart_ih','seed_chart_N','seed_chart_sqrt_h','seed_chart_Ktrace','seed_nodal_native_rate','seed_metric_L2_rate','new_native_momentum','new_metric_total_momentum')
  require_schema(fc,dict(seed_g=(3784,4,4),seed_U=(3784,4),seed_z=(32,3784,4),seed_nodal_native_rate=(3784,99),seed_metric_L2_rate=(3784,3,3),new_native_momentum=(3784,99),new_metric_total_momentum=(3784,6)))
  f=read_pair(fc,fn);sl=slice(iq*3784,(iq+1)*3784)
  assert np.array_equal(f['seed_g'],nc['input_g'][sl]) and np.array_equal(f['seed_U'],nc['input_U'][sl]) and np.array_equal(f['seed_z'],nc['input_z'][:,sl])
  for a,z in (('current_ih','seed_chart_ih'),('current_N','seed_chart_N'),('current_sqrt_h','seed_chart_sqrt_h')):assert np.array_equal(m[a],f[z]),(iq,a)
  v=f['seed_nodal_native_rate'];k=tensor_velocity_coordinates(f['seed_metric_L2_rate']);p=f['new_native_momentum'];pi=f['new_metric_total_momentum']
  mv=point_action(v.reshape(3784,33,3).transpose(1,0,2),{n:a[:,sl] if n in ('L','D','eL','eD') else a[sl] for n,a in b.items()}).transpose(1,0,2).reshape(3784,99);capture('current_M_vstar',mv)
  emv=point_action_envelope(abs(v).reshape(3784,33,3).transpose(1,0,2),{n:a[:,sl] if n in ('L','D','eL','eD') else a[sl] for n,a in b.items()}).transpose(1,0,2).reshape(3784,99);capture('current_M_vstar_envelope',emv)
  bk=np.einsum('pia,pa->pi',m['B'],k,optimize=True);capture('current_B_kstar',bk)
  bt=np.einsum('pia,pi->pa',m['B'],v,optimize=True);capture('current_BT_vstar',bt)
  tk=np.einsum('pab,pb->pa',m['T_total'],k,optimize=True);capture('current_T_kstar',tk)
  cn=p-mv-bk;capture('current_native_affine_offset',cn);cm=pi-bt-tk;capture('current_metric_affine_offset',cm)
  en=abs(p)+emv+np.einsum('pia,pa->pi',m['B_envelope'],abs(k),optimize=True)
  em=abs(pi)+np.einsum('pia,pi->pa',m['B_envelope'],abs(v),optimize=True)+np.einsum('pab,pb->pa',m['T_total_envelope'],abs(k),optimize=True)
  capture('current_native_affine_envelope',en);capture('current_metric_affine_envelope',em)
  check(f'current_q{iq}_native_affine_reconstruction',cn+mv+bk,p,en+abs(cn))
  check(f'current_q{iq}_metric_affine_reconstruction',cm+bt+tk,pi,em+abs(cm))
  c=dict(B=m['B'],eB=m['B_envelope'],T=m['T_total'],eT=m['T_total_envelope'],ih=m['current_ih'],N=m['current_N'],mu=m['current_sqrt_h'],lie=m['saved_Lie_beta_h'],elie=m['saved_Lie_beta_h_envelope'],vstar=v,kstar=k,pstar=p,pistar=pi,cn=cn,cm=cm,ecn=en,ecm=em,Kstar=f['seed_chart_Ktrace'])
  checkpoint('COLUMN',dict(c,**{n:a for n,a in RAW.items() if n.startswith('control_')}),dict(kind='copied_signed_blocks_and_current_actual_affine_reference',column=iq,metric_parent=mc,force_parent=fc,kinetic_law_replayed=False,ordinary_pdot=None,physical_change=False));chunks.append(c);RAW.clear();AVAILABLE.clear()
 data={n:np.concatenate([c[n] for c in chunks]) for n in chunks[0]}
 inputrec=force['checkpoints'][0];fixed=inputrec['metadata']['fixed'];bg=inputrec['metadata']['owned_background'];assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 Hbar=fixed['Hunit']/299792458.*bg['h'];assert math.isfinite(Hbar) and Hbar>0
 d=scalar_scatter(data['mu']*(3*Hbar-data['Kstar']),g)+trace_CMC_actions(data['kstar'],data['ih'],data['N'],data['mu'],g)
 expected=scalar_scatter(data['mu']*(3*Hbar+np.einsum('pij,pij->p',data['ih'],data['lie'])/(2*data['N'])),g)
 den=scalar_scatter(data['mu']*(6*Hbar+abs(data['Kstar'])+np.einsum('pij,pij->p',abs(data['ih']),abs(point_metric_tensor(data['kstar']))+data['elie'])/(2*data['N'])),g)
 check('current_CMC_rhs_saved_Lie_identity',d,expected,den)
 nn=data['pstar'].reshape(15136,33,3).transpose(1,0,2);cc=data['cn'].reshape(15136,33,3).transpose(1,0,2)
 targets=dict(Pn=scatter_velocity(nn,g),Pm=scatter_metric(data['pistar'],g),cn=scatter_velocity(cc,g),cm=scatter_metric(data['cm'],g),trace_rhs=d)
 for n,a in targets.items():finite_real(n,a)
 checkpoint('AFFINE',dict(targets,**{n:a for n,a in RAW.items() if n.startswith('control_')}),dict(kind='actual_current_weak_targets_and_owned_H_trace_rhs',Hbar=Hbar,native_target='actual force V003',metric_target='actual force V003',old_targets_adopted=False,outer_trace='free instantaneous coefficients; no physical wall',history=None))
 data['target_Pn']=targets['Pn'];data['target_Pm']=targets['Pm']
 return g,b,data,targets,native_scale

def scalar_evaluate(x,g):
 y=scalar_lift(x);out=np.zeros((4,86,44))
 for iq in range(4):
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):out[iq]+=g['hats'][iq,a,0]*y[di:86+di,dj:44+dj]
 return out.reshape(15136)

def trace_forward(k,d,g):return trace_CMC_actions(evaluate_metric(k,g),d['ih'],d['N'],d['mu'],g)

def trace_adjoint(lam,d,g):
 sv=scalar_evaluate(lam,g);ih=d['ih'];t=np.stack((ih[:,0,0],ih[:,1,1],ih[:,2,2],2*ih[:,0,1],2*ih[:,0,2],2*ih[:,1,2]),axis=-1)
 return scatter_metric(t*(d['mu']*sv/(2*d['N']))[:,None],g)

def trace_forward_envelope(k,d,g):
 tensor=abs(point_metric_tensor(evaluate_metric(abs(k),g)));tr=np.einsum('pij,pij->p',abs(d['ih']),tensor,optimize=True)/(2*d['N'])
 return scalar_scatter(d['mu']*tr,g)


def trace_adjoint_envelope(lam,d,g):
 sv=scalar_evaluate(abs(lam),g);ih=abs(d['ih']);t=np.stack((ih[:,0,0],ih[:,1,1],ih[:,2,2],2*ih[:,0,1],2*ih[:,0,2],2*ih[:,1,2]),axis=-1)
 return scatter_metric(t*(d['mu']*sv/(2*d['N']))[:,None],g)


def coupled_action(v,k,b,d,g):
 vp=evaluate_velocity(v,g);kv=evaluate_metric(k,g);vf=vp.transpose(1,0,2).reshape(15136,99)
 bk=np.einsum('pia,pa->pi',d['B'],kv,optimize=True).reshape(15136,33,3).transpose(1,0,2)
 n=scatter_velocity(point_action(vp,b)+bk,g)
 m=scatter_metric(np.einsum('pia,pi->pa',d['B'],vf,optimize=True)+np.einsum('pab,pb->pa',d['T'],kv,optimize=True),g)
 return n,m

def coupled_envelope(v,k,b,d,g):
 vp=abs(evaluate_velocity(abs(v),g));kv=abs(evaluate_metric(abs(k),g))
 # Metric R powers and value hats are nonnegative; all cancellation is bounded upstream.
 vf=vp.transpose(1,0,2).reshape(15136,99);bk=np.einsum('pia,pa->pi',d['eB'],kv,optimize=True).reshape(15136,33,3).transpose(1,0,2)
 n=scatter_velocity(point_action_envelope(vp,b)+bk,g)
 m=scatter_metric(np.einsum('pia,pi->pa',d['eB'],vf,optimize=True)+np.einsum('pab,pb->pa',d['eT'],kv,optimize=True),g)
 return n,m

def scalar_mask():
 mask=np.ones((87,45),dtype=bool);mask[0]=False;return mask

def pack_fields(v,k,lam=None):
 out=[v[np.broadcast_to(native_mask(),v.shape)],k[metric_mask()]]
 if lam is not None:out.append(lam[scalar_mask()])
 return np.concatenate(out)

def unpack_fields(x,constrained):
 nv=380292;nk=23048;assert len(x)==nv+nk+(3870 if constrained else 0)
 v=np.zeros((33,3,87,45));k=np.zeros((6,87,45));v[np.broadcast_to(native_mask(),v.shape)]=x[:nv];k[metric_mask()]=x[nv:nv+nk]
 lam=None
 if constrained:lam=np.zeros((87,45));lam[scalar_mask()]=x[nv+nk:]
 return v,k,lam

def system_action(x,b,d,g,constrained):
 v,k,lam=unpack_fields(x,constrained);n,m=coupled_action(v,k,b,d,g)
 if constrained:m+=trace_adjoint(lam,d,g);q=trace_forward(k,d,g)
 else:q=None
 return pack_fields(n,m,q)
def positive_scales(ns,d,g):
 # Positive proper-tensor mass congruence; no modification of signed T or targets.
 F=metric_value_matrix(g['R'].reshape(15136)).transpose(0,2,1);t=point_metric_tensor(F);ih=d['ih']
 q=np.einsum('paij,pjk,pakl,pli->pa',t,ih,t,ih,optimize=True)*d['mu'][:,None]
 eq=np.einsum('paij,pjk,pakl,pli->pa',abs(t),abs(ih),abs(t),abs(ih),optimize=True)*d['mu'][:,None]
 capture('proper_metric_point_diagonal',q);capture('proper_metric_point_diagonal_envelope',eq);assert np.all(q>0) and np.all(np.isfinite(q))
 out=np.zeros((6,87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   # Axis tied coefficients require both row contributions; this positive
   # diagonal is a congruence only, not the physical kinetic diagonal.
   val=q[sl].reshape(86,44,6)*weight[:,:,None]*g['hats'][iq,a,0][:,:,None]**2
   out[:,di:86+di,dj:44+dj]+=val.transpose(2,0,1)
 out=restrict_metric(out);ms=np.ones_like(out);ms[metric_mask()]=np.sqrt(out[metric_mask()]);assert np.all(ms>0)
 mass=scalar_scatter(d['mu'],g);ss=np.ones((87,45));ss[scalar_mask()]=np.sqrt(mass[scalar_mask()]);assert np.all(ss>0) and np.all(np.isfinite(ss))
 for n,a in dict(native_congruence=ns,metric_proper_congruence=ms,scalar_mass_congruence=ss,scalar_positive_mass_diagonal=mass).items():finite_real(n,a)
 return ns,ms,ss

def original_ratios(res,rhs,scale):
 raw=float(np.linalg.norm(res));den=float(np.linalg.norm(rhs));white=float(np.linalg.norm(res/scale));wd=float(np.linalg.norm(rhs/scale))
 assert all(math.isfinite(x) for x in (raw,den,white,wd)) and (den>0)==(wd>0)
 if den==0:return np.array((0.,0.)) if raw==white==0 else np.array((math.inf,math.inf))
 return np.array((raw/den,white/wd))

def certify_original(x,rhs,b,d,g,constrained,scales,label):
 ax=system_action(x,b,d,g,constrained);res=rhs-ax;capture(label+'_original_action',ax);capture(label+'_original_residual',res)
 fields=unpack_fields(res,constrained);rfields=unpack_fields(rhs,constrained);ratios=[]
 for name,a,r,s in zip(('native','metric','trace'),fields,rfields,scales):
  if a is None:continue
  capture(label+'_'+name+'_original_residual',a);capture(label+'_'+name+'_original_rhs',r)
  ratio=original_ratios(a,r,s);capture(label+'_'+name+'_original_ratios',ratio);ratios.append(ratio)
  if name in ('native','metric'):
   target=d['target_Pn' if name=='native' else 'target_Pm'];cr=original_ratios(a,target,s);capture(label+'_'+name+'_actual_target_ratios',cr);ratios.append(cr)
 return ax,res,np.stack(ratios)

def minres_core(A,rhs,scale,tolerance,certificate,label,cap=CAP):
 # The same bounded recurrence serves fresh dense witnesses and the full field.
 white_rhs=rhs/scale;wn=float(np.linalg.norm(white_rhs));capture(label+'_white_rhs',white_rhs);assert math.isfinite(wn)
 if wn==0:
  assert np.all(rhs==0);x=np.zeros_like(rhs);res,ratios=certificate(x);return x,ratios,bool(np.all(ratios<=LINEAR_TOL)),'zero_rhs'
 assert math.isfinite(tolerance) and tolerance>0
 def W(y):return A(y/scale)/scale
 y=np.zeros_like(rhs);r=white_rhs.copy();beta=float(np.linalg.norm(r));v=r/beta;pv=np.zeros_like(v);ow=np.zeros_like(v);pw=np.zeros_like(v)
 cs=-1.;sn=0.;dbar=eps=0.;phibar=beta;history=[];reason='iteration_cap'
 for it in range(1,cap+1):
  z=W(v);capture(label+'_Lanczos_action',z);assert np.all(np.isfinite(z));z=z-beta*pv;alpha=float(np.sum(v*z));z=z-alpha*v;next_beta=float(np.linalg.norm(z))
  oldeps=eps;delta=cs*dbar+sn*alpha;gbar=sn*dbar-cs*alpha;eps=sn*next_beta;dbar=-cs*next_beta;gamma=math.hypot(gbar,next_beta)
  capture(label+'_Lanczos_scalars',np.array((it,alpha,beta,next_beta,gamma,phibar)))
  if not all(math.isfinite(a) for a in (alpha,next_beta,delta,gbar,eps,dbar,gamma)) or gamma==0:reason='Lanczos_or_Givens_breakdown';break
  cs=gbar/gamma;sn=next_beta/gamma;phi=cs*phibar;phibar=sn*phibar;w=(v-oldeps*ow-delta*pw)/gamma;y=y+phi*w
  capture(label+'_white_iterate',y);capture(label+'_Lanczos_direction',v);capture(label+'_MINRES_direction',w)
  assert np.all(np.isfinite(y)) and np.all(np.isfinite(w))
  if it%20==0 or abs(phibar)/wn<=tolerance or next_beta==0 or it==cap:
   x=y/scale;res,ratios=certificate(x);white_res=float(np.linalg.norm(res/scale))/wn
   history.append((it,white_res,float(np.max(ratios))));capture(label+'_history',np.asarray(history));capture(label+'_original_iterate',x)
   if np.all(ratios<=LINEAR_TOL):reason='all_original_rows_admitted';break
   if it%40==0:checkpoint('ITERATION',{k:a for k,a in AVAILABLE.items() if k.startswith(label+'_') and k.endswith(('iterate','residual','history','scalars'))},dict(kind='unqualified_restart_snapshot_signed_MINRES_iterate',stage=label,iteration=it))
  if next_beta==0:reason='Lanczos_terminal_original_rows_failed';break
  ow=pw;pw=w;pv=v;v=z/next_beta;beta=next_beta
 x=y/scale;res,ratios=certificate(x);capture(label+'_history',np.asarray(history));capture(label+'_original_iterate',x)
 return x,ratios,bool(np.all(ratios<=LINEAR_TOL)),reason


def bounded_minres(A,rhs,scale,b,d,g,constrained,scales,label):
 # The sufficient white target covers original row and actual target norms.
 wn=float(np.linalg.norm(rhs/scale));bounds=[]
 if wn>0:
  for r,z in zip(unpack_fields(rhs,constrained),scales):
   if r is None:continue
   nr=float(np.linalg.norm(r));nw=float(np.linalg.norm(r/z));assert math.isfinite(nr) and math.isfinite(nw) and (nr>0)==(nw>0)
   if nr>0:bounds.extend((nr/float(np.max(z)),nw))
   else:raise ArithmeticError('Exact zero row requires separate null-row compatibility; no floor replaces its norm')
  for target,z in ((d['target_Pn'],scales[0]),(d['target_Pm'],scales[1])):
   nr=float(np.linalg.norm(target));nw=float(np.linalg.norm(target/z));assert nr>0 and nw>0 and math.isfinite(nr) and math.isfinite(nw);bounds.extend((nr/float(np.max(z)),nw))
  tolerance=LINEAR_TOL*min(bounds)/wn
 else:tolerance=LINEAR_TOL
 capture(label+'_sufficient_white_target',np.array(tolerance))
 def certificate(x):
  ax,res,ratios=certify_original(x,rhs,b,d,g,constrained,scales,label);return res,ratios
 return minres_core(A,rhs,scale,tolerance,certificate,label)


def dense_fixtures():
 # Independent rational canonical example, not a physical field or old solve.
 A=np.array(((2.,1.),(1.,-1.)));x=np.array((1/3,7/3));rhs=np.array((3.,-2.));check('rational_current_canonical_unconstrained',A@x,rhs,abs(A)@abs(x)+abs(rhs))
 S=np.array(((2.,1.,0.),(1.,-1.,3.),(0.,3.,0.)));y=np.array((1.,1.,-2/3));rr=np.array((3.,-2.,3.));check('rational_trace_saddle_original_rows',S@y,rr,abs(S)@abs(y)+abs(rr))
 delta=np.array((y[0]-y[1]-rhs[1],));expected=np.array((-3*y[2],));check('rational_saved_metric_momentum_change_sign',delta,expected,abs(delta)+abs(expected))
 for name,matrix,target,answer in (('fresh_indefinite_2D',A,rhs,x),('fresh_trace_saddle_3D',S,rr,y)):
  def certificate(rate):
   action=matrix@rate;residual=target-action;capture(name+'_original_dense_action',action);capture(name+'_original_dense_residual',residual)
   return residual,original_ratios(residual,target,np.ones_like(target))[None]
  sol,ratios,ok,reason=minres_core(lambda rate:matrix@rate,target,np.ones_like(target),1e-12,certificate,name,cap=6)
  capture(name+'_solution',sol);capture(name+'_original_norm_ratios',ratios);assert ok,(name,reason)
  check(name+'_actual_MINRES_convergence',sol,answer,abs(sol)+abs(answer))



def operator_controls(b,d,g):
 nv=np.broadcast_to(native_mask(),(33,3,87,45));mm=metric_mask();sm=scalar_mask()
 v=((np.arange(33*3*87*45).reshape(33,3,87,45)%13)-6)/37.*nv;k=((np.arange(6*87*45).reshape(6,87,45)%11)-5)/41.*mm
 u=((np.arange(v.size).reshape(v.shape)%17)-8)/43.*nv;l=((np.arange(k.size).reshape(k.shape)%19)-9)/47.*mm
 lam=((np.arange(87*45).reshape(87,45)%7)-3)/53.*sm;capture('operator_native_test',v);capture('operator_metric_test',k);capture('operator_scalar_test',lam)
 av,ak=coupled_action(v,k,b,d,g);eu,ek=coupled_action(u,l,b,d,g);ev,em=coupled_envelope(v,k,b,d,g);eue,ele=coupled_envelope(u,l,b,d,g)
 actual=np.array((np.sum(u*av)+np.sum(l*ak),));expected=np.array((np.sum(v*eu)+np.sum(k*ek),));env=np.array((np.sum(abs(u)*ev)+np.sum(abs(l)*em)+np.sum(abs(v)*eue)+np.sum(abs(k)*ele),));check('full_signed_weak_bilinear_reciprocity',actual,expected,env)
 ck=trace_forward(k,d,g);ct=trace_adjoint(lam,d,g);capture('trace_forward_test',ck);capture('trace_adjoint_test',ct)
 check('trace_original_weak_adjoint',np.array((np.sum(lam*ck),)),np.array((np.sum(k*ct),)),np.array((np.sum(abs(lam)*trace_forward_envelope(k,d,g))+np.sum(abs(k)*trace_adjoint_envelope(lam,d,g)),)))
 sv=scalar_evaluate(lam,g);ih=d['ih'];positive=d['mu']*(ih[:,0,0]+ih[:,1,1]+g['R'].reshape(15136)**2*ih[:,2,2])/(2*d['N'])
 capture('scalar_C_positive_restriction_weight',positive);assert np.all(positive>0) and np.all(np.isfinite(positive))
 embedded=np.zeros((6,87,45));embedded[0]=lam;embedded[5]=lam;rankrow=trace_forward(embedded,d,g);massrow=scalar_scatter(positive*sv,g)
 check('C_scalar_positive_mass_restriction',rankrow,massrow,scalar_scatter(positive*abs(sv),g)+abs(massrow))
 # Actual two-point cell hats are injective for bilinear Q1 on each cell.
 h=g['hats'][:,:,0].transpose(2,3,0,1).reshape(3784,4,4);capture('cell_Q1_value_matrices',h);det=np.linalg.det(h);capture('cell_Q1_value_determinants',det);assert np.all(np.isfinite(det)) and np.all(det!=0)
 checkpoint('OPERATOR',{n:a for n,a in dict(RAW,**AVAILABLE).items()},dict(kind='signed_action_adjoint_and_trace_full_rank_restriction',controls=CHECKS[-3:],scalar_rank=3870,proof='positive quadrature plus actual cell Q1 injectivity and a=f scalar embedding',outer_instantaneous_dofs_free=True,physical_wall=False))


def save_solution(x,rhs,ratios,ok,reason,b,d,g,targets,scales,constrained,label):
 v,k,lam=unpack_fields(x,constrained);kn=trace_forward(k,d,g);gap=kn-targets['trace_rhs'];capture(label+'_trace_gap',gap)
 trace_ratios=original_ratios(gap,targets['trace_rhs'],scales[2]);capture(label+'_trace_compatibility_ratios',trace_ratios);trace_ok=bool(np.all(trace_ratios<=LINEAR_TOL))
 n,m=coupled_action(v,k,b,d,g);Pn=targets['cn']+n;Pm=targets['cm']+m;delta=Pm-targets['Pm'];capture(label+'_new_native_momentum',Pn);capture(label+'_new_metric_momentum',Pm);capture(label+'_metric_momentum_change',delta)
 if constrained:
  reaction=trace_adjoint(lam,d,g);capture(label+'_trace_reaction',reaction);en,em=coupled_envelope(v,k,b,d,g)
  rmetric=AVAILABLE[label+'_metric_original_residual'].copy();capture(label+'_momentum_change_original_metric_residual',rmetric)
  check('trace_preparation_metric_change_plus_original_residual_equals_minus_CTlambda',delta+rmetric,-reaction,abs(Pm)+abs(targets['Pm'])+em+trace_adjoint_envelope(lam,d,g)+abs(targets['cm'])+abs(rmetric))
 data=dict(native_nodal_rate=v,metric_nodal_rate=k,current_Pn=targets['Pn'],current_Pm=targets['Pm'],new_Pn=Pn,new_Pm=Pm,metric_momentum_change=delta,trace_original_action=kn,trace_rhs=targets['trace_rhs'],trace_gap=gap,trace_original_ratios=trace_ratios,canonical_original_ratios=ratios)
 if lam is not None:data.update(trace_multiplier=lam,trace_reaction=trace_adjoint(lam,d,g))
 data.update({n:a for n,a in dict(RAW,**AVAILABLE).items() if n.startswith(label+'_')})
 rec=checkpoint('SOLUTION',data,dict(kind='trace_constrained_preparation' if constrained else 'actual_canonical_compatibility_test',canonical_rows_admitted=ok,trace_row_admitted=trace_ok,solver_reason=reason,targets='CURRENT actual force V003',metric_momentum_changed=constrained,no_uniqueness_or_rank_G_claim=True,preparation='new metric momentum disclosed' if constrained else 'attempt to preserve both canonical targets',physical_Cauchy_adoption=False))
 if ok:
  # These are genuine rates and their fixed-basis spatial jets, not L2 gradients.
  jets={}
  for name,a,evalf in (('native',v,evaluate_velocity),('metric',k,evaluate_metric)):
   for j,axis in enumerate(('value','R','Z')):
    val=evalf(a,g,j);finite_real(label+'_'+name+'_jet_'+axis,val);jets[name+'_jet_'+axis]=val
  checkpoint('RATE_JETS',jets,dict(kind='genuine_fixed_Q1_rate_value_and_spatial_jets',stage=label,canonical_rows_admitted=ok,weak_trace_admitted=trace_ok,pointwise_CMC_claim=False,physical_time_history=None))
 return rec,trace_ok


def run_admission(parents,allow_trace):
 global RAW,AVAILABLE
 checkpoint('INPUT',{},dict(kind='same_conditional_sigma1_current_canonical_member',parents=PARENTS,targets='current actual native and metric momenta',optional_trace_preparation_requested=allow_trace,new_source_terms=False,phase_momentum_reset=False,ordinary_momentum_reset=False,history=None,physical_outer_trace=None,activity_outside_0p3_15p1=None))
 RAW={};AVAILABLE={};dense_fixtures();checkpoint('FIXTURE',dict(RAW,**AVAILABLE),dict(kind='five_fresh_rational_signed_saddle_controls',controls=CHECKS.copy(),physical_state=False));RAW={};AVAILABLE={}
 g,b,d,targets,ns=load_saved_system(parents);ns,ms,ss=positive_scales(ns,d,g);scales=(ns,ms,ss)
 checkpoint('BASIS',dict({n:a for n,a in g.items()},native_scale=ns,metric_scale=ms,scalar_scale=ss),dict(kind='unchanged_E_F_S_bases_and_positive_solver_congruences',native_dofs=380292,metric_dofs=23048,scalar_dofs=3870,axis_reflection=True,free_outer_instantaneous_rate=True))
 RAW={};AVAILABLE={};operator_controls(b,d,g);RAW={};AVAILABLE={}
 rn=targets['Pn']-targets['cn'];rm=targets['Pm']-targets['cm'];rhs=pack_fields(rn,rm);scale=pack_fields(ns,ms)
 finite_real('canonical_native_rhs',rn);finite_real('canonical_metric_rhs',rm)
 x,ratio,ok,reason=bounded_minres(lambda a:system_action(a,b,d,g,False),rhs,scale,b,d,g,False,scales,'compatibility')
 comp,trace_ok=save_solution(x,rhs,ratio,ok,reason,b,d,g,targets,scales,False,'compatibility')
 if not ok:return dict(status='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED',compatibility=comp,trace_preparation=None)
 if trace_ok:return dict(status='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE',compatibility=comp,trace_preparation=None)
 if not allow_trace:return dict(status='RETURNED_CANONICAL_RATE_FAILS_WEAK_CMC',compatibility=comp,trace_preparation=None,existence_of_another_compatible_rate=None)
 # Compatibility record remains unchanged. New saddle is a separate preparation.
 RAW={};AVAILABLE={};rhs=pack_fields(rn,rm,targets['trace_rhs']);scale=pack_fields(ns,ms,ss)
 y,ratio,ok,reason=bounded_minres(lambda a:system_action(a,b,d,g,True),rhs,scale,b,d,g,True,scales,'trace_preparation')
 prep,trace_ok=save_solution(y,rhs,ratio,ok,reason,b,d,g,targets,scales,True,'trace_preparation')
 return dict(status='DISCLOSED_TRACE_PREPARATION_ADMITTED' if ok and trace_ok else 'TRACE_PREPARATION_ORIGINAL_ROWS_NOT_ADMITTED',compatibility=comp,trace_preparation=prep,physical_adoption=False)


def recovery_admission():
 # All prior arithmetic, fields and snapshots remain immutable inputs.
 pins,parents=admission()
 bound={'cross_u_canonical_nodal_metric_rate_solve_v001.py':'f84b8a9bea9d45ac1370985401172621d93d59dc814bedda785206188b3c2c4b',
        FAILED_STEM+'.md':'426cc5a3c12cce7557118903379bfc69e2d1afa935cc76a3bb315e8e2598beea',
        FAILED_STEM+'_RESULT.json':'efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82',
        FAILED_STEM+'_RECEIPT.json':'8f306769022830cb0762e735308f493b072b58320fbdffabf46898c5a180f473'}
 for n,h in bound.items():assert sha(path(n))==h;pins[str(path(n).resolve())]=h
 old=json.loads(path(FAILED_STEM+'_RESULT.json').read_text());rc=json.loads(path(FAILED_STEM+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['closed']>rc['owner']['started']
 assert rc['owner']==old['owner'] and rc['owner']['owner']=='root' and rc['owner']['pid']==39611
 assert rc['owner']['source_sha256']==bound['cross_u_canonical_nodal_metric_rate_solve_v001.py'] and rc['result_sha256']==bound[FAILED_STEM+'_RESULT.json']
 assert old['status']==old['case']['status']=='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED' and old['case']['trace_preparation'] is None
 assert len(old['controls'])==17 and [x['ordinal'] for x in old['controls']]==list(range(17)) and all(x['passed'] and x['tolerance']==TOL for x in old['controls'])
 assert len(old['checkpoints'])==25 and all(v is False for v in old['qualification'].values())
 assert old['case']['compatibility']['metadata']['canonical_rows_admitted'] is False
 assert old['case']['compatibility']['metadata']['solver_reason']=='iteration_cap'
 for mapping in (rc['input_sha256'],rc['output_sha256']):
  for n,h in mapping.items():
   key=str(path(n).resolve());assert key not in pins or pins[key]==h
   assert sha(path(n))==h;pins[key]=h
 assert {p.name for p in BASE.glob(FAILED_STEM+'_*.npz')}=={r['file'] for r in old['checkpoints']}
 assert {p.name for p in BASE.glob(FAILED_STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in old['checkpoints']}
 for r in old['checkpoints']:
  assert rc['output_sha256'][r['file']]==r['sha256'] and rc['output_sha256'][r['commit_file']]==r['commit_sha256']
  assert resolve_record(r)==r and r['metadata']['owner']==rc['owner'] and r['metadata']['failed'] is False
 return pins,parents,old


def recover_saved_system(parents,old):
 # No old feature, matrix-column, affine-load, basis, fixture or initial solve replay.
 brec=unique_record(old,'unchanged_E_F_S_bases_and_positive_solver_congruences')
 names=('R','dv','hats','cell_i','cell_j','r','z','native_scale','metric_scale','scalar_scale')
 a=read_pair(brec,names)
 for n,v in a.items():capture('recovered_basis_'+n,v)
 g={n:a[n] for n in ('R','dv','hats','cell_i','cell_j','r','z')};scales=(a['native_scale'],a['metric_scale'],a['scalar_scale'])
 assert g['R'].shape==g['dv'].shape==(4,3784) and g['hats'].shape==(4,4,3,86,44)
 assert all(np.all(x>0) and np.all(np.isfinite(x)) for x in scales)
 affine=unique_record(old,'actual_current_weak_targets_and_owned_H_trace_rhs')
 targets=read_pair(affine,('Pn','Pm','cn','cm','trace_rhs'))
 for n,v in targets.items():capture('recovered_target_'+n,v)
 cols=[r for r in old['checkpoints'] if r['metadata']['kind']=='copied_signed_blocks_and_current_actual_affine_reference']
 assert len(cols)==4 and [r['metadata']['column'] for r in cols]==list(range(4))
 chunks=[];keys=('B','eB','T','eT','ih','N','mu','lie','elie','vstar','kstar','pstar','pistar','cn','cm','ecn','ecm','Kstar')
 for iq,r in enumerate(cols):
  c=read_pair(r,keys)
  for n,v in c.items():capture('recovered_q%d_'%iq+n,v)
  chunks.append(c)
 d={}
 for n in keys:d[n]=np.concatenate([c[n] for c in chunks]);capture('recovered_whole_'+n,d[n])
 d['target_Pn']=targets['Pn'];d['target_Pm']=targets['Pm']
 weak=parents[PARENTS[1]['stem']];mass=unique_record(weak,'complete_fixed_metric_native99_mass_coefficients')
 mass_names=('mixing_L','modal_D','Maxwell_M0','operation_eL','operation_eD','operation_eM0')
 m=read_pair(mass,mass_names)
 b=dict(L=m['mixing_L'],D=m['modal_D'],M0=m['Maxwell_M0'],eL=m['operation_eL'],eD=m['operation_eD'],eM0=m['operation_eM0'])
 for n,v in b.items():capture('recovered_mass_'+n,v)
 sol=old['case']['compatibility']
 sn=('compatibility_original_iterate','compatibility_original_residual','compatibility_original_action','compatibility_native_original_rhs','compatibility_metric_original_rhs','compatibility_native_original_residual','compatibility_metric_original_residual','canonical_original_ratios','native_nodal_rate','metric_nodal_rate')
 x=read_pair(sol,sn)
 for n,v in x.items():capture('recovered_seed_'+n,v)
 seed=x['compatibility_original_iterate'];res=x['compatibility_original_residual'];action=x['compatibility_original_action']
 rhs=pack_fields(x['compatibility_native_original_rhs'],x['compatibility_metric_original_rhs'])
 assert seed.shape==res.shape==action.shape==rhs.shape==(403340,)
 assert np.array_equal(seed,pack_fields(x['native_nodal_rate'],x['metric_nodal_rate']))
 assert np.array_equal(res,pack_fields(x['compatibility_native_original_residual'],x['compatibility_metric_original_residual']))
 capture('recovered_original_rhs',rhs)
 refs=[{n:r[n] for n in ('file','sha256','commit_file','commit_sha256')} for r in old['checkpoints']]
 checkpoint('RECOVERED_BASE',dict(original_iterate=seed,original_residual=res,original_action=action,original_rhs=rhs,original_ratios=x['canonical_original_ratios'],current_Pn=targets['Pn'],current_Pm=targets['Pm'],native_affine=targets['cn'],metric_affine=targets['cm'],trace_rhs=targets['trace_rhs'],native_scale=scales[0],metric_scale=scales[1],scalar_scale=scales[2]),dict(kind='exact_saved_600_iterate_original_targets_and_rows',parent_result_sha256='efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82',reused_checkpoint_refs=refs,reused_controls=old['controls'],basis_ref=brec,affine_ref=affine,column_refs=[{n:r[n] for n in ('file','sha256','commit_file','commit_sha256')} for r in cols],native_mass_ref={n:mass[n] for n in ('file','sha256','commit_file','commit_sha256')},original_nonadmission_preserved=True,temporal_or_physical_state_changed=False))
 return g,b,d,targets,scales,seed,res,action,rhs


def refinement_tolerance(original_rhs,correction_rhs,d,scales,constrained):
 wn=float(np.linalg.norm(correction_rhs/pack_fields(*scales if constrained else scales[:2])))
 assert math.isfinite(wn) and wn>0
 bounds=[]
 for r,s in zip(unpack_fields(original_rhs,constrained),scales):
  if r is None:continue
  nr=float(np.linalg.norm(r));nw=float(np.linalg.norm(r/s))
  assert nr>0 and nw>0 and math.isfinite(nr) and math.isfinite(nw),'No replacement of exact zero original row norm'
  bounds.extend((nr/float(np.max(s)),nw))
 for t,s in ((d['target_Pn'],scales[0]),(d['target_Pm'],scales[1])):
  nr=float(np.linalg.norm(t));nw=float(np.linalg.norm(t/s));assert nr>0 and nw>0 and math.isfinite(nr) and math.isfinite(nw)
  bounds.extend((nr/float(np.max(s)),nw))
 tolerance=LINEAR_TOL*min(bounds)/wn;assert tolerance>0 and math.isfinite(tolerance)
 return tolerance


def shifted_dense_fixture():
 # New four-dimensional signed correction witness, distinct from all 17 old controls.
 matrix=np.array(((3.,1.,0.,0.),(1.,-2.,0.,0.),(0.,0.,2.,1.),(0.,0.,1.,-3.)))
 answer=np.array((1/2,-1/3,2/5,-1/7));base=answer+np.array((1/10,1/20,-1/30,1/40))
 rhs=matrix@answer;residual=rhs-matrix@base
 for n,a in dict(matrix=matrix,answer=answer,base=base,original_rhs=rhs,correction_rhs=residual).items():capture('shifted_dense_'+n,a)
 def certificate(delta):
  candidate=base+delta;capture('shifted_dense_candidate',candidate);r=rhs-matrix@candidate;capture('shifted_dense_original_residual',r)
  return r,original_ratios(r,rhs,np.ones_like(rhs))[None]
 delta,ratio,ok,reason=minres_core(lambda v:matrix@v,residual,np.ones_like(rhs),1e-12,certificate,'fresh_shifted_4D',cap=8)
 capture('shifted_dense_correction',delta);capture('shifted_dense_original_ratios',ratio);assert ok,reason
 check('fresh_4D_original_rows_after_shifted_residual_correction',base+delta,answer,abs(base)+abs(delta)+abs(answer))


def refine_saved_iterate(seed,residual,base_action,original_rhs,b,d,g,scales,constrained,label):
 current=seed.copy();current_res=residual.copy();current_action=base_action.copy();scale=pack_fields(*scales if constrained else scales[:2]);cycles=[]
 for cycle in range(1,MAX_CYCLES+1):
  stage=label+'_cycle_%03d'%cycle;CONTEXT.update(stage=stage,cycle=cycle)
  base=current.copy();r0=current_res.copy();a0=current_action.copy()
  for n,a in dict(base_iterate=base,correction_rhs=r0,base_original_action=a0,original_rhs=original_rhs).items():capture(stage+'_'+n,a)
  if np.all(r0==0):break
  tolerance=refinement_tolerance(original_rhs,r0,d,scales,constrained);capture(stage+'_sufficient_white_target',np.array(tolerance))
  def certificate(delta):
   candidate=base+delta;capture(stage+'_updated_candidate',candidate)
   ax,rr,ratios=certify_original(candidate,original_rhs,b,d,g,constrained,scales,stage)
   return rr,ratios
  delta,ratio,ok,reason=minres_core(lambda v:system_action(v,b,d,g,constrained),r0,scale,tolerance,certificate,stage,cap=RESTART_CAP)
  capture(stage+'_correction',delta);current=base+delta;capture(stage+'_updated_iterate',current)
  current_action,current_res,ratio=certify_original(current,original_rhs,b,d,g,constrained,scales,stage)
  da=system_action(delta,b,d,g,constrained);capture(stage+'_correction_action',da)
  predicted=r0-da;capture(stage+'_residual_update_prediction',predicted);defect=current_res-predicted;capture(stage+'_residual_update_defect',defect)
  bv,bk,bl=unpack_fields(base,constrained);dv,dk,dl=unpack_fields(delta,constrained)
  bn,bm=coupled_envelope(bv,bk,b,d,g);dn,dm=coupled_envelope(dv,dk,b,d,g)
  if constrained:
   bm+=trace_adjoint_envelope(bl,d,g);dm+=trace_adjoint_envelope(dl,d,g)
   bp=trace_forward_envelope(bk,d,g);dp=trace_forward_envelope(dk,d,g)
  else:bp=dp=None
  env=abs(original_rhs)+pack_fields(bn+dn,bm+dm,None if bp is None else bp+dp)+abs(r0)+abs(da)+abs(current_res)
  capture(stage+'_residual_update_operation_envelope',env)
  # Preserve completed signed progress before any arithmetic admission.
  rec=checkpoint('REFINEMENT_CYCLE',{n:a for n,a in AVAILABLE.items() if n.startswith(stage+'_')},dict(kind='shifted_residual_correction_against_original_rows',stage=stage,cycle=cycle,iteration_cap=RESTART_CAP,solver_reason=reason,canonical_rows_admitted=bool(np.all(ratio<=LINEAR_TOL)),original_rhs_and_actual_targets_unchanged=True,correction_rhs_is_saved_previous_residual=True,physical_Cauchy_adoption=False))
  check(stage+'_fresh_original_residual_update_identity',current_res,predicted,env)
  cycles.append(dict(cycle=cycle,record={n:rec[n] for n in ('file','sha256','commit_file','commit_sha256')},reason=reason,original_ratios=ratio.tolist()))
  if np.all(ratio<=LINEAR_TOL):break
 ax,rr,ratio=certify_original(current,original_rhs,b,d,g,constrained,scales,label)
 return current,ratio,bool(np.all(ratio<=LINEAR_TOL)),cycles


def run_continuation(parents,old,allow_trace):
 global RAW,AVAILABLE,CHECKS
 CHECKS=json.loads(json.dumps(old['controls']));CHECKS_BASE=json.loads(json.dumps(CHECKS))
 checkpoint('INPUT',{},dict(kind='same_current_targets_saved_iterate_recovery',parent_result_sha256='efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82',parent_receipt_sha256='8f306769022830cb0762e735308f493b072b58320fbdffabf46898c5a180f473',reused_controls=CHECKS_BASE,reused_records=25,max_correction_cycles=MAX_CYCLES,correction_iteration_cap=RESTART_CAP,original_iteration_cap=CAP,old17_replayed=False,initial_zero_solve_replayed=False,optional_trace_preparation_requested=allow_trace,history=None,exterior=None,activity_outside_0p3_15p1=None))
 RAW={};AVAILABLE={};shifted_dense_fixture();checkpoint('FIXTURE',dict(RAW,**AVAILABLE),dict(kind='one_new_signed_shifted_residual_correction_control',controls=CHECKS[17:],physical_state=False));RAW={};AVAILABLE={}
 g,b,d,targets,scales,seed,res,action,rhs=recover_saved_system(parents,old);RAW={};AVAILABLE={}
 x,ratio,ok,cycles=refine_saved_iterate(seed,res,action,rhs,b,d,g,scales,False,'compatibility')
 comp,trace_ok=save_solution(x,rhs,ratio,ok,'shifted_residual_original_rows_admitted' if ok else 'bounded_shifted_corrections_not_admitted',b,d,g,targets,scales,False,'compatibility')
 assert CHECKS[:17]==CHECKS_BASE
 if not ok:return dict(status='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED',compatibility=comp,compatibility_corrections=cycles,trace_preparation=None,parent_nonadmission_preserved=True)
 if trace_ok:return dict(status='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE',compatibility=comp,compatibility_corrections=cycles,trace_preparation=None,parent_nonadmission_preserved=True)
 if not allow_trace:return dict(status='RETURNED_CANONICAL_RATE_FAILS_WEAK_CMC',compatibility=comp,compatibility_corrections=cycles,trace_preparation=None,existence_of_another_compatible_rate=None,parent_nonadmission_preserved=True)
 # No metric canonical preparation change occurs before original-row admission.
 RAW={};AVAILABLE={};rn,rm,_=unpack_fields(rhs,False);trace_rhs=pack_fields(rn,rm,targets['trace_rhs'])
 seed_trace=pack_fields(*unpack_fields(x,False)[:2],np.zeros((87,45)))
 trace_action=system_action(seed_trace,b,d,g,True);trace_residual=trace_rhs-trace_action
 for n,a in dict(seed=seed_trace,original_rhs=trace_rhs,original_action=trace_action,original_residual=trace_residual).items():capture('trace_initial_'+n,a)
 checkpoint('TRACE_INITIAL',dict(AVAILABLE),dict(kind='separate_disclosed_trace_preparation_after_canonical_admission',canonical_targets_prior_to_reaction=True,physical_adoption=False))
 y,ratio,ok,tcycles=refine_saved_iterate(seed_trace,trace_residual,trace_action,trace_rhs,b,d,g,scales,True,'trace_preparation')
 prep,trace_ok=save_solution(y,trace_rhs,ratio,ok,'shifted_trace_original_rows_admitted' if ok else 'bounded_shifted_trace_not_admitted',b,d,g,targets,scales,True,'trace_preparation')
 return dict(status='DISCLOSED_TRACE_PREPARATION_ADMITTED' if ok and trace_ok else 'TRACE_PREPARATION_ORIGINAL_ROWS_NOT_ADMITTED',compatibility=comp,compatibility_corrections=cycles,trace_preparation=prep,trace_corrections=tcycles,physical_adoption=False,parent_nonadmission_preserved=True)


def main():
 global np,OWNER,INPUTS,RECOVERY
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');ap.add_argument('--trace-preparation',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS,'Guarded definitions only; root and distinct FULL review required'
 assert PROTOCOL_SHA and sha(path(STEM+'.md'))==PROTOCOL_SHA and not list(BASE.glob(STEM+'_*'))
 INPUTS,parents,RECOVERY=recovery_admission();INPUTS[str(path(STEM+'.md').resolve())]=PROTOCOL_SHA;INPUTS[str(Path(__file__).resolve())]=sha(__file__)
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(sigma=1.,target='actual-current-unchanged',trace_preparation=args.trace_preparation,linear_tolerance=LINEAR_TOL,arithmetic_tolerance=TOL,old_iteration_cap=CAP,correction_cycle_cap=MAX_CYCLES,correction_iteration_cap=RESTART_CAP),qualification=FLAGS))
  import numpy as np_local
  np=np_local;result=run_continuation(parents,RECOVERY,args.trace_preparation)
  cycle_count=len(result.get('compatibility_corrections',[]))+len(result.get('trace_corrections',[]))
  assert len(CHECKS)==BASE_CONTROLS+cycle_count+(1 if result.get('trace_preparation') is not None else 0) and all(c['passed'] for c in CHECKS)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status=result['status'],case=result,controls=CHECKS,reused_control_count=17,parent_result_sha256='efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82',checkpoints=RECORDS,qualification=FLAGS));recheck()
  json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));recheck();print(result['status'],len(CHECKS),len(RECORDS))
  return 0 if result['status'] in ('CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE','DISCLOSED_TRACE_PREPARATION_ADMITTED') else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:
   if RAW or AVAILABLE:checkpoint('ERROR_RAW',dict(RAW,**AVAILABLE),dict(kind='unqualified_completed_saved_iterate_recovery_operands',context=dict(CONTEXT),controls=CHECKS),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  try:
   eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,prior_receipt_sha256=prior,controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),qualification=FLAGS))
   if prior is None:json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=None,error_sha256=eh,qualification=FLAGS))
  finally:seal_actual()
  return 1

if __name__=='__main__':raise SystemExit(main())
