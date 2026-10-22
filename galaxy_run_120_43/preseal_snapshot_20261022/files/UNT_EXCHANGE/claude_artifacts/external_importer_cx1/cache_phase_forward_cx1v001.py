"""Uninstalled phase checks around the actual cached forward return path."""
from cache_verify_scope_cx1v003 import make_verifier
from request_guard_cx1v002 import require

def make_forward(original,*,chain_modules,phase_use,held_lock):
 def return_forward(self,entry,key):
  result=original(self,key)
  require(self.entries.get(key)==entry,'CACHE_FORWARD_ENTRY_REPLACED')
  return result
 checked=make_verifier(return_forward,chain_modules=chain_modules,phase_use=phase_use,held_lock=held_lock)
 def forward(self,key):
  entry=self.entries.get(key)
  if entry is None:return original(self,key)
  return checked(self,entry,key)
 return forward
