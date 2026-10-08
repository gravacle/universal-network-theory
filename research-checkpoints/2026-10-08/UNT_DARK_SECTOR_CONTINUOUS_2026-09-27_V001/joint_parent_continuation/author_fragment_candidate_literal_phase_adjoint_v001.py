"""HELD literal phase Mstar in the original independent3870 coordinate pairing.
Globals np,P,K(exact72 scalar value only), exact73 pack/unpack/keep, outward
mp_add/mp_mul, paired117 norm helpers, and PHASE_ADJOINT_REFERENCE.
The real coefficient identity is Mstar=S* diag(W H) S, W=original dv/R.
This explicit transpose has its own DD association; no bitwise symmetry claim.
H already contains N*mu. No EOS, old current/action, or diagonal is evaluated.
"""
PHASE_ADJOINT_AUTHOR_DRAFT=True
PHASE_ADJOINT_AUTHORING_IN_PROGRESS=False


def phase_adjoint_evaluation_transpose(field,basis,keep,label):
 assert field[0].shape==field[1].shape==(15136,)
 phase_response_keep(label+'_supplied_point_words',field,keep)
 f=P.a_reshape(field,(4,86,44));out=P.a_dd(np.zeros((87,45)))
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   tag=label+'_iq%d_corner%d'%(iq,corner);key=(slice(di,86+di),slice(dj,44+dj))
   term=P.a_mul64(basis['hats'][iq,corner,0],P.a_slice(f,iq));phase_response_keep(tag+'_term',term,keep)
   update=P.a_add(P.a_slice(out,key),term);phase_response_keep(tag+'_updated_corner',update,keep)
   out[0][key]=update[0];out[1][key]=update[1];phase_response_keep(tag+'_partial',out,keep)
 folded=P.a_add(P.a_slice(out,(1,slice(None))),P.a_slice(out,(0,slice(None))))
 phase_response_keep(label+'_axis_fold_before_restriction',folded,keep)
 out[0][1]=folded[0];out[1][1]=folded[1];out[0][0]=0.;out[1][0]=0.
 return phase_response_keep(label+'_completed',out,keep)


def phase_adjoint_positive(nodes,H,basis,keep,label):
 mask=P.scalar_mask();assert np.count_nonzero(mask)==3870
 x=mp_add(abs(nodes[0]),abs(nodes[1]),keep,label+'_nodal_absolute_words');x=P.scalar_lift(x)
 value=np.zeros((4,86,44))
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   tag=label+'_S_iq%d_corner%d'%(iq,corner)
   term=mp_mul(abs(basis['hats'][iq,corner,0]),x[di:86+di,dj:44+dj],keep,tag+'_term')
   value[iq]=mp_add(value[iq],term,keep,tag+'_sum');keep(tag+'_partial',value.copy())
 weight=np.asarray(basis['dv']/basis['R']).reshape(4,86,44);keep(label+'_source_rounded_weight',weight.copy())
 assert np.all(np.isfinite(weight)) and np.all(weight>0)
 h=mp_add(abs(H[0]),abs(H[1]),keep,label+'_H_absolute_words').reshape(4,86,44)
 weighted=mp_mul(weight,value,keep,label+'_W_times_S');point=mp_mul(h,weighted,keep,label+'_H_times_W_S')
 out=np.zeros((87,45))
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   tag=label+'_Sstar_iq%d_corner%d'%(iq,corner);key=(slice(di,86+di),slice(dj,44+dj))
   term=mp_mul(abs(basis['hats'][iq,corner,0]),point[iq],keep,tag+'_term')
   out[key]=mp_add(out[key],term,keep,tag+'_sum');keep(tag+'_partial',out.copy())
 out[1]=mp_add(out[1],out[0],keep,label+'_axis_fold');out[0]=0.
 keep(label+'_completed_weak_envelope',out.copy());return out


def phase_adjoint_mass_star(nodes,H,basis,keep,label):
 assert not PHASE_ADJOINT_AUTHOR_DRAFT and not PHASE_ADJOINT_AUTHORING_IN_PROGRESS
 assert nodes[0].shape==nodes[1].shape==(87,45) and H[0].shape==H[1].shape==(15136,)
 phase_response_keep(label+'_input_nodes',nodes,keep);phase_response_keep(label+'_input_literal_H',H,keep)
 assert all(np.all(a[0]==0) for a in nodes)
 value=K.phase_scalar_value(nodes,basis,keep,label+'_original_S');phase_response_keep(label+'_completed_S',value,keep)
 weight=np.asarray(basis['dv']/basis['R']).reshape(15136,);keep(label+'_original_rounded_dv_over_R',weight.copy())
 assert np.all(np.isfinite(weight)) and np.all(weight>0)
 weighted=P.a_mul64(weight,value);phase_response_keep(label+'_W_S',weighted,keep)
 point=P.a_mul(H,weighted);phase_response_keep(label+'_H_W_S',point,keep)
 weak=phase_adjoint_evaluation_transpose(point,basis,keep,label+'_original_Sstar')
 envelope=phase_adjoint_positive(nodes,H,basis,keep,label+'_independent_positive')
 absolute=mp_add(abs(weak[0]),abs(weak[1]),keep,label+'_completed_word_absolute_upper')
 keep(label+'_positive_enclosure_margin',(envelope-absolute).copy())
 assert np.all(absolute<=envelope),'Explicit coefficient-transpose polynomial enclosure required'
 return phase_response_keep(label+'_completed_Mstar',weak,keep)


def phase_adjoint_reference(rhs,scale,keep,label):
 assert rhs[0].shape==rhs[1].shape==scale.shape==(3870,)
 phase_response_keep(label+'_both_word_eLp',rhs,keep);keep(label+'_positive_coordinate_scale',scale.copy())
 assert scale.dtype==np.float64 and np.all(np.isfinite(scale)) and np.all(scale>0)
 zero=bool(all(np.all(a==0) for a in rhs));scaled=P.a_div64(rhs,scale,keep,label+'_source_coordinate_division')
 phase_response_keep(label+'_scaled_source',scaled,keep);norms=[]
 for version,words in (('raw',rhs),('scaled',scaled)):
  phase_response_keep(label+'_'+version+'_source_words',words,keep)
  value=native_metric_gmres_norm(words,label+'_'+version+'_source_norm')
  assert np.isfinite(value) and (value==0 if zero else value>0),'Nonzero source cannot have unresolved zero norm'
  norms.append(value);keep(label+'_source_norms_partial',np.asarray(norms))
 return dict(source=tuple(a.copy() for a in rhs),scale=scale.copy(),norms=tuple(norms),zero_source_both_words=zero,
             zero_source_relative_ratio_undefined=zero,relative_reference_is_NEW_eLp=True,physical_norm_or_forward_error_qualified=False)


def phase_adjoint_scores(residual,reference,keep,label):
 assert residual[0].shape==residual[1].shape==(3870,)
 phase_response_keep(label+'_residual_words',residual,keep)
 zero=bool(all(np.all(a==0) for a in residual));scaled=P.a_div64(residual,reference['scale'],keep,label+'_residual_coordinate_division')
 phase_response_keep(label+'_scaled_residual',scaled,keep);absolute=np.zeros(2);ratios=np.zeros(2)
 for column,(version,words) in enumerate((('raw',residual),('scaled',scaled))):
  phase_response_keep(label+'_'+version+'_residual_words',words,keep)
  value=native_metric_gmres_norm(words,label+'_'+version+'_residual_norm');absolute[column]=value
  assert np.isfinite(value) and (value==0 if zero else value>0),'Unresolved nonzero residual norm refuses'
  ratios[column]=(0. if zero else 1.) if reference['zero_source_both_words'] else value/reference['norms'][column]
  keep(label+'_absolute_norms_partial',absolute.copy());keep(label+'_admission_scores_partial',ratios.copy())
 keep(label+'_absolute_raw_scaled_norms',absolute.copy());keep(label+'_source_raw_scaled_norms',np.asarray(reference['norms']))
 keep(label+'_relative_ratio_undefined_zero_source',np.asarray(reference['zero_source_both_words']))
 keep(label+'_exact_both_word_zero_residual',np.asarray(zero));keep(label+'_admission_scores',ratios.copy())
 assert np.all(np.isfinite(ratios)) and np.all(ratios>=0);return ratios


def phase_adjoint_certificate(nodes,rhs,H,basis,scale,keep,label):
 assert all(np.array_equal(a,b) for a,b in zip(rhs,PHASE_ADJOINT_REFERENCE['source']))
 assert np.array_equal(scale,PHASE_ADJOINT_REFERENCE['scale'])
 field=phase_response_unpack(nodes);phase_response_keep(label+'_lambda_scalar_nodes',field,keep)
 full=K.phase_mass_action(field,H,basis,keep,label+'_explicit_coefficient_Mstar')
 action=phase_response_pack(full);phase_response_keep(label+'_action',action,keep)
 res=P.a_sub(rhs,action);phase_response_keep(label+'_residual',res,keep)
 scores=phase_adjoint_scores(res,PHASE_ADJOINT_REFERENCE,keep,label+'_source_relative_certificate')
 return res,scores,action
