"""Definitions only: one compact shared a=f metric contact at node (43,22).
Caller supplies np, reviewed a_*/normal_pair_* helpers and keep(name,array).
No import, invocation, field/feature replay, global solve or rate response here.
Q=psi diag(1,1,R^2), with the exact registered hat/R/Z and R-power jets.
CovUi/covzi and their OWNED firstjets, BOTH mechanical-rate words, phi,
N/beta and gauge jets are held. Supplied mechanical_jets are authoritative.
Differentiated Eq2 supplies all time/R/Z/phi chart contacts; no second jets.
The stored connection representative is varied covariantly, preserving its
finite metric-compatibility gap. Its algebraic-LC derivative is saved separately.
Finite chart/readout defects are diagnostics, never subtracted from the state.
Offsheet support gives zero ordinary-sheet contact; exterior ports stay unknown.
This is a configuration partial derivative, not an induced global Legendre rate.
Immutable v001158/088a864c retained; v002 adds genuine owned firstjet inputs
and saves raw-versus-owned values and differentiated readout contacts.
"""

def compact_contact_dot(x,y):
 return normal_pair_sum(a_mul(x,y),x[0].ndim-1)

def compact_lift_matvec(A,x):
 product=a_mul(A,(x[0][...,None,:],x[1][...,None,:]))
 return normal_pair_sum(product,product[0].ndim-1)

def compact_metric_hat(geo,iq,keep,label):
 assert type(iq) is int and 0<=iq<4
 ci,cj=geo['cell_i'],geo['cell_j'];psi=np.zeros(3784);pr=psi.copy();pz=psi.copy()
 for a,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  mask=(ci+di==43)&(cj+dj==22)
  for target,jet in ((psi,0),(pr,1),(pz,2)):target[mask]=geo['hats'][iq,a,jet].reshape(3784)[mask]
 take=np.flatnonzero(psi!=0);keep(label+'_indices',take);assert take.shape==(4,)
 R=geo['R'][iq,take];Q=np.zeros((4,3,3));Qa=np.zeros((4,4,3,3))
 for i,factor in enumerate((np.ones(4),np.ones(4),R**2)):
  Q[:,i,i]=psi[take]*factor;Qa[:,1,i,i]=pr[take]*factor;Qa[:,2,i,i]=pz[take]*factor
 Qa[:,1,2,2]+=2*R*psi[take]
 for n,x in dict(psi=psi[take],psi_R=pr[take],psi_Z=pz[take],Q=Q,Q_jet=Qa).items():keep(label+'_'+n,x)
 assert np.all((ci[take]>=42)&(ci[take]<=43)&(cj[take]>=21)&(cj[take]<=22))
 return take,Q,Qa

def compact_metric_configuration_contact(s,c,jets,mechanical_jets,Q,Qa,keep,label):
 p=len(s['U']);assert Q.shape==(p,3,3) and Qa.shape==(p,4,3,3)
 assert np.array_equal(Q,Q.swapaxes(1,2)) and np.all(Qa[:,0]==0) and np.all(Qa[:,3]==0)
 put=lambda n,x:normal_keep_pair(label+'_'+n,x,keep)
 N,beta,w,gamma=c['N'],c['beta'],c['up'],c['gamma'];zsp=s['z'][:,:,1:]
 cj=paired_normal_chart_jets(s,c,jets,keep,label+'_background_chart')
 for n in ('u','z','h','N','beta'):put('owned_first_'+n,mechanical_jets[n])
 for n,a in (('h','dh'),('N','dN'),('beta','dbeta')):put('raw_minus_owned_first_'+n,a_sub(cj[a],mechanical_jets[n]))
 dih=a_mul64(-1.,normal_pair_sandwich(c['ih'],a_dd(Q),c['ih']));put('dih',dih)
 Qw=a_matvec(Q,a_dd(w));dw=put('delta_up',a_mul64(-1.,a_matvec(c['ih'],Qw)))
 sq=compact_contact_dot(a_dd(w),Qw);dgam=put('delta_gamma',a_div64(a_mul64(-.5,sq),gamma,keep,label+'_delta_gamma_division'))
 e0=a_div64(dgam,N,keep,label+'_eta0_division');eta=put('delta_U',a_stack([e0]+[a_sub(a_slice(dw,(slice(None),i)),a_mul64(beta[:,i],e0)) for i in range(3)],axis=1))
 A=compact_contact_dot(a_dd(w[None]),a_dd(zsp));dA=compact_contact_dot((dw[0][None],dw[1][None]),a_dd(zsp))
 dz0=a_mul64(-N[None],a_sub(a_div64(dA,gamma[None],keep,label+'_delta_z0_first'),a_div64(a_mul(A,(dgam[0][None],dgam[1][None])),gamma[None]**2,keep,label+'_delta_z0_second')))
 dzvalue=a_dd(np.zeros_like(s['z']));dzvalue[0][:,:,0]=dz0[0];dzvalue[1][:,:,0]=dz0[1];put('delta_z',dzvalue)
 q=a_dd(np.zeros((p,4,4)));q[0][:,1:,1:]=Q
 qb=a_matvec(Q,a_dd(beta));q00=compact_contact_dot(a_dd(beta),qb)
 for i in range(3):q[0][:,0,i+1]=q[0][:,i+1,0]=qb[0][:,i];q[1][:,0,i+1]=q[1][:,i+1,0]=qb[1][:,i]
 q[0][:,0,0]=q00[0];q[1][:,0,0]=q00[1];put('delta_g',q)
 dhi=put('delta_hi',a_mul64(-1.,normal_pair_sandwich(s['hi'],q,s['hi'])))
 dq=a_dd(np.zeros((p,4,4,4)));dq[0][:,:,1:,1:]=Qa
 eta_jet=a_dd(np.zeros((p,4,4)));zeta_jet=a_dd(np.zeros_like(jets['dz'][0]));w_jet=[];gamma_jet=[]
 for a in range(4):
  ha=a_slice(mechanical_jets['h'],(slice(None),a,slice(None),slice(None)));ia=a_mul64(-1.,normal_pair_sandwich(c['ih'],ha,c['ih']))
  ua_raw=a_dd(np.zeros((p,3)))
  for i in range(3):
   x=compact_contact_dot(a_dd(s['g'][:,i+1]),a_slice(jets['du'],(slice(None),a,slice(None))))
   x=a_add(x,compact_contact_dot(a_slice(jets['dg'],(slice(None),a,i+1,slice(None))),a_dd(s['U'])))
   ua_raw[0][:,i]=x[0];ua_raw[1][:,i]=x[1]
  ua=a_slice(mechanical_jets['u'],(slice(None),a,slice(None)));put('raw_minus_owned_covU_first_%d'%a,a_sub(ua_raw,ua))
  wa=a_add(compact_lift_matvec(ia,a_dd(c['u'])),a_matvec(c['ih'],ua));w_jet.append(wa)
  ga=a_div64(a_sub(compact_contact_dot(a_dd(w),ua),a_mul64(.5,compact_contact_dot(a_dd(w),compact_lift_matvec(ha,a_dd(w))))),gamma,keep,label+'_gamma_jet_%d'%a);gamma_jet.append(ga)
  dwa=a_add(compact_lift_matvec(ia,Qw),a_matvec(c['ih'],a_matvec(Qa[:,a],a_dd(w))))
  dwa=a_mul64(-1.,a_add(dwa,a_matvec(c['ih'],a_matvec(Q,wa))))
  dsa=a_add(compact_contact_dot(wa,Qw),compact_contact_dot(a_dd(w),a_matvec(Qa[:,a],a_dd(w))))
  dsa=a_add(dsa,compact_contact_dot(a_dd(w),a_matvec(Q,wa)))
  dga=a_add(a_div64(a_mul64(-.5,dsa),gamma,keep,label+'_delta_gamma_jet_first_%d'%a),a_div64(a_mul64(.5,a_mul(sq,ga)),gamma**2,keep,label+'_delta_gamma_jet_second_%d'%a))
  na=a_slice(mechanical_jets['N'],(slice(None),a));ba=a_slice(mechanical_jets['beta'],(slice(None),a,slice(None)))
  e0a=a_sub(a_div64(dga,N,keep,label+'_eta0_jet_first_%d'%a),a_div64(a_mul(dgam,na),N**2,keep,label+'_eta0_jet_second_%d'%a))
  ea=a_stack([e0a]+[a_sub(a_sub(a_slice(dwa,(slice(None),i)),a_mul(a_slice(ba,(slice(None),i)),e0)),a_mul64(beta[:,i],e0a)) for i in range(3)],axis=1)
  eta_jet[0][:,a]=ea[0];eta_jet[1][:,a]=ea[1];put('delta_du_partial',eta_jet)
  za=a_slice(mechanical_jets['z'],(slice(None),slice(None),a,slice(None)))
  put('raw_minus_owned_covz_first_%d'%a,a_sub(a_slice(jets['dz'],(slice(None),slice(None),a,slice(1,None))),za))
  Aa=a_add(compact_contact_dot((wa[0][None],wa[1][None]),a_dd(zsp)),compact_contact_dot(a_dd(w[None]),za))
  dAa=a_add(compact_contact_dot((dwa[0][None],dwa[1][None]),a_dd(zsp)),compact_contact_dot((dw[0][None],dw[1][None]),za))
  first=a_div64(dAa,gamma[None],keep,label+'_zeta_jet_first_%d'%a)
  first=a_sub(first,a_div64(a_mul(dA,(ga[0][None],ga[1][None])),gamma[None]**2,keep,label+'_zeta_jet_second_%d'%a))
  second=a_add(a_mul(Aa,(dgam[0][None],dgam[1][None])),a_mul(A,(dga[0][None],dga[1][None])))
  first=a_sub(first,a_div64(second,gamma[None]**2,keep,label+'_zeta_jet_third_%d'%a))
  first=a_add(first,a_div64(a_mul64(2.,a_mul(a_mul(A,(dgam[0][None],dgam[1][None])),(ga[0][None],ga[1][None]))),gamma[None]**3,keep,label+'_zeta_jet_fourth_%d'%a))
  zja=a_sub(a_mul64(-N[None],first),a_mul((na[0][None],na[1][None]),a_mul64(-1.,a_div64(dz0,N[None],keep,label+'_zeta_lapse_part_%d'%a))))
  zeta_jet[0][:,:,a,0]=zja[0];zeta_jet[1][:,:,a,0]=zja[1];put('delta_dz_partial',zeta_jet)
  qba=a_add(a_matvec(Qa[:,a],a_dd(beta)),a_matvec(Q,ba));q00a=a_add(compact_contact_dot(ba,qb),compact_contact_dot(a_dd(beta),qba))
  for i in range(3):dq[0][:,a,0,i+1]=dq[0][:,a,i+1,0]=qba[0][:,i];dq[1][:,a,0,i+1]=dq[1][:,a,i+1,0]=qba[1][:,i]
  dq[0][:,a,0,0]=q00a[0];dq[1][:,a,0,0]=q00a[1];put('delta_dg_partial',dq)
 put('delta_du',eta_jet);put('delta_dz',zeta_jet);put('delta_dg',dq)
 # The raw covector readout contact is the derivative of its retained gap.
 du_readout=[]
 for a in range(4):
  rows=[]
  for i in range(3):
   x=a_add(compact_contact_dot(a_slice(q,(slice(None),i+1,slice(None))),a_slice(jets['du'],(slice(None),a,slice(None)))),compact_contact_dot(a_dd(s['g'][:,i+1]),a_slice(eta_jet,(slice(None),a,slice(None)))))
   x=a_add(x,compact_contact_dot(a_slice(dq,(slice(None),a,i+1,slice(None))),a_dd(s['U'])))
   x=a_add(x,compact_contact_dot(a_slice(jets['dg'],(slice(None),a,i+1,slice(None))),eta));rows.append(x)
  du_readout.append(a_stack(rows,1))
 put('delta_raw_minus_owned_covU_first',a_stack(du_readout,1))
 put('delta_raw_minus_owned_covz_first',a_slice(zeta_jet,(slice(None),slice(None),slice(None),slice(1,None))))
 put('delta_raw_minus_owned_h_first',a_sub(a_slice(dq,(slice(None),slice(None),slice(1,None),slice(1,None))),a_dd(Qa)))
 nq=[]
 for a in range(4):
  G=a_slice(jets['Ga'],(slice(None),slice(None),a,slice(None)))
  reaction=a_add(compact_contact_matrix_product(a_transpose(G,(0,2,1)),q),compact_contact_matrix_product(q,G))
  nq.append(a_sub(a_slice(dq,(slice(None),a,slice(None),slice(None))),reaction))
 dG=put('delta_Ga_covariant',normal_pair_connection_from_jet(s['hi'],a_stack(nq,axis=1),keep,label+'_connection'))
 lm=put('log_dens',a_mul64(.5,normal_pair_sum(normal_pair_sum(a_mul64(c['ih'],a_dd(Q)),2),1)))
 dc=compact_contact_chart_derivatives(s,c,Q,dih,dw,dgam,eta,dzvalue,lm,keep,label+'_chart_derivative')
 d=dict(g=q,hi=dhi,U=eta,z=dzvalue,du=eta_jet,dz=zeta_jet,Ga=dG)
 compact_contact_geometry_gaps(s,c,jets,d,Q,keep,label+'_gaps')
 return d,dc,dict(Q=Q,Q_jet=Qa,background_chart_jets=dict(dh=mechanical_jets['h'],dN=mechanical_jets['N'],dbeta=mechanical_jets['beta']),raw_background_chart_jets=cj,owned_mechanical_jets=mechanical_jets,up_jet=a_stack(w_jet,1),gamma_jet=a_stack(gamma_jet,1),mechanical_rate_variation_zero=True,global_induced_rate_computed=False)

def compact_contact_matrix_product(A,B):
 return a_stack([compact_lift_matvec(A,a_slice(B,(Ellipsis,slice(None),j))) for j in range(B[0].shape[-1])],axis=-1)

def compact_contact_chart_derivatives(s,c,Q,dih,dw,dgam,eta,dz,lm,keep,label):
 put=lambda n,x:normal_keep_pair(label+'_'+n,x,keep)
 N,w,gamma,beta=c['N'],c['up'],c['gamma'],c['beta'];zsp=s['z'][:,:,1:];p=len(w)
 dJU0=a_sub(a_div64(dw,N[:,None]*gamma[:,None],keep,label+'_JU_first'),a_div64(a_mul64(w,(dgam[0][:,None],dgam[1][:,None])),N[:,None]*gamma[:,None]**2,keep,label+'_JU_second'))
 dJU=a_stack([dJU0]+[a_sub(a_slice(dih,(slice(None),i,slice(None))),a_mul64(beta[:,i,None],dJU0)) for i in range(3)],axis=1)
 dJzz=a_mul64(-N[:,None],a_sub(a_div64(dw,gamma[:,None],keep,label+'_Jzz_first'),a_div64(a_mul64(w,(dgam[0][:,None],dgam[1][:,None])),gamma[:,None]**2,keep,label+'_Jzz_second')))
 A=compact_contact_dot(a_dd(w[None]),a_dd(zsp));dA=compact_contact_dot((dw[0][None],dw[1][None]),a_dd(zsp));zz=a_matvec(c['ih'],a_dd(zsp));dzz=compact_lift_matvec((dih[0][None],dih[1][None]),a_dd(zsp))
 dJzU=a_sub(a_div64(dzz,gamma[None,:,None],keep,label+'_JzU_first_full'),a_div64(a_mul(zz,(dgam[0][None,:,None],dgam[1][None,:,None])),gamma[None,:,None]**2,keep,label+'_JzU_second_full'))
 numer=a_add(a_mul64(w[None],(dA[0][:,:,None],dA[1][:,:,None])),a_mul((A[0][:,:,None],A[1][:,:,None]),(dw[0][None],dw[1][None])))
 dJzU=a_sub(dJzU,a_div64(numer,gamma[None,:,None]**3,keep,label+'_JzU_third'))
 numer=a_mul64(3*w[None],a_mul((A[0][:,:,None],A[1][:,:,None]),(dgam[0][None,:,None],dgam[1][None,:,None])))
 dJzU=a_mul64(-N[None,:,None],a_add(dJzU,a_div64(numer,gamma[None,:,None]**4,keep,label+'_JzU_fourth')))
 dUh=[];dzh=[]
 for ai,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  E=np.zeros((p,3,3));E[:,i,j]=E[:,j,i]=1.;Ew=a_matvec(E,a_dd(w));wh=a_mul64(-1.,a_matvec(c['ih'],Ew))
  gh=a_div64(a_mul64(-.5,compact_contact_dot(a_dd(w),Ew)),gamma,keep,label+'_Uh_gamma_%d'%ai)
  dwh=a_mul64(-1.,a_add(compact_lift_matvec(dih,Ew),a_matvec(c['ih'],a_matvec(E,dw))))
  dgh=a_add(a_div64(a_mul64(-.5,a_add(compact_contact_dot(dw,Ew),compact_contact_dot(a_dd(w),a_matvec(E,dw)))),gamma,keep,label+'_dUh_gamma_first_%d'%ai),a_div64(a_mul64(-1.,a_mul(gh,dgam)),gamma,keep,label+'_dUh_gamma_second_%d'%ai))
  dh0=a_div64(dgh,N,keep,label+'_dUh0_%d'%ai);dUh.append(a_stack([dh0]+[a_sub(a_slice(dwh,(slice(None),k)),a_mul64(beta[:,k],dh0)) for k in range(3)],axis=1))
  Bh=compact_contact_dot((wh[0][None],wh[1][None]),a_dd(zsp));dBh=compact_contact_dot((dwh[0][None],dwh[1][None]),a_dd(zsp))
  value=a_sub(a_div64(dBh,gamma[None],keep,label+'_dzh_first_%d'%ai),a_div64(a_mul(Bh,(dgam[0][None],dgam[1][None])),gamma[None]**2,keep,label+'_dzh_second_%d'%ai))
  value=a_sub(value,a_div64(a_add(a_mul(dA,(gh[0][None],gh[1][None])),a_mul(A,(dgh[0][None],dgh[1][None]))),gamma[None]**2,keep,label+'_dzh_third_%d'%ai))
  value=a_add(value,a_div64(a_mul64(2.,a_mul(a_mul(A,(gh[0][None],gh[1][None])),(dgam[0][None],dgam[1][None]))),gamma[None]**3,keep,label+'_dzh_fourth_%d'%ai));dzh.append(a_mul64(-N[None],value))
 dc=dict(ih=dih,up=dw,gamma=dgam,JU=dJU,JzU=dJzU,Jzz=dJzz,Uh=a_stack(dUh,1),zh=a_stack(dzh,2),embed=a_dd(np.zeros_like(c['embed'])),dens=a_mul64(c['dens'],lm),sqrt_h=a_mul64(c['sqrt_h'],lm),log_dens=lm)
 for n,x in dc.items():put(n,x)
 return dc

def compact_contact_geometry_gaps(s,c,jets,d,Q,keep,label):
 put=lambda n,x:normal_keep_pair(label+'_'+n,x,keep)
 LC=normal_pair_connection_from_jet(s['hi'],jets['dg'],keep,label+'_algebraic_LC');gap=put('LC_minus_stored_Ga',a_sub(LC,jets['Ga']))
 E=[];dE=[]
 for a in range(4):
  G=a_slice(jets['Ga'],(slice(None),slice(None),a,slice(None)))
  reaction=a_add(normal_pair_right(a_transpose(G,(0,2,1)),s['g']),normal_pair_left(s['g'],G))
  E.append(a_sub(a_slice(jets['dg'],(slice(None),a,slice(None),slice(None))),reaction))
  dG=a_slice(d['Ga'],(slice(None),slice(None),a,slice(None)))
  dreaction=a_add(normal_pair_right(a_transpose(dG,(0,2,1)),s['g']),normal_pair_left(s['g'],dG))
  dreaction=a_add(dreaction,a_add(compact_contact_matrix_product(a_transpose(G,(0,2,1)),d['g']),compact_contact_matrix_product(d['g'],G)))
  dE.append(a_sub(a_slice(d['dg'],(slice(None),a,slice(None),slice(None))),dreaction))
 put('base_metric_compatibility',a_stack(E,1));put('delta_metric_compatibility',a_stack(dE,1));diff=a_dd(np.zeros_like(gap[0]))
 for a in range(4):
  for b in range(4):
   value=a_mul64(-1.,a_matvec(s['hi'],compact_lift_matvec(d['g'],a_slice(gap,(slice(None),slice(None),a,b)))))
   diff[0][:,:,a,b]=value[0];diff[1][:,:,a,b]=value[1]
 put('delta_Ga_algebraic_minus_covariant_predicted',diff)
 alg=normal_pair_connection_from_jet(s['hi'],d['dg'],keep,label+'_delta_algebraic_LC_fixed_inverse')
 inverse_part=a_dd(np.zeros_like(alg[0]))
 for a in range(4):
  for b in range(4):
   terms=a_sub(a_add(a_slice(jets['dg'],(slice(None),a,b,slice(None))),a_slice(jets['dg'],(slice(None),b,a,slice(None)))),a_slice(jets['dg'],(slice(None),slice(None),a,b)))
   value=a_mul64(.5,compact_lift_matvec(d['hi'],terms));inverse_part[0][:,:,a,b]=value[0];inverse_part[1][:,:,a,b]=value[1]
 alg=put('delta_Ga_algebraic',a_add(alg,inverse_part));actual=put('delta_Ga_algebraic_minus_covariant',a_sub(alg,d['Ga']))
 put('finite_inverse_contact_gap',a_sub(actual,diff))
 constraint=a_div64(a_mul64(-1.,compact_contact_dot((d['U'][0][None],d['U'][1][None]),a_dd(s['z']))),s['U'][None,:,0],keep,label+'_normalized_z0_contact')
 put('Eq2_z0_minus_normalized_contact',a_sub(a_slice(d['z'],(slice(None),slice(None),0)),constraint))
 return dict(base_metric_compatibility_defect_retained=True,algebraic_LC_contact_adopted=False,finite_derivative_defect_saved=True)
