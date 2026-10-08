"""HELD two NEW whole-grid fixed-rate configuration/York JVP measurements.
Only authenticated CLOSED words hydrate SAME225, updated13764 phase/15744 rows,
21562 FY operands and19724 H. No old current/EOS/action/target/solver replay.
Root alone releases/executes after whole source and distinct peer review.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_WHOLE_CONFIGURATION_YORK_CONTACT_V001'
DRIVER_PROTOCOL='CROSS_U_CANDIDATE_WHOLE_CONFIGURATION_YORK_CONTACT_V001.md'
PROTOCOL_SHA='d3945a99650a30837a1bf7a00908def8f41103af49a8bfca52ef18b8f9fde3a9'
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
DIRECTIONS=(
 dict(chi=((43,0,.125,2.**-65),(43,22,-.0625,-2.**-67)),W=((0,42,21,.03125,2.**-66),(1,43,22,-.015625,-2.**-67),(2,44,22,.0078125,2.**-68)),t=((43,22,.03125,2.**-66),)),
 dict(chi=((1,1,-.03125,2.**-66),(85,43,.015625,2.**-67)),W=((0,1,1,.0625,2.**-65),(1,85,43,.0078125,2.**-68),(2,43,0,-.015625,2.**-67)),t=((86,44,.125,2.**-65),(86,22,-.0625,-2.**-66),(43,44,.03125,2.**-67))))
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)


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


def hydrate_sheet(refs):
 ref=refs['sheet'];names=tuple(n for n in ref['metadata']['schema'] if n.startswith(('completed_sheet_geometry_geometry_','completed_sheet_geometry_gauge_','fixed_label_ordinary_fixed_galaxy_','fixed_label_ordinary_fixed_reference_dust_','fixed_label_ordinary_fixed_radiation_')) or n in ('fixed_label_sheet_fixed_R','fixed_label_sheet_fixed_Z','fixed_label_sheet_rho_fixed_indices','fixed_label_sheet_rho_fixed_right_weight'))
 data=read_closed(ref,names)
 for n,x in data.items():keep('copied_original_sheet_'+n,x)
 geometry={n:pair_from(data,'completed_sheet_geometry_geometry_'+n) for n in ('h','ih','mu')};gauge={n:pair_from(data,'completed_sheet_geometry_gauge_'+n) for n in ('N','beta')}
 labels={n:pair_from(data,'fixed_label_ordinary_'+v) for n,v in dict(galaxy_mass_weight='fixed_galaxy_mass',galaxy_specific_covector='fixed_galaxy_covector',reference_dust_energy_weight='fixed_reference_dust_energy',radiation_weights='fixed_radiation_weights',radiation_covectors='fixed_radiation_covectors').items()}
 labels.update(existing_once_counted_branch_registered=True,provenance=ref['metadata']['reference'])
 return dict(indices=data['fixed_label_sheet_rho_fixed_indices'],right_weight=data['fixed_label_sheet_rho_fixed_right_weight'],R=data['fixed_label_sheet_fixed_R'],Z=data['fixed_label_sheet_fixed_Z'],geometry=geometry,gauge=gauge,labels=labels,provenance=dict(same_fixed_positions_and_labels=True,closed_sheet=thin(ref),original_reference=ref['metadata']['reference'],physical_adoption=False))


def configuration_control_names(case):
 label='direction%d_NEW_whole_configuration'%case
 return [label+'_column%d_York_actual_trace_JVP'%iq for iq in range(4)]+[label+'_'+n+'_polynomial_transpose' for n in ('native','metric','phase','York_target')]+[label+'_normal_CMC_'+n+'_polynomial_transpose' for n in ('normal','CMC')]+[label+'_fixed_label_sheet_polynomial_transpose']


def configuration_packet(refs):
 global REFS
 REFS=refs;basis=read_closed(refs['basis'],('R','dv','hats','cell_i','cell_j'));mass=read_closed(refs['mass']['preparation'],tuple('updated_phase_mass_candidate_H_'+w for w in ('hi','lo'))+('updated_phase_mass_uncancelled_H_envelope',)+tuple('updated_phase_mass_NEW_basis_'+n for n in ('R','dv','hats')))
 for n,x in basis.items():keep('unchanged_original_basis_'+n,x)
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],mass['updated_phase_mass_NEW_basis_'+n])
 H=pair_from(mass,'updated_phase_mass_candidate_H');eH=mass['updated_phase_mass_uncancelled_H_envelope'];fy_keep('copied_current19724_H',H,keep);keep('copied_current19724_eH',eH)
 header=seal_completed('INPUT',dict(kind='closed_same_candidate_configuration_York_sources',original_input=thin(refs['input']),basis=thin(refs['basis']),normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],anchor_terminal=refs['anchor']['terminal'],mass_terminal=refs['mass']['terminal'],chi_recovery_terminal=refs['chi_recovery_terminal'],directions=DIRECTIONS,expected_control_names=[n for case in range(len(DIRECTIONS)) for n in configuration_control_names(case)],original_targets_or_epsilon_refitted=False,physical_adoption=False));clear_completed();columns=[];cached=[];Hbar=None
 for iq,source in enumerate(refs['columns']):
  CONTEXT.update(column=iq,stage='hydrate_closed_configuration_York_column');col,hbar=hydrate_configuration_column(refs,source,iq,H,eH)
  if Hbar is None:Hbar=hbar
  else:assert Hbar==hbar
  record=seal_completed('CACHE_COLUMN',dict(kind='copied_same225_updated_phase_normal_and_York_direction_operands',input=thin(header),column=iq,state=thin(source['state']),finite_phase=thin(source['new']),normal_rows=[thin(q) for q in source['joined_rows']],anchor_column=thin(refs['anchor']['columns'][iq]),mass_preparation=thin(refs['mass']['preparation']),EOS_current_action_curvature_or_target_replayed=False,physical_adoption=False));cached.append(thin(record));columns.append(col);clear_completed()
 sheet=hydrate_sheet(refs);sr=seal_completed('SHEET_CACHE',dict(kind='copied_fixed_positions_labels_and_completed_sheet_geometry',input=thin(header),sheet=thin(refs['sheet']),no_metric_interpolation_or_sheet_geometry_replay=True,physical_adoption=False));clear_completed()
 names=tuple('NEW_reference_anchor_'+n+'_'+k+'_'+w for n in ('current_candidate_weak','unchanged_or_prepared_target','target_minus_current_epsilon') for k in ('native','metric') for w in ('hi','lo'));canonical=read_closed(refs['anchor']['canonical'],names)
 groups={g:{k:pair_from(canonical,'NEW_reference_anchor_'+n+'_'+k) for k in ('native','metric')} for g,n in (('current','current_candidate_weak'),('priors','unchanged_or_prepared_target'),('epsilon','target_minus_current_epsilon'))}
 current=read_closed(refs['current'],tuple(n+'_'+w for n in ('NEW_finite_phase_NEW_finite_literal_weak','NEW_finite_phase_NEW_target_minus_finite_current') for w in ('hi','lo')));prior=read_closed(refs['prior'],('fixed_literal_weak_phase_charge_hi','fixed_literal_weak_phase_charge_lo'))
 groups['current']['phase']=pair_from(current,'NEW_finite_phase_NEW_finite_literal_weak');groups['priors']['phase']=pair_from(prior,'fixed_literal_weak_phase_charge');groups['epsilon']['phase']=pair_from(current,'NEW_finite_phase_NEW_target_minus_finite_current')
 provenance=dict(updated_phase_state_owner=13764,fixed_reference_longitudinal_chart=True,normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],anchor_terminal=refs['anchor']['terminal'],mass_terminal=refs['mass']['terminal'],physical_adoption=False)
 prepared=prepare_candidate_whole_configuration_york(columns,basis,sheet,groups['current'],groups['priors'],groups['epsilon'],provenance,keep,'NEW_whole_configuration_preparation')
 pr=seal_completed('PREPARATION',dict(kind='same_state_whole_configuration_York_cached_prerequisites',input=thin(header),cached_columns=cached,sheet_cache=thin(sr),original_current_prior_epsilon_words_unchanged=True,dimension=18745,reduced_stage_complete=False,physical_adoption=False));clear_completed();outputs=[]
 probes=dict(normal=np.zeros((4,87,45)),CMC=np.zeros((87,45)),native=np.zeros((33,3,87,45)),metric=np.zeros((6,87,45)),phase=np.zeros((87,45)))
 probes['normal'][:,43,22]=(1.,2.,3.,4.);probes['normal'][[0,1,3],43,0]=(2.,-1.,.5);probes['CMC'][43,22]=1.;probes['CMC'][86,44]=.5;probes['phase'][43,22]=1.;probes['phase'][86,44]=-.25;probes['native'][0,0,43,22]=1.;probes['native'][1,1,43,22]=2.;probes['native'][2,2,43,22]=3.;probes['metric'][:,43,22]=np.arange(1.,7.)
 for case,entries in enumerate(DIRECTIONS):
  CONTEXT.update(direction=case,stage='NEW_declared_configuration_direction');direction={n:P.a_dd(np.zeros(shape)) for n,shape in dict(chi=(87,45),W=(3,87,45),t=(87,45)).items()}
  for n,values in entries.items():
   for entry in values:
    key=tuple(entry[:-2]);direction[n][0][key]=entry[-2];direction[n][1][key]=entry[-1]
   cq_keep('direction%d_nodes_'%case+n,direction[n],keep)
  for n,x in probes.items():keep('direction%d_probe_'%case+n,x)
  dr=seal_completed('DIRECTION',dict(kind='NEW_two_word_original_coordinate_configuration_direction',direction=case,input=thin(header),preparation=thin(pr),entries=entries,sheet_chi_exercised=(case==0),free_outer_top_total_trace_exercised=(case==1),expected_control_names=configuration_control_names(case),physical_adoption=False));clear_completed();rowrefs=[];colrefs=[];before=len(CHECKS)
  def row_complete(iq,row,jet,data):
   CONTEXT.update(direction=case,column=iq,row=row,jet=jet,stage='seal_NEW_configuration_normal_test');capture_families('completed_NEW_normal_',data)
   q=seal_completed('NORMAL_TEST',dict(kind='NEW_configuration_four_normal_test_direction',direction=case,column=iq,row=row,jet=jet,input=thin(header),direction_record=thin(dr),cache=cached[iq],relative_phase_count=1,ordinary_mean_count=1,physical_adoption=False));rowrefs.append(thin(q));clear_completed();return thin(q)
  def column_complete(iq,part):
   CONTEXT.update(direction=case,column=iq,stage='seal_NEW_configuration_column');capture_families('completed_NEW_column_',part)
   q=seal_completed('COLUMN',dict(kind='NEW_fixed_rate_configuration_York_contact_column',direction=case,column=iq,input=thin(header),direction_record=thin(dr),cache=cached[iq],normal_tests=rowrefs[-16:],normal_coordinate_order=['value','R','Z','t'],current_primitive_and_York_anchor_gaps_retained=True,reduced_stage_complete=False,physical_adoption=False));colrefs.append(thin(q));clear_completed();return thin(q)
  out=candidate_whole_configuration_york_contact(prepared,direction,Hbar,probes,keep,P.check,'direction%d_NEW_whole_configuration'%case,column_complete=column_complete,test_complete=row_complete)
  assert [q['name'] for q in CHECKS[before:]]==configuration_control_names(case) and len(rowrefs)==4*16 and len(colrefs)==4
  capture_families('completed_NEW_whole_configuration_',out)
  record=seal_completed('FULL_WEAK',dict(kind='NEW_whole_configuration_York_canonical_literal_phase_normal_CMC_JVP',direction=case,input=thin(header),direction_record=thin(dr),columns=colrefs,normal_tests=rowrefs,controls=CHECKS[before:],mechanical_phase_temporal_response_and_epsilon_feedback_external=True,original_six_canonical_restoration_not_evaluated=True,reduced_stage_complete=False,physical_adoption=False));outputs.append(thin(record));clear_completed()
 expected_roles=['INPUT']+['CACHE_COLUMN']*4+['SHEET_CACHE','PREPARATION']+(['DIRECTION']+(['NORMAL_TEST']*16+['COLUMN'])*4+['FULL_WEAK'])*len(DIRECTIONS);expected_names=[n for case in range(len(DIRECTIONS)) for n in configuration_control_names(case)]
 assert [q['metadata']['role'] for q in RECORDS]==expected_roles and [q['name'] for q in CHECKS]==expected_names and len(expected_names)==len(set(expected_names)) and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 return dict(status='WHOLE_CONFIGURATION_YORK_CANONICAL_NORMAL_CMC_CONTACTS_MEASURED',input=thin(header),preparation=thin(pr),cached_columns=cached,sheet_cache=thin(sr),readouts=outputs,normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],anchor_terminal=refs['anchor']['terminal'],mass_terminal=refs['mass']['terminal'],chi_recovery_terminal=refs['chi_recovery_terminal'],directions=DIRECTIONS,expected_control_names=expected_names,controls=len(expected_names),roles=len(expected_roles),fixed_rate_partial_only=True,old_current_EOS_action_target_or_solver_replayed=False,original_targets_and_epsilon_unchanged=True,reduced_stage_complete=False,canonical_normal_CMC_finite_state_or_physical_adoption=False,physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root full review and guarded release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(*COMPONENT_PROTOCOL);bind(*WHOLE_COMPONENT_PROTOCOL)
  for n,h in PINS.items():bind(n,h)
  initialize_configuration_helpers();refs=whole_configuration_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,directions=DIRECTIONS,expected_control_names=[n for case in range(len(DIRECTIONS)) for n in configuration_control_names(case)],expected_roles=147,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=configuration_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(CHECKS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_NEW_whole_configuration_York_contact',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
