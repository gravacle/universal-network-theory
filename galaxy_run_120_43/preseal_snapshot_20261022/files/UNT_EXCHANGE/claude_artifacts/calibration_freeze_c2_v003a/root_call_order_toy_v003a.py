"""Runnable toy of the v003 root call order (ROOT_CALL_ORDER.md). SYNTHETIC ONLY.

engine -> [record] -> select -> evaluate members -> [reference] -> sensitivity -> write -> register -> verify -> score

Synthetic DDO154-shaped region and a synthetic 43-id query manifest (role SYNTHETIC_FIXTURE) are written into the
run folder; the forwards are toys; the target rows are invented. No NGC3198 file of any kind is opened, no project
forward, no network, single thread. For the real freeze swap in the real region file (13c16a63...), the real
target-free query manifest (a2936517..., role PROGRAM_PIN) and the real forwards; nothing else changes.

usage: python3 -I -B root_call_order_toy.py          (writes only under ./root_call_order_runs/run_<UTC>_<pid>/)
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import datetime
import hashlib
import importlib.util
import json
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
ENG_PATH = os.path.join(HERE, 'calibration_region_engine_c2v003a.py')
FRZ_PATH = os.path.join(HERE, 'prediction_freeze_c2v003a.py')


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


def main():
    E, F = load(ENG_PATH, 'engine_c2v003'), load(FRZ_PATH, 'freeze_c2v003')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = os.path.join(HERE, 'root_call_order_runs', 'run_%s_%d' % (stamp, os.getpid()))
    os.makedirs(run_dir)
    p = lambda name: os.path.join(run_dir, name)   # noqa: E731

    # ---- synthetic inputs (stand-ins for the two pinned program files) --------------------------------------
    rows = ['R%02d' % i for i in range(1, 13)]
    z, sig, mu = 2.865260238532134, 0.7, 28.03
    dc = 10 ** ((mu - 25) / 5)
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
    region_path, qm_path = p('SYNTHETIC_REGION_NOT_DDO154.json'), p('SYNTHETIC_QUERY_MANIFEST_NOT_NGC3198.json')

    coordinates = [
        dict(name='a', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.75, units='dimensionless',
             scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='b', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.80, units='dimensionless',
             scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='q', transform='linear', lower=0.0, upper=2.0, role='fixed', trial_value=1.0, units='kpc',
             scope='shared', kind='other', reference_value=None, sensitivity={'mode': 'box_ends'}),
        dict(name='D_ddo', transform='log', lower=dc * 0.97, upper=dc * 1.03, role='nuisance', trial_value=dc,
             units='Mpc', scope='ddo154_nuisance', kind='distance', reference_value=4.04, sensitivity=None),
        dict(name='D_ngc', transform='log', lower=12.0, upper=15.6, role='nuisance', trial_value=13.8, units='Mpc',
             scope='ngc3198_nuisance', kind='distance', reference_value=13.8, sensitivity={'mode': 'box_ends'}),
        dict(name='i_ngc', transform='linear', lower=65.0, upper=77.0, role='nuisance', trial_value=71.0, units='deg',
             scope='ngc3198_nuisance', kind='inclination', reference_value=None,
             sensitivity={'mode': 'step', 'step': 3.0}),
    ]

    def forward_ddo(theta):      # toy DDO154 forward: admitted disc around (0.85, 0.85)
        g = 40.0 * ((theta['a'] - 0.85) ** 2 + (theta['b'] - 0.85) ** 2)
        return {'speeds_km_s': {r: 100.0 + g for r in rows}, 'valid': True, 'reasons': []}

    def forward_ngc(theta):      # toy NGC3198 forward: receives shared + NGC3198 slots only (D10)
        assert 'D_ddo' not in theta
        return {'speeds_km_s': {q: 150.0 + 20.0 * (theta['a'] + theta['b']) + 40.0 * (theta['a'] - theta['b']) *
                                (j + 1) / 43.0 + 3.0 * (theta['q'] - 1.0) + 10.0 * (theta['D_ngc'] / 13.8 - 1.0) +
                                0.2 * (theta['i_ngc'] - 71.0) for j, q in enumerate(qids)},
                'valid': True, 'reasons': []}

    # 0. coordinate spec (D10; D4 engine-ready dicts)
    fs = need('make_freeze_coordinate_spec', F.make_freeze_coordinate_spec(coordinates=coordinates))
    # 1. engine (DDO154 calibration region)
    run = E.run_calibration_region(
        forward=forward_ddo, coordinates=fs['engine_coordinates'], observation_region_path=region_path,
        observation_region_sha256=sha(region_path), u_seed=None, budget=600, rel_step=0.05, min_step=1e-4,
        max_halvings=3, null_tolerance=1e-6, repair_iterations=8, max_repair_step=0.25, march_step=0.05,
        bisection_steps=4, design_count=8, global_design_count=24, max_march_rounds=4, hull_growth_tol=0.01,
        ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0}, rng_seed=0)
    # 1b. P34-16: record EVERY run (also a failed one) before deciding anything
    rec = need('write_calibration_record', E.write_calibration_record(
        run=run, record_path=p('CALIBRATION_RECORD.json'), registry_path=p('CALIBRATION_REGISTRY.jsonl')))
    if run['status'] != 'COMPLETE':
        raise SystemExit('engine status %s: recorded, no freeze' % run['status'])
    # 2. select (pass the run output itself: P34-14 re-verification + region binding)
    sel = need('select_representative_points',
               F.select_representative_points(exploration=run, interior_count=6, spec=fs['spec']))
    # 3. evaluate members (every selected point, D2)
    ev = need('evaluate_envelopes', F.evaluate_envelopes(forward_ngc=forward_ngc, points=sel['points'],
                                                         spec=fs['spec'], query_ids=qids, budget=100))
    ref = need('select_reference_member', F.select_reference_member(selection=sel, evaluation=ev))
    # 4. sensitivity (D6)
    sens = need('evaluate_sensitivity', F.evaluate_sensitivity(
        forward_ngc=forward_ngc, reference=ref, selection=sel, spec=fs['spec'], query_ids=qids,
        null_direction_rule={'mode': 'box_ends'}, budget=100))
    # 5. write (manifest + registration file)
    w = need('write_freeze_manifest', F.write_freeze_manifest(
        out_path=p('FREEZE_MANIFEST.json'), registration_path=p('FREEZE_REGISTRATION.json'),
        parameter_region={'description': 'toy computational trial box',
                          'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'},
        observation_rule={'rule': 'closed Bonferroni rectangle (synthetic stand-in)'}, spec=fs['spec'], selection=sel,
        alternatives={'primary': 'TOY_STATE', 'declared': [{'name': 'TOY_STATE', 'kind': 'state',
                                                            'description': 'toy primary',
                                                            'status': 'EVALUATED_BEFORE_FREEZE'}]},
        alternative_evaluations={'TOY_STATE': ev}, reference=ref, sensitivity=sens, query_ids=qids,
        query_manifest={'path': qm_path, 'sha256': sha(qm_path), 'role': 'SYNTHETIC_FIXTURE'},
        code_files=[FRZ_PATH, ENG_PATH], input_files=[region_path, qm_path, p('CALIBRATION_RECORD.json')],
        notes={'toy': True}, allow_incomplete=False))
    # 6. register: log the hashes externally BEFORE any target access (stand-in for the FROM_ message)
    line = {'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'manifest_file_sha256': w['manifest_file_sha256'], 'registration_file_sha256': w['registration_file_sha256'],
            'calibration_record_file_sha256': rec['record_file_sha256'], 'targets_opened': False}
    with open(p('EXTERNAL_REGISTRATION_LOG.jsonl'), 'x') as fh:
        fh.write(json.dumps(line, sort_keys=True) + '\n')
    # 7. verify
    vf = need('verify_freeze_manifest', F.verify_freeze_manifest(freeze_manifest_path=w['path']))
    vr = need('verify_registration', F.verify_registration(registration_path=w['registration_path']))
    vc = need('verify_calibration_record', E.verify_calibration_record(record_path=rec['record_path'],
                                                                      registry_path=rec['registry_path']))
    # 8. score (targets are opened only now; the expected sha comes from the external log, not the registration file)
    logged = json.loads(open(p('EXTERNAL_REGISTRATION_LOG.jsonl')).read().splitlines()[0])
    targets = [{'id': q, 'velocity': 150.0 + 34.0 + 0.1 * j, 'sigma': 2.0} for j, q in enumerate(qids)]   # invented
    sc = need('score_after_freeze', F.score_after_freeze(
        freeze_manifest_path=w['path'], registration_path=w['registration_path'],
        expected_manifest_file_sha256=logged['manifest_file_sha256'], target_rows=targets))
    summary = {'run_dir': run_dir, 'engine_status': run['status'], 'n_admitted': run['exploration']['n_admitted'],
               'truncation_causes': run['truncation_causes'], 'n_members': len(sel['points']),
               'freeze_status': w['freeze_status'], 'manifest_file_sha256': w['manifest_file_sha256'],
               'registration_file_sha256': w['registration_file_sha256'],
               'calibration_record_file_sha256': rec['record_file_sha256'],
               'calibration_record_bound': w['calibration_record_bound'], 'verify_ok': vf['ok'], 'registration_ok': vr['ok'],
               'record_chain_ok': vc['registry_chain_ok'],
               'headline': {k: sc['headline'][k] for k in ('member_within_error_counts', 'reference_member_id',
                                                           'reference_within_error_count', 'n_members_invalid',
                                                           'query_manifest_role', 'region_possibly_truncated')},
               'echo': {k: sc[k] for k in ('manifest_file_sha256_expected', 'manifest_file_sha256_actual',
                                           'manifest_sha256_self', 'registration_file_sha256', 'target_rows_sha256')}}
    with open(p('TOY_SUMMARY.json'), 'x') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
