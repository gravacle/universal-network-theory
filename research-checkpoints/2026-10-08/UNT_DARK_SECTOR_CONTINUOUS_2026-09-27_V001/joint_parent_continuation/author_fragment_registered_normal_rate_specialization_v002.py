"""Definitions only: fixed-configuration rate derivative of registered134.
No evaluation, producer, admission, solver, target momentum or Noether formula.
Caller supplies np, admitted a_*, normal_pair_*, normal_action_dot/reduce,
normal_contact_connection, the registered134 chart/lift/metric definitions,
normal_keep_pair, and C/ALPHA/ELL. Both rate words are retained everywhere.

One column has a common CURRENT jets/features/momenta and four NEW W/t rate
increments. Prepare its current chart once; prepare each direction's fixed
test cache once; apply that cache to all four increments. New rate features
and momenta must come from the admitted affine81 with Z=0, and all four slots
of du/dz/Gamma retained. Their DG spatial slots must be exactly zero for this
rate-only branch. The original base df/db, including temporal primary tests,
are retained in the cache; only their RATE increments are zero.

The output is the Frechet delta(delta L), with registered134 doubled contacts.
An exact finite rate update also has its separate increment-squared remainder.
Hamiltonian rows still require the original minus sign and separate F/weight/
hat scatter convention. Fixed curvature, ordinary, phase first jets and all
configuration variables have zero rate derivative here. Existing stationarity,
literal/registered, owned/reconstructed, compatibility, primary and port gaps
are references or explicit new readouts; they are never declared zero by this
kernel. Unknown physical ports stay None. This is not a generator equivalence.

NEW ONE-RESPONSE COMPARISON BEFORE NUMERICAL ADOPTION:
Preserved original200/header SHA e1de0f9dc032cdaf28ca34b6775a3512db477419c5f19affbce136e090d28dfb.
Root selected three patches before reading response results: nodes (43,22),
(21,11),(64,33). Each owns its four adjacent cells and all four Gauss columns,
for 48 owned contacts total; selection uses registered cell_i/j only, no value
or error-based tuning. The first patch is the existing compact-target patch.
Retain every patch, including failures. Full-grid generic comparison remains a
separately held follow-up if discrepancies/domain concerns require root action.
Select one actually earned W/t nodal response and consume its saved genuine
point values/affine66/81 rate jets/features/momenta; do not reconstruct completed
operands. At the SAME owned current contacts compare this cache path against
full166+132 with d(g,hi,U,z)=0, dc=0, configuration-feature contact=0,
dcurvature=0, and those identical supplied response operands. Check every
native7/z07/phase2/EH3/component4/coefficient pair for all16 tests, including
time-primary df/db, before collapse. Use 2e-11 times independent positive
upstream construction bounds for implementation identities; post-cancelled
magnitudes remain diagnostics only. Apply original Q1 incidence/scatter to
each completed patch family and compare four weak patch rows plus its exact
polynomial-transpose functional. Compare CMC with sqrt_h*delta(Ktrace) from
SAME affine81, retaining the Gamma/ADM gap. Original canonical admission and
literal/frozen/owned/primary/physical-port gaps remain separate evidence.
This bounded implementation test uses the full static polynomial derivation;
it is not whole-grid arithmetic, stationarity or physical constraint admission.
The first whole-grid specialization output must earn its own weak functional
controls and retain every gap. Only root-owned natural closure and independent
review may permit broader numerical reuse. No global inverse is authorized.
"""

KERNEL_AUTHOR_DRAFT=True
KERNEL_AUTHORING_IN_PROGRESS=False

def rate_normal_put(keep,label,name,x):
 normal_keep_pair(label+'_'+name,x,keep);return x

def rate_normal_cross(x,y,dx,dy,axes):
 return a_add(normal_action_dot(dx,y,axes),normal_action_dot(x,dy,axes))

def rate_normal_column_cache(s,c,jets,moments,gap_refs,keep,label):
 required=('primitive_legendre','frozen_rate_certificate','owned_vs_reconstructed_jets','metric_compatibility','registered_vs_literal_normal','primary_gauge','physical_ports')
 assert all(n in gap_refs for n in required)
 cj=paired_normal_chart_jets(s,c,jets,keep,label+'_current_chart')
 Ku=normal_pair_sandwich(c['ih'],moments['K'],c['ih']);rate_normal_put(keep,label,'current_K_raised',Ku)
 return dict(chart=cj,K_raised=Ku,gap_refs={n:gap_refs[n] for n in required},physical_adoption=False,exact_generator_equivalence=False)

def rate_normal_test_cache(s,c,jets,feature,column,f,df,b,db,keep,label):
 cj=column['chart'];lift=paired_normal_lift(s,c,jets,cj,f,df,b,db,keep,label+'_current_lift')
 test=paired_normal_metric_delta(s,jets,feature,lift,keep,label+'_current_metric_test')
 q,eta,zeta=lift['q'],lift['eta'],lift['zeta'];U,z,g,P=s['U'],s['z'],s['g'],s['P']
 duc=np.einsum('pab,pb->pa',q,U)+np.einsum('pab,pb->pa',g,eta)
 dP=duc[:,:,None]*U[:,None,:]+s['uc'][:,:,None]*eta[:,None,:]
 ez=np.einsum('pa,jpa->jp',eta,z);nz=lift['dzeta']
 for l in range(4):
  nz=a_sub(nz,a_mul64(zeta[:,:,l,None,None],a_slice(jets['Ga'],(slice(None),l,slice(None),slice(None)))))
  rate_normal_put(keep,label,'current_compensation_covariant_jet_partial',nz)
 qq=a_dd(np.zeros_like(feature['paired']['q'][0]))
 for a in range(4):qq=a_add(qq,a_mul64(U[None,:,a,None],a_slice(nz,(slice(None),slice(None),a,slice(None)))))
 Vt=rate_normal_put(keep,label,'compensation_V',a_matvec(P,qq));Dt=rate_normal_put(keep,label,'compensation_D',normal_pair_sandwich(P,nz,P.swapaxes(-1,-2)))
 Lie=a_dd(np.zeros_like(c['h']))
 for i in range(3):Lie=a_add(Lie,a_mul64(b[:,i,None,None],a_slice(cj['dh'],(slice(None),i+1,slice(None),slice(None)))))
 Lie=a_add(Lie,a_dd(np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])))
 rate_normal_put(keep,label,'Lie_h',Lie)
 made_duc=a_add(a_matvec(q,a_dd(U)),a_matvec(g,a_dd(eta)))
 made_P=a_add(a_prod(duc[:,:,None],U[:,None,:]),a_prod(s['uc'][:,:,None],eta[:,None,:]))
 made_I=normal_pair_sandwich(s['hi'],a_dd(q),s['hi']);made_I=(-made_I[0],-made_I[1])
 nq=[]
 for a in range(4):
  ga=a_slice(jets['Ga'],(slice(None),slice(None),a,slice(None)))
  connection=a_add(normal_pair_right(a_transpose(ga,(0,2,1)),q),normal_pair_left(q,ga))
  nq.append(a_sub(a_slice(lift['dq'],(slice(None),a)),connection))
 made_G=normal_contact_connection(a_dd(s['hi']),a_stack(nq,axis=1),keep,label+'_constructed_test_Gamma')
 gaps=dict(raw_test_duc=a_sub(made_duc,a_dd(duc)),raw_test_projector=a_sub(made_P,a_dd(dP)),raw_test_inverse=a_sub(made_I,a_dd(test['dhi'])),test_Gamma=a_sub(made_G,test['paired']['deltaG']))
 for n,x in gaps.items():rate_normal_put(keep,label,n+'_construction_gap',x)
 for n,x in dict(compensation_V=Vt,compensation_D=Dt,Lie_h=Lie).items():rate_normal_put(keep,label,n,x)
 for n,x in dict(test_projector=dP,compensation_numerator=ez,f=f,df=df,b=b,db=db).items():keep(label+'_'+n,np.asarray(x).copy())
 return dict(lift=lift,test=test,projector=dP,ez=ez,compensation_V=Vt,compensation_D=Dt,Lie_h=Lie,f=f,df=df,b=b,db=db,construction_gaps=gaps,gap_refs=column['gap_refs'])

def rate_normal_test_increment(s,c,jets,feature,chart,cache,keep,label):
 U,z,g,P,beta,N=s['U'],s['z'],s['g'],s['P'],c['beta'],c['N'];p=len(U)
 f,b=cache['f'],cache['b'];lift=cache['lift'];q,eta,zeta=lift['q'],lift['eta'],lift['zeta'];F=feature['paired']
 assert jets['dg'][0].shape==(p,4,4,4) and jets['dg'][1].shape==(p,4,4,4)
 assert np.all(jets['dg'][0][:,1:]==0.) and np.all(jets['dg'][1][:,1:]==0.),'fixed configuration rate branch only'
 dq=a_dd(np.zeros((p,4,4,4)));v=a_mul64(-2*f[:,None],chart['dN'])
 for i in range(3):
  for k in range(3):
   v=a_add(v,a_mul64((2*c['h'][:,i,k]*b[:,k])[:,None],a_slice(chart['dbeta'],(slice(None),slice(None),i))))
   v=a_add(v,a_mul64((2*beta[:,i]*b[:,k])[:,None],a_slice(chart['dh'],(slice(None),slice(None),i,k))))
   rate_normal_put(keep,label,'test_dq00_partial',v)
 for word in (0,1):dq[word][:,:,0,0]=v[word]
 for i in range(3):
  v=a_dd(np.zeros((p,4)))
  for k in range(3):v=a_add(v,a_mul64(b[:,k,None],a_slice(chart['dh'],(slice(None),slice(None),i,k))))
  for word in (0,1):dq[word][:,:,0,i+1]=dq[word][:,:,i+1,0]=v[word]
 rate_normal_put(keep,label,'dq',dq)
 du0=a_slice(jets['du'],(slice(None),slice(None),0));de0=a_add(a_mul64((-f/N)[:,None],du0),a_mul64((U[:,0]*f/N**2)[:,None],chart['dN']))
 de=a_dd(np.zeros_like(s['du']))
 for word in (0,1):de[word][:,:,0]=de0[word]
 for i in range(3):
  v=a_sub(a_mul64(-b[:,i,None],du0),a_mul64(eta[:,0,None],a_slice(chart['dbeta'],(slice(None),slice(None),i))))
  v=a_sub(v,a_mul64(beta[:,i,None],de0))
  for word in (0,1):de[word][:,:,i+1]=v[word]
 rate_normal_put(keep,label,'deta',de)
 dez=a_dd(np.zeros((32,p,4)))
 for a in range(4):
  dez=a_add(dez,a_mul64(z[:,:,a,None],a_slice(de,(slice(None),slice(None),a))))
  dez=a_add(dez,a_mul64(eta[None,:,a,None],a_slice(jets['dz'],(slice(None),slice(None),slice(None),a))))
  rate_normal_put(keep,label,'compensation_numerator_jet_partial',dez)
 zt=a_add(a_div64((-dez[0],-dez[1]),U[None,:,0,None],keep,label+'_dzeta_division'),a_mul64(cache['ez'][:,:,None]/U[None,:,0,None]**2,(du0[0][None],du0[1][None])))
 dzeta=a_dd(np.zeros_like(s['dz']))
 for word in (0,1):dzeta[word][:,:,:,0]=zt[word]
 rate_normal_put(keep,label,'dzeta',dzeta)
 nq=[]
 for a in range(4):
  ga=a_slice(jets['Ga'],(slice(None),slice(None),a,slice(None)))
  connection=a_add(normal_pair_right(a_transpose(ga,(0,2,1)),q),normal_pair_left(q,ga))
  nq.append(a_sub(a_slice(dq,(slice(None),a)),connection))
 G=normal_pair_connection_from_jet(s['hi'],a_stack(nq,axis=1),keep,label+'_test_Gamma')
 nu=de;nz=a_dd(np.zeros_like(s['dz']));comp=dzeta
 for l in range(4):
  nu=a_add(nu,a_mul64(U[:,l,None,None],a_transpose(a_slice(G,(slice(None),slice(None),slice(None),l)),(0,2,1))))
  nu=a_add(nu,a_mul64(eta[:,l,None,None],a_transpose(a_slice(jets['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1))))
  nz=a_sub(nz,a_mul64(z[:,:,l,None,None],a_slice(G,(slice(None),l,slice(None),slice(None)))))
  comp=a_sub(comp,a_mul64(zeta[:,:,l,None,None],a_slice(jets['Ga'],(slice(None),l,slice(None),slice(None)))))
  for n,x in dict(test_nu_partial=nu,test_nz_partial=nz,compensation_covariant_jet_partial=comp).items():rate_normal_put(keep,label,n,x)
 qq=a_dd(np.zeros_like(F['q'][0]));acc=a_dd(np.zeros_like(F['a'][0]));cq=a_dd(np.zeros_like(F['q'][0]))
 for a in range(4):
  qq=a_add(qq,a_add(a_mul64(eta[None,:,a,None],a_slice(F['nz'],(slice(None),slice(None),a,slice(None)))),a_mul64(U[None,:,a,None],a_slice(nz,(slice(None),slice(None),a,slice(None))))))
  acc=a_add(acc,a_add(a_mul64(eta[:,a,None],a_slice(F['nu'],(slice(None),a,slice(None)))),a_mul64(U[:,a,None],a_slice(nu,(slice(None),a,slice(None))))))
  cq=a_add(cq,a_mul64(U[None,:,a,None],a_slice(comp,(slice(None),slice(None),a,slice(None)))))
 V=a_add(a_matvec(cache['projector'],F['q']),a_matvec(P,qq))
 D=a_add(normal_pair_sandwich(cache['projector'],F['nz'],P.swapaxes(-1,-2)),normal_pair_sandwich(P,F['nz'],cache['projector'].swapaxes(-1,-2)))
 D=a_add(D,normal_pair_sandwich(P,nz,P.swapaxes(-1,-2)))
 lower=a_add(normal_pair_right(F['nu'],q),normal_pair_right(nu,g));FF=a_sub(lower,a_transpose(lower,(0,2,1)))
 out=dict(dV=V,dD=D,dF=FF,da=acc,compensation_V=a_matvec(P,cq),compensation_D=normal_pair_sandwich(P,comp,P.swapaxes(-1,-2)),dq=dq,deta=de,dzeta=dzeta,deltaG=G)
 for n,x in out.items():rate_normal_put(keep,label,n,x)
 return out

def rate_normal_direction(s,c,current_feature,current_moments,rate_jets,rate_feature,rate_moments,rate_chart,column,cache,keep,label):
 F=current_feature['paired'];F1=rate_feature['paired'];T=cache['test']['paired']
 T1=rate_normal_test_increment(s,c,rate_jets,rate_feature,rate_chart,cache,keep,label+'_test_increment')
 dot=normal_action_dot;cross=rate_normal_cross;hi=s['hi'];It=cache['test']['dhi'];lm=cache['test']['lm'];om=s['omega'][:,None]**2
 V21=rate_normal_put(keep,label,'delta_V_squared',cross(F['V_raised'],F['V'],F1['V_raised'],F1['V'],(2,)))
 D21=rate_normal_put(keep,label,'delta_D_squared',cross(F['D_raised'],F['D'],F1['D_raised'],F1['D'],(2,3)));FF21=rate_normal_put(keep,label,'delta_F_squared',cross(F['Fup'],F['F'],F1['Fup'],F1['F'],(1,2)))
 tV21=rate_normal_put(keep,label,'mixed_V_squared',a_add(cross(a_matvec(It,F['V']),F['V'],a_matvec(It,F1['V']),F1['V'],(2,)),a_mul64(2.,cross(F['V_raised'],T['dV'],F1['V_raised'],T1['dV'],(2,)))))
 tD21=rate_normal_put(keep,label,'mixed_D_squared_partial',a_mul64(2.,cross(F['D_raised'],T['dD'],F1['D_raised'],T1['dD'],(2,3))))
 tF21=rate_normal_put(keep,label,'mixed_F_squared_partial',a_mul64(2.,cross(F['Fup'],T['dF'],F1['Fup'],T1['dF'],(1,2))))
 for A,B0 in ((It,hi),(hi,It)):
  tD21=a_add(tD21,cross(normal_pair_sandwich(A,F['D'],B0),F['D'],normal_pair_sandwich(A,F1['D'],B0),F1['D'],(2,3)))
  tF21=a_add(tF21,cross(normal_pair_sandwich(A,F['F'],B0),F['F'],normal_pair_sandwich(A,F1['F'],B0),F1['F'],(1,2)))
  rate_normal_put(keep,label,'mixed_D_squared_partial',tD21);rate_normal_put(keep,label,'mixed_F_squared_partial',tF21)
 az1=normal_action_reduce(a_mul64(s['z'],(F1['a'][0][None],F1['a'][1][None])),(2,));taz1=normal_action_reduce(a_mul64(s['z'],(T1['da'][0][None],T1['da'][1][None])),(2,))
 zero=a_dd(np.zeros_like(V21[0]));modal_primal=a_stack((a_div64(V21,2*om,keep,label+'_primal_frequency'),zero,zero,a_mul64(-ELL**2/2,D21),az1),axis=-1)
 modal_test=a_stack((a_div64(tV21,2*om,keep,label+'_test_frequency'),zero,zero,a_mul64(-ELL**2/2,tD21),taz1),axis=-1)
 modal=[normal_pair_sum(a_mul64(s['w'][:,None,None],x),0) for x in (modal_primal,modal_test)];zp=a_dd(np.zeros(len(s['U'])))
 primal=a_stack([a_mul64(-ALPHA/4,FF21),zp]+[a_slice(modal[0],(slice(None),i)) for i in range(5)],axis=-1)
 variation=a_stack([a_mul64(-ALPHA/4,tF21),zp]+[a_slice(modal[1],(slice(None),i)) for i in range(5)],axis=-1)
 native=a_add(variation,a_mul64(lm[:,None],primal));rate_normal_put(keep,label,'native_terms',native)
 zk=a_div64(cross(F['V_raised'],cache['compensation_V'],F1['V_raised'],T1['compensation_V'],(2,)),om,keep,label+'_z0_frequency')
 zg=a_mul64(-ELL**2,cross(F['D_raised'],cache['compensation_D'],F1['D_raised'],T1['compensation_D'],(2,3)))
 za=normal_action_reduce(a_mul64(cache['lift']['zeta'],(F1['a'][0][None],F1['a'][1][None])),(2,))
 zm=normal_pair_sum(a_mul64(s['w'][:,None,None],a_stack((zk,zero,zero,zg,za),axis=-1)),0)
 mode=a_stack([zp,zp]+[a_slice(zm,(slice(None),i)) for i in range(5)],axis=-1);rate_normal_put(keep,label,'mode_terms',mode)
 Ku1=normal_pair_sandwich(c['ih'],rate_moments['K'],c['ih'])
 kinetic=a_sub(a_mul64(2.,a_mul(current_moments['Ktrace'],rate_moments['Ktrace'])),cross(current_moments['K'],column['K_raised'],rate_moments['K'],Ku1,(1,2)))
 kinetic=a_div64(a_mul64(cache['f']*c['sqrt_h'],kinetic),2*C,keep,label+'_EH_kinetic')
 shift=a_mul64(-1.,dot(rate_moments['metric_EH_tensor'],cache['Lie_h'],(1,2)))
 EH=a_stack((zp,kinetic,shift),axis=-1);phase=a_stack((zp,zp),axis=-1)
 for n,x in dict(EH_terms=EH,absolute_phase_terms=phase).items():rate_normal_put(keep,label,n,x)
 components=a_stack((a_mul64(c['dens'],normal_pair_sum(native,1)),a_mul64(c['dens'],normal_pair_sum(mode,1)),zp,normal_pair_sum(EH,1)),axis=-1)
 coefficient=normal_pair_sum(components,1)
 for n,x in dict(component_densities=components,coefficient=coefficient).items():rate_normal_put(keep,label,n,x)
 return dict(native_metric_terms=native,mode_compensation_terms=mode,absolute_phase_terms=phase,EH_terms=EH,component_densities=components,coefficient=coefficient,construction_gaps=cache['construction_gaps'],gap_refs=cache['gap_refs'],physical_adoption=False,exact_generator_equivalence=False)

def rate_normal_CMC_contact(s,c,metric_value,rate_moments,keep,label):
 # This identity uses genuine local physical hdot values, not coefficient slots.
 assert metric_value[0].shape==metric_value[1].shape==(len(c['N']),6)
 entries=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2));trace=a_dd(np.zeros(len(c['N'])))
 for a,(i,j) in enumerate(entries):
  entry=a_slice(metric_value,(slice(None),a));trace=a_add(trace,a_mul64(c['ih'][:,i,j],entry))
  if i!=j:trace=a_add(trace,a_mul64(c['ih'][:,j,i],entry))
 gamma=a_mul64(c['sqrt_h'],a_mul64(c['N'],a_mul64(-.5*s['hi'][:,0,0],trace)))
 rate_normal_put(keep,label,'Gamma_density',gamma)
 ADM=rate_normal_put(keep,label,'ADM_density',a_div64(a_mul64(c['sqrt_h'],trace),2*c['N'],keep,label+'_ADM_division'))
 actual=rate_normal_put(keep,label,'affine81_density',a_mul64(c['sqrt_h'],rate_moments['Ktrace']));gap=a_sub(gamma,actual)
 for n,x in dict(Gamma_density=gamma,ADM_density=ADM,Gamma_minus_ADM=a_sub(gamma,ADM),Gamma_chain_minus_affine81=gap).items():rate_normal_put(keep,label,n,x)
 return dict(Gamma_density=gamma,ADM_density=ADM,Gamma_chain_minus_affine81=gap,phase_direct_contact_zero=True,Hbar_fixed=True,physical_adoption=False)
