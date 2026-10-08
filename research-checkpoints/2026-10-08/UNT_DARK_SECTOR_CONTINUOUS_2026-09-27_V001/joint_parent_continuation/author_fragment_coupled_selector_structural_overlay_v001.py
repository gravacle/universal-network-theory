"""HELD definitions-only merge into coupledV005's existing selected-map schema.
Caller supplies authenticated CLOSED metadata packets. No readers, arrays,
numerical operators, proof recomputation or runtime-admission promotion.
"""
from copy import deepcopy
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
FUTURE_CONFIGURATION_SELECTORS=None
FUTURE_MECHANICAL_GAUGE_SELECTORS=None
FUTURE_FIXED_SHEET_MASK_WEIGHT_PROOF=None
FUTURE_PHASE_GAUGE_TRANSFER_PROOF=None
FUTURE_COMPLETE_SELECTED_BYTE_LEASES=None
FUTURE_COMPONENT_WORD_LINK_PROOF=None
INPUT_PINS={
 'closed9':('NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_V003.json','7bceaa8396fed1f7635ddcaac194e3939f8fb21aef229d079f75e6b83e516f70'),
 'mechanical':('ROOT_ACTUAL_CLOSED_SECOND_CYCLE_MECHANICAL_SELECTORS_V001.json','27c6d4dae409839e6abb7160bea2d8ef201a87c1a0e43ccf08eb648bb4241fbb'),
 'Rv':('ROOT_ACTUAL_CLOSED_NEW139_NORMAL_RESPONSE_SELECTORS_V001.json','57330c46ceb54161e51b6d50e75b6edf8582dd163de758735ea88721541c58e2'),
 'sheet':('NATIVE_CLOSED_ORIGINAL_SHEET_SELECTOR_SCHEMA_ADDENDUM_V001.json','1c40eca2a438acdb13c4c91a1f6998df2827e6172dcccf106153ddb06f0c7ddd'),
 'prior90':('ROOT_CLOSED_COUPLED_MECHANICAL_WORD_LINK_PREFLIGHT_V001_RESULT.json','8cf0ea08adec78c014e173fb616bb3e3dce567f0b8f90c36ac77f42a199dcdb6'),
 'partial303_bytes':('ROOT_CLOSED9_SELECTED_BYTE_CUSTODY_RESIDENT_PREFIX_V001.json','3a86209ace124aae5c28b9d2a8a4034eff24dbf151fe5c2fdd9e873a82fb1737')}
COMPONENT_SOURCE_PINS={
 'mechanical_adjoint':('same_NEW_eL_adjoint_additional_cycle_v002.py','3fddd656f7030f1765775b5b8442798b3c835a58b23518e79033208462541f56'),
 'literal_rate_normal120':('cross_u_NEW139_literal_rate_normal_refresh_preparation_v005.py','3deb4cfc0700adb932abc5713daf0b6a833a538cf29fdfe05082017af48b129e'),
 'configuration_three_chi':('cross_u_NEW139_configuration_three_unit_preparation_v006.py','6789a603ca989f27ac97f0e91f69902b29d6e4899012931d9ccbe89de451dfbe'),
 'mechanical_gauge64':('cross_u_NEW139_mechanical_gauge_current_preparation_v005.py','e1d504e0be1de04638fca626665e024b4323826260980ce6980505797a11a222')}
COMPONENT_STATUS={
 'mechanical_adjoint':'SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_ADMITTED',
 'literal_rate_normal120':'NEW139_LITERAL_RATE_NORMAL_COEFFICIENTS_REFRESHED_UNQUALIFIED',
 'configuration_three_chi':'NEW139_THREE_CHI_COEFFICIENTS_AND_SOURCE_ENVELOPES_PREPARED_UNQUALIFIED',
 'mechanical_gauge64':'NEW139_MECHANICAL_GAUGE64_POINT_COEFFICIENTS_PREPARED_UNQUALIFIED'}
SOURCE_PINS={
 'cross_u_NEW139_coupled425955_correction_v005.py':'51564c81094d7d89705d446f0a3d2963ab305dc71f78a901a5baf43f9e228ab8',
 'author_fragment_coupled_future4_selector_assembly_v003.py':'a07cc2e9f80d229e30d6002bad7115a6a47917872f0211994cf59620deae439d',
 'author_fragment_candidate_configuration_coefficient_wholeweak_v002.py':'fa55addae8e9bfe19d2f60628b5ba1776889b452902e4b3ae4ddaf893c62d122'}


def cso_component(packet,group):
 assert packet['all13group_runtime_map_admitted'] is False and packet['physical_adoption'] is False
 terminal=packet['actual_terminal'];assert len(terminal)==4 and all(v is not None for q in terminal for v in q)
 assert tuple(terminal[0])==COMPONENT_SOURCE_PINS[group] and terminal[1][2]==COMPONENT_STATUS[group] and terminal[2][2]=='CLOSED'
 component=packet['component'];assert component['not_runtime_selected_map'] is True and component['physical_adoption'] is False
 assert component['data_word_equalities_verified'] is False
 for record in component['records'].values():
  assert record['terminal']==group and record['success_role_membership_verified'] is True
  assert record['scientific_owner']['source_sha256']==terminal[0][1]
 return deepcopy(terminal),deepcopy(component)


def cso_merge_records(records,additional):
 for name,record in additional.items():
  if name in records:assert records[name]==record,'Conflicting scientific record alias: '+name
  else:records[name]=deepcopy(record)


def cso_validate_selectors(value,records,terminals):
 if value is None:return
 if isinstance(value,list):
  for item in value:cso_validate_selectors(item,records,terminals)
 elif isinstance(value,dict):
  if '$terminal' in value:
   assert set(value)=={'$terminal','$result_path'} and value['$terminal'] in terminals
   assert isinstance(value['$result_path'],list);return
  if '$record' in value:
   assert value['$record'] in records
   if '$metadata' in value:assert set(value)=={'$record','$metadata'} and isinstance(value['$metadata'],list)
   else:
    assert set(value)=={'$record','$keys','$shape','$dtype'} and len(value['$keys']) in (1,2)
    assert len(value['$keys'])==len(set(value['$keys'])) and value['$dtype'] in ('float64','int64','bool')
    assert isinstance(value['$shape'],list) and all(type(n) is int and n>=0 for n in value['$shape'])
   return
  if '$copy_finite_h_spatial' in value:assert set(value)=={'$copy_finite_h_spatial'}
  if '$concat_phase_VALUE' in value:assert set(value)=={'$concat_phase_VALUE'} and len(value['$concat_phase_VALUE'])==4
  for item in value.values():cso_validate_selectors(item,records,terminals)
 else:assert type(value) in (str,bool,int),'No scientific floating value injected in a selector subtree'


def cso_configuration_word_links(component,closed9):
 links=[];templates={q['name']:q['left'] for q in closed9['word_links'] if q['name'] in ('point_TOTAL_u','point_TOTAL_z','point_TOTAL_h_dot','N_first','beta_first','fixed_E0')}
 recipes=component['point_TOTAL_word_link_recipes'];assert len(recipes)==4
 for iq,recipe in enumerate(recipes):
  assert recipe['column']==iq and recipe['finite139_endpoints'] is None and recipe['exact_uint64_comparisons_verified'] is False
  for name,endpoint in recipe['future_group_endpoints'].items():
   if name=='h_spatial_first':
    finite={'$copy_finite_h_spatial':{'$record':'finite_rate_state_input%d'%iq,'$keys':['completed_RATE_STATE_INPUT_h_first_hi','completed_RATE_STATE_INPUT_h_first_lo'],'$shape':[3784,4,3,3],'$dtype':'float64'}}
    assert endpoint['$shape']==[3784,2,3,3]
   else:
    finite=deepcopy(templates[name]);finite['$record']='finite_rate_state_input%d'%iq
    if name=='point_TOTAL_h_dot':finite['$keys']=['NEW_FIXED_GEOMETRY_TOTAL_RATE_column%d_NEW_TOTAL_hdot_%s'%(iq,w) for w in ('hi','lo')]
    assert finite['$shape']==endpoint['$shape'] and finite['$dtype']==endpoint['$dtype']
   links.append(dict(name='configuration_column%d_'%iq+name,family=name,column=iq,left=finite,right=deepcopy(endpoint),exact_uint64_word_comparison_earned=False,required_for_runtime=True))
 return links


def merge_coupled_selector_overlay(closed9,mechanical_packet,Rv_packet,sheet_addendum,configuration_packet=None,gauge_packet=None):
 assert not AUTHORING_IN_PROGRESS and closed9['status']=='NATIVE_HELD_COUPLED_INPUT_SELECTOR_ASSEMBLY_INCOMPLETE_V003'
 assert closed9['closed_group_count']==9 and closed9['pending_group_count']==4 and len(closed9['records'])==303
 assert sheet_addendum['closed9_unchanged_sha256']==INPUT_PINS['closed9'][1] and sheet_addendum['sheet_nodes']==4832 and sheet_addendum['sheet_radiation_count']==0
 out=deepcopy(closed9);mt,mechanical=cso_component(mechanical_packet,'mechanical_adjoint');rt,Rv=cso_component(Rv_packet,'literal_rate_normal120')
 assert mechanical['cycle_number']==2 and mechanical['current_cycle_fresh_basis'] is True and mechanical['operator']=='represented_directed_original244_coefficient_Astar'
 assert mechanical['same_NEW_eL_source_and_original53_reference'] is True
 assert len(Rv['descriptors'])==len(Rv['chunks'])==120 and len(Rv['columns'])==4
 assert all(d['basis_provenance']==closed9['original_basis'] for d in Rv['descriptors'])
 out['terminals'].update(mechanical_adjoint=mt,literal_rate_normal120=rt)
 for records in (mechanical['records'],Rv['records'],sheet_addendum['records']):cso_merge_records(out['records'],records)
 out.update(Rv_chunks=Rv['chunks'],Rv_descriptors=Rv['descriptors'],Rv_closed=Rv['closed_scope'])
 s=mechanical['selectors'];rhs=mechanical['same_NEW_eL_current_cycle_RHS'];out['data']['lambda_mechanical']=deepcopy(s['lambda_mechanical'])
 out['data']['adjoint_certificates']['mechanical']=dict(admitted={'$terminal':'mechanical_adjoint','$result_path':['case','history','source_relative_adjoint_rows_admitted']},stationarity_rhs='e_L_target_minus_literal',canonical_epsilon_substituted=False,same_genuine_point_TOTAL_eL_or_rate_independent_phase_verified=None,rhs=deepcopy(rhs),residual=deepcopy(s['residual']),scores=deepcopy(s['scores']),source_norms=deepcopy(s['source_norms']))
 out['adjoint_admission']={g:dict(terminal=deepcopy(out['terminals'][g+'_adjoint']),original_lambda_and_certificate_argument_words_verified=None,fresh_eL_source_words_verified=None,physical_adoption=False) for g in ('mechanical','phase')}
 for link in out['word_links']:
  if link['name']=='mechanical_adjoint_eL_rhs':link.update(left=deepcopy(rhs),right={'$record':'literal220_weak_bridge','$keys':['NEW_literal_stationarity_eL_packed_hi','NEW_literal_stationarity_eL_packed_lo'],'$shape':[403340],'$dtype':'float64'},missing_endpoint_group=None)
  if link['name']=='mechanical_lambda_argument':link.update(left=deepcopy(s['lambda_mechanical']),right=deepcopy(mechanical['argument_word_links'][0]['right']),missing_endpoint_group=None)
 out['word_links'].extend(deepcopy(mechanical['argument_word_links'][1:]))
 pending=['configuration_three_chi','mechanical_gauge64']
 if configuration_packet is not None:
  terminal,configuration=cso_component(configuration_packet,'configuration_three_chi');pending.remove('configuration_three_chi');out['terminals']['configuration_three_chi']=terminal;cso_merge_records(out['records'],configuration['records'])
  assert len(configuration['descriptors'])==len(configuration['chunks'])==120 and len(configuration['york_columns'])==len(configuration['columns'])==4
  out.update(q_chunks=configuration['chunks'],q_descriptors=configuration['descriptors'])
  out['data']['q']=dict(york_columns=deepcopy(configuration['york_columns']),column_provenance=deepcopy(configuration['column_provenance']),sheet=deepcopy(sheet_addendum['data_q_sheet']),physical_adoption=False)
  out['word_links'].extend(cso_configuration_word_links(configuration,closed9))
 if gauge_packet is not None:
  terminal,gauge=cso_component(gauge_packet,'mechanical_gauge64');pending.remove('mechanical_gauge64');out['terminals']['mechanical_gauge64']=terminal;cso_merge_records(out['records'],gauge['records'])
  assert len(gauge['columns'])==4;phase=closed9['phase_gauge_columns'];out['gauge_columns']=deepcopy(gauge['columns'])
  for iq,column in enumerate(out['gauge_columns']):
   assert column['column']==iq and column['gauge_row_order']==phase['normal_row_order'] and column['gauge_jet_order']==phase['normal_test_jet_order']
   column['paired']['phase']=deepcopy(phase['paired_members'][iq]);column['invariant_phase_record']=deepcopy(phase['records'][iq]);column['phase_branch_operand_transfer_verified']=None
 out['sheet_unit_admission']=deepcopy(sheet_addendum['sheet_unit_admission'])
 out['phase_gauge_invariance']=None;out['phase_rate_independent_operand_transfer_verified']=None
 out['root_proof_bindings']=dict(prior90=INPUT_PINS['prior90'],partial303_bytes=INPUT_PINS['partial303_bytes'],fixed_sheet_mask_weight=None,phase_gauge_transfer=None,complete_selected_byte_leases=None,component_word_links=None)
 out['pending_groups']=pending;out['pending_group_count']=len(pending);out['closed_group_count']=13-len(pending)
 out['status']='NATIVE_COUPLED_SELECTOR_STRUCTURAL_OVERLAY_PREPARED_HELD';out['AUTHOR_DRAFT']=True;out['not_runtime_selected_map']=True
 out['remaining_runtime_words_unevaluated']=True;out['all_selected_seals_verified']=None;out['same_genuine_point_TOTAL_state_verified']=None
 out['independent_source_unsigned_and_paired_lineage_verified']=None;out['original_targets_references_and_basis_unchanged']=None;out['fresh_eL_mechanical_and_phase_adjoint_source_certificates_admitted']=None
 out['physical_adoption']=False;out['runtime_selected_map_binding']=None;out['sheet_selector_addendum']=INPUT_PINS['sheet'];out['closed9_selector']=INPUT_PINS['closed9']
 out['total_word_links']=len(out['word_links']);out['closed_selected_member_metadata_complete_for_overlay']=None
 for key in ('data','A_chunks','Rv_chunks','q_chunks','gauge_columns','word_links'):cso_validate_selectors(out[key],out['records'],out['terminals'])
 assert out['original_basis']==closed9['original_basis'] and out['A_descriptors']==closed9['A_descriptors'] and out['A_chunks']==closed9['A_chunks'] and out['A_closed']==closed9['A_closed']
 assert out['data']['Rw']==closed9['data']['Rw'] and out['Cstar_equals_minus_Rv_assumed'] is False and out['feedback_derivative_frozen'] is True
 return out
