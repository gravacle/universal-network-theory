"""Guarded saved constrained native ADM momenta and local kinetic admission."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,traceback
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V001'
PARENT='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
ORDINARY='CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001'
PROTOCOL_SHA='daf7b25ced27a951751c463529606bf983b0dc65f221cee8b5432357d849bc12'
PINS={
 'cross_u_saved_full_metric_native_source_residual_v001.py':'23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68',
 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001.md':'88fbf64e1568af3f47f1346b809c6d8a35fe7b685a73817938616b9056068e24',
 PARENT+'_RESULT.json':'ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798',
 PARENT+'_RECEIPT.json':'eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde',
 'cross_u_saved_rotating_sheet_frechet_v001.py':'ab56dd280d6317699fe38e7b5499d1e25b214197b1d3d1db8a598ad271dc72da',
 'CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001.md':'e1ea987af25cf02dab2460e555f59b13691fefee254e83e1789a1c3a28281f05',
 ORDINARY+'_RESULT.json':'e62722bbff40d0f063d3a80e2467b06d7d4d305dd304140efced5add000fe929',
 ORDINARY+'_RECEIPT.json':'f24459d3dfffbfd773323ba69c375ac8f08bda5e121d2f530dc156c1955fb6d7',
 'CROSS_U_CONSTRAINED_CANONICAL_CHART_AND_CMC_ADMISSION_V001.md':'872ca230d040bfca08ac127c117e741e81549a4316e62dd5de8df8e8732f7e98'}
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10
B=A0*KPC/LIGHT**2;C=1.98;KB=.02;ALPHA=KB/C;GC=3*math.pi/8;ELL=.1
SIGMAS=(.1,1.,10.,100.);TOL=2e-11;SAMPLE_COUNT=8;NATIVE_COUNT=99
CONTROL_COUNT=60;PAIR_COUNT=6
np=None;OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];RAW={};ARM_AVAILABLE={};CONTEXT={};CHECKS=[]
FLAGS={k:False for k in ('full_slice_Cauchy_qualified','global_constraint_solution_qualified','CMC_solution_qualified','physical_initial_state_qualified','retarded_formation_history_qualified','physical_native_inertia_qualified','physical_junction_qualified','active_source_mapping_qualified','metric_correction_applied','orbital_force_qualified','observational_qualified','joint_model_adopted')}

def now():return datetime.now(timezone.utc).isoformat()


def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p


def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()


def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [canonical(x) for x in v]
 if np is not None and isinstance(v,np.generic):return canonical(v.item())
 if v is None or type(v) in (str,bool,int):return v
 if type(v) is float and math.isfinite(v):return v
 raise TypeError('Nonfinite or unsupported metadata: '+type(v).__name__)


def encode(v):return (json.dumps(canonical(v),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def publish(n,b):
 p=path(n)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==b;OUTPUTS[n]=sha(p);return OUTPUTS[n]


def json_file(n,v):return publish(n,encode(v))


def array(v,name):
 a=np.asarray(v)
 if a.dtype.kind not in 'fiu' or not np.all(np.isfinite(a)):raise ValueError(name+' must be finite real numeric data.')
 return a.astype(np.float64,copy=False)


def check(name,actual,expected,envelope=None):
 ordinal=len(CHECKS);CONTEXT.update(current_control=name,current_control_ordinal=ordinal)
 a=np.asarray(actual);b=np.asarray(expected);prefix=f'control_{ordinal:03d}_{name}'
 RAW[prefix+'_actual']=a.copy();RAW[prefix+'_expected']=b.copy()
 if envelope is not None:RAW[prefix+'_envelope']=np.asarray(envelope).copy()
 assert a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
 env=max(1e-30,float(np.max(abs(a),initial=0)),float(np.max(abs(b),initial=0))) if envelope is None else max(1e-30,float(np.max(array(envelope,'control envelope'),initial=0)))
 gap=float(np.max(abs(a-b),initial=0));err=gap/env;assert all(math.isfinite(x) for x in (env,gap,err))
 row=dict(ordinal=ordinal,name=name,absolute_gap=gap,envelope=env,error=err,tolerance=TOL,passed=err<=TOL);CHECKS.append(row)
 assert row['passed'],name
 return row


def checkpoint(tag,arrays,meta):
 md=canonical(dict(meta,owner=OWNER,qualification=FLAGS,schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}))
 text=encode(md).decode();md=json.loads(text);name=f'{STEM}_{len(RECORDS):05d}_{tag}.npz';p=path(name)
 with p.open('xb') as f:np.savez_compressed(f,metadata_json=np.array(text),**arrays);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);rec=dict(file=name,sha256=sha(p),metadata=md);cf=name+'.COMMIT.json';ch=json_file(cf,rec)
 rec=dict(rec,commit_file=cf,commit_sha256=ch);OUTPUTS[name]=rec['sha256'];RECORDS.append(rec)
 with np.load(p,allow_pickle=False) as f:
  assert set(f.files)==set(arrays)|{'metadata_json'} and str(f['metadata_json'])==text
  for k,a in arrays.items():assert f[k].dtype==a.dtype and f[k].shape==a.shape and np.array_equal(f[k],a,equal_nan=True)
 return rec


def seal_created():
 for p in sorted(BASE.glob(STEM+'_*')):
  if p.is_file():p.chmod(0o444);OUTPUTS[p.name]=sha(p)


def recheck(strict=True):
 for n,h in INPUTS.items():assert sha(path(n))==h,('Input changed',n)
 assert sha(__file__)==OWNER['source_sha256']
 if strict:assert path(STEM+'_OWNER_START.json').read_bytes()==encode(OWNER)
 for n,h in OUTPUTS.items():assert sha(path(n))==h,('Output changed',n)
 for r in RECORDS:
  assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
  with np.load(path(r['file']),allow_pickle=False) as f:
   assert json.loads(str(f['metadata_json']))==r['metadata'] and set(f.files)==set(r['metadata']['schema'])|{'metadata_json'}
   for k,s in r['metadata']['schema'].items():assert f[k].shape==tuple(s['shape']) and str(f[k].dtype)==s['dtype'] and bool(np.all(np.isfinite(f[k])))==s['finite']
 if strict:
  assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={r['file'] for r in RECORDS}
  assert {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in RECORDS}


def selected_arrays(file,names):
 out={}
 with np.load(path(file),allow_pickle=False) as f:
  for k in names:
   a=f[k].copy();RAW['loaded_'+k]=a
   assert a.dtype==np.dtype('float64') and np.all(np.isfinite(a));out[k]=a
 return out


def scaled_check(name,actual,expected,envelope):
 a=np.asarray(actual);b=np.asarray(expected);e=np.asarray(envelope);assert a.shape==b.shape==e.shape
 scale=np.maximum(e,1e-30);label=f'raw_{len(CHECKS):03d}_{name}'
 RAW[label+'_actual']=a.copy();RAW[label+'_expected']=b.copy();RAW[label+'_envelope']=e.copy();RAW[label+'_scale']=scale.copy()
 return check(name,a/scale,b/scale,np.ones_like(a))


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

def symmetric_tensor_from_coordinates(p):
 t=np.zeros((len(p),3,3));t[:,0,0]=p[:,0];t[:,1,1]=p[:,1];t[:,2,2]=p[:,2]
 for k,(i,j) in enumerate(((0,1),(0,2),(1,2)),start=3):t[:,i,j]=t[:,j,i]=p[:,k]/2
 return t

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

def gauge_velocity_jet(s,c,dN,dbeta):
 p=len(s['U']);dbeta=np.broadcast_to(dbeta,(p,3));dN=np.broadcast_to(dN,(p,))
 dg=np.zeros((p,4,4,4));du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4))
 dg[:,0,0,0]=-2*c['N']*dN+2*np.einsum('pi,pij,pj->p',c['beta'],c['h'],dbeta)
 dg[:,0,0,1:]=np.einsum('pij,pj->pi',c['h'],dbeta);dg[:,0,1:,0]=dg[:,0,0,1:]
 du[:,0,0]=-s['U'][:,0]*dN/c['N'];du[:,0,1:]=-dbeta*s['U'][:,0,None]-c['beta']*du[:,0,0,None]
 dz[:,:,0,0]=-np.einsum('jpa,pa->jp',s['z'],du[:,0])/s['U'][None,:,0]
 return du,dz,dg,connection_from_jet(s['hi'],dg)

def kinetic_tangent(s,du,dz,dGa,ell=ELL):
 dn=du+np.einsum('pbal,pl->pab',dGa,s['U']);dnz=dz-np.einsum('plab,jpl->jpab',dGa,s['z'])
 dV=np.einsum('pab,jpb->jpa',s['P'],np.einsum('pa,jpab->jpb',s['U'],dnz))
 dD=np.einsum('pac,jpcd,pbd->jpab',s['P'],dnz,s['P'])
 dF=lower_last(s['g'],dn)-np.swapaxes(lower_last(s['g'],dn),1,2)
 dFu=np.einsum('pac,pcd,pdb->pab',s['hi'],dF,s['hi'])
 dPiU=-ALPHA*np.einsum('pac,pcb->pab',s['hi'],dF)
 dPi=s['w'][:,None,None,None]*(np.einsum('pa,jpb->jpab',s['U'],raise_cov(s['hi'],dV))/s['omega'][:,None,None,None]**2-ell**2*np.einsum('pac,jpcd,pdb->jpab',s['hi'],dD,s['hi']))
 # Acceleration.Z is linear in all velocities; subtract the constant connection vertex.
 zero=dict(s,Z=np.zeros_like(s['Z']));dC=connection_momentum(zero,dPi,dFu)[0]
 return dict(du=du,dz=dz,dg_connection=dGa,delta_nu=dn,delta_nz=dnz,delta_V=dV,delta_D=dD,delta_F=dF,delta_PiU=dPiU,delta_Pi=dPi,delta_Ctime=dC[:,0])

def kinetic_gram(s,tangents,ell=ELL):
 dF=np.stack([x['delta_F'] for x in tangents]);dV=np.stack([x['delta_V'] for x in tangents]);dD=np.stack([x['delta_D'] for x in tangents])
 hi=s['hi'];w=s['w'];om=s['omega'];dens=np.sqrt(-np.linalg.det(s['g']))
 mx=-ALPHA*np.einsum('Apab,pac,pbd,Bpcd->pAB',dF,hi,hi,dF)/2
 tv=np.einsum('Ajpa,pab,Bjpb->jpAB',dV,hi,dV)/om[:,None,None,None]**2
 td=-ell**2*np.einsum('Ajpab,pac,pbd,Bjpcd->jpAB',dD,hi,hi,dD)
 out=dens[:,None,None]*(mx+np.einsum('j,jpAB->pAB',w,tv+td))
 env=dens[:,None,None]*(ALPHA*np.einsum('Apab,pac,pbd,Bpcd->pAB',abs(dF),abs(hi),abs(hi),abs(dF))/2+np.einsum('j,jpAB->pAB',w,np.einsum('Ajpa,pab,Bjpb->jpAB',abs(dV),abs(hi),abs(dV))/om[:,None,None,None]**2+ell**2*np.einsum('Ajpab,pac,pbd,Bjpcd->jpAB',abs(dD),abs(hi),abs(hi),abs(dD))))
 return out,env

def assemble_kinetic(s,c):
 columns=[];tangents=[]
 for col in range(105):
  y=np.zeros(99);k=np.zeros(6)
  if col<99:y[col]=1
  else:k[col-99]=1
  du,dz,dg,dGa=native_velocity_jet(s,c,y,k);t=kinetic_tangent(s,du,dz,dGa)
  py,ph=reduced_momenta(s,c,t['delta_PiU'],t['delta_Pi'],t['delta_Ctime']);columns.append(np.concatenate((py,ph),axis=1));tangents.append(dict(t,delta_metric_jet=dg))
  ARM_AVAILABLE['assembling_velocity_columns']=np.stack(columns,axis=-1)
  for name in ('delta_F','delta_V','delta_D','delta_PiU','delta_Pi','du','dz'):ARM_AVAILABLE['assembling_'+name]=np.stack([v[name] for v in tangents])
 H=np.stack(columns,axis=-1);ARM_AVAILABLE['assembling_H']=H.copy();G,env=kinetic_gram(s,tangents)
 return H,G,env,tangents

def phase_momentum(s,PX,PXX):
 X=np.sqrt(-covdot(s['hi'],s['phi'],s['phi']));v=-raise_cov(s['hi'],s['phi'])/X[:,None]
 J=PX[:,None]*v-raise_cov(s['hi'],s['r']);dens=np.sqrt(-np.linalg.det(s['g']))
 PU00=s['hi'][:,0,0]+s['U'][:,0]**2
 slope=dens*(PXX*v[:,0]**2-(PX/X)*(s['hi'][:,0,0]+v[:,0]**2)-PU00)
 env=dens*(abs(PXX)*v[:,0]**2+abs(PX/X)*(abs(s['hi'][:,0,0])+v[:,0]**2)+abs(s['hi'][:,0,0])+s['U'][:,0]**2)
 return dens*J[:,0],slope,env,J,X

def ordinary_velocity(g,p):
 hi=np.linalg.inv(g);h=g[:,1:,1:];ih=np.linalg.inv(h);N=1/np.sqrt(-hi[:,0,0]);beta=N[:,None]**2*hi[:,0,1:]
 p=np.asarray(p);pu=np.einsum('pij,pj->pi',ih,p);gamma=np.sqrt(1+np.sum(p*pu,axis=1))
 u=np.column_stack((gamma/N,pu-beta*gamma[:,None]/N[:,None]));coordinate=N[:,None]*pu/gamma[:,None]-beta
 H=N*gamma-np.sum(beta*p,axis=1)
 return dict(u_M=u,coordinate_velocity=coordinate,gamma=gamma,specific_covariant_momentum=p,coordinate_time_Hamiltonian=H)

def phase_inventory(s,W,u,fixed):
 eta=fixed['Hunit']/LIGHT;Q0=fixed['Q0_over_Hstar']*eta;ep=fixed['eps'];norm=1/ep-math.log1p(1/ep)
 assert ep==1e-5 and np.all((u>0)&(u<ep))
 q=np.sqrt(1+u);ss=u/(ep-u);Abar=1.5*fixed['OA']/fixed['rG'];fac=2*eta*eta/C
 X=np.sqrt(-covdot(s['hi'],s['phi'],s['phi']));PX=W/X
 PXX=fac*Abar*(2*ss/(ep*norm)+4*q*q/(norm*(ep-u)**2))/Q0**2
 p,slope,env,J,X=phase_momentum(s,PX,PXX)
 return dict(p_phi=p,phi_velocity_slope=slope,phi_velocity_slope_envelope=env,J_phi=J,X=X,P_X=PX,P_XX=PXX,phase_u=u,phase_clock_domain=(u>0)&(u<ep))

def take_points(s,index):
 return features(s['g'][index],s['hi'][index],s['Ga'][index],s['U'][index],s['du'][index],s['z'][:,index],s['dz'][:,index],s['phi'][index],s['omega'],s['xi'],s['w'])

def momentum_envelope(s,c):
 pu=np.einsum('pa,pai->pi',abs(s['PiU'][:,0]),abs(c['JU']))+np.einsum('jp,jpi->pi',abs(s['Pi'][:,:,0,0]),abs(c['JzU']))
 pz=abs(s['Pi'][:,:,0,1:])+abs(s['Pi'][:,:,0,0,None]*c['Jzz'][None,:,:])
 return c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)

def local_block(s,index,Hbar,label):
 local=take_points(s,index);c=adm_chart(local);p=len(index);base_py,base_ph=reduced_momenta(local,c)
 H,G,env,tangents=assemble_kinetic(local,c)
 M=H[:,:99,:99];mixed=H[:,:99,99:];T=H[:,99:,99:]
 available=dict(sample_indices=np.asarray(index,dtype=np.int64),sample_g=local['g'],sample_hi=local['hi'],sample_Ga=local['Ga'],sample_U=local['U'],sample_z=local['z'],sample_du=local['du'],sample_dz=local['dz'],sample_phi=local['phi'],sample_JU=c['JU'],sample_JzU=c['JzU'],sample_Jzz=c['Jzz'],sample_metric_embedding=c['embed'],sample_U_metric_chain=c['Uh'],sample_zt_metric_chain=c['zh'],sample_density=c['dens'],native_base_momentum=base_py,metric_base_native_momentum=base_ph,kinetic_H=H,kinetic_Gram=G,kinetic_envelope=env,native_M=M,native_metric_B=mixed,native_metric_T=T,EH_metric_Hessian=c['EH_Hessian'],sample_K=c['K'],sample_pi_EH=c['pi_EH'])
 for key in ('du','dz','delta_metric_jet','dg_connection','delta_F','delta_V','delta_D','delta_PiU','delta_Pi','delta_Ctime'):available['velocity_'+key]=np.stack([t[key] for t in tangents])
 ARM_AVAILABLE.update(available)
 for key in list(ARM_AVAILABLE):
  if key.startswith('assembling_'):del ARM_AVAILABLE[key]
 scaled_check(label+'_kinetic_Gram_and_mixed_symmetry',np.stack((H,H)),np.stack((G,np.swapaxes(H,1,2))),np.stack((env,env+np.swapaxes(env,1,2))))
 direct=[];direct_env=[]
 for k in range(6):
  dq=np.zeros((p,4,4,4));dq[:,0]=c['embed'][:,k];du=np.zeros((p,4,4));du[:,0]=c['Uh'][:,k];dz=np.zeros((32,p,4,4));dz[:,:,0,0]=c['zh'][:,:,k]
  bare,be,_=metric_native(local,np.zeros_like(local['g']),dq,np.zeros_like(local['U']),np.zeros_like(local['du']))
  chain,ce,*_=variation(local,np.zeros_like(local['U']),du,np.zeros_like(local['z']),dz)
  direct.append(c['dens']*(bare.sum(axis=1)+chain.sum(axis=1)));direct_env.append(c['dens']*(be.sum(axis=1)+ce.sum(axis=1)))
  ARM_AVAILABLE['metric_momentum_directional']=np.stack(direct,axis=1);ARM_AVAILABLE['metric_momentum_directional_envelope']=np.stack(direct_env,axis=1)
 available['metric_momentum_directional']=np.stack(direct,axis=1);available['metric_momentum_directional_envelope']=np.stack(direct_env,axis=1)
 ARM_AVAILABLE.update(available)
 scaled_check(label+'_independent_metric_momentum_pullback',base_ph,available['metric_momentum_directional'],available['metric_momentum_directional_envelope'])
 constraints=[];constraint_env=[]
 for t in tangents:
  dg=t['delta_metric_jet'];du=t['du'];dz=t['dz']
  unit=np.einsum('pamn,pm,pn->pa',dg,local['U'],local['U'])+2*np.einsum('pm,pam->pa',local['uc'],du)
  transverse=np.einsum('pab,jpb->jpa',du,local['z'])+np.einsum('pb,jpab->jpa',local['U'],dz)
  ue=np.einsum('pamn,pm,pn->pa',abs(dg),abs(local['U']),abs(local['U']))+2*np.einsum('pm,pam->pa',abs(local['uc']),abs(du))
  te=np.einsum('pab,jpb->jpa',abs(du),abs(local['z']))+np.einsum('pb,jpab->jpa',abs(local['U']),abs(dz))
  constraints.append(np.concatenate((unit.ravel(),transverse.ravel())));constraint_env.append(np.concatenate((ue.ravel(),te.ravel())))
 gv=[];ge=[]
 for k in range(4):
  db=np.zeros(3)
  if k>0:db[k-1]=1
  du,dz,dg,dGa=gauge_velocity_jet(local,c,float(k==0),db);t=kinetic_tangent(local,du,dz,dGa)
  available['gauge_'+str(k)+'_du']=du;available['gauge_'+str(k)+'_dz']=dz;available['gauge_'+str(k)+'_dg']=dg;available['gauge_'+str(k)+'_connection']=dGa
  terms=[t['delta_F'],t['delta_V'],t['delta_D']];gv.append(np.concatenate([a.ravel() for a in terms]))
  ne=abs(du)+np.einsum('pbal,pl->pab',abs(dGa),abs(local['U']));nz=abs(dz)+np.einsum('plab,jpl->jpab',abs(dGa),abs(local['z']))
  nf=lower_last(abs(local['g']),ne);vf=np.einsum('pab,jpb->jpa',abs(local['P']),np.einsum('pa,jpab->jpb',abs(local['U']),nz));df=np.einsum('pac,jpcd,pbd->jpab',abs(local['P']),nz,abs(local['P']))
  ge.append(np.concatenate(((nf+np.swapaxes(nf,1,2)).ravel(),vf.ravel(),df.ravel())))
 available.update(constraint_velocity_contacts=np.stack(constraints),constraint_velocity_envelopes=np.stack(constraint_env),gauge_velocity_contacts=np.stack(gv),gauge_velocity_envelopes=np.stack(ge));ARM_AVAILABLE.update(available)
 actual=np.concatenate((available['constraint_velocity_contacts'].ravel(),available['gauge_velocity_contacts'].ravel()));ee=np.concatenate((available['constraint_velocity_envelopes'].ravel(),available['gauge_velocity_envelopes'].ravel()))
 scaled_check(label+'_unit_transverse_and_primary_gauge_jets',actual,np.zeros_like(actual),ee)
 # Positive congruence only improves arithmetic units. No regularization, jitter or pseudoinverse.
 row=np.max(abs(M),axis=2);assert np.all(row>0)
 scale=1/np.sqrt(row);Mhat=scale[:,:,None]*M*scale[:,None,:];rhs=-mixed;rhs_hat=scale[:,:,None]*rhs
 available.update(native_rhs=rhs,native_equilibration=scale,native_equilibrated_M=Mhat,native_equilibrated_rhs=rhs_hat);ARM_AVAILABLE.update(available)
 solved=np.linalg.solve(Mhat,rhs_hat);ARM_AVAILABLE['native_equilibrated_solution']=solved.copy()
 Y=scale[:,:,None]*solved;ARM_AVAILABLE['native_velocity_response']=Y.copy()
 condition=np.linalg.cond(Mhat);ARM_AVAILABLE['native_condition_number']=condition.copy();assert np.all(np.isfinite(condition))
 kiso_tensor=2*c['N'][:,None,None]*Hbar*c['h'];kiso=np.stack([kiso_tensor[:,i,j] for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=1)
 coeff=np.concatenate((np.broadcast_to(np.eye(6)[None,:,:],(p,6,6)),kiso[:,:,None]),axis=2)
 allY=np.einsum('pij,pjk->pik',Y,coeff);allrhs=-np.einsum('pij,pjk->pik',mixed,coeff)
 action=np.einsum('pij,pjk->pik',M,allY);action_env=np.einsum('pij,pjk->pik',abs(M),abs(allY))+abs(allrhs)
 # Y=-M^-1 B, therefore S=T+B^T Y, with the independently assembled lower block.
 S=T+np.einsum('pki,pil->pkl',H[:,99:,:99],Y)
 Senv=env[:,99:,99:]+np.einsum('pki,pil->pkl',env[:,99:,:99],abs(Y))
 available.update(native_equilibrated_solution=solved,native_velocity_response=Y,native_condition_number=condition,metric_coefficients=coeff,owned_isotropic_hdot=kiso_tensor,owned_isotropic_coefficients=kiso,all_velocity_response=allY,original_M_action=action,original_M_rhs=allrhs,original_M_residual=action-allrhs,original_M_residual_envelope=action_env,native_metric_Schur=S,native_metric_Schur_envelope=Senv,total_metric_reduced_Hessian=S+c['EH_Hessian'],partial_Hamiltonian_metric_Hessian=-S)
 ARM_AVAILABLE.update(available);scaled_check(label+'_six_plus_owned_isotropic_original_linear_residual',action,allrhs,action_env)
 fresh_py=[];fresh_ph=[];fresh_env=[];phase_cases=[];new_first_jets=[];new_constraint=[];new_constraint_env=[]
 for k in range(7):
  du,dz,dg,dGa=native_velocity_jet(local,c,allY[:,:,k],coeff[:,:,k]);fresh=features(local['g'],local['hi'],local['Ga']+dGa,local['U'],local['du']+du,local['z'],local['dz']+dz,local['phi'],local['omega'],local['xi'],local['w'])
  py,ph=reduced_momenta(fresh,c);fresh_py.append(py);fresh_ph.append(ph);fresh_env.append(momentum_envelope(fresh,c)+momentum_envelope(local,c));phase_cases.append(fresh['phi'])
  ARM_AVAILABLE['reconstructed_native_momentum']=np.stack(fresh_py,axis=2);ARM_AVAILABLE['reconstructed_metric_native_momentum']=np.stack(fresh_ph,axis=2);ARM_AVAILABLE['reconstructed_momentum_envelope']=np.stack(fresh_env,axis=2)
  new_first_jets.append((du,dz,dg,dGa));unit=2*np.einsum('pm,pam->pa',fresh['uc'],fresh['nu']);tr=np.einsum('pab,jpb->jpa',fresh['nu'],fresh['z'])+np.einsum('pb,jpab->jpa',fresh['U'],fresh['nz'])
  ue=2*np.einsum('pm,pam->pa',abs(fresh['uc']),abs(fresh['nu']));te=np.einsum('pab,jpb->jpa',abs(fresh['nu']),abs(fresh['z']))+np.einsum('pb,jpab->jpa',abs(fresh['U']),abs(fresh['nz']))
  new_constraint.append(np.concatenate((unit.ravel(),tr.ravel())));new_constraint_env.append(np.concatenate((ue.ravel(),te.ravel())))
  ARM_AVAILABLE['reconstructed_unit_transverse_jets']=np.stack(new_constraint);ARM_AVAILABLE['reconstructed_unit_transverse_envelope']=np.stack(new_constraint_env)
  for n,key in enumerate(('du','dz','dg','connection')):ARM_AVAILABLE['reconstructed_'+key]=np.stack([t[n] for t in new_first_jets])
 available.update(reconstructed_native_momentum=np.stack(fresh_py,axis=2),reconstructed_metric_native_momentum=np.stack(fresh_ph,axis=2),reconstructed_momentum_envelope=np.stack(fresh_env,axis=2),reconstructed_unit_transverse_jets=np.stack(new_constraint),reconstructed_unit_transverse_envelope=np.stack(new_constraint_env))
 for n,key in enumerate(('du','dz','dg','connection')):available['reconstructed_'+key]=np.stack([t[n] for t in new_first_jets])
 ARM_AVAILABLE.update(available)
 scaled_check(label+'_fixed_99_canonical_momenta_reconstructed',available['reconstructed_native_momentum'],np.broadcast_to(base_py[:,:,None],(p,99,7)),available['reconstructed_momentum_envelope'])
 predicted=np.einsum('pij,pjk->pik',S,coeff);delta=available['reconstructed_metric_native_momentum']-base_ph[:,:,None]
 pe=np.einsum('pij,pjk->pik',Senv,abs(coeff));available.update(metric_native_momentum_change=delta,metric_native_momentum_predicted=predicted,metric_native_momentum_change_envelope=pe,metric_EH_momentum_change=np.einsum('pij,pjk->pik',c['EH_Hessian'],coeff));ARM_AVAILABLE.update(available)
 scaled_check(label+'_native_metric_Schur_not_bare_EH',delta,predicted,pe+abs(base_ph[:,:,None])+abs(available['reconstructed_metric_native_momentum']))
 actual=available['reconstructed_unit_transverse_jets'];scaled_check(label+'_reconstructed_complete_constraint_jets',actual,np.zeros_like(actual),available['reconstructed_unit_transverse_envelope'])
 # A positive metric-velocity unit Gram, not the signed gravitational Hessian.
 e=metric_basis();Q=np.einsum('aij,pjk,bkl,pli->pab',e,c['ih'],e,c['ih']);available['metric_velocity_unit_Gram']=Q;ARM_AVAILABLE.update(available)
 qe,qv=np.linalg.eigh(Q);available.update(metric_unit_Gram_eigenvalues=qe,metric_unit_Gram_eigenvectors=qv);ARM_AVAILABLE.update(available);assert np.all(qe>0)
 W=np.einsum('pai,pi,pbi->pab',qv,1/np.sqrt(qe),qv);Ws=np.einsum('pai,pi,pbi->pab',qv,np.sqrt(qe),qv)
 nat=(S+np.swapaxes(S,1,2))/2;total=nat+c['EH_Hessian']
 norm_nat=np.einsum('pij,pjk,pkl->pil',W,nat,W);norm_EH=np.einsum('pij,pjk,pkl->pil',W,c['EH_Hessian'],W);norm_total=norm_nat+norm_EH
 ARM_AVAILABLE.update(metric_normalization=W,metric_inverse_normalization=Ws,normalized_native_Schur=norm_nat,normalized_EH_Hessian=norm_EH,normalized_total_metric_Schur=norm_total)
 eig=np.linalg.eigvalsh(norm_total);ARM_AVAILABLE['total_metric_Schur_eigenvalues']=eig.copy()
 eig_EH=np.linalg.eigvalsh(norm_EH);ARM_AVAILABLE['EH_metric_eigenvalues']=eig_EH.copy()
 eig_nat=np.linalg.eigvalsh(norm_nat);ARM_AVAILABLE['native_metric_eigenvalues']=eig_nat.copy()
 scaleEH=np.max(abs(eig_EH),axis=1);ranktol=6*np.finfo(np.float64).eps*np.max(abs(eig),axis=1);rank=np.sum(abs(eig)>ranktol[:,None],axis=1)
 available.update(metric_normalization=W,metric_inverse_normalization=Ws,normalized_native_Schur=norm_nat,normalized_EH_Hessian=norm_EH,normalized_total_metric_Schur=norm_total,total_metric_Schur_eigenvalues=eig,EH_metric_eigenvalues=eig_EH,native_metric_eigenvalues=eig_nat,total_metric_rank=rank,total_metric_rank_tolerance=ranktol,native_relative_EH_scale=np.max(abs(eig_nat),axis=1)/scaleEH)
 ARM_AVAILABLE.update(available)
 expectedEH=np.column_stack((-2*c['sqrt_h']/(4*c['N']*C),np.repeat((c['sqrt_h']/(4*c['N']*C))[:,None],5,axis=1)))
 qcert=np.einsum('pij,pjk,pkl->pil',W,Q,W);recert=np.einsum('pij,pjk,pkl->pil',Ws,norm_total,Ws)
 actual=np.concatenate((qcert.ravel(),recert.ravel(),eig_EH.ravel()));expected=np.concatenate((np.broadcast_to(np.eye(6),(p,6,6)).ravel(),total.ravel(),expectedEH.ravel()));ee=np.maximum(abs(actual),abs(expected))
 scaled_check(label+'_proper_metric_congruence_and_EH_signature',actual,expected,ee)
 assert np.all(np.isfinite(eig)) and np.all(rank==6),'Local coupled metric Legendre rank refusal; no regularization.'
 return available

def arm(case,ordinary_case,fixed,cp):
 global RAW,ARM_AVAILABLE
 RAW={};ARM_AVAILABLE={};start=len(CHECKS);sig=case['sigma'];CONTEXT.update(stage='canonical_local_legendre',sigma=sig)
 names=['q0_'+x for x in ('R','Z','g','hi','Ga','U','du','z','dz','phi','Pi','PiU','mu')]+['xi','weights','omega_star','b0_d0_q0_Wstar','b0_d0_q0_phase_u_chart','b0_d0_q0_X2']
 vals=selected_arrays(case['checkpoint']['file'],names)
 s=features(vals['q0_g'],vals['q0_hi'],vals['q0_Ga'],vals['q0_U'],vals['q0_du'],vals['q0_z'],vals['q0_dz'],vals['q0_phi'],vals['omega_star'],vals['xi'],vals['weights']);c=adm_chart(s);py,ph=reduced_momenta(s,c)
 assert len(s['U'])==1972 and len(s['xi'])==32 and np.all(s['w']>0) and np.all(s['omega']>0)
 pnat=symmetric_tensor_from_coordinates(ph)
 for name,value in dict(q0_R=vals['q0_R'],q0_Z_coordinate=vals['q0_Z'],xi=s['xi'],weights=s['w'],omega_star=s['omega'],chart_Ui=c['u'],chart_zi=s['z'][:,:,1:],chart_velocity=c['old_velocity'],native_canonical_momentum=py,metric_native_momentum_symmetric_coordinates=ph,metric_native_canonical_momentum_tensor=pnat,metric_total_canonical_momentum_tensor=pnat+c['pi_EH'],metric_EH_momentum_tensor=c['pi_EH'],trial_K_tensor=c['K'],trial_Ktrace=c['Ktrace'],chart_density=c['dens'],chart_N=c['N'],chart_beta=c['beta']).items():ARM_AVAILABLE[name]=value.copy()
 index=np.array([k*(len(s['U'])-1)//(SAMPLE_COUNT-1) for k in range(SAMPLE_COUNT)],dtype=np.int64)
 assert np.array_equal(s['Pi'],vals['q0_Pi']) and np.array_equal(s['PiU'],vals['q0_PiU']) and np.array_equal(s['mu'],vals['q0_mu']),'Literal full first-jet momentum certificate changed.'
 actual=np.concatenate((s['Pi'][:,index].ravel(),s['PiU'][index].ravel(),s['mu'][:,index].ravel(),c['rebuilt_U'].ravel(),c['rebuilt_zt'].ravel()));expected=np.concatenate((vals['q0_Pi'][:,index].ravel(),vals['q0_PiU'][index].ravel(),vals['q0_mu'][:,index].ravel(),s['U'].ravel(),s['z'][:,:,0].ravel()));env=np.maximum(abs(actual),abs(expected))
 scaled_check(f's{sig}_saved_full_firstjet_momenta_and_chart',actual,expected,env)
 phase=phase_inventory(s,vals['b0_d0_q0_Wstar'],vals['b0_d0_q0_phase_u_chart'],fixed);ARM_AVAILABLE.update({n:a.copy() for n,a in phase.items()})
 actual=np.column_stack((phase['p_phi'],phase['phi_velocity_slope'],phase['X']**2));expected=np.column_stack((c['sqrt_h']*(phase['P_X']-phase['X']*(c['gamma']**2-1)),c['sqrt_h']/c['N']*(phase['P_XX']-(c['gamma']**2-1)),vals['b0_d0_q0_X2']))
 penv=np.column_stack((c['sqrt_h']*(abs(phase['P_X'])+abs(phase['X'])*(c['gamma']**2+1)),phase['phi_velocity_slope_envelope'],np.maximum(abs(actual[:,2]),abs(expected[:,2]))))
 scaled_check(f's{sig}_complete_phase_charge_and_clock_derivative',actual,expected,penv)
 cone=s['U'][None,:,0]**2/s['omega'][:,None]**2-ELL**2*(s['hi'][None,:,0,0]+s['U'][None,:,0]**2);ARM_AVAILABLE['native_temporal_cone_coefficient']=cone
 assert np.all(cone>0) and np.all(phase['phi_velocity_slope']!=0),'This local reduced temporal chart is not invertible.'
 ov=selected_arrays(ordinary_case['checkpoint']['file'],('source_g','source_k','source_D','p_phi','mass_weight'));specific=np.zeros((4832,3));specific[:,2]=ov['p_phi'];o=ordinary_velocity(ov['source_g'],specific)
 ARM_AVAILABLE.update({'ordinary_'+n:a.copy() for n,a in o.items()});ARM_AVAILABLE['ordinary_mass_weight']=ov['mass_weight'].copy()
 unit=np.einsum('pa,pab,pb->p',o['u_M'],ov['source_g'],o['u_M']);cov=lower(ov['source_g'],o['u_M'])[:,1:]
 actual=np.concatenate((unit,cov.ravel(),o['coordinate_velocity'].ravel(),o['gamma']));expected=np.concatenate((-np.ones(4832),specific.ravel(),ov['source_k'][:,1:].ravel(),1/np.sqrt(-np.linalg.inv(ov['source_g'])[:,0,0])/np.sqrt(ov['source_D'])));env=np.maximum(abs(actual),abs(expected))
 scaled_check(f's{sig}_ordinary_conserved_covariant_momentum_to_exact_velocity',actual,expected,env)
 Hbar=fixed['Hunit']/LIGHT*cp['background']['h']
 local=local_block(s,index,Hbar,f's{sig}');ARM_AVAILABLE.update(local)
 # Metric instant, U and phase covector are held during the K-only momentum-preserving step.
 local_s=take_points(s,index);p0=phase_momentum(local_s,phase['P_X'][index],phase['P_XX'][index])[0];unchanged=[]
 for k in range(7):
  f=features(local_s['g'],local_s['hi'],local_s['Ga']+local['reconstructed_connection'][k],local_s['U'],local_s['du']+local['reconstructed_du'][k],local_s['z'],local_s['dz']+local['reconstructed_dz'][k],local_s['phi'],local_s['omega'],local_s['xi'],local_s['w'])
  unchanged.append(phase_momentum(f,phase['P_X'][index],phase['P_XX'][index])[0])
 ARM_AVAILABLE['phase_K_step_momentum']=np.stack(unchanged);ARM_AVAILABLE['phase_K_step_old_momentum']=p0.copy()
 scaled_check(f's{sig}_pure_K_step_preserves_owned_phase_momentum',np.stack(unchanged),np.broadcast_to(p0,(7,8)),np.broadcast_to(phase['phi_velocity_slope_envelope'][index],(7,8)))
 ARM_AVAILABLE.update({n:a.copy() for n,a in RAW.items() if not n.startswith(('loaded_','current_'))})
 rec=checkpoint('ARM',ARM_AVAILABLE,dict(kind='compact_saved_covector_canonical_and_local_99_plus_6_legendre_prerequisite',sigma=sig,parent_file=case['checkpoint']['file'],parent_sha256=case['checkpoint']['sha256'],ordinary_parent_file=ordinary_case['checkpoint']['file'],ordinary_parent_sha256=ordinary_case['checkpoint']['sha256'],controls=CHECKS[start:],compact_point_count=1972,local_point_indices=index.tolist(),native_chart='3 covariant U_i plus 32x3 spatial mode covectors; full unit/transverse chart',EH_representative='ADM with paired GHY port; not the old reference GammaGamma time-boundary canonical representative',metric_basis='RR,ZZ,phiphi,RZ,Rphi,Zphi; off-diagonal entries both1; momentum components are basis contractions',conditional_K_increment='delta hdot=2 N Hbar h at fixed metric instant; native p held, total metric p not independently fixed',owned_Hbar=Hbar,ordinary_meridional_momenta='zero disclosed old circular Cauchy assumption',unknowns=dict(full_Cauchy_slice=None,normal_constraint_solution=None,physical_initial_history=None,metric_exterior=None,activity_outside_support=None),physical_changes=[]))
 ARM_AVAILABLE={};return dict(sigma=sig,status='CONDITIONAL_COMPACT_LEGENDRE_PREREQUISITE',checkpoint=rec,sample_count=8,compact_point_count=1972,qualification=FLAGS)


def fixture_metric_adm(h,N,beta):
 # Independent closed ADM inverse for the constant synthetic metric.
 ih=np.diag(1/np.diag(h));g=np.zeros((1,4,4));hi=np.zeros_like(g)
 g[0,1:,1:]=h;g[0,0,1:]=h@beta;g[0,1:,0]=g[0,0,1:]
 g[0,0,0]=-N*N+beta@h@beta
 hi[0,0,0]=-1/(N*N);hi[0,0,1:]=beta/(N*N);hi[0,1:,0]=hi[0,0,1:]
 hi[0,1:,1:]=ih-np.outer(beta,beta)/(N*N)
 return g,hi


def fixture_sym_basis_independent():
 return np.array([[[1,0,0],[0,0,0],[0,0,0]],
                  [[0,0,0],[0,1,0],[0,0,0]],
                  [[0,0,0],[0,0,0],[0,0,1]],
                  [[0,1,0],[1,0,0],[0,0,0]],
                  [[0,0,1],[0,0,0],[1,0,0]],
                  [[0,0,0],[0,0,1],[0,1,0]]],dtype=float)


def fixture_all32_aligned_kinetic(xi,w):
 assert len(xi)==len(w)==32 and np.all(w>0)
 g=np.diag([-1.,1.,1.,1.])[None];hi=g.copy();Ga=np.zeros((1,4,4,4))
 U=np.array([[1.,0.,0.,0.]]);du=np.zeros((1,4,4));dz=np.zeros((32,1,4,4))
 z=np.zeros((32,1,4));z[:,0,1:]=B*xi[:,None]**2*np.array([1/7,-1/11,1/13])[None]
 omega=np.full(32,1/3);phi=np.array([[1/17,0.,0.,0.]])
 s=features(g,hi,Ga,U,du,z,dz,phi,omega,xi,w);c=adm_chart(s)
 RAW.update(fixture_aligned_g=g,fixture_aligned_U=U,fixture_aligned_z=z,
            fixture_aligned_omega=omega,fixture_aligned_xi=xi,fixture_aligned_weights=w)
 H,G,env,tangents=assemble_kinetic(s,c)
 # Direct analytical L_kin = ALPHA|udot|²/2
 #   +sum_j m_j|zdot_j-hdot*z_j/2|²/2, m_j=w_j/omega_j².
 e=fixture_sym_basis_independent();m=w/omega**2
 diag=np.r_[np.full(3,ALPHA),np.repeat(m,3)]
 M=np.diag(diag);mix=np.zeros((99,6))
 ez=np.einsum('kij,mj->mki',e,z[:,0,1:])
 mix[3:]=(-m[:,None,None]*ez/2).transpose(0,2,1).reshape(96,6)
 metric=np.einsum('j,jki,jli->kl',m,ez,ez)/4
 expected=np.block([[M,mix],[mix.T,metric]])
 RAW.update(fixture_aligned_H=H,fixture_aligned_Gram=G,fixture_aligned_envelope=env,
            fixture_aligned_expected_H=expected,fixture_aligned_expected_m=m,
            fixture_aligned_expected_mix=mix,fixture_aligned_expected_metric=metric)
 scaled_check('independent_all32_aligned_canonical_Hessian',H[0],expected,env[0]+abs(expected))
 scaled_check('independent_all32_aligned_kinetic_Gram',G[0],expected,env[0]+abs(expected))
 # Inverse of the analytical diagonal block, not a new spectral/physical inverse.
 response=mix/diag[:,None];schur=H[0,99:,99:]-H[0,99:,:99]@response
 schur_env=env[0,99:,99:]+abs(H[0,99:,:99])@abs(response)
 RAW.update(fixture_aligned_exact_native_metric_response=response,
            fixture_aligned_metric_Schur=schur,fixture_aligned_Schur_envelope=schur_env)
 scaled_check('independent_aligned_modal_metric_Schur_cancellation',schur,np.zeros((6,6)),schur_env)
 p,pmetric=reduced_momenta(s,c);p0=np.r_[np.einsum('j,ji->i',w,z[:,0,1:]),np.zeros(96)]
 actual=np.r_[p[0],pmetric[0]];target=np.r_[p0,np.zeros(6)]
 RAW.update(fixture_aligned_raw_canonical_momentum=p,fixture_aligned_raw_metric_momentum=pmetric,
            fixture_aligned_expected_linear_acceleration_momentum=p0)
 scaled_check('independent_aligned_acceleration_affine_momentum',actual,target,
              np.maximum(abs(actual),abs(target)))
 return dict(state=s,chart=c,H=H,Gram=G,expected=expected)


def fixture_isolated_tilted_modal():
 # Unit rational chart: gw=2/9,v=3/5,gamma=5/4,z=2/7,omega=1/3,ell=1/5.
 # L=(78/25)(zdot-kz)²/2-(1/200)(kz)²/2.
 # k is physical isotropic K; hdot=2k I. All other modal columns vanish.
 xi=(np.arange(32)+.5)/32;w=np.r_[2/9,np.full(31,7/279)];omega=np.full(32,1/3)
 g=np.diag([-1.,1.,1.,1.])[None];U=np.array([[5/4,3/4,0.,0.]])
 z=np.zeros((32,1,4));z[0,0,2]=2/7
 s=features(g,g.copy(),np.zeros((1,4,4,4)),U,np.zeros((1,4,4)),z,
            np.zeros((32,1,4,4)),np.array([[1/17,0.,0.,0.]]),omega,xi,w)
 c=adm_chart(s);y=np.zeros(99);y[4]=1;zero6=np.zeros(6);kiso=np.array([2.,2.,2.,0.,0.,0.])
 jet0=native_velocity_jet(s,c,y,zero6);jet1=native_velocity_jet(s,c,np.zeros(99),kiso)
 t0=kinetic_tangent(s,jet0[0],jet0[1],jet0[3],ell=1/5)
 t1=kinetic_tangent(s,jet1[0],jet1[1],jet1[3],ell=1/5)
 p0,h0=reduced_momenta(s,c,t0['delta_PiU'],t0['delta_Pi'],t0['delta_Ctime'])
 p1,h1=reduced_momenta(s,c,t1['delta_PiU'],t1['delta_Pi'],t1['delta_Ctime'])
 H=np.array([[p0[0,4],p1[0,4]],[2*h0[0,:3].sum(),2*h1[0,:3].sum()]])
 G,env=kinetic_gram(s,[t0,t1],ell=1/5)
 expected=np.array([[78/25,-156/175],[-156/175,623/2450]])
 RAW.update(fixture_tilted_g=g,fixture_tilted_U=U,fixture_tilted_z=z,fixture_tilted_weights=w,
            fixture_tilted_omega=omega,fixture_tilted_field_velocity=y,fixture_tilted_metric_velocity=kiso,
            fixture_tilted_H=H,fixture_tilted_Gram=G,fixture_tilted_expected_H=expected,
            fixture_tilted_delta_V0=t0['delta_V'],fixture_tilted_delta_D0=t0['delta_D'],
            fixture_tilted_delta_V1=t1['delta_V'],fixture_tilted_delta_D1=t1['delta_D'])
 scaled_check('independent_rational_tilted_modal_two_column_block',np.stack((H,G[0])),
              np.stack((expected,expected)),np.stack((env[0]+abs(expected),env[0]+abs(expected))))
 schur=H[1,1]-H[1,0]*H[0,1]/H[0,0]
 envs=abs(H[1,1])+abs(H[1,0]*H[0,1]/H[0,0])
 RAW.update(fixture_tilted_retained_metric_Schur=np.array(schur),
            fixture_tilted_expected_Schur=np.array(-1/2450),fixture_tilted_Schur_envelope=np.array(envs))
 scaled_check('independent_tilted_non_EH_metric_Schur',np.array(schur),np.array(-1/2450),np.array(envs))
 return dict(H=H,Gram=G,expected=expected)


def fixture_covector_chart_gauge_phase_and_ordinary():
 h=np.diag([4.,9.,16.]);N=7/5;beta=np.array([1/7,-1/11,1/13]);g,hi=fixture_metric_adm(h,N,beta)
 U=np.array([[25/28,97/392,25/308,-25/364]])
 z=np.zeros((32,1,4));z[:,0,1:]=((np.arange(32)+1)/64)[:,None]*np.array([1/7,-1/11,1/13])[None]
 Jzz=np.array([-97/350,-1/11,1/13]);z[:,0,0]=z[:,0,1:]@Jzz
 xi=(np.arange(32)+.5)/32;w=np.full(32,1/32);omega=np.full(32,1/3)
 s=features(g,hi,np.zeros((1,4,4,4)),U,np.zeros((1,4,4)),z,np.zeros((32,1,4,4)),
            np.array([[3/17,0.,0.,0.]]),omega,xi,w);c=adm_chart(s)
 JU=np.array([[3/14,0.,0.],[43/196,0.,0.],[3/154,1/9,0.],[-3/182,0.,1/16]])
 JzU=-z[:,0,1:]*np.array([112/625,28/225,7/100])[None]
 actual=np.r_[c['rebuilt_U'].ravel(),c['rebuilt_zt'].ravel(),c['JU'].ravel(),c['Jzz'].ravel(),c['JzU'].ravel(),c['N'],c['gamma'],c['dens']]
 expected=np.r_[U.ravel(),z[:,:,0].ravel(),JU.ravel(),Jzz,JzU.ravel(),7/5,5/4,168/5]
 RAW.update(fixture_chart_g=g,fixture_chart_inverse=hi,fixture_chart_U=U,fixture_chart_z=z,
            fixture_chart_expected_JU=JU,fixture_chart_expected_Jzz=Jzz,fixture_chart_expected_JzU=JzU,
            fixture_chart_actual=actual,fixture_chart_expected=expected)
 scaled_check('independent_rational_covector_ADM_chart',actual,expected,np.maximum(abs(actual),abs(expected)))
 # Mixed native/metric temporal jet: constraints use BOTH dg(U,U) and 2g(U,du).
 y=(np.arange(99)+1)/101;k=np.array([1/17,-1/19,1/23,1/29,-1/31,1/37])
 du,dz,dg,dGa=native_velocity_jet(s,c,y,k)
 unit=np.einsum('pab,pa,pb->p',dg[:,0],U,U)+2*np.einsum('pab,pa,pb->p',g,U,du[:,0])
 unit_env=np.einsum('pab,pa,pb->p',abs(dg[:,0]),abs(U),abs(U))+2*np.einsum('pab,pa,pb->p',abs(g),abs(U),abs(du[:,0]))
 trans=np.einsum('pa,jpa->jp',du[:,0],z)+np.einsum('pa,jpa->jp',U,dz[:,:,0])
 trans_env=np.einsum('pa,jpa->jp',abs(du[:,0]),abs(z))+np.einsum('pa,jpa->jp',abs(U),abs(dz[:,:,0]))
 actual=np.r_[unit,trans.ravel()];envelope=np.r_[unit_env,trans_env.ravel()]
 RAW.update(fixture_chart_velocity99=y,fixture_chart_metric_velocity6=k,fixture_chart_du=du,
            fixture_chart_dz=dz,fixture_chart_dg=dg,fixture_chart_delta_connection=dGa,
            fixture_chart_unit_jet=unit,fixture_chart_transverse_jet=trans,fixture_chart_jet_envelope=envelope)
 scaled_check('independent_mixed_unit_and_transverse_velocity_jets',actual,np.zeros_like(actual),envelope)
 # Pure coordinate-time lapse/shift derivatives leave the physical covariant jets zero.
 gdU,gdZ,gdg,gdGa=gauge_velocity_jet(s,c,1/17,np.array([1/19,-1/23,1/29]))
 gt=kinetic_tangent(s,gdU,gdZ,gdGa)
 eU=abs(gdU)+np.einsum('pbal,pl->pab',abs(gdGa),abs(U))
 eZ=abs(gdZ)+np.einsum('plab,jpl->jpab',abs(gdGa),abs(z))
 actual=np.r_[gt['delta_nu'].ravel(),gt['delta_nz'].ravel()];envelope=np.r_[eU.ravel(),eZ.ravel()]
 RAW.update(fixture_gauge_du=gdU,fixture_gauge_dz=gdZ,fixture_gauge_dg=gdg,
            fixture_gauge_delta_connection=gdGa,fixture_gauge_delta_nu=gt['delta_nu'],
            fixture_gauge_delta_nz=gt['delta_nz'],fixture_gauge_envelope=envelope)
 scaled_check('independent_lapse_shift_primary_covariant_cancellation',actual,np.zeros_like(actual),envelope)
 # Full relative-Y phase momentum and slope, not the P(X) constituent alone.
 mom,slope,env,J,X=phase_momentum(s,np.array([2/7]),np.array([7/3]))
 expected=np.array([24*(2/7-(15/119)*(9/16)),(120/7)*(7/3-9/16),15/119])
 actual=np.array([mom[0],slope[0],X[0]])
 RAW.update(fixture_phase_pressure_PX=np.array([2/7]),fixture_phase_pressure_PXX=np.array([7/3]),
            fixture_phase_current=J,fixture_phase_momentum=mom,fixture_phase_slope=slope,
            fixture_phase_expected=expected,fixture_phase_actual=actual)
 scaled_check('independent_rational_relative_phase_density_and_slope',actual,expected,
              np.maximum(abs(actual),abs(expected)))
 # Cylindrical h_phiphi=16, specific p_phi=3: gamma=5/4 and nonzero rotation.
 material=ordinary_velocity(g,np.array([[0.,0.,3.]]))
 expected_u=np.array([[25/28,-25/196,25/308,173/1456]])
 expected_v=np.array([[-1/7,1/11,173/1300]])
 actual=np.r_[material['u_M'].ravel(),material['coordinate_velocity'].ravel(),material['gamma'],material['coordinate_time_Hamiltonian']]
 expected=np.r_[expected_u.ravel(),expected_v.ravel(),5/4,79/52]
 RAW.update(fixture_material_specific_p=np.array([[0.,0.,3.]]),fixture_material_u=material['u_M'],
            fixture_material_coordinate_velocity=material['coordinate_velocity'],
            fixture_material_coordinate_time_Hamiltonian=material['coordinate_time_Hamiltonian'],
            fixture_material_expected=expected,fixture_material_actual=actual)
 # This is the coordinate-time generator N*gamma-beta.p; normal energy is gamma.
 scaled_check('independent_rotating_fixed_angular_momentum_conversion',actual,expected,
              np.maximum(abs(actual),abs(expected)))
 return dict(state=s,chart=c,material=material)


def observer_adm_legendre_analytical_fixtures(xi,w):
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS,'Root-only reviewed execution.'
 start=len(CHECKS)
 a=fixture_all32_aligned_kinetic(xi,w)
 b=fixture_isolated_tilted_modal()
 c=fixture_covector_chart_gauge_phase_and_ordinary()
 assert len(CHECKS)-start==11
 return dict(aligned=a,tilted=b,chart=c)


def admission():
 pins={}
 def add(n,h):
  n=str(path(n).resolve())
  assert isinstance(h,str) and len(h)==64 and all(c in '0123456789abcdef' for c in h)
  assert n not in pins or pins[n]==h,('Conflicting input seal',n)
  pins[n]=h
 for n,h in PINS.items():add(n,h)
 add(STEM+'.md',PROTOCOL_SHA);add(__file__,sha(__file__))
 specs=((PARENT,13990,'cross_u_saved_full_metric_native_source_residual_v001.py',
         'CONDITIONAL_FULL_METRIC_WEAK_MEASURES_ARITHMETIC_PASS',36,
         'CONDITIONAL_FULL_METRIC_WEAK_MEASURES'),
        (ORDINARY,15580,'cross_u_saved_rotating_sheet_frechet_v001.py',
         'CONDITIONAL_ORDINARY_SOURCE_FRECHET_ARITHMETIC_PASS',19,
         'CONDITIONAL_ORDINARY_SOURCE_FRECHET_BLOCK'))
 receipts={}
 for stem,pid,source,status,count,case_status in specs:
  rc=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['closed'] and rc['owner']['owner']=='root'
  assert rc['owner']['pid']==pid and rc['owner']['source_file']==source
  assert rc['owner']['source_sha256']==PINS[source]
  assert rc['result_sha256']==PINS[stem+'_RESULT.json']
  assert all(v is False for v in rc['qualification'].values())
  for field in ('input_sha256','output_sha256'):
   for n,h in rc[field].items():add(n,h)
  receipts[stem]=rc
 for n,h in pins.items():assert sha(path(n))==h,('Input seal changed',n)
 results={}
 for stem,pid,source,status,count,case_status in specs:
  rc=receipts[stem]
  assert path(stem+'_RESULT.json').stat().st_size<32*1024*1024
  result=json.loads(path(stem+'_RESULT.json').read_text())
  assert result['owner']==rc['owner'] and result['status']==status
  assert json.loads(path(stem+'_OWNER_START.json').read_text())==rc['owner']
  manifest=json.loads(path(stem+'_MANIFEST.json').read_text())
  assert manifest['owner']==rc['owner'] and manifest['input_sha256']==rc['input_sha256']
  assert len(result['controls'])==count and all(c['passed'] is True for c in result['controls'])
  assert [c['sigma'] for c in result['cases']]==list(SIGMAS)
  assert len(result['checkpoints'])==6 and all(v is False for v in result['qualification'].values())
  records=result['checkpoints'];assert len({r['file'] for r in records})==6
  for r in records:
   assert r['commit_file']==r['file']+'.COMMIT.json'
   assert pins[str(path(r['file']).resolve())]==r['sha256']
   assert pins[str(path(r['commit_file']).resolve())]==r['commit_sha256']
   assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
   md=r['metadata'];assert md['owner']==rc['owner'] and all(v is False for v in md['qualification'].values())
   assert all(d['finite'] is True for d in md['schema'].values())
  assert {p.name for p in BASE.glob(stem+'_*.npz')}=={r['file'] for r in records}
  assert {p.name for p in BASE.glob(stem+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in records}
  for c in result['cases']:
   assert c['checkpoint'] in records and c['checkpoint']['metadata']['sigma']==c['sigma']
   assert c['status']==case_status and all(v is False for v in c['qualification'].values())
  results[stem]=result
 parent,ordinary=results[PARENT],results[ORDINARY]
 def schema(rec,n,shape):
  assert rec['metadata']['schema'][n]==dict(shape=shape,dtype='float64',finite=True),(rec['file'],n)
 input_record=parent['checkpoints'][0]
 for n,shape in dict(r_kpc=[87],z_kpc=[45],final_state=[65,87,45],xi=[32],weights=[32],source_samples32=[4832,9]).items():schema(input_record,n,shape)
 assert input_record['metadata']['physical_changes']==[]
 schema(ordinary['checkpoints'][0],'source_samples32',[4832,9])
 omd=ordinary['checkpoints'][0]['metadata']
 assert omd['parent_file']==input_record['file'] and omd['parent_sha256']==input_record['sha256']
 assert omd['copied_metric_controls']==parent['controls'] and omd['physical_changes']==[]
 qshapes=dict(R=[1972],Z=[1972],g=[1972,4,4],hi=[1972,4,4],Ga=[1972,4,4,4],
              U=[1972,4],du=[1972,4,4],z=[32,1972,4],dz=[32,1972,4,4],phi=[1972,4],
              V=[32,1972,4],D=[32,1972,4,4],a=[1972,4],r=[1972,4],
              Pi=[32,1972,4,4],PiU=[1972,4,4],mu=[32,1972])
 for nc,oc in zip(parent['cases'],ordinary['cases']):
  nr,orr=nc['checkpoint'],oc['checkpoint'];assert nc['sigma']==oc['sigma']
  for n,shape in qshapes.items():schema(nr,'q0_'+n,shape)
  for n in ('xi','weights','omega_star'):schema(nr,n,[32])
  for n in ('phase_u_chart','Pstar','Wstar','X2'):schema(nr,'b0_d0_q0_'+n,[1972])
  for n,shape in dict(source_g=[4832,4,4],source_k=[4832,4],source_D=[4832],mass_weight=[4832],p_phi=[4832]).items():schema(orr,n,shape)
  assert orr['metadata']['parent_file']==nr['file'] and orr['metadata']['parent_sha256']==nr['sha256']
 fixed=dict(input_record['metadata']['owned_fixed'])
 cpname='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json'
 sharedname='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json'
 assert str(path(cpname).resolve()) in pins and str(path(sharedname).resolve()) in pins
 cp=json.loads(path(cpname).read_text());shared=json.loads(path(sharedname).read_text())
 assert cp==next(r for r in shared['rows'] if r['eps']==1e-5)
 shared_fixed=dict(shared['manifest']['fixed_parent']);shared_fixed['eps']=1e-5
 assert fixed==shared_fixed and fixed['Q0_over_Hstar']==100 and fixed['eps']==1e-5
 return pins,parent,ordinary,fixed,cp


def fixtures(xi,w):
 start=len(CHECKS);observer_adm_legendre_analytical_fixtures(xi,w)
 g=np.diag([-1.,1.,1.,1.])[None];U=np.array([[1.,0.,0.,0.]])
 s=features(g,g.copy(),np.zeros((1,4,4,4)),U,np.zeros((1,4,4)),np.zeros((32,1,4)),np.zeros((32,1,4,4)),np.array([[1/17,0.,0.,0.]]),np.ones(32),xi,w);c=adm_chart(s)
 trace=np.array([1.,1.,1.,0.,0.,0.]);expected=(np.diag([1.,1.,1.,2.,2.,2.])-np.outer(trace,trace))/(4*C)
 RAW.update(fixture_EH_ADM_Hessian=c['EH_Hessian'],fixture_EH_independent_expected=expected)
 scaled_check('independent_flat_EH_six_component_DeWitt_signature',c['EH_Hessian'][0],expected,np.maximum(abs(c['EH_Hessian'][0]),abs(expected)))
 assert len(CHECKS)-start==12

def run_arm(case,ordinary_case,fixed,cp):
 global RAW,ARM_AVAILABLE
 start=len(CHECKS)
 try:
  with np.errstate(over='raise',invalid='raise',divide='raise'):return arm(case,ordinary_case,fixed,cp)
 except Exception:
  failure=traceback.format_exc();available=dict(ARM_AVAILABLE);available.update(RAW)
  rec=checkpoint('REFUSED_ARM',available,dict(kind='unaccepted_available_local_Legendre_operands',sigma=case['sigma'],context=dict(CONTEXT),traceback=failure,controls=CHECKS[start:],native_parent_file=case['checkpoint']['file'],native_parent_sha256=case['checkpoint']['sha256'],ordinary_parent_file=ordinary_case['checkpoint']['file'],ordinary_parent_sha256=ordinary_case['checkpoint']['sha256'],physical_changes=[]))
  ARM_AVAILABLE={};RAW={}
  return dict(sigma=case['sigma'],status='LOCAL_LEGENDRE_REFUSED',checkpoint=rec,qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW,ARM_AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded prospective root-only source; complete independent source/protocol admission required.')
 assert not list(BASE.glob(STEM+'_*')),'Own runtime namespace occupied.'
 INPUTS,parent,ordinary,fixed,cp=admission();cases=[];exit_code=0
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__),scope='compact saved constrained momenta and local 99+six ADM Legendre prerequisite')
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(controls=CONTROL_COUNT,pairs=PAIR_COUNT,sigma=SIGMAS,compact_points=1972,local_points=8,native_velocities=99,metric_velocities=6,tolerance=TOL),parent_file=PARENT+'_RESULT.json',ordinary_parent_file=ORDINARY+'_RESULT.json',qualification=FLAGS))
  import numpy as _np
  np=_np
  vals=selected_arrays(parent['checkpoints'][0]['file'],('xi','weights'));assert vals['xi'].shape==vals['weights'].shape==(32,) and np.all(vals['xi']>0) and np.all(vals['weights']>0)
  checkpoint('INPUT',vals,dict(kind='unchanged_owned32_quad_calibration_and_compact_parent_refs',fixed=fixed,owned_EPS5_background=cp['background'],parent_file=PARENT+'_RESULT.json',parent_sha256=PINS[PARENT+'_RESULT.json'],ordinary_parent_file=ORDINARY+'_RESULT.json',ordinary_parent_sha256=PINS[ORDINARY+'_RESULT.json'],copied_metric_controls=parent['controls'],copied_ordinary_controls=ordinary['controls'],copied_original_failures=parent['checkpoints'][0]['metadata']['copied_original_failures'],physical_changes=[]))
  RAW={};ARM_AVAILABLE={};fixtures(vals['xi'],vals['weights']);available=dict(ARM_AVAILABLE);available.update(RAW)
  checkpoint('ARITHMETIC_FIXTURES',available,dict(kind='twelve_fixed_artificial_chart_and_kinetic_contact_controls',controls=list(CHECKS),physical_changes=[]))
  for c,o in zip(parent['cases'],ordinary['cases']):cases.append(run_arm(c,o,fixed,cp))
  accepted=all(c['status']=='CONDITIONAL_COMPACT_LEGENDRE_PREREQUISITE' for c in cases)
  assert len(cases)==4 and len(RECORDS)==PAIR_COUNT
  if accepted:assert len(CHECKS)==CONTROL_COUNT and all(c['passed'] for c in CHECKS)
  else:exit_code=3
  status='CONDITIONAL_COMPACT_LEGENDRE_ARITHMETIC_PASS' if accepted else 'LOCAL_LEGENDRE_REFUSALS_RETAINED'
  result=dict(owner=OWNER,status=status,cases=cases,controls=CHECKS,predeclared_control_count=CONTROL_COUNT,checkpoints=RECORDS,parent_file=PARENT+'_RESULT.json',parent_sha256=PINS[PARENT+'_RESULT.json'],ordinary_parent_file=ORDINARY+'_RESULT.json',ordinary_parent_sha256=PINS[ORDINARY+'_RESULT.json'],qualification=FLAGS)
  recheck();rh=json_file(STEM+'_RESULT.json',result)
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\n{status}; {len(CHECKS)} of {CONTROL_COUNT} predeclared arithmetic controls, four outcomes, six pairs.\n\n1972 selected first-jet points per arm; eight local kinetic admissions retain all99 native velocities and six metric directions. Signed Schur/rank and original residuals are saved. No full Cauchy slice, metric correction, exterior, formation history or physical velocity is supplied.\n').encode())
  recheck();rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS)
  json_file(STEM+'_RECEIPT.json',rc);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(rc);recheck();print(status,len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_failure=None;closing_failure=None;available=dict(ARM_AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_constrained_canonical_operands',context=dict(CONTEXT)))
   except BaseException:raw_failure=traceback.format_exc()
  try:seal_created();recheck(False)
  except BaseException:closing_failure=traceback.format_exc()
  name=STEM+'_RECEIPT.json';prior=sha(path(name)) if path(name).exists() else None
  if prior:OUTPUTS[name]=prior
  unknown_npz=[p.name for p in BASE.glob(STEM+'_*.npz') if p.name not in {r['file'] for r in RECORDS}];unknown_commit=[p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json') if p.name not in {r['commit_file'] for r in RECORDS}]
  error=dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_failure,closing_traceback=closing_failure,context=dict(CONTEXT),checkpoints=RECORDS,controls=CHECKS,completed_cases=cases,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=unknown_npz,unqualified_commits=unknown_commit,qualification=FLAGS)
  eh=json_file(STEM+'_ERROR.json',error)
  if prior is None:
   rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=eh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(rc)
  recheck(False);raise
 return exit_code

if __name__=='__main__':raise SystemExit(main())
