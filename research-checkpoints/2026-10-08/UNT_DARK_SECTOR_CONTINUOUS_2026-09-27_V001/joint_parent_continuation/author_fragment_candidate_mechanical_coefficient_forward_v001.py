"""HELD original-coordinate directed coefficient proxy Ahat=S K E.
Globals np,P and the exact nine selected124 outward/lift/scatter definitions.
No147 jet/action/prepare, current, point-basis, factor or solver is invoked.
Future containing callers own natural closure authentication and publication.
"""
COEFFICIENT_FORWARD_AUTHOR_DRAFT=True
COEFFICIENT_FORWARD_AUTHORING_IN_PROGRESS=False
COEFFICIENT_FORWARD_SOURCE=(None,None)
COEFFICIENT_FORWARD_RESULT=(None,None,None)
COEFFICIENT_FORWARD_RECEIPT=(None,None,None)
COEFFICIENT_FORWARD_PROOF=(None,None,None)

def cpf_pair(name,x,keep,shape=None):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
 keep(name+'_both_words',np.stack(x).copy())
 for word,a in zip(('hi','lo'),x):
  keep(name+'_'+word,np.asarray(a).copy())
  assert a.dtype==np.float64 and np.all(np.isfinite(a)),name
  if shape is not None:assert a.shape==shape,name
 return x

def cpf_matvec(A,x,keep,label):
 assert A[0].shape==A[1].shape and x[0].shape==x[1].shape and A[0].shape[-1]==x[0].shape[-1]
 terms=cpf_pair(label+'_all_products',P.a_mul(A,tuple(a[...,None,:] for a in x)),keep,A[0].shape)
 out=P.a_dd(np.zeros(A[0].shape[:-1]))
 for column in range(A[0].shape[-1]):
  out=cpf_pair(label+'_column%d_partial'%column,P.a_add(out,P.a_slice(terms,(Ellipsis,column))),keep,A[0].shape[:-1])
 return out

def prepare_candidate_mechanical_coefficient_forward(chunks,basis,closed,keep,label):
 assert not COEFFICIENT_FORWARD_AUTHOR_DRAFT and not COEFFICIENT_FORWARD_AUTHORING_IN_PROGRESS
 for key,ref in (('source',COEFFICIENT_FORWARD_SOURCE),('result',COEFFICIENT_FORWARD_RESULT),('receipt',COEFFICIENT_FORWARD_RECEIPT),('proof',COEFFICIENT_FORWARD_PROOF)):
  assert all(x is not None for x in ref) and tuple(closed[key])==ref,'Authentic future closed coefficient packet required'
 assert closed['naturally_closed'] is True and closed['natural_exit_code']==0 and closed['all_selected_seals_verified'] is True and closed['physical_adoption'] is False
 assert len(closed['same_candidate_provenance'])==4 and len(chunks)==120
 assert basis['closed_provenance'],'Authentic original basis association required'
 for n,shape in (('R',(4,3784)),('dv',(4,3784)),('hats',(4,4,3,86,44))):
  keep(label+'_original_basis_'+n,np.asarray(basis[n]).copy());assert basis[n].shape==shape and basis[n].dtype==np.float64 and np.all(np.isfinite(basis[n]))
 assert np.all(basis['R']>0) and np.all(basis['dv']>0)
 for serial,d in enumerate(chunks):
  iq,lo=serial//30,(serial%30)*128;hi=min(lo+128,3784)
  assert (d['column'],d['lo'],d['hi'])==(iq,lo,hi) and d['same_candidate_provenance']==closed['same_candidate_provenance'][iq]
  assert d['point_block_ref'] and d['committed_original_point'] and d['basis_provenance']==basis['closed_provenance']
  assert set(d['selected_names'])=={'H','B','E','D','eH','eB','eE','eD'}
  for n in ('H','B','E','D'):assert len(d['selected_names'][n])==2 and all(isinstance(key,str) for key in d['selected_names'][n]) and isinstance(d['selected_names']['e'+n],str)
 return dict(chunks=list(chunks),basis={n:basis[n].copy() for n in ('R','dv','hats')},closed=closed,
             basis_provenance=basis['closed_provenance'],
             coefficient_forward_only=True,original_coordinates=403340,authoritative147_association_measured=False,
             uniform_DD_linearity_or_adjoint_qualified=False,global_inverse_qualified=False,physical_adoption=False)

def candidate_paired_arrowhead_forward(block,native,metric,keep,label):
 p=metric[0].shape[0];cpf_pair(label+'_native_physical_input',native,keep,(33,p,3));cpf_pair(label+'_metric_physical_input',metric,keep,(p,6))
 for n,shape in dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3)).items():cpf_pair(label+'_saved_'+n,block[n],keep,shape)
 head=cpf_pair(label+'_head_input',tuple(np.concatenate((native[w][0],metric[w]),axis=1) for w in (0,1)),keep,(p,9));arms=P.a_slice(native,slice(1,None))
 h=cpf_matvec(block['H'],head,keep,label+'_H');b=cpf_matvec(block['B'],arms,keep,label+'_B')
 for mode in range(32):h=cpf_pair(label+'_head_through_mode%d'%mode,P.a_add(h,P.a_slice(b,mode)),keep,(p,9))
 e=cpf_matvec(block['E'],tuple(w[None] for w in head),keep,label+'_E');d=cpf_matvec(block['D'],arms,keep,label+'_D')
 arm=cpf_pair(label+'_arm_output',P.a_add(e,d),keep,(32,p,3))
 u=P.a_slice(h,(slice(None),slice(0,3)));m=P.a_slice(h,(slice(None),slice(3,None)))
 return cpf_pair(label+'_native_output',tuple(np.concatenate((u[w][None],arm[w]),axis=0) for w in (0,1)),keep,(33,p,3)),cpf_pair(label+'_metric_output',m,keep,(p,6))

def candidate_measured_coefficient_fullweak_forward(prepared,x,read_closed_chunk,keep,label,chunk_complete,column_complete):
 assert prepared['coefficient_forward_only'] is True and prepared['physical_adoption'] is False
 assert callable(read_closed_chunk) and callable(chunk_complete) and callable(column_complete),'Containing consumer seals every completed chunk and column'
 cpf_pair(label+'_original_packed_direction',x,keep,(403340,));fields=[P.unpack_fields(a,False) for a in x]
 native=tuple(q[0] for q in fields);metric=tuple(q[1] for q in fields);nm=np.broadcast_to(P.native_mask(),(33,3,87,45));mm=P.metric_mask()
 for n,pair,mask in (('native',native,nm),('metric',metric,mm)):
  cpf_pair(label+'_original_'+n+'_nodes',pair,keep);assert all(np.all(a[~mask]==0) for a in pair)
 basis=prepared['basis'];nv=cpf_pair(label+'_original_E_native_value_lift',P.dd_native_node_value(native,basis,keep,jet=0),keep,(33,15136,3))
 mv=cpf_pair(label+'_original_E_metric_physical_value_lift',P.dd_metric_node_value(metric,basis,keep,jet=0),keep,(15136,6))
 no=P.a_dd(np.zeros((33,15136,3)));mo=P.a_dd(np.zeros((15136,6)));chunks=[];columns=[]
 for descriptor in prepared['chunks']:
  iq,lo,hi=(descriptor[n] for n in ('column','lo','hi'));sl=slice(iq*3784+lo,iq*3784+hi)
  block=read_closed_chunk(descriptor,('H','B','E','D'))
  assert block['record']==descriptor['point_block_ref'] and block['source_provenance']==descriptor['same_candidate_provenance']
  part=candidate_paired_arrowhead_forward(block['paired_raw'],P.a_slice(nv,(slice(None),sl)),P.a_slice(mv,sl),keep,label+'_q%d_chunk%d_K'%(iq,lo))
  for w in (0,1):no[w][:,sl]=part[0][w];mo[w][sl]=part[1][w]
  ref=chunk_complete(descriptor,part);assert isinstance(ref,dict) and all(ref.get(k) for k in ('file','sha256','commit_file','commit_sha256'));chunks.append(ref)
  if hi==3784:
   col=slice(iq*3784,(iq+1)*3784);n=cpf_pair(label+'_completed_column%d_native'%iq,tuple(a[:,col].copy() for a in no),keep,(33,3784,3));m=cpf_pair(label+'_completed_column%d_metric'%iq,tuple(a[col].copy() for a in mo),keep,(3784,6))
   ref=column_complete(iq,dict(point_native=n,point_metric=m,chunk_refs=chunks[-30:],same_candidate_provenance=prepared['closed']['same_candidate_provenance'][iq],coefficient_proxy_only=True,physical_adoption=False));assert isinstance(ref,dict) and all(ref.get(k) for k in ('file','sha256','commit_file','commit_sha256'));columns.append(ref)
 cpf_pair(label+'_completed_native_point',no,keep,(33,15136,3));cpf_pair(label+'_completed_metric_point',mo,keep,(15136,6))
 wn=cpf_pair(label+'_original_S_native_weak',P.dd_native_scatter(no,basis,keep),keep,(33,3,87,45));wm=cpf_pair(label+'_original_S_metric_weak',P.dd_metric_scatter(mo,basis,keep),keep,(6,87,45))
 assert all(np.all(a[~nm]==0) for a in wn) and all(np.all(a[~mm]==0) for a in wm)
 packed=cpf_pair(label+'_original_packed_Ahat',P.pack_dd(wn,wm),keep,(403340,))
 return dict(packed=packed,weak=dict(native=wn,metric=wm),chunk_refs=chunks,column_refs=columns,
             operator='original_S_directed_saved_K_original_E',coefficient_forward_only=True,
             authoritative147_whole_correction_required=True,original_six_canonical_gates_evaluated=False,
             old_147_or_point_basis_or_current_or_factor_action_replayed=False,
             uniform_association_or_adjoint_or_inverse_qualified=False,physical_adoption=False)

def candidate_fullweak_coefficient_forward_positive(prepared,x,read_closed_chunk,keep,label,chunk_complete,column_complete):
 assert prepared['coefficient_forward_only'] is True and prepared['physical_adoption'] is False
 assert callable(read_closed_chunk) and callable(chunk_complete) and callable(column_complete)
 cpf_pair(label+'_supplied_original_direction',x,keep,(403340,));mag=mp_add(abs(x[0]),abs(x[1]),keep,label+'_word_magnitude')
 native,metric,_=P.unpack_fields(mag,False);basis=prepared['basis']
 nv,mv=candidate_mechanical_positive_lift(native,metric,basis,keep,label+'_original124_E_bound')
 no=np.zeros((33,15136,3));mo=np.zeros((15136,6));chunks=[];columns=[]
 for descriptor in prepared['chunks']:
  iq,lo,hi=(descriptor[n] for n in ('column','lo','hi'));sl=slice(iq*3784+lo,iq*3784+hi);p=hi-lo
  block=read_closed_chunk(descriptor,('H','B','E','D','eH','eB','eE','eD'));e={}
  assert block['record']==descriptor['point_block_ref'] and block['source_provenance']==descriptor['same_candidate_provenance']
  for n,shape in dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3)).items():
   pair=cpf_pair(label+'_saved_'+n,block['paired_raw'][n],keep,shape);a=np.asarray(block['operation_envelopes'][n])
   keep(label+'_saved_padded_point_e'+n,a.copy());assert a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(a>=0)
   assert np.all(a>=mp_add(abs(pair[0]),abs(pair[1]),keep,label+'_represented_pair_magnitude_'+n)),'Actual padded point coefficient bound required'
   e[n]=a
  head=np.concatenate((nv[0,sl],mv[sl]),axis=1);arms=nv[1:,sl]
  h=mp_mv(e['H'],head,keep,label+'_H_bound');b=mp_mv(e['B'],arms,keep,label+'_B_bound')
  for mode in range(32):h=mp_add(h,b[mode],keep,label+'_mode%d_head_bound'%mode)
  a=mp_add(mp_mv(e['E'],head[None],keep,label+'_E_bound'),mp_mv(e['D'],arms,keep,label+'_D_bound'),keep,label+'_arms_bound')
  n=np.concatenate((h[:,:3][None],a),axis=0);m=h[:,3:];keep(label+'_completed_chunk_native_bound',n.copy());keep(label+'_completed_chunk_metric_bound',m.copy())
  assert np.all(np.isfinite(n)) and np.all(n>=0) and np.all(np.isfinite(m)) and np.all(m>=0)
  no[:,sl]=n;mo[sl]=m;ref=chunk_complete(descriptor,(n,m));assert isinstance(ref,dict) and all(ref.get(k) for k in ('file','sha256','commit_file','commit_sha256'));chunks.append(ref)
  if hi==3784:
   col=slice(iq*3784,(iq+1)*3784);n=no[:,col].copy();m=mo[col].copy();keep(label+'_completed_column%d_native_bound'%iq,n.copy());keep(label+'_completed_column%d_metric_bound'%iq,m.copy())
   ref=column_complete(iq,dict(point_native=n,point_metric=m,chunk_refs=chunks[-30:],same_candidate_provenance=prepared['closed']['same_candidate_provenance'][iq],represented_coefficient_enclosure_only=True,physical_adoption=False));assert isinstance(ref,dict) and all(ref.get(k) for k in ('file','sha256','commit_file','commit_sha256'));columns.append(ref)
 keep(label+'_completed_native_point_bound',no.copy());keep(label+'_completed_metric_point_bound',mo.copy())
 wn,wm=candidate_mechanical_positive_scatter(no,mo,basis,keep,label+'_original124_S_bound')
 out=P.pack_fields(wn,wm);keep(label+'_original_packed_Ahat_outward_envelope',out.copy());assert out.shape==(403340,) and np.all(np.isfinite(out)) and np.all(out>=0)
 return dict(packed=out,weak=dict(native=wn,metric=wm),chunk_refs=chunks,column_refs=columns,
             original124_outward_primitives_and_maps=True,nodal_factor_envelope_substituted=False,
             represented_coefficient_enclosure_only=True,authoritative147_association_bound_earned=False,
             uniform_inverse_or_physical_adoption=False,physical_adoption=False)
