"""Definitions only: the same combined direction's initial weak-CMC contact.
The current Gamma Ktrace, compact contacts and new rate Ktrace are owned pairs.
Hbar is the fixed current EPS5 value; phase velocity has no direct K contact.
Caller supplies np, reviewed a_* and normal_keep_pair, keep(name,array).
Raw sqrt_h includes cylindrical R; scalar scatter later uses original dv/R once.
No producer, canonical solve, full rank, finite preparation or evolution claim.
"""

def combined_initial_CMC_density(sqrt_h,current_Ktrace,compact_delta_Ktrace,
 compact_delta_sqrt_h,compact_log_dens,rate_delta_Ktrace,take,Hbar,keep,label):
 p=len(sqrt_h);assert sqrt_h.shape==(p,) and np.all(sqrt_h>0)
 assert current_Ktrace[0].shape==current_Ktrace[1].shape==rate_delta_Ktrace[0].shape==rate_delta_Ktrace[1].shape==(p,)
 take=np.asarray(take);assert take.ndim==1 and len(np.unique(take))==len(take) and np.all((take>=0)&(take<p))
 for x in (compact_delta_Ktrace,compact_delta_sqrt_h,compact_log_dens):assert x[0].shape==x[1].shape==take.shape
 put=lambda n,x:normal_keep_pair(label+'_'+n,x,keep)
 gap=put('current_pointwise_initial_CMC_gap',a_sub(current_Ktrace,a_dd(np.full(p,3*Hbar))))
 compact_trace=put('compact_trace_contact_density',a_mul64(sqrt_h[take],compact_delta_Ktrace))
 compact_measure=put('compact_measure_contact_density',a_mul(compact_delta_sqrt_h,(gap[0][take],gap[1][take])))
 compact=put('compact_initial_CMC_density_contact',a_add(compact_trace,compact_measure))
 put('compact_sqrt_h_minus_4D_density_chain_contact',a_sub(compact_delta_sqrt_h,a_mul64(sqrt_h[take],compact_log_dens)))
 rate=put('global_induced_rate_initial_CMC_density_contact',a_mul64(sqrt_h,rate_delta_Ktrace))
 embedded=a_dd(np.zeros(p))
 for word in (0,1):embedded[word][take]=compact[word]
 put('embedded_compact_initial_CMC_density_contact',embedded)
 total=put('combined_initial_CMC_density_contact',a_add(embedded,rate))
 return dict(compact=embedded,rate=rate,total=total,compact_trace=compact_trace,
 compact_measure=compact_measure,current_pointwise_gap=gap,
 phase_velocity_direct_metric_CMC_contact_zero=True,Hbar_fixed=True,
 initial_CMC_only=True,full_CMC_preservation_computed=False,
 finite_configuration_prepared=False,primitive_bridge_resolved=False)
