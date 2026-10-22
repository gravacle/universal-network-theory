"""Synthetic tests of the V006 extension decision (kmax_compare_ext_c2v006.evaluate_ext) plus one end-to-end CLI run on the
real R3 bytes (C4, C3, C2, R present; C5, C6 absent -> INCOMPLETE).  C4/C3/C2/R adapted records are the REAL R3 results
(read-only); C5/C6 are synthetic copies of C4's record with registered grid, driver, route_a numerics and rows
C4 + delta*tau (no observed velocity is used anywhere: tau comes from the prereg).  Writes only into OUT (must not exist).
usage: python3 -I -B tests_kmax_compare_ext_c2v006.py OUT"""
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    CX = load(HERE / 'kmax_compare_ext_c2v006.py', 'cx')
    pre = json.loads((HERE / 'KMAX_MATRIX_PREREG_V006.json').read_text())
    bi = pre['binding_inputs']
    pre5 = json.loads(Path(bi['prereg_v005']['path']).read_text())
    C5M = CX.load_pinned(bi['v005_compare']['path'], bi['v005_compare']['sha256'], 'c5m')
    r3 = json.loads(Path(bi['r3_recovery']['path']).read_text())['brackets']
    cases = {c['id']: c for c in pre['cases']}
    real = {cid: C5M.adapt_result(cases[cid]['bound']['result']['path']) for cid in ('C4', 'C3', 'C2', 'R')}
    ids = pre5['row_ids']
    tau = dict(zip(ids, pre5['tau_km_s']))
    v9 = bi['drivers']['v009']['sha256']

    def synth(cid, base_rows, mult, **over):
        a = copy.deepcopy(real['C4'])
        gid = cases[cid]['grid']
        a['rows'] = {i: base_rows[i] + (mult[i] if isinstance(mult, dict) else mult) * tau[i] * (1 if k % 2 == 0 else -1) for k, i in enumerate(ids)}
        a['driver_sha256'] = over.get('driver', v9)
        a['grid_spec'] = over.get('grid', pre['grids'][gid]['composite_grid_spec'])
        ns = a['normalized_spec']
        ns['numerics']['composite_grid_spec'] = a['grid_spec']
        ns['numerics']['route_a'] = over.get('route_a', {'column_workers': 8, 'max_iterations': 16})
        ns['admit'] = {}
        return a

    def run(name, d45, d56, drop=(), v9ok=True, v7ok=True, **over):
        ad = dict(real)
        c5 = synth('C5', real['C4']['rows'], d45, **over.get('C5', {}))
        c6 = synth('C6', c5['rows'], d56, **over.get('C6', {}))
        ad['C5'], ad['C6'] = c5, c6
        for d in drop:
            ad.pop(d)
        packets = {c: {'V4': True, 'V5': True} for c in ad}
        v7 = {c: {'V7': v7ok} for c in ('C5', 'C6')}
        v9adm = {'admissible': v9ok, 'reason': 'synthetic'}
        ev = CX.evaluate_ext(pre, pre5, C5M, ad, packets, r3, v9adm, v7)
        return ev
    T = []

    def check(name, ev, outcome, subtype=None, extra=None):
        d = ev['decision']
        ok = d['outcome'] == outcome and (subtype is None or d.get('subtype') == subtype) and (extra is None or extra(ev))
        T.append({'test': name, 'pass': bool(ok), 'outcome': d['outcome'], 'subtype': d.get('subtype'), 'reasons': d['reasons'][:3]})
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
    check('T7_MAXIT_12', run('', 0.8, 0.3, C5={'route_a': {'column_workers': 8, 'max_iterations': 12}}), 'INCOMPLETE',
          extra=lambda e: e['gates']['C5']['failed'] == ['V3'] and e['gates']['C6']['valid_all'])
    check('T8_V7_FALSE', run('', 0.8, 0.3, v7ok=False), 'INCOMPLETE', extra=lambda e: 'V7' in e['gates']['C5']['failed'])
    check('T9_C5_DRIVER_V005', run('', 0.8, 0.3, C5={'driver': bi['drivers']['v005']['sha256']}), 'INCOMPLETE')
    check('T10_C5_GRID_G6', run('', 0.8, 0.3, C5={'grid': pre['grids']['G6']['composite_grid_spec']}), 'INCOMPLETE')
    check('T11_NEAR_BOUNDARY', run('', 2.0, 1.0 - 1e-9), 'ADOPT')
    check('T11b_JUST_ABOVE_TAU', run('', 2.1, 1.0 + 1e-6), 'NOT_CONVERGED_EXT', 'CONTRACTING_ABOVE_TAU')
    check('T12_C3_DIAG_MISSING_NOT_BLOCKING', run('', 0.8, 0.3, drop=('C3',)), 'ADOPT')
    check('T13_N1_ALLOWED', run('', 0.8, 0.3, C5={'route_a': {'column_workers': 1, 'max_iterations': 16}}), 'ADOPT')
    check('T14_N4_NOT_REGISTERED', run('', 0.8, 0.3, C6={'route_a': {'column_workers': 4, 'max_iterations': 16}}), 'INCOMPLETE')
    ev = run('', 0.8, 0.3)
    T.append({'test': 'T15_DHAT34_DIAGNOSTIC_EQUALS_R3', 'pass': bool(ev['sequences']['3_4_diagnostic']['equals_registered_R3_value']),
              'value': ev['sequences']['3_4_diagnostic']['Dhat']})
    T.append({'test': 'T16_REAL_C4_C3_C2_R_ALL_GATES_PASS', 'pass': all(ev['gates'][c]['valid_all'] for c in ('C4', 'C3', 'C2', 'R')),
              'failed': {c: ev['gates'][c]['failed'] for c in ('C4', 'C3', 'C2', 'R')}})
    # end-to-end CLI on real R3 bytes, C5/C6 absent
    cases_file = out / 'CASES_R3_ONLY.json'
    with open(cases_file, 'x') as f:
        json.dump({c: cases[c]['bound']['result']['path'] for c in ('C4', 'C3', 'C2', 'R')}, f, indent=1)
    p = subprocess.run([PY, '-I', '-B', str(HERE / 'kmax_compare_ext_c2v006.py'), '--prereg', str(HERE / 'KMAX_MATRIX_PREREG_V006.json'),
                        '--cases', str(cases_file), '--outdir', str(out / 'E2E_R3_ONLY'), '--bracket-recovery', bi['r3_recovery']['path']],
                       capture_output=True, text=True)
    with open(out / 'E2E_R3_ONLY.stdout.txt', 'x') as f:
        f.write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    e2e = json.loads((out / 'E2E_R3_ONLY/KMAX_EXT_COMPARISON.json').read_text()) if p.returncode == 0 else None
    T.append({'test': 'T17_E2E_R3_ONLY_INCOMPLETE_C5_C6', 'pass': bool(e2e and e2e['decision']['outcome'] == 'INCOMPLETE'
                                                                   and not e2e['test_mode'] and e2e['bracket_recovery']['equals_R3']
                                                                   and e2e['gates']['C4']['valid_all']
                                                                   and e2e['gates']['C5']['failed'] == ['missing'] and e2e['gates']['C6']['failed'] == ['missing']),
              'exit': p.returncode, 'outcome': e2e and e2e['decision']['outcome']})
    res = {'tests': T, 'n': len(T), 'n_pass': sum(t['pass'] for t in T)}
    with open(out / 'TESTS_RESULT.json', 'x') as f:
        json.dump(res, f, indent=1, default=str)
    for t in T:
        print('PASS' if t['pass'] else 'FAIL', t['test'], t.get('outcome'), t.get('subtype') or '')
    print('%d/%d' % (res['n_pass'], res['n']))


if __name__ == '__main__':
    main()
