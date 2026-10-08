# Definitions only. Globals np,P (exact DD provider),K (repaired phase pair_sum).
# Caller supplies earned paired delta(phi_t); configuration and normal test values
# use the same binary64 convention as admitted134 normal lift/metric delta.
# The old stored-r normal representative and the literal Pphi representative are
# both retained. No configuration, EOS, source, canonical target or history reset.
def phase_normal_keep(name,x,keep):
 keep(name+'_hi',x[0]);keep(name+'_lo',x[1]);return x

def phase_normal_dot_matrix(x,A,y,keep,label):
 raised=P.a_matvec(A,y);phase_normal_keep(label+'_raised',raised,keep)
 return phase_normal_keep(label,K.phase_pair_sum(P.a_mul(x,raised),1,keep,label+'_sum'),keep)

def phase_normal_lift_values(s,c,f,b,keep,label):
 N,h,beta,U=c['N'],c['h'],c['beta'],s['U'];p=len(U)
 assert f.shape==(p,) and b.shape==(p,3)
 q=np.zeros((p,4,4));q[:,0,0]=-2*N*f+2*np.einsum('pi,pij,pj->p',beta,h,b);q[:,0,1:]=np.einsum('pij,pj->pi',h,b);q[:,1:,0]=q[:,0,1:]
 eta=np.empty_like(U);eta[:,0]=-U[:,0]*f/N;eta[:,1:]=-U[:,0,None]*b-beta*eta[:,0,None]
 duc=np.einsum('pab,pb->pa',q,U)+np.einsum('pab,pb->pa',s['g'],eta);dP=duc[:,:,None]*U[:,None,:]+s['uc'][:,:,None]*eta[:,None,:]
 dhi=-np.einsum('pac,pcd,pdb->pab',s['hi'],q,s['hi']);lm=np.einsum('pab,pba->p',s['hi'],q)/2
 dX=-np.einsum('pa,pab,pb->p',s['phi'],dhi,s['phi'])/(2*s['phase_X'])
 out=dict(q=q,eta=eta,dP=dP,dhi=dhi,lm=lm,dX=dX)
 for n,x in out.items():keep(label+'_'+n,x)
 return out

def phase_velocity_normal_contact(s,c,lift,w,keep,label):
 assert w[0].shape==w[1].shape==s['phase_X'].shape
 hi,dhi,dP,X,PX,PXX=s['hi'],lift['dhi'],lift['dP'],s['phase_X'],s['phase_PX'],s['phase_PXX'];phi=P.a_dd(s['phi'])
 raised=P.a_matvec(hi,phi);phase_normal_keep(label+'_raised_phi',raised,keep)
 dXv=P.a_div64(P.a_mul(P.a_mul64(-1.,P.a_slice(raised,(slice(None),0))),w),X,keep,label+'_velocity_clock');phase_normal_keep(label+'_delta_X_velocity',dXv,keep)
 dhi_phi=P.a_matvec(dhi,phi);dhiT_phi=P.a_matvec(dhi.transpose(0,2,1),phi)
 numerator=P.a_mul64(-.5,P.a_add(P.a_slice(dhi_phi,(slice(None),0)),P.a_slice(dhiT_phi,(slice(None),0))))
 ddX=P.a_sub(P.a_div64(P.a_mul(numerator,w),X,keep,label+'_mixed_clock_numerator'),P.a_div64(P.a_mul64(lift['dX'],dXv),X,keep,label+'_mixed_clock_denominator'));phase_normal_keep(label+'_delta_normal_X',ddX,keep)
 pressure=P.a_add(P.a_mul64(PXX,P.a_mul64(lift['dX'],dXv)),P.a_mul64(PX,ddX));pressure=P.a_add(pressure,P.a_mul64(lift['lm'],P.a_mul64(PX,dXv)));phase_normal_keep(label+'_absolute_pressure_contact',pressure,keep)
 rv=P.a_mul64(s['P'][:,:,0],(w[0][:,None],w[1][:,None]));drv=P.a_mul64(dP[:,:,0],(w[0][:,None],w[1][:,None]));phase_normal_keep(label+'_delta_relative_phase',rv,keep);phase_normal_keep(label+'_delta_normal_relative_phase',drv,keep)
 registered_r=P.a_dd(s['r']);registered_dr=P.a_dd(np.einsum('pab,pb->pa',dP,s['phi']))
 literal_r=P.a_matvec(s['P'],phi);literal_dr=P.a_matvec(dP,phi)
 phase_normal_keep(label+'_relative_primal_construction_gap',P.a_sub(literal_r,registered_r),keep);phase_normal_keep(label+'_relative_normal_construction_gap',P.a_sub(literal_dr,registered_dr),keep)
 contacts={}
 for family,r,dr in (('registered_normal',registered_r,registered_dr),('literal_action',literal_r,literal_dr)):
  prefix=label+'_'+family
  t=P.a_add(phase_normal_dot_matrix(rv,dhi,r,keep,prefix+'_inverse_left'),phase_normal_dot_matrix(r,dhi,rv,keep,prefix+'_inverse_right'))
  t=P.a_add(t,P.a_mul64(2.,phase_normal_dot_matrix(rv,hi,dr,keep,prefix+'_projector_left')));t=P.a_add(t,P.a_mul64(2.,phase_normal_dot_matrix(r,hi,drv,keep,prefix+'_projector_right')))
  measure=P.a_add(phase_normal_dot_matrix(rv,hi,r,keep,prefix+'_measure_left'),phase_normal_dot_matrix(r,hi,rv,keep,prefix+'_measure_right'))
  relative=P.a_mul64(-.5,P.a_add(t,P.a_mul64(lift['lm'],measure)));phase_normal_keep(prefix+'_relative_contact',relative,keep)
  contacts[family]=P.a_mul64(c['dens'],P.a_add(pressure,relative));phase_normal_keep(prefix+'_density_contact',contacts[family],keep)
 gap=P.a_sub(contacts['literal_action'],contacts['registered_normal']);phase_normal_keep(label+'_literal_minus_registered_normal_gap',gap,keep)
 return dict(**contacts,literal_minus_registered_normal_gap=gap,delta_X_velocity=dXv,delta_normal_X=ddX,absolute_pressure_contact=pressure,configuration_updated=False,phase_charge_restored=False,normal_constraints_qualified=False)
