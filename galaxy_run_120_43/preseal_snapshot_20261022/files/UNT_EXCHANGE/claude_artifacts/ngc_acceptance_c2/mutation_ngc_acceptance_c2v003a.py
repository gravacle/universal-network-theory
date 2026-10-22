"""Mutation check for the NGC acceptance c2v003a round (c2v003 + A167; synthetic only): the adapter c2v003a and handoff
c2v003a replace c2v002 and c2v003; the reader, S5 tool, contract and builder are the c2v003 files. M01-M72 are the c2v003
mutants carried; M73-M75 cover A167. The adapter sha is re-filled into the handoff only (the builder pins c2v002 and is
not re-pinned). The c2v003 text follows.

Mutation check for the NGC acceptance c2v003 build (synthetic only).

For each mutant: a new directory with the modules (adapter c2v002 and enumerator c2v001, unchanged; handoff, iterate
reader, S5 tool and contract builder c2v003), the built contract NGC_ROW_CONTRACT_C2V001.json and the suite copied, ONE
logical change applied to one module (each listed old text must occur exactly once; a mutant may list several anchors
when the change spans non-adjacent lines), the sibling pins re-filled from bytes so that a mutant is never killed by a
stale pin alone (enumerator sha -> adapter, handoff; adapter sha -> handoff, contract builder; S5 sha -> reader, handoff;
reader sha -> handoff), then the full suite is run in a fresh python3 -I -B process. A mutant is killed when at least one
test fails; the killing test ids are recorded beside the intended ones. A control copy (no change) must pass every test.
M01-M43 are the c2v002 mutants carried to c2v003 (the handoff anchors now in handoff c2v003); M44-M72 cover A162 items
1-6 (M71 with the F34 last_current variant).
Usage: python3 -I -B mutation_ngc_acceptance_c2v003a.py --out <new dir> [--module-dir <dir>]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

E, A, H = 'ngc_consumed_states_c2v001.py', 'ngc_lo_state_adapter_c2v003a.py', 'ngc_acceptance_handoff_c2v003a.py'
R, S, C = 'ngc_route_a_iterates_c2v003.py', 'ngc_s5_rebuild_export_c2v003.py', 'ngc_row_contract_c2v003.py'
T, K = 'test_ngc_acceptance_c2v003a.py', 'NGC_ROW_CONTRACT_C2V001.json'
FILES = (E, A, H, R, S, C, T, K)
G_LINE = '            g = (v * KM_S_TO_M_S) ** 2 * R * rho * b1 / den            # A155 ratio form (= d / t_i), evaluated\n'
SRB_CALL = '                                                   lib=lib, rowmod=rowmod)\n'
MUTANTS = [
    # ---- c2v002 mutants, carried (adapter c2v002 and enumerator c2v001 unchanged; handoff anchors in c2v003)
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
    # ---- A162 item 1: the route-A iterate reader
    ('M44_reader_monitor_next_state_dropped', R,
     [("        occ.append({'iteration': n, 'role': NEXT, 'state_sha256': p['next_state_digest']})\n", '')],
     ['P25', 'P26', 'P17']),
    ('M45_reader_file_sha_unchecked', R, [('    if sha is not None:\n', '    if False:\n')], ['F34']),
    ('M46_reader_iteration_range_unchecked', R, [('    need(its == set(range(a + 1)) and els == set(range(a + 1)), C_READ,',
                                                 '    need(True, C_READ,')], ['F34']),
    ('M47_reader_identity_sha_unchecked', R,
     [("    need(isinstance(ident, dict) and ident_doc['identity_sha256'] == hashlib.sha256(canonical(ident)).hexdigest(), C_READ,",
       '    need(isinstance(ident, dict), C_READ,')], ['F34']),
    ('M48_reader_list_occurrence_equality_off', R,
     [("    need(isinstance(occ, list) and [{k: o.get(k) for k in ('iteration', 'role', 'state_sha256')} if isinstance(o, dict)\n"
       "                                    else None for o in occ] == enum['occurrences'], C_LIST,",
       '    need(isinstance(occ, list), C_LIST,')], ['F35']),
    ('M49_reader_write_list_admission_not_state_bound', R,
     [("            adm = S5.verify_admission(ref, call_result=enum['call_result'], state_sha256=d, recheck_digest=True)",
       "            adm = S5.verify_admission(ref, call_result=enum['call_result'], recheck_digest=True)")], ['F36']),
    ('M50_reader_list_source_check_off', R,
     [("            need(src == adm['rebuilt']['roster_digest'], C_LIST, 'ITERATE_SOURCE_IS_NOT_THE_ADMITTED_ROSTER')",
       "            need(True, C_LIST, 'ITERATE_SOURCE_IS_NOT_THE_ADMITTED_ROSTER')")], ['F35']),
    # ---- A162 item 2: the S5 rebuild-export tool
    ('M51_s5_digest_equality_off', S,
     [("        need(adm['digest_equal'], C_DIGEST, ", "        need(True, C_DIGEST, ")], ['F37']),
    ('M52_s5_recorded_roster_check_off', S, [('        need(recorded is None or rd == recorded, C_ROSTER,',
                                              '        need(True, C_ROSTER,')], ['F37']),
    ('M53_s5_recipe_approval_off', S, [("             and recipe_ref['sha256'] in set(approved_recipe_sha256), C_RECIPE,",
                                        '             , C_RECIPE,')], ['F37', 'F36']),
    ('M54_s5_accepted_state_rebuilt', S, [("    need(st['state_sha256'] != accepted, C_ACCEPTED,", '    need(True, C_ACCEPTED,')],
     ['F37']),
    ('M55_s5_verify_export_off', S,
     [("    obj = strict_json(read_pin(ref, C_VERIFY, 'state input'), 'state input', C_VERIFY)\n",
       "    return {'admission': None, 'timing_seconds': None}\n")], ['F37']),
    ('M56_s5_export_identity_check_off', S,
     [("    need(state['state_sha256'] == rb['state_digest'] and state['source_sha256'] == rb['roster_digest']\n"
       "         and state['stage_kind'] == rb['stage_kind'], C_VERIFY,", '    need(True, C_VERIFY,')], ['F37']),
    # ---- A162 item 4: execution facts
    ('M57_handoff_execution_refusal_off', H, [('        if bad:\n', '        if False:\n')], ['F39']),
    ('M58_handoff_retried_ignores_retries', H, [('        if len(stages) > 1 or (type(retries) is int and retries != 0):',
                                                 '        if len(stages) > 1:')], ['F39']),
    ('M59_handoff_resumed_ignores_start_iteration', H, [("value('--start-iteration') == '0'", 'True')], ['F39']),
    ('M60_handoff_completed_normally_is_true_relaxed', H,
     [("                and outcome.get('converged_finite_fixed_point') is True and mode == 'computed')",
       "                and mode == 'computed')")], ['F39']),
    # ---- A162 item 5: SRB-ROT report-only
    ('M61_handoff_srb_unavailable_gates', H,
     [(SRB_CALL, SRB_CALL + "            if rec['srb_rot_report']['status'] != 'COMPUTED':\n"
                            "                rec['reading'] = 'INCOMPLETE'\n")], ['P32', 'F40']),
    ('M62_handoff_srb_bound_gates', H,
     [(SRB_CALL, SRB_CALL + "            if rec['srb_rot_report']['status'] == 'COMPUTED' and max(b for b in json.loads(open("
                            "rec['srb_rot_report']['report']['path']).read())['bound_km_s'] if b is not None) > 1.0:\n"
                            "                rec['reading'] = 'INCOMPLETE'\n")], ['P32']),
    ('M63_handoff_srb_label_changed', H, [("SRB_LABEL = 'report-only: no registered NGC tau'", "SRB_LABEL = 'report-only'")],
     ['P31']),
    # ---- A162 item 6: S2 pins
    ('M64_handoff_s2_pending_ignored', H, [('    if pending:\n', '    if False:\n')], ['F41', 'P18']),
    ('M65_handoff_registered_s2_check_off', H, [("            need(s2_pins == S2_PINS, 'S2_PINS_NOT_THE_MODULE_CONSTANTS')",
                                                 "            need(True, 'S2_PINS_NOT_THE_MODULE_CONSTANTS')")], ['F41']),
    # ---- A162 item 3: the contract (handoff pin, builder)
    ('M66_handoff_policy_contract_check_off', H,
     [("        need(policy.get('row_contract') is None or policy['row_contract'] == contract_pin,",
       '        need(True,')], ['F38']),
    ('M67_contract_builder_radius_rule_changed', C,
     [("        x = float(r['Rad_text']) * KPC_M ", "        x = float(r['Rad_text']) * KPC_M * (1 + 1e-12) ")], ['P29', 'F38']),
    ('M68_contract_builder_column_check_off', C,
     [("    need(man.get('emitted_columns') == MANIFEST_COLUMNS and man.get('no_other_columns_emitted') is True,",
       '    need(True,')], ['F38']),
    # ---- A162 items 1-2 at the handoff
    ('M69_handoff_export_verification_off', H,
     [("                    v = S.verify_export(ref, call_result=rec['result'], state=s)\n",
       "                    v = {'admission': None}\n")], ['F37']),
    ('M70_handoff_iterate_list_verification_off', H,
     [("            rec['route_a_iterates'] = R.verify_iterate_list(iter_ref, rec['call_dir'], driver_sha256=registry['driver']['sha256'])['list']",
       "            rec['route_a_iterates'] = iter_ref")], ['F35']),
    ('M71_reader_boundary_vs_last_current_unchecked', R,
     [("    need(payloads[a]['state_digest'] == boundary == rec.get('boundary_state_digest_at_return'), C_READ,",
       '    need(True, C_READ,')], ['F34']),
    ('M72_handoff_contract_registered_check_off', H,
     [("            need(contract_pin == ROW_CONTRACT, 'ROW_CONTRACT_NOT_THE_PINNED_CONTRACT')",
       "            need(True, 'ROW_CONTRACT_NOT_THE_PINNED_CONTRACT')")], ['F38']),
    # ---- A167: C4b on the spec route; S2 schema strings *_C3V003
    ('M73_c4b_theta_route_substituted_for_spec_route', A,
     [("bits_equal=routes['state_gamma_eff_hex'] == routes['spec_route_gamma_eff_hex'],",
       "bits_equal=routes['state_gamma_eff_hex'] == routes['theta_route_gamma_eff_hex'],")], ['P35', 'F06']),
    ('M74_c4b_all_three_routes_required_c2v002', A,
     [("bits_equal=routes['state_gamma_eff_hex'] == routes['spec_route_gamma_eff_hex'],",
       "bits_equal=len({routes['state_gamma_eff_hex'], routes['spec_route_gamma_eff_hex'], routes['theta_route_gamma_eff_hex']}) == 1,")],
     ['P35']),
    ('M75_s2_schema_strings_back_to_c3v001', A,
     [("SLOT_PROOF_SCHEMA = 'UNT_NGC_POINT_LO_SLOT_PROOF_C3V003'", "SLOT_PROOF_SCHEMA = 'UNT_NGC_POINT_LO_SLOT_PROOF_C3V001'"),
      ("RHO_SCHEMA = 'UNT_NGC_POINT_RHO_NUMERICAL_C3V003'", "RHO_SCHEMA = 'UNT_NGC_POINT_RHO_NUMERICAL_C3V001'"),
      ("RHO_IDENTITY_SCHEMA = 'UNT_NGC_POINT_RHO_IDENTITY_C3V003'", "RHO_IDENTITY_SCHEMA = 'UNT_NGC_POINT_RHO_IDENTITY_C3V001'")],
     ['F42']),
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


def refill(files, old, new, targets):
    for t in targets:
        assert files[t].count(old.encode()) == 1, (t, old[:12])
        files[t] = files[t].replace(old.encode(), new.encode())


def build(src, dst, target=None, changes=()):
    os.mkdir(dst)
    files = {n: rd(os.path.join(src, n)) for n in FILES}
    e0, a0, s0, r0 = sha(files[E]), sha(files[A]), sha(files[S]), sha(files[R])
    for old, new in changes:
        n = files[target].count(old.encode())
        if n != 1 or old == new:
            raise SystemExit('MUTANT_ANCHOR_NOT_UNIQUE_OR_NO_CHANGE (%d): %s' % (n, old[:80]))
        files[target] = files[target].replace(old.encode(), new.encode())
    e1 = sha(files[E])
    if e1 != e0:
        refill(files, e0, e1, (A, H))
    a1 = sha(files[A])
    if a1 != a0:
        refill(files, a0, a1, (H,))
    s1 = sha(files[S])
    if s1 != s0:
        refill(files, s0, s1, (R, H))
    r1 = sha(files[R])
    if r1 != r0:
        refill(files, r0, r1, (H,))
    for n, raw in files.items():
        wr(os.path.join(dst, n), raw)
    return {n: sha(raw) for n, raw in files.items()}


def run_suite(d):
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, T), '--run-dir', os.path.join(d, 'run')],
                       capture_output=True, text=True, timeout=3600)
    try:
        res = json.loads(rd(os.path.join(d, 'run', 'SUITE_RESULTS_C2V003A.json')))
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
    report = {'schema': 'NGC_ACCEPTANCE_C2V003A_MUTATION_RESULTS', 'synthetic_only': True,
              'source_shas': {n: sha(rd(os.path.join(src, n))) for n in FILES}, 'mutants': []}
    ctl = os.path.join(out, 'M00_control')
    report['control'] = dict(run_suite(ctl) if build(src, ctl) else {}, shas=None)
    for mid, target, changes, intended in MUTANTS:
        d = os.path.join(out, mid)
        shas = build(src, d, target, changes)
        r = run_suite(d)
        r.update(id=mid, target=target, intended=intended, killed=bool(r['failed']),
                 killed_by_intended=any(t in r['failed'] for t in intended) if intended else None, mutant_shas=shas)
        report['mutants'].append(r)
        print('%s killed=%s by=%s' % (mid, r['killed'], r['failed'][:6]), flush=True)
    graded = [m for m in report['mutants'] if m['intended']]
    report['summary'] = {'control_clean': report['control'].get('failed') == [],
                         'killed': '%d/%d' % (sum(m['killed'] for m in report['mutants']), len(report['mutants'])),
                         'killed_by_intended': '%d/%d' % (sum(m['killed_by_intended'] is True for m in graded), len(graded)),
                         'no_intended_test (exploratory)': [m['id'] for m in report['mutants'] if not m['intended']]}
    raw = (json.dumps(report, indent=1, sort_keys=True) + '\n').encode()
    wr(os.path.join(out, 'MUTATION_RESULTS_C2V003A.json'), raw)
    print(json.dumps(dict(report['summary'], results_sha256=sha(raw))))
    return 0 if report['summary']['control_clean'] and all(m['killed'] for m in report['mutants']) else 1


if __name__ == '__main__':
    sys.exit(main())
