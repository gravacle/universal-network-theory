"""HELD finite phase state/current evaluation after an admitted NEW response.
Root releases only after natural preparation/response closures and full review.
Transport phi0 once; NEW invariant EOS/current per column and one fresh scatter.
No old225/160/EOS/current/mass/solver/fixture or physical preparation replay.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V001'
DRIVER_PROTOCOL='CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V001.md'
PROTOCOL_SHA='d0e9acda83836ac36a6074fb53052e4ae09516b68039b079141a01ca43a2001a'
PREPARATION_SOURCE=(None,None)
PREPARATION_RESULT=(None,None,'COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARED_UNQUALIFIED')
PREPARATION_RECEIPT=(None,None,'CLOSED')
PREPARATION_CLOSURE_PROOF=(None,None,None)
RESPONSE_SOURCE=(None,None)
RESPONSE_RESULT=(None,None,'CANDIDATE_LITERAL_PHASE_LINEAR_RESPONSE_ADMITTED')
RESPONSE_RECEIPT=(None,None,'CLOSED')
RESPONSE_CLOSURE_PROOF=(None,None,None)
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_candidate_literal_phase_charge_response_v002.py':'887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6',
 'author_fragment_candidate_finite_phase_state_update_v001.py':'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b',
 'author_fragment_finite0_completed_state_restore_v002.py':'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RESULT.json':'ee8edf2f0f618a3d290fb847e97d799c2446ef245093fe3e3a1ea3f8f921238d',
 'CLOSED_REGISTERED_SCALAR_HAT_CONDITIONING_AUDIT_V002_RECEIPT.json':'f1806a9b804a14e8236814840e2c82002c493b8cbf1f65fb1a5b98807ce6979a',
 'CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json':'5f632a9927d41e36a40c7f2e0988997905ff99ac8dfef985307ce7723f63d4f9'}
COMPONENT_PROTOCOL=('CANDIDATE_FINITE_PHASE_STATE_UPDATE_V001.md','a52f704ae4b700361d4917af6ed1a40ede8d29fbef8c1c86f587d9b060503066')
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for name,h in PINS.items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h,name
 names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(IO_PARENT,names),IO_PARENT,'exec'),globals());initialize_io()
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,{'recheck'}),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']

def initialize_helpers():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 file='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
 names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','scalar_mask','scalar_lift','scalar_scatter','dd_scalar_scatter'}
 assert len(names)==17;exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 for name in names:setattr(P,name,SCOPE[name])
 selections=(('author_fragment_finite_york_geometry_target_v001.py',11,None),('author_fragment_finite_york_spacetime_first_jets_v001.py',20,None),('author_fragment_candidate_invariant_phase_eos_current_v001.py',3,None),('author_fragment_exact_exponent_two_product_v003.py',2,None),('author_fragment_candidate_finite_phase_state_update_v001.py',5,None),('author_fragment_finite0_completed_state_restore_v002.py',1,{'finite0_validate_saved_transaction_ownership'}),('cross_u_candidate_literal_phase_charge_response_v002.py',2,{'bind_record','candidate_phase_response_admission'}))
 for file,count,names in selections:
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if names is None else names;assert len(names)==count,file
  if file=='author_fragment_finite0_completed_state_restore_v002.py':
   for n in tree.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('FINITE0_RESTORE_PARENT_SOURCE_SHA','FINITE0_RESTORE_RECOVERY_SOURCE_SHA'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals()['FINITE_PHASE_AUTHOR_DRAFT']=False;globals()['FINITE_PHASE_AUTHORING_IN_PROGRESS']=False
 install_exact_exponent_product(SCOPE,P,keep,'NEW_finite_phase_exact_exponent_product')

def read_closed(ref,names):
 data=read(ref,names);RAW.clear();return data

def clear_completed():
 context=dict(CONTEXT);clear_current();CONTEXT.update(context)

def seal_completed(role,metadata):
 CONTEXT.update(stage='seal_'+role,role=role)
 record=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,role=role))
 CONTEXT.update(last_completed_role=thin(record));return record

def finite_phase_evaluation_packet(refs):
 CONTEXT.update(stage='NEW_finite_phase_covector_EOS_and_current')
 answer=evaluate_candidate_finite_phase_update(refs,read_closed,seal_completed,clear_completed,keep,'NEW_finite_phase',baseline_mixed=None)
 assert len(RECORDS)==6 and CHECKS==[] and [r['metadata']['role'] for r in RECORDS]==['PHASE_UPDATE_INPUT']+['FINITE_PHASE_COLUMN']*4+['FINITE_PHASE_CURRENT']
 assert [r['metadata']['column'] for r in RECORDS[1:5]]==[0,1,2,3]
 md=RECORDS[-1]['metadata'];columns=RECORDS[1:5]
 return dict(status='CANDIDATE_FINITE_PHASE_STATE_AND_LITERAL_CURRENT_MEASURED',input=RECORDS[0],columns=columns,current=RECORDS[-1],parent_preparation=thin(refs['prepared']['preparation']),parent_response=refs['response_source'],original_input=thin(refs['original_input']),original_literal_phase_charge=thin(refs['prepared']['prior']),original_canonical_target_refs=refs['original_input']['metadata']['refs']['canonical_columns'],original_target_words_unchanged=True,linear_response_admitted=True,strict_EOS_domain_passed=True,new_H_strictly_positive=[r['metadata']['new_H_strictly_positive'] for r in columns],new_H_resolved_positive=[r['metadata']['new_H_resolved_positive'] for r in columns],target_residual_raw_scaled_norms=md['target_residual_raw_scaled_norms'],descriptive_original_raw_scaled_ratios=md['descriptive_original_raw_scaled_ratios'],ratio_scope=md['ratio_scope'],phase_charge_restored=False,weak_remainder_includes_scatter_and_addition_defects=True,mixed_time_jets_are_response_increments_only=True,instantaneous_spatial_phase_unchanged=True,new_phase_mass_diagonal_constructed=False,configuration_unchanged=True,mechanical_canonical_currents_reevaluated=False,normal_constraints_reevaluated=False,initial_CMC_reevaluated=False,next_required_coupling=dict(canonical='fresh native/metric canonical currents at unchanged geometry/rates and changed phase with original targets retained',normal='fresh literal phase normal stress once with original native/EH and ordinary terms in all four normal equations; old normal totals cannot be adopted',initial_CMC='retain or freshly authenticate unchanged metric/gauge mechanical K/CMC words with their original primitive/connection defects',mixed_phase='supply authentic baseline mixed time jets before total mixed phase derivatives or evolution; stored response R/Z are increments',phase='fresh positive H/diagonal and original target-relative raw/scaled certificate before any next linear phase response or finite charge acceptance'),finite_candidate_admitted=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and all(x is not None for ref in (PREPARATION_SOURCE,PREPARATION_RESULT,PREPARATION_RECEIPT,PREPARATION_CLOSURE_PROOF,RESPONSE_SOURCE,RESPONSE_RESULT,RESPONSE_RECEIPT,RESPONSE_CLOSURE_PROOF) for x in ref),'Root release and naturally closed admitted preparation/response proofs required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(*COMPONENT_PROTOCOL)
  for name,h in PINS.items():bind(name,h)
  initialize_helpers();refs=candidate_finite_phase_admission()
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,preparation=dict(source=PREPARATION_SOURCE,result=PREPARATION_RESULT,receipt=PREPARATION_RECEIPT,proof=PREPARATION_CLOSURE_PROOF),response=refs['response_source'],original_input=thin(refs['original_input']),state_ancestry=[dict(state=thin(q['state']),candidate_provenance=q['candidate_provenance']) for q in refs['columns']],baseline_mixed_time_jets_supplied=False,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=finite_phase_evaluation_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],case['descriptive_original_raw_scaled_ratios'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_NEW_finite_phase_state_and_current',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
