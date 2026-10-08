"""Guarded genuine weak nodal native99 temporal map; root-only evaluation."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback,ast,zipfile,struct
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001'
PARENT='CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
PARENT_OWNER=None
PINS={}
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
   h=geo['hats'][iq,a,jet];factor=np.broadcast_to(h,(86,44,3)).copy();factor[...,2]=R**2*h
   if jet==1:factor[...,2]+=2*R*geo['hats'][iq,a,0]
   out[...,iq,:,:,:]+=np.moveaxis(y[..., :,i:86+i,j:44+j],-3,-1)*factor
 return out.reshape(x.shape[:-3]+(15136,3))

def scatter_velocity(field,geo):
 assert field.shape[-2:]==(15136,3)
 f=field.reshape(field.shape[:-2]+(4,86,44,3));out=np.zeros(field.shape[:-2]+(3,87,45))
 for iq in range(4):
  R=geo['R'][iq].reshape(86,44);wq=geo['dv'][iq].reshape(86,44)/R
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   factor=np.broadcast_to(geo['hats'][iq,a,0],(86,44,3)).copy();factor[...,2]*=R**2
   out[..., :,i:86+i,j:44+j]+=np.moveaxis(f[...,iq,:,:,:]*wq[...,None]*factor,-1,-3)
 return restrict_velocity(out)

def scatter_velocity_independent(field,geo):
 out=np.zeros(field.shape[:-2]+(3,87,45));prefix=field.shape[:-2];groups=int(math.prod(prefix)) if prefix else 1;fo=field.reshape(groups,15136,3);oo=out.reshape(groups,3,87,45)
 for iq in range(4):
  R=geo['R'][iq];wq=geo['dv'][iq]/R;f=fo[:,iq*3784:(iq+1)*3784]
  for a,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for c in range(3):
    scale=R**2 if c==2 else np.ones_like(R)
    val=f[...,c]*wq*geo['hats'][iq,a,0]*scale
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
 names=('g','hi','U','z','owned_chart_ih','owned_chart_N','owned_chart_beta','owned_chart_u','owned_chart_gamma','owned_chart_JU','owned_chart_JzU','owned_chart_Jzz','owned_chart_dens','owned_chart_old_velocity','owned_native_canonical_density')
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
 return dict(L=L,D=D,M0=M0,eL=eL,eD=eD,eM0=eM0,velocity=vel,target=target)

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
 dz=np.linalg.solve(pre['D'],r[1:]);red=r[0]-np.einsum('jnik,jnk->ni',pre['B'],dz,optimize=True);u=np.linalg.solve(pre['M0'],red)
 z=np.linalg.solve(pre['D'],r[1:]-np.einsum('jnki,nk->jni',pre['B'],u,optimize=True));y=np.concatenate((u[None],z))/pre['scale'][None]
 return y.reshape(33,87,45,3).transpose(0,3,1,2)*pre['mask'][None]

def dot(a,b):return float(np.sum(a*b))

def solve_native(rhs,b,g,pre):
 x=np.zeros_like(rhs);r=rhs.copy();z=apply_preconditioner(r,pre);p=z.copy();rz=dot(r,z);scale=pre['normscale'];den=float(np.linalg.norm(rhs/scale));history=[]
 assert math.isfinite(den)
 for k in range(NATIVE_CAP+1):
  ax=original_action(x,b,g);r=rhs-ax;ratio=float(np.linalg.norm(r/scale))/den if den else 0.
  history.append((k,ratio));AVAILABLE.update(native_iterate=x.copy(),native_original_action=ax.copy(),native_original_residual=r.copy(),native_history=np.asarray(history,dtype=float),native_search=p.copy(),native_preconditioned_residual=z.copy())
  if ratio<=LINEAR_TOL:return x,ax,r,np.asarray(history,dtype=float)
  assert k<NATIVE_CAP,'Native weak map iteration cap retained'
  if k:
   z=apply_preconditioner(r,pre);newrz=dot(r,z);assert newrz>0 and math.isfinite(newrz);p=z+(newrz/rz)*p;rz=newrz
  ap=original_action(p,b,g);pa=dot(p,ap);capture('current_native_search_action',ap);assert pa>0 and rz>0 and math.isfinite(pa) and math.isfinite(rz)
  alpha=rz/pa;assert math.isfinite(alpha);x=x+alpha*p

def mode_action(x,b,g):
 v=evaluate_velocity(x,g);return scatter_velocity(np.einsum('jpik,jpk->jpi',b['D'],v,optimize=True),g)

def mode_preconditioner(rhs,pre):
 r=rhs.transpose(0,2,3,1).reshape(32,3915,3)/pre['scale'][None];y=np.linalg.solve(pre['D'],r)/pre['scale'][None]
 return y.reshape(32,87,45,3).transpose(0,3,1,2)*pre['mask'][None]

def solve_modal(rhs,b,g,pre):
 x=np.zeros_like(rhs);r=rhs.copy();z=mode_preconditioner(r,pre);p=z.copy();rz=np.sum(r*z,axis=(1,2,3));scale=pre['normscale'][1:];den=np.linalg.norm((rhs/scale).reshape(32,-1),axis=1);active=den>0;history=[]
 for k in range(MODAL_CAP+1):
  ax=mode_action(x,b,g);r=rhs-ax;ratio=np.zeros(32);ratio[active]=np.linalg.norm((r/scale).reshape(32,-1),axis=1)[active]/den[active]
  history.append(np.r_[k,ratio]);AVAILABLE.update(modal_projection_iterate=x.copy(),modal_projection_action=ax.copy(),modal_projection_residual=r.copy(),modal_projection_history=np.asarray(history,dtype=float),modal_projection_search=p.copy())
  pending=active&(ratio>LINEAR_TOL)
  if not np.any(pending):return x,ax,r,np.asarray(history,dtype=float)
  assert k<MODAL_CAP,'Modal projection iteration cap retained'
  if k:
   z=mode_preconditioner(r,pre);newrz=np.sum(r*z,axis=(1,2,3));assert np.all(newrz[pending]>0) and np.all(np.isfinite(newrz));beta=np.zeros(32);beta[pending]=newrz[pending]/rz[pending];p=z+beta[:,None,None,None]*p;rz=newrz
  p[~pending]=0;ap=mode_action(p,b,g);pa=np.sum(p*ap,axis=(1,2,3));capture('current_modal_search_action',ap);assert np.all(pa[pending]>0) and np.all(rz[pending]>0) and np.all(np.isfinite(pa))
  alpha=np.zeros(32);alpha[pending]=rz[pending]/pa[pending];x=x+alpha[:,None,None,None]*p

