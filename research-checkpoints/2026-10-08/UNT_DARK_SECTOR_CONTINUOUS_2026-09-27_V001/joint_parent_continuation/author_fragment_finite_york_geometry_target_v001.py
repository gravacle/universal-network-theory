"""Held definitions only: exact conformal geometry and actual-trace target/JVP.
Globals np,P provide the admitted paired arithmetic; keep normalizes numeric data.
rho and rho_R/Z are new log-psi pairs; h=exp(4rho)*owned h_ref. A new spatial
inverse/volume is resolved from h_ref, never inferred from the owned inverse.
The owned reference inverse/volume and old /3 target are comparison operands.
W_jet is the NEW increment from W_aux, ordered component x(value,R,Z); t is
the NEW scalar increment with fixed owned reference canonical density weight.
Reference L maps/raising coefficients are a fixed target-data operator, not a
candidate action Hessian. All its tiny cross entries participate. No old W
application, coefficient, feature, fixture, inverse launch or payload is run.
This component supplies spatial geometry only; complete spacetime/connection,
EOS/currents, mechanical Legendre and normal/CMC residuals remain unearned.
"""
FINITE_YORK_AUTHOR_DRAFT=True
FINITE_YORK_AUTHORING_IN_PROGRESS=False

def fy_keep(name,x,keep):
 keep(name+'_hi',np.asarray(x[0]).copy());keep(name+'_lo',np.asarray(x[1]).copy());return x

def fy_sum(x,axis):
 axis=axis%x[0].ndim;out=P.a_dd(np.zeros(x[0].shape[:axis]+x[0].shape[axis+1:]))
 for i in range(x[0].shape[axis]):out=P.a_add(out,(np.take(x[0],i,axis=axis),np.take(x[1],i,axis=axis)))
 return out

def fy_mv(A,x):return fy_sum(P.a_mul(A,(x[0][...,None,:],x[1][...,None,:])),-1)

def fy_mm(A,B):return P.a_stack([fy_mv(A,P.a_slice(B,(Ellipsis,slice(None),j))) for j in range(B[0].shape[-1])],axis=-1)

def fy_contract(A,B):return fy_sum(fy_sum(P.a_mul(A,B),-1),-1)

def fy_scale_matrix(s,A):return P.a_mul((s[0][...,None,None],s[1][...,None,None]),A)

def fy_div(x,y,keep,label):
 # Two bounded corrections use the complete paired denominator each time.
 assert np.all(np.isfinite(y[0])) and np.all(np.isfinite(y[1])) and np.all(abs(y[0])>abs(y[1]))
 fy_keep(label+'_numerator',x,keep);fy_keep(label+'_denominator',y,keep)
 q=P.a_div64(x,y[0],keep,label+'_initial_high_denominator')
 for step in range(2):
  r=fy_keep(label+'_current_remainder',P.a_sub(x,P.a_mul(y,q)),keep)
  dq=P.a_div64(r,y[0],keep,label+'_correction_'+str(step));q=fy_keep(label+'_current_quotient',P.a_add(q,dq),keep)
 fy_keep(label+'_final_division_residual',P.a_sub(x,P.a_mul(y,q)),keep);return fy_keep(label+'_quotient',q,keep)

def fy_sqrt(x,keep,label):
 assert np.all(x[0]-abs(x[1])>0)
 root=P.a_dd(np.sqrt(x[0]));fy_keep(label+'_initial_root',root,keep)
 for step in range(2):
  residual=fy_keep(label+'_current_square_residual',P.a_sub(x,P.a_mul(root,root)),keep)
  change=fy_div(residual,P.a_mul64(2.,root),keep,label+'_correction_'+str(step));root=fy_keep(label+'_current_root',P.a_add(root,change),keep)
 fy_keep(label+'_final_square_residual',P.a_sub(P.a_mul(root,root),x),keep);return fy_keep(label+'_root',root,keep)

def fy_physical_reference_inverse(h,keep,label):
 assert h[0].shape==h[1].shape and h[0].shape[-2:]==(3,3)
 assert all(np.array_equal(w,w.swapaxes(-1,-2)) for w in h)
 a,b,c,d,e,f=[P.a_slice(h,(Ellipsis,i,j)) for i,j in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))]
 A=P.a_sub(P.a_mul(d,f),P.a_mul(e,e));B=P.a_sub(P.a_mul(c,e),P.a_mul(b,f));C=P.a_sub(P.a_mul(b,e),P.a_mul(c,d))
 D=P.a_sub(P.a_mul(a,f),P.a_mul(c,c));E=P.a_sub(P.a_mul(b,c),P.a_mul(a,e));F=P.a_sub(P.a_mul(a,d),P.a_mul(b,b))
 det=fy_keep(label+'_determinant',P.a_add(P.a_add(P.a_mul(a,A),P.a_mul(b,B)),P.a_mul(c,C)),keep)
 ah,dh,fh,bh,ch,eh=[abs(v[0])+abs(v[1]) for v in (a,d,f,b,c,e)]
 bounds=(ah,ah*dh+bh*bh,ah*(dh*fh+eh*eh)+bh*(ch*eh+bh*fh)+ch*(bh*eh+ch*dh))
 for name,value,bound in zip(('leading_one','leading_two','determinant'),(a,F,det),bounds):
  fy_keep(label+'_'+name+'_positive_operand',value,keep);keep(label+'_'+name+'_operation_envelope',np.asarray(bound).copy())
  lower=value[0]-abs(value[1]);keep(label+'_'+name+'_positive_lower',np.asarray(lower).copy());assert np.all(lower>2e-11*bound)
 adj=P.a_stack([P.a_stack(row,axis=-1) for row in ((A,B,C),(B,D,E),(C,E,F))],axis=-2)
 inverse=fy_div(adj,(det[0][...,None,None],det[1][...,None,None]),keep,label+'_inverse')
 fy_keep(label+'_h_inverse_minus_identity',P.a_sub(fy_mm(h,inverse),P.a_dd(np.broadcast_to(np.eye(3),h[0].shape))),keep)
 return inverse,det

def fy_longitudinal_increment(reference,W_jet,keep,label):
 maps=reference['L_maps'];assert maps[0].shape==maps[1].shape==(W_jet[0].shape[0],3,3,3,3)
 assert W_jet[0].shape==W_jet[1].shape==(maps[0].shape[0],3,3)
 product=P.a_mul(maps,(W_jet[0][...,None,None],W_jet[1][...,None,None]));L=fy_keep(label+'_L_increment',fy_sum(fy_sum(product,2),1),keep)
 inverse=P.a_dd(reference['target_raising_inverse']);raised=fy_mm(fy_mm(inverse,L),inverse)
 return fy_keep(label+'_canonical_density_increment',P.a_mul64(reference['mu_owned'][:,None,None],raised),keep)

def finite_york_geometry_target(reference,rho,rho_gradient,W_jet,t,direction,keep,label):
 p=rho[0].size;h0=P.a_dd(reference['h']);dh0=reference['h_spatial_jets'];Pi=reference['Pi_owned'];T0=reference['T_owned']
 assert rho[0].shape==rho[1].shape==t[0].shape==t[1].shape==(p,)
 assert h0[0].shape==(p,3,3) and dh0[0].shape==dh0[1].shape==(p,2,3,3)
 assert rho_gradient[0].shape==rho_gradient[1].shape==(p,2)
 assert Pi[0].shape==Pi[1].shape==T0[0].shape==T0[1].shape==(p,3,3)
 assert reference['ih_owned'].shape==reference['target_raising_inverse'].shape==(p,3,3) and reference['mu_owned'].shape==(p,)
 assert np.all(np.isfinite(reference['mu_owned'])) and np.all(reference['mu_owned']>0)
 for n,shape in (('rho',(p,)),('rho_gradient',(p,2)),('W_jet',(p,3,3)),('t',(p,))):
  assert direction[n][0].shape==direction[n][1].shape==shape
  fy_keep(label+'_direction_input_'+n,direction[n],keep)
 put=lambda n,x:fy_keep(label+'_'+n,x,keep)
 for n,x in (('reference_h',h0),('reference_h_spatial_jets',dh0),('reference_Pi_owned',Pi),('reference_T_owned',T0),('rho_input',rho),('rho_gradient_input',rho_gradient),('W_increment_input',W_jet),('t_increment_input',t)):put(n,x)
 I0,det0=fy_physical_reference_inverse(h0,keep,label+'_physical_reference');mu0=fy_sqrt(det0,keep,label+'_physical_reference_volume')
 put('physical_minus_owned_reference_inverse',P.a_sub(I0,P.a_dd(reference['ih_owned'])))
 put('physical_minus_owned_reference_volume',P.a_sub(mu0,P.a_dd(reference['mu_owned'])))
 tau0=put('actual_owned_reference_trace',fy_contract(h0,Pi));put('actual_minus_owned_reference_trace',P.a_sub(tau0,reference['tau_owned']))
 k0=put('reference_inverse_trace',fy_contract(h0,I0));c0=put('owned_T_reference_trace',fy_contract(h0,T0))
 base=P.a_add(T0,fy_scale_matrix(fy_div(P.a_sub(tau0,c0),k0,keep,label+'_base_trace_correction'),I0))
 anchor=put('owned_reference_target_anchor',P.a_sub(Pi,base));put('owned_reference_anchor_trace',fy_contract(h0,anchor))
 put('owned_reference_raw_three_target',P.a_add(T0,fy_scale_matrix(P.a_div64(tau0,3.,keep,label+'_raw_three'),P.a_dd(reference['ih_owned']))))
 # exp/expm1 are elementary binary64 constructions, not an asserted exact exp.
 exp_hi=np.exp(4*rho[0]);exp_lo=np.expm1(4*rho[1]);keep(label+'_elementary_exp_high',exp_hi.copy());keep(label+'_elementary_expm1_low',exp_lo.copy())
 assert np.all(np.isfinite(exp_hi)) and np.all(exp_hi>0) and np.all(np.isfinite(exp_lo))
 lam=put('conformal_weight',P.a_add(P.a_dd(exp_hi),P.a_prod(exp_hi,exp_lo)));assert np.all(lam[0]-abs(lam[1])>0)
 inverse_lam=fy_div(P.a_dd(np.ones(p)),lam,keep,label+'_inverse_weight')
 h=put('candidate_h',fy_scale_matrix(lam,h0));I=put('candidate_inverse',fy_scale_matrix(inverse_lam,I0))
 mu=put('candidate_volume',P.a_mul(mu0,P.a_mul(lam,fy_sqrt(lam,keep,label+'_weight_root'))))
 put('candidate_inverse_residual',P.a_sub(fy_mm(h,I),P.a_dd(np.broadcast_to(np.eye(3),(p,3,3)))))
 h_jets=P.a_add(dh0,P.a_mul((P.a_mul64(4.,rho_gradient)[0][...,None,None],P.a_mul64(4.,rho_gradient)[1][...,None,None]),(h0[0][:,None],h0[1][:,None])))
 h_jets=put('candidate_h_spatial_jets',P.a_mul((lam[0][:,None,None,None],lam[1][:,None,None,None]),h_jets))
 BW=fy_longitudinal_increment(reference,W_jet,keep,label+'_new_W');T=put('candidate_T',fy_scale_matrix(inverse_lam,P.a_add(P.a_add(T0,anchor),BW)))
 tau=put('candidate_trace_coordinate',P.a_add(tau0,P.a_mul64(reference['mu_owned'],t)))
 kappa=put('candidate_inverse_trace',fy_contract(h,I));kbound=np.sum((abs(h[0])+abs(h[1]))*(abs(I[0])+abs(I[1])),axis=(1,2))
 keep(label+'_kappa_operation_envelope',kbound.copy());assert np.all(kappa[0]-abs(kappa[1])>2e-11*kbound)
 c=put('candidate_T_actual_trace',fy_contract(h,T));trace_part=fy_div(P.a_sub(tau,c),kappa,keep,label+'_candidate_trace_part')
 target=put('candidate_target',P.a_add(T,fy_scale_matrix(trace_part,I)));put('candidate_target_trace_minus_coordinate',P.a_sub(fy_contract(h,target),tau))
 raw_three=P.a_add(T,fy_scale_matrix(P.a_div64(tau,3.,keep,label+'_candidate_raw_three'),I));put('candidate_actual_trace_minus_raw_three_target',P.a_sub(target,raw_three))
 dr=direction['rho'];drg=direction['rho_gradient'];dBW=fy_longitudinal_increment(reference,direction['W_jet'],keep,label+'_direction_W')
 Q=put('delta_h',fy_scale_matrix(P.a_mul64(4.,dr),h));dI=put('delta_inverse',fy_scale_matrix(P.a_mul64(-4.,dr),I));dmu=put('delta_volume',P.a_mul(P.a_mul64(6.,dr),mu))
 formal=put('formal_inverse_contact',P.a_mul64(-1.,fy_mm(fy_mm(I,Q),I)));put('analytic_minus_formal_inverse_contact',P.a_sub(dI,formal))
 formal_mu=P.a_mul(P.a_mul64(.5,mu),fy_contract(I,Q));put('analytic_minus_formal_volume_contact',P.a_sub(dmu,formal_mu))
 d_hjets=P.a_add(P.a_mul((P.a_mul64(4.,dr)[0][:,None,None,None],P.a_mul64(4.,dr)[1][:,None,None,None]),h_jets),P.a_mul((P.a_mul64(4.,drg)[0][...,None,None],P.a_mul64(4.,drg)[1][...,None,None]),(h[0][:,None],h[1][:,None])))
 put('delta_h_spatial_jets',d_hjets);dT=put('delta_T',P.a_add(fy_scale_matrix(P.a_mul64(-4.,dr),T),fy_scale_matrix(inverse_lam,dBW)))
 dtau=put('delta_trace_coordinate',P.a_mul64(reference['mu_owned'],direction['t']));dc=put('delta_T_actual_trace',P.a_add(fy_contract(Q,T),fy_contract(h,dT)))
 dk=put('delta_inverse_trace',P.a_add(fy_contract(Q,I),fy_contract(h,dI)))
 dpart=fy_div(P.a_sub(P.a_sub(dtau,dc),P.a_mul(trace_part,dk)),kappa,keep,label+'_direction_trace_part')
 dtarget=put('delta_target',P.a_add(P.a_add(dT,fy_scale_matrix(trace_part,dI)),fy_scale_matrix(dpart,I)))
 put('delta_actual_trace_minus_coordinate',P.a_sub(P.a_add(fy_contract(Q,target),fy_contract(h,dtarget)),dtau))
 for name,actual in (('independent_delta_h',Q),('independent_delta_inverse',dI),('independent_delta_target',dtarget),('registered_delta_h',Q)):
  if name in direction:
   supplied=direction[name];assert supplied[0].shape==supplied[1].shape==actual[0].shape
   put(name+'_supplied',supplied);put('actual_minus_'+name,P.a_sub(actual,supplied))
 return dict(h=h,ih=I,mu=mu,h_spatial_jets=h_jets,target=target,tau=tau,delta_h=Q,delta_ih=dI,delta_mu=dmu,delta_h_spatial_jets=d_hjets,delta_target=dtarget,delta_tau=dtau,reference_anchor=anchor,raw_reference_TT_certificate_transferred=False,physical_adoption=False)
