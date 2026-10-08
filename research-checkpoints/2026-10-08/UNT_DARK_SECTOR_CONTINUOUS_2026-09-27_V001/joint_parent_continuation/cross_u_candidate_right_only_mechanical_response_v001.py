"""HELD actual same-candidate right-only mechanical response.
Root binds naturally CLOSED target/cache/factor/apply proofs and executes only.
No old primal, current, target, EOS, factor, action, control or solve is replayed.
Original paired weak67/six gates own acceptance; nodal factors are numerical.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_RIGHT_ONLY_MECHANICAL_RESPONSE_V001'
DRIVER_PROTOCOL='CROSS_U_CANDIDATE_RIGHT_ONLY_MECHANICAL_RESPONSE_V001.md'
PROTOCOL_SHA='b2386dafbb4615e046706a1bace30c1fbce0519a582724821365ede1cefb6d4a'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
ANCHOR_SOURCE=(None,None)
ANCHOR_RESULT=(None,None,'REFERENCE_YORK_ANCHOR_TARGET_AND_CANONICAL_EPSILON_MEASURED')
ANCHOR_RECEIPT=(None,None,'CLOSED')
ANCHOR_PROOF=(None,None,None)
MECHANICAL_SOURCE=(None,None)
MECHANICAL_RESULT=(None,None,'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=(None,None,'CLOSED')
MECHANICAL_CLOSURE_PROOF=(None,None,None)
FACTOR_SOURCE=(None,None)
FACTOR_RESULT=(None,None,'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
FACTOR_RECEIPT=(None,None,'CLOSED')
FACTOR_PROOF=(None,None,None)
APPLY_SOURCE=(None,None)
APPLY_RESULT=(None,None,'DIRECTED_NODAL_REPRESENTED_FACTOR_ADJOINT_AND_NEW_WEAK_CONTACTS_PASS')
APPLY_RECEIPT=(None,None,'CLOSED')
APPLY_PROOF=(None,None,None)
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py': 'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db', 'author_fragment_candidate_directed_nodal_factor_apply_v001.py': '4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_native_metric_star_paired_gmres_v001.py': '3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770', 'author_fragment_candidate_right_only_mechanical_gmres_v001.py': '3fb3ec63aebea319e6e673b13fa7ec8fefba88791458f83ad481ff2ca26b16ab', 'author_fragment_initial_york_trace_target_response_v001.py': '71fda02b76e03c5ac4fe917f0514a3f13e60ec15b9aad21610045fbe40fe71e1', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d'}
CAP=80
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

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
 np=numpy;SCOPE.update(np=np,capture=keep,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','pack_fields','unpack_fields','collapse','fields_from_pair','dd_node_update','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
  for n in names:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|{'C','ALPHA','ELL'}});P.C=1.98;P.ALPHA=.02/1.98;P.ELL=.1;P.LINEAR_TOL=1e-10
 choices=(('author_fragment_finite_york_geometry_target_v001.py',None),('author_fragment_compact_metric_contact_momenta_v002.py',{'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}),('author_fragment_candidate_specialized_temporal_action_v001.py',{'ft_keep','candidate_temporal_jets','candidate_temporal_canonical','candidate_specialized_temporal_action'}),('author_fragment_candidate_specialized_weak_mechanical_action_v002.py',{'sw_keep','specialized_weak_mechanical_action'}),('author_fragment_candidate_directed_nodal_factor_apply_v001.py',None),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_provider_admission','candidate_point_cache_names'}),('author_fragment_native_metric_star_paired_gmres_v001.py',{'native_metric_gmres_put','native_metric_gmres_tree','native_metric_gmres_dot','native_metric_gmres_expansion','native_metric_gmres_norm','native_metric_gmres_upper','native_metric_gmres_candidate','native_metric_gmres_solve'}),('author_fragment_candidate_right_only_mechanical_gmres_v001.py',None),('author_fragment_initial_york_trace_target_response_v001.py',{'trace_target_reference_scores'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',None),('cross_u_candidate_literal_phase_charge_response_v002.py',{'bind_record'}),('author_fragment_exact_exponent_two_product_v003.py',None))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_candidate_chunk_point_block_provider_v001.py'
 for n in ast.parse((BASE/file).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('POINT_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_mechanical_exact_exponent_product')

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

def response_admission():
 anchor,arc=closed_packet(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF);case=anchor['case']
 assert len(anchor['checkpoints'])==6 and len(anchor['controls'])==5 and case['prepared_metric_target_is_exact_owned_reference'] is True and case['free_prior_or_target_refitted'] is case['new_varying_target_JVP'] is case['physical_adoption'] is False
 assert case['canonical_prefix']=='NEW_reference_anchor' and case['updated_phase_H_p_eH_copied_only'] is True
 inp=selected_record(case['input'],anchor,arc);canonical=selected_record(case['canonical'],anchor,arc);assert canonical['metadata']['input']==thin(inp) and canonical['metadata']['mechanical_current_unchanged_under_phase_update'] is True
 mechanical=candidate_point_provider_admission(bind);assert thin(mechanical['original_basis'])==case['original_basis']
 for iq,q in enumerate(mechanical['caches']):assert q['metadata']['state']==case['columns'][iq]['metadata']['state']
 factor,frc=closed_packet(FACTOR_SOURCE,FACTOR_RESULT,FACTOR_RECEIPT,FACTOR_PROOF);fc=factor['case'];assert fc['closed_mechanical']==json.loads(P.encode(mechanical['closed_provenance']).decode()) and fc['right_preconditioner_factor_resolved'] is True and fc['full_weak_or_global_inverse_qualified'] is False
 assert len(fc['completed_node_refs'])==3870 and len(fc['completed_chunk_refs'])==120
 factors=selected_record(fc['factors'],factor,frc);md=factors['metadata']
 assert md['kind']=='completed_signed_directed_active_nodal_numerical_factors' and md['active_node_count']==3870 and md['coefficient_dimension']==403340 and md['right_preconditioner_factor_resolved'] is True
 assert md['sheet_head_dimension']==6 and md['sheet_arm_dimension']==2 and md['interior_head_dimension']==9 and md['interior_arm_dimension']==3 and md['inactive_coordinates_are_zero_not_identity_padding'] is True
 assert md['nodal_apply_or_weak_functional_qualified'] is md['exact_weak_DD_or_global_inverse_qualified'] is md['physical_adoption'] is False
 application,aprc=closed_packet(APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF)
 assert application['case']['factor_terminal']==json.loads(json.dumps(dict(source=FACTOR_SOURCE,result=FACTOR_RESULT,receipt=FACTOR_RECEIPT,proof=FACTOR_PROOF))) and application['case']['factor_record']==thin(factors)
 assert application['roles']==len(application['checkpoints'])==22 and len(application['controls'])==22
 assert application['uniform_DD_or_global_inverse_qualified'] is application['original_six_residual_gates_tested'] is application['old_componentwise_inverse_failure_repaired'] is False
 return dict(anchor=anchor,input=inp,canonical=canonical,mechanical=mechanical,factors=factors,application=application,closed_provenance=dict(anchor=(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF),mechanical=mechanical['closed_provenance'],factor=(FACTOR_SOURCE,FACTOR_RESULT,FACTOR_RECEIPT,FACTOR_PROOF),application=(APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF)))

def seal(role,metadata):
 q=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,context=dict(CONTEXT)));clear_current();return q

def isolate(role,fn,metadata):
 outer=dict(AVAILABLE);context=dict(CONTEXT);clear_current();CONTEXT.update(context,operation_role=role)
 try:
  value=fn();q=seal(role,metadata)
 except BaseException:
  for n,a in outer.items():AVAILABLE['retained_outer_'+n]=a
  raise
 AVAILABLE.update(outer);CONTEXT.update(context);return value,q

def hydrate_blocks(admitted,basis):
 caches=[];refs=[];prefix=POINT_CACHE_PREFIX
 for iq,ref in enumerate(admitted['caches']):
  data=read(ref,candidate_point_cache_names(ref['metadata']));RAW.clear()
  for n,a in data.items():keep('copied_cache%d_'%iq+n,a)
  pair=lambda n:tuple(data[prefix+n+'_'+w].copy() for w in ('hi','lo'));ep=prefix+'copied_positive_coefficient_'
  cache=dict(s={n:data[prefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:data[prefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a.copy() for n,a in data.items() if n.startswith(ep)},constants=ref['metadata']['constants'],candidate_provenance=ref['metadata']['candidate_provenance'],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
  assert all(cache['constants'][n]==getattr(P,n) for n in ('ALPHA','ELL','C')) and cache['c']['N'].shape==(3784,) and cache['s']['z'].shape==(32,3784,4)
  caches.append(cache);refs.append(thin(seal('CACHE_COPY',dict(kind='copied_closed147_full_cache_and_original_primary_E0_time_contacts',column=iq,source=thin(ref),physical_adoption=False))))
 return dict(columns=caches,basis={n:basis[n] for n in ('R','dv','hats')},all_four_actual_columns_required=True,global_inverse_earned=False,physical_adoption=False),refs

def response_packet(refs):
 data=read(refs['input'],tuple(refs['input']['metadata']['schema']));RAW.clear()
 for n,a in data.items():keep('copied_anchor_input_'+n,a)
 basis={n:data['original_basis_'+n].copy() for n in ('R','dv','hats')};actual=read(refs['mechanical']['input'],tuple('registered_basis_'+n for n in ('R','dv','hats')));RAW.clear()
 for n in basis:keep('copied_mechanical_basis_'+n,actual['registered_basis_'+n]);assert np.array_equal(basis[n],actual['registered_basis_'+n])
 canonical=read(refs['canonical'],tuple(refs['canonical']['metadata']['schema']));RAW.clear()
 for n,a in canonical.items():keep('copied_anchor_canonical_'+n,a)
 prefix='NEW_reference_anchor';rhs=tuple(canonical[prefix+'_packed_target_minus_current_RHS_'+w].copy() for w in ('hi','lo'));native_ref=P.unpack_fields(data['original_reference_original_rhs'],False)[0];canonical_ref=data['original_reference_current_Pn'];scales=(data['original_reference_native_scale'],data['original_reference_metric_scale'])
 metric_pair=tuple(canonical[prefix+'_target_minus_current_epsilon_metric_'+w] for w in ('hi','lo'));metric_ref=metric_pair[0]+metric_pair[1];native_metric_gmres_put('NEW_metric_reference_norm_readout_defect',P.a_sub(metric_pair,P.a_dd(metric_ref)))
 start=P.a_dd(np.zeros(403340));zero_action=P.a_dd(np.zeros(403340));native_metric_gmres_put('NEW_mechanical_zero_correction_start',start);native_metric_gmres_put('NEW_exact_homogeneous_action_at_zero',zero_action);native_metric_gmres_put('NEW_original_target_minus_current_RHS',rhs)
 def scores(res,label):
  rows,norms,zero=trace_target_reference_scores(res,native_ref,canonical_ref,metric_ref,scales,label);fields=[P.unpack_fields(a,False) for a in res]
  for row,field in ((0,0),(1,0),(2,1)):
   if zero[row] and any(np.any(q[field]!=0) for q in fields):rows[row]=1.
  keep(label+'_both_word_exact_zero_reference_authoritative_scores',rows.copy());return rows
 initial=scores(rhs,'NEW_initial_original_six');assert np.array_equal(initial,np.asarray(refs['canonical']['metadata']['six_reference_scores']))
 inp=seal('INPUT',dict(kind='copied_closed_same_candidate_prepared_target_current_and_original_six_references',canonical=thin(refs['canonical']),anchor_input=thin(refs['input']),mechanical=refs['mechanical']['closed_provenance'],closed_provenance=refs['closed_provenance'],all_anchor_fields_bitcopied=True,exact_zero_linear_action_is_homogeneous147_proof=True,original_target_and_epsilon_unchanged=True,cap=CAP,physical_adoption=False))
 current=dict(action=zero_action,residual=rhs,scores=initial,admitted=bool(np.all(initial<=P.LINEAR_TOL)));blocks=None;cache_refs=[];factor_ref=None;new_actions=[];progress_refs=[]
 if not current['admitted']:
  blocks,cache_refs=hydrate_blocks(refs['mechanical'],basis);q=refs['factors'];names=tuple('assembled_'+n+'_'+w for n in ('D_inverse','S_inverse','B','E') for w in ('hi','lo'));fd=read(q,names);RAW.clear()
  factors={n:tuple(keep('copied_factor_'+n+'_'+w,fd['assembled_'+n+'_'+w]) for w in ('hi','lo')) for n in ('D_inverse','S_inverse','B','E')}
  factors.update(closed_provenance=dict(factor_record=thin(q),terminal=(FACTOR_SOURCE,FACTOR_RESULT,FACTOR_RECEIPT,FACTOR_PROOF)),all_active_factor_seals_verified=True,active_node_count=3870,right_preconditioner_factor_resolved=True,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
  prepared=prepare_candidate_directed_nodal_factor_apply(factors,keep,'NEW_closed_factor_coordinate_copy');factor_ref=thin(seal('FACTOR_COPY',dict(kind='copied_closed_resolved_nodal_numerical_factors_without_refactor',factors=thin(q),application=(APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF),physical_adoption=False)))
  def right(x,tag):return isolate('RIGHT_APPLY',lambda:candidate_directed_nodal_factor_apply(prepared,x,keep,tag),dict(kind='NEW_signed_directed_represented_factor_application',label=tag,input=thin(inp),factors=factor_ref,full_weak_inverse_qualified=False))[0]
  def action(x,tag):
   fields=[P.unpack_fields(a,False) for a in x];columns=[]
   def complete(iq,column):
    capture_families('completed_column_',column);q=seal('ACTION_COLUMN',dict(kind='NEW_same_candidate_fixed_configuration_temporal147_action_column',label=tag,column=iq,cache=cache_refs[iq],input=thin(inp),formal_primary_E0_time_gaps_retained=True,physical_adoption=False));columns.append(thin(q));return thin(q)
   def calculate():
    native_metric_gmres_put(tag+'_supplied_original_packed_direction',x);result=specialized_weak_mechanical_action(blocks,basis,tuple(q[0] for q in fields),tuple(q[1] for q in fields),keep,tag,complete);out=tuple(P.pack_fields(result['weak']['native'][w],result['weak']['metric'][w]) for w in (0,1));native_metric_gmres_put(tag+'_completed_original_weak_action',out);return out
   out,q=isolate('ACTION_WEAK',calculate,dict(kind='NEW_full_off_node_weak67_action',label=tag,input=thin(inp),new_columns=columns,current_or_target_replayed=False,physical_adoption=False));new_actions.append(thin(q));return out
  def positive(x,tag):return isolate('ACTION_POSITIVE',lambda:candidate_weak_mechanical_positive(blocks,basis,x,keep,tag),dict(kind='NEW_full147_original_lift_scatter_unsigned_outward_operation_envelope',label=tag,input=thin(inp),represented_factor_envelope_used_for_action=False,physical_adoption=False))[0]
  def progress(iteration,nodes,after,increment):
   for n,pair in (('nodes',nodes),('action',after['action']),('residual',after['residual']),('exact_increment',increment)):native_metric_gmres_put('mechanical_GMRES_completed_'+n,pair)
   keep('mechanical_GMRES_completed_original_six_scores',after['scores']);progress_refs.append(thin(seal('ITERATION',dict(kind='NEW_right_only_GMRES_candidate_all_original_six_rows',iteration=iteration,cap=CAP,admitted=after['admitted'],physical_adoption=False))))
  admission=dict(closed_provenance=refs['closed_provenance'],all_four_same_candidate_caches_authenticated=True,active_nodal_factors_admitted=True,original_six_reference_gates_unchanged=True,RHS_is_current_prepared_target_minus_current=True,all_off_node_weak_couplings_retained=True,physical_adoption=False,full_weak_inverse_qualified=False)
  nodes,after,increment,history=candidate_right_only_mechanical_gmres(start,current,rhs,right,action,positive,scores,admission,keep,'mechanical_GMRES',CAP,progress)
 else:nodes,after,increment,history=start,current,P.a_dd(np.zeros(403340)),dict(iterations=0,cap=CAP,restarts=0,reason='already_original_six_rows_admitted',original_six_rows_admitted=True,physical_adoption=False)
 final=scores(after['residual'],'NEW_final_original_six');assert np.array_equal(final,after['scores']);admitted=bool(np.all(final<=P.LINEAR_TOL))
 for n,pair in (('paired_correction',nodes),('original_action',after['action']),('original_residual',after['residual']),('original_RHS',rhs),('exact_increment',increment)):native_metric_gmres_put('NEW_final_'+n,pair)
 keep('NEW_final_original_six_scores',final);solution=seal('SOLUTION',dict(kind='NEW_same_candidate_right_only_mechanical_response_and_original_six_certificates',input=thin(inp),cache_copies=cache_refs,factor_copy=factor_ref,iterations=progress_refs,new_action_refs=new_actions,history=history,original_six_rows_admitted=admitted,canonical_epsilon_not_suppressed=True,updated_phase_and_York_geometry_contacts_are_separate=True,finite_state_normal_CMC_evolution_not_evaluated=True,physical_adoption=False))
 assert all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 return dict(status='CANDIDATE_RIGHT_ONLY_MECHANICAL_ORIGINAL_SIX_ROWS_ADMITTED' if admitted else 'CANDIDATE_RIGHT_ONLY_MECHANICAL_ORIGINAL_SIX_ROWS_NOT_ADMITTED',input=thin(inp),solution=thin(solution),closed_provenance=refs['closed_provenance'],original_six_scores=final.tolist(),history=history,cap=CAP,cycles=1,restarts=0,nominal_target_or_current_refitted=False,full_weak_inverse_qualified=False,new_finite_geometry_or_normal_CMC_or_physical_admission=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and CAP==80,'Root reviewed release required'
 assert all(x is not None for ref in (ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF,MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF,FACTOR_SOURCE,FACTOR_RESULT,FACTOR_RECEIPT,FACTOR_PROOF,APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF) for x in ref),'All natural closures/proofs required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  initialize_helpers();refs=response_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_provenance=refs['closed_provenance'],cap=CAP,cycles=1,restarts=0,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=response_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],case['original_six_scores'],rh);return 0 if case['status'].endswith('_ROWS_ADMITTED') else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_right_only_mechanical_response_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
