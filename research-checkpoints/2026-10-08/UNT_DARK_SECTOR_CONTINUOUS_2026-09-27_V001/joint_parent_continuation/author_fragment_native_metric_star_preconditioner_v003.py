"""Definitions-only numerical native-star + metric congruence candidate.
Caller supplies np/P/keep and authenticated saved PREPARATION/current B,T/geometry.
No runner, input reads, old native block assembly, fine action, inverse or solver
is executed on import. Native D/B/Maxwell/basis_scale are copied, never replayed.
The cached native surrogate in its saved scale coordinates has U block
M+sum B_i D_i^-1 B_i.T, mode blocks D_i and U<-mode B_i.
Only NEW common-basis self-node metric cross/T moments are assembled here.
Both serialized transpose defects and rounded/identified basis contacts remain
explicit; this symmetric numerical surrogate is not the exact fine diagonal.
Its signed small-block elimination retains C=Gu-sum Lbar_i.T Gzi. Absolute
spectral magnitudes change only the numerical congruence, never the full action,
RHS, physical law, original certificates, literal/frozen gap or initial state.
Inactive coordinates have identity fillers solely for batched small matrices.
Outer/top rates remain free. No global inverse/rank/coercivity is claimed.
Coordinate factors include the right eigenvector transpose, preserving the
original auxiliary coordinates under inactive axis/sheet masks; sorted spectral
columns alone cannot be subjected to those physical component masks.
Recurrence choice/cap and actual adjoint qualification belong to a later caller.
"""
NATIVE_METRIC_STAR_AUTHOR_DRAFT=True
NATIVE_METRIC_STAR_AUTHORING_IN_PROGRESS=True

def native_metric_star_pair(label,x):
 for w,suffix in enumerate(('hi','lo')):keep(label+'_'+suffix,np.asarray(x[w]).copy())
 return x

def native_metric_star_round(label,x):
 native_metric_star_pair(label+'_words',x);out=x[0]+x[1];keep(label+'_binary64',out.copy())
 native_metric_star_pair(label+'_readout_defect',P.a_sub(x,P.a_dd(out)));assert np.all(np.isfinite(out));return out

def native_metric_star_mm(A,B,label):
 assert A.shape[-1]==B.shape[-2]
 columns=[]
 for j in range(B.shape[-1]):
  column=native_metric_star_pair(label+'_current_column',P.a_matvec(A,P.a_dd(B[...,j])));columns.append(column)
 return native_metric_star_round(label,P.a_stack(columns,axis=-1))

def native_metric_star_masks():
 nm=np.ones((3,87,45),dtype=bool);nm[:,0]=False;nm[1,:,0]=False
 km=np.ones((6,87,45),dtype=bool);km[:,0]=False;km[3:5,:,0]=False
 return nm.transpose(1,2,0).reshape(3915,3),km.transpose(1,2,0).reshape(3915,6)

def copy_saved_native_star(saved,label):
 shapes={'preconditioner_D':(32,3915,3,3),'preconditioner_B':(32,3915,3,3),'preconditioner_Maxwell':(3915,3,3),'preconditioner_basis_scale':(3915,3),'kinetic_congruence_scale':(33,3,87,45)}
 out={}
 for name,shape in shapes.items():
  x=np.asarray(saved[name]);keep(label+'_copied_'+name,x.copy());assert x.dtype==np.float64 and x.shape==shape and np.all(np.isfinite(x));out[name]=x.copy()
 nm,km=native_metric_star_masks();keep(label+'_native_active_mask',nm.copy());keep(label+'_metric_active_mask',km.copy())
 assert np.all(out['preconditioner_basis_scale']>0) and np.all(out['kinetic_congruence_scale']>0)
 outer=nm[..., :,None]*nm[...,None,:];inactive_identity=np.eye(3)[None]*(~nm)[..., :,None]
 for name in ('preconditioner_D','preconditioner_Maxwell'):
  a=out[name];assert np.array_equal(a*(~outer),np.broadcast_to(inactive_identity,a.shape))
 assert np.all(out['preconditioner_B']*(~outer)==0)
 return dict(D=out['preconditioner_D'],B=out['preconditioner_B'],M=out['preconditioner_Maxwell'],basis_scale=out['preconditioner_basis_scale'],native_mask=nm,metric_mask=km,inherited_normscale=out['kinetic_congruence_scale'])

def native_metric_star_local_factors(g,iq,label):
 # A NEW common-basis numerical Gram convention, not an old FE action replay.
 R=np.asarray(g['R'][iq]).reshape(86,44);h=np.asarray(g['hats'][iq,:,0]);assert h.shape==(4,86,44)
 F=np.zeros((86,44,6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 E=np.broadcast_to(h[...,None],(4,86,44,3)).copy();E[...,2]=R**2*h
 V=F[None]*h[...,None,None];keep(label+'_unidentified_native_factor',E.copy());keep(label+'_unidentified_metric_factor',V.copy())
 native_metric_star_pair(label+'_Fhat_product_readout_defect',P.a_sub(P.a_dd(V),P.a_prod(F[None],h[...,None,None])))
 for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
  if di==0:E[corner,0,:,0]=0
  if dj==0:E[corner,:,0,1]=0;V[corner,:,0,:,3:5]=0
 for lo,hi in ((0,1),(2,3)):
  ew=P.a_sum(E[lo,0],E[hi,0]);vw=P.a_sum(V[lo,0],V[hi,0]);native_metric_star_pair(label+'_axis_native_%d'%lo,ew);native_metric_star_pair(label+'_axis_metric_%d'%lo,vw)
  E[lo,0]=ew[0];V[lo,0]=vw[0];E[hi,0]=0;V[hi,0]=0
  keep(label+'_axis_native_geometry_compression_%d'%lo,ew[1].copy());keep(label+'_axis_metric_geometry_compression_%d'%lo,vw[1].copy())
 keep(label+'_identified_native_factor',E.copy());keep(label+'_identified_metric_factor',V.copy());return E,V

def assemble_new_metric_star_couplings(B,T,eB,eT,g,cached,label):
 assert B.shape==eB.shape==(15136,99,6) and T.shape==eT.shape==(15136,6,6)
 for name,a in (('B',B),('T',T),('eB',eB),('eT',eT)):
  keep(label+'_authenticated_point_'+name,a.copy());assert a.dtype==np.float64 and np.all(np.isfinite(a))
 assert np.all(eB>=0) and np.all(eT>=0) and np.asarray(g['R']).shape==np.asarray(g['dv']).shape==(4,3784)
 G=np.zeros((33,3,6,87,45));eG=G.copy();K=np.zeros((6,6,87,45));eK=K.copy()
 keep(label+'_point_T_transpose_defect',(T-T.swapaxes(-1,-2)).copy())
 for iq in range(4):
  E,F=native_metric_star_local_factors(g,iq,label+'_q%d'%iq);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44);keep(label+'_current_positive_weight',weight.copy());assert np.all(np.isfinite(weight)) and np.all(weight>0)
  b=B[iq*3784:(iq+1)*3784].reshape(86,44,33,3,6);eb=eB[iq*3784:(iq+1)*3784].reshape(b.shape)+abs(b)
  t=T[iq*3784:(iq+1)*3784].reshape(86,44,6,6);et=eT[iq*3784:(iq+1)*3784].reshape(t.shape)+abs(t)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   bf=np.einsum('ijgcl,ijla->ijgca',b,F[corner],optimize=True);keep(label+'_current_BF',bf.copy())
   value=weight[...,None,None,None]*E[corner][...,None,:,None]*bf;keep(label+'_current_cross_terms',value.copy())
   bound=weight[...,None,None,None]*abs(E[corner][...,None,:,None])*np.einsum('ijgcl,ijla->ijgca',eb,abs(F[corner]),optimize=True);keep(label+'_current_cross_positive_terms',bound.copy())
   sl=(slice(None),slice(None),slice(None),slice(di,86+di),slice(dj,44+dj));G[sl]+=value.transpose(2,3,4,0,1);eG[sl]+=bound.transpose(2,3,4,0,1);keep(label+'_cross_current_partial',G.copy());keep(label+'_cross_bound_current_partial',eG.copy())
   tf=np.einsum('ijlk,ijka->ijla',t,F[corner],optimize=True);keep(label+'_current_TF',tf.copy())
   value=weight[...,None,None]*np.einsum('ijla,ijlb->ijab',F[corner],tf,optimize=True);keep(label+'_current_metric_terms',value.copy())
   bound=weight[...,None,None]*np.einsum('ijla,ijlk,ijkb->ijab',abs(F[corner]),et,abs(F[corner]),optimize=True);keep(label+'_current_metric_positive_terms',bound.copy())
   sl=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj));K[sl]+=value.transpose(2,3,0,1);eK[sl]+=bound.transpose(2,3,0,1);keep(label+'_metric_current_partial',K.copy());keep(label+'_metric_bound_current_partial',eK.copy())
 for a in (G,eG,K,eK):a[...,1,:]+=a[...,0,:];a[...,0,:]=0
 G=G.transpose(0,3,4,1,2).reshape(33,3915,3,6);eG=eG.transpose(0,3,4,1,2).reshape(G.shape);K=K.transpose(2,3,0,1).reshape(3915,6,6);eK=eK.transpose(2,3,0,1).reshape(K.shape)
 nm,km=cached['native_mask'],cached['metric_mask'];active=nm[..., :,None]*km[...,None,:]
 G*=active[None];eG*=active[None];ma=km[..., :,None]*km[...,None,:];K*=ma;eK*=ma
 # Pull physical native nodal coefficients into the earned scale coordinates.
 scale=cached['basis_scale'][None,...,None];keep(label+'_cross_physical',G.copy());keep(label+'_cross_physical_envelope',eG.copy());G/=scale;eG/=scale
 for name,a in (('cross_saved_scale_coordinates',G),('cross_positive_envelope',eG),('metric_block',K),('metric_positive_envelope',eK)):
  keep(label+'_'+name,a.copy());assert np.all(np.isfinite(a))
 keep(label+'_metric_block_transpose_defect',(K-K.swapaxes(-1,-2)).copy())
 return dict(G=G,eG=eG,T=K,eT=eK,common_basis_is_numerical_surrogate=True,old_native_star_replayed=False,fine_action_changed=False)

def native_metric_star_spectral(raw,envelope,label):
 assert raw.shape==envelope.shape and raw.shape[-1]==raw.shape[-2] and np.all(np.isfinite(raw)) and np.all(np.isfinite(envelope)) and np.all(envelope>=0)
 n=raw.shape[-1];keep(label+'_raw_block',raw.copy());keep(label+'_upstream_envelope',envelope.copy());keep(label+'_transpose_defect',(raw-raw.swapaxes(-1,-2)).copy())
 symmetric=(raw+raw.swapaxes(-1,-2))*.5;keep(label+'_symmetric_preconditioner_block',symmetric.copy())
 native_metric_star_pair(label+'_symmetrization_rounding',P.a_sub(P.a_mul64(.5,P.a_add(P.a_dd(raw),P.a_dd(raw.swapaxes(-1,-2)))),P.a_dd(symmetric)))
 rows=np.sum(abs(symmetric),axis=-1);keep(label+'_row_magnitudes',rows.copy());assert np.all(rows>0) and np.all(np.isfinite(rows))
 exponent=np.floor_divide(np.frexp(rows)[1]-1,2);sigma=np.ldexp(np.ones_like(rows),exponent);inverse_sigma=np.ldexp(np.ones_like(rows),-exponent)
 keep(label+'_exact_power_two_balance_exponents',exponent.copy());keep(label+'_balance',sigma.copy());keep(label+'_inverse_balance',inverse_sigma.copy());assert np.all(np.isfinite(sigma)) and np.all(sigma>0) and np.all(np.isfinite(inverse_sigma))
 first=symmetric*inverse_sigma[..., :,None];keep(label+'_first_balanced_block',first.copy());native_metric_star_pair(label+'_first_balance_rounding',P.a_sub(P.a_prod(symmetric,inverse_sigma[..., :,None]),P.a_dd(first)))
 rawwhite=first*inverse_sigma[...,None,:];keep(label+'_raw_balanced_block',rawwhite.copy());native_metric_star_pair(label+'_second_balance_rounding',P.a_sub(P.a_prod(first,inverse_sigma[...,None,:]),P.a_dd(rawwhite)))
 keep(label+'_balanced_transpose_defect',(rawwhite-rawwhite.swapaxes(-1,-2)).copy());white=.5*(rawwhite+rawwhite.swapaxes(-1,-2));keep(label+'_balanced_block',white.copy())
 native_metric_star_pair(label+'_balanced_symmetrization_rounding',P.a_sub(P.a_mul64(.5,P.a_add(P.a_dd(rawwhite),P.a_dd(rawwhite.swapaxes(-1,-2)))),P.a_dd(white)))
 bound=(envelope+abs(raw)+abs(raw.swapaxes(-1,-2)))*inverse_sigma[..., :,None]*inverse_sigma[...,None,:];keep(label+'_balanced_positive_bound',bound.copy());assert np.all(np.isfinite(white)) and np.all(np.isfinite(bound))
 values,vectors=np.linalg.eigh(white);keep(label+'_signed_eigenvalues',values.copy());keep(label+'_eigenvectors',vectors.copy())
 defect=white@vectors-vectors*values[...,None,:];orth=vectors.swapaxes(-1,-2)@vectors-np.eye(n);keep(label+'_eigen_equation_defect',defect.copy());keep(label+'_orthogonality_defect',orth.copy())
 asym=.5*(raw-raw.swapaxes(-1,-2))*inverse_sigma[..., :,None]*inverse_sigma[...,None,:]
 budget=P.TOL*np.linalg.norm(bound,2,axis=(-2,-1))+np.linalg.norm(defect,2,axis=(-2,-1))+np.linalg.norm(asym,2,axis=(-2,-1))+512*n*np.finfo(float).eps*np.linalg.norm(abs(white),2,axis=(-2,-1))
 margin=np.min(abs(values),axis=-1)-budget;keep(label+'_resolved_error_budget',np.asarray(budget).copy());keep(label+'_resolved_spectral_margin',np.asarray(margin).copy());assert np.all(np.isfinite(values)) and np.all(margin>0),'Unresolved/singular local star block: no jitter or drop'
 V=inverse_sigma[..., :,None]*vectors;spectral_factor=V/np.sqrt(abs(values))[...,None,:];keep(label+'_unrotated_spectral_column_factor',spectral_factor.copy())
 factor=native_metric_star_mm(spectral_factor,vectors.swapaxes(-1,-2),label+'_coordinate_preserving_factor');signed_inverse=(V/values[...,None,:])@V.swapaxes(-1,-2)
 keep(label+'_absolute_congruence_factor',factor.copy());keep(label+'_signed_inverse',signed_inverse.copy());assert np.all(np.isfinite(factor)) and np.all(np.isfinite(signed_inverse))
 absolute=((sigma[..., :,None]*vectors)*abs(values)[...,None,:])@(vectors.swapaxes(-1,-2)*sigma[...,None,:]);keep(label+'_balanced_absolute_block',absolute.copy())
 check=absolute@factor@factor.swapaxes(-1,-2)-np.eye(n);keep(label+'_absolute_inverse_contact',check.copy());P.check(label+'_absolute_inverse_construction',check,np.zeros_like(check),abs(absolute)@abs(factor)@abs(factor.swapaxes(-1,-2))+np.eye(n))
 signed_contact=symmetric@signed_inverse-np.eye(n);keep(label+'_signed_inverse_contact',signed_contact.copy());P.check(label+'_signed_inverse_construction',signed_contact,np.zeros_like(signed_contact),abs(symmetric)@abs(signed_inverse)+np.eye(n))
 return symmetric,signed_inverse,factor

def factor_native_metric_star(cached,new,label):
 D,B,M=cached['D'],cached['B'],cached['M'];n=M.shape[0];assert D.shape==B.shape==(32,n,3,3) and M.shape==(n,3,3)
 Ds,DI,DF=native_metric_star_spectral(D,2*abs(D),label+'_mode_blocks');A=B.swapaxes(-1,-2);keep(label+'_cached_mode_U_blocks',A.copy())
 G=new['G'];eG=new['eG'];assert G.shape==eG.shape==(33,n,3,6);Gz=G[1:];L=native_metric_star_mm(DI,A,label+'_Lbar');V=native_metric_star_mm(DI,Gz,label+'_Dinv_metric')
 cterms=native_metric_star_mm(L.swapaxes(-1,-2),Gz,label+'_C_terms');sterms=native_metric_star_mm(Gz.swapaxes(-1,-2),V,label+'_S_terms')
 C=native_metric_star_round(label+'_C',P.a_sub(P.a_dd(G[0]),P.a_dd(np.sum(cterms,axis=0))))
 S=native_metric_star_round(label+'_S',P.a_sub(P.a_dd(new['T']),P.a_dd(np.sum(sterms,axis=0))))
 eC=eG[0]+np.sum(abs(L).swapaxes(-1,-2)@eG[1:]+abs(cterms),axis=0);eS=new['eT']+np.sum(eG[1:].swapaxes(-1,-2)@abs(V)+abs(Gz).swapaxes(-1,-2)@(abs(DI)@eG[1:])+abs(sterms),axis=0)
 keep(label+'_C_positive_bound',eC.copy());keep(label+'_S_positive_bound',eS.copy())
 nm,km=cached['native_mask'],cached['metric_mask'];active=km[..., :,None]*km[...,None,:];S*=active;eS*=active;S+=np.eye(6)[None]*(~km)[..., :,None];eS+=np.eye(6)[None]*(~km)[..., :,None]
 C*=nm[..., :,None]*km[...,None,:];eC*=nm[..., :,None]*km[...,None,:]
 K=np.zeros((n,9,9));eK=K.copy();K[:,:3,:3]=M;K[:,:3,3:]=C;K[:,3:,:3]=C.swapaxes(-1,-2);K[:,3:,3:]=S
 eK[:,:3,:3]=2*abs(M);eK[:,:3,3:]=eC;eK[:,3:,:3]=eC.swapaxes(-1,-2);eK[:,3:,3:]=eS
 keep(label+'_retained_signed_reduced_block',K.copy());Ks,KI,KF=native_metric_star_spectral(K,eK,label+'_U_metric_block')
 return dict(L=L,V=V,D_factor=DF,K_factor=KF,D_symmetric=Ds,K_symmetric=Ks,C=C,S=S,basis_scale=cached['basis_scale'].copy(),native_mask=nm.copy(),metric_mask=km.copy(),dimension_native_groups=33,metric_components=6,fine_action_or_RHS_changed=False,global_inverse_or_coercivity_claimed=False,unqualified_literal_primitive_gap_preserved=True)

def native_metric_star_forward(y,k,pre,label):
 # Node-order pairs: native[33,n,3], metric[n,6], same independent DOF mask.
 n=pre['basis_scale'].shape[0];assert y[0].shape==y[1].shape==(33,n,3) and k[0].shape==k[1].shape==(n,6)
 y=tuple(a*pre['native_mask'][None] for a in y);k=tuple(a*pre['metric_mask'] for a in k)
 uk=native_metric_star_pair(label+'_U_metric_factor',P.a_matvec(pre['K_factor'],tuple(np.concatenate((y[w][0],k[w]),axis=-1) for w in (0,1))))
 u=P.a_slice(uk,(slice(None),slice(0,3)));metric=P.a_slice(uk,(slice(None),slice(3,9)))
 mode=native_metric_star_pair(label+'_mode_factor',P.a_matvec(pre['D_factor'],P.a_slice(y,slice(1,33))))
 lu=native_metric_star_pair(label+'_Lbar_U',P.a_matvec(pre['L'],u));vk=native_metric_star_pair(label+'_Dinv_metric_term',P.a_matvec(pre['V'],metric));z=native_metric_star_pair(label+'_mode_chart',P.a_sub(P.a_sub(mode,lu),vk))
 native=P.a_stack([u]+[P.a_slice(z,i) for i in range(32)]);native=native_metric_star_pair(label+'_saved_scale_pullback',P.a_mul64(1/pre['basis_scale'][None],native))
 native=tuple(a*pre['native_mask'][None] for a in native);metric=tuple(a*pre['metric_mask'] for a in metric);native_metric_star_pair(label+'_native',native);native_metric_star_pair(label+'_metric',metric);return native,metric

def native_metric_star_adjoint(r,s,pre,label):
 n=pre['basis_scale'].shape[0];assert r[0].shape==r[1].shape==(33,n,3) and s[0].shape==s[1].shape==(n,6)
 scaled=native_metric_star_pair(label+'_saved_scale_adjoint',P.a_mul64(1/pre['basis_scale'][None],tuple(a*pre['native_mask'][None] for a in r)));mode=P.a_slice(scaled,slice(1,33))
 lu=native_metric_star_pair(label+'_Lbar_adjoint_terms',P.a_matvec(pre['L'].swapaxes(-1,-2),mode));vk=native_metric_star_pair(label+'_metric_adjoint_terms',P.a_matvec(pre['V'].swapaxes(-1,-2),mode))
 us=P.a_slice(scaled,0);ks=tuple(a*pre['metric_mask'] for a in s)
 for i in range(32):us=P.a_sub(us,P.a_slice(lu,i));ks=P.a_sub(ks,P.a_slice(vk,i))
 native_metric_star_pair(label+'_U_restriction',us);native_metric_star_pair(label+'_metric_restriction',ks)
 uk=native_metric_star_pair(label+'_U_metric_adjoint',P.a_matvec(pre['K_factor'].swapaxes(-1,-2),tuple(np.concatenate((us[w],ks[w]),axis=-1) for w in (0,1))))
 modes=native_metric_star_pair(label+'_mode_adjoint',P.a_matvec(pre['D_factor'].swapaxes(-1,-2),mode));native=P.a_stack([P.a_slice(uk,(slice(None),slice(0,3)))]+[P.a_slice(modes,i) for i in range(32)]);metric=P.a_slice(uk,(slice(None),slice(3,9)))
 native=tuple(a*pre['native_mask'][None] for a in native);metric=tuple(a*pre['metric_mask'] for a in metric);native_metric_star_pair(label+'_native',native);native_metric_star_pair(label+'_metric',metric);return native,metric

def fresh_correlated_native_metric_star_control(label='fresh_correlated_native_metric_star'):
 # New full32-star witness. Independent dyadic RHS/solution; C=I/2 is nonzero.
 I=np.eye(3);j=np.arange(1,33,dtype=float);D=np.broadcast_to(2*I,(32,1,3,3)).copy();B=(j[:,None,None,None]/8)*I[None,None];M=I[None].copy();scale=np.array([[2.,4.,8.]])
 cached=dict(D=D,B=B,M=M,basis_scale=scale,native_mask=np.ones((1,3),dtype=bool),metric_mask=np.ones((1,6),dtype=bool));G=np.zeros((33,1,3,6));G[0,0,:,:3]=37*I/8;G[1:,0,:,:3]=I/8
 T=np.diag([1.25,1.25,1.25,-2.,3.,-4.])[None];new=dict(G=G,eG=2*abs(G),T=T,eT=2*abs(T));pre=factor_native_metric_star(cached,new,label+'_factor')
 expected_C=np.zeros((1,3,6));expected_C[0,:,:3]=I/2;expected_S=np.diag([1.,1.,1.,-2.,3.,-4.])[None]
 P.check(label+'_nonzero_C_and_signed_S',np.concatenate((pre['C'].ravel(),pre['S'].ravel())),np.concatenate((expected_C.ravel(),expected_S.ravel())),np.concatenate((2*abs(G[0]).ravel()+2*abs(expected_C).ravel(),2*abs(T).ravel()+2*abs(expected_S).ravel())))
 u=np.array([1.,-2.,3.]);k=np.array([2.,-1.,.5,1.,-2.,3.]);m=j[:,None]*np.array([1/32,-1/64,1/128])[None];expected_native=np.concatenate((u[None],m-j[:,None]*u[None]/16-k[None,:3]/16))[:,None]/scale[None]
 r=np.empty((33,1,3));r[0,0]=np.array([747/16,-795/32,923/64])*scale[0];r[1:,0]=2*m*scale[0];s=np.array([[73/16,-97/32,161/64,2.,-6.,12.]])
 keep(label+'_independent_RHS_native',r.copy());keep(label+'_independent_RHS_metric',s.copy());keep(label+'_independent_solution_native',expected_native.copy());keep(label+'_independent_solution_metric',k[None].copy())
 v,w=native_metric_star_adjoint(P.a_dd(r),P.a_dd(s),pre,label+'_adjoint');x,z=native_metric_star_forward(v,w,pre,label+'_forward');xn=native_metric_star_round(label+'_actual_native',x);zk=native_metric_star_round(label+'_actual_metric',z)
 P.check(label+'_correlated_absolute_inverse_known_solution',np.concatenate((xn.ravel(),zk.ravel())),np.concatenate((expected_native.ravel(),k)),np.concatenate((abs(xn).ravel()+abs(expected_native).ravel()+abs(r).ravel(),abs(zk).ravel()+abs(k)+abs(s[0]))))
 return dict(kind='NEW_full32_correlated_star_nonzero_C_signed_metric_known_inverse',native_groups=33,native_components=99,metric_components=6,cross_completion_forbidden=True,basis_scale=[2,4,8],no_old_fixture_or_operator_replay=True,physical_adoption=False)


def fresh_native_star_inactive_coordinate_control(label='fresh_native_star_inactive_coordinates'):
 # Balanced eigenvalues sort as(1,1.5,2), with the inactive vector first.
 raw=np.diag([2.,1.,6.])[None];mask=np.array([[True,False,True]]);rhs=np.array([[2.,0.,12.]])
 keep(label+'_independent_block',raw.copy());keep(label+'_independent_mask',mask.copy());keep(label+'_independent_RHS',rhs.copy())
 symmetric,inverse,factor=native_metric_star_spectral(raw,2*abs(raw),label+'_actual_factor')
 outer=mask[..., :,None]*mask[...,None,:];inactive=np.eye(3)[None]*(~mask)[..., :,None];leak=factor*(~outer)-inactive;keep(label+'_inactive_factor_contact',leak.copy())
 P.check(label+'_coordinate_factor_preserves_inactive_space',leak,np.zeros_like(leak),abs(factor)+np.eye(3))
 restricted=native_metric_star_pair(label+'_actual_adjoint',P.a_matvec(factor.swapaxes(-1,-2),P.a_dd(rhs)));restricted=tuple(a*mask for a in restricted)
 result=native_metric_star_pair(label+'_actual_forward',P.a_matvec(factor,restricted));result=tuple(a*mask for a in result);actual=native_metric_star_round(label+'_masked_absolute_inverse',result);expected=np.array([[1.,0.,2.]])
 keep(label+'_independent_solution',expected.copy());P.check(label+'_masked_inverse_known_solution',actual,expected,abs(actual)+abs(expected)+abs(rhs))
 return dict(kind='NEW_inactive_coordinate_eigenordering_control',raw_diagonal=[2,1,6],balanced_spectral_order=[1,1.5,2],inactive_physical_coordinate=1,coordinate_factor_required=True,physical_adoption=False)
