# Definitions only. np and the admitted paired arithmetic P are supplied by caller.
# Consumes saved total canonical metric density; no primitive/FE/momentum replay.
def york_point_keep(name,x,keep):
 keep(name+'_hi',x[0]);keep(name+'_lo',x[1]);return x

def york_point_tensor(local,keep,label):
 assert local[0].shape==local[1].shape==(3784,6)
 out=P.a_dd(np.zeros((3784,3,3)))
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  value=P.a_mul64(1. if i==j else .5,P.a_slice(local,(slice(None),slot)))
  for word in (0,1):out[word][:,i,j]=out[word][:,j,i]=value[word]
  york_point_keep(label+'_tensor_partial',out,keep)
 return out

def york_point_trace(h,tensor,keep,label):
 out=P.a_dd(np.zeros(3784))
 for i in range(3):
  for j in range(3):
   out=P.a_add(out,P.a_mul64(h[:,i,j],P.a_slice(tensor,(slice(None),i,j))))
   york_point_keep(label+'_trace_partial',out,keep)
 return out

def york_point_split(local,h,ih,sqrt_h,keep,label):
 assert h.shape==ih.shape==(3784,3,3) and sqrt_h.shape==(3784,)
 assert np.all(np.isfinite(h)) and np.all(np.isfinite(ih)) and np.all(np.isfinite(sqrt_h)) and np.all(sqrt_h>0)
 assert np.all(h==h.transpose(0,2,1)) and np.all(ih==ih.transpose(0,2,1))
 tensor=york_point_tensor(local,keep,label);york_point_keep(label+'_total_canonical_tensor_density',tensor,keep)
 tau=york_point_trace(h,tensor,keep,label+'_total');york_point_keep(label+'_total_canonical_trace_density',tau,keep)
 tau_third=P.a_div64(tau,3.,keep,label+'_trace_division');york_point_keep(label+'_one_third_trace_density',tau_third,keep)
 isotropic=P.a_mul64(ih,(tau_third[0][:,None,None],tau_third[1][:,None,None]));york_point_keep(label+'_isotropic_canonical_density',isotropic,keep)
 tf=P.a_sub(tensor,isotropic);york_point_keep(label+'_trace_subtracted_canonical_density',tf,keep)
 reconstructed=P.a_add(tf,isotropic);york_point_keep(label+'_reconstructed_total_density',reconstructed,keep)
 reconstruction_gap=P.a_sub(reconstructed,tensor);york_point_keep(label+'_reconstruction_gap',reconstruction_gap,keep)
 inverse_trace=york_point_trace(h,P.a_dd(ih),keep,label+'_stored_inverse');york_point_keep(label+'_h_contract_stored_ih',inverse_trace,keep)
 inverse_trace_gap=P.a_sub(inverse_trace,P.a_dd(np.full(3784,3.)));york_point_keep(label+'_stored_inverse_trace_gap',inverse_trace_gap,keep)
 actual_tf_trace=york_point_trace(h,tf,keep,label+'_trace_subtracted');york_point_keep(label+'_actual_trace_subtracted_trace',actual_tf_trace,keep)
 predicted_tf_trace=P.a_sub(tau,P.a_mul(tau_third,inverse_trace));york_point_keep(label+'_predicted_trace_from_stored_inverse_gap',predicted_tf_trace,keep)
 trace_gap=P.a_sub(actual_tf_trace,predicted_tf_trace);york_point_keep(label+'_trace_gap_identity',trace_gap,keep)
 # Positive operation bounds precede every trace and subtraction cancellation.
 et=abs(tensor[0])+abs(tensor[1]);e_tau=np.einsum('pij,pij->p',abs(h),et)
 e_inv=np.einsum('pij,pij->p',abs(h),abs(ih));e_iso=abs(ih)*(e_tau/3.)[:,None,None]
 e_tf=et+e_iso;e_reconstruction=e_tf+e_iso+et
 e_trace=np.einsum('pij,pij->p',abs(h),e_tf)+e_tau+(e_tau/3.)*e_inv
 keep(label+'_reconstruction_operation_envelope',e_reconstruction);keep(label+'_trace_identity_operation_envelope',e_trace)
 return dict(total=tensor,tau=tau,isotropic=isotropic,trace_subtracted=tf,
  reconstruction_gap=reconstruction_gap,actual_tf_trace=actual_tf_trace,predicted_tf_trace=predicted_tf_trace,
  stored_inverse_trace=inverse_trace,stored_inverse_trace_gap=inverse_trace_gap,trace_identity_gap=trace_gap,
  reconstruction_envelope=e_reconstruction,trace_identity_envelope=e_trace,
  canonical_trace_is_bare_EH_K=False,continuum_TT_admitted=False,physical_exterior_admitted=False)
