"""Definitions-only global DD adapter. ROOT injects np and admits saved operands.
No runner, input loading, recurrence, cap, state adoption or physical assumption.
The scalar selected component must PASS before any owner executes this adapter.
"""
np=None
DD_ARRAY_CURRENT={}

def a_keep(name,**arrays):
 # Retain references to newly created arrays; caller snapshots on refusal.
 DD_ARRAY_CURRENT.clear();DD_ARRAY_CURRENT.update(operation=name,arrays=arrays)
 for a in arrays.values():assert a.dtype==np.float64 and np.all(np.isfinite(a)),name
def a_sum(x,y):
 x=np.asarray(x,dtype=np.float64);y=np.asarray(y,dtype=np.float64);a_keep('two_sum_inputs',x=x,y=y)
 s=x+y;a_keep('two_sum_sum',x=x,y=y,s=s)
 bb=s-x;a_keep('two_sum_split',x=x,y=y,s=s,bb=bb)
 e=(x-(s-bb))+(y-bb);a_keep('two_sum_result',s=s,e=e);return s,e
def a_split(x):
 x=np.asarray(x,dtype=np.float64);a_keep('split_input',x=x)
 assert np.all((x==0)|((abs(x)>=2.**-450)&(abs(x)<=2.**450))),'Dekker safe high/low operand domain'
 c=(2.**27+1.)*x;a_keep('split_product',x=x,c=c)
 h=c-(c-x);l=x-h;a_keep('split_result',h=h,l=l);return h,l
def a_prod(x,y):
 x=np.asarray(x,dtype=np.float64);y=np.asarray(y,dtype=np.float64);a_keep('two_prod_inputs',x=x,y=y)
 xh,xl=a_split(x);yh,yl=a_split(y);p=x*y;a_keep('two_prod_product',x=x,y=y,p=p)
 t0=xh*yh-p;a_keep('two_prod_t0',p=p,t0=t0)
 t1=t0+xh*yl;a_keep('two_prod_t1',p=p,t1=t1)
 t2=t1+xl*yh;a_keep('two_prod_t2',p=p,t2=t2)
 e=t2+xl*yl;a_keep('two_prod_result',p=p,e=e);return p,e
def a_dd(x):
 x=np.asarray(x,dtype=np.float64);return x,np.zeros_like(x)
def a_add(x,y):
 s,e=a_sum(x[0],y[0]);t,f=a_sum(x[1],y[1]);u,v=a_sum(e,t)
 h,w=a_sum(s,u);l0,l1=a_sum(w,v);l2,l3=a_sum(l0,f)
 tail0,tail1=a_sum(l1,l3);low0,low1=a_sum(l2,tail0)
 return a_sum(h,low0+(low1+tail1))
def a_sub(x,y):return a_add(x,(-y[0],-y[1]))
def a_mul(x,y):
 out=a_prod(x[0],y[0]);out=a_add(out,a_prod(x[0],y[1]))
 out=a_add(out,a_prod(x[1],y[0]));return a_add(out,a_prod(x[1],y[1]))
def a_mul64(x,y):return a_add(a_prod(x,y[0]),a_prod(x,y[1]))
def a_matvec(A,x):
 # A is a retained binary64 coefficient block; no rounded new coefficient matrix.
 assert A.shape[-1]==x[0].shape[-1] and x[0].shape==x[1].shape
 shape=np.broadcast_shapes(A.shape[:-2],x[0].shape[:-1])+(A.shape[-2],)
 out=a_dd(np.zeros(shape))
 for j in range(A.shape[-1]):out=a_add(out,a_mul64(A[...,j],(x[0][...,j,None],x[1][...,j,None])))
 return out
def a_stack(pairs,axis=0):return np.stack([x[0] for x in pairs],axis=axis),np.stack([x[1] for x in pairs],axis=axis)
def a_slice(pair,key):return pair[0][key],pair[1][key]
def a_reshape(pair,shape):return pair[0].reshape(shape),pair[1].reshape(shape)
def a_transpose(pair,axes):return pair[0].transpose(axes),pair[1].transpose(axes)

def dd_native_value(x,g,capture):
 # Only original binary64 nodal coefficients are candidates, never hidden DD nodes.
 assert x.shape==(33,3,87,45);y=x.copy();y[:,0,0,:]=0;y[:,1,0,:]=y[:,1,1,:];y[:,1,:,0]=0;y[:,2,0,:]=y[:,2,1,:]
 out=a_dd(np.zeros((33,4,86,44,3)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   val=np.moveaxis(y[:,:,di:86+di,dj:44+dj],1,-1)
   updated=a_add(a_slice(out,(slice(None),iq)),a_prod(val,factor))
   out[0][:,iq]=updated[0];out[1][:,iq]=updated[1]
   capture("native_evaluation_current_partial_hi",out[0]);capture("native_evaluation_current_partial_lo",out[1])
 return a_reshape(out,(33,15136,3))
def dd_metric_F(R):
 F=np.zeros(R.shape+(6,6));F[...,0,0]=1;F[...,0,1]=R**2;F[...,1,5]=1;F[...,2,0]=R**2;F[...,3,3]=R;F[...,4,2]=R**3;F[...,5,4]=R**2
 return F
def dd_metric_value(x,g,capture):
 assert x.shape==(6,87,45);y=x.copy();y[:,0,:]=y[:,1,:];y[3:5,:,0]=0
 out=a_dd(np.zeros((4,86,44,6)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=F*hat[...,None,None]
   exact_factor=a_prod(F,hat[...,None,None]);geometry_defect=a_sub(a_dd(factor),exact_factor)
   capture('geometry_Fhat64_minus_exact_product_q%d_corner%d_hi'%(iq,corner),geometry_defect[0])
   capture('geometry_Fhat64_minus_exact_product_q%d_corner%d_lo'%(iq,corner),geometry_defect[1])
   val=np.moveaxis(y[:,di:86+di,dj:44+dj],0,-1)
   updated=a_add(a_slice(out,iq),a_matvec(factor,a_dd(val)))
   out[0][iq]=updated[0];out[1][iq]=updated[1]
   capture("metric_evaluation_current_partial_hi",out[0]);capture("metric_evaluation_current_partial_lo",out[1])
 return a_reshape(out,(15136,6))
def dd_point_coupled(v,k,b,d,capture):
 # Parent order: M0vU + sum L^T[D(z+LvU)] + Bu k, mode D(z+LvU)+Bz k.
 p=v[0].shape[1];assert v[0].shape==v[1].shape==(33,p,3) and k[0].shape==k[1].shape==(p,6)
 u=a_slice(v,0);modes=[];U=a_matvec(b['M0'],u)
 capture('point_Maxwell_U_hi',U[0]);capture('point_Maxwell_U_lo',U[1])
 for mode in range(32):
  mixed=a_add(a_slice(v,mode+1),a_matvec(b['L'][mode],u))
  capture('point_mode%d_mixed_hi'%mode,mixed[0]);capture('point_mode%d_mixed_lo'%mode,mixed[1])
  Dm=a_matvec(b['D'][mode],mixed)
  capture('point_mode%d_Dmixed_hi'%mode,Dm[0]);capture('point_mode%d_Dmixed_lo'%mode,Dm[1])
  modes.append(Dm);U=a_add(U,a_matvec(b['L'][mode].swapaxes(-1,-2),Dm))
  capture('point_U_through_mode%d_hi'%mode,U[0]);capture('point_U_through_mode%d_lo'%mode,U[1])
 native=a_stack([U]+modes);Bv=a_matvec(d['B'],k)
 native=a_add(native,a_transpose(a_reshape(Bv,(p,33,3)),(1,0,2)))
 vf=a_reshape(a_transpose(v,(1,0,2)),(p,99))
 metric=a_add(a_matvec(d['B'].swapaxes(-1,-2),vf),a_matvec(d['T'],k))
 capture('point_native_action_hi',native[0]);capture('point_native_action_lo',native[1])
 capture('point_metric_action_hi',metric[0]);capture('point_metric_action_lo',metric[1])
 return native,metric

def dd_native_scatter(field,g,capture):
 assert field[0].shape==field[1].shape==(33,15136,3)
 f=a_reshape(field,(33,4,86,44,3));out=a_dd(np.zeros((33,3,87,45)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  weighted=a_mul64(weight[...,None],a_slice(f,(slice(None),iq)))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
   val=a_transpose(a_mul64(factor,weighted),(0,3,1,2));key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj))
   update=a_add(a_slice(out,key),val);out[0][key]=update[0];out[1][key]=update[1]
   capture("scatter_current_partial_hi",out[0]);capture("scatter_current_partial_lo",out[1])
 for component in (1,2):
  update=a_add(a_slice(out,(slice(None),component,1,slice(None))),a_slice(out,(slice(None),component,0,slice(None))))
  out[0][:,component,1]=update[0];out[1][:,component,1]=update[1]
  capture("native_scatter_current_restricted_hi",out[0]);capture("native_scatter_current_restricted_lo",out[1])
 out[0][:,:,0]=0;out[1][:,:,0]=0;out[0][:,1,:,0]=0;out[1][:,1,:,0]=0
 return out
def dd_metric_scatter(field,g,capture):
 # Original scatter F64 contraction, then weight64 and hat64 separately.
 assert field[0].shape==field[1].shape==(15136,6)
 f=a_reshape(field,(4,86,44,6));out=a_dd(np.zeros((6,87,45)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=dd_metric_F(R);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44)
  FTf=a_matvec(F.swapaxes(-1,-2),a_slice(f,iq));weighted=a_mul64(weight[...,None],FTf)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   value=a_mul64(g['hats'][iq,corner,0][...,None],weighted);val=a_transpose(value,(2,0,1));key=(slice(None),slice(di,86+di),slice(dj,44+dj))
   update=a_add(a_slice(out,key),val);out[0][key]=update[0];out[1][key]=update[1]
   capture("scatter_current_partial_hi",out[0]);capture("scatter_current_partial_lo",out[1])
 update=a_add(a_slice(out,(slice(None),1,slice(None))),a_slice(out,(slice(None),0,slice(None))))
 out[0][:,1]=update[0];out[1][:,1]=update[1];capture("metric_scatter_current_restricted_hi",out[0]);capture("metric_scatter_current_restricted_lo",out[1]);out[0][:,0]=0;out[1][:,0]=0;out[0][3:5,:,0]=0;out[1][3:5,:,0]=0
 return out
def global_coupled_action_dd(v,k,b,d,g,capture):
 vp=dd_native_value(v,g,capture);capture('native_point_rate_hi',vp[0]);capture('native_point_rate_lo',vp[1])
 kp=dd_metric_value(k,g,capture);capture('metric_point_rate_hi',kp[0]);capture('metric_point_rate_lo',kp[1])
 npnt,mpnt=dd_point_coupled(vp,kp,b,d,capture)
 n=dd_native_scatter(npnt,g,capture);capture('native_weak_action_hi',n[0]);capture('native_weak_action_lo',n[1])
 m=dd_metric_scatter(mpnt,g,capture);capture('metric_weak_action_hi',m[0]);capture('metric_weak_action_lo',m[1])
 return n,m
def original_residual_dd(rhs,action):return a_sub(a_dd(rhs),action)
def rounded_node_update(base,delta,capture,label):
 # Original binary64 candidate is the high word; the low word is a disclosed defect.
 high,low=a_sum(base,delta);capture(label+'_actual_binary64_nodes',high);capture(label+'_exact_update_minus_actual_nodes',low)
 return high,low
def shifted_residual_with_update_defect(base_residual,delta_action,node_rounding_action):
 # A(x_actual)=A(xbase)+A(delta)-A(exact_update_minus_actual_nodes).
 return a_add(a_sub(base_residual,delta_action),node_rounding_action)
