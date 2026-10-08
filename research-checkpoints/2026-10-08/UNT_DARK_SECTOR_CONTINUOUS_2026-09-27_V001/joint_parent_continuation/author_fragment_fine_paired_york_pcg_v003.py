# DEFINITIONS ONLY. Globals np/P/Q/C/keep/arrays; no author evaluation.
# Fine physical action remains authoritative; B=TT* is only a preconditioner.
FINE_PCG_AUTHOR_DRAFT=True

def fine_pcg_inner(x,y,label):
 prod=P.a_mul(x,y);value=Q.york_pair_reduce(prod);Q.york_pair_keep(label+'_paired_inner_product',value,keep)
 envelope=np.asarray(np.sum((abs(x[0])+abs(x[1]))*(abs(y[0])+abs(y[1]))));keep(label+'_inner_operation_envelope',envelope)
 readout=float(value[0]+value[1]);keep(label+'_inner_binary64_readout',np.asarray(readout));Q.york_pair_keep(label+'_inner_readout_defect',P.a_sub(value,P.a_dd(np.asarray(readout))),keep)
 assert np.isfinite(readout) and np.isfinite(envelope) and envelope>=0
 return value,readout,envelope

def fine_pcg_update(nodes,delta,label):
 # Each word is inserted separately. Exact increment minus newpair is q_hi+q_lo.
 Q.york_pair_keep(label+'_old_nodes',nodes,keep);Q.york_pair_keep(label+'_paired_increment',delta,keep)
 middle,qh=P.dd_node_update(nodes,delta[0],keep,label+'_high_word');Q.york_pair_keep(label+'_middle_nodes',middle,keep);keep(label+'_high_compression',qh)
 updated,ql=P.dd_node_update(middle,delta[1],keep,label+'_low_word');Q.york_pair_keep(label+'_updated_nodes',updated,keep);keep(label+'_low_compression',ql)
 compression=P.a_add(P.a_dd(qh),P.a_dd(ql));Q.york_pair_keep(label+'_total_compression',compression,keep)
 return updated,compression

def fine_pcg_construction(direction,result,old_direction,old_result,label):
 curvature,cvalue,cb=fine_pcg_inner(direction,result['action'],label+'_curvature')
 energy=result['energy'];Q.york_pair_keep(label+'_independent_point_energy',energy,keep)
 gap=P.a_sub(curvature,energy);Q.york_pair_keep(label+'_curvature_minus_point_energy',gap,keep)
 bound=np.asarray(np.sum((abs(direction[0])+abs(direction[1]))*result['envelope'])+result['energy_envelope']);keep(label+'_curvature_energy_envelope',bound)
 contacts=[(float(gap[0]+gap[1]),float(bound))]
 if old_direction is not None:
  left,lv,lb=fine_pcg_inner(old_direction,result['action'],label+'_adjoint_left');right,rv,rb=fine_pcg_inner(direction,old_result['action'],label+'_adjoint_right')
  agap=P.a_sub(left,right);Q.york_pair_keep(label+'_successive_direction_adjoint_gap',agap,keep)
  ab=np.asarray(np.sum((abs(old_direction[0])+abs(old_direction[1]))*result['envelope'])+np.sum((abs(direction[0])+abs(direction[1]))*old_result['envelope']));keep(label+'_adjoint_construction_envelope',ab);contacts.append((float(agap[0]+agap[1]),float(ab)))
 else:contacts.append((0.,0.))
 return cvalue,contacts

def fine_paired_pcg(nodes,current,action,precondition,certificate,label,cap,snapshots=(),initial=None):
 # Generic paired loop used by BOTH the new artificial control and actual York.
 # No automatic residual replacement or restart; fresh certificates own admission.
 assert 1<=cap<=512 and all(1<=k<=cap for k in snapshots)
 start=nodes;before=current;r=current['residual'];old_direction=old_result=None;history=[];worst=np.zeros((3,2));reason='iteration_cap'
 Q.york_pair_keep(label+'_start_nodes',nodes,keep);Q.york_pair_keep(label+'_start_original_residual',r,keep)
 def contact(slot,value,bound):
  assert np.isfinite(value) and np.isfinite(bound) and bound>=0
  error=abs(value)/max(bound,1e-30)
  if error>=abs(worst[slot,0])/max(worst[slot,1],1e-30):worst[slot]=value,bound
  keep(label+'_worst_construction_actual_and_envelope',worst);assert error<=2e-11,(slot,error)
 if current['admitted']:reason='original_rows_already_admitted';iteration=0
 else:
  if initial is None:
   z=precondition(r,label+'_initial_preconditioner');Q.york_pair_keep(label+'_preconditioned_residual',z,keep)
   rz,rho,re=fine_pcg_inner(r,z,label+'_initial_rz');Q.york_pair_keep(label+'_rz',rz,keep);direction=z
  else:
   z,rz,rho,direction=(initial[n] for n in ('z','rz','rho','direction'));assert np.isfinite(rho)
   Q.york_pair_keep(label+'_preconditioned_residual',z,keep);Q.york_pair_keep(label+'_rz',rz,keep)
  Q.york_pair_keep(label+'_search_direction',direction,keep)
  for iteration in range(1,cap+1):
   P.CONTEXT.update(stage='new_fine_paired_PCG',iteration=iteration,cap=cap)
   Q.york_pair_keep(label+'_current_nodes',nodes,keep);Q.york_pair_keep(label+'_recursive_residual',r,keep);Q.york_pair_keep(label+'_search_direction',direction,keep)
   result=initial['first_action'](label+'_direction_action') if initial is not None and iteration==1 else action(direction,label+'_direction_action');Q.york_pair_keep(label+'_Ap',result['action'],keep)
   curvature,contacts=fine_pcg_construction(direction,result,old_direction,old_result,label+'_construction')
   contact(0,*contacts[0]);contact(1,*contacts[1]);keep(label+'_rho_and_curvature',np.asarray((rho,curvature)))
   if rho<=0 or curvature<=0:
    reason='nonpositive_or_null_numerical_curvature_with_unadmitted_original_rows';break
   alpha=rho/curvature;keep(label+'_alpha',np.asarray(alpha));assert np.isfinite(alpha)
   delta=P.a_mul64(alpha,direction);Q.york_pair_keep(label+'_completed_paired_increment',delta,keep)
   Q.york_pair_keep(label+'_before_update_original_residual',current['residual'],keep)
   Q.york_pair_keep(label+'_before_update_recursive_residual',r,keep)
   old_nodes=nodes;old_current=current;updated,q=fine_pcg_update(nodes,delta,label+'_node_update')
   aq=action(q,label+'_compression_action');Q.york_pair_keep(label+'_compression_original_action',aq['action'],keep)
   alpha_ap=P.a_mul64(alpha,result['action']);Q.york_pair_keep(label+'_alpha_Ap',alpha_ap,keep)
   rnew=P.a_add(P.a_sub(r,alpha_ap),aq['action']);Q.york_pair_keep(label+'_new_recursive_residual',rnew,keep)
   fresh=certificate(updated,label+'_fresh_original');Q.york_pair_keep(label+'_fresh_original_residual',fresh['residual'],keep);keep(label+'_fresh_original_ratios',fresh['ratios'])
   gap=P.a_sub(P.a_add(P.a_sub(fresh['residual'],old_current['residual']),alpha_ap),aq['action']);Q.york_pair_keep(label+'_original_residual_update_contact',gap,keep)
   envelope=old_current['residual_envelope']+fresh['residual_envelope']+abs(alpha)*result['envelope']+aq['envelope'];keep(label+'_original_update_contact_envelope',envelope)
   e=np.abs(gap[0]+gap[1])/np.maximum(envelope,1e-30);index=int(np.argmax(e));contact(2,float(gap[0][index]+gap[1][index]),float(envelope[index]))
   drift=P.a_sub(fresh['residual'],rnew);Q.york_pair_keep(label+'_fresh_minus_recursive_residual',drift,keep)
   drift_norm=float(np.linalg.norm(drift[0]+drift[1]));keep(label+'_recursive_drift_norm',np.asarray(drift_norm))
   nodes=updated;current=fresh;r=rnew;Q.york_pair_keep(label+'_current_nodes',nodes,keep);Q.york_pair_keep(label+'_recursive_residual',r,keep)
   history.append((iteration,*current['ratios'].ravel(),rho,curvature,alpha,drift_norm));keep(label+'_history',np.asarray(history))
   if iteration in snapshots:
    P.checkpoint('ITERATION',arrays(),dict(kind='unqualified_fine_PCG_paired_iterate',iteration=iteration,cap=cap,original_component_ratios=current['ratios'].tolist(),recursive_residual_is_not_admission=True,physical_adoption=False))
   if current['admitted']:reason='fresh_original_rows_admitted';break
   old_direction=direction;old_result=result;Q.york_pair_keep(label+'_previous_search_direction',old_direction,keep);Q.york_pair_keep(label+'_previous_Ap',old_result['action'],keep)
   z=precondition(r,label+'_current_preconditioner');Q.york_pair_keep(label+'_preconditioned_residual',z,keep)
   newrz,newrho,re=fine_pcg_inner(r,z,label+'_current_rz');Q.york_pair_keep(label+'_rz',newrz,keep)
   if newrho<=0:rho=newrho;reason='nonpositive_preconditioned_residual_with_unadmitted_original_rows';break
   beta=newrho/rho;keep(label+'_beta',np.asarray(beta));assert np.isfinite(beta)
   direction=P.a_add(z,P.a_mul64(beta,direction));Q.york_pair_keep(label+'_search_direction',direction,keep);rho=newrho
 keep(label+'_iterations_completed',np.asarray(iteration,dtype=np.int64));keep(label+'_history',np.asarray(history,dtype=np.float64).reshape(-1,11));keep(label+'_worst_construction_actual_and_envelope',worst)
 P.check(label+'_energy_adjoint_and_original_update_construction',worst[:,0],np.zeros(3),worst[:,1])
 return nodes,current,dict(cap=cap,iterations=iteration,reason=reason,original_component_ratios=current['ratios'].tolist(),all_original_rows_admitted=current['admitted'],recursive_residual_replaced=False,automatic_restart=False,potential_error_bound_claimed=False)

def york_fine_pcg_action(x,d,label):
 value,L,density=Q.york_packed_action(x,d,label)
 Q.york_pair_keep(label+'_completed_action',value,keep)
 field=(Q.york_unpack(x[0]),Q.york_unpack(x[1]));env,eL,ed=Q.york_action_envelope(field,d['map_envelope'],d['ih'],d['sqrt_h'],d['geometry'],keep,label+'_positive')
 weight=(d['geometry']['dv']/d['geometry']['R']).reshape(15136)
 energy=fine_pcg_weighted_energy(L,density,weight,label)
 energy_envelope=np.asarray(np.sum(weight[:,None,None]*eL*ed));keep(label+'_point_energy_operation_envelope',energy_envelope)
 return dict(action=value,envelope=Q.york_pack(env),energy=energy,energy_envelope=energy_envelope)

def york_fine_pcg_precondition(r,pre,label):
 value=r[0]+r[1];keep(label+'_binary64_residual',value);Q.york_pair_keep(label+'_residual_readout_defect',P.a_sub(r,P.a_dd(value)),keep)
 adjoint=C.york_twolevel_adjoint(value,pre,label+'_adjoint');keep(label+'_completed_extended_preconditioner_coordinate',adjoint)
 z=C.york_twolevel_forward(adjoint,pre,label+'_forward');keep(label+'_completed_fine_preconditioned_residual',z);return P.a_dd(z)

def york_fine_pcg_certificate(nodes,d,label):
 current=Q.york_original_certificate(nodes,d,label)
 env=d['rhs_envelope']+Q.york_packed_envelope(nodes,d,label+'_positive');keep(label+'_original_residual_operation_envelope',env);current['residual_envelope']=env;return current

def york_fine_pcg_warm(nodes,current,d,pre,label,cap=512,initial=None):
 # The supplied original action/residual is reused; only its positive bound is new.
 current=dict(current);current['residual_envelope']=d['rhs_envelope']+Q.york_packed_envelope(nodes,d,label+'_start_positive') if initial is None else initial['start_residual_envelope']
 keep(label+'_start_original_residual_envelope',current['residual_envelope'])
 return fine_paired_pcg(nodes,current,lambda x,l:york_fine_pcg_action(x,d,l),lambda r,l:york_fine_pcg_precondition(r,pre,l),lambda x,l:york_fine_pcg_certificate(x,d,l),label,cap,(64,128,256,512),initial)

def fresh_fine_pcg_control():
 # Coupled anisotropic dyadic A=G^T G. Gershgorin lambda_min>7/16.
 A=np.asarray(((65537./65536.,.5,1./16.),(.5,65./4.,4.),(1./16.,4.,257.)));G=np.asarray(((1.,.5,0.),(0.,4.,1.),(1./256.,0.,16.)))
 target=np.asarray((1.,-2.,3.));rhs=np.asarray((12289./65536.,-20.,12209./16.));scale=np.asarray((2.,3.,4.));I=np.asarray(((1.,0.),(.5,1.),(0.,.5)));L=np.asarray(((2.,0.),(.5,1.)))
 for n,v in (('A',A),('G',G),('exact_target',target),('independent_rhs',rhs),('scale',scale),('I',I),('L',L)):keep('fresh_fine_PCG_'+n,v)
 pre=dict(fine_scale=scale,coarse_scale=np.asarray((1.,2.)),coarse_factor=L,prolong=lambda x:I@x,adjoint=lambda x:I.T@x)
 def action(x,label):
  y=P.a_matvec(A,x);Q.york_pair_keep(label+'_action',y,keep);gx=P.a_matvec(G,x);Q.york_pair_keep(label+'_independent_Gx',gx,keep)
  energy=Q.york_pair_reduce(P.a_mul(gx,gx));Q.york_pair_keep(label+'_independent_energy',energy,keep)
  ex=abs(x[0])+abs(x[1]);env=abs(A)@ex;eb=np.asarray(np.sum((abs(G)@ex)**2));keep(label+'_envelope',env);keep(label+'_energy_envelope',eb);return dict(action=y,envelope=env,energy=energy,energy_envelope=eb)
 def certificate(x,label):
  a=action(x,label);res=P.a_sub(P.a_dd(rhs),a['action']);Q.york_pair_keep(label+'_residual',res,keep)
  ratios=np.stack([P.original_ratios((res[0]+res[1])[i:i+1],rhs[i:i+1],scale[i:i+1]) for i in range(3)]);keep(label+'_ratios',ratios)
  return dict(action=a['action'],residual=res,ratios=ratios,global_ratios=P.original_ratios(res[0]+res[1],rhs,scale),admitted=bool(np.all(ratios<=1e-10)),residual_envelope=abs(rhs)+a['envelope'])
 start=(np.asarray((.25,.5,-.25)),np.asarray((2.**-55,-2.**-54,2.**-56)));current=certificate(start,'fresh_fine_PCG_start')
 nodes,last,meta=fine_paired_pcg(start,current,action,lambda r,l:york_fine_pcg_precondition(r,pre,l),certificate,'fresh_fine_PCG',12)
 error=float(np.linalg.norm(nodes[0]+nodes[1]-target));resnorm=float(np.linalg.norm(last['residual'][0]+last['residual'][1]));rounding=64*np.finfo(float).eps*(np.linalg.norm(target)+np.linalg.norm(nodes[0])+np.linalg.norm(nodes[1])+np.linalg.norm(rhs));bound=(16./7.)*resnorm+rounding
 keep('fresh_fine_PCG_nodal_error_residual_rounding_bound',np.asarray((error,resnorm,rounding,bound)));Q.york_pair_keep('fresh_fine_PCG_final_nodes',nodes,keep)
 P.check('fresh_coupled_anisotropic_fine_PCG_original_rows_and_error_bound',np.asarray((float(last['admitted']),max(0.,error-bound))),np.asarray((1.,0.)),np.ones(2))
 return dict(kind='fresh_coupled_anisotropic_fine_PCG_with_same_generic_loop',cap=12,original_ratios=last['ratios'].tolist(),original_rows_admitted=last['admitted'],fine_eigenvalue_lower_bound=7./16.,independent_error_bound=bound,solver=meta,old_York_or_twolevel_fixture_replayed=False)

def fine_pcg_weighted_energy(L,density,weight,label):
 # Weight is applied before L*density, keeping each protected operand admitted.
 keep(label+'_positive_geometric_weight',weight)
 weighted=P.a_mul64(weight[:,None,None],L);Q.york_pair_keep(label+'_weighted_longitudinal',weighted,keep)
 products=P.a_mul(weighted,density);Q.york_pair_keep(label+'_weighted_point_energy_products',products,keep)
 energy=Q.york_pair_reduce(products);Q.york_pair_keep(label+'_point_energy',energy,keep)
 return energy

def fine_pcg_cached_direction_action(cache,d,label):
 # Exact completed first action/tensors/positive bounds from failed V006 only.
 for n in ('action','L','density'):Q.york_pair_keep(label+'_reused_'+n,cache[n],keep)
 for n in ('envelope','L_envelope','density_envelope'):keep(label+'_reused_'+n,cache[n])
 weight=(d['geometry']['dv']/d['geometry']['R']).reshape(15136)
 energy=fine_pcg_weighted_energy(cache['L'],cache['density'],weight,label)
 energy_envelope=np.asarray(np.sum(weight[:,None,None]*cache['L_envelope']*cache['density_envelope']));keep(label+'_point_energy_operation_envelope',energy_envelope)
 return dict(action=cache['action'],envelope=cache['envelope'],energy=energy,energy_envelope=energy_envelope)

def fresh_reassociated_weighted_energy_control():
 L=P.a_dd(np.asarray([[[2.**-240]]]));density=P.a_dd(np.asarray([[[2.**-215]]]));weight=np.asarray((2.**20,));expected=np.asarray(2.**-435)
 for n,x in (('L',L),('density',density)):Q.york_pair_keep('fresh_reassociated_'+n,x,keep)
 keep('fresh_reassociated_weight',weight);keep('fresh_reassociated_exact_expected',expected)
 energy=fine_pcg_weighted_energy(L,density,weight,'fresh_reassociated')
 assert np.array_equal(energy[0],expected) and np.all(energy[1]==0),'Tiny dyadic product requires exact words, not a denominator-floor pass'
 normalized=np.asarray((energy[0]+energy[1])/expected);keep('fresh_reassociated_exact_normalized_energy',normalized)
 P.check('fresh_reassociated_tiny_weighted_energy_exact_words',normalized,np.asarray(1.),np.asarray(1.))
 return dict(kind='new_exact_dyadic_weighted_energy_association',old_unweighted_product_exponent=-455,exact_weighted_energy_exponent=-435,exact_words_required=True,old_fixture_replayed=False)
