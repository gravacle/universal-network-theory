"""Mutation check for the NGC acceptance c2v001 build (synthetic only).

For each mutant: a new directory with the three modules and the suite copied, ONE exact textual change applied to one
module (the old text must occur exactly once), the sibling pins re-filled from bytes (enumerator sha into the adapter;
adapter and enumerator shas into the handoff) so that a mutant is never killed by a stale pin alone, then the full suite
is run in a fresh python3 -I -B process. A mutant is killed when at least one test fails; the killing test ids are
recorded beside the intended ones. A control copy (no change) must pass every test.
Usage: python3 -I -B mutation_ngc_acceptance_c2v001.py --out <new dir> [--module-dir <dir>]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

E, A, H, T = ('ngc_consumed_states_c2v001.py', 'ngc_lo_state_adapter_c2v001.py', 'ngc_acceptance_handoff_c2v001.py',
              'test_ngc_acceptance_c2v001.py')
MUTANTS = [
    ('M01_t_i_gate_removed', A, "        if ctx['rule_id'] is None:\n", "        if ctx['rule_id'] is None and False:\n", ['P16', 'P18']),
    ('M02_S4_partial_shell_dropped', A, '        elif lo < e_top:\n', '        elif False:\n', ['P02', 'P11']),
    ('M03_S4_off_strict_lo_core_tiling', A, '        if hi <= e_top:\n', '        if True:\n', ['P02', 'P11']),
    ('M04_S6_X_row_with_readout_excluded', A,
     'if in_x and reason.get(q) in AUTHORIZED_INVALID_REASONS and vmax[i] is None and not missing[i]:',
     'if in_x and reason.get(q) in AUTHORIZED_INVALID_REASONS and not missing[i]:', ['P06', 'F07']),
    ('M05_S6_missing_pass_list_ignored', A,
     '            missing = [True] * n                                        # a missing / malformed pass row list\n',
     '            pass\n', ['F08']),
    ('M06_monotone_fail_rule_off', A, "    if agg['fail_on_present']:\n",
     "    if agg['fail_on_present'] and not (missing_v or missing_t):\n", ['P08']),
    ('M07_threshold_0p005_to_0p05', A, 'PER_SHELL_MAX = 0.005', 'PER_SHELL_MAX = 0.05', ['P12', 'P13']),
    ('M08_C4b_gamma_check_off', A, "        need(rec['gamma_c4b']['bits_equal'], C_GAMMA,",
     "        need(True, C_GAMMA,", ['F06']),
    ('M09_unit_edges_check_off', A, '    need(np.array_equal(edges, expected_unit_edges()), C_GEOMETRY,',
     '    need(True, C_GEOMETRY,', ['F03']),
    ('M10_rho_10_key_compare_off', A, "        need(rec['rho_bitwise_equal_to_slot'], C_RHO,", "        need(True, C_RHO,", ['F14']),
    ('M11_certificate_as_rho_check_off', A,
     "    need(rr['sha256'] != registry['launch']['sha256'] and os.path.realpath(rr['path']) != os.path.realpath(registry['launch']['path']),",
     '    need(True,', ['F02']),
    ('M12_contract_token_scan_off', A, '    bad = _keys_with_tokens(c)\n', '    bad = []\n', ['F09']),
    ('M13_anchor_guard_off', A,
     "    need(rec.get('is_anchor') is False and 'ANCHOR' not in str(rec.get('reading')).upper()\n"
     "         and 'ANCHOR' not in str(rec.get('state_class')).upper(), C_ADMISSION,",
     '    need(True, C_ADMISSION,', ['F11']),
    ('M14_scope_text_guard_off', A,
     "    need(rec.get('scope_disclosure') == SCOPE_DISCLOSURE, C_ADMISSION,", '    need(True, C_ADMISSION,', ['F12']),
    ('M15_transient_without_non_iterate_pass', A,
     "    elif classes == {ITERATE} and all(s['verdict'] == 'PASS' for s in states if s['state_class'] != ITERATE):",
     '    elif classes == {ITERATE}:', ['P14']),
    ('M16_review_gate_off', A, "        raise Refusal(C_REVIEW, 'no trusted review for row contract %s' % contract_sha[:16])\n",
     '        return None\n', ['F13']),
    ('M17_enumerator_iterate_read_as_route_b', E, '        elif r <= set(ITERATE_ROLES):\n            cls = ITERATE\n',
     '        elif r <= set(ITERATE_ROLES):\n            cls = ROUTE_B\n', ['P01', 'P13']),
    ('M18_enumerator_missing_iterates_not_blocking', E,
     "        if route_a_iterates_ref is None:\n            inv['blockers'].append(",
     "        if route_a_iterates_ref is None:\n            [].append(", ['F18']),
    ('M19_handoff_route_b_fail_not_decisive', H, "    if any(e['class'] in DECISIVE for e in failed):\n",
     '    if False:\n', ['P19']),
    ('M20_handoff_adoption_guard_off', H, '            A.guard_state_record(r)  ', '            (lambda r: r)(r)  ', ['F12']),
    ('M21_handoff_receipt_gate_off', H,
     "        if not (is_pin(policy.get('receipt')) and receipt_ok(policy['receipt'], rec['result']['sha256'])):",
     '        if False:', ['F23']),
    ('M22_S7_own_radius_check_off', A,
     "                        need(own is not None and bits(own) == bits(contract['R_m'][i]), C_CONTRACT,",
     '                        need(True, C_CONTRACT,', ['F15']),
    ('M23_B1_reproduce_check_off', A, '    need(not np.max(relative) > B1_RELATIVE_CHECK, C_INPUT,', '    need(True, C_INPUT,', ['F21']),
    ('M24_S5_digest_check_off', A, "U.TailState.from_arrays(arrays, record, expected_digest=state['state_sha256'])",
     'U.TailState.from_arrays(arrays, record, expected_digest=None)', ['F16']),
    ('M25_blas_single_thread_check_off', A, "        need(all(os.environ.get(k) == '1' for k in THREAD_ENV), C_RHO,",
     '        need(True, C_RHO,', ['F25']),
]


def rd(p):
    with open(p, 'rb') as f:
        return f.read()


def wr(p, raw):
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def build(src, dst, target=None, old=None, new=None):
    os.mkdir(dst)
    files = {n: rd(os.path.join(src, n)) for n in (E, A, H, T)}
    e0, a0 = sha(files[E]), sha(files[A])
    if target is not None:
        n = files[target].count(old.encode())
        if n != 1:
            raise SystemExit('MUTANT_ANCHOR_NOT_UNIQUE (%d): %s' % (n, old[:80]))
        files[target] = files[target].replace(old.encode(), new.encode())
    e1 = sha(files[E])
    if e1 != e0:
        assert files[A].count(e0.encode()) == 1 and files[H].count(e0.encode()) == 1
        files[A] = files[A].replace(e0.encode(), e1.encode())
        files[H] = files[H].replace(e0.encode(), e1.encode())
    a1 = sha(files[A])
    if a1 != a0:
        assert files[H].count(a0.encode()) == 1
        files[H] = files[H].replace(a0.encode(), a1.encode())
    for n, raw in files.items():
        wr(os.path.join(dst, n), raw)
    return {n: sha(raw) for n, raw in files.items()}


def run_suite(d):
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, T), '--run-dir', os.path.join(d, 'run')],
                       capture_output=True, text=True, timeout=1800)
    try:
        res = json.loads(rd(os.path.join(d, 'run', 'SUITE_RESULTS_C2V001.json')))
    except (OSError, ValueError):
        return {'exit': p.returncode, 'failed': ['SUITE_DID_NOT_COMPLETE'], 'stderr_tail': p.stderr[-800:]}
    return {'exit': p.returncode, 'failed': [r['id'].split()[0] for r in res['results'] if not r['ok']],
            'must_pass': res['must_pass'], 'must_fail': res['must_fail']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--module-dir', default=os.path.dirname(os.path.realpath(__file__)))
    a = ap.parse_args()
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        raise SystemExit('python3 -I -B required')
    out = os.path.realpath(a.out)
    os.mkdir(out)
    src = os.path.realpath(a.module_dir)
    report = {'schema': 'NGC_ACCEPTANCE_C2V001_MUTATION_RESULTS', 'synthetic_only': True,
              'source_shas': {n: sha(rd(os.path.join(src, n))) for n in (E, A, H, T)}, 'mutants': []}
    ctl = os.path.join(out, 'M00_control')
    report['control'] = dict(run_suite(ctl) if build(src, ctl) else {}, shas=None)
    for mid, target, old, new, intended in MUTANTS:
        d = os.path.join(out, mid)
        shas = build(src, d, target, old, new)
        r = run_suite(d)
        r.update(id=mid, target=target, intended=intended, killed=bool(r['failed']),
                 killed_by_intended=any(t in r['failed'] for t in intended), mutant_shas=shas)
        report['mutants'].append(r)
        print('%s killed=%s by=%s' % (mid, r['killed'], r['failed'][:6]), flush=True)
    report['summary'] = {'control_clean': report['control'].get('failed') == [],
                         'killed': '%d/%d' % (sum(m['killed'] for m in report['mutants']), len(report['mutants'])),
                         'killed_by_intended': '%d/%d' % (sum(m['killed_by_intended'] for m in report['mutants']),
                                                          len(report['mutants']))}
    raw = (json.dumps(report, indent=1, sort_keys=True) + '\n').encode()
    wr(os.path.join(out, 'MUTATION_RESULTS_C2V001.json'), raw)
    print(json.dumps(dict(report['summary'], results_sha256=sha(raw))))
    return 0 if report['summary']['control_clean'] and all(m['killed'] for m in report['mutants']) else 1


if __name__ == '__main__':
    sys.exit(main())
