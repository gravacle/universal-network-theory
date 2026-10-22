"""A122 PRELAUNCH emitter. No scientific launches; guard007 remains unchanged.
Candidate inputs are not a root admission. Root must publish the bound admission
separately after distinct review. Records are exact native returns, never labels.
"""
import argparse
import hashlib
import json
import os
import types
from pathlib import Path

GUARD_PATH = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_packet_cx1/impl/step4_guard_cx1v007.py')
GUARD_SHA256 = '42bf0ce9dcd48f734299ace4f07cb92a15563e57a39f5ae40be451e481d1c3de'

def guard():
    data = GUARD_PATH.read_bytes()
    if hashlib.sha256(data).hexdigest() != GUARD_SHA256:
        raise PermissionError('GUARD_BOOTSTRAP_HASH_MISMATCH')
    g = types.ModuleType('_prelaunch_guard007')
    g.__file__ = str(GUARD_PATH)
    exec(compile(data, str(GUARD_PATH), 'exec'), g.__dict__)
    return g

def emit(admission_ref, plan_ref, output_dir):
    g = guard()
    cfg = g.doc(admission_ref)
    plan = g.doc(plan_ref)
    g.require(cfg.get('schema') == 'UNT_STEP4_ADMISSION_CX1V001' and cfg.get('authority') == g.AUTHORITY, 'ROOT_CANDIDATE_REQUIRED')
    g.require(cfg.get('status') == 'ROOT_AUTHORIZED' and cfg.get('plan') is None, 'UNBOUND_ADMISSION_CANDIDATE_REQUIRED')
    g.require(plan.get('schema') == 'UNT_STEP4_LAUNCH_PLAN_CX1V001', 'PLAN_REQUIRED')
    g.require(plan.get('guard', {}).get('sha256') in (GUARD_SHA256, 'f27a48686b7b2f9048542dcd7614e84322a81758bd4c28d2fa0bc5ffe64314bc'), 'GUARD_IDENTITY')
    g.admitted_source(plan['guard'], cfg)
    # Native calls still use unchanged guard007; guard008 adds A124 disk admission.
    g.source_map(cfg)
    g.check_review(cfg)
    calls = plan.get('calls')
    g.require(isinstance(calls, list) and bool(calls), 'NONEMPTY_CALLS_REQUIRED')
    ids = [c.get('case') for c in calls]
    g.require(all(isinstance(x, str) and bool(x) for x in ids) and len(set(ids)) == len(ids), 'UNIQUE_CASES_REQUIRED')
    g.require(cfg.get('case_order') == ids, 'ROOT_ORDER_BINDING')
    out = g.safe_path(str(output_dir))
    g.require(out.is_dir(), 'EXISTING_OUTPUT_DIRECTORY_REQUIRED')
    targets = [out / ('PRELAUNCH_%04d.json' % i) for i in range(len(calls))]
    manifest_path = out / 'PRELAUNCH_MANIFEST.json'
    for p in targets + [manifest_path]:
        g.require(not os.path.lexists(p), 'EXISTING_OUTPUT_REFUSED')
    records = []
    for call in calls:
        g.require(call.get('spec_status') == 'ROOT_FINAL' and call.get('pending') == [], 'PENDING_SPEC_REFUSED')
        g.require(call['driver']['sha256'] in (g.R5_SHA, g.REF_SHA), 'EXACT_DRIVER_REQUIRED')
        g.admitted_source(call['driver'], cfg)
        g.verify(call['spec'])
        approved = cfg.get('calls', {}).get(call['case'])
        g.require(isinstance(approved, dict) and approved.get('spec') == call['spec'] and approved.get('driver') == call['driver'], 'ROOT_CALL_BINDING')
        # Do not allow callers to substitute an existing PASS-labelled artifact.
        g.require(call.get('prelaunch') is None and approved.get('prelaunch') is None, 'PRELAUNCH_INPUT_MUST_BE_PENDING')
        # Outer fence covers the entire native call, including initial spec reads.
        with g.fence(cfg['sources']):
            record = g.native_preflight(cfg, call)
        records.append(record)
    # Recheck custody before emitting anything; no partial success on gate failure.
    g.verify(admission_ref)
    g.verify(plan_ref)
    g.source_map(cfg)
    payloads = [(json.dumps(r, sort_keys=True, indent=2, allow_nan=False) + '\n').encode() for r in records]
    entries = [{'case': c['case'], 'spec': c['spec'], 'driver': c['driver'],
                'prelaunch': {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest()}}
               for c, p, b in zip(calls, targets, payloads)]
    manifest = {'schema': 'UNT_STEP4_PRELAUNCH_MANIFEST_CX1V001',
                'admission_candidate': admission_ref, 'plan_candidate': plan_ref,
                'guard': g.pin(GUARD_PATH), 'producer': g.pin(__file__), 'calls': entries,
                'authority': 'Records only; independent root admission is still required.'}
    mb = (json.dumps(manifest, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    # Exclusive writes preserve any prefix on I/O failure. No cleanup or retry.
    for p, b in zip(targets + [manifest_path], payloads + [mb]):
        with p.open('xb') as f:
            f.write(b)
    return {'manifest': g.pin(manifest_path), 'records': len(records)}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('admission', 'admission-sha256', 'plan', 'plan-sha256', 'output-dir'):
        p.add_argument('--' + name, required=True)
    a = p.parse_args()
    result = emit({'path': a.admission, 'sha256': a.admission_sha256},
                  {'path': a.plan, 'sha256': a.plan_sha256}, a.output_dir)
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
