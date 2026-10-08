"""Definitions only: compact fixed-rate weak trace contact; no invocation.
Caller supplies np, reviewed a_*/normal_pair_* helpers and keep(name,array).
Both words of current mechanical metric rate, Gamma and contact are retained.
The density is the existing sqrt_h scalar-test density, with no new scatter.
Gamma/ADM compatibility and its differentiated gap remain diagnostics.
No global induced-rate solve, pointwise CMC adoption or physical port choice.
"""

def compact_trace_pair_contract(A,B):
 return normal_pair_sum(normal_pair_sum(a_mul(A,B),2),1)

def compact_trace_symmetric_rate(k):
 p=k[0].shape[0];assert k[0].shape==k[1].shape==(p,6)
 out=a_dd(np.zeros((p,3,3)))
 for i,(a,b) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for word in range(2):out[word][:,a,b]=out[word][:,b,a]=k[word][:,i]
 return out

def compact_metric_weak_trace_contact(s,c,jets,metric_rate,d,dc,aux,Hbar,keep,label):
 # metric_rate is the paired current physical six-coordinate rate F k.
 # The configuration partial holds that rate and independent N/beta jets.
 put=lambda n,x:normal_keep_pair(label+'_'+n,x,keep)
 p=len(s['U']);Q,Qa=aux['Q'],aux['Q_jet'];cj=aux['background_chart_jets']
 assert Q.shape==(p,3,3) and Qa.shape==(p,4,3,3)
 N,h,ih,beta,mu=c['N'],c['h'],c['ih'],c['beta'],c['sqrt_h']
 krate=put('current_metric_rate_tensor',compact_trace_symmetric_rate(metric_rate))
 put('firstjet_minus_mechanical_rate',a_sub(a_slice(jets['dg'],(slice(None),0,slice(1,None),slice(1,None))),krate))
 lie=a_dd(np.zeros((p,3,3)));dlie=a_dd(np.zeros((p,3,3)))
 for i in range(3):
  lie=a_add(lie,a_mul64(beta[:,i,None,None],a_slice(cj['dh'],(slice(None),i+1,slice(None),slice(None)))))
  dlie=a_add(dlie,a_mul64(beta[:,i,None,None],a_dd(Qa[:,i+1])))
  for a in range(3):
   for b in range(3):
    ba=a_slice(cj['dbeta'],(slice(None),a+1,i));bb=a_slice(cj['dbeta'],(slice(None),b+1,i))
    lv=a_add(a_mul64(h[:,i,b],ba),a_mul64(h[:,a,i],bb))
    dv=a_add(a_mul64(Q[:,i,b],ba),a_mul64(Q[:,a,i],bb))
    lv=a_add(a_slice(lie,(slice(None),a,b)),lv);dv=a_add(a_slice(dlie,(slice(None),a,b)),dv)
    for word in range(2):lie[word][:,a,b]=lv[word];dlie[word][:,a,b]=dv[word]
  put('Lie_beta_h_partial',lie);put('delta_Lie_beta_h_partial',dlie)
 put('Lie_beta_h',lie);put('delta_Lie_beta_h',dlie)
 Kg=put('K_Gamma',a_mul64(N[:,None,None],a_slice(jets['Ga'],(slice(None),0,slice(1,None),slice(1,None)))))
 dKg=put('delta_K_Gamma',a_mul64(N[:,None,None],a_slice(d['Ga'],(slice(None),0,slice(1,None),slice(1,None)))))
 Ka=put('K_ADM',a_div64(a_sub(krate,lie),2*N[:,None,None],keep,label+'_K_ADM_division'))
 dKa=put('delta_K_ADM',a_div64((-dlie[0],-dlie[1]),2*N[:,None,None],keep,label+'_delta_K_ADM_division'))
 lm=dc['log_dens'];dmu=put('delta_sqrt_h',dc['sqrt_h'])
 put('delta_density_chain_gap',a_sub(dmu,a_mul64(mu,lm)))
 reference_mu=a_div64(a_dd(c['dens']),N,keep,label+'_native_density_reference_division')
 put('sqrt_h_minus_native_density_reference',a_sub(a_dd(mu),reference_mu))
 out={}
 for name,K,dK in (('Gamma',Kg,dKg),('ADM',Ka,dKa)):
  trace=put(name+'_trace',compact_trace_pair_contract(a_dd(ih),K))
  gap=put(name+'_pointwise_CMC_gap',a_sub(trace,a_dd(np.full(p,3*Hbar))))
  dt=put(name+'_delta_trace',a_add(compact_trace_pair_contract(dc['ih'],K),compact_trace_pair_contract(a_dd(ih),dK)))
  density=put(name+'_weak_trace_density',a_mul64(mu,gap))
  delta_density=put(name+'_delta_weak_trace_density',a_add(a_mul64(mu,dt),a_mul(dmu,gap)))
  out[name]=dict(K=K,delta_K=dK,trace=trace,pointwise_CMC_gap=gap,delta_trace=dt,density=density,delta_density=delta_density)
 put('K_Gamma_minus_ADM',a_sub(Kg,Ka));put('delta_K_Gamma_minus_ADM',a_sub(dKg,dKa))
 put('weak_trace_density_gap',a_sub(out['Gamma']['density'],out['ADM']['density']))
 put('delta_weak_trace_density_gap',a_sub(out['Gamma']['delta_density'],out['ADM']['delta_density']))
 return dict(Gamma=out['Gamma'],ADM=out['ADM'],configuration_partial_only=True,global_induced_rate_computed=False,pointwise_CMC_adopted=False)
