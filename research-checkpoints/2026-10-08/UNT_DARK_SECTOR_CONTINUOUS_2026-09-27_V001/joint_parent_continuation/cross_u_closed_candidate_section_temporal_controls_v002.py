"""HELD actual CLOSED94049 candidate section0 NEW temporal action component.
Root alone releases; no live97585 records or old producer/operator/fixture calls.
Only two NEW160 temporal contacts on four predeclared support points proceed.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CLOSED_CANDIDATE_SECTION_TEMPORAL_CONTROLS_V002'
DRIVER_PROTOCOL='CLOSED_CANDIDATE_SECTION_TEMPORAL_ACTION_V001.md'
PROTOCOL_SHA='a0d0ac06acfa57ded146f2cebf56b3406fef11e930a11546bfece5e2e359ab5b'
PARENT_FILE='cross_u_finite0_candidate_action_residual_v007.py'
PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
FAILED_ERROR='CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V007_ERROR.json'
FAILED_RECEIPT='CROSS_U_FINITE0_CANDIDATE_ACTION_RESIDUAL_V007_RECEIPT.json'
FAILED_ERROR_SHA='4edf894c38ee0fd2ff54996ba45dd444f7ca3ccdedfc81c8dd3cd67ccf8a7bcd'
FAILED_RECEIPT_SHA='3e333a3023836a16c3d90701bcc49134fd022c9a990b2ce2bdf4a8551c852543'
REPAIR_PROOF=('EXACT_EXPONENT_TWO_PRODUCT_CONTROLS_V003_RESULT.json','ec1e646fd48e7a06aaf3e719dc90a2504b47cc5bfc6bf641a6e33b4650529614','EXACT_EXPONENT_TWO_PRODUCT_FRESH_AND_CLOSED_OPERAND_CONTROLS_PASS')
FINITE0_RESTORE_PARENT_SOURCE_SHA=PARENT_SHA
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'author_fragment_finite0_completed_state_restore_v001.py':'6510c60a03c0b63eb16ec2b7fa5ca7bff0ad484f8865d99a1abd7241511cfc3d',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_closed_candidate_section_temporal_action_v001.py':'6a44527c6e28681b2b8885df931290eddfcc8f142c58a8bc3039ad9a8b584536'}
np=P=None;SCOPE={};RAW={};AVAILABLE={};DD_ARRAY_CURRENT={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={}
FLAGS=dict(whole_grid_action_qualified=False,mechanical_inverse_earned=False,global_rank_earned=False,Hessian_symmetry_earned=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,physical_adoption=False)

def bind(name,checksum):
 assert checksum is not None and P.sha(P.path(name))==checksum,name
 key=str(P.path(name).resolve());assert key not in INPUTS or INPUTS[key]==checksum;INPUTS[key]=checksum

def keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a
 assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name
 return a

def arrays(values):return {n:np.asarray(a).copy() for n,a in values.items()}
def thin(ref):return {n:ref[n] for n in ('file','sha256','commit_file','commit_sha256')}
def clear_scratch():RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear();CONTEXT.clear()

def capture_tree(prefix,values):
 for n,x in values.items():
  if isinstance(x,dict):capture_tree(prefix+n+'_',x)
  elif isinstance(x,tuple) and len(x)==2 and all(isinstance(a,np.ndarray) for a in x):ms_keep(prefix+n,x,keep)
  elif isinstance(x,np.ndarray):keep(prefix+n,x)

def initialize_io():
 global P,SCOPE
 file=list(PINS)[1];assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==PINS[file]
 names={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual','read_pair','resolve_record'}
 t=ast.parse((BASE/file).read_text());defs=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==13
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001',OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),SCOPE);P=types.SimpleNamespace(**{n:SCOPE[n] for n in names})

def initialize_arithmetic():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 files=list(PINS);trees=[ast.parse((BASE/n).read_text()) for n in files[:2]]
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F'}
 defs=[n for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in primitive];assert len(defs)==25
 exec(compile(ast.Module(body=defs,type_ignores=[]),files[1],'exec'),SCOPE)
 for n in base|primitive|{'B','GC','ALPHA','ELL','C'}:setattr(P,n,SCOPE[n]);globals()[n]=SCOPE[n]
 for file,count in zip(files[2:],(11,20,7,5,6,2,12)):
  t=ast.parse((BASE/file).read_text());defs=[n for n in t.body if isinstance(n,ast.FunctionDef)];assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_exact_exponent_product');globals()['a_prod']=P.a_prod

def closed_state_admission():
 for name,h in ((PARENT_FILE,PARENT_SHA),(FAILED_ERROR,FAILED_ERROR_SHA),(FAILED_RECEIPT,FAILED_RECEIPT_SHA),(DRIVER_PROTOCOL,PROTOCOL_SHA),*PINS.items()):bind(name,h)
 name,h,status=REPAIR_PROOF;bind(name,h);assert json.loads(P.path(name).read_text())['status']==status
 e=json.loads(P.path(FAILED_ERROR).read_text());rc=json.loads(P.path(FAILED_RECEIPT).read_text())
 assert rc['status']=='CLOSED_ERROR' and rc['error_sha256']==FAILED_ERROR_SHA and rc.get('result_sha256') is None and e['status']=='FAILED'
 assert e['owner']==rc['owner'] and e['owner']['pid']==94049 and e['owner']['source_sha256']==PARENT_SHA and e['controls']==[]
 assert all(a is False for a in e['qualification'].values()) and e['qualification']==rc['qualification']
 records=e['checkpoints'][:3];assert len(e['checkpoints'])==4
 assert [r['metadata']['kind'] for r in records]==['owned_current_mechanical_time_words_reference_finite_candidate','unchanged_registered_E_F_normal_scalar_basis','NEW_candidate_completed_configuration_features_momenta_EOS_and_mean']
 for r in records:
  bind(r['file'],r['sha256']);bind(r['commit_file'],r['commit_sha256']);assert json.loads(P.path(r['commit_file']).read_text())=={n:r[n] for n in ('file','sha256','metadata')}
  assert rc['output_sha256'][r['file']]==r['sha256'] and rc['output_sha256'][r['commit_file']]==r['commit_sha256'] and r['metadata']['owner']==e['owner'] and r['metadata']['failed'] is False
 assert records[2]['metadata']['column']==0 and e['context']['state']==thin(records[2])
 return records,e

def packet(records,failed):
 input_ref,basis_ref,state_ref=records
 basis=P.read_pair(basis_ref,tuple(basis_ref['metadata']['schema']));data=P.read_pair(state_ref,finite0_completed_state_names(state_ref['metadata']['schema']))
 bundle=finite0_restore_completed_state(data,input_ref['metadata'],state_ref['metadata']);del data
 candidate,geometry,gauge,covectors,mechanical,reference,section=ms_closed_support(bundle,basis,keep,'closed_section0');del bundle
 arguments=ms_arguments(keep,'NEW_original_EF');polynomials=[];physical=[]
 for a,argument in enumerate(arguments):
  physical.append(ms_section_lift(argument,section,keep,'argument%d_serialized_lift'%a));polynomials.append(ms_direct_polynomial(argument,section,keep,'argument%d_independent_test'%a))
  for n in ('native','metric'):ms_keep('argument%d_serialized_minus_separate_polynomial_'%a+n,P.a_sub(physical[a][n],polynomials[a][n]),keep)
 capture_tree('copied_completed_point_candidate_',candidate);capture_tree('copied_completed_point_inputs_',dict(geometry=geometry,gauge=gauge,covectors=covectors,mechanical=mechanical,reference=reference))
 input_record=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='CLOSED_candidate_section0_and_predeclared_NEW_temporal_arguments',closed_parent=[thin(r) for r in records],parent_failure_preserved=dict(owner=failed['owner'],status=failed['status'],error_sha256=FAILED_ERROR_SHA,receipt_sha256=FAILED_RECEIPT_SHA),section=0,cells=[[42,21],[42,22],[43,21],[43,22]],node=[43,22],argument_count=2,candidate_primal_or_EOS_replayed=False,missing_sections_fabricated=False,physical_adoption=False));clear_scratch()
 results=[];action_records=[]
 for a in range(2):
  CONTEXT.update(stage='NEW_same_candidate_temporal_action',argument=a,input=thin(input_record),completed_actions=[thin(r) for r in action_records])
  for n,x in physical[a].items():ms_keep('argument%d_supplied_physical_'%a+n,x,keep)
  envelope=ms_rate_envelopes(candidate,physical[a],keep,'argument%d_positive'%a)
  action=ms_temporal_point_action(candidate,(geometry,gauge,covectors,mechanical,reference),physical[a],keep,'argument%d_action'%a)
  weak,we=ms_section_scatter(action['point'],envelope,section,keep,'argument%d_transpose'%a)
  results.append(dict(point=action['point'],weak=weak,point_envelope=envelope,weak_envelope=we))
  action_records.append(P.checkpoint('ACTION',arrays(AVAILABLE),dict(kind='NEW_temporal_action_and_section_transpose',section=0,argument=a,parent_state=thin(state_ref),input=thin(input_record),pure_configuration_direction_zero=True,genuine_native_rates=99,genuine_physical_metric_rates=6,phase_mechanical_rate_crosszero_scope='fixed configuration declared action only',old_operator_replayed=False,physical_adoption=False)));clear_scratch()
 CONTEXT.update(stage='NEW_partial_section_functional_and_cross_bilinear',completed_actions=[thin(r) for r in action_records])
 for action in range(2):
  for test in range(2):ms_transpose_contacts(arguments[test],polynomials[test],results[action],section,keep,'action%d_test%d'%(action,test),P.check)
 cross=ms_cross_bilinear_readout(arguments,polynomials,results,section,keep,'NEW_declared_Cstar_H_L')
 readout=P.checkpoint('READOUT',arrays({**AVAILABLE,**RAW}),dict(kind='NEW_section0_temporal_transpose_and_descriptive_cross_bilinears',actions=[thin(r) for r in action_records],controls=CHECKS,descriptive_cross_bilinears=cross,exact_symmetry_gate_or_SPD_assumption=False,partial_section_only=True,mechanical_inverse_or_global_rank_earned=False,primitive_or_canonical_target_repaired=False,physical_adoption=False))
 assert len(RECORDS)==4 and len(CHECKS)==8 and all(x['passed'] for x in CHECKS)
 return dict(status='CLOSED_CANDIDATE_PARTIAL_SECTION_TEMPORAL_ACTION_TRANSPOSE_MEASURED',input=input_record,actions=action_records,readout=readout,cross_bilinears=cross,original_failed_parent_preserved=True,first_quadrature_compact_support_only=True,other_sections_evaluated=False,mechanical_or_phase_inverse_earned=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS,'Root release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);records,failed=closed_state_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_parent_refs=[thin(r) for r in records],section=0,predeclared_support_cells=[[42,21],[42,22],[43,21],[43,22]],new_action_arguments=2,transpose_controls=8,committed_roles=4,live_recovery_accessed=False,physical_adoption=False));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=packet(records,failed)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   data={**AVAILABLE,**RAW,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if data:
    try:P.checkpoint('ERROR_RAW',arrays(data),dict(kind='available_NEW_section_temporal_operands',context=dict(CONTEXT)),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
