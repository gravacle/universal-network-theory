"""Guarded whole upper-half Q2 Cauchy inventory of one declared stationary trial."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,hashlib,json,math,os,traceback
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V001'
METRIC='CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001'
ADM='CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002'
BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001'
PHASE='CROSS_U_SAVED_COUPLED_PHASE_INITIAL_RATE_V001'
PROTOCOL_SHA=None
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10
B=A0*KPC/LIGHT**2;C=1.98;KB=.02;ALPHA=KB/C;GC=3*math.pi/8;ELL=.1
SIGMAS=(.1,1.,10.,100.);TOL=2e-11;CONTROL_COUNT=92;PAIR_COUNT=22
POINTS_PER_COLUMN=3784;POINTS_PER_ARM=15136
np=None;OWNER=None;QBAR=None;INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={}
FLAGS={k:False for k in ('full_Cauchy_slice_qualified','nodal_Q1_velocity_qualified','global_constraint_solution_qualified','physical_initial_state_qualified','formation_history_qualified','physical_junction_qualified','local_cosmic_ordinary_state_qualified','active_source_mapping_qualified','orbital_force_qualified','observational_qualified','joint_model_adopted')}
COMPACT='CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001'
PINS={'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CROSS_U_CONSTRAINED_CANONICAL_CHART_AND_CMC_ADMISSION_V001.md': '872ca230d040bfca08ac127c117e741e81549a4316e62dd5de8df8e8732f7e98', 'CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md': '087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523', 'cross_u_saved_full_metric_native_source_residual_v001.py': '23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68', 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001.md': '88fbf64e1568af3f47f1346b809c6d8a35fe7b685a73817938616b9056068e24', 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_RESULT.json': 'ef7f81025c000fd9281bbb9a5afdbb3503a204b56ed0f8b6a291fc2152225798', 'CROSS_U_SAVED_FULL_METRIC_NATIVE_SOURCE_RESIDUAL_V001_RECEIPT.json': 'eb450284a7c28b65df0eb5d9ecb08d0f6156c98d7ca6ae52ce2af37b6353dfde', 'cross_u_saved_full_native_adm_legendre_v002.py': '9185f2dcd981d7599023858dd8c533b13a510c150ad994b5ea3f569b947d9de0', 'CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002.md': 'e8529df3d5c3997f3120a0d483e035493517514ddeaaa3e55834e811006d81e3', 'CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002_RESULT.json': '4d4c9e89520390db932b66548aed361607abcc70b48d422502a3f53af9d06fb6', 'CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002_RECEIPT.json': '4a21c59742252d7fcaaccfd7b9371fa846bc1d248579ae9408a9838ae971b99e', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RESULT.json': 'fc54d032172c901d288d7f845c077b7f4114199183190e3c0b7eb2c8a1420e85', 'CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001_RECEIPT.json': '41a22374c9747d5b64bf4894290433af8a2cdb92f345f64f6de89f8cc175ea0f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json': '3f4cbdf1c8255ae06668dc63fa6cdfc7ca4c5b70c78a2b5cbe64a303fb17973c', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', 'CROSS_U_SAVED_COUPLED_PHASE_INITIAL_RATE_V001_RESULT.json': 'd23bc2ce8ec4c748f7f3ea9aa287623ae5bfde95809e262c9273e6331f062d42', 'CROSS_U_SAVED_COUPLED_PHASE_INITIAL_RATE_V001_RECEIPT.json': '3d3cb067b47f33ef45c107f17eb9d3d909d165a3ec3ad4aefb3ee5bc38bcd16f', 'authoring_cross_u_whole_slice_cauchy_data_v001_499_367dd464.py': '367dd4641f5d8be808d92bfc1c0ae1b3ef5543466c924a9302ec5f8e32bdd82a', 'cross_u_saved_full_native_adm_constraint_sources_v001.py': '93104ea38c4469bfd272309810c7971fffefdb0512adf90d02e71b8850de919c', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001.md': '66a4f31f5df9c76ace15963634d8907fd88fdbb2fd7b17305eb8d63fce57dfee', 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001_RESULT.json': None, 'CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001_RECEIPT.json': None}
HELPER_SPANS=[{'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'shape_quadrature', 'first': 96, 'last': 109, 'sha256': '0cd9bc8e1c40eb7cb5e4befe5af97a9b76c936c97ac70703029743d999bc9a40'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'interpolate', 'first': 111, 'last': 117, 'sha256': '39701bc4c9f5c75bfbada6289b2b323cc8628c8c37a6c3ebd6e2eedf6848cf25'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'lower', 'first': 125, 'last': 125, 'sha256': '065bc9c41f65ef90b29f76e49d31bbe082ab7995a2f31dcfee81e74d72847a28'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'lower_last', 'first': 127, 'last': 127, 'sha256': 'a5499ee24271aa5e88cc7a6bbc63e5c554179f3f1b572dd891ed65ccce86554a'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'raise_cov', 'first': 129, 'last': 129, 'sha256': 'f361d67c7314df41c3c6ac01d96d9362912269eb45ffb4a6568bbb1398b4263b'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'covdot', 'first': 130, 'last': 130, 'sha256': '7746ebccfd341cc85e0168705cc0c0627b26e9157cfd2c3a7813a960e59f8551'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'metric', 'first': 132, 'last': 149, 'sha256': 'b882f426f1130f04f7128c1816c996626e9b2f811d094f2231afefbf141bb6e4'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'features', 'first': 151, 'last': 175, 'sha256': '4f458b4c8277a90abc2cffcea3d268b1be54a828a2cfc66b281bd50b5e4554e0'}, {'file': 'cross_u_saved_full_metric_native_source_residual_v001.py', 'name': 'trial_point', 'first': 208, 'last': 228, 'sha256': '9773147db78761b620210c05e8f55ac62ee6c463f04d7f72633cfad066945407'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'metric_partial', 'first': 236, 'last': 239, 'sha256': '35322f99ef24ed0ca3167bda05714d8499b4c99cd91f32f2c30f46570ca05d07'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'metric_basis', 'first': 294, 'last': 297, 'sha256': '82d2cfa2ad99dd38b4a4288768515717bfc43bcd761411b1b144c51ede631b6f'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'adm_chart', 'first': 304, 'last': 330, 'sha256': 'dcf8e74239d8b577aff9b945b795a614f8cc1bd7258f04f99a186ab32e6ceb18'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'connection_momentum', 'first': 332, 'last': 340, 'sha256': '535db3aa5173a0be102fc7d54342aea7175c4518a029280212df48464ddfc80e'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'reduced_momenta', 'first': 342, 'last': 349, 'sha256': '9fbfc9ba16c8585383461623765b6f1f16e30dcec05d5608d7e2ead915e66bb9'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'phase_momentum', 'first': 413, 'last': 419, 'sha256': '65d559e41586e1189e5f6d7b53a209795d4af24299c5f9b6294ce7cc52d927e3'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'phase_inventory', 'first': 428, 'last': 435, 'sha256': '21634e74f441d6c2ea0bc83136530b872dbd1beecd414caf490ccdcf9c012cbe'}, {'file': 'cross_u_saved_full_native_adm_legendre_v002.py', 'name': 'chart_operation_envelopes', 'first': 457, 'last': 480, 'sha256': 'd36b54047e7cff6638f1ce035a1ab6926e4ae13ba5e20aa43b9ffaf905a2f2d9'}]

def shape_quadrature(r,z):
    dr=np.diff(r)[:,None]; dz=np.diff(z)[None,:]
    nodes=(-1/math.sqrt(3),1/math.sqrt(3)); out=[]
    for u in nodes:
        for v in nodes:
            rr=(r[:-1,None]+r[1:,None])/2+u*dr/2
            volume=rr*dr*dz/4
            shapes=[]
            for i,j in ((0,0),(1,0),(0,1),(1,1)):
                si=1 if i else -1; sj=1 if j else -1
                shapes.append(((1+si*u)*(1+sj*v)/4,
                               si*(1+sj*v)/(2*dr),sj*(1+si*u)/(2*dz),i,j))
            out.append((rr,volume,shapes))
    return out


def interpolate(x,shapes):
    val=np.zeros(x.shape[:-2]+(x.shape[-2]-1,x.shape[-1]-1))
    gr=np.zeros_like(val); gz=np.zeros_like(val)
    for n,nr,nz,i,j in shapes:
        xx=x[...,i:x.shape[-2]-1+i,j:x.shape[-1]-1+j]
        val+=n*xx; gr+=nr*xx; gz+=nz*xx
    return val,gr,gz


def lower(g,v):return np.einsum('pab,...pb->...pa',g,v)


def lower_last(g,v):return np.einsum('pab,pcb->pca',g,v)


def raise_cov(hi,v):return np.einsum('pab,...pb->...pa',hi,v)


def covdot(hi,a,b):return np.einsum('...pa,...pa->...p',raise_cov(hi,a),b)


def metric(R,Phi,gr,beta,br):
 n=np.exp(Phi);rho=R/n;m=np.exp(-2*Phi);p=len(R)
 g=np.zeros((p,4,4));g[:,0,0]=-n*n+rho*rho*beta*beta;g[:,0,3]=g[:,3,0]=rho*rho*beta
 g[:,1,1]=g[:,2,2]=m;g[:,3,3]=rho*rho
 hi=np.zeros_like(g);hi[:,0,0]=-1/(n*n);hi[:,0,3]=hi[:,3,0]=beta/(n*n)
 hi[:,1,1]=hi[:,2,2]=1/m;hi[:,3,3]=1/(rho*rho)-beta*beta/(n*n)
 dg=np.zeros((p,4,4,4))
 for a in (1,2):
  nr=n*gr[:,a];rr=rho*((1/R if a==1 else 0)-gr[:,a]);mr=-2*m*gr[:,a];bb=br[:,a]
  dg[:,a,0,0]=-2*n*nr+2*rho*rr*beta*beta+2*rho*rho*beta*bb
  dg[:,a,0,3]=dg[:,a,3,0]=2*rho*rr*beta+rho*rho*bb
  dg[:,a,1,1]=dg[:,a,2,2]=mr;dg[:,a,3,3]=2*rho*rr
 Ga=np.zeros_like(dg)
 for a in range(4):
  for b in range(4):
   Ga[:,:,a,b]=np.einsum('plm,pm->pl',hi,(dg[:,a,b,:]+dg[:,b,a,:]-dg[:,:,a,b]))/2
 RAW.update(current_metric=g,current_inverse=hi,current_metric_jet=dg,current_connection=Ga)
 return g,hi,dg,Ga,n,rho


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


def trial_point(r,z,x,odd,xi,w,omega,shapes,R,Z,sel):
 val,dr,dz=interpolate(x,shapes);ov,orr,oz=interpolate(odd,shapes)
 Phi=B*val[0][sel];gr=np.zeros((len(R),4));gr[:,1]=B*dr[0][sel];gr[:,2]=B*dz[0][sel]
 beta=ov[0][sel];chi=ov[1][sel];br=np.zeros_like(gr);cr=np.zeros_like(gr)
 br[:,1]=orr[0][sel];br[:,2]=oz[0][sel];cr[:,1]=orr[1][sel];cr[:,2]=oz[1][sel]
 g,hi,dg,Ga,n,rho=metric(R,Phi,gr,beta,br);c=np.cosh(chi);ss=np.sinh(chi)
 U=np.zeros((len(R),4));U[:,0]=c/n;U[:,3]=ss/rho-beta*c/n;du=np.zeros((len(R),4,4))
 E=np.zeros_like(U);E[:,0]=ss/n;E[:,3]=c/rho-beta*ss/n;de=np.zeros_like(du)
 for a in (1,2):
  lr=(1/R if a==1 else 0)-gr[:,a]
  du[:,a,0]=(ss*cr[:,a]-c*gr[:,a])/n
  du[:,a,3]=(c*cr[:,a]-ss*lr)/rho-br[:,a]*c/n-beta*du[:,a,0]
  de[:,a,0]=(c*cr[:,a]-ss*gr[:,a])/n
  de[:,a,3]=(ss*cr[:,a]-c*lr)/rho-br[:,a]*ss/n-beta*de[:,a,0]
 zz=np.zeros((32,len(R),4));pz=np.zeros((32,len(R),4,4));sw=np.sqrt(w)[:,None]
 zz[:,:,1]=B*val[1::2][:,sel]/sw;zz[:,:,2]=B*val[2::2][:,sel]/sw
 for a,der in ((1,dr),(2,dz)):
  pz[:,:,a,1]=B*der[1::2][:,sel]/sw;pz[:,:,a,2]=B*der[2::2][:,sel]/sw
 phi=np.zeros_like(U);phi[:,0]=QBAR
 s=features(g,hi,Ga,U,du,zz,pz,phi,omega,xi,w);s.update(R=R,Z=Z,Phi=Phi,gr=gr,n=n,rho=rho,E=E,de=de)
 return s


def metric_partial(s):
 # Metric compatibility recovers the same exact first metric jet, no second derivatives.
 a=np.einsum('plam,pln->pamn',s['Ga'],s['g'])
 return a+np.swapaxes(a,2,3)


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


def phase_momentum(s,PX,PXX):
 X=np.sqrt(-covdot(s['hi'],s['phi'],s['phi']));v=-raise_cov(s['hi'],s['phi'])/X[:,None]
 J=PX[:,None]*v-raise_cov(s['hi'],s['r']);dens=np.sqrt(-np.linalg.det(s['g']))
 PU00=s['hi'][:,0,0]+s['U'][:,0]**2
 slope=dens*(PXX*v[:,0]**2-(PX/X)*(s['hi'][:,0,0]+v[:,0]**2)-PU00)
 env=dens*(abs(PXX)*v[:,0]**2+abs(PX/X)*(abs(s['hi'][:,0,0])+v[:,0]**2)+abs(s['hi'][:,0,0])+s['U'][:,0]**2)
 return dens*J[:,0],slope,env,J,X


def phase_inventory(s,W,u,fixed):
 eta=fixed['Hunit']/LIGHT;Q0=fixed['Q0_over_Hstar']*eta;ep=fixed['eps'];norm=1/ep-math.log1p(1/ep)
 assert ep==1e-5 and np.all((u>0)&(u<ep))
 q=np.sqrt(1+u);ss=u/(ep-u);Abar=1.5*fixed['OA']/fixed['rG'];fac=2*eta*eta/C
 X=np.sqrt(-covdot(s['hi'],s['phi'],s['phi']));PX=W/X
 PXX=fac*Abar*(2*ss/(ep*norm)+4*q*q/(norm*(ep-u)**2))/Q0**2
 p,slope,env,J,X=phase_momentum(s,PX,PXX)
 return dict(p_phi=p,phi_velocity_slope=slope,phi_velocity_slope_envelope=env,J_phi=J,X=X,P_X=PX,P_XX=PXX,phase_u=u,phase_clock_domain=(u>0)&(u<ep))


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
  assert isinstance(a,np.ndarray) and a.dtype.kind in 'fiu'
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
 out={}
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert json.loads(str(f['metadata_json']))==rec['metadata']
  for n in names:
   a=f[n].copy();RAW['loaded_'+n]=a
   s=rec['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a)),n
   out[n]=a
 return out

def authenticate_helpers():
 # Compile/AST source comparison only; the copied definitions are not imported.
 trees={}
 own=ast.parse(Path(__file__).read_text());own_defs={n.name:n for n in own.body if isinstance(n,ast.FunctionDef)}
 for row in HELPER_SPANS:
  if row['file'] not in trees:
   text=path(row['file']).read_text();tree=ast.parse(text);trees[row['file']]=(text,{n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)})
  text,defs=trees[row['file']];node=defs[row['name']]
  assert node.lineno==row['first'] and node.end_lineno==row['last']
  raw=ast.get_source_segment(text,node)+'\n';assert hashlib.sha256(raw.encode()).hexdigest()==row['sha256']
  assert ast.dump(node,include_attributes=False)==ast.dump(own_defs[row['name']],include_attributes=False)

def admission():
 ins={}
 def add(n,h):
  n=str(path(n).resolve());assert isinstance(h,str) and len(h)==64 and (n not in ins or ins[n]==h);ins[n]=h
 for n,h in PINS.items():add(n,h)
 add(STEM+'.md',PROTOCOL_SHA);add(__file__,sha(__file__))
 parents={}
 for stem in (METRIC,ADM,BAND,PHASE,COMPACT):
  r=json.loads(path(stem+'_RESULT.json').read_text());rc=json.loads(path(stem+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and rc['result_sha256']==PINS[stem+'_RESULT.json']
  assert all(v is False for v in r['qualification'].values())
  for key in ('input_sha256','output_sha256'):
   for n,h in rc[key].items():add(n,h)
  parents[stem]=(r,rc)
 for n,h in ins.items():assert sha(path(n))==h,n
 authenticate_helpers()
 metric,mrc=parents[METRIC];adm,arc=parents[ADM];band,brc=parents[BAND];phase,prc=parents[PHASE];compact,crc=parents[COMPACT]
 assert mrc['owner']['pid']==13990 and arc['owner']['pid']==20012 and brc['owner']['pid']==88234 and prc['owner']['pid']==20822
 assert metric['status']=='CONDITIONAL_FULL_METRIC_WEAK_MEASURES_ARITHMETIC_PASS'
 assert adm['status']=='CONDITIONAL_COMPACT_LEGENDRE_ARITHMETIC_PASS' and band['status']=='CONDITIONAL_LINEAR_PASS' and phase['status']=='CONDITIONAL_INITIAL_PHASE_EULER_RATE_PASS'
 assert compact['status']=='CONDITIONAL_CANONICAL_CONSTRAINT_SOURCE_ARITHMETIC_PASS'
 for parent,count in ((metric,36),(adm,60),(band,22),(phase,20),(compact,42)):
  assert len(parent['controls'])==count and all(c['passed'] for c in parent['controls'])
  assert [c['sigma'] for c in parent['cases']]==list(SIGMAS)
 initial=metric['checkpoints'][0]
 for n,shape in dict(r_kpc=[87],z_kpc=[45],final_state=[65,87,45],xi=[32],weights=[32]).items():assert initial['metadata']['schema'][n]==dict(shape=shape,dtype='float64',finite=True)
 fixed=initial['metadata']['owned_fixed'];assert fixed==adm['checkpoints'][0]['metadata']['fixed'] and fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 cp=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_EPS_1em05_CP.json').read_text())
 shared=json.loads(path('CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json').read_text());assert cp==next(c for c in shared['rows'] if c['eps']==1e-5)
 sf=dict(shared['manifest']['fixed_parent']);sf['eps']=1e-5;assert sf==fixed
 for case in band['cases']:
  rec=case['final_checkpoint'];assert case['status']=='LINEAR_PASS' and case['original_residual']<=1e-10
  assert rec['metadata']['schema']['physical_beta_chi']==dict(shape=[2,87,45],dtype='float64',finite=True)
 return ins,metric,adm,band,phase,compact,fixed,cp

def geometry(even,odds):
 global RAW
 RAW={};r,z=even['r_kpc'],even['z_kpc'];assert r.shape==(87,) and z.shape==(45,) and r[0]==z[0]==0 and np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
 f=np.stack(np.broadcast_arrays(r[:,None],z[None,:]));table=[];parts=[];pgrad=[];loc=[];der=[];volumes=[];save={}
 for iq,(rr,vol,shapes) in enumerate(shape_quadrature(r,z)):
  R=np.broadcast_to(rr,vol.shape);Z=np.broadcast_to(sum(n*z[j:len(z)-1+j][None,:] for n,nr,nz,i,j in shapes),vol.shape)
  assert R.size==Z.size==vol.size==POINTS_PER_COLUMN and np.all(R>0) and np.all(vol>0)
  values,vr,vz=interpolate(f,shapes)
  parts.append(np.full(vol.size,sum(n for n,nr,nz,i,j in shapes)))
  pgrad.append(np.stack((np.broadcast_to(sum(nr for n,nr,nz,i,j in shapes),vol.shape),np.broadcast_to(sum(nz for n,nr,nz,i,j in shapes),vol.shape)),axis=-1).reshape(-1,2))
  loc.append(values.reshape(2,-1).T);der.append(np.stack((vr,vz),axis=-1).reshape(2,-1,2).transpose(1,0,2))
  volumes.append(vol.sum());save.update({f'q{iq}_R':R.ravel().copy(),f'q{iq}_Z':Z.ravel().copy(),f'q{iq}_reference_volume':vol.ravel().copy()})
  table.append((R,Z,vol,shapes))
 RAW.update(save)
 a=np.concatenate(parts);b=np.concatenate(pgrad);check('Q1_partition_and_derivative_identity',np.r_[a,b.ravel()],np.r_[np.ones_like(a),np.zeros(b.size)],np.ones(a.size+b.size)*4)
 actual=np.concatenate(loc);expected=np.concatenate([np.column_stack((R.ravel(),Z.ravel())) for R,Z,vol,shapes in table]);derivative=np.concatenate(der);target=np.broadcast_to(np.eye(2),derivative.shape)
 check('Q1_affine_coordinate_and_gradient_identity',np.r_[actual.ravel(),derivative.ravel()],np.r_[expected.ravel(),target.ravel()],np.r_[abs(actual).ravel()+abs(expected).ravel()+1,abs(derivative).ravel()+abs(target).ravel()+1])
 v=np.array([sum(volumes)]);target=np.array([(r[-1]**2-r[0]**2)*(z[-1]-z[0])/2]);check('whole_upper_half_reference_R_measure',v,target,abs(v)+abs(target))
 x=even['final_state'];pairs=[x[1::2,0,:].ravel(),x[2::2,:,0].ravel()]
 for odd in odds:pairs.extend((odd[0,0]-odd[0,1],odd[1,0]))
 actual=np.concatenate(pairs);check('inherited_axis_and_reflection_node_parity',actual,np.zeros_like(actual),np.ones_like(actual))
 RAW.update(save);rec=checkpoint('GEOMETRY',RAW,dict(kind='all_four_Q2_columns_no_compact_selection',point_count=POINTS_PER_ARM,column_count=4,controls=list(CHECKS),axis='R=0 nodes retained; quadrature R>0',sheet='upper-half reflected distribution once',physical_changes=[]))
 return table,rec

def scatter_q1(values,weight,shapes,nr,nz):
 loads=np.zeros((values.shape[1],nr,nz));cell=(nr-1,nz-1)
 for N,NR,NZ,i,j in shapes:loads[:,i:nr-1+i,j:nz-1+j]+=np.moveaxis((values*weight[:,None]*N).reshape(cell+(values.shape[1],)),-1,0)
 return loads

def whole_column(case,iq,table,even,odd,xi,w,omega,fixed,cp,metric_case,compact_case):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};start=len(CHECKS);CONTEXT.update(sigma=case['sigma'],column=iq,stage='whole_slice_column')
 rr,zz,vol,shapes=table;sel=np.ones(vol.shape,dtype=bool);R=rr.ravel();Z=zz.ravel();dv=vol.ravel();weight=dv/R
 inside=(rr>2)&(rr<48)&(zz<16);outside=~inside;ix=np.flatnonzero(inside.ravel());ox=np.flatnonzero(outside.ravel())
 assert len(ix)==(1972,1972,1938,1938)[iq] and len(ix)+len(ox)==POINTS_PER_COLUMN
 label=f'q{iq}_'
 primitive=('g','hi','Ga','U','du','z','dz','phi','V','D','a','r','f','Pi','mu','PiU','A','Phi')
 old=read_pair(metric_case['checkpoint'],[label+k for k in primitive]+[label+'R',label+'Z',label+'reference_volume'])
 old_canonical=read_pair(compact_case['checkpoint'],[label+'old_native_canonical_momentum']+[label+'phase_'+k for k in ('p','P_X','P_XX','Pstar','Wstar')])
 old_u=read_pair(metric_case['checkpoint'],[f'b0_d0_q{iq}_phase_u_chart'])[f'b0_d0_q{iq}_phase_u_chart']
 new=trial_point(even['r_kpc'],even['z_kpc'],even['final_state'],odd,xi,w,omega,shapes,R[ox],Z[ox],outside)
 def merged(k,axis):
  other=new[k];prior=old[label+k];shape=list(other.shape);shape[axis]=POINTS_PER_COLUMN;out=np.empty(shape,dtype=other.dtype)
  si=[slice(None)]*out.ndim;si[axis]=ix;so=[slice(None)]*out.ndim;so[axis]=ox
  assert prior.shape[axis]==len(ix) and other.shape[axis]==len(ox);out[tuple(si)]=prior;out[tuple(so)]=other;return out
 s={k:merged(k,1 if k in ('z','dz','V','D','f','Pi','mu') else 0) for k in primitive}
 s.update(omega=omega,xi=xi,w=w,R=R,Z=Z)
 # Complete only inexpensive kinematic contacts absent from saved selected records;
 # do not reevaluate their native Pi/PiU or fixed99 canonical momentum map.
 s['uc']=lower(s['g'],s['U']);s['P']=np.eye(4)[None]+np.einsum('pa,pb->pab',s['uc'],s['U']);s['Z']=np.einsum('j,jpa->pa',w,s['z'])
 s['nu']=s['du']+np.einsum('pbal,pl->pab',s['Ga'],s['U']);nuc=lower_last(s['g'],s['nu']);s['F']=nuc-nuc.swapaxes(1,2);s['Fup']=np.einsum('pac,pcd,pdb->pab',s['hi'],s['F'],s['hi'])
 c=adm_chart(s);ce=chart_operation_envelopes(s,c)
 AR=AVAILABLE
 for n in ('g','hi','Ga','U','du','z','dz','phi','PiU','Pi','mu','P','F','a','V','D'):AR[n]=s[n].copy()
 for n in ('h','ih','N','beta','u','up','gamma','JU','JzU','Jzz','Uh','zh','embed','dens','sqrt_h','old_velocity','K','Ktrace','pi_EH'):AR['chart_'+n]=c[n].copy()
 unit=np.einsum('pa,pab,pb->p',s['U'],s['g'],s['U'])+1;ue=np.einsum('pa,pab,pb->p',abs(s['U']),abs(s['g']),abs(s['U']))+1
 transverse=np.einsum('pa,jpa->jp',s['U'],s['z']);te=np.einsum('pa,jpa->jp',abs(s['U']),abs(s['z']))
 actual=np.r_[unit,c['rebuilt_U'].ravel(),c['rebuilt_zt'].ravel(),transverse.ravel()];expected=np.r_[np.zeros_like(unit),s['U'].ravel(),s['z'][:,:,0].ravel(),np.zeros(transverse.size)]
 env=np.r_[ue,ce['rebuilt_U'].ravel()+abs(s['U']).ravel(),ce['rebuilt_zt'].ravel()+abs(s['z'][:,:,0]).ravel(),te.ravel()]
 check(f's{case["sigma"]}_q{iq}_unit_transverse_covector_chart',actual,expected,env)
 dg=metric_partial(s);left=np.einsum('plm,pln->pmn',abs(s['Ga'][:,:,0,:]),abs(s['g']));gde=left+left.transpose(0,2,1)
 velocity_env=np.einsum('pia,pa->pi',gde[:,1:,:],abs(s['U']))+np.einsum('pia,pa->pi',abs(s['g'][:,1:,:]),abs(s['du'][:,0]))
 t=np.r_[dg[:,0].ravel(),s['du'][:,0].ravel(),s['dz'][:,:,0].ravel(),c['old_velocity'].ravel()]
 e=np.r_[gde.ravel(),abs(s['du'][:,0]).ravel(),abs(s['dz'][:,:,0]).ravel(),np.column_stack((velocity_env,np.zeros((len(R),96)))).ravel()]
 check(f's{case["sigma"]}_q{iq}_declared_stationary_temporal_seed',t,np.zeros_like(t),e)
 cn=adm_chart(new);cen=chart_operation_envelopes(new,cn);pyn,pmn=reduced_momenta(new,cn);CT,CD,CM=connection_momentum(s)
 py=np.empty((len(R),99));py[ix]=old_canonical[label+'old_native_canonical_momentum'];py[ox]=pyn
 pm=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',CT[:,0],c['embed'])+np.einsum('pa,pka->pk',s['PiU'][:,0],c['Uh'])+np.einsum('jp,jpk->pk',s['Pi'][:,:,0,0],c['zh']))
 # Independent tensor pullback operands retained before the weak projection.
 pu=np.einsum('pa,pai->pi',new['PiU'][:,0],cn['JU'])+np.einsum('jp,jpi->pi',new['Pi'][:,:,0,0],cn['JzU'])
 pz=new['Pi'][:,:,0,1:]+new['Pi'][:,:,0,0,None]*cn['Jzz'][None]
 alt=cn['dens'][:,None]*np.concatenate((pu,pz.transpose(1,0,2).reshape(len(ox),96)),axis=1)
 pe=cn['dens'][:,None]*np.concatenate((np.einsum('pa,pai->pi',abs(new['PiU'][:,0]),cen['JU'])+np.einsum('jp,jpi->pi',abs(new['Pi'][:,:,0,0]),cen['JzU']),(abs(new['Pi'][:,:,0,1:])+abs(new['Pi'][:,:,0,0,None])*cen['Jzz'][None]).transpose(1,0,2).reshape(len(ox),96)),axis=1)
 me=c['dens'][:,None]*(np.einsum('pmn,pkmn->pk',abs(CT[:,0]),abs(c['embed']))+np.einsum('pa,pka->pk',abs(s['PiU'][:,0]),abs(c['Uh']))+np.einsum('jp,jpk->pk',abs(s['Pi'][:,:,0,0]),abs(c['zh'])))
 actual=np.r_[pyn.ravel(),py[ix].ravel(),old[label+'R'],old[label+'Z'],old[label+'reference_volume'],pm[ox].ravel()]
 expected=np.r_[alt.ravel(),old_canonical[label+'old_native_canonical_momentum'].ravel(),R[ix],Z[ix],dv[ix],pmn.ravel()]
 envelope=np.r_[pe.ravel()+abs(alt).ravel(),2*abs(py[ix]).ravel(),abs(R[ix])+abs(old[label+'R']),abs(Z[ix])+abs(old[label+'Z']),abs(dv[ix])+abs(old[label+'reference_volume']),me[ox].ravel()+abs(pmn).ravel()]
 check(f's{case["sigma"]}_q{iq}_canonical_reuse_registration_and_new_pullback',actual,expected,envelope)
 eta=fixed['Hunit']/LIGHT;ep=fixed['eps'];norm=1/ep-math.log1p(1/ep);u0=ep*cp['background']['s']/(1+cp['background']['s'])
 un=u0+(1+u0)*np.expm1(-2*new['Phi']);AR['new_phase_u']=un.copy();assert np.all((un>0)&(un<ep))
 ss=un/(ep-un);qq=np.sqrt(1+un);fac=2*eta*eta/C;Abar=1.5*fixed['OA']/fixed['rG']
 Wn=fac*Abar*qq*(2*qq*ss/(ep*norm));Pn=fac*Abar*((np.log1p(ss)-ss/(1+ss))/norm-1)
 pn=phase_inventory(new,Wn,un,fixed)
 phase_u=np.empty(len(R));phase_u[ix]=old_u;phase_u[ox]=un
 PX=np.empty(len(R));PXX=np.empty(len(R));Pstar=np.empty(len(R));W=np.empty(len(R));p_phi=np.empty(len(R))
 for a,key,other in ((PX,'P_X',pn['P_X']),(PXX,'P_XX',pn['P_XX']),(Pstar,'Pstar',Pn),(W,'Wstar',Wn),(p_phi,'p',pn['p_phi'])):
  a[ix]=old_canonical[label+'phase_'+key];a[ox]=other
 pcheck,slope,slope_env,J,X=phase_momentum(s,PX,PXX);assert np.all(slope>0) and np.all((phase_u>0)&(phase_u<ep))
 phase=dict(p_phi=p_phi,P_X=PX,P_XX=PXX,X=X,phi_velocity_slope=slope,J_phi=J)
 b=np.einsum('pi,pi->p',c['u'],c['up']);closed=c['sqrt_h']*(PX-X*b)
 expected_ratio=np.exp(-2*s['Phi']);normgap=X*X/(100*eta)**2-1-phase_u
 vp=-raise_cov(s['hi'],s['phi'])/X[:,None];rraise=raise_cov(s['hi'],s['r'])
 current_env=c['dens']*(abs(PX*vp[:,0])+abs(rraise[:,0]))+abs(closed)+abs(p_phi)
 actual=np.r_[c['dens']/R,normgap,p_phi,pcheck];expected=np.r_[expected_ratio,np.zeros_like(normgap),closed,p_phi]
 envelope=np.r_[abs(c['dens']/R)+abs(expected_ratio),X*X/(100*eta)**2+1+abs(phase_u),current_env,current_env]
 check(f's{case["sigma"]}_q{iq}_phase_reuse_domain_density_and_full_charge',actual,expected,envelope)
 AR.update(compact_reused_whole_indices=ix.astype(np.int64),new_whole_indices=ox.astype(np.int64),compact_old_native_canonical_momentum=old_canonical[label+'old_native_canonical_momentum'].copy(),compact_old_phase_p=old_canonical[label+'phase_p'].copy(),phase_u=phase_u.copy())
 pmEH=np.einsum('pij,kij->pk',c['pi_EH'],metric_basis());total_metric=pm+pmEH
 canonical=np.concatenate((py,total_metric,phase['p_phi'][:,None]),axis=1)
 loads=scatter_q1(canonical,weight,shapes,87,45)
 # Constant and affine Q1 tests supply independent p/R versus R-volume checks.
 lhs=np.stack((loads.sum(axis=(1,2)),np.einsum('kij,i->k',loads,even['r_kpc']),np.einsum('kij,j->k',loads,even['z_kpc'])))
 rhs=np.stack((np.einsum('p,pk->k',weight,canonical),np.einsum('p,p,pk->k',weight,R,canonical),np.einsum('p,p,pk->k',weight,Z,canonical)))
 le=np.stack((np.einsum('p,pk->k',weight,abs(canonical)),np.einsum('p,p,pk->k',weight,R,abs(canonical)),np.einsum('p,p,pk->k',weight,Z,abs(canonical))))
 check(f's{case["sigma"]}_q{iq}_Q1_p_over_R_weak_moments',lhs,rhs,le+abs(lhs)+abs(rhs))
 AR.update(R=R,Z=Z,reference_volume=dv,p_over_R_weak_weight=weight,native_canonical_density=py,metric_native_canonical_density=pm,metric_EH_canonical_density=pmEH,metric_total_canonical_density=total_metric,canonical_density_106=canonical,Q1_weak_loads=loads,phase_Pstar=Pstar,phase_Wstar=W,phase_P_X=phase['P_X'],phase_P_XX=phase['P_XX'],phase_X=X,phase_canonical_density=phase['p_phi'],phase_velocity_slope=phase['phi_velocity_slope'],phase_current=phase['J_phi'],connection_momentum_time=CT[:,0].copy(),connection_native_time=CD[:,0].copy(),connection_Maxwell_time=CM[:,0].copy())
 ci,cj=np.indices((86,44));AR.update(cell_i=ci.ravel().astype(np.int64),cell_j=cj.ravel().astype(np.int64))
 for a,(N,NR,NZ,i,j) in enumerate(shapes):AR[f'corner{a}_shape']=np.full(len(R),N);AR[f'corner{a}_shape_R']=np.broadcast_to(NR,vol.shape).ravel().copy();AR[f'corner{a}_shape_Z']=np.broadcast_to(NZ,vol.shape).ravel().copy()
 AR.update({n:a.copy() for n,a in RAW.items() if n.startswith('control_')})
 rec=checkpoint('COLUMN',AR,dict(kind='pointwise_L2_stationary_seed_covector_Cauchy_inventory',sigma=case['sigma'],column=iq,points=POINTS_PER_COLUMN,controls=CHECKS[start:],configuration_source='exact declared nodal trial/interpolation; independent covector chart at quadrature',temporal_seed='all primitive coordinate time partial jets zero; covariant time derivatives retain connection',weak_normalization='upper half/per unit azimuth; p/R times authentic R dR dZ; no added mirror2 or2pi',velocity_scope='pointwise stationary seed only; no Q1 nodal velocity inverse or owned-K increment yet',unknowns=dict(full_Cauchy_slice=None,metric_constraint_solution=None,ordinary_cosmic_density=None,exterior_ports=None,activity_outside_0p3_15p1=None,physical_history=None),compact_parent_file=compact_case['checkpoint']['file'],compact_parent_sha256=compact_case['checkpoint']['sha256'],metric_parent_file=metric_case['checkpoint']['file'],metric_parent_sha256=metric_case['checkpoint']['sha256'],reused_points=len(ix),new_points=len(ox),physical_changes=[]))
 RAW={};AVAILABLE={};return rec,loads

def run_arm(case,tables,even,odd,xi,w,fixed,cp,metric_case,compact_case):
 global RAW,AVAILABLE
 RAW={};AVAILABLE={};start=len(CHECKS);sigma=case['sigma'];rows=[];total=np.zeros((106,87,45));POINTS=0
 omega=sigma*xi*fixed['Hunit']/LIGHT
 parent_frequency=next(c for c in ADM_PARENT['cases'] if c['sigma']==sigma)['checkpoint'];old=read_pair(parent_frequency,['omega_star'])['omega_star']
 check(f's{sigma}_unchanged_native_frequency',omega,old,abs(omega)+abs(old))
 for iq,table in enumerate(tables):
  rec,loads=whole_column(case,iq,table,even,odd,xi,w,omega,fixed,cp,metric_case,compact_case);rows.append(rec);total+=loads;POINTS+=POINTS_PER_COLUMN
 actual=total.copy();expected=np.zeros_like(total)
 for rec in rows:expected+=read_pair(rec,['Q1_weak_loads'])['Q1_weak_loads']
 check(f's{sigma}_whole_slice_Q1_weak_sum',actual,expected,abs(actual)+abs(expected));assert POINTS==POINTS_PER_ARM
 RAW['whole_Q1_weak_loads']=total.copy();RAW['point_count']=np.array([POINTS],dtype=np.int64)
 summary=checkpoint('ARM_SUMMARY',RAW,dict(kind='all15136_point_inventory_and_weak_load_sum',sigma=sigma,column_files=[r['file'] for r in rows],column_sha256=[r['sha256'] for r in rows],controls=CHECKS[start:],unknowns=dict(nodal_velocity=None,metric_boundary=None,exterior=None,formation_history=None,ordinary_volume_state=None),physical_changes=[]))
 return dict(sigma=sigma,status='CONDITIONAL_WHOLE_SLICE_INVENTORY',columns=[dict(file=r['file'],sha256=r['sha256'],commit_file=r['commit_file'],commit_sha256=r['commit_sha256']) for r in rows],summary=summary,qualification=FLAGS)

def main():
 global np,OWNER,INPUTS,RAW,AVAILABLE,QBAR,ADM_PARENT
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS or not args.root_run:raise SystemExit('Guarded whole-slice source: final FULL source/protocol admission and root-only evaluation required.')
 assert not list(BASE.glob(STEM+'_*')),'Own runtime prefix occupied.'
 INPUTS,metric,ADM_PARENT,band,phase,compact,fixed,cp=admission();OWNER=dict(owner='root',pid=os.getpid(),started=now(),source_file=Path(__file__).name,source_sha256=sha(__file__))
 cases=[];exit_code=0
 try:
  json_file(STEM+'_OWNER_START.json',OWNER);json_file(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=INPUTS,configuration=dict(points_per_arm=POINTS_PER_ARM,columns=4,modes=32,canonical_fields=99,weak_fields=106,controls=CONTROL_COUNT,pairs=PAIR_COUNT,sigma=SIGMAS,tolerance=TOL),parent_metric_result_file=METRIC+'_RESULT.json',parent_metric_result_sha256=PINS[METRIC+'_RESULT.json'],qualification=FLAGS))
  import numpy as _np
  np=_np
  even=read_pair(metric['checkpoints'][0],('r_kpc','z_kpc','final_state','xi','weights'));xi,w=even['xi'],even['weights'];assert np.all(xi>0) and np.all(w>0)
  QBAR=metric['checkpoints'][0]['metadata']['phase_Qbar_star'];assert math.isfinite(QBAR) and QBAR>0
  odds=[read_pair(c['final_checkpoint'],('physical_beta_chi',))['physical_beta_chi'] for c in band['cases']]
  arrays={k:v.copy() for k,v in even.items()};arrays.update({f'sigma{i}_physical_beta_chi':a.copy() for i,a in enumerate(odds)})
  checkpoint('INPUT',arrays,dict(kind='unchanged_full87x45_nodal_trial_and_four_rotating_fields',fixed=fixed,owned_EPS5_background=cp['background'],phase_Qbar_star=QBAR,copied_metric_controls=metric['controls'],copied_canonical_controls=ADM_PARENT['controls'],copied_phase_controls=phase['controls'],copied_band_controls=band['controls'],old_wall_scope='original finitebox trial values retained, not physical junction data',activity_scope='observational activity only0.3..15.1; outside unknown; no activity enters this producer',physical_changes=[]))
  tables,geo=geometry(even,odds)
  for case,odd,mc,cc in zip(band['cases'],odds,metric['cases'],compact['cases']):cases.append(run_arm(case,tables,even,odd,xi,w,fixed,cp,mc,cc))
  assert len(RECORDS)==PAIR_COUNT and len(CHECKS)==CONTROL_COUNT and all(c['passed'] for c in CHECKS)
  recheck();rh=json_file(STEM+'_RESULT.json',dict(owner=OWNER,status='CONDITIONAL_WHOLE_SLICE_CAUCHY_INVENTORY_PASS',cases=cases,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS))
  publish(STEM+'_REPORT.md',(f'# {STEM}\n\nAll four stationary trial inventories;15136 points/arm,32 modes,99 native canonical fields,106 pointwise/weak fields. {len(CHECKS)} arithmetic controls/{len(RECORDS)} pairs.\n\nPointwise L2 configurations and canonical densities with R-weighted Q1 weak loads are conditional Cauchy free-data operands. No nodal velocity reconstruction, owned-K increment, phase evolution, physical Cauchy preparation, constraint solution, ordinary cosmic volume state, exterior/current port, junction or metric-geodesic velocity is adopted.\n').encode())
  recheck();rc=dict(owner=OWNER,status='CLOSED',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc);assert json.loads(path(STEM+'_RECEIPT.json').read_text())==canonical(rc);recheck()
  print('CONDITIONAL_WHOLE_SLICE_CAUCHY_INVENTORY_PASS',len(CHECKS),len(RECORDS))
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None;available=dict(AVAILABLE);available.update(RAW)
  if np is not None and available:
   try:checkpoint('ERROR_RAW',available,dict(kind='unaccepted_available_whole_slice_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:seal_actual();recheck(False)
  except BaseException:close_error=traceback.format_exc()
  prior=sha(path(STEM+'_RECEIPT.json')) if path(STEM+'_RECEIPT.json').exists() else None
  if prior:OUTPUTS[STEM+'_RECEIPT.json']=prior
  en=json_file(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,completed_cases=cases,checkpoints=RECORDS,input_sha256=INPUTS,preserved_outputs=dict(OUTPUTS),prior_receipt_sha256=prior,unqualified_npz=[p.name for p in BASE.glob(STEM+'_*.npz') if p.name not in {r['file'] for r in RECORDS}],unqualified_commits=[p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json') if p.name not in {r['commit_file'] for r in RECORDS}],qualification=FLAGS))
  if prior is None:
   rc=dict(owner=OWNER,status='CLOSED_ERROR',closed=now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),error_sha256=en,qualification=FLAGS);json_file(STEM+'_RECEIPT.json',rc)
  seal_actual();recheck(False);raise
 return exit_code

if __name__=='__main__':raise SystemExit(main())
