"""Observation/fallback-only executor factory; not a production installer.
Trusted caller supplies parent, lock/context accessors and independent root anchors.
VALID admission is deliberately refused until acceptance/cache wiring is implemented.
"""
import copy
from executor_hook_cx1v006 import make_executor_type
from executor_observer_adapter_cx1v001 import make_observer
from registered_candidate_inventory_cx1v001 import inventory
from register_two_stage_cx1v003 import pin
from request_guard_cx1v002 import require

def make_type(parent,*,root_binding_pin,expected_policy,expected_entry,theta_key,lock_for,context_for,pause,max_polls):
 require(all(pin(p) for p in (root_binding_pin,expected_policy,expected_entry)),'FACTORY_ROOT_PINS')
 require(all(callable(f) for f in (theta_key,lock_for,context_for,pause)),'FACTORY_CALLBACKS')
 require(type(max_polls) is int and max_polls>0,'FACTORY_POLL_LIMIT')
 anchors=copy.deepcopy(dict(root_binding_pin=root_binding_pin,expected_policy=expected_policy,expected_entry=expected_entry))
 base=make_executor_type(parent,None)
 class BoundObservationExecutor(base):
  def __init__(self,*args,**kwargs):
   super().__init__(*args,**kwargs)
   self._external_orch=context_for(self)
   self._external_lock=lambda:lock_for(self)
   self._external_pause=pause;self._external_max_polls=max_polls
   self._external_observe=make_observer(self,theta_key=theta_key,**copy.deepcopy(anchors))
   self._external_candidate_inventory=lambda:inventory(ctx=self._external_orch,lock=self._external_lock(),**copy.deepcopy(anchors))
  def _validate(self,candidate):
   require(False,'VALID_ADMISSION_NOT_INSTALLED')
 return BoundObservationExecutor
