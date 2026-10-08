"""HELD candidate-dependent literal phase mass action/diagonal; definitions only.
Globals np,P and K with exact72 phase_pair_keep/phase_scalar_value/phase_mass_diagonal.
Each of four columns supplies completed fresh116 eos, authenticated candidate_provenance,
and the identical prior_literal_weak_charge reference. No EOS/current/H replay.
The caller owns NEW basis and input admissions, repaired full DD arithmetic and fixed charge.
"""
CANDIDATE_PHASE_MASS_AUTHOR_DRAFT=True
CANDIDATE_PHASE_MASS_AUTHORING_IN_PROGRESS=False


def candidate_phase_mass_pair(x,shape,keep,label):
 assert isinstance(x,tuple) and len(x)==2 and all(isinstance(w,np.ndarray) for w in x)
 assert x[0].shape==x[1].shape
 keep(label+'_both_words',np.stack(x,axis=0).copy())
 assert all(w.shape==shape and w.dtype==np.dtype('float64') and np.all(np.isfinite(w)) for w in x)
 return K.phase_pair_keep(label,(x[0].copy(),x[1].copy()),keep)


def prepare_candidate_phase_mass(columns,basis,keep,label):
 assert len(columns)==4 and np.count_nonzero(P.scalar_mask())==3870
 geometry={}
 for n in ('R','dv','hats'):
  a=np.asarray(basis[n]);keep(label+'_NEW_basis_'+n,a.copy())
  assert a.dtype==np.dtype('float64') and np.all(np.isfinite(a));geometry[n]=a.copy()
 assert geometry['R'].shape in ((4,3784),(4,86,44)) and geometry['dv'].shape==geometry['R'].shape
 assert geometry['hats'].shape==(4,4,3,86,44) and np.all(geometry['R']>0) and np.all(geometry['dv']>0)
 families={n:[] for n in ('H','delta_H','current_point_density','current_point_density_direction','u')};eH=[];provenance=[]
 prior=columns[0]['prior_literal_weak_charge'];assert isinstance(prior,dict)
 assert all(isinstance(prior[n],str) and prior[n] for n in ('file','sha256','commit_file','commit_sha256'))
 constants=columns[0]['eos']['constants']
 for iq,column in enumerate(columns):
  eos=column['eos'];prefix=label+'_column%d'%iq
  assert column['prior_literal_weak_charge']==prior and isinstance(column['candidate_provenance'],dict) and column['candidate_provenance']
  provenance.append(dict(column['candidate_provenance']))
  assert eos['candidate_pressure_recomputed_from_invariant'] is True and eos['owned_pressure_u_used'] is False and eos['paired_input_collapsed'] is False
  assert eos['constants']==constants and constants['synthetic_control'] is False and constants['eps']==1e-5
  assert constants['relative_phase_coefficient']==1. and constants['C']==1.98
  for target,family,key in (('H','value','H'),('delta_H','delta','H'),('current_point_density','value','p'),('current_point_density_direction','delta','p'),('u','value','u')):
   families[target].append(candidate_phase_mass_pair(eos[family][key],(3784,),keep,prefix+'_'+target))
  envelope=np.asarray(eos['H_operation_envelope']).copy();keep(prefix+'_uncancelled_H_envelope',envelope)
  assert envelope.shape==(3784,) and envelope.dtype==np.dtype('float64') and np.all(np.isfinite(envelope)) and np.all(envelope>=0);eH.append(envelope)
  u=families['u'][-1];lo=u[0]-abs(u[1]);hi=constants['eps']-u[0]-abs(u[1])
  keep(prefix+'_strict_clock_u_lower',lo.copy());keep(prefix+'_strict_eps_minus_u_lower',hi.copy())
  assert np.all(lo>0) and np.all(hi>0),'Fresh candidate strict invariant domain required'
 fields={}
 for n,parts in families.items():
  fields[n]=P.a_reshape(P.a_stack(parts,0),(15136,));K.phase_pair_keep(label+'_candidate_'+n,fields[n],keep)
 envelope=np.concatenate(eH);keep(label+'_uncancelled_H_envelope',envelope.copy())
 lower=fields['H'][0]-abs(fields['H'][1]);margin=lower-2e-11*envelope
 keep(label+'_point_H_lower',lower.copy());keep(label+'_point_H_positive_construction_margin',margin.copy())
 diagonal=K.phase_mass_diagonal(fields['H'],geometry,keep,label+'_NEW_candidate_diagonal')
 candidate_phase_mass_pair(diagonal,(87,45),keep,label+'_diagonal_completed')
 mask=P.scalar_mask();diag_lower=diagonal[0][mask]-abs(diagonal[1][mask]);keep(label+'_independent_diagonal_lower',diag_lower.copy())
 return dict(**fields,eH=envelope,diagonal=diagonal,prior_literal_weak_charge=dict(prior),candidate_provenance=provenance,
             point_lower=lower,positive_margin=margin,diagonal_lower=diag_lower,basis=geometry,
             strictly_positive_H=bool(np.all(lower>0)),resolved_positive_H=bool(np.all(margin>0)),
             strictly_positive_diagonal=bool(np.all(diag_lower>0)),positive_construction_tolerance=2e-11,
             fresh_literal_candidate_H_used=True,reference_H_reused=False,paired_H_collapsed=False,
             configuration_contact_scope='supplied fresh116 direction only; not a whole chi map',
             fixed_literal_weak_charge_changed=False,phase_space_dofs=3870,phase_outer_top_nodes_free=True,
             invertibility_or_solve_acceptance_inferred=False,physical_adoption=False)


def candidate_phase_mass_spatial_jets(phase_nodes,basis,keep,label):
 # Exact73 R/Z polynomial only: the value was already evaluated by exact72.
 y=tuple(P.scalar_lift(a) for a in phase_nodes);out={}
 for jet,name in ((1,'R'),(2,'Z')):
  value=P.a_dd(np.zeros((4,86,44)))
  for iq in range(4):
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
    term=P.a_mul64(basis['hats'][iq,corner,jet],P.a_slice(y,(slice(di,86+di),slice(dj,44+dj))))
    K.phase_pair_keep(label+'_'+name+'_iq%d_corner%d_term'%(iq,corner),term,keep)
    v=P.a_add(P.a_slice(value,iq),term);value[0][iq]=v[0];value[1][iq]=v[1]
    K.phase_pair_keep(label+'_'+name+'_iq%d_corner%d_partial'%(iq,corner),value,keep)
  out[name]=P.a_reshape(value,(15136,));K.phase_pair_keep(label+'_'+name,out[name],keep)
 return out


def candidate_phase_mass_action(cache,basis,phase_nodes,keep,label):
 nodes=candidate_phase_mass_pair(phase_nodes,(87,45),keep,label+'_supplied_phase_nodes')
 assert all(np.all(w[0]==0) for w in nodes),'Independent original3870 phase coordinates required'
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],cache['basis'][n]),'Same NEW scalar basis required'
 # These three operations are the exact72 mass-action sequence and original transpose.
 value=K.phase_scalar_value(nodes,basis,keep,label);K.phase_pair_keep(label+'_completed_value',value,keep)
 weighted=P.a_mul(cache['H'],value);K.phase_pair_keep(label+'_point_charge_response',weighted,keep)
 weak=P.dd_scalar_scatter(weighted,basis,keep,label+'_weak_mass');K.phase_pair_keep(label+'_completed_weak',weak,keep)
 spatial=candidate_phase_mass_spatial_jets(nodes,basis,keep,label+'_mixed_phase_jets')
 return dict(weak=weak,point=weighted,scalar_jets=dict(value=value,**spatial),
             mixed_jet_rule='delta_partial_t_phi_i equals partial_i_delta_phi_t',
             instantaneous_spatial_phase_replaced=False,extra_N_or_mu_factor_inserted=False,
             temporal_mechanical_crossblock_zero_scope='fixed configuration only',physical_adoption=False)


def candidate_phase_mass_certificate(rhs,action,scale,keep,label):
 rhs=candidate_phase_mass_pair(rhs,(87,45),keep,label+'_fixed_original_RHS')
 action=candidate_phase_mass_pair(action,(87,45),keep,label+'_fresh_literal_mass_action')
 residual=P.a_sub(rhs,action);K.phase_pair_keep(label+'_original_residual',residual,keep)
 mask=P.scalar_mask();assert np.count_nonzero(mask)==3870
 scale=np.asarray(scale);keep(label+'_supplied_positive_scale',scale.copy())
 assert scale.shape==(3870,) and scale.dtype==np.dtype('float64') and np.all(np.isfinite(scale)) and np.all(scale>0)
 f=rhs[0][mask]+rhs[1][mask];r=residual[0][mask]+residual[1][mask]
 norms=np.array((np.linalg.norm(f),np.linalg.norm(f/scale),np.linalg.norm(r),np.linalg.norm(r/scale)),dtype=np.float64)
 keep(label+'_original_RHS_raw_scaled_and_residual_raw_scaled_norms',norms.copy());assert np.all(np.isfinite(norms))
 exact_rhs_zero=all(np.all(w[mask]==0) for w in rhs);exact_residual_zero=all(np.all(w[mask]==0) for w in residual)
 if norms[0]==0:
  assert norms[1]==0 and exact_rhs_zero,'Zero RHS readout must retain exactly zero original words'
  ratios=np.array((0.,0.)) if exact_residual_zero else np.array((np.inf,np.inf))
 else:
  assert norms[1]>0;ratios=np.array((norms[2]/norms[0],norms[3]/norms[1]))
 keep(label+'_original_raw_scaled_ratio_or_exact_zero_fallback',ratios.copy())
 return dict(residual=residual,norms=norms,ratios=ratios,zero_target_relative_ratio_undefined=exact_rhs_zero,
             exact_zero_residual=exact_residual_zero,no_forward_error_or_physical_acceptance_inferred=True)
