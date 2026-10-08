"""HELD saved-column collector recovery; root alone releases and executes.
Reuse earned65759 TOTAL-rate columns and completed current words. Only the
unstarted original normal/CMC collector runs, with its original test mask.
Original success/failure files and owners remain unchanged.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,traceback,types
BASE=Path(__file__).resolve().parent
STEM='SAVED_FIXED_GEOMETRY_TOTAL_RATE_COLUMN_READOUT_RECOVERY_V002'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
DRIVER_PROTOCOL='SAVED_FIXED_GEOMETRY_TOTAL_RATE_COLUMN_READOUT_RECOVERY_V001.md'
PROTOCOL_SHA='71423168c9d0264f311bfb56b5bf17167e7bc94812c9764395dd63040aa2199e'
PARENT_SOURCE=('cross_u_fixed_geometry_total_rate_state_evaluation_v004.py','59f23b9476d38aadc8297c104d4cf8e5ab217ac1ce3a0bc077e34f2fec99b39f')
PARENT_ERROR=('CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V004_ERROR.json', '183070c4620623ee5f82f93f8c65de2a73815c0c60bcaeead64ea6fcecb09fea')
PARENT_RECEIPT=('CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V004_RECEIPT.json', 'fa2972d289c42d29be375c1d42e3533ec0d40ddd67724adebf0a1e3d4928487d', 'CLOSED_ERROR')
PARENT_FAILURE_PROOF=('READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_V001.json', '7b70a0936d9ca72ee38fab4a25cd543918c656829750443e50ace9251f875b17', 'READONLY_NATURAL_CLOSED_TOTAL_RATE_COLLECTOR_FAILURE_SEALS_VERIFIED')
PARENT_STEM='CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V004'
TRACEBACK_SHA='238de507d083034f0e2cf5a3586df7407b1befa6407cd5ae3574258775703643'
STATUS='FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED'
PRIMITIVE_SOURCE='cross_u_paired_current_primitive_momentum_readout_v002.py'
ARITHMETIC_SOURCE='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
NORMAL_SOURCE='cross_u_paired_current_normal_constraints_v002.py'
FY_SOURCE='author_fragment_finite_york_geometry_target_v001.py'
FN_SOURCE='author_fragment_finite_candidate_native_EH_normal_v003.py'
EXACT_SOURCE='author_fragment_exact_exponent_two_product_v003.py'
RECHECK_SOURCE='author_fragment_single_decode_recheck_v001.py'
PINS={
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_candidate_native_EH_normal_v003.py':'5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'author_fragment_fixed_geometry_total_rate_state_v002.py':'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d'}
FLAGS={'physical_adoption':False,'uniform_DD_or_global_inverse_qualified':False,'fresh_current_six_or_normal_CMC_admitted':False,'changed_spatial_geometry':False,'stationarity_feedback_or_new43_earned':False}
np=P=N=None;SCOPE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];RAW={};AVAILABLE={};CONTEXT={};DD_ARRAY_CURRENT={}

def definitions(file,names,scope):
 data=(BASE/file).read_bytes();assert hashlib.sha256(data).hexdigest()==PINS[file],file
 tree=ast.parse(data);items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in items}==set(names),file
 exec(compile(ast.Module(body=items,type_ignores=[]),file,'exec'),scope)

def bind(name,digest):
 assert isinstance(name,str) and name and isinstance(digest,str) and len(digest)==64
 key=str(P.path(name).resolve());assert key not in INPUTS or INPUTS[key]==digest
 assert P.sha(P.path(name))==digest,name;INPUTS[key]=digest

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def keep(name,value):
 a=np.asarray(value);RAW[name]=a.copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name
 AVAILABLE[name]=a.copy();return a

def clear_current():RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear()

def initialize():
 global np,P,N,SCOPE
 io={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual'}
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 definitions(PRIMITIVE_SOURCE,io,SCOPE);P=types.SimpleNamespace(**{n:SCOPE[n] for n in io})
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 arithmetic={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_slice','a_reshape','scalar_mask','scalar_lift','scalar_scatter','dd_scalar_scatter'}
 definitions(ARITHMETIC_SOURCE,arithmetic,SCOPE);definitions(PRIMITIVE_SOURCE,{'normal_keep_pair'},SCOPE)
 for n in arithmetic:setattr(P,n,SCOPE[n])
 normal={'normal_test_mask','extend_normal_tests','restrict_normal_rows','normal_hat_jet','normal_hat_operation_envelope','scatter_normal_envelope','paired_restrict_normal_rows','paired_scatter_normal'}
 definitions(NORMAL_SOURCE,normal,SCOPE);N=types.SimpleNamespace(**{n:SCOPE[n] for n in normal})
 definitions(FY_SOURCE,{'fy_keep','fy_sum'},globals())
 definitions(FN_SOURCE,{'fn_abs','finite_candidate_test_polynomials','finite_candidate_global_normal_CMC'},globals())
 definitions(EXACT_SOURCE,{'exact_exponent_two_product','install_exact_exponent_product'},globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_fixed_rate_shared_exact_product')
 definitions(RECHECK_SOURCE,{'recheck'},SCOPE);P.recheck=SCOPE['recheck']

def json_bound(q):
 bind(q[0],q[1]);p=P.path(q[0]);assert p.stat().st_size<=128*1024*1024,'Bounded original failure metadata required'
 value=json.loads(p.read_text());assert len(q)==2 or value['status']==q[2];return value

def admit_saved():
 bind(*PARENT_SOURCE);e=json_bound(PARENT_ERROR);rc=json_bound(PARENT_RECEIPT);proof=json_bound(PARENT_FAILURE_PROOF)
 owner=e['owner'];assert owner==rc['owner']==proof['owner'] and owner['owner']=='root' and owner['pid']==65759 and owner['source_sha256']==PARENT_SOURCE[1]
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==PARENT_ERROR[1] and rc['prior_receipt_sha256'] is None
 assert proof['source_sha256']==PARENT_SOURCE[1] and proof['error_sha256']==PARENT_ERROR[1] and proof['receipt_sha256']==PARENT_RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==1
 for name in ('all_input_seals_verified','all_output_seals_verified','all_success_role_seals_verified','all_failed_raw_seals_verified'):assert proof[name] is True,name
 assert proof['success_roles']==90 and proof['failed_raw_roles']==1 and proof['original_controls_passed']==0 and proof['controls']==[]
 assert e['controls']==[] and e['raw_preservation_traceback'] is e['closing_traceback'] is None
 assert hashlib.sha256(e['traceback'].encode()).hexdigest()==TRACEBACK_SHA==proof['source_traceback_sha256']
 assert e['qualification']==rc['qualification']==proof['qualification']==FLAGS and e['input_sha256']==rc['input_sha256']
 assert len(rc['input_sha256'])==77 and len(rc['output_sha256'])==185 and not P.path(PARENT_STEM+'_RESULT.json').exists()
 expected=['INPUT','RATE_INCREMENT']+(['BASELINE_COLUMN_INPUT','RATE_STATE_INPUT','RATE_STATE_FIRST_JETS','RATE_STATE_FEATURES','RATE_STATE_MOMENTA']+['RATE_STATE_NORMAL_TEST']*16+['RATE_STATE_COLUMN'])*4+['ERROR_RAW']
 records=e['checkpoints'];assert len(records)==len(proof['records'])==len(expected)==91
 for i,(q,pr,role) in enumerate(zip(records,proof['records'],expected)):
  assert q['file']==PARENT_STEM+'_%05d_'%i+role+'.npz' and thin(q)==thin(pr) and pr['ordinal']==i and pr['role']==role
  assert pr['owner_equal'] is pr['embedded_metadata_equal'] is pr['member_names_headers_and_structural_lengths_equal'] is pr['qualification_all_false'] is True
  assert pr['failed'] is (i==90);md=q['metadata'];assert md['owner']==owner and md['qualification']==FLAGS and md['failed'] is (i==90)
  for name,digest in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][name]==digest
  bind(q['commit_file'],q['commit_sha256']);assert json.loads(P.path(q['commit_file']).read_text())=={k:q[k] for k in ('file','sha256','metadata')}
  if i<90:assert md['kind']==role and md['physical_adoption'] is False
 columns=[records[23+22*iq] for iq in range(4)];header=records[0];raw=records[90];provenance=header['metadata']['provenance']
 assert proof['input']==thin(header) and proof['columns']==[thin(q) for q in columns] and proof['error_raw']==thin(raw)
 assert raw['metadata']['kind']=='incomplete_TOTAL_rate_value_state' and raw['metadata']['context']==e['context'] and len(raw['metadata']['schema'])==12
 assert provenance['physical_adoption'] is False and provenance['correction_original_six_gates_admitted'] is True
 for iq,q in enumerate(columns):assert q['metadata']['column']==iq and q['metadata']['provenance']==provenance['columns'][iq]
 failure=dict(source=PARENT_SOURCE,error=PARENT_ERROR,receipt=PARENT_RECEIPT,root_proof=PARENT_FAILURE_PROOF,owner=owner,status='CLOSED_ERROR',original_RESULT_absent=True,failed_raw=thin(raw),original_controls=0,original_failure_preserved=True)
 return dict(error=e,receipt=rc,proof=proof,inherited=records[:90],input=header,columns=columns,raw=raw,provenance=provenance,failure=failure)

def read_selected(q,names):
 CONTEXT.update(stage='read_authenticated_earned_words',record=thin(q))
 assert len(names)==len(set(names)) and all(n in q['metadata']['schema'] for n in names)
 bind(q['file'],q['sha256']);out={}
 with np.load(P.path(q['file']),allow_pickle=False) as f:
  assert set(f.files)==set(q['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
  for n in names:
   a=f[n].copy();s=q['metadata']['schema'][n];keep('copied_earned_'+n,a)
   assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a)),n;out[n]=a
 return out

def recovery_packet(refs):
 header=refs['input'];names=['completed_INPUT_basis_'+n for n in ('R','dv','hats')]+['completed_INPUT_sheet_'+w for w in ('hi','lo')]
 d=read_selected(header,names);basis={n:d['completed_INPUT_basis_'+n] for n in ('R','dv','hats')};sheet=tuple(d['completed_INPUT_sheet_'+w] for w in ('hi','lo'));parts=[]
 assert all(np.all(a[~N.normal_test_mask()]==0) for a in sheet)
 for iq,q in enumerate(refs['columns']):
  CONTEXT.update(stage='hydrate_earned_column_collector_operands',column=iq)
  names=['completed_RATE_STATE_COLUMN_'+family+'_'+n+'_'+w for family in ('value','delta') for n in ('normal_coefficients','initial_CMC_density') for w in ('hi','lo')]
  d=read_selected(q,names);part={family:{n:tuple(d['completed_RATE_STATE_COLUMN_'+family+'_'+n+'_'+w] for w in ('hi','lo')) for n in ('normal_coefficients','initial_CMC_density')} for family in ('value','delta')}
  part.update(normal_coordinate_order=('value','R','Z','t'),relative_phase_count=1,ordinary_label_count=1);parts.append(part)
 names=['NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_'+family+'_current_'+w for family in ('native','metric') for w in ('hi','lo')]
 d=read_selected(refs['raw'],names);current={family:tuple(d['NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_'+family+'_current_'+w] for w in ('hi','lo')) for family in ('native','metric')}
 assert current['native'][0].shape==current['native'][1].shape==(33,3,87,45) and current['metric'][0].shape==current['metric'][1].shape==(6,87,45)
 clear_current()
 for n,x in current.items():fy_keep('NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_full_'+n+'_current',x,keep)
 normal_test=np.zeros((4,87,45));normal_test[:,43,22]=(1.,-2.,3.,4.);normal_test[:,43,0]=(1.,-2.,3.,4.)
 keep('original_inadmissible_diagnostic_normal_test',normal_test.copy());normal_test[~N.normal_test_mask()]=0
 assert normal_test[2,43,0]==0 and np.array_equal(normal_test[(0,1,3),43,0],np.array((1.,-2.,4.)))
 keep('NEW_original_mask_restricted_normal_test',normal_test.copy());scalar_test=np.zeros((87,45));scalar_test[43,22]=1.;keep('unchanged_original_CMC_test',scalar_test.copy())
 CONTEXT.update(stage='NEW_unstarted_original_collector',ancestor_failure=refs['failure'])
 normal=finite_candidate_global_normal_CMC(parts,basis,normal_test,scalar_test,keep,P.check,'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC')
 weak_normal=fy_keep('NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_volume_plus_unchanged_sheet_normal',P.a_add(normal['value']['weak_normal'],sheet),keep)
 expected=['NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_'+family+'_'+kind+'_polynomial_transpose' for family in ('value','delta') for kind in ('normal','CMC')]
 assert [c['name'] for c in CHECKS]==expected and all(c['passed'] is True and c['tolerance']==2e-11 for c in CHECKS)
 result=dict(current=current,weak_normal=weak_normal,weak_initial_CMC=normal['value']['weak_initial_CMC'],normal_CMC=normal,unchanged_sheet_weak_normal=sheet,columns=[thin(q) for q in refs['columns']],provenance=refs['provenance'],point_first_TOTAL_addition=True,nodal_add_then_lift_construction_gap_external=True,original_canonical_targets_unchanged=True,phase_current_words_unchanged=True,spatial_metric_words_unchanged=True,all_genuine_time_components_updated=True,canonical_after_finite_update_admission_external=True,stationarity_feedback_external=True,physical_metric_or_normal_CMC_adoption=False,physical_adoption=False)
 readout=seal_readout(result,dict(kind_scope='fresh_point_first_TOTAL_rate_momenta_all16normal_CMC_at_unchanged_spatial_geometry',correction_original_six_admitted=True,new_current_original_six_admission_external=True,stationarity_feedback_and_geometry_solve_external=True,exact_geodesic_and_new43_external=True,provenance=refs['provenance'],inherited_success_input=thin(header),inherited_success_columns=[thin(q) for q in refs['columns']],completed_current_evidence=thin(refs['raw']),ancestor_failure=refs['failure'],only_unstarted_collector_and_original_mask_restricted_probe=True))
 return dict(status=STATUS,columns=result['columns'],readout=thin(readout),input=thin(header),original_targets=refs['provenance']['unchanged_original_targets'],correction=header['metadata']['correction'],all16normal_ports_per_section=True,current99_and_physical6_fresh=True,spatial_geometry_unchanged=True,new_current_six_canonical_gates_or_normal_CMC_acceptance=False,stationarity_feedback_or_new43_earned=False,physical_adoption=False,ancestor_failure=refs['failure'],inherited_success_records=[thin(q) for q in refs['inherited']],new_owned_records=[thin(readout)],original_controls=0,new_collector_controls=4,new_point_ports_or_current_scatters=0)

def seal_readout(payload,metadata):
 def collect(prefix,x):
  if isinstance(x,np.ndarray):keep(prefix,x)
  elif isinstance(x,tuple) and len(x)==2 and all(isinstance(a,np.ndarray) for a in x):
   keep(prefix+'_both_words',np.stack(x).copy())
   for w,a in zip(('hi','lo'),x):keep(prefix+'_'+w,a)
  elif isinstance(x,dict):
   for n,a in x.items():collect(prefix+'_'+str(n),a)
 collect('completed_READOUT',payload)
 q=P.checkpoint('READOUT',{n:a.copy() for n,a in {**RAW,**AVAILABLE}.items()},dict(metadata,kind='READOUT',physical_adoption=False));clear_current();return q

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None
 assert all(x is not None for q in (PARENT_ERROR,PARENT_RECEIPT,PARENT_FAILURE_PROOF) for x in q),'Root natural failure byte proof and FULL-reviewed release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive future namespace required';initialize()
 SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for name,digest in PINS.items():bind(name,digest)
  refs=admit_saved();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],ancestor_failure=refs['failure'],inherited_success_records=[thin(q) for q in refs['inherited']],selected_decode_records=[thin(refs['input'])]+[thin(q) for q in refs['columns']]+[thin(refs['raw'])],input_sha256=dict(INPUTS),new_point_ports_or_current_scatters=0,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=recovery_packet(refs)
  assert len(RECORDS)==1 and len(CHECKS)==4;P.recheck()
  rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=STATUS,case=case,controls=CHECKS,checkpoints=refs['inherited']+RECORDS,inherited_success_records=[thin(q) for q in refs['inherited']],new_owned_records=[thin(q) for q in RECORDS],ancestor_failure=refs['failure'],qualification=FLAGS))
  P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),inherited_output_sha256={q[k]:q[h] for q in refs['inherited'] for k,h in (('file','sha256'),('commit_file','commit_sha256'))},ancestor_failure=refs['failure'],result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',{n:a.copy() for n,a in {**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}.items()},dict(context=dict(CONTEXT),kind='incomplete_saved_column_collector_recovery',original_failure_preserved=True),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,original_failure_preserved=True,ancestor_failure=dict(source=PARENT_SOURCE,error=PARENT_ERROR,receipt=PARENT_RECEIPT,root_proof=PARENT_FAILURE_PROOF),qualification=FLAGS))
  prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),original_failure_preserved=True,qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
