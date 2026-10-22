"""Read-only preparation for direct acceptance under an already held lock.
Uses pinned c2v004 finished/dependency/first-pass checks; no producer invocation,
lock acquisition/release, reingest or writes. Caller authenticates natural binding and expected_lo selection. All dependency bytes are preflighted without execution and returned for a future private loader.
"""
import types
from accept_deps_preflight_cx1v001 import preflight
from pathlib import Path
from snapshot_cx1v001 import Refusal
from readonly_scope_cx1v001 import ReadOnlyScope
from original_spec_resolver_cx1v001 import OriginalSpecResolver
from valid_admission_cx1v002 import check_held_lock
from request_guard_cx1v002 import require
ENTRY_SHA='eb895263c8458696b265b30dc5dee771dcb89649e5b490c893bb613281c7bf19'

def prepare(orch, *, snapshot, lock, modules, wrapper, entry_pin, call, candidate, deps_pin, expected_lo, first_pass=None):
    ctx=orch.ctx;check_held_lock(lock,ctx.work_dir)
    raw=snapshot.pin(entry_pin);require(entry_pin['sha256']==ENTRY_SHA,'ACCEPT_ENTRY_VERSION')
    entry=types.ModuleType('_cx1_direct_accept_helpers');entry.__file__=entry_pin['path']
    exec(compile(raw,entry.__file__,'exec'),entry.__dict__)
    root=Path(candidate['call_dir'])
    resolver=OriginalSpecResolver(snapshot,work_dir=ctx.work_dir,bindings=[{
        'direct_plan':candidate['direct_plan'],'case':candidate['case'],'spec':candidate['spec'],'driver':ctx.driver}])
    source=resolver(root);require(str(source)==candidate['spec']['path'],'ACCEPT_SPEC_PATH')
    try:
        with ReadOnlyScope(snapshot,list(modules)+[entry]):
            require(not orch.check_identity_now(),'WORK_IDENTITY_CHANGED')
            require(call['key'] not in orch.cache.entries,'ALREADY_ACCEPTED')
            spec=snapshot.document(candidate['spec'])
            require(spec==call['spec'] and candidate['spec']['sha256']==call['spec_sha256'],'ACCEPT_SPEC_BINDING')
            receipt=entry.finished(wrapper,ctx,call,root)
            rc=snapshot.document(receipt)
            require((rc.get('pins') or {}).get('spec')==candidate['spec']
                    and (rc.get('pins') or {}).get('driver')==ctx.driver,'ACCEPT_RECEIPT_ASSOCIATION')
            passes=entry.passes_of(wrapper,root)
            require(len(passes)<entry.MAX_PASSES,'ACCEPTANCE_RERUN_LIMIT')
            if passes:
                require(first_pass is not None,'FIRST_PASS_REQUIRED')
                require(not entry.first_pass_problems(wrapper,root,passes,first_pass),'FIRST_PASS_NOT_INCOMPLETE_HERE')
            else:require(first_pass is None,'FIRST_PASS_WITHOUT_PASS')
            d=entry.read_deps(deps_pin['path'],deps_pin['sha256']);tr=ctx.cfg['tail_readiness']
            require(d['deps']['enumerator']==tr.get('state_enumerator'),'ACCEPT_ENUMERATOR')
            require(d['deps']['guard'].get('sha256')==snapshot.hash(wrapper.G.__file__),'ACCEPT_GUARD')
            require(d['policy']['approved_certificate_producers']==tr.get('approved_certificate_producers'),'ACCEPT_PRODUCERS')
            checked_deps=preflight(snapshot,d['deps'],expected_lo)
            ctx.prelaunch_check(spec)
            rec=ctx.certificate_record(wrapper.point_identity(spec))
            require(type(rec) is dict and type(rec.get('bundle')) is dict,'POINT_NOT_REGISTERED')
            policy=dict({k:d['policy'][k] for k in entry.POLICY_KEYS},receipt=receipt,prelaunch_bundle=rec['bundle'])
            require(entry.passes_of(wrapper,root)==passes,'ACCEPTANCE_PASSES_CHANGED')
    except entry.Refused as exc:raise Refusal('DIRECT_ACCEPT_PREP:'+str(exc)) from exc
    check_held_lock(lock,ctx.work_dir)
    return {'prerequisites_only':True,'call_dir':str(root),'spec':spec,'deps':d['deps'],
            'dependency_bytes':checked_deps,'policy':policy,'passes_before':passes,'receipt':receipt,'entry':dict(entry_pin)}
