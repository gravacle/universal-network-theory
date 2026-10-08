"""Guarded genuine weak nodal native99 temporal map; root-only evaluation."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback,ast,zipfile,struct
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001'
PARENT='CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='66d95d04926de468c0c64cd155e80064b9d72c7f49f1925785057105c5b2d232'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
PINS={'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_MAP_AND_BASIS_V001.md': 'faf6d1d5cccb9266cde70c1a6264745da2cea9e1f3ceaab871a760ee1d0bada9', 'author_fragment_weak_nodal_native_legendre_admission_minimal_v001.txt': 'c61b2d86d0710df40ce4782276f7a263092fe90dc8d2780428eed1863365a8f9', 'author_fragment_weak_nodal_native_legendre_admission_closed_v001.txt': '8bfb10164b41af7b3f9515320ceb2233285a1964ac870909fab706102e67601f', 'author_fragment_weak_nodal_native_legendre_admission_v001.txt': '23b322ba6ce64dbb03021c00a149b620d4a54f9eace2b789fe1b57d8d4469cf9', 'author_fragment_weak_nodal_native_mass_fixtures_v001.txt': '1bbc486572918c70cae5d78113c8e39bd319df54ae7ff6f54e41f795afbdd1aa', 'authoring_cross_u_weak_nodal_native_legendre_v001_279_947c8947.py': '947c894720c474a140eaeee3f7cde0d950ad3300e4d29418af9ee6042909e826', 'authoring_cross_u_weak_nodal_native_legendre_v001_568_ad4339ce.py': 'ad4339cec13e7f00c625a2689cc7774830b5ac261f6e093754a0f9d0bb678724', 'authoring_cross_u_weak_nodal_native_legendre_v001_568_ef750df1.py': 'ef750df1c1bf2a275e3745989eb9710123da13a6b05c45c93923e17164e3c1dc', 'authoring_cross_u_weak_nodal_native_legendre_v001_572_0c478546.py': '0c4785460c9a93017b69b039c6d9d18e42a2dbc15e432efeec15546a62bfabd9', 'authoring_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_16_5e4405e0.md': '5e4405e0881af11cb32432be073cd04909ad6d4e1577bf2e57e11b441c9fc8ee', 'authoring_cross_u_weak_nodal_native_legendre_v001_570_3b03926e.py': '3b03926ef7cac422b83c4f5b2cb735e6fb628785dceeae8eaae749167c3fd170', 'authoring_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_16_b2768c6c.md': 'b2768c6c2214943ef570924f0922f5d682031a8f1ec8fade6f2a699e0111b7d0'}
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1
TOL=2e-11;LINEAR_TOL=1e-10;NATIVE_CAP=160;MODAL_CAP=160
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(nodal_metric_velocity_qualified=False,full_constraint_qualified=False,CMC_qualified=False,physical_inertia_qualified=False,history_qualified=False,exterior_qualified=False,source_qualified=False,physical_metric_qualified=False,galaxy_velocity_qualified=False)

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

def scalar_lump(field,geo):
 # Positive nodal scalar weights ONLY for preconditioning; not mass-lumped action.
 assert field.shape[-1]==15136
 f=field.reshape(field.shape[:-1]+(4,86,44));out=np.zeros(field.shape[:-1]+(87,45))
 for iq in range(4):
  wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):out[...,i:86+i,j:44+j]+=wq*geo['hats'][iq,a,0]*f[...,iq,:,:]
 out[...,1,:]+=out[...,0,:];out[...,0,:]=0;return out

def coefficients(cols,w,omega):
 # Authoritative saved chart: no feature/105 Gram/local solve replay.
 names=('g','hi','U','z','owned_chart_ih','owned_chart_N','owned_chart_beta','owned_chart_u','owned_chart_gamma','owned_chart_JU','owned_chart_JzU','owned_chart_Jzz','owned_chart_dens','owned_chart_old_velocity','owned_native_canonical_density','actual_owned_native_density')
 data={}
 for name in names:
  data[name]=np.concatenate([c[name] for c in cols],axis=1 if name in ('z','owned_chart_JzU') else 0);finite_real('input_'+name,data[name])
 hi=data['hi'];U=data['U'];z=data['z'];ih=data['owned_chart_ih'];N=data['owned_chart_N'];u=data['owned_chart_u'];gamma=data['owned_chart_gamma'];beta=data['owned_chart_beta'];dens=data['owned_chart_dens'];JU=data['owned_chart_JU'];JzU=data['owned_chart_JzU'];Jzz=data['owned_chart_Jzz']
 assert U.shape==(15136,4) and z.shape==(32,15136,4) and np.all(N>0) and np.all(dens>0) and np.all(w>0) and np.all(omega>0)
 S=np.zeros((15136,4,3));S[:,0]=Jzz;S[:,1:]=np.eye(3)[None]
 L=u[None,:,:,None]*U[None,:,0,None,None]*JzU[:,:,None,:];finite_real('mixing_L',L)
 cone=U[None,:,0]**2/omega[:,None]**2-ELL**2*(hi[None,:,0,0]+U[None,:,0]**2);finite_real('native_cone',cone);assert np.all(cone>0)
 gram=np.einsum('pai,pab,pbk->pik',S,hi,S,optimize=True);finite_real('transverse_Gram',gram);np.linalg.cholesky(gram)
 D=dens[None,:,None,None]*w[:,None,None,None]*cone[:,:,None,None]*gram[None];finite_real('modal_D',D)
 M0=dens[:,None,None]*ALPHA*ih/N[:,None,None]**2;finite_real('Maxwell_M0',M0);np.linalg.cholesky(M0)
 euc=np.einsum('pab,pb->pa',abs(data['g']),abs(U));eup=np.einsum('pij,pj->pi',abs(ih),euc[:,1:])
 eJU=np.empty_like(JU);eJU[:,0]=eup/(N*gamma)[:,None];eJU[:,1:]=abs(ih)+abs(beta)[:,:,None]*eJU[:,None,0,:]
 eJzU=np.einsum('jpa,pai->jpi',abs(z),eJU)/abs(U[None,:,0,None]);eJzz=(eup+abs(beta)*gamma[:,None]/N[:,None])/abs(U[:,0,None])
 eS=np.zeros_like(S);eS[:,0]=eJzz;eS[:,1:]=np.eye(3)[None];eL=abs(u)[None,:,:,None]*abs(U[None,:,0,None,None])*eJzU[:,:,None,:]
 econe=U[None,:,0]**2/omega[:,None]**2+ELL**2*(abs(hi[None,:,0,0])+U[None,:,0]**2)
 egram=np.einsum('pai,pab,pbk->pik',eS,abs(hi),eS,optimize=True)
 eD=dens[None,:,None,None]*w[:,None,None,None]*econe[:,:,None,None]*egram[None];eM0=dens[:,None,None]*ALPHA*abs(ih)/N[:,None,None]**2
 for name,a in dict(operation_euc=euc,operation_eup=eup,operation_eJU=eJU,operation_eJzU=eJzU,operation_eJzz=eJzz,operation_eS=eS,operation_eL=eL,operation_econe=econe,operation_eD=eD,operation_eM0=eM0).items():finite_real(name,a);assert np.all(a>=0)
 vel=data['owned_chart_old_velocity'].reshape(15136,33,3).transpose(1,0,2);capture('authoritative_point_velocity',vel)
 target=data['owned_native_canonical_density'].reshape(15136,33,3).transpose(1,0,2);capture('authoritative_point_native_density',target)
 pstar=data['actual_owned_native_density'].reshape(15136,33,3).transpose(1,0,2);capture('actual_owned_point_native_density',pstar);capture('saved_affine_momentum_gap',pstar-target)
 return dict(L=L,D=D,M0=M0,eL=eL,eD=eD,eM0=eM0,velocity=vel,target=target,pstar=pstar)

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

def node_spd(a,mask):
 # Inactive coordinates are not DOFs; identity filler is for batched solves only.
 m=mask.transpose(1,2,0).reshape(3915,3);out=a.copy()*m[...,None]*m[:,None,:]
 for i in range(3):out[...,i,i]+=~m[...,i]
 return out

def preconditioner(b,g,r):
 def lump(a):
  n=a.ndim;v=scalar_lump(a.transpose(tuple(range(n-3))+(n-2,n-1,n-3)),g).reshape(a.shape[:-3]+(3,3,3915))
  return v.transpose(tuple(range(n-3))+(n-1,n-3,n-2))
 DD=lump(b['D']);BB=lump(np.einsum('jpki,jpkl->jpil',b['L'],b['D'],optimize=True));M0=lump(b['M0']);m=native_mask();DD=node_spd(DD,m);M0=node_spd(M0,m)
 mm=m.transpose(1,2,0).reshape(3915,3);BB*=mm[None,:,:,None]*mm[None,:,None,:]
 for name,a in dict(preconditioner_D=DD,preconditioner_B=BB,preconditioner_Maxwell=M0).items():finite_real(name,a)
 np.linalg.cholesky(DD);np.linalg.cholesky(M0);DB=np.linalg.solve(DD,np.swapaxes(BB,-1,-2));finite_real('preconditioner_Dinv_BT',DB)
 A=M0+np.einsum('jnik,jnkl->nil',BB,DB,optimize=True);finite_real('preconditioner_positive_U_block',A)
 scale=np.ones((3915,3));scale[:,2]=np.broadcast_to(r[:,None]**2,(87,45)).reshape(3915);scale[:45,2]=1
 diag=np.concatenate((np.diagonal(A,axis1=-2,axis2=-1)[None],np.diagonal(DD,axis1=-2,axis2=-1)))*scale[None]**2
 capture('preconditioner_basis_scale',scale);finite_real('preconditioner_diagonal',diag);assert np.all(diag>0)
 normscale=np.sqrt(diag).reshape(33,87,45,3).transpose(0,3,1,2);capture('kinetic_congruence_scale',normscale)
 return dict(D=DD,B=BB,M0=M0,scale=scale,normscale=normscale,mask=m)

def apply_preconditioner(rhs,pre):
 r=rhs.transpose(0,2,3,1).reshape(33,3915,3)/pre['scale'][None]
 dz=np.linalg.solve(pre['D'],r[1:,...,None])[...,0];red=r[0]-np.einsum('jnik,jnk->ni',pre['B'],dz,optimize=True);u=np.linalg.solve(pre['M0'],red[...,None])[...,0]
 z=np.linalg.solve(pre['D'],(r[1:]-np.einsum('jnki,nk->jni',pre['B'],u,optimize=True))[...,None])[...,0];y=np.concatenate((u[None],z))/pre['scale'][None]
 return y.reshape(33,87,45,3).transpose(0,3,1,2)*pre['mask'][None]

def dot(a,b):return float(np.sum(a*b))

def solve_native(rhs,b,g,pre):
 x=np.zeros_like(rhs);capture('native_iterate',x);r=rhs.copy();capture('native_original_residual',r);z=apply_preconditioner(r,pre);capture('native_preconditioned_residual',z);p=z.copy();capture('native_search',p);rz=dot(r,z);capture('native_rz',np.array(rz));scale=pre['normscale'];den=float(np.linalg.norm(rhs/scale));capture('native_scaled_rhs_norm',np.array(den));denraw=float(np.linalg.norm(rhs));capture('native_rhs_norm',np.array(denraw));history=[]
 AVAILABLE.update(native_iterate=x.copy(),native_original_residual=r.copy(),native_search=p.copy(),native_preconditioned_residual=z.copy(),native_initial_rz=np.array(rz))
 capture('native_norm_denominators',np.array([den,denraw]));assert math.isfinite(den) and math.isfinite(denraw)
 assert (den>0 and denraw>0) or np.all(rhs==0),'Underflowed nonzero native norm'
 for k in range(NATIVE_CAP+1):
  ax=original_action(x,b,g);capture('native_original_action',ax);r=rhs-ax;capture('native_original_residual',r);ratio=max(float(np.linalg.norm(r/scale))/den,float(np.linalg.norm(r))/denraw) if den else 0.
  history.append((k,ratio));AVAILABLE.update(native_iterate=x.copy(),native_original_action=ax.copy(),native_original_residual=r.copy(),native_history=np.asarray(history,dtype=float),native_search=p.copy(),native_preconditioned_residual=z.copy());assert math.isfinite(ratio) and np.all(np.isfinite(ax)) and np.all(np.isfinite(r))
  if k and k%20==0:checkpoint('NATIVE_ITERATION',{n:AVAILABLE[n] for n in ('native_iterate','native_original_action','native_original_residual','native_history','native_search','native_preconditioned_residual')},dict(kind='resumable_unqualified_native_iterate',iteration=k))
  if ratio<=LINEAR_TOL:return x,ax,r,np.asarray(history,dtype=float)
  assert k<NATIVE_CAP,'Native weak map iteration cap retained'
  if k:
   z=apply_preconditioner(r,pre);capture('native_preconditioned_residual',z);newrz=dot(r,z);capture('native_updated_rz',np.array(newrz));assert newrz>0 and math.isfinite(newrz);capture('native_beta',np.array(newrz/rz));p=z+(newrz/rz)*p;capture('native_search',p);rz=newrz;capture('native_rz',np.array(rz))
  ap=original_action(p,b,g);capture('current_native_search_action',ap);pa=dot(p,ap);capture('native_search_energy',np.array(pa));assert pa>0 and rz>0 and math.isfinite(pa) and math.isfinite(rz)
  alpha=rz/pa;capture('native_alpha',np.array(alpha));assert math.isfinite(alpha);x=x+alpha*p;capture('native_iterate',x)

def mode_action(x,b,g):
 v=evaluate_velocity(x,g);return scatter_velocity(np.einsum('jpik,jpk->jpi',b['D'],v,optimize=True),g)

def mode_preconditioner(rhs,pre):
 r=rhs.transpose(0,2,3,1).reshape(32,3915,3)/pre['scale'][None];y=np.linalg.solve(pre['D'],r[...,None])[...,0]/pre['scale'][None]
 return y.reshape(32,87,45,3).transpose(0,3,1,2)*pre['mask'][None]

def solve_modal(rhs,b,g,pre):
 x=np.zeros_like(rhs);capture('modal_projection_iterate',x);r=rhs.copy();capture('modal_projection_residual',r);z=mode_preconditioner(r,pre);capture('modal_projection_preconditioned_residual',z);p=z.copy();capture('modal_projection_search',p);rz=np.sum(r*z,axis=(1,2,3));capture('modal_rz',rz);scale=pre['normscale'][1:];den=np.linalg.norm((rhs/scale).reshape(32,-1),axis=1);capture('modal_scaled_rhs_norm',den);denraw=np.linalg.norm(rhs.reshape(32,-1),axis=1);capture('modal_rhs_norm',denraw);active=den>0;history=[]
 AVAILABLE.update(modal_projection_iterate=x.copy(),modal_projection_residual=r.copy(),modal_projection_search=p.copy(),modal_projection_preconditioned_residual=z.copy(),modal_initial_rz=rz.copy())
 capture('modal_norm_denominators',np.stack((den,denraw)));assert np.all(np.isfinite(den)) and np.all(np.isfinite(denraw));assert np.all(active==(denraw>0)) and np.all(np.all(rhs.reshape(32,-1)==0,axis=1)==~active),'Underflowed nonzero modal norm'
 for k in range(MODAL_CAP+1):
  ax=mode_action(x,b,g);capture('modal_projection_action',ax);r=rhs-ax;capture('modal_projection_residual',r);ratio=np.zeros(32);ratio[active]=np.maximum(np.linalg.norm((r/scale).reshape(32,-1),axis=1)[active]/den[active],np.linalg.norm(r.reshape(32,-1),axis=1)[active]/denraw[active])
  history.append(np.r_[k,ratio]);AVAILABLE.update(modal_projection_iterate=x.copy(),modal_projection_action=ax.copy(),modal_projection_residual=r.copy(),modal_projection_history=np.asarray(history,dtype=float),modal_projection_search=p.copy())
  assert np.all(np.isfinite(ratio)) and np.all(np.isfinite(ax)) and np.all(np.isfinite(r))
  if k and k%20==0:checkpoint('MODAL_ITERATION',{n:AVAILABLE[n] for n in ('modal_projection_iterate','modal_projection_action','modal_projection_residual','modal_projection_history','modal_projection_search')},dict(kind='resumable_unqualified_modal_projection_iterate',iteration=k))
  pending=active&(ratio>LINEAR_TOL)
  if not np.any(pending):return x,ax,r,np.asarray(history,dtype=float)
  assert k<MODAL_CAP,'Modal projection iteration cap retained'
  if k:
   z=mode_preconditioner(r,pre);capture('modal_projection_preconditioned_residual',z);newrz=np.sum(r*z,axis=(1,2,3));capture('modal_updated_rz',newrz);assert np.all(newrz[pending]>0) and np.all(np.isfinite(newrz));beta=np.zeros(32);beta[pending]=newrz[pending]/rz[pending];capture('modal_beta',beta);p=z+beta[:,None,None,None]*p;capture('modal_projection_search',p);rz=newrz;capture('modal_rz',rz)
  p[~pending]=0;capture('modal_projection_search',p);ap=mode_action(p,b,g);capture('current_modal_search_action',ap);pa=np.sum(p*ap,axis=(1,2,3));capture('modal_search_energy',pa);assert np.all(pa[pending]>0) and np.all(rz[pending]>0) and np.all(np.isfinite(pa))
  alpha=np.zeros(32);alpha[pending]=rz[pending]/pa[pending];capture('modal_alpha',alpha);x=x+alpha[:,None,None,None]*p;capture('modal_projection_iterate',x)



# Private definitions-only admission/load fragment. No helper is evaluated by author.
# Requires existing path, sha, read_pair, json interfaces in the guarded producer.
NODAL_MAP_WHOLE='CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002'
NODAL_MAP_Q1='CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001'
NODAL_MAP_COMPACT='CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002'
NODAL_MAP_Q1_OWNER_PID=26129
NODAL_MAP_PINS={
 'cross_u_whole_slice_cauchy_data_v002.py':'6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7',
 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002.md':'0b9529c22d9a007e96e6088387dee5b578d9620914e6933f45d9fd28e80fdb91',
 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RESULT.json':'af0365e378a46c727108c7df57f527994a22b7428d72b1f67c6f1bbac93667ed',
 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RECEIPT.json':'88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9',
 'cross_u_whole_slice_q1_adm_residual_v001.py':'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a',
 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001.md':'e5c7762d97fc6f2cd759cab4f303aa3a7463ab33e45001161d25bdf80c1ec440',
 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RESULT.json':'6c323ea0b01169c37c6c6c9960d7469ed57386148ff6022cc3d2bbc6da0b493b',
 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RECEIPT.json':'2919b4ab5715a7cff10a73836b6db65018520b234f65d1fb00f40c4581854f13',
 'cross_u_saved_full_native_adm_constraint_sources_v002.py':'1236e6b6837dd0356f7aae55bcf3d8ee4ed0ce3b4530907580990430e021d880',
 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002.md':'609ad771c8d7e3487d7db4545a76343452c91d773e8c6138de71ebcb92518b6c',
 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002_RESULT.json':'82dc17bc2d3d5ab730110887ea24c67d5b5b99fdff843397d98b455a8b5f29d2',
 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002_RECEIPT.json':'bdbe52eaf088bf2139d1bc7c385dcee755cd1fffcbbfef8467d86c85edfc46a7',
 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json':'3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c'}

def nodal_map_admission():
 # Hard-stop before reading any current Q1 output until authentic terminal pins.
 assert NODAL_MAP_Q1_OWNER_PID is not None and all(h is not None for h in NODAL_MAP_PINS.values())
 pins={}
 def add(n,h):
  n=str(path(n).resolve());assert isinstance(h,str) and len(h)==64 and (n not in pins or pins[n]==h);pins[n]=h
 for n,h in NODAL_MAP_PINS.items():add(n,h)
 parents={}
 for stem,pid,status,ncontrol,npair in ((NODAL_MAP_WHOLE,24903,'CONDITIONAL_WHOLE_SLICE_CAUCHY_INVENTORY_PASS',92,22),(NODAL_MAP_Q1,NODAL_MAP_Q1_OWNER_PID,'CONDITIONAL_WHOLE_Q1_ADM_RESIDUAL_ARITHMETIC_PASS',77,23),(NODAL_MAP_COMPACT,23177,'CONDITIONAL_CANONICAL_CONSTRAINT_SOURCE_ARITHMETIC_PASS',42,6)):
  result=json.loads(path(stem+'_RESULT.json').read_text());receipt=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert receipt['status']=='CLOSED' and receipt['owner']==result['owner'] and receipt['owner']['owner']=='root' and receipt['owner']['pid']==pid
  assert receipt['result_sha256']==NODAL_MAP_PINS[stem+'_RESULT.json'] and result['status']==status
  assert len(result['controls'])==ncontrol and all(c['passed'] for c in result['controls']) and len(result['checkpoints'])==npair
  assert [c['sigma'] for c in result['cases']]==[.1,1.,10.,100.] and all(v is False for v in result['qualification'].values())
  for key in ('input_sha256','output_sha256'):
   for n,h in receipt[key].items():add(n,h)
  for rec in result['checkpoints']:
   assert receipt['output_sha256'][rec['file']]==rec['sha256'] and receipt['output_sha256'][rec['commit_file']]==rec['commit_sha256']
   assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
   assert rec['metadata']['owner']==receipt['owner'] and all(v is False for v in rec['metadata']['qualification'].values())
  parents[stem]=(result,receipt)
 for n,h in pins.items():assert sha(path(n))==h,n
 def resolve(ref):
  rec=json.loads(path(ref['commit_file']).read_text());assert rec['file']==ref['file'] and rec['sha256']==ref['sha256']
  assert sha(path(ref['commit_file']))==ref['commit_sha256']
  return dict(rec,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])
 whole,whole_rc=parents[NODAL_MAP_WHOLE];q1,q1_rc=parents[NODAL_MAP_Q1];compact,compact_rc=parents[NODAL_MAP_COMPACT]
 assert whole_rc['owner']['source_sha256']==NODAL_MAP_PINS['cross_u_whole_slice_cauchy_data_v002.py']
 assert q1_rc['owner']['source_sha256']==NODAL_MAP_PINS['cross_u_whole_slice_q1_adm_residual_v001.py']
 wc=next(c for c in whole['cases'] if c['sigma']==1.);qc=next(c for c in q1['cases'] if c['sigma']==1.);cc=next(c for c in compact['cases'] if c['sigma']==1.)
 whole_sigma1=dict(wc,columns=[resolve(r) for r in wc['columns']],input=whole['checkpoints'][0],geometry=whole['checkpoints'][1],compact=cc['checkpoint'])
 q1_sigma1=dict(qc,columns=[resolve(r) for r in qc['columns']],input=q1['checkpoints'][0])
 assert len(whole_sigma1['columns'])==len(q1_sigma1['columns'])==4
 fixed=whole['checkpoints'][0]['metadata']['fixed'];cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text())
 assert fixed['eps']==cp['eps']==1e-5 and fixed['Q0_over_Hstar']==100 and whole['checkpoints'][0]['metadata']['owned_EPS5_background']==cp['background']
 assert q1['checkpoints'][0]['metadata']['fixed']==fixed and q1['checkpoints'][0]['metadata']['owned_EPS5_background']==cp['background']
 def schema(md,n,shape,dtype='float64'):assert md['schema'][n]==dict(shape=shape,dtype=dtype,finite=True),n
 for iq,(wr,qr) in enumerate(zip(whole_sigma1['columns'],q1_sigma1['columns'])):
  wm,qm=wr['metadata'],qr['metadata'];assert wm['column']==qm['column']==iq and wm['sigma']==qm['sigma']==1. and wm['points']==qm['points']==3784
  assert qm['whole_parent_file']==wr['file'] and qm['whole_parent_sha256']==wr['sha256'] and qm['compact_parent_file']==cc['checkpoint']['file'] and qm['compact_parent_sha256']==cc['checkpoint']['sha256']
  native=dict(g=[3784,4,4],hi=[3784,4,4],Ga=[3784,4,4,4],U=[3784,4],du=[3784,4,4],z=[32,3784,4],dz=[32,3784,4,4],phi=[3784,4],Pi=[32,3784,4,4],PiU=[3784,4,4],native_canonical_density=[3784,99],R=[3784],Z=[3784],Phi=[3784],reference_volume=[3784])
  for n,shape in native.items():schema(wm,n,shape)
  for n in ('cell_i','cell_j'):schema(wm,n,[3784],'int64')
  for a in range(4):
   for k in ('shape','shape_R','shape_Z'):schema(wm,f'corner{a}_{k}',[3784])
  selected=(1972,1972,1938,1938)[iq];schema(wm,'compact_reused_whole_indices',[selected],'int64');schema(wm,'new_whole_indices',[3784-selected],'int64')
  owned=dict(owned_du_increment=[3784,4,4],owned_dz_increment=[32,3784,4,4],owned_connection_increment=[3784,4,4,4],owned_native_canonical_density=[3784,99],owned_native_Pi=[32,3784,4,4],owned_native_PiU=[3784,4,4],owned_metric_native_p=[3784,6],owned_metric_total_p=[3784,3,3])
  for n,shape in owned.items():schema(qm,n,shape)
  for n,shape in dict(ih=[3784,3,3],N=[3784],beta=[3784,3],u=[3784,3],up=[3784,3],gamma=[3784],JU=[3784,4,3],JzU=[32,3784,3],Jzz=[3784,3],dens=[3784],old_velocity=[3784,99]).items():schema(qm,'owned_chart_'+n,shape)
  # Fixed-H forcing exists in two authentic partitions; no completed action replay.
  schema(cc['checkpoint']['metadata'],f'q{iq}_metric_only_native_momentum_delta',[selected,99]);schema(cc['checkpoint']['metadata'],f'q{iq}_original_native_rhs',[selected,99])
  schema(qm,'new_metric_only_native_momentum_delta',[3784-selected,99]);schema(qm,'new_original_native_rhs',[3784-selected,99])
  schema(qm,f'copied_q{iq}_native_p',[selected,99]);schema(qm,'new_native_p',[3784-selected,99])
  for n in ('R','Z','reference_volume'):
   schema(whole_sigma1['geometry']['metadata'],f'q{iq}_{n}',[3784])
  for a in range(4):
   for k in ('shape','shape_R','shape_Z'):schema(whole_sigma1['geometry']['metadata'],f'q{iq}_corner{a}_{k}',[3784])
 return pins,whole_sigma1,q1_sigma1,fixed,cp

def read_native_column(rec):
 # Primitive positions/old jets and every real Q1 hat come from WHOLE, not Q1.
 names=('g','hi','U','z','native_canonical_density','R','Z','reference_volume','cell_i','cell_j','compact_reused_whole_indices','new_whole_indices')+tuple(f'corner{a}_{k}' for a in range(4) for k in ('shape','shape_R','shape_Z'))
 return read_pair(rec,names)

def read_owned_column(rec):
 # Target density is copied old p; actual pstar must use both saved current partitions.
 # old_velocity supplies vstar only; no nodal velocity compatibility is assumed.
 iq=rec['metadata']['column'];assert iq in (0,1,2,3)
 names=('owned_native_canonical_density',f'copied_q{iq}_native_p','new_native_p')+tuple('owned_chart_'+k for k in ('ih','N','beta','u','gamma','JU','JzU','Jzz','dens','old_velocity'))
 return read_pair(rec,names)


def weak_mass_fixtures(w):
    w=np.asarray(w,dtype=np.float64)
    assert w.shape==(32,) and np.all(np.isfinite(w)) and np.all(w>0)
    x=np.array([0.,.5,1.]);qweight=np.full(3,1./3.)
    e=np.array([[1.,0.],[.5,.5],[0.,1.]])
    E=np.concatenate(((1-x)[:,None,None]*np.eye(3)[None],x[:,None,None]*np.eye(3)[None]),axis=2)
    G=np.einsum('q,qai,qaj->ij',qweight,E,E)
    exact_G=np.kron(np.array([[5.,1.],[1.,5.]])/12.,np.eye(3))
    RAW.update(fixture_weak_x=x,fixture_weak_qweight=qweight,fixture_weak_scalar_hats=e,fixture_weak_E=E,fixture_weak_G=G,fixture_weak_G_exact=exact_G,fixture_weak_weights=w)
    check('weak_mass_abstract_hat_Gram',G,exact_G,np.einsum('q,qai,qaj->ij',qweight,abs(E),abs(E)))
    u=np.array([0.,0.,0.,1.,0.,0.]);eu=np.einsum('qai,i->qa',E,u)
    RAW.update(fixture_weak_U_coefficients=u,fixture_weak_U_values=eu)
    D=w[:,None,None]*G[None]
    RAW['fixture_weak_modal_D']=D.copy()
    selector=np.diag([1.,0.,0.])
    for varying in (False,True):
        label='varying' if varying else 'constant'
        L=(x if varying else np.ones(3))[:,None,None]*selector[None]
        LE=np.einsum('qab,qbi->qai',L,E)
        Bbase=np.einsum('q,qai,qaj->ij',qweight,LE,E)
        Abase=np.einsum('q,qai,qaj->ij',qweight,LE,LE)
        B=w[:,None,None]*Bbase[None]
        A=G+w.sum()*Abase
        RAW.update({f'fixture_weak_{label}_L':L,f'fixture_weak_{label}_LE':LE,f'fixture_weak_{label}_B':B,f'fixture_weak_{label}_A':A})
        dsolve=np.linalg.solve(D,B.transpose(0,2,1))
        RAW[f'fixture_weak_{label}_Dsolve_BT']=dsolve.copy()
        elimination=np.einsum('jik,jkl->il',B,dsolve)
        schur=A-elimination
        expected=exact_G.copy()
        if varying:
            expected+=w.sum()*np.kron(np.array([[1.,-1.],[-1.,1.]])/72.,selector)
        env=abs(G)+w.sum()*np.einsum('q,qai,qaj->ij',qweight,abs(LE),abs(LE))+np.einsum('jik,jkl->il',abs(B),abs(dsolve))
        RAW.update({f'fixture_weak_{label}_elimination':elimination,f'fixture_weak_{label}_Schur':schur,f'fixture_weak_{label}_Schur_expected':expected,f'fixture_weak_{label}_Schur_envelope':env})
        check(f'weak_mass_{label}_projection_Schur',schur,expected,env)
        if varying:
            rhs=-np.einsum('jki,k->ji',B,u)
            RAW['fixture_weak_varying_minimizer_rhs']=rhs.copy()
            z=np.linalg.solve(D,rhs[:,:,None])[:,:,0]
            RAW['fixture_weak_varying_minimizer']=z.copy()
            target=np.einsum('qab,qb->qa',L,eu)
            projected=np.einsum('qai,ji->jqa',E,z)
            residual=projected+target[None]
            expected_z=np.broadcast_to(np.array([1./12.,0.,0.,-11./12.,0.,0.]),(32,6)).copy()
            expected_residual=np.zeros((32,3,3));expected_residual[:,:,0]=np.array([1./12.,-1./6.,1./12.])[None]
            RAW.update(fixture_weak_varying_target=target,fixture_weak_varying_projected=projected,fixture_weak_varying_residual=residual,fixture_weak_varying_expected_minimizer=expected_z,fixture_weak_varying_expected_residual=expected_residual)
            check('weak_mass_varying_exact_LS_residual',residual,expected_residual,abs(projected)+abs(target)[None]+abs(expected_residual))
            orthogonal=np.einsum('q,qai,jqa->ji',qweight,E,residual)
            orthogonal_env=np.einsum('q,qai,jqa->ji',qweight,abs(E),abs(projected)+abs(target)[None])
            RAW.update(fixture_weak_varying_orthogonal=orthogonal,fixture_weak_varying_orthogonal_envelope=orthogonal_env)
            check('weak_mass_varying_LS_orthogonality',orthogonal,np.zeros_like(orthogonal),orthogonal_env)
            objective=np.einsum('j,q,jqa,jqa->',w,qweight,residual,residual)
            expected_objective=w.sum()/72.
            objective_env=np.einsum('j,q,jqa,jqa->',w,qweight,abs(projected)+abs(target)[None],abs(projected)+abs(target)[None])
            RAW.update(fixture_weak_varying_objective=np.array(objective),fixture_weak_varying_expected_objective=np.array(expected_objective),fixture_weak_varying_objective_envelope=np.array(objective_env))
            check('weak_mass_varying_nonzero_projection_remainder',np.array(objective),np.array(expected_objective),np.array(objective_env))

# Six independent gates: abstract mass; constant Schur; varying Schur;
# varying LS residual; weighted orthogonality; exact nonzero objective.
# Rational identities, independent of all physical frequency and state choices:
# G_scalar = [[5,1],[1,5]]/12;
# B_varying/w = [[1,1],[1,9]]/24 (first component only);
# A_mode_varying/w = [[1,1],[1,17]]/48 (first component only);
# (A_mode-B D^-1 B^T)/w = [[1,-1],[-1,1]]/72.
# For nodal U first component (0,1), z_min=(1/12,-11/12),
# residual=(1/12,-1/6,1/12), objective=sum_j w_j/72.


def evaluate_envelope(x,g,jet=0):
 y=lift_velocity(abs(x));out=np.zeros(x.shape[:-3]+(4,86,44,3))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44)
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   h=abs(g['hats'][iq,a,jet]);f=np.broadcast_to(h[...,None],(86,44,3)).copy();f[...,2]=R**2*h
   if jet==1:f[...,2]+=2*R*abs(g['hats'][iq,a,0])
   out[...,iq,:,:,:]+=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)*f
 return out.reshape(x.shape[:-3]+(15136,3))

def independent_point_action(v,b):
 B=np.einsum('jpki,jpkl->jpil',b['L'],b['D'],optimize=True)
 A=b['M0']+np.einsum('jpik,jpkl->pil',B,b['L'],optimize=True)
 return np.concatenate(((np.einsum('pik,pk->pi',A,v[0],optimize=True)+np.einsum('jpik,jpk->pi',B,v[1:],optimize=True))[None],np.einsum('jpik,jpk->jpi',b['D'],v[1:],optimize=True)+np.einsum('jpki,pk->jpi',B,v[0],optimize=True)))

def linear_gate(label,residual,rhs,scale,modal=False):
 axes=(1,2,3) if modal else None
 if modal:
  a=np.linalg.norm(residual.reshape(32,-1),axis=1);d=np.linalg.norm(rhs.reshape(32,-1),axis=1);aa=np.linalg.norm((residual/scale).reshape(32,-1),axis=1);dd=np.linalg.norm((rhs/scale).reshape(32,-1),axis=1)
 else:a=np.array([np.linalg.norm(residual)]);d=np.array([np.linalg.norm(rhs)]);aa=np.array([np.linalg.norm(residual/scale)]);dd=np.array([np.linalg.norm(rhs/scale)])
 ratios=np.zeros((len(a),2));active=d>0;ratios[active,0]=a[active]/d[active];ratios[active,1]=aa[active]/dd[active]
 for n,v in (('residual_norm',a),('rhs_norm',d),('scaled_residual_norm',aa),('scaled_rhs_norm',dd),('actual',ratios)):RAW[label+'_'+n]=v.copy()
 assert np.all(np.isfinite(a)) and np.all(np.isfinite(d)) and np.all(np.isfinite(aa)) and np.all(np.isfinite(dd)) and np.all(np.isfinite(ratios))
 assert np.all((d>0)==(dd>0)) and np.all(a[~active]==0) and np.all(aa[~active]==0)
 k=len(CHECKS);error=float(np.max(ratios,initial=0));row=dict(ordinal=k,name=label,error=error,tolerance=LINEAR_TOL,passed=error<=LINEAR_TOL);CHECKS.append(row);assert row['passed'],row

def geometry_controls(cols,r,z):
 global RAW
 start=len(CHECKS);R=np.stack([c['R'] for c in cols]);dv=np.stack([c['reference_volume'] for c in cols]);hats=np.stack([np.stack([np.stack([c[f'corner{a}_{k}'].reshape(86,44) for k in ('shape','shape_R','shape_Z')]) for a in range(4)]) for c in cols])
 g=dict(R=R,dv=dv,hats=hats,cell_i=cols[0]['cell_i'].copy(),cell_j=cols[0]['cell_j'].copy())
 for name,a in g.items():capture('geometry_'+name,a)
 assert R.shape==(4,3784) and hats.shape==(4,4,3,86,44) and np.all(R>0) and np.all(dv>0) and np.all(hats[:,:,0]>0)
 for c in cols:assert np.array_equal(c['cell_i'],g['cell_i']) and np.array_equal(c['cell_j'],g['cell_j'])
 ci,cj=np.indices((86,44));assert np.array_equal(g['cell_i'],ci.ravel()) and np.array_equal(g['cell_j'],cj.ravel())
 summed=hats.sum(axis=1);target=np.zeros_like(summed);target[:,0]=1;check('authentic_hat_partition_and_derivatives',summed,target,abs(hats).sum(axis=1)+abs(target))
 ir=np.arange(87)[:,None];iz=np.arange(45)[None,:];group=np.arange(33)[:,None,None,None];component=np.arange(3)[None,:,None,None]
 x=np.sin(.13*(group+1)+.11*(component+1)+.07*ir+.03*iz)*native_mask()[None];y=np.cos(.17*(group+1)+.09*(component+1)+.05*ir+.04*iz)*native_mask()[None]
 capture('manufactured_nodal_x',x);capture('manufactured_nodal_y',y)
 field=np.stack([np.column_stack((np.sin(.01*rr),np.cos(.02*rr),np.ones_like(rr))) for rr in R]).reshape(15136,3)
 ev=evaluate_velocity(x,g);dual=scatter_velocity(np.broadcast_to(field,(33,15136,3)),g);wq=(dv/R).reshape(15136)
 a=np.array(dot(x,dual));expected=np.array(np.einsum('p,jpi,pi->',wq,ev,field));env=np.array(dot(abs(x),scatter_velocity(np.broadcast_to(abs(field),(33,15136,3)),g))+np.einsum('p,jpi,pi->',wq,evaluate_envelope(x,g),abs(field)))
 check('native_axis_sheet_basis_adjoint',a,expected,env)
 phi=np.zeros((3,87,45));phi[2]=1;pv=evaluate_velocity(phi,g);pr=evaluate_velocity(phi,g,1);pz=evaluate_velocity(phi,g,2);rr=R.reshape(15136)
 actual=np.column_stack((pv[:,2],pr[:,2],pz[:,2]));expect=np.column_stack((rr**2,2*rr,np.zeros_like(rr)));en=np.column_stack((evaluate_envelope(phi,g)[:,2],evaluate_envelope(phi,g,1)[:,2],evaluate_envelope(phi,g,2)[:,2]))+abs(expect)
 check('regular_covector_phi_value_and_derivatives',actual,expect,en)
 counts=np.array([np.count_nonzero(native_mask()),33*np.count_nonzero(native_mask())],dtype=np.int64);check('independent_native_basis_dimension',counts,np.array([11524,380292]),abs(counts))
 check('independent_native_point_scatter',dual,scatter_velocity_independent(np.broadcast_to(field,(33,15136,3)),g),scatter_velocity(np.broadcast_to(abs(field),(33,15136,3)),g))
 RAW.update(manufactured_nodal_x=x,manufactured_nodal_y=y,manufactured_qpoint_field=field,manufactured_evaluated_x=ev,manufactured_dual_load=dual,manufactured_phi_value=pv,manufactured_phi_R=pr,manufactured_phi_Z=pz,native_independent_mask=native_mask(),r_kpc=r,z_kpc=z)
 RAW.update({k:a for k,a in AVAILABLE.items() if k.startswith('geometry_')});rec=checkpoint('GEOMETRY',RAW,dict(kind='genuine_affine_native_temporal_basis',controls=CHECKS[start:],outer_scope='all instantaneous velocity coefficients retained; no continued wall trace supplied',covector_phi='R² times even scalar coefficient',nodes=[87,45],independent_native_coefficients=380292))
 return g,x,y,rec

def new_map(whole,q1,fixed,cp):
 global RAW,AVAILABLE
 ev=read_pair(whole['input'],('r_kpc','z_kpc','xi','weights'));r,z,xi,w=(ev[k] for k in ('r_kpc','z_kpc','xi','weights'))
 assert r.shape==(87,) and z.shape==(45,) and xi.shape==w.shape==(32,) and r[0]==z[0]==0 and np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
 checkpoint('INPUT',ev,dict(kind='unchanged_grid_spectrum_and_closed_parent_references',sigma=SIGMA,fixed=fixed,owned_background=cp['background'],whole_columns=[dict(file=c['file'],sha256=c['sha256']) for c in whole['columns']],owned_columns=[dict(file=c['file'],sha256=c['sha256']) for c in q1['columns']],basis_note_sha256=PINS['CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_MAP_AND_BASIS_V001.md']))
 RAW={};start=len(CHECKS);weak_mass_fixtures(w);checkpoint('FIXTURE',RAW,dict(kind='six_independent_two_node_projection_identities',controls=CHECKS[start:],scope='artificial algebra only; not physical galaxy data'))
 cols=[]
 for wr,qr in zip(whole['columns'],q1['columns']):
  c=read_native_column(wr);owned=read_owned_column(qr);assert not set(c)&set(owned);c.update(owned)
  for name,a in c.items():AVAILABLE[f'loaded_q{qr["metadata"]["column"]}_'+name]=a.copy()
  ix=c['compact_reused_whole_indices'];ox=c['new_whole_indices'];assert np.array_equal(np.sort(np.r_[ix,ox]),np.arange(3784))
  actual=np.empty((3784,99));actual[ix]=owned[f'copied_q{qr["metadata"]["column"]}_native_p'];actual[ox]=owned['new_native_p'];c['actual_owned_native_density']=actual;RAW[f'loaded_actual_owned_density_q{qr["metadata"]["column"]}']=actual.copy();cols.append(c)
 RAW={};g,mx,my,geometry=geometry_controls(cols,r,z)
 RAW={};AVAILABLE={};start=len(CHECKS);omega=SIGMA*xi*fixed['Hunit']/299792458.;block=coefficients(cols,w,omega)
 old=np.concatenate([c['native_canonical_density'] for c in cols]).reshape(15136,33,3).transpose(1,0,2)
 assert np.array_equal(old,block['target']);check('immutable_native_momentum_density_copy',old,block['target'],abs(old)+abs(block['target']))
 point=point_action(block['velocity'],block);pbound=point_action_envelope(block['velocity'],block);check('independent_point_kinetic_block_expansion',point,independent_point_action(block['velocity'],block),pbound)
 ax=original_action(mx,block,g);ay=original_action(my,block,g);be=np.array(dot(abs(mx),original_envelope(my,block,g))+dot(abs(my),original_envelope(mx,block,g)));check('genuine_weak_native_bilinear_symmetry',np.array(dot(mx,ay)),np.array(dot(my,ax)),be)
 gap=block['pstar']-block['target'];rhs=scatter_velocity(point-gap,g);rhsenv=scatter_velocity(pbound+abs(block['pstar'])+abs(block['target']),g)
 capture('implicit_fixed_time_baseline',block['pstar']-point);capture('point_kinetic_seed_action',point);capture('point_kinetic_seed_envelope',pbound);capture('original_weak_rhs',rhs);capture('original_weak_rhs_envelope',rhsenv);capture('original_weak_momentum_target',scatter_velocity(old,g));AVAILABLE.update({k:a for k,a in RAW.items() if k.startswith('control_')})
 checkpoint('COEFFICIENT',AVAILABLE,dict(kind='complete_fixed_metric_native99_mass_coefficients',controls=CHECKS[start:],sigma=SIGMA,points=15136,all_modes=32,time_jet='authenticated owned-H chart velocities; no metric nodal velocity inferred',momentum_map='p_star+M(v-v_star)',physical_changes=[]))
 RAW={};AVAILABLE={};start=len(CHECKS);pre=preconditioner(block,g,r)
 pmx=apply_preconditioner(mx,pre);pmy=apply_preconditioner(my,pre);check('positive_block_preconditioner_bilinear_symmetry',np.array(dot(mx,pmy)),np.array(dot(my,pmx)),np.array(dot(abs(mx),abs(pmy))+dot(abs(my),abs(pmx))))
 AVAILABLE.update({k:a for k,a in RAW.items() if k.startswith('control_')});checkpoint('PREPARATION',AVAILABLE,dict(kind='preconditioner_only_positive_node_block',controls=CHECKS[start:],actual_operator_mass_lumped=False,actual_operator_Maxwell_substitution=False))
 RAW={};AVAILABLE={};start=len(CHECKS);capture('original_weak_rhs',rhs);capture('original_weak_rhs_envelope',rhsenv);solution,action,residual,history=solve_native(rhs,block,g,pre)
 v=evaluate_velocity(solution,g);dv=v-block['velocity'];delta=point_action(dv,block);recovered=block['pstar']+delta;defect=gap+delta;capture('recovered_point_momentum_density',recovered);capture('point_momentum_projection_defect',defect)
 independent=scatter_velocity_independent(independent_point_action(v,block),g);aenv=original_envelope(solution,block,g);check('original_weak_action_independent_expansion',action,independent,aenv+abs(independent))
 weakdefect=scatter_velocity(defect,g);env=original_envelope(solution,block,g)+rhsenv;check('point_defect_true_weak_residual_identity',weakdefect,-residual,env)
 linear_gate('native_original_and_congruence_norm',residual,rhs,pre['normscale'])
 finite_real('recovered_nodal_native_velocity',solution);finite_real('recovered_qpoint_native_velocity',v);finite_real('recovered_qpoint_native_velocity_R',evaluate_velocity(solution,g,1));finite_real('recovered_qpoint_native_velocity_Z',evaluate_velocity(solution,g,2));capture('original_weak_action_envelope',aenv);capture('original_weak_point_defect',weakdefect)
 AVAILABLE.update({k:a for k,a in RAW.items() if k.startswith('control_') or k.startswith('native_original_and')});srec=checkpoint('SOLUTION',AVAILABLE,dict(kind='conditional_sigma1_weak_native_velocity_projection',controls=CHECKS[start:],sigma=SIGMA,iterations=int(history[-1,0]),linear_tolerance=LINEAR_TOL,pointwise_momentum_identity_claim=False,spatial_field_Euler_claim=False,temporal_wall_trace=None))
 RAW={};AVAILABLE={};start=len(CHECKS);uonly=np.zeros_like(solution);uonly[0]=solution[0];vu=evaluate_velocity(uonly,g);rhsmodal=-scatter_velocity(np.einsum('jpik,jpk->jpi',block['D'],np.einsum('jpik,pk->jpi',block['L'],vu[0],optimize=True),optimize=True),g);capture('projection_modal_rhs',rhsmodal)
 zmin,ma,mr,mhist=solve_modal(rhsmodal,block,g,pre);linear_gate('all32_projection_original_and_congruence_norms',mr,rhsmodal,pre['normscale'][1:],modal=True)
 test=uonly.copy();test[1:]=zmin;vv=evaluate_velocity(test,g);mixed=vv[1:]+np.einsum('jpik,pk->jpi',block['L'],vv[0],optimize=True);wq=(g['dv']/g['R']).reshape(15136)
 energy=np.einsum('p,jpi,jpik,jpk->j',wq,mixed,block['D'],mixed,optimize=True);capture('projection_remainder_each_mode',energy);assert np.all(np.isfinite(energy)) and np.all(energy>=0)
 full=original_action(test,block,g);check('projection_modal_original_action_identity',full[1:],ma-rhsmodal,scatter_velocity(np.einsum('jpik,jpk->jpi',block['eD'],abs(vv[1:])+np.einsum('jpik,pk->jpi',block['eL'],abs(vv[0]),optimize=True),optimize=True),g)+abs(ma)+abs(rhsmodal))
 maxwell=scatter_velocity(np.einsum('pik,pk->pi',block['M0'],vv[0],optimize=True),g);actual=np.array(dot(solution[0],full[0]-maxwell));expected=np.array(energy.sum()-dot(zmin,full[1:]));en=np.array(dot(abs(solution[0]),original_envelope(test,block,g)[0]+abs(maxwell))+dot(abs(zmin),abs(full[1:]))+abs(energy).sum());check('retained_global_projection_remainder_quadratic',actual,expected,en)
 finite_real('projection_minimizer_nodal',zmin);finite_real('projection_qpoint_defect',mixed);capture('projection_original_full_action',full);capture('projection_Maxwell_only_action',maxwell);capture('projection_original_modal_weak_residual',full[1:]);capture('projection_remainder_total',np.array(energy.sum()));AVAILABLE.update({k:a for k,a in RAW.items() if k.startswith('control_') or k.startswith('all32_projection')});prec=checkpoint('PROJECTION',AVAILABLE,dict(kind='all32_independent_modal_mass_minimizers_and_FE_remainder',controls=CHECKS[start:],projection_remainder_discarded=False,physical_stability_claim=False,iterations=int(mhist[-1,0])))
 return dict(sigma=SIGMA,status='CONDITIONAL_WEAK_NATIVE_LEGENDRE_PASS',solution=srec,projection=prec,qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded weak native nodal map: exact CLOSED pins and FULL reviews required.')
 assert PROTOCOL_SHA and len(PROTOCOL_SHA)==64 and sha(path(STEM+'.md'))==PROTOCOL_SHA
 assert not list(BASE.glob(STEM+'_*')),'Unused namespace required; old outputs preserved'
 INPUTS,whole,q1,fixed,cp=nodal_map_admission()
 for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():assert sha(path(n))==h;INPUTS[str(path(n).resolve())]=h
 INPUTS[str(Path(__file__).resolve())]=sha(__file__);OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,sigma=SIGMA,configuration=dict(native_components=99,modes=32,points=15136,grid=[87,45],independent_native_coefficients=380292,native_cap=NATIVE_CAP,modal_cap=MODAL_CAP,arithmetic_tolerance=TOL,linear_tolerance=LINEAR_TOL),qualification=FLAGS))
  import numpy as _np
  np=_np;case=new_map(whole,q1,fixed,cp);assert len(CHECKS)==21 and all(c['passed'] for c in CHECKS)
  normal=[r for r in RECORDS if r['metadata']['kind'] not in ('resumable_unqualified_native_iterate','resumable_unqualified_modal_projection_iterate')];assert len(normal)==7 and len(RECORDS)<=23
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_WEAK_NATIVE_LEGENDRE_ARITHMETIC_PASS',cases=[case],controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS))
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\nGenuine sigma1 weak native99 velocity map and all32 modal projection remainders; original weak equations certified. No metric solve, source adjustment or physical galaxy velocity is inferred.\n\nThe pointwise momentum projection defect, true weak residual and all unfinished iterates remain explicit. Exterior/time/source histories are unregistered.\n').encode());recheck();rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);recheck();print('CONDITIONAL_WEAK_NATIVE_LEGENDRE_ARITHMETIC_PASS',len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None;available=dict(AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unqualified_available_weak_native_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  if prior:OUTPUTS[STEM+'_RECEIPT.json']=prior
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=[p.name for p in BASE.glob(STEM+'*.npz') if p.name not in {r['file'] for r in RECORDS}],qualification=FLAGS))
  if prior is None:json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS))
  seal_actual();recheck(False);raise

if __name__=='__main__':raise SystemExit(main())
