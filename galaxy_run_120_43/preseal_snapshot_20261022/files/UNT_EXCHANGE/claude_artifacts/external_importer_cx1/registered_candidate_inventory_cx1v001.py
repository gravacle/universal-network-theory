"""Complete registered metadata for polling only, not VALID admission candidates.
Root binding pin and code anchors must be supplied by a trusted installer.
No spec, result, receipt or runtime capture contents are opened here.
"""
import copy
from snapshot_cx1v001 import Snapshot
from importer_root_binding_cx1v002 import load
from register_two_stage_cx1v003 import select_two_stage
from valid_admission_cx1v002 import check_held_lock
from request_guard_cx1v002 import require

def inventory(*,ctx,lock,root_binding_pin,expected_policy,expected_entry):
 check_held_lock(lock,ctx.work_dir);s=Snapshot()
 context={k:getattr(ctx,k) for k in ('config_sha256','cache_id','gate_digest')}
 bound=load(s,binding_pin=root_binding_pin,expected_policy=expected_policy,expected_entry=expected_entry,context=context)
 selected=select_two_stage(s,register_pin=bound['register_pin'],binding_pin=bound['binding_pin'],context=context,key=None,spec_pin=None)
 require(selected['campaign_capture']==bound['runtime_policy']['campaign_capture'],'INVENTORY_CAMPAIGN_CAPTURE')
 reg=s.document(bound['register_pin'])
 result=[dict(key=e['key'],spec=copy.deepcopy(e['spec']),call_dir=e['call_root'],direct_plan=copy.deepcopy(bound['direct_plan_pin']),row=e['row'],attempt=e['attempt']) for e in reg['entries']]
 fresh=Snapshot()
 for p in (root_binding_pin,bound['register_pin'],bound['binding_pin']):fresh.pin(p)
 check_held_lock(lock,ctx.work_dir)
 return result
