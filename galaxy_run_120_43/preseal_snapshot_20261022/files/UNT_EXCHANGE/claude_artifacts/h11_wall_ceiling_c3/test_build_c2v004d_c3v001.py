"""Synthetic tests for build_params_s45_c2v004d_c3v001 and check_s1_pair_caps_c3v001 (Claude3, 0844).
Reads the pinned C2V004B and C2V004C bytes read-only; every other file is synthetic and written under WORK_DIR.
usage: python3 -I -B test_build_c2v004d_c3v001.py BUILDER_PATH CHECKER_PATH WORK_DIR   (WORK_DIR must not exist)"""
import datetime as dt
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

builder, checker, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
os.mkdir(work)
PY = sys.executable
FILL, LATER = '2026-10-22T09:30:00Z', '2026-10-26T12:00:00Z'
CEIL = dt.datetime(2026, 12, 1, 5, 59, tzinfo=dt.timezone.utc)
secs = lambda s: int((CEIL - dt.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)).total_seconds())
W, W_LATER = secs(FILL), secs(LATER)
KEYS = ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')
CASES = ('S1_UA_C3T', 'S1_UA_C4T')
results = []


def check(name, cond, detail=None):
    results.append({'id': name, 'pass': bool(cond), 'detail': detail})


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def flat(o, pre=''):
    if isinstance(o, dict) and o:
        out = {}
        for k, v in o.items():
            out.update(flat(v, pre + k + '.'))
        return out
    return {pre[:-1]: o}


def changed(fa, fb):
    return {k for k in set(fa) | set(fb) if fa.get(k, '<absent>') != fb.get(k, '<absent>')}


def refused(fn, code):
    try:
        fn()
    except SystemExit as e:
        return str(e).startswith('REFUSED ' + code)
    except Exception:
        return False
    return False


B0 = load(builder, 'b0')
b_raw, c_raw = B0.BASE_B.read_bytes(), B0.BASE_C.read_bytes()
fB, fC = flat(json.loads(b_raw)), flat(json.loads(c_raw))
HW = sorted(k for k in fC if k.startswith('batches.HEADLINE.') and k.endswith('.wall_cap_s'))
PW = sorted(k for k in fC if k.startswith('batches.POST_S1.') and k.endswith('.wall_cap_s'))
PROV_C = {'schema', 'supersedes.path', 'supersedes.sha256', 'supersedes.what_changes', 'note_a271'}
PROV_D = {'schema', 'supersedes.path', 'supersedes.sha256', 'supersedes.what_changes', 'note_a284'}


def builder_suite(M):
    """Independent checks of a builder module. Returns the ids of failed checks (empty for a correct builder)."""
    fails = []

    def ck(name, cond):
        if not cond:
            fails.append(name)
    try:
        raw, draw, wall = M.build(b_raw, c_raw, FILL)
    except BaseException as e:
        return ['reference_build_raised ' + str(e)[:80]]
    doc = json.loads(raw)
    fD = flat(doc)
    ck('wall_is_seconds_to_phase2_ceiling', wall == W == 3443340)
    ck('vs_c2v004c_exactly_2_post_s1_walls_plus_provenance', changed(fC, fD) == set(PW) | PROV_D)
    ck('vs_c2v004b_exactly_13_walls_plus_provenance', changed(fB, fD) == set(HW) | set(PW) | PROV_C | PROV_D)
    ck('post_s1_walls_are_W', len(PW) == 2 and all(fD[k] == W for k in PW))
    ck('headline_walls_are_c2v004c', len(HW) == 11 and all(fD[k] == fC[k] for k in HW))
    ck('rss_output_and_other_walls_unchanged', all(fD.get(k) == v for k, v in fB.items()
                                                   if k.endswith(('.rss_cap_bytes', '.output_cap_bytes')) or
                                                   (k.endswith('.wall_cap_s') and k not in HW and k not in PW)))
    ck('rss_is_ram_everywhere', all(v == 137438953472 for k, v in fD.items() if k.endswith('.rss_cap_bytes')))
    ck('serialization_matches_dbp_convention', raw == (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode())
    ck('supersedes_binds_c2v004c', doc['supersedes']['sha256'] == B0.BASE_C_SHA and
       doc['supersedes']['path'] == str(B0.BASE_C) and doc['schema'] == 'DIRECT_BATCH_PARAMS_S45_C2V004D')
    d = json.loads(draw)
    ck('leaf_diff_record_consistent', d['against_c2v004c']['n_changed'] == 7 and d['against_c2v004b']['n_changed'] == 19 and
       d['successor_sha256'] == hashlib.sha256(raw).hexdigest() and d['c2v004c_fill_utc'] == FILL)
    ck('deterministic', M.build(b_raw, c_raw, FILL)[0] == raw)
    try:
        raw2, _, wall2 = M.build(b_raw, c_raw, LATER)
        f2 = flat(json.loads(raw2))
        ck('later_exact_fill_moves_only_post_s1_walls', wall2 == W_LATER and all(f2[k] == W_LATER for k in PW) and
           all(f2[k] == fC[k] for k in HW) and changed(fC, f2) == set(PW) | PROV_D)
    except BaseException:
        fails.append('later_exact_fill_raised')
    ck('fill_too_late_refused', refused(lambda: M.build(b_raw, c_raw, '2026-11-30T05:59:00Z'), 'FILL_TOO_LATE'))
    ck('fill_after_ceiling_refused', refused(lambda: M.build(b_raw, c_raw, '2026-12-02T00:00:00Z'), 'FILL_TOO_LATE'))
    ck('fill_before_c2v004c_fill_refused', refused(lambda: M.build(b_raw, c_raw, '2026-10-22T09:29:59Z'), 'FILL_BEFORE_C2V004C_FILL'))
    ck('noncanonical_utc_refused', refused(lambda: M.build(b_raw, c_raw, '2026-10-22 09:30:00'), 'BAD_UTC') and
       refused(lambda: M.build(b_raw, c_raw, '2026-10-22T9:30:00Z'), 'NONCANONICAL_UTC'))
    ck('tampered_c2v004b_refused', refused(lambda: M.build(b_raw.replace(b'100800', b'100801', 1), c_raw, FILL), 'BASE_B_PIN_MISMATCH'))
    ck('tampered_c2v004c_refused', refused(lambda: M.build(b_raw, c_raw.replace(b'"wall_cap_s": 100800', b'"wall_cap_s": 100801', 1), FILL),
                                           'BASE_C_PIN_MISMATCH'))
    return fails


# 1. builder checks on the real builder
base_fails = builder_suite(B0)
check('builder_suite_all_pass', not base_fails, base_fails)

# 2. CLI: new absolute out dir only; exclusive outputs
out1 = work / 'run1'
r = subprocess.run([PY, '-I', '-B', str(builder), '--fill-utc', FILL, '--out-dir', str(out1)], capture_output=True, text=True)
names = sorted(os.listdir(out1)) if out1.is_dir() else []
check('cli_writes_two_files', r.returncode == 0 and names == ['DIRECT_BATCH_PARAMS_S45_C2V004D.json', 'LEAF_DIFF_S45_C2V004D.json'],
      r.stdout + r.stderr)
D_PATH = out1 / 'DIRECT_BATCH_PARAMS_S45_C2V004D.json'
D_RAW = D_PATH.read_bytes()
D_SHA = hashlib.sha256(D_RAW).hexdigest()
check('cli_bytes_equal_build', D_RAW == B0.build(b_raw, c_raw, FILL)[0])
r2 = subprocess.run([PY, '-I', '-B', str(builder), '--fill-utc', FILL, '--out-dir', str(out1)], capture_output=True, text=True)
check('cli_existing_out_dir_refused', r2.returncode != 0 and 'OUT_DIR_MUST_BE_NEW' in (r2.stdout + r2.stderr))
r3 = subprocess.run([PY, '-I', '-B', str(builder), '--fill-utc', FILL, '--out-dir', 'relative_dir'], capture_output=True, text=True, cwd=str(work))
check('cli_relative_out_dir_refused', r3.returncode != 0 and not (work / 'relative_dir').exists())

# 3. synthetic S1 pair records for the checker
fx = work / 'pair_fixtures'
os.mkdir(fx)


def put(p, obj):
    raw = (json.dumps(obj, indent=1, sort_keys=True) + '\n').encode()
    with open(p, 'xb') as f:
        f.write(raw)
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest()}


def make_pair(tag, dbp_doc, mutate=lambda kind, case, obj: None):
    d = fx / tag
    os.mkdir(d)
    post = dbp_doc['batches']['POST_S1']
    calls, refs = [], {}
    for case, entry in zip(CASES, post['case_order']):
        caps = {k: post['caps_per_case'][entry][k] for k in KEYS}
        call = dict(case=case, spec={'path': '/synthetic/spec_%s.json' % case, 'sha256': '0' * 64},
                    driver={'path': '/synthetic/driver.py', 'sha256': '1' * 64}, **caps)
        cplan = {'schema': 'UNT_STEP4_LAUNCH_PLAN_CX1V001', 'binding_status': 'ROOT_BOUND', 'batch': 'POST_S1', 'calls': [dict(call)]}
        mutate('child_plan', case, cplan)
        cadm = {'schema': 'UNT_STEP4_ADMISSION_CX1V001', 'status': 'ROOT_AUTHORIZED', 'case_order': [case],
                'plan': put(d / ('child_plan_%s.json' % case), cplan), 'caps': {case: dict(caps)}}
        mutate('child_admission', case, cadm)
        refs[case] = put(d / ('child_admission_%s.json' % case), cadm)
        calls.append(call)
    plan = {'schema': 'UNT_STEP4_LAUNCH_PLAN_CX1V001', 'binding_status': 'ROOT_BOUND', 'batch': 'POST_S1', 'calls': calls}
    mutate('plan', None, plan)
    adm = {'schema': 'UNT_STEP4_ADMISSION_CX1V001', 'status': 'ROOT_AUTHORIZED', 'plan': put(d / 'pair_plan.json', plan),
           'caps': {c['case']: {k: c[k] for k in KEYS} for c in plan['calls']}, 's1_pair_admissions': refs}
    mutate('parent_admission', None, adm)
    put(d / 'parent_admission.json', adm)
    return str(d / 'pair_plan.json'), str(d / 'parent_admission.json')


def m(kind0, case0, fn):
    def mutate(kind, case, obj):
        if kind == kind0 and case in (case0, None):
            fn(obj)
    return mutate


D_DOC, C_DOC = json.loads(D_RAW), json.loads(c_raw)
CASES_RUN = [
    # (id, dbp_path, dbp_sha, pair, expected: 'PASS' or the CHECK_FAILED code)
    ('positive_d_caps_pass', D_PATH, D_SHA, make_pair('positive', D_DOC), 'PASS'),
    ('pair_filled_from_c2v004c_refused', D_PATH, D_SHA, make_pair('from_c', C_DOC), 'PLAN_CAPS'),
    ('old_wall_in_plan', D_PATH, D_SHA, make_pair('plan_old', D_DOC, m('plan', None, lambda o: o['calls'][0].update(wall_cap_s=100800))), 'PLAN_CAPS'),
    ('rss_changed_in_plan', D_PATH, D_SHA, make_pair('plan_rss', D_DOC, m('plan', None, lambda o: o['calls'][1].update(rss_cap_bytes=1))), 'PLAN_CAPS'),
    ('old_wall_in_parent_admission', D_PATH, D_SHA,
     make_pair('adm_old', D_DOC, m('parent_admission', None, lambda o: o['caps']['S1_UA_C4T'].update(wall_cap_s=100800))), 'PARENT_ADMISSION_CAPS'),
    ('old_wall_in_child_admission', D_PATH, D_SHA,
     make_pair('cadm_old', D_DOC, m('child_admission', 'S1_UA_C3T', lambda o: o['caps']['S1_UA_C3T'].update(wall_cap_s=100800))), 'CHILD_ADMISSION_CAPS'),
    ('old_wall_in_child_plan', D_PATH, D_SHA,
     make_pair('cplan_old', D_DOC, m('child_plan', 'S1_UA_C4T', lambda o: o['calls'][0].update(wall_cap_s=100800))), 'CHILD_PLAN_CAPS'),
    ('child_admission_pin_sha_refused', D_PATH, D_SHA,
     make_pair('cadm_sha', D_DOC, m('parent_admission', None, lambda o: o['s1_pair_admissions']['S1_UA_C3T'].update(sha256='0' * 64))), 'PIN_SHA'),
    ('wrong_case_order', D_PATH, D_SHA, make_pair('order', D_DOC, m('plan', None, lambda o: o['calls'].reverse())), 'PLAN_CASE_ORDER'),
    ('plan_not_bound_by_parent', D_PATH, D_SHA,
     make_pair('unbound', D_DOC, m('parent_admission', None, lambda o: o['plan'].update(sha256='0' * 64))), 'PARENT_PLAN_BINDING'),
    ('dbp_sha_mismatch', D_PATH, '0' * 64, make_pair('dbp_sha', D_DOC), 'DBP_C2V004D_PIN'),
    ('c2v004c_given_as_dbp', B0.BASE_C, B0.BASE_C_SHA, make_pair('c_as_d', D_DOC), 'DBP_SCHEMA'),
]


def run_checker(path, dbp, sha, pair):
    r = subprocess.run([PY, '-I', '-B', str(path), str(dbp), sha, pair[0], pair[1]], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode == 0 and '"status": "PASS"' in r.stdout:
        return 'PASS', out
    for line in out.splitlines():
        if line.startswith('CHECK_FAILED '):
            return line.split()[1], out
    return 'ERROR', out


def checker_suite(path):
    fails, seen = [], {}
    for cid, dbp, sha, pair, want in CASES_RUN:
        got, out = run_checker(path, dbp, sha, pair)
        seen[cid] = got
        if got != want:
            fails.append(cid)
    return fails, seen


cfails, cseen = checker_suite(checker)
check('checker_suite_all_pass', not cfails, cseen)
pos = run_checker(checker, D_PATH, D_SHA, CASES_RUN[0][3])[1]
check('checker_reports_both_walls_W', '"S1_UA_C3T": %d' % W in pos and '"S1_UA_C4T": %d' % W in pos, pos)

# 4. restoring mutants: each removes or bends one guard; an independent check above must catch it
mdir = work / 'mutants'
os.mkdir(mdir)
bsrc, csrc = builder.read_text(), checker.read_text()
B_MUT = {
    'M1_scope_checks_removed_and_DIII_wall_changed': [
        ("        refuse('LEAF_DIFF_SCOPE_VS_C2V004C')", "        pass"),
        ("        refuse('LEAF_DIFF_SCOPE_VS_C2V004B')", "        pass"),
        ("            refuse('OTHER_WALL_CHANGED')", "            pass"),
        ("    fd = flat(doc)\n", "    doc['batches']['DIII']['caps_per_case']['DECIDING_III_LOW_R5']['wall_cap_s'] = wall\n    fd = flat(doc)\n")],
    'M2_shorter_wall_allowed': [("    if wall <= OLD_WALL:\n", "    if False:\n")],
    'M3_c2v004c_pin_skipped': [("    if sha_b(c_raw) != BASE_C_SHA:\n", "    if False:\n")],
    'M4_wall_rounded_up_a_day': [("    wall = int((ceiling - fill).total_seconds())\n", "    wall = int((ceiling - fill).total_seconds()) + 86400\n")],
    'M5_headline_walls_refilled_from_new_fill': [
        ("        refuse('LEAF_DIFF_SCOPE_VS_C2V004C')", "        pass"),
        ("            refuse('HEADLINE_WALL_NOT_C2V004C')", "            pass"),
        ("    fd = flat(doc)\n", "    for k in head:\n        doc['batches']['HEADLINE']['caps_per_case'][k]['wall_cap_s'] = wall\n    fd = flat(doc)\n")],
    'M6_fill_before_c2v004c_allowed': [("    if wall > c_wall:\n", "    if False:\n")],
}
C_MUT = {
    'K1_child_plan_caps_unchecked': [("            fail('CHILD_PLAN_CAPS', case)", "            pass")],
    'K2_parent_admission_caps_unchecked': [("            fail('PARENT_ADMISSION_CAPS', case)", "            pass")],
    'K3_pin_sha_unchecked': [("    if hashlib.sha256(raw).hexdigest() != ref['sha256']:\n", "    if False:\n")],
    'K4_parent_plan_binding_unchecked': [("        fail('PARENT_PLAN_BINDING')", "        pass")],
    'K5_wall_only_compared': [("KEYS = ('wall_cap_s', 'rss_cap_bytes', 'output_cap_bytes')", "KEYS = ('wall_cap_s',)")],
}
killed = {}
for name, edits in B_MUT.items():
    s = bsrc
    for old, new in edits:
        assert s.count(old) == 1, (name, old)
        s = s.replace(old, new)
    p = mdir / (name + '.py')
    p.write_text(s)
    f = builder_suite(load(p, name))
    killed[name] = {'killed': bool(f), 'by': f[:4]}
for name, edits in C_MUT.items():
    s = csrc
    for old, new in edits:
        assert s.count(old) == 1, (name, old)
        s = s.replace(old, new)
    p = mdir / (name + '.py')
    p.write_text(s)
    f, _ = checker_suite(p)
    killed[name] = {'killed': bool(f), 'by': f[:4]}
check('all_mutants_killed', all(v['killed'] for v in killed.values()), killed)

rec = {'schema': 'TEST_RECORD_C2V004D_C3V001', 'builder_sha256': hashlib.sha256(builder.read_bytes()).hexdigest(),
       'checker_sha256': hashlib.sha256(checker.read_bytes()).hexdigest(), 'base_c2v004b_sha256': B0.BASE_B_SHA,
       'base_c2v004c_sha256': B0.BASE_C_SHA, 'reference_c2v004d_sha256': D_SHA, 'fill_utc': FILL, 'wall_cap_s': W,
       'builder_checks': 18, 'builder_failures': base_fails, 'checker_cases': cseen,
       'n': len(results), 'passed': sum(r['pass'] for r in results), 'results': results, 'mutants': killed}
with open(work / 'TEST_RECORD.json', 'x') as fh:
    fh.write(json.dumps(rec, indent=1, sort_keys=True) + '\n')
print(json.dumps({'n': rec['n'], 'passed': rec['passed'], 'builder_failures': base_fails,
                  'mutants_killed': sum(v['killed'] for v in killed.values()), 'of': len(killed)}))
