"""D021 acceptance loader: root-selected record, same bytes for preflight and execution.
Scoped to one isolated process/thread. Native producer pin checks remain intact.
This is an IO/namespace adapter, not a security sandbox or an installed importer.
"""
import ast,builtins,copy,importlib.util,sys,threading,types
from collections.abc import MutableMapping
from contextlib import contextmanager
from pathlib import Path
from accept_deps_preflight_cx1v001 import preflight
from exclusive_output_scope_cx1v003 import ExclusiveOutputScope
from request_guard_cx1v002 import require
from snapshot_cx1v001 import Refusal
HANDOFF={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py','sha256':'5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}
GUARD_SHA='3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25'
LO={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/proof_side_c3v003/lo_state_proof_adapter_c3v003.py','sha256':'211a3220f015f8410f81e981f73355d9975d9b738a42a9d1092c28c4ae1c336c','entry':'adapt_call_lo'}
POLICY_KEYS={'approved_certificate_producers','approved_evidence_producer_sha256','approved_review_sha256','approved_uniform_producer_sha256','evidence_producer','packet_binding_reviews','root_ruling_refs','row_policy_reviews','trusted_source_producers'}

class Registry(MutableMapping):
 """Track private module registration so dataclasses sees the correct module."""
 def __init__(self):self.prior={};self.absent=object()
 def __getitem__(self,k):return sys.modules[k]
 def __iter__(self):return iter(sys.modules)
 def __len__(self):return len(sys.modules)
 def __setitem__(self,k,v):
  self.prior.setdefault(k,sys.modules.get(k,self.absent));sys.modules[k]=v
 def __delitem__(self,k):
  self.prior.setdefault(k,sys.modules.get(k,self.absent));del sys.modules[k]
 def restore(self):
  for k,v in reversed(list(self.prior.items())):
   if v is self.absent:sys.modules.pop(k,None)
   else:sys.modules[k]=v
  self.prior.clear()

@contextmanager
def load_acceptance(*,snapshot,record_pin,expected_enumerator,expected_guard,expected_producers,output_roots,allow_synthetic=False):
 require(threading.active_count()==1,'ACCEPT_LOADER_SINGLE_THREAD')
 doc=snapshot.document(record_pin)
 require(type(doc) is dict and doc.get('schema')=='H3_CAMPAIGN_ACCEPTANCE_DEPS_C2V001','ACCEPT_RECORD_SCHEMA')
 require(doc.get('status')!='TEMPLATE_ROOT_FILLS_FROM_C1','ACCEPT_RECORD_UNFILLED')
 synthetic=doc.get('status')=='SYNTHETIC' or doc.get('synthetic') is True
 require(not synthetic or allow_synthetic is True,'ACCEPT_SYNTHETIC_RECORD_REFUSED')
 pins=doc.get('deps');policy=doc.get('policy')
 require(type(policy) is dict and set(policy)==POLICY_KEYS and all(v is not None for v in policy.values()),'ACCEPT_POLICY_FIELDS')
 require(type(pins) is dict and pins.get('enumerator')==expected_enumerator,'ACCEPT_RECORD_ENUMERATOR')
 require(pins.get('guard')==expected_guard and expected_guard.get('sha256')==GUARD_SHA,'ACCEPT_RECORD_D021_GUARD')
 require(type(expected_producers) is list and len(expected_producers)==7 and policy['approved_certificate_producers']==expected_producers,'ACCEPT_ORDERED_SEVEN')
 checked=preflight(snapshot,pins,LO)
 # All eight dependencies and the handoff compile before any source executes.
 for info in checked.values():compile(info['raw'],info['pin']['path'],'exec')
 handraw=snapshot.pin(HANDOFF);compile(handraw,HANDOFF['path'],'exec')
 registry=Registry();modules=[]
 scope=ExclusiveOutputScope(snapshot,[],output_roots)
 shim=types.ModuleType('_cx1_accept_io');shim.__file__=__file__;shim.Path=Path
 import numpy as np
 shim.np=np
 def module_proxy(original,**changes):
  proxy=types.ModuleType(original.__name__);proxy.__dict__.update(vars(original));proxy.__dict__.update(changes);return proxy
 try:
  with scope:
   scope.enter_module(shim)
   pathlib_proxy=module_proxy(__import__('pathlib'),Path=shim.Path)
   sys_proxy=module_proxy(sys,modules=registry)
   # Native dynamic loaders still perform their own pinned-source checks.
   # Their module objects inherit snapshot-aware imports before exec.
   def configure(m):
    m.__dict__['__builtins__']=dict(vars(builtins),open=shim.open,__import__=private_import)
    modules.append(m);return m
   def spec_from_file_location(name,location,*args,**kwargs):
    spec=importlib.util.spec_from_file_location(name,location,*args,**kwargs)
    require(spec is not None,'ACCEPT_DYNAMIC_SPEC')
    original=spec.loader
    class Loader:
     def create_module(self,spec):return None
     def exec_module(self,m):
      configure(m);raw=snapshot.read(spec.origin)
      exec(compile(raw,spec.origin,'exec'),m.__dict__)
     def __getattr__(self,k):return getattr(original,k)
    spec.loader=Loader();return spec
   def module_from_spec(spec):return configure(importlib.util.module_from_spec(spec))
   util_proxy=module_proxy(importlib.util,spec_from_file_location=spec_from_file_location,module_from_spec=module_from_spec)
   importlib_proxy=module_proxy(__import__('importlib'),util=util_proxy)
   def private_import(name,globals=None,locals=None,fromlist=(),level=0):
    if level:raise Refusal('ACCEPT_RELATIVE_IMPORT')
    if name=='pathlib':return pathlib_proxy
    if name=='sys':return sys_proxy
    if name=='numpy':return shim.np
    if name=='importlib':return importlib_proxy
    if name=='importlib.util':return util_proxy if fromlist else importlib_proxy
    return builtins.__import__(name,globals,locals,fromlist,level)
   hand=types.ModuleType('_cx1_acceptance_handoff');hand.__file__=HANDOFF['path'];configure(hand)
   registry[hand.__name__]=hand
   exec(compile(handraw,HANDOFF['path'],'exec'),hand.__dict__)
   deps=hand.load_deps(copy.deepcopy(pins))
   require(set(deps)==set(pins)|{'pins'},'ACCEPT_LOADED_DEPS')
   yield types.SimpleNamespace(handoff=hand,deps=deps,policy=copy.deepcopy(policy),record=copy.deepcopy(record_pin),modules=modules,snapshot=snapshot)
 finally:
  registry.restore()
