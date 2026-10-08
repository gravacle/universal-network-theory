"""HELD direct baseline TOTAL hdot plus original Fhat CORRECTION event adapter.
Import-free; globals np,P,H,REPORT and retained fce_* geometry/readout helpers.
The containing owner authenticates direct event records and all closed operands.
No source, Gauss interpolation, nodal TOTAL reconstruction or numerical runner.
"""
DIRECT_TOTAL43_AUTHOR_DRAFT=True
DIRECT_TOTAL43_AUTHORING_IN_PROGRESS=False
DIRECT_TOTAL43_PARENT_PINS={
 'coupled':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'finite':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'direct_baseline':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)}}
DIRECT_TOTAL43_SOURCE_PINS={
 'author_fragment_finite_conformal_circle_event_v001.py':'b607fcf3346d83e012771e75d9b658cef9ad51aeac4de09ad0a69bb3d75489b1',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'author_fragment_revised_43_observer_report_v002.py':'0cab1853d083239175943a4765101a95104949bb14f13ca1eb9902713df92843',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70'}
DIRECT_TOTAL43_CATALOGUE=('NGC3198_FINE_Q3_43_POINT_SAVED_RECAP_V001.json','ea6e41a879bab1ed43fa556031ad96ae3535779707af62d30eff061b191fc024')
DIRECT_TOTAL43_ROW_PATH=('rows',)
DIRECT_TOTAL43_FIELDS={'radius':('R_kpc',),'observed':('observed_velocity_kms',),'sigma':('quoted_error_kms',),'model':('Q1_predicted_velocity_kms',)}

def direct_TOTAL43_sample_correction(r,z,total_chi,metric_correction,*,R,radial_side,keep,label):
 fce_pair(label+'_finite_TOTAL_chi_nodes',total_chi,keep,(87,45));fce_pair(label+'_metric_CORRECTION_nodes',metric_correction,keep,(6,87,45))
 mask=P.scalar_mask().copy();mask[-1]=False;mask[:,-1]=False
 assert np.count_nonzero(mask)==3740 and all(np.all(w[~mask]==0) for w in total_chi)
 assert all(np.all(w[~P.metric_mask()]==0) for w in metric_correction)
 for n,a,shape in (('R',r,(87,)),('Z',z,(45,))):
  keep(label+'_original_mesh_'+n,np.asarray(a).copy());assert a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(np.diff(a)>0)
 assert r[0]==z[0]==0 and z[1]>0
 contact=H.q1_radial_readout_contact(r,R,catalogue_R_kpc=R,mapping=dict(kind='coordinate_R_equals_catalogue_kpc'),side=radial_side)
 i=contact['selected_cell'];w=contact['value_weights'];d=contact['radial_derivative_weights'];dz=z[1]-z[0]
 weights=np.array(((w[0],w[1],0.,0.),(d[0],d[1],0.,0.),(-w[0]/dz,-w[1]/dz,w[0]/dz,w[1]/dz)))
 keep(label+'_positive_sheet_value_R_Z_weights',weights.copy());corners=((i,0),(i+1,0),(i,1),(i+1,1))
 scalar=tuple(P.scalar_lift(a) for a in total_chi);lifted=tuple(P.lift_metric(a) for a in metric_correction)
 fce_pair(label+'_axis_extended_TOTAL_chi',scalar,keep,(87,45));fce_pair(label+'_axis_sheet_extended_CORRECTION',lifted,keep,(6,87,45))
 rho=[P.a_dd(np.asarray(0.)) for unused in range(3)];six=P.a_dd(np.zeros(6));F=P.dd_metric_F(np.asarray(R));keep(label+'_original_event_F',F.copy())
 for corner,(ci,cj) in enumerate(corners):
  a=fce_pair(label+'_chi_corner%d'%corner,tuple(v[ci,cj].copy() for v in scalar),keep,())
  for jet in range(3):
   product=fce_pair(label+'_chi_corner%d_jet%d_product'%(corner,jet),P.a_mul64(weights[jet,corner],a),keep,())
   rho[jet]=fce_pair(label+'_chi_jet%d_partial'%jet,P.a_add(rho[jet],product),keep,())
  a=fce_pair(label+'_CORRECTION_corner%d'%corner,tuple(v[:,ci,cj].copy() for v in lifted),keep,(6,));Fhat=weights[0,corner]*F
  keep(label+'_original_rounded_Fhat_corner%d'%corner,Fhat.copy())
  product=fce_pair(label+'_CORRECTION_time_corner%d'%corner,P.a_matvec(Fhat,a),keep,(6,));six=fce_pair(label+'_CORRECTION_time_partial',P.a_add(six,product),keep,(6,))
 ht=P.a_dd(np.zeros((3,3)))
 for slot,(a,b) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for word in (0,1):ht[word][a,b]=ht[word][b,a]=six[word][slot]
 return dict(rho=rho[0],rho_gradient=P.a_stack(rho[1:],0),delta_h_dot=fce_pair(label+'_physical_hdot_CORRECTION',ht,keep,(3,3)),radius_contact=contact,corners=corners)

def direct_TOTAL43_finite_event(reference,baseline_h_dot,r,z,total_chi,metric_correction,*,R,radial_side,admission,keep,label):
 assert not DIRECT_TOTAL43_AUTHOR_DRAFT and not DIRECT_TOTAL43_AUTHORING_IN_PROGRESS
 assert admission['source_pins']==DIRECT_TOTAL43_SOURCE_PINS
 for group,pins in DIRECT_TOTAL43_PARENT_PINS.items():
  parent=admission[group]
  for n,pin in pins.items():assert all(v is not None for v in pin) and tuple(parent[n])==tuple(pin)
  assert parent['naturally_closed'] is True and parent['exit_code']==0 and parent['all_selected_seals_verified'] is True
 closure=admission['finite']['metric_admission']
 assert closure['finite_constraint_solution_admitted'] is closure['finite_domains_admitted'] is True and closure['finite_physical_metric_admitted'] is False
 assert closure['provenance'] and closure['declared_conditional_boundary'] and reference['provenance']
 assert reference['same_reference_as_finite_candidate']==closure['reference_provenance'] and reference['direct_event_data_not_Gauss_interpolation'] is True
 assert reference['R']==R and reference['Z']==0 and reference['radial_side']==radial_side and radial_side in ('left','right')
 assert admission['coordinate_event']==[0.,R,0.,0.] and admission['original_mesh_and_basis_words_verified'] is True
 assert admission['point_TOTAL_addition_after_original_lift'] is True and admission['baseline_event_TOTAL_hdot_matches_finite_BASELINE_before_correction'] is True
 assert admission['total_chi_matches_finite_TOTAL_nodes'] is True and admission['metric_correction_matches_coupled_increment'] is True
 for n in ('basis_record','total_chi_record','metric_correction_record','direct_baseline_event_record'):
  assert isinstance(admission[n],dict) and all(admission[n].get(k) for k in ('file','sha256','commit_file','commit_sha256'))
 fce_pair(label+'_DIRECT_baseline_TOTAL_hdot',baseline_h_dot,keep,(3,3));assert all(np.array_equal(w,w.T) for w in baseline_h_dot)
 sampled=direct_TOTAL43_sample_correction(r,z,total_chi,metric_correction,R=R,radial_side=radial_side,keep=keep,label=label+'_original_Q1')
 ht=fce_pair(label+'_NEW_event_TOTAL_hdot',P.a_add(baseline_h_dot,sampled['delta_h_dot']),keep,(3,3))
 geometry=fce_conformal_ADM_event(reference,sampled['rho'],sampled['rho_gradient'],ht,keep,label+'_finite_geometry')
 parity=np.array((1.,1.,-1.,1.));lower_g=tuple(w*parity[:,None]*parity[None,:] for w in geometry['g']);lower_dg=tuple(w*parity[:,None,None]*parity[None,:,None]*parity[None,None,:] for w in geometry['dg'])
 fce_pair(label+'_reflected_lower_g',lower_g,keep,(4,4));fce_pair(label+'_reflected_lower_dg',lower_dg,keep,(4,4,4))
 same=all(np.array_equal(a,b) for a,b in zip(geometry['g'],lower_g));keep(label+'_reflection_metric_sheet_match',np.asarray(same,dtype=np.int64))
 return dict(upper=dict(g=geometry['g'],dg=geometry['dg']),lower=dict(g=lower_g,dg=lower_dg),geometry=geometry,sampling=sampled,closure=closure,
  coordinate_event=(0.,R,0.,0.),radial_side=radial_side,reference_provenance=reference['provenance'],sheet_reflection_metric_match=same,
  baseline_TOTAL_event_record=admission['direct_baseline_event_record'],baseline_TOTAL_hdot=baseline_h_dot,metric_CORRECTION_record=admission['metric_correction_record'],event_TOTAL_hdot=ht,
  point_TOTAL_addition_after_original_lift=True,nodal_TOTAL_equivalence_earned=False,Gauss_metric_or_jets_interpolated=False,
  lapse_shift_and_all_gauge_jets_held=True,W_t_direct_geometry_zero=True,configuration_changed=True,physical_metric_admitted=False)

def direct_TOTAL43_report_from_completed(baseline_document,completed,*,catalogue_admission,finite_closure,domain_admission,provenance,requested_motion_scope):
 assert not DIRECT_TOTAL43_AUTHOR_DRAFT and not DIRECT_TOTAL43_AUTHORING_IN_PROGRESS and len(completed)==43 and requested_motion_scope in ('radial_balance_diagnostic','compatible_instantaneous_circle')
 assert tuple(catalogue_admission['reference'])==DIRECT_TOTAL43_CATALOGUE and catalogue_admission['bytes_authenticated'] is True
 assert finite_closure['finite_constraint_solution_admitted'] is domain_admission['finite_domains_admitted'] is True and finite_closure['finite_physical_metric_admitted'] is False
 old=REPORT.report43_path(baseline_document,DIRECT_TOTAL43_ROW_PATH);assert len(old)==43;rows=[];events=[]
 for index,(saved,item) in enumerate(zip(old,completed)):
  assert item['index']==index and item['all_selected_readout_seals_verified'] is True
  assert all(item['readout_ref'].get(k) for k in ('file','sha256','commit_file','commit_sha256'))
  event=item['event'];full=item['completed_circle_readout'];side=item['report_side'];assert side in full['sides'] and event['closure']==finite_closure
  assert full['finite_constraint_solution_admitted'] is True and item['report_side_selected_using_Vobs'] is False
  precision=full['supplied_precision_admission'];assert precision['binary64_readout_admitted'] is precision['paired_word_collapse_admitted'] is True
  assert precision['finite_event_provenance']==dict(closure=finite_closure['provenance'],reference=event['reference_provenance'],coordinate_event=list(event['coordinate_event']),radial_side=event['radial_side'])
  R=REPORT.report43_number(REPORT.report43_path(saved,DIRECT_TOTAL43_FIELDS['radius']));assert event['coordinate_event']==(0.,R,0.,0.)
  selection=full['sides'][side]['readout']['readout'];chosen=selection['selected_index'];orientation=selection['declared_rotation_orientation'];assert orientation==1
  gate=full['sides'][side]['supplied_circle_gate'];compatible=gate is not None and gate['admitted'] is True
  speed=None if chosen is None else selection['candidates'][chosen]['declared_orientation_speed_kms']
  velocity=speed if requested_motion_scope=='radial_balance_diagnostic' or compatible else None
  flags=dict(finite_constraint_solution_admitted=True,finite_domains_admitted=True,physical_metric_admitted=False,unique_oriented_radial_root=chosen is not None,readout_precision_admitted=True,full_instantaneous_circle_admitted=compatible)
  note='Conditional local radial-balance snapshot; all original circle defects retained.' if velocity is not None else 'READOUT_REFUSED: unique declared root or requested full-circle compatibility missing.'
  rows.append(dict(R_kpc=R,velocity_kms=velocity,interval_flags=flags,note=note));events.append(item)
 scope=dict(motion_scope=requested_motion_scope,declared_conditional_boundary=finite_closure['declared_conditional_boundary'],orientation=1,orientation_selected_using_Vobs=False,persistent_orbit_or_stability_admitted=False)
 report=REPORT.revised_43_observer_report(baseline_document,rows,baseline_row_path=DIRECT_TOTAL43_ROW_PATH,baseline_fields=DIRECT_TOTAL43_FIELDS,provenance=provenance,admission_status=dict(finite_closure=finite_closure,domain_admission=domain_admission,physical_metric_admitted=False),prediction_kind='local_metric_circular_snapshot',prediction_scope=scope)
 return dict(report=report,events=events,no_circle_or_metric_body_replayed=True,formatter_performed_admission=False,physical_or_observational_adoption=False)
