"""Definitions only: positive operation bounds for paired normal action134.
Signed primitives/features/momenta are consumed elsewhere, never replayed here.
Input op contains pilot's uncancelled du/dz/dg/Ga bounds. Configuration is fixed.
All projector, polarization, connection, inverse and quadratic bounds precede
their signed cancellations. Curvature envelopes and ordinary source are supplied
once by the caller. These bounds do not replace the original 1e-10 bridge test.
Caller supplies np,C,ALPHA,ELL,B,GC,connection_from_jet_envelope and keep.
No definitions, arrays, helpers, physical fields or operators evaluated by author.
"""

def normal_positive_save(label,rows,keep):
 for n,a in rows.items():keep(label+'_'+n,a);assert np.all(np.isfinite(a)) and np.all(a>=0),(label,n)
 return rows

def normal_positive_features(s,c,op,keep,label):
 U,z,g,hi=abs(s['U']),abs(s['z']),abs(s['g']),abs(s['hi']);w=abs(s['w']);om=s['omega'][:,None]**2
 uc=np.einsum('pab,pb->pa',g,U);P=np.eye(4)[None]+uc[:,:,None]*U[:,None,:];Z=np.einsum('j,jpa->pa',w,z)
 nu=op['du']+np.einsum('pbal,pl->pab',op['Ga'],U);nz=op['dz']+np.einsum('plab,jpl->jpab',op['Ga'],z)
 q=np.einsum('pa,jpab->jpb',U,nz);V=np.einsum('pab,jpb->jpa',P,q);D=np.einsum('pac,jpcd,pbd->jpab',P,nz,P)
 lower=np.einsum('pab,pcb->pca',g,nu);F=lower+lower.swapaxes(1,2);Fup=np.einsum('pac,pcd,pdb->pab',hi,F,hi)
 a=np.einsum('pa,pab->pb',U,nu);Vu=np.einsum('pab,jpb->jpa',hi,V);Du=np.einsum('pac,jpcd,pdb->jpab',hi,D,hi)
 Pi=w[:,None,None,None]*(U[None,:,:,None]*Vu[:,:,None,:]/om[:,:,None,None]+ELL**2*Du)
 PiU=abs(ALPHA)*np.einsum('pac,pcb->pab',hi,F)+U[:,:,None]*Z[:,None,:]
 sym=(Pi+Pi.swapaxes(2,3))/2;Klo=Z[:,:,None,None]*U[:,None,:,None]*U[:,None,None,:]+np.einsum('jpab,jpl->plab',sym,z)
 Kup=np.einsum('plm,pmab->plab',hi,Klo);CC=(Kup.transpose(0,2,1,3)+Kup.transpose(0,2,3,1)+Kup)/2
 CC+=abs(ALPHA)*(Fup[:,:,:,None]*U[:,None,None,:]+Fup[:,:,None,:]*U[:,None,:,None])/2
 K=abs(c['N'])[:,None,None]*op['Ga'][:,0,1:,1:];ih=abs(c['ih']);tr=np.einsum('pij,pij->p',ih,K)
 pi=abs(c['sqrt_h'])[:,None,None]*(np.einsum('pik,pkl,plj->pij',ih,K,ih)+tr[:,None,None]*ih)/(2*abs(C))
 r=np.einsum('pab,pb->pa',P,abs(s['phi']));z2=np.einsum('jpa,pab,jpb->jp',z,hi,z)
 return normal_positive_save(label,dict(uc=uc,P=P,Z=Z,nu=nu,nz=nz,q=q,V=V,D=D,F=F,Fup=Fup,a=a,V_raised=Vu,D_raised=Du,Pi=Pi,PiU=PiU,connection_momentum=CC,K=K,Ktrace=tr,metric_EH_tensor=pi,r=r,z2=z2),keep)

def normal_positive_chart_jets(s,c,op,keep,label):
 hi=abs(s['hi']);dhi=np.einsum('pij,pajk,pkl->pail',hi,op['dg'],hi);N=abs(c['N'])
 dN=N[:,None]**3*dhi[:,:,0,0]/2;dbeta=2*N[:,None,None]*dN[:,:,None]*hi[:,None,0,1:]+N[:,None,None]**2*dhi[:,:,0,1:]
 return normal_positive_save(label,dict(dhi=dhi,dN=dN,dbeta=dbeta,dh=op['dg'][:,:,1:,1:]),keep)

def normal_positive_lift(s,c,op,cj,f,df,b,db,keep,label):
 U,z,g,h,N,beta=abs(s['U']),abs(s['z']),abs(s['g']),abs(c['h']),abs(c['N']),abs(c['beta']);p=len(U)
 f,df,b,db=abs(f),abs(df),abs(b),abs(db);q=np.zeros((p,4,4))
 q[:,0,0]=2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b);q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:]
 eta=np.zeros((p,4));eta[:,0]=U[:,0]*f/N;eta[:,1:]=U[:,0,None]*b+beta*eta[:,0,None]
 ez=np.einsum('pa,jpa->jp',eta,z);zeta=np.zeros_like(z);zeta[:,:,0]=ez/U[None,:,0]
 dq=np.zeros((p,4,4,4));dq[:,:,0,0]=2*cj['dN']*f[:,None]+2*N[:,None]*df
 dq[:,:,0,0]+=2*np.einsum('pai,pij,pj->pa',cj['dbeta'],h,b)+2*np.einsum('pi,paij,pj->pa',beta,cj['dh'],b)+2*np.einsum('pi,pij,paj->pa',beta,h,db)
 dq[:,:,0,1:]=np.einsum('paij,pj->pai',cj['dh'],b)+np.einsum('pij,paj->pai',h,db);dq[:,:,1:,0]=dq[:,:,0,1:]
 deta=np.zeros((p,4,4));deta[:,:,0]=op['du'][:,:,0]*f[:,None]/N[:,None]+U[:,0,None]*df/N[:,None]+U[:,0,None]*f[:,None]*cj['dN']/N[:,None]**2
 deta[:,:,1:]=op['du'][:,:,0,None]*b[:,None,:]+U[:,0,None,None]*db+eta[:,0,None,None]*cj['dbeta']+beta[:,None,:]*deta[:,:,0,None]
 dez=np.einsum('pab,jpb->jpa',deta,z)+np.einsum('pb,jpab->jpa',eta,op['dz']);dzeta=np.zeros_like(op['dz'])
 dzeta[:,:,:,0]=dez/U[None,:,0,None]+ez[:,:,None]*op['du'][None,:,:,0]/U[None,:,0,None]**2
 return normal_positive_save(label,dict(q=q,dq=dq,eta=eta,deta=deta,zeta=zeta,dzeta=dzeta),keep)

def normal_positive_direction(s,c,op,features,curvature,f,df,b,db,keep,label):
 U,z,g,hi=abs(s['U']),abs(s['z']),abs(s['g']),abs(s['hi']);P=features['P'];w=abs(s['w']);om=s['omega'][:,None]**2;kj=(B*GC)**2*s['xi'][:,None]**4
 cj=normal_positive_chart_jets(s,c,op,keep,label+'_chart');lift=normal_positive_lift(s,c,op,cj,f,df,b,db,keep,label+'_lift')
 q,eta=lift['q'],lift['eta'];nq=lift['dq']+np.einsum('plam,pln->pamn',op['Ga'],q)+np.einsum('plan,pml->pamn',op['Ga'],q)
 dG=connection_from_jet_envelope(hi,nq);dnu=lift['deta']+np.einsum('pbal,pl->pab',dG,U)+np.einsum('pbal,pl->pab',op['Ga'],eta)
 dnz=np.einsum('plab,jpl->jpab',dG,z);duc=np.einsum('pab,pb->pa',q,U)+np.einsum('pab,pb->pa',g,eta)
 dP=duc[:,:,None]*U[:,None,:]+features['uc'][:,:,None]*eta[:,None,:];dqq=np.einsum('pa,jpab->jpb',eta,features['nz'])+np.einsum('pa,jpab->jpb',U,dnz)
 dV=np.einsum('pab,jpb->jpa',dP,features['q'])+np.einsum('pab,jpb->jpa',P,dqq)
 dD=np.einsum('pac,jpcd,pbd->jpab',dP,features['nz'],P)+np.einsum('pac,jpcd,pbd->jpab',P,dnz,P)+np.einsum('pac,jpcd,pbd->jpab',P,features['nz'],dP)
 lower=np.einsum('pab,pcb->pca',q,features['nu'])+np.einsum('pab,pcb->pca',g,dnu);dF=lower+lower.swapaxes(1,2)
 da=np.einsum('pa,pab->pb',eta,features['nu'])+np.einsum('pa,pab->pb',U,dnu);dhi=np.einsum('pac,pcd,pdb->pab',hi,q,hi)
 dr=np.einsum('pab,pb->pa',dP,abs(s['phi']));lm=np.einsum('pab,pba->p',hi,q)/2
 normal_positive_save(label+'_metric_delta',dict(deltaG=dG,dnu=dnu,dnz=dnz,dP=dP,dV=dV,dD=dD,dF=dF,da=da,dhi=dhi,dr=dr,log_measure=lm),keep)
 V,D,F=features['V'],features['D'],features['F'];Vu,Du,Fu=features['V_raised'],features['D_raised'],features['Fup'];z2=features['z2'];r=features['r']
 V2=np.sum(Vu*V,axis=2);D2=np.sum(Du*D,axis=(2,3));F2=np.sum(Fu*F,axis=(1,2));az=np.einsum('pa,jpa->jp',features['a'],z)
 dz2=np.einsum('jpa,pab,jpb->jp',z,dhi,z);dV2=np.einsum('jpa,pab,jpb->jp',V,dhi,V)+2*np.sum(Vu*dV,axis=2)
 dD2=2*np.sum(Du*dD,axis=(2,3));dF2=2*np.sum(Fu*dF,axis=(1,2))
 for A0,A1 in ((dhi,hi),(hi,dhi)):
  dD2+=np.einsum('pac,jpab,pbd,jpcd->jp',A0,D,A1,D);dF2+=np.einsum('pac,pab,pbd,pcd->p',A0,F,A1,F)
 r2=np.einsum('pa,pab,pb->p',r,hi,r);dr2=np.einsum('pa,pab,pb->p',r,dhi,r)+2*np.einsum('pa,pab,pb->p',r,hi,dr)
 modal=np.stack((V2/(2*om),z2/2,z2*z2/(4*kj),ELL**2*D2/2,az),axis=-1)
 dmodal=np.stack((dV2/(2*om),dz2/2,z2*dz2/(2*kj),ELL**2*dD2/2,np.einsum('pa,jpa->jp',da,z)),axis=-1)
 primal=np.column_stack((abs(ALPHA)*F2/4,r2/2,np.einsum('j,jpk->pk',w,modal)));variation=np.column_stack((abs(ALPHA)*dF2/4,dr2/2,np.einsum('j,jpk->pk',w,dmodal)));native=variation+lm[:,None]*primal
 zeta=lift['zeta'];nzeta=lift['dzeta']+np.einsum('plab,jpl->jpab',op['Ga'],zeta);qq=np.einsum('pa,jpab->jpb',U,nzeta)
 vv=np.einsum('pab,jpb->jpa',P,qq);dd=np.einsum('pac,jpcd,pbd->jpab',P,nzeta,P);zz=np.einsum('jpa,pab,jpb->jp',z,hi,zeta)
 zm=np.stack((np.sum(Vu*vv,axis=2)/om,zz,z2*zz/kj,ELL**2*np.sum(Du*dd,axis=(2,3)),np.einsum('pa,jpa->jp',features['a'],zeta)),axis=-1)
 mode=np.column_stack((np.zeros((len(U),2)),np.einsum('j,jpk->pk',w,zm)))
 dX=np.einsum('pa,pab,pb->p',abs(s['phi']),dhi,abs(s['phi']))/(2*abs(s['phase_X']));phase=np.column_stack((abs(s['phase_PX'])*dX,abs(s['phase_P'])*lm))
 f,df,b,db=abs(f),abs(df),abs(b),abs(db);K,kt,pi=features['K'],features['Ktrace'],features['metric_EH_tensor'];ih=abs(c['ih'])
 curvature_term=(f*curvature['envelope_Q']+np.einsum('pi,pi->p',df[:,1:],curvature['envelope_V']))/(2*abs(C))
 kinetic=f*abs(c['sqrt_h'])*(kt**2+np.einsum('pij,pik,pkl,plj->p',K,ih,K,ih))/(2*abs(C))
 Lie=np.einsum('pi,pijk->pjk',b,cj['dh'][:,1:])+np.einsum('pik,pjk->pij',abs(c['h']),db[:,1:])+np.einsum('pkj,pik->pij',abs(c['h']),db[:,1:])
 EH=np.column_stack((curvature_term,kinetic,np.einsum('pij,pij->p',pi,Lie)))
 components=np.column_stack((abs(c['dens'])*native.sum(axis=1),abs(c['dens'])*mode.sum(axis=1),abs(c['dens'])*phase.sum(axis=1),EH.sum(axis=1)))
 return normal_positive_save(label,dict(native_metric_terms=native,mode_compensation_terms=mode,absolute_phase_terms=phase,EH_terms=EH,component_densities=components,coefficient=components.sum(axis=1)),keep)

def normal_positive_primary(s,c,features,keep,label):
 U,z,h,beta,N=abs(s['U']),abs(s['z']),abs(c['h']),abs(c['beta']),abs(c['N']);p=len(U);out=np.zeros((p,4))
 for row in range(4):
  q=np.zeros((p,4,4));eta=np.zeros((p,4))
  if row==0:q[:,0,0]=2*N;eta[:,0]=U[:,0]/N;eta[:,1:]=beta*eta[:,0,None]
  else:
   i=row-1;q[:,0,0]=2*np.einsum('pi,pi->p',beta,h[:,:,i]);q[:,0,1:]=h[:,:,i];q[:,1:,0]=q[:,0,1:];eta[:,i+1]=U[:,0]
  zeta=np.einsum('pa,jpa->jp',eta,z)/U[None,:,0]
  out[:,row]=abs(c['dens'])*(np.einsum('pab,pab->p',features['connection_momentum'][:,0],q)+np.einsum('pa,pa->p',features['PiU'][:,0],eta)+np.einsum('jp,jp->p',features['Pi'][:,:,0,0],zeta))
  keep(label+'_partial',out)
 return normal_positive_save(label,dict(primary=out),keep)['primary']
