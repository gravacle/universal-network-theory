"""HELD CLOSED finite-phase to all four normal/canonical value join.
Only new62 phase stress and its replacement assembly are evaluated. Original
native/EH/ordinary/current/CMC and invariant EOS producers are never invoked.
Root releases after complete source/protocol review; all physical flags false.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V001'
DRIVER_PROTOCOL='CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V001.md'
PROTOCOL_SHA='ea315890531821cb5fee52140315a98c7fd8962c03f51afe2075f615e0b5ea10'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_candidate_phase_normal_stress_v001.py':'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd',
 'author_fragment_finite_candidate_native_EH_normal_v003.py':'5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499',
 'author_fragment_fixed_geometry_phase_normal_join_v001.py':'7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'cross_u_candidate_literal_phase_charge_response_v002.py':'887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6',
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'author_fragment_candidate_finite_phase_state_update_v001.py':'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b'}
COMPONENT_PROTOCOL=('FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V001.md','74afb238a2ebb8d57a72e31b5d11e8a2fc2f3c832399d1f759478539e5ba128e')
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
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
 global np,N
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 file=list(PINS)[0];names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','scalar_mask','scalar_lift'}
 assert len(names)==15;exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 for name in names:setattr(P,name,SCOPE[name])
 file=list(PINS)[1];exec(compile(selected_definitions(file,{'normal_keep_pair'}),file,'exec'),SCOPE)
 selections=(('author_fragment_finite_york_geometry_target_v001.py',11,None),('author_fragment_finite_york_spacetime_first_jets_v001.py',20,None),('author_fragment_candidate_phase_normal_stress_v001.py',1,None),('author_fragment_exact_exponent_two_product_v003.py',2,None),('author_fragment_fixed_geometry_phase_normal_join_v001.py',7,None),('author_fragment_finite_candidate_native_EH_normal_v003.py',1,{'finite_candidate_test_polynomials'}),('cross_u_candidate_literal_phase_charge_response_v002.py',1,{'bind_record'}))
 for file,count,chosen in selections:
  tree=ast.parse((BASE/file).read_text());chosen={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if chosen is None else chosen;assert len(chosen)==count,file
  if file=='author_fragment_fixed_geometry_phase_normal_join_v001.py':
   for n in tree.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(selected_definitions(file,chosen),file,'exec'),globals())
 globals()['PHASE_NORMAL_JOIN_AUTHOR_DRAFT']=False;globals()['PHASE_NORMAL_JOIN_AUTHORING_IN_PROGRESS']=False
 install_exact_exponent_product(SCOPE,P,keep,'NEW_phase_normal_join_exact_exponent_product')
 normal={'normal_test_mask','extend_normal_tests','restrict_normal_rows','normal_hat_jet','normal_hat_operation_envelope','scatter_normal_envelope','paired_restrict_normal_rows','paired_scatter_normal'};normal_scope=dict(SCOPE);file=list(PINS)[2]
 assert len(normal)==8;exec(compile(selected_definitions(file,normal),file,'exec'),normal_scope);N=types.SimpleNamespace(**{n:normal_scope[n] for n in normal})

def read_closed(ref,names):
 data=read(ref,names);RAW.clear();return data

def clear_completed():
 context=dict(CONTEXT);clear_current();CONTEXT.update(context)

def seal_completed(role,metadata):
 CONTEXT.update(stage='seal_'+role,role=role)
 record=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,role=role))
 CONTEXT.update(last_completed_role=thin(record));return record

def phase_normal_join_packet(refs):
 CONTEXT.update(stage='NEW_all_four_phase_normal_values_and_incremental_weak_join')
 answer=join_fixed_geometry_phase_normal_values(refs,read_closed,seal_completed,clear_completed,keep,P.check,'NEW_phase_normal_join')
 expected=['JOIN_INPUT']+(['PHASE_NORMAL_ROW']*4+['NORMAL_JOIN_COLUMN'])*4+['NORMAL_CANONICAL_VALUE_JOIN'];assert len(RECORDS)==22 and [q['metadata']['role'] for q in RECORDS]==expected
 assert len(CHECKS)==2 and all(c['passed'] is True and c['tolerance']==2e-11 for c in CHECKS)
 rows=[q for q in RECORDS if q['metadata']['role']=='PHASE_NORMAL_ROW'];columns=[q for q in RECORDS if q['metadata']['role']=='NORMAL_JOIN_COLUMN']
 assert [(q['metadata']['column'],q['metadata']['row'],q['metadata']['jet']) for q in rows]==[(iq,row,0) for iq in range(4) for row in range(4)] and [q['metadata']['column'] for q in columns]==list(range(4))
 assert answer['readout']==thin(RECORDS[-1]) and answer['columns']==[thin(q) for q in columns] and answer['value_only'] is True and answer['new_configuration_JVP'] is False
 return dict(status='FIXED_GEOMETRY_PHASE_UPDATED_FOUR_NORMAL_CANONICAL_VALUES_MEASURED',input=RECORDS[0],columns=columns,normal_rows=rows,readout=RECORDS[-1],normal_terminal=refs['normal_terminal'],finite_phase_terminal=refs['finite_terminal'],original_input=thin(refs['input']),original_basis=thin(refs['basis']),old_loads=thin(refs['loads']),unchanged_sheet=thin(refs['sheet']),new_phase_current=thin(refs['current']),original_literal_phase_charge=thin(refs['prior']),original_canonical_target_refs=refs['input']['metadata']['refs']['canonical_columns'],new_normal_norms=RECORDS[-1]['metadata']['normal_norms'],all_four_phase_normal_value_rows_recomputed=True,relative_phase_count=1,ordinary_mean_and_sheet_count=1,mechanical_current_CMC_and_test_R_Z_t_words_copied_by_action_invariance=True,original_targets_and_epsilon_unchanged=True,new_compact_chi_or_configuration_JVP=False,mixed_time_jets_or_evolution_admitted=False,finite_phase_current_exact_target_not_asserted=True,canonical_normal_CMC_or_physical_admission=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root reviewed guard/protocol release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(*COMPONENT_PROTOCOL)
  for name,h in PINS.items():bind(name,h)
  initialize_helpers();refs=fixed_geometry_phase_normal_join_admission()
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,normal_terminal=refs['normal_terminal'],finite_phase_terminal=refs['finite_terminal'],original_input=thin(refs['input']),basis=thin(refs['basis']),state_ancestry=[dict(state=thin(q['state']),old_column=thin(q['old']),finite_phase_column=thin(q['new']),old_row_value_refs=[thin(v) for v in q['phase_rows']]) for q in refs['columns']],value_only=True,new_compact_chi_contact=False,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=phase_normal_join_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],case['new_normal_norms'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_NEW_phase_normal_value_join',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
