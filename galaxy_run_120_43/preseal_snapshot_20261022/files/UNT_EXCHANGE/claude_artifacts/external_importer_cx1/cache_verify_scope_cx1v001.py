"""Uninstalled private cache verifier transaction. Never wrap cache put/writes."""
from snapshot_cx1v001 import Snapshot
from readonly_scope_cx1v001 import ReadOnlyScope
from request_guard_cx1v002 import require

def make_verifier(original, *, chain_modules):
 def verify(self,entry,stem):
  if (entry.get('provenance') or {}).get('execution_origin')!='DIRECT_EXTERNAL':
   return original(self,entry,stem)
  ctx=self.ctx
  require(not hasattr(ctx,'_cx1_cache_snapshot'),'EXTERNAL_CACHE_TRANSACTION_NESTED')
  snap=Snapshot();ctx._cx1_cache_snapshot=snap
  try:
   with ReadOnlyScope(snap,chain_modules):return original(self,entry,stem)
  finally:delattr(ctx,'_cx1_cache_snapshot')
 return verify
