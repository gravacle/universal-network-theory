"""Locked natural-plan/root prerequisites plus associated terminal observation.
No receipt existence or missing result is interpreted as fallback permission.
"""
from snapshot_cx1v001 import Snapshot
from natural_request_cx1v001 import select
from importer_root_binding_cx1v002 import load
from invocation_plan_binding_cx1v002 import bind as bind_invocation
from invocation_interpreter_cx1v001 import check as check_interpreter
from terminal_snapshot_cx1v001 import observe as observe_terminal
from registered_envelope_runtime_cx1v001 import check
from valid_admission_cx1v002 import check_held_lock
from request_guard_cx1v002 import require

def observe(*,ctx,lock,wave,call_index,plan_pin,theta_key,root_binding_pin,expected_policy,expected_entry):
 snapshot=Snapshot()
 request=select(snapshot,ctx=ctx,lock=lock,wave=wave,call_index=call_index,plan_pin=plan_pin,theta_key=theta_key)
 context={k:getattr(ctx,k) for k in ('config_sha256','cache_id','gate_digest')}
 bound=load(snapshot,binding_pin=root_binding_pin,expected_policy=expected_policy,expected_entry=expected_entry,context=context)
 require(bound['runtime_policy']['driver']==ctx.driver and bound['runtime_policy']['monitor']==ctx.cfg['monitor'],'NATURAL_RUNTIME_CODE_BINDING')
 reg=snapshot.document(bound['register_pin']);entries=reg.get('entries')
 require(type(entries) is list and all(type(e) is dict for e in entries),'NATURAL_REGISTER_ENTRIES')
 selected=[e for e in entries if e.get('key')==request['key']]
 require(len(selected)<=1,'NATURAL_REGISTER_DUPLICATE')
 spec_pin=selected[0].get('spec') if selected else None
 if selected:
  require(type(spec_pin) is dict and spec_pin.get('sha256')==request['spec_sha256'],'NATURAL_REGISTER_SPEC')
  require(snapshot.pin(spec_pin)==request['mapped']['raw'],'NATURAL_REGISTER_SPEC_BYTES')
 direct_plan_pin=bound.pop('direct_plan_pin')
 result=check(snapshot,**bound,key=request['key'],spec_pin=spec_pin)
 terminal=dict(direct_state='UNKNOWN',outcome=None,acceptance=None)
 if result['registered']:
  entry=result['runtime']['entry'];runtime=bound['runtime_policy']
  invocation=bind_invocation(snapshot,plan_pin=direct_plan_pin,entry=entry,driver=runtime['driver'],monitor=runtime['monitor'])
  launch=snapshot.document(runtime['direct_launch'])
  check_interpreter(snapshot,python=invocation['python'],identity=launch['interpreter'])
  terminal=observe_terminal(snapshot,call_root=entry['call_root'],spec=spec_pin,driver=runtime['driver'],monitor=runtime['monitor'],python=invocation['python'],caps=invocation['caps'])
 check_held_lock(lock,ctx.work_dir)
 Snapshot().pin(plan_pin) # catch a plan change during observation, outside cached reads
 return dict(natural_plan_committed=True,registered=result['registered'],identity_bound=True,runtime_environment_bound=result['registered'],envelope_valid=result['registered'],**terminal)
