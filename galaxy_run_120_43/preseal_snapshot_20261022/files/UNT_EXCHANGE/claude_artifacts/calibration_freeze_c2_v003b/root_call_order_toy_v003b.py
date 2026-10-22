"""Runnable toy of the root call order with prediction_freeze_c2v003b, in both coordinate modes. SYNTHETIC ONLY.

  --mode 4D  the v003a toy verbatim (DDO154 distance a nuisance; root_call_order_toy_v003a.py inputs, forwards and
             notes), run on v003b: the 4-coordinate behaviour.
  --mode 3D  A13: DDO154_DISTANCE_FIXED_AT_REGISTERED. Step 0 converts the coordinate list with apply_coordinate_mode
             (the DDO154 distance becomes a fixed counted constant at 4.04 Mpc; 2 free coordinates here). The NGC3198
             slots are the adopted slots V002 (ngc_freeze_inputs_c3, 4c5951cb, read only, sha checked); the toy
             forward_ngc refuses every geometry other than the registered 13.8 Mpc / 72 deg with GEOMETRY_NOT_EXPOSED
             (A16.4); the notes are the slots V002 notes_block_for_manifest (A16.1 slot block, SA-BH-01, SA-REACH-01)
             plus an A18 entry.

engine -> [record] -> select -> evaluate members -> [reference] -> sensitivity -> write -> register -> verify -> score

The synthetic DDO154-shaped region and a synthetic 43-id query manifest (role SYNTHETIC_FIXTURE) are written into the
run folder; the forwards are toys; the target rows are invented. The only real files opened are the slots V002 file
(target-free) and, read-only, the two modules. No NGC3198 velocity, no project forward, no network, single thread.

usage: python3 -I -B root_call_order_toy_v003b.py --mode 4D|3D   (writes only under ./root_call_order_runs/)
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import copy
import datetime
import hashlib
import importlib.util
import json
import math
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
ENG_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_freeze_c2_v003a/calibration_region_engine_c2v003a.py'
ENG_SHA = '193841fa1f1d078f7fc981fdba78cf3d736b50ee17e019f0cf94aae94e3a63a6'
FRZ_PATH = os.path.join(HERE, 'prediction_freeze_c2v003b.py')
SLOTS_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_freeze_inputs_c3/NGC3198_FREEZE_SLOTS_C3V002.json'
SLOTS_SHA = '4c5951cbef9aa2c1cf7e7e4c859b59a7aafb5476bd7e59c20caef769376f6c7e'
A18_NOTE = {
    'section': 'A18',
    'text_verbatim': ("A2's in-plane anisotropy is a counted coefficient-estimation limitation. It enters the freeze "
                      "manifest notes next to SA-REACH-01. Route B's m=0 projection averages it to first order."),
    'source': {'file_name': 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md', 'section': 'A18',
               'status': 'OPEN_CITED_BY_NAME_NOT_PINNED'},
    'deciding_tests': ('static x<->y invariance check of the born graph, initial configuration and move set; one chain '
                       'started rotated 90 deg about z (sampler lineage)'),
}


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def need(step, res):
    if not res.get('ok'):
        raise SystemExit('%s refused: %s' % (step, res.get('reasons', [])[:4]))
    return res


def toy_inputs(run_dir, mode):
    """Synthetic region + query manifest + coordinates + forwards + notes for one mode (no I/O outside run_dir except
    the read-only slots file in 3D)."""
    p = lambda name: os.path.join(run_dir, name)   # noqa: E731
    rows = ['R%02d' % i for i in range(1, 13)]
    z, sig = 2.865260238532134, 0.7
    if mode == '4D':
        mu = 28.03                                   # the v003a toy verbatim
        dc = 10 ** ((mu - 25) / 5)
    else:
        dc = 4.04                                    # A13: the registered distance is the central value
        mu = 25.0 + 5.0 * math.log10(dc)
    with open(p('SYNTHETIC_REGION_NOT_DDO154.json'), 'x') as fh:
        json.dump({'rows': [{'id': r, 'reference_radius_kpc': 0.5 * (i + 1), 'observed_speed_km_s': 100.0,
                             'quoted_random_sigma_km_s': sig,
                             'conditional_random_acceptance_low_km_s': 100.0 - z * sig,
                             'conditional_random_acceptance_high_km_s': 100.0 + z * sig} for i, r in enumerate(rows)],
                   'statistical_choice': 'synthetic', 'forward_coordinates': 'synthetic',
                   'distance_summary': {'modulus_mag': mu, 'distance_central_Mpc': dc, 'reported68_low_Mpc': dc * 0.97,
                                        'reported68_high_Mpc': dc * 1.03, 'scope': 'synthetic'}}, fh)
    qids = ['TOY-Q%02d' % k for k in range(1, 44)]
    with open(p('SYNTHETIC_QUERY_MANIFEST_NOT_NGC3198.json'), 'x') as fh:
        json.dump({'rows': [{'query_id': q, 'data_row_index': j + 1, 'Rad_text': '%.2f' % (0.7 * (j + 1)),
                             'Rad_unit': 'kpc'} for j, q in enumerate(qids)]}, fh)
    shared = [
        dict(name='a', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.75, units='dimensionless',
             scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='b', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.80, units='dimensionless',
             scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='q', transform='linear', lower=0.0, upper=2.0, role='fixed', trial_value=1.0, units='kpc',
             scope='shared', kind='other', reference_value=None, sensitivity={'mode': 'box_ends'}),
        dict(name='D_ddo', transform='log', lower=dc * 0.97, upper=dc * 1.03, role='nuisance', trial_value=dc,
             units='Mpc', scope='ddo154_nuisance', kind='distance', reference_value=4.04, sensitivity=None),
    ]
    out = {'rows': rows, 'qids': qids, 'region_path': p('SYNTHETIC_REGION_NOT_DDO154.json'),
           'qm_path': p('SYNTHETIC_QUERY_MANIFEST_NOT_NGC3198.json')}
    if mode == '4D':
        ngc = [dict(name='D_ngc', transform='log', lower=12.0, upper=15.6, role='nuisance', trial_value=13.8,
                    units='Mpc', scope='ngc3198_nuisance', kind='distance', reference_value=13.8,
                    sensitivity={'mode': 'box_ends'}),
               dict(name='i_ngc', transform='linear', lower=65.0, upper=77.0, role='nuisance', trial_value=71.0,
                    units='deg', scope='ngc3198_nuisance', kind='inclination', reference_value=None,
                    sensitivity={'mode': 'step', 'step': 3.0})]
        dn, inc, d0, i0 = 'D_ngc', 'i_ngc', 13.8, 71.0
        notes = {'toy': True}
    else:
        if sha(SLOTS_PATH) != SLOTS_SHA:
            raise SystemExit('slots V002 bytes differ from %s' % SLOTS_SHA)
        slots = json.load(open(SLOTS_PATH))
        ngc = copy.deepcopy(slots['ngc3198_slots'])
        dn, inc, d0, i0 = 'ngc3198_distance_Mpc', 'ngc3198_inclination_deg', 13.8, 72.0
        notes = copy.deepcopy(slots['notes_block_for_manifest'])
        notes['structural_assumptions']['A18-CBAR-INPLANE-ANISOTROPY'] = copy.deepcopy(A18_NOTE)
        notes['slots_source'] = {'path': SLOTS_PATH, 'sha256': SLOTS_SHA}
        notes['synthetic_toy'] = True
    out.update(coordinates=shared + ngc, notes=notes, ngc_names=(dn, inc))

    def forward_ddo(theta):      # toy DDO154 forward: admitted disc around (0.85, 0.85)
        g = 40.0 * ((theta['a'] - 0.85) ** 2 + (theta['b'] - 0.85) ** 2)
        return {'speeds_km_s': {r: 100.0 + g for r in rows}, 'valid': True, 'reasons': []}

    def forward_ngc(theta):      # toy NGC3198 forward: receives shared + NGC3198 slots only (D10)
        assert 'D_ddo' not in theta, 'DDO154 distance leaked into forward_ngc'
        if mode == '3D' and (theta[dn] != d0 or theta[inc] != i0):    # A16.4
            return {'valid': False, 'speeds_km_s': {},
                    'reasons': ['GEOMETRY_NOT_EXPOSED: toy forward evaluates only D=%r Mpc, i=%r deg' % (d0, i0)]}
        return {'speeds_km_s': {q: 150.0 + 20.0 * (theta['a'] + theta['b']) + 40.0 * (theta['a'] - theta['b']) *
                                (j + 1) / 43.0 + 3.0 * (theta['q'] - 1.0) + 10.0 * (theta[dn] / 13.8 - 1.0) +
                                0.2 * (theta[inc] - i0) for j, q in enumerate(qids)},
                'valid': True, 'reasons': []}
    out.update(forward_ddo=forward_ddo, forward_ngc=forward_ngc)
    return out


def run_chain(E, F, T, run_dir, mode, frz_path):
    """The documented call order; returns a dict of every intermediate output."""
    p = lambda name: os.path.join(run_dir, name)   # noqa: E731
    coords = T['coordinates']
    res = {}
    if mode == '3D':
        # 0a. A13: convert the V001-form list under the declared coordinate mode
        cm = {'mode': 'DDO154_DISTANCE_FIXED_AT_REGISTERED', 'free_coordinates': ['a', 'b'],
              'fixed_engine_coordinates': {'D_ddo': 4.04}}
        am = need('apply_coordinate_mode', F.apply_coordinate_mode(coordinates=coords, coordinate_mode=cm))
        coords = am['coordinates']
        res['apply_coordinate_mode'] = am
    # 0. coordinate spec (D10; D4 engine-ready dicts)
    fs = need('make_freeze_coordinate_spec', F.make_freeze_coordinate_spec(coordinates=coords))
    res['fs'] = fs
    # 1. engine (DDO154 calibration region)
    run = E.run_calibration_region(
        forward=T['forward_ddo'], coordinates=fs['engine_coordinates'], observation_region_path=T['region_path'],
        observation_region_sha256=sha(T['region_path']), u_seed=None, budget=600, rel_step=0.05, min_step=1e-4,
        max_halvings=3, null_tolerance=1e-6, repair_iterations=8, max_repair_step=0.25, march_step=0.05,
        bisection_steps=4, design_count=8, global_design_count=24, max_march_rounds=4, hull_growth_tol=0.01,
        ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0}, rng_seed=0)
    res['run'] = run
    # 1b. P34-16: record EVERY run (also a failed one) before deciding anything
    rec = need('write_calibration_record', E.write_calibration_record(
        run=run, record_path=p('CALIBRATION_RECORD.json'), registry_path=p('CALIBRATION_REGISTRY.jsonl')))
    res['rec'] = rec
    if run['status'] != 'COMPLETE':
        raise SystemExit('engine status %s: recorded, no freeze' % run['status'])
    res.update(freeze_chain(F, T, run_dir, fs, run, rec, frz_path))
    return res


def freeze_chain(F, T, out_dir, fs, run, rec, frz_path, notes=None, forward_ngc=None, alternatives=None):
    """Steps 2-8 (select ... score) in out_dir."""
    p = lambda name: os.path.join(out_dir, name)   # noqa: E731
    fwd = forward_ngc or T['forward_ngc']
    qids = T['qids']
    res = {}
    # 2. select (pass the run output itself: P34-14 re-verification + region binding)
    sel = need('select_representative_points',
               F.select_representative_points(exploration=run, interior_count=6, spec=fs['spec']))
    # 3. evaluate members (every selected point, D2)
    ev = need('evaluate_envelopes', F.evaluate_envelopes(forward_ngc=fwd, points=sel['points'],
                                                         spec=fs['spec'], query_ids=qids, budget=100))
    ref = need('select_reference_member', F.select_reference_member(selection=sel, evaluation=ev))
    # 4. sensitivity (D6)
    sens = need('evaluate_sensitivity', F.evaluate_sensitivity(
        forward_ngc=fwd, reference=ref, selection=sel, spec=fs['spec'], query_ids=qids,
        null_direction_rule={'mode': 'box_ends'}, budget=100))
    res.update(sel=sel, ev=ev, ref=ref, sens=sens)
    # 5. write (manifest + registration file)
    w = F.write_freeze_manifest(
        out_path=p('FREEZE_MANIFEST.json'), registration_path=p('FREEZE_REGISTRATION.json'),
        parameter_region={'description': 'toy computational trial box',
                          'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'},
        observation_rule={'rule': 'closed Bonferroni rectangle (synthetic stand-in)'}, spec=fs['spec'], selection=sel,
        alternatives=alternatives or {'primary': 'TOY_STATE', 'declared': [{'name': 'TOY_STATE', 'kind': 'state',
                                                                           'description': 'toy primary',
                                                                           'status': 'EVALUATED_BEFORE_FREEZE'}]},
        alternative_evaluations={'TOY_STATE': ev}, reference=ref, sensitivity=sens, query_ids=qids,
        query_manifest={'path': T['qm_path'], 'sha256': sha(T['qm_path']), 'role': 'SYNTHETIC_FIXTURE'},
        code_files=[frz_path, ENG_PATH], input_files=[T['region_path'], T['qm_path'], rec['record_path']],
        notes=T['notes'] if notes is None else notes, allow_incomplete=False)
    res['w'] = w
    if not w.get('ok'):
        return res
    # 6. register: log the hashes externally BEFORE any target access (stand-in for the FROM_ message)
    line = {'utc': F._now_utc(), 'manifest_file_sha256': w['manifest_file_sha256'],
            'registration_file_sha256': w['registration_file_sha256'],
            'calibration_record_file_sha256': rec['record_file_sha256'], 'targets_opened': False}
    with open(p('EXTERNAL_REGISTRATION_LOG.jsonl'), 'x') as fh:
        fh.write(json.dumps(line, sort_keys=True) + '\n')
    # 7. verify
    res['vf'] = F.verify_freeze_manifest(freeze_manifest_path=w['path'])
    res['vr'] = F.verify_registration(registration_path=w['registration_path'])
    # 8. score (targets are opened only now; the expected sha comes from the external log, not the registration file)
    logged = json.loads(open(p('EXTERNAL_REGISTRATION_LOG.jsonl')).read().splitlines()[0])
    targets = [{'id': q, 'velocity': 150.0 + 34.0 + 0.1 * j, 'sigma': 2.0} for j, q in enumerate(qids)]   # invented
    res['sc'] = F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=w['registration_path'],
                                     expected_manifest_file_sha256=logged['manifest_file_sha256'], target_rows=targets)
    return res


def main():
    mode = sys.argv[sys.argv.index('--mode') + 1] if '--mode' in sys.argv else None
    if mode not in ('4D', '3D'):
        raise SystemExit('usage: root_call_order_toy_v003b.py --mode 4D|3D')
    if sha(ENG_PATH) != ENG_SHA:
        raise SystemExit('engine bytes differ from %s' % ENG_SHA)
    E, F = load(ENG_PATH, 'engine_c2v003a_toyb'), load(FRZ_PATH, 'freeze_c2v003b_toy')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = os.path.join(HERE, 'root_call_order_runs', 'run_%s_%s_%d' % (mode, stamp, os.getpid()))
    os.makedirs(run_dir)
    T = toy_inputs(run_dir, mode)
    r = run_chain(E, F, T, run_dir, mode, FRZ_PATH)
    for k in ('w', 'vf', 'vr', 'sc'):
        need(k, r[k])
    doc = json.load(open(r['w']['path']))
    sc = r['sc']
    summary = {'run_dir': run_dir, 'mode': mode, 'freeze_sha256': sha(FRZ_PATH), 'engine_sha256': sha(ENG_PATH),
               'engine_status': r['run']['status'], 'n_admitted': r['run']['exploration']['n_admitted'],
               'varying_engine': r['sel']['admitted_region']['varying_engine_names'],
               'n_members': len(r['sel']['points']), 'freeze_status': r['w']['freeze_status'],
               'manifest_file_sha256': r['w']['manifest_file_sha256'],
               'registration_file_sha256': r['w']['registration_file_sha256'],
               'calibration_record_file_sha256': r['rec']['record_file_sha256'],
               'calibration_record_bound': r['w']['calibration_record_bound'], 'verify_ok': r['vf']['ok'],
               'registration_ok': r['vr']['ok'],
               'coordinate_mode': r['fs'].get('coordinate_mode'),
               'headline_conditions_present': 'headline_conditions' in doc,
               'envelope_label': doc['pointwise_envelope'][0]['label'], 'sensitivity_label': doc['sensitivity']['label'],
               'band_scope_headline': doc['band_scope']['headline'],
               'box_limited_rows_valid': sum(1 for x in doc['sensitivity']['per_query'] if x['valid']),
               'scored_alternatives': [(a['name'], a['status'], a['scored']) for a in sc['alternatives']],
               'headline': {k: sc['headline'][k] for k in ('member_within_error_counts', 'reference_member_id',
                                                           'reference_within_error_count', 'n_members_invalid',
                                                           'query_manifest_role', 'region_possibly_truncated')}}
    if mode == '3D':
        hc = doc['headline_conditions']
        summary['headline_conditions'] = {k: hc[k] for k in ('coordinate_mode', 'free_engine_coordinates',
                                                             'band_condition', 'structural_assumptions_present')}
        summary['fixed_counted_constants'] = hc['fixed_counted_constants']
        summary['ngc3198_slot_box_sensitivity'] = {k: hc['ngc3198_slot_box_sensitivity'][k] for k in (
            'status', 'box_end_entries', 'n_refused_geometry_not_exposed', 'box_limited_band_rows_invalid',
            'box_limited_band_rows_total')}
        summary['apply_coordinate_mode_changed'] = r['apply_coordinate_mode']['changed']
    with open(os.path.join(run_dir, 'TOY_SUMMARY.json'), 'x') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
