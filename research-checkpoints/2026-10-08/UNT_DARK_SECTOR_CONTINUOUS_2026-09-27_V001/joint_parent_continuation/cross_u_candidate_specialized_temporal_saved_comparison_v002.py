"""HELD root-only NEW specialization versus eight CLOSED temporal targets.
Read only selected sealed raw constants/arguments/targets/envelopes. No general
160/225/action, old mixed/metric contact, scatter or fixture body is invoked.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_SPECIALIZED_TEMPORAL_SAVED_COMPARISON_V002'
DRIVER_PROTOCOL='CANDIDATE_SPECIALIZED_TEMPORAL_SAVED_COMPARISON_V001.md'
PROTOCOL_SHA='bc71afc552642c9da8b7d3206c5ef34dd7e413577f73f4136c32b1a5d1de9546'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc'}
PARENTS=(
 ('CLOSED_CANDIDATE_SECTION_TEMPORAL_CONTROLS_V002','4b8f747f460b3c636535f899d073a4c47b450deef880fbc057d67e3424eb13d1','bf5eb61faf3514575f470b1cc34e5b4c0e071ba4f8768daacb4ab0634c7a522d','1e434be6a95581ab72a30aa3815302b8667032b8a7595e92c6692e3429d7f1ef',1551,8,'actions'),
 ('CLOSED_CANDIDATE_LOCAL_METRIC_BLOCK_CONTROLS_V002','013e5f6ddd1cee47f6bc69d714efd0d1ae2cf1ffa80e1df1b0e89b21717c27b7','49cca20953ac0366f232d6274969c11c0ea71c18bdd7f76fa924a7507931aa7e','fb027c02d0fcda8858d1395f6f18ace98f442185309b766232dfd758b562ec53',2952,18,'columns'))
SNAMES=('g','hi','U','z','P','w','omega')
CNAMES=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')
POINT_FAMILIES=('native','metric_native','metric_EH','metric_total')
np=P=None;SCOPE={};RAW={};AVAILABLE={};DD_ARRAY_CURRENT={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={}
FLAGS=dict(whole_grid_action_qualified=False,mechanical_inverse_earned=False,global_rank_earned=False,Hessian_symmetry_earned=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,physical_adoption=False)

def bind(name,checksum):
 assert checksum is not None and P.sha(P.path(name))==checksum,name
 key=str(P.path(name).resolve());assert key not in INPUTS or INPUTS[key]==checksum;INPUTS[key]=checksum
def keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name;return a
def arrays(values):return {n:np.asarray(a).copy() for n,a in values.items()}
def thin(ref):return {n:ref[n] for n in ('file','sha256','commit_file','commit_sha256')}
def clear_scratch():RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear();CONTEXT.clear()
def pair(data,prefix):return data[prefix+'_hi'],data[prefix+'_lo']
def action_prefix(prefix):return prefix+('_NEW_action' if prefix.startswith('column') else '_action')
def comparison_fields(prefix):
 ap=action_prefix(prefix);groups=[prefix+'_supplied_physical_'+n for n in ('native','metric')]+[ap+'_NEW_point_'+n for n in POINT_FAMILIES]
 groups+=[ap+'_NEW160_temporal_completed_configuration_'+n for n in ('du','dz','dg','Ga')]
 groups+=[ap+'_formal_minus_canonical_primary_'+n+'_time' for n in ('U','z')]
 groups+=[ap+'_NEW160_temporal_'+n for n in ('KGamma_minus_KADM_delta','Ktrace_Gamma_minus_ADM_delta','inverse_first_delta','up_first_delta','gamma_first_delta')]
 return [g+'_'+w for g in groups for w in ('hi','lo')]+[prefix+'_positive_uncancelled_'+n for n in ('native','metric_native','metric_EH','metric')]

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
 for file,count,selected in ((files[2],11,None),(files[3],6,compact),(files[4],2,None),(files[5],6,None)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (selected is None or n.name in selected)];assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_exact_exponent_product');globals()['a_prod']=P.a_prod

def selected_admission():
 for name,h in ((DRIVER_PROTOCOL,PROTOCOL_SHA),*PINS.items()):bind(name,h)
 cases=[];inputs=[]
 for stem,rh,rch,source,pid,count,role in PARENTS:
  bind(stem+'_RESULT.json',rh);bind(stem+'_RECEIPT.json',rch);r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text())
  assert rc['status']=='CLOSED' and rc['result_sha256']==rh and rc['error_sha256'] is None and r['owner']==rc['owner'] and r['owner']['pid']==pid and r['owner']['source_sha256']==source
  assert len(r['controls'])==count and all(x['passed'] for x in r['controls']) and r['qualification']==rc['qualification'] and all(x is False for x in r['qualification'].values())
  input_ref=r['case']['input'];columns=r['case'][role];assert len(columns)==(2 if role=='actions' else 6)
  for ref in (input_ref,*columns):
   bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);assert json.loads(P.path(ref['commit_file']).read_text())=={n:ref[n] for n in ('file','sha256','metadata')}
   assert ref['metadata']['owner']==r['owner'] and ref['metadata']['failed'] is False and rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256']
  inputs.append(input_ref)
  for ordinal,ref in enumerate(columns):
   prefix=('argument%d'%ordinal) if role=='actions' else ('column%d'%ordinal)
   for n in comparison_fields(prefix):assert ref['metadata']['schema'][n]['dtype']=='float64' and ref['metadata']['schema'][n]['finite'] is True,n
   cases.append(dict(ref=ref,prefix=prefix,parent_status=r['status'],parent_qualification=r['qualification'],ordinal=len(cases)))
 return inputs,cases

def compare_group(label,actual,expected,bound):
 ft_keep(label+'_NEW',actual,keep);ft_keep(label+'_saved_expected',expected,keep);gap=ft_keep(label+'_difference',P.a_sub(actual,expected),keep);keep(label+'_uncancelled_envelope',bound)
 assert np.shape(bound)==actual[0].shape==expected[0].shape and np.all(bound>=0)
 P.check(label+'_same_declared_temporal_map',gap[0]+gap[1],np.zeros_like(gap[0]),bound)

def packet(input_refs,cases):
 names=['copied_completed_point_candidate_s_'+n for n in SNAMES]+['copied_completed_point_candidate_c_'+n for n in CNAMES]
 eprefix='copied_completed_point_candidate_coefficient_envelopes_';names+=[n for n in input_refs[0]['metadata']['schema'] if n.startswith(eprefix)]
 names+=['copied_completed_point_inputs_reference_E0_'+w for w in ('hi','lo')]
 for ref in input_refs:
  for n in names:assert ref['metadata']['schema'][n]==input_refs[0]['metadata']['schema'][n],n
 first=P.read_pair(input_refs[0],names);second=P.read_pair(input_refs[1],names)
 assert all(np.array_equal(first[n],second[n]) for n in names),'The saved contacts do not own the same raw candidate'
 candidate=dict(s={n:first['copied_completed_point_candidate_s_'+n] for n in SNAMES},c={n:first['copied_completed_point_candidate_c_'+n] for n in CNAMES},coefficient_envelopes={n[len(eprefix):]:first[n] for n in names if n.startswith(eprefix)},candidate_provenance=[thin(r) for r in input_refs])
 reference=dict(E0=pair(first,'copied_completed_point_inputs_reference_E0'))
 cache=candidate_temporal_prepare(candidate,reference,keep,'NEW_fixed_candidate_cache');del first,second
 input_record=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='NEW_specialized_temporal_cache_from_two_identical_CLOSED_candidate_inputs',parents=[thin(r) for r in input_refs],candidate_action_or_current_primal_replayed=False,other_sections_fabricated=False,physical_adoption=False));clear_scratch();completed=[]
 for item in cases:
  ordinal,prefix,ref=item['ordinal'],item['prefix'],item['ref'];ap=action_prefix(prefix);CONTEXT.update(case=ordinal,stage='NEW_specialized_temporal_comparison',input=thin(input_record),target=thin(ref),completed=[thin(r) for r in completed])
  data=P.read_pair(ref,comparison_fields(prefix));physical={n:pair(data,prefix+'_supplied_physical_'+n) for n in ('native','metric')}
  jet_bounds=candidate_temporal_jet_envelopes(cache,physical,keep,'case%d_NEW_uncancelled'%ordinal)
  result=candidate_specialized_temporal_action(cache,physical,keep,'case%d_NEW_specialized'%ordinal);jets=result['jets'];native=cache['p'];assert native==4
  for n in POINT_FAMILIES:
   envelope=data[prefix+'_positive_uncancelled_'+('metric' if n=='metric_total' else n)]
   compare_group('case%d_%s'%(ordinal,n),result['point'][n],pair(data,ap+'_NEW_point_'+n),2*envelope)
  for n in ('du','dz','dg','Ga'):compare_group('case%d_%s'%(ordinal,n),jets[n],pair(data,ap+'_NEW160_temporal_completed_configuration_'+n),2*jet_bounds[n])
  for n,key,bound in (('formal_inverse_time','inverse_first_delta','formal_inverse_time'),('formal_up_time','up_first_delta','formal_up_time'),('gamma_time','gamma_first_delta','gamma_time')):
   saved=pair(data,ap+'_NEW160_temporal_'+key);expected=tuple(a[:,0] for a in saved)
   compare_group('case%d_%s'%(ordinal,n),jets[n],expected,2*jet_bounds[bound])
  for n,key,shape in (('U','primary_U',(4,4)),('z','primary_z',(32,4,4))):
   actual=pair(AVAILABLE,'case%d_NEW_specialized_NEW_linear_jets_formal_minus_canonical_primary_%s_time'% (ordinal,n));assert actual[0].shape==shape
   compare_group('case%d_primary_%s'%(ordinal,n),actual,pair(data,ap+'_formal_minus_canonical_primary_'+n+'_time'),2*jet_bounds[key])
  for n in ('KGamma_minus_KADM','Ktrace_Gamma_minus_ADM'):
   actual=pair(AVAILABLE,'case%d_NEW_specialized_NEW_linear_canonical_%s_direction'%(ordinal,n))
   compare_group('case%d_%s'%(ordinal,n),actual,pair(data,ap+'_NEW160_temporal_'+n+'_delta'),2*jet_bounds[n])
  completed.append(P.checkpoint('COMPARISON',arrays({**AVAILABLE,**RAW}),dict(kind='NEW_specialization_against_earned_temporal_words',case=ordinal,target=thin(ref),input=thin(input_record),parent_status_preserved=item['parent_status'],parent_qualification_preserved=item['parent_qualification'],controls=CHECKS[-15:],configuration_held=True,general160_or_old_action_replayed=False,physical_adoption=False)));clear_scratch()
 readout=P.checkpoint('READOUT',dict(control_errors=np.asarray([x['error'] for x in CHECKS]),control_count=np.asarray(len(CHECKS))),dict(kind='eight_saved_temporal_targets_NEW_implementation_comparison',comparisons=[thin(r) for r in completed],controls=CHECKS,finite_action_or_global_rank_qualification=False,physical_adoption=False))
 assert len(CHECKS)==120 and len(RECORDS)==10 and all(x['passed'] for x in CHECKS)
 return dict(status='CANDIDATE_SPECIALIZED_TEMPORAL_EIGHT_SAVED_COMPARISONS_PASS',input=input_record,comparisons=completed,readout=readout,saved_targets=8,controls=120,old_numerical_contact_or_fixture_replayed=False,whole_grid_action_or_inverse_qualified=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS,'Root release required';assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required'
 initialize_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);input_refs,cases=selected_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,parent_inputs=[thin(r) for r in input_refs],targets=[thin(x['ref']) for x in cases],new_comparisons=8,controls=120,roles=10,live_recovery_accessed=False,physical_adoption=False));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):result=packet(input_refs,cases)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=result['status'],case=result,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(result['status'],len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   data={**AVAILABLE,**RAW,**{'last_DD_'+n:x for n,x in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
   if data:
    try:P.checkpoint('ERROR_RAW',arrays(data),dict(kind='available_NEW_specialized_temporal_operands',context=dict(CONTEXT)),failed=True)
    except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
