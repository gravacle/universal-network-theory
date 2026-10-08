"""HELD NEW represented coefficient A* e_L response; definitions only.
Globals np,P,keep and unchanged117 paired GMRES helpers. No physical norm,
forward error, symmetry, global inverse or all-direction adjoint is inferred.
The fixed saved positive coordinate scale weights this NEW residual by r/s.
"""
MECHANICAL_ADJOINT_AUTHOR_DRAFT=True
MECHANICAL_ADJOINT_AUTHORING_IN_PROGRESS=False

def mechanical_adjoint_reference(rhs,scale,keep,label):
 assert rhs[0].shape==rhs[1].shape==scale.shape==(403340,)
 native_metric_gmres_put(label+'_both_word_eL',rhs);keep(label+'_original_positive_coordinate_scale',scale.copy())
 assert scale.dtype==np.float64 and np.all(np.isfinite(scale)) and np.all(scale>0)
 reference={};groups=(('native',slice(0,380292)),('metric',slice(380292,None)),('packed',slice(None)))
 scaled=P.a_div64(rhs,scale,keep,label+'_source_coordinate_division');native_metric_gmres_put(label+'_scaled_source',scaled)
 for name,selection in groups:
  words=tuple(a[selection].copy() for a in rhs);zero=bool(all(np.all(a==0) for a in words));norms=[]
  for version,pair in (('raw',words),('scaled',tuple(a[selection].copy() for a in scaled))):
   native_metric_gmres_put(label+'_'+name+'_'+version+'_source_words',pair)
   value=native_metric_gmres_norm(pair,label+'_'+name+'_'+version+'_source_norm')
   assert np.isfinite(value) and (value==0 if zero else value>0),'Nonzero source cannot acquire an unresolved zero norm'
   norms.append(value)
  reference[name]=dict(zero_source_both_words=zero,norms=tuple(norms),selection=selection)
 return dict(groups=reference,scale=scale.copy(),source=tuple(a.copy() for a in rhs),relative_reference_is_NEW_eL=True,physical_norm_or_forward_error_qualified=False)

def mechanical_adjoint_scores(res,reference,keep,label):
 assert res[0].shape==res[1].shape==(403340,);native_metric_gmres_put(label+'_residual_words',res)
 scaled=P.a_div64(res,reference['scale'],keep,label+'_residual_coordinate_division');native_metric_gmres_put(label+'_scaled_residual',scaled)
 scores=np.zeros((3,2));absolute=np.zeros((3,2));zero_flags=[];undefined=[]
 for row,name in enumerate(('native','metric','packed')):
  ref=reference['groups'][name];selection=ref['selection'];words=tuple(a[selection].copy() for a in res);zero=bool(all(np.all(a==0) for a in words));zero_flags.append(zero);undefined.append(ref['zero_source_both_words'])
  for column,(version,pair) in enumerate((('raw',words),('scaled',tuple(a[selection].copy() for a in scaled)))):
   native_metric_gmres_put(label+'_'+name+'_'+version+'_residual_words',pair)
   value=native_metric_gmres_norm(pair,label+'_'+name+'_'+version+'_residual_norm');absolute[row,column]=value
   assert np.isfinite(value) and (value==0 if zero else value>0),'Unresolved nonzero residual norm refuses'
   scores[row,column]=(0. if zero else 1.) if ref['zero_source_both_words'] else value/ref['norms'][column]
   keep(label+'_completed_absolute_norms_partial',absolute.copy());keep(label+'_completed_admission_scores_partial',scores.copy())
 keep(label+'_absolute_raw_and_scaled_norms',absolute.copy());keep(label+'_source_norms',np.asarray([reference['groups'][n]['norms'] for n in ('native','metric','packed')]))
 keep(label+'_relative_ratio_undefined_zero_sources',np.asarray(undefined,dtype=np.bool_));keep(label+'_exact_both_word_zero_residuals',np.asarray(zero_flags,dtype=np.bool_));keep(label+'_admission_scores',scores.copy())
 assert np.all(np.isfinite(scores)) and np.all(scores>=0)
 return scores

def candidate_right_only_mechanical_adjoint_gmres(rhs,right_adjoint,action_star,positive_star,scores,admission,keep,label,cap=80,progress=None):
 assert not MECHANICAL_ADJOINT_AUTHOR_DRAFT and not MECHANICAL_ADJOINT_AUTHORING_IN_PROGRESS and cap==80
 assert admission['closed_provenance'] and admission['same_updated_candidate_and_original_coordinates'] is True and admission['two_selected_fullweak_transpose_contacts_passed'] is True
 assert admission['literal_eL_both_words_copied'] is True and admission['active_signed_nodal_factor_and_adjoint_controls_passed'] is True and admission['source_relative_adjoint_certificates_declared'] is True
 assert admission['uniform_adjoint_or_global_inverse_qualified'] is admission['physical_adoption'] is False
 start=native_metric_gmres_put(label+'_exact_zero_start',P.a_dd(np.zeros(403340)));zero=native_metric_gmres_put(label+'_exact_homogeneous_coefficient_transpose_at_zero',P.a_dd(np.zeros(403340)))
 initial=scores(rhs,label+'_initial_source_relative_scores');current=dict(action=zero,residual=rhs,scores=initial,admitted=bool(np.all(initial<=P.LINEAR_TOL)))
 def forward(x,tag):return right_adjoint(x,tag)
 def identity(x,tag):return native_metric_gmres_put(tag+'_identity_left_both_words',tuple(a.copy() for a in x))
 nodes,after,increment,history=native_metric_gmres_solve(start,current,rhs,forward,identity,action_star,positive_star,scores,label,cap,progress)
 history.update(operator='represented_directed_original244_coefficient_Astar',preconditioning='right_signed_nodal110_adjoint_identity_left',warm_start=False,restarts=0,original_forward_canonical_gates_tested=False,forward_error_or_global_inverse_qualified=False,physical_adoption=False)
 return nodes,after,increment,history
