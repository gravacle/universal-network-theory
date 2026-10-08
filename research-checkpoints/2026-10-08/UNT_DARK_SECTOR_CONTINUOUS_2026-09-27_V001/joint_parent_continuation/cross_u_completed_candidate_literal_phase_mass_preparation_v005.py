"""HELD full completed-candidate phase mass handoff; definitions only.
Natural CLOSED97585 and authentic prior-phase ancestry seals are mandatory.
Copy four completed phase transactions/current weak words; prepare NEW H diagonal only.
No225/116/current/normal/curvature/matter/fixture/operator/solve replay.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARATION_V005'
PROTOCOL='CROSS_U_COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARATION_V004.md'
PROTOCOL_SHA='b6930f9dca96687c7fb230e88087dba983dae9147df0aa30bb053107d72d2d1b'
RECOVERY_FILE='cross_u_finite0_state_normal_recovery_v005.py'
RECOVERY_SHA='8f9b528e1da5114b148585799e902cdaaa14a6ac2af60e7deff9a85375792be2'
RECOVERY_RESULT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RESULT.json', 'ea3c323511febbd278217e19ce8364d0e09186edc6d1d5c61bf87fb5fa211954', 'FINITE0_NEW_ACTION_CURRENT_NORMAL_CMC_RESIDUAL_MEASURED')
RECOVERY_RECEIPT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RECEIPT.json', '9e26a9c77d2ec7f023344c8399645cb94dc3252f2ab0dd744e14469050a30955', 'CLOSED')
RECOVERY_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_V001.json', '47ea566a93b34846c5861f7b184f80a73ac1ddd74f52bc891a7160b0a57fdab1', 'ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED')
RECOVERY_SUCCESS_PROOF_STATUS='ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED'
PRIOR_PHASE_PRODUCER_SOURCE=('cross_u_phase_fixed_weak_charge_preparation_v003.py','ed18caa749cbbfef40956ee4764390d688aaf6a1567912317d6cc81c9851d079')
PRIOR_PHASE_PRODUCER_RESULT=('CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003_RESULT.json','fefe9a83c871577653a3965d0c61ff869f6786ff0b1c9a943d9abf4fd6ee79d7','LITERAL_PHASE_HESSIAN_POSITIVE_AND_FIXED_WEAK_CHARGE_MASS_PREPARED')
PRIOR_PHASE_PRODUCER_RECEIPT=('CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003_RECEIPT.json','9d2fb6e0a649976167144b0d428bc730800844d78670587ad8891b11ddfcca90','CLOSED')
PRIOR_PHASE_ANCESTRY_PROOF=('ROOT_CLOSED_PRIOR_PHASE_LOADS_ANCESTRY_SEALS_V001.json','cf5575e71d2c818d84da7fbb5e676bf60e9051ebed2917aab8e9a192e3884ed3','ROOT_CLOSED_PRIOR_PHASE_LOADS_ANCESTRY_SEALS_VERIFIED')
COMPONENT_PROOF=('CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json','5f632a9927d41e36a40c7f2e0988997905ff99ac8dfef985307ce7723f63d4f9','CANDIDATE_LITERAL_PHASE_MASS_MANUFACTURED_COMPONENT_CONTROLS_PASS')
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_phase_literal_charge_hessian_v002.py':'293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143',
 'author_fragment_candidate_literal_phase_mass_v001.py':'0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38',
 'author_fragment_finite0_completed_state_restore_v002.py':'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235'}
np=P=K=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for file,checksum in PINS.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==checksum,file
 tree=ast.parse((BASE/IO_PARENT).read_text());names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==10
 exec(compile(ast.Module(body=defs,type_ignores=[]),IO_PARENT,'exec'),globals());initialize_io()

def initialize_phase_helpers():
 global np,K
 import numpy as numpy
 np=numpy;SCOPE['np']=np;files=list(PINS);names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_reshape','scalar_mask','scalar_lift','dd_scalar_scatter'}
 tree=ast.parse((BASE/files[0]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==15;SCOPE['capture']=keep;exec(compile(ast.Module(body=defs,type_ignores=[]),files[0],'exec'),SCOPE)
 for name in names:setattr(P,name,SCOPE[name])
 tree=ast.parse((BASE/files[2]).read_text());names={'phase_pair_keep','phase_scalar_value','phase_mass_diagonal'};scope=dict(np=np,P=P);defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==3;exec(compile(ast.Module(body=defs,type_ignores=[]),files[2],'exec'),scope);K=types.SimpleNamespace(**{n:scope[n] for n in names})
 for file,count in ((files[3],5),(files[4],8),(files[6],2)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==count
  for n in tree.body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('FINITE0_RESTORE_PARENT_SOURCE_SHA','FINITE0_RESTORE_RECOVERY_SOURCE_SHA'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 tree=ast.parse((BASE/files[5]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='candidate_phase_registered_constants'];assert len(defs)==1;exec(compile(ast.Module(body=defs,type_ignores=[]),files[5],'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_phase_mass_exact_exponent_product')

def bind_record(ref):
 bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);cm=json.loads(P.path(ref['commit_file']).read_text())
 assert cm['file']==ref['file'] and cm['sha256']==ref['sha256']
 if 'metadata' in ref:assert cm['metadata']==ref['metadata']
 return dict(file=ref['file'],sha256=ref['sha256'],commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'],metadata=cm['metadata'])

def completed_candidate_admission():
 bind(RECOVERY_FILE,RECOVERY_SHA);bind('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V003.md','0b65e9ebe92bc4a1ccd7aa5710dcc1d3e8f65597a03acdf4352a1fb4d2427f52')
 for name,h,status in (RECOVERY_RESULT,RECOVERY_RECEIPT,RECOVERY_CLOSURE_PROOF,COMPONENT_PROOF):bind(name,h);assert json.loads(P.path(name).read_text())['status']==status,name
 r=json.loads(P.path(RECOVERY_RESULT[0]).read_text());rc=json.loads(P.path(RECOVERY_RECEIPT[0]).read_text())
 assert r['owner']==rc['owner'] and r['owner']['pid']==97585 and r['owner']['source_sha256']==RECOVERY_SHA
 proof_json=json.loads(P.path(RECOVERY_CLOSURE_PROOF[0]).read_text());assert RECOVERY_CLOSURE_PROOF[2]==proof_json['status']==RECOVERY_SUCCESS_PROOF_STATUS
 assert proof_json['owner']==r['owner'] and proof_json['source_sha256']==RECOVERY_SHA and proof_json['result_sha256']==RECOVERY_RESULT[1] and proof_json['receipt_sha256']==RECOVERY_RECEIPT[1]
 assert type(proof_json['exit_code']) is int and proof_json['exit_code']==0 and proof_json['naturally_closed'] is True and proof_json['all_success_role_seals_verified'] is True
 assert not P.path('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_ERROR.json').exists() and not P.path('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_ERROR_RECEIPT.json').exists(),'Successful natural closure cannot inherit a failure terminal'
 assert rc['result_sha256']==RECOVERY_RESULT[1] and rc['error_sha256'] is None and r['qualification']==rc['qualification']==FLAGS
 assert len(r['checkpoints'])==73 and len(r['inherited_success_records'])==3 and len(r['controls'])==12 and all(q['passed'] for q in r['controls'])
 assert (r['case']['new_committed_roles'],r['case']['inherited_committed_roles'],r['case']['logical_committed_roles'])==(73,3,76)
 kinds=[q['metadata']['kind'] for q in r['checkpoints']]
 assert kinds.count('NEW_candidate_completed_configuration_features_momenta_EOS_and_mean')==3 and kinds.count('NEW_completed_normal_test_and_primary_comparison_contacts')==64 and kinds.count('NEW_finite0_candidate_coefficients_current_and_normal_rows')==4
 assert kinds.count('NEW_same_position_fixed_canonical_sheet_geometry_energy_and_incidence')==1 and kinds.count('NEW_candidate_current_and_full_normal_initial_CMC_measurement')==1
 for q in r['checkpoints']:
  assert q['metadata']['owner']==r['owner'] and q['metadata']['failed'] is False
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256']
 inherited=[bind_record(q) for q in r['inherited_success_records']];input_ref,basis_ref,state0=inherited
 for q in inherited:
  for name,key in (('file','sha256'),('commit_file','commit_sha256')):assert rc['input_sha256'][str(P.path(q[name]).resolve())]==q[key]
 assert input_ref['metadata']['owner']['pid']==94049 and input_ref['metadata']['owner']['source_sha256']==IO_PARENT_SHA
 assert [q['metadata']['kind'] for q in inherited]==['owned_current_mechanical_time_words_reference_finite_candidate','unchanged_registered_E_F_normal_scalar_basis','NEW_candidate_completed_configuration_features_momenta_EOS_and_mean']
 assert len(input_ref['metadata']['schema'])==4 and len(basis_ref['metadata']['schema'])==7 and state0['metadata']['column']==0
 states=[state0]+[bind_record(q) for q in r['checkpoints'] if q['metadata']['kind']=='NEW_candidate_completed_configuration_features_momenta_EOS_and_mean'];assert [q['metadata']['column'] for q in states]==[0,1,2,3]
 loads=bind_record(r['case']['loads']);assert loads['metadata']['kind']=='NEW_candidate_current_and_full_normal_initial_CMC_measurement'
 assert loads['metadata']['original_native_metric_and_literal_weak_phase_targets_unchanged'] is True and loads['metadata']['physical_adoption'] is False
 columns=r['case']['columns'];assert len(columns)==4 and loads['metadata']['columns']==[thin(q) for q in columns]
 assert all(q in r['checkpoints'] for q in columns) and r['case']['loads'] in r['checkpoints'] and r['case']['sheet'] in r['checkpoints']
 for iq,q in enumerate(columns):assert q['metadata']['column']==iq and q['metadata']['candidate_state']==thin(states[iq]) and len(q['metadata']['normal_test_refs'])==16
 proof=dict(owner=dict(r['owner']),source_sha256=RECOVERY_SHA,result_sha256=RECOVERY_RESULT[1],receipt_sha256=RECOVERY_RECEIPT[1],closure_proof_sha256=RECOVERY_CLOSURE_PROOF[1],receipt_status='CLOSED',closed_metadata_authenticated=True)
 prior=bind_record(input_ref['metadata']['refs']['phase_loads'])
 # The main read authenticated this sealed reference without registering it in
 # its receipt input map. Preserve that receipt; use the actual prior terminal.
 bind(*PRIOR_PHASE_PRODUCER_SOURCE)
 for name,h,status in (PRIOR_PHASE_PRODUCER_RESULT,PRIOR_PHASE_PRODUCER_RECEIPT,PRIOR_PHASE_ANCESTRY_PROOF):bind(name,h);assert json.loads(P.path(name).read_text())['status']==status
 pr=json.loads(P.path(PRIOR_PHASE_PRODUCER_RESULT[0]).read_text());pc=json.loads(P.path(PRIOR_PHASE_PRODUCER_RECEIPT[0]).read_text());ancestry=json.loads(P.path(PRIOR_PHASE_ANCESTRY_PROOF[0]).read_text())
 assert pr['owner']==pc['owner'] and pr['owner']['source_sha256']==PRIOR_PHASE_PRODUCER_SOURCE[1] and pc['result_sha256']==PRIOR_PHASE_PRODUCER_RESULT[1] and pc['error_sha256'] is None
 assert pr['qualification']==pc['qualification'] and all(x is False for x in pr['qualification'].values()) and len(pr['controls'])==6 and all(x['passed'] for x in pr['controls'])
 assert input_ref['metadata']['refs']['phase_loads']==pr['loads']==prior and prior in pr['checkpoints'] and prior['metadata']['owner']==pr['owner'] and prior['metadata']['failed'] is False
 for name,key in (('file','sha256'),('commit_file','commit_sha256')):assert pc['output_sha256'][prior[name]]==prior[key]
 assert ancestry['prior_source_sha256']==PRIOR_PHASE_PRODUCER_SOURCE[1] and ancestry['prior_result_sha256']==PRIOR_PHASE_PRODUCER_RESULT[1] and ancestry['prior_receipt_sha256']==PRIOR_PHASE_PRODUCER_RECEIPT[1]
 assert ancestry['prior_loads']==thin(prior) and ancestry['ancestor_input']==thin(input_ref) and ancestry['sealed_INPUT_prior_reference_equal'] is True
 assert ancestry['recovery_result_sha256']==RECOVERY_RESULT[1] and ancestry['recovery_receipt_sha256']==RECOVERY_RECEIPT[1] and ancestry['recovery_closure_proof_sha256']==RECOVERY_CLOSURE_PROOF[1]
 assert ancestry['all_prior_input_seals_verified'] is True and ancestry['all_prior_success_role_seals_verified'] is True
 return dict(result=r,receipt=rc,input=input_ref,basis=basis_ref,states=states,loads=loads,prior_phase_loads=prior,closed_proof=proof)

def phase_preparation_packet(refs):
 meta=refs['input']['metadata'];basis=read(refs['basis'],('R','dv','hats'));constants=candidate_phase_registered_constants(meta['fixed']);prior=refs['prior_phase_loads'];target=read(prior,('fixed_literal_weak_phase_charge_hi','fixed_literal_weak_phase_charge_lo'))
 selected=tuple(n for n in refs['loads']['metadata']['schema'] if n.startswith(('value_native_current_','value_metric_current_','value_literal_phase_current_','delta_native_current_','delta_metric_current_','delta_literal_phase_current_','actual_native_canonical_target_residual_','actual_metric_canonical_target_residual_','actual_phase_canonical_target_residual_','prior_signed_bridge_','prior_phase_current_')))
 current=read(refs['loads'],selected)
 for word in ('hi','lo'):assert np.array_equal(current['prior_phase_current_fixed_literal_weak_phase_charge_'+word],target['fixed_literal_weak_phase_charge_'+word])
 for n,a in {**current,**{'original_'+n:x for n,x in target.items()}}.items():keep('copied_completed_'+n,a)
 current_ref=P.checkpoint('CURRENT',arrays(AVAILABLE),dict(kind='bitcopied_completed_current_weak_and_original_target_primitive_phase_gaps',loads=thin(refs['loads']),prior_literal_weak_charge=thin(prior),norms=refs['loads']['metadata']['norms'],new_current_scatter_performed=False,physical_adoption=False));clear_current();columns=[];phase_refs=[]
 for state in refs['states']:
  iq=state['metadata']['column'];CONTEXT.update(stage='restore_completed_phase_transaction',column=iq,state=thin(state))
  schema=state['metadata']['schema'];names=tuple(n for n in schema if n.startswith('completed_phase_') or (n.startswith('candidate_phase_') and any(k in n for k in ('analytic_chain','clock_square_construction_gap','supplied_minus_constructed_projector_gap','elementary_','ratio_readout_product_defect','clock_u_lower','eps_minus_clock_u_lower'))))
  data=read(state,names);restored=finite0_restore_completed_phase_eos(data,meta,state['metadata'],constants,refs['closed_proof'])
  for n,a in data.items():keep('copied_STATE_'+n,a)
  column=dict(eos=restored['eos'],candidate_provenance=dict(state=thin(state),input=thin(refs['input']),ownership=restored['ownership'],normal_transaction_source=RECOVERY_SHA,supplied_configuration_direction=dict(node=[43,22],kind='true_conformal_scalar_hat_at_fixed_mechanical_rates')),prior_literal_weak_charge=prior)
  phase_ref=P.checkpoint('PHASE_COLUMN',arrays(AVAILABLE),dict(kind='bitcopied_completed_candidate_literal_EOS_current_H_and_supplied_contact',column=iq,candidate_provenance=column['candidate_provenance'],prior_literal_weak_charge=thin(prior),EOS_or_phase_current_replayed=False,physical_adoption=False));columns.append(column);phase_refs.append(thin(phase_ref));del data,restored;clear_current()
 CONTEXT.update(stage='NEW_candidate_phase_diagonal',phase_columns=phase_refs);cache=prepare_candidate_phase_mass(columns,basis,keep,'candidate_phase_mass')
 preparation=P.checkpoint('PREPARATION',arrays(AVAILABLE),dict(kind='NEW_candidate_dependent_literal_phase_mass_diagonal_and_cache',phase_columns=phase_refs,current=thin(current_ref),basis=thin(refs['basis']),prior_literal_weak_charge=thin(prior),point_H_strictly_positive=cache['strictly_positive_H'],point_H_resolved_positive=cache['resolved_positive_H'],diagonal_strictly_positive=cache['strictly_positive_diagonal'],phase_space_dofs=3870,phase_outer_top_free=True,configuration_contact_scope=cache['configuration_contact_scope'],no_EOS_current_action_or_fixture_replay=True,invertibility_solve_or_physical_admission=False,physical_adoption=False))
 assert len(RECORDS)==6 and CHECKS==[]
 return dict(status='COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARED_UNQUALIFIED',preparation=preparation,current=current_ref,phase_columns=phase_refs,original_literal_phase_target=thin(prior),candidate_source=refs['closed_proof'],new_H_diagonal_only=True,no_inverse_or_canonical_solve=True,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and all(x is not None for x in (PROTOCOL_SHA,RECOVERY_RESULT[1],RECOVERY_RECEIPT[1],*RECOVERY_CLOSURE_PROOF,*PRIOR_PHASE_PRODUCER_SOURCE,*PRIOR_PHASE_PRODUCER_RESULT,*PRIOR_PHASE_PRODUCER_RECEIPT,*PRIOR_PHASE_ANCESTRY_PROOF)),'Natural closed recovery, earned proof and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(IO_PARENT,IO_PARENT_SHA)
  for name,h in tuple(PINS.items())+((PROTOCOL,PROTOCOL_SHA),):bind(name,h)
  refs=completed_candidate_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256'];P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,candidate_source=refs['closed_proof'],inherited_success_records=[thin(refs[n]) for n in ('input','basis')]+[thin(q) for q in refs['states']],physical_adoption=False))
  initialize_phase_helpers()
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=phase_preparation_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_candidate_phase_mass_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
