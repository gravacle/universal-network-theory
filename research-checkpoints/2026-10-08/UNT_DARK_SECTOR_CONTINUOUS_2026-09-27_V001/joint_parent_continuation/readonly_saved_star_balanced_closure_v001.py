"""Guarded saved-only factor closure; the original componentwise FAIL remains."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NATIVE_METRIC_STAR_PRECONDITIONER_PREPARATION_V004'
OUT='READONLY_SAVED_STAR_BALANCED_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE='cross_u_native_metric_star_preconditioner_preparation_v004.py'
SOURCE_SHA='baba0601348770ee6461b4abc9fc368addb3ecba3f8c1842c3bea4781d7e26e0'
PROTOCOL_SHA='1b1c1586bd5989686768504aeb6ff391a989702a1938a9e3365711376a374e9b'
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
OLD='CROSS_U_NATIVE_METRIC_STAR_PRECONDITIONER_PREPARATION_V002'
OLD_ERROR_SHA='e7daed54d1fee510e79a7e87391c64d23aefec0a1b5f7990a70cb2c765e93a14'
OLD_RECEIPT_SHA='7aff2f4525c6687bb7305406d288d3eba74b59a2f2ba2cbca3dfb532a015b902'
TOL=2e-11
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def saved_json(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def main():
 assert AUTHOR_DRAFT is False and all(TERMINAL[n] is not None for n in ('pid','result_sha256','receipt_sha256')) and TERMINAL['error_sha256'] is None and not path(OUT).exists()
 assert sha(SOURCE)==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 r=saved_json(STEM+'_RESULT.json',TERMINAL['result_sha256']);rc=saved_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256'])
 assert rc['status']=='CLOSED' and rc['result_sha256']==TERMINAL['result_sha256'] and rc.get('error_sha256') is None and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['status']=='SAVED_COMPLETED_STAR_BALANCED_NORMWISE_CONSTRUCTION_PASS' and r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 assert r['new_candidate_factor_certified'] is True and r['original_failed_control_preserved'] is True and r['total_controls']==15 and r['original_control_pass_count']==12 and r['original_componentwise_control_12_passed'] is False and r['new_normwise_controls']==2
 assert all(r[n] is False for n in ('fine_action_or_RHS_or_original_six_gates_changed','new_response_computed','physical_adoption'))
 def inherited(n,h):
  key=n if n in rc['input_sha256'] else str(path(n).resolve());assert rc['input_sha256'][key]==h
  return saved_json(n,h)
 old=inherited(OLD+'_ERROR.json',OLD_ERROR_SHA);oldrc=inherited(OLD+'_RECEIPT.json',OLD_RECEIPT_SHA)
 assert old['status']=='FAILED' and oldrc['status']=='CLOSED_ERROR' and oldrc['error_sha256']==OLD_ERROR_SHA and oldrc.get('result_sha256') is None and oldrc['owner']==old['owner'] and old['owner']['pid']==80804 and old['qualification']==oldrc['qualification'] and all(v is False for v in old['qualification'].values())
 assert not path(OLD+'_RESULT.json').exists() and r['parent_terminal']['pid']==80804 and r['parent_terminal']['error_sha256']==OLD_ERROR_SHA and r['parent_terminal']['receipt_sha256']==OLD_RECEIPT_SHA
 records=r['checkpoints'];controls=r['controls'];assert len(records)==5 and len(controls)==15 and controls[:13]==old['controls'] and controls[12]==dict(ordinal=12,name='NEW_star_factor_U_metric_block_absolute_inverse_construction',error=1.,tolerance=TOL,passed=False)
 assert all(c['passed'] is True for c in controls[:12]+controls[13:]) and [c['ordinal'] for c in controls]==list(range(15))
 assert [r[n] for n in ('input','fixture','assembly','completed_factor','factor')]==records and len({q['file'] for q in records})==5
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,k in ((q['file'],'sha256'),(q['commit_file'],'commit_sha256')):assert rc['output_sha256'][n]==q[k] and sha(n)==q[k]
  assert saved_json(q['commit_file'],q['commit_sha256'])=={n:q[n] for n in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and q['metadata']['failed'] is False
  assert all(s['finite'] is True for s in q['metadata']['schema'].values())
 import numpy as np
 selected=[];triplet_errors=[];triplets={}
 def read(q,names):
  out={};schema=q['metadata']['schema']
  with np.load(path(q['file']),allow_pickle=False) as z:
   assert set(z.files)==set(schema)|{'metadata_json'} and json.loads(str(z['metadata_json']))==q['metadata']
   for n in names:
    x=z[n].copy();assert list(x.shape)==schema[n]['shape'] and str(x.dtype)==schema[n]['dtype'] and schema[n]['finite'] is True and np.all(np.isfinite(x)),n;out[n]=x
  selected.append(dict(file=q['file'],fields=len(names)));return out
 for i,q in enumerate(records[:4]):
  parent=old['checkpoints'][i];assert q['metadata']['parent_ref']=={n:parent[n] for n in ('file','sha256','commit_file','commit_sha256')} and q['metadata']['parent_metadata']==parent['metadata'] and q['metadata']['all_original_fields_bitcopied'] is True and q['metadata']['old_science_or_controls_replayed'] is False and q['metadata']['original_componentwise_failed_control_preserved'] is True and q['metadata']['schema']==parent['metadata']['schema']
  for n,k in ((parent['file'],'sha256'),(parent['commit_file'],'commit_sha256')):
   key=n if n in rc['input_sha256'] else str(path(n).resolve());assert rc['input_sha256'][key]==parent[k] and sha(n)==parent[k]
  with np.load(path(q['file']),allow_pickle=False) as z,np.load(path(parent['file']),allow_pickle=False) as p:
   assert json.loads(str(z['metadata_json']))==q['metadata'] and json.loads(str(p['metadata_json']))==parent['metadata']
   for n in q['metadata']['schema']:assert np.array_equal(z[n],p[n]),n
 for c in controls:
  assert c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL)
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));hits=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert hits
  rows=[read(q,names) for q in hits];a=rows[0];assert all(all(np.array_equal(a[n],b[n]) for n in names) for b in rows)
  actual,expected,envelope=(a[n] for n in names);assert actual.shape==expected.shape==envelope.shape and np.all(envelope>=0);triplets[c['ordinal']]=(actual,expected,envelope)
  error=float(np.max(abs(actual-expected)/np.maximum(envelope,1e-30),initial=0));assert error==c['error'];triplet_errors.append(error)
 factor=records[4];fm=factor['metadata'];assert fm['kind']=='NEW_balanced_normwise_certificate_of_completed_saved_coupled_factor' and fm['original_failed_control']==controls[12] and fm['new_controls']==controls[13:] and fm['arithmetic_tolerance']==TOL
 assert all(fm[n] is True for n in ('original_componentwise_failed_control_preserved','signed_contact_is_NEW_once','scaling_round_trip_bitwise_exact','gate_is_construction_operation_norm','all_original_controls_copied_without_replay','preconditioner_is_numerical_only','recurrence_not_selected')) and all(fm[n] is False for n in ('absolute_contact_or_factor_replayed','explanatory_orthogonality_bound_is_an_admission_route','fine_action_RHS_or_original_row_gates_changed','forward_inverse_error_or_global_coercivity_claimed','physical_adoption'))
 prefix='NEW_completed_star_certificate_';aliases=dict(absolute='balanced_absolute_block',factor='absolute_congruence_factor',symmetric='symmetric_preconditioner_block',signed_inverse='signed_inverse',balance='balance',inverse_balance='inverse_balance',balance_exponents='exact_power_two_balance_exponents',eigenvalues='signed_eigenvalues',eigenvectors='eigenvectors',eigen_equation_defect='eigen_equation_defect',orthogonality_defect='orthogonality_defect',resolved_error_budget='resolved_error_budget',resolved_spectral_margin='resolved_spectral_margin')
 raw=read(records[3],tuple('NEW_star_factor_U_metric_block_'+n for n in aliases.values())+('NEW_star_factor_U_metric_block_absolute_inverse_contact','NEW_star_factor_U_metric_block_coordinate_preserving_factor_binary64','NEW_star_factor_Lbar_binary64','NEW_star_factor_Dinv_metric_binary64','NEW_star_factor_mode_blocks_absolute_congruence_factor','NEW_star_factor_mode_blocks_symmetric_preconditioner_block','NEW_star_factor_retained_signed_reduced_block'))
 copied=read(factor,tuple(prefix+'copied_'+n for n in aliases))
 for n,v in aliases.items():assert np.array_equal(copied[prefix+'copied_'+n],raw['NEW_star_factor_U_metric_block_'+v])
 failed=read(factor,tuple(prefix+'copied_failed_absolute_'+n for n in ('actual','expected','original_envelope')))
 for n,x in zip(('actual','expected','original_envelope'),triplets[12]):assert np.array_equal(failed[prefix+'copied_failed_absolute_'+n],x)
 assert np.array_equal(triplets[12][0],raw['NEW_star_factor_U_metric_block_absolute_inverse_contact']) and np.array_equal(copied[prefix+'copied_factor'],raw['NEW_star_factor_U_metric_block_coordinate_preserving_factor_binary64'])
 assert np.all(copied[prefix+'copied_resolved_spectral_margin']>0)
 conversions=('saved_absolute_contact_balanced','saved_absolute_block_balanced','saved_coordinate_factor_balanced','NEW_signed_contact_balanced','saved_symmetric_block_balanced','saved_signed_inverse_balanced')
 cv=read(factor,tuple(prefix+n+'_'+field for n in conversions for field in ('input','converted','round_trip','round_trip_difference','power_two_shift')))
 for n in conversions:assert np.array_equal(cv[prefix+n+'_input'],cv[prefix+n+'_round_trip']) and np.all(cv[prefix+n+'_round_trip_difference']==0)
 pre_names=('L','V','D_factor','K_factor','D_symmetric','K_symmetric','C','S','basis_scale','native_mask','metric_mask');pre=read(factor,tuple('NEW_star_preconditioner_'+n for n in pre_names))
 expected=dict(L=raw['NEW_star_factor_Lbar_binary64'],V=raw['NEW_star_factor_Dinv_metric_binary64'],D_factor=raw['NEW_star_factor_mode_blocks_absolute_congruence_factor'],K_factor=copied[prefix+'copied_factor'],D_symmetric=raw['NEW_star_factor_mode_blocks_symmetric_preconditioner_block'],K_symmetric=copied[prefix+'copied_symmetric'],C=raw['NEW_star_factor_retained_signed_reduced_block'][:,:3,3:],S=raw['NEW_star_factor_retained_signed_reduced_block'][:,3:,3:])
 inp=read(records[0],('older_native_STAR_copied_preconditioner_basis_scale','older_native_STAR_native_active_mask','older_native_STAR_metric_active_mask'));expected.update(basis_scale=inp['older_native_STAR_copied_preconditioner_basis_scale'],native_mask=inp['older_native_STAR_native_active_mask'],metric_mask=inp['older_native_STAR_metric_active_mask'])
 for n,x in expected.items():assert np.array_equal(pre['NEW_star_preconditioner_'+n],x)
 scores=read(factor,tuple(prefix+n for n in ('absolute_saved_contact_norm','absolute_operation_norm_envelope','absolute_normwise_scores','NEW_signed_contact_norm','signed_operation_norm_envelope','signed_normwise_scores')))
 for kind,actual_name in (('absolute','absolute_saved_contact_norm'),('signed','NEW_signed_contact_norm')):
  actual=scores[prefix+actual_name];envelope=scores[prefix+kind+'_operation_norm_envelope'];score=scores[prefix+kind+'_normwise_scores'];assert actual.shape==envelope.shape==score.shape==(3915,) and np.all(actual>=0) and np.all(envelope>=1) and np.array_equal(score,actual/envelope) and np.all(score<=TOL)
  ordinal=13 if kind=='absolute' else 14;c=controls[ordinal];assert c['error']==float(np.max(score)) and fm[kind+'_max_score']==c['error']
  assert np.array_equal(triplets[ordinal][0],actual) and np.all(triplets[ordinal][1]==0) and np.array_equal(triplets[ordinal][2],envelope)
 report=dict(status='SAVED_COMPLETED_STAR_BALANCED_NORMWISE_CLOSURE_PASS',owner_pid=os.getpid(),parent=TERMINAL,original_parent=r['parent_terminal'],committed_pairs=5,total_controls=15,original_control_pass_count=12,original_componentwise_control_12_passed=False,original_failed_control_preserved=True,new_normwise_controls=2,new_candidate_factor_certified=True,absolute_max_score=controls[13]['error'],signed_max_score=controls[14]['error'],factor_ref={n:factor[n] for n in ('file','sha256','commit_file','commit_sha256')},selected=selected,stored_triplet_errors=triplet_errors,old_input_maps_rehashed=False,matrix_reproducts_eigh_factors_assembly_fixture_or_operator_replayed=False,forward_inverse_error_or_global_coercivity_claimed=False,fine_action_RHS_or_original_six_gates_changed=False,new_response_computed=False,source_qualification=r['qualification'],physical_adoption=False,scope_limit='Exact saved record and factor-alias copies, stored roundtrip words, fifteen triplets including originalFalse, two already-stored norm scores only; no matrix norm/SVD/reproducts/scaling helper/factor/eigh/assembly/fixture/operator replay.')
 for q in records:assert sha(q['file'])==q['sha256'] and sha(q['commit_file'])==q['commit_sha256']
 assert sha(SOURCE)==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA and sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
