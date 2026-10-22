"""0843 two-stage binding prerequisite. Root policy must authenticate BOTH input pins.
No unrequested runtime/spec contents are opened; no status can authorize ingestion.
"""
from pathlib import Path
from request_guard_cx1v002 import require

def sha(v):return type(v) is str and len(v)==64 and all(c in '0123456789abcdef' for c in v)
def pin(v):return type(v) is dict and set(v)=={'path','sha256'} and type(v['path']) is str and v['path'].startswith('/') and sha(v['sha256'])

def select_two_stage(snapshot, *, register_pin, binding_pin, context, key, spec_pin):
 require(pin(register_pin) and pin(binding_pin),'L2_REGISTER_PINS')
 require(type(context) is dict and set(context)=={'config_sha256','cache_id','gate_digest'} and all(sha(v) for v in context.values()),'L2_CONTEXT')
 binding=snapshot.document(binding_pin)
 require(type(binding) is dict and set(binding)=={'schema','register','context','campaign_capture','utc','interpreter','freeze'} and binding['schema']=='SPECULATIVE_REGISTER_BINDING_L2_V001','L2_BINDING_SCHEMA')
 require(binding['register']==register_pin and binding['context']==context,'L2_BINDING_MISMATCH')
 require(pin(binding['campaign_capture']),'L2_CAMPAIGN_CAPTURE_PIN')
 reg=snapshot.document(register_pin)
 require(type(reg) is dict and set(reg)=={'schema','entries'} and reg['schema']=='SPECULATIVE_REGISTER_L2_V001','L2_REGISTER_SCHEMA')
 entries=reg['entries'];require(type(entries) is list and len(entries)==7,'L2_SEVEN_CALLS')
 rows=set();roots=set();keys=set();selected=[]
 fields={'row','key','spec','call_root','attempt','launcher','guard','binder','dbp','runtime_capture'}
 for e in entries:
  require(type(e) is dict and set(e)==fields,'L2_ENTRY_SCHEMA')
  require(type(e['row']) is int and e['row'] in (28,29,30,31,300,301,302) and e['row'] not in rows,'L2_ROW')
  require(sha(e['key']) and e['key'] not in keys,'L2_KEY')
  require(type(e['attempt']) is int and e['attempt']>=1,'L2_ATTEMPT')
  for f in ('spec','launcher','guard','binder','dbp','runtime_capture'):require(pin(e[f]),'L2_PIN:'+f)
  root=e['call_root'];require(type(root) is str and Path(root).is_absolute() and root not in roots,'L2_ROOT')
  require(Path(root).name=='DDO154_JACOBIAN_R%d_%s_A%d'%(e['row'],e['key'][:16],e['attempt']),'L2_ROOT_NAME')
  rows.add(e['row']);keys.add(e['key']);roots.add(root)
  if e['key']==key:
   require(e['spec']==spec_pin,'L2_REQUEST_SPEC');selected.append(e)
 return {'prerequisites_only':True,'entry':selected[0] if selected else None,'register':dict(register_pin),'binding':dict(binding_pin),'campaign_capture':binding['campaign_capture'],'binding_record':binding}
