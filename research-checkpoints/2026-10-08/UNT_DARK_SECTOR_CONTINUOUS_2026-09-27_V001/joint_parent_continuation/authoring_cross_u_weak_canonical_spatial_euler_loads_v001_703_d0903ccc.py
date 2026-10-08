"""Guarded new canonical spatial Euler-load coefficients; authoring in progress."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback,ast,zipfile,struct
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
B=None;TOL=2e-11;EXPECTED_CONTROLS=None
np=None;GEO=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(spatial_Euler_loads_qualified=False,CMC_qualified=False,force_convective_qualified=False,physical_metric_qualified=False,history_qualified=False,exterior_qualified=False,physical_inertia_qualified=False,source_qualified=False,galaxy_velocity_qualified=False)
PINS={}

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

def point_metric_tensor(k):
 # k represents a symmetric metric VELOCITY; offdiagonal k values are actual hdot_ij.
 out=np.zeros(k.shape[:-1]+(3,3));out[...,0,0]=k[...,0];out[...,1,1]=k[...,1];out[...,2,2]=k[...,2]
 for a,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):out[...,i,j]=out[...,j,i]=k[...,a]
 return out

def tensor_velocity_coordinates(hdot):
 return np.stack((hdot[...,0,0],hdot[...,1,1],hdot[...,2,2],hdot[...,0,1],hdot[...,0,2],hdot[...,1,2]),axis=-1)

def tensor_momentum_coordinates(pi):
 return np.stack((pi[...,0,0],pi[...,1,1],pi[...,2,2],2*pi[...,0,1],2*pi[...,0,2],2*pi[...,1,2]),axis=-1)

def lower(g,v):return np.einsum('pab,...pb->...pa',g,v)

def lower_last(g,v):return np.einsum('pab,pcb->pca',g,v)

def raise_cov(hi,v):return np.einsum('pab,...pb->...pa',hi,v)

def covdot(hi,a,b):return np.einsum('...pa,...pa->...p',raise_cov(hi,a),b)

def features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w):
 # du/dz have derivative index first; z and dz are COVECTORS.
 nu=du+np.einsum('pbal,pl->pab',Ga,U)
 nz=dz-np.einsum('plab,jpl->jpab',Ga,z)
 uc=lower(g,U);P=np.eye(4)[None,:,:]+np.einsum('pa,pb->pab',uc,U)
 q=np.einsum('pa,jpab->jpb',U,nz);V=np.einsum('pab,jpb->jpa',P,q)
 D=np.einsum('pac,jpcd,pbd->jpab',P,nz,P)
 F=lower_last(g,nu)-np.swapaxes(lower_last(g,nu),1,2)
 # lower_last(g,nu) lowers nu's last (vector) index, leaving derivative index first.
 a=np.einsum('pa,pab->pb',U,nu);r=np.einsum('pab,pb->pa',P,phi)
 z2=covdot(hi,z,z);f=1+z2/((B*GC)**2*xi[:,None]**4)
 Vu=raise_cov(hi,V);Du=np.einsum('pac,jpcd,pdb->jpab',hi,D,hi)
 Pi=w[:,None,None,None]*(np.einsum('pa,jpb->jpab',U,Vu)/omega[:,None,None,None]**2-ELL**2*Du)
 nuc=lower_last(g,nu);mu=np.einsum('jpab,pab->jp',Pi,nuc)
 Z=np.einsum('j,jpa->pa',w,z);Fup=np.einsum('pac,pcd,pdb->pab',hi,F,hi)
 PiU=-ALPHA*np.einsum('pac,pcb->pab',hi,F)+np.einsum('pa,pb->pab',U,Z)
 Aj=(np.einsum('jpn,jprn->jpr',Vu,nz)+np.einsum('jpa,pa->jp',q,U)[:,:,None]*V)/omega[:,None,None]**2
 Aj-=ELL**2*(np.einsum('jprn,jpn->jpr',D,Vu)
        +np.einsum('jpmr,jpmn,pn->jpr',np.einsum('pmc,jpcr->jpmr',hi,D),nz,U))
 # In the second projector term raise D's FIRST index; rho stays lower.
 Q=np.einsum('pa,pa->p',U,phi);Ur=np.einsum('pa,pa->p',U,r)
 A=-(Q[:,None]*r+Ur[:,None]*phi)+np.einsum('pn,prn->pr',Z,nu)+np.einsum('j,jpr->pr',w,Aj)
 out=dict(g=g,hi=hi,Ga=Ga,U=U,du=du,z=z,dz=dz,phi=phi,omega=omega,xi=xi,w=w,nu=nu,nz=nz,uc=uc,P=P,q=q,V=V,D=D,a=a,r=r,f=f,z2=z2,Pi=Pi,mu=mu,Z=Z,F=F,Fup=Fup,PiU=PiU,A=A)
 RAW.update({f'current_{k}':v for k,v in out.items() if isinstance(v,np.ndarray)})
 return out

def variation(s,eta,deta,zeta,dzeta):
 g,hi,Ga=s['g'],s['hi'],s['Ga'];U=s['U'];z=s['z'];w=s['w'];om=s['omega'];P=s['P']
 ne=deta+np.einsum('pbal,pl->pab',Ga,eta)
 nzeta=dzeta-np.einsum('plab,jpl->jpab',Ga,zeta)
 ec=lower(g,eta);dP=np.einsum('pa,pb->pab',ec,U)+np.einsum('pa,pb->pab',s['uc'],eta)
 dq=np.einsum('pa,jpab->jpb',eta,s['nz'])+np.einsum('pa,jpab->jpb',U,nzeta)
 dV=np.einsum('pab,jpb->jpa',dP,s['q'])+np.einsum('pab,jpb->jpa',P,dq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,s['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,s['nz'],dP)+np.einsum('pac,jpcd,pbd->jpab',P,nzeta,P)
 dF=lower_last(g,ne)-np.swapaxes(lower_last(g,ne),1,2)
 da=np.einsum('pa,pab->pb',eta,s['nu'])+np.einsum('pa,pab->pb',U,ne)
 dr=np.einsum('pab,pb->pa',dP,s['phi'])
 # Raw terms and TERMwise absolute contraction sums, before any integration/cancellation.
 mterms=[raise_cov(hi,s['V'])*dV/om[:,None,None]**2,
  -raise_cov(hi,z)*zeta,-(s['z2']/((B*GC)**2*s['xi'][:,None]**4))[:,:,None]*raise_cov(hi,z)*zeta,
  -ELL**2*np.einsum('pac,jpcd,pdb->jpab',hi,s['D'],hi)*dD,
  da[None,:,:]*z+s['a'][None,:,:]*zeta]
 md=np.stack([np.sum(t,axis=tuple(range(2,t.ndim))) for t in mterms],axis=-1)
 me=np.stack([np.sum(abs(t),axis=tuple(range(2,t.ndim))) for t in mterms],axis=-1)
 mx=-ALPHA*s['Fup']*dF/2;ph=-raise_cov(hi,s['r'])*dr
 terms=np.column_stack((mx.sum(axis=(1,2)),ph.sum(axis=1),np.einsum('j,jpk->pk',w,md)))
 env=np.column_stack((abs(mx).sum(axis=(1,2)),abs(ph).sum(axis=1),np.einsum('j,jpk->pk',w,me)))
 weakU=np.sum(s['A']*eta,axis=1)+np.sum(s['PiU']*ne,axis=(1,2))
 potential=w[:,None]*np.sum((s['a'][None,:,:]-s['f'][:,:,None]*raise_cov(hi,z))*zeta,axis=-1)
 weakmode=potential+np.einsum('jpab,jpab->jp',s['Pi'],nzeta)
 unitjet=2*(np.einsum('pab,pb->pa',lower_last(g,s['nu']),eta)+np.einsum('pb,pab->pa',s['uc'],ne))
 constraint=np.column_stack((2*np.einsum('pa,pa->p',s['uc'],eta),unitjet))
 dc=np.einsum('pa,jpa->jp',eta,z)+np.einsum('pa,jpa->jp',U,zeta)
 ddc=np.einsum('pab,jpb->jpa',ne,z)+np.einsum('pb,jpab->jpa',eta,s['nz'])+np.einsum('pab,jpb->jpa',s['nu'],zeta)+np.einsum('pb,jpab->jpa',U,nzeta)
 RAW.update(current_eta=eta,current_eta_partial=deta,current_zeta=zeta,current_zeta_partial=dzeta,current_direct_terms=terms,current_envelope=env,current_weakU=weakU,current_weakmode=weakmode,current_mode_envelope=me,current_constraint=constraint,current_delta_transverse=dc,current_delta_transverse_jet=ddc)
 return terms,env,md,weakU,weakmode,constraint,dc,ddc

def metric_partial(s):
 # Metric compatibility recovers the same exact first metric jet, no second derivatives.
 a=np.einsum('plam,pln->pamn',s['Ga'],s['g'])
 return a+np.swapaxes(a,2,3)

def connection_delta(s,q,dq):
 nq=dq-np.einsum('plam,pln->pamn',s['Ga'],q)-np.einsum('plan,pml->pamn',s['Ga'],q)
 dG=np.zeros_like(s['Ga'])
 for a in range(4):
  for b in range(4):dG[:,:,a,b]=np.einsum('plm,pm->pl',s['hi'],nq[:,a,b,:]+nq[:,b,a,:]-nq[:,:,a,b])/2
 return dG

def metric_native(s,q,dq,eta,deta):
 hi,g,U,z,P=s['hi'],s['g'],s['U'],s['z'],s['P'];w=s['w'];om=s['omega'];kj=(B*GC)**2*s['xi'][:,None]**4
 dG=connection_delta(s,q,dq);dhi=-np.einsum('pac,pcd,pdb->pab',hi,q,hi)
 dnu=deta+np.einsum('pbal,pl->pab',dG,U)+np.einsum('pbal,pl->pab',s['Ga'],eta)
 dnz=-np.einsum('plab,jpl->jpab',dG,z)
 duc=lower(q,U)+lower(g,eta);dP=np.einsum('pa,pb->pab',duc,U)+np.einsum('pa,pb->pab',s['uc'],eta)
 dqq=np.einsum('pa,jpab->jpb',eta,s['nz'])+np.einsum('pa,jpab->jpb',U,dnz)
 dV=np.einsum('pab,jpb->jpa',dP,s['q'])+np.einsum('pab,jpb->jpa',P,dqq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,s['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,dnz,P)+np.einsum('pac,jpcd,pbd->jpab',P,s['nz'],dP)
 lower_nu=lower_last(q,s['nu'])+lower_last(g,dnu);dF=lower_nu-np.swapaxes(lower_nu,1,2)
 da=np.einsum('pa,pab->pb',eta,s['nu'])+np.einsum('pa,pab->pb',U,dnu);dr=np.einsum('pab,pb->pa',dP,s['phi'])
 z2=s['z2'];V2=covdot(hi,s['V'],s['V']);F2=np.sum(s['Fup']*s['F'],axis=(1,2));r2=covdot(hi,s['r'],s['r'])
 Du=np.einsum('pac,jpcd,pdb->jpab',hi,s['D'],hi);D2=np.sum(Du*s['D'],axis=(2,3));az=np.einsum('pa,jpa->jp',s['a'],z)
 dz2=covdot(dhi,z,z);dV2=covdot(dhi,s['V'],s['V'])+2*covdot(hi,s['V'],dV)
 dD2=2*np.sum(Du*dD,axis=(2,3))+np.einsum('pac,jpab,pbd,jpcd->jp',dhi,s['D'],hi,s['D'])+np.einsum('pac,jpab,pbd,jpcd->jp',hi,s['D'],dhi,s['D'])
 dF2=2*np.sum(s['Fup']*dF,axis=(1,2))+np.einsum('pac,pab,pbd,pcd->p',dhi,s['F'],hi,s['F'])+np.einsum('pac,pab,pbd,pcd->p',hi,s['F'],dhi,s['F'])
 dr2=covdot(dhi,s['r'],s['r'])+2*covdot(hi,s['r'],dr);daz=np.einsum('pa,jpa->jp',da,z)
 modal=np.stack((V2/(2*om[:,None]**2),-z2/2,-z2*z2/(4*kj),-ELL**2*D2/2,az),axis=-1)
 dm=np.stack((dV2/(2*om[:,None]**2),-dz2/2,-z2*dz2/(2*kj),-ELL**2*dD2/2,daz),axis=-1)
 primal=np.column_stack((-ALPHA*F2/4,-r2/2,np.einsum('j,jpk->pk',w,modal)))
 derivative=np.column_stack((-ALPHA*dF2/4,-dr2/2,np.einsum('j,jpk->pk',w,dm)))
 lm=np.einsum('pab,pba->p',hi,q)/2
 total=derivative+lm[:,None]*primal
 # Sum absolute tensor products BEFORE contractions or inter-term cancellation.
 def quad_env(hh,v):return np.einsum('pab,jpa,jpb->jp',abs(hh),abs(v),abs(v))
 ez=quad_env(hi,z);ev=quad_env(hi,s['V']);ed=np.einsum('pac,jpab,pbd,jpcd->jp',abs(hi),abs(s['D']),abs(hi),abs(s['D']))
 edz=quad_env(dhi,z);edv=quad_env(dhi,s['V'])+2*np.sum(abs(raise_cov(hi,s['V'])*dV),axis=-1)
 edd=2*np.sum(abs(Du*dD),axis=(2,3))+np.einsum('pac,jpab,pbd,jpcd->jp',abs(dhi),abs(s['D']),abs(hi),abs(s['D']))+np.einsum('pac,jpab,pbd,jpcd->jp',abs(hi),abs(s['D']),abs(dhi),abs(s['D']))
 ef=np.einsum('pac,pab,pbd,pcd->p',abs(hi),abs(s['F']),abs(hi),abs(s['F']))
 edf=2*np.sum(abs(s['Fup']*dF),axis=(1,2))+np.einsum('pac,pab,pbd,pcd->p',abs(dhi),abs(s['F']),abs(hi),abs(s['F']))+np.einsum('pac,pab,pbd,pcd->p',abs(hi),abs(s['F']),abs(dhi),abs(s['F']))
 er=np.einsum('pab,pa,pb->p',abs(hi),abs(s['r']),abs(s['r']));edr=np.einsum('pab,pa,pb->p',abs(dhi),abs(s['r']),abs(s['r']))+2*np.sum(abs(raise_cov(hi,s['r'])*dr),axis=-1)
 mp=np.stack((ev/(2*om[:,None]**2),ez/2,ez*ez/(4*kj),ELL**2*ed/2,np.sum(abs(s['a'][None,:,:]*z),axis=-1)),axis=-1)
 em=np.stack((edv/(2*om[:,None]**2),edz/2,ez*edz/(2*kj),ELL**2*edd/2,np.sum(abs(da[None,:,:]*z),axis=-1)),axis=-1)
 el=np.einsum('pab,pba->p',abs(hi),abs(q))/2
 penv=np.column_stack((ALPHA*ef/4,er/2,np.einsum('j,jpk->pk',w,mp)))
 denv=np.column_stack((ALPHA*edf/4,edr/2,np.einsum('j,jpk->pk',w,em)))
 env=denv+el[:,None]*penv
 per_mode=w[:,None,None]*(dm+lm[None,:,None]*modal)
 menv=w[:,None,None]*(em+el[None,:,None]*mp)
 operands=dict(delta_connection=dG,delta_inverse=dhi,delta_U=eta,delta_U_partial=deta,log_measure_tangent=lm,raw_native_primal=primal,raw_native_no_measure=derivative,per_mode_metric_terms=per_mode,per_mode_metric_envelope=menv)
 RAW.update({'current_metric_'+k:v for k,v in operands.items()})
 return total,env,operands

def metric_basis():
 e=np.zeros((6,3,3))
 for k,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[k,i,j]=e[k,j,i]=1
 return e

def chart_spacetime_jets(s,c):
 # Actual first jets, including the replaced nodal native time rate.
 dg=metric_partial(s);hi=s['hi'];dhi=-np.einsum('pij,pajk,pkl->pail',hi,dg,hi)
 N=c['N'];ga=c['gamma'];be=c['beta'];ih=c['ih'];up=c['up'];U=s['U'];z=s['z']
 dN=N[:,None]**3*dhi[:,:,0,0]/2
 db=2*N[:,None,None]*dN[:,:,None]*hi[:,None,0,1:]+N[:,None,None]**2*dhi[:,:,0,1:]
 dh=dg[:,:,1:,1:];dih=-np.einsum('pij,pajk,pkl->pail',ih,dh,ih)
 du=np.einsum('paim,pm->pai',dg[:,:,1:,:],U)+np.einsum('pim,pam->pai',s['g'][:,1:,:],s['du'])
 dup=np.einsum('pij,paj->pai',ih,du)+np.einsum('paij,pj->pai',dih,c['u'])
 dga=(np.einsum('pi,pai->pa',up,du)-np.einsum('pi,paij,pj->pa',up,dh,up)/2)/ga[:,None]
 dJU=np.empty((len(U),4,4,3));dJU[:,:,0,:]=dup/(N*ga)[:,None,None]-c['JU'][:,None,0,:]*(dN/N[:,None]+dga/ga[:,None])[:,:,None]
 dJU[:,:,1:,:]=dih-db[:,:,:,None]*c['JU'][:,None,None,0,:]-be[:,None,:,None]*dJU[:,:,None,0,:]
 dJzz=-s['du'][:,:,1:]/U[:,None,0,None]+U[:,None,1:]*s['du'][:,:,0,None]/U[:,None,0,None]**2
 dJzU=-(np.einsum('jpam,pmi->jpai',s['dz'],c['JU'])+np.einsum('jpm,pami->jpai',z,dJU))/U[None,:,None,0,None]
 dJzU+=np.einsum('jpm,pmi->jpi',z,c['JU'])[:,:,None,:]*s['du'][None,:,:,0,None]/U[None,:,None,0,None]**2
 e=metric_basis();t=np.einsum('pi,kij,pj->pk',up,e,up);dt=2*np.einsum('pai,kij,pj->pak',dup,e,up)
 dUh=np.empty((len(U),4,6,4));dUh[:,:,:,0]=-dt/(2*N*ga)[:,None,None]-c['Uh'][:,None,:,0]*(dN/N[:,None]+dga/ga[:,None])[:,:,None]
 dUh[:,:,:,1:]=-np.einsum('paij,kjl,pl->paki',dih,e,up)-np.einsum('pij,kjl,pal->paki',ih,e,dup)-db[:,:,None,:]*c['Uh'][:,None,:,0,None]-be[:,None,None,:]*dUh[:,:,:,0,None]
 dzh=-(np.einsum('jpam,pkm->jpak',s['dz'],c['Uh'])+np.einsum('jpm,pakm->jpak',z,dUh))/U[None,:,None,0,None]
 dzh+=np.einsum('jpm,pkm->jpk',z,c['Uh'])[:,:,None,:]*s['du'][None,:,:,0,None]/U[None,:,None,0,None]**2
 dem=np.zeros((len(U),4,6,4,4));dem[:,:,:,0,1:]=np.einsum('kij,paj->paki',e,db);dem[:,:,:,1:,0]=dem[:,:,:,0,1:]
 dem[:,:,:,0,0]=2*np.einsum('pai,kij,pj->pak',db,e,be)
 out=dict(dg=dg,dhi=dhi,dN=dN,dbeta=db,dh=dh,dih=dih,du_cov=du,dup=dup,dgamma=dga,dJU=dJU,dJzU=dJzU,dJzz=dJzz,dUh=dUh,dzh=dzh,dembed=dem)
 for k,v in out.items():capture('chart_first_'+k,v)
 return out

def canonical_native_coefficients(s,c,cj):
 # Covariant derivative of the configuration Jacobian, not velocity-only jets.
 Ga=s['Ga'];JU=c['JU'];Jzu=c['JzU'];Jzz=c['Jzz'];Pi=s['Pi'];pu=s['PiU'];p=len(s['U'])
 nJU=cj['dJU']+np.einsum('pral,pli->pari',Ga,JU)
 nJzu=np.zeros((32,p,4,4,3));nJzu[:,:,:,0,:]=cj['dJzU'];nJzu-=np.einsum('pan,jpi->jpani',Ga[:,0],Jzu)
 nJzz=np.empty((p,4,4,3))
 for i in range(3):nJzz[:,:,:,i]=-Ga[:,i+1]-Ga[:,0]*Jzz[:,None,None,i]
 nJzz[:,:,0,:]+=cj['dJzz']
 Az=s['w'][:,None,None]*(s['a'][None]-s['f'][:,:,None]*raise_cov(s['hi'],s['z']))
 Au=np.einsum('pr,pri->pi',s['A'],JU)+np.einsum('par,pari->pi',pu,nJU)+np.einsum('jp,jpi->pi',Az[:,:,0],Jzu)+np.einsum('jpan,jpani->pi',Pi,nJzu)
 Azcan=Az[:,:,1:]+Az[:,:,0,None]*Jzz[None]+np.einsum('jpan,pani->jpi',Pi,nJzz)
 Pu=np.einsum('par,pri->pai',pu,JU)+np.einsum('jpa,jpi->pai',Pi[:,:,:,0],Jzu)
 Pz=Pi[:,:,:,1:]+Pi[:,:,:,0,None]*Jzz[None,:,None,:]
 ac=np.concatenate((Au,Azcan.transpose(1,0,2).reshape(p,96)),axis=1)
 pc=np.concatenate((Pu,Pz.transpose(1,2,0,3).reshape(p,4,96)),axis=2)
 dens=c['dens'];co=np.stack((ac,pc[:,1],pc[:,2]),axis=-1)*dens[:,None,None]
 eAu=np.einsum('pr,pri->pi',abs(s['A']),abs(JU))+np.einsum('par,pari->pi',abs(pu),abs(nJU))+np.einsum('jp,jpi->pi',abs(Az[:,:,0]),abs(Jzu))+np.einsum('jpan,jpani->pi',abs(Pi),abs(nJzu))
 eAz=abs(Az[:,:,1:])+abs(Az[:,:,0,None]*Jzz[None])+np.einsum('jpan,pani->jpi',abs(Pi),abs(nJzz))
 ePu=np.einsum('par,pri->pai',abs(pu),abs(JU))+np.einsum('jpa,jpi->pai',abs(Pi[:,:,:,0]),abs(Jzu))
 ePz=abs(Pi[:,:,:,1:])+abs(Pi[:,:,:,0,None]*Jzz[None,:,None,:])
 ea=np.concatenate((eAu,eAz.transpose(1,0,2).reshape(p,96)),axis=1);ep=np.concatenate((ePu,ePz.transpose(1,2,0,3).reshape(p,4,96)),axis=2)
 eco=np.stack((ea,ep[:,1],ep[:,2]),axis=-1)*dens[:,None,None]
 out=dict(coefficient=co,envelope=eco,momentum=dens[:,None]*pc[:,0],momentum_envelope=dens[:,None]*ep[:,0],A_can=ac,P_can=pc,A_z_raw=Az,nJU=nJU,nJzu=nJzu,nJzz=nJzz)
 for k,v in out.items():capture('native_config_'+k,v)
 return out

def native_configuration_lift(s,c,cj,value,dvalue):
 p=len(s['U']);assert value.shape==(p,99) and dvalue.shape==(p,4,99)
 vu=value[:,:3];vz=value[:,3:].reshape(p,32,3).transpose(1,0,2);du=dvalue[:,:,:3];dz=dvalue[:,:,3:].reshape(p,4,32,3).transpose(2,0,1,3)
 eta=np.einsum('pri,pi->pr',c['JU'],vu)
 deta=np.einsum('pari,pi->par',cj['dJU'],vu)+np.einsum('pri,pai->par',c['JU'],du)
 zeta=np.zeros_like(s['z']);zeta[:,:,1:]=vz;zeta[:,:,0]=np.einsum('jpi,pi->jp',c['JzU'],vu)+np.einsum('pi,jpi->jp',c['Jzz'],vz)
 dzeta=np.zeros_like(s['dz']);dzeta[:,:,:,1:]=dz
 dzeta[:,:,:,0]=np.einsum('jpai,pi->jpa',cj['dJzU'],vu)+np.einsum('jpi,pai->jpa',c['JzU'],du)+np.einsum('pai,jpi->jpa',cj['dJzz'],vz)+np.einsum('pi,jpai->jpa',c['Jzz'],dz)
 return eta,deta,zeta,dzeta

def metric_configuration_lift(s,c,cj,a,f,df):
 assert a in range(6) and df.shape==(len(f),4) and np.all(df[:,0]==0)
 q=c['embed'][:,a]*f[:,None,None];dq=cj['dembed'][:,:,a]*f[:,None,None,None]+c['embed'][:,None,a]*df[:,:,None,None]
 eta=c['Uh'][:,a]*f[:,None];deta=cj['dUh'][:,:,a]*f[:,None,None]+c['Uh'][:,None,a]*df[:,:,None]
 ze=np.zeros_like(s['z']);dze=np.zeros_like(s['dz']);ze[:,:,0]=c['zh'][:,:,a]*f[None]
 dze[:,:,:,0]=cj['dzh'][:,:,:,a]*f[None,:,None]+c['zh'][:,:,None,a]*df[None]
 return q,dq,eta,deta,ze,dze

def EH_spatial_metric_direction(s,c,cj,H,dH,R):
 # First derivative 3D curvature + ADM/GHY kinetic representative, divided by R.
 assert dH.shape==(len(R),4,3,3) and np.all(dH[:,0]==0)
 ih=c['ih'];dh=cj['dh'][:,1:];dHsp=dH[:,1:];ratio=c['sqrt_h']/R;p=len(R)
 dih=-np.einsum('pij,pajk,pkl->pail',ih,dh,ih);delta_ih=-np.einsum('pij,pjk,pkl->pil',ih,H,ih)
 delta_dih=-np.einsum('pij,pajk,pkl->pail',delta_ih,dh,ih)-np.einsum('pij,pajk,pkl->pail',ih,dHsp,ih)-np.einsum('pij,pajk,pkl->pail',ih,dh,delta_ih)
 G=np.zeros((p,3,3,3));dG=np.zeros_like(G)
 for i in range(3):
  for j in range(3):
   jet=dh[:,i,j,:]+dh[:,j,i,:]-dh[:,:,i,j];dj=dHsp[:,i,j,:]+dHsp[:,j,i,:]-dHsp[:,:,i,j]
   G[:,:,i,j]=np.einsum('plm,pm->pl',ih,jet)/2
   dG[:,:,i,j]=(np.einsum('plm,pm->pl',delta_ih,jet)+np.einsum('plm,pm->pl',ih,dj))/2
 bar=np.zeros_like(G);bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 cc=G-bar;dc=dG;tr=np.einsum('plil->pi',cc);dt=np.einsum('plil->pi',dc)
 theta=np.einsum('pij,pij->p',ih,H)/2;dratio=ratio*theta
 ri=ratio[:,None]*np.einsum('pij,paij->pa',ih,dh)/2;ri[:,0]-=ratio/R
 dri=dratio[:,None]*np.einsum('pij,paij->pa',ih,dh)/2+ratio[:,None]*(np.einsum('pij,paij->pa',delta_ih,dh)+np.einsum('pij,paij->pa',ih,dHsp))/2;dri[:,0]-=dratio/R
 N=c['N'];Ni=cj['dN'][:,1:];V=(N*ratio)[:,None,None]*ih;dV=N[:,None,None]*(dratio[:,None,None]*ih+ratio[:,None,None]*delta_ih)
 DV=(Ni*ratio[:,None]+N[:,None]*ri)[:,:,None,None]*ih[:,None]+(N*ratio)[:,None,None,None]*dih
 dDV=(Ni*dratio[:,None]+N[:,None]*dri)[:,:,None,None]*ih[:,None]+(Ni*ratio[:,None]+N[:,None]*ri)[:,:,None,None]*delta_ih[:,None]+(N*dratio)[:,None,None,None]*dih+(N*ratio)[:,None,None,None]*delta_dih
 DV+=np.einsum('pial,plj->paij',bar,V)+np.einsum('pjal,pil->paij',bar,V)
 dDV+=np.einsum('pial,plj->paij',bar,dV)+np.einsum('pjal,pil->paij',bar,dV)
 aa=np.einsum('pkij,pk->pij',cc,tr)-np.einsum('plik,pkjl->pij',cc,cc)
 daa=np.einsum('pkij,pk->pij',dc,tr)+np.einsum('pkij,pk->pij',cc,dt)-np.einsum('plik,pkjl->pij',dc,cc)-np.einsum('plik,pkjl->pij',cc,dc)
 rt=np.column_stack((-np.einsum('plij,plij->p',dDV,cc)-np.einsum('plij,plij->p',DV,dc),np.einsum('pjij,pi->p',dDV,tr)+np.einsum('pjij,pi->p',DV,dt),np.einsum('pij,pij->p',dV,aa)+np.einsum('pij,pij->p',V,daa)))/(2*C)
 eaa=np.einsum('pkij,pk->pij',abs(cc),abs(tr))+np.einsum('plik,pkjl->pij',abs(cc),abs(cc))
 edaa=np.einsum('pkij,pk->pij',abs(dc),abs(tr))+np.einsum('pkij,pk->pij',abs(cc),abs(dt))+np.einsum('plik,pkjl->pij',abs(dc),abs(cc))+np.einsum('plik,pkjl->pij',abs(cc),abs(dc))
 er=np.column_stack((np.einsum('plij,plij->p',abs(dDV),abs(cc))+np.einsum('plij,plij->p',abs(DV),abs(dc)),np.einsum('pjij,pi->p',abs(dDV),abs(tr))+np.einsum('pjij,pi->p',abs(DV),abs(dt)),np.einsum('pij,pij->p',abs(dV),eaa)+np.einsum('pij,pij->p',abs(V),edaa)))/(2*C)
 K=c['K'];kt=c['Ktrace'];ku=np.einsum('pik,pkl,plj->pij',ih,K,ih);mix=np.einsum('pik,pkl->pil',ih,K)
 Q=np.einsum('pij,pij->p',K,ku)-kt**2
 Lie=np.einsum('pk,pkij->pij',c['beta'],dHsp)+np.einsum('pik,pjk->pij',H,cj['dbeta'][:,1:])+np.einsum('pkj,pik->pij',H,cj['dbeta'][:,1:])
 dK=-Lie/(2*N[:,None,None]);kk=np.einsum('pik,pkj->pij',mix,ku)
 it=np.column_stack((theta*Q,2*np.einsum('pij,pij->p',ku-kt[:,None,None]*ih,dK),-2*np.einsum('pij,pij->p',kk-kt[:,None,None]*ku,H)))*(N*ratio)[:,None]/(2*C)
 ei=np.column_stack((abs(theta)*(np.einsum('pij,pij->p',abs(K),abs(ku))+kt**2),2*np.einsum('pij,pij->p',abs(ku)+abs(kt[:,None,None]*ih),abs(dK)),2*np.einsum('pij,pij->p',np.einsum('pik,pkj->pij',abs(mix),abs(ku))+abs(kt[:,None,None]*ku),abs(H))))*(N*ratio)[:,None]/(2*C)
 raw=dict(curvature_terms=rt,curvature_envelope=er,kinetic_terms=it,kinetic_envelope=ei,C3=cc,delta_C3=dc,V=V,delta_V=dV,barDV=DV,delta_barDV=dDV,delta_K=dK)
 for k,v in raw.items():capture('EH_config_'+k,v)
 return dict(terms=np.column_stack((rt,it)),envelope=np.column_stack((er,ei)),value=rt.sum(axis=1)+it.sum(axis=1),raw=raw)

def phase_metric_direction(s,q,P,PX,X):
 dhi=-np.einsum('pac,pcd,pdb->pab',s['hi'],q,s['hi']);dX=-np.einsum('pa,pab,pb->p',s['phi'],dhi,s['phi'])/(2*X)
 lm=np.einsum('pab,pba->p',s['hi'],q)/2
 terms=np.column_stack((PX*dX,P*lm));env=np.column_stack((abs(PX)*np.einsum('pa,pab,pb->p',abs(s['phi']),abs(dhi),abs(s['phi']))/(2*X),abs(P)*np.einsum('pab,pba->p',abs(s['hi']),abs(q))/2))
 return terms,env

def canonical_metric_coefficients(s,c,cj,R,P,PX,X):
 p=len(R);e=metric_basis();terms=np.empty((p,6,3,15));en=np.empty_like(terms)
 for a in range(6):
  for jet in range(3):
   f=np.full(p,float(jet==0));df=np.zeros((p,4))
   if jet:df[:,jet]=1
   q,dq,eta,deta,ze,dze=metric_configuration_lift(s,c,cj,a,f,df)
   nt,ne,_=metric_native(s,q,dq,eta,deta);zt,zev,*_=variation(s,np.zeros_like(eta),np.zeros_like(deta),ze,dze)
   phase,pe=phase_metric_direction(s,q,P,PX,X)
   H=e[a][None]*f[:,None,None];dH=e[a][None,None]*df[:,:,None,None]
   eh=EH_spatial_metric_direction(s,c,cj,H,dH,R)
   # Seven native terms include the complete z0 complement; phase2 and EH6.
   terms[:,a,jet,:7]=(nt+zt)*c['dens'][:,None];en[:,a,jet,:7]=(ne+zev)*c['dens'][:,None]
   terms[:,a,jet,7:9]=phase*c['dens'][:,None];en[:,a,jet,7:9]=pe*c['dens'][:,None]
   # All stored coefficients are coordinate densities; quadrature divides by R once.
   terms[:,a,jet,9:]=eh['terms']*R[:,None];en[:,a,jet,9:]=eh['envelope']*R[:,None]
   capture('metric_config_'+str(a)+'_'+str(jet)+'_terms',terms[:,a,jet].copy());capture('metric_config_'+str(a)+'_'+str(jet)+'_envelope',en[:,a,jet].copy())
 return dict(coefficient=terms.sum(axis=-1),envelope=en.sum(axis=-1),terms=terms,term_envelope=en)

def scatter_configuration_coefficients(co,g,kind,independent=False,envelope=False):
 # Coordinate-density coefficients: value/R/Z hat jets, reference_volume/R once.
 assert kind in ('native','metric') and co.shape==(15136,99 if kind=='native' else 6,3)
 out=np.zeros((33,3,87,45)) if kind=='native' else np.zeros((6,87,45))
 for iq in range(4):
  R=g['R'][iq];wq=g['dv'][iq]/R;qco=co[iq*3784:(iq+1)*3784]
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hats=g['hats'][iq,a].reshape(3,3784)
   if kind=='native':
    fac=np.broadcast_to(hats[:,:,None],(3,3784,3)).copy();fac[:,:,2]*=R[None]**2;fac[1,:,2]+=2*R*hats[0]
    if envelope:
     fac=np.broadcast_to(abs(hats)[:,:,None],(3,3784,3)).copy();fac[:,:,2]*=R[None]**2;fac[1,:,2]+=2*R*abs(hats[0])
    vals=np.einsum('pgcj,jpc->pgc',qco.reshape(3784,33,3,3),fac)*wq[:,None]
    vals=vals.transpose(1,2,0)
   else:
    F=metric_value_matrix(R);fac=hats[:,:,None,None]*F[None];fac[1]+=hats[0,:,None,None]*metric_R_matrix(R)
    if envelope:
     fac=abs(hats)[:,:,None,None]*abs(F[None]);fac[1]+=abs(hats[0,:,None,None])*abs(metric_R_matrix(R))
    vals=np.einsum('paj,jpab->pb',qco,fac)*wq[:,None];vals=vals.T
   if independent:
    for ix in np.ndindex(out.shape[:-2]):np.add.at(out[ix],(g['cell_i']+di,g['cell_j']+dj),vals[ix])
   else:out[...,di:86+di,dj:44+dj]+=vals.reshape(out.shape[:-2]+(86,44))
 return restrict_velocity(out) if kind=='native' else restrict_metric(out)

def ordinary_metric_force(g,p_specific,mass_weight):
 h=g[:,1:,1:];ih=np.linalg.inv(h);hi=np.linalg.inv(g);N=1/np.sqrt(-hi[:,0,0]);up=np.einsum('pij,pj->pi',ih,p_specific);ga=np.sqrt(1+np.sum(p_specific*up,axis=1));e=metric_basis()
 terms=np.einsum('pi,kij,pj->pk',up,e,up)*((mass_weight*N)/(2*ga))[:,None]
 env=np.einsum('pi,kij,pj->pk',abs(up),abs(e),abs(up))*((mass_weight*N)/(2*ga))[:,None]
 capture('ordinary_gamma',ga);capture('ordinary_up',up);capture('ordinary_metric_local_force',terms);capture('ordinary_metric_local_force_envelope',env)
 return terms,env

def ordinary_metric_load(source,r):
 R=source['source_R'];assert np.all(source['source_Z']==0);i=source['source_indices'];t=source['source_right_weight']
 assert np.all((i>=0)&(i<86)) and np.all((t>0)&(t<1))
 local,env=ordinary_metric_force(source['source_g'],source['source_specific_covariant_p'],source['source_mass_weight'])
 transformed=np.einsum('pa,pab->pb',local,metric_value_matrix(R));tenv=np.einsum('pa,pab->pb',env,abs(metric_value_matrix(R)))
 out=np.zeros((6,87,45));eo=np.zeros_like(out)
 for offset,h in ((0,1-t),(1,t)):
  for k in range(6):np.add.at(out[k,:,0],i+offset,transformed[:,k]*h);np.add.at(eo[k,:,0],i+offset,tenv[:,k]*h)
 capture('ordinary_metric_regular_point_force',transformed);capture('ordinary_metric_nodal_force',out);capture('ordinary_metric_nodal_envelope',eo)
 check('conserved_annular_force_basis_partition_and_location',np.r_[1-t+t,(1-t)*r[i]+t*r[i+1]],np.r_[np.ones(len(t)),R],np.r_[np.full(len(t),2.),abs((1-t)*r[i])+abs(t*r[i+1])+abs(R)])
 return restrict_metric(out),restrict_metric(eo)

WEAK_METRIC_PARENT="CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001"
WEAK_METRIC_WHOLE="CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002"
WEAK_METRIC_Q1="CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001"
WEAK_METRIC_PINS={'author_fragment_weak_metric_cmc_admission_v001.txt': 'f014280bd217b41cce1d70f5f0607e2bdf2e67c1ca795ddae8e4f61445ee269c', 'cross_u_whole_slice_cauchy_data_v002.py': '6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7', 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002.md': '0b9529c22d9a007e96e6088387dee5b578d9620914e6933f45d9fd28e80fdb91', 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RESULT.json': 'af0365e378a46c727108c7df57f527994a22b7428d72b1f67c6f1bbac93667ed', 'CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RECEIPT.json': '88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9', 'cross_u_whole_slice_q1_adm_residual_v001.py': 'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a', 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001.md': 'e5c7762d97fc6f2cd759cab4f303aa3a7463ab33e45001161d25bdf80c1ec440', 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RESULT.json': '6c323ea0b01169c37c6c6c9960d7469ed57386148ff6022cc3d2bbc6da0b493b', 'CROSS_U_WHOLE_SLICE_Q1_ADM_RESIDUAL_V001_RECEIPT.json': '2919b4ab5715a7cff10a73836b6db65018520b234f65d1fb00f40c4581854f13', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json': '3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c', 'cross_u_weak_nodal_native_legendre_v001.py': 'e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001.md': '2c9da869068cf3d2ae9269395b111ec1d0e71f26e0ffef6ff0afb50e40995a0e', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RESULT.json': 'e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5', 'CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_RECEIPT.json': '00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae', 'READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json': 'af16bda38df395882c54ca2b57bd7d9ed36cc3aae39b437687bc35930423d56d'}

def weak_metric_admission():
 pins={}
 def add(n,h):
  n=str(path(n).resolve());assert isinstance(h,str) and len(h)==64 and (n not in pins or pins[n]==h);pins[n]=h
 for n,h in WEAK_METRIC_PINS.items():add(n,h)
 parents={}
 specs=((WEAK_METRIC_PARENT,28469,'CONDITIONAL_WEAK_NATIVE_LEGENDRE_ARITHMETIC_PASS',21,10),(WEAK_METRIC_WHOLE,24903,'CONDITIONAL_WHOLE_SLICE_CAUCHY_INVENTORY_PASS',92,22),(WEAK_METRIC_Q1,26129,'CONDITIONAL_WHOLE_Q1_ADM_RESIDUAL_ARITHMETIC_PASS',77,23))
 for stem,pid,status,count,npair in specs:
  result=json.loads(path(stem+'_RESULT.json').read_text());receipt=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert receipt['status']=='CLOSED' and receipt['closed'] and receipt['owner']==result['owner'] and receipt['owner']['owner']=='root' and receipt['owner']['pid']==pid
  assert result['status']==status and receipt['result_sha256']==WEAK_METRIC_PINS[stem+'_RESULT.json']
  assert len(result['controls'])==count and all(c['passed'] for c in result['controls']) and len(result['checkpoints'])==npair and all(v is False for v in result['qualification'].values())
  for key in ('input_sha256','output_sha256'):
   for n,h in receipt[key].items():add(n,h)
  assert {p.name for p in path(stem+'_RESULT.json').parent.glob(stem+'_*.npz')}=={r['file'] for r in result['checkpoints']}
  assert {p.name for p in path(stem+'_RESULT.json').parent.glob(stem+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in result['checkpoints']}
  for rec in result['checkpoints']:
   assert receipt['output_sha256'][rec['file']]==rec['sha256'] and receipt['output_sha256'][rec['commit_file']]==rec['commit_sha256']
   assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
   assert rec['metadata']['owner']==receipt['owner'] and all(v is False for v in rec['metadata']['qualification'].values())
  parents[stem]=(result,receipt)
 for n,h in pins.items():assert sha(path(n))==h,n
 weak_result,weak_rc=parents[WEAK_METRIC_PARENT];whole,whole_rc=parents[WEAK_METRIC_WHOLE];q1,q1_rc=parents[WEAK_METRIC_Q1]
 assert weak_rc['owner']['source_sha256']==WEAK_METRIC_PINS['cross_u_weak_nodal_native_legendre_v001.py']
 assert whole_rc['owner']['source_sha256']==WEAK_METRIC_PINS['cross_u_whole_slice_cauchy_data_v002.py'] and q1_rc['owner']['source_sha256']==WEAK_METRIC_PINS['cross_u_whole_slice_q1_adm_residual_v001.py']
 assert [c['sigma'] for c in whole['cases']]==[.1,1.,10.,100.] and [c['sigma'] for c in q1['cases']]==[.1,1.,10.,100.]
 assert len(weak_result['cases'])==1 and weak_result['cases'][0]['sigma']==1. and weak_result['cases'][0]['status']=='CONDITIONAL_WEAK_NATIVE_LEGENDRE_PASS'
 audit=json.loads(path('READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json').read_text())
 assert audit['status']=='SAVED_PACKET_AUDIT_PASS' and audit['pair_count']==10 and audit['control_count']==21 and audit['terminal']['owner_pid']==28469
 for key,name in (('source_sha256','cross_u_weak_nodal_native_legendre_v001.py'),('result_sha256',WEAK_METRIC_PARENT+'_RESULT.json'),('receipt_sha256',WEAK_METRIC_PARENT+'_RECEIPT.json')):assert audit['terminal'][key]==WEAK_METRIC_PINS[name]
 def one(kind):
  rows=[r for r in weak_result['checkpoints'] if r['metadata']['kind']==kind];assert len(rows)==1;return rows[0]
 weak=dict(result=weak_result,receipt=weak_rc,case=weak_result['cases'][0],input=one('unchanged_grid_spectrum_and_closed_parent_references'),geometry=one('genuine_affine_native_temporal_basis'),coefficient=one('complete_fixed_metric_native99_mass_coefficients'),preparation=one('preconditioner_only_positive_node_block'),saved_audit_sha256=WEAK_METRIC_PINS['READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json'])
 wc=next(c for c in whole['cases'] if c['sigma']==1.);qc=next(c for c in q1['cases'] if c['sigma']==1.)
 whole_sigma1=dict(wc,columns=[resolve_record(r) for r in wc['columns']],input=whole['checkpoints'][0],geometry=whole['checkpoints'][1])
 q1_sigma1=dict(qc,columns=[resolve_record(r) for r in qc['columns']],input=q1['checkpoints'][0])
 fixed=whole_sigma1['input']['metadata']['fixed'];cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text())
 assert fixed['eps']==cp['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 assert whole_sigma1['input']['metadata']['owned_EPS5_background']==q1_sigma1['input']['metadata']['owned_EPS5_background']==weak['input']['metadata']['owned_background']==cp['background']
 assert q1_sigma1['input']['metadata']['fixed']==weak['input']['metadata']['fixed']==fixed
 def schema(rec,n,shape,dtype='float64'):assert rec['metadata']['schema'][n]==dict(shape=shape,dtype=dtype,finite=True),n
 for n,shape in dict(r_kpc=[87],z_kpc=[45],xi=[32],weights=[32]).items():schema(weak['input'],n,shape)
 for n,shape in dict(geometry_R=[4,3784],geometry_dv=[4,3784],geometry_hats=[4,4,3,86,44]).items():schema(weak['geometry'],n,shape)
 for n in ('geometry_cell_i','geometry_cell_j'):schema(weak['geometry'],n,[3784],'int64')
 schema(weak['geometry'],'native_independent_mask',[3,87,45],'bool')
 for n,shape in dict(input_g=[15136,4,4],input_hi=[15136,4,4],input_U=[15136,4],input_z=[32,15136,4],mixing_L=[32,15136,3,3],modal_D=[32,15136,3,3],Maxwell_M0=[15136,3,3],operation_eL=[32,15136,3,3],operation_eD=[32,15136,3,3],operation_eM0=[15136,3,3],authoritative_point_velocity=[33,15136,3],authoritative_point_native_density=[33,15136,3],actual_owned_point_native_density=[33,15136,3],implicit_fixed_time_baseline=[33,15136,3],saved_affine_momentum_gap=[33,15136,3]).items():schema(weak['coefficient'],n,shape)
 for n,shape in dict(preconditioner_D=[32,3915,3,3],preconditioner_B=[32,3915,3,3],preconditioner_Maxwell=[3915,3,3],preconditioner_basis_scale=[3915,3],kinetic_congruence_scale=[33,3,87,45]).items():schema(weak['preparation'],n,shape)
 assert len(whole_sigma1['columns'])==len(q1_sigma1['columns'])==4
 for iq,(wr,qr) in enumerate(zip(whole_sigma1['columns'],q1_sigma1['columns'])):
  wm,qm=wr['metadata'],qr['metadata'];assert wm['column']==qm['column']==iq and wm['sigma']==qm['sigma']==1. and wm['points']==qm['points']==3784
  assert qm['whole_parent_file']==wr['file'] and qm['whole_parent_sha256']==wr['sha256']
  assert weak['input']['metadata']['whole_columns'][iq]==dict(file=wr['file'],sha256=wr['sha256']) and weak['input']['metadata']['owned_columns'][iq]==dict(file=qr['file'],sha256=qr['sha256'])
  for n,shape in dict(Ga=[3784,4,4,4],g=[3784,4,4],hi=[3784,4,4],U=[3784,4],z=[32,3784,4],metric_total_canonical_density=[3784,6],native_canonical_density=[3784,99],R=[3784],Z=[3784],reference_volume=[3784]).items():schema(wr,n,shape)
  for n in ('cell_i','cell_j'):schema(wr,n,[3784],'int64')
  selected=(1972,1972,1938,1938)[iq]
  schema(wr,'compact_reused_whole_indices',[selected],'int64');schema(wr,'new_whole_indices',[3784-selected],'int64')
  for n,shape in dict(up=[3784,3],sqrt_h=[3784],K=[3784,3,3],Ktrace=[3784],Uh=[3784,6,4],zh=[32,3784,6],embed=[3784,6,4,4],h=[3784,3,3],N=[3784],ih=[3784,3,3],beta=[3784,3],u=[3784,3],gamma=[3784],JU=[3784,4,3],JzU=[32,3784,3],Jzz=[3784,3],dens=[3784],old_velocity=[3784,99]).items():schema(qr,'owned_chart_'+n,shape)
  for n,shape in dict(owned_metric_native_p=[3784,6],owned_EH_p=[3784,3,3],owned_metric_total_p=[3784,3,3],owned_native_canonical_density=[3784,99],new_native_p=[3784-selected,99],new_owned_hdot_tensor=[3784-selected,3,3]).items():schema(qr,n,shape)
  schema(qr,f'copied_q{iq}_native_p',[selected,99]);schema(qr,f'copied_q{iq}_owned_hdot_tensor',[selected,3,3])
 return pins,weak,whole_sigma1,q1_sigma1,fixed,cp

def read_weak_metric_basis(weak):
 return read_pair(weak['geometry'],('geometry_R','geometry_dv','geometry_hats','geometry_cell_i','geometry_cell_j','native_independent_mask','r_kpc','z_kpc'))

def read_weak_metric_coefficients(weak):
 return read_pair(weak['coefficient'],('input_g','input_hi','input_U','input_z','mixing_L','modal_D','Maxwell_M0','operation_eL','operation_eD','operation_eM0','authoritative_point_velocity','authoritative_point_native_density','actual_owned_point_native_density','implicit_fixed_time_baseline','saved_affine_momentum_gap'))

def read_weak_metric_owned_column(rec):
 iq=rec['metadata']['column'];assert iq in (0,1,2,3)
 names=tuple('owned_chart_'+k for k in ('up','sqrt_h','K','Ktrace','Uh','zh','embed','h','N','ih','beta','u','gamma','JU','JzU','Jzz','dens','old_velocity'))+('owned_metric_native_p','owned_EH_p','owned_metric_total_p','owned_native_canonical_density',f'copied_q{iq}_native_p','new_native_p',f'copied_q{iq}_owned_hdot_tensor','new_owned_hdot_tensor')
 return read_pair(rec,names)

def connection_momentum(s,Pi=None,Fup=None):
 Pi=s['Pi'] if Pi is None else Pi;Fup=s['Fup'] if Fup is None else Fup
 Z=s['Z'];U=s['U'];z=s['z'];hi=s['hi']
 sym=(Pi+np.swapaxes(Pi,2,3))/2
 Klo=np.einsum('pl,pa,pb->plab',Z,U,U)-np.einsum('jpab,jpl->plab',sym,z)
 Kup=np.einsum('plm,pmab->plab',hi,Klo)
 D=(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)-Kup)/2
 mx=-ALPHA*(Fup[:,:,:,None]*U[:,None,None,:]+Fup[:,:,None,:]*U[:,None,:,None])/2
 return D+mx,D,mx

def reduced_momenta(s,c,PiU=None,Pi=None,Ctime=None):
 PiU=s['PiU'] if PiU is None else PiU;Pi=s['Pi'] if Pi is None else Pi
 if Ctime is None:Ctime=connection_momentum(s)[0][:,0]
 pu=np.einsum('pa,pai->pi',PiU[:,0],c['JU'])+np.einsum('jp,jpi->pi',Pi[:,:,0,0],c['JzU'])
 pz=Pi[:,:,0,1:]+Pi[:,:,0,0,None]*c['Jzz'][None,:,:]
 py=c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)
 pmetric=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',Ctime,c['embed'])+np.einsum('pa,pka->pk',PiU[:,0],c['Uh'])+np.einsum('jp,jpk->pk',Pi[:,:,0,0],c['zh']))
 return py,pmetric

def spatial_euler_admission():
 pins,weak,whole,q1,fixed,cp=weak_metric_admission()
 for n,h in PINS.items():
  p=str(path(n).resolve());assert p not in pins or pins[p]==h;pins[p]=h;assert sha(path(n))==h,n
 stem='CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001';result=json.loads(path(stem+'_RESULT.json').read_text());rc=json.loads(path(stem+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc['closed'] and rc['owner']==result['owner'] and rc['owner']['owner']=='root' and rc['owner']['pid']==30671
 assert rc['result_sha256']==PINS[stem+'_RESULT.json'] and result['status']=='CONDITIONAL_WEAK_METRIC_TEMPORAL_CMC_ARITHMETIC_PASS'
 assert rc['owner']['source_sha256']==PINS['cross_u_weak_nodal_metric_temporal_cmc_v001.py'] and len(result['controls'])==49 and all(x['passed'] for x in result['controls']) and len(result['checkpoints'])==22
 assert all(v is False for v in result['qualification'].values())
 for group in ('input_sha256','output_sha256'):
  for n,h in rc[group].items():
   p=str(path(n).resolve());assert p not in pins or pins[p]==h;pins[p]=h
 for rec in result['checkpoints']:
  assert rc['output_sha256'][rec['file']]==rec['sha256'] and rc['output_sha256'][rec['commit_file']]==rec['commit_sha256']
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')} and rec['metadata']['owner']==rc['owner']
 for n,h in pins.items():assert sha(path(n))==h,n
 audit=json.loads(path('READONLY_CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_SAVED_AUDIT.json').read_text())
 assert audit['status']=='SAVED_PACKET_AUDIT_PASS' and audit['control_count']==49 and audit['terminal']['owner_pid']==30671
 for key,n in (('source_sha256','cross_u_weak_nodal_metric_temporal_cmc_v001.py'),('result_sha256',stem+'_RESULT.json'),('receipt_sha256',stem+'_RECEIPT.json')):assert audit['terminal'][key]==PINS[n]
 metcols=[r for r in result['checkpoints'] if r['metadata']['kind']=='six_new_metric_time_columns_and_affine_CMC_operands'];assert len(metcols)==4
 solution=resolve_record(weak['case']['solution']);ordinary=resolve_record(q1['checkpoint'])
 def schema(rec,n,shape,dtype='float64'):assert rec['metadata']['schema'][n]==dict(shape=shape,dtype=dtype,finite=True),n
 for n,shape in dict(recovered_nodal_native_velocity=[33,3,87,45],recovered_qpoint_native_velocity=[33,15136,3],recovered_qpoint_native_velocity_R=[33,15136,3],recovered_qpoint_native_velocity_Z=[33,15136,3],recovered_point_momentum_density=[33,15136,3]).items():schema(solution,n,shape)
 for n,shape in dict(source_R=[4832],source_Z=[4832],source_g=[4832,4,4],source_mass_weight=[4832],source_specific_covariant_p=[4832,3],source_right_weight=[4832]).items():schema(ordinary,n,shape)
 schema(ordinary,'source_indices',[4832],'int64')
 for iq,(wr,qr,mr) in enumerate(zip(whole['columns'],q1['columns'],metcols)):
  assert mr['metadata']['column']==iq and mr['metadata']['sigma']==SIGMA and mr['metadata']['whole_parent_file']==wr['file'] and mr['metadata']['owned_parent_file']==qr['file']
  for n,shape in dict(du=[3784,4,4],dz=[32,3784,4,4],phi=[3784,4],phase_Pstar=[3784],phase_P_X=[3784],phase_P_XX=[3784],phase_X=[3784],phase_canonical_density=[3784]).items():schema(wr,n,shape)
  for n,shape in dict(owned_du_increment=[3784,4,4],owned_dz_increment=[32,3784,4,4],owned_connection_increment=[3784,4,4,4]).items():schema(qr,n,shape)
  for n,shape in dict(B=[3784,99,6],B_envelope=[3784,99,6],current_metric_pistar=[3784,6],current_metric_time_jet=[3784,6],current_metric_time_tensor=[3784,3,3],current_native_pstar=[3784,99],old_native_target=[3784,99]).items():schema(mr,n,shape)
 return pins,weak,whole,q1,metcols,solution,ordinary,fixed,cp

def load_seed_column(iq,wr,qr,mr,bc,sol,xi,w,omega):
 old=read_pair(wr,('Ga','du','dz','phi','R','Z','reference_volume','phase_Pstar','phase_P_X','phase_P_XX','phase_X','phase_canonical_density'))
 own=read_weak_metric_owned_column(qr);own.update(read_pair(qr,('owned_du_increment','owned_dz_increment','owned_connection_increment')))
 met=read_pair(mr,('B','B_envelope','current_metric_pistar','current_metric_time_jet','current_metric_time_tensor','current_native_pstar','old_native_target'))
 sl=slice(iq*3784,(iq+1)*3784);c={k.removeprefix('owned_chart_'):v for k,v in own.items() if k.startswith('owned_chart_')}
 y=sol['recovered_qpoint_native_velocity'][:,sl].transpose(1,0,2).reshape(3784,99);ystar=c['old_velocity'];delta=y-ystar
 capture('seed_nodal_native_rate',y);capture('seed_old_L2_native_rate',ystar);capture('seed_native_rate_delta',delta)
 du=old['du']+own['owned_du_increment'];capture('seed_owned_du',du)
 dz=old['dz']+own['owned_dz_increment'];capture('seed_owned_dz',dz)
 Ga=old['Ga']+own['owned_connection_increment'];capture('seed_owned_connection',Ga)
 du[:,0]+=np.einsum('pri,pi->pr',c['JU'],delta[:,:3]);capture('seed_current_du',du)
 zm=delta[:,3:].reshape(3784,32,3).transpose(1,0,2);dz[:,:,0,1:]+=zm
 dz[:,:,0,0]+=np.einsum('jpi,pi->jp',c['JzU'],delta[:,:3])+np.einsum('pi,jpi->jp',c['Jzz'],zm);capture('seed_current_dz',dz)
 for n,key in (('R','R'),('reference_volume','dv')):assert np.array_equal(old[n],GEO[key][iq])
 s=features(bc['input_g'][sl],bc['input_hi'][sl],Ga,bc['input_U'][sl],du,bc['input_z'][:,sl],dz,old['phi'],omega,xi,w)
 s['R']=old['R'];s['Z_coordinate']=old['Z'];cj=chart_spacetime_jets(s,c)
 for k,a in dict(seed_covariant_native_rate_R=sol['recovered_qpoint_native_velocity_R'][:,sl],seed_covariant_native_rate_Z=sol['recovered_qpoint_native_velocity_Z'][:,sl],seed_metric_L2_rate=met['current_metric_time_tensor'],seed_owned_coordinate_Ndot=cj['dN'][:,0],seed_owned_coordinate_betadot=cj['dbeta'][:,0]).items():capture(k,a)
 return s,c,cj,old,met,sol['recovered_point_momentum_density'][:,sl].transpose(1,0,2).reshape(3784,99)

def configuration_direction_controls(s,c,cj,native,metric,R,P,PX,X):
 p=len(R);value=np.broadcast_to((np.arange(99)%7-3)[None]/17.,(p,99)).copy();dv=np.zeros((p,4,99));dv[:,1]=(np.arange(99)%5-2)[None]/19.;dv[:,2]=(np.arange(99)%3-1)[None]/23.
 eta,de,ze,dz=native_configuration_lift(s,c,cj,value,dv);dt,env,*_=variation(s,eta,de,ze,dz)
 assembled=np.sum(native['coefficient'][:,:,0]*value+native['coefficient'][:,:,1]*dv[:,1]+native['coefficient'][:,:,2]*dv[:,2],axis=1)
 ea=np.sum(native['envelope'][:,:,0]*abs(value)+native['envelope'][:,:,1]*abs(dv[:,1])+native['envelope'][:,:,2]*abs(dv[:,2]),axis=1)
 check('native99_full_configuration_first_variation',assembled,c['dens']*dt.sum(axis=1),ea+c['dens']*env.sum(axis=1))
 vv=(np.arange(6)-2)/13.;vr=(np.arange(6)%3-1)/11.;vz=(np.arange(6)%2-.5)/7.;f=np.full(p,1.);zero=np.zeros((p,4));q=np.zeros_like(s['g']);dq=np.zeros((p,4,4,4));et=np.zeros_like(s['U']);det=np.zeros_like(s['du']);zt=np.zeros_like(s['z']);dzt=np.zeros_like(s['dz']);H=np.zeros((p,3,3));dH=np.zeros((p,4,3,3));e=metric_basis()
 for a in range(6):
  df=zero.copy();df[:,1]=vr[a];df[:,2]=vz[a];qq,dqq,ee,dee,zz,dzz=metric_configuration_lift(s,c,cj,a,np.full(p,vv[a]),df)
  q+=qq;dq+=dqq;et+=ee;det+=dee;zt+=zz;dzt+=dzz;H+=e[a]*vv[a];dH[:,1]+=e[a]*vr[a];dH[:,2]+=e[a]*vz[a]
 mt,me,_=metric_native(s,q,dq,et,det);ztv,zev,*_=variation(s,np.zeros_like(et),np.zeros_like(det),zt,dzt);pt,pe=phase_metric_direction(s,q,P,PX,X);eh=EH_spatial_metric_direction(s,c,cj,H,dH,R)
 direct=c['dens']*((mt+ztv).sum(axis=1)+pt.sum(axis=1))+R*eh['value'];ede=c['dens']*((me+zev).sum(axis=1)+pe.sum(axis=1))+R*eh['envelope'].sum(axis=1)
 calc=np.sum(metric['coefficient'][:,:,0]*vv+metric['coefficient'][:,:,1]*vr+metric['coefficient'][:,:,2]*vz,axis=1);eca=np.sum(metric['envelope'][:,:,0]*abs(vv)+metric['envelope'][:,:,1]*abs(vr)+metric['envelope'][:,:,2]*abs(vz),axis=1)
 check('six_metric_full_configuration_first_variation',calc,direct,eca+ede)

def current_seed_witnesses(s,c,cj,native,old,met,expected):
 check('new_seed_native_canonical_momentum',native['momentum'],expected,native['momentum_envelope']+abs(expected))
 py,pm=reduced_momenta(s,c);EH=c['sqrt_h'][:,None,None]*(np.einsum('pik,pkl,plj->pij',c['ih'],c['K'],c['ih'])-c['Ktrace'][:,None,None]*c['ih'])/(2*C)
 total=pm+tensor_momentum_coordinates(EH);delta=AVAILABLE['seed_native_rate_delta'];prediction=met['current_metric_pistar']+np.einsum('pia,pi->pa',met['B'],delta)
 ep=abs(met['current_metric_pistar'])+np.einsum('pia,pi->pa',met['B_envelope'],abs(delta))+abs(pm)+abs(tensor_momentum_coordinates(EH))
 check('new_seed_full_metric_canonical_momentum',total,prediction,ep)
 vphi=-raise_cov(s['hi'],s['phi'])/old['phase_X'][:,None];J=old['phase_P_X'][:,None]*vphi-raise_cov(s['hi'],s['r']);phasep=c['dens']*J[:,0]
 check('new_seed_phase_current_density',phasep,old['phase_canonical_density'],c['dens']*(abs(old['phase_P_X']*vphi[:,0])+abs(raise_cov(s['hi'],s['r'])[:,0]))+abs(old['phase_canonical_density']))
 dg=cj['dg'];unit=np.einsum('pab,pa,pb->p',s['g'],s['U'],s['U'])+1
 ujet=np.einsum('pamn,pm,pn->pa',dg,s['U'],s['U'])+2*np.einsum('pab,pb->pa',lower_last(s['g'],s['du']),s['U'])
 # Direct partial derivative of U.z (no metric in the contraction).
 z0=np.einsum('pa,jpa->jp',s['U'],s['z']);zjet=np.einsum('pam,jpm->jpa',s['du'],s['z'])+np.einsum('pm,jpam->jpa',s['U'],s['dz'])
 eu=np.einsum('pab,pa,pb->p',abs(s['g']),abs(s['U']),abs(s['U']))+1
 eud=np.einsum('pamn,pm,pn->pa',abs(dg),abs(s['U']),abs(s['U']))+2*np.einsum('pab,pb->pa',np.einsum('pac,pbc->pab',abs(s['du']),abs(s['g'])),abs(s['U']))
 ez=np.einsum('pa,jpa->jp',abs(s['U']),abs(s['z']));ezd=np.einsum('pam,jpm->jpa',abs(s['du']),abs(s['z']))+np.einsum('pm,jpam->jpa',abs(s['U']),abs(s['dz']))
 check('new_seed_unit_transverse_complete_first_jets',np.r_[unit.ravel(),ujet.ravel(),z0.ravel(),zjet.ravel()],np.zeros(unit.size+ujet.size+z0.size+zjet.size),np.r_[eu.ravel(),eud.ravel(),ez.ravel(),ezd.ravel()])
 data=dict(new_native_momentum=native['momentum'],new_metric_native_momentum=pm,new_metric_EH_momentum=EH,new_metric_total_momentum=total,new_phase_current=J,new_phase_canonical_density=phasep,old_native_L2_point_momentum=met['current_native_pstar'],old_native_target=met['old_native_target'],old_metric_L2_momentum=met['current_metric_pistar'],new_native_minus_old_target=native['momentum']-met['old_native_target'])
 for k,a in data.items():capture(k,a)
 return data

# In-progress final data flow follows; scientific execution remains closed.
if __name__=='__main__':raise RuntimeError('Authoring in progress')
