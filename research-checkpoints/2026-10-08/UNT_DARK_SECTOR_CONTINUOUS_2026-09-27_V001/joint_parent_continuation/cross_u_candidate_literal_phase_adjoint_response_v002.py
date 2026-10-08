"""HELD NEW literal phase Mstar lambda_p=eLp response; root numerical ownership.
Source law p=N*mu*(-PX*hi*phi/X-Ptranspose*hi*P*phi)^0 is the selected
analytic phase action derivative at held geometry, including relative phase once.
This law identification is not a bitwise rounded-pressure AD identity.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_LITERAL_PHASE_ADJOINT_RESPONSE_V002'
PROTOCOL='CANDIDATE_LITERAL_PHASE_ADJOINT_RESPONSE_V001.md'
PROTOCOL_SHA='bec0b4f7ea89f24e26b042e1998fbe41e7c4b3e24575a51d84fc8a49019df410'
PHASE_MASS_SOURCE=('cross_u_updated_finite_phase_mass_preparation_v002.py', '76a929447f2a0ed968825872e57ce2cf309fb49eeff13a1d8916ae3becb374cc')
PHASE_MASS_RESULT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RESULT.json', '9febbd8cd23e96efbec23ffb6d24323d8b2ac99aaef5e73ce903bf49660b47c5', 'UPDATED_FINITE_PHASE_LITERAL_MASS_CACHE_PREPARED_UNQUALIFIED')
PHASE_MASS_RECEIPT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RECEIPT.json', '69e25ed8a9c413f7c153a69e976a9f36cb3636fd67a8193eb3138514a2be2872', 'CLOSED')
PHASE_MASS_PROOF=('ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_V001.json', '2b6d27847c8b70d592209d117dbc18f7ee0e41f8ed454d684734ec03d92ed662', 'ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_VERIFIED')
CAP=160
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_finite0_candidate_action_residual_v007.py':'ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58',
 'author_fragment_phase_literal_charge_hessian_v002.py':'293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143',
 'author_fragment_phase_fixed_weak_charge_response_core_v001.py':'331fb805f572de4257f76e879ba28ceef5e20d4cb4898260e712c95efb553c2c',
 'author_fragment_native_metric_star_paired_gmres_v001.py':'3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'author_fragment_candidate_literal_phase_adjoint_v001.py':'ba57821a1e06818326563ddcc9e05c34272571c002bbd3d30a3e59a5b70c742d',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'author_fragment_candidate_phase_normal_stress_v001.py':'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd',
 'CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RESULT.json':'ee8edf2f0f618a3d290fb847e97d799c2446ef245093fe3e3a1ea3f8f921238d',
 'CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RECEIPT.json':'f1806a9b804a14e8236814840e2c82002c493b8cbf1f65fb1a5b98807ce6979a',
 'CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json':'5f632a9927d41e36a40c7f2e0988997905ff99ac8dfef985307ce7723f63d4f9'}
np=P=K=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};PHASE_ADJOINT_REFERENCE=None
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)


def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])


def initialize():
 global np,K
 for file,h in PINS.items():assert h is not None and hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
 io='cross_u_finite0_candidate_action_residual_v007.py';names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(io,names),io,'exec'),globals());initialize_io()
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,CAP=CAP,LINEAR_TOL=1e-10)
 file=list(PINS)[0];names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','scalar_mask','scalar_lift','dd_node_update','minres_core'}
 exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 for n in names:setattr(P,n,SCOPE[n])
 P.LINEAR_TOL=1e-10
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,None),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']
 file='author_fragment_phase_literal_charge_hessian_v002.py';names={'phase_pair_keep','phase_scalar_value'};scope=dict(np=np,P=P)
 exec(compile(selected_definitions(file,names),file,'exec'),scope);K=types.SimpleNamespace(**{n:scope[n] for n in names})
 choices=(('author_fragment_phase_fixed_weak_charge_response_core_v001.py',None),('author_fragment_native_metric_star_paired_gmres_v001.py',{'native_metric_gmres_put','native_metric_gmres_tree','native_metric_gmres_dot','native_metric_gmres_norm'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',{'mp_out','mp_add','mp_mul'}),('author_fragment_candidate_literal_phase_adjoint_v001.py',None),('author_fragment_exact_exponent_two_product_v003.py',None))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals().update(PHASE_ADJOINT_AUTHOR_DRAFT=False,PHASE_ADJOINT_AUTHORING_IN_PROGRESS=False)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_phase_adjoint_exact_exponent_product')


def bind_record(ref):
 bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);cm=json.loads(P.path(ref['commit_file']).read_text())
 assert cm['file']==ref['file'] and cm['sha256']==ref['sha256']
 if 'metadata' in ref:assert cm['metadata']==ref['metadata']
 return dict(file=ref['file'],sha256=ref['sha256'],commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'],metadata=cm['metadata'])


def closed_phase_mass_admission():
 assert all(x is not None for q in (PHASE_MASS_SOURCE,PHASE_MASS_RESULT,PHASE_MASS_RECEIPT,PHASE_MASS_PROOF) for x in q),'Natural closed updated-H preparation and proof required'
 for q in (PHASE_MASS_SOURCE,PHASE_MASS_RESULT,PHASE_MASS_RECEIPT,PHASE_MASS_PROOF):bind(q[0],q[1])
 r=json.loads(P.path(PHASE_MASS_RESULT[0]).read_text());rc=json.loads(P.path(PHASE_MASS_RECEIPT[0]).read_text());proof=json.loads(P.path(PHASE_MASS_PROOF[0]).read_text())
 assert r['status']==PHASE_MASS_RESULT[2] and rc['status']==PHASE_MASS_RECEIPT[2] and proof['status']==PHASE_MASS_PROOF[2]
 assert r['owner']==rc['owner']==proof['owner'] and r['owner']['pid']==19724 and r['owner']['source_sha256']==proof['source_sha256']==PHASE_MASS_SOURCE[1]
 assert rc['result_sha256']==proof['result_sha256']==PHASE_MASS_RESULT[1] and proof['receipt_sha256']==PHASE_MASS_RECEIPT[1] and rc['error_sha256'] is None
 assert type(proof['exit_code']) is int and proof['exit_code']==0 and proof['naturally_closed'] is proof['all_success_role_seals_verified'] is True
 assert type(proof['input_seals_verified']) is int and proof['input_seals_verified']==len(rc['input_sha256']) and type(proof['output_seals_verified']) is int and proof['output_seals_verified']==len(rc['output_sha256'])
 stem=PHASE_MASS_RESULT[0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 assert r['qualification']==rc['qualification']==FLAGS and r['controls']==[] and len(r['checkpoints'])==6
 records=[bind_record(q) for q in r['checkpoints']]
 for q in records:
  assert q['metadata']['owner']==r['owner'] and q['metadata']['failed'] is False
  for k,h in (('file','sha256'),('commit_file','commit_sha256')):assert rc['output_sha256'][q[k]]==q[h]
 c=r['case'];prep=bind_record(c['preparation']);current=bind_record(c['current']);columns=[bind_record(q) for q in c['columns']]
 assert records==[current]+columns+[prep] and [q['metadata']['column'] for q in columns]==[0,1,2,3]
 md=prep['metadata'];assert md['kind']=='NEW_updated_finite_phase_literal_H_mass_diagonal_and_cache' and current['metadata']['kind']=='bitcopied_updated_phase_current_and_unchanged_literal_target'
 assert md['columns']==[thin(q) for q in columns] and md['current']==thin(current) and md['phase_space_dofs']==3870 and md['phase_outer_top_free'] is True
 assert md['current_H_and_p_tied_to_closed_finite_phase'] is md['point_H_strictly_positive'] is md['point_H_resolved_positive'] is md['diagonal_strictly_positive'] is True
 assert md['old_preupdate_H_or_diagonal_used'] is md['inverse_response_or_physical_admission'] is False and md['constants']['eps']==1e-5 and md['constants']['relative_phase_coefficient']==1.
 basis=bind_record(md['basis']);prior=bind_record(md['prior_literal_weak_charge']);assert thin(basis)==c['basis'] and thin(prior)==c['original_literal_phase_charge']==current['metadata']['prior_literal_weak_charge']
 for q in (basis,prior):
  for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert rc['input_sha256'][str(P.path(q[n]).resolve())]==q[h]
 terminal=md['terminal'];assert terminal==c['finite_terminal']==current['metadata']['terminal'] and terminal['owner']['pid']==13764
 for key in ('source','result','receipt','proof'):bind(*terminal[key][:2])
 fr=json.loads(P.path(terminal['result'][0]).read_text());fc=json.loads(P.path(terminal['receipt'][0]).read_text());fp=json.loads(P.path(terminal['proof'][0]).read_text())
 assert fr['status']==terminal['result'][2] and fc['status']=='CLOSED' and fp['status']==terminal['proof'][2] and fr['owner']==fc['owner']==fp['owner']==terminal['owner']
 assert fc['result_sha256']==fp['result_sha256']==terminal['result'][1] and fp['receipt_sha256']==terminal['receipt'][1] and fp['source_sha256']==terminal['source'][1]
 assert fp['exit_code']==0 and fp['naturally_closed'] is fp['all_input_seals_verified'] is fp['all_success_role_seals_verified'] is True and fc['error_sha256'] is None
 assert fr['case']['configuration_unchanged'] is fr['case']['original_target_words_unchanged'] is fr['case']['strict_EOS_domain_passed'] is True
 finite=[bind_record(q['metadata']['finite_phase']) for q in columns];assert [thin(q) for q in finite]==[thin(q) for q in fr['case']['columns']]
 fi=bind_record(fr['case']['input']);assert fi in fr['checkpoints'] and fi['metadata']['owner']==fr['owner'] and fi['metadata']['failed'] is False
 for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert fc['output_sha256'][fi[n]]==fi[h]
 assert current['metadata']['current']==thin(fr['case']['current']) and thin(basis)==fi['metadata']['basis'] and thin(prior)==fi['metadata']['prior_literal_weak_charge']
 for q in finite:
  assert q['metadata']['owner']==fr['owner'] and q['metadata']['failed'] is False
  for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert fc['output_sha256'][q[n]]==q[h]
 hat=json.loads(P.path('CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RESULT.json').read_text());htr=json.loads(P.path('CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RECEIPT.json').read_text())
 assert hat['status']=='ACTUAL_REGISTERED_SCALAR_HAT_INJECTIVITY_BOUND_PASS' and htr['status']=='CLOSED' and htr['error_sha256'] is None and htr['result_sha256']==PINS['CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RESULT.json']
 hat_basis=bind_record(hat['reference']);assert thin(basis['metadata']['reference'])==thin(hat_basis) and hat['evidence']['independent_node_count']==3870
 assert hat['evidence']['outer_and_top_scalar_nodes_free'] is True
 return dict(result=r,preparation=prep,current=current,basis=basis,prior=prior,columns=columns,finite=finite,finite_terminal=terminal,hat_basis=hat_basis,conditional_hat_bound=hat['phase_mass_bound'],closed_proof=proof)


def phase_adjoint_packet(refs):
 global PHASE_ADJOINT_REFERENCE,K
 CONTEXT.update(stage='copy_closed_updated_literal_phase_cache')
 prep=read(refs['preparation'],tuple(refs['preparation']['metadata']['schema']));current=read(refs['current'],tuple(refs['current']['metadata']['schema']));basis=read(refs['basis'],('R','dv','hats'));hat=read(refs['hat_basis'],('R','dv','hats'))
 target_saved=read(refs['prior'],('fixed_literal_weak_phase_charge_hi','fixed_literal_weak_phase_charge_lo'))
 for family,data in (('prepared',prep),('current',current),('basis',basis),('canonical_hat_basis',hat),('original_prior',target_saved)):
  for n,a in data.items():keep('copied_'+family+'_'+n,a)
 for n in basis:assert np.array_equal(basis[n],hat[n]) and np.array_equal(basis[n],prep['updated_phase_mass_NEW_basis_'+n]) and np.array_equal(basis[n],current['unchanged_registered_basis_'+n])
 input_ref=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='closed_updated_literal_phase_H_p_original_charge_and_same_scalar_basis',preparation=thin(refs['preparation']),current=thin(refs['current']),basis=thin(refs['basis']),prior=thin(refs['prior']),mass_terminal=dict(source=PHASE_MASS_SOURCE,result=PHASE_MASS_RESULT,receipt=PHASE_MASS_RECEIPT,proof=PHASE_MASS_PROOF),finite_terminal=refs['finite_terminal'],canonical_hat_basis=thin(refs['hat_basis']),R_dv_hats_bridge_bitwise=True,conditional_real_coefficient_hat_bound=refs['conditional_hat_bound'],no_EOS_current_diagonal_or_old_action_replayed=True,physical_adoption=False));clear_current()
 columns=[];gap_names=('pressure','PX','PXX','literal_current','registered_current','literal_canonical_density','registered_canonical_density','literal_temporal_H','registered_temporal_H','reduced_ADM_H','current_gap','density_gap','hessian_gap','reduced_gap','clock_square_construction_gap','supplied_minus_constructed_projector_gap')+tuple(n+'_analytic_chain_'+part for n in ('P','PX','PXX') for part in ('actual','expected','gap'))
 for iq,(mass,finite) in enumerate(zip(refs['columns'],refs['finite'])):
  CONTEXT.update(stage='copy_literal_source_law_and_stage_comparisons',column=iq);md=read(mass,tuple(mass['metadata']['schema']));prefix='NEW_finite_phase_column%d_NEW_invariant_'%iq
  names=tuple(prefix+n+suffix+'_'+w for n in gap_names for suffix in ('','_delta') for w in ('hi','lo') if prefix+n+suffix+'_'+w in finite['metadata']['schema'])
  assert all(prefix+n+'_'+w in names for n in ('literal_canonical_density','literal_temporal_H','density_gap','hessian_gap','reduced_gap','P_analytic_chain_gap','PX_analytic_chain_gap') for w in ('hi','lo'))
  gaps=read(finite,names)
  for family,data in (('updated_mass',md),('literal_source',gaps)):
   for n,a in data.items():keep('column%d_copied_'%iq+family+'_'+n,a)
  for n in ('literal_temporal_H','literal_canonical_density'):
   for w in ('hi','lo'):assert np.array_equal(md['copied_finite_phase_'+prefix+n+'_'+w],gaps[prefix+n+'_'+w])
  columns.append(P.checkpoint('PHASE_COLUMN',arrays(AVAILABLE),dict(kind='same_transaction_literal_p_H_and_inherited_pressure_current_H_comparisons',column=iq,input=thin(input_ref),mass_column=thin(mass),finite_column=thin(finite),candidate_provenance=mass['metadata']['candidate_provenance'],canonical_and_literal_derivative_same_selected_source_formula=True,source_scope='analytic continuum/represented coefficient law at held geometry; not rounded-pressure AD word identity',copied_delta_scope='old temporal phase step evidence only; not new lambda direction',physical_adoption=False)));clear_current()
 H=pair_from(prep,'updated_phase_mass_candidate_H');diagonal=pair_from(prep,'updated_phase_mass_diagonal_completed');charge=pair_from(current,'copied_updated_NEW_finite_phase_NEW_finite_literal_weak');target=pair_from(target_saved,'fixed_literal_weak_phase_charge')
 for w,i in (('hi',0),('lo',1)):assert np.array_equal(target[i],current['copied_updated_original_fixed_literal_weak_phase_charge_'+w])
 rhs=P.a_sub(target,charge);phase_response_keep('NEW_literal_phase_eLp_target_minus_saved_literal_current',rhs,keep)
 stored=pair_from(current,'copied_updated_NEW_finite_phase_NEW_target_minus_finite_current');phase_response_keep('copied_saved_target_minus_finite_literal_current',stored,keep)
 identity=P.a_sub(rhs,stored);phase_response_keep('NEW_eLp_same_source_transaction_identity',identity,keep)
 assert all(np.array_equal(a,b) for a,b in zip(rhs,stored)),'Same literal charge/current transaction required'
 mask=P.scalar_mask();assert np.count_nonzero(mask)==3870 and all(np.all(a[0]==0) for x in (rhs,target,charge,diagonal) for a in x)
 assert np.all(H[0]>abs(H[1])) and np.all(prep['updated_phase_mass_point_H_positive_construction_margin']>0) and np.all(diagonal[0][mask]>abs(diagonal[1][mask]))
 u=pair_from(prep,'updated_phase_mass_candidate_u');assert np.all(u[0]-abs(u[1])>0) and np.all(1e-5-u[0]-abs(u[1])>0)
 scale=np.sqrt(diagonal[0][mask]+diagonal[1][mask]);keep('NEW_phase_adjoint_positive_coordinate_scale',scale.copy());assert np.all(np.isfinite(scale)) and np.all(scale>0)
 phase_response_keep('NEW_phase_adjoint_diagonal_scale_sqrt_contact',P.a_sub(P.a_prod(scale,scale),phase_response_pack(diagonal)),keep)
 PHASE_ADJOINT_REFERENCE=phase_adjoint_reference(phase_response_pack(rhs),scale,keep,'NEW_phase_adjoint_source_reference')
 initial=P.a_dd(np.zeros((87,45)));phase_response_keep('NEW_phase_adjoint_exact_zero_lambda',initial,keep)
 initial_ref=P.checkpoint('INITIAL',arrays(AVAILABLE),dict(kind='NEW_eLp_and_zero_adjoint_unknown_same_literal_phase_state',input=thin(input_ref),columns=[thin(q) for q in columns],actual_budget=dict(cycles=1,cap=CAP),source_relative_raw_scaled_tolerance=1e-10,zero_unknown_is_adjoint_not_physical_rate_reset=True,coefficient_Mstar_equals_M_only_in_real_polynomial_scope=True,bitwise_DD_symmetry_or_uniform_error_qualified=False,physical_adoption=False));clear_current()
 counters=dict(operator=0,certificate=0)
 def mass_star(nodes,coefficient,g,capture,label):
  CONTEXT.update(stage='NEW_explicit_scalar_Mstar',operator_call=counters['operator']);weak=phase_adjoint_mass_star(nodes,coefficient,g,capture,label)
  P.checkpoint('OPERATOR',arrays({n:a for n,a in AVAILABLE.items() if n.startswith(label+'_')}),dict(kind='NEW_explicit_Sstar_H_W_S_completed_application',call=counters['operator'],input=thin(input_ref),label=label,weights_once=True,bitwise_symmetry_inferred=False,physical_adoption=False));counters['operator']+=1;return weak
 K.phase_mass_action=mass_star
 def certificate(nodes,rhs_packed,coefficient,g,positive_scale,capture,label):
  result=phase_adjoint_certificate(nodes,rhs_packed,coefficient,g,positive_scale,capture,label)
  P.checkpoint('CANDIDATE',arrays({n:a for n,a in AVAILABLE.items() if n.startswith(label+'_')}),dict(kind='NEW_both_word_lambda_explicit_Mstar_eLp_source_relative_certificate',call=counters['certificate'],input=thin(input_ref),label=label,source_relative_raw_scaled_tolerance=1e-10,physical_adoption=False));counters['certificate']+=1;return result
 globals()['phase_response_certificate']=certificate;CONTEXT.update(stage='NEW_one_cycle_phase_adjoint_MINRES')
 label='NEW_literal_phase_adjoint';answer=phase_response_solve(H,diagonal,rhs,basis,keep,label,cap=CAP,max_cycles=1)
 capture_families('completed_adjoint_answer_',{n:answer[n] for n in ('nodal_pair','jet_pairs','original_residual','original_ratios')});exact_zero=PHASE_ADJOINT_REFERENCE['zero_source_both_words']
 if exact_zero:
  assert answer['history']==[] and all(np.all(a==0) for a in answer['nodal_pair']);action=P.a_dd(np.zeros((87,45)))
 else:
  assert len(answer['history'])==1 and answer['history'][0]['cap']==CAP
  action=phase_response_unpack(pair_from(AVAILABLE,label+'_cycle_001_final_original_action'))
 phase_response_keep('completed_explicit_phase_Mstar_action',action,keep)
 residual=P.a_sub(rhs,action);phase_response_keep('completed_eLp_minus_Mstar_lambda',residual,keep);phase_response_keep('completed_Mstar_lambda_minus_eLp',P.a_sub(action,rhs),keep)
 assert all(np.array_equal(a[mask],b) for a,b in zip(residual,answer['original_residual']))
 ratios=phase_adjoint_scores(phase_response_pack(residual),PHASE_ADJOINT_REFERENCE,keep,'NEW_phase_adjoint_final_source_certificate');admitted=bool(np.all(ratios<=1e-10))
 solution=P.checkpoint('SOLUTION',arrays({**AVAILABLE,**RAW}),dict(kind='NEW_3870_literal_phase_coefficient_adjoint_response',input=thin(input_ref),initial=thin(initial_ref),history=answer['history'],actual_budget=dict(cycles=1,cap=CAP),adjoint_response_admitted=admitted,NEW_source_relative_raw_scaled_tolerance=1e-10,exact_both_word_zero_source=exact_zero,zero_source_relative_ratio_undefined=exact_zero,rounded_MINRES_recurrence_is_numerical_only=True,SPD_uniform_DD_or_global_inverse_qualified=False,original_finite_canonical_gates_tested=False,physical_adoption=False));clear_current()
 jets={n+'_'+word:pair[i] for n,pair in answer['jet_pairs'].items() for i,word in enumerate(('hi','lo'))}
 jet_ref=P.checkpoint('ADJOINT_JETS',arrays(jets),dict(kind='same_original_scalar_S_value_R_Z_of_lambda_p',solution=thin(solution),adjoint_response_admitted=admitted,lambda_is_adjoint_not_phase_state_or_rate_update=True,gauge_Cstar_feedback_external=True,physical_adoption=False))
 return dict(status='CANDIDATE_LITERAL_PHASE_ADJOINT_RESPONSE_ADMITTED' if admitted else 'CANDIDATE_LITERAL_PHASE_ADJOINT_RESPONSE_NONADMITTED',adjoint_response_admitted=admitted,input=input_ref,initial=initial_ref,columns=columns,solution=solution,adjoint_jets=jet_ref,preparation=thin(refs['preparation']),current=thin(refs['current']),prior=thin(refs['prior']),phase_mass_terminal=dict(source=PHASE_MASS_SOURCE,result=PHASE_MASS_RESULT,receipt=PHASE_MASS_RECEIPT,proof=PHASE_MASS_PROOF),finite_terminal=refs['finite_terminal'],raw_scaled_eLp_relative_ratios=ratios.tolist(),history=answer['history'],actual_budget=dict(cycles=1,cap=CAP),old_current_EOS_mass_diagonal_action_or_solver_replayed=False,original_literal_charge_unchanged=True,phase_state_or_rate_updated=False,gauge_Cstar_feedback_applied=False,physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and all(x is not None for q in (PHASE_MASS_SOURCE,PHASE_MASS_RESULT,PHASE_MASS_RECEIPT,PHASE_MASS_PROOF) for x in q),'Root release and natural closed updated phase mass proof required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(PROTOCOL,PROTOCOL_SHA)
  for name,h in PINS.items():bind(name,h)
  refs=closed_phase_mass_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,phase_mass_proof=refs['closed_proof'],literal_coefficient_law_source='fresh116 absolute plus relative phase once at held geometry',physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=phase_adjoint_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],case['raw_scaled_eLp_relative_ratios'],rh);return 0 if case['adjoint_response_admitted'] else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_phase_adjoint_operands',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
