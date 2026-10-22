"""Explicit direct layout from pinned plan metadata; NOT launch/admission authority.
No path proxy, aliases, run reads, or writes. Plan/root/environment validation
and acceptance-producer adaptation remain caller obligations.
"""
from pathlib import Path
from snapshot_cx1v001 import Refusal


def require(ok, why):
    if not ok: raise Refusal(why)


def canonical(value):
    require(type(value) is str and bool(value), 'LAYOUT_PATH_TYPE')
    p = Path(value)
    require(p.is_absolute() and str(p) == value and str(p.resolve()) == value,
            'LAYOUT_NONCANONICAL_PATH')
    return p


def bind_layout(snapshot, *, plan_pin, case, expected_spec, expected_driver):
    """Read only the pinned plan; return actual paths even for pending calls.
    A matching plan entry is a structural binding, not proof of root approval.
    """
    plan = snapshot.document(plan_pin)
    require(type(plan) is dict and type(plan.get('calls')) is list, 'LAYOUT_PLAN')
    require(type(case) is str and bool(case), 'LAYOUT_CASE')
    calls = plan['calls']
    require(all(type(c) is dict for c in calls), 'LAYOUT_CALL_OBJECT')
    names = [c.get('case') for c in calls]
    require(all(type(n) is str and bool(n) for n in names)
            and len(set(names)) == len(names), 'LAYOUT_DUPLICATE_CASE')
    matches = [c for c in calls if c['case'] == case]
    require(len(matches) == 1, 'LAYOUT_CASE_MISSING')
    call = matches[0]
    require(call.get('spec') == expected_spec and call.get('driver') == expected_driver,
            'LAYOUT_IDENTITY_MISMATCH')
    for pin in (expected_spec, expected_driver):
        require(type(pin) is dict and set(pin) == {'path','sha256'}, 'LAYOUT_PIN')
        canonical(pin['path'])
        sha = pin['sha256']
        require(type(sha) is str and len(sha)==64 and all(c in '0123456789abcdef' for c in sha), 'LAYOUT_SHA')
    outputs = []
    for c in calls:
        for key in ('outdir','receipt','monitor_log'):
            outputs.append(canonical(c.get(key)))
        outputs.append(canonical(c['receipt'] + '.launch.json'))
    outputs.append(canonical(plan.get('launcher_log')))
    for i,p in enumerate(outputs):
        for q in outputs[i+1:]:
            require(not p.is_relative_to(q) and not q.is_relative_to(p), 'LAYOUT_OUTPUT_OVERLAP')
    out = canonical(call['outdir'])
    return {'schema':'CX1_DIRECT_LAYOUT_V001', 'plan':dict(plan_pin), 'case':case,
            'spec':dict(expected_spec), 'driver':dict(expected_driver),
            'outdir':str(out), 'receipt_path':call['receipt'],
            'monitor_log':call['monitor_log'], 'result_path':str(out/'result.json'),
            'finish_path':str(out/'finish.json'),
            'archived_spec_path':str(out/'inputs/call_spec.json')}
