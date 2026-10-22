"""Synthetic tests of kmax_compare_c2v005.py (Claude2 lane).  Mock result.json files on tiny registered grids
(the real prereg V005 with only the grid table, the G2 base axis and the v005 deciding-test paths swapped to
synthetic files; test mode).  Nothing is launched, no stage or kernel runs, no observed velocity is read, and
no file under CLAUDE2/runs is opened (the deciding-test result is a synthetic file in WORKDIR).
usage: python3 -I -B tests_kmax_compare_c2v005.py NEW_WORKDIR
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
V005_IDS = ('C3', 'C4', 'R', 'S3', 'Y3', 'S4', 'Y4')


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


def mock_case(root, cmp, pre, cid, speeds, m4, R1, last_change=0.005, leak=False, overmask=False, ident='a' * 64, wrong_grid=False,
              status='COMPLETED', driver=None, passes=None, physical=None, brackets=None):
    c = {x['id']: x for x in pre['cases']}[cid]
    drv = pre['binding_inputs']['drivers']
    if driver is None:
        driver = 'v001' if c['grid'] == 'G2' else 'v005'
    if passes is None:
        passes = 6
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
                       'brackets': brackets or R1, 'column_workers': 2}, 'admit': {}, 'reference_compare': False}
    radial = [x * KPC for x in (0.2, 0.5, 1.0, 3.0, 5.9, 8.0, 12.8)]
    per_r = [{'m4': (0.5 if R / KPC > 6.0 or R / KPC < 0.4 else m4 * (1 + 0.01 * j))} for j, R in enumerate(radial)]
    ok = status == 'COMPLETED'
    r = {'schema': cmp.RESULT_SCHEMA, 'status': status, 'valid': ok, 'reasons': [], 'driver_sha256': drv[driver]['sha256'],
         'call_spec_sha256': 'c' * 64,
         'rows': ([{'id': i, 'speed_km_s': float(v)} for i, v in zip(pre['row_ids'], speeds)] if ok else []), 'normalized_spec': ns, 'final_pass': 3,
         'passes': [{'pass': 2, 'max_abs_change_km_s': 0.15}, {'pass': 3, 'max_abs_change_km_s': last_change, 'field': str(d / 'fb'), 'rotation': str(d / 'rot')}],
         'identity': {'route_a': {'custody': {'identity_sha256': ident}}},
         'residual_diagnostics': {'azimuthal_harmonics': {'global_max': {'m4': 0.5, 'm8': 0.1}, 'per_radius_max': per_r, 'radial_nodes_m': radial}},
         'elapsed_seconds': 1.0}
    (d / 'result.json').write_text(json.dumps(r))
    return str(d / 'result.json')


def deciding(work, pre, name, verdict='PASS_BITWISE_EQUAL', driver=None, spec=None, finish_ok=True, present=True):
    """Write a synthetic deciding result/finish pair and return a prereg copy pointing at it."""
    d = work / ('deciding_' + name)
    d.mkdir()
    req = pre['binding_inputs']['v005_deciding_test']['required']
    p = copy.deepcopy(pre)
    p['binding_inputs']['v005_deciding_test']['result_path'] = str(d / 'result.json')
    p['binding_inputs']['v005_deciding_test']['finish_path'] = str(d / 'finish.json')
    if present:
        r = {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'status': 'COMPLETED', 'driver_sha256': driver or req['driver_sha256'],
             'call_spec_sha256': spec or req['call_spec_sha256'], 'deciding_test': {'verdict': verdict, 'status': 'DIAGNOSTIC_ONLY'}}
        (d / 'result.json').write_text(json.dumps(r))
        (d / 'finish.json').write_text(json.dumps({'status': 'COMPLETED', 'result_sha256': sha(d / 'result.json') if finish_ok else '0' * 64}))
    pp = d / 'prereg.json'
    pp.write_text(json.dumps(p))
    return pp, p


BASEV = np.linspace(11.6, 50.9, 12)
PLAN = {'cube': ([0.9, 0.2, 0.06], 1e-2), 'sphere': ([-1.0, -0.08, -0.04], 3e-4), 'cylinder': ([-0.5, -0.07, -0.035], 2e-3)}


def scenario(work, cmp, pre_path, pre, R1, name, mods, expect, extra=None, recovery='R1', row_offsets=None):
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
            kw.setdefault('ident', {'2': 'a', '3': 'b', '4': 'c'}[str(K)] * 64)
            cases[cid] = mock_case(root, cmp, pre, cid, sp, m4, R1, **kw)
    cases['R'] = mock_case(root, cmp, pre, 'R', BASEV + plan['cube'][0][0] + rinner, 1e-2, R1, **dict((extra or {}).get('R', {})))
    for drop in mods.get('drop', []):
        cases.pop(drop)
    cf = root / 'cases.json'
    cf.write_text(json.dumps(cases))
    od = root / 'cmp_out'
    argv = ['--prereg', str(pre_path), '--cases', str(cf), '--outdir', str(od), '--test-allow-unpinned-prereg']
    if recovery is not None:
        rp = root / 'recovery.json'
        rp.write_text(json.dumps({'brackets': R1, 'reason': 'test'} if recovery == 'R1' else recovery))
        argv += ['--bracket-recovery', str(rp)]
    rc = cmp.main(argv)
    if expect.startswith('REFUSED'):
        check('%s -> REFUSED (rc 2, no output)' % name, rc == 2 and not od.exists(), {'rc': rc})
        return None
    rep = json.loads((od / 'KMAX_COMPARISON.json').read_text())
    got = rep['decision']['outcome'] + ('/' + rep['decision'].get('adopted_shape', '') if rep['decision'].get('adopted_shape') else '')
    check('%s -> %s' % (name, expect), got == expect, {'got': got, 'reasons': rep['decision']['reasons'][:4]})
    return rep


def main(work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=False)
    cmp = load(HERE / 'kmax_compare_c2v005.py', 'kmax_cmp5')
    real_path = HERE / 'KMAX_MATRIX_PREREG_V005.json'
    real = json.loads(real_path.read_text())
    r1_file = json.loads((HERE / 'd7_recovery' / 'KMAX_D7_RECOVERY_R1.json').read_text())
    R1 = r1_file['brackets']
    anchor = real['anchor']['brackets']
    # ---- static checks on the real files (no run file opened)
    check('compare script pins the V005 prereg bytes', cmp.PREREG_SHA256 == sha(real_path), {'pinned': cmp.PREREG_SHA256})
    check('real R1 recovery file validates against the real prereg', cmp.validate_recovery(real, R1) == [], cmp.validate_recovery(real, R1))
    check('R1 equals amendment_v005.d7_recovery.R1.brackets', cmp.canon(R1) == cmp.canon(real['amendment_v005']['d7_recovery']['R1']['brackets']))
    check('real prereg: v005 in drivers and in drivers_allowed of exactly C3,C4,R,S3,Y3,S4,Y4',
          'v005' in real['binding_inputs']['drivers'] and sorted(c['id'] for c in real['cases'] if 'v005' in c['drivers_allowed']) == sorted(V005_IDS))
    v4 = json.loads(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v004_c2/KMAX_MATRIX_PREREG_V004.json').read_text())
    same = [k for k in ('criterion', 'tau_km_s', 'quoted_sigma_km_s', 'row_ids', 'grids', 'anchor', 'fixed_across_all_cases', 'admission_constraint')
            if cmp.canon(v4[k]) == cmp.canon(real[k])]
    check('V005 criterion/tau/sigma/rows/grids/anchor/fixed/admission byte-identical to V004 (canonical)', len(same) == 8, same)
    # ---- tiny prereg family
    base = copy.deepcopy(real)
    base['grids'] = copy.deepcopy(TINY)
    cmp.BASE_SPEC = TINY_BASE
    pp_pass, pre = deciding(work, base, 'pass')
    # 1 v005 valid
    rep = scenario(work, cmp, pp_pass, pre, R1, 'v005_valid_adopt', {}, 'ADOPT/sphere')
    check('v005-valid: all 10 cases valid; C3..Y4,R ran v005, C2/S2/Y2 v001', all(g['valid_all'] for g in rep['gates'].values())
          and all(rep['gates'][c]['driver'] == 'v005' for c in V005_IDS) and all(rep['gates'][c]['driver'] == 'v001' for c in ('C2', 'S2', 'Y2')),
          {c: (g['driver'], g['failed']) for c, g in rep['gates'].items()})
    check('v005-valid: admissibility recorded PASS', rep['v005_admissibility']['admissible'] is True and rep['v005_admissibility']['verdict'] == 'PASS_BITWISE_EQUAL')
    check('v005-valid: recovery recorded as R1, changed fs entries 5,6,7,8,9,45,50 only',
          rep['bracket_recovery']['equals_registered_R1'] and rep['bracket_recovery']['changed_fs_entries'] == ['5', '6', '7', '8', '9', '45', '50']
          and rep['bracket_recovery']['changed_rule_keys'] == ['fs_absolute_overrides'], rep['bracket_recovery'])
    check('adopt next step names the driver of the adopted K=4 case (v005)', 'driver v005' in rep['decision']['next_step'])
    # 2 deciding FAIL / absent / custody
    pp, p = deciding(work, base, 'fail', verdict='FAIL')
    rep = scenario(work, cmp, pp, p, R1, 'v005_deciding_fail', {}, 'INCOMPLETE')
    bad = sorted(c for c, g in rep['gates'].items() if not g['valid_all'])
    check('deciding FAIL: exactly the v005 cases invalid, each V3 only with V005_INADMISSIBLE', bad == sorted(V005_IDS)
          and all(rep['gates'][c]['failed'] == ['V3'] and any(m.startswith('V005_INADMISSIBLE') for m in rep['gates'][c]['V3_mismatch']) for c in V005_IDS),
          {c: rep['gates'][c].get('V3_mismatch') for c in bad})
    check('deciding FAIL: next step is amendment_v005.driver.inadmissible_next_step',
          all(rep['decision']['next_step'][c]['V3'] == real['amendment_v005']['driver']['inadmissible_next_step'] for c in V005_IDS))
    pp, p = deciding(work, base, 'absent', present=False)
    rep = scenario(work, cmp, pp, p, R1, 'v005_deciding_absent', {}, 'INCOMPLETE')
    check('deciding absent: reason names absence', 'absent' in rep['v005_admissibility']['reason'] and 'absent' in ' '.join(rep['gates']['C3']['V3_mismatch']))
    for nm, kw, word in (('finish_sha_mismatch', {'finish_ok': False}, 'result_sha256'), ('wrong_driver', {'driver': 'b' * 64}, 'driver_sha256'),
                         ('wrong_spec', {'spec': 'd' * 64}, 'call_spec_sha256')):
        pp, p = deciding(work, base, nm, **kw)
        rep = scenario(work, cmp, pp, p, R1, 'v005_deciding_' + nm, {}, 'INCOMPLETE')
        check('deciding %s: inadmissible (%s)' % (nm, word), not rep['v005_admissibility']['admissible'] and word in rep['v005_admissibility']['reason'],
              rep['v005_admissibility']['reason'])
    # 3 v003 cases need no deciding test; mixed drivers fail V6
    pp_abs, p_abs = deciding(work, base, 'absent2', present=False)
    v003 = {c: {'driver': 'v003'} for c in V005_IDS}
    scenario(work, cmp, pp_abs, p_abs, R1, 'v003_cases_without_deciding', {}, 'ADOPT/sphere', extra=v003)
    rep = scenario(work, cmp, pp_pass, pre, R1, 'S3_v003_admitting_v005_C3', {}, 'INCOMPLETE', extra={'S3': {'driver': 'v003'}})
    check('V6: S3 under v003 admitting a v005 C3 fails V6 only', rep['gates']['S3']['failed'] == ['V6'], rep['gates']['S3']['failed'])
    rep = scenario(work, cmp, pp_pass, pre, R1, 'C3_on_v001', {}, 'INCOMPLETE', extra={'C3': {'driver': 'v001'}, 'S3': {'driver': 'v001'}, 'Y3': {'driver': 'v001'}})
    check('C3 under v001 still refused by drivers_allowed', 'V3' in rep['gates']['C3']['failed'])
    # 4 D7-recovered shapes and D7 step (4)
    rep = scenario(work, cmp, pp_pass, pre, R1, 'S2_first_attempt_in_slot', {}, 'INCOMPLETE',
                   extra={'S2': {'brackets': anchor, 'status': 'FAILED_AT_STAGE'}})
    check('S2 first attempt (anchor block, FAILED_AT_STAGE) fails V1 and V3 (brackets); next step V1 names the D7 recovery',
          {'V1', 'V3'} <= set(rep['gates']['S2']['failed']) and 'brackets' in rep['gates']['S2']['V3_mismatch']
          and 'D7 recovery' in rep['decision']['next_step']['S2']['V1'], rep['gates']['S2'])
    rep = scenario(work, cmp, pp_pass, pre, R1, 'C2_not_regenerated', {}, 'INCOMPLETE', extra={'C2': {'brackets': anchor, 'passes': 4}})
    bad = sorted(c for c, g in rep['gates'].items() if not g['valid_all'])
    check('D7 step 4: C2 on the anchor block is named alone (V3 brackets); S2R/Y2R stay valid', bad == ['C2'] and rep['gates']['C2']['V3_mismatch'] == ['brackets'],
          {'bad': bad, 'mm': rep['gates']['C2'].get('V3_mismatch')})
    rep = scenario(work, cmp, pp_pass, pre, R1, 'C3_v005_not_regenerated', {}, 'INCOMPLETE', extra={'C3': {'brackets': anchor}})
    check('D7 step 4: v005 C3 on the anchor block named alone', sorted(c for c, g in rep['gates'].items() if not g['valid_all']) == ['C3'])
    scenario(work, cmp, pp_pass, pre, R1, 'C2R_passes4_equivalence', {}, 'ADOPT/sphere', extra={'C2': {'passes': 4}})
    rep = scenario(work, cmp, pp_pass, pre, R1, 'S2R_Y2R_missing', {'drop': ['S2', 'Y2']}, 'INCOMPLETE')
    check('missing S2R/Y2R named missing', rep['gates']['S2']['failed'] == ['missing'] and rep['gates']['Y2']['failed'] == ['missing'])
    # 5 recovery file handling
    scenario(work, cmp, pp_pass, pre, R1, 'missing_recovery_flag', {}, 'REFUSED', recovery=None)
    scenario(work, cmp, pp_pass, pre, R1, 'recovery_is_anchor_block', {}, 'REFUSED', recovery={'brackets': anchor, 'reason': 't'})
    nar = copy.deepcopy(R1)
    nar['rule']['fs_absolute_overrides']['46'] = [303000000.0, 317625000.0]
    scenario(work, cmp, pp_pass, pre, R1, 'recovery_narrows_46', {}, 'REFUSED', recovery={'brackets': nar, 'reason': 't'})
    rf = copy.deepcopy(R1)
    rf['rule']['rfs_factors'] = [0.7, 1.2]
    scenario(work, cmp, pp_pass, pre, R1, 'recovery_changes_rfs_factors', {}, 'REFUSED', recovery={'brackets': rf, 'reason': 't'})
    nt = copy.deepcopy(R1)
    nt['rule']['fs_absolute_overrides']['11'] = [302500000.0, 320000000.0]
    scenario(work, cmp, pp_pass, pre, R1, 'recovery_new_entry_without_template', {}, 'REFUSED', recovery={'brackets': nt, 'reason': 't'})
    scenario(work, cmp, pp_pass, pre, R1, 'recovery_extra_key', {}, 'REFUSED', recovery={'brackets': R1, 'reason': 't', 'note': 'x'})
    # 6 later cumulative invocation R2 (S3 miss on column 10 -> W1 hull) applied to every case
    R2 = copy.deepcopy(R1)
    R2['rule']['fs_absolute_overrides']['10'] = [151250000.0, 317625000.0]
    allR2 = {c: {'brackets': R2} for c in ('C2', 'S2', 'Y2', 'C3', 'S3', 'Y3', 'C4', 'S4', 'Y4', 'R')}
    rep = scenario(work, cmp, pp_pass, pre, R2, 'R2_all_cases', {}, 'ADOPT/sphere', extra=allR2, recovery={'brackets': R2, 'reason': 'R2', 'invocation': 'R2'})
    check('R2 accepted: contains R1, widened entry contains template', rep['bracket_recovery']['equals_registered_R1'] is False
          and rep['bracket_recovery']['changed_fs_entries'] == ['5', '6', '7', '8', '9', '10', '45', '50'])
    rep = scenario(work, cmp, pp_pass, pre, R1, 'R2_flag_cases_on_R1', {}, 'INCOMPLETE', recovery={'brackets': R2, 'reason': 'R2'})
    check('R2 with cases still on R1: every case V3 brackets', all('brackets' in g.get('V3_mismatch', []) for g in rep['gates'].values()))
    # 7 inherited outcomes
    scenario(work, cmp, pp_pass, pre, R1, 'inner_fail', {'R': 0.08}, 'INNER_UNRESOLVED')
    scenario(work, cmp, pp_pass, pre, R1, 'shape_disagree', {'plan': {'cylinder': ([-0.5, 0.15, 0.13], 2e-3)}}, 'NOT_CONVERGED')
    scenario(work, cmp, pp_pass, pre, R1, 'slow_contraction', {'plan': {'sphere': ([-0.1005, -0.049, 0.0], 3e-4), 'cylinder': ([-0.1, -0.0485, 0.0], 2e-3),
                                                                        'cube': ([0.1, 0.0485, 0.0], 1e-2)}}, 'NOT_CONVERGED')
    scenario(work, cmp, pp_pass, pre, R1, 'picard_gate', {}, 'INCOMPLETE', extra={'S4': {'last_change': 0.02}})
    rep = scenario(work, cmp, pp_pass, pre, R1, 'overmask_S4', {}, 'INCOMPLETE', extra={'S4': {'overmask': True}})
    check('over-masked S4 fails V5 only', rep['gates']['S4']['failed'] == ['V5'])
    scenario(work, cmp, pp_pass, pre, R1, 'identity_mismatch_S3', {}, 'INCOMPLETE', extra={'S3': {'ident': 'f' * 64}})
    scenario(work, cmp, pp_pass, pre, R1, 'm4_tie_cylinder', {'plan': {'cylinder': ([-0.5, -0.04, -0.01], 3.2e-4)}}, 'ADOPT/cylinder')
    # 8 pin refusals
    rc = cmp.main(['--prereg', str(pp_pass), '--cases', str(work / 'mock_v005_valid_adopt' / 'cases.json'), '--outdir', str(work / 'pin_refusal')])
    check('unpinned prereg refused without the test flag', rc == 2 and not (work / 'pin_refusal').exists())
    rc = cmp.main(['--prereg', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v004_c2/KMAX_MATRIX_PREREG_V004.json',
                   '--cases', str(work / 'mock_v005_valid_adopt' / 'cases.json'), '--outdir', str(work / 'v004_refusal')])
    check('prereg V004 refused by c2v005', rc == 2 and not (work / 'v004_refusal').exists())
    summary = {'schema': 'UNT_KMAX_COMPARE_TESTS_C2_V005', 'n': len(RESULTS), 'n_pass': sum(r['pass'] for r in RESULTS), 'results': RESULTS,
               'scripts': {p: sha(HERE / p) for p in ('kmax_compare_c2v005.py', 'tests_kmax_compare_c2v005.py')},
               'prereg_sha256': sha(real_path), 'r1_sha256': sha(HERE / 'd7_recovery' / 'KMAX_D7_RECOVERY_R1.json')}
    with open(work / 'TEST_RESULTS.json', 'x') as f:
        json.dump(summary, f, indent=1)
    print('%d/%d pass' % (summary['n_pass'], summary['n']))
    return 0 if summary['n_pass'] == summary['n'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
