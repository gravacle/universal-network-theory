"""Read-only VALID-path custody prerequisites; certificate/taxonomy gates still required.
No F6 admission: nonaccepted readings refuse, never become MODEL_INVALID here.
"""
import hashlib
import json
import re
import types
from pathlib import Path
from snapshot_cx1v001 import Refusal, strict_json
from request_guard_cx1v001 import require

MONITOR_SHA='ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'
HANDOFF={'path':'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',
         'sha256':'5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'}


def monitor_for_snapshot(snapshot, pin):
    raw=snapshot.pin(pin)
    require(pin['sha256']==MONITOR_SHA,'MONITOR_VERSION')
    m=types.ModuleType('_cx1_snapshot_monitor')
    m.__file__=pin['path']
    exec(compile(raw,pin['path'],'exec'),m.__dict__)
    class SnapshotPath(type(Path())):
        def read_text(self, *args, **kwargs):
            return snapshot.read(str(self)).decode('utf-8')
    # Only this privately loaded module is adapted. Builtins and shared pathlib
    # are unchanged. The verifier's logic remains the exact pinned source.
    m.Path=SnapshotPath
    m.sha256_file=snapshot.hash
    m.json=types.SimpleNamespace(loads=lambda s:strict_json(s.encode() if isinstance(s,str) else s),dumps=json.dumps)
    return m


def check_valid_custody(snapshot, *, call, candidate, driver_pin, monitor_pin):
    directory=Path(candidate['call_dir'])
    rp=directory/'RECEIPT.json';result_path=directory/'out/result.json'
    receipt_pin=candidate.get('receipt')
    require(type(receipt_pin) is dict and receipt_pin.get('path')==str(rp),'FOREIGN_RECEIPT')
    receipt=snapshot.document(receipt_pin)
    require(type(receipt) is dict,'RECEIPT_OBJECT')
    result_pin=receipt.get('result')
    require(type(result_pin) is dict and result_pin.get('path')==str(result_path),'FOREIGN_RESULT')
    require((receipt.get('pins') or {}).get('driver')==driver_pin,'RECEIPT_DRIVER')
    require((receipt.get('pins') or {}).get('spec')==candidate['spec'],'RECEIPT_SPEC')
    snapshot.pin(driver_pin)
    result=snapshot.document(result_pin)
    require(type(result) is dict and result.get('call_spec_sha256')==call['spec_sha256']
            and result.get('driver_sha256')==driver_pin['sha256'],'RESULT_BINDING')
    monitor=monitor_for_snapshot(snapshot,monitor_pin)
    verified=monitor.verify_receipt(rp,spec_sha256=call['spec_sha256'],driver_sha256=driver_pin['sha256'])
    require(verified['ok'],'MONITOR_RECEIPT_REFUSED')
    require(receipt.get('status')=='FINISHED' and receipt.get('driver_status')=='COMPLETED'
            and result.get('status')=='COMPLETED' and receipt.get('exit_code')==0
            and receipt.get('stop_reason') is None,'CALL_NOT_COMPLETED')
    fp=directory/'out/finish.json'
    finish=strict_json(snapshot.read(fp))
    require(type(finish) is dict and finish.get('result_path')==str(result_path)
            and finish.get('result_sha256')==result_pin['sha256'],'FINISH_BINDING')
    acc_ref=candidate.get('acceptance')
    acc=snapshot.document(acc_ref)
    require(type(acc) is dict and acc.get('schema')=='DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'
            and acc.get('handoff')==HANDOFF,'ACCEPTANCE_SCHEMA_HANDOFF')
    require(acc.get('reading') in ('ACCEPTED','ACCEPTED_PASS_FLAGGED')
            and acc.get('outputs_are_evidence') is True and (acc.get('guard') or {}).get('ok') is True
            and acc.get('step4_stop_for_root_ruling') is False,'ACCEPTANCE_NOT_ACCEPTED')
    require(acc.get('call_dir')==str(directory) and acc.get('result')==result_pin,'FOREIGN_ACCEPTANCE')
    require(acc.get('bundle')==candidate.get('bundle'),'ACCEPTANCE_BUNDLE')
    snapshot.document(candidate['bundle']) # semantics checked later by certificate guard
    passes=[]
    for p in directory.iterdir():
        if p.name.startswith('ACCEPTANCE_TAILSTATES_'):
            match=re.fullmatch(r'ACCEPTANCE_TAILSTATES_C2V002_A([0-9]{3})',p.name)
            require(match is not None and not p.is_symlink() and p.is_dir(),'ACCEPTANCE_PASS_ENTRY')
            passes.append((int(match.group(1)),str(p)))
    passes.sort()
    require(1<=len(passes)<=2 and [n for n,_ in passes]==list(range(1,len(passes)+1)), 'ACCEPTANCE_PASS_SEQUENCE')
    require(acc.get('tailstate_dir')==passes[-1][1],'ACCEPTANCE_NOT_LATEST')
    return {'prerequisites_only':True,'receipt':receipt,'result':result,'acceptance':acc,
            'finish':{'path':str(fp),'sha256':snapshot.hash(fp)}}
