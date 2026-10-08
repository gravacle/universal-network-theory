"""HELD definitions-only restore of an authenticated completed finite0 STATE.
Globals np and P; caller authenticates INPUT/STATE records and their source.
No225/160/curvature/EOS/ordinary function is called. Arrays retain their words.
Unused registry constants/contract flags are restored from immutable source or
INPUT metadata explicitly; they do not confer candidate/physical admission.
"""
FINITE0_RESTORE_AUTHOR_DRAFT=True
FINITE0_RESTORE_AUTHORING_IN_PROGRESS=True
FINITE0_RESTORE_PARENT_SOURCE_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'

def finite0_saved_pair(data,name):
 a,b=data[name+'_hi'],data[name+'_lo']
 assert isinstance(a,np.ndarray) and isinstance(b,np.ndarray) and a.dtype==b.dtype==np.dtype('float64') and a.shape==b.shape
 assert np.all(np.isfinite(a)) and np.all(np.isfinite(b))
 return a.copy(),b.copy()

def finite0_saved_pair_family(data,prefix):
 names=sorted(n[len(prefix):-3] for n in data if n.startswith(prefix) and n.endswith('_hi'))
 assert names and len(names)==len(set(names));return {n:finite0_saved_pair(data,prefix+n) for n in names}

def finite0_saved_dual_family(data,prefix):
 names=sorted(n[len(prefix):-9] for n in data if n.startswith(prefix) and n.endswith('_value_hi'))
 assert names and len(names)==len(set(names))
 return {n:(finite0_saved_pair(data,prefix+n+'_value'),finite0_saved_pair(data,prefix+n+'_delta')) for n in names}

def finite0_saved_raw_family(data,prefix):
 out={n[len(prefix):]:x.copy() for n,x in data.items() if n.startswith(prefix)}
 assert out and all(isinstance(x,np.ndarray) and np.all(np.isfinite(x)) for x in out.values());return out

def finite0_completed_state_names(schema):
 prefixes=('completed_candidate_s_','completed_candidate_c_','completed_candidate_jets_',
  'completed_candidate_features_','completed_candidate_momenta_','completed_candidate_KADM_',
  'completed_contact_','completed_curvature_','completed_phase_','completed_mean_',
  'NEW_reference_input_','candidate_raw_model_','candidate_raw_coefficient_operation_',
  'candidate_raw_new_first_operation_','candidate_raw_unchanged_material_')
 return tuple(n for n in schema if n.startswith(prefixes))

def finite0_restore_completed_state(data,input_metadata,state_metadata,registered_constants=None):
 assert state_metadata['kind']=='NEW_candidate_completed_configuration_features_momenta_EOS_and_mean'
 assert state_metadata['failed'] is False and state_metadata['new_candidate_coefficients_and_EOS_evaluated'] is True
 assert state_metadata['all_configuration_inverse_E0_and_chart_gaps_retained'] is True and state_metadata['physical_adoption'] is False
 assert input_metadata['rho']==0. and input_metadata['compact_direction_node']==[43,22]
 assert input_metadata['owner']==state_metadata['owner'] and state_metadata['owner']['source_sha256']==FINITE0_RESTORE_PARENT_SOURCE_SHA
 iq=state_metadata['column'];refs=input_metadata['refs'];assert iq in range(4)
 for name,field in (('pilot_reference','pilots'),('owned_spatial_reference','forces')):
  assert all(state_metadata[name][k]==refs[field][iq][k] for k in ('file','sha256','commit_file','commit_sha256'))
 assert all(state_metadata['current_time_words'][k]==refs['current_jets'][k] for k in ('file','sha256','commit_file','commit_sha256'))
 raw=lambda prefix:finite0_saved_raw_family(data,prefix)
 pairs=lambda prefix:finite0_saved_pair_family(data,prefix)
 duals=lambda prefix:finite0_saved_dual_family(data,prefix)
 s=raw('completed_candidate_s_');c=raw('completed_candidate_c_');p=len(c['N']);assert p==3784
 feature=dict(constants={n:s[n] for n in ('g','hi','U','z','P','uc','Z','r','z2','f','phi','omega','xi','w')},paired=pairs('completed_candidate_features_'),configuration_changed=False,candidate_configuration_rebuilt=True)
 candidate=dict(s=s,c=c,jets=pairs('completed_candidate_jets_'),features=feature,momenta=pairs('completed_candidate_momenta_'),KADM=finite0_saved_pair(data,'completed_candidate_KADM'),positive_first_jet_envelopes=raw('candidate_raw_new_first_operation_'),coefficient_envelopes=raw('candidate_raw_coefficient_operation_'),canonical_target_references=refs['canonical_columns'][iq],prior_bridge_references=refs['prior_readout'],original_offsets_refitted=False,candidate_action_JVP_evaluated=False,phase_EOS_or_normal_weakrows_evaluated=False,physical_adoption=False)
 contact=dict(d=pairs('completed_contact_d_'),dc=pairs('completed_contact_dc_'),delta_features=dict(paired=pairs('completed_contact_delta_features_paired_'),configuration=pairs('completed_contact_delta_features_configuration_'),fixed_rates_gauge_spectrum_and_phase_jets=True),delta_momenta=pairs('completed_contact_delta_momenta_'),state=duals('completed_contact_state_'),geometry_rounding_map_differentiated=False,phase_relative_owned_by_separate_literal_core=True,old_coefficients_transported=False,physical_adoption=False)
 for n in ('h_first','delta_h_first','inverse_first','delta_inverse_first'):contact[n]=finite0_saved_pair(data,'completed_contact_'+n)
 curvature=duals('completed_curvature_');curvature.update(operation_envelopes=raw('completed_curvature_operation_envelopes_'),old_curvature_transported=False)
 eos=dict(value=pairs('completed_phase_value_'),delta=pairs('completed_phase_delta_'),PXXX=finite0_saved_pair(data,'completed_phase_PXXX'),constants=registered_constants,current_operation_envelope=data['completed_phase_current_operation_envelope'].copy(),H_operation_envelope=data['completed_phase_H_operation_envelope'].copy(),candidate_pressure_recomputed_from_invariant=True,owned_pressure_u_used=False,paired_input_collapsed=False,elementary_log_accuracy_admitted=False,fixed_phase_charge_restored=False,finite_candidate_physically_admitted=False)
 ordinary=dict(value=pairs('completed_mean_value_'),delta=pairs('completed_mean_delta_'),energy_metric_direction_contact=finite0_saved_pair(data,'completed_mean_energy_metric_direction_contact'),existing_labels_and_mean_weights_unchanged=True,extra_volume_factor_or_budget_subtraction_introduced=False,physical_adoption=False)
 geometry=pairs('NEW_reference_input_geometry_');gauge=pairs('NEW_reference_input_gauge_');covectors=pairs('NEW_reference_input_covectors_');mechanical=pairs('NEW_reference_input_mechanical_');phase=pairs('NEW_reference_input_phase_');direction=pairs('NEW_reference_input_direction_')
 material=raw('NEW_reference_input_material_')
 for n in ('B','GC','ALPHA','ELL','C'):material[n]=data['candidate_raw_unchanged_material_'+n].item();assert material[n]==getattr(P,n)
 reference=pairs('NEW_reference_input_reference_');reference.update(canonical_targets=refs['canonical_columns'][iq],prior_bridge_references=refs['prior_readout'])
 model=dict(value={n:finite0_saved_pair(data,'candidate_raw_model_'+n+'_paired_model') for n in ('g','hi','U','z','uc','P','up','gamma','dens')},delta={})
 inputs=(geometry,model,gauge,covectors,mechanical,phase,material,reference)
 sp={n:P.a_dd(s[n]) for n in ('g','hi','U','uc','P','phi')};cp={n:P.a_dd(c[n]) for n in ('N','beta','h','ih','u')};cp['mu']=P.a_dd(c['sqrt_h'])
 D={**contact['d'],**contact['dc']};D['mu']=contact['dc']['sqrt_h']
 fixed,bg=input_metadata['fixed'],input_metadata['owned_background'];Hbar=bg['h']*fixed['Hunit']/299792458.
 assert np.isfinite(Hbar) and Hbar>0
 return dict(candidate=candidate,contact=contact,curvature=curvature,eos=eos,ordinary=ordinary,s=sp,c=cp,D=D,inputs=inputs,direction=direction,Hbar=Hbar,column=iq,restored_completed_STATE=True,completed_action_replayed=False,typed_flags_restored_from_source=True,EOS_constants_required_by_remaining_tests=False,physical_adoption=False)
