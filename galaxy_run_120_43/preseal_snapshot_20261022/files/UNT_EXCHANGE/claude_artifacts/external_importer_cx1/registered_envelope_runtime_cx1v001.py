"""Joint D002/D005 prerequisites; caller authenticates root policy pins.
No liveness, acceptance, admission, launch or final-phase invalidation decision.
"""
from registered_runtime_cx1v005 import check_registered_runtime
from envelope_observation_guard_cx1v001 import check_observation
from request_guard_cx1v002 import require

def check(snapshot,*,register_pin,binding_pin,context,key,spec_pin,runtime_policy,envelope_policy):
 require(type(envelope_policy) is dict and set(envelope_policy)=={'tool','start','pinset'},'ROOT_ENVELOPE_POLICY')
 runtime=check_registered_runtime(snapshot,register_pin=register_pin,binding_pin=binding_pin,context=context,key=key,spec_pin=spec_pin,runtime_policy=runtime_policy)
 if not runtime['registered']:return runtime
 register=snapshot.document(register_pin);freeze=snapshot.document(runtime_policy['freeze'])
 required=[register_pin,runtime_policy['driver'],runtime_policy['monitor'],freeze['policy'],freeze['entry']]
 for entry in register['entries']:
  required.extend(entry[k] for k in ('spec','launcher','guard','binder','dbp','runtime_capture'))
 unique={(p['path'],p['sha256']):p for p in required}
 # No candidate-controlled coverage list; all seven registered calls are covered.
 envelope=check_observation(snapshot,tool_pin=envelope_policy['tool'],start_pin=envelope_policy['start'],pinset_pin=envelope_policy['pinset'],required_pins=[unique[k] for k in sorted(unique)])
 return {'prerequisites_only':True,'registered':True,'runtime':runtime,'envelope':envelope,'required_pin_count':len(unique),'admission_authorized':False}
