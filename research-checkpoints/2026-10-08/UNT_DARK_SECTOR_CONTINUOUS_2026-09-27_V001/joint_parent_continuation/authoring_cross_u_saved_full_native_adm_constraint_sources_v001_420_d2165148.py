"""IN-PROGRESS guarded complete-action canonical lapse/shift source block.
No numerical/scientific function is evaluated during authorship. Root only.
"""
from pathlib import Path
import math,ast,hashlib,json,os,traceback
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_FULL_NATIVE_ADM_CONSTRAINT_SOURCES_V001'
PARENT='CROSS_U_SAVED_FULL_NATIVE_ADM_LEGENDRE_V002'
PARENT_RESULT_SHA='PENDING_NATURAL_CLOSURE'
PARENT_RECEIPT_SHA='PENDING_NATURAL_CLOSURE'
np=None
RAW={}
ARM_AVAILABLE={}
LIGHT=299792458.;KPC=3.085677581491367e19;A0=1.0059833281731022e-10
B=A0*KPC/LIGHT**2;C=1.98;KB=.02;ALPHA=KB/C;GC=3*math.pi/8;ELL=.1
SIGMAS=(.1,1.,10.,100.);TOL=2e-11

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
 p=y.shape[0];uy=y[:,:3];zy=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 au=np.einsum('pik,pk->pi',block['A'],uy)+np.einsum('jpik,jpk->pi',block['B'],zy)
 az=np.einsum('jpki,pk->jpi',block['B'],uy)+np.einsum('jpik,jpk->jpi',block['D'],zy)
 return np.concatenate((au,az.transpose(1,0,2).reshape(p,96)),axis=1)


def arrowhead_solve(block,rhs):
 # No subtraction of enormous modal Grams to recover the Maxwell Schur.
 # The exact transverse-span identity must first be certified against saved M.
 p=rhs.shape[0];rr=rhs[:,3:].reshape(p,32,3,-1).transpose(1,0,2,3)
 dsolve=np.linalg.solve(block['D'],rr)
 reduced=rhs[:,:3]-np.einsum('jpik,jpkl->pil',block['B'],dsolve)
 yu=np.linalg.solve(block['Maxwell'],reduced)
 modal_rhs=rr-np.einsum('jpki,pkl->jpil',block['B'],yu)
 yz=np.linalg.solve(block['D'],modal_rhs)
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
 etr=np.einsum('plil->pi',abs(cc))
 eaa=np.einsum('pkij,pk->pij',abs(cc),etr)+np.einsum('plik,pkjl->pij',abs(cc),abs(cc))
 envelope=np.einsum('plij,plij->p',abs(DV),abs(cc))+np.einsum('pjij,pi->p',abs(DV),etr)+np.einsum('pij,pij->p',abs(V),eaa)
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
 es=np.einsum('pij,pij->p',abs(c['pi_EH']),abs(Lie_h))/R
 return dict(normal=normal,shift=shift,normal_envelope=ek+curv['envelope']/(2*C),shift_envelope=es,curvature=curv,paired_GHY_time_port=None,outer_geometry_port=None)


def ordinary_canonical_constraint_rows(g,p_specific,mass_weight,f,b):
 o=ordinary_velocity(g,p_specific)
 normal=mass_weight*o['gamma']*f
 shift=-mass_weight*np.einsum('pi,pi->p',p_specific,b)
 return dict(normal=normal,shift=shift,gamma=o['gamma'],source_support='fixed owned razor-thin rest-mass annuli; no3D density or unknown activity extension')


def main():
 raise SystemExit('Guarded in-progress source; future parent terminal seals, complete EH ADM weak block, controls/custody and independent reviews are pending. No root evaluation admitted.')

if __name__=='__main__':raise SystemExit(main())
