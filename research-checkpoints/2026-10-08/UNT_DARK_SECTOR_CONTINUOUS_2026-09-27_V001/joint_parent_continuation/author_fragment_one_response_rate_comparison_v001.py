"""Prospective definitions only: SAME saved response operands, two derivative paths.
Caller supplies reviewed specialization200, full166+132, positive98, np/P/keep,
and authenticated current/response arrays. No load/evaluation is performed here.
The enclosing producer must hard-stop before I/O while its actual response
terminal pins are None. No feature, first-jet, inverse, old normal or fixture
producer is called: current and NEW affine66/81 operands are saved inputs.

The comparison envelope is a positive construction bound, not a new canonical
or physical residual tolerance. At fixed configuration the registered action
is degree<=2 in first jets; its nonnegative bound at E_current+E_response
contains every mixed first-variation product and each affine inhomogeneity.
Factor4 bounds the two evaluation paths conservatively. Do not divide an
implementation error by a finished tiny coefficient. Original affine/canonical
native and NEW metric admission results remain immutable external evidence.
The finite rate increment-squared remainder is outside this Frechet experiment.
"""
COMPARISON_KERNEL_AUTHOR_DRAFT=True
COMPARISON_KERNEL_AUTHORING_IN_PROGRESS=False

def rate_comparison_positive_increment(s,c,native_value,metric_value,keep,label):
 y=abs(native_value[0])+abs(native_value[1]);k=abs(metric_value[0])+abs(metric_value[1]);p=len(s['U'])
 assert y.shape==(p,99) and k.shape==(p,6)
 yu=y[:,:3];zi=y[:,3:].reshape(p,32,3).transpose(1,0,2)
 du=np.zeros((p,4,4));du[:,0]=np.einsum('paj,pj->pa',abs(c['JU']),yu)+np.einsum('pma,pm->pa',abs(c['Uh']),k)
 dz=np.zeros((32,p,4,4));dz[:,:,0,1:]=zi
 dz[:,:,0,0]=np.einsum('jpk,pk->jp',abs(c['JzU']),yu)+np.einsum('pk,jpk->jp',abs(c['Jzz']),zi)+np.einsum('jpm,pm->jp',abs(c['zh']),k)
 dg=np.zeros((p,4,4,4));dg[:,0]=np.einsum('pmab,pm->pab',abs(c['embed']),k)
 out=dict(du=du,dz=dz,dg=dg,Ga=connection_from_jet_envelope(abs(s['hi']),dg))
 for n,x in out.items():keep(label+'_'+n,x);assert np.all(np.isfinite(x)) and np.all(x>=0)
 return out

def rate_comparison_full_direction(s,c,jets,feature,moments,rate_jets,rate_feature,rate_moments,f,df_test,b,db,keep,label):
 z=lambda x:a_dd(np.zeros_like(x));p=len(s['U'])
 d={n:z(s[n]) for n in ('g','hi','U','z')};d.update(rate_jets)
 dc={n:z(c[n]) for n in ('ih','dens','sqrt_h')};dc['log_dens']=a_dd(np.zeros(p))
 df=dict(paired=rate_feature['paired'],configuration={n:z(s[n]) for n in ('uc','P','r','z2')})
 lift,test,dlift,dtest,cj,dcj=normal_contact_test_derivatives(s,c,jets,feature,d,dc,df,f,df_test,b,db,keep,label+'_full_test')
 native=combined_normal_native_contact(s,feature,test,d,df,dtest,keep,label+'_full_native')
 mode=combined_normal_z0_contact(s,jets,feature,lift,d,df,dlift,keep,label+'_full_z0')
 phase=combined_normal_absolute_phase_contact(s,c,test,d,dc,dtest,keep,label+'_full_phase')
 zero_curvature=dict(Q=a_dd(np.zeros(p)),V=a_dd(np.zeros((p,3))))
 EH=combined_normal_EH_contact(s,c,cj,moments,{},d,dc,dcj,rate_moments,zero_curvature,f,df_test,b,db,keep,label+'_full_EH')
 # dc.dens is exactly zero: the supplied primal-density term vanishes algebraically.
 components=a_stack((a_mul64(c['dens'],normal_pair_sum(native,1)),a_mul64(c['dens'],normal_pair_sum(mode,1)),a_mul64(c['dens'],normal_pair_sum(phase,1)),normal_pair_sum(EH,1)),axis=-1)
 coefficient=normal_pair_sum(components,1)
 out=dict(native_metric_terms=native,mode_compensation_terms=mode,absolute_phase_terms=phase,EH_terms=EH,component_densities=components,coefficient=coefficient)
 for n,x in out.items():normal_keep_pair(label+'_full_'+n,x,keep)
 return out

def rate_comparison_direction(s,c,jets,feature,moments,current_op,rate_jets,rate_feature,rate_moments,rate_op,rate_chart,column,f,df_test,b,db,keep,label):
 cache=rate_normal_test_cache(s,c,jets,feature,column,f,df_test,b,db,keep,label+'_cache')
 fast=rate_normal_direction(s,c,feature,moments,rate_jets,rate_feature,rate_moments,rate_chart,column,cache,keep,label+'_specialized')
 full=rate_comparison_full_direction(s,c,jets,feature,moments,rate_jets,rate_feature,rate_moments,f,df_test,b,db,keep,label)
 positive={n:current_op[n]+rate_op[n] for n in ('du','dz','dg','Ga')}
 ef=normal_positive_features(s,c,positive,keep,label+'_positive_feature')
 ecurvature=dict(envelope_Q=np.zeros(len(s['U'])),envelope_V=np.zeros((len(s['U']),3)))
 envelope=normal_positive_direction(s,c,positive,ef,ecurvature,f,df_test,b,db,keep,label+'_positive_direction')
 differences={};bounds={};norms=[]
 for n in ('native_metric_terms','mode_compensation_terms','absolute_phase_terms','EH_terms','component_densities','coefficient'):
  delta=a_sub(fast[n],full[n]);normal_keep_pair(label+'_'+n+'_specialized_minus_full',delta,keep)
  e=4*envelope[n];keep(label+'_'+n+'_implementation_envelope',e)
  differences[n]=delta;bounds[n]=e;norms.append((np.linalg.norm(delta[0]+delta[1]),np.linalg.norm(fast[n][0]+fast[n][1]),np.linalg.norm(full[n][0]+full[n][1]),np.linalg.norm(e)))
 keep(label+'_family_L2_diagnostics',np.asarray(norms))
 return fast,full,differences,bounds
