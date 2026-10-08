"""HELD NEW directed candidate nodal moments and active factors; definitions only.
Globals np,P; P exposes repaired paired arithmetic, dd_metric_F and check/TOL.
No import, producer, weak action, solver, eigenvalue or physical-state update.
point_provider supplies NEW same-candidate paired H/B/E/D, real readouts and bounds.
Its paired-to-real/source-association contacts and CLOSED custody remain explicit.
"""
NODAL_ARROWHEAD_AUTHOR_DRAFT=True
NODAL_ARROWHEAD_AUTHORING_IN_PROGRESS=False
NODAL_ARROWHEAD_ALL_FOUR_CLOSED_PROOF=None

def nj_keep(label,a,keep):
 a=np.asarray(a);keep(label,a.copy())
 assert a.dtype==np.float64 and np.all(np.isfinite(a)),label
 return a

def nj_pair(label,x,keep):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
 keep(label+'_both_words',np.stack(x).copy())
 for word,a in zip(('hi','lo'),x):nj_keep(label+'_'+word,a,keep)
 return x

def nj_readout(label,x,keep):
 nj_pair(label+'_paired',x,keep);a=nj_keep(label+'_binary64',x[0]+x[1],keep)
 gap=nj_pair(label+'_pair_minus_readout',P.a_sub(x,P.a_dd(a)),keep)
 error=nj_keep(label+'_conversion_error_upper',(1+64*np.finfo(np.float64).eps)*(abs(gap[0])+abs(gap[1])),keep)
 return a,error

def nj_product(A,B,keep,label):
 assert A[0].shape==A[1].shape and B[0].shape==B[1].shape and A[0].shape[-1]==B[0].shape[-2]
 terms=nj_pair(label+'_all_products',P.a_mul((A[0][..., :, :,None],A[1][..., :, :,None]),(B[0][...,None,:,:],B[1][...,None,:,:])),keep)
 out=P.a_dd(np.zeros(terms[0].shape[:-2]+(terms[0].shape[-1],)))
 for k in range(A[0].shape[-1]):
  out=nj_pair(label+'_through%d'%k,P.a_add(out,P.a_slice(terms,(Ellipsis,k,slice(None)))),keep)
 return out

def nj_identified_maps(R,hat,i,j,corner,keep,label):
 p=len(R);assert R.shape==i.shape==j.shape==(p,) and hat.shape==(4,p)
 offsets=((0,0),(1,0),(0,1),(1,1));di,dj=offsets[corner]
 axis=i==0;valid=np.ones(p,dtype=bool) if corner in (0,2) else ~axis
 node_i=np.maximum(i+di,1);node_j=j+dj;node=(node_i-1)*45+node_j
 keep(label+'_independent_node',node.copy());keep(label+'_corner_valid',valid.copy())
 F=nj_keep(label+'_original_F64',P.dd_metric_F(R),keep)
 native=P.a_dd(np.zeros((p,3)));left=P.a_dd(np.zeros((p,6,6)));right=P.a_dd(np.zeros((p,6,6)))
 en=np.zeros((p,3));el=np.zeros((p,6,6));er=np.zeros((p,6,6))
 sources=(corner,corner+1) if corner in (0,2) else (corner,)
 for ordinal,source in enumerate(sources):
  sdi,sdj=offsets[source];use=valid if ordinal==0 else valid&axis
  h=hat[source];nf=np.broadcast_to(h[:,None],(p,3)).copy();nf[:,2]=R**2*h
  nf[(i+sdi)==0,0]=0;nf[(j+sdj)==0,1]=0;nf[~use]=0
  nj_keep(label+'_source%d_native_factor'%source,nf,keep)
  native=nj_pair(label+'_source%d_native_sum'%source,P.a_add(native,P.a_dd(nf)),keep);en+=abs(nf)
  ml=nj_pair(label+'_source%d_separate_left_product'%source,P.a_prod(h[:,None,None],F),keep)
  mr=nj_keep(label+'_source%d_rounded_right_Fhat'%source,h[:,None,None]*F,keep)
  for word in (0,1):ml[word][~use]=0;ml[word][node_j==0,:,3:5]=0
  mr[~use]=0;mr[node_j==0,:,3:5]=0
  left=nj_pair(label+'_source%d_left_sum'%source,P.a_add(left,ml),keep)
  right=nj_pair(label+'_source%d_right_sum'%source,P.a_add(right,P.a_dd(mr)),keep)
  eb=abs(h[:,None,None])*abs(F);eb[~use]=0;eb[node_j==0,:,3:5]=0;el+=eb;er+=abs(mr)
 n,nerror=nj_readout(label+'_native_alias',native,keep);ml,mlerror=nj_readout(label+'_left_alias',left,keep);mr,mrerror=nj_readout(label+'_right_alias',right,keep)
 nj_pair(label+'_left_minus_right_polynomial',P.a_sub(left,right),keep)
 L=np.zeros((p,9,9));Q=L.copy();eL=L.copy();eQ=L.copy();N=np.zeros((p,3,3));eN=N.copy()
 for k in range(3):N[:,k,k]=n[:,k];eN[:,k,k]=en[:,k]+nerror[:,k]
 L[:,:3,:3]=N;Q[:,:3,:3]=N;L[:,3:,3:]=ml;Q[:,3:,3:]=mr
 eL[:,:3,:3]=eN;eQ[:,:3,:3]=eN;eL[:,3:,3:]=el+mlerror;eQ[:,3:,3:]=er+mrerror
 allowance=1+64*np.finfo(np.float64).eps
 for name,a in (('N',N),('L_head',L),('R_head',Q),('eN',allowance*eN),('eL_head',allowance*eL),('eR_head',allowance*eQ)):
  nj_keep(label+'_'+name,a,keep)
 return dict(node=node,valid=valid,N=N,L=L,R=Q,eN=allowance*eN,eL=allowance*eL,eR=allowance*eQ)

def candidate_nodal_arrowhead_moments(columns,basis,point_provider,keep,chunk_complete,label,chunk_size=128,carry=None):
 assert len(columns)==4 and chunk_size==128 and callable(chunk_complete)
 assert isinstance(basis['closed_provenance'],dict) and basis['closed_provenance']
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert basis['cell_i'].shape==basis['cell_j'].shape==(3784,) and basis['cell_i'].dtype==basis['cell_j'].dtype==np.int64
 assert np.array_equal(basis['cell_i'],np.repeat(np.arange(86),44)) and np.array_equal(basis['cell_j'],np.tile(np.arange(44),86))
 shapes=dict(H=(3870,9,9),B=(32,3870,9,3),E=(32,3870,3,9),D=(32,3870,3,3))
 moments={n:np.zeros(s) for n,s in shapes.items()};bounds={n:np.zeros(s) for n,s in shapes.items()};completed=[];start=0
 if carry is not None:
  assert carry['basis_provenance']==basis['closed_provenance'] and carry['chunk_size']==chunk_size and carry['closed_restore_provenance']
  start=carry['next_chunk'];completed=list(carry['completed_chunk_refs'])
  for n,s in shapes.items():
   moments[n]=nj_keep(label+'_restored_'+n,carry['moments'][n],keep).copy();bounds[n]=nj_keep(label+'_restored_e'+n,carry['bounds'][n],keep).copy()
   assert moments[n].shape==bounds[n].shape==s and np.all(bounds[n]>=0)
 chunks=[(iq,lo,min(lo+chunk_size,3784)) for iq in range(4) for lo in range(0,3784,chunk_size)]
 assert isinstance(start,int) and 0<=start<=len(chunks) and len(completed)==start
 for serial,(iq,lo,hi) in enumerate(chunks):
  if serial<start:continue
  tag=label+'_q%d_chunk%03d'%(iq,serial);assert columns[iq]['closed_candidate_provenance']
  point=point_provider(iq,slice(lo,hi),keep,tag+'_NEW_point');p=hi-lo
  assert point['closed_candidate_provenance']==columns[iq]['closed_candidate_provenance'] and point['construction_contacts'] and point['committed_chunk']
  for n,s in dict(H=(p,9,9),B=(32,p,9,3),E=(32,p,3,9),D=(32,p,3,3)).items():
   pair=nj_pair(tag+'_point_paired_raw_'+n,point['paired_raw'][n],keep);gap=nj_pair(tag+'_point_readout_gap_'+n,point['readout_gaps'][n],keep)
   a=nj_keep(tag+'_point_'+n,point[n],keep);e=nj_keep(tag+'_point_e'+n,point['e'+n],keep)
   assert a.shape==e.shape==pair[0].shape==gap[0].shape==s and np.array_equal(a,pair[0]+pair[1]) and np.all(e>=abs(a)),n
  R=nj_keep(tag+'_original_R',basis['R'][iq,lo:hi],keep);dv=nj_keep(tag+'_original_dv',basis['dv'][iq,lo:hi],keep)
  assert np.all(R>0) and np.all(dv>0);weight=nj_keep(tag+'_original_weight64',dv/R,keep)
  hats=basis['hats'][iq,:,0].reshape(4,3784)[:,lo:hi];i=basis['cell_i'][lo:hi];j=basis['cell_j'][lo:hi];affected=[]
  for corner in range(4):
   maps=nj_identified_maps(R,hats,i,j,corner,keep,tag+'_corner%d'%corner);L,Q,N=maps['L'],maps['R'],maps['N'];eL,eQ,eN=maps['eL'],maps['eR'],maps['eN']
   for n,left,right,el,er in (('H',L,Q,eL,eQ),('B',L,N,eL,eN),('E',N,Q,eN,eQ),('D',N,N,eN,eN)):
    if n=='H':
     term=np.einsum('pai,pab,pbj->pij',left,point[n],right,optimize=True)*weight[:,None,None]
     env=np.einsum('pai,pab,pbj->pij',el,point['e'+n],er,optimize=True)*weight[:,None,None]
    else:
     term=np.einsum('pai,mpab,pbj->mpij',left,point[n],right,optimize=True)*weight[None,:,None,None]
     env=np.einsum('pai,mpab,pbj->mpij',el,point['e'+n],er,optimize=True)*weight[None,:,None,None]
    term=nj_keep(tag+'_corner%d_%s_moment'%(corner,n),term,keep);env=nj_keep(tag+'_corner%d_%s_uncancelled'%(corner,n),(1+128*np.finfo(np.float64).eps)*env,keep)
    assert np.all(env>=0)
    if n=='H':np.add.at(moments[n],maps['node'],term);np.add.at(bounds[n],maps['node'],env)
    else:np.add.at(moments[n],(slice(None),maps['node']),term);np.add.at(bounds[n],(slice(None),maps['node']),env)
   affected.append(maps['node'][maps['valid']])
  nodes=np.unique(np.concatenate(affected));data={}
  for n in shapes:
   key=nodes if n=='H' else (slice(None),nodes)
   data[n]=nj_keep(tag+'_completed_nodes_'+n,moments[n][key],keep).copy();data['e'+n]=nj_keep(tag+'_completed_nodes_e'+n,bounds[n][key],keep).copy()
  ref=chunk_complete(dict(chunk=serial,next_chunk=serial+1,iq=iq,lo=lo,hi=hi,node_ids=nodes.copy(),updated_node_blocks=data,
                          completed_point_blocks=point,committed_point_chunk=point['committed_chunk'],basis_provenance=basis['closed_provenance'],chunk_size=chunk_size))
  assert isinstance(ref,dict) and ref;completed.append(ref)
 return dict(moments=moments,bounds=bounds,completed_chunk_refs=completed,next_chunk=len(chunks),chunk_size=chunk_size,
             basis_provenance=basis['closed_provenance'],full_all_four_sections=True,mode_specific_moments=True,
             real_preconditioner_surrogate=True,authoritative_action='paired_specialized_weak67',global_inverse_qualified=False,physical_adoption=False)

def nj_exact_ldexp(a,exponent,keep,label):
 nj_keep(label+'_original',a,keep);keep(label+'_exponent',np.asarray(exponent).copy())
 with np.errstate(over='ignore',under='ignore',invalid='ignore'):
  scaled=np.ldexp(a,exponent);restored=np.ldexp(scaled,-exponent)
 keep(label+'_scaled_and_restored_attempt',np.stack((scaled,restored)).copy())
 nj_keep(label+'_scaled',scaled,keep);nj_keep(label+'_restored',restored,keep)
 assert np.array_equal(restored.view(np.uint64),a.view(np.uint64)),'Nonexact power-of-two scaling refused'
 return scaled

def nj_active_inverse(A,eA,equilibrate,keep,label):
 nj_keep(label+'_original_matrix',A,keep);nj_keep(label+'_original_uncancelled',eA,keep)
 assert A.shape==eA.shape and A.shape[-1]==A.shape[-2] and A.shape[-1] in (2,3,6,9) and np.all(eA>=0)
 n=A.shape[-1];rows=np.zeros(A.shape[:-1],dtype=np.int64);cols=rows.copy();Ab=A.copy();eb=eA.copy()
 if equilibrate:
  rowmax=nj_keep(label+'_row_maximum',np.max(abs(A),axis=-1),keep);assert np.all(rowmax>0)
  rows=-np.frexp(rowmax)[1].astype(np.int64);first=nj_exact_ldexp(A,rows[..., :,None],keep,label+'_row_equilibration')
  colmax=nj_keep(label+'_column_maximum_after_rows',np.max(abs(first),axis=-2),keep);assert np.all(colmax>0)
  cols=-np.frexp(colmax)[1].astype(np.int64);exponent=rows[..., :,None]+cols[...,None,:]
  Ab=nj_exact_ldexp(A,exponent,keep,label+'_balanced_matrix');eb=nj_exact_ldexp(eA,exponent,keep,label+'_balanced_envelope')
 keep(label+'_row_exponents',rows.copy());keep(label+'_column_exponents',cols.copy())
 identity=np.broadcast_to(np.eye(n),A.shape).copy();Jb=nj_keep(label+'_NEW_numerical_balanced_inverse',np.linalg.solve(Ab,identity),keep)
 left=nj_pair(label+'_balanced_AJ_minus_identity',P.a_sub(nj_product(P.a_dd(Ab),P.a_dd(Jb),keep,label+'_AJ'),P.a_dd(identity)),keep)
 right=nj_pair(label+'_balanced_JA_minus_identity',P.a_sub(nj_product(P.a_dd(Jb),P.a_dd(Ab),keep,label+'_JA'),P.a_dd(identity)),keep)
 eleft=nj_keep(label+'_AJ_positive_envelope',np.matmul(abs(Ab),abs(Jb))+identity,keep);eright=nj_keep(label+'_JA_positive_envelope',np.matmul(abs(Jb),abs(Ab))+identity,keep)
 lr=nj_keep(label+'_AJ_row_sum_readout',np.max(np.sum(abs(left[0])+abs(left[1]),axis=-1),axis=-1),keep)
 rr=nj_keep(label+'_JA_row_sum_readout',np.max(np.sum(abs(right[0])+abs(right[1]),axis=-1),axis=-1),keep)
 eps=np.finfo(np.float64).eps;le=nj_keep(label+'_AJ_envelope_norm',np.max(np.sum(eleft,axis=-1),axis=-1),keep);re=nj_keep(label+'_JA_envelope_norm',np.max(np.sum(eright,axis=-1),axis=-1),keep)
 uncertainty=nj_keep(label+'_paired_product_and_reduction_uncertainty',512*eps**2*np.maximum(le,re),keep)
 r=nj_keep(label+'_two_sided_residual_upper',np.nextafter((1+64*eps)*np.maximum(lr,rr)+uncertainty,np.inf),keep)
 assert float(P.TOL)==2e-11
 P.check(label+'_balanced_AJ_residual',lr,np.zeros_like(lr),le);P.check(label+'_balanced_JA_residual',rr,np.zeros_like(rr),re)
 assert np.all(r<1),'Numerical inverse not resolved'
 perturbation=nj_keep(label+'_inverse_times_construction_envelope',np.max(np.sum(np.matmul(abs(Jb),eb),axis=-1),axis=-1),keep)
 cone=nj_keep(label+'_construction_cone_upper',np.nextafter((1+64*eps)*P.TOL*perturbation/(1-r),np.inf),keep)
 assert np.all(cone<1),'Active coefficient construction is not resolved'
 J=nj_exact_ldexp(Jb,cols[..., :,None]+rows[...,None,:],keep,label+'_physical_inverse')
 return J,dict(balanced_inverse=Jb,row_exponents=rows,column_exponents=cols,two_sided_residual_upper=r,
               construction_cone_upper=cone,norm_convention='declared power-of-two row/column coordinates',
               real_coefficient_inverse_resolved=True,uniform_all_input_DD_inverse_qualified=False)

def candidate_nodal_arrowhead_factors(prepared,keep,node_complete,label,equilibrate=False,carry=None):
 assert prepared['full_all_four_sections'] is True and callable(node_complete) and isinstance(equilibrate,bool)
 moments,bounds=prepared['moments'],prepared['bounds'];DI=np.zeros((32,3870,3,3));J=np.zeros((3870,9,9));completed=[];start=0
 if carry is not None:
  assert carry['completed_moment_refs']==prepared['completed_chunk_refs'] and carry['equilibrated']==equilibrate and carry['closed_restore_provenance']
  DI=nj_keep(label+'_restored_D_inverse',carry['D_inverse_raw'],keep).copy();J=nj_keep(label+'_restored_S_inverse',carry['S_inverse_raw'],keep).copy()
  assert DI.shape==(32,3870,3,3) and J.shape==(3870,9,9)
  start=carry['next_node'];completed=list(carry['completed_node_refs'])
 assert isinstance(start,int) and 0<=start<=3870 and len(completed)==start
 for node in range(start,3870):
  tag=label+'_node%04d'%node;sheet=node%45==0;ai=np.array((0,2) if sheet else (0,1,2));hi=np.array((0,2,3,4,5,8) if sheet else tuple(range(9)))
  keep(tag+'_active_arm',ai.copy());keep(tag+'_active_head',hi.copy())
  d=moments['D'][:,node][:,ai][:,:,ai];ed=bounds['D'][:,node][:,ai][:,:,ai]
  dinv,dinfo=nj_active_inverse(d,ed,equilibrate,keep,tag+'_arms_NEW')
  h=moments['H'][node][np.ix_(hi,hi)];eh=bounds['H'][node][np.ix_(hi,hi)]
  b=moments['B'][:,node][:,hi][:,:,ai];eb=bounds['B'][:,node][:,hi][:,:,ai]
  e=moments['E'][:,node][:,ai][:,:,hi];ee=bounds['E'][:,node][:,ai][:,:,hi]
  reactions=nj_product(nj_product(P.a_dd(b),P.a_dd(dinv),keep,tag+'_B_Dinv'),P.a_dd(e),keep,tag+'_B_Dinv_E')
  reaction_bounds=nj_keep(tag+'_Schur_uncancelled_mode_terms',np.matmul(np.matmul(eb,abs(dinv)),ee),keep)
  s=P.a_dd(h);es=eh.copy()
  for mode in range(32):
   s=nj_pair(tag+'_Schur_through%02d'%mode,P.a_sub(s,P.a_slice(reactions,mode)),keep);es+=reaction_bounds[mode]
   nj_keep(tag+'_Schur_uncancelled_through%02d'%mode,es,keep)
  sraw,sgap=nj_readout(tag+'_Schur_final',s,keep);es=nj_keep(tag+'_Schur_final_envelope',(1+128*np.finfo(np.float64).eps)*es+sgap,keep)
  headinv,hinfo=nj_active_inverse(sraw,es,equilibrate,keep,tag+'_head_NEW')
  for mode in range(32):DI[mode,node][np.ix_(ai,ai)]=dinv[mode]
  J[node][np.ix_(hi,hi)]=headinv
  data=dict(node=node,sheet=bool(sheet),active_arm=ai.copy(),active_head=hi.copy(),D_inverse=dinv.copy(),S_inverse=headinv.copy(),
            H=h.copy(),B=b.copy(),E=e.copy(),D=d.copy(),S=sraw.copy(),S_pair=s,D_certificate=dinfo,S_certificate=hinfo,
            completed_moment_refs=prepared['completed_chunk_refs'],physical_coordinate_inverse_maps_retained=True)
  ref=node_complete(data);assert isinstance(ref,dict) and ref;completed.append(ref)
 return dict(D_inverse=P.a_dd(DI),S_inverse=P.a_dd(J),D_inverse_raw=DI,S_inverse_raw=J,B=P.a_dd(moments['B']),E=P.a_dd(moments['E']),next_node=3870,
             active_node_count=3870,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,
             completed_node_refs=completed,completed_moment_refs=prepared['completed_chunk_refs'],equilibrated=equilibrate,
             right_preconditioner_factor_resolved=True,authoritative_action='paired_specialized_weak67',
             nodal_apply_or_weak_functional_qualified=False,exact_point_or_nodal_weak_DD_inverse_claimed=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
