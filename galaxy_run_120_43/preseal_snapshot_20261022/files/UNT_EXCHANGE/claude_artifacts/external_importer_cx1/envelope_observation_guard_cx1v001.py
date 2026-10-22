"""D002 prerequisite: authenticate root START/pinset, observe read-only, never produce END."""
from envelope_observation_adapter_cx1v002 import build
from snapshot_cx1v001 import Refusal

def check_observation(snapshot,*,tool_pin,start_pin,pinset_pin,required_pins):
 def need(ok,why):
  if not ok:raise Refusal(why)
 raw=snapshot.pin(tool_pin);m,_=build(raw,tool_pin['path'])
 def signed(pin,schema):
  obj=snapshot.document(pin)
  need(type(obj) is dict and obj.get('schema')==schema,'ENVELOPE_SCHEMA')
  body={k:v for k,v in obj.items() if k!='body_sha256'}
  need(obj.get('body_sha256')==m.sha_b(m.canon(body).encode('ascii')),'ENVELOPE_BODY_SHA')
  need(obj.get('phase')=='L2_DIRECT' and obj.get('unresolved_pins')==[],'ENVELOPE_PHASE_OR_UNRESOLVED')
  return obj
 ps=signed(pinset_pin,m.SCHEMA_PINSET);start=signed(start_pin,m.SCHEMA_MANIFEST)
 need(start.get('label')=='start','START_LABEL')
 need(start.get('pin_set')=={'path':pinset_pin['path'],'file_sha256':pinset_pin['sha256'],'body_sha256':ps['body_sha256']},'START_PINSET_BINDING')
 need(type(required_pins) is list and bool(required_pins),'REQUIRED_COVERAGE')
 required={(p['path'],p['sha256']) for p in required_pins}
 need(len(required)==len(required_pins),'DUPLICATE_REQUIRED_PIN')
 try:
  indexed,_=m._index(start,'start')
  need(required.issubset(indexed),'REQUIRED_PIN_MISSING')
  observation=m.observe(ps,pinset_pin['sha256'],pinset_pin['path'])
  comparison=m.compare_observation(start,observation)
 except m.Refusal as exc:raise Refusal('ENVELOPE_OBSERVATION_REFUSED:'+str(exc)) from exc
 need(not comparison['problems'],'ENVELOPE_OBSERVATION_INVALIDATED')
 return {'prerequisites_only':True,'phase':'L2_DIRECT','observation_label':observation['label'],'final_END':False,'start':start_pin,'pinset':pinset_pin,'notes':comparison['notes']}
