"""Held definitions only: exact analytic directional contractions, never executed here.

Caller supplies np and the admitted ALPHA, ELL, B, GC, C constants. s is the actual
forthcoming Euler seed and c its chart; d contains directional g,hi,Ga,U,du,z,dz.
The primitive mixed time jets and gauge coefficients require separate admission.
No accepted float-allocation helper is differentiated by a dual-number wrapper.
No source import, fixture, state/field recovery, inverse, solve or evolution occurs.
"""
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False

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
