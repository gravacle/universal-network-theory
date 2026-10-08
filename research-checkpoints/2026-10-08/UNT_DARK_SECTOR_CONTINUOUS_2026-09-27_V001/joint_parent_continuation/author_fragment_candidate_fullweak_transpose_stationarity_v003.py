"""HELD streamed paired point-coefficient transpose and stationarity bridge.
Definitions only; globals np,P. A=S K E, hence coefficient A*=E* K* S*.
The containing caller authenticates all120 completed paired H/B/E/D chunks,
their same-candidate cache/basis and natural terminal before any reader call.
No point action, current producer, factor application or adjoint solver is run.
The measured-coefficient association with authoritative147/67 must be checked
by a NEW fullweak pairing contact; this source does not assume it is exact.
"""
FULLWEAK_TRANSPOSE_AUTHOR_DRAFT=True
FULLWEAK_TRANSPOSE_AUTHORING_IN_PROGRESS=False
FULLWEAK_TRANSPOSE_SOURCE=(None,None)
FULLWEAK_TRANSPOSE_RESULT=(None,None)
FULLWEAK_TRANSPOSE_RECEIPT=(None,None)
FULLWEAK_TRANSPOSE_PROOF=(None,None)

def ct_pair(name,x,keep):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
 keep(name+'_both_words',np.stack(x).copy())
 for suffix,a in zip(('hi','lo'),x):
  keep(name+'_'+suffix,np.asarray(a).copy());assert a.dtype==np.float64 and np.all(np.isfinite(a)),name
 return x

def ct_matvec(A,x,keep,label):
 assert A[0].shape==A[1].shape and x[0].shape==x[1].shape and A[0].shape[-1]==x[0].shape[-1]
 terms=ct_pair(label+'_all_product_terms',P.a_mul((A[0],A[1]),(x[0][...,None,:],x[1][...,None,:])),keep)
 out=P.a_dd(np.zeros(terms[0].shape[:-1]))
 for k in range(terms[0].shape[-1]):out=ct_pair(label+'_through%d'%k,P.a_add(out,P.a_slice(terms,(Ellipsis,k))),keep)
 return out

def prepare_candidate_fullweak_transpose(chunks,basis,closed,keep,label):
 assert not FULLWEAK_TRANSPOSE_AUTHOR_DRAFT and not FULLWEAK_TRANSPOSE_AUTHORING_IN_PROGRESS
 refs=(FULLWEAK_TRANSPOSE_SOURCE,FULLWEAK_TRANSPOSE_RESULT,FULLWEAK_TRANSPOSE_RECEIPT,FULLWEAK_TRANSPOSE_PROOF)
 assert all(x is not None for ref in refs for x in ref),'Authentic natural closure required before I/O'
 assert [closed[n] for n in ('source','result','receipt','proof')]==list(refs)
 assert closed['naturally_closed'] is True and closed['natural_exit_code']==0 and closed['all_selected_seals_verified'] is True
 assert closed['physical_adoption'] is False and closed['same_candidate_provenance']
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert np.all(basis['R']>0) and np.all(basis['dv']>0) and basis['closed_provenance']
 expected=[(iq,lo,min(lo+128,3784)) for iq in range(4) for lo in range(0,3784,128)]
 assert len(chunks)==len(expected)==120
 for descriptor,(iq,lo,hi) in zip(chunks,expected):
  assert (descriptor['column'],descriptor['lo'],descriptor['hi'])==(iq,lo,hi)
  assert descriptor['point_block_ref'] and descriptor['same_candidate_provenance']==closed['same_candidate_provenance'][iq]
  assert descriptor['basis_provenance']==basis['closed_provenance']
 copied={n:np.asarray(basis[n]).copy() for n in ('R','dv','hats')}
 for n,a in copied.items():keep(label+'_original_basis_'+n,a.copy())
 return dict(chunks=list(chunks),basis=copied,closed=closed,physical_adoption=False,
             coefficient_transpose_only=True,authoritative147_association_measured=False,global_inverse_qualified=False)

def candidate_original_scatter_transpose(x,basis,keep,label):
 assert x[0].shape==x[1].shape==(403340,);ct_pair(label+'_supplied_packed_dual',x,keep)
 nh,mh,_=P.unpack_fields(x[0],False);nl,ml,_=P.unpack_fields(x[1],False)
 n=ct_pair(label+'_native_lift',(P.lift_velocity(nh),P.lift_velocity(nl)),keep)
 m=ct_pair(label+'_metric_lift',(P.lift_metric(mh),P.lift_metric(ml)),keep)
 no=P.a_dd(np.zeros((33,4,86,44,3)));mo=P.a_dd(np.zeros((4,86,44,6)))
 for iq in range(4):
  R=basis['R'][iq].reshape(86,44);weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44);F=P.dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=basis['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
   nv=tuple(np.moveaxis(n[w][:,:,di:86+di,dj:44+dj],1,-1) for w in (0,1))
   term=ct_pair(label+'_native_factor_product',P.a_mul64(factor,nv),keep)
   term=ct_pair(label+'_native_weight_product',P.a_mul64(weight[...,None],term),keep)
   out=P.a_add(P.a_slice(no,(slice(None),iq)),term)
   for w in (0,1):no[w][:,iq]=out[w]
   ct_pair(label+'_native_partial',no,keep)
   mv=tuple(np.moveaxis(m[w][:,di:86+di,dj:44+dj],0,-1) for w in (0,1))
   term=ct_pair(label+'_metric_hat_product',P.a_mul64(hat[...,None],mv),keep)
   term=ct_pair(label+'_metric_weight_product',P.a_mul64(weight[...,None],term),keep)
   term=ct_pair(label+'_metric_F_product',P.a_matvec(F,term),keep)
   out=P.a_add(P.a_slice(mo,iq),term)
   for w in (0,1):mo[w][iq]=out[w]
   ct_pair(label+'_metric_partial',mo,keep)
 return ct_pair(label+'_native_point',P.a_reshape(no,(33,15136,3)),keep),ct_pair(label+'_metric_point',P.a_reshape(mo,(15136,6)),keep)

def candidate_paired_arrowhead_transpose(block,native,metric,keep,label):
 p=metric[0].shape[0];assert native[0].shape==native[1].shape==(33,p,3) and metric[0].shape==metric[1].shape==(p,6)
 shapes=dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3))
 for name,shape in shapes.items():assert block[name][0].shape==block[name][1].shape==shape;ct_pair(label+'_saved_'+name,block[name],keep)
 head=ct_pair(label+'_head_dual',tuple(np.concatenate((native[w][0],metric[w]),axis=1) for w in (0,1)),keep)
 arms=P.a_slice(native,slice(1,None));transpose=lambda a:tuple(w.swapaxes(-1,-2) for w in a)
 h=ct_matvec(transpose(block['H']),head,keep,label+'_Hstar')
 e=ct_matvec(transpose(block['E']),arms,keep,label+'_Estar')
 for mode in range(32):h=ct_pair(label+'_head_through_mode%d'%mode,P.a_add(h,P.a_slice(e,mode)),keep)
 arm=ct_pair(label+'_arm_result',P.a_add(ct_matvec(transpose(block['B']),tuple(w[None] for w in head),keep,label+'_Bstar'),ct_matvec(transpose(block['D']),arms,keep,label+'_Dstar')),keep)
 u=P.a_slice(h,(slice(None),slice(0,3)));m=P.a_slice(h,(slice(None),slice(3,None)))
 n=ct_pair(label+'_native_result',tuple(np.concatenate((u[w][None],arm[w]),axis=0) for w in (0,1)),keep)
 return n,ct_pair(label+'_metric_result',m,keep)

def candidate_original_evaluation_transpose(n,m,basis,keep,label):
 assert n[0].shape==n[1].shape==(33,15136,3) and m[0].shape==m[1].shape==(15136,6)
 nf=P.a_reshape(n,(33,4,86,44,3));mf=P.a_reshape(m,(4,86,44,6))
 no=P.a_dd(np.zeros((33,3,87,45)));mo=P.a_dd(np.zeros((6,87,45)))
 for iq in range(4):
  R=basis['R'][iq].reshape(86,44);F=P.dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=basis['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   term=ct_pair(label+'_native_corner_product',P.a_transpose(P.a_mul64(factor,P.a_slice(nf,(slice(None),iq))),(0,3,1,2)),keep)
   key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj));out=P.a_add(P.a_slice(no,key),term)
   for w in (0,1):no[w][key]=out[w]
   ct_pair(label+'_native_partial',no,keep)
   Fhat=hat[...,None,None]*F;term=ct_pair(label+'_metric_rounded_Fhat_product',P.a_transpose(P.a_matvec(Fhat.swapaxes(-1,-2),P.a_slice(mf,iq)),(2,0,1)),keep)
   key=(slice(None),slice(di,86+di),slice(dj,44+dj));out=P.a_add(P.a_slice(mo,key),term)
   for w in (0,1):mo[w][key]=out[w]
   ct_pair(label+'_metric_partial',mo,keep)
 for component in (1,2):
  out=P.a_add(P.a_slice(no,(slice(None),component,1,slice(None))),P.a_slice(no,(slice(None),component,0,slice(None))))
  for w in (0,1):no[w][:,component,1]=out[w]
  ct_pair(label+'_native_axis_fold',no,keep)
 for w in (0,1):no[w][:,:,0]=0;no[w][:,1,:,0]=0
 out=P.a_add(P.a_slice(mo,(slice(None),1,slice(None))),P.a_slice(mo,(slice(None),0,slice(None))))
 for w in (0,1):mo[w][:,1]=out[w];mo[w][:,0]=0;mo[w][3:5,:,0]=0
 ct_pair(label+'_native_restricted',no,keep);ct_pair(label+'_metric_restricted',mo,keep)
 return ct_pair(label+'_packed',P.pack_dd(no,mo),keep)

def candidate_measured_coefficient_fullweak_transpose(prepared,dual,read_closed_chunk,keep,label,chunk_complete=None):
 assert callable(read_closed_chunk) and prepared['coefficient_transpose_only'] is True
 n,m=candidate_original_scatter_transpose(dual,prepared['basis'],keep,label+'_Sstar')
 no=P.a_dd(np.zeros((33,15136,3)));mo=P.a_dd(np.zeros((15136,6)));completed=[]
 for descriptor in prepared['chunks']:
  iq,lo,hi=(descriptor[k] for k in ('column','lo','hi'));sl=slice(iq*3784+lo,iq*3784+hi)
  block=read_closed_chunk(descriptor,('H','B','E','D'))
  assert block['source_provenance']==descriptor['same_candidate_provenance'] and block['record']==descriptor['point_block_ref']
  part=candidate_paired_arrowhead_transpose(block['paired_raw'],P.a_slice(n,(slice(None),sl)),P.a_slice(m,sl),keep,label+'_column%d_chunk%d_Kstar'%(iq,lo))
  for w in (0,1):no[w][:,sl]=part[0][w];mo[w][sl]=part[1][w]
  ct_pair(label+'_point_native_partial',no,keep);ct_pair(label+'_point_metric_partial',mo,keep)
  if chunk_complete is not None:completed.append(chunk_complete(descriptor,part))
 result=candidate_original_evaluation_transpose(no,mo,prepared['basis'],keep,label+'_Estar')
 return dict(packed=result,chunk_refs=completed,coefficient_transpose_only=True,
             authoritative147_association_measured=False,nodal110_used_as_operator=False,
             registered_action_gradient_equals_literal_assumed=False,global_inverse_qualified=False,physical_adoption=False)

def candidate_literal_stationarity_bridge(target,current_registered,current_action_gradient,provenance,keep,label):
 assert provenance['same_candidate_and_chart'] is True and provenance['literal_gradient_constructed_independently'] is True
 out={}
 for name,shape in (('mechanical',(403340,)),('phase',(3870,))):
  for family,values in (('target',target),('registered',current_registered),('literal_action_gradient',current_action_gradient)):
   assert values[name][0].shape==values[name][1].shape==shape;ct_pair(label+'_'+family+'_'+name,values[name],keep)
  epsilon=ct_pair(label+'_epsilon_'+name,P.a_sub(target[name],current_registered[name]),keep)
  bridge=ct_pair(label+'_literal_minus_registered_'+name,P.a_sub(current_action_gradient[name],current_registered[name]),keep)
  defect=ct_pair(label+'_true_stationarity_defect_'+name,P.a_sub(epsilon,bridge),keep)
  ct_pair(label+'_direct_defect_bookkeeping_gap_'+name,P.a_sub(defect,P.a_sub(target[name],current_action_gradient[name])),keep)
  out[name]=dict(epsilon=epsilon,action_gradient_bridge=bridge,e_L=defect)
 return dict(groups=out,provenance=provenance,zero_stationarity_assumed=False,physical_adoption=False)

def candidate_legendre_feedback_from_adjoint_groups(lambda_mechanical,lambda_phase,mechanical_mixed_transpose,phase_mixed_transpose,keep,label):
 for name,x,shape in (('mechanical',lambda_mechanical,(403340,)),('phase',lambda_phase,(3870,))):
  assert x[0].shape==x[1].shape==shape;ct_pair(label+'_supplied_adjoint_'+name,x,keep)
 parts=[]
 for name,callback,adjoint in (('mechanical',mechanical_mixed_transpose,lambda_mechanical),('phase',phase_mixed_transpose,lambda_phase)):
  part=callback(adjoint,keep,label+('_Cmechanical_star' if name=='mechanical' else '_Cphase_star'))
  keep(label+'_'+name+'_completed_mixed_weak_and_time_both_words',np.concatenate([np.stack(part[n]).reshape(-1) for n in ('weak_normal','time_coefficient_point')]).copy())
  assert part['gauge_target_derivative_zero'] is True and part['same_candidate_provenance']
  assert part['weak_normal'][0].shape==part['weak_normal'][1].shape==(4,87,45)
  assert part['time_coefficient_point'][0].shape==part['time_coefficient_point'][1].shape==(15136,4)
  ct_pair(label+'_'+name+'_mixed_weak',part['weak_normal'],keep);ct_pair(label+'_'+name+'_mixed_time',part['time_coefficient_point'],keep)
  parts.append(part)
 assert parts[0]['same_candidate_provenance']==parts[1]['same_candidate_provenance']
 weak=ct_pair(label+'_negative_mixed_adjoint_feedback',P.a_mul64(-1.,P.a_add(parts[0]['weak_normal'],parts[1]['weak_normal'])),keep)
 primary=ct_pair(label+'_negative_primary_time_feedback',P.a_mul64(-1.,P.a_add(parts[0]['time_coefficient_point'],parts[1]['time_coefficient_point'])),keep)
 return dict(weak_normal=weak,time_coefficient_point=primary,mixed_parts=parts,
             sign_convention='C=D_gauge_registered_p;epsilon=target-p;feedback=-Cstar_lambda',
             adjoint_equations='Astar_lambda_m=e_L_m;Mstar_lambda_p=e_L_p',
             adjoint_residual_or_bridge_accuracy_qualified=False,CMC_is_separate_constraint=True,physical_adoption=False)


def candidate_fullweak_coefficient_positive(prepared,dual,read_closed_chunk,keep,label):
 # Outward primitives are exact selected mp_add/mul/sum/mv from reviewed124.
 mag=lambda x:mp_add(abs(x[0]),abs(x[1]),keep,label+'_word_magnitude')
 x=mag(dual);assert x.shape==(403340,);nh,mh,_=P.unpack_fields(x,False)
 n=P.lift_velocity(nh);m=P.lift_metric(mh);basis=prepared['basis']
 sn=np.zeros((33,4,86,44,3));sm=np.zeros((4,86,44,6))
 for iq in range(4):
  R=basis['R'][iq].reshape(86,44);weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44);F=P.dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=basis['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
   nv=np.moveaxis(n[:,:,di:86+di,dj:44+dj],1,-1)
   term=mp_mul(abs(factor),nv,keep,label+'_Sstar_native_factor');term=mp_mul(weight[...,None],term,keep,label+'_Sstar_native_weight')
   sn[:,iq]=mp_add(sn[:,iq],term,keep,label+'_Sstar_native_sum')
   mv=np.moveaxis(m[:,di:86+di,dj:44+dj],0,-1)
   term=mp_mul(abs(hat[...,None]),mv,keep,label+'_Sstar_metric_hat');term=mp_mul(weight[...,None],term,keep,label+'_Sstar_metric_weight')
   sm[iq]=mp_add(sm[iq],mp_mv(abs(F),term,keep,label+'_Sstar_metric_F'),keep,label+'_Sstar_metric_sum')
  keep(label+'_Sstar_native_partial',sn.copy());keep(label+'_Sstar_metric_partial',sm.copy())
 sn=sn.reshape(33,15136,3);sm=sm.reshape(15136,6);pn=np.zeros_like(sn);pm=np.zeros_like(sm)
 shapes=lambda p:dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3))
 for descriptor in prepared['chunks']:
  iq,lo,hi=(descriptor[k] for k in ('column','lo','hi'));sl=slice(iq*3784+lo,iq*3784+hi);p=hi-lo
  block=read_closed_chunk(descriptor,('H','B','E','D','eH','eB','eE','eD'))
  assert block['source_provenance']==descriptor['same_candidate_provenance'] and block['record']==descriptor['point_block_ref']
  e={}
  for name,shape in shapes(p).items():
   pair=ct_pair(label+'_positive_saved_pair_'+name,block['paired_raw'][name],keep);a=np.asarray(block['operation_envelopes'][name])
   keep(label+'_positive_saved_outward_e'+name,a.copy())
   assert a.shape==pair[0].shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(a>=0)
   assert np.all(a>=mag(pair)),'Completed outward coefficient enclosure required'
   e[name]=a
  head=np.concatenate((sn[0,sl],sm[sl]),axis=1);arms=sn[1:,sl]
  h=mp_mv(e['H'].swapaxes(-1,-2),head,keep,label+'_Hstar_positive')
  h=mp_add(h,mp_sum(mp_mv(e['E'].swapaxes(-1,-2),arms,keep,label+'_Estar_positive'),0,keep,label+'_Estar_modes'),keep,label+'_head_positive')
  a=mp_add(mp_mv(e['B'].swapaxes(-1,-2),head[None],keep,label+'_Bstar_positive'),mp_mv(e['D'].swapaxes(-1,-2),arms,keep,label+'_Dstar_positive'),keep,label+'_arm_positive')
  pn[:,sl]=np.concatenate((h[:,:3][None],a),axis=0);pm[sl]=h[:,3:]
  keep(label+'_Kstar_native_partial',pn.copy());keep(label+'_Kstar_metric_partial',pm.copy())
 nf=pn.reshape(33,4,86,44,3);mf=pm.reshape(4,86,44,6);no=np.zeros((33,3,87,45));mo=np.zeros((6,87,45))
 for iq in range(4):
  R=basis['R'][iq].reshape(86,44);F=P.dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=basis['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj))
   term=mp_mul(abs(factor),nf[:,iq],keep,label+'_Estar_native_factor').transpose(0,3,1,2);no[key]=mp_add(no[key],term,keep,label+'_Estar_native_sum')
   Fhat=hat[...,None,None]*F;key=(slice(None),slice(di,86+di),slice(dj,44+dj))
   term=mp_mv(abs(Fhat.swapaxes(-1,-2)),mf[iq],keep,label+'_Estar_metric_Fhat').transpose(2,0,1);mo[key]=mp_add(mo[key],term,keep,label+'_Estar_metric_sum')
   keep(label+'_Estar_native_partial',no.copy());keep(label+'_Estar_metric_partial',mo.copy())
 for component in (1,2):no[:,component,1]=mp_add(no[:,component,1],no[:,component,0],keep,label+'_native_axis_fold')
 mo[:,1]=mp_add(mo[:,1],mo[:,0],keep,label+'_metric_axis_fold');no[:,:,0]=0;no[:,1,:,0]=0;mo[:,0]=0;mo[3:5,:,0]=0
 out=P.pack_fields(no,mo);keep(label+'_outward_represented_coefficient_transpose_envelope',out.copy())
 assert out.shape==(403340,) and np.all(np.isfinite(out)) and np.all(out>=0)
 return out


def ct_dot(x,y,keep,label):
 assert x[0].shape==x[1].shape==y[0].shape==y[1].shape==(403340,)
 terms=ct_pair(label+'_product_terms',P.a_mul(x,y),keep)
 while len(terms[0])>1:
  n=len(terms[0]);m=n-n%2
  out=P.a_add((terms[0][:m:2],terms[1][:m:2]),(terms[0][1:m:2],terms[1][1:m:2]))
  if n%2:out=tuple(np.concatenate((out[w],terms[w][-1:])) for w in (0,1))
  terms=ct_pair(label+'_tree_partial',out,keep)
 return ct_pair(label+'_scalar',tuple(np.asarray(a[0]).copy() for a in terms),keep)


def candidate_new_fullweak_transpose_pairing_contact(probe,dual,new_authoritative_forward,transpose_result,forward_operation_envelope,transpose_operation_envelope,provenance,keep,check,label):
 assert provenance['genuinely_NEW_same_candidate_forward_direction'] is True and provenance['old_point_basis_or_action_replayed'] is False
 for n,x in (('probe',probe),('dual',dual),('NEW_authoritative_forward',new_authoritative_forward),('coefficient_transpose',transpose_result)):
  assert x[0].shape==x[1].shape==(403340,);ct_pair(label+'_'+n,x,keep)
 for name,a in (('authoritative_forward_operation_envelope',forward_operation_envelope),('represented_transpose_operation_envelope',transpose_operation_envelope)):
  keep(label+'_'+name,np.asarray(a).copy());assert a.shape==(403340,) and np.all(np.isfinite(a)) and np.all(a>=0)
 left=ct_dot(dual,new_authoritative_forward,keep,label+'_dual_forward');right=ct_dot(probe,transpose_result,keep,label+'_probe_transpose')
 gap=ct_pair(label+'_pairing_and_source_association_gap',P.a_sub(left,right),keep)
 pm=mp_add(abs(probe[0]),abs(probe[1]),keep,label+'_probe_mag');dm=mp_add(abs(dual[0]),abs(dual[1]),keep,label+'_dual_mag')
 products=mp_add(mp_mul(dm,forward_operation_envelope,keep,label+'_forward_bound_products'),mp_mul(pm,transpose_operation_envelope,keep,label+'_transpose_bound_products'),keep,label+'_total_bound_products')
 bound=np.asarray(mp_sum(products,0,keep,label+'_uncancelled_bound')).copy();keep(label+'_uncancelled_bound',bound)
 if bound==0:assert all(np.all(a==0) for a in gap),'Exact both-word zero required with zero envelope'
 check(label,np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),bound)
 return dict(left=left,right=right,gap=gap,envelope=bound,provenance=provenance,
             NEW_direction_pairing_measured=True,all_direction_uniform_adjoint_or_inverse_qualified=False,physical_adoption=False)
