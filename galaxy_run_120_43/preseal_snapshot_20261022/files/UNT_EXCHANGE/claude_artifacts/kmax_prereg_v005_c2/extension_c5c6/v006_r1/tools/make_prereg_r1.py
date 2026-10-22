"""Build KMAX_MATRIX_PREREG_V006_R1.json (DRAFT, unsealed) from the bytes of the V006 draft (f90ab96c) by applying exactly
the findings of extension_c5c6/check/CHECK_V001.md (849d1b8d): M1, L1, L2, L3, L4.  Every sha written is computed here from
bytes.  Then writes the pinned compare successor: the PREREG_SHA256 placeholder line of prereg/kmax_compare_ext_c2v006_r1.py
is replaced by the R1 sha (only that line).  Writes v006_r1/prereg/KMAX_MATRIX_PREREG_V006_R1.json (must not exist).
usage: python3 -I -B make_prereg_r1.py"""
import copy
import hashlib
import importlib.util
import json
import os
import time
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
K5 = EX / 'kmax_prereg_v005_c2'
LANE = K5 / 'extension_c5c6'
OUT = LANE / 'v006_r1'
V006 = (LANE / 'prereg_v006/KMAX_MATRIX_PREREG_V006.json', 'f90ab96cc1640cb2bc4204489f3e44e9165eb1aaead9875e7a8e754c9e02eb79')
CMP6 = (LANE / 'prereg_v006/kmax_compare_ext_c2v006.py', 'e6475f3843e1b73a76ccaf8c9324cced6f9fe162d6b73c75c7ad61c6aeba261c')
TST6 = (LANE / 'prereg_v006/tests_kmax_compare_ext_c2v006.py', '87506f45d834855d33ebc57f6b131d51311af59cfb93c2b76950b21f0aa951af')
CHECK = (LANE / 'check/CHECK_V001.md', '849d1b8d1671fc01cd7e695fd1982c5d3f2124f9dcd3fae3a2a430f5884bb1b0')
EST = (LANE / 'analysis/ESTIMATES_V001.json', 'a51d62810550aa0664e5b324962075c2593663e141ff49c8d868f937c9e0a33f')
CL2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
EXT1 = '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext'
CMP_R1 = OUT / 'prereg/kmax_compare_ext_c2v006_r1.py'
PLACEHOLDER = "PREREG_SHA256 = '<R1_PREREG_SHA256>'"


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def pin(p):
    return {'path': str(p), 'sha256': sha(p)}


def pinned_json(p, s):
    if sha(p) != s:
        raise SystemExit('REFUSED pin %s' % p)
    return json.loads(Path(p).read_text())


def ext_state():
    """C5/C6 outdirs absent at build time (runs and runs_ext, by the symlink and by the External1 real path)."""
    names = []
    for root in (CL2 / 'runs', CL2 / 'runs_ext', Path(EXT1)):
        if root.is_dir():
            names += ['%s/%s' % (root, n) for n in os.listdir(root) if 'C5' in n or 'C6' in n]
    return {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'entries_naming_C5_or_C6': sorted(names),
            'roots_listed': [str(CL2 / 'runs'), str(CL2 / 'runs_ext'), EXT1]}


def main():
    pre = copy.deepcopy(pinned_json(*V006))
    for p, s in (CMP6, TST6, CHECK, EST):
        if sha(p) != s:
            raise SystemExit('REFUSED pin %s' % p)
    pre5 = pinned_json(pre['binding_inputs']['prereg_v005']['path'], pre['binding_inputs']['prereg_v005']['sha256'])
    c5p = pre['binding_inputs']['v005_compare']
    if sha(c5p['path']) != c5p['sha256']:
        raise SystemExit('REFUSED V005 compare pin')
    sp = importlib.util.spec_from_file_location('c5m', c5p['path'])
    C5M = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(C5M)
    specs = json.loads((OUT / 'specs/SPECS_EXT_M32.json').read_text())
    dry = OUT / 'dryrun/DRYRUN_R1_SUMMARY_V002.json'
    dryj = json.loads(dry.read_text())
    if not dryj['all_as_expected']:
        raise SystemExit('REFUSED: R1 dry runs not all as expected')
    st = ext_state()
    if st['entries_naming_C5_or_C6']:
        raise SystemExit('REFUSED: a C5/C6 entry exists: %s' % st['entries_naming_C5_or_C6'])

    # ------------------------------------------------------------------ header
    pre['revision'] = 'R1'
    pre['status'] = ('DRAFT_FOR_REVIEW R1 (not sealed).  Written 2026-10-17 as the successor of the V006 draft f90ab96c, applying '
                     'exactly the findings M1, L1, L2, L3, L4 of the independent check CHECK_V001 (849d1b8d); still before any C5/C6 '
                     'call exists (no outdir KMAX_A2F10_C5R3_RUN_V001 / KMAX_A2F10_C6R3_RUN_V001 / KMAX_A2F10_C5R3_N1_RUN_V001 / '
                     'KMAX_A2F10_C6R3_N1_RUN_V001 under runs or runs_ext; predates_state).  The seal (SEAL_RECORD_V006_R1: this file '
                     'sha + the compare successor kmax_compare_ext_c2v006_r1.py sha) is a separate act after review and before any '
                     'C5/C6 launch (SEAL_READY_V006_R1.json lists its preconditions).  Thresholds, statistics and gates are V005\'s '
                     'unchanged.')
    pre['supersedes_draft'] = {'prereg_v006_draft': {'path': str(V006[0]), 'sha256': V006[1]},
                               'compare_v006_draft': {'path': str(CMP6[0]), 'sha256': CMP6[1]},
                               'tests_v006_draft': {'path': str(TST6[0]), 'sha256': TST6[1]},
                               'note': 'the V006 draft was never sealed; R1 replaces it as the text to seal'}
    pre['predates_state'] = st
    pre['revision_r1'] = {
        'check': {'path': str(CHECK[0]), 'sha256': CHECK[1], 'verdict': 'PASS_WITH_DEFECTS (0 MAJOR, 1 MEDIUM, 4 LOW, 3 INFO)'},
        'applied': {
            'M1': ('cases[C5,C6].route_a_numerics.max_iterations 16 -> 32 (the c2v009 ceiling ROUTE_A_MAX_ITERATIONS_MAX), so the V3 gate '
                   'admits the budget the specs carry; specs regenerated with max_iterations 32 (v006_r1/specs, CALL_*_M32_C2V009.json; '
                   'leaf diff vs the superseded _M16 specs: /label and /numerics/route_a/max_iterations only); criterion.gates and '
                   'fixed_across_extension_cases.route_a_max_iterations restated; gate_next_steps.V1 (iii) restated for a budget '
                   'that is already the ceiling (the "rerun with max_iterations 32" branch is gone: it is the registered budget); '
                   'launch caps (LAUNCH_EXT_V002.json): output C5 96 GiB, C6 128 GiB, wall caps re-derived from ESTIMATES_V001 for '
                   '32 iterations.'),
            'L1': 'V3 for every prefix-bound case requires result sha256 == cases[].bound.result.sha256 when --bracket-recovery is the R3 block (compare successor).',
            'L2': ('V005\'s v005-admissibility condition is executed by the compare successor (binding_inputs.v005_admissibility); '
                   'a v005 case (C4, C3, R) not admissible fails V3 with V005_INADMISSIBLE and V005\'s inadmissible_next_step.'),
            'L3': ('V005\'s K0_max_rel_diff_vs_C2 and field_diagnostic are carried (criterion.diagnostics_reported; reported, not decided); '
                   '--no-field-diagnostic disables the ring diagnostic.'),
            'L4': 'cases[C5,C6].outdirs registers the primary N8 and alternate N1 outdirs (+ receipts) on the External1 real path.'},
        'not_applied': {'I1, I2, I3': 'INFO findings; no change requested', 'M1 (b)': 'the alternative fix (b) was not taken; fix (a) is applied'}}

    bi = pre['binding_inputs']
    # ------------------------------------------------------------------ L2
    dt = pre5['binding_inputs']['v005_deciding_test']
    v5 = C5M.v005_admissibility(pre5)
    bi['v005_admissibility'] = {
        'condition': pre5['amendment_v005']['driver']['admissibility_condition'],
        'condition_source': 'V005 amendment_v005.driver.admissibility_condition (prereg_v005 dbddc02c), carried verbatim',
        'executed_by': 'v005_admissibility(V005 prereg) of the pinned V005 compare (binding_inputs.v005_compare 49404bc4), called by the compare successor at comparison time',
        'deciding_test': {'result_path': dt['result_path'], 'finish_path': dt['finish_path'], 'required': dt['required']},
        'applies_to': 'every case whose driver_sha256 is v005 (C4, C3, R)',
        'inadmissible_next_step': pre5['amendment_v005']['driver']['inadmissible_next_step'],
        'state_at_r1_build': {'admissible': v5['admissible'], 'verdict': v5.get('verdict'), 'result_sha256': v5.get('result_sha256'),
                              'finish_sha256': v5.get('finish_sha256'), 'reason': v5.get('reason'),
                              'scope': 'TESTED at build time; the binding evaluation is the one at comparison time'}}
    # ------------------------------------------------------------------ cases: M1, L1, L4
    for c in pre['cases']:
        if c['prefix'] == 'bound':
            c['bound']['result_sha256_enforced'] = 'V3 term when --bracket-recovery equals the registered R3 block (CHECK_V001 L1); reported only under a later R(n)'
        if c['id'] in ('C5', 'C6'):
            c['route_a_numerics']['max_iterations'] = 32
            new = {}
            for var, key in (('primary_N8', '%s_N8' % c['id']), ('alternate_N1', '%s_N1' % c['id'])):
                s = specs['specs'][key]
                if sha(s['path']) != s['sha256']:
                    raise SystemExit('REFUSED spec pin %s' % key)
                new[var] = {'path': s['path'], 'sha256': s['sha256'], 'grid': s['grid'], 'route_a_column_workers': s['route_a_column_workers'],
                            'route_a_max_iterations': s['route_a_max_iterations'], 'override_key_lint': s['override_key_lint'],
                            'leaf_diff_vs_C4R3': s['leaf_diff_vs_C4R3'], 'brackets_equal_R3': s['brackets_equal_R3'],
                            'supersedes': s['supersedes'], 'leaf_diff_vs_superseded_M16': s['leaf_diff_vs_superseded_M16'],
                            'dry_run_v009': {'job': 'v009_%s_M32' % key, 'as_expected': dryj['jobs']['v009_%s_M32' % key]['as_expected'],
                                             'stages_planned': dryj['jobs']['v009_%s_M32' % key]['stages_planned'],
                                             'binding_blockers': dryj['jobs']['v009_%s_M32' % key]['binding_blockers'],
                                             'per_call_seed_sha256': dryj['jobs']['v009_%s_M32' % key]['seed']['sha256']}}
            c['specs'] = new
            n8 = '%s/KMAX_A2F10_%sR3_RUN_V001' % (EXT1, c['id'])
            n1 = '%s/KMAX_A2F10_%sR3_N1_RUN_V001' % (EXT1, c['id'])
            if c['outdir'] != n8:
                raise SystemExit('REFUSED: V006 primary outdir changed')
            c['outdirs'] = {'primary_N8': {'outdir': n8, 'receipt': n8 + '.receipt.json', 'spec': 'specs.primary_N8'},
                            'alternate_N1': {'outdir': n1, 'receipt': n1 + '.receipt.json', 'spec': 'specs.alternate_N1'},
                            'note': ('External1 real path (CLAUDE2/runs_ext is a symlink to it).  Exactly one result per case enters the '
                                     'CASES map; the compare reports which registered outdir it lies in (CHECK_V001 L4) and does not decide on it.')}
    # ------------------------------------------------------------------ V7 expectation note (M1)
    sm = {}
    for cid in ('C5', 'C6'):
        p = OUT / 'analysis/prep_smoke_m32' / cid / 'PREP_V009_SMOKE.json'
        old = json.loads(Path(pre['route_a_expected_inputs'][cid]['path']).read_text())
        if p.is_file():
            new = json.loads(p.read_text())
            eq = (new['expected_identity_inputs_sha256'] == old['expected_identity_inputs_sha256']
                  and new['expected_start_iteration_0000'] == old['expected_start_iteration_0000']
                  and new['node_diagnostics_iteration0_sha256'] == old['node_diagnostics_iteration0_sha256'])
            sm[cid] = {'path': str(p), 'sha256': sha(p), 'seed_sha256': new['seed']['sha256'], 'max_iterations': new['max_iterations'],
                       'verdict': new['verdict'], 'digests_equal_registered_expectation': eq, 'status': 'TESTED-POSITIVE' if (eq and new['verdict'] == 'PASS') else 'TESTED-NEGATIVE'}
        else:
            sm[cid] = {'status': 'UNTESTED', 'deciding_test': 'tools/prep_v009_smoke_c2ext.py on the M32 per-call seed'}
    pre['route_a_expected_inputs']['max_iterations_independence'] = {
        'claim': ('the registered expectations (made from the max_iterations-16 per-call seed) are the expectations for the R1 '
                  'max_iterations-32 seed: prep v009 names max_iterations only in the prepare_inputs signature (line 41) and never '
                  'uses it; the R1 per-call seed differs from the M16 seed only in numerical_inputs.max_iterations and its '
                  'c2_changed_fields mirror (dry-run seed leaf diff, DRYRUN_R1_SUMMARY_V002.json)'),
        'dry_run_summary': pin(dry),
        'operator_evaluation_on_M32_seed': sm}
    # ------------------------------------------------------------------ fixed / criterion text (M1, L1, L2, L3)
    fx = pre['fixed_across_extension_cases']
    fx['route_a_max_iterations'] = (
        '32 for C5 and C6 (seed numerical_inputs.max_iterations; base seed 8; 32 = the c2v009 ceiling).  The solvers use it only as the '
        'loop bound (for iteration in range(start_iteration, max_iterations), serial 44d9c23c:110, parallel aed4dd59:196), so a route A '
        'converging at iteration n computes the same arrays with any budget > n.  Reason for 32 (CHECK_V001 M1): measured prefixes '
        'converged at iterations 4/5/6 (K=2/3/4) with the late contraction ratio rising (G4: 0.45 -> 0.66; signed step projection mu '
        '0.45 -> 0.57, cos 0.95: a monotone slow mode, analysis/ROUTE_A_MODE_V001.json); the pessimistic G6 projection '
        '(analysis/ESTIMATES_V001.json) reaches residual/bound 1.14 at index 13 with ratios about 0.95, i.e. about 1.03 at index 15, '
        'not converged within 16; a 16-iteration checkpoint cannot be resumed with a larger budget (max_iterations is in the checkpoint '
        'identity controls), so the budget is set to the ceiling before the first call.  Superseded value: 16 (V006 draft f90ab96c).')
    cr = pre['criterion']
    cr['gates'] = ('V1-V5 exactly as V005 per_case_validity_gates (V3 against the registered block: V005 anchor physical/coefficients/picard, '
                   'the recovery block for every extension case, the registered grid, cube truncation, the case drivers_allowed with the '
                   'v009 admissibility condition for v009 cases and V005\'s v005 admissibility condition (binding_inputs.v005_admissibility) '
                   'for v005 cases, for every prefix-bound case under the R3 block its registered bound result sha256, and for C5/C6 '
                   'numerics.route_a.max_iterations 32 and column_workers in {1, 8}); V6 not applicable (no admitted extension case); '
                   'V7 (C5, C6): the route-A checkpoint IDENTITY.inputs_sha256 entries and the iteration_0000/START digests equal '
                   'route_a_expected_inputs (prep v009 operator evaluation of the registered per-call seed).')
    cr['diagnostics_reported'] = ('Carried from V005 (CHECK_V001 L3; V005: K0 drift between grids is reported, not hidden): '
                                  'K0_max_rel_diff_vs_C2 (max_i |K0_i(case)/K0_i(C2) - 1| of the final rotation stage base_K_values_SI) and '
                                  'field_diagnostic (V005 ring_diagnostic: the gravity-only ring indicator of each final field packet at the 12 '
                                  'row radii); both reported for every present case, neither used by X1-X4.  --no-field-diagnostic disables '
                                  'the ring diagnostic only.')
    rules = cr['decision_rule']
    rules[3] = rules[3].replace('route-A accepted iteration of C5/C6.',
                                'route-A accepted iteration of C5/C6, K0_max_rel_diff_vs_C2 and field_diagnostic (criterion.diagnostics_reported).')
    gs = cr['gate_next_steps']
    old_iii = ('(iii) route A without a converged fixed point within 16 iterations (ROUTE_A_NO_FIXED_POINT / ITERATION_BUDGET_EXHAUSTED): '
               'registered as a measured property of the route-A relaxation at that grid; next step: if the saved residual history contracts '
               'over its last 3 iterations, rerun with max_iterations 32 (v009 ceiling), else a reviewed study of the route-A relaxation '
               '(a relaxation change is a new prereg version);')
    if old_iii not in gs['V1']:
        raise SystemExit('REFUSED: V1 (iii) text not found')
    gs['V1'] = gs['V1'].replace(old_iii, (
        '(iii) route A without a converged fixed point within 32 iterations, the c2v009 ceiling (ROUTE_A_NO_FIXED_POINT / '
        'ITERATION_BUDGET_EXHAUSTED): registered as a measured property of the route-A relaxation at that grid; next step: if the saved '
        'residual history contracts over its last 3 iterations, a driver successor raising the route-A ceiling and its own prereg version '
        '(under separate review), else a reviewed study of the route-A relaxation (a relaxation change is a new prereg version); no rerun '
        'under V006 R1;'))
    gs['V3'] = ('Custody mismatch: regenerate the spec with v006_r1/tools/make_specs_r1.py from the registered block and rerun that case; '
                'a bound-result sha mismatch (C4, C3, C2, R under R3): restore the registered R3 result path in the CASES map (no rerun).  '
                'V005_INADMISSIBLE / V009_INADMISSIBLE: the respective inadmissible_next_step.')
    pre['resources_note'] = (pre['resources_note'].replace('Caps are launch parameters (LAUNCH_EXT_V001.json), not part of the rule.',
                                                           'Caps are launch parameters (v006_r1/LAUNCH_EXT_V002.json, route-A budget 32: output C5 96 GiB, C6 128 GiB; '
                                                           'wall caps from ESTIMATES_V001 at 32 iterations), not part of the rule.'))
    if 'LAUNCH_EXT_V002' not in pre['resources_note']:
        raise SystemExit('REFUSED: resources_note text not found')
    b = (json.dumps(pre, indent=1, allow_nan=False) + '\n').encode()
    p = OUT / 'prereg/KMAX_MATRIX_PREREG_V006_R1.json'
    with open(p, 'xb') as f:
        f.write(b)
    r1sha = hashlib.sha256(b).hexdigest()
    src = CMP_R1.read_text()
    if src.count(PLACEHOLDER) != 1:
        raise SystemExit('REFUSED: compare placeholder not found exactly once')
    with open(CMP_R1, 'w') as f:
        f.write(src.replace(PLACEHOLDER, "PREREG_SHA256 = '%s'" % r1sha))
    print('prereg R1', r1sha)
    print('compare R1', sha(CMP_R1))
    print('v005_admissibility', v5['admissible'], v5.get('verdict'))
    print('smoke m32', {k: v.get('status') for k, v in sm.items()})


if __name__ == '__main__':
    main()
