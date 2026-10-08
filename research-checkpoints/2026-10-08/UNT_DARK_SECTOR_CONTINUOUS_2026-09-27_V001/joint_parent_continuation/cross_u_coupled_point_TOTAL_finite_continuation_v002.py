"""HELD separate finite continuation from a naturally CLOSED coupled correction.
Authentic NEW139 point TOTAL, original FY/material/gauge/priors and literal phase
are read through one root-bound selector map. New94->138->158 science only.
No old producer/control/action/solver replay, nodal TOTAL inference, feedback
reuse or physical admission. Root alone binds, releases and executes.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_COUPLED_POINT_TOTAL_FINITE_CONTINUATION_V002'
DRIVER_PROTOCOL='CROSS_U_COUPLED_POINT_TOTAL_FINITE_CONTINUATION_V002.md'
PROTOCOL_SHA='376373bd1ef7ce6f98dbb46facf0aea74ee849c0bf17814155157064938b7cfc'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
SELECTED_DATA_MAP=(None,None,'ROOT_COUPLED_POINT_TOTAL_FINITE_SELECTED_OPERANDS_AND_OWNERS_VERIFIED_HELD')
FINITE_CLOSURES={n:((None,None),(None,None,None),(None,None,'CLOSED'),(None,None,None)) for n in ('baseline139','coupled_correction','original_targets','phase_baseline','original_state_recovery')}
# These are external authority bindings, not invented automatic acceptance.
ORIGINAL_WHOLE_CORRECTION_AUTHORITIES={n:(None,None,None) for n in ('mechanical147','mechanical_normal87','configuration290','phase_normal157')}
FRESH_FEEDBACK_AUTHORITY=(None,None,None)
np=P=N=None
SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
COUPLED_REC=None;COUPLED_TERMINALS=None
EXPECTED_STAGE_COUNTS={'POINT_TOTAL_CONFIGURATION_FIELD': 3, 'POINT_TOTAL_CONFIGURATION_SECTIONS': 1, 'POINT_TOTAL_NEW_POINT_INCREMENTS': 1, 'POINT_TOTAL_UPDATED_COLUMN_TIME': 4, 'POINT_TOTAL_TRIAL_FIELDS': 1, 'POINT_TOTAL_COLUMN_HANDOFF': 4, 'TRIAL_YORK_GEOMETRY': 4, 'TRIAL_SPACETIME_MODEL': 4, 'TRIAL_RAW_CANDIDATE': 4, 'TRIAL_PRIMAL_CONTACT_STATE': 4, 'TRIAL_LITERAL_PHASE': 4, 'TRIAL_INTRINSIC_CURVATURE': 4, 'POINT_TOTAL_COLUMN_ASSOCIATION': 4, 'TRIAL_SAME_POSITION_SHEET_GEOMETRY': 1, 'TRIAL_RESIDUAL_INPUT': 1, 'TRIAL_MEAN_INPUT': 4, 'TRIAL_MEAN_ORDINARY': 4, 'TRIAL_NORMAL_NATIVE_EH': 64, 'TRIAL_NORMAL_PHASE': 16, 'TRIAL_NORMAL_TOTAL': 64, 'TRIAL_NEW_TEMPORAL_CACHE': 4, 'TRIAL_LITERAL_GRADIENT': 4, 'TRIAL_SHEET_ORDINARY_INPUT': 1, 'TRIAL_SHEET_ORDINARY': 1, 'TRIAL_SHEET_NORMAL': 1, 'TRIAL_GLOBAL_NORMAL_CMC': 1, 'TRIAL_FRESH_WEAK_CURRENT': 3, 'TRIAL_FRESH_WEAK_CURRENTS': 1, 'TRIAL_PHASE_REGISTRATION_COMPARISON': 1, 'TRIAL_CANONICAL_TARGET_EPSILON': 1, 'TRIAL_CURRENT_LITERAL_AND_UNFEEDBACKED_RESIDUAL': 1, 'INPUT': 1, 'COLUMN_INDEX': 4, 'ORIGINAL_SIX_MEASURED': 1}
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_candidate_configuration_contact_v001.py': '7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_candidate_phase_normal_stress_v001.py': 'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd', 'author_fragment_finite_fixed_canonical_ordinary_v001.py': '2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a', 'author_fragment_fixed_label_finite_sheet_geometry_v002.py': '556bac0713c74947b0abece865bf7e74c3d3b212029af1248aa7dd0af525a661', 'cross_u_NEW139_coupled425955_correction_v002.py': '2f12ae3e8c87411c3912f7d838e1e4e9760fdfa21731a54a03d85e81115c8fb5', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_point_TOTAL_trial_fields_v001.py': '96925b148cb7c1b3660e76867e5c499e9b10868bc737209b194d9c667adc46ef', 'author_fragment_total_trial_fields_to_column_v001.py': 'c0c3f97320301834666f35db66195aa5715c182dd2bb29ec4e957433808aaf94', 'author_fragment_fresh_trial_residual_packet_v001.py': '5814945f10ed230da7a26d234c83b49966a2376e692f81a55c0b38d077d48af4', 'author_fragment_phase_fixed_weak_charge_response_core_v001.py': '331fb805f572de4257f76e879ba28ceef5e20d4cb4898260e712c95efb553c2c', 'author_fragment_candidate_whole_configuration_york_contact_v001.py': '0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd', 'author_fragment_candidate_shared_canonical_action_blocks_v001.py': '4ffdbf60dde14d9b87a7cb947dca7f61ec7e4ffe456653aed5298de27dbd59ee', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_literal_temporal_gradient_bridge_v001.py': '880d9689965e7f66a159178cbec13b0a1e03e3929c7796e90c4370a9919f4d50', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871', 'author_fragment_initial_york_trace_target_response_v001.py': '71fda02b76e03c5ac4fe917f0514a3f13e60ec15b9aad21610045fbe40fe71e1', 'cross_u_candidate_reference_york_anchor_canonical_packet_v004.py': '184d850aee263a6d4957c7df632c7bd928d6804d9c43978489c5b6abda02b5d7'}

def finite_definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in defs}==set(names),file
 exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),scope)

def finite_literal_metadata(file,names):
 tree=ast.parse((BASE/file).read_text());found={}
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names:found[n.targets[0].id]=ast.literal_eval(n.value)
 assert set(found)==set(names);globals().update(found)

def initialize_finite_continuation():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for file,h in PINS.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
 # Exact original initializer depends on the first13 ordered pins. The extra
 # dependency pins are appended; no producer or top-level science is selected.
 finite_definitions(IO_PARENT,{'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from','initialize_arithmetic'},globals())
 initialize_io();initialize_arithmetic();P.LINEAR_TOL=1e-10
 finite_definitions('author_fragment_single_decode_recheck_v001.py',None,SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']
 extra={'a_reshape','a_transpose','pack_fields','unpack_fields','pack_dd','dd_native_node_value','dd_metric_node_value','metric_R_matrix','fields_from_pair','collapse'}
 finite_definitions('cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py',extra,SCOPE)
 primitive={'lift_velocity','lift_metric'};finite_definitions('cross_u_paired_current_primitive_momentum_readout_v002.py',primitive,SCOPE)
 for n in extra|primitive:setattr(P,n,SCOPE[n]);globals()[n]=SCOPE[n]
 choices=(('author_fragment_exact_exponent_two_product_v003.py',None),('cross_u_NEW139_coupled425955_correction_v002.py',{'coupled_pair','coupled_canonical','coupled_resolve','coupled_stage'}),('author_fragment_phase_fixed_weak_charge_response_core_v001.py',{'phase_response_keep','phase_response_scalar_jets'}),('author_fragment_candidate_whole_configuration_york_contact_v001.py',{'cq_keep','cq_zero','candidate_configuration_york_direction_jets'}),('author_fragment_candidate_shared_canonical_action_blocks_v001.py',{'cs_keep','cs_native_weak','cs_york_covector_six'}),('author_fragment_candidate_specialized_temporal_action_v001.py',{'ft_keep','candidate_temporal_prepare'}),('author_fragment_candidate_literal_temporal_gradient_bridge_v001.py',None),('author_fragment_candidate_fullweak_transpose_stationarity_v003.py',{'ct_pair','candidate_original_evaluation_transpose'}),('author_fragment_total_trial_fields_to_column_v001.py',None),('author_fragment_point_TOTAL_trial_fields_v001.py',None),('author_fragment_fresh_trial_residual_packet_v001.py',None),('author_fragment_initial_york_trace_target_response_v001.py',{'trace_target_reference_scores'}),('cross_u_candidate_reference_york_anchor_canonical_packet_v004.py',{'anchor_scores'}))
 for file,names in choices:finite_definitions(file,names,globals())
 for file,names in (('author_fragment_total_trial_fields_to_column_v001.py',{'TOTAL_TRIAL_SOURCE_PINS'}),('author_fragment_point_TOTAL_trial_fields_v001.py',{'POINT_TOTAL_TRIAL_SOURCE_PINS'}),('author_fragment_fresh_trial_residual_packet_v001.py',{'FRESH_TRIAL_SOURCE_PINS'})):finite_literal_metadata(file,names)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_finite_continuation_exact_exponent_product')
 assert P.TOL==2e-11 and P.LINEAR_TOL==1e-10

def finite_terminal(name):
 refs=FINITE_CLOSURES[name];assert all(v is not None for q in refs for v in q),name
 for q in refs:bind(q[0],q[1])
 source,result,receipt,proof=refs;r=json.loads(P.path(result[0]).read_text());rc=json.loads(P.path(receipt[0]).read_text());p=json.loads(P.path(proof[0]).read_text())
 assert r['status']==result[2] and rc['status']==receipt[2]=='CLOSED' and p['status']==proof[2] and rc.get('error_sha256') is None
 assert r['owner']==rc['owner']==p['owner'] and r['owner']['source_sha256']==p['source_sha256']==source[1]
 assert rc['result_sha256']==p['result_sha256']==result[1] and p['receipt_sha256']==receipt[1]
 assert type(p['exit_code']) is int and p['exit_code']==0 and p['naturally_closed'] is p['all_success_role_seals_verified'] is True
 assert p.get('all_input_seals_verified') is True or (type(p.get('input_seals_verified')) is int and p['input_seals_verified']==len(rc['input_sha256']))
 assert r['qualification']==rc['qualification'] and r['qualification'] and all(x is False for x in r['qualification'].values())
 assert all(c['passed'] is True for c in r.get('controls',[]))
 stem=result[0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 return dict(result_data=r,receipt_data=rc,proof_data=p,owner=r['owner'])

def finite_admission():
 global COUPLED_REC,COUPLED_TERMINALS
 assert all(v is not None for v in SELECTED_DATA_MAP),'Future root-selected immutable member/owner map required'
 bind(*SELECTED_DATA_MAP[:2]);m=json.loads(P.path(SELECTED_DATA_MAP[0]).read_text());assert m['status']==SELECTED_DATA_MAP[2]
 assert coupled_canonical(m['terminals'])==coupled_canonical(FINITE_CLOSURES) and m['physical_adoption'] is False
 for n in ('all_selected_seals_verified','genuine_point_TOTAL_not_nodal_baseline_verified','all_original_FY_material_gauge_phase_and_label_sources_verified','original_targets_and_reference_denominators_unchanged','correction_solution_and_baseline_source_words_verified'):assert m[n] is True
 groups={n:finite_terminal(n) for n in FINITE_CLOSURES};records={}
 assert groups['coupled_correction']['result_data']['status']=='NEW139_COUPLED425955_PROXY_CORRECTION_NUMERICALLY_MEASURED_UNQUALIFIED'
 for name,d in m['records'].items():
  ref=d['reference'];bind(ref['commit_file'],ref['commit_sha256']);cm=json.loads(P.path(ref['commit_file']).read_text());group=groups[d['terminal']]
  assert cm['file']==ref['file'] and cm['sha256']==ref['sha256'] and cm['metadata']['owner']==d['scientific_owner'] and cm['metadata']['failed'] is False
  assert cm['metadata']['qualification'] and all(x is False for x in cm['metadata']['qualification'].values()) and d['success_role_membership_verified'] is True
  if d['scientific_owner']==group['owner']:
   for key,h in (('file','sha256'),('commit_file','commit_sha256')):assert group['receipt_data']['output_sha256'][ref[key]]==ref[h]
   assert coupled_canonical(ref) in [coupled_canonical({k:q[k] for k in ('file','sha256','commit_file','commit_sha256')}) for q in group['result_data']['checkpoints']]
  else:
   assert d['explicit_inherited_owner_and_success_ref_verified'] is True and coupled_canonical(ref) in [coupled_canonical(q) for q in d['inherited_success_refs']]
   proof=d['ancestor_proof'];assert all(x is not None for x in proof);bind(*proof[:2]);p=json.loads(P.path(proof[0]).read_text());assert p['status']==proof[2] and d['exact_original_owner_role_membership_in_ancestor_verified'] is True
  records[name]=dict(ref,metadata=cm['metadata'])
 COUPLED_REC=records;COUPLED_TERMINALS=groups
 assert m['correction_solution_record']==groups['coupled_correction']['result_data']['case']['solution']
 assert coupled_canonical(m['correction_baseline_terminal'])==coupled_canonical(groups['coupled_correction']['result_data']['case']['closures']['finite139'])==coupled_canonical(FINITE_CLOSURES['baseline139'])
 return m

def finite_capture(name,value):
 CONTEXT['active_capture']=name
 for token in name.split('_'):
  for key in ('column','row','jet'):
   if token.startswith(key) and token[len(key):].isdigit():CONTEXT['active_'+key]=int(token[len(key):])
 return keep(name,value)

def finite_stage(role,payload):
 CONTEXT.update(active_stage=role)
 refs=[]
 def collect(v):
  if isinstance(v,dict):
   if all(k in v and isinstance(v[k],str) for k in ('file','sha256','commit_file','commit_sha256')):refs.append(thin(v))
   else:
    for x in v.values():collect(x)
  elif isinstance(v,(list,tuple)):
   for x in v:collect(x)
 collect(payload)
 for key in ('column','row','jet'):
  if key in payload:CONTEXT['active_'+key]=payload[key]
 return coupled_stage(role,payload,dict(kind='NEW_point_TOTAL_finite_continuation_completed_child',completed_stage_name=role,baseline=FINITE_CLOSURES['baseline139'],correction=FINITE_CLOSURES['coupled_correction'],original_selected_source_map=SELECTED_DATA_MAP,explicit_source_and_child_stage_refs=refs,payload_tags={n:x for n,x in payload.items() if x is None or type(x) in (str,bool,int)},old_scientific_body_replayed=False))

def finite_word_equal(a,b):
 if isinstance(a,np.ndarray):return isinstance(b,np.ndarray) and a.shape==b.shape and a.dtype==b.dtype and np.array_equal(a.view(np.uint8),b.view(np.uint8))
 if isinstance(a,dict):return isinstance(b,dict) and a.keys()==b.keys() and all(finite_word_equal(a[k],b[k]) for k in a)
 if isinstance(a,(list,tuple)):return isinstance(b,type(a)) and len(a)==len(b) and all(finite_word_equal(x,y) for x,y in zip(a,b))
 if type(a) is float:return type(b) is float and math.isfinite(a) and math.isfinite(b) and a.hex()==b.hex()
 return type(a) is type(b) and a==b

def finite_word_links(m):
 required={'basis_R','basis_dv','basis_hats','basis_r','basis_z','fixed_native_target','fixed_literal_phase_target','fixed_registered_phase_target','original_native_affine_reference','original_native_canonical_reference','original_metric_epsilon_denominator','original_native_scale','original_metric_scale','solution_mechanical','solution_phase','solution_chi','solution_W','solution_t'}
 for iq in range(4):required|={'column%d_'%iq+n for n in ('point_TOTAL_u','point_TOTAL_z','point_TOTAL_h_dot','genuine_N_jets','genuine_beta_jets','updated_phi','unchanged_phi_spatial','raw225_Lie','material','E0','FY_h','FY_h_spatial_pair','FY_Pi_owned','FY_T_owned','FY_tau_owned','FY_ih_owned','FY_target_raising_inverse','FY_mu_owned','FY_L_maps')}
 assert required<={x['name'] for x in m['word_links']}
 for link in m['word_links']:
  CONTEXT.update(active_component='operand_word_link',active_label=link['name']);a=coupled_resolve(link['left'],'NEW_finite_link_left_'+link['name']);b=coupled_resolve(link['right'],'NEW_finite_link_right_'+link['name'])
  assert finite_word_equal(a,b),link['name']

def finite_original_six(result,references,label):
 # The initial prepared metric RHS is the unchanged denominator; the NEW
 # varying-York epsilon is the residual, never its own norm reference.
 packed=P.pack_dd(result['epsilon']['native'],result['epsilon']['metric']);coupled_pair(label+'_fresh_varying_target_minus_current',packed,(403340,))
 scores,norms,zero=anchor_scores(packed,references['native_affine'],references['native_canonical'],references['metric_original_epsilon'],references['scales'],label+'_original_reference')
 return dict(scores=scores,norms=norms,zero_reference=zero,all_original_six_measured_admitted=bool(np.all(scores<=1e-10)),original_metric_reference_unchanged=True,new_metric_epsilon_denominator_used=False,normal_CMC_stationarity_or_physical_adoption=False)

def finite_packet(m):
 CONTEXT.update(active_component='immutable_input_hydration',active_column=None,active_label='NEW_finite_inputs');data=coupled_resolve(m['data'],'NEW_finite_inputs');finite_word_links(m)
 basis=data['basis'];saved=data['correction'];fields=[P.unpack_fields(a,False) for a in saved['mechanical']]
 correction=dict(native=tuple(q[0] for q in fields),metric=tuple(q[1] for q in fields),phase=saved['phase'],chi=saved['configuration']['chi'],W=saved['configuration']['W'],t=saved['configuration']['t'])
 provenance=coupled_canonical(m['trial_provenance']);provenance.update(baseline_closure=FINITE_CLOSURES['baseline139'],correction_closure=FINITE_CLOSURES['coupled_correction'],fixed_binding=SELECTED_DATA_MAP[:2],source_pins=TOTAL_TRIAL_SOURCE_PINS,point_TOTAL_source_pins=POINT_TOTAL_TRIAL_SOURCE_PINS)
 assert provenance['all_source_seals_authenticated'] is provenance['all_point_TOTAL_operand_seals_authenticated'] is provenance['original_fixed_references_verified'] is True and provenance['physical_adoption'] is False
 globals().update(TOTAL_TRIAL_AUTHOR_DRAFT=False,TOTAL_TRIAL_AUTHORING_IN_PROGRESS=False,TOTAL_TRIAL_BASELINE_CLOSURE=FINITE_CLOSURES['baseline139'],TOTAL_TRIAL_CORRECTION_CLOSURE=FINITE_CLOSURES['coupled_correction'],TOTAL_TRIAL_FIXED_BINDING=SELECTED_DATA_MAP[:2],POINT_TOTAL_TRIAL_AUTHOR_DRAFT=False,POINT_TOTAL_TRIAL_AUTHORING_IN_PROGRESS=False,POINT_TOTAL_TRIAL_BASELINE_CLOSURE=FINITE_CLOSURES['baseline139'],POINT_TOTAL_TRIAL_CORRECTION_CLOSURE=FINITE_CLOSURES['coupled_correction'],FRESH_TRIAL_RESIDUAL_AUTHOR_DRAFT=False,FRESH_TRIAL_RESIDUAL_AUTHORING_IN_PROGRESS=False,FRESH_TRIAL_OWNER_BINDING=SELECTED_DATA_MAP[:2])
 for iq,fixed in enumerate(data['fixed_columns']):assert fixed['provenance']==provenance['columns'][iq] and fixed['point_TOTAL']['provenance']==fixed['provenance']
 finite_stage('INPUT',dict(data=data,correction=correction,trial_provenance=provenance))
 prepared=prepare_point_TOTAL_trial_fields(data['previous_configuration'],correction,basis,data['fixed_columns'],provenance,finite_capture,'NEW_finite_point_TOTAL',finite_stage)
 columns=[];indexes=[]
 for iq,fixed in enumerate(data['fixed_columns']):
  CONTEXT.update(active_component='new_finite_column',active_column=iq,active_label='NEW_finite_column%d'%iq)
  column=point_TOTAL_trial_fields_to_column(prepared,iq,fixed,finite_capture,'NEW_finite_column%d'%iq,finite_stage);columns.append(column)
  indexes.append(finite_stage('COLUMN_INDEX',dict(column=iq,h=column['geometry']['h'],ih=column['geometry']['ih'],mu=column['geometry']['mu'],York_target=column['york']['target'],phase_p=column['phase']['values']['p'],phase_H=column['phase']['values']['H'],phase_u=column['phase']['values']['u'],phase_H_operation_envelope=column['phase']['eos']['H_operation_envelope'],completed_column_stage_refs=column['completed_stages'],point_TOTAL_association=column['point_TOTAL_association_record'])))
 CONTEXT.update(active_component='new_fixed_label_sheet',active_column=None,active_label='NEW_finite_sheet_geometry')
 sheet=total_trial_fields_to_sheet(prepared,data['sheet_source'],finite_capture,'NEW_finite_sheet_geometry',finite_stage)
 residual_provenance=coupled_canonical(m['residual_provenance']);residual_provenance.update(owner_binding=SELECTED_DATA_MAP[:2],source_pins=FRESH_TRIAL_SOURCE_PINS)
 CONTEXT.update(active_component='new_finite_residual',active_label='NEW_finite_residual')
 result=fresh_trial_residual_packet(prepared,columns,data['mean_labels'],data['Hbar'],sheet,data['sheet_source'],data['sheet_labels'],data['priors'],data['normal_test'],data['scalar_test'],residual_provenance,finite_capture,P.check,'NEW_finite_residual',finite_stage)
 CONTEXT.update(active_component='original_six_measurement',active_column=None,active_label='NEW_finite_original_six')
 six=finite_original_six(result,data['original_six_references'],'NEW_finite_original_six');assessment=finite_stage('ORIGINAL_SIX_MEASURED',six)
 expected={'NEW_finite_residual_sheet_polynomial_transpose'}|{'NEW_finite_residual_NEW_global_'+family+'_'+n+'_polynomial_transpose' for family in ('value','delta') for n in ('normal','CMC')}
 assert {c['name'] for c in CHECKS}==expected and len(CHECKS)==len(expected)==5 and all(c['passed'] is True and c['tolerance']==2e-11 for c in CHECKS),'Exact source-derived NEW five-control inventory'
 assert dict(Counter(r['metadata']['completed_stage_name'] for r in RECORDS))==EXPECTED_STAGE_COUNTS,'Exact source-derived completed child inventory'
 return dict(status='COUPLED_POINT_TOTAL_FRESH_NONLINEAR_FINITE_RESIDUAL_MEASURED_UNQUALIFIED',input_source_map=SELECTED_DATA_MAP,closures=FINITE_CLOSURES,trial_fields=prepared['total_fields_record'],columns=indexes,sheet=sheet['record'],readout=result['record'],original_six_measurement=assessment,original_six_measured_admitted=six['all_original_six_measured_admitted'],original_whole_correction_authorities=ORIGINAL_WHOLE_CORRECTION_AUTHORITIES,fresh_feedback_authority=FRESH_FEEDBACK_AUTHORITY,fresh_feedback_required=True,frozen_proxy_feedback_substituted=False,normal_CMC_source_unsigned_admission_not_supplied_by_transpose_bounds=True,stationarity_canonical_normal_CMC_or_galaxy_admitted=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root FULL peer review and exclusive release required'
 assert not list(BASE.glob(STEM+'_*'));initialize_finite_continuation();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(IO_PARENT,IO_PARENT_SHA)
  for file,h in PINS.items():bind(file,h)
  m=finite_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],selected_map=SELECTED_DATA_MAP,closures=FINITE_CLOSURES,input_sha256=INPUTS,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=finite_packet(m)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;closing_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_point_TOTAL_finite_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:closing_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=closing_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
