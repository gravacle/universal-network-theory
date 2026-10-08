"""HELD actual represented mechanical Astar lambda=eL response.
Only root binds future natural closures and executes the new namespace.
No saved producer/action/transpose contact/factor/control is replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_RIGHT_ONLY_MECHANICAL_ADJOINT_RESPONSE_V002'
DRIVER_PROTOCOL='CANDIDATE_RIGHT_ONLY_MECHANICAL_ADJOINT_RESPONSE_V001.md'
PROTOCOL_SHA='8e2fcafa2722c0aed693c169e8a7accd3d0e07d7be13ca0b44b0cd8e0c898133'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
LITERAL_SOURCE=(None,None)
LITERAL_RESULT=(None,None,'CANDIDATE_LITERAL_TEMPORAL_GRADIENT_BRIDGE_AND_DIRECTION_CONTACTS_PASS')
LITERAL_RECEIPT=(None,None,'CLOSED')
LITERAL_PROOF=(None,None,None)
TRANSPOSE_SOURCE=(None,None)
TRANSPOSE_RESULT=(None,None,'NEW_FULLWEAK_COEFFICIENT_TRANSPOSE_DIRECTION_CONTACTS_PASS')
TRANSPOSE_RECEIPT=(None,None,'CLOSED')
TRANSPOSE_PROOF=(None,None,None)
NODAL_SOURCE=('cross_u_candidate_directed_nodal_preconditioner_preparation_v005.py', '41d6b4b3d200c8e017759ee3f95e05addaf3d7ea59b53a61f0fcc12b3f514659')
NODAL_RESULT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RESULT.json', '20ddbdfe237cf5062440971f59b838046962994ad9517d3851d400e3e3b8a811', 'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
NODAL_RECEIPT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RECEIPT.json', '46221584fefc9a1ee67cfe62cdf6b27d4710964f60b4ad7865ed6e48e0cdd57b', 'CLOSED')
NODAL_PROOF=('ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_V001.json', '915f5cb58d42291166940df770359ab4416ef153c47dba9b43c680dbc6a6b7af', 'ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_VERIFIED')
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py', '489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json', '49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e', 'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json', 'c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64', 'CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json', '2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9', 'ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
APPLY_SOURCE=('candidate_directed_nodal_factor_apply_recovery_v002.py','3ef8c8fa9268021b5d6c96d4a4f87e95e6cbc9b37dd5e5af33bd868a91d9aca5')
APPLY_RESULT=('CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_RECOVERY_V002_RESULT.json','ad8efa717b6d3c7890fdc17dad48846af21627cd4b93d8f9d9a9364fd7098006','DIRECTED_NODAL_REPRESENTED_FACTOR_ADJOINT_AND_NEW_WEAK_CONTACTS_PASS')
APPLY_RECEIPT=('CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_RECOVERY_V002_RECEIPT.json','baa37120a40c140722adab059cbef0f70c6ac92a66344ba0673b0c686ffb09ed','CLOSED')
APPLY_PROOF=('ROOT_NATURAL_CLOSED_FACTOR_APPLY_RECOVERY_SUCCESS_SEALS_V001.json','3839f419ebaa070e107174bd2212c1325c3a646a91429314caba0b01faa4ee2c','ROOT_NATURAL_CLOSED_FACTOR_APPLY_RECOVERY_SUCCESS_SEALS_VERIFIED')
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_directed_nodal_factor_apply_v001.py': '4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b', 'author_fragment_native_metric_star_paired_gmres_v001.py': '3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770', 'author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py': '25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235'}
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
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_node_update'}
 primitive={'a_matvec','a_transpose','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','pack_fields','unpack_fields','pack_dd'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
  for n in names:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|{'B','GC','C','ALPHA','ELL'}})
 for n in ('B','GC','C','ALPHA','ELL'):setattr(P,n,SCOPE[n])
 P.LINEAR_TOL=1e-10
 choices=(('author_fragment_candidate_directed_nodal_factor_apply_v001.py',None),('author_fragment_native_metric_star_paired_gmres_v001.py',{'native_metric_gmres_put','native_metric_gmres_tree','native_metric_gmres_dot','native_metric_gmres_expansion','native_metric_gmres_norm','native_metric_gmres_upper','native_metric_gmres_candidate','native_metric_gmres_solve'}),('author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py',None),('author_fragment_candidate_weak_mechanical_positive_v001.py',{'mp_out','mp_add','mp_mul','mp_div','mp_sum','mp_mm','mp_mv'}),('author_fragment_candidate_fullweak_transpose_stationarity_v003.py',{'ct_pair','ct_matvec','candidate_original_scatter_transpose','candidate_paired_arrowhead_transpose','candidate_original_evaluation_transpose','candidate_measured_coefficient_fullweak_transpose','candidate_fullweak_coefficient_positive'}),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_provider_admission','candidate_point_cache_names'}),('cross_u_candidate_literal_phase_charge_response_v002.py',{'bind_record'}),('author_fragment_exact_exponent_two_product_v003.py',None))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_candidate_chunk_point_block_provider_v001.py'
 for n in ast.parse((BASE/file).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('POINT_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False,MECHANICAL_ADJOINT_AUTHOR_DRAFT=False,MECHANICAL_ADJOINT_AUTHORING_IN_PROGRESS=False)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_adjoint_exact_exponent_product')


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
 q=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,context=dict(CONTEXT)));clear_current();return q

def isolate(role,fn,metadata):
 outer=dict(AVAILABLE);context=dict(CONTEXT);clear_current();CONTEXT.update(context,operation_role=role)
 try:
  value=fn();q=seal(role,metadata)
 except BaseException:
  for n,a in outer.items():AVAILABLE['retained_outer_'+n]=a
  raise
 AVAILABLE.update(outer);CONTEXT.update(context);return value,q

def transpose_admission():
 mechanical=candidate_point_provider_admission(bind);r,rc=closed_packet(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF);case=r['case']
 assert case['closed_mechanical']==json.loads(P.encode(mechanical['closed_provenance']).decode())
 assert case['right_preconditioner_factor_resolved'] is True and case['full_weak_or_global_inverse_qualified'] is case['physical_adoption'] is False
 assert len(case['completed_chunk_refs'])==120 and len(case['completed_node_refs'])==3870
 inp=selected_record(case['input'],r,rc);bprov=inp['metadata']['basis_provenance'];assert inp['metadata']['closed_mechanical']==case['closed_mechanical'] and inp['metadata']['original_input']==thin(mechanical['input']) and inp['metadata']['original_basis']==thin(mechanical['original_basis'])
 chunks=[]
 for serial,ref in enumerate(case['completed_chunk_refs']):
  record=selected_record(ref,r,rc);md=record['metadata'];iq=serial//30;lo=(serial%30)*128;hi=min(lo+128,3784);prefix='NEW_directed_nodal_q%d_chunk%03d_point_'%(iq,serial)
  assert md['kind']=='completed_directed_nodal_moment_chunk_patch' and md['chunk']==serial and md['next_chunk']==serial+1 and md['column']==iq and md['selection']==[lo,hi] and md['chunk_size']==128 and md['basis_provenance']==bprov
  point=selected_record(md['committed_point_chunk'],r,rc);pm=point['metadata'];cp=mechanical['caches'][iq]['metadata']['candidate_provenance']
  assert pm['closed_candidate_provenance']==cp and pm['source']['column']==iq and pm['source']['selection']==[lo,hi] and pm['source']['closed_mechanical']==case['closed_mechanical']
  assert len(md['completed_source_contacts'])==3 and all(q['passed'] is True and q['tolerance']==2e-11 for q in md['completed_source_contacts'])
  p=hi-lo;shapes=dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3))
  names={}
  for n,shape in shapes.items():
   names[n]=tuple(prefix+'paired_raw_'+n+'_'+w for w in ('hi','lo'));names['e'+n]=prefix+'e'+n
   for key in names[n]+(names['e'+n],):assert md['schema'][key]==dict(shape=list(shape),dtype='float64',finite=True),key
  chunks.append(dict(column=iq,lo=lo,hi=hi,point_block_ref=thin(record),same_candidate_provenance=cp,basis_provenance=bprov,selected_names=names,committed_original_point=thin(point)))
 closed=dict(source=NODAL_SOURCE,result=NODAL_RESULT,receipt=NODAL_RECEIPT,proof=NODAL_PROOF,naturally_closed=True,natural_exit_code=0,all_selected_seals_verified=True,physical_adoption=False,same_candidate_provenance=[q['metadata']['candidate_provenance'] for q in mechanical['caches']])
 return dict(mechanical=mechanical,input=inp,chunks=chunks,closed=closed,basis_provenance=bprov)

def read_point_coefficients(descriptor,names):
 assert set(names) in ({'H','B','E','D'},{'H','B','E','D','eH','eB','eE','eD'})
 selected=tuple(key for n in ('H','B','E','D') for key in descriptor['selected_names'][n])+tuple(descriptor['selected_names']['e'+n] for n in ('H','B','E','D'))
 data=read(P.resolve_record(descriptor['point_block_ref']),selected);RAW.clear();pairs={};bounds={}
 for n in ('H','B','E','D'):
  pairs[n]=tuple(keep('loaded_point_'+n+'_'+w,data[key]) for w,key in zip(('hi','lo'),descriptor['selected_names'][n]));bounds[n]=keep('loaded_padded_point_e'+n,data[descriptor['selected_names']['e'+n]])
 return dict(record=descriptor['point_block_ref'],source_provenance=descriptor['same_candidate_provenance'],paired_raw=pairs,operation_envelopes=bounds)

def adjoint_admission():
 refs=transpose_admission();nodal,nrc=closed_packet(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF);factors=selected_record(nodal['case']['factors'],nodal,nrc)
 app,aprc=closed_packet(APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF);apr=json.loads(P.path(APPLY_PROOF[0]).read_text())
 assert app['case']['factor_record']==thin(factors) and app['case']['factor_terminal']==json.loads(json.dumps(dict(source=NODAL_SOURCE,result=NODAL_RESULT,receipt=NODAL_RECEIPT,proof=NODAL_PROOF)))
 assert len(app['checkpoints'])==len(app['controls'])==22 and apr['all_inherited_success_role_seals_verified'] is True and apr['inherited_controls']==18 and apr['new_controls']==4
 assert apr['uniform_DD_or_global_inverse_qualified'] is apr['old_componentwise_inverse_failure_repaired'] is apr['physical_adoption'] is False
 trans,trc=closed_packet(TRANSPOSE_SOURCE,TRANSPOSE_RESULT,TRANSPOSE_RECEIPT,TRANSPOSE_PROOF);tp=json.loads(P.path(TRANSPOSE_PROOF[0]).read_text());tc=trans['case']
 assert tp['all_inherited_success_role_seals_verified'] is True and tc['roles']==len(trans['checkpoints'])==267 and tc['current_roles']==len(trans['current_checkpoints'])==268
 assert tc['inherited_original_roles']==7 and tc['new_original_roles']==260 and tc['auxiliary_inherited_copy_roles']==8 and tc['original_failure_preserved'] is True and tc['uniform_DD_adjoint_or_global_inverse_qualified'] is False
 assert tc['closed_nodal']==json.loads(json.dumps(refs['closed'])) and len(tc['cases'])==2 and [q['name'] for q in trans['controls']]==['NEW_fullweak_transpose_case%d_pairing'%i for i in (0,1)]
 parent_input=bind_record(tc['input']);parent_prepared=bind_record(tc['prepared']);assert parent_input in trans['checkpoints'] and parent_prepared in trans['checkpoints']
 assert parent_input['metadata']['nodal_input']==thin(refs['input']) and parent_input['metadata']['mechanical']==json.loads(json.dumps(refs['mechanical']['closed_provenance'])) and parent_input['metadata']['point_descriptors']==json.loads(json.dumps(refs['chunks']))
 assert parent_prepared['metadata']['input']==thin(parent_input) and parent_prepared['metadata']['closed_nodal']==json.loads(json.dumps(refs['closed']))
 literal,lrc=closed_packet(LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF);lc=literal['case'];assert lc['roles']==len(literal['checkpoints'])==23 and lc['new_controls']==len(literal['controls'])==26 and lc['physical_adoption'] is False
 lin=selected_record(lc['input'],literal,lrc);bridge=selected_record(lc['stationarity_bridge'],literal,lrc);copy=selected_record(lc['canonical_copy'],literal,lrc);weak=selected_record(lc['literal_weak'],literal,lrc)
 assert lin['metadata']['mechanical']==json.loads(json.dumps(refs['mechanical']['closed_provenance'])) and bridge['metadata']['canonical']==thin(copy) and bridge['metadata']['literal']==thin(weak)
 assert bridge['metadata']['eL_sign']=='epsilon minus (literal minus registered)' and bridge['metadata']['stationarity_or_feedback_zero_assumed'] is False
 terminal=[tuple(q) for q in lc['anchor_terminal']];anchor,arc=closed_packet(*terminal);canonical=selected_record(anchor['case']['canonical'],anchor,arc);anchor_input=selected_record(anchor['case']['input'],anchor,arc)
 assert copy['metadata']['canonical']==thin(canonical) and anchor['case']['original_basis']==thin(refs['mechanical']['original_basis']) and anchor['case']['prepared_metric_target_is_exact_owned_reference'] is True
 assert canonical['metadata']['mechanical_current_unchanged_under_phase_update'] is True and canonical['metadata']['input']==thin(anchor_input)
 refs.update(factors=factors,literal=literal,bridge=bridge,literal_weak=weak,canonical_copy=copy,anchor_input=anchor_input,transpose=trans,closed_provenance=dict(literal=(LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF),transpose=(TRANSPOSE_SOURCE,TRANSPOSE_RESULT,TRANSPOSE_RECEIPT,TRANSPOSE_PROOF),factor=(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF),application=(APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF),anchor=terminal,mechanical=refs['mechanical']['closed_provenance']))
 return refs


def adjoint_packet(refs):
 ad=read(refs['anchor_input'],tuple('original_basis_'+n for n in ('R','dv','hats'))+('original_reference_native_scale','original_reference_metric_scale'));RAW.clear()
 for n,a in ad.items():keep('copied_anchor_'+n,a)
 basis={n:ad['original_basis_'+n].copy() for n in ('R','dv','hats')};bd=read(refs['input'],tuple('original_registered_basis_'+n for n in basis));RAW.clear()
 for n,a in basis.items():keep('copied_nodal_'+n,bd['original_registered_basis_'+n]);assert np.array_equal(a,bd['original_registered_basis_'+n])
 data=read(refs['bridge'],tuple(refs['bridge']['metadata']['schema']));RAW.clear()
 for n,a in data.items():keep('copied_stationarity_bridge_'+n,a)
 pair=lambda name:tuple(data['NEW_literal_stationarity_eL_'+name+'_'+w].copy() for w in ('hi','lo'))
 rhs=P.pack_dd(pair('native'),pair('metric'));native_metric_gmres_put('NEW_adjoint_packed_eL_RHS',rhs)
 cd=read(refs['canonical_copy'],tuple(refs['canonical_copy']['metadata']['schema']));RAW.clear()
 for n,a in cd.items():keep('copied_canonical_reference_'+n,a)
 scale=P.pack_fields(ad['original_reference_native_scale'],ad['original_reference_metric_scale']);reference=mechanical_adjoint_reference(rhs,scale,keep,'NEW_adjoint_source_reference')
 inp=thin(seal('INPUT',dict(kind='copied_NEW_literal_stationarity_eL_and_fixed_coordinate_scaling',bridge=thin(refs['bridge']),canonical=thin(refs['canonical_copy']),anchor_input=thin(refs['anchor_input']),closed_provenance=refs['closed_provenance'],RHS_sign='epsilon minus literal-minus-registered',score_groups=['native','metric','packed'],score_columns=['raw','divided_by_saved_coordinate_scale'],original_forward_physical_six_gates_tested=False,zero_source_relative_ratio_undefined=True,physical_adoption=False)))
 prepared=dict(chunks=list(refs['chunks']),basis=basis,closed=refs['closed'],physical_adoption=False,coefficient_transpose_only=True,authoritative147_association_measured=False,global_inverse_qualified=False)
 initial=mechanical_adjoint_scores(rhs,reference,keep,'NEW_adjoint_initial');keep('NEW_adjoint_initial_scores',initial)
 factors=None;factor_copy=None;actions=[];positives=[];right_refs=[];iteration_refs=[]
 if not np.all(initial<=P.LINEAR_TOL):
  names=tuple('assembled_'+n+'_'+w for n in ('D_inverse','S_inverse','B','E') for w in ('hi','lo'));fd=read(refs['factors'],names);RAW.clear()
  factors={n:tuple(keep('copied_factor_'+n+'_'+w,fd['assembled_'+n+'_'+w]) for w in ('hi','lo')) for n in ('D_inverse','S_inverse','B','E')}
  factors.update(closed_provenance=dict(factor_record=thin(refs['factors']),terminal=(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)),all_active_factor_seals_verified=True,active_node_count=3870,right_preconditioner_factor_resolved=True,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
  nodal=prepare_candidate_directed_nodal_factor_apply(factors,keep,'NEW_adjoint_closed_factor_copy');factor_copy=thin(seal('FACTOR_COPY',dict(kind='copied_resolved_directed_signed_factor_for_NEW_adjoint_right_map',source=thin(refs['factors']),controls=(APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF),physical_adoption=False)))
 def right(x,tag):
  assert factors is not None
  out,q=isolate('RIGHT_ADJOINT',lambda:candidate_directed_nodal_factor_adjoint(nodal,x,keep,tag),dict(kind='NEW_nodal110_signed_factor_adjoint_application',label=tag,input=inp,factor=factor_copy,physical_adoption=False));right_refs.append(thin(q));return out
 def action(x,tag):
  chunks=[]
  def completed(descriptor,part):
   ct_pair(tag+'_completed_chunk_native',part[0],keep);ct_pair(tag+'_completed_chunk_metric',part[1],keep)
   q=seal('ADJOINT_CHUNK',dict(kind='NEW_directed_Kstar_application_to_NEW_GMRES_dual',label=tag,column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],source=descriptor['point_block_ref'],input=inp,physical_adoption=False));chunks.append(thin(q));return thin(q)
  def calculate():
   native_metric_gmres_put(tag+'_supplied_NEW_dual',x);out=candidate_measured_coefficient_fullweak_transpose(prepared,x,read_point_coefficients,keep,tag,completed);native_metric_gmres_put(tag+'_completed_Astar',out['packed']);return out['packed']
  out,q=isolate('ADJOINT_WEAK',calculate,dict(kind='NEW_original244_coefficient_Astar_fullweak',label=tag,input=inp,chunks=chunks,old_pairing_or_action_replayed=False,physical_adoption=False));actions.append(thin(q));return out
 def positive(x,tag):
  chunks=[];pending=[]
  def reader(descriptor,names):
   if pending:
    previous=pending.pop();q=seal('POSITIVE_CHUNK',dict(kind='completed_NEW124_outward_Kstar_positive_partial',label=tag,column=previous['column'],selection=[previous['lo'],previous['hi']],source=previous['point_block_ref'],input=inp,physical_adoption=False));chunks.append(thin(q))
   data=read_point_coefficients(descriptor,names);pending.append(descriptor);return data
  def calculate():
   native_metric_gmres_put(tag+'_supplied_NEW_dual',x);return candidate_fullweak_coefficient_positive(prepared,x,reader,keep,tag)
  out,q=isolate('ADJOINT_POSITIVE',calculate,dict(kind='NEW_separate124_outward244_source_coefficient_transpose_bound',label=tag,input=inp,completed_chunk_partials=chunks,last_chunk_and_full_Estar_retained_here=True,nodal_factor_bound_substituted=False,physical_adoption=False));positives.append(thin(q));return out
 def scores(x,tag):return mechanical_adjoint_scores(x,reference,keep,tag)
 def progress(iteration,nodes,after,increment):
  for n,pair in (('lambda',nodes),('Astar',after['action']),('residual',after['residual']),('exact_increment',increment)):native_metric_gmres_put('NEW_adjoint_completed_'+n,pair)
  keep('NEW_adjoint_completed_source_relative_scores',after['scores']);iteration_refs.append(thin(seal('ITERATION',dict(kind='NEW_right_only_adjoint_candidate_original_eL_relative_certificate',iteration=iteration,cap=CAP,admitted=after['admitted'],physical_adoption=False))))
 admission=dict(closed_provenance=refs['closed_provenance'],same_updated_candidate_and_original_coordinates=True,two_selected_fullweak_transpose_contacts_passed=True,literal_eL_both_words_copied=True,active_signed_nodal_factor_and_adjoint_controls_passed=True,source_relative_adjoint_certificates_declared=True,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False)
 nodes,after,increment,history=candidate_right_only_mechanical_adjoint_gmres(rhs,right,action,positive,scores,admission,keep,'mechanical_adjoint_GMRES',CAP,progress)
 final=scores(after['residual'],'NEW_adjoint_final');assert np.array_equal(final,after['scores']);admitted=bool(np.all(final<=P.LINEAR_TOL))
 native_metric_gmres_put('NEW_final_Astar_minus_eL',P.a_mul64(-1.,after['residual']))
 for n,pair in (('lambda',nodes),('Astar',after['action']),('eL_RHS',rhs),('eL_minus_Astar',after['residual']),('exact_increment',increment)):native_metric_gmres_put('NEW_final_'+n,pair)
 keep('NEW_final_adjoint_source_relative_scores',final)
 solution=thin(seal('SOLUTION',dict(kind='NEW_represented_mechanical_Astar_lambda_eL_response',input=inp,factor_copy=factor_copy,right_applications=right_refs,new_action_refs=actions,new_positive_refs=positives,iterations=iteration_refs,history=history,source_relative_adjoint_rows_admitted=admitted,original_forward_canonical_or_physical_gates_tested=False,phase_mass_or_gauge_feedback_evaluated=False,physical_adoption=False)))
 assert all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 return dict(status='CANDIDATE_MECHANICAL_ADJOINT_NEW_SOURCE_ROWS_ADMITTED' if admitted else 'CANDIDATE_MECHANICAL_ADJOINT_NEW_SOURCE_ROWS_NOT_ADMITTED',input=inp,solution=solution,closed_provenance=refs['closed_provenance'],source_relative_scores=final.tolist(),history=history,cap=CAP,cycles=1,restarts=0,warm_start=False,represented_coefficient_transpose_only=True,uniform_adjoint_or_global_inverse_qualified=False,original_forward_physical_six_gates_tested=False,phase_M_or_gauge_Cstar_feedback_evaluated=False,physical_adoption=False)


def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and CAP==80,'Root reviewed release required'
 assert all(x is not None for ref in (LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF,TRANSPOSE_SOURCE,TRANSPOSE_RESULT,TRANSPOSE_RECEIPT,TRANSPOSE_PROOF,NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF,MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF,APPLY_SOURCE,APPLY_RESULT,APPLY_RECEIPT,APPLY_PROOF) for x in ref),'All natural closures/proofs required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  initialize_helpers();refs=adjoint_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_provenance=refs['closed_provenance'],cap=CAP,cycles=1,restarts=0,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=adjoint_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],case['source_relative_scores'],rh);return 0 if case['status'].endswith('_ROWS_ADMITTED') else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_right_only_mechanical_adjoint_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
