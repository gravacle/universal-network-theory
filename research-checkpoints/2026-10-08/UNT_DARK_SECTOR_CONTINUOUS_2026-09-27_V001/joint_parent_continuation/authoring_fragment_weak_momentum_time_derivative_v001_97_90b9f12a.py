"""Held definitions only: exact analytic directional contractions, never executed here.

Caller supplies np and the admitted ALPHA, ELL, B, GC constants. s is the actual
forthcoming Euler seed and c its chart; d contains directional g,hi,Ga,U,du,z,dz.
The primitive mixed time jets and gauge coefficients require separate admission.
No accepted float-allocation helper is differentiated by a dual-number wrapper.
No source import, fixture, state/field recovery, inverse, solve or evolution occurs.
"""
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False

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
