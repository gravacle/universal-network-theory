"""HELD paired directed local-factor application; definitions only.
Globals np,P,mh_pair. Signed factors are numerical coefficient pairs, not a
proved all-input DD inverse. A containing driver must bind actual earned local
factor closure/proof; no old basis/action/certificate is invoked here.
"""
MODAL_APPLY_AUTHOR_DRAFT=True
MODAL_APPLY_AUTHORING_IN_PROGRESS=False
MODAL_APPLY_FACTOR_SOURCE=(None,None)
MODAL_APPLY_FACTOR_RESULT=(None,None,None)
MODAL_APPLY_FACTOR_RECEIPT=(None,None,None)
MODAL_APPLY_FACTOR_PROOF=(None,None,None)

def ma_matvec(A,x,keep,label):
 assert A[0].shape==A[1].shape and x[0].shape==x[1].shape and A[0].shape[:-2]==x[0].shape[:-1] and A[0].shape[-1]==x[0].shape[-1]
 terms=P.a_mul(A,(x[0][...,None,:],x[1][...,None,:]));mh_pair(label+'_all_paired_products',terms,A[0].shape,keep)
 out=P.a_dd(np.zeros(A[0].shape[:-1]))
 for column in range(A[0].shape[-1]):
  term=P.a_slice(terms,(Ellipsis,column));mh_pair(label+'_column%d_product'%column,term,out[0].shape,keep)
  out=P.a_add(out,term);mh_pair(label+'_column%d_partial'%column,out,out[0].shape,keep)
 return out

def candidate_modal_head_factor_apply(factors,rhs,keep,label):
 assert factors['p']==4 and isinstance(factors['closed_provenance'],dict) and factors['closed_provenance'] and factors['local_real_certificate_admitted'] is True
 assert factors['uniform_all_input_DD_inverse_qualified'] is False and factors['full_weak_or_global_inverse_qualified'] is False and factors['physical_adoption'] is False
 p=4;B=mh_pair(label+'_factor_B_head_from_arm',factors['B'],(32,p,9,3),keep);E=mh_pair(label+'_factor_E_arm_from_head',factors['E'],(32,p,3,9),keep)
 DI=mh_pair(label+'_factor_measured_D_inverse',factors['D_inverse'],(32,p,3,3),keep);J=mh_pair(label+'_factor_signed_S9_candidate_inverse',factors['S9_inverse'],(p,9,9),keep)
 native=mh_pair(label+'_original_native_density_RHS',rhs['native'],(p,99),keep);metric=mh_pair(label+'_original_metric_density_RHS',rhs['metric'],(p,6),keep)
 head_rhs=P.a_stack([P.a_slice(native,(slice(None),i)) for i in range(3)]+[P.a_slice(metric,(slice(None),i)) for i in range(6)],-1);mh_pair(label+'_head_RHS',head_rhs,(p,9),keep)
 arm_rhs=tuple(a[:,3:].reshape(p,32,3).transpose(1,0,2) for a in native);mh_pair(label+'_arm_RHS',arm_rhs,(32,p,3),keep)
 free=ma_matvec(DI,arm_rhs,keep,label+'_Dinv_arm_RHS');mh_pair(label+'_free_arm_solution',free,(32,p,3),keep);reduced=head_rhs
 for mode in range(32):
  contribution=ma_matvec(P.a_slice(B,mode),P.a_slice(free,mode),keep,label+'_mode%02d_head_reaction'%mode);mh_pair(label+'_mode%02d_head_reaction'%mode,contribution,(p,9),keep)
  reduced=P.a_sub(reduced,contribution);mh_pair(label+'_mode%02d_reduced_head_RHS'%mode,reduced,(p,9),keep)
 head=ma_matvec(J,reduced,keep,label+'_head_solution');mh_pair(label+'_head_solution',head,(p,9),keep);arms=P.a_dd(np.zeros((32,p,3)))
 for mode in range(32):
  reaction=ma_matvec(P.a_slice(E,mode),head,keep,label+'_mode%02d_arm_reaction'%mode);mh_pair(label+'_mode%02d_arm_reaction'%mode,reaction,(p,3),keep)
  corrected=P.a_sub(P.a_slice(arm_rhs,mode),reaction);mh_pair(label+'_mode%02d_corrected_arm_RHS'%mode,corrected,(p,3),keep)
  result=ma_matvec(P.a_slice(DI,mode),corrected,keep,label+'_mode%02d_arm_solution'%mode);mh_pair(label+'_mode%02d_arm_solution'%mode,result,(p,3),keep)
  for word in (0,1):arms[word][mode]=result[word]
  mh_pair(label+'_mode%02d_all_arm_solution_partial'%mode,arms,(32,p,3),keep)
 native_rate=P.a_stack([P.a_slice(head,(slice(None),i)) for i in range(3)]+[P.a_slice(arms,(mode,slice(None),i)) for mode in range(32) for i in range(3)],-1)
 metric_rate=P.a_stack([P.a_slice(head,(slice(None),i)) for i in range(3,9)],-1)
 mh_pair(label+'_native_rate',native_rate,(p,99),keep);mh_pair(label+'_physical_symmetric_metric_rate',metric_rate,(p,6),keep)
 return dict(native=native_rate,metric=metric_rate,head=head,arms=arms,both_RHS_words_used=True,signed_directed_factors_used=True,physical_metric_six_order='RR,ZZ,phiphi,RZ,Rphi,Zphi; no extra factor2',exact_real_vs_represented_DD_factor_scope_retained=True,exact_inverse_or_all_input_DD_linearity_claimed=False,full_weak_or_global_preconditioner_admitted=False,physical_adoption=False)
