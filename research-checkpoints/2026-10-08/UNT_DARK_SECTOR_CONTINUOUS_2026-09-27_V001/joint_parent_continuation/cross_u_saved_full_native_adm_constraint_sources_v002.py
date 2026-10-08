"""Guarded complete-action canonical lapse/shift source prerequisite.
No numerical/scientific function is evaluated during authorship. Root only.
"""
from pathlib import Path
import math,ast,hashlib,json,os,traceback,argparse,zipfile,struct
from datetime import datetime,timezone
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002'
FAILED='CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001'
FAILED_RESULT_SHA='05a93d3bc99bde21d2eb8470bcc17ee239d90065185afa6f75d8fbbfb6129c1f'
FAILED_RECEIPT_SHA='d8f76dd6285355455809d6ba0afc236bcf32f29ed48680a94b4c0b5104c525e5'
PARENT='CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002'
PARENT_RESULT_SHA='4d4c9e89520390db932b66548aed361607abcc70b48d422502a3f53af9d06fb6'
PARENT_RECEIPT_SHA='4a21c59742252d7fcaaccfd7b9371fa846bc1d248579ae9408a9838ae971b99e'
np=None
RAW={}
ARM_AVAILABLE={}
OWNER=None;INPUTS={};OUTPUTS={};RECORDS=[];CONTEXT={};CHECKS=[]
FLAGS={k:False for k in ('full_slice_Cauchy_qualified','global_constraint_solution_qualified','CMC_solution_qualified','physical_initial_state_qualified','physical_history_qualified','physical_native_inertia_qualified','physical_junction_qualified','active_source_mapping_qualified','metric_correction_applied','orbital_force_qualified','observational_qualified','joint_model_adopted')}
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10
B=A0*KPC/LIGHT**2;C=1.98;KB=.02;ALPHA=KB/C;GC=3*math.pi/8;ELL=.1
SIGMAS=(.1,1.,10.,100.);TOL=2e-11
BOXES=((2.,12.),(16.,48.))
CONTROL_COUNT=42;PAIR_COUNT=6
PROTOCOL_SHA='609ad771c8d7e3487d7db4545a76343452c91d773e8c6138de71ebcb92518b6c'

PINS={'author_fragment_adm_constraint_sources_admission_v001.txt': 'ccc6bcf342a45dd7bdf24bff8fef06f9015951b008c2ba120a93df77b3b9c82d', 'authoring_cross_u_saved_full_native_adm_constraint_sources_v001_420_d2165148.py': 'd2165148137075506492846193cc057e86717ce1c53916c93346cd9c597cbcd5', 'authoring_cross_u_saved_full_native_adm_constraint_sources_v001_1012_531d7edb.py': '531d7edb560652c3e40f30a823ded6681868cc12d7d068d3f217c5bf6f1fdc32', 'author_fragment_adm_constraint_sources_fixtures_v001.txt': '6be1a2259d1d1c15ee3aa28c01900e6ba14dc64942f054f8f8a64baaf12299dc', 'authoring_cross_u_saved_full_native_adm_constraint_sources_v002_1153_a930006c.py': 'a930006c65db4cd1a6525692a2019f821ac29c7c25c0b5929286fd11d38211cf', 'author_fragment_adm_constraint_v002_span_envelopes.txt': '975756c5578d68758a41e787ceae7373296f524161bfd090576fe0b10787a63f', 'author_fragment_adm_constraint_sources_v002_recovery.txt': '69f705a7320057e863a255e3138121a1c548c9fa3719bbed748639ba70e0e869', 'authoring_cross_u_saved_full_native_adm_constraint_sources_v002_1438_e6052b78.py': 'e6052b78f27901bc9c4147d8737669f7bb91225de67821e537c879cf8bcd64ad', 'author_fragment_adm_constraint_sources_v002_recovery_final.txt': 'af0195ecbe22c193748307c92862905a5093174a62212263410a3c064483c958', 'reviewed_cross_u_saved_full_native_adm_constraint_sources_v002_1438_dae9aaf7.py': 'dae9aaf74c95a5b76781ef7c4447c7b8649e3ca079a751f5c3f2bb5af001b0bb', 'reviewed_cross_u_saved_full_native_adm_constraint_sources_v002_1438_e5d506e6.py': 'e5d506e6b0acec22dd9fd004c8f8789cc3604eeace86cb4d8c2be3ca2048515a', 'reviewed_CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V002_19_f7046ef2.md': 'f7046ef2d7b3de1ac814c90d9a98a970ca96afeffd48fffc3b2e2021f7fda579'}


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


def take_points(s,index):
 return features(s['g'][index],s['hi'][index],s['Ga'][index],s['U'][index],s['du'][index],s['z'][:,index],s['dz'][:,index],s['phi'][index],s['omega'],s['xi'],s['w'])




def chart_operation_envelopes(s,c):
 # u_i=g_i,nu U^nu; propagate its CANCELING contraction before h^-1 and JU.
 N,ga,be,ih=c['N'],c['gamma'],c['beta'],c['ih'];U,z=s['U'],s['z']
 eu=np.einsum('pia,pa->pi',abs(s['g'][:,1:,:]),abs(U))
 RAW['operation_chart_u_cov_envelope']=eu.copy()
 eup=np.einsum('pij,pj->pi',abs(ih),eu)
 RAW['operation_chart_up_envelope']=eup.copy()
 eU=np.column_stack((ga/N,eup+abs(be)*ga[:,None]/N[:,None]))
 RAW['operation_chart_rebuilt_U_envelope']=eU.copy()
 ezt=np.einsum('jpi,pi->jp',abs(z[:,:,1:]),eU[:,1:])/abs(c['rebuilt_U'][None,:,0])
 RAW['operation_chart_rebuilt_zt_envelope']=ezt.copy()
 eJU=np.zeros_like(c['JU']);eJU[:,0]=eup/(N*ga)[:,None]
 eJU[:,1:]=abs(ih)+abs(be)[:,:,None]*eJU[:,None,0,:]
 RAW['operation_chart_JU_envelope']=eJU.copy()
 eJzU=np.einsum('jpa,pai->jpi',abs(z),eJU)/abs(U[None,:,0,None])
 RAW['operation_chart_JzU_envelope']=eJzU.copy()
 eJzz=np.maximum(eU[:,1:],abs(U[:,1:]))/abs(U[:,0,None])
 RAW['operation_chart_Jzz_envelope']=eJzz.copy()
 # EXACT order of the preexisting rational-chart actual/expected vectors.
 ordered=np.r_[eU.ravel(),ezt.ravel(),eJU.ravel(),eJzz.ravel(),eJzU.ravel(),
               abs(N),abs(ga),abs(c['dens'])]
 RAW['operation_chart_certificate_envelope']=ordered.copy()
 return dict(u_cov=eu,up=eup,rebuilt_U=eU,rebuilt_zt=ezt,JU=eJU,JzU=eJzU,Jzz=eJzz,
             certificate_envelope=ordered)


def momentum_envelope(s,c):
 # Propagate original covariant jets/projectors and additive momenta before cancellation.
 ce=chart_operation_envelopes(s,c);g,hi,U,z=s['g'],s['hi'],s['U'],s['z']
 euc=np.einsum('pab,pb->pa',abs(g),abs(U));eP=np.eye(4)[None]+np.einsum('pa,pb->pab',euc,abs(U))
 enu=s.get('operation_nu_envelope',abs(s['du'])+np.einsum('pbal,pl->pab',abs(s['Ga']),abs(U)))
 enz=s.get('operation_nz_envelope',abs(s['dz'])+np.einsum('plab,jpl->jpab',abs(s['Ga']),abs(z)))
 eV=np.einsum('pab,jpb->jpa',eP,np.einsum('pa,jpab->jpb',abs(U),enz))
 eD=np.einsum('pac,jpcd,pbd->jpab',eP,enz,eP)
 eg=lower_last(abs(g),enu);eF=eg+np.swapaxes(eg,1,2)
 eZ=np.einsum('j,jpa->pa',s['w'],abs(z))
 ePiU=ALPHA*np.einsum('pac,pcb->pab',abs(hi),eF)+np.einsum('pa,pb->pab',abs(U),eZ)
 ePi=s['w'][:,None,None,None]*(np.einsum('pa,jpb->jpab',abs(U),raise_cov(abs(hi),eV))/s['omega'][:,None,None,None]**2+ELL**2*np.einsum('pac,jpcd,pdb->jpab',abs(hi),eD,abs(hi)))
 RAW.update(operation_momentum_covariant_U_envelope=enu,operation_momentum_covariant_z_envelope=enz,operation_momentum_projector_envelope=eP,operation_momentum_PiU_envelope=ePiU,operation_momentum_Pi_envelope=ePi)
 pu=np.einsum('pa,pai->pi',ePiU[:,0],ce['JU'])+np.einsum('jp,jpi->pi',ePi[:,:,0,0],ce['JzU'])
 pz=ePi[:,:,0,1:]+ePi[:,:,0,0,None]*ce['Jzz'][None,:,:]
 return c['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(pu),96)),axis=1)


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


def arrowhead_blocks(s,c):
 # Full fixed-metric99 kinetic map, including every transverse azimuthal mode.
 U,P,hi=s['U'],s['P'],s['hi'];w,om=s['w'],s['omega']
 S=P[:,:,1:]+P[:,:,0,None]*c['Jzz'][:,None,:]
 T=P[None,:,:,0,None]*c['JzU'][:,:,None,:]
 cone=U[None,:,0]**2/om[:,None]**2-ELL**2*(hi[None,:,0,0]+U[None,:,0]**2)
 assert np.all(w>0) and np.all(cone>0) and np.all(c['N']>0)
 factor=c['dens'][None,:]*w[:,None]*cone
 gram=np.einsum('pai,pab,pbj->pij',S,hi,S)
 DD=factor[:,:,None,None]*gram[None]
 BB=factor[:,:,None,None]*np.einsum('jpai,pab,pbk->jpik',T,hi,S)
 AA_modes=factor[:,:,None,None]*np.einsum('jpai,pab,jpbk->jpik',T,hi,T)
 Maxwell=c['dens'][:,None,None]*ALPHA*c['ih']/c['N'][:,None,None]**2
 AA=Maxwell+AA_modes.sum(axis=0)
 RAW.update(arrowhead_S=S,arrowhead_T=T,arrowhead_native_cone=cone,arrowhead_factor=factor,arrowhead_transverse_Gram=gram,arrowhead_D=DD,arrowhead_B=BB,arrowhead_A_modes=AA_modes,arrowhead_A=AA,arrowhead_Maxwell_Schur=Maxwell)
 return dict(S=S,T=T,cone=cone,factor=factor,D=DD,B=BB,A_modes=AA_modes,A=AA,Maxwell=Maxwell)


def arrowhead_action(block,y):
 assert y.ndim==2 and y.shape[1]==99
 p=y.shape[0];uy=y[:,:3];zy=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 au=np.einsum('pik,pk->pi',block['A'],uy)+np.einsum('jpik,jpk->pi',block['B'],zy)
 az=np.einsum('jpki,pk->jpi',block['B'],uy)+np.einsum('jpik,jpk->jpi',block['D'],zy)
 return np.concatenate((au,az.transpose(1,0,2).reshape(p,96)),axis=1)


def arrowhead_solve(block,rhs):
 assert rhs.ndim==3 and rhs.shape[1]==99
 # No subtraction of enormous modal Grams to recover the Maxwell Schur.
 # The exact transverse-span identity must first be certified against saved M.
 p=rhs.shape[0];rr=rhs[:,3:].reshape(p,32,3,-1).transpose(1,0,2,3)
 dsolve=np.linalg.solve(block['D'],rr);RAW['arrowhead_modal_elimination']=dsolve.copy()
 reduced=rhs[:,:3]-np.einsum('jpik,jpkl->pil',block['B'],dsolve)
 RAW['arrowhead_reduced_U_rhs']=reduced.copy()
 yu=np.linalg.solve(block['Maxwell'],reduced);RAW['arrowhead_U_solution']=yu.copy()
 modal_rhs=rr-np.einsum('jpki,pkl->jpil',block['B'],yu)
 RAW['arrowhead_modal_rhs']=modal_rhs.copy()
 yz=np.linalg.solve(block['D'],modal_rhs);RAW['arrowhead_mode_solution']=yz.copy()
 y=np.concatenate((yu,yz.transpose(1,0,2,3).reshape(p,96,-1)),axis=1)
 RAW.update(arrowhead_rhs=rhs,arrowhead_modal_elimination=dsolve,arrowhead_reduced_U_rhs=reduced,arrowhead_U_solution=yu,arrowhead_mode_solution=yz,arrowhead_solution=y)
 return y


def adm_first_jets(s,c):
 dg=metric_partial(s);dhi=-np.einsum('pbc,pacd,pde->pabe',s['hi'],dg,s['hi'])
 dN=.5*c['N'][:,None]**3*dhi[:,:,0,0]
 dbeta=2*c['N'][:,None,None]*dN[:,:,None]*s['hi'][:,None,0,1:]+c['N'][:,None,None]**2*dhi[:,:,0,1:]
 return dict(dg=dg,dhi=dhi,dN=dN,dbeta=dbeta,dh=dg[:,:,1:,1:])


def lapse_shift_lift(s,c,f,df,b,db):
 # Fixed h_ij,U_i,z_ji, phi and their independent jets. b^i=delta beta^i.
 jets=adm_first_jets(s,c);N,h,beta,U,z=c['N'],c['h'],c['beta'],s['U'],s['z']
 dN,dh,dbe=jets['dN'],jets['dh'],jets['dbeta'];p=len(U)
 q=np.zeros((p,4,4));dq=np.zeros((p,4,4,4));eta=np.zeros((p,4));deta=np.zeros((p,4,4))
 q[:,0,0]=-2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b)
 q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:]
 dq[:,:,0,0]=-2*dN*f[:,None]-2*N[:,None]*df+2*np.einsum('pai,pij,pj->pa',dbe,h,b)+2*np.einsum('pi,paij,pj->pa',beta,dh,b)+2*np.einsum('pi,pij,paj->pa',beta,h,db)
 dq[:,:,0,1:]=np.einsum('paij,pj->pai',dh,b)+np.einsum('pij,paj->pai',h,db);dq[:,:,1:,0]=dq[:,:,0,1:]
 eta[:,0]=-U[:,0]*f/N;eta[:,1:]=-U[:,0,None]*b-beta*eta[:,0,None]
 deta[:,:,0]=-s['du'][:,:,0]*f[:,None]/N[:,None]-U[:,0,None]*df/N[:,None]+U[:,0,None]*f[:,None]*dN/N[:,None]**2
 deta[:,:,1:]=-s['du'][:,:,0,None]*b[:,None,:]-U[:,0,None,None]*db-dbe*eta[:,None,0,None]-beta[:,None,:]*deta[:,:,0,None]
 zeta=np.zeros_like(z);dzeta=np.zeros_like(s['dz']);ez=np.einsum('pa,jpa->jp',eta,z)
 zeta[:,:,0]=-ez/U[None,:,0]
 dzeta[:,:,:,0]=-(np.einsum('pab,jpb->jpa',deta,z)+np.einsum('pb,jpab->jpa',eta,s['dz']))/U[None,:,0,None]+ez[:,:,None]*s['du'][None,:,:,0]/U[None,:,0,None]**2
 RAW.update(constraint_test_lapse=f,constraint_test_lapse_partial=df,constraint_test_shift=b,constraint_test_shift_partial=db,constraint_metric_test=q,constraint_metric_test_partial=dq,constraint_U_chain=eta,constraint_U_chain_partial=deta,constraint_z_chain=zeta,constraint_z_chain_partial=dzeta)
 return dict(q=q,dq=dq,eta=eta,deta=deta,zeta=zeta,dzeta=dzeta,ADM_jets=jets)


def absolute_phase_metric_row(s,q,Pstar,Wstar):
 raised=raise_cov(s['hi'],s['phi']);X2=-covdot(s['hi'],s['phi'],s['phi'])
 dl=np.einsum('pa,pab,pb->p',raised,q,raised)/(2*X2)
 measure=np.einsum('pab,pba->p',s['hi'],q)/2
 value=Wstar*dl+Pstar*measure
 envelope=abs(Wstar)*np.einsum('pa,pab,pb->p',abs(raised),abs(q),abs(raised))/(2*X2)+abs(Pstar)*np.einsum('pab,pba->p',abs(s['hi']),abs(q))/2
 return value,envelope


def native_phase_constraint_direction(s,c,f,df,b,db,Pstar,Wstar,R):
 lift=lapse_shift_lift(s,c,f,df,b,db)
 native,en,*_=metric_native(s,lift['q'],lift['dq'],lift['eta'],lift['deta'])
 modal,me,*_=variation(s,np.zeros_like(s['U']),np.zeros_like(s['du']),lift['zeta'],lift['dzeta'])
 phase,pe=absolute_phase_metric_row(s,lift['q'],Pstar,Wstar)
 ratio=c['dens']/R
 action_components=ratio[:,None]*np.column_stack((native.sum(axis=1),modal.sum(axis=1),phase))
 envelope=ratio[:,None]*np.column_stack((en.sum(axis=1),me.sum(axis=1),pe))
 # Hamiltonian source derivative at fixed canonical state is minus action derivative.
 return dict(Hamiltonian_components=-action_components,action_components=action_components,envelope=envelope,lift=lift)


def spatial_generator_density(s,c,py,pmetric,p_phi,b,db,R):
 # Total metric momentum is native chart+connection PLUS EH in the same representative.
 jets=adm_first_jets(s,c);u=c['u'];zi=s['z'][:,:,1:]
 dUcov=np.einsum('pajm,pm->paj',jets['dg'][:,:,1:,:],s['U'])+np.einsum('pjm,pam->paj',s['g'][:,1:,:],s['du'])
 Lie_h=np.einsum('pk,pkij->pij',b,jets['dh'][:,1:])+np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])
 Lie_u=np.einsum('pk,pkj->pj',b,dUcov[:,1:])+np.einsum('pk,pjk->pj',u,db[:,1:])
 Lie_z=np.einsum('pk,jpkm->jpm',b,s['dz'][:,:,1:,1:])+np.einsum('jpk,pmk->jpm',zi,db[:,1:])
 metric=np.einsum('pij,pij->p',pmetric,Lie_h)
 preferred=np.einsum('pi,pi->p',py[:,:3],Lie_u)
 mode=np.einsum('jpi,jpi->p',py[:,3:].reshape(len(py),32,3).transpose(1,0,2),Lie_z)
 phase=p_phi*np.einsum('pi,pi->p',b,s['phi'][:,1:])
 return np.column_stack((metric,preferred,mode,phase))/R[:,None]


def spatial_curvature_weak_density(s,c,f,df,R):
 # Complete first-derivative R3 weak representative in flat cylindrical reference.
 # Output is divided by reference R. Integrate with the authentic R dR dZ weight.
 # Reflected internal sheet distributions belong to this global weak form once.
 jets=adm_first_jets(s,c);dh=jets['dh'][:,1:];ih=c['ih'];p=len(R)
 Ga=np.zeros((p,3,3,3))
 for i in range(3):
  for j in range(3):Ga[:,:,i,j]=np.einsum('plm,pm->pl',ih,dh[:,i,j,:]+dh[:,j,i,:]-dh[:,:,i,j])/2
 bar=np.zeros_like(Ga);bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 cc=Ga-bar;tr=np.einsum('plil->pi',cc)
 ratio=c['sqrt_h']/R;dratio=ratio[:,None]*np.einsum('pij,paij->pa',ih,dh)/2;dratio[:,0]-=ratio/R
 dih=-np.einsum('pij,pajk,pkl->pail',ih,dh,ih)
 V=f[:,None,None]*ratio[:,None,None]*ih
 DV=(df[:,1:]*ratio[:,None]+f[:,None]*dratio)[:,:,None,None]*ih[:,None]+f[:,None,None,None]*ratio[:,None,None,None]*dih
 DV+=np.einsum('pial,plj->paij',bar,V)+np.einsum('pjal,pil->paij',bar,V)
 aa=np.einsum('pkij,pk->pij',cc,tr)-np.einsum('plik,pkjl->pij',cc,cc)
 one=-np.einsum('plij,plij->p',DV,cc)
 two=np.einsum('pjij,pi->p',DV,tr)
 three=np.einsum('pij,pij->p',V,aa)
 eGa=np.zeros_like(Ga)
 for i in range(3):
  for j in range(3):eGa[:,:,i,j]=np.einsum('plm,pm->pl',abs(ih),abs(dh[:,i,j,:])+abs(dh[:,j,i,:])+abs(dh[:,:,i,j]))/2
 ecc=eGa+abs(bar);etr=np.einsum('plil->pi',ecc)
 edratio=ratio[:,None]*(np.einsum('pij,paij->pa',abs(ih),abs(dh))/2);edratio[:,0]+=ratio/R
 edih=np.einsum('pij,pajk,pkl->pail',abs(ih),abs(dh),abs(ih))
 eV=abs(f)[:,None,None]*ratio[:,None,None]*abs(ih)
 eDV=(abs(df[:,1:])*ratio[:,None]+abs(f[:,None])*edratio)[:,:,None,None]*abs(ih[:,None])+abs(f[:,None,None,None])*ratio[:,None,None,None]*edih
 eDV+=np.einsum('pial,plj->paij',abs(bar),eV)+np.einsum('pjal,pil->paij',abs(bar),eV)
 eaa=np.einsum('pkij,pk->pij',ecc,etr)+np.einsum('plik,pkjl->pij',ecc,ecc)
 envelope=np.einsum('plij,plij->p',eDV,ecc)+np.einsum('pjij,pi->p',eDV,etr)+np.einsum('pij,pij->p',eV,eaa)
 RAW.update(ADM_curvature_connection_envelope=ecc,ADM_curvature_V_envelope=eV,ADM_curvature_DV_envelope=eDV)
 RAW.update(ADM_spatial_connection=Ga,ADM_spatial_reference_connection=bar,ADM_spatial_connection_difference=cc,ADM_curvature_V=V,ADM_curvature_reference_DV=DV,ADM_curvature_terms=np.column_stack((one,two,three)),ADM_curvature_uncancelled_envelope=envelope)
 return dict(value=one+two+three,envelope=envelope,terms=np.column_stack((one,two,three)),unknown_outer_port=None,internal_sheet='reflected global weak distribution once; no added synthetic jump')


def EH_ADM_constraint_direction(s,c,f,df,b,db,R):
 curv=spatial_curvature_weak_density(s,c,f,df,R)
 ratio=c['sqrt_h']/R;K=c['K'];ih=c['ih'];Kt=c['Ktrace']
 K2=np.einsum('pij,pik,pjl,pkl->p',K,ih,ih,K)
 kinetic=ratio*f*(K2-Kt**2)/(2*C)
 # Positive Hamiltonian shift row from the full metric Lie derivative.
 jets=adm_first_jets(s,c)
 Lie_h=np.einsum('pk,pkij->pij',b,jets['dh'][:,1:])+np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])
 shift=np.einsum('pij,pij->p',c['pi_EH'],Lie_h)/R
 normal=kinetic-curv['value']/(2*C)
 ek=ratio*abs(f)*(np.einsum('pij,pik,pjl,pkl->p',abs(K),abs(ih),abs(ih),abs(K))+np.einsum('pij,pij->p',abs(ih),abs(K))**2)/(2*C)
 eLie=np.einsum('pk,pkij->pij',abs(b),abs(jets['dh'][:,1:]))+np.einsum('pik,pjk->pij',abs(c['h']),abs(db[:,1:]))+np.einsum('pkj,pik->pij',abs(c['h']),abs(db[:,1:]))
 es=np.einsum('pij,pij->p',abs(c['pi_EH']),eLie)/R
 return dict(normal=normal,shift=shift,normal_envelope=ek+curv['envelope']/(2*C),shift_envelope=es,curvature=curv,paired_GHY_time_port=None,outer_geometry_port=None)


def ordinary_canonical_constraint_rows(g,p_specific,mass_weight,f,b):
 o=ordinary_velocity(g,p_specific)
 normal=mass_weight*o['gamma']*f
 shift=-mass_weight*np.einsum('pi,pi->p',p_specific,b)
 return dict(normal=normal,shift=shift,gamma=o['gamma'],source_support='fixed owned razor-thin rest-mass annuli; no3D density or unknown activity extension')


def gauge_velocity_jet(s,c,dN,dbeta):
 p=len(s['U']);dbeta=np.broadcast_to(dbeta,(p,3));dN=np.broadcast_to(dN,(p,))
 dg=np.zeros((p,4,4,4));du=np.zeros((p,4,4));dz=np.zeros((32,p,4,4))
 dg[:,0,0,0]=-2*c['N']*dN+2*np.einsum('pi,pij,pj->p',c['beta'],c['h'],dbeta)
 dg[:,0,0,1:]=np.einsum('pij,pj->pi',c['h'],dbeta);dg[:,0,1:,0]=dg[:,0,0,1:]
 du[:,0,0]=-s['U'][:,0]*dN/c['N'];du[:,0,1:]=-dbeta*s['U'][:,0,None]-c['beta']*du[:,0,0,None]
 dz[:,:,0,0]=-np.einsum('jpa,pa->jp',s['z'],du[:,0])/s['U'][None,:,0]
 return du,dz,dg,connection_from_jet(s['hi'],dg)


def compact(R,Z,box):
 l,h=box;m=(l+h)/2;d=(h-l)/2;x=(R-m)/d;y=Z/16
 ok=(abs(x)<1)&(y<1)&(y>=0);f=(1-x*x)**3*(1-y*y)**3
 fr=-6*x/d*(1-x*x)**2*(1-y*y)**3;fz=-6*y/16*(1-y*y)**2*(1-x*x)**3
 return np.where(ok,f,0),np.where(ok,fr,0),np.where(ok,fz,0)


def arrowhead_original_envelope(block,y,rhs):
 if 'operation_A' in block:return arrowhead_original_operation_envelope(block,y,rhs)
 uy=abs(y[:,:3]);zy=abs(y[:,3:].reshape(len(y),32,3).transpose(1,0,2))
 eu=np.einsum('pik,pk->pi',abs(block['Maxwell'])+abs(block['A_modes']).sum(axis=0),uy)+np.einsum('jpik,jpk->pi',abs(block['B']),zy)
 ez=np.einsum('jpki,pk->jpi',abs(block['B']),uy)+np.einsum('jpik,jpk->jpi',abs(block['D']),zy)
 return np.concatenate((eu,ez.transpose(1,0,2).reshape(len(y),96)),axis=1)+abs(rhs)


def arrowhead_operation_envelopes(s,c,chartenv=None,label='current'):
 # If the producer already stored the admitted chart operation envelopes, pass
 # them here. Otherwise its owner may run that same positive helper once; this
 # neither reconstructs a signed kinetic Gram nor solves a modal block.
 if chartenv is None:chartenv=chart_operation_envelopes(s,c)
 U,g,hi=s['U'],s['g'],s['hi'];w,om=s['w'],s['omega']
 p=len(U);assert U.shape==(p,4) and g.shape==hi.shape==(p,4,4)
 assert w.shape==om.shape==(32,) and np.all(om>0) and np.all(w>0)
 assert chartenv['Jzz'].shape==(p,3) and chartenv['JzU'].shape==(32,p,3)
 out={}
 def keep(name,value):
  RAW['operation_arrowhead_'+label+'_'+name]=value.copy()
  out[name]=value
  assert np.issubdtype(value.dtype,np.number) and np.all(np.isfinite(value))
  assert np.all(value>=0)
  return value
 # P_a^b=delta_a^b+(g_ac U^c)U^b. Its magnitude must precede cancellation
 # in P_0^0 and in the compensated spatial-covector columns S and T.
 euc=keep('U_cov',np.einsum('pab,pb->pa',abs(g),abs(U)))
 eP=keep('P',np.eye(4)[None]+euc[:,:,None]*abs(U)[:,None,:])
 eS=keep('S',eP[:,:,1:]+eP[:,:,0,None]*chartenv['Jzz'][:,None,:])
 eT=keep('T',eP[None,:,:,0,None]*chartenv['JzU'][:,:,None,:])
 # The actual cone is U0^2/omega^2-ell^2(hi00+U0^2). Keep all three
 # terms positive here, including the inner hi00+U0^2 cancellation.
 eU02=abs(U[None,:,0])**2
 econe=keep('cone',eU02/abs(om[:,None])**2
             +ELL**2*(abs(hi[None,:,0,0])+eU02))
 efactor=keep('factor',abs(c['dens'])[None,:]*abs(w)[:,None]*econe)
 ehi=abs(hi)
 egram=keep('transverse_Gram',np.einsum('pai,pab,pbj->pij',eS,ehi,eS))
 eD=keep('D',efactor[:,:,None,None]*egram[None])
 eB=keep('B',efactor[:,:,None,None]
         *np.einsum('jpai,pab,pbk->jpik',eT,ehi,eS))
 eAm=keep('A_modes',efactor[:,:,None,None]
          *np.einsum('jpai,pab,jpbk->jpik',eT,ehi,eT))
 eMaxwell=keep('Maxwell',abs(c['dens'])[:,None,None]*abs(ALPHA)
               *abs(c['ih'])/abs(c['N'])[:,None,None]**2)
 keep('A',eMaxwell+eAm.sum(axis=0))
 return out

def arrowhead_operation_envelope_slice(envelope,index):
 # Explicit point-axis registration: generic bb's old default v[index] would
 # mis-index a newly attached modal envelope. Slice this dictionary separately.
 index=np.asarray(index,dtype=np.int64)
 assert index.ndim==1
 modal=('T','cone','factor','D','B','A_modes')
 return {name:(value[:,index] if name in modal else value[index])
         for name,value in envelope.items()}

def saved_span_operation_envelope(envelope,saved_T,saved_modal_A,
                                  old_modal_envelope,label='sample'):
 # Call with the eight-point envelope slice and the exact stored old witnesses.
 # old_modal_envelope is the SECOND (modal-A sized) slice of the old failed
 # control envelope: |A_old|+|B_old||Dinv_old||B_old|. No Dinv is recomputed.
 eS,eT,eAm=envelope['S'],envelope['T'],envelope['A_modes']
 assert saved_T.shape==eT.shape and saved_modal_A.shape==eAm.shape
 assert old_modal_envelope.shape==saved_modal_A.shape
 assert np.all(np.isfinite(old_modal_envelope)) and np.all(old_modal_envelope>=0)
 # Expected span is S_a^i T_i^k, where i=1..3 are the spatial rows of T.
 # Add the actual T magnitude only after retaining each underlying operation.
 espan=np.einsum('pai,jpik->jpak',eS,eT[:,:,1:,:])
 et=eT+espan+abs(saved_T)
 RAW['operation_arrowhead_'+label+'_span_product']=espan.copy()
 RAW['operation_arrowhead_'+label+'_span_control_envelope']=et.copy()
 # This deliberately keeps the complete old Schur-product bound, including
 # its old |A| term. Adding uncancelled EA avoids a subtraction/replacement
 # cancellation and does not make an independent claim about inverse error.
 es=old_modal_envelope+eAm
 RAW['operation_arrowhead_'+label+'_old_modal_control_envelope']=old_modal_envelope.copy()
 RAW['operation_arrowhead_'+label+'_modal_control_envelope']=es.copy()
 result=np.concatenate((et.ravel(),es.ravel()))
 assert np.all(np.isfinite(result)) and np.all(result>=0)
 return result

def span_operation_envelopes(s,c,block,index,oldenv):
 # Requested recovery interface. Only append positive bounds to the block;
 # none of its signed S/T/A/B/D/cone/factor/Maxwell entries is replaced.
 envelope=arrowhead_operation_envelopes(s,c)
 for name in ('A','B','D','A_modes','Maxwell'):
  block['operation_'+name]=envelope[name]
 index=np.asarray(index,dtype=np.int64);assert index.shape==(8,)
 e=arrowhead_operation_envelope_slice(envelope,index)
 saved_T=block['T'][:,index];saved_A=block['A_modes'][:,index]
 nT=saved_T.size;nA=saved_A.size
 oldenv=np.asarray(oldenv);assert oldenv.shape==(nT+nA,)
 oldes=oldenv[nT:].reshape(saved_A.shape)
 newenv=saved_span_operation_envelope(e,saved_T,saved_A,oldes)
 rawoperands={'operation_'+name:value for name,value in envelope.items()}
 rawoperands.update(operation_sample_indices=index.copy(),
                    operation_old_span_control_envelope=oldenv.copy(),
                    operation_old_modal_control_envelope=oldes.copy(),
                    operation_sample_span_control_envelope=newenv.copy())
 return newenv,rawoperands

def arrowhead_saved_action_operation_envelope(envelope,y,rhs):
 # Same 99 coordinates and original residual as arrowhead_original_envelope.
 # Use for each of seven saved Y columns and for every full-q owned-K residual.
 # Every signed A/B/D action remains the producer's original stored/action row.
 assert y.ndim==2 and y.shape[1]==99 and rhs.shape==y.shape
 p=len(y);uy=abs(y[:,:3]);zy=abs(y[:,3:].reshape(p,32,3).transpose(1,0,2))
 assert envelope['A'].shape==(p,3,3)
 assert envelope['B'].shape==envelope['D'].shape==(32,p,3,3)
 eu=np.einsum('pik,pk->pi',envelope['A'],uy)
 eu+=np.einsum('jpik,jpk->pi',envelope['B'],zy)
 ez=np.einsum('jpki,pk->jpi',envelope['B'],uy)
 ez+=np.einsum('jpik,jpk->jpi',envelope['D'],zy)
 result=np.concatenate((eu,ez.transpose(1,0,2).reshape(p,96)),axis=1)+abs(rhs)
 assert np.all(np.isfinite(result)) and np.all(result>=0)
 return result

def arrowhead_original_operation_envelope(block,y,rhs):
 # Positive block fields are installed by span_operation_envelopes at q0.
 # Install the same fields after arrowhead_operation_envelopes for q1..q3.
 # Old synthetic fixtures need not be replayed or re-registered.
 names=('A','B','D');assert all('operation_'+name in block for name in names)
 envelope={name:block['operation_'+name] for name in names}
 return arrowhead_saved_action_operation_envelope(envelope,y,rhs)


def certify_saved_arrowhead(s,c,block,old,label,failed_raw,old_pass,old_failure):
 index=old['sample_indices'].astype(np.int64);assert index.shape==(8,)
 # Exact carried original-M witness; no completed matrix/control is repeated.
 carry_completed_M(old_pass,failed_raw)
 key=f"raw_{old_failure['ordinal']:03d}_{old_failure['name']}_"
 actual=failed_raw[key+'actual'].copy();expected=failed_raw[key+'expected'].copy();oldenv=failed_raw[key+'envelope'].copy()
 T=failed_raw['arrowhead_sample_transverse_T'];Schur=failed_raw['arrowhead_sample_modal_Schur'];AA=failed_raw['arrowhead_sample_modal_A'];nspan=T.size
 assert np.array_equal(actual,np.concatenate((T.ravel(),AA.ravel())))
 assert np.array_equal(expected,np.concatenate((failed_raw['arrowhead_sample_transverse_span'].ravel(),Schur.ravel())))
 envelope,operands=span_operation_envelopes(s,c,block,index,oldenv)
 ARM_AVAILABLE.update({label+'_span_'+name:value.copy() for name,value in operands.items()})
 ARM_AVAILABLE.update({label+'_old_span_actual':actual,label+'_old_span_expected':expected,label+'_old_span_envelope':oldenv,label+'_recovered_span_envelope':envelope})
 # Same original signed operands and same2e-11. Four old FALSE outcomes stay in
 # ancestry unchanged; this newly qualified arithmetic check uses honest bounds.
 scaled_check(label+'_exact_transverse_span_and_Maxwell_Schur',actual,expected,envelope)
 # Reuse every saved solved velocity column as an ORIGINAL-M action certificate;
 # no saved105 Hessian, inverse or eigensystem is regenerated.
 modal=('T','cone','factor','D','B','A_modes','operation_B','operation_D','operation_A_modes')
 bb={k:(v[:,index] if k in modal else v[index]) for k,v in block.items()}
 Y=old['all_velocity_response'];expected=old['original_M_action']
 action=np.stack([arrowhead_action(bb,Y[:,:,k]) for k in range(Y.shape[-1])],axis=-1)
 env=np.stack([arrowhead_original_envelope(bb,Y[:,:,k],expected[:,:,k]) for k in range(Y.shape[-1])],axis=-1)
 ARM_AVAILABLE.update(arrowhead_saved_velocity_columns=Y.copy(),arrowhead_saved_original_action=expected.copy(),arrowhead_saved_block_action=action,arrowhead_saved_block_action_envelope=env)
 scaled_check(label+'_saved_seven_column_original_action',action,expected,env)


def reconstruct_owned_K(s,c,block,Hbar,label):
 # Prescribed initial K increment only: all metric positions and all native p stay
 # fixed. This does not hold the old total metric p fixed or earn a history.
 kten=2*c['N'][:,None,None]*Hbar*c['h']
 k=np.column_stack((kten[:,0,0],kten[:,1,1],kten[:,2,2],kten[:,0,1],kten[:,0,2],kten[:,1,2]))
 py,ph=reduced_momenta(s,c);du,dz,dg,dGa=native_velocity_jet(s,c,np.zeros((len(py),99)),k)
 kt=kinetic_tangent(s,du,dz,dGa);delta,_=reduced_momenta(s,c,kt['delta_PiU'],kt['delta_Pi'],kt['delta_Ctime'])
 ARM_AVAILABLE.update({label+'owned_hdot_tensor':kten,label+'owned_hdot_coordinates':k,label+'old_native_canonical_momentum':py,label+'metric_only_native_momentum_delta':delta})
 y=arrowhead_solve(block,-delta[:,:,None])[:,:,0]
 ARM_AVAILABLE[label+'reconstructed_native_velocity_delta']=y.copy()
 action=arrowhead_action(block,y);env=arrowhead_original_envelope(block,y,-delta)
 ARM_AVAILABLE.update({label+'original_native_block_action':action,label+'original_native_rhs':-delta,label+'original_native_residual':action+delta,label+'original_native_residual_envelope':env})
 du,dz,dg,dGa=native_velocity_jet(s,c,y,k)
 new=features(s['g'],s['hi'],s['Ga']+dGa,s['U'],s['du']+du,s['z'],s['dz']+dz,s['phi'],s['omega'],s['xi'],s['w']);nc=adm_chart(new)
 nmp,nph=reduced_momenta(new,nc);m_env=momentum_envelope(new,nc)+momentum_envelope(s,c)
 constraints=np.concatenate((np.einsum('pa,pa->p',new['uc'],new['U'])+1,np.einsum('pa,jpa->jp',new['U'],new['z']).ravel(),2*np.einsum('pab,pb->pa',lower_last(new['g'],new['nu']),new['U']).ravel(),(np.einsum('pab,jpb->jpa',new['nu'],new['z'])+np.einsum('pb,jpab->jpa',new['U'],new['nz'])).ravel()))
 # Operation bounds, not normalization by exact-zero cancellation remainders.
 unenv=abs(new['du'])+np.einsum('pbal,pl->pab',abs(new['Ga']),abs(new['U']))
 znenv=abs(new['dz'])+np.einsum('plab,jpl->jpab',abs(new['Ga']),abs(new['z']))
 cenv=np.concatenate((np.einsum('pa,pa->p',abs(new['uc']),abs(new['U']))+1,np.einsum('pa,jpa->jp',abs(new['U']),abs(new['z'])).ravel(),(2*np.einsum('pab,pb->pa',lower_last(abs(new['g']),unenv),abs(new['U']))).ravel(),(np.einsum('pab,jpb->jpa',unenv,abs(new['z']))+np.einsum('pb,jpab->jpa',abs(new['U']),znenv)).ravel()))
 Kgap=nc['K']-c['K'];Kexpected=Hbar*c['h'];Kenv=abs(nc['K'])+abs(c['K'])+abs(Kexpected)
 for key,value in dict(native_p=nmp,metric_native_p=nph,metric_EH_p=nc['pi_EH'],metric_total_p=symmetric_tensor_from_coordinates(nph)+nc['pi_EH'],du_increment=du,dz_increment=dz,dg_increment=dg,connection_increment=dGa,new_K=nc['K'],old_K=c['K'],K_increment=Kgap,K_expected=Kexpected,native_p_reconstruction_envelope=m_env,constraints=constraints,constraint_envelope=cenv).items():ARM_AVAILABLE[label+key]=value.copy()
 return new,nc,dict(action=action,rhs=-delta,action_envelope=env,native_p=nmp,old_native_p=py,momentum_envelope=m_env,constraints=constraints,constraint_envelope=cenv,Kgap=Kgap,Kexpected=Kexpected,Kenv=Kenv)


def adm_probe(R,Z,box,direction):
 f,fr,fz=compact(R,Z,box);p=len(R);df=np.zeros((p,4));df[:,1]=fr;df[:,2]=fz
 b=np.zeros((p,3));db=np.zeros((p,4,3))
 if direction==0:return f,df,b,db
 if direction==1:b[:,0]=f;db[:,:,0]=df
 if direction==2:
  b[:,1]=Z*f/16;db[:,:,1]=Z[:,None]*df/16;db[:,2,1]+=f/16
 if direction==3:
  b[:,2]=f/R;db[:,:,2]=df/R[:,None];db[:,1,2]-=f/R**2
 return np.zeros(p),np.zeros((p,4)),b,db


def constraint_arm(case,metric_case,ordinary_case,fixed,cp,failed_case):
 global RAW,ARM_AVAILABLE
 RAW={};ARM_AVAILABLE={};start=len(CHECKS);sig=case['sigma'];Hbar=fixed['Hunit']/LIGHT*cp['background']['h'];CONTEXT.update(stage='canonical_constraints',sigma=sig)
 oldnames=('sample_indices','native_M','kinetic_envelope','all_velocity_response','original_M_action')
 failed_raw=read_failed_raw(failed_case['checkpoint']);ARM_AVAILABLE.update({'failed_V001_'+name:value.copy() for name,value in failed_raw.items()})
 old=selected_arrays_any(case['checkpoint']['file'],oldnames)
 totals=np.zeros((2,4,5));envelopes=np.zeros_like(totals);gen_totals=np.zeros((2,4,4));AR=ARM_AVAILABLE
 controls={k:[[],[],[]] for k in ('original_block_residual','fixed_native_p','unit_transverse_and_K','phase_instant')}
 for iq in range(4):
  RAW={};label=f'q{iq}_';names=[label+x for x in ('R','Z','g','hi','Ga','U','du','z','dz','phi','reference_volume')]+['xi','weights','omega_star']+[f'b0_d0_q{iq}_'+x for x in ('Wstar','Pstar','phase_u_chart')]
  if iq==0:
   vals={name:failed_raw['loaded_'+name].copy() for name in names}
   feature_names=('g','hi','Ga','U','du','z','dz','phi','omega','xi','w','nu','nz','uc','P','q','V','D','a','r','f','z2','Pi','mu','Z','F','Fup','PiU','A')
   s={name:failed_raw['current_'+name].copy() for name in feature_names}
   # The uncheckpointed chart alone is reconstructed algebraically; all saved
   # primitive/features/fixedmetric blocks are authoritative and reused exactly.
   c=adm_chart(s)
   block={name:failed_raw['arrowhead_'+alias].copy() for name,alias in (('S','S'),('T','T'),('cone','native_cone'),('factor','factor'),('D','D'),('B','B'),('A_modes','A_modes'),('A','A'),('Maxwell','Maxwell_Schur'))}
  else:
   vals=selected_arrays(metric_case['checkpoint']['file'],names)
   s=features(vals[label+'g'],vals[label+'hi'],vals[label+'Ga'],vals[label+'U'],vals[label+'du'],vals[label+'z'],vals[label+'dz'],vals[label+'phi'],vals['omega_star'],vals['xi'],vals['weights']);c=adm_chart(s);block=arrowhead_blocks(s,c)
   op=arrowhead_operation_envelopes(s,c,label=f'q{iq}')
   for name in ('A','B','D','A_modes','Maxwell'):block['operation_'+name]=op[name]
   ARM_AVAILABLE.update({label+'operation_'+name:value.copy() for name,value in op.items()})
  R,Z,dv=vals[label+'R'],vals[label+'Z'],vals[label+'reference_volume'];assert R.shape==Z.shape==dv.shape==((1972,1972,1938,1938)[iq],) and np.all(R>0) and np.all(dv>0)
  if iq==0:certify_saved_arrowhead(s,c,block,old,f's{sig}',failed_raw,*failed_case['checkpoint']['metadata']['controls'])
  n,nc,cert=reconstruct_owned_K(s,c,block,Hbar,label)
  phase=phase_inventory(s,vals[f'b0_d0_q{iq}_Wstar'],vals[f'b0_d0_q{iq}_phase_u_chart'],fixed)
  np0=phase_momentum(n,phase['P_X'],phase['P_XX'])[0]
  for key,a,e,v in (('original_block_residual',cert['action'],cert['rhs'],cert['action_envelope']),('fixed_native_p',cert['native_p'],cert['old_native_p'],cert['momentum_envelope']),('unit_transverse_and_K',np.concatenate((cert['constraints'],cert['Kgap'].ravel())),np.concatenate((np.zeros_like(cert['constraints']),cert['Kexpected'].ravel())),np.concatenate((cert['constraint_envelope'],cert['Kenv'].ravel()))),('phase_instant',np0,phase['p_phi'],abs(np0)+abs(phase['p_phi']))):
   controls[key][0].append(a.ravel());controls[key][1].append(e.ravel());controls[key][2].append(v.ravel())
  pmetric=symmetric_tensor_from_coordinates(AR[label+'metric_native_p'])+nc['pi_EH']
  for key,value in dict(R=R,Z_coordinate=Z,reference_volume=dv,chart_N=nc['N'],chart_beta=nc['beta'],chart_density=nc['dens'],phase_p=phase['p_phi'],phase_P_X=phase['P_X'],phase_P_XX=phase['P_XX'],phase_Pstar=vals[f'b0_d0_q{iq}_Pstar'],phase_Wstar=vals[f'b0_d0_q{iq}_Wstar'],mode_temporal_cone=block['cone'],arrowhead_A=block['A'],arrowhead_B=block['B'],arrowhead_D=block['D'],arrowhead_Maxwell=block['Maxwell']).items():AR[label+key]=value.copy()
  for ib,box in enumerate(BOXES):
   for direction in range(4):
    tag=f'b{ib}_a{direction}_q{iq}_';CONTEXT.update(quadrature=iq,rectangle=ib,direction=direction)
    f,df,b,db=adm_probe(R,Z,box,direction)
    src=native_phase_constraint_direction(n,nc,f,df,b,db,vals[f'b0_d0_q{iq}_Pstar'],vals[f'b0_d0_q{iq}_Wstar'],R)
    eh=EH_ADM_constraint_direction(n,nc,f,df,b,db,R)
    density=np.column_stack((src['Hamiltonian_components'],eh['normal']+eh['shift']))
    denv=np.column_stack((src['envelope'],eh['normal_envelope']+eh['shift_envelope']))
    gen=spatial_generator_density(n,nc,cert['native_p'],pmetric,phase['p_phi'],b,db,R)
    totals[ib,direction,:4]+=np.einsum('p,pk->k',dv,density);envelopes[ib,direction,:4]+=np.einsum('p,pk->k',dv,denv);gen_totals[ib,direction]+=np.einsum('p,pk->k',dv,gen)
    for key,value in dict(f=f,df=df,b=b,db=db,metric_test=src['lift']['q'],metric_test_partial=src['lift']['dq'],U_chain=src['lift']['eta'],U_chain_partial=src['lift']['deta'],Hamiltonian_signed_density=density,uncancelled_density_envelope=denv,canonical_spatial_generator_density=gen,EH_curvature_terms=eh['curvature']['terms'],EH_curvature_envelope=eh['curvature']['envelope']).items():AR[tag+key]=value.copy()
    # Pointwise rows and integrated direct-generator differences are measures,
    # not on-shell/null/gauge certificates. The paired temporal improvement
    # and source ports remain separate when a noncompact continuation is used.
    AR[tag+'direct_minus_generator']=density.sum(axis=1)-gen.sum(axis=1)
  # Raw phase and native momentum fields are stored once per quadrature;
  # probe-derived full mode jets are reconstructible and not duplicated.
  AR[label+'new_native_Pi']=n['Pi'].copy();AR[label+'new_native_PiU']=n['PiU'].copy();AR[label+'new_metric_connection_momentum']=connection_momentum(n)[0][:,0].copy()
  AR.update({key:value.copy() for key,value in RAW.items() if key.startswith(('control_','raw_'))})
 for key,(a,e,v) in controls.items():scaled_check(f's{sig}_{key}',np.concatenate(a),np.concatenate(e),np.concatenate(v))
 sv=selected_arrays(ordinary_case['checkpoint']['file'],('source_g','source_k','source_D','p_phi','mass_weight'));sv.update(selected_arrays(metric_case['checkpoint']['file'],('source_R','source_Z')));sg=sv['source_g'];specific=np.zeros((len(sg),3));specific[:,2]=sv['p_phi'];oc=ordinary_velocity(sg,specific)
 AR.update(ordinary_g=sg.copy(),ordinary_specific_p=specific,ordinary_mass_weight=sv['mass_weight'].copy(),ordinary_source_k=sv['source_k'].copy(),ordinary_source_D=sv['source_D'].copy(),ordinary_U=oc['u_M'].copy(),ordinary_gamma=oc['gamma'].copy())
 av=[];ev=[];ee=[]
 for ib,box in enumerate(BOXES):
  for direction in range(4):
   f,df,b,db=adm_probe(sv['source_R'],sv['source_Z'],box,direction);rows=ordinary_canonical_constraint_rows(sg,specific,sv['mass_weight'],f,b)
   hi=np.linalg.inv(sg);N=1/np.sqrt(-hi[:,0,0]);beta=N[:,None]**2*hi[:,0,1:];h=sg[:,1:,1:]
   qq=np.zeros_like(sg);qq[:,0,0]=-2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b);qq[:,0,1:]=np.einsum('pij,pj->pi',h,b);qq[:,1:,0]=qq[:,0,1:]
   oldk=sv['source_k'];D=sv['source_D'];direct=-sv['mass_weight']*np.einsum('pa,pab,pb->p',oldk,qq,oldk)/(2*np.sqrt(D))
   expected=rows['normal']+rows['shift'];env=abs(sv['mass_weight'])*np.einsum('pa,pab,pb->p',abs(oldk),abs(qq),abs(oldk))/(2*np.sqrt(D))+abs(rows['normal'])+abs(rows['shift'])
   av.append(direct);ev.append(expected);ee.append(env);totals[ib,direction,4]=expected.sum();envelopes[ib,direction,4]=env.sum()
   tag=f'b{ib}_a{direction}_source_';AR.update({tag+key:value.copy() for key,value in dict(f=f,b=b,metric_test=qq,action_derived_Hamiltonian=direct,canonical_Hamiltonian=expected,normal=rows['normal'],shift=rows['shift'],envelope=env).items()})
 scaled_check(f's{sig}_ordinary_same_worldline_canonical_constraints',np.concatenate(av),np.concatenate(ev),np.concatenate(ee))
 AR.update(weak_constraint_components=totals,weak_constraint_uncancelled_envelopes=envelopes,canonical_generator_components=gen_totals,weak_constraint_totals=totals.sum(axis=-1),direct_shift_minus_generator=totals[:,1:,:4].sum(axis=-1)-gen_totals[:,1:].sum(axis=-1))
 again=np.zeros_like(totals)
 for ib in range(2):
  for direction in range(4):
   for iq in range(4):again[ib,direction,:4]+=np.einsum('p,pk->k',AR[f'q{iq}_reference_volume'],AR[f'b{ib}_a{direction}_q{iq}_Hamiltonian_signed_density'])
   again[ib,direction,4]=AR[f'b{ib}_a{direction}_source_canonical_Hamiltonian'].sum()
 scaled_check(f's{sig}_independent_saved_density_recontraction',again,totals,envelopes+abs(totals))
 AR.update({key:value.copy() for key,value in RAW.items() if key.startswith(('control_','raw_'))})
 rec=checkpoint('ARM',AR,dict(kind='conditional_complete_canonical_compact_weak_normal_shift_prerequisite',sigma=sig,controls=CHECKS[start:],canonical_parent_file=case['checkpoint']['file'],canonical_parent_sha256=case['checkpoint']['sha256'],metric_parent_file=metric_case['checkpoint']['file'],metric_parent_sha256=metric_case['checkpoint']['sha256'],ordinary_parent_file=ordinary_case['checkpoint']['file'],ordinary_parent_sha256=ordinary_case['checkpoint']['sha256'],owned_Hbar=Hbar,point_count=7820,quad_columns=4,all32_modes=True,fixed_native_p=True,metric_p_independently_fixed=False,initial_K_increment='2 N Hbar h coordinate metric rate; local conditional Cauchy prescription, not inferred physical history',normal_and_shift_component_names=['native_metric','mode_constraint_compensation','absolute_phase','EH_ADM','ordinary_annuli'],sheet_scope='global reflected weak form and owned half annuli once; no synthetic internal jump',unknowns=dict(full_Cauchy_slice=None,CMC_solve=None,metric_boundary=None,full_normal_time_improvement=None,ordinary_Euler_evolution=None,local_cosmic_ordinary_state=None,phase_history=None,active_outside_measurement=None),physical_changes=[]))
 ARM_AVAILABLE={};RAW={}
 return dict(sigma=sig,status='CONDITIONAL_COMPACT_CANONICAL_CONSTRAINT_SOURCE',checkpoint=rec,qualification=FLAGS)


# PRIVATE TEXT-ONLY FRAGMENT. Do not execute during authoring or edit a parent.
# Integrate with existing path/sha/checkpoint/recheck helpers and PINS/STEM/
# PROTOCOL_SHA. Admission uses only stdlib; selected_arrays is ROOT-runtime only.
# Add stdlib zipfile and struct imports. Publish compact references, not parent
# RESULT/checkpoint metadata recursively. All32 modes/all4 quadrature columns.
METRIC='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
ORDINARY='CROSS_U_SAVED_ROTATING_SHEET_FRECHET_V001'
CONSTRAINT_ADMISSION_PINS={
 'cross_u_saved_full_native_adm_legendre_v002.py':'9185f2dcd981d7599023858dd8c533b13a510c150ad994b5ea3f569b947d9de0',
 'CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002.md':'e8529df3d5c3997f3120a0d483e035493517514ddeaaa3e55834e811006d81e3',
 'CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002_RESULT.json':'4d4c9e89520390db932b66548aed361607abcc70b48d422502a3f53af9d06fb6',
 'CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002_RECEIPT.json':'4a21c59742252d7fcaaccfd7b9371fa846bc1d248579ae9408a9838ae971b99e',
 'cross_u_saved_full_metric_native_source_residual_v001.py':'23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68',
 METRIC+'.md':'88fbf64e1568af3f47f1346b809c6d8a35fe7b685a73817938616b9056068e24',
 METRIC+'_RESULT.json':'ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798',
 METRIC+'_RECEIPT.json':'eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde',
 'cross_u_saved_rotating_sheet_frechet_v001.py':'ab56dd280d6317699fe38e7b5499d1e25b214197b1d3d1db8a598ad271dc72da',
 ORDINARY+'.md':'e1ea987af25cf02dab2460e555f59b13691fefee254e83e1789a1c3a28281f05',
 ORDINARY+'_RESULT.json':'e62722bbff40d0f063d3a80e2467b06d7d4d305dd304140efced5add000fe929',
 ORDINARY+'_RECEIPT.json':'f24459d3dfffbfd773323ba69c375ac8f08bda5e121d2f530dc156c1955fb6d7'}

LEGENDRE_SELECTED={
 'xi':[32],'weights':[32],'omega_star':[32],'q0_R':[1972],'q0_Z_coordinate':[1972],
 'chart_Ui':[1972,3],'chart_zi':[32,1972,3],'chart_velocity':[1972,99],
 'native_canonical_momentum':[1972,99],'metric_native_momentum_symmetric_coordinates':[1972,6],
 'metric_native_canonical_momentum_tensor':[1972,3,3],'metric_total_canonical_momentum_tensor':[1972,3,3],
 'metric_EH_momentum_tensor':[1972,3,3],'trial_K_tensor':[1972,3,3],'trial_Ktrace':[1972],
 'chart_density':[1972],'chart_N':[1972],'chart_beta':[1972,3],
 'native_M':[8,99,99],'kinetic_envelope':[8,105,105],'original_M_action':[8,99,7],'native_metric_B':[8,99,6],'native_metric_T':[8,6,6],
 'native_base_momentum':[8,99],'metric_base_native_momentum':[8,6],
 'native_velocity_response':[8,99,6],'all_velocity_response':[8,99,7],
 'reconstructed_native_momentum':[8,99,7],'reconstructed_metric_native_momentum':[8,6,7],
 'sample_indices':[8],'sample_g':[8,4,4],'sample_hi':[8,4,4],'sample_Ga':[8,4,4,4],
 'sample_U':[8,4],'sample_du':[8,4,4],'sample_z':[32,8,4],'sample_dz':[32,8,4,4],
 'sample_phi':[8,4],'sample_JU':[8,4,3],'sample_JzU':[32,8,3],'sample_Jzz':[8,3],
 'sample_metric_embedding':[8,6,4,4],'sample_U_metric_chain':[8,6,4],
 'sample_zt_metric_chain':[32,8,6],'sample_density':[8],'sample_K':[8,3,3],
 'sample_pi_EH':[8,3,3],'owned_isotropic_hdot':[8,3,3],'owned_isotropic_coefficients':[8,6],
 'reconstructed_du':[7,8,4,4],'reconstructed_dz':[7,32,8,4,4],
 'reconstructed_dg':[7,8,4,4,4],'reconstructed_connection':[7,8,4,4,4],
 'p_phi':[1972],'P_X':[1972],'P_XX':[1972],'phase_u':[1972],'X':[1972],
 'ordinary_specific_covariant_momentum':[4832,3],'ordinary_mass_weight':[4832]}
Q_SELECTED={
 'R':[1972],'Z':[1972],'reference_volume':[1972],
 'g':[1972,4,4],'hi':[1972,4,4],'Ga':[1972,4,4,4],
 'U':[1972,4],'du':[1972,4,4],'z':[32,1972,4],'dz':[32,1972,4,4],
 'phi':[1972,4],'Pi':[32,1972,4,4],'PiU':[1972,4,4],'mu':[32,1972],
 'V':[32,1972,4],'D':[32,1972,4,4],'a':[1972,4],'r':[1972,4]}
Q_COUNTS=(1972,1972,1938,1938)
SOURCE_GEOMETRY_SELECTED={'source_R':[4832],'source_Z':[4832],'source_g':[4832,4,4],
 'source_hi':[4832,4,4],'source_Ga':[4832,4,4,4],'source_gr':[4832,4],
 'source_k':[4832,4],'source_D':[4832],'source_n':[4832],'source_Gamma':[4832],
 'source_rho':[4832],'source_held_Omega0':[4832]}
ORDINARY_SELECTED={'source_g':[4832,4,4],'source_k':[4832,4],'source_D':[4832],
 'p_phi':[4832],'mass_weight':[4832]}


def admission():
 pins={}
 def add(n,h):
  n=str(path(n).resolve());assert isinstance(h,str) and len(h)==64
  assert n not in pins or pins[n]==h,('Conflicting input seal',n);pins[n]=h
 for table in (CONSTRAINT_ADMISSION_PINS,PINS):
  for n,h in table.items():add(n,h)
 add(STEM+'.md',PROTOCOL_SHA);add(__file__,sha(__file__))
 specs=((PARENT,20012,'cross_u_saved_full_native_adm_legendre_v002.py',
         'CONDITIONAL_COMPACT_LEGENDRE_ARITHMETIC_PASS',60,'CONDITIONAL_COMPACT_LEGENDRE_PREREQUISITE'),
        (METRIC,13990,'cross_u_saved_full_metric_native_source_residual_v001.py',
         'CONDITIONAL_FULL_METRIC_WEAK_MEASURES_ARITHMETIC_PASS',36,'CONDITIONAL_FULL_METRIC_WEAK_MEASURES'),
        (ORDINARY,15580,'cross_u_saved_rotating_sheet_frechet_v001.py',
         'CONDITIONAL_ORDINARY_SOURCE_FRECHET_ARITHMETIC_PASS',19,'CONDITIONAL_ORDINARY_SOURCE_FRECHET_BLOCK'))
 results={};receipts={}
 for stem,pid,source,status,count,cs in specs:
  rc=json.loads(path(stem+'_RECEIPT.json').read_text());assert rc['status']=='CLOSED' and rc['closed']
  assert rc['owner']['owner']=='root' and rc['owner']['pid']==pid and rc['owner']['source_file']==source
  assert rc['owner']['source_sha256']==CONSTRAINT_ADMISSION_PINS[source]
  assert rc['result_sha256']==CONSTRAINT_ADMISSION_PINS[stem+'_RESULT.json']
  assert all(v is False for v in rc['qualification'].values())
  for field in ('input_sha256','output_sha256'):
   for n,h in rc[field].items():add(n,h)
  assert path(stem+'_RESULT.json').stat().st_size<32*1024*1024
  result=json.loads(path(stem+'_RESULT.json').read_text())
  assert result['owner']==rc['owner'] and result['status']==status
  assert json.loads(path(stem+'_OWNER_START.json').read_text())==rc['owner']
  ma=json.loads(path(stem+'_MANIFEST.json').read_text());assert ma['owner']==rc['owner'] and ma['input_sha256']==rc['input_sha256']
  assert len(result['controls'])==count and all(c['passed'] is True for c in result['controls'])
  assert [c['sigma'] for c in result['cases']]==list(SIGMAS) and len(result['checkpoints'])==6
  assert all(v is False for v in result['qualification'].values()) and not path(stem+'_ERROR.json').exists()
  for r in result['checkpoints']:
   assert r['commit_file']==r['file']+'.COMMIT.json'
   assert json.loads(path(r['commit_file']).read_text())=={k:v for k,v in r.items() if k not in ('commit_file','commit_sha256')}
   assert pins[str(path(r['file']).resolve())]==r['sha256'] and pins[str(path(r['commit_file']).resolve())]==r['commit_sha256']
   assert r['metadata']['owner']==rc['owner'] and all(v is False for v in r['metadata']['qualification'].values())
  assert {p.name for p in BASE.glob(stem+'_*.npz')}=={r['file'] for r in result['checkpoints']}
  assert {p.name for p in BASE.glob(stem+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in result['checkpoints']}
  for c in result['cases']:
   assert c['status']==cs and c['checkpoint'] in result['checkpoints']
   assert c['checkpoint']['metadata']['sigma']==c['sigma'] and all(v is False for v in c['qualification'].values())
  results[stem]=result;receipts[stem]=rc
 for n,h in pins.items():assert sha(path(n))==h,('Input seal changed',n)
 parent,metric,ordinary=results[PARENT],results[METRIC],results[ORDINARY]
 assert parent['copied_completed_control_count']==6 and parent['recovery_changes']==['uncancelled operation envelopes only']
 old=parent['copied_failed_controls'];assert len(old)==7 and [c['passed'] for c in old]==[True]*6+[False]
 assert parent['controls'][:6]==old[:6] and old[6]['ordinal']==6 and old[6]['error']==1.
 fixed=dict(metric['checkpoints'][0]['metadata']['owned_fixed'])
 assert parent['checkpoints'][0]['metadata']['fixed']==fixed
 assert parent['checkpoints'][0]['metadata']['copied_metric_controls']==metric['controls']
 assert parent['checkpoints'][0]['metadata']['copied_ordinary_controls']==ordinary['controls']
 cpname='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json'
 sharedname='CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json'
 assert str(path(cpname).resolve()) in pins and str(path(sharedname).resolve()) in pins
 cp=json.loads(path(cpname).read_text());shared=json.loads(path(sharedname).read_text())
 assert cp==next(r for r in shared['rows'] if r['eps']==1e-5)
 shared_fixed=dict(shared['manifest']['fixed_parent']);shared_fixed['eps']=1e-5
 assert fixed==shared_fixed and fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 assert parent['checkpoints'][0]['metadata']['owned_EPS5_background']==cp['background']
 selected={}
 def schema(rec,fields):
  for n,shape in fields.items():
   dtype='int64' if n=='sample_indices' else 'float64'
   assert rec['metadata']['schema'][n]==dict(shape=shape,dtype=dtype,finite=True),(rec['file'],n)
  selected.setdefault(rec['file'],(rec,[]))[1].extend(fields)
 schema(parent['checkpoints'][0],{'xi':[32],'weights':[32]})
 schema(metric['checkpoints'][0],{'r_kpc':[87],'z_kpc':[45],'final_state':[65,87,45],
                               'xi':[32],'weights':[32],'source_samples32':[4832,9]})
 schema(ordinary['checkpoints'][0],{'source_samples32':[4832,9]})
 for pc,mc,oc in zip(parent['cases'],metric['cases'],ordinary['cases']):
  assert pc['sigma']==mc['sigma']==oc['sigma'];pr,mr,orr=pc['checkpoint'],mc['checkpoint'],oc['checkpoint']
  assert pr['metadata']['parent_file']==mr['file'] and pr['metadata']['parent_sha256']==mr['sha256']
  assert pr['metadata']['ordinary_parent_file']==orr['file'] and pr['metadata']['ordinary_parent_sha256']==orr['sha256']
  assert orr['metadata']['parent_file']==mr['file'] and orr['metadata']['parent_sha256']==mr['sha256']
  assert pr['metadata']['local_point_indices']==[k*1971//7 for k in range(8)]
  assert pr['metadata']['physical_changes']==[] and pr['metadata']['compact_point_count']==1972
  schema(pr,LEGENDRE_SELECTED);schema(mr,SOURCE_GEOMETRY_SELECTED)
  schema(mr,{'xi':[32],'weights':[32],'omega_star':[32]});schema(orr,ORDINARY_SELECTED)
  for q in range(4):
   nq=Q_COUNTS[q]
   schema(mr,{f'q{q}_'+n:[nq if d==1972 else d for d in s] for n,s in Q_SELECTED.items()})
   schema(mr,{f'b0_d0_q{q}_'+n:[nq] for n in ('Pstar','Wstar','phase_u_chart','X2')})
 for rec,names in selected.values():
  with zipfile.ZipFile(path(rec['file'])) as z:
   assert set(z.namelist())=={n+'.npy' for n in rec['metadata']['schema']}|{'metadata_json.npy'}
   def header(f):
    assert f.read(6)==b'\x93NUMPY';v=f.read(2);assert v in (b'\x01\x00',b'\x02\x00',b'\x03\x00')
    size=struct.unpack('<H' if v==b'\x01\x00' else '<I',f.read(2 if v==b'\x01\x00' else 4))[0]
    return ast.literal_eval(f.read(size).decode('utf8' if v==b'\x03\x00' else 'latin1'))
   with z.open('metadata_json.npy') as f:
    hd=header(f);assert hd['shape']==() and hd['descr'].startswith('<U')
    assert json.loads(f.read().decode('utf-32-le').rstrip('\x00'))==rec['metadata']
   for n in set(names):
    with z.open(n+'.npy') as f:hd=header(f)
    d=rec['metadata']['schema'][n]
    assert list(hd['shape'])==d['shape'] and hd['descr']==('<i8' if n=='sample_indices' else '<f8')
 return pins,parent,metric,ordinary,fixed,cp



# PRIVATE DEFINITIONS ONLY. No import, invocation or numerical evaluation by author.
# Six independent artificial controls for the currently held constraint interfaces.
# These are prospective arithmetic fixtures, not Cauchy data or an exterior choice.


FAILED_RECOVERY_PINS={'cross_u_saved_full_native_adm_constraint_sources_v001.py': '93104ea38c4469bfd272309810c7971fffefdb0512adf90d02e71b8850de919c', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001.md': '66a4f31f5df9c76ace15963634d8907fd88fdbb2fd7b17305eb8d63fce57dfee', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001_OWNER_START.json': 'cd20deb4b8dd268d403ef962c35e93e44351e5335b3fb633e1636a9d0b06e5e7', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001_MANIFEST.json': '14e3b2fa2f94f5fa5c1dca09080a8e00cfbe9c579ab70b59dd8fe3a4037f2005', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001_RESULT.json': '05a93d3bc99bde21d2eb8470bcc17ee239d90065185afa6f75d8fbbfb6129c1f', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001_RECEIPT.json': 'd8f76dd6285355455809d6ba0afc236bcf32f29ed48680a94b4c0b5104c525e5'}

FAILED_PARTIAL_SHAPES={'arrowhead_A': [1972, 3, 3], 'arrowhead_A_modes': [32, 1972, 3, 3], 'arrowhead_B': [32, 1972, 3, 3], 'arrowhead_D': [32, 1972, 3, 3], 'arrowhead_Maxwell_Schur': [1972, 3, 3], 'arrowhead_S': [1972, 4, 3], 'arrowhead_T': [32, 1972, 4, 3], 'arrowhead_factor': [32, 1972], 'arrowhead_native_cone': [32, 1972], 'arrowhead_sample_M': [8, 99, 99], 'arrowhead_sample_indices': [8], 'arrowhead_sample_modal_A': [32, 8, 3, 3], 'arrowhead_sample_modal_Schur': [32, 8, 3, 3], 'arrowhead_sample_transverse_T': [32, 8, 4, 3], 'arrowhead_sample_transverse_span': [32, 8, 4, 3], 'arrowhead_transverse_Gram': [1972, 3, 3], 'current_A': [1972, 4], 'current_D': [32, 1972, 4, 4], 'current_F': [1972, 4, 4], 'current_Fup': [1972, 4, 4], 'current_Ga': [1972, 4, 4, 4], 'current_P': [1972, 4, 4], 'current_Pi': [32, 1972, 4, 4], 'current_PiU': [1972, 4, 4], 'current_U': [1972, 4], 'current_V': [32, 1972, 4], 'current_Z': [1972, 4], 'current_a': [1972, 4], 'current_du': [1972, 4, 4], 'current_dz': [32, 1972, 4, 4], 'current_f': [32, 1972], 'current_g': [1972, 4, 4], 'current_hi': [1972, 4, 4], 'current_mu': [32, 1972], 'current_nu': [1972, 4, 4], 'current_nz': [32, 1972, 4, 4], 'current_omega': [32], 'current_phi': [1972, 4], 'current_q': [32, 1972, 4], 'current_r': [1972, 4], 'current_uc': [1972, 4], 'current_w': [32], 'current_xi': [32], 'current_z': [32, 1972, 4], 'current_z2': [32, 1972], 'loaded_b0_d0_q0_Pstar': [1972], 'loaded_b0_d0_q0_Wstar': [1972], 'loaded_b0_d0_q0_phase_u_chart': [1972], 'loaded_omega_star': [32], 'loaded_q0_Ga': [1972, 4, 4, 4], 'loaded_q0_R': [1972], 'loaded_q0_U': [1972, 4], 'loaded_q0_Z': [1972], 'loaded_q0_du': [1972, 4, 4], 'loaded_q0_dz': [32, 1972, 4, 4], 'loaded_q0_g': [1972, 4, 4], 'loaded_q0_hi': [1972, 4, 4], 'loaded_q0_phi': [1972, 4], 'loaded_q0_reference_volume': [1972], 'loaded_q0_z': [32, 1972, 4], 'loaded_weights': [32], 'loaded_xi': [32], 'saved_native_M': [8, 99, 99]}

FAILED_FIXTURE_NAMES=(
 'independent_ADM_lapse_shift_unit_transverse_jets',
 'independent_conformal_weak_curvature_isotropic_K_EH',
 'independent_canonical_ordinary_normal_shift',
 'independent_manufactured_99_arrowhead_action_solve',
 'independent_projected_chart_span_modal_Schur',
 'independent_nonzero_acceleration_Z_affine_momentum')

FAILED_FIXTURE_CONTROL_SHAPES=([200],[12],[2],[198],[672],[1,99])

def failed_admission(pins,parent,metric,ordinary,fixed,cp):
 # Pure stdlib admission: COMPLETE closed failed map and every pair/header.
 pins=dict(pins)
 def add(n,h):
  n=str(path(n).resolve());assert type(h) is str and len(h)==64
  assert n not in pins or pins[n]==h,('Conflicting failed-parent seal',n)
  pins[n]=h
 for n,h in FAILED_RECOVERY_PINS.items():add(n,h)
 rc=json.loads(path(FAILED+'_RECEIPT.json').read_text())
 result=json.loads(path(FAILED+'_RESULT.json').read_text())
 owner=json.loads(path(FAILED+'_OWNER_START.json').read_text())
 manifest=json.loads(path(FAILED+'_MANIFEST.json').read_text())
 assert rc['status']=='CLOSED' and rc['closed']=='2026-10-07T01:18:39.129484+00:00'
 assert owner==rc['owner']==result['owner']==manifest['owner']
 assert owner['owner']=='root' and owner['pid']==21859
 assert owner['source_file']=='cross_u_saved_full_native_adm_constraint_sources_v001.py'
 assert owner['source_sha256']==FAILED_RECOVERY_PINS[owner['source_file']]
 assert owner['started']=='2026-10-07T01:18:15.949276+00:00'
 assert rc['result_sha256']==FAILED_RESULT_SHA==FAILED_RECOVERY_PINS[FAILED+'_RESULT.json']
 assert FAILED_RECEIPT_SHA==FAILED_RECOVERY_PINS[FAILED+'_RECEIPT.json']
 assert manifest['input_sha256']==rc['input_sha256']
 assert manifest['canonical_parent_file']==PARENT+'_RESULT.json'
 assert manifest['canonical_parent_sha256']==PARENT_RESULT_SHA
 assert manifest['configuration']==dict(controls=42,pairs=6,sigma=list(SIGMAS),
  tolerance=TOL,points_per_quadrature=[1972,1972,1938,1938],quadrature_columns=4,
  canonical_velocities=99,compact_ADM_directions=8)
 for field in ('input_sha256','output_sha256'):
  for n,h in rc[field].items():add(n,h)
 assert result['status']=='CANONICAL_CONSTRAINT_SOURCE_REFUSALS_RETAINED'
 assert result['predeclared_control_count']==42 and len(result['controls'])==14
 assert result['parent_file']==PARENT+'_RESULT.json' and result['parent_sha256']==PARENT_RESULT_SHA
 assert result['copied_original_failed_controls']==parent['copied_failed_controls']
 assert [c['ordinal'] for c in result['controls']]==list(range(14))
 assert [c['passed'] for c in result['controls']]==[True]*7+[False,True,False,True,False,True,False]
 assert not path(FAILED+'_ERROR.json').exists()
 for obj in (rc,result,manifest):assert all(v is False for v in obj['qualification'].values())
 records=result['checkpoints'];assert len(records)==6
 assert records[0]['file']==FAILED+'_00000_INPUT.npz'
 assert records[1]['file']==FAILED+'_00001_ARITHMETIC_FIXTURES.npz'
 assert len(result['cases'])==4 and [c['sigma'] for c in result['cases']]==list(SIGMAS)
 inp,fixture=records[:2];im=inp['metadata'];fm=fixture['metadata']
 assert im['kind']=='exact_owned32_quad_and_closed_canonical_refs'
 assert im['fixed']==fixed and im['owned_EPS5_background']==cp['background']
 assert im['parent_file']==PARENT+'_RESULT.json' and im['parent_sha256']==PARENT_RESULT_SHA
 assert im['copied_canonical_controls']==parent['controls']
 assert im['copied_metric_controls']==metric['controls'] and im['copied_ordinary_controls']==ordinary['controls']
 assert im['copied_original_failed_controls']==parent['copied_failed_controls']
 assert im['schema']=={n:dict(shape=[32],dtype='float64',finite=True) for n in ('xi','weights')}
 assert fm['kind']=='fixed_artificial_action_owned_ADM_and_arrowhead_controls'
 assert fm['controls']==result['controls'][:6] and len(fm['schema'])==149
 for k,(name,shape) in enumerate(zip(FAILED_FIXTURE_NAMES,FAILED_FIXTURE_CONTROL_SHAPES)):
  assert fm['controls'][k]['ordinal']==k and fm['controls'][k]['name']==name
  assert fm['controls'][k]['passed'] is True and fm['controls'][k]['tolerance']==TOL
  for pref,suffixes in (('control_',('actual','expected','envelope')),('raw_',('actual','expected','envelope','scale'))):
   for suffix in suffixes:assert fm['schema'][f'{pref}{k:03d}_{name}_{suffix}']==dict(shape=shape,dtype='float64',finite=True)
 for i,(case,pc) in enumerate(zip(result['cases'],parent['cases'])):
  rec=case['checkpoint'];md=rec['metadata'];oldM=6+2*i;oldFail=oldM+1;label=f's{case["sigma"]}'
  assert case['status']=='CANONICAL_SOURCE_REFUSED' and rec==records[i+2]
  assert rec['file']==f'{FAILED}_{i+2:05d}_REFUSED_ARM.npz'
  assert md['kind']=='unaccepted_available_complete_canonical_constraint_operands'
  assert md['sigma']==pc['sigma']==case['sigma']
  assert md['canonical_parent_file']==pc['checkpoint']['file'] and md['canonical_parent_sha256']==pc['checkpoint']['sha256']
  assert md['controls']==result['controls'][oldM:oldFail+1]
  assert md['controls'][0]['name']==label+'_exact_arrowhead_vs_saved_original_99' and md['controls'][0]['passed'] is True
  assert md['controls'][1]['name']==label+'_exact_transverse_span_and_Maxwell_Schur' and md['controls'][1]['passed'] is False
  assert md['controls'][1]['error']==result['controls'][oldFail]['error'] and all(c['tolerance']==TOL for c in md['controls'])
  assert md['context']['current_control_ordinal']==oldFail and md['context']['current_control']==md['controls'][1]['name']
  assert md['context']['stage']=='canonical_constraints' and 'exact_transverse_span_and_Maxwell_Schur' in md['traceback']
  expected={n:dict(shape=shape,dtype=('int64' if n=='arrowhead_sample_indices' else 'float64'),finite=True) for n,shape in FAILED_PARTIAL_SHAPES.items()}
  for row,shape in zip(md['controls'],([8,99,99],[5376])):
   for pref,suffixes in (('control_',('actual','expected','envelope')),('raw_',('actual','expected','envelope','scale'))):
    for suffix in suffixes:expected[f'{pref}{row["ordinal"]:03d}_{row["name"]}_{suffix}']=dict(shape=shape,dtype='float64',finite=True)
  assert md['schema']==expected and len(expected)==77
  # These unsaved seven-Y certificate inputs are owned by the authentic parent,
  # not fabricated loaded_* fields in the refused V001 payload.
  for n,shape in dict(sample_indices=[8],native_M=[8,99,99],kinetic_envelope=[8,105,105],
   all_velocity_response=[8,99,7],original_M_action=[8,99,7]).items():
   assert pc['checkpoint']['metadata']['schema'][n]==dict(shape=shape,dtype=('int64' if n=='sample_indices' else 'float64'),finite=True)
  assert all(v is False for v in case['qualification'].values())
 for rec in records:
  assert rec['commit_file']==rec['file']+'.COMMIT.json'
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
  assert pins[str(path(rec['file']).resolve())]==rec['sha256'] and pins[str(path(rec['commit_file']).resolve())]==rec['commit_sha256']
  md=rec['metadata'];assert md['owner']==owner and md['physical_changes']==[]
  assert all(v is False for v in md['qualification'].values())
  with zipfile.ZipFile(path(rec['file'])) as zz:
   assert set(zz.namelist())=={n+'.npy' for n in md['schema']}|{'metadata_json.npy'}
   def header(ff):
    assert ff.read(6)==b'\x93NUMPY';v=ff.read(2);assert v in (b'\x01\x00',b'\x02\x00',b'\x03\x00')
    ln=struct.unpack('<H' if v==b'\x01\x00' else '<I',ff.read(2 if v==b'\x01\x00' else 4))[0]
    return ast.literal_eval(ff.read(ln).decode('utf8' if v==b'\x03\x00' else 'latin1'))
   with zz.open('metadata_json.npy') as ff:
    hd=header(ff);assert hd['shape']==() and hd['descr'].startswith('<U')
    assert json.loads(ff.read().decode('utf-32-le').rstrip('\x00'))==md
   for n,desc in md['schema'].items():
    with zz.open(n+'.npy') as ff:hd=header(ff)
    assert list(hd['shape'])==desc['shape'] and hd['descr']==('<i8' if desc['dtype']=='int64' else '<f8')
    assert hd['fortran_order'] is False and desc['finite'] is True
 assert {p.name for p in BASE.glob(FAILED+'_*.npz')}=={rec['file'] for rec in records}
 assert {p.name for p in BASE.glob(FAILED+'_*.npz.COMMIT.json')}=={rec['commit_file'] for rec in records}
 for n,h in pins.items():assert sha(path(n))==h,('Failed-parent/full input seal changed',n)
 return pins,dict(result=result,receipt=rc,input=inp,fixture=fixture,cases=result['cases'])

def read_failed_raw(record):
 # ROOT runtime only: load and preserve original signed arrays, no action replay.
 assert sha(path(record['file']))==record['sha256'] and sha(path(record['commit_file']))==record['commit_sha256']
 assert json.loads(path(record['commit_file']).read_text())=={k:v for k,v in record.items() if k not in ('commit_file','commit_sha256')}
 md=record['metadata'];out={};captured=[]
 with np.load(path(record['file']),allow_pickle=False) as ff:
  assert set(ff.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(ff['metadata_json']))==md
  for n,desc in md['schema'].items():
   a=ff[n].copy();key='failed_loading_'+n;RAW[key]=a;captured.append(key)
   assert a.shape==tuple(desc['shape']) and str(a.dtype)==desc['dtype'] and bool(np.all(np.isfinite(a)))==desc['finite']
   out[n]=a
 # Drop successful loading scratch only after the whole pair is authenticated;
 # on any refusal the progressively captured arrays remain in the owned RAW.
 for n in captured:RAW.pop(n)
 return out

def recover_fixture(failed):
 assert len(CHECKS)==0
 rows=failed['fixture']['metadata']['controls'];assert rows==failed['result']['controls'][:6]
 saved=read_failed_raw(failed['fixture'])
 RAW.update(saved)  # all149 arrays, exact original keys and dtype/values
 CHECKS.extend(json.loads(json.dumps(rows,allow_nan=False)))
 assert len(CHECKS)==6 and CHECKS==rows and all(c['passed'] is True for c in CHECKS)
 CONTEXT.update(recovery_stage='six_completed_fixtures_copied_without_replay',failed_fixture_file=failed['fixture']['file'],failed_fixture_sha256=failed['fixture']['sha256'])
 return saved

def carry_completed_M(oldrow,oldraw):
 # Only the active ordinal/key prefix is rebased. Original dictionaries remain
 # verbatim in copied_constraint_V001_controls and the sealed failed checkpoint.
 assert oldrow['passed'] is True and oldrow['tolerance']==TOL
 old=oldrow['ordinal'];assert old in (6,8,10,12)
 ordinal=len(CHECKS);assert ordinal>=6  # actual next ordinal also after a prior arm refusal
 row=json.loads(json.dumps(oldrow,allow_nan=False));row['ordinal']=ordinal
 for pref,suffixes in (('control_',('actual','expected','envelope')),('raw_',('actual','expected','envelope','scale'))):
  oldkey=f'{pref}{old:03d}_{oldrow["name"]}_';newkey=f'{pref}{ordinal:03d}_{oldrow["name"]}_'
  for suffix in suffixes:
   a=oldraw[oldkey+suffix];assert a.shape==(8,99,99) and a.dtype==np.dtype('float64')
   RAW[newkey+suffix]=a.copy()
 CHECKS.append(row)
 CONTEXT.update(current_control=row['name'],current_control_ordinal=ordinal,copied_original_control_ordinal=old)
 return row


def constraint_fixture_chart(xi,w):
 N=7/5;beta=np.array([1/7,-1/11,1/13]);hd=np.array([4.,9.,16.]);ihd=1/hd
 g=np.zeros((1,4,4));hi=np.zeros_like(g)
 g[0,1:,1:]=np.diag(hd);g[0,0,1:]=hd*beta;g[0,1:,0]=g[0,0,1:];g[0,0,0]=-N*N+np.sum(hd*beta*beta)
 hi[0,0,0]=-1/N**2;hi[0,0,1:]=beta/N**2;hi[0,1:,0]=hi[0,0,1:];hi[0,1:,1:]=np.diag(ihd)-np.outer(beta,beta)/N**2
 u=np.array([3/2,0.,0.]);up=ihd*u;gamma=5/4;U=np.r_[gamma/N,up-beta*gamma/N][None]
 zs=(B*GC)*xi[:,None]**2*np.array([2/7,-1/9,1/11])[None,:]
 z=np.zeros((32,1,4));z[:,0,1:]=zs;z[:,0,0]=zs@beta-N*(zs@up)/gamma
 s=dict(g=g,hi=hi,U=U,z=z,Ga=np.zeros((1,4,4,4)),du=np.zeros((1,4,4)),dz=np.zeros((32,1,4,4)),phi=np.zeros((1,4)),w=w,omega=xi/3,xi=xi)
 RAW.update({f'fixture_chart_{k}':v.copy() for k,v in s.items() if isinstance(v,np.ndarray)})
 return s,adm_chart(s)


def constraint_analytic_fixtures(xi,w):
 # 1. Nonzero lapse/shift and independent partial jets at a tilted covector chart.
 s,c=constraint_fixture_chart(xi,w)
 f=np.array([3/19]);df=np.array([[1/29,-2/31,3/37,-4/41.]])
 b=np.array([[2/17,-3/19,1/23.]])
 db=np.array([[[1/43,-2/47,3/53],[-4/59,5/61,-6/67],[7/71,-8/73,9/79],[-10/83,11/89,-12/97.]]])
 lift=lapse_shift_lift(s,c,f,df,b,db);q,dq,eta,deta,zeta,dzeta=(lift[k] for k in ('q','dq','eta','deta','zeta','dzeta'))
 g,U,z,du,dz=s['g'],s['U'],s['z'],s['du'],s['dz'];dg=lift['ADM_jets']['dg']
 unit=np.einsum('pab,pa,pb->p',q,U,U)+2*np.einsum('pab,pa,pb->p',g,U,eta)
 ue=np.einsum('pab,pa,pb->p',abs(q),abs(U),abs(U))+2*np.einsum('pab,pa,pb->p',abs(g),abs(U),abs(eta))
 uj=np.einsum('pcab,pa,pb->pc',dq,U,U)+2*np.einsum('pab,pca,pb->pc',q,du,U)+2*np.einsum('pcab,pa,pb->pc',dg,U,eta)+2*np.einsum('pab,pca,pb->pc',g,du,eta)+2*np.einsum('pab,pa,pcb->pc',g,U,deta)
 uje=np.einsum('pcab,pa,pb->pc',abs(dq),abs(U),abs(U))+2*np.einsum('pab,pca,pb->pc',abs(q),abs(du),abs(U))+2*np.einsum('pcab,pa,pb->pc',abs(dg),abs(U),abs(eta))+2*np.einsum('pab,pca,pb->pc',abs(g),abs(du),abs(eta))+2*np.einsum('pab,pa,pcb->pc',abs(g),abs(U),abs(deta))
 trans=np.einsum('pa,jpa->jp',eta,z)+np.einsum('pa,jpa->jp',U,zeta)
 te=np.einsum('pa,jpa->jp',abs(eta),abs(z))+np.einsum('pa,jpa->jp',abs(U),abs(zeta))
 tj=np.einsum('pca,jpa->jpc',deta,z)+np.einsum('pa,jpca->jpc',eta,dz)+np.einsum('pca,jpa->jpc',du,zeta)+np.einsum('pa,jpca->jpc',U,dzeta)
 tje=np.einsum('pca,jpa->jpc',abs(deta),abs(z))+np.einsum('pa,jpca->jpc',abs(eta),abs(dz))+np.einsum('pca,jpa->jpc',abs(du),abs(zeta))+np.einsum('pa,jpca->jpc',abs(U),abs(dzeta))
 covU=np.einsum('pia,pa->pi',q[:,1:,:],U)+np.einsum('pia,pa->pi',g[:,1:,:],eta)
 cue=np.einsum('pia,pa->pi',abs(q[:,1:,:]),abs(U))+np.einsum('pia,pa->pi',abs(g[:,1:,:]),abs(eta))
 direct_z0=np.einsum('jpi,pi->jp',z[:,:,1:],b)-f[None,:]*np.einsum('jpi,pi->jp',z[:,:,1:],c['up'])/c['gamma'][None,:]
 ze=np.einsum('jpi,pi->jp',abs(z[:,:,1:]),abs(b))+abs(f[None,:])*np.einsum('jpi,pi->jp',abs(z[:,:,1:]),abs(c['up']))/c['gamma'][None,:]
 actual=np.r_[unit.ravel(),uj.ravel(),trans.ravel(),tj.ravel(),covU.ravel(),zeta[:,:,0].ravel()]
 expected=np.r_[np.zeros(unit.size+uj.size+trans.size+tj.size+covU.size),direct_z0.ravel()]
 envelope=np.r_[ue.ravel(),uje.ravel(),te.ravel(),tje.ravel(),cue.ravel(),ze.ravel()]
 RAW.update(fixture_ADM_unit=unit,fixture_ADM_unit_jet=uj,fixture_ADM_transverse=trans,fixture_ADM_transverse_jet=tj,fixture_ADM_fixed_covU=covU,fixture_ADM_direct_z0=direct_z0)
 scaled_check('independent_ADM_lapse_shift_unit_transverse_jets',actual,expected,envelope)

 # 2. Full first-derivative conformal curvature and isotropic Kplus EH ledger.
 # h=psi^4 diag(1,1,R^2), d ln psi=(a,b,0). This analytic Gamma includes
 # Gamma^0_ij=Hh_ij/N and Gamma^i_0j=NH delta^i_j, not a synthetic K override.
 R=np.array([7/3]);psi=5/4;a=1/7;bb=-2/11;N=7/5;H=2/13
 hd=psi**4*np.array([1.,1.,float(R[0])**2]);h=np.diag(hd)
 g=np.zeros((1,4,4));hi=np.zeros_like(g);g[0,0,0]=-N*N;g[0,1:,1:]=h;hi[0,0,0]=-1/N**2;hi[0,1:,1:]=np.diag(1/hd)
 U=np.array([[1/N,0.,0.,0.]]);Ga=np.zeros((1,4,4,4));bar=np.zeros((3,3,3));bar[0,2,2]=-R[0];bar[2,0,2]=bar[2,2,0]=1/R[0]
 ag=np.array([a,bb,0.]);barh=np.diag([1.,1.,float(R[0])**2]);barhi=np.diag([1.,1.,1/float(R[0])**2]);eye=np.eye(3)
 for k in range(3):
  for i in range(3):
   for j in range(3):Ga[0,k+1,i+1,j+1]=bar[k,i,j]+2*(eye[k,i]*ag[j]+eye[k,j]*ag[i]-barh[i,j]*barhi[k,k]*ag[k])
 Ga[0,0,1:,1:]=H*h/N;Ga[0,1:,0,1:]=N*H*eye;Ga[0,1:,1:,0]=N*H*eye
 z=np.zeros((32,1,4));s=dict(g=g,hi=hi,U=U,z=z,Ga=Ga,du=np.zeros((1,4,4)),dz=np.zeros((32,1,4,4)),phi=np.zeros((1,4)))
 RAW.update(fixture_EH_g=g.copy(),fixture_EH_hi=hi.copy(),fixture_EH_Gamma=Ga.copy())
 c=adm_chart(s);f=np.array([3/19]);df=np.array([[1/29,-2/31,3/37,0.]])
 b=np.array([[2/17,-3/19,1/23.]])
 db=np.array([[[0.,0.,0.],[1/29,2/31,-3/37],[-4/41,5/43,6/47],[7/53,-8/59,9/61.]]])
 curv=spatial_curvature_weak_density(s,c,f,df,R);eh=EH_ADM_constraint_direction(s,c,f,df,b,db,R)
 expected_curv=8*psi**2*(df[:,1]*a+df[:,2]*bb+f*(a*a+bb*bb))
 expected_normal=-3*psi**6*H*H*f/C-expected_curv/(2*C)
 expected_traceLie=12*(a*b[:,0]+bb*b[:,1])+2*b[:,0]/R+2*(db[:,1,0]+db[:,2,1]+db[:,3,2])
 expected_shift=-psi**6*H*expected_traceLie/C
 expected_K=np.broadcast_to(H*h,(1,3,3))
 actual=np.r_[curv['value'],eh['normal'],eh['shift'],c['K'].ravel()]
 expected=np.r_[expected_curv,expected_normal,expected_shift,expected_K.ravel()]
 envelope=np.r_[curv['envelope'],eh['normal_envelope'],eh['shift_envelope'],abs(expected_K).ravel()]
 RAW.update(fixture_EH_curvature_expected=expected_curv,fixture_EH_normal_expected=expected_normal,fixture_EH_shift_expected=expected_shift,fixture_EH_K_expected=expected_K)
 scaled_check('independent_conformal_weak_curvature_isotropic_K_EH',actual,expected,envelope)

 # 3. Canonical particle source has +m gamma deltaN and -m p_i deltaBeta.
 ss,cc=constraint_fixture_chart(xi,w);p=np.array([[3/2,0.,0.]]);mass=np.array([11/13]);f=np.array([3/19]);b=np.array([[2/17,-3/19,1/23.]])
 ordinary=ordinary_canonical_constraint_rows(ss['g'],p,mass,f,b)
 expected=np.array([(11/13)*(5/4)*(3/19),-(11/13)*(3/2)*(2/17)])
 actual=np.r_[ordinary['normal'],ordinary['shift']]
 RAW.update(fixture_ordinary_g=ss['g'].copy(),fixture_ordinary_p=p.copy(),fixture_ordinary_mass=mass.copy(),fixture_ordinary_f=f.copy(),fixture_ordinary_b=b.copy())
 scaled_check('independent_canonical_ordinary_normal_shift',actual,expected,abs(expected))

 # 4. Manufactured full99 arrowhead: D positive, B=L^T D, A=M+sum L^T D L.
 # Independent explicit M99 multiplication supplies rhs; solve is never its oracle.
 diag=np.array([2.,3.,5.]);D=w[:,None,None,None]*(1+xi)[:,None,None,None]*np.diag(diag)[None,None]
 L=np.empty((32,1,3,3))
 for j in range(32):L[j,0]=np.array([[1/7,2/11,-3/13],[4/17,-5/19,6/23],[7/29,8/31,-9/37]])/(j+1)
 BT=np.einsum('jpik,jpkl->jpil',D,L);Bmat=BT.swapaxes(2,3)
 Am=np.einsum('jpki,jpkl->jpil',L,BT);M=np.diag([7/11,13/17,19/23])[None];A=M+Am.sum(axis=0)
 block=dict(D=D,B=Bmat,A_modes=Am,A=A,Maxwell=M)
 full=np.zeros((1,99,99));full[:,:3,:3]=A
 for j in range(32):
  sl=slice(3+3*j,6+3*j);full[:,sl,sl]=D[j];full[:,:3,sl]=Bmat[j];full[:,sl,:3]=BT[j]
 y=(np.arange(99,dtype=float)+1)[None]/113;rhs=np.einsum('pab,pb->pa',full,y)
 actual_action=arrowhead_action(block,y);sol=arrowhead_solve(block,rhs[:,:,None])[:,:,0]
 action_env=np.einsum('pab,pb->pa',abs(full),abs(y))
 RAW.update(fixture_arrowhead_full99=full,fixture_arrowhead_y=y,fixture_arrowhead_rhs=rhs,fixture_arrowhead_actual_action=actual_action,fixture_arrowhead_actual_solution=sol)
 scaled_check('independent_manufactured_99_arrowhead_action_solve',np.r_[actual_action.ravel(),sol.ravel()],np.r_[rhs.ravel(),y.ravel()],np.r_[action_env.ravel(),abs(y).ravel()])

 # 5. The actual chart's projected temporal compensation lies in spatial span S.
 # Certify per-mode A=B D^-1 B^T without subtracting the large Grams to define M.
 ss,cc=constraint_fixture_chart(xi,w);uc=np.einsum('pab,pb->pa',ss['g'],ss['U']);ss['P']=np.eye(4)[None]+np.einsum('pa,pb->pab',uc,ss['U'])
 ab=arrowhead_blocks(ss,cc);Lspan=ss['P'][:,1:,0][None,:,:,None]*cc['JzU'][:,:,None,:]
 span=np.einsum('pai,jpib->jpab',ab['S'],Lspan)
 elim=np.linalg.solve(ab['D'],ab['B'].swapaxes(2,3));cancel=np.einsum('jpik,jpkl->jpil',ab['B'],elim)
 span_env=np.einsum('pai,jpib->jpab',abs(ab['S']),abs(Lspan))+abs(ab['T'])
 cancel_env=np.einsum('jpik,jpkl->jpil',abs(ab['B']),abs(elim))+abs(ab['A_modes'])
 RAW.update(fixture_span_actual=ab['T'].copy(),fixture_span_expected=span,fixture_Schur_Gram_expected=cancel)
 scaled_check('independent_projected_chart_span_modal_Schur',np.r_[ab['T'].ravel(),ab['A_modes'].ravel()],np.r_[span.ravel(),cancel.ravel()],np.r_[span_env.ravel(),cancel_env.ravel()])

 # 6. An aligned constant nonzero Z supplies affine momentum even with all jets0.
 # PiU^0_i=U^0 Z_i, hence p_ui=sqrt(h) h^ij Z_j; mode momenta remain exactly0.
 N=7/5;h=np.diag([4.,9.,16.]);g=np.zeros((1,4,4));hi=np.zeros_like(g);g[0,0,0]=-N*N;g[0,1:,1:]=h;hi[0,0,0]=-1/N**2;hi[0,1:,1:]=np.diag([1/4,1/9,1/16])
 U=np.array([[1/N,0.,0.,0.]]);z=np.zeros((32,1,4));z[:,0,1:]=(B*GC)*xi[:,None]**2*np.array([2/7,-1/9,1/11])[None]
 s=features(g,hi,np.zeros((1,4,4,4)),U,np.zeros((1,4,4)),z,np.zeros((32,1,4,4)),np.zeros((1,4)),xi/3,xi,w);c=adm_chart(s);py,_=reduced_momenta(s,c)
 Z=np.einsum('j,jpi->pi',w,z[:,:,1:]);expected=np.zeros((1,99));expected[:,:3]=24*Z*np.array([1/4,1/9,1/16])[None]
 assert np.any(expected!=0)
 RAW.update(fixture_affine_z=z.copy(),fixture_affine_Z=Z,fixture_affine_native_canonical_actual=py,fixture_affine_native_canonical_expected=expected)
 scaled_check('independent_nonzero_acceleration_Z_affine_momentum',py,expected,abs(expected))


def fixtures(xi,w):
 constraint_analytic_fixtures(xi,w)
 assert len(CHECKS)==6

def selected_arrays_any(file,names):
 out={}
 with np.load(path(file),allow_pickle=False) as ff:
  for name in names:
   a=ff[name].copy();RAW['loaded_'+name]=a
   assert a.dtype.kind in 'fiu' and np.all(np.isfinite(a)),name
   out[name]=a
 return out


def run_arm(case,metric_case,ordinary_case,fixed,cp,failed_case):
 global RAW,ARM_AVAILABLE
 start=len(CHECKS)
 try:
  with np.errstate(over='raise',invalid='raise',divide='raise'):return constraint_arm(case,metric_case,ordinary_case,fixed,cp,failed_case)
 except Exception:
  failure=traceback.format_exc();available=dict(ARM_AVAILABLE);available.update(RAW)
  rec=checkpoint('REFUSED_ARM',available,dict(kind='unaccepted_available_complete_canonical_constraint_operands',sigma=case['sigma'],controls=CHECKS[start:],context=dict(CONTEXT),traceback=failure,canonical_parent_file=case['checkpoint']['file'],canonical_parent_sha256=case['checkpoint']['sha256'],physical_changes=[]))
  RAW={};ARM_AVAILABLE={}
  return dict(sigma=case['sigma'],status='CANONICAL_SOURCE_REFUSED',checkpoint=rec,qualification=FLAGS)


def main():
 global np,OWNER,INPUTS,RAW,ARM_AVAILABLE
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded complete-action canonical constraint-source prerequisite; FULL independent admission and root-only execution required.')
 assert not list(BASE.glob(STEM+'_*')),'Own runtime namespace occupied.'
 INPUTS,parent,metric,ordinary,fixed,cp=admission();INPUTS,failed=failed_admission(INPUTS,parent,metric,ordinary,fixed,cp);cases=[];exit_code=0
 OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__),scope='saved four-arm full canonical compact normal/momentum source prerequisite')
 try:
  json_file(STEM+'_OWNER_START.json',OWNER)
  json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(controls=CONTROL_COUNT,pairs=PAIR_COUNT,sigma=SIGMAS,tolerance=TOL,points_per_quadrature=(1972,1972,1938,1938),quadrature_columns=4,canonical_velocities=99,compact_ADM_directions=8),canonical_parent_file=PARENT+'_RESULT.json',canonical_parent_sha256=PARENT_RESULT_SHA,qualification=FLAGS))
  import numpy as _np
  np=_np
  vals=read_failed_raw(failed['input']);assert vals['xi'].shape==vals['weights'].shape==(32,) and np.all(vals['xi']>0) and np.all(vals['weights']>0)
  checkpoint('INPUT',vals,dict(kind='exact_owned32_quad_and_closed_canonical_refs',failed_input_file=failed['input']['file'],failed_input_sha256=failed['input']['sha256'],copied_constraint_V001_controls=failed['result']['controls'],constraint_V001_result_sha256=FAILED_RESULT_SHA,fixed=fixed,owned_EPS5_background=cp['background'],parent_file=PARENT+'_RESULT.json',parent_sha256=PARENT_RESULT_SHA,copied_canonical_controls=parent['controls'],copied_metric_controls=metric['controls'],copied_ordinary_controls=ordinary['controls'],copied_original_failed_controls=parent['copied_failed_controls'],original_failure_disposition='inherited ADM/Legendre V001 ordinal6 False and constraint V001 span failures7/9/11/13 retained distinctly; recovery changes only operation envelopes and custody',physical_changes=[]))
  RAW={};ARM_AVAILABLE={};recover_fixture(failed);available=dict(ARM_AVAILABLE);available.update(RAW)
  checkpoint('ARITHMETIC_FIXTURES',available,dict(kind='fixed_artificial_action_owned_ADM_and_arrowhead_controls',controls=list(CHECKS),failed_fixture_file=failed['fixture']['file'],failed_fixture_sha256=failed['fixture']['sha256'],copied_without_fixture_replay=True,physical_changes=[]))
  for a,m,o,fc in zip(parent['cases'],metric['cases'],ordinary['cases'],failed['result']['cases']):cases.append(run_arm(a,m,o,fixed,cp,fc))
  accepted=all(c['status']=='CONDITIONAL_COMPACT_CANONICAL_CONSTRAINT_SOURCE' for c in cases)
  assert len(cases)==4 and len(RECORDS)==PAIR_COUNT
  if accepted:assert len(CHECKS)==CONTROL_COUNT and all(c['passed'] for c in CHECKS)
  else:exit_code=3
  status='CONDITIONAL_CANONICAL_CONSTRAINT_SOURCE_ARITHMETIC_PASS' if accepted else 'CANONICAL_CONSTRAINT_SOURCE_REFUSALS_RETAINED'
  result=dict(owner=OWNER,status=status,cases=cases,controls=CHECKS,predeclared_control_count=CONTROL_COUNT,checkpoints=RECORDS,parent_file=PARENT+'_RESULT.json',parent_sha256=PARENT_RESULT_SHA,copied_original_failed_controls=parent['copied_failed_controls'],copied_constraint_V001_controls=failed['result']['controls'],constraint_V001_result_sha256=FAILED_RESULT_SHA,recovery_changes=['operation-envelope arithmetic only; completed six fixtures/four original-M controls and all saved partials reused'],qualification=FLAGS)
  recheck();rh=json_file(STEM+'_RESULT.json',result)
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\n{status}; {len(CHECKS)} of {CONTROL_COUNT} arithmetic controls, four arms, six pairs.\n\nAll four authentic quadrature columns, all32 native modes and full99 canonical variables are retained. The owned isotropic metric-rate increment preserves native p and changes metric p explicitly. Signed complete weak normal/shift rows and independent canonical generators are saved; no residual-smallness gate, inverse, metric/source correction or physical Cauchy/history/junction is adopted. Activity outside the measured support remains unknown.\n').encode())
  recheck();rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS)
  json_file(STEM+'_RECEIPT.json',rc);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(rc);recheck();print(status,len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_failure=None;closing_failure=None;available=dict(ARM_AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_complete_canonical_constraint_operands',context=dict(CONTEXT)))
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
