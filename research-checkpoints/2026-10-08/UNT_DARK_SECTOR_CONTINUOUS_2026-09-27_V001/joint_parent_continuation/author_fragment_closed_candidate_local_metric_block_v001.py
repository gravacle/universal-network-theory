"""HELD six NEW local physical metric-rate columns at closed STATE0 support.
Globals np,P,Fraction,fy_* and exact reviewed193 ms_* definitions.
Expected EH entries use independent exact rational raw coefficients only.
Point columns are not six global nodal arguments or an inverse/rank proof.
"""
LOCAL_METRIC_BLOCK_AUTHOR_DRAFT=True
LOCAL_METRIC_BLOCK_AUTHORING_IN_PROGRESS=False

def mt_inputs(section,keep,label):
 q=len(section['R']);arguments=[]
 for column in range(6):
  v=P.a_dd(np.zeros((q,99)));k=P.a_dd(np.zeros((q,6)));k[0][:,column]=1.
  ms_keep(label+'_column%d_native_zero'%column,v,keep);ms_keep(label+'_column%d_physical_metric'%column,k,keep);arguments.append(dict(native=v,metric=k))
 native=P.a_dd(np.zeros((33,3,87,45)));metric=P.a_dd(np.zeros((6,87,45)))
 for mode,component,a in ((0,0,.5),(1,1,-.25),(17,2,2.**-12)):native[0][mode,component,43,22]=a;native[1][mode,component,43,22]=a*2.**-60
 for slot,a in enumerate((.25,2.**-9,-2.**-12,2.**-11,2.**-13,-.5)):metric[0][slot,43,22]=a;metric[1][slot,43,22]=-a*2.**-60
 assert all(np.all(a[~np.broadcast_to(P.native_mask(),a.shape)]==0) for a in native) and all(np.all(a[~P.metric_mask()]==0) for a in metric)
 test=dict(native=ms_keep(label+'_NEW_fixed_native_nodal_test',native,keep),metric=ms_keep(label+'_NEW_fixed_metric_nodal_test',metric,keep))
 return arguments,test,ms_direct_polynomial(test,section,keep,label+'_independent_test')

def mt_eh_fraction_reference(candidate,keep,label):
 c,s=candidate['c'],candidate['s'];I=c['ih'];q=len(I);assert np.array_equal(I,I.swapaxes(-1,-2)) and np.all(c['N']>0) and np.all(c['sqrt_h']>0) and np.all(s['hi'][:,0,0]<0)
 slots=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2));expected=P.a_dd(np.zeros((q,6,6)));bound=np.zeros((q,6,6));rational=[];F=lambda a:Fraction.from_float(float(a))
 for p in range(q):
  A=[[F(I[p,i,j]) for j in range(3)] for i in range(3)];alpha=-F(c['sqrt_h'][p])*F(c['N'][p])*F(s['hi'][p,0,0])/(4*F(P.C));assert alpha>0
  for a,(i,j) in enumerate(slots):
   for b,(k,l) in enumerate(slots):
    if i==j and k==l:terms=(A[i][k]**2,-A[i][i]*A[k][k])
    elif i==j:terms=(2*A[i][k]*A[i][l],-2*A[i][i]*A[k][l])
    elif k==l:terms=(2*A[i][k]*A[j][k],-2*A[i][j]*A[k][k])
    else:terms=(2*A[i][k]*A[j][l],2*A[i][l]*A[j][k],-4*A[i][j]*A[k][l])
    exact=alpha*sum(terms);h=float(exact);lo=float(exact-F(h));remainder=exact-F(h)-F(lo);expected[0][p,a,b]=h;expected[1][p,a,b]=lo;bound[p,a,b]=float(abs(alpha)*sum(abs(t) for t in terms))
    rational.append(dict(point=p,row=a,column=b,numerator=str(exact.numerator),denominator=str(exact.denominator),pair_conversion_remainder_numerator=str(remainder.numerator),pair_conversion_remainder_denominator=str(remainder.denominator)))
 ms_keep(label+'_independent_EH_table',expected,keep);keep(label+'_independent_EH_uncancelled_envelope',bound)
 return expected,bound,rational

def mt_eh_column_control(action,envelope,column,expected,bound,keep,label,check):
 actual=action['point']['metric_EH'];target=tuple(a[:,:,column] for a in expected);tensor=action['contact']['delta_momenta']['metric_EH_tensor']
 ms_keep(label+'_EH_tensor_asymmetry',P.a_sub(tensor,(tensor[0].swapaxes(-1,-2),tensor[1].swapaxes(-1,-2))),keep)
 summed=P.a_stack([P.a_slice(tensor,(slice(None),i,j)) if i==j else P.a_add(P.a_slice(tensor,(slice(None),i,j)),P.a_slice(tensor,(slice(None),j,i))) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1)
 ms_keep(label+'_EH_registered_2upper_minus_two_sided_covector',P.a_sub(actual,summed),keep)
 ms_keep(label+'_independent_expected',target,keep);gap=ms_keep(label+'_actual_minus_independent_EH',P.a_sub(actual,target),keep);e=envelope['metric_EH']+bound[:,:,column];keep(label+'_positive_EH_comparison_envelope',e)
 check(label+'_independent_closed_form_EH_column',gap[0]+gap[1],np.zeros_like(e),e)

def mt_block_readout(candidate,results,expected,keep,label):
 matrices={};envelopes={};descriptive={}
 for n,key in (('native','native'),('metric_native','metric_native'),('metric_EH','metric_EH'),('metric_total','metric')):
  M=ms_keep(label+'_'+n+'_point_response_matrix',P.a_stack([r['point'][n] for r in results],-1),keep);matrices[n]=M
  E=np.stack([r['point_envelope'][key] for r in results],-1);envelopes[n]=E;keep(label+'_'+n+'_point_operation_envelope',E)
  if n!='native':
   skew=ms_keep(label+'_'+n+'_signed_skew',P.a_sub(M,(M[0].swapaxes(-1,-2),M[1].swapaxes(-1,-2))),keep);e=E+E.swapaxes(-1,-2);keep(label+'_'+n+'_skew_envelope',e);abs_skew=abs(skew[0]+skew[1]);ratio=np.zeros_like(e);np.divide(abs_skew,e,out=ratio,where=e>0)
   keep(label+'_'+n+'_descriptive_normalized_skew',ratio);descriptive[n]=dict(maximum_normalized_skew=float(np.max(ratio)),zero_envelope_nonzero_gap=bool(np.any(abs_skew[e==0]!=0)),symmetry_gate_applied=False)
 h=candidate['c']['h'];trace_vector=P.a_dd(np.stack([h[:,i,j] for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1));ms_keep(label+'_fixed_raw_h_trace_test_vector',trace_vector,keep)
 for n in ('metric_native','metric_EH','metric_total'):
  energy=ms_keep(label+'_'+n+'_trace_quadratic',fy_sum(P.a_mul(trace_vector,fy_mv(matrices[n],trace_vector)),1),keep);e=np.einsum('pi,pij,pj->p',abs(trace_vector[0]),envelopes[n],abs(trace_vector[0]));keep(label+'_'+n+'_trace_quadratic_envelope',e)
  descriptive[n]['trace_signed_values']=(energy[0]+energy[1]).tolist()
 ms_keep(label+'_independent_EH_trace_quadratic',fy_sum(P.a_mul(trace_vector,fy_mv(expected,trace_vector)),1),keep)
 return dict(metric_block_descriptors=descriptive,native_from_metric_measured=True,reciprocal_metric_from_all99_native_columns_measured=False,trace_test_is_arithmetic_contraction_not_conformal_time_adoption=True,local_physical_columns_are_global_nodal_responses=False,global_rank_or_Schur_inverse_earned=False,physical_adoption=False)
