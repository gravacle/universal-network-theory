"""VALID admission transaction prototype; not installed in any campaign entry.
Requires an already-held parent lock and privately loaded chain modules.
Requires an existing original-directory acceptance handoff; never produces one.
F6/negative acceptance is explicitly unsupported here and fails closed.
"""
import copy
import os
from pathlib import Path
from snapshot_cx1v001 import Snapshot, Refusal
from readonly_scope_cx1v001 import ReadOnlyScope
from request_guard_cx1v001 import check_request, require
from custody_guard_cx1v002 import check_valid_custody


def check_held_lock(lock, work_dir):
    expected=Path(work_dir)/'ORCHESTRATOR.lock'
    require(lock.held is True and lock._fd is not None and Path(lock.path)==expected,'WORK_LOCK_REQUIRED')
    try:
        fd=os.fstat(lock._fd);path=expected.stat()
    except OSError as exc:raise Refusal('WORK_LOCK_UNREADABLE') from exc
    require((fd.st_dev,fd.st_ino)==(path.st_dev,path.st_ino),'WORK_LOCK_INODE_CHANGED')


def validate_valid(orch, *, lock, chain_modules, wave_dir, plan, candidate):
    """Return a verified classification plus provenance, never a cache write.
    This function must only be called from the future natural-plan executor hook.
    The lock object comes from that parent run; a caller-created plan is insufficient.
    """
    ctx=orch.ctx
    check_held_lock(lock,ctx.work_dir)
    snap=Snapshot()
    pp=Path(wave_dir)/'WAVE_PLAN.json'
    plan_pin={'path':str(pp),'sha256':snap.hash(pp)}
    require(snap.document(plan_pin)==plan,'COMMITTED_PLAN_DIFFERS')
    require(not (Path(wave_dir)/'WAVE_RESULT.json').exists(),'WAVE_ALREADY_INGESTED')
    index=candidate.get('call_index')
    with ReadOnlyScope(snap,chain_modules):
        require(not orch.check_identity_now(),'WORK_IDENTITY_CHANGED')
        calls=[c for c in plan['calls'] if c.get('call_index')==index]
        require(len(calls)==1,'UNREQUESTED_POINT')
        call=calls[0]
        mapped=ctx.mapper.build(call['theta'])
        checked=check_request(snap,work_dir=ctx.work_dir,wave=plan['wave'],call_index=index,
            plan_pin=plan_pin,config_sha256=ctx.config_sha256,cache_id=ctx.cache_id,gate_digest=ctx.gate_digest,
            candidate=candidate,mapped=mapped,theta_key=orch._external_parent_theta_key,cached_keys=orch.cache.entries)
        ctx.prelaunch_check(call['spec'])
        custody=check_valid_custody(snap,call=call,candidate=candidate,driver_pin=ctx.driver,
                                   monitor_pin=ctx.cfg['monitor'])
        handoff=Path(checked['original_call_dir'])/'TAIL_CERTIFICATE_ACCEPTANCE.json'
        require(handoff.is_file(),'EXISTING_CERTIFICATE_HANDOFF_REQUIRED')
        classified=orch.executor.classify(call,{'call_dir':checked['original_call_dir'],'status':'OK'})
        cls,code,forward,provenance=classified
        require(cls=='VALID','EXTERNAL_NOT_VALID:'+str(code))
        certificate=provenance.get('tail_certificates') or {}
        require(certificate.get('ok') is True and certificate.get('certificate_bundle')==candidate['bundle'],
                'EXTERNAL_CERTIFICATE_BUNDLE_MISMATCH')
        provenance=copy.deepcopy(provenance)
        provenance.update(execution_origin='DIRECT_EXTERNAL',external_admission={
            'schema':'CX1_EXTERNAL_VALID_ADMISSION_V001','candidate':copy.deepcopy(candidate),
            'natural_plan':plan_pin,'config_sha256':ctx.config_sha256,'cache_id':ctx.cache_id})
    check_held_lock(lock,ctx.work_dir)
    return {'classification':cls,'failure_class':code,'forward':forward,'provenance':provenance,
            'snapshot':snap,'receipt':custody['receipt'],'call':call}
