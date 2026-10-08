"""Guarded definitions-only NEW certificate of completed saved coupled factor.
Caller supplies np/P/keep and authentic raw aliases; no input or kernel evaluation.
Preserve original failed componentwise absolute contact/control unchanged.
S=diag(2**e) is the saved positive power-of-two balance. For saved absolute A,
factor F and C=A F F^T-I, Cb=S^-1 C S, Ab=S^-1 A S^-1, Fb=S F obey
Cb=Ab Fb Fb^T-I in exact arithmetic. No absolute composition is reevaluated.
The NEW matrix operation-norm certificate uses ||Cb||2 relative to
1+||abs(Ab)||2 ||abs(Fb)||2^2, at the unchanged arithmetic2e-11.
This is explicitly a balanced normwise construction/backward-error test;
it is not the old offdiagonal relative test, a forward inverse-error bound,
a fine-action/coercivity claim, or any changed original physical row gate.
The signed contact Hsym SI-I is unearned and is computed once, then balanced
as Csb=S^-1 Cs S; Hb=S^-1 Hsym S^-1 and Ib=S SI S give Csb=Hb Ib-I.
Eigen-equation/orthogonality defects and strict resolved margins stay copied.
For ideal B=V |lambda| V^T, G=V |lambda|^-1/2 V^T, q=||V^T V-I||2,
kappa=max|lambda|/min|lambda|, the analytic identity defect is bounded by
q+(1+q)*(kappa*q+sqrt(kappa)*q+kappa*q*q), before finite construction errors.
Retain that explanatory bound, actual converted saved contact, and actual
normwise certificate; never use the explanatory bound as an alternative gate.
All scaling round trips must be bitwise exact and finite (including subnormal
cases); no silently lost word, exponent clipping, jitter, spectrum or factor
reconstruction, assembly, eigh, old fixture or operator replay is permitted.
"""
SAVED_STAR_BALANCED_CERTIFIER_AUTHOR_DRAFT=True
SAVED_STAR_BALANCED_CERTIFIER_AUTHORING_IN_PROGRESS=False

def saved_star_exact_power_balance(A,shift,label):
 A=np.asarray(A);assert A.dtype==np.float64 and np.all(np.isfinite(A))
 shift=np.asarray(shift);assert shift.dtype.kind in 'iu';keep(label+'_input',A.copy());keep(label+'_power_two_shift',shift.copy())
 out=np.ldexp(A,shift);keep(label+'_converted',out.copy());assert np.all(np.isfinite(out)),'Balanced conversion overflow'
 back=np.ldexp(out,-shift);keep(label+'_round_trip',back.copy());keep(label+'_round_trip_difference',(back-A).copy())
 assert np.array_equal(back,A),'Balanced conversion discarded bits; no exponent/readout loss allowed'
 return out

def certify_saved_native_metric_star_factor(s,label):
 required=('absolute','factor','symmetric','signed_inverse','failed_absolute_actual','failed_absolute_expected','failed_absolute_original_envelope','balance','inverse_balance','balance_exponents','eigenvalues','eigenvectors','eigen_equation_defect','orthogonality_defect','resolved_error_budget','resolved_spectral_margin')
 assert all(n in s for n in required)
 for n in required:keep(label+'_copied_'+n,np.asarray(s[n]).copy())
 e=np.asarray(s['balance_exponents']);sigma=np.asarray(s['balance']);inverse_sigma=np.asarray(s['inverse_balance']);n=s['factor'].shape[-1]
 assert e.dtype.kind in 'iu' and e.shape==sigma.shape==inverse_sigma.shape==s['eigenvalues'].shape and n==9
 assert np.array_equal(sigma,np.ldexp(np.ones_like(sigma),e)) and np.array_equal(inverse_sigma,np.ldexp(np.ones_like(sigma),-e)) and np.all(sigma>0) and np.all(inverse_sigma>0)
 shape=e.shape[:-1]+(n,n)
 for k in ('absolute','factor','symmetric','signed_inverse','failed_absolute_actual','failed_absolute_expected','failed_absolute_original_envelope','eigenvectors','eigen_equation_defect','orthogonality_defect'):
  assert np.asarray(s[k]).shape==shape and np.asarray(s[k]).dtype==np.float64 and np.all(np.isfinite(s[k]))
 assert np.all(s['failed_absolute_expected']==0) and np.all(s['failed_absolute_original_envelope']>=0) and np.all(np.isfinite(s['resolved_error_budget'])) and np.all(s['resolved_error_budget']>=0) and np.all(np.isfinite(s['resolved_spectral_margin'])) and np.all(s['resolved_spectral_margin']>0)
 absvals=abs(s['eigenvalues']);assert np.all(np.isfinite(absvals)) and np.all(absvals>0)
 q=np.linalg.norm(s['orthogonality_defect'],2,axis=(-2,-1));kappa=np.max(absvals,axis=-1)/np.min(absvals,axis=-1)
 explanatory=q+(1+q)*(kappa*q+np.sqrt(kappa)*q+kappa*q*q)
 keep(label+'_saved_eigen_equation_norm',np.linalg.norm(s['eigen_equation_defect'],2,axis=(-2,-1)));keep(label+'_saved_orthogonality_norm',q.copy());keep(label+'_spectral_condition_magnitude',kappa.copy());keep(label+'_ideal_orthogonality_identity_bound_only',explanatory.copy())
 ei=e[..., :,None];ej=e[...,None,:]
 Cb=saved_star_exact_power_balance(s['failed_absolute_actual'],-ei+ej,label+'_saved_absolute_contact_balanced')
 Ab=saved_star_exact_power_balance(s['absolute'],-ei-ej,label+'_saved_absolute_block_balanced')
 Fb=saved_star_exact_power_balance(s['factor'],ei,label+'_saved_coordinate_factor_balanced')
 a_norm=np.linalg.norm(abs(Ab),2,axis=(-2,-1));f_norm=np.linalg.norm(abs(Fb),2,axis=(-2,-1));actual=np.linalg.norm(Cb,2,axis=(-2,-1));envelope=1+a_norm*f_norm*f_norm
 for k,x in (('absolute_positive_block_norm',a_norm),('absolute_positive_factor_norm',f_norm),('absolute_saved_contact_norm',actual),('absolute_operation_norm_envelope',envelope)):keep(label+'_'+k,np.asarray(x).copy())
 assert np.all(np.isfinite(envelope)) and np.all(envelope>=1)
 P.check(label+'_NEW_saved_absolute_balanced_normwise_construction',actual,np.zeros_like(actual),envelope)
 absolute_scores=actual/envelope;keep(label+'_absolute_normwise_scores',absolute_scores.copy())
 product=s['symmetric']@s['signed_inverse'];keep(label+'_NEW_signed_composition_product',product.copy());Cs=product-np.eye(n);keep(label+'_NEW_signed_contact',Cs.copy())
 Csb=saved_star_exact_power_balance(Cs,-ei+ej,label+'_NEW_signed_contact_balanced')
 Hb=saved_star_exact_power_balance(s['symmetric'],-ei-ej,label+'_saved_symmetric_block_balanced')
 Ib=saved_star_exact_power_balance(s['signed_inverse'],ei+ej,label+'_saved_signed_inverse_balanced')
 h_norm=np.linalg.norm(abs(Hb),2,axis=(-2,-1));i_norm=np.linalg.norm(abs(Ib),2,axis=(-2,-1));signed_actual=np.linalg.norm(Csb,2,axis=(-2,-1));signed_envelope=1+h_norm*i_norm
 for k,x in (('signed_positive_block_norm',h_norm),('signed_positive_inverse_norm',i_norm),('NEW_signed_contact_norm',signed_actual),('signed_operation_norm_envelope',signed_envelope)):keep(label+'_'+k,np.asarray(x).copy())
 assert np.all(np.isfinite(signed_envelope)) and np.all(signed_envelope>=1)
 P.check(label+'_NEW_signed_balanced_normwise_construction',signed_actual,np.zeros_like(signed_actual),signed_envelope)
 signed_scores=signed_actual/signed_envelope;keep(label+'_signed_normwise_scores',signed_scores.copy())
 return dict(kind='NEW_balanced_normwise_certificate_of_completed_saved_coupled_factor',new_arithmetic_controls=2,arithmetic_tolerance=P.TOL,absolute_max_score=float(np.max(absolute_scores)),signed_max_score=float(np.max(signed_scores)),original_componentwise_failed_control_preserved=True,absolute_contact_or_factor_replayed=False,signed_contact_is_NEW_once=True,scaling_round_trip_bitwise_exact=True,gate_is_construction_operation_norm=True,explanatory_orthogonality_bound_is_an_admission_route=False,fine_action_RHS_or_original_row_gates_changed=False,forward_inverse_error_or_global_coercivity_claimed=False,physical_adoption=False)
