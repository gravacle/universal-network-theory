"""HELD finite196 source-owned scalar/zero/copy normalization only.
Globals np,P,keep,candidate_phase_registered_constants are exact selected sources.
Containing admission authenticates every selected original INPUT/STATE/SHEET ref.
No prior array is claimed to exist when its source law constructs a zero field.
"""
FINITE196_SOURCE_OPERANDS_AUTHOR_DRAFT=True
FINITE196_SOURCE_OPERANDS_AUTHORING_IN_PROGRESS=False
FINITE196_SOURCE_OPERANDS_PRIVATE_SCOPE=False
FINITE196_SOURCE_OPERANDS_BINDING=(None,None)
FINITE196_SOURCE_OPERANDS_PINS={
 'cross_u_finite0_candidate_action_residual_v007.py':'ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58',
 'author_fragment_point_TOTAL_trial_fields_v001.py':'96925b148cb7c1b3660e76867e5c499e9b10868bc737209b194d9c667adc46ef',
 'author_fragment_total_trial_fields_to_column_v001.py':'c0c3f97320301834666f35db66195aa5715c182dd2bb29ec4e957433808aaf94',
 'author_fragment_fresh_trial_residual_packet_v001.py':'5814945f10ed230da7a26d234c83b49966a2376e692f81a55c0b38d077d48af4',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae'}


def finite196_source_pair(value,shape,keep,label):
 assert isinstance(value,np.ndarray) and value.dtype==np.float64 and value.shape==shape and np.all(np.isfinite(value))
 out=P.a_dd(value.copy())
 for w,a in zip(('hi','lo'),out):keep(label+'_'+w,a.copy())
 assert np.array_equal(out[0].view(np.uint64),value.view(np.uint64)) and np.all(out[1]==0)
 return out


def finite196_materialize_source_owned_operands(data,provenance,keep,label):
 assert not FINITE196_SOURCE_OPERANDS_AUTHOR_DRAFT and not FINITE196_SOURCE_OPERANDS_AUTHORING_IN_PROGRESS and FINITE196_SOURCE_OPERANDS_PRIVATE_SCOPE is True
 assert all(x is not None for x in FINITE196_SOURCE_OPERANDS_BINDING)
 assert provenance['source_operand_binding']==FINITE196_SOURCE_OPERANDS_BINDING and provenance['source_operand_pins']==FINITE196_SOURCE_OPERANDS_PINS
 assert provenance['all_source_operand_and_metadata_seals_authenticated'] is True and provenance['physical_adoption'] is False
 md=data['_source_metadata'];original=md['original_input']
 assert original['owner']['pid']==94049 and original['owner']['source_sha256']==FINITE196_SOURCE_OPERANDS_PINS['cross_u_finite0_candidate_action_residual_v007.py']
 assert original['kind']=='owned_current_mechanical_time_words_reference_finite_candidate' and original['rho']==0. and original['compact_direction_node']==[43,22]
 assert md['anchor_input']['owner']['pid']==21562 and md['anchor_input']['rho_W_t_all_exact_zero'] is True
 assert len(md['anchor_columns'])==4 and all(x['owner']['pid']==21562 and x['column']==iq and x['rho_W_t_exact_zero'] is True for iq,x in enumerate(md['anchor_columns']))
 assert md['sheet']['owner']['pid']==97585 and md['sheet']['finite_rho']==0. and md['sheet']['labels_and_locations_unchanged'] is True
 assert data['previous_configuration'] is None,'Only the source-declared original zero chart is materialized'
 out=dict(data);out['previous_configuration']={}
 for n,shape in (('chi',(87,45)),('W',(3,87,45)),('t',(87,45))):
  out['previous_configuration'][n]=finite196_source_pair(np.zeros(shape,dtype=np.float64),shape,keep,label+'_source_defined_previous_zero_'+n)
 out['source_defined_zero_configuration_not_archived_array']=dict(original_input=provenance['original_input'],anchor_input=provenance['anchor_input'],anchor_columns=provenance['anchor_columns'],original_sheet=provenance['original_sheet'],new_source_construction=True)
 assert len(data['fixed_columns'])==4
 out['fixed_columns']=[]
 constants=candidate_phase_registered_constants(original['fixed'])
 assert constants['synthetic_control'] is False
 for n,v in constants.items():
  if type(v) in (int,float):keep(label+'_original_registered_phase_constant_'+n,np.asarray(v).copy())
 for iq,item in enumerate(data['fixed_columns']):
  fixed=dict(item);material=dict(item['material'])
  for n in ('B','GC','ALPHA','ELL','C'):
   a=material[n];assert isinstance(a,np.ndarray) and a.dtype==np.float64 and a.shape==() and np.isfinite(a) and a>0
   keep(label+'_column%d_archived_material_'%iq+n,a.copy());material[n]=a.item()
   assert type(material[n]) is float and material[n]==getattr(P,n)
  fixed['material']=material;fixed['phase_constants']=dict(constants)
  phi=item['point_TOTAL']['phi'];assert isinstance(phi,tuple) and len(phi)==2 and all(a.dtype==np.float64 and a.shape==(3784,4) and np.all(np.isfinite(a)) for a in phi)
  assert item['phase_spatial'] is None
  fixed['phase_spatial']=tuple(a[:,1:].copy() for a in phi)
  for w,a in zip(('hi','lo'),fixed['phase_spatial']):
   keep(label+'_column%d_copied_updated_spatial_phase_'%iq+w,a.copy());assert np.array_equal(a.view(np.uint64),phi[0 if w=='hi' else 1][:,1:].view(np.uint64))
  # Point TOTAL u/z/h_dot and all genuine gauge jets stay exactly as selected.
  out['fixed_columns'].append(fixed)
 assert data['Hbar'] is None
 out['Hbar']=original['owned_background']['h']*original['fixed']['Hunit']/299792458.
 assert np.isfinite(out['Hbar']) and out['Hbar']>0
 keep(label+'_original_F0_Hbar_association',np.asarray(out['Hbar']).copy())
 assert data['original_six_references']['native_affine'] is None and data['original_six_references']['metric_original_epsilon'] is None
 refs=dict(data['original_six_references'])
 rhs=data['_original_six_archived']['original_rhs'];assert rhs.dtype==np.float64 and rhs.shape==(403340,) and np.all(np.isfinite(rhs))
 refs['native_affine']=P.unpack_fields(rhs,False)[0]
 keep(label+'_original_native_affine_reference',refs['native_affine'].copy())
 eps=data['_original_six_archived']['metric_epsilon'];assert all(a.dtype==np.float64 and a.shape==(6,87,45) and np.all(np.isfinite(a)) for a in eps)
 refs['metric_original_epsilon']=P.collapse(eps)
 keep(label+'_original_metric_epsilon_denominator',refs['metric_original_epsilon'].copy())
 out['original_six_references']=refs
 assert data['priors']['nominal_metric'] is None
 out['priors']=dict(data['priors'],nominal_metric=finite196_source_pair(data['_archived_nominal_metric'],(6,87,45),keep,label+'_unchanged_nominal_metric'))
 assert data['sheet_labels'] is None
 src=data['sheet_source'];p=src['R'].size;assert p==4832 and src['fixed_labels_and_positions_verified'] is True
 out['sheet_labels']=dict(galaxy_mass_weight=finite196_source_pair(src['mass_weight'],(p,),keep,label+'_source_sheet_mass'),galaxy_specific_covector=finite196_source_pair(src['specific_covariant_p'],(p,3),keep,label+'_source_sheet_covector'),
  reference_dust_energy_weight=finite196_source_pair(np.zeros(p,dtype=np.float64),(p,),keep,label+'_source_sheet_zero_dust'),
  radiation_weights=finite196_source_pair(np.zeros((0,p),dtype=np.float64),(0,p),keep,label+'_source_sheet_empty_radiation_weights'),
  radiation_covectors=finite196_source_pair(np.zeros((0,p,3),dtype=np.float64),(0,p,3),keep,label+'_source_sheet_empty_radiation_covectors'),
  existing_once_counted_branch_registered=True,provenance=src['provenance'])
 out['source_operand_materialization_scope']=dict(archived_material_scalar_copy_only=True,updated_spatial_phase_copy_only=True,zero_chart_and_zero_sheet_terms_from_original_F0_source=True,registered_phase_constants_from_original_fixed_metadata=True,
  original_six_reference_associations_unchanged=True,old_geometry_current_EOS_normal_or_control_replayed=False,physical_adoption=False)
 return out
