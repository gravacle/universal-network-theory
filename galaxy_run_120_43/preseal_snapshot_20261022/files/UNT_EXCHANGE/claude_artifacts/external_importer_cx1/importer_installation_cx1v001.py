"""Private A296 importer installation. No launch CLI and no policy/freeze approval.
The entry must supply the authenticated source-loaded private wrapper and its
complete module list. Installation preserves native plan/cache identities.
"""
import copy
from pathlib import Path
from snapshot_cx1v001 import Snapshot,Refusal
from request_guard_cx1v002 import require
from importer_root_binding_cx1v002 import load as root_load
from certificate_spec_adapter_cx1v002 import build_checker,SHA as WRAPPER_SHA
from classifier_spec_adapter_cx1v001 import build_classifier,SHA as PARENT_SHA
from scheduler_adapter_cx1v001 import build_scheduler,SOURCE_SHA
from valid_executor_factory_cx1v004 import make_type
from stateless_phase_cx1v002 import make_phase_use
from cache_verify_scope_cx1v003 import make_verifier
from cache_phase_forward_cx1v001 import make_forward
from cache_certificate_adapter_cx1v003 import make_checker

def install(wrapper,*,chain_modules,root_binding_pin,policy_pin,entry_pin,deps_pin,accept_entry_pin,scheduler_pin,records_root,pause,max_polls):
 W=wrapper;O=W.O;s=Snapshot()
 require(not getattr(W,'_cx1_installed',False),'IMPORTER_ALREADY_INSTALLED')
 raw=s.pin(dict(path=W.__file__,sha256=WRAPPER_SHA))
 parent_raw=s.pin(dict(path=O.__file__,sha256=PARENT_SHA))
 require(O.Context is W.Context and O.Orchestrator is W.Orchestrator and O.Cache is W.Cache and O.CampaignExecutor is W.CampaignExecutor,'IMPORTER_NATIVE_PATCH_IDENTITY')
 require(W in chain_modules and O in chain_modules and W.G in chain_modules,'IMPORTER_CHAIN_MODULES')
 require(scheduler_pin['sha256']==SOURCE_SHA,'IMPORTER_SCHEDULER_VERSION')
 scheduler=build_scheduler(s.pin(scheduler_pin),scheduler_pin['path'])
 anchors=copy.deepcopy(dict(root_binding_pin=root_binding_pin,expected_policy=policy_pin,expected_entry=entry_pin))
 dependency=copy.deepcopy(deps_pin);accept_entry=copy.deepcopy(accept_entry_pin)
 active_locks={};orchestrators={}
 def held(ctx):
  lock=active_locks.get(str(Path(ctx.work_dir)/'ORCHESTRATOR.lock'))
  require(lock is not None,'IMPORTER_PARENT_LOCK_NOT_HELD');return lock
 ParentLock=O.Lock
 class TrackedLock(ParentLock):
  def acquire(self):
   acquired=super().acquire()
   if acquired:
    require(str(self.path) not in active_locks,'IMPORTER_DUPLICATE_LOCK')
    active_locks[str(self.path)]=self
   return acquired
  def release(self):
   try:return super().release()
   finally:
    if active_locks.get(str(self.path)) is self:active_locks.pop(str(self.path))
 raw_phase=make_phase_use(held_lock=held,**anchors)
 def phase_use(ctx,entry):
  try:return raw_phase(ctx,entry)
  except (Refusal,OSError,ValueError,KeyError,TypeError) as exc:
   # Preserve the native wrapper's BaseException refusal boundary: the engine
   # must never turn invalidated evidence into an ordinary model failure.
   raise W.CertificateRefusal(str(exc)) from exc
 Context=W.Context
 checker=build_checker(raw,W.__file__,W)
 classifier=build_classifier(parent_raw,O.__file__,O)
 cache_checker=make_checker(Context.check_cached_certificate,chain_modules=chain_modules,theta_key=O.theta_key)
 ParentCache=W.Cache
 class InstalledCache(ParentCache):pass
 InstalledCache._verify_impl=make_verifier(ParentCache._verify_impl,chain_modules=chain_modules,phase_use=phase_use,held_lock=held)
 InstalledCache.forward=make_forward(ParentCache.forward,chain_modules=chain_modules,phase_use=phase_use,held_lock=held)
 Executor=make_type(W.CampaignExecutor,scheduler=scheduler,theta_key=O.theta_key,lock_for=lambda ex:held(ex.ctx),context_for=lambda ex:ex.ctx,orch_for=lambda ex:orchestrators[id(ex.ctx)],modules=chain_modules,wrapper=W,accept_entry_pin=accept_entry,deps_pin=dependency,records_root=records_root,pause=pause,max_polls=max_polls,**anchors)
 ParentOrchestrator=W.Orchestrator
 class InstalledOrchestrator(ParentOrchestrator):
  def __init__(self,ctx,*args,**kwargs):
   snap=Snapshot();context={k:getattr(ctx,k) for k in ('config_sha256','cache_id','gate_digest')}
   root_load(snap,binding_pin=anchors['root_binding_pin'],expected_policy=anchors['expected_policy'],expected_entry=anchors['expected_entry'],context=context)
   doc=snap.document(dependency);tr=ctx.cfg['tail_readiness']
   require(doc.get('schema')=='H3_CAMPAIGN_ACCEPTANCE_DEPS_C2V001' and doc.get('status')=='ROOT_FILLED' and doc.get('synthetic') is not True,'IMPORTER_ROOT_DEPS')
   require(doc['deps']['enumerator']==tr['state_enumerator'] and doc['deps']['guard']==dict(path=W.G.__file__,sha256=snap.hash(W.G.__file__)),'IMPORTER_CONTEXT_DEPS')
   require(doc['policy']['approved_certificate_producers']==tr['approved_certificate_producers'],'IMPORTER_CONTEXT_PRODUCERS')
   require(snap.hash(ctx.C.__file__)==SOURCE_SHA,'IMPORTER_CONTEXT_SCHEDULER')
   require(id(ctx) not in orchestrators,'IMPORTER_CONTEXT_REUSED')
   orchestrators[id(ctx)]=self;self._external_parent_theta_key=O.theta_key
   try:super().__init__(ctx,*args,**kwargs)
   except BaseException:
    orchestrators.pop(id(ctx),None);raise
 # All adapter construction and source checks finish before private mutation.
 Context._cx1_original_spec_path=lambda self,directory:Path(directory)/'spec.json'
 Context.certificate_check=checker;Context.check_cached_certificate=cache_checker
 W.OldExecutor._classify=classifier
 O.Lock=TrackedLock;O.Cache=InstalledCache;O.CampaignExecutor=Executor;O.Orchestrator=InstalledOrchestrator
 W._cx1_installed=True
 return dict(Context=Context,Orchestrator=InstalledOrchestrator,Cache=InstalledCache,Executor=Executor,Lock=TrackedLock,phase_use=phase_use,scheduler=scheduler)
