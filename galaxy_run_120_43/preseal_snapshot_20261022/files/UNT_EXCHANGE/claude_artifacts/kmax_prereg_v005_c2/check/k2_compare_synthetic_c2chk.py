"""Checker K2: independent synthetic tests of kmax_compare_c2v005.py (written without reusing the author's tests).
Loads the compare script read-only by path and calls main(argv) in-process.  Synthetic result.json files on tiny
grids: a TEST copy of the real V005 prereg with only grids (and, in-process, the module constant BASE_SPEC for G2)
and binding_inputs.v005_deciding_test paths replaced by synthetic ones.  Test mode is therefore used everywhere
except the pin-refusal tests.  No file under CLAUDE2/runs is opened.
usage: python3 -I -B k2_compare_synthetic_c2chk.py NEW_WORKDIR
"""
import copy
import hashlib
import importlib.util
import io
import json
import contextlib
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
KPC = 3.085677581491367e19
OUT = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ok(name, cond, detail=None):
    OUT.append({'test': name, 'pass': bool(cond), 'detail': detail})
    print(('PASS ' if cond else 'FAIL ') + name + ('   ' + json.dumps(detail, default=str)[:400] if detail is not None else ''))


spec = importlib.util.spec_from_file_location('cmp_c2v005_under_check', str(LANE / 'kmax_compare_c2v005.py'))
CMP = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CMP)
REAL_PATH = LANE / 'KMAX_MATRIX_PREREG_V005.json'
REAL = json.loads(REAL_PATH.read_text())
R1REC = json.loads((LANE / 'd7_recovery/KMAX_D7_RECOVERY_R1.json').read_text())
R1 = R1REC['brackets']
ANCH = REAL['anchor']['brackets']
DRV = {k: v['sha256'] for k, v in REAL['binding_inputs']['drivers'].items()}
IDS = REAL['row_ids']
TAU = dict(zip(IDS, REAL['tau_km_s']))
V005_CASES = ['C3', 'C4', 'R', 'S3', 'Y3', 'S4', 'Y4']

TINY_G2 = {'breaks_inverse_kpc': [-2, -1, 0, 1, 2], 'panel_orders': [2, 2, 2, 2]}
TINY = {'G3': {'version': 't3', 'breaks_inverse_kpc': [-3, -1, 0, 1, 3], 'panel_orders': [2, 2, 2, 2], 'total_axis_nodes': 8, 'scope': 'test'},
        'G4': {'version': 't4', 'breaks_inverse_kpc': [-4, -2, 0, 2, 4], 'panel_orders': [3, 2, 2, 3], 'total_axis_nodes': 10, 'scope': 'test'},
        'GR': {'version': 'tr', 'breaks_inverse_kpc': [-2, -1, 0, 1, 2], 'panel_orders': [2, 3, 3, 2], 'total_axis_nodes': 10, 'scope': 'test'}}
CMP.BASE_SPEC = TINY_G2   # in-process only: G2 (composite_grid_spec null) uses the module default axis


def test_prereg(work, deciding_dir):
    p = copy.deepcopy(REAL)
    for g, s in TINY.items():
        p['grids'][g]['composite_grid_spec'] = s
    dt = p['binding_inputs']['v005_deciding_test']
    dt['result_path'] = str(deciding_dir / 'result.json')
    dt['finish_path'] = str(deciding_dir / 'finish.json')
    path = work / 'PREREG_TEST.json'
    path.write_text(json.dumps(p, indent=1))
    return path, p


def write_deciding(d, verdict='PASS_BITWISE_EQUAL', driver=None, spec_sha=None, finish='ok', result='ok', with_deciding=True):
    d.mkdir(parents=True, exist_ok=True)
    req = REAL['binding_inputs']['v005_deciding_test']['required']
    r = {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'status': 'COMPLETED', 'valid': True,
         'driver_sha256': driver or req['driver_sha256'], 'call_spec_sha256': spec_sha or req['call_spec_sha256']}
    if with_deciding:
        r['deciding_test'] = {'verdict': verdict, 'status': 'DIAGNOSTIC_ONLY'}
    for f in ('result.json', 'finish.json'):
        if (d / f).exists():
            (d / f).unlink()
    if result == 'absent':
        return
    if result == 'garbage':
        (d / 'result.json').write_text('{not json')
    else:
        (d / 'result.json').write_text(json.dumps(r))
    if finish == 'absent':
        return
    rs = sha(d / 'result.json')
    (d / 'finish.json').write_text(json.dumps({'status': 'COMPLETED', 'result_sha256': rs if finish == 'ok' else '0' * 64}))


def speeds(shape, K, bad=None):
    """v_i = 30 + shape offset + tail(K); d23 = 0.6 tau, d34 = 0.2 tau -> Dhat34 0.2, q 1/3 (pass)."""
    off = {'cube': 0.0, 'sphere': 0.01, 'cylinder': 0.02}[shape]
    f = {2: 0.0, 3: 0.6, 4: 0.8}[K]
    if bad == 'nonconv':
        f = {2: 0.0, 3: 0.3, 4: 0.6}[K]          # d34 = d23 -> q = 1 fails
    if bad == 'disagree' and K == 4:
        return {i: 30.0 + off + 0.8 * TAU[i] + 2.5 * TAU[i] for i in IDS}
    return {i: 30.0 + off + f * TAU[i] for i in IDS}


def mock(root, pre, cid, rows, brackets, driver, ident, status='COMPLETED', passes=6, last=0.004, m4=1.0, leak=False, grid_override=None,
         shape_override=None):
    c = {x['id']: x for x in pre['cases']}[cid]
    gs = pre['grids'][c['grid']]['composite_grid_spec']
    ax = CMP.expected_axis(gs)
    k = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
    edge = float((gs or CMP.BASE_SPEC)['breaks_inverse_kpc'][-1])
    m = CMP.driver_mask(k, c['shape'], (c['kmax_inverse_kpc'] or edge) / KPC)
    w = np.where(m[:, None, None], 1e-9 + 0j, 0j) * np.ones((len(k), 10, 1))
    if leak:
        w[np.argmax(~m)] = 1e-20
    d = root / cid
    (d / 'field').mkdir(parents=True)
    (d / 'rot').mkdir()
    np.savez(d / 'field/refreshed_prepared.npz', wavevectors=k, weighted_responses=w)
    (d / 'field/finish.json').write_text(json.dumps({'outputs': {'refreshed_prepared.npz': {'path': str(d / 'field/refreshed_prepared.npz'),
                                                                                            'sha256': sha(d / 'field/refreshed_prepared.npz')}}}))
    (d / 'rot/finish.json').write_text(json.dumps({'base_K_values_SI': [1.0] * 72}))
    anc = pre['anchor']
    trunc = {'shape': shape_override or c['shape'], 'kmax_inverse_kpc': c['kmax_inverse_kpc']}
    rad = [0.3 * KPC, 1.0 * KPC, 3.0 * KPC, 5.5 * KPC, 7.0 * KPC]
    r = {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'status': status, 'valid': status == 'COMPLETED', 'reasons': [],
         'driver_sha256': DRV[driver] if driver in DRV else driver, 'call_spec_sha256': hashlib.sha256(cid.encode()).hexdigest(),
         'rows': [{'id': i, 'speed_km_s': rows[i]} for i in IDS] if status == 'COMPLETED' else [],
         'normalized_spec': {'galaxy': 'DDO154', 'physical': anc['physical'], 'coefficients': anc['coefficients'],
                             'numerics': {'composite_grid_spec': grid_override if grid_override is not None else gs, 'truncation': trunc,
                                          'picard': {'passes': passes, 'speed_change_bound_km_s': 0.01, 'observe_every_pass': True},
                                          'brackets': brackets}},
         'passes': [{'pass': 1, 'max_abs_change_km_s': 1.0}, {'pass': 2, 'max_abs_change_km_s': last, 'field': str(d / 'field'), 'rotation': str(d / 'rot')}],
         'final_pass': 2, 'identity': {'route_a': {'custody': {'identity_sha256': ident}}},
         'residual_diagnostics': {'azimuthal_harmonics': {'per_radius_max': [{'m4': 9.0}, {'m4': m4}, {'m4': m4}, {'m4': m4}, {'m4': 9.0}],
                                                          'radial_nodes_m': rad, 'global_max': {'m4': 9.0, 'm8': 1.0}}}}
    (d / 'result.json').write_text(json.dumps(r))
    return str(d / 'result.json')


def standard(root, pre, mods=None):
    """10 cases: G2 (C2R/S2R/Y2R) v001 + R1; >80-node cases v005 + R1; identities per cube."""
    mods = mods or {}
    shp = {'C': 'cube', 'S': 'sphere', 'Y': 'cylinder'}
    cases = {}
    for c in pre['cases']:
        cid = c['id']
        if cid == 'R':
            rows = {i: 30.0 + 0.5 * TAU[i] for i in IDS}
        else:
            rows = speeds(shp[cid[0]], int(cid[1]), mods.get('bad_' + shp[cid[0]]))
        kw = {'brackets': R1, 'driver': 'v001' if c['grid'] == 'G2' else 'v005',
              'ident': {'G2': 'a' * 64, 'G3': 'b' * 64, 'G4': 'c' * 64, 'GR': 'd' * 64}[c['grid']]}
        kw.update(mods.get(cid, {}))
        if kw.pop('missing', False):
            continue
        rows = kw.pop('rows', rows)
        cases[cid] = mock(root, pre, cid, rows, **kw)
    return cases


def run(work, name, pre_path, pre, cases, recovery='R1', test_flag=True):
    root = work / name
    root.mkdir(parents=True, exist_ok=True)
    cf = root / 'cases.json'
    cf.write_text(json.dumps(cases))
    argv = ['--prereg', str(pre_path), '--cases', str(cf), '--outdir', str(root / 'out'), '--no-field-diagnostic']
    if recovery == 'R1':
        argv += ['--bracket-recovery', str(LANE / 'd7_recovery/KMAX_D7_RECOVERY_R1.json')]
    elif recovery is not None:
        rp = root / 'recovery.json'
        rp.write_text(json.dumps(recovery))
        argv += ['--bracket-recovery', str(rp)]
    if test_flag:
        argv.append('--test-allow-unpinned-prereg')
    err = io.StringIO()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
        rc = CMP.main(argv)
    rep = json.loads((root / 'out/KMAX_COMPARISON.json').read_text()) if (root / 'out/KMAX_COMPARISON.json').exists() else None
    return rc, rep, err.getvalue().strip()


def bad_set(rep):
    return sorted(c for c, g in rep['gates'].items() if not g['valid_all'])


def main(work):
    work = Path(work)
    work.mkdir(parents=False)
    ddir = work / 'deciding'
    pre_path, pre = test_prereg(work, ddir)
    # ---------- static facts
    ok('compare pins sha256(prereg V005 bytes)', CMP.PREREG_SHA256 == sha(REAL_PATH), CMP.PREREG_SHA256)
    ok('compare drivers table read from prereg includes v005 2aef51c4', DRV.get('v005', '').startswith('2aef51c4'))
    ok('real R1 file validates', CMP.validate_recovery(REAL, R1) == [], CMP.validate_recovery(REAL, R1))
    ok('anchor block as recovery is rejected (R1 entries not contained)', any('R1 entry' in x for x in CMP.validate_recovery(REAL, ANCH)))

    # ---------- 1. everything valid, deciding PASS -> ADOPT cube (tie order; all pass)
    write_deciding(ddir)
    rc, rep, _ = run(work, 's01_all_valid', pre_path, pre, standard(work / 's01_all_valid/res', pre))
    ok('s01 all valid + deciding PASS -> ADOPT cube', rc == 0 and rep['decision']['outcome'] == 'ADOPT' and rep['decision']['adopted_shape'] == 'cube'
       and bad_set(rep) == [] and rep['v005_admissibility']['admissible'] is True, {'dec': rep['decision'].get('outcome'), 'bad': bad_set(rep)})
    ok('s01 report records recovery R1 (equals_registered_R1, changed fs entries 5..9,45,50)',
       rep['bracket_recovery']['equals_registered_R1'] and rep['bracket_recovery']['changed_fs_entries'] == ['5', '6', '7', '8', '9', '45', '50']
       and rep['bracket_recovery']['changed_rule_keys'] == ['fs_absolute_overrides'], rep['bracket_recovery'])
    ok('s01 carried u_i has 3 terms and adopts at G4', rep['decision']['adopted_grid'] == 'G4' and set(rep['decision']['carried_terms']) == {'K34', 'inner', 'shape_spread'})

    # ---------- 2. deciding failure branches: every v005 case V3-only V005_INADMISSIBLE, G2 cases untouched
    branches = {
        'result_absent': dict(result='absent'),
        'finish_absent': dict(finish='absent'),
        'finish_sha_mismatch': dict(finish='bad'),
        'verdict_FAIL': dict(verdict='FAIL'),
        'verdict_missing': dict(with_deciding=False),
        'wrong_driver': dict(driver='75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22'),
        'wrong_call_spec': dict(spec_sha='f' * 64),
        'unreadable_result': dict(result='garbage'),
        'verdict_lowercase': dict(verdict='pass_bitwise_equal'),
    }
    for nm, kw in branches.items():
        write_deciding(ddir, **kw)
        rc, rep, err = run(work, 's02_' + nm, pre_path, pre, standard(work / ('s02_%s/res' % nm), pre))
        bad = bad_set(rep)
        v3only = all(rep['gates'][c]['failed'] == ['V3'] and rep['gates'][c]['V3_mismatch'] and
                     all(m.startswith('V005_INADMISSIBLE') for m in rep['gates'][c]['V3_mismatch']) for c in V005_CASES)
        nxt = all(rep['decision']['next_step'][c]['V3'] == REAL['amendment_v005']['driver']['inadmissible_next_step'] for c in V005_CASES)
        ok('s02 deciding %s -> INCOMPLETE, exactly the 7 v005 cases V3-only V005_INADMISSIBLE, next step = inadmissible_next_step' % nm,
           rc == 0 and rep['decision']['outcome'] == 'INCOMPLETE' and bad == sorted(V005_CASES) and v3only and nxt
           and rep['v005_admissibility']['admissible'] is False,
           {'bad': bad, 'reason': rep['v005_admissibility'].get('reason')})
    write_deciding(ddir)

    # ---------- 3. no single-shape adoption: missing / failed G2 sphere or cylinder -> INCOMPLETE
    rc, rep, _ = run(work, 's03_S2R_Y2R_missing', pre_path, pre, standard(work / 's03_S2R_Y2R_missing/res', pre, {'S2': {'missing': True}, 'Y2': {'missing': True}}))
    ok('s03 S2/Y2 missing (cube complete and passing) -> INCOMPLETE naming S2,Y2 missing; no adoption',
       rep['decision']['outcome'] == 'INCOMPLETE' and bad_set(rep) == ['S2', 'Y2'] and rep['gates']['S2']['failed'] == ['missing'], bad_set(rep))
    rc, rep, _ = run(work, 's03b_S2_failed_at_stage', pre_path, pre, standard(work / 's03b_S2_failed_at_stage/res', pre, {'S2': {'status': 'FAILED_AT_STAGE'}}))
    ok('s03b S2 FAILED_AT_STAGE -> INCOMPLETE with V1 next step naming the D7 recovery',
       rep['decision']['outcome'] == 'INCOMPLETE' and 'V1' in rep['gates']['S2']['failed'] and 'D7 recovery' in rep['decision']['next_step']['S2']['V1'], rep['gates']['S2']['failed'])
    rc, rep, _ = run(work, 's03c_only_cube_passes', pre_path, pre, standard(work / 's03c_only_cube_passes/res', pre, {'bad_sphere': 'nonconv', 'bad_cylinder': 'nonconv'}))
    ok('s03c all cases valid, only cube passes -> ADOPT cube (pre-registered rule 5 among valid cases)',
       rep['decision']['outcome'] == 'ADOPT' and rep['decision']['adopted_shape'] == 'cube' and rep['sequences']['sphere']['pass'] is False, rep['decision']['reasons'])

    # ---------- 4. D7 step (4): a case on the anchor block fails V3 brackets
    rc, rep, _ = run(work, 's04_C2_on_anchor', pre_path, pre, standard(work / 's04_C2_on_anchor/res', pre, {'C2': {'brackets': ANCH, 'passes': 4, 'last': 0.005}}))
    ok('s04 C2 bound call (anchor block, passes 4 within bound) -> only C2 invalid, V3 brackets',
       bad_set(rep) == ['C2'] and rep['gates']['C2']['V3_mismatch'] == ['brackets'], rep['gates']['C2'].get('V3_mismatch'))
    rc, rep, _ = run(work, 's04b_C3_on_anchor', pre_path, pre, standard(work / 's04b_C3_on_anchor/res', pre, {'C3': {'brackets': ANCH}}))
    ok('s04b v005 C3 first run (anchor block) -> only C3 invalid, V3 brackets', bad_set(rep) == ['C3'] and rep['gates']['C3']['V3_mismatch'] == ['brackets'])

    # ---------- 5. other decision branches
    rc, rep, _ = run(work, 's05_none_pass', pre_path, pre, standard(work / 's05_none_pass/res', pre, {'bad_cube': 'nonconv', 'bad_sphere': 'nonconv', 'bad_cylinder': 'nonconv'}))
    ok('s05 no shape passes -> NOT_CONVERGED', rep['decision']['outcome'] == 'NOT_CONVERGED' and 'subtype' not in rep['decision'], rep['decision']['outcome'])
    rc, rep, _ = run(work, 's05b_disagree', pre_path, pre, standard(work / 's05b_disagree/res', pre, {'bad_sphere': 'disagree'}))
    ok('s05b sphere K=4 off by 2.5 tau -> NOT_CONVERGED/SHAPE_DISAGREEMENT or sphere fails pass',
       rep['decision']['outcome'] == 'NOT_CONVERGED' or (rep['decision']['outcome'] == 'ADOPT' and rep['sequences']['sphere']['pass'] is False), rep['decision'])
    rows_disagree = {i: 30.0 + 0.8 * TAU[i] + 2.2 * TAU[i] for i in IDS}
    rows_y3 = {i: 30.0 + 0.6 * TAU[i] + 2.2 * TAU[i] for i in IDS}
    rows_y2 = {i: 30.0 + 0.0 * TAU[i] + 2.2 * TAU[i] for i in IDS}
    rc, rep, _ = run(work, 's05c_disagree_passing', pre_path, pre, standard(work / 's05c_disagree_passing/res', pre,
                                                                             {'Y4': {'rows': rows_disagree}, 'Y3': {'rows': rows_y3}, 'Y2': {'rows': rows_y2}}))
    ok('s05c cylinder passes but offset 2.2 tau at K=4 -> NOT_CONVERGED SHAPE_DISAGREEMENT',
       rep['decision']['outcome'] == 'NOT_CONVERGED' and rep['decision'].get('subtype') == 'SHAPE_DISAGREEMENT', rep['decision'].get('reasons'))
    rc, rep, _ = run(work, 's05d_inner', pre_path, pre, standard(work / 's05d_inner/res', pre, {'R': {'rows': {i: 30.0 + 1.5 * TAU[i] for i in IDS}}}))
    ok('s05d Dhat_R 1.5 -> INNER_UNRESOLVED', rep['decision']['outcome'] == 'INNER_UNRESOLVED', rep['decision']['outcome'])

    # ---------- 6. gate details
    rc, rep, _ = run(work, 's06_S2_v005', pre_path, pre, standard(work / 's06_S2_v005/res', pre, {'S2': {'driver': 'v005'}}))
    ok('s06 S2 under v005 -> V3 (driver not allowed) and V6 (driver != cube)', set(rep['gates']['S2']['failed']) == {'V3', 'V6'}, rep['gates']['S2'])
    rc, rep, _ = run(work, 's06b_S3_v003', pre_path, pre, standard(work / 's06b_S3_v003/res', pre, {'S3': {'driver': 'v003'}}))
    ok('s06b S3 under v003 admitting v005 C3 -> V6 only', rep['gates']['S3']['failed'] == ['V6'], rep['gates']['S3']['failed'])
    rc, rep, _ = run(work, 's06c_C3_unknown_driver', pre_path, pre, standard(work / 's06c_C3_unknown_driver/res', pre, {'C3': {'driver': 'e' * 64}}))
    ok('s06c C3 unknown driver sha -> V3', 'V3' in rep['gates']['C3']['failed'])
    rc, rep, _ = run(work, 's06d_Y4_leak', pre_path, pre, standard(work / 's06d_Y4_leak/res', pre, {'Y4': {'leak': True}}))
    ok('s06d Y4 mask leak -> V5 only', rep['gates']['Y4']['failed'] == ['V5'], rep['gates']['Y4']['failed'])
    rc, rep, _ = run(work, 's06e_S4_ident', pre_path, pre, standard(work / 's06e_S4_ident/res', pre, {'S4': {'ident': 'e' * 64}}))
    ok('s06e S4 route-A identity != C4 -> V6 only', rep['gates']['S4']['failed'] == ['V6'])
    rc, rep, _ = run(work, 's06f_picard', pre_path, pre, standard(work / 's06f_picard/res', pre, {'C3': {'last': 0.02}}))
    ok('s06f C3 final change 0.02 > 0.0125 -> V2 only', rep['gates']['C3']['failed'] == ['V2'])
    rc, rep, _ = run(work, 's06g_C2_passes4_not_eq', pre_path, pre, standard(work / 's06g_C2_passes4_not_eq/res', pre, {'C2': {'passes': 4, 'last': 0.011}}))
    ok('s06g C2 passes 4 stopped by cap (0.011 > 0.01) -> V3 PICARD_CAP_NOT_EQUIVALENT', 'PICARD_CAP_NOT_EQUIVALENT' in rep['gates']['C2'].get('V3_mismatch', []))

    # ---------- 7. D7 recovery argument handling
    rc, rep, err = run(work, 's07_no_recovery_arg', pre_path, pre, standard(work / 's07_no_recovery_arg/res', pre), recovery=None)
    ok('s07 invoked D7 without --bracket-recovery -> REFUSED rc 2, no output', rc == 2 and rep is None and 'bracket-recovery' in err, err)
    rec = {'brackets': ANCH, 'reason': 'x'}
    rc, rep, err = run(work, 's07b_anchor_as_recovery', pre_path, pre, {}, recovery=rec)
    ok('s07b anchor block as recovery -> REFUSED', rc == 2 and rep is None, err[:200])
    b = copy.deepcopy(R1); b['rule']['fs_absolute_overrides']['46'] = [3.03e8, 3.17625e8]
    rc, rep, err = run(work, 's07c_narrow46', pre_path, pre, {}, recovery={'brackets': b, 'reason': 'x'})
    ok('s07c narrowing anchor entry 46 -> REFUSED', rc == 2 and 'narrowed' in err, err[:200])
    b = copy.deepcopy(R1); del b['rule']['fs_absolute_overrides']['47']
    rc, rep, err = run(work, 's07d_remove47', pre_path, pre, {}, recovery={'brackets': b, 'reason': 'x'})
    ok('s07d removing anchor entry 47 -> REFUSED', rc == 2 and 'removed' in err, err[:200])
    b = copy.deepcopy(R1); b['rule']['rfs_factors'] = [0.7, 1.2]
    rc, rep, err = run(work, 's07e_rfs_factors', pre_path, pre, {}, recovery={'brackets': b, 'reason': 'x'})
    ok('s07e changing rfs_factors -> REFUSED', rc == 2 and 'non-override' in err, err[:200])
    b = copy.deepcopy(R1); b['rule']['fs_absolute_overrides']['5'] = [3.025e8, 3.17625e8]
    rc, rep, err = run(work, 's07f_R1_entry_undone', pre_path, pre, {}, recovery={'brackets': b, 'reason': 'x'})
    ok('s07f undoing an R1 widening -> REFUSED (R1 entry not contained)', rc == 2 and 'R1 entry' in err, err[:200])
    b = copy.deepcopy(R1); b['rule']['fs_absolute_overrides']['60'] = [2.0e8, 3.1e8]
    rc, rep, err = run(work, 's07g_new_entry_no_template', pre_path, pre, {}, recovery={'brackets': b, 'reason': 'x'})
    ok('s07g new entry not containing the fs template -> REFUSED', rc == 2 and 'template' in err, err[:200])
    rc, rep, err = run(work, 's07h_extra_key', pre_path, pre, {}, recovery={'brackets': R1, 'reason': 'x', 'note': 'y'})
    ok('s07h extra top-level key in recovery file -> REFUSED', rc == 2 and rep is None, err[:200])
    b = copy.deepcopy(R1); b['extra'] = 1
    rc, rep, err = run(work, 's07i_extra_block_key', pre_path, pre, {}, recovery={'brackets': b, 'reason': 'x'})
    ok('s07i extra key in brackets block -> REFUSED', rc == 2 and rep is None, err[:200])
    b = copy.deepcopy(R1); b['rule']['fs_absolute_overrides']['46'] = [1.5125e8, 3.17625e8]; b['rule']['fs_absolute_overrides']['60'] = [1.5e8, 3.1e8]
    write_deciding(ddir)
    rc, rep, err = run(work, 's07j_R2_valid_cases_on_R1', pre_path, pre, standard(work / 's07j_R2_valid_cases_on_R1/res', pre), recovery={'brackets': b, 'reason': 'R2', 'invocation': 'R2'})
    ok('s07j valid R2 (widens 46, adds 60 containing template) accepted; cases still on R1 all fail V3 brackets',
       rc == 0 and rep['bracket_recovery']['equals_registered_R1'] is False and bad_set(rep) == sorted(c['id'] for c in REAL['cases'])
       and all('brackets' in rep['gates'][c]['V3_mismatch'] for c in bad_set(rep)), {'rc': rc, 'err': err[:200]})
    b = copy.deepcopy(R1); b['rule']['le_factor_overrides'] = {'1': {'3': [0.3, 0.95]}}
    ok('le_factor_overrides new entry containing le_first_factors accepted by validate_recovery', CMP.validate_recovery(REAL, b) == [], CMP.validate_recovery(REAL, b))
    b['rule']['le_factor_overrides'] = {'2': {'3': [0.85, 1.1]}}
    ok('le_factor_overrides new entry not containing le_next_factors rejected', CMP.validate_recovery(REAL, b) != [], CMP.validate_recovery(REAL, b))

    # ---------- 8. pin refusals (real prereg path never run end-to-end: it would stat the real deciding outdir)
    tam = work / 'tampered.json'
    tam.write_text(REAL_PATH.read_text().replace('"schema": "KMAX_MATRIX_PREREG_V005"', '"schema": "KMAX_MATRIX_PREREG_V005X"'))
    rc, rep, err = run(work, 's08_tampered', tam, pre, {}, test_flag=False)
    ok('s08 tampered prereg without test flag -> REFUSED', rc == 2 and 'pinned' in err, err[:160])
    v4 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v004_c2/KMAX_MATRIX_PREREG_V004.json')
    rc, rep, err = run(work, 's08b_v004', v4, pre, {}, test_flag=False)
    ok('s08b prereg V004 -> REFUSED', rc == 2 and 'pinned' in err, err[:160])
    rc, rep, err = run(work, 's08c_unregistered_id', pre_path, pre, {'S2R': '/nonexistent'})
    ok('s08c unregistered case id "S2R" in cases.json -> REFUSED (cases.json must use registered ids)', rc == 2, err[:160])

    n = len(OUT); p = sum(1 for x in OUT if x['pass'])
    (work / 'K2_RESULTS.json').write_text(json.dumps({'compare_sha256': sha(LANE / 'kmax_compare_c2v005.py'), 'prereg_sha256': sha(REAL_PATH),
                                                     'tests': OUT, 'pass': p, 'total': n}, indent=1, default=str))
    print('%d/%d pass' % (p, n))
    return 0 if p == n else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
