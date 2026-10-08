"""Guarded current genuine-nodal lapse/shift weak constraint coefficients. Definitions only."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_CURRENT_CANONICAL_NODAL_NORMAL_CONSTRAINTS_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
NODAL_TERMINAL=dict(owner_pid=None,source_sha256=None,protocol_sha256=None,result_sha256=None,receipt_sha256=None)
SIGMA=1.;C=1.98;KB=.02;ALPHA=KB/C;ELL=.1;GC=3*math.pi/8
B=None;TOL=2e-11;EXPECTED_CONTROLS=None
np=None;GEO=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS=dict(normal_constraints_qualified=False,primary_gauge_qualified=False,physical_CMC_qualified=False,evolution_qualified=False,physical_metric_qualified=False,source_history_qualified=False,exterior_qualified=False,galaxy_velocity_qualified=False)
PINS={
 'CROSS_U_CURRENT_CANONICAL_LAPSE_SHIFT_WEAK_CONSTRAINT_EXTENSION_V001.md':'4e2218acd0b89e01ef22e225399128ff315b44fdd18e04b2c7743e925a7bbf0e',
 'author_fragment_current_lapse_shift_configuration_lift_v001.txt':'5318aba4d814654f390803439e3ec1935010c7ce7aea8c15eec9333a07c6ab91',
 'cross_u_weak_canonical_spatial_euler_loads_v003.py':'4f239074b5345709f493b3633f7dd376fa7ac97dbb23bf20825eabde2ed56b79',
 'cross_u_weak_nodal_metric_temporal_cmc_v001.py':'e11bb7ec123971998fbdd64d1e2171627aae9202804d1c625202f412b5f85b6c',
 'author_fragment_spatial_euler_v002_momentum_envelopes.txt':'c333059f668027a34b4f17d566aca5d6202e7b9ab290956513288efbd34268d3'}

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

def phase_metric_direction(s,q,P,PX,X):
 dhi=-np.einsum('pac,pcd,pdb->pab',s['hi'],q,s['hi']);dX=-np.einsum('pa,pab,pb->p',s['phi'],dhi,s['phi'])/(2*X)
 lm=np.einsum('pab,pba->p',s['hi'],q)/2
 terms=np.column_stack((PX*dX,P*lm));env=np.column_stack((abs(PX)*np.einsum('pa,pab,pb->p',abs(s['phi']),abs(dhi),abs(s['phi']))/(2*X),abs(P)*np.einsum('pab,pba->p',abs(s['hi']),abs(q))/2))
 return terms,env

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

def point_metric_tensor(k):
 # k represents a symmetric metric VELOCITY; offdiagonal k values are actual hdot_ij.
 out=np.zeros(k.shape[:-1]+(3,3));out[...,0,0]=k[...,0];out[...,1,1]=k[...,1];out[...,2,2]=k[...,2]
 for a,(i,j) in enumerate(((0,1),(0,2),(1,2)),3):out[...,i,j]=out[...,j,i]=k[...,a]
 return out

def tensor_velocity_coordinates(hdot):
 return np.stack((hdot[...,0,0],hdot[...,1,1],hdot[...,2,2],hdot[...,0,1],hdot[...,0,2],hdot[...,1,2]),axis=-1)

def tensor_momentum_coordinates(pi):
 return np.stack((pi[...,0,0],pi[...,1,1],pi[...,2,2],2*pi[...,0,1],2*pi[...,0,2],2*pi[...,1,2]),axis=-1)
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

def connection_from_jet(hi,dg):
 p=len(hi);out=np.zeros((p,4,4,4))
 for a in range(4):
  for b in range(4):out[:,:,a,b]=np.einsum('plm,pm->pl',hi,dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b])/2
 return out

def native_velocity_jet(s,c,y,k):
 # y has 99 reduced field velocities; k has six symmetric hdot coefficients.
 p=len(s['U']);y=np.broadcast_to(y,(p,99));k=np.broadcast_to(k,(p,6))
 du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4));dg=np.zeros((p,4,4,4))
 du[:,0]=np.einsum('pai,pi->pa',c['JU'],y[:,:3])+np.einsum('pka,pk->pa',c['Uh'],k)
 dz[:,:,0,1:]=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 dz[:,:,0,0]=np.einsum('jpi,pi->jp',c['JzU'],y[:,:3])+np.einsum('pi,jpi->jp',c['Jzz'],dz[:,:,0,1:])+np.einsum('jpk,pk->jp',c['zh'],k)
 dg[:,0]=np.einsum('pk,pkab->pab',k,c['embed'])
 return du,dz,dg,connection_from_jet(s['hi'],dg)

def connection_from_jet_envelope(hi,dg):
 # hi is the saved inverse. dg may be the actual signed metric first jet OR
 # a previously propagated nonnegative envelope for that jet's construction.
 # Bound the three Christoffel summands BEFORE their +/- cancellation.
 p=len(hi);out=np.zeros((p,4,4,4));eh=abs(hi);ed=abs(dg)
 for a in range(4):
  for b in range(4):
   terms=ed[:,a,b,:]+ed[:,b,a,:]+ed[:,:,a,b]
   out[:,:,a,b]=np.einsum('plm,pm->pl',eh,terms)/2
 RAW['operation_connection_jet_envelope']=out.copy()
 return out

def velocity_operation_envelopes(s,c,y,k,chartenv):
 p=len(s['U']);y=abs(np.broadcast_to(y,(p,99)));k=abs(np.broadcast_to(k,(p,6)))
 e=abs(metric_basis());up=chartenv['up'];N,ga=c['N'],c['gamma']
 edga=np.einsum('pi,kij,pj->pk',up,e,up)/(2*ga[:,None])
 eUh=np.empty_like(c['Uh']);eUh[:,:,0]=edga/N[:,None]
 eUh[:,:,1:]=np.einsum('pij,kjl,pl->pki',abs(c['ih']),e,up)+abs(c['beta'])[:,None,:]*eUh[:,:,0,None]
 RAW['assembling_envelope_U_metric_chain']=eUh.copy()
 ezh=np.einsum('jpa,pka->jpk',abs(s['z']),eUh)/abs(s['U'][None,:,0,None])
 RAW['assembling_envelope_zt_metric_chain']=ezh.copy()
 embed=np.zeros_like(c['embed']);embed[:,:,1:,1:]=e[None]
 embed[:,:,0,1:]=np.einsum('kij,pj->pki',e,abs(c['beta']));embed[:,:,1:,0]=embed[:,:,0,1:]
 embed[:,:,0,0]=np.einsum('pi,kij,pj->pk',abs(c['beta']),e,abs(c['beta']))
 RAW['assembling_envelope_metric_embedding']=embed.copy()
 du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4));dg=np.zeros((p,4,4,4))
 du[:,0]=np.einsum('pai,pi->pa',chartenv['JU'],y[:,:3])+np.einsum('pka,pk->pa',eUh,k)
 dz[:,:,0,1:]=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 dz[:,:,0,0]=np.einsum('jpi,pi->jp',chartenv['JzU'],y[:,:3])+np.einsum('pi,jpi->jp',chartenv['Jzz'],dz[:,:,0,1:])+np.einsum('jpk,pk->jp',ezh,k)
 dg[:,0]=np.einsum('pk,pkab->pab',k,embed)
 RAW.update(assembling_envelope_du=du.copy(),assembling_envelope_dz=dz.copy(),assembling_envelope_dg=dg.copy())
 Ga=connection_from_jet_envelope(s['hi'],dg)
 RAW['assembling_envelope_delta_connection']=Ga.copy()
 nu=du+np.einsum('pbal,pl->pab',Ga,abs(s['U']))
 nz=dz+np.einsum('plab,jpl->jpab',Ga,abs(s['z']))
 RAW.update(assembling_envelope_nu=nu.copy(),assembling_envelope_nz=nz.copy())
 # P=I+U_cov outer U contains cancellation even when its physical00 entry is0.
 uc=np.einsum('pab,pb->pa',abs(s['g']),abs(s['U']))
 Pe=np.eye(4)[None]+np.einsum('pa,pb->pab',uc,abs(s['U']))
 RAW['assembling_envelope_projector']=Pe.copy()
 qq=np.einsum('pa,jpab->jpb',abs(s['U']),nz)
 V=np.einsum('pab,jpb->jpa',Pe,qq)
 D=np.einsum('pac,jpcd,pbd->jpab',Pe,nz,Pe)
 nuc=np.einsum('pab,pcb->pca',abs(s['g']),nu)
 F=nuc+np.swapaxes(nuc,1,2)
 RAW.update(assembling_envelope_F=F.copy(),assembling_envelope_V=V.copy(),assembling_envelope_D=D.copy())
 return dict(du=du,dz=dz,dg=dg,Gamma=Ga,nu=nu,nz=nz,projector=Pe,F=F,V=V,D=D)
# Definitions only. Caller supplies np, saved current first jets and keep(name,array).
# No source, gauge, canonical preparation, temporal trace or exterior is selected.
def current_lapse_shift_configuration_lift(s,c,cj,f,df,b,db,keep):
 p=len(c['N']);assert f.shape==(p,) and df.shape==(p,4) and b.shape==(p,3) and db.shape==(p,4,3)
 N,h,beta,U,z=c['N'],c['h'],c['beta'],s['U'],s['z'];dN,dh,dbe=cj['dN'],cj['dh'],cj['dbeta']
 out={}
 def put(n,a):
  out[n]=a;keep(n,a);assert a.dtype.kind=='f' and np.all(np.isfinite(a)),n;return a
 q=np.zeros((p,4,4));q[:,0,0]=-2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b);q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:];put('metric',q)
 dq=np.zeros((p,4,4,4));dq[:,:,0,0]=-2*dN*f[:,None]-2*N[:,None]*df+2*np.einsum('pai,pij,pj->pa',dbe,h,b)+2*np.einsum('pi,paij,pj->pa',beta,dh,b)+2*np.einsum('pi,pij,paj->pa',beta,h,db)
 dq[:,:,0,1:]=np.einsum('paij,pj->pai',dh,b)+np.einsum('pij,paj->pai',h,db);dq[:,:,1:,0]=dq[:,:,0,1:];put('metric_partial',dq)
 eta=np.empty_like(U);eta[:,0]=-U[:,0]*f/N;eta[:,1:]=-U[:,0,None]*b-beta*eta[:,0,None];put('U',eta)
 deta=np.empty_like(s['du']);deta[:,:,0]=-s['du'][:,:,0]*f[:,None]/N[:,None]-U[:,0,None]*df/N[:,None]+U[:,0,None]*f[:,None]*dN/N[:,None]**2
 deta[:,:,1:]=-s['du'][:,:,0,None]*b[:,None,:]-U[:,0,None,None]*db-dbe*eta[:,None,0,None]-beta[:,None,:]*deta[:,:,0,None];put('U_partial',deta)
 ez=np.einsum('pa,jpa->jp',eta,z);put('Uz_compensation_numerator',ez)
 zeta=np.zeros_like(z);zeta[:,:,0]=-ez/U[None,:,0];put('z',zeta)
 dez=np.einsum('pab,jpb->jpa',deta,z)+np.einsum('pb,jpab->jpa',eta,s['dz']);put('Uz_compensation_partial_numerator',dez)
 dzeta=np.zeros_like(s['dz']);dzeta[:,:,:,0]=-dez/U[None,:,0,None]+ez[:,:,None]*s['du'][None,:,:,0]/U[None,:,0,None]**2;put('z_partial',dzeta)
 return out

def current_lapse_shift_primary_time_coefficients(s,c):
 # Raw canonical gauge momenta in the identical retained native representative.
 # EH ADM/GHY, P(X) and ordinary Hamiltonian have no gauge-velocity terms.
 # Return signed pieces, not a positivity/tolerance gate; upstream bounds are required.
 N,beta,h,U,z=c['N'],c['beta'],c['h'],s['U'],s['z'];PU,Pi,CC=s['PiU'][:,0],s['Pi'][:,:,0,0],s['connection_momentum'][:,0]
 zl=(z[:,:,0]-np.einsum('pi,jpi->jp',beta,z[:,:,1:]))/N[None]
 nt=c['dens'][:,None]*np.column_stack((-2*N*CC[:,0,0],-U[:,0]*PU[:,0]/N,U[:,0]*np.einsum('pi,pi->p',beta,PU[:,1:])/N,np.einsum('jp,jp->p',Pi,zl)))
 bt=np.stack((2*CC[:,0,0,None]*np.einsum('pi,pij->pj',beta,h),2*np.einsum('pi,pij->pj',CC[:,0,1:],h),-U[:,0,None]*PU[:,1:],np.einsum('jp,jpi->pi',Pi,z[:,:,1:])),axis=-1)*c['dens'][:,None,None]
 return dict(lapse_terms=nt,shift_terms=bt,lapse=nt.sum(axis=1),shift=bt.sum(axis=2))

def reconstruct_admitted_current_seed(old_s,old_c,old_cj,old_rates,y,k,xi,w,omega):
 # The caller has admitted BOTH original canonical rows and the selected weak
 # trace, before this function may receive any rate. Configuration is unchanged.
 assert y.shape==(3784,99) and k.shape==(3784,6)
 oldy=old_rates['seed_nodal_native_rate'];oldk=tensor_velocity_coordinates(old_rates['seed_metric_L2_rate'])
 dy=y-oldy;dk=k-oldk
 for name,a in dict(admitted_native_rate=y,admitted_metric_rate=k,old_native_rate=oldy,old_metric_L2_rate=oldk,native_rate_difference=dy,metric_rate_difference=dk).items():finite_real(name,a)
 ddu,ddz,ddg,dGa=native_velocity_jet(old_s,old_c,dy,dk)
 for name,a in dict(du_difference=ddu,dz_difference=ddz,metric_partial_difference=ddg,connection_difference=dGa).items():finite_real(name,a)
 # Upstream difference bounds preserve |new|+|old|, not a rounded cancellation.
 _,ce=native_momentum_operation_envelopes(old_s,old_c,'old_reconstruction')
 ve=velocity_operation_envelopes(old_s,old_c,abs(y)+abs(oldy),abs(k)+abs(oldk),ce)
 du=old_s['du']+ddu;finite_real('current_partial_U',du)
 dz=old_s['dz']+ddz;finite_real('current_partial_z',dz)
 Ga=old_s['Ga']+dGa;finite_real('current_connection',Ga)
 edu=abs(old_s['du'])+ve['du'];edz=abs(old_s['dz'])+ve['dz'];eGa=abs(old_s['Ga'])+ve['Gamma']
 for name,a in dict(partial_U=edu,partial_z=edz,connection=eGa).items():finite_real('reconstruction_envelope_'+name,a)
 # This is the ONLY physical native feature evaluation at this new first jet.
 s=features(old_s['g'],old_s['hi'],Ga,old_s['U'],du,old_s['z'],dz,old_s['phi'],omega,xi,w)
 egp=np.einsum('plam,pln->pamn',eGa,abs(s['g']));edg=egp+egp.swapaxes(2,3)
 s['connection_envelope']=eGa;s['metric_partial_envelope']=edg
 finite_real('current_metric_partial_operation_envelope',edg)
 for name in ('R','Z_coordinate','phase_P','phase_PX','phase_PXX','phase_X'):s[name]=old_s[name]
 c=dict(old_c);c['old_velocity']=y.copy();c['K']=c['N'][:,None,None]*Ga[:,0,1:,1:]
 c['Ktrace']=np.einsum('pij,pij->p',c['ih'],c['K'])
 ku=np.einsum('pik,pkl,plj->pij',c['ih'],c['K'],c['ih'])
 c['pi_EH']=c['sqrt_h'][:,None,None]*(ku-c['Ktrace'][:,None,None]*c['ih'])/(2*C)
 for name in ('K','Ktrace','pi_EH'):finite_real('current_chart_'+name,c[name])
 cj=chart_spacetime_jets(s,c)
 CC,Cn,Cm=connection_momentum(s)
 for name,a in dict(connection_momentum=CC,connection_D=Cn,connection_Maxwell=Cm).items():s[name]=a;finite_real('current_'+name,a)
 py,pm=reduced_momenta(s,c);finite_real('current_native_momentum',py);finite_real('current_native_metric_momentum',pm)
 total=pm+tensor_momentum_coordinates(c['pi_EH']);finite_real('current_total_metric_momentum',total)
 phase=-s['phase_PX'][:,None]*raise_cov(s['hi'],s['phi'])/s['phase_X'][:,None]-raise_cov(s['hi'],s['r'])
 finite_real('current_phase_current',phase);pp=c['dens']*phase[:,0];finite_real('current_phase_momentum',pp)
 # Recompute positive readout bounds from the primitive reconstruction operations.
 se=dict(s,du=edu,dz=edz,Ga=eGa);_,op=native_momentum_operation_envelopes(se,c,'new_reconstruction')
 return s,c,cj,dict(native=py,metric_native=pm,metric_EH=c['pi_EH'],metric_total=total,phase_current=phase,phase_momentum=pp),op

def current_reference_curvature(s,c,cj):
 # Q and V are COORDINATE DENSITIES, already containing cylindrical R.
 # sqrt(h)R3 = Q + partial_i V^i for the fixed flat cylindrical reference.
 R=s['R'];dh=cj['dh'][:,1:];edh=s['metric_partial_envelope'][:,1:,1:,1:];ih=c['ih'];p=len(R)
 G=np.zeros((p,3,3,3));eG=np.zeros_like(G)
 for i in range(3):
  for j in range(3):
   terms=dh[:,i,j,:]+dh[:,j,i,:]-dh[:,:,i,j]
   G[:,:,i,j]=np.einsum('plm,pm->pl',ih,terms)/2
   eG[:,:,i,j]=np.einsum('plm,pm->pl',abs(ih),edh[:,i,j,:]+edh[:,j,i,:]+edh[:,:,i,j])/2
 bar=np.zeros_like(G);bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 cc=G-bar;ec=eG+abs(bar)
 first=np.einsum('pij,pkil,pljk->p',ih,cc,cc);second=np.einsum('pij,pkij,plkl->p',ih,cc,cc)
 Q=c['sqrt_h']*(first-second)
 V=c['sqrt_h'][:,None]*(np.einsum('pij,pkij->pk',ih,cc)-np.einsum('pik,plil->pk',ih,cc))
 eQ=c['sqrt_h']*(np.einsum('pij,pkil,pljk->p',abs(ih),ec,ec)+np.einsum('pij,pkij,plkl->p',abs(ih),ec,ec))
 eV=c['sqrt_h'][:,None]*(np.einsum('pij,pkij->pk',abs(ih),ec)+np.einsum('pik,plil->pk',abs(ih),ec))
 out=dict(Gamma3=G,reference_Gamma3=bar,C3=cc,envelope_C3=ec,Q_terms=c['sqrt_h'][:,None]*np.column_stack((first,-second)),Q=Q,V=V,envelope_Q=eQ,envelope_V=eV)
 for name,a in out.items():finite_real('reference_curvature_'+name,a)
 return out

def current_EH_lapse_shift_direction(s,c,cj,curvature,f,df,b,db):
 # Same ADM/GHY time representative as the admitted canonical metric momentum.
 # Test time derivatives do not enter this representative. No time ports are set0.
 K,ih,N,sh=c['K'],c['ih'],c['N'],c['sqrt_h'];kt=c['Ktrace']
 ku=np.einsum('pik,pkl,plj->pij',ih,K,ih);k2=np.einsum('pij,pij->p',K,ku)
 lapse_curv=(f*curvature['Q']-np.einsum('pi,pi->p',df[:,1:],curvature['V']))/(2*C)
 lapse_kin=f*sh*(kt**2-k2)/(2*C)
 Lie=np.einsum('pi,pijk->pjk',b,cj['dh'][:,1:])+np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])
 shift=-np.einsum('pij,pij->p',c['pi_EH'],Lie)
 eLie=np.einsum('pi,pijk->pjk',abs(b),s['metric_partial_envelope'][:,1:,1:,1:])+np.einsum('pik,pjk->pij',abs(c['h']),abs(db[:,1:]))+np.einsum('pkj,pik->pij',abs(c['h']),abs(db[:,1:]))
 eK=N[:,None,None]*s['connection_envelope'][:,0,1:,1:]
 eku=np.einsum('pik,pkl,plj->pij',abs(ih),eK,abs(ih));ekt=np.einsum('pij,pij->p',abs(ih),eK)
 epi=sh[:,None,None]*(eku+ekt[:,None,None]*abs(ih))/(2*C)
 env=np.column_stack(((abs(f)*curvature['envelope_Q']+np.einsum('pi,pi->p',abs(df[:,1:]),curvature['envelope_V']))/(2*C),abs(f)*sh*(ekt**2+np.einsum('pij,pij->p',eK,eku))/(2*C),np.einsum('pij,pij->p',epi,eLie)))
 terms=np.column_stack((lapse_curv,lapse_kin,shift))
 for name,a in dict(terms=terms,envelope=env,Lie_test_h=Lie,envelope_Lie_test_h=eLie).items():finite_real('current_EH_direction_'+name,a)
 return terms,env

def current_primary_operation_envelope(s,c,op):
 # Canonical gauge-time bound from Pi/PiU/connection contractions BEFORE any
 # lowering, projector or metric connection cancellations.
 U,z,hi=s['U'],s['z'],s['hi'];epi=op['Pi'];sym=(epi+epi.swapaxes(2,3))/2
 eK=np.einsum('pl,pa,pb->plab',op['Z'],abs(U),abs(U))+np.einsum('jpab,jpl->plab',sym,abs(z))
 eKup=np.einsum('plm,pmab->plab',abs(hi),eK)
 eD=(eKup.transpose(0,2,1,3)+eKup.transpose(0,2,3,1)+eKup)/2
 eFup=np.einsum('pac,pcd,pdb->pab',abs(hi),op['F'],abs(hi))
 eMx=ALPHA*(eFup[:,:,:,None]*abs(U)[:,None,None,:]+eFup[:,:,None,:]*abs(U)[:,None,:,None])/2
 eCC=eD+eMx;N,beta,h=c['N'],c['beta'],c['h'];p=len(N);env=np.zeros((p,4))
 for row in range(4):
  eeta=np.zeros((p,4));eq=np.zeros((p,4,4))
  if row==0:
   eq[:,0,0]=2*N;eeta[:,0]=abs(U[:,0])/N;eeta[:,1:]=abs(beta)*eeta[:,0,None]
  else:
   i=row-1;eq[:,0,0]=2*np.einsum('pi,pi->p',abs(beta),abs(h[:,:,i]));eq[:,0,1:]=abs(h[:,:,i]);eq[:,1:,0]=eq[:,0,1:];eeta[:,i+1]=abs(U[:,0])
  ez=np.einsum('pa,jpa->jp',eeta,abs(z))/abs(U[None,:,0])
  env[:,row]=c['dens']*(np.einsum('pab,pab->p',eCC[:,0],eq)+np.einsum('pa,pa->p',op['PiU'][:,0],eeta)+np.einsum('jp,jp->p',epi[:,:,0,0],ez))
 for name,a in dict(connection=eCC,connection_Klo=eK,connection_raised_Klo=eKup,metric_gauge_time=env).items():finite_real('primary_operation_'+name,a)
 return env

def current_normal_coefficient_fields(s,c,cj,op):
 p=len(s['U']);curvature=current_reference_curvature(s,c,cj)
 # rows=(N,betaR,betaZ,betaphi), jets=(value,R,Z,time).
 components=np.zeros((p,4,4,4));envelope=np.zeros_like(components)
 for row in range(4):
  for jet,axis in enumerate((None,1,2,0)):
   f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
   if row==0:
    if axis is None:f[:]=1
    else:df[:,axis]=1
   else:
    if axis is None:b[:,row-1]=1
    else:db[:,axis,row-1]=1
   label=f'normal_{row}_{jet}';lift=current_lapse_shift_configuration_lift(s,c,cj,f,df,b,db,lambda name,a:capture(label+'_'+name,a))
   nt,ne,_=metric_native(s,lift['metric'],lift['metric_partial'],lift['U'],lift['U_partial'])
   zt,ze,*_=variation(s,np.zeros_like(s['U']),np.zeros_like(s['du']),lift['z'],lift['z_partial'])
   pt,pe=phase_metric_direction(s,lift['metric'],s['phase_P'],s['phase_PX'],s['phase_X'])
   et,ee=current_EH_lapse_shift_direction(s,c,cj,curvature,f,df,b,db)
   components[:,row,jet]=np.column_stack((c['dens']*nt.sum(axis=1),c['dens']*zt.sum(axis=1),c['dens']*pt.sum(axis=1),et.sum(axis=1)))
   envelope[:,row,jet]=np.column_stack((c['dens']*ne.sum(axis=1),c['dens']*ze.sum(axis=1),c['dens']*pe.sum(axis=1),ee.sum(axis=1)))
   for name,a in dict(native_terms=nt,mode_compensation_terms=zt,absolute_phase_terms=pt,EH_terms=et).items():capture(label+'_'+name,a)
   capture('normal_components_partial',components);capture('normal_component_envelope_partial',envelope)
   assert np.all(np.isfinite(components[:,row,jet])) and np.all(np.isfinite(envelope[:,row,jet]))
 coefficient=components.sum(axis=-1);ecoefficient=envelope.sum(axis=-1)
 primary=current_lapse_shift_primary_time_coefficients(s,c);signed=np.column_stack((primary['lapse'],primary['shift']));eprimary=current_primary_operation_envelope(s,c,op)
 for name,a in dict(coefficient=coefficient,envelope=ecoefficient,components=components,component_envelope=envelope,primary_signed=signed,primary_operation_envelope=eprimary,lapse_primary_terms=primary['lapse_terms'],shift_primary_terms=primary['shift_terms']).items():finite_real('current_normal_'+name,a)
 check('four_time_test_coefficients_equal_canonical_primary',coefficient[:,:,3],signed,ecoefficient[:,:,3]+eprimary)
 check('four_primary_gauge_momenta_vanish',signed,np.zeros_like(signed),eprimary)
 return dict(coefficient=coefficient,envelope=ecoefficient,components=components,component_envelope=envelope,primary=signed,primary_envelope=eprimary,curvature=curvature)

def normal_test_mask():
 # All four coefficient fields are axis-even; betaR=R*coefficient is smooth.
 # betaZ is odd across the sheet. Outer test values vanish, not physical fields.
 m=np.ones((4,87,45),dtype=bool);m[:,0]=False;m[:,-1]=False;m[:,:,-1]=False;m[2,:,0]=False
 return m

def extend_normal_tests(a):
 assert a.shape==(4,87,45)
 out=a.copy();out[:,0]=out[:,1];out[:,-1]=0;out[:,:,-1]=0;out[2,:,0]=0
 return out

def restrict_normal_rows(a):
 assert a.shape==(4,87,45)
 out=a.copy();out[:,1]+=out[:,0];out[:,0]=0;out[:,-1]=0;out[:,:,-1]=0;out[2,:,0]=0
 return out

def normal_hat_jet(geo,iq,corner,row):
 N,NR,NZ=geo['hats'][iq,corner];R=geo['R'][iq].reshape(86,44)
 if row==1:return (R*N,R*NR+N,R*NZ)
 return (N,NR,NZ)

def evaluate_normal_test(a,geo):
 a=extend_normal_tests(a);out=np.zeros((15136,4,3))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    av=a[row,i:86+i,j:44+j]
    for jet,h in enumerate(normal_hat_jet(geo,iq,corner,row)):out[sl,row,jet]+=(av*h).reshape(3784)
 return out

def scatter_normal_action(coeff,geo):
 # coeff is a COORDINATE density. The quadrature measure is dv/R exactly once.
 assert coeff.shape==(15136,4,3)
 out=np.zeros((4,87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for corner,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    val=sum(coeff[sl,row,k].reshape(86,44)*h for k,h in enumerate(normal_hat_jet(geo,iq,corner,row)))
    out[row,i:86+i,j:44+j]+=wq*val
 return restrict_normal_rows(out)

def scatter_normal_action_independent(coeff,geo):
 assert coeff.shape==(15136,4,3);out=np.zeros((4,87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);R=geo['R'][iq];wq=geo['dv'][iq]/R
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hs=geo['hats'][iq,corner].reshape(3,3784).T
   for row in range(4):
    basis=hs.copy()
    if row==1:basis=hs*R[:,None];basis[:,1]+=hs[:,0]
    val=wq*np.sum(coeff[sl,row]*basis,axis=1)
    np.add.at(out[row],(geo['cell_i']+di,geo['cell_j']+dj),val)
 return restrict_normal_rows(out)

def ordinary_normal_rows(source,gamma):
 # The authoritative ordinary gamma belongs to the same authenticated g,p,
 # order and mass labels. These rows do not reset velocity or source history.
 R=source['source_R'];Z=source['source_Z'];mass=source['source_mass_weight'];p=source['source_specific_covariant_p'];i=source['source_indices'];t=source['source_right_weight']
 assert gamma.shape==R.shape and p.shape==(len(R),3) and np.all(gamma>=1) and np.all(mass>=0)
 assert i.dtype.kind=='i' and np.all((i>=0)&(i<86)) and np.all((t>=0)&(t<=1)) and np.all(Z==0)
 force=mass[:,None]*np.column_stack((gamma,-p))
 # Hamiltonian normal/shift signs; the action contribution is minus this row.
 out=np.zeros((4,87,45));env=np.zeros_like(out)
 for side,hat in ((0,1-t),(1,t)):
  for row in range(4):
   scale=R if row==1 else np.ones_like(R)
   val=force[:,row]*scale*hat
   np.add.at(out[row,:,0],i+side,val);np.add.at(env[row,:,0],i+side,abs(val))
 out=restrict_normal_rows(out);env=restrict_normal_rows(env)
 for name,a in dict(ordinary_Hamiltonian_normal_point=force,ordinary_Hamiltonian_normal_nodal=out,ordinary_Hamiltonian_normal_envelope=env,ordinary_gamma=gamma).items():finite_real(name,a)
 return out,env

def reference_curvature_fixtures():
 # Independent first-jet cylindrical identities, no strong second derivatives.
 R=np.array((3.,));one=np.ones(1);zero=np.zeros((1,4));h=np.diag((1.,1.,9.))[None];ih=np.diag((1.,1.,1/9))[None]
 dh=np.zeros((1,4,3,3));dh[:,1,2,2]=2*R
 Ga=np.zeros((1,4,4,4));Ga[:,1,3,3]=-R;Ga[:,3,1,3]=Ga[:,3,3,1]=1/R
 g=np.zeros((1,4,4));g[:,0,0]=-1;g[:,1:,1:]=h
 ep=np.einsum('plam,pln->pamn',abs(Ga),abs(g));ep+=ep.swapaxes(2,3)
 s=dict(R=R,metric_partial_envelope=ep,connection_envelope=abs(Ga));cj=dict(dh=dh)
 c=dict(h=h,ih=ih,sqrt_h=R,N=one,beta=np.zeros((1,3)),K=np.zeros((1,3,3)),Ktrace=np.zeros(1),pi_EH=np.zeros((1,3,3)))
 flat=current_reference_curvature(s,c,cj)
 check('flat_cylindrical_reference_Q_and_V_zero',np.column_stack((flat['Q'],flat['V'])),np.zeros((1,4)),np.column_stack((flat['envelope_Q'],flat['envelope_V'])))
 # varphi=5/4, grad ln(varphi)=(2/7,-1/5,0) are fresh local rational jets.
 ph=5/4;l=np.array((2/7,-1/5,0.));hc=ph**4*h;ihc=ih/ph**4
 dhc=dh*ph**4
 for axis in range(3):dhc[:,axis+1]+=4*l[axis]*hc
 gc=g.copy();gc[:,1:,1:]=hc;Gac=connection_from_jet(np.linalg.inv(gc),np.pad(dhc,((0,0),(0,0),(1,0),(1,0))))
 ec=np.einsum('plam,pln->pamn',abs(Gac),abs(gc));ec+=ec.swapaxes(2,3)
 sc=dict(s,metric_partial_envelope=ec,connection_envelope=abs(Gac));cc=dict(c,h=hc,ih=ihc,sqrt_h=ph**6*R);cjc=dict(dh=dhc)
 curved=current_reference_curvature(sc,cc,cjc)
 expected_Q=8*R*ph**2*np.sum(l*l);expected_V=-8*R[:,None]*ph**2*l[None]
 check('conformal_cylindrical_Q_and_V_first_jet',np.column_stack((curved['Q'],curved['V'])),np.column_stack((expected_Q,expected_V)),np.column_stack((curved['envelope_Q'],curved['envelope_V']))+abs(np.column_stack((expected_Q,expected_V))))
 f=np.array((7/6,));df=zero.copy();df[:,1]=1/9;df[:,2]=-2/11;b=np.zeros((1,3));db=np.zeros((1,4,3))
 terms,env=current_EH_lapse_shift_direction(sc,cc,cjc,curved,f,df,b,db)
 target=4*R*ph**2*(f*np.sum(l*l)+np.sum(df[:,1:]*l[None],axis=1))/C
 check('conformal_compact_lapse_weak_curvature',terms[:,0],target,env[:,0]+abs(target))
 H=2/13;ck=dict(c,K=H*h,Ktrace=3*H*one,pi_EH=-R[:,None,None]*H*ih/C)
 # Nonzero isotropic temporal connection is part of this synthetic first jet.
 sk=dict(s,connection_envelope=abs(Ga));sk['connection_envelope']=sk['connection_envelope'].copy();sk['connection_envelope'][:,0,1:,1:]=H*h
 b[:,0]=3/11;db[:,1,0]=2/17;db[:,2,1]=-1/19
 terms,env=current_EH_lapse_shift_direction(sk,ck,cj,flat,f,zero,b,db)
 targets=np.column_stack((-3*R*H**2*f/C,2*H*(b[:,0]+R*(db[:,1,0]+db[:,2,1]))/C))
 check('ADM_lapse_kinetic_and_isotropic_shift_divergence',terms[:,1:],targets,env[:,1:]+abs(targets))

def native_normal_fixtures(xi,w,omega):
 # Fresh Cartesian first jet. All32 modes are nonzero, and the N_R target
 # independently tests the acceleration.Z lapse-gradient contact.
 u=3/4;gamma=5/4;X=2/5;P=7/13;PX=11/17
 g=np.diag((-1.,1.,1.,1.))[None];hi=g.copy();Ga=np.zeros((1,4,4,4));U=np.array(((gamma,u,0.,0.),));du=np.zeros((1,4,4))
 zr=(B*GC)*xi**2*(np.arange(1.,33.)/1024);z=np.zeros((32,1,4));z[:,0,1]=zr;z[:,0,0]=-u*zr/gamma;dz=np.zeros((32,1,4,4));phi=np.array(((X,0.,0.,0.),))
 s=features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w);s.update(phase_P=np.array((P,)),phase_PX=np.array((PX,)),phase_X=np.array((X,)))
 JU=np.zeros((1,4,3));JU[:,0,0]=u/gamma;JU[:,1:]=np.eye(3)[None]
 Jzu=-np.einsum('jpa,pai->jpi',z,JU)/gamma
 c=dict(N=np.ones(1),beta=np.zeros((1,3)),h=np.eye(3)[None],ih=np.eye(3)[None],gamma=np.array((gamma,)),up=np.array(((u,0.,0.),)),JU=JU,JzU=Jzu,Jzz=np.array(((-u/gamma,0.,0.),)),dens=np.ones(1))
 cj=dict(dN=np.zeros((1,4)),dh=np.zeros((1,4,3,3)),dbeta=np.zeros((1,4,3)))
 s['connection_momentum']=connection_momentum(s)[0];_,op=native_momentum_operation_envelopes(s,c,'fresh_normal')
 ep=current_primary_operation_envelope(s,c,op);actual=[];envelopes=[]
 for axis in (None,1,2,0):
  f=np.zeros(1);df=np.zeros((1,4));b=np.zeros((1,3));db=np.zeros((1,4,3))
  if axis is None:f[:]=1
  else:df[:,axis]=1
  lift=current_lapse_shift_configuration_lift(s,c,cj,f,df,b,db,lambda n,a:capture('fresh_native_normal_'+str(axis)+'_'+n,a))
  mt,me,_=metric_native(s,lift['metric'],lift['metric_partial'],lift['U'],lift['U_partial'])
  zt,ze,*_=variation(s,np.zeros_like(U),np.zeros_like(du),lift['z'],lift['z_partial'])
  pt,pe=phase_metric_direction(s,lift['metric'],s['phase_P'],s['phase_PX'],s['phase_X'])
  actual.append((mt.sum(axis=1)+zt.sum(axis=1)+pt.sum(axis=1))[0]);envelopes.append((me.sum(axis=1)+ze.sum(axis=1)+pe.sum(axis=1))[0])
 q=zr**2/gamma**2;kj=(B*GC)**2*xi**4
 target=np.array((P-PX*X+u*u*X*X/2-np.sum(w*(q/2+q*q/(4*kj))),np.sum(w*zr),0.,0.))
 env=np.asarray(envelopes)+abs(target);env[3]+=ep[0,0]
 check('tilted_fixed_covector_lapse_value_gradient_and_time_contacts',np.asarray(actual),target,env)
 primary=current_lapse_shift_primary_time_coefficients(s,c);signed=np.column_stack((primary['lapse'],primary['shift']))
 check('fresh_four_canonical_gauge_primary_contacts',signed,np.zeros_like(signed),ep)
 # Independent material normal/shift signs at fixed covariant p and rest mass.
 mass=2/7;p=np.array((3/4,0.,0.));G=5/4;force=mass*np.r_[G,-p]
 check('fixed_mass_and_covariant_p_ordinary_normal_shift_signs',force,np.array((5/14,-3/14,0.,0.)),abs(force)+np.array((5/14,3/14,0.,0.)))

def current_state_first_jet_witnesses(s,c,op,old_phase):
 dg=metric_partial(s);U,z,du,dz=s['U'],s['z'],s['du'],s['dz'];g=s['g']
 unit=np.einsum('pa,pab,pb->p',U,g,U)+1
 uj=np.einsum('pamn,pm,pn->pa',dg,U,U)+2*np.einsum('pab,pbc,pc->pa',du,g,U)
 transverse=np.einsum('pa,jpa->jp',U,z)
 tj=np.einsum('pab,jpb->jpa',du,z)+np.einsum('pb,jpab->jpa',U,dz)
 eu=np.einsum('pa,pab,pb->p',abs(U),abs(g),abs(U))+1
 eud=np.einsum('pamn,pm,pn->pa',s['metric_partial_envelope'],abs(U),abs(U))+2*np.einsum('pab,pbc,pc->pa',AVAILABLE['reconstruction_envelope_partial_U'],abs(g),abs(U))
 et=np.einsum('pa,jpa->jp',abs(U),abs(z))
 etd=np.einsum('pab,jpb->jpa',AVAILABLE['reconstruction_envelope_partial_U'],abs(z))+np.einsum('pb,jpab->jpa',abs(U),AVAILABLE['reconstruction_envelope_partial_z'])
 a=np.concatenate((unit.ravel(),uj.ravel(),transverse.ravel(),tj.ravel()));e=np.concatenate((eu.ravel(),eud.ravel(),et.ravel(),etd.ravel()))
 check('current_genuine_rate_complete_unit_and_transverse_first_jets',a,np.zeros_like(a),e)
 J=-s['phase_PX'][:,None]*raise_cov(s['hi'],s['phi'])/s['phase_X'][:,None]-raise_cov(s['hi'],s['r'])
 eJ=abs(s['phase_PX'])[:,None]*np.einsum('pab,pb->pa',abs(s['hi']),abs(s['phi']))/s['phase_X'][:,None]+np.einsum('pab,pb->pa',abs(s['hi']),np.einsum('pab,pb->pa',op['P'],abs(s['phi'])))
 check('unchanged_configuration_phase_current_inventory',np.column_stack((J,c['dens']*J[:,0])),np.column_stack((old_phase['new_phase_current'],old_phase['new_phase_canonical_density'])),np.column_stack((eJ,c['dens']*eJ[:,0]))+abs(np.column_stack((old_phase['new_phase_current'],old_phase['new_phase_canonical_density']))))

def current_readout_metric_envelope(s,c,op):
 # eC was constructed upstream in current_primary_operation_envelope.
 eCC=AVAILABLE['primary_operation_connection'];e=abs(metric_basis());up=op['up'];N,ga=c['N'],c['gamma']
 eUh=np.empty_like(c['Uh']);eUh[:,:,0]=np.einsum('pi,kij,pj->pk',up,e,up)/(2*N*ga)[:,None]
 eUh[:,:,1:]=np.einsum('pij,kjl,pl->pki',abs(c['ih']),e,up)+abs(c['beta'])[:,None,:]*eUh[:,:,0,None]
 ezh=np.einsum('jpa,pka->jpk',abs(s['z']),eUh)/abs(s['U'][None,:,0,None])
 embed=np.zeros_like(c['embed']);embed[:,:,1:,1:]=e[None];embed[:,:,0,1:]=np.einsum('kij,pj->pki',e,abs(c['beta']));embed[:,:,1:,0]=embed[:,:,0,1:];embed[:,:,0,0]=np.einsum('pi,kij,pj->pk',abs(c['beta']),e,abs(c['beta']))
 native=c['dens'][:,None]*(np.einsum('pab,pkab->pk',eCC[:,0],embed)+np.einsum('pa,pka->pk',op['PiU'][:,0],eUh)+np.einsum('jp,jpk->pk',op['Pi'][:,:,0,0],ezh))
 eK=N[:,None,None]*s['connection_envelope'][:,0,1:,1:];ih=abs(c['ih']);ekt=np.einsum('pij,pij->p',ih,eK);eku=np.einsum('pik,pkl,plj->pij',ih,eK,ih)
 EH=c['sqrt_h'][:,None,None]*(eku+ekt[:,None,None]*ih)/(2*C)
 total=native+tensor_momentum_coordinates(EH)
 for name,a in dict(native=native,EH=EH,total=total,Uh=eUh,zh=ezh,embed=embed).items():finite_real('current_metric_readout_envelope_'+name,a)
 return total
