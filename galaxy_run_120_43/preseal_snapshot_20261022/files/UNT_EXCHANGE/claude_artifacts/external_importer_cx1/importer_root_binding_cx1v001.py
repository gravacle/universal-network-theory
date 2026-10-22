"""Root-supplied trust-anchor binding; digest integrity is not proof of authorship.
The separate entry must receive expected pins/context through root's invocation,
never derive them from a candidate, cache entry or the binding being checked.
"""
import copy
from register_two_stage_cx1v003 import pin,sha
from request_guard_cx1v002 import require

def load(snapshot,*,binding_pin,expected_policy,expected_entry,context):
 for p in (binding_pin,expected_policy,expected_entry):require(pin(p),'ROOT_ANCHOR_PIN')
 require(type(context) is dict and set(context)=={'config_sha256','cache_id','gate_digest'} and all(sha(v) for v in context.values()),'ROOT_CONTEXT')
 obj=snapshot.document(binding_pin)
 fields={'schema','policy','entry','context','register','binding','runtime','envelope'}
 require(type(obj) is dict and set(obj)==fields and obj['schema']=='CX1_IMPORTER_ROOT_BINDING_V001','ROOT_BINDING_SCHEMA')
 require(obj['policy']==expected_policy and obj['entry']==expected_entry,'ROOT_CODE_BINDING')
 require(obj['context']==context,'ROOT_CONTEXT_BINDING')
 for k in ('register','binding'):require(pin(obj[k]),'ROOT_EVIDENCE_PIN:'+k)
 runtime=obj['runtime'];envelope=obj['envelope']
 require(type(runtime) is dict and set(runtime)=={'campaign_capture','producer','driver','monitor','output_root','freeze','direct_launch'},'ROOT_RUNTIME_FIELDS')
 for k,v in runtime.items():
  if k!='output_root':require(pin(v),'ROOT_RUNTIME_PIN:'+k)
 require(type(runtime['output_root']) is str and runtime['output_root'].startswith('/'),'ROOT_OUTPUT_ROOT')
 require(type(envelope) is dict and set(envelope)=={'tool','start','pinset'} and all(pin(v) for v in envelope.values()),'ROOT_ENVELOPE_FIELDS')
 snapshot.pin(expected_policy);snapshot.pin(expected_entry)
 freeze=snapshot.document(runtime['freeze'])
 require(type(freeze) is dict and freeze.get('policy')==expected_policy and freeze.get('entry')==expected_entry,'ROOT_FREEZE_CODE_BINDING')
 return copy.deepcopy(dict(register_pin=obj['register'],binding_pin=obj['binding'],context=context,runtime_policy=runtime,envelope_policy=envelope))
