"""HELD single-column configuration JVP at genuine NEW139 point TOTAL rates.
Globals np/P; reviewed nmg_pair/equal/stage114 and unchanged cq_*290.
The mechanical column is the authenticated114 hydration result, not an old
normal/configuration contact. Invariant cache ownership remains explicit.
No139/225/EOS/current/FY primal producer or nodal TOTAL reconstruction occurs.
"""
NEW139_CONFIGURATION_AUTHOR_DRAFT=True
NEW139_CONFIGURATION_AUTHORING_IN_PROGRESS=False
NEW139_CONFIGURATION_FINITE_CLOSURE=(None,None,None,None)
NEW139_CONFIGURATION_INVARIANT_CLOSURES={'phase':(None,None,None,None),'normal_phase_join':(None,None,None,None),'York_anchor':(None,None,None,None),'material':(None,None,None,None)}
NEW139_CONFIGURATION_SOURCE_PINS={
 'author_fragment_NEW139_mechanical_gauge_preparation_v003.py':'244a0d50f89b72dbc2447eba66939ddcd5cd6a2b94483bb7595c0a1e41249dc7',
 'author_fragment_candidate_whole_configuration_york_contact_v001.py':'0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py':'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_candidate_native_EH_normal_v003.py':'5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a'}

def nqc_require(admission):
 assert not NEW139_CONFIGURATION_AUTHOR_DRAFT and not NEW139_CONFIGURATION_AUTHORING_IN_PROGRESS
 normalize=lambda closure:tuple(tuple(q) for q in closure)
 for closure in (NEW139_CONFIGURATION_FINITE_CLOSURE,*NEW139_CONFIGURATION_INVARIANT_CLOSURES.values()):
  assert len(closure)==4 and all(isinstance(q,(tuple,list)) and len(q) in (2,3) and all(v is not None for v in q) for q in closure),'Future CLOSED bindings required'
 assert normalize(admission['finite_closure'])==normalize(NEW139_CONFIGURATION_FINITE_CLOSURE)
 assert set(admission['invariant_closures'])==set(NEW139_CONFIGURATION_INVARIANT_CLOSURES)
 for n,closure in NEW139_CONFIGURATION_INVARIANT_CLOSURES.items():assert normalize(admission['invariant_closures'][n])==normalize(closure)
 assert admission['source_pins']==NEW139_CONFIGURATION_SOURCE_PINS and admission['physical_adoption'] is False
 for n in ('all_invariant_seals_authenticated','same_original_basis_and_fixed_sources_verified','same_original_priors_and_York_reference_verified','same_phase_operands_verified','same_fixed_geometry_and_gauge_verified'):assert admission[n] is True,n
 assert admission['updated_phase_state_owner']==13764 and type(admission['column']) is int and 0<=admission['column']<4

def prepare_NEW139_configuration_york_column(mechanical_column,invariant,admission,keep,label,stage_complete):
 nqc_require(admission);fresh=mechanical_column;s,c=fresh['candidate']['s'],fresh['candidate']['c'];p=len(c['N']);assert p==3784 and callable(stage_complete)
 assert fresh['physical_adoption'] is False and fresh['same_candidate_provenance']['column']==admission['column']
 assert tuple(tuple(q) for q in fresh['same_candidate_provenance']['finite_closure'])==tuple(tuple(q) for q in NEW139_CONFIGURATION_FINITE_CLOSURE)
 assert fresh['input_record']==admission['mechanical_hydration_record'] and fresh['source_records']==admission['NEW139_selected_records']
 for n in ('B','GC','ALPHA','ELL','C'):assert admission['material_constants'][n]==getattr(P,n)
 assert invariant['closed_source_refs']==admission['invariant_source_refs'] and invariant['closed_source_refs']
 phase=invariant['phase'];ns=invariant['normal_s'];nc=invariant['normal_c'];assert phase['physical_adoption'] is False and phase['EOS_values_recomputed'] is False
 for n in ('g','hi','U','uc','P'):
  nmg_equal(label+'_same_normal_raw_'+n,ns[n],P.a_dd(s[n]),keep)
  if n in phase['s']:nmg_equal(label+'_same_cached_phase_'+n,phase['s'][n],ns[n],keep)
 nmg_equal(label+'_same_phase_covector',phase['s']['phi'],fresh['updated_phase_pair'],keep);nmg_equal(label+'_same_normal_phase',ns['phi'],phase['s']['phi'],keep)
 for n in ('N','beta','h','ih','u','mu'):
  nmg_equal(label+'_same_normal_raw_'+n,nc[n],P.a_dd(c['sqrt_h' if n=='mu' else n]),keep)
  if n in phase['c']:nmg_equal(label+'_same_cached_phase_'+n,phase['c'][n],nc[n],keep)
 constants=phase['constants'];assert constants['eps']==1e-5 and constants['relative_phase_coefficient']==1. and constants['synthetic_control'] is False
 for n in ('X','u','p','H'):nmg_pair(label+'_inherited_phase_'+n,phase['values'][n],(p,),keep)
 assert np.all(phase['values']['X'][0]-abs(phase['values']['X'][1])>0) and np.all(phase['values']['u'][0]-abs(phase['values']['u'][1])>0) and np.all(constants['eps']-phase['values']['u'][0]-abs(phase['values']['u'][1])>0)
 york=invariant['york'];shapes=dict(h=(p,3,3),ih=(p,3,3),mu=(p,),h_spatial_jets=(p,2,3,3),T=(p,3,3),kappa=(p,),trace_part=(p,),inverse_lam=(p,),FY_target=(p,3,3),target=(p,3,3),tau=(p,))
 for n,shape in shapes.items():nmg_pair(label+'_inherited_York_'+n,york[n],shape,keep)
 for n in ('h','h_spatial_jets'):nmg_equal(label+'_same_true_geometry_'+n,york[n],fresh['geometry'][n],keep)
 ref=invariant['york_reference'];nmg_pair(label+'_fixed_L_maps',ref['L_maps'],(p,3,3,3,3),keep)
 for n,shape in (('target_raising_inverse',(p,3,3)),('mu_owned',(p,))):keep(label+'_fixed_reference_'+n,np.asarray(ref[n]).copy());assert ref[n].shape==shape and ref[n].dtype==np.float64 and np.all(np.isfinite(ref[n]))
 assert np.all(ref['mu_owned']>0);kbound=np.sum((abs(york['h'][0])+abs(york['h'][1]))*(abs(york['ih'][0])+abs(york['ih'][1])),axis=(1,2));keep(label+'_cached_York_kappa_uncancelled_envelope',kbound.copy());assert np.all(york['kappa'][0]-abs(york['kappa'][1])>2e-11*kbound)
 assert len(invariant['phase_normal_prefixes'])==4 and len(set(invariant['phase_normal_prefixes']))==4 and invariant['phase_normal_provenance']
 for prefix in invariant['phase_normal_prefixes']:
  for name in cached_updated_phase_contact_names(prefix,normal=True):assert name in invariant['phase_normal_data'],'Missing authentic phase VALUE cache member'
 labels=invariant['mean_labels'];assert labels['existing_once_counted_branch_registered'] is True and labels['radiation_weights'][0].shape==labels['radiation_weights'][1].shape==(128,p) and labels['radiation_covectors'][0].shape==labels['radiation_covectors'][1].shape==(128,p,3)
 provenance=dict(updated_phase_state_owner=13764,same_candidate_geometry_and_current_mechanical_rates=True,fixed_reference_longitudinal_chart=True,NEW139_point_TOTAL_input=fresh['input_record'],original_invariant_sources=invariant['closed_source_refs'],original_invariant_provenance=invariant['provenance'],physical_adoption=False)
 column={n:fresh[n] for n in ('candidate','geometry','gauge','covectors','mechanical','reference')}
 column.update({n:invariant[n] for n in ('phase','normal_s','normal_c','phase_normal_data','phase_normal_prefixes','phase_normal_provenance','mean_labels','york','york_reference')});column.update(provenance=provenance,NEW139_admission=dict(admission),original_mechanical_hydration_record=fresh['input_record'],physical_adoption=False)
 records=[];record=nmg_stage('NEW139_CONFIGURATION_CACHE',dict(column=admission['column'],prepared=column,source_records=fresh['source_records'],invariant_sources=invariant['closed_source_refs'],cached_phase_or_FY_or_current_primal_recomputed=False,old_rate_configuration_contact_relabelled=False,physical_adoption=False),stage_complete,records)
 column['configuration_cache_record']=record;return column

def NEW139_configuration_york_column_JVP(column,direction,direction_registration,Hbar,keep,check,label,test_complete,column_complete):
 nqc_require(column['NEW139_admission']);assert callable(test_complete) and callable(column_complete) and column['physical_adoption'] is False
 assert direction_registration['column']==column['NEW139_admission']['column'] and direction_registration['same_original_basis_verified'] is True and direction_registration['original_290_nodal_masks_and_jet_map_verified'] is True
 assert direction_registration['basis_record']==column['NEW139_admission']['original_basis_record'] and direction_registration['direction_record']
 assert np.isfinite(Hbar) and Hbar>0 and Hbar==column['NEW139_admission']['Hbar'] and set(direction)=={'rho','rho_gradient','W_jet','t'}
 for n,shape in (('rho',(3784,)),('rho_gradient',(3784,2)),('W_jet',(3784,3,3)),('t',(3784,))):nmg_pair(label+'_NEW_direction_'+n,direction[n],shape,keep)
 rows=[];native_EH_coefficients=P.a_dd(np.zeros((3784,4,4)))
 def completed(row,jet,data):
  value=nmg_pair(label+'_row%d_jet%d_NEW_native_EH_normal_JVP'%(row,jet),data['native']['delta']['hamiltonian'],(3784,),keep)
  for w in (0,1):native_EH_coefficients[w][:,row,jet]=value[w]
  nmg_pair(label+'_completed_native_EH_Bq_coefficients',native_EH_coefficients,(3784,4,4),keep)
  payload=dict(row=row,jet=jet,result=data,configuration_cache=column['configuration_cache_record'],direction_registration=direction_registration,admission=column['NEW139_admission'],physical_adoption=False)
  return nmg_stage('NEW139_CONFIGURATION_NORMAL_TEST',payload,lambda kind,words:test_complete(row,jet,kind,words),rows)
 part=candidate_configuration_york_column(column,direction,Hbar,keep,check,label,completed);assert len(rows)==16 and part['tests']==rows
 point={n:nmg_pair(label+'_NEW_point_current_JVP_'+n,part['contact']['delta_momenta'][key],(3784,width),keep) for n,key,width in (('native','native_density',99),('metric','metric_total_density',6))};point['phase']=nmg_pair(label+'_NEW_point_literal_phase_JVP',part['eos']['delta']['p'],(3784,),keep)
 tensor=nmg_pair(label+'_NEW_varying_York_target_tensor',part['target_direction']['target'],(3784,3,3),keep);nmg_pair(label+'_NEW_varying_target_asymmetry',P.a_sub(tensor,tuple(a.swapaxes(-1,-2) for a in tensor)),(3784,3,3),keep);six=[]
 for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2)):
  x=P.a_slice(tensor,(slice(None),i,j));six.append(x if i==j else P.a_add(x,P.a_slice(tensor,(slice(None),j,i))))
 target=nmg_pair(label+'_NEW_target_physical_covector_six',P.a_stack(six,-1),(3784,6),keep)
 canonical={**point,'metric':nmg_pair(label+'_NEW_registered_current_minus_varying_target',P.a_sub(point['metric'],target),(3784,6),keep)}
 epsilon={n:nmg_pair(label+'_NEW_epsilon_JVP_'+n,P.a_mul64(-1.,x),x[0].shape,keep) for n,x in canonical.items()}
 primary=nmg_pair(label+'_NEW_time_primary_action_JVP',P.a_mul64(-1.,P.a_slice(part['normal_coefficients'],(slice(None),slice(None),3))),(3784,4),keep)
 result=dict(column_result=part,current_point_JVP=point,prepared_York_target_tensor_JVP=tensor,prepared_York_target_covector_six_JVP=target,canonical_point_JVP=canonical,canonical_epsilon_point_JVP=epsilon,native_EH_Bq_coefficients_JVP=native_EH_coefficients,normal_coefficients_JVP=part['normal_coefficients'],time_primary_action_coefficients_point_JVP=primary,initial_CMC_density_JVP=part['initial_CMC_density'],completed_normal_test_refs=rows,configuration_cache_record=column['configuration_cache_record'],direction_registration=direction_registration,W_t_direct_current_and_normal_and_CMC_analytic_zero=True,W_t_varying_York_target_JVP_retained=True,original_E_F_scalar_and_normal_scatter_external=True,current_priors_and_epsilon_bookkeeping_owned_by_original126=True,source_uncancelled_enclosure_and_fullweak_controls_external=True,Legendre_gauge_feedback_included=False,old29272_contact_reused=False,old8526_role_scratch_released=False,physical_adoption=False)
 result['column_record']=nmg_stage('NEW139_CONFIGURATION_JVP',result,column_complete,[]);return result
