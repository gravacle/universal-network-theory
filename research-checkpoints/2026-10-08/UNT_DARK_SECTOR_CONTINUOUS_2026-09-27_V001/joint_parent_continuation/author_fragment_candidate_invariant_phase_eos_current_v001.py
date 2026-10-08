"""HELD candidate paired invariant EOS/literal current/Hessian/product-rule JVP.
Globals np,math,P and the reviewed fs_* dual/fy_* paired helpers. No invocation.
Every candidate/direction input is a pair; no binary64 word collapse is accepted.
Elementary log constructions retain high/low terms and their ratio-readout defect;
their transcendental accuracy and the physical candidate remain caller admissions.
The current literal projector is supplied, never replaced by a unit reduction.
"""
CANDIDATE_PHASE_AUTHOR_DRAFT=True
CANDIDATE_PHASE_AUTHORING_IN_PROGRESS=False


def candidate_phase_registered_constants(fixed):
 assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 C=1.98;cp=299792458.;eta=fixed['Hunit']/cp;eps=fixed['eps']
 norm=1/eps-math.log1p(1/eps);X0=100*eta;fac=2*eta*eta/C;Abar=1.5*fixed['OA']/fixed['rG'];A0=fac*Abar
 assert all(math.isfinite(x) and x>0 for x in (eta,eps,norm,X0,A0,fixed['rG']))
 return dict(eps=eps,norm=norm,X0=X0,A0=A0,C=C,eta=eta,synthetic_control=False,
             Hunit=fixed['Hunit'],OA=fixed['OA'],rG=fixed['rG'],relative_phase_coefficient=1.,
             physical_constants_selected_or_fitted=False)


def candidate_phase_log1p_dual(a,keep,label):
 total=fs_keep(label+'_one_plus_argument',fs_add(a,fs_dual(P.a_dd(np.ones_like(a[0][0])))),keep)
 yh,yl=total[0];assert np.all(yh-abs(yl)>0)
 ratio=yl/yh;keep(label+'_elementary_low_over_high',np.asarray(ratio).copy())
 fy_keep(label+'_ratio_readout_product_defect',P.a_sub(P.a_prod(yh,ratio),P.a_dd(yl)),keep)
 high=np.log(yh);keep(label+'_elementary_log_high',np.asarray(high).copy())
 low=np.log1p(ratio);keep(label+'_elementary_log1p_low',np.asarray(low).copy())
 assert np.all(np.isfinite(high)) and np.all(np.isfinite(low))
 value=fy_keep(label+'_paired_log',P.a_add(P.a_dd(high),P.a_dd(low)),keep)
 delta=fy_div(a[1],total[0],keep,label+'_analytic_direction')
 return value,delta


def candidate_invariant_phase_eos_current(s,c,direction,constants,keep,label):
 """s: paired hi/P/phi/U/uc; c: paired N/mu/ih/u. Directions have the same keys.
 H is d(dens*literal_J^0)/d(phi_0) at fixed configuration, not reduced ADM H.
 Its JVP includes inverse/projector/clock/measure contacts supplied by direction.
 """
 p=s['phi'][0].shape[0];put=lambda n,x:fs_keep(label+'_'+n,x,keep)
 for values,shapes in ((s,dict(hi=(p,4,4),P=(p,4,4),phi=(p,4),U=(p,4),uc=(p,4))),
                      (c,dict(N=(p,),mu=(p,),ih=(p,3,3),u=(p,3)))):
  for n,shape in shapes.items():
   assert n in direction
   for pair in (values[n],direction[n]):
    assert isinstance(pair,tuple) and len(pair)==2
    assert all(w.shape==shape and w.dtype==np.dtype('float64') and np.all(np.isfinite(w)) for w in pair)
   put('supplied_'+n,fs_dual(values[n],direction[n]))
 for n,values in (('hi',s),('ih',c)):
  assert all(np.array_equal(w,w.swapaxes(-1,-2)) for pair in (values[n],direction[n]) for w in pair),'Symmetric inverse model required'
 hi=fs_dual(s['hi'],direction['hi']);projector=fs_dual(s['P'],direction['P']);phi=fs_dual(s['phi'],direction['phi'])
 U=fs_dual(s['U'],direction['U']);uc=fs_dual(s['uc'],direction['uc'])
 N=fs_dual(c['N'],direction['N']);mu=fs_dual(c['mu'],direction['mu']);I=fs_dual(c['ih'],direction['ih']);uvec=fs_dual(c['u'],direction['u'])
 assert np.all(N[0][0]-abs(N[0][1])>0) and np.all(mu[0][0]-abs(mu[0][1])>0)
 eps,norm,X0,A0=(float(constants[n]) for n in ('eps','norm','X0','A0'))
 assert type(constants['synthetic_control']) is bool and all(math.isfinite(x) and x>0 for x in (eps,norm,X0,A0))
 assert norm==1/eps-math.log1p(1/eps) and constants['relative_phase_coefficient']==1.
 if not constants['synthetic_control']:assert eps==1e-5 and constants['C']==1.98
 one=fs_dual(P.a_dd(np.ones(p)));constant=lambda x:fs_dual(P.a_dd(np.full(p,x)))
 x0=constant(X0);normalization=constant(norm);epsilon=constant(eps)
 raised=put('raised_phi',fs_mv(hi,phi));invariant=put('phi_inverse_phi',fs_dot(phi,raised))
 X2=put('invariant_X_squared',fs_neg(invariant));X=put('invariant_X',fs_sqrt(X2,keep,label+'_clock_root'))
 q=put('invariant_q',fs_div(X,x0,keep,label+'_q'));argument=put('clock_pressure_u',fs_sub(fs_mul(q,q),one))
 lower=argument[0][0]-abs(argument[0][1]);upper=eps-argument[0][0]-abs(argument[0][1])
 keep(label+'_clock_u_lower',np.asarray(lower).copy());keep(label+'_eps_minus_clock_u_lower',np.asarray(upper).copy())
 assert np.all(lower>0) and np.all(upper>0),'Same strict invariant EOS domain 0<u<eps'
 d=put('distance_to_EOS_boundary',fs_sub(epsilon,argument));ss=put('EOS_s',fs_div(argument,d,keep,label+'_s'))
 logarithm=put('EOS_log1p_s',candidate_phase_log1p_dual(ss,keep,label+'_log1p_s'))
 fraction=put('EOS_s_over_one_plus_s',fs_div(ss,fs_add(one,ss),keep,label+'_s_fraction'))
 pressure=put('pressure',fs_scale(A0,fs_sub(fs_div(fs_sub(logarithm,fraction),normalization,keep,label+'_pressure_norm'),one)))
 epnorm=fs_mul(epsilon,normalization);q2=fs_mul(q,q);d2=fs_mul(d,d);d3=fs_mul(d2,d)
 PX=put('PX',fs_div(fs_scale(2*A0,fs_div(fs_mul(q,ss),epnorm,keep,label+'_PX_dimensionless')),x0,keep,label+'_PX_units'))
 first=put('PXX_first_term',fs_div(fs_scale(2.,ss),epnorm,keep,label+'_PXX_first'))
 second=put('PXX_second_term',fs_div(fs_scale(4.,q2),fs_mul(normalization,d2),keep,label+'_PXX_second'))
 PXX=put('PXX',fs_div(fs_scale(A0,fs_add(first,second)),fs_mul(x0,x0),keep,label+'_PXX_units'))
 # PXXX is needed for delta(PXX); no PXXXX or delta(PXXX) is asserted.
 t1=fy_div(P.a_mul64(12.,q[0]),P.a_mul(normalization[0],d2[0]),keep,label+'_PXXX_first');fy_keep(label+'_PXXX_first_term',t1,keep)
 t2=fy_div(P.a_mul64(16.,P.a_mul(q2[0],q[0])),P.a_mul(normalization[0],d3[0]),keep,label+'_PXXX_second');fy_keep(label+'_PXXX_second_term',t2,keep)
 PXXX=fy_div(P.a_mul64(A0,P.a_add(t1,t2)),P.a_mul(P.a_mul(x0[0],x0[0]),x0[0]),keep,label+'_PXXX_units');fy_keep(label+'_PXXX',PXXX,keep)
 for n,actual,expected in (('P',pressure[1],P.a_mul(PX[0],X[1])),('PX',PX[1],P.a_mul(PXX[0],X[1])),('PXX',PXX[1],P.a_mul(PXXX,X[1]))):
  fy_keep(label+'_'+n+'_analytic_chain_actual',actual,keep);fy_keep(label+'_'+n+'_analytic_chain_expected',expected,keep);fy_keep(label+'_'+n+'_analytic_chain_gap',P.a_sub(actual,expected),keep)
 clock=put('clock_velocity',fs_div(raised,fs_expand(X,(Ellipsis,None)),keep,label+'_clock_normalization'))
 pressure_J=put('pressure_current',fs_neg(fs_mul(fs_expand(PX,(Ellipsis,None)),clock)))
 r=put('literal_projected_phase',fs_mv(projector,phi));hi_r=put('raised_relative_phase',fs_mv(hi,r))
 relative=put('literal_relative_current_negative',fs_mv(fs_transpose(projector,(0,2,1)),hi_r))
 J=put('literal_current',fs_sub(pressure_J,relative));registered_J=put('registered_current',fs_sub(pressure_J,hi_r))
 density=put('candidate_density',fs_mul(N,mu));momentum=put('literal_canonical_density',fs_mul(density,fs_slice(J,(slice(None),0))))
 registered_p=put('registered_canonical_density',fs_mul(density,fs_slice(registered_J,(slice(None),0))))
 n0=fs_slice(clock,(slice(None),0));n02=put('clock_time_square',fs_mul(n0,n0))
 pressure_H=put('pressure_temporal_H',fs_sub(fs_mul(PXX,n02),fs_mul(fs_div(PX,X,keep,label+'_PX_over_X'),fs_add(fs_slice(hi,(slice(None),0,0)),n02))))
 p0=fs_slice(projector,(slice(None),slice(None),0));hp0=put('inverse_projector_time_column',fs_mv(hi,p0));A00=put('literal_relative_temporal_coefficient',fs_dot(p0,hp0))
 H=put('literal_temporal_H',fs_mul(density,fs_sub(pressure_H,A00)))
 registered_H=put('registered_temporal_H',fs_mul(density,fs_sub(pressure_H,fs_slice(hp0,(slice(None),0)))))
 norm_b=put('spatial_native_norm_b',fs_dot(uvec,fs_mv(I,uvec)));reduced_H=put('reduced_ADM_H',fs_div(fs_mul(mu,fs_sub(PXX,norm_b)),N,keep,label+'_reduced_H'))
 comparisons={}
 for n,a,b in (('current_gap',J,registered_J),('density_gap',momentum,registered_p),('hessian_gap',H,registered_H),('reduced_gap',H,reduced_H)):
  comparisons[n]=put(n,fs_sub(a,b))
 put('clock_square_construction_gap',fs_add(fs_mul(X,X),invariant))
 constructed_P=fs_add(fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4)))),fs_mul(fs_expand(uc,(Ellipsis,slice(None),None)),fs_expand(U,(Ellipsis,None,slice(None)))))
 put('supplied_minus_constructed_projector_gap',fs_sub(projector,constructed_P))
 absolute=lambda x:abs(x[0])+abs(x[1])
 ehi,ephi,eU,euc=map(absolute,(s['hi'],s['phi'],s['U'],s['uc']));eP=np.maximum(np.eye(4)[None]+euc[:,:,None]*eU[:,None,:],absolute(s['P']))
 ev=np.einsum('pab,pb->pa',ehi,ephi);eA=np.einsum('pai,pab,pbj->pij',eP,ehi,eP)
 XL=X[0][0]-abs(X[0][1]);assert np.all(XL>0)
 px,pXX=absolute(PX[0]),absolute(PXX[0]);edens=absolute(density[0])
 eJ=px[:,None]/XL[:,None]*ev+np.einsum('pab,pb->pa',eA,ephi)
 eH=edens*((pXX/XL**2+px/XL**3)*ev[:,0]**2+px/XL*ehi[:,0,0]+eA[:,0,0])
 assert np.all(np.isfinite(eJ)) and np.all(np.isfinite(eH))
 keep(label+'_current_operation_envelope',np.asarray(eJ).copy());keep(label+'_H_operation_envelope',np.asarray(eH).copy())
 keep(label+'_H_pair_lower',np.asarray(H[0][0]-abs(H[0][1])).copy())
 values=dict(X2=X2,X=X,q=q,u=argument,s=ss,pressure=pressure,PX=PX,PXX=PXX,J=J,registered_J=registered_J,p=momentum,registered_p=registered_p,H=H,registered_H=registered_H,reduced_H=reduced_H,density=density,**comparisons)
 return dict(value={n:x[0] for n,x in values.items()},delta={n:x[1] for n,x in values.items()},PXXX=PXXX,
             constants=dict(constants),current_operation_envelope=eJ,H_operation_envelope=eH,
             candidate_pressure_recomputed_from_invariant=True,owned_pressure_u_used=False,
             paired_input_collapsed=False,elementary_log_accuracy_admitted=False,
             fixed_phase_charge_restored=False,finite_candidate_physically_admitted=False)
