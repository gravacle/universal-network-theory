"""Held fixed-label sheet geometry: definitions only, no payload or invocation.
Globals np,P and reviewed fy128 helpers. Reference g is the authenticated
saved full metric at ORIGINAL matter labels, never an interpolated Gauss metric.
rho is sampled directly from the NEW nodal log-conformal field. Mass/covectors
are external immutable labels; no volume or radial multiplier is applied here.
The declared tangent differentiates the conformal algebra, not IEEE rounding.
"""
FIXED_LABEL_SHEET_AUTHOR_DRAFT=True
FIXED_LABEL_SHEET_AUTHORING_IN_PROGRESS=False

def fixed_label_sheet_Q1_scalar(nodes,indices,right_weight,keep,label):
 assert nodes[0].shape==nodes[1].shape==(87,45)
 assert indices.dtype==np.dtype('int64') and indices.shape==right_weight.shape
 assert np.all((indices>=0)&(indices<86)) and np.all((right_weight>0)&(right_weight<1))
 assert all(np.all(np.isfinite(w)) for w in nodes) and np.all(np.isfinite(right_weight))
 keep(label+'_fixed_indices',indices.copy());keep(label+'_fixed_right_weight',right_weight.copy())
 left=tuple(w[indices,0].copy() for w in nodes);right=tuple(w[indices+1,0].copy() for w in nodes)
 fy_keep(label+'_left_nodal_word',left,keep);fy_keep(label+'_right_nodal_word',right,keep)
 # This is a declared node-to-label scalar evaluation, not metric interpolation.
 out=P.a_add(P.a_mul64(1-right_weight,left),P.a_mul64(right_weight,right))
 return fy_keep(label+'_sample',out,keep)

def fixed_label_finite_sheet_geometry(reference_g,source_R,source_Z,r,indices,right_weight,rho_nodes,delta_rho_nodes,keep,label):
 p=len(source_R);assert reference_g.dtype==np.dtype('float64') and reference_g.shape==(p,4,4)
 assert source_Z.shape==(p,) and np.all(source_Z==0) and r.shape==(87,)
 assert np.all(np.diff(r)>0) and np.all(np.isfinite(reference_g)) and np.all(source_R>0)
 assert np.array_equal(reference_g,reference_g.swapaxes(-1,-2))
 assert indices.shape==right_weight.shape==(p,)
 put=lambda n,x:fy_keep(label+'_'+n,x,keep)
 keep(label+'_authentic_reference_g',reference_g.copy());keep(label+'_fixed_R',source_R.copy());keep(label+'_fixed_Z',source_Z.copy())
 # Preserve the location contact, without repairing weights or moving labels.
 location=P.a_sub(P.a_add(P.a_prod(1-right_weight,r[indices]),P.a_prod(right_weight,r[indices+1])),P.a_dd(source_R))
 put('fixed_label_location_contact',location)
 rho=fixed_label_sheet_Q1_scalar(rho_nodes,indices,right_weight,keep,label+'_rho')
 drho=fixed_label_sheet_Q1_scalar(delta_rho_nodes,indices,right_weight,keep,label+'_delta_rho')
 h0=put('reference_h',P.a_dd(reference_g[:,1:,1:]));I0,det0=fy_physical_reference_inverse(h0,keep,label+'_reference_inverse')
 mu0=put('reference_volume',fy_sqrt(det0,keep,label+'_reference_volume_root'))
 cov_beta=put('reference_shift_covector',P.a_dd(reference_g[:,0,1:]));beta=put('fixed_beta',fy_mv(I0,cov_beta))
 N2=put('reference_lapse_square',P.a_sub(fy_sum(P.a_mul(beta,cov_beta),-1),P.a_dd(reference_g[:,0,0])))
 lapse=put('fixed_lapse',fy_sqrt(N2,keep,label+'_reference_lapse_root'))
 put('reference_shift_reconstruction_gap',P.a_sub(fy_mv(h0,beta),cov_beta))
 put('reference_g00_reconstruction_gap',P.a_sub(P.a_sub(fy_sum(P.a_mul(beta,fy_mv(h0,beta)),-1),P.a_mul(lapse,lapse)),P.a_dd(reference_g[:,0,0])))
 exp_hi=np.exp(4*rho[0]);exp_lo=np.expm1(4*rho[1]);keep(label+'_elementary_exp_high',exp_hi.copy());keep(label+'_elementary_expm1_low',exp_lo.copy())
 assert np.all(np.isfinite(exp_hi)) and np.all(exp_hi>0) and np.all(np.isfinite(exp_lo))
 lam=put('conformal_weight',P.a_add(P.a_dd(exp_hi),P.a_prod(exp_hi,exp_lo)))
 assert np.all(lam[0]-abs(lam[1])>0)
 inv_lam=fy_div(P.a_dd(np.ones(p)),lam,keep,label+'_inverse_conformal_weight')
 h=put('candidate_h',fy_scale_matrix(lam,h0));I=put('candidate_inverse',fy_scale_matrix(inv_lam,I0))
 mu=put('candidate_volume',P.a_mul(mu0,P.a_mul(lam,fy_sqrt(lam,keep,label+'_conformal_root'))))
 dh=put('delta_h',fy_scale_matrix(P.a_mul64(4.,drho),h));dI=put('delta_inverse',fy_scale_matrix(P.a_mul64(-4.,drho),I))
 dmu=put('delta_volume',P.a_mul(P.a_mul64(6.,drho),mu))
 put('candidate_inverse_contact',P.a_sub(fy_mm(h,I),P.a_dd(np.broadcast_to(np.eye(3),(p,3,3)))))
 put('candidate_inverse_direction_contact',P.a_add(fy_mm(dh,I),fy_mm(h,dI)))
 zero_N=P.a_dd(np.zeros(p));zero_beta=P.a_dd(np.zeros((p,3)))
 return dict(geometry=dict(h=h,ih=I,mu=mu,delta_h=dh,delta_ih=dI,delta_mu=dmu),gauge=dict(N=(lapse,zero_N),beta=(beta,zero_beta)),rho=rho,delta_rho=drho,
             original_label_positions_unchanged=True,mass_or_volume_factor_added=False,reference_metric_lineage_admitted_by_this_helper=False,
             conformal_exp_accuracy_admitted=False,physical_inverse_precision_admitted=False,finite_candidate_physically_admitted=False)
