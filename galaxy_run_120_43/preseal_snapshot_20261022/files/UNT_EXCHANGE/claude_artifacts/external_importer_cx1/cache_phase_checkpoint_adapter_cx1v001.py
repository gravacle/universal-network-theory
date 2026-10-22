"""Uninstalled fresh checkpoint-backed phase callback for cache_verify_scope v003.
Resolver must authenticate its checkpoint and import association independently.
No event producer, checkpoint publisher, or campaign freeze is supplied here.
"""
import copy
from phase_checkpoint_cx1v001 import check
from phase_invalidation_cx1v001 import require_use
from request_guard_cx1v002 import require

def make_phase_use(*,resolve,held_lock):
 require(callable(resolve) and callable(held_lock),'PHASE_RESOLVER_REQUIRED')
 def phase_use(ctx,entry):
  binding=resolve(ctx,copy.deepcopy(entry))
  require(type(binding) is dict and set(binding)=={'checkpoint_pin','directory','phase_id','import_id'},'PHASE_BINDING_SCHEMA')
  require(type(binding['import_id']) is str and bool(binding['import_id']),'PHASE_IMPORT_ID')
  result=check(checkpoint_pin=binding['checkpoint_pin'],directory=binding['directory'],work_dir=ctx.work_dir,lock=held_lock(ctx),phase_id=binding['phase_id'])
  return require_use(result['journal']['events'],binding['phase_id'],binding['import_id'])
 return phase_use
