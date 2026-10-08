"""HELD JSON-only finalization of completed42198 science; no payload/arithmetic replay."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
STEM='SAVED_MECHANICAL_COEFFICIENT_FORWARD_FINALIZATION_V001'
PROTOCOL=('SAVED_MECHANICAL_COEFFICIENT_FORWARD_FINALIZATION_V001.md','3da1b90fbb1d5a5363049569340c5d16c6480d251f8c99dbd3adaaf5ffd99f24')
SOURCE=('cross_u_candidate_mechanical_coefficient_forward_contacts_v002.py','f4cca61afeec9a093cb38448009e9050d5da0104fa110e42e43280efaa7ac02c')
ORIGINAL='CROSS_U_CANDIDATE_MECHANICAL_COEFFICIENT_FORWARD_CONTACTS_V002'
MANIFEST=(ORIGINAL+'_MANIFEST.json','2b0141ee2b4c19ad0cca91386e05f30ba423771ab219803ba5cc6a2c723df100')
OUTPUT_PROOF=('ROOT_CLOSED_SAVED_COEFFICIENT_FORWARD_OUTPUT_ONLY_SEALS_V001.json','8bb868fe40b653552b722d1fd1d0dbbde778c81c16d6774b9e8c90a59e160e6e')
FINAL=(ORIGINAL+'_00522_PREPARATION.npz.COMMIT.json','7fcf3157a39c40665153f77cab5a19bf901938256ec8332ecf057bf5671c6b5a')
ALL_INPUT_PROOF=(None,None,'ROOT_CLOSED_SAVED_COEFFICIENT_FORWARD_ALL_INPUT_SEALS_VERIFIED')
INPUTS={};OUTPUTS={};OWNER=None

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()

def bind(ref):
 name,digest=ref;assert isinstance(name,str) and isinstance(digest,str) and len(digest)==64
 p=BASE/name;assert sha(p)==digest,name;INPUTS[name]=digest;return json.loads(p.read_text()) if name.endswith('.json') else None

def publish(suffix,value):
 name=STEM+'_'+suffix+'.json';p=BASE/name;data=(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);digest=sha(p);OUTPUTS[name]=digest;return digest

def admit_saved():
 bind(SOURCE);bind(PROTOCOL);m=bind(MANIFEST);out=bind(OUTPUT_PROOF);final=bind(FINAL);inp=bind(ALL_INPUT_PROOF[:2]);md=final['metadata'];owner=out['scientific_owner']
 assert owner['pid']==42198 and owner['source_sha256']==SOURCE[1] and m['owner']==md['owner']==inp['scientific_owner']==owner
 assert out['status']=='ROOT_CLOSED_SAVED_COEFFICIENT_FORWARD_OUTPUT_ONLY_SEALS_AUTHENTICATED' and out['original_worker_exit_code']==inp['original_observed_exit_code']==1
 assert out['all_output_seals_verified'] is True and out['all_role_owners_verified'] is True and out['roles']==523 and len(out['verified_output_sha256'])==1046
 assert inp['status']==ALL_INPUT_PROOF[2] and inp['all_input_seals_verified'] is True and inp['recovery_publication_ready'] is True
 assert inp['manifest_sha256']==MANIFEST[1] and inp['input_count_expected']==inp['input_count_verified']==len(m['input_sha256'])==518 and inp['verified_input_sha256']==m['input_sha256']
 assert all(not (BASE/(ORIGINAL+'_'+n+'.json')).exists() for n in ('RESULT','RECEIPT','ERROR','ERROR_RECEIPT'))
 assert md['publication_role']=='PREPARATION' and md['failed'] is False and md['schema']=={} and md['cases']==out['cases'] and [q['case'] for q in md['cases']]==[0,1]
 assert out['verified_output_sha256'][FINAL[0]]==FINAL[1] and out['verified_output_sha256'][final['file']]==final['sha256']
 for q in (md['input'],md['prepared']):assert all(out['verified_output_sha256'][q[k]]==q[h] for k,h in (('file','sha256'),('commit_file','commit_sha256')))
 expected=dict(INPUT=1,CACHE_COPY=4,PREPARED=1,DIRECTION=2,ACTION_COLUMN=8,ACTION_WEAK=2,ACTION_POSITIVE=2,PROXY_CHUNK=240,PROXY_COLUMN=8,PROXY_WEAK=2,PROXY_POSITIVE_CHUNK=240,PROXY_POSITIVE_COLUMN=8,PROXY_POSITIVE=2,ASSOCIATION=2,PREPARATION=1)
 assert out['role_census']==expected and sum(expected.values())==523
 controls=out['controls'];names=['NEW_coefficient_forward_case%d_'%i+s for i in (0,1) for s in ('all403340_vector_association','independent_dual_dot_association')]
 assert len(controls)==4 and [q['name'] for q in controls]==names and [q['ordinal'] for q in controls]==list(range(4))
 assert out['original_four_sampled_controls_passed'] is True and all(q['passed'] is True and q['tolerance']==2e-11 and math.isfinite(q['error']) and 0<=q['error']<=2e-11 for q in controls)
 assert md['original2e11_unchanged'] is True and md['original_six_canonical_gates_evaluated'] is False and md['uniform_association_adjoint_inverse_or_physics'] is False
 assert md['old_component_inverse_failure_repaired'] is False and md['physical_adoption'] is False and out['physical_adoption'] is False and out['uniform_association_or_inverse_qualified'] is False
 assert len(md['qualification'])==9 and all(v is False for v in md['qualification'].values()) and out['numerical_actions_replayed'] is False
 prep=dict(file=final['file'],sha256=final['sha256'],commit_file=FINAL[0],commit_sha256=FINAL[1])
 case=dict(original_owner=owner,original_observed_exit_code=1,missing_original_RESULT_RECEIPT_ERROR=True,input=md['input'],prepared=md['prepared'],preparation=prep,cases=md['cases'],roles=523,role_census=expected,new_controls=0,new_scientific_actions=0,new_numeric_roles=0,original_six_canonical_gates_evaluated=False,uniform_association_adjoint_or_inverse_qualified=False,physical_adoption=False)
 return case,controls,md['qualification']

def main():
 global OWNER
 assert AUTHOR_DRAFT is False and all(x is not None for x in ALL_INPUT_PROOF),'Root review, full518 input proof and release required before I/O'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused recovery namespace required'
 OWNER=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__).resolve()))
 try:
  publish('OWNER_START',OWNER);INPUTS[Path(__file__).name]=OWNER['source_sha256'];case,controls,qualification=admit_saved()
  publish('MANIFEST',dict(owner=OWNER,source_refs=dict(source=SOURCE,manifest=MANIFEST,output_proof=OUTPUT_PROOF,all_input_proof=ALL_INPUT_PROOF,final_commit=FINAL),input_sha256=dict(INPUTS),original_role_outputs_inherited_in_place=True,new_scientific_actions=0))
  rh=publish('RESULT',dict(owner=OWNER,status='NEW_MECHANICAL_COEFFICIENT_FORWARD_TWO_DIRECTION_ASSOCIATIONS_SAVED_RECOVERED',earned_original_status='NEW_MECHANICAL_COEFFICIENT_FORWARD_TWO_DIRECTION_ASSOCIATIONS_PASS',case=case,controls=controls,qualification=qualification))
  publish('RECEIPT',dict(owner=OWNER,status='CLOSED',closed=datetime.now(timezone.utc).isoformat(),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,original_observed_exit_code=1,new_scientific_actions=0,qualification=qualification));print('SAVED_RECOVERED',523,4,rh);return 0
 except BaseException:
  eh=publish('ERROR',dict(owner=OWNER,status='FAILED',traceback=traceback.format_exc(),input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),new_scientific_actions=0,original_failure_preserved=True,physical_adoption=False));prior=BASE/(STEM+'_RECEIPT.json')
  publish('ERROR_RECEIPT' if prior.exists() else 'RECEIPT',dict(owner=OWNER,status='CLOSED_ERROR',closed=datetime.now(timezone.utc).isoformat(),error_sha256=eh,prior_receipt_sha256=sha(prior) if prior.exists() else None,input_sha256=dict(INPUTS),output_sha256=dict(OUTPUTS),new_scientific_actions=0,physical_adoption=False));raise
if __name__=='__main__':raise SystemExit(main())
