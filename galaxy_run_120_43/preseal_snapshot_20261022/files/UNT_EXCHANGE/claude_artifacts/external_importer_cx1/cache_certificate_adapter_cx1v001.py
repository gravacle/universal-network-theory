"""Private context adapter; uninstalled. Original checker and parent cache checks remain required."""
import copy
from snapshot_cx1v001 import Snapshot
from readonly_scope_cx1v001 import ReadOnlyScope
from original_spec_resolver_cx1v001 import OriginalSpecResolver
from external_cache_guard_cx1v001 import check_external_cache
from request_guard_cx1v002 import require

def make_checker(original, *, chain_modules, theta_key):
 def check(self, entry):
  p=entry.get('provenance') or {}
  if p.get('execution_origin')!='DIRECT_EXTERNAL':
   return original(self,entry)
  normalized=copy.deepcopy(entry)
  key=theta_key(normalized['theta'])
  require('key' not in normalized or normalized['key']==key,'EXTERNAL_CACHE_KEY')
  normalized['key']=key
  snap=Snapshot()
  with ReadOnlyScope(snap,chain_modules):
   checked=check_external_cache(snap,ctx=self,entry=normalized,theta_key=theta_key)
   c=checked['candidate']
   resolver=OriginalSpecResolver(snap,work_dir=self.work_dir,bindings=[{
    'direct_plan':c['direct_plan'],'case':c['case'],'spec':c['spec'],'driver':self.driver}])
   absent=object();previous=getattr(self,'_cx1_original_spec_path',absent)
   self._cx1_original_spec_path=resolver
   try:return original(self,normalized)
   finally:
    if previous is absent:delattr(self,'_cx1_original_spec_path')
    else:self._cx1_original_spec_path=previous
 return check
