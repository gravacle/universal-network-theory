"""Synthetic tests of kmax_compare_c2v002.py (Claude2 lane).  Mock result.json files on tiny registered
grids (the real prereg with only the grid table and G2 base axis swapped, test mode).  Nothing is launched,
no stage or kernel runs, no observed velocity is read.  usage: python3 -I -B tests_kmax_compare_c2v002.py NEW_WORKDIR
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
KPC = 3.085677581491367e19
RESULTS = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(name, cond, detail=''):
    RESULTS.append({'test': name, 'pass': bool(cond), 'detail': detail})
    print(('PASS ' if cond else 'FAIL ') + name + ('  ' + json.dumps(detail, default=str)[:300] if detail else ''))


TINY = {'G2': {'composite_grid_spec': None, 'axis_nodes': 8},
        'G3': {'composite_grid_spec': {'version': 'T3', 'breaks_inverse_kpc': [-3, -2, -1, 0, 1, 2, 3], 'panel_orders': [2] * 6, 'total_axis_nodes': 12, 'scope': 't'}, 'axis_nodes': 12},
        'G4': {'composite_grid_spec': {'version': 'T4', 'breaks_inverse_kpc': [-4, -3, -2, -1, 0, 1, 2, 3, 4], 'panel_orders': [2] * 8, 'total_axis_nodes': 16, 'scope': 't'}, 'axis_nodes': 16},
        'GR': {'composite_grid_spec': {'version': 'TR', 'breaks_inverse_kpc': [-2, -1, 0, 1, 2], 'panel_orders': [2, 4, 4, 2], 'total_axis_nodes': 12, 'scope': 't'}, 'axis_nodes': 12}}
TINY_BASE = {'breaks_inverse_kpc': [-2, -1, 0, 1, 2], 'panel_orders': [2, 2, 2, 2]}


def mock_case(root, cmp, pre, cid, speeds, m4, last_change=0.005, leak=False, overmask=False, ident='a' * 64, wrong_grid=False,
              status='COMPLETED', driver=None, passes=None, physical=None, brackets=None):
    c = {x['id']: x for x in pre['cases']}[cid]
    drv = pre['binding_inputs']['drivers']
    if driver is None:
        driver = 'v001' if c['grid'] == 'G2' else 'v003'
    if passes is None:
        passes = 4 if cid == 'C2' else 6
    gs = pre['grids'][c['grid']]['composite_grid_spec']
    ax = cmp.expected_axis(gs)
    if wrong_grid:
        ax = ax * 1.000001
    k = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
    rng = np.random.default_rng(int.from_bytes(cid.encode(), 'big') % 2 ** 32)
    w = (rng.normal(size=(len(k), 10, 1)) + 1j * rng.normal(size=(len(k), 10, 1))) * 1e-12
    edge = float((gs or cmp.BASE_SPEC)['breaks_inverse_kpc'][-1])
    m = cmp.driver_mask(k, c['shape'], (c['kmax_inverse_kpc'] or edge) / KPC)
    w[~m] = 0
    if leak and (~m).any():
        w[np.argmax(~m)] = 1e-30
    if overmask:
        w[np.argmax(m)] = 0
    d = root / cid
    (d / 'fb').mkdir(parents=True)
    (d / 'rot').mkdir()
    np.savez(d / 'fb' / 'refreshed_prepared.npz', wavevectors=k, weighted_responses=w)
    (d / 'fb' / 'finish.json').write_text(json.dumps({'outputs': {'refreshed_prepared.npz': {'path': str(d / 'fb' / 'refreshed_prepared.npz'), 'sha256': sha(d / 'fb' / 'refreshed_prepared.npz')}}}))
    (d / 'rot' / 'finish.json').write_text(json.dumps({'base_K_values_SI': [1.0 + (0.001 if c['grid'] == 'G4' else 0)] * 72}))
    anc = pre['anchor']
    tr = {'shape': c['shape'], 'kmax_inverse_kpc': c['kmax_inverse_kpc']}
    ns = {'schema': 'X', 'galaxy': 'DDO154', 'label': cid, 'physical': physical or anc['physical'], 'coefficients': anc['coefficients'],
          'numerics': {'composite_grid_spec': gs, 'truncation': tr,
                       'picard': {'passes': passes, 'speed_change_bound_km_s': 0.01, 'observe_every_pass': True},
                       'brackets': brackets or anc['brackets'], 'column_workers': 2}, 'admit': {}, 'reference_compare': False}
    radial = [x * KPC for x in (0.2, 0.5, 1.0, 3.0, 5.9, 8.0, 12.8)]
    per_r = [{'m4': (0.5 if R / KPC > 6.0 or R / KPC < 0.4 else m4 * (1 + 0.01 * j))} for j, R in enumerate(radial)]
    r = {'schema': cmp.RESULT_SCHEMA, 'status': status, 'valid': status == 'COMPLETED', 'reasons': [], 'driver_sha256': drv[driver]['sha256'],
         'call_spec_sha256': (pre['cases'][6]['bound_call']['call_spec_sha256'] if cid == 'C2' else 'c' * 64),
         'rows': [{'id': i, 'speed_km_s': float(v)} for i, v in zip(pre['row_ids'], speeds)], 'normalized_spec': ns, 'final_pass': 3,
         'passes': [{'pass': 2, 'max_abs_change_km_s': 0.15}, {'pass': 3, 'max_abs_change_km_s': last_change, 'field': str(d / 'fb'), 'rotation': str(d / 'rot')}],
         'identity': {'route_a': {'custody': {'identity_sha256': ident}}},
         'residual_diagnostics': {'azimuthal_harmonics': {'global_max': {'m4': 0.5, 'm8': 0.1}, 'per_radius_max': per_r, 'radial_nodes_m': radial}},
         'elapsed_seconds': 1.0}
    (d / 'result.json').write_text(json.dumps(r))
    return str(d / 'result.json')


BASEV = np.linspace(11.6, 50.9, 12)
# tau = [0.4,0.2,0.175,0.125,0.1,0.05,0.05,0.05,0.075,0.15,0.175,0.325]
PLAN = {'cube': ([0.9, 0.2, 0.06], 1e-2), 'sphere': ([-1.0, -0.08, -0.04], 3e-4), 'cylinder': ([-0.5, -0.07, -0.035], 2e-3)}


def scenario(work, cmp, pre_path, pre, name, mods, expect, extra=None, recovery=None, row_offsets=None):
    root = work / ('mock_' + name)
    plan = copy.deepcopy(PLAN)
    plan.update(mods.get('plan', {}))
    rinner = mods.get('R', 0.003)
    letter = {'cube': 'C', 'sphere': 'S', 'cylinder': 'Y'}
    cases = {}
    for shp, (off, m4) in plan.items():
        for K, o in zip((2, 3, 4), off):
            cid = '%s%d' % (letter[shp], K)
            kw = dict((extra or {}).get(cid, {}))
            sp = BASEV + o
            if row_offsets and cid in row_offsets:
                sp = sp + np.asarray(row_offsets[cid])
            ident = {'2': 'a', '3': 'b', '4': 'c'}[str(K)] * 64
            kw.setdefault('ident', ident)
            cases[cid] = mock_case(root, cmp, pre, cid, sp, m4, **kw)
    cases['R'] = mock_case(root, cmp, pre, 'R', BASEV + plan['cube'][0][0] + rinner, 1e-2, **dict((extra or {}).get('R', {})))
    for drop in mods.get('drop', []):
        cases.pop(drop)
    cf = root / 'cases.json'
    cf.write_text(json.dumps(cases))
    od = root / 'cmp_out'
    argv = ['--prereg', str(pre_path), '--cases', str(cf), '--outdir', str(od), '--test-allow-unpinned-prereg']
    if recovery:
        rp = root / 'recovery.json'
        rp.write_text(json.dumps(recovery))
        argv += ['--bracket-recovery', str(rp)]
    cmp.main(argv)
    rep = json.loads((od / 'KMAX_COMPARISON.json').read_text())
    got = rep['decision']['outcome'] + ('/' + rep['decision'].get('adopted_shape', '') if rep['decision'].get('adopted_shape') else '')
    check('%s -> %s' % (name, expect), got == expect, {'got': got, 'reasons': rep['decision']['reasons'][:4]})
    return rep


def main(work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=False)
    cmp = load(HERE / 'kmax_compare_c2v002.py', 'kmax_cmp2')
    pre_path = HERE / 'KMAX_MATRIX_PREREG_V002.json'
    real = json.loads(pre_path.read_text())
    pre = copy.deepcopy(real)
    pre['grids'] = copy.deepcopy(TINY)
    cmp.BASE_SPEC = TINY_BASE
    pp = work / 'tiny_prereg.json'
    pp.write_text(json.dumps(pre))
    # 1 adopt; D2 spread term
    rep = scenario(work, cmp, pp, pre, 'adopt', {}, 'ADOPT/sphere')
    check('adopt: all 10 cases valid (C2 v001 passes 4 equivalence; S2/Y2 v001; G3/G4/GR v003)', all(g['valid_all'] for g in rep['gates'].values()),
          {c: g['failed'] for c, g in rep['gates'].items()})
    u = rep['decision']['carried_numerical_uncertainty_km_s']['DDO154_SPARC12_01']
    want = abs(-0.04 - (-0.08)) + 0.003 + max(abs(-0.04 - (-0.04)), abs(-0.035 - (-0.04)))
    check('D2: u_i = |K34| + |inner| + max passing-shape spread at K=4', abs(u - want) < 1e-9, {'u': u, 'want': want})
    check('ring diagnostic ran on every case', all(rep['field_diagnostic'].get(c) for c in rep['gates']))
    check('modal block equals registered', rep['modal_common_block']['modal_equals_registered'] is True)
    # 2 D1: slow contraction (q = 0.95) within tau -> not a pass
    scenario(work, cmp, pp, pre, 'D1_slow_contraction', {'plan': {'sphere': ([-0.1005, -0.049, 0.0], 3e-4), 'cylinder': ([-0.1, -0.0485, 0.0], 2e-3),
                                                                  'cube': ([0.1, 0.0485, 0.0], 1e-2)}}, 'NOT_CONVERGED')
    # 3 per-row tau: row 01 moves 0.3 km/s 3->4 (tau 0.4), row 06 moves 0.01 -> ADOPT (V001 uniform 0.05 would fail)
    ro = {'S4': [0.3] + [0.0] * 11, 'Y4': [0.3] + [0.0] * 11, 'C4': [0.3] + [0.0] * 11}
    rep = scenario(work, cmp, pp, pre, 'per_row_tau_adopt', {}, 'ADOPT/sphere', row_offsets=ro)
    check('per-row tau: Dhat_3_4 of sphere < 1 although |d| = 0.3 km/s on row 01', rep['sequences']['sphere'].get('Dhat_3_4', 9) <= 1
          and rep['sequences']['sphere']['D_3_4'] > 0.29, {'Dhat': rep['sequences']['sphere'].get('Dhat_3_4'), 'D': rep['sequences']['sphere'].get('D_3_4')})
    check('tail diagnostic reported per row', len(rep['sequences']['sphere']['tail_diagnostic']['per_row']) == 12)
    # 4 D3 over-masked packet
    rep = scenario(work, cmp, pp, pre, 'D3_overmask', {}, 'INCOMPLETE', extra={'S4': {'overmask': True}})
    check('D3: over-masked S4 fails V5 only', rep['gates']['S4']['failed'] == ['V5'], rep['gates']['S4']['failed'])
    scenario(work, cmp, pp, pre, 'mask_leak', {}, 'INCOMPLETE', extra={'Y3': {'leak': True}})
    # 5 D8 odd C4 named alone
    phys = dict(pre['anchor']['physical'])
    phys['gamma'] = phys['gamma'] * 1.0000001
    rep = scenario(work, cmp, pp, pre, 'D8_odd_C4', {}, 'INCOMPLETE', extra={'C4': {'physical': phys}})
    bad = sorted(c for c, g in rep['gates'].items() if not g['valid_all'])
    check('D8: only C4 named (S4/Y4 still valid: identity equal)', bad == ['C4'], {'bad': bad, 'off_modal': rep['modal_common_block']['cases_off_modal']})
    # 6 C2 Picard cap not equivalent
    rep = scenario(work, cmp, pp, pre, 'C2_picard_cap', {}, 'INCOMPLETE', extra={'C2': {'last_change': 0.011}})
    check('root d: C2 passes 4 with final change 0.011 > bound fails V3 PICARD_CAP_NOT_EQUIVALENT',
          'PICARD_CAP_NOT_EQUIVALENT' in rep['gates']['C2'].get('V3_mismatch', []), rep['gates']['C2'])
    check('next step for C2 V3 is pre-named', 'C2\'' in json.dumps(rep['decision']['next_step']))
    # 7 driver allowance
    rep = scenario(work, cmp, pp, pre, 'C3_on_v001', {}, 'INCOMPLETE', extra={'C3': {'driver': 'v001'}})
    check('root c: C3 under v001 fails V3 (driver)', rep['gates']['C3']['failed'] == ['V3'], rep['gates']['C3'].get('V3_mismatch'))
    rep = scenario(work, cmp, pp, pre, 'C2_on_v003_ok', {}, 'ADOPT/sphere', extra={'C2': {'driver': 'v003'}, 'S2': {'driver': 'v003'}, 'Y2': {'driver': 'v003'}})
    rep = scenario(work, cmp, pp, pre, 'S2_driver_differs_from_C2', {}, 'INCOMPLETE', extra={'S2': {'driver': 'v003'}})
    check('V6: S2 under v003 admitting a v001 C2 fails V6', rep['gates']['S2']['failed'] == ['V6'], rep['gates']['S2']['failed'])
    scenario(work, cmp, pp, pre, 'other_case_passes4', {}, 'INCOMPLETE', extra={'C3': {'passes': 4}})
    # 8 other outcomes
    scenario(work, cmp, pp, pre, 'inner_fail', {'R': 0.08}, 'INNER_UNRESOLVED')
    scenario(work, cmp, pp, pre, 'shape_disagree', {'plan': {'cylinder': ([-0.5, 0.15, 0.13], 2e-3)}}, 'NOT_CONVERGED')
    scenario(work, cmp, pp, pre, 'picard_gate', {}, 'INCOMPLETE', extra={'S4': {'last_change': 0.02}})
    scenario(work, cmp, pp, pre, 'missing_case', {'drop': ['C3']}, 'INCOMPLETE')
    scenario(work, cmp, pp, pre, 'wrong_grid', {}, 'INCOMPLETE', extra={'C4': {'wrong_grid': True}})
    scenario(work, cmp, pp, pre, 'identity_mismatch', {}, 'INCOMPLETE', extra={'S3': {'ident': 'f' * 64}})
    # 9 D13 m4 window: cylinder m4 within 10% of sphere and smaller Dhat_3_4 -> cylinder
    scenario(work, cmp, pp, pre, 'm4_tie_cylinder', {'plan': {'cylinder': ([-0.5, -0.04, -0.01], 3.2e-4)}}, 'ADOPT/cylinder')
    scenario(work, cmp, pp, pre, 'm4_cube_lowest', {'plan': {'cube': ([0.9, 0.0, -0.02], 1e-5)}}, 'ADOPT/cube')
    # 10 D7 bracket recovery
    rb = copy.deepcopy(pre['anchor']['brackets'])
    rb['rule']['fs_absolute_overrides']['10'] = [302500000.0, 330000000.0]
    allcases = {c: {'brackets': rb} for c in ('C2', 'S2', 'Y2', 'C3', 'S3', 'Y3', 'C4', 'S4', 'Y4', 'R')}
    scenario(work, cmp, pp, pre, 'D7_without_recovery', {}, 'INCOMPLETE', extra=allcases)
    rep = scenario(work, cmp, pp, pre, 'D7_with_recovery', {}, 'ADOPT/sphere', extra=allcases, recovery={'brackets': rb, 'reason': 'test'})
    check('D7: recovery recorded with changed key', rep['bracket_recovery'] and rep['bracket_recovery']['changed_rule_keys'] == ['fs_absolute_overrides'])
    rc = cmp.main(['--prereg', str(pp), '--cases', str(work / 'mock_adopt' / 'cases.json'), '--outdir', str(work / 'pin_refusal')])
    check('unpinned prereg refused without test flag', rc == 2)
    summary = {'schema': 'UNT_KMAX_COMPARE_TESTS_C2_V002', 'n': len(RESULTS), 'n_pass': sum(r['pass'] for r in RESULTS), 'results': RESULTS,
               'scripts': {p: sha(HERE / p) for p in ('kmax_compare_c2v002.py', 'tests_kmax_compare_c2v002.py')},
               'prereg_sha256': sha(pre_path)}
    with open(work / 'TEST_RESULTS.json', 'x') as f:
        json.dump(summary, f, indent=1)
    print('%d/%d pass' % (summary['n_pass'], summary['n']))
    return 0 if summary['n_pass'] == summary['n'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
