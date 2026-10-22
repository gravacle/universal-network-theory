"""SYNTHETIC ONLY: v010-shaped freeze/score readiness, no scientific forward.

Execute with the pinned runtime -I -B. A run writes exclusively into a new directory.
The only external data read is the target-free adopted NGC slot declaration.
Raw result metadata is synthetic, not a certificate or production result.
"""
import os
for _key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_key] = '1'
import copy
import datetime
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import types

HERE = Path(__file__).resolve().parent
ART = HERE.parent
BASE = ART / 'calibration_engine_freeze_v003b_v003d'
ENGINE = BASE / 'calibration_region_engine_c2v003b.py'
ORIGINAL = BASE / 'prediction_freeze_c2v003d.py'
SUCCESSOR = HERE / 'prediction_freeze_v010_boundary_cx3v001.py'
TOY = BASE / 'root_call_order/root_call_order_toy_v003d.py'
SLOTS = ART / 'ngc_freeze_inputs_c3/NGC3198_FREEZE_SLOTS_C3V002.json'
DRIVER = ART / 'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
ALLOWED_EXTERNAL = {str(p.resolve()) for p in (ENGINE, ORIGINAL, TOY, SLOTS, DRIVER)}
READS = set()
DENIED = []


def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.spawn', 'os.posix_spawn',
                 'os.fork', 'os.forkpty') or event.startswith('socket.'):
        DENIED.append(event)
        raise PermissionError('no processes or network')
    if event in ('os.remove', 'os.unlink', 'os.rename', 'os.replace', 'os.rmdir'):
        DENIED.append(event)
        raise PermissionError('immutable output policy')
    if event == 'open' and not isinstance(args[0], int):
        p = str(Path(os.fsdecode(args[0])).resolve())
        mode, flags = args[1], args[2]
        write = isinstance(mode, str) and any(c in mode for c in 'wax+') or isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        inside = p == str(HERE) or p.startswith(str(HERE) + os.sep)
        if write:
            if not inside or not isinstance(flags, int) or not (flags & os.O_EXCL or flags & os.O_CREAT and not os.path.lexists(p)):
                DENIED.append(['write', p])
                raise PermissionError('all writes require exclusive create in lane')
        elif inside or p in ALLOWED_EXTERNAL or 'site-packages/numpy/' in p or p.startswith(sys.base_prefix + '/'):
            READS.add(p)
        else:
            DENIED.append(['read', p])
            raise PermissionError('read outside exact input allowlist')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def write(path, obj):
    with Path(path).open('xb') as f:
        f.write(canonical(obj))


def load(path, name):
    raw = Path(path).read_bytes()
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    sys.modules[name] = mod
    exec(compile(raw, str(path), 'exec'), mod.__dict__)
    return mod


def expect(name, condition, evidence=None):
    tests.append({'name': name, 'passed': bool(condition), 'evidence': evidence})
    if not condition:
        raise AssertionError(name + ': ' + repr(evidence))


def stub_hash(label):
    return hashlib.sha256(('SYNTHETIC_FIXTURE:' + label).encode()).hexdigest()


def make_result(speeds, rule='continuum_v001', fired=False):
    """Source-derived field layout, with entirely synthetic contents and metadata.

    Current driver cannot produce NGC tail route B; this models a future result boundary.
    nodes_v001 is an interface branch only, not the adopted NGC source rule.
    """
    config_hash = stub_hash(rule + '_config')
    config = {'path': 'SYNTHETIC_CONFIG_NOT_A_REAL_CERTIFICATE.json', 'sha256': config_hash,
              'written': True, 'normalized_sha256': config_hash}
    ro = {'rule': 'RO1', 'armed': True, 'fired': fired, 'events': [],
          'worker_sha256': stub_hash('worker'), 'binding_sha256': stub_hash('binding')}
    if fired:
        ro['events'] = [{'code': 'ROUTE_A_READOUT_NO_CIRCULAR_BRANCH',
                         'refusal': 'NO_SUBLUMINAL_CIRCULAR_PRESSURE_BRANCH',
                         'after_convergence': True, 'query_id': qids[0]}]
    stages = [{'stage': 'synthetic_' + k, 'kind': k, 'finish_sha256': stub_hash(k + 'finish'),
               'state_digest': stub_hash(k + 'state'), 'empty': False,
               'production_admissible': True, 'test_only_admitted': False,
               'i1t_verdict': 'PASS', 'srb_rot': None}
              for k in ('route_a_tail_manifest', 'reference', 'body', 'offset',
                        'columns_v001', 'rotation_v001', 'columns_v005', 'rotation_v005')]
    return {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'galaxy': 'NGC3198',
            'driver_sha256': driver_sha, 'call_spec_sha256': stub_hash('spec:' + rule),
            'accepted_for_calibration': False, 'scored': False, 'valid': True,
            'status': 'COMPLETED', 'reasons': [], 'synthetic_fixture': True,
            'rows': [{'id': q, 'speed_km_s': speeds[q], 'valid': True, 'reason': None} for q in qids],
            'speeds_km_s': speeds, 'invalid_rows': [],
            'route_a_outcome': {'classification': 'CONVERGED', 'converged_finite_fixed_point': True,
                                'outcome': 'CONVERGED_FINITE_FIXED_POINT', 'ro1': ro},
            'uv_tail': {'schema': 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010', 'enabled': True,
                        'config': config, 'source_rule': rule,
                        'nodes_ext_context': {'n_ext_nodes': 123, 'synthetic_fixture': True} if rule == 'nodes_v001' else None,
                        'admissibility': 'production', 'pending_certificates': [],
                        'certificates': {k: ['SYNTHETIC_NOT_A_CERTIFICATE', stub_hash(k)] for k in ('eps_certificate', 'lo_certificate')},
                        'K_inverse_kpc': 2.0, 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 16.0},
                        'kept_regions': {'route_a': {'kept': {'shape': 'cube', 'K_inverse_kpc': 2.0}, 'domain_empty': False}},
                        'domain_empty_all_stages': False, 'stage_records': stages}}


def forward(rule, directory, delta=0.0, fired=False):
    saved = []
    def f(theta):
        x = T['forward_ngc'](theta)
        if not x['valid']:
            return x
        obj = make_result({q: v + delta for q, v in x['speeds_km_s'].items()}, rule, fired)
        path = directory / ('RAW_%03d.json' % len(saved))
        write(path, obj)
        saved.append(path)
        return obj
    return f, saved


def writer_args(F, folder, fs, sel, evs, ref, sens, raw_paths):
    notes = copy.deepcopy(T['notes'])
    notes['readiness_scope'] = 'SYNTHETIC_ONLY; metadata populated for schema tests, not real scientific certificates'
    notes['raw_result_custody'] = [{'path': str(p), 'sha256': sha(p)} for p in raw_paths]
    return dict(out_path=str(folder / 'FREEZE_MANIFEST.json'), registration_path=str(folder / 'FREEZE_REGISTRATION.json'),
                parameter_region={'description': 'synthetic computational trial box',
                                  'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'},
                observation_rule={'rule': 'synthetic closed rectangle'}, spec=fs['spec'], selection=sel,
                alternatives=copy.deepcopy(slots['alternatives']), alternative_evaluations=evs,
                reference=ref, sensitivity=sens, query_ids=qids,
                query_manifest={'path': T['qm_path'], 'sha256': sha(T['qm_path']), 'role': 'SYNTHETIC_FIXTURE'},
                code_files=[F.__file__, str(ENGINE), str(Path(__file__).resolve())],
                input_files=[T['region_path'], T['qm_path'], rec['record_path'], str(SLOTS)] + [str(p) for p in raw_paths],
                notes=notes, allow_incomplete=False)


def pipeline(F, label, rule):
    folder = RUN / label
    folder.mkdir()
    rawdir = folder / 'raw'
    rawdir.mkdir()
    fwd, raw_paths = forward(rule, rawdir, fired=rule == 'nodes_v001')
    alt_dir = folder / 'raw_alternative'
    alt_dir.mkdir()
    alt_fwd, alt_paths = forward(rule, alt_dir, delta=7.0)
    ev = F.evaluate_envelopes(forward_ngc=fwd, points=sel['points'], spec=fs['spec'], query_ids=qids, budget=100)
    alt_ev = F.evaluate_envelopes(forward_ngc=alt_fwd, points=sel['points'], spec=fs['spec'], query_ids=qids, budget=100)
    ref = F.select_reference_member(selection=sel, evaluation=ev)
    sens = F.evaluate_sensitivity(forward_ngc=fwd, reference=ref, selection=sel, spec=fs['spec'], query_ids=qids,
                                  null_direction_rule={'mode': 'box_ends'}, budget=100)
    args = writer_args(F, folder, fs, sel, {'BR_A_F10_PRIMARY': ev, 'ORIGINAL_K': alt_ev}, ref, sens, raw_paths + alt_paths)
    w = F.write_freeze_manifest(**args)
    expect(label + ':freeze_complete', w.get('ok') and w.get('freeze_status') == 'FREEZE_COMPLETE', w.get('reasons'))
    logged = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'manifest_file_sha256': w['manifest_file_sha256'], 'registration_file_sha256': w['registration_file_sha256'],
              'calibration_record_file_sha256': rec['record_file_sha256'],
              'observation_region_sha256': T['region_sha_logged'], 'targets_opened': False}
    write(folder / 'PRE_TARGET_REGISTRATION.json', logged)
    vf = F.verify_freeze_manifest(freeze_manifest_path=w['path'])
    vr = F.verify_registration(registration_path=w['registration_path'])
    sf3 = toy.sf3_step7(E, vf, w['path'], rec, logged)
    pre8 = toy.sf3_step8(w['path'], logged)
    expect(label + ':verify_and_sf3_before_target', vf['ok'] and vr['ok'] and sf3['ok'] and pre8['ok'])
    # Created and opened only after the external-log analogue and all pre-target checks.
    targets = [{'id': q, 'velocity': 184.0 + 0.1 * j, 'sigma': 2.0} for j, q in enumerate(qids)]
    target_path = folder / 'SYNTHETIC_TARGET_ROWS.json'
    write(target_path, targets)
    targets = json.loads(target_path.read_bytes())
    sc = F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=w['registration_path'],
                             expected_manifest_file_sha256=logged['manifest_file_sha256'], target_rows=targets)
    expect(label + ':score', sc['ok'], sc.get('reasons'))
    write(folder / 'LADDER_SCORE_SYNTHETIC.json', sc)
    doc = json.loads(Path(w['path']).read_bytes())
    expect(label + ':43_predictions_per_member', doc['query_ids'] == qids and all(len(m['speeds_km_s']) == 43 for m in doc['members']))
    env = doc['pointwise_envelope']
    expect(label + ':envelope_independent_oracle', all(row['band_low_km_s'] == min(m['speeds_km_s'][j] for m in doc['members']) and row['band_high_km_s'] == max(m['speeds_km_s'][j] for m in doc['members']) for j, row in enumerate(env)))
    expect(label + ':a16_not_fake_zero_sensitivity', doc['headline_conditions']['ngc3198_slot_box_sensitivity']['n_refused_geometry_not_exposed'] == 4 and sum(r['valid'] for r in doc['sensitivity']['per_query']) == 0)
    expect(label + ':alternatives_preserved', any(a['name'] == 'ORIGINAL_K' and a['scored'] and not a['headline'] for a in sc['alternatives']) and all(not a['scored'] for a in sc['alternatives'] if a['name'].startswith('ML_') or a['name'].startswith('GL10_')))
    oracle = []
    for member in sc['members']:
        count = 0
        for row, target in zip(member['rows'], targets):
            residual = row['predicted_speed_km_s'] - target['velocity']
            expected = {'observed_speed_km_s': target['velocity'], 'quoted_sigma_km_s': target['sigma'],
                        'signed_residual_km_s': residual, 'sigma_ratio': residual / target['sigma'],
                        'fractional_error': residual / target['velocity'], 'valid': True,
                        'within_error': abs(residual) <= target['sigma']}
            assert all(row[k] == v for k, v in expected.items())
            count += expected['within_error']
        assert member['within_error_count'] == count and member['n_rows'] == 43
        oracle.append(count)
    expect(label + ':ladder_fields_and_43_denominator', len(oracle) == len(doc['members']), oracle)
    tampered = folder / 'TAMPERED_MANIFEST_COPY.json'
    with tampered.open('xb') as f:
        f.write(Path(w['path']).read_bytes() + b'\n')
    bad = F.score_after_freeze(freeze_manifest_path=str(tampered), registration_path=w['registration_path'],
                              expected_manifest_file_sha256=logged['manifest_file_sha256'], target_rows=targets)
    expect(label + ':manifest_tamper_refused', not bad['ok'] and 'sha256' in ' '.join(bad['reasons']))
    bad2 = F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=w['registration_path'],
                               expected_manifest_file_sha256='0' * 64, target_rows=targets)
    expect(label + ':wrong_external_hash_refused', not bad2['ok'])
    bad3 = F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=w['registration_path'],
                               expected_manifest_file_sha256=logged['manifest_file_sha256'], target_rows=targets[:-1])
    expect(label + ':missing_target_row_refused', not bad3['ok'])
    # Target data in freeze notes is refused by both modules, without touching the real target.
    bad_args = copy.deepcopy(args)
    bad_args.update(out_path=str(folder / 'REJECTED_TARGET_NOTES.json'), registration_path=str(folder / 'REJECTED_TARGET_REGISTRATION.json'))
    bad_args['notes']['target_rows'] = targets
    bad4 = F.write_freeze_manifest(**bad_args)
    expect(label + ':target_notes_refused', not bad4['ok'] and not Path(bad_args['out_path']).exists())
    return {'label': label, 'rule': rule, 'n_members': len(doc['members']), 'freeze_status': w['freeze_status'],
            'manifest': w['path'], 'manifest_sha256': w['manifest_file_sha256'],
            'registration_sha256': w['registration_file_sha256'], 'score_sha256': sha(folder / 'LADDER_SCORE_SYNTHETIC.json'),
            'raw_results_pinned': len(raw_paths + alt_paths), 'headline': sc['headline'],
            'sf3': sf3, 'pre8': pre8, 'rejections': {'tamper': bad['reasons'], 'wrong_external_hash': bad2['reasons'],
                                                   'missing_target_row': bad3['reasons'], 'target_notes': bad4['reasons']}}


if __name__ == '__main__':
    limit_note = 'RLIMIT_AS unavailable on this macOS runtime; observed RSS reported'
    try:
        old_soft, old_hard = resource.getrlimit(resource.RLIMIT_AS)
        new_soft = min(7 * 1024**3, old_hard) if old_hard > 0 else 7 * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (new_soft, old_hard))
        limit_note = str(resource.getrlimit(resource.RLIMIT_AS))
    except (OSError, ValueError) as exc:
        limit_note += ': ' + str(exc)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    RUN = HERE / ('synthetic_checks_v003_' + stamp)
    RUN.mkdir()
    sys.addaudithook(audit)
    tests = []
    E, F, S, toy = load(ENGINE, 'cx3_engine'), load(ORIGINAL, 'cx3_original'), load(SUCCESSOR, 'cx3_successor'), load(TOY, 'cx3_toy')
    toy.ENG_PATH = str(ENGINE)
    driver_sha = sha(DRIVER)
    slots = json.loads(SLOTS.read_bytes())
    T = toy.toy_inputs(str(RUN), '3D')
    qids = T['qids']
    mode = F.apply_coordinate_mode(coordinates=T['coordinates'], coordinate_mode={'mode': 'DDO154_DISTANCE_FIXED_AT_REGISTERED', 'free_coordinates': ['a', 'b'], 'fixed_engine_coordinates': {'D_ddo': 4.04}})
    fs = F.make_freeze_coordinate_spec(coordinates=mode['coordinates'])
    T['region_sha_logged'] = sha(T['region_path'])
    run = E.run_calibration_region(forward=T['forward_ddo'], coordinates=fs['engine_coordinates'],
                                  observation_region_path=T['region_path'], observation_region_sha256=T['region_sha_logged'],
                                  u_seed=None, budget=600, rel_step=0.05, min_step=1e-4, max_halvings=3,
                                  null_tolerance=1e-6, repair_iterations=8, max_repair_step=0.25, march_step=0.05,
                                  bisection_steps=4, design_count=8, global_design_count=24, max_march_rounds=4,
                                  hull_growth_tol=0.01, ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0}, rng_seed=0)
    rec = E.write_calibration_record(run=run, record_path=str(RUN / 'CALIBRATION_RECORD.json'), registry_path=str(RUN / 'CALIBRATION_REGISTRY.jsonl'))
    expect('synthetic_engine_complete_and_recorded', run['status'] == 'COMPLETE' and rec['ok'], [run['status'], rec.get('reasons')])
    sel = F.select_representative_points(exploration=run, interior_count=6, spec=fs['spec'])
    expect('selection', sel['ok'])
    pipelines = [pipeline(F, 'v003d_continuum', 'continuum_v001'),
                 pipeline(S, 'successor_continuum', 'continuum_v001'),
                 pipeline(S, 'successor_nodes_ro1_fired', 'nodes_v001')]
    baseline = make_result({q: 100.0 + j for j, q in enumerate(qids)})
    probes = []
    def probe(name, mutate, old_accepts):
        obj = copy.deepcopy(baseline)
        mutate(obj)
        old = F._call_forward(lambda theta: obj, {}, qids)
        new = S._call_forward(lambda theta: obj, {}, qids)
        expect(name + ':old_behavior', all(old[1]) is old_accepts, old[3])
        expect(name + ':successor_refuses', not any(new[1]), new[3])
        ev = S.evaluate_envelopes(forward_ngc=lambda theta: obj, points=sel['points'], spec=fs['spec'], query_ids=qids, budget=100)
        ref = S.select_reference_member(selection=sel, evaluation=ev)
        expect(name + ':no_freeze_reference', not ref['ok'])
        probes.append({'name': name, 'v003d_accepted': all(old[1]), 'successor_refused': not any(new[1]),
                       'successor_reasons': new[3], 'reference_reasons': ref.get('reasons')})
    probe('missing_prediction_id', lambda d: d['speeds_km_s'].pop(qids[-1]), False)
    probe('missing_rows_entry', lambda d: d['rows'].pop(), True)
    probe('truncated_null_speed', lambda d: (d['rows'][-1].update(valid=False, reason='QUERY_BEYOND_TRUNCATION', speed_km_s=None), d['speeds_km_s'].__setitem__(qids[-1], None), d['invalid_rows'].append(qids[-1])), False)
    probe('truncated_finite_diagnostic_speed', lambda d: (d['rows'][-1].update(valid=False, reason='QUERY_BEYOND_TRUNCATION'), d['invalid_rows'].append(qids[-1])), True)
    probe('speed_map_disagrees_with_rows', lambda d: d['speeds_km_s'].__setitem__(qids[-1], 999.0), True)
    probe('duplicate_rows', lambda d: d['rows'].__setitem__(-1, copy.deepcopy(d['rows'][0])), True)
    probe('raw_target_rows', lambda d: d.__setitem__('target_rows', [{'id': qids[0], 'velocity': 100.0, 'sigma': 1.0}]), True)
    probe('nested_target_alias', lambda d: d['uv_tail'].__setitem__('targetVelocityKms', [123.0]), True)
    probe('ro1_unarmed', lambda d: d['route_a_outcome']['ro1'].__setitem__('armed', False), True)
    probe('ro1_unrecognised_refusal', lambda d: d['route_a_outcome']['ro1'].update(fired=True, events=[{'code': 'ROUTE_A_READOUT_NO_CIRCULAR_BRANCH', 'after_convergence': True, 'refusal': 'OTHER'}]), True)
    probe('tail_pending_certificate', lambda d: d['uv_tail']['pending_certificates'].append('eps_certificate'), True)
    probe('tail_missing_stage_digest', lambda d: d['uv_tail']['stage_records'][0].pop('state_digest'), True)
    probe('nodes_missing_context', lambda d: d['uv_tail'].__setitem__('source_rule', 'nodes_v001'), True)
    expect('no_denied_accesses', not DENIED, DENIED)
    report = {'scope': 'TESTED_SYNTHETIC_ONLY; real NGC route-B tail producer and scientific acceptance UNTESTED',
              'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'tests': tests,
              'n_passed': sum(x['passed'] for x in tests), 'n_total': len(tests), 'pipelines': pipelines,
              'probes': probes, 'external_inputs_sha256': {str(p): sha(p) for p in (ENGINE, ORIGINAL, SUCCESSOR, TOY, SLOTS, DRIVER)},
              'read_audit': sorted(READS), 'denied_accesses': DENIED,
              'resource_maxrss_native_units': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'address_space_limit_attempt': limit_note, 'single_thread_env': {k: os.environ[k] for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')},
              'process_creation': 'denied by audit hook; one process only'}
    write(RUN / 'RESULTS_CX3V003.json', report)
    print(json.dumps({'run_dir': str(RUN), 'passed': report['n_passed'], 'total': report['n_total'], 'peak_rss': report['resource_maxrss_native_units']}))
