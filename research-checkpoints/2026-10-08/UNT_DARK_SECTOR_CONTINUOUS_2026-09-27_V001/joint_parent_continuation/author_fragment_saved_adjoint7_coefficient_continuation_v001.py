"""HELD explicit saved-seven-step represented coefficient Astar continuation.
Definitions only. Globals np,P,json,bind,keep and selected170/53 helpers are
containing-owned. No original action, factor, score-reference or prefix replay.
"""
ADJOINT7_CONTINUATION_AUTHOR_DRAFT=True
ADJOINT7_CONTINUATION_AUTHORING_IN_PROGRESS=False
ADJOINT7_PREFIX_SOURCE=('saved_original_mechanical_adjoint_gmres7_scalar_state_reconstruction_v002.py','f114fdb053170dd1be2e2040aa23a50d3eb1ae63d1d81af7aa022f216c1ba766')
ADJOINT7_PREFIX_RESULT=('SAVED_ORIGINAL_MECHANICAL_ADJOINT_GMRES7_SCALAR_STATE_RECONSTRUCTION_V002_RESULT.json','72a3b334235c93e0ab60902f1b14d27450efea60492cb12fa79b7e811392af3d','ORIGINAL_MECHANICAL_ADJOINT_GMRES7_SCALAR_STATE_RECONSTRUCTED')
ADJOINT7_PREFIX_RECEIPT=('SAVED_ORIGINAL_MECHANICAL_ADJOINT_GMRES7_SCALAR_STATE_RECONSTRUCTION_V002_RECEIPT.json','33ff7acbdd75c2dbb67909cec9ff0d160652ff02cbf277efe708d05f438b2502','CLOSED')
ADJOINT7_PREFIX_PROOF=('ROOT_NATURAL_CLOSED_ADJOINT7_SCALAR_RECOVERY_SUCCESS_SEALS_V001.json','d8e2a611bcaa80bdb2c3fa53bbe753e6a6c6d2b7a542d4366aaa5dd93afb92a7','ROOT_NATURAL_CLOSED_ADJOINT7_SCALAR_RECOVERY_SUCCESS_SEALS_VERIFIED')
ADJOINT7_ORIGINAL_SOURCE=('cross_u_candidate_right_only_mechanical_adjoint_response_v003.py','720ab9f4bad4a39a1c44e93acb22a8c4dd5ead032598503bec93774c6cab969b')
ADJOINT7_SELECTED_PINS={
 'author_fragment_native_metric_star_paired_gmres_resume_v002.py':'73b15a0e0512295aed41389a80c20ec6cf50ddef634497c805ada69c8ed738ee',
 'author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py':'25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c',
 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py':'3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871',
 'author_fragment_candidate_directed_nodal_factor_apply_v001.py':'4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b'}

def saved_adjoint7_prefix_admission():
 for q in (ADJOINT7_PREFIX_SOURCE,ADJOINT7_PREFIX_RESULT,ADJOINT7_PREFIX_RECEIPT,ADJOINT7_PREFIX_PROOF,ADJOINT7_ORIGINAL_SOURCE):bind(q[0],q[1])
 for n,h in ADJOINT7_SELECTED_PINS.items():bind(n,h)
 r=json.loads(P.path(ADJOINT7_PREFIX_RESULT[0]).read_text());rc=json.loads(P.path(ADJOINT7_PREFIX_RECEIPT[0]).read_text());pr=json.loads(P.path(ADJOINT7_PREFIX_PROOF[0]).read_text());case=r['case']
 assert r['status']==ADJOINT7_PREFIX_RESULT[2] and rc['status']=='CLOSED' and rc['result_sha256']==ADJOINT7_PREFIX_RESULT[1] and rc['error_sha256'] is None
 assert r['owner']==rc['owner']==pr['owner'] and r['owner']['pid']==57863 and r['owner']['source_sha256']==ADJOINT7_PREFIX_SOURCE[1]
 assert pr['status']==ADJOINT7_PREFIX_PROOF[2] and pr['source_sha256']==ADJOINT7_PREFIX_SOURCE[1] and pr['result_sha256']==ADJOINT7_PREFIX_RESULT[1] and pr['receipt_sha256']==ADJOINT7_PREFIX_RECEIPT[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==0 and pr['all_input_seals_verified'] is pr['all_success_role_seals_verified'] is True
 assert pr['success_roles']==18 and pr['selected_original_roles']==case['selected_original_roles']==23 and case['original_owner']==pr['original_failed_owner']
 assert case['original_owner']['pid']==37897 and case['original_owner']['source_sha256']==ADJOINT7_ORIGINAL_SOURCE[1] and case['original_natural_exit_code']==pr['original_exit_code']==1
 assert case['cap']==pr['cap']==80 and case['next_iteration']==pr['next_iteration']==7 and len(case['basis'])==8 and len(case['scalar_steps'])==7
 assert case['initial_and7next_basis_words_exact'] is pr['initial_and7next_basis_words_exact'] is True
 assert case['old_actions_factors_or_controls_replayed'] is pr['original_actions_factors_or_controls_replayed'] is False
 assert case['full_original_input_or_unused_archive_audit_claimed'] is pr['original_all550_inputs_or_all857_outputs_verified'] is False
 assert case['physical_adoption'] is case['original_forward_physical_six_gates_tested'] is case['source_relative_adjoint_gates_tested'] is False
 assert r['qualification']==rc['qualification']==pr['qualification'] and len(r['qualification'])==9 and all(v is False for v in r['qualification'].values())
 assert r['controls']==pr['new_construction_controls'] and len(r['controls'])==2 and all(q['passed'] is True and q['tolerance']==2e-11 for q in r['controls'])
 records={}
 for name,refs in (('context',[case['context']]),('basis',case['basis']),('resume_state',[case['resume_state']]),('earned_first_forward',[case['earned_first_forward']])):
  assert (refs if name=='basis' else refs[0])==pr[name]
  for ref in refs:
   bind(ref['commit_file'],ref['commit_sha256']);q=json.loads(P.path(ref['commit_file']).read_text());md=q['metadata']
   assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
   assert all(rc['output_sha256'][ref[f]]==ref[h] for f,h in (('file','sha256'),('commit_file','commit_sha256')))
   assert md['owner']==r['owner'] and md['failed'] is False and md['qualification']==r['qualification'];records[ref['file']]=md
 return dict(case=case,owner=r['owner'],records=records,prefix_proof=ADJOINT7_PREFIX_PROOF,original_owner=case['original_owner'],qualification=dict(r['qualification']))

def adjoint7_pair(x,keep,label):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 assert all(a.shape==(403340,) and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x),label
 for w,suffix in enumerate(('hi','lo')):keep(label+'_'+suffix,x[w].copy())
 return x

def prepare_saved_adjoint7_coefficient_continuation(admitted,read_record,complete_stage,keep,label):
 assert callable(read_record) and callable(complete_stage) and admitted['prefix_proof']==ADJOINT7_PREFIX_PROOF
 case=admitted['case'];records=admitted['records'];stage_refs=[]
 def load(ref):
  md=records[ref['file']];d=read_record(ref,tuple(md['schema']));assert set(d)==set(md['schema'])
  for n,a in d.items():
   keep(label+'_loaded_'+n,np.asarray(a).copy());s=md['schema'][n]
   assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=True) and a.dtype==np.float64 and np.all(np.isfinite(a)),n
  q=complete_stage('PREFIX_COPY',d,dict(source=ref,prefix_proof=ADJOINT7_PREFIX_PROOF,old_actions_or_factors_replayed=False));assert isinstance(q,dict) and q;stage_refs.append(q);return d,md
 cd,cm=load(case['context']);pair=lambda d,n:adjoint7_pair(tuple(d[n+'_'+w].copy() for w in ('hi','lo')),keep,label+'_'+n)
 start=pair(cd,'start');rhs=pair(cd,'rhs');current=dict(action=pair(cd,'current_action'),residual=pair(cd,'current_residual'),scores=cd['current_scores'].copy(),admitted=False)
 assert cm['source']['sha256']=='06457c58d751d9396b1f05209c94d32fba47f00bc4d436f401aff488cc8b731e' and cm['original_forward_physical_six_gates_tested'] is False
 assert all(np.all(a==0) for a in start+current['action']) and all(np.array_equal(rhs[w].view(np.uint64),current['residual'][w].view(np.uint64)) for w in (0,1))
 V=[]
 for j,ref in enumerate(case['basis']):
  d,md=load(ref);assert md['context']['basis']==j and md['factor_context']==cm['factor_context'];V.append(pair(d,'basis'))
 sd,sm=load(case['resume_state']);fd,fm=load(case['earned_first_forward'])
 assert sm['cap']==80 and sm['next_iteration']==sm['iterations']==7 and sm['basis']==case['basis'] and sm['earned_first_forward']==case['earned_first_forward']
 assert sm['column_action_scopes']==['represented_coefficient_Astar']*7 and sm['reason']=='explicit_cap'
 assert fm['exact_input_basis']==case['basis'][7] and fm['factor_context']==cm['factor_context']
 assert fm['must_return_once_after_exact_argument_context_match'] is True and fm['factor_application_replayed'] is False
 state=dict(sd,V=V,start=start,rhs=rhs,current=current,updated=start,after=dict(current),increment=(np.zeros(403340),np.zeros(403340)),prefix_proof=ADJOINT7_PREFIX_PROOF)
 for n in ('cap','iterations','next_iteration','reason','column_action_scopes','prefix_state_authenticated','original_associations_or_committed_state_verified','all_available_next_basis_words_matched','completed_actions_and_factors_not_replayed','original_rhs_warm_current_and_six_references_unchanged','original_right_and_left_maps_unchanged'):state[n]=sm[n]
 for n in ('updated_is_original_start','after_is_original_current','increment_is_original_zero_correction'):assert sm[n] is True,n
 state['initial_norm']=float(sd['initial_norm']);state['history']=sd['history'].tolist();state['Arnoldi_contact_norms']=sd['Arnoldi_contact_norms'].tolist();state['Arnoldi_operation_bounds']=sd['Arnoldi_operation_bounds'].tolist()
 scale=cd['NEW_adjoint_source_reference_original_positive_coordinate_scale'].copy();assert scale.shape==(403340,) and np.all(scale>0)
 reference=dict(groups={},scale=scale,source=rhs,relative_reference_is_NEW_eL=True,physical_norm_or_forward_error_qualified=False)
 for row,(name,selection) in enumerate((('native',slice(0,380292)),('metric',slice(380292,None)),('packed',slice(None)))):
  zero=bool(all(np.all(a[selection]==0) for a in rhs));norms=tuple(float(cd['NEW_adjoint_source_reference_'+name+'_'+version+'_source_norm_normalizing_norm']) for version in ('raw','scaled'))
  assert all(np.isfinite(v) and (v==0 if zero else v>0) for v in norms) and np.array_equal(np.asarray(norms).view(np.uint64),cd['cached_source_norms'][row].view(np.uint64))
  reference['groups'][name]=dict(zero_source_both_words=zero,norms=norms,selection=selection)
 assert np.array_equal(current['scores'],np.asarray([[0.,0.] if reference['groups'][n]['zero_source_both_words'] else [1.,1.] for n in ('native','metric','packed')]))
 return dict(state=state,reference=reference,first=pair(fd,'earned_solution'),first_ref=case['earned_first_forward'],factor_context=cm['factor_context'],context_ref=case['context'],original_owner=admitted['original_owner'],copy_refs=stage_refs,qualification=dict(admitted['qualification']))

def adjoint7_truthful_history(generic):
 assert generic['recurrence_action_scope']=='authoritative' and generic['column_action_scopes']==['authoritative']*generic['iterations'] and generic['authoritative_acceptance_action_used'] is True
 out=dict(generic);out.pop('single_original_action_Arnoldi_relation_qualified');out.pop('original_six_rows_admitted')
 out.update(operator='represented_directed_original244_coefficient_Astar',column_action_scopes=['represented_coefficient_Astar']*generic['iterations'],recurrence_action_scope='represented_coefficient_Astar',acceptance_scope='same_represented_coefficient_Astar_original53_source_relative_rows',source_relative_adjoint_rows_admitted=generic['original_six_rows_admitted'],generic_same_callback_Arnoldi_bookkeeping=generic['single_original_action_Arnoldi_relation_qualified'],single_original147_forward_or_physical_A_relation_qualified=False,original_forward_physical_six_gates_tested=False,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False)
 if out['reason']=='original_six_rows_admitted':out['reason']='source_relative_adjoint_rows_admitted'
 return out

def continue_saved_adjoint7_coefficient(packet,operator_admission,right_adjoint,action_star,positive_star,complete_stage,keep,label):
 assert not ADJOINT7_CONTINUATION_AUTHOR_DRAFT and not ADJOINT7_CONTINUATION_AUTHORING_IN_PROGRESS and P.LINEAR_TOL==1e-10
 assert tuple(GMRES_RESUME_PREFIX_PROOF)==ADJOINT7_PREFIX_PROOF and all(callable(f) for f in (right_adjoint,action_star,positive_star,complete_stage))
 assert operator_admission['original_source']==ADJOINT7_ORIGINAL_SOURCE and operator_admission['source_pins']==ADJOINT7_SELECTED_PINS and operator_admission['factor_context']==packet['factor_context']
 assert operator_admission['operator']=='represented_directed_original244_coefficient_Astar' and operator_admission['same_original244_directed_point_descriptors'] is True and operator_admission['original53_source_relative_gate_semantics_preserved'] is True
 assert operator_admission['all_selected_sources_and_role_seals_verified'] is operator_admission['padded_point_envelopes_authenticated'] is True
 assert operator_admission['uniform_adjoint_or_global_inverse_qualified'] is operator_admission['physical_adoption'] is False
 s=packet['state'];assert s['column_action_scopes']==['represented_coefficient_Astar']*7 and s['iterations']==s['next_iteration']==7
 internal=dict(s,column_action_scopes=['authoritative']*7);first_used=False;stage_refs=[]
 def stage(role,data,metadata):
  ref=complete_stage(role,data,dict(metadata,operator='represented_coefficient_Astar',prefix_proof=ADJOINT7_PREFIX_PROOF,physical_adoption=False));assert isinstance(ref,dict) and ref;stage_refs.append(ref);return ref
 def right(x,tag):
  nonlocal first_used
  adjoint7_pair(x,keep,tag+'_input')
  if not first_used:
   assert all(np.array_equal(x[w].view(np.uint64),s['V'][7][w].view(np.uint64)) for w in (0,1)),'First right input must be exact earned V7'
   y=adjoint7_pair(tuple(a.copy() for a in packet['first']),keep,tag+'_earned_output')
   stage('EARNED_RIGHT_ADJOINT_REUSE',dict(input_hi=x[0],input_lo=x[1],output_hi=y[0],output_lo=y[1]),dict(source=packet['first_ref'],factor_context=packet['factor_context'],exact_argument_both_words=True,factor_application_replayed=False));first_used=True;return y
  y=adjoint7_pair(right_adjoint(x,tag),keep,tag+'_new_output');stage('NEW_RIGHT_ADJOINT',dict(input_hi=x[0],input_lo=x[1],output_hi=y[0],output_lo=y[1]),dict(factor_context=packet['factor_context']));return y
 def action(x,tag):
  y=adjoint7_pair(action_star(x,tag),keep,tag+'_new_Astar');stage('NEW_ASTAR_WEAK',dict(input_hi=x[0],input_lo=x[1],output_hi=y[0],output_lo=y[1]),dict(original244_scope=True));return y
 def positive(x,tag):
  e=np.asarray(positive_star(x,tag)).copy();keep(tag+'_completed_unsigned_Astar_envelope',e.copy())
  assert e.shape==(403340,) and e.dtype==np.float64 and np.all(np.isfinite(e)) and np.all(e>=0)
  stage('NEW_ASTAR_POSITIVE',dict(envelope=e),dict(original244_unsigned_scope=True));return e
 def identity(x,tag):return adjoint7_pair(tuple(a.copy() for a in x),keep,tag+'_original_identity_left')
 def scores(x,tag):return mechanical_adjoint_scores(x,packet['reference'],keep,tag)
 def progress(i,nodes,after,increment):
  for n,x in (('nodes',nodes),('action',after['action']),('residual',after['residual']),('increment',increment)):adjoint7_pair(x,keep,label+'_candidate_'+n)
  stage('CANDIDATE',dict(nodes_hi=nodes[0],nodes_lo=nodes[1],action_hi=after['action'][0],action_lo=after['action'][1],residual_hi=after['residual'][0],residual_lo=after['residual'][1],increment_hi=increment[0],increment_lo=increment[1],scores=after['scores']),dict(iteration=i,admitted=after['admitted'],gate='original53_native_metric_packed_raw_and_scaled_1e-10'))
 def checkpoint(i,v,small):
  adjoint7_pair(v,keep,label+'_completed_basis');assert small['column_action_scopes']==['authoritative']*i
  data=dict(basis_hi=v[0],basis_lo=v[1],**{n:np.asarray(small[n]) for n in ('H_hi','H_lo','R','Givens_cos','Givens_sin','rotated_RHS','initial_norm','history','Arnoldi_contact_norms','Arnoldi_operation_bounds')})
  stage('ITERATION_STATE',data,dict(iteration=i,next_iteration=i,cap=80,column_action_scopes=['represented_coefficient_Astar']*i,original_context=packet['context_ref'],reason=small['reason']))
 nodes,after,increment,generic=native_metric_gmres_solve(s['start'],s['current'],s['rhs'],right,identity,action,positive,scores,label,80,progress,internal,action,action,checkpoint)
 assert first_used and generic['resumed_completed_iterations']==7 and generic['saved_prefix_actions_or_factors_replayed'] is False
 return nodes,after,increment,dict(adjoint7_truthful_history(generic),earned_V7_factor_returned_once=True,new_stage_refs=stage_refs,original_failed37897_exit_code=1,original_all550_input_or_all857_output_audit_claimed=False,normal_CMC_feedback_or_galaxy_qualification=False)
