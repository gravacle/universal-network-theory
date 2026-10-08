"""HELD actual SAME225 three-unit configuration coefficient preparation; no author execution."""
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
STEM='CROSS_U_CANDIDATE_CONFIGURATION_THREE_UNIT_PREPARATION_V002'
DRIVER_PROTOCOL='CROSS_U_CANDIDATE_CONFIGURATION_THREE_UNIT_PREPARATION_V002.md'
PROTOCOL_SHA='cdf9ebf4dbfffc97fa430fade8f7c017fa3ef041d941a87aa3574cc90669a3ef'

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

def unit_packet(refs):
 global REFS
 REFS=refs
 basis=read_closed(refs['basis'],('R','dv','hats','cell_i','cell_j'))
 mass=read_closed(refs['mass']['preparation'],tuple('updated_phase_mass_candidate_H_'+w for w in ('hi','lo'))+('updated_phase_mass_uncancelled_H_envelope',)+tuple('updated_phase_mass_NEW_basis_'+n for n in ('R','dv','hats')))
 for n,a in basis.items():keep('unchanged_original_basis_'+n,a)
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],mass['updated_phase_mass_NEW_basis_'+n])
 H=pair_from(mass,'updated_phase_mass_candidate_H');eH=mass['updated_phase_mass_uncancelled_H_envelope'];fy_keep('copied_current19724_H',H,keep);keep('copied_current19724_eH',eH)
 expected_names=[n for iq in range(4) for lo in range(0,3784,CHUNK_SIZE) for jet in range(3) for n in unit_control_names(iq,lo,jet)]
 expected_roles=['INPUT'];chunk_records=[];contexts=[];Hbar=None
 header=seal_completed('INPUT',dict(kind='closed_SAME225_updated_phase_three_NEW_local_chi_jet_columns',basis=thin(refs['basis']),original_input=thin(refs['input']),normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],anchor_terminal=refs['anchor']['terminal'],mass_terminal=refs['mass']['terminal'],chi_recovery_terminal=refs['chi_recovery_terminal'],point_chunk_bound=CHUNK_SIZE,expected_control_names=expected_names,old_q22_or_completed_whole_direction_replayed=False,physical_adoption=False));clear_completed()
 for iq,source in enumerate(refs['columns']):
  CONTEXT.update(column=iq,stage='hydrate_closed_configuration_operands');column,hbar=hydrate_configuration_column(refs,source,iq,H,eH)
  if Hbar is None:Hbar=hbar
  else:assert hbar==Hbar
  clear_completed();keep('closed_column_Hbar',np.asarray(hbar));keep('closed_column_point_count',np.asarray(len(column['candidate']['c']['N'])))
  cr=seal_completed('COLUMN_CONTEXT',dict(kind='closed_column_operand_lineage_only',column=iq,input=thin(header),state=thin(source['state']),finite_phase=thin(source['new']),joined_rows=[thin(q) for q in source['joined_rows']],anchor=thin(refs['anchor']['columns'][iq]),current_H=thin(refs['mass']['preparation']),hydration_only_no_primal_producer=True,physical_adoption=False));contexts.append(thin(cr));expected_roles.append('COLUMN_CONTEXT');clear_completed()
  for lo in range(0,3784,CHUNK_SIZE):
   hi=min(lo+CHUNK_SIZE,3784);CONTEXT.update(column=iq,lo=lo,hi=hi,stage='copy_closed_point_chunk')
   chunk=qu_slice_column(column,slice(lo,hi));assert len(chunk['candidate']['c']['N'])==hi-lo
   capture_families('copied_closed_chunk_',chunk)
   cache=seal_completed('CACHE_CHUNK',dict(kind='bitcopied_closed_SAME225_updated_phase_and_reference_operands',column=iq,lo=lo,hi=hi,column_context=thin(cr),input=thin(header),source=source['state']['metadata']['owner'],same_candidate_provenance=chunk['provenance'],old_direction_or_EOS_value_action_replayed=False,physical_adoption=False));expected_roles.append('CACHE_CHUNK');clear_completed()
   units=[];unit_refs=[];unit_stages=[];normal_refs=[];normal_position=0;stage_position=0
   for jet in range(3):
    label='column%d_chunk%d_unit%d'%(iq,lo,jet);before=len(CHECKS);stages=[];rows=[]
    def complete_stage(stage,values,provenance):
     nonlocal stage_position
     assert stage==STAGES[stage_position];stage_position+=1
     # Completed returned objects carry resumption state; signed/unsigned
     # internal scratch stays available on failures until this stage commits.
     clear_completed();CONTEXT.update(column=iq,lo=lo,hi=hi,unit=jet,stage=stage)
     capture_families('completed_NEW_'+stage+'_',values)
     q=seal_completed('UNIT_'+stage,dict(kind='NEW_local_configuration_unit_completed_stage',column=iq,lo=lo,hi=hi,unit=jet,stage=stage,input=thin(header),cache=thin(cache),completed_stages=stages.copy(),normal_rows=rows.copy(),provenance=provenance,controls=CHECKS[before:] if stage=='UNIT' else [],source_terms_before_final_cancellation=True,physical_adoption=False))
     stages.append(thin(q));expected_roles.append('UNIT_'+stage);clear_completed();return thin(q)
    def complete_test(row,test_jet,values,provenance):
     nonlocal normal_position
     assert (row,test_jet)==divmod(normal_position,4);normal_position+=1
     clear_completed();CONTEXT.update(column=iq,lo=lo,hi=hi,unit=jet,row=row,jet=test_jet,stage='NORMAL_TEST')
     capture_families('completed_NEW_normal_',values)
     q=seal_completed('NORMAL_TEST',dict(kind='NEW_fixed_rate_unit_normal_coefficient_and_source_envelope',column=iq,lo=lo,hi=hi,unit=jet,row=row,jet=test_jet,coordinate_order=['value','R','Z','t'],input=thin(header),cache=thin(cache),completed_stages=stages.copy(),completed_rows=rows.copy(),provenance=provenance,relative_phase_count=1,ordinary_mean_count=1,source_terms_before_final_cancellation=True,physical_adoption=False))
     rows.append(thin(q));expected_roles.append('NORMAL_TEST');clear_completed();return thin(q)
    out=candidate_configuration_unit_response(chunk,jet,Hbar,keep,P.check,label,complete_stage,complete_test)
    assert stage_position==len(STAGES) and normal_position==16 and len(stages)==7 and len(rows)==16
    assert [q['name'] for q in CHECKS[before:]]==unit_control_names(iq,lo,jet)
    units.append(out);unit_refs.append(stages[-1]);unit_stages.append(stages.copy());normal_refs.append(rows.copy());stage_position=0;normal_position=0
   coefficients={};envelopes={}
   for field in ('mechanical','phase','normal','CMC'):
    pairs=[]
    for out in units:
     part=out['response']
     if field=='mechanical':
      dm=part['contact']['delta_momenta'];x=tuple(np.concatenate((dm['native_density'][w],dm['metric_total_density'][w]),axis=1) for w in (0,1))
     else:x=part['eos']['delta']['p'] if field=='phase' else part['normal_coefficients'] if field=='normal' else part['initial_CMC_density']
     pairs.append(x)
    coefficients[field]=qu_pair('completed_chunk_coefficient_'+field,P.a_stack(pairs,-1),keep)
    envelopes[field]=keep('completed_chunk_source_unsigned_'+field,np.stack([out['source_envelope']['fields'][field] for out in units],-1))
   keep('completed_chunk_configuration_jet_order',np.asarray([0,1,2],dtype=np.int64))
   outref=seal_completed('COEFFICIENT_CHUNK',dict(kind='NEW_three_unit_frozen_coefficient_columns_with_independent_source_envelopes',column=iq,lo=lo,hi=hi,input=thin(header),cache=thin(cache),unit_records=unit_refs,stage_records=unit_stages,normal_records=normal_refs,same_candidate_provenance=chunk['provenance'],configuration_jet_order=['rho','rho_R','rho_Z'],fields=dict(mechanical=105,phase=1,normal=[4,4],CMC=1),W_trace_York_target_and_sheet_external=True,source_coefficient_law_only=True,exact_DD_Jacobian_or_uniform290_association_qualified=False,physical_adoption=False));chunk_records.append(thin(outref));expected_roles.append('COEFFICIENT_CHUNK');clear_completed();del chunk,units
  del column
 assert [q['name'] for q in CHECKS]==expected_names and len(expected_names)==len(set(expected_names))
 assert all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 keep('completed_chunk_count',np.asarray(len(chunk_records)));keep('completed_unit_count',np.asarray(3*len(chunk_records)));keep('completed_control_count',np.asarray(len(CHECKS)))
 readout=seal_completed('READOUT',dict(kind='four_actual_sections_three_NEW_local_jet_columns',input=thin(header),column_contexts=contexts,coefficient_chunks=chunk_records,expected_control_names=expected_names,all_four_actual_sections=True,source_majorants_conditional_on_completed_actual_stages=True,original_targets_or_physics_refitted=False,physical_adoption=False));expected_roles.append('READOUT');clear_completed()
 assert [q['metadata']['role'] for q in RECORDS]==expected_roles
 return dict(status='CANDIDATE_THREE_CONFIGURATION_JET_COEFFICIENTS_AND_SOURCE_ENVELOPES_PREPARED_UNQUALIFIED',input=thin(header),readout=thin(readout),coefficient_chunks=chunk_records,expected_control_names=expected_names,controls=len(expected_names),roles=len(expected_roles),same_candidate_provenance=dict(normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],anchor_terminal=refs['anchor']['terminal'],mass_terminal=refs['mass']['terminal']),updated_phase_state_owner=13764,old_q22_or_whole_direction_replayed=False,source_coefficient_law_only=True,exact_DD_Jacobian_or_uniform290_association_qualified=False,W_trace_York_target_sheet_and_global_scatter_external=True,reduced_stage_complete=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and CHUNK_SIZE==128,'Root full review and release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for ref in (REFERENCE_CONFIGURATION_SOURCE,UNIT_COMPONENT,UNIT_PROTOCOL,COMPONENT_PROTOCOL,WHOLE_COMPONENT_PROTOCOL):bind(*ref)
  for n,h in {**PINS,**ADDITIONAL_PINS}.items():bind(n,h)
  initialize_unit_helpers();refs=whole_configuration_admission()
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,point_chunk_bound=CHUNK_SIZE,configuration_jet_order=['rho','rho_R','rho_Z'],old_q22_or_whole_direction_replayed=False,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=unit_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck()
  P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_three_unit_configuration_preparation',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json')
  P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
