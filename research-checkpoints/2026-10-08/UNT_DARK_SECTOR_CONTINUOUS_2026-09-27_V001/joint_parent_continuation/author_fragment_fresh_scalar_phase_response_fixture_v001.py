# Definitions only; globals np, P, K, phase_response_solve. No author evaluation.
# Artificial unit cells; no EOS, galaxy state, parameter or physical preparation.
# Exact tensor Q1 mass has lambda_min >= (1/6)^2 by row Gershgorin bounds.
# Frozen Gaussian factors and DD action roundoff are bounded conservatively by
# 512*eps in operator norm; 1/36 - 512*eps > 1/40. The allowance below also
# retains the independent exact RHS versus frozen-geometry construction defect.
def fresh_phase_response_control():
 label='fresh_phase_response'
 keep=P.capture
 r=np.arange(87,dtype=float);z=np.arange(45,dtype=float)
 alpha=(1.-1./np.sqrt(3.))/2.;beta=(1.+1./np.sqrt(3.))/2.
 hats=np.empty((4,4,3,86,44));R=np.empty((4,86,44));dv=np.empty_like(R)
 for iq,(ar,az) in enumerate(((alpha,alpha),(beta,alpha),(alpha,beta),(beta,beta))):
  R[iq]=np.broadcast_to(r[:-1,None]+ar,(86,44));dv[iq]=R[iq]/4.
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   nr=ar if di else 1.-ar;nz=az if dj else 1.-az
   hats[iq,corner,0]=nr*nz
   hats[iq,corner,1]=(1. if di else -1.)*nz
   hats[iq,corner,2]=nr*(1. if dj else -1.)
 keep(label+'_r',r);keep(label+'_z',z);keep(label+'_R',R);keep(label+'_dv',dv);keep(label+'_hats',hats)
 g=dict(R=R.reshape(4,3784),dv=dv.reshape(4,3784),hats=hats)
 radial_rhs=np.ones(87);radial_rhs[0]=0.;radial_rhs[1]=1.5;radial_rhs[-1]=.5
 vertical_rhs=np.ones(45);vertical_rhs[[0,-1]]=.5
 radial_diag=np.full(87,2./3.);radial_diag[0]=0.;radial_diag[1]=4./3.;radial_diag[-1]=1./3.
 vertical_diag=np.full(45,2./3.);vertical_diag[[0,-1]]=1./3.
 rhs=radial_rhs[:,None]*vertical_rhs[None,:]
 diagonal=radial_diag[:,None]*vertical_diag[None,:]
 exact=np.ones((87,45));exact[0]=0.
 keep(label+'_independent_rhs',rhs);keep(label+'_independent_diagonal',diagonal);keep(label+'_exact_nodal_solution',exact)
 H=P.a_dd(np.ones(15136));keep(label+'_H_hi',H[0]);keep(label+'_H_lo',H[1])
 answer=phase_response_solve(H,P.a_dd(diagonal),P.a_dd(rhs),g,keep,label,cap=160,max_cycles=1)
 nodes=answer['nodal_pair'];error=P.a_sub(nodes,P.a_dd(exact))
 keep(label+'_nodal_error_hi',error[0]);keep(label+'_nodal_error_lo',error[1])
 mask=P.scalar_mask();assert np.count_nonzero(mask)==3870
 residual=answer['original_residual'];ratios=answer['original_ratios']
 residual_norm=float(np.linalg.norm(residual[0]+residual[1]))
 node_norm=float(np.linalg.norm((nodes[0]+nodes[1])[mask]))
 error_norm=float(np.linalg.norm((error[0]+error[1])[mask]))
 eps=np.finfo(float).eps;construction_allowance=512.*eps*(np.sqrt(3870.)+node_norm)
 lower_bound=1./36.-512.*eps;assert lower_bound>1./40.
 coercive_error_bound=40.*(residual_norm+construction_allowance)
 keep(label+'_independent_error_bound_operands',np.array((residual_norm,node_norm,error_norm,construction_allowance,lower_bound,coercive_error_bound)))
 keep(label+'_original_ratios',ratios)
 # One control tests the actual original-row 1e-10 solve and its coercive nodal
 # error consequence. It intentionally does not impose 2e-11 nodal equality.
 actual=np.array((ratios[0],ratios[1],error_norm));expected=np.zeros(3)
 envelope=np.array((P.LINEAR_TOL/P.TOL,P.LINEAR_TOL/P.TOL,coercive_error_bound/P.TOL))
 P.check(label+'_original_rows_and_coercive_nodal_error',actual,expected,envelope)
 return dict(kind='fresh_unit_cell_scalar_Q1_phase_response',space_dimension=3870,
  solve_cap=160,max_cycles=1,history=answer['history'],linearized_response_admitted=answer['linearized_weak_charge_response_admitted'],
  exact_mass_lower_bound='1/36',rounding_safe_inverse_bound=40.,construction_operator_bound='512*binary64_epsilon',
  original_ratios=ratios.tolist(),nodal_error_norm=error_norm,coercive_error_bound=coercive_error_bound,
  independent_rhs_and_diagonal=True,physical_EOS_or_state=False,checkpoint_owned_by_caller=True)
