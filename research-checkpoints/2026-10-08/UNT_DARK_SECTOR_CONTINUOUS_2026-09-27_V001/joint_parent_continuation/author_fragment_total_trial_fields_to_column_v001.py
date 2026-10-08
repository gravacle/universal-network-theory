"""HELD total-trial addition/lifting and fresh column primal handoff.
Import-free definitions only; globals np/P/N and exact selected source kernels.
The root containing owner authenticates closed baseline/correction/fixed sources,
provides the shared exact-product arithmetic namespace and mandatory stage seals.
No producer, old value/action/EOS replay, solve, residual or physical admission.
"""
TOTAL_TRIAL_AUTHOR_DRAFT=True
TOTAL_TRIAL_AUTHORING_IN_PROGRESS=False
TOTAL_TRIAL_BASELINE_CLOSURE=(None,None,None,None)
TOTAL_TRIAL_CORRECTION_CLOSURE=(None,None,None,None)
TOTAL_TRIAL_FIXED_BINDING=(None,None)
TOTAL_TRIAL_SOURCE_PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_candidate_whole_configuration_york_contact_v001.py': '0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd', 'author_fragment_phase_fixed_weak_charge_response_core_v001.py': '331fb805f572de4257f76e879ba28ceef5e20d4cb4898260e712c95efb553c2c', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_finite_candidate_configuration_contact_v001.py': '7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_fixed_label_finite_sheet_geometry_v002.py': '556bac0713c74947b0abece865bf7e74c3d3b212029af1248aa7dd0af525a661', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd'}


def tt_pair(label,x,shape,keep):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 assert all(isinstance(a,np.ndarray) and a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a)) for a in x)
 for word,a in zip(('hi','lo'),x):keep(label+'_'+word,a.copy())
 return tuple(a.copy() for a in x)


def tt_zero(shape):return P.a_dd(np.zeros(shape))


def tt_add(label,before,increment,shape,keep):
 before=tt_pair(label+'_previous_total',before,shape,keep);increment=tt_pair(label+'_NEW_increment',increment,shape,keep)
 after=tt_pair(label+'_updated_total',P.a_add(before,increment),shape,keep);words=[]
 for term in (before[0],before[1],increment[0],increment[1],-after[0],-after[1]):
  accumulator=term;partial=[]
  for word in words:accumulator,low=P.a_sum(accumulator,word);partial.append(low)
  words=partial+[accumulator]
 keep(label+'_six_word_addition_defect',np.stack(words).copy())
 return after


def tt_stage(stage,payload,stage_complete,records):
 assert callable(stage_complete),'Containing owner must seal every completed child before the next child'
 ref=stage_complete(stage,payload);records.append(ref)
 assert isinstance(ref,dict) and all(isinstance(ref[n],str) and ref[n] for n in ('file','sha256','commit_file','commit_sha256'))
 return ref


def tt_require(provenance):
 assert not TOTAL_TRIAL_AUTHOR_DRAFT and not TOTAL_TRIAL_AUTHORING_IN_PROGRESS
 assert all(x is not None for q in (TOTAL_TRIAL_BASELINE_CLOSURE,TOTAL_TRIAL_CORRECTION_CLOSURE,TOTAL_TRIAL_FIXED_BINDING) for x in q),'Future natural closures/source binding required before supplied operands'
 assert provenance['baseline_closure']==TOTAL_TRIAL_BASELINE_CLOSURE and provenance['correction_closure']==TOTAL_TRIAL_CORRECTION_CLOSURE and provenance['fixed_binding']==TOTAL_TRIAL_FIXED_BINDING
 assert provenance['source_pins']==TOTAL_TRIAL_SOURCE_PINS and provenance['all_source_seals_authenticated'] is True and provenance['original_fixed_references_verified'] is True and provenance['physical_adoption'] is False
 assert len(provenance['columns'])==4 and provenance['sheet_source'] and provenance['phase_baseline_source']


def prepare_total_trial_fields(previous,correction,basis,provenance,keep,label,stage_complete):
 tt_require(provenance)
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and basis['r'].shape==(87,) and basis['z'].shape==(45,)
 for n,a in basis.items():keep(label+'_unchanged_basis_'+n,np.asarray(a).copy())
 assert np.all(basis['R']>0) and np.all(basis['dv']>0)
 masks=N.normal_test_mask();assert [int(np.count_nonzero(x)) for x in masks]==[3740,3740,3655,3740]
 specs={'chi':((87,45),masks[0]),'W':((3,87,45),masks[1:]),'t':((87,45),P.scalar_mask()),'native':((33,3,87,45),np.broadcast_to(P.native_mask(),(33,3,87,45))),'metric':((6,87,45),P.metric_mask()),'phase':((87,45),P.scalar_mask())}
 total={}
 for n,(shape,mask) in specs.items():
  step=tt_pair(label+'_increment_'+n,correction[n],shape,keep);assert all(np.all(a[~mask]==0) for a in step)
  if n=='phase':continue
  base=tt_pair(label+'_baseline_'+n,previous[n],shape,keep);assert all(np.all(a[~mask]==0) for a in base)
  total[n]=tt_add(label+'_'+n,base,step,shape,keep);assert all(np.all(a[~mask]==0) for a in total[n])
 sections=candidate_configuration_york_direction_jets({n:total[n] for n in ('chi','W','t')},basis,keep,label+'_TOTAL_configuration')
 native=tt_pair(label+'_TOTAL_native_time_values',P.dd_native_node_value(total['native'],basis,keep,jet=0),(33,15136,3),keep)
 metric=tt_pair(label+'_TOTAL_physical_metric_time_values',P.dd_metric_node_value(total['metric'],basis,keep,jet=0),(15136,6),keep)
 phase_jets=phase_response_scalar_jets(correction['phase'],basis,keep,label+'_NEW_phase_increment')
 for n in ('value','R','Z'):phase_jets[n]=tt_pair(label+'_phase_increment_'+n,phase_jets[n],(15136,),keep)
 phi=tt_pair(label+'_previous_TOTAL_phi',previous['phi'],(15136,4),keep);increment=tt_zero((15136,4))
 for w in (0,1):increment[w][:,0]=phase_jets['value'][w]
 changed=tt_add(label+'_phi',phi,increment,(15136,4),keep);assert all(np.array_equal(a[:,1:],b[:,1:]) for a,b in zip(changed,phi))
 reference_limit=all(np.all(a==0) for n in ('chi','W','t') for a in total[n]);records=[]
 packet=dict(nodes=total,sections=sections,native_time=native,metric_time=metric,phi=changed,phase_mixed_increment={n:phase_jets[n] for n in ('R','Z')},phase_mixed_are_increments=True,basis=basis,provenance=provenance,reference_configuration_exact_zero=reference_limit,physical_adoption=False)
 record=tt_stage('TOTAL_TRIAL_FIELDS',packet,stage_complete,records);packet['total_fields_record']=record
 return packet


def tt_captured_pair(captured,prefix,suffix,shape,keep,label):
 names=tuple(prefix+'_'+suffix+'_'+w for w in ('hi','lo'));assert all(n in captured for n in names),'Required FY128 completed capture missing'
 return tt_pair(label,tuple(captured[n].copy() for n in names),shape,keep)


def total_trial_fields_to_column(prepared,iq,fixed,keep,label,stage_complete):
 tt_require(prepared['provenance']);assert 0<=iq<4
 assert prepared['physical_adoption'] is False and fixed['provenance']==prepared['provenance']['columns'][iq] and fixed['provenance']['original_fixed_references_verified'] is True
 basis=prepared['basis'];q=prepared['sections'][iq];p=3784;sl=slice(iq*p,(iq+1)*p);records=[];YR=fixed['york_reference'];reference=dict(fixed['reference'])
 assert np.array_equal(fixed['material']['R'],basis['R'][iq]) and fixed['phase_constants']['synthetic_control'] is False
 gauge={n:tt_pair(label+'_fixed_gauge_'+n,x,shape,keep) for n,x,shape in ((n,fixed['gauge'][n],sh) for n,sh in (('N',(p,)),('beta',(p,3)),('N_jets',(p,4)),('beta_jets',(p,4,3))))}
 cov={n:tt_pair(label+'_fixed_covector_'+n,fixed['covectors'][n],shape,keep) for n,shape in (('u',(p,3)),('z',(32,p,3)),('u_jets',(p,4,3)),('z_jets',(32,p,4,3)))}
 time=tuple(a[:,sl].copy() for a in prepared['native_time'])
 for w in (0,1):cov['u_jets'][w][:,0]=time[w][0];cov['z_jets'][w][:,:,0]=time[w][1:]
 for n in ('u_jets','z_jets'):tt_pair(label+'_TOTAL_'+n,cov[n],cov[n][0].shape,keep)
 ht=tt_zero((p,3,3))
 for ordinal,(a,b) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for w in (0,1):ht[w][:,a,b]=ht[w][:,b,a]=prepared['metric_time'][w][sl,ordinal]
 mechanical={'h_dot':tt_pair(label+'_TOTAL_physical_h_dot',ht,(p,3,3),keep)};phi=tt_pair(label+'_TOTAL_paired_phi',tuple(a[sl].copy() for a in prepared['phi']),(p,4),keep)
 spatial_phi=tt_pair(label+'_fixed_spatial_phase',fixed['phase_spatial'],(p,3),keep)
 assert all(np.array_equal(a[:,1:],b) for a,b in zip(phi,spatial_phi)), 'Original instantaneous spatial phase covectors must remain unchanged'
 yd={n:tt_zero(q[n][0].shape) for n in ('rho','rho_gradient','W_jet','t')};fy_label=label+'_NEW_FY';captured={}
 def fy_capture(n,a):
  captured[n]=np.asarray(a).copy();keep(n,a)
 geometry=finite_york_geometry_target(YR,q['rho'],q['rho_gradient'],q['W_jet'],q['t'],yd,fy_capture,fy_label)
 lam=tt_captured_pair(captured,fy_label,'conformal_weight',(p,),keep,label+'_completed_FY_lambda');I0=tt_captured_pair(captured,fy_label,'physical_reference_inverse_quotient',(p,3,3),keep,label+'_completed_FY_reference_inverse')
 target=tt_pair(label+'_authoritative_York_target',YR['Pi_owned'] if prepared['reference_configuration_exact_zero'] else geometry['target'],(p,3,3),keep)
 tt_pair(label+'_FY_target_minus_authoritative_target',P.a_sub(geometry['target'],target),(p,3,3),keep)
 york=dict(h=geometry['h'],ih=geometry['ih'],mu=geometry['mu'],h_spatial_jets=geometry['h_spatial_jets'],target=target,FY_target=geometry['target'],tau=geometry['tau'])
 for n,suffix,shape in (('T','candidate_T',(p,3,3)),('kappa','candidate_inverse_trace',(p,)),('trace_part','candidate_trace_part_quotient',(p,)),('inverse_lam','inverse_weight_quotient',(p,))):york[n]=tt_captured_pair(captured,fy_label,suffix,shape,keep,label+'_completed_FY_'+n)
 tt_stage('TRIAL_YORK_GEOMETRY',dict(geometry=geometry,york=york,conformal_lambda=lam,physical_reference_inverse=I0,provenance=fixed['provenance']),stage_complete,records)
 reference.update(physical_spatial_inverse=I0,h_spatial_jets=YR['h_spatial_jets']);zero={n:tt_zero(shape) for n,shape in (('rho',(p,)),('rho_gradient',(p,2)),('h_dot',(p,3,3)),('u_jets',(p,4,3)),('z_jets',(32,p,4,3)))}
 model=finite_york_spacetime_first_jets(geometry,{'lambda':lam,'rho_gradient':q['rho_gradient']},gauge,cov,mechanical,zero,reference,keep,label+'_NEW_model')
 tt_stage('TRIAL_SPACETIME_MODEL',dict(model=model,gauge=gauge,covectors=cov,mechanical=mechanical,provenance=fixed['provenance']),stage_complete,records)
 candidate=finite_candidate_raw_action_adapter(geometry,model,gauge,cov,mechanical,dict(phi=phi),fixed['material'],reference,P.paired_current_affine_features,P.paired_current_affine_momenta,keep,label+'_NEW_raw')
 candidate['candidate_provenance']=dict(previous=fixed['provenance'],total_fields=prepared['total_fields_record'],new_geometry_and_total_rates=True,physical_adoption=False)
 tt_pair(label+'_paired_phi_minus_raw225_phi',P.a_sub(phi,P.a_dd(candidate['s']['phi'])),(p,4),keep);tt_pair(label+'_raw_h_target_trace_minus_tau',P.a_sub(fy_contract(P.a_dd(candidate['c']['h']),target),geometry['tau']),(p,),keep)
 tt_stage('TRIAL_RAW_CANDIDATE',dict(candidate=candidate,paired_phi=phi,model=model,provenance=candidate['candidate_provenance']),stage_complete,records)
 direction={n:tt_zero(shape) for n,shape in (('h',(p,3,3)),('h_spatial_jets',(p,2,3,3)),('h_dot',(p,3,3)),('u_jets',(p,4,3)),('z_jets',(32,p,4,3)),('phi',(p,4)))}
 contact=finite_candidate_configuration_contact(candidate,geometry,gauge,cov,mechanical,direction,reference,keep,label+'_NEW_zero_direction_state')
 tt_stage('TRIAL_PRIMAL_CONTACT_STATE',dict(contact=contact,candidate_provenance=candidate['candidate_provenance'],zero_direction_only=True),stage_complete,records)
 s={n:P.a_dd(candidate['s'][n]) for n in ('g','hi','U','uc','P')};s['phi']=phi;c={n:P.a_dd(candidate['c']['sqrt_h' if n=='mu' else n]) for n in ('N','beta','h','ih','u','mu')}
 D={n:tt_zero(a[0].shape) for n,a in {**s,**c}.items()};eos_c={n:c[n] for n in ('N','mu','ih','u')};eos_label=label+'_NEW_phase';phase_fields={}
 def phase_capture(n,a):
  if n.startswith(eos_label+'_'):phase_fields[n]=np.asarray(a).copy()
  keep(n,a)
 eos=candidate_invariant_phase_eos_current(s,eos_c,D,fixed['phase_constants'],phase_capture,eos_label)
 tt_stage('TRIAL_LITERAL_PHASE',dict(eos=eos,s=s,c=c,completed_stage_fields=phase_fields,paired_phase_retained=True,provenance=candidate['candidate_provenance']),stage_complete,records)
 curvature=finite_candidate_intrinsic_curvature(candidate,contact,keep,label+'_NEW_curvature')
 tt_stage('TRIAL_INTRINSIC_CURVATURE',dict(curvature=curvature,candidate_provenance=candidate['candidate_provenance']),stage_complete,records)
 return dict(candidate=candidate,geometry=geometry,model=model,york=york,york_reference=YR,conformal={'lambda':lam,'rho_gradient':q['rho_gradient']},gauge=gauge,covectors=cov,mechanical=mechanical,reference=reference,contact=contact,curvature=curvature,phase=dict(s=s,c=eos_c,values=eos['value'],eos=eos,completed_stage_fields=phase_fields,prefix=eos_label),normal_s=s,normal_c=c,completed_stages=records,all_six_physical_time_entries_retained=True,normal_rows_or_weak_currents_evaluated=False,strict_EOS_domain_inherited_from_NEW116_only=True,phase_H_positive_not_inferred=True,physical_adoption=False)


def total_trial_fields_to_sheet(prepared,source,keep,label,stage_complete):
 tt_require(prepared['provenance']);assert prepared['physical_adoption'] is False
 assert source['provenance']==prepared['provenance']['sheet_source'] and source['fixed_labels_and_positions_verified'] is True
 for n in ('g','R','Z','indices','right_weight'):keep(label+'_original_sheet_'+n,np.asarray(source[n]).copy())
 result=fixed_label_finite_sheet_geometry(source['g'],source['R'],source['Z'],prepared['basis']['r'],source['indices'],source['right_weight'],prepared['nodes']['chi'],tt_zero((87,45)),keep,label+'_NEW_sheet')
 records=[];record=tt_stage('TRIAL_SAME_POSITION_SHEET_GEOMETRY',dict(sheet=result,original_source=source['provenance'],total_fields=prepared['total_fields_record'],labels_unchanged=True,physical_adoption=False),stage_complete,records)
 return dict(sheet=result,original_source=source['provenance'],record=record,ordinary_source_not_evaluated=True,physical_adoption=False)
