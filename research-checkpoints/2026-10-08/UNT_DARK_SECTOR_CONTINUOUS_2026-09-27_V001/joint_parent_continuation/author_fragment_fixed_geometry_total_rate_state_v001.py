"""HELD finite rate-state update at fixed geometry; root owns release/execution.
No FY/configuration/EOS/ordinary primal replay. Genuine TOTAL rates are retained.
"""
FIXED_RATE_STATE_AUTHOR_DRAFT=True
FIXED_RATE_STATE_AUTHORING_IN_PROGRESS=False
FIXED_RATE_STATE_BASELINE_CLOSURE=(None,None,None,None)
FIXED_RATE_STATE_CORRECTION_CLOSURE=(None,None,None,None)
FIXED_RATE_STATE_UPDATED_PHASE_CLOSURE=(None,None,None,None)
FIXED_RATE_STATE_FIXED_BINDING=(None,None)
FIXED_RATE_STATE_SOURCE_PINS={
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_candidate_native_EH_normal_v003.py':'5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499',
 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py':'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db'}

def frs_pair(label,x,shape,keep):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 assert all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x),label
 return fy_keep(label,tuple(a.copy() for a in x),keep)

def frs_require(provenance):
 assert not FIXED_RATE_STATE_AUTHOR_DRAFT and not FIXED_RATE_STATE_AUTHORING_IN_PROGRESS
 for q in (FIXED_RATE_STATE_BASELINE_CLOSURE,FIXED_RATE_STATE_CORRECTION_CLOSURE,FIXED_RATE_STATE_UPDATED_PHASE_CLOSURE,FIXED_RATE_STATE_FIXED_BINDING):assert all(x is not None for x in q)
 for n,q in (('baseline_closure',FIXED_RATE_STATE_BASELINE_CLOSURE),('correction_closure',FIXED_RATE_STATE_CORRECTION_CLOSURE),('updated_phase_closure',FIXED_RATE_STATE_UPDATED_PHASE_CLOSURE),('fixed_binding',FIXED_RATE_STATE_FIXED_BINDING)):assert provenance[n]==q
 assert provenance['source_pins']==FIXED_RATE_STATE_SOURCE_PINS and provenance['all_source_seals_authenticated'] is True
 assert provenance['correction_original_six_gates_admitted'] is True and provenance['original_fixed_references_verified'] is True and provenance['physical_adoption'] is False
 assert len(provenance['columns'])==4 and provenance['original_owned_TOTAL_time_words'] and provenance['unchanged_original_targets']

def frs_stage(kind,payload,complete,records):
 assert callable(complete),'Containing owner must seal a completed stage before the next stage'
 q=complete(kind,payload);assert isinstance(q,dict) and all(isinstance(q[n],str) and q[n] for n in ('file','sha256','commit_file','commit_sha256'));records.append(q);return q

def prepare_fixed_geometry_rate_increment(native_nodes,metric_nodes,basis,provenance,keep,label,stage_complete):
 frs_require(provenance)
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 masks={'native':np.broadcast_to(P.native_mask(),(33,3,87,45)),'metric':P.metric_mask()};supplied={}
 for n,x,shape in (('native',native_nodes,(33,3,87,45)),('metric',metric_nodes,(6,87,45))):
  supplied[n]=frs_pair(label+'_supplied_'+n+'_increment',x,shape,keep);assert all(np.all(a[~masks[n]]==0) for a in supplied[n])
 native=frs_pair(label+'_NEW_original_E_increment',P.dd_native_node_value(supplied['native'],basis,keep,jet=0),(33,15136,3),keep)
 metric=frs_pair(label+'_NEW_original_F_physical6_increment',P.dd_metric_node_value(supplied['metric'],basis,keep,jet=0),(15136,6),keep)
 records=[];ref=frs_stage('RATE_INCREMENT',dict(native_nodes=supplied['native'],metric_nodes=supplied['metric'],native=native,metric=metric,provenance=provenance,physical_adoption=False),stage_complete,records)
 return dict(native=native,metric=metric,basis=basis,provenance=provenance,increment_record=ref,point_first_TOTAL_addition=True,physical_adoption=False)

def fixed_geometry_rate_state_column(column,native_increment,metric_increment,Hbar,provenance,keep,label,stage_complete,row_complete):
 frs_require(provenance);p=len(column['candidate']['c']['N']);assert np.isfinite(Hbar)
 assert column['provenance']==provenance['columns'][column['column']] and column['fixed_geometry_identity_verified'] is True and column['updated_phase_identity_verified'] is True
 assert column['unchanged_curvature_and_ordinary_identity_verified'] is True and column['owned_TOTAL_time_word_identity_verified'] is True
 s,c=column['candidate']['s'],column['candidate']['c'];records=[];zero=lambda shape:P.a_dd(np.zeros(shape))
 nr=frs_pair(label+'_NEW_native_increment',native_increment,(p,99),keep);mr=frs_pair(label+'_NEW_physical6_increment',metric_increment,(p,6),keep)
 ua=frs_pair(label+'_closed_TOTAL_covector_u_first',column['covectors']['u_jets'],(p,4,3),keep)
 za=frs_pair(label+'_closed_TOTAL_covector_z_first',column['covectors']['z_jets'],(32,p,4,3),keep)
 ha=frs_pair(label+'_closed_TOTAL_h_first',column['h_first'],(p,4,3,3),keep)
 ht=frs_pair(label+'_closed_TOTAL_hdot',column['mechanical']['h_dot'],(p,3,3),keep)
 assert all(np.array_equal(a[:,0].view(np.uint64),b.view(np.uint64)) for a,b in zip(ha,ht))
 Na=frs_pair(label+'_unchanged_owned_N_first',column['gauge']['N_jets'],(p,4),keep);ba=frs_pair(label+'_unchanged_owned_beta_first',column['gauge']['beta_jets'],(p,4,3),keep)
 E0=frs_pair(label+'_unchanged_owned_lowered_E0',column['reference']['E0'],(p,4,4,4),keep)
 Lie=frs_pair(label+'_unchanged_closed_Lie_beta_h',column['Lie_beta_h'],(p,3,3),keep)
 phase=frs_pair(label+'_unchanged_UPDATED_phase_covector',column['updated_phase_covector'],(p,4),keep)
 nu=tuple(a.reshape(p,33,3) for a in nr);vu=P.a_add(P.a_slice(ua,(slice(None),0)),tuple(a[:,0].copy() for a in nu))
 vu=frs_pair(label+'_NEW_TOTAL_u_time',vu,(p,3),keep)
 vz=P.a_add(P.a_slice(za,(slice(None),slice(None),0)),tuple(a[:,1:].transpose(1,0,2).copy() for a in nu));vz=frs_pair(label+'_NEW_TOTAL_z_time',vz,(32,p,3),keep)
 Q=zero((p,3,3))
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for w in (0,1):Q[w][:,i,j]=Q[w][:,j,i]=mr[w][:,slot]
 frs_pair(label+'_NEW_symmetric_physical_hdot_increment',Q,(p,3,3),keep)
 newht=frs_pair(label+'_NEW_TOTAL_hdot',P.a_add(ht,Q),(p,3,3),keep)
 uan=tuple(a.copy() for a in ua);zan=tuple(a.copy() for a in za);han=tuple(a.copy() for a in ha)
 for w in (0,1):uan[w][:,0]=vu[w];zan[w][:,:,0]=vz[w];han[w][:,0]=newht[w]
 for n,new,old,axis in (('u_first',uan,ua,1),('z_first',zan,za,2),('h_first',han,ha,1)):
  assert all(np.array_equal(np.take(a,(1,2,3),axis=axis).view(np.uint64),np.take(b,(1,2,3),axis=axis).view(np.uint64)) for a,b in zip(new,old));fy_keep(label+'_NEW_TOTAL_'+n,new,keep)
 frs_stage('RATE_STATE_INPUT',dict(h_first=han,u_jets=uan,z_jets=zan,N_jets=Na,beta_jets=ba,E0=E0,updated_phase=phase,provenance=column['provenance'],point_first_addition=True,nodal_add_then_lift_equivalence_earned=False),stage_complete,records)
 captured={};jetlabel=label+'_NEW_raw225_first_jets'
 def jet_keep(name,value):
  if name in {jetlabel+'_'+n+'_'+w for n in ('inverse_first','up_first','gamma_first') for w in ('hi','lo')}:captured[name]=np.asarray(value).copy()
  return keep(name,value)
 jets,envelopes=fa_new_first_jets(s,c,han,Na,ba,uan,zan,E0,jet_keep,jetlabel)
 first={}
 for n,shape in (('inverse_first',(p,4,3,3)),('up_first',(p,4,3)),('gamma_first',(p,4))):first[n]=frs_pair(label+'_NEW_'+n,tuple(captured[jetlabel+'_'+n+'_'+w] for w in ('hi','lo')),shape,keep)
 frs_stage('RATE_STATE_FIRST_JETS',dict(jets=jets,envelopes=envelopes,first=first,owned_covectors=dict(u_jets=uan,z_jets=zan),fixed_E0=E0,provenance=column['provenance']),stage_complete,records)
 features=P.paired_current_affine_features(s,c,jets,keep,label+'_NEW_current_features')
 frs_stage('RATE_STATE_FEATURES',dict(features=features,current_U_tensor_Z_retained=True,provenance=column['provenance']),stage_complete,records)
 momenta=P.paired_current_affine_momenta(s,c,features,jets,keep,label+'_NEW_current_momenta')
 frs_stage('RATE_STATE_MOMENTA',dict(momenta=momenta,all99_native_and6_physical_metric_entries=True,offdiagonal_registered_twice_upper_once=True,provenance=column['provenance']),stage_complete,records)
 candidate=dict(column['candidate'],features=features,momenta=momenta,jets=jets,jet_envelopes=envelopes)
 denom=P.a_mul64(2.,P.a_dd(c['N']));fy_keep(label+'_NEW_KADM_denominator',denom,keep)
 KADM=frs_pair(label+'_NEW_KADM',fy_div(P.a_sub(newht,Lie),tuple(a[:,None,None] for a in denom),keep,label+'_NEW_KADM_division'),(p,3,3),keep)
 fy_keep(label+'_NEW_KGamma_minus_KADM',P.a_sub(momenta['K'],KADM),keep)
 fy_keep(label+'_NEW_Ktrace_Gamma_minus_ADM',P.a_sub(momenta['Ktrace'],fy_contract(P.a_dd(c['ih']),KADM)),keep)
 A=P.a_dd(np.einsum('pi,jpi->jp',c['up'],s['z'][:,:,1:]))
 values=dict(h=P.a_dd(c['h']),ih=P.a_dd(c['ih']),mu=P.a_dd(c['sqrt_h']),N=P.a_dd(c['N']),beta=P.a_dd(c['beta']),up=P.a_dd(c['up']),gamma=P.a_dd(c['gamma']),A=A,U=P.a_dd(s['U']),z=P.a_dd(s['z']),g=P.a_dd(s['g']),hi=P.a_dd(s['hi']),uc=P.a_dd(s['uc']),P=P.a_dd(s['P']),phi=phase,Z=P.a_dd(s['Z']),z2=P.a_dd(s['z2']),dens=P.a_dd(c['dens']),h_first=han,N_first=Na,beta_first=ba,z_spatial_first=zan,KADM=KADM,**first,**jets)
 state={n:(a,zero(a[0].shape)) for n,a in values.items()}
 for n,a in values.items():fy_keep(label+'_NEW_value_only_state_'+n,a,keep)
 needed=('nu','nz','q','V','D','F','V_raised','D_raised','Fup','a')
 contact=dict(state=state,delta_features={'paired':{n:zero(features['paired'][n][0].shape) for n in needed}},delta_momenta={n:zero(momenta[n][0].shape) for n in ('K','Ktrace','metric_EH_tensor')},direction_is_zero_for_value_evaluation_only=True,configuration_JVP_not_supplied=True)
 curvature={n:(frs_pair(label+'_unchanged_intrinsic_'+n,column['intrinsic_curvature'][n],shape,keep),zero(shape)) for n,shape in (('Q',(p,)),('V',(p,3)))}
 fixed={n:frs_pair(label+'_unchanged_'+n,column['fixed_terms'][n],(p,4,4),keep) for n in ('phase_action','ordinary_Hamiltonian')}
 assert column['fixed_terms']['relative_phase_count']==column['fixed_terms']['ordinary_label_count']==1
 assert all(np.all(a[:,:,1:]==0) for pair in fixed.values() for a in pair),'Literal phase/ordinary have no test firstjet action at fixed state'
 coefficients=zero((p,4,4));native_EH_coefficients=zero((p,4,4));theta=None;rows=[]
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
   if row==0:
    if coordinate is None:f[:]=1.
    else:df[:,coordinate]=1.
   elif coordinate is None:b[:,row-1]=1.
   else:db[:,coordinate,row-1]=1.
   tag=label+'_row%d_jet%d'%(row,jet)
   result=finite_candidate_native_EH_normal(candidate,contact,curvature,f,df,b,db,Hbar,column['reference'],keep,tag+'_NEW_native_EH_value')
   assert result['relative_phase_included'] is False and result['all_four_coordinate_test_jets_retained'] is True
   phase_action=P.a_slice(fixed['phase_action'],(slice(None),row,jet));ordinary_H=P.a_slice(fixed['ordinary_Hamiltonian'],(slice(None),row,jet))
   joined_action=fy_keep(tag+'_NEW_native_plus_unchanged_phase_action',P.a_add(result['value']['action'],phase_action),keep)
   total_action=fy_keep(tag+'_NEW_total_action',P.a_sub(joined_action,ordinary_H),keep);H=fy_keep(tag+'_NEW_total_Hamiltonian',P.a_mul64(-1.,total_action),keep)
   for w in (0,1):coefficients[w][:,row,jet]=H[w];native_EH_coefficients[w][:,row,jet]=result['value']['hamiltonian'][w]
   if theta is None:theta=tuple(a.copy() for a in result['value']['initial_CMC_density'])
   else:assert all(np.array_equal(a.view(np.uint64),bw.view(np.uint64)) for a,bw in zip(theta,result['value']['initial_CMC_density']))
   fy_keep(tag+'_completed_NEW_normal_coefficients',coefficients,keep);fy_keep(tag+'_completed_NEW_CMC_density',theta,keep)
   rows.append(frs_stage('RATE_STATE_NORMAL_TEST',dict(row=row,jet=jet,coordinate=coordinate,result=result,total_action=total_action,total_Hamiltonian=H,initial_CMC_density=theta,relative_phase_count=1,ordinary_label_count=1,provenance=column['provenance']),lambda kind,payload:row_complete(row,jet,kind,payload),records))
 part=dict(value=dict(normal_coefficients=coefficients,initial_CMC_density=theta),delta=dict(normal_coefficients=zero((p,4,4)),initial_CMC_density=zero((p,))),native_EH_coefficients=native_EH_coefficients,normal_coordinate_order=('value','R','Z','t'),relative_phase_count=1,ordinary_label_count=1,new_point_current=momenta,new_TOTAL_time_words=dict(u_jets=uan,z_jets=zan,h_dot=newht),stage_refs=records,normal_test_refs=rows,configuration_held=True,updated_phase_held=True,normal_configuration_JVP_earned=False,zero_direction_is_value_evaluation_only=True,physical_adoption=False)
 part['column_record']=frs_stage('RATE_STATE_COLUMN',part,stage_complete,records);return part

def fixed_geometry_rate_state_packet(columns,increment,Hbar,normal_test,scalar_test,keep,check,label,stage_complete,row_complete,column_complete):
 provenance=increment['provenance'];frs_require(provenance);basis=increment['basis'];assert len(columns)==4
 parts=[];column_refs=[];native=[];metric=[]
 for iq,column in enumerate(columns):
  assert column['column']==iq and np.array_equal(column['candidate']['s']['R'],basis['R'][iq]);sl=slice(iq*3784,(iq+1)*3784)
  nr=tuple(a[:,sl].transpose(1,0,2).reshape(3784,99).copy() for a in increment['native']);mr=tuple(a[sl].copy() for a in increment['metric'])
  part=fixed_geometry_rate_state_column(column,nr,mr,Hbar,provenance,keep,label+'_column%d'%iq,lambda kind,payload:stage_complete(iq,kind,payload),lambda row,jet,kind,payload:row_complete(iq,row,jet,kind,payload))
  current=part['new_point_current'];native.append(tuple(a.copy() for a in current['native_density']));metric.append(tuple(a.copy() for a in current['metric_total_density']))
  ref=column_complete(iq,part);assert ref==part['column_record'];column_refs.append(ref)
  parts.append({n:part[n] for n in ('value','delta','normal_coordinate_order','relative_phase_count','ordinary_label_count')})
 modes=tuple(np.concatenate([a[w] for a in native]).reshape(15136,33,3).transpose(1,0,2) for w in (0,1));metric_point=tuple(np.concatenate([a[w] for a in metric]) for w in (0,1))
 weak_native=fy_keep(label+'_NEW_full_native_current',P.dd_native_scatter(modes,basis,keep),keep);weak_metric=fy_keep(label+'_NEW_full_metric_current',P.dd_metric_scatter(metric_point,basis,keep),keep)
 normal=finite_candidate_global_normal_CMC(parts,basis,normal_test,scalar_test,keep,check,label+'_NEW_value_normal_CMC')
 return dict(current=dict(native=weak_native,metric=weak_metric),normal_CMC=normal,columns=column_refs,provenance=provenance,point_first_TOTAL_addition=True,nodal_add_then_lift_construction_gap_external=True,original_canonical_targets_unchanged=True,phase_current_words_unchanged=True,spatial_metric_words_unchanged=True,all_genuine_time_components_updated=True,canonical_after_finite_update_admission_external=True,stationarity_feedback_external=True,physical_metric_or_normal_CMC_adoption=False,physical_adoption=False)
