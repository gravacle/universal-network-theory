"""HELD NEW candidate phase response; selected definitions only, root numerical ownership."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_LITERAL_PHASE_CHARGE_RESPONSE_V001'
PROTOCOL='CROSS_U_CANDIDATE_LITERAL_PHASE_CHARGE_RESPONSE_V001.md'
PROTOCOL_SHA='9ee43bb828777adefffec3d843a5a04b7790a695b10e366de4612bf083ef0c14'
PREPARATION_SOURCE=(None,None)
PREPARATION_RESULT=(None,None,'COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARED_UNQUALIFIED')
PREPARATION_RECEIPT=(None,None,'CLOSED')
PREPARATION_CLOSURE_PROOF=(None,None,None)
CAP=160
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_finite0_candidate_action_residual_v007.py':'ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58',
 'author_fragment_phase_literal_charge_hessian_v002.py':'293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143',
 'author_fragment_phase_fixed_weak_charge_response_core_v001.py':'331fb805f572de4257f76e879ba28ceef5e20d4cb4898260e712c95efb553c2c',
 'author_fragment_candidate_literal_phase_mass_v001.py':'0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RESULT.json':'ee8edf2f0f618a3d290fb847e97d799c2446ef245093fe3e3a1ea3f8f921238d',
 'CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RECEIPT.json':'f1806a9b804a14e8236814840e2c82002c493b8cbf1f65fb1a5b98807ce6979a',
 'CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json':'5f632a9927d41e36a40c7f2e0988997905ff99ac8dfef985307ce7723f63d4f9'}
np=P=K=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])

def initialize():
 global np,K
 for file,h in PINS.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
 io='cross_u_finite0_candidate_action_residual_v007.py';names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(io,names),io,'exec'),globals());initialize_io()
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,CAP=CAP,LINEAR_TOL=1e-10)
 file=list(PINS)[0];names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_reshape','scalar_mask','scalar_lift','dd_scalar_scatter','dd_node_update','minres_core'}
 exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 for n in names:setattr(P,n,SCOPE[n])
 P.LINEAR_TOL=1e-10
 file='author_fragment_phase_literal_charge_hessian_v002.py';names={'phase_pair_keep','phase_scalar_value','phase_mass_action'};scope=dict(np=np,P=P)
 exec(compile(selected_definitions(file,names),file,'exec'),scope);K=types.SimpleNamespace(**{n:scope[n] for n in names})
 for file,count in (('author_fragment_phase_fixed_weak_charge_response_core_v001.py',6),('author_fragment_exact_exponent_two_product_v003.py',2)):
  names={n.name for n in ast.parse((BASE/file).read_text()).body if isinstance(n,ast.FunctionDef)};assert len(names)==count
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_candidate_literal_phase_mass_v001.py';exec(compile(selected_definitions(file,{'candidate_phase_mass_pair','candidate_phase_mass_certificate'}),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_candidate_phase_response_exact_product')

def bind_record(ref):
 bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);cm=json.loads(P.path(ref['commit_file']).read_text())
 assert cm['file']==ref['file'] and cm['sha256']==ref['sha256']
 if 'metadata' in ref:assert cm['metadata']==ref['metadata']
 return dict(file=ref['file'],sha256=ref['sha256'],commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'],metadata=cm['metadata'])

def candidate_phase_response_admission():
 bind(*PREPARATION_SOURCE)
 for name,h,status in (PREPARATION_RESULT,PREPARATION_RECEIPT,PREPARATION_CLOSURE_PROOF):bind(name,h);assert json.loads(P.path(name).read_text())['status']==status,name
 r=json.loads(P.path(PREPARATION_RESULT[0]).read_text());rc=json.loads(P.path(PREPARATION_RECEIPT[0]).read_text());proof=json.loads(P.path(PREPARATION_CLOSURE_PROOF[0]).read_text())
 assert r['owner']==rc['owner']==proof['owner'] and r['owner']['source_sha256']==proof['source_sha256']==PREPARATION_SOURCE[1]
 assert rc['result_sha256']==proof['result_sha256']==PREPARATION_RESULT[1] and proof['receipt_sha256']==PREPARATION_RECEIPT[1] and rc['error_sha256'] is None
 assert type(proof['exit_code']) is int and proof['exit_code']==0 and proof['naturally_closed'] is True and proof['all_success_role_seals_verified'] is True
 parent_stem=PREPARATION_RESULT[0].removesuffix('_RESULT.json');assert not P.path(parent_stem+'_ERROR.json').exists() and not P.path(parent_stem+'_ERROR_RECEIPT.json').exists()
 assert r['qualification']==rc['qualification']==FLAGS and r['controls']==[] and len(r['checkpoints'])==6 and r['case']['no_inverse_or_canonical_solve'] is True
 records=[bind_record(q) for q in r['checkpoints']]
 for q in records:
  assert q['metadata']['owner']==r['owner'] and q['metadata']['failed'] is False
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256']
 prep=bind_record(r['case']['preparation']);current=bind_record(r['case']['current']);assert prep in records and current in records
 assert prep['metadata']['kind']=='NEW_candidate_dependent_literal_phase_mass_diagonal_and_cache' and current['metadata']['kind']=='bitcopied_completed_current_weak_and_original_target_primitive_phase_gaps'
 assert prep['metadata']['phase_space_dofs']==3870 and prep['metadata']['phase_outer_top_free'] is True and prep['metadata']['invertibility_solve_or_physical_admission'] is False
 columns=[q for q in records if q['metadata']['kind']=='bitcopied_completed_candidate_literal_EOS_current_H_and_supplied_contact'];assert [q['metadata']['column'] for q in columns]==[0,1,2,3]
 assert [thin(q) for q in columns]==prep['metadata']['phase_columns']==r['case']['phase_columns'] and prep['metadata']['current']==thin(current)
 assert all(q['metadata']['EOS_or_phase_current_replayed'] is False for q in columns) and all(q['metadata']['physical_adoption'] is False for q in records)
 basis=bind_record(prep['metadata']['basis']);prior=bind_record(prep['metadata']['prior_literal_weak_charge']);assert thin(prior)==r['case']['original_literal_phase_target']==current['metadata']['prior_literal_weak_charge']
 for q in (basis,prior):
  for name,key in (('file','sha256'),('commit_file','commit_sha256')):assert rc['input_sha256'][str(P.path(q[name]).resolve())]==q[key]
 hat=json.loads(P.path('CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RESULT.json').read_text());htr=json.loads(P.path('CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RECEIPT.json').read_text())
 assert hat['status']=='ACTUAL_REGISTERED_SCALAR_HAT_INJECTIVITY_BOUND_PASS' and htr['status']=='CLOSED' and htr['result_sha256']==PINS['CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RESULT.json'] and htr['error_sha256'] is None
 assert thin(basis)==hat['reference'] and hat['evidence']['independent_node_count']==3870 and hat['evidence']['outer_and_top_scalar_nodes_free'] is True
 component=json.loads(P.path('CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json').read_text());assert component['status']=='CANDIDATE_LITERAL_PHASE_MASS_MANUFACTURED_COMPONENT_CONTROLS_PASS'
 return dict(result=r,preparation=prep,current=current,basis=basis,prior=prior,columns=columns,proof=proof,stored_hat_bound=hat['phase_mass_bound'])

def candidate_phase_response_packet(refs):
 CONTEXT.update(stage='copy_closed_candidate_phase_cache')
 prep=read(refs['preparation'],tuple(refs['preparation']['metadata']['schema']));current=read(refs['current'],tuple(refs['current']['metadata']['schema']));basis=read(refs['basis'],('R','dv','hats'))
 for family,data in (('prepared',prep),('completed_current',current),('original_basis',basis)):
  for n,a in data.items():keep('copied_'+family+'_'+n,a)
 H=pair_from(prep,'candidate_phase_mass_candidate_H');diagonal=pair_from(prep,'candidate_phase_mass_diagonal_completed')
 target=pair_from(current,'copied_completed_original_fixed_literal_weak_phase_charge');charge=pair_from(current,'copied_completed_value_literal_phase_current')
 rhs=P.a_sub(target,charge);phase_response_keep('NEW_original_target_minus_current_RHS',rhs,keep)
 stored_residual=pair_from(current,'copied_completed_actual_phase_canonical_target_residual');gap=P.a_add(rhs,stored_residual);phase_response_keep('NEW_RHS_plus_saved_current_minus_target_contact',gap,keep)
 input_ref=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='closed_candidate_NEW_H_diagonal_and_original_literal_target_current_RHS',preparation=thin(refs['preparation']),current=thin(refs['current']),basis=thin(refs['basis']),prior_literal_weak_charge=thin(refs['prior']),candidate_proof=refs['proof'],stored_hat_bound=refs['stored_hat_bound'],new_current_EOS_scatter_or_diagonal_replayed=False,physical_adoption=False));clear_current()
 md=refs['preparation']['metadata'];assert md['point_H_strictly_positive'] is True and md['point_H_resolved_positive'] is True and md['diagonal_strictly_positive'] is True
 mask=P.scalar_mask();assert np.count_nonzero(mask)==3870 and H[0].shape==H[1].shape==(15136,) and diagonal[0].shape==diagonal[1].shape==rhs[0].shape==rhs[1].shape==(87,45)
 assert np.all(prep['candidate_phase_mass_point_H_positive_construction_margin']>0) and np.all(H[0]>abs(H[1])) and np.all(diagonal[0][mask]>abs(diagonal[1][mask]))
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],prep['candidate_phase_mass_NEW_basis_'+n])
 assert all(np.all(w[0]==0) for x in (rhs,target,charge) for w in x)
 initial=P.a_dd(np.zeros((87,45)));phase_response_keep('NEW_phase_response_initial_nodes',initial,keep);phase_response_keep('NEW_phase_response_initial_RHS',rhs,keep)
 initial_ref=P.checkpoint('INITIAL',arrays(AVAILABLE),dict(kind='zero_NEW_response_increment_with_unchanged_physical_phase_baseline',input=thin(input_ref),actual_budget=dict(cycles=1,cap=CAP),zero_unknown_is_response_not_physical_state_reset=True,physical_adoption=False));clear_current();CONTEXT.update(stage='NEW_candidate_scalar_charge_response')
 label='NEW_candidate_phase_response';answer=phase_response_solve(H,diagonal,rhs,basis,keep,label,cap=CAP,max_cycles=1)
 capture_families('completed_answer_',answer);scale=AVAILABLE[label+'_new_phase_positive_scale']
 exact_rhs_zero=all(np.all(w[mask]==0) for w in rhs)
 if exact_rhs_zero:
  assert answer['history']==[] and all(np.all(w==0) for w in answer['nodal_pair']);action=P.a_dd(np.zeros((87,45)))
 else:
  assert len(answer['history'])==1 and answer['history'][0]['cap']==CAP
  action=phase_response_unpack(pair_from(AVAILABLE,label+'_cycle_001_final_original_action'))
 phase_response_keep('completed_original_mass_action',action,keep)
 certificate=candidate_phase_mass_certificate(rhs,action,scale,keep,'NEW_candidate_original_phase_certificate')
 assert all(np.array_equal(w[mask],a) for w,a in zip(certificate['residual'],answer['original_residual']))
 # The fresh113 exact-zero-word fallback and original ratios own final admission.
 admitted=bool(np.all(certificate['ratios']<=1e-10))
 capture_families('completed_certificate_',certificate)
 solution=P.checkpoint('SOLUTION',arrays({**AVAILABLE,**RAW}),dict(kind='NEW_candidate_literal_phase_3870_paired_linear_charge_response',input=thin(input_ref),initial=thin(initial_ref),history=answer['history'],actual_budget=dict(cycles=1,cap=CAP),original_raw_scaled_tolerance=1e-10,response_admitted=admitted,exact_zero_RHS=exact_rhs_zero,rounded_recurrence_is_numerical_only=True,finite_phase_charge_restored=False,configuration_updated=False,physical_adoption=False));clear_current()
 jets={n+'_'+word:pair[i] for n,pair in answer['jet_pairs'].items() for i,word in enumerate(('hi','lo'))}
 jet_ref=P.checkpoint('RATE_JETS',arrays(jets),dict(kind='same_original_Q1_phase_response_value_R_Z_mixed_jets',solution=thin(solution),response_admitted=admitted,mixed_jet_rule='delta_partial_t_phi_i equals partial_i_delta_phi_t',instantaneous_spatial_phase_replaced=False,finite_charge_restored=False,physical_adoption=False))
 return dict(status='CANDIDATE_LITERAL_PHASE_LINEAR_RESPONSE_ADMITTED' if admitted else 'CANDIDATE_LITERAL_PHASE_LINEAR_RESPONSE_NONADMITTED',response_admitted=admitted,preparation=thin(refs['preparation']),input=input_ref,initial=initial_ref,solution=solution,rate_jets=jet_ref,original_raw_scaled_ratios=certificate['ratios'].tolist(),history=answer['history'],actual_budget=dict(cycles=1,cap=CAP),original_literal_weak_charge_unchanged=True,finite_phase_charge_restored=False,configuration_updated=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and all(x is not None for x in (PROTOCOL_SHA,*PREPARATION_SOURCE,*PREPARATION_RESULT,*PREPARATION_RECEIPT,*PREPARATION_CLOSURE_PROOF)),'Root release and natural closed candidate preparation proof required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(PROTOCOL,PROTOCOL_SHA)
  for name,h in PINS.items():bind(name,h)
  refs=candidate_phase_response_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,parent=refs['proof'],physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=candidate_phase_response_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],case['original_raw_scaled_ratios'],rh);return 0 if case['response_admitted'] else 3
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_candidate_phase_response_operands',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));raise
if __name__=='__main__':raise SystemExit(main())
