"""D022 stateless phase-use check. Reads root envelope artifacts; never writes.
Root supplies independent binding/policy/entry pins to the installer. Every use
re-derives association, runtime/register checks and finality under the held lock.
"""
import copy,hashlib
from pathlib import Path
from snapshot_cx1v001 import Snapshot,Refusal,strict_json
from importer_root_binding_cx1v002 import load
from registered_envelope_runtime_cx1v001 import check as check_open
from final_envelope_evidence_cx1v001 import check as check_final
from register_two_stage_cx1v003 import select_two_stage
from valid_admission_cx1v002 import check_held_lock
from request_guard_cx1v002 import require

def _phase(snapshot,envelope):
 start=envelope['start'];directory=Path(start['path']).parent
 require(directory.is_dir() and directory.resolve()==directory,'ENVELOPE_DIRECTORY')
 paths=sorted(directory.iterdir());ends=[];reports=[]
 for p in paths:
  require(p.is_file() and not p.is_symlink(),'ENVELOPE_UNEXPECTED_ENTRY')
  raw=snapshot.read(p);obj=strict_json(raw)
  require(type(obj) is dict,'ENVELOPE_DOCUMENT')
  schema=obj.get('schema','');pin={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}
  if schema=='UNT_PINNED_INPUT_ENVELOPE_MANIFEST_C2V003':
   if obj.get('label')=='end':ends.append(pin)
   elif obj.get('label')=='start':require(pin==start,'ENVELOPE_FOREIGN_START')
   else:raise Refusal('ENVELOPE_UNKNOWN_MANIFEST_LABEL')
  elif schema=='UNT_PINNED_INPUT_ENVELOPE_COMPARE_C2V003':reports.append(pin)
  elif schema=='UNT_PINNED_INPUT_ENVELOPE_PINSET_C2V003':
   require(pin==envelope['pinset'],'ENVELOPE_FOREIGN_PINSET')
  else:raise Refusal('ENVELOPE_UNKNOWN_DOCUMENT')
 require(len(ends)<=1 and len(reports)<=1,'ENVELOPE_AMBIGUOUS_FINALITY')
 if not ends:
  require(not reports,'ENVELOPE_REPORT_WITHOUT_END');status='PROVISIONAL_ENVELOPE'
 else:
  require(len(reports)==1,'ENVELOPE_END_WITHOUT_COMPARE')
  result=check_final(snapshot,tool_pin=envelope['tool'],start_pin=start,end_pin=ends[0],report_pin=reports[0],pinset_pin=envelope['pinset'])
  require(result['storage_event_kind']=='FINAL_PASS','ENVELOPE_FINAL_FAILED');status='ENVELOPE_FINAL_PASS'
 require(sorted(directory.iterdir())==paths,'ENVELOPE_CHANGED_DURING_CHECK')
 return status

def check_phase(snapshot,*,bound,context,entry):
 """Internal check; bound must come from independently anchored root binding."""
 try:
  prov=entry.get('provenance') or {};admit=prov.get('external_admission') or {};candidate=admit.get('candidate') or {}
  require(prov.get('execution_origin')=='DIRECT_EXTERNAL','PHASE_EXTERNAL_ORIGIN')
  require(admit.get('config_sha256')==context['config_sha256'] and admit.get('cache_id')==context['cache_id'],'PHASE_CONTEXT')
  require(entry.get('key')==candidate.get('key'),'PHASE_ENTRY_KEY')
  selected=select_two_stage(snapshot,register_pin=bound['register_pin'],binding_pin=bound['binding_pin'],context=context,key=entry['key'],spec_pin=candidate.get('spec'))
  reg=selected['entry'];require(reg is not None,'PHASE_UNREGISTERED_IMPORT')
  require(candidate.get('row')==reg['row'] and candidate.get('call_dir')==reg['call_root'] and prov.get('call_dir')==reg['call_root'],'PHASE_IMPORT_ASSOCIATION')
  snapshot.pin(bound['envelope_policy']['start'])
  phase=_phase(snapshot,bound['envelope_policy'])
  # Reuse all D002/D005 checks. Finality does not excuse changed runtime or pins.
  args={k:bound[k] for k in ('register_pin','binding_pin','runtime_policy','envelope_policy')}
  checked=check_open(snapshot,**args,context=context,key=entry['key'],spec_pin=candidate['spec'])
  require(checked['registered'],'PHASE_REGISTER_REFUSED')
  require(_phase(snapshot,bound['envelope_policy'])==phase,'ENVELOPE_STATE_CHANGED')
  return phase
 except (OSError,ValueError,KeyError,TypeError,Refusal) as exc:
  raise Refusal('INVALIDATED_BY_ENVELOPE:'+str(exc)) from exc

def make_phase_use(*,root_binding_pin,expected_policy,expected_entry,held_lock):
 anchors=copy.deepcopy(dict(binding_pin=root_binding_pin,expected_policy=expected_policy,expected_entry=expected_entry))
 require(callable(held_lock),'PHASE_LOCK_CALLBACK')
 def phase_use(ctx,entry):
  lock=held_lock(ctx);check_held_lock(lock,ctx.work_dir);snapshot=Snapshot()
  context={k:getattr(ctx,k) for k in ('config_sha256','cache_id','gate_digest')}
  bound=load(snapshot,**anchors,context=context)
  status=check_phase(snapshot,bound=bound,context=context,entry=entry)
  fresh=Snapshot()
  for p in (anchors['binding_pin'],bound['register_pin'],bound['binding_pin'],bound['envelope_policy']['start']):fresh.pin(p)
  check_held_lock(lock,ctx.work_dir)
  return status
 return phase_use
