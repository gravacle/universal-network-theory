"""HELD consumer of three NEW fixed-rate local conformal-jet responses.
Globals np,P, reviewed mp_add/mp_mul/mp_sum. No producer, I/O or callback runs.
Three columns represent the declared frozen-coefficient law, not bitwise DD
linearity. Complete original290 remains the association/finite-state authority.
Independent source unsigned columns are required; |signed response| is no substitute.
"""
CONFIGURATION_JET_COEFFICIENT_AUTHOR_DRAFT=True
CONFIGURATION_JET_COEFFICIENT_AUTHORING_IN_PROGRESS=False
CONFIGURATION_JET_UNIT_SOURCE=(None,None)
CONFIGURATION_JET_UNIT_RESULT=(None,None,None)
CONFIGURATION_JET_UNIT_RECEIPT=(None,None,'CLOSED')
CONFIGURATION_JET_UNIT_PROOF=(None,None,None)
CONFIGURATION_JET_PARENT_PINS={
 'author_fragment_candidate_whole_configuration_york_contact_v001.py':'0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'author_fragment_finite_candidate_native_EH_normal_v003.py':'5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499',
 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py':'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94'}


def qj_pair(label,pair,keep,shape=None):
 assert isinstance(pair,tuple) and len(pair)==2
 keep(label+'_both_words',np.stack(pair).copy())
 for word,a in zip(('hi','lo'),pair):
  keep(label+'_'+word,np.asarray(a).copy())
  assert a.dtype==np.float64 and a.shape==pair[0].shape and np.all(np.isfinite(a))
  assert shape is None or a.shape==shape
 return pair


def prepare_candidate_configuration_jet_coefficients(responses,source_envelopes,provenance,keep,label):
 assert not CONFIGURATION_JET_COEFFICIENT_AUTHOR_DRAFT and not CONFIGURATION_JET_COEFFICIENT_AUTHORING_IN_PROGRESS
 assert all(x is not None for ref in (CONFIGURATION_JET_UNIT_SOURCE,CONFIGURATION_JET_UNIT_RESULT,CONFIGURATION_JET_UNIT_RECEIPT,CONFIGURATION_JET_UNIT_PROOF) for x in ref),'Authentic CLOSED NEW three-unit preparation required'
 assert len(responses)==len(source_envelopes)==3 and provenance['updated_phase_state_owner']==13764
 assert provenance['naturally_closed'] is True and provenance['all_selected_seals_verified'] is True
 assert provenance['same_geometry_full99_plus6_current_rates_and_York_reference'] is True and provenance['physical_adoption'] is False
 assert provenance['unit_source']==CONFIGURATION_JET_UNIT_SOURCE and provenance['unit_result']==CONFIGURATION_JET_UNIT_RESULT
 assert provenance['unit_receipt']==CONFIGURATION_JET_UNIT_RECEIPT and provenance['unit_proof']==CONFIGURATION_JET_UNIT_PROOF
 p=responses[0]['normal_coefficients'][0].shape[0];assert 1<=p<=3784
 shapes=dict(mechanical=(p,105),phase=(p,),normal=(p,4,4),CMC=(p,));fields={n:[] for n in shapes};bounds={n:[] for n in shapes}
 for jet,(part,envelope) in enumerate(zip(responses,source_envelopes)):
  unit=qj_pair(label+'_unit%d_original_local_chi_jets'%jet,part['chi_jets'],keep,(p,3))
  expected=np.zeros((p,3));expected[:,jet]=1.
  assert np.array_equal(unit[0],expected) and np.all(unit[1]==0),'Exactly three NEW (1,0) point jet columns required'
  assert part['provenance']['new_unit_response'] is True and part['provenance']['old_q22_or_direction_action_replayed'] is False
  assert part['provenance']['same_candidate_provenance']==provenance['same_candidate_provenance']
  for n in ('h_dot','u_jets','z_jets'):
   qj_pair(label+'_unit%d_fixed_rates_'%jet+n,part['direction'][n],keep)
   assert all(np.all(a==0) for a in part['direction'][n])
  dm=part['contact']['delta_momenta'];native=qj_pair(label+'_unit%d_native99'%jet,dm['native_density'],keep,(p,99));metric=qj_pair(label+'_unit%d_metric6'%jet,dm['metric_total_density'],keep,(p,6))
  supplied=dict(mechanical=tuple(np.concatenate((native[w],metric[w]),axis=1) for w in (0,1)),phase=part['eos']['delta']['p'],normal=part['normal_coefficients'],CMC=part['initial_CMC_density'])
  assert envelope['source_terms_before_output_cancellation'] is True and envelope['signed_response_magnitude_used_as_bound'] is False
  assert envelope['same_unit_response_provenance']==part['provenance'] and envelope['upstream_EFT_error_bound_qualified'] is False
  for n,shape in shapes.items():
   x=qj_pair(label+'_unit%d_'%jet+n,supplied[n],keep,shape);e=keep(label+'_unit%d_source_unsigned_'%jet+n,np.asarray(envelope['fields'][n]).copy())
   assert e.dtype==np.float64 and e.shape==shape and np.all(np.isfinite(e)) and np.all(e>=0)
   fields[n].append(tuple(w.copy() for w in x));bounds[n].append(e.copy())
  if jet>0:assert all(np.all(w==0) for w in supplied['phase']),'Cached literal phase current has no first-spatial-jet dependence'
 coefficients={n:qj_pair(label+'_completed_coefficient_'+n,P.a_stack(fields[n],-1),keep,shape+(3,)) for n,shape in shapes.items()}
 envelopes={n:keep(label+'_completed_unsigned_'+n,np.stack(bounds[n],axis=-1)) for n in shapes}
 return dict(coefficients=coefficients,envelopes=envelopes,points=p,provenance=provenance,original_normal_test_order=('value','R','Z','t'),source_coefficient_law_only=True,arbitrary_DD_linearity_or_uniform_association_qualified=False,York_target_action_included=False,sheet_action_included=False,global_inverse_or_physical_adoption=False)


def candidate_configuration_jet_point_action(prepared,rho,rho_gradient,keep,label):
 assert not CONFIGURATION_JET_COEFFICIENT_AUTHOR_DRAFT and prepared['global_inverse_or_physical_adoption'] is False
 p=prepared['points'];qj_pair(label+'_rho',rho,keep,(p,));qj_pair(label+'_rho_R_Z',rho_gradient,keep,(p,2))
 jets=qj_pair(label+'_local_input_jets',P.a_stack([rho]+[P.a_slice(rho_gradient,(slice(None),a)) for a in (0,1)],-1),keep,(p,3));out={}
 for name,coeff in prepared['coefficients'].items():
  value=P.a_dd(np.zeros(coeff[0].shape[:-1]));qj_pair(label+'_'+name+'_initial_zero',value,keep)
  for jet in range(3):
   scalar=P.a_slice(jets,(slice(None),jet));key=(slice(None),)+(None,)*(value[0].ndim-1)
   term=qj_pair(label+'_'+name+'_jet%d_product'%jet,P.a_mul(P.a_slice(coeff,(Ellipsis,jet)),tuple(w[key] for w in scalar)),keep,value[0].shape)
   value=qj_pair(label+'_'+name+'_ordered_partial%d'%jet,P.a_add(value,term),keep,value[0].shape)
  out[name]=value
 mechanical=out['mechanical'];out.update(native=P.a_slice(mechanical,(slice(None),slice(0,99))),metric_current=P.a_slice(mechanical,(slice(None),slice(99,None))))
 for name in ('native','metric_current'):qj_pair(label+'_completed_'+name,out[name],keep)
 return dict(point=out,configuration_jet_order=('rho','rho_R','rho_Z'),current_only=True,metric_York_target_subtraction_external=True,ordinary_sheet_external=True,full290_association_validation_required=True,exact_DD_Jacobian_or_normal_acceptance=False,physical_adoption=False)


def candidate_configuration_jet_point_positive(prepared,rho,rho_gradient,keep,label):
 assert not CONFIGURATION_JET_COEFFICIENT_AUTHOR_DRAFT and prepared['global_inverse_or_physical_adoption'] is False
 p=prepared['points'];qj_pair(label+'_rho_words',rho,keep,(p,));qj_pair(label+'_gradient_words',rho_gradient,keep,(p,2))
 jets=P.a_stack([rho]+[P.a_slice(rho_gradient,(slice(None),a)) for a in (0,1)],-1)
 magnitude=mp_add(abs(jets[0]),abs(jets[1]),keep,label+'_input_word_magnitude');out={}
 for name,e in prepared['envelopes'].items():
  key=(slice(None),)+(None,)*(e.ndim-2)+(slice(None),)
  terms=mp_mul(e,magnitude[key],keep,label+'_'+name+'_uncancelled_terms');out[name]=mp_sum(terms,-1,keep,label+'_'+name+'_unsigned_sum')
 return dict(point=out,source_unsigned_columns_used=True,response_gap_or_floor_used=False,source_coefficient_contraction_bound_only=True,upstream_EFT_error_or_uniform290_association_qualified=False,physical_adoption=False)
