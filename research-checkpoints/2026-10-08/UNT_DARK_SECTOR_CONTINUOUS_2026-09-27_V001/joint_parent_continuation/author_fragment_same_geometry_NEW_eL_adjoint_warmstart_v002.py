"""HELD NEW-eL warm adjoint handoff at unchanged geometry; definitions only.
Globals np,P plus reviewed170 GMRES/53 source-relative helpers. No old action,
factor, basis, scalar state, target/current, EOS or physical producer is replayed.
The old lambda and its saved represented244 action are a warm seed only.
"""
SAME_GEOMETRY_ADJOINT_AUTHOR_DRAFT=True
SAME_GEOMETRY_ADJOINT_AUTHORING_IN_PROGRESS=False
SAME_GEOMETRY_ADJOINT_OLD_SOURCE=(None,None)
SAME_GEOMETRY_ADJOINT_OLD_RESULT=(None,None,None)
SAME_GEOMETRY_ADJOINT_OLD_RECEIPT=(None,None,None)
SAME_GEOMETRY_ADJOINT_OLD_PROOF=(None,None,None)
SAME_GEOMETRY_ADJOINT_NEW_E_L_SOURCE=(None,None)
SAME_GEOMETRY_ADJOINT_NEW_E_L_RESULT=(None,None,None)
SAME_GEOMETRY_ADJOINT_NEW_E_L_RECEIPT=(None,None,None)
SAME_GEOMETRY_ADJOINT_NEW_E_L_PROOF=(None,None,None)
SAME_GEOMETRY_ADJOINT_SOURCE_PINS={'author_fragment_native_metric_star_paired_gmres_resume_v002.py':'73b15a0e0512295aed41389a80c20ec6cf50ddef634497c805ada69c8ed738ee','author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py':'25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c','author_fragment_candidate_fullweak_transpose_stationarity_v003.py':'3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871','author_fragment_candidate_directed_nodal_factor_apply_v001.py':'4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b'}

def same_geometry_adjoint_pair(x,keep,label):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 assert all(a.shape==(403340,) and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x),label
 for w,n in enumerate(('hi','lo')):keep(label+'_'+n,x[w].copy())
 return x


def prepare_same_geometry_adjoint_warmstart(rhs_new,original_scale,lambda_old,action_old,old_positive,admission,keep,label,complete_stage):
 assert not SAME_GEOMETRY_ADJOINT_AUTHOR_DRAFT and not SAME_GEOMETRY_ADJOINT_AUTHORING_IN_PROGRESS
 refs=(SAME_GEOMETRY_ADJOINT_OLD_SOURCE,SAME_GEOMETRY_ADJOINT_OLD_RESULT,SAME_GEOMETRY_ADJOINT_OLD_RECEIPT,SAME_GEOMETRY_ADJOINT_OLD_PROOF,SAME_GEOMETRY_ADJOINT_NEW_E_L_SOURCE,SAME_GEOMETRY_ADJOINT_NEW_E_L_RESULT,SAME_GEOMETRY_ADJOINT_NEW_E_L_RECEIPT,SAME_GEOMETRY_ADJOINT_NEW_E_L_PROOF)
 assert all(v is not None for q in refs for v in q) and admission['terminals']==list(refs),'Root-authenticated closed old solution and fresh eL required'
 assert admission['source_pins']==SAME_GEOMETRY_ADJOINT_SOURCE_PINS and admission['operator']=='represented_directed_original244_coefficient_Astar'
 for n in ('all_selected_seals_verified','old_solution_and_action_argument_words_verified','same_paired_point_descriptors_and_original_basis_verified','same_147_raw_configuration_and_E0_words_verified','same_right_factor_and_original_coordinate_scale_verified','new_eL_copied_from_fresh139_literal142_bridge','callbacks_publish_completed_operands_without_mutation'):
  assert admission[n] is True,n
 assert admission['uniform_adjoint_or_global_inverse_qualified'] is admission['physical_adoption'] is False
 assert callable(complete_stage) and P.LINEAR_TOL==1e-10
 rhs=same_geometry_adjoint_pair(tuple(a.copy() for a in rhs_new),keep,label+'_NEW_eL');start=same_geometry_adjoint_pair(tuple(a.copy() for a in lambda_old),keep,label+'_old_lambda_warm_seed');action=same_geometry_adjoint_pair(tuple(a.copy() for a in action_old),keep,label+'_saved244_action_of_old_lambda')
 reference=mechanical_adjoint_reference(rhs,original_scale,keep,label+'_NEW_source_reference')
 residual=same_geometry_adjoint_pair(P.a_sub(rhs,action),keep,label+'_NEW_total_residual_from_saved_action');scores=mechanical_adjoint_scores(residual,reference,keep,label+'_NEW_initial_source_relative')
 current=dict(action=action,residual=residual,scores=scores,admitted=bool(np.all(scores<=P.LINEAR_TOL)))
 bound=None
 if old_positive is not None:
  assert admission['old_positive_bound_at_exact_warm_lambda_verified'] is True and admission['old_positive_record']
  bound=np.asarray(old_positive).copy();keep(label+'_saved_unsigned244_bound_at_old_lambda',bound.copy());assert bound.shape==(403340,) and bound.dtype==np.float64 and np.all(np.isfinite(bound)) and np.all(bound>=0)
 ref=complete_stage('WARMSTART_CONTEXT',dict(lambda_hi=start[0],lambda_lo=start[1],saved_action_hi=action[0],saved_action_lo=action[1],rhs_hi=rhs[0],rhs_lo=rhs[1],residual_hi=residual[0],residual_lo=residual[1],scores=scores.copy(),original_scale=original_scale.copy(),**({} if bound is None else dict(saved_positive=bound))),dict(old_solution=admission['old_solution_record'],fresh_eL=admission['new_eL_record'],old_source_rows_admitted=admission['old_source_rows_admitted'],NEW_initial_source_rows_admitted=current['admitted'],old_action_or_factor_replayed=False,old_basis_not_reused=True,physical_adoption=False));assert ref
 return dict(start=start,rhs=rhs,current=current,reference=reference,saved_positive=bound,context=ref,admission=admission,new_RHS_basis_required=not current['admitted'],physical_adoption=False)


def same_geometry_adjoint_warmstart_response(packet,right_adjoint,action_star,positive_star,keep,label,complete_stage):
 assert not SAME_GEOMETRY_ADJOINT_AUTHOR_DRAFT and P.LINEAR_TOL==1e-10 and all(callable(f) for f in (right_adjoint,action_star,positive_star,complete_stage))
 admission=packet['admission'];assert admission['operator']=='represented_directed_original244_coefficient_Astar' and admission['physical_adoption'] is False
 if not packet['current']['admitted']:assert packet['saved_positive'] is not None,'Retrieve earned old-lambda unsigned bound before new candidate construction; do not replay it'
 stages=[]
 def stage(role,data,metadata):
  ref=complete_stage(role,data,dict(metadata,context=packet['context'],operator='represented_coefficient_Astar',new_eL_reference=True,physical_adoption=False));assert ref;stages.append(ref);return ref
 def right(x,tag):
  y=same_geometry_adjoint_pair(right_adjoint(x,tag),keep,tag+'_NEW_right_output');stage('NEW_RIGHT_ADJOINT',dict(input_hi=x[0],input_lo=x[1],output_hi=y[0],output_lo=y[1]),dict(old_basis_or_right_application_replayed=False));return y
 def action(x,tag):
  y=same_geometry_adjoint_pair(action_star(x,tag),keep,tag+'_NEW244_action');stage('NEW_ASTAR_WEAK',dict(input_hi=x[0],input_lo=x[1],output_hi=y[0],output_lo=y[1]),dict(total_or_direction_action_owns_its_argument=True));return y
 def positive(x,tag):
  same=all(np.array_equal(x[w].view(np.uint64),packet['start'][w].view(np.uint64)) for w in (0,1))
  e=packet['saved_positive'].copy() if same and packet['saved_positive'] is not None else np.asarray(positive_star(x,tag)).copy()
  keep(tag+'_completed_unsigned_bound',e.copy());assert e.shape==(403340,) and e.dtype==np.float64 and np.all(np.isfinite(e)) and np.all(e>=0)
  stage('ASTAR_POSITIVE',dict(input_hi=x[0],input_lo=x[1],envelope=e),dict(earned_exact_warm_argument_bound_reused=bool(same),coefficient_scope_only=True));return e
 def identity(x,tag):return same_geometry_adjoint_pair(tuple(a.copy() for a in x),keep,tag+'_original_identity_left')
 def scores(x,tag):return mechanical_adjoint_scores(x,packet['reference'],keep,tag)
 def progress(i,nodes,after,increment):
  stage('CANDIDATE',dict(lambda_hi=nodes[0],lambda_lo=nodes[1],action_hi=after['action'][0],action_lo=after['action'][1],residual_hi=after['residual'][0],residual_lo=after['residual'][1],increment_hi=increment[0],increment_lo=increment[1],scores=after['scores'].copy()),dict(iteration=i,admitted=after['admitted'],total_lambda_not_correction_owns_certificate=True))
 def checkpoint(i,v,small):
  same_geometry_adjoint_pair(v,keep,label+'_completed_NEW_basis');assert small['column_action_scopes']==['authoritative']*i
  stage('ITERATION_STATE',dict(basis_hi=v[0],basis_lo=v[1],**{n:np.asarray(small[n]) for n in ('H_hi','H_lo','R','Givens_cos','Givens_sin','rotated_RHS','initial_norm','history','Arnoldi_contact_norms','Arnoldi_operation_bounds')}),dict(iteration=i,next_iteration=i,cap=80,column_action_scopes=['represented_coefficient_Astar']*i,reason=small['reason'],old_RHS_prefix_not_imported=True))
 nodes,after,increment,history=native_metric_gmres_solve(packet['start'],packet['current'],packet['rhs'],right,identity,action,positive,scores,label,80,progress,None,action,action,checkpoint)
 final=mechanical_adjoint_scores(after['residual'],packet['reference'],keep,label+'_NEW_final_source_relative');assert np.array_equal(final.view(np.uint64),after['scores'].view(np.uint64))
 history=dict(history);generic=history.pop('single_original_action_Arnoldi_relation_qualified',False);history.pop('original_six_rows_admitted',None)
 history['generic_same_callback_Arnoldi_bookkeeping']=generic;history['fresh_total_action_evaluated']=history['iterations']>0
 history['represented_coefficient_acceptance_action_used']=history.pop('authoritative_acceptance_action_used',False)
 history['column_action_scopes']=['represented_coefficient_Astar']*history['iterations'];history['recurrence_action_scope']='represented_coefficient_Astar';history['acceptance_scope']='same represented244 total-lambda action and NEW53 source-relative rows'
 if history['reason']=='original_six_rows_admitted':history['reason']='NEW_source_relative_adjoint_rows_admitted'
 if history['reason']=='already_original_rows_admitted':history['reason']='already_NEW_source_relative_adjoint_rows_admitted'
 history.update(operator='represented_directed_original244_coefficient_Astar',source_relative_adjoint_rows_admitted=bool(np.all(final<=1e-10)),warm_start=True,new_rhs=True,restarts=0,new_cycle_cap=80,old_rhs_iterations_not_relabelled=True,old_basis_actions_or_factors_replayed=False,old_action_at_warm_lambda_reused=True,exact_DD_superposition_assumed=False,original147_or_forward_physical_rows_tested=False,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False)
 stage('SOLUTION',dict(lambda_hi=nodes[0],lambda_lo=nodes[1],action_hi=after['action'][0],action_lo=after['action'][1],residual_hi=after['residual'][0],residual_lo=after['residual'][1],increment_hi=increment[0],increment_lo=increment[1],scores=final),dict(history=history,NEW_RHS_feedback_admission=history['source_relative_adjoint_rows_admitted'],phase_or_gauge_feedback_evaluated=False))
 return nodes,after,increment,dict(history,new_stage_refs=stages,normal_feedback_or_physical_adoption=False)
