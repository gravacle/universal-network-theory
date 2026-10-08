# Guarded new W solve definitions. np,P,keep,thin and reviewed York functions supplied.
# Frozen maps/source/diagonal; only the auxiliary potential changes numerically.
YORK_SOLVER_AUTHOR_DRAFT=True

def york_pack(x):return x[york_vector_mask()]

def york_unpack(x):
 assert x.shape==(11135,);out=np.zeros((3,87,45));out[york_vector_mask()]=x;return out

def york_packed_action(x,d,label):
 field=(york_unpack(x[0]),york_unpack(x[1]))
 action,L,density=york_mass_action(field,d['maps'],d['ih'],d['sqrt_h'],d['geometry'],keep,label)
 return (york_pack(action[0]),york_pack(action[1])),L,density

def york_packed_envelope(x,d,label):
 field=(york_unpack(x[0]),york_unpack(x[1]))
 env,eL,ed=york_action_envelope(field,d['map_envelope'],d['ih'],d['sqrt_h'],d['geometry'],keep,label)
 return york_pack(env)

def york_component_ratios(residual,rhs,scale):
 assert residual.shape==rhs.shape==scale.shape==(11135,)
 cuts=(0,3740,7395,11135)
 return np.stack([P.original_ratios(residual[cuts[i]:cuts[i+1]],rhs[cuts[i]:cuts[i+1]],scale[cuts[i]:cuts[i+1]]) for i in range(3)])

def york_original_certificate(x,d,label):
 action,L,density=york_packed_action(x,d,label)
 residual=P.a_sub(d['rhs'],action)
 york_pair_keep(label+'_original_action',action,keep);york_pair_keep(label+'_original_residual',residual,keep)
 ratios=york_component_ratios(residual[0]+residual[1],d['rhs'][0]+d['rhs'][1],d['scale']);keep(label+'_original_raw_scaled_ratios',ratios)
 global_ratios=P.original_ratios(residual[0]+residual[1],d['rhs'][0]+d['rhs'][1],d['scale']);keep(label+'_original_global_ratios',global_ratios)
 assert np.all(np.isfinite(ratios))
 return dict(action=action,residual=residual,ratios=ratios,global_ratios=global_ratios,admitted=bool(np.all(ratios<=1e-10)),longitudinal=L,density=density)

def york_measure_and_solve(d,max_cycles,cap):
 assert 1<=max_cycles<=3 and 1<=cap<=160
 nodes=P.a_dd(np.zeros(11135));initial=york_original_certificate(nodes,d,'initial_york')
 rhs0=d['rhs'][0]+d['rhs'][1];rawnorm=float(np.linalg.norm(rhs0));whitenorm=float(np.linalg.norm(rhs0/d['scale']))
 keep('original_rhs_norms',np.array((rawnorm,whitenorm)))
 cuts=(0,3740,7395,11135);component_norms=np.array([(np.linalg.norm(rhs0[cuts[i]:cuts[i+1]]),np.linalg.norm(rhs0[cuts[i]:cuts[i+1]]/d['scale'][cuts[i]:cuts[i+1]])) for i in range(3)])
 keep('original_rhs_component_norms',component_norms)
 sufficient=1e-10*min(min(component_norms[i,0]/float(np.max(d['scale'][cuts[i]:cuts[i+1]])),component_norms[i,1]) for i in range(3))
 keep('sufficient_original_white_target',np.array(sufficient));york_pair_keep('initial_original_rhs',d['rhs'],keep);keep('initial_original_positive_scale',d['scale'])
 P.checkpoint('INITIAL',{**P.AVAILABLE,**P.RAW},dict(kind='new_zero_potential_original_York_certificate',input_ref=thin(d['input_ref']),original_rows_admitted=initial['admitted'],original_ratios=initial['ratios'].tolist(),original_global_ratios=initial['global_ratios'].tolist(),physical_TT_prepared=False))
 cycles=[];current=initial
 for cycle in range(1,max_cycles+1):
  if current['admitted']:break
  label='york_cycle_%03d'%cycle;start=nodes;before=current
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage='new_compact_york_correction',cycle=cycle)
  york_pair_keep(label+'_before_nodes',start,keep);york_pair_keep(label+'_before_action',before['action'],keep);york_pair_keep(label+'_before_residual',before['residual'],keep);keep(label+'_before_ratios',before['ratios'])
  correction_rhs=before['residual'][0]+before['residual'][1]
  keep(label+'_solver_rhs_binary64',correction_rhs)
  readout_defect=P.a_sub(before['residual'],P.a_dd(correction_rhs));york_pair_keep(label+'_solver_rhs_readout_defect',readout_defect,keep)
  white=float(np.linalg.norm(correction_rhs/d['scale']));assert white>0
  tolerance=min(.1,max(np.finfo(float).tiny,sufficient/white));keep(label+'_relative_recurrence_target',np.array(tolerance))
  def iteration_action(delta):
   action,_,_=york_packed_action(P.a_dd(delta),d,label+'_iterative_action')
   return action[0]+action[1]
  def original_rows(delta):
   trial,q=P.dd_node_update(start,delta,keep,label+'_callback_update')
   answer=york_original_certificate(trial,d,label+'_callback')
   return answer['residual'][0]+answer['residual'][1],answer['ratios']
  delta,solver_ratios,solver_admitted,reason=P.minres_core(iteration_action,correction_rhs,d['scale'],tolerance,original_rows,label,cap=cap)
  keep(label+'_completed_correction',delta);keep(label+'_solver_return_ratios',solver_ratios)
  nodes,q=P.dd_node_update(start,delta,keep,label+'_final_update')
  after=york_original_certificate(nodes,d,label+'_updated')
  adelta,_,_=york_packed_action(P.a_dd(delta),d,label+'_correction_action');aq,_,_=york_packed_action(P.a_dd(q),d,label+'_compression_action')
  gap=P.a_sub(P.a_add(P.a_sub(after['residual'],before['residual']),adelta),aq)
  york_pair_keep(label+'_original_residual_update_identity',gap,keep)
  envelope=2*d['rhs_envelope']
  for suffix,value in (('before',start),('after',nodes),('delta',P.a_dd(delta)),('compression',P.a_dd(q))):envelope=envelope+york_packed_envelope(value,d,label+'_'+suffix)
  keep(label+'_residual_update_operation_envelope',envelope)
  P.check(label+'_paired_original_residual_update_identity',gap[0]+gap[1],np.zeros(11135),envelope)
  record=P.checkpoint('CYCLE',{**P.AVAILABLE,**P.RAW},dict(kind='new_auxiliary_york_original_row_correction',cycle=cycle,cap=cap,solver_reason=reason,solver_return_admitted=solver_admitted,original_rows_admitted=after['admitted'],original_ratios=after['ratios'].tolist(),controls=P.CHECKS[-1:],physical_TT_prepared=False))
  cycles.append(record);current=after
 return nodes,current,initial,cycles

def york_point_projection(nodes,certificate,d):
 # A=L*BL is PSD; original-row admission fixes the unique L W even if
 # the auxiliary W itself has a kernel. No quantitative W-error is claimed.
 assert certificate['admitted']
 L=certificate['longitudinal'];longitudinal_density=certificate['density']
 tt=P.a_sub(d['PiTF'],longitudinal_density)
 york_pair_keep('auxiliary_potential_nodes',nodes,keep);york_pair_keep('projected_longitudinal_tensor',L,keep)
 york_pair_keep('projected_longitudinal_density',longitudinal_density,keep);york_pair_keep('compact_weak_TT_remainder_density',tt,keep)
 reconstruction=P.a_sub(P.a_add(tt,longitudinal_density),d['PiTF']);york_pair_keep('point_density_decomposition_identity',reconstruction,keep)
 weak=york_weak_source(tt,d['maps'],d['geometry'],keep,'projected_TT')
 weak=(york_pack(weak[0]),york_pack(weak[1]));york_pair_keep('compact_weak_TT_remainder',weak,keep)
 equality=P.a_sub(weak,certificate['residual']);york_pair_keep('weak_TT_equals_original_residual_contact',equality,keep)
 weak_ratios=york_component_ratios(weak[0]+weak[1],d['rhs'][0]+d['rhs'][1],d['scale']);keep('compact_weak_TT_original_component_ratios',weak_ratios)
 return dict(compact_weak_TT_original_rows_admitted=bool(np.all(weak_ratios<=1e-10)),compact_weak_TT_original_component_ratios=weak_ratios.tolist(),potential_unique_not_claimed=True,longitudinal_projection_original_rows_admitted=True,continuum_divergence_free_TT_not_claimed=True,physical_exterior_adopted=False)
