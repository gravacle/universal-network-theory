"""Locked planned-request binding only; never admission, execution or cache write.
Caller must obtain the lock/context/mapper and register pin from trusted parent
and root inputs. Pending output directories are allowed. No status is inferred.
"""
import hashlib
from pathlib import Path
from snapshot_cx1v001 import Snapshot, strict_json
from request_guard_cx1v001 import require
from valid_admission_cx1v001 import check_held_lock
from speculative_register_cx1v001 import select_registered
from direct_layout_cx1v001 import bind_layout

def bind_planned(*,lock,work_dir,wave,call_index,context,plan_pin,register_pin,
                 mapped,theta_key,driver_pin,cached_keys):
    check_held_lock(lock,work_dir)
    require(type(wave) is int and wave>=1 and type(call_index) is int and call_index>=0,'REQUEST_INDEX')
    work=Path(work_dir)
    require(work.is_absolute() and str(work.resolve())==str(work),'WORK_DIR_CANONICAL')
    wd=work/'waves'/('wave_%04d'%wave)
    require(plan_pin.get('path')==str(wd/'WAVE_PLAN.json'),'NATURAL_PLAN_PATH')
    require(not (wd/'WAVE_RESULT.json').exists(),'WAVE_ALREADY_INGESTED')
    snap=Snapshot();plan=snap.document(plan_pin)
    require(type(plan) is dict and plan.get('wave')==wave and all(plan.get(k)==v for k,v in context.items()),'PLAN_IDENTITY')
    calls=plan.get('calls');require(type(calls) is list and all(type(c) is dict for c in calls),'PLAN_CALLS')
    indices=[c.get('call_index') for c in calls]
    require(all(type(i) is int for i in indices) and len(indices)==len(set(indices)),'PLAN_DUPLICATE_INDEX')
    matches=[c for c in calls if c['call_index']==call_index];require(len(matches)==1,'UNREQUESTED_POINT')
    call=matches[0]
    require(call.get('key')==theta_key(call['theta']) and call['key'] not in cached_keys,'THETA_OR_DUPLICATE')
    raw=mapped.get('raw')
    require(type(raw) is bytes and mapped.get('key')==call['key'] and mapped.get('spec')==call.get('spec')
            and mapped.get('sha256')==call.get('spec_sha256')==hashlib.sha256(raw).hexdigest()
            and strict_json(raw)==call['spec'],'MAPPER_BYTES')
    reg=snap.document(register_pin)
    require(type(reg) is dict and type(reg.get('entries')) is list,'REGISTER_SHAPE')
    matches=[e for e in reg['entries'] if type(e) is dict and e.get('theta_key')==call['key']
             and type(e.get('spec')) is dict and e['spec'].get('sha256')==call['spec_sha256']]
    require(len(matches)<=1,'REGISTER_AMBIGUOUS_REQUEST')
    # Run full structural validation even with no match.
    spec=matches[0]['spec'] if matches else {'path':str(work/'UNMATCHED_SPEC'),'sha256':call['spec_sha256']}
    entry=select_registered(snap,register_pin=register_pin,context=context,theta_key=call['key'],spec_pin=spec,driver_pin=driver_pin)
    if entry is None:
        check_held_lock(lock,work_dir)
        return {'registered':False,'prerequisites_only':True}
    layout=bind_layout(snap,plan_pin=entry['direct_plan'],case=entry['case'],expected_spec=entry['spec'],expected_driver=driver_pin)
    out=Path(layout['outdir']);require(out!=work and work not in out.parents,'EXTERNAL_CALL_IS_LOCAL')
    require(snap.pin(entry['spec'])==raw,'FINAL_SPEC_BYTES')
    check_held_lock(lock,work_dir)
    return {'registered':True,'prerequisites_only':True,'entry':entry,'layout':layout,'natural_plan':dict(plan_pin),'snapshot':snap}
