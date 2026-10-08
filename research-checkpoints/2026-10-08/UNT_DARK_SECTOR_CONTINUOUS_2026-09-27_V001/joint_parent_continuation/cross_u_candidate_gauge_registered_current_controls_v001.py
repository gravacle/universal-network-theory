"""HELD actual SAME225 gauge-current component and64-port measurement.
Only CLOSED words hydrate. NEW directions/contacts and independent rational
references are evaluated after root release. All prior targets and source
qualifications remain unchanged; no old producer, EOS or action replay.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_GAUGE_REGISTERED_CURRENT_CONTROLS_V001'
DRIVER_PROTOCOL='CROSS_U_CANDIDATE_GAUGE_REGISTERED_CURRENT_CONTROLS_V001.md'
PROTOCOL_SHA='19a321a18e1d3504154ac87db3106e9b1e1e37675cdbcadacaa3363a31f14ee2'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
SUPPORT_SOURCE=('cross_u_cached_updated_phase_compact_chi_contact_v003.py', '4f6f6c2db02bfe97e2c4132e16fc592050c3a3cd23876eaf96e4589b871dc2ab')
SUPPORT_NAMES={'clear_completed', 'initialize_helpers', 'read_closed', 'selected_definitions', 'seal_completed', 'load_io', 'cached_chi_admission'}
MECHANICAL_SUPPORT_SOURCE=('cross_u_candidate_mechanical_rate_normal_controls_v001.py', 'c766f885e6f28659e61998058c5e5399f7c12a53749e1306fa0d4d5fc0f06223')
MECHANICAL_SUPPORT_NAMES={'mechanical_rate_admission', 'hydrate_mechanical_rate_column', 'load_support', 'initialize_mechanical_rate_helpers'}
CHI_SUPPORT_NAMES={'hydrate_chi_column', 'rational_control'}
POINT_CELLS=((42, 21), (42, 22), (43, 21), (43, 22))
SHAPES={'g': (4, 4), 'hi': (4, 4), 'U': (4,), 'uc': (4,), 'P': (4, 4), 'phi': (4,), 'N': (), 'mu': (), 'h': (3, 3), 'beta': (3,), 'ih': (3, 3), 'u': (3,)}
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_candidate_phase_normal_stress_v001.py': 'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_fixed_geometry_phase_normal_join_v001.py': '7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_fixed_canonical_ordinary_v001.py': '2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_candidate_finite_phase_state_update_v001.py': 'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b', 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py': 'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10', 'author_fragment_cached_phase_chi_fraction_reference_v001.py': '414ed54d382a1e644a7a8ba9847881d1b53fa2e76d480de7b4c223cf00940b43', 'author_fragment_phase_literal_charge_hessian_v002.py': '293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143', 'author_fragment_candidate_literal_phase_mass_v001.py': '0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38', 'author_fragment_cached_updated_phase_temporal_normal_v002.py': 'b60d4bc3823439910843f10661dc960035bdad9af78ff3326cd4bc702474bf44', 'author_fragment_cached_phase_rate_fraction_reference_v001.py': '0a9dcc2f6caef474dc43766b44a5e43290734098c35c5b90669230f2e29a9af7', 'author_fragment_finite_candidate_configuration_contact_v001.py': '7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41', 'author_fragment_finite0_completed_state_restore_v002.py': 'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59', 'author_fragment_candidate_whole_configuration_york_contact_v001.py': '0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_mechanical_rate_normal_contact_v001.py': 'db9e749646132e7db23184b9ec22086a9654d1537d1768c8f11298ecbd5b6aad', 'author_fragment_candidate_gauge_registered_current_contact_v001.py': 'ac0502f41c6ad04208f5ef5610d43b3e11064a4b66eb73d076d43c959ffb0cdd', 'author_fragment_gauge_chart_firstjet_fraction_reference_v001.py': '7f844b6bb2bf0f8e63b151b0d35c3e936f42f3ed0d8c23ae550191719ac6d854'}
COMPONENT_PROTOCOLS=(('CANDIDATE_GAUGE_REGISTERED_CURRENT_CONTACT_V001.md', '9a51839d44aec928a4ae937b3da9115394796c8a9a28f74c1d7febfa18a02c1f'), ('GAUGE_CHART_FIRSTJET_FRACTION_REFERENCE_V001.md', '977132142159c40f9a01c6aface7a94bb803d34d1c0e08d9594ba8e914381cd6'))
OWNED_NORMAL_SOURCE=(None,None)
OWNED_NORMAL_RESULT=(None,None,'FINITE0_NEW_ACTION_CURRENT_NORMAL_CMC_RESIDUAL_MEASURED')
OWNED_NORMAL_RECEIPT=(None,None,'CLOSED')
OWNED_NORMAL_PROOF=(None,None,'ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED')
OWNED_FINITE_SOURCE=(None,None)
OWNED_FINITE_RESULT=(None,None,'CANDIDATE_FINITE_PHASE_STATE_AND_LITERAL_CURRENT_MEASURED')
OWNED_FINITE_RECEIPT=(None,None,'CLOSED')
OWNED_FINITE_PROOF=(None,None,'ROOT_NATURAL_CLOSED_FINITE_PHASE_STATE_SUCCESS_SEALS_VERIFIED')
OWNED_JOIN_SOURCE=(None,None)
OWNED_JOIN_RESULT=(None,None,'FIXED_GEOMETRY_PHASE_UPDATED_FOUR_NORMAL_CANONICAL_VALUES_MEASURED')
OWNED_JOIN_RECEIPT=(None,None,'CLOSED')
OWNED_JOIN_PROOF=(None,None,'ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_VERIFIED')
OWNED_MECHANICAL_SOURCE=(None,None)
OWNED_MECHANICAL_RESULT=(None,None,'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
OWNED_MECHANICAL_RECEIPT=(None,None,'CLOSED')
OWNED_MECHANICAL_PROOF=(None,None,'ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
CHART_FAMILIES=('g','hi','U','z','dg','du','dz','Ga','dens','K','metric_EH_density')
EOS_FAMILIES=('X2','X','q','u','s','pressure','PX','PXX','J','registered_J','p','registered_p','H','registered_H','reduced_H','density','current_gap','density_gap','hessian_gap','reduced_gap')
CHAIN_FAMILIES=tuple(n+'_chain_'+k for n in ('P','PX','PXX') for k in ('actual','expected','gap'))
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};REFERENCE_METADATA=[]
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def load_support():
 assert hashlib.sha256((BASE/SUPPORT_SOURCE[0]).read_bytes()).hexdigest()==SUPPORT_SOURCE[1]
 tree=ast.parse((BASE/SUPPORT_SOURCE[0]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in SUPPORT_NAMES];assert len(defs)==len(SUPPORT_NAMES)
 exec(compile(ast.Module(body=defs,type_ignores=[]),SUPPORT_SOURCE[0],'exec'),globals());load_io()

def initialize_mechanical_rate_helpers():
 initialize_helpers()
 base={'dd_native_node_value','dd_metric_node_value','metric_R_matrix','scalar_scatter'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 SCOPE.update(B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 for n in base|primitive|{'B','GC','C','ALPHA','ELL'}:setattr(P,n,SCOPE[n]);globals()[n]=SCOPE[n]
 globals().update({n:SCOPE[n] for n in ('a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape')})
 selections=(('author_fragment_finite_york_spacetime_first_jets_v001.py',20,None),('author_fragment_compact_metric_contact_momenta_v002.py',7,None),('author_fragment_finite_candidate_configuration_contact_v001.py',5,None),('author_fragment_finite_candidate_native_EH_normal_v003.py',8,None),('author_fragment_finite0_completed_state_restore_v002.py',8,None),('author_fragment_candidate_whole_configuration_york_contact_v001.py',6,{'cq_keep','cq_zero','cq_join','candidate_configuration_normal_CMC_direction','candidate_configuration_canonical_functional','cq_six'}),('author_fragment_candidate_specialized_temporal_action_v001.py',6,None),('author_fragment_candidate_chunk_point_block_provider_v001.py',2,{'candidate_point_provider_admission','candidate_point_cache_names'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',8,{'mp_out','mp_add','mp_mul','mp_div','mp_sum','mp_mm','mp_mv','candidate_mechanical_positive_point'}),('author_fragment_candidate_mechanical_rate_normal_contact_v001.py',1,{'candidate_mechanical_rate_normal_column'}))
 for file,count,names in selections:
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if names is None else names;assert len(names)==count,file
  for n in tree.body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith(('FINITE0_RESTORE_','POINT_')):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals().update(MECHANICAL_RATE_NORMAL_AUTHOR_DRAFT=False,MECHANICAL_RATE_NORMAL_AUTHORING_IN_PROGRESS=False,POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False)
 # a_mul and a_mul64 retain the previously installed repaired arithmetic SCOPE.
 assert SCOPE['a_prod'] is P.a_prod and SCOPE['a_mul'].__globals__ is SCOPE

def mechanical_rate_admission():
 refs=cached_chi_admission();cache=candidate_point_provider_admission(bind)
 assert cache['closed_provenance']['owner']['pid']==13576 and cache['preparation']['metadata']['basis']==thin(refs['basis'])
 original=cache['input']['metadata'];assert original['original_input']==thin(refs['input']) and original['loads']==thin(refs['loads'])
 proof=json.loads(P.path(refs['normal_terminal'][3][0]).read_text());owner=proof['owner'];assert owner['pid']==97585
 context=dict(owner=owner,source_sha256=owner['source_sha256'],receipt_status='CLOSED',result_sha256=refs['normal_terminal'][1][1],receipt_sha256=refs['normal_terminal'][2][1],closure_proof_sha256=refs['normal_terminal'][3][1],closed_metadata_authenticated=True)
 for iq,(source,cr) in enumerate(zip(refs['columns'],cache['caches'])):
  md=cr['metadata'];assert md['column']==iq and md['state']==thin(source['state']) and md['candidate_provenance']['state']==thin(source['state']) and md['candidate_provenance']['input']==thin(refs['input'])
  schema=source['state']['metadata']['schema']
  for n,shape in (('Q',[3784]),('V',[3784,3])):
   for w in ('hi','lo'):assert schema['completed_curvature_'+n+'_value_'+w]['shape']==shape and schema['completed_curvature_'+n+'_value_'+w]['dtype']=='float64'
 refs.update(mechanical_cache=cache,closed_recovery_context=context);return refs

def hydrate_mechanical_rate_column(refs,source,iq):
 schema=source['state']['metadata']['schema'];prefixes=('completed_candidate_s_','completed_candidate_c_','completed_candidate_jets_','completed_candidate_features_','completed_candidate_momenta_','completed_candidate_KADM_','candidate_raw_coefficient_operation_','candidate_raw_new_first_operation_','NEW_reference_input_geometry_','NEW_reference_input_gauge_','NEW_reference_input_covectors_','NEW_reference_input_mechanical_','NEW_reference_input_reference_','candidate_raw_unchanged_material_')
 names=tuple(n for n in schema if n.startswith(prefixes))+tuple('completed_curvature_'+n+'_value_'+w for n in ('Q','V') for w in ('hi','lo'))
 assert len(names)==len(set(names));data=read_closed(source['state'],names)
 for n,a in data.items():keep('column%d_copied_STATE_'%iq+n,a)
 md=source['state']['metadata'];im=refs['input']['metadata'];ownership=finite0_validate_saved_transaction_ownership(im,md,refs['closed_recovery_context']);raw=lambda p:finite0_saved_raw_family(data,p);pairs=lambda p:finite0_saved_pair_family(data,p)
 for n in ('B','GC','ALPHA','ELL','C'):assert data['candidate_raw_unchanged_material_'+n].item()==getattr(P,n)
 s=raw('completed_candidate_s_');c=raw('completed_candidate_c_');feature=dict(constants={n:s[n] for n in ('g','hi','U','z','P','uc','Z','r','z2','f','phi','omega','xi','w')},paired=pairs('completed_candidate_features_'),configuration_changed=False,candidate_configuration_rebuilt=True)
 candidate=dict(s=s,c=c,jets=pairs('completed_candidate_jets_'),features=feature,momenta=pairs('completed_candidate_momenta_'),KADM=finite0_saved_pair(data,'completed_candidate_KADM'),coefficient_envelopes=raw('candidate_raw_coefficient_operation_'),positive_first_jet_envelopes=raw('candidate_raw_new_first_operation_'),physical_adoption=False)
 geometry=pairs('NEW_reference_input_geometry_');gauge=pairs('NEW_reference_input_gauge_');covectors=pairs('NEW_reference_input_covectors_');mechanical=pairs('NEW_reference_input_mechanical_');reference=pairs('NEW_reference_input_reference_')
 curvature={n:finite0_saved_pair(data,'completed_curvature_'+n+'_value') for n in ('Q','V')};curvature['physical_adoption']=False
 finite=read_closed(source['new'],tuple('NEW_finite_phase_column%d_phase_covector_updated_'%iq+w for w in ('hi','lo')));phi=pair_from(finite,'NEW_finite_phase_column%d_phase_covector_updated'%iq);fy_keep('column%d_copied_updated13764_phase'%iq,phi,keep)
 assert phi[0].shape==phi[1].shape==(3784,4) and all(np.array_equal(a[:,1:],b[:,1:]) for a,b in zip(phi,P.a_dd(s['phi'])))
 cr=refs['mechanical_cache']['caches'][iq];cachedata=read_closed(cr,candidate_point_cache_names(cr['metadata']))
 for n,a in cachedata.items():keep('column%d_copied13576_'%iq+n,a)
 prefix=POINT_CACHE_PREFIX;pair=lambda n:pair_from(cachedata,prefix+n);ep=prefix+'copied_positive_coefficient_'
 cache=dict(s={n:cachedata[prefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:cachedata[prefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a.copy() for n,a in cachedata.items() if n.startswith(ep)},constants=cr['metadata']['constants'],candidate_provenance=cr['metadata']['candidate_provenance'],configuration_held=True)
 for n in POINT_S:assert np.array_equal(cache['s'][n],s[n])
 for n in POINT_C:assert np.array_equal(cache['c'][n],c[n])
 assert all(np.array_equal(a,b) for a,b in zip(cache['fixed_E0'],reference['E0']))
 bg,fixed=im['owned_background'],im['fixed'];Hbar=bg['h']*fixed['Hunit']/299792458.;assert Hbar>0 and np.isfinite(Hbar)
 provenance=dict(same_candidate_geometry_and_current_mechanical_rates=True,original_state=thin(source['state']),updated_phase=thin(source['new']),ownership=ownership,phi_only_update_leaves_native_EH_mechanical_action_invariant=True,physical_adoption=False)
 return dict(candidate=candidate,geometry=geometry,gauge=gauge,covectors=covectors,mechanical=mechanical,reference=reference,intrinsic_curvature=curvature,curvature_provenance=dict(closed_state=thin(source['state']),owner=md['owner'],same_fixed_spatial_geometry=True),updated_phase_pair=phi,provenance=provenance),cache,Hbar

def hydrate_chi_column(source,iq):
 names={n:'completed_candidate_'+('s_' if n in ('g','hi','U','uc','P','phi') else 'c_')+('sqrt_h' if n=='mu' else n) for n in SHAPES}
 dnames={n:'completed_contact_'+('d_' if n in ('g','hi','U','uc','P','phi') else 'dc_')+n for n in SHAPES}
 wanted=tuple(names.values())+tuple(n+'_'+w for n in dnames.values() for w in ('hi','lo'))+('predeclared_true_conformal_chi','predeclared_true_conformal_gradient')
 raw=read_closed(source['state'],wanted);values={};direction={}
 for n,name in names.items():
  a=keep('column%d_closed_raw_'%iq+n,raw[name].copy());assert a.shape==(3784,)+SHAPES[n] and a.dtype==np.float64;values[n]=P.a_dd(a)
  direction[n]=cached_phase_pair(raw,dnames[n],a.shape,keep,'column%d_original_chi_'%iq+n)
 for n in ('N','beta','u','phi'):assert all(np.all(a==0) for a in direction[n])
 index=np.asarray([44*i+j for i,j in POINT_CELLS],dtype=np.int64);off=np.ones(3784,dtype=bool);off[index]=False
 for n in SHAPES:assert all(np.all(a[off]==0) for a in direction[n]),'Original compact direction must have exactly its declared four-cell support'
 for n in ('predeclared_true_conformal_chi','predeclared_true_conformal_gradient'):keep('column%d_unchanged_'%iq+n,raw[n].copy());assert np.all(raw[n][off]==0)
 prefix='NEW_finite_phase_column%d_'%iq;wanted=cached_updated_phase_contact_names(prefix+'NEW_invariant_')+tuple(prefix+'phase_covector_'+n+'_'+w for n in ('before','increment','updated') for w in ('hi','lo'))
 finite=read_closed(source['new'],wanted);before=cached_phase_pair(finite,prefix+'phase_covector_before',(3784,4),keep,'column%d_phase_before'%iq);step=cached_phase_pair(finite,prefix+'phase_covector_increment',(3784,4),keep,'column%d_phase_step'%iq);updated=cached_phase_pair(finite,prefix+'phase_covector_updated',(3784,4),keep,'column%d_phase_updated'%iq)
 assert all(np.array_equal(a,b) for a,b in zip(before,values['phi'])) and all(np.all(a[:,1:]==0) for a in step) and all(np.array_equal(a[:,1:],b[:,1:]) for a,b in zip(before,updated));values['phi']=updated
 s={n:values[n] for n in ('g','hi','U','uc','P','phi')};c={n:values[n] for n in ('N','mu','h','beta','ih','u')}
 fixed=REFS['input']['metadata']['refs']['fixed'];assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 norm=cached_phase_pair(finite,prefix+'NEW_invariant_pressure_norm_value_denominator',(3784,),keep,'column%d_copied_registered_norm'%iq);X0=cached_phase_pair(finite,prefix+'NEW_invariant_q_value_denominator',(3784,),keep,'column%d_copied_registered_X0'%iq)
 for a in (norm,X0):assert np.all(a[1]==0) and np.all(a[0]==a[0][0])
 eta=fixed['Hunit']/299792458.;fac=2*eta*eta/1.98;Abar=1.5*fixed['OA']/fixed['rG'];A0=fac*Abar;assert X0[0][0]==100*eta
 constants=dict(eps=1e-5,norm=float(norm[0][0]),X0=float(X0[0][0]),A0=A0,C=1.98,eta=eta,synthetic_control=False,Hunit=fixed['Hunit'],OA=fixed['OA'],rG=fixed['rG'],relative_phase_coefficient=1.,physical_constants_selected_or_fitted=False)
 prepared=prepare_cached_updated_phase_contact(finite,prefix+'NEW_invariant_',s,c,constants,source['new']['metadata']['candidate_provenance'],keep,'column%d_cached_EOS'%iq)
 rows=[];caches=[]
 for row,ref in enumerate(source['joined_rows']):
  rp='NEW_phase_normal_join_column%d_row%d_NEW_literal_phase_'%(iq,row);data=read_closed(ref,cached_updated_phase_contact_names(rp,True));rows.append((rp,data));caches.append({n:pair_from(data,rp+NORMAL_NAMES[n]) for n in NORMAL_FIELDS})
 return prepared,direction,rows,caches,index

def rational_control(name,actual,targets):
 shape=actual[0].shape;eh=np.empty(shape);el=np.empty(shape);error=np.empty(shape);envelope=np.empty(shape);entries=[]
 def flatten(tree):
  if isinstance(tree,list):return [x for q in tree for x in flatten(q)]
  return [tree]
 for ordinal,q in enumerate([x for target in targets for x in flatten(target)]):
  key=np.unravel_index(ordinal,shape);value,bound=q[1],q[2];assert isinstance(value,Fraction) and isinstance(bound,Fraction)
  h=float(value);l=float(value-Fraction.from_float(h));remainder=value-Fraction.from_float(h)-Fraction.from_float(l);observed=Fraction.from_float(float(actual[0][key]))+Fraction.from_float(float(actual[1][key]));difference=abs(observed-value)
  eh[key]=h;el[key]=l;error[key]=0. if difference==0 else math.nextafter(float(difference),math.inf);envelope[key]=0. if bound==0 else math.nextafter(float(bound),math.inf)
  entries.append(dict(index=list(key),numerator=str(value.numerator),denominator=str(value.denominator),conversion_remainder_numerator=str(remainder.numerator),conversion_remainder_denominator=str(remainder.denominator),bound_numerator=str(bound.numerator),bound_denominator=str(bound.denominator),actual_error_numerator=str(difference.numerator),actual_error_denominator=str(difference.denominator)))
  CONTEXT['rational_reference_partial']=dict(name=name,entries=entries.copy())
 fy_keep(name+'_exact_Fraction_converted_target',(eh,el),keep);fy_keep(name+'_actual_selected_words',actual,keep);keep(name+'_exact_rational_error',error);keep(name+'_positive_rational_bound',envelope)
 REFERENCE_METADATA.append(dict(name=name,entries=entries));P.check(name,error,np.zeros(shape),envelope)

def initialize_gauge_helpers():
 # Reviewed support functions close over THIS shared namespace, never imports.
 initialize_mechanical_rate_helpers()
 exec(compile(selected_definitions(SUPPORT_SOURCE[0],CHI_SUPPORT_NAMES),SUPPORT_SOURCE[0],'exec'),globals())
 for file in ('author_fragment_candidate_gauge_registered_current_contact_v001.py','author_fragment_gauge_chart_firstjet_fraction_reference_v001.py'):
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)}
  assert len(names)==(6 if file.endswith('current_contact_v001.py') else 1)
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals().update(GAUGE_CURRENT_AUTHOR_DRAFT=False,GAUGE_CURRENT_AUTHORING_IN_PROGRESS=False,GAUGE_CHART_REFERENCE_AUTHOR_DRAFT=False,GAUGE_CHART_REFERENCE_AUTHORING_IN_PROGRESS=False)
 for stem,actual in (('NORMAL','NORMAL'),('FINITE','FINITE'),('JOIN','JOIN'),('MECHANICAL','MECHANICAL')):
  for tail in ('SOURCE','RESULT','RECEIPT','PROOF'):
   name='OWNED_'+stem+'_'+tail;ref=globals()[name];assert all(x is not None for x in ref),name
   target=actual+('_CLOSURE_PROOF' if actual=='MECHANICAL' and tail=='PROOF' else '_'+tail);globals()[target]=ref
 for n in ('B','GC','C','ALPHA','ELL'):assert getattr(P,n)==SCOPE[n]==globals()[n]
 for n in ('a_dd','a_slice','a_add','a_mul','a_stack','normal_pair_sum','a_transpose'):assert globals()[n] is SCOPE[n]
 assert P.a_mul.__globals__ is SCOPE and SCOPE['a_prod'] is P.a_prod


def select_gauge_points(value,indices):
 if isinstance(value,np.ndarray):
  axes=[a for a,n in enumerate(value.shape) if n==3784];assert len(axes)<=1
  return np.take(value,indices,axis=axes[0]).copy() if axes else value.copy()
 if isinstance(value,dict):return {n:select_gauge_points(x,indices) for n,x in value.items()}
 if isinstance(value,tuple):return tuple(select_gauge_points(x,indices) for x in value)
 if isinstance(value,list):return [select_gauge_points(x,indices) for x in value]
 return value


def gauge_component_direction(p,case):
 zero=lambda shape:P.a_dd(np.zeros(shape));direction=dict(N=zero((p,)),beta=zero((p,3)),N_jets=zero((p,4)),beta_jets=zero((p,4,3)))
 assert case in (0,1)
 if case==0:
  direction['N'][0][:]=.125;direction['N'][1][:]=2.**-63
  direction['beta'][0][:]=(.25,-.125,.0625);direction['beta'][1][:]=(2.**-62,-2.**-63,2.**-64)
 for a in range(4):
  direction['N_jets'][0][:,a]=(a+1)*(-1. if a%2 else 1.)/32;direction['N_jets'][1][:,a]=(a+1)*2.**-67
  for i in range(3):direction['beta_jets'][0][:,a,i]=(a+1)*(i+1)*(-1. if (a+i)%2 else 1.)/64;direction['beta_jets'][1][:,a,i]=(a+i+1)*(-1. if i%2 else 1.)*2.**-69
 return direction


def gauge_component_control_names(case):
 prefix='component%d_NEW_gauge'%case
 return [prefix+'_chart_'+n for n in CHART_FAMILIES]+[prefix+'_EOS_'+n for n in EOS_FAMILIES]+[prefix+'_'+n for n in CHAIN_FAMILIES]


def gauge_locked_chart(label):
 root=label+'_NEW_gauge_mechanical_';suffix={'h_beta':'h_beta_owned_representative','z0_quotient':'z0_quotient_owned_representative','shift_inverse':'shift_inverse_value_quotient','current_dg':'current_dg','current_du':'current_du'}
 for a in range(4):
  for name in ('U0_first','U0_second','z0_first','z0_second'):suffix[name+'_'+str(a)]=name+'_'+str(a)+'_value_quotient'
 return {n:tuple(AVAILABLE[root+s+'_'+w].copy() for w in ('hi','lo')) for n,s in suffix.items()}


def gauge_rational_control(name,actual,targets):
 rational_control(name,actual,targets)
 def flat(x):return [v for y in x for v in flat(y)] if isinstance(x,list) else [x]
 rows=[v for target in targets for v in flat(target)];assert len(rows)==actual[0].size
 mask=np.asarray([v[2]==0 for v in rows]).reshape(actual[0].shape)
 keep(name+'_exact_zero_envelope_mask',mask.copy());assert all(np.all(w[mask]==0) for w in actual),'A zero rational envelope requires both actual words zero'


def measure_gauge_components(column,normal_cache,input_ref):
 indices=np.asarray([44*i+j for i,j in POINT_CELLS],dtype=np.int64);small=select_gauge_points(column,indices);normal=select_gauge_points(normal_cache,indices);results=[]
 f=(1.,0.,0.,0.);b=((0.,0.,0.),(1.,0.,0.),(0.,1.,0.),(0.,0.,1.))
 for case in range(2):
  label='component%d_NEW_gauge'%case;direction=gauge_component_direction(4,case)
  CONTEXT.update(stage='NEW_component_input',component=case,column=0)
  capture_families(label+'_copied_selected_column_',small);capture_families(label+'_NEW_direction_',direction);keep(label+'_original_flat_point_indices',indices.copy())
  ref=seal_completed('COMPONENT_INPUT',dict(kind='NEW_actual_section0_fourpoint_gauge_direction',component=case,source_input=thin(input_ref),cells=POINT_CELLS,firstjet_coordinate_order=['t','R','Z','phi'],gauge_values_zero=case==1,physical_adoption=False));clear_completed()
  result=candidate_gauge_registered_current_column(small,direction,keep,label);capture_families(label+'_completed_',result);locks=gauge_locked_chart(label)
  for n,x in locks.items():fy_keep(label+'_NEW_value_lock_'+n,x,keep)
  chart=[gauge_chart_firstjet_fraction_reference(small,direction,result,locks,i) for i in range(4)]
  actual={**result['mechanical']['d'],'dens':result['mechanical']['dc']['dens'],'K':result['mechanical']['delta_momenta']['K'],'metric_EH_density':result['mechanical']['delta_momenta']['metric_EH_density']}
  for n in CHART_FAMILIES:
   pair=actual[n];pair=tuple(np.moveaxis(w,1,0).copy() for w in pair) if n in ('z','dz') else pair
   gauge_rational_control(label+'_chart_'+n,pair,[q[n] for q in chart])
  phase_direction={n:result['mechanical']['d'][n] for n in ('g','hi','U','uc','P')};phase_direction['phi']=P.a_dd(np.zeros((4,4)))
  phase_direction.update({n:result['mechanical']['dc'][n] for n in ('N','mu','h','beta','ih','u')})
  phase=[chi_cached_contact_reference(small['phase'],phase_direction,normal,f,b,i,False) for i in range(4)]
  for n in EOS_FAMILIES:gauge_rational_control(label+'_EOS_'+n,result['phase']['delta'][n],[q['eos'][n] for q in phase])
  for n in ('P','PX','PXX'):
   for key in ('actual','expected','gap'):
    pair=result['phase']['chain_gaps'][n] if key=='gap' else tuple(AVAILABLE[label+'_NEW_literal_phase_NEW_'+n+'_analytic_chain_'+key+'_'+w].copy() for w in ('hi','lo'))
    gauge_rational_control(label+'_'+n+'_chain_'+key,pair,[q['chain'][n][key] for q in phase])
  if case==1:
   for name,values in (('phase',result['phase']['delta']),('chart_values',{n:actual[n] for n in ('g','hi','U','z','dens')})):
    for n,x in values.items():assert all(np.all(w==0) for w in x),(name,n)
  names=gauge_component_control_names(case);assert [q['name'] for q in CHECKS[-len(names):]]==names
  ref=seal_completed('COMPONENT_CONTACT',dict(kind='NEW_gauge_chart_firstjet_and_cached_EOS_direction_reference',component=case,input=thin(input_ref),direction=thin(ref),control_names=names,controls=CHECKS[-len(names):],exact_rational_targets=REFERENCE_METADATA[-len(names):],no_primal_EOS_or_old_direction_replay=True,stage_analytic_chain_gap_not_assumed_zero=True,physical_adoption=False));results.append(thin(ref));clear_completed()
 return results


def gauge_current_packet(refs):
 global REFS
 REFS=refs;basis=read_closed(refs['basis'],('R','dv','hats','cell_i','cell_j'))
 for n,a in basis.items():keep('copied_original_basis_'+n,a.copy())
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 assert np.array_equal(basis['cell_i'],np.repeat(np.arange(86),44)) and np.array_equal(basis['cell_j'],np.tile(np.arange(44),86))
 names=[n for case in range(2) for n in gauge_component_control_names(case)]
 header=seal_completed('INPUT',dict(kind='SAME225_updated13764_gauge_current_component_sources',original_input=thin(refs['input']),basis=thin(refs['basis']),normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],mechanical_terminal=refs['mechanical_cache']['closed_provenance'],expected_control_names=names,gauge_row_order=['N','beta_R','beta_Z','beta_phi'],gauge_jet_order=['value','R','Z','t'],current_targets_and_epsilon_unchanged=True,physical_adoption=False));clear_completed();columns=[];cache_refs=[];component_refs=[]
 for iq,source in enumerate(refs['columns']):
  CONTEXT.update(stage='hydrate_closed_gauge_column',column=iq);column,cache,_=hydrate_mechanical_rate_column(refs,source,iq)
  phase,_,_,normal,index=hydrate_chi_column(source,iq)
  column.update(phase=phase,constants=cache['constants'],same_candidate_provenance=column['provenance'],gauge_target_derivative_zero=True,physical_adoption=False)
  assert np.array_equal(column['candidate']['s']['R'],basis['R'][iq]);columns.append(column)
  q=seal_completed('CACHE_COLUMN',dict(kind='copied_SAME225_updated13764_stages_and_original_Gamma_curvature_provenance',column=iq,input=thin(header),state=thin(source['state']),updated_phase=thin(source['new']),temporal_cache=thin(refs['mechanical_cache']['caches'][iq]),joined_normal_rows=[thin(v) for v in source['joined_rows']],gauge_current_targets_unchanged=True,EOS_primal_or_action_replayed=False,physical_adoption=False));cache_refs.append(thin(q));clear_completed()
  if iq==0:component_refs=measure_gauge_components(column,normal,header)
 tests=[];colrefs=[]
 def test_complete(iq,row,jet,result):
  CONTEXT.update(stage='completed_NEW_gauge_test',column=iq,row=row,jet=jet);capture_families('completed_NEW_gauge_',result)
  if jet>0:
   for n,x in result['phase']['delta'].items():assert all(np.all(w==0) for w in x),n
  q=seal_completed('GAUGE_TEST',dict(kind='NEW_gauge_registered_mechanical_and_UPDATED_literal_phase_point_contact',column=iq,row=row,jet=jet,input=thin(header),cache=cache_refs[iq],coordinate_order=['value','R','Z','t'],genuine99_and_physical6=True,all_primary_time_jets_retained=True,phase_firstjet_port_bothwords_zero=jet>0,target_derivative_zero=True,C_equals_minus_Rv_or_Schwarz_assumed=False,physical_adoption=False));tests.append(thin(q));clear_completed();return thin(q)
 def column_complete(iq,result):
  CONTEXT.update(stage='completed_NEW_gauge_column',column=iq);capture_families('completed_NEW_gauge_column_',result)
  q=seal_completed('COLUMN',dict(kind='NEW_all16_gauge_current_coefficient_inventory',column=iq,input=thin(header),cache=cache_refs[iq],test_refs=tests[-16:],native_shape=[3784,99,4,4],metric_shape=[3784,6,4,4],phase_shape=[3784,4,4],native_E_metric_F_scalar_left_scatter_and_normal_test_transpose_external=True,physical_adoption=False));colrefs.append(thin(q));clear_completed();return thin(q)
 result=candidate_whole_gauge_registered_current_coefficients(columns,basis,keep,'NEW_actual_gauge_current',test_complete,column_complete)
 assert len(result['completed_column_refs'])==4 and len(tests)==64 and len(colrefs)==4
 expected=['INPUT','CACHE_COLUMN','COMPONENT_INPUT','COMPONENT_CONTACT','COMPONENT_INPUT','COMPONENT_CONTACT']+['CACHE_COLUMN']*3+(['GAUGE_TEST']*16+['COLUMN'])*4+['PREPARATION']
 assert [q['metadata']['role'] for q in RECORDS]==expected[:-1] and [q['name'] for q in CHECKS]==names and len(names)==len(set(names)) and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 capture_families('completed_NEW_gauge_forward_',{'columns':{str(i):q['coefficients'] for i,q in enumerate(result['columns'])}})
 preparation=seal_completed('PREPARATION',dict(kind='NEW_candidate_gauge_registered_current_forward_block',input=thin(header),cache_columns=cache_refs,component_refs=component_refs,columns=colrefs,tests=tests,controls=CHECKS,all64_ports_earned=True,source_scatter_adjoint_and_stationarity_feedback_external=True,original_current_targets_unchanged=True,global_inverse_rank_or_physical_adoption=False,physical_adoption=False));clear_completed()
 assert [q['metadata']['role'] for q in RECORDS]==expected
 return dict(status='CANDIDATE_GAUGE_REGISTERED_CURRENT_FORWARD_CONTACTS_MEASURED',input=thin(header),cache_columns=cache_refs,component_refs=component_refs,columns=colrefs,tests=tests,preparation=thin(preparation),expected_control_names=names,controls=len(names),roles=len(expected),registered_mechanical_literal_phase_current_only=True,C_equals_minus_Rv_or_Schwarz_assumed=False,original_targets_epsilon_and_physical_flags_unchanged=True,source_left_scatter_right_normal_test_adjoint_external=True,stationarity_feedback_and_global_inverse_unearned=True,physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root guarded release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(*MECHANICAL_SUPPORT_SOURCE);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for ref in COMPONENT_PROTOCOLS:bind(*ref)
  for name,h in PINS.items():bind(name,h)
  initialize_gauge_helpers();refs=mechanical_rate_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,expected_control_names=[n for case in range(2) for n in gauge_component_control_names(case)],qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=gauge_current_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(CHECKS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_NEW_gauge_current',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
