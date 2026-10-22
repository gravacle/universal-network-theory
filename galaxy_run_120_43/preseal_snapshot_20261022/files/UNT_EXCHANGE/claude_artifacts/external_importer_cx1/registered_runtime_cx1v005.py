"""Join two-stage register selection and root-pinned runtime records.
Caller supplies authenticated root pins; this prerequisite never authorizes ingestion.
"""
from pathlib import Path
from runtime_launch_binding_cx1v001 import check_launches
from register_two_stage_cx1v003 import select_two_stage,pin
from request_guard_cx1v002 import require
from runtime_distribution_record_cx1v004 import compare

def check_registered_runtime(snapshot,*,register_pin,binding_pin,context,key,spec_pin,runtime_policy):
 fields={'campaign_capture','producer','driver','monitor','output_root','freeze','direct_launch'}
 require(type(runtime_policy) is dict and set(runtime_policy)==fields,'ROOT_RUNTIME_POLICY')
 for name in fields-{'output_root'}:require(pin(runtime_policy[name]),'ROOT_RUNTIME_PIN:'+name)
 root=runtime_policy['output_root'];require(type(root) is str and Path(root).is_absolute(),'ROOT_OUTPUT_PATH')
 selected=select_two_stage(snapshot,register_pin=register_pin,binding_pin=binding_pin,context=context,key=key,spec_pin=spec_pin)
 require(selected['campaign_capture']==runtime_policy['campaign_capture'],'CAMPAIGN_CAPTURE_BINDING')
 entry=selected['entry']
 if entry is None:return {'prerequisites_only':True,'registered':False}
 require(Path(entry['call_root']).parent==Path(root),'REGISTER_OUTPUT_ROOT')
 direct=snapshot.document(entry['runtime_capture']);campaign=snapshot.document(runtime_policy['campaign_capture'])
 for record in (direct,campaign):
  require(record.get('producer')==runtime_policy['producer'],'RUNTIME_PRODUCER_POLICY')
  for name in ('driver','monitor'):
   expected=runtime_policy[name];actual=record.get(name) or {}
   require(actual.get('sha256')==expected['sha256'] and actual.get('realpath')==str(Path(expected['path']).resolve()),'RUNTIME_CODE_POLICY:'+name)
 launch=check_launches(snapshot,freeze_pin=runtime_policy['freeze'],launch_pin=runtime_policy['direct_launch'],register_pin=register_pin,binding=selected['binding_record'],direct_pin=entry['runtime_capture'],campaign_pin=runtime_policy['campaign_capture'],direct=direct,campaign=campaign)
 try:comparison=compare(direct,campaign)
 except ValueError as exc:require(False,'RUNTIME_COMPARISON_REFUSED:'+str(exc))
 return {'prerequisites_only':True,'registered':True,'entry':entry,'comparison':comparison,'launch_checks':launch,'launch_association_source':'caller-authenticated register, binding, runtime policy pins; not inferred from time'}
