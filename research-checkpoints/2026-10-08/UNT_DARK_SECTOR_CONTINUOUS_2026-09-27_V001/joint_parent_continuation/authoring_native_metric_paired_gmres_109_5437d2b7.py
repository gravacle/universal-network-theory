"""Definitions-only paired nonsymmetric GMRES; np/P/keep supplied by caller.
No factor/source/RHS/physical change, import-time action, or numerical author run.
Actual caller must authenticate latest75215 seed and earned STAR factor proof.
Square T and its actual transpose use the retained coupled chart/physical masks.
Arnoldi works on T* A T; no self-adjointness, SPD fine action or error bound is
assumed. Cap is explicit <=80, no restart/direction drop/clipping. Two-pass DD
MGS retains all basis/H words, operator/orthogonalization/QR/readout defects.
Binary64 Givens/upper solve are numerical coordinates only; final acceptance
belongs to all six original raw/scaled rows, then the separately NEW literal
increment readout. Candidates at20/40/80 (or explicit smaller cap/breakdown)
are built from the authenticated warm seed, never from a reset physical state.
Old action/residual are reused; only NEW directions/candidates and unsigned
operation bounds are evaluated. Full before/after/q and recursive-prediction
contacts are retained. A later caller must normalize all checkpoint operands.
"""
NATIVE_METRIC_GMRES_AUTHOR_DRAFT=True
NATIVE_METRIC_GMRES_AUTHORING_IN_PROGRESS=True

def native_metric_gmres_put(label,x):
 for w,suffix in enumerate(('hi','lo')):keep(label+'_'+suffix,np.asarray(x[w]).copy())
 return x

def native_metric_gmres_tree(x,label):
 assert x[0].shape==x[1].shape and x[0].ndim==1 and len(x[0])>0
 native_metric_gmres_put(label+'_terms',x);v=x
 while len(v[0])>1:
  n=len(v[0]);m=n-n%2;v2=P.a_add((v[0][:m:2],v[1][:m:2]),(v[0][1:m:2],v[1][1:m:2]))
  if n%2:v2=tuple(np.concatenate((v2[w],v[w][-1:])) for w in (0,1))
  v=v2;native_metric_gmres_put(label+'_partial',v)
 return native_metric_gmres_put(label+'_sum',tuple(np.asarray(a[0]).copy() for a in v))

def native_metric_gmres_dot(x,y,label):return native_metric_gmres_tree(P.a_mul(x,y),label)

def native_metric_gmres_norm(x,label):
 words=native_metric_gmres_dot(x,x,label+'_squared');value=float(words[0]+words[1]);keep(label+'_squared_readout',np.asarray(value));native_metric_gmres_put(label+'_squared_readout_defect',P.a_sub(words,P.a_dd(value)))
 assert np.isfinite(value) and value>=0
 if value==0:assert np.all(x[0]==0) and np.all(x[1]==0),'Unresolved nonzero Arnoldi norm'
 norm=float(np.sqrt(value));keep(label+'_normalizing_norm',np.asarray(norm));native_metric_gmres_put(label+'_sqrt_contact',P.a_sub(P.a_prod(norm,norm),words));return norm

def native_metric_gmres_star_full(x,pre,label,adjoint=False):
 assert x[0].shape==x[1].shape==(403340,);parts=[P.unpack_fields(a,False) for a in x]
 native=tuple(a[0].transpose(0,2,3,1).reshape(33,3915,3) for a in parts);metric=tuple(a[1].transpose(1,2,0).reshape(3915,6) for a in parts)
 fn=native_metric_star_adjoint if adjoint else native_metric_star_forward
 n,k=fn(native,metric,pre,label+'_node_order')
 n=tuple(a.reshape(33,87,45,3).transpose(0,3,1,2) for a in n);k=tuple(a.reshape(87,45,6).transpose(2,0,1) for a in k)
 return native_metric_gmres_put(label+'_full_independent',P.pack_dd(n,k))

def native_metric_gmres_upper(R,b,label):
 assert R.shape==(len(b),len(b));x=np.zeros_like(b)
 for i in range(len(b)-1,-1,-1):
  pivot=R[i,i];keep(label+'_current_pivot',np.asarray(pivot));assert np.isfinite(pivot) and pivot!=0,'Exact QR pivot breakdown; no clipping'
  terms=R[i,i+1:]*x[i+1:];keep(label+'_current_terms',terms.copy());x[i]=(b[i]-np.sum(terms))/pivot;keep(label+'_current_solution',x.copy());assert np.all(np.isfinite(x))
 keep(label+'_solution',x.copy());keep(label+'_row_contact',(R@x-b).copy());keep(label+'_row_positive_envelope',(abs(R)@abs(x)+abs(b)).copy());return x

def native_metric_gmres_candidate(start,current,rhs,delta,action,positive,scores,label):
 native_metric_gmres_put(label+'_before_nodes',start);native_metric_gmres_put(label+'_before_action',current['action']);native_metric_gmres_put(label+'_before_original_residual',current['residual']);native_metric_gmres_put(label+'_delta',delta)
 mid,qh=P.dd_node_update(start,delta[0],keep,label+'_insert_high');native_metric_gmres_put(label+'_after_high_insert',mid)
 updated,ql=P.dd_node_update(mid,delta[1],keep,label+'_insert_low');native_metric_gmres_put(label+'_updated_nodes',updated)
 q=native_metric_gmres_put(label+'_total_compression_words',P.a_sum(qh,ql));increment=native_metric_gmres_put(label+'_exact_increment_two_word_readout',P.a_sub(delta,q))
 recycled_trace_exact_defect((delta[0],delta[1],-q[0],-q[1],-increment[0],-increment[1]),label+'_increment_readout')
 actual=native_metric_gmres_put(label+'_NEW_original_action',action(updated,label+'_candidate_action'));res=native_metric_gmres_put(label+'_NEW_original_residual',P.a_sub(rhs,actual))
 a_delta=native_metric_gmres_put(label+'_NEW_delta_action',action(delta,label+'_delta_action'));a_q=native_metric_gmres_put(label+'_NEW_compression_action',action(q,label+'_compression_action'))
 predicted=native_metric_gmres_put(label+'_residual_prediction',P.a_add(P.a_sub(current['residual'],a_delta),a_q));gap=native_metric_gmres_put(label+'_residual_update_gap',P.a_sub(res,predicted))
 bound=2*(abs(rhs[0])+abs(rhs[1]))
 for role,x in (('old',start),('new',updated),('delta',delta),('q',q)):
  e=np.asarray(positive(x,label+'_'+role+'_positive'));keep(label+'_'+role+'_positive_envelope',e.copy());assert e.shape==rhs[0].shape and np.all(np.isfinite(e)) and np.all(e>=0);bound=bound+2*e
 keep(label+'_residual_update_envelope',bound.copy());P.check(label+'_NEW_original_residual_update_construction',gap[0]+gap[1],np.zeros_like(bound),bound)
 rows=np.asarray(scores(res,label+'_original_six'));keep(label+'_original_six_scores',rows.copy());assert rows.shape==(3,2) and np.all(np.isfinite(rows)) and np.all(rows>=0)
 return updated,dict(action=actual,residual=res,scores=rows,admitted=bool(np.all(rows<=P.LINEAR_TOL))),increment

def native_metric_gmres_solve(start,current,rhs,forward,adjoint,action,positive,scores,label,cap,progress=None):
 assert 1<=cap<=80 and start[0].shape==start[1].shape==rhs[0].shape==rhs[1].shape and start[0].ndim==1
 n=len(start[0]);native_metric_gmres_put(label+'_warm_nodes',start);native_metric_gmres_put(label+'_original_RHS',rhs);native_metric_gmres_put(label+'_cached_original_action',current['action']);native_metric_gmres_put(label+'_cached_original_residual',current['residual'])
 if np.all(current['scores']<=P.LINEAR_TOL):return start,current,P.a_dd(np.zeros(n)),dict(iterations=0,cap=cap,restarts=0,reason='already_original_rows_admitted')
 initial=native_metric_gmres_put(label+'_initial_adjoint_residual',adjoint(current['residual'],label+'_initial_adjoint'));beta=native_metric_gmres_norm(initial,label+'_initial');assert beta>0,'Congruence residual zero but original rows fail'
 V=[native_metric_gmres_put(label+'_basis_000',P.a_div64(initial,beta,keep,label+'_initial_normalization'))];Hh=np.zeros((cap+1,cap));Hl=Hh.copy();R=Hh.copy();cs=np.zeros(cap);sn=cs.copy();g=np.zeros(cap+1);g[0]=beta;history=[];arnoldi_errors=[];arnoldi_bounds=[];updated=start;after=current;increment=P.a_dd(np.zeros(n));reason='explicit_cap';iterations=0
 for j in range(cap):
  fy=native_metric_gmres_put(label+'_current_forward_direction',forward(V[j],label+'_current_forward'));av=native_metric_gmres_put(label+'_current_fine_direction_action',action(fy,label+'_current_fine_action'));original=native_metric_gmres_put(label+'_current_congruence_action',adjoint(av,label+'_current_adjoint'));w=original;h=P.a_dd(np.zeros(j+1))
  for repeat in range(2):
   for i in range(j+1):
    value=native_metric_gmres_dot(V[i],w,label+'_current_MGS_dot');h[0][i],h[1][i]=P.a_add((h[0][i],h[1][i]),value)
    w=native_metric_gmres_put(label+'_current_MGS_remainder',P.a_sub(w,P.a_mul(value,V[i])))
  Hh[:j+1,j]=h[0];Hl[:j+1,j]=h[1];norm=native_metric_gmres_norm(w,label+'_current_remainder');Hh[j+1,j]=norm
  rebuilt=w;envelope=abs(w[0])+abs(w[1])+abs(original[0])+abs(original[1])
  for i in range(j+1):rebuilt=P.a_add(rebuilt,P.a_mul((h[0][i],h[1][i]),V[i]));envelope=envelope+(abs(h[0][i])+abs(h[1][i]))*(abs(V[i][0])+abs(V[i][1]))
  defect=native_metric_gmres_put(label+'_current_Arnoldi_reconstruction_gap',P.a_sub(original,rebuilt));keep(label+'_current_Arnoldi_positive_envelope',envelope.copy());arnoldi_errors.append(float(np.linalg.norm(defect[0]+defect[1])));arnoldi_bounds.append(float(np.linalg.norm(envelope)))
  column=Hh[:j+2,j]+Hl[:j+2,j];native_metric_gmres_put(label+'_current_H_readout_defect',P.a_sub((Hh[:j+2,j],Hl[:j+2,j]),P.a_dd(column)));keep(label+'_current_unrotated_H_column',column.copy())
  for i in range(j):a,b=column[i],column[i+1];column[i]=cs[i]*a+sn[i]*b;column[i+1]=-sn[i]*a+cs[i]*b
  den=float(np.hypot(column[j],column[j+1]));keep(label+'_current_Givens_denominator',np.asarray(den))
  if not np.isfinite(den) or den==0:reason='exact_QR_pivot_breakdown';break
  cs[j]=column[j]/den;sn[j]=column[j+1]/den;a,b=column[j],column[j+1];column[j]=cs[j]*a+sn[j]*b;discarded=-sn[j]*a+cs[j]*b;keep(label+'_current_QR_lower_roundoff',np.asarray(discarded));column[j+1]=0;R[:j+2,j]=column
  a,b=g[j],g[j+1];g[j]=cs[j]*a+sn[j]*b;g[j+1]=-sn[j]*a+cs[j]*b;iterations=j+1
  history.append((iterations,float(abs(g[j+1])),norm,den));keep(label+'_history',np.asarray(history));keep(label+'_H_hi',Hh.copy());keep(label+'_H_lo',Hl.copy());keep(label+'_R',R.copy());keep(label+'_Givens_cos',cs.copy());keep(label+'_Givens_sin',sn.copy());keep(label+'_rotated_RHS',g.copy());native_metric_gmres_put(label+'_all_earned_basis',P.a_stack(V,axis=1))
  checkpoint=iterations in (20,40,80) or iterations==cap or norm==0
  if checkpoint:
   coeff=native_metric_gmres_upper(R[:iterations,:iterations],g[:iterations],label+'_current_small_upper');aux=P.a_dd(np.zeros(n))
   for i in range(iterations):aux=P.a_add(aux,P.a_mul64(coeff[i],V[i]))
   native_metric_gmres_put(label+'_current_auxiliary_candidate',aux);delta=native_metric_gmres_put(label+'_current_physical_candidate_increment',forward(aux,label+'_candidate_forward'))
   updated,after,increment=native_metric_gmres_candidate(start,current,rhs,delta,action,positive,scores,label+'_candidate_%03d'%iterations)
   if progress is not None:progress(iterations,updated,after,increment)
   if after['admitted']:reason='original_six_rows_admitted';break
  if norm==0:reason='exact_Arnoldi_breakdown_without_original_admission';break
  if iterations<cap:V.append(native_metric_gmres_put(label+'_basis_%03d'%iterations,P.a_div64(w,norm,keep,label+'_current_normalization')))
 ae=np.asarray(arnoldi_errors);ab=np.asarray(arnoldi_bounds);keep(label+'_all_Arnoldi_contact_norms',ae.copy());keep(label+'_all_Arnoldi_operation_bounds',ab.copy());P.check(label+'_all_Arnoldi_reconstructions',ae,np.zeros_like(ae),ab)
 if iterations:
  Q=np.eye(iterations+1)
  for i in range(iterations):a,b=Q[i].copy(),Q[i+1].copy();Q[i]=cs[i]*a+sn[i]*b;Q[i+1]=-sn[i]*a+cs[i]*b
  HH=Hh[:iterations+1,:iterations]+Hl[:iterations+1,:iterations];RR=R[:iterations+1,:iterations];contact=Q@HH-RR;bound=abs(Q)@abs(HH)+abs(RR);keep(label+'_small_Q',Q.copy());keep(label+'_small_QR_contact',contact.copy());keep(label+'_small_QR_positive_bound',bound.copy());P.check(label+'_small_QR_operation_norm',np.asarray(np.linalg.norm(contact)),np.asarray(0.),np.asarray(np.linalg.norm(bound)))
 return updated,after,increment,dict(iterations=iterations,cap=cap,restarts=0,reason=reason,original_six_rows_admitted=after['admitted'],self_adjointness_assumed=False,physical_adoption=False)
