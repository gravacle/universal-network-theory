"""HELD root-only directed local modal/head coefficient experiment.
Copy the earned CLOSED6552 arm cache, three Pi sets and measured D metadata.
Only nine NEW head temporal applications and local real certificates are new.
No candidate, arm producer/certificate, old action, fixture or weak solve replay.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,itertools,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_MODAL_HEAD_LOCAL_CERTIFICATE_V002'
DRIVER_PROTOCOL='CANDIDATE_MODAL_HEAD_LOCAL_CERTIFICATE_CONTROLS_V001.md'
PROTOCOL_SHA='ba20b857b41b96961160886cd9de358d947584ebc685661b0fa104fb07117ebc'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_modal_head_reconstruction_v002.py':'25953c3a734691047875d656c5c324d108c13a57bf910f78eeb5efbb8473b455',
 'author_fragment_candidate_modal_head_local_certificate_v001.py':'614edfd6fe923b9defc541b41bdf6cda10418dba917fb616ba2e229f33d0f549'}
EXTRA_PINS={
 'CANDIDATE_MODAL_HEAD_RECONSTRUCTION_V002.md':'c3ebf7ba1cdc02e761bc520300958f774872bd052a6b0ae57c8d4afbc8f57d68',
 'CANDIDATE_MODAL_HEAD_LOCAL_CERTIFICATE_V001.md':'eeeb6892f36505d63d8d2e87eebc6de54b64571abfd3d9ec2656834fc377e5bd',
 'cross_u_candidate_modal_arm_certificate_recovery_v002.py':'7f21ccab616b1788e5b4b3c674783639ca33fcdf23733b8f2cfa828c32e2dc1a',
 'CANDIDATE_MODAL_ARM_CERTIFICATE_RECOVERY_V001.md':'c854cfd3995129d6017d75239571c031262c04231f9bdc1cd24e0b2ed3ce616c'}
PARENT_STEM='CANDIDATE_MODAL_ARM_CERTIFICATE_RECOVERY_V002'
PARENT_RESULT_SHA='64232331af9dec8d3a1b7e7cb1714e26a41e5e96c52813d93dec43192486868f'
PARENT_RECEIPT_SHA='9a425a54a8fb981c7a3c4bf198650825752e59defd4ffaffe7fc4099009db375'
PARENT_CLOSURE='ROOT_NATURAL_CLOSED_MODAL_ARM_RECOVERY_SUCCESS_SEALS_V001.json'
PARENT_CLOSURE_SHA='44ddd9a8779fc1e5199df2f3047c6ae4a273c6669696f0d217f02f5c7f49892e'
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
 for file,count,selected in ((files[2],11,None),(files[3],6,compact),(files[4],2,None),(files[5],6,None),(files[6],6,None),(files[7],12,None)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (selected is None or n.name in selected)];assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_exact_exponent_product');globals()['a_prod']=P.a_prod

def hydrate_input(data,refs):
 s={n:data[CACHE_PREFIX+'raw_configuration_'+n] for n in SNAMES};c={n:data[CACHE_PREFIX+'raw_chart_'+n] for n in CNAMES};prefix=CACHE_PREFIX+'copied_positive_coefficient_'
 cache=dict(s=s,c=c,p=4,A=pair(data,CACHE_PREFIX+'anchored_raw_up_dot_zi'),NA=pair(data,CACHE_PREFIX+'paired_N_times_anchored_A'),gamma_squared=pair(data,GAMMA_SQUARED),fixed_E0=pair(data,CACHE_PREFIX+'fixed_lowered_E0'),envelopes={n[len(prefix):]:a for n,a in data.items() if n.startswith(prefix)},constants={n:getattr(P,n) for n in ('ALPHA','ELL','C')},candidate_provenance=[thin(refs['input'])],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
 assert c['ih'].shape==(4,3,3) and s['z'].shape==(32,4,4) and s['U'].shape==(4,4) and s['hi'].shape==(4,4,4) and all(a.shape==(4,) for a in cache['gamma_squared'])
 return cache

def selected_admission():
 for name,h in ((DRIVER_PROTOCOL,PROTOCOL_SHA),*PINS.items(),*EXTRA_PINS.items(),(PARENT_STEM+'_RESULT.json',PARENT_RESULT_SHA),(PARENT_STEM+'_RECEIPT.json',PARENT_RECEIPT_SHA),(PARENT_CLOSURE,PARENT_CLOSURE_SHA)):bind(name,h)
 r=json.loads(P.path(PARENT_STEM+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT_STEM+'_RECEIPT.json').read_text());proof=json.loads(P.path(PARENT_CLOSURE).read_text())
 assert r['status']=='CANDIDATE_FOUR_POINT_MODAL_ARM_RECOVERY_CERTIFICATE_PASS' and rc['status']=='CLOSED' and rc['result_sha256']==PARENT_RESULT_SHA and rc['error_sha256'] is None
 assert r['owner']==rc['owner']==proof['owner'] and r['owner']['pid']==6552 and r['owner']['source_sha256']==EXTRA_PINS['cross_u_candidate_modal_arm_certificate_recovery_v002.py']
 assert r['qualification']==rc['qualification']==proof['qualification']==FLAGS and all(x is False for x in FLAGS.values())
 assert proof['status']=='ROOT_NATURAL_CLOSED_MODAL_ARM_RECOVERY_SUCCESS_SEALS_VERIFIED' and proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_input_seals_verified'] is True and proof['all_success_role_seals_verified'] is True
 assert proof['source_sha256']==r['owner']['source_sha256'] and proof['result_sha256']==PARENT_RESULT_SHA and proof['receipt_sha256']==PARENT_RECEIPT_SHA and proof['controls']==r['controls'] and proof['role_count']==6
 assert proof['earned_axes_order']==[0,1,2] and proof['only_new_axes']==[1,2] and proof['inherited_numeric_fields_bitwise_identical'] is True and proof['original_failed_metadata_and_missing_RESULT_preserved'] is True and proof['coefficient_certificate_or_axis0_action_replayed'] is False
 assert not P.path(PARENT_STEM+'_ERROR.json').exists() and not P.path(PARENT_STEM+'_ERROR_RECEIPT.json').exists()
 controls=r['controls'];assert len(controls)==4 and all(x['ordinal']==i and x['passed'] is True and x['tolerance']==2e-11 for i,x in enumerate(controls))
 case=r['case'];assert case['roles']==6 and case['controls']==4 and case['inherited_controls']==2 and case['new_basis_coordinates']==[1,2] and case['original_failed_status_preserved']=='CLOSED_ERROR' and case['uniform_all_input_DD_or_global_inverse_earned'] is False and case['physical_adoption'] is False
 refs=dict(input=case['input'],coefficients=case['coefficients'],readout=case['readout'],controls=controls,closed_provenance=dict(owner=r['owner'],result=dict(file=PARENT_STEM+'_RESULT.json',sha256=PARENT_RESULT_SHA),receipt=dict(file=PARENT_STEM+'_RECEIPT.json',sha256=PARENT_RECEIPT_SHA),proof=dict(file=PARENT_CLOSURE,sha256=PARENT_CLOSURE_SHA),original_failed_status_preserved=case['original_failed_status_preserved']))
 assert len(case['basis'])==3
 for axis,ref in enumerate(case['basis']):refs['basis%d'%axis]=ref;assert ref['metadata']['coordinate']==axis and ref['metadata']['input']==thin(refs['input']) and ref['metadata']['coefficients']==thin(refs['coefficients'])
 assert case['basis'][0]['metadata']['inherited_source_failed'] is True and case['basis'][0]['metadata']['original_error_and_missing_RESULT_preserved'] is True
 ordered=[refs['input'],refs['coefficients']]+case['basis']+[refs['readout']];assert ordered==r['checkpoints'] and refs['readout']['metadata']['basis']==[thin(x) for x in case['basis']]
 assert refs['readout']['metadata']['input']==thin(refs['input']) and refs['readout']['metadata']['coefficients']==thin(refs['coefficients'])
 for ref,count in zip(ordered,(69,23,429,427,427,3)):
  bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);assert json.loads(P.path(ref['commit_file']).read_text())=={n:ref[n] for n in ('file','sha256','metadata')}
  assert ref['metadata']['owner']==r['owner'] and ref['metadata']['failed'] is False and ref['metadata']['qualification']==FLAGS and len(ref['metadata']['schema'])==count
  assert rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
  assert all(x['dtype']=='float64' and x['finite'] is True for x in ref['metadata']['schema'].values())
 for axis in range(3):
  schema=refs['basis%d'%axis]['metadata']['schema'];prefix='basis%d_NEW_specialized_NEW_linear_canonical_'%axis
  for name,shape in (('Pi',[32,4,4,4]),('native_density',[4,99]),('metric_total_density',[4,6])):
   for word in ('hi','lo'):assert schema[prefix+name+'_'+word]['shape']==shape
 return refs

def head_argument(slot):
 native=P.a_dd(np.zeros((4,99)));metric=P.a_dd(np.zeros((4,6)));target=native if slot<3 else metric;coordinate=slot if slot<3 else slot-3
 target[0][:,coordinate]=1.;target[1][:,coordinate]=2.**-60;mh_pair('NEW_head%d_physical_native'%slot,native,(4,99),keep);mh_pair('NEW_head%d_physical_metric'%slot,metric,(4,6),keep)
 return dict(native=native,metric=metric)

def packet(refs):
 CHECKS.extend([dict(x) for x in refs['controls']]);datasets={}
 for tag in ('input','coefficients','basis0','basis1','basis2','readout'):
  ref=refs[tag];CONTEXT.update(stage='bitcopy_closed_arm_roles',current_role=tag,source=thin(ref),completed_roles=list(datasets))
  datasets[tag]=P.read_pair(ref,list(ref['metadata']['schema']))
  for n,a in datasets[tag].items():keep('copied_closed_arm_'+tag+'_'+n,a)
 input_record=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='earned_modal_arm_cache_Pi_and_coefficients_copied_once',closed_refs={n:thin(refs[n]) for n in datasets},closed_provenance=refs['closed_provenance'],inherited_controls=refs['controls'],all_parent_fields_bitcopied=True,no_original_arm_action_or_certificate_replayed=True));cache=hydrate_input(datasets['input'],refs);columns=[]
 for axis in range(3):
  data=datasets['basis%d'%axis];prefix='basis%d_NEW_specialized_NEW_linear_canonical_'%axis
  columns.append(dict(Pi=pair(data,prefix+'Pi'),native=pair(data,prefix+'native_density'),metric_total=pair(data,prefix+'metric_total_density'),physical_native=pair(data,'basis%d_NEW_physical_native'%axis),physical_metric=pair(data,'basis%d_NEW_physical_metric'%axis),amplitude_words=(1.,2.**-60),closed_provenance=dict(ref=thin(refs['basis%d'%axis]),terminal=refs['closed_provenance'])))
 clear_scratch();CONTEXT.update(stage='NEW_per_mode_head_reconstruction',input=thin(input_record));reconstructed=reconstruct_modal_head_blocks(cache,columns,keep,describe,P.check,'NEW_head_from_closed_modal_Pi')
 reconstruction_record=P.checkpoint('RECONSTRUCTION',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_directed_head_from_closed_Pi_with_original_simultaneous_association_contacts',input=thin(input_record),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS[4:],uniform_DD_operator_or_global_inverse_qualified=False,physical_adoption=False));clear_scratch();heads=[];head_records=[]
 for slot in range(9):
  CONTEXT.update(stage='NEW_head_temporal_column',slot=slot,input=thin(input_record),reconstruction=thin(reconstruction_record),completed=[thin(r) for r in head_records]);physical=head_argument(slot);result=candidate_specialized_temporal_action(cache,physical,keep,'NEW_head%d_specialized'%slot)
  record=P.checkpoint('HEAD_COLUMN',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_U3_or_physical_metric6_temporal_basis_column',head_coordinate=slot,amplitude_words=[1.,2.**-60],input=thin(input_record),fixed_configuration=True,no_extra_metric_multiplicity=True,physical_adoption=False));head_records.append(record)
  heads.append(dict(native=result['point']['native'],metric_total=result['point']['metric_total'],physical_native=physical['native'],physical_metric=physical['metric'],amplitude_words=(1.,2.**-60),head_coordinate=slot,new_provenance=dict(record=thin(record),source_sha256=SCOPE['OWNER']['source_sha256'])));clear_scratch()
 CONTEXT.update(stage='NEW_directed_H_E_extraction',input=thin(input_record),heads=[thin(r) for r in head_records]);head=collect_directed_head_blocks(cache,heads,keep,describe,'NEW_directed_head_matrix')
 head_record=P.checkpoint('HEAD_BLOCKS',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_signed_directed_H9_and_arm_from_head_E_without_transpose_replacement',input=thin(input_record),heads=[thin(r) for r in head_records],rational_descriptions=dict(DESCRIPTIONS),uniform_DD_operator_or_global_inverse_qualified=False,physical_adoption=False));clear_scratch()
 arm=dict(closed_provenance=refs['closed_provenance'],coefficient_points=refs['coefficients']['metadata']['rational_descriptions']['NEW_modal_arm_completed_rational_points'],measured_matrix_records=refs['readout']['metadata']['rational_descriptions']['NEW_measured_modal_matrix_completed_measured_matrix_bounds'],measured_admission={n:refs['readout']['metadata'][n] for n in ('measured_three_basis_real_coefficient_matrices_invertible','same_three_input_amplitudes_only','uniform_all_input_DD_error_or_global_inverse_earned','physical_adoption')})
 CONTEXT.update(stage='NEW_local_measured_real_Schur_certificate',input=thin(input_record),reconstruction=thin(reconstruction_record),head_blocks=thin(head_record));local=candidate_modal_head_local_real_certificate(reconstructed,head,arm,keep,describe,P.check,'NEW_local_measured_real_Schur')
 keep('control_errors',np.asarray([x['error'] for x in CHECKS]));local_record=P.checkpoint('LOCAL_CERTIFICATE',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_four_signed_local_measured_real_Schur_coefficients_only',input=thin(input_record),reconstruction=thin(reconstruction_record),head_blocks=thin(head_record),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS[7:],all_four_local_measured_real_coefficient_Schur_inverses_certified=local['all_four_local_measured_real_coefficient_Schur_inverses_certified'],uniform_all_input_DD_inverse_qualified=False,full_weak_or_global_inverse_qualified=False,physical_rank_or_adoption=False))
 assert len(CHECKS)==139 and len(RECORDS)==13 and all(x['passed'] for x in CHECKS)
 return dict(status='CANDIDATE_FOUR_POINT_DIRECTED_MODAL_HEAD_LOCAL_REAL_CERTIFICATE_PASS',input=input_record,reconstruction=reconstruction_record,heads=head_records,head_blocks=head_record,local_certificate=local_record,controls=139,inherited_controls=4,new_controls=135,roles=13,closed_arm_provenance=refs['closed_provenance'],all_four_local_measured_real_coefficient_Schur_inverses_certified=True,uniform_all_input_DD_inverse_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS,'Root release required';assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required'
 initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);refs=selected_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_refs={n:thin(refs[n]) for n in ('input','coefficients','basis0','basis1','basis2','readout')},closed_provenance=refs['closed_provenance'],new_head_actions=9,inherited_controls=4,new_controls=135,controls=139,roles=13,no_old_producer_action_or_certificate_replay=True,physical_adoption=False));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   data={**RAW,**AVAILABLE,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if data:
    try:P.checkpoint('ERROR_RAW',arrays(data),dict(kind='completed_closed_inputs_and_NEW_head_local_certificate_partials',context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS)),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),rational_descriptions=dict(DESCRIPTIONS),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
