"""Definitions only: five physical target-field first contact at York psi_ref=1.
Caller supplies np and admitted paired arithmetic P; no functions are invoked.
Reference conformal geometry/native/modal covectors are fixed. S is the owned
weight-one tensor density Pi_TT_ref+Btilde W, not a newly fitted moment map.
The three delta W components enter only through supplied full delta_BW density.
Tau and delta_tau are total canonical trace densities, never bare-EH K.
Choose tau=mu_ref*t with fixed current-reference mu_ref=sqrt_h; delta_tau
is mu_ref*delta_t. No delta_mu*t is inserted into this target parameterization.
This is one target derivative, not a field solve, rank or finite preparation.
"""

def five_field_pair_contract(x,y):
 out=P.a_dd(np.zeros(x[0].shape[:-2]))
 for i in range(3):
  for j in range(3):out=P.a_add(out,P.a_mul(P.a_slice(x,(Ellipsis,i,j)),P.a_slice(y,(Ellipsis,i,j))))
 return out

def five_field_raw_left(A,x):
 return P.a_stack([P.a_matvec(A,P.a_slice(x,(Ellipsis,slice(None),j))) for j in range(x[0].shape[-1])],axis=-1)

def five_field_raw_right(x,A):
 return P.a_stack([P.a_matvec(A.swapaxes(-1,-2),P.a_slice(x,(Ellipsis,i,slice(None)))) for i in range(x[0].shape[-2])],axis=-2)

def initial_york_five_field_target_contact(A_ref,h_basis,h,ih,sqrt_h,S,tau,
 owned_Pi,delta_a,delta_BW,delta_tau,keep,label):
 # h_basis is the authentic coordinate conformal value map diag(1,1,R^2).
 p=len(A_ref);assert A_ref.shape==sqrt_h.shape==(p,) and np.all(A_ref>0) and np.all(sqrt_h>0)
 assert h_basis.shape==h.shape==ih.shape==(p,3,3)
 for x in (S,owned_Pi,delta_BW):assert x[0].shape==x[1].shape==(p,3,3)
 for x in (tau,delta_a,delta_tau):assert x[0].shape==x[1].shape==(p,)
 def put(n,x):keep(label+'_'+n+'_hi',x[0]);keep(label+'_'+n+'_lo',x[1]);return x
 theta=put('delta_log_psi',P.a_div64(delta_a,4*A_ref,keep,label+'_conformal_normalization'))
 Q=put('delta_h',P.a_mul64(h_basis,(delta_a[0][:,None,None],delta_a[1][:,None,None])))
 product=five_field_raw_right(five_field_raw_left(ih,Q),ih);delta_ih=put('delta_ih',(-product[0],-product[1]))
 third=P.a_div64(tau,3.,keep,label+'_base_tau_division');base=put('base_target_tensor_density',P.a_add(S,P.a_mul64(ih,(third[0][:,None,None],third[1][:,None,None]))))
 put('base_target_minus_owned_literal_tensor_density',P.a_sub(base,owned_Pi))
 conformal=put('conformal_target_contact',P.a_mul((theta[0][:,None,None],theta[1][:,None,None]),P.a_mul64(-4.,S)))
 inverse_tau=P.a_mul(delta_ih,(tau[0][:,None,None],tau[1][:,None,None]));trace_delta=P.a_mul64(ih,(delta_tau[0][:,None,None],delta_tau[1][:,None,None]))
 canonical_trace=put('canonical_trace_target_contact',P.a_div64(P.a_add(inverse_tau,trace_delta),3.,keep,label+'_delta_trace_division'))
 target=put('delta_target_tensor_density',P.a_add(P.a_add(conformal,delta_BW),canonical_trace))
 six=[]
 for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2)):
  value=P.a_slice(target,(slice(None),i,j))
  if i!=j:value=P.a_add(value,P.a_slice(target,(slice(None),j,i)))
  six.append(value)
 coordinate=put('delta_target_six_coordinate_density',P.a_stack(six,axis=-1))
 put('serialized_delta_inverse_antisymmetry',P.a_sub(delta_ih,P.a_transpose(delta_ih,(0,2,1))))
 put('serialized_target_contact_antisymmetry',P.a_sub(target,P.a_transpose(target,(0,2,1))))
 relative_amplitude=put('delta_a_over_reference_amplitude',P.a_div64(delta_a,A_ref,keep,label+'_amplitude_normalization'))
 put('registered_delta_h_minus_reference_conformal_contact',P.a_sub(Q,P.a_mul64(h,(relative_amplitude[0][:,None,None],relative_amplitude[1][:,None,None]))))
 t_ref=put('fixed_reference_scalar_trace',P.a_div64(tau,sqrt_h,keep,label+'_reference_trace_scalar'))
 delta_t=put('fixed_reference_scalar_trace_contact',P.a_div64(delta_tau,sqrt_h,keep,label+'_reference_trace_scalar_contact'))
 put('fixed_reference_tau_reconstruction_gap',P.a_sub(tau,P.a_mul64(sqrt_h,t_ref)))
 put('fixed_reference_delta_tau_reconstruction_gap',P.a_sub(delta_tau,P.a_mul64(sqrt_h,delta_t)))
 put('owned_h_minus_reference_amplitude_basis',P.a_sub(P.a_dd(h),P.a_prod(A_ref[:,None,None],h_basis)))
 dmu=put('literal_spatial_density_contact',P.a_mul64(.5*sqrt_h,five_field_pair_contract(P.a_dd(ih),Q)))
 put('density_contact_minus_exact_conformal_chain',P.a_sub(dmu,P.a_mul64(6*sqrt_h,theta)))
 dt=put('actual_canonical_trace_contact',P.a_add(five_field_pair_contract(Q,base),five_field_pair_contract(P.a_dd(h),target)))
 put('canonical_trace_contact_minus_delta_tau',P.a_sub(dt,delta_tau))
 return dict(delta_h=Q,delta_ih=delta_ih,delta_target=target,delta_coordinate_target=coordinate,
 delta_sqrt_h=dmu,base_target=base,canonical_tau_is_K=False,psi_reference_one=True,
 tau_parameterization="fixed_reference_mu_ref_times_scalar_t",reference_weight_held_fixed=True,
 native_and_phase_targets_unchanged=True,physical_free_data_and_exterior_admitted=False,
 global_rate_response_computed=False,global_rank_claimed=False,finite_preparation_adopted=False)
