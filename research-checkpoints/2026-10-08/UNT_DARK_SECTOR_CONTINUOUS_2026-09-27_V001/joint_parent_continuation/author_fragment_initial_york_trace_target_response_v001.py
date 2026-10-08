"""Definitions only: new zero-native-source target response and original certificates.
Globals np/P/R/keep/pair_keep/math are supplied by a guarded caller.
The frozen signed action generates one numerical approximate inverse only;
current literal action admission is a separate post-solve original-row test.
"""

def trace_target_reference_scores(residual,native_reference,canonical_reference,metric_reference,scales,label):
 fields=P.fields_from_pair(residual,label+'_norm_only_residual');rows=[];norms=[];zero=[]
 for role,value,reference,scale in (('native_original_affine',fields[0],native_reference,scales[0]),('native_original_canonical',fields[0],canonical_reference,scales[0]),('metric_NEW_target',fields[1],metric_reference,scales[1])):
  raw=float(np.linalg.norm(value));white=float(np.linalg.norm(value/scale));den=float(np.linalg.norm(reference));wd=float(np.linalg.norm(reference/scale))
  assert all(math.isfinite(t) for t in (raw,white,den,wd)) and (den>0)==(wd>0)
  norms.append((raw,white,den,wd,P.LINEAR_TOL*den,P.LINEAR_TOL*wd));zero.append(den==0)
  # A zero fixed reference requires exact zero; score1 denotes a refused flag,
  # never a fabricated relative denominator. Normal production refs are nonzero.
  row=np.array((raw/den,white/wd)) if den>0 else np.array((0.,0.) if raw==white==0 else (1.,1.))
  rows.append(row);keep(label+'_'+role+'_absolute_norms_references_thresholds',np.asarray(norms[-1]));keep(label+'_'+role+'_admission_scores',row)
 scores=np.stack(rows);keep(label+'_original_admission_scores',scores);keep(label+'_zero_reference_flags',np.asarray(zero,dtype=bool))
 return scores,np.asarray(norms),zero

def trace_target_frozen_approximate_inverse(rhs,b,d,g,scales,native_reference,canonical_reference):
 # One NEW RHS, one160 cap. No old initial rates/solves/controls are repeated.
 reference=P.fields_from_pair(rhs,'NEW_trace_target_norm_reference');metric_reference=reference[1]
 assert np.all(reference[0]==0) and np.linalg.norm(metric_reference)>0
 scale=P.pack_fields(scales[0],scales[1]);keep('NEW_trace_target_positive_congruence',scale);assert np.all(scale>0)
 bound=[]
 for ref,s in ((native_reference,scales[0]),(canonical_reference,scales[0]),(metric_reference,scales[1])):
  raw=float(np.linalg.norm(ref));white=float(np.linalg.norm(ref/s));assert raw>0 and white>0
  bound.extend((raw/float(np.max(s)),white))
 recurrence_rhs=P.collapse(rhs,'NEW_trace_target_recurrence_rhs');pair_keep('NEW_trace_target_recurrence_rhs_rounding_defect',P.a_sub(rhs,P.a_dd(recurrence_rhs)))
 wn=float(np.linalg.norm(recurrence_rhs/scale));sufficient=P.LINEAR_TOL*min(bound);tolerance=sufficient/wn
 keep('NEW_trace_target_sufficient_absolute_white_target',np.asarray(sufficient));keep('NEW_trace_target_recurrence_relative_target',np.asarray(tolerance));assert math.isfinite(tolerance) and tolerance>0
 start=P.a_dd(np.zeros(403340));pair_keep('NEW_trace_target_zero_response_start',start)
 def action(delta):
  v,k,_=P.unpack_fields(delta,False);n,m=P.coupled_action(v,k,b,d,g);out=P.pack_fields(n,m);keep('NEW_trace_target_latest_frozen_recurrence_action',out);assert np.all(np.isfinite(out));return out
 def certificate(delta):
  nodes,q=P.dd_node_update(start,delta,keep,'NEW_trace_target_candidate_update');a=P.dd_node_original_action(nodes,b,d,g,keep);pair_keep('NEW_trace_target_candidate_frozen_action',a)
  res=P.a_sub(rhs,a);pair_keep('NEW_trace_target_candidate_frozen_residual',res);scores,norms,zero=trace_target_reference_scores(res,native_reference,canonical_reference,metric_reference,scales,'NEW_trace_target_candidate_frozen')
  return P.collapse(res,'NEW_trace_target_candidate_frozen_residual_readout'),scores
 delta,scores,ok,reason=P.minres_core(action,recurrence_rhs,scale,tolerance,certificate,'NEW_trace_target_frozen_approximate_inverse',cap=160);keep('NEW_trace_target_completed_float_correction',delta);keep('NEW_trace_target_frozen_solver_return_scores',scores)
 nodes,q=P.dd_node_update(start,delta,keep,'NEW_trace_target_final_update');a=P.dd_node_original_action(nodes,b,d,g,keep);pair_keep('NEW_trace_target_final_frozen_action',a)
 res=P.a_sub(rhs,a);pair_keep('NEW_trace_target_final_frozen_residual',res);scores,norms,zero=trace_target_reference_scores(res,native_reference,canonical_reference,metric_reference,scales,'NEW_trace_target_final_frozen')
 da=P.dd_node_original_action(P.a_dd(delta),b,d,g,keep);pair_keep('NEW_trace_target_completed_correction_action',da);qa=P.dd_node_original_action(P.a_dd(q),b,d,g,keep);pair_keep('NEW_trace_target_third_word_action',qa)
 predicted=P.shifted_residual_with_update_defect(rhs,da,qa);pair_keep('NEW_trace_target_shift_prediction',predicted);gap=P.a_sub(res,predicted);pair_keep('NEW_trace_target_shift_identity_gap',gap)
 bound=2*(abs(rhs[0])+abs(rhs[1]))
 for role,x in (('new',nodes),('correction',P.a_dd(delta)),('third_word',P.a_dd(q))):bound+=P.node_positive_envelope(x,b,d,g,'NEW_trace_target_'+role);keep('NEW_trace_target_update_envelope_through_'+role,bound)
 actual=np.array([np.linalg.norm(x) for x in P.fields_from_pair(gap,'NEW_trace_target_update_norm')[:2]]);envelope=np.array([np.linalg.norm(x) for x in P.unpack_fields(bound,False)[:2]])
 P.check('NEW_trace_target_paired_approximation_update_with_third_word',actual,np.zeros(2),envelope)
 return nodes,a,res,scores,dict(cap=160,cycles=1,reason=reason,frozen_solver_callback_admitted=bool(ok),frozen_original_reference_scores=scores.tolist(),absolute_residual_reference_thresholds=norms.tolist(),frozen_action_is_numerical_approximation_only=True,literal_original_response_admitted=False),metric_reference

def fresh_trace_target_zero_native_control():
 # NEW indefinite coupled action, exactly zero native source, independent x=(1,-2).
 A=np.asarray(((2.,1.),(1.,-1.)));rhs=np.asarray((0.,3.));target=np.asarray((1.,-2.));scale=np.asarray((2.,3.));refs=np.asarray((1.,2.,3.))
 for n,x in (('A',A),('rhs',rhs),('target',target),('scale',scale),('fixed_nonzero_references',refs)):keep('fresh_zero_native_'+n,x)
 start=P.a_dd(np.zeros(2));pair_keep('fresh_zero_native_start',start)
 def original(delta):
  nodes,q=P.dd_node_update(start,delta,keep,'fresh_zero_native_update');a=P.a_matvec(A,nodes);pair_keep('fresh_zero_native_current_action',a);res=P.a_sub(P.a_dd(rhs),a);pair_keep('fresh_zero_native_current_residual',res)
  r=res[0]+res[1];scores=np.stack((P.original_ratios(r[:1],refs[:1],scale[:1]),P.original_ratios(r[:1],refs[1:2],scale[:1]),P.original_ratios(r[1:],rhs[1:],scale[1:])))
  keep('fresh_zero_native_current_reference_scores',scores);return r,scores
 def action(delta):return A@delta
 y,scores,ok,reason=P.minres_core(action,rhs,scale,1e-10*min(refs[0]/scale[0],refs[1]/scale[0],refs[2]/scale[1])/np.linalg.norm(rhs/scale),original,'fresh_zero_native_indefinite_response',cap=8)
 keep('fresh_zero_native_completed_correction',y);keep('fresh_zero_native_solver_return_scores',scores);nodes,q=P.dd_node_update(start,y,keep,'fresh_zero_native_final_update');res=P.a_sub(P.a_dd(rhs),P.a_matvec(A,nodes));pair_keep('fresh_zero_native_final_nodes',nodes);pair_keep('fresh_zero_native_final_residual',res)
 # A^2 has Gershgorin lower1, hence singular-value lower1: error<=norm(res).
 error=float(np.linalg.norm(nodes[0]+nodes[1]-target));rn=float(np.linalg.norm(res[0]+res[1]));rounding=64*np.finfo(float).eps*(np.linalg.norm(nodes[0])+np.linalg.norm(nodes[1])+np.linalg.norm(target)+np.linalg.norm(rhs));keep('fresh_zero_native_error_bound',np.asarray((error,rn,rounding)))
 mv=P.a_mul64(2.,P.a_slice(nodes,0));bk=P.a_slice(nodes,1);pair_keep('fresh_zero_native_uncancelled_Mv',mv);pair_keep('fresh_zero_native_uncancelled_Bk',bk)
 keep('fresh_zero_native_exact_zero_reference_decisions',np.asarray((0.==0.,not (1.==0.)),dtype=bool))
 P.check('fresh_coupled_zero_native_source_original_rows_and_independent_error_bound',np.asarray((float(ok),max(0.,error-rn-rounding))),np.asarray((1.,0.)),np.ones(2))
 return dict(kind='fresh_signed_coupled_zero_native_RHS_control',cap=8,reason=reason,original_scores=scores.tolist(),independent_singular_value_lower_bound=1.,zero_source_relative_ratio_defined=False,old_fixtures_or_fields_replayed=False)
