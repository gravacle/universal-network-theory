"""HELD root-only paired local-factor applications and one NEW mixed action.
Use12 completed canonical RHS columns without action replay, then one unequal-
mode NEW147 direction and its inverse application. No old producer/certificate.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_MODAL_HEAD_FACTOR_APPLY_CONTROLS_V003'
DRIVER_PROTOCOL='CANDIDATE_MODAL_HEAD_FACTOR_APPLY_CONTROLS_V002.md'
PROTOCOL_SHA='a8ff0f9503f25dd13edb453ea24fd1dd289851608ac117d13602c977f5458745'
HEAD_SOURCE=('cross_u_candidate_modal_head_local_certificate_v002.py','86d418075600731ab8125075906d6b5b0fea9d48548d4e941d6fba61a6be2bb5')
HEAD_RESULT=('CANDIDATE_MODAL_HEAD_LOCAL_CERTIFICATE_V002_RESULT.json','ca3657a497949d06979642f4f4f95a50a3bfd5ea2db85136ef08bc377790e55e','CANDIDATE_FOUR_POINT_DIRECTED_MODAL_HEAD_LOCAL_REAL_CERTIFICATE_PASS')
HEAD_RECEIPT=('CANDIDATE_MODAL_HEAD_LOCAL_CERTIFICATE_V002_RECEIPT.json','e3e185ec5b873b6927517ea0aa2c8694cfc0f228d770f04e38e2634dda16d805','CLOSED')
HEAD_PROOF=('ROOT_NATURAL_CLOSED_MODAL_HEAD_SUCCESS_SEALS_V001.json','903b0f5ed45cc228065d0e93b45e2c24c0a222630eed8151507e694f66c2829a','ROOT_NATURAL_CLOSED_MODAL_HEAD_SUCCESS_SEALS_VERIFIED')
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_modal_head_reconstruction_v002.py':'25953c3a734691047875d656c5c324d108c13a57bf910f78eeb5efbb8473b455',
 'author_fragment_candidate_modal_head_local_certificate_v001.py':'614edfd6fe923b9defc541b41bdf6cda10418dba917fb616ba2e229f33d0f549',
 'author_fragment_candidate_modal_head_factor_apply_v001.py':'deb543e9dea46717b991c84fbb4241e388896231018d9b90f885260739fb6817',
 'author_fragment_candidate_modal_head_apply_measurement_v001.py':'52cefbed87a13a7411d8717100a37aec16605b733deecf5e70e08794cdf21a3a'}
EXTRA_PINS={
 'CANDIDATE_MODAL_HEAD_LOCAL_CERTIFICATE_CONTROLS_V001.md':'ba20b857b41b96961160886cd9de358d947584ebc685661b0fa104fb07117ebc',
 'CANDIDATE_MODAL_HEAD_FACTOR_APPLY_V001.md':'e0e38dc270a6a9d154a61c34d2145c7de48c7ab5e24f75bc1c88147f97f39d0b',
 'CANDIDATE_MODAL_HEAD_APPLY_MEASUREMENT_V001.md':'504f3044a423214a591e98ec06ac4db9195934ae152b34c470d33d46a17828a8'}
SNAMES=('g','hi','U','z','P','w','omega')
CNAMES=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')
CACHE_PREFIX='copied_closed_arm_input_copied_closed_input_NEW_fixed_candidate_cache_'
GAMMA_SQUARED='copied_closed_arm_input_copied_closed_gamma_squared_denominator'
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
 for file,count,selected in ((files[2],11,None),(files[3],6,compact),(files[4],2,None),(files[5],6,None),(files[6],1,{'mh_pair'}),(files[7],3,{'ml_rational','ml_decode','ml_matrix_words'}),(files[8],2,None),(files[9],7,None)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (selected is None or n.name in selected)];assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_exact_exponent_product');globals()['a_prod']=P.a_prod

def hydrate_input(data,refs):
 s={n:data[CACHE_PREFIX+'raw_configuration_'+n] for n in SNAMES};c={n:data[CACHE_PREFIX+'raw_chart_'+n] for n in CNAMES};prefix=CACHE_PREFIX+'copied_positive_coefficient_'
 cache=dict(s=s,c=c,p=4,A=pair(data,CACHE_PREFIX+'anchored_raw_up_dot_zi'),NA=pair(data,CACHE_PREFIX+'paired_N_times_anchored_A'),gamma_squared=pair(data,GAMMA_SQUARED),fixed_E0=pair(data,CACHE_PREFIX+'fixed_lowered_E0'),envelopes={n[len(prefix):]:a for n,a in data.items() if n.startswith(prefix)},constants={n:getattr(P,n) for n in ('ALPHA','ELL','C')},candidate_provenance=[thin(refs['input'])],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
 assert c['ih'].shape==(4,3,3) and s['z'].shape==(32,4,4) and s['U'].shape==(4,4) and s['hi'].shape==(4,4,4) and all(a.shape==(4,) for a in cache['gamma_squared'])
 return cache

def selected_admission():
 assert all(x is not None for record in (HEAD_SOURCE,HEAD_RESULT,HEAD_RECEIPT,HEAD_PROOF) for x in record[:2]),'Naturally closed local factor pins required'
 for name,h in ((DRIVER_PROTOCOL,PROTOCOL_SHA),*PINS.items(),*EXTRA_PINS.items(),HEAD_SOURCE,HEAD_RESULT[:2],HEAD_RECEIPT[:2],HEAD_PROOF[:2]):bind(name,h)
 r=json.loads(P.path(HEAD_RESULT[0]).read_text());rc=json.loads(P.path(HEAD_RECEIPT[0]).read_text());proof=json.loads(P.path(HEAD_PROOF[0]).read_text());stem=HEAD_RESULT[0].removesuffix('_RESULT.json')
 assert r['status']==HEAD_RESULT[2] and rc['status']==HEAD_RECEIPT[2] and rc['result_sha256']==HEAD_RESULT[1] and rc['error_sha256'] is None and r['owner']==rc['owner']==proof['owner'] and r['owner']['pid']==7683 and r['owner']['source_sha256']==HEAD_SOURCE[1]
 assert proof['status']==HEAD_PROOF[2] and proof['source_sha256']==HEAD_SOURCE[1] and proof['result_sha256']==HEAD_RESULT[1] and proof['receipt_sha256']==HEAD_RECEIPT[1] and proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_input_seals_verified'] is True and proof['all_success_role_seals_verified'] is True
 assert proof['parent_numeric_fields_bitwise_identical'] is True and proof['parent_numeric_field_count']==1378 and proof['parent_copy_counts']==dict(input=69,coefficients=23,readout=3,basis0=429,basis1=427,basis2=427)
 assert proof['all_four_local_measured_real_coefficient_Schur_inverses_certified'] is True and proof['nine_NEW_head_actions_only'] is True and proof['old_modal_action_or_certificate_replayed'] is False and proof['uniform_all_input_DD_inverse_qualified'] is False and proof['full_weak_or_global_inverse_qualified'] is False
 assert r['qualification']==rc['qualification']==proof['qualification']==FLAGS and all(x is False for x in FLAGS.values()) and not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 assert len(r['controls'])==139 and proof['controls']==r['controls'] and all(x['ordinal']==i and x['passed'] is True and x['tolerance']==2e-11 for i,x in enumerate(r['controls']))
 case=r['case'];assert case['roles']==13 and case['controls']==139 and case['all_four_local_measured_real_coefficient_Schur_inverses_certified'] is True and case['uniform_all_input_DD_inverse_qualified'] is False and case['full_weak_or_global_inverse_qualified'] is False and case['physical_adoption'] is False
 refs={n:case[n] for n in ('input','reconstruction','head_blocks','local_certificate')};assert len(case['heads'])==9
 for slot,ref in enumerate(case['heads']):refs['head%d'%slot]=ref;assert ref['metadata']['head_coordinate']==slot and ref['metadata']['input']==thin(refs['input']) and ref['metadata']['amplitude_words']==[1.,2.**-60]
 assert [refs['input'],refs['reconstruction']]+case['heads']+[refs['head_blocks'],refs['local_certificate']]==r['checkpoints']
 assert refs['reconstruction']['metadata']['input']==refs['head_blocks']['metadata']['input']==refs['local_certificate']['metadata']['input']==thin(refs['input']) and refs['local_certificate']['metadata']['head_blocks']==thin(refs['head_blocks']) and refs['local_certificate']['metadata']['reconstruction']==thin(refs['reconstruction'])
 assert refs['head_blocks']['metadata']['heads']==[thin(x) for x in case['heads']] and len(refs['input']['metadata']['schema'])==1378
 for ref in refs.values():
  bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);assert json.loads(P.path(ref['commit_file']).read_text())=={n:ref[n] for n in ('file','sha256','metadata')}
  assert ref['metadata']['owner']==r['owner'] and ref['metadata']['failed'] is False and ref['metadata']['qualification']==FLAGS and rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
 selection=dict(input=list(refs['input']['metadata']['schema']),reconstruction=[f'NEW_head_from_closed_modal_Pi_head_from_arm_normalized_{w}' for w in ('hi','lo')],head_blocks=[f'NEW_directed_head_matrix_{n}_normalized_{w}' for n in ('H9','arm_from_head') for w in ('hi','lo')],local_certificate=[f'NEW_local_measured_real_Schur_{n}_{w}' for n in ('S9_all_points_partial','S9_inverse_all_points_partial','measured_D_inverse') for w in ('hi','lo')])
 for slot in range(9):selection['head%d'%slot]=[f'NEW_head{slot}_{n}_{w}' for n in ('physical_native','physical_metric','specialized_NEW_linear_canonical_native_density','specialized_NEW_linear_canonical_metric_total_density') for w in ('hi','lo')]
 for tag,names in selection.items():assert all(refs[tag]['metadata']['schema'][n]['dtype']=='float64' and refs[tag]['metadata']['schema'][n]['finite'] is True for n in names)
 points=refs['local_certificate']['metadata']['rational_descriptions']['NEW_local_measured_real_Schur_completed_local_points'];assert len(points)==4 and all(r['point']==i and r['assembly_cone_resolved'] is True and r['local_real_coefficient_Schur_inverse_certified'] is True and len(r['arms'])==32 for i,r in enumerate(points))
 return dict(refs=refs,selection=selection,closed_provenance=dict(owner=r['owner'],source=dict(file=HEAD_SOURCE[0],sha256=HEAD_SOURCE[1]),result=dict(file=HEAD_RESULT[0],sha256=HEAD_RESULT[1]),receipt=dict(file=HEAD_RECEIPT[0],sha256=HEAD_RECEIPT[1]),proof=dict(file=HEAD_PROOF[0],sha256=HEAD_PROOF[1]),parent_qualification=r['qualification']))

def exact_measured_blocks(refs):
 record=refs['head_blocks']['metadata']['rational_descriptions']['NEW_directed_head_matrix_H9_exact_normalization'];assert record['shape']==[4,9,9] and len(record['entries'])==324;H={tuple(r['index']):ml_decode(r['exact']) for r in record['entries']};assert len(H)==324
 points=refs['local_certificate']['metadata']['rational_descriptions']['NEW_local_measured_real_Schur_completed_local_points'];blocks=[]
 for point,item in enumerate(points):
  arms=[]
  for mode,arm in enumerate(item['arms']):
   assert arm['mode']==mode;arms.append({n:[[ml_decode(x) for x in row] for row in arm[k]] for n,k in (('B','directed_B'),('E','directed_E'),('D','measured_D'))})
  blocks.append(dict(H=[[H[point,i,j] for j in range(9)] for i in range(9)],arms=arms))
 return blocks

def mixed_argument():
 native=P.a_dd(np.zeros((4,99)));metric=P.a_dd(np.zeros((4,6)))
 for point in range(4):
  for slot in range(9):
   target=native if slot<3 else metric;coordinate=slot if slot<3 else slot-3;sign=(-1.)**(point+slot)
   target[0][point,coordinate]=sign*(slot+1)*(1+point/8)/2**(slot%4+2);target[1][point,coordinate]=sign*(point+1)*2.**-60
  for mode in range(32):
   for axis in range(3):native[0][point,3+3*mode+axis]=(-1.)**(point+mode+axis)*(mode+1)*(axis+1)*(1+point/8)/128;native[1][point,3+3*mode+axis]=(-1.)**axis*(mode+1)*2.**-60
 mh_pair('NEW_unequal_mode_mixed_physical_native',native,(4,99),keep);mh_pair('NEW_unequal_mode_mixed_physical_metric',metric,(4,6),keep);return dict(native=native,metric=metric)

def apply_case(name,factors,blocks,rhs,direction,input_record,source):
 CONTEXT.update(stage='NEW_paired_factor_application',case=name,input=thin(input_record),RHS_source=source);start=len(CHECKS)
 for tag,values in (('RHS',rhs),('known_direction',direction)):
  for n,x in values.items():mh_pair(name+'_'+tag+'_'+n,x,(4,99) if n=='native' else (4,6),keep)
 actual=candidate_modal_head_factor_apply(factors,rhs,keep,name+'_apply');measure=measure_modal_head_application(factors,blocks,rhs,actual,direction,keep,describe,P.check,name+'_measurement')
 record=P.checkpoint('APPLICATION',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_paired_signed_local_apply_and_three_full_component_construction_contacts',case=name,input=thin(input_record),RHS_source=source,rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS[start:],source_law_failure_inferred_if_refused=False,**measure));clear_scratch();return record

def packet(admitted):
 refs=admitted['refs'];data={}
 for tag,selected in admitted['selection'].items():
  CONTEXT.update(stage='copy_earned_factor_and_RHS_fields',tag=tag,source=thin(refs[tag]));data[tag]=P.read_pair(refs[tag],selected)
  for n,a in data[tag].items():keep('copied_earned_factor_'+tag+'_'+n,a)
 descriptions=dict(B=refs['reconstruction']['metadata']['rational_descriptions']['NEW_head_from_closed_modal_Pi_head_from_arm_exact_normalization'],H=refs['head_blocks']['metadata']['rational_descriptions']['NEW_directed_head_matrix_H9_exact_normalization'],E=refs['head_blocks']['metadata']['rational_descriptions']['NEW_directed_head_matrix_arm_from_head_exact_normalization'],local_points=refs['local_certificate']['metadata']['rational_descriptions']['NEW_local_measured_real_Schur_completed_local_points'])
 input_record=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='earned_signed_factors_and12_canonical_RHS_probes_copied_without_action',closed_provenance=admitted['closed_provenance'],selected_refs={n:thin(r) for n,r in refs.items()},selected_fields=admitted['selection'],factor_conversion_and_readout_remainders=descriptions,parent_139_controls_are_ancestry_only=True));cache=hydrate_input(data['input'],refs);blocks=exact_measured_blocks(refs)
 factors=dict(B=pair(data['reconstruction'],'NEW_head_from_closed_modal_Pi_head_from_arm_normalized'),E=pair(data['head_blocks'],'NEW_directed_head_matrix_arm_from_head_normalized'),D_inverse=pair(data['local_certificate'],'NEW_local_measured_real_Schur_measured_D_inverse'),S9_inverse=pair(data['local_certificate'],'NEW_local_measured_real_Schur_S9_inverse_all_points_partial'),p=4,closed_provenance=admitted['closed_provenance'],local_real_certificate_admitted=True,uniform_all_input_DD_inverse_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
 clear_scratch();completed=[]
 for slot in range(9):
  d=data['head%d'%slot];prefix='NEW_head%d_'%slot;rhs=dict(native=pair(d,prefix+'specialized_NEW_linear_canonical_native_density'),metric=pair(d,prefix+'specialized_NEW_linear_canonical_metric_total_density'));direction=dict(native=pair(d,prefix+'physical_native'),metric=pair(d,prefix+'physical_metric'))
  completed.append(apply_case('earned_head%d'%slot,factors,blocks,rhs,direction,input_record,thin(refs['head%d'%slot])))
 for axis in range(3):
  d=data['input'];prefix='copied_closed_arm_basis%d_basis%d_NEW_'%(axis,axis);rhs=dict(native=pair(d,prefix+'specialized_NEW_linear_canonical_native_density'),metric=pair(d,prefix+'specialized_NEW_linear_canonical_metric_total_density'));direction=dict(native=pair(d,prefix+'physical_native'),metric=pair(d,prefix+'physical_metric'))
  completed.append(apply_case('earned_simultaneous_modal_axis%d'%axis,factors,blocks,rhs,direction,input_record,dict(input=thin(refs['input']),original_basis_axis=axis,old_action_replayed=False)))
 CONTEXT.update(stage='one_NEW_unequal_mode_mixed147_forward',input=thin(input_record));physical=mixed_argument();forward=candidate_specialized_temporal_action(cache,physical,keep,'NEW_unequal_mode_mixed_specialized')
 forward_record=P.checkpoint('MIXED_FORWARD',arrays({**RAW,**AVAILABLE}),dict(kind='one_NEW_unequal_mode_paired_original147_temporal_direction',input=thin(input_record),formula='head_hi=sign*(slot+1)*(1+point/8)/2**(slot%4+2);head_lo=sign*(point+1)*2**-60;arm_hi=sign*(mode+1)*(axis+1)*(1+point/8)/128;arm_lo=(-1)**axis*(mode+1)*2**-60',physical_direction_and_all147_contacts_retained=True,old_basis_or_action_replayed=False,physical_adoption=False));clear_scratch()
 rhs=dict(native=forward['point']['native'],metric=forward['point']['metric_total']);mixed=apply_case('NEW_unequal_mode_mixed',factors,blocks,rhs,physical,input_record,thin(forward_record));completed.append(mixed)
 CONTEXT.update(stage='completed_application_readout',input=thin(input_record),applications=[thin(r) for r in completed]);keep('new_control_errors',np.asarray([x['error'] for x in CHECKS]));readout=P.checkpoint('READOUT',arrays(AVAILABLE),dict(kind='13_supplied_RHS_local_apply_construction_contacts_only',input=thin(input_record),applications=[thin(r) for r in completed],NEW_mixed_forward=thin(forward_record),controls=CHECKS,original147_action_at_recovered_direction_evaluated=False,these_RHS_only=True,global_preconditioner_or_physical_adoption=False))
 assert len(CHECKS)==39 and len(RECORDS)==16 and all(r['passed'] for r in CHECKS)
 return dict(status='CANDIDATE_LOCAL_MODAL_HEAD_PAIRED_APPLY_13_RHS_CONSTRUCTION_PASS',input=input_record,applications=completed,mixed_forward=forward_record,readout=readout,controls=39,roles=16,earned_RHS_reused_without_action=12,new_mixed_original147_actions=1,global_preconditioner_or_inverse_qualified=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS,'Root release required';assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required'
 initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);admitted=selected_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_provenance=admitted['closed_provenance'],selected_refs={n:thin(r) for n,r in admitted['refs'].items()},earned_RHS_reused_without_action=12,one_NEW_mixed_original147_action=True,controls=39,roles=16,source_law_failure_inferred_if_refused=False,physical_adoption=False));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=packet(admitted)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   data={**RAW,**AVAILABLE,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if data:
    try:P.checkpoint('ERROR_RAW',arrays(data),dict(kind='completed_NEW_apply_forward_and_exact_reference_partials',context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS)),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,source_law_failure_inferred=False,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
