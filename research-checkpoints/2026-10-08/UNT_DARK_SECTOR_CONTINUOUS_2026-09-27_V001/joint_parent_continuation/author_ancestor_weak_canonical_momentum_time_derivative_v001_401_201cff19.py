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
B=None;TOL=2e-11;EXPECTED_CONTROLS=None
np=None;GEO=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(momentum_time_derivative_qualified=False,force_convective_qualified=False,CMC_qualified=False,physical_metric_qualified=False,history_qualified=False,exterior_qualified=False,source_qualified=False,galaxy_velocity_qualified=False)
PINS={'author_fragment_weak_momentum_time_derivative_v002.py':'ac627a75c27b5e1e306017d3c6ae0d599de2e72580c86206a6c27f71ab9d3155','CROSS_U_WEAK_CANONICAL_MOMENTUM_NO_ACCELERATION_DERIVATIVE_V001.md':'c7da6054e73dd1c696876aa7e6d51d3151e5b925ac82769b798a2286f1d46c51'}
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

