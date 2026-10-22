"""Target-free final-point handoff writer. No scientific execution or streaming.
The expected authority digest is externally published by Claude2, never inferred
from an arbitrary input. Synthetic mode cannot issue an ADMITTED handoff.
"""
import argparse,contextlib,hashlib,json,math,os,re,stat,sys,types
from pathlib import Path
SCHEMA='UNT_STEP4_STEP5_RELEASE_AUTHORITY_CX1V001'
ROOT={'identity':'Claude2','role':'coordinator_and_single_scientific_launch_owner'}
SYNTHETIC={'identity':'SYNTHETIC_FIXTURE','role':'NO_AUTHORITY'}
# Producer source and its exact distinct review are bound by the external root
# publication. The pure verifier replays source/point/certificate semantics from
# immutable input snapshots; a status string alone never grants release.
PRODUCER_ACTIVE=False
PRODUCER_AUDIT_INSTALLED=False
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step5_ngc_route_ab_readiness_cx3')
FILLER={'path':str(BASE/'tools/fill_step5_cx3v003.py'),'sha256':'2348974f469ff2d9177a1f3be88296180bb7c614dad7e820438991abac3ddd6c'}
POLICY={'path':str(BASE/'POLICY_CX3V001.json'),'sha256':'4f0d7d039fcee03fc9e2e1c74624919c77b14e19b101389124864219057e5bbf'}
REGISTRY={'path':str(BASE/'STEP5_REGISTRY_CX3V002.json'),'sha256':'85b1e66aa56d38e455c86d20e9bf5a854e7e3d4a65d3e27adc5eb223b89cf59c'}
CONTRACT={'path':str(BASE/'HANDOFF_CONTRACT_CX3V002.md'),'sha256':'6ae6a0fc406df004e1aaeb425dd4ee3966c797b63f6d775bfb92d9a340b6dc7a'}
PENDING='PENDING_UV_TAIL_CERTIFICATE'
class Refusal(ValueError):pass
def need(ok,reason):
 if ok is not True:raise Refusal(reason)
def keys(obj,names,where):need(type(obj) is dict and set(obj)==set(names),'EXACT_FIELDS_'+where)
def lexical(value):
 need(type(value) is str and Path(value).is_absolute(),'ABSOLUTE_PATH_REQUIRED')
 p=Path(value);low=str(p).casefold();parts=[x.casefold() for x in p.parts]
 need(not any(x.startswith('uvt_') or x=='kmax_a2f10_c5h_run_v001' or x in ('.codex','.codex-alt') for x in parts),'PROTECTED_PATH_REFUSED')
 clean=low.replace('target_free','').replace('target-free','')
 need(not ('ngc3198' in clean and any(x in clean for x in ('observ','velocit','rotmod','target'))),'NGC_TARGET_PATH_REFUSED')
 return p
def safe_path(value):
 p=lexical(value);todo=list(p.parts[1:]);current=Path('/');links=0
 while todo:
  part=todo.pop(0)
  if part in ('','.'):continue
  if part=='..':current=current.parent;continue
  candidate=lexical(str(current/part))
  try:info=os.lstat(candidate)
  except (FileNotFoundError,NotADirectoryError):current=candidate;continue
  if stat.S_ISLNK(info.st_mode):
   links+=1;need(links<=40,'SYMLINK_LOOP_REFUSED');target=os.readlink(candidate)
   lexical(str(Path(target) if os.path.isabs(target) else current/target))
   if os.path.isabs(target):current=Path('/');parts=list(Path(target).parts[1:])
   else:parts=list(Path(target).parts)
   todo=parts+todo
  else:current=candidate
 return lexical(str(current))
def scan(obj):
 if isinstance(obj,dict):
  for k,v in obj.items():
   need(type(k) is str,'STRING_KEYS_REQUIRED');n=k.casefold()
   if k.startswith('/'):lexical(k)
   need(n=='target_free' or not any(t in n for t in ('target','observed','velocit','rotmod','rotation_curve','v_obs','vobs','prediction')),'TARGET_FIELD_REFUSED')
   scan(v)
 elif isinstance(obj,list):
  for x in obj:scan(x)
 elif isinstance(obj,str) and obj.startswith('/'):lexical(obj)
 elif type(obj) is float:need(math.isfinite(obj),'NONFINITE_JSON')
def pairs(items):
 d={}
 for k,v in items:
  need(k not in d,'DUPLICATE_JSON_KEY');d[k]=v
 return d
def finite(s):
 x=float(s);need(math.isfinite(x),'NONFINITE_JSON');return x
def decode(b):
 d=json.loads(b,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda s:(_ for _ in ()).throw(Refusal('NONFINITE_JSON')));scan(d);return d
def encoded(o):return (json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def hexsha(h):need(type(h) is str and re.fullmatch('[0-9a-f]{64}',h) is not None,'SHA256_REQUIRED')
def pin_shape(ref):
 keys(ref,('path','sha256'),'PIN');lexical(ref['path']);hexsha(ref['sha256'])
class Snapshots:
 def __init__(self):self.data={};self.pins={};self.aliases={}
 def raw(self,ref):
  pin_shape(ref);path=str(safe_path(ref['path']))
  if path not in self.data:
   with open(path,'rb') as f:self.data[path]=f.read(2*1024*1024+1)
   need(len(self.data[path])<=2*1024*1024,'INPUT_SIZE_LIMIT')
  b=self.data[path];need(digest(b)==ref['sha256'],'PIN_BYTES_CHANGED');self.pins[path]=ref['sha256'];self.aliases[ref['path']]=b;return b
 def doc(self,ref):return decode(self.raw(ref))
def load_filler(s):
 b=s.raw(FILLER);m=types.ModuleType('_selected_step5_filler');m.__file__=FILLER['path'];exec(compile(b,FILLER['path'],'exec'),m.__dict__);return m

def producer_audit(event,args):
 if not PRODUCER_ACTIVE:return
 if event=='open' or event.startswith(('socket.','subprocess.')) or event in ('import','os.system','os.fork','os.forkpty','os.posix_spawn','os.exec','os.mkdir','os.remove','os.rmdir','os.rename','os.link','os.symlink','os.truncate','os.putenv','os.unsetenv','os.kill','os.killpg'):
  raise Refusal('PRODUCER_IO_OR_PROCESS_REFUSED')
@contextlib.contextmanager
def pure_producer_fence():
 global PRODUCER_ACTIVE,PRODUCER_AUDIT_INSTALLED
 if not PRODUCER_AUDIT_INSTALLED:sys.addaudithook(producer_audit);PRODUCER_AUDIT_INSTALLED=True
 names=('stat','lstat','readlink','listdir','scandir','chdir');original={k:getattr(os,k) for k in names}
 def deny(*a,**kw):raise Refusal('PRODUCER_METADATA_REFUSED')
 before=PRODUCER_ACTIVE
 for k in names:setattr(os,k,deny)
 PRODUCER_ACTIVE=True
 try:yield
 finally:
  PRODUCER_ACTIVE=before
  for k,v in original.items():setattr(os,k,v)
def verify_producer(s,a,r,mode,point_sha):
 source=s.raw(a['producer_pin'])
 inputs=types.MappingProxyType({**s.data,**s.aliases})
 with pure_producer_fence():
  module=types.ModuleType('_root_reviewed_admission_verifier');module.__file__=a['producer_pin']['path']
  exec(compile(source,a['producer_pin']['path'],'exec'),module.__dict__)
  need(getattr(module,'ADMISSION_API',None)=='UNT_STEP4_TARGET_FREE_PRODUCER_API_CX1V001','PRODUCER_API_REQUIRED')
  answer=module.verify_admission(snapshots=inputs,record_pin=dict(a['record_pin']),decision_pin=dict(r['decision_pin']),acceptance_pin=dict(r['acceptance_pin']),mode=mode)
 scan(answer);keys(answer,('api','ok','reasons','point_sha256','provenance','certificate_pins','decision_sha256'),'PRODUCER_ANSWER')
 need(answer=={'api':'UNT_STEP4_TARGET_FREE_PRODUCER_API_CX1V001','ok':True,'reasons':[],'point_sha256':point_sha,'provenance':r['provenance'],'certificate_pins':r['certificate_pins'],'decision_sha256':r['decision_pin']['sha256']},'PRODUCER_SCIENTIFIC_VERIFICATION_REQUIRED')
 return answer

def checked_v007(s,v,synthetic,authority):
 keys(v,('seal','verdict','prereg','compare','addendum','case_block'),'V007')
 need(Path(v['compare']['path']).suffix=='.py' and Path(v['addendum']['path']).suffix in ('.md','.txt'),'V007_SOURCE_TEXT_TYPES_REQUIRED')
 for k,ref in v.items():
  if k in ('compare','addendum'):s.raw(ref)
  else:s.doc(ref)
 seal=s.doc(v['seal']);report=s.doc(v['verdict']);pre=s.doc(v['prereg'])
 # Frozen source documents remain opaque; only the minimal target-free semantic
 # verdict/registration view is admitted by this proposed producer contract.
 keys(seal,('schema','sealed_by','prereg','compare','frozen_addendum','verdict','case_block'),'SEAL')
 need(seal['schema']=='UNT_V007_ADOPTION_SEAL_VIEW_CX1V001' and seal['sealed_by']==authority,'SEALED_V007_REQUIRED')
 for k in ('prereg','compare','verdict','case_block'):need(seal[k]==v[k],'SEALED_V007_BINDING')
 need(seal['frozen_addendum']==v['addendum'],'SEALED_V007_BINDING')
 keys(report,('schema','test_mode','decision','script_sha256','prereg','case_block'),'V007_VERDICT')
 need(report['schema']=='UNT_V007_VERDICT_VIEW_CX1V001','V007_VERDICT_SCHEMA')
 keys(report['decision'],('tests_read','outcome'),'V007_DECISION')
 need(report['test_mode'] is synthetic and report['decision']=={'tests_read':True,'outcome':'ADOPT_TAIL'},'SEALED_ADOPT_TAIL_REQUIRED')
 need(report['script_sha256']==v['compare']['sha256'] and report['prereg']==v['prereg'] and report['case_block']==v['case_block'],'V007_VERDICT_BINDING')
 keys(pre,('schema','binding_inputs'),'PREREG_VIEW');keys(pre['binding_inputs'],('case_block',),'PREREG_BINDING')
 need(pre['schema']=='UNT_V007_PREREG_VIEW_CX1V001' and pre['binding_inputs']['case_block']==v['case_block'],'V007_PREREG_BINDING')
 return v['verdict']

def prepare(authority_path,expected_sha,output_dir,*,synthetic_dry_only=False):
 need(type(synthetic_dry_only) is bool,'SYNTHETIC_FLAG_BOOL')
 s=Snapshots();anchor={'path':str(authority_path),'sha256':expected_sha};a=s.doc(anchor)
 keys(a,('schema','mode','authority','writer_pin','record_pin','rule_pin','producer_pin','producer_review_pin','selected_registry_pin','driver_branch','driver_acceptance_pin'),'AUTHORITY')
 mode='SYNTHETIC_DRY_ONLY' if synthetic_dry_only else 'PRODUCTION';owner=SYNTHETIC if synthetic_dry_only else ROOT
 need(a['schema']==SCHEMA and a['mode']==mode and a['authority']==owner,'EXTERNAL_ROOT_PUBLICATION_REQUIRED')
 need(a['writer_pin']=={'path':str(Path(__file__)),'sha256':digest(s.raw(a['writer_pin']))},'WRITER_IDENTITY')
 need(a['selected_registry_pin']==REGISTRY,'SELECTED_STEP5_REGISTRY_REQUIRED')
 registry=s.doc(REGISTRY);policy=s.doc(POLICY);s.raw(CONTRACT)
 need(registry['selected_filler']==FILLER and registry['policy']==POLICY and registry['handoff_contract']==CONTRACT,'SELECTED_CONSUMER_BINDING')
 r=s.doc(a['record_pin']) # recursively scan before following any record refs
 need(type(a['producer_pin']) is dict and type(a['producer_review_pin']) is dict,'FINAL_EXPORT_PRODUCER_PENDING')
 producer=s.raw(a['producer_pin']);review=s.doc(a['producer_review_pin'])
 keys(review,('schema','mode','verdict','producer_pin','record_schema','blocking_findings','reviewer','semantic_scope'),'PRODUCER_REVIEW')
 need(review['schema']=='UNT_STEP4_TARGET_FREE_PRODUCER_REVIEW_CX1V001' and review['mode']==mode and review['verdict']=='PASS' and review['producer_pin']==a['producer_pin'] and review['record_schema']=='UNT_STEP4_SCIENTIFIC_POINT_ADMISSION_CX1V001' and review['blocking_findings']==[],'PRODUCER_REVIEW_REQUIRED')
 need(type(review['reviewer']) is str and review['reviewer'] not in ('','Codex1'),'DISTINCT_PRODUCER_REVIEW_REQUIRED')
 need(review['semantic_scope']==['NATIVE_RECTANGLE_MEMBERSHIP_RECOMPUTED','COMPLETE_DOUBLE_REPLAY','NATIVE_RECORD_REGISTRY_VERIFIED','GUARDED_ADMISSION_PROVENANCE','POST_STATE_CERTIFICATES_VERIFIED','NGC_POINT_CERTIFICATES_VERIFIED','UNCHANGED_NATIVE_COORDINATES'],'PRODUCER_REVIEW_SCOPE_REQUIRED')
 rule=s.doc(a['rule_pin'])
 keys(rule,('schema','mode','authority','release_scope','requires_full_decision','pointwise_streaming_allowed','coordinate_pin'),'RULE')
 need(rule=={'schema':'UNT_STEP4_STEP5_RELEASE_RULE_CX1V001','mode':mode,'authority':owner,'release_scope':'FULL_FINAL_DECISION','requires_full_decision':True,'pointwise_streaming_allowed':False,'coordinate_pin':policy['coordinates']},'FULL_FINAL_DECISION_RULE_REQUIRED')
 keys(r,('schema','mode','status','target_free','coordinate_pin','point','v007','decision_pin','acceptance_pin','certificate_pins','certificate_evidence_pin','scientific_evidence_pin','provenance'),'ADMISSION_RECORD')
 need(r['schema']=='UNT_STEP4_SCIENTIFIC_POINT_ADMISSION_CX1V001' and r['mode']==mode and r['status']=='SCIENTIFICALLY_ADMITTED' and r['target_free'] is True,'SCIENTIFIC_ADMITTED_POINT_REQUIRED')
 need(r['coordinate_pin']==policy['coordinates'],'COORDINATE_CONTRACT_MISMATCH')
 v007=checked_v007(s,r['v007'],synthetic_dry_only,owner)
 d=s.doc(r['decision_pin'])
 keys(d,('schema','mode','target_free','scope','engine_status','engine_ok','coordinate_pin','admitted_points','replay','registry','blocking_findings'),'FINAL_DECISION')
 need(d['schema']=='UNT_STEP4_FINAL_DECISION_TARGET_FREE_VIEW_CX1V001' and d['mode']==mode and d['target_free'] is True and d['scope']=='FULL_FINAL_DECISION' and d['engine_status']=='COMPLETE' and d['engine_ok'] is True and d['blocking_findings']==[],'FULL_FINAL_DECISION_REQUIRED')
 need(d['coordinate_pin']==r['coordinate_pin'],'FINAL_COORDINATE_BINDING')
 keys(d['replay'],('complete_runs','match','canonical_run_sha256'),'REPLAY');hexsha(d['replay']['canonical_run_sha256'])
 need(d['replay']['complete_runs']==2 and type(d['replay']['complete_runs']) is int and d['replay']['match'] is True,'COMPLETE_DOUBLE_REPLAY_REQUIRED')
 keys(d['registry'],('record_file_sha256','record_sha256','registry_line_sha256','verify_ok','registry_chain_ok','verify_reasons'),'REGISTRY_VIEW')
 for k in ('record_file_sha256','record_sha256','registry_line_sha256'):hexsha(d['registry'][k])
 need(d['registry']['verify_ok'] is True and d['registry']['registry_chain_ok'] is True and d['registry']['verify_reasons']==[],'VERIFIED_NATIVE_REGISTRY_REQUIRED')
 F=load_filler(s);coordinates=s.doc(policy['coordinates'])
 try:
  F.validate_points({'admitted_points':d['admitted_points']},coordinates)
  F.validate_points({'admitted_points':[r['point']]},coordinates)
 except F.Refusal as e:raise Refusal('CONSUMER_COORDINATE_CONTRACT: '+str(e)) from None
 need(type(r['point']) is dict and sum(canonical(p)==canonical(r['point']) for p in d['admitted_points'])==1,'POINT_NOT_IN_FINAL_ADMITTED_SET')
 keys(r['point'],('log_index','u','theta_natural'),'POINT')
 point_sha=digest(canonical(r['point']))
 p=r['provenance'];keys(p,('native_record_sha256','native_registry_line_sha256','replay_run_sha256','guarded_plan_sha256','guarded_admission_sha256','record_producer_pin'),'PROVENANCE')
 for k in ('native_record_sha256','native_registry_line_sha256','replay_run_sha256','guarded_plan_sha256','guarded_admission_sha256'):hexsha(p[k])
 need(p['native_record_sha256']==d['registry']['record_file_sha256'] and p['native_registry_line_sha256']==d['registry']['registry_line_sha256'] and p['replay_run_sha256']==d['replay']['canonical_run_sha256'] and p['record_producer_pin']==a['producer_pin'],'FINAL_SOURCE_PROVENANCE_BINDING')
 acceptance=s.doc(r['acceptance_pin'])
 keys(acceptance,('schema','mode','phase','ok','blockers','point_sha256','decision_pin','guarded_plan_sha256','guarded_admission_sha256','v007_verdict_pin','post_state_bundle_pin','certificate_pins'),'ACCEPTANCE_VIEW')
 need(acceptance['schema']=='UNT_STEP4_POST_STATE_ACCEPTANCE_VIEW_CX1V001' and acceptance['mode']==mode and acceptance['phase']=='acceptance' and acceptance['ok'] is True and acceptance['blockers']==[],'POST_STATE_ACCEPTANCE_REQUIRED')
 need(acceptance['point_sha256']==point_sha and acceptance['decision_pin']==r['decision_pin'] and acceptance['v007_verdict_pin']==v007 and all(acceptance[k]==p[k] for k in ('guarded_plan_sha256','guarded_admission_sha256')),'ACCEPTANCE_POINT_PROVENANCE_BINDING')
 certs=r['certificate_pins'];keys(certs,('eps_certificate','lo_certificate'),'CERTIFICATE_PINS')
 need(acceptance['certificate_pins']==certs,'CERTIFICATE_ACCEPTANCE_BINDING')
 bundle=s.doc(acceptance['post_state_bundle_pin'])
 keys(bundle,('schema','mode','target_free','point_sha256','phase','certificate_pins'),'POST_STATE_BUNDLE_VIEW')
 need(bundle=={'schema':'UNT_STEP4_POST_STATE_BUNDLE_VIEW_CX1V001','mode':mode,'target_free':True,'point_sha256':point_sha,'phase':'acceptance','certificate_pins':certs},'POST_STATE_BUNDLE_BINDING')
 evidence=s.doc(r['certificate_evidence_pin'])
 keys(evidence,('schema','mode','target_free','point_sha256','certificate_pins','verified','scope','blockers'),'CERTIFICATE_EVIDENCE')
 need(evidence=={'schema':'UNT_STEP5_POINT_CERTIFICATE_EVIDENCE_CX1V001','mode':mode,'target_free':True,'point_sha256':point_sha,'certificate_pins':certs,'verified':True,'scope':'NGC91_K32_MS96','blockers':[]},'POINT_CERTIFICATE_EVIDENCE_REQUIRED')
 for kind,ref in certs.items():
  # Proof formats belong to the exact reviewed pure producer, which must parse
  # their native schemas and recompute their validity. Scan each JSON first;
  # neither proof data nor arbitrary fields are copied into the handoff.
  s.doc(ref)
 s.doc(r['scientific_evidence_pin']) # native schema and predicate belong to reviewed producer
 verify_producer(s,a,r,mode,point_sha)
 branch=a['driver_branch'];need(branch in policy['drivers'],'UNREGISTERED_DRIVER_BRANCH')
 if branch=='r007':
  need(not synthetic_dry_only,'SYNTHETIC_DRIVER_ACCEPTANCE_REFUSED');s.raw(a['driver_acceptance_pin'])
 else:need(a['driver_acceptance_pin'] is None,'FALLBACK_ACCEPTANCE_MUST_BE_NULL')
 out=safe_path(str(output_dir));need(out.parent.is_dir() and not os.path.lexists(out),'NEW_OUTPUT_DIRECTORY_REQUIRED')
 export={'schema':'UNT_STEP4_TARGET_FREE_ADMITTED_EXPORT_CX3V001','mode':'SYNTHETIC_DRY_ONLY' if synthetic_dry_only else 'ADMITTED','target_free':True,'coordinate_pin':policy['coordinates'],'admitted_points':[r['point']]}
 eb=encoded(export);export_pin={'path':str(out/'TARGET_FREE_EXPORT_CX1V001.json'),'sha256':digest(eb)}
 handoff={'schema':'UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001','mode':export['mode'],'source_export_pin':export_pin,'log_index':r['point']['log_index'],'policy_pin':POLICY,'driver_branch':branch,'driver_acceptance_pin':a['driver_acceptance_pin'],'v007_adoption_pin':None if synthetic_dry_only else v007,'root_admission':'SYNTHETIC_DRY_ONLY' if synthetic_dry_only else policy['root_admission_required'],'certificate_pins':{k:PENDING for k in certs} if synthetic_dry_only else certs}
 hb=encoded(handoff);handoff_pin={'path':str(out/'HANDOFF_CX1V001.json'),'sha256':digest(hb)}
 receipt={'schema':'UNT_STEP4_STEP5_WRITER_RECEIPT_CX1V001','mode':mode,'launch_authorized':False,'release_scope':'FULL_FINAL_DECISION','external_authority_pin':anchor,'record_pin':a['record_pin'],'producer_pin':a['producer_pin'],'producer_review_pin':a['producer_review_pin'],'decision_pin':r['decision_pin'],'acceptance_pin':r['acceptance_pin'],'point_sha256':point_sha,'source_snapshots':s.pins,'export_pin':export_pin,'handoff_pin':handoff_pin,'production_scientific_admission':'UNTESTED' if synthetic_dry_only else 'ROOT_PRODUCER_BOUND'}
 return {'TARGET_FREE_EXPORT_CX1V001.json':eb,'HANDOFF_CX1V001.json':hb,'WRITER_RECEIPT_CX1V001.json':encoded(receipt)},receipt

def write_point(authority_path,expected_sha,output_dir,*,synthetic_dry_only=False):
 payloads,receipt=prepare(authority_path,expected_sha,output_dir,synthetic_dry_only=synthetic_dry_only)
 out=safe_path(str(output_dir));out.mkdir(exist_ok=False)
 for name,b in payloads.items():
  with (out/name).open('xb') as f:f.write(b)
 return receipt

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--authority',required=True);p.add_argument('--expected-sha256',required=True);p.add_argument('--output-dir',required=True);p.add_argument('--synthetic-dry-only',action='store_true');a=p.parse_args()
 try:r=write_point(a.authority,a.expected_sha256,a.output_dir,synthetic_dry_only=a.synthetic_dry_only)
 except (Refusal,OSError,KeyError,TypeError,ValueError) as e:p.exit(2,'REFUSED: '+str(e)+'\n')
 print(json.dumps({'mode':r['mode'],'launch_authorized':False,'handoff_pin':r['handoff_pin']}))
if __name__=='__main__':main()
