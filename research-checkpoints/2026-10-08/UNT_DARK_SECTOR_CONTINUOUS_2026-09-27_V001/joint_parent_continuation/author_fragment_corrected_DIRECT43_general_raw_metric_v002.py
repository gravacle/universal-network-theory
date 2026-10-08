"""HELD corrected DIRECT43 paired general ADM word producer; no imports or IO.
Globals np,P,H and exact selected DIRECT103/fce132/fy128 arithmetic. A future
containing owner authenticates a conditionally accepted finite trial first.
Geometric h_phi=0 is the source law; all genuine gauge time/phi words enter dg.
Raw reference words and compatibility gaps survive separately. No circle call,
interval-to-word conversion, catalogue fit or physical qualification occurs.
"""
CORRECTED_DIRECT43_AUTHOR_DRAFT=True
CORRECTED_DIRECT43_AUTHORING_IN_PROGRESS=False
CORRECTED_DIRECT43_PARENT_PINS={
 'coupled':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'finite':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'direct_baseline':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)}}
CORRECTED_DIRECT43_SOURCE_PINS={
 'author_fragment_direct_TOTAL43_finite_event_v001.py':'9458f530b2d15beb9138d806749a42ef1192df9215292a3b39280b63d7f50e59',
 'author_fragment_finite_conformal_circle_event_v001.py':'b607fcf3346d83e012771e75d9b658cef9ad51aeac4de09ad0a69bb3d75489b1',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'direct43_original_baseline_preparation_v003.py':'68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336',
 'author_fragment_direct43_owned_baseline_field_law_v004.py':'99ea2904f4b699764f0e186b9cb7d05db691bb5dc91a5019ee7199bb850ce7b1'}


def cdg_complete(role,payload,stage_complete,records):
 assert role not in records,'Each completed event stage requires a new sealed role'
 ref=stage_complete(role,payload)
 assert isinstance(ref,dict) and all(isinstance(ref.get(k),str) and ref[k] for k in ('file','sha256','commit_file','commit_sha256'))
 records[role]=ref;return ref


def corrected_DIRECT43_require(admission):
 assert not CORRECTED_DIRECT43_AUTHOR_DRAFT and not CORRECTED_DIRECT43_AUTHORING_IN_PROGRESS
 assert admission['source_pins']==CORRECTED_DIRECT43_SOURCE_PINS
 assert admission['scope'] in ('conditional_accepted_finite_trial','closed_measured_unqualified_changed_trial')
 for group,pins in CORRECTED_DIRECT43_PARENT_PINS.items():
  q=admission[group]
  for n,pin in pins.items():assert all(v is not None for v in pin) and tuple(q[n])==tuple(pin)
  assert q['naturally_closed'] is True and type(q['exit_code']) is int and q['exit_code']==0 and q['all_selected_seals_verified'] is True
  assert q['owner']['source_sha256']==pins['source'][1]
 if admission['scope']=='conditional_accepted_finite_trial':
  closure=admission['finite']['metric_admission']
  assert closure['finite_constraint_solution_admitted'] is closure['finite_domains_admitted'] is True and closure['finite_physical_metric_admitted'] is False
  for n in ('original_whole_correction_source_unsigned_authority_verified','fresh_nonlinear_canonical_phase_normal_CMC_and_stationarity_feedback_admitted','fixed_original_reference_denominators_verified'):assert closure[n] is True
  assert closure['provenance'] and closure['reference_provenance'] and closure['declared_conditional_boundary']
 else:
  assert 'metric_admission' not in admission['finite'],'A measured diagnostic cannot carry an accepted-finite certificate'
  closure=admission['finite']['changed_field_evidence']
  assert closure['measurement_only'] is closure['closed_measured_trial_words_verified'] is True
  for n in ('finite_constraint_solution_admitted','finite_domains_admitted','finite_physical_metric_admitted','scientific_acceptance_used','source_precision_admitted'):assert closure[n] is False
  assert closure['provenance'] and closure['reference_provenance'] and closure['declared_diagnostic_boundary']
 for n in ('original_mesh_and_basis_words_verified','point_TOTAL_addition_after_original_lift','baseline_event_TOTAL_hdot_matches_finite_BASELINE_before_correction','total_chi_matches_finite_TOTAL_nodes','metric_correction_matches_coupled_increment','selected_record_words_and_metadata_authenticated'):assert admission[n] is True
 for n in ('basis_record','total_chi_record','metric_correction_record','direct_baseline_reference_record','direct_baseline_event_record'):
  assert isinstance(admission[n],dict) and all(isinstance(admission[n].get(k),str) and admission[n][k] for k in ('file','sha256','commit_file','commit_sha256'))
 a,b=admission['baseline_reference_metadata'],admission['baseline_event_metadata']
 for md in (a,b):
  assert md['owner']==admission['direct_baseline']['owner'] and md['failed'] is md['physical_adoption'] is False
  assert len(md['qualification'])==9 and all(v is False for v in md['qualification'].values()) and md['Z']==0.
 assert type(a['index']) is type(b['index']) is int and 0<=a['index']<43 and a['index']==b['index'] and a['R']==b['R'] and np.isfinite(a['R']) and a['R']>0
 assert a['radial_side']==b['radial_side']=='left' and a['vertical_side']==b['vertical_side']=='upper'
 assert {k:b['reference_event'][k] for k in ('file','sha256','commit_file','commit_sha256')}==admission['direct_baseline_reference_record']
 assert a['stationary_seed_adopted_as_current'] is False
 assert b['original_point_first_order'] is True and b['node_sum_then_lift_equivalence_claimed'] is False
 assert b['Gauss_rate_interpolated'] is b['KADM_plus_Lie_inverse_used'] is False
 return closure


def corrected_DIRECT43_general_ADM_words(reference,rho,rho_gradient,h_dot,*,keep,label,stage_complete,records):
 assert not CORRECTED_DIRECT43_AUTHOR_DRAFT and not CORRECTED_DIRECT43_AUTHORING_IN_PROGRESS and callable(keep) and callable(stage_complete)
 for name,shape in (('h',(3,3)),('h_spatial_jets',(2,3,3)),('N',()),('beta',(3,)),('N_jets',(4,)),('beta_jets',(4,3)),('g',(4,4)),('dg',(4,4,4))):fce_pair(label+'_reference_'+name,reference[name],keep,shape)
 h0,hj0,N,beta,Na,ba=(reference[n] for n in ('h','h_spatial_jets','N','beta','N_jets','beta_jets'))
 assert all(np.array_equal(w,w.swapaxes(-1,-2)) for n in ('h','h_spatial_jets','g','dg') for w in reference[n])
 assert N[0]-abs(N[1])>0,'Positive held lapse required; genuine gauge phi jets are retained'
 fce_pair(label+'_new_total_rho',rho,keep,());fce_pair(label+'_new_total_rho_R_Z',rho_gradient,keep,(2,));fce_pair(label+'_new_total_physical_hdot',h_dot,keep,(3,3))
 assert all(np.array_equal(w,w.T) for w in h_dot)
 I0,det0=fy_physical_reference_inverse(h0,keep,label+'_physical_reference');mu0=fy_sqrt(det0,keep,label+'_physical_reference_volume')
 cdg_complete(label+'_REFERENCE_DOMAIN',dict(reference=reference,reference_inverse=I0,reference_det=det0,reference_volume=mu0),stage_complete,records)
 high=np.asarray(np.exp(4*rho[0]));keep(label+'_elementary_exp_high',high.copy())
 low=np.asarray(np.expm1(4*rho[1]));keep(label+'_elementary_expm1_low',low.copy())
 assert np.isfinite(high) and high>0 and np.isfinite(low)
 high_pair=fce_pair(label+'_exp_high_pair',P.a_dd(high),keep,())
 low_term=fce_pair(label+'_exp_low_product',P.a_prod(high,low),keep,())
 lam=fce_pair(label+'_conformal_lambda',P.a_add(high_pair,low_term),keep,());assert lam[0]-abs(lam[1])>0
 ilam=fy_div(P.a_dd(np.asarray(1.)),lam,keep,label+'_inverse_lambda')
 h=fce_pair(label+'_finite_h',fy_scale_matrix(lam,h0),keep,(3,3));I=fce_pair(label+'_finite_I',fy_scale_matrix(ilam,I0),keep,(3,3))
 root=fy_sqrt(lam,keep,label+'_lambda_root');lamroot=fce_pair(label+'_lambda_times_root',P.a_mul(lam,root),keep,())
 mu=fce_pair(label+'_finite_mu',P.a_mul(mu0,lamroot),keep,())
 cdg_complete(label+'_CONFORMAL',dict(rho=rho,rho_gradient=rho_gradient,exp_high=high,expm1_low=low,lambda_pair=lam,inverse_lambda=ilam,h=h,ih=I,mu=mu),stage_complete,records)
 spatial=[]
 for jet in range(2):
  factor=fce_pair(label+'_rho_gradient_factor%d'%jet,P.a_mul64(4.,P.a_slice(rho_gradient,jet)),keep,())
  addition=fce_pair(label+'_rho_gradient_term%d'%jet,fy_scale_matrix(factor,h0),keep,(3,3))
  joined=fce_pair(label+'_spatial_reference_plus_conformal_term%d'%jet,P.a_add(P.a_slice(hj0,jet),addition),keep,(3,3))
  spatial.append(fce_pair(label+'_finite_spatial_h_jet%d'%jet,fy_scale_matrix(lam,joined),keep,(3,3)))
 ha=fce_pair(label+'_complete_h_first',P.a_stack([h_dot]+spatial+[P.a_dd(np.zeros((3,3)))],0),keep,(4,3,3))
 hb=fce_pair(label+'_h_beta',fy_mv(h,beta),keep,(3,));N2=fce_pair(label+'_held_lapse_squared',P.a_mul(N,N),keep,())
 beta_h_beta=fce_pair(label+'_beta_dot_h_beta',fy_sum(P.a_mul(beta,hb),0),keep,())
 g00=fce_pair(label+'_ADM_g00',P.a_sub(beta_h_beta,N2),keep,())
 g=fce_block(g00,hb,h,keep,label+'_finite_ADM_g');rows=[]
 cdg_complete(label+'_METRIC',dict(g=g,h_first=ha,h_beta=hb,lapse_squared=N2,gauge_N_jets=Na,gauge_beta_jets=ba,geometric_h_phi_zero=True),stage_complete,records)
 for a in range(4):
  H=P.a_slice(ha,a);b=P.a_slice(ba,a);n=P.a_slice(Na,a)
  left=fce_pair(label+'_h_jet_beta%d'%a,fy_mv(H,beta),keep,(3,));right=fce_pair(label+'_h_beta_jet%d'%a,fy_mv(h,b),keep,(3,))
  hba=fce_pair(label+'_current_h_beta_jet%d'%a,P.a_add(left,right),keep,(3,))
  first=fce_pair(label+'_beta_jet_dot_h_beta%d'%a,fy_sum(P.a_mul(b,hb),0),keep,());second=fce_pair(label+'_beta_dot_h_beta_jet%d'%a,fy_sum(P.a_mul(beta,hba),0),keep,())
  Nn=fce_pair(label+'_N_times_genuine_N_jet%d'%a,P.a_mul(N,n),keep,())
  lapse=fce_pair(label+'_fixed_lapse_jet_term%d'%a,P.a_mul64(2.,Nn),keep,())
  joined=fce_pair(label+'_ADM_g00_two_shift_terms%d'%a,P.a_add(first,second),keep,())
  zerozero=fce_pair(label+'_ADM_g00_jet%d'%a,P.a_sub(joined,lapse),keep,())
  rows.append(fce_block(zerozero,hba,H,keep,label+'_finite_ADM_dg%d'%a))
  cdg_complete(label+'_FIRST_JET%d'%a,dict(derivative_index=a,dg=rows[-1],gauge_N_jet=n,gauge_beta_jet=b,h_jet=H),stage_complete,records)
 dg=fce_pair(label+'_finite_ADM_complete_dg',P.a_stack(rows,0),keep,(4,4,4))
 cdg_complete(label+'_RAW_PAIR',dict(g=g,dg=dg,raw_reference_g=reference['g'],raw_reference_dg=reference['dg']),stage_complete,records)
 invN2=fy_div(P.a_dd(np.asarray(1.)),N2,keep,label+'_inverse_lapse_squared')
 bb=fce_pair(label+'_beta_outer_beta',P.a_mul(tuple(w[:,None] for w in beta),tuple(w[None,:] for w in beta)),keep,(3,3))
 i00=fce_pair(label+'_ADM_inverse_00',P.a_mul64(-1.,invN2),keep,());i0i=fce_pair(label+'_ADM_inverse_0i',P.a_mul(beta,invN2),keep,(3,))
 ibb=fce_pair(label+'_inverse_lapse_times_beta_outer',fy_scale_matrix(invN2,bb),keep,(3,3))
 iij=fce_pair(label+'_ADM_inverse_ij',P.a_sub(I,ibb),keep,(3,3));hi=fce_block(i00,i0i,iij,keep,label+'_finite_ADM_inverse')
 gaps={}
 for name,x,y,shape in (('ADM_minus_raw_reference_metric',g,reference['g'],(4,4)),('ADM_minus_raw_reference_first_jets',dg,reference['dg'],(4,4,4))):gaps[name]=fce_pair(label+'_'+name,P.a_sub(x,y),keep,shape)
 cdg_complete(label+'_REFERENCE_GAPS',dict(source_association_gaps=gaps,raw_reference=reference,completed_g=g,completed_dg=dg),stage_complete,records)
 residuals={}
 for name,A,B,size in (('spatial_inverse',h,I,3),('spacetime_inverse',g,hi,4)):
  product=fce_pair(label+'_'+name+'_product',fy_mm(A,B),keep,(size,size))
  residuals[name]=fce_pair(label+'_'+name,P.a_sub(product,P.a_dd(np.eye(size))),keep,(size,size))
 cdg_complete(label+'_INVERSE_DIAGNOSTICS',dict(ih=I,spacetime_inverse=hi,inverse_residuals=residuals),stage_complete,records)
 return dict(g=g,dg=dg,h=h,ih=I,mu=mu,h_first=ha,fixed_N=N,fixed_beta=beta,fixed_gauge_N_jets=Na,fixed_gauge_beta_jets=ba,raw_reference=reference,source_association_gaps=gaps,inverse_residuals=residuals,geometric_h_phi_zero=True,axisymmetric_gauge_phi_exact_zero=bool(all(np.all(w[3]==0) for pair in (Na,ba) for w in pair)),raw_reference_phi_words_projected=False,elementary_exp_accuracy_admitted=False,geometry_readout_precision_admitted=False)


def corrected_DIRECT43_general_raw_event(reference,baseline_h_dot,r,z,total_chi,metric_correction,*,R,radial_side,admission,keep,label,stage_complete):
 closure=corrected_DIRECT43_require(admission);assert callable(keep) and callable(stage_complete)
 assert reference['same_reference_as_finite_candidate']==closure['reference_provenance'] and reference['direct_event_data_not_Gauss_interpolation'] is True
 assert reference['provenance']==admission['baseline_reference_metadata']['reference_event_provenance']
 assert reference['R']==R==admission['baseline_reference_metadata']['R'] and reference['Z']==0 and reference['radial_side']==radial_side=='left'
 assert admission['coordinate_event']==[0.,R,0.,0.] and admission['event_provenance']
 assert admission['geometric_h_phi_zero_source_law_verified'] is True
 refs={};fce_pair(label+'_DIRECT_baseline_TOTAL_hdot',baseline_h_dot,keep,(3,3));assert all(np.array_equal(w,w.T) for w in baseline_h_dot)
 cdg_complete(label+'_INPUT',dict(reference=reference,baseline_TOTAL_hdot=baseline_h_dot,admission=admission),stage_complete,refs)
 sampled=direct_TOTAL43_sample_correction(r,z,total_chi,metric_correction,R=R,radial_side=radial_side,keep=keep,label=label+'_original_Q1')
 fce_pair(label+'_sampled_rho_gradient',sampled['rho_gradient'],keep,(2,))
 cdg_complete(label+'_SAMPLING',dict(sampling=sampled,basis_record=admission['basis_record'],total_chi_record=admission['total_chi_record'],metric_correction_record=admission['metric_correction_record']),stage_complete,refs)
 ht=fce_pair(label+'_NEW_event_TOTAL_hdot',P.a_add(baseline_h_dot,sampled['delta_h_dot']),keep,(3,3))
 cdg_complete(label+'_TOTAL_RATE',dict(event_TOTAL_hdot=ht,baseline_TOTAL_hdot=baseline_h_dot,correction=sampled['delta_h_dot'],baseline_record=admission['direct_baseline_event_record']),stage_complete,refs)
 geometry=corrected_DIRECT43_general_ADM_words(reference,sampled['rho'],sampled['rho_gradient'],ht,keep=keep,label=label+'_general_ADM',stage_complete=stage_complete,records=refs)
 assert type(admission['baseline_reference_metadata']['axisymmetric_gauge_phi_exact_zero']) is bool and geometry['axisymmetric_gauge_phi_exact_zero']==admission['baseline_reference_metadata']['axisymmetric_gauge_phi_exact_zero']
 out=dict(g=geometry['g'],dg=geometry['dg'],geometry=geometry,sampling=sampled,reference=reference,baseline_TOTAL_hdot=baseline_h_dot,event_TOTAL_hdot=ht,closure=closure,provenance=admission['event_provenance'],source_stage_refs=refs.copy(),coordinate_system='native313_cp_model_equals_one',derivative_index_first=True,coordinate=[0.,R,0.,0.],index=admission['baseline_reference_metadata']['index'],radial_side=radial_side,vertical_side='upper',scope=admission['scope'],finite_constraint_solution_admitted=closure['finite_constraint_solution_admitted'],finite_domains_admitted=closure['finite_domains_admitted'],physical_metric_admitted=False,point_TOTAL_addition_after_original_lift=True,nodal_TOTAL_equivalence_earned=False,Gauss_metric_or_jets_interpolated=False,all_genuine_gauge_time_phi_words_retained=True,W_t_direct_geometry_zero=True,source_uncertainty_admitted=False,installed_exp_accuracy_admitted=False,paired_word_collapse_admitted=False,binary64_readout_admitted=False,original132_exact_zero_gate_admitted=False,full_circle_admitted=False,circle_or_velocity_adopted=False)
 cdg_complete(label+'_OUTPUT',out,stage_complete,refs);out['source_stage_refs']=refs;return out
