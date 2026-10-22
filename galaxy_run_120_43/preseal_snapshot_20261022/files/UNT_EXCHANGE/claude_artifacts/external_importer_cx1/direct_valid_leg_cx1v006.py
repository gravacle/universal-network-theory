"""D021 VALID leg; called only after authenticated natural registered observation.
No launch API. Acceptance output directories are deterministic and exclusive.
Interrupted/foreign passes refuse; only one INCOMPLETE pass may be retried.
"""
import copy
from pathlib import Path
from snapshot_cx1v001 import Snapshot
from request_guard_cx1v002 import require
from direct_accept_prepare_cx1v004 import prepare
from acceptance_loader_cx1v002 import load_acceptance,LO,HANDOFF
from direct_handoff_writer_cx1v004 import write_handoff
from valid_admission_cx1v002 import validate_valid,check_held_lock

ACCEPTED=('ACCEPTED','ACCEPTED_PASS_FLAGGED')

def complete(orch,*,lock,modules,wrapper,accept_entry_pin,deps_pin,records_root,wave_dir,plan,candidate):
 ctx=orch.ctx;check_held_lock(lock,ctx.work_dir);s=Snapshot()
 dep_record=s.document(deps_pin)
 require(dep_record.get('schema')=='H3_CAMPAIGN_ACCEPTANCE_DEPS_C2V001' and dep_record.get('status')=='ROOT_FILLED' and dep_record.get('synthetic') is not True,'VALID_LEG_ROOT_DEPS_REQUIRED')
 calls=[c for c in plan['calls'] if c.get('call_index')==candidate.get('call_index')]
 require(len(calls)==1,'VALID_LEG_UNREQUESTED')
 call=calls[0];candidate=copy.deepcopy(candidate)
 require(call['key']==candidate['key'] and call['spec_sha256']==candidate['spec']['sha256'],'VALID_LEG_IDENTITY')
 direct=s.document(candidate['direct_plan'])
 matches=[c for c in direct.get('calls',[]) if c.get('point_key')==candidate['key']]
 require(len(matches)==1,'VALID_LEG_PLAN_KEY')
 dc=matches[0]
 require(dc.get('row')==candidate['row'] and dc.get('spec')==candidate['spec'],'VALID_LEG_PLAN_ROW_SPEC')
 require('theta' not in candidate or candidate['theta']==call['theta'],'VALID_LEG_THETA_CHANGED')
 require('case' not in candidate or candidate['case']==dc.get('case'),'VALID_LEG_CASE_CHANGED')
 candidate.update(theta=copy.deepcopy(call['theta']),case=dc.get('case'))
 directory=Path(candidate['call_dir'])
 candidate['receipt']={'path':str(directory/'RECEIPT.json'),'sha256':s.hash(directory/'RECEIPT.json')}
 root=Path(records_root)
 require(root.is_absolute() and root.resolve()==root and root.is_relative_to(Path(HANDOFF['path']).parents[2]),'VALID_LEG_RECORD_ROOT')
 # Root must be an installer-owned records directory under claude_artifacts.
 root=root/candidate['key']
 passes=wrapper.acceptance_passes(directory)
 require(len(passes)<=2,'VALID_LEG_PASS_LIMIT')
 records=[]
 for i,name in enumerate(passes,1):
  rp=root/('PASS_%03d'%i)/'ACCEPTANCE_RECORD.json'
  require(rp.is_file() and not rp.is_symlink(),'VALID_LEG_INTERRUPTED_OR_FOREIGN_PASS')
  ref={'path':str(rp),'sha256':s.hash(rp)};rec=s.document(ref)
  require(rec.get('schema')=='DDO154_TAIL_ACCEPTANCE_RECORD_C2V001' and rec.get('handoff')==HANDOFF,'VALID_LEG_RECORD_SCHEMA')
  require(rec.get('call_dir')==str(directory) and rec.get('tailstate_dir')==str(directory/name),'VALID_LEG_RECORD_CUSTODY')
  require(rec.get('pins')==s.document(deps_pin).get('deps'),'VALID_LEG_RECORD_DEPS')
  records.append((rec,ref))
 if len(records)==2:require(records[0][0].get('reading')=='INCOMPLETE','VALID_LEG_FIRST_PASS_NOT_INCOMPLETE')
 if records and records[-1][0].get('reading') not in ACCEPTED:
  require(len(records)==1 and records[0][0].get('reading')=='INCOMPLETE','VALID_LEG_FAILURE_READING_STANDS')
 if not records or records[-1][0].get('reading') not in ACCEPTED:
  prep=prepare(orch,snapshot=s,lock=lock,modules=modules,wrapper=wrapper,entry_pin=accept_entry_pin,call=call,candidate=candidate,deps_pin=deps_pin,expected_lo=LO,first_pass=records[0][1] if records else None)
  tr=ctx.cfg['tail_readiness'];guard={'path':wrapper.G.__file__,'sha256':s.hash(wrapper.G.__file__)}
  output=root/('PASS_%03d'%(len(records)+1))
  with load_acceptance(snapshot=s,record_pin=deps_pin,expected_enumerator=tr['state_enumerator'],expected_guard=guard,expected_producers=tr['approved_certificate_producers'],output_roots=[directory,output]) as loaded:
   policy=dict(loaded.policy,receipt=prep['receipt'],prelaunch_bundle=prep['policy']['prelaunch_bundle'])
   rec,ref=loaded.handoff.accept_call(call_dir=str(directory),spec=call['spec'],deps=loaded.deps,policy=policy,records_dir=str(output),mode='guard')
  records.append((rec,ref))
 rec,ref=records[-1]
 require(rec.get('reading') in ACCEPTED,'VALID_LEG_ACCEPTANCE_NOT_ACCEPTED:'+str(rec.get('reading')))
 require('acceptance' not in candidate or candidate['acceptance']==ref,'VALID_LEG_ACCEPTANCE_CHANGED')
 require('bundle' not in candidate or candidate['bundle']==rec.get('bundle'),'VALID_LEG_BUNDLE_CHANGED')
 candidate.update(acceptance=ref,bundle=rec.get('bundle'))
 if len(records)==2:candidate['first_acceptance']=records[0][1]
 write_handoff(orch,lock=lock,chain_modules=modules,wrapper_module=wrapper,call=call,candidate=candidate)
 verified=validate_valid(orch,lock=lock,chain_modules=modules,wave_dir=wave_dir,plan=plan,candidate=candidate)
 check_held_lock(lock,ctx.work_dir)
 return {'candidate':candidate,'verified':verified,'reading':rec['reading']}
