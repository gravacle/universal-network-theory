"""HELD finite phase update after a CLOSED admitted NEW candidate response.
Definitions only. Globals np/P/json/math/thin, bind/bind_record, reviewed143
candidate_phase_response_admission,100 ownership validator,116 constants/current
and fy_keep. The containing root namespace supplies exact-exponent arithmetic,
fs/fy helpers, read_closed/seal_completed/clear_completed and finite-first keep.
No225/160/EOS/current/mass/solver replay: only NEW116 at the changed phase state.
"""
FINITE_PHASE_AUTHOR_DRAFT=True
FINITE_PHASE_AUTHORING_IN_PROGRESS=False
PREPARATION_SOURCE=(None,None)
PREPARATION_RESULT=(None,None,'COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARED_UNQUALIFIED')
PREPARATION_RECEIPT=(None,None,'CLOSED')
PREPARATION_CLOSURE_PROOF=(None,None,None)
RESPONSE_SOURCE=(None,None)
RESPONSE_RESULT=(None,None,'CANDIDATE_LITERAL_PHASE_LINEAR_RESPONSE_ADMITTED')
RESPONSE_RECEIPT=(None,None,'CLOSED')
RESPONSE_CLOSURE_PROOF=(None,None,None)


def candidate_finite_phase_admission():
 assert not FINITE_PHASE_AUTHOR_DRAFT and not FINITE_PHASE_AUTHORING_IN_PROGRESS
 assert all(x is not None for r in (PREPARATION_SOURCE,PREPARATION_RESULT,PREPARATION_RECEIPT,PREPARATION_CLOSURE_PROOF,RESPONSE_SOURCE,RESPONSE_RESULT,RESPONSE_RECEIPT,RESPONSE_CLOSURE_PROOF) for x in r),'Future admitted CLOSED phase response and preparation required'
 prepared=candidate_phase_response_admission()
 for ref in (RESPONSE_SOURCE,RESPONSE_RESULT,RESPONSE_RECEIPT,RESPONSE_CLOSURE_PROOF):bind(ref[0],ref[1])
 r=json.loads(P.path(RESPONSE_RESULT[0]).read_text());rc=json.loads(P.path(RESPONSE_RECEIPT[0]).read_text());proof=json.loads(P.path(RESPONSE_CLOSURE_PROOF[0]).read_text());stem=RESPONSE_RESULT[0].removesuffix('_RESULT.json')
 assert r['status']==RESPONSE_RESULT[2] and rc['status']==RESPONSE_RECEIPT[2] and rc['result_sha256']==RESPONSE_RESULT[1] and rc['error_sha256'] is None
 assert r['owner']==rc['owner']==proof['owner'] and r['owner']['source_sha256']==proof['source_sha256']==RESPONSE_SOURCE[1]
 assert proof['status']==RESPONSE_CLOSURE_PROOF[2] and proof['result_sha256']==RESPONSE_RESULT[1] and proof['receipt_sha256']==RESPONSE_RECEIPT[1] and proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_success_role_seals_verified'] is True
 assert r['qualification']==rc['qualification'] and all(x is False for x in r['qualification'].values()) and not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 case=r['case'];assert case['response_admitted'] is True and case['original_literal_weak_charge_unchanged'] is True and case['finite_phase_charge_restored'] is False and case['configuration_updated'] is False and case['physical_adoption'] is False
 assert case['preparation']==thin(prepared['preparation']) and case['input']['metadata']['preparation']==thin(prepared['preparation']) and case['input']['metadata']['current']==thin(prepared['current']) and case['input']['metadata']['basis']==thin(prepared['basis']) and case['input']['metadata']['prior_literal_weak_charge']==thin(prepared['prior'])
 assert case['solution']['metadata']['input']==thin(case['input']) and case['rate_jets']['metadata']['solution']==thin(case['solution']) and case['solution']['metadata']['response_admitted'] is True and case['rate_jets']['metadata']['response_admitted'] is True
 ratios=np.asarray(case['original_raw_scaled_ratios']);assert ratios.shape==(2,) and np.all(np.isfinite(ratios)) and np.all(ratios<=1e-10) and case['solution']['metadata']['original_raw_scaled_tolerance']==1e-10
 for ref in r['checkpoints']:
  bound=bind_record(ref);assert bound==ref and ref['metadata']['owner']==r['owner'] and ref['metadata']['failed'] is False
  assert rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
 assert case['input'] in r['checkpoints'] and case['solution'] in r['checkpoints'] and case['rate_jets'] in r['checkpoints']
 columns=[];original_input=None
 for iq,phase_ref in enumerate(prepared['columns']):
  provenance=phase_ref['metadata']['candidate_provenance'];state=bind_record(provenance['state']);original=bind_record(provenance['input'])
  assert state['metadata']['column']==iq and state['metadata']['physical_adoption'] is False and phase_ref['metadata']['EOS_or_phase_current_replayed'] is False
  if original_input is None:original_input=original
  else:assert original==original_input
  ownership=finite0_validate_saved_transaction_ownership(original['metadata'],state['metadata'],prepared['result']['case']['candidate_source']);assert ownership==provenance['ownership']
  columns.append(dict(state=state,phase=phase_ref,candidate_provenance=provenance))
 return dict(prepared=prepared,columns=columns,original_input=original_input,input=case['input'],solution=case['solution'],rate_jets=case['rate_jets'],response_source=dict(source=RESPONSE_SOURCE,result=RESPONSE_RESULT,receipt=RESPONSE_RECEIPT,proof=RESPONSE_CLOSURE_PROOF,owner=r['owner']),physical_adoption=False)


def finite_phase_pair(data,name,shape,keep,label):
 pair=(data[name+'_hi'].copy(),data[name+'_lo'].copy());keep(label+'_both_words',np.stack(pair).copy())
 assert all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in pair);fy_keep(label,pair,keep);return pair


def finite_phase_state_names(schema):
 names=tuple('completed_candidate_s_'+n for n in ('hi','P','phi','U','uc'))+tuple('completed_candidate_c_'+n for n in ('N','sqrt_h','ih','u'))
 assert all(schema[n]['dtype']=='float64' and schema[n]['finite'] is True for n in names);return names


def finite_phase_add_retaining_defect(old,increment,keep,label):
 fy_keep(label+'_before',old,keep);fy_keep(label+'_increment',increment,keep);new=P.a_add(old,increment);fy_keep(label+'_updated',new,keep)
 words=[]
 for ordinal,term in enumerate((old[0],old[1],increment[0],increment[1],-new[0],-new[1])):
  accumulator=term;next_words=[]
  for word in words:accumulator,low=P.a_sum(accumulator,word);next_words.append(low)
  words=next_words+[accumulator];keep(label+'_exact_addition_step%d'%ordinal,np.stack(words).copy())
 expansion=keep(label+'_exact_six_word_addition_defect',np.stack(words).copy());return new,expansion


def evaluate_candidate_finite_phase_update(admitted,read_closed,seal_completed,clear_completed,keep,label,baseline_mixed=None):
 assert not FINITE_PHASE_AUTHOR_DRAFT and not FINITE_PHASE_AUTHORING_IN_PROGRESS and admitted['physical_adoption'] is False
 assert admitted['response_source']['source']==RESPONSE_SOURCE and admitted['response_source']['result']==RESPONSE_RESULT and admitted['response_source']['receipt']==RESPONSE_RECEIPT and admitted['response_source']['proof']==RESPONSE_CLOSURE_PROOF
 prepared=admitted['prepared'];cache_words=read_closed(prepared['preparation'],tuple('candidate_phase_mass_candidate_'+n+'_'+w for n in ('H','current_point_density') for w in ('hi','lo')));cached_H=finite_phase_pair(cache_words,'candidate_phase_mass_candidate_H',(15136,),keep,label+'_unchanged_prepared_H');cached_p=finite_phase_pair(cache_words,'candidate_phase_mass_candidate_current_point_density',(15136,),keep,label+'_unchanged_prepared_p');basis=read_closed(prepared['basis'],('R','dv','hats'));jet_data=read_closed(admitted['rate_jets'],tuple(n+'_'+w for n in ('value','R','Z') for w in ('hi','lo')))
 jets={n:finite_phase_pair(jet_data,n,(15136,),keep,label+'_admitted_response_'+n) for n in ('value','R','Z')}
 response=read_closed(admitted['solution'],('completed_original_mass_action_hi','completed_original_mass_action_lo','completed_certificate_residual_hi','completed_certificate_residual_lo','NEW_candidate_phase_response_new_phase_positive_scale'))
 linear_action=finite_phase_pair(response,'completed_original_mass_action',(87,45),keep,label+'_saved_admitted_linear_action');linear_residual=finite_phase_pair(response,'completed_certificate_residual',(87,45),keep,label+'_saved_admitted_linear_residual');scale=keep(label+'_saved_original_positive_phase_scale',response['NEW_candidate_phase_response_new_phase_positive_scale'].copy());assert scale.shape==(3870,) and np.all(np.isfinite(scale)) and np.all(scale>0)
 current=read_closed(prepared['current'],tuple(n+'_'+w for n in ('copied_completed_original_fixed_literal_weak_phase_charge','copied_completed_value_literal_phase_current') for w in ('hi','lo')))
 target=finite_phase_pair(current,'copied_completed_original_fixed_literal_weak_phase_charge',(87,45),keep,label+'_unchanged_original_target');old_weak=finite_phase_pair(current,'copied_completed_value_literal_phase_current',(87,45),keep,label+'_saved_old_literal_weak')
 for n,a in basis.items():keep(label+'_unchanged_basis_'+n,a.copy())
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.count_nonzero(P.scalar_mask())==3870
 keep(label+'_original_admitted_response_tolerance',np.asarray(admitted['solution']['metadata']['original_raw_scaled_tolerance']));input_ref=seal_completed('PHASE_UPDATE_INPUT',dict(kind='closed_phase_response_and_fixed_candidate_sources',response=admitted['response_source'],rate_jets=thin(admitted['rate_jets']),solution=thin(admitted['solution']),preparation=thin(prepared['preparation']),basis=thin(prepared['basis']),original_input=thin(admitted['original_input']),prior_literal_weak_charge=thin(prepared['prior']),original_canonical_target_refs=admitted['original_input']['metadata']['refs']['canonical_columns'],unchanged_intrinsic_configuration=True,baseline_mixed_jets_supplied=baseline_mixed is not None,baseline_mixed_provenance=None if baseline_mixed is None else baseline_mixed['provenance'],physical_adoption=False));clear_completed()
 constants=candidate_phase_registered_constants(admitted['original_input']['metadata']['fixed']);parts=[];columns=[];records=[]
 for iq,source in enumerate(admitted['columns']):
  state=source['state'];raw=read_closed(state,finite_phase_state_names(state['metadata']['schema']));old=read_closed(source['phase'],tuple('copied_STATE_completed_phase_value_'+n+'_'+w for n in ('p','H') for w in ('hi','lo')))
  for n,a in raw.items():keep(label+'_column%d_saved_'%iq+n,a.copy())
  s={n:P.a_dd(raw['completed_candidate_s_'+n]) for n in ('hi','P','phi','U','uc')};c={n:P.a_dd(raw['completed_candidate_c_'+('sqrt_h' if n=='mu' else n)]) for n in ('N','mu','ih','u')};p=3784;selection=slice(iq*p,(iq+1)*p)
  old_p=finite_phase_pair(old,'copied_STATE_completed_phase_value_p',(p,),keep,label+'_column%d_old_p'%iq);old_H=finite_phase_pair(old,'copied_STATE_completed_phase_value_H',(p,),keep,label+'_column%d_old_H'%iq)
  assert all(np.array_equal(a,b[selection]) for supplied,cached in ((old_p,cached_p),(old_H,cached_H)) for a,b in zip(supplied,cached)),'Completed phase-column words must match prepared H/current exactly'
  increment=P.a_dd(np.zeros((p,4)))
  for word in (0,1):increment[word][:,0]=jets['value'][word][selection]
  changed,addition=finite_phase_add_retaining_defect(s['phi'],increment,keep,label+'_column%d_phase_covector'%iq);assert all(np.array_equal(a[:,1:],b[:,1:]) for a,b in zip(changed,s['phi']));s['phi']=changed
  direction={n:P.a_dd(np.zeros_like(x[0])) for n,x in {**s,**c}.items()};direction['phi']=increment
  mixed={n:tuple(a[selection].copy() for a in jets[n]) for n in ('R','Z')}
  for n,x in mixed.items():fy_keep(label+'_column%d_mixed_increment_'%iq+n,x,keep)
  if baseline_mixed is not None:
   assert baseline_mixed['provenance'] and set(baseline_mixed['jets'])=={'R','Z'}
   for n,x in mixed.items():
    base=tuple(a[selection].copy() for a in baseline_mixed['jets'][n]);total,defect=finite_phase_add_retaining_defect(base,x,keep,label+'_column%d_total_mixed_'%iq+n);mixed[n]=total
  eos=candidate_invariant_phase_eos_current(s,c,direction,constants,keep,label+'_column%d_NEW_invariant'%iq)
  linear=P.a_mul(old_H,tuple(a[:,0] for a in increment));fy_keep(label+'_column%d_NEW_old_H_times_step_diagnostic'%iq,linear,keep)
  remainder=P.a_sub(P.a_sub(eos['value']['p'],old_p),linear);fy_keep(label+'_column%d_finite_point_nonlinear_remainder'%iq,remainder,keep)
  H=eos['value']['H'];lower=H[0]-abs(H[1]);margin=lower-2e-11*eos['H_operation_envelope'];keep(label+'_column%d_NEW_H_lower'%iq,lower.copy());keep(label+'_column%d_NEW_H_resolved_margin'%iq,margin.copy())
  provenance=dict(source_candidate=source['candidate_provenance'],admitted_response=admitted['response_source'],geometry_policy='saved raw225 geometry pairs with zero low words; paired phase update retained',fresh_direction_scope='same temporal phase step only; all configuration directions zero',mixed_jet_scope='total with supplied authenticated baseline' if baseline_mixed is not None else 'response increments only; no baseline time jets invented; represented phase addition defects retained separately')
  record=seal_completed('FINITE_PHASE_COLUMN',dict(kind='NEW_phase_covector_invariant_EOS_literal_current_and_H',column=iq,input=thin(input_ref),state=thin(state),prior_phase=thin(source['phase']),candidate_provenance=provenance,strict_EOS_domain_passed=True,new_H_strictly_positive=bool(np.all(lower>0)),new_H_resolved_positive=bool(np.all(margin>0)),original_phase_targets_unchanged=True,normal_or_CMC_constraints_reevaluated=False,phase_charge_restoration_not_inferred=True,physical_adoption=False));records.append(thin(record));columns.append(dict(eos=eos,candidate_provenance=provenance,prior_literal_weak_charge=prepared['prior'],phi=changed,mixed_phase_jets=mixed,mixed_are_increments=baseline_mixed is None,phase_addition_defect=addition));parts.append(eos['value']['p']);clear_completed()
 point=P.a_reshape(P.a_stack(parts,0),(15136,));fy_keep(label+'_NEW_finite_literal_point_density',point,keep);new_weak=P.dd_scalar_scatter(point,basis,keep,label+'_NEW_finite_literal_weak');fy_keep(label+'_NEW_finite_literal_weak',new_weak,keep)
 residual=P.a_sub(target,new_weak);fy_keep(label+'_NEW_target_minus_finite_current',residual,keep);nonlinear=P.a_sub(P.a_sub(new_weak,old_weak),linear_action);fy_keep(label+'_weak_nonlinear_and_scatter_association_remainder',nonlinear,keep)
 prediction=P.a_sub(linear_residual,nonlinear);fy_keep(label+'_linear_residual_minus_weak_remainder',prediction,keep);fy_keep(label+'_finite_residual_identity_contact',P.a_sub(residual,prediction),keep)
 mask=P.scalar_mask();t=target[0][mask]+target[1][mask];r=residual[0][mask]+residual[1][mask];norms=keep(label+'_target_and_NEW_residual_raw_scaled_norms',np.asarray((np.linalg.norm(t),np.linalg.norm(t/scale),np.linalg.norm(r),np.linalg.norm(r/scale))))
 exact_target_zero=all(np.all(a[mask]==0) for a in target);exact_residual_zero=all(np.all(a[mask]==0) for a in residual)
 if norms[0]>0 and norms[1]>0:
  ratios=keep(label+'_descriptive_original_target_raw_scaled_ratios',np.asarray((norms[2]/norms[0],norms[3]/norms[1])));scores=ratios.tolist();score_scope='descriptive target-normalized finite residual only; no acceptance inferred'
 elif exact_target_zero:
  scores=[0.,0.] if exact_residual_zero else [None,None];score_scope='zero target has undefined relative ratio; exact two-word zero residual fallback only'
 else:
  scores=[None,None];score_scope='collapsed zero target norm with nonzero original words; no finite certificate inferred'
 readout=seal_completed('FINITE_PHASE_CURRENT',dict(kind='NEW_finite_literal_weak_charge_and_nonlinear_residual_only',input=thin(input_ref),columns=records,unchanged_target=thin(prepared['prior']),target_relative_ratio_undefined=exact_target_zero,exact_two_word_residual_zero=exact_residual_zero,target_residual_raw_scaled_norms=norms.tolist(),descriptive_original_raw_scaled_ratios=scores,ratio_scope=score_scope,charge_target_words_unchanged=True,weak_remainder_includes_scatter_and_phase_addition_defects=True,finite_charge_admission_performed=False,new_phase_mass_diagonal_not_constructed=True,normal_CMC_mechanical_current_or_evolution_not_replayed=True,physical_adoption=False));clear_completed()
 return dict(columns=columns,new_point_density=point,new_weak_current=new_weak,target=target,residual=residual,weak_nonlinear_remainder=nonlinear,column_records=records,current_record=thin(readout),linear_response_admitted=True,finite_phase_charge_restored=False,physical_adoption=False)
