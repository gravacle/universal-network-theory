"""Held saved-factor recovery; original failed component control remains False."""
from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NATIVE_METRIC_STAR_PRECONDITIONER_PREPARATION_V003'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='fbd7fa1ac9f54820e5757a54027403d6411fc4bd6891c8120fda96645c3af25b'
PROVIDER='cross_u_native_metric_star_preconditioner_preparation_v002.py'
PROVIDER_SHA='711c7f83bbe1c1603f03796fc9109e7abc075c8ea042f26beffc869418827aaa'
CERTIFIER='author_fragment_saved_native_metric_star_balanced_certifier_v001.py'
CERTIFIER_SHA='64b8e76d9a67c6efbc97c229eff7fccbcb87e6bbae20cc73ecbe42ceb1382524'
P=U=np=None

def bind(n,h):
 p=Path(n);p=p if p.is_absolute() else BASE/p;assert h is not None and P.sha(p)==h,n
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h;return p

def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())
def arrays():return {n:np.asarray(x).copy() for n,x in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def reset(stage):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage)

def initialize():
 global P,U,np,ORIGINAL_CAPTURE
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('failed_STAR_definitions_only',BASE/PROVIDER);U=importlib.util.module_from_spec(spec);spec.loader.exec_module(U);U.initialize()
 P,np=U.P,U.np;ORIGINAL_CAPTURE=U.ORIGINAL_CAPTURE;P.capture=keep;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 assert not P.CHECKS and not P.RECORDS and not P.OUTPUTS and all(v is False for v in P.FLAGS.values())
 for n,h in ((PROVIDER,PROVIDER_SHA),(CERTIFIER,CERTIFIER_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 exec(compile((BASE/CERTIFIER).read_text(),str(BASE/CERTIFIER),'exec'),globals())
 assert SAVED_STAR_BALANCED_CERTIFIER_AUTHOR_DRAFT is True and SAVED_STAR_BALANCED_CERTIFIER_AUTHORING_IN_PROGRESS is False

def recovery_admission():
 old='CROSS_U_NATIVE_METRIC_STAR_PRECONDITIONER_PREPARATION_V002';eh='e7daed54d1fee510e79a7e87391c64d23aefec0a1b5f7990a70cb2c765e93a14';ch='7aff2f4525c6687bb7305406d288d3eba74b59a2f2ba2cbca3dfb532a015b902'
 for n,h in ((old+'_ERROR.json',eh),(old+'_RECEIPT.json',ch),(old+'.md','c4e82d22e375067dc21d1e502c4f4fcb48934fbd7965c79501d92b737b2574c1'),('ROOT_SAVED_STAR_FACTOR_FAILED_CONTACT_DIAGNOSTIC_V001.json','f2ac7d038304da09030752f7d1707f336c044fe372a3c3600dacc4d67d0a5ff5')):bind(n,h)
 e=json.loads(P.path(old+'_ERROR.json').read_text());rc=json.loads(P.path(old+'_RECEIPT.json').read_text())
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==eh and rc.get('result_sha256') is None and e['owner']==rc['owner'] and e['owner']['pid']==80804 and e['owner']['source_sha256']==PROVIDER_SHA
 assert e['qualification']==rc['qualification'] and all(v is False for v in e['qualification'].values()) and len(e['controls'])==13 and len(e['checkpoints'])==4
 assert all(c['passed'] is True for c in e['controls'][:12]) and e['controls'][12]==dict(ordinal=12,name='NEW_star_factor_U_metric_block_absolute_inverse_construction',error=1.0,tolerance=2e-11,passed=False)
 shapes=(('INPUT',88,'238c016b4db9a84937a0fbf1da2db211e306aaa21f31b10b60482e9dff74e6b6','ba7ae657a59b38dd09aaeda4b4aeb592d9cd4d3bf55e2071a0f86fbfcc768b0e'),('FIXTURE',256,'06c5aacae3cf8a0d23d3bc0b014eb5c805bc859384b043bf6068f73c45b6a922','d6a53cf42a25293b4f194c3b00083892d5cdd79dac180fd528884497acb84125'),('COMMON_BASIS',101,'c18bfd078ae1075ed1b4d6b5ccc53f5a1bc15816ebbc2731c3fc2d4121ca3b1f','fc9705201076c3154b14a7080e53ae9f7e658888e9cc1fcd310dabd0e5df6622'),('ERROR_RAW',132,'84042e36c71c4abe38e1b7891080a4a7aba48242b252e3c854f745baee94d57e','b93754b1fd1afe677b774912e7e6089c28929b2e882739033bdc5c990beb126c'))
 refs={}
 for i,(tag,count,h,c) in enumerate(shapes):
  q=e['checkpoints'][i];assert q['file']==old+'_%05d_'%i+tag+'.npz' and q['sha256']==h and q['commit_sha256']==c and len(q['metadata']['schema'])==count and q['metadata']['failed'] is (i==3)
  for n,v in ((q['file'],h),(q['commit_file'],c)):assert rc['output_sha256'][n]==v;bind(n,v)
  a=json.loads(P.path(q['commit_file']).read_text());assert a=={n:q[n] for n in ('file','sha256','metadata')} and a['metadata']['owner']==e['owner'] and a['metadata']['qualification']==e['qualification'];refs[tag]=q
 raw=refs['ERROR_RAW']['metadata']['schema'];prefix='NEW_star_factor_U_metric_block_'
 for n in ('absolute_congruence_factor','balanced_absolute_block','symmetric_preconditioner_block','signed_inverse','absolute_inverse_contact','eigenvectors','eigen_equation_defect','orthogonality_defect'):assert raw[prefix+n]==dict(shape=[3915,9,9],dtype='float64',finite=True)
 assert raw[prefix+'exact_power_two_balance_exponents']==dict(shape=[3915,9],dtype='int32',finite=True)
 return dict(records=refs,controls=e['controls'],terminal=dict(pid=80804,source_sha256=PROVIDER_SHA,protocol_sha256='c4e82d22e375067dc21d1e502c4f4fcb48934fbd7965c79501d92b737b2574c1',error_sha256=eh,receipt_sha256=ch,result_sha256=None),original_failed_control_preserved=True)

def copy_record(q,tag):
 reset('bitcopy_earned_'+tag);a=P.read_pair(q,tuple(q['metadata']['schema']))
 for n,x in a.items():keep(n,x.copy())
 rec=P.checkpoint(tag,{n:np.asarray(x).copy() for n,x in a.items()},dict(kind='exact_reuse_of_failed_STAR_'+tag,parent_ref=thin(q),parent_metadata=q['metadata'],all_original_fields_bitcopied=True,old_science_or_controls_replayed=False,original_componentwise_failed_control_preserved=True));return a,rec

def recovery_packet(refs):
 P.CHECKS.extend(json.loads(json.dumps(refs['controls'])));records={}
 inp,records['input']=copy_record(refs['records']['INPUT'],'INPUT');fixture,records['fixture']=copy_record(refs['records']['FIXTURE'],'FIXTURE');del fixture
 common,records['assembly']=copy_record(refs['records']['COMMON_BASIS'],'COMMON_BASIS');del common
 raw,records['completed_factor']=copy_record(refs['records']['ERROR_RAW'],'COMPLETED_FACTOR')
 reset('NEW_all_node_balanced_normwise_saved_factor_certificates');p='NEW_star_factor_U_metric_block_';control='control_012_NEW_star_factor_U_metric_block_absolute_inverse_construction_'
 aliases=dict(absolute='balanced_absolute_block',factor='absolute_congruence_factor',symmetric='symmetric_preconditioner_block',signed_inverse='signed_inverse',balance='balance',inverse_balance='inverse_balance',balance_exponents='exact_power_two_balance_exponents',eigenvalues='signed_eigenvalues',eigenvectors='eigenvectors',eigen_equation_defect='eigen_equation_defect',orthogonality_defect='orthogonality_defect',resolved_error_budget='resolved_error_budget',resolved_spectral_margin='resolved_spectral_margin')
 s={n:raw[p+v] for n,v in aliases.items()};s.update(failed_absolute_actual=raw[control+'actual'],failed_absolute_expected=raw[control+'expected'],failed_absolute_original_envelope=raw[control+'envelope'])
 assert np.array_equal(s['failed_absolute_actual'],raw[p+'absolute_inverse_contact']) and np.array_equal(s['factor'],raw[p+'coordinate_preserving_factor_binary64'])
 certificate=certify_saved_native_metric_star_factor(s,'NEW_completed_star_certificate');assert len(P.CHECKS)==15 and P.CHECKS[12]['passed'] is False and all(c['passed'] for c in P.CHECKS[13:])
 K=raw['NEW_star_factor_retained_signed_reduced_block'];pre=dict(L=raw['NEW_star_factor_Lbar_binary64'],V=raw['NEW_star_factor_Dinv_metric_binary64'],D_factor=raw['NEW_star_factor_mode_blocks_absolute_congruence_factor'],K_factor=s['factor'],D_symmetric=raw['NEW_star_factor_mode_blocks_symmetric_preconditioner_block'],K_symmetric=s['symmetric'],C=K[:,:3,3:],S=K[:,3:,3:],basis_scale=inp['older_native_STAR_copied_preconditioner_basis_scale'],native_mask=inp['older_native_STAR_native_active_mask'],metric_mask=inp['older_native_STAR_metric_active_mask'])
 for n,x in pre.items():keep('NEW_star_preconditioner_'+n,np.asarray(x).copy())
 rec=P.checkpoint('CERTIFIED_FACTOR',arrays(),dict(certificate,input_ref=thin(records['input']),completed_factor_ref=thin(records['completed_factor']),original_failed_control=refs['controls'][12],all_original_controls_copied_without_replay=True,new_controls=P.CHECKS[13:],sqrt_columns_coordinate_words_readout_and_upstream_evidence_in_completed_factor=True,preconditioner_is_numerical_only=True,recurrence_not_selected=True))
 records['factor']=rec;assert len(P.RECORDS)==5
 return dict(status='SAVED_COMPLETED_STAR_BALANCED_NORMWISE_CONSTRUCTION_PASS',**records,parent_terminal=refs['terminal'],new_candidate_factor_certified=True,total_controls=15,original_control_pass_count=12,original_componentwise_control_12_passed=False,new_normwise_controls=2,original_failed_control_preserved=True,fine_action_or_RHS_or_original_six_gates_changed=False,new_response_computed=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and '--root-run' in sys.argv,'Held FULL review and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();refs=recovery_admission();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_NEW_saved_star_balanced_normwise_recovery');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  case=recovery_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='NEW_saved_STAR_certificate_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
