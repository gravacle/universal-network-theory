"""HELD direct finite chi/total-hdot event adapter; no imports, IO or runner.
Globals np,P,H and exact selected fy128 inverse/volume/matrix arithmetic.
The consumer authenticates a completed conditional finite candidate first.
Reference h/jets and fixed N/beta/gauge jets are DIRECT event data, not Gauss
interpolation. W/t affect the target/rate response, never this held gauge.
"""
FINITE_CIRCLE_EVENT_AUTHOR_DRAFT=True
FINITE_CIRCLE_EVENT_AUTHORING_IN_PROGRESS=False
FINITE_CIRCLE_EVENT_SOURCE=(None,None)
FINITE_CIRCLE_EVENT_RESULT=(None,None,None)
FINITE_CIRCLE_EVENT_RECEIPT=(None,None,None)
FINITE_CIRCLE_EVENT_PROOF=(None,None,None)

def fce_pair(label,x,keep,shape):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
 keep(label+'_both_words',np.stack(x).copy())
 for n,a in zip(('hi','lo'),x):
  keep(label+'_'+n,np.asarray(a).copy());assert a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)),label
 return x

def fce_block(g00,g0i,h,keep,label):
 rows=[P.a_stack([g00]+[P.a_slice(g0i,i) for i in range(3)],0)]
 for i in range(3):rows.append(P.a_stack([P.a_slice(g0i,i)]+[P.a_slice(h,(i,j)) for j in range(3)],0))
 return fce_pair(label,P.a_stack(rows,0),keep,(4,4))

def fce_Q1_chi_and_total_metric_rate(r,z,chi,metric,R,radial_side,keep,label):
 fce_pair(label+'_total_chi_nodes',chi,keep,(87,45));fce_pair(label+'_solved_TOTAL_metric_rate_nodes',metric,keep,(6,87,45))
 mask=P.scalar_mask().copy();mask[-1]=False;mask[:,-1]=False
 assert np.count_nonzero(mask)==3740 and all(np.all(w[~mask]==0) for w in chi)
 assert all(np.all(w[~P.metric_mask()]==0) for w in metric),'Original metric independent coordinates required'
 for n,a,shape in (('R',r,(87,)),('Z',z,(45,))):
  keep(label+'_registered_mesh_'+n,np.asarray(a).copy());assert a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(np.diff(a)>0)
 assert r[0]==z[0]==0 and z[1]>0
 contact=H.q1_radial_readout_contact(r,R,catalogue_R_kpc=R,mapping=dict(kind='coordinate_R_equals_catalogue_kpc'),side=radial_side)
 i=contact['selected_cell'];w=contact['value_weights'];d=contact['radial_derivative_weights'];dz=z[1]-z[0]
 weights=np.array(((w[0],w[1],0.,0.),(d[0],d[1],0.,0.),(-w[0]/dz,-w[1]/dz,w[0]/dz,w[1]/dz)))
 keep(label+'_positive_sheet_value_R_Z_weights',weights.copy());corners=((i,0),(i+1,0),(i,1),(i+1,1))
 scalar=tuple(P.scalar_lift(a) for a in chi);lifted=tuple(P.lift_metric(a) for a in metric)
 fce_pair(label+'_axis_extended_total_chi',scalar,keep,(87,45));fce_pair(label+'_axis_sheet_extended_total_metric_rate',lifted,keep,(6,87,45))
 rho=[P.a_dd(np.asarray(0.)) for unused in range(3)];six=P.a_dd(np.zeros(6));F=P.dd_metric_F(np.asarray(R));keep(label+'_original_event_F',F.copy())
 for corner,(ci,cj) in enumerate(corners):
  a=fce_pair(label+'_chi_corner%d'%corner,tuple(v[ci,cj].copy() for v in scalar),keep,())
  for jet in range(3):
   product=fce_pair(label+'_chi_corner%d_jet%d_product'%(corner,jet),P.a_mul64(weights[jet,corner],a),keep,())
   rho[jet]=fce_pair(label+'_chi_jet%d_partial'%jet,P.a_add(rho[jet],product),keep,())
  a=fce_pair(label+'_TOTAL_metric_corner%d'%corner,tuple(v[:,ci,cj].copy() for v in lifted),keep,(6,));Fhat=weights[0,corner]*F
  keep(label+'_original_rounded_event_Fhat_corner%d'%corner,Fhat.copy())
  product=fce_pair(label+'_physical_time_corner%d'%corner,P.a_matvec(Fhat,a),keep,(6,));six=fce_pair(label+'_physical_time_partial',P.a_add(six,product),keep,(6,))
 ht=P.a_dd(np.zeros((3,3)))
 for slot,(a,b) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for word in (0,1):ht[word][a,b]=ht[word][b,a]=six[word][slot]
 return dict(rho=rho[0],rho_gradient=P.a_stack(rho[1:],0),h_dot=fce_pair(label+'_genuine_TOTAL_hdot',ht,keep,(3,3)),radius_contact=contact,corners=corners,all_six_physical_time_components_present=True)

def fce_conformal_ADM_event(reference,rho,rho_gradient,h_dot,keep,label):
 for name,shape in (('h',(3,3)),('h_spatial_jets',(2,3,3)),('N',()),('beta',(3,)),('N_jets',(4,)),('beta_jets',(4,3)),('g',(4,4)),('dg',(4,4,4))):fce_pair(label+'_reference_'+name,reference[name],keep,shape)
 h0,hj0,N,beta,Na,ba=(reference[n] for n in ('h','h_spatial_jets','N','beta','N_jets','beta_jets'))
 assert all(np.array_equal(w,w.swapaxes(-1,-2)) for n in ('h','h_spatial_jets','g','dg') for w in reference[n])
 assert N[0]-abs(N[1])>0 and all(np.all(w[3]==0) for pair in (Na,ba) for w in pair),'Positive held lapse and axisymmetric gauge jets required'
 fce_pair(label+'_new_total_rho',rho,keep,());fce_pair(label+'_new_total_rho_R_Z',rho_gradient,keep,(2,));fce_pair(label+'_new_total_physical_hdot',h_dot,keep,(3,3))
 assert all(np.array_equal(w,w.T) for w in h_dot)
 I0,det0=fy_physical_reference_inverse(h0,keep,label+'_physical_reference');mu0=fy_sqrt(det0,keep,label+'_physical_reference_volume')
 high=np.asarray(np.exp(4*rho[0]));low=np.asarray(np.expm1(4*rho[1]));keep(label+'_elementary_exp_high',high.copy());keep(label+'_elementary_expm1_low',low.copy())
 assert np.isfinite(high) and high>0 and np.isfinite(low)
 lam=fce_pair(label+'_conformal_lambda',P.a_add(P.a_dd(high),P.a_prod(high,low)),keep,());assert lam[0]-abs(lam[1])>0
 ilam=fy_div(P.a_dd(np.asarray(1.)),lam,keep,label+'_inverse_lambda');h=fce_pair(label+'_finite_h',fy_scale_matrix(lam,h0),keep,(3,3));I=fce_pair(label+'_finite_I',fy_scale_matrix(ilam,I0),keep,(3,3))
 mu=fce_pair(label+'_finite_mu',P.a_mul(mu0,P.a_mul(lam,fy_sqrt(lam,keep,label+'_lambda_root'))),keep,())
 spatial=[]
 for jet in range(2):
  addition=fce_pair(label+'_rho_gradient_term%d'%jet,fy_scale_matrix(P.a_mul64(4.,P.a_slice(rho_gradient,jet)),h0),keep,(3,3))
  spatial.append(fce_pair(label+'_finite_spatial_h_jet%d'%jet,fy_scale_matrix(lam,P.a_add(P.a_slice(hj0,jet),addition)),keep,(3,3)))
 ha=P.a_stack([h_dot]+spatial+[P.a_dd(np.zeros((3,3)))],0);fce_pair(label+'_complete_h_first',ha,keep,(4,3,3))
 hb=fce_pair(label+'_h_beta',fy_mv(h,beta),keep,(3,));N2=fce_pair(label+'_held_lapse_squared',P.a_mul(N,N),keep,())
 g=fce_block(P.a_sub(fy_sum(P.a_mul(beta,hb),0),N2),hb,h,keep,label+'_finite_ADM_g');rows=[]
 for a in range(4):
  H=P.a_slice(ha,a);b=P.a_slice(ba,a);n=P.a_slice(Na,a)
  hba=fce_pair(label+'_current_h_beta_jet%d'%a,P.a_add(fy_mv(H,beta),fy_mv(h,b)),keep,(3,))
  first=fce_pair(label+'_beta_jet_dot_h_beta%d'%a,fy_sum(P.a_mul(b,hb),0),keep,());second=fce_pair(label+'_beta_dot_h_beta_jet%d'%a,fy_sum(P.a_mul(beta,hba),0),keep,())
  lapse=fce_pair(label+'_fixed_lapse_jet_term%d'%a,P.a_mul64(2.,P.a_mul(N,n)),keep,())
  rows.append(fce_block(P.a_sub(P.a_add(first,second),lapse),hba,H,keep,label+'_finite_ADM_dg%d'%a))
 dg=fce_pair(label+'_finite_ADM_complete_dg',P.a_stack(rows,0),keep,(4,4,4))
 invN2=fy_div(P.a_dd(np.asarray(1.)),N2,keep,label+'_inverse_lapse_squared');bb=P.a_mul(tuple(w[:,None] for w in beta),tuple(w[None,:] for w in beta))
 hi=fce_block(P.a_mul64(-1.,invN2),P.a_mul(beta,invN2),P.a_sub(I,fy_scale_matrix(invN2,bb)),keep,label+'_finite_ADM_inverse')
 differences=dict(reference_metric=P.a_sub(g,reference['g']),reference_first_jets=P.a_sub(dg,reference['dg']))
 residuals=dict(spatial_inverse=P.a_sub(fy_mm(h,I),P.a_dd(np.eye(3))),spacetime_inverse=P.a_sub(fy_mm(g,hi),P.a_dd(np.eye(4))))
 for n,pair in {**differences,**residuals}.items():fce_pair(label+'_retained_'+n+'_difference',pair,keep,pair[0].shape)
 return dict(g=g,dg=dg,h=h,ih=I,mu=mu,h_first=ha,fixed_N=N,fixed_beta=beta,fixed_gauge_N_jets=Na,fixed_gauge_beta_jets=ba,reference_differences=differences,inverse_residuals=residuals,elementary_exp_accuracy_admitted=False,geometry_readout_precision_admitted=False)

def finite_conformal_circle_event(reference,r,z,chi_nodes,total_metric_nodes,*,R,radial_side,closure,keep,label):
 assert not FINITE_CIRCLE_EVENT_AUTHOR_DRAFT and not FINITE_CIRCLE_EVENT_AUTHORING_IN_PROGRESS
 for name,ref in (('source',FINITE_CIRCLE_EVENT_SOURCE),('result',FINITE_CIRCLE_EVENT_RESULT),('receipt',FINITE_CIRCLE_EVENT_RECEIPT),('proof',FINITE_CIRCLE_EVENT_PROOF)):
  assert all(x is not None for x in ref) and tuple(closure[name])==ref,'Authentic accepted conditional finite candidate required'
 assert closure['naturally_closed'] is True and closure['exit_code']==0 and closure['all_selected_seals_verified'] is True
 assert closure['finite_constraint_solution_admitted'] is True and closure['finite_physical_metric_admitted'] is False and closure['finite_domains_admitted'] is True
 assert closure['provenance'] and closure['declared_conditional_boundary'] and reference['provenance'] and reference['R']==R and reference['Z']==0 and reference['radial_side']==radial_side
 assert reference['same_reference_as_finite_candidate']==closure['reference_provenance'] and reference['direct_event_data_not_Gauss_interpolation'] is True
 sampled=fce_Q1_chi_and_total_metric_rate(r,z,chi_nodes,total_metric_nodes,R,radial_side,keep,label+'_direct_Q1')
 geometry=fce_conformal_ADM_event(reference,sampled['rho'],sampled['rho_gradient'],sampled['h_dot'],keep,label+'_NEW_finite')
 parity=np.array((1.,1.,-1.,1.));lower_g=tuple(w*parity[:,None]*parity[None,:] for w in geometry['g']);lower_dg=tuple(w*parity[:,None,None]*parity[None,:,None]*parity[None,None,:] for w in geometry['dg'])
 fce_pair(label+'_reflected_lower_g',lower_g,keep,(4,4));fce_pair(label+'_reflected_lower_dg',lower_dg,keep,(4,4,4))
 same=all(np.array_equal(a,b) for a,b in zip(geometry['g'],lower_g));keep(label+'_reflection_metric_on_sheet_match',np.asarray(same,dtype=np.int64))
 return dict(upper=dict(g=geometry['g'],dg=geometry['dg']),lower=dict(g=lower_g,dg=lower_dg),geometry=geometry,sampling=sampled,closure=closure,
             coordinate_event=(0.,R,0.,0.),radial_side=radial_side,reference_provenance=reference['provenance'],sheet_reflection_metric_match=same,
             configuration_changed=True,total_chi_and_total_hdot_supplied=True,lapse_shift_and_gauge_jets_held=True,W_t_direct_geometry_zero=True,
             Gauss_metric_or_jets_interpolated=False,canonical_normal_CMC_acceptance_performed_here=False,physical_metric_admitted=False)

def finite_conformal_event_circle_readout(event,*,orientation,readout_precision_admission,sheet_junction_convention,keep,label,side_complete,circle_gate=None):
 assert type(orientation) is int and orientation in (-1,1) and isinstance(sheet_junction_convention,dict) and sheet_junction_convention
 assert readout_precision_admission.get('paired_word_collapse_admitted') is True and readout_precision_admission.get('binary64_readout_admitted') is True and readout_precision_admission.get('provenance')
 assert readout_precision_admission['finite_event_provenance']==dict(closure=event['closure']['provenance'],reference=event['reference_provenance'],coordinate_event=list(event['coordinate_event']),radial_side=event['radial_side'])
 assert callable(side_complete) and (circle_gate is None or callable(circle_gate))
 sides=dict(upper=event['upper'],lower=event['lower']);results={};completed=[]
 if sheet_junction_convention.get('kind')=='registered_reflected_mean_connection':
  assert sheet_junction_convention.get('action_junction_admitted') is True and sheet_junction_convention.get('provenance') and event['sheet_reflection_metric_match']
  mean=fce_pair(label+'_declared_reflected_mean_dg',P.a_mul64(.5,P.a_add(event['upper']['dg'],event['lower']['dg'])),keep,(4,4,4));sides['registered_junction']=dict(g=event['upper']['g'],dg=mean)
 for side,data in sides.items():
  assert side in readout_precision_admission['admitted_sides'],'Conditioning admission must cover this supplied side/junction'
  raw={};defects={}
  for n,shape in (('g',(4,4)),('dg',(4,4,4))):
   fce_pair(label+'_'+side+'_supplied_'+n,data[n],keep,shape);value,error=P.a_sum(data[n][0],data[n][1])
   keep(label+'_'+side+'_'+n+'_binary64',np.asarray(value).copy());keep(label+'_'+side+'_'+n+'_collapse_defect',np.asarray(error).copy());assert np.all(np.isfinite(value)) and np.all(np.isfinite(error))
   raw[n]=value;defects[n]=error
  result=H.supplied_model_local_circle_event(raw['g'],raw['dg'],radius_contact=event['sampling']['radius_contact'],orientation=orientation,input_scope='conditional_finite_metric',metric_admission=event['closure'],readout_precision_admission=readout_precision_admission)
  results[side]=dict(readout=result,conversion_defects=defects)
  ref=side_complete(side,results[side]);assert isinstance(ref,dict) and all(ref.get(n) for n in ('file','sha256','commit_file','commit_sha256'));completed.append(ref);gate=None
  if circle_gate is not None:
   registration=dict(coordinate_event=event['coordinate_event'],radial_side=event['radial_side'],sheet_side=side,sheet_junction_convention=sheet_junction_convention,declared_orientation=orientation)
   gate=circle_gate(result,registration);assert isinstance(gate,dict) and type(gate['admitted']) is bool and gate.get('provenance')
  results[side]['supplied_circle_gate']=gate
 return dict(sides=results,completed_side_refs=completed,declared_sheet_junction=dict(sheet_junction_convention),prediction_kind='local_metric_circular_snapshot',
             all_radial_vertical_clock_axial_geodesic_and_root_diagnostics_retained=True,orientation_chosen_using_observations=False,
             supplied_precision_admission=readout_precision_admission,finite_constraint_solution_admitted=event['closure']['finite_constraint_solution_admitted'],
             full_circle_admission_performed_by_adapter=False,stationarity_stability_evolution_or_observational_qualification=False,physical_metric_admitted=False)
