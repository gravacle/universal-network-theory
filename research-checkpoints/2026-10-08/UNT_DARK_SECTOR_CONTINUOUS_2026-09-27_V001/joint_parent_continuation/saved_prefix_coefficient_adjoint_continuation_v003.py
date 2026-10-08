"""HELD compact represented coefficient Astar continuation from earned7 state."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='SAVED_PREFIX_COEFFICIENT_ADJOINT_CONTINUATION_V003'
DRIVER_PROTOCOL='SAVED_PREFIX_COEFFICIENT_ADJOINT_CONTINUATION_V001.md'
PROTOCOL_SHA='6624549270106da22a805b31a93086752c55b8af68d95e1d51b1b981a238ddca'
OLD_SOURCE=('cross_u_candidate_right_only_mechanical_adjoint_response_v003.py','720ab9f4bad4a39a1c44e93acb22a8c4dd5ead032598503bec93774c6cab969b')
SELECTED_PROOF=('READONLY_CLOSED_ADJOINT7_SELECTED_PREFIX_BYTE_SEALS_V001.json','457d33990eb54213e087515e96b6a9bd2f0bf1f11ce17449991898bd02c572b0','READONLY_CLOSED_ADJOINT7_SELECTED_PREFIX_BYTE_SEALS_VERIFIED')
NODAL_PROJECTION=('ROOT_CLOSED_NODAL120_BOUNDED_RESULT_PROJECTION_V001.json','f1ef9d6660125f8a1beef9fa42d1c3549d299d672341bbf5acfb49a00efa741c','ROOT_CLOSED_NODAL120_BOUNDED_RESULT_PROJECTION_VERIFIED')
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
VERIFIED_ARCHIVES={};SMALL_STATE={};POSITIVE_PENDING={};CURRENT_CANDIDATE=None;NEW_BASIS=[];NEW_STATES=[];NEW_ACTIONS=[]
ACTIVE_ARGUMENT={}
GMRES_LABEL='resumed_mechanical_adjoint_GMRES'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_directed_nodal_factor_apply_v001.py': '4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b', 'author_fragment_native_metric_star_paired_gmres_v001.py': '3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770', 'author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py': '25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_native_metric_star_paired_gmres_resume_v002.py': '73b15a0e0512295aed41389a80c20ec6cf50ddef634497c805ada69c8ed738ee', 'author_fragment_saved_adjoint7_coefficient_continuation_v001.py': 'b7d5b2028b71956292d042beb5a036c3c15f5b8acf2d425ea0d58337a82a250b'}
FLAGS={'physical_metric_qualified': False, 'canonical_currents_restored': False, 'normal_constraints_qualified': False, 'initial_CMC_solved': False, 'phase_charge_restored': False, 'CMC_preservation_qualified': False, 'exterior_qualified': False, 'evolution_qualified': False, 'galaxy_velocity_qualified': False}
NODAL_SOURCE=('cross_u_candidate_directed_nodal_preconditioner_preparation_v005.py', '41d6b4b3d200c8e017759ee3f95e05addaf3d7ea59b53a61f0fcc12b3f514659')
NODAL_RESULT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RESULT.json', '20ddbdfe237cf5062440971f59b838046962994ad9517d3851d400e3e3b8a811', 'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
NODAL_RECEIPT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RECEIPT.json', '46221584fefc9a1ee67cfe62cdf6b27d4710964f60b4ad7865ed6e48e0cdd57b', 'CLOSED')
NODAL_PROOF=('ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_V001.json', '915f5cb58d42291166940df770359ab4416ef153c47dba9b43c680dbc6a6b7af', 'ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_VERIFIED')

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

def bounded_keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a
 if name.startswith(GMRES_LABEL):
  for key in ('H_hi','H_lo','R','Givens_cos','Givens_sin','rotated_RHS','history','all_Arnoldi_contact_norms','all_Arnoldi_operation_bounds'):
   if name.endswith('_'+key):SMALL_STATE[key]=a.copy()
 if CONTEXT.get('stage')=='positive' and name.endswith(('_Kstar_native_partial','_Kstar_metric_partial')):
  iq=CONTEXT['column'];lo,hi=CONTEXT['selection'];sl=slice(iq*3784+lo,iq*3784+hi)
  POSITIVE_PENDING['native' if name.endswith('_Kstar_native_partial') else 'metric']=a[:,sl].copy() if name.endswith('_Kstar_native_partial') else a[sl].copy()
 assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name
 while len(AVAILABLE)>12:AVAILABLE.pop(next(iter(AVAILABLE)))
 return a

def initialize():
 load_io();globals()['keep']=bounded_keep;initialize_helpers()
 for file in ('author_fragment_native_metric_star_paired_gmres_resume_v002.py','author_fragment_saved_adjoint7_coefficient_continuation_v001.py'):exec(compile(selected_definitions(file,None),file,'exec'),globals())
 for n in ast.parse((BASE/'author_fragment_saved_adjoint7_coefficient_continuation_v001.py').read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('ADJOINT7_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(GMRES_RESUME_AUTHOR_DRAFT=False,GMRES_RESUME_AUTHORING_IN_PROGRESS=False,GMRES_RESUME_PREFIX_PROOF=ADJOINT7_PREFIX_PROOF,GMRES_RESUME_COEFFICIENT_PROOF=(None,None,None),ADJOINT7_CONTINUATION_AUTHOR_DRAFT=False,ADJOINT7_CONTINUATION_AUTHORING_IN_PROGRESS=False)
 P.LINEAR_TOL=1e-10

def commit(ref,receipt=None):
 bind(ref['commit_file'],ref['commit_sha256']);q=json.loads(P.path(ref['commit_file']).read_text());md=q['metadata']
 assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
 assert md['failed'] is False and md['qualification']==FLAGS
 if receipt is not None:assert all(receipt['output_sha256'][ref[f]]==ref[h] for f,h in (('file','sha256'),('commit_file','commit_sha256')))
 return dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def read_selected(ref,names):
 q=commit(ref);path=P.path(q['file']);st=path.stat();identity=(st.st_ino,st.st_size,st.st_mtime_ns,st.st_mode);assert not st.st_mode&0o222
 if q['file'] not in VERIFIED_ARCHIVES:bind(q['file'],q['sha256']);VERIFIED_ARCHIVES[q['file']]=(q['sha256'],identity)
 assert VERIFIED_ARCHIVES[q['file']]==(q['sha256'],identity);md=q['metadata'];out={}
 with np.load(path,allow_pickle=False) as f:
  assert set(f.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md
  for n in names:
   a=f[n].copy();RAW['loaded_'+n]=a;keep('loaded_'+n,a);s=md['schema'][n]
   assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True and np.all(np.isfinite(a));out[n]=a
 end=path.stat();assert identity==(end.st_ino,end.st_size,end.st_mtime_ns,end.st_mode);return out

def complete_stage(role,data,metadata):
 global CURRENT_CANDIDATE
 context=dict(CONTEXT);q=P.checkpoint(role,arrays(data),dict(metadata,context=context));ref=thin(q);clear_current();CONTEXT.update(context)
 if role=='CANDIDATE':CURRENT_CANDIDATE=ref
 if role=='ITERATION_STATE':NEW_BASIS.append(ref);NEW_STATES.append(ref)
 if role=='NEW_ASTAR_WEAK':NEW_ACTIONS.append(ref)
 return ref

def terminal_identity(terminal):
 source,result,receipt,proof=terminal
 for q in (source,receipt,proof):bind(q[0],q[1])
 rc=json.loads(P.path(receipt[0]).read_text());pr=json.loads(P.path(proof[0]).read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==result[1] and rc['error_sha256'] is None
 assert rc['owner']==pr['owner'] and rc['owner']['source_sha256']==source[1] and rc['qualification'] and all(v is False for v in rc['qualification'].values())
 assert pr['status']==proof[2] and pr['source_sha256']==source[1] and pr['result_sha256']==result[1] and pr['receipt_sha256']==receipt[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==0 and pr['all_input_seals_verified'] is pr['all_success_role_seals_verified'] is True
 assert all(v is False for v in pr.get('qualification',FLAGS).values()) and pr.get('physical_adoption',False) is False;return rc,pr

def admission():
 prefix=saved_adjoint7_prefix_admission();bind(*SELECTED_PROOF[:2]);sp=json.loads(P.path(SELECTED_PROOF[0]).read_text())
 assert sp['status']==SELECTED_PROOF[2] and sp['owner']==prefix['original_owner'] and sp['source']['sha256']==OLD_SOURCE[1] and sp['selected_expected_roles']==sp['selected_verified_roles']==16
 rows=[q for q in sp['records'] if q['ordinal']==0];assert len(rows)==1 and rows[0]['role']=='INPUT';old=commit(rows[0]);assert old['metadata']['owner']==prefix['original_owner']
 closed=old['metadata']['closed_provenance'];assert closed['factor']==json.loads(json.dumps((NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)))
 receipts={}
 for name in ('literal','transpose','application','anchor'):receipts[name],_=terminal_identity(closed[name])
 mechanical=closed['mechanical'];terminal_identity([mechanical[n] for n in ('source','result','receipt','proof')])
 nrc,npr=terminal_identity((NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF));bind(*NODAL_PROJECTION[:2]);projection=json.loads(P.path(NODAL_PROJECTION[0]).read_text());projected=projection['projected_result'];case=projected['case']
 assert projection['status']==NODAL_PROJECTION[2] and projection['source_sha256']==NODAL_SOURCE[1] and projection['receipt_sha256']==NODAL_RECEIPT[1] and projection['original_result']['sha256']==NODAL_RESULT[1]
 assert projection['original_proof']==dict(file=NODAL_PROOF[0],sha256=NODAL_PROOF[1],status=NODAL_PROOF[2]) and projection['owner']==nrc['owner']==npr['owner']==projected['owner']
 assert all(projection[n] is True for n in ('naturally_closed','all_success_role_seals_verified','selected_case_fields_exact','top_result_suffix_exact','full_result_bytes_sha256_freshly_verified','original_all_controls_passed_inherited')) and projection['exit_code']==0
 assert projected['status']==NODAL_RESULT[2] and projected['qualification']==FLAGS and case['closed_mechanical']==mechanical and case['right_preconditioner_factor_resolved'] is True and len(case['completed_chunk_refs'])==120
 nodal_input=commit(case['input'],nrc);bprov=nodal_input['metadata']['basis_provenance'];assert nodal_input['metadata']['closed_mechanical']==mechanical
 chunks=[];candidate_by_column={}
 for serial,ref in enumerate(case['completed_chunk_refs']):
  q=commit(ref,nrc);md=q['metadata'];iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784);p=hi-lo;pre='NEW_directed_nodal_q%d_chunk%03d_point_'%(iq,serial)
  assert md['owner']==nrc['owner'] and md['kind']=='completed_directed_nodal_moment_chunk_patch' and md['chunk']==serial and md['next_chunk']==serial+1 and md['column']==iq and md['selection']==[lo,hi] and md['basis_provenance']==bprov
  point=commit(md['committed_point_chunk'],nrc);pm=point['metadata'];assert pm['source']['closed_mechanical']==mechanical and pm['source']['column']==iq and pm['source']['selection']==[lo,hi] and pm['source']['original_basis']==bprov['original_basis']
  if iq not in candidate_by_column:candidate_by_column[iq]=pm['closed_candidate_provenance']
  assert pm['closed_candidate_provenance']==candidate_by_column[iq]
  assert len(md['completed_source_contacts'])==3 and all(c['passed'] is True and c['tolerance']==2e-11 for c in md['completed_source_contacts'])
  names={n:tuple(pre+'paired_raw_'+n+'_'+w for w in ('hi','lo')) for n in ('H','B','E','D')};names.update({'e'+n:pre+'e'+n for n in ('H','B','E','D')})
  for n,shape in dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3)).items():
   for key in names[n]+(names['e'+n],):assert md['schema'][key]==dict(shape=list(shape),dtype='float64',finite=True)
  chunks.append(dict(column=iq,lo=lo,hi=hi,point_block_ref=thin(q),same_candidate_provenance=pm['closed_candidate_provenance'],basis_provenance=bprov,selected_names=names,committed_original_point=thin(point)))
 cm=prefix['records'][prefix['case']['context']['file']];assert cm['source']==thin(old) and cm['factor_context']['terminal']==closed['factor'] and cm['factor_context']['application']==closed['application']
 factor=commit(cm['factor_context']['original'],nrc);copy=commit(cm['factor_context']['copy']);assert copy['metadata']['source']==thin(factor) and copy['metadata']['controls']==closed['application'] and copy['metadata']['owner']==prefix['original_owner']
 fm=factor['metadata'];assert fm['owner']==nrc['owner'] and fm['active_node_count']==3870 and fm['right_preconditioner_factor_resolved'] is True and fm['inactive_coordinates_are_zero_not_identity_padding'] is True
 assert fm['sheet_head_dimension']==6 and fm['sheet_arm_dimension']==2 and fm['interior_head_dimension']==9 and fm['interior_arm_dimension']==3 and fm['nodal_apply_or_weak_functional_qualified'] is fm['exact_weak_DD_or_global_inverse_qualified'] is fm['physical_adoption'] is False
 return dict(prefix=prefix,old=old,nodal_input=nodal_input,nodal_receipt=nrc,basis_provenance=bprov,chunks=chunks,factor=factor,factor_context=cm['factor_context'],closed_provenance=closed)

def hydrate(refs):
 packet=prepare_saved_adjoint7_coefficient_continuation(refs['prefix'],read_selected,complete_stage,keep,'saved_adjoint7_hydration');assert packet['factor_context']==refs['factor_context']
 d=read_selected(thin(refs['old']),tuple('copied_anchor_original_basis_'+n for n in ('R','dv','hats')));basis={n:d['copied_anchor_original_basis_'+n] for n in ('R','dv','hats')}
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 n=read_selected(thin(refs['nodal_input']),tuple('original_registered_basis_'+n for n in basis))
 for key,a in basis.items():assert np.array_equal(a.view(np.uint64),n['original_registered_basis_'+key].view(np.uint64))
 complete_stage('BASIS_CONTEXT',basis,dict(original_input=thin(refs['old']),nodal_input=thin(refs['nodal_input']),bitwise_closed_basis_match=True))
 fd=read_selected(thin(refs['factor']),tuple('assembled_'+n+'_'+w for n in ('D_inverse','S_inverse','B','E') for w in ('hi','lo')))
 factors={n:tuple(fd['assembled_'+n+'_'+w] for w in ('hi','lo')) for n in ('D_inverse','S_inverse','B','E')}
 factors.update(closed_provenance=dict(factor_record=thin(refs['factor']),terminal=(NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF)),all_active_factor_seals_verified=True,active_node_count=3870,right_preconditioner_factor_resolved=True,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
 nodal=prepare_candidate_directed_nodal_factor_apply(factors,keep,'NEW_same_earned_signed_factor_guard');complete_stage('FACTOR_CONTEXT',dict(active_nodes=np.asarray(3870)),dict(original_factor=thin(refs['factor']),factor_context=packet['factor_context'],inverse_or_factor_body_replayed=False))
 prepared=dict(chunks=refs['chunks'],basis=basis,closed=refs['closed_provenance']['factor'],physical_adoption=False,coefficient_transpose_only=True,authoritative147_association_measured=False,global_inverse_qualified=False)
 return packet,nodal,prepared

def continuation(refs,packet,nodal,prepared):
 def read_chunk(descriptor,names):
  CONTEXT.update(column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],source=descriptor['point_block_ref'])
  keys=tuple(key for n in ('H','B','E','D') for key in descriptor['selected_names'][n])+tuple(descriptor['selected_names']['e'+n] for n in ('H','B','E','D'));d=read_selected(descriptor['point_block_ref'],keys)
  return dict(record=descriptor['point_block_ref'],source_provenance=descriptor['same_candidate_provenance'],paired_raw={n:tuple(d[k] for k in descriptor['selected_names'][n]) for n in ('H','B','E','D')},operation_envelopes={n:d[descriptor['selected_names']['e'+n]] for n in ('H','B','E','D')})
 def action(x,tag):
  ACTIVE_ARGUMENT.clear();ACTIVE_ARGUMENT.update(current_supplied_hi=x[0].copy(),current_supplied_lo=x[1].copy())
  CONTEXT.update(stage='signed_Astar',label=tag)
  def completed(d,part):return complete_stage('ADJOINT_CHUNK',dict(native_hi=part[0][0],native_lo=part[0][1],metric_hi=part[1][0],metric_lo=part[1][1]),dict(source=d['point_block_ref'],column=d['column'],selection=[d['lo'],d['hi']],label=tag,operator='represented_coefficient_Astar'))
  return candidate_measured_coefficient_fullweak_transpose(prepared,x,read_chunk,keep,tag,completed)['packed']
 def positive(x,tag):
  ACTIVE_ARGUMENT.clear();ACTIVE_ARGUMENT.update(current_supplied_hi=x[0].copy(),current_supplied_lo=x[1].copy())
  pending=[];parts=[];POSITIVE_PENDING.clear();CONTEXT.update(stage='positive',label=tag)
  def completed():
   if pending:
    d=pending.pop();assert set(POSITIVE_PENDING)=={'native','metric'};parts.append(complete_stage('POSITIVE_CHUNK',dict(POSITIVE_PENDING),dict(source=d['point_block_ref'],column=d['column'],selection=[d['lo'],d['hi']],label=tag,original244_unsigned_scope=True)));POSITIVE_PENDING.clear()
  def reader(d,names):completed();pending.append(d);return read_chunk(d,names)
  e=candidate_fullweak_coefficient_positive(prepared,x,reader,keep,tag);completed();assert len(parts)==120;return e
 def right(x,tag):
  ACTIVE_ARGUMENT.clear();ACTIVE_ARGUMENT.update(current_supplied_hi=x[0].copy(),current_supplied_lo=x[1].copy())
  CONTEXT.update(stage='new_signed_right_adjoint',label=tag);return candidate_directed_nodal_factor_adjoint(nodal,x,keep,tag)
 operator=dict(original_source=OLD_SOURCE,source_pins=ADJOINT7_SELECTED_PINS,factor_context=packet['factor_context'],operator='represented_directed_original244_coefficient_Astar',same_original244_directed_point_descriptors=True,original53_source_relative_gate_semantics_preserved=True,all_selected_sources_and_role_seals_verified=True,padded_point_envelopes_authenticated=True,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False)
 nodes,after,increment,history=continue_saved_adjoint7_coefficient(packet,operator,right,action,positive,complete_stage,keep,GMRES_LABEL)
 final=mechanical_adjoint_scores(after['residual'],packet['reference'],keep,'NEW_final_source_relative');assert np.array_equal(final.view(np.uint64),after['scores'].view(np.uint64));admitted=bool(np.all(final<=P.LINEAR_TOL))
 terminal=complete_stage('TERMINAL_SCALAR_STATE',SMALL_STATE,dict(history=history,original_context=packet['context_ref'],basis_states=NEW_STATES,terminal_not_unconditionally_resumable=True))
 solution=complete_stage('SOLUTION',dict(lambda_hi=nodes[0],lambda_lo=nodes[1],action_hi=after['action'][0],action_lo=after['action'][1],residual_hi=after['residual'][0],residual_lo=after['residual'][1],increment_hi=increment[0],increment_lo=increment[1],scores=final),dict(history=history,terminal_state=terminal,original_prefix=ADJOINT7_PREFIX_PROOF,original_factor=thin(refs['factor']),original_failed37897_exit_code=1,original_forward_physical_six_gates_tested=False,phase_or_gauge_feedback_evaluated=False))
 return dict(status='SAVED_PREFIX_COEFFICIENT_ADJOINT_SOURCE_ROWS_ADMITTED' if admitted else 'SAVED_PREFIX_COEFFICIENT_ADJOINT_SOURCE_ROWS_NOT_ADMITTED',solution=solution,source_relative_scores=final.tolist(),history=history,roles=len(RECORDS),controls=len(CHECKS),cap80_total=True,cycles=1,restarts=0,old_actions_factors_or_controls_replayed=False,original_all550_inputs_or_all857_outputs_verified=False,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS,'Root FULL/peer-reviewed exclusive release required';assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(IO_PARENT,IO_PARENT_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,original_source=OLD_SOURCE,prefix_proof=ADJOINT7_PREFIX_PROOF,nodal_projection=NODAL_PROJECTION,original_closed_provenance=refs['closed_provenance'],all_original_inputs_or_outputs_audited=False,physical_adoption=False));packet,nodal,prepared=hydrate(refs)
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=continuation(refs,packet,nodal,prepared)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**SMALL_STATE,**ACTIVE_ARGUMENT,**{'last_positive_'+n:a for n,a in POSITIVE_PENDING.items()},**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_coefficient_adjoint_operation',context=dict(CONTEXT),last_candidate=CURRENT_CANDIDATE,basis_states=NEW_STATES,completed_new_actions=NEW_ACTIONS,original_prefix=ADJOINT7_PREFIX_PROOF),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
