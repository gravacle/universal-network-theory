"""D002 pure phase-state projection; trusted event ingestion and enforcement are NOT implemented.
An append-only invalidation event invalidates all prior admissions without rewriting them.
The caller must serialize event ingestion and every use under the campaign lock.
"""
from snapshot_cx1v001 import Refusal

def project(events,phase_id):
 def need(ok,why):
  if not ok:raise Refusal(why)
 need(type(phase_id) is str and bool(phase_id),'PHASE_ID')
 need(type(events) is list,'EVENT_LIST')
 admitted={};consumed=set();final=None;invalid=False
 for i,event in enumerate(events):
  need(type(event) is dict and set(event)=={'seq','phase_id','kind','subject'},'EVENT_SHAPE')
  need(type(event['seq']) is int and event['seq']==i,'EVENT_SEQUENCE')
  need(event['phase_id']==phase_id,'PHASE_MISMATCH')
  kind=event['kind'];subject=event['subject']
  need(type(subject) is str,'SUBJECT_TYPE')
  if kind=='ADMIT':
   need(not invalid and final is None,'PHASE_CLOSED')
   need(bool(subject) and subject not in admitted,'DUPLICATE_OR_EMPTY_IMPORT')
   admitted[subject]='PROVISIONAL_ENVELOPE'
  elif kind=='CONSUME':
   need(not invalid,'INVALIDATED_BY_ENVELOPE')
   need(subject in admitted,'UNKNOWN_IMPORT')
   consumed.add(subject)
  elif kind in ('FINAL_PASS','FINAL_INVALIDATE','FINAL_REFUSAL'):
   need(subject=='','FINAL_SUBJECT')
   need(final is None,'DUPLICATE_FINAL')
   final=kind;invalid=kind!='FINAL_PASS'
  else:raise Refusal('UNKNOWN_EVENT')
 state={key:('INVALIDATED_BY_ENVELOPE' if invalid else 'ENVELOPE_FINAL_PASS' if final=='FINAL_PASS' else value) for key,value in admitted.items()}
 return dict(phase_id=phase_id,imports=state,final=final,freeze_campaign=invalid and bool(consumed),refuse_further_use=invalid,root_escalation_required=invalid,projection_only=True)

def require_use(events,phase_id,import_id):
 state=project(events,phase_id)
 if state['refuse_further_use']:raise Refusal('INVALIDATED_BY_ENVELOPE')
 if import_id not in state['imports']:raise Refusal('UNKNOWN_IMPORT')
 return state['imports'][import_id]
