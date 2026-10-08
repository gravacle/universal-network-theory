"""Definitions only: actual transpose of the registered frozen value polynomial.
Caller supplies np/P/keep. A=S Ppoint E, hence A*=E* Ppoint* S*.
Evaluation retains rounded Fhat64; scatter retains separate F64, weight64, hat64.
Serialized M0/D/T are transposed, not assumed symmetric. No inverse, native
coercivity, gauge null, physical range, literal adjoint or rank is assumed.
The caller consumes saved final nodes/action/residual and evaluates only a NEW
transpose candidate plus positive construction bounds and saved-word pairings.
"""
ACTUAL_ADJOINT_KERNEL_AUTHOR_DRAFT=True
ACTUAL_ADJOINT_KERNEL_AUTHORING_IN_PROGRESS=False

def actual_adjoint_put(label,x):
 for w,suffix in enumerate(('hi','lo')):keep(label+'_'+suffix,np.asarray(x[w]).copy())
 return x

def actual_adjoint_dot(x,y,label):
 assert x[0].shape==x[1].shape==y[0].shape==y[1].shape and x[0].ndim==1
 value=actual_adjoint_put(label+'_original_product_terms',P.a_mul(x,y))
 while len(value[0])>1:
  n=len(value[0]);m=n-n%2;out=P.a_add((value[0][:m:2],value[1][:m:2]),(value[0][1:m:2],value[1][1:m:2]))
  if n%2:out=tuple(np.concatenate((out[w],value[w][-1:])) for w in (0,1))
  value=actual_adjoint_put(label+'_current_partial',out)
 return actual_adjoint_put(label+'_value',tuple(np.asarray(v[0]).copy() for v in value))

def actual_scatter_transpose(x,g,label):
 # S*: restriction* is the original lift; reverse hat/weight/F products.
 assert x[0].shape==x[1].shape==(403340,)
 nh,mh,_=P.unpack_fields(x[0],False);nl,ml,_=P.unpack_fields(x[1],False)
 n=(P.lift_velocity(nh),P.lift_velocity(nl));m=(P.lift_metric(mh),P.lift_metric(ml))
 actual_adjoint_put(label+'_native_lift',n);actual_adjoint_put(label+'_metric_lift',m)
 no=P.a_dd(np.zeros((33,4,86,44,3)));mo=P.a_dd(np.zeros((4,86,44,6)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);weight=(g['dv'][iq]/g['R'][iq]).reshape(86,44);F=P.dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
   nv=tuple(np.moveaxis(n[w][:,:,di:86+di,dj:44+dj],1,-1) for w in (0,1))
   term=actual_adjoint_put(label+'_native_current_factor_term',P.a_mul64(factor,nv))
   term=actual_adjoint_put(label+'_native_current_weight_term',P.a_mul64(weight[...,None],term))
   out=P.a_add(P.a_slice(no,(slice(None),iq)),term);no[0][:,iq]=out[0];no[1][:,iq]=out[1];actual_adjoint_put(label+'_native_current_partial',no)
   mv=tuple(np.moveaxis(m[w][:,di:86+di,dj:44+dj],0,-1) for w in (0,1))
   term=actual_adjoint_put(label+'_metric_current_hat_term',P.a_mul64(hat[...,None],mv))
   term=actual_adjoint_put(label+'_metric_current_weight_term',P.a_mul64(weight[...,None],term))
   term=actual_adjoint_put(label+'_metric_current_F_term',P.a_matvec(F,term))
   out=P.a_add(P.a_slice(mo,iq),term);mo[0][iq]=out[0];mo[1][iq]=out[1];actual_adjoint_put(label+'_metric_current_partial',mo)
 return actual_adjoint_put(label+'_native_point',P.a_reshape(no,(33,15136,3))),actual_adjoint_put(label+'_metric_point',P.a_reshape(mo,(15136,6)))

def actual_point_transpose(v,k,b,d,label):
 p=v[0].shape[1];assert v[0].shape==v[1].shape==(33,p,3) and k[0].shape==k[1].shape==(p,6)
 u=P.a_slice(v,0);modes=[];U=actual_adjoint_put(label+'_Maxwell_transpose',P.a_matvec(b['M0'].swapaxes(-1,-2),u))
 for mode in range(32):
  mixed=actual_adjoint_put(label+'_current_mixed',P.a_add(P.a_slice(v,mode+1),P.a_matvec(b['L'][mode],u)))
  Dm=actual_adjoint_put(label+'_current_D_transpose',P.a_matvec(b['D'][mode].swapaxes(-1,-2),mixed));modes.append(Dm)
  U=actual_adjoint_put(label+'_U_current_partial',P.a_add(U,P.a_matvec(b['L'][mode].swapaxes(-1,-2),Dm)))
 native=P.a_stack([U]+modes);Bk=actual_adjoint_put(label+'_B_metric',P.a_matvec(d['B'],k))
 native=actual_adjoint_put(label+'_native',P.a_add(native,P.a_transpose(P.a_reshape(Bk,(p,33,3)),(1,0,2))))
 vf=P.a_reshape(P.a_transpose(v,(1,0,2)),(p,99))
 metric=actual_adjoint_put(label+'_metric',P.a_add(P.a_matvec(d['B'].swapaxes(-1,-2),vf),P.a_matvec(d['T'].swapaxes(-1,-2),k)))
 return native,metric

def actual_evaluation_transpose(n,m,g,label):
 # E*: rounded native factor and rounded metric Fhat64, then lift* restrictions.
 assert n[0].shape==n[1].shape==(33,15136,3) and m[0].shape==m[1].shape==(15136,6)
 nf=P.a_reshape(n,(33,4,86,44,3));mf=P.a_reshape(m,(4,86,44,6))
 no=P.a_dd(np.zeros((33,3,87,45)));mo=P.a_dd(np.zeros((6,87,45)))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=P.dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   term=P.a_transpose(P.a_mul64(factor,P.a_slice(nf,(slice(None),iq))),(0,3,1,2));actual_adjoint_put(label+'_native_current_term',term)
   key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj));out=P.a_add(P.a_slice(no,key),term);no[0][key]=out[0];no[1][key]=out[1];actual_adjoint_put(label+'_native_current_partial',no)
   Fhat=hat[...,None,None]*F;term=P.a_transpose(P.a_matvec(Fhat.swapaxes(-1,-2),P.a_slice(mf,iq)),(2,0,1));actual_adjoint_put(label+'_metric_current_Fhat_term',term)
   key=(slice(None),slice(di,86+di),slice(dj,44+dj));out=P.a_add(P.a_slice(mo,key),term);mo[0][key]=out[0];mo[1][key]=out[1];actual_adjoint_put(label+'_metric_current_partial',mo)
 # The inherited float restrict helpers round additions; retain DD sums here.
 for component in (1,2):
  out=P.a_add(P.a_slice(no,(slice(None),component,1,slice(None))),P.a_slice(no,(slice(None),component,0,slice(None))))
  no[0][:,component,1]=out[0];no[1][:,component,1]=out[1];actual_adjoint_put(label+'_native_restricted_partial',no)
 no[0][:,:,0]=0;no[1][:,:,0]=0;no[0][:,1,:,0]=0;no[1][:,1,:,0]=0
 out=P.a_add(P.a_slice(mo,(slice(None),1,slice(None))),P.a_slice(mo,(slice(None),0,slice(None))))
 mo[0][:,1]=out[0];mo[1][:,1]=out[1];mo[0][:,0]=0;mo[1][:,0]=0;mo[0][3:5,:,0]=0;mo[1][3:5,:,0]=0
 actual_adjoint_put(label+'_native_restricted',no);actual_adjoint_put(label+'_metric_restricted',mo)
 return actual_adjoint_put(label+'_packed',P.pack_dd(no,mo))

def actual_frozen_adjoint(x,b,d,g,label):
 n,m=actual_scatter_transpose(x,g,label+'_Sstar');n,m=actual_point_transpose(n,m,b,d,label+'_Pstar')
 return actual_evaluation_transpose(n,m,g,label+'_Estar')

def actual_adjoint_positive(x,b,d,g,label):
 # Independent positive contractions; safety factor2 covers bound-rounding.
 nh,mh,_=P.unpack_fields(abs(x[0])+abs(x[1]),False);n=P.lift_velocity(nh);m=P.lift_metric(mh)
 sn=np.zeros((33,4,86,44,3));sm=np.zeros((4,86,44,6))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);weight=abs((g['dv'][iq]/g['R'][iq]).reshape(86,44));F=abs(P.dd_metric_F(R))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
   sn[:,iq]+=abs(factor)*weight[...,None]*np.moveaxis(n[:,:,di:86+di,dj:44+dj],1,-1)
   val=abs(hat[...,None])*weight[...,None]*np.moveaxis(m[:,di:86+di,dj:44+dj],0,-1);sm[iq]+=np.einsum('...ab,...b->...a',F,val,optimize=True)
 sn=sn.reshape(33,15136,3);sm=sm.reshape(15136,6);keep(label+'_Sstar_native_positive',sn);keep(label+'_Sstar_metric_positive',sm)
 mixed=sn[1:]+np.einsum('jpik,pk->jpi',b['eL'],sn[0],optimize=True)
 modes=np.einsum('jpki,jpk->jpi',b['eD'],mixed,optimize=True)
 U=np.einsum('pki,pk->pi',b['eM0'],sn[0],optimize=True)+np.einsum('jpki,jpk->pi',b['eL'],modes,optimize=True)
 pn=np.concatenate((U[None],modes))+np.einsum('pia,pa->pi',d['eB'],sm,optimize=True).reshape(15136,33,3).transpose(1,0,2)
 pm=np.einsum('pia,pi->pa',d['eB'],sn.transpose(1,0,2).reshape(15136,99),optimize=True)+np.einsum('pba,pb->pa',d['eT'],sm,optimize=True)
 keep(label+'_Pstar_native_positive',pn);keep(label+'_Pstar_metric_positive',pm)
 pn=pn.reshape(33,4,86,44,3);pm=pm.reshape(4,86,44,6);no=np.zeros((33,3,87,45));mo=np.zeros((6,87,45))
 for iq in range(4):
  R=g['R'][iq].reshape(86,44);F=P.dd_metric_F(R)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=g['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]=R**2*hat
   no[:,:,di:86+di,dj:44+dj]+=np.moveaxis(abs(factor)*pn[:,iq],-1,1)
   term=np.einsum('...ab,...a->...b',abs(hat[...,None,None]*F),pm[iq],optimize=True);mo[:,di:86+di,dj:44+dj]+=np.moveaxis(term,-1,0)
 out=2*P.pack_fields(P.restrict_velocity(no),P.restrict_metric(mo));keep(label+'_packed_positive',out)
 assert out.shape==(403340,) and np.all(np.isfinite(out)) and np.all(out>=0);return out

def fresh_actual_point_adjoint_control():
 # NEW one-point full105 polynomial, independent dense transpose and low words.
 M0=np.asarray((((2.,1.,0.),(0.,3.,0.),(0.,0.,4.)),));L=np.zeros((32,1,3,3));D=np.broadcast_to(np.eye(3),(32,1,3,3)).copy()
 L[0,0]=np.asarray(((1.,2.,0.),(0.,1.,0.),(0.,0.,1.)));D[0,0]=np.asarray(((5.,1.,0.),(0.,6.,0.),(0.,0.,7.)))
 B=np.zeros((1,99,6));B[0,0,0]=3.;B[0,4,1]=1.;T=np.diag(np.arange(8.,14.))[None];T[0,0,1]=2.
 b=dict(M0=M0,L=L,D=D);d=dict(B=B,T=T);dense=np.zeros((105,105));dense[:3,:3]=M0[0]
 for j in range(32):
  sl=slice(3+3*j,6+3*j);dense[:3,:3]+=L[j,0].T@D[j,0]@L[j,0];dense[:3,sl]=L[j,0].T@D[j,0];dense[sl,:3]=D[j,0]@L[j,0];dense[sl,sl]=D[j,0]
 dense[:99,99:]=B[0];dense[99:,:99]=B[0].T;dense[99:,99:]=T[0]
 x=(np.arange(1.,106.)/128.,np.where(np.arange(105)%2==0,2.**-60,-2.**-61));v=tuple(z[:99].reshape(1,33,3).transpose(1,0,2) for z in x);k=tuple(z[99:].reshape(1,6) for z in x)
 for n,a in (('M0',M0),('L',L),('D',D),('B',B),('T',T),('independent_dense',dense)):keep('fresh_actual_adjoint_'+n,a)
 actual_adjoint_put('fresh_actual_adjoint_input',x);n,m=actual_point_transpose(v,k,b,d,'fresh_actual_adjoint_same_Pstar')
 actual=actual_adjoint_put('fresh_actual_adjoint_result',tuple(np.concatenate((n[w].transpose(1,0,2).reshape(99),m[w].reshape(6))) for w in (0,1)))
 expected=actual_adjoint_put('fresh_actual_adjoint_independent_dense_expected',P.a_matvec(dense.T,x));gap=actual_adjoint_put('fresh_actual_adjoint_dense_gap',P.a_sub(actual,expected));bound=2*abs(dense.T)@(abs(x[0])+abs(x[1]));keep('fresh_actual_adjoint_positive_bound',bound)
 P.check('NEW_nonsymmetric_full105_actual_transpose',gap[0]+gap[1],np.zeros(105),bound)
 forward=actual_adjoint_put('fresh_actual_adjoint_forward_distinction',P.a_matvec(dense,x));difference=actual_adjoint_put('fresh_actual_adjoint_transpose_minus_forward',P.a_sub(actual,forward));assert np.linalg.norm(difference[0]+difference[1])>0
 probe=P.a_dd(np.arange(105.,0.,-1.)/64.);actual_adjoint_put('fresh_actual_adjoint_pairing_probe',probe)
 left=actual_adjoint_dot(P.a_matvec(dense,probe),x,'fresh_actual_adjoint_pairing_left');right=actual_adjoint_dot(probe,actual,'fresh_actual_adjoint_pairing_right');pg=actual_adjoint_put('fresh_actual_adjoint_pairing_gap',P.a_sub(left,right))
 eb=2*(np.sum((abs(dense)@(abs(probe[0])+abs(probe[1])))*(abs(x[0])+abs(x[1])))+np.sum((abs(probe[0])+abs(probe[1]))*bound));keep('fresh_actual_adjoint_pairing_bound',np.asarray(eb))
 P.check('NEW_nonsymmetric_actual_transpose_pairing',np.asarray(pg[0]+pg[1]),np.asarray(0.),np.asarray(eb))
 return dict(kind='NEW_nonsymmetric_full105_serialized_point_transpose_control',controls=2,old_fixture_replayed=False,actual_transpose_differs_from_forward=True,global_range_or_physical_claim=False)
