# New literal phase Legendre readout; definitions only, fixed authentic configuration.
# Globals: np, P (admitted DD helpers). keep captures completed pairs before later calls.
def phase_pair_keep(name,x,keep):
 keep(name+'_hi',x[0]);keep(name+'_lo',x[1]);return x

def phase_pair_sum(x,axis,keep,label):
 assert isinstance(axis,int) and 0<=axis<x[0].ndim
 out=P.a_dd(np.zeros(x[0].shape[:axis]+x[0].shape[axis+1:]))
 for i in range(x[0].shape[axis]):
  key=[slice(None)]*x[0].ndim;key[axis]=i;out=P.a_add(out,P.a_slice(x,tuple(key)));phase_pair_keep(label+'_through%d'%i,out,keep)
 return out

def phase_literal_charge_hessian(s,c,keep,label):
 # P is the literal stored projector, not a reimposed exact unit reduction.
 phi=P.a_dd(s['phi']);ih=P.a_dd(s['hi']);projector=P.a_dd(s['P']);p=len(s['phi']);X=s['phase_X'];PX=s['phase_PX'];PXX=s['phase_PXX']
 assert X.shape==PX.shape==PXX.shape==(p,) and np.all(np.isfinite(X)) and np.all(X>0)
 raised=P.a_matvec(ih,phi);phase_pair_keep(label+'_raised_phase',raised,keep)
 clock_velocity=P.a_div64(raised,X[:,None],keep,label+'_clock_normalization');phase_pair_keep(label+'_clock_velocity',clock_velocity,keep)
 pressure=P.a_mul64(-PX[:,None],clock_velocity);phase_pair_keep(label+'_pressure_current',pressure,keep)
 r=P.a_matvec(projector,phi);phase_pair_keep(label+'_projected_phase',r,keep);hi_r=P.a_matvec(ih,r);phase_pair_keep(label+'_raised_relative_phase',hi_r,keep)
 relative=P.a_matvec(P.a_transpose(projector,(0,2,1)),hi_r);phase_pair_keep(label+'_literal_relative_current_negative',relative,keep)
 action_J=P.a_sub(pressure,relative);phase_pair_keep(label+'_literal_action_current',action_J,keep)
 registered_J=P.a_sub(pressure,hi_r);phase_pair_keep(label+'_registered_current_readout',registered_J,keep)
 action_p=P.a_mul64(c['dens'],P.a_slice(action_J,(slice(None),0)));phase_pair_keep(label+'_literal_action_canonical_density',action_p,keep)
 registered_p=P.a_mul64(c['dens'],P.a_slice(registered_J,(slice(None),0)));phase_pair_keep(label+'_registered_canonical_density_readout',registered_p,keep)
 n0=P.a_slice(clock_velocity,(slice(None),0));n02=P.a_mul(n0,n0);phase_pair_keep(label+'_clock_velocity_time_square',n02,keep)
 pressure_curvature=P.a_mul64(PXX,n02);phase_pair_keep(label+'_pressure_second_derivative_term',pressure_curvature,keep)
 inverse_clock=P.a_add(P.a_dd(s['hi'][:,0,0]),n02);phase_pair_keep(label+'_inverse_plus_clock_square',inverse_clock,keep)
 pressure_gradient=P.a_div64(P.a_mul64(PX,inverse_clock),X,keep,label+'_pressure_gradient_normalization');phase_pair_keep(label+'_pressure_first_derivative_term',pressure_gradient,keep)
 p0=P.a_slice(projector,(slice(None),slice(None),0));h_p0=P.a_matvec(ih,p0);phase_pair_keep(label+'_inverse_projector_time_column',h_p0,keep)
 A00=phase_pair_sum(P.a_mul(p0,h_p0),1,keep,label+'_relative_temporal_hessian');phase_pair_keep(label+'_literal_projector_temporal_coefficient',A00,keep)
 pressure_H=P.a_sub(pressure_curvature,pressure_gradient);phase_pair_keep(label+'_pressure_temporal_hessian',pressure_H,keep)
 H=P.a_mul64(c['dens'],P.a_sub(pressure_H,A00));phase_pair_keep(label+'_literal_temporal_hessian',H,keep)
 H_registered=P.a_mul64(c['dens'],P.a_sub(pressure_H,P.a_slice(h_p0,(slice(None),0))));phase_pair_keep(label+'_registered_temporal_hessian',H_registered,keep)
 up=P.a_matvec(P.a_dd(c['ih']),P.a_dd(c['u']));norm_b=phase_pair_sum(P.a_mul(P.a_dd(c['u']),up),1,keep,label+'_norm_b');phase_pair_keep(label+'_native_spatial_norm_b',norm_b,keep)
 reduced=P.a_div64(P.a_mul64(c['sqrt_h'],P.a_sub(P.a_dd(PXX),norm_b)),c['N'],keep,label+'_reduced_ADM_hessian');phase_pair_keep(label+'_reduced_ADM_hessian',reduced,keep)
 delta_current=P.a_sub(action_J,registered_J);phase_pair_keep(label+'_action_minus_registered_current_gap',delta_current,keep)
 delta_p=P.a_sub(action_p,registered_p);phase_pair_keep(label+'_action_minus_registered_density_gap',delta_p,keep)
 reduced_gap=P.a_sub(H,reduced);phase_pair_keep(label+'_literal_minus_reduced_hessian_gap',reduced_gap,keep)
 hgap=P.a_sub(H,H_registered);phase_pair_keep(label+'_action_minus_registered_hessian_gap',hgap,keep)
 invariant=phase_pair_sum(P.a_mul(phi,raised),1,keep,label+'_clock_invariant');clock_gap=P.a_add(P.a_prod(X,X),invariant);phase_pair_keep(label+'_owned_X_squared_plus_phi_inverse_phi_gap',clock_gap,keep)
 Pe=np.eye(4)[None]+abs(s['uc'])[:,:,None]*abs(s['U'])[:,None,:];ehi=abs(s['hi']);ephi=abs(s['phi']);ev=np.einsum('pab,pb->pa',ehi,ephi);eA=np.einsum('pai,pab,pbj->pij',Pe,ehi,Pe)
 eJ=abs(PX[:,None]/X[:,None])*ev+np.einsum('pab,pb->pa',eA,ephi);eH=abs(c['dens'])*((abs(PXX)/X**2+abs(PX)/X**3)*ev[:,0]**2+abs(PX/X)*ehi[:,0,0]+eA[:,0,0])
 keep(label+'_current_operation_envelope',eJ);keep(label+'_hessian_operation_envelope',eH)
 return dict(action_current=action_J,registered_current=registered_J,action_canonical_density=action_p,registered_canonical_density=registered_p,literal_hessian=H,registered_hessian=H_registered,reduced_hessian=reduced,current_gap=delta_current,density_gap=delta_p,hessian_gap=hgap,reduced_gap=reduced_gap,clock_gap=clock_gap,norm_b=norm_b,current_envelope=eJ,hessian_envelope=eH)

def phase_scalar_value(x,g,keep,label):
 assert x[0].shape==x[1].shape==(87,45)
 y=tuple(P.scalar_lift(a) for a in x);out=P.a_dd(np.zeros((4,86,44)))
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   term=P.a_mul64(g['hats'][iq,corner,0],P.a_slice(y,(slice(di,86+di),slice(dj,44+dj))))
   updated=P.a_add(P.a_slice(out,iq),term);out[0][iq]=updated[0];out[1][iq]=updated[1];phase_pair_keep(label+'_value_partial',out,keep)
 return P.a_reshape(out,(15136,))

def phase_mass_action(x,H,g,keep,label):
 value=phase_scalar_value(x,g,keep,label);weighted=P.a_mul(H,value);phase_pair_keep(label+'_point_charge_response',weighted,keep)
 return P.dd_scalar_scatter(weighted,g,keep,label+'_weak_mass')

def phase_mass_diagonal(H,g,keep,label):
 out=P.a_dd(np.zeros((87,45)));Hp=P.a_reshape(H,(4,86,44))
 for iq in range(4):
  weighted=P.a_mul64((g['dv'][iq]/g['R'][iq]).reshape(86,44),P.a_slice(Hp,iq));phase_pair_keep(label+'_weighted_H',weighted,keep)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0].copy()
   if di==0:hat[0]=0
   else:hat[0]+=g['hats'][iq,corner-1,0,0]
   # The merged-axis effective scalar hat enters twice, retaining its low product.
   term=P.a_mul64(hat,P.a_mul64(hat,weighted));key=(slice(di,86+di),slice(dj,44+dj));updated=P.a_add(P.a_slice(out,key),term)
   out[0][key]=updated[0];out[1][key]=updated[1];phase_pair_keep(label+'_mass_diagonal_partial',out,keep)
 out[0][0]=0;out[1][0]=0;phase_pair_keep(label+'_mass_diagonal',out,keep);return out
