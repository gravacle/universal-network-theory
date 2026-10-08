"""Guarded analytic D0 caller workdraft; no author science execution."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback,ast,zipfile,struct
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WEAK_CANONICAL_MOMENTUM_TIME_DERIVATIVE_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
FORCE_PID=None
FORCE_RESULT_SHA=None
FORCE_RECEIPT_SHA=None
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
B=None;TOL=2e-11;EXPECTED_CONTROLS=33
np=None;GEO=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(momentum_time_derivative_qualified=False,force_convective_qualified=False,CMC_qualified=False,physical_metric_qualified=False,history_qualified=False,exterior_qualified=False,source_qualified=False,galaxy_velocity_qualified=False)
PINS={'author_fragment_force_v003_success_d0_admission_v002.txt':'ba8bba3db2f3cf8a3151e831c3e996e3a252ea80b73027fca207d494bfa607f6','authoring_momentum_time_derivative_v001_1122_14b620bd.py':'14b620bdfda77d2b6d68e1189784c36d284b2e07fb5fa59c43e6dfb5182f5ea7','authoring_momentum_time_derivative_v001_1038_a628f36a.py':'a628f36ad7f67ed140a6418ff839621f2a4da8a4f33b83f94896438d1fc2fff2','author_fragment_force_v003_success_d0_admission_v001.txt':'1b95ffa96d38b5fc89d4e864a2a4ce69d8c71dc00e5d21fae6bed7760d1f3ff9','author_fragment_fresh_D0_momentum_fixtures_v001.txt':'cebf2c7031cfac949fa50402b0a3cb3e903373cf9af3f5881949a26054993baa','author_fragment_D0_EH_operation_envelope_v001.txt':'f9e6b3716c9dbc87c3a90f3beb2c9d8bbc3b3621454e326f7493f23bcfc85472','author_fragment_d0_derivative_operation_envelopes_v001.txt':'f9be8d463e387c5c443395f539fd13092b491a7a809f77f92358686c652f3e45','author_fragment_D0_primitive_chart_operation_envelopes_v001.txt':'5d26904ef524f2d5631949f6ee5eeab7dcc7298103871ac232ff674635c03038','author_fragment_spatial_euler_v002_momentum_envelopes.txt':'c333059f668027a34b4f17d566aca5d6202e7b9ab290956513288efbd34268d3','authoring_momentum_time_derivative_v001_623_85c4afd2.py':'85c4afd26c926d3bde8a47c0cbc2d39b2c7c9cada7b5e72f8c953bb9feca3bb3','authoring_momentum_time_derivative_v001_596_596b208a.py':'596b208a40d7d5d9ac61ed2ee7315e86e554737a9069acb2765ba339f35b0378','authoring_momentum_time_derivative_v001_475_1aec4776.py':'1aec4776026b2b2b730924010c180ddd808a1f95f84b7012f9f58ec658cb60f6','authoring_spatial_euler_v003_reviewed1189_5ecfcfd3.py':'5ecfcfd3aed0b85aae186dbc88bbbd2b10ef0695080eabe2aef9a325d3644f76','author_fragment_weak_momentum_time_derivative_v002.py':'ac627a75c27b5e1e306017d3c6ae0d599de2e72580c86206a6c27f71ab9d3155','CROSS_U_WEAK_CANONICAL_MOMENTUM_NO_ACCELERATION_DERIVATIVE_V001.md':'c7da6054e73dd1c696876aa7e6d51d3151e5b925ac82769b798a2286f1d46c51'}
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


def metric_basis():
 e=np.zeros((6,3,3))
 for k,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[k,i,j]=e[k,j,i]=1
 return e


def tensor_momentum_coordinates(pi):
 return np.stack((pi[...,0,0],pi[...,1,1],pi[...,2,2],2*pi[...,0,1],2*pi[...,0,2],2*pi[...,1,2]),axis=-1)


def gauge_velocity_primary_direction(s,c,delta_n,delta_b,keep):
 # Independent primary test: vary ONLY coordinate gauge velocities, keeping
 # configuration, spatial jets and mechanical velocities fixed. No evolution.
 out={k:np.zeros_like(s[k]) for k in ('g','hi','Ga','U','du','z','dz')}
 N,be,h=c['N'],c['beta'],c['h'];U0=s['U'][:,0]
 out['du'][:,0,0]=-U0*delta_n/N
 out['du'][:,0,1:]=-U0[:,None]*delta_b-be*out['du'][:,0,0,None]
 t=np.einsum('pi,jpi->jp',s['U'][:,1:],s['z'][:,:,1:])
 out['dz'][:,:,0,0]=-np.einsum('pi,jpi->jp',out['du'][:,0,1:],s['z'][:,:,1:])/U0[None]+t*out['du'][None,:,0,0]/U0[None]**2
 dj=np.zeros((len(N),4,4,4));dj[:,0,0,0]=-2*N*delta_n+2*np.einsum('pi,pij,pj->p',be,h,delta_b)
 dj[:,0,0,1:]=np.einsum('pij,pj->pi',h,delta_b);dj[:,0,1:,0]=dj[:,0,0,1:]
 for a in range(4):
  for bb in range(4):out['Ga'][:,:,a,bb]=np.einsum('plm,pm->pl',s['hi'],dj[:,a,bb,:]+dj[:,bb,a,:]-dj[:,:,a,bb])/2
 for name,a in out.items():keep('primary_gauge_'+name,a)
 return out


def primitive_time_direction(s,c,cj,v,k,v_spatial,k_spatial,n,b,n_spatial,b_spatial,n_second,b_second,keep):
 # Formal D0: native/metric mechanical accelerations zero. Gauge second jets
 # remain explicit until the primary cancellation has been proved/tested.
 # Spatial derivative axis is (R,Z,phi); supplied axisymmetric phi jets are zero.
 out={}
 def put(name,a):out[name]=a;keep('D0_primitive_'+name,a);return a
 p=len(c['N']);N,be,h,ih,u,up,ga=c['N'],c['beta'],c['h'],c['ih'],c['u'],c['up'],c['gamma']
 vu=v[:,:3];vz=v[:,3:].reshape(p,32,3).transpose(1,0,2)
 va=np.zeros((p,4,99));va[:,1:]=v_spatial
 ha=np.zeros((p,4,3,3));ha[:,1:]=k_spatial
 na=np.empty((p,4));na[:,0]=n_second;na[:,1:]=n_spatial
 ba=np.empty((p,4,3));ba[:,0]=b_second;ba[:,1:]=b_spatial
 vua=va[:,:,:3];vza=va[:,:,3:].reshape(p,4,32,3).transpose(2,0,1,3)
 dih=-np.einsum('pij,pjk,pkl->pil',ih,k,ih)
 diha=-np.einsum('pij,pajk,pkl->pail',dih,cj['dh'],ih)-np.einsum('pij,pajk,pkl->pail',ih,ha,ih)-np.einsum('pij,pajk,pkl->pail',ih,cj['dh'],dih)
 dup=np.einsum('pij,pj->pi',dih,u)+np.einsum('pij,pj->pi',ih,vu)
 dupa=np.einsum('paij,pj->pai',diha,u)+np.einsum('paij,pj->pai',cj['dih'],vu)+np.einsum('pij,paj->pai',dih,cj['du_cov'])+np.einsum('pij,paj->pai',ih,vua)
 dga=(np.einsum('pi,pi->p',up,vu)+np.einsum('pi,pij,pj->p',u,dih,u)/2)/ga
 dga_a=(np.einsum('pi,pai->pa',dup,cj['du_cov'])+np.einsum('pi,pai->pa',up,vua)+np.einsum('pi,paij,pj->pa',vu,cj['dih'],u)+np.einsum('pi,paij,pj->pa',u,diha,u)/2)/ga[:,None]-cj['dgamma']*dga[:,None]/ga[:,None]
 dU=np.empty_like(s['U']);dU[:,0]=dga/N-ga*n/N**2
 dU[:,1:]=dup-b*s['U'][:,0,None]-be*dU[:,0,None];put('U',dU)
 ddu=np.empty_like(s['du'])
 ddu[:,:,0]=dga_a/N[:,None]-cj['dgamma']*n[:,None]/N[:,None]**2-dga[:,None]*cj['dN']/N[:,None]**2-ga[:,None]*na/N[:,None]**2+2*ga[:,None]*cj['dN']*n[:,None]/N[:,None]**3
 ddu[:,:,1:]=dupa-ba*s['U'][:,None,0,None]-cj['dbeta']*dU[:,None,0,None]-b[:,None,:]*s['du'][:,:,0,None]-be[:,None,:]*ddu[:,:,0,None];put('du',ddu)
 zsp=s['z'][:,:,1:];zspa=s['dz'][:,:,:,1:];U0=s['U'][:,0];U0a=s['du'][:,:,0]
 t=np.einsum('pi,jpi->jp',s['U'][:,1:],zsp)
 ta=np.einsum('pai,jpi->jpa',s['du'][:,:,1:],zsp)+np.einsum('pi,jpai->jpa',s['U'][:,1:],zspa)
 dt=np.einsum('pi,jpi->jp',dU[:,1:],zsp)+np.einsum('pi,jpi->jp',s['U'][:,1:],vz)
 dta=np.einsum('pai,jpi->jpa',ddu[:,:,1:],zsp)+np.einsum('pai,jpi->jpa',s['du'][:,:,1:],vz)+np.einsum('pi,jpai->jpa',dU[:,1:],zspa)+np.einsum('pi,jpai->jpa',s['U'][:,1:],vza)
 dz=np.empty_like(s['z']);dz[:,:,1:]=vz;dz[:,:,0]=-dt/U0[None]+t*dU[None,:,0]/U0[None]**2;put('z',dz)
 ddz=np.empty_like(s['dz']);ddz[:,:,:,1:]=vza
 ddz[:,:,:,0]=-dta/U0[None,:,None]+ta*dU[None,:,None,0]/U0[None,:,None]**2+dt[:,:,None]*U0a[None]/U0[None,:,None]**2+t[:,:,None]*ddu[None,:,:,0]/U0[None,:,None]**2-2*t[:,:,None]*U0a[None]*dU[None,:,None,0]/U0[None,:,None]**3;put('dz',ddz)
 dg=np.empty_like(s['g']);dg[:,1:,1:]=k;dg[:,0,1:]=np.einsum('pij,pj->pi',k,be)+np.einsum('pij,pj->pi',h,b);dg[:,1:,0]=dg[:,0,1:]
 dg[:,0,0]=-2*N*n+np.einsum('pi,pij,pj->p',be,k,be)+2*np.einsum('pi,pij,pj->p',be,h,b);put('g',dg)
 ddg=np.empty_like(cj['dg']);ddg[:,:,1:,1:]=ha
 ddg[:,:,0,1:]=np.einsum('paij,pj->pai',ha,be)+np.einsum('paij,pj->pai',cj['dh'],b)+np.einsum('pij,paj->pai',k,cj['dbeta'])+np.einsum('pij,paj->pai',h,ba);ddg[:,:,1:,0]=ddg[:,:,0,1:]
 ddg[:,:,0,0]=-2*(cj['dN']*n[:,None]+N[:,None]*na)+2*np.einsum('pai,pij,pj->pa',cj['dbeta'],k,be)+np.einsum('pi,paij,pj->pa',be,ha,be)+2*np.einsum('pai,pij,pj->pa',cj['dbeta'],h,b)+2*np.einsum('pi,paij,pj->pa',be,cj['dh'],b)+2*np.einsum('pi,pij,paj->pa',be,h,ba);put('dg_partial',ddg)
 dhi=put('hi',-np.einsum('pij,pjk,pkl->pil',s['hi'],dg,s['hi']))
 dGa=np.empty_like(s['Ga'])
 for a in range(4):
  for bb in range(4):
   jet=cj['dg'][:,a,bb,:]+cj['dg'][:,bb,a,:]-cj['dg'][:,:,a,bb]
   djet=ddg[:,a,bb,:]+ddg[:,bb,a,:]-ddg[:,:,a,bb]
   dGa[:,:,a,bb]=(np.einsum('plm,pm->pl',dhi,jet)+np.einsum('plm,pm->pl',s['hi'],djet))/2
 put('Ga',dGa)
 return out


def derivative_chart(s,c,d,k,n,b,keep):
 # Mechanical configuration direction: du_cov=v_u, dz_cov=v_z, dh=k.
 # Complete dU,dz have already been produced by the constrained primitive lift.
 out={}
 def put(name,a):out[name]=a;keep('D0_chart_'+name,a);return a
 N,ih,u,up,ga,be=c['N'],c['ih'],c['u'],c['up'],c['gamma'],c['beta']
 dih=put('ih',-np.einsum('pij,pjk,pkl->pil',ih,k,ih))
 ducov=np.einsum('pia,pa->pi',d['g'][:,1:,:],s['U'])+np.einsum('pia,pa->pi',s['g'][:,1:,:],d['U'])
 dup=put('up',np.einsum('pij,pj->pi',dih,u)+np.einsum('pij,pj->pi',ih,ducov))
 dga=put('gamma',(np.einsum('pi,pi->p',up,ducov)+np.einsum('pi,pij,pj->p',u,dih,u)/2)/ga)
 dJU=np.empty_like(c['JU']);dJU[:,0]=dup/(N*ga)[:,None]-c['JU'][:,0]*(n/N+dga/ga)[:,None]
 dJU[:,1:]=dih-b[:,:,None]*c['JU'][:,None,0]-be[:,:,None]*dJU[:,None,0];put('JU',dJU)
 U0=s['U'][:,0];dU0=d['U'][:,0]
 put('Jzz',-d['U'][:,1:]/U0[:,None]+s['U'][:,1:]*dU0[:,None]/U0[:,None]**2)
 zJU=np.einsum('jpa,pai->jpi',s['z'],c['JU'])
 put('JzU',-(np.einsum('jpa,pai->jpi',d['z'],c['JU'])+np.einsum('jpa,pai->jpi',s['z'],dJU))/U0[None,:,None]+zJU*dU0[None,:,None]/U0[None,:,None]**2)
 # Fixed symmetric coordinate tensors; no derivative of an evolving tetrad basis.
 E=c['embed'][:,:,1:,1:];de=np.zeros_like(c['embed'])
 de[:,:,0,1:]=np.einsum('pkij,pj->pki',E,b);de[:,:,1:,0]=de[:,:,0,1:]
 de[:,:,0,0]=2*np.einsum('pi,pkij,pj->pk',be,E,b);put('embed',de)
 dt=2*np.einsum('pi,pkij,pj->pk',dup,E,up)
 dUh=np.empty_like(c['Uh']);dUh[:,:,0]=-dt/(2*N*ga)[:,None]-c['Uh'][:,:,0]*(n/N+dga/ga)[:,None]
 dUh[:,:,1:]=-np.einsum('pij,pkjl,pl->pki',dih,E,up)-np.einsum('pij,pkjl,pl->pki',ih,E,dup)-b[:,None,:]*c['Uh'][:,:,0,None]-be[:,None,:]*dUh[:,:,0,None];put('Uh',dUh)
 zUh=np.einsum('jpa,pka->jpk',s['z'],c['Uh'])
 put('zh',-(np.einsum('jpa,pka->jpk',d['z'],c['Uh'])+np.einsum('jpa,pka->jpk',s['z'],dUh))/U0[None,:,None]+zUh*dU0[None,:,None]/U0[None,:,None]**2)
 dl=put('log_dens',n/N+np.einsum('pij,pij->p',ih,k)/2)
 put('dens',c['dens']*dl);put('sqrt_h',c['sqrt_h']*np.einsum('pij,pij->p',ih,k)/2)
 return out


def derivative_native_momentum_features(s,d,keep):
 # Only differentiate actual primitive/feature operands. Fixed xi,w,omega.
 out={}
 def put(name,a):out[name]=a;keep('D0_native_'+name,a);return a
 g,hi,Ga,U,z,P=s['g'],s['hi'],s['Ga'],s['U'],s['z'],s['P']
 dn=put('nu',d['du']+np.einsum('pbal,pl->pab',d['Ga'],U)+np.einsum('pbal,pl->pab',Ga,d['U']))
 dnz=put('nz',d['dz']-np.einsum('plab,jpl->jpab',d['Ga'],z)-np.einsum('plab,jpl->jpab',Ga,d['z']))
 duc=put('uc',np.einsum('pab,pb->pa',d['g'],U)+np.einsum('pab,pb->pa',g,d['U']))
 dP=put('P',np.einsum('pa,pb->pab',duc,U)+np.einsum('pa,pb->pab',s['uc'],d['U']))
 dq=put('q',np.einsum('pa,jpab->jpb',d['U'],s['nz'])+np.einsum('pa,jpab->jpb',U,dnz))
 dV=put('V',np.einsum('pab,jpb->jpa',dP,s['q'])+np.einsum('pab,jpb->jpa',P,dq))
 dD=put('D',np.einsum('pac,jpcd,pbd->jpab',dP,s['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,dnz,P)+np.einsum('pac,jpcd,pbd->jpab',P,s['nz'],dP))
 lowered=np.einsum('pab,pcb->pca',d['g'],s['nu'])+np.einsum('pab,pcb->pca',g,dn)
 dF=put('F',lowered-lowered.swapaxes(1,2))
 put('a',np.einsum('pa,pab->pb',d['U'],s['nu'])+np.einsum('pa,pab->pb',U,dn))
 dz2=put('z2',np.einsum('pac,jpa,jpc->jp',d['hi'],z,z)+2*np.einsum('pac,jpa,jpc->jp',hi,z,d['z']))
 put('f',dz2/((B*GC)**2*s['xi'][:,None]**4))
 dVu=put('V_raised',np.einsum('pab,jpb->jpa',d['hi'],s['V'])+np.einsum('pab,jpb->jpa',hi,dV))
 dDu=put('D_raised',np.einsum('pac,jpcd,pdb->jpab',d['hi'],s['D'],hi)+np.einsum('pac,jpcd,pdb->jpab',hi,dD,hi)+np.einsum('pac,jpcd,pdb->jpab',hi,s['D'],d['hi']))
 dFu=put('Fup',np.einsum('pac,pcd,pdb->pab',d['hi'],s['F'],hi)+np.einsum('pac,pcd,pdb->pab',hi,dF,hi)+np.einsum('pac,pcd,pdb->pab',hi,s['F'],d['hi']))
 Vu=s['V_raised'];w=s['w'];om=s['omega']
 dPi=put('Pi',w[:,None,None,None]*((np.einsum('pa,jpb->jpab',d['U'],Vu)+np.einsum('pa,jpb->jpab',U,dVu))/om[:,None,None,None]**2-ELL**2*dDu))
 dZ=put('Z',np.einsum('j,jpa->pa',w,d['z']))
 put('PiU',-ALPHA*(np.einsum('pac,pcb->pab',d['hi'],s['F'])+np.einsum('pac,pcb->pab',hi,dF))+np.einsum('pa,pb->pab',d['U'],s['Z'])+np.einsum('pa,pb->pab',U,dZ))
 nuc=np.einsum('pab,pcb->pca',g,s['nu'])
 put('mu',np.einsum('jpab,pab->jp',dPi,nuc)+np.einsum('jpab,pab->jp',s['Pi'],lowered))
 sym=(s['Pi']+s['Pi'].swapaxes(2,3))/2;dsym=(dPi+dPi.swapaxes(2,3))/2
 Klo=s['connection_Klo']
 dK=np.einsum('pl,pa,pb->plab',dZ,U,U)+np.einsum('pl,pa,pb->plab',s['Z'],d['U'],U)+np.einsum('pl,pa,pb->plab',s['Z'],U,d['U'])-np.einsum('jpab,jpl->plab',dsym,z)-np.einsum('jpab,jpl->plab',sym,d['z'])
 dKu=put('connection_Kup',np.einsum('plm,pmab->plab',d['hi'],Klo)+np.einsum('plm,pmab->plab',hi,dK))
 dCD=(dKu.transpose(0,2,1,3)+dKu.transpose(0,2,3,1)-dKu)/2
 dCM=-ALPHA*(dFu[:,:,:,None]*U[:,None,None,:]+s['Fup'][:,:,:,None]*d['U'][:,None,None,:]+dFu[:,:,None,:]*U[:,None,:,None]+s['Fup'][:,:,None,:]*d['U'][:,None,:,None])/2
 put('connection_native',dCD);put('connection_Maxwell',dCM);put('connection_momentum',dCD+dCM)
 return out


def derivative_reduced_momenta(s,c,dfeatures,dc,pnative,pmetric_native,keep):
 # Reuse actual current primal momenta in density terms; copied targets are not inputs.
 PiU,Pi=s['PiU'],s['Pi'];dPU,dPi=dfeatures['PiU'],dfeatures['Pi'];dens=c['dens'];dl=dc['log_dens']
 du=np.einsum('pa,pai->pi',dPU[:,0],c['JU'])+np.einsum('pa,pai->pi',PiU[:,0],dc['JU'])+np.einsum('jp,jpi->pi',dPi[:,:,0,0],c['JzU'])+np.einsum('jp,jpi->pi',Pi[:,:,0,0],dc['JzU'])
 dz=dPi[:,:,0,1:]+dPi[:,:,0,0,None]*c['Jzz'][None]+Pi[:,:,0,0,None]*dc['Jzz'][None]
 py=dl[:,None]*pnative+dens[:,None]*np.concatenate((du,dz.transpose(1,0,2).reshape(len(dens),96)),axis=1);keep('D0_native_canonical_density',py)
 CT=s['connection_momentum'][:,0];dCT=dfeatures['connection_momentum'][:,0]
 dm=np.einsum('pmn,pkmn->pk',dCT,c['embed'])+np.einsum('pmn,pkmn->pk',CT,dc['embed'])+np.einsum('pa,pka->pk',dPU[:,0],c['Uh'])+np.einsum('pa,pka->pk',PiU[:,0],dc['Uh'])+np.einsum('jp,jpk->pk',dPi[:,:,0,0],c['zh'])+np.einsum('jp,jpk->pk',Pi[:,:,0,0],dc['zh'])
 pm=dl[:,None]*pmetric_native+dens[:,None]*dm;keep('D0_native_metric_canonical_density',pm)
 return py,pm


def derivative_native_force_features(s,d,df,dphi,keep):
 # Full algebraic A/A_z coefficients require an independently admitted phase
 # gradient direction dphi. This function never infers phi_ddot from stationarity.
 out={}
 def put(name,a):out[name]=a;keep('D0_force_'+name,a);return a
 hi,U,z,w,om=s['hi'],s['U'],s['z'],s['w'],s['omega'];Vu=s['V_raised']
 dr=put('r',np.einsum('pab,pb->pa',df['P'],s['phi'])+np.einsum('pab,pb->pa',s['P'],dphi))
 Q=np.einsum('pa,pa->p',U,s['phi']);dQ=np.einsum('pa,pa->p',d['U'],s['phi'])+np.einsum('pa,pa->p',U,dphi)
 Ur=np.einsum('pa,pa->p',U,s['r']);dUr=np.einsum('pa,pa->p',d['U'],s['r'])+np.einsum('pa,pa->p',U,dr)
 qu=np.einsum('jpa,pa->jp',s['q'],U);dqu=np.einsum('jpa,pa->jp',df['q'],U)+np.einsum('jpa,pa->jp',s['q'],d['U'])
 dAj=(np.einsum('jpn,jprn->jpr',df['V_raised'],s['nz'])+np.einsum('jpn,jprn->jpr',Vu,df['nz'])+dqu[:,:,None]*s['V']+qu[:,:,None]*df['V'])/om[:,None,None]**2
 H=np.einsum('pmc,jpcr->jpmr',hi,s['D']);dH=np.einsum('pmc,jpcr->jpmr',d['hi'],s['D'])+np.einsum('pmc,jpcr->jpmr',hi,df['D'])
 dAj-=ELL**2*(np.einsum('jprn,jpn->jpr',df['D'],Vu)+np.einsum('jprn,jpn->jpr',s['D'],df['V_raised'])+np.einsum('jpmr,jpmn,pn->jpr',dH,s['nz'],U)+np.einsum('jpmr,jpmn,pn->jpr',H,df['nz'],U)+np.einsum('jpmr,jpmn,pn->jpr',H,s['nz'],d['U']))
 put('A',-(dQ[:,None]*s['r']+Q[:,None]*dr+dUr[:,None]*s['phi']+Ur[:,None]*dphi)+np.einsum('pn,prn->pr',df['Z'],s['nu'])+np.einsum('pn,prn->pr',s['Z'],df['nu'])+np.einsum('j,jpr->pr',w,dAj))
 zu=np.einsum('pab,jpb->jpa',hi,z);dzu=np.einsum('pab,jpb->jpa',d['hi'],z)+np.einsum('pab,jpb->jpa',hi,d['z'])
 put('A_z_raw',w[:,None,None]*(df['a'][None]-df['f'][:,:,None]*zu-s['f'][:,:,None]*dzu))
 return out


def derivative_EH_momentum(c,k,n,Lie_dot,keep):
 # Lie_dot=Lie_b h+Lie_beta k, with actual spatial rate and gauge-gradient jets.
 ih,N,K,Kt=c['ih'],c['N'],c['K'],c['Ktrace'];root=c['sqrt_h']
 dih=-np.einsum('pij,pjk,pkl->pil',ih,k,ih);dK=-Lie_dot/(2*N[:,None,None])-(n/N)[:,None,None]*K
 dKt=np.einsum('pij,pij->p',dih,K)+np.einsum('pij,pij->p',ih,dK)
 dKup=np.einsum('pij,pjk,pkl->pil',dih,K,ih)+np.einsum('pij,pjk,pkl->pil',ih,dK,ih)+np.einsum('pij,pjk,pkl->pil',ih,K,dih)
 dratio=np.einsum('pij,pij->p',ih,k)/2
 dp=dratio[:,None,None]*c['pi_EH']+root[:,None,None]/(2*C)*(dKup-dKt[:,None,None]*ih-Kt[:,None,None]*dih)
 keep('D0_EH_metric_tensor_density',dp)
 six=np.column_stack((dp[:,0,0],dp[:,1,1],dp[:,2,2],2*dp[:,0,1],2*dp[:,0,2],2*dp[:,1,2]));keep('D0_EH_metric_coordinate_density',six)
 return six



def momentum_derivative_terms(s,c,df,dc,pnative,pmetric_native,label):
 # Exact signed products expose the reduced derivative, not a second field call.
 p=len(c['N']);ds=c['dens'];PU,Pi=s['PiU'],s['Pi'];dPU,dPi=df['PiU'],df['Pi'];dl=dc['log_dens']
 nt=np.zeros((p,99,5));mt=np.zeros((p,6,7))
 nt[:,:,0]=dl[:,None]*pnative
 nt[:,:3,1]=ds[:,None]*np.einsum('pa,pai->pi',dPU[:,0],c['JU'])
 nt[:,:3,2]=ds[:,None]*np.einsum('pa,pai->pi',PU[:,0],dc['JU'])
 nt[:,:3,3]=ds[:,None]*np.einsum('jp,jpi->pi',dPi[:,:,0,0],c['JzU'])
 nt[:,:3,4]=ds[:,None]*np.einsum('jp,jpi->pi',Pi[:,:,0,0],dc['JzU'])
 nt[:,3:,1]=ds[:,None]*dPi[:,:,0,1:].transpose(1,0,2).reshape(p,96)
 nt[:,3:,2]=ds[:,None]*(dPi[:,:,0,0,None]*c['Jzz'][None]).transpose(1,0,2).reshape(p,96)
 nt[:,3:,3]=ds[:,None]*(Pi[:,:,0,0,None]*dc['Jzz'][None]).transpose(1,0,2).reshape(p,96)
 mt[:,:,0]=dl[:,None]*pmetric_native
 CT=s['connection_momentum'][:,0];dCT=df['connection_momentum'][:,0]
 mt[:,:,1]=ds[:,None]*np.einsum('pmn,pkmn->pk',dCT,c['embed'])
 mt[:,:,2]=ds[:,None]*np.einsum('pmn,pkmn->pk',CT,dc['embed'])
 mt[:,:,3]=ds[:,None]*np.einsum('pa,pka->pk',dPU[:,0],c['Uh'])
 mt[:,:,4]=ds[:,None]*np.einsum('pa,pka->pk',PU[:,0],dc['Uh'])
 mt[:,:,5]=ds[:,None]*np.einsum('jp,jpk->pk',dPi[:,:,0,0],c['zh'])
 mt[:,:,6]=ds[:,None]*np.einsum('jp,jpk->pk',Pi[:,:,0,0],dc['zh'])
 capture(label+'_native_signed_terms',nt);capture(label+'_metric_native_signed_terms',mt)
 return nt,mt


def Lie_metric_rate(c,cj,k,k_spatial,b,b_spatial,label):
 # Coordinate Lie_b h + Lie_beta k; spatial axis is R,Z,phi.
 h,be=c['h'],c['beta'];dh=cj['dh'][:,1:];db=cj['dbeta'][:,1:]
 terms=np.stack((np.einsum('pa,paij->pij',b,dh),np.einsum('paj,pia->pij',h,b_spatial),np.einsum('pia,pja->pij',h,b_spatial),np.einsum('pa,paij->pij',be,k_spatial),np.einsum('paj,pia->pij',k,db),np.einsum('pia,pja->pij',k,db)),axis=-1)
 capture(label+'_Lie_rate_signed_terms',terms)
 val=terms.sum(axis=-1);capture(label+'_Lie_rate',val)
 return val


def derivative_at_seed(s,c,cj,v,k,v_spatial,k_spatial,n,b,n_spatial,b_spatial,n_second,b_second,label):
 # Local algebraic directional derivative only; no acceleration is imposed.
 def keep(name,a):
  RAW[label+'_'+name]=a.copy();assert a.dtype.kind=='f' and np.all(np.isfinite(a)),name
 p=len(c['N']);assert v.shape==(p,99) and k.shape==(p,3,3) and v_spatial.shape==(p,3,99) and k_spatial.shape==(p,3,3,3)
 assert n.shape==n_second.shape==(p,) and b.shape==b_second.shape==(p,3) and n_spatial.shape==(p,3) and b_spatial.shape==(p,3,3)
 d=primitive_time_direction(s,c,cj,v,k,v_spatial,k_spatial,n,b,n_spatial,b_spatial,n_second,b_second,keep)
 dc=derivative_chart(s,c,d,k,n,b,keep);df=derivative_native_momentum_features(s,d,keep)
 py,pm=derivative_reduced_momenta(s,c,df,dc,c['p_native'],c['p_metric_native'],keep)
 lie=Lie_metric_rate(c,cj,k,k_spatial,b,b_spatial,label);pe=derivative_EH_momentum(c,k,n,lie,keep)
 pt=pm+pe;keep('D0_total_metric_coordinate_density',pt)
 nt,mt=momentum_derivative_terms(s,c,df,dc,c['p_native'],c['p_metric_native'],label)
 return dict(native=py,metric_native=pm,metric_EH=pe,metric_total=pt,primitive=d,chart=dc,features=df,native_terms=nt,metric_native_terms=mt)


def primary_derivative_at_seed(s,c,delta_n,delta_b,label):
 # Delta of the canonical momentum under a gauge-velocity-only direction.
 def keep(name,a):
  RAW[label+'_'+name]=a.copy();assert a.dtype.kind=='f' and np.all(np.isfinite(a)),name
 d=gauge_velocity_primary_direction(s,c,delta_n,delta_b,keep)
 dc=derivative_chart(s,c,d,np.zeros_like(c['h']),np.zeros_like(c['N']),np.zeros_like(c['beta']),keep)
 df=derivative_native_momentum_features(s,d,keep)
 py,pm=derivative_reduced_momenta(s,c,df,dc,c['p_native'],c['p_metric_native'],keep)
 nt,mt=momentum_derivative_terms(s,c,df,dc,c['p_native'],c['p_metric_native'],label)
 return dict(native=py,metric_native=pm,metric_EH=np.zeros_like(pm),metric_total=pm,primitive=d,chart=dc,features=df,native_terms=nt,metric_native_terms=mt)


def scalar_phase_weak_flux(Jdens,geo,independent=False):
 # Scalar axis-even Q1 tests. Boundary flux is separate and remains unknown.
 assert Jdens.shape==(15136,4);out=np.zeros((87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);weight=geo['dv'][iq]/geo['R'][iq]
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hats=geo['hats'][iq,a].reshape(3,3784)
   value=(hats[1]*Jdens[sl,1]+hats[2]*Jdens[sl,2])*weight
   if independent:np.add.at(out,(geo['cell_i']+di,geo['cell_j']+dj),value)
   else:out[di:86+di,dj:44+dj]+=value.reshape(86,44)
 out[1]+=out[0];out[0]=0
 return out


# Retained exact primal/chart definitions for fresh synthetic derivative controls only.
# Actual physical columns will use saved force seeds, with no primal replay.
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

def metric_partial(s):
 # Metric compatibility recovers the same exact first metric jet, no second derivatives.
 a=np.einsum('plam,pln->pamn',s['Ga'],s['g'])
 return a+np.swapaxes(a,2,3)

def connection_momentum(s,Pi=None,Fup=None):
 Pi=s['Pi'] if Pi is None else Pi;Fup=s['Fup'] if Fup is None else Fup
 Z=s['Z'];U=s['U'];z=s['z'];hi=s['hi']
 sym=(Pi+np.swapaxes(Pi,2,3))/2
 Klo=np.einsum('pl,pa,pb->plab',Z,U,U)-np.einsum('jpab,jpl->plab',sym,z)
 Kup=np.einsum('plm,pmab->plab',hi,Klo)
 D=(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)-Kup)/2
 mx=-ALPHA*(Fup[:,:,:,None]*U[:,None,None,:]+Fup[:,:,None,:]*U[:,None,:,None])/2
 return D+mx,D,mx

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

def reduced_momenta(s,c,PiU=None,Pi=None,Ctime=None):
 PiU=s['PiU'] if PiU is None else PiU;Pi=s['Pi'] if Pi is None else Pi
 if Ctime is None:Ctime=connection_momentum(s)[0][:,0]
 pu=np.einsum('pa,pai->pi',PiU[:,0],c['JU'])+np.einsum('jp,jpi->pi',Pi[:,:,0,0],c['JzU'])
 pz=Pi[:,:,0,1:]+Pi[:,:,0,0,None]*c['Jzz'][None,:,:]
 py=c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)
 pmetric=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',Ctime,c['embed'])+np.einsum('pa,pka->pk',PiU[:,0],c['Uh'])+np.einsum('jp,jpk->pk',Pi[:,:,0,0],c['zh']))
 return py,pmetric

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

def connection_from_jet(hi,dg):
 p=len(hi);out=np.zeros((p,4,4,4))
 for a in range(4):
  for b in range(4):out[:,:,a,b]=np.einsum('plm,pm->pl',hi,dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b])/2
 return out


def phase_charge_temporal_coefficients(s,c,v,k,PX,PXX,X,label):
 # Exact current phi_i=0 chart. Return coefficients, never select phi_tt or gauge.
 # dot(p_phi) = mechanical + n_coefficient*Ndot + acceleration_coefficient*phi_tt.
 # Spatial conservation is supplied separately by the saved full J weak flux.
 p=len(c['N']);assert s['phi'].shape==(p,4) and np.all(s['phi'][:,1:]==0)
 assert v.shape==(p,99) and k.shape==(p,3,3) and PX.shape==PXX.shape==X.shape==(p,)
 out={}
 def put(name,value):
  out[name]=value;capture(label+'_'+name,value)
  assert value.dtype.kind=='f' and np.all(np.isfinite(value)),name
  return value
 N,root,u,up,ih=c['N'],c['sqrt_h'],c['u'],c['up'],c['ih']
 relative_tilt=put('relative_tilt_squared',np.einsum('pi,pi->p',u,up))
 theta=put('coordinate_volume_rate',np.einsum('pij,pij->p',ih,k)/2)
 tilt_terms=put('tilt_rate_terms',np.column_stack((2*np.einsum('pi,pi->p',up,v[:,:3]),-np.einsum('pi,pij,pj->p',up,k,up))))
 tilt_rate=put('tilt_rate',tilt_terms.sum(axis=1))
 slope=put('exact_charge_clock_slope',PXX-relative_tilt)
 assert np.all(N>0) and np.all(root>0) and np.all(X>0) and np.all(relative_tilt>=0) and np.all(slope>0)
 terms=put('mechanical_charge_rate_terms',root[:,None]*np.column_stack((theta*PX,-theta*X*relative_tilt,-X*tilt_rate)))
 put('mechanical_charge_rate',terms.sum(axis=1))
 put('lapse_velocity_coefficient',-root*slope*X/N)
 put('phase_acceleration_coefficient',root*slope/N)
 put('registered_charge_density',root*(PX-X*relative_tilt))
 put('mechanical_charge_rate_envelope',root*(abs(theta*PX)+abs(theta*X*relative_tilt)+abs(X)*(2*np.einsum('pi,pi->p',abs(up),abs(v[:,:3]))+np.einsum('pi,pij,pj->p',abs(up),abs(k),abs(up)))))
 return out


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


def primitive_time_direction_operation_envelopes(s,c,cj,v,k,v_spatial,k_spatial,n,b,n_spatial,b_spatial,n_second,b_second,label):
 out={};pr={}
 def put(name,a):
  out[name]=a;capture(label+'_primitive_operation_'+name,a)
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0),name
  return a
 def primal(name,a):
  pr[name]=a;capture(label+'_primal_operation_'+name,a)
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0),name
  return a
 p=len(c['N']);N,ga=c['N'],c['gamma'];ih,h,be=abs(c['ih']),abs(c['h']),abs(c['beta']);U,z=abs(s['U']),abs(s['z']);du,dz=abs(s['du']),abs(s['dz'])
 vv,kk=abs(v),abs(k);vu=vv[:,:3];vz=vv[:,3:].reshape(p,32,3).transpose(1,0,2)
 va=np.zeros((p,4,99));va[:,1:]=abs(v_spatial);vua=va[:,:,:3];vza=va[:,:,3:].reshape(p,4,32,3).transpose(2,0,1,3)
 ha=np.zeros((p,4,3,3));ha[:,1:]=abs(k_spatial);na=np.empty((p,4));na[:,0]=abs(n_second);na[:,1:]=abs(n_spatial);ba=np.empty((p,4,3));ba[:,0]=abs(b_second);ba[:,1:]=abs(b_spatial);nn,bb=abs(n),abs(b)
 prod=np.einsum('plam,pln->pamn',abs(s['Ga']),abs(s['g']));edg=primal('dg',prod+prod.swapaxes(2,3))
 edhi=primal('dhi',np.einsum('pij,pajk,pkl->pail',abs(s['hi']),edg,abs(s['hi'])))
 edN=primal('dN',N[:,None]**3*edhi[:,:,0,0]/2)
 edbe=primal('dbeta',2*N[:,None,None]*edN[:,:,None]*abs(s['hi'])[:,None,0,1:]+N[:,None,None]**2*edhi[:,:,0,1:])
 edh=primal('dh',edg[:,:,1:,1:]);edih=primal('dih',np.einsum('pij,pajk,pkl->pail',ih,edh,ih))
 eu=primal('u',np.einsum('pia,pa->pi',abs(s['g'])[:,1:,:],U));eup=primal('up',np.einsum('pij,pj->pi',ih,eu))
 educ=primal('du_cov',np.einsum('paij,pj->pai',edg[:,:,1:,:],U)+np.einsum('pij,paj->pai',abs(s['g'])[:,1:,:],du))
 edup=primal('dup',np.einsum('paij,pj->pai',edih,eu)+np.einsum('pij,paj->pai',ih,educ))
 edga=primal('dgamma',(np.einsum('pi,pai->pa',eup,educ)+np.einsum('pi,paij,pj->pa',eu,edih,eu)/2)/ga[:,None])
 dih=put('spatial_inverse',np.einsum('pij,pjk,pkl->pil',ih,kk,ih))
 diha=put('spatial_inverse_firstjet',np.einsum('pij,pajk,pkl->pail',dih,edh,ih)+np.einsum('pij,pajk,pkl->pail',ih,ha,ih)+np.einsum('pij,pajk,pkl->pail',ih,edh,dih))
 dup=put('up',np.einsum('pij,pj->pi',dih,eu)+np.einsum('pij,pj->pi',ih,vu))
 dupa=put('up_firstjet',np.einsum('paij,pj->pai',diha,eu)+np.einsum('paij,pj->pai',edih,vu)+np.einsum('pij,paj->pai',dih,educ)+np.einsum('pij,paj->pai',ih,vua))
 dga=put('gamma',(np.einsum('pi,pi->p',eup,vu)+np.einsum('pi,pij,pj->p',eu,dih,eu)/2)/ga)
 dgaa=put('gamma_firstjet',(np.einsum('pi,pai->pa',dup,educ)+np.einsum('pi,pai->pa',eup,vua)+np.einsum('pi,paij,pj->pa',vu,edih,eu)+np.einsum('pi,paij,pj->pa',eu,diha,eu)/2)/ga[:,None]+edga*dga[:,None]/ga[:,None])
 dU=np.empty_like(s['U']);dU[:,0]=dga/N+ga*nn/N**2;dU[:,1:]=dup+bb*U[:,0,None]+be*dU[:,0,None];put('U',dU)
 ddu=np.empty_like(s['du']);ddu[:,:,0]=dgaa/N[:,None]+edga*nn[:,None]/N[:,None]**2+dga[:,None]*edN/N[:,None]**2+ga[:,None]*na/N[:,None]**2+2*ga[:,None]*edN*nn[:,None]/N[:,None]**3
 ddu[:,:,1:]=dupa+ba*U[:,None,0,None]+edbe*dU[:,None,0,None]+bb[:,None,:]*du[:,:,0,None]+be[:,None,:]*ddu[:,:,0,None];put('du',ddu)
 zs,zsa=z[:,:,1:],dz[:,:,:,1:];t=np.einsum('pi,jpi->jp',U[:,1:],zs)
 ta=np.einsum('pai,jpi->jpa',du[:,:,1:],zs)+np.einsum('pi,jpai->jpa',U[:,1:],zsa)
 dt=np.einsum('pi,jpi->jp',dU[:,1:],zs)+np.einsum('pi,jpi->jp',U[:,1:],vz)
 dta=np.einsum('pai,jpi->jpa',ddu[:,:,1:],zs)+np.einsum('pai,jpi->jpa',du[:,:,1:],vz)+np.einsum('pi,jpai->jpa',dU[:,1:],zsa)+np.einsum('pi,jpai->jpa',U[:,1:],vza)
 ddz=np.empty_like(s['dz']);ddz[:,:,:,1:]=vza;U0=U[:,0];U0a=du[:,:,0]
 ez=np.empty_like(s['z']);ez[:,:,1:]=vz;ez[:,:,0]=dt/U0[None]+t*dU[None,:,0]/U0[None]**2;put('z',ez)
 ddz[:,:,:,0]=dta/U0[None,:,None]+ta*dU[None,:,None,0]/U0[None,:,None]**2+dt[:,:,None]*U0a[None]/U0[None,:,None]**2+t[:,:,None]*ddu[None,:,:,0]/U0[None,:,None]**2+2*t[:,:,None]*U0a[None]*dU[None,:,None,0]/U0[None,:,None]**3;put('dz',ddz)
 dg=np.empty_like(s['g']);dg[:,1:,1:]=kk;dg[:,0,1:]=np.einsum('pij,pj->pi',kk,be)+np.einsum('pij,pj->pi',h,bb);dg[:,1:,0]=dg[:,0,1:]
 dg[:,0,0]=2*N*nn+np.einsum('pi,pij,pj->p',be,kk,be)+2*np.einsum('pi,pij,pj->p',be,h,bb);put('g',dg)
 ddg=np.empty_like(cj['dg']);ddg[:,:,1:,1:]=ha;ddg[:,:,0,1:]=np.einsum('paij,pj->pai',ha,be)+np.einsum('paij,pj->pai',edh,bb)+np.einsum('pij,paj->pai',kk,edbe)+np.einsum('pij,paj->pai',h,ba);ddg[:,:,1:,0]=ddg[:,:,0,1:]
 ddg[:,:,0,0]=2*(edN*nn[:,None]+N[:,None]*na)+2*np.einsum('pai,pij,pj->pa',edbe,kk,be)+np.einsum('pi,paij,pj->pa',be,ha,be)+2*np.einsum('pai,pij,pj->pa',edbe,h,bb)+2*np.einsum('pi,paij,pj->pa',be,edh,bb)+2*np.einsum('pi,pij,paj->pa',be,h,ba);put('dg_partial',ddg)
 dhi=put('hi',np.einsum('pij,pjk,pkl->pil',abs(s['hi']),dg,abs(s['hi'])))
 dGa=np.empty_like(s['Ga'])
 for a in range(4):
  for bb0 in range(4):
   jet=edg[:,a,bb0,:]+edg[:,bb0,a,:]+edg[:,:,a,bb0];djet=ddg[:,a,bb0,:]+ddg[:,bb0,a,:]+ddg[:,:,a,bb0]
   dGa[:,:,a,bb0]=(np.einsum('plm,pm->pl',dhi,jet)+np.einsum('plm,pm->pl',abs(s['hi']),djet))/2
 put('Ga',dGa)
 return out,pr

def derivative_chart_operation_envelopes(s,c,ed,pr,k,n,b,label):
 out={}
 def put(name,a):
  out[name]=a;capture(label+'_chart_operation_'+name,a)
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0),name
  return a
 N,ga=c['N'],c['gamma'];ih,be=abs(c['ih']),abs(c['beta']);eu,eup=pr['u'],pr['up'];U,z=abs(s['U']),abs(s['z']);kk,nn,bb=abs(k),abs(n),abs(b)
 E=abs(c['embed'][:,:,1:,1:]);dih=put('ih',np.einsum('pij,pjk,pkl->pil',ih,kk,ih))
 educ=np.einsum('pia,pa->pi',ed['g'][:,1:,:],U)+np.einsum('pia,pa->pi',abs(s['g'])[:,1:,:],ed['U'])
 dup=put('up',np.einsum('pij,pj->pi',dih,eu)+np.einsum('pij,pj->pi',ih,educ))
 dga=put('gamma',(np.einsum('pi,pi->p',eup,educ)+np.einsum('pi,pij,pj->p',eu,dih,eu)/2)/ga)
 JU=np.empty_like(c['JU']);JU[:,0]=eup/(N*ga)[:,None];JU[:,1:]=ih+be[:,:,None]*JU[:,None,0];put('primal_JU',JU)
 Jzz=put('primal_Jzz',(eup+be*(ga/N)[:,None])/U[:,0,None])
 JzU=put('primal_JzU',np.einsum('jpa,pai->jpi',z,JU)/U[None,:,0,None])
 Uh=np.empty_like(c['Uh']);Uh[:,:,0]=np.einsum('pi,pkij,pj->pk',eup,E,eup)/(2*N*ga)[:,None];Uh[:,:,1:]=np.einsum('pij,pkjl,pl->pki',ih,E,eup)+be[:,None,:]*Uh[:,:,0,None];put('primal_Uh',Uh)
 zh=put('primal_zh',np.einsum('jpa,pka->jpk',z,Uh)/U[None,:,0,None])
 dJU=np.empty_like(c['JU']);dJU[:,0]=dup/(N*ga)[:,None]+JU[:,0]*(nn/N+dga/ga)[:,None];dJU[:,1:]=dih+bb[:,:,None]*JU[:,None,0]+be[:,:,None]*dJU[:,None,0];put('JU',dJU)
 put('Jzz',ed['U'][:,1:]/U[:,0,None]+U[:,1:]*ed['U'][:,0,None]/U[:,0,None]**2)
 put('JzU',(np.einsum('jpa,pai->jpi',ed['z'],JU)+np.einsum('jpa,pai->jpi',z,dJU))/U[None,:,0,None]+np.einsum('jpa,pai->jpi',z,JU)*ed['U'][None,:,0,None]/U[None,:,0,None]**2)
 de=np.zeros_like(c['embed']);de[:,:,0,1:]=np.einsum('pkij,pj->pki',E,bb);de[:,:,1:,0]=de[:,:,0,1:];de[:,:,0,0]=2*np.einsum('pi,pkij,pj->pk',be,E,bb);put('embed',de)
 dt=2*np.einsum('pi,pkij,pj->pk',dup,E,eup);dUh=np.empty_like(c['Uh']);dUh[:,:,0]=dt/(2*N*ga)[:,None]+Uh[:,:,0]*(nn/N+dga/ga)[:,None]
 dUh[:,:,1:]=np.einsum('pij,pkjl,pl->pki',dih,E,eup)+np.einsum('pij,pkjl,pl->pki',ih,E,dup)+bb[:,None,:]*Uh[:,:,0,None]+be[:,None,:]*dUh[:,:,0,None];put('Uh',dUh)
 put('zh',(np.einsum('jpa,pka->jpk',ed['z'],Uh)+np.einsum('jpa,pka->jpk',z,dUh))/U[None,:,0,None]+np.einsum('jpa,pka->jpk',z,Uh)*ed['U'][None,:,0,None]/U[None,:,0,None]**2)
 dl=put('log_dens',nn/N+np.einsum('pij,pij->p',ih,kk)/2);put('dens',abs(c['dens'])*dl);put('sqrt_h',abs(c['sqrt_h'])*np.einsum('pij,pij->p',ih,kk)/2)
 return out


def derivative_operation_envelopes(s,c,d,dc,df,label,env):
 out={};ed=env['primitive'];ec=env['chart'];p=len(s['U'])
 def put(name,a):
  out[name]=a;capture(label+'_operation_'+name,a)
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0),name
  return a
 for k in ('g','hi','Ga','U','du','z','dz'):
  assert ed[k].shape==d[k].shape;put('input_d_'+k,ed[k])
 for k in ('JU','JzU','Jzz','Uh','zh','embed','log_dens'):
  assert ec[k].shape==dc[k].shape;put('input_chart_'+k,ec[k])
 primal_density,ep=native_momentum_operation_envelopes(s,c,label+'_D0_primal')
 g,hi,U,z=abs(s['g']),abs(s['hi']),abs(s['U']),abs(s['z']);w,om=abs(s['w']),abs(s['omega'])
 assert np.all(om>0) and np.all(c['N']>0) and np.all(c['gamma']>0) and np.all(U[:,0]>0)
 Vu=put('primal_V_raised',np.einsum('pab,jpb->jpa',hi,ep['V']))
 Fu=put('primal_Fup',np.einsum('pac,pcd,pdb->pab',hi,ep['F'],hi))
 sym=(ep['Pi']+ep['Pi'].swapaxes(2,3))/2
 Klo=put('primal_connection_Klo',np.einsum('pl,pa,pb->plab',ep['Z'],U,U)+np.einsum('jpab,jpl->plab',sym,z))
 Ku=np.einsum('plm,pmab->plab',hi,Klo)
 CD=put('primal_connection_native',(Ku.transpose(0,2,1,3)+Ku.transpose(0,2,3,1)+Ku)/2)
 CM=put('primal_connection_Maxwell',abs(ALPHA)*(Fu[:,:,:,None]*U[:,None,None,:]+Fu[:,:,None,:]*U[:,None,:,None])/2)
 CC=put('primal_connection_momentum',CD+CM)
 E=abs(c['embed'][:,:,1:,1:]);N=abs(c['N']);ga=abs(c['gamma']);be=abs(c['beta']);ih=abs(c['ih'])
 Uh=np.empty_like(c['Uh']);Uh[:,:,0]=np.einsum('pi,pkij,pj->pk',ep['up'],E,ep['up'])/(2*N*ga)[:,None]
 Uh[:,:,1:]=np.einsum('pij,pkjl,pl->pki',ih,E,ep['up'])+be[:,None,:]*Uh[:,:,0,None];put('primal_Uh',Uh)
 zh=put('primal_zh',np.einsum('jpa,pka->jpk',z,Uh)/U[None,:,0,None])
 embed=np.zeros_like(c['embed']);embed[:,:,1:,1:]=E;embed[:,:,0,1:]=np.einsum('pkij,pj->pki',E,be);embed[:,:,1:,0]=embed[:,:,0,1:];embed[:,:,0,0]=np.einsum('pi,pkij,pj->pk',be,E,be);put('primal_embed',embed)
 pn=put('primal_native_density',primal_density)
 pm=put('primal_native_metric_density',abs(c['dens'])[:,None]*(np.einsum('pmn,pkmn->pk',CC[:,0],embed)+np.einsum('pa,pka->pk',ep['PiU'][:,0],Uh)+np.einsum('jp,jpk->pk',ep['Pi'][:,:,0,0],zh)))
 dn=put('d_nu',ed['du']+np.einsum('pbal,pl->pab',ed['Ga'],U)+np.einsum('pbal,pl->pab',abs(s['Ga']),ed['U']))
 dnz=put('d_nz',ed['dz']+np.einsum('plab,jpl->jpab',ed['Ga'],z)+np.einsum('plab,jpl->jpab',abs(s['Ga']),ed['z']))
 duc=put('d_uc',np.einsum('pab,pb->pa',ed['g'],U)+np.einsum('pab,pb->pa',g,ed['U']))
 dp=put('d_P',np.einsum('pa,pb->pab',duc,U)+np.einsum('pa,pb->pab',ep['U_cov'],ed['U']))
 dq=put('d_q',np.einsum('pa,jpab->jpb',ed['U'],ep['nz'])+np.einsum('pa,jpab->jpb',U,dnz))
 dv=put('d_V',np.einsum('pab,jpb->jpa',dp,ep['q'])+np.einsum('pab,jpb->jpa',ep['P'],dq))
 dd=put('d_D',np.einsum('pac,jpcd,pbd->jpab',dp,ep['nz'],ep['P'])+np.einsum('pac,jpcd,pbd->jpab',ep['P'],dnz,ep['P'])+np.einsum('pac,jpcd,pbd->jpab',ep['P'],ep['nz'],dp))
 low=np.einsum('pab,pcb->pca',ed['g'],ep['nu'])+np.einsum('pab,pcb->pca',g,dn)
 dF=put('d_F',low+low.swapaxes(1,2))
 dVu=put('d_V_raised',np.einsum('pab,jpb->jpa',ed['hi'],ep['V'])+np.einsum('pab,jpb->jpa',hi,dv))
 dDu=put('d_D_raised',np.einsum('pac,jpcd,pdb->jpab',ed['hi'],ep['D'],hi)+np.einsum('pac,jpcd,pdb->jpab',hi,dd,hi)+np.einsum('pac,jpcd,pdb->jpab',hi,ep['D'],ed['hi']))
 dFu=put('d_Fup',np.einsum('pac,pcd,pdb->pab',ed['hi'],ep['F'],hi)+np.einsum('pac,pcd,pdb->pab',hi,dF,hi)+np.einsum('pac,pcd,pdb->pab',hi,ep['F'],ed['hi']))
 dPi=put('d_Pi',w[:,None,None,None]*((np.einsum('pa,jpb->jpab',ed['U'],Vu)+np.einsum('pa,jpb->jpab',U,dVu))/om[:,None,None,None]**2+ELL**2*dDu))
 dZ=put('d_Z',np.einsum('j,jpa->pa',w,ed['z']))
 dPU=put('d_PiU',abs(ALPHA)*(np.einsum('pac,pcb->pab',ed['hi'],ep['F'])+np.einsum('pac,pcb->pab',hi,dF))+np.einsum('pa,pb->pab',ed['U'],ep['Z'])+np.einsum('pa,pb->pab',U,dZ))
 dsym=(dPi+dPi.swapaxes(2,3))/2
 dK=put('d_connection_Klo',np.einsum('pl,pa,pb->plab',dZ,U,U)+np.einsum('pl,pa,pb->plab',ep['Z'],ed['U'],U)+np.einsum('pl,pa,pb->plab',ep['Z'],U,ed['U'])+np.einsum('jpab,jpl->plab',dsym,z)+np.einsum('jpab,jpl->plab',sym,ed['z']))
 dKu=put('d_connection_Kup',np.einsum('plm,pmab->plab',ed['hi'],Klo)+np.einsum('plm,pmab->plab',hi,dK))
 dCD=put('d_connection_native',(dKu.transpose(0,2,1,3)+dKu.transpose(0,2,3,1)+dKu)/2)
 dCM=put('d_connection_Maxwell',abs(ALPHA)*(dFu[:,:,:,None]*U[:,None,None,:]+Fu[:,:,:,None]*ed['U'][:,None,None,:]+dFu[:,:,None,:]*U[:,None,:,None]+Fu[:,:,None,:]*ed['U'][:,None,:,None])/2)
 dCC=put('d_connection_momentum',dCD+dCM)
 eu=np.einsum('pa,pai->pi',dPU[:,0],ep['JU'])+np.einsum('pa,pai->pi',ep['PiU'][:,0],ec['JU'])+np.einsum('jp,jpi->pi',dPi[:,:,0,0],ep['JzU'])+np.einsum('jp,jpi->pi',ep['Pi'][:,:,0,0],ec['JzU'])
 ez=dPi[:,:,0,1:]+dPi[:,:,0,0,None]*ep['Jzz'][None]+ep['Pi'][:,:,0,0,None]*ec['Jzz'][None]
 en=put('D0_native_density',ec['log_dens'][:,None]*pn+abs(c['dens'])[:,None]*np.concatenate((eu,ez.transpose(1,0,2).reshape(p,96)),axis=1))
 em=np.einsum('pmn,pkmn->pk',dCC[:,0],embed)+np.einsum('pmn,pkmn->pk',CC[:,0],ec['embed'])+np.einsum('pa,pka->pk',dPU[:,0],Uh)+np.einsum('pa,pka->pk',ep['PiU'][:,0],ec['Uh'])+np.einsum('jp,jpk->pk',dPi[:,:,0,0],zh)+np.einsum('jp,jpk->pk',ep['Pi'][:,:,0,0],ec['zh'])
 em=put('D0_native_metric_density',ec['log_dens'][:,None]*pm+abs(c['dens'])[:,None]*em)
 return en,em,out


def derivative_EH_momentum_operation_envelope(c,pr,k,k_spatial,n,b,b_spatial,label):
 out={}
 def put(name,a):
  out[name]=a;capture(label+'_EH_operation_'+name,a)
  assert a.dtype.kind=='f' and np.all(np.isfinite(a)) and np.all(a>=0),name
  return a
 N,root=c['N'],abs(c['sqrt_h']);ih,h,K,be=abs(c['ih']),abs(c['h']),abs(c['K']),abs(c['beta']);kk,nn,bb=abs(k),abs(n),abs(b)
 edih=put('spatial_inverse',np.einsum('pij,pjk,pkl->pil',ih,kk,ih))
 kt=put('primal_trace',np.einsum('pij,pij->p',ih,K))
 kup=put('primal_raised_K',np.einsum('pij,pjk,pkl->pil',ih,K,ih))
 pe=put('primal_momentum',root[:,None,None]*(kup+kt[:,None,None]*ih)/(2*C))
 dh,db=pr['dh'][:,1:],pr['dbeta'][:,1:]
 lt=put('Lie_rate_terms',np.stack((np.einsum('pa,paij->pij',bb,dh),np.einsum('paj,pia->pij',h,abs(b_spatial)),np.einsum('pia,pja->pij',h,abs(b_spatial)),np.einsum('pa,paij->pij',be,abs(k_spatial)),np.einsum('paj,pia->pij',kk,db),np.einsum('pia,pja->pij',kk,db)),axis=-1))
 lie=put('Lie_rate',lt.sum(axis=-1))
 dk=put('K',lie/(2*N[:,None,None])+(nn/N)[:,None,None]*K)
 dkt=put('trace',np.einsum('pij,pij->p',edih,K)+np.einsum('pij,pij->p',ih,dk))
 dkup=put('raised_K',np.einsum('pij,pjk,pkl->pil',edih,K,ih)+np.einsum('pij,pjk,pkl->pil',ih,dk,ih)+np.einsum('pij,pjk,pkl->pil',ih,K,edih))
 theta=put('measure_rate',np.einsum('pij,pij->p',ih,kk)/2)
 dp=put('momentum',theta[:,None,None]*pe+root[:,None,None]/(2*C)*(dkup+dkt[:,None,None]*ih+kt[:,None,None]*edih))
 six=put('coordinate_density',np.column_stack((dp[:,0,0],dp[:,1,1],dp[:,2,2],2*dp[:,0,1],2*dp[:,0,2],2*dp[:,1,2])))
 return six,out


def fresh_d0_fixture_state(g,dg,U,du,z,dz,phi,xi,w,omega,label):
 p=len(U);assert xi.shape==w.shape==omega.shape==(32,)
 assert g.shape==(p,4,4) and dg.shape==(p,4,4,4)
 assert z.shape==(32,p,4) and dz.shape==(32,p,4,4)
 for name,a in dict(g=g,dg=dg,U=U,du=du,z=z,dz=dz,phi=phi,xi=xi,w=w,omega=omega).items():capture(label+'_seed_'+name,a)
 hi=np.linalg.inv(g);capture(label+'_seed_hi',hi)
 Ga=connection_from_jet(hi,dg);capture(label+'_seed_Ga',Ga)
 s=features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w)
 for name,a in s.items():
  if isinstance(a,np.ndarray):capture(label+'_primal_'+name,a)
 sym=(s['Pi']+s['Pi'].swapaxes(2,3))/2
 s['connection_Klo']=np.einsum('pl,pa,pb->plab',s['Z'],U,U)-np.einsum('jpab,jpl->plab',sym,z)
 capture(label+'_primal_connection_Klo',s['connection_Klo'])
 s['connection_momentum'],cn,cm=connection_momentum(s)
 for name,a in (('connection_momentum',s['connection_momentum']),('connection_native',cn),('connection_Maxwell',cm)):capture(label+'_primal_'+name,a)
 s['V_raised']=raise_cov(hi,s['V']);capture(label+'_primal_V_raised',s['V_raised'])
 c=adm_chart(s)
 for name,a in c.items():capture(label+'_chart_'+name,a)
 c['p_native'],c['p_metric_native']=reduced_momenta(s,c)
 capture(label+'_primal_p_native',c['p_native']);capture(label+'_primal_p_metric_native',c['p_metric_native'])
 cj=chart_spacetime_jets(s,c)
 for name,a in cj.items():capture(label+'_first_'+name,a)
 return s,c,cj

def fresh_d0_gauge_envelopes(s,c,delta_n,delta_b,label):
 # Only for the declared constant Minkowski fixture: N=1,beta=0,h=I.
 # Build |delta(dg)| before the Christoffel cyclic cancellation. Never use
 # abs(finished deltaGamma), deltaPi or a finished zero canonical derivative.
 p=len(delta_n);ejet=np.zeros((p,4,4,4))
 ejet[:,0,0,0]=2*abs(delta_n);ejet[:,0,0,1:]=abs(delta_b);ejet[:,0,1:,0]=abs(delta_b)
 eGa=np.zeros_like(s['Ga'])
 for a in range(4):
  for b in range(4):eGa[:,:,a,b]=np.einsum('plm,pm->pl',abs(s['hi']),ejet[:,a,b,:]+ejet[:,b,a,:]+ejet[:,:,a,b])/2
 e_du=np.zeros_like(s['du']);e_du[:,0,0]=abs(s['U'][:,0])*abs(delta_n);e_du[:,0,1:]=abs(s['U'][:,0,None])*abs(delta_b)
 e_dz=np.zeros_like(s['dz']);e_t=np.einsum('pi,jpi->jp',abs(s['U'][:,1:]),abs(s['z'][:,:,1:]))
 e_dz[:,:,0,0]=np.einsum('pi,jpi->jp',e_du[:,0,1:],abs(s['z'][:,:,1:]))/abs(s['U'][None,:,0])+e_t*e_du[None,:,0,0]/s['U'][None,:,0]**2
 eNu=e_du+np.einsum('pbal,pl->pab',eGa,abs(s['U']))
 eNz=e_dz+np.einsum('plab,jpl->jpab',eGa,abs(s['z']))
 eQ=np.einsum('pa,jpab->jpb',abs(s['U']),eNz)
 eV=np.einsum('pab,jpb->jpa',abs(s['P']),eQ)
 eD=np.einsum('pac,jpcd,pbd->jpab',abs(s['P']),eNz,abs(s['P']))
 lo=np.einsum('pab,pcb->pca',abs(s['g']),eNu);eF=lo+lo.swapaxes(1,2)
 eVu=np.einsum('pab,jpb->jpa',abs(s['hi']),eV)
 eDu=np.einsum('pac,jpcd,pdb->jpab',abs(s['hi']),eD,abs(s['hi']))
 ePi=abs(s['w'])[:,None,None,None]*(np.einsum('pa,jpb->jpab',abs(s['U']),eVu)/s['omega'][:,None,None,None]**2+ELL**2*eDu)
 ePU=abs(ALPHA)*np.einsum('pac,pcb->pab',abs(s['hi']),eF)
 esym=(ePi+ePi.swapaxes(2,3))/2
 eK=np.einsum('jpab,jpl->plab',esym,abs(s['z']))
 eKu=np.einsum('plm,pmab->plab',abs(s['hi']),eK)
 eCD=(eKu.transpose(0,2,1,3)+eKu.transpose(0,2,3,1)+eKu)/2
 eFu=np.einsum('pac,pcd,pdb->pab',abs(s['hi']),eF,abs(s['hi']))
 eCM=abs(ALPHA)*(eFu[:,:,:,None]*abs(s['U'][:,None,None,:])+eFu[:,:,None,:]*abs(s['U'][:,None,:,None]))/2
 eCT=eCD+eCM
 # Upstream chart bounds are kept even when the chart's signed contraction
 # vanishes. Configuration/density variations are exactly zero in this test.
 eJU=np.empty_like(c['JU']);eJU[:,0]=abs(c['up'])/(c['N']*c['gamma'])[:,None]
 eJU[:,1:]=abs(c['ih'])+abs(c['beta'][:,:,None])*eJU[:,None,0]
 eJzU=np.einsum('jpa,pai->jpi',abs(s['z']),eJU)/abs(s['U'][None,:,0,None])
 eJzz=abs(s['U'][:,1:]/s['U'][:,0,None])
 E=abs(c['embed'][:,:,1:,1:]);eUh=np.empty_like(c['Uh'])
 eUh[:,:,0]=np.einsum('pi,pkij,pj->pk',abs(c['up']),E,abs(c['up']))/(2*c['N']*c['gamma'])[:,None]
 eUh[:,:,1:]=np.einsum('pij,pkjl,pl->pki',abs(c['ih']),E,abs(c['up']))+abs(c['beta'][:,None,:])*eUh[:,:,0,None]
 ezh=np.einsum('jpa,pka->jpk',abs(s['z']),eUh)/abs(s['U'][None,:,0,None])
 eu=np.einsum('pa,pai->pi',ePU[:,0],eJU)+np.einsum('jp,jpi->pi',ePi[:,:,0,0],eJzU)
 ez=ePi[:,:,0,1:]+ePi[:,:,0,0,None]*eJzz[None]
 en=c['dens'][:,None]*np.concatenate((eu,ez.transpose(1,0,2).reshape(p,96)),axis=1)
 em=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',eCT[:,0],abs(c['embed']))+np.einsum('pa,pka->pk',ePU[:,0],eUh)+np.einsum('jp,jpk->pk',ePi[:,:,0,0],ezh))
 for name,a in dict(metric_jet=ejet,Gamma=eGa,du=e_du,dz=e_dz,nu=eNu,nz=eNz,V=eV,D=eD,F=eF,Pi=ePi,PiU=ePU,connection=eCT,JU=eJU,JzU=eJzU,Jzz=eJzz,Uh=eUh,zh=ezh,native=en,metric=em).items():capture(label+'_positive_'+name,a)
 return en,em

def fresh_d0_momentum_fixtures(xi,w,omega):
 assert xi.shape==w.shape==omega.shape==(32,) and np.all(xi>0) and np.all(w>0) and np.all(omega>0)
 # Nonzero mode amplitudes/rates in every one of the32 retained slots. Their
 # rational values are artificial control data, not a physical preparation.
 j=np.arange(1,33,dtype=float);zz=j/320;cc=(j+1)/480
 a=5/4;ad=2/7;R=7/5
 g=np.zeros((1,4,4));g[0]=np.diag((-1,a*a,a*a,a*a*R*R))
 dg=np.zeros((1,4,4,4));dg[0,0,1:,1:]=np.diag((2*a*ad,2*a*ad,2*a*ad*R*R));dg[0,1,3,3]=2*a*a*R
 U=np.array(((1.,0.,0.,0.),));du=np.zeros((1,4,4));z=np.zeros((32,1,4));z[:,0,1]=zz
 dz=np.zeros((32,1,4,4));dz[:,0,0,1]=cc;phi=np.array(((1.,0.,0.,0.),))
 s,c,cj=fresh_d0_fixture_state(g,dg,U,du,z,dz,phi,xi,w,omega,'fresh_cylindrical')
 v=np.zeros((1,99));v[0,3:].reshape(32,3)[:,0]=cc
 k=dg[:,0,1:,1:].copy();vs=np.zeros((1,3,99));ks=np.zeros((1,3,3,3));ks[0,0,2,2]=4*a*ad*R
 zero=np.zeros(1);b=np.zeros((1,3));ns=np.zeros((1,3));bs=np.zeros((1,3,3))
 out=derivative_at_seed(s,c,cj,v,k,vs,ks,zero,b,ns,bs,zero,b,'fresh_cylindrical')
 # hddot=0 -> addot=-adot²/a. These exact targets do not assume a cosmic law.
 ex=np.zeros((1,99));ex[0,0]=R*np.sum(w*(ad*zz+a*cc));ex[0,3:].reshape(32,3)[:,0]=w*R*ad*ad*zz/(a*omega**2)
 capture('fresh_cylindrical_expected_native',ex);check('fresh_cylindrical_D0_native',out['native'],ex,abs(ex)+abs(out['native_terms']).sum(axis=-1))
 terms=np.column_stack((cc**2/a,-3*ad*zz*cc/a**2,3*ad**2*zz**2/a**3))
 em=np.zeros((1,6));em[0,0]=-R*np.sum(w*terms.sum(axis=1)/omega**2)/2
 eb=np.zeros_like(em);eb[0,0]=R*np.sum(w*abs(terms).sum(axis=1)/omega**2)/2
 capture('fresh_cylindrical_metric_target_terms',terms);capture('fresh_cylindrical_expected_metric_native',em)
 check('fresh_cylindrical_D0_metric_native',out['metric_native'],em,eb+abs(out['metric_native_terms']).sum(axis=-1))
 ee=np.zeros((1,6));ee[0,:3]=ad**2/(a*C)*np.array((R,R,1/R))
 capture('fresh_cylindrical_expected_EH',ee);check('fresh_cylindrical_D0_EH',out['metric_EH'],ee,abs(ee)+abs(out['metric_EH']))
 # The nonzero cylindrical spatial covariant jet D_phi,phi=R*z is present,
 # but it has no aligned temporal momentum vertex. Quartic variation is an
 # independent algebraic force contact; it is never placed in the momentum.
 fq=1+zz**2/(a*a*(B*GC)**2*xi**4)
 dfq=(2*zz*cc/a**2-2*ad*zz**2/a**3)/((B*GC)**2*xi**4)
 az=np.zeros((32,1,4));az[:,0,1]=-w*(dfq*zz/a**2+fq*(cc/a**2-2*ad*zz/a**3))
 azb=np.zeros_like(az);edf=(2*abs(zz*cc)/a**2+2*abs(ad*zz**2)/a**3)/((B*GC)**2*xi**4)
 azb[:,0,1]=w*(edf*abs(zz)/a**2+fq*(abs(cc)/a**2+2*abs(ad*zz)/a**3))
 def keep_quartic(name,x):capture('fresh_cylindrical_'+name,x)
 af=derivative_native_force_features(s,out['primitive'],out['features'],np.zeros_like(phi),keep_quartic)
 capture('fresh_cylindrical_expected_quartic',az);check('fresh_cylindrical_D0_quartic_contact',af['A_z_raw'],az,azb+abs(af['A_z_raw']))
 # A Cartesian local patch (constant spatial metric jets) with a genuine
 # anisotropic symmetric hdot, including offdiagonal coordinate factors2.
 g=np.diag((-1.,1.,1.,1.))[None];dg=np.zeros((1,4,4,4))
 km=np.array(((2/7,1/5,-1/11),(1/5,-3/8,1/13),(-1/11,1/13,4/9)))
 dg[0,0,1:,1:]=km;z=np.zeros((32,1,4));z[:,0,1:]=zz[:,None]*np.array((1.,-2/3,1/4))
 dz=np.zeros((32,1,4,4));dz[:,0,0,1:]=cc[:,None]*np.array((-1/5,1.,2/7))
 s,c,cj=fresh_d0_fixture_state(g,dg,U,du,z,dz,phi,xi,w,omega,'fresh_sheared')
 v=np.zeros((1,99));v[0,3:]=dz[:,0,0,1:].reshape(96);k=km[None]
 out=derivative_at_seed(s,c,cj,v,k,vs,np.zeros_like(ks),zero,b,ns,bs,zero,b,'fresh_sheared')
 zs=z[:,0,1:];cs=dz[:,0,0,1:];theta=np.trace(km)/2;kk=km@km
 kz=np.einsum('ab,jb->ja',km,zs);kc=np.einsum('ab,jb->ja',km,cs);kkz=np.einsum('ab,jb->ja',kk,zs)
 pz=w[:,None]/omega[:,None]**2*(cs-kz/2)
 dpz=w[:,None]/omega[:,None]**2*(theta*(cs-kz/2)+kkz-3*kc/2)
 ex=np.zeros((1,99));ex[0,:3]=np.sum(w[:,None]*(theta*zs+cs-kz),axis=0);ex[0,3:]=dpz.reshape(96)
 capture('fresh_sheared_expected_native',ex);check('fresh_sheared_D0_native',out['native'],ex,abs(ex)+abs(out['native_terms']).sum(axis=-1))
 dzu=cs-kz
 mt=-np.einsum('ja,jb->ab',dpz,zs)/4-np.einsum('ja,jb->ab',zs,dpz)/4-np.einsum('ja,jb->ab',pz,dzu)/4-np.einsum('ja,jb->ab',dzu,pz)/4
 mb=(np.einsum('ja,jb->ab',abs(dpz),abs(zs))+np.einsum('ja,jb->ab',abs(zs),abs(dpz))+np.einsum('ja,jb->ab',abs(pz),abs(dzu))+np.einsum('ja,jb->ab',abs(dzu),abs(pz)))/4
 em=np.array(((mt[0,0],mt[1,1],mt[2,2],2*mt[0,1],2*mt[0,2],2*mt[1,2]),))
 eb=np.array(((mb[0,0],mb[1,1],mb[2,2],2*mb[0,1],2*mb[0,2],2*mb[1,2]),))
 capture('fresh_sheared_expected_metric_native',em);check('fresh_sheared_D0_metric_native',out['metric_native'],em,eb+abs(out['metric_native_terms']).sum(axis=-1))
 trace=np.trace(km);et=(theta*(km-trace*np.eye(3))-2*kk+np.trace(kk)*np.eye(3)+trace*km)/(4*C)
 ebt=(abs(theta)*(abs(km)+abs(trace)*np.eye(3))+2*abs(km)@abs(km)+np.trace(abs(km)@abs(km))*np.eye(3)+abs(trace)*abs(km))/(4*C)
 ee=np.array(((et[0,0],et[1,1],et[2,2],2*et[0,1],2*et[0,2],2*et[1,2]),));eb=np.array(((ebt[0,0],ebt[1,1],ebt[2,2],2*ebt[0,1],2*ebt[0,2],2*ebt[1,2]),))
 capture('fresh_sheared_expected_EH',ee);check('fresh_sheared_D0_EH',out['metric_EH'],ee,eb+abs(out['metric_EH']))
 # Tilted constant Minkowski state. Four packed independent primary columns
 # are lapse,shiftR,shiftZ,shiftphi. Configuration variations vanish exactly;
 # the complete coordinate temporal jets and connection must cancel together.
 p=4;g=np.broadcast_to(np.diag((-1.,1.,1.,1.)),(p,4,4)).copy();dg=np.zeros((p,4,4,4))
 U=np.broadcast_to(np.array((5/4,3/4,0.,0.)),(p,4)).copy();du=np.zeros((p,4,4))
 z=np.zeros((32,p,4));z[:,:,1:]=zz[:,None,None]*np.array((1.,-2/3,1/4));z[:,:,0]=-3*z[:,:,1]/5
 dz=np.zeros((32,p,4,4));phi=np.broadcast_to(np.array((1.,0.,0.,0.)),(p,4)).copy()
 s,c,cj=fresh_d0_fixture_state(g,dg,U,du,z,dz,phi,xi,w,omega,'fresh_primary')
 dn=np.array((1.,0.,0.,0.));db=np.zeros((p,3));db[1:]=np.eye(3)
 out=primary_derivative_at_seed(s,c,dn,db,'fresh_primary_first')
 en,em=fresh_d0_gauge_envelopes(s,c,dn,db,'fresh_primary_first')
 actual=np.concatenate((out['native'],out['metric_total']),axis=1);bound=np.concatenate((en,em),axis=1)
 check('fresh_four_first_gauge_primary_cancellations',actual,np.zeros_like(actual),bound)
 # Only gauge second jets vary here. Mechanical rates/accelerations and all
 # first gauge velocities are zero; this is not a translation history choice.
 v=np.zeros((p,99));k=np.zeros((p,3,3));vs=np.zeros((p,3,99));ks=np.zeros((p,3,3,3))
 zero=np.zeros(p);b=np.zeros((p,3));ns=np.zeros((p,3));bs=np.zeros((p,3,3))
 out=derivative_at_seed(s,c,cj,v,k,vs,ks,zero,b,ns,bs,dn,db,'fresh_primary_second')
 en,em=fresh_d0_gauge_envelopes(s,c,dn,db,'fresh_primary_second')
 actual=np.concatenate((out['native'],out['metric_total']),axis=1);bound=np.concatenate((en,em),axis=1)
 check('fresh_four_second_gauge_primary_cancellations',actual,np.zeros_like(actual),bound)
 return dict(fresh_controls=9,retained_modes=32,synthetic_only=True,physical_history_qualified=False)


FORCE_TERMINAL={'owner_pid': 36387, 'source_sha256': '4f239074b5345709f493b3633f7dd376fa7ac97dbb23bf20825eabde2ed56b79', 'protocol_sha256': 'de6ae873e7cf783c4bdfbc20eeb0d5de82c27ea7dc709ba8832ed4c4ec7aba2b', 'result_sha256': '981a314d7ca598c101db34d4da6f36679c752da81d8cc1325c521f4ce0c7b770', 'receipt_sha256': '822c82d59631ebef6f87c0847829370792338a1dcb741c325843d1c8f07e3af2'}
FORCE_STEM='CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003'
FORCE_CP='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json'
FORCE_CP_SHA='3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c'
FORCE_SAVED_AUDIT='READONLY_CROSS_U_WEAK_CANONICAL_SPATIAL_EULER_LOADS_V003_SAVED_AUDIT.json'
FORCE_SAVED_AUDIT_SHA='80b7fac6e83d178bc2eb706853d301bbf258e0fe9f22caa0423e28010eac66e2'


def force_d0_column_shapes():
 p=3784;j=32;sh={}
 def add(prefix,rows):
  for n,a in rows.items():sh[prefix+n]=list(a)
 add('seed_',dict(g=(p,4,4),hi=(p,4,4),Ga=(p,4,4,4),U=(p,4),uc=(p,4),du=(p,4,4),z=(j,p,4),dz=(j,p,4,4),phi=(p,4),nu=(p,4,4),nz=(j,p,4,4),P=(p,4,4),q=(j,p,4),V=(j,p,4),D=(j,p,4,4),F=(p,4,4),Fup=(p,4,4),Pi=(j,p,4,4),PiU=(p,4,4),Z=(p,4),A=(p,4),mu=(j,p),a=(p,4),r=(p,4),f=(j,p),z2=(j,p),V_raised=(j,p,4),connection_Klo=(p,4,4,4),connection_momentum=(p,4,4,4),connection_D=(p,4,4,4),connection_Maxwell=(p,4,4,4),R=(p,),Z_coordinate=(p,),phase_P=(p,),phase_PX=(p,),phase_PXX=(p,),phase_X=(p,)))
 add('seed_chart_',dict(h=(p,3,3),ih=(p,3,3),N=(p,),beta=(p,3),u=(p,3),up=(p,3),gamma=(p,),JU=(p,4,3),JzU=(j,p,3),Jzz=(p,3),embed=(p,6,4,4),Uh=(p,6,4),zh=(j,p,6),dens=(p,),sqrt_h=(p,),old_velocity=(p,99),K=(p,3,3),Ktrace=(p,)))
 add('seed_chart_derivative_',dict(dg=(p,4,4,4),dhi=(p,4,4,4),dN=(p,4),dbeta=(p,4,3),dh=(p,4,3,3),dih=(p,4,3,3),du_cov=(p,4,3),dup=(p,4,3),dgamma=(p,4),dJU=(p,4,4,3),dJzU=(j,p,4,3),dJzz=(p,4,3),dUh=(p,4,6,4),dzh=(j,p,4,6),dembed=(p,4,6,4,4)))
 add('',dict(seed_nodal_native_rate=(p,99),seed_old_L2_native_rate=(p,99),seed_native_rate_delta=(p,99),seed_covariant_native_rate_R=(33,p,3),seed_covariant_native_rate_Z=(33,p,3),seed_metric_L2_rate=(p,3,3),seed_metric_L2_rate_R=(p,3,3),seed_metric_L2_rate_Z=(p,3,3),seed_owned_coordinate_Ndot=(p,),seed_owned_coordinate_betadot=(p,3),new_native_momentum=(p,99),new_metric_native_momentum=(p,6),new_metric_EH_momentum=(p,3,3),new_metric_total_momentum=(p,6),new_phase_current=(p,4),new_phase_canonical_density=(p,),native_Euler_coefficient=(p,99,3),native_Euler_envelope=(p,99,3),metric_Euler_coefficient=(p,6,3),metric_Euler_envelope=(p,6,3),metric_Euler_component_coefficients=(p,6,3,15),metric_Euler_component_envelope=(p,6,3,15)))
 return sh

def force_d0_require_schema(rec,shapes):
 for n,shape in shapes.items():
  assert rec['metadata']['schema'][n]==dict(shape=shape,dtype='float64',finite=True),(rec['file'],n)

def force_success_admission():
 # This gate precedes every file access and every numerical load.
 assert type(FORCE_TERMINAL['owner_pid']) is int and all(type(FORCE_TERMINAL[k]) is str and len(FORCE_TERMINAL[k])==64 for k in ('source_sha256','protocol_sha256','result_sha256','receipt_sha256')),'Actual natural CLOSED force terminal is required.'
 assert sha(path(FORCE_SAVED_AUDIT))==FORCE_SAVED_AUDIT_SHA;aud=json.loads(path(FORCE_SAVED_AUDIT).read_text())
 assert aud['status']=='SAVED_PACKET_AUDIT_PASS' and aud['control_count']==36 and aud['census']['pairs']==8 and aud['D0_seed_operands_admitted'] is True and aud['original_failed_gate_preserved'] is True and aud['terminal']['error_sha256'] is None and all(aud['terminal'][k]==v for k,v in FORCE_TERMINAL.items())
 names=dict(source='cross_u_weak_canonical_spatial_euler_loads_v003.py',protocol=FORCE_STEM+'.md',result=FORCE_STEM+'_RESULT.json',receipt=FORCE_STEM+'_RECEIPT.json')
 for k,n in names.items():assert sha(path(n))==FORCE_TERMINAL[k+'_sha256'],(k,n)
 result=json.loads(path(names['result']).read_text());rc=json.loads(path(names['receipt']).read_text());owner=result['owner']
 assert rc['status']=='CLOSED' and rc['owner']==owner and owner['owner']=='root' and owner['pid']==FORCE_TERMINAL['owner_pid'] and owner['source_sha256']==FORCE_TERMINAL['source_sha256']
 assert rc['result_sha256']==FORCE_TERMINAL['result_sha256'] and rc.get('error_sha256') is None
 assert result['status']=='CONDITIONAL_WEAK_CANONICAL_SPATIAL_EULER_ARITHMETIC_PASS' and len(result['cases'])==1
 assert len(result['controls'])==36 and all(c['ordinal']==i and c['passed'] is True and c['tolerance']==2e-11 for i,c in enumerate(result['controls']))
 assert all(v is False for v in result['qualification'].values()) and result['qualification']==rc['qualification']
 pins={str(path(FORCE_SAVED_AUDIT).resolve()):FORCE_SAVED_AUDIT_SHA}
 for mapping in (rc['input_sha256'],rc['output_sha256'],{names[k]:FORCE_TERMINAL[k+'_sha256'] for k in names}):
  for n,h in mapping.items():
   key=str(path(n).resolve());assert key not in pins or pins[key]==h;assert sha(path(n))==h;pins[key]=h
 assert pins[str(path(FORCE_CP).resolve())]==FORCE_CP_SHA
 manifest=json.loads(path(FORCE_STEM+'_MANIFEST.json').read_text());assert manifest['owner']==owner and manifest['input_sha256']==rc['input_sha256']
 assert json.loads(path(FORCE_STEM+'_OWNER_START.json').read_text())==owner
 cfg=manifest['configuration'];assert (cfg['sigma'],cfg['modes'],cfg['columns'],cfg['points'],cfg['controls'],cfg['pairs'],cfg['tolerance'])==(1.,32,4,15136,36,8,2e-11)
 records=[]
 for ref in result['checkpoints']:
  rec=resolve_record(ref);assert {k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}=={k:v for k,v in ref.items() if k not in ('commit_file','commit_sha256')}
  assert rec['metadata']['owner']==owner and rec['metadata']['failed'] is False and rec['metadata']['qualification']==result['qualification'];records.append(rec)
 assert len(records)==8 and [r['file'].rsplit('_',1)[-1] for r in records]==['INPUT.npz','FIXTURE.npz','BASIS.npz','COLUMN.npz','COLUMN.npz','COLUMN.npz','COLUMN.npz','LOADS.npz']
 assert {p.name for p in BASE.glob(FORCE_STEM+'_*.npz')}=={r['file'] for r in records}
 assert {p.name for p in BASE.glob(FORCE_STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in records}
 case=result['cases'][0];assert case['sigma']==1. and case['status']=='CONDITIONAL_WEAK_CANONICAL_SPATIAL_EULER_LOADS_PASS' and case['qualification']==result['qualification']
 assert case['columns']==records[3:7] and case['loads']==records[7]
 force_d0_require_schema(records[0],dict(r_kpc=[87],z_kpc=[45],xi=[32],weights=[32]));fixed=records[0]['metadata']['fixed'];cp=json.loads(path(FORCE_CP).read_text())
 assert cp['eps']==1e-5 and records[0]['metadata']['owned_background']==cp['background'] and records[0]['metadata']['new_source_terms'] is False
 for iq,rec in enumerate(records[3:7]):
  md=rec['metadata'];assert md['column']==iq and md['points']==3784 and md['sigma']==1. and md['coefficient_jet_order']==['value','R','Z'] and md['physical_changes']==[]
  assert all(v is None for v in md['unknown_ports'].values());force_d0_require_schema(rec,force_d0_column_shapes())
 assert records[7]['metadata']['unknowns']['phase_charge_evolution'] is None and records[7]['metadata']['force_scope']=='spatial E only; E minus pdot_noacc not yet computed'
 return pins,dict(result=result,receipt=rc,input=records[0],basis=records[2],columns=records[3:7],loads=records[7]),fixed,cp

def load_force_column(ref):
 rec=resolve_record(ref);force_d0_require_schema(rec,force_d0_column_shapes());raw=read_pair(rec,tuple(force_d0_column_shapes()))
 features=('g','hi','Ga','U','uc','du','z','dz','phi','nu','nz','P','q','V','D','F','Fup','Pi','PiU','Z','A','mu','a','r','f','z2','V_raised','connection_Klo','connection_momentum','connection_D','connection_Maxwell')
 s={k:raw['seed_'+k] for k in features};c={k.removeprefix('seed_chart_'):a for k,a in raw.items() if k.startswith('seed_chart_') and not k.startswith('seed_chart_derivative_')};cj={k.removeprefix('seed_chart_derivative_'):a for k,a in raw.items() if k.startswith('seed_chart_derivative_')}
 c.update(pi_EH=raw['new_metric_EH_momentum'],p_native=raw['new_native_momentum'],p_metric_native=raw['new_metric_native_momentum'])
 rates={k:raw[k] for k in ('seed_nodal_native_rate','seed_covariant_native_rate_R','seed_covariant_native_rate_Z','seed_metric_L2_rate','seed_metric_L2_rate_R','seed_metric_L2_rate_Z','seed_owned_coordinate_Ndot','seed_owned_coordinate_betadot')}
 momenta={k:raw[k] for k in ('new_native_momentum','new_metric_native_momentum','new_metric_EH_momentum','new_metric_total_momentum','new_phase_current','new_phase_canonical_density')}
 # Caller attaches exact INPUT xi/weights and the already registered omega conversion.
 # Gauge n,b and their gradients stay independent; this loader chooses none.
 return s,c,cj,rates,momenta,raw



def bounded_D0(s,c,cj,v,k,vs,ks,n,b,ns,bs,n2,b2,label):
 # All signed operations remain in the accepted analytic kernel. Bounds are
 # independently positive product chains, with the same per-component scale.
 out=derivative_at_seed(s,c,cj,v,k,vs,ks,n,b,ns,bs,n2,b2,label)
 ed,pr=primitive_time_direction_operation_envelopes(s,c,cj,v,k,vs,ks,n,b,ns,bs,n2,b2,label)
 ec=derivative_chart_operation_envelopes(s,c,ed,pr,k,n,b,label)
 en,em,ops=derivative_operation_envelopes(s,c,out['primitive'],out['chart'],out['features'],label,dict(primitive=ed,chart=ec))
 ee,ehops=derivative_EH_momentum_operation_envelope(c,pr,k,ks,n,b,bs,label)
 out.update(native_envelope=en,metric_native_envelope=em,metric_EH_envelope=ee,metric_total_envelope=em+ee,operations=ops,EH_operations=ehops)
 for key in ('native','metric_native','metric_EH','metric_total','native_envelope','metric_native_envelope','metric_EH_envelope','metric_total_envelope','native_terms','metric_native_terms'):capture(label+'_'+key,out[key])
 return out

def gauge_first_directions(p):
 # Local coefficient directions, not a selected global gauge or nodal basis.
 labels=('Ndot','betadot_R','betadot_Z','betadot_phi','Ndot_R','Ndot_Z','betadot_R_R','betadot_R_Z','betadot_Z_R','betadot_Z_Z','betadot_phi_R','betadot_phi_Z')
 out=[]
 for i in range(12):
  n=np.zeros(p);b=np.zeros((p,3));ns=np.zeros((p,3));bs=np.zeros((p,3,3))
  if i==0:n[:]=1
  elif i<4:b[:,i-1]=1
  elif i<6:ns[:,i-4]=1
  else:
   j=i-6;bs[:,j%2,j//2]=1
  out.append((labels[i],n,b,ns,bs))
 return out

def D0_seed_column(iq,ref,xi,w,omega):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};CONTEXT.update(stage='new_analytic_D0_at_saved_seed',column=iq);start=len(CHECKS)
 s,c,cj,rates,mom,raw=load_force_column(ref);s.update(xi=xi,w=w,omega=omega)
 p=len(c['N']);v=rates['seed_nodal_native_rate'];k=rates['seed_metric_L2_rate'];vs=np.zeros((p,3,99));ks=np.zeros((p,3,3,3))
 for j,ax in enumerate(('R','Z')):
  vs[:,j]=rates['seed_covariant_native_rate_'+ax].transpose(1,0,2).reshape(p,99);ks[:,j]=rates['seed_metric_L2_rate_'+ax]
 for name,a in dict(native_rate=v,metric_L2_rate=k,native_rate_spatial=vs,metric_L2_rate_spatial=ks,owned_Ndot=rates['seed_owned_coordinate_Ndot'],owned_betadot=rates['seed_owned_coordinate_betadot']).items():capture('actual_seed_'+name,a)
 zero=np.zeros(p);bzero=np.zeros((p,3));nszero=np.zeros((p,3));bszero=np.zeros((p,3,3));vz=np.zeros_like(v);kz=np.zeros_like(k);vsz=np.zeros_like(vs);ksz=np.zeros_like(ks)
 base=bounded_D0(s,c,cj,v,k,vs,ks,zero,bzero,nszero,bszero,zero,bzero,'D0_intercept')
 check('D0_native_full_signed_product_recontraction',base['native_terms'].sum(axis=-1),base['native'],base['native_envelope']+abs(base['native_terms']).sum(axis=-1))
 check('D0_native_metric_full_signed_product_recontraction',base['metric_native_terms'].sum(axis=-1),base['metric_native'],base['metric_native_envelope']+abs(base['metric_native_terms']).sum(axis=-1))
 data={k0:a for k0,a in AVAILABLE.items() if k0.startswith('D0_intercept_')}
 gn=[];gm=[];ge=[];gnt=[];gmt=[];eng=[];emg=[];eeg=[]
 directions=gauge_first_directions(p)
 for label,n,b,ns,bs in directions:
  CONTEXT.update(stage='local_first_gauge_coefficient',gauge_direction=label)
  out=bounded_D0(s,c,cj,vz,kz,vsz,ksz,n,b,ns,bs,zero,bzero,'D0_gauge_work')
  gn.append(out['native']);gm.append(out['metric_native']);ge.append(out['metric_EH']);gnt.append(out['native_terms']);gmt.append(out['metric_native_terms']);eng.append(out['native_envelope']);emg.append(out['metric_native_envelope']);eeg.append(out['metric_EH_envelope'])
  for key,a in dict(native=np.stack(gn),metric_native=np.stack(gm),metric_EH=np.stack(ge),native_terms=np.stack(gnt),metric_native_terms=np.stack(gmt),native_envelope=np.stack(eng),metric_native_envelope=np.stack(emg),metric_EH_envelope=np.stack(eeg)).items():capture('completed_first_gauge_'+key,a)
 gn,gm,ge=np.stack(gn),np.stack(gm),np.stack(ge);eng,emg,eeg=np.stack(eng),np.stack(emg),np.stack(eeg)
 primary=[];primary_env=[]
 for i in range(4):
  CONTEXT.update(stage='primary_second_gauge_cancellation',direction=i)
  n2=zero.copy();b2=bzero.copy()
  if i==0:n2[:]=1
  else:b2[:,i-1]=1
  out=bounded_D0(s,c,cj,vz,kz,vsz,ksz,zero,bzero,nszero,bszero,n2,b2,'D0_primary_work')
  primary.append(np.concatenate((out['native'],out['metric_total']),axis=1));primary_env.append(np.concatenate((out['native_envelope'],out['metric_total_envelope']),axis=1))
  capture('completed_second_gauge_actual',np.stack(primary));capture('completed_second_gauge_envelope',np.stack(primary_env))
 primary=np.stack(primary);primary_env=np.stack(primary_env);check('actual_four_second_gauge_primary_cancellations',primary,np.zeros_like(primary),primary_env)
 # Independent direct composite direction certifies the entire local affine
 # first-gauge decomposition. These artificial values are not physical data.
 amps=np.array((2/7,-3/11,5/13,-7/17,11/19,-13/23,17/29,-19/31,23/37,-29/41,31/43,-37/47))
 nn=zero.copy();bb=bzero.copy();ns=nszero.copy();bs=bszero.copy()
 for a,(_,n,b,nsp,bsp) in zip(amps,directions):nn+=a*n;bb+=a*b;ns+=a*nsp;bs+=a*bsp
 direct=bounded_D0(s,c,cj,v,k,vs,ks,nn,bb,ns,bs,zero,bzero,'D0_linearity_work')
 predn=base['native']+np.einsum('a,api->pi',amps,gn);predm=base['metric_total']+np.einsum('a,api->pi',amps,gm+ge)
 en=base['native_envelope']+np.einsum('a,api->pi',abs(amps),eng)+direct['native_envelope'];em=base['metric_total_envelope']+np.einsum('a,api->pi',abs(amps),emg+eeg)+direct['metric_total_envelope']
 capture('first_gauge_linearity_amplitudes',amps);capture('first_gauge_linearity_direct_native',direct['native']);capture('first_gauge_linearity_direct_metric',direct['metric_total'])
 check('actual_local_first_gauge_affine_decomposition',np.concatenate((predn,predm),axis=1),np.concatenate((direct['native'],direct['metric_total']),axis=1),np.concatenate((en,em),axis=1))
 phase=phase_charge_temporal_coefficients(s,c,v,k,raw['seed_phase_PX'],raw['seed_phase_PXX'],raw['seed_phase_X'],'current_phase')
 phase_env=c['sqrt_h']*(abs(raw['seed_phase_PX'])+abs(raw['seed_phase_X'])*np.einsum('pi,pi->p',abs(c['u']),abs(c['up'])))+abs(mom['new_phase_canonical_density'])
 check('exact_current_phase_charge_chart_density',phase['registered_charge_density'],mom['new_phase_canonical_density'],phase_env)
 # Only the already-owned coordinate gauge VALUE jets are included here.
 # Their R/Z derivatives remain independent symbolic fields, not zero data.
 owned=np.column_stack((rates['seed_owned_coordinate_Ndot'],rates['seed_owned_coordinate_betadot']))
 knownn=base['native']+np.einsum('pa,api->pi',owned,gn[:4]);knownm=base['metric_total']+np.einsum('pa,api->pi',owned,(gm+ge)[:4])
 knownen=base['native_envelope']+np.einsum('pa,api->pi',abs(owned),eng[:4]);knownem=base['metric_total_envelope']+np.einsum('pa,api->pi',abs(owned),(emg+eeg)[:4])
 data.update(D0_native_intercept=base['native'],D0_metric_native_intercept=base['metric_native'],D0_metric_EH_intercept=base['metric_EH'],D0_metric_total_intercept=base['metric_total'],D0_native_intercept_envelope=base['native_envelope'],D0_metric_total_intercept_envelope=base['metric_total_envelope'],D0_native_registered_gauge_values=knownn,D0_metric_registered_gauge_values=knownm,D0_native_registered_gauge_values_envelope=knownen,D0_metric_registered_gauge_values_envelope=knownem,first_gauge_native_coefficients=gn,first_gauge_metric_native_coefficients=gm,first_gauge_metric_EH_coefficients=ge,first_gauge_native_envelope=eng,first_gauge_metric_native_envelope=emg,first_gauge_metric_EH_envelope=eeg,first_gauge_native_product_terms=np.stack(gnt),first_gauge_metric_native_product_terms=np.stack(gmt),first_gauge_linearity_amplitudes=amps,second_gauge_canonical_actual=primary,second_gauge_canonical_envelope=primary_env,current_phase_density=mom['new_phase_canonical_density'],current_phase_current_density=c['dens'][:,None]*mom['new_phase_current'],owned_gauge_value_jets=owned,current_native_spatial_Euler_coefficient=raw['native_Euler_coefficient'],current_metric_spatial_Euler_coefficient=raw['metric_Euler_coefficient'])
 data.update({'phase_'+key:a for key,a in phase.items()});data.update({key:a for key,a in RAW.items() if key.startswith('control_')})
 for key,a in data.items():finite_real('D0_column_'+key,a)
 assert len(CHECKS)-start==5
 rec=checkpoint('COLUMN',data,dict(kind='actual_same_action_formal_D0_and_local_gauge_coefficients',sigma=SIGMA,column=iq,parent=ref,controls=CHECKS[start:],gauge_first_labels=[r[0] for r in directions],inactive_phi_gradients=True,gauge_scope='four saved coordinate value jets retained; eight spatial gauge jets remain symbolic',mechanical_acceleration_scope='algebraic partial at zero mechanical accelerations; physical accelerations not selected',metric_rate_scope='saved L2 kstar, not solved nodal metric rate',phase_scope='current phi_i=0 only; physical phi_tt unselected',ordinary_pdot=None,temporal_improvement_ports=None,outer_ports=None,physical_changes=[]))
 return dict(data={key:data[key] for key in ('D0_native_registered_gauge_values','D0_metric_registered_gauge_values','D0_native_registered_gauge_values_envelope','D0_metric_registered_gauge_values_envelope','current_phase_current_density','phase_mechanical_charge_rate','phase_lapse_velocity_coefficient','owned_gauge_value_jets')},record=rec)



def scalar_phase_flux_operation_envelope(Jdens,geo):
 out=np.zeros((87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);weight=geo['dv'][iq]/geo['R'][iq]
  for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hats=abs(geo['hats'][iq,a].reshape(3,3784));value=(hats[1]*abs(Jdens[sl,1])+hats[2]*abs(Jdens[sl,2]))*weight
   np.add.at(out,(geo['cell_i']+di,geo['cell_j']+dj),value)
 out[1]+=out[0];out[0]=0
 return out

def point_D0_weak_density(field,kind,independent=False,envelope=False):
 co=np.zeros(field.shape+(3,));co[:,:,0]=field
 return scatter_configuration_coefficients(co,GEO,kind,independent=independent,envelope=envelope)

def D0_weak_assembly(columns,force):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};CONTEXT.update(stage='genuine_D0_weak_load_and_known_force_assembly');start=len(CHECKS)
 rows=[x['data'] for x in columns];pn=np.concatenate([x['D0_native_registered_gauge_values'] for x in rows]);pm=np.concatenate([x['D0_metric_registered_gauge_values'] for x in rows]);en=np.concatenate([x['D0_native_registered_gauge_values_envelope'] for x in rows]);em=np.concatenate([x['D0_metric_registered_gauge_values_envelope'] for x in rows])
 nl=point_D0_weak_density(pn,'native');capture('D0_native_registered_gauge_values_load',nl);ne=point_D0_weak_density(en,'native',envelope=True);ni=point_D0_weak_density(pn,'native',independent=True)
 check('new_D0_native_value_density_weak_incidence',nl,ni,ne+abs(ni))
 ml=point_D0_weak_density(pm,'metric');capture('D0_metric_registered_gauge_values_load',ml);me=point_D0_weak_density(em,'metric',envelope=True);mi=point_D0_weak_density(pm,'metric',independent=True)
 check('new_D0_metric_value_density_weak_incidence',ml,mi,me+abs(mi))
 Jdens=np.concatenate([x['current_phase_current_density'] for x in rows]);flux=scalar_phase_weak_flux(Jdens,GEO);capture('exact_current_phase_weak_flux',flux);fi=scalar_phase_weak_flux(Jdens,GEO,independent=True);fe=scalar_phase_flux_operation_envelope(Jdens,GEO)
 check('new_exact_phase_current_weak_flux_incidence',flux,fi,fe+abs(fi))
 old=read_pair(force['loads'],('native_spatial_Euler_load','native_spatial_Euler_envelope','complete_known_metric_spatial_Euler_load','complete_known_metric_spatial_Euler_envelope','ordinary_metric_spatial_Euler_load','ordinary_metric_spatial_Euler_envelope'))
 fn=old['native_spatial_Euler_load']-nl;fm=old['complete_known_metric_spatial_Euler_load']-ml;fne=old['native_spatial_Euler_envelope']+ne;fme=old['complete_known_metric_spatial_Euler_envelope']+me
 for key,a in dict(known_native_E_minus_D0p_load=fn,known_metric_E_minus_D0p_load=fm,known_native_E_minus_D0p_envelope=fne,known_metric_E_minus_D0p_envelope=fme).items():capture(key,a)
 # A fresh deterministic test in the registered physical bases independently
 # contracts the saved spatial E load and the new coordinate momentum density.
 nt=(np.arange(fn.size)%13-6).reshape(fn.shape)/37.;mt=(np.arange(fm.size)%11-5).reshape(fm.shape)/41.;nv=evaluate_velocity(nt,GEO);mv=evaluate_metric(mt,GEO);weight=(GEO['dv']/GEO['R']).reshape(15136)
 actual=np.array((np.sum(fn*nt),np.sum(fm*mt)))
 expected=np.array((np.sum(old['native_spatial_Euler_load']*nt)-np.einsum('pi,ip,p->',pn,nv.transpose(1,0,2).reshape(15136,99).T,weight),np.sum(old['complete_known_metric_spatial_Euler_load']*mt)-np.einsum('pi,pi,p->',pm,mv,weight)))
 bound=np.array((np.sum(fne*abs(nt))+np.sum(old['native_spatial_Euler_envelope']*abs(nt))+np.einsum('pi,pi,p->',en,abs(nv.transpose(1,0,2).reshape(15136,99)),weight),np.sum(fme*abs(mt))+np.sum(old['complete_known_metric_spatial_Euler_envelope']*abs(mt))+np.einsum('pi,pi,p->',em,abs(mv),weight)))
 capture('new_D0_force_native_test',nt);capture('new_D0_force_metric_test',mt);capture('new_D0_force_direct_weak_pairing',expected)
 check('new_E_minus_D0p_registered_weak_functional_pairing',actual,expected,bound)
 mechanical=np.concatenate([x['phase_mechanical_charge_rate'] for x in rows]);nc=np.concatenate([x['phase_lapse_velocity_coefficient'] for x in rows]);owned=np.concatenate([x['owned_gauge_value_jets'] for x in rows]);charge_known=mechanical+nc*owned[:,0]
 # This is the known local charge-rate part. phi_tt has not been solved.
 # The scalar weak mass/clock map and source-location material jets remain future inputs.
 data=dict(D0_native_registered_gauge_values_load=nl,D0_metric_registered_gauge_values_load=ml,D0_native_weak_envelope=ne,D0_metric_weak_envelope=me,known_native_E_minus_D0p_load=fn,known_metric_E_minus_D0p_load=fm,known_native_E_minus_D0p_envelope=fne,known_metric_E_minus_D0p_envelope=fme,current_phase_current_density=Jdens,current_phase_weak_flux=flux,current_phase_weak_flux_envelope=fe,current_phase_known_charge_rate_density=charge_known,native_weak_test=nt,metric_weak_test=mt,ordinary_metric_spatial_Euler_load=old['ordinary_metric_spatial_Euler_load'],ordinary_metric_spatial_Euler_envelope=old['ordinary_metric_spatial_Euler_envelope'])
 data.update({key:a for key,a in RAW.items() if key.startswith('control_')})
 for key,a in data.items():finite_real('D0_load_'+key,a)
 assert len(CHECKS)-start==4
 return checkpoint('LOADS',data,dict(kind='new_D0_and_known_E_minus_D0p_weak_loads_with_exact_phase_flux',sigma=SIGMA,controls=CHECKS[start:],ordinary_pdot=None,physical_phi_tt=None,spatial_gauge_derivatives=None,mechanical_accelerations=None,metric_nodal_rate=None,CMC_preservation=None,temporal_improvement_ports=None,outer_ports=None,activity_outside_0p3_15p1=None,force_scope='known part at saved gauge VALUE jets; eight gradient fields remain symbolic; no acceleration/evolution solution',physical_changes=[]))

def new_D0_packet(force,fixed,cp):
 global RAW,AVAILABLE,GEO,B
 ev=read_pair(force['input'],('r_kpc','z_kpc','xi','weights'));xi,w=ev['xi'],ev['weights'];assert xi.shape==w.shape==(32,) and np.all(xi>0) and np.all(w>0) and np.all(np.diff(xi)>0)
 B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2;omega=SIGMA*xi*fixed['Hunit']/299792458.;assert np.all(np.isfinite(omega)) and np.all(omega>0)
 checkpoint('INPUT',ev,dict(kind='unchanged_sigma1_seed_spectrum_and_actual_force_references',sigma=SIGMA,fixed=fixed,owned_background=cp['background'],force_terminal=FORCE_TERMINAL,force_saved_audit_sha256=FORCE_SAVED_AUDIT_SHA,new_source_terms=False,ordinary_source_location_jets=None,physical_history=None))
 RAW={};AVAILABLE={};start=len(CHECKS);fresh_d0_momentum_fixtures(xi,w,omega);assert len(CHECKS)-start==9
 checkpoint('FIXTURE',dict(RAW,**AVAILABLE),dict(kind='nine_fresh_analytic_D0_configuration_connection_gauge_controls',controls=CHECKS[start:],synthetic_only=True,physical_acceleration_selected=False))
 RAW={};AVAILABLE={};geo=read_pair(force['basis'],tuple(force['basis']['metadata']['schema']));GEO=dict(R=geo['geometry_R'],dv=geo['geometry_dv'],hats=geo['geometry_hats'],cell_i=geo['geometry_cell_i'],cell_j=geo['geometry_cell_j'],r=geo['r_kpc'],z=geo['z_kpc'])
 assert GEO['R'].shape==GEO['dv'].shape==(4,3784) and np.all(GEO['R']>0) and np.all(GEO['dv']>0) and np.array_equal(geo['native_independent_mask'],native_mask())
 checkpoint('BASIS',geo,dict(kind='unchanged_time_independent_native_and_regular_metric_Q1_basis',parent=force['basis'],native_basis=380292,metric_basis=23048,nodal_metric_rate_selected=False,physical_outer_trace=None))
 columns=[D0_seed_column(iq,rec,xi,w,omega) for iq,rec in enumerate(force['columns'])];load=D0_weak_assembly(columns,force);assert len(CHECKS)==EXPECTED_CONTROLS
 return dict(sigma=SIGMA,status='CONDITIONAL_D0_KNOWN_FORCE_WEAK_ARITHMETIC_PASS',columns=[x['record'] for x in columns],loads=load,qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS,'Root-only guarded execution after FULL admission'
 assert PROTOCOL_SHA and len(PROTOCOL_SHA)==64 and sha(path(STEM+'.md'))==PROTOCOL_SHA
 assert not list(BASE.glob(STEM+'_*')),'Unused runtime namespace required'
 INPUTS={str(path(STEM+'.md').resolve()):PROTOCOL_SHA,str(Path(__file__).resolve()):sha(__file__)};OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=sha(__file__))
 json_file(STEM+'_OWNER_START.json',OWNER)
 try:
  import numpy as np_local
  np=np_local
  pins,force,fixed,cp=force_success_admission()
  for name,h in PINS.items():
   key=str(path(name).resolve());assert sha(path(name))==h and (key not in pins or pins[key]==h);pins[key]=h
  for key,h in pins.items():assert key not in INPUTS or INPUTS[key]==h;INPUTS[key]=h
  json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(sigma=SIGMA,modes=32,columns=4,points=15136,gauge_first=12,gauge_primary_second=4,controls=EXPECTED_CONTROLS,pairs=8,tolerance=TOL,floor=1e-30,physical_history=None,physical_phi_tt=None,ordinary_pdot=None,new_source_terms=False),qualification=FLAGS))
  case=new_D0_packet(force,fixed,cp);assert len(RECORDS)==8 and len(CHECKS)==EXPECTED_CONTROLS and all(x['passed'] for x in CHECKS)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_D0_KNOWN_FORCE_WEAK_ARITHMETIC_PASS',cases=[case],controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));recheck()
  json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=OUTPUTS,result_sha256=rh,error_sha256=None,qualification=FLAGS));return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:
   if np is not None and (RAW or AVAILABLE):checkpoint('ERROR_RAW',dict(RAW,**AVAILABLE),dict(context=dict(CONTEXT),controls=CHECKS),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:recheck(strict=False)
  except BaseException:close_error=traceback.format_exc()
  seal_actual();eh=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),unqualified_npz=[p.name for p in BASE.glob(STEM+'*.npz') if p.name not in {r['file'] for r in RECORDS}],qualification=FLAGS))
  json_file(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=OUTPUTS,result_sha256=None,error_sha256=eh,qualification=FLAGS));return 1

if __name__=='__main__':raise SystemExit(main())
