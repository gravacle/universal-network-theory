# Guarded definitions only: no imports, calls, solve or numerical author evaluation.
# Globals np/P; P is the exact admitted DD-node arithmetic/basis/scatter provider.
# This NEW geometric mass uses adjoint F64 and hat64 separately on both sides.
# Do not substitute old rounded Fhat64 temporal evaluation into this Riesz action.
AUTHOR_DRAFT=True
RIESZ_TARGET=('CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002_00006_READOUT.npz','metric_primitive_momentum_hi','metric_primitive_momentum_lo')
RIESZ_SOURCE_PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_phase_fixed_weak_charge_preparation_v003.py':'ed18caa749cbbfef40956ee4764390d688aaf6a1567912317d6cc81c9851d079',
 'CROSS_U_WEAK_NODAL_METRIC_TEMPORAL_AND_CMC_EXTENSION_V001.md':'78491aa4158dec6152a19136d5b3265cc63cdc965ebf4002d8df371074b46806'}

def metric_riesz_keep(name,x,keep):
 keep(name+'_hi',x[0]);keep(name+'_lo',x[1]);return x

def metric_riesz_geometry(c,g,keep,label):
 # c combines the four authenticated primitive COLUMN reference charts in order.
 # Stored inverse and measure bits define the registered positive quadrature metric.
 h=c['h'];ih=c['ih'];mu=c['sqrt_h'];R=g['R'].reshape(15136)
 assert h.shape==ih.shape==(15136,3,3) and mu.shape==R.shape==(15136,)
 assert np.all(np.isfinite(h)) and np.all(np.isfinite(ih)) and np.all(np.isfinite(mu)) and np.all(mu>0) and np.all(R>0)
 off=np.ones((3,3),bool);np.fill_diagonal(off,False)
 assert np.all(h[:,off]==0) and np.all(ih[:,off]==0)
 assert np.all(np.diagonal(h,axis1=1,axis2=2)>0) and np.all(np.diagonal(ih,axis1=1,axis2=2)>0)
 keep(label+'_reference_h',h);keep(label+'_reference_ih',ih);keep(label+'_reference_sqrt_h',mu)
 inverse_defect=np.einsum('pij,pjk->pik',h,ih)-np.eye(3)[None]
 inverse_bound=np.einsum('pij,pjk->pik',abs(h),abs(ih))+np.eye(3)[None]
 keep(label+'_reference_inverse_defect',inverse_defect);keep(label+'_reference_inverse_bound',inverse_bound)
 A=h[:,0,0];conformal=np.stack((h[:,1,1]-A,h[:,2,2]-A*R**2),axis=1)
 keep(label+'_reference_conformal_definition_gap',conformal)
 # Physical local order RR,ZZ,phiphi,RZ,Rphi,Zphi. Cross slots are 2*pi^ij.
 out=[]
 for i,k,factor in ((0,0,1.),(1,1,1.),(2,2,1.),(0,1,2.),(0,2,2.),(1,2,2.)):
  q=P.a_mul64(factor*mu,P.a_prod(ih[:,i,i],ih[:,k,k]))
  out.append(q);metric_riesz_keep(label+'_local_weight_%d'%len(out),q,keep)
 weights=P.a_stack(out,axis=1);metric_riesz_keep(label+'_local_weights',weights,keep)
 assert np.all(weights[0]>abs(weights[1]))
 return weights

def metric_riesz_coefficient_value(x,g,keep,label):
 assert x[0].shape==x[1].shape==(6,87,45)
 y=(P.lift_metric(x[0]),P.lift_metric(x[1]));out=P.a_dd(np.zeros((4,86,44,6)))
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   val=(np.moveaxis(y[0][:,di:86+di,dj:44+dj],0,-1),np.moveaxis(y[1][:,di:86+di,dj:44+dj],0,-1))
   term=P.a_mul64(g['hats'][iq,corner,0][...,None],val)
   update=P.a_add(P.a_slice(out,iq),term);out[0][iq]=update[0];out[1][iq]=update[1]
   metric_riesz_keep(label+'_coefficient_partial',out,keep)
 return P.a_reshape(out,(15136,6))

def metric_riesz_action(x,weights,g,keep,label):
 coefficients=metric_riesz_coefficient_value(x,g,keep,label)
 H=P.a_matvec(P.dd_metric_F(g['R'].reshape(15136)),coefficients)
 metric_riesz_keep(label+'_covariant_tensor_local',H,keep)
 density=P.a_mul(weights,H);metric_riesz_keep(label+'_canonical_representer_density_local',density,keep)
 weak=P.dd_metric_scatter(density,g,keep);metric_riesz_keep(label+'_weak_metric_mass',weak,keep)
 return weak,density,H

def metric_riesz_positive_envelope(x,weights,g,keep,label):
 # Positive hats/F/R factors propagate both signed words before any cancellation.
 magnitudes=P.a_dd(abs(x[0])+abs(x[1]))
 eweights=P.a_dd(abs(weights[0])+abs(weights[1]))
 envelope,_,_=metric_riesz_action(magnitudes,eweights,g,keep,label+'_positive')
 metric_riesz_keep(label+'_positive_weak_envelope',envelope,keep);return envelope

def metric_riesz_local_blocks(weights,g,keep,label):
 # The seven node-local entries provide a 2x2 (a,b) block plus c,d,e,f diagonals.
 R=g['R'].reshape(15136);F=P.dd_metric_F(R);r2=F[:,0,1];r3=F[:,4,2]
 w=lambda a:P.a_slice(weights,(slice(None),a))
 r22=P.a_prod(r2,r2);r32=P.a_prod(r3,r3);r12=P.a_prod(R,R)
 point=P.a_stack((P.a_add(w(0),P.a_mul(w(2),r22)),P.a_mul64(r2,w(0)),P.a_mul(w(0),r22),P.a_mul(w(4),r32),P.a_mul(w(3),r12),P.a_mul(w(5),r22),w(1)),axis=1)
 metric_riesz_keep(label+'_point_block_entries',point,keep)
 point=P.a_reshape(point,(4,86,44,7));out=P.a_dd(np.zeros((7,87,45)))
 for iq in range(4):
  weighted=P.a_mul64((g['dv'][iq]/g['R'][iq]).reshape(86,44,1),P.a_slice(point,iq))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=P.a_dd(g['hats'][iq,corner,0].copy())
   if di==0:hat[0][0]=0;hat[1][0]=0
   else:
    pair=P.a_sum(hat[0][0],g['hats'][iq,corner-1,0,0]);hat[0][0]=pair[0];hat[1][0]=pair[1]
   term=P.a_mul(P.a_reshape(P.a_mul(hat,hat),(86,44,1)),weighted)
   key=(slice(None),slice(di,86+di),slice(dj,44+dj));update=P.a_add(P.a_slice(out,key),P.a_transpose(term,(2,0,1)))
   out[0][key]=update[0];out[1][key]=update[1];metric_riesz_keep(label+'_nodal_blocks_partial',out,keep)
 out[0][:,0]=0;out[1][:,0]=0
 # d,e coefficients are odd across the sheet; every other coefficient is even.
 out[0][4:6,:,0]=0;out[1][4:6,:,0]=0
 metric_riesz_keep(label+'_nodal_blocks',out,keep)
 return out

def metric_riesz_certificate(x,target,weights,g,scale,keep,label):
 mask=P.metric_mask();assert np.count_nonzero(mask)==23048
 assert target[0].shape==target[1].shape==scale.shape==(6,87,45) and np.all(scale[mask]>0)
 action,density,H=metric_riesz_action(x,weights,g,keep,label+'_original')
 residual=P.a_sub(target,action);metric_riesz_keep(label+'_original_target_residual',residual,keep)
 rhs=(target[0]+target[1])[mask];res=(residual[0]+residual[1])[mask];s=scale[mask]
 ratios=P.original_ratios(res,rhs,s);keep(label+'_original_raw_and_scaled_ratios',ratios)
 return dict(action=action,residual=residual,ratios=ratios,canonical_density=density,covariant_representer=H,
  numerical_representer_admitted=bool(np.all(ratios<=1e-10)),continuum_stress_unique=False,
  physical_TT_or_exterior_admitted=False,reference_state_changed=False)
