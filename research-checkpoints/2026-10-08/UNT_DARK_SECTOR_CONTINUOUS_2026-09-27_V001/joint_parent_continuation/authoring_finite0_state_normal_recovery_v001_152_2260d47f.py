"""HELD definitions-only finite0 completed-STATE normal-test recovery skeleton.
No completed225/160/curvature/116/49 transaction is replayed for column0.
Only its16 uncommitted normal tests and later unearned columns/assembly proceed.
The repair proof pin remainsNone until root earns it. Root alone may release.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
STEM='CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V001'
DRIVER_PROTOCOL='CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V001.md'
PROTOCOL_SHA=None
PARENT_FILE='cross_u_finite0_candidate_action_residual_v007.py'
PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PARENT_PROTOCOL='CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V001.md'
PARENT_PROTOCOL_SHA='253f43b95c8029d0f54b7e38082771bad2e6080f7288e076bcdea36c73e0235b'
RESTORE_FILE='author_fragment_finite0_completed_state_restore_v001.py'
RESTORE_SHA='6510c60a03c0b63eb16ec2b7fa5ca7bff0ad484f8865d99a1abd7241511cfc3d'
REPAIR_FILE='author_fragment_exact_exponent_two_product_v002.py'
REPAIR_SHA='23750efc4326f0b9154da9a052001dbc44119dab7c7bd286ed86f1522a9707a9'
REPAIR_CONTROL_PROOF=(None,None,None)
FAILED_ERROR='CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V007_ERROR.json'
FAILED_RECEIPT='CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V007_RECEIPT.json'
FAILED_TERMINAL=dict(pid=94049,source_sha256=PARENT_SHA,error_sha256='4edf894c38ee0fd2ff54996ba45dd444f7ca3ccdedfc81c8dd3cd67ccf8a7bcd',receipt_sha256='3e333a3023836a16c3d90701bcc49134fd022c9a990b2ce2bdf4a8551c852543',result_sha256=None,status='CLOSED_ERROR')
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};PINS={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def load_original_definitions():
 assert hashlib.sha256((BASE/PARENT_FILE).read_bytes()).hexdigest()==PARENT_SHA
 tree=ast.parse((BASE/PARENT_FILE).read_text())
 selected=('PINS','ADMISSION_FILE','ADMISSION_SHA','CONTROL_PROOF','MIXED_CONTROL_PROOF','SHEET_CONTROL_PROOF')
 for a in tree.body:
  if isinstance(a,ast.Assign) and len(a.targets)==1 and isinstance(a.targets[0],ast.Name) and a.targets[0].id in selected:globals()[a.targets[0].id]=ast.literal_eval(a.value)
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name not in ('packet','main')]
 assert {n.name for n in defs}=={'bind','keep','pair_from','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','initialize_arithmetic','compact_direction','finite0_inputs','mean_labels','candidate_column','sheet_rows','canonical_functional_contact'}
 exec(compile(ast.Module(body=defs,type_ignores=[]),PARENT_FILE,'exec'),globals())

def load_recovery_helpers():
 for file,checksum in ((RESTORE_FILE,RESTORE_SHA),(REPAIR_FILE,REPAIR_SHA)):
  bind(file,checksum);tree=ast.parse((BASE/file).read_text());body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.Assign))]
  exec(compile(ast.Module(body=body,type_ignores=[]),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_exact_exponent_product');globals()['a_prod']=P.a_prod


def recovery_admission():
 bind(PARENT_FILE,PARENT_SHA);bind(PARENT_PROTOCOL,PARENT_PROTOCOL_SHA);bind(FAILED_ERROR,FAILED_TERMINAL['error_sha256']);bind(FAILED_RECEIPT,FAILED_TERMINAL['receipt_sha256'])
 e=json.loads(P.path(FAILED_ERROR).read_text());rc=json.loads(P.path(FAILED_RECEIPT).read_text())
 assert rc['status']=='CLOSED_ERROR' and rc['error_sha256']==FAILED_TERMINAL['error_sha256'] and e['status']=='FAILED'
 assert e['owner']==rc['owner'] and e['owner']['pid']==94049 and e['owner']['source_sha256']==PARENT_SHA
 assert e['controls']==[] and len(e['checkpoints'])==4 and e['raw_preservation_traceback'] is None and e['closing_traceback'] is None
 assert e['context']['stage']=='NEW_candidate_normal_test' and (e['context']['column'],e['context']['row'],e['context']['jet'])==(0,0,0) and e['context']['completed_test_refs']==[]
 records=e['checkpoints'];kinds=['owned_current_mechanical_time_words_reference_finite_candidate','unchanged_registered_E_F_normal_scalar_basis','NEW_candidate_completed_configuration_features_momenta_EOS_and_mean','available_new_finite_candidate_operands']
 assert [r['metadata']['kind'] for r in records]==kinds and [len(r['metadata']['schema']) for r in records]==[4,7,40917,942]
 for record in records:
  bind(record['file'],record['sha256']);bind(record['commit_file'],record['commit_sha256']);cm=json.loads(P.path(record['commit_file']).read_text());assert cm=={n:record[n] for n in ('file','sha256','metadata')}
  assert rc['output_sha256'][record['file']]==record['sha256'] and rc['output_sha256'][record['commit_file']]==record['commit_sha256']
 assert thin(records[2])==e['context']['state'] and records[2]['metadata']['column']==0
 assert all(x is False for x in e['qualification'].values()) and e['qualification']==rc['qualification']==FLAGS
 return records,e


def recovery_packet(parent_records):
 input_ref,basis_ref,state_ref,_=parent_records;meta=input_ref['metadata'];refs=meta['refs']
 # Registry constant setup is unchanged; no candidate EOS/current is evaluated.
 constants=candidate_phase_registered_constants(meta['fixed']);rate=read(input_ref,tuple(input_ref['metadata']['schema']));basis=read(basis_ref,tuple(basis_ref['metadata']['schema']))
 state_data=read(state_ref,finite0_completed_state_names(state_ref['metadata']['schema']));bundle=finite0_restore_completed_state(state_data,meta,state_ref['metadata'],constants)
 del state_data
 RECORDS.extend(parent_records[:3]);columns=[];records=[];moments=[]
 q,record,m=recovery_completed_column0(refs,bundle,state_ref);columns.append(q);records.append(record);moments.append(m);del bundle
 mean=read(refs['mean_input'],('fine_reference_directions','fine_reference_weights'));assert np.all(mean['fine_reference_weights']>0)
 Hbar=meta['owned_background']['h']*meta['fixed']['Hunit']/299792458.;assert math.isfinite(Hbar) and Hbar>0
 for iq in range(1,4):
  q,record,m=candidate_column(refs,iq,basis,rate,mean['fine_reference_directions'],mean['fine_reference_weights'],Hbar,constants);columns.append(q);records.append(record);moments.append(m)
 return finish_recovery_packet(refs,basis,columns,records,moments)

def recovery_completed_column0(refs,bundle,state_ref):
 clear_current();iq=bundle['column'];assert iq==0 and bundle['completed_action_replayed'] is False
 CONTEXT.update(stage='NEW_normal_tests_on_restored_STATE0',column=iq,state=thin(state_ref),failed_parent=FAILED_TERMINAL)
 candidate,contact,curvature,eos,ordinary=(bundle[n] for n in ('candidate','contact','curvature','eos','ordinary'))
 s,c,D,inputs,Hbar=(bundle[n] for n in ('s','c','D','inputs','Hbar'))
 coeff={family:P.a_dd(np.zeros((3784,4,4))) for family in ('value','delta')};theta={};point_outputs={};test_refs=[]
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   clear_current();CONTEXT.update(stage='NEW_candidate_normal_test',column=iq,row=row,jet=jet,state=thin(state_ref),completed_test_refs=list(test_refs))
   f=np.zeros(3784);df=np.zeros((3784,4));b=np.zeros((3784,3));db=np.zeros((3784,4,3))
   if row==0:
    if coordinate is None:f[:]=1.
    else:df[:,coordinate]=1.
   elif coordinate is None:b[:,row-1]=1.
   else:db[:,coordinate,row-1]=1.
   label='row%d_jet%d'%(row,jet);native=finite_candidate_native_EH_normal(candidate,contact,curvature,f,df,b,db,Hbar,inputs[7],keep,label+'_native_EH');capture_families('completed_'+label+'_native_EH_',native)
   phase=candidate_phase_normal_stress(s,c,D,eos,f,b,keep,label+'_phase') if coordinate is None else dict(value={n:P.a_dd(np.zeros(3784)) for n in ('action','absolute','relative')},delta={n:P.a_dd(np.zeros(3784)) for n in ('action','absolute','relative')},relative_phase_included_once=True)
   # Phase and ordinary action have no test-firstjet coefficient; their value
   # calls are skipped for jet directions by the exact declared local action.
   own=ordinary if coordinate is None else dict(value=dict(normal_density=P.a_dd(np.zeros((3784,4)))),delta=dict(normal_density=P.a_dd(np.zeros((3784,4)))))
   total=finite_candidate_total_normal(native,phase,own,f,b,keep,label+'_total');capture_families('completed_'+label+'_total_',total)
   for family in ('value','delta'):
    for word in (0,1):coeff[family][word][:,row,jet]=total[family]['hamiltonian'][word]
    theta[family]=native[family]['initial_CMC_density'];put_pair(point_outputs,family+'_current_Hamiltonian_coefficients',coeff[family])
   test_ref=P.checkpoint('NORMAL_TEST',arrays(AVAILABLE),dict(kind='NEW_completed_normal_test_and_primary_comparison_contacts',column=iq,row=row,jet=jet,normal_coordinate_order=['value','R','Z','t'],candidate_state=thin(state_ref),restored_failed_parent=FAILED_TERMINAL,relative_phase_count=1,ordinary_mean_count=1,physical_ports_admitted=False,physical_adoption=False));test_refs.append(thin(test_ref))
 clear_current();CONTEXT.update(stage='NEW_candidate_column_publication',column=iq,state=thin(state_ref),completed_test_refs=list(test_refs))
 for family in ('value','delta'):put_pair(point_outputs,family+'_normal_coefficients',coeff[family]);put_pair(point_outputs,family+'_initial_CMC_density',theta[family]);put_pair(point_outputs,family+'_phase_density',eos[family]['p'])
 for n,x in candidate['momenta'].items():put_pair(point_outputs,'NEW_current_momentum_'+n,x)
 for n,x in contact['delta_momenta'].items():put_pair(point_outputs,'NEW_delta_momentum_'+n,x)
 data=arrays({**AVAILABLE,**point_outputs});record=P.checkpoint('COLUMN',data,dict(kind='NEW_finite0_candidate_coefficients_current_and_normal_rows',column=iq,candidate_state=thin(state_ref),restored_failed_parent=FAILED_TERMINAL,normal_test_refs=test_refs,pilot_reference=thin(refs['pilots'][iq]),owned_spatial_reference=thin(refs['forces'][iq]),current_time_words=thin(refs['current_jets']),geometry_reference_rho=0.,direction='true_conformal_scalar_hat43_22_at_reference_mechanical_rates_fixed',phase_charge_direction_restored=False,normal_coordinate_order=['value','R','Z','t'],all_primary_comparison_gaps_retained=True,relative_phase_count=1,ordinary_mean_count=1,old_coefficients_features_momenta_or_normals_reused=False,original_target_or_epsilon_refitted=False,physical_adoption=False));clear_current()
 compact=dict(value=dict(normal_coefficients=coeff['value'],initial_CMC_density=theta['value']),delta=dict(normal_coefficients=coeff['delta'],initial_CMC_density=theta['delta']),normal_coordinate_order=('value','R','Z','t'),relative_phase_count=1,ordinary_label_count=1)
 return compact,record,dict(value=dict(native=candidate['momenta']['native_density'],metric=candidate['momenta']['metric_total_density'],phase=eos['value']['p']),delta=dict(native=contact['delta_momenta']['native_density'],metric=contact['delta_momenta']['metric_total_density'],phase=eos['delta']['p']))

def finish_recovery_packet(refs,basis,columns,records,moments):
 sheet_test=np.zeros((4,87,45));sheet_test[:,43,0]=(1.,2.,0.,4.);sheet,sheet_ref=sheet_rows(refs,basis,sheet_test);clear_current();CONTEXT.update(stage='NEW_global_current_normal_CMC_residual');global_rows=finite_candidate_global_normal_CMC(columns,basis,nt,st,keep,P.check,'candidate_global');prior=read(refs['prior_readout'],('native_original_target','metric_original_target')+tuple(family+'_'+n+'_'+word for family in ('native','metric') for n in ('frozen_rhs_defect','primitive_minus_earned_bridge','actual_target_residual') for word in ('hi','lo')));phase_prior=read(refs['phase_loads'],tuple(n+'_'+word for n in ('fixed_literal_weak_phase_charge','registered_weak_phase_charge','owned_registered_weak_phase_charge','literal_minus_registered_weak_gap','registered_minus_owned_weak_gap') for word in ('hi','lo')));data={};norms={}
 for family in ('value','delta'):
  native=P.a_stack([m[family]['native'] for m in moments],0);native=(native[0].reshape(15136,33,3).transpose(1,0,2),native[1].reshape(15136,33,3).transpose(1,0,2));metric=(np.concatenate([m[family]['metric'][0] for m in moments]),np.concatenate([m[family]['metric'][1] for m in moments]));phase=(np.concatenate([m[family]['phase'][0] for m in moments]),np.concatenate([m[family]['phase'][1] for m in moments]))
  nweak=P.dd_native_scatter(native,basis,keep);mweak=P.dd_metric_scatter(metric,basis,keep);pweak=P.dd_scalar_scatter(phase,basis,keep,'candidate_'+family+'_phase_charge');normal=P.a_add(global_rows[family]['weak_normal'],sheet[family]);trace=global_rows[family]['weak_initial_CMC']
  for n,x in (('native_current',nweak),('metric_current',mweak),('literal_phase_current',pweak),('total_weak_normal',normal),('initial_weak_CMC',trace)):put_pair(data,family+'_'+n,x)
  for kind,point,weak,test in (('native',native,nweak,native_test),('metric',metric,mweak,metric_test),('phase',phase,pweak,st)):canonical_functional_contact(kind,point,weak,test,basis,'candidate_'+family+'_'+kind+'_current_polynomial_transpose')
  if family=='value':
   target_norms={}
   for n,x,target in (('native',nweak,P.a_dd(prior['native_original_target'])),('metric',mweak,P.a_dd(prior['metric_original_target'])),('phase',pweak,pair_from(phase_prior,'fixed_literal_weak_phase_charge'))):
    residual=put_pair(data,'actual_'+n+'_canonical_target_residual',P.a_sub(x,target));target_norms[n]=float(np.linalg.norm(residual[0]+residual[1]))
   norms['actual_canonical_target_residuals_L2']=target_norms
  norms[family]=dict(normal_L2=[float(np.linalg.norm((normal[0]+normal[1])[row])) for row in range(4)],initial_CMC_L2=float(np.linalg.norm(trace[0]+trace[1])),native_current_L2=float(np.linalg.norm(nweak[0]+nweak[1])),metric_current_L2=float(np.linalg.norm(mweak[0]+mweak[1])),literal_phase_current_L2=float(np.linalg.norm(pweak[0]+pweak[1])))
 capture_families('prior_signed_bridge_',prior);capture_families('prior_phase_current_',phase_prior);data.update(arrays(AVAILABLE));data.update(arrays({n:x for n,x in RAW.items() if n.startswith('control_')}));loads=P.checkpoint('LOADS',arrays(data),dict(kind='NEW_candidate_current_and_full_normal_initial_CMC_measurement',columns=[thin(q) for q in records],sheet=thin(sheet_ref),norms=norms,completed_controls=CHECKS[2:],original_native_metric_and_literal_weak_phase_targets_unchanged=True,inherited_frozen_primitive_epsilon_and_phase_registration_gaps_retained=True,compact_direction_is_unqualified_charge_and_canonical_partial=True,relative_phase_count=1,ordinary_sheet_and_reference_mean_counted_once=True,no_offset_gain_or_source_refit=True,physical_ports=None,physical_adoption=False))
 assert len(RECORDS)==76 and len(CHECKS)==12 and all(x['passed'] for x in CHECKS)
 return dict(status='FINITE0_NEW_ACTION_CURRENT_NORMAL_CMC_RESIDUAL_MEASURED',columns=records,sheet=sheet_ref,loads=loads,norms=norms,finite_configuration_rho=0.,direction_node=[43,22],original_native_metric_and_phase_targets_retained=True,primitive_bridge_resolved=False,physical_normal_CMC_or_charge_solved=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and all(x is not None for x in (PROTOCOL_SHA,RESTORE_SHA,*REPAIR_CONTROL_PROOF)),'Completed repair controls and root full release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_original_definitions();initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);parent_records,parent_error=recovery_admission()
  for n,h in tuple(PINS.items())+((ADMISSION_FILE,ADMISSION_SHA),(DRIVER_PROTOCOL,PROTOCOL_SHA)):bind(n,h)
  for name,h,status in (CONTROL_PROOF,MIXED_CONTROL_PROOF,SHEET_CONTROL_PROOF,REPAIR_CONTROL_PROOF):
   bind(name,h);assert json.loads(P.path(name).read_text())['status']==status,name
  bind(RESTORE_FILE,RESTORE_SHA);bind(REPAIR_FILE,REPAIR_SHA)
  INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256'];P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,failed_parent=FAILED_TERMINAL,inherited_success_records=[thin(r) for r in parent_records[:3]],preserved_failed_raw=thin(parent_records[3]),resumed_from_column=0,resumed_from_normal_test=[0,0],old_completed_action_replay=False,qualification=FLAGS))
  initialize_arithmetic();load_recovery_helpers()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=recovery_packet(parent_records)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,failed_parent=FAILED_TERMINAL,inherited_success_records=[thin(r) for r in parent_records[:3]],preserved_failed_raw=thin(parent_records[3]),qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   available={**AVAILABLE,**RAW,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if available:
    try:P.checkpoint('ERROR_RAW',arrays(available),dict(context=dict(CONTEXT),kind='available_unfinished_recovered_finite_candidate_operands'),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',failed_parent=FAILED_TERMINAL,traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
