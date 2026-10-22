"""Pure prerequisite guard; passing does NOT authorize admission or a cache write.
Only the future locked integration may use this result, followed by monitor,
acceptance, certificate and taxonomy verification through the pinned chain.
"""
import hashlib
from pathlib import Path
from snapshot_cx1v001 import Refusal, strict_json
from direct_layout_cx1v001 import bind_layout


def require(ok, reason):
    if not ok: raise Refusal(reason)


def check_request(snapshot, *, work_dir, wave, call_index, plan_pin,
                  config_sha256, cache_id, gate_digest, candidate,
                  mapped, theta_key, cached_keys, driver_pin):
    require(type(wave) is int and wave >= 1 and type(call_index) is int and call_index >= 0, 'REQUEST_INDEX')
    work = Path(work_dir)
    require(work.is_absolute() and str(work.resolve()) == str(work), 'WORK_DIR_CANONICAL')
    expected_plan = work/'waves'/('wave_%04d' % wave)/'WAVE_PLAN.json'
    require(plan_pin.get('path') == str(expected_plan), 'NATURAL_PLAN_PATH')
    plan = snapshot.document(plan_pin)  # Missing plan always refuses; no synthetic plan creation.
    require(type(plan) is dict, 'PLAN_SCHEMA')
    require(plan.get('config_sha256') == config_sha256 and plan.get('cache_id') == cache_id
            and plan.get('gate_digest') == gate_digest, 'PLAN_IDENTITY')
    calls = plan.get('calls')
    require(type(calls) is list and all(type(c) is dict for c in calls), 'PLAN_CALLS')
    indices = [c.get('call_index') for c in calls]
    require(all(type(i) is int for i in indices) and len(set(indices)) == len(indices), 'PLAN_DUPLICATE_INDEX')
    matches = [c for c in calls if c['call_index'] == call_index]
    require(len(matches) == 1, 'UNREQUESTED_POINT')
    call = matches[0]
    require(type(candidate) is dict, 'CANDIDATE_SCHEMA')
    require(candidate.get('key') == call.get('key') == theta_key(call['theta']), 'THETA_KEY')
    require(candidate.get('theta') == call['theta'], 'THETA_VALUE')
    require(call['key'] not in cached_keys, 'DUPLICATE_IMPORT')
    require(mapped.get('key') == call['key'] and mapped.get('spec') == call.get('spec')
            and mapped.get('sha256') == call.get('spec_sha256'), 'MAPPER_SPEC')
    raw = mapped.get('raw')
    require(type(raw) is bytes and hashlib.sha256(raw).hexdigest() == call['spec_sha256']
            and strict_json(raw) == call['spec'], 'MAPPER_BYTES')
    spec_pin = candidate.get('spec')
    require(type(spec_pin) is dict, 'SPEC_PIN')
    original = candidate.get('call_dir')
    require(type(original) is str and Path(original).is_absolute(), 'ORIGINAL_CALL_DIR')
    directory = Path(original)
    require(str(directory.resolve()) == original and directory.is_dir(), 'MOVED_OR_NONCANONICAL_CALL_DIR')
    require(directory != work and work not in directory.parents, 'EXTERNAL_CALL_IS_LOCAL')
    layout=bind_layout(snapshot,plan_pin=candidate.get('direct_plan'),case=candidate.get('case'),
                       expected_spec=spec_pin,expected_driver=driver_pin)
    require(layout['outdir']==str(directory/'out') and layout['receipt_path']==str(directory/'RECEIPT.json')
            and layout['monitor_log']==str(directory/'monitor.log'),'DIRECT_LAYOUT_ROOT_MISMATCH')
    require(spec_pin.get('sha256') == call['spec_sha256'], 'FINAL_SPEC_PIN')
    require(snapshot.pin(spec_pin) == raw, 'FINAL_SPEC_BYTES')
    slots = ((call['spec'].get('numerics') or {}).get('uv_tail') or {})
    for field in ('eps_certificate','lo_certificate'):
        ref = slots.get(field)
        require(type(ref) is dict, 'UNCERTIFIED_SLOT:' + field)
        snapshot.pin(ref)  # Content validity still requires the certificate guard.
    return {'call': call, 'original_call_dir': original, 'plan_pin': dict(plan_pin),
            'prerequisites_only': True}
