"""HELD NEW-eL80 represented244 warm refiner; root alone binds and executes.
Only earned warm words/reference are hydrated; no old RHS/action/factor replay.
Original244/110 numerical callbacks and53 source rows remain conditional.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_REFINEMENT_V001'
DRIVER_PROTOCOL='SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_REFINEMENT_V001.md'
PROTOCOL_SHA='634291a41fe9e624fbfb0216b13ed00f69839cde03080f3fefb7fab5bb0e0f93'
WARM_SOURCE=(None,None)
WARM_RESULT=(None,None,None)
WARM_RECEIPT=(None,None,None)
WARM_PROOF=(None,None,None)
WARM_TEMPLATE=('same_geometry_NEW_eL_saved_adjoint_warm_admission_v001.py','51960b88ab9f2f3a0e4f090916ea9d62257727aefbe3f59d01af23821eb95c1e')
SUPPORT_SOURCE=('saved_prefix_coefficient_adjoint_continuation_v002.py','66bd49dc21ab49cc7ae7c1b0cd5c929d882f8879e6773e7db2a40acd9a640075')
SUPPORT_NAMES={'selected_definitions','load_io','initialize_helpers','bounded_keep','commit','read_selected','complete_stage','terminal_identity'}
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
VERIFIED_ARCHIVES={};SMALL_STATE={};POSITIVE_PENDING={};CURRENT_CANDIDATE=None;NEW_BASIS=[];NEW_STATES=[];NEW_ACTIONS=[];ACTIVE_ARGUMENT={}
GMRES_LABEL='NEW_eL_warm_mechanical_adjoint_GMRES'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
FLAGS={'physical_metric_qualified': False, 'canonical_currents_restored': False, 'normal_constraints_qualified': False, 'initial_CMC_solved': False, 'phase_charge_restored': False, 'CMC_preservation_qualified': False, 'exterior_qualified': False, 'evolution_qualified': False, 'galaxy_velocity_qualified': False}
NODAL_SOURCE=('cross_u_candidate_directed_nodal_preconditioner_preparation_v005.py', '41d6b4b3d200c8e017759ee3f95e05addaf3d7ea59b53a61f0fcc12b3f514659')
NODAL_RESULT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RESULT.json', '20ddbdfe237cf5062440971f59b838046962994ad9517d3851d400e3e3b8a811', 'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
NODAL_RECEIPT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RECEIPT.json', '46221584fefc9a1ee67cfe62cdf6b27d4710964f60b4ad7865ed6e48e0cdd57b', 'CLOSED')
NODAL_PROOF=('ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_V001.json', '915f5cb58d42291166940df770359ab4416ef153c47dba9b43c680dbc6a6b7af', 'ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_VERIFIED')
NODAL_PROJECTION=('ROOT_CLOSED_NODAL120_BOUNDED_RESULT_PROJECTION_V001.json', 'f1ef9d6660125f8a1beef9fa42d1c3549d299d672341bbf5acfb49a00efa741c', 'ROOT_CLOSED_NODAL120_BOUNDED_RESULT_PROJECTION_VERIFIED')
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_directed_nodal_factor_apply_v001.py': '4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b', 'author_fragment_native_metric_star_paired_gmres_v001.py': '3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770', 'author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py': '25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_native_metric_star_paired_gmres_resume_v002.py': '73b15a0e0512295aed41389a80c20ec6cf50ddef634497c805ada69c8ed738ee', 'author_fragment_same_geometry_NEW_eL_adjoint_warmstart_v002.py': '31fe8dec87da94c2f429aa479173ea2e2485c534f5144b173c82a136d3061f29'}

def load_support():
 assert hashlib.sha256((BASE/SUPPORT_SOURCE[0]).read_bytes()).hexdigest()==SUPPORT_SOURCE[1]
 tree=ast.parse((BASE/SUPPORT_SOURCE[0]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in SUPPORT_NAMES];assert len(defs)==len(SUPPORT_NAMES)
 exec(compile(ast.Module(body=defs,type_ignores=[]),SUPPORT_SOURCE[0],'exec'),globals());load_io();globals()['keep']=bounded_keep;initialize_helpers()
 for file in ('author_fragment_native_metric_star_paired_gmres_resume_v002.py','author_fragment_same_geometry_NEW_eL_adjoint_warmstart_v002.py'):
  exec(compile(selected_definitions(file,None),file,'exec'),globals())
 for n in ast.parse((BASE/'author_fragment_same_geometry_NEW_eL_adjoint_warmstart_v002.py').read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SAME_GEOMETRY_ADJOINT_SOURCE_PINS':globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(GMRES_RESUME_AUTHOR_DRAFT=False,GMRES_RESUME_AUTHORING_IN_PROGRESS=False,SAME_GEOMETRY_ADJOINT_AUTHOR_DRAFT=False,SAME_GEOMETRY_ADJOINT_AUTHORING_IN_PROGRESS=False)
 assert P.LINEAR_TOL==1e-10 and SCOPE['a_mul'].__globals__ is SCOPE and P.a_prod is SCOPE['a_prod']

def source_constants(file,names):
 tree=ast.parse(P.path(file).read_text());out={}
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names:out[n.targets[0].id]=ast.literal_eval(n.value)
 assert set(out)==set(names);return out,tree

def admission():
 wrc,wproof=terminal_identity((WARM_SOURCE,WARM_RESULT,WARM_RECEIPT,WARM_PROOF));assert P.path(WARM_RESULT[0]).stat().st_size<=16*1024*1024
 bind(*WARM_RESULT[:2]);warm=json.loads(P.path(WARM_RESULT[0]).read_text());assert warm['owner']==wrc['owner'] and warm['qualification']==FLAGS and warm['controls']==[] and len(warm['checkpoints'])==3
 bind(*WARM_TEMPLATE);original=ast.parse(P.path(WARM_TEMPLATE[0]).read_text());wc,actual=source_constants(WARM_SOURCE[0],{'OLD_SOURCE','OLD_RESULT','OLD_RECEIPT','OLD_PROOF','NEW_E_L_SOURCE','NEW_E_L_RESULT','NEW_E_L_RECEIPT','NEW_E_L_PROOF','OLD_INPUT_COMMIT','PINS','AUTHOR_DRAFT','AUTHORING_IN_PROGRESS'})
 functions=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.FunctionDef)}
 assert functions(original)==functions(actual) and wc['AUTHOR_DRAFT'] is wc['AUTHORING_IN_PROGRESS'] is False
 case=warm['case'];assert warm['status']==case['status']==WARM_RESULT[2] and case['status'] in ('NEW_E_L_SAVED_WARM_SOURCE_ROWS_ADMITTED_ZERO_ACTIONS','NEW_E_L_SAVED_WARM_RESIDUAL_MEASURED_REFINEMENT_REQUIRED')
 assert case['roles']==3 and case['construction_controls']==case['new_point_actions']==case['new_factor_applications']==0 and case['new_cycle_cap_if_refined']==80
 assert case['old_RHS_iterations_not_relabelled'] is True
 for key in ('old_actions_factors_unsigned_or_basis_replayed','normal_phase_or_gauge_feedback_evaluated','uniform_adjoint_or_global_inverse_qualified','physical_adoption'):assert case[key] is False
 rows={}
 for i,(role,key) in enumerate((('WORD_LINKS','word_links'),('WARMSTART_CONTEXT','warm_context'),('MEASURED_ADMISSION','measured_admission'))):
  q=warm['checkpoints'][i];assert q['file'].endswith('_%05d_%s.npz'%(i,role)) and thin(q)==case[key];q=commit(q,wrc);assert q['metadata']['owner']==warm['owner'];rows[role]=q
 measured=rows['MEASURED_ADMISSION']['metadata'];adm=measured['admission'];assert adm['operator']=='represented_directed_original244_coefficient_Astar' and adm['source_pins']==SAME_GEOMETRY_ADJOINT_SOURCE_PINS
 assert adm['terminals']==[list(wc[n]) for n in ('OLD_SOURCE','OLD_RESULT','OLD_RECEIPT','OLD_PROOF','NEW_E_L_SOURCE','NEW_E_L_RESULT','NEW_E_L_RECEIPT','NEW_E_L_PROOF')]
 for name in ('all_selected_seals_verified','old_solution_and_action_argument_words_verified','same_paired_point_descriptors_and_original_basis_verified','same_147_raw_configuration_and_E0_words_verified','same_right_factor_and_original_coordinate_scale_verified','new_eL_copied_from_fresh139_literal142_bridge','callbacks_publish_completed_operands_without_mutation','old_positive_bound_at_exact_warm_lambda_verified','old_source_rows_admitted'):assert adm[name] is True
 assert adm['uniform_adjoint_or_global_inverse_qualified'] is adm['physical_adoption'] is False
 assert measured['word_links']==thin(rows['WORD_LINKS']) and measured['source_relative_adjoint_rows_admitted']==case['source_relative_adjoint_rows_admitted'] and measured['refinement_required']==case['refinement_required']
 assert case['refinement_required'] is (not case['source_relative_adjoint_rows_admitted']) and measured['old_actions_factors_unsigned_or_basis_replayed'] is False
 link=rows['WORD_LINKS']['metadata'];context=rows['WARMSTART_CONTEXT']['metadata']
 assert link['solution']==adm['old_solution_record']==context['old_solution'] and link['positive']==adm['old_positive_record'] and context['fresh_eL']==adm['new_eL_record'] and context['NEW_initial_source_rows_admitted']==case['source_relative_adjoint_rows_admitted']
 assert context['old_source_rows_admitted'] is True and context['old_action_or_factor_replayed'] is context['physical_adoption'] is False and context['old_basis_not_reused'] is True
 for names in (('OLD_SOURCE','OLD_RESULT','OLD_RECEIPT','OLD_PROOF'),('NEW_E_L_SOURCE','NEW_E_L_RESULT','NEW_E_L_RECEIPT','NEW_E_L_PROOF')):terminal_identity(tuple(wc[n] for n in names))
 old_input=wc['OLD_INPUT_COMMIT'];key=str(P.path(old_input).resolve());assert key in wrc['input_sha256'];bind(old_input,wrc['input_sha256'][key]);old=json.loads(P.path(old_input).read_text());assert old['metadata']['failed'] is False and old['metadata']['qualification']==FLAGS and old['metadata']['owner']['pid']==37897
 closed=old['metadata']['closed_provenance'];assert closed['factor']==json.loads(json.dumps((NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)))
 mechanical=closed['mechanical'];terminal_identity([mechanical[n] for n in ('source','result','receipt','proof')])
 nrc,npr=terminal_identity((NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF));bind(*NODAL_PROJECTION[:2]);projection=json.loads(P.path(NODAL_PROJECTION[0]).read_text());projected=projection['projected_result'];case=projected['case']
 assert projection['status']==NODAL_PROJECTION[2] and projection['source_sha256']==NODAL_SOURCE[1] and projection['receipt_sha256']==NODAL_RECEIPT[1] and projection['original_result']['sha256']==NODAL_RESULT[1]
 assert projection['original_proof']==dict(file=NODAL_PROOF[0],sha256=NODAL_PROOF[1],status=NODAL_PROOF[2]) and projection['owner']==nrc['owner']==npr['owner']==projected['owner']
 assert all(projection[n] is True for n in ('naturally_closed','all_success_role_seals_verified','selected_case_fields_exact','top_result_suffix_exact','full_result_bytes_sha256_freshly_verified','original_all_controls_passed_inherited')) and projection['exit_code']==0
 assert projected['status']==NODAL_RESULT[2] and projected['qualification']==FLAGS and case['closed_mechanical']==mechanical and case['right_preconditioner_factor_resolved'] is True and len(case['completed_chunk_refs'])==120
 nodal_input=commit(case['input'],nrc);bprov=nodal_input['metadata']['basis_provenance'];assert nodal_input['metadata']['closed_mechanical']==mechanical
 chunks=[];candidate_by_column={}
 for serial,ref in enumerate(case['completed_chunk_refs']):
  q=commit(ref,nrc);md=q['metadata'];iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784);p=hi-lo;pre='NEW_directed_nodal_q%d_chunk%03d_point_'%(iq,serial)
  assert md['owner']==nrc['owner'] and md['kind']=='completed_directed_nodal_moment_chunk_patch' and md['chunk']==serial and md['next_chunk']==serial+1 and md['column']==iq and md['selection']==[lo,hi] and md['basis_provenance']==bprov
  point=commit(md['committed_point_chunk'],nrc);pm=point['metadata'];assert pm['source']['closed_mechanical']==mechanical and pm['source']['column']==iq and pm['source']['selection']==[lo,hi] and pm['source']['original_basis']==bprov['original_basis']
  if iq not in candidate_by_column:candidate_by_column[iq]=pm['closed_candidate_provenance']
  assert pm['closed_candidate_provenance']==candidate_by_column[iq]
  assert len(md['completed_source_contacts'])==3 and all(c['passed'] is True and c['tolerance']==2e-11 for c in md['completed_source_contacts'])
  names={n:tuple(pre+'paired_raw_'+n+'_'+w for w in ('hi','lo')) for n in ('H','B','E','D')};names.update({'e'+n:pre+'e'+n for n in ('H','B','E','D')})
  for n,shape in dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3)).items():
   for key in names[n]+(names['e'+n],):assert md['schema'][key]==dict(shape=list(shape),dtype='float64',finite=True)
  chunks.append(dict(column=iq,lo=lo,hi=hi,point_block_ref=thin(q),same_candidate_provenance=pm['closed_candidate_provenance'],basis_provenance=bprov,selected_names=names,committed_original_point=thin(point)))
 factor=commit(link['solution']);assert factor['metadata']['original_factor']
 factor=commit(factor['metadata']['original_factor'],nrc);fm=factor['metadata'];assert fm['owner']==nrc['owner'] and fm['active_node_count']==3870 and fm['right_preconditioner_factor_resolved'] is True and fm['inactive_coordinates_are_zero_not_identity_padding'] is True
 assert fm['sheet_head_dimension']==6 and fm['sheet_arm_dimension']==2 and fm['interior_head_dimension']==9 and fm['interior_arm_dimension']==3 and fm['nodal_apply_or_weak_functional_qualified'] is fm['exact_weak_DD_or_global_inverse_qualified'] is fm['physical_adoption'] is False
 return dict(warm=warm,warm_receipt=wrc,roles=rows,nodal_input=nodal_input,nodal_receipt=nrc,chunks=chunks,factor=factor,closed_provenance=closed,basis_provenance=bprov)

def hydrate(refs):
 q=refs['roles'];names=tuple(n+'_'+w for n in ('lambda','saved_action','rhs','residual') for w in ('hi','lo'))+('scores','original_scale','saved_positive')
 d=read_selected(thin(q['WARMSTART_CONTEXT']),names);m=read_selected(thin(q['MEASURED_ADMISSION']),('scores','new_source_norms','new_source_exact_both_word_zero'));ties=read_selected(thin(q['WORD_LINKS']),('exact_word_ties',))
 assert ties['exact_word_ties'].dtype==np.bool_ and ties['exact_word_ties'].shape==(2,) and np.all(ties['exact_word_ties'])
 assert d['scores'].shape==m['scores'].shape==m['new_source_norms'].shape==(3,2) and m['new_source_exact_both_word_zero'].shape==(3,) and m['new_source_exact_both_word_zero'].dtype==np.bool_
 assert np.array_equal(d['scores'].view(np.uint64),m['scores'].view(np.uint64)) and np.array_equal(d['scores'],np.asarray(refs['warm']['case']['source_relative_scores'])) and np.all(d['scores']>=0)
 pair=lambda name:tuple(d[name+'_'+w].copy() for w in ('hi','lo'))
 for name in ('lambda','saved_action','rhs','residual'):same_geometry_adjoint_pair(pair(name),keep,'owned_warm_'+name)
 assert d['original_scale'].shape==d['saved_positive'].shape==(403340,) and np.all(d['original_scale']>0) and np.all(d['saved_positive']>=0)
 groups={}
 for i,(name,sl) in enumerate((('native',slice(0,380292)),('metric',slice(380292,None)),('packed',slice(None)))):
  zero=bool(m['new_source_exact_both_word_zero'][i]);norms=tuple(m['new_source_norms'][i]);assert all(np.isfinite(v) and (v==0 if zero else v>0) for v in norms)
  assert zero==all(np.all(a[sl]==0) for a in pair('rhs'));groups[name]=dict(zero_source_both_words=zero,norms=norms,selection=sl)
 admitted=bool(np.all(d['scores']<=1e-10));assert admitted==refs['warm']['case']['source_relative_adjoint_rows_admitted']
 reference=dict(groups=groups,scale=d['original_scale'].copy(),source=pair('rhs'),relative_reference_is_NEW_eL=True,physical_norm_or_forward_error_qualified=False)
 packet=dict(start=pair('lambda'),rhs=pair('rhs'),current=dict(action=pair('saved_action'),residual=pair('residual'),scores=d['scores'].copy(),admitted=admitted),reference=reference,saved_positive=d['saved_positive'].copy(),context=thin(q['WARMSTART_CONTEXT']),admission=q['MEASURED_ADMISSION']['metadata']['admission'],physical_adoption=False)
 complete_stage('WARM_REFERENCE_CONTEXT',dict(scores=d['scores'],norms=m['new_source_norms'],zero_source_both_words=m['new_source_exact_both_word_zero']),dict(warm_terminal=(WARM_SOURCE,WARM_RESULT,WARM_RECEIPT,WARM_PROOF),source_records={n:thin(r) for n,r in q.items()},norm_preparation_replayed=False,old_lambda_freshly_admitted=admitted))
 n=read_selected(thin(refs['nodal_input']),tuple('original_registered_basis_'+key for key in ('R','dv','hats')));basis={key:n['original_registered_basis_'+key] for key in ('R','dv','hats')}
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 complete_stage('BASIS_CONTEXT',basis,dict(nodal_input=thin(refs['nodal_input']),basis_provenance=refs['basis_provenance'],same_closed_coefficient_basis=True))
 fd=read_selected(thin(refs['factor']),tuple('assembled_'+name+'_'+w for name in ('D_inverse','S_inverse','B','E') for w in ('hi','lo')));factors={name:tuple(fd['assembled_'+name+'_'+w] for w in ('hi','lo')) for name in ('D_inverse','S_inverse','B','E')}
 factors.update(closed_provenance=dict(factor_record=thin(refs['factor']),terminal=(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)),all_active_factor_seals_verified=True,active_node_count=3870,right_preconditioner_factor_resolved=True,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
 nodal=prepare_candidate_directed_nodal_factor_apply(factors,keep,'NEW_same_earned_signed_factor_guard');complete_stage('FACTOR_CONTEXT',dict(active_nodes=np.asarray(3870)),dict(original_factor=thin(refs['factor']),inverse_or_factor_body_replayed=False))
 prepared=dict(chunks=refs['chunks'],basis=basis,closed=refs['closed_provenance']['factor'],physical_adoption=False,coefficient_transpose_only=True,authoritative147_association_measured=False,global_inverse_qualified=False)
 return packet,nodal,prepared

def refinement(refs,packet,nodal,prepared):
 def read_chunk(descriptor,names):
  CONTEXT.update(column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],source=descriptor['point_block_ref'])
  keys=tuple(key for n in ('H','B','E','D') for key in descriptor['selected_names'][n])+tuple(descriptor['selected_names']['e'+n] for n in ('H','B','E','D'));d=read_selected(descriptor['point_block_ref'],keys)
  return dict(record=descriptor['point_block_ref'],source_provenance=descriptor['same_candidate_provenance'],paired_raw={n:tuple(d[k] for k in descriptor['selected_names'][n]) for n in ('H','B','E','D')},operation_envelopes={n:d[descriptor['selected_names']['e'+n]] for n in ('H','B','E','D')})
 def action(x,tag):
  ACTIVE_ARGUMENT.clear();ACTIVE_ARGUMENT.update(current_supplied_hi=x[0].copy(),current_supplied_lo=x[1].copy())
  CONTEXT.update(stage='signed_Astar',label=tag)
  def completed(d,part):return complete_stage('ADJOINT_CHUNK',dict(native_hi=part[0][0],native_lo=part[0][1],metric_hi=part[1][0],metric_lo=part[1][1]),dict(source=d['point_block_ref'],column=d['column'],selection=[d['lo'],d['hi']],label=tag,operator='represented_coefficient_Astar'))
  return candidate_measured_coefficient_fullweak_transpose(prepared,x,read_chunk,keep,tag,completed)['packed']
 def positive(x,tag):
  ACTIVE_ARGUMENT.clear();ACTIVE_ARGUMENT.update(current_supplied_hi=x[0].copy(),current_supplied_lo=x[1].copy())
  pending=[];parts=[];POSITIVE_PENDING.clear();CONTEXT.update(stage='positive',label=tag)
  def completed():
   if pending:
    d=pending.pop();assert set(POSITIVE_PENDING)=={'native','metric'};parts.append(complete_stage('POSITIVE_CHUNK',dict(POSITIVE_PENDING),dict(source=d['point_block_ref'],column=d['column'],selection=[d['lo'],d['hi']],label=tag,original244_unsigned_scope=True)));POSITIVE_PENDING.clear()
  def reader(d,names):completed();pending.append(d);return read_chunk(d,names)
  e=candidate_fullweak_coefficient_positive(prepared,x,reader,keep,tag);completed();assert len(parts)==120;return e
 def right(x,tag):
  ACTIVE_ARGUMENT.clear();ACTIVE_ARGUMENT.update(current_supplied_hi=x[0].copy(),current_supplied_lo=x[1].copy())
  CONTEXT.update(stage='new_signed_right_adjoint',label=tag);return candidate_directed_nodal_factor_adjoint(nodal,x,keep,tag)
 nodes,after,increment,history=same_geometry_adjoint_warmstart_response(packet,right,action,positive,keep,GMRES_LABEL,complete_stage)
 assert history['new_cycle_cap']==80 and history['restarts']==0 and history['old_rhs_iterations_not_relabelled'] is True and history['uniform_adjoint_or_global_inverse_qualified'] is history['physical_adoption'] is False
 rows=[q for q in RECORDS if q['file'].endswith('_SOLUTION.npz')];assert len(rows)==1
 return dict(status='NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_ADMITTED' if history['source_relative_adjoint_rows_admitted'] else 'NEW_E_L_REPRESENTED_ADJOINT_SOURCE_ROWS_NOT_ADMITTED',solution=thin(rows[0]),source_relative_scores=after['scores'].tolist(),history=history,roles=len(RECORDS),controls=len(CHECKS),warm_terminal=(WARM_SOURCE,WARM_RESULT,WARM_RECEIPT,WARM_PROOF),new_rhs_basis=True,cycles=1,restarts=0,new_cycle_cap80=True,old_RHS_iterations_not_relabelled=True,old_actions_factors_or_norm_preparation_replayed=False,original147_or_forward_physical_rows_tested=False,normal_phase_or_gauge_feedback_evaluated=False,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and all(v is not None for q in (WARM_SOURCE,WARM_RESULT,WARM_RECEIPT,WARM_PROOF) for v in q),'Root closed warm tuple plus FULL/peer release required'
 assert not list(BASE.glob(STEM+'_*'));load_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(*WARM_TEMPLATE)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,warm_terminal=(WARM_SOURCE,WARM_RESULT,WARM_RECEIPT,WARM_PROOF),nodal_projection=NODAL_PROJECTION,new_cycle_cap=80,old_result_not_parsed=True,old_RHS_basis_not_imported=True,physical_adoption=False));packet,nodal,prepared=hydrate(refs)
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=refinement(refs,packet,nodal,prepared)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**SMALL_STATE,**ACTIVE_ARGUMENT,**{'last_positive_'+n:a for n,a in POSITIVE_PENDING.items()},**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_eL_warm_adjoint_operation',context=dict(CONTEXT),last_candidate=CURRENT_CANDIDATE,basis_states=NEW_STATES,completed_new_actions=NEW_ACTIONS,warm_terminal=(WARM_SOURCE,WARM_RESULT,WARM_RECEIPT,WARM_PROOF)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
