"""Select a request solely from a committed natural plan under the parent lock.
No candidate files are read. Root registration and complete admission follow later.
"""
import hashlib
from pathlib import Path
from snapshot_cx1v001 import strict_json
from request_guard_cx1v002 import require
from valid_admission_cx1v002 import check_held_lock

def select(snapshot,*,ctx,lock,wave,call_index,plan_pin,theta_key):
 check_held_lock(lock,ctx.work_dir)
 require(type(wave) is int and wave>0 and type(call_index) is int and call_index>=0,'NATURAL_REQUEST_INDEX')
 work=Path(ctx.work_dir);require(work.is_absolute() and str(work.resolve())==str(work),'NATURAL_WORK_PATH')
 expected=work/'waves'/('wave_%04d'%wave)/'WAVE_PLAN.json'
 require(plan_pin.get('path')==str(expected),'NATURAL_COMMITTED_PLAN_PATH')
 plan=snapshot.document(plan_pin)
 require(type(plan) is dict and plan.get('wave')==wave,'NATURAL_PLAN_WAVE')
 for name in ('config_sha256','cache_id','gate_digest'):require(plan.get(name)==getattr(ctx,name),'NATURAL_PLAN_CONTEXT:'+name)
 calls=plan.get('calls');require(type(calls) is list and all(type(c) is dict for c in calls),'NATURAL_PLAN_CALLS')
 indices=[c.get('call_index') for c in calls]
 require(all(type(i) is int and i>=0 for i in indices) and len(indices)==len(set(indices)),'NATURAL_PLAN_INDICES')
 chosen=[c for c in calls if c['call_index']==call_index];require(len(chosen)==1,'NATURAL_UNREQUESTED')
 call=chosen[0];require(call.get('key')==theta_key(call['theta']),'NATURAL_THETA_KEY')
 mapped=ctx.mapper.build(call['theta']);raw=mapped.get('raw')
 require(type(raw) is bytes and hashlib.sha256(raw).hexdigest()==call.get('spec_sha256') and strict_json(raw)==call.get('spec'),'NATURAL_MAPPER_BYTES')
 require(mapped.get('key')==call['key'] and mapped.get('spec')==call['spec'] and mapped.get('sha256')==call['spec_sha256'],'NATURAL_MAPPER_IDENTITY')
 check_held_lock(lock,ctx.work_dir)
 return dict(prerequisites_only=True,key=call['key'],spec_sha256=call['spec_sha256'],call=call,mapped=mapped,plan_pin=dict(plan_pin))
