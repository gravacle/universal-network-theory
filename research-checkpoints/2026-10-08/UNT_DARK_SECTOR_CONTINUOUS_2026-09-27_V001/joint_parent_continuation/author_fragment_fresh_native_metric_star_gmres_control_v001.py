"""Definitions-only NEW cap3 witness; caller supplies np/P/keep/GMRES117.
A is nonsymmetric and T is anisotropic; the first native RHS coordinate is zero.
The two inherited native reference norms are predeclared (1,2), never the zero
native RHS norm. The remaining two coordinates use the nonzero new metric RHS.
B=T^T A T has symmetric-part Gershgorin lower3/16, so ||B^-1||2<=16/3.
The known paired answer and dyadic forward/transpose words are independent of
the Arnoldi recurrence. The nodal bound includes disclosed arithmetic allowance;
this is a method witness, no current physical operator or canonical admission.
"""
FRESH_STAR_GMRES_CONTROL_AUTHOR_DRAFT=True
FRESH_STAR_GMRES_CONTROL_AUTHORING_IN_PROGRESS=False

def fresh_native_metric_star_gmres_control():
 label='fresh_nonsymmetric_star_GMRES';eps=2.**-60;before=len(P.CHECKS)
 A=np.asarray(((2.,1.,0.),(-.5,3.,1.),(0.,-2.,4.)));T=np.diag(np.asarray((2.,.5,.25)));scale=np.asarray((.5,2.,4.))
 B=np.asarray(((8.,1.,0.),(-.5,.75,.125),(0.,-.25,.25)));xt=np.asarray((1.,-2.,3.));yt=np.asarray((.5,-4.,12.));b=np.asarray((0.,-3.5,16.))
 for n,x in (('A',A),('T',T),('B_independent',B),('positive_scale',scale),('known_physical_high',xt),('known_auxiliary_high',yt),('RHS_high_independent',b),('native_reference_norms',np.asarray((1.,2.))),('symmetric_part_lower',np.asarray(3./16.)),('coercive_inverse_bound',np.asarray(16./3.))):keep(label+'_'+n,np.asarray(x).copy())
 target=native_metric_gmres_put(label+'_known_physical_pair',(xt.copy(),eps*xt));aux_target=native_metric_gmres_put(label+'_known_auxiliary_pair',(yt.copy(),eps*yt));rhs=native_metric_gmres_put(label+'_original_RHS',(b.copy(),eps*b));start=P.a_dd(np.zeros(3))
 def forward(x,l):return native_metric_gmres_put(l+'_T_forward',P.a_matvec(T,x))
 def adjoint(x,l):return native_metric_gmres_put(l+'_T_actual_transpose',P.a_matvec(T.T,x))
 def action(x,l):return native_metric_gmres_put(l+'_nonsymmetric_fine_action',P.a_matvec(A,x))
 def positive(x,l):
  e=abs(A)@(abs(x[0])+abs(x[1]));keep(l+'_uncancelled_A_envelope',e.copy());return e
 def scores(res,l):
  r=res[0]+res[1];q=rhs[0]+rhs[1];metric_raw=float(np.linalg.norm(q[1:]));metric_scaled=float(np.linalg.norm(q[1:]/scale[1:]));assert metric_raw>0 and metric_scaled>0 and rhs[0][0]==rhs[1][0]==0
  rows=np.asarray(((abs(r[0]),abs(r[0]/scale[0])/(1./scale[0])),(abs(r[0])/2.,abs(r[0]/scale[0])/(2./scale[0])),(np.linalg.norm(r[1:])/metric_raw,np.linalg.norm(r[1:]/scale[1:])/metric_scaled)))
  keep(l+'_six_predeclared_scores',rows.copy());keep(l+'_native_zero_RHS_relative_score_undefined',np.asarray(True));return rows
 e=P.a_dd(np.asarray((1.,0.,0.)));e=(e[0],eps*e[0])
 ae=action(e,label+'_dyadic_Ae');ate=native_metric_gmres_put(label+'_dyadic_ATe',P.a_matvec(A.T,e));f=forward(aux_target,label+'_dyadic_Ty');g=adjoint(rhs,label+'_dyadic_TTb')
 high=np.concatenate((ae[0],ate[0],f[0],g[0]));low=np.concatenate((ae[1],ate[1],f[1],g[1]));expected=np.asarray((2.,-.5,0.,2.,1.,0.,1.,-2.,3.,0.,-1.75,4.))
 keep(label+'_dyadic_expected_high',expected.copy());keep(label+'_dyadic_expected_low',(eps*expected).copy());assert np.array_equal(high,expected) and np.array_equal(low,eps*expected) and not np.array_equal(ae[0],ate[0])
 P.check(label+'_actual_forward_transpose_dyadic_words',np.concatenate((high,low)),np.concatenate((expected,eps*expected)),np.ones(24))
 initial_action=P.a_dd(np.zeros(3));current=dict(action=initial_action,residual=rhs,scores=scores(rhs,label+'_initial'),admitted=False)
 updated,after,increment,meta=native_metric_gmres_solve(start,current,rhs,forward,adjoint,action,positive,scores,label,3)
 native_metric_gmres_put(label+'_completed_nodes',updated);native_metric_gmres_put(label+'_completed_action',after['action']);native_metric_gmres_put(label+'_completed_residual',after['residual']);native_metric_gmres_put(label+'_completed_increment',increment)
 error=native_metric_gmres_put(label+'_known_auxiliary_error',P.a_div64(P.a_sub(updated,target),np.asarray((2.,.5,.25)),keep,label+'_physical_to_auxiliary'))
 dual=adjoint(after['residual'],label+'_original_residual_dual');error_norm=float(np.linalg.norm(error[0]+error[1]));dual_norm=float(np.linalg.norm(dual[0]+dual[1]))
 uncancelled=abs(T.T)@(abs(A)@(abs(updated[0])+abs(updated[1]))+abs(rhs[0])+abs(rhs[1]));roundoff=512*np.finfo(float).eps*(float(np.linalg.norm(uncancelled))+float(np.linalg.norm(abs(aux_target[0])+abs(aux_target[1]))));bound=(16./3.)*(dual_norm+roundoff)
 for n,x in (('known_auxiliary_error_norm',error_norm),('original_dual_residual_norm',dual_norm),('uncancelled_dual_operation_envelope',uncancelled),('disclosed_roundoff_allowance',roundoff),('coercive_nodal_error_bound',bound)):keep(label+'_'+n,np.asarray(x).copy())
 assert meta['cap']==3 and meta['restarts']==0 and meta['self_adjointness_assumed'] is False and meta['iterations']<=3 and after['admitted'] and bound>0
 rows=after['scores'];P.check(label+'_original_six_rows_and_independent_known_answer',np.concatenate((rows.ravel(),np.asarray((error_norm,)))),np.zeros(7),np.concatenate((np.full(6,P.LINEAR_TOL/P.TOL),np.asarray((bound/P.TOL,)))))
 assert len(P.CHECKS)-before==5
 return dict(kind='NEW_nonsymmetric_anisotropic_cap3_paired_GMRES_known_answer',solver=meta,controls=5,native_RHS_zero_relative_score=None,native_inherited_reference_norms=(1.,2.),metric_RHS_nonzero=True,original_row_tolerance=P.LINEAR_TOL,symmetric_part_lower=3./16.,coercive_inverse_bound=16./3.,known_auxiliary_error=error_norm,disclosed_roundoff_allowance=roundoff,coercive_nodal_error_bound=bound,operator_or_factor_or_old_fixture_replayed=False,physical_adoption=False)
