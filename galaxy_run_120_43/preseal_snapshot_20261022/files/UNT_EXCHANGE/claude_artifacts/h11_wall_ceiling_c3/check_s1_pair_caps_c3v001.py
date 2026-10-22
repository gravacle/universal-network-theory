"""Check the S1 pair's caps against DBP C2V004D (Claude3, 0844; V006 A284). Read-only; prints PASS or exits CHECK_FAILED.
usage: python3 -I -B check_s1_pair_caps_c3v001.py DBP_C2V004D_PATH DBP_SHA256 PAIR_PLAN_PATH PARENT_ADMISSION_PATH

The S1 pair guard (1274a39a) binds each call's caps three ways: to the parent admission's cfg.caps[case]
(ROOT_CAPS_BINDING, L428), to its child admission's caps (L377), and to its child plan's call bytes (L381).
So all five records must carry the DBP POST_S1 caps: the pair plan, the parent admission, both child admissions
and both child plans. The child records are read through the parent's pinned refs, and their sha256 is verified.
The DBP names the two POST_S1 entries ROOT_NAMES_AT_REGISTRATION_K3/_K4; root registers them as S1_UA_C3T and
S1_UA_C4T, in the pair guard's S1_OVERLAP_CASES order."""
import hashlib
import json
import sys

CASES = ('S1_UA_C3T', 'S1_UA_C4T')
KEYS = ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')


def fail(code, *detail):
    raise SystemExit('CHECK_FAILED ' + code + (' ' + json.dumps(detail, sort_keys=True) if detail else ''))


def pinned(ref, what):
    if not (isinstance(ref, dict) and set(ref) == {'path', 'sha256'} and isinstance(ref['path'], str)):
        fail('PIN_FORM', what)
    raw = open(ref['path'], 'rb').read()
    if hashlib.sha256(raw).hexdigest() != ref['sha256']:
        fail('PIN_SHA', what)
    return json.loads(raw)


def main(argv):
    if len(argv) != 4:
        fail('USAGE')
    dbp_raw = open(argv[0], 'rb').read()
    if hashlib.sha256(dbp_raw).hexdigest() != argv[1]:
        fail('DBP_C2V004D_PIN')
    d = json.loads(dbp_raw)
    if d.get('schema') != 'DIRECT_BATCH_PARAMS_S45_C2V004D':
        fail('DBP_SCHEMA')
    post = d['batches']['POST_S1']
    order = post['case_order']
    if len(order) != 2 or set(order) != set(post['caps_per_case']):
        fail('DBP_POST_S1_ENTRIES')
    want = {case: {k: post['caps_per_case'][e][k] for k in KEYS} for case, e in zip(CASES, order)}
    plan_raw = open(argv[2], 'rb').read()
    plan, adm = json.loads(plan_raw), json.load(open(argv[3]))
    if (adm.get('plan') or {}).get('sha256') != hashlib.sha256(plan_raw).hexdigest():
        fail('PARENT_PLAN_BINDING')
    if plan.get('batch') != 'POST_S1':
        fail('PLAN_BATCH')
    calls = plan.get('calls')
    if not isinstance(calls, list) or [c.get('case') for c in calls] != list(CASES):
        fail('PLAN_CASE_ORDER')
    refs = adm.get('s1_pair_admissions')
    if not isinstance(refs, dict) or set(refs) != set(CASES):
        fail('PARENT_PAIR_ADMISSIONS')
    for call in calls:
        case, w = call['case'], want[call['case']]
        got = {k: call.get(k) for k in KEYS}
        if got != w:
            fail('PLAN_CAPS', case, got, w)
        if (adm.get('caps') or {}).get(case) != w:
            fail('PARENT_ADMISSION_CAPS', case)
        child = pinned(refs[case], 'child admission ' + case)
        if child.get('caps') != {case: w}:
            fail('CHILD_ADMISSION_CAPS', case)
        cplan = pinned(child.get('plan'), 'child plan ' + case)
        ccalls = cplan.get('calls')
        if not (isinstance(ccalls, list) and len(ccalls) == 1 and ccalls[0].get('case') == case and
                {k: ccalls[0].get(k) for k in KEYS} == w):
            fail('CHILD_PLAN_CAPS', case)
    print(json.dumps({'status': 'PASS', 'checked': 'pair plan, parent admission, 2 child admissions, 2 child plans',
                      'wall_cap_s': {c: want[c]['wall_cap_s'] for c in CASES}}, sort_keys=True))


if __name__ == '__main__':
    main(sys.argv[1:])
