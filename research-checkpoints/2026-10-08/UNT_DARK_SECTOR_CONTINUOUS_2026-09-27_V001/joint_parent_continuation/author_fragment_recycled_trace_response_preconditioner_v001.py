"""Guard-held NEW numerical congruence for the unchanged trace-response equations.
Caller supplies np/P/keep, cached paired nodes/action/residual/RHS, positive scale,
four earned original_iterate snapshots at40/80/120/160, original six-row score
callback and sufficient white target, and authenticated frozen action callbacks.
No input, old operator, fixture, current feature or solver is evaluated on import.
Four coarse directions are fixed successive snapshot differences from zero;
there is no selected subset, direction drop, eigenvalue gain or altered RHS.
Hs=(H+H.T)/2 and |Hs| are numerical preconditioner coefficients only. Preserved
H asymmetry and construction margins do not prove physical self-adjointness,
global coercivity, an inverse error bound or a canonical/physical preparation.
Actual literal qualification requires one NEW increment readout at fixed config,
with old literal action reused and all compression/construction defects retained.
"""
RECYCLED_TRACE_KERNEL_AUTHOR_DRAFT=True
RECYCLED_TRACE_KERNEL_AUTHORING_IN_PROGRESS=False

def recycled_trace_put(label,x):
 for w,suffix in enumerate(('hi','lo')):keep(label+'_'+suffix,np.asarray(x[w]).copy())
 return x

def recycled_trace_tree_sum(x,label):
 # Vectorized pairwise DD reduction: keep original words, one partial, final.
 assert x[0].shape==x[1].shape and x[0].ndim==1
 recycled_trace_put(label+'_terms',x);value=x
 while len(value[0])>1:
  n=len(value[0]);m=n-n%2;next_value=P.a_add((value[0][:m:2],value[1][:m:2]),(value[0][1:m:2],value[1][1:m:2]))
  if n%2:next_value=tuple(np.concatenate((next_value[w],value[w][-1:])) for w in (0,1))
  value=next_value;recycled_trace_put(label+'_current_partial',value)
 return recycled_trace_put(label+'_sum',tuple(np.asarray(v[0]).copy() for v in value))

def recycled_trace_dot(x,y,label):
 assert x[0].shape==x[1].shape==y[0].shape==y[1].shape
 return recycled_trace_tree_sum(P.a_mul(x,y),label)

def recycled_trace_exact_defect(words,label):
 # Grow an error-free expansion of the supplied finite saved arithmetic words.
 expansion=[]
 for word in words:
  q=np.asarray(word).copy();out=[]
  for old in expansion:q,e=P.a_sum(q,old);out.append(e)
  expansion=out+[q]
 result=np.stack(expansion);keep(label+'_exact_expansion',result.copy());return result

def recycled_trace_preconditioner(snapshots,scale,action_dd,positive_action,label):
 assert tuple(snapshots)==(40,80,120,160) and scale.ndim==1 and np.all(np.isfinite(scale)) and np.all(scale>0)
 n=len(scale);previous=np.zeros(n);columns=[]
 keep(label+'_inherited_positive_scale',scale.copy())
 for k in (40,80,120,160):
  current=np.asarray(snapshots[k]);assert current.shape==(n,) and np.all(np.isfinite(current));keep(label+'_snapshot_%d'%k,current.copy())
  difference=recycled_trace_put(label+'_direction_%d_exact_difference'%k,P.a_sub(P.a_dd(current),P.a_dd(previous)));previous=current
  white=recycled_trace_put(label+'_direction_%d_scaled_words'%k,P.a_mul64(scale,difference));norm=float(np.linalg.norm(white[0]+white[1]));keep(label+'_direction_%d_normalizing_norm'%k,np.asarray(norm).copy());assert np.isfinite(norm) and norm>0
  normalized=recycled_trace_put(label+'_direction_%d_normalized_words'%k,P.a_div64(difference,norm,keep,label+'_direction_%d_normalization'%k))
  column=normalized[0]+normalized[1];keep(label+'_direction_%d_rounded_coarse_column'%k,column.copy());recycled_trace_put(label+'_direction_%d_rounding_defect'%k,P.a_sub(normalized,P.a_dd(column)));columns.append(column)
 C=np.stack(columns,axis=1);keep(label+'_coarse_columns',C.copy());white=[P.a_mul64(scale,P.a_dd(C[:,i])) for i in range(4)]
 Gh=np.zeros((4,4));Gl=Gh.copy();eG=Gh.copy()
 for i in range(4):
  for j in range(4):
   value=recycled_trace_dot(white[i],white[j],label+'_independence_%d_%d'%(i,j));Gh[i,j],Gl[i,j]=value
   eG[i,j]=2*np.sum((abs(white[i][0])+abs(white[i][1]))*(abs(white[j][0])+abs(white[j][1])))
 recycled_trace_put(label+'_independence_Gram',(Gh,Gl));keep(label+'_independence_positive_construction_bound',eG.copy())
 G=Gh+Gl;Gs=(G+G.T)/2;wg,vg=np.linalg.eigh(Gs);keep(label+'_independence_eigenvalues',wg.copy());keep(label+'_independence_eigenvectors',vg.copy());keep(label+'_independence_asymmetry',(G-G.T).copy())
 gerror=P.TOL*np.linalg.norm(eG,2)+np.linalg.norm(Gs@vg-vg*wg,2)+1024*np.finfo(float).eps*np.linalg.norm(abs(Gs),2)
 keep(label+'_independence_resolved_error_budget',np.asarray(gerror).copy());assert np.all(np.isfinite(wg)) and np.min(wg)>gerror
 Hh=np.zeros((4,4));Hl=Hh.copy();eH=Hh.copy()
 for j in range(4):
  action=recycled_trace_put(label+'_new_coarse_action_%d'%j,action_dd(P.a_dd(C[:,j])))
  envelope=np.asarray(positive_action(P.a_dd(C[:,j]),label+'_new_coarse_positive_action_%d'%j));keep(label+'_new_coarse_positive_action_%d'%j,envelope.copy());assert envelope.shape==(n,) and np.all(np.isfinite(envelope)) and np.all(envelope>=0)
  for i in range(4):
   value=recycled_trace_dot(P.a_dd(C[:,i]),action,label+'_projected_action_%d_%d'%(i,j));Hh[i,j],Hl[i,j]=value;eH[i,j]=2*np.sum(abs(C[:,i])*envelope)
 recycled_trace_put(label+'_projected_H',(Hh,Hl));keep(label+'_projected_positive_construction_bound',eH.copy())
 H=Hh+Hl;Hs=(H+H.T)/2;keep(label+'_projected_H_rounded',H.copy());keep(label+'_projected_H_asymmetry',(H-H.T).copy());keep(label+'_symmetrized_preconditioner_H',Hs.copy())
 symwords=P.a_mul64(.5,P.a_add((Hh,Hl),(Hh.T,Hl.T)));recycled_trace_put(label+'_symmetrization_rounding_defect',P.a_sub(symwords,P.a_dd(Hs)))
 recycled_trace_put(label+'_projected_H_rounding_defect',P.a_sub((Hh,Hl),P.a_dd(H)))
 eigenvalues,eigenvectors=np.linalg.eigh(Hs);keep(label+'_projected_eigenvalues',eigenvalues.copy());keep(label+'_projected_eigenvectors',eigenvectors.copy())
 eigdefect=Hs@eigenvectors-eigenvectors*eigenvalues;orthdefect=eigenvectors.T@eigenvectors-np.eye(4);keep(label+'_projected_eigen_equation_defect',eigdefect.copy());keep(label+'_projected_eigen_orthogonality_defect',orthdefect.copy())
 herror=P.TOL*np.linalg.norm(eH,2)+np.linalg.norm(eigdefect,2)+1024*np.finfo(float).eps*np.linalg.norm(abs(Hs),2)
 keep(label+'_projected_resolved_error_budget',np.asarray(herror).copy());assert np.all(np.isfinite(eigenvalues)) and np.min(abs(eigenvalues))>herror
 factor=eigenvectors/np.sqrt(abs(eigenvalues))[None,:];absolute=(eigenvectors*abs(eigenvalues))@eigenvectors.T;keep(label+'_absolute_H',absolute.copy());keep(label+'_absolute_inverse_sqrt_factor',factor.copy());assert np.all(np.isfinite(factor))
 defect=absolute@(factor@factor.T)-np.eye(4);keep(label+'_coarse_inverse_defect',defect.copy());eabsolute=(abs(eigenvectors)*abs(eigenvalues))@abs(eigenvectors).T;keep(label+'_absolute_H_construction_envelope',eabsolute.copy());P.check(label+'_coarse_absolute_inverse_construction',defect,np.zeros((4,4)),eabsolute@abs(factor)@abs(factor).T+np.eye(4))
 return dict(columns=C,factor=factor,scale=scale,dimension=n,coarse_dimension=4,H=(Hh,Hl),H_asymmetry=H-H.T,independence_margin=float(np.min(wg)-gerror),projected_spectral_margin=float(np.min(abs(eigenvalues))-herror),symmetrization_is_preconditioner_only=True,physical_operator_or_RHS_changed=False,global_rank_or_coercivity_claimed=False)

def recycled_trace_forward(y,pre,label):
 n=pre['dimension'];assert y.shape==(n+4,);fine=y[:n]/pre['scale'];keep(label+'_fine_part',fine.copy());coarse=pre['columns']@(pre['factor']@y[n:]);keep(label+'_coarse_part',coarse.copy());out=fine+coarse;keep(label+'_rounded_fine_correction',out.copy())
 recycled_trace_put(label+'_addition_readout_defect',P.a_sub(P.a_add(P.a_dd(fine),P.a_dd(coarse)),P.a_dd(out)));assert np.all(np.isfinite(out));return out

def recycled_trace_adjoint(x,pre,label):
 assert x.shape==(pre['dimension'],);fine=x/pre['scale'];keep(label+'_fine_restriction',fine.copy());restricted=pre['columns'].T@x;keep(label+'_coarse_restriction',restricted.copy());coarse=pre['factor'].T@restricted;keep(label+'_coarse_coordinates',coarse.copy());out=np.concatenate((fine,coarse));keep(label+'_extended_vector',out.copy());assert np.all(np.isfinite(out));return out

def recycled_trace_warm_correction(nodes,current,rhs,pre,action64,action_dd,positive_action,score_callback,sufficient_white_target,label,cap=160):
 assert 1<=cap<=160 and not np.all(current['scores']<=P.LINEAR_TOL) and nodes[0].shape==nodes[1].shape==rhs[0].shape==rhs[1].shape==(pre['dimension'],)
 recycled_trace_put(label+'_before_nodes',nodes);recycled_trace_put(label+'_before_action',current['action']);recycled_trace_put(label+'_before_residual',current['residual']);recycled_trace_put(label+'_original_RHS',rhs);keep(label+'_before_scores',current['scores'].copy())
 rounded=current['residual'][0]+current['residual'][1];keep(label+'_recurrence_rhs_readout',rounded.copy());recycled_trace_put(label+'_recurrence_rhs_rounding_defect',P.a_sub(current['residual'],P.a_dd(rounded)))
 recurrence_rhs=recycled_trace_adjoint(rounded,pre,label+'_RHS');norm=float(np.linalg.norm(recurrence_rhs));tolerance=sufficient_white_target/norm;keep(label+'_sufficient_original_white_target',np.asarray(sufficient_white_target).copy());keep(label+'_relative_recurrence_target',np.asarray(tolerance).copy());assert np.isfinite(tolerance) and tolerance>0 and norm>0
 def action(y):return recycled_trace_adjoint(action64(recycled_trace_forward(y,pre,label+'_iterative_forward')),pre,label+'_iterative_adjoint')
 def certificate(y):
  delta=recycled_trace_forward(y,pre,label+'_callback_forward');trial,q=P.dd_node_update(nodes,delta,keep,label+'_callback_update');a=recycled_trace_put(label+'_callback_action',action_dd(trial));res=recycled_trace_put(label+'_callback_residual',P.a_sub(rhs,a));scores=score_callback(res,label+'_callback_original');keep(label+'_callback_scores',scores.copy())
  return recycled_trace_adjoint(res[0]+res[1],pre,label+'_callback_residual_adjoint'),scores
 y,scores,admitted,reason=P.minres_core(action,recurrence_rhs,np.ones(pre['dimension']+4),tolerance,certificate,label,cap=cap);keep(label+'_completed_extended_correction',y.copy());keep(label+'_solver_return_scores',scores.copy())
 delta=recycled_trace_forward(y,pre,label+'_completed_forward');updated,q=P.dd_node_update(nodes,delta,keep,label+'_final_update');a=recycled_trace_put(label+'_final_action',action_dd(updated));res=recycled_trace_put(label+'_final_residual',P.a_sub(rhs,a));scores=score_callback(res,label+'_final_original');keep(label+'_final_scores',scores.copy())
 da=recycled_trace_put(label+'_NEW_correction_action',action_dd(P.a_dd(delta)));qa=recycled_trace_put(label+'_NEW_compression_action',action_dd(P.a_dd(q)));gap=recycled_trace_put(label+'_original_residual_update_gap',P.a_sub(P.a_add(P.a_sub(res,current['residual']),da),qa))
 bound=2*(abs(rhs[0])+abs(rhs[1]))
 for role,x in (('old',nodes),('new',updated),('delta',P.a_dd(delta)),('q',P.a_dd(q))):bound+=positive_action(x,label+'_identity_'+role);keep(label+'_uncancelled_update_bound',bound.copy())
 P.check(label+'_paired_original_residual_update_with_q',gap[0]+gap[1],np.zeros(pre['dimension']),bound)
 increment=recycled_trace_put(label+'_exact_NEW_literal_increment',P.a_sum(delta,-q))
 return updated,dict(action=a,residual=res,scores=scores,admitted=bool(np.all(scores<=P.LINEAR_TOL))),increment,dict(cap=cap,new_cycles=1,reason=reason,callback_admitted=bool(admitted),original_six_scores=scores.tolist(),literal_original_response_admitted=False,finite_configuration_adopted=False,physical_adoption=False)

def recycled_trace_literal_translation(old_literal_action,NEW_increment_literal_action,rhs,new_frozen_action,score_callback,label):
 assert old_literal_action[0].shape==old_literal_action[1].shape==NEW_increment_literal_action[0].shape==NEW_increment_literal_action[1].shape==rhs[0].shape==rhs[1].shape==new_frozen_action[0].shape==new_frozen_action[1].shape
 recycled_trace_put(label+'_old_saved_literal_action',old_literal_action);recycled_trace_put(label+'_NEW_increment_literal_action',NEW_increment_literal_action)
 action=recycled_trace_put(label+'_new_literal_action',P.a_add(old_literal_action,NEW_increment_literal_action))
 defect=recycled_trace_exact_defect([old_literal_action[0],old_literal_action[1],NEW_increment_literal_action[0],NEW_increment_literal_action[1],-action[0],-action[1]],label+'_literal_addition_defect')
 residual=recycled_trace_put(label+'_new_literal_residual',P.a_sub(rhs,action));bridge=recycled_trace_put(label+'_literal_minus_frozen_derivative',P.a_sub(action,new_frozen_action));scores=score_callback(residual,label+'_literal_original');keep(label+'_literal_original_scores',scores.copy())
 return dict(action=action,residual=residual,frozen_bridge=bridge,addition_defect_expansion=defect,scores=scores,literal_original_response_admitted=bool(np.all(scores<=P.LINEAR_TOL)),original_primitive_stationarity_mismatch_resolved=False,finite_configuration_adopted=False,physical_adoption=False)

def fresh_recycled_trace_response_control():
 # NEW four-direction indefinite coupled method witness, not an old fixture.
 A=np.asarray(((2.,0.,.25,0.),(0.,3.,0.,.125),(.25,0.,-4.,0.),(0.,.125,0.,-5.)));scale=np.asarray((2.,3.,4.,5.));target=np.asarray((1.,-1.,-8.,24.));rhs=P.a_dd(np.asarray((0.,0.,129./4,-961./8)))
 start=(np.asarray((.5,-.25,-4.,10.)),np.asarray((2.**-60,-2.**-61,2.**-62,-2.**-63)));snapshots={};x=np.zeros(4)
 for j,k in enumerate((40,80,120,160)):x=x.copy();x[j]=2.**-j;snapshots[k]=x
 for n,v in (('A',A),('scale',scale),('target',target)):keep('fresh_recycled_'+n,v.copy())
 recycled_trace_put('fresh_recycled_rhs',rhs);recycled_trace_put('fresh_recycled_old_pair',start)
 def action_dd(x):return P.a_matvec(A,x)
 def action64(x):return A@x
 def positive(x,label):
  out=abs(A)@(abs(x[0])+abs(x[1]));keep(label+'_positive_action',out.copy());return out
 references=((slice(0,2),np.asarray((1.,2.)),scale[:2]),(slice(0,2),np.asarray((2.,3.)),scale[:2]),(slice(2,4),rhs[0][2:],scale[2:]))
 def scores(res,label):
  value=res[0]+res[1];rows=[]
  for sl,ref,s in references:rows.append((float(np.linalg.norm(value[sl])/np.linalg.norm(ref)),float(np.linalg.norm(value[sl]/s)/np.linalg.norm(ref/s))))
  out=np.asarray(rows);keep(label+'_six_original_scores',out.copy());return out
 sufficient=P.LINEAR_TOL*min(v for sl,ref,s in references for v in (np.linalg.norm(ref)/np.max(s),np.linalg.norm(ref/s)))
 current_action=action_dd(start);current_res=P.a_sub(rhs,current_action);current=dict(action=current_action,residual=current_res,scores=scores(current_res,'fresh_recycled_start'))
 pre=recycled_trace_preconditioner(snapshots,scale,action_dd,positive,'fresh_recycled_preconditioner')
 probe=np.asarray((.5,-.25,.75,-1.));dual=np.asarray((.125,-.25,.375,-.5,.625,-.75,.875,-1.));keep('fresh_recycled_adjoint_probe',probe.copy());keep('fresh_recycled_adjoint_dual',dual.copy());f=recycled_trace_forward(dual,pre,'fresh_recycled_forward');a=recycled_trace_adjoint(probe,pre,'fresh_recycled_adjoint')
 left=recycled_trace_dot(P.a_dd(probe),P.a_dd(f),'fresh_recycled_adjoint_left');right=recycled_trace_dot(P.a_dd(a),P.a_dd(dual),'fresh_recycled_adjoint_right');adjgap=P.a_sub(left,right);recycled_trace_put('fresh_recycled_adjoint_gap',adjgap)
 Cf,Ff=abs(pre['columns']),abs(pre['factor']);adjbound=2*(np.sum(abs(probe)*(abs(dual[:4])/scale+Cf@(Ff@abs(dual[4:]))))+np.sum(abs(dual[:4])*abs(probe)/scale)+np.sum(abs(dual[4:])*(Ff.T@(Cf.T@abs(probe)))));keep('fresh_recycled_adjoint_uncancelled_bound',np.asarray(adjbound).copy());P.check('fresh_recycled_actual_T_Tstar_adjoint',np.asarray(adjgap[0]+adjgap[1]),np.asarray(0.),np.asarray(adjbound))
 updated,after,increment,meta=recycled_trace_warm_correction(start,current,rhs,pre,action64,action_dd,positive,scores,sufficient,'fresh_recycled_warm_method',cap=8)
 error=float(np.linalg.norm(updated[0]+updated[1]-target));residual=float(np.linalg.norm(after['residual'][0]+after['residual'][1]));allowance=128*np.finfo(float).eps*(np.linalg.norm(updated[0])+np.linalg.norm(updated[1])+np.linalg.norm(target)+np.linalg.norm(rhs[0]));bound=(4./7)*residual+allowance;keep('fresh_recycled_independent_error_bound',np.asarray((error,residual,allowance,bound)).copy());assert after['admitted'] and np.all(rhs[0][:2]==0) and np.all(rhs[1][:2]==0)
 # Gershgorin signs separate the two positive and two negative eigenvalues
 # from zero by at least7/4, so ||error||<=4||residual||/7 before roundoff.
 P.check('fresh_recycled_zero_native_source_independent_error',np.asarray(error),np.asarray(0.),np.asarray(bound/P.TOL))
 return dict(kind='NEW_four_direction_indefinite_recycled_trace_method_control',cap=8,independent_singular_value_lower_bound=7./4,original_six_scores=after['scores'].tolist(),zero_native_source_relative_ratio=None,old_fixture_replayed=False,physical_adoption=False)
