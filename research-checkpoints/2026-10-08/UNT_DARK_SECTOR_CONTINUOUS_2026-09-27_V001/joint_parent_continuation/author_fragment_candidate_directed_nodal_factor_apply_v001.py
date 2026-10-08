"""HELD full independent-node directed factor apply and supplied adjoint.
Definitions only; globals np,P. The containing caller authenticates CLOSED
198 numerical factors/COMMITs/proof and all source pins before hydration.
P supplies repaired paired arithmetic plus original pack_fields/unpack_fields,
native_mask/metric_mask. No basis, action, inverse, factor or solver is replayed.
"""
NODAL_FACTOR_APPLY_AUTHOR_DRAFT=True
NODAL_FACTOR_APPLY_AUTHORING_IN_PROGRESS=False
NODAL_FACTOR_SOURCE=(None,None)
NODAL_FACTOR_RESULT=(None,None,None)
NODAL_FACTOR_RECEIPT=(None,None,None)
NODAL_FACTOR_CLOSURE_PROOF=(None,None,None)
NODAL_FACTOR_APPLY_SOURCE_PINS={
 'author_fragment_candidate_directed_nodal_arrowhead_v001.py':'0a05eacd67d3093e2328c7197cdfb257488771ec7e0078b77a972340ef662bb6',
 'author_fragment_candidate_modal_head_factor_apply_v001.py':'deb543e9dea46717b991c84fbb4241e388896231018d9b90f885260739fb6817',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py':'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235'}

def nfa_pair(name,x,shape,keep):
 assert isinstance(x,tuple) and len(x)==2
 keep(name+'_both_words',np.stack(x).copy())
 assert all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x),name
 for word,a in zip(('hi','lo'),x):keep(name+'_'+word,a.copy())
 return x

def nfa_positive(name,a,keep):
 keep(name,np.asarray(a).copy());assert a.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(a>=0),name;return a

def nfa_matvec(A,x,ex,keep,label):
 assert A[0].shape==A[1].shape and x[0].shape==x[1].shape==ex.shape
 assert A[0].shape[:-2]==x[0].shape[:-1] and A[0].shape[-1]==x[0].shape[-1]
 terms=nfa_pair(label+'_all_products',P.a_mul(A,(x[0][...,None,:],x[1][...,None,:])),A[0].shape,keep)
 out=P.a_dd(np.zeros(A[0].shape[:-1]))
 for column in range(A[0].shape[-1]):
  term=P.a_slice(terms,(Ellipsis,column));nfa_pair(label+'_column%d_product'%column,term,out[0].shape,keep)
  out=nfa_pair(label+'_column%d_partial'%column,P.a_add(out,term),out[0].shape,keep)
 bound=nfa_positive(label+'_positive_operation_envelope',(1+128*np.finfo(np.float64).eps)*np.matmul(abs(A[0])+abs(A[1]),ex[...,None])[...,0],keep)
 return out,bound

def prepare_candidate_directed_nodal_factor_apply(factors,keep,label):
 assert isinstance(factors['closed_provenance'],dict) and factors['closed_provenance'] and factors['all_active_factor_seals_verified'] is True
 assert factors['active_node_count']==3870 and factors['right_preconditioner_factor_resolved'] is True
 assert factors['sheet_head_dimension']==6 and factors['sheet_arm_dimension']==2 and factors['interior_head_dimension']==9 and factors['interior_arm_dimension']==3
 assert factors['nodal_apply_or_weak_functional_qualified'] is False and factors['full_weak_or_global_inverse_qualified'] is False and factors['physical_adoption'] is False
 nm=P.native_mask();mm=P.metric_mask();en=np.ones((3,87,45),dtype=bool);em=np.ones((6,87,45),dtype=bool);en[:,0]=False;en[1,:,0]=False;em[:,0]=False;em[3:5,:,0]=False
 keep(label+'_original_native_mask',nm.copy());keep(label+'_original_metric_mask',mm.copy());assert np.array_equal(nm,en) and np.array_equal(mm,em)
 assert np.count_nonzero(np.broadcast_to(nm,(33,3,87,45)))==380292 and np.count_nonzero(mm)==23048
 sheet=np.arange(0,3870,45,dtype=np.int64);am=np.ones((3870,3),dtype=bool);hm=np.ones((3870,9),dtype=bool);am[sheet,1]=False;hm[np.ix_(sheet,(1,6,7))]=False
 keep(label+'_independent_sheet_node_ids',sheet.copy());keep(label+'_active_arm_mask',am.copy());keep(label+'_active_head_mask',hm.copy())
 masks=dict(D_inverse=am[None,:,:,None]&am[None,:,None,:],S_inverse=hm[:,:,None]&hm[:,None,:],B=hm[None,:,:,None]&am[None,:,None,:],E=am[None,:,:,None]&hm[None,:,None,:])
 shapes=dict(D_inverse=(32,3870,3,3),S_inverse=(3870,9,9),B=(32,3870,9,3),E=(32,3870,3,9));prepared={}
 for n,shape in shapes.items():
  x=nfa_pair(label+'_closed_'+n,tuple(a.copy() for a in factors[n]),shape,keep);valid=np.broadcast_to(masks[n],shape)
  assert all(np.all(a[~valid]==0) for a in x),'Inactive coordinate must be zero: '+n
  for a in x:a.flags.writeable=False
  prepared[n]=x
 return dict(prepared,closed_provenance=dict(factors['closed_provenance']),native_mask=nm.copy(),metric_mask=mm.copy(),active_arm_mask=am,active_head_mask=hm,
             original_independent_dofs=403340,full_signed_directed_factors=True,coefficient_space='original native33x3 plus metric(a,b,c,d,e,f) nodal coordinates',
             factor_scope='resolved approximate real numerical self factors; original paired weak67 remains authority',
             represented_factor_apply_or_adjoint_qualified=False,uniform_all_input_DD_linearity_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)

def nfa_unpack(x,prepared,keep,label):
 nfa_pair(label+'_original_packed_words',x,(403340,),keep);native=[];metric=[]
 for word,a in enumerate(x):
  v,k,lam=P.unpack_fields(a,False);assert lam is None
  keep(label+'_unpacked_native_word%d'%word,v.copy());keep(label+'_unpacked_metric_coefficients_word%d'%word,k.copy())
  assert np.all(v[~np.broadcast_to(prepared['native_mask'],v.shape)]==0) and np.all(k[~prepared['metric_mask']]==0)
  native.append(v[:,:,1:,:].reshape(33,3,3870).transpose(0,2,1).copy());metric.append(k[:,1:,:].reshape(6,3870).T.copy())
 head=P.a_stack([P.a_slice(tuple(native),(0,slice(None),i)) for i in range(3)]+[P.a_slice(tuple(metric),(slice(None),i)) for i in range(6)],-1)
 arms=tuple(a[1:].copy() for a in native);nfa_pair(label+'_head_nodal_coefficient_RHS',head,(3870,9),keep);nfa_pair(label+'_modal_RHS',arms,(32,3870,3),keep)
 return head,arms

def nfa_pack(head,arms,prepared,keep,label):
 nfa_pair(label+'_head_nodal_coefficient_solution',head,(3870,9),keep);nfa_pair(label+'_modal_solution',arms,(32,3870,3),keep);packed=[]
 assert all(np.all(a[~prepared['active_head_mask']]==0) for a in head) and all(np.all(a[:,~prepared['active_arm_mask']]==0) for a in arms)
 for word in (0,1):
  v=np.zeros((33,3,87,45));k=np.zeros((6,87,45));v[0,:,1:,:]=head[word][:,:3].T.reshape(3,86,45);v[1:,:,1:,:]=arms[word].transpose(0,2,1).reshape(32,3,86,45);k[:,1:,:]=head[word][:,3:].T.reshape(6,86,45)
  keep(label+'_native_node_word%d'%word,v.copy());keep(label+'_metric_coefficient_node_word%d'%word,k.copy())
  assert np.all(v[~np.broadcast_to(prepared['native_mask'],v.shape)]==0) and np.all(k[~prepared['metric_mask']]==0)
  packed.append(P.pack_fields(v,k))
 return nfa_pair(label+'_original_packed_solution',tuple(packed),(403340,),keep)

def nfa_apply(prepared,x,keep,label,adjoint):
 assert isinstance(adjoint,bool) and prepared['original_independent_dofs']==403340 and prepared['full_signed_directed_factors'] is True
 assert prepared['closed_provenance'] and prepared['represented_factor_apply_or_adjoint_qualified'] is False and prepared['full_weak_or_global_inverse_qualified'] is False and prepared['physical_adoption'] is False
 head_rhs,arm_rhs=nfa_unpack(x,prepared,keep,label);DI,J,B,E=[prepared[n] for n in ('D_inverse','S_inverse','B','E')]
 if adjoint:
  DI=tuple(a.swapaxes(-1,-2) for a in DI);J=tuple(a.swapaxes(-1,-2) for a in J);B,E=tuple(a.swapaxes(-1,-2) for a in E),tuple(a.swapaxes(-1,-2) for a in B)
 eh=nfa_positive(label+'_head_RHS_word_magnitude',abs(head_rhs[0])+abs(head_rhs[1]),keep);ea=nfa_positive(label+'_arm_RHS_word_magnitude',abs(arm_rhs[0])+abs(arm_rhs[1]),keep)
 free,efree=nfa_matvec(DI,arm_rhs,ea,keep,label+'_free_arms');reduced=head_rhs;er=eh.copy();inflate=1+128*np.finfo(np.float64).eps
 for mode in range(32):
  contribution,eb=nfa_matvec(P.a_slice(B,mode),P.a_slice(free,mode),efree[mode],keep,label+'_mode%02d_head_reaction'%mode)
  reduced=nfa_pair(label+'_mode%02d_reduced_head'%mode,P.a_sub(reduced,contribution),(3870,9),keep);er=nfa_positive(label+'_mode%02d_reduced_head_positive'%mode,inflate*(er+eb),keep)
 head,ehead=nfa_matvec(J,reduced,er,keep,label+'_head_solution');arms=P.a_dd(np.zeros((32,3870,3)));earms=np.zeros((32,3870,3))
 for mode in range(32):
  reaction,ecr=nfa_matvec(P.a_slice(E,mode),head,ehead,keep,label+'_mode%02d_arm_reaction'%mode)
  corrected=nfa_pair(label+'_mode%02d_corrected_arm_RHS'%mode,P.a_sub(P.a_slice(arm_rhs,mode),reaction),(3870,3),keep);ec=nfa_positive(label+'_mode%02d_corrected_arm_positive'%mode,inflate*(ea[mode]+ecr),keep)
  result,eresult=nfa_matvec(P.a_slice(DI,mode),corrected,ec,keep,label+'_mode%02d_arm_solution'%mode)
  for word in (0,1):arms[word][mode]=result[word]
  earms[mode]=eresult;nfa_pair(label+'_completed_arm_inventory',arms,(32,3870,3),keep);nfa_positive(label+'_completed_arm_positive_inventory',earms,keep)
 out=nfa_pack(head,arms,prepared,keep,label)
 bound=nfa_pack(P.a_dd(ehead),P.a_dd(earms),prepared,keep,label+'_positive_polynomial')[0];nfa_positive(label+'_packed_positive_operation_envelope',bound,keep)
 return out

def candidate_directed_nodal_factor_apply(prepared,x,keep,label):
 return nfa_apply(prepared,x,keep,label,False)

def candidate_directed_nodal_factor_adjoint(prepared,x,keep,label):
 return nfa_apply(prepared,x,keep,label,True)
