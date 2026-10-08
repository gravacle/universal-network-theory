"""HELD point-TOTAL-preserving input wrapper for unchanged138/158 algebra.
Globals np/P/N, exact tt_*138 helpers, original E/F/scalar maps and cfg290 jets.
The containing owner authenticates CLOSED NEW139 point operands and each NEW
correction. No nodal mechanical baseline, zero gauge-time policy or mixed phase
baseline is inferred. Fresh geometry/current/feedback acceptance stays external.
"""
POINT_TOTAL_TRIAL_AUTHOR_DRAFT=True
POINT_TOTAL_TRIAL_AUTHORING_IN_PROGRESS=False
POINT_TOTAL_TRIAL_BASELINE_CLOSURE=(None,None,None,None)
POINT_TOTAL_TRIAL_CORRECTION_CLOSURE=(None,None,None,None)
POINT_TOTAL_TRIAL_SOURCE_PINS={
 'author_fragment_total_trial_fields_to_column_v001.py':'c0c3f97320301834666f35db66195aa5715c182dd2bb29ec4e957433808aaf94',
 'author_fragment_fixed_geometry_total_rate_state_v002.py':'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d',
 'author_fragment_fresh_trial_residual_packet_v001.py':'5814945f10ed230da7a26d234c83b49966a2376e692f81a55c0b38d077d48af4'}

def prepare_point_TOTAL_trial_fields(previous_configuration,correction,basis,fixed_columns,provenance,keep,label,stage_complete):
 assert not POINT_TOTAL_TRIAL_AUTHOR_DRAFT and not POINT_TOTAL_TRIAL_AUTHORING_IN_PROGRESS
 assert all(isinstance(q,(tuple,list)) and len(q) in (2,3) and all(v is not None for v in q) for c in (POINT_TOTAL_TRIAL_BASELINE_CLOSURE,POINT_TOTAL_TRIAL_CORRECTION_CLOSURE) for q in c),'Future natural closure bindings required'
 tt_require(provenance)
 assert provenance['baseline_closure']==POINT_TOTAL_TRIAL_BASELINE_CLOSURE and provenance['correction_closure']==POINT_TOTAL_TRIAL_CORRECTION_CLOSURE
 assert provenance['point_TOTAL_source_pins']==POINT_TOTAL_TRIAL_SOURCE_PINS and provenance['all_point_TOTAL_operand_seals_authenticated'] is True
 assert len(fixed_columns)==4 and basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert basis['r'].shape==(87,) and basis['z'].shape==(45,) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 for n,a in basis.items():keep(label+'_original_basis_'+n,np.asarray(a).copy())
 masks=N.normal_test_mask();assert [int(np.count_nonzero(x)) for x in masks]==[3740,3740,3655,3740]
 nodes={};records=[]
 for n,shape,mask in (('chi',(87,45),masks[0]),('W',(3,87,45),masks[1:]),('t',(87,45),P.scalar_mask())):
  base=tt_pair(label+'_previous_configuration_'+n,previous_configuration[n],shape,keep);step=tt_pair(label+'_NEW_configuration_increment_'+n,correction[n],shape,keep)
  assert all(np.all(a[~mask]==0) for x in (base,step) for a in x)
  nodes[n]=tt_add(label+'_configuration_'+n,base,step,shape,keep)
  assert all(np.all(a[~mask]==0) for a in nodes[n])
  tt_stage('POINT_TOTAL_CONFIGURATION_FIELD',dict(field=n,previous=base,increment=step,total=nodes[n],provenance=provenance),stage_complete,records)
 sections=candidate_configuration_york_direction_jets(nodes,basis,keep,label+'_TOTAL_configuration')
 tt_stage('POINT_TOTAL_CONFIGURATION_SECTIONS',dict(nodes=nodes,sections=sections,provenance=provenance),stage_complete,records)
 new_nodes={}
 for n,shape,mask in (('native',(33,3,87,45),np.broadcast_to(P.native_mask(),(33,3,87,45))),('metric',(6,87,45),P.metric_mask()),('phase',(87,45),P.scalar_mask())):
  new_nodes[n]=tt_pair(label+'_NEW_increment_nodes_'+n,correction[n],shape,keep);assert all(np.all(a[~mask]==0) for a in new_nodes[n])
 dn=tt_pair(label+'_NEW_original_E_increment',P.dd_native_node_value(new_nodes['native'],basis,keep,jet=0),(33,15136,3),keep)
 dm=tt_pair(label+'_NEW_original_F_physical6_increment',P.dd_metric_node_value(new_nodes['metric'],basis,keep,jet=0),(15136,6),keep)
 dp=phase_response_scalar_jets(new_nodes['phase'],basis,keep,label+'_NEW_phase_increment')
 for n in ('value','R','Z'):dp[n]=tt_pair(label+'_NEW_phase_increment_'+n,dp[n],(15136,),keep)
 tt_stage('POINT_TOTAL_NEW_POINT_INCREMENTS',dict(nodes=new_nodes,native=dn,metric=dm,phase_jets=dp,original_maps_once=True,provenance=provenance),stage_complete,records)
 native=[];metric=[];phase=[];baseline_sources=[]
 for iq,fixed in enumerate(fixed_columns):
  assert fixed['provenance']==provenance['columns'][iq] and fixed['provenance']['original_fixed_references_verified'] is True
  base=fixed['point_TOTAL'];assert base['registration_verified'] is True and base['same_original_basis_verified'] is True and base['provenance']==fixed['provenance']
  assert base['sealed_sources'] and all(isinstance(q,dict) and all(isinstance(q[k],str) and q[k] for k in ('file','sha256','commit_file','commit_sha256')) for q in base['sealed_sources'])
  p=3784;sl=slice(iq*p,(iq+1)*p);owned={}
  for n,shape in (('u_jets',(p,4,3)),('z_jets',(32,p,4,3)),('h_dot',(p,3,3)),('phi',(p,4)),('N_jets',(p,4)),('beta_jets',(p,4,3)),('raw225_Lie_beta_h',(p,3,3))):owned[n]=tt_pair(label+'_column%d_owned_point_TOTAL_'%iq+n,base[n],shape,keep)
  for n in ('u_jets','z_jets'):assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(owned[n],fixed['covectors'][n]))
  for n in ('N_jets','beta_jets'):assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(owned[n],fixed['gauge'][n]))
  assert all(np.array_equal(a.view(np.uint64),a.swapaxes(-1,-2).view(np.uint64)) for a in owned['h_dot'])
  assert all(np.array_equal(a[:,1:].view(np.uint64),b.view(np.uint64)) for a,b in zip(owned['phi'],fixed['phase_spatial']))
  bn=tuple(np.concatenate((owned['u_jets'][w][:,0][None],owned['z_jets'][w][:,:,0]),axis=0) for w in (0,1))
  bm=tuple(np.stack([owned['h_dot'][w][:,a,b] for a,b in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],axis=-1) for w in (0,1))
  nt=tt_add(label+'_column%d_native_point_TOTAL'%iq,bn,tuple(a[:,sl].copy() for a in dn),(33,p,3),keep)
  mt=tt_add(label+'_column%d_metric_point_TOTAL'%iq,bm,tuple(a[sl].copy() for a in dm),(p,6),keep)
  ph0=tt_add(label+'_column%d_phase0_point_TOTAL'%iq,tuple(a[:,0].copy() for a in owned['phi']),tuple(a[sl].copy() for a in dp['value']),(p,),keep)
  pt=tuple(a.copy() for a in owned['phi'])
  for w in (0,1):pt[w][:,0]=ph0[w]
  pt=tt_pair(label+'_column%d_phase_point_TOTAL'%iq,pt,(p,4),keep)
  assert all(np.array_equal(a[:,1:].view(np.uint64),b[:,1:].view(np.uint64)) for a,b in zip(pt,owned['phi']))
  ref=tt_stage('POINT_TOTAL_UPDATED_COLUMN_TIME',dict(column=iq,owned_point_TOTAL=owned,native_time=nt,metric_time=mt,phi=pt,mixed_phase_increment={n:tuple(a[sl].copy() for a in dp[n]) for n in ('R','Z')},sealed_baseline_sources=base['sealed_sources'],provenance=fixed['provenance'],nodal_mechanical_baseline_inferred=False),stage_complete,records)
  native.append(nt);metric.append(mt);phase.append(pt);baseline_sources.append(dict(column=iq,sealed_sources=base['sealed_sources'],point_record=ref))
 native_time=tt_pair(label+'_all_four_native_point_TOTAL',tuple(np.concatenate([x[w] for x in native],axis=1) for w in (0,1)),(33,15136,3),keep)
 metric_time=tt_pair(label+'_all_four_metric_point_TOTAL',tuple(np.concatenate([x[w] for x in metric],axis=0) for w in (0,1)),(15136,6),keep)
 phi=tt_pair(label+'_all_four_paired_phase_TOTAL',tuple(np.concatenate([x[w] for x in phase],axis=0) for w in (0,1)),(15136,4),keep)
 packet=dict(nodes=nodes,sections=sections,native_time=native_time,metric_time=metric_time,phi=phi,phase_mixed_increment={n:dp[n] for n in ('R','Z')},phase_mixed_are_increments=True,basis=basis,provenance=provenance,reference_configuration_exact_zero=all(np.all(a==0) for n in ('chi','W','t') for a in nodes[n]),baseline_point_sources=baseline_sources,point_TOTAL_preserving=True,new_E_F_increment_lifted_once=True,nodal_mechanical_baseline_inferred=False,physical_adoption=False)
 ref=tt_stage('POINT_TOTAL_TRIAL_FIELDS',packet,stage_complete,records);packet['total_fields_record']=ref;packet['point_TOTAL_preparation_records']=records
 return packet

def point_TOTAL_trial_fields_to_column(prepared,iq,fixed,keep,label,stage_complete):
 assert not POINT_TOTAL_TRIAL_AUTHOR_DRAFT and not POINT_TOTAL_TRIAL_AUTHORING_IN_PROGRESS
 assert all(isinstance(q,(tuple,list)) and len(q) in (2,3) and all(v is not None for v in q) for c in (POINT_TOTAL_TRIAL_BASELINE_CLOSURE,POINT_TOTAL_TRIAL_CORRECTION_CLOSURE) for q in c),'Future natural closure bindings required'
 tt_require(prepared['provenance']);assert prepared['point_TOTAL_preserving'] is True and prepared['nodal_mechanical_baseline_inferred'] is False and 0<=iq<4
 assert prepared['provenance']['baseline_closure']==POINT_TOTAL_TRIAL_BASELINE_CLOSURE and prepared['provenance']['correction_closure']==POINT_TOTAL_TRIAL_CORRECTION_CLOSURE
 assert prepared['baseline_point_sources'][iq]['sealed_sources']==fixed['point_TOTAL']['sealed_sources'] and fixed['provenance']==prepared['provenance']['columns'][iq]
 records=[];copied={}
 for n,shape in (('N',(3784,)),('beta',(3784,3)),('N_jets',(3784,4)),('beta_jets',(3784,4,3))):copied[n]=tt_pair(label+'_unchanged_genuine_gauge_'+n,fixed['gauge'][n],shape,keep)
 old_Lie=tt_pair(label+'_owned_raw225_Lie_beta_h',fixed['point_TOTAL']['raw225_Lie_beta_h'],(3784,3,3),keep)
 tt_stage('POINT_TOTAL_COLUMN_HANDOFF',dict(column=iq,gauge=copied,owned_raw225_Lie_beta_h=old_Lie,baseline_point_sources=fixed['point_TOTAL']['sealed_sources'],total_fields=prepared['total_fields_record'],provenance=fixed['provenance'],gauge_time_not_zeroed=True,owned_Lie_not_replaced_by_contact_Lie=True),stage_complete,records)
 captured={}
 def capture(n,a):
  if n in (label+'_NEW_raw_Lie_beta_h_hi',label+'_NEW_raw_Lie_beta_h_lo'):captured[n]=np.asarray(a).copy()
  keep(n,a)
 column=total_trial_fields_to_column(prepared,iq,fixed,capture,label,stage_complete)
 assert len(column['completed_stages'])==6 and column['physical_adoption'] is False
 for n in copied:assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(copied[n],column['gauge'][n]))
 names=tuple(label+'_NEW_raw_Lie_beta_h_'+w for w in ('hi','lo'));assert all(n in captured for n in names),'NEW225 Lie capture required; no reconstruction from KADM'
 new_Lie=tt_pair(label+'_NEW_raw225_Lie_beta_h',tuple(captured[n] for n in names),(3784,3,3),keep)
 gap=tt_pair(label+'_NEW_minus_previous_raw225_Lie_beta_h',P.a_sub(new_Lie,old_Lie),(3784,3,3),keep)
 ref=tt_stage('POINT_TOTAL_COLUMN_ASSOCIATION',dict(column=iq,genuine_gauge=copied,previous_raw225_Lie_beta_h=old_Lie,new_raw225_Lie_beta_h=new_Lie,geometry_dependent_Lie_change=gap,raw225_new_Lie_authoritative=True,formal160_Lie_not_substituted=True,original_six_column_stages=column['completed_stages'],provenance=column['candidate']['candidate_provenance'],physical_adoption=False),stage_complete,records)
 column['point_TOTAL_handoff_records']=records;column['point_TOTAL_association_record']=ref;column['point_TOTAL_preserving']=True
 return column
