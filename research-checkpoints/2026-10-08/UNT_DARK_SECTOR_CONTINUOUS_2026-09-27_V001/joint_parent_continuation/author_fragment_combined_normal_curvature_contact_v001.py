"""Definitions only: differentiated flat-reference Q/V coordinate densities.
Uses saved current C3/Q/V and uncancelled construction envelopes; no primal
curvature or connection reconstruction. Current spatial metric jets, supplied
metric contact jets/inverse contact and density fraction retain both words.
The cylindrical reference R/barGamma and current scalar test are fixed.
Caller supplies np, a_*, normal_pair_sum/keep and admitted DD divide helpers.
Curvature densities already include cylindrical R: scatter with dv/R once.
This is a first configuration contact, not a finite constraint preparation.
"""

def combined_curvature_contact(s,c,cj,curvature,dc,dcj,envelopes,keep,label):
 I=c['ih'];I1=dc['ih'];dh=a_slice(cj['dh'],(slice(None),slice(1,None),slice(None),slice(None)))
 dh1=a_slice(dcj['dh'],(slice(None),slice(1,None),slice(None),slice(None)));p=len(I)
 dG=a_dd(np.zeros((p,3,3,3)));eG=np.zeros((p,3,3,3))
 eI=abs(I);eI1=envelopes['delta_ih'];edh=envelopes['dh'];edh1=envelopes['delta_dh'];elog=envelopes['log_dens']
 assert eI1.shape==(p,3,3) and edh.shape==edh1.shape==(p,3,3,3) and elog.shape==(p,)
 for i in range(3):
  for j in range(3):
   cyclic=a_sub(a_add(a_slice(dh,(slice(None),i,j,slice(None))),a_slice(dh,(slice(None),j,i,slice(None)))),a_slice(dh,(slice(None),slice(None),i,j)))
   cyclic1=a_sub(a_add(a_slice(dh1,(slice(None),i,j,slice(None))),a_slice(dh1,(slice(None),j,i,slice(None)))),a_slice(dh1,(slice(None),slice(None),i,j)))
   value=a_dd(np.zeros((p,3)))
   for m in range(3):
    x=a_slice(cyclic,(slice(None),m));x1=a_slice(cyclic1,(slice(None),m))
    value=a_add(value,a_add(a_mul(a_slice(I1,(slice(None),slice(None),m)),(x[0][:,None],x[1][:,None])),a_mul64(I[:,:,m],(x1[0][:,None],x1[1][:,None]))))
   value=a_mul64(.5,value);dG[0][:,:,i,j]=value[0];dG[1][:,:,i,j]=value[1]
   ecyc=edh[:,i,j]+edh[:,j,i]+edh[:,:,i,j];ecyc1=edh1[:,i,j]+edh1[:,j,i]+edh1[:,:,i,j]
   eG[:,:,i,j]=.5*(np.einsum('plm,pm->pl',eI1,ecyc)+np.einsum('plm,pm->pl',eI,ecyc1))
   normal_keep_pair(label+'_delta_Gamma3_partial',dG,keep);keep(label+'_delta_Gamma3_envelope_partial',eG)
 C3=curvature['C3'];ec=curvature['envelope_C3'];mu=c['sqrt_h'];log=dc['log_dens']
 q=a_dd(np.zeros(p));v=a_dd(np.zeros((p,3)));eq=np.zeros(p);ev=np.zeros((p,3))
 # Each original cubic product receives all three contacts, with original signs.
 for i in range(3):
  for j in range(3):
   for k in range(3):
    for l in range(3):
     for sign,a,b in ((1.,(k,i,l),(l,j,k)),(-1.,(k,i,j),(l,k,l))):
      ca=C3[:,a[0],a[1],a[2]];cb=C3[:,b[0],b[1],b[2]]
      da=a_slice(dG,(slice(None),a[0],a[1],a[2]));db=a_slice(dG,(slice(None),b[0],b[1],b[2]))
      term=a_add(a_mul(a_prod(ca,cb),a_slice(I1,(slice(None),i,j))),a_mul64(I[:,i,j],a_add(a_mul64(cb,da),a_mul64(ca,db))))
      q=a_add(q,a_mul64(sign,term))
      ea=ec[:,a[0],a[1],a[2]];eb=ec[:,b[0],b[1],b[2]];eda=eG[:,a[0],a[1],a[2]];edb=eG[:,b[0],b[1],b[2]]
      eq+=eI1[:,i,j]*ea*eb+eI[:,i,j]*(eda*eb+ea*edb)
    for sign,ii,jj,a in ((1.,i,j,(k,i,j)),(-1.,i,k,(j,i,j))):
     ca=C3[:,a[0],a[1],a[2]];da=a_slice(dG,(slice(None),a[0],a[1],a[2]))
     term=a_mul64(sign,a_add(a_mul64(ca,a_slice(I1,(slice(None),ii,jj))),a_mul64(I[:,ii,jj],da)))
     update=a_add(a_slice(v,(slice(None),k)),term);v[0][:,k]=update[0];v[1][:,k]=update[1]
     ev[:,k]+=eI1[:,ii,jj]*ec[:,a[0],a[1],a[2]]+eI[:,ii,jj]*eG[:,a[0],a[1],a[2]]
   normal_keep_pair(label+'_delta_Q_polynomial_partial',q,keep);normal_keep_pair(label+'_delta_V_polynomial_partial',v,keep)
 q=a_add(a_mul64(mu,q),a_mul64(curvature['Q'],log));v=a_add(a_mul64(mu[:,None],v),a_mul64(curvature['V'],(log[0][:,None],log[1][:,None])))
 eq=mu*eq+elog*curvature['envelope_Q'];ev=mu[:,None]*ev+elog[:,None]*curvature['envelope_V']
 for name,x in (('Gamma3',dG),('Q',q),('V',v)):normal_keep_pair(label+'_delta_'+name,x,keep)
 for name,x in (('Gamma3',eG),('Q',eq),('V',ev)):keep(label+'_delta_'+name+'_operation_envelope',x)
 return dict(Gamma3=dG,Q=q,V=v,envelope_Gamma3=eG,envelope_Q=eq,envelope_V=ev,base_reference_connection_fixed=True)

def combined_mean_lapse_contact(Q,radiation_contravariant_stress_density,keep,label):
 # D_B and the antipodal momentum row are fixed; the mean dust contact is zero.
 # This differentiates the earned canonical angular stress representative.
 assert Q[0].shape==Q[1].shape==radiation_contravariant_stress_density.shape
 value=a_mul64(radiation_contravariant_stress_density,Q)
 value=normal_pair_sum(normal_pair_sum(value,2),1);value=a_mul64(-.5,value)
 normal_keep_pair(label+'_once_counted_radiation_lapse_density_contact',value,keep)
 keep(label+'_fixed_dust_lapse_density_contact',np.zeros(value[0].shape));keep(label+'_fixed_antipodal_mean_momentum_contact',np.zeros(value[0].shape+(3,)))
 return value
