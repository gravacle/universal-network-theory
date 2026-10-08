"""HELD metric-only current-configuration/nonconverged-response event sampler.
Globals np,math,P (paired arithmetic) and H (reviewed Q1 radial contact).
No input loading, EOS/native action, Gauss tensor interpolation or invocation.
The fixed analytic lapse/shift time policy is authenticated by the caller;
serialized Gamma-derived gauge/compatibility gaps remain separate evidence.
"""
DIAGNOSTIC_EVENT_AUTHOR_DRAFT=True
DIAGNOSTIC_EVENT_AUTHORING_IN_PROGRESS=False

def diagnostic_event_pair_keep(label,value,keep):
 keep(label+'_hi',np.asarray(value[0]).copy());keep(label+'_lo',np.asarray(value[1]).copy());return value

def diagnostic_current_metric_event(r,z,potential_nodes,beta_nodes,current_metric_nodes,response_metric_nodes,*,potential_normalization,R,radial_side,sheet_side,provenance,keep,label):
 """One exact catalogue R at Z=0, from the authenticated half-plane Q1 state.
 potential_nodes=final_state[0], beta_nodes=sigma1_physical_beta_chi[0].
 Phi=B*(Q1 potential_nodes), retaining the literal source association.
 Both rate pairs are independent coefficient fields (a,b,c,d,e,f), not tensors.
 All physical/finite-preparation admission remains false. Both words persist.
 """
 assert r.shape==(87,) and z.shape==(45,) and r.dtype==z.dtype==np.float64
 assert potential_nodes.shape==beta_nodes.shape==(87,45)
 assert all(a.dtype==np.float64 and np.all(np.isfinite(a)) for a in (r,z,potential_nodes,beta_nodes))
 assert np.all(np.diff(r)>0) and np.all(np.diff(z)>0) and z[0]==0 and r[0]==0
 assert math.isfinite(R) and R>0 and sheet_side in ('positive','negative')
 B=float(potential_normalization);assert math.isfinite(B) and B>0;keep(label+'_source_potential_normalization',np.array(B))
 assert provenance['gauge_time_policy']=='original_stationary_seed_plus_fixed_N_beta_owned_K_lift'
 assert provenance['nonconverged_response_adopted_as_physical_solution'] is False and provenance['configuration_changed'] is False
 assert provenance.get('configuration_source') and provenance.get('current_rate_source') and provenance.get('response_source')
 keep(label+'_coordinate_event',np.array((0.,R,0.,0.)))
 for n,a in (('mesh_R',r),('mesh_Z',z),('potential_nodes',potential_nodes),('beta_nodes',beta_nodes)):keep(label+'_'+n,a.copy())
 for n,x in (('current_metric_nodes',current_metric_nodes),('full_response_metric_nodes',response_metric_nodes)):
  assert isinstance(x,tuple) and len(x)==2 and all(a.shape==(6,87,45) and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x)
  diagnostic_event_pair_keep(label+'_'+n,x,keep)
  assert all(np.all(a[:,0,:]==0) and np.all(a[3:5,:,0]==0) for a in x),'Original independent metric mask'
 nodes=diagnostic_event_pair_keep(label+'_current_plus_response_nodes',P.a_add(current_metric_nodes,response_metric_nodes),keep)
 defect=np.empty((6,87,45))
 for index in np.ndindex(defect.shape):defect[index]=math.fsum((float(current_metric_nodes[0][index]),float(current_metric_nodes[1][index]),float(response_metric_nodes[0][index]),float(response_metric_nodes[1][index]),-float(nodes[0][index]),-float(nodes[1][index])))
 keep(label+'_nodal_addition_exact_fsum_readout_defect',defect)
 lifted=tuple(a.copy() for a in nodes)
 for a in lifted:a[:,0,:]=a[:,1,:];a[3:5,:,0]=0
 diagnostic_event_pair_keep(label+'_axis_sheet_lifted_nodes',lifted,keep)
 contact=H.q1_radial_readout_contact(r,R,catalogue_R_kpc=R,mapping=dict(kind='coordinate_R_equals_catalogue_kpc'),side=radial_side)
 i=contact['selected_cell'];rw=contact['value_weights'];rd=contact['radial_derivative_weights'];dz=z[1]-z[0]
 weights=np.array((rw[0],rw[1],0.,0.));dR=np.array((rd[0],rd[1],0.,0.));dZ=np.array((-rw[0]/dz,-rw[1]/dz,rw[0]/dz,rw[1]/dz))
 keep(label+'_Q1_selected_cell',np.array((i,0),dtype=np.int64));keep(label+'_Q1_value_weights',weights);keep(label+'_Q1_R_weights',dR);keep(label+'_Q1_positive_Z_weights',dZ)
 corners=((i,0),(i+1,0),(i,1),(i+1,1));corners_phi=np.array([potential_nodes[index] for index in corners]);corners_beta=np.array([beta_nodes[index] for index in corners])
 keep(label+'_potential_corner_values',corners_phi);keep(label+'_beta_corner_values',corners_beta)
 # Literal four-corner source reduction, then B; independent fsum gap is saved.
 products=np.array([a*c for c in (corners_phi,corners_beta) for a in (weights,dR,dZ)])
 keep(label+'_scalar_Q1_six_product_rows',products);sums=[];gaps=[]
 for row in products:
  value=0.
  for x in row:value+=float(x)
  sums.append(value);gaps.append(math.fsum(map(float,row))-value)
 keep(label+'_scalar_Q1_literal_sums',np.array(sums));keep(label+'_scalar_Q1_fsum_reduction_gap',np.array(gaps))
 Phi=B*sums[0];b=sums[3];gr=B*np.array(sums[1:3]);br=np.array(sums[4:6])
 keep(label+'_sampled_potential_shift_RZ',np.r_[Phi,b,gr,br])
 F=np.zeros((6,6));F[0,0]=1.;F[0,1]=R**2;F[1,5]=1.;F[2,0]=R**2;F[3,3]=R;F[4,2]=R**3;F[5,4]=R**2;keep(label+'_physical_metric_F',F)
 hdot=P.a_dd(np.zeros(6))
 for corner,index in enumerate(corners):
  x=tuple(a[:,index[0],index[1]] for a in lifted);diagnostic_event_pair_keep(label+'_current_rate_corner%d'%corner,x,keep)
  factor=weights[corner]*F;keep(label+'_current_F_hat%d'%corner,factor)
  contribution=diagnostic_event_pair_keep(label+'_current_physical_rate_corner%d'%corner,P.a_matvec(factor,x),keep)
  hdot=diagnostic_event_pair_keep(label+'_physical_metric_rate_partial',P.a_add(hdot,contribution),keep)
 diagnostic_event_pair_keep(label+'_physical_metric_hdot_six',hdot,keep)
 N=math.exp(Phi);rho=R/N;m=math.exp(-2*Phi)
 assert all(math.isfinite(a) and a>0 for a in (N,rho,m))
 g=np.diag(np.array((-N*N+rho*rho*b*b,m,m,rho*rho)));g[0,3]=g[3,0]=rho*rho*b
 spatial=np.zeros((4,4,4))
 for coordinate in (1,2):
  nr=N*gr[coordinate-1];rr=rho*((1/R if coordinate==1 else 0)-gr[coordinate-1]);mr=-2*m*gr[coordinate-1];bb=br[coordinate-1]
  spatial[coordinate,0,0]=-2*N*nr+2*rho*rr*b*b+2*rho*rho*b*bb
  spatial[coordinate,0,3]=spatial[coordinate,3,0]=2*rho*rr*b+rho*rho*bb
  spatial[coordinate,1,1]=spatial[coordinate,2,2]=mr;spatial[coordinate,3,3]=2*rho*rr
 keep(label+'_analytic_owned_Ndot_betadot',np.zeros(4));keep(label+'_new_event_fixed_configuration_g',g.copy());keep(label+'_new_event_fixed_spatial_dg',spatial.copy())
 dg=P.a_dd(spatial)
 for q,(a,c) in enumerate(((1,1),(2,2),(3,3),(1,2),(1,3),(2,3))):
  for w in (0,1):dg[w][0,a,c]=dg[w][0,c,a]=hdot[w][q]
 for q,a in ((4,1),(5,2),(2,3)):
  x=diagnostic_event_pair_keep(label+'_current_time_cross',P.a_mul64(b,P.a_slice(hdot,q)),keep)
  for w in (0,1):dg[w][0,0,a]=dg[w][0,a,0]=x[w]
 x=diagnostic_event_pair_keep(label+'_time_time_contact',P.a_mul64(b*b,P.a_slice(hdot,2)),keep)
 for w in (0,1):dg[w][0,0,0]=x[w]
 if sheet_side=='negative':
  parity=np.array((1.,1.,-1.,1.));g=g*parity[:,None]*parity[None,:]
  dg=tuple(a*parity[:,None,None]*parity[None,:,None]*parity[None,None,:] for a in dg)
 keep(label+'_g_model',g.copy());diagnostic_event_pair_keep(label+'_full_dg_model',dg,keep)
 raw,rounding=P.a_sum(dg[0],dg[1]);keep(label+'_dg_binary64_readout',np.asarray(raw).copy());keep(label+'_dg_binary64_readout_defect',np.asarray(rounding).copy())
 assert np.all(np.isfinite(g)) and np.all(np.isfinite(raw)) and np.array_equal(g,g.T) and all(np.array_equal(a,a.swapaxes(-1,-2)) for a in dg)
 return dict(g_model=g,dg_model_pair=dg,dg_model_binary64=raw,dg_readout_defect=rounding,physical_metric_rate_pair=hdot,nodal_addition_readout_defect=defect,radius_contact=contact,
             coordinate_event=(0.,R,0.,0.),sheet_side=sheet_side,sheet_junction_convention='registered_reflected_half_plane_one_sided_jet_only',provenance=dict(provenance),
             configuration_changed=False,original_canonical_or_literal_response_admitted=False,finite_constraint_solution_admitted=False,physical_metric_admitted=False,
             readout_precision_admitted=False,Gauss_metric_or_jet_interpolated=False,EOS_or_native_action_evaluated=False,diagnostic_only=True)
