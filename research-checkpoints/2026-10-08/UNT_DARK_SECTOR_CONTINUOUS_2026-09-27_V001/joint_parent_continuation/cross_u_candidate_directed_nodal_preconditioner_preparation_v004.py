"""HELD all-grid directed numerical point/moment/active-factor preparation.
Root alone releases after natural mechanical-cache closure and full review.
Only NEW133 point blocks,198 moments and active factors; no weak action or solve.
Completed chunks/nodes are sealed before the next unit. Old physics is not replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V004'
DRIVER_PROTOCOL='CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V004.md'
PROTOCOL_SHA='9847b15256590f8eec8be71f338363f848d7a194eb7539341d589a3ce1b7ef0a'
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py', '489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json', '49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e', 'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json', 'c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64', 'CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json', '2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9', 'ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
POINT_PENDING_SOURCE=(None,None)
POINT_PENDING_ERROR=(None,None,'FAILED')
POINT_PENDING_RECEIPT=(None,None,'CLOSED_ERROR')
POINT_PENDING_CLOSURE_PROOF=(None,None,'ROOT_NATURAL_CLOSED_NODAL_POINT_ENVELOPE_PARTIAL_SEALS_VERIFIED')
USE_SAVED_CARRY=False
SAVED_CARRY_PROOF=(None,None,'ROOT_NATURAL_CLOSED_NODAL_PREPARATION_PARTIAL_SEALS_VERIFIED')
EQUILIBRATE=False
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py':'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db',
 'author_fragment_candidate_modal_head_point_reconstruction_v001.py':'a49fce7da61d67c514b3cbd3a4b247a0fa17c3a417a0577b26571e3e6daf9827',
 'author_fragment_candidate_chunk_point_block_provider_v001.py':'4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625',
 'author_fragment_candidate_directed_nodal_arrowhead_v001.py':'0a05eacd67d3093e2328c7197cdfb257488771ec7e0078b77a972340ef662bb6',
 'author_fragment_candidate_pending_point_envelope_recovery_v002.py':'295c31c6181dcab21bfee62b55324f56a4fc01cfd8c2e4feb40424b4a957948d',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d'}
COMPONENT_PROTOCOLS={
 'CANDIDATE_CHUNK_POINT_BLOCK_PROVIDER_V001.md':'2a17d53795254add6c0005bd7c8598f2b6854fdc7bfc9b9edca6b2e8e5dcdd61',
 'CANDIDATE_DIRECTED_NODAL_ARROWHEAD_V001.txt':'d6f1ce10e9cc70488588793178c31556b6eb8ce7c641d7d73ffeb9bfefa651da',
 'CANDIDATE_PENDING_POINT_ENVELOPE_RECOVERY_V002.md':'b5efb3b600685da4076e35a7efb8246a321773a3952391a6fe66ced75b4bdc00'}
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
MOMENT_SHAPES=dict(H=(3870,9,9),B=(32,3870,9,3),E=(32,3870,3,9),D=(32,3870,3,3))

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for name,h in PINS.items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h,name
 tree=ast.parse((BASE/IO_PARENT).read_text());names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==10
 exec(compile(ast.Module(body=defs,type_ignores=[]),IO_PARENT,'exec'),globals());initialize_io()
 file=list(PINS)[-1];tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==1 and defs[0].name=='recheck'
 exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']

def preparation_keep(name,a):
 CONTEXT['last_operand']=name
 return keep(name,a)

def clear_completed():
 context=dict(CONTEXT);clear_current();CONTEXT.update(context)

def initialize_helpers():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=preparation_keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 files=list(PINS);trees=[ast.parse((BASE/n).read_text()) for n in files[:2]]
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter','scalar_mask','pack_fields','unpack_fields'}
 defs=[n for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in primitive];assert len(defs)==33
 exec(compile(ast.Module(body=defs,type_ignores=[]),files[1],'exec'),SCOPE)
 for n in base|primitive|{'B','GC','C','ALPHA','ELL'}:setattr(P,n,SCOPE[n]);globals()[n]=SCOPE[n]
 compact={'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}
 for file,count,selected in ((files[2],11,None),(files[3],6,compact),(files[4],2,None),(files[5],6,None),(files[6],3,None),(files[7],5,None),(files[8],7,None),(files[9],9,None),(files[10],2,None)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (selected is None or n.name in selected)];assert len(defs)==count,file
  if file==files[8]:
   for n in tree.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('POINT_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 globals()['POINT_PROVIDER_AUTHOR_DRAFT']=False;globals()['POINT_RECOVERY_AUTHOR_DRAFT']=False;globals()['POINT_RECOVERY_AUTHORING_IN_PROGRESS']=False
 install_exact_exponent_product(SCOPE,P,preparation_keep,'NEW_nodal_preparation_exact_exponent_product');globals()['a_prod']=P.a_prod

def read_closed(ref,names):
 data=read(ref,names);RAW.clear()
 return data

def seal_completed(role,metadata):
 CONTEXT.update(stage='seal_'+role,role=role)
 record=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,controls=list(CHECKS[CONTEXT.get('unit_control_start',0):])))
 CONTEXT.update(last_completed_role=thin(record),last_completed_role_kind=role,unit_control_start=len(CHECKS))
 return record

def describe(name,value):
 P.json_file(STEM+'_DESCRIPTION_%05d_%s.json'%(len(RECORDS),name),dict(owner=SCOPE['OWNER'],value=value))

def bind_saved_role(ref,owner,receipt):
 bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);record=P.resolve_record(ref)
 assert record['metadata']['owner']==owner and record['metadata']['failed'] is False and record['metadata']['qualification']==FLAGS
 assert receipt['output_sha256'][ref['file']]==ref['sha256'] and receipt['output_sha256'][ref['commit_file']]==ref['commit_sha256']
 return record

def restore_saved_carries(basis_provenance,closed_mechanical):
 if not USE_SAVED_CARRY:return None,None,None
 assert all(x is not None for x in SAVED_CARRY_PROOF);bind(SAVED_CARRY_PROOF[0],SAVED_CARRY_PROOF[1]);proof=json.loads(P.path(SAVED_CARRY_PROOF[0]).read_text())
 assert proof['status']==SAVED_CARRY_PROOF[2] and proof['naturally_closed'] is True and proof['exit_code']==1 and proof['all_input_seals_verified'] is True and proof['all_committed_role_seals_verified'] is True and proof['failed_raw_preserved'] is True
 assert proof['mechanical_source']==list(MECHANICAL_SOURCE) and proof['mechanical_result']==list(MECHANICAL_RESULT) and proof['closed_mechanical']==closed_mechanical and proof['basis_provenance']==basis_provenance and proof['equilibrated']==EQUILIBRATE
 assert proof['pending_unit_has_no_earned_numerical_substep'] is True,'Partial point directions or computed factor require selective recovery, never replay'
 source,error,receipt=proof['source'],proof['error'],proof['receipt']
 for ref in (source,error,receipt):bind(ref['file'],ref['sha256'])
 er=json.loads(P.path(error['file']).read_text());rc=json.loads(P.path(receipt['file']).read_text());owner=proof['owner']
 assert er['owner']==rc['owner']==owner and owner['source_sha256']==source['sha256'] and er['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==error['sha256']
 assert er['qualification']==rc['qualification']==FLAGS and er['raw_preservation_traceback'] is None and er['closing_traceback'] is None
 chunks=proof['completed_moment_chunks'];nodes=proof['completed_node_factors'];assert 0<=len(chunks)<=120 and 0<=len(nodes)<=3870 and (not nodes or len(chunks)==120)
 moments={n:np.zeros(s) for n,s in MOMENT_SHAPES.items()};bounds={n:np.zeros(s) for n,s in MOMENT_SHAPES.items()};chunk_refs=[];node_refs=[]
 for serial,ref in enumerate(chunks):
  record=bind_saved_role(ref,owner,rc);assert any(thin(r)==thin(record) for r in er['checkpoints']);md=record['metadata']
  assert md['kind']=='completed_directed_nodal_moment_chunk_patch' and md['chunk']==serial and md['next_chunk']==serial+1 and md['basis_provenance']==basis_provenance and md['chunk_size']==128
  names=('independent_node_ids',)+tuple('updated_'+prefix+n for n in MOMENT_SHAPES for prefix in ('','e'));data=read(record,names);ids=data['independent_node_ids'];assert ids.dtype==np.int64 and np.all((ids>=0)&(ids<3870)) and np.array_equal(ids,np.unique(ids))
  for n,s in MOMENT_SHAPES.items():
   key=ids if n=='H' else (slice(None),ids);a=data['updated_'+n];e=data['updated_e'+n];assert a.shape==e.shape==moments[n][key].shape and np.all(e>=0);moments[n][key]=a;bounds[n][key]=e
  chunk_refs.append(thin(record));clear_completed()
 moment_carry=dict(moments=moments,bounds=bounds,next_chunk=len(chunks),completed_chunk_refs=chunk_refs,chunk_size=128,basis_provenance=basis_provenance,closed_restore_provenance=proof)
 DI=np.zeros((32,3870,3,3));J=np.zeros((3870,9,9))
 for node,ref in enumerate(nodes):
  record=bind_saved_role(ref,owner,rc);assert any(thin(r)==thin(record) for r in er['checkpoints']);md=record['metadata'];assert md['kind']=='completed_directed_active_nodal_factor' and md['node']==node and md['next_node']==node+1 and md['completed_moment_refs']==chunk_refs and md['equilibrated']==EQUILIBRATE
  data=read(record,('active_arm','active_head','completed_D_inverse','completed_S_inverse'));ai=data['active_arm'];hi=data['active_head'];sheet=node%45==0
  assert np.array_equal(ai,np.array((0,2) if sheet else (0,1,2))) and np.array_equal(hi,np.array((0,2,3,4,5,8) if sheet else tuple(range(9))))
  assert data['completed_D_inverse'].shape==(32,len(ai),len(ai)) and data['completed_S_inverse'].shape==(len(hi),len(hi))
  for mode in range(32):DI[mode,node][np.ix_(ai,ai)]=data['completed_D_inverse'][mode]
  J[node][np.ix_(hi,hi)]=data['completed_S_inverse'];node_refs.append(thin(record));clear_completed()
 factor_carry=dict(D_inverse_raw=DI,S_inverse_raw=J,next_node=len(nodes),completed_node_refs=node_refs,completed_moment_refs=chunk_refs,equilibrated=EQUILIBRATE,closed_restore_provenance=proof) if nodes else None
 return moment_carry,factor_carry,dict(proof_file=SAVED_CARRY_PROOF[0],proof_sha256=SAVED_CARRY_PROOF[1],original_failure_preserved=True,inherited_controls=er['controls'],inherited_completed_chunk_refs=chunk_refs,inherited_completed_node_refs=node_refs)

def completed_moment_chunk(data):
 CONTEXT.update(stage='completed_nodal_moment_chunk',chunk=data['chunk'],next_chunk=data['next_chunk'],column=data['iq'],selection=[data['lo'],data['hi']])
 preparation_keep('independent_node_ids',data['node_ids'])
 for n,a in data['updated_node_blocks'].items():preparation_keep('updated_'+n,a)
 record=seal_completed('MOMENT_CHUNK',dict(kind='completed_directed_nodal_moment_chunk_patch',chunk=data['chunk'],next_chunk=data['next_chunk'],column=data['iq'],selection=[data['lo'],data['hi']],basis_provenance=data['basis_provenance'],chunk_size=data['chunk_size'],committed_point_chunk=data['committed_point_chunk'],completed_source_contacts=data['completed_point_blocks']['construction_contacts'],mode_specific_moments=True,original_paired_weak_action_authoritative=True,global_or_physical_qualified=False));clear_completed()
 return thin(record)

def completed_node_factor(data):
 CONTEXT.update(stage='completed_active_nodal_factor',node=data['node'],next_node=data['node']+1)
 for n in ('active_arm','active_head','H','B','E','D','S','D_inverse','S_inverse'):preparation_keep(('completed_'+n if n.endswith('inverse') else n),data[n])
 put_pair(AVAILABLE,'completed_S_pair',data['S_pair'])
 for family in ('D','S'):
  for n in ('balanced_inverse','row_exponents','column_exponents','two_sided_residual_upper','construction_cone_upper'):preparation_keep(family+'_certificate_'+n,data[family+'_certificate'][n])
 record=seal_completed('NODE_FACTOR',dict(kind='completed_directed_active_nodal_factor',node=data['node'],next_node=data['node']+1,sheet=data['sheet'],equilibrated=EQUILIBRATE,completed_moment_refs=data['completed_moment_refs'],physical_coordinate_inverse_maps_retained=True,real_coefficient_inverse_resolved=True,uniform_DD_or_componentwise_application_qualified=False,global_or_physical_qualified=False));clear_completed()
 return thin(record)

def preparation_packet(admitted):
 original=read(admitted['input'],tuple(admitted['input']['metadata']['schema']));basis={n:original['registered_basis_'+n].copy() for n in ('R','dv','hats','cell_i','cell_j','r','z')}
 assert basis['r'].shape==(87,) and basis['z'].shape==(45,) and np.all(np.isfinite(basis['r'])) and np.all(np.isfinite(basis['z']))
 closed_mechanical=json.loads(P.encode(admitted['closed_provenance']).decode());basis['closed_provenance']=dict(mechanical=closed_mechanical,original_basis=thin(admitted['original_basis']),copied_closed_input=thin(admitted['input']),fields=['registered_basis_'+n for n in ('R','dv','hats','cell_i','cell_j','r','z')])
 columns=[dict(closed_candidate_provenance=ref['metadata']['candidate_provenance']) for ref in admitted['caches']]
 for n,a in original.items():preparation_keep('closed_mechanical_INPUT_'+n,a)
 for n,a in basis.items():
  if isinstance(a,np.ndarray):preparation_keep('original_registered_basis_'+n,a)
 input_record=seal_completed('INPUT',dict(kind='copied_closed_candidate_mechanical_inputs_targets_and_original_basis',closed_mechanical=closed_mechanical,caches=[thin(r) for r in admitted['caches']],original_input=thin(admitted['input']),original_basis=thin(admitted['original_basis']),basis_provenance=basis['closed_provenance'],current_target_or_primitive_defect_recomputed=False,phase_supplied_separately=True,physical_adoption=False));clear_completed()
 moment_carry,factor_carry,inherited=restore_saved_carries(basis['closed_provenance'],closed_mechanical);start_chunks=0 if moment_carry is None else moment_carry['next_chunk'];start_nodes=0 if factor_carry is None else factor_carry['next_node']
 provider=prepare_candidate_point_block_provider(admitted,read_closed,seal_completed,clear_completed,describe,P.check)
 provider,pending_recovery=prepare_candidate_pending_point_recovery(admitted,provider,bind,read_closed,seal_completed,clear_completed,preparation_keep)
 moments=candidate_nodal_arrowhead_moments(columns,basis,provider,preparation_keep,completed_moment_chunk,'NEW_directed_nodal',chunk_size=128,carry=moment_carry)
 assert moments['next_chunk']==len(moments['completed_chunk_refs'])==120 and moments['full_all_four_sections'] is True and moments['mode_specific_moments'] is True
 for n in MOMENT_SHAPES:preparation_keep('assembled_'+n,moments['moments'][n]);preparation_keep('assembled_e'+n,moments['bounds'][n])
 moment_record=seal_completed('MOMENTS',dict(kind='completed_all_four_directed_real_nodal_self_moments',completed_chunk_refs=moments['completed_chunk_refs'],basis_provenance=basis['closed_provenance'],chunk_size=128,next_chunk=120,mode_specific_moments=True,aliased_forward_and_scatter_maps_combined_before_moments=True,authoritative_action='paired_specialized_weak67',full_weak_or_global_inverse_qualified=False,physical_adoption=False));clear_completed()
 factors=candidate_nodal_arrowhead_factors(moments,preparation_keep,completed_node_factor,'NEW_directed_active_factors',equilibrate=EQUILIBRATE,carry=factor_carry)
 assert factors['next_node']==len(factors['completed_node_refs'])==3870 and factors['right_preconditioner_factor_resolved'] is True and factors['nodal_apply_or_weak_functional_qualified'] is False
 for n in ('D_inverse_raw','S_inverse_raw'):preparation_keep('assembled_'+n,factors[n])
 for n in ('D_inverse','S_inverse','B','E'):put_pair(AVAILABLE,'assembled_'+n,factors[n])
 preparation_keep('original_native_mask',P.native_mask());preparation_keep('original_metric_mask',P.metric_mask())
 factor_record=seal_completed('FACTORS',dict(kind='completed_signed_directed_active_nodal_numerical_factors',moments=thin(moment_record),completed_node_refs=factors['completed_node_refs'],completed_moment_refs=factors['completed_moment_refs'],equilibrated=EQUILIBRATE,active_node_count=3870,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,coefficient_dimension=403340,inactive_coordinates_are_zero_not_identity_padding=True,right_preconditioner_factor_resolved=True,nodal_apply_or_weak_functional_qualified=False,exact_weak_DD_or_global_inverse_qualified=False,physical_adoption=False));clear_completed()
 new_chunks=120-start_chunks;new_nodes=3870-start_nodes;expected_roles=4+15*new_chunks+new_nodes-13;expected_controls=3*new_chunks+4*new_nodes-3
 preparation_keep('completed_chunk_and_node_counts',np.asarray([120,3870],dtype=np.int64));preparation_keep('new_chunk_and_node_counts',np.asarray([new_chunks,new_nodes],dtype=np.int64));preparation_keep('resolved_active_coordinate_count',np.asarray(403340,dtype=np.int64))
 preparation=seal_completed('PREPARATION',dict(kind='directed_nodal_numerical_preconditioner_preparation_only',input=thin(input_record),moments=thin(moment_record),factors=thin(factor_record),closed_mechanical=closed_mechanical,inherited_closed_partial=inherited,roles=expected_roles,new_controls=expected_controls,retained_original_TOL=2e-11,new_point_actions=12*new_chunks-12,pending_point_recovery=pending_recovery,inherited_point_actions=12,inherited_post_Pi_controls=3,old_producer_weak_action_fixture_or_solver_replayed=False,normwise_factor_resolution_does_not_upgrade_original_componentwise_apply_failure=True,right_preconditioner_factor_resolved=True,nodal_apply_or_weak_functional_qualified=False,full_weak_global_or_physical_qualified=False))
 assert len(RECORDS)==expected_roles and len(CHECKS)==expected_controls and all(q['passed'] for q in CHECKS)
 return dict(status='CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED',input=input_record,moments=moment_record,factors=factor_record,preparation=preparation,roles=expected_roles,new_controls=expected_controls,completed_chunk_refs=moments['completed_chunk_refs'],completed_node_refs=factors['completed_node_refs'],closed_mechanical=closed_mechanical,inherited_closed_partial=inherited,authoritative_action='paired_specialized_weak67',pending_point_recovery=pending_recovery,new_point_actions=12*new_chunks-12,inherited_point_actions=12,right_preconditioner_factor_resolved=True,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root release required'
 assert all(x is not None for ref in (MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF) for x in ref),'Naturally CLOSED mechanical cache and proof required before IO'
 assert isinstance(EQUILIBRATE,bool) and USE_SAVED_CARRY is False,'This successor restores only the earned first point chunk; later moment/factor recovery needs its own explicit admission'
 assert all(x is not None for ref in (POINT_PENDING_SOURCE,POINT_PENDING_ERROR,POINT_PENDING_RECEIPT,POINT_PENDING_CLOSURE_PROOF) for x in ref),'Closed earned point chunk proof required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(IO_PARENT,IO_PARENT_SHA)
  for name,h in tuple(PINS.items())+tuple(COMPONENT_PROTOCOLS.items())+((DRIVER_PROTOCOL,PROTOCOL_SHA),):bind(name,h)
  INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256'];initialize_helpers();admitted=candidate_point_provider_admission(bind)
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_mechanical=admitted['closed_provenance'],chunk_cap=128,all_four_sections_required=True,equilibrated=EQUILIBRATE,use_saved_carry=USE_SAVED_CARRY,io_recheck_successor=list(PINS)[-1],old_weak_action_or_solver_evaluated=False,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=preparation_packet(admitted)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_point_moment_or_active_factor_with_completed_reference_context',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
