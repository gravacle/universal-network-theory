# Definitions only: unchanged paired York action, warm nodes and original targets.
# Q/P/np/keep supplied by the guarded caller; no imports or calls here.
YORK_BLOCK_SOLVER_AUTHOR_DRAFT=True

def york_block_embed(value,indices,size):
 out=np.zeros(size);out[indices]=value;return out

def york_block_update(start,delta,indices,label):
 # Keep the inactive node words bit-identical; update only the selected block.
 selected=(start[0][indices],start[1][indices]);part,q=P.dd_node_update(selected,delta,keep,label)
 out=(start[0].copy(),start[1].copy());out[0][indices]=part[0];out[1][indices]=part[1]
 fullq=york_block_embed(q,indices,len(start[0]));Q.york_pair_keep(label+'_full_updated_nodes',out,keep);keep(label+'_full_compression_word',fullq)
 return out,fullq

def york_block_increment(start,before,scale,indices,rows,action,certificate,sufficient,label,cap):
 assert 1<=cap<=160 and sufficient>0 and np.all(scale>0)
 rhs_pair=tuple(v[indices] for v in before['residual']);rhs=rhs_pair[0]+rhs_pair[1]
 keep(label+'_correction_rhs_binary64',rhs);Q.york_pair_keep(label+'_correction_rhs_readout_defect',P.a_sub(rhs_pair,P.a_dd(rhs)),keep)
 white=float(np.linalg.norm(rhs/scale[indices]));assert white>0
 tolerance=min(.1,max(np.finfo(float).tiny,sufficient/white));keep(label+'_relative_recurrence_target',np.asarray(tolerance))
 def A(delta):
  full=york_block_embed(delta,indices,len(start[0]));value=action(P.a_dd(full),label+'_iterative_action');return value[0][indices]+value[1][indices]
 def original_rows(delta):
  trial,q=york_block_update(start,delta,indices,label+'_callback_update');answer=certificate(trial,label+'_callback')
  return answer['residual'][0][indices]+answer['residual'][1][indices],answer['ratios'][rows]
 delta,ratios,admitted,reason=P.minres_core(A,rhs,scale[indices],tolerance,original_rows,label,cap=cap)
 keep(label+'_completed_block_correction',delta);keep(label+'_solver_return_ratios',ratios)
 nodes,q=york_block_update(start,delta,indices,label+'_final_update');answer=certificate(nodes,label+'_updated')
 full=york_block_embed(delta,indices,len(start[0]));keep(label+'_completed_full_correction',full)
 return nodes,q,answer,full,dict(reason=reason,return_admitted=admitted,return_ratios=ratios.tolist(),cap=cap)

def york_support_measurement(d):
 phi=np.zeros((3,3),bool);phi[0,2]=phi[2,0]=phi[1,2]=phi[2,1]=True
 counts=[];maxima=[]
 for word in d['maps']:
  bad=np.concatenate((word[:,:2,:,:, :][...,phi].ravel(),word[:,2,:,:,:][...,~phi].ravel()))
  counts.append(np.count_nonzero(bad));maxima.append(np.max(abs(bad),initial=0))
 keep('incompatible_cross_component_map_word_counts',np.asarray(counts,dtype=np.int64));keep('incompatible_cross_component_map_word_maxima',np.asarray(maxima))
 assert counts==[0,0],'Block split requires exact disjoint support in both saved map words'
 ih=d['ih'];off=~np.eye(3,dtype=bool);assert np.all(ih[:,off]==0)
 diagonal=np.diagonal(ih,axis1=1,axis2=2);assert np.all(diagonal>0) and np.all(d['sqrt_h']>0)
 weights=d['sqrt_h'][:,None,None]*diagonal[:,:,None]*diagonal[:,None,:];keep('positive_serialized_tensor_pairing_weights',weights);assert np.all(weights>0)
 return dict(both_word_cross_component_support_exact_zero=True,positive_diagonal_inverse_tensor_pairing=True,split_groups=['R_Z','phi'],support_measurement_is_operator_replay=False)

def york_block_sufficient_targets(rhs,scale):
 cuts=(0,3740,7395,11135);norms=np.asarray([(np.linalg.norm(rhs[cuts[i]:cuts[i+1]]),np.linalg.norm(rhs[cuts[i]:cuts[i+1]]/scale[cuts[i]:cuts[i+1]])) for i in range(3)])
 targets=1e-10*np.asarray([min(norms[i,0]/float(np.max(scale[cuts[i]:cuts[i+1]])),norms[i,1]) for i in range(3)])
 keep('original_component_rhs_norms',norms);keep('original_component_sufficient_white_targets',targets);assert np.all(targets>0)
 return targets

def york_fresh_block_control():
 # A has coupled R/Z entries, a separate phi block and lambda_min(A)>1.
 A=np.asarray(((2.,1.,0.),(1.,3.,0.),(0.,0.,5.)));expected=np.asarray((1.,2.,3.));rhs=np.asarray((4.,7.,15.));scale=np.sqrt(np.asarray((2.,3.,5.)))
 nodes=(np.asarray((.5,-.5,1.25)),np.asarray((2.**-55,-2.**-54,2.**-56)))
 for name,value in (('matrix',A),('expected_nodes',expected),('original_rhs',rhs),('positive_scale',scale)):keep('fresh_block_'+name,value)
 Q.york_pair_keep('fresh_block_warm_nodes',nodes,keep)
 def action(x,label):
  value=P.a_matvec(A,x);Q.york_pair_keep(label+'_paired_action',value,keep);return value
 def certificate(x,label):
  value=action(x,label);res=P.a_sub(P.a_dd(rhs),value);ratios=np.stack([P.original_ratios((res[0]+res[1])[i:i+1],rhs[i:i+1],scale[i:i+1]) for i in range(3)])
  Q.york_pair_keep(label+'_original_residual',res,keep);keep(label+'_original_component_ratios',ratios);return dict(action=value,residual=res,ratios=ratios,admitted=bool(np.all(ratios<=1e-10)))
 current=certificate(nodes,'fresh_block_initial');history=[]
 for name,indices,rows in (('R_Z',np.arange(2),np.asarray((0,1))),('phi',np.asarray((2,)),np.asarray((2,)))):
  sufficient=1e-10*min(min(abs(rhs[i])/scale[i],abs(rhs[i]/scale[i])) for i in rows)
  nodes,q,current,delta,solver=york_block_increment(nodes,current,scale,indices,rows,action,certificate,sufficient,'fresh_block_'+name,8)
  history.append(solver)
 Q.york_pair_keep('fresh_block_final_nodes',nodes,keep);keep('fresh_block_final_component_ratios',current['ratios'])
 error=float(np.linalg.norm(nodes[0]+nodes[1]-expected));resnorm=float(np.linalg.norm(current['residual'][0]+current['residual'][1]))
 rounding=64*np.finfo(float).eps*(np.linalg.norm(expected)+np.linalg.norm(nodes[0])+np.linalg.norm(nodes[1])+np.linalg.norm(rhs));bound=resnorm+rounding
 keep('fresh_block_solution_error_and_coercive_bound',np.asarray((error,resnorm,rounding,bound)))
 P.check('fresh_block_normalized_warm_original_rows_and_coercive_error',np.asarray((float(current['admitted']),max(0.,error-bound))),np.asarray((1.,0.)),np.ones(2))
 return dict(kind='fresh_coupled_RZ_and_separate_phi_warm_MINRES_control',cap_per_group=8,groups=history,original_row_tolerance=1e-10,coercive_eigenvalue_lower_bound=1.,independent_solution_error_bound=bound,no_York_fixture_or_physical_state_replayed=True)

def york_measure_block_corrections(nodes,current,d):
 targets=d['sufficient_component_targets'];records=[]
 action=lambda x,label:Q.york_packed_action(x,d,label)[0]
 certificate=lambda x,label:Q.york_original_certificate(x,d,label)
 for group,indices,rows in (('R_Z',np.arange(7395),np.asarray((0,1))),('phi',np.arange(7395,11135),np.asarray((2,)))):
  if np.all(current['ratios'][rows]<=1e-10):continue
  label='block_york_'+group;start=nodes;before=current
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage='new_block_normalized_york_correction',group=group)
  Q.york_pair_keep(label+'_before_nodes',start,keep);Q.york_pair_keep(label+'_before_action',before['action'],keep);Q.york_pair_keep(label+'_before_residual',before['residual'],keep);keep(label+'_before_component_ratios',before['ratios']);keep(label+'_active_indices',indices);keep(label+'_active_component_rows',rows)
  sufficient=float(np.min(targets[rows]));keep(label+'_sufficient_original_white_target',np.asarray(sufficient))
  nodes,q,current,delta,solver=york_block_increment(start,before,d['scale'],indices,rows,action,certificate,sufficient,label,160)
  adelta=action(P.a_dd(delta),label+'_correction_action');aq=action(P.a_dd(q),label+'_compression_action')
  gap=P.a_sub(P.a_add(P.a_sub(current['residual'],before['residual']),adelta),aq);Q.york_pair_keep(label+'_original_residual_update_identity',gap,keep)
  envelope=2*d['rhs_envelope']
  for suffix,value in (('before',start),('after',nodes),('delta',P.a_dd(delta)),('compression',P.a_dd(q))):envelope=envelope+Q.york_packed_envelope(value,d,label+'_'+suffix)
  keep(label+'_residual_update_operation_envelope',envelope);P.check(label+'_paired_original_residual_update_identity',gap[0]+gap[1],np.zeros(11135),envelope)
  record=P.checkpoint('BLOCK',arrays(),dict(kind='new_block_normalized_warm_York_correction',group=group,cap=160,solver=solver,original_rows_admitted=current['admitted'],original_component_ratios=current['ratios'].tolist(),controls=P.CHECKS[-1:],same_original_targets_and_operator=True,physical_TT_prepared=False));records.append(record)
 return nodes,current,records
