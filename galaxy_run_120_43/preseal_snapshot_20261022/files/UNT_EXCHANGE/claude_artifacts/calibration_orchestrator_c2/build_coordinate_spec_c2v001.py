"""build_coordinate_spec_c2v001 -- builds DDO154_CALIBRATION_COORDINATE_SPEC_V001.json (Claude2 lane).

PROPOSED FINAL coordinate spec for Claude2 to freeze. It supersedes the draft
calibration_prep_c2_0470/calibration_spec/DDO154_CALIBRATION_COORDINATE_SPEC_DRAFT_C2V001.json (a7709bd2...)
and applies its checker's corrections (calibration_spec_check/CHECK_V001.md, PASS_WITH_CORRECTIONS, D1-D21).

Every input is verified from bytes before use. Read-only everywhere; the only file written is the spec JSON next to
this script (exclusive create; refuses to overwrite). No forward is run, no NGC3198 file is opened, no network.
The A2 anchor run result and the seed-scan / factor-3 results are read (completed runs; read-only).

usage: <codex python3> -I -B build_coordinate_spec_c2v001.py [--out PATH]
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
UPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
C2 = UPC + '/CLAUDE2'

PINS = {
    'engine_c2v003a': (ART + '/calibration_freeze_c2_v003a/calibration_region_engine_c2v003a.py',
                       '193841fa1f1d078f7fc981fdba78cf3d736b50ee17e019f0cf94aae94e3a63a6'),
    'freeze_c2v003a': (ART + '/calibration_freeze_c2_v003a/prediction_freeze_c2v003a.py',
                       '5ee3e5dce72c77870903ce378e146fb86f7288ab2a403deb39796e348ee0f9b8'),
    'delta_v003_v003a': (ART + '/calibration_freeze_c2_v003a/DELTA_V003_V003A.md',
                         '881286532338d2543eb28d9fc849429a817975d89c3f238522afc836805341d3'),
    'root_call_order_v003': (ART + '/calibration_freeze_c2_v003/final/ROOT_CALL_ORDER.md',
                             'ab5d467e6fa409e46e2f5eb99172416139f837206f6c5fd8a626d5cbff57837b'),
    'engine_note_v002': (ART + '/calibration_freeze_c2_v002/ENGINE_DELTA_NOTES.md',
                         'f96b83a4ecc6f4089a5024c54fefc65ca9f37844261afa6a51279f4976a766fe'),
    'driver_v003c': (ART + '/absorb_c2_0473/driver_f/galaxy_m0_forward_c2v003c.py',
                     'ed326130e89654a377615e46a077764cf3ad39e0bf07bc9d0606225bc69fbdf2'),
    'driver_v003c_check': (ART + '/absorb_c2_0473/driver_f/CHECK_V001.md',
                           '1e31055c449e635ed3c90b3394cf112e177914911fe340f238d248722b2ab4bb'),
    'driver_v003b': (ART + '/galaxy_m0_forward_c2_v003/galaxy_m0_forward_c2v003b.py',
                     '7ce59e05f39e0517fd7c1d89a6c31b116b96662ee475fec88f47ae76ab1184f1'),
    'driver_v003b_interface': (ART + '/galaxy_m0_forward_c2_v003/INTERFACE_V003B_DELTA.md',
                               'e45d8bd41887eff3bf55dfa212a84963294e94c4c123773ca5af3ed196ded159'),
    'driver_v001_anchor': (ART + '/galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py',
                           '75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22'),
    'monitor_c2v001': (ART + '/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
                       'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'),
    'campaign_c2v001': (ART + '/galaxy_m0_forward_c2_0466/campaign_c2v001.py',
                        '71274ceb15e57786ee8f575fd74b48e848193467156f0adcebbe7ee415e44597'),
    'draft_spec': (ART + '/calibration_prep_c2_0470/calibration_spec/DDO154_CALIBRATION_COORDINATE_SPEC_DRAFT_C2V001.json',
                   'a7709bd2a9ace5dc34ae31cb75b07f570ff39fcbbd99c6f4bbaa367eed620d54'),
    'draft_spec_check': (ART + '/calibration_prep_c2_0470/calibration_spec_check/CHECK_V001.md',
                         'c7bd9613702cfc025dfbdd10c3114afbc4575137516cc0be870fd5af059c728a'),
    'observation_region': (UPC + '/CODEX1/DDO154_CALIBRATION_OBSERVATION_REGION_V001.json',
                           '13c16a6394fde450c9c1d9b258a8fb5dd01d80ce275a54d9761a285f76145b6d'),
    'anchor_spec': (C2 + '/specs/CALL_A2_ANCHOR_F10_C2V001.json',
                    'a93c95b95c1f112b7293ffd598371335227cb93d7334981be33e368c6cd9f52b'),
    'anchor_receipt': (C2 + '/runs/A2_ANCHOR_F10_RUN_V001.receipt.json',
                       'f8bc976a2b8084b4da1b7e846e3ce3997871c3689449e4a6c04788bc16b4acce'),
    'anchor_result': (C2 + '/runs/A2_ANCHOR_F10_RUN_V001/result.json',
                      'bcd2f64ec6c858a51718b2badb85b9e35121b6a3575227a4c9e4b8b5c673836e'),
    'f3_receipt': (C2 + '/runs/A2_ANCHOR_F3_RUN_V001.receipt.json',
                   '5c3c7171349d30c74d162c389bc709cdac3fbe8803aa3cc8e16e53cc4bc908af'),
    'f3_result': (C2 + '/runs/A2_ANCHOR_F3_RUN_V001/result.json',
                  '529f395475ffc26f05d29501746ca70b8f811832144a6eb8b305772a2627e729'),
    'seed_scan_result': (C2 + '/runs/A2_SEED_SCAN_G2_RUN_V001/result.json',
                         '951580e26aea5a0b4d0d2d73da7b1730effaac9444f385908e1ee4bb9778677d'),
    'a2_coefficients': (C2 + '/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
                        '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'),
    'cycle_run_result': (UPC + '/CODEX1/OWNED_L4_CURRENT_GRAPH_CYCLE_RUN_V001/result.json',
                         '6377a9bc71b05d9fb288e9260e83b4237daf1c487f30bd59d6a168e0894aea8f'),
    'admission_run_result': (UPC + '/CODEX1/OWNED_L4_ADMISSION_RESIDENCE_RUN_V001/result.json',
                             '3c82d2be7993669cab01430e0eea34eeb603985a8533fc72ed804f93ddb88d19'),
    'root_decisions_a1_a2': (C2 + '/ROOT_DECISIONS_A1_A2_2026-10-17_V001.md',
                             'c8bf13d3beb5d833c308936b54c993deb684aa8949e79d7692d5e8eded740e36'),
    'root_decisions_ngc': (C2 + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V001.md',
                           '06cae881fe075b421e0fd0b7664ba389876228011ab4baec73df4e216c42a905'),
}
NATIVE_LITERALS = ('Ud', 'dstar', 'Delta', 'lambda_J', 'lambda_R', 'epsilon_c', 'epsilon_r', 'E_R', 'E_S', 'E_I',
                   'e_R', 'e_I', 'C_identity', 'h', 't', 'g', 'kappa', 'epsilon', 'theta')
ANCHOR_ALIAS_RTOL = 1e-14
MAPPING_ID = 'C2V001_PHYS4_GAMMA_EQ_GE_TIMES_EREF'


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def read_pinned(key):
    path, want = PINS[key]
    raw = open(path, 'rb').read()
    got = hashlib.sha256(raw).hexdigest()
    if got != want:
        raise SystemExit('PIN MISMATCH %s: %s != %s (%s)' % (key, got, want, path))
    return raw


def load_module(key, name):
    raw = read_pinned(key)
    path = PINS[key][0]
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    if sha_file(path) != PINS[key][1]:
        raise SystemExit('module changed while loading: %s' % key)
    del raw
    return m


def coord(name, transform, lower, upper, role, trial, units, scope, kind, ref=None, sens=None):
    return {'name': name, 'transform': transform, 'lower': float(lower), 'upper': float(upper), 'role': role,
            'trial_value': float(trial), 'units': units, 'scope': scope, 'kind': kind, 'reference_value': ref,
            'sensitivity': sens}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(HERE, 'DDO154_CALIBRATION_COORDINATE_SPEC_V001.json'))
    a = ap.parse_args(argv)
    verified = {}
    for key in PINS:
        if key in ('cycle_run_result', 'admission_run_result', 'a2_coefficients'):
            if sha_file(PINS[key][0]) != PINS[key][1]:
                raise SystemExit('PIN MISMATCH %s' % key)
        else:
            read_pinned(key)
        verified[key] = {'path': PINS[key][0], 'sha256': PINS[key][1]}
    E = load_module('engine_c2v003a', 'eng_spec_builder')
    F = load_module('freeze_c2v003a', 'frz_spec_builder')
    region = json.loads(read_pinned('observation_region'))
    anchor_spec = json.loads(read_pinned('anchor_spec'))
    anchor_res = json.loads(read_pinned('anchor_result'))
    anchor_rcpt = json.loads(read_pinned('anchor_receipt'))
    f3_res = json.loads(read_pinned('f3_result'))
    f3_rcpt = json.loads(read_pinned('f3_receipt'))
    scan = json.loads(read_pinned('seed_scan_result'))
    draft = json.loads(read_pinned('draft_spec'))

    # ---- native literals at the A2 point: both provenance trial dicts, verified from bytes -------------------
    trials = []
    for key in ('cycle_run_result', 'admission_run_result'):
        doc = json.load(open(PINS[key][0], 'rb'))
        trials.append((doc['trial'], doc['sampler_result']['inputs']['beta']))
    if trials[0] != trials[1]:
        raise SystemExit('cycle and admission trial dicts differ')
    trial_dict, beta = trials[0]
    if sorted(trial_dict) != sorted(NATIVE_LITERALS) or beta != 1.0:
        raise SystemExit('unexpected native literal set')

    # ---- anchor (A2 factor 10) -------------------------------------------------------------------------------
    ph = anchor_spec['physical']
    Eref = ph['Eref_J']
    s0 = ph['common_scale_s']
    gam = ph['gamma']
    ell0 = ph['ell_F_m']
    ge0 = gam / Eref
    if ge0 * Eref != gam:
        raise SystemExit('gamma_over_Eref * Eref does not reproduce the anchor gamma bitwise')
    if not (anchor_res['valid'] is True and anchor_res['status'] == 'COMPLETED'
            and anchor_res['call_spec_sha256'] == PINS['anchor_spec'][1]
            and anchor_res['driver_sha256'] == PINS['driver_v001_anchor'][1]):
        raise SystemExit('anchor result does not bind to the anchor spec / driver')
    if anchor_rcpt['result']['sha256'] != PINS['anchor_result'][1] or anchor_rcpt['driver_status'] != 'COMPLETED':
        raise SystemExit('anchor receipt does not bind to the anchor result')

    # ---- evaluated evidence: seed scan (route-A G2 kernel rule) and the factor-3 full-chain call -------------
    cands = {c['factor']: c for c in scan['candidates']}
    if scan['status'] != 'COMPLETED_SELECTED' or sorted(cands) != [1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0] or \
            not all(c['rule_pass'] for c in cands.values()):
        raise SystemExit('seed scan is not the expected rule-pass 1..1000 scan')
    if cands[10.0]['scale_s'] != s0 or cands[10.0]['candidate_seed']['gamma_eval'] != gam:
        raise SystemExit('factor-10 scan candidate is not the anchor')
    g_lo = cands[1.0]['candidate_seed']['gamma_over_Eref']
    g_hi = cands[100.0]['candidate_seed']['gamma_over_Eref']
    if not (g_lo < ge0 < g_hi):
        raise SystemExit('anchor gamma_over_Eref outside the factor 1..100 scan values')
    f3 = cands[3.0]
    if f3_res['status'] != 'FAILED' or f3_res['valid'] is not False or 'KeyError: 70' not in f3_res['reasons']:
        raise SystemExit('factor-3 result is not the recorded rfs column-70 failure')
    f3_s, f3_ge = f3['scale_s'], f3['candidate_seed']['gamma_over_Eref']

    # ---- coordinates (freeze format, 11 keys each) ----------------------------------------------------------
    ds = region['distance_summary']
    box = E.ddo154_distance_box(distance_summary=ds, modulus_half_width_multiple=1.0)
    if not box['ok']:
        raise SystemExit('distance box: %s' % box['reasons'])
    coords = [
        coord('common_scale_s', 'log', s0 * 0.5, s0 * 2.0, 'free', s0, 'dimensionless', 'shared', 'other'),
        coord('gamma_over_Eref', 'log', g_lo, g_hi, 'free', ge0, 'gamma per J of Eref_base_J', 'shared', 'other'),
        coord('ell_F_m', 'log', ell0 * 0.5, ell0 * 2.0, 'free', ell0, 'm', 'shared', 'other'),
        coord('distance_Mpc', 'log', box['lower'], box['upper'], 'nuisance', 4.04, 'Mpc', 'ddo154_nuisance',
              'distance', ref=4.04),
        coord('Eref_base_J', 'linear', Eref * 0.5, Eref * 2.0, 'fixed', Eref, 'J', 'shared', 'other'),
        coord('entropy_K_factor', 'linear', 64.0 / 121.0, 196.0 / 121.0, 'fixed', ph['entropy_K_factor'],
              'dimensionless (K / K(sigma0=11 km/s, Gamma))', 'shared', 'other'),
        coord('ML_3p6', 'linear', 0.4, 0.6, 'fixed', 0.5, 'solar M/L at 3.6 micron', 'shared', 'other'),
        coord('helium_factor', 'linear', 1.33, 1.36, 'fixed', 1.36, 'dimensionless (total gas / HI)', 'shared',
              'other'),
        coord('Gamma_poly', 'linear', 1.4, 5.0 / 3.0, 'fixed', 5.0 / 3.0, 'dimensionless (polytropic index)',
              'shared', 'other'),
    ]
    for lit in NATIVE_LITERALS:
        v = float(trial_dict[lit])
        coords.append(coord('native_' + lit, 'linear', v - 1.0, v + 1.0, 'fixed', v,
                            'dimensionless (sampler literal; energy ratios in units of Ud)', 'shared', 'other'))
    coords.append(coord('native_beta', 'linear', 0.0, 2.0, 'fixed', float(beta), 'dimensionless (sampler beta)',
                        'shared', 'other'))
    if abs(ph['entropy_K_factor'] - 64.0 / 121.0) > 0.0:
        raise SystemExit('anchor entropy factor is not 64/121')
    # NGC3198 slots: filled by the NGC lane before freeze. These placeholders exist only so the freeze module can
    # emit engine_coordinates; engine coordinates never contain NGC slots (verified below with two placeholder sets).
    ngc_placeholder = [
        coord('ngc3198_distance_Mpc', 'log', 12.0, 15.6, 'nuisance', 13.8, 'Mpc', 'ngc3198_nuisance', 'distance',
              ref=13.8, sens={'mode': 'box_ends'}),
        coord('ngc3198_inclination_deg', 'linear', 60.0, 80.0, 'nuisance', 70.0, 'deg', 'ngc3198_nuisance',
              'inclination', ref=None, sens={'mode': 'box_ends'}),
    ]
    alt_ngc = [dict(c, lower=c['lower'] * 0.99, upper=c['upper'] * 1.01) for c in ngc_placeholder]
    fs = F.make_freeze_coordinate_spec(coordinates=coords + ngc_placeholder)
    fs2 = F.make_freeze_coordinate_spec(coordinates=coords + alt_ngc)
    if not (fs['ok'] and fs2['ok']):
        raise SystemExit('make_freeze_coordinate_spec: %s %s' % (fs['reasons'], fs2['reasons']))
    eng_coords = fs['engine_coordinates']
    if json.dumps(eng_coords, sort_keys=True) != json.dumps(fs2['engine_coordinates'], sort_keys=True):
        raise SystemExit('engine coordinates depend on NGC slots')
    es = E.make_coordinate_spec(coordinates=eng_coords)
    if not es['ok']:
        raise SystemExit('engine make_coordinate_spec: %s' % es['reasons'])
    # engine trial_u exactly as run_calibration_region computes it (L2621-2625), then the seed theta it requests
    tu = []
    for nm in es['varying_names']:
        tr = es['transforms'][nm]
        xl, xh = E._x_of(tr, es['lower'][nm]), E._x_of(tr, es['upper'][nm])
        tu.append((E._x_of(tr, es['trial_values'][nm]) - xl) / (xh - xl))
    nat = E.to_natural(spec=es, u=tu)
    th = nat['theta_natural']
    seed_phys = {'common_scale_s': th['common_scale_s'], 'gamma': th['gamma_over_Eref'] * th['Eref_base_J'],
                 'ell_F_m': th['ell_F_m'], 'distance_Mpc': th['distance_Mpc'], 'Eref_J': th['Eref_base_J']}
    dev = {k: (seed_phys[k] - ph[k]) / ph[k] for k in seed_phys}
    if max(abs(v) for v in dev.values()) > ANCHOR_ALIAS_RTOL:
        raise SystemExit('engine seed theta deviates from the anchor beyond the alias tolerance: %r' % dev)

    # ---- distance binding through the engine's own check --------------------------------------------------------
    reg = E.load_observation_region(path=PINS['observation_region'][0], expected_sha256=PINS['observation_region'][1])
    bind = E._check_distance_binding(es, reg, {'name': 'distance_Mpc', 'modulus_half_width_multiple': 1.0})
    if not bind['ok']:
        raise SystemExit('distance binding: %s' % bind['reasons'])
    # anchor speeds against the rectangles (DDO154 calibration rows only; evidence for the repair path)
    cls = E.classify_prediction(prediction={'valid': True, 'speeds_km_s': anchor_res['speeds_km_s'], 'reasons': []},
                                rectangles=reg['rectangles'], row_ids=reg['row_ids'])
    v2 = [(reg['observed'][r] / anchor_res['speeds_km_s'][r]) ** 2 for r in reg['row_ids']]

    eng_params = {
        'budget': 120, 'rel_step': 0.05, 'min_step': 0.005, 'max_halvings': 2, 'null_tolerance': 0.001,
        'repair_iterations': 3, 'max_repair_step': 0.25, 'march_step': 0.05, 'bisection_steps': 3,
        'design_count': 12, 'global_design_count': 12, 'max_march_rounds': 2, 'hull_growth_tol': 0.02,
        'rng_seed': 0, 'u_seed': None,
        'ddo154_distance': {'name': 'distance_Mpc', 'modulus_half_width_multiple': 1.0},
    }
    # per-side march bound used by the orchestrator's sibling guard (documented here for the record)
    n_var = len(es['varying_names'])
    side_bound = int(math.floor(math.log2(math.sqrt(n_var) / eng_params['march_step']))) + 2 + eng_params['bisection_steps']

    spec = {
        'schema': 'DDO154_CALIBRATION_COORDINATE_SPEC_C2V001',
        'status': 'PROPOSED_FINAL_FOR_FREEZE_BY_CLAUDE2_NOT_FROZEN',
        'decides_nothing_physical': True,
        'author': 'Claude2-lane subagent, claude_artifacts/calibration_orchestrator_c2 (build_coordinate_spec_c2v001.py)',
        'created_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'supersedes': {'path': PINS['draft_spec'][0], 'sha256': PINS['draft_spec'][1]},
        'applies_check': {'path': PINS['draft_spec_check'][0], 'sha256': PINS['draft_spec_check'][1],
                          'verdict': 'PASS_WITH_CORRECTIONS'},
        'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS',
        'ngc3198_access': 'NONE',
        'ngc3198_rule': ('NGC3198 is never used in calibration: no NGC3198 target file is read by this spec, its builder, '
                         'the orchestrator or any calibration call, and no NGC3198 value is used; no box, alternative, '
                         'engine parameter or freeze choice depends on NGC3198 information. NGC3198 target velocities '
                         'are opened only by score_after_freeze after verify_freeze_manifest passes (ROOT_CALL_ORDER 8).'),
        'engine': {'path': PINS['engine_c2v003a'][0], 'sha256': PINS['engine_c2v003a'][1]},
        'freeze': {'path': PINS['freeze_c2v003a'][0], 'sha256': PINS['freeze_c2v003a'][1]},
        'observation_region': {'path': PINS['observation_region'][0], 'sha256': PINS['observation_region'][1],
                               'row_ids': reg['row_ids']},
        'coordinates': coords,
        'coordinate_order_note': ('freeze format (11 keys). Varying engine order = free coordinates then the DDO154 '
                                  'distance nuisance, as listed. Shared fixed coordinates are held at trial_value in '
                                  'every DDO154 call and are passed to the NGC3198 forward; their boxes are '
                                  'FIXED_PLACEHOLDER_BOX_NEVER_VARIED (they bracket the declared discrete alternatives).'),
        'varying_order': list(es['varying_names']),
        'units': {c['name']: c['units'] for c in coords},
        'ddo154_forward_constants': {
            'inclination_deg': {
                'value': 66.0, 'units': 'deg', 'status': 'COUNTED_ASSUMPTION_FIXED (CA-31)',
                'why_not_a_coordinate': ('prediction_freeze_c2v003a admits DDO154-scoped coordinates only as role '
                                         'nuisance; the inclination is not varied, so it is a constant of the DDO154 '
                                         'call-spec template (physical.inclination_deg = 66.0), asserted on every call.'),
                'evidence': ('driver v003b/v003c normalize_spec refuses inclination != 66 (BLOCKED_GAS_REDEPROJECTION: the '
                             'gas annuli are extracted in the 66 deg plane; INTERFACE_V003B_DELTA.md section 4).'),
                'catalogue_summary': '64 +/- 3 deg (calibration input:1147-1149); the draft box [61, 67] is NOT explored',
                'deciding_work': ('reviewed gas re-extraction stage at i (extract_source.py with inclination_deg = i, '
                                  'profile composition, reducer V002), then derive_geometry; until then UNTESTED.')},
        },
        'call_spec_mapping': {
            'mapping_id': MAPPING_ID,
            'template': {'path': PINS['anchor_spec'][0], 'sha256': PINS['anchor_spec'][1],
                         'schema': anchor_spec['schema']},
            'set_from_theta': {'physical.common_scale_s': 'common_scale_s',
                               'physical.gamma': 'gamma_over_Eref * Eref_base_J',
                               'physical.ell_F_m': 'ell_F_m',
                               'physical.distance_Mpc': 'distance_Mpc'},
            'asserted_equal_to_template': {'physical.Eref_J': 'Eref_base_J',
                                           'physical.entropy_K_factor': 'entropy_K_factor',
                                           'physical.inclination_deg': 'ddo154_forward_constants.inclination_deg'},
            'label': ('"DDO154 calibration orchestrator c2v001 theta <key16>; template <sha8>" (non-physical, '
                      'declared changed field)'),
            'numerics': ('replaced as a whole by the numerics block root supplies after the convergence verdict; '
                         'default = the template (anchor) numerics. Any numerics other than the template\'s disables the '
                         'anchor alias and changes the cache id (no cross-numerics reuse).'),
            'declared_changed_paths': ['label', 'physical.common_scale_s', 'physical.gamma', 'physical.ell_F_m',
                                       'physical.distance_Mpc', 'numerics (only when root supplies non-default numerics)'],
            'bound_not_passed': {
                'ML_3p6, helium_factor, Gamma_poly': ('not driver inputs: embedded in the pinned route-B source '
                                                      'preparation; asserted at their trial values on every call (PC-5: '
                                                      'not exposed by driver v003c)'),
                'native_*': ('not driver inputs: carried by the coefficient pin 2e3a36d8 (A2 pooled grid built from the '
                             'cycle and admission captures); literals verified equal to both provenance trial dicts'),
            },
            'units_note': ('gamma_over_Eref is gamma (seed numerical_inputs.gamma units) per J of Eref_base_J; the driver '
                           'forms Eref_eff = s*Eref_J and gamma_eff = s*gamma, so gamma_eff/Eref_eff = gamma_over_Eref.'),
        },
        'trial_point': {
            'name': 'A2_ANCHOR_F10',
            'statement': 'trial at the factor-10 anchor (seed-scan factor 10, s = 0.10154172268068731)',
            'anchor_spec': {'path': PINS['anchor_spec'][0], 'sha256': PINS['anchor_spec'][1]},
            'anchor_receipt': {'path': PINS['anchor_receipt'][0], 'sha256': PINS['anchor_receipt'][1],
                               'receipt_sha256_self': anchor_rcpt['receipt_sha256']},
            'anchor_result': {'path': PINS['anchor_result'][0], 'sha256': PINS['anchor_result'][1],
                              'status': anchor_res['status'], 'valid': anchor_res['valid'],
                              'driver_sha256': anchor_res['driver_sha256'],
                              'elapsed_seconds': anchor_rcpt['elapsed_seconds'],
                              'peak_rss_bytes': anchor_rcpt['peak_rss_bytes'],
                              'final_output_bytes': anchor_rcpt['final_output_bytes']},
            'anchor_admitted_on_ddo154_rectangles': cls['admitted'],
            'anchor_outside_rows': cls['outside_rows'],
            'reuse': ('the anchor run is reused as the engine seed evaluation (no rerun) through an ANCHOR ALIAS cache '
                      'entry: the engine requests the seed at to_natural(trial_u), which differs from the anchor values '
                      'by log/exp rounding only; the alias is accepted iff every mapped physical field agrees within '
                      'ANCHOR_ALIAS_RTOL, all non-physical fields except label agree exactly, and the numerics in use '
                      'equal the anchor numerics.'),
            'anchor_alias_rtol': ANCHOR_ALIAS_RTOL,
            'engine_trial_u': tu,
            'engine_seed_theta': th,
            'engine_seed_relative_deviation_from_anchor': dev,
            'driver_equivalence_assumption': {
                'id': 'ANCHOR_REUSE_DRIVER_EQUIVALENCE',
                'statement': ('the anchor result was computed by driver c2v001 (75b0c08a); calibration calls use c2v003c '
                              '(ed326130). At the registered geometry (4.04 Mpc, 66 deg) v003b plans, writes and pins '
                              'nothing v003 does not (INTERFACE_V003B_DELTA section 3: t04 dry-run reports identical apart '
                              'from driver_sha256; t05 run-mode requests byte-identical), v003 reproduction plans equal '
                              'v001\'s (INTERFACE_V003_DELTA section 1), and v003c touches no numerics (CHECK_V001 of '
                              'driver_f). The anchor route A converged at iteration 4 (v001 refuses otherwise).'),
                'status': 'COUNTED (plan-level identity; a bitwise rerun of the anchor under v003c is UNTESTED, '
                          'deciding test: one v003c call at the anchor spec, ~1.9 h)'},
        },
        'box_justification': {
            'common_scale_s': {
                'box': [s0 * 0.5, s0 * 2.0], 'transform': 'log', 'centre': 'anchor s',
                'evidence': ('obs/pred v^2 at the evaluated anchor across the 12 DDO154 rows spans [%.4f, %.4f]; a pure '
                             'common rescale (fixed-source response proportional to 1/s) would need s in anchor x '
                             '[%.3f, %.3f], which the x[0.5, 2] box contains with margin. Computational only.'
                             % (min(v2), max(v2), 1.0 / max(v2), 1.0 / min(v2))),
                'factor3_point': ('the factor-3 call (s = %r, gamma_over_Eref = %r) lies OUTSIDE this box along s '
                                  '(s/s_anchor = %.3f). It is recorded as an evaluated invalid point, not used to set '
                                  'any edge.' % (f3_s, f3_ge, f3_s / s0)),
            },
            'gamma_over_Eref': {
                'box': [g_lo, g_hi], 'transform': 'log',
                'edges': 'the factor-1 and factor-100 seed-scan values (both evaluated, both rule-pass); anchor (factor 10) '
                         'sits exactly at the log-centre (ratios 10.0 / 10.0)',
                'evidence': ('A2 seed scan (route-A G2 kernel, rule c2v001): factors 1, 3, 10, 30, 100, 300, 1000 all '
                             'rule-pass (96/96 radial nodes inward, positive two-sided margin at the failure column) along '
                             'the seed curve s(factor); full chain: factor 10 VALID (the anchor), factor 3 INVALID (driver '
                             'c2v001 FAILED, reasons ["KeyError: 70"]: rfs column 70 failed and gave no bracket source; '
                             'c2v003+ reports this as FAILED_AT_STAGE).'),
                'factor3_treatment': ('an EVALUATED INVALID POINT (gamma_over_Eref %r inside this box, at s outside the s '
                                      'box), NOT a box edge by fiat. Invalid evaluations inside the box are expected near '
                                      'it; the engine treats them as non-admitted and the orchestrator flags every side '
                                      'whose first non-admitted evaluation is invalid as VALIDITY_LIMITED (D6).' % f3_ge),
                'scope_caution': ('the scan is a route-A kernel diagnostic along the seed curve (s varies with the factor); '
                                  'the rectangle box pairs every gamma_over_Eref with every s in its box. Full-chain '
                                  'validity off the seed curve is UNTESTED; the engine evaluates it.'),
            },
            'ell_F_m': {
                'box': [ell0 * 0.5, ell0 * 2.0], 'transform': 'log',
                'evidence': ('no ell_F response has been evaluated (UNTESTED; deciding test: BR-A Jacobian column 2). Box '
                             'x[0.5, 2] keeps the sampled primitive covector span between ~1.04 and ~4.16 reciprocal-lattice '
                             'periods per axis at the anchor numerics (72 nodes, cube, kmax 2/kpc; review row 7). D13: '
                             're-derive if root supplies other numerics after the convergence verdict.'),
            },
            'distance_Mpc': {
                'box': [box['lower'], box['upper']], 'transform': 'log',
                'evidence': ('the region file distance_summary reported conditional 68%% interval exactly (modulus 28.03 '
                             '[28.00, 28.07]); ddo154_distance_box with modulus_half_width_multiple 1.0; bound by the '
                             'engine (_check_distance_binding ok). Trial 4.04 Mpc = registered route-B geometry = the '
                             'anchor. Not hard support (%s).' % box['semantics']),
            },
        },
        'evaluated_evidence': {
            'seed_scan': {'path': PINS['seed_scan_result'][0], 'sha256': PINS['seed_scan_result'][1],
                          'candidates': [{'factor': f, 'rule_pass': c['rule_pass'], 'scale_s': c['scale_s'],
                                          'gamma_over_Eref': c['candidate_seed']['gamma_over_Eref'],
                                          'radial_inward': c['radial_inward'],
                                          'failure_column_two_sided_margin': c['failure_column_two_sided_margin']}
                                         for f, c in sorted(cands.items())]},
            'factor3_full_chain': {'result': {'path': PINS['f3_result'][0], 'sha256': PINS['f3_result'][1]},
                                   'receipt': {'path': PINS['f3_receipt'][0], 'sha256': PINS['f3_receipt'][1]},
                                   'status': f3_res['status'], 'valid': f3_res['valid'], 'reasons': f3_res['reasons'],
                                   'elapsed_seconds': f3_rcpt['elapsed_seconds'],
                                   'classification': 'EVALUATED_INVALID_POINT (not a box edge)'},
            'anchor_full_chain': {'result_sha256': PINS['anchor_result'][1], 'status': 'COMPLETED', 'valid': True,
                                  'admitted': cls['admitted'], 'outside_rows': cls['outside_rows']},
        },
        'fixed': {
            'statement': ('fixed = inclination 66 deg (counted, template constant), every native coordinate at the A2 '
                          'point, M/L3.6 0.5, helium 1.36, Gamma 5/3, entropy K factor 64/121, Eref_base_J at the anchor.'),
            'native_provenance': {'cycle': verified['cycle_run_result'], 'admission': verified['admission_run_result'],
                                  'trial_dict': trial_dict, 'beta': beta, 'identical_in_both': True,
                                  'coefficients': verified['a2_coefficients'],
                                  'pc6_status': 'literals verified from bytes here (D20 provenance named); the per-call '
                                                'assertion is done by the orchestrator mapper (fixed coordinates at trial)'},
        },
        'discrete_alternatives': {
            'freeze_alternatives_declaration': {
                'primary': 'BR_A_F10_PRIMARY',
                'declared': [
                    {'name': 'BR_A_F10_PRIMARY', 'kind': 'state',
                     'description': 'route-B BR-A state (K factor 64/121, M/L 0.5, He 1.36, Gamma 5/3) at the A2 factor-10 calibration',
                     'status': 'EVALUATED_BEFORE_FREEZE'},
                    {'name': 'ORIGINAL_K', 'kind': 'state',
                     'description': ('entropy_K_factor 1.0 (binding reference sigma0 11 km/s) instead of 64/121, evaluated '
                                     'on the NGC3198 side at the same selected points (ROOT_DECISIONS_NGC3198 N4); DDO154 '
                                     'admission at K = 1 is not re-established (counted)'),
                     'status': 'EVALUATED_BEFORE_FREEZE'},
                    {'name': 'ML_3p6_0.4', 'kind': 'source',
                     'description': 'stellar M/L3.6 = 0.4 (population-model alternative, binding V003:28)',
                     'status': 'NOT_EVALUATED_BEFORE_FREEZE'},
                    {'name': 'ML_3p6_0.6', 'kind': 'source',
                     'description': 'stellar M/L3.6 = 0.6 (population-model alternative, binding V003:28)',
                     'status': 'NOT_EVALUATED_BEFORE_FREEZE'},
                ]},
            'alternative_notes': {
                'ORIGINAL_K': ('MARKED FOR EVALUATION BEFORE FREEZE: exposed by the driver (physical.entropy_K_factor) and '
                               'by the NGC3198 lane (N4). The freeze writer refuses unless its evaluation on the selected '
                               'points is supplied (D9). If the budget does not allow it, root changes its status to '
                               'NOT_EVALUATED_BEFORE_FREEZE in a recorded decision before step 5; never silently.'),
                'ML_3p6_0.4': 'NOT_EVALUATED_BEFORE_FREEZE: not exposed by driver v003c (PC-5); deciding work: a reviewed driver extension',
                'ML_3p6_0.6': 'NOT_EVALUATED_BEFORE_FREEZE: not exposed by driver v003c (PC-5); deciding work: a reviewed driver extension',
            },
            'not_carried_here': ('helium 1.33, Gamma 1.4, h* 5.1/9.5, photometry variant: draft tier-2 items; not '
                                 'exposed by driver v003c; UNTESTED, listed in untested_with_deciding_tests'),
        },
        'engine_parameters': eng_params,
        'engine_parameter_rationale': {
            'wave_capacity': ('a wave runs at most floor(12 / column_workers) calls at once (campaign: max_concurrent x '
                              'column_workers <= 12). Anchor numerics have column_workers 2: 6 calls per batch, 12 '
                              'single-thread processes. budget 120, design_count 12 and global_design_count 12 are '
                              'multiples of both 6 and 12, so every batch is full whether column_workers is 1 or 2.'),
            'budget': ('120 = 20 batches of 6. Core stages for 4 varying coordinates: seed (alias, 0 calls) + 8 Jacobian '
                       '(+ halvings) + <= 3 repair + <= 2 m %d-call march sides + 24 designs; the remainder goes to the '
                       'iterated rounds. A run that exhausts the budget during the rounds stays COMPLETE with '
                       'budget_exhausted / hull_convergence_not_verified (v002 engine note item 2). Disk: ~6.1 GB per '
                       'call (anchor receipt) -> 120 calls ~730 GB > free disk: the D3 retention rule is a root '
                       'precondition; the orchestrator halts (DISK_GUARD) rather than run out of disk.' % side_bound),
            'max_march_rounds': '2 (root\'s call; the budget, not the rounds, is expected to bind)',
            'hull_growth_tol': ('0.02 >= march_step * 2^-bisection_steps = 0.00625 (v002 engine note: below the bisection '
                                'resolution the rounds chase bisection noise)'),
            'rel_step': 'u-units; 0.05 gives ln steps 0.069 (s), 0.230 (gamma_over_Eref), 0.069 (ell_F), 0.0016 (D)',
            'identification': ('engine S3 rule: identified iff s_i >= max(null_tolerance, 1e-6, eps) * s_max OR s_i >= z = '
                               '2.865 (per unit u). Replaces draft DI-4 (D4: DI-4 cannot be implemented inside '
                               'run_calibration_region); the FD noise floor (PC-7) stays UNTESTED.'),
            'side_bound_calls': side_bound,
        },
        'ngc3198_nuisance_slots': {
            'status': 'TO_BE_DECLARED_BY_THE_NGC3198_LANE_BEFORE_FREEZE',
            'required': ('exactly one ngc3198_nuisance distance slot (units Mpc, reference_value 13.8, sensitivity) and '
                         'one inclination slot (units deg, sensitivity); prediction_freeze_c2v003a D10'),
            'placeholder_for_engine_coordinate_derivation': ngc_placeholder,
            'placeholder_statement': ('PLACEHOLDER VALUES, NOT NGC3198 INFORMATION. They exist only so '
                                      'make_freeze_coordinate_spec can emit engine_coordinates; engine coordinates exclude '
                                      'NGC slots (verified: two different placeholder sets give byte-identical engine '
                                      'coordinates). The real slots replace them at freeze; the orchestrator re-checks that '
                                      'engine_coordinates are unchanged.'),
        },
        'checker_corrections_applied': [
            {'id': 'D1', 'resolution': ('"never pinned" withdrawn. The engine moves only along identified directions; '
                                        'admitted points keep the anchor projection on near-null directions. Entry rule: '
                                        'every near-null direction is displaced to both box ends at the reference member by '
                                        'evaluate_sensitivity (null_direction_rule box_ends, D6) and reported as the '
                                        'BOX_LIMITED sensitivity band; the headline is labelled conditional on the anchor '
                                        'projection along near-null directions. DDO154 admission of the displaced points is '
                                        'not established (counted).')},
            {'id': 'D2', 'resolution': ('driver v003c F1 separates ROUTE_A_NO_FIXED_POINT (model outcome) from BLOCKED '
                                        'ROUTE_A_ITERATION_NOT_4 (still a tooling limit; PC-9 open). Both are cached as '
                                        'INVALID evaluations with the driver status kept as failure_class, never retried; '
                                        'sides they stop are flagged VALIDITY_LIMITED.')},
            {'id': 'D3', 'resolution': ('disk line: ~6.1 GB per call (anchor receipt final_output_bytes 6081118006). The '
                                        'orchestrator never deletes; it halts with DISK_GUARD before a wave whose output cap '
                                        'sum exceeds free disk minus a reserve. The retention rule is a root precondition.')},
            {'id': 'D4', 'resolution': 'replaced by the v003 engine S3 absolute+relative rule (engine_parameter_rationale)'},
            {'id': 'D5', 'resolution': ('every run is recorded (write_calibration_record, P34-16). NO_ADMITTED_POINT_FOUND '
                                        '= REPAIR_FAILED, emptiness UNTESTED (the engine already runs the coarse global '
                                        'design before declaring it). BUDGET_EXHAUSTED -> rerun with a larger budget: the '
                                        'theta-keyed cache replays every evaluated point with zero new calls (cache id '
                                        'excludes the budget and the boxes).')},
            {'id': 'D6', 'resolution': ('the orchestrator summary lists VALIDITY_LIMITED sides (boundary cause '
                                        'INVALID_EVALUATION*) for the freeze notes')},
            {'id': 'D7', 'resolution': ('EDGE_LIMITED: the summary names every coordinate on which an admitted point sits '
                                        'on a box face or a march reached a box edge. Declared widening: rerun with that '
                                        'coordinate\'s log-box doubled about the anchor (distance: modulus half-width '
                                        'multiple 2), both regions reported, cache reused; never silent.')},
            {'id': 'D8', 'resolution': ('tier-2 branches are not carried; alternatives enter the freeze through the '
                                        'freeze module\'s alternatives field (state/source), evaluated on the same points')},
            {'id': 'D9', 'resolution': 'UNTESTED: A2 coefficient sensitivity (per-chain grids) -- listed with deciding test'},
            {'id': 'D10', 'resolution': 'numerics are root\'s after the convergence verdict; route-A truncation counted'},
            {'id': 'D11', 'resolution': 'cost wording: every call reruns the whole chain (~1.9 h); no 1/s shortcut used'},
            {'id': 'D12', 'resolution': ('PC-4 rule replaced: gamma_over_Eref edges are the evaluated factor-1 / factor-100 '
                                         'seed-scan points under A2; no edge moved by fiat')},
            {'id': 'D13', 'resolution': 'ell_F rationale stated for the anchor numerics; re-derive if numerics change'},
            {'id': 'D14', 'resolution': 'CA-25 reworded: natives and b are fixed at one point, not explored'},
            {'id': 'D15', 'resolution': 'wording: no NGC3198 target file read; no NGC3198 value used'},
            {'id': 'D16', 'resolution': 'every input of this spec is verified from bytes by the builder (inputs_pinned)'},
            {'id': 'D17', 'resolution': 'no validation toy in this spec; the orchestrator test labels its toy as synthetic'},
            {'id': 'D18', 'resolution': 's box rationale recomputed from the A2 anchor rows (box_justification)'},
            {'id': 'D19', 'resolution': 'tier-2 coverage not claimed; untested list carries the items'},
            {'id': 'D20', 'resolution': 'native provenance named and verified (fixed.native_provenance)'},
            {'id': 'D21', 'resolution': 'freeze-stage NGC3198 evaluations not budgeted here (NGC lane)'},
        ],
        'preconditions_before_freeze': [
            {'id': 'PC-1', 'status': 'OPEN', 'item': 'P-88 kmax/truncation verdict; root supplies the numerics block'},
            {'id': 'PC-5', 'status': 'PARTIAL', 'item': 'distance exposed (v003b/c); inclination and M/L, He, Gamma not'},
            {'id': 'PC-7', 'status': 'OPEN', 'item': 'FD noise floor (repeat call at the anchor; outside the cache)'},
            {'id': 'PC-9', 'status': 'OPEN', 'item': 'route-A iteration != 4 still BLOCKED (cached invalid, flagged)'},
            {'id': 'D3', 'status': 'OPEN', 'item': 'disk retention rule (root)'},
            {'id': 'NGC-slots', 'status': 'OPEN', 'item': 'NGC3198 distance and inclination slots (NGC lane)'},
            {'id': 'REVIEW', 'status': 'OPEN', 'item': 'independent check of this spec and the orchestrator'},
        ],
        'counted_assumptions': [
            dict(c, statement=('The 11 native ratios and b are fixed at the A2 sampler point (one point, not explored); '
                               '12 observations do not generically identify 15 coordinates.'))
            if c['id'] == 'CA-25' else
            (dict(c, statement=('Box edges for s and gamma_over_Eref are justified from A2-coefficient evidence (factor '
                                'scan, anchor rows); route-A kernel diagnostics along the seed curve do not establish '
                                'full-chain validity off it.')) if c['id'] == 'CA-30' else c)
            for c in draft['counted_assumptions']] + [
            {'id': 'CA-31', 'source': 'driver v003b/v003c; this spec',
             'statement': 'DDO154 inclination fixed at 66 deg (registered gas plane); not explored.'},
            {'id': 'CA-32', 'source': 'this spec trial_point',
             'statement': 'Anchor reuse: the c2v001 anchor result stands for the c2v003c seed evaluation (plan identity).'},
        ],
        'untested_with_deciding_tests': [
            {'claim': 'ell_F response of the 12 rows', 'deciding_test': 'Jacobian column ell_F_m (W1/W2)', 'status': 'UNTESTED'},
            {'claim': 'full-chain validity off the seed curve', 'deciding_test': 'Jacobian and repair calls', 'status': 'UNTESTED'},
            {'claim': 'inclination != 66', 'deciding_test': 'gas re-extraction stage', 'status': 'UNTESTED'},
            {'claim': 'v003c bitwise reproduction of the anchor', 'deciding_test': 'one v003c call at the anchor spec',
             'status': 'UNTESTED'},
            {'claim': 'A2 coefficient sensitivity', 'deciding_test': 'per-chain grids at the reference member', 'status': 'UNTESTED'},
            {'claim': 'M/L, He, Gamma, h*, photometry alternatives', 'deciding_test': 'driver extension (PC-5)', 'status': 'UNTESTED'},
            {'claim': 'converged truncation', 'deciding_test': 'P-88', 'status': 'UNTESTED'},
            {'claim': 'tilt family', 'deciding_test': 'disk axis along each Cbar principal axis and [111]', 'status': 'UNTESTED'},
        ],
        'validation': {
            'freeze_make_freeze_coordinate_spec_ok': fs['ok'],
            'engine_make_coordinate_spec_ok': es['ok'],
            'engine_coordinates_independent_of_ngc_placeholders': True,
            'distance_binding_ok': bind['ok'],
            'n_coordinates': len(coords), 'n_varying': len(es['varying_names']),
            'anchor_alias_max_abs_relative_deviation': max(abs(v) for v in dev.values()),
            'gamma_over_Eref_times_Eref_reproduces_anchor_gamma_bitwise': True,
        },
        'engine_coordinates': eng_coords,
        'inputs_pinned': verified,
        'builder': {'path': os.path.realpath(__file__), 'sha256': sha_file(os.path.realpath(__file__))},
    }
    areasons = []
    if F._bind_alternatives(spec['discrete_alternatives']['freeze_alternatives_declaration'], areasons) is None:
        raise SystemExit('alternatives declaration refused by the freeze module: %s' % areasons)
    spec['validation']['freeze_alternatives_declaration_accepted'] = True
    raw = (json.dumps(spec, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    with open(a.out, 'xb') as fh:
        fh.write(raw)
    print(json.dumps({'out': a.out, 'sha256': hashlib.sha256(raw).hexdigest(), 'n_coordinates': len(coords),
                      'varying': es['varying_names'], 'alias_dev_max': max(abs(v) for v in dev.values()),
                      'anchor_admitted': cls['admitted'], 'outside_rows': cls['outside_rows']}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
