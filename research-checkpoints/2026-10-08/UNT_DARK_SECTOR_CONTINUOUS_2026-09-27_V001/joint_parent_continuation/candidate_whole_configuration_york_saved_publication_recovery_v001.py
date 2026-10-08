"""HELD saved-only completed fixed-rate whole-configuration/York publication; root alone releases.
Reads source/JSON/COMMIT bytes only. Root's natural-close full-seal proof owns
archive bytes and embedded metadata/schema. No archive opens, NumPy, numerical
helpers, producers, controls, actions, scatters or arithmetic replay.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_WHOLE_CONFIGURATION_YORK_SAVED_PUBLICATION_RECOVERY_V001'
PROTOCOL='CANDIDATE_WHOLE_CONFIGURATION_YORK_SAVED_PUBLICATION_RECOVERY_V001.md'
PROTOCOL_SHA='39e0164c211d2bfcbaf8aabbe76f279fb46e0823a0478a718567867afce6099a'
ORIGINAL_STEM='CROSS_U_CANDIDATE_WHOLE_CONFIGURATION_YORK_CONTACT_V002'
EXPECTED_SOURCE=('cross_u_candidate_whole_configuration_york_contact_v002.py', '4e22dfa402b4938805852f6127fb5ab3cffd53d03b4c709c85d3230648f71c52')
EXPECTED_OWNER_PID=29272
EXPECTED_MEASUREMENT_STATUS='WHOLE_CONFIGURATION_YORK_CANONICAL_NORMAL_CMC_CONTACTS_MEASURED'
RECOVERED_STATUS='WHOLE_CONFIGURATION_YORK_CANONICAL_NORMAL_CMC_CONTACTS_SAVED_RECOVERED'
SUCCESS_COUNT=147
CONTROL_COUNT=22
READOUT_ORDINALS=(76, 146)
READOUT_ROLE='FULL_WEAK'
SOURCE=(None,None)
ERROR=(None,None)
RECEIPT=(None,None)
ROOT_FAILURE_PROOF=(None,None,None)
INPUTS={};OUTPUTS={};CONTEXT={};OWNER=None
THIN_KEYS=('file','sha256','commit_file','commit_sha256')


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


def thin(record):
 return {k:record[k] for k in THIN_KEYS}


def expected_roles():
 return ['INPUT']+['CACHE_COLUMN']*4+['SHEET_CACHE','PREPARATION']+(['DIRECTION']+(['NORMAL_TEST']*16+['COLUMN'])*4+['FULL_WEAK'])*2


def expected_control_names():
 names=[]
 for direction in range(2):
  label='direction%d_NEW_whole_configuration'%direction
  names.extend([label+'_column%d_York_actual_trace_JVP'%iq for iq in range(4)]+[label+'_'+n+'_polynomial_transpose' for n in ('native','metric','phase','York_target')]+[label+'_normal_CMC_'+n+'_polynomial_transpose' for n in ('normal','CMC')]+[label+'_fixed_label_sheet_polynomial_transpose'])
 return names


def admit_saved():
 assert SOURCE==EXPECTED_SOURCE and ERROR[0]==ORIGINAL_STEM+'_ERROR.json' and RECEIPT[0]==ORIGINAL_STEM+'_RECEIPT.json'
 for ref in (SOURCE,ERROR,RECEIPT,ROOT_FAILURE_PROOF):bind(ref[0],ref[1])
 e=json.loads((BASE/ERROR[0]).read_text());rc=json.loads((BASE/RECEIPT[0]).read_text());proof=json.loads((BASE/ROOT_FAILURE_PROOF[0]).read_text())
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==ERROR[1]
 assert e['owner']==rc['owner']==proof['owner'] and e['owner']['pid']==EXPECTED_OWNER_PID and e['owner']['source_sha256']==SOURCE[1]
 assert proof['status']==ROOT_FAILURE_PROOF[2] and proof['source_sha256']==SOURCE[1] and proof['error_sha256']==ERROR[1] and proof['receipt_sha256']==RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==1
 assert proof['all_input_seals_verified'] is proof['all_success_role_seals_verified'] is proof['all_partial_error_seals_verified'] is True
 assert proof['completed_scientific_roles']==SUCCESS_COUNT and proof['earned_controls']==CONTROL_COUNT and proof['error_raw_roles']==1 and proof['original_controls_passed'] is True
 assert e['input_sha256']==rc['input_sha256'] and e['qualification']==rc['qualification'] and e['qualification'] and all(v is False for v in e['qualification'].values())
 assert isinstance(e['traceback'],str) and e['traceback'] and not (BASE/(ORIGINAL_STEM+'_RESULT.json')).exists()
 controls=e['controls'];names=expected_control_names()
 assert len(names)==len(set(names))==len(controls)==CONTROL_COUNT and [q['name'] for q in controls]==names and [q['ordinal'] for q in controls]==list(range(CONTROL_COUNT))
 assert all(q['passed'] is True and q['tolerance']==2e-11 and math.isfinite(q['error']) and 0<=q['error']<=2e-11 for q in controls)
 records=e['checkpoints'];roles=expected_roles();assert len(roles)==SUCCESS_COUNT and len(records)==SUCCESS_COUNT+1
 assert [q['metadata']['role'] for q in records[:SUCCESS_COUNT]]==roles
 assert [thin(q) for q in proof['records']]==[thin(q) for q in records]
 for ordinal,q in enumerate(records):
  CONTEXT.update(stage='authenticate_saved_COMMIT',record=ordinal)
  role=roles[ordinal] if ordinal<SUCCESS_COUNT else 'ERROR_RAW'
  assert q['file']==ORIGINAL_STEM+'_%05d_%s.npz'%(ordinal,role) and q['commit_file']==q['file']+'.COMMIT.json'
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256']
  bind(q['commit_file'],q['commit_sha256'])
  assert json.loads((BASE/q['commit_file']).read_text())=={k:q[k] for k in ('file','sha256','metadata')}
  md=q['metadata'];assert md['owner']==e['owner'] and md['qualification']==e['qualification'] and md['failed'] is (ordinal==SUCCESS_COUNT)
  if ordinal<SUCCESS_COUNT:assert all(v['finite'] is True for v in md['schema'].values())
 assert records[-1]['metadata']['schema']=={} and records[-1]['metadata']['context']['last_completed_role']==thin(records[READOUT_ORDINALS[-1]])
 assert records[0]['metadata']['expected_control_names']==names
 inherited=[]
 for direction,ordinal in enumerate(READOUT_ORDINALS):
  md=records[ordinal]['metadata'];part=controls[direction*(CONTROL_COUNT//2):(direction+1)*(CONTROL_COUNT//2)]
  assert md['direction']==direction and md['input']==thin(records[0]) and md['controls']==part and md['physical_adoption'] is False
  inherited.extend(md['controls'])
 assert inherited==controls
 return e,rc,records[:SUCCESS_COUNT],records[-1]


def recovered_case(e,rc,earned,failed):
 header=earned[0];hm=header['metadata'];readouts=[earned[n] for n in READOUT_ORDINALS]
 assert earned[5]['metadata']['input']==thin(header) and earned[6]['metadata']['input']==thin(header)
 assert earned[6]['metadata']['cached_columns']==[thin(q) for q in earned[1:5]] and earned[6]['metadata']['sheet_cache']==thin(earned[5]) and earned[6]['metadata']['original_current_prior_epsilon_words_unchanged'] is True
 for direction,readout in enumerate(readouts):
  start=7+70*direction;dr=earned[start];md=readout['metadata'];columns=[];rows=[]
  assert dr['metadata']['direction']==direction and dr['metadata']['input']==thin(header) and dr['metadata']['entries']==hm['directions'][direction] and dr['metadata']['preparation']==thin(earned[6])
  for iq in range(4):
   tests=earned[start+1+17*iq:start+17+17*iq];column=earned[start+17+17*iq]
   assert [(q['metadata']['row'],q['metadata']['jet']) for q in tests]==[(r,j) for r in range(4) for j in range(4)]
   assert all(q['metadata']['column']==iq and q['metadata']['direction']==direction and q['metadata']['input']==thin(header) and q['metadata']['direction_record']==thin(dr) and q['metadata']['cache']==thin(earned[1+iq]) for q in tests)
   assert column['metadata']['column']==iq and column['metadata']['direction']==direction and column['metadata']['input']==thin(header) and column['metadata']['direction_record']==thin(dr) and column['metadata']['cache']==thin(earned[1+iq])
   assert column['metadata']['normal_tests']==[thin(q) for q in tests] and column['metadata']['reduced_stage_complete'] is False
   columns.append(thin(column));rows.extend(thin(q) for q in tests)
  assert md['direction_record']==thin(dr) and md['columns']==columns and md['normal_tests']==rows
  assert md['mechanical_phase_temporal_response_and_epsilon_feedback_external'] is md['original_six_canonical_restoration_not_evaluated'] is True and md['reduced_stage_complete'] is False
 case=dict(status=EXPECTED_MEASUREMENT_STATUS,input=thin(header),cached_columns=[thin(q) for q in earned[1:5]],readouts=[thin(q) for q in readouts],
  directions=hm['directions'],expected_control_names=hm['expected_control_names'],controls=CONTROL_COUNT,roles=SUCCESS_COUNT,preparation=thin(earned[6]),sheet_cache=thin(earned[5]),normal_terminal=hm['normal_terminal'],finite_terminal=hm['finite_terminal'],join_terminal=hm['join_terminal'],anchor_terminal=hm['anchor_terminal'],mass_terminal=hm['mass_terminal'],chi_recovery_terminal=hm['chi_recovery_terminal'],fixed_rate_partial_only=True,old_current_EOS_action_target_or_solver_replayed=False,original_targets_and_epsilon_unchanged=True,reduced_stage_complete=False,canonical_normal_CMC_finite_state_or_physical_adoption=False,physical_adoption=False)
 case.update(original_failure=dict(source=SOURCE,error=ERROR,receipt=RECEIPT,root_proof=ROOT_FAILURE_PROOF,owner=e['owner'],status='CLOSED_ERROR',missing_original_RESULT=True,
  traceback=e['traceback'],raw_preservation_traceback=e['raw_preservation_traceback'],closing_traceback=e['closing_traceback'],context=e['context'],failed_empty_raw=thin(failed)),
  new_scientific_actions=0,new_controls=0,new_numeric_roles=0,archive_arrays_decoded=False,archive_byte_and_embedded_schema_authority=ROOT_FAILURE_PROOF,
  original_parent_input_sha256=rc['input_sha256'],checkpoint_metadata_authority='Original COMMITs, bound ERROR and root full-seal proof',publication_only=True)
 return case


def main():
 global OWNER
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root guarded release required'
 assert all(v is not None for ref in (SOURCE,ERROR,RECEIPT,ROOT_FAILURE_PROOF) for v in ref),'Natural CLOSED_ERROR and root full-seal proof required before publication'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__).resolve()))
 bind(Path(__file__).name,OWNER['source_sha256']);bind(PROTOCOL,PROTOCOL_SHA)
 # Admission precedes every write; a rejected or unbound parent creates no outputs.
 e,rc,earned,failed=admit_saved();case=recovered_case(e,rc,earned,failed)
 try:
  publish(STEM+'_OWNER_START.json',OWNER)
  publish(STEM+'_MANIFEST.json',dict(owner=OWNER,input_sha256=dict(INPUTS),case=case,qualification=e['qualification']))
  rh=publish(STEM+'_RESULT.json',dict(owner=OWNER,status=RECOVERED_STATUS,case=case,controls=e['controls'],checkpoints=[thin(q) for q in earned],qualification=e['qualification']))
  publish(STEM+'_RECEIPT.json',dict(owner=OWNER,status='CLOSED',closed=datetime.now(timezone.utc).isoformat(),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=e['qualification']))
  print(RECOVERED_STATUS,CONTROL_COUNT,SUCCESS_COUNT,rh);return 0
 except BaseException:
  eh=publish(STEM+'_ERROR.json',dict(owner=OWNER,status='FAILED',traceback=traceback.format_exc(),context=dict(CONTEXT),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),old_failure_preserved=True,new_scientific_actions=0,physical_adoption=False))
  prior=BASE/(STEM+'_RECEIPT.json');publish(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=OWNER,status='CLOSED_ERROR',closed=datetime.now(timezone.utc).isoformat(),error_sha256=eh,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),physical_adoption=False));raise
if __name__=='__main__':raise SystemExit(main())
