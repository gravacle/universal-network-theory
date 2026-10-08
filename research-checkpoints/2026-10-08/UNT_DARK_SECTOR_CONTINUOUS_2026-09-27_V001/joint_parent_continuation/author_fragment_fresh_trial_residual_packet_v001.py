"""HELD fresh total-trial residual glue; import-free definitions only.
Globals np/P/N, tt_*138, selected FY/FS, native/EH247, phase62, ordinary49,
canonical126, temporal147, literal142 and original evaluation-transpose244.
Completed NEW138 columns are inputs. No old primal/current/action/solver replay.
Every new child is synchronously sealed before the next child; root owns I/O.
No frozen feedback value, stationarity, physical or observer admission is made.
"""
FRESH_TRIAL_RESIDUAL_AUTHOR_DRAFT=True
FRESH_TRIAL_RESIDUAL_AUTHORING_IN_PROGRESS=False
FRESH_TRIAL_OWNER_BINDING=(None,None)
FRESH_TRIAL_FEEDBACK_CLOSURE=(None,None,None,None)
FRESH_TRIAL_SOURCE_PINS={'author_fragment_total_trial_fields_to_column_v001.py': 'c0c3f97320301834666f35db66195aa5715c182dd2bb29ec4e957433808aaf94', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_candidate_phase_normal_stress_v001.py': 'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd', 'author_fragment_finite_fixed_canonical_ordinary_v001.py': '2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a', 'author_fragment_candidate_shared_canonical_action_blocks_v001.py': '4ffdbf60dde14d9b87a7cb947dca7f61ec7e4ffe456653aed5298de27dbd59ee', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_literal_temporal_gradient_bridge_v001.py': '880d9689965e7f66a159178cbec13b0a1e03e3929c7796e90c4370a9919f4d50', 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py': '3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871'}


def fr_pair(label,x,shape,keep):return tt_pair(label,x,shape,keep)


def fr_join(parts,shape,keep,label):
 assert len(parts)==4
 return fr_pair(label,tuple(np.concatenate([a[w] for a in parts],axis=0) for w in (0,1)),shape,keep)


def fr_require(prepared,columns,provenance):
 tt_require(prepared['provenance'])
 assert not FRESH_TRIAL_RESIDUAL_AUTHOR_DRAFT and not FRESH_TRIAL_RESIDUAL_AUTHORING_IN_PROGRESS
 assert all(a is not None for a in FRESH_TRIAL_OWNER_BINDING) and provenance['owner_binding']==FRESH_TRIAL_OWNER_BINDING
 assert provenance['source_pins']==FRESH_TRIAL_SOURCE_PINS and provenance['all_selected_source_seals_authenticated'] is True and provenance['fixed_original_labels_and_targets_verified'] is True and provenance['physical_adoption'] is False
 assert len(columns)==4 and prepared['physical_adoption'] is False
 for iq,column in enumerate(columns):
  assert len(column['completed_stages'])==6 and column['physical_adoption'] is False
  assert column['candidate']['candidate_provenance']['total_fields']==prepared['total_fields_record']
  assert column['candidate']['candidate_provenance']['previous']==prepared['provenance']['columns'][iq]


def fresh_trial_normal_column(column,mean_labels,Hbar,keep,label,stage_complete):
 candidate,contact,curvature=column['candidate'],column['contact'],column['curvature'];s,c=column['normal_s'],column['normal_c'];p=3784;records=[]
 assert candidate['c']['h'].shape==(p,3,3) and np.isfinite(Hbar) and Hbar>0
 assert mean_labels['existing_once_counted_branch_registered'] is True and mean_labels['provenance']
 assert all(np.all(w==0) for w in mean_labels['galaxy_mass_weight']),'Galaxy sheet must not be counted in reference mean'
 tt_stage('TRIAL_MEAN_INPUT',dict(labels=mean_labels,candidate_provenance=candidate['candidate_provenance']),stage_complete,records)
 zero_h=tt_zero((p,3,3));geometry=dict(h=c['h'],ih=c['ih'],delta_h=zero_h,delta_ih=zero_h)
 ordinary=finite_fixed_canonical_ordinary_point(geometry,dict(N=c['N'],beta=c['beta']),mean_labels,keep,label+'_NEW_mean')
 tt_stage('TRIAL_MEAN_ORDINARY',dict(ordinary=ordinary,labels=mean_labels['provenance'],candidate_provenance=candidate['candidate_provenance']),stage_complete,records)
 D={n:tt_zero(a[0].shape) for n,a in {**s,**c}.items()};eos=column['phase']['eos'];coeff=tt_zero((p,4,4));theta=None
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
   if row==0:
    if coordinate is None:f[:]=1.
    else:df[:,coordinate]=1.
   elif coordinate is None:b[:,row-1]=1.
   else:db[:,coordinate,row-1]=1.
   child=label+'_row%d_jet%d'%(row,jet)
   native=finite_candidate_native_EH_normal(candidate,contact,curvature,f,df,b,db,Hbar,column['reference'],keep,child+'_NEW_native_EH')
   tt_stage('TRIAL_NORMAL_NATIVE_EH',dict(row=row,jet=jet,native_EH=native,candidate_provenance=candidate['candidate_provenance']),stage_complete,records)
   if coordinate is None:
    phase=candidate_phase_normal_stress(s,c,D,eos,f,b,keep,child+'_NEW_phase')
    tt_stage('TRIAL_NORMAL_PHASE',dict(row=row,phase=phase,candidate_provenance=candidate['candidate_provenance']),stage_complete,records);own=ordinary
   else:
    phase=dict(value=dict(action=tt_zero((p,))),delta=dict(action=tt_zero((p,))),relative_phase_included_once=True)
    own=dict(value=dict(normal_density=tt_zero((p,4))),delta=dict(normal_density=tt_zero((p,4))))
   total=finite_candidate_total_normal(native,phase,own,f,b,keep,child+'_NEW_total')
   for word in (0,1):coeff[word][:,row,jet]=total['value']['hamiltonian'][word]
   fr_pair(child+'_completed_normal_coefficients',coeff,(p,4,4),keep)
   same_theta=fr_pair(child+'_initial_CMC_density',native['value']['initial_CMC_density'],(p,),keep)
   if theta is None:theta=tuple(a.copy() for a in same_theta)
   else:assert all(np.array_equal(a,b) for a,b in zip(theta,same_theta)),'One same-state initial CMC density across test ports'
   tt_stage('TRIAL_NORMAL_TOTAL',dict(row=row,jet=jet,total=total,completed_coefficients=coeff,initial_CMC_density=theta,relative_phase_count=1,ordinary_mean_count=1,candidate_provenance=candidate['candidate_provenance']),stage_complete,records)
 return dict(value=dict(normal_coefficients=coeff,initial_CMC_density=theta),delta=dict(normal_coefficients=tt_zero((p,4,4)),initial_CMC_density=tt_zero((p,))),normal_coordinate_order=('value','R','Z','t'),relative_phase_count=1,ordinary_label_count=1,completed_stages=records,zero_direction_only=True,physical_adoption=False)


def fresh_trial_sheet_normal(sheet_packet,source,labels,normal_test,keep,check,label,stage_complete):
 assert sheet_packet['original_source']==source['provenance'] and source['fixed_labels_and_positions_verified'] is True
 assert labels['existing_once_counted_branch_registered'] is True and labels['provenance']==source['provenance']
 assert all(np.all(w==0) for n in ('reference_dust_energy_weight','radiation_weights') for w in labels[n]),'Reference mean must not be counted on the galaxy sheet'
 sheet=sheet_packet['sheet'];records=[];n=len(source['R']);assert source['indices'].shape==source['right_weight'].shape==(n,)
 assert np.all(source['Z']==0) and source['indices'].dtype==np.int64 and np.all((source['indices']>=0)&(source['indices']<86))
 assert np.all((source['right_weight']>0)&(source['right_weight']<1)) and normal_test.shape==(4,87,45) and np.all(normal_test[~N.normal_test_mask()]==0)
 tt_stage('TRIAL_SHEET_ORDINARY_INPUT',dict(labels=labels,source=source,geometry=sheet_packet['record']),stage_complete,records)
 ordinary=finite_fixed_canonical_ordinary_point(sheet['geometry'],sheet['gauge'],labels,keep,label+'_NEW_ordinary')
 tt_stage('TRIAL_SHEET_ORDINARY',dict(ordinary=ordinary,source=source['provenance'],geometry=sheet_packet['record']),stage_complete,records)
 force=fr_pair(label+'_normal_density',ordinary['value']['normal_density'],(n,4),keep);out=tt_zero((4,87,45));test_value=np.zeros((n,4));env=np.zeros((4,87,45))
 for side,hat in ((0,1-source['right_weight']),(1,source['right_weight'])):
  for row in range(4):
   scale=source['R'] if row==1 else np.ones(n);val=fr_pair(label+'_current_force',P.a_mul64(hat,P.a_mul64(scale,P.a_slice(force,(slice(None),row)))),(n,),keep)
   ev=abs(hat*scale)*(abs(force[0][:,row])+abs(force[1][:,row]));test_value[:,row]+=hat*scale*normal_test[row,source['indices']+side,0]
   for node in range(87):
    take=np.flatnonzero(source['indices']+side==node)
    if len(take):
     subtotal=normal_pair_sum((val[0][take],val[1][take]),0);joined=P.a_add(P.a_slice(out,(row,node,0)),subtotal)
     for word in (0,1):out[word][row,node,0]=joined[word]
     env[row,node,0]+=np.sum(ev[take]);fr_pair(label+'_current_nodal',out,(4,87,45),keep)
 out=fr_pair(label+'_restricted_normal',N.paired_restrict_normal_rows(out),(4,87,45),keep);env=N.restrict_normal_rows(env)
 selected=normal_test!=0;nodal=fy_sum(P.a_mul64(normal_test[selected],tuple(a[selected] for a in out)),0)
 selected=test_value!=0;direct=fy_sum(P.a_mul64(test_value[selected],tuple(a[selected] for a in force)),0);gap=fr_pair(label+'_functional_gap',P.a_sub(nodal,direct),(),keep)
 bound=np.asarray(np.sum(abs(normal_test)*env)+np.sum(abs(test_value)*(abs(force[0])+abs(force[1]))));keep(label+'_functional_envelope',bound.copy());check(label+'_polynomial_transpose',gap[0]+gap[1],np.asarray(0.),bound)
 record=tt_stage('TRIAL_SHEET_NORMAL',dict(weak=out,functional_nodal=nodal,functional_direct=direct,gap=gap,envelope=bound,source=source['provenance'],mean_count=0,sheet_count=1,physical_adoption=False),stage_complete,records)
 return dict(weak=out,record=record,completed_stages=records,physical_adoption=False)


def fresh_trial_literal_column(column,keep,label,stage_complete):
 records=[];captured={};prefix=label+'_NEW_temporal_cache'
 def capture(name,a):captured[name]=np.asarray(a).copy();keep(name,a)
 cache=candidate_temporal_prepare(column['candidate'],column['reference'],capture,prefix)
 cache['formal_Iu']=tt_captured_pair(captured,prefix,'formal_I_times_u',(3784,3),keep,label+'_completed_formal_Iu')
 fr_pair(label+'_completed_gamma_squared',cache['gamma_squared'],(3784,),keep)
 tt_stage('TRIAL_NEW_TEMPORAL_CACHE',dict(cache=cache,candidate_provenance=column['candidate']['candidate_provenance']),stage_complete,records)
 gradient=candidate_literal_temporal_gradient_bridge(column['candidate'],cache,keep,label+'_NEW_literal_gradient')
 tt_stage('TRIAL_LITERAL_GRADIENT',dict(gradient=gradient,candidate_provenance=column['candidate']['candidate_provenance']),stage_complete,records)
 return dict(gradient=gradient,cache=cache,completed_stages=records,physical_adoption=False)


def fresh_trial_residual_packet(prepared,columns,mean_labels,Hbar,sheet_packet,sheet_source,sheet_labels,priors,normal_test,scalar_test,provenance,keep,check,label,stage_complete):
 fr_require(prepared,columns,provenance);assert len(mean_labels)==4 and callable(check) and callable(stage_complete)
 basis=prepared['basis'];records=[];normal_columns=[];literal_columns=[]
 assert normal_test.shape==(4,87,45) and scalar_test.shape==(87,45)
 assert np.all(normal_test[~N.normal_test_mask()]==0) and np.all(scalar_test[~P.scalar_mask()]==0)
 tt_stage('TRIAL_RESIDUAL_INPUT',dict(prepared_total=prepared['total_fields_record'],columns=[q['completed_stages'] for q in columns],fixed_priors=priors,normal_test=normal_test,scalar_test=scalar_test,provenance=provenance),stage_complete,records)
 for iq,column in enumerate(columns):
  normal_columns.append(fresh_trial_normal_column(column,mean_labels[iq],Hbar,keep,label+'_column%d'%iq,stage_complete))
  literal_columns.append(fresh_trial_literal_column(column,keep,label+'_column%d'%iq,stage_complete))
 sheet=fresh_trial_sheet_normal(sheet_packet,sheet_source,sheet_labels,normal_test,keep,check,label+'_sheet',stage_complete)
 global_rows=finite_candidate_global_normal_CMC(normal_columns,basis,normal_test,scalar_test,keep,check,label+'_NEW_global')
 tt_stage('TRIAL_GLOBAL_NORMAL_CMC',dict(rows=global_rows,sheet=sheet['record'],all_primary_coefficients_retained=True,physical_adoption=False),stage_complete,records)
 point={n:fr_join([q['candidate']['momenta'][key] for q in columns],shape,keep,label+'_NEW_point_'+n) for n,key,shape in (('native','native_density',(15136,99)),('metric','metric_total_density',(15136,6)))}
 point['phase']=fr_join([q['phase']['values']['p'] for q in columns],(15136,),keep,label+'_NEW_literal_phase_point')
 current={}
 for n,shape in (('native',(33,3,87,45)),('metric',(6,87,45)),('phase',(87,45))):
  if n=='native':value=cs_native_weak(point[n],basis,keep,label+'_NEW_registered_native')
  elif n=='metric':value=P.dd_metric_scatter(point[n],basis,keep)
  else:value=P.dd_scalar_scatter(point[n],basis,keep,label+'_NEW_phase_scatter')
  current[n]=fr_pair(label+'_NEW_current_'+n,value,shape,keep)
  tt_stage('TRIAL_FRESH_WEAK_CURRENT',dict(family=n,point=point[n],current=current[n],total_fields=prepared['total_fields_record'],physical_adoption=False),stage_complete,records)
 tt_stage('TRIAL_FRESH_WEAK_CURRENTS',dict(point=point,current=current,total_fields=prepared['total_fields_record'],physical_adoption=False),stage_complete,records)
 registered_phase_point=fr_join([q['phase']['values']['registered_p'] for q in columns],(15136,),keep,label+'_NEW_registered_phase_comparison_point')
 registered_phase_weak=fr_pair(label+'_NEW_registered_phase_comparison_weak',P.dd_scalar_scatter(registered_phase_point,basis,keep,label+'_NEW_registered_phase_comparison_scatter'),(87,45),keep)
 registered_phase_target=fr_pair(label+'_unchanged_registered_phase_comparison_target',priors['registered_phase'],(87,45),keep)
 assert all(np.all(w[~P.scalar_mask()]==0) for w in registered_phase_target)
 phase_bridge=dict(literal_minus_registered=fr_pair(label+'_literal_minus_registered_phase_weak',P.a_sub(current['phase'],registered_phase_weak),(87,45),keep),registered_target_minus_current=fr_pair(label+'_registered_phase_comparison_epsilon',P.a_sub(registered_phase_target,registered_phase_weak),(87,45),keep))
 tt_stage('TRIAL_PHASE_REGISTRATION_COMPARISON',dict(registered_point=registered_phase_point,registered_weak=registered_phase_weak,registered_target=registered_phase_target,bridges=phase_bridge,literal_charge_authority_not_replaced=True,physical_adoption=False),stage_complete,records)
 tensor=fr_join([q['york']['target'] for q in columns],(15136,3,3),keep,label+'_varying_York_target_tensor');six=cs_york_covector_six(tensor,keep,label+'_varying_York_target')
 targets=dict(native=priors['native'],metric=fr_pair(label+'_varying_York_weak_target',P.dd_metric_scatter(six,basis,keep),(6,87,45),keep),phase=priors['literal_phase']);epsilon={}
 for n,shape in (('native',(33,3,87,45)),('metric',(6,87,45)),('phase',(87,45))):
  targets[n]=fr_pair(label+'_fixed_or_prepared_target_'+n,targets[n],shape,keep);mask=np.broadcast_to(P.native_mask(),shape) if n=='native' else P.metric_mask() if n=='metric' else P.scalar_mask()
  assert all(np.all(w[~mask]==0) for w in targets[n]);epsilon[n]=fr_pair(label+'_target_minus_registered_current_'+n,P.a_sub(targets[n],current[n]),shape,keep)
 nominal=fr_pair(label+'_prepared_minus_nominal_metric_target',P.a_sub(targets['metric'],priors['nominal_metric']),(6,87,45),keep)
 tt_stage('TRIAL_CANONICAL_TARGET_EPSILON',dict(targets=targets,epsilon=epsilon,prepared_minus_nominal=nominal,original_targets_and_offsets_not_refitted=True,physical_adoption=False),stage_complete,records)
 ln=fr_join([q['gradient']['literal']['native'] for q in literal_columns],(15136,99),keep,label+'_literal_native_point');lm=fr_join([q['gradient']['literal']['metric_total'] for q in literal_columns],(15136,6),keep,label+'_literal_metric_point')
 weight=(basis['dv']/basis['R']).reshape(15136);keep(label+'_original_weight64',weight.copy())
 weighted_n=fr_pair(label+'_weighted_literal_native',P.a_mul64(weight[:,None],ln),(15136,99),keep);weighted_m=fr_pair(label+'_weighted_literal_metric',P.a_mul64(weight[:,None],lm),(15136,6),keep)
 modes=tuple(a.reshape(15136,33,3).transpose(1,0,2) for a in weighted_n);packed_literal=candidate_original_evaluation_transpose(modes,weighted_m,basis,keep,label+'_NEW_literal_weighted_Estar')
 packed_current=P.pack_dd(current['native'],current['metric']);packed_target=P.pack_dd(targets['native'],targets['metric']);packed_epsilon=P.pack_dd(epsilon['native'],epsilon['metric'])
 bridge=fr_pair(label+'_literal_minus_registered_weak',P.a_sub(packed_literal,packed_current),(403340,),keep);eL=fr_pair(label+'_mechanical_target_minus_literal_eL',P.a_sub(packed_target,packed_literal),(403340,),keep)
 fr_pair(label+'_eL_minus_epsilon_plus_literal_bridge',P.a_sub(eL,P.a_sub(packed_epsilon,bridge)),(403340,),keep)
 normal=fr_pair(label+'_unfeedbacked_total_weak_normal',P.a_add(global_rows['value']['weak_normal'],sheet['weak']),(4,87,45),keep)
 CMC=fr_pair(label+'_initial_weak_CMC',global_rows['value']['weak_initial_CMC'],(87,45),keep)
 record=tt_stage('TRIAL_CURRENT_LITERAL_AND_UNFEEDBACKED_RESIDUAL',dict(current=current,targets=targets,epsilon=epsilon,literal_mechanical=packed_literal,literal_minus_registered=bridge,mechanical_eL=eL,phase_eL=epsilon['phase'],phase_registration_comparison=phase_bridge,unfeedbacked_weak_normal=normal,initial_weak_CMC=CMC,time_primary_action_coefficients=global_rows['value']['time_primary_action_coefficients'],fresh_feedback_required=True,physical_adoption=False),stage_complete,records)
 return dict(status='FRESH_TOTAL_TRIAL_CURRENTS_TARGETS_LITERAL_BRIDGES_AND_UNFEEDBACKED_NORMAL_CMC_EVALUATED',record=record,completed_stages=records,normal_columns=normal_columns,literal_columns=literal_columns,sheet=sheet,global_rows=global_rows,current=current,targets=targets,epsilon=epsilon,literal_mechanical=packed_literal,literal_minus_registered=bridge,mechanical_eL=eL,phase_eL=epsilon['phase'],phase_registration_comparison=phase_bridge,unfeedbacked_weak_normal=normal,initial_weak_CMC=CMC,relative_phase_count=1,mean_count=1,sheet_count=1,fresh_gauge_C_and_current_eL_adjoint_or_certified_bound_required=True,frozen_feedback_value_used=False,rounded_pressure_program_AD_claimed=False,stationarity_or_canonical_normal_CMC_solution_admitted=False,physical_adoption=False)
