"""HELD additional bounded80 correction cycle for the SAME NEW-eL source.
Exact naturally closed cap80 total seed/action/positive are reused. No old
Arnoldi prefix, action, factor or source norms are replayed. Root alone runs.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='SAME_NEW_E_L_ADJOINT_ADDITIONAL_CYCLE_V001'
DRIVER_PROTOCOL='SAME_NEW_E_L_ADJOINT_ADDITIONAL_CYCLE_V001.md'
PROTOCOL_SHA='c38a4cfba0e845db32cc9975573c52de2c4ea7a5c980b528289b9ccfa2cc95e1'
WARM_SOURCE=(None,None)
WARM_RESULT=(None,None,None)
WARM_RECEIPT=(None,None,None)
WARM_PROOF=(None,None,None)
WARM_TEMPLATE=('same_geometry_NEW_eL_saved_adjoint_warm_admission_v001.py','51960b88ab9f2f3a0e4f090916ea9d62257727aefbe3f59d01af23821eb95c1e')
SUPPORT_SOURCE=('saved_prefix_coefficient_adjoint_continuation_v002.py','66bd49dc21ab49cc7ae7c1b0cd5c929d882f8879e6773e7db2a40acd9a640075')
SUPPORT_NAMES={'selected_definitions','load_io','initialize_helpers','bounded_keep','commit','read_selected','complete_stage','terminal_identity'}
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
VERIFIED_ARCHIVES={};SMALL_STATE={};POSITIVE_PENDING={};CURRENT_CANDIDATE=None;NEW_BASIS=[];NEW_STATES=[];NEW_ACTIONS=[];ACTIVE_ARGUMENT={}
GMRES_LABEL='SAME_NEW_eL_additional80_mechanical_adjoint_GMRES'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
FLAGS={'physical_metric_qualified': False, 'canonical_currents_restored': False, 'normal_constraints_qualified': False, 'initial_CMC_solved': False, 'phase_charge_restored': False, 'CMC_preservation_qualified': False, 'exterior_qualified': False, 'evolution_qualified': False, 'galaxy_velocity_qualified': False}
NODAL_SOURCE=('cross_u_candidate_directed_nodal_preconditioner_preparation_v005.py', '41d6b4b3d200c8e017759ee3f95e05addaf3d7ea59b53a61f0fcc12b3f514659')
NODAL_RESULT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RESULT.json', '20ddbdfe237cf5062440971f59b838046962994ad9517d3851d400e3e3b8a811', 'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
NODAL_RECEIPT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RECEIPT.json', '46221584fefc9a1ee67cfe62cdf6b27d4710964f60b4ad7865ed6e48e0cdd57b', 'CLOSED')
NODAL_PROOF=('ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_V001.json', '915f5cb58d42291166940df770359ab4416ef153c47dba9b43c680dbc6a6b7af', 'ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_VERIFIED')
NODAL_PROJECTION=('ROOT_CLOSED_NODAL120_BOUNDED_RESULT_PROJECTION_V001.json', 'f1ef9d6660125f8a1beef9fa42d1c3549d299d672341bbf5acfb49a00efa741c', 'ROOT_CLOSED_NODAL120_BOUNDED_RESULT_PROJECTION_VERIFIED')
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_directed_nodal_factor_apply_v001.py': '4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b', 'author_fragment_native_metric_star_paired_gmres_v001.py': '3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770', 'author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py': '25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_native_metric_star_paired_gmres_resume_v002.py': '73b15a0e0512295aed41389a80c20ec6cf50ddef634497c805ada69c8ed738ee', 'author_fragment_same_geometry_NEW_eL_adjoint_warmstart_v002.py': '31fe8dec87da94c2f429aa479173ea2e2485c534f5144b173c82a136d3061f29'}

PREVIOUS_SOURCE=(None,None)
PREVIOUS_RESULT=(None,None,'NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_NOT_ADMITTED')
PREVIOUS_RECEIPT=(None,None,'CLOSED')
PREVIOUS_PROOF=(None,None,None)
PARENT_TEMPLATE=('same_geometry_NEW_eL_saved_adjoint_refinement_v001.py','7d1f0d238924a487a680ac24e6f5d355d72aaea902227dd3c4571c7a8e13976b')
PARENT_NAMES={'load_support','source_constants','admission','hydrate','refinement'}
BASE_COMPLETE_STAGE=None
PREVIOUS_SELECTION={}


def load_cycle_support():
 global BASE_COMPLETE_STAGE
 assert hashlib.sha256((BASE/PARENT_TEMPLATE[0]).read_bytes()).hexdigest()==PARENT_TEMPLATE[1]
 tree=ast.parse((BASE/PARENT_TEMPLATE[0]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in PARENT_NAMES];assert {n.name for n in defs}==PARENT_NAMES
 exec(compile(ast.Module(body=defs,type_ignores=[]),PARENT_TEMPLATE[0],'exec'),globals());load_support()
 BASE_COMPLETE_STAGE=complete_stage;globals()['complete_stage']=cycle_stage


def cycle_history(history):
 h=dict(history);assert h['new_cycle_cap']==80 and h['restarts']==0 and h['old_rhs_iterations_not_relabelled'] is True
 h.update(new_rhs=False,same_NEW_eL_source_and_original53_reference=True,additional_correction_cycle=True,cycle_number=2,current_cycle_restarts=0,restarts=1,previous_completed_iterations=80,cumulative_iterations=80+h['iterations'],cumulative_iteration_budget=160,previous_terminal=(PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF),previous80_actions_factors_and_basis_replayed=False,physical_adoption=False)
 return h


def cycle_stage(role,data,metadata):
 md=dict(metadata,additional_cycle=True,same_NEW_eL_source=True,previous_terminal=(PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF))
 if role=='SOLUTION':md['history']=cycle_history(md['history'])
 return BASE_COMPLETE_STAGE(role,data,md)


def cycle_admission():
 global PREVIOUS_SELECTION
 rc,proof=terminal_identity((PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF));bind(*PREVIOUS_RESULT[:2]);bind(*PARENT_TEMPLATE)
 keys={'WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF','PINS','SUPPORT_SOURCE','IO_PARENT','IO_PARENT_SHA','WARM_TEMPLATE','NODAL_SOURCE','NODAL_RESULT','NODAL_RECEIPT','NODAL_PROOF','NODAL_PROJECTION','FLAGS','AUTHOR_DRAFT','AUTHORING_IN_PROGRESS','GMRES_LABEL'}
 c,t=source_constants(PREVIOUS_SOURCE[0],keys);template=ast.parse(P.path(PARENT_TEMPLATE[0]).read_text())
 functions=lambda tree:{n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
 assert functions(t)==functions(template) and c['AUTHOR_DRAFT'] is c['AUTHORING_IN_PROGRESS'] is False
 for n in keys-{'AUTHOR_DRAFT','AUTHORING_IN_PROGRESS','GMRES_LABEL','WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF'}:assert c[n]==globals()[n],n
 for n in ('WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF'):globals()[n]=tuple(c[n])
 assert proof['measurement_status']==PREVIOUS_RESULT[2] and proof['source_relative_adjoint_rows_admitted'] is False and proof['iterations']==80 and proof['candidate_iterations']==[20,40,80]
 assert proof['all_original_construction_controls_passed'] is True and proof['numeric_arrays_decoded'] is proof['scientific_factor_or_control_actions_replayed'] is proof['physical_adoption'] is False
 h=proof['case_history'];assert h['iterations']==h['cap']==h['new_cycle_cap']==80 and h['reason']=='explicit_cap' and h['restarts']==0 and h['source_relative_adjoint_rows_admitted'] is False
 assert h['operator']=='represented_directed_original244_coefficient_Astar' and h['column_action_scopes']==['represented_coefficient_Astar']*80 and h['recurrence_action_scope']=='represented_coefficient_Astar'
 assert h['uniform_adjoint_or_global_inverse_qualified'] is h['physical_adoption'] is False
 canonical=lambda q:json.loads(json.dumps(q));assert proof['warm_terminal']==canonical(tuple(c[n] for n in ('WARM_SOURCE','WARM_RESULT','WARM_RECEIPT','WARM_PROOF')))
 rows=proof['records'];assert len(rows)==proof['role_count'] and all(q['owner_equal'] is q['embedded_metadata_equal'] is q['qualification_all_false'] is True for q in rows)
 byrole={n:[q for q in rows if q['role']==n] for n in ('SOLUTION','CANDIDATE','ASTAR_POSITIVE','WARM_REFERENCE_CONTEXT','ITERATION_STATE')}
 assert len(byrole['SOLUTION'])==len(byrole['WARM_REFERENCE_CONTEXT'])==1 and len(byrole['CANDIDATE'])==3 and len(byrole['ITERATION_STATE'])==79
 selected={}
 for role in ('SOLUTION','WARM_REFERENCE_CONTEXT'):selected[role]=commit(byrole[role][0],rc)
 for q in byrole['CANDIDATE']:
  a=commit(q,rc)
  if a['metadata']['iteration']==80:assert 'CANDIDATE' not in selected;selected['CANDIDATE']=a
 label=c['GMRES_LABEL']+'_candidate_080_new_positive'
 for q in byrole['ASTAR_POSITIVE']:
  a=commit(q,rc)
  if a['metadata']['context']['label']==label:assert 'ASTAR_POSITIVE' not in selected;selected['ASTAR_POSITIVE']=a
 assert set(selected)=={'SOLUTION','WARM_REFERENCE_CONTEXT','CANDIDATE','ASTAR_POSITIVE'}
 assert thin(selected['SOLUTION'])==proof['total_lambda_source_certificate'] and thin(selected['WARM_REFERENCE_CONTEXT'])==proof['warm_reference_context']
 assert all(q['metadata']['owner']==rc['owner'] for q in selected.values())
 sm=selected['SOLUTION']['metadata'];assert sm['history']=={k:v for k,v in h.items() if k not in ('new_stage_refs','normal_feedback_or_physical_adoption')} and sm['NEW_RHS_feedback_admission'] is sm['phase_or_gauge_feedback_evaluated'] is False
 cm=selected['CANDIDATE']['metadata'];assert cm['iteration']==80 and cm['admitted'] is False and cm['total_lambda_not_correction_owns_certificate'] is True
 pm=selected['ASTAR_POSITIVE']['metadata'];assert pm['coefficient_scope_only'] is True and pm['earned_exact_warm_argument_bound_reused'] is False
 assert selected['WARM_REFERENCE_CONTEXT']['metadata']['warm_terminal']==proof['warm_terminal'] and selected['WARM_REFERENCE_CONTEXT']['metadata']['norm_preparation_replayed'] is False
 selected['LAST_ITERATION_STATE']=commit(byrole['ITERATION_STATE'][-1],rc);assert selected['LAST_ITERATION_STATE']['metadata']['iteration']==79
 PREVIOUS_SELECTION=dict(proof=proof,records=selected,receipt=rc)
 refs=admission();assert selected['WARM_REFERENCE_CONTEXT']['metadata']['source_records']=={n:thin(q) for n,q in refs['roles'].items()}
 return refs


def seed_additional_cycle(packet):
 rows=PREVIOUS_SELECTION['records'];proof=PREVIOUS_SELECTION['proof'];names=tuple(n+'_'+w for n in ('lambda','action','residual','increment') for w in ('hi','lo'))+('scores',)
 s=read_selected(thin(rows['SOLUTION']),names)
 complete_stage('CAP80_SOLUTION_COPY',s,dict(previous_solution=thin(rows['SOLUTION']),measured_admitted=False,prior_iteration_count=80,source_certificate_owns_total_lambda=True))
 c=read_selected(thin(rows['CANDIDATE']),names)
 ties=np.asarray([np.array_equal(s[n].view(np.uint64),c[n].view(np.uint64)) for n in names],dtype=np.bool_);keep('cap80_solution_candidate_word_ties',ties.copy());assert np.all(ties)
 complete_stage('CAP80_CANDIDATE_WORD_LINKS',dict(exact_word_ties=ties),dict(previous_solution=thin(rows['SOLUTION']),previous_candidate=thin(rows['CANDIDATE']),iteration=80))
 e=read_selected(thin(rows['ASTAR_POSITIVE']),('input_hi','input_lo','envelope'))
 for w in ('hi','lo'):assert np.array_equal(e['input_'+w].view(np.uint64),s['lambda_'+w].view(np.uint64))
 assert e['envelope'].shape==(403340,) and e['envelope'].dtype==np.float64 and np.all(np.isfinite(e['envelope'])) and np.all(e['envelope']>=0)
 complete_stage('CAP80_POSITIVE_COPY',e,dict(previous_positive=thin(rows['ASTAR_POSITIVE']),exact_cap80_argument_words_verified=True,coefficient_unsigned_scope_only=True))
 r=read_selected(thin(rows['WARM_REFERENCE_CONTEXT']),('norms','zero_source_both_words'))
 inherited_norms=np.asarray([packet['reference']['groups'][n]['norms'] for n in ('native','metric','packed')]);inherited_zero=np.asarray([packet['reference']['groups'][n]['zero_source_both_words'] for n in ('native','metric','packed')],dtype=np.bool_)
 assert np.array_equal(r['norms'].view(np.uint64),inherited_norms.view(np.uint64)) and np.array_equal(r['zero_source_both_words'],inherited_zero)
 assert s['scores'].shape==(3,2) and np.array_equal(s['scores'].view(np.uint64),np.asarray(proof['source_relative_scores'],dtype=np.float64).view(np.uint64)) and not np.all(s['scores']<=1e-10)
 pair=lambda n:tuple(s[n+'_'+w].copy() for w in ('hi','lo'))
 for n in ('lambda','action','residual','increment'):same_geometry_adjoint_pair(pair(n),keep,'cap80_'+n)
 admission=dict(packet['admission'],old_solution_record=thin(rows['SOLUTION']),old_positive_record=thin(rows['ASTAR_POSITIVE']),old_source_rows_admitted=False,previous_new_source_rows_admitted=False,old_positive_bound_at_exact_warm_lambda_verified=True,previous_terminal=(PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF),same_NEW_eL_reference_and_source_unchanged=True)
 context=complete_stage('ADDITIONAL_CYCLE_CONTEXT',dict(lambda_hi=s['lambda_hi'],lambda_lo=s['lambda_lo'],saved_action_hi=s['action_hi'],saved_action_lo=s['action_lo'],rhs_hi=packet['rhs'][0],rhs_lo=packet['rhs'][1],residual_hi=s['residual_hi'],residual_lo=s['residual_lo'],scores=s['scores'],original_scale=packet['reference']['scale'],saved_positive=e['envelope'],source_norms=r['norms'],zero_source_both_words=r['zero_source_both_words']),dict(previous_records={n:thin(q) for n,q in rows.items()},same_NEW_eL_source_and_original53_reference=True,old80_basis_or_H_QR_imported=False,old80_actions_factors_or_source_norms_replayed=False,cap80_not_resume_iteration80=True,cycle_number=2,additional_cycle_cap=80,previous_source_rows_admitted=False,physical_adoption=False))
 return dict(start=pair('lambda'),rhs=packet['rhs'],current=dict(action=pair('action'),residual=pair('residual'),scores=s['scores'].copy(),admitted=False),reference=packet['reference'],saved_positive=e['envelope'].copy(),context=context,admission=admission,physical_adoption=False)


def additional_cycle(refs,packet,nodal,prepared):
 case=refinement(refs,packet,nodal,prepared);case['history']=cycle_history(case['history'])
 case.update(status='SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_ADMITTED' if case['history']['source_relative_adjoint_rows_admitted'] else 'SAME_NEW_E_L_ADDITIONAL_CYCLE_SOURCE_ROWS_NOT_ADMITTED',cycles=2,restarts=1,current_cycle_restarts=0,current_cycle_cap=80,previous_completed_iterations=80,cumulative_iterations=80+case['history']['iterations'],same_NEW_eL_source_and_reference=True,previous_terminal=(PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF),previous_solution=thin(PREVIOUS_SELECTION['records']['SOLUTION']),previous80_actions_factors_or_basis_replayed=False,original_cap80_measurement_preserved=True,physical_adoption=False)
 return case


def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(v is not None for q in (PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF) for v in q),'Root natural closed nonadmission plus FULL/peer release required'
 assert not list(BASE.glob(STEM+'_*'));load_cycle_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(*WARM_TEMPLATE);bind(*PARENT_TEMPLATE)
  for n,h in PINS.items():bind(n,h)
  refs=cycle_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,previous_terminal=(PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF),warm_terminal=(WARM_SOURCE,WARM_RESULT,WARM_RECEIPT,WARM_PROOF),additional_cycle_cap=80,cumulative_budget=160,same_NEW_eL_source_and_reference=True,old80_actions_factors_or_basis_replayed=False,physical_adoption=False))
  packet,nodal,prepared=hydrate(refs);packet=seed_additional_cycle(packet)
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=additional_cycle(refs,packet,nodal,prepared)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**SMALL_STATE,**ACTIVE_ARGUMENT,**{'last_positive_'+n:a for n,a in POSITIVE_PENDING.items()},**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_same_NEW_eL_additional_cycle',context=dict(CONTEXT),last_candidate=CURRENT_CANDIDATE,basis_states=NEW_STATES,completed_new_actions=NEW_ACTIONS,previous_terminal=(PREVIOUS_SOURCE,PREVIOUS_RESULT,PREVIOUS_RECEIPT,PREVIOUS_PROOF)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=OUTPUTS,qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
