"""Tests of the V006 R1 extension decision (kmax_compare_ext_c2v006_r1).  Successor of tests_kmax_compare_ext_c2v006.py
(87506f45): its 17 tests (T1-T17) are kept with the R1 route-A budget (synthetic C5/C6 carry max_iterations 32; T7 now checks
that 16 is REJECTED), plus tests of each CHECK_V001 finding applied in R1 (T18-T29).
C4/C3/C2/R adapted records are the REAL R3 results (read-only); C5/C6 are synthetic copies of C4's record with the registered
grid, driver, route_a numerics and rows C4 + delta*tau (no observed velocity is used anywhere: tau comes from the prereg).
End-to-end CLI runs use the real R3 bytes (C5, C6 absent -> INCOMPLETE).  Writes only into OUT (must not exist).
usage: python3 -I -B tests_kmax_compare_ext_c2v006_r1.py OUT"""
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
PRE = HERE / 'KMAX_MATRIX_PREREG_V006_R1.json'
CMP = HERE / 'kmax_compare_ext_c2v006_r1.py'
V006 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6/prereg_v006/KMAX_MATRIX_PREREG_V006.json')


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    CX = load(CMP, 'cx')
    pre = json.loads(PRE.read_text())
    bi = pre['binding_inputs']
    pre5 = json.loads(Path(bi['prereg_v005']['path']).read_text())
    C5M = CX.load_pinned(bi['v005_compare']['path'], bi['v005_compare']['sha256'], 'c5m')
    r3 = json.loads(Path(bi['r3_recovery']['path']).read_text())['brackets']
    cases = {c['id']: c for c in pre['cases']}
    real = {cid: C5M.adapt_result(cases[cid]['bound']['result']['path']) for cid in ('C4', 'C3', 'C2', 'R')}
    ids = pre5['row_ids']
    tau = dict(zip(ids, pre5['tau_km_s']))
    v9 = bi['drivers']['v009']['sha256']
    MAXIT = cases['C5']['route_a_numerics']['max_iterations']

    def synth(cid, base_rows, mult, **over):
        a = copy.deepcopy(real['C4'])
        gid = cases[cid]['grid']
        a['rows'] = {i: base_rows[i] + (mult[i] if isinstance(mult, dict) else mult) * tau[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(ids)}
        a['driver_sha256'] = over.get('driver', v9)
        a['grid_spec'] = over.get('grid', pre['grids'][gid]['composite_grid_spec'])
        a['result_path'] = over.get('result_path', a['result_path'])
        ns = a['normalized_spec']
        ns['numerics']['composite_grid_spec'] = a['grid_spec']
        ns['numerics']['route_a'] = over.get('route_a', {'column_workers': 8, 'max_iterations': MAXIT})
        ns['admit'] = {}
        return a

    def run(name, d45, d56, drop=(), v9ok=True, v7ok=True, v5adm=None, bracket_is_r3=True, real_over=None, **over):
        ad = dict(real)
        if real_over:
            for cid, f in real_over.items():
                ad[cid] = f(copy.deepcopy(real[cid]))
        c5 = synth('C5', real['C4']['rows'], d45, **over.get('C5', {}))
        c6 = synth('C6', c5['rows'], d56, **over.get('C6', {}))
        ad['C5'], ad['C6'] = c5, c6
        for d in drop:
            ad.pop(d)
        packets = {c: {'V4': True, 'V5': True} for c in ad}
        v7 = {c: {'V7': v7ok} for c in ('C5', 'C6')}
        v9adm = {'admissible': v9ok, 'reason': 'synthetic'}
        v5 = v5adm if v5adm is not None else {'admissible': True, 'reason': 'synthetic'}
        return CX.evaluate_ext(pre, pre5, C5M, ad, packets, r3, v9adm, v7, v5, bracket_is_r3)
    T = []

    def check(name, ev, outcome, subtype=None, extra=None):
        d = ev['decision']
        ok = d['outcome'] == outcome and (subtype is None or d.get('subtype') == subtype) and (extra is None or bool(extra(ev)))
        T.append({'test': name, 'pass': bool(ok), 'outcome': d['outcome'], 'subtype': d.get('subtype'), 'reasons': d['reasons'][:3]})
    # ---- T1-T17: the V006 tests (route-A budget now 32)
    ev = run('ADOPT', 0.8, 0.3)
    check('T1_ADOPT', ev, 'ADOPT', extra=lambda e: abs(e['decision']['carried_numerical_uncertainty_km_s'][ids[0]]
                                                       - (0.3 * tau[ids[0]] + abs(pre['carried_from_r3']['inner_control']['delta'][ids[0]]))) < 1e-12
          and e['decision']['carried_terms']['shape_spread'] is None)
    check('T2_CONTRACTING_ABOVE_TAU', run('', 10, 4), 'NOT_CONVERGED_EXT', 'CONTRACTING_ABOVE_TAU')
    check('T3_NOT_CONTRACTING', run('', 10, 8), 'NOT_CONVERGED_EXT', 'NOT_CONTRACTING')
    check('T4_FLOOR_LIKE', run('', 0.5, 0.4), 'NOT_CONVERGED_EXT', 'FLOOR_LIKE')
    check('T5_MISSING_C6', run('', 0.8, 0.3, drop=('C6',)), 'INCOMPLETE', extra=lambda e: 'missing' in e['gates']['C6']['failed'])
    check('T6_V009_INADMISSIBLE', run('', 0.8, 0.3, v9ok=False), 'INCOMPLETE',
          extra=lambda e: e['decision']['next_step']['C5']['V3'] == pre['binding_inputs']['v009_admissibility']['inadmissible_next_step'])
    check('T7_MAXIT_16_REJECTED', run('', 0.8, 0.3, C5={'route_a': {'column_workers': 8, 'max_iterations': 16}}), 'INCOMPLETE',
          extra=lambda e: e['gates']['C5']['failed'] == ['V3'] and e['gates']['C6']['valid_all'])
    check('T8_V7_FALSE', run('', 0.8, 0.3, v7ok=False), 'INCOMPLETE', extra=lambda e: 'V7' in e['gates']['C5']['failed'])
    check('T9_C5_DRIVER_V005', run('', 0.8, 0.3, C5={'driver': bi['drivers']['v005']['sha256']}), 'INCOMPLETE')
    check('T10_C5_GRID_G6', run('', 0.8, 0.3, C5={'grid': pre['grids']['G6']['composite_grid_spec']}), 'INCOMPLETE')
    check('T11_NEAR_BOUNDARY', run('', 2.0, 1.0 - 1e-9), 'ADOPT')
    check('T11b_JUST_ABOVE_TAU', run('', 2.1, 1.0 + 1e-6), 'NOT_CONVERGED_EXT', 'CONTRACTING_ABOVE_TAU')
    check('T12_C3_DIAG_MISSING_NOT_BLOCKING', run('', 0.8, 0.3, drop=('C3',)), 'ADOPT')
    check('T13_N1_ALLOWED', run('', 0.8, 0.3, C5={'route_a': {'column_workers': 1, 'max_iterations': MAXIT}}), 'ADOPT')
    check('T14_N4_NOT_REGISTERED', run('', 0.8, 0.3, C6={'route_a': {'column_workers': 4, 'max_iterations': MAXIT}}), 'INCOMPLETE')
    ev = run('', 0.8, 0.3)
    T.append({'test': 'T15_DHAT34_DIAGNOSTIC_EQUALS_R3', 'pass': bool(ev['sequences']['3_4_diagnostic']['equals_registered_R3_value']),
              'value': ev['sequences']['3_4_diagnostic']['Dhat']})
    T.append({'test': 'T16_REAL_C4_C3_C2_R_ALL_GATES_PASS', 'pass': all(ev['gates'][c]['valid_all'] for c in ('C4', 'C3', 'C2', 'R')),
              'failed': {c: ev['gates'][c]['failed'] for c in ('C4', 'C3', 'C2', 'R')}})
    cases_file = out / 'CASES_R3_ONLY.json'
    with open(cases_file, 'x') as f:
        json.dump({c: cases[c]['bound']['result']['path'] for c in ('C4', 'C3', 'C2', 'R')}, f, indent=1)

    def e2e(name, extra_args=(), prereg=PRE):
        p = subprocess.run([PY, '-I', '-B', str(CMP), '--prereg', str(prereg), '--cases', str(cases_file), '--outdir', str(out / name),
                            '--bracket-recovery', bi['r3_recovery']['path']] + list(extra_args), capture_output=True, text=True)
        with open(out / (name + '.stdout.txt'), 'x') as f:
            f.write(p.stdout + '\n--- stderr ---\n' + p.stderr)
        rep = json.loads((out / name / 'KMAX_EXT_COMPARISON.json').read_text()) if p.returncode == 0 else None
        tab = (out / name / 'KMAX_EXT_COMPARISON_TABLE.txt').read_text() if p.returncode == 0 else ''
        return p, rep, tab
    p, e1, tab1 = e2e('E2E_R3_ONLY')
    T.append({'test': 'T17_E2E_R3_ONLY_INCOMPLETE_C5_C6', 'pass': bool(e1 and e1['decision']['outcome'] == 'INCOMPLETE'
                                                                   and not e1['test_mode'] and e1['bracket_recovery']['equals_R3']
                                                                   and e1['gates']['C4']['valid_all']
                                                                   and e1['gates']['C5']['failed'] == ['missing'] and e1['gates']['C6']['failed'] == ['missing']),
              'exit': p.returncode, 'outcome': e1 and e1['decision']['outcome']})
    # ---- T18-T29: the CHECK_V001 findings applied in R1
    spec_ok = {}
    for cid in ('C5', 'C6'):
        for var in ('primary_N8', 'alternate_N1'):
            sp = cases[cid]['specs'][var]
            b = Path(sp['path']).read_bytes()
            s = json.loads(b)
            spec_ok['%s_%s' % (cid, var)] = bool(CX.hashlib.sha256(b).hexdigest() == sp['sha256'] and s['numerics']['route_a']['max_iterations'] == 32
                                                  and sp['route_a_max_iterations'] == 32)
    T.append({'test': 'T18_M1_PREREG_AND_SPECS_MAXIT_32', 'pass': bool(all(spec_ok.values()) and all(cases[c]['route_a_numerics']['max_iterations'] == 32 for c in ('C5', 'C6'))
                                                                     and '32' in pre['criterion']['gates'] and 'max_iterations 16' not in pre['criterion']['gates']),
              'specs': spec_ok})
    check('T19_M1_MAXIT_32_ADMITTED_V1iii_PATH', run('', 0.8, 0.3, C6={'route_a': {'column_workers': 8, 'max_iterations': 32}}), 'ADOPT',
          extra=lambda e: e['gates']['C5']['V3'] and e['gates']['C6']['V3'])
    check('T20_L1_C4_BOUND_SHA_MISMATCH_UNDER_R3', run('', 0.8, 0.3, real_over={'C4': lambda a: dict(a, result_sha256='0' * 64)}), 'INCOMPLETE',
          extra=lambda e: e['gates']['C4']['failed'] == ['V3'] and any(m.startswith('bound_result_sha256') for m in e['gates']['C4']['V3_mismatch']))
    check('T21_L1_BOUND_SHA_NOT_ENFORCED_UNDER_LATER_RN', run('', 0.8, 0.3, bracket_is_r3=False, real_over={'C4': lambda a: dict(a, result_sha256='0' * 64)}),
          'ADOPT', extra=lambda e: e['gates']['C4']['bound_result_sha256'] == {'registered': cases['C4']['bound']['result']['sha256'], 'actual': '0' * 64,
                                                                                 'equal': False, 'enforced': False})
    check('T22_L1_C3_BOUND_SHA_MISMATCH_DIAGNOSTIC_ONLY', run('', 0.8, 0.3, real_over={'C3': lambda a: dict(a, result_sha256='0' * 64)}), 'ADOPT',
          extra=lambda e: 'V3' in e['gates']['C3']['failed'] and e['sequences']['3_4_diagnostic'] is None)
    check('T23_L2_V005_INADMISSIBLE', run('', 0.8, 0.3, v5adm={'admissible': False, 'reason': 'synthetic absent'}), 'INCOMPLETE',
          extra=lambda e: e['gates']['C4']['failed'] == ['V3'] and e['gates']['C4']['V3_mismatch'] == ['V005_INADMISSIBLE: synthetic absent']
          and e['decision']['next_step']['C4']['V3'] == pre5['amendment_v005']['driver']['inadmissible_next_step']
          and not e['gates']['C3']['valid_all'] and not e['gates']['R']['valid_all'] and e['gates']['C2']['valid_all'])
    v5real = C5M.v005_admissibility(pre5)
    T.append({'test': 'T24_L2_REAL_V005_ADMISSIBILITY_EXECUTED_PASS', 'pass': bool(v5real['admissible'] and v5real['verdict'] == 'PASS_BITWISE_EQUAL'
                                                                                 and e1 and e1['v005_admissibility'] == v5real),
              'v005_admissibility': v5real})
    k0 = (e1 or {}).get('K0_max_rel_diff_vs_C2') or {}
    fd = (e1 or {}).get('field_diagnostic') or {}
    T.append({'test': 'T25_L3_K0_AND_FIELD_DIAGNOSTIC_REPORTED', 'pass': bool(e1 and set(k0) == {'C4', 'C3', 'C2', 'R'} and k0['C2'] == 0.0
                                                                           and e1['field_diagnostic_enabled'] is True
                                                                           and all(fd.get(c) and len(fd[c]['rows']) == 12 for c in ('C4', 'C3', 'C2', 'R'))
                                                                           and 'gravity-only ring g0 relative to C2' in tab1),
              'K0_max_rel_diff_vs_C2': k0})
    p2, e2, tab2 = e2e('E2E_R3_ONLY_NO_FIELD', ['--no-field-diagnostic'])
    T.append({'test': 'T26_L3_NO_FIELD_DIAGNOSTIC_EFFECTIVE', 'pass': bool(e2 and e2['field_diagnostic_enabled'] is False and e2['field_diagnostic'] is None
                                                                        and 'gravity-only ring' not in tab2 and e1
                                                                        and e2['decision'] == e1['decision'] and e2['gates'] == e1['gates']
                                                                        and e2['K0_max_rel_diff_vs_C2'] == e1['K0_max_rel_diff_vs_C2']),
              'exit': p2.returncode})
    n1 = cases['C5']['outdirs']['alternate_N1']['outdir']
    check('T27_L4_N1_OUTDIR_REPORTED_NOT_DECIDING', run('', 0.8, 0.3, C5={'result_path': n1 + '/result.json', 'route_a': {'column_workers': 1, 'max_iterations': 32}}),
          'ADOPT', extra=lambda e: e['gates']['C5']['registered_outdir'] == 'alternate_N1' and e['gates']['C6']['registered_outdir'] is None)
    od = {c: {k: v for k, v in cases[c]['outdirs'].items() if k != 'note'} for c in ('C5', 'C6')}   # 'note' is a string entry
    T.append({'test': 'T28_L4_PREREG_REGISTERS_N8_AND_N1_OUTDIRS', 'pass': bool(all(set(od[c]) == {'primary_N8', 'alternate_N1'} for c in od)
                                                                             and all(od[c]['primary_N8']['outdir'] == cases[c]['outdir'] for c in od)
                                                                             and all(v['outdir'].startswith('/Volumes/External1/') for c in od for v in od[c].values())
                                                                             and len({v['outdir'] for c in od for v in od[c].values()}) == 4),
              'outdirs': od})
    p3, e3, _ = e2e('E2E_V006_DRAFT_PREREG_REFUSED', prereg=V006)
    T.append({'test': 'T29_PIN_REFUSES_SUPERSEDED_V006_DRAFT', 'pass': bool(p3.returncode == 2 and e3 is None and 'REFUSED: prereg sha' in p3.stderr),
              'exit': p3.returncode})
    res = {'tests': T, 'n': len(T), 'n_pass': sum(t['pass'] for t in T)}
    with open(out / 'TESTS_RESULT.json', 'x') as f:
        json.dump(res, f, indent=1, default=str)
    for t in T:
        print('PASS' if t['pass'] else 'FAIL', t['test'], t.get('outcome'), t.get('subtype') or '')
    print('%d/%d' % (res['n_pass'], res['n']))


if __name__ == '__main__':
    main()
