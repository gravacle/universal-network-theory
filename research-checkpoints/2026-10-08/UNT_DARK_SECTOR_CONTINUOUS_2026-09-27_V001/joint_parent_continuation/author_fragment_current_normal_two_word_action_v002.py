"""Definitions only: same normal1101 action on two-word first jets.
Configuration/test-only coefficients retain the original binary64 convention.
All rate-dependent contractions retain both words and every hh/hl/lh/ll term.
Caller supplies reviewed a_*, a_div64, normal_pair_* and affine jet helpers,
np,C,ALPHA,ELL,B,GC. ROOT alone evaluates an admitted containing producer.
Fixed curvature Q/V and ordinary annular source are each assembled once.
No source, gauge, history, pressure subtraction, physical port or law changes.
The original FE 1e-10 momentum bridge is a separate mandatory caller gate.
Preserved unexecuted v001 SHA 6ea87fd4085fed799e03ff507cdcaba06f4b1095f089b5727472025c43b77f31.
"""

def normal_action_reduce(x,axes):
 for axis in sorted(((a+x[0].ndim) if a<0 else a for a in axes),reverse=True):x=normal_pair_sum(x,axis)
 return x

def normal_action_dot(x,y,axes):return normal_action_reduce(a_mul(x,y),axes)

def paired_normal_chart_jets(s,c,j,keep,label):
 dg=j['dg'];dhi=a_transpose(normal_pair_sandwich(s['hi'],a_transpose(dg,(1,0,2,3)),s['hi']),(1,0,2,3));dhi=(-dhi[0],-dhi[1])
 dN=a_mul64(c['N'][:,None]**3/2,a_slice(dhi,(slice(None),slice(None),0,0)))
 db=a_add(a_mul64(2*c['N'][:,None,None]*s['hi'][:,None,0,1:],(dN[0][:,:,None],dN[1][:,:,None])),a_mul64(c['N'][:,None,None]**2,a_slice(dhi,(slice(None),slice(None),0,slice(1,None)))))
 out=dict(dN=dN,dbeta=db,dh=a_slice(dg,(slice(None),slice(None),slice(1,None),slice(1,None))))
 for n,x in out.items():normal_keep_pair(label+'_'+n,x,keep)
 return out

def paired_normal_lift(s,c,j,cj,f,df,b,db,keep,label):
 N,h,beta,U,z=c['N'],c['h'],c['beta'],s['U'],s['z'];p=len(U)
 q=np.zeros((p,4,4));q[:,0,0]=-2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b);q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:]
 eta=np.empty_like(U);eta[:,0]=-U[:,0]*f/N;eta[:,1:]=-U[:,0,None]*b-beta*eta[:,0,None]
 ez=np.einsum('pa,jpa->jp',eta,z);zeta=np.zeros_like(z);zeta[:,:,0]=-ez/U[None,:,0]
 for n,x in dict(q=q,eta=eta,zeta=zeta,compensation_numerator=ez).items():keep(label+'_'+n,x)
 dq=a_dd(np.zeros((p,4,4,4)));d00=a_add(a_mul64(-2*f[:,None],cj['dN']),a_dd(-2*N[:,None]*df+2*np.einsum('pi,pij,paj->pa',beta,h,db)))
 for i in range(3):
  for k in range(3):
   d00=a_add(d00,a_mul64((2*h[:,i,k]*b[:,k])[:,None],a_slice(cj['dbeta'],(slice(None),slice(None),i))))
   d00=a_add(d00,a_mul64((2*beta[:,i]*b[:,k])[:,None],a_slice(cj['dh'],(slice(None),slice(None),i,k))));normal_keep_pair(label+'_dq00_partial',d00,keep)
 dq[0][:,:,0,0]=d00[0];dq[1][:,:,0,0]=d00[1]
 for i in range(3):
  value=a_dd(np.einsum('pk,pak->pa',h[:,i],db))
  for k in range(3):value=a_add(value,a_mul64(b[:,k,None],a_slice(cj['dh'],(slice(None),slice(None),i,k))))
  dq[0][:,:,0,i+1]=dq[0][:,:,i+1,0]=value[0];dq[1][:,:,0,i+1]=dq[1][:,:,i+1,0]=value[1]
 normal_keep_pair(label+'_dq',dq,keep)
 du0=a_slice(j['du'],(slice(None),slice(None),0));de0=a_add(a_mul64((-f/N)[:,None],du0),a_dd(-U[:,0,None]*df/N[:,None]))
 de0=a_add(de0,a_mul64((U[:,0]*f/N**2)[:,None],cj['dN']));deta=a_dd(np.zeros_like(s['du']));deta[0][:,:,0]=de0[0];deta[1][:,:,0]=de0[1]
 for i in range(3):
  value=a_add(a_mul64(-b[:,i,None],du0),a_dd(-U[:,0,None]*db[:,:,i]))
  value=a_sub(value,a_mul64(eta[:,0,None],a_slice(cj['dbeta'],(slice(None),slice(None),i))));value=a_sub(value,a_mul64(beta[:,i,None],de0))
  deta[0][:,:,i+1]=value[0];deta[1][:,:,i+1]=value[1]
 normal_keep_pair(label+'_deta',deta,keep);dez=a_dd(np.zeros((32,p,4)))
 for a in range(4):
  dez=a_add(dez,a_mul64(z[:,:,a,None],a_slice(deta,(slice(None),slice(None),a))))
  dez=a_add(dez,a_mul64(eta[None,:,a,None],a_slice(j['dz'],(slice(None),slice(None),slice(None),a))));normal_keep_pair(label+'_compensation_numerator_jet_partial',dez,keep)
 dz0=a_add(a_div64((-dez[0],-dez[1]),U[None,:,0,None],keep,label+'_dzeta_division'),a_mul64(ez[:,:,None]/U[None,:,0,None]**2,(du0[0][None],du0[1][None])))
 dzeta=a_dd(np.zeros_like(s['dz']));dzeta[0][:,:,:,0]=dz0[0];dzeta[1][:,:,:,0]=dz0[1];normal_keep_pair(label+'_dzeta',dzeta,keep)
 return dict(q=q,dq=dq,eta=eta,deta=deta,zeta=zeta,dzeta=dzeta)

def paired_normal_metric_delta(s,j,feature,lift,keep,label):
 q,eta=lift['q'],lift['eta'];F=feature['paired'];U,z,g,hi,P=s['U'],s['z'],s['g'],s['hi'],s['P'];nq=[]
 for a in range(4):
  ga=a_slice(j['Ga'],(slice(None),slice(None),a,slice(None)))
  connection=a_add(normal_pair_right(a_transpose(ga,(0,2,1)),q),normal_pair_left(q,ga))
  nq.append(a_sub(a_slice(lift['dq'],(slice(None),a,slice(None),slice(None))),connection))
 deltaG=normal_pair_connection_from_jet(hi,a_stack(nq,axis=1),keep,label+'_delta_connection')
 dnu=lift['deta'];dnz=a_dd(np.zeros_like(s['dz']))
 for l in range(4):
  dnu=a_add(dnu,a_mul64(U[:,l,None,None],a_transpose(a_slice(deltaG,(slice(None),slice(None),slice(None),l)),(0,2,1))))
  dnu=a_add(dnu,a_mul64(eta[:,l,None,None],a_transpose(a_slice(j['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1))))
  dnz=a_sub(dnz,a_mul64(z[:,:,l,None,None],a_slice(deltaG,(slice(None),l,slice(None),slice(None)))));normal_keep_pair(label+'_dnu_partial',dnu,keep);normal_keep_pair(label+'_dnz_partial',dnz,keep)
 duc=np.einsum('pab,pb->pa',q,U)+np.einsum('pab,pb->pa',g,eta);dP=duc[:,:,None]*U[:,None,:]+s['uc'][:,:,None]*eta[:,None,:]
 dqq=a_dd(np.zeros_like(F['q'][0]));da=a_dd(np.zeros_like(F['a'][0]))
 for a in range(4):
  dqq=a_add(dqq,a_add(a_mul64(eta[None,:,a,None],a_slice(F['nz'],(slice(None),slice(None),a,slice(None)))),a_mul64(U[None,:,a,None],a_slice(dnz,(slice(None),slice(None),a,slice(None))))))
  da=a_add(da,a_add(a_mul64(eta[:,a,None],a_slice(F['nu'],(slice(None),a,slice(None)))),a_mul64(U[:,a,None],a_slice(dnu,(slice(None),a,slice(None))))));normal_keep_pair(label+'_delta_q_partial',dqq,keep);normal_keep_pair(label+'_delta_acceleration_partial',da,keep)
 dV=a_add(a_matvec(dP,F['q']),a_matvec(P,dqq))
 dD=a_add(normal_pair_sandwich(dP,F['nz'],P.swapaxes(-1,-2)),normal_pair_sandwich(P,F['nz'],dP.swapaxes(-1,-2)));dD=a_add(dD,normal_pair_sandwich(P,dnz,P.swapaxes(-1,-2)))
 lower=a_add(normal_pair_right(F['nu'],q),normal_pair_right(dnu,g));dF=a_sub(lower,a_transpose(lower,(0,2,1)))
 dhi=-np.einsum('pac,pcd,pdb->pab',hi,q,hi);dr=np.einsum('pab,pb->pa',dP,s['phi']);lm=np.einsum('pab,pba->p',hi,q)/2
 out=dict(deltaG=deltaG,dnu=dnu,dnz=dnz,dV=dV,dD=dD,dF=dF,da=da)
 for n,x in out.items():normal_keep_pair(label+'_'+n,x,keep)
 for n,x in dict(dhi=dhi,dr=dr,log_measure=lm).items():keep(label+'_'+n,x)
 return dict(paired=out,dhi=dhi,dr=dr,lm=lm)

def paired_normal_native_metric_terms(s,feature,delta,keep,label):
 F=feature['paired'];D=delta['paired'];hi,dhi=s['hi'],delta['dhi'];om=s['omega'][:,None]**2;kj=(B*GC)**2*s['xi'][:,None]**4
 V2=normal_action_dot(F['V_raised'],F['V'],(2,));D2=normal_action_dot(F['D_raised'],F['D'],(2,3));F2=normal_action_dot(F['Fup'],F['F'],(1,2))
 dV2=a_add(normal_action_dot(a_matvec(dhi,F['V']),F['V'],(2,)),a_mul64(2.,normal_action_dot(F['V_raised'],D['dV'],(2,))))
 dD2=a_mul64(2.,normal_action_dot(F['D_raised'],D['dD'],(2,3)))
 dF2=a_mul64(2.,normal_action_dot(F['Fup'],D['dF'],(1,2)))
 for A0,A1 in ((dhi,hi),(hi,dhi)):
  dD2=a_add(dD2,normal_action_dot(normal_pair_sandwich(A0,F['D'],A1),F['D'],(2,3)))
  dF2=a_add(dF2,normal_action_dot(normal_pair_sandwich(A0,F['F'],A1),F['F'],(1,2)));normal_keep_pair(label+'_delta_D_squared_partial',dD2,keep);normal_keep_pair(label+'_delta_F_squared_partial',dF2,keep)
 az=normal_action_reduce(a_mul64(s['z'],(F['a'][0][None],F['a'][1][None])),(2,));daz=normal_action_reduce(a_mul64(s['z'],(D['da'][0][None],D['da'][1][None])),(2,))
 dz2=np.einsum('jpa,pab,jpb->jp',s['z'],dhi,s['z']);z2=s['z2']
 primal=a_stack((a_div64(V2,2*om,keep,label+'_primal_frequency'),a_dd(-z2/2),a_dd(-z2*z2/(4*kj)),a_mul64(-ELL**2/2,D2),az),axis=-1)
 derivative=a_stack((a_div64(dV2,2*om,keep,label+'_variation_frequency'),a_dd(-dz2/2),a_dd(-z2*dz2/(2*kj)),a_mul64(-ELL**2/2,dD2),daz),axis=-1)
 modal=normal_pair_sum(a_mul64(s['w'][:,None,None],primal),0);dmodal=normal_pair_sum(a_mul64(s['w'][:,None,None],derivative),0)
 r2=np.einsum('pa,pab,pb->p',s['r'],hi,s['r']);dr2=np.einsum('pa,pab,pb->p',s['r'],dhi,s['r'])+2*np.einsum('pa,pab,pb->p',s['r'],hi,delta['dr'])
 p=a_stack([a_mul64(-ALPHA/4,F2),a_dd(-r2/2)]+[a_slice(modal,(slice(None),i)) for i in range(5)],axis=-1)
 dp=a_stack([a_mul64(-ALPHA/4,dF2),a_dd(-dr2/2)]+[a_slice(dmodal,(slice(None),i)) for i in range(5)],axis=-1)
 out=a_add(dp,a_mul64(delta['lm'][:,None],p));normal_keep_pair(label+'_primal',p,keep);normal_keep_pair(label+'_variation_without_measure',dp,keep);return normal_keep_pair(label+'_terms',out,keep)

def paired_normal_z0_terms(s,j,feature,lift,keep,label):
 F=feature['paired'];nz=lift['dzeta'];U,zeta,P=s['U'],lift['zeta'],s['P']
 for l in range(4):nz=a_sub(nz,a_mul64(zeta[:,:,l,None,None],a_slice(j['Ga'],(slice(None),l,slice(None),slice(None)))));normal_keep_pair(label+'_covariant_compensation_jet_partial',nz,keep)
 dq=a_dd(np.zeros_like(F['q'][0]))
 for a in range(4):dq=a_add(dq,a_mul64(U[None,:,a,None],a_slice(nz,(slice(None),slice(None),a,slice(None)))))
 dV=a_matvec(P,dq);dD=normal_pair_sandwich(P,nz,P.swapaxes(-1,-2))
 kinetic=a_div64(normal_action_dot(F['V_raised'],dV,(2,)),s['omega'][:,None]**2,keep,label+'_frequency')
 zeta_dot=np.einsum('jpa,pab,jpb->jp',s['z'],s['hi'],zeta);quartic=s['z2']/((B*GC)**2*s['xi'][:,None]**4)
 gradient=a_mul64(-ELL**2,normal_action_dot(F['D_raised'],dD,(2,3)));acc=normal_action_reduce(a_mul64(zeta,(F['a'][0][None],F['a'][1][None])),(2,))
 modes=a_stack((kinetic,a_dd(-zeta_dot),a_dd(-quartic*zeta_dot),gradient,acc),axis=-1);modal=normal_pair_sum(a_mul64(s['w'][:,None,None],modes),0)
 zero=a_dd(np.zeros(len(U)));out=a_stack([zero,zero]+[a_slice(modal,(slice(None),i)) for i in range(5)],axis=-1)
 normal_keep_pair(label+'_covariant_compensation_jet',nz,keep);return normal_keep_pair(label+'_terms',out,keep)

def paired_normal_EH_terms(s,c,cj,moments,curvature,f,df,b,db,keep,label):
 kinetic=a_sub(a_mul(moments['Ktrace'],moments['Ktrace']),normal_action_dot(moments['K'],normal_pair_sandwich(c['ih'],moments['K'],c['ih']),(1,2)))
 kinetic=a_div64(a_mul64(f*c['sqrt_h'],kinetic),2*C,keep,label+'_kinetic_division')
 cv=a_prod(f,curvature['Q'])
 for i in range(3):cv=a_sub(cv,a_prod(df[:,i+1],curvature['V'][:,i]))
 cv=a_div64(cv,2*C,keep,label+'_curvature_division');Lie=a_dd(np.zeros_like(c['h']))
 for i in range(3):Lie=a_add(Lie,a_mul64(b[:,i,None,None],a_slice(cj['dh'],(slice(None),i+1,slice(None),slice(None)))))
 Lie=a_add(Lie,a_dd(np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])))
 paired_shift=normal_action_dot(moments['metric_EH_tensor'],Lie,(1,2));normal_keep_pair(label+'_unnegated_shift',paired_shift,keep);shift=(-paired_shift[0],-paired_shift[1])
 normal_keep_pair(label+'_Lie_test_h',Lie,keep);out=a_stack((cv,kinetic,shift),axis=-1);return normal_keep_pair(label+'_terms',out,keep)

def paired_normal_direction(s,c,jets,feature,moments,curvature,f,df,b,db,keep,label):
 cj=paired_normal_chart_jets(s,c,jets,keep,label+'_chart');lift=paired_normal_lift(s,c,jets,cj,f,df,b,db,keep,label+'_lift')
 delta=paired_normal_metric_delta(s,jets,feature,lift,keep,label+'_metric_delta')
 native=paired_normal_native_metric_terms(s,feature,delta,keep,label+'_native');mode=paired_normal_z0_terms(s,jets,feature,lift,keep,label+'_z0')
 dX=-np.einsum('pa,pab,pb->p',s['phi'],delta['dhi'],s['phi'])/(2*s['phase_X']);phase=a_stack((a_prod(s['phase_PX'],dX),a_prod(s['phase_P'],delta['lm'])),axis=-1);normal_keep_pair(label+'_absolute_phase_terms',phase,keep)
 EH=paired_normal_EH_terms(s,c,cj,moments,curvature,f,df,b,db,keep,label+'_EH')
 components=a_stack((a_mul64(c['dens'],normal_pair_sum(native,1)),a_mul64(c['dens'],normal_pair_sum(mode,1)),a_mul64(c['dens'],normal_pair_sum(phase,1)),normal_pair_sum(EH,1)),axis=-1)
 coefficient=normal_pair_sum(components,1);normal_keep_pair(label+'_components',components,keep);normal_keep_pair(label+'_coefficient',coefficient,keep)
 return dict(native_metric_terms=native,mode_compensation_terms=mode,absolute_phase_terms=phase,EH_terms=EH,component_densities=components,coefficient=coefficient,configuration_or_law_changed=False,ordinary_source_added_here=False)
