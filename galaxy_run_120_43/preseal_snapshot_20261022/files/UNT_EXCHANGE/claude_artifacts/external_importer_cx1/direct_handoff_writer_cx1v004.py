"""Uninstalled direct certificate handoff producer; inert-tested only.
Requires a trusted private Context with explicit-spec checker installed and a
held parent lock. Never produces scientific output or modifies existing files.
"""
import os
from pathlib import Path
from snapshot_cx1v001 import Snapshot
from readonly_scope_cx1v001 import ReadOnlyScope
from original_spec_resolver_cx1v001 import OriginalSpecResolver
from custody_guard_cx1v003 import check_valid_custody
from request_guard_cx1v001 import require
from valid_admission_cx1v001 import check_held_lock
import certificate_spec_adapter_cx1v004 as adapter

def write_handoff(orch, *, lock, chain_modules, wrapper_module, call, candidate):
    ctx=orch.ctx;root=Path(candidate['call_dir']);target=root/'TAIL_CERTIFICATE_ACCEPTANCE.json'
    check_held_lock(lock,ctx.work_dir)
    def verify(snapshot, handoff=None):
        with ReadOnlyScope(snapshot,chain_modules):
            require(not orch.check_identity_now(),'WORK_IDENTITY_CHANGED')
            custody=check_valid_custody(snapshot,call=call,candidate=candidate,driver_pin=ctx.driver,monitor_pin=ctx.cfg['monitor'])
            spec=snapshot.document(candidate['spec'])
            ctx.prelaunch_check(spec)
            resolver=OriginalSpecResolver(snapshot,work_dir=ctx.work_dir,bindings=[{
                'direct_plan':candidate['direct_plan'],'case':candidate['case'],
                'spec':candidate['spec'],'driver':ctx.driver}])
            absent=object();prior=getattr(ctx,'_cx1_original_spec_path',absent)
            ctx._cx1_original_spec_path=resolver
            try:
                rec=ctx.certificate_record(wrapper_module.point_identity(spec))
                require(type(rec) is dict,'CERTIFICATE_POINT_MISSING')
                if handoff is None:
                    handoff={'schema':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001',
                        'result_sha256':custody['acceptance']['result']['sha256'],
                        'call_spec_sha256':candidate['spec']['sha256'],
                        'certificate_bundle':candidate['bundle'],'prelaunch_bundle':rec['bundle'],
                        'writer':{'path':str(Path(__file__).resolve()),'sha256':snapshot.hash(Path(__file__).resolve())},
                        'checker_adapter':{'path':str(Path(adapter.__file__).resolve()),'sha256':snapshot.hash(Path(adapter.__file__).resolve())}}
                g=ctx.certificate_check(spec,'acceptance',result=custody['result'],call_dir=root,_handoff=handoff)
                require(g.get('ok') is True,'CERTIFICATE_HANDOFF_REFUSED')
                return handoff
            finally:
                if prior is absent:delattr(ctx,'_cx1_original_spec_path')
                else:ctx._cx1_original_spec_path=prior
    snap=Snapshot();handoff=verify(snap)
    check_held_lock(lock,ctx.work_dir)
    # All evidence reads above use the snapshot; writes happen outside read scope.
    if target.exists():
        require(snap.document({'path':str(target),'sha256':snap.hash(target)})==handoff,'IMMUTABLE_HANDOFF_DIFFERS')
        created=False
    else:
        import json
        raw=(json.dumps(handoff,sort_keys=True,indent=1,allow_nan=False)+'\n').encode()
        with target.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        created=True
    fresh=Snapshot()
    saved=fresh.document({'path':str(target),'sha256':fresh.hash(target)})
    require(saved==handoff,'HANDOFF_READBACK_DIFFERS')
    verify(fresh,saved)
    check_held_lock(lock,ctx.work_dir)
    return {'prerequisites_only':True,'created':created,'handoff':{'path':str(target),'sha256':fresh.hash(target)}}
