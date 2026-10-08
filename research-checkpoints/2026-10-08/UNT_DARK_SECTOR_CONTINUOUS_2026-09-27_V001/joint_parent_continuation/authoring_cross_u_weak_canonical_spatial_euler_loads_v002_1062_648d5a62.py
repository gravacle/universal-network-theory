"""Guarded new canonical spatial Euler-load coefficients; authoring in progress."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback,ast,zipfile,struct
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V002'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='ae50d65afc3790d2a5fd41dc13d6352fe5b53181f7cb8fffc88690c4937344d0'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
B=None;TOL=2e-11;EXPECTED_CONTROLS=36
np=None;GEO=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(spatial_Euler_loads_qualified=False,CMC_qualified=False,force_convective_qualified=False,physical_metric_qualified=False,history_qualified=False,exterior_qualified=False,physical_inertia_qualified=False,source_qualified=False,galaxy_velocity_qualified=False)
PINS={'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_ASSEMBLY_V001.md': '5e025effae0a5029df1cbe1935137263e5b27c442cca4fe3ced46a992566b84d', 'CROSS_U_FULL_CANONICAL_CMC_PRESERVATION_EXTENSION_V001.md': '60a222d80500b01771092919ede0d1374969ee769471964aec911929aad9e424', 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_AND_CMC_EXTENSION_V001.md': '78491aa4158dec6152a19136d5b3265cc63cdc965ebf4002d8df371074b46806', 'cross_u_saved_full_native_adm_legendre_v002.py': '9185f2dcd981d7599023858dd8c533b13a510c150ad994b5ea3f569b947d9de0', 'cross_u_whole_slice_q1_adm_residual_v001.py': 'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a', 'cross_u_weak_nodal_metric_temporal_cmc_v001.py': 'e11bb7ec123971998fbdd64d1e2171627aae9202804d1c625202f412b5f85b6c', 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001.md': '60de28cc558734f648fc3845ebf18ab47b10f0cf9d06a89142e59268951baf7a', 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RESULT.json': '2210b4993989d6cb432d9981cc8819f1c21c394ded9d349f6d34b009adb92528', 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_RECEIPT.json': 'f74d4d67ba87838b4902dc53eebd38812c9b723870ef57528144a7b3a22151cf', 'READONLY_CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_CMC_V001_SAVED_AUDIT.json': 'a3066b6cf48187e3fd577672aeeb89e03aa9174a6fb520f6bbdf018132cf2781', 'author_fragment_weak_canonical_euler_fixtures_v001.txt': 'cb7b66bc588283b084f448ff6db3b2aec93484ad719450deb04c012232f21353', 'authoring_cross_u_weak_canonical_spatial_euler_loads_v001_7_da1cc7a4.py': 'da1cc7a43f1ec85e1c2e289efde7b142975a782a8ca48a862693f486d2b8c7d5', 'authoring_cross_u_weak_canonical_spatial_euler_loads_v001_703_d0903ccc.py': 'd0903ccca08525cf03d2b51d87f1259e9c8a932e26cca6c9aa38529640c44eb9', 'authoring_cross_u_weak_canonical_spatial_euler_loads_v001_931_b05657c5.py': 'b05657c57df241228a00555b06e2321a40c1859ec2706ba0ed40a73acaf061ee', 'authoring_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_3_40963921.md': '40963921d70c549f7510a39e8e9668d852dc340d14657731c86839297dd2f839', 'authoring_cross_u_weak_canonical_spatial_euler_loads_v001_934_6868209e.py': '6868209e65b014db9e30f2779283baeac1c3a3f57a91e158bc1db8ea04f258b0', 'author_fragment_spatial_euler_v002_momentum_envelopes.txt': 'c333059f668027a34b4f17d566aca5d6202e7b9ab290956513288efbd34268d3', 'author_fragment_weak_spatial_euler_v002_failed_admission.txt': '1ffce4bb3af971ab9271e9c2f245291ca6431ec4696624d5d27e27fbfc65dcc9', 'author_static_weak_canonical_spatial_euler_loads_v001_83236dab.json': 'ec658f7e6c569b3cfc04ae4a7c2e4d11e20bebf0d9c37f258664a3e685e9646b', 'authoring_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V002_4_9dfeaaef.md': '9dfeaaef1243c7669e69035de8521c2af9cacc71dc3340c2d8d1a49653ff946b'}

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
    vals=np.einsum('pgcj,jpc->pgc',qco.reshape(3784,33,3,3),fac)*wq[:,None,None]
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

FAILED_FORCE_RAW_SCHEMA={'chart_first_dJU': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 3]}, 'chart_first_dJzU': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 3]}, 'chart_first_dJzz': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 3]}, 'chart_first_dN': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'chart_first_dUh': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 6, 4]}, 'chart_first_dbeta': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 3]}, 'chart_first_dembed': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 6, 4, 4]}, 'chart_first_dg': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 4]}, 'chart_first_dgamma': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'chart_first_dh': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 3, 3]}, 'chart_first_dhi': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 4]}, 'chart_first_dih': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 3, 3]}, 'chart_first_du_cov': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 3]}, 'chart_first_dup': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 3]}, 'chart_first_dzh': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 6]}, 'control_007_new_seed_native_canonical_momentum_actual': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'control_007_new_seed_native_canonical_momentum_envelope': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'control_007_new_seed_native_canonical_momentum_expected': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'current_A': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'current_D': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}, 'current_F': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_Fup': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_Ga': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 4]}, 'current_P': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_Pi': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}, 'current_PiU': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_U': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'current_V': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4]}, 'current_Z': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'current_a': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'current_du': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_dz': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}, 'current_f': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784]}, 'current_g': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_hi': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_mu': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784]}, 'current_nu': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'current_nz': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}, 'current_omega': {'dtype': 'float64', 'finite': True, 'shape': [32]}, 'current_phi': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'current_q': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4]}, 'current_r': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'current_uc': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'current_w': {'dtype': 'float64', 'finite': True, 'shape': [32]}, 'current_xi': {'dtype': 'float64', 'finite': True, 'shape': [32]}, 'current_z': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4]}, 'current_z2': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784]}, 'loaded_B': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99, 6]}, 'loaded_B_envelope': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99, 6]}, 'loaded_Ga': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 4]}, 'loaded_R': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_Z': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_copied_q0_native_p': {'dtype': 'float64', 'finite': True, 'shape': [1972, 99]}, 'loaded_copied_q0_owned_hdot_tensor': {'dtype': 'float64', 'finite': True, 'shape': [1972, 3, 3]}, 'loaded_current_metric_pistar': {'dtype': 'float64', 'finite': True, 'shape': [3784, 6]}, 'loaded_current_metric_time_jet': {'dtype': 'float64', 'finite': True, 'shape': [3784, 6]}, 'loaded_current_metric_time_tensor': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3, 3]}, 'loaded_current_native_pstar': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'loaded_du': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'loaded_dz': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}, 'loaded_new_native_p': {'dtype': 'float64', 'finite': True, 'shape': [1812, 99]}, 'loaded_new_owned_hdot_tensor': {'dtype': 'float64', 'finite': True, 'shape': [1812, 3, 3]}, 'loaded_old_native_target': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'loaded_owned_EH_p': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3, 3]}, 'loaded_owned_chart_JU': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 3]}, 'loaded_owned_chart_JzU': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 3]}, 'loaded_owned_chart_Jzz': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3]}, 'loaded_owned_chart_K': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3, 3]}, 'loaded_owned_chart_Ktrace': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_owned_chart_N': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_owned_chart_Uh': {'dtype': 'float64', 'finite': True, 'shape': [3784, 6, 4]}, 'loaded_owned_chart_beta': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3]}, 'loaded_owned_chart_dens': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_owned_chart_embed': {'dtype': 'float64', 'finite': True, 'shape': [3784, 6, 4, 4]}, 'loaded_owned_chart_gamma': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_owned_chart_h': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3, 3]}, 'loaded_owned_chart_ih': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3, 3]}, 'loaded_owned_chart_old_velocity': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'loaded_owned_chart_sqrt_h': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_owned_chart_u': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3]}, 'loaded_owned_chart_up': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3]}, 'loaded_owned_chart_zh': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 6]}, 'loaded_owned_connection_increment': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 4]}, 'loaded_owned_du_increment': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'loaded_owned_dz_increment': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}, 'loaded_owned_metric_native_p': {'dtype': 'float64', 'finite': True, 'shape': [3784, 6]}, 'loaded_owned_metric_total_p': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3, 3]}, 'loaded_owned_native_canonical_density': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'loaded_phase_P_X': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_phase_P_XX': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_phase_Pstar': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_phase_X': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_phase_canonical_density': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'loaded_phi': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4]}, 'loaded_reference_volume': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'native_config_A_can': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'native_config_A_z_raw': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4]}, 'native_config_P_can': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 99]}, 'native_config_coefficient': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99, 3]}, 'native_config_envelope': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99, 3]}, 'native_config_momentum': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'native_config_momentum_envelope': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'native_config_nJU': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 3]}, 'native_config_nJzu': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4, 3]}, 'native_config_nJzz': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 3]}, 'seed_covariant_native_rate_R': {'dtype': 'float64', 'finite': True, 'shape': [33, 3784, 3]}, 'seed_covariant_native_rate_Z': {'dtype': 'float64', 'finite': True, 'shape': [33, 3784, 3]}, 'seed_current_du': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'seed_current_dz': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}, 'seed_metric_L2_rate': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3, 3]}, 'seed_native_rate_delta': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'seed_nodal_native_rate': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'seed_old_L2_native_rate': {'dtype': 'float64', 'finite': True, 'shape': [3784, 99]}, 'seed_owned_connection': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4, 4]}, 'seed_owned_coordinate_Ndot': {'dtype': 'float64', 'finite': True, 'shape': [3784]}, 'seed_owned_coordinate_betadot': {'dtype': 'float64', 'finite': True, 'shape': [3784, 3]}, 'seed_owned_du': {'dtype': 'float64', 'finite': True, 'shape': [3784, 4, 4]}, 'seed_owned_dz': {'dtype': 'float64', 'finite': True, 'shape': [32, 3784, 4, 4]}}

# Private definitions-only failed force admission/reuse. No functions evaluated.
FAILED_FORCE_STEM='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001'
FAILED_FORCE_PINS={'cross_u_weak_canonical_spatial_euler_loads_v001.py': '8aba0c892ec0a029e09d5380b18d489f9f9838aac84d6a95628dd1e41508e1c2', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001.md': 'bf321450bae902a94099e28e27de5c1e197b0c4d11551ecefce1826050ed14de', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_OWNER_START.json': '20dc54817d93c8c1c547fbfa8e220c1700beb1c70487f1d4015972fa0691a5bf', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_MANIFEST.json': 'e0ddc3e3a4788c729e4820783efa197266d22ff942ab4b05e449d68fbb972d71', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_ERROR.json': '8abfa418e010ebd5728845461e3391a73064925015537bdaa88643202e8d0c83', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_RECEIPT.json': 'fd79952cefba089c86568c8641e88df1a9df50a8ef3c1935a5e6a3490b300b85', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00000_INPUT.npz': 'bc369cdd912d35304808c98d00364f280fc7e4d33084acf5d82acf189998af86', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00000_INPUT.npz.COMMIT.json': '39ca62702c755c6003eff13b776869bdf5542f91146ff13755541bef928de6bc', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00001_FIXTURE.npz': '631491cbaa32c21889ea3ec2ecf83b042cac153f75b68acaaa9878b5c20ad37c', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00001_FIXTURE.npz.COMMIT.json': '0bfc0a6bb1f681f6f3a4f5f69273b0b6b56bf3b5baa0bf7581dbad455e25e541', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00002_BASIS.npz': '5fe6b50493333d4ab2eed2799aa20181d046606b6a9a7e4622a34e4a153df40e', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00002_BASIS.npz.COMMIT.json': 'd4421cd41b177583e72e56603f96d90e5b7fc4a94c0e0fe55353121880906d63', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00003_ERROR_RAW.npz': 'd5de99e6cab90fc907e7b92ca81fae916471d339ea0e7ceb63b9956c46483133', 'CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V001_00003_ERROR_RAW.npz.COMMIT.json': '1649a82dc1ce88ac41b922b6e8e4d27685372ad6c83aa5985cfaf2a07bf0cf53'}

def force_failed_admission(pins):
 pins=dict(pins)
 def add(n,h):
  k=str(path(n).resolve());assert k not in pins or pins[k]==h;pins[k]=h;assert sha(path(n))==h,n
 for n,h in FAILED_FORCE_PINS.items():add(n,h)
 er=json.loads(path(FAILED_FORCE_STEM+'_ERROR.json').read_text());rc=json.loads(path(FAILED_FORCE_STEM+'_RECEIPT.json').read_text())
 owner=rc['owner'];assert owner['owner']=='root' and owner['pid']==34079 and owner['source_sha256']==FAILED_FORCE_PINS['cross_u_weak_canonical_spatial_euler_loads_v001.py']
 assert rc['status']=='CLOSED_ERROR' and rc['closed'] and er['status']=='FAILED' and er['owner']==owner and er['prior_receipt_sha256'] is None
 assert rc['error_sha256']==FAILED_FORCE_PINS[FAILED_FORCE_STEM+'_ERROR.json'] and er['qualification']==rc['qualification'] and all(x is False for x in rc['qualification'].values())
 assert json.loads(path(FAILED_FORCE_STEM+'_OWNER_START.json').read_text())==owner
 manifest=json.loads(path(FAILED_FORCE_STEM+'_MANIFEST.json').read_text());assert manifest['owner']==owner and manifest['input_sha256']==rc['input_sha256'] and manifest['configuration']['controls']==36 and manifest['configuration']['pairs']==8
 for group in ('input_sha256','output_sha256'):
  for n,h in rc[group].items():add(n,h)
 for n,h in er['preserved_outputs'].items():add(n,h)
 controls=er['controls'];assert len(controls)==8 and [x['ordinal'] for x in controls]==list(range(8)) and all(x['passed'] for x in controls[:7]) and controls[7]['passed'] is False
 assert controls[7]['name']=='new_seed_native_canonical_momentum' and controls[7]['tolerance']==2e-11 and controls[7]['error']>controls[7]['tolerance']
 assert all(x['tolerance']==2e-11 for x in controls) and er['context']['column']==0 and er['context']['ordinal']==7
 records=er['checkpoints'];assert len(records)==4 and er['unqualified_npz']==[] and not path(FAILED_FORCE_STEM+'_RESULT.json').exists()
 assert {p.name for p in BASE.glob(FAILED_FORCE_STEM+'_*.npz')}=={r['file'] for r in records} and {p.name for p in BASE.glob(FAILED_FORCE_STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in records}
 kinds=('unchanged_sigma1_configuration_spectrum_and_owned_seed_references','seven_independent_new_canonical_configuration_force_contacts','unchanged_genuine_native_and_regular_six_metric_configuration_basis','unqualified_available_canonical_spatial_Euler_operands')
 for r,kind,count in zip(records,kinds,(4,136,8,118)):
  assert r['metadata']['kind']==kind and r['metadata']['owner']==owner and len(r['metadata']['schema'])==count and all(v['finite'] for v in r['metadata']['schema'].values())
  assert rc['output_sha256'][r['file']]==r['sha256'] and rc['output_sha256'][r['commit_file']]==r['commit_sha256']
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
 assert records[1]['metadata']['controls']==controls[:7] and records[1]['metadata']['physical_seed'] is False and records[3]['metadata']['failed'] is True
 raw=records[3]['metadata']['schema'];assert raw==FAILED_FORCE_RAW_SCHEMA
 for n,shape in dict(control_007_new_seed_native_canonical_momentum_actual=[3784,99],control_007_new_seed_native_canonical_momentum_expected=[3784,99],control_007_new_seed_native_canonical_momentum_envelope=[3784,99],native_config_momentum=[3784,99],native_config_momentum_envelope=[3784,99],native_config_coefficient=[3784,99,3],native_config_envelope=[3784,99,3],seed_nodal_native_rate=[3784,99],seed_old_L2_native_rate=[3784,99],seed_native_rate_delta=[3784,99],seed_owned_du=[3784,4,4],seed_owned_dz=[32,3784,4,4],seed_owned_connection=[3784,4,4,4],seed_current_du=[3784,4,4],seed_current_dz=[32,3784,4,4]).items():assert raw[n]==dict(shape=shape,dtype='float64',finite=True),n
 assert all('current_'+k in raw for k in ('g','hi','Ga','U','uc','du','z','dz','phi','omega','xi','w','nu','nz','P','q','V','D','a','r','f','z2','Pi','mu','Z','F','Fup','PiU','A'))
 assert all('chart_first_'+k in raw for k in ('dg','dhi','dN','dbeta','dh','dih','du_cov','dup','dgamma','dJU','dJzU','dJzz','dUh','dzh','dembed'))
 for n,h in pins.items():assert sha(path(n))==h,n
 return pins,dict(error=er,receipt=rc,input=records[0],fixture=records[1],basis=records[2],raw=records[3])

def read_force_failed_raw(failed):
 return read_pair(failed['raw'],tuple(failed['raw']['metadata']['schema']))

def reuse_force_completed(failed):
 # Runtime ROOT-only loading and copying. No fixture or coefficient calculation.
 return dict(input_arrays=read_pair(failed['input'],tuple(failed['input']['metadata']['schema'])),fixture_arrays=read_pair(failed['fixture'],tuple(failed['fixture']['metadata']['schema'])),basis_arrays=read_pair(failed['basis'],tuple(failed['basis']['metadata']['schema'])),raw_arrays=read_force_failed_raw(failed),controls=[dict(x) for x in failed['error']['controls'][:7]],original_controls=[dict(x) for x in failed['error']['controls']])


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
 pins,failed=force_failed_admission(pins)
 return pins,weak,whole,q1,metcols,solution,ordinary,fixed,cp,failed

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

# Definitions only. Exact pre-cancellation readout bounds; no signed physics call.
def native_momentum_operation_envelopes(s,c,label,du=None,dz=None):
 g,hi,U,z=s['g'],s['hi'],s['U'],s['z'];w,om=s['w'],s['omega'];N,ga,be,ih=c['N'],c['gamma'],c['beta'],c['ih']
 du=s['du'] if du is None else du;dz=s['dz'] if dz is None else dz
 out={}
 def put(name,a):
  out[name]=a;RAW['momentum_operation_'+label+'_'+name]=a.copy()
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0)
  return a
 # All additions precede covariant derivative and projector cancellations.
 euc=put('U_cov',np.einsum('pab,pb->pa',abs(g),abs(U)))
 enu=put('nu',abs(du)+np.einsum('pbal,pl->pab',abs(s['Ga']),abs(U)))
 enz=put('nz',abs(dz)+np.einsum('plab,jpl->jpab',abs(s['Ga']),abs(z)))
 ep=put('P',np.eye(4)[None]+euc[:,:,None]*abs(U)[:,None,:])
 eq=put('q',np.einsum('pa,jpab->jpb',abs(U),enz))
 ev=put('V',np.einsum('pab,jpb->jpa',ep,eq))
 ed=put('D',np.einsum('pac,jpcd,pbd->jpab',ep,enz,ep))
 elower=put('nu_lower',np.einsum('pab,pcb->pca',abs(g),enu))
 ef=put('F',elower+elower.swapaxes(1,2))
 ez=put('Z',np.einsum('j,jpa->pa',abs(w),abs(z)))
 epiu=put('PiU',abs(ALPHA)*np.einsum('pac,pcb->pab',abs(hi),ef)+np.einsum('pa,pb->pab',abs(U),ez))
 epi=put('Pi',abs(w)[:,None,None,None]*(np.einsum('pa,jpb->jpab',abs(U),np.einsum('pab,jpb->jpa',abs(hi),ev))/abs(om)[:,None,None,None]**2+ELL**2*np.einsum('pac,jpcd,pdb->jpab',abs(hi),ed,abs(hi))))
 # u=g_sp U and h^-1 u are propagated before their possible exact-zero sums.
 eup=put('up',np.einsum('pij,pj->pi',abs(ih),euc[:,1:]))
 eju=np.empty_like(c['JU']);eju[:,0]=eup/abs(N*ga)[:,None]
 eju[:,1:]=abs(ih)+abs(be)[:,:,None]*eju[:,None,0,:];put('JU',eju)
 ejzu=put('JzU',np.einsum('jpa,pai->jpi',abs(z),eju)/abs(U[None,:,0,None]))
 ejzz=put('Jzz',(eup+abs(be)*abs(ga/N)[:,None])/abs(U[:,0,None]))
 eu=put('native_U',np.einsum('pa,pai->pi',epiu[:,0],eju)+np.einsum('jp,jpi->pi',epi[:,:,0,0],ejzu))
 em=put('native_modes',epi[:,:,0,1:]+epi[:,:,0,0,None]*ejzz[None])
 value=put('native_density',abs(c['dens'])[:,None]*np.concatenate((eu,em.transpose(1,0,2).reshape(len(U),96)),axis=1))
 return value,out

def saved_affine_point_momentum_envelope(s,c,bc,iq,new_rate,old_rate,old_du,old_dz):
 # The primal old pstar and recovered p were already saved; no p/field replay.
 old,operands=native_momentum_operation_envelopes(s,c,'old_pointstar',old_du,old_dz)
 sl=slice(iq*3784,(iq+1)*3784);p=len(new_rate)
 # Preserve the original subtraction's operation bound, not its rounded residue.
 v=abs(new_rate)+abs(old_rate);u=v[:,:3];zm=v[:,3:].reshape(p,32,3).transpose(1,0,2)
 M=bc['operation_eM0'][sl];L=bc['operation_eL'][:,sl];D=bc['operation_eD'][:,sl]
 mixed=zm+np.einsum('jpik,pk->jpi',L,u,optimize=True)
 modes=np.einsum('jpik,jpk->jpi',D,mixed,optimize=True)
 nativeU=np.einsum('pik,pk->pi',M,u,optimize=True)+np.einsum('jpki,jpk->pi',L,modes,optimize=True)
 action=np.concatenate((nativeU,modes.transpose(1,0,2).reshape(p,96)),axis=1)
 value=old+action
 for name,a in dict(delta_velocity=v,eM0=M,eL=L,eD=D,mixed=mixed,modes=modes,native_U=nativeU,action=action,old_pointstar=old,expected_density=value).items():
  RAW['momentum_operation_saved_affine_'+name]=a.copy()
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0)
 return value


def current_seed_witnesses(s,c,cj,native,old,met,expected,bc,iq):
 original=native['momentum_envelope'].copy();RAW['original_postcancel_native_momentum_envelope']=original
 current,operations=native_momentum_operation_envelopes(s,c,'current')
 expected_envelope=saved_affine_point_momentum_envelope(s,c,bc,iq,AVAILABLE['seed_nodal_native_rate'],AVAILABLE['seed_old_L2_native_rate'],AVAILABLE['seed_owned_du'],AVAILABLE['seed_owned_dz'])
 native['momentum_envelope']=current;RAW['new_full_native_readout_envelope']=current+expected_envelope
 check('new_seed_native_canonical_momentum',native['momentum'],expected,current+expected_envelope)
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

def adm_chart(s):
 # Independent configuration is U_i and every z_ji, all spatial covectors.
 g,hi,U,z=s['g'],s['hi'],s['U'],s['z'];p=len(U)
 h=g[:,1:,1:];ih=np.linalg.inv(h);N=1/np.sqrt(-hi[:,0,0]);beta=N[:,None]**2*hi[:,0,1:]
 assert np.all(N>0) and np.all(np.linalg.eigvalsh(h)>0)
 uc=lower(g,U);u=uc[:,1:];up=np.einsum('pij,pj->pi',ih,u);gamma=np.sqrt(1+np.sum(u*up,axis=1))
 rebuilt=np.column_stack((gamma/N,up-beta*gamma[:,None]/N[:,None]))
 zt=-np.einsum('pi,jpi->jp',rebuilt[:,1:],z[:,:,1:])/rebuilt[None,:,0]
 JU=np.empty((p,4,3));JU[:,0]=up/(N*gamma)[:,None];JU[:,1:]=ih-beta[:,:,None]*JU[:,None,0,:]
 JzU=-np.einsum('jpa,pai->jpi',z,JU)/U[None,:,0,None]
 Jzz=-U[:,1:]/U[:,0,None]
 e=metric_basis();embed=np.zeros((p,6,4,4));embed[:,:,1:,1:]=e[None,:,:,:]
 embed[:,:,0,1:]=np.einsum('kij,pj->pki',e,beta);embed[:,:,1:,0]=embed[:,:,0,1:]
 embed[:,:,0,0]=np.einsum('pi,kij,pj->pk',beta,e,beta)
 dgamma=-np.einsum('pi,kij,pj->pk',up,e,up)/(2*gamma[:,None])
 Uh=np.empty((p,6,4));Uh[:,:,0]=dgamma/N[:,None]
 Uh[:,:,1:]=-np.einsum('pij,kjl,pl->pki',ih,e,up)-beta[:,None,:]*Uh[:,:,0,None]
 zh=-np.einsum('jpa,pka->jpk',z,Uh)/U[None,:,0,None]
 dens=np.sqrt(-np.linalg.det(g));sqrt_h=np.sqrt(np.linalg.det(h))
 dg=metric_partial(s);udot=np.einsum('pia,pa->pi',dg[:,0,1:,:],U)+lower_last(g,s['du'])[:,0,1:]
 zdot=s['dz'][:,:,0,1:]
 old_velocity=np.concatenate((udot,zdot.transpose(1,0,2).reshape(p,96)),axis=1)
 # Kplus = projected nabla n = N Gamma^0_ij; this is the declared stationary trial K.
 K=N[:,None,None]*s['Ga'][:,0,1:,1:];Kup=np.einsum('pik,pkl,plj->pij',ih,K,ih);Kt=np.einsum('pij,pij->p',ih,K)
 pEH=sqrt_h[:,None,None]*(Kup-Kt[:,None,None]*ih)/(2*C)
 GEH=sqrt_h[:,None,None]/(4*N[:,None,None]*C)*(np.einsum('aij,pjk,bkl,pli->pab',e,ih,e,ih)-np.einsum('pij,kij->pk',ih,e)[:,:,None]*np.einsum('pij,kij->pk',ih,e)[:,None,:])
 return dict(h=h,ih=ih,N=N,beta=beta,u=u,up=up,gamma=gamma,rebuilt_U=rebuilt,rebuilt_zt=zt,JU=JU,JzU=JzU,Jzz=Jzz,embed=embed,Uh=Uh,zh=zh,dens=dens,sqrt_h=sqrt_h,old_velocity=old_velocity,K=K,Ktrace=Kt,pi_EH=pEH,EH_Hessian=GEH)

def connection_from_jet(hi,dg):
 p=len(hi);out=np.zeros((p,4,4,4))
 for a in range(4):
  for b in range(4):out[:,:,a,b]=np.einsum('plm,pm->pl',hi,dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b])/2
 return out

def euler_fixture_keep(name,value):
 RAW['euler_fixture_'+name]=np.asarray(value).copy();return value

def euler_fixture_state(g,dg,U,du,z,dz,phi,w,xi,omega):
 hi=np.linalg.inv(g);Ga=connection_from_jet(hi,dg)
 for n,v in dict(g=g,dg=dg,hi=hi,Ga=Ga,U=U,du=du,z=z,dz=dz,phi=phi,w=w,xi=xi,omega=omega).items():euler_fixture_keep(n,v)
 s=features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w)
 c=adm_chart(s);cj=chart_spacetime_jets(s,c)
 return s,c,cj

def canonical_euler_fixtures():
 start=len(CHECKS)
 # Flat Cartesian point, constant tilted covector chart, nonzero quartic mode.
 # Artificial local values only; no physical preparation or EOS is selected.
 xi=np.arange(1.,33.)/33;w=np.r_[2/9,np.full(31,7/(9*31))];om=np.ones(32)
 u=3/4;ga=5/4;X=2.;zk=(B*GC)*xi[0]**2*(2/7);kj=(B*GC)**2*xi[0]**4
 g=np.diag([-1.,1.,1.,1.])[None];dg=np.zeros((1,4,4,4));U=np.array([[ga,u,0.,0.]])
 du=np.zeros((1,4,4));z=np.zeros((32,1,4));z[0,0]=np.array([-u*zk/ga,zk,0.,0.]);dz=np.zeros((32,1,4,4));phi=np.array([[X,0.,0.,0.]])
 s,c,cj=euler_fixture_state(g,dg,U,du,z,dz,phi,w,xi,om)
 cc=canonical_native_coefficients(s,c,cj);q2=zk**2/ga**2;ff=1+q2/kj
 expected=np.zeros((1,99,3));ee=np.zeros_like(expected);mom=np.zeros((1,99));me=np.zeros_like(mom)
 expected[0,0,0]=-X**2*u+w[0]*u*zk**2*ff/ga**4
 expected[0,0,1]=w[0]*u*zk/ga**2;expected[0,3,0]=-w[0]*zk*ff/ga**2;mom[0,0]=w[0]*zk/ga
 ee[0,0,0]=X**2*abs(u)+abs(w[0]*u*zk**2*ff/ga**4);ee[0,0,1]=abs(expected[0,0,1]);ee[0,3,0]=abs(expected[0,3,0]);me[0,0]=abs(mom[0,0])
 value=np.zeros((1,99));value[0,0]=2/7;value[0,3]=-3/11;dv=np.zeros((1,4,99));dv[0,1,0]=5/13;dv[0,2,3]=7/17
 eta,de,ze,dze=native_configuration_lift(s,c,cj,value,dv);terms,env,*_=variation(s,eta,de,ze,dze)
 direct=terms.sum(axis=1);want=np.einsum('pij,pij->p',expected,np.stack((value,dv[:,1],dv[:,2]),axis=-1))
 actual=np.r_[cc['coefficient'].ravel(),cc['momentum'].ravel(),direct];target=np.r_[expected.ravel(),mom.ravel(),want]
 bound=np.r_[(cc['envelope']+ee).ravel(),(cc['momentum_envelope']+me).ravel(),env.sum(axis=1)+np.einsum('pij,pij->p',ee,abs(np.stack((value,dv[:,1],dv[:,2]),axis=-1)))]
 for n,v in dict(native_expected=expected,native_expected_envelope=ee,momentum_expected=mom,native_value=value,native_dvalue=dv,direct_terms=terms,direct_expected=want).items():euler_fixture_keep(n,v)
 check('new_Euler_tilted_static_chart_value_flux_and_affine_momentum',actual,target,bound)
 # RR canonical metric chart: fixed covariant u,zsp, not longitudinal normalization.
 # Keep value, R-gradient and Z-gradient jets separately so small gradient is visible.
 av=[];ev=[];be=[];P0=-7/13;PX0=11/17
 pot=q2/2+q2*q2/(4*kj)
 vr=X**2*u*u/4-w[0]*pot/2+w[0]*ff*zk**2/(2*ga**4)+P0/2
 gr=-w[0]*zk*u*u/(2*ga**2)
 for jet in range(3):
  f=np.array([float(jet==0)]);df=np.zeros((1,4))
  if jet:df[:,jet]=1.
  q,dq,eta,de,ze,dze=metric_configuration_lift(s,c,cj,0,f,df)
  mt,mv,_=metric_native(s,q,dq,eta,de);zt,zv,*_=variation(s,np.zeros_like(eta),np.zeros_like(de),ze,dze)
  pt,pv=phase_metric_direction(s,q,np.array([P0]),np.array([PX0]),np.array([X]))
  av.append((mt+zt).sum()+pt.sum());ev.append(vr*f[0]+gr*df[0,1]);be.append(mv.sum()+zv.sum()+pv.sum()+abs(ev[-1]))
  # First differentiated unit/transverse identities, with base partial jets zero.
  unit=np.einsum('pab,pa,pb->p',q,U,U)+2*np.einsum('pa,pab,pb->p',U,g,eta)
  tran=np.einsum('pa,jpa->jp',eta,z)+np.einsum('pa,jpa->jp',U,ze)
  ujet=np.einsum('pabc,pb,pc->pa',dq,U,U)+2*np.einsum('pb,pbc,pac->pa',U,g,de)
  tjet=np.einsum('pam,jpm->jpa',de,z)+np.einsum('pm,jpam->jpa',U,dze)
  ub=np.einsum('pab,pa,pb->p',abs(q),abs(U),abs(U))+2*np.einsum('pa,pab,pb->p',abs(U),abs(g),abs(eta))
  tb=np.einsum('pa,jpa->jp',abs(eta),abs(z))+np.einsum('pa,jpa->jp',abs(U),abs(ze))
  ujb=np.einsum('pabc,pb,pc->pa',abs(dq),abs(U),abs(U))+2*np.einsum('pb,pbc,pac->pa',abs(U),abs(g),abs(de))
  tjb=np.einsum('pam,jpm->jpa',abs(de),abs(z))+np.einsum('pm,jpam->jpa',abs(U),abs(dze))
  zeros=np.r_[unit.ravel(),tran.ravel(),ujet.ravel(),tjet.ravel()];zb=np.r_[ub.ravel(),tb.ravel(),ujb.ravel(),tjb.ravel()]
  av.extend(zeros.tolist());ev.extend(np.zeros_like(zeros).tolist());be.extend(zb.tolist())
  for n,v in dict(q=q,dq=dq,eta=eta,deta=de,zeta=ze,dzeta=dze,native_terms=mt,mode_complement=zt,phase_terms=pt,constraints=zeros,constraint_envelope=zb).items():euler_fixture_keep('RR_'+str(jet)+'_'+n,v)
 check('new_Euler_fixed_covector_metric_chart_and_absolute_phase_contact',np.asarray(av),np.asarray(ev),np.asarray(be))
 # Nonzero 3D curvature: psi=exp(A Z), at Z=0, h=psi^4 diag(1,1,R^2).
 # Exact paired first-order scalar curvature bulk is 4|grad psi|^2/C.
 R=np.array([2.]);A=1/5;f=2/7;dfz=-3/11;hh=np.diag([1.,1.,4.]);g=np.zeros((1,4,4));g[0,0,0]=-1;g[0,1:,1:]=hh
 dg=np.zeros((1,4,4,4));dg[0,1,3,3]=4.;dg[0,2,1:,1:]=4*A*hh
 U=np.array([[1.,0.,0.,0.]]);du=np.zeros((1,4,4));z=np.zeros((32,1,4));dz=np.zeros((32,1,4,4));phi=np.zeros((1,4))
 sh,ch,jh=euler_fixture_state(g,dg,U,du,z,dz,phi,w,xi,om)
 H=(4*f*hh)[None];dH=np.zeros((1,4,3,3));dH[0,1]=4*f*dg[0,1,1:,1:];dH[0,2]=4*dfz*hh+4*f*dg[0,2,1:,1:]
 eh=EH_spatial_metric_direction(sh,ch,jh,H,dH,R);target=np.array([8*(A*A*f+A*dfz)/C])
 euler_fixture_keep('curvature_terms',eh['terms']);euler_fixture_keep('curvature_expected',target)
 check('new_Euler_EH_nonzero_conformal_spatial_configuration_force',eh['value'],target,eh['envelope'].sum(axis=1)+8*(abs(A*A*f)+abs(A*dfz))/C)
 # Flat cylindrical h, nonzero anisotropic K, fixed coordinate hdot variation.
 kap=np.array([1/3,-2/5,4/7]);g=np.zeros((1,4,4));g[0,0,0]=-1;g[0,1:,1:]=hh
 dg=np.zeros((1,4,4,4));dg[0,1,3,3]=4.;dg[0,0,1:,1:]=2*np.diag(kap*np.array([1.,1.,4.]))
 sh,ch,jh=euler_fixture_state(g,dg,U,du,z,dz,phi,w,xi,om)
 H=np.zeros((1,3,3));H[0,0,0]=1;dH=np.zeros((1,4,3,3));eh=EH_spatial_metric_direction(sh,ch,jh,H,dH,R)
 trace=kap.sum();Q=(kap*kap).sum()-trace*trace;target=np.array([(Q/2-2*kap[0]**2+2*trace*kap[0])/(2*C)])
 euler_fixture_keep('kinetic_configuration_terms',eh['terms']);euler_fixture_keep('kinetic_configuration_expected',target)
 check('new_Euler_EH_fixed_hdot_anisotropic_configuration_force',eh['value'],target,eh['envelope'].sum(axis=1)+(abs(Q)/2+2*kap[0]**2+2*abs(trace*kap[0]))/(2*C))
 # Moving covector chart z=a y. P_a=p_a+(z/a)p_z is a derived OLD-chart
 # combination; it is independent canonical only with y=z/a,P_y=a p_z.
 aa=3/2;Hr=2/5;zs=(B*GC)*xi[0]**2*(3/7);zd=zs*(7/11)
 hh=aa**2*np.diag([1.,1.,4.]);g=np.zeros((1,4,4));g[0,0,0]=-1;g[0,1:,1:]=hh
 dg=np.zeros((1,4,4,4));dg[0,0,1:,1:]=2*Hr*hh;dg[0,1,3,3]=4*aa**2
 z=np.zeros((32,1,4));z[0,0,2]=zs;dz=np.zeros((32,1,4,4));dz[0,0,0,2]=zd
 sh,ch,jh=euler_fixture_state(g,dg,U,du,z,dz,phi,w,xi,om);nc=canonical_native_coefficients(sh,ch,jh);pm,ph=reduced_momenta(sh,ch)
 pz=w[0]*aa*R[0]*(zd-Hr*zs);az=-Hr*pz-w[0]*aa*R[0]*zs*(1+zs**2/(kj*aa**2));pa=-zs*pz/aa
 got=np.array([nc['momentum'][0,4],nc['coefficient'][0,4,0],2*aa*(ph[0,0]+ph[0,1]+4*ph[0,2])]);target=np.array([pz,az,pa])
 eb=np.array([nc['momentum_envelope'][0,4],nc['envelope'][0,4,0],abs(got[2])+abs(pa)])+abs(target)
 for n,v in dict(scale_momentum=pm,scale_metric_momentum=ph,scale_expected=target,scale_raw_value=nc['coefficient']).items():euler_fixture_keep(n,v)
 check('new_Euler_scale_mode_covector_affine_time_chart_contacts',got,target,eb)
 # Fixed canonical momentum, not fixed circular velocity/Omega.
 g=np.diag([-1.,1.,1.,1.])[None];p=np.array([[9/20,3/5,0.]]);mass=np.array([7/11]);force,env=ordinary_metric_force(g,p,mass)
 target=mass[:,None]*np.array([[81.,144.,0.,216.,0.,0.]])/1000
 for n,v in dict(ordinary_metric=g,ordinary_fixed_p=p,ordinary_mass=mass,ordinary_force=force,ordinary_expected=target).items():euler_fixture_keep(n,v)
 check('new_Euler_ordinary_fixed_canonical_momentum_metric_force',force,target,env+abs(target))
 assert len(CHECKS)-start==6
 return dict(new_controls=6,scope='Fresh artificial spatial/configuration force contacts only; no physical source, EOS, clock, gauge or history selected')

def radial_curvature_fixture():
 R=np.array([2.]);a=3/2;ar=2/7;f=-3/11;fr=5/13;bar=np.diag([1.,1.,4.]);br=np.zeros((3,3));br[2,2]=4.
 g=np.zeros((1,4,4));g[0,0,0]=-1;g[0,1:,1:]=a*a*bar;dg=np.zeros((1,4,4,4));dg[0,1,1:,1:]=2*a*ar*bar+a*a*br
 U=np.array([[1.,0.,0.,0.]]);du=np.zeros((1,4,4));z=np.zeros((32,1,4));dz=np.zeros((32,1,4,4));phi=np.zeros((1,4));xi=np.arange(1.,33.)/33;w=np.full(32,1/32);omega=np.ones(32)
 s,c,cj=euler_fixture_state(g,dg,U,du,z,dz,phi,w,xi,omega);H=(2*a*f*bar)[None];dH=np.zeros((1,4,3,3));dH[0,1]=2*(ar*f+a*fr)*bar+2*a*f*br
 eh=EH_spatial_metric_direction(s,c,cj,H,dH,R);target=np.array([-ar*ar*f/(C*a*a)+2*ar*fr/(C*a)]);env=eh['envelope'].sum(axis=1)+abs(ar*ar*f/(C*a*a))+abs(2*ar*fr/(C*a))
 capture('radial_curvature_fixture_terms',eh['terms']);capture('radial_curvature_fixture_target',target)
 check('new_Euler_EH_radial_warp_complete_cylindrical_configuration_jet',eh['value'],target,env)

def restore_force_column0(cached):
 # Literal saved state/coefficients only. Never replay features/chart/nativecoeff.
 global RAW,AVAILABLE
 RAW={'failed_V001_'+k:a.copy() for k,a in cached.items()};AVAILABLE={}
 s={k.removeprefix('current_'):a for k,a in cached.items() if k.startswith('current_')}
 c={k.removeprefix('loaded_owned_chart_'):a for k,a in cached.items() if k.startswith('loaded_owned_chart_')}
 cj={k.removeprefix('chart_first_'):a for k,a in cached.items() if k.startswith('chart_first_')}
 native={k.removeprefix('native_config_'):a for k,a in cached.items() if k.startswith('native_config_')}
 old={k:cached['loaded_'+k] for k in ('R','Z','reference_volume','phase_Pstar','phase_P_X','phase_P_XX','phase_X','phase_canonical_density')}
 met={k:cached['loaded_'+k] for k in ('B','B_envelope','current_metric_pistar','current_metric_time_jet','current_metric_time_tensor','current_native_pstar','old_native_target')}
 for k,a in cached.items():
  if k.startswith('seed_'):capture(k,a)
 s['R']=old['R'];s['Z_coordinate']=old['Z']
 expected=cached['control_007_new_seed_native_canonical_momentum_expected']
 assert np.array_equal(native['momentum'],cached['control_007_new_seed_native_canonical_momentum_actual'])
 assert np.array_equal(old['R'],GEO['R'][0]) and np.array_equal(old['reference_volume'],GEO['dv'][0])
 return s,c,cj,native,old,met,expected

def spatial_euler_column(iq,wr,qr,mr,bc,sol,xi,w,omega,Hbar,cached=None):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};CONTEXT.update(column=iq,stage='canonical_spatial_Euler_loads');start=len(CHECKS)
 if cached is not None:
  assert iq==0;s,c,cj,native,old,met,expected=restore_force_column0(cached)
 else:
  s,c,cj,old,met,expected=load_seed_column(iq,wr,qr,mr,bc,sol,xi,w,omega);native=canonical_native_coefficients(s,c,cj)
 mom=current_seed_witnesses(s,c,cj,native,old,met,expected,bc,iq)
 metric=canonical_metric_coefficients(s,c,cj,old['R'],old['phase_Pstar'],old['phase_P_X'],old['phase_X'])
 configuration_direction_controls(s,c,cj,native,metric,old['R'],old['phase_Pstar'],old['phase_P_X'],old['phase_X'])
 klo=np.einsum('pl,pa,pb->plab',s['Z'],s['U'],s['U'])-np.einsum('jpab,jpl->plab',(s['Pi']+s['Pi'].swapaxes(2,3))/2,s['z']);conn,Dconn,mx=connection_momentum(s)
 data=dict(native_Euler_coefficient=native['coefficient'],native_Euler_envelope=native['envelope'],metric_Euler_coefficient=metric['coefficient'],metric_Euler_envelope=metric['envelope'],metric_Euler_component_coefficients=metric['terms'],metric_Euler_component_envelope=metric['term_envelope'],native_raw_Az=native['A_z_raw'])
 data.update(mom)
 if cached is not None:data.update({'failed_V001_'+k:a for k,a in cached.items()})
 data.update({k:a for k,a in RAW.items() if k.startswith(('momentum_operation_','original_postcancel_','new_full_'))})
 for k in ('g','hi','Ga','U','uc','du','z','dz','phi','nu','nz','P','q','V','D','F','Fup','Pi','PiU','Z','A','mu','a','r','f','z2'):data['seed_'+k]=s[k]
 data.update(seed_V_raised=raise_cov(s['hi'],s['V']),seed_connection_Klo=klo,seed_connection_momentum=conn,seed_connection_D=Dconn,seed_connection_Maxwell=mx,seed_R=old['R'],seed_Z_coordinate=old['Z'],seed_phase_P=old['phase_Pstar'],seed_phase_PX=old['phase_P_X'],seed_phase_PXX=old['phase_P_XX'],seed_phase_X=old['phase_X'])
 for k,a in c.items():data['seed_chart_'+k]=a
 for k,a in cj.items():data['seed_chart_derivative_'+k]=a
 for k in ('seed_nodal_native_rate','seed_old_L2_native_rate','seed_native_rate_delta','seed_covariant_native_rate_R','seed_covariant_native_rate_Z','seed_metric_L2_rate','seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot'):data[k]=AVAILABLE[k]
 for a,idx in (('R',1),('Z',2)):data['seed_metric_L2_rate_'+a]=2*Hbar*(cj['dN'][:,idx,None,None]*c['h']+c['N'][:,None,None]*cj['dh'][:,idx])
 data.update({k:a for k,a in RAW.items() if k.startswith('control_')})
 for n,a in data.items():finite_real('final_'+n,a)
 assert len(CHECKS)-start==6
 rec=checkpoint('COLUMN',data,dict(kind='new_sigma1_canonical_spatial_Euler_coefficients_on_explicit_mixed_seed',sigma=SIGMA,column=iq,points=3784,controls=CHECKS[start:],whole_parent=wr,owned_parent=qr,metric_parent=mr,coefficient_jet_order=['value','R','Z'],native_order='covariant U_i followed by32 covariant z_ji',metric_local_order=['RR','ZZ','phiphi','RZ','Rphi','Zphi'],component_order=['Maxwell','relative_phase','mode_time','mode_quadratic','mode_quartic','mode_projected_gradient','acceleration_Z','absolute_phase_X','absolute_phase_measure','EH_curvature_DV_C','EH_curvature_DV_traceC','EH_curvature_CC','EH_kinetic_measure','EH_kinetic_deltaK','EH_kinetic_inverse_metric'],seed_scope='CLOSED nodal native99 rate; earlier prescribed L2 metric kstar, not a metric nodal solution',unknown_ports=dict(native_outer=None,metric_spatial_GHY=None,ADM_time_GHY=None,phase_current=None,ordinary_traction=None,exterior=None,activity_outside_0p3_15p1=None),no_acceleration_derivative_computed=False,physical_changes=[]))
 keep={n:data[n] for n in ('native_Euler_coefficient','native_Euler_envelope','metric_Euler_coefficient','metric_Euler_envelope','metric_Euler_component_coefficients','metric_Euler_component_envelope')}
 return keep,rec

def force_weak_assembly(columns,ordinary,r):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};CONTEXT.update(stage='actual_weak_configuration_force_scatter');start=len(CHECKS)
 nc=np.concatenate([d['native_Euler_coefficient'] for d in columns]);ne=np.concatenate([d['native_Euler_envelope'] for d in columns]);mc=np.concatenate([d['metric_Euler_coefficient'] for d in columns]);me=np.concatenate([d['metric_Euler_envelope'] for d in columns])
 nl=scatter_configuration_coefficients(nc,GEO,'native');capture('native_spatial_Euler_load',nl);nle=scatter_configuration_coefficients(ne,GEO,'native',envelope=True);capture('native_spatial_Euler_envelope',nle);ni=scatter_configuration_coefficients(nc,GEO,'native',independent=True)
 check('new_native99_value_R_Z_force_scatter_incidence',nl,ni,nle+abs(ni))
 ml=scatter_configuration_coefficients(mc,GEO,'metric');capture('metric_spatial_Euler_bulk_load',ml);mle=scatter_configuration_coefficients(me,GEO,'metric',envelope=True);capture('metric_spatial_Euler_bulk_envelope',mle);mi=scatter_configuration_coefficients(mc,GEO,'metric',independent=True)
 check('new_six_metric_value_R_Z_force_scatter_incidence',ml,mi,mle+abs(mi))
 nt=(np.arange(nl.size)%11-5).reshape(nl.shape)/31.;mt=(np.arange(ml.size)%7-3).reshape(ml.shape)/29.;nv=np.stack([evaluate_velocity(nt,GEO,j) for j in range(3)],axis=-1);mv=np.stack([evaluate_metric(mt,GEO,j) for j in range(3)],axis=-1);weight=(GEO['dv']/GEO['R']).reshape(15136)
 direct=np.array([np.einsum('pgcj,gpcj,p->',nc.reshape(15136,33,3,3),nv,weight),np.einsum('paj,paj,p->',mc,mv,weight)]);actual=np.array([np.sum(nl*nt),np.sum(ml*mt)])
 den=np.array([np.einsum('pgcj,gpcj,p->',ne.reshape(15136,33,3,3),abs(nv),weight)+np.sum(nle*abs(nt)),np.einsum('paj,paj,p->',me,abs(mv),weight)+np.sum(mle*abs(mt))])
 capture('weak_force_native_test',nt);capture('weak_force_metric_test',mt);capture('weak_force_direct_functional',direct)
 check('new_spatial_force_registered_basis_functional_pairing',actual,direct,den)
 comp=np.concatenate([d['metric_Euler_component_coefficients'] for d in columns]);ce=np.concatenate([d['metric_Euler_component_envelope'] for d in columns]);loads=[];bounds=[]
 for k in range(15):
  loads.append(scatter_configuration_coefficients(comp[:,:,:,k],GEO,'metric'));bounds.append(scatter_configuration_coefficients(ce[:,:,:,k],GEO,'metric',envelope=True));capture('metric_spatial_Euler_completed_component_loads',np.stack(loads));capture('metric_spatial_Euler_completed_component_envelopes',np.stack(bounds))
 loads=np.stack(loads);bounds=np.stack(bounds);check('new_metric_Euler_signed_component_recontraction',loads.sum(axis=0),ml,bounds.sum(axis=0)+mle)
 source=read_pair(ordinary,('source_R','source_Z','source_g','source_mass_weight','source_specific_covariant_p','source_indices','source_right_weight'));ordinary_load,ordinary_env=ordinary_metric_load(source,r)
 total=ml+ordinary_load;capture('complete_known_metric_spatial_Euler_load',total)
 data=dict(native_spatial_Euler_load=nl,native_spatial_Euler_envelope=nle,metric_spatial_Euler_bulk_load=ml,metric_spatial_Euler_bulk_envelope=mle,metric_spatial_Euler_component_loads=np.concatenate((loads,ordinary_load[None])),metric_spatial_Euler_component_envelope=np.concatenate((bounds,ordinary_env[None])),ordinary_metric_spatial_Euler_load=ordinary_load,ordinary_metric_spatial_Euler_envelope=ordinary_env,complete_known_metric_spatial_Euler_load=total,complete_known_metric_spatial_Euler_envelope=mle+ordinary_env)
 data.update({k:a for k,a in AVAILABLE.items() if k.startswith('ordinary_') or k.startswith('weak_force_')});data.update({'ordinary_input_'+k:a for k,a in source.items()});data.update({k:a for k,a in RAW.items() if k.startswith('control_')})
 for n,a in data.items():
  if n=='ordinary_input_source_indices':
   capture('summary_'+n,a);assert a.dtype==np.dtype('int64') and np.all((a>=0)&(a<86))
  else:finite_real('summary_'+n,a)
 assert len(CHECKS)-start==5
 return checkpoint('LOADS',data,dict(kind='genuine_weak_native99_and_six_metric_spatial_Euler_loads',sigma=SIGMA,controls=CHECKS[start:],native_basis=380292,metric_basis=23048,modes=32,quadrature_points=15136,force_scope='spatial E only; E minus pdot_noacc not yet computed',port_scope='actual algebraic outer hats retained; physical outer/time/traction ports remainunknown',unknowns=dict(metric_rate_target=None,free_shear=None,force_convective=None,CMC_preservation=None,phase_charge_evolution=None,ordinary_support_evolution=None,exterior_history=None,activity_outside_0p3_15p1=None),physical_changes=[]))

def new_force_packet(weak,whole,q1,metric,solution,ordinary,fixed,cp,failed):
 global RAW,AVAILABLE,GEO,B
 ev=read_pair(failed['input'],tuple(failed['input']['metadata']['schema']));xi=ev['xi'];w=ev['weights'];assert np.all(w>0) and np.all(xi>0) and np.all(np.diff(xi)>0)
 B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2;omega=SIGMA*xi*fixed['Hunit']/299792458.;Hbar=fixed['Hunit']/299792458.*cp['background']['h'];assert np.all(np.isfinite(omega)) and np.all(omega>0) and math.isfinite(Hbar) and Hbar>0
 checkpoint('INPUT',ev,dict(kind='unchanged_sigma1_configuration_spectrum_and_owned_seed_references',sigma=SIGMA,fixed=fixed,owned_background=cp['background'],Hbar=Hbar,new_source_terms=False,uncomputed_physical_sigma=[.1,10.,100.],weak99_solution=solution,failed_ancestor=failed['error']['owner'],original_controls=failed['error']['controls'],original_failure_retained=True))
 RAW={};AVAILABLE={};fixture=read_pair(failed['fixture'],tuple(failed['fixture']['metadata']['schema']));CHECKS.extend(json.loads(json.dumps(failed['error']['controls'][:7])))
 assert len(CHECKS)==7 and all(x['passed'] is True for x in CHECKS)
 checkpoint('FIXTURE',fixture,dict(kind='seven_exact_reused_independent_canonical_configuration_force_contacts',controls=CHECKS[:],old_pair=dict(file=failed['fixture']['file'],sha256=failed['fixture']['sha256']),no_fixture_replay=True,physical_seed=False))
 RAW={};AVAILABLE={};geo=read_pair(failed['basis'],tuple(failed['basis']['metadata']['schema']));GEO=dict(R=geo['geometry_R'],dv=geo['geometry_dv'],hats=geo['geometry_hats'],cell_i=geo['geometry_cell_i'],cell_j=geo['geometry_cell_j'],r=geo['r_kpc'],z=geo['z_kpc']);assert np.array_equal(geo['native_independent_mask'],native_mask()) and np.all(GEO['R']>0) and np.all(GEO['dv']>0)
 checkpoint('BASIS',geo,dict(kind='unchanged_genuine_native_and_regular_six_metric_configuration_basis',native_basis=380292,metric_basis=23048,old_pair=dict(file=failed['basis']['file'],sha256=failed['basis']['sha256']),basis_replay=False,temporal_basis_reinterpretation=False,physical_wall_selected=False))
 cached=read_pair(failed['raw'],tuple(failed['raw']['metadata']['schema']))
 bc=read_weak_metric_coefficients(weak);sol=read_pair(solution,('recovered_nodal_native_velocity','recovered_qpoint_native_velocity','recovered_qpoint_native_velocity_R','recovered_qpoint_native_velocity_Z','recovered_point_momentum_density'));data=[];records=[]
 for iq,(wr,qr,mr) in enumerate(zip(whole['columns'],q1['columns'],metric)):
  d,rec=spatial_euler_column(iq,wr,qr,mr,bc,sol,xi,w,omega,Hbar,cached if iq==0 else None);data.append(d);records.append(rec)
 load=force_weak_assembly(data,ordinary,ev['r_kpc']);assert len(CHECKS)==EXPECTED_CONTROLS
 return dict(sigma=SIGMA,status='CONDITIONAL_WEAK_CANONICAL_SPATIAL_EULER_LOADS_PASS',columns=records,loads=load,qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded canonical spatial Euler loads: complete FULL root/distinct review required.')
 assert PROTOCOL_SHA and len(PROTOCOL_SHA)==64 and sha(path(STEM+'.md'))==PROTOCOL_SHA
 assert not list(BASE.glob(STEM+'_*')),'Unused namespace required; all old results preserved'
 INPUTS,weak,whole,q1,metric,solution,ordinary,fixed,cp,failed=spatial_euler_admission()
 INPUTS[str(path(STEM+'.md').resolve())]=PROTOCOL_SHA;INPUTS[str(Path(__file__).resolve())]=sha(__file__);OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(sigma=SIGMA,modes=32,columns=4,points=15136,native_basis=380292,metric_basis=23048,controls=EXPECTED_CONTROLS,pairs=8,tolerance=TOL,configuration_jet_tests=18,kinetic_replay=False,new_solve=False),qualification=FLAGS))
  import numpy as _np
  np=_np
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=new_force_packet(weak,whole,q1,metric,solution,ordinary,fixed,cp,failed)
  assert len(CHECKS)==EXPECTED_CONTROLS and all(c['passed'] for c in CHECKS) and len(RECORDS)==8
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_WEAK_CANONICAL_SPATIAL_EULER_ARITHMETIC_PASS',cases=[case],controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS))
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\nComplete new sigma1 canonical native99 and six-metric spatial Euler coefficients and registered weak loads on the explicit conditional seed. All32 modes, absolute phase pressure and fixed-p conserved annular source remain once.\n\nThe CLOSED nodal native rate replaces only the old native L2 rate. The earlier prescribed L2 metric kstar remains distinct from a nodal metric solution. Actual new seed momenta/current/time jets are retained. No convective momentum derivative, acceleration, CMC solve, physical rate, source gain, history or metric correction is selected.\n').encode());recheck();json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS));recheck();print('CONDITIONAL_WEAK_CANONICAL_SPATIAL_EULER_ARITHMETIC_PASS',len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None;available=dict(AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unqualified_available_canonical_spatial_Euler_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  if prior:OUTPUTS[STEM+'_RECEIPT.json']=prior
  eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=[p.name for p in BASE.glob(STEM+'*.npz') if p.name not in {r['file'] for r in RECORDS}],qualification=FLAGS))
  if prior is None:json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS))
  seal_actual();recheck(False);raise

if __name__=='__main__':main()
