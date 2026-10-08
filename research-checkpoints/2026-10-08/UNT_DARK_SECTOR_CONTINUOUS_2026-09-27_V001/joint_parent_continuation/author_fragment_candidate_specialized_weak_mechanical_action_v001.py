"""HELD direct fixed-configuration weak mechanical operator; definitions only.
Uses the independently checked147 temporal specialization and original nodal
value lifts/scatters. Each of four caches must come from its own CLOSED actual
candidate; no geometry/chart/current/160 producer or frozen action is invoked.
The containing caller authenticates custody, original basis/targets and all
arithmetic/provider pins. This operator owns neither an inverse nor a finite
candidate, normal stress response or physical acceptance.
"""
SPECIALIZED_WEAK_MECHANICAL_AUTHOR_DRAFT=True
SPECIALIZED_WEAK_MECHANICAL_AUTHORING_IN_PROGRESS=False

def sw_keep(label,x,keep):
 assert isinstance(x,tuple) and len(x)==2 and x[0].shape==x[1].shape
 for name,a in zip(('hi','lo'),x):
  keep(label+'_'+name,np.asarray(a).copy())
  assert a.dtype==np.float64 and np.all(np.isfinite(a)),label
 return x

def prepare_specialized_weak_mechanical(columns,basis,keep,label):
 assert len(columns)==4 and basis['R'].shape==basis['dv'].shape==(4,3784)
 assert basis['hats'].shape==(4,4,3,86,44)
 assert np.all(basis['R']>0) and np.all(basis['dv']>0)
 caches=[]
 for iq,column in enumerate(columns):
  candidate=column['candidate'];assert np.array_equal(candidate['s']['R'],basis['R'][iq])
  assert isinstance(candidate['candidate_provenance'],dict) and candidate['candidate_provenance']
  cache=candidate_temporal_prepare(candidate,column['reference'],keep,label+'_column%d'%iq)
  assert cache['p']==3784
  caches.append(cache)
 return dict(columns=caches,basis={n:np.asarray(basis[n]).copy() for n in ('R','dv','hats')},
             source='same_candidate_fixed_configuration_temporal147',all_four_actual_columns_required=True,
             general160_or_current_replayed=False,global_inverse_earned=False,physical_adoption=False)

def specialized_weak_mechanical_action(blocks,basis,native_nodes,metric_nodes,keep,label,column_complete=None):
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],blocks['basis'][n])
 masks=dict(native=np.broadcast_to(P.native_mask(),(33,3,87,45)),metric=P.metric_mask())
 for n,a,shape in (('native',native_nodes,(33,3,87,45)),('metric',metric_nodes,(6,87,45))):
  assert isinstance(a,tuple) and len(a)==2 and all(w.shape==shape for w in a)
  sw_keep(label+'_supplied_'+n+'_nodes',a,keep)
  assert all(np.all(w[~masks[n]]==0) for w in a),'Original independent coordinates required'
 native=sw_keep(label+'_original_lift_native_values',P.dd_native_node_value(native_nodes,basis,keep,jet=0),keep)
 metric=sw_keep(label+'_original_lift_physical_metric_values',P.dd_metric_node_value(metric_nodes,basis,keep,jet=0),keep)
 assert native[0].shape==native[1].shape==(33,15136,3)
 assert metric[0].shape==metric[1].shape==(15136,6)
 native_parts=[];metric_parts=[];completed=[]
 for iq,cache in enumerate(blocks['columns']):
  sl=slice(iq*3784,(iq+1)*3784)
  physical=dict(native=tuple(a[:,sl].transpose(1,0,2).reshape(3784,99).copy() for a in native),
                metric=tuple(a[sl].copy() for a in metric))
  result=candidate_specialized_temporal_action(cache,physical,keep,label+'_column%d_NEW'%iq)
  point=result['point'];native_parts.append(sw_keep(label+'_column%d_native_point'%iq,point['native'],keep))
  metric_parts.append(sw_keep(label+'_column%d_metric_point'%iq,point['metric_total'],keep))
  data=dict(supplied_physical_rates=physical,specialized_temporal_result=result,
            general160_configuration_contact_evaluated=False,normal_stress_response_earned=False)
  completed.append(column_complete(iq,data) if column_complete is not None else data)
 point_native=sw_keep(label+'_completed_native_point',tuple(np.concatenate([a[w] for a in native_parts]) for w in (0,1)),keep)
 point_metric=sw_keep(label+'_completed_metric_point',tuple(np.concatenate([a[w] for a in metric_parts]) for w in (0,1)),keep)
 modes=sw_keep(label+'_native_original_scatter_modes',tuple(a.reshape(15136,33,3).transpose(1,0,2) for a in point_native),keep)
 weak_native=sw_keep(label+'_original_weak_native',P.dd_native_scatter(modes,basis,keep),keep)
 weak_metric=sw_keep(label+'_original_weak_metric',P.dd_metric_scatter(point_metric,basis,keep),keep)
 assert all(np.all(w[~masks['native']]==0) for w in weak_native)
 assert all(np.all(w[~masks['metric']]==0) for w in weak_metric)
 return dict(weak=dict(native=weak_native,metric=weak_metric),point=dict(native=point_native,metric=point_metric),
             completed_specialized_columns=completed,configuration_held=True,phase_block_supplied_separately=True,
             current_or_target_recontracted=False,general160_or_frozen_action_replayed=False,
             full_normal_response_or_global_inverse_earned=False,physical_adoption=False)
