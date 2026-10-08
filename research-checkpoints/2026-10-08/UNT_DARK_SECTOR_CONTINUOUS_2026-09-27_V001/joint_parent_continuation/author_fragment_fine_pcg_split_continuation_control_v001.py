# Definitions only; globals np/P/Q/keep/fine_paired_pcg. NEW fixture, no old replay.
def fresh_fine_pcg_split_continuation_control():
 A=np.asarray(((17/4,1/2,0.),(1/2,5/4,1/2),(0.,1/2,1.)));G=np.asarray(((2.,0.,0.),(1/2,1.,0.),(0.,1/2,1.)))
 target=np.asarray((1.,-2.,3.));rhs=np.asarray((13/4,-1/2,2.));scale=np.ones(3)
 for n,x in (('A',A),('G',G),('independent_target',target),('independent_RHS',rhs)):keep('fresh_split_'+n,x)
 def action(x,label):
  y=P.a_matvec(A,x);Q.york_pair_keep(label+'_action',y,keep);gx=P.a_matvec(G,x);Q.york_pair_keep(label+'_Gx',gx,keep)
  energy=Q.york_pair_reduce(P.a_mul(gx,gx));Q.york_pair_keep(label+'_energy',energy,keep);ex=abs(x[0])+abs(x[1]);env=abs(A)@ex;eb=np.asarray(np.sum((abs(G)@ex)**2));keep(label+'_envelope',env);keep(label+'_energy_envelope',eb)
  return dict(action=y,envelope=env,energy=energy,energy_envelope=eb)
 def certificate(x,label):
  a=action(x,label);r=P.a_sub(P.a_dd(rhs),a['action']);Q.york_pair_keep(label+'_residual',r,keep)
  ratios=np.stack([P.original_ratios((r[0]+r[1])[i:i+1],rhs[i:i+1],scale[i:i+1]) for i in range(3)]);keep(label+'_ratios',ratios)
  env=abs(rhs)+a['envelope'];keep(label+'_residual_envelope',env)
  return dict(action=a['action'],residual=r,ratios=ratios,global_ratios=P.original_ratios(r[0]+r[1],rhs,scale),admitted=bool(np.all(ratios<=1e-10)),residual_envelope=env)
 def precondition(r,label):
  z=P.a_dd(r[0]+r[1]);Q.york_pair_keep(label+'_identity_binary64_preconditioner',z,keep);return z
 def cached(label,n):return tuple(P.AVAILABLE[label+n+'_'+w].copy() for w in ('hi','lo'))
 start=P.a_dd(np.zeros(3));initial=certificate(start,'fresh_split_initial')
 full,last,whole=fine_paired_pcg(start,initial,action,precondition,certificate,'fresh_split_uninterrupted',6)
 Q.york_pair_keep('fresh_split_completed_uninterrupted_nodes',full,keep);Q.york_pair_keep('fresh_split_completed_uninterrupted_residual',last['residual'],keep)
 first,mid,part=fine_paired_pcg(start,initial,action,precondition,certificate,'fresh_split_prefix',1)
 assert part['iterations']==1 and not mid['admitted'] and part['reason']=='iteration_cap'
 state=dict(recursive_residual=cached('fresh_split_prefix','_recursive_residual'),z=cached('fresh_split_prefix','_preconditioned_residual'),rz=cached('fresh_split_prefix','_rz'),rho=float(P.AVAILABLE['fresh_split_prefix_current_rz_inner_binary64_readout']),direction=cached('fresh_split_prefix','_search_direction'),previous_direction=cached('fresh_split_prefix','_previous_search_direction'),previous_result=dict(action=cached('fresh_split_prefix','_previous_Ap'),envelope=P.AVAILABLE['fresh_split_prefix_direction_action_envelope'].copy()))
 Q.york_pair_keep('fresh_split_carried_original_residual',mid['residual'],keep)
 resumed,end,suffix=fine_paired_pcg(first,mid,action,precondition,certificate,'fresh_split_suffix',5,continuation=state)
 assert all(np.array_equal(full[w],resumed[w]) and np.array_equal(last['residual'][w],end['residual'][w]) for w in (0,1)),'Split continuation must retain both exact recurrence words'
 assert whole['iterations']==part['iterations']+suffix['iterations'] and last['admitted'] and end['admitted']
 Q.york_pair_keep('fresh_split_final_nodes',resumed,keep);error=float(np.linalg.norm(resumed[0]+resumed[1]-target));rn=float(np.linalg.norm(end['residual'][0]+end['residual'][1]));rounding=64*np.finfo(float).eps*(np.linalg.norm(target)+np.linalg.norm(resumed[0])+np.linalg.norm(resumed[1])+np.linalg.norm(rhs));bound=4*rn+rounding
 keep('fresh_split_known_error_residual_rounding_bound',np.asarray((error,rn,rounding,bound)))
 P.check('NEW_split_recurrence_exact_words_and_known_solution',np.asarray((float(end['admitted']),max(0.,error-bound))),np.asarray((1.,0.)),np.ones(2))
 return dict(kind='NEW_explicit_1_plus_5_vs_6_step_paired_PCG_continuation_known_solution',prefix=part,suffix=suffix,uninterrupted=whole,fine_Gershgorin_eigenvalue_lower_bound=1/4,both_final_node_and_residual_words_exact=True,independent_known_solution_bound=bound,old_fixture_or_original_action_replayed=False,physical_adoption=False)
