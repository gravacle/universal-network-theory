"""HELD right-only adapter for the retained paired GMRES117 recurrence.
Globals np,P,keep,native_metric_gmres_put,native_metric_gmres_solve.
The containing caller authenticates completed same-candidate weak67 caches,
current-minus-prepared-target RHS and NEW active nodal factor admission.
No old star operator, source, prepared-target, action or solve is invoked here.
"""
RIGHT_GMRES_AUTHOR_DRAFT=True
RIGHT_GMRES_AUTHORING_IN_PROGRESS=False
RIGHT_GMRES_CANDIDATE_CLOSURE=(None,None,None)
RIGHT_GMRES_CACHE_CLOSURE=(None,None,None)
RIGHT_GMRES_NODAL_FACTOR_CLOSURE=(None,None,None)

def candidate_right_identity_left(x,label):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape==(403340,)
 out=tuple(a.copy() for a in x)
 for word,a in zip(('hi','lo'),out):
  keep(label+'_explicit_identity_left_'+word,a.copy())
  assert a.dtype==np.float64 and np.all(np.isfinite(a))
 return out

def candidate_right_only_mechanical_gmres(start,current,rhs,right_apply,action,positive,scores,admission,keep,label,cap,progress=None):
 assert 1<=cap<=80 and P.LINEAR_TOL==1e-10
 assert isinstance(admission['closed_provenance'],dict) and admission['closed_provenance']
 assert admission['all_four_same_candidate_caches_authenticated'] is True
 assert admission['active_nodal_factors_admitted'] is True
 assert admission['original_six_reference_gates_unchanged'] is True
 assert admission['RHS_is_current_prepared_target_minus_current'] is True
 assert admission['all_off_node_weak_couplings_retained'] is True
 assert admission['physical_adoption'] is False and admission['full_weak_inverse_qualified'] is False
 for name,pair in (('supplied_correction_start',start),('supplied_canonical_defect_RHS',rhs),('cached_same_candidate_action',current['action']),('cached_same_candidate_residual',current['residual'])):
  native_metric_gmres_put(label+'_'+name,pair)
  assert pair[0].shape==pair[1].shape==(403340,)
 keep(label+'_original_reference_scores',np.asarray(current['scores']).copy())
 def forward(x,tag):return right_apply(x,tag+'_signed_active_nodal_right_factor')
 result=native_metric_gmres_solve(start,current,rhs,forward,candidate_right_identity_left,action,positive,scores,label+'_right_only',cap,progress)
 updated,after,increment,meta=result
 meta=dict(meta)
 meta.update(preconditioning='A(Q) P_node_inverse with explicit identity left map',left_map_is_identity=True,left_map_is_right_factor_transpose=False,original_affine_and_canonical_reference_gates_unchanged=True,full_off_node_candidate_action_retained=True,physical_base_state_reset=False,full_weak_inverse_qualified=False,physical_adoption=False)
 return updated,after,increment,meta
