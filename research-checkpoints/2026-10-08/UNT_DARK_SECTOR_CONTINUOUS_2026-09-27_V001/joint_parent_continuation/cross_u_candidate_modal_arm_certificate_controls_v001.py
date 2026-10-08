"""HELD root-only actual closed-candidate modal arm certificate.
Only four owned points, exact rational raw coefficients and three NEW temporal
basis applications. No saved action, producer, fixture, general160 or solve replay.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,itertools,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_MODAL_ARM_CERTIFICATE_CONTROLS_V001'
DRIVER_PROTOCOL='CANDIDATE_MODAL_ARM_CERTIFICATE_CONTROLS_V001.md'
PROTOCOL_SHA='02e7d560b5b8a18c32f3210cb0b94e089a622e9f79a4348ab1566d2153499660'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_modal_arm_certificate_v001.py':'972c096d991068d1d128a380f9253176c2270bbdf0044689c92d9d9777f6f1e8'}
PARENT_STEM='CANDIDATE_SPECIALIZED_TEMPORAL_SAVED_COMPARISON_V002'
PARENT_RESULT_SHA='fc2b009c54d1fb660879cfaf8e34530516737a90a512f4fd0870bbb1f1e8fd9b'
PARENT_RECEIPT_SHA='0e435089752904a2e001731b761e73218c19bda68960be88aeac716822db9d44'
PARENT_SOURCE='cross_u_candidate_specialized_temporal_saved_comparison_v002.py'
PARENT_SOURCE_SHA='64835bc1352e3c1a668439cd8fa0fdc890c8d93de86b7a22df9414b77bdd09e1'
PARENT_CLOSURE='ROOT_NATURAL_CLOSED_SPECIALIZED_TEMPORAL_SUCCESS_SEALS_V001.json'
PARENT_CLOSURE_SHA='15363648731f0deec31764e9b319e14b159a3294e620c08c062d64f3099b7aab'
SNAMES=('g','hi','U','z','P','w','omega')
CNAMES=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')
CACHE_PREFIX='NEW_fixed_candidate_cache_'
GAMMA_SQUARED='case0_NEW_specialized_NEW_linear_jets_z0_time_second_quotient_denominator'
np=P=None;SCOPE={};RAW={};AVAILABLE={};DD_ARRAY_CURRENT={};DESCRIPTIONS={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={}
FLAGS=dict(whole_grid_action_qualified=False,mechanical_inverse_earned=False,global_rank_earned=False,Hessian_symmetry_earned=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,physical_adoption=False)

def bind(name,checksum):
 assert checksum is not None and P.sha(P.path(name))==checksum,name
 key=str(P.path(name).resolve());assert key not in INPUTS or INPUTS[key]==checksum;INPUTS[key]=checksum

def keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name;return a

def describe(name,value):DESCRIPTIONS[name]=value

def arrays(values):return {n:np.asarray(a).copy() for n,a in values.items()}

def thin(ref):return {n:ref[n] for n in ('file','sha256','commit_file','commit_sha256')}

def clear_scratch():RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear();DESCRIPTIONS.clear();CONTEXT.clear()

def pair(data,prefix):return data[prefix+'_hi'],data[prefix+'_lo']

def initialize_io():
 global P,SCOPE
 file=list(PINS)[1];assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==PINS[file]
 names={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual','read_pair','resolve_record'}
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==13
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001',OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),SCOPE);P=types.SimpleNamespace(**{n:SCOPE[n] for n in names})

def initialize_arithmetic():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,C=1.98,ALPHA=.02/1.98,ELL=.1)
 files=list(PINS);trees=[ast.parse((BASE/n).read_text()) for n in files[:2]]
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F'}
 defs=[n for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in primitive];assert len(defs)==25
 exec(compile(ast.Module(body=defs,type_ignores=[]),files[1],'exec'),SCOPE)
 for n in base|primitive|{'ALPHA','ELL','C'}:setattr(P,n,SCOPE[n]);globals()[n]=SCOPE[n]
 compact={'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}
 for file,count,selected in ((files[2],11,None),(files[3],6,compact),(files[4],2,None),(files[5],6,None),(files[6],10,None)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (selected is None or n.name in selected)];assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_exact_exponent_product');globals()['a_prod']=P.a_prod

def selected_admission():
 for name,h in ((DRIVER_PROTOCOL,PROTOCOL_SHA),*PINS.items(),(PARENT_SOURCE,PARENT_SOURCE_SHA),(PARENT_STEM+'_RESULT.json',PARENT_RESULT_SHA),(PARENT_STEM+'_RECEIPT.json',PARENT_RECEIPT_SHA),(PARENT_CLOSURE,PARENT_CLOSURE_SHA)):bind(name,h)
 r=json.loads(P.path(PARENT_STEM+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT_STEM+'_RECEIPT.json').read_text());proof=json.loads(P.path(PARENT_CLOSURE).read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==PARENT_RESULT_SHA and rc['error_sha256'] is None and r['owner']==rc['owner']==proof['owner'] and r['owner']['pid']==4414 and r['owner']['source_sha256']==PARENT_SOURCE_SHA
 assert r['status']=='CANDIDATE_SPECIALIZED_TEMPORAL_EIGHT_SAVED_COMPARISONS_PASS' and len(r['controls'])==120 and all(x['passed'] and x['error']==0 for x in r['controls'])
 assert r['qualification']==rc['qualification']==proof['qualification'] and all(x is False for x in r['qualification'].values())
 assert proof['status']=='ROOT_NATURAL_CLOSED_SPECIALIZED_TEMPORAL_SUCCESS_SEALS_VERIFIED' and proof['naturally_closed'] and proof['observed_exit_code']==0 and proof['all_input_seals_verified'] and proof['all_success_role_seals_verified'] and proof['control_count']==120 and proof['role_count']==10
 assert proof['result_sha256']==PARENT_RESULT_SHA and proof['receipt_sha256']==PARENT_RECEIPT_SHA
 refs=dict(input=r['case']['input'],gamma=r['case']['comparisons'][0],parent_qualification=r['qualification'],parent_status=r['status'],closure_proof=dict(file=PARENT_CLOSURE,sha256=PARENT_CLOSURE_SHA))
 for ref in (refs['input'],refs['gamma']):
  bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);assert json.loads(P.path(ref['commit_file']).read_text())=={n:ref[n] for n in ('file','sha256','metadata')}
  assert ref['metadata']['owner']==r['owner'] and ref['metadata']['failed'] is False and rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
 for ref,names in ((refs['input'],list(refs['input']['metadata']['schema'])),(refs['gamma'],[GAMMA_SQUARED+'_'+w for w in ('hi','lo')])):
  for n in names:assert ref['metadata']['schema'][n]['dtype']=='float64' and ref['metadata']['schema'][n]['finite'] is True,n
 assert all(refs['gamma']['metadata']['schema'][GAMMA_SQUARED+'_'+w]['shape']==[1,4] for w in ('hi','lo'))
 return refs

def hydrate(refs):
 data=P.read_pair(refs['input'],list(refs['input']['metadata']['schema']));gamma=P.read_pair(refs['gamma'],[GAMMA_SQUARED+'_'+w for w in ('hi','lo')])
 s={n:data[CACHE_PREFIX+'raw_configuration_'+n] for n in SNAMES};c={n:data[CACHE_PREFIX+'raw_chart_'+n] for n in CNAMES};prefix=CACHE_PREFIX+'copied_positive_coefficient_'
 cache=dict(s=s,c=c,p=4,A=pair(data,CACHE_PREFIX+'anchored_raw_up_dot_zi'),NA=pair(data,CACHE_PREFIX+'paired_N_times_anchored_A'),gamma_squared=tuple(a[0].copy() for a in pair(gamma,GAMMA_SQUARED)),fixed_E0=pair(data,CACHE_PREFIX+'fixed_lowered_E0'),envelopes={n[len(prefix):]:a for n,a in data.items() if n.startswith(prefix)},constants={n:getattr(P,n) for n in ('ALPHA','ELL','C')},candidate_provenance=[thin(refs['input']),thin(refs['gamma'])],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
 assert c['ih'].shape==(4,3,3) and s['z'].shape==(32,4,4) and s['U'].shape==(4,4) and s['hi'].shape==(4,4,4)
 for n,a in data.items():keep('copied_closed_input_'+n,a)
 ft_keep('copied_closed_gamma_squared_denominator',cache['gamma_squared'],keep)
 return cache

def packet(refs):
 CONTEXT.update(stage='hydrate_exact_earned_raw_cache',refs={n:thin(refs[n]) for n in ('input','gamma')})
 cache=hydrate(refs);input_record=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='exact_cached_four_point_constants_from_CLOSED4414',refs={n:thin(refs[n]) for n in ('input','gamma')},parent_status_preserved=refs['parent_status'],parent_qualification_preserved=refs['parent_qualification'],closure_proof=refs['closure_proof'],candidate_prepare_or_primal_replayed=False,other_sections_fabricated=False,physical_adoption=False));clear_scratch()
 CONTEXT.update(stage='independent_exact_rational_arm_certificate',input=thin(input_record));certificate=candidate_modal_arm_certificate(cache,keep,describe,'NEW_modal_arm')
 P.check('NEW_exact_common_G_inverse_identity',certificate['inverse_identity'],np.broadcast_to(np.eye(3),(4,3,3)).copy(),np.ones((4,3,3)))
 coefficient_record=P.checkpoint('COEFFICIENTS',arrays(AVAILABLE),dict(kind='four_exact_nonsymmetric_common_G_and_128_signed_eta',input=thin(input_record),rational_descriptions=dict(DESCRIPTIONS),real_raw_coefficient_point_arm_invertibility_qualified=True,rounded_DD_or_global_inverse_earned=False,controls=CHECKS[-1:],physical_adoption=False));clear_scratch();completed=[];results=[]
 for coordinate in range(3):
  CONTEXT.update(stage='NEW_simultaneous_modal_basis',coordinate=coordinate,input=thin(input_record),coefficients=thin(coefficient_record),completed=[thin(r) for r in completed])
  physical=candidate_modal_basis_argument(coordinate,4,keep,'basis%d_NEW_physical'%coordinate);result=candidate_specialized_temporal_action(cache,physical,keep,'basis%d_NEW_specialized'%coordinate)
  info=candidate_modal_arm_compare(certificate,result,coordinate,keep,describe,'basis%d_NEW_modal_column'%coordinate,P.check)
  completed.append(P.checkpoint('MODAL_BASIS',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_all32_modal_axes_source_separated',coordinate=coordinate,input=thin(input_record),coefficients=thin(coefficient_record),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS[-1:],source_off_arm_zero_is_static_not_an_independent_numerical_probe=True,**info)));results.append(result);clear_scratch()
 CONTEXT.update(stage='sampled_real_matrix_perturbation_bound',input=thin(input_record),coefficients=thin(coefficient_record),basis=[thin(r) for r in completed]);measured=candidate_modal_measured_matrix_bound(certificate,results,keep,describe,'NEW_measured_modal_matrix')
 keep('control_errors',np.asarray([x['error'] for x in CHECKS]));readout=P.checkpoint('READOUT',arrays(AVAILABLE),dict(kind='three_NEW_modal_basis_real_matrix_certificate_only',input=thin(input_record),coefficients=thin(coefficient_record),basis=[thin(r) for r in completed],rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS,parent_qualification_preserved=refs['parent_qualification'],**measured))
 assert len(CHECKS)==4 and len(RECORDS)==6 and all(x['passed'] for x in CHECKS)
 return dict(status='CANDIDATE_FOUR_POINT_MODAL_ARM_CERTIFICATE_PASS',input=input_record,coefficients=coefficient_record,basis=completed,readout=readout,controls=4,roles=6,exact_raw_point_arm_qualified=True,sampled_three_basis_real_matrices_qualified=True,uniform_all_input_DD_or_global_inverse_earned=False,parent_qualification_preserved=refs['parent_qualification'],physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS,'Root release required';assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required'
 initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);refs=selected_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_refs={n:thin(refs[n]) for n in ('input','gamma')},closure_proof=refs['closure_proof'],new_basis_actions=3,controls=4,roles=6,live_recovery_accessed=False,physical_adoption=False));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   data={**RAW,**AVAILABLE,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if data:
    try:P.checkpoint('ERROR_RAW',arrays(data),dict(kind='available_NEW_modal_arm_operands',context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS)),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
