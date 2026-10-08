"""HELD refreshed139 literal142 current gradient/eL, root execution only.
Consumes closed NEW point-TOTAL stages; no nodal baseline is invented and no
old current, geometry, EOS, point action, normal, factor or solver is replayed.
The same-field147 cache is reused only after raw/E0 byte-word identity checks.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_CONTACTS_V003'
DRIVER_PROTOCOL='REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_CONTACTS_V003.md'
PROTOCOL_SHA='7b891b3c2280422ef2d025cd409cc48deb5c07fca144f3b38c91f42e5fd4df0e'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
FINITE_SOURCE=(None,None)
FINITE_RESULT=(None,None,None)
FINITE_RECEIPT=(None,None,None)
FINITE_CLOSURE_PROOF=(None,None,None)
FINITE_STATUS='FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED'
CONTACT_PARENT='cross_u_candidate_literal_temporal_gradient_contacts_v002.py'
CONTACT_DEFS=('exact','rational','pair_value','rat_matrix','rat_mv','rat_mm','rat_tr','rat_contract','scalar_rows_contact','new_covariant_direction','independent_component_contacts','literal_est','literal_est_positive','independent_weighted_evaluation_contact')
DECLARED_CELLS=((1,0),(30,17),(85,21),(41,43))
SNAMES=('g', 'hi', 'U', 'z', 'uc', 'P', 'Z', 'r', 'z2', 'f', 'phi', 'omega', 'xi', 'w', 'R', 'Z_coordinate')
CNAMES=('h', 'ih', 'N', 'beta', 'u', 'up', 'gamma', 'dens', 'sqrt_h', 'JU', 'JzU', 'Jzz', 'Uh', 'zh', 'embed')
MATERIAL=('B', 'GC', 'ALPHA', 'ELL', 'C')
FEATURE_NAMES=('F', 'Fup', 'V', 'V_raised', 'D', 'D_raised', 'Pi', 'PiU')
MOMENT_NAMES=('K', 'Ktrace', 'native_density', 'metric_native_density', 'metric_EH_tensor', 'metric_EH_density', 'metric_total_density')
ANCHOR_SOURCE=('cross_u_candidate_reference_york_anchor_canonical_packet_v004.py', '184d850aee263a6d4957c7df632c7bd928d6804d9c43978489c5b6abda02b5d7')
ANCHOR_RESULT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RESULT.json', '94220e4f2c37e16239a261143ef498b9d935ed234a91d9c95b3119fce75d3352', 'REFERENCE_YORK_ANCHOR_TARGET_AND_CANONICAL_EPSILON_MEASURED')
ANCHOR_RECEIPT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RECEIPT.json', '2aa42aef8e9a8a45f7f902f223092640f461703dac71b8bf103918f4425abeee', 'CLOSED')
ANCHOR_PROOF=('ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_V001.json', '1b43fc07b4c51c64b1798575f1f1aec48005761bf744f6d981d37b52071d2e4a', 'ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_VERIFIED')
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py', '489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json', '49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e', 'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json', 'c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64', 'CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json', '2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9', 'ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_literal_temporal_gradient_bridge_v001.py': '880d9689965e7f66a159178cbec13b0a1e03e3929c7796e90c4370a9919f4d50', 'author_fragment_candidate_literal_gradient_positive_v001.py': 'ccd80e8fbc75927d95bc5d985362a73af819340c004b8d19ef143dad0f385e94', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'cross_u_candidate_literal_temporal_gradient_contacts_v002.py': '4e65631f487b3576e0eb69ee6aa8b7a66c82e00d6c5952a5f86b551df9fa2b21', 'author_fragment_fixed_geometry_total_rate_state_v002.py': 'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d'}
PINS['author_fragment_fixed_rate_inherited_success_admission_v001.py']='8da980eeb2c429b8612cd0c69be37490b3efa661978ecbedb859f03bce761687'
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};DESCRIPTIONS={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in items}==set(names),file
 exec(compile(ast.Module(body=items,type_ignores=[]),file,'exec'),scope)

def initialize():
 global np
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 definitions(IO_PARENT,{'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'},globals());initialize_io()
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','pack_fields','unpack_fields','pack_dd'}
 definitions(list(PINS)[0],base,SCOPE);definitions(list(PINS)[1],primitive,SCOPE)
 for n in base|primitive|set(MATERIAL):setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|set(MATERIAL)})
 choices=(('author_fragment_finite_york_geometry_target_v001.py',{'fy_keep','fy_sum','fy_mv','fy_mm','fy_contract','fy_div'}),('author_fragment_exact_exponent_two_product_v003.py',None),('author_fragment_candidate_literal_temporal_gradient_bridge_v001.py',None),('author_fragment_candidate_literal_gradient_positive_v001.py',None),('author_fragment_candidate_specialized_temporal_action_v001.py',{'ft_keep','candidate_temporal_jets'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',{'mp_out','mp_add','mp_mul','mp_div','mp_sum','mp_mm','mp_mv'}),('author_fragment_candidate_fullweak_transpose_stationarity_v003.py',{'ct_pair','candidate_original_evaluation_transpose'}),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_provider_admission','candidate_point_cache_names'}),(CONTACT_PARENT,set(CONTACT_DEFS)))
 for file,names in choices:definitions(file,names,globals())
 for n in ast.parse((BASE/'author_fragment_candidate_chunk_point_block_provider_v001.py').read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('POINT_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False)
 definitions('author_fragment_fixed_rate_inherited_success_admission_v001.py',{'fixed_rate_inherited_success_admission','fixed_rate_record_seals'},globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_refreshed_literal_exact_product');globals()['a_prod']=P.a_prod


def closed(source,result,receipt,proof):
 assert all(x is not None for q in (source,result,receipt,proof) for x in q),'Natural closure must be bound by root before any packet read'
 for q in (source,result,receipt,proof):bind(q[0],q[1])
 assert P.path(result[0]).stat().st_size<=128*1024*1024,'Larger result needs a separately reviewed bounded projection'
 r=json.loads(P.path(result[0]).read_text());rc=json.loads(P.path(receipt[0]).read_text());pr=json.loads(P.path(proof[0]).read_text())
 assert r['status']==result[2] and rc['status']==receipt[2] and pr['status']==proof[2]
 assert r['owner']==rc['owner']==pr['owner'] and r['owner']['source_sha256']==source[1]==pr['source_sha256']
 assert rc['result_sha256']==result[1]==pr['result_sha256'] and rc.get('error_sha256') is None and pr['receipt_sha256']==receipt[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==0 and pr['all_success_role_seals_verified'] is True
 assert r['qualification']==rc['qualification'] and r['qualification'] and all(v is False for v in r['qualification'].values())
 assert all(c['passed'] is True for c in r['controls'])
 return r,dict(rc,_fixed_rate_inherited_success=fixed_rate_inherited_success_admission(r,rc,bind))


def record(r,rc,ref):
 bind(ref['commit_file'],ref['commit_sha256']);q=json.loads(P.path(ref['commit_file']).read_text());assert q['file']==ref['file'] and q['sha256']==ref['sha256']
 q=dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256']);md=q['metadata']
 seals=fixed_rate_record_seals(r,rc,q)
 assert md['failed'] is False and md['qualification'] and all(v is False for v in md['qualification'].values())
 assert any(thin(x)==thin(q) for x in r['checkpoints']) and ('metadata' not in ref or ref['metadata']==md)
 for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert seals[n]==h
 return q


def stage(r,rc,kind,column=None):
 found=[q for q in r['checkpoints'] if q['metadata']['kind']==kind and (column is None or q['metadata'].get('column')==column)]
 assert len(found)==1,(kind,column);return record(r,rc,found[0])


def selected(q,names,label):
 assert len(names)==len(set(names)) and all(n in q['metadata']['schema'] for n in names),label
 bind(q['file'],q['sha256']);bind(q['commit_file'],q['commit_sha256']);data=read(q,names)
 for n,a in data.items():keep(label+'_'+n,a);s=q['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True
 return data


def saved_pair(data,prefix):return tuple(data[prefix+'_'+w].copy() for w in ('hi','lo'))


def seal(role,metadata):
 q=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)));clear_current();DESCRIPTIONS.clear();return thin(q)


def admission():
 finite,frc=closed(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF);anchor,arc=closed(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF);fc,ac=finite['case'],anchor['case']
 assert fc['status']==FINITE_STATUS and fc['spatial_geometry_unchanged'] is fc['current99_and_physical6_fresh'] is fc['all16normal_ports_per_section'] is True and fc['physical_adoption'] is False
 assert ac['prepared_metric_target_is_exact_owned_reference'] is True and ac['free_prior_or_target_refitted'] is False and ac['new_varying_target_JVP'] is False
 fi=stage(finite,frc,'INPUT');out=record(finite,frc,fc['readout']);ai=record(anchor,arc,ac['input']);can=record(anchor,arc,ac['canonical']);pr=fi['metadata']['provenance']
 assert ai['metadata']['rho_W_t_all_exact_zero'] is True and ai['metadata']['TT_or_exterior_prior_refitted'] is False and can['metadata']['input']==thin(ai)
 assert [thin(q) for q in fc['original_targets']]==[thin(q) for q in ac['original_canonical_target_refs']]==[thin(q) for q in pr['unchanged_original_targets']]
 assert pr['original_owned_TOTAL_time_words']==[q['metadata']['state'] for q in ac['columns']]
 assert pr['all_source_seals_authenticated'] is pr['original_fixed_references_verified'] is pr['correction_original_six_gates_admitted'] is True
 assert out['metadata']['kind_scope']=='fresh_point_first_TOTAL_rate_momenta_all16normal_CMC_at_unchanged_spatial_geometry'
 mechanical=candidate_point_provider_admission(bind);assert mechanical['original_basis']==ac['original_basis']
 cols=[]
 for iq in range(4):
  q={n:stage(finite,frc,n,iq) for n in ('BASELINE_COLUMN_INPUT','RATE_STATE_INPUT','RATE_STATE_FIRST_JETS','RATE_STATE_FEATURES','RATE_STATE_MOMENTA','RATE_STATE_COLUMN')}
  assert thin(q['RATE_STATE_COLUMN'])==fc['columns'][iq] and q['BASELINE_COLUMN_INPUT']['metadata']['state']==pr['original_owned_TOTAL_time_words'][iq]
  assert q['RATE_STATE_COLUMN']['metadata']['provenance']==pr['columns'][iq] and mechanical['caches'][iq]['metadata']['state']==pr['original_owned_TOTAL_time_words'][iq]
  cols.append(q)
 return dict(finite_input=fi,finite_readout=out,finite_provenance=pr,anchor_input=ai,anchor_canonical=can,mechanical=mechanical,columns=cols)


def hydrate(refs,iq):
 q=refs['columns'][iq];label='NEW139_column%d'%iq;CONTEXT.update(stage='select_NEW139_current_operands',column=iq)
 names=tuple('completed_BASELINE_COLUMN_INPUT_candidate_s_'+n for n in SNAMES)+tuple('completed_BASELINE_COLUMN_INPUT_candidate_c_'+n for n in CNAMES)
 data=selected(q['BASELINE_COLUMN_INPUT'],names,label+'_fixed_raw');s={n:data['completed_BASELINE_COLUMN_INPUT_candidate_s_'+n].copy() for n in SNAMES};c={n:data['completed_BASELINE_COLUMN_INPUT_candidate_c_'+n].copy() for n in CNAMES}
 fields=('h_first','u_jets','z_jets','N_jets','beta_jets','E0','updated_phase');d=selected(q['RATE_STATE_INPUT'],tuple('completed_RATE_STATE_INPUT_'+n+'_'+w for n in fields for w in ('hi','lo')),label+'_TOTAL_inputs');owned={n:saved_pair(d,'completed_RATE_STATE_INPUT_'+n) for n in fields}
 assert owned['h_first'][0].shape==(3784,4,3,3) and owned['u_jets'][0].shape==(3784,4,3) and owned['z_jets'][0].shape==(32,3784,4,3)
 first_names=tuple('completed_RATE_STATE_FIRST_JETS_jets_'+n+'_'+w for n in ('du','dz','dg','Ga') for w in ('hi','lo'))+tuple('completed_RATE_STATE_FIRST_JETS_owned_covectors_'+n+'_'+w for n in ('u_jets','z_jets') for w in ('hi','lo'))+tuple('completed_RATE_STATE_FIRST_JETS_fixed_E0_'+w for w in ('hi','lo'))
 first=selected(q['RATE_STATE_FIRST_JETS'],first_names,label+'_current_first');jets={n:saved_pair(first,'completed_RATE_STATE_FIRST_JETS_jets_'+n) for n in ('du','dz','dg','Ga')}
 for n in ('u_jets','z_jets'):
  assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(owned[n],saved_pair(first,'completed_RATE_STATE_FIRST_JETS_owned_covectors_'+n)))
 assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(owned['E0'],saved_pair(first,'completed_RATE_STATE_FIRST_JETS_fixed_E0')))
 fd=selected(q['RATE_STATE_FEATURES'],tuple('completed_RATE_STATE_FEATURES_features_paired_'+n+'_'+w for n in FEATURE_NAMES for w in ('hi','lo')),label+'_current_features');F={n:saved_pair(fd,'completed_RATE_STATE_FEATURES_features_paired_'+n) for n in FEATURE_NAMES}
 md=selected(q['RATE_STATE_MOMENTA'],tuple('completed_RATE_STATE_MOMENTA_momenta_'+n+'_'+w for n in MOMENT_NAMES for w in ('hi','lo')),label+'_current_momenta');M={n:saved_pair(md,'completed_RATE_STATE_MOMENTA_momenta_'+n) for n in MOMENT_NAMES}
 cache_ref=refs['mechanical']['caches'][iq];cd=selected(cache_ref,candidate_point_cache_names(cache_ref['metadata']),label+'_fixed147');prefix=POINT_CACHE_PREFIX;cp=lambda n:saved_pair(cd,prefix+n);ep=prefix+'copied_positive_coefficient_'
 provenance=dict(finite_terminal=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),fresh_stages={n:thin(r) for n,r in q.items()},unchanged_configuration_from=cache_ref['metadata']['candidate_provenance'],point_TOTAL_time_words=thin(q['RATE_STATE_INPUT']),nodal_TOTAL_equivalence_earned=False)
 candidate=dict(s=s,c=c,features=dict(paired=F),momenta=M,jets=jets,candidate_provenance=provenance)
 cache=dict(s={n:cd[prefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:cd[prefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=cp('anchored_raw_up_dot_zi'),NA=cp('paired_N_times_anchored_A'),gamma_squared=cp('gamma_squared_denominator'),fixed_E0=cp('fixed_lowered_E0'),formal_Iu=cp('formal_I_times_u'),envelopes={n[len(ep):]:a.copy() for n,a in cd.items() if n.startswith(ep)},constants=cache_ref['metadata']['constants'],candidate_provenance=provenance,configuration_held=True)
 for family in ('s','c'):
  for n,a in cache[family].items():assert np.array_equal(a.view(np.uint64),candidate[family][n].view(np.uint64)),(family,n)
 assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(cache['fixed_E0'],owned['E0']))
 tx=seal('TRANSACTION_COPY',dict(column=iq,fresh_stages={n:thin(r) for n,r in q.items()},fixed147_cache=thin(cache_ref),same_raw_configuration_and_E0_words_verified=True,old_rate_dependent_current_contacts_reused=False,physical_adoption=False))
 return candidate,cache,tx


def new_direction(basis):
 n=np.zeros((33,3,87,45));m=np.zeros((6,87,45))
 for mode,component,i,j,v in ((0,0,2,0,-.25),(12,2,2,0,.125),(0,1,31,18,-.0625),(19,0,31,18,.25),(27,2,86,22,-.125),(32,0,42,44,.0625)):n[mode,component,i,j]=v
 for slot in range(6):m[slot,31,18]=(-1.)**(slot+1)*2.**(-4-slot)
 m[1,2,0]=-.125;m[2,86,22]=.0625;m[5,42,44]=-.03125
 n[~np.broadcast_to(P.native_mask(),n.shape)]=0;m[~P.metric_mask()]=0;native=(n,-2.**-60*n);metric=(m,-2.**-60*m)
 lg_keep('NEW_refreshed_direction_packed',P.pack_dd(native,metric),keep);pn=lg_keep('NEW_refreshed_direction_native_values',P.dd_native_node_value(native,basis,keep,jet=0),keep);pm=lg_keep('NEW_refreshed_direction_metric_values',P.dd_metric_node_value(metric,basis,keep,jet=0),keep)
 ref=seal('DIRECTION',dict(kind='NEW_paired_original_E_F_probe_at_fresh_TOTAL_current',cells=DECLARED_CELLS,low_word_scale=-2.**-60,old_direction_or_lift_replayed=False,physical_adoption=False));return native,metric,pn,pm,ref


def packet(refs):
 basis=selected(refs['mechanical']['input'],tuple('registered_basis_'+n for n in ('R','dv','hats','cell_i','cell_j','r','z')),'closed_same_basis');basis={n.removeprefix('registered_basis_'):a for n,a in basis.items()}
 fb=selected(refs['finite_input'],tuple('completed_INPUT_basis_'+n for n in ('R','dv','hats')),'NEW139_basis')
 for n in ('R','dv','hats'):assert np.array_equal(basis[n].view(np.uint64),fb['completed_INPUT_basis_'+n].view(np.uint64))
 inp=seal('INPUT',dict(kind='NEW139_closed_point_TOTAL_current_for_literal142_eL',finite_input=thin(refs['finite_input']),finite_readout=thin(refs['finite_readout']),anchor_input=thin(refs['anchor_input']),anchor_canonical=thin(refs['anchor_canonical']),same_basis_from=thin(refs['mechanical']['input']),old_primal_current_EOS_or_solver_replayed=False,physical_adoption=False))
 shapes=dict(native=[33,3,87,45],metric=[6,87,45]);targets=selected(refs['anchor_canonical'],tuple('NEW_reference_anchor_unchanged_or_prepared_target_'+n+'_'+w for n in shapes for w in ('hi','lo'))+tuple('NEW_reference_anchor_target_minus_current_epsilon_metric_'+w for w in ('hi','lo')),'unchanged_anchor_targets')
 current=selected(refs['finite_readout'],tuple('completed_READOUT_current_'+n+'_'+w for n in shapes for w in ('hi','lo')),'NEW139_registered_S_current')
 original=selected(refs['anchor_input'],('original_reference_original_rhs','original_reference_current_Pn','original_reference_native_scale','original_reference_metric_scale'),'unchanged_original_references_scales')
 for n in ('original_reference_native_scale','original_reference_metric_scale'):assert np.all(original[n]>0)
 epsilon={n:lg_keep('NEW_refreshed_epsilon_'+n,P.a_sub(saved_pair(targets,'NEW_reference_anchor_unchanged_or_prepared_target_'+n),saved_pair(current,'completed_READOUT_current_'+n)),keep) for n in shapes}
 cre=seal('CANONICAL_COPY',dict(kind='fixed_anchor_target_minus_fresh139_registered_current',anchor=thin(refs['anchor_canonical']),fresh_current=thin(refs['finite_readout']),epsilon_sign='target minus registered current',metric_denominator_is_original_anchor_epsilon=True,original_targets_and_scales_unchanged=True,registered_current_copied_not_rescattered=True,physical_adoption=False))
 native,metric,pn,pm,direction=new_direction(basis);columns=[];gradients=[];bounds=[];transactions=[]
 for iq in range(4):
  candidate,cache,tx=hydrate(refs,iq);transactions.append(tx);label='NEW_refreshed_literal_q%d'%iq;CONTEXT.update(stage='fresh_literal142_reverse_chain',column=iq)
  gradient=candidate_literal_temporal_gradient_bridge(candidate,cache,keep,label);positive=candidate_literal_gradient_positive(candidate,cache,keep,label+'_unsigned')
  for n,pair in gradient['literal'].items():upper=mp_add(abs(pair[0]),abs(pair[1]),keep,label+'_represented_magnitude');keep(label+'_compared_'+n+'_outward_bound',positive[n]);assert np.all(upper<=positive[n])
  components={n:tuple(AVAILABLE[label+'_literal_'+suffix+'_'+w].copy() for w in ('hi','lo')) for n,suffix in (('nu_Maxwell','nu_Maxwell_adjoint'),('nu_acceleration','nu_acceleration_adjoint'),('nz_V','nz_V_adjoint'),('nz_D','nz_D_adjoint'))}
  gr=seal('GRADIENT_COLUMN',dict(column=iq,transaction=tx,current_U_outer_Z_retained=True,coefficient_polynomial_derivative_not_bitwise_EFT_AD=True,physical_adoption=False));columns.append(gr);gradients.append(gradient['literal']);bounds.append(positive)
  sl=slice(iq*3784,(iq+1)*3784);physical=dict(native=tuple(a[:,sl].transpose(1,0,2).reshape(3784,99).copy() for a in pn),metric=tuple(a[sl].copy() for a in pm))
  jets=candidate_temporal_jets(cache,physical,keep,label+'_NEW_jets');nu,nz=new_covariant_direction(cache,jets,label+'_NEW_covariant_direction');jr=seal('JET_COLUMN',dict(column=iq,transaction=tx,direction=direction,NEW_temporal_jets_only_no_primal_or_canonical_action=True,physical_adoption=False))
  control=independent_component_contacts(candidate,cache,gradient,components,jets,physical,nu,nz,label+'_independent');seal('COMPONENT_CONTACT',dict(column=iq,gradient=gr,jets=jr,control=control,controls=list(CHECKS[-6:]),original_tolerance=2e-11,physical_adoption=False))
  del candidate,cache,gradient,positive,components,jets,nu,nz
 literal={n:tuple(np.concatenate([q[n][w] for q in gradients]) for w in (0,1)) for n in ('native','metric_native','metric_EH','metric_total')}
 for n,pair in literal.items():lg_keep('NEW_refreshed_literal_full_point_'+n,pair,keep)
 weak=literal_est(literal['native'],literal['metric_total'],basis,'NEW_refreshed_literal_full_weak');bound=literal_est_positive(np.concatenate([q['native'] for q in bounds]),np.concatenate([q['metric_total'] for q in bounds]),basis,'NEW_refreshed_literal_full_weak_unsigned');upper=mp_add(abs(weak[0]),abs(weak[1]),keep,'NEW_refreshed_literal_full_weak_magnitude');assert np.all(upper<=bound)
 wr=seal('EVALUATION_TRANSPOSE',dict(columns=columns,basis=thin(refs['mechanical']['input']),weight64='original dv/R once before unweighted original E/F transpose',literal_weak_from_fresh_current=True,registered_S_association_distinct=True,physical_adoption=False))
 fields=[P.unpack_fields(w,False) for w in weak];eL={}
 for n,index in (('native',0),('metric',1)):
  L=tuple(q[index] for q in fields);registered=saved_pair(current,'completed_READOUT_current_'+n);gap=lg_keep('NEW_weak_literal_minus_registered_'+n,P.a_sub(L,registered),keep);eL[n]=lg_keep('NEW_literal_stationarity_eL_'+n,P.a_sub(epsilon[n],gap),keep)
 packed=lg_keep('NEW_literal_stationarity_eL_packed',P.pack_dd(eL['native'],eL['metric']),keep)
 lg_keep('NEW_literal_registered_epsilon_packed',P.pack_dd(epsilon['native'],epsilon['metric']),keep);keep('NEW_literal_original_scale_packed',P.pack_fields(original['original_reference_native_scale'],original['original_reference_metric_scale']));keep('NEW_literal_source_operation_bound_packed',bound)
 bridge=seal('WEAK_BRIDGE',dict(canonical=cre,literal=wr,finite_readout=thin(refs['finite_readout']),anchor_input=thin(refs['anchor_input']),anchor_canonical=thin(refs['anchor_canonical']),epsilon_sign='target minus registered current',eL_sign='epsilon minus (literal minus registered)',normal_feedback_sign='minus Cstar lambda_mechanical minus Cpstar lambda_phase',same_new_state_adjoint_required=True,old_lambda_or_gauge_current_reused=False,stationarity_or_feedback_zero_assumed=False,physical_adoption=False))
 independent_weighted_evaluation_contact(literal,weak,basis,native,metric,'NEW_refreshed_weighted_Estar_polynomial');contact=seal('WEAK_CONTACT',dict(direction=direction,literal=wr,controls=list(CHECKS[-2:]),independent_Fraction_original_rounded_maps=True,physical_adoption=False))
 expected=['NEW_refreshed_literal_q%d_independent_'%iq+n for iq in range(4) for n in ('Maxwell','modal_V','modal_D','acceleration','formal_native','formal_EH')]+['NEW_refreshed_weighted_Estar_polynomial_'+n for n in ('native','metric')]
 assert [c['name'] for c in CHECKS]==expected and len(CHECKS)==26 and all(c['passed'] and c['tolerance']==2e-11 for c in CHECKS) and len(RECORDS)==22
 final=seal('PREPARATION',dict(input=inp,canonical_copy=cre,columns=columns,literal_weak=wr,stationarity_bridge=bridge,contact=contact,new_rate_dependent_feedback_required=True,physical_adoption=False));assert len(RECORDS)==23
 return dict(status='REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_AND_eL_CONTACTS_PASS',input=inp,transactions=transactions,canonical_copy=cre,columns=columns,literal_weak=wr,stationarity_bridge=bridge,preparation=final,finite_terminal=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),anchor_terminal=(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF),roles=23,new_controls=26,source_polynomial_only=True,normal_feedback_or_geometry_correction_admitted=False,physical_adoption=False)


def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(v is not None for q in (FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF) for v in q),'Root review and natural finite closure required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,future_finite_terminal=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),new_literal142_sections=4,new_controls=26,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW139_literal142_contact',context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
