"""HELD compact NEW139 three-chi point-coefficient worker. Root alone executes.
Hydrate earned genuine point TOTAL state; no old current/EOS/value/target replay.
Three NEW (1,0) unit-jet derivatives are numerical proxy coefficients only.
Original290 whole correction and fresh94/138/158 finite residual stay authoritative.
"""

from pathlib import Path

from datetime import datetime,timezone

from fractions import Fraction

import ast,hashlib,json,math,os,types,traceback

BASE=Path(__file__).resolve().parent

AUTHOR_DRAFT=True

AUTHORING_IN_PROGRESS=False

IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'

IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'

SUPPORT_SOURCE=('cross_u_cached_updated_phase_compact_chi_contact_v003.py','4f6f6c2db02bfe97e2c4132e16fc592050c3a3cd23876eaf96e4589b871dc2ab')

SUPPORT_NAMES={'selected_definitions','load_io','read_closed','clear_completed','seal_completed','initialize_helpers','cached_chi_admission','hydrate_chi_column'}

COMPONENT_PROTOCOL=('CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V001.md','14f9c9d3a8970bed81bdd771b9ba0c5030c280439a84c9506cf825bc1b567aa3')

WHOLE_COMPONENT_PROTOCOL=('CANDIDATE_WHOLE_CONFIGURATION_YORK_CONTACT_V001.md','7b9acfdd2dfad89587d79166e8e0e8bbdf32b2e1613db1bbb0cf1659ed39be68')

PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_candidate_phase_normal_stress_v001.py': 'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_fixed_geometry_phase_normal_join_v001.py': '7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_fixed_canonical_ordinary_v001.py': '2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_candidate_finite_phase_state_update_v001.py': 'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b', 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py': 'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10', 'author_fragment_cached_phase_chi_fraction_reference_v001.py': '414ed54d382a1e644a7a8ba9847881d1b53fa2e76d480de7b4c223cf00940b43', 'author_fragment_phase_literal_charge_hessian_v002.py': '293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143', 'author_fragment_candidate_literal_phase_mass_v001.py': '0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38', 'author_fragment_cached_updated_phase_temporal_normal_v002.py': 'b60d4bc3823439910843f10661dc960035bdad9af78ff3326cd4bc702474bf44', 'author_fragment_cached_phase_rate_fraction_reference_v001.py': '0a9dcc2f6caef474dc43766b44a5e43290734098c35c5b90669230f2e29a9af7', 'author_fragment_finite_candidate_configuration_contact_v001.py': '7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41', 'author_fragment_finite0_completed_state_restore_v002.py': 'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59', 'author_fragment_candidate_whole_configuration_york_contact_v001.py': '0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd', 'cross_u_cached_updated_phase_temporal_normal_controls_v002.py': 'e1449a16eae52f69494b03aa906a8e0d3ddda1c7c0f9fad060fa1fc80889f1ca', 'cross_u_candidate_right_only_mechanical_response_v001.py': 'e5ce23b048f0fac3d507c5b4bc068713154d9c896140ee041457fdc1fa130c6d'}

JOIN_SOURCE=('cross_u_fixed_geometry_phase_normal_canonical_value_join_v002.py', '28e8cb501975c4fd20660ce022a54c0ab9c677dc00108399e76fe023f870755b')

JOIN_RESULT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RESULT.json', 'd382c372ac74e581beee2a491ae4a143cf24a6c73dd87fd0565044a6041fd9ed', 'FIXED_GEOMETRY_PHASE_UPDATED_FOUR_NORMAL_CANONICAL_VALUES_MEASURED')

JOIN_RECEIPT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RECEIPT.json', '2f331b3a45b1e5dfe25114ab4d3f0d90528029b9d3d060c2809c1d691f7d31b6', 'CLOSED')

JOIN_PROOF=('ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_V001.json', '3bc8ea72625fbcda04440f9bc80dfde01b1aeb30804a555b84771c2b899651ae', 'ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_VERIFIED')

MASS_SOURCE=('cross_u_updated_finite_phase_mass_preparation_v002.py', '76a929447f2a0ed968825872e57ce2cf309fb49eeff13a1d8916ae3becb374cc')

MASS_RESULT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RESULT.json', '9febbd8cd23e96efbec23ffb6d24323d8b2ac99aaef5e73ce903bf49660b47c5', 'UPDATED_FINITE_PHASE_LITERAL_MASS_CACHE_PREPARED_UNQUALIFIED')

MASS_RECEIPT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RECEIPT.json', '69e25ed8a9c413f7c153a69e976a9f36cb3636fd67a8193eb3138514a2be2872', 'CLOSED')

MASS_PROOF=('ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_V001.json', '2b6d27847c8b70d592209d117dbc18f7ee0e41f8ed454d684734ec03d92ed662', 'ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_VERIFIED')

POINT_CELLS=((42, 21), (42, 22), (43, 21), (43, 22))

SHAPES={'g': (4, 4), 'hi': (4, 4), 'U': (4,), 'uc': (4,), 'P': (4, 4), 'phi': (4,), 'N': (), 'mu': (), 'h': (3, 3), 'beta': (3,), 'ih': (3, 3), 'u': (3,)}

ANCHOR_SOURCE=('cross_u_candidate_reference_york_anchor_canonical_packet_v004.py', '184d850aee263a6d4957c7df632c7bd928d6804d9c43978489c5b6abda02b5d7')

ANCHOR_RESULT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RESULT.json', '94220e4f2c37e16239a261143ef498b9d935ed234a91d9c95b3119fce75d3352', 'REFERENCE_YORK_ANCHOR_TARGET_AND_CANONICAL_EPSILON_MEASURED')

ANCHOR_RECEIPT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RECEIPT.json', '2aa42aef8e9a8a45f7f902f223092640f461703dac71b8bf103918f4425abeee', 'CLOSED')

ANCHOR_PROOF=('ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_V001.json', '1b43fc07b4c51c64b1798575f1f1aec48005761bf744f6d981d37b52071d2e4a', 'ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_VERIFIED')

CHI_RECOVERY_SOURCE=('cached_updated_phase_chi_saved_publication_recovery_v003.py', 'af34519717f0fd159d87865f9589a8361c750705ec9e90e34645331aaae05e9c')

CHI_RECOVERY_RESULT=('CACHED_UPDATED_PHASE_CHI_SAVED_PUBLICATION_RECOVERY_V003_RESULT.json', '4bd7ff16795f1ae6bfcb284a259505a206cc8bdd5266452b7ec62c20a84f94ef', 'CACHED_UPDATED_PHASE_ORIGINAL_COMPACT_CHI_CONTACT_SAVED_RECOVERED')

CHI_RECOVERY_RECEIPT=('CACHED_UPDATED_PHASE_CHI_SAVED_PUBLICATION_RECOVERY_V003_RECEIPT.json', '50b09751cb82b43724c30f2cf1a6afc10a9cbe4542114e820ee08059df10590d', 'CLOSED')

CHI_RECOVERY_PROOF=('ROOT_NATURAL_CLOSED_CACHED_PHASE_CHI_SAVED_RECOVERY_SUCCESS_SEALS_V001.json', '8b38a017b6eb58c96863645e86adcabb3a7d936ce24a3df8c37cd34e9687b680', 'ROOT_NATURAL_CLOSED_CACHED_PHASE_CHI_SAVED_RECOVERY_SUCCESS_SEALS_VERIFIED')

np=P=N=None

SCOPE={}

RAW={}

AVAILABLE={}

INPUTS={}

OUTPUTS={}

RECORDS=[]

CHECKS=[]

CONTEXT={}

DD_ARRAY_CURRENT={}

FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

REFERENCE_CONFIGURATION_SOURCE=('cross_u_candidate_whole_configuration_york_contact_v001.py','9660497e415caec2ec424c1f2e8d0a78ea5b3948b9ae52e38aa3e444c57ce747')

UNIT_COMPONENT=('author_fragment_candidate_configuration_three_unit_preparation_v001.py','1394e4ddf5eeefd4c44030635b0106550bb419dee74922e9e22d09107b5050fd')

UNIT_PROTOCOL=('CANDIDATE_CONFIGURATION_THREE_UNIT_PREPARATION_V001.md','568d960dea85cfba3a9785b44e89b9ab09edbd547ef1700f6b25c54f30e0f4af')

ADDITIONAL_PINS={
 'author_fragment_finite_candidate_native_EH_normal_v004.py':'27185f96e5ac8a00c8b1077ccedc9f2ced9399ed8379bdc16b2510926ae640a1',
 'author_fragment_configuration_current_CMC_unsigned_v001.py':'32da627c4107fe3155fcdbf1b200bbafb355749dfd7ae129950c675c952e8576',
 'author_fragment_configuration_normal_unsigned_v001.py':'6d56f02628a2dbceb2b896b4360f2c6a935560a36add1af291cad2750afe650f',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94'}

CHUNK_SIZE=128

STAGES=('DIRECTION','CONTACT','EOS','CURVATURE','ORDINARY','CURRENT_UNSIGNED','UNIT')

STEM='CROSS_U_NEW139_CONFIGURATION_THREE_UNIT_PREPARATION_V001'
DRIVER_PROTOCOL='CROSS_U_NEW139_CONFIGURATION_THREE_UNIT_PREPARATION_V001.md'
PROTOCOL_SHA=None
NEW139_FINITE_CLOSURE=(None,None,None,None)
NEW139_MECHANICAL_CLOSURE=(None,None,None,None)
CHUNK_SIZE=128
NEW139_COMPONENTS={
 'author_fragment_NEW139_mechanical_gauge_preparation_v002.py':'a0f549175fa058b983220342eeb9ee798049faf5a5d2f62690ebe8f51451a849',
 'author_fragment_NEW139_configuration_york_handoff_v001.py':'afb9b390ea2c28426c1839d93d70f9c2ef52b6d51301e23db2003f7fda48e716',
 'author_fragment_candidate_chunk_point_block_provider_v001.py':'4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625'}


def load_support():
 assert hashlib.sha256((BASE/SUPPORT_SOURCE[0]).read_bytes()).hexdigest()==SUPPORT_SOURCE[1]
 tree=ast.parse((BASE/SUPPORT_SOURCE[0]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in SUPPORT_NAMES];assert len(defs)==len(SUPPORT_NAMES)
 exec(compile(ast.Module(body=defs,type_ignores=[]),SUPPORT_SOURCE[0],'exec'),globals());load_io()

def initialize_configuration_helpers():
 initialize_helpers()
 more={'a_matvec','a_transpose','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','paired_current_affine_features','paired_current_affine_momenta','native_mask','metric_mask','dd_native_scatter','dd_metric_F','dd_metric_scatter'}
 exec(compile(selected_definitions(list(PINS)[1],more),list(PINS)[1],'exec'),SCOPE)
 exec(compile(selected_definitions(list(PINS)[0],{'scalar_scatter'}),list(PINS)[0],'exec'),SCOPE)
 SCOPE.update(B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 for n in more|{'scalar_scatter','B','GC','C','ALPHA','ELL'}:setattr(P,n,SCOPE[n])
 aliases=more|{'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','normal_keep_pair','scalar_mask','scalar_lift','scalar_scatter','dd_scalar_scatter','B','GC','C','ALPHA','ELL'}
 globals().update({n:SCOPE[n] for n in aliases})
 selections=(('author_fragment_finite_york_spacetime_first_jets_v001.py',20,None),('author_fragment_compact_metric_contact_momenta_v002.py',7,None),('author_fragment_finite_candidate_configuration_contact_v001.py',5,None),('author_fragment_finite_candidate_native_EH_normal_v003.py',8,None),('author_fragment_finite_fixed_canonical_ordinary_v001.py',1,None),('author_fragment_finite0_completed_state_restore_v002.py',8,None),('author_fragment_candidate_whole_configuration_york_contact_v001.py',12,None),('cross_u_cached_updated_phase_temporal_normal_controls_v002.py',1,{'admit_current_mass'}),('cross_u_candidate_right_only_mechanical_response_v001.py',2,{'closed_packet','selected_record'}))
 for file,count,names in selections:
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if names is None else names;assert len(names)==count,file
  if file=='author_fragment_finite0_completed_state_restore_v002.py':
   for n in tree.body:
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('FINITE0_RESTORE_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals().update(WHOLE_CONFIGURATION_YORK_AUTHOR_DRAFT=False,WHOLE_CONFIGURATION_YORK_AUTHORING_IN_PROGRESS=False,FINITE_ORDINARY_AUTHOR_DRAFT=False)

def whole_configuration_admission():
 refs=cached_chi_admission();mass=admit_current_mass(refs);anchor,arc=closed_packet(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF);case=anchor['case']
 assert anchor['owner']['pid']==21562 and len(anchor['checkpoints'])==6 and len(anchor['controls'])==5
 assert case['prepared_metric_target_is_exact_owned_reference'] is True and case['free_prior_or_target_refitted'] is case['new_varying_target_JVP'] is case['physical_adoption'] is False
 assert case['original_input']==thin(refs['input']) and case['original_basis']==thin(refs['basis']) and case['old_loads']==thin(refs['loads']) and case['phase_normal_join']==thin(refs['joined_readout'])
 inp=selected_record(case['input'],anchor,arc);canonical=selected_record(case['canonical'],anchor,arc);columns=[selected_record(q,anchor,arc) for q in case['columns']]
 assert canonical['metadata']['input']==thin(inp) and canonical['metadata']['mechanical_current_unchanged_under_phase_update'] is True
 assert canonical['metadata']['phase_normal_canonical_join']==thin(refs['joined_readout']) and canonical['metadata']['current_finite_phase_columns']==[thin(q['new']) for q in refs['columns']]
 for iq,q in enumerate(columns):
  assert q['metadata']['column']==iq and q['metadata']['state']==thin(refs['columns'][iq]['state']) and q['metadata']['current_finite_phase']==thin(refs['columns'][iq]['new'])
  assert q['metadata']['rho_W_t_exact_zero'] is q['metadata']['FY_reconstruction_is_comparison_only'] is True and q['metadata']['target_authority']=='Pi_owned both original words unchanged'
 chi,crc=closed_packet(CHI_RECOVERY_SOURCE,CHI_RECOVERY_RESULT,CHI_RECOVERY_RECEIPT,CHI_RECOVERY_PROOF)
 assert chi['owner']['pid']==25319 and len(chi['controls'])==47 and chi['case']['roles']==26 and chi['case']['new_scientific_actions']==chi['case']['new_controls']==0
 assert chi['case']['normal_terminal']==json.loads(json.dumps(refs['normal_terminal'])) and chi['case']['finite_terminal']==json.loads(json.dumps(refs['finite_terminal'])) and chi['case']['join_terminal']==json.loads(json.dumps(refs['join_terminal']))
 proof=json.loads(P.path(refs['normal_terminal'][3][0]).read_text());owner=proof['owner'];assert owner['pid']==97585
 context=dict(owner=owner,source_sha256=owner['source_sha256'],receipt_status='CLOSED',result_sha256=refs['normal_terminal'][1][1],receipt_sha256=refs['normal_terminal'][2][1],closure_proof_sha256=refs['normal_terminal'][3][1],closed_metadata_authenticated=True)
 refs.update(mass=mass,anchor=dict(input=inp,canonical=canonical,columns=columns,terminal=(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF)),chi_recovery_terminal=(CHI_RECOVERY_SOURCE,CHI_RECOVERY_RESULT,CHI_RECOVERY_RECEIPT,CHI_RECOVERY_PROOF),closed_recovery_context=context)
 return refs

def hydrate_configuration_column(refs,source,iq,H,eH):
 schema=source['state']['metadata']['schema'];names=finite0_completed_state_names(schema)+tuple(n for n in schema if n.startswith('unchanged_mean_labels_'))
 raw=read_closed(source['state'],names)
 for n,x in raw.items():keep('column%d_copied_STATE_'%iq+n,x)
 restored=finite0_restore_completed_state(raw,refs['input']['metadata'],source['state']['metadata'],closed_recovery_proof=refs['closed_recovery_context'])
 phase,old_direction,rows,old_normals,index=hydrate_chi_column(source,iq)
 normal_s=dict(restored['s'],phi=phase['s']['phi']);normal_c=restored['c'];sl=slice(iq*3784,(iq+1)*3784)
 assert all(np.array_equal(a,b) for a,b in zip(phase['values']['H'],P.a_slice(H,sl)))
 finite=read_closed(source['new'],('NEW_finite_phase_column%d_NEW_invariant_H_operation_envelope'%iq,));assert np.array_equal(eH[sl],finite['NEW_finite_phase_column%d_NEW_invariant_H_operation_envelope'%iq])
 labels=finite0_saved_pair_family(raw,'unchanged_mean_labels_');labels.update(existing_once_counted_branch_registered=True,provenance=dict(reference=refs['input']['metadata']['refs']['mean_columns'][iq],same_registered_antipodal_rule=True,candidate_volume_or_radial_rescale=False))
 assert labels['radiation_weights'][0].shape==(128,3784) and labels['radiation_covectors'][0].shape==(128,3784,3)
 yref=refs['anchor']['columns'][iq];mapping=dict(h='candidate_h',ih='candidate_inverse',mu='candidate_volume',h_spatial_jets='candidate_h_spatial_jets',T='candidate_T',kappa='candidate_inverse_trace',trace_part='candidate_trace_part_quotient',inverse_lam='inverse_weight_quotient',FY_target='candidate_target',tau='candidate_trace_coordinate')
 ynames=tuple('NEW_FY_reference_anchor_'+v+'_'+w for v in mapping.values() for w in ('hi','lo'))+tuple(n+'_'+w for n in ('authoritative_exact_reference_target','NEW_anchor_L_maps') for w in ('hi','lo'))+('unchanged_owned_input_chart_ih','unchanged_owned_input_chart_sqrt_h')
 ydata=read_closed(yref,ynames)
 for n,x in ydata.items():keep('column%d_copied_anchor_'%iq+n,x)
 york={n:pair_from(ydata,'NEW_FY_reference_anchor_'+v) for n,v in mapping.items()};york['target']=pair_from(ydata,'authoritative_exact_reference_target')
 reference=dict(L_maps=pair_from(ydata,'NEW_anchor_L_maps'),target_raising_inverse=ydata['unchanged_owned_input_chart_ih'],mu_owned=ydata['unchanged_owned_input_chart_sqrt_h'])
 normal_data={};prefixes=[]
 for rp,data in rows:normal_data.update(data);prefixes.append(rp)
 geometry,model,gauge,covectors,mechanical,old_phase,material,E0=restored['inputs']
 provenance=dict(updated_phase_state_owner=13764,same_candidate_geometry_and_current_mechanical_rates=True,fixed_reference_longitudinal_chart=True,original_state=thin(source['state']),finite_phase_column=thin(source['new']),joined_normal_rows=[thin(q) for q in source['joined_rows']],anchor_column=thin(yref),current_H_mass=thin(refs['mass']['preparation']),physical_adoption=False)
 return dict(candidate=restored['candidate'],geometry=geometry,gauge=gauge,covectors=covectors,mechanical=mechanical,reference=E0,phase=phase,normal_s=normal_s,normal_c=normal_c,phase_normal_data=normal_data,phase_normal_prefixes=prefixes,phase_normal_provenance=provenance,mean_labels=labels,york=york,york_reference=reference,provenance=provenance),restored['Hbar']

def initialize_unit_helpers():
 initialize_configuration_helpers()
 selections=((ADDITIONAL_PINS.keys().__iter__().__next__(),8,None),
  ('author_fragment_configuration_current_CMC_unsigned_v001.py',1,None),
  ('author_fragment_configuration_normal_unsigned_v001.py',1,None),
  ('author_fragment_candidate_weak_mechanical_positive_v001.py',7,{'mp_out','mp_add','mp_mul','mp_div','mp_sum','mp_mm','mp_mv'}),
  (UNIT_COMPONENT[0],3,None))
 for file,count,names in selections:
  tree=ast.parse(P.path(file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
  assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 globals().update(CONFIGURATION_UNIT_AUTHOR_DRAFT=False,CONFIGURATION_UNIT_AUTHORING_IN_PROGRESS=False,
  CONFIGURATION_CURRENT_UNSIGNED_AUTHOR_DRAFT=False,CONFIGURATION_CURRENT_UNSIGNED_AUTHORING_IN_PROGRESS=False,
  CONFIGURATION_NORMAL_UNSIGNED_AUTHOR_DRAFT=False,CONFIGURATION_NORMAL_UNSIGNED_AUTHORING_IN_PROGRESS=False)
 assert all(getattr(P,n)==SCOPE[n] for n in ('B','GC','C','ALPHA','ELL'))
 for n in ('a_dd','a_slice','a_add','a_mul','a_stack','normal_pair_sum'):assert globals()[n] is getattr(P,n)
 assert P.a_mul.__globals__ is SCOPE and P.a_mul64.__globals__ is SCOPE

def unit_control_names(iq,lo,jet):
 label='column%d_chunk%d_unit%d'%(iq,lo,jet)
 return [label+'_'+n+'_source_unsigned_enclosure' for n in ('mechanical','phase','normal','CMC')]

def initialize_NEW139_units():
 initialize_unit_helpers()
 for file in NEW139_COMPONENTS:
  bind(file,NEW139_COMPONENTS[file]);tree=ast.parse(P.path(file).read_text())
  names={'candidate_point_provider_admission','candidate_point_cache_names'} if 'chunk_point' in file else None
  defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
  assert len(defs)==(2 if names is not None else 6 if 'mechanical_gauge' in file else 3),file
  for n in tree.body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith(('NEW139_','POINT_','MECHANICAL_')):
    globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 globals().update(NEW139_GAUGE_AUTHOR_DRAFT=False,NEW139_CONFIGURATION_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHOR_DRAFT=False,
  NEW139_GAUGE_FINITE_CLOSURE=NEW139_FINITE_CLOSURE,NEW139_CONFIGURATION_FINITE_CLOSURE=NEW139_FINITE_CLOSURE,
  NEW139_GAUGE_MECHANICAL_CACHE_CLOSURE=NEW139_MECHANICAL_CLOSURE,
  MECHANICAL_SOURCE=NEW139_MECHANICAL_CLOSURE[0],MECHANICAL_RESULT=NEW139_MECHANICAL_CLOSURE[1],
  MECHANICAL_RECEIPT=NEW139_MECHANICAL_CLOSURE[2],MECHANICAL_CLOSURE_PROOF=NEW139_MECHANICAL_CLOSURE[3])

def NEW139_unit_admission():
 refs=whole_configuration_admission();finite,rc=closed_packet(*NEW139_FINITE_CLOSURE);case=finite['case']
 assert case['status']==finite['status']=='FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED'
 assert case['spatial_geometry_unchanged'] is case['current99_and_physical6_fresh'] is case['all16normal_ports_per_section'] is True and case['physical_adoption'] is False
 mechanical=candidate_point_provider_admission(bind);assert thin(mechanical['original_basis'])==thin(refs['basis'])
 selected=[]
 for iq,source in enumerate(refs['columns']):
  stages={}
  for role in NEW139_GAUGE_ROLES:
   matches=[q for q in finite['checkpoints'] if q['metadata'].get('kind')==role and q['metadata'].get('column')==iq]
   assert len(matches)==1,(iq,role);stages[role]=selected_record(matches[0],finite,rc)
  assert stages['BASELINE_COLUMN_INPUT']['metadata']['state']==thin(source['state']) and stages['BASELINE_COLUMN_INPUT']['metadata']['phase_rows']==[thin(q) for q in source['joined_rows']]
  for role in NEW139_GAUGE_ROLES[1:]:
   assert stages[role]['metadata']['provenance']['state']==thin(source['state']) and stages[role]['metadata']['provenance']['phase_rows']==[thin(q) for q in source['joined_rows']]
  assert thin(stages['RATE_STATE_COLUMN'])==thin(case['columns'][iq])
  assert finite['case']['columns'][iq]['metadata']['provenance']['state']==thin(source['state'])
  assert mechanical['caches'][iq]['metadata']['state']==thin(source['state'])
  selected.append(stages)
 inputs=[q for q in finite['checkpoints'] if q['metadata']['kind']=='INPUT'];assert len(inputs)==1
 inp=selected_record(inputs[0],finite,rc);provenance=inp['metadata']['provenance']
 assert provenance['original_fixed_references_verified'] is provenance['all_source_seals_authenticated'] is True
 assert provenance['original_owned_TOTAL_time_words']==[thin(q['state']) for q in refs['columns']]
 closures=dict(phase=refs['finite_terminal'],normal_phase_join=refs['join_terminal'],York_anchor=refs['anchor']['terminal'],material=refs['normal_terminal'])
 globals()['NEW139_CONFIGURATION_INVARIANT_CLOSURES']=closures
 refs.update(NEW139_finite=finite,NEW139_receipt=rc,NEW139_stages=selected,NEW139_input=inp,mechanical_cache=mechanical,invariant_closures=closures)
 return refs

def compact_stage(role,payload,metadata):
 clear_completed();capture_families('completed_'+role+'_',payload)
 return seal_completed(role,metadata)

def hydrate_NEW139_configuration(refs,source,iq,H,eH):
 invariant,Hbar=hydrate_configuration_column(refs,source,iq,H,eH)
 fixed=dict(invariant,updated_phase_pair=invariant['phase']['s']['phi'])
 ref=refs['mechanical_cache']['caches'][iq];data=read_closed(ref,candidate_point_cache_names(ref['metadata']));prefix=POINT_CACHE_PREFIX
 pair=lambda n:tuple(data[prefix+n+'_'+w].copy() for w in ('hi','lo'));ep=prefix+'copied_positive_coefficient_'
 cache=dict(s={n:data[prefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:data[prefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a.copy() for n,a in data.items() if n.startswith(ep)},constants=ref['metadata']['constants'],candidate_provenance=ref['metadata']['candidate_provenance'],configuration_held=True)
 selected={role:dict(ref=thin(q),metadata=q['metadata'],data=read_closed(q,tuple(n for n in q['metadata']['schema'] if n.startswith('completed_BASELINE_COLUMN_INPUT_candidate_s_') or n.startswith('completed_BASELINE_COLUMN_INPUT_candidate_c_')) if role=='BASELINE_COLUMN_INPUT' else tuple(n for n in q['metadata']['schema'] if n.startswith('completed_'+role+'_')))) for role,q in refs['NEW139_stages'][iq].items()}
 admission=dict(finite_closure=NEW139_FINITE_CLOSURE,mechanical_cache_closure=NEW139_MECHANICAL_CLOSURE,source_pins=NEW139_GAUGE_SOURCE_PINS,column=iq,finite_owner=refs['NEW139_finite']['owner'],selected_records={role:thin(q) for role,q in refs['NEW139_stages'][iq].items()},material_constants={n:getattr(P,n) for n in ('B','GC','ALPHA','ELL','C')},all_selected_NEW139_seals_authenticated=True,all_original_support_seals_authenticated=True,same_original_basis_verified=True,same_fixed_geometry_and_gauge_verified=True,same_fixed_mechanical_raw_E0_verified=True,original_targets_unchanged=True,physical_adoption=False)
 mech=prepare_NEW139_mechanical_gauge_column(fixed,selected,cache,admission,keep,'NEW139_config_column%d'%iq,lambda role,payload:compact_stage(role,payload,dict(column=iq,source_records=admission['selected_records'],mechanical_gauge_ports_not_evaluated=True)))
 invariant['closed_source_refs']=dict(state=thin(source['state']),phase=thin(source['new']),phase_rows=[thin(q) for q in source['joined_rows']],York=thin(refs['anchor']['columns'][iq]),mass=thin(refs['mass']['preparation']))
 adm=dict(finite_closure=NEW139_FINITE_CLOSURE,invariant_closures=refs['invariant_closures'],source_pins=NEW139_CONFIGURATION_SOURCE_PINS,column=iq,updated_phase_state_owner=13764,material_constants=admission['material_constants'],mechanical_hydration_record=mech['input_record'],NEW139_selected_records=mech['source_records'],invariant_source_refs=invariant['closed_source_refs'],original_basis_record=thin(refs['basis']),Hbar=Hbar,all_invariant_seals_authenticated=True,same_original_basis_and_fixed_sources_verified=True,same_original_priors_and_York_reference_verified=True,same_phase_operands_verified=True,same_fixed_geometry_and_gauge_verified=True,physical_adoption=False)
 column=prepare_NEW139_configuration_york_column(mech,invariant,adm,keep,'NEW139_config_column%d'%iq,lambda role,payload:compact_stage(role,payload,dict(column=iq,fresh_mechanical_input=mech['input_record'],invariant_sources=invariant['closed_source_refs'])))
 return column,Hbar

def compact_unit_packet(refs):
 basis=read_closed(refs['basis'],('R','dv','hats','cell_i','cell_j'));mass=read_closed(refs['mass']['preparation'],tuple('updated_phase_mass_candidate_H_'+w for w in ('hi','lo'))+('updated_phase_mass_uncancelled_H_envelope',)+tuple('updated_phase_mass_NEW_basis_'+n for n in ('R','dv','hats')))
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],mass['updated_phase_mass_NEW_basis_'+n])
 H=pair_from(mass,'updated_phase_mass_candidate_H');eH=mass['updated_phase_mass_uncancelled_H_envelope']
 header=compact_stage('INPUT',dict(basis=basis),dict(finite_terminal=NEW139_FINITE_CLOSURE,mechanical_terminal=NEW139_MECHANICAL_CLOSURE,invariant_terminals=refs['invariant_closures'],basis=thin(refs['basis']),current_H=thin(refs['mass']['preparation']),point_TOTAL_baseline=True,coefficient_jet_order=['rho','rho_R','rho_Z'],source_units_only_no_old_directions=True))
 chunks=[];columns=[];expected_names=[];Hbar=None
 for iq,source in enumerate(refs['columns']):
  CONTEXT.update(column=iq,stage='hydrate_authentic_NEW139_TOTAL');column,hbar=hydrate_NEW139_configuration(refs,source,iq,H,eH)
  if Hbar is None:Hbar=hbar
  else:assert Hbar==hbar
  column_chunks=[]
  for lo in range(0,3784,128):
   hi=min(lo+128,3784);CONTEXT.update(column=iq,lo=lo,hi=hi,stage='NEW_unit_derivatives');chunk=qu_slice_column(column,slice(lo,hi));units=[];unit_refs=[]
   for jet in range(3):
    label='column%d_chunk%d_unit%d'%(iq,lo,jet);before=len(CHECKS);expected_names.extend(unit_control_names(iq,lo,jet));stages=[];ports=[]
    clear_completed();capture_families('active_chunk_',chunk)
    def stage_complete(stage,values,provenance):
     assert stage==STAGES[len(stages)];capture_families('completed_stage_'+stage+'_',values);stages.append(stage)
     # These are captured partials, not fictitious independently committed roles.
     return dict(stage=stage,captured_in_current_unit=True)
    def test_complete(row,test_jet,values,provenance):
     assert (row,test_jet)==divmod(len(ports),4);capture_families('completed_port%d_'%len(ports),values);ports.append([row,test_jet])
     return dict(row=row,jet=test_jet,captured_in_current_unit=True)
    out=candidate_configuration_unit_response(chunk,jet,Hbar,keep,P.check,label,stage_complete,test_complete)
    assert stages==list(STAGES) and ports==[[r,j] for r in range(4) for j in range(4)] and [q['name'] for q in CHECKS[before:]]==unit_control_names(iq,lo,jet)
    ur=compact_stage('UNIT',out,dict(column=iq,lo=lo,hi=hi,unit=jet,input=thin(header),configuration_cache=column['configuration_cache_record'],completed_stage_names=stages,completed_port_inventory=ports,controls=CHECKS[before:],source_terms_before_cancellation=True,broad_235_scratch_not_copied=True,physical_adoption=False));unit_refs.append(thin(ur));units.append(out)
   coefficients={};envelopes={}
   for field in ('mechanical','phase','normal','CMC'):
    pairs=[]
    for out in units:
     part=out['response'];dm=part['contact']['delta_momenta']
     x=tuple(np.concatenate((dm['native_density'][w],dm['metric_total_density'][w]),axis=1) for w in (0,1)) if field=='mechanical' else part['eos']['delta']['p'] if field=='phase' else part['normal_coefficients'] if field=='normal' else part['initial_CMC_density'];pairs.append(x)
    coefficients[field]=P.a_stack(pairs,-1);envelopes[field]=np.stack([q['source_envelope']['fields'][field] for q in units],-1)
   q=compact_stage('COEFFICIENT_CHUNK',dict(coefficients=coefficients,envelopes=envelopes),dict(column=iq,lo=lo,hi=hi,chunk_ordinal=30*iq+lo//128,input=thin(header),units=unit_refs,same_candidate_provenance=chunk['provenance'],configuration_jet_order=['rho','rho_R','rho_Z'],original290_whole_correction_authority=True,York_W_t_sheet_and_global_scatter_external=True,exact_DD_linearity_or_uniform_association_qualified=False));chunks.append(thin(q));column_chunks.append(thin(q));clear_completed();del chunk,units
  cr=compact_stage('COLUMN_INDEX',dict(Hbar=np.asarray(Hbar)),dict(column=iq,chunks=column_chunks,configuration_cache=column['configuration_cache_record'],same_candidate_provenance=column['provenance'],point_TOTAL_baseline=True));columns.append(thin(cr));del column
 expected_roles=['INPUT']+(['NEW139_MECHANICAL_GAUGE_INPUT','NEW139_CONFIGURATION_CACHE']+(['UNIT']*3+['COEFFICIENT_CHUNK'])*30+['COLUMN_INDEX'])*4+['PREPARATION']
 assert [q['name'] for q in CHECKS]==expected_names and len(set(expected_names))==len(expected_names)==1440 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 preparation=compact_stage('PREPARATION',dict(chunk_count=np.asarray(len(chunks)),Hbar=np.asarray(Hbar)),dict(input=thin(header),chunks=chunks,columns=columns,basis=thin(refs['basis']),finite_terminal=NEW139_FINITE_CLOSURE,invariant_terminals=refs['invariant_closures'],same_candidate_provenance=[q['metadata']['same_candidate_provenance'] for q in RECORDS if q['metadata']['role']=='COLUMN_INDEX'],controls=1440,point_TOTAL_baseline=True,represented_coefficient_source_enclosure_only=True,original290_whole_correction_and_fresh_finite_authority=True,reduced_stage_complete=False,physical_adoption=False))
 assert [q['metadata']['role'] for q in RECORDS]==expected_roles and len(chunks)==120 and len(RECORDS)==494
 return dict(status='NEW139_THREE_CHI_COEFFICIENTS_AND_SOURCE_ENVELOPES_PREPARED_UNQUALIFIED',input=thin(header),preparation=thin(preparation),chunks=chunks,columns=columns,controls=1440,roles=len(RECORDS),finite_terminal=NEW139_FINITE_CLOSURE,mechanical_terminal=NEW139_MECHANICAL_CLOSURE,invariant_terminals=refs['invariant_closures'],original_targets_or_rates_refitted=False,old_q3_or_whole_direction_replayed=False,uniform290_DD_or_global_inverse_qualified=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and CHUNK_SIZE==128,'Root FULL review and release required'
 assert all(x is not None for c in (NEW139_FINITE_CLOSURE,NEW139_MECHANICAL_CLOSURE) for pin in c for x in pin),'Future natural closures required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for ref in (UNIT_COMPONENT,UNIT_PROTOCOL,COMPONENT_PROTOCOL,WHOLE_COMPONENT_PROTOCOL):bind(*ref)
  for n,h in {**PINS,**ADDITIONAL_PINS,**NEW139_COMPONENTS}.items():bind(n,h)
  initialize_NEW139_units();refs=NEW139_unit_admission()
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,point_chunk_bound=128,units=3,planned_roles=494,planned_controls=1440,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=compact_unit_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck()
  P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='NEW139_compact_unit_partial_and_active_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json')
  P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())

