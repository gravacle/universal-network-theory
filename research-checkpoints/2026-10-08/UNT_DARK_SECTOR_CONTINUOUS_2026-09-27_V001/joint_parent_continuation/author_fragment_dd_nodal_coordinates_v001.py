"""Definitions only: two-word values in the SAME native/metric Q1 coordinates.
ROOT supplies the accepted array DD primitives, point/scatter kernels and geometry.
No new physical DOF, coefficient, source, gauge, RHS or solver cap is registered.
"""
np=None

def dd_native_node_value(x,g,capture,jet=0):
 assert x[0].shape==x[1].shape==(33,3,87,45) and jet in (0,1,2)
 y=(lift_velocity(x[0]),lift_velocity(x[1]));out=a_dd(np.zeros((33,4,86,44,3)))
 capture('dd_native_input_nodes_hi',x[0]);capture('dd_native_input_nodes_lo',x[1])
 for iq in range(4):
  R=g['R'][iq].reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,jet];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   if jet==1:factor[...,2]+=2*R*g['hats'][iq,corner,0]
   val=(np.moveaxis(y[0][:,:,di:86+di,dj:44+dj],1,-1),np.moveaxis(y[1][:,:,di:86+di,dj:44+dj],1,-1))
   updated=a_add(a_slice(out,(slice(None),iq)),a_mul64(factor,val));out[0][:,iq]=updated[0];out[1][:,iq]=updated[1]
   capture('dd_native_current_jet%d_partial_hi'%jet,out[0]);capture('dd_native_current_jet%d_partial_lo'%jet,out[1])
 return a_reshape(out,(33,15136,3))
def dd_metric_node_value(x,g,capture,jet=0):
 assert x[0].shape==x[1].shape==(6,87,45) and jet in (0,1,2)
 y=(lift_metric(x[0]),lift_metric(x[1]));out=a_dd(np.zeros((4,86,44,6)))
 capture('dd_metric_input_nodes_hi',x[0]);capture('dd_metric_input_nodes_lo',x[1])
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,jet];factor=hat[...,None,None]*F
   if jet==1:factor+=g['hats'][iq,corner,0][...,None,None]*metric_R_matrix(R)
   val=(np.moveaxis(y[0][:,di:86+di,dj:44+dj],0,-1),np.moveaxis(y[1][:,di:86+di,dj:44+dj],0,-1))
   updated=a_add(a_slice(out,iq),a_matvec(factor,val));out[0][iq]=updated[0];out[1][iq]=updated[1]
   capture('dd_metric_current_jet%d_partial_hi'%jet,out[0]);capture('dd_metric_current_jet%d_partial_lo'%jet,out[1])
 return a_reshape(out,(15136,6))
def dd_node_original_action(x,b,d,g,capture):
 assert x[0].shape==x[1].shape==(403340,)
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False)
 vp=dd_native_node_value((vh,vl),g,capture);kp=dd_metric_node_value((kh,kl),g,capture)
 capture('dd_native_point_rate_hi',vp[0]);capture('dd_native_point_rate_lo',vp[1]);capture('dd_metric_point_rate_hi',kp[0]);capture('dd_metric_point_rate_lo',kp[1])
 n,m=dd_point_coupled(vp,kp,b,d,capture)
 nw=dd_native_scatter(n,g,capture);mw=dd_metric_scatter(m,g,capture)
 capture('dd_original_native_action_hi',nw[0]);capture('dd_original_native_action_lo',nw[1]);capture('dd_original_metric_action_hi',mw[0]);capture('dd_original_metric_action_lo',mw[1])
 return pack_dd(nw,mw)
def dd_node_update(start,delta,capture,label):
 # Exact three-word EFT sum; a disclosed third word is the compression defect.
 capture(label+'_old_nodes_hi',start[0]);capture(label+'_old_nodes_lo',start[1]);capture(label+'_float_correction',delta)
 s,e=a_sum(start[0],delta);t,f=a_sum(start[1],e);h,g=a_sum(s,t);l,q=a_sum(g,f);hi,lo=a_sum(h,l)
 capture(label+'_updated_nodes_hi',hi);capture(label+'_updated_nodes_lo',lo);capture(label+'_exact_update_minus_two_word_nodes',q)
 return (hi,lo),q

def a_div64(x,den,capture,label):
 # Division by the ORIGINAL finite denominator, no newly frozen reciprocal.
 den=np.asarray(den,dtype=np.float64);capture(label+'_denominator',den);assert np.all(np.isfinite(den)) and np.all(den!=0)
 q1=x[0]/den;capture(label+'_first_quotient',q1);r=a_sub(x,a_mul64(den,a_dd(q1)))
 capture(label+'_first_remainder_hi',r[0]);capture(label+'_first_remainder_lo',r[1])
 q2=(r[0]+r[1])/den;capture(label+'_second_quotient',q2);q=a_sum(q1,q2)
 r=a_sub(x,a_mul64(den,q));capture(label+'_second_remainder_hi',r[0]);capture(label+'_second_remainder_lo',r[1])
 q3=(r[0]+r[1])/den;capture(label+'_third_quotient',q3);q=a_add(q,a_dd(q3))
 residual=a_sub(x,a_mul64(den,q));capture(label+'_division_defect_hi',residual[0]);capture(label+'_division_defect_lo',residual[1]);capture(label+'_quotient_hi',q[0]);capture(label+'_quotient_lo',q[1])
 return q
def dd_scalar_scatter(field,g,capture,label):
 assert field[0].shape==field[1].shape==(15136,)
 f=a_reshape(field,(4,86,44));out=a_dd(np.zeros((87,45)))
 for iq in range(4):
  weighted=a_mul64((g['dv'][iq]/g['R'][iq]).reshape(86,44),a_slice(f,iq))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   val=a_mul64(g['hats'][iq,corner,0],weighted);key=(slice(di,86+di),slice(dj,44+dj));update=a_add(a_slice(out,key),val)
   out[0][key]=update[0];out[1][key]=update[1];capture(label+'_scalar_scatter_partial_hi',out[0]);capture(label+'_scalar_scatter_partial_lo',out[1])
 update=a_add(a_slice(out,(1,slice(None))),a_slice(out,(0,slice(None))));out[0][1]=update[0];out[1][1]=update[1];out[0][0]=0;out[1][0]=0
 capture(label+'_scalar_scatter_hi',out[0]);capture(label+'_scalar_scatter_lo',out[1]);return out
def dd_node_trace(x,d,g,capture,label):
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False);kp=dd_metric_node_value((kh,kl),g,capture)
 # Both entries of each symmetric offdiagonal contraction remain explicit.
 terms=[]
 for coord,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  terms.append(a_mul64(d['ih'][:,i,j],a_slice(kp,(slice(None),coord))))
  if i!=j:terms.append(a_mul64(d['ih'][:,j,i],a_slice(kp,(slice(None),coord))))
 total=a_dd(np.zeros(15136))
 for i,term in enumerate(terms):total=a_add(total,term);capture(label+'_trace_contraction_through%d_hi'%i,total[0]);capture(label+'_trace_contraction_through%d_lo'%i,total[1])
 tr=a_div64(total,2*d['N'],capture,label+'_trace_normalization');weighted=a_mul64(d['mu'],tr)
 capture(label+'_point_density_hi',weighted[0]);capture(label+'_point_density_lo',weighted[1]);return dd_scalar_scatter(weighted,g,capture,label)
def dd_node_rate_jets(x,g,capture):
 vh,kh,_=unpack_fields(x[0],False);vl,kl,_=unpack_fields(x[1],False);out={}
 for jet,axis in enumerate(('value','R','Z')):
  for name,pair,evalf in (('native',(vh,vl),dd_native_node_value),('metric',(kh,kl),dd_metric_node_value)):
   value=evalf(pair,g,capture,jet);out[name+'_jet_'+axis+'_hi']=value[0];out[name+'_jet_'+axis+'_lo']=value[1]
 return out
