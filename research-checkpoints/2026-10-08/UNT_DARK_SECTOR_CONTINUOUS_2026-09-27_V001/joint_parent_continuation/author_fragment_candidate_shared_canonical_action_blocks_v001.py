"""HELD candidate-dependent mechanical action and canonical Newton contacts.
Globals np,P,fy_* and the exact NEW160 configuration-contact definitions.
All four columns are completed SAME225 candidate dictionaries; EOS/H and weak
current words are newly earned cached operands, never old frozen coefficients.
The phase-only mass cache/action is supplied by its distinct reviewed adapter.
No producer, payload, current replay, solver, inverse, budget or physical adoption.
"""
CANDIDATE_CANONICAL_BLOCK_AUTHOR_DRAFT=True
CANDIDATE_CANONICAL_BLOCK_AUTHORING_IN_PROGRESS=False

def cs_keep(label,value,keep):
 assert isinstance(value,tuple) and len(value)==2 and value[0].shape==value[1].shape
 keep(label+'_both_words',np.stack(value,axis=0).copy())
 for name,a in zip(('hi','lo'),value):
  keep(label+'_'+name,np.asarray(a).copy());assert a.dtype==np.float64 and np.all(np.isfinite(a))
 return value

def cs_native_weak(point,basis,keep,label):
 assert point[0].shape==point[1].shape==(15136,99)
 modes=tuple(a.reshape(15136,33,3).transpose(1,0,2) for a in point)
 cs_keep(label+'_point_covector_modes',modes,keep)
 return cs_keep(label+'_weak',P.dd_native_scatter(modes,basis,keep),keep)

def cs_york_covector_six(tensor,keep,label):
 assert tensor[0].shape==tensor[1].shape==(15136,3,3)
 cs_keep(label+'_density_tensor',tensor,keep)
 cs_keep(label+'_serialized_asymmetry',P.a_sub(tensor,(tensor[0].swapaxes(-1,-2),tensor[1].swapaxes(-1,-2))),keep)
 rows=[]
 for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2)):
  a=P.a_slice(tensor,(slice(None),i,j))
  rows.append(a if i==j else P.a_add(a,P.a_slice(tensor,(slice(None),j,i))))
 # Offdiagonal test entries vary together: sum the two density entries ONCE.
 return cs_keep(label+'_canonical_six',P.a_stack(rows,-1),keep)

def prepare_candidate_shared_canonical_blocks(columns,basis,current_weak,phase_cache,keep,label):
 assert len(columns)==4 and basis['R'].shape==basis['dv'].shape==(4,3784)
 assert basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 for iq,column in enumerate(columns):
  c=column['candidate'];assert np.array_equal(c['s']['R'],basis['R'][iq])
  for n,shape in (('native_density',(3784,99)),('metric_total_density',(3784,6))):
   assert c['momenta'][n][0].shape==c['momenta'][n][1].shape==shape
   cs_keep(label+'_column%d_current_%s'%(iq,n),c['momenta'][n],keep)
  for n in ('p','H'):assert column['eos']['value'][n][0].shape==column['eos']['value'][n][1].shape==(3784,)
 H=tuple(np.concatenate([c['eos']['value']['H'][w] for c in columns]) for w in (0,1))
 q=tuple(np.concatenate([c['eos']['value']['p'][w] for c in columns]) for w in (0,1))
 eH=np.concatenate([c['eos']['H_operation_envelope'] for c in columns])
 cs_keep(label+'_same_candidate_literal_H',H,keep);cs_keep(label+'_same_candidate_literal_phase_density',q,keep);keep(label+'_literal_H_operation_envelope',eH.copy())
 assert all(np.array_equal(H[w],phase_cache['H'][w]) and np.array_equal(q[w],phase_cache['current_point_density'][w]) for w in (0,1))
 assert np.array_equal(eH,phase_cache['eH']) and phase_cache['diagonal'][0].shape==phase_cache['diagonal'][1].shape==(87,45)
 shapes=dict(native=(33,3,87,45),metric=(6,87,45),phase=(87,45))
 masks=dict(native=np.broadcast_to(P.native_mask(),shapes['native']),metric=P.metric_mask(),phase=P.scalar_mask())
 for n,shape in shapes.items():
  a=current_weak[n];assert a[0].shape==a[1].shape==shape and all(np.all(w[~masks[n]]==0) for w in a)
  cs_keep(label+'_completed_current_weak_'+n,a,keep)
 return dict(columns=columns,current_weak=current_weak,phase_cache=phase_cache,mechanical_phase_temporal_cross_blocks_zero=True,
             global_mechanical_invertibility_earned=False,current_weak_recontracted=False,old_frozen_action_reused=False,physical_adoption=False)

def candidate_shared_temporal_action(blocks,basis,native_nodes,metric_nodes,phase_nodes,phase_action,keep,label,column_complete=None):
 masks=dict(native=np.broadcast_to(P.native_mask(),(33,3,87,45)),metric=P.metric_mask(),phase=P.scalar_mask())
 for n,a,shape in (('native',native_nodes,(33,3,87,45)),('metric',metric_nodes,(6,87,45)),('phase',phase_nodes,(87,45))):
  assert a[0].shape==a[1].shape==shape and all(np.all(w[~masks[n]]==0) for w in a)
  cs_keep(label+'_NEW_'+n+'_temporal_nodes',a,keep)
 native=cs_keep(label+'_NEW_native_point_time_words',P.dd_native_node_value(native_nodes,basis,keep,jet=0),keep)
 metric=cs_keep(label+'_NEW_physical_metric_six_time_words',P.dd_metric_node_value(metric_nodes,basis,keep,jet=0),keep)
 native_parts=[];metric_parts=[];completed=[]
 for iq,column in enumerate(blocks['columns']):
  sl=slice(iq*3784,(iq+1)*3784);u=P.a_dd(np.zeros((3784,4,3)));z=P.a_dd(np.zeros((32,3784,4,3)));ht=P.a_dd(np.zeros((3784,3,3)))
  for w in (0,1):u[w][:,0]=native[w][0,sl];z[w][:,:,0]=native[w][1:,sl]
  for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
   for w in (0,1):ht[w][:,i,j]=metric[w][sl,slot];ht[w][:,j,i]=metric[w][sl,slot]
  direction=dict(h=P.a_dd(np.zeros((3784,3,3))),h_spatial_jets=P.a_dd(np.zeros((3784,2,3,3))),h_dot=ht,u_jets=u,z_jets=z)
  for n,a in direction.items():cs_keep(label+'_column%d_NEW_direction_'%iq+n,a,keep)
  contact=finite_candidate_configuration_contact(column['candidate'],column['geometry'],column['gauge'],column['covectors'],column['mechanical'],direction,column['reference'],keep,label+'_column%d_NEW_mechanical_action'%iq)
  n=cs_keep(label+'_column%d_native_action'%iq,contact['delta_momenta']['native_density'],keep)
  m=cs_keep(label+'_column%d_metric_action'%iq,contact['delta_momenta']['metric_total_density'],keep)
  native_parts.append(n);metric_parts.append(m)
  # Let the existing containing writer seal/release this completed contact.
  data=dict(direction=direction,contact=contact,physical_metric_time_values=tuple(a[sl] for a in metric))
  completed.append(column_complete(iq,data) if column_complete is not None else data)
 n=cs_keep(label+'_NEW_native_point_action',tuple(np.concatenate([a[w] for a in native_parts]) for w in (0,1)),keep)
 m=cs_keep(label+'_NEW_metric_point_action',tuple(np.concatenate([a[w] for a in metric_parts]) for w in (0,1)),keep)
 nw=cs_native_weak(n,basis,keep,label+'_NEW_native_action')
 mw=cs_keep(label+'_NEW_metric_weak_action',P.dd_metric_scatter(m,basis,keep),keep)
 phase=phase_action(blocks['phase_cache'],basis,phase_nodes,keep,label+'_NEW_literal_phase_mass')
 assert phase['weak'][0].shape==phase['weak'][1].shape==(87,45) and phase['point'][0].shape==phase['point'][1].shape==(15136,)
 cs_keep(label+'_NEW_phase_weak_action',phase['weak'],keep);cs_keep(label+'_NEW_phase_point_action',phase['point'],keep)
 for n in ('value','R','Z'):
  a=phase['scalar_jets'][n];assert a[0].shape==a[1].shape==(15136,);cs_keep(label+'_NEW_phase_time_'+n,a,keep)
 return dict(weak=dict(native=nw,metric=mw,phase=phase['weak']),point=dict(native=n,metric=m,phase=phase['point']),
             phase_scalar_jets=phase['scalar_jets'],completed_mechanical_columns=completed,
             mechanical_phase_temporal_cross_blocks_zero=True,Frechet_action_only=True,old_frozen_action_reused=False,physical_adoption=False)

def candidate_shared_canonical_rows(blocks,basis,configuration_parts,temporal_action,prepared_Pi,delta_prepared_Pi,native_prior,literal_phase_prior,nominal_metric_prior,keep,label):
 assert len(configuration_parts)==4;native_parts=[];metric_parts=[];phase_parts=[]
 for iq,(column,part) in enumerate(zip(blocks['columns'],configuration_parts)):
  d=part['direction'];assert all(np.all(w==0) for n in ('h_dot','u_jets','z_jets') for w in d[n])
  if 'phi' in d:assert all(np.all(w==0) for w in d['phi']),'Selected configuration branch holds phase firstjets; phase rate enters only its mass block'
  contact,eos=part['contact'],part['eos']
  for n in ('p','H'):assert all(np.array_equal(eos['value'][n][w],column['eos']['value'][n][w]) for w in (0,1))
  for n,a in (('native',contact['delta_momenta']['native_density']),('metric',contact['delta_momenta']['metric_total_density']),('phase',eos['delta']['p'])):
   cs_keep(label+'_column%d_configuration_contact_'%iq+n,a,keep)
  native_parts.append(contact['delta_momenta']['native_density']);metric_parts.append(contact['delta_momenta']['metric_total_density']);phase_parts.append(eos['delta']['p'])
 nq=tuple(np.concatenate([a[w] for a in native_parts]) for w in (0,1));mq=tuple(np.concatenate([a[w] for a in metric_parts]) for w in (0,1));pq=tuple(np.concatenate([a[w] for a in phase_parts]) for w in (0,1))
 for n,a in (('native',nq),('metric',mq),('phase',pq)):cs_keep(label+'_completed_D_Q_point_'+n,a,keep)
 configuration=dict(native=cs_native_weak(nq,basis,keep,label+'_D_Q_native'),metric=cs_keep(label+'_D_Q_metric',P.dd_metric_scatter(mq,basis,keep),keep),phase=cs_keep(label+'_D_Q_literal_phase',P.dd_scalar_scatter(pq,basis,keep,label+'_D_Q_phase_scatter'),keep))
 six=cs_york_covector_six(prepared_Pi,keep,label+'_prepared_actual_trace_York_target')
 dsix=cs_york_covector_six(delta_prepared_Pi,keep,label+'_D_QWtau_actual_trace_York_target')
 target_metric=cs_keep(label+'_prepared_metric_weak_target',P.dd_metric_scatter(six,basis,keep),keep)
 dtarget_metric=cs_keep(label+'_prepared_metric_target_JVP',P.dd_metric_scatter(dsix,basis,keep),keep)
 priors=dict(native=native_prior,metric=target_metric,phase=literal_phase_prior)
 expected_shapes=dict(native=(33,3,87,45),metric=(6,87,45),phase=(87,45))
 target_delta=dict(native=P.a_dd(np.zeros((33,3,87,45))),metric=dtarget_metric,phase=P.a_dd(np.zeros((87,45))))
 residual={};epsilon={};jvp={}
 for n,shape in expected_shapes.items():
  assert priors[n][0].shape==priors[n][1].shape==shape
  mask=np.broadcast_to(P.native_mask(),shape) if n=='native' else P.metric_mask() if n=='metric' else P.scalar_mask()
  assert all(np.all(w[~mask]==0) for w in priors[n])
  cs_keep(label+'_current_candidate_weak_'+n,blocks['current_weak'][n],keep);cs_keep(label+'_unchanged_or_prepared_target_'+n,priors[n],keep)
  residual[n]=cs_keep(label+'_current_minus_target_'+n,P.a_sub(blocks['current_weak'][n],priors[n]),keep)
  epsilon[n]=cs_keep(label+'_target_minus_current_epsilon_'+n,P.a_sub(priors[n],blocks['current_weak'][n]),keep)
  jvp[n]=cs_keep(label+'_canonical_JVP_'+n,P.a_sub(P.a_add(configuration[n],temporal_action['weak'][n]),target_delta[n]),keep)
 assert nominal_metric_prior[0].shape==nominal_metric_prior[1].shape==(6,87,45)
 nominal=dict(current_minus_nominal=cs_keep(label+'_current_minus_original_nominal_metric_target',P.a_sub(blocks['current_weak']['metric'],nominal_metric_prior),keep),prepared_minus_nominal=cs_keep(label+'_prepared_minus_original_nominal_metric_target',P.a_sub(target_metric,nominal_metric_prior),keep))
 return dict(residual=residual,epsilon=epsilon,JVP=jvp,configuration_contact=configuration,temporal_action=temporal_action['weak'],prepared_target=priors,prepared_target_JVP=target_delta,nominal_metric_bridge=nominal,
             original_offsets_refitted=False,phase_and_native_priors_unchanged=True,full_configuration_couplings_present=True,
             mechanical_inverse_or_global_rank_earned=False,canonical_or_phase_restoration_qualified=False,physical_adoption=False)
