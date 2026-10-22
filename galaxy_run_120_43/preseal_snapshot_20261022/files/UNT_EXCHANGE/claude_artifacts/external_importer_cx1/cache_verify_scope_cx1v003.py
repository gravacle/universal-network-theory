"""Uninstalled cache transaction with mandatory phase-use callback.
The installer supplies authenticated fresh phase state and parent held lock.
Callback receives context and entry and must raise on invalidation/unknown import;
it must return exactly PROVISIONAL_ENVELOPE or ENVELOPE_FINAL_PASS.
No journal authentication or consumer freeze is implemented here.
"""
import copy
from snapshot_cx1v001 import Snapshot
from cache_external_selector_cx1v001 import needs_external_validation
from readonly_scope_cx1v001 import ReadOnlyScope
from request_guard_cx1v002 import require
from valid_admission_cx1v002 import check_held_lock

def make_verifier(original, *, chain_modules, phase_use, held_lock):
 require(callable(phase_use) and callable(held_lock),'PHASE_USE_AND_LOCK_REQUIRED')
 def verify(self,entry,stem):
  if not needs_external_validation(self.ctx,entry):return original(self,entry,stem)
  ctx=self.ctx
  require(not hasattr(ctx,'_cx1_cache_snapshot'),'EXTERNAL_CACHE_TRANSACTION_NESTED')
  identity=copy.deepcopy(entry)
  def check():
   check_held_lock(held_lock(ctx),ctx.work_dir)
   status=phase_use(ctx,copy.deepcopy(identity))
   require(status in ('PROVISIONAL_ENVELOPE','ENVELOPE_FINAL_PASS'),'PHASE_USE_REFUSED')
   check_held_lock(held_lock(ctx),ctx.work_dir)
  check()
  snap=Snapshot();ctx._cx1_cache_snapshot=snap
  try:
   with ReadOnlyScope(snap,chain_modules):result=original(self,entry,stem)
   require(entry==identity,'CACHE_ENTRY_CHANGED_DURING_VERIFY')
   check() # a stale snapshot must not hide an intervening final invalidation
   return result
  finally:delattr(ctx,'_cx1_cache_snapshot')
 return verify
