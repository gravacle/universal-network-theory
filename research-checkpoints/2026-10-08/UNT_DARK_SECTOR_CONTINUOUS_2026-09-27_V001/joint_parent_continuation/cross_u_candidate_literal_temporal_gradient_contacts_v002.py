"""HELD NEW literal current temporal-gradient and stationarity bridge contacts.
Source-only authoring; root alone binds future anchor closure and executes.
No old current, feature, geometry, canonical action or fixture is replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_LITERAL_TEMPORAL_GRADIENT_CONTACTS_V002'
DRIVER_PROTOCOL='CANDIDATE_LITERAL_TEMPORAL_GRADIENT_CONTACTS_V001.md'
PROTOCOL_SHA='c5e1904b9d310f6ae8ae03023236d61ce93d81b9b0dab23b0827336d78c738cc'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py', '489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json', '49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e', 'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json', 'c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64', 'CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json', '2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9', 'ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
RECOVERY_FILE='cross_u_finite0_state_normal_recovery_v005.py'
RECOVERY_SHA='8f9b528e1da5114b148585799e902cdaaa14a6ac2af60e7deff9a85375792be2'
RECOVERY_RESULT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RESULT.json', 'ea3c323511febbd278217e19ce8364d0e09186edc6d1d5c61bf87fb5fa211954', 'FINITE0_NEW_ACTION_CURRENT_NORMAL_CMC_RESIDUAL_MEASURED')
RECOVERY_RECEIPT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RECEIPT.json', '9e26a9c77d2ec7f023344c8399645cb94dc3252f2ab0dd744e14469050a30955', 'CLOSED')
RECOVERY_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_V001.json', '47ea566a93b34846c5861f7b184f80a73ac1ddd74f52bc891a7160b0a57fdab1', 'ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED')
RECOVERY_SUCCESS_PROOF_STATUS='ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED'
PRIOR_PHASE_PRODUCER_SOURCE=('cross_u_phase_fixed_weak_charge_preparation_v003.py', 'ed18caa749cbbfef40956ee4764390d688aaf6a1567912317d6cc81c9851d079')
PRIOR_PHASE_PRODUCER_RESULT=('CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003_RESULT.json', 'fefe9a83c871577653a3965d0c61ff869f6786ff0b1c9a943d9abf4fd6ee79d7', 'LITERAL_PHASE_HESSIAN_POSITIVE_AND_FIXED_WEAK_CHARGE_MASS_PREPARED')
PRIOR_PHASE_PRODUCER_RECEIPT=('CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003_RECEIPT.json', '9d2fb6e0a649976167144b0d428bc730800844d78670587ad8891b11ddfcca90', 'CLOSED')
PRIOR_PHASE_ANCESTRY_PROOF=('ROOT_CLOSED_PRIOR_PHASE_LOADS_ANCESTRY_SEALS_V001.json', 'cf5575e71d2c818d84da7fbb5e676bf60e9051ebed2917aab8e9a192e3884ed3', 'ROOT_CLOSED_PRIOR_PHASE_LOADS_ANCESTRY_SEALS_VERIFIED')
COMPONENT_PROOF=('CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json', '5f632a9927d41e36a40c7f2e0988997905ff99ac8dfef985307ce7723f63d4f9', 'CANDIDATE_LITERAL_PHASE_MASS_MANUFACTURED_COMPONENT_CONTROLS_PASS')
ADMISSION_PARENT='cross_u_completed_candidate_literal_phase_mass_preparation_v004.py'
ADMISSION_PARENT_SHA='18891223822037932792c117146c685b3e7a1c1632d45a122f9e05def8992e8f'
ADMISSION_PROTOCOL=('CROSS_U_COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARATION_V004.md', 'b6930f9dca96687c7fb230e88087dba983dae9147df0aa30bb053107d72d2d1b')
SNAMES=('g', 'hi', 'U', 'z', 'uc', 'P', 'Z', 'r', 'z2', 'f', 'phi', 'omega', 'xi', 'w', 'R', 'Z_coordinate')
CNAMES=('h', 'ih', 'N', 'beta', 'u', 'up', 'gamma', 'dens', 'sqrt_h', 'JU', 'JzU', 'Jzz', 'Uh', 'zh', 'embed')
MATERIAL=('B', 'GC', 'ALPHA', 'ELL', 'C')
ANCHOR_SOURCE=('cross_u_candidate_reference_york_anchor_canonical_packet_v004.py', '184d850aee263a6d4957c7df632c7bd928d6804d9c43978489c5b6abda02b5d7')
ANCHOR_RESULT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RESULT.json', '94220e4f2c37e16239a261143ef498b9d935ed234a91d9c95b3119fce75d3352', 'REFERENCE_YORK_ANCHOR_TARGET_AND_CANONICAL_EPSILON_MEASURED')
ANCHOR_RECEIPT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RECEIPT.json', '2aa42aef8e9a8a45f7f902f223092640f461703dac71b8bf103918f4425abeee', 'CLOSED')
ANCHOR_PROOF=('ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_V001.json', '1b43fc07b4c51c64b1798575f1f1aec48005761bf744f6d981d37b52071d2e4a', 'ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_VERIFIED')
FEATURE_NAMES=('F','Fup','V','V_raised','D','D_raised','Pi','PiU')
MOMENT_NAMES=('K','Ktrace','native_density','metric_native_density','metric_EH_tensor','metric_EH_density','metric_total_density')
DECLARED_CELLS=((0,0),(42,21),(85,21),(42,43))
np=P=ADMISSION=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};DESCRIPTIONS={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_finite0_completed_state_restore_v002.py': 'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59', 'cross_u_completed_candidate_mechanical_cache_preparation_v004.py': '489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522', 'cross_u_completed_candidate_literal_phase_mass_preparation_v004.py': '18891223822037932792c117146c685b3e7a1c1632d45a122f9e05def8992e8f', 'author_fragment_candidate_literal_temporal_gradient_bridge_v001.py': '880d9689965e7f66a159178cbec13b0a1e03e3929c7796e90c4370a9919f4d50', 'author_fragment_candidate_literal_gradient_positive_v001.py': 'ccd80e8fbc75927d95bc5d985362a73af819340c004b8d19ef143dad0f385e94', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6'}

def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(IO_PARENT,names),IO_PARENT,'exec'),globals());initialize_io()
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,None),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']

def closed_packet(source,result,receipt,proof):
 assert all(x is not None for q in (source,result,receipt,proof) for x in q),'Naturally CLOSED packet/proof required'
 for q in (source,result,receipt,proof):bind(q[0],q[1])
 r=json.loads(P.path(result[0]).read_text());rc=json.loads(P.path(receipt[0]).read_text());pr=json.loads(P.path(proof[0]).read_text());stem=result[0].removesuffix('_RESULT.json')
 assert r['status']==result[2] and rc['status']==receipt[2] and rc['result_sha256']==result[1] and rc['error_sha256'] is None
 assert r['owner']==rc['owner']==pr['owner'] and r['owner']['source_sha256']==source[1] and r['qualification']==rc['qualification'] and all(x is False for x in r['qualification'].values())
 assert pr['status']==proof[2] and pr['source_sha256']==source[1] and pr['result_sha256']==result[1] and pr['receipt_sha256']==receipt[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==0 and pr['all_input_seals_verified'] is True and pr['all_success_role_seals_verified'] is True
 assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 assert all(x['passed'] is True and x['tolerance']==2e-11 for x in r['controls'])
 return r,rc

def selected_record(ref,result,receipt):
 q=bind_record(ref);assert q in result['checkpoints'] and q['metadata']['owner']==result['owner'] and q['metadata']['failed'] is False
 for k,h in (('file','sha256'),('commit_file','commit_sha256')):assert receipt['output_sha256'][q[k]]==q[h]
 return q

def seal(role,metadata):
 q=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)));clear_current();DESCRIPTIONS.clear();return q

def load_completed_admission():
 global ADMISSION
 bind(ADMISSION_PARENT,ADMISSION_PARENT_SHA);bind(*ADMISSION_PROTOCOL)
 names={'bind_record','completed_candidate_admission'};tree=ast.parse((BASE/ADMISSION_PARENT).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==2
 selected=('RECOVERY_FILE','RECOVERY_SHA','RECOVERY_RESULT','RECOVERY_RECEIPT','RECOVERY_CLOSURE_PROOF','RECOVERY_SUCCESS_PROOF_STATUS','COMPONENT_PROOF','IO_PARENT_SHA','FLAGS','PRIOR_PHASE_PRODUCER_SOURCE','PRIOR_PHASE_PRODUCER_RESULT','PRIOR_PHASE_PRODUCER_RECEIPT','PRIOR_PHASE_ANCESTRY_PROOF')
 scope={n:globals()[n] for n in selected};scope.update(P=P,bind=bind,thin=thin,json=json)
 exec(compile(ast.Module(body=defs,type_ignores=[]),ADMISSION_PARENT,'exec'),scope);ADMISSION=types.SimpleNamespace(**{n:scope[n] for n in names})

def initialize_helpers():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','pack_fields','unpack_fields','pack_dd'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
  for n in names:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|set(MATERIAL)})
 for n in MATERIAL:setattr(P,n,SCOPE[n])
 choices=((list(PINS)[2],None),(list(PINS)[3],{'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}),(list(PINS)[4],None),(list(PINS)[6],{'finite0_saved_pair','finite0_validate_saved_transaction_ownership'}),(list(PINS)[9],None),(list(PINS)[10],None),(list(PINS)[11],{'ft_keep','candidate_temporal_jets'}),(list(PINS)[12],{'mp_out','mp_add','mp_mul','mp_div','mp_sum','mp_mm','mp_mv'}),(list(PINS)[13],{'ct_pair','candidate_original_evaluation_transpose'}),(list(PINS)[14],{'candidate_point_provider_admission','candidate_point_cache_names'}),(list(PINS)[15],{'bind_record'}))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 for file,prefix in ((list(PINS)[6],'FINITE0_RESTORE_'),(list(PINS)[14],'POINT_')):
  for n in ast.parse((BASE/file).read_text()).body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith(prefix):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_literal_gradient_exact_product');globals()['a_prod']=P.a_prod
 load_completed_admission()

def gradient_admission():
 original=ADMISSION.completed_candidate_admission();mechanical=candidate_point_provider_admission(bind)
 assert mechanical['preparation']['metadata']['closed_candidate_proof']==original['closed_proof']
 for iq,q in enumerate(mechanical['caches']):
  md=q['metadata'];assert md['state']==thin(original['states'][iq]) and md['candidate_provenance']['state']==thin(original['states'][iq]) and md['candidate_provenance']['input']==thin(original['input'])
 anchor,arc=closed_packet(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF);case=anchor['case']
 assert case['prepared_metric_target_is_exact_owned_reference'] is True and case['free_prior_or_target_refitted'] is False and case['new_varying_target_JVP'] is False and case['physical_adoption'] is False
 assert case['original_input']==thin(original['input']) and case['original_basis']==thin(original['basis']) and case['old_loads']==thin(original['loads'])
 canonical=selected_record(case['canonical'],anchor,arc);md=canonical['metadata'];assert md['kind']=='NEW_exact_reference_prepared_target_and_current_canonical_epsilon' and md['mechanical_current_unchanged_under_phase_update'] is True and md['physical_adoption'] is False
 return dict(original=original,mechanical=mechanical,canonical=canonical,anchor_terminal=(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF))

def hydrate_transaction(refs,iq):
 state=refs['original']['states'][iq];meta=refs['original']['input']['metadata'];md=state['metadata'];ownership=finite0_validate_saved_transaction_ownership(meta,md,refs['original']['closed_proof'])
 assert md['kind']=='NEW_candidate_completed_configuration_features_momenta_EOS_and_mean' and md['failed'] is False and md['physical_adoption'] is False
 for key,family in (('pilot_reference','pilots'),('owned_spatial_reference','forces')):assert thin(md[key])==thin(meta['refs'][family][iq])
 assert thin(md['current_time_words'])==thin(meta['refs']['current_jets'])
 names=tuple('completed_candidate_s_'+n for n in SNAMES)+tuple('completed_candidate_c_'+n for n in CNAMES)+tuple('completed_candidate_features_'+n+'_'+w for n in FEATURE_NAMES for w in ('hi','lo'))+tuple('completed_candidate_momenta_'+n+'_'+w for n in MOMENT_NAMES for w in ('hi','lo'))
 diagnostics=tuple(n for n in md['schema'] if n.startswith(('candidate_raw_direct_minus_quotient_','candidate_raw_model_minus_new_raw_chart_first_','candidate_raw_geometry_','candidate_raw_new_candidate_minus_owned_reference_')) or n in tuple('candidate_raw_'+x+'_'+w for x in ('KGamma_minus_KADM','Ktrace_Gamma_minus_ADM','new_first_compatibility_minus_E0') for w in ('hi','lo')))
 assert len(names)==len(set(names)) and all(n in md['schema'] for n in names);data=read(state,names+diagnostics);RAW.clear()
 for n,a in data.items():keep('copied_STATE%d_'%iq+n,a)
 pair=lambda prefix,n:finite0_saved_pair(data,prefix+n)
 candidate=dict(s={n:data['completed_candidate_s_'+n].copy() for n in SNAMES},c={n:data['completed_candidate_c_'+n].copy() for n in CNAMES},features=dict(paired={n:pair('completed_candidate_features_',n) for n in FEATURE_NAMES}),momenta={n:pair('completed_candidate_momenta_',n) for n in MOMENT_NAMES},candidate_provenance=refs['mechanical']['caches'][iq]['metadata']['candidate_provenance'])
 cache_ref=refs['mechanical']['caches'][iq];cd=read(cache_ref,candidate_point_cache_names(cache_ref['metadata']));RAW.clear();prefix=POINT_CACHE_PREFIX
 for n,a in cd.items():keep('copied_cache%d_'%iq+n,a)
 cp=lambda n:tuple(cd[prefix+n+'_'+w].copy() for w in ('hi','lo'));ep=prefix+'copied_positive_coefficient_'
 cache=dict(s={n:cd[prefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:cd[prefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=cp('anchored_raw_up_dot_zi'),NA=cp('paired_N_times_anchored_A'),gamma_squared=cp('gamma_squared_denominator'),fixed_E0=cp('fixed_lowered_E0'),formal_Iu=cp('formal_I_times_u'),envelopes={n[len(ep):]:a.copy() for n,a in cd.items() if n.startswith(ep)},constants=cache_ref['metadata']['constants'],candidate_provenance=candidate['candidate_provenance'],configuration_held=True)
 for family in ('s','c'):
  for n,a in cache[family].items():assert np.array_equal(a,candidate[family][n]),(family,n)
 ref=thin(seal('TRANSACTION_COPY',dict(kind='selected_completed_same_raw_current_and147_cache_word_copies',column=iq,state=thin(state),temporal_cache=thin(cache_ref),ownership=ownership,old_primal_or_action_replayed=False,physical_adoption=False)))
 return candidate,cache,ref

def exact(x):return Fraction.from_float(float(x))

def rational(x):return dict(numerator_hex=hex(x.numerator),denominator_hex=hex(x.denominator))

def pair_value(x,index):return exact(x[0][index])+exact(x[1][index])

def rat_matrix(x,p):return [[pair_value(x,(p,i,j)) for j in range(x[0].shape[-1])] for i in range(x[0].shape[-2])]

def rat_mv(A,x):return [sum((a*b for a,b in zip(row,x)),Fraction(0)) for row in A]

def rat_mm(A,B):return [[sum((a*b for a,b in zip(row,col)),Fraction(0)) for col in zip(*B)] for row in A]

def rat_tr(A):return list(map(list,zip(*A)))

def rat_contract(A,B):return sum((a*b for row,col in zip(A,B) for a,b in zip(row,col)),Fraction(0))

def scalar_rows_contact(rows,label):
 ratios=[];table=[];expected=[]
 for actual,target,envelope in rows:
  bound=abs(target)+envelope;gap=actual-target;assert bound or actual==target==0,'Exact zero polynomial envelope requires exact zero identity'
  r=abs(gap)/bound if bound else Fraction(0);h=float(target);l=float(target-exact(h));z=float(r);z=np.nextafter(z,np.inf) if exact(z)<r else z
  table.append(dict(actual=rational(actual),target=rational(target),conversion_remainder=rational(target-exact(h)-exact(l)),uncancelled_envelope=rational(envelope),difference=rational(gap),exact_ratio=rational(r)));expected.append((h,l));ratios.append(z)
  DESCRIPTIONS[label]=table.copy();keep(label+'_progressive_expected_words',np.asarray(expected).copy());keep(label+'_progressive_upward_ratios',np.asarray(ratios).copy())
  assert r<=Fraction.from_float(2e-11),'Original component implementation tolerance unchanged'
 P.check(label,np.asarray(ratios),np.zeros(len(ratios)),np.ones(len(ratios)))

def declared_direction(basis):
 n=np.zeros((33,3,87,45));m=np.zeros((6,87,45))
 for mode,component,i,j,v in ((0,0,1,0,.5),(3,2,1,0,-.25),(0,1,43,22,.125),(7,0,43,22,-.5),(23,2,86,22,.0625),(31,0,43,44,-.125)):n[mode,component,i,j]=v
 for slot in range(6):m[slot,43,22]=(-1.)**slot*2.**(-3-slot)
 m[0,1,0]=.25;m[2,86,22]=-.125;m[5,43,44]=.0625
 n[~np.broadcast_to(P.native_mask(),n.shape)]=0;m[~P.metric_mask()]=0;native=(n,2.**-60*n);metric=(m,2.**-60*m)
 lg_keep('NEW_direction_packed',P.pack_dd(native,metric),keep);pn=lg_keep('NEW_direction_native_original_values',P.dd_native_node_value(native,basis,keep,jet=0),keep);pm=lg_keep('NEW_direction_metric_original_values',P.dd_metric_node_value(metric,basis,keep,jet=0),keep)
 ref=thin(seal('DIRECTION',dict(kind='NEW_paired_original_E_F_direction_with_sheet_axis_and_free_boundary_coordinates',declared_cells=DECLARED_CELLS,low_word_scale=2.**-60,old_direction_or_lift_replayed=False,physical_adoption=False)))
 return native,metric,pn,pm,ref

def new_covariant_direction(cache,jets,label):
 nu,nz=jets['du'],jets['dz'];s=cache['s']
 for l in range(4):
  ga=P.a_transpose(P.a_slice(jets['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1));nu=P.a_add(nu,P.a_mul64(s['U'][:,l,None,None],ga));nz=P.a_sub(nz,P.a_mul64(s['z'][:,:,l,None,None],P.a_slice(jets['Ga'],(slice(None),l,slice(None),slice(None)))))
  lg_keep(label+'_nu_partial',nu,keep);lg_keep(label+'_nz_partial',nz,keep)
 return lg_keep(label+'_nu',nu,keep),lg_keep(label+'_nz',nz,keep)

def independent_component_contacts(candidate,cache,gradient,components,jets,physical,nu,nz,label):
 s,c,F,M=candidate['s'],candidate['c'],candidate['features']['paired'],candidate['momenta'];rows={n:[] for n in ('Maxwell','modal_V','modal_D','acceleration','formal_native','formal_EH')}
 for i,j in DECLARED_CELLS:
  p=i*44+j;g,hi,I,Proj=([[exact(a) for a in row] for row in x[p]] for x in (s['g'],s['hi'],c['ih'],s['P']));U=list(map(exact,s['U'][p]));du=rat_matrix(nu,p);lower=rat_mm(du,g);dF=[[lower[a][b]-lower[b][a] for b in range(4)] for a in range(4)];dFu=rat_mm(rat_mm(hi,dF),hi)
  curF,curFu=rat_matrix(F['F'],p),rat_matrix(F['Fup'],p);terms=[-exact(P.ALPHA)/4*a*b for A,B in ((dF,curFu),(curF,dFu)) for ar,br in zip(A,B) for a,b in zip(ar,br)];target=sum(terms,Fraction(0));actual=rat_contract(rat_matrix(components['nu_Maxwell'],p),du);rows['Maxwell'].append((actual,target,sum(map(abs,terms),Fraction(0))))
  vterms=[];dterms=[];acc=[];av=ad=Fraction(0)
  for mode in range(32):
   dz=[[pair_value(nz,(mode,p,a,b)) for b in range(4)] for a in range(4)];dq=rat_mv(rat_tr(dz),U);dV=rat_mv(Proj,dq);dVu=rat_mv(hi,dV);dD=rat_mm(rat_mm(Proj,dz),rat_tr(Proj));dDu=rat_mm(rat_mm(hi,dD),hi);w=exact(s['w'][mode]);om=exact(float(s['omega'][mode]**2))
   for a in range(4):vterms.extend((w/(2*om)*dV[a]*pair_value(F['V_raised'],(mode,p,a)),w/(2*om)*pair_value(F['V'],(mode,p,a))*dVu[a]))
   for a in range(4):
    for b in range(4):dterms.extend((-w*exact(P.ELL**2)/2*dD[a][b]*pair_value(F['D_raised'],(mode,p,a,b)),-w*exact(P.ELL**2)/2*pair_value(F['D'],(mode,p,a,b))*dDu[a][b]));av+=pair_value(components['nz_V'],(mode,p,a,b))*dz[a][b];ad+=pair_value(components['nz_D'],(mode,p,a,b))*dz[a][b]
   for a in range(4):acc.append(w*exact(s['z'][mode,p,a])*sum((U[b]*du[b][a] for b in range(4)),Fraction(0)))
  rows['modal_V'].append((av,sum(vterms,Fraction(0)),sum(map(abs,vterms),Fraction(0))));rows['modal_D'].append((ad,sum(dterms,Fraction(0)),sum(map(abs,dterms),Fraction(0))));rows['acceleration'].append((rat_contract(rat_matrix(components['nu_acceleration'],p),du),sum(acc,Fraction(0)),sum(map(abs,acc),Fraction(0))))
  primitive=[pair_value(gradient['primitive_adjoints']['nu'],(p,0,a))*pair_value(jets['Ut'],(p,a)) for a in range(4)]+[pair_value(gradient['primitive_adjoints']['nz'],(mode,p,0,a))*pair_value(jets['Zt'],(mode,p,a)) for mode in range(32) for a in range(4)]+[pair_value(gradient['primitive_adjoints']['Gamma'],(p,l,a,b))*pair_value(jets['Ga'],(p,l,a,b)) for l in range(4) for a in range(4) for b in range(4)]
  rhs=[pair_value(gradient['literal']['native'],(p,a))*pair_value(physical['native'],(p,a)) for a in range(99)]+[pair_value(gradient['literal']['metric_native'],(p,a))*pair_value(physical['metric'],(p,a)) for a in range(6)];dens=exact(c['dens'][p]);left=[dens*t for t in primitive];rows['formal_native'].append((sum(rhs,Fraction(0)),sum(left,Fraction(0)),sum(map(abs,left+rhs),Fraction(0))))
  K=rat_matrix(M['K'],p);dK=[[exact(c['N'][p])*pair_value(jets['Ga'],(p,0,a+1,b+1)) for b in range(3)] for a in range(3)];Kup=rat_mm(rat_mm(I,K),I);dKup=rat_mm(rat_mm(I,dK),I);tau=pair_value(M['Ktrace'],(p,));dktrace=rat_contract(I,dK)
  ehterms=[dens/(2*exact(P.C))*a*b for A,B in ((dK,Kup),(K,dKup)) for ar,br in zip(A,B) for a,b in zip(ar,br)]+[-dens/exact(P.C)*tau*dktrace];er=[pair_value(gradient['literal']['metric_EH'],(p,a))*pair_value(physical['metric'],(p,a)) for a in range(6)];rows['formal_EH'].append((sum(er,Fraction(0)),sum(ehterms,Fraction(0)),sum(map(abs,ehterms+er),Fraction(0))))
 for name,values in rows.items():scalar_rows_contact(values,label+'_'+name)
 return dict(points=[i*44+j for i,j in DECLARED_CELLS],check_names=[label+'_'+n for n in rows],whole_grid_stationarity_or_uniform_gradient_qualified=False)

def literal_est(ar,br,basis,label):
 weight=keep(label+'_original_weight64',(basis['dv']/basis['R']).reshape(15136));n=P.a_mul64(weight[:,None],ar);m=P.a_mul64(weight[:,None],br);lg_keep(label+'_weighted_native',n,keep);lg_keep(label+'_weighted_metric',m,keep)
 modes=tuple(w.reshape(15136,33,3).transpose(1,0,2) for w in n);return candidate_original_evaluation_transpose(modes,m,basis,keep,label+'_original_Estar')

def literal_est_positive(native,metric,basis,label):
 n=native.reshape(4,86,44,33,3).transpose(3,0,1,2,4);m=metric.reshape(4,86,44,6);no=np.zeros((33,3,87,45));mo=np.zeros((6,87,45))
 for iq in range(4):
  R=basis['R'][iq].reshape(86,44);weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44);F=P.dd_metric_F(R)
  nv=mp_mul(weight[...,None],n[:,iq],keep,label);mv=mp_mul(weight[...,None],m[iq],keep,label)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=basis['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   term=mp_mul(abs(factor),nv,keep,label).transpose(0,3,1,2);key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj));no[key]=mp_add(no[key],term,keep,label)
   Fhat=hat[...,None,None]*F;term=mp_mv(abs(Fhat.swapaxes(-1,-2)),mv,keep,label).transpose(2,0,1);key=(slice(None),slice(di,86+di),slice(dj,44+dj));mo[key]=mp_add(mo[key],term,keep,label)
   keep(label+'_native_partial',no.copy());keep(label+'_metric_partial',mo.copy())
 for component in (1,2):no[:,component,1]=mp_add(no[:,component,1],no[:,component,0],keep,label)
 no[:,:,0]=0;no[:,1,:,0]=0;mo[:,1]=mp_add(mo[:,1],mo[:,0],keep,label);mo[:,0]=0;mo[3:5,:,0]=0
 out=P.pack_fields(no,mo);keep(label+'_completed_packed',out.copy());return out

def independent_weighted_evaluation_contact(literal,weak,basis,test_native,test_metric,label):
 wn,wm,_=P.unpack_fields(weak[0],False);ln,lm,_=P.unpack_fields(weak[1],False);nodal=[Fraction(0),Fraction(0)];direct=[Fraction(0),Fraction(0)];bound=[Fraction(0),Fraction(0)];F=P.dd_metric_F(basis['R'])
 for family,pair,test in ((0,(wn,ln),test_native),(1,(wm,lm),test_metric)):
  for index in zip(*np.nonzero((test[0]!=0)|(test[1]!=0))):term=pair_value(pair,index)*pair_value(test,index);nodal[family]+=term;bound[family]+=abs(term)
 for iq in range(4):
  for p in range(3784):
   i,j=int(basis['cell_i'][p]),int(basis['cell_j'][p]);r=basis['R'][iq,p];hat=[basis['hats'][iq,k,0].reshape(3784)[p] for k in range(4)];weight=exact(float(basis['dv'][iq,p]/r));tn=[[Fraction(0)]*3 for _ in range(33)];tm=[Fraction(0)]*6
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
    ni,nj=i+di,j+dj
    for a in range(3):
     independent_i=1 if ni==0 and a in (1,2) else ni
     if ni==0 and a==0 or nj==0 and a==1:continue
     factor=exact(float(r**2*hat[corner])) if a==2 else exact(hat[corner])
     for mode in range(33):tn[mode][a]+=factor*pair_value(test_native,(mode,a,independent_i,nj))
    for slot in range(6):
     if nj==0 and slot in (3,4):continue
     coefficient=pair_value(test_metric,(slot,1 if ni==0 else ni,nj))
     for a in range(6):tm[a]+=exact(float(hat[corner]*F[iq,p,a,slot]))*coefficient
   if not any(any(row) for row in tn) and not any(tm):continue
   for mode in range(33):
    for a in range(3):term=weight*tn[mode][a]*pair_value(literal['native'],(iq*3784+p,3*mode+a));direct[0]+=term;bound[0]+=abs(term)
   for a in range(6):term=weight*tm[a]*pair_value(literal['metric_total'],(iq*3784+p,a));direct[1]+=term;bound[1]+=abs(term)
 for family,name in enumerate(('native','metric')):scalar_rows_contact([(nodal[family],direct[family],bound[family])],label+'_'+name)

def literal_packet(refs):
 basis=read(refs['original']['basis'],('R','dv','hats','cell_i','cell_j','r','z'));RAW.clear();bcopy=read(refs['mechanical']['input'],tuple('registered_basis_'+n for n in basis));RAW.clear()
 for n,a in basis.items():keep('original_basis_'+n,a);keep('copied_mechanical_basis_'+n,bcopy['registered_basis_'+n]);assert np.array_equal(a,bcopy['registered_basis_'+n])
 inp=thin(seal('INPUT',dict(kind='authentic_same_completed_current_and147_basis_for_literal_gradient_bridge',original_input=thin(refs['original']['input']),original_loads=thin(refs['original']['loads']),basis=thin(refs['original']['basis']),mechanical=refs['mechanical']['closed_provenance'],anchor_terminal=refs['anchor_terminal'],physical_adoption=False)))
 md=refs['canonical']['metadata'];prefix=md['canonical_prefix'];names=tuple(prefix+n+'_'+w for n in ('_current_candidate_weak_native','_current_candidate_weak_metric','_target_minus_current_epsilon_native','_target_minus_current_epsilon_metric') for w in ('hi','lo'));canonical=read(refs['canonical'],names);RAW.clear();old=read(refs['original']['loads'],tuple('value_'+n+'_current_'+w for n in ('native','metric') for w in ('hi','lo')));RAW.clear()
 for n,a in canonical.items():keep('copied_anchor_'+n,a)
 for n in ('native','metric'):
  for w in ('hi','lo'):keep('copied_registered_S_'+n+'_'+w,old['value_'+n+'_current_'+w]);assert np.array_equal(old['value_'+n+'_current_'+w],canonical[prefix+'_current_candidate_weak_'+n+'_'+w])
 cre=thin(seal('CANONICAL_COPY',dict(kind='copied_authoritative_anchor_epsilon_and_registered_S_current',canonical=thin(refs['canonical']),original_loads=thin(refs['original']['loads']),old_current_scatter_replayed=False,physical_adoption=False)))
 native,metric,pn,pm,direction=declared_direction(basis);columns=[];gradients=[];bounds=[];transaction_refs=[]
 for iq in range(4):
  CONTEXT.update(stage='NEW_literal_current_gradient_column',column=iq);candidate,cache,transaction=hydrate_transaction(refs,iq);transaction_refs.append(transaction);label='NEW_literal_gradient_q%d'%iq
  gradient=candidate_literal_temporal_gradient_bridge(candidate,cache,keep,label);positive=candidate_literal_gradient_positive(candidate,cache,keep,label+'_unsigned')
  for n,pair in gradient['literal'].items():upper=mp_add(abs(pair[0]),abs(pair[1]),keep,label+'_represented_magnitude');keep(label+'_compared_'+n+'_outward_bound',positive[n]);assert np.all(upper<=positive[n]),'Literal gradient source reverse chain enclosure'
  components={n:tuple(AVAILABLE[label+'_literal_'+suffix+'_'+w].copy() for w in ('hi','lo')) for n,suffix in (('nu_Maxwell','nu_Maxwell_adjoint'),('nu_acceleration','nu_acceleration_adjoint'),('nz_V','nz_V_adjoint'),('nz_D','nz_D_adjoint'))}
  gradient_ref=thin(seal('GRADIENT_COLUMN',dict(kind='NEW_literal142_right_raw_left_registered_point_bridges_and_unsigned71',column=iq,transaction=transaction,literal_derivative_is_coefficient_polynomial_not_bitwise_EFT_AD=True,physical_adoption=False)));columns.append(gradient_ref);gradients.append(gradient['literal']);bounds.append(positive)
  sl=slice(iq*3784,(iq+1)*3784);physical=dict(native=tuple(a[:,sl].transpose(1,0,2).reshape(3784,99).copy() for a in pn),metric=tuple(a[sl].copy() for a in pm));jets=candidate_temporal_jets(cache,physical,keep,label+'_NEW_jets');nu,nz=new_covariant_direction(cache,jets,label+'_NEW_covariant_direction')
  jet_ref=thin(seal('JET_COLUMN',dict(kind='NEW147_temporal_jets_only_no_canonical_or_current_producer',column=iq,transaction=transaction,direction=direction,physical_adoption=False)))
  control=independent_component_contacts(candidate,cache,gradient,components,jets,physical,nu,nz,label+'_independent');seal('COMPONENT_CONTACT',dict(kind='exact_Fraction_literal_quadratic_and_formal_reverse_contacts',column=iq,gradient=gradient_ref,jets=jet_ref,control=control,controls=list(CHECKS[-6:]),original_tolerance=2e-11,physical_adoption=False))
  del candidate,cache,gradient,positive,components,jets,nu,nz
 literal={n:tuple(np.concatenate([q[n][w] for q in gradients]) for w in (0,1)) for n in ('native','metric_native','metric_EH','metric_total')}
 for n,pair in literal.items():lg_keep('NEW_literal_full_point_'+n,pair,keep)
 weak=literal_est(literal['native'],literal['metric_total'],basis,'NEW_literal_full_weak');bound=literal_est_positive(np.concatenate([q['native'] for q in bounds]),np.concatenate([q['metric_total'] for q in bounds]),basis,'NEW_literal_full_weak_unsigned');upper=mp_add(abs(weak[0]),abs(weak[1]),keep,'NEW_literal_full_weak_magnitude');assert np.all(upper<=bound),'Weighted literal gradient E transpose enclosure'
 weak_ref=thin(seal('EVALUATION_TRANSPOSE',dict(kind='NEW_literal_gradient_weighted_original_Estar_not_registered_S',columns=columns,basis=thin(refs['original']['basis']),weight64='original dv/R',metric_right_factor='original rounded Fhat',separate_outward_unsigned_chain=True,physical_adoption=False)))
 fields=[P.unpack_fields(w,False) for w in weak]
 for name,index in (('native',0),('metric',1)):
  L=tuple(q[index] for q in fields);registered=tuple(canonical[prefix+'_current_candidate_weak_'+name+'_'+w] for w in ('hi','lo'));epsilon=tuple(canonical[prefix+'_target_minus_current_epsilon_'+name+'_'+w] for w in ('hi','lo'));delta=lg_keep('NEW_weak_literal_minus_registered_'+name,P.a_sub(L,registered),keep);lg_keep('NEW_literal_stationarity_eL_'+name,P.a_sub(epsilon,delta),keep)
 bridge_ref=thin(seal('WEAK_BRIDGE',dict(kind='copied_epsilon_minus_NEW_literal_minus_registered_stationarity_bridge',canonical=cre,literal=weak_ref,epsilon_sign='target minus registered current',eL_sign='epsilon minus (literal minus registered)',normal_feedback_sign='minus C_transpose A_inverse_transpose eL with C=gauge registered-current derivative',stationarity_or_feedback_zero_assumed=False,physical_adoption=False)))
 independent_weighted_evaluation_contact(literal,weak,basis,native,metric,'NEW_weighted_Estar_polynomial');contact_ref=thin(seal('WEAK_CONTACT',dict(kind='NEW_literal_weighted_original_Estar_exact_Fraction_polynomial_contacts',direction=direction,literal=weak_ref,controls=list(CHECKS[-2:]),registered_S_current_copied_not_replayed=True,physical_adoption=False)))
 assert len(CHECKS)==26 and len(RECORDS)==22 and all(q['passed'] and q['tolerance']==2e-11 for q in CHECKS)
 final=thin(seal('PREPARATION',dict(kind='four_section_literal_temporal_gradient_and_canonical_stationarity_bridge_measured',input=inp,canonical=cre,columns=columns,weak=weak_ref,bridge=bridge_ref,contact=contact_ref,global_stationarity_or_adjoint_solve_qualified=False,physical_adoption=False)))
 assert len(RECORDS)==23
 return dict(status='CANDIDATE_LITERAL_TEMPORAL_GRADIENT_BRIDGE_AND_DIRECTION_CONTACTS_PASS',input=inp,transactions=transaction_refs,canonical_copy=cre,columns=columns,literal_weak=weak_ref,stationarity_bridge=bridge_ref,preparation=final,anchor_terminal=refs['anchor_terminal'],roles=23,new_controls=26,old_current_features_action_EOS_factor_or_solver_replayed=False,uniform_gradient_Schwarz_adjoint_inverse_or_stationarity_qualified=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root reviewed release required'
 assert all(x is not None for q in (ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF) for x in q),'Authentic naturally CLOSED anchor required before I/O'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  initialize_helpers();refs=gradient_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,anchor_terminal=refs['anchor_terminal'],new_literal_gradients=4,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=literal_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_literal_gradient_contact_with_completed_ancestry',context=dict(CONTEXT),exact_targets=DESCRIPTIONS),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
