"""0531 v003f roster-bound adaptation of the 111-check v003e reviewer; SYNTHETIC ONLY.

Original reviewer inputs and independent D1/band/LADDER oracles are retained.
Required refusals invert nine former defect probes; the public scorer signature
now requires external root pins. Unreachable old downstream assertions are mapped
explicitly. Additional tests cover every 0531 ruling and partial failed members.
The audit hook allows pinned modules/slots/prior reviewer results and this new run
only; it refuses other files, subprocesses, network, deletion and overwrites.
Synthetic targets are written only after freeze, registration and logged SHA.
"""
import os
for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import copy
import datetime
import hashlib
import json
import math
import resource
import sys
import types
import traceback
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REVIEW = TOOLS
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V003E = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py')
ORIGINAL_RESULTS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_freeze_v003e_c2/runs/run_20261018T125924Z/REVIEW_RESULTS.json')
BOUNDARY = ART / 'freeze_score_readiness_cx3/prediction_freeze_v010_boundary_cx3v002.py'
V003D = ART / 'calibration_engine_freeze_v003b_v003d/prediction_freeze_c2v003d.py'
ENGINE = ART / 'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py'
SLOTS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json')
PINS = {ORIGINAL_RESULTS: 'd0756161d5778b3b41876cf715eb2203ccb85e93f659bdd15f0cb40d88cbd5a1', V003E: '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405',
        BOUNDARY: 'edb86bfd60108db625fcc893ea646262f3edfdcf361c3a0d1b62dbb08b393d36',
        V003D: '74e0d4060e443755486fba3aa0775060d2909c2bb78df9d948f346159112b67d',
        ENGINE: '6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3',
        SLOTS: 'd3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969'}
PINS.update({Path(k):v for k,v in {'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json': 'ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_f10_c2/route_b_v006/configs/GALAXY_CONFIG_NGC3198_C2V006.json': '64b6f1fadb432b1d5e2ee5b54620fb0c4d2cdb59e425e8034458e0dcd58ee441', '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json': 'f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/annular_source_kernel_0403/annular_bernstein_source_kernel_v001.py': '2544d22f46dbf225139f92f6a566f814e5857f265c43d88565c6a4d3894a759e', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/r5/cascade/route_b/ngc_uvt_route_b_binding_cx3v006_r5cx3v001.py': 'f348d0ca9fb052549f2cd219e040afd294e2ad6da02cf659d9b0bfb27325bca7', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V002_DEFAULT.json': '88ef386d2bd4e14be23709d21b23fd3b7b57a2cc85adcc09d6a0459bcbc108da', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/build_registered_radii_cx3v001.py': '3db13f6eea538fb4084fff9fc6caf8fca5dcae64e3024429835b89ab763738ac'}.items()})
PINS.update({Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage0_grid_gate_c2/candidate/STAGE0_POOLED8_CANDIDATE_GRID_V001.npz'):'bdb9016c97685d72de8fb93d43cb6ce5baff42b64e59f99af14fb310c8317ca5',Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003f/runs/run_20261018T131716816089Z/REVIEW_RESULTS.json'):'f2e0c9e6ad6c16bc1028d55a3725995f12ebfc8f99894fcc09ad6e41c1650e51'})
ALLOWED = {str(p.resolve()) for p in PINS} | {str(Path(__file__).resolve())}
READS, DENIED = set(), []
RUN = None


def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.spawn', 'os.posix_spawn', 'os.fork',
                 'os.forkpty') or event.startswith('socket.'):
        DENIED.append(event)
        raise PermissionError('no processes or network')
    if event in ('os.remove', 'os.unlink', 'os.rename', 'os.replace', 'os.rmdir', 'shutil.rmtree'):
        DENIED.append(event)
        raise PermissionError('no deletion')
    if event == 'open' and not isinstance(args[0], int):
        p = str(Path(os.fsdecode(args[0])).resolve())
        mode, flags = args[1], args[2]
        wr = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
             (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)))
        inside = RUN is not None and (p == str(RUN) or p.startswith(str(RUN) + os.sep))
        if wr:
            if not inside or (isinstance(flags, int) and not (flags & os.O_EXCL)) and os.path.lexists(p):
                DENIED.append(['write', p])
                raise PermissionError('writes only by exclusive create inside the run dir')
        elif inside or p in ALLOWED or 'site-packages/numpy/' in p or p.startswith(sys.base_prefix + '/') \
                or p.startswith(sys.prefix + '/'):
            READS.add(p)
        else:
            DENIED.append(['read', p])
            raise PermissionError('read outside allowlist: ' + p)


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def write_x(path, obj):
    with open(path, 'xb') as fh:
        fh.write(canon(obj) if not isinstance(obj, bytes) else obj)


def load(path, name):
    raw = Path(path).read_bytes()
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    sys.modules[name] = mod
    exec(compile(raw, str(path), 'exec'), mod.__dict__)
    return mod


TESTS = []


def check(name, cond, evidence=None, expect_finding=False):
    """Record a check. expect_finding=True marks a probe whose PASS means a defect was demonstrated."""
    TESTS.append({'name': name, 'passed': bool(cond), 'demonstrates_finding': expect_finding,
                  'evidence': evidence if isinstance(evidence, (str, int, float, bool, type(None), list, dict)) else repr(evidence)})
    print(('PASS ' if cond else 'FAIL ') + ('[FINDING] ' if expect_finding else '') + name)


def stub(label):
    return hashlib.sha256(('RVW_SYNTHETIC:' + label).encode()).hexdigest()


# ------------------------------------------------------------------ own synthetic world
QIDS = ['RVW-Q%02d' % k for k in range(1, 44)]
REGION_ROWS = ['RR%02d' % i for i in range(1, 13)]
OBS, SIG = 80.0, 0.9
Z = 2.865260238532134
DC = 4.04


def build_world(run):
    region = run / 'RVW_SYNTHETIC_REGION_NOT_DDO154.json'
    mu = 25.0 + 5.0 * math.log10(DC)
    write_x(region, {'rows': [{'id': r, 'reference_radius_kpc': 0.4 * (i + 1) + 0.1, 'observed_speed_km_s': OBS,
                                'quoted_random_sigma_km_s': SIG,
                                'conditional_random_acceptance_low_km_s': OBS - Z * SIG,
                                'conditional_random_acceptance_high_km_s': OBS + Z * SIG}
                               for i, r in enumerate(REGION_ROWS)],
                      'statistical_choice': 'review synthetic', 'forward_coordinates': 'review synthetic',
                      'distance_summary': {'modulus_mag': mu, 'distance_central_Mpc': DC, 'reported68_low_Mpc': DC * 0.97,
                                           'reported68_high_Mpc': DC * 1.03, 'scope': 'review synthetic'}})
    qm = run / 'RVW_SYNTHETIC_QUERY_MANIFEST_NOT_NGC3198.json'
    write_x(qm, {'rows': [{'query_id': q, 'data_row_index': j + 1, 'Rad_text': '%.2f' % (0.55 * (j + 1)),
                           'Rad_unit': 'kpc'} for j, q in enumerate(QIDS)]})
    slots = json.loads(SLOTS.read_bytes())
    shared = [
        dict(name='a', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.35, units='dimensionless',
             scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='b', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.55, units='dimensionless',
             scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='q', transform='linear', lower=0.5, upper=1.5, role='fixed', trial_value=1.0, units='kpc',
             scope='shared', kind='other', reference_value=None, sensitivity={'mode': 'box_ends'}),
        dict(name='D_ddo', transform='log', lower=DC * 0.97, upper=DC * 1.03, role='nuisance', trial_value=DC,
             units='Mpc', scope='ddo154_nuisance', kind='distance', reference_value=4.04, sensitivity=None),
    ]
    ngc = copy.deepcopy(slots['ngc3198_slots'])
    notes = copy.deepcopy(slots['notes_block_for_manifest'])
    notes['slots_source'] = {'path': str(SLOTS), 'sha256': PINS[SLOTS]}
    notes['review_scope'] = 'Claude review synthetic fixtures; not a science result'
    notes['structural_assumptions']['A18-REVIEW-SYNTHETIC'] = {'section': 'A18', 'text_verbatim': 'review synthetic stand-in for the A18 in-plane anisotropy note (not the root text)', 'source': 'review fixture'}
    trial = {c['name']: c['trial_value'] for c in ngc}
    return dict(region=str(region), qm=str(qm), coords=shared + ngc, notes=notes, slots=slots, ngc_trial=trial)


def forward_ddo(theta):
    g = 30.0 * ((theta['a'] - 0.35) ** 2 + 0.6 * (theta['b'] - 0.55) ** 2)
    return {'speeds_km_s': {r: OBS + g + 0.02 * i * (theta['a'] - 0.35) for i, r in enumerate(REGION_ROWS)},
            'valid': True, 'reasons': []}


def base_speed(theta, j):
    return 92.0 + 25.0 * theta['a'] + 12.0 * theta['b'] + (j + 1) * (0.9 + 0.6 * theta['a'] - 0.4 * theta['b']) \
        + 2.0 * (theta['q'] - 1.0)


def v010_result(speeds, invalid=None):
    """Own v010-shaped forward result. invalid: {row index: (reason, gate pin or None)} -> null speed, valid False."""
    invalid = invalid or {}
    rows, smap, inv = [], {}, []
    for j, q in enumerate(QIDS):
        if j in invalid:
            reason, gate = invalid[j]
            r = {'id': q, 'speed_km_s': None, 'valid': False, 'reason': reason}
            if gate is not None:
                r['registered_invalid_gate'] = gate
            rows.append(r)
            smap[q] = None
            inv.append(q)
        else:
            rows.append({'id': q, 'speed_km_s': speeds[j], 'valid': True, 'reason': None})
            smap[q] = speeds[j]
    stages = [{'stage': 'rvw_' + k, 'kind': k, 'finish_sha256': stub(k + 'f'), 'state_digest': stub(k + 's'),
               'empty': False, 'production_admissible': True, 'test_only_admitted': False}
              for k in ('reference', 'body', 'columns', 'rotation')]
    return {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'galaxy': 'NGC3198', 'driver_sha256': stub('driver'),
            'call_spec_sha256': stub('spec'), 'scored': False, 'valid': True, 'status': 'COMPLETED', 'reasons': [],
            'rows': rows, 'speeds_km_s': smap, 'invalid_rows': inv,
            'route_a_outcome': {'classification': 'CONVERGED', 'converged_finite_fixed_point': True,
                                'ro1': {'rule': 'RO1', 'armed': True, 'fired': False, 'events': [],
                                        'worker_sha256': stub('w'), 'binding_sha256': stub('b')}},
            'uv_tail': {'schema': 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010', 'enabled': True, 'admissibility': 'production',
                        'pending_certificates': [], 'source_rule': 'continuum_v001', 'nodes_ext_context': None,
                        'config': {'normalized_sha256': stub('cfg')}, 'stage_records': stages}}


class World:
    pass


W = World()


def make_forward(pattern, delta=0.0, raw_dir=None, saved=None):
    """pattern(theta) -> invalid dict. Geometry other than the registered slot trial values refuses (A16.4)."""
    def f(theta):
        assert 'D_ddo' not in theta
        if any(theta[k] != v for k, v in W.ngc_trial.items()):
            return {'valid': False, 'speeds_km_s': {}, 'reasons': ['GEOMETRY_NOT_EXPOSED: review toy']}
        speeds = [base_speed(theta, j) + delta for j in range(43)]
        obj = v010_result(speeds, pattern(theta))
        if raw_dir is not None:
            p = raw_dir / ('RAW_%03d.json' % len(saved))
            write_x(p, obj)
            saved.append(str(p))
        return obj
    return f


def gate_file(name, reasons, qids, extra=None, status='REGISTERED', schema=None):
    doc = {'schema': schema or W.F.INVALID_GATE_SCHEMA, 'registration_status': status, 'registered_reasons': reasons,
           'query_ids': qids, 'scope': 'review synthetic declaration; no physical registration'}
    if extra:
        doc.update(extra)
    p = RUN / ('GATE_' + name + '.json')
    write_x(p, doc)
    return {'path': str(p), 'sha256': sha_file(p)}


def pipeline(F, label, pattern, alternatives=None, extra_inputs=(), alt_pattern=None, write=True):
    folder = RUN / label
    folder.mkdir()
    raw = folder / 'raw'
    raw.mkdir()
    saved = []
    fwd = make_forward(pattern, 0.0, raw, saved)
    afwd = make_forward(alt_pattern or pattern, 6.5, raw, saved)
    ev = F.evaluate_envelopes(forward_ngc=fwd, points=W.sel['points'], spec=W.fs['spec'], query_ids=QIDS, budget=100)
    alt = F.evaluate_envelopes(forward_ngc=afwd, points=W.sel['points'], spec=W.fs['spec'], query_ids=QIDS, budget=100)
    res = {'ev': ev, 'alt': alt, 'folder': folder}
    if not (ev.get('ok') and alt.get('ok')):
        return res
    ref = F.select_reference_member(selection=W.sel, evaluation=ev)
    res['ref'] = ref
    if not ref.get('ok'):
        return res
    sens = F.evaluate_sensitivity(forward_ngc=fwd, reference=ref, selection=W.sel, spec=W.fs['spec'], query_ids=QIDS,
                                  null_direction_rule={'mode': 'box_ends'}, budget=100)
    res['sens'] = sens
    if not write:
        return res
    alts = alternatives or copy.deepcopy(W.slots['alternatives'])
    evs = {'BR_A_F10_PRIMARY': ev, 'ORIGINAL_K': alt}
    for a in alts['declared']:
        if a['status'] == 'EVALUATED_BEFORE_FREEZE' and a['name'] not in evs:
            evs[a['name']] = alt
    notes = copy.deepcopy(W.notes)
    notes['raw_result_custody'] = [{'path': p, 'sha256': sha_file(p)} for p in saved]
    w = F.write_freeze_manifest(
        out_path=str(folder / 'FREEZE_MANIFEST.json'), registration_path=str(folder / 'FREEZE_REGISTRATION.json'),
        parameter_region={'description': 'review synthetic trial box',
                          'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'},
        observation_rule={'rule': 'review synthetic closed rectangle'}, spec=W.fs['spec'], selection=W.sel,
        alternatives=alts, alternative_evaluations=evs, reference=ref, sensitivity=sens, query_ids=QIDS,
        query_manifest={'path': W.qm, 'sha256': sha_file(W.qm), 'role': 'SYNTHETIC_FIXTURE'},
        code_files=[F.__file__, str(ENGINE), str(Path(__file__).resolve())],
        input_files=[W.region, W.qm, W.rec['record_path'], str(SLOTS)] + saved + list(extra_inputs),
        notes=notes, allow_incomplete=False)
    res['w'] = w
    if not w.get('ok'):
        return res
    logged = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'manifest_file_sha256': w['manifest_file_sha256'], 'registration_file_sha256': w['registration_file_sha256'],
              'targets_opened': False}
    write_x(folder / 'PRE_TARGET_LOG.json', logged)
    res['logged'] = logged
    res['vf'] = F.verify_freeze_manifest(freeze_manifest_path=w['path'])
    res['vr'] = F.verify_registration(registration_path=w['registration_path'])
    res['doc'] = json.loads(Path(w['path']).read_bytes())
    return res


def make_targets(doc, folder, invalid_bait=True):
    """Own targets, created only after the freeze, registration and logged hash. Built from the frozen reference
    member's own predictions: rows j % 3 == 0 sit 3.2 sigma off (miss), others 0.4 sigma off (hit). On a row the
    reference left null, the target is set to the unseen base value, so any leak of a value would score a hit."""
    ref_id = doc['reference_member']['member_id']
    ref = next(m for m in doc['members'] if m['member_id'] == ref_id)
    rows = []
    for j, q in enumerate(QIDS):
        s = 1.5
        p = ref['speeds_km_s'][j]
        if p is None:
            p = base_speed(ref['theta_ngc'], j) if invalid_bait else 50.0
            v = p
        else:
            v = p + (3.2 * s if j % 3 == 0 else -0.4 * s)
        rows.append({'id': q, 'velocity': float(v), 'sigma': s})
    tp = folder / 'RVW_SYNTHETIC_TARGET_ROWS.json'
    write_x(tp, rows)
    return json.loads(tp.read_bytes())


def score(F, res, targets, expected=None):
    return F.score_after_freeze(freeze_manifest_path=res['w']['path'], registration_path=res['w']['registration_path'],
                                expected_manifest_file_sha256=expected or res['logged']['manifest_file_sha256'],
                                target_rows=targets)


# ------------------------------------------------------------------ independent oracles
def oracle_contract_valid(m):
    if not (m['evaluated'] and m['forward_valid_flag'] is True):
        return False
    for rv, s, reg in zip(m['row_valid'], m['speeds_km_s'], m['row_registration']):
        if rv:
            if s is None or not math.isfinite(s):
                return False
        elif reg is None or reg.get('status') != 'INVALID' or s is not None:
            return False
    return True


def oracle_reference(doc):
    c = doc['admitted_region']['centroid_identified']
    cands = []
    for m in doc['members']:
        if oracle_contract_valid(m):
            d = math.sqrt(sum((a - b) ** 2 for a, b in zip(m['identified_projection'], c)))
            cands.append((d, m['log_index'], m['member_id']))
    cands.sort()
    return cands[0][2] if cands else None


def oracle_member_rows(m, targets):
    out = []
    for j, t in enumerate(targets):
        reg = m['row_registration'][j]
        p = m['speeds_km_s'][j]
        if reg is not None or not m['row_valid'][j] or p is None:
            out.append(False)
        else:
            out.append(abs(p - t['velocity']) <= t['sigma'])
    return out


def oracle_envelope(doc, targets):
    rows = []
    for j, t in enumerate(targets):
        vals = [m['speeds_km_s'][j] for m in doc['members'] if m['row_valid'][j] and m['speeds_km_s'][j] is not None]
        if not vals:
            rows.append((None, None, False, False))
        else:
            lo, hi = min(vals), max(vals)
            rows.append((lo, hi, True, lo <= t['velocity'] + t['sigma'] and hi >= t['velocity'] - t['sigma']))
    return rows


def probe_eval(F, label, mutate, expect_ok, finding=False, note=None):
    base = v010_result([100.0 + 0.5 * j for j in range(43)])

    def fwd(theta):
        if any(theta[k] != v for k, v in W.ngc_trial.items()):
            return {'valid': False, 'speeds_km_s': {}, 'reasons': ['GEOMETRY_NOT_EXPOSED']}
        d = copy.deepcopy(base)
        mutate(d)
        return d
    try:
        ev = F.evaluate_envelopes(forward_ngc=fwd, points=W.sel['points'], spec=W.fs['spec'], query_ids=QIDS, budget=100)
    except Exception as exc:   # an escaped exception is itself a finding
        check(label, False, 'EXCEPTION ' + repr(exc))
        return None
    ok = bool(ev.get('ok'))
    check(label, ok == expect_ok, {'ok': ok, 'reasons': (ev.get('reasons') or [])[:3], 'note': note}, finding)
    return ev


def invalidate(d, j, reason, gate=None, speed=None, map_speed=None, roster=True):
    q = QIDS[j]
    d['rows'][j].update(valid=False, reason=reason, speed_km_s=speed)
    if gate is not None:
        d['rows'][j]['registered_invalid_gate'] = gate
    d['speeds_km_s'][q] = map_speed
    if roster:
        d['invalid_rows'] = [x for x in QIDS if x in set(d['invalid_rows']) | {q}]


def rehash_manifest(F, doc):
    body = {k: v for k, v in doc.items() if k != 'manifest_sha256'}
    doc = dict(doc)
    doc['manifest_sha256'] = hashlib.sha256(F._canonical_bytes(body)).hexdigest()
    return F._canonical_bytes(doc)


# ------------------------------------------------------------------ main
def main():
    global RUN
    for p, h in PINS.items():
        if sha_file(p) != h:
            raise SystemExit('pin mismatch %s' % p)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    RUN = REVIEW / 'runs' / ('run_' + stamp)
    RUN.mkdir(parents=True)
    sys.addaudithook(audit)
    E = load(ENGINE, 'rvw_engine')
    F = load(V003E, 'rvw_v003e')
    D = load(V003D, 'rvw_v003d')
    B = load(BOUNDARY, 'rvw_boundary')
    W.F = F
    world = build_world(RUN)
    for k, v in world.items():
        setattr(W, k, v)
    mode = F.apply_coordinate_mode(coordinates=W.coords, coordinate_mode={
        'mode': 'DDO154_DISTANCE_FIXED_AT_REGISTERED', 'free_coordinates': ['a', 'b'],
        'fixed_engine_coordinates': {'D_ddo': DC}})
    check('setup:coordinate_mode', mode.get('ok'), mode.get('reasons'))
    W.fs = F.make_freeze_coordinate_spec(coordinates=mode['coordinates'])
    check('setup:freeze_spec', W.fs.get('ok'), W.fs.get('reasons'))
    region_sha = sha_file(W.region)
    run = E.run_calibration_region(
        forward=forward_ddo, coordinates=W.fs['engine_coordinates'], observation_region_path=W.region,
        observation_region_sha256=region_sha, u_seed=None, budget=700, rel_step=.05, min_step=1e-4, max_halvings=3,
        null_tolerance=1e-6, repair_iterations=8, max_repair_step=.25, march_step=.05, bisection_steps=4,
        design_count=8, global_design_count=24, max_march_rounds=4, hull_growth_tol=.01,
        ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.}, rng_seed=7)
    W.rec = E.write_calibration_record(run=run, record_path=str(RUN / 'CALIBRATION_RECORD.json'),
                                       registry_path=str(RUN / 'CALIBRATION_REGISTRY.jsonl'))
    check('setup:calibration_complete', run.get('status') == 'COMPLETE' and W.rec.get('ok'),
          [run.get('status'), (run.get('reasons') or [])[:3]])
    W.sel = F.select_representative_points(exploration=run, interior_count=5, spec=W.fs['spec'])
    check('setup:selection', W.sel.get('ok'), W.sel.get('reasons'))
    pts = W.sel['points']
    centroid = W.sel['admitted_region']['centroid_identified']
    dist = sorted((math.sqrt(sum((a - b) ** 2 for a, b in zip(p['identified_projection'], centroid))), p['log_index'], i)
                  for i, p in enumerate(pts))
    nearest_theta = pts[dist[0][2]]['theta_natural']
    second_theta = pts[dist[1][2]]['theta_natural']
    def is_pt(theta, th):
        return abs(theta['a'] - th['a']) < 1e-12 and abs(theta['b'] - th['b']) < 1e-12
    summary = {'n_members': len(pts), 'nearest_log_index': dist[0][1], 'second_log_index': dist[1][1]}

    # ---------- gate files (target-free, pinned, created before any freeze)
    g_outer = gate_file('OUTER_SYNTH', ['RVW_SYNTH_OUTER_GATE'], QIDS[38:])
    g_all = gate_file('ALL43_SYNTH', ['RVW_SYNTH_ROW_GATE'], QIDS)
    W.root_gatepins = [g_outer, g_all]
    W.default_root_pins = root_rosters(RUN/'DEFAULT_ROOT_AUTHORITY')

    # ================= S0 all-valid regression: v003d vs v003e LADDER output on identical inputs
    allvalid = lambda th: {}
    r_e = pipeline(F, 'S0_all_valid_v003e', allvalid)
    r_d = pipeline(D, 'S0_all_valid_v003d', allvalid)
    ok0 = all(r.get('w', {}).get('ok') for r in (r_e, r_d))
    check('S0:both_freeze', ok0, [r_e.get('w', {}).get('reasons'), r_d.get('w', {}).get('reasons'),
                                  r_e['ev'].get('reasons'), r_d['ev'].get('reasons')])
    if ok0:
        de, dd = r_e['doc'], r_d['doc']
        t = make_targets(de, r_e['folder'])
        te = score(F, r_e, t)
        td = score(D, r_d, t)
        check('S0:both_score', te.get('ok') and td.get('ok'), [te.get('reasons'), td.get('reasons')])
        same_members = [ {k: v for k, v in m.items() if k != 'row_registration'} for m in de['members']] == dd['members']
        check('S0:frozen_member_arrays_identical_except_new_row_registration', same_members)
        check('S0:row_registration_all_null', all(r is None for m in de['members'] for r in m['row_registration']))
        diff_top = sorted(k for k in set(de) | set(dd) if de.get(k) != dd.get(k))
        check('S0:manifest_top_level_diffs_are_schema_module_hash_pins_members_alt_and_timestamps_only',
              set(diff_top) <= {'schema', 'module', 'manifest_sha256', 'pins', 'members', 'created_utc',
                                'alternative_results', 'reference_member', 'sensitivity', 'notes', 'rules'}, diff_top)
        for key in ('pointwise_envelope', 'admitted_region'):
            check('S0:%s_identical' % key, de[key] == dd[key])
        check('S0:reference_member_identical_except_rule_text',
              {k: v for k, v in de['reference_member'].items() if k != 'rule'} == {k: v for k, v in dd['reference_member'].items() if k != 'rule'}
              and de['reference_member']['rule'] == F.REFERENCE_RULE and dd['reference_member']['rule'] == D.REFERENCE_RULE)
        strip = lambda ms: [{k: v for k, v in m.items() if k != 'row_registration'} for m in ms]
        check('S0:alternative_members_identical_except_row_registration',
              all(strip(de['alternative_results'][nm]['members']) == dd['alternative_results'][nm]['members']
                  and {k: v for k, v in de['alternative_results'][nm].items() if k != 'members'} == {k: v for k, v in dd['alternative_results'][nm].items() if k != 'members'}
                  for nm in dd['alternative_results']) and set(de['alternative_results']) == set(dd['alternative_results']))
        strip2 = lambda ms: [{k: v for k, v in m.items() if k not in ('row_registration', 'reasons')} for m in ms]
        check('S0:NOTE_sensitivity_entry_diagnostic_reason_text_changed_only',
              strip(de['sensitivity']['evaluations']) != dd['sensitivity']['evaluations'], None, expect_finding=True)
        check('S0:sensitivity_identical_except_row_registration_and_diagnostic_reasons',
              strip2(de['sensitivity']['evaluations']) == strip2(dd['sensitivity']['evaluations'])
              and {k: v for k, v in de['sensitivity'].items() if k != 'evaluations'} == {k: v for k, v in dd['sensitivity'].items() if k != 'evaluations'})
        check('S0:NOTE_v003e_manifest_module_stamp_is_boundary_name', de['module'] == 'prediction_freeze_v010_boundary_cx3v002', de['module'], expect_finding=True)
        check('S0:sensitivity_per_query_identical', de['sensitivity']['per_query'] == dd['sensitivity']['per_query'])
        hd = {k: v for k, v in te['headline'].items()}
        check('S0:headline_identical', hd == td['headline'],
              sorted(k for k in set(hd) | set(td['headline']) if hd.get(k) != td['headline'].get(k)))
        common_ok = True
        for me, md in zip(te['members'], td['members']):
            for k in md:
                if k == 'rows':
                    for re_, rd_ in zip(me['rows'], md['rows']):
                        for kk in rd_:
                            if kk == 'row_notes':
                                continue
                            if re_[kk] != rd_[kk]:
                                common_ok = False
                elif me[k] != md[k]:
                    common_ok = False
        check('S0:ladder_member_rows_identical_on_all_v003d_keys', common_ok)
        check('S0:envelope_score_identical_on_v003d_keys',
              all({k: a[k] for k in b} == b for a, b in zip(te['pointwise_envelope']['rows'], td['pointwise_envelope']['rows'])))
        def alt_same(a, b):
            for k in b:
                if k == 'members':
                    for ma, mb in zip(a[k], b[k]):
                        for kk in mb:
                            if kk == 'rows':
                                if any({x: ra[x] for x in rb if x != 'row_notes'} != {x: rb[x] for x in rb if x != 'row_notes'} for ra, rb in zip(ma['rows'], mb['rows'])):
                                    return False
                            elif ma[kk] != mb[kk]:
                                return False
                elif isinstance(b[k], dict) and isinstance(a.get(k), dict):
                    if any(a[k].get(x) != b[k][x] for x in b[k] if x != 'rows') :
                        return False
                elif a.get(k) != b[k]:
                    return False
            return True
        check('S0:alternatives_score_identical_on_v003d_keys', len(te['alternatives']) == len(td['alternatives']) and all(alt_same(a, b) for a, b in zip(te['alternatives'], td['alternatives'])),
              [sorted(k for k in b if a.get(k) != b[k]) for a, b in zip(te['alternatives'], td['alternatives'])])
        summary['S0_reference'] = de['reference_member']['member_id']
        summary['S0_top_level_diffs'] = diff_top

    # ================= S1 GL4 + per-member outer cut + all-INVALID gated row; nearest member carries extra INVALIDs
    def gl4(theta):
        inv = {0: ('QUERY_INSIDE_INNERMOST_NODE', None), 1: ('QUERY_INSIDE_INNERMOST_NODE', None),
               42: ('RVW_SYNTH_ROW_GATE', g_all)}
        if is_pt(theta, nearest_theta):
            inv.update({39: ('RVW_SYNTH_OUTER_GATE', g_outer), 40: ('RVW_SYNTH_OUTER_GATE', g_outer),
                        41: ('RVW_SYNTH_OUTER_GATE', g_outer)})
        if theta['a'] > 0.38:
            inv[38] = ('RVW_SYNTH_OUTER_GATE', g_outer)
        return inv
    # v003d on the same pattern: reconstruct the 0581 blocker
    rd1 = pipeline(D, 'S1_gl4_v003d', gl4, write=False)
    check('S1:v003d_cannot_select_reference_under_GL4', not rd1.get('ref', {}).get('ok', False),
          (rd1.get('ref') or rd1['ev']).get('reasons', [])[:2])
    r1 = pipeline(F, 'S1_gl4_v003e', gl4, extra_inputs=[g_outer['path'], g_all['path']])
    ok1 = r1.get('w', {}).get('ok') and r1['vf'].get('ok') and r1['vr'].get('ok')
    check('S1:GL4_pattern_freezes_and_verifies', ok1,
          [r1['ev'].get('reasons'), r1.get('ref', {}).get('reasons'), r1.get('w', {}).get('reasons'),
           r1.get('vf', {}).get('reasons')])
    if ok1:
        doc = r1['doc']
        check('S1:manifest_has_43_ids_every_member_43_rows',
              doc['query_ids'] == QIDS and all(len(m['speeds_km_s']) == 43 and len(m['row_registration']) == 43
                                               for m in doc['members']))
        check('S1:INVALID_rows_null_with_reason',
              all((m['speeds_km_s'][j] is None and m['row_registration'][j]['status'] == 'INVALID'
                   and isinstance(m['row_registration'][j]['reason'], str))
                  for m in doc['members'] if m['member_valid'] for j in (0, 1, 42)))
        oref = oracle_reference(doc)
        check('S1:D1_reference_matches_independent_oracle', doc['reference_member']['member_id'] == oref,
              [doc['reference_member']['member_id'], oref])
        check('S1:D1_reference_is_nearest_member_despite_extra_INVALID_rows',
              doc['reference_member']['log_index'] == summary['nearest_log_index'],
              [doc['reference_member']['log_index'], summary['nearest_log_index']])
        t = make_targets(doc, r1['folder'])
        s1 = score(F, r1, t)
        check('S1:score_ok', s1.get('ok'), s1.get('reasons'))
        if s1.get('ok'):
            write_x(r1['folder'] / 'SCORE.json', s1)
            check('S1:43_rows_every_member_and_headline_n_rows_43',
                  s1['headline']['n_rows'] == 43 and all(m['n_rows'] == 43 and len(m['rows']) == 43 for m in s1['members']))
            agree = True
            inv_ok = True
            for fm, sm in zip(doc['members'], s1['members']):
                orows = oracle_member_rows(fm, t)
                if [r['within_error'] for r in sm['rows']] != orows or sm['within_error_count'] != sum(orows):
                    agree = False
                for j, r in enumerate(sm['rows']):
                    if fm['row_registration'][j] is not None:
                        if not (r['score_status'] == 'INVALID_AS_MISS' and r['tier'] == 'MISS_WORST_TIER'
                                and r['within_error'] is False and r['prediction'] is None and r['valid'] is False
                                and r['registered_reason'] == fm['row_registration'][j]['reason']
                                and r['id'] in sm['invalid_as_miss']):
                            inv_ok = False
            check('S1:within_error_counts_match_independent_oracle', agree)
            check('S1:INVALID_rows_scored_INVALID_AS_MISS_worst_tier_never_hit_listed_separately', inv_ok)
            ref = next(m for m in s1['members'] if m['member_id'] == doc['reference_member']['member_id'])
            ref_inv = [r['id'] for r in ref['rows'] if r['score_status'] == 'INVALID_AS_MISS']
            check('S1:bait_targets_on_INVALID_rows_did_not_become_hits',
                  all(not r['within_error'] for r in ref['rows'] if r['id'] in ref_inv) and len(ref_inv) == 6, ref_inv)
            check('S1:invalid_count_includes_INVALID_rows', ref['invalid_count'] >= len(ref_inv))
            oe = oracle_envelope(doc, t)
            env_ok = all((r['band_low_km_s'], r['band_high_km_s'], r['valid'], r['band_overlaps_error_bar']) == o
                         for r, o in zip(s1['pointwise_envelope']['rows'], oe))
            check('S1:envelope_from_finite_members_matches_oracle', env_ok)
            allinv = [s1['pointwise_envelope']['rows'][j] for j in (0, 1, 42)]
            check('S1:all_INVALID_rows_are_band_misses',
                  all(r['score_status'] == 'INVALID_AS_MISS' and r['tier'] == 'MISS_WORST_TIER' and not r['band_overlaps_error_bar']
                      and not r['valid'] for r in allinv))
            partial = [doc['pointwise_envelope'][j] for j in (38, 39, 40, 41)]
            check('S1:partially_INVALID_rows_band_uses_finite_subset',
                  all(r['valid'] and 0 < r['n_valid'] < len(doc['members']) for r in partial),
                  [(r['n_valid'], len(doc['members'])) for r in partial])
            alts = {a['name']: a for a in s1['alternatives']}
            check('S1:GL10_not_scored_not_headline', alts['GL10_SOURCE_GAUSS_ORDER']['status'] == 'NOT_EVALUATED_BEFORE_FREEZE'
                  and not alts['GL10_SOURCE_GAUSS_ORDER'].get('scored') and not alts['GL10_SOURCE_GAUSS_ORDER'].get('headline'))
            check('S1:ORIGINAL_K_scored_separately_not_headline', alts['ORIGINAL_K'].get('scored') and not alts['ORIGINAL_K'].get('headline'))
            summary['S1'] = {'reference': doc['reference_member']['member_id'],
                             'ref_within_error': s1['headline']['reference_within_error_count'],
                             'ref_invalid_as_miss': ref_inv,
                             'member_counts': s1['headline']['member_within_error_counts']}
            # ----- S3 post-freeze tamper attempts on the S1 manifest
            # (a) turn the reference's INVALID Q01 into a finite hit, re-hash, and score with the logged hash
            forged = copy.deepcopy(doc)
            ri = next(i for i, m in enumerate(forged['members']) if m['member_id'] == doc['reference_member']['member_id'])
            fm = forged['members'][ri]
            fm['row_valid'][0] = True
            fm['speeds_km_s'][0] = t[0]['velocity']
            fm['row_registration'][0] = None
            fp = r1['folder'] / 'FORGED_Q01_HIT.json'
            write_x(fp, rehash_manifest(F, forged))
            vf = F.verify_freeze_manifest(freeze_manifest_path=str(fp))
            check('S3:forged_INVALID_to_hit_fails_verification', not vf.get('ok'), vf.get('reasons', [])[:2])
            sc = F.score_after_freeze(freeze_manifest_path=str(fp), registration_path=r1['w']['registration_path'],
                                      expected_manifest_file_sha256=r1['logged']['manifest_file_sha256'], target_rows=t)
            check('S3:forged_INVALID_to_hit_refused_at_score', not sc.get('ok'), sc.get('reasons', [])[:1])
            # (b) post-freeze INVALID registration: add a gate to a valid MISS row of the reference (re-hashed)
            miss_j = next(j for j, r in enumerate(ref['rows']) if r['score_status'] == 'MISS')
            g_late = gate_file('LATE_POST_TARGET', ['RVW_LATE'], [QIDS[miss_j]])
            forged2 = copy.deepcopy(doc)
            fm2 = forged2['members'][ri]
            fm2['row_valid'][miss_j] = False
            fm2['speeds_km_s'][miss_j] = None
            fm2['row_registration'][miss_j] = {'status': 'INVALID', 'reason': 'RVW_LATE', 'registration': g_late}
            fp2 = r1['folder'] / 'FORGED_LATE_GATE.json'
            write_x(fp2, rehash_manifest(F, forged2))
            sc2 = F.score_after_freeze(freeze_manifest_path=str(fp2), registration_path=r1['w']['registration_path'],
                                       expected_manifest_file_sha256=r1['logged']['manifest_file_sha256'], target_rows=t)
            check('S3:post_target_gate_registration_refused_by_logged_hash', not sc2.get('ok'), sc2.get('reasons', [])[:1])
            # (c) byte tamper, (d) wrong external hash, (e) target-row extra field, (f) 42 rows
            fp3 = r1['folder'] / 'TAMPER_APPENDED_NEWLINE.json'
            write_x(fp3, Path(r1['w']['path']).read_bytes() + b'\n')
            sc3 = F.score_after_freeze(freeze_manifest_path=str(fp3), registration_path=r1['w']['registration_path'],
                                       expected_manifest_file_sha256=r1['logged']['manifest_file_sha256'], target_rows=t)
            check('S3:byte_tamper_refused', not sc3.get('ok'))
            sc4 = score(F, r1, t, expected='f' * 64)
            check('S3:external_hash_mismatch_refused', not sc4.get('ok'))
            t5 = copy.deepcopy(t)
            t5[0]['invalid'] = True
            check('S3:target_row_extra_field_refused', not score(F, r1, t5).get('ok'))
            check('S3:target_rows_42_refused', not score(F, r1, t[:-1]).get('ok'))
            t6 = copy.deepcopy(t)
            t6[0], t6[1] = t6[1], t6[0]
            check('S3:target_rows_reordered_refused', not score(F, r1, t6).get('ok'))
            # score_after_freeze has no registration/gate input: INVALID status comes only from frozen bytes
            import inspect
            params = sorted(inspect.signature(F.score_after_freeze.__wrapped__).parameters)
            check('S3:score_signature_has_no_registration_or_gate_input',
                  params == ['expected_manifest_file_sha256', 'freeze_manifest_path', 'registration_path', 'row_registration_rosters', 'target_rows'], params)

    # ================= S2 refusal probes (constant v010 result, all members)
    ev = probe_eval(F, 'S2:baseline_all_valid_ok', lambda d: None, True)
    probe_eval(F, 'S2:GL4_builtin_Q01_Q02_ok', lambda d: (invalidate(d, 0, 'QUERY_INSIDE_INNERMOST_NODE'),
                                                         invalidate(d, 1, 'QUERY_INSIDE_INNERMOST_NODE')), True)
    probe_eval(F, 'S2:finite_on_INVALID_row_refused', lambda d: invalidate(d, 0, 'QUERY_INSIDE_INNERMOST_NODE', speed=101.0, map_speed=101.0), False)
    probe_eval(F, 'S2:finite_only_in_speed_map_on_INVALID_refused', lambda d: invalidate(d, 0, 'QUERY_INSIDE_INNERMOST_NODE', map_speed=101.0), False)
    probe_eval(F, 'S2:NaN_on_INVALID_row_refused', lambda d: invalidate(d, 0, 'QUERY_INSIDE_INNERMOST_NODE', speed=float('nan')), False)
    for lab, val in (('None', None), ('NaN', float('nan')), ('inf', float('inf')), ('string', '100.0'), ('bool', True)):
        def mut(d, val=val):
            d['rows'][5]['speed_km_s'] = val
            d['speeds_km_s'][QIDS[5]] = val
        probe_eval(F, 'S2:nonfinite_on_valid_row_refused_' + lab, mut, False)
    probe_eval(F, 'S2:row_speed_disagrees_with_map_refused', lambda d: d['speeds_km_s'].__setitem__(QIDS[5], 1.0), False)
    for lab, val in (('int1', 1), ('str', 'true'), ('None', None)):
        probe_eval(F, 'S2:row_valid_flag_nonbool_refused_' + lab, lambda d, val=val: d['rows'][3].__setitem__('valid', val), False)
    probe_eval(F, 'S2:invalid_roster_missing_refused', lambda d: invalidate(d, 0, 'QUERY_INSIDE_INNERMOST_NODE', roster=False), False)
    probe_eval(F, 'S2:invalid_roster_extra_refused', lambda d: d['invalid_rows'].append(QIDS[7]), False)
    def reorder(d):
        invalidate(d, 0, 'QUERY_INSIDE_INNERMOST_NODE'); invalidate(d, 1, 'QUERY_INSIDE_INNERMOST_NODE')
        d['invalid_rows'] = [QIDS[1], QIDS[0]]
    probe_eval(F, 'S2:invalid_roster_reordered_refused', reorder, False)
    probe_eval(F, 'S2:unknown_reason_without_gate_refused', lambda d: invalidate(d, 4, 'RVW_UNREGISTERED'), False)
    probe_eval(F, 'S2:null_reason_on_INVALID_refused', lambda d: invalidate(d, 4, None), False)
    probe_eval(F, 'S2:empty_reason_on_INVALID_refused', lambda d: invalidate(d, 4, ''), False)
    probe_eval(F, 'S2:unhashable_reason_refused_not_raised', lambda d: invalidate(d, 4, ['QUERY_INSIDE_INNERMOST_NODE']), False)
    probe_eval(F, 'S2:reason_on_valid_row_refused', lambda d: d['rows'][4].__setitem__('reason', 'QUERY_INSIDE_INNERMOST_NODE'), False)
    probe_eval(F, 'S2:gate_on_valid_row_refused', lambda d: d['rows'][4].__setitem__('registered_invalid_gate', g_all), False)
    probe_eval(F, 'S2:missing_row_refused', lambda d: (d['rows'].pop(), d['speeds_km_s'].pop(QIDS[-1])), False)
    probe_eval(F, 'S2:duplicate_row_refused', lambda d: d['rows'].__setitem__(1, copy.deepcopy(d['rows'][0])), False)
    # gates
    probe_eval(F, 'S2:gate_valid_pinned_ok', lambda d: invalidate(d, 42, 'RVW_SYNTH_ROW_GATE', gate=g_all), True)
    probe_eval(F, 'S2:gate_sha_mismatch_refused', lambda d: invalidate(d, 42, 'RVW_SYNTH_ROW_GATE', gate={'path': g_all['path'], 'sha256': 'a' * 64}), False)
    probe_eval(F, 'S2:gate_query_not_listed_refused', lambda d: invalidate(d, 10, 'RVW_SYNTH_OUTER_GATE', gate=g_outer), False)
    probe_eval(F, 'S2:gate_reason_not_listed_refused', lambda d: invalidate(d, 42, 'RVW_OTHER', gate=g_all), False)
    g_draft = gate_file('DRAFT', ['RVW_D'], QIDS, status='DRAFT')
    probe_eval(F, 'S2:gate_status_not_REGISTERED_refused', lambda d: invalidate(d, 42, 'RVW_D', gate=g_draft), False)
    g_schema = gate_file('BADSCHEMA', ['RVW_S'], QIDS, schema='SOMETHING_ELSE')
    probe_eval(F, 'S2:gate_wrong_schema_refused', lambda d: invalidate(d, 42, 'RVW_S', gate=g_schema), False)
    g_tgt = gate_file('TARGETBEARING', ['RVW_T'], QIDS, extra={'observed_speed_km_s': [1.0]})
    probe_eval(F, 'S2:gate_with_target_field_refused', lambda d: invalidate(d, 42, 'RVW_T', gate=g_tgt), False)
    g_tgt2 = gate_file('TARGETALIAS', ['RVW_T2'], QIDS, extra={'targetVelocityKms': [1.0]})
    probe_eval(F, 'S2:gate_with_target_alias_refused', lambda d: invalidate(d, 42, 'RVW_T2', gate=g_tgt2), False)
    probe_eval(F, 'S2:gate_pin_extra_key_refused', lambda d: invalidate(d, 42, 'RVW_SYNTH_ROW_GATE', gate=dict(g_all, bytes=1)), False)
    probe_eval(F, 'S2:gate_path_directory_refused', lambda d: invalidate(d, 42, 'RVW_SYNTH_ROW_GATE', gate={'path': str(RUN), 'sha256': g_all['sha256']}), False)
    # gate laxity: registered_reasons / query_ids given as STRINGS -> substring membership
    g_str = gate_file('STRINGLISTS', 'RVW_LONG_REASON_TEXT', ''.join(QIDS))
    probe_eval(F, 'S2:FINDING_gate_string_fields_substring_match_accepted',
               lambda d: invalidate(d, 42, 'LONG', gate=g_str), True, finding=True,
               note='registered_reasons and query_ids are not type-checked as lists; "in" on a str is substring')
    # built-in reasons are not bound to any registered roster
    probe_eval(F, 'S2:FINDING_builtin_innermost_reason_accepted_on_mid_row_Q20',
               lambda d: invalidate(d, 19, 'QUERY_INSIDE_INNERMOST_NODE'), True, finding=True)
    probe_eval(F, 'S2:FINDING_builtin_innermost_reason_accepted_on_outer_Q43',
               lambda d: invalidate(d, 42, 'QUERY_INSIDE_INNERMOST_NODE'), True, finding=True)
    # outer valid False + rows present: v003e refuses whole freeze (v003d / edb86bfd: member invalid)
    def nonconv(d):
        d['valid'] = False
        d['route_a_outcome']['classification'] = 'NOT_CONVERGED'
        d['route_a_outcome']['converged_finite_fixed_point'] = False
    e_v = probe_eval(F, 'S2:valid_false_with_rows_refuses_entire_evaluation_in_v003e', nonconv, False)
    for mod, lab in ((D, 'v003d'), (B, 'edb86bfd')):
        base = v010_result([100.0 + 0.5 * j for j in range(43)])
        def fwd(theta, base=base):
            if any(theta[k] != v for k, v in W.ngc_trial.items()):
                return {'valid': False, 'speeds_km_s': {}, 'reasons': ['GEOMETRY_NOT_EXPOSED']}
            d = copy.deepcopy(base); nonconv(d); return d
        evx = mod.evaluate_envelopes(forward_ngc=fwd, points=W.sel['points'], spec=W.fs['spec'], query_ids=QIDS, budget=100)
        check('S2:valid_false_with_rows_is_member_invalid_not_refusal_in_' + lab,
              evx.get('ok') and evx['n_member_valid'] == 0, [evx.get('ok'), (evx.get('reasons') or [])[:2]])
    # one member with a non-finite valid row while others are fine -> whole evaluation refuses
    n = [0]
    def one_bad(theta):
        if any(theta[k] != v for k, v in W.ngc_trial.items()):
            return {'valid': False, 'speeds_km_s': {}, 'reasons': ['GEOMETRY_NOT_EXPOSED']}
        d = v010_result([100.0 + 0.5 * j for j in range(43)], {0: ('QUERY_INSIDE_INNERMOST_NODE',None),1: ('QUERY_INSIDE_INNERMOST_NODE',None)}); n[0] += 1
        if n[0] == 3:
            d['rows'][9]['speed_km_s'] = None; d['speeds_km_s'][QIDS[9]] = None
        return d
    evb = F.evaluate_envelopes(forward_ngc=one_bad, points=W.sel['points'], spec=W.fs['spec'], query_ids=QIDS, budget=100, row_registration_roster=W.default_root_pins['BR_A_F10_PRIMARY'])
    check('S2:single_nonfinite_valid_row_in_one_member_refuses_freeze', not evb.get('ok'), (evb.get('reasons') or [])[:2])
    # raw result target fields / aliases
    for key in ('target_rows', 'targetSpeed', 'observed_v', 'VOBS', 'Target-Velocities', 'vobs_kms'):
        probe_eval(F, 'S2:raw_result_target_key_refused_' + key, lambda d, key=key: d['uv_tail'].__setitem__(key, [1.0]), False)
    probe_eval(F, 'S2:raw_row_target_key_refused', lambda d: d['rows'][3].__setitem__('observed_speed_km_s', 1.0), False)

    # ================= S4 BLOCKING probe: registered-INVALID Q01/Q02 emitted as finite valid values (GL10-style repair)
    def repaired(theta):
        return {}          # Q01/Q02 valid and finite in every member: the slots V002 GL4 roster is not consulted
    r4 = pipeline(F, 'S4_Q01_Q02_finite_valid', repaired)
    ok4 = r4.get('w', {}).get('ok') and r4['vf'].get('ok')
    check('S4:FINDING_freeze_accepts_finite_valid_Q01_Q02_despite_slots_V002_INVALID_roster', ok4,
          [r4['ev'].get('reasons'), r4.get('w', {}).get('reasons')], expect_finding=True)
    if ok4:
        doc4 = r4['doc']
        # targets placed on the predicted Q01/Q02 values (synthetic): the registered-INVALID rows now count as hits
        t4 = make_targets(doc4, r4['folder'])
        ref_id = doc4['reference_member']['member_id']
        refm = next(m for m in doc4['members'] if m['member_id'] == ref_id)
        t4b = copy.deepcopy(t4)
        for j in (0, 1):
            t4b[j]['velocity'] = refm['speeds_km_s'][j]
        tp = r4['folder'] / 'RVW_SYNTHETIC_TARGET_ROWS_Q01Q02_ON_PREDICTION.json'
        write_x(tp, t4b)
        t4b = json.loads(tp.read_bytes())
        s4 = score(F, r4, t4b)
        refs = next(m for m in s4.get('members', []) if m['member_id'] == ref_id) if s4.get('ok') else None
        check('S4:FINDING_registered_INVALID_rows_score_as_HIT',
              refs is not None and all(refs['rows'][j]['score_status'] == 'HIT' for j in (0, 1)),
              None if refs is None else [refs['rows'][j]['score_status'] for j in (0, 1)], expect_finding=True)
        summary['S4'] = {'notes_slots_source_pinned_in_inputs': str(SLOTS) in [p['path'] for p in doc4['pins']['input_files']],
                         'q01_q02_status': None if refs is None else [refs['rows'][j]['status'] for j in (0, 1)]}

    # ================= S5 GL10 / alternatives
    def alt_with(status, name='GL10_SOURCE_GAUSS_ORDER', primary=None):
        a = copy.deepcopy(W.slots['alternatives'])
        for e in a['declared']:
            if e['name'] == 'GL10_SOURCE_GAUSS_ORDER':
                e['status'] = status
                e['name'] = name
        if primary:
            a['primary'] = primary
        return a
    gl4only = lambda th: {0: ('QUERY_INSIDE_INNERMOST_NODE', None), 1: ('QUERY_INSIDE_INNERMOST_NODE', None)}
    r5 = pipeline(F, 'S5_gl10_evaluated', gl4only, alternatives=alt_with('EVALUATED_BEFORE_FREEZE'))
    check('S5:GL10_marked_EVALUATED_refused', not r5.get('w', {}).get('ok', False), (r5.get('w') or {}).get('reasons', [])[:2])
    r5b = pipeline(F, 'S5_gl10_lowercase_evaluated', gl4only, alternatives=alt_with('EVALUATED_BEFORE_FREEZE', name='gl10_source_gauss_order'))
    gl10r = lambda r: (not r.get('w', {}).get('ok', False)) and any('GL10' in x or 'primary' in x.lower() for x in (r.get('w') or {}).get('reasons', []))
    check('S5:GL10_marked_EVALUATED_refused_for_GL10_reason', gl10r(r5), (r5.get('w') or {}).get('reasons', [])[:2])
    check('S5:GL10_lowercase_EVALUATED_refused', gl10r(r5b), (r5b.get('w') or {}).get('reasons', [])[:2])
    r5c = pipeline(F, 'S5_gl10_primary', gl4only, alternatives=alt_with('NOT_EVALUATED_BEFORE_FREEZE', primary='GL10_SOURCE_GAUSS_ORDER'))
    check('S5:GL10_as_primary_refused', gl10r(r5c), (r5c.get('w') or {}).get('reasons', [])[:2])
    r5d = pipeline(F, 'S5_gl10_renamed_evaluated', gl4only, alternatives=alt_with('EVALUATED_BEFORE_FREEZE', name='SOURCE_GAUSS_ORDER_10'))
    check('S5:NOTE_GL10_guard_is_name_prefix_only_renamed_alternative_accepted', r5d.get('w', {}).get('ok', False),
          (r5d.get('w') or {}).get('reasons', [])[:2], expect_finding=True)
    if r5d.get('w', {}).get('ok'):
        t5 = make_targets(r5d['doc'], r5d['folder'])
        s5 = score(F, r5d, t5)
        alts = {a['name']: a for a in s5.get('alternatives', [])}
        check('S5:renamed_alternative_still_non_headline', s5.get('ok') and not alts['SOURCE_GAUSS_ORDER_10'].get('headline'))
    # pre-existing D9 behaviour in v003d for comparison
    rd5 = pipeline(D, 'S5_gl10_evaluated_v003d', gl4only, alternatives=alt_with('EVALUATED_BEFORE_FREEZE'), write=True)
    check('S5:v003d_cannot_reach_writer_under_GL4_anyway', not rd5.get('w', {}).get('ok', False) and 'w' not in rd5, [(rd5.get('ref') or rd5['ev']).get('reasons', [])[:1]])

    # ================= S6 all-INVALID member is reference-eligible (vacuous D1)
    def nearest_all_invalid(theta):
        if is_pt(theta, nearest_theta):
            return {j: ('QUERY_INSIDE_INNERMOST_NODE', None) for j in range(43)}
        return {0: ('QUERY_INSIDE_INNERMOST_NODE', None), 1: ('QUERY_INSIDE_INNERMOST_NODE', None)}
    r6 = pipeline(F, 'S6_nearest_member_all_INVALID', nearest_all_invalid)
    ok6 = r6.get('w', {}).get('ok')
    check('S6:NOTE_member_with_zero_finite_rows_selected_as_reference',
          ok6 and r6['doc']['reference_member']['log_index'] == summary['nearest_log_index'],
          [ok6, (r6.get('w') or {}).get('reasons', [])[:2]], expect_finding=True)
    if ok6:
        t6 = make_targets(r6['doc'], r6['folder'])
        s6 = score(F, r6, t6)
        check('S6:all_INVALID_reference_scores_0_of_43', s6.get('ok') and s6['headline']['reference_within_error_count'] == 0
              and s6['headline']['n_rows'] == 43)

    # ================= S7 sensitivity summary unit (own entries)
    ref = {'row_valid': [False, True, False], 'speeds_km_s': [None, 100.0, None]}
    reg = {'status': 'INVALID', 'reason': 'QUERY_INSIDE_INNERMOST_NODE', 'registration': None}
    e1 = {'skipped_zero_displacement': False, 'evaluated': True, 'row_valid': [True, True, False], 'speeds_km_s': [90.0, 101.0, None],
          'row_registration': [None, None, reg], 'kind': 'k', 'target': 'a'}
    e2 = {'skipped_zero_displacement': False, 'evaluated': True, 'row_valid': [False, True, False], 'speeds_km_s': [None, 99.0, None],
          'row_registration': [reg, None, reg], 'kind': 'k', 'target': 'b'}
    pq, _pt = F._sensitivity_summary(ref, [e1, e2], ['x', 'y', 'z'])
    check('S7:sens_row_ref_INVALID_band_from_finite_entry', pq[0]['valid'] and pq[0]['box_limited_band_low_km_s'] == 90.0 and pq[0]['box_limited_band_high_km_s'] == 90.0, pq[0])
    check('S7:sens_row_all_finite', pq[1]['valid'] and pq[1]['box_limited_band_low_km_s'] == 99.0 and pq[1]['box_limited_band_high_km_s'] == 101.0)
    check('S7:sens_row_all_INVALID_no_band', not pq[2]['valid'] and pq[2]['box_limited_band_low_km_s'] is None)
    e3 = dict(e2, evaluated=True, row_valid=[False, False, False], speeds_km_s=[None, None, None], row_registration=[None, None, None])
    pq3, _ = F._sensitivity_summary(ref, [e1, e3], ['x', 'y', 'z'])
    check('S7:sens_unregistered_failed_entry_invalidates_row', not pq3[1]['valid'])

    extra_0531()
    extra_0545_0548()

    # ---------------------------------------------------------- report
    report = {'label': 'TESTED_SYNTHETIC_ONLY', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'run_dir': str(RUN), 'n_checks': len(TESTS), 'n_passed': sum(t['passed'] for t in TESTS),
              'n_findings_demonstrated': sum(1 for t in TESTS if t['passed'] and t['demonstrates_finding']),
              'checks': TESTS, 'summary': summary,
              'module_pins_from_bytes': {str(p): sha_file(p) for p in PINS},
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'reads_outside_run_dir': sorted(p for p in READS if not p.startswith(str(RUN))
                                             and not p.startswith(sys.base_prefix) and 'site-packages' not in p),
              'denied': DENIED, 'real_targets_opened': False, 'launches': 0}
    write_x(RUN / 'REVIEW_RESULTS.json', report)
    print(json.dumps({k: report[k] for k in ('run_dir', 'n_checks', 'n_passed', 'n_findings_demonstrated', 'denied')}))


# Inserted before the independent reviewer's main() call. Original functions,
# fixtures and oracles remain in the copied source; authority is supplied here.
_old_pipeline = pipeline
_old_score = score
_old_probe_eval = probe_eval
_old_check = check
ORIGINAL_CHECK_NAMES = [t['name'] for t in json.loads(ORIGINAL_RESULTS.read_bytes())['checks']]
INVERTED_0531 = {
    'S0:both_freeze',
    'S2:baseline_all_valid_ok',
    'S2:FINDING_gate_string_fields_substring_match_accepted',
    'S2:FINDING_builtin_innermost_reason_accepted_on_mid_row_Q20',
    'S2:FINDING_builtin_innermost_reason_accepted_on_outer_Q43',
    'S2:valid_false_with_rows_refuses_entire_evaluation_in_v003e',
    'S4:FINDING_freeze_accepts_finite_valid_Q01_Q02_despite_slots_V002_INVALID_roster',
    'S5:NOTE_GL10_guard_is_name_prefix_only_renamed_alternative_accepted',
    'S6:NOTE_member_with_zero_finite_rows_selected_as_reference',
}
def check(name, cond, evidence=None, expect_finding=False):
    changed = name in INVERTED_0531
    if changed:
        cond = not cond
        evidence = {'0531_expectation': 'original finding/behavior is now refused or restored', 'original_evidence': evidence}
        expect_finding = False
    _old_check(name, cond, evidence, expect_finding)
    TESTS[-1]['expectation_changed_by_0531'] = changed or name == 'S3:score_signature_has_no_registration_or_gate_input'

def root_rosters(folder, gates=None, cut=None):
    folder.mkdir(exist_ok=True)
    pins = {}
    for index, alternative in enumerate(W.slots['alternatives']['declared']):
        doc = {'schema': W.F.ROW_ROSTER_SCHEMA, 'scope': 'SYNTHETIC_FIXTURE', 'alternative': copy.deepcopy(alternative),
               'slots': {'path': str(SLOTS), 'sha256': PINS[SLOTS]},
               'query_manifest': {'path': W.qm, 'sha256': sha_file(W.qm)},
               'query_mapping': [{'query_id': q, 'slots_query_id': s['query_id']} for q, s in zip(QIDS, W.slots['query_block']['rows'])],
               'root_gates': list(W.root_gatepins if gates is None else gates),
               'outer_cut': {'mode': 'NONE'} if cut is None else cut}
        p = folder / ('ROOT_ROSTER_%02d.json' % index)
        write_x(p, doc)
        pins[alternative['name']] = {'path': str(p), 'sha256': sha_file(p)}
    return pins

def pipeline(F, label, pattern, alternatives=None, extra_inputs=(), alt_pattern=None, write=True):
    if F is not W.F:
        baseline_alternatives=copy.deepcopy(alternatives or W.slots['alternatives'])
        baseline_alternatives['declared']=[a for a in baseline_alternatives['declared'] if a['name']!='STAGE0_GRID_OUTER']
        return _old_pipeline(F,label,pattern,baseline_alternatives,extra_inputs,alt_pattern,write)
    folder=RUN/label;folder.mkdir();raw=folder/'raw';raw.mkdir();saved=[]
    root_pins=root_rosters(folder/'root_authority');W.last_root_pins=root_pins
    fwd=make_forward(pattern,0.,raw,saved);afwd=make_forward(alt_pattern or pattern,6.5,raw,saved)
    ev=F.evaluate_envelopes(forward_ngc=fwd,points=W.sel['points'],spec=W.fs['spec'],query_ids=QIDS,budget=100,
        row_registration_roster=root_pins['BR_A_F10_PRIMARY'])
    alt=F.evaluate_envelopes(forward_ngc=afwd,points=W.sel['points'],spec=W.fs['spec'],query_ids=QIDS,budget=100,
        row_registration_roster=root_pins['ORIGINAL_K'])
    res={'ev':ev,'alt':alt,'folder':folder,'root_pins':root_pins}
    if not(ev.get('ok') and alt.get('ok')):return res
    ref=F.select_reference_member(selection=W.sel,evaluation=ev);res['ref']=ref
    if not ref.get('ok'):return res
    sens=F.evaluate_sensitivity(forward_ngc=fwd,reference=ref,selection=W.sel,spec=W.fs['spec'],query_ids=QIDS,
        null_direction_rule={'mode':'box_ends'},budget=100,row_registration_roster=root_pins['BR_A_F10_PRIMARY']);res['sens']=sens
    if not write:return res
    alts=alternatives or copy.deepcopy(W.slots['alternatives']);evs={'BR_A_F10_PRIMARY':ev,'ORIGINAL_K':alt}
    for a in alts['declared']:
        if a['status']=='EVALUATED_BEFORE_FREEZE' and a['name'] not in evs:evs[a['name']]=alt
    notes=copy.deepcopy(W.notes);notes['raw_result_custody']=[{'path':p,'sha256':sha_file(p)} for p in saved]
    w=F.write_freeze_manifest(out_path=str(folder/'FREEZE_MANIFEST.json'),registration_path=str(folder/'FREEZE_REGISTRATION.json'),
        parameter_region={'description':'review synthetic trial box','bounds_semantics':'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'},
        observation_rule={'rule':'review synthetic closed rectangle'},spec=W.fs['spec'],selection=W.sel,
        alternatives=alts,alternative_evaluations=evs,reference=ref,sensitivity=sens,query_ids=QIDS,
        query_manifest={'path':W.qm,'sha256':sha_file(W.qm),'role':'SYNTHETIC_FIXTURE'},
        code_files=[F.__file__,str(ENGINE),str(Path(__file__).resolve())],input_files=[W.region,W.qm,W.rec['record_path'],str(SLOTS)]+saved+list(extra_inputs),
        notes=notes,allow_incomplete=False,row_registration_rosters=root_pins)
    res['w']=w
    if not w.get('ok'):return res
    logged={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_file_sha256':w['manifest_file_sha256'],
        'registration_file_sha256':w['registration_file_sha256'],'targets_opened':False}
    write_x(folder/'PRE_TARGET_LOG.json',logged);res['logged']=logged
    res['vf']=F.verify_freeze_manifest(freeze_manifest_path=w['path']);res['vr']=F.verify_registration(registration_path=w['registration_path'])
    res['doc']=json.loads(Path(w['path']).read_bytes())
    if label=='S1_gl4_v003e':W.good=res
    return res

def score(F,res,targets,expected=None):
    if F is not W.F:return _old_score(F,res,targets,expected)
    return F.score_after_freeze(freeze_manifest_path=res['w']['path'],registration_path=res['w']['registration_path'],
        expected_manifest_file_sha256=expected or res['logged']['manifest_file_sha256'],target_rows=targets,row_registration_rosters=res['root_pins'])

def probe_eval(F,label,mutate,expect_ok,finding=False,note=None):
    if F is not W.F:return _old_probe_eval(F,label,mutate,expect_ok,finding,note)
    folder=RUN/('PROBE_%03d'%len(TESTS));folder.mkdir();pins=root_rosters(folder)
    base=v010_result([100.+.5*j for j in range(43)],{} if label=='S2:baseline_all_valid_ok' else {
        0:('QUERY_INSIDE_INNERMOST_NODE',None),1:('QUERY_INSIDE_INNERMOST_NODE',None)})
    if label=='S2:invalid_roster_missing_refused':base['invalid_rows'].remove(QIDS[0])
    def fwd(theta):
        d=copy.deepcopy(base);mutate(d);return d
    ev=F.evaluate_envelopes(forward_ngc=fwd,points=W.sel['points'],spec=W.fs['spec'],query_ids=QIDS,budget=100,
        row_registration_roster=pins['BR_A_F10_PRIMARY'])
    ok=bool(ev.get('ok'));check(label,ok==expect_ok,{'ok':ok,'reasons':ev.get('reasons',[])[:3],'note':note},finding)
    return ev

def extra_0531():
    F=W.F
    def extra(name,condition,evidence=None):check('0531:'+name,condition,evidence)
    extra('N1_module_stamp',F.MODULE_NAME=='prediction_freeze_c2v003g_cx3v001')
    good=getattr(W,'good',None)
    extra('GL4_good_pipeline_available',bool(good and good.get('w',{}).get('ok')),None if good is None else good.get('w'))
    gl4={0:('QUERY_INSIDE_INNERMOST_NODE',None),1:('QUERY_INSIDE_INNERMOST_NODE',None)}
    def result(theta):return v010_result([100.+j for j in range(43)],gl4)
    def ev(label,forward=result,pins=None,budget=100):
        folder=RUN/('EXTRA_'+label);folder.mkdir()
        pins=pins or root_rosters(folder)
        return F.evaluate_envelopes(forward_ngc=forward,points=W.sel['points'],spec=W.fs['spec'],query_ids=QIDS,budget=budget,
            row_registration_roster=pins['BR_A_F10_PRIMARY'])
    # Contradictions remain refusals under an outer false flag, including map-only reports.
    for label,rows in [('false_rows',True),('false_map_only',False)]:
        def bad(theta,rows=rows):
            r=result(theta);r['valid']=False;r['speeds_km_s'][QIDS[0]]=100.
            if rows:r['rows'][0]['speed_km_s']=100.
            else:r.pop('rows')
            return r
        extra('B1_finite_roster_INVALID_'+label,not ev(label,bad).get('ok'))
    def failed(theta):
        r=result(theta);r['valid']=False;r['status']='NOT_CONVERGED';r['route_a_outcome']={};r.pop('uv_tail')
        r['rows'][5]['speed_km_s']=None;r['speeds_km_s'][QIDS[5]]=None
        return r
    failure=ev('ordinary_failure',failed)
    extra('S4_failed_member_continues_excluded_D1_and_band',failure.get('ok') and failure['n_member_valid']==0 and all(not x['valid'] for x in failure['pointwise_envelope']) and not F.select_reference_member(selection=W.sel,evaluation=failure).get('ok'))
    # S4: genuinely failed members may have no rows or a partial diagnostic
    # subset. Such values never enter frozen prediction arrays, D1 or bands.
    failed_cases = {
        'absent_rows_and_map': {'valid': False, 'status': 'NOT_CONVERGED'},
        'empty_rows': {'valid': False, 'rows': [], 'speeds_km_s': {}},
        'partial_valid_null': {'valid': False, 'rows': [{'id': QIDS[5], 'valid': True, 'speed_km_s': None}]},
        'partial_valid_finite': {'valid': False, 'rows': [{'id': QIDS[5], 'valid': True, 'speed_km_s': 105.}]},
        'mandatory_valid_null_diagnostic': {'valid': False, 'rows': [{'id': QIDS[0], 'valid': True, 'speed_km_s': None}]},
        'partial_registered_INVALID': {'valid': False, 'rows': [{'id': QIDS[0], 'valid': False, 'speed_km_s': None, 'reason': 'QUERY_INSIDE_INNERMOST_NODE'}]},
    }
    for label, raw in failed_cases.items():
        failed_ev = ev('failed_'+label, lambda th, raw=raw: copy.deepcopy(raw))
        ok = failed_ev.get('ok') and failed_ev['n_member_valid'] == 0 and failed_ev['n_member_invalid'] == len(failed_ev['members'])
        ok = ok and all(not any(m['row_valid']) and all(v is None for v in m['speeds_km_s']) for m in failed_ev['members'])
        ok = ok and all(not r['valid'] for r in failed_ev['pointwise_envelope'])
        ok = ok and not F.select_reference_member(selection=W.sel, evaluation=failed_ev).get('ok')
        extra('S4_failed_member_'+label+'_continues_without_predictions', ok, failed_ev.get('reasons'))
    failures = {
        'partial_finite_mandatory_INVALID': {'valid': False, 'rows': [{'id': QIDS[0], 'valid': False, 'speed_km_s': 101., 'reason': 'QUERY_INSIDE_INNERMOST_NODE'}]},
        'partial_finite_declared_INVALID': {'valid': False, 'rows': [{'id': QIDS[5], 'valid': False, 'speed_km_s': 101., 'reason': 'RVW_SYNTH_ROW_GATE'}]},
        'partial_unregistered_INVALID': {'valid': False, 'rows': [{'id': QIDS[5], 'valid': False, 'speed_km_s': None, 'reason': 'NO_ROOT_AUTHORITY'}]},
        'partial_target_field': {'valid': False, 'rows': [{'id': QIDS[5], 'valid': True, 'speed_km_s': None, 'observed_velocity': 100.}]},
    }
    for label, raw in failures.items():
        refusal = ev('failed_'+label, lambda th, raw=raw: copy.deepcopy(raw))
        extra('S4_failed_member_'+label+'_refused', not refusal.get('ok'), refusal.get('reasons'))
    missing_root = F.evaluate_envelopes(forward_ngc=lambda th: {'valid': False}, points=W.sel['points'], spec=W.fs['spec'], query_ids=QIDS, budget=100)
    extra('B1_failed_member_still_requires_external_root_pin', not missing_root.get('ok'), missing_root.get('reasons'))
    # A partial member failure must not void other members' finite bands or D1.
    calls = [0]
    def mixed_failure(th):
        calls[0] += 1
        return {'valid': False, 'rows': []} if calls[0] == 1 else result(th)
    mixed = ev('mixed_partial_failure', mixed_failure)
    extra('S4_partial_failure_excluded_while_other_members_define_D1_bands', mixed.get('ok') and mixed['n_member_invalid'] == 1 and mixed['n_member_valid'] > 0 and all(r['valid'] for r in mixed['pointwise_envelope'][2:]) and F.select_reference_member(selection=W.sel, evaluation=mixed).get('ok'))
    # An unauthorized producer gate must remain unauthorized even if self-declared REGISTERED.
    unauthorized=gate_file('UNAUTHORIZED_NEW',['CX3_PRIVATE_REASON'],[QIDS[10]])
    def unlisted(theta):
        r=result(theta);invalidate(r,10,'CX3_PRIVATE_REASON',gate=unauthorized);return r
    extra('S2_unlisted_producer_gate_refused',not ev('unlisted',unlisted).get('ok'))
    # Put malformed fields inside the root roster, so S3 is exercised directly.
    malformed=gate_file('ROOT_STRING_FIELDS','LONG_REASON',''.join(QIDS))
    folder=RUN/'EXTRA_bad_root_gate';folder.mkdir();pins=root_rosters(folder,[malformed])
    extra('S3_root_listed_gate_strings_refused',not ev('bad_root_gate_eval',pins=pins).get('ok'))
    malformed2=gate_file('ROOT_MIXED_FIELDS',['GOOD',True],QIDS)
    folder=RUN/'EXTRA_bad_root_gate2';folder.mkdir();pins=root_rosters(folder,[malformed2])
    extra('S3_root_listed_gate_mixed_types_refused',not ev('bad_root_gate_eval2',pins=pins).get('ok'))
    # Empty registered-valid set is not eligible even with genuinely root-listed permissions.
    def allinvalid(theta):
        inv=dict(gl4);inv.update({j:('RVW_SYNTH_ROW_GATE',W.root_gatepins[1]) for j in range(2,43)})
        return v010_result([100.+j for j in range(43)],inv)
    empty=ev('empty_valid',allinvalid)
    extra('N2_all_registered_INVALID_refused',not empty.get('ok'),empty.get('reasons'))
    # Root cut is selected by exact theta; no producer hint participates.
    cutfile=RUN/'ROOT_SYNTHETIC_CERTIFIED_CUT.json'
    write_x(cutfile,{'schema':'NGC_CANDIDATE_ROSTER_CUT_CX3V001','first_unconfined_R_kpc':20.,'confinement_status':'CERTIFIED_UNCONFINED',
        'classification_evidence':{'synthetic_only':True},'dropped_HI_mass_fraction':.01,'full_roster_digest':stub('full'),'kept_roster_digest':stub('kept'),'controls_sha256':stub('controls')})
    cp={'path':str(cutfile),'sha256':sha_file(cutfile)}
    S=F._spec_from(W.fs['spec'],[])
    theta=F._theta_ngc_from_engine(S,W.sel['points'][0]['theta_natural'])
    contexts=[{'theta_ngc':theta,'cut':cp}]
    folder=RUN/'EXTRA_cut_authority';folder.mkdir();pins=root_rosters(folder,cut={'mode':'PER_THETA','contexts':contexts})
    def cut_result(th):
        inv=dict(gl4)
        geom=json.loads(Path(F.REGISTERED_GL_NODES_PATH).read_bytes());kpc=geom['kpc_m']
        last=max(r for r in geom['orders']['4']['radii_m'] if r < 20.*kpc)
        for j in range(43):
            radius=.55*(j+1)*kpc
            if radius>=20.*kpc:inv[j]=('QUERY_BEYOND_OUTER_GAS_CUT',None)
            elif radius>last:inv[j]=('QUERY_OUTSIDE_RETAINED_SUPPORT',None)
        return v010_result([100.+j for j in range(43)],inv)
    cutgood=ev('cut_exact',cut_result,pins,budget=1)
    extra('B1_outer_cut_exact_theta_and_pinned_radius',cutgood.get('ok') and cutgood['members'][0]['member_valid'],cutgood.get('reasons'))
    extra('B1_outer_cut_missing_theta_refused',not ev('cut_missing_theta',cut_result,pins,budget=2).get('ok'))
    extra('B1_outer_cut_finite_row_refused',not ev('cut_finite',result,pins,budget=1).get('ok'))
    folder=RUN/'EXTRA_cut_ambiguous_authority';folder.mkdir();badpins=root_rosters(folder,cut={'mode':'PER_THETA','contexts':contexts+contexts})
    extra('B1_outer_cut_ambiguous_theta_refused',not ev('cut_ambiguous',cut_result,badpins,budget=1).get('ok'))
    if good and good.get('w',{}).get('ok'):
        doc=good['doc'];t=json.loads((good['folder']/'RVW_SYNTHETIC_TARGET_ROWS.json').read_bytes())
        args=dict(freeze_manifest_path=good['w']['path'],registration_path=good['w']['registration_path'],expected_manifest_file_sha256=good['logged']['manifest_file_sha256'],target_rows=t)
        extra('B1_scorer_requires_external_root_pins',not F.score_after_freeze(**args).get('ok'))
        folder=RUN/'EXTRA_wrong_authority';folder.mkdir();other=root_rosters(folder)
        extra('B1_scorer_refuses_different_external_roster',not F.score_after_freeze(**args,row_registration_rosters=other).get('ok'))
        extra('B1_manifest_records_all_alternative_root_pins',doc['row_registration_rosters']==good['root_pins'])
        extra('S1_first_two_rows_always_registered_INVALID',all(m['row_registration'][0]['reason']=='QUERY_INSIDE_INNERMOST_NODE' and m['row_registration'][1]['reason']=='QUERY_INSIDE_INNERMOST_NODE' for m in doc['members']))
        # Rehashed copies cannot omit the root binding or repair mandatory INVALID rows.
        forged=copy.deepcopy(doc);forged.pop('row_registration_rosters');p=RUN/'FORGED_MISSING_ROOT_ROSTER.json';write_x(p,rehash_manifest(F,forged))
        extra('B1_verifier_refuses_missing_root_binding',not F.verify_freeze_manifest(freeze_manifest_path=str(p)).get('ok'))
        # Preserve all-valid LADDER arithmetic as a unit regression, without allowing
        # an all-valid GL4 public freeze. The full reviewer S0 now must refuse.
        D=load(V003D,'cx3_regression_d')
        for j in range(43):
            a=F._ladder_row(QIDS[j],100.+j,True,101.+j,1.5);b=D._ladder_row(QIDS[j],100.+j,True,101.+j,1.5)
            assert a==b
        extra('S0_arithmetic_regression_43_valid_LADDER_rows',True)
        fm=doc['members'][0]
        # Registered-valid rows in the actual frozen member use exactly v003d LADDER arithmetic.
        scored=score(F,good,t);sm=scored['members'][0]
        same=True
        for j in range(43):
            if fm['row_valid'][j]:
                baseline=D._ladder_row(QIDS[j],fm['speeds_km_s'][j],True,t[j]['velocity'],t[j]['sigma'])
                same=same and all(sm['rows'][j][k]==v for k,v in baseline.items() if k!='row_notes')
        extra('S0_arithmetic_regression_roster_valid_rows',same)
    # 0535 F1/F2: reproduce registered geometry independently from profile bytes.
    import numpy as np
    geom=json.loads(Path(F.REGISTERED_GL_NODES_PATH).read_bytes());kpc=geom['kpc_m']
    profile=json.loads(Path(geom['sources']['profile']['path']).read_bytes())['galaxies']['NGC3198']['HI_plus_He']
    kernel=load(Path(geom['sources']['radial_kernel']['path']),'cx3_independent_radial_kernel')
    for order,count in ((4,100),(10,250)):
        x,w=np.polynomial.legendre.leggauss(order);radii=[]
        edges=profile['s_edges_kpc2']
        for lo,hi in zip(edges[:-1],edges[1:]):
            for gx in x:
                radius=float(np.sqrt((lo+hi)/2+(hi-lo)*gx/2)*kpc)
                sigma=kernel.annular_bernstein_sigma(s_edges=edges,annular_means=profile['annular_means_Msun_pc2'],
                    boundary_controls=profile['boundary_controls_Msun_pc2'],s_query=[float((radius/kpc)**2)])
                assert sigma['ok']
                if float(sigma['sigma'][0])!=0:radii.append(radius)
        extra('0535_registered_GL%d_all_nodes_bitwise_independent'%order,np.array_equal(np.asarray(radii[:count]),np.asarray(geom['orders'][str(order)]['radii_m'])))
    loaded=F._load_row_roster(pins['BR_A_F10_PRIMARY'],QIDS,True)
    derived=F._row_contract(loaded,theta)
    last=max(r for r in geom['orders']['4']['radii_m'] if r<20.*kpc)
    outer=[q for j,q in enumerate(QIDS) if .55*(j+1)*kpc>=20.*kpc]
    gaps=[q for j,q in enumerate(QIDS) if last<.55*(j+1)*kpc<20.*kpc]
    extra('0535_F1_outer_exact_pinned_cut_set',set(q for q,v in derived.items() if v['reason']=='QUERY_BEYOND_OUTER_GAS_CUT')==set(outer),outer)
    extra('0535_F2_gap_exact_registered_node_set',bool(gaps) and set(q for q,v in derived.items() if v['reason']=='QUERY_OUTSIDE_RETAINED_SUPPORT')==set(gaps),gaps)
    def gap_finite(th):
        r=cut_result(th);j=QIDS.index(gaps[0]);r['rows'][j]={'id':QIDS[j],'valid':True,'speed_km_s':100.};r['speeds_km_s'][QIDS[j]]=100.;r['invalid_rows'].remove(QIDS[j]);return r
    extra('0535_F2_finite_gap_refused',not ev('gap_finite',gap_finite,pins,budget=1).get('ok'))
    def wrong_outer(th):
        r=cut_result(th);j=QIDS.index(gaps[0]);r['rows'][j]['reason']='QUERY_BEYOND_OUTER_GAS_CUT';return r
    extra('0535_F1_outer_reason_below_cut_refused',not ev('wrong_outer',wrong_outer,pins,budget=1).get('ok'))
    def wrong_gap(th):
        r=cut_result(th);j=QIDS.index(outer[0]);r['rows'][j]['reason']='QUERY_OUTSIDE_RETAINED_SUPPORT';return r
    extra('0535_F2_gap_reason_at_or_above_cut_refused',not ev('wrong_gap',wrong_gap,pins,budget=1).get('ok'))
    edge=copy.deepcopy(loaded)
    edge['radii'][QIDS[3]]=last/kpc;edge['radii'][QIDS[4]]=20.;edge['radii'][QIDS[5]]=math.nextafter(last/kpc,math.inf)
    ed=F._row_contract(edge,theta)
    extra('0535_F1_F2_equal_cut_outer_equal_last_node_valid',QIDS[3] not in ed and ed[QIDS[4]]['reason']=='QUERY_BEYOND_OUTER_GAS_CUT' and ed[QIDS[5]]['reason']=='QUERY_OUTSIDE_RETAINED_SUPPORT')
    overlap=copy.deepcopy(loaded);overlap['radii'][QIDS[0]]=20.;overlap['radii'][QIDS[1]]=20.1
    over=F._row_contract(overlap,theta)
    extra('0535_F1_outer_overrides_inner_on_overlap',all(over[q]['reason']=='QUERY_BEYOND_OUTER_GAS_CUT' for q in QIDS[:2]))
    # Use the same root-pinned cut for each exact registered member/sensitivity theta.
    if good and good.get('w',{}).get('ok'):
        all_theta={canon(m['theta_ngc']):m['theta_ngc'] for m in good['doc']['members']+good['doc']['sensitivity']['evaluations']}
        full_context={'mode':'PER_THETA','contexts':[{'theta_ngc':v,'cut':cp} for v in all_theta.values()]}
        original_root_rosters=globals()['root_rosters']
        def cut_rosters(folder,gates=None,cut=None):return original_root_rosters(folder,gates,full_context if cut is None else cut)
        globals()['root_rosters']=cut_rosters
        try:full=pipeline(F,'0535_GAP_FREEZE',lambda th:{j:(row['reason'],None) for j,row in enumerate(cut_result(th)['rows']) if row['valid'] is False})
        finally:globals()['root_rosters']=original_root_rosters
        extra('0535_F1_F2_full_freeze_verifies',full.get('w',{}).get('ok') and full.get('vf',{}).get('ok'),full.get('w',full.get('sens')))
        if full.get('w',{}).get('ok'):
            # Only now, after immutable freeze/registration/log, synthesize targets.
            targets=[{'id':q,'velocity':100.+j,'sigma':2.} for j,q in enumerate(QIDS)]
            target_path=full['folder']/'SYNTHETIC_TARGETS_AFTER_FREEZE.json';write_x(target_path,targets)
            scored=score(F,full,targets)
            expected=set(outer+gaps+QIDS[:2])
            ok=scored.get('ok') and all(m['n_rows']==43 and set(m['invalid_as_miss'])==expected for m in scored['members'])
            extra('0535_F1_F2_all43_scored_gap_and_outer_as_misses',ok,scored.get('reasons'))
            forged=copy.deepcopy(full['doc']);j=QIDS.index(gaps[0]);forged['members'][0]['row_registration'][j]['reason']='QUERY_BEYOND_OUTER_GAS_CUT'
            forged_path=RUN/'FORGED_GAP_REASON.json';write_x(forged_path,rehash_manifest(F,forged))
            extra('0535_F1_F2_rehashed_wrong_gap_reason_refused',not F.verify_freeze_manifest(freeze_manifest_path=str(forged_path)).get('ok'))
            dependency_paths={p['path'] for p in full['doc']['pins']['input_files']}
            extra('0535_registered_nodes_and_sources_pinned_in_manifest',F.REGISTERED_GL_NODES_PATH in dependency_paths and all(p['path'] in dependency_paths for p in geom['sources'].values()))
    extra('0535_headline_names_all_registered_reasons',all(reason in F.HEADLINE_RULE for reason in F.REGISTERED_INVALID_REASONS))
    executed={t['name']:t for t in TESTS}
    mapping=[]
    for name in ORIGINAL_CHECK_NAMES:
        if name in executed:
            mapping.append({'original_name':name,'status':'RERUN_CHANGED_EXPECTATION_0531' if executed[name].get('expectation_changed_by_0531') else 'RERUN_PRESERVED_EXPECTATION',
                'passed':executed[name]['passed'],'replacement_check':name})
        elif name.startswith(('S0:','S4:','S5:renamed_alternative','S6:all_INVALID')):
            # These assertions were downstream of a freeze that 0531 now requires to
            # refuse. The input scenario was run; target access/scoring is unreachable.
            mapping.append({'original_name':name,'status':'SUPERSEDED_DOWNSTREAM_OF_REQUIRED_REFUSAL',
                'passed':True,'replacement_check':'S0:both_freeze' if name.startswith('S0:') else '0531:B1_scorer_requires_external_root_pins',
                'reason':'0531 forbids this all-validGL4, renamedGL10 or allINVALID freeze. Valid-row arithmetic has separate regression checks.'})
        else:
            mapping.append({'original_name':name,'status':'UNACCOUNTED','passed':False})
    extra('all_111_original_checks_accounted_for',len(mapping)==111 and all(x['status']!='UNACCOUNTED' for x in mapping),{'total':len(mapping),'statuses':{s:sum(x['status']==s for x in mapping) for s in sorted(set(x['status'] for x in mapping))}})
    write_x(RUN/'ORIGINAL_111_SCENARIO_MAPPING.json',{'original_result_pin':{'path':str(ORIGINAL_RESULTS),'sha256':sha_file(ORIGINAL_RESULTS)},'mapping':mapping,
        'statement':'Not an unchanged111/111 claim: changed root rulings and unreachable downstream checks are enumerated explicitly.'})



def extra_0545_0548():
    F=W.F;good=W.good
    def chk(name,ok,evidence=None):check('0545_0548:'+name,ok,evidence)
    # Exact set and order, including every NOT_EVALUATED declaration.
    for index,alt in enumerate(W.slots['alternatives']['declared']):
        fewer=copy.deepcopy(W.slots['alternatives']);fewer['declared'].pop(index);reasons=[]
        chk('F1_omit_'+alt['name']+'_refused',F._bind_alternatives(fewer,reasons) is None and bool(reasons),reasons)
    reversed_alts=copy.deepcopy(W.slots['alternatives']);reversed_alts['declared'].reverse();reasons=[]
    chk('F1_reordered_alternatives_refused',F._bind_alternatives(reversed_alts,reasons) is None and bool(reasons))
    chk('F1_full_exact_six_alternatives_preserved',good['doc']['alternatives']==W.slots['alternatives'] and len(good['doc']['alternatives']['declared'])==6)
    original_qm=W.qm
    rawqm=json.loads(Path(original_qm).read_bytes());reversed_qm=copy.deepcopy(rawqm);reversed_qm['rows'].reverse()
    qp=RUN/'REVERSED_QUERY_ROWS.json';write_x(qp,reversed_qm);W.qm=str(qp)
    try:
        folder=RUN/'REVERSED_QUERY_ROOT';pins=root_rosters(folder)
        roster=F._load_row_roster(pins['BR_A_F10_PRIMARY'],QIDS,True)
        byid={r['query_id']:float(r['Rad_text']) for r in rawqm['rows']}
        chk('F2_reversed_file_rows_bind_radii_by_id',roster['radii']==byid)
        cut=copy.deepcopy(roster);cut['cut_mode']='PER_THETA';cut['contexts']=[(canon({'fixture':1}),20.)]
        reference=F._load_row_roster(good['root_pins']['BR_A_F10_PRIMARY'],QIDS,True)
        reference['cut_mode']='PER_THETA';reference['contexts']=[(canon({'fixture':1}),20.)]
        chk('F2_reversed_rows_identical_cut_gap_set',F._row_contract(cut,{'fixture':1})==F._row_contract(reference,{'fixture':1}))
    finally:W.qm=original_qm
    for unit in ('Mpc','pc','m','KPC'):
        bad=copy.deepcopy(rawqm)
        for row in bad['rows']:row['Rad_unit']=unit
        p=RUN/('BAD_UNIT_'+unit+'.json');write_x(p,bad)
        chk('F3_nonregistered_unit_'+unit+'_refused',not F.load_query_manifest(path=str(p),expected_sha256=sha_file(p)).get('ok'))
    # Positive scaling can coalesce adjacent floats: document the metre authority.
    geom=json.loads(Path(F.REGISTERED_GL_NODES_PATH).read_bytes());kpc=geom['kpc_m']
    radii=[float(row['Rad_text']) for row in W.slots['query_block']['rows']]
    ulp_disagreements=[]
    for r in radii:
        if any((r>=cut)!=((r*kpc)>=(cut*kpc)) for cut in (math.nextafter(r,-math.inf),math.nextafter(r,math.inf))):ulp_disagreements.append(r)
    node_disagreements=sum((r>=n/kpc)!=((r*kpc)>=(n/kpc*kpc)) for r in radii for n in geom['orders']['4']['radii_m'])
    chk('F4_metres_ulp_note_demonstrated',len(ulp_disagreements)==8 and node_disagreements==0,{'query_radii_with_ulp_neighbour_difference':ulp_disagreements,'GL4_node_cut_comparison_differences':node_disagreements})
    # Two-pass mechanism: collect target-free raw predictions, register root
    # authority only afterward, then evaluate/freeze from pinned raw replays.
    phase1=RUN/'TWO_PASS_RAW_FIRST';phase1.mkdir();rawpins={};alltheta={canon(m['theta_ngc']):m['theta_ngc'] for m in good['doc']['members']+good['doc']['sensitivity']['evaluations']}
    pattern=lambda th:{0:('QUERY_INSIDE_INNERMOST_NODE',None),1:('QUERY_INSIDE_INNERMOST_NODE',None)}
    for delta in (0.,6.5):
        producer=make_forward(pattern,delta)
        for number,(key,theta) in enumerate(alltheta.items()):
            p=phase1/('RAW_'+str(delta)+'_'+str(number)+'.json');write_x(p,producer(theta));rawpins[delta,key]={'path':str(p),'sha256':sha_file(p)}
    write_x(phase1/'FIRST_PASS_COMPLETE_NO_TARGETS.json',{'raw_pins':list(rawpins.values()),'targets_opened':False,'root_roster_registered':False})
    original_make_forward=globals()['make_forward'];replay_calls=[0]
    def replay_factory(pattern,delta=0.,raw_dir=None,saved=None):
        def replay(theta):
            pinned=rawpins[delta,canon(theta)];assert sha_file(pinned['path'])==pinned['sha256'];obj=json.loads(Path(pinned['path']).read_bytes());replay_calls[0]+=1
            if raw_dir is not None:
                p=raw_dir/('REPLAY_RAW_%03d.json'%len(saved));write_x(p,obj);saved.append(str(p))
            return obj
        return replay
    globals()['make_forward']=replay_factory
    try:replayed=pipeline(F,'TWO_PASS_REGISTER_THEN_REPLAY',pattern)
    finally:globals()['make_forward']=original_make_forward
    chk('F5_saved_raw_then_root_registration_then_replay_freeze',replayed.get('w',{}).get('ok') and replayed.get('vf',{}).get('ok') and replay_calls[0]>0,replayed.get('w',replayed.get('sens')))
    # The currently adopted Stage0 declaration is unscored, non-headline fallback.
    targets=json.loads((good['folder']/'RVW_SYNTHETIC_TARGET_ROWS.json').read_bytes());scored=score(F,good,targets)
    stage=next(a for a in scored['alternatives'] if a['name']=='STAGE0_GRID_OUTER')
    chk('A65_public_stage0_NOT_EVALUATED_nonheadline',scored['ok'] and stage['status']=='NOT_EVALUATED_BEFORE_FREEZE' and stage['scored'] is False and stage['headline'] is False)
    stage_record=next(a for a in W.slots['alternatives']['declared'] if a['name']=='STAGE0_GRID_OUTER')
    stage_roster=F._load_row_roster(good['root_pins']['STAGE0_GRID_OUTER'],QIDS)
    scope=F._alternative_score_scope(stage_record,QIDS,stage_roster)
    chk('A65_exact_outer_query_ids_from_frozen_radii',scope['query_ids']==QIDS[35:] and scope['registered_query_ids']==['NGC3198-Q%02d'%i for i in range(36,44)] and scope['n_rows']==8)
    changed=copy.deepcopy(W.slots['alternatives']);changed['declared'][-1]['status']='EVALUATED_BEFORE_FREEZE';reasons=[]
    chk('A65_producer_stage0_status_flip_refused',F._bind_alternatives(changed,reasons) is None and bool(reasons))
    # Positive subset arithmetic is private unit coverage, not an adopted evaluated
    # Stage0 public freeze. Inner-row values/targets must never enter these counts.
    member=copy.deepcopy(good['doc']['members'][0]);member['row_valid']=[True]*43;member['speeds_km_s']=[100.]*43;member['row_registration']=[None]*43
    bound=[(100.,1.) for _ in QIDS];outer=F._score_members_on_rows([member],QIDS,bound,scope['query_ids'])[0]
    chk('A65_subset_arithmetic_scores_only_eight_outer_rows',outer['n_rows']==8 and outer['within_error_count']==8 and [r['id'] for r in outer['rows']]==QIDS[35:])
    inner_changed=copy.deepcopy(member);inner_changed['speeds_km_s'][:35]=[1e9]*35
    bound_inner=[(-1e9,1.)]*35+bound[35:]
    chk('A65_inner_prediction_and_target_changes_irrelevant',F._score_members_on_rows([inner_changed],QIDS,bound_inner,scope['query_ids'])[0]==outer)
    invalid=copy.deepcopy(member);invalid['row_valid'][35]=False;invalid['speeds_km_s'][35]=None;invalid['row_registration'][35]={'status':'INVALID','reason':'QUERY_OUTSIDE_RETAINED_SUPPORT','registration':None}
    misses=F._score_members_on_rows([invalid],QIDS,bound,scope['query_ids'])[0]
    chk('A65_outer_INVALID_is_miss_in_eight_row_denominator',misses['n_rows']==8 and misses['within_error_count']==7 and misses['invalid_as_miss']==[QIDS[35]])
    chk('A65_stage0_grid_pin_in_manifest',any(p['sha256']==stage_record['coefficient_grid_pin']['sha256'] for p in good['doc']['pins']['input_files']))
    prior_path=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003f/runs/run_20261018T131716816089Z/REVIEW_RESULTS.json');prior=json.loads(prior_path.read_bytes());byname={x['name']:x for x in TESTS}
    mapped=[{'original_name':x['name'],'current_name':x['name'],'status':'RERUN_SAME_EXPECTATION_WITH_SIX_ALTERNATIVES','passed':byname[x['name']]['passed']} for x in prior['checks']]
    chk('all139_prior_checks_rerun',len(mapped)==139 and all(x['passed'] for x in mapped))
    write_x(RUN/'ORIGINAL_139_MAPPING_V001.json',{'prior_result_pin':{'path':str(prior_path),'sha256':sha_file(prior_path)},'mapping':mapped})

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        if RUN is not None:
            try:
                write_x(RUN / 'CRASH.json', {'traceback': traceback.format_exc(), 'checks': TESTS})
            except Exception:
                pass
        raise
