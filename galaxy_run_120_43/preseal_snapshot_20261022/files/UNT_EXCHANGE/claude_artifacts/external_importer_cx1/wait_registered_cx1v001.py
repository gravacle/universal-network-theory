"""Uninstalled bounded wait driver. Observer MUST authenticate each observation.
No default observer, scheduler or sleep: this utility cannot launch or admit.
A poll limit returns HOLD, never permits fallback. Keep parent lock throughout.
"""
from inflight_policy_cx1v001 import decide
from valid_admission_cx1v002 import check_held_lock
from request_guard_cx1v002 import require

def wait_registered(*, lock, work_dir, observe, pause, max_polls):
 require(type(max_polls) is int and max_polls>0,'WAIT_POLL_LIMIT')
 trace=[]
 for i in range(max_polls):
  check_held_lock(lock,work_dir)
  evidence=observe()
  check_held_lock(lock,work_dir)
  require(type(evidence) is dict,'WAIT_OBSERVATION_SCHEMA')
  require(evidence.get('registered') is True,'REGISTERED_CALL_DISAPPEARED')
  action=decide(**evidence);trace.append(action)
  if action not in ('WAIT_EXTERNAL','WAIT_ACCEPTANCE'):
   return {'action':action,'polls':i+1,'trace':trace}
  if i+1<max_polls:
   pause()
   check_held_lock(lock,work_dir)
 return {'action':'HOLD_POLL_LIMIT','polls':max_polls,'trace':trace}
