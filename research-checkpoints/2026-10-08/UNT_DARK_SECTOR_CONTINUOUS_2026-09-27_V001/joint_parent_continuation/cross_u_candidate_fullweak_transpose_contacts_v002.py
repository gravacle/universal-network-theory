"""HELD NEW fullweak paired coefficient-transpose association contacts.
Root alone binds natural closure/releases. Source/metadata authoring only.
No original point basis, current, factor, action, solver or fixture is replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_FULLWEAK_TRANSPOSE_CONTACTS_V002'
DRIVER_PROTOCOL='CANDIDATE_FULLWEAK_TRANSPOSE_CONTACTS_V002.md'
PROTOCOL_SHA='3594e6eecbc05320ac8f4133b4c9d5232e980c1f22f80184a4f51db18f1d6906'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
NODAL_SOURCE=(None,None)
NODAL_RESULT=(None,None,'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
NODAL_RECEIPT=(None,None,'CLOSED')
NODAL_PROOF=(None,None,None)
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py','489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json','49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e','COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json','c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64','CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json','2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9','ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py': 'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871'}
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
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter','pack_fields','unpack_fields','pack_dd','scalar_mask'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
  for n in names:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|{'C','ALPHA','ELL'}});P.C=1.98;P.ALPHA=.02/1.98;P.ELL=.1
 choices=(('author_fragment_finite_york_geometry_target_v001.py',None),('author_fragment_compact_metric_contact_momenta_v002.py',{'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}),('author_fragment_candidate_specialized_temporal_action_v001.py',{'ft_keep','candidate_temporal_jets','candidate_temporal_canonical','candidate_specialized_temporal_action'}),('author_fragment_candidate_specialized_weak_mechanical_action_v002.py',{'sw_keep','specialized_weak_mechanical_action'}),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_provider_admission','candidate_point_cache_names'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',None),('cross_u_candidate_literal_phase_charge_response_v002.py',{'bind_record'}),('author_fragment_exact_exponent_two_product_v003.py',None),('author_fragment_candidate_fullweak_transpose_stationarity_v003.py',None))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_candidate_chunk_point_block_provider_v001.py'
 for n in ast.parse((BASE/file).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('POINT_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False,FULLWEAK_TRANSPOSE_AUTHOR_DRAFT=False,FULLWEAK_TRANSPOSE_AUTHORING_IN_PROGRESS=False,FULLWEAK_TRANSPOSE_SOURCE=NODAL_SOURCE,FULLWEAK_TRANSPOSE_RESULT=NODAL_RESULT,FULLWEAK_TRANSPOSE_RECEIPT=NODAL_RECEIPT,FULLWEAK_TRANSPOSE_PROOF=NODAL_PROOF)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_fullweak_transpose_exact_exponent_product')


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

def new_original_direction(case,dual,keep,label):
 assert case in (0,1) and isinstance(dual,bool);n=np.zeros((33,3,87,45));m=np.zeros((6,87,45))
 if case==0:
  entries=((0,0,1,0,.5),(4,2,43,22,-.25),(17,1,86,44,.125)) if not dual else ((0,2,1,0,-.25),(9,0,43,22,.5),(31,2,86,44,-.125))
  for mode,component,i,j,value in entries:n[mode,component,i,j]=value
  for slot in range(6):m[slot,43,22]=(-1. if (slot+int(dual))%2 else 1.)*2.**(-3-slot)
  m[0,1,0]=.25 if dual else -.125;m[5,86,44]=-.0625 if dual else .125
 else:
  parity=np.where((np.arange(87)[:,None]+np.arange(45)[None,:])%2,1.,-1.)
  modes=(0,1,9,31) if not dual else (0,4,17,29)
  for mode in modes:
   for component in range(3):n[mode,component]=parity*((-1.)**(mode+component+int(dual)))*2.**(-6-component)
  for slot in range(6):m[slot]=parity*((-1.)**(slot+int(dual)))*2.**(-8-slot)
 n[~np.broadcast_to(P.native_mask(),n.shape)]=0;m[~P.metric_mask()]=0
 pair=P.pack_dd((n,2.**-60*n),(m,2.**-60*m));ct_pair(label+'_original_packed_both_words',pair,keep)
 assert pair[0].shape==pair[1].shape==(403340,) and np.any(pair[1]!=0)
 return pair

def transpose_packet(refs):
 nd=read(refs['input'],tuple('original_registered_basis_'+n for n in ('R','dv','hats')));RAW.clear();basis={n:keep('copied_nodal_original_basis_'+n,nd['original_registered_basis_'+n]) for n in ('R','dv','hats')}
 md=read(refs['mechanical']['input'],tuple('registered_basis_'+n for n in basis));RAW.clear()
 for n in basis:keep('copied_mechanical_registered_basis_'+n,md['registered_basis_'+n]);assert np.array_equal(basis[n],md['registered_basis_'+n])
 basis['closed_provenance']=refs['basis_provenance'];inp=thin(seal('INPUT',dict(kind='copied_authentic_original_basis_and120_padded_point_descriptors',nodal_input=thin(refs['input']),closed_nodal=refs['closed'],mechanical=refs['mechanical']['closed_provenance'],point_descriptors=refs['chunks'],inverse_factors_used_as_operator=False,physical_adoption=False)))
 blocks,cache_refs=hydrate_blocks(refs['mechanical'],basis);prepared=prepare_candidate_fullweak_transpose(refs['chunks'],basis,refs['closed'],keep,'NEW_fullweak_transpose_prepared');prep=thin(seal('PREPARED',dict(kind='authenticated120_paired_point_coefficients_and_original_basis',input=inp,cache_copies=cache_refs,closed_nodal=refs['closed'],physical_adoption=False)))
 cases=[]
 for case in (0,1):
  label='NEW_fullweak_transpose_case%d'%case;probe=new_original_direction(case,False,keep,label+'_probe');dual=new_original_direction(case,True,keep,label+'_dual');direction=thin(seal('DIRECTION',dict(kind='genuinely_NEW_predeclared_same_candidate_paired_original_coordinates',case=case,input=inp,old_basis_or_action_replayed=False,physical_adoption=False)));columns=[];chunks=[]
  fields=[P.unpack_fields(a,False) for a in probe]
  def column_complete(iq,data):
   capture_families('completed_column_',data);ref=thin(seal('ACTION_COLUMN',dict(kind='NEW_authoritative147_fixed_configuration_temporal_column',case=case,column=iq,cache=cache_refs[iq],direction=direction,physical_adoption=False)));columns.append(ref);return ref
  result=specialized_weak_mechanical_action(blocks,basis,tuple(q[0] for q in fields),tuple(q[1] for q in fields),keep,label+'_authoritative67',column_complete)
  forward=ct_pair(label+'_NEW_authoritative_weak',P.pack_dd(result['weak']['native'],result['weak']['metric']),keep);forward_ref=thin(seal('ACTION_WEAK',dict(kind='NEW_all_four_original_weak67_forward',case=case,columns=columns,direction=direction,physical_adoption=False)))
  forward_bound=candidate_weak_mechanical_positive(blocks,basis,probe,keep,label+'_authoritative_positive124');positive_ref=thin(seal('ACTION_POSITIVE',dict(kind='NEW_separate_unsigned147_original_lift_and_scatter_bound',case=case,direction=direction,represented_factor_bound_used=False,physical_adoption=False)))
  def chunk_complete(descriptor,part):
   ct_pair(label+'_completed_chunk_native',part[0],keep);ct_pair(label+'_completed_chunk_metric',part[1],keep)
   ref=thin(seal('TRANSPOSE_CHUNK',dict(kind='NEW_directed_point_coefficient_transpose',case=case,column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],source=descriptor['point_block_ref'],direction=direction,completed_point_partials_retained_before_clear=True,physical_adoption=False)));chunks.append(ref);return ref
  trans=candidate_measured_coefficient_fullweak_transpose(prepared,dual,read_point_coefficients,keep,label+'_coefficient_transpose',chunk_complete);transpose_ref=thin(seal('TRANSPOSE_WEAK',dict(kind='NEW_original_Sstar_directed_Kstar_rounded_Estar',case=case,direction=direction,chunks=chunks,uniform_adjoint_or_inverse_qualified=False,physical_adoption=False)))
  trans_bound=candidate_fullweak_coefficient_positive(prepared,dual,read_point_coefficients,keep,label+'_coefficient_positive');transpose_positive_ref=thin(seal('TRANSPOSE_POSITIVE',dict(kind='NEW_saved_padded_point_bound_reverse_original_maps',case=case,direction=direction,raw_or_nodal_moment_envelope_substituted=False,physical_adoption=False)))
  provenance=dict(genuinely_NEW_same_candidate_forward_direction=True,old_point_basis_or_action_replayed=False,same_candidate_provenance=refs['closed']['same_candidate_provenance'],forward=forward_ref,transpose=transpose_ref,closed_nodal=refs['closed'])
  contact=candidate_new_fullweak_transpose_pairing_contact(probe,dual,forward,trans['packed'],forward_bound,trans_bound,provenance,keep,P.check,label+'_pairing')
  pairing=thin(seal('PAIRING',dict(kind='NEW_wholeweak_direction_pair_and_source_association_contact',case=case,direction=direction,forward=forward_ref,forward_positive=positive_ref,transpose=transpose_ref,transpose_positive=transpose_positive_ref,controls=list(CHECKS[-1:]),literal_action_gradient_or_gauge_block_tested=False,physical_adoption=False)))
  cases.append(dict(case=case,direction=direction,forward=forward_ref,transpose=transpose_ref,pairing=pairing,association_gap=[np.asarray(w).item() for w in contact['gap']],uncancelled_envelope=float(contact['envelope'])))
 assert len(CHECKS)==2 and len(RECORDS)==266 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 final=thin(seal('PREPARATION',dict(kind='two_NEW_fullweak_forward_coefficient_transpose_contacts_only',input=inp,prepared=prep,cases=cases,original2e11_implementation_gates_unchanged=True,literal_LV_bridge_earned=False,gauge_mixed_block_earned=False,stationarity_feedback_earned=False,canonical_six_rows_tested=False,global_inverse_or_uniform_adjoint_qualified=False,old_component_inverse_failure_repaired=False,physical_adoption=False)))
 assert len(RECORDS)==267
 return dict(status='NEW_FULLWEAK_COEFFICIENT_TRANSPOSE_DIRECTION_CONTACTS_PASS',input=inp,prepared=prep,preparation=final,cases=cases,closed_nodal=refs['closed'],roles=267,new_controls=2,old_point_basis_or_current_or_factor_or_solver_replayed=False,literal_LV_or_gauge_or_adjoint_solve_earned=False,uniform_DD_adjoint_or_global_inverse_qualified=False,original_six_or_normal_or_CMC_physical_admitted=False,old_component_inverse_failure_repaired=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root reviewed release required'
 assert all(x is not None for ref in (NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF) for x in ref),'Natural CLOSED nodal packet/proof required before I/O'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  initialize_helpers();refs=transpose_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_nodal=refs['closed'],new_direction_count=2,literal_stationarity_and_gauge_contacts_external=True,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=transpose_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_fullweak_transpose_contact_with_completed_ancestry',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())

