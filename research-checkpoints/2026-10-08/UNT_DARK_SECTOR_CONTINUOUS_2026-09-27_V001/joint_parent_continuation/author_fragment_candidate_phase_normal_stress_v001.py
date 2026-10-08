"""Held literal absolute+relative phase normal coefficient and full shared JVP.
Globals np,P and reviewed fs_* dual/fy_* paired helpers. Definitions only.
Tests f=delta_test N,b=delta_test beta hold h and spatial material labels fixed.
No derivatives of tests enter this first-derivative phase action. The relative
phase term belongs here once; a native collector must exclude its duplicate.
The caller supplies the same invariant EOS values/directions from its candidate.
Hamiltonian normal rows are minus the action variation, as in the existing lift.
"""
CANDIDATE_PHASE_NORMAL_AUTHOR_DRAFT=True
CANDIDATE_PHASE_NORMAL_AUTHORING_IN_PROGRESS=False

def candidate_phase_normal_stress(s,c,direction,eos,f,b,keep,label):
 p=s['phi'][0].shape[0];put=lambda n,x:fs_keep(label+'_'+n,x,keep)
 for values,shapes in ((s,dict(g=(p,4,4),hi=(p,4,4),U=(p,4),uc=(p,4),P=(p,4,4),phi=(p,4))),
                       (c,dict(N=(p,),mu=(p,),h=(p,3,3),beta=(p,3)))):
  for n,shape in shapes.items():
   for pair in (values[n],direction[n]):
    assert isinstance(pair,tuple) and len(pair)==2
    assert all(w.shape==shape and w.dtype==np.dtype('float64') and np.all(np.isfinite(w)) for w in pair)
   put('supplied_'+n,fs_dual(values[n],direction[n]))
 assert f.shape==(p,) and b.shape==(p,3) and f.dtype==b.dtype==np.dtype('float64')
 assert np.all(np.isfinite(f)) and np.all(np.isfinite(b))
 keep(label+'_fixed_test_lapse',f.copy());keep(label+'_fixed_test_shift',b.copy())
 assert eos['candidate_pressure_recomputed_from_invariant'] is True
 variables={n:fs_dual(s[n],direction[n]) for n in s if n in ('g','hi','U','uc','P','phi')}
 g,I,U,uc,projector,phi=(variables[n] for n in ('g','hi','U','uc','P','phi'))
 N,mu,h,beta=(fs_dual(c[n],direction[n]) for n in ('N','mu','h','beta'))
 assert np.all(N[0][0]-abs(N[0][1])>0) and np.all(mu[0][0]-abs(mu[0][1])>0)
 X,pressure,PX=(fs_dual(eos['value'][n],eos['delta'][n]) for n in ('X','pressure','PX'))
 for n,a in (('X',X),('pressure',pressure),('PX',PX)):
  assert all(w.shape==(p,) and np.all(np.isfinite(w)) for pair in a for w in pair);put('EOS_'+n,a)
 assert np.all(X[0][0]-abs(X[0][1])>0)
 ft=fs_dual(P.a_dd(f));bt=fs_dual(P.a_dd(b));zero=fs_dual(P.a_dd(np.zeros((p,3,3))))
 hb=fs_mv(h,bt);q00=fs_add(fs_scale(-2.,fs_mul(N,ft)),fs_scale(2.,fs_dot(beta,hb)))
 q=put('metric_test',fs_block(q00,hb,zero))
 It=put('inverse_metric_test',fs_neg(fs_mm(fs_mm(I,q),I)))
 eta0=fs_neg(fs_div(fs_mul(fs_slice(U,(slice(None),0)),ft),N,keep,label+'_eta_time'))
 etai=fs_sub(fs_neg(fs_mul(fs_expand(fs_slice(U,(slice(None),0)),(Ellipsis,None)),bt)),fs_mul(beta,fs_expand(eta0,(Ellipsis,None))))
 eta=put('native_test',fs_stack([eta0]+[fs_slice(etai,(slice(None),i)) for i in range(3)],1))
 uct=put('lowered_native_test',fs_add(fs_mv(q,U),fs_mv(g,eta)))
 Pt=put('projector_test',fs_add(fs_mul(fs_expand(uct,(Ellipsis,slice(None),None)),fs_expand(U,(Ellipsis,None,slice(None)))),
                             fs_mul(fs_expand(uc,(Ellipsis,slice(None),None)),fs_expand(eta,(Ellipsis,None,slice(None))))))
 r=put('relative_phase',fs_mv(projector,phi));rt=put('relative_phase_test',fs_mv(Pt,phi))
 r2=put('relative_phase_squared',fs_dot(r,fs_mv(I,r)))
 Xtest=put('clock_test',fs_div(fs_scale(-.5,fs_dot(phi,fs_mv(It,phi))),X,keep,label+'_clock_test'))
 lm=put('measure_test',fs_div(ft,N,keep,label+'_measure_test'))
 absolute_terms=put('absolute_terms',fs_stack([fs_mul(PX,Xtest),fs_mul(pressure,lm)],1))
 relative_terms=put('relative_terms',fs_stack([fs_scale(-.5,fs_dot(r,fs_mv(It,r))),
                         fs_neg(fs_dot(r,fs_mv(I,rt))),fs_scale(-.5,fs_mul(r2,lm))],1))
 density=put('density',fs_mul(N,mu))
 absolute=put('absolute_action',fs_mul(density,fs_sum(absolute_terms,1)))
 relative=put('relative_action',fs_mul(density,fs_sum(relative_terms,1)))
 action=put('action_coefficient',fs_add(absolute,relative));hamiltonian=put('Hamiltonian_coefficient',fs_neg(action))
 put('EOS_clock_square_contact',fs_add(fs_mul(X,X),fs_dot(phi,fs_mv(I,phi))))
 put('measure_test_trace_contact',fs_sub(lm,fs_scale(.5,fs_sum(fs_sum(fs_mul(I,fs_transpose(q,(0,2,1))),2),1))))
 unit=fs_add(fs_dot(U,uc),fs_dual(P.a_dd(np.ones(p))));put('unit_constraint',unit)
 constructed=fs_add(fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4)))),fs_mul(fs_expand(uc,(Ellipsis,slice(None),None)),fs_expand(U,(Ellipsis,None,slice(None)))))
 put('projector_construction_contact',fs_sub(projector,constructed))
 outputs=dict(absolute=absolute,relative=relative,action=action,hamiltonian=hamiltonian)
 return dict(value={n:a[0] for n,a in outputs.items()},delta={n:a[1] for n,a in outputs.items()},
             test_first_derivative_coefficients_zero=True,relative_phase_included_once=True,
             global_weak_rows_assembled=False,finite_candidate_physically_admitted=False)
