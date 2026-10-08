"""HELD saved-only χ census/publication recovery; root alone releases.
Only source/JSON/COMMIT/byte authentication and existing metadata are used.
No NumPy, payload decode, arithmetic helper, producer, current, EOS, normal,
functional, scatter, fixture or completed control is reevaluated.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CACHED_UPDATED_PHASE_CHI_SAVED_PUBLICATION_RECOVERY_V003'
PROTOCOL='CACHED_UPDATED_PHASE_CHI_SAVED_PUBLICATION_RECOVERY_V002.md'
PROTOCOL_SHA='8f44966a430cb361a6ab3198ba7e38333c83d6d1f52aab0ac8638eafed940df5'
SOURCE=('cross_u_cached_updated_phase_compact_chi_contact_v004.py','7a2e417362df9229167e2574512c826fcfb1f128f80d0ac31f94f8c719f17c56')
ERROR=('CROSS_U_CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V004_ERROR.json','87fa5ff51d7b92f58c0ef2ba9144661f633f3e192975a28a0942c067f45c8b88')
RECEIPT=('CROSS_U_CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V004_RECEIPT.json','524fa4cf5656dc38679035ca82cea35fa503bbb69244f1a9a0e9827d0cf0f4df')
ROOT_FAILURE_PROOF=('ROOT_NATURAL_CLOSED_CACHED_PHASE_CHI_COMPLETED_ACTION_PARTIAL_SEALS_V001.json', 'df74b8eec4941e99c3d15b1f2e6340f4f2112286d9e37c1b19523ae61f47d214', 'ROOT_NATURAL_CLOSED_CACHED_PHASE_CHI_COMPLETED_ACTION_PARTIAL_SEALS_VERIFIED')
EOS_KEYS=('X2', 'X', 'q', 'u', 's', 'pressure', 'PX', 'PXX', 'J', 'registered_J', 'p', 'registered_p', 'H', 'registered_H', 'reduced_H', 'density', 'current_gap', 'density_gap', 'hessian_gap', 'reduced_gap')
NORMAL_KEYS=('absolute','relative','action','hamiltonian')
INPUTS={};OUTPUTS={};CONTEXT={};OWNER=None


def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()


def bind(name,digest):
 assert isinstance(name,str) and name and isinstance(digest,str) and len(digest)==64
 p=BASE/name if not Path(name).is_absolute() else Path(name);key=str(p.resolve())
 assert key not in INPUTS or INPUTS[key]==digest;assert sha(p)==digest,name;INPUTS[key]=digest
 return p


def publish(name,value):
 p=BASE/name;data=(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);digest=sha(p);OUTPUTS[name]=digest;return digest


def census_names():
 return (tuple('four_point_cached_EOS_'+n for n in EOS_KEYS)+tuple('four_point_'+n+'_chain_'+k for n in ('P','PX','PXX') for k in ('actual','expected','gap'))+
         tuple('four_point_row%d_'%r+n for r in range(4) for n in NORMAL_KEYS)+('NEW_updated_phase_chi_normal_functional_polynomial_transpose','NEW_updated_phase_chi_literal_current_functional'))


def admit_saved():
 for ref in (SOURCE,ERROR,RECEIPT,ROOT_FAILURE_PROOF):bind(ref[0],ref[1])
 e=json.loads((BASE/ERROR[0]).read_text());rc=json.loads((BASE/RECEIPT[0]).read_text());proof=json.loads((BASE/ROOT_FAILURE_PROOF[0]).read_text())
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==ERROR[1] and e['owner']==rc['owner']==proof['owner']
 assert e['owner']['pid']==23460 and e['owner']['source_sha256']==SOURCE[1]
 assert proof['status']==ROOT_FAILURE_PROOF[2] and proof['source_sha256']==SOURCE[1] and proof['error_sha256']==ERROR[1] and proof['receipt_sha256']==RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==1 and proof['all_input_seals_verified'] is True and proof['all_partial_error_seals_verified'] is True and proof['completed_scientific_roles']==26 and proof['earned_controls']==47 and proof['error_raw_roles']==1 and proof['exact_Fraction_error_bound_ratios_passed'] is True
 assert e['qualification']==rc['qualification'] and all(x is False for x in e['qualification'].values())
 assert e['raw_preservation_traceback'] is None and e['closing_traceback'] is None
 assert 'line 231, in cached_chi_packet' in e['traceback'] and 'assert len(CHECKS)==48 and all' in e['traceback'] and e['traceback'].endswith('AssertionError\n')
 failed_stem=ERROR[0].removesuffix('_ERROR.json');assert not (BASE/(failed_stem+'_RESULT.json')).exists()
 assert e['input_sha256']==rc['input_sha256'] and len(rc['input_sha256'])==144 and len(rc['output_sha256'])==57
 controls=e['controls'];names=census_names();assert len(EOS_KEYS)==20 and len(names)==len(set(names))==len(controls)==47
 assert tuple(q['name'] for q in controls)==names and tuple(q['ordinal'] for q in controls)==tuple(range(47))
 assert all(q['passed'] is True and q['tolerance']==2e-11 and math.isfinite(q['error']) and 0<=q['error']<=2e-11 for q in controls)
 records=e['checkpoints'];expected=['CACHED_CHI_INPUT']+(['EOS_CHI_CONTACT']+['PHASE_CHI_NORMAL_ROW']*4+['CHI_COLUMN'])*4+['CHI_READOUT']
 assert len(records)==27 and [q['metadata']['role'] for q in records[:26]]==expected
 for index,q in enumerate(records):
  CONTEXT.update(stage='authenticate_completed_saved_record',record=index)
  for k,h in (('file','sha256'),('commit_file','commit_sha256')):bind(q[k],q[h]);assert rc['output_sha256'][q[k]]==q[h]
  assert json.loads((BASE/q['commit_file']).read_text())=={k:q[k] for k in ('file','sha256','metadata')}
  md=q['metadata'];assert md['owner']==e['owner'] and md['qualification']==e['qualification'] and md['failed'] is (index==26)
  if index<26:assert all(v['finite'] is True and v['dtype'] in ('float64','int64','bool') for v in md['schema'].values())
 assert records[-1]['metadata']['schema']=={} and records[-1]['file'].endswith('_ERROR_RAW.npz')
 for iq in range(4):
  eos,rows,col=records[1+6*iq],records[2+6*iq:6+6*iq],records[6+6*iq]
  assert eos['metadata']['column']==col['metadata']['column']==iq and [q['metadata']['row'] for q in rows]==list(range(4))
  assert col['metadata']['eos_contact']=={n:eos[n] for n in ('file','sha256','commit_file','commit_sha256')}
  assert col['metadata']['normal_contacts']==[{n:q[n] for n in ('file','sha256','commit_file','commit_sha256')} for q in rows]
  assert col['metadata']['mechanical_CMC_and_test_gradient_contacts_bitwise_unchanged'] is True and col['metadata']['new_phase_delta_is_chi_not_temporal_step'] is True
 assert records[25]['metadata']['point_direction_count']==1 and records[25]['metadata']['geometry_response_or_physical_admission'] is False
 return e,rc,records[:26],records[-1]


def main():
 global OWNER
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None
 assert all(x is not None for x in ROOT_FAILURE_PROOF),'Root authenticated natural CLOSED_ERROR proof required before IO'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive future namespace required'
 OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__).resolve()))
 try:
  publish(STEM+'_OWNER_START.json',OWNER);bind(Path(__file__).name,OWNER['source_sha256']);bind(PROTOCOL,PROTOCOL_SHA)
  e,rc,earned,failed=admit_saved();columns=[earned[6+6*iq] for iq in range(4)];header=earned[0];readout=earned[25]
  case=dict(original_failure=dict(source=SOURCE,error=ERROR,receipt=RECEIPT,root_proof=ROOT_FAILURE_PROOF,owner=e['owner'],status='CLOSED_ERROR',missing_original_RESULT=True,failed_empty_raw=failed),
   input=header,columns=columns,readout=readout,normal_terminal=header['metadata']['normal_terminal'],finite_terminal=header['metadata']['finite_terminal'],join_terminal=header['metadata']['join_terminal'],
   point_control_cells=header['metadata']['four_point_control_cells'],chi_node=header['metadata']['chi_node'],controls=47,roles=26,original_erroneous_predicted_controls=48,
   census_derivation=dict(EOS=20,chain=9,normal=16,weak=2),new_scientific_actions=0,new_controls=0,new_numeric_roles=0,
   new_EOS_values_or_logs=False,old_temporal_direction_reused=False,original_targets_or_epsilon_refitted=False,full_geometry_Jacobian_or_physical_admission=False,physical_adoption=False)
  publish(STEM+'_MANIFEST.json',dict(owner=OWNER,case=case,input_sha256=dict(INPUTS),scope='Saved-only completed47-control26-role publication; original48predictionfailure preserved',qualification=e['qualification']))
  rh=publish(STEM+'_RESULT.json',dict(owner=OWNER,status='CACHED_UPDATED_PHASE_ORIGINAL_COMPACT_CHI_CONTACT_SAVED_RECOVERED',case=case,controls=e['controls'],checkpoints=earned,qualification=e['qualification']))
  publish(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=datetime.now(timezone.utc).isoformat(),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=e['qualification']))
  print('SAVED_RECOVERED',47,26,rh);return 0
 except BaseException:
  eh=publish(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=traceback.format_exc(),context=dict(CONTEXT),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),old_failure_preserved=True,new_scientific_actions=0,physical_adoption=False))
  prior=BASE/(STEM+'_RECEIPT.json');publish(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=OWNER,status='CLOSED_ERROR',closed=datetime.now(timezone.utc).isoformat(),error_sha256=eh,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),physical_adoption=False));raise
if __name__=='__main__':raise SystemExit(main())
