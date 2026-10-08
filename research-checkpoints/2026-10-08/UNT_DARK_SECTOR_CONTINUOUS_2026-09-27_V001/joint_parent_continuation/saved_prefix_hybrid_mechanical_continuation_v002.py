"""HELD saved17-prefix hybrid mechanical search; root owns release/execution.
Authoritative original17 actions stay earned; later Ahat steps are proxy search.
Only NEW original147/67 + original six1e-10 gates can admit a correction.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='SAVED_PREFIX_HYBRID_MECHANICAL_CONTINUATION_V002'
DRIVER_PROTOCOL='SAVED_PREFIX_HYBRID_MECHANICAL_CONTINUATION_V002.md'
PROTOCOL_SHA='81e66a54afe1c9f6aec9c2c277279446e5c90c65abb32ed040c945286eaa8d0a'
PREFIX_SOURCE=(None,None)
PREFIX_RESULT=(None,None,'ORIGINAL_MECHANICAL_GMRES17_SCALAR_STATE_RECONSTRUCTED')
PREFIX_RECEIPT=(None,None,'CLOSED')
PREFIX_PROOF=(None,None,'ROOT_NATURAL_CLOSED_GMRES17_SCALAR_RECOVERY_SUCCESS_SEALS_VERIFIED')
SAMPLED_SOURCE=(None,None)
SAMPLED_RESULT=(None,None,'NEW_MECHANICAL_COEFFICIENT_FORWARD_TWO_DIRECTION_ASSOCIATIONS_SAVED_RECOVERED')
SAMPLED_RECEIPT=(None,None,'CLOSED')
SAMPLED_PROOF=(None,None,'ROOT_NATURAL_CLOSED_SAVED_ONLY_COEFFICIENT_FORWARD_RECOVERY_SEALS_VERIFIED')
ORPHAN18_CRC_PROOF=(None,None)
SELECTED_OUTPUT_PROOF=(None,None,'CLOSED34002_PARTIAL_SUCCESS_OUTPUT_BYTE_SEALS_VERIFIED')
OLD_SOURCE=('cross_u_candidate_right_only_mechanical_response_v003.py','6988334ae0fbb84541c91b8c89d4481f81170d8d5f2deb79f7b85561d7cc6d9b')
OLD_STEM='CROSS_U_CANDIDATE_RIGHT_ONLY_MECHANICAL_RESPONSE_V003'
SEARCH_POLICY='replace_unfinished_original18_with_coefficient_proxy_search'
CAP=80
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
CAPTURE_MODE='bounded';SMALL_STATE={};PREFIX_BASIS=[];CURRENT_CANDIDATE=None;NEW_BASIS=[];NEW_STEPS=[];ACTION_SEQUENCE=[]
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
NODAL_SOURCE=('cross_u_candidate_directed_nodal_preconditioner_preparation_v005.py', '41d6b4b3d200c8e017759ee3f95e05addaf3d7ea59b53a61f0fcc12b3f514659')
NODAL_RESULT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RESULT.json', '20ddbdfe237cf5062440971f59b838046962994ad9517d3851d400e3e3b8a811', 'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
NODAL_RECEIPT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RECEIPT.json', '46221584fefc9a1ee67cfe62cdf6b27d4710964f60b4ad7865ed6e48e0cdd57b', 'CLOSED')
NODAL_PROOF=('ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_V001.json', '915f5cb58d42291166940df770359ab4416ef153c47dba9b43c680dbc6a6b7af', 'ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_VERIFIED')
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py': 'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db', 'author_fragment_candidate_directed_nodal_factor_apply_v001.py': '4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_native_metric_star_paired_gmres_v001.py': '3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770', 'author_fragment_candidate_right_only_mechanical_gmres_v001.py': '3fb3ec63aebea319e6e673b13fa7ec8fefba88791458f83ad481ff2ca26b16ab', 'author_fragment_initial_york_trace_target_response_v001.py': '71fda02b76e03c5ac4fe917f0514a3f13e60ec15b9aad21610045fbe40fe71e1', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_native_metric_star_paired_gmres_resume_v002.py': '73b15a0e0512295aed41389a80c20ec6cf50ddef634497c805ada69c8ed738ee', 'author_fragment_candidate_mechanical_coefficient_forward_v001.py': 'bc6e09716ab71ed9a43ff6bd27666a393fe0584f7ac1ac3ed5d519edd747c3c7'}

def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(IO_PARENT,names),IO_PARENT,'exec'),globals());initialize_io()
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,None),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']

def initialize_helpers():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','pack_fields','unpack_fields','collapse','fields_from_pair','dd_node_update','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
  for n in names:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|{'B','GC','C','ALPHA','ELL'}})
 for n in ('B','GC','C','ALPHA','ELL'):setattr(P,n,SCOPE[n])
 P.LINEAR_TOL=1e-10
 choices=(('author_fragment_finite_york_geometry_target_v001.py',None),('author_fragment_compact_metric_contact_momenta_v002.py',{'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}),('author_fragment_candidate_specialized_temporal_action_v001.py',{'ft_keep','candidate_temporal_jets','candidate_temporal_canonical','candidate_specialized_temporal_action'}),('author_fragment_candidate_specialized_weak_mechanical_action_v002.py',{'sw_keep','specialized_weak_mechanical_action'}),('author_fragment_candidate_directed_nodal_factor_apply_v001.py',None),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_provider_admission','candidate_point_cache_names'}),('author_fragment_native_metric_star_paired_gmres_v001.py',{'native_metric_gmres_put','native_metric_gmres_tree','native_metric_gmres_dot','native_metric_gmres_expansion','native_metric_gmres_norm','native_metric_gmres_upper','native_metric_gmres_candidate','native_metric_gmres_solve'}),('author_fragment_candidate_right_only_mechanical_gmres_v001.py',None),('author_fragment_initial_york_trace_target_response_v001.py',{'trace_target_reference_scores'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',None),('cross_u_candidate_literal_phase_charge_response_v002.py',{'bind_record'}),('author_fragment_exact_exponent_two_product_v003.py',None))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_candidate_chunk_point_block_provider_v001.py'
 for n in ast.parse((BASE/file).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('POINT_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_mechanical_exact_exponent_product')

def bounded_keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a
 if any(name=='hybrid_mechanical_GMRES_right_only_'+n for n in ('H_hi','H_lo','R','Givens_cos','Givens_sin','rotated_RHS','history','all_Arnoldi_contact_norms','all_Arnoldi_operation_bounds')):SMALL_STATE[name]=a.copy()
 assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name
 if CAPTURE_MODE=='bounded':
  while len(AVAILABLE)>12:AVAILABLE.pop(next(iter(AVAILABLE)))
 return a

def initialize():
 load_io();globals()['keep']=bounded_keep;initialize_helpers()
 f='author_fragment_native_metric_star_paired_gmres_resume_v002.py';exec(compile(selected_definitions(f,None),f,'exec'),globals())
 f='author_fragment_candidate_mechanical_coefficient_forward_v001.py';exec(compile(selected_definitions(f,None),f,'exec'),globals())
 exec(compile(selected_definitions(list(PINS)[1],{'pack_dd','scalar_mask'}),list(PINS)[1],'exec'),SCOPE);P.pack_dd=SCOPE['pack_dd'];P.scalar_mask=SCOPE['scalar_mask'];globals().update(pack_dd=P.pack_dd,scalar_mask=P.scalar_mask)
 globals().update(GMRES_RESUME_AUTHOR_DRAFT=False,GMRES_RESUME_AUTHORING_IN_PROGRESS=False,GMRES_RESUME_PREFIX_PROOF=PREFIX_PROOF,GMRES_RESUME_COEFFICIENT_PROOF=SAMPLED_PROOF,COEFFICIENT_FORWARD_AUTHOR_DRAFT=False,COEFFICIENT_FORWARD_AUTHORING_IN_PROGRESS=False,COEFFICIENT_FORWARD_SOURCE=NODAL_SOURCE,COEFFICIENT_FORWARD_RESULT=NODAL_RESULT,COEFFICIENT_FORWARD_RECEIPT=NODAL_RECEIPT,COEFFICIENT_FORWARD_PROOF=NODAL_PROOF)
 P.LINEAR_TOL=1e-10

def closed_packet(source,result,receipt,proof):
 for q in (source,result,receipt,proof):assert all(x is not None for x in q);bind(q[0],q[1])
 r=json.loads(P.path(result[0]).read_text());rc=json.loads(P.path(receipt[0]).read_text());pr=json.loads(P.path(proof[0]).read_text())
 assert r['status']==result[2] and rc['status']==receipt[2] and rc['result_sha256']==result[1] and rc['error_sha256'] is None
 assert r['owner']==rc['owner']==pr['owner'] and r['owner']['source_sha256']==source[1]
 assert pr['status']==proof[2] and pr['source_sha256']==source[1] and pr['result_sha256']==result[1] and pr['receipt_sha256']==receipt[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==0 and pr['all_input_seals_verified'] is True and pr['all_success_role_seals_verified'] is True
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 assert all(c['passed'] is True and c['tolerance']==2e-11 for c in r['controls'])
 return r,rc

def commit(ref,receipt=None):
 bind(ref['commit_file'],ref['commit_sha256']);q=json.loads(P.path(ref['commit_file']).read_text())
 assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
 if receipt is not None:
  assert all(receipt['output_sha256'][ref[f]]==ref[h] for f,h in (('file','sha256'),('commit_file','commit_sha256')))
 assert q['metadata']['failed'] is False and all(v is False for v in q['metadata']['qualification'].values())
 return dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def read_selected(q,names):
 # Full archive byte identity is inherited from the proof authenticated before this read.
 md=q['metadata'];out={}
 with np.load(P.path(q['file']),allow_pickle=False) as f:
  assert set(f.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md
  for n in names:
   a=f[n].copy();s=md['schema'][n];keep('loaded_'+n,a);assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True and np.all(np.isfinite(a));out[n]=a
 return out

def packed_pair(d,name):return tuple(d[name+'_'+w].copy() for w in ('hi','lo'))

def publish_compact(role,data,metadata):
 q=P.checkpoint(role,arrays(data),dict(metadata,context=dict(CONTEXT)));clear_current();return thin(q)

def admission():
 bind(*OLD_SOURCE);bind(SELECTED_OUTPUT_PROOF[0],SELECTED_OUTPUT_PROOF[1]);pr=json.loads(P.path(SELECTED_OUTPUT_PROOF[0]).read_text())
 assert pr['status']==SELECTED_OUTPUT_PROOF[2] and pr['source']['sha256']==OLD_SOURCE[1] and pr['all_success_role_seals_verified'] is True
 assert pr['observed_closure_evidence']['observed_exit_code']==1 and pr['observed_closure_evidence']['original_failed_run_preserved'] is True
 old=[]
 for i,tag in enumerate(('INPUT','CACHE_COPY','CACHE_COPY','CACHE_COPY','CACHE_COPY','FACTOR_COPY')):
  rows=[q for q in pr['records'] if q['ordinal']==i];assert len(rows)==1;x=rows[0]
  assert x['role']==tag and x['file']==OLD_STEM+'_%05d_'%i+tag+'.npz' and x['failed'] is False
  assert all(x[n] is True for n in ('owner_equal','embedded_metadata_equal','member_names_headers_and_structural_lengths_equal','qualification_all_false'))
  q=commit(x);assert q['metadata']['owner']==pr['owner'] and P.path(x['file']).stat().st_size==x['data_bytes'];old.append(q)
 prefix,pc=closed_packet(PREFIX_SOURCE,PREFIX_RESULT,PREFIX_RECEIPT,PREFIX_PROOF);case=prefix['case'];assert case['selected_original_roles']==53 and case['original_owner']==pr['owner']
 assert len(case['basis'])==18 and len(case['scalar_steps'])==17 and case['old_actions_factors_or_controls_replayed'] is False
 sampled,sc=closed_packet(SAMPLED_SOURCE,SAMPLED_RESULT,SAMPLED_RECEIPT,SAMPLED_PROOF)
 assert sampled['case']['original_observed_exit_code']==1 and sampled['case']['roles']==523 and sampled['case']['new_scientific_actions']==0 and len(sampled['controls'])==4
 nodal,nc=closed_packet(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)
 assert old[0]['metadata']['closed_provenance']['factor']==json.loads(json.dumps((NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)))
 bind(ORPHAN18_CRC_PROOF[0],ORPHAN18_CRC_PROOF[1]);orphan=json.loads(P.path(ORPHAN18_CRC_PROOF[0]).read_text())
 assert orphan['closed_workers_only'] is True and orphan['numerical_array_interpretation_or_action_executed'] is orphan['original_archives_mutated'] is False
 assert SEARCH_POLICY=='replace_unfinished_original18_with_coefficient_proxy_search'
 original18=[dict(file=q['file'],sha256=q['sha256'],commit_file=q['commit_file'],commit_sha256=q['commit_sha256']) for q in pr['records'] if q['ordinal'] in (109,110,111)]
 assert len(original18)==3 and all(q['role']=='ACTION_COLUMN' for q in pr['records'] if q['ordinal'] in (109,110,111))
 return dict(original18_columns=original18,old=old,old_proof=pr,prefix=prefix,prefix_receipt=pc,nodal=nodal,nodal_receipt=nc,sampled=sampled,orphan=orphan)

def hydrate(refs):
 global PREFIX_BASIS
 case=refs['prefix']['case'];rc=refs['prefix_receipt'];ctx=commit(case['context'],rc);assert ctx['metadata']['source']==thin(refs['old'][0]) and ctx['metadata']['factor_context']['copy']==thin(refs['old'][5]);assert ctx['metadata']['factor_context']['terminal']==json.loads(json.dumps((NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)));cd=read_selected(ctx,tuple(ctx['metadata']['schema']))
 start=packed_pair(cd,'start');rhs=packed_pair(cd,'rhs');current=dict(action=packed_pair(cd,'current_action'),residual=packed_pair(cd,'current_residual'),scores=cd['current_scores'].copy(),admitted=False)
 V=[];PREFIX_BASIS=list(case['basis'])
 for j,ref in enumerate(PREFIX_BASIS):
  q=commit(ref,rc);assert q['metadata']['context']['basis']==j and q['metadata']['factor_context']==ctx['metadata']['factor_context'];d=read_selected(q,('basis_hi','basis_lo'));V.append(packed_pair(d,'basis'))
 stateq=commit(case['resume_state'],rc);sd=read_selected(stateq,tuple(stateq['metadata']['schema']));md=stateq['metadata'];assert md['next_iteration']==md['iterations']==17 and md['cap']==80
 state=dict(sd);state.update(V=V,start=start,rhs=rhs,current=current,updated=start,after=dict(current,admitted=False),increment=P.a_dd(np.zeros(403340)),prefix_proof=PREFIX_PROOF,coefficient_proof=SAMPLED_PROOF)
 for n in ('cap','iterations','next_iteration','reason','column_action_scopes','prefix_state_authenticated','original_associations_or_committed_state_verified','all_available_next_basis_words_matched','completed_actions_and_factors_not_replayed','original_rhs_warm_current_and_six_references_unchanged','original_right_and_left_maps_unchanged'):state[n]=md[n]
 state['initial_norm']=float(sd['initial_norm']);state['history']=sd['history'].tolist();state['Arnoldi_contact_norms']=sd['Arnoldi_contact_norms'].tolist();state['Arnoldi_operation_bounds']=sd['Arnoldi_operation_bounds'].tolist()
 firstq=commit(case['earned_first_forward'],rc);firstd=read_selected(firstq,('earned_solution_hi','earned_solution_lo'));assert firstq['metadata']['exact_input_basis']==case['basis'][17] and firstq['metadata']['factor_context']==ctx['metadata']['factor_context']
 assert firstq['metadata']['must_return_once_after_exact_argument_context_match'] is True and firstq['metadata']['factor_application_replayed'] is False
 oldinput=refs['old'][0];bd=read_selected(oldinput,tuple('copied_anchor_input_original_basis_'+n for n in ('R','dv','hats')));basis={n:bd['copied_anchor_input_original_basis_'+n] for n in ('R','dv','hats')};caches=[]
 for iq,q in enumerate(refs['old'][1:5]):
  assert q['metadata']['column']==iq;src=commit(q['metadata']['source']);names=candidate_point_cache_names(src['metadata']);d=read_selected(q,tuple('copied_cache%d_'%iq+n for n in names));d={n:d['copied_cache%d_'%iq+n] for n in names};prefix=POINT_CACHE_PREFIX;ep=prefix+'copied_positive_coefficient_'
  pair=lambda n:packed_pair(d,prefix+n)
  caches.append(dict(s={n:d[prefix+'raw_configuration_'+n] for n in POINT_S},c={n:d[prefix+'raw_chart_'+n] for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a for n,a in d.items() if n.startswith(ep)},constants=src['metadata']['constants'],candidate_provenance=src['metadata']['candidate_provenance'],configuration_held=True,old_coefficients_or_primal_features_replayed=False))
  assert all(caches[-1]['constants'][n]==getattr(P,n) for n in ('C','ALPHA','ELL'))
 fd=read_selected(refs['old'][5],tuple('copied_factor_'+n+'_'+w for n in ('D_inverse','S_inverse','B','E') for w in ('hi','lo')))
 factors={n:packed_pair(fd,'copied_factor_'+n) for n in ('D_inverse','S_inverse','B','E')};factors.update(closed_provenance=dict(factor_record=refs['old'][5]['metadata']['factors'],terminal=(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)),all_active_factor_seals_verified=True,active_node_count=3870,right_preconditioner_factor_resolved=True,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
 prepared=prepare_candidate_directed_nodal_factor_apply(factors,keep,'NEW_reused_factor_coordinate_guard');clear_current()
 return dict(context=ctx,data=cd,state=state,start=start,rhs=rhs,current=current,basis=basis,blocks=dict(columns=caches,basis=basis),factors=prepared,first=packed_pair(firstd,'earned_solution'),first_ref=case['earned_first_forward'],first_meta=firstq['metadata'])

def coefficient_prepare(refs,packet):
 r,rc=refs['nodal'],refs['nodal_receipt'];case=r['case'];assert len(case['completed_chunk_refs'])==120 and case['right_preconditioner_factor_resolved'] is True
 assert case['closed_mechanical']==refs['old'][0]['metadata']['closed_provenance']['mechanical']
 inp=commit(case['input'],rc);bprov=inp['metadata']['basis_provenance'];chunks=[]
 bd=read_selected(inp,tuple('original_registered_basis_'+n for n in ('R','dv','hats')))
 for n in ('R','dv','hats'):assert np.array_equal(bd['original_registered_basis_'+n],packet['basis'][n])
 for serial,ref in enumerate(case['completed_chunk_refs']):
  q=commit(ref,rc);md=q['metadata'];iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784);p=hi-lo;prefix='NEW_directed_nodal_q%d_chunk%03d_point_'%(iq,serial)
  assert md['kind']=='completed_directed_nodal_moment_chunk_patch' and md['column']==iq and md['selection']==[lo,hi] and md['basis_provenance']==bprov
  cp=packet['blocks']['columns'][iq]['candidate_provenance'];point=commit(md['committed_point_chunk'],rc);assert point['metadata']['closed_candidate_provenance']==cp
  names={n:tuple(prefix+'paired_raw_'+n+'_'+w for w in ('hi','lo')) for n in ('H','B','E','D')};names.update({'e'+n:prefix+'e'+n for n in ('H','B','E','D')})
  for n,shape in dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3)).items():
   for key in names[n]+(names['e'+n],):assert md['schema'][key]==dict(shape=list(shape),dtype='float64',finite=True)
  chunks.append(dict(column=iq,lo=lo,hi=hi,point_block_ref=thin(q),same_candidate_provenance=cp,basis_provenance=bprov,selected_names=names,committed_original_point=thin(point)))
 closed=dict(source=NODAL_SOURCE,result=NODAL_RESULT,receipt=NODAL_RECEIPT,proof=NODAL_PROOF,naturally_closed=True,natural_exit_code=0,all_selected_seals_verified=True,physical_adoption=False,same_candidate_provenance=[c['candidate_provenance'] for c in packet['blocks']['columns']]);basis=dict(packet['basis'],closed_provenance=bprov)
 return prepare_candidate_mechanical_coefficient_forward(chunks,basis,closed,keep,'NEW_same_nodal_coefficient_guard')

def continuation(refs,packet,proxy):
 global CAPTURE_MODE,CURRENT_CANDIDATE
 first_used=False;step_refs=[];right_refs=[];candidate_refs=[];label='hybrid_mechanical_GMRES_right_only';state=packet['state'];CURRENT_CANDIDATE=dict(context=refs['prefix']['case']['context'],initial=True)
 native_ref=P.unpack_fields(packet['data']['copied_anchor_input_original_reference_original_rhs'],False)[0];canonical_ref=packet['data']['copied_anchor_input_original_reference_current_Pn'];scales=tuple(packet['data']['copied_anchor_input_original_reference_'+n] for n in ('native_scale','metric_scale'))
 metric_pair=packed_pair(packet['data'],'copied_anchor_canonical_NEW_reference_anchor_target_minus_current_epsilon_metric');metric_ref=metric_pair[0]+metric_pair[1]
 def scores(res,tag):
  rows,norms,zero=trace_target_reference_scores(res,native_ref,canonical_ref,metric_ref,scales,tag);fields=[P.unpack_fields(a,False) for a in res]
  for row,field in ((0,0),(1,0),(2,1)):
   if zero[row] and any(np.any(q[field]!=0) for q in fields):rows[row]=1.
  keep(tag+'_both_word_exact_zero_reference_authoritative_scores',rows.copy());return rows
 def right(x,tag):
  nonlocal first_used
  CONTEXT.update(stage='right_factor',label=tag,search_basis_index=17+len(NEW_BASIS))
  if not first_used:
   assert all(np.array_equal(x[w].view(np.uint64),state['V'][17][w].view(np.uint64)) for w in (0,1));assert packet['first_meta']['factor_context']==packet['context']['metadata']['factor_context'];first_used=True
   right_refs.append(publish_compact('EARNED_FORWARD_REUSE',dict(index=np.asarray(17,dtype=np.int64)),dict(source=packet['first_ref'],exact_both_word_argument_match=True,exact_factor_context_match=True,factor_application_replayed=False)));return tuple(a.copy() for a in packet['first'])
  out=candidate_directed_nodal_factor_apply(packet['factors'],x,keep,tag);right_refs.append(publish_compact('RIGHT_APPLY',dict(input_hi=x[0],input_lo=x[1],output_hi=out[0],output_lo=out[1]),dict(kind='NEW_same_original_right_factor',label=tag,factors=thin(refs['old'][5]),physical_adoption=False)));return out
 def forward(x,tag):return right(x,tag+'_signed_active_nodal_right_factor')
 def read_chunk(d,names):
  CONTEXT.update(stage='proxy_chunk',column=d['column'],selection=[d['lo'],d['hi']]);q=commit(d['point_block_ref'],refs['nodal_receipt']);keys=tuple(key for n in ('H','B','E','D') for key in d['selected_names'][n]);data=read_selected(q,keys)
  return dict(record=d['point_block_ref'],source_provenance=d['same_candidate_provenance'],paired_raw={n:tuple(data[k] for k in d['selected_names'][n]) for n in ('H','B','E','D')})
 def proxy_action(x,tag):
  request=publish_compact('ACTION_REQUEST',dict(input_hi=x[0],input_lo=x[1]),dict(label=tag,scope='coefficient_proxy',original18_replaced_search_change=True));chunks=[]
  def complete_chunk(d,part):
   q=publish_compact('PROXY_CHUNK',dict(native_hi=part[0][0],native_lo=part[0][1],metric_hi=part[1][0],metric_lo=part[1][1]),dict(request=request,source=d['point_block_ref'],column=d['column'],selection=[d['lo'],d['hi']],scope='coefficient_proxy'));chunks.append(q);return q
  def complete_column(iq,data):return publish_compact('PROXY_COLUMN',dict(column=np.asarray(iq,dtype=np.int64)),dict(request=request,chunks=data['chunk_refs'],scope='coefficient_proxy',same_candidate_provenance=data['same_candidate_provenance']))
  out=candidate_measured_coefficient_fullweak_forward(proxy,x,read_chunk,keep,tag,complete_chunk,complete_column);y=out['packed'];q=publish_compact('ACTION_WEAK',dict(output_hi=y[0],output_lo=y[1]),dict(request=request,chunks=chunks,columns=out['column_refs'],scope='coefficient_proxy',uniform_original147_equality_qualified=False));ACTION_SEQUENCE.append(q);return y
 def acceptance_action(x,tag):
  global CAPTURE_MODE
  request=publish_compact('ACTION_REQUEST',dict(input_hi=x[0],input_lo=x[1]),dict(label=tag,scope='authoritative147'));CONTEXT.update(stage='authoritative147',label=tag,request=request,column=0);fields=[P.unpack_fields(a,False) for a in x];cols=[];CAPTURE_MODE='column'
  def complete(iq,data):
   p=data['specialized_temporal_result']['point'];q=publish_compact('AUTHORITATIVE_COLUMN',dict(native_hi=p['native'][0],native_lo=p['native'][1],metric_hi=p['metric_total'][0],metric_lo=p['metric_total'][1]),dict(request=request,column=iq,cache=thin(refs['old'][iq+1]),scope='authoritative147',all_previous_completed_column_outputs_retained=True));cols.append(q);CONTEXT.update(stage='authoritative147',label=tag,request=request,column=iq+1);return q
  out=specialized_weak_mechanical_action(packet['blocks'],packet['basis'],tuple(q[0] for q in fields),tuple(q[1] for q in fields),keep,tag,complete);CAPTURE_MODE='bounded';y=tuple(P.pack_fields(out['weak']['native'][w],out['weak']['metric'][w]) for w in (0,1));q=publish_compact('ACTION_WEAK',dict(output_hi=y[0],output_lo=y[1]),dict(request=request,columns=cols,scope='authoritative147'));ACTION_SEQUENCE.append(q);return y
 def positive(x,tag):
  CONTEXT.update(stage='original_positive124',label=tag)
  e=candidate_weak_mechanical_positive(packet['blocks'],packet['basis'],x,keep,tag);publish_compact('ACTION_POSITIVE',dict(envelope=e),dict(label=tag,source='original124_unsigned147_E_S',authoritative147_envelope_not_proxy_factor=True));return e
 def progress(iteration,nodes,after,increment):
  global CURRENT_CANDIDATE
  CURRENT_CANDIDATE=publish_compact('CANDIDATE',dict(nodes_hi=nodes[0],nodes_lo=nodes[1],action_hi=after['action'][0],action_lo=after['action'][1],residual_hi=after['residual'][0],residual_lo=after['residual'][1],increment_hi=increment[0],increment_lo=increment[1],scores=after['scores']),dict(iteration=iteration,admitted=after['admitted'],acceptance_scope='original147_and_original_six_1e10'));candidate_refs.append(CURRENT_CANDIDATE)
 def iteration_checkpoint(iteration,new_basis,small):
  q=publish_compact('BASIS',dict(basis_hi=new_basis[0],basis_lo=new_basis[1]),dict(basis_index=iteration,original_prefix_basis=PREFIX_BASIS,scope='proxy_generated_search_basis'));NEW_BASIS.append(q)
  data={n:np.asarray(small[n]) for n in ('H_hi','H_lo','R','Givens_cos','Givens_sin','rotated_RHS','initial_norm','history','Arnoldi_contact_norms','Arnoldi_operation_bounds')};step=publish_compact('ITERATION_STATE',data,dict(next_iteration=iteration,cap=80,basis=PREFIX_BASIS+NEW_BASIS,candidate_context=CURRENT_CANDIDATE,reason=small['reason'],column_action_scopes=small['column_action_scopes'],original_context=refs['prefix']['case']['context'],completed_new_action_refs=list(ACTION_SEQUENCE),single_uniform_original_A_relation_qualified=False));step_refs.append(step)
 updated,after,increment,history=native_metric_gmres_solve(packet['start'],packet['current'],packet['rhs'],forward,candidate_right_identity_left,acceptance_action,positive,scores,label,80,progress,state,proxy_action,acceptance_action,iteration_checkpoint)
 assert first_used and history['resumed_completed_iterations']==17 and history['saved_prefix_actions_or_factors_replayed'] is False
 terminal=publish_compact('TERMINAL_STATE',dict(SMALL_STATE,initial_norm=np.asarray(state['initial_norm'])),dict(history=history,basis=PREFIX_BASIS+NEW_BASIS,candidate_context=CURRENT_CANDIDATE,original_context=refs['prefix']['case']['context'],terminal_not_unconditionally_resumable=True,cap80_total=True))
 final=scores(after['residual'],'NEW_final_original_six');assert np.array_equal(final,after['scores']);admitted=bool(np.all(final<=P.LINEAR_TOL))
 solution=publish_compact('SOLUTION',dict(correction_hi=updated[0],correction_lo=updated[1],action_hi=after['action'][0],action_lo=after['action'][1],residual_hi=after['residual'][0],residual_lo=after['residual'][1],increment_hi=increment[0],increment_lo=increment[1],scores=final),dict(terminal_state=terminal,history=history,original_prefix=PREFIX_PROOF,sampled_validation_only_additional=SAMPLED_PROOF,coefficient_provenance=(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF),right_refs=right_refs,candidates=candidate_refs,iteration_states=step_refs,original18_completed_columns=refs['original18_columns'],original18_orphan_tail_proof=ORPHAN18_CRC_PROOF,original18_unfinished_not_completed=True,optional18_tail_recovery_not_executed=True,old_partial_outputs_preserved=True,physical_base_rates_reset=False,physical_adoption=False))
 return dict(status='HYBRID_SEARCH_ORIGINAL_SIX_MECHANICAL_ROWS_ADMITTED' if admitted else 'HYBRID_SEARCH_ORIGINAL_SIX_MECHANICAL_ROWS_NOT_ADMITTED',solution=solution,history=history,original_six_scores=final.tolist(),prefix_roles_inherited_without_replay=38,original_worker_exit_code=1,original18_search_change=SEARCH_POLICY,original18_recovered_or_discarded=False,cap80_total=True,restarts=0,physical_adoption=False,full_weak_inverse_qualified=False,normal_CMC_evolution_or_new43_readout_earned=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and all(v is not None for q in (PREFIX_SOURCE,PREFIX_RESULT,PREFIX_RECEIPT,PREFIX_PROOF,SAMPLED_SOURCE,SAMPLED_RESULT,SAMPLED_RECEIPT,SAMPLED_PROOF,SELECTED_OUTPUT_PROOF,ORPHAN18_CRC_PROOF) for v in q),'Root proof-bound FULL-reviewed release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required';initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(IO_PARENT,IO_PARENT_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,prefix_proof=PREFIX_PROOF,old_selected_output_proof=SELECTED_OUTPUT_PROOF,sampled_validation_only_additional=SAMPLED_PROOF,original_nodal_provenance=(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF),search_policy=SEARCH_POLICY,optional18_tail_proof=ORPHAN18_CRC_PROOF,full_original_unused_inputs_audited=False,physical_adoption=False));packet=hydrate(refs);proxy=coefficient_prepare(refs,packet);clear_current()
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=continuation(refs,packet,proxy)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='NEW_unfinished_hybrid_operation_with_saved_prefix_and_incremental_state',context=dict(CONTEXT),prefix_basis=PREFIX_BASIS,new_basis=NEW_BASIS,candidate=CURRENT_CANDIDATE,completed_action_refs=ACTION_SEQUENCE),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
