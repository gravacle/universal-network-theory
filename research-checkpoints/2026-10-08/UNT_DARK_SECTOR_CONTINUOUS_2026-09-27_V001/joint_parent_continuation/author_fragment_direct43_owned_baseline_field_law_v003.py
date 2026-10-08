"""HELD DIRECT evaluation of the ORIGINAL owned reference and TOTAL rate law.
Globals np,P,H,W,Q,D43,keep; W.metric and Q connection/metric-basis/metric-partial
are unchanged selected source definitions. No IO, producer, inverse or runner.
The seed connection is an operand of the prescribed owned-K gauge law, never
adopted as the current stationary metric. No Gauss field interpolation occurs.
"""
DIRECT43_BASELINE_AUTHOR_DRAFT=True
DIRECT43_BASELINE_AUTHORING_IN_PROGRESS=False
DIRECT43_BASELINE_PARENT_PINS={
 'reference_fields':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'nodal_current':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'admitted_rate_correction':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'point_TOTAL_baseline':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)}}
DIRECT43_BASELINE_SOURCE_PINS={
 'cross_u_whole_slice_cauchy_data_v002.py':'6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7',
 'cross_u_whole_slice_q1_adm_residual_v001.py':'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a',
 'cross_u_weak_canonical_spatial_euler_loads_v003.py':'4f239074b5345709f493b3633f7dd376fa7ac97dbb23bf20825eabde2ed56b79',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'saved_prefix_hybrid_mechanical_continuation_v007.py':'d2ef156021ae94c25e523a3e5e3329d3c9687ff8a8df74df7c10ac30a40dd076',
 'cross_u_finite0_candidate_action_residual_v007.py':'ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58',
 'author_fragment_fixed_geometry_total_rate_state_v002.py':'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d',
 'author_fragment_point_TOTAL_trial_fields_v001.py':'96925b148cb7c1b3660e76867e5c499e9b10868bc737209b194d9c667adc46ef',
 'author_fragment_direct_TOTAL43_finite_event_v001.py':'9458f530b2d15beb9138d806749a42ef1192df9215292a3b39280b63d7f50e59'}

def direct43_baseline_require(admission):
 assert not DIRECT43_BASELINE_AUTHOR_DRAFT and not DIRECT43_BASELINE_AUTHORING_IN_PROGRESS
 assert admission['source_pins']==DIRECT43_BASELINE_SOURCE_PINS
 for group,pins in DIRECT43_BASELINE_PARENT_PINS.items():
  q=admission[group]
  for n,pin in pins.items():assert all(v is not None for v in pin) and tuple(q[n])==tuple(pin)
  assert q['naturally_closed'] is True and q['exit_code']==0 and q['all_selected_seals_verified'] is True
 for n in ('reference_nodes_and_sigma1_shift_owned_by_original24903','current47969_solution_and_RATE_JETS_same_coefficients','correction60363_is_original139_point_increment','same_original_mesh_basis_and_fixed_materials','point_TOTAL_baseline_law_matches_original139_ancestry'):
  assert admission[n] is True
 assert admission['point_TOTAL_baseline']['inherited_scientific_owner_preserved'] is True
 assert admission['owned_K_Hbar_uses_original_q1_operation_order'] is True
 for n in ('reference_fields_record','current_metric_nodes_record','rate_correction_record','basis_record'):
  assert all(isinstance(admission[n].get(k),str) and admission[n][k] for k in ('file','sha256','commit_file','commit_sha256'))
 assert admission['fixed']['B']>0 and all(np.isfinite(admission['fixed'][n]) for n in ('B','Hbar','finite_normal_Hbar'))

def direct43_original_owned_reference(r,z,potential_nodes,shift_nodes,*,R,radial_side,admission,keep,label):
 direct43_baseline_require(admission)
 assert r.shape==(87,) and z.shape==(45,) and r.dtype==z.dtype==np.float64 and r[0]==z[0]==0 and z[1]>0
 assert np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
 for n,a in (('R_mesh',r),('Z_mesh',z),('original_potential_nodes',potential_nodes),('original_sigma1_shift_nodes',shift_nodes)):
  keep(label+'_'+n,a.copy());assert a.dtype==np.float64 and np.all(np.isfinite(a))
 assert potential_nodes.shape==shift_nodes.shape==(87,45)
 contact=H.q1_radial_readout_contact(r,R,catalogue_R_kpc=R,mapping=dict(kind='coordinate_R_equals_catalogue_kpc'),side=radial_side)
 i=contact['selected_cell'];v=contact['value_weights'];d=contact['radial_derivative_weights'];dz=z[1]-z[0]
 weights=np.asarray(((v[0],v[1],0.,0.),(d[0],d[1],0.,0.),(-v[0]/dz,-v[1]/dz,v[0]/dz,v[1]/dz)))
 keep(label+'_original_positive_sheet_weights',weights.copy());corners=((i,0),(i+1,0),(i,1),(i+1,1));sums=np.zeros((2,3,1))
 for corner,(ci,cj) in enumerate(corners):
  for field,nodes in enumerate((potential_nodes,shift_nodes)):
   for jet in range(3):
    product=weights[jet,corner]*nodes[ci,cj];keep(label+'_source_scalar_product_%d_%d_%d'%(corner,field,jet),np.asarray(product))
    sums[field,jet]+=product;keep(label+'_source_scalar_partial',sums.copy())
 B=admission['fixed']['B'];Hbar=admission['fixed']['Hbar'];keep(label+'_owned_K_Hbar',np.asarray(Hbar));keep(label+'_finite_normal_Hbar',np.asarray(admission['fixed']['finite_normal_Hbar']));keep(label+'_Hbar_source_association_gap',np.asarray(Hbar-admission['fixed']['finite_normal_Hbar']));Phi=B*sums[0,0];gr=np.zeros((1,4));gr[:,1:3]=B*sums[0,1:].T
 beta_scalar=sums[1,0];br=np.zeros((1,4));br[:,1:3]=sums[1,1:].T
 for n,a in (('source_Phi',Phi),('source_Phi_spatial',gr),('source_shift',beta_scalar),('source_shift_spatial',br)):keep(label+'_'+n,a.copy())
 g,hi,seed_dg,seed_Ga,unused_n,unused_rho=W.metric(np.asarray([R]),Phi,gr,beta_scalar,br)
 for n,a in (('source_g',g),('source_hi',hi),('seed_dg_operand',seed_dg),('seed_Gamma_operand',seed_Ga)):keep(label+'_'+n,a.copy())
 h=g[:,1:,1:];N=1/np.sqrt(-hi[:,0,0]);beta=N[:,None]**2*hi[:,0,1:]
 for n,a in (('source_h',h),('source_N',N),('source_beta',beta)):keep(label+'_'+n,a.copy())
 e=Q.metric_basis();embed=np.zeros((1,6,4,4));embed[:,:,1:,1:]=e[None,:,:,:]
 embed[:,:,0,1:]=np.einsum('kij,pj->pki',e,beta);embed[:,:,1:,0]=embed[:,:,0,1:]
 embed[:,:,0,0]=np.einsum('pi,kij,pj->pk',beta,e,beta)
 kten=2*N[:,None,None]*Hbar*h
 k=np.column_stack((kten[:,0,0],kten[:,1,1],kten[:,2,2],kten[:,0,1],kten[:,0,2],kten[:,1,2]))
 increment_dg=np.zeros((1,4,4,4));increment_dg[:,0]=np.einsum('pk,pkab->pab',k,embed)
 for n,a in (('source_embed',embed),('owned_prescribed_hdot',kten),('owned_hdot_six',k),('owned_increment_dg',increment_dg)):keep(label+'_'+n,a.copy())
 increment_Ga=Q.connection_from_jet(hi,increment_dg);keep(label+'_owned_Gamma_increment',increment_Ga.copy());Ga=seed_Ga+increment_Ga;keep(label+'_owned_Gamma',Ga.copy())
 dg=Q.metric_partial(dict(g=g,Ga=Ga));dhi=-np.einsum('pij,pajk,pkl->pail',hi,dg,hi)
 dN=N[:,None]**3*dhi[:,:,0,0]/2
 db=2*N[:,None,None]*dN[:,:,None]*hi[:,None,0,1:]+N[:,None,None]**2*dhi[:,:,0,1:]
 for n,a in (('chart_dg',dg),('chart_dhi',dhi),('genuine_N_jets',dN),('genuine_beta_jets',db)):
  keep(label+'_'+n,a.copy());assert np.all(np.isfinite(a))
 keep(label+'_owned_chart_minus_literal_seed_dg',dg-seed_dg);keep(label+'_owned_chart_minus_prescribed_time_dg',dg[:,0]-increment_dg[:,0])
 values=dict(h=h[0],h_spatial_jets=dg[0,1:3,1:,1:],N=N[0],beta=beta[0],N_jets=dN[0],beta_jets=db[0],g=g[0],dg=dg[0])
 reference={}
 for n,a in values.items():
  q=P.a_dd(np.asarray(a).copy());reference[n]=q;keep(label+'_reference_'+n+'_both_words',np.stack(q).copy())
 reference.update(R=R,Z=0.,radial_side=radial_side,provenance=admission['reference_event_provenance'],same_reference_as_finite_candidate=admission['finite_reference_provenance'],direct_event_data_not_Gauss_interpolation=True)
 return dict(reference=reference,radius_contact=contact,source_chart_first=dict(dg=dg,dhi=dhi,N_jets=dN,beta_jets=db),seed_and_owned_connection=dict(seed=seed_Ga,increment=increment_Ga,owned=Ga),stationary_seed_adopted_as_current=False,Gauss_rate_or_gauge_interpolated=False,KADM_plus_Lie_inverse_used=False,physical_adoption=False)

def direct43_baseline_TOTAL_rate(r,z,current47969_nodes,correction60363_metric_nodes,*,R,radial_side,admission,keep,label):
 direct43_baseline_require(admission);zero=P.a_dd(np.zeros((87,45)))
 original=D43.direct_TOTAL43_sample_correction(r,z,zero,current47969_nodes,R=R,radial_side=radial_side,keep=keep,label=label+'_original47969')
 keep(label+'_completed_original47969_physical_hdot_both_words',np.stack(original['delta_h_dot']).copy())
 increment=D43.direct_TOTAL43_sample_correction(r,z,zero,correction60363_metric_nodes,R=R,radial_side=radial_side,keep=keep,label=label+'_original60363_increment')
 hdot=P.a_add(original['delta_h_dot'],increment['delta_h_dot']);keep(label+'_DIRECT_baseline_TOTAL_hdot_both_words',np.stack(hdot).copy())
 return dict(h_dot=hdot,original_current_hdot=original['delta_h_dot'],original_admitted_increment=increment['delta_h_dot'],radius_contact=original['radius_contact'],original_point_first_order=True,node_sum_then_lift_equivalence_claimed=False,source_records={n:admission[n] for n in ('current_metric_nodes_record','rate_correction_record','basis_record')},Gauss_rate_interpolated=False,KADM_plus_Lie_inverse_used=False,physical_adoption=False)
