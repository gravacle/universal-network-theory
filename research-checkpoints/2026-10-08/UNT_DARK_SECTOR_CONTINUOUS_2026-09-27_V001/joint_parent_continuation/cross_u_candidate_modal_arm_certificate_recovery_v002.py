"""HELD root-only actual closed-candidate modal arm certificate.
Restore earned four-point INPUT/COEFFICIENTS and completed coordinate0 from
CLOSED_ERROR5934. Only coordinates1/2 and the final measured bound are new.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,itertools,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_MODAL_ARM_CERTIFICATE_RECOVERY_V002'
DRIVER_PROTOCOL='CANDIDATE_MODAL_ARM_CERTIFICATE_RECOVERY_V001.md'
PROTOCOL_SHA='c854cfd3995129d6017d75239571c031262c04231f9bdc1cd24e0b2ed3ce616c'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_modal_arm_certificate_v001.py':'972c096d991068d1d128a380f9253176c2270bbdf0044689c92d9d9777f6f1e8'}
FAILED_STEM='CANDIDATE_MODAL_ARM_CERTIFICATE_CONTROLS_V002'
FAILED_ERROR_SHA='23652db2f5b77c6b7eb3729ee4e5f742a4a2cf86bdfd88861521b0fbc21260bd'
FAILED_RECEIPT_SHA='5dae7e8d104279b04d4f445bdc39a6150a606068e33272d35b1b8e282e1b42c2'
FAILED_SOURCE='cross_u_candidate_modal_arm_certificate_controls_v002.py'
FAILED_SOURCE_SHA='93e8e23e20b56c48688e4542bad6e0adb6dba69d061fd01a3fc9aa0b8da9f932'
FAILED_CLOSURE='ROOT_NATURAL_CLOSED_MODAL_ARM_PARTIAL_FAILURE_SEALS_V001.json'
FAILED_CLOSURE_SHA='e5bcc572bac2f375d4cc864126595097c8c06338a259f5560113d6cee373c7e6'
SNAMES=('g','hi','U','z','P','w','omega')
CNAMES=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')
CACHE_PREFIX='copied_closed_input_NEW_fixed_candidate_cache_'
GAMMA_SQUARED='copied_closed_gamma_squared_denominator'
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
 for name,h in ((DRIVER_PROTOCOL,PROTOCOL_SHA),*PINS.items(),(FAILED_SOURCE,FAILED_SOURCE_SHA),(FAILED_STEM+'_ERROR.json',FAILED_ERROR_SHA),(FAILED_STEM+'_RECEIPT.json',FAILED_RECEIPT_SHA),(FAILED_CLOSURE,FAILED_CLOSURE_SHA)):bind(name,h)
 e=json.loads(P.path(FAILED_STEM+'_ERROR.json').read_text());rc=json.loads(P.path(FAILED_STEM+'_RECEIPT.json').read_text());proof=json.loads(P.path(FAILED_CLOSURE).read_text())
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==FAILED_ERROR_SHA and e['owner']==rc['owner']==proof['owner'] and e['owner']['pid']==5934 and e['owner']['source_sha256']==FAILED_SOURCE_SHA
 assert e['raw_preservation_traceback'] is None and e['closing_traceback'] is None and e['traceback'].endswith("TypeError: dict() got multiple values for keyword argument 'coordinate'\n") and 'line 114, in packet' in e['traceback'] and FAILED_SOURCE in e['traceback']
 assert e['context']['stage']=='NEW_simultaneous_modal_basis' and e['context']['coordinate']==0 and e['context']['completed']==[] and e['context']['control']=='basis0_NEW_modal_column_independent_modal_column'
 assert e['qualification']==rc['qualification']==proof['qualification'] and all(x is False for x in e['qualification'].values()) and not P.path(FAILED_STEM+'_RESULT.json').exists()
 assert proof['status']=='ROOT_NATURAL_CLOSED_MODAL_ARM_PARTIAL_FAILURE_SEALS_VERIFIED' and proof['naturally_closed'] and proof['exit_code']==1 and proof['all_input_seals_verified'] and proof['all_success_role_seals_verified'] and proof['all_preserved_failed_raw_seals_verified'] and proof['original_failed_raw_metadata_unchanged']
 assert proof['error_sha256']==FAILED_ERROR_SHA and proof['receipt_sha256']==FAILED_RECEIPT_SHA and proof['source_sha256']==FAILED_SOURCE_SHA and proof['completed_numerical_axes']==[0] and proof['unstarted_axes']==[1,2] and proof['sampled_three_basis_matrix_invertibility_completed'] is False
 controls=e['controls'];assert len(controls)==2 and controls==proof['controls'] and all(x['passed'] and x['tolerance']==2e-11 and x['ordinal']==i for i,x in enumerate(controls))
 assert controls[0]['name']=='NEW_exact_common_G_inverse_identity' and controls[1]['name']=='basis0_NEW_modal_column_independent_modal_column';records=e['checkpoints'];assert len(records)==3
 refs=dict(input=records[0],coefficients=records[1],basis0=records[2],controls=controls,original_owner=e['owner'],original_failed_qualification=e['qualification'],original_status=rc['status'],closure_proof=dict(file=FAILED_CLOSURE,sha256=FAILED_CLOSURE_SHA))
 assert proof['earned_input']==refs['input'] and proof['earned_coefficients']==refs['coefficients'] and proof['completed_first_axis_failed_raw']==refs['basis0']
 assert e['context']['input']==thin(refs['input']) and e['context']['coefficients']==thin(refs['coefficients'])
 for key,count,failed in (('input',69,False),('coefficients',23,False),('basis0',429,True)):
  ref=refs[key];bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);assert json.loads(P.path(ref['commit_file']).read_text())=={n:ref[n] for n in ('file','sha256','metadata')}
  assert ref['metadata']['owner']==e['owner'] and ref['metadata']['failed'] is failed and len(ref['metadata']['schema'])==count and rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
  for n,shape in ref['metadata']['schema'].items():assert shape['dtype']=='float64' and shape['finite'] is True,n
 points=refs['coefficients']['metadata']['rational_descriptions']['NEW_modal_arm_completed_rational_points'];assert len(points)==4 and all(r['determinant_resolved'] and len(r['modes'])==32 and all(m['eta_resolved'] for m in r['modes']) for r in points)
 for n,shape in (('native_density',[4,99]),('metric_native_density',[4,6]),('metric_EH_density',[4,6]),('metric_total_density',[4,6]),('Pi',[32,4,4,4])):
  for word in ('hi','lo'):assert refs['basis0']['metadata']['schema']['basis0_NEW_specialized_NEW_linear_canonical_'+n+'_'+word]['shape']==shape
 return refs

def hydrate_input(data,refs):
 s={n:data[CACHE_PREFIX+'raw_configuration_'+n] for n in SNAMES};c={n:data[CACHE_PREFIX+'raw_chart_'+n] for n in CNAMES};prefix=CACHE_PREFIX+'copied_positive_coefficient_'
 cache=dict(s=s,c=c,p=4,A=pair(data,CACHE_PREFIX+'anchored_raw_up_dot_zi'),NA=pair(data,CACHE_PREFIX+'paired_N_times_anchored_A'),gamma_squared=pair(data,GAMMA_SQUARED),fixed_E0=pair(data,CACHE_PREFIX+'fixed_lowered_E0'),envelopes={n[len(prefix):]:a for n,a in data.items() if n.startswith(prefix)},constants={n:getattr(P,n) for n in ('ALPHA','ELL','C')},candidate_provenance=[thin(refs['input'])],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
 assert c['ih'].shape==(4,3,3) and s['z'].shape==(32,4,4) and s['U'].shape==(4,4) and s['hi'].shape==(4,4,4) and all(a.shape==(4,) for a in cache['gamma_squared'])
 return cache

def copy_saved_role(ref,tag,meta):
 data=P.read_pair(ref,list(ref['metadata']['schema']));record=P.checkpoint(tag,arrays(data),dict(meta,inherited_source=thin(ref),inherited_source_owner=ref['metadata']['owner'],inherited_source_failed=ref['metadata']['failed'],original_source_failed_metadata_unchanged=True,numerical_outputs_recomputed=False));return data,record

def packet(refs):
 CHECKS.extend([dict(x) for x in refs['controls']]);preserved=dict(original_status=refs['original_status'],original_failed_qualification=refs['original_failed_qualification'],closure_proof=refs['closure_proof'])
 CONTEXT.update(stage='bitcopy_earned_INPUT',source=thin(refs['input']));data,input_record=copy_saved_role(refs['input'],'INPUT',dict(kind='earned_modal_arm_cache_restored_without_prepare',**preserved));cache=hydrate_input(data,refs);clear_scratch()
 CONTEXT.update(stage='bitcopy_earned_COEFFICIENTS',source=thin(refs['coefficients']),input=thin(input_record));descriptions=refs['coefficients']['metadata']['rational_descriptions'];data,coefficient_record=copy_saved_role(refs['coefficients'],'COEFFICIENTS',dict(kind='earned_all4G_all128eta_exact_certificate_without_recalculation',input=thin(input_record),rational_descriptions=descriptions,controls=CHECKS[:1],**preserved))
 certificate=dict(expected=pair(data,'NEW_modal_arm_independent_arm_matrix'),envelope=data['NEW_modal_arm_arm_uncancelled_envelope'],inverse_identity=data['NEW_modal_arm_exact_inverse_product'],rational_points=descriptions['NEW_modal_arm_completed_rational_points'],real_raw_coefficient_point_arm_invertibility_qualified=True,rounded_DD_arm_implementation_invertibility_qualified=False,point_or_global_Schur_inverse_earned=False,physical_adoption=False);clear_scratch()
 CONTEXT.update(stage='bitcopy_completed_coordinate0',source=thin(refs['basis0']),input=thin(input_record),coefficients=thin(coefficient_record));data,basis0=copy_saved_role(refs['basis0'],'INHERITED_MODAL_BASIS',dict(kind='completed_coordinate0_from_failed_metadata_publication',coordinate=0,input=thin(input_record),coefficients=thin(coefficient_record),rational_descriptions=refs['basis0']['metadata']['rational_descriptions'],controls=CHECKS[1:2],original_error_and_missing_RESULT_preserved=True,**preserved))
 result0=dict(point={n:pair(data,'basis0_NEW_specialized_NEW_linear_canonical_'+key) for n,key in (('native','native_density'),('metric_native','metric_native_density'),('metric_EH','metric_EH_density'),('metric_total','metric_total_density'))});completed=[basis0];results=[result0];clear_scratch()
 for coordinate in (1,2):
  CONTEXT.update(stage='NEW_simultaneous_modal_basis',coordinate=coordinate,input=thin(input_record),coefficients=thin(coefficient_record),completed=[thin(r) for r in completed])
  physical=candidate_modal_basis_argument(coordinate,4,keep,'basis%d_NEW_physical'%coordinate);result=candidate_specialized_temporal_action(cache,physical,keep,'basis%d_NEW_specialized'%coordinate)
  info=candidate_modal_arm_compare(certificate,result,coordinate,keep,describe,'basis%d_NEW_modal_column'%coordinate,P.check);assert info['coordinate']==coordinate
  metadata=dict(info);metadata.update(kind='NEW_all32_modal_axes_source_separated',input=thin(input_record),coefficients=thin(coefficient_record),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS[-1:],source_off_arm_zero_is_static_not_an_independent_numerical_probe=True,original_failed_status_preserved=refs['original_status'])
  completed.append(P.checkpoint('MODAL_BASIS',arrays({**RAW,**AVAILABLE}),metadata));results.append(result);clear_scratch()
 CONTEXT.update(stage='sampled_real_matrix_perturbation_bound',input=thin(input_record),coefficients=thin(coefficient_record),basis=[thin(r) for r in completed]);measured=candidate_modal_measured_matrix_bound(certificate,results,keep,describe,'NEW_measured_modal_matrix')
 keep('control_errors',np.asarray([x['error'] for x in CHECKS]));readout=P.checkpoint('READOUT',arrays(AVAILABLE),dict(kind='three_completed_modal_basis_real_matrix_certificate_only',input=thin(input_record),coefficients=thin(coefficient_record),basis=[thin(r) for r in completed],rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS,original_failed_status_preserved=refs['original_status'],**measured))
 assert len(CHECKS)==4 and len(RECORDS)==6 and all(x['passed'] for x in CHECKS)
 return dict(status='CANDIDATE_FOUR_POINT_MODAL_ARM_RECOVERY_CERTIFICATE_PASS',input=input_record,coefficients=coefficient_record,basis=completed,readout=readout,controls=4,inherited_controls=2,new_basis_coordinates=[1,2],roles=6,exact_raw_point_arm_qualified=True,sampled_three_basis_real_matrices_qualified=True,uniform_all_input_DD_or_global_inverse_earned=False,original_failed_status_preserved=refs['original_status'],original_failed_qualification_preserved=refs['original_failed_qualification'],physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS,'Root release required';assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required'
 initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);refs=selected_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_refs={n:thin(refs[n]) for n in ('input','coefficients','basis0')},closure_proof=refs['closure_proof'],new_basis_coordinates=[1,2],inherited_controls=2,controls=4,roles=6,live_recovery_accessed=False,physical_adoption=False));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   data={**RAW,**AVAILABLE,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if data:
    try:P.checkpoint('ERROR_RAW',arrays(data),dict(kind='available_recovered_and_NEW_modal_arm_operands',context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS)),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
