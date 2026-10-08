"""HELD bounded numerical recurrence for425955 coupled quasi-Newton coordinates.
Same paired117 two-pass MGS/QR/update contacts; identity left, explicit signed
right map, one cycle cap40 and no restart. Generalized row diagnostics are
numerical only. Original147/87/290/phase and all physical finite gates remain
external authorities. An action callback may use sampled coefficient proxies;
passing these recurrence contacts cannot admit an UNT metric or new43 result.
Globals np,P,keep; no source body, old solve, payload or import-time work.
"""
COUPLED_KRYLOV_AUTHOR_DRAFT=True
COUPLED_KRYLOV_AUTHORING_IN_PROGRESS=False
COUPLED_KRYLOV_PARENT=('author_fragment_native_metric_star_paired_gmres_v001.py','3ba68a8916f94a2ffc5fb3d66e72cf66c6ab249d2941a658f3003b70f8e04770')
COUPLED_KRYLOV_FUTURE_CLOSURES={n:(None,None,None) for n in ('mechanical_coefficient','rate_normal_coefficient','configuration_coefficient','gauge_feedback','same_candidate_rows')}

def cqn_identity_left(x,label):
 assert x[0].shape==x[1].shape==(425955,)
 return cqn_put(label+'_identity_left',tuple(w.copy() for w in x))

def cqn_put(label,x):
 for w,suffix in enumerate(('hi','lo')):keep(label+'_'+suffix,np.asarray(x[w]).copy())
 return x


def cqn_tree(x,label):
 assert x[0].shape==x[1].shape and x[0].ndim==1 and len(x[0])>0
 cqn_put(label+'_terms',x);v=x
 while len(v[0])>1:
  n=len(v[0]);m=n-n%2;v2=P.a_add((v[0][:m:2],v[1][:m:2]),(v[0][1:m:2],v[1][1:m:2]))
  if n%2:v2=tuple(np.concatenate((v2[w],v[w][-1:])) for w in (0,1))
  v=v2;cqn_put(label+'_partial',v)
 return cqn_put(label+'_sum',tuple(np.asarray(a[0]).copy() for a in v))


def cqn_dot(x,y,label):return cqn_tree(P.a_mul(x,y),label)


def cqn_expansion(words,label):
 expansion=[]
 for word in words:
  q=np.asarray(word).copy();out=[]
  for old in expansion:q,e=P.a_sum(q,old);out.append(e)
  expansion=out+[q]
 result=np.stack(expansion);keep(label+'_exact_expansion',result.copy());return result


def cqn_norm(x,label):
 words=cqn_dot(x,x,label+'_squared');value=float(words[0]+words[1]);keep(label+'_squared_readout',np.asarray(value));cqn_put(label+'_squared_readout_defect',P.a_sub(words,P.a_dd(value)))
 assert np.isfinite(value) and value>=0
 if value==0:assert np.all(x[0]==0) and np.all(x[1]==0),'Unresolved nonzero Arnoldi norm'
 norm=float(np.sqrt(value));keep(label+'_normalizing_norm',np.asarray(norm));cqn_put(label+'_sqrt_contact',P.a_sub(P.a_prod(norm,norm),words));return norm


def cqn_upper(R,b,label):
 assert R.shape==(len(b),len(b));x=np.zeros_like(b)
 for i in range(len(b)-1,-1,-1):
  pivot=R[i,i];keep(label+'_current_pivot',np.asarray(pivot));assert np.isfinite(pivot) and pivot!=0,'Exact QR pivot breakdown; no clipping'
  terms=R[i,i+1:]*x[i+1:];keep(label+'_current_terms',terms.copy());x[i]=(b[i]-np.sum(terms))/pivot;keep(label+'_current_solution',x.copy());assert np.all(np.isfinite(x))
 keep(label+'_solution',x.copy());keep(label+'_row_contact',(R@x-b).copy());keep(label+'_row_positive_envelope',(abs(R)@abs(x)+abs(b)).copy());return x


def cqn_candidate(start,current,rhs,delta,action,positive,scores,update,label):
 cqn_put(label+'_before_nodes',start);cqn_put(label+'_before_action',current['action']);cqn_put(label+'_before_original_residual',current['residual']);cqn_put(label+'_delta',delta)
 mid,qh=update(start,delta[0],keep,label+'_insert_high');cqn_put(label+'_after_high_insert',mid)
 updated,ql=update(mid,delta[1],keep,label+'_insert_low');cqn_put(label+'_updated_nodes',updated)
 q=cqn_put(label+'_total_compression_words',P.a_sum(qh,ql));increment=cqn_put(label+'_exact_increment_two_word_readout',P.a_sub(delta,q))
 cqn_expansion((delta[0],delta[1],-q[0],-q[1],-increment[0],-increment[1]),label+'_increment_readout')
 actual=cqn_put(label+'_NEW_original_action',action(updated,label+'_candidate_action'));res=cqn_put(label+'_NEW_original_residual',P.a_sub(rhs,actual))
 a_delta=cqn_put(label+'_NEW_delta_action',action(delta,label+'_delta_action'));a_q=cqn_put(label+'_NEW_compression_action',action(q,label+'_compression_action'))
 predicted=cqn_put(label+'_residual_prediction',P.a_add(P.a_sub(current['residual'],a_delta),a_q));gap=cqn_put(label+'_residual_update_gap',P.a_sub(res,predicted))
 bound=2*(abs(rhs[0])+abs(rhs[1]))
 for role,x in (('old',start),('new',updated),('delta',delta),('q',q)):
  e=np.asarray(positive(x,label+'_'+role+'_positive'));keep(label+'_'+role+'_positive_envelope',e.copy());assert e.shape==rhs[0].shape and np.all(np.isfinite(e)) and np.all(e>=0);bound=bound+2*e
 keep(label+'_residual_update_envelope',bound.copy());P.check(label+'_NEW_original_residual_update_construction',gap[0]+gap[1],np.zeros_like(bound),bound)
 rows=np.asarray(scores(res,label+'_numerical_rows'));keep(label+'_numerical_rows_scores',rows.copy());assert rows.ndim==2 and rows.shape[1]==2 and rows.shape[0]>0 and np.all(np.isfinite(rows)) and np.all(rows>=0)
 return updated,dict(action=actual,residual=res,scores=rows,numerically_admitted=bool(np.all(rows<=P.LINEAR_TOL))),increment


def cqn_solve(start,current,rhs,forward,action,positive,scores,update,admission,label,cap,progress):
 assert not COUPLED_KRYLOV_AUTHOR_DRAFT and not COUPLED_KRYLOV_AUTHORING_IN_PROGRESS
 assert all(x is not None for pin in COUPLED_KRYLOV_FUTURE_CLOSURES.values() for x in pin)
 assert 1<=cap<=40 and P.LINEAR_TOL==1e-10 and start[0].shape==start[1].shape==rhs[0].shape==rhs[1].shape==(425955,)
 assert callable(update) and callable(progress) and all(callable(f) for f in (forward,action,positive,scores))
 assert admission['all_selected_source_seals_authenticated'] is True and admission['same_candidate_original_law'] is True
 assert admission['derivative_feedback_frozen_explicitly'] is True and admission['fresh_finite_feedback_value_required'] is True
 assert admission['future_closures']==COUPLED_KRYLOV_FUTURE_CLOSURES and admission['physical_adoption'] is False
 assert admission['original_six_canonical_gates_unchanged'] is True and admission['original_phase_normal_CMC_authority_external'] is True
 n=len(start[0]);cqn_put(label+'_warm_nodes',start);cqn_put(label+'_original_RHS',rhs);cqn_put(label+'_cached_original_action',current['action']);cqn_put(label+'_cached_original_residual',current['residual'])
 if np.all(current['scores']<=P.LINEAR_TOL):return start,current,P.a_dd(np.zeros(n)),dict(iterations=0,cap=cap,restarts=0,reason='already_numerical_rows_admitted')
 initial=cqn_put(label+'_initial_identity_left_residual',cqn_identity_left(current['residual'],label+'_initial_identity_left'));beta=cqn_norm(initial,label+'_initial');assert beta>0,'Coordinate residual zero while numerical rows fail'
 V=[cqn_put(label+'_basis_000',P.a_div64(initial,beta,keep,label+'_initial_normalization'))];Hh=np.zeros((cap+1,cap));Hl=Hh.copy();R=Hh.copy();cs=np.zeros(cap);sn=cs.copy();g=np.zeros(cap+1);g[0]=beta;history=[];arnoldi_errors=[];arnoldi_bounds=[];updated=start;after=current;increment=P.a_dd(np.zeros(n));reason='explicit_cap';iterations=0
 for j in range(cap):
  fy=cqn_put(label+'_current_forward_direction',forward(V[j],label+'_current_forward'));av=cqn_put(label+'_current_fine_direction_action',action(fy,label+'_current_fine_action'));original=cqn_put(label+'_current_coordinate_action',cqn_identity_left(av,label+'_current_identity_left'));w=original;h=P.a_dd(np.zeros(j+1))
  for repeat in range(2):
   for i in range(j+1):
    value=cqn_dot(V[i],w,label+'_current_MGS_dot');h[0][i],h[1][i]=P.a_add((h[0][i],h[1][i]),value)
    w=cqn_put(label+'_current_MGS_remainder',P.a_sub(w,P.a_mul(value,V[i])))
  Hh[:j+1,j]=h[0];Hl[:j+1,j]=h[1];norm=cqn_norm(w,label+'_current_remainder');Hh[j+1,j]=norm
  rebuilt=w;envelope=abs(w[0])+abs(w[1])+abs(original[0])+abs(original[1])
  for i in range(j+1):rebuilt=P.a_add(rebuilt,P.a_mul((h[0][i],h[1][i]),V[i]));envelope=envelope+(abs(h[0][i])+abs(h[1][i]))*(abs(V[i][0])+abs(V[i][1]))
  defect=cqn_put(label+'_current_Arnoldi_reconstruction_gap',P.a_sub(original,rebuilt));keep(label+'_current_Arnoldi_positive_envelope',envelope.copy());arnoldi_errors.append(float(np.linalg.norm(defect[0]+defect[1])));arnoldi_bounds.append(float(np.linalg.norm(envelope)))
  column=Hh[:j+2,j]+Hl[:j+2,j];cqn_put(label+'_current_H_readout_defect',P.a_sub((Hh[:j+2,j],Hl[:j+2,j]),P.a_dd(column)));keep(label+'_current_unrotated_H_column',column.copy());keep(label+'_H_hi',Hh.copy());keep(label+'_H_lo',Hl.copy());cqn_put(label+'_all_earned_basis',P.a_stack(V,axis=1))
  for i in range(j):a,b=column[i],column[i+1];column[i]=cs[i]*a+sn[i]*b;column[i+1]=-sn[i]*a+cs[i]*b
  den=float(np.hypot(column[j],column[j+1]));keep(label+'_current_Givens_denominator',np.asarray(den))
  if not np.isfinite(den) or den==0:reason='exact_QR_pivot_breakdown';break
  cs[j]=column[j]/den;sn[j]=column[j+1]/den;a,b=column[j],column[j+1];column[j]=cs[j]*a+sn[j]*b;discarded=-sn[j]*a+cs[j]*b;keep(label+'_current_QR_lower_roundoff',np.asarray(discarded));column[j+1]=0;R[:j+2,j]=column
  a,b=g[j],g[j+1];g[j]=cs[j]*a+sn[j]*b;g[j+1]=-sn[j]*a+cs[j]*b;iterations=j+1
  history.append((iterations,float(abs(g[j+1])),norm,den));keep(label+'_history',np.asarray(history));keep(label+'_H_hi',Hh.copy());keep(label+'_H_lo',Hl.copy());keep(label+'_R',R.copy());keep(label+'_Givens_cos',cs.copy());keep(label+'_Givens_sin',sn.copy());keep(label+'_rotated_RHS',g.copy());cqn_put(label+'_all_earned_basis',P.a_stack(V,axis=1))
  checkpoint=iterations in (20,40) or iterations==cap or norm==0
  if checkpoint:
   coeff=cqn_upper(R[:iterations,:iterations],g[:iterations],label+'_current_small_upper');aux=P.a_dd(np.zeros(n))
   for i in range(iterations):aux=P.a_add(aux,P.a_mul64(coeff[i],V[i]))
   cqn_put(label+'_current_auxiliary_candidate',aux);delta=cqn_put(label+'_current_physical_candidate_increment',forward(aux,label+'_candidate_forward'))
   updated,after,increment=cqn_candidate(start,current,rhs,delta,action,positive,scores,update,label+'_candidate_%03d'%iterations)
   if progress is not None:progress(iterations,updated,after,increment)
   if after['numerically_admitted']:reason='numerical_rows_admitted';break
  if norm==0:reason='exact_Arnoldi_breakdown_without_original_admission';break
  if iterations<cap:V.append(cqn_put(label+'_basis_%03d'%iterations,P.a_div64(w,norm,keep,label+'_current_normalization')))
 ae=np.asarray(arnoldi_errors);ab=np.asarray(arnoldi_bounds);keep(label+'_all_Arnoldi_contact_norms',ae.copy());keep(label+'_all_Arnoldi_operation_bounds',ab.copy());P.check(label+'_all_Arnoldi_reconstructions',ae,np.zeros_like(ae),ab)
 if iterations:
  Q=np.eye(iterations+1)
  for i in range(iterations):a,b=Q[i].copy(),Q[i+1].copy();Q[i]=cs[i]*a+sn[i]*b;Q[i+1]=-sn[i]*a+cs[i]*b
  HH=Hh[:iterations+1,:iterations]+Hl[:iterations+1,:iterations];RR=R[:iterations+1,:iterations];contact=Q@HH-RR;bound=abs(Q)@abs(HH)+abs(RR);keep(label+'_small_Q',Q.copy());keep(label+'_small_QR_contact',contact.copy());keep(label+'_small_QR_positive_bound',bound.copy());P.check(label+'_small_QR_operation_norm',np.asarray(np.linalg.norm(contact)),np.asarray(0.),np.asarray(np.linalg.norm(bound)))
 return updated,after,increment,dict(iterations=iterations,cap=cap,restarts=0,reason=reason,numerical_rows_admitted=after['numerically_admitted'],self_identity_leftness_assumed=False,physical_adoption=False)

