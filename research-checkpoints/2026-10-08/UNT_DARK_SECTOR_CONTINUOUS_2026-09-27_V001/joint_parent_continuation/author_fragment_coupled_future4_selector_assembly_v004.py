"""HELD V003 metadata-only selector assembly for four naturally CLOSED components.
Root supplies authenticated result/receipt/proof and selected COMMIT dictionaries.
No file readers, archive decoding, numerical imports, actions, or runtime adoption.
The returned overlay remains incomplete until independent word/admission predicates.
"""
from copy import deepcopy
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
FUTURE_CLOSURES={n:None for n in ('mechanical_gauge64','literal_rate_normal120','configuration_three_chi','mechanical_adjoint')}
SOURCE_PINS={
 'mechanical_gauge64':('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py','e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222'),
 'literal_rate_normal120':('cross_u_NEW139_literal_rate_normal_refresh_preparation_v005.py','3deb4cfc0700adb932abc5713daf0b6a833a538cf29fdfe05082017af48b129e'),
 'configuration_three_chi':('cross_u_NEW139_configuration_three_unit_preparation_v006.py','6789a603ca989f27ac97f0e91f69902b29d6e4899012931d9ccbe89de451dfbe'),
 'mechanical_adjoint':('same_geometry_NEW_eL_saved_adjoint_refinement_v002.py','859589c1dd50756dabc93a1563298d1bf99056beefe7bcd8f00166b59ad30d4e')}
STATUS={
 'mechanical_gauge64':'NEW139_MECHANICAL_GAUGE64_POINT_COEFFICIENTS_PREPARED_UNQUALIFIED',
 'literal_rate_normal120':'NEW139_LITERAL_RATE_NORMAL_COEFFICIENTS_REFRESHED_UNQUALIFIED',
 'configuration_three_chi':'NEW139_THREE_CHI_COEFFICIENTS_AND_SOURCE_ENVELOPES_PREPARED_UNQUALIFIED',
 'mechanical_adjoint':'NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_ADMITTED'}

ADDITIONAL_CYCLE_SOURCE=('same_NEW_eL_adjoint_additional_cycle_v002.py','3fddd656f7030f1765775b5b8442798b3c835a58b23518e79033208462541f56')
ADDITIONAL_CYCLE_STATUS='SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_ADMITTED'
PREVIOUS_CYCLE_TERMINAL=(('same_geometry_NEW_eL_saved_adjoint_refinement_v002.py', '859589c1dd50756dabc93a1563298d1bf99056beefe7bcd8f00166b59ad30d4e'), ('SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_REFINEMENT_V002_RESULT.json', 'ae527ae20678c6da63dfca367f59d224688180c7d1f95668367c6165e185f830', 'NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_NOT_ADMITTED'), ('SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_REFINEMENT_V002_RECEIPT.json', '3b8c345b212922eb852ca1167f8a1e78ed3d83891cb62c77ad6166afe624141f', 'CLOSED'), ('READONLY_NATURAL_CLOSED_NEW_E_L_REFINEMENT_SEALS_V001.json', '5d58d3ff95c4ccd1b9018554ab67c38e021d5e7fbb5760c47e95f50add2b13d7', 'READONLY_NATURAL_CLOSED_NEW_E_L_REFINEMENT_SEALS_VERIFIED'))

def thin(q):
 return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def member(record,md,prefix,shape,paired=True,dtype='float64'):
 keys=[prefix+'_'+w for w in ('hi','lo')] if paired else [prefix]
 for n in keys:assert md['schema'][n]==dict(shape=list(shape),dtype=dtype,finite=True),n
 return {'$record':record,'$keys':keys,'$shape':list(shape),'$dtype':dtype}

def admitted_metadata(group,packet):
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and FUTURE_CLOSURES[group] is not None
 terminal=packet['terminal'];assert terminal==FUTURE_CLOSURES[group]
 additional=group=='mechanical_adjoint' and tuple(terminal[0])==ADDITIONAL_CYCLE_SOURCE
 assert tuple(terminal[0])==(ADDITIONAL_CYCLE_SOURCE if additional else SOURCE_PINS[group])
 assert packet['terminal_bytes_authenticated'] is packet['selected_COMMIT_bytes_authenticated'] is True
 result,receipt,proof=packet['result'],packet['receipt'],packet['proof'];owner=result['owner']
 assert result['status']==terminal[1][2]==(ADDITIONAL_CYCLE_STATUS if additional else STATUS[group]) and receipt['status']==terminal[2][2]=='CLOSED'
 assert proof['status']==terminal[3][2]
 source=terminal[0]
 if proof['status']=='READONLY_PERSISTENCE_COMPLETE_NEW139_COMPONENT_SUCCESS_SEALS_VERIFIED':
  assert group=='mechanical_gauge64' and tuple(source)==('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py','e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222')
  assert proof['kind']=='gauge' and proof['outcome']=='SUCCESS' and owner['pid']==89675
  assert proof['exit_code'] is None and proof['naturally_closed'] is False and proof['producer_exit_observed'] is proof['post_receipt_recheck_observed'] is False
  assert proof['persistence_complete'] is proof['process_absent'] is proof['session_retired'] is True
  closure=proof['observed_closure'];assert closure['pid']==89675 and closure['session_id']==42171 and closure['exit_code'] is None and closure['naturally_closed'] is False
  assert closure['persistence_complete'] is closure['process_absent'] is closure['session_retired'] is True and closure['producer_exit_observed'] is closure['post_receipt_recheck_observed'] is False
  assert isinstance(closure['observed_utc'],str) and closure['observed_utc'] and all(isinstance(closure[n],str) and closure[n] for n in ('process_absent_evidence','session_retired_evidence'))
  assert proof['all_input_seals_verified'] is proof['all_output_seals_verified'] is proof['all_success_role_seals_verified'] is proof['planned_role_and_control_census_complete'] is True
  assert proof['input_count']==len(receipt['input_sha256'])==109 and proof['output_count']==len(receipt['output_sha256'])==151
  assert proof['planned_roles']==proof['success_roles']==len(proof['records'])==74 and proof['failed_roles']==0 and proof['planned_controls']==proof['actual_control_count']==len(proof['controls'])==44
 else:
  assert proof['status']==terminal[3][2] and proof['naturally_closed'] is True and proof['exit_code']==0
 assert proof['all_input_seals_verified'] is proof['all_success_role_seals_verified'] is True
 assert owner==receipt['owner']==proof['owner'] and owner['source_sha256']==terminal[0][1]
 assert receipt['result_sha256']==proof['result_sha256']==terminal[1][1] and proof['receipt_sha256']==terminal[2][1] and receipt.get('error_sha256') is None
 assert result['qualification']==receipt['qualification'] and all(v is False for v in result['qualification'].values())
 assert result['case']['status']==result['status'] and result['case']['physical_adoption'] is False
 refs={q['commit_file']:q for q in result['checkpoints']};records={};metadata={}
 for name,ref in packet['selected_records'].items():
  assert ref['commit_file'] in refs and thin(refs[ref['commit_file']])==thin(ref)
  for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert receipt['output_sha256'][ref[n]]==ref[h]
  cm=packet['commits'][ref['commit_file']];md=cm['metadata']
  assert cm['file']==ref['file'] and cm['sha256']==ref['sha256'] and packet['commit_hashes'][ref['commit_file']]==ref['commit_sha256']
  assert md==refs[ref['commit_file']]['metadata'] and md['owner']==owner and md['failed'] is False and md['qualification']==result['qualification']
  records[name]=dict(terminal=group,reference=thin(ref),scientific_owner=deepcopy(owner),success_role_membership_verified=True);metadata[name]=md
 return result['case'],records,metadata

def additional_cycle_selectors(case,records,md,packet):
 history=case['history'];iterations=history['iterations'];previous=tuple(tuple(q) for q in case['previous_terminal'])
 assert previous==PREVIOUS_CYCLE_TERMINAL==tuple(tuple(q) for q in history['previous_terminal'])
 assert case['status']==ADDITIONAL_CYCLE_STATUS and type(iterations) is int and 0<=iterations<=80
 assert case['new_cycle_cap80'] is True and case['cycles']==2 and case['restarts']==1 and case['current_cycle_restarts']==0 and case['current_cycle_cap']==80
 assert case['previous_completed_iterations']==80 and case['cumulative_iterations']==80+iterations and case['same_NEW_eL_source_and_reference'] is True
 assert case['previous80_actions_factors_or_basis_replayed'] is False and case['original_cap80_measurement_preserved'] is True
 assert history['new_rhs'] is False and history['same_NEW_eL_source_and_original53_reference'] is history['additional_correction_cycle'] is True
 assert history['cycle_number']==2 and history['current_cycle_restarts']==0 and history['restarts']==1 and history['previous_completed_iterations']==80
 assert history['cap']==history['new_cycle_cap']==80 and history['cumulative_iterations']==80+iterations and history['cumulative_iteration_budget']==160
 assert history['previous80_actions_factors_and_basis_replayed'] is history['physical_adoption'] is False
 assert history['source_relative_adjoint_rows_admitted'] is True and history['operator']=='represented_directed_original244_coefficient_Astar'
 assert history['recurrence_action_scope']=='represented_coefficient_Astar' and history['column_action_scopes']==['represented_coefficient_Astar']*iterations
 assert history['uniform_adjoint_or_global_inverse_qualified'] is history['exact_DD_superposition_assumed'] is False
 scores=case['source_relative_scores'];assert len(scores)==3 and all(len(row)==2 and all(0<=x<=1e-10 for x in row) for row in scores)
 proof=packet['proof'];assert proof['measurement_status']==case['status'] and proof['source_relative_adjoint_rows_admitted'] is True
 assert proof['case_history']==history and proof['source_relative_scores']==scores and proof['iterations']==iterations and proof['all_original_construction_controls_passed'] is True
 assert case['roles']==len(packet['result']['checkpoints'])==proof['role_count'] and case['controls']==len(packet['result']['controls'])==proof['control_count']
 assert tuple(tuple(q) for q in proof['previous_terminal'])==previous and proof['qualification']==packet['result']['qualification']
 def named(ref):
  hits=[n for n,q in records.items() if q['reference']==thin(ref)];assert len(hits)==1;return hits[0]
 def role(suffix):
  hits=[n for n,q in records.items() if q['reference']['file'].endswith('_'+suffix+'.npz')];assert len(hits)==1;return hits[0]
 solution=named(case['solution']);m=md[solution];assert m['NEW_RHS_feedback_admission'] is True and m['phase_or_gauge_feedback_evaluated'] is False
 assert m['history']=={k:v for k,v in history.items() if k not in ('new_stage_refs','normal_feedback_or_physical_adoption')}
 assert thin(case['solution'])==thin(proof['total_lambda_source_certificate'])
 candidates=[q for q in history['new_stage_refs'] if q['file'].endswith('_CANDIDATE.npz')];assert candidates
 candidate=named(candidates[-1]);cm=md[candidate];assert cm['iteration']==iterations and cm['admitted'] is cm['total_lambda_not_correction_owns_certificate'] is True
 reference=role('WARM_REFERENCE_CONTEXT');r=md[reference];assert thin(proof['warm_reference_context'])==records[reference]['reference'] and r['norm_preparation_replayed'] is False
 assert r['warm_terminal']==case['warm_terminal']==proof['warm_terminal']
 context=role('ADDITIONAL_CYCLE_CONTEXT');c=md[context];assert thin(proof['additional_cycle_context'])==records[context]['reference']
 assert c['same_NEW_eL_source_and_original53_reference'] is c['cap80_not_resume_iteration80'] is True and c['cycle_number']==2 and c['additional_cycle_cap']==80
 assert c['old80_basis_or_H_QR_imported'] is c['old80_actions_factors_or_source_norms_replayed'] is c['previous_source_rows_admitted'] is c['physical_adoption'] is False
 previous_records=c['previous_records'];assert set(previous_records)=={'SOLUTION','CANDIDATE','ASTAR_POSITIVE','WARM_REFERENCE_CONTEXT','LAST_ITERATION_STATE'} and thin(case['previous_solution'])==thin(previous_records['SOLUTION'])
 copies={n:role(n) for n in ('CAP80_SOLUTION_COPY','CAP80_CANDIDATE_WORD_LINKS','CAP80_POSITIVE_COPY')}
 assert md[copies['CAP80_SOLUTION_COPY']]['previous_solution']==previous_records['SOLUTION'] and md[copies['CAP80_SOLUTION_COPY']]['measured_admitted'] is False
 assert md[copies['CAP80_CANDIDATE_WORD_LINKS']]['previous_solution']==previous_records['SOLUTION'] and md[copies['CAP80_CANDIDATE_WORD_LINKS']]['previous_candidate']==previous_records['CANDIDATE'] and md[copies['CAP80_CANDIDATE_WORD_LINKS']]['iteration']==80
 assert md[copies['CAP80_POSITIVE_COPY']]['previous_positive']==previous_records['ASTAR_POSITIVE'] and md[copies['CAP80_POSITIVE_COPY']]['exact_cap80_argument_words_verified'] is md[copies['CAP80_POSITIVE_COPY']]['coefficient_unsigned_scope_only'] is True
 for name in (solution,candidate,reference,context,*copies.values()):
  assert md[name]['additional_cycle'] is md[name]['same_NEW_eL_source'] is True and tuple(tuple(q) for q in md[name]['previous_terminal'])==previous
 selectors=dict(lambda_mechanical=member(solution,m,'lambda',(403340,)),residual=member(solution,m,'residual',(403340,)),scores=member(solution,m,'scores',(3,2),False),source_norms=member(reference,r,'norms',(3,2),False),zero_source=member(reference,r,'zero_source_both_words',(3,),False,'bool'))
 links=[dict(name='mechanical_lambda_argument',left=selectors['lambda_mechanical'],right=member(candidate,cm,'lambda',(403340,)),verified=False),dict(name='same_NEW_eL_source_norms',left=selectors['source_norms'],right=member(context,c,'source_norms',(3,2),False),verified=False),dict(name='same_NEW_eL_zero_source',left=selectors['zero_source'],right=member(context,c,'zero_source_both_words',(3,),False,'bool'),verified=False)]
 return dict(records=records,selectors=selectors,descriptors=[],data_word_equalities_verified=False,argument_word_links=links,inherited_RHS_context=deepcopy(r['source_records']['WARMSTART_CONTEXT']),inherited_RHS_terminal=deepcopy(r['warm_terminal']),RHS_selector_after_ancestor_membership=dict(record_name=None,keys=['rhs_hi','rhs_lo'],shape=[403340],scientific_owner_pid=89302,ancestor_membership_verified=None),same_NEW_eL_current_cycle_RHS=member(context,c,'rhs',(403340,)),same_NEW_eL_original_scale=member(context,c,'original_scale',(403340,),False),same_NEW_eL_RHS_to_89302_and_fresh_literal_word_links_verified=False,source_norm_nonzero_or_exact_two_word_zero_runtime_checks_verified=False,cycle_number=2,current_cycle_fresh_basis=True,same_NEW_eL_source_and_original53_reference=True,previous_terminal=previous,previous_records=deepcopy(previous_records),completed_cap80_copy_records={n:records[q]['reference'] for n,q in copies.items()},operator='represented_directed_original244_coefficient_Astar',physical_adoption=False,not_runtime_selected_map=True)


def component_selectors(group,packet,basis_wrapper):
 case,records,md=admitted_metadata(group,packet);out=dict(records=records,selectors={},descriptors=[],data_word_equalities_verified=False)
 def named(ref):
  hits=[n for n,q in records.items() if q['reference']==thin(ref)];assert len(hits)==1;return hits[0]
 if group=='mechanical_gauge64':
  assert case['roles']==74 and case['new_ports']==64 and case['new_controls']==44 and len(case['columns'])==4
  out['columns']=[]
  for iq,ref in enumerate(case['columns']):
   name=named(ref);m=md[name];assert m['column']==iq and len(m['tests'])==16 and m['input']==case['prepared_inputs'][iq]
   assert list(m['gauge_row_order'])==['N','beta_R','beta_Z','beta_phi'] and list(m['gauge_coordinate_order'])==['value','R','Z','t']
   out['columns'].append(dict(column=iq,fresh_mechanical_record=thin(ref),paired={n:member(name,m,'completed_MECHANICAL_GAUGE_COLUMN_coefficients_'+n,(3784,w,4,4)) for n,w in (('native',99),('metric',6))},gauge_row_order=list(m['gauge_row_order']),gauge_jet_order=list(m['gauge_coordinate_order']),source_records=deepcopy(m['source_records']),invariant_phase_record=None,phase_branch_operand_transfer_verified=None))
  out['source_unsigned_or_fullweak_control_invented']=False
 elif group in ('literal_rate_normal120','configuration_three_chi'):
  assert len(case['chunks'])==120 and len(case['columns'])==4
  assert case['roles']==(2050 if group=='literal_rate_normal120' else 494)
  out['chunks']={};out['columns']=[]
  for serial,ref in enumerate(case['chunks']):
   iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784);p=hi-lo;name=named(ref);m=md[name]
   if group=='literal_rate_normal120':
    assert m['column']==iq and m['selection']==[lo,hi] and m['chunk_ordinal']==serial and len(m['port_refs'])==16
    shapes=dict(normal_native=(p,4,4,99),normal_metric=(p,4,4,6),CMC_metric=(p,6),time_primary_rate_native=(p,4,99),time_primary_rate_metric=(p,4,6),current_normal_value=(p,4,4),current_time_primary_action=(p,4),current_initial_CMC_density=(p,))
    e=dict(e_native=(p,4,4,99),e_metric=(p,4,4,6),e_CMC_metric=(p,6),e_time_primary_rate_native=(p,4,99),e_time_primary_rate_metric=(p,4,6))
    block={n:member(name,m,'completed_refresh_'+n,s) for n,s in shapes.items()};block.update({n:member(name,m,'completed_refresh_'+n,s,False) for n,s in e.items()})
    out['chunks'][str(serial)]=dict(block,record=thin(ref),same_candidate_provenance=deepcopy(m['same_candidate_provenance']),physical_adoption=False)
    out['descriptors'].append(dict(column=iq,lo=lo,hi=hi,point_coefficients_ref=thin(ref),same_candidate_provenance=deepcopy(m['same_candidate_provenance']),basis_provenance=deepcopy(basis_wrapper)))
   else:
    assert (m['column'],m['lo'],m['hi'],m['chunk_ordinal'])==(iq,lo,hi,serial) and len(m['units'])==3 and m['configuration_jet_order']==['rho','rho_R','rho_Z']
    shapes=dict(mechanical=(p,105,3),phase=(p,3),normal=(p,4,4,3),CMC=(p,3))
    prepared=dict(coefficients={n:member(name,m,'completed_COEFFICIENT_CHUNK_coefficients_'+n,s) for n,s in shapes.items()},envelopes={n:member(name,m,'completed_COEFFICIENT_CHUNK_envelopes_'+n,s,False) for n,s in shapes.items()},points=p,global_inverse_or_physical_adoption=False)
    descriptor=thin(ref);out['descriptors'].append(descriptor);out['chunks'][str(serial)]=dict(source=descriptor,metadata={'$record':name,'$metadata':[]},prepared=prepared,all_selected_seals_verified=True)
  for iq,ref in enumerate(case['columns']):
   name=named(ref);m=md[name];assert m['column']==iq and m['chunks']==case['chunks'][30*iq:30*(iq+1)]
   out['columns'].append(dict(record=thin(ref),same_candidate_provenance=deepcopy(m['same_candidate_provenance']),original_basis_words_verified=None,configuration_cache=m.get('configuration_cache')))
  if group=='configuration_three_chi':
   out['york_columns']=[];out['point_TOTAL_word_link_recipes']=[]
   for iq,col in enumerate(out['columns']):
    cache=named(col['configuration_cache']);m=md[cache];assert m['column']==iq
    root='completed_NEW139_CONFIGURATION_CACHE_prepared_'
    york={n:member(cache,m,root+'york_'+n,s) for n,s in dict(h=(3784,3,3),ih=(3784,3,3),T=(3784,3,3),kappa=(3784,),trace_part=(3784,),inverse_lam=(3784,)).items()}
    reference=dict(L_maps=member(cache,m,root+'york_reference_L_maps',(3784,3,3,3,3)),target_raising_inverse=member(cache,m,root+'york_reference_target_raising_inverse',(3784,3,3),False),mu_owned=member(cache,m,root+'york_reference_mu_owned',(3784,),False))
    out['york_columns'].append(dict(york=york,york_reference=reference,source_record=col['configuration_cache'],column=iq))
    values={n:member(cache,m,root+suffix,s) for n,suffix,s in [('point_TOTAL_u','covectors_u_jets',(3784,4,3)),('point_TOTAL_z','covectors_z_jets',(32,3784,4,3)),('point_TOTAL_h_dot','mechanical_h_dot',(3784,3,3)),('N_first','gauge_N_jets',(3784,4)),('beta_first','gauge_beta_jets',(3784,4,3)),('h_spatial_first','geometry_h_spatial_jets',(3784,2,3,3)),('fixed_E0','reference_E0',(3784,4,4,4))]}
    out['point_TOTAL_word_link_recipes'].append(dict(column=iq,future_group_endpoints=values,finite139_endpoints=None,exact_uint64_comparisons_verified=False))
   out['column_provenance']=[q['same_candidate_provenance'] for q in out['columns']]
  out['closed_scope']=dict(naturally_closed=True,natural_exit_code=0,all_selected_seals_verified=True,physical_adoption=False,same_candidate_provenance=[x['same_candidate_provenance'] for x in out['columns']])
  out['closed_scope'].update(dict(zip(('source','result','receipt','proof'),packet['terminal'])))
 else:
  if tuple(packet['terminal'][0])==ADDITIONAL_CYCLE_SOURCE:return additional_cycle_selectors(case,records,md,packet)
  history=case['history'];assert case['new_cycle_cap80'] is True and case['cycles']==1 and case['restarts']==0 and history['iterations']<=80
  assert history['source_relative_adjoint_rows_admitted'] is True and history['operator']=='represented_directed_original244_coefficient_Astar'
  assert all(0<=x<=1e-10 for row in case['source_relative_scores'] for x in row)
  solution=named(case['solution']);m=md[solution];assert m['NEW_RHS_feedback_admission'] is True
  candidates=[q for q in history['new_stage_refs'] if q['file'].endswith('_CANDIDATE.npz')];assert candidates
  candidate=named(candidates[-1]);cm=md[candidate];assert cm['iteration']==history['iterations'] and cm['admitted'] is True and cm['total_lambda_not_correction_owns_certificate'] is True
  refs=[n for n,q in records.items() if q['reference']['file'].endswith('_WARM_REFERENCE_CONTEXT.npz')];assert len(refs)==1;reference=refs[0]
  out['selectors']=dict(lambda_mechanical=member(solution,m,'lambda',(403340,)),residual=member(solution,m,'residual',(403340,)),scores=member(solution,m,'scores',(3,2),False),source_norms=member(reference,md[reference],'norms',(3,2),False),zero_source=member(reference,md[reference],'zero_source_both_words',(3,),False,'bool'))
  out['argument_word_links']=[dict(name='mechanical_lambda_argument',left=member(solution,m,'lambda',(403340,)),right=member(candidate,cm,'lambda',(403340,)),verified=False)]
  out['inherited_RHS_context']=deepcopy(md[reference]['source_records']['WARMSTART_CONTEXT']);out['inherited_RHS_terminal']=deepcopy(md[reference]['warm_terminal'])
  out['RHS_selector_after_ancestor_membership']=dict(record_name=None,keys=['rhs_hi','rhs_lo'],shape=[403340],scientific_owner_pid=89302,ancestor_membership_verified=None)
  out['source_norm_nonzero_or_exact_two_word_zero_runtime_checks_verified']=False
 out['physical_adoption']=False;out['not_runtime_selected_map']=True;return out

def assemble_future4_metadata_overlay(packets,closed9):
 assert set(packets)==set(FUTURE_CLOSURES) and closed9['status']=='NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_INCOMPLETE_V003'
 assert closed9['closed_group_count']==9 and closed9['pending_group_count']==4 and closed9['remaining_runtime_words_unevaluated'] is True
 out={n:component_selectors(n,q,closed9['original_basis']) for n,q in packets.items()}
 return dict(status='NATIVE_COUPLED_FUTURE4_METADATA_SELECTORS_PREPARED_HELD',AUTHOR_DRAFT=True,not_runtime_selected_map=True,components=out,source_pins={**deepcopy(SOURCE_PINS),'mechanical_adjoint':tuple(packets['mechanical_adjoint']['terminal'][0])},runtime_word_links_verified=False,phase_transfer_verified=None,sheet_input_admission=None,original_target_and_scale_links_verified=None,fresh_total_lambda_source_certificate_runtime_verified=None,physical_adoption=False)
