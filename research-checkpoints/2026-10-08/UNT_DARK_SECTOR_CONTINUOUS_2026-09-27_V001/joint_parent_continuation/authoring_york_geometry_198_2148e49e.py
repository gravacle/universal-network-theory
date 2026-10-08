# Guarded definitions only: globals np/P, no imports/calls/evaluation/solver.
# h,ih are saved reference arrays; dh is the saved two-word spatial h first jet.
# Unknown W=(R*even, sheet-odd vertical, even azimuthal) uses11135 compact hats.
# This auxiliary zero-potential boundary is a decomposition convention, not a wall.
AUTHOR_DRAFT=True

def york_pair_keep(name,x,keep):
 keep(name+'_hi',x[0]);keep(name+'_lo',x[1]);return x

def york_vector_mask():
 mask=np.ones((3,87,45),bool);mask[:,0]=False;mask[:,-1]=False;mask[:,:,-1]=False;mask[1,:,0]=False
 assert np.count_nonzero(mask)==11135;return mask

def york_vector_lift(x):
 assert x.shape==(3,87,45)
 y=x.copy();y[:,0]=y[:,1];y[:,-1]=0;y[:,:,-1]=0;y[1,:,0]=0;return y

def york_vector_restrict(x,keep,label):
 assert x[0].shape==x[1].shape==(3,87,45)
 out=(x[0].copy(),x[1].copy())
 axis=P.a_add(P.a_slice(out,(slice(None),1,slice(None))),P.a_slice(out,(slice(None),0,slice(None))))
 for word in (0,1):out[word][:,1]=axis[word];out[word][:,0]=0;out[word][:,-1]=0;out[word][:,:,-1]=0;out[word][1,:,0]=0
 return york_pair_keep(label+'_restricted',out,keep)

def york_hat_factors(g,iq,corner,component):
 # Exactly the existing normal-space three coordinate value/R/Z factors.
 N,NR,NZ=g['hats'][iq,corner];R=g['R'][iq].reshape(86,44)
 if component==0:return np.stack((R*N,R*NR+N,R*NZ),axis=-1)
 return np.stack((N,NR,NZ),axis=-1)

def york_vector_jets(x,g,keep,label):
 assert x[0].shape==x[1].shape==(3,87,45)
 y=(york_vector_lift(x[0]),york_vector_lift(x[1]));out=P.a_dd(np.zeros((4,86,44,3,3)))
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for component in range(3):
    factor=york_hat_factors(g,iq,corner,component)
    val=(y[0][component,di:86+di,dj:44+dj,None],y[1][component,di:86+di,dj:44+dj,None])
    key=(iq,slice(None),slice(None),component,slice(None));update=P.a_add(P.a_slice(out,key),P.a_mul64(factor,val))
    out[0][key]=update[0];out[1][key]=update[1];york_pair_keep(label+'_jets_partial',out,keep)
 return P.a_reshape(out,(15136,3,3))

def york_geometry_maps(h,ih,dh,keep,label):
 # Maps[p,component,jet=value/R/Z,i,j] form L_h W directly from Lie_hW.
 p=len(h);assert h.shape==ih.shape==(p,3,3) and dh[0].shape==dh[1].shape==(p,3,3,3)
 maps=P.a_dd(np.zeros((p,3,3,3,3)));envelope=np.zeros((p,3,3,3,3))
 two_thirds=P.a_div64(P.a_mul64(2.,P.a_dd(h)),3.,keep,label+'_two_thirds_metric')
 for k in range(3):
  trace=P.a_dd(np.zeros(p));etrace=np.zeros(p)
  for i in range(3):
   for j in range(3):
    slot=P.a_slice(dh,(slice(None),k,i,j));trace=P.a_add(trace,P.a_mul64(ih[:,i,j],slot));etrace+=abs(ih[:,i,j])*(abs(slot[0])+abs(slot[1]));york_pair_keep(label+'_metric_gradient_trace_partial',trace,keep)
  third=P.a_div64(trace,3.,keep,label+'_gradient_trace_%d'%k)
  value=P.a_sub(P.a_slice(dh,(slice(None),k)),P.a_mul64(h,(third[0][:,None,None],third[1][:,None,None])))
  for word in (0,1):maps[word][:,k,0]=value[word]
  envelope[:,k,0]=abs(dh[0][:,k])+abs(dh[1][:,k])+abs(h)*(etrace/3.)[:,None,None]
  york_pair_keep(label+'_maps_partial',maps,keep)
  for derivative in range(2):
   q=P.a_dd(np.zeros((p,3,3)));eq=np.zeros((p,3,3))
   for i in range(3):
    for j in range(3):
     # Preserve each product separately; the two h terms may themselves cancel.
     value=P.a_add(P.a_dd(h[:,k,j] if i==derivative else np.zeros(p)),P.a_dd(h[:,i,k] if j==derivative else np.zeros(p)))
     if derivative==k:value=P.a_sub(value,P.a_slice(two_thirds,(slice(None),i,j)))
     for word in (0,1):q[word][:,i,j]=value[word]
     eq[:,i,j]=(abs(h[:,k,j]) if i==derivative else 0.)+(abs(h[:,i,k]) if j==derivative else 0.)+(2.*abs(h[:,i,j])/3. if derivative==k else 0.)
   for word in (0,1):maps[word][:,k,derivative+1]=q[word]
   envelope[:,k,derivative+1]=eq;york_pair_keep(label+'_maps_partial',maps,keep)
 keep(label+'_map_operation_envelope',envelope)
 return maps,envelope

def york_apply_maps(jets,maps,keep,label):
 p=jets[0].shape[0];assert jets[0].shape==jets[1].shape==(p,3,3)
 out=P.a_dd(np.zeros((p,3,3)))
 for component in range(3):
  for jet in range(3):
   scalar=P.a_slice(jets,(slice(None),component,jet));term=P.a_mul(P.a_slice(maps,(slice(None),component,jet)),(scalar[0][:,None,None],scalar[1][:,None,None]))
   out=P.a_add(out,term);york_pair_keep(label+'_longitudinal_partial',out,keep)
 return out

def york_map_adjoint(tensor,maps,keep,label):
 p=len(tensor[0]);assert tensor[0].shape==tensor[1].shape==(p,3,3)
 out=P.a_dd(np.zeros((p,3,3)))
 for component in range(3):
  for jet in range(3):
   value=P.a_dd(np.zeros(p))
   for i in range(3):
    for j in range(3):value=P.a_add(value,P.a_mul(P.a_slice(tensor,(slice(None),i,j)),P.a_slice(maps,(slice(None),component,jet,i,j))));york_pair_keep(label+'_adjoint_contraction_partial',value,keep)
   for word in (0,1):out[word][:,component,jet]=value[word]
   york_pair_keep(label+'_coordinate_adjoint_partial',out,keep)
 return out

def york_vector_scatter(coeff,g,keep,label):
 assert coeff[0].shape==coeff[1].shape==(15136,3,3)
 field=P.a_reshape(coeff,(4,86,44,3,3));out=P.a_dd(np.zeros((3,87,45)))
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for component in range(3):
    factor=york_hat_factors(g,iq,corner,component);value=P.a_dd(np.zeros((86,44)))
    for jet in range(3):value=P.a_add(value,P.a_mul64(factor[...,jet],P.a_slice(field,(iq,slice(None),slice(None),component,jet))))
    value=P.a_mul64((g['dv'][iq]/g['R'][iq]).reshape(86,44),value)
    key=(component,slice(di,86+di),slice(dj,44+dj));update=P.a_add(P.a_slice(out,key),value)
    out[0][key]=update[0];out[1][key]=update[1];york_pair_keep(label+'_scatter_partial',out,keep)
 return york_vector_restrict(out,keep,label)

def york_raised_density(L,ih,sqrt_h,keep,label):
 p=len(ih);assert L[0].shape==L[1].shape==(p,3,3) and sqrt_h.shape==(p,)
 off=np.ones((3,3),bool);np.fill_diagonal(off,False);assert np.all(ih[:,off]==0) and np.all(np.diagonal(ih,axis1=1,axis2=2)>0) and np.all(sqrt_h>0)
 out=P.a_dd(np.zeros((p,3,3)))
 for i in range(3):
  for j in range(3):
   factor=P.a_mul64(sqrt_h,P.a_prod(ih[:,i,i],ih[:,j,j]));value=P.a_mul(factor,P.a_slice(L,(slice(None),i,j)))
   for word in (0,1):out[word][:,i,j]=value[word]
   york_pair_keep(label+'_raised_longitudinal_density_partial',out,keep)
 return out

def york_weak_source(pi_tf,maps,g,keep,label):
 coeff=york_map_adjoint(pi_tf,maps,keep,label+'_point_source')
 return york_vector_scatter(coeff,g,keep,label+'_source')

def york_mass_action(x,maps,ih,sqrt_h,g,keep,label):
 jets=york_vector_jets(x,g,keep,label+'_trial');L=york_apply_maps(jets,maps,keep,label+'_trial')
 density=york_raised_density(L,ih,sqrt_h,keep,label+'_trial')
 out=york_vector_scatter(york_map_adjoint(density,maps,keep,label+'_point_action'),g,keep,label+'_action')
 return out,L,density


def york_hat_envelope(g,iq,corner,component):
 N,NR,NZ=g['hats'][iq,corner];R=g['R'][iq].reshape(86,44)
 if component==0:return np.stack((R*abs(N),R*abs(NR)+abs(N),R*abs(NZ)),axis=-1)
 return np.stack((abs(N),abs(NR),abs(NZ)),axis=-1)

def york_positive_scatter(coeff,g,keep,label):
 assert coeff.shape==(15136,3,3) and np.all(coeff>=0)
 field=coeff.reshape(4,86,44,3,3);out=np.zeros((3,87,45))
 for iq in range(4):
  weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for component in range(3):
    value=weight*np.sum(field[iq,:,:,component]*york_hat_envelope(g,iq,corner,component),axis=-1)
    out[component,di:86+di,dj:44+dj]+=value
 out[:,1]+=out[:,0];out[:,0]=0;out[:,-1]=0;out[:,:,-1]=0;out[1,:,0]=0
 keep(label+'_positive_scatter',out);return out

def york_source_envelope(pi_tf,map_envelope,g,keep,label):
 e=abs(pi_tf[0])+abs(pi_tf[1]);coeff=np.einsum('pkqij,pij->pkq',map_envelope,e)
 keep(label+'_point_source_operation_envelope',coeff)
 return york_positive_scatter(coeff,g,keep,label)

def york_local_diagonal(maps,map_envelope,ih,sqrt_h,g,keep,label):
 assert maps[0].shape==maps[1].shape==map_envelope.shape==(15136,3,3,3,3)
 point=P.a_reshape(maps,(4,86,44,3,3,3,3));env=map_envelope.reshape(4,86,44,3,3,3,3)
 inverse=ih.reshape(4,86,44,3,3);measure=sqrt_h.reshape(4,86,44)
 out=P.a_dd(np.zeros((3,87,45)));eout=np.zeros((3,87,45))
 for iq in range(4):
  weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for component in range(3):
    factor=P.a_dd(york_hat_factors(g,iq,corner,component).copy());efactor=york_hat_envelope(g,iq,corner,component).copy()
    # Axis identification makes a single coefficient's hat the SUM of both
    # first-cell radial corners. It enters twice in the exact diagonal.
    if di==0:factor[0][0]=0;factor[1][0]=0;efactor[0]=0
    else:
     joined=P.a_add(P.a_slice(factor,0),P.a_dd(york_hat_factors(g,iq,corner-1,component)[0]))
     factor[0][0]=joined[0];factor[1][0]=joined[1];efactor[0]+=york_hat_envelope(g,iq,corner-1,component)[0]
    L=P.a_dd(np.zeros((86,44,3,3)));eL=np.zeros((86,44,3,3))
    for jet in range(3):
     v=P.a_slice(factor,(slice(None),slice(None),jet));term=P.a_mul(P.a_slice(point,(iq,slice(None),slice(None),component,jet)),(v[0][...,None,None],v[1][...,None,None]))
     L=P.a_add(L,term);eL+=env[iq,:,:,component,jet]*efactor[...,jet,None,None];york_pair_keep(label+'_local_unit_L_partial',L,keep)
    value=P.a_dd(np.zeros((86,44)));evalue=np.zeros((86,44))
    for i in range(3):
     for j in range(3):
      coeff=P.a_mul64(measure[iq],P.a_prod(inverse[iq,:,:,i,i],inverse[iq,:,:,j,j]))
      square=P.a_mul(P.a_slice(L,(slice(None),slice(None),i,j)),P.a_slice(L,(slice(None),slice(None),i,j)))
      value=P.a_add(value,P.a_mul(coeff,square));evalue+=measure[iq]*abs(inverse[iq,:,:,i,i]*inverse[iq,:,:,j,j])*eL[:,:,i,j]**2
      york_pair_keep(label+'_diagonal_value_partial',value,keep)
    value=P.a_mul64(weight,value);key=(component,slice(di,86+di),slice(dj,44+dj));update=P.a_add(P.a_slice(out,key),value)
    out[0][key]=update[0];out[1][key]=update[1];eout[key]+=weight*evalue
    york_pair_keep(label+'_nodal_diagonal_partial',out,keep);keep(label+'_nodal_diagonal_operation_envelope_partial',eout)
 mask=york_vector_mask()
 for word in (0,1):out[word][~mask]=0
 eout[~mask]=0;york_pair_keep(label+'_nodal_diagonal',out,keep);keep(label+'_nodal_diagonal_operation_envelope',eout)
 return out,eout

def york_fresh_controls(keep):
 # New local Cartesian/cylindrical checks; no former GR/native fixture replay.
 R=1.5;Z=.5;a=.25;b=-.125
 h=np.diag((1.,1.,R**2))[None];ih=np.diag((1.,1.,1./R**2))[None];dh=np.zeros((1,3,3,3));dh[:,0,2,2]=2*R
 maps,em=york_geometry_maps(h,ih,P.a_dd(dh),keep,'fresh_york')
 rotation=P.a_dd(np.zeros((1,3,3)));rotation[0][:,2,0]=1.
 rot=york_apply_maps(rotation,maps,keep,'fresh_york_rotation')
 er=np.einsum('pkqij,pkq->pij',em,abs(rotation[0])+abs(rotation[1]));keep('fresh_york_rotation_operation_envelope',er)
 P.check('fresh_cylindrical_axial_Killing_vector',rot[0]+rot[1],np.zeros((1,3,3)),er)
 jets=P.a_dd(np.array((((a*R,a,0.),(-2*a*Z,0.,-2*a),(b*R**2,2*b*R,0.)),)))
 L=york_apply_maps(jets,maps,keep,'fresh_york_shear');target=np.diag((2*a,-4*a,2*a*R**2))[None];target[:,0,2]=target[:,2,0]=2*b*R**3
 eL=np.einsum('pkqij,pkq->pij',em,abs(jets[0])+abs(jets[1]));keep('fresh_york_shear_target',target);keep('fresh_york_shear_operation_envelope',eL)
 P.check('fresh_cylindrical_nonzero_tracefree_longitudinal_shear',L[0]+L[1],target,eL+abs(target))
 return dict(kind='fresh_axial_Killing_and_nonzero_cylindrical_shear',squared_shear_norm_exact='273/128',physical_reference_selected=False)
