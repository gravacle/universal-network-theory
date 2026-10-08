"""Held definitions: finite fixed-canonical ordinary energy/stress and full JVP.
Globals np,P, reviewed fs_* dual/fy_* paired helpers. Every dual is (value,direction).
Inputs are existing once-counted canonical labels and reference mean weights;
no source reconstruction, new angular rule, volume factor, history or offset.
Caller authenticates the original excess/reference budget and spatial tests.
"""
FINITE_ORDINARY_AUTHOR_DRAFT=True

def finite_fixed_canonical_ordinary_point(geometry,gauge,labels,keep,label):
 put=lambda name,x:fs_keep(label+'_'+name,x,keep)
 I=fs_dual(geometry['ih'],geometry['delta_ih']);h=fs_dual(geometry['h'],geometry['delta_h'])
 N=fs_dual(gauge['N']);beta=fs_dual(gauge['beta']);p=I[0][0].shape[0]
 assert labels['existing_once_counted_branch_registered'] is True and labels['provenance']
 mass=fs_dual(labels['galaxy_mass_weight']);cov=fs_dual(labels['galaxy_specific_covector'])
 dust=fs_dual(labels['reference_dust_energy_weight']);weights=labels['radiation_weights'];rays=labels['radiation_covectors']
 assert all(w.shape==(p,) for x in (mass,dust,N) for pair in x for w in pair)
 assert all(w.shape==(p,3) for pair in cov for w in pair)
 assert all(w.shape==(p,3,3) for pair in I for w in pair)
 assert weights[0].shape==weights[1].shape and weights[0].ndim==2 and weights[0].shape[1]==p
 assert rays[0].shape==rays[1].shape==weights[0].shape+(3,)
 for x in (mass,dust):assert np.all(x[0][0]-abs(x[0][1])>=0)
 assert np.all(weights[0]-abs(weights[1])>=0)
 for name,x in (('fixed_galaxy_mass',mass),('fixed_galaxy_covector',cov),('fixed_reference_dust_energy',dust),('fixed_N',N),('fixed_shift',beta)):put(name,x)
 fy_keep(label+'_fixed_radiation_weights',weights,keep);fy_keep(label+'_fixed_radiation_covectors',rays,keep)
 up=put('galaxy_raised_covector',fs_mv(I,cov))
 one=fs_dual(P.a_dd(np.ones(p)))
 gamma=put('galaxy_gamma',fs_sqrt(fs_add(one,fs_dot(cov,up)),keep,label+'_galaxy_gamma_root'))
 EG=put('galaxy_energy',fs_mul(mass,gamma));momentum=put('galaxy_momentum',fs_mul(fs_expand(mass,(Ellipsis,None)),cov))
 outer=fs_mul(fs_expand(up,(Ellipsis,slice(None),None)),fs_expand(up,(Ellipsis,None,slice(None))))
 SG=put('galaxy_contravariant_stress',fs_mul(fs_expand(fs_div(mass,gamma,keep,label+'_mass_over_gamma'),(Ellipsis,None,None)),outer))
 ER=fs_dual(P.a_dd(np.zeros(p)));SR=fs_dual(P.a_dd(np.zeros((p,3,3))));PR=fs_dual(P.a_dd(np.zeros((p,3))))
 for a in range(weights[0].shape[0]):
  w=fs_dual(P.a_slice(weights,a));k=fs_dual(P.a_slice(rays,a));raised=put('radiation_current_raised_covector',fs_mv(I,k))
  energy=put('radiation_current_energy',fs_sqrt(fs_dot(k,raised),keep,label+'_radiation_root_'+str(a)))
  ER=put('radiation_energy_partial',fs_add(ER,fs_mul(w,energy)))
  PR=put('radiation_momentum_partial',fs_add(PR,fs_mul(fs_expand(w,(Ellipsis,None)),k)))
  outer=fs_mul(fs_expand(raised,(Ellipsis,slice(None),None)),fs_expand(raised,(Ellipsis,None,slice(None))))
  term=fs_mul(fs_expand(fs_div(w,energy,keep,label+'_radiation_weight_over_energy_'+str(a)),(Ellipsis,None,None)),outer)
  SR=put('radiation_stress_partial',fs_add(SR,term))
 E=put('total_energy',fs_add(fs_add(EG,dust),ER));S=put('total_stress',fs_add(SG,SR));mom=put('total_momentum',fs_add(momentum,PR))
 rows=put('normal_density',fs_stack([E]+[fs_neg(fs_slice(mom,(slice(None),a))) for a in range(3)],1))
 force=put('metric_configuration_force',fs_scale(.5,fs_mul(fs_expand(N,(Ellipsis,None,None)),S)))
 H=put('canonical_Hamiltonian',fs_sub(fs_mul(N,E),fs_dot(beta,mom)))
 # Geometry sensitivity has fixed labels; the dust derivative is exactly zero.
 contraction=fy_contract(geometry['delta_h'],S[0]);contact=P.a_add(E[1],P.a_mul64(.5,contraction));fy_keep(label+'_energy_direction_plus_half_delta_h_stress',contact,keep)
 return dict(value=dict(energy=E[0],momentum=mom[0],stress=S[0],normal_density=rows[0],metric_force=force[0],Hamiltonian=H[0]),
             delta=dict(energy=E[1],momentum=mom[1],stress=S[1],normal_density=rows[1],metric_force=force[1],Hamiltonian=H[1]),
             energy_metric_direction_contact=contact,existing_labels_and_mean_weights_unchanged=True,
             extra_volume_factor_or_budget_subtraction_introduced=False,physical_adoption=False)
