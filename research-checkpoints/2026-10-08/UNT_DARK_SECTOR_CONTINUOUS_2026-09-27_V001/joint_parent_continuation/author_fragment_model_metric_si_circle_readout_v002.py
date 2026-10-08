"""Definitions-only native313->SI tensor/readout adapter; no metric is supplied here.
Caller supplies np, math, G (resident geometry API) and CIRCLE (reviewed dynamic API).
No field solve, observer fit, source change, low-word collapse or file IO occurs.
"""
MODEL_SI_CIRCLE_AUTHOR_DRAFT = True
MODEL_SI_UNIT_SOURCE_PINS = {
 'CROSS_U_EPS5_MACRO_BACKGROUND_CALLER_REGISTRATION_V001.md':'087b59df9fd2ef89b3f471fa5fc8a6b0e5a1102b8c37f6d2d6e377f8130e2523',
 'cross_u_saved_full_metric_native_source_residual_v001.py':'23ff7ab909e60f4cd5ab96e12ea7cc1bc64e07821ebb11dd5cec28a9a02f5d68',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_full_dynamic_metric_circle_v002.py':'3be37b2181ff154067ccd0d01587266ce64a58a118bd6dbd331fca1f49001c6b',
 'cross_u_full_metric_geodesic_and_rotating_material_v001.py':'53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa'}


def native_313_si_registration():
 # Macro registration: t313=cp*tsecond/L0; provider uses (t313,Rkpc,Zkpc,phi), c=1.
 L0=3.085677581491367e19;cp=299792458.
 J=np.diag(np.array((cp/L0,1/L0,1/L0,1.),dtype=np.float64))
 return dict(metric_length_unit_m=L0,cp_m_per_s=cp,dmodel_dSI=J,
             model_coordinates=('t313','R_kpc','Z_kpc','phi_rad'),
             SI_coordinates=('t_second','R_metre','Z_metre','phi_rad'),
             metric_relation='dsSI_squared=L0_squared*ds313_squared',
             time_relation='t313=cp*t_second/L0',source_pins=dict(MODEL_SI_UNIT_SOURCE_PINS))


def affine_metric_unit_pullback(g_model,dg_model,jacobian,metric_length_unit_m):
 # y_model=J*x_new+constant. Constant origin never enters the local tensor/jet.
 g=np.asarray(g_model);dg=np.asarray(dg_model);J=np.asarray(jacobian)
 assert g.shape==(4,4) and dg.shape==(4,4,4) and J.shape==(4,4)
 assert all(x.dtype==np.dtype('float64') and np.all(np.isfinite(x)) for x in (g,dg,J))
 assert np.array_equal(g,g.T) and np.array_equal(dg,dg.swapaxes(1,2)),'Supplied symmetry required; no repair'
 L=float(metric_length_unit_m);assert math.isfinite(L) and L>0
 L2=L*L;det=float(np.linalg.det(J));assert math.isfinite(L2) and L2>0 and math.isfinite(det) and det!=0
 out=np.zeros((4,4));jet=np.zeros((4,4,4));eg=np.zeros_like(out);edg=np.zeros_like(jet)
 # One construction per independent symmetric component, then exact copies.
 for m in range(4):
  for n in range(m,4):
   value=L2*np.einsum('i,ij,j->',J[:,m],g,J[:,n])
   bound=L2*np.einsum('i,ij,j->',abs(J[:,m]),abs(g),abs(J[:,n]))
   out[m,n]=out[n,m]=value;eg[m,n]=eg[n,m]=bound
   for a in range(4):
    value=L2*np.einsum('l,i,lij,j->',J[:,a],J[:,m],dg,J[:,n])
    bound=L2*np.einsum('l,i,lij,j->',abs(J[:,a]),abs(J[:,m]),abs(dg),abs(J[:,n]))
    jet[a,m,n]=jet[a,n,m]=value;edg[a,m,n]=edg[a,n,m]=bound
 assert all(np.all(np.isfinite(x)) for x in (out,jet,eg,edg))
 return dict(g=out,dg=jet,g_operation_envelope=eg,dg_operation_envelope=edg,
             supplied_g=g.copy(),supplied_dg=dg.copy(),jacobian=J.copy(),metric_length_unit_m=L,
             derivative_index_first=True,affine_origin_requires_caller_event_registration=True)


def q1_radial_readout_contact(r_model,model_R,*,catalogue_R_kpc,mapping,side):
 r=np.asarray(r_model);R=float(model_R);catalogue=float(catalogue_R_kpc)
 assert r.ndim==1 and r.dtype==np.dtype('float64') and len(r)>=3 and np.all(np.isfinite(r)) and np.all(np.diff(r)>0)
 assert math.isfinite(R) and math.isfinite(catalogue) and catalogue>0 and r[0]<R<=r[-1]
 assert side in ('left','right') and isinstance(mapping,dict) and mapping
 assert mapping['kind'] in ('coordinate_R_equals_catalogue_kpc','supplied_radius_map')
 if mapping['kind']=='coordinate_R_equals_catalogue_kpc':assert R==catalogue
 else:assert isinstance(mapping['provenance'],dict) and mapping['provenance']
 endpoint=bool(R==r[-1]);assert not endpoint or side=='left','Outer RIGHT jet requires registered exterior'
 i=int(np.searchsorted(r,R,side='left'));node=bool(r[i]==R);left=i-1;right=None if endpoint else (i if node else left)
 cell=left if side=='left' else right;dr=float(r[cell+1]-r[cell]);t=(R-r[cell])/dr
 assert 0<=t<=1
 return dict(model_R=R,catalogue_R_kpc=catalogue,mapping=dict(mapping),exact_mesh_node=node,
             left_cell=left,right_cell=right,outer_endpoint=endpoint,right_interior_jet_defined=not endpoint,
             selected_side=side,selected_cell=cell,
             value_weights=np.array((1-t,t)),radial_derivative_weights=np.array((-1/dr,1/dr)),
             Q1_scope='actual open-cell derivative or declared one-sided node limit; no smoothed slope',
             sheet_vertical_jet_registration_required=True,extrapolation_performed=False)


def orient_dynamic_circle_candidates(result,orientation):
 assert type(orientation) is int and orientation in (-1,1)
 candidates=[];matching=[]
 for index,value in enumerate(result['candidates']):
  v=float(value['normal_axial_velocity']);assert math.isfinite(v)
  matches=orientation*v>=0
  row=dict(value,signed_local_axial_velocity_kms=v/1000.,
           declared_orientation_speed_kms=orientation*v/1000.,matches_declared_orientation=matches)
  candidates.append(row)
  if matches:matching.append(index)
 return dict(dynamic_readout=result,candidates=candidates,declared_rotation_orientation=orientation,
             matching_indices=matching,selected_index=matching[0] if len(matching)==1 else None,
             orientation_status='unique_oriented_radial_root' if len(matching)==1 else
             ('no_oriented_radial_root' if not matching else 'multiple_oriented_radial_roots'),
             vertical_time_and_geodesic_diagnostics_preserved=True,orientation_chosen_using_observations=False,
             physical_circle_or_observational_acceptance_performed=False)


def supplied_model_local_circle_event(g_model,dg_model,*,radius_contact,orientation,
                                      input_scope,metric_admission,readout_precision_admission):
 assert input_scope in ('new_analytic_control','conditional_finite_metric','finite_physical_metric')
 assert isinstance(metric_admission,dict) and isinstance(readout_precision_admission,dict)
 if input_scope=='finite_physical_metric':
  assert metric_admission.get('finite_physical_metric_admitted') is True and metric_admission.get('provenance')
  assert readout_precision_admission.get('binary64_readout_admitted') is True and readout_precision_admission.get('provenance')
 elif input_scope=='conditional_finite_metric':
  assert metric_admission.get('finite_constraint_solution_admitted') is True and metric_admission.get('provenance')
  assert isinstance(metric_admission.get('declared_conditional_boundary'),dict) and metric_admission['declared_conditional_boundary']
  assert metric_admission.get('finite_physical_metric_admitted') is False
  assert readout_precision_admission.get('binary64_readout_admitted') is True and readout_precision_admission.get('provenance')
 else:assert metric_admission.get('finite_physical_metric_admitted') is False
 assert isinstance(radius_contact,dict) and radius_contact['selected_side'] in ('left','right')
 units=native_313_si_registration()
 pulled=affine_metric_unit_pullback(g_model,dg_model,units['dmodel_dSI'],units['metric_length_unit_m'])
 geometry=G.metric_geometry(pulled['g'],pulled['dg'],units['cp_m_per_s'])
 dynamic=CIRCLE.full_dynamic_circle_candidates(geometry,azimuth=3,meridional=(1,2),radial=1)
 oriented=orient_dynamic_circle_candidates(dynamic,orientation)
 return dict(units=units,pullback=pulled,geometry=geometry,readout=oriented,
             radius_contact=dict(radius_contact),input_scope=input_scope,
             supplied_metric_admission=dict(metric_admission),supplied_readout_precision_admission=dict(readout_precision_admission),
             prediction_kind='local_metric_circular_snapshot',metric_computed_by_adapter=False,
             galaxy_diagnostic_allowed=input_scope!='new_analytic_control',
             physical_metric_admitted=input_scope=='finite_physical_metric',
             persistent_orbit_stability_or_observational_translation_qualified=False,
             supplied_pair_words_collapsed=False)
