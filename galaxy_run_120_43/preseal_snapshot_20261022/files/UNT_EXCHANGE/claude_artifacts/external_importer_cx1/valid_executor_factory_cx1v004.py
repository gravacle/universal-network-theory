"""Authenticated observer plus D021 VALID leg, for a trusted private installer.
Parent locking and natural plan creation are unchanged. No standalone launch CLI.
"""
import copy
from executor_hook_cx1v006 import make_executor_type
from executor_observer_adapter_cx1v002 import make_observer
from registered_candidate_inventory_cx1v001 import inventory
from register_two_stage_cx1v003 import pin
from request_guard_cx1v002 import require
from direct_valid_leg_cx1v004 import complete
from snapshot_cx1v001 import Snapshot

def make_type(parent,*,scheduler,root_binding_pin,expected_policy,expected_entry,theta_key,lock_for,context_for,pause,max_polls,orch_for,modules,wrapper,accept_entry_pin,deps_pin,records_root):
 require(all(pin(p) for p in (root_binding_pin,expected_policy,expected_entry,accept_entry_pin,deps_pin)),'FACTORY_ROOT_PINS')
 require(all(callable(f) for f in (theta_key,lock_for,context_for,pause,orch_for)),'FACTORY_CALLBACKS')
 require(type(max_polls) is int and max_polls>0,'FACTORY_POLL_LIMIT')
 anchors=copy.deepcopy(dict(root_binding_pin=root_binding_pin,expected_policy=expected_policy,expected_entry=expected_entry))
 accept_pin=copy.deepcopy(accept_entry_pin);dependency_pin=copy.deepcopy(deps_pin)
 base=make_executor_type(parent,scheduler)
 class BoundValidExecutor(base):
  def __init__(self,*args,**kwargs):
   super().__init__(*args,**kwargs)
   self._external_context=context_for(self)
   require(self._external_context is self.ctx,'FACTORY_CONTEXT_IDENTITY')
   self._external_lock=lambda:lock_for(self)
   self._external_orch=orch_for(self)
   require(self._external_orch.ctx is self.ctx,'FACTORY_ORCH_CONTEXT')
   self._external_modules=modules
   self._external_pause=pause;self._external_max_polls=max_polls
   self._authenticated_observe=make_observer(self,theta_key=theta_key,**copy.deepcopy(anchors))
   self._external_candidate_inventory=lambda:inventory(ctx=self._external_context,lock=self._external_lock(),**copy.deepcopy(anchors))
   self._external_observe=self._observe_valid
   self._prepared={}
  def _observe_valid(self,candidate,call):
   observed=self._authenticated_observe(candidate,call)
   if observed.get('direct_state')!='TERMINAL' or observed.get('outcome') is not None:return observed
   require(all(observed.get(k) is True for k in ('natural_plan_committed','registered','identity_bound','runtime_environment_bound','envelope_valid')),'VALID_LEG_UNAUTHENTICATED')
   result=complete(self._external_orch,lock=self._external_lock(),modules=modules,wrapper=wrapper,accept_entry_pin=accept_pin,deps_pin=dependency_pin,records_root=records_root,wave_dir=self._external_wave_dir,plan=self._external_plan,candidate=candidate)
   require(self._authenticated_observe(candidate,call)==observed,'VALID_LEG_AUTHENTICATION_CHANGED')
   Snapshot().pin(dependency_pin)
   self._prepared[call['call_index']]=result
   return dict(observed,outcome='COMPLETED_VALID',acceptance=result['reading'])
  def _validate(self,candidate):
   calls=[c for c in self._external_plan['calls'] if c['call_index']==candidate['call_index']]
   require(len(calls)==1,'FACTORY_UNREQUESTED')
   evidence=self._observe_valid(candidate,calls[0])
   require(evidence.get('outcome')=='COMPLETED_VALID' and evidence.get('acceptance') in ('ACCEPTED','ACCEPTED_PASS_FLAGGED'),'FACTORY_NOT_VALID')
   result=self._prepared[candidate['call_index']]
   candidate.update(copy.deepcopy(result['candidate']))
   return result['verified']
 return BoundValidExecutor
