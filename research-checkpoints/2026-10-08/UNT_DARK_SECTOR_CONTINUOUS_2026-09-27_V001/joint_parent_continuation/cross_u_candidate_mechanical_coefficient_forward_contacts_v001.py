"""HELD two NEW coefficient-forward/authoritative147 association contacts.
Only root authenticates future closure, releases and executes this namespace.
No completed action, point basis, current, factor, EOS or solver is replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_MECHANICAL_COEFFICIENT_FORWARD_CONTACTS_V001'
DRIVER_PROTOCOL='CANDIDATE_MECHANICAL_COEFFICIENT_FORWARD_CONTACTS_V001.md'
PROTOCOL_SHA='709bc3379616c997b1057c41e5de5c8bc2b8399c62f88b9aaa6fe9ff6d58b560'
COEFFICIENT_PROTOCOL='CANDIDATE_MECHANICAL_COEFFICIENT_FORWARD_V001.md'
COEFFICIENT_PROTOCOL_SHA='761f85a729f58f6334e604c2ffdee9ad275244b901e7c05dc74e00b043e3b96a'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
NODAL_SOURCE=(None,None)
NODAL_RESULT=(None,None,'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
NODAL_RECEIPT=(None,None,'CLOSED')
NODAL_PROOF=(None,None,None)
MECHANICAL_SOURCE=(None,None)
MECHANICAL_RESULT=(None,None,'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=(None,None,'CLOSED')
MECHANICAL_CLOSURE_PROOF=(None,None,None)
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py': 'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_mechanical_coefficient_forward_v001.py': 'bc6e09716ab71ed9a43ff6bd27666a393fe0584f7ac1ac3ed5d519edd747c3c7'}
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
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter','pack_fields','unpack_fields','pack_dd','scalar_mask'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
  for n in names:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|{'B','GC','C','ALPHA','ELL'}})
 for n in ('B','GC','C','ALPHA','ELL'):setattr(P,n,SCOPE[n])
 choices=(('author_fragment_finite_york_geometry_target_v001.py',None),('author_fragment_compact_metric_contact_momenta_v002.py',{'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}),('author_fragment_candidate_specialized_temporal_action_v001.py',{'ft_keep','candidate_temporal_jets','candidate_temporal_canonical','candidate_specialized_temporal_action'}),('author_fragment_candidate_specialized_weak_mechanical_action_v002.py',{'sw_keep','specialized_weak_mechanical_action'}),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_provider_admission','candidate_point_cache_names'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',None),('cross_u_candidate_literal_phase_charge_response_v002.py',{'bind_record'}),('author_fragment_exact_exponent_two_product_v003.py',None),('author_fragment_candidate_mechanical_coefficient_forward_v001.py',None))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_candidate_chunk_point_block_provider_v001.py'
 for n in ast.parse((BASE/file).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('POINT_'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False,COEFFICIENT_FORWARD_AUTHOR_DRAFT=False,COEFFICIENT_FORWARD_AUTHORING_IN_PROGRESS=False,COEFFICIENT_FORWARD_SOURCE=NODAL_SOURCE,COEFFICIENT_FORWARD_RESULT=NODAL_RESULT,COEFFICIENT_FORWARD_RECEIPT=NODAL_RECEIPT,COEFFICIENT_FORWARD_PROOF=NODAL_PROOF)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_coefficient_forward_exact_exponent_product')


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
 q=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,publication_role=role,context=dict(CONTEXT)));clear_current();return q

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

def coefficient_admission():
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

def new_coefficient_direction(case,dual,keep,label):
 assert case in (0,1) and isinstance(dual,bool);n=np.zeros((33,3,87,45));m=np.zeros((6,87,45));nl=np.zeros_like(n);ml=np.zeros_like(m)
 if case==0:
  entries=((0,0,23,17,.25),(6,2,57,31,-.125),(25,1,86,7,.0625),(32,0,49,44,-.03125),(0,2,1,0,.125)) if not dual else ((0,1,23,17,-.125),(12,0,57,31,.25),(28,2,86,7,-.0625),(3,0,49,44,.03125),(0,0,1,0,-.25))
  for k,(mode,component,i,z,value) in enumerate(entries):n[mode,component,i,z]=value;nl[mode,component,i,z]=(-1.)**k*2.**-60*value
  for slot in range(6):m[slot,23,17]=(-1.)**(slot+int(dual))*2.**(-4-slot);ml[slot,23,17]=(-1.)**(slot+1)*2.**-60*m[slot,23,17]
  for slot,i,z,value in ((0,1,0,.0625),(5,86,7,-.03125),(2,49,44,.015625)):
   m[slot,i,z]=value*(-1. if dual else 1.);ml[slot,i,z]=-2.**-61*m[slot,i,z]
 else:
  ii=np.arange(87)[:,None];jj=np.arange(45)[None,:];pattern=np.where((2*ii+jj)%3==0,-1.,1.)
  modes=(0,2,11,23,32) if not dual else (0,5,14,26,30)
  for mode in modes:
   for component in range(3):
    n[mode,component]=pattern*(-1.)**(mode+component+int(dual))*2.**(-9-component)
    nl[mode,component]=np.where((ii+2*jj+component)%2,1.,-1.)*2.**-60*n[mode,component]
  for slot in range(6):
   m[slot]=pattern*(-1.)**(slot+int(dual))*2.**(-11-slot);ml[slot]=np.where((ii+jj+slot)%2,1.,-1.)*2.**-61*m[slot]
 nm=np.broadcast_to(P.native_mask(),n.shape);mm=P.metric_mask()
 for a in (n,nl):a[~nm]=0
 for a in (m,ml):a[~mm]=0
 cpf_pair(label+'_native_nodes',(n,nl),keep,n.shape);cpf_pair(label+'_metric_nodes',(m,ml),keep,m.shape)
 out=cpf_pair(label+'_original_packed',P.pack_dd((n,nl),(m,ml)),keep,(403340,));assert np.any(out[1]!=0)
 return out

def independent_dual_dot(x,y,keep,label):
 assert x[0].shape==x[1].shape==y[0].shape==y[1].shape==(403340,)
 terms=cpf_pair(label+'_independent_product_terms',P.a_mul(x,y),keep,(403340,))
 while len(terms[0])>1:
  n=len(terms[0]);m=n-n%2;out=P.a_add((terms[0][:m:2],terms[1][:m:2]),(terms[0][1:m:2],terms[1][1:m:2]))
  if n%2:out=tuple(np.concatenate((out[w],terms[w][-1:])) for w in (0,1))
  terms=cpf_pair(label+'_balanced_product_sum_partial',out,keep)
 return cpf_pair(label+'_scalar',tuple(np.asarray(a[0]).copy() for a in terms),keep,())

def paired_association_control(actual,expected,envelope,keep,label):
 cpf_pair(label+'_actual',actual,keep);cpf_pair(label+'_expected',expected,keep)
 assert actual[0].shape==expected[0].shape;envelope=keep(label+'_uncancelled_envelope',np.asarray(envelope).copy())
 assert envelope.shape==actual[0].shape and envelope.dtype==np.float64 and np.all(envelope>=0)
 gap=cpf_pair(label+'_both_word_gap',P.a_sub(actual,expected),keep)
 error=mp_add(abs(gap[0]),abs(gap[1]),keep,label+'_both_word_error_upper');active=envelope>0
 keep(label+'_zero_envelope_mask',(~active).astype(np.int64));ratios=np.zeros(envelope.shape)
 with np.errstate(over='ignore',divide='ignore',invalid='ignore',under='ignore'):np.divide(error,envelope,out=ratios,where=active)
 ratios=np.where(active&(error>0),np.nextafter(ratios,np.inf),ratios);keep(label+'_dimensionless_ratio_upper',ratios.copy())
 assert all(np.all(a[~active]==0) for a in actual+expected),'Both supplied words must be exactly zero when the envelope is zero'
 assert np.all(np.isfinite(ratios));P.check(label,ratios,np.zeros_like(ratios),np.ones_like(ratios))
 return dict(name=label,maximum_ratio_upper=float(np.max(ratios,initial=0)),original_tolerance=2e-11,both_words_retained=True,no_reference_floor=True)


def coefficient_forward_packet(refs):
 nd=read(refs['input'],tuple('original_registered_basis_'+n for n in ('R','dv','hats')));RAW.clear();basis={n:keep('copied_nodal_original_basis_'+n,nd['original_registered_basis_'+n]) for n in ('R','dv','hats')}
 md=read(refs['mechanical']['input'],tuple('registered_basis_'+n for n in basis));RAW.clear()
 for n in basis:keep('copied_mechanical_registered_basis_'+n,md['registered_basis_'+n]);assert np.array_equal(basis[n],md['registered_basis_'+n])
 basis['closed_provenance']=refs['basis_provenance'];inp=thin(seal('INPUT',dict(kind='closed_original_basis_and120_padded_point_descriptors',nodal_input=thin(refs['input']),closed_nodal=refs['closed'],mechanical=refs['mechanical']['closed_provenance'],point_descriptors=refs['chunks'],inverse_factors_used=False,physical_adoption=False)))
 blocks,cache_refs=hydrate_blocks(refs['mechanical'],basis);prepared=prepare_candidate_mechanical_coefficient_forward(refs['chunks'],basis,refs['closed'],keep,'NEW_coefficient_forward_prepared');prep=thin(seal('PREPARED',dict(kind='authenticated_same_candidate120_paired_point_coefficients',input=inp,cache_copies=cache_refs,closed_nodal=refs['closed'],physical_adoption=False)))
 cases=[]
 for case in (0,1):
  label='NEW_coefficient_forward_case%d'%case;CONTEXT.update(case=case,stage='NEW_direction');probe=new_coefficient_direction(case,False,keep,label+'_probe');dual=new_coefficient_direction(case,True,keep,label+'_dual');direction=thin(seal('DIRECTION',dict(kind='NEW_signed_paired_original_coordinates_and_independent_dual',case=case,input=inp,prior_direction_or_action_replayed=False,physical_adoption=False)));columns=[]
  fields=[P.unpack_fields(a,False) for a in probe]
  def action_column(iq,data):
   CONTEXT.update(case=case,column=iq,stage='NEW_authoritative_column');capture_families('completed_column_',data);ref=thin(seal('ACTION_COLUMN',dict(kind='NEW_authoritative147_original67_column',case=case,column=iq,cache=cache_refs[iq],direction=direction,physical_adoption=False)));columns.append(ref);return ref
  authoritative=specialized_weak_mechanical_action(blocks,basis,tuple(q[0] for q in fields),tuple(q[1] for q in fields),keep,label+'_authoritative67',action_column)
  forward=cpf_pair(label+'_NEW_authoritative_weak',P.pack_dd(authoritative['weak']['native'],authoritative['weak']['metric']),keep,(403340,));forward_ref=thin(seal('ACTION_WEAK',dict(kind='NEW_all_four_authoritative147_weak',case=case,columns=columns,direction=direction,physical_adoption=False)))
  ef=candidate_weak_mechanical_positive(blocks,basis,probe,keep,label+'_authoritative_positive124');keep(label+'_authoritative_outward_envelope',ef);assert ef.shape==(403340,) and np.all(ef>=0);ef_ref=thin(seal('ACTION_POSITIVE',dict(kind='NEW_separate124_unsigned147_original_E_S_bound',case=case,direction=direction,represented_coefficient_bound_substituted=False,physical_adoption=False)))
  def proxy_chunk(descriptor,part):
   CONTEXT.update(case=case,column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],stage='NEW_proxy_chunk');cpf_pair('completed_proxy_native',part[0],keep);cpf_pair('completed_proxy_metric',part[1],keep)
   return thin(seal('PROXY_CHUNK',dict(kind='NEW_paired_original_point_K_forward',case=case,direction=direction,source=descriptor['point_block_ref'],column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],physical_adoption=False)))
  def proxy_column(iq,data):
   CONTEXT.update(case=case,column=iq,stage='NEW_proxy_column');capture_families('completed_proxy_column_',data)
   return thin(seal('PROXY_COLUMN',dict(kind='NEW_paired_proxy_point_column',case=case,column=iq,direction=direction,chunks=data['chunk_refs'],same_candidate_provenance=data['same_candidate_provenance'],physical_adoption=False)))
  proxy=candidate_measured_coefficient_fullweak_forward(prepared,probe,read_point_coefficients,keep,label+'_proxy',proxy_chunk,proxy_column);proxy_ref=thin(seal('PROXY_WEAK',dict(kind='NEW_original_S_directed_K_original_E',case=case,direction=direction,chunks=proxy['chunk_refs'],columns=proxy['column_refs'],authoritative147_action_used_as_proxy=False,physical_adoption=False)))
  def positive_chunk(descriptor,part):
   CONTEXT.update(case=case,column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],stage='NEW_proxy_positive_chunk');keep('completed_positive_native',part[0]);keep('completed_positive_metric',part[1])
   return thin(seal('PROXY_POSITIVE_CHUNK',dict(kind='NEW_padded_point_original124_coefficient_enclosure',case=case,direction=direction,source=descriptor['point_block_ref'],column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],physical_adoption=False)))
  def positive_column(iq,data):
   CONTEXT.update(case=case,column=iq,stage='NEW_proxy_positive_column');capture_families('completed_positive_column_',data)
   return thin(seal('PROXY_POSITIVE_COLUMN',dict(kind='NEW_outward_proxy_point_column',case=case,column=iq,direction=direction,chunks=data['chunk_refs'],same_candidate_provenance=data['same_candidate_provenance'],physical_adoption=False)))
  positive=candidate_fullweak_coefficient_forward_positive(prepared,probe,read_point_coefficients,keep,label+'_proxy_positive',positive_chunk,positive_column);eh=positive['packed'];keep(label+'_proxy_outward_envelope',eh);eh_ref=thin(seal('PROXY_POSITIVE',dict(kind='NEW_separate_original124_padded_K_E_S_bound',case=case,direction=direction,chunks=positive['chunk_refs'],columns=positive['column_refs'],authoritative147_envelope_substituted=False,physical_adoption=False)))
  cpf_pair(label+'_retained_authoritative_weak',forward,keep,(403340,));cpf_pair(label+'_retained_proxy_weak',proxy['packed'],keep,(403340,));keep(label+'_retained_authoritative_envelope',ef);keep(label+'_retained_proxy_envelope',eh)
  vector_envelope=mp_add(ef,eh,keep,label+'_joint_uncancelled_vector_envelope');vector=paired_association_control(proxy['packed'],forward,vector_envelope,keep,label+'_all403340_vector_association')
  left=independent_dual_dot(dual,proxy['packed'],keep,label+'_independent_dual_proxy');right=independent_dual_dot(dual,forward,keep,label+'_independent_dual_authoritative')
  dm=mp_add(abs(dual[0]),abs(dual[1]),keep,label+'_dual_word_magnitude');dot_envelope=mp_sum(mp_mul(dm,vector_envelope,keep,label+'_dot_uncancelled_terms'),0,keep,label+'_dot_uncancelled_sum');dot=paired_association_control(left,right,dot_envelope,keep,label+'_independent_dual_dot_association')
  contact=thin(seal('ASSOCIATION',dict(kind='complete_vector_and_independent_balanced_dual_dot',case=case,direction=direction,authoritative=forward_ref,authoritative_positive=ef_ref,proxy=proxy_ref,proxy_positive=eh_ref,controls=CHECKS[-2:],uniform_association_or_inverse_qualified=False,physical_adoption=False)))
  cases.append(dict(case=case,direction=direction,authoritative=forward_ref,authoritative_positive=ef_ref,proxy=proxy_ref,proxy_positive=eh_ref,association=contact,vector=vector,dot=dot))
 expected_names=['NEW_coefficient_forward_case%d_'%case+suffix for case in (0,1) for suffix in ('all403340_vector_association','independent_dual_dot_association')]
 assert [q['name'] for q in CHECKS]==expected_names and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 from collections import Counter
 census=dict(Counter(q['metadata']['publication_role'] for q in RECORDS));expected=dict(INPUT=1,CACHE_COPY=4,PREPARED=1,DIRECTION=2,ACTION_COLUMN=8,ACTION_WEAK=2,ACTION_POSITIVE=2,PROXY_CHUNK=240,PROXY_COLUMN=8,PROXY_WEAK=2,PROXY_POSITIVE_CHUNK=240,PROXY_POSITIVE_COLUMN=8,PROXY_POSITIVE=2,ASSOCIATION=2)
 assert census==expected and len(RECORDS)==522 and len(CHECKS)==4
 final=thin(seal('PREPARATION',dict(kind='two_NEW_coefficient_forward_association_contacts_only',input=inp,prepared=prep,cases=cases,original2e11_unchanged=True,original_six_canonical_gates_evaluated=False,uniform_association_adjoint_inverse_or_physics=False,old_component_inverse_failure_repaired=False,physical_adoption=False)))
 assert len(RECORDS)==523
 return dict(status='NEW_MECHANICAL_COEFFICIENT_FORWARD_TWO_DIRECTION_ASSOCIATIONS_PASS',input=inp,prepared=prep,preparation=final,cases=cases,closed_nodal=refs['closed'],closed_mechanical=refs['mechanical']['closed_provenance'],roles=523,role_census=dict(expected,PREPARATION=1),new_controls=4,new_authoritative_directions=2,old_point_basis_factor_current_EOS_action_or_solver_replayed=False,original_six_canonical_gates_evaluated=False,uniform_association_adjoint_or_inverse_qualified=False,physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root reviewed release required'
 assert all(x is not None for ref in (NODAL_SOURCE,NODAL_RESULT,NODAL_RECEIPT,NODAL_PROOF,MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF) for x in ref),'Authentic natural CLOSED nodal and mechanical packets required before I/O'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(COEFFICIENT_PROTOCOL,COEFFICIENT_PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  initialize_helpers();refs=coefficient_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_nodal=refs['closed'],new_direction_count=2,coefficient_proxy_only=True,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=coefficient_forward_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_coefficient_forward_association_with_completed_ancestry',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
