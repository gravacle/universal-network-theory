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
PROTOCOL_SHA='PENDING_FINAL_PROTOCOL'
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
B=A0*KPC/LIGHT**2;C=1.98;KB=2-C;ALPHA=KB/C;GC=3*math.pi/8;ELL=.1
SIGMAS=(.1,1.,10.,100.);TOL=2e-11;SAMPLE_COUNT=8;NATIVE_COUNT=99
CONTROL_COUNT=None;PAIR_COUNT=6
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
 H=np.stack(columns,axis=-1);G,env=kinetic_gram(s,tangents)
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
 scaled_check(label+'_kinetic_Gram_and_mixed_symmetry',np.stack((H,H)),np.stack((G,np.swapaxes(H,1,2))),np.stack((env,env+np.swapaxes(env,1,2))))
 direct=[];direct_env=[]
 for k in range(6):
  dq=np.zeros((p,4,4,4));dq[:,0]=c['embed'][:,k];du=np.zeros((p,4,4));du[:,0]=c['Uh'][:,k];dz=np.zeros((32,p,4,4));dz[:,:,0,0]=c['zh'][:,:,k]
  bare,be,_=metric_native(local,np.zeros_like(local['g']),dq,np.zeros_like(local['U']),np.zeros_like(local['du']))
  chain,ce,*_=variation(local,np.zeros_like(local['U']),du,np.zeros_like(local['z']),dz)
  direct.append(c['dens']*(bare.sum(axis=1)+chain.sum(axis=1)));direct_env.append(c['dens']*(be.sum(axis=1)+ce.sum(axis=1)))
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
 solved=np.linalg.solve(Mhat,rhs_hat);Y=scale[:,:,None]*solved
 condition=np.linalg.cond(Mhat);assert np.all(np.isfinite(condition))
 kiso_tensor=2*c['N'][:,None,None]*Hbar*c['h'];kiso=np.stack([kiso_tensor[:,i,j] for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=1)
 coeff=np.concatenate((np.broadcast_to(np.eye(6)[None,:,:],(p,6,6)),kiso[:,:,None]),axis=2)
 allY=np.einsum('pij,pjk->pik',Y,coeff);allrhs=-np.einsum('pij,pjk->pik',mixed,coeff)
 action=np.einsum('pij,pjk->pik',M,allY);action_env=np.einsum('pij,pjk->pik',abs(M),abs(allY))+abs(allrhs)
 S=T-np.einsum('pki,pil->pkl',H[:,99:,:99],Y*-1)
 # Y=-M^-1 B, therefore S=T+B^T Y, with the independently assembled lower block.
 S=T+np.einsum('pki,pil->pkl',H[:,99:,:99],Y)
 Senv=env[:,99:,99:]+np.einsum('pki,pil->pkl',env[:,99:,:99],abs(Y))
 available.update(native_equilibrated_solution=solved,native_velocity_response=Y,native_condition_number=condition,metric_coefficients=coeff,owned_isotropic_hdot=kiso_tensor,owned_isotropic_coefficients=kiso,all_velocity_response=allY,original_M_action=action,original_M_rhs=allrhs,original_M_residual=action-allrhs,original_M_residual_envelope=action_env,native_metric_Schur=S,native_metric_Schur_envelope=Senv,total_metric_reduced_Hessian=S+c['EH_Hessian'],partial_Hamiltonian_metric_Hessian=-S)
 ARM_AVAILABLE.update(available);scaled_check(label+'_six_plus_owned_isotropic_original_linear_residual',action,allrhs,action_env)
 fresh_py=[];fresh_ph=[];fresh_env=[];phase_cases=[];new_first_jets=[];new_constraint=[];new_constraint_env=[]
 for k in range(7):
  du,dz,dg,dGa=native_velocity_jet(local,c,allY[:,:,k],coeff[:,:,k]);fresh=features(local['g'],local['hi'],local['Ga']+dGa,local['U'],local['du']+du,local['z'],local['dz']+dz,local['phi'],local['omega'],local['xi'],local['w'])
  py,ph=reduced_momenta(fresh,c);fresh_py.append(py);fresh_ph.append(ph);fresh_env.append(momentum_envelope(fresh,c)+momentum_envelope(local,c));phase_cases.append(fresh['phi'])
  new_first_jets.append((du,dz,dg,dGa));unit=2*np.einsum('pm,pam->pa',fresh['uc'],fresh['nu']);tr=np.einsum('pab,jpb->jpa',fresh['nu'],fresh['z'])+np.einsum('pb,jpab->jpa',fresh['U'],fresh['nz'])
  ue=2*np.einsum('pm,pam->pa',abs(fresh['uc']),abs(fresh['nu']));te=np.einsum('pab,jpb->jpa',abs(fresh['nu']),abs(fresh['z']))+np.einsum('pb,jpab->jpa',abs(fresh['U']),abs(fresh['nz']))
  new_constraint.append(np.concatenate((unit.ravel(),tr.ravel())));new_constraint_env.append(np.concatenate((ue.ravel(),te.ravel())))
 available.update(reconstructed_native_momentum=np.stack(fresh_py,axis=2),reconstructed_metric_native_momentum=np.stack(fresh_ph,axis=2),reconstructed_momentum_envelope=np.stack(fresh_env,axis=2),reconstructed_unit_transverse_jets=np.stack(new_constraint),reconstructed_unit_transverse_envelope=np.stack(new_constraint_env))
 for n,key in enumerate(('du','dz','dg','connection')):available['reconstructed_'+key]=np.stack([t[n] for t in new_first_jets])
 ARM_AVAILABLE.update(available)
 scaled_check(label+'_fixed_99_canonical_momenta_reconstructed',available['reconstructed_native_momentum'],np.broadcast_to(base_py[:,:,None],(p,99,7)),available['reconstructed_momentum_envelope'])
 predicted=np.einsum('pij,pjk->pik',S,coeff);delta=available['reconstructed_metric_native_momentum']-base_ph[:,:,None]
 pe=np.einsum('pij,pjk->pik',Senv,abs(coeff));available.update(metric_native_momentum_change=delta,metric_native_momentum_predicted=predicted,metric_native_momentum_change_envelope=pe,metric_EH_momentum_change=np.einsum('pij,pjk->pik',c['EH_Hessian'],coeff));ARM_AVAILABLE.update(available)
 scaled_check(label+'_native_metric_Schur_not_bare_EH',delta,predicted,pe+abs(base_ph[:,:,None])+abs(available['reconstructed_metric_native_momentum']))
 actual=available['reconstructed_unit_transverse_jets'];scaled_check(label+'_reconstructed_complete_constraint_jets',actual,np.zeros_like(actual),available['reconstructed_unit_transverse_envelope'])
 return available

def arm(case,ordinary_case,fixed,cp):
 global RAW,ARM_AVAILABLE
 RAW={};ARM_AVAILABLE={};start=len(CHECKS);sig=case['sigma'];CONTEXT.update(stage='canonical_local_legendre',sigma=sig)
 names=['q0_'+x for x in ('R','Z','g','hi','Ga','U','du','z','dz','phi','Pi','PiU','mu')]+['xi','weights','omega_star','b0_d0_q0_Wstar','b0_d0_q0_phase_u_chart','b0_d0_q0_X2']
 vals=selected_arrays(case['checkpoint']['file'],names)
 s=features(vals['q0_g'],vals['q0_hi'],vals['q0_Ga'],vals['q0_U'],vals['q0_du'],vals['q0_z'],vals['q0_dz'],vals['q0_phi'],vals['omega_star'],vals['xi'],vals['weights']);c=adm_chart(s);py,ph=reduced_momenta(s,c)
 assert len(s['U'])==1972 and len(s['xi'])==32 and np.all(s['w']>0) and np.all(s['omega']>0)
 for name,value in dict(q0_R=vals['q0_R'],q0_Z_coordinate=vals['q0_Z'],xi=s['xi'],weights=s['w'],omega_star=s['omega'],chart_Ui=c['u'],chart_zi=s['z'][:,:,1:],chart_velocity=c['old_velocity'],native_canonical_momentum=py,metric_native_momentum_symmetric_coordinates=ph,metric_EH_momentum_tensor=c['pi_EH'],trial_K_tensor=c['K'],trial_Ktrace=c['Ktrace'],chart_density=c['dens'],chart_N=c['N'],chart_beta=c['beta']).items():ARM_AVAILABLE[name]=value.copy()
 actual=np.concatenate((s['Pi'].ravel(),s['PiU'].ravel(),s['mu'].ravel(),c['rebuilt_U'].ravel(),c['rebuilt_zt'].ravel()));expected=np.concatenate((vals['q0_Pi'].ravel(),vals['q0_PiU'].ravel(),vals['q0_mu'].ravel(),s['U'].ravel(),s['z'][:,:,0].ravel()));env=np.maximum(abs(actual),abs(expected))
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
 actual=np.concatenate((unit,cov.ravel(),o['coordinate_velocity'].ravel(),o['gamma']));expected=np.concatenate((-np.ones(4832),specific.ravel(),ov['source_k'][:,1:].ravel(),1/np.sqrt(ov['source_D'])));env=np.maximum(abs(actual),abs(expected))
 scaled_check(f's{sig}_ordinary_conserved_covariant_momentum_to_exact_velocity',actual,expected,env)
 index=np.array([k*(len(s['U'])-1)//(SAMPLE_COUNT-1) for k in range(SAMPLE_COUNT)],dtype=np.int64);Hbar=fixed['Hunit']/LIGHT*cp['background']['h']
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

# New main and fixed controls follow. This protected workdraft is incomplete.
if __name__=='__main__':
 raise SystemExit('AUTHOR_DRAFT: incomplete protected workdraft; no evaluation authorized')
