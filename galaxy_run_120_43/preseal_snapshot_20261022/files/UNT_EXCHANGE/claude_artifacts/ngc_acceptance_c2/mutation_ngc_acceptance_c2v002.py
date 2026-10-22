"""Mutation check for the NGC acceptance c2v002 build (synthetic only).

For each mutant: a new directory with the three modules (adapter c2v002, the unchanged enumerator c2v001, handoff c2v002)
and the suite copied, ONE logical change applied to one module (each listed old text must occur exactly once; a mutant
may list several anchors when the change spans non-adjacent lines), the sibling pins re-filled from bytes (enumerator sha
into the adapter and the handoff; adapter sha into the handoff) so that a mutant is never killed by a stale pin alone,
then the full suite is run in a fresh python3 -I -B process. A mutant is killed when at least one test fails; the
killing test ids are recorded beside the intended ones. A control copy (no change) must pass every test.
M01-M25 are the c2v001 mutants carried to c2v002 (M06 adapted: the per-row missing-t path is gone); M26-M43 cover the
A155 delta and the B1 fix (M26 restores the c2v001 empty-row-set PASS).
Usage: python3 -I -B mutation_ngc_acceptance_c2v002.py --out <new dir> [--module-dir <dir>]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

E, A, H, T = ('ngc_consumed_states_c2v001.py', 'ngc_lo_state_adapter_c2v002.py', 'ngc_acceptance_handoff_c2v002.py',
              'test_ngc_acceptance_c2v002.py')
G_LINE = '            g = (v * KM_S_TO_M_S) ** 2 * R * rho * b1 / den            # A155 ratio form (= d / t_i), evaluated\n'
MUTANTS = [
    ('M01_t_i_gate_removed', A, [("        if ctx['rule_id'] is None:\n", "        if ctx['rule_id'] is None and False:\n")],
     ['F10']),
    ('M02_S4_partial_shell_dropped', A, [('        elif lo < e_top:\n', '        elif False:\n')], ['P02', 'P11']),
    ('M03_S4_off_strict_lo_core_tiling', A, [('        if hi <= e_top:\n', '        if True:\n')], ['P02', 'P11']),
    ('M04_S6_X_row_with_readout_excluded', A,
     [('if in_x and reason.get(q) in AUTHORIZED_INVALID_REASONS and vmax[i] is None and not missing[i]:',
       'if in_x and reason.get(q) in AUTHORIZED_INVALID_REASONS and not missing[i]:')], ['P06', 'F07']),
    ('M05_S6_missing_pass_list_ignored', A,
     [('            missing = [True] * n                                        # a missing / malformed pass row list\n',
       '            pass\n')], ['F08']),
    ('M06_monotone_fail_rule_off', A, [("    if agg['fail_on_present']:\n",
                                        "    if agg['fail_on_present'] and not missing_v:\n")], ['P08']),
    ('M07_threshold_0p005_to_0p05', A, [('PER_SHELL_MAX = 0.005', 'PER_SHELL_MAX = 0.05')], ['P12', 'P13']),
    ('M08_C4b_gamma_check_off', A, [("        need(rec['gamma_c4b']['bits_equal'], C_GAMMA,", "        need(True, C_GAMMA,")],
     ['F06']),
    ('M09_unit_edges_check_off', A, [('    need(np.array_equal(edges, expected_unit_edges()), C_GEOMETRY,',
                                      '    need(True, C_GEOMETRY,')], ['F03']),
    ('M10_rho_10_key_compare_off', A, [("        need(rec['rho_bitwise_equal_to_slot'], C_RHO,", "        need(True, C_RHO,")],
     ['F14']),
    ('M11_certificate_as_rho_check_off', A,
     [("    need(rr['sha256'] != registry['launch']['sha256'] and os.path.realpath(rr['path']) != os.path.realpath(registry['launch']['path']),",
       '    need(True,')], ['F02']),
    ('M12_contract_token_scan_off', A, [('    bad = _keys_with_tokens(c)\n', '    bad = []\n')], ['F09', 'F26']),
    ('M13_anchor_guard_off', A,
     [("    need(rec.get('is_anchor') is False and 'ANCHOR' not in str(rec.get('reading')).upper()\n"
       "         and 'ANCHOR' not in str(rec.get('state_class')).upper(), C_ADMISSION,",
       '    need(True, C_ADMISSION,')], ['F11']),
    ('M14_scope_text_guard_off', A,
     [("    need(rec.get('scope_disclosure') == SCOPE_DISCLOSURE, C_ADMISSION,", '    need(True, C_ADMISSION,')], ['F12']),
    ('M15_transient_without_non_iterate_pass', A,
     [("    elif classes == {ITERATE} and all(s['verdict'] == 'PASS' for s in states if s['state_class'] != ITERATE):",
       '    elif classes == {ITERATE}:')], ['P14']),
    ('M16_review_gate_off', A, [("        raise Refusal(C_REVIEW, 'no trusted review for row contract %s' % contract_sha[:16])\n",
                                 '        return None\n')], ['F13']),
    ('M17_enumerator_iterate_read_as_route_b', E, [('        elif r <= set(ITERATE_ROLES):\n            cls = ITERATE\n',
                                                    '        elif r <= set(ITERATE_ROLES):\n            cls = ROUTE_B\n')],
     ['P01', 'P13']),
    ('M18_enumerator_missing_iterates_not_blocking', E,
     [("        if route_a_iterates_ref is None:\n            inv['blockers'].append(",
       "        if route_a_iterates_ref is None:\n            [].append(")], ['F18']),
    ('M19_handoff_route_b_fail_not_decisive', H, [("    if any(e['class'] in DECISIVE for e in failed):\n", '    if False:\n')],
     ['P19']),
    ('M20_handoff_adoption_guard_off', H, [('            A.guard_state_record(r)  ', '            (lambda r: r)(r)  ')],
     ['F12']),
    ('M21_handoff_receipt_gate_off', H,
     [("        if not (is_pin(policy.get('receipt')) and receipt_ok(policy['receipt'], rec['result']['sha256'])):",
       '        if False:')], ['F23']),
    ('M22_S7_own_radius_check_off', A,
     [("                        need(own is not None and bits(own) == bits(contract['R_m'][i]), C_CONTRACT,",
       '                        need(True, C_CONTRACT,')], ['F15']),
    ('M23_B1_reproduce_check_off', A, [('    need(not np.max(relative) > B1_RELATIVE_CHECK, C_INPUT,', '    need(True, C_INPUT,')],
     ['F21']),
    ('M24_S5_digest_check_off', A, [("U.TailState.from_arrays(arrays, record, expected_digest=state['state_sha256'])",
                                     'U.TailState.from_arrays(arrays, record, expected_digest=None)')], ['F16']),
    ('M25_blas_single_thread_check_off', A, [("        need(all(os.environ.get(k) == '1' for k in THREAD_ENV), C_RHO,",
                                              '        need(True, C_RHO,')], ['F25']),
    # ---- A155 delta and the B1 fix
    ('M26_empty_row_set_reads_PASS_c2v001_defect', A,
     [("    if not in_set or agg['row_set_empty']:\n        return 'UNAVAILABLE', [C_EMPTY], False\n",
       "    if False:\n        return 'UNAVAILABLE', [C_EMPTY], False\n"),
      ("    if not agg['rows_in_arithmetic'] or not _num(agg['G']):\n", '    if False:\n'),
      ('        total, fail = None, False ', '        total, fail = 0.0, False ')], ['F32']),
    ('M27_guard_decided_without_arithmetic_off', A,
     [("        need(isinstance(ria, list) and len(ria) > 0 and _num(rec.get('G')) and rec.get('t_rule_id') == RULE_ID,\n",
       '        need(True,\n')], ['F32']),
    ('M28_zero_speed_rows_dropped', A,
     [("    calc = [r for r in rows if r['status'] in (ROW_INCLUDED, ROW_MISSING) and r['v'] is not None]\n",
       "    calc = [r for r in rows if r['status'] in (ROW_INCLUDED, ROW_MISSING) and r['v']]\n")], ['F31']),
    ('M29_zero_speed_flag_off', A, [("    zero_speed = [r['id'] for r in calc if r['v'] == 0.0]\n", '    zero_speed = []\n')],
     ['F31']),
    ('M30_zero_speed_refused', A, [("    _finite(v, 'speeds', nonnegative=True)\n", "    _finite(v, 'speeds', positive=True)\n")],
     ['F31']),
    ('M31_contract_theta_bits_check_off', A, [("    if bits(float.fromhex(c['theta_hex'])) != bits(THETA):\n", '    if False:\n')],
     ['F27']),
    ('M32_state_c_bits_check_off', A, [("        need(_num(cs) and bits(cs) == bits(call['c']), C_RULE,\n",
                                        '        need(True, C_RULE,\n')], ['F27']),
    ('M33_contract_c_bits_check_off', A, [("    if bits(float.fromhex(c['c_hex'])) != bits(C_M_S):\n", '    if False:\n')],
     ['F27']),
    ('M34_N_min_factor_in_g', A, [(G_LINE, G_LINE.replace('/ den   ', '/ den * 1.5'))], ['F28', 'P23']),
    ('M35_per_shell_1_over_k_s_in_g', A, [(G_LINE, G_LINE.replace('/ den   ', '/ den / lo'))], ['F29', 'P23']),
    ('M36_km_s_to_m_s_conversion_dropped', A, [(G_LINE, G_LINE.replace('(v * KM_S_TO_M_S) ** 2', 'v ** 2'))],
     ['F33', 'P12']),
    ('M37_t_i_entry_text_check_off', A,
     [("            need(text in ti, C_ADMISSION, 't_i entry: %s not found verbatim (A155 rule TI_B_SCALE_R_V001)' % name)\n",
       "            need(True, C_ADMISSION, 'x')\n")], ['F10']),
    ('M38_pass_meaning_guard_off', A, [("    need(rec.get('pass_meaning') == PASS_MEANING, C_ADMISSION,", '    need(True, C_ADMISSION,')],
     ['F12']),
    ('M39_stored_t_guard_off', A, [("    need(not _keys_named(rec, T_VALUE_KEYS), C_ADMISSION,", '    need(True, C_ADMISSION,')],
     ['F26']),
    ('M40_handoff_pass_meaning_check_off', H,
     [("        need(call_rec.get('pass_meaning') == A.PASS_MEANING, 'CALL_RECORD_WITHOUT_THE_E_A155_1_PASS_MEANING')\n",
       '        pass\n')], ['F12']),
    ('M41_contract_exact_keys_off', A, [('    need(set(c) <= keys and set(c) >= keys - set(CONTRACT_RULE_KEYS), C_CONTRACT,',
                                         '    need(True, C_CONTRACT,')], ['F26', 'F29']),
    ('M42_t_i_entry_unpinned', A,
     [("T_I_ENTRY = {'path': V006, 'heading': '## A155',\n"
       "             'section_sha256': 'ed6b144b66837069c4febf81a4feaf11c160f9be5f26d914d4c40041b60f3c9d'}\n",
       'T_I_ENTRY = None\n')], ['P16', 'P18']),
    ('M43_foreign_rule_id_accepted', A, [("    if rule_id is None or c['rule_id'] != rule_id:\n", '    if rule_id is None:\n')],
     ['F10']),
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


def build(src, dst, target=None, changes=()):
    os.mkdir(dst)
    files = {n: rd(os.path.join(src, n)) for n in (E, A, H, T)}
    e0, a0 = sha(files[E]), sha(files[A])
    for old, new in changes:
        n = files[target].count(old.encode())
        if n != 1 or old == new:
            raise SystemExit('MUTANT_ANCHOR_NOT_UNIQUE_OR_NO_CHANGE (%d): %s' % (n, old[:80]))
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
        res = json.loads(rd(os.path.join(d, 'run', 'SUITE_RESULTS_C2V002.json')))
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
    report = {'schema': 'NGC_ACCEPTANCE_C2V002_MUTATION_RESULTS', 'synthetic_only': True,
              'source_shas': {n: sha(rd(os.path.join(src, n))) for n in (E, A, H, T)}, 'mutants': []}
    ctl = os.path.join(out, 'M00_control')
    report['control'] = dict(run_suite(ctl) if build(src, ctl) else {}, shas=None)
    for mid, target, changes, intended in MUTANTS:
        d = os.path.join(out, mid)
        shas = build(src, d, target, changes)
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
    wr(os.path.join(out, 'MUTATION_RESULTS_C2V002.json'), raw)
    print(json.dumps(dict(report['summary'], results_sha256=sha(raw))))
    return 0 if report['summary']['control_clean'] and all(m['killed'] for m in report['mutants']) else 1


if __name__ == '__main__':
    sys.exit(main())
