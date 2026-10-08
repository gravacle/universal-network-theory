"""HELD conditional unsigned NEW configuration-normal product-rule majorant.
Inputs are completed SAME160/NEW253 normal inventories and cached updated195
phase test operands, never a signed final response used as its own envelope.
Globals np,P and the seven reviewed124 outward mp_* primitives. The boundary
is the actual paired feature/test-feature/Gamma3 and EOS chart-stage operands;
upstream construction errors and a uniform DD Jacobian remain unqualified.
"""
CONFIGURATION_NORMAL_UNSIGNED_AUTHOR_DRAFT=True
CONFIGURATION_NORMAL_UNSIGNED_AUTHORING_IN_PROGRESS=False
CONFIGURATION_NORMAL_UNSIGNED_PINS={
 'author_fragment_finite_candidate_native_EH_normal_v004.py':'27185f96e5ac8a00c8b1077ccedc9f2ced9399ed8379bdc16b2510926ae640a1',
 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py':'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94'}


def candidate_configuration_normal_unsigned(candidate,contact,normal,curvature,phase,eos,phase_test,ordinary_roots,mean_labels,f,df,b,db,keep,label):
 assert not CONFIGURATION_NORMAL_UNSIGNED_AUTHOR_DRAFT and not CONFIGURATION_NORMAL_UNSIGNED_AUTHORING_IN_PROGRESS
 s,c=candidate['s'],candidate['c'];S=contact['state'];V=normal['uncancelled_inventory'];p=len(c['N']);counter=0
 assert normal['relative_phase_included'] is False
 for a,shape in ((f,(p,)),(df,(p,4)),(b,(p,3)),(db,(p,4,3))):assert a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a))
 def tag(n):
  nonlocal counter
  counter+=1;return label+'_%05d_'%counter+n
 def mag(pair,n):
  keep(tag(n+'_both_words'),np.stack(pair).copy());assert isinstance(pair,tuple) and len(pair)==2
  assert all(a.dtype==np.float64 and np.all(np.isfinite(a)) for a in pair)
  return mp_add(abs(pair[0]),abs(pair[1]),keep,tag(n+'_magnitude'))
 add=lambda a,b:mp_add(a,b,keep,tag('add'))
 mul=lambda a,b:mp_mul(a,b,keep,tag('mul'))
 div=lambda a,b:mp_div(a,b,keep,tag('div'))
 sum_=lambda a,k:mp_sum(a,k,keep,tag('sum'))
 mm=lambda a,b:mp_mm(a,b,keep,tag('mm'))
 mv=lambda a,b:mp_mv(a,b,keep,tag('mv'))
 def dual(x,n):return mag(x[0],n+'_value'),mag(x[1],n+'_direction')
 def plus(a,b):return add(a[0],b[0]),add(a[1],b[1])
 def times(a,b):return mul(a[0],b[0]),add(mul(a[1],b[0]),mul(a[0],b[1]))
 def scale(k,a):return mul(abs(k),a[0]),mul(abs(k),a[1])
 def reduce(a,k):return sum_(a[0],k),sum_(a[1],k)
 def dot(a,b):return reduce(times(a,b),-1)
 def contract(a,b):return reduce(reduce(times(a,b),-1),-1)
 def lower(pair,n):
  keep(tag(n+'_denominator_both_words'),np.stack(pair).copy());a=np.nextafter(pair[0]-abs(pair[1]),-np.inf)
  keep(tag(n+'_positive_denominator_lower'),a.copy());assert np.all(np.isfinite(a)) and np.all(a>0);return a
 F={n:dual(x,'native_feature_'+n) for n,x in V['F'].items()}
 T={n:dual(V[n],'native_test_feature_'+n) for n in ('Vt','Dt','Ft','Vut','Dut','Fut','at','z2','z2_test')}
 Z=dual(S['z'],'native_z');Zt=dual(normal['tests']['zeta'],'native_z_test')
 v2=dot(F['V_raised'],F['V']);v2t=plus(dot(T['Vut'],F['V']),dot(F['V_raised'],T['Vt']))
 d2=contract(F['D_raised'],F['D']);d2t=plus(contract(T['Dut'],F['D']),contract(F['D_raised'],T['Dt']))
 f2=contract(F['Fup'],F['F']);f2t=plus(contract(T['Fut'],F['F']),contract(F['Fup'],T['Ft']))
 A=tuple(a[None] for a in F['a']);At=tuple(a[None] for a in T['at'])
 az=dot(Z,A);azt=plus(dot(Zt,A),dot(Z,At));z2=T['z2'];z2t=T['z2_test']
 om=s['omega'][:,None]**2;kj=(P.B*P.GC)**2*s['xi'][:,None]**4
 for n,a in (('source_rounded_omega_squared',om),('source_rounded_quartic_denominator',kj)):
  keep(tag(n),a.copy());assert np.all(np.isfinite(a)) and np.all(a>0)
 divided=lambda a,k:(div(a[0],abs(k)),div(a[1],abs(k)))
 modes=(divided(v2,2*om),scale(.5,z2),divided(times(z2,z2),4*kj),scale(P.ELL**2/2,d2),az)
 tests=(divided(v2t,2*om),scale(.5,z2t),divided(times(z2,z2t),2*kj),scale(P.ELL**2/2,d2t),azt)
 primal=scale(P.ALPHA/4,f2);tested=scale(P.ALPHA/4,f2t)
 for a,t in zip(modes,tests):
  primal=plus(primal,reduce(scale(s['w'][:,None],a),0));tested=plus(tested,reduce(scale(s['w'][:,None],t),0))
 dens=dual(S['dens'],'native_measure');mu=dual(S['mu'],'spatial_measure')
 for n in ('N','beta'):assert all(np.all(w==0) for w in S[n][1])
 lm=(div(abs(f),lower(S['N'][0],'lapse_measure')),np.zeros(p))
 native=times(dens,plus(tested,times(lm,primal)))
 K,Kup,Kt,Ktu,tau,taut=(dual(V[n],'EH_'+n) for n in ('K','Kup','Kt','Ktu','tau','tau_test'))
 kin=plus(contract(K,Kup),times(tau,tau))
 kint=plus(plus(contract(Kt,Kup),contract(K,Ktu)),scale(2.,times(tau,taut)))
 ft=(abs(f),np.zeros(p));EHkin=div(plus(times(times(ft,mu),kin),times(dens,kint))[1],abs(2*P.C))
 I=dual(S['ih'],'intrinsic_inverse');C3=dual(curvature['C3'],'intrinsic_connection_difference')
 q=(np.zeros(p),np.zeros(p));vv=(np.zeros((p,3)),np.zeros((p,3)))
 for i in range(3):
  for j in range(3):
   for k in range(3):
    for l in range(3):
     for a,bc in (((k,i,l),(l,j,k)),((k,i,j),(l,k,l))):
      aa=tuple(x[:,a[0],a[1],a[2]] for x in C3);bb=tuple(x[:,bc[0],bc[1],bc[2]] for x in C3)
      q=plus(q,times(tuple(x[:,i,j] for x in I),times(aa,bb)))
    for ii,jj,a in ((i,j,(k,i,j)),(i,k,(j,i,j))):
     term=times(tuple(x[:,ii,jj] for x in I),tuple(x[:,a[0],a[1],a[2]] for x in C3))
     for word in (0,1):vv[word][:,k]=add(vv[word][:,k],term[word])
  for word in (0,1):keep(tag('partial_intrinsic_curvature_'+str(word)),np.stack((q[word],vv[word][:,0],vv[word][:,1],vv[word][:,2]),axis=-1).copy())
 eQ=times(mu,q)[1];eV=times(tuple(x[:,None] for x in mu),vv)[1]
 EHcurv=div(add(mul(abs(f),eQ),sum_(mul(abs(df[:,1:]),eV),1)),abs(2*P.C))
 eNative=native[1];eEH=add(EHkin,EHcurv);ePhase=np.zeros(p);eOrdinary=np.zeros(p)
 if phase_test is not None:
  assert np.all(df==0) and np.all(db==0) and phase is not None and eos['old_temporal_direction_reused'] is False
  a=phase_test;ps,pc=phase['s'],phase['c'];D={**contact['d'],**contact['dc']};D['mu']=contact['dc']['sqrt_h']
  M=lambda name:mag(a[name],'cached_phase_test_'+name)
  phi=mag(ps['phi'],'updated_phi');hi=mag(ps['hi'],'updated_phase_inverse');dp={n:mag(D[n],'NEW_phase_direction_'+n) for n in ('hi','P','U','uc','g','h','mu')}
  U=mag(ps['U'],'updated_phase_U');uc=mag(ps['uc'],'updated_phase_uc');g=mag(ps['g'],'updated_phase_g')
  assert all(np.all(w==0) for n in ('N','beta','phi') for w in D[n])
  ehb=mv(dp['h'],abs(b));eq=np.zeros((p,4,4));eq[:,0,0]=mul(2.,sum_(mul(abs(c['beta']),ehb),1));eq[:,0,1:]=eq[:,1:,0]=ehb
  qmag=M('q');eit=add(add(mm(mm(dp['hi'],qmag),hi),mm(mm(hi,eq),hi)),mm(mm(hi,qmag),dp['hi']))
  eeta0=div(mul(dp['U'][:,0],abs(f)),lower(pc['N'],'phase_test_lapse'))
  eeta=np.concatenate((eeta0[:,None],add(mul(dp['U'][:,0,None],abs(b)),mul(abs(c['beta']),eeta0[:,None]))),axis=1)
  eta=M('eta');euct=add(add(mv(eq,U),mv(qmag,dp['U'])),add(mv(dp['g'],eta),mv(g,eeta)))
  outer=lambda x,y:mul(x[..., :,None],y[...,None,:])
  ept=add(add(outer(euct,U),outer(M('uct'),dp['U'])),add(outer(dp['uc'],eta),outer(uc,eeta)))
  r=M('r');rt=M('rt');er=mv(dp['P'],phi);ert=mv(ept,phi);hir=mv(hi,r);ehir=add(mv(dp['hi'],r),mv(hi,er))
  er2=add(sum_(mul(er,hir),1),sum_(mul(r,ehir),1));r2=sum_(mul(r,hir),1)
  eX=mag(eos['delta']['X'],'NEW_cached_stage_dX');ePX=mag(eos['delta']['PX'],'NEW_cached_stage_dPX');ePressure=mag(eos['delta']['pressure'],'NEW_cached_stage_dPressure')
  eXtest=div(add(mul(.5,sum_(mul(phi,mv(eit,phi)),1)),mul(M('Xtest'),eX)),lower(eos['value']['X'],'phase_test_X'))
  PX=mag(eos['value']['PX'],'updated_PX');pressure=mag(eos['value']['pressure'],'updated_pressure');lmphase=M('lm')
  baseabs=add(mul(PX,M('Xtest')),mul(pressure,lmphase));dabs=add(add(mul(ePX,M('Xtest')),mul(PX,eXtest)),mul(ePressure,lmphase))
  itr=mv(M('It'),r);eitr=add(mv(eit,r),mv(M('It'),er));hirt=mv(hi,rt);ehirt=add(mv(dp['hi'],rt),mv(hi,ert))
  baserel=add(add(mul(.5,sum_(mul(r,itr),1)),sum_(mul(r,hirt),1)),mul(.5,mul(r2,lmphase)))
  drel=add(add(mul(.5,add(sum_(mul(er,itr),1),sum_(mul(r,eitr),1))),add(sum_(mul(er,hirt),1),sum_(mul(r,ehirt),1))),mul(.5,mul(er2,lmphase)))
  edensity=mul(mag(pc['N'],'fixed_phase_N'),dp['mu']);ePhase=add(mul(edensity,add(baseabs,baserel)),mul(M('density'),add(dabs,drel)))
 if ordinary_roots is not None:
  assert phase_test is not None and mean_labels['existing_once_counted_branch_registered'] is True
  dI=mag(contact['dc']['ih'],'NEW_ordinary_inverse_direction');cov=mag(mean_labels['galaxy_specific_covector'],'fixed_mean_covector')
  eRoot=div(sum_(mul(cov,mv(dI,cov)),1),mul(2.,lower(ordinary_roots['galaxy_gamma'],'ordinary_galaxy_gamma')))
  eEnergy=mul(mag(mean_labels['galaxy_mass_weight'],'fixed_mean_mass'),eRoot);rays=mag(mean_labels['radiation_covectors'],'fixed_radiation_covectors');weights=mag(mean_labels['radiation_weights'],'fixed_radiation_weights')
  for j in range(rays.shape[0]):
   energy=tuple(w[j] for w in ordinary_roots['radiation_energy']);ej=div(sum_(mul(rays[j],mv(dI,rays[j])),1),mul(2.,lower(energy,'ordinary_radiation_energy_%d'%j)))
   eEnergy=add(eEnergy,mul(weights[j],ej))
  eOrdinary=mul(abs(f),eEnergy)
 total=add(add(eNative,eEH),add(ePhase,eOrdinary))
 for n,a in (('native',eNative),('EH_kinetic',EHkin),('EH_curvature',EHcurv),('phase',ePhase),('ordinary',eOrdinary),('total_normal',total)):
  keep(label+'_completed_source_unsigned_'+n,a.copy());assert a.shape==(p,) and np.all(np.isfinite(a)) and np.all(a>=0)
 return dict(normal=total,components=dict(native=eNative,EH_kinetic=EHkin,EH_curvature=EHcurv,phase=ePhase,ordinary=eOrdinary),source_terms_before_output_cancellation=True,signed_response_magnitude_used_as_bound=False,conditional_actual_test_feature_and_EOS_stage_boundary=True,upstream_EFT_error_bound_qualified=False,source_input_association_or_uniform_Jacobian_qualified=False,physical_adoption=False)
