"""HELD definitions: direct supplied-event conditional43 local readout/report.
Globals np, math, H (reviewed114 adapter), REPORT (reviewed132 formatter).
The containing root caller authenticates files/proofs and owns publication.
No sampler, field solve, EOS/source/exterior choice or galaxy invocation occurs.
Paired native313 input requires an earned binary64 collapse/conditioning record;
the stored rounding defect is descriptive and never earns that admission.
"""
CONDITIONAL43_AUTHOR_DRAFT=True
CONDITIONAL43_DEPENDENCY_PINS={
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'author_fragment_revised_43_observer_report_v002.py':'0cab1853d083239175943a4765101a95104949bb14f13ca1eb9902713df92843',
 'author_fragment_full_dynamic_metric_circle_v002.py':'3be37b2181ff154067ccd0d01587266ce64a58a118bd6dbd331fca1f49001c6b',
 'cross_u_full_metric_geodesic_and_rotating_material_v001.py':'53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa'}


def circle43_supplied_native_metric(metric,precision,retained):
 assert isinstance(metric,dict) and isinstance(precision,dict)
 assert isinstance(retained,dict)
 assert precision.get('binary64_readout_admitted') is True and precision.get('provenance')
 assert metric['coordinates']=='native313_t_R_Z_phi' and metric['derivative_index_first'] is True
 retained.update(format=metric['format'],coordinates=metric['coordinates'],derivative_index_first=True)
 if metric['format']=='binary64':
  g=np.asarray(metric['g']);dg=np.asarray(metric['dg'])
  retained.update(supplied_g=g.copy(),supplied_dg=dg.copy(),paired_words_supplied=False)
 elif metric['format']=='paired':
  assert precision.get('paired_word_collapse_admitted') is True,'Actual paired readout precision proof required'
  pairs={}
  for n,shape in (('g',(4,4)),('dg',(4,4,4))):
   hi=np.asarray(metric[n+'_hi']);lo=np.asarray(metric[n+'_lo'])
   retained.update({n+'_hi':hi.copy(),n+'_lo':lo.copy()})
   assert hi.shape==lo.shape==shape and hi.dtype==lo.dtype==np.dtype('float64')
   assert np.all(np.isfinite(hi)) and np.all(np.isfinite(lo))
   s=hi+lo;retained[n+'_binary64']=s.copy();v=s-hi;defect=(hi-(s-v))+(lo-v)
   retained[n+'_two_sum_rounding_defect']=defect.copy()
   assert np.all(np.isfinite(s)) and np.all(np.isfinite(defect))
   pairs[n]=s
  g,dg=pairs['g'],pairs['dg'];retained['paired_words_supplied']=True
 else:raise AssertionError('Supplied metric format must be binary64 or paired')
 assert g.shape==(4,4) and dg.shape==(4,4,4) and g.dtype==dg.dtype==np.dtype('float64')
 assert np.all(np.isfinite(g)) and np.all(np.isfinite(dg))
 retained.update(readout_precision_admission=dict(precision),rounding_defect_performed_admission=False)
 return g,dg,retained


def conditional_43_local_circle_report(baseline_document,events,*,baseline_row_path,
 baseline_fields,r_model,orientation,finite_closure,domain_admission,provenance,
 requested_motion_scope,prediction_kind='local_metric_circular_snapshot',circle_gate=None):
 """Each event owns R_kpc/Vobs_kms/measured_sigma_kms and supplied metric/precision.
 Required sampling: coordinate_event(t313,R,Z,phi), radial_side, radius_mapping,
 sheet_side/junction convention and sampling_provenance. No tensor interpolation.
 circle_gate(readout,registration_without_Vobs) may earn instantaneous-circle
 compatibility under caller-declared criteria; no threshold is invented here.
 Diagnostic scope displays a unique oriented radial candidate with all defects.
 """
 assert prediction_kind in ('local_metric_circular_snapshot','evolved_tracer','reduced_pipeline')
 assert requested_motion_scope in ('radial_balance_diagnostic','compatible_instantaneous_circle')
 assert type(orientation) is int and orientation in (-1,1)
 assert circle_gate is None or callable(circle_gate)
 assert all(isinstance(x,dict) and x for x in (finite_closure,domain_admission,provenance))
 assert finite_closure.get('finite_physical_metric_admitted') is False
 boundary=finite_closure.get('declared_conditional_boundary');assert isinstance(boundary,dict) and boundary
 assert set(baseline_fields)=={'radius','observed','sigma','model'}
 old=REPORT.report43_path(baseline_document,baseline_row_path)
 assert isinstance(old,list) and isinstance(events,list) and len(old)==len(events)==43
 # Catalogue fields are authenticated/tied here and never enter root/orientation selection.
 for saved,event in zip(old,events):
  for key,field in (('R_kpc','radius'),('Vobs_kms','observed'),('measured_sigma_kms','sigma')):
   assert REPORT.report43_number(event[key])==REPORT.report43_number(REPORT.report43_path(saved,baseline_fields[field]))
 admitted=finite_closure.get('finite_constraint_solution_admitted') is True and bool(finite_closure.get('provenance'))
 domains=domain_admission.get('finite_domains_admitted') is True and bool(domain_admission.get('provenance'))
 supported=prediction_kind=='local_metric_circular_snapshot'
 records=[];revised=[]
 for index,event in enumerate(events):
  flags=dict(event.get('interval_flags',{}));assert all(isinstance(k,str) and k and type(v) is bool for k,v in flags.items())
  flags.update(finite_constraint_solution_admitted=admitted,finite_domains_admitted=domains,
               supplied_metric_available=event.get('metric') is not None,unique_oriented_radial_root=False,
               readout_precision_admitted=False,full_instantaneous_circle_admitted=False)
  record=dict(index=index,R_kpc=event['R_kpc'],supplied_event=event,declared_orientation=orientation,
              radial_candidate_velocity_kms=None,admitted_report_velocity_kms=None);records.append(record)
  note='';velocity=None
  try:
   assert admitted and domains,'Finite constraint/current/canonical/normal/CMC/domain closure is not admitted'
   assert supported,'Requested prediction kind needs a different dynamics/observational pipeline'
   assert event.get('metric') is not None,'Metric/first jets are missing at this event'
   registration=dict(event['sampling']);record['sampling_registration']=registration
   coordinates=np.asarray(registration['coordinate_event']);assert coordinates.shape==(4,) and np.all(np.isfinite(coordinates))
   assert registration['sampling_provenance'] and registration['sheet_side'] in ('upper','lower','registered_junction')
   assert isinstance(registration['sheet_junction_convention'],dict) and registration['sheet_junction_convention']
   contact=H.q1_radial_readout_contact(r_model,float(coordinates[1]),catalogue_R_kpc=event['R_kpc'],mapping=registration['radius_mapping'],side=registration['radial_side']);record['radius_contact']=contact
   precision=event['readout_precision_admission']
   words={};record['metric_readout_words']=words
   g,dg,words=circle43_supplied_native_metric(event['metric'],precision,words);flags['readout_precision_admitted']=True
   result=H.supplied_model_local_circle_event(g,dg,radius_contact=contact,orientation=orientation,input_scope='conditional_finite_metric',metric_admission=finite_closure,readout_precision_admission=precision);record['local_readout']=result
   selection=result['readout'];selected=selection['selected_index'];flags['unique_oriented_radial_root']=selected is not None
   if selected is not None:record['radial_candidate_velocity_kms']=selection['candidates'][selected]['declared_orientation_speed_kms']
   gate=None
   if circle_gate is not None:
    gate=circle_gate(result,dict(registration,declared_orientation=orientation));record['circle_gate']=gate
    assert isinstance(gate,dict) and type(gate['admitted']) is bool and gate.get('provenance')
    flags['full_instantaneous_circle_admitted']=gate['admitted']
   if selected is None:note=selection['orientation_status']
   elif requested_motion_scope=='compatible_instantaneous_circle' and not flags['full_instantaneous_circle_admitted']:note='Full instantaneous-circle compatibility is unadmitted; radial candidate retained separately.'
   else:
    velocity=record['radial_candidate_velocity_kms']
    note='Conditional local radial-balance diagnostic; full circle/geodesic defects retained.' if requested_motion_scope=='radial_balance_diagnostic' else 'Conditional compatible instantaneous circle; supplied gate retained.'
  except (AssertionError,KeyError,ValueError,TypeError,ArithmeticError) as error:
   note='READOUT_REFUSED: '+type(error).__name__+': '+str(error);record['refusal']=note
  record.update(admitted_report_velocity_kms=velocity,interval_flags=dict(flags),note=note)
  revised.append(dict(R_kpc=event['R_kpc'],velocity_kms=velocity,interval_flags=flags,note=note))
 status=dict(finite_closure=finite_closure,domain_admission=domain_admission,physical_metric_admitted=False,
             report_scope=requested_motion_scope,all43_readout_rows_available=all(x['velocity_kms'] is not None for x in revised))
 scope=dict(input_scope='conditional_finite_metric',motion_scope=requested_motion_scope,
            declared_conditional_boundary=boundary,rotation_orientation=orientation,
            orientation_selected_using_Vobs=False,normal_observer_local_speed=True,
            persistent_orbit_or_stability_admitted=False,synthetic_line_or_reduced_pipeline_admitted=False)
 formatted=REPORT.revised_43_observer_report(baseline_document,revised,baseline_row_path=baseline_row_path,baseline_fields=baseline_fields,provenance=provenance,admission_status=status,prediction_kind=prediction_kind,prediction_scope=scope)
 return dict(report=formatted,events=records,dependency_pins=dict(CONDITIONAL43_DEPENDENCY_PINS),
             containing_caller_must_authenticate_dependencies=True,metric_sampled_by_reader=False,
             finite_constraint_admission_performed=False,physical_or_observational_adoption=False)
