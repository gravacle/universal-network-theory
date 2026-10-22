"""Independent checker fixtures for calibration_freeze_c2_v003/final (engine ec509648..., freeze f670d14b...).

Expectations: check/BLIND_FIXTURE_PLAN.md (b3a04968..., written before any v003 file was opened).
SYNTHETIC ONLY. The only real file opened is the target-free NGC3198 query manifest (a2936517..., ids/radii
only). No NGC3198 velocity, no project forward, no network, single thread. Writes only under
check/runs/run_<UTC>_<pid>/.

usage: python3 -I -B fixtures_check_c2v003.py                 (full suite)
       python3 -I -B fixtures_check_c2v003.py --sub NAME DIR     (one isolated sub-run, used for timeouts)
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
import shutil
import subprocess
import sys
import time
import traceback

import numpy as np

HERE = os.path.dirname(os.path.realpath(__file__))
FINAL = os.path.join(os.path.dirname(HERE), 'final')
ENG_PATH = os.path.join(FINAL, 'calibration_region_engine_c2v003.py')
FRZ_PATH = os.path.join(FINAL, 'prediction_freeze_c2v003.py')
QM_REAL = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
           'CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json')
QM_SHA = 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'
PY = sys.executable


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


E = load(ENG_PATH, 'engine_c2v003_chk')
F = load(FRZ_PATH, 'freeze_c2v003_chk')


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


RESULTS = []


def rec(fid, item, ok, detail):
    RESULTS.append({'id': fid, 'item': item, 'pass': bool(ok), 'detail': detail})
    print('%-4s %-12s %-10s %s' % ('PASS' if ok else 'FAIL', fid, item, json.dumps(detail, default=str)[:300]))


def guard(fid, item, fn):
    try:
        fn()
    except Exception as exc:  # a raise inside a fixture is a FAIL (S10 contract: fail closed)
        rec(fid, item, False, {'raised': '%s: %s' % (type(exc).__name__, exc),
                               'tb': traceback.format_exc()[-1500:]})


# ----------------------------------------------------------------------------------------------------------
# synthetic inputs
# ----------------------------------------------------------------------------------------------------------
ROWS = ['S%02d' % i for i in range(1, 13)]
Z, SIG, MU = 2.865260238532134, 0.7, 28.03
DC = 10 ** ((MU - 25) / 5)


def write_region(path):
    with open(path, 'x') as fh:
        json.dump({'rows': [{'id': r, 'reference_radius_kpc': 0.4 * (i + 1), 'observed_speed_km_s': 100.0,
                             'quoted_random_sigma_km_s': SIG,
                             'conditional_random_acceptance_low_km_s': 100.0 - Z * SIG,
                             'conditional_random_acceptance_high_km_s': 100.0 + Z * SIG}
                            for i, r in enumerate(ROWS)],
                   'statistical_choice': 'checker synthetic', 'forward_coordinates': 'checker synthetic',
                   'distance_summary': {'modulus_mag': MU, 'distance_central_Mpc': DC,
                                        'reported68_low_Mpc': DC * 0.96, 'reported68_high_Mpc': DC * 1.04,
                                        'scope': 'checker synthetic'}}, fh)
    return path


def coords_std():
    return [
        dict(name='a', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.55,
             units='dimensionless', scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='b', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.60,
             units='dimensionless', scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='q', transform='linear', lower=0.0, upper=2.0, role='fixed', trial_value=1.0, units='kpc',
             scope='shared', kind='other', reference_value=None, sensitivity={'mode': 'box_ends'}),
        dict(name='D_ddo', transform='log', lower=DC * 0.96, upper=DC * 1.04, role='nuisance', trial_value=DC,
             units='Mpc', scope='ddo154_nuisance', kind='distance', reference_value=4.04, sensitivity=None),
        dict(name='D_ngc', transform='log', lower=12.0, upper=15.6, role='nuisance', trial_value=13.8,
             units='Mpc', scope='ngc3198_nuisance', kind='distance', reference_value=13.8,
             sensitivity={'mode': 'box_ends'}),
        dict(name='i_ngc', transform='linear', lower=64.0, upper=78.0, role='nuisance', trial_value=71.0,
             units='deg', scope='ngc3198_nuisance', kind='inclination', reference_value=None,
             sensitivity={'mode': 'step', 'step': 4.0}),
    ]


def ddo_std(theta):
    # admitted ellipse around (0.62, 0.66); D_ddo is a weak direction (candidate near-null)
    g = 40.0 * (theta['a'] - 0.62) ** 2 + 60.0 * (theta['b'] - 0.66) ** 2
    return {'speeds_km_s': {r: 100.0 + g + 0.02 * (i - 5.5) * (theta['D_ddo'] / DC - 1.0)
                            for i, r in enumerate(ROWS)}, 'valid': True, 'reasons': []}


NGC_CALLS = []


def make_ngc(ids, bad=None):
    """bad: None or (predicate(theta), action) where action in nan_and_999 / missing / flag_false / raise /
    huge / np_true / str_true / int_one."""
    def fwd(theta):
        NGC_CALLS.append(sorted(theta))
        assert set(theta) == {'a', 'b', 'q', 'D_ngc', 'i_ngc'}, sorted(theta)   # D10
        sp = {q: 150.0 + 30.0 * theta['a'] + 25.0 * theta['b'] * (j + 1) / 43.0 + 3.0 * (theta['q'] - 1.0)
              + 8.0 * (theta['D_ngc'] / 13.8 - 1.0) + 0.15 * (theta['i_ngc'] - 71.0) for j, q in enumerate(ids)}
        res = {'speeds_km_s': sp, 'valid': True, 'reasons': []}
        if bad is not None and bad[0](theta):
            act = bad[1]
            if act == 'nan_and_999':
                sp[ids[4]] = float('nan')
                sp[ids[0]] = 999.0
            elif act == 'missing':
                del sp[ids[10]]
            elif act == 'flag_false':
                res['valid'] = False
            elif act == 'np_true':
                res['valid'] = np.True_
            elif act == 'str_true':
                res['valid'] = 'true'
            elif act == 'int_one':
                res['valid'] = 1
            elif act == 'raise':
                raise RuntimeError('checker forward failure')
            elif act == 'huge':
                for q in ids:
                    sp[q] = 1e307 * (1.0 + theta['a'])
        return res
    return fwd


ENGINE_PARAMS = dict(u_seed=None, budget=500, rel_step=0.05, min_step=1e-4, max_halvings=3, null_tolerance=1e-6,
                     repair_iterations=8, max_repair_step=0.25, march_step=0.05, bisection_steps=4, design_count=8,
                     global_design_count=24, max_march_rounds=4, hull_growth_tol=0.01, rng_seed=1)


def run_engine(forward, engine_coords, region_path, **over):
    kw = dict(ENGINE_PARAMS)
    kw.update(over)
    return E.run_calibration_region(forward=forward, coordinates=engine_coords, observation_region_path=region_path,
                                    observation_region_sha256=sha(region_path),
                                    ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0}, **kw)


ALTS = {'primary': 'CHK_STATE', 'declared': [{'name': 'CHK_STATE', 'kind': 'state', 'description': 'checker primary',
                                              'status': 'EVALUATED_BEFORE_FREEZE'}]}
PREG = {'description': 'checker computational trial box', 'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'}


class Base:
    """One engine run + selection shared by many freeze fixtures (the engine is deterministic)."""

    def __init__(self, d):
        self.d = d
        os.makedirs(d)
        self.region = write_region(os.path.join(d, 'SYNTHETIC_REGION_12ROW_NOT_DDO154.json'))
        qm = F.load_query_manifest(path=QM_REAL, expected_sha256=QM_SHA)
        assert qm['ok'], qm['reasons']
        self.ids = list(qm['query_ids'])
        self.fs = F.make_freeze_coordinate_spec(coordinates=coords_std())
        assert self.fs['ok'], self.fs['reasons']
        self.engine_coords_given = copy.deepcopy(self.fs['engine_coordinates'])
        self.run = run_engine(ddo_std, self.fs['engine_coordinates'], self.region)
        self.rec = E.write_calibration_record(run=self.run, record_path=os.path.join(d, 'CALIBRATION_RECORD.json'),
                                              registry_path=os.path.join(d, 'CALIBRATION_REGISTRY.jsonl'))
        self.sel = F.select_representative_points(exploration=self.run, interior_count=5, spec=self.fs['spec'])
        self.k = 0

    def fresh(self, tag):
        self.k += 1
        p = os.path.join(self.d, 'w%03d_%s' % (self.k, tag))
        os.makedirs(p)
        return p

    def evaluate(self, fwd, points=None, budget=100, ids=None):
        return F.evaluate_envelopes(forward_ngc=fwd, points=(self.sel['points'] if points is None else points),
                                    spec=self.fs['spec'], query_ids=(self.ids if ids is None else ids), budget=budget)

    def freeze(self, tag, ev=None, fwd=None, ids=None, qm=None, input_files=None, code_files=None,
               parameter_region=None, notes=None, allow_incomplete=False, sel=None, sens_fwd=None):
        sel = self.sel if sel is None else sel
        ids = self.ids if ids is None else ids
        fwd = make_ngc(ids) if fwd is None else fwd
        ev = self.evaluate(fwd, points=sel['points'], ids=ids) if ev is None else ev
        ref = F.select_reference_member(selection=sel, evaluation=ev)
        sens = F.evaluate_sensitivity(forward_ngc=(fwd if sens_fwd is None else sens_fwd), reference=ref,
                                      selection=sel, spec=self.fs['spec'], query_ids=ids,
                                      null_direction_rule={'mode': 'box_ends'}, budget=200)
        d = self.fresh(tag)
        qm = {'path': QM_REAL, 'sha256': QM_SHA, 'role': 'PROGRAM_PIN'} if qm is None else qm
        if input_files is None:
            input_files = [self.region, qm['path'], self.rec['record_path']]
        w = F.write_freeze_manifest(
            out_path=os.path.join(d, 'FREEZE_MANIFEST.json'), registration_path=os.path.join(d, 'FREEZE_REGISTRATION.json'),
            parameter_region=(PREG if parameter_region is None else parameter_region),
            observation_rule={'rule': 'closed rectangle (checker synthetic)'}, spec=self.fs['spec'], selection=sel,
            alternatives=ALTS, alternative_evaluations={'CHK_STATE': ev}, reference=ref, sensitivity=sens,
            query_ids=ids, query_manifest=qm, code_files=([FRZ_PATH, ENG_PATH] if code_files is None else code_files),
            input_files=input_files, notes=({'checker': True} if notes is None else notes),
            allow_incomplete=allow_incomplete)
        return {'ev': ev, 'ref': ref, 'sens': sens, 'w': w, 'dir': d}


def targets_from(speeds, ids, sigma=1.0):
    return [{'id': q, 'velocity': float(150.0 if (s is None or not math.isfinite(s)) else s), 'sigma': sigma}
            for q, s in zip(ids, speeds)]


def score(w, targets, expected=None):
    return F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=w['registration_path'],
                                expected_manifest_file_sha256=(w['manifest_file_sha256'] if expected is None else expected),
                                target_rows=targets)


def pick(sel, k):
    p = sel['points'][k]
    a0, b0 = p['theta_natural']['a'], p['theta_natural']['b']
    return (lambda th: abs(th['a'] - a0) < 1e-12 and abs(th['b'] - b0) < 1e-12), p


def rewrite_canonical(path_in, path_out, mutate, rehash=True):
    raw = open(path_in, 'rb').read()
    doc = json.loads(raw)
    mutate(doc)
    if rehash:
        body = {k: v for k, v in doc.items() if k != 'manifest_sha256'}
        doc['manifest_sha256'] = hashlib.sha256(F._canonical_bytes(body)).hexdigest()
    with open(path_out, 'xb') as fh:
        fh.write(F._canonical_bytes(doc))
    return path_out


# ----------------------------------------------------------------------------------------------------------
# fixtures
# ----------------------------------------------------------------------------------------------------------

def fx_base(B):
    ok = (B.run['status'] == 'COMPLETE' and B.rec['ok'] and B.sel['ok'] and len(B.sel['points']) >= 4)
    rec('B-BASE', 'setup', ok, {'engine_status': B.run['status'], 'reasons': B.run['reasons'][:3],
                                'n_admitted': (B.run['exploration'] or {}).get('n_admitted'),
                                'ident': (B.run['identifiability'] or {}).get('identified'),
                                'near_null': (B.run['identifiability'] or {}).get('near_null'),
                                'n_members': len(B.sel['points']), 'sel_reasons': B.sel['reasons'][:3]})


def fx_d4(B):
    # D4a: engine accepted fs['engine_coordinates'] unchanged (B.run is that call)
    unchanged = B.fs['engine_coordinates'] == B.engine_coords_given
    rec('B-D4a', 'D4', B.run['status'] not in ('INPUT_INVALID', None) and unchanged,
        {'status': B.run['status'], 'engine_coord_keys': sorted(B.fs['engine_coordinates'][0])})
    # D4b: one step rule.
    out = {}
    for label, step in (('outside', 1.5), ('boundary', 1.0), ('inside', 0.5)):
        cs = coords_std()
        cs[2]['sensitivity'] = {'mode': 'step', 'step': step}   # q trial 1.0 in [0,2]
        f = F.make_freeze_coordinate_spec(coordinates=cs)
        ec = [dict(c) for c in coords_std()[:4]]
        eng_coords = []
        for c in ec:
            c2 = {k: c[k] for k in ('name', 'transform', 'lower', 'upper', 'role', 'trial_value', 'units')}
            c2['scope'] = 'shared' if c['scope'] == 'shared' else 'DDO154'
            c2['sensitivity'] = 'NONE'
            eng_coords.append(c2)
        eng_coords[2]['sensitivity'] = {'step_natural': step}
        e = E.make_coordinate_spec(coordinates=eng_coords)
        out[label] = (f['ok'], e['ok'])
    ok = out['outside'] == (False, False) and out['boundary'][0] == out['boundary'][1] and out['inside'] == (True, True)
    rec('B-D4b', 'D4', ok, {'(freeze_ok, engine_ok)': out})


def fx_d1(B):
    for fid, act in (('B-D1a', 'nan_and_999'), ('B-D1b', 'missing'), ('B-D1c1', 'flag_false'), ('B-D1c2', 'str_true'),
                     ('B-D1c3', 'int_one'), ('B-D1c4', 'np_true')):
        predicate, pt = pick(B.sel, 1)
        ev = B.evaluate(make_ngc(B.ids, (predicate, act)))
        m = ev['members'][1] if ev.get('ok') else None
        others_ok = ev.get('ok') and all(x['member_valid'] for i, x in enumerate(ev['members']) if i != 1)
        env_q01 = ev['envelopes'][B.ids[0]] if ev.get('ok') else None
        cond = (m is not None and not any(m['row_valid']) and m['member_valid'] is False and others_ok and
                env_q01['band_high_km_s'] is not None and env_q01['band_high_km_s'] < 900.0)
        det = {'member_valid': m and m['member_valid'], 'n_row_valid': m and sum(m['row_valid']),
               'q01_band_high': env_q01 and env_q01['band_high_km_s'], 'q01_valid': env_q01 and env_q01['valid']}
        if fid == 'B-D1a' and cond:
            # score: targets equal the bad member's own (diagnostic) speeds and 999 at Q01 -> must score 0
            fr = B.freeze('d1a', ev=ev, fwd=make_ngc(B.ids, (predicate, act)))
            det['write_ok'] = fr['w']['ok']
            det['write_reasons'] = fr['w']['reasons'][:3]
            if fr['w']['ok']:
                s = score(fr['w'], targets_from(m['speeds_km_s'], B.ids))
                bad = next(x for x in s['members'] if x['member_id'] == m['member_id']) if s['ok'] else None
                det.update({'score_ok': s['ok'], 'bad_member_count': bad and bad['within_error_count'],
                            'dist': s['ok'] and s['headline']['member_within_error_counts'],
                            'n_members_invalid': s['ok'] and s['headline']['n_members_invalid'],
                            'counts_by_member': s['ok'] and s['headline']['counts_by_member']})
                cond = cond and s['ok'] and bad['within_error_count'] == 0 and s['headline']['n_members_invalid'] == 1 \
                    and s['headline']['counts_by_member'][m['member_id']] == 0
                vf = F.verify_freeze_manifest(freeze_manifest_path=fr['w']['path'])
                det['verify_ok'] = vf['ok']
                cond = cond and vf['ok']
                # B-D1d: verifier refuses a re-hashed manifest whose invalid member has mixed row_valid
                d = B.fresh('d1d')

                def mut(doc, mid=m['member_id']):
                    mm = next(x for x in doc['members'] if x['member_id'] == mid)
                    mm['row_valid'] = [s_ is not None for s_ in mm['speeds_km_s']]
                path = rewrite_canonical(fr['w']['path'], os.path.join(d, 'FORGED_MIXED_ROWS.json'), mut)
                vd = F.verify_freeze_manifest(freeze_manifest_path=path)
                rec('B-D1d', 'D1', vd['ok'] is False and any('D1' in r for r in vd['reasons']),
                    {'verify_ok': vd['ok'], 'reasons': vd['reasons'][:2]})
        rec(fid, 'D1', cond, det)


def fx_p34_06(B):
    predicate, pt = pick(B.sel, 2)
    fwd = make_ngc(B.ids, (predicate, 'raise'))
    fr = B.freeze('p3406', fwd=fwd)
    det = {'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:2],
           'env_valid': sum(r['valid'] for r in fr['ev']['pointwise_envelope']) if fr['ev'].get('ok') else None}
    ok = fr['w']['ok'] and det['env_valid'] == 43
    if ok:
        refm = next(x for x in fr['ev']['members'] if x['member_id'] == fr['ref']['member_id'])
        s = score(fr['w'], targets_from(refm['speeds_km_s'], B.ids))
        det.update({'dist': s['headline']['member_within_error_counts'], 'ref_count': s['headline']['reference_within_error_count'],
                    'raised_member_count': s['headline']['counts_by_member']['M%03d' % 2]})
        ok = s['ok'] and s['headline']['reference_within_error_count'] == 43 and \
            s['headline']['counts_by_member']['M%03d' % 2] == 0 and s['headline']['member_within_error_counts']['max'] == 43
    rec('B-P34-06', 'P34-06', ok, det)


def fx_d2(B):
    fwd = make_ngc(B.ids)
    pts = B.sel['points']
    cases = {
        'subset_2': pts[:2],
        'reordered': list(reversed(pts)),
    }
    # swap one member for an admitted point outside the selection, same role
    sel_li = {p['log_index'] for p in pts}
    extra = [p for p in B.run['exploration']['admitted_points'] if p['log_index'] not in sel_li]
    if extra:
        sw = copy.deepcopy(pts)
        e0 = extra[0]
        V = B.sel['admitted_region']['right_vectors']
        ident = B.sel['admitted_region']['identified']
        sw[-1] = {'u': list(e0['u']), 'theta_natural': dict(e0['theta_natural']), 'role': pts[-1]['role'],
                  'log_index': e0['log_index'], 'identified_projection': [float(np.dot(e0['u'], V[k])) for k in ident]}
        cases['swapped'] = sw
    for name, p in cases.items():
        ev = B.evaluate(fwd, points=p)
        fr = B.freeze('d2_' + name, ev=ev, fwd=fwd)
        rec('B-D2-' + name, 'D2', fr['w']['ok'] is False and ev.get('ok') is True,
            {'eval_ok': ev.get('ok'), 'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:2]})
        if name == 'subset_2':
            fr2 = B.freeze('d2_subset_allow', ev=ev, fwd=fwd, allow_incomplete=True)
            rec('B-D2-subset_allow_incomplete', 'D2', fr2['w']['ok'] is False,
                {'write_ok': fr2['w']['ok'], 'freeze_status': fr2['w']['freeze_status'], 'reasons': fr2['w']['reasons'][:1]})
    # D2c: verifier recomputes the selection
    fr = B.freeze('d2c_clean', fwd=fwd)
    if not fr['w']['ok']:
        rec('B-D2c', 'D2', False, {'clean write failed': fr['w']['reasons'][:3]})
        return
    d = B.fresh('d2c')
    ref_id = fr['ref']['member_id']
    victim = next(m['member_id'] for m in fr['ev']['members'] if m['member_id'] != ref_id and m['role'] == 'interior')

    def mut(doc):
        idx = next(i for i, m in enumerate(doc['members']) if m['member_id'] == victim)
        li = doc['members'][idx]['log_index']
        del doc['members'][idx]
        doc['admitted_region']['selected_points'] = [x for x in doc['admitted_region']['selected_points'] if x['log_index'] != li]
        doc['member_evaluation']['n_selected'] -= 1
        doc['member_evaluation']['n_evaluated'] -= 1
        doc['member_evaluation']['n_member_valid'] -= 1
        doc['member_evaluation']['evaluations_used'] -= 1
        doc['pointwise_envelope'] = F._pointwise_envelope(doc['members'], doc['query_ids'])
        doc['reference_member']['ranking'] = F._reference_ranking(doc['members'], doc['admitted_region']['centroid_identified'])
    path = rewrite_canonical(fr['w']['path'], os.path.join(d, 'FORGED_DROPPED_MEMBER.json'), mut)
    vd = F.verify_freeze_manifest(freeze_manifest_path=path)
    rec('B-D2c', 'D2', vd['ok'] is False and any('D2' in r for r in vd['reasons']),
        {'verify_ok': vd['ok'], 'reasons': vd['reasons'][:2]})


def fx_d3(B):
    fwd_real = make_ngc(B.ids)
    # D3a: 43 arbitrary ids, matching forward, real manifest pinned as PROGRAM_PIN
    arb = ['ARB-%02d' % i for i in range(1, 44)]
    fr = B.freeze('d3a', fwd=make_ngc(arb), ids=arb)
    rec('B-D3a', 'D3', fr['w']['ok'] is False, {'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:1]})
    # D3a': arbitrary ids with the arbitrary ids' own manifest under role PROGRAM_PIN -> refused
    d = B.fresh('d3a2')
    qa = os.path.join(d, 'ARBITRARY_QM.json')
    with open(qa, 'x') as fh:
        json.dump({'rows': [{'query_id': q, 'data_row_index': j + 1, 'Rad_text': '1.0', 'Rad_unit': 'kpc'}
                            for j, q in enumerate(arb)]}, fh)
    fr = B.freeze('d3a2w', fwd=make_ngc(arb), ids=arb, qm={'path': qa, 'sha256': sha(qa), 'role': 'PROGRAM_PIN'})
    rec('B-D3a2', 'D3', fr['w']['ok'] is False, {'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:1]})
    # same under SYNTHETIC_FIXTURE: allowed by design but must be stamped not-program in the scorer
    fr = B.freeze('d3a3w', fwd=make_ngc(arb), ids=arb, qm={'path': qa, 'sha256': sha(qa), 'role': 'SYNTHETIC_FIXTURE'})
    det = {'write_ok': fr['w']['ok'], 'role': fr['w']['query_manifest_role']}
    ok = fr['w']['ok']
    if ok:
        s = score(fr['w'], targets_from([150.0] * 43, arb))
        det.update({'score_ok': s['ok'], 'is_program_pin': s['headline']['query_manifest_is_program_pin'],
                    'note': [r for r in s['reasons'] if 'SYNTHETIC' in r][:1]})
        ok = s['ok'] and s['headline']['query_manifest_is_program_pin'] is False and \
            s['headline']['query_manifest_role'] == 'SYNTHETIC_FIXTURE'
    rec('B-D3a3', 'D3', ok, det)
    # D3b: tampered copy of the real manifest
    d = B.fresh('d3b')
    tq = os.path.join(d, 'TAMPERED_QM_COPY.json')
    raw = open(QM_REAL, 'rb').read()
    traw = raw.replace(b'"Rad_text": "0.32"', b'"Rad_text": "0.33"', 1)
    assert traw != raw
    with open(tq, 'xb') as fh:
        fh.write(traw)
    r1 = B.freeze('d3b1', fwd=fwd_real, qm={'path': tq, 'sha256': sha(tq), 'role': 'PROGRAM_PIN'})
    r2 = B.freeze('d3b2', fwd=fwd_real, qm={'path': tq, 'sha256': QM_SHA, 'role': 'PROGRAM_PIN'})
    r3 = B.freeze('d3b3', fwd=fwd_real, qm={'path': QM_REAL, 'sha256': QM_SHA, 'role': 'SYNTHETIC_FIXTURE'})
    rec('B-D3b', 'D3', not r1['w']['ok'] and not r2['w']['ok'] and not r3['w']['ok'],
        {'own_sha_as_program': r1['w']['reasons'][:1], 'real_sha_tampered_bytes': r2['w']['reasons'][:1],
         'real_as_synthetic': r3['w']['reasons'][:1]})
    # D3c: permuted ids
    perm = list(B.ids)
    perm[0], perm[1] = perm[1], perm[0]
    fr = B.freeze('d3c', fwd=make_ngc(perm), ids=perm)
    rec('B-D3c', 'D3', fr['w']['ok'] is False, {'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:1]})
    # D3d: input_files omits the query manifest
    fr = B.freeze('d3d', fwd=fwd_real, input_files=[B.region, B.rec['record_path']])
    rec('B-D3d', 'D3', fr['w']['ok'] is False, {'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:1]})
    # D3e: post-freeze tamper of the pinned query manifest copy (byte-identical copy pinned as PROGRAM_PIN)
    d = B.fresh('d3e')
    cq = os.path.join(d, 'QM_COPY.json')
    shutil.copyfile(QM_REAL, cq)
    fr = B.freeze('d3e_w', fwd=fwd_real, qm={'path': cq, 'sha256': QM_SHA, 'role': 'PROGRAM_PIN'},
                  input_files=[B.region, cq, B.rec['record_path']])
    det = {'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:1]}
    ok = fr['w']['ok']
    if ok:
        v0 = F.verify_freeze_manifest(freeze_manifest_path=fr['w']['path'])
        with open(cq, 'wb') as fh:
            fh.write(traw)
        v1 = F.verify_freeze_manifest(freeze_manifest_path=fr['w']['path'])
        s = score(fr['w'], targets_from([150.0] * 43, B.ids))
        det.update({'verify_before': v0['ok'], 'verify_after': v1['ok'], 'score_after': s['ok'],
                    'score_reasons': s['reasons'][:2]})
        ok = v0['ok'] and not v1['ok'] and not s['ok'] and s['target_rows_sha256'] is not None
    rec('B-D3e', 'D3', ok, det)


def fx_s8(B):
    out = {}
    for name in ('range', 'extra_key', 'inf_key', 'nan_key', 'str_garbage'):
        run = copy.deepcopy(B.run)
        hb = run['exploration'].get('hull_box')
        if not isinstance(hb, dict) or not hb:
            out[name] = 'no hull_box in run'
            continue
        k0 = sorted(hb)[0]
        if name == 'range':
            hb[k0] = {'min': hb[k0]['min'], 'max': hb[k0]['max'] + 0.1}
        elif name == 'extra_key':
            hb['99'] = {'min': 0.0, 'max': 0.1}
        elif name == 'inf_key':
            hb[float('inf')] = {'min': 0.0, 'max': 0.1}
        elif name == 'nan_key':
            hb[float('nan')] = {'min': 0.0, 'max': 0.1}
        else:
            hb['x'] = {'min': 0.0, 'max': 0.1}
        r = F.select_representative_points(exploration=run, interior_count=5, spec=B.fs['spec'])
        out[name] = (r['ok'], (r['reasons'] or [''])[0][:120])
    rec('B-S8', 'S8', all(isinstance(v, tuple) and v[0] is False for v in out.values()), out)
    rec('B-S10b', 'S10', all(isinstance(out.get(k), tuple) for k in ('inf_key', 'nan_key')), {k: out.get(k) for k in ('inf_key', 'nan_key')})


def fx_s10(B):
    deep = []
    cur = deep
    for _ in range(5000):
        nxt = []
        cur.append(nxt)
        cur = nxt
    cyc = []
    cyc.append(cyc)
    cycd = {}
    cycd['self'] = cycd
    det = {}
    for name, notes in (('deep_list', deep), ('cyclic_list', cyc), ('cyclic_dict', cycd)):
        try:
            fr = B.freeze('s10_' + name, notes=notes)
            det[name] = (fr['w']['ok'], (fr['w']['reasons'] or [''])[0][:120])
        except Exception as exc:
            det[name] = ('RAISED', '%s: %s' % (type(exc).__name__, str(exc)[:100]))
    rec('B-S10a', 'S10', all(v[0] is False for v in det.values()), det)
    # ndarray as transform / role
    det = {}
    for field, val in (('transform', np.array(['linear'])), ('role', np.array('free')), ('scope', np.array(['shared'])),
                       ('lower', np.array([0.0, 1.0]))):
        cs = coords_std()
        cs[0][field] = val
        try:
            r = F.make_freeze_coordinate_spec(coordinates=cs)
            fres = r['ok']
        except Exception as exc:
            fres = 'RAISED %s' % type(exc).__name__
        ec = copy.deepcopy(B.fs['engine_coordinates'])
        ec[0][field] = val
        try:
            r = E.make_coordinate_spec(coordinates=ec)
            eres = r['ok']
        except Exception as exc:
            eres = 'RAISED %s' % type(exc).__name__
        det[field] = (fres, eres)
    rec('B-S10c', 'S10', all(v == (False, False) for v in det.values()), det)


def fx_s11(B):
    det = {}
    for name, pr in (('empty', {}), ('string', 'box'), ('no_label', {'description': 'box'}),
                     ('wrong_label', {'bounds_semantics': 'EMPIRICAL'})):
        fr = B.freeze('s11_' + name, parameter_region=pr)
        det[name] = (fr['w']['ok'], (fr['w']['reasons'] or [''])[0][:90])
    rec('B-S11', 'S11', all(v[0] is False for v in det.values()), det)


def fx_p34_15(B):
    fr = B.freeze('p3415_int', notes={i: 'n%d' % i for i in range(12)})
    det = {'write_ok': fr['w']['ok'], 'reasons': fr['w']['reasons'][:1]}
    ok = fr['w']['ok']
    if ok:
        v = F.verify_freeze_manifest(freeze_manifest_path=fr['w']['path'])
        s = score(fr['w'], targets_from([150.0] * 43, B.ids))
        det.update({'verify_ok': v['ok'], 'score_ok': s['ok']})
        ok = v['ok'] and s['ok']
    try:
        fr2 = B.freeze('p3415_dup', notes={1: 'a', '1': 'b'})
        det['dup_key'] = (fr2['w']['ok'], (fr2['w']['reasons'] or [''])[0][:90])
        ok = ok and fr2['w']['ok'] is False
    except Exception as exc:
        det['dup_key'] = 'RAISED %s' % type(exc).__name__
        ok = False
    # engine side: a run record whose run carries a dict with >= 11 int keys must round-trip
    rr = copy.deepcopy(B.run)
    rr['checker_int_keys'] = {i: i for i in range(13)}
    d = B.fresh('p3415_rec')
    w = E.write_calibration_record(run=rr, record_path=os.path.join(d, 'REC.json'), registry_path=os.path.join(d, 'REG.jsonl'))
    vr = E.verify_calibration_record(record_path=os.path.join(d, 'REC.json'), registry_path=os.path.join(d, 'REG.jsonl')) if w['ok'] else {'ok': None}
    det['engine_record'] = (w['ok'], vr['ok'])
    ok = ok and w['ok'] and vr['ok']
    rec('B-P34-15', 'P34-15', ok, det)


def fx_p34_14(B):
    adm = {p['log_index'] for p in B.run['exploration']['admitted_points']}
    sel_li = [p['log_index'] for p in B.sel['points']]
    pa = B.run['exploration'].get('primary_anchor') or {}
    anchor_members = [p['log_index'] for p in B.sel['points'] if p['role'] == 'anchor']
    ok1 = set(sel_li) <= adm and B.sel['admission_reverified'] is True and \
        (not anchor_members or anchor_members == [pa.get('log_index')])
    rec('B-P34-14a', 'P34-14', ok1, {'selected': sel_li, 'anchor_members': anchor_members,
                                    'primary_anchor': pa.get('log_index'), 'reverified': B.sel['admission_reverified']})
    # forged run: a non-admitted logged evaluation injected into admitted_points / as primary_anchor
    log = B.run['evaluation_log']
    nonadm = [e for e in log if e.get('valid') and not e.get('admitted')]
    det = {'n_nonadmitted_log': len(nonadm)}
    ok2 = bool(nonadm)
    if nonadm:
        e0 = nonadm[0]
        r1 = copy.deepcopy(B.run)
        pt = copy.deepcopy(r1['exploration']['admitted_points'][0])
        pt.update({'u': list(e0['u']), 'theta_natural': dict(e0['theta_natural']), 'log_index': e0['index'],
                   'prediction': copy.deepcopy(e0.get('prediction'))})
        r1['exploration']['admitted_points'].append(pt)
        r1['exploration_fingerprint'] = None
        s1 = F.select_representative_points(exploration=r1, interior_count=5, spec=B.fs['spec'])
        r2 = copy.deepcopy(B.run)
        r2['exploration']['primary_anchor'] = {'log_index': e0['index']}
        s2 = F.select_representative_points(exploration=r2, interior_count=5, spec=B.fs['spec'])
        det.update({'inject_admitted': (s1['ok'], (s1['reasons'] or [''])[0][:120]),
                    'forge_primary_anchor': (s2['ok'], (s2['reasons'] or [''])[0][:120]),
                    'admitted_point_keys': sorted(pt)})
        ok2 = s1['ok'] is False and s2['ok'] is False
    rec('B-P34-14b', 'P34-14', ok2, det)
    # EXTRA (added after reading v003, not a blind-plan row): P34-14 re-verification uses the rectangles carried
    # in the run dict, not rectangles re-derived from the pinned region file bytes. Forge the run dict: inject a
    # non-admitted logged evaluation, widen the rectangles in the dict, empty hull_box; then freeze with and
    # without the calibration record pinned. Expected (P34-14 intent): no non-admitted point becomes a member.
    if nonadm:
        r3 = copy.deepcopy(r1)
        for rid in r3['region']['rectangles']:
            lo, hi = r3['region']['rectangles'][rid]
            r3['region']['rectangles'][rid] = [lo - 1e6, hi + 1e6]
        r3['exploration']['hull_box'] = {}
        s3 = F.select_representative_points(exploration=r3, interior_count=60, spec=B.fs['spec'])
        det = {'select_ok': s3['ok'], 'select_reasons': s3['reasons'][:2]}
        member_li = [p['log_index'] for p in s3['points']] if s3['ok'] else []
        det['injected_is_member'] = e0['index'] in member_li
        ok = not s3['ok'] or e0['index'] not in member_li
        if s3['ok']:
            fr_nr = B.freeze('p3414d_norecord', sel=s3, input_files=[B.region, QM_REAL])
            fr_r = B.freeze('p3414d_record', sel=s3)
            det['write_without_record_pin'] = (fr_nr['w']['ok'], fr_nr['w']['freeze_status'], fr_nr['w']['reasons'][:1])
            det['write_with_record_pin'] = (fr_r['w']['ok'], fr_r['w']['reasons'][:1])
            if fr_nr['w']['ok']:
                det['verify_without_record_pin'] = F.verify_freeze_manifest(freeze_manifest_path=fr_nr['w']['path'])['ok']
                det['injected_log_index'] = e0['index']
                det['injected_prediction_row0'] = e0['prediction']['speeds_km_s'][ROWS[0]]
                det['true_rectangle_row0'] = B.run['region']['rectangles'][ROWS[0]]
            ok = (not fr_nr['w']['ok']) and (not fr_r['w']['ok'])
        rec('X-P34-14d', 'P34-14', ok, det)


def fx_p34_16(B):
    # EXTRA: an INPUT_INVALID run (wrong region sha) is still recorded and chained; an edited registry line is detected
    d = B.fresh('p3416')
    bad = E.run_calibration_region(forward=ddo_std, coordinates=B.fs['engine_coordinates'], observation_region_path=B.region,
                                   observation_region_sha256='0' * 64,
                                   ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0}, **ENGINE_PARAMS)
    reg = os.path.join(d, 'REG.jsonl')
    w1 = E.write_calibration_record(run=bad, record_path=os.path.join(d, 'R1.json'), registry_path=reg)
    w2 = E.write_calibration_record(run=B.run, record_path=os.path.join(d, 'R2.json'), registry_path=reg)
    v_ok = E.verify_calibration_record(record_path=os.path.join(d, 'R2.json'), registry_path=reg)
    lines = open(reg, 'rb').read().splitlines(keepends=True)
    with open(reg, 'wb') as fh:
        fh.write(lines[0].replace(b'INPUT_INVALID', b'INPUT_INVALIE', 1) + b''.join(lines[1:]))
    v_bad = E.verify_calibration_record(record_path=os.path.join(d, 'R2.json'), registry_path=reg)
    rec('X-P34-16', 'P34-16', bad['status'] == 'INPUT_INVALID' and w1['ok'] and w2['ok'] and v_ok['ok'] and
        v_ok.get('registry_chain_ok') is True and not (v_bad['ok'] and v_bad.get('registry_chain_ok')),
        {'bad_status': bad['status'], 'w1': w1['ok'], 'w2': w2['ok'], 'verify': (v_ok['ok'], v_ok.get('registry_chain_ok')),
         'after_edit': (v_bad['ok'], v_bad.get('registry_chain_ok'), v_bad['reasons'][:1])})


def fx_d8(B):
    fr = B.freeze('d8_clean')
    if not fr['w']['ok']:
        rec('B-D8', 'D8', False, {'clean write failed': fr['w']['reasons'][:3]})
        return
    w = fr['w']
    T = targets_from([150.0] * 43, B.ids)
    # D8a: caller sha differs from registered
    s = score(w, T, expected='f' * 64)
    ok = (not s['ok'] and s['manifest_file_sha256_actual'] == w['manifest_file_sha256'] and
          s['target_rows_sha256'] is not None and s['manifest_file_sha256_registered'] == w['manifest_file_sha256'])
    rec('B-D8a', 'D8', ok, {k: s[k] for k in ('ok', 'manifest_file_sha256_expected', 'manifest_file_sha256_actual',
                                              'manifest_file_sha256_registered', 'target_rows_sha256')})
    # D8b: manifest file bytes changed after registration (re-hashed notes edit: verifies, but not registered)
    d = B.fresh('d8b')
    forged = rewrite_canonical(w['path'], os.path.join(d, 'FORGED_REHASHED.json'),
                               lambda doc: doc['notes'].update({'edited': True}))
    vf = F.verify_freeze_manifest(freeze_manifest_path=forged)
    s = F.score_after_freeze(freeze_manifest_path=forged, registration_path=w['registration_path'],
                             expected_manifest_file_sha256=w['manifest_file_sha256'], target_rows=T)
    ok = (not s['ok'] and s['manifest_file_sha256_actual'] == sha(forged) and
          s['manifest_file_sha256_expected'] == w['manifest_file_sha256'] and s['target_rows_sha256'] is not None)
    rec('B-D8b', 'D8', ok, {'forged_verifies_by_design': vf['ok'], 'score_ok': s['ok'],
                            'actual': s['manifest_file_sha256_actual'], 'reasons': s['reasons'][:1]})
    # D8c: forged registration pointing at the forged file, re-self-hashed; caller passes the LOGGED sha
    reg = json.loads(open(w['registration_path'], 'rb').read())
    reg['expected_manifest_file_sha256'] = sha(forged)
    reg['manifest_path'] = os.path.realpath(forged)
    reg['manifest_sha256_self'] = json.loads(open(forged, 'rb').read())['manifest_sha256']
    body = {k: v for k, v in reg.items() if k != 'registration_sha256'}
    reg['registration_sha256'] = hashlib.sha256(F._canonical_bytes(body)).hexdigest()
    freg = os.path.join(d, 'FORGED_REGISTRATION.json')
    with open(freg, 'xb') as fh:
        fh.write(F._canonical_bytes(reg))
    vr = F.verify_registration(registration_path=freg)
    s = F.score_after_freeze(freeze_manifest_path=forged, registration_path=freg,
                             expected_manifest_file_sha256=w['manifest_file_sha256'], target_rows=T)
    # forged registration with a broken self-hash
    reg2 = dict(reg)
    reg2['registration_sha256'] = '0' * 64
    freg2 = os.path.join(d, 'FORGED_REGISTRATION_BADHASH.json')
    with open(freg2, 'xb') as fh:
        fh.write(F._canonical_bytes(reg2))
    s2 = F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=freg2,
                              expected_manifest_file_sha256=w['manifest_file_sha256'], target_rows=T)
    ok = (not s['ok'] and not s2['ok'] and s['target_rows_sha256'] is not None and s2['target_rows_sha256'] is not None
          and s2['manifest_file_sha256_actual'] == w['manifest_file_sha256'])
    rec('B-D8c', 'D8', ok, {'forged_reg_self_verifies': vr['ok'], 'score_logged_sha': (s['ok'], s['reasons'][:1]),
                            'bad_selfhash': (s2['ok'], s2['reasons'][:1]),
                            'echo_bad_selfhash': {k: s2[k] for k in ('manifest_file_sha256_actual', 'target_rows_sha256',
                                                                     'registration_file_sha256')}})
    # clean path echo + score
    s = score(w, T)
    rec('B-D8-clean', 'D8', s['ok'] and all(s[k] for k in ('manifest_file_sha256_expected', 'manifest_file_sha256_actual',
                                                          'manifest_sha256_self', 'registration_file_sha256',
                                                          'target_rows_sha256')),
        {k: s[k] for k in ('ok', 'manifest_file_sha256_actual', 'manifest_sha256_self', 'registration_file_sha256')})


# ---------------------------------------------------------------- S2 (repair stays in span(identified))
def fx_s2(run_dir):
    d = os.path.join(run_dir, 's2')
    os.makedirs(d)
    region = write_region(os.path.join(d, 'REGION.json'))
    cs = [dict(name='a', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.8, units='dimensionless',
               scope='shared', sensitivity='NONE'),
          dict(name='c', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.2, units='dimensionless',
               scope='shared', sensitivity='NONE'),
          dict(name='b', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=0.5, units='dimensionless',
               scope='shared', sensitivity='NONE'),
          dict(name='D_ddo', transform='log', lower=DC * 0.96, upper=DC * 1.04, role='fixed', trial_value=DC,
               units='Mpc', scope='DDO154', sensitivity='NONE')]

    def fwd(th):   # depends on (a + c) and b only: exact null direction (1, -1, 0)/sqrt(2) in u
        s_ = th['a'] + th['c']
        return {'speeds_km_s': {r: 100.0 + (8.0 + 0.3 * i) * (s_ - 1.6) + (5.0 - 0.2 * i) * (th['b'] - 0.5)
                                for i, r in enumerate(ROWS)}, 'valid': True, 'reasons': []}
    run = E.run_calibration_region(forward=fwd, coordinates=cs, observation_region_path=region,
                                   observation_region_sha256=sha(region), u_seed=None, budget=300, rel_step=0.05,
                                   min_step=1e-4, max_halvings=3, null_tolerance=1e-6, repair_iterations=8,
                                   max_repair_step=0.9, march_step=0.05, bisection_steps=4, design_count=4,
                                   global_design_count=0, max_march_rounds=1, hull_growth_tol=0.01,
                                   ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0}, rng_seed=0)
    ex = run.get('exploration') or {}
    rep = ex.get('repair') or {}
    steps = rep.get('steps') or []
    nn = [s.get('near_null_component_max') for s in steps]
    dirs = ex.get('unidentified_directions') or ex.get('directions') or []
    proj_keys = sorted({k for dd in (dirs if isinstance(dirs, list) else []) if isinstance(dd, dict) for k in dd
                        if 'projection' in k})
    trunc = [s.get('step_length_fraction') for s in steps]
    # admitted primary via repair: its (a - c) must equal the trial's (0.6) within 1e-9
    pa = ex.get('primary_anchor') or {}
    amc = None
    if pa.get('log_index') is not None:
        e = run['evaluation_log'][pa['log_index']]
        amc = e['theta_natural']['a'] - e['theta_natural']['c']
    ok = (run['identifiability'] is not None and len(run['identifiability'].get('near_null') or []) == 1 and
          len(steps) >= 1 and all(x is not None and x <= 1e-9 for x in nn) and
          'trial_projection' in proj_keys and 'seed_projection' in proj_keys and
          any(t is not None and t < 1.0 for t in trunc))
    # EXTRA (not a blind-plan row): the repair-unreachable region on this toy is NOT reported empty, and the global
    # design (A1) finds it when enabled.
    run2 = E.run_calibration_region(forward=fwd, coordinates=cs, observation_region_path=region,
                                    observation_region_sha256=sha(region), u_seed=None, budget=400, rel_step=0.05,
                                    min_step=1e-4, max_halvings=3, null_tolerance=1e-6, repair_iterations=8,
                                    max_repair_step=0.9, march_step=0.05, bisection_steps=4, design_count=4,
                                    global_design_count=48, max_march_rounds=2, hull_growth_tol=0.01,
                                    ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0}, rng_seed=0)
    rec('X-S2-A1', 'A1', run['empty_region'] is not True and run2['status'] == 'COMPLETE' and
        (run2['exploration'] or {}).get('n_admitted', 0) > 0,
        {'no_global_status': run['status'], 'no_global_empty_region': run['empty_region'],
         'global_status': run2['status'], 'global_n_admitted': (run2['exploration'] or {}).get('n_admitted')})
    rec('B-S2', 'S2', ok, {'status': run['status'], 'near_null': (run['identifiability'] or {}).get('near_null'),
                           'n_steps': len(steps), 'near_null_component_max': nn, 'step_length_fraction': trunc,
                           'repair_terminated': [p.get('terminated_by') for p in rep.get('phases', [])],
                           'projection_keys': proj_keys, 'primary_source': pa.get('source'),
                           'primary_a_minus_c': amc, 'trial_a_minus_c': 0.6})


# ---------------------------------------------------------------- sub-runs (subprocess, timeout)
def sub_s1(variant, d):
    os.makedirs(d)
    region = write_region(os.path.join(d, 'REGION.json'))
    fs = F.make_freeze_coordinate_spec(coordinates=coords_std())

    def fwd(th):
        if variant == 'all_1e307':
            v = {r: 1e307 * (1.0 + th['a'] + 0.1 * i * th['b']) for i, r in enumerate(ROWS)}
        elif variant == 'all_1e308':
            v = {r: 1.7e308 * (th['a'] - 0.5) * (1 if i % 2 else -1) for i, r in enumerate(ROWS)}
        elif variant == 'far_1e307':   # normal near the seed, 1e307 once the march leaves a < 0.75
            if th['a'] > 0.75 or th['b'] > 0.8:
                v = {r: 1e307 for r in ROWS}
            else:
                return ddo_std(th)
        else:
            raise SystemExit('unknown variant')
        return {'speeds_km_s': v, 'valid': True, 'reasons': []}
    t0 = time.time()
    run = run_engine(fwd, fs['engine_coordinates'], region)
    dt = time.time() - t0
    w = E.write_calibration_record(run=run, record_path=os.path.join(d, 'REC.json'), registry_path=os.path.join(d, 'REG.jsonl'))
    out = {'variant': variant, 'status': run['status'], 'ok': run['ok'], 'seconds': round(dt, 2),
           'reasons': [r[:140] for r in run['reasons'][:4]], 'record_ok': w['ok'],
           'record_reasons': w['reasons'][:2]}
    if run['status'] == 'COMPLETE':
        sel = F.select_representative_points(exploration=run, interior_count=3, spec=fs['spec'])
        out['select_ok'] = sel['ok']
    print('JSONRESULT ' + json.dumps(out, default=str))


def sub_e2e(variant, d):
    """End-to-end toy of ROOT_CALL_ORDER.md on synthetic stand-ins, real query-manifest ids (PROGRAM_PIN)."""
    os.makedirs(d)
    p = lambda n: os.path.join(d, n)   # noqa: E731
    region = write_region(p('SYNTHETIC_REGION_12ROW_NOT_DDO154.json'))
    qm = F.load_query_manifest(path=QM_REAL, expected_sha256=QM_SHA)
    ids = list(qm['query_ids'])
    steps = {}

    def stop(step, res):
        steps[step] = {'ok': res.get('ok'), 'reasons': [str(r)[:160] for r in (res.get('reasons') or [])[:3]]}
        print('JSONRESULT ' + json.dumps({'variant': variant, 'stopped_at': step, 'steps': steps}, default=str))
        sys.exit(0)

    fs = F.make_freeze_coordinate_spec(coordinates=coords_std())                                   # 0
    if not fs['ok']:
        stop('0_spec', fs)
    fwd_ddo = ddo_std
    if variant == 'ddo_1e307':
        def fwd_ddo(th):
            return {'speeds_km_s': {r: 1e307 * (1.0 + th['a'] + 0.1 * i * th['b']) for i, r in enumerate(ROWS)},
                    'valid': True, 'reasons': []}
    t0 = time.time()
    run = run_engine(fwd_ddo, fs['engine_coordinates'], region)                                     # 1
    steps['1_engine'] = {'status': run['status'], 'seconds': round(time.time() - t0, 2),
                         'truncation_causes': run['truncation_causes'],
                         'region_possibly_truncated': run['region_possibly_truncated']}
    rec_ = E.write_calibration_record(run=run, record_path=p('CALIBRATION_RECORD.json'),             # 1b
                                      registry_path=p('CALIBRATION_REGISTRY.jsonl'))
    steps['1b_record'] = {'ok': rec_['ok'], 'status': rec_['status']}
    if run['status'] != 'COMPLETE':
        vc = E.verify_calibration_record(record_path=p('CALIBRATION_RECORD.json'), registry_path=p('CALIBRATION_REGISTRY.jsonl'))
        steps['1c_record_verify'] = {'ok': vc['ok'], 'chain': vc.get('registry_chain_ok')}
        sel = F.select_representative_points(exploration=run, interior_count=5, spec=fs['spec'])
        stop('1_engine_not_complete(select_attempted)', sel)
    sel = F.select_representative_points(exploration=run, interior_count=5, spec=fs['spec'])        # 2
    if not sel['ok']:
        stop('2_select', sel)
    steps['2_select'] = {'n_members': len(sel['points']), 'roles': [x['role'] for x in sel['points']]}
    bad = None
    if variant == 'nan_member':
        bad = (pick(sel, 1)[0], 'nan_and_999')
    elif variant == 'ngc_1e307':
        bad = (pick(sel, 1)[0], 'huge')
    fwd_ngc = make_ngc(ids, bad)
    budget = len(sel['points']) - 1 if variant in ('partial', 'partial_allow') else 100
    ev = F.evaluate_envelopes(forward_ngc=fwd_ngc, points=sel['points'], spec=fs['spec'], query_ids=ids,  # 3
                              budget=budget)
    if not ev['ok']:
        stop('3_evaluate', ev)
    steps['3_evaluate'] = {'status': ev['status'], 'n_member_valid': ev['n_member_valid'],
                           'n_member_invalid': ev['n_member_invalid']}
    ref = F.select_reference_member(selection=sel, evaluation=ev)                                   # 3b
    if not ref['ok']:
        stop('3b_reference', ref)
    sens = F.evaluate_sensitivity(forward_ngc=fwd_ngc, reference=ref, selection=sel, spec=fs['spec'],  # 4
                                  query_ids=ids, null_direction_rule={'mode': 'box_ends'}, budget=200)
    if not sens['ok']:
        stop('4_sensitivity', sens)
    steps['4_sensitivity'] = {'status': sens['status'], 'n_entries': len(sens['evaluations'])}
    qpath = QM_REAL
    if variant == 'tampered_qm':
        qpath = p('QM_COPY.json')
        shutil.copyfile(QM_REAL, qpath)
    w = F.write_freeze_manifest(                                                                   # 5
        out_path=p('FREEZE_MANIFEST.json'), registration_path=p('FREEZE_REGISTRATION.json'), parameter_region=PREG,
        observation_rule={'rule': 'closed Bonferroni rectangle (checker synthetic)'}, spec=fs['spec'], selection=sel,
        alternatives=ALTS, alternative_evaluations={'CHK_STATE': ev}, reference=ref, sensitivity=sens, query_ids=ids,
        query_manifest={'path': qpath, 'sha256': QM_SHA, 'role': 'PROGRAM_PIN'}, code_files=[FRZ_PATH, ENG_PATH],
        input_files=[region, qpath, rec_['record_path']], notes={'checker_e2e': variant},
        allow_incomplete=(variant == 'partial_allow'))
    if not w['ok']:
        stop('5_write', w)
    steps['5_write'] = {'freeze_status': w['freeze_status'], 'calibration_record_bound': w['calibration_record_bound'],
                        'incomplete_reasons': w['incomplete_reasons'][:2]}
    line = {'manifest_file_sha256': w['manifest_file_sha256'], 'registration_file_sha256': w['registration_file_sha256'],
            'calibration_record_file_sha256': rec_['record_file_sha256'], 'targets_opened': False}
    with open(p('EXTERNAL_REGISTRATION_LOG.jsonl'), 'x') as fh:                                     # 6
        fh.write(json.dumps(line, sort_keys=True) + '\n')
    if variant == 'tampered_qm':
        raw = open(qpath, 'rb').read()
        with open(qpath, 'wb') as fh:
            fh.write(raw.replace(b'"Rad_text": "0.32"', b'"Rad_text": "0.31"', 1))
    if variant == 'tampered_manifest':
        raw = open(w['path'], 'rb').read()
        os.chmod(w['path'], 0o644)
        with open(w['path'], 'wb') as fh:
            fh.write(raw.replace(b'"checker_e2e":"tampered_manifest"', b'"checker_e2e":"tampered_manifesT"', 1))
    if variant == 'forged_registration':
        reg = json.loads(open(w['registration_path'], 'rb').read())
        forged = p('FORGED_MANIFEST.json')
        rewrite_canonical(w['path'], forged, lambda doc: doc['notes'].update({'forged': True}))
        reg.update({'expected_manifest_file_sha256': sha(forged), 'manifest_path': os.path.realpath(forged),
                    'manifest_sha256_self': json.loads(open(forged, 'rb').read())['manifest_sha256']})
        body = {k: v for k, v in reg.items() if k != 'registration_sha256'}
        reg['registration_sha256'] = hashlib.sha256(F._canonical_bytes(body)).hexdigest()
        os.remove(w['registration_path'])
        with open(w['registration_path'], 'xb') as fh:
            fh.write(F._canonical_bytes(reg))
        w = dict(w)
        w['path'] = forged
    vf = F.verify_freeze_manifest(freeze_manifest_path=w['path'])                                   # 7
    vr = F.verify_registration(registration_path=w['registration_path'])
    vc = E.verify_calibration_record(record_path=rec_['record_path'], registry_path=rec_['registry_path'])
    steps['7_verify'] = {'manifest': vf['ok'], 'manifest_reasons': [r[:140] for r in vf['reasons'][:2]],
                         'registration': vr['ok'], 'record': vc['ok'], 'chain': vc.get('registry_chain_ok')}
    logged = json.loads(open(p('EXTERNAL_REGISTRATION_LOG.jsonl')).read().splitlines()[0])
    refm = ref['member']
    T = targets_from(refm['speeds_km_s'], ids, sigma=1.0)                                        # invented targets
    s = F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=w['registration_path'],    # 8
                             expected_manifest_file_sha256=logged['manifest_file_sha256'], target_rows=T)
    steps['8_score'] = {'ok': s['ok'], 'reasons': [r[:160] for r in s['reasons'][:2]],
                        'echo': {k: s[k] for k in ('manifest_file_sha256_expected', 'manifest_file_sha256_actual',
                                                   'manifest_file_sha256_registered', 'target_rows_sha256')}}
    if s['ok']:
        h = s['headline']
        steps['8_score']['headline'] = {k: h[k] for k in ('member_within_error_counts', 'counts_by_member',
                                                          'reference_member_id', 'reference_within_error_count',
                                                          'n_members_invalid', 'freeze_status', 'query_manifest_role',
                                                          'query_manifest_is_program_pin', 'calibration_record_bound',
                                                          'region_possibly_truncated')}
    print('JSONRESULT ' + json.dumps({'variant': variant, 'stopped_at': None, 'steps': steps}, default=str))


def run_sub(name, variant, d, timeout=240):
    t0 = time.time()
    try:
        cp = subprocess.run([PY, '-I', '-B', os.path.realpath(__file__), '--sub', name, variant, d],
                            capture_output=True, text=True, timeout=timeout, env=dict(os.environ))
    except subprocess.TimeoutExpired:
        return {'TIMEOUT': True, 'seconds': round(time.time() - t0, 1)}
    line = [x for x in cp.stdout.splitlines() if x.startswith('JSONRESULT ')]
    if not line:
        return {'NO_RESULT': True, 'rc': cp.returncode, 'stderr_tail': cp.stderr[-1500:]}
    r = json.loads(line[-1][len('JSONRESULT '):])
    r['wall_seconds'] = round(time.time() - t0, 1)
    return r


def fx_s1(run_dir):
    for v in ('all_1e307', 'all_1e308', 'far_1e307'):
        r = run_sub('s1', v, os.path.join(run_dir, 's1_' + v), timeout=240)
        ok = ('TIMEOUT' not in r and 'NO_RESULT' not in r and r.get('record_ok') is True and
              (r.get('status') != 'COMPLETE' or r.get('select_ok') is not None))
        if v in ('all_1e307', 'all_1e308'):
            ok = ok and r.get('ok') is False
        rec('B-S1-' + v, 'S1', ok, r)


def fx_e2e(run_dir):
    res = {}
    for v in ('clean', 'nan_member', 'partial', 'partial_allow', 'tampered_qm', 'tampered_manifest',
              'forged_registration', 'ddo_1e307', 'ngc_1e307'):
        res[v] = run_sub('e2e', v, os.path.join(run_dir, 'e2e_' + v), timeout=300)
    st = lambda v: res[v].get('steps', {})   # noqa: E731

    def g(v, *ks):
        x = st(v)
        for k in ks:
            if not isinstance(x, dict):
                return None
            x = x.get(k)
        return x
    c = res['clean']
    ok = (c.get('stopped_at') is None and g('clean', '5_write', 'freeze_status') == 'FREEZE_COMPLETE' and
          g('clean', '7_verify', 'manifest') and g('clean', '7_verify', 'registration') and g('clean', '7_verify', 'record')
          and g('clean', '8_score', 'ok') and g('clean', '8_score', 'headline', 'query_manifest_is_program_pin') is True
          and g('clean', '8_score', 'headline', 'calibration_record_bound') is True
          and g('clean', '8_score', 'headline', 'reference_within_error_count') == 43)
    rec('B-E2E-clean', 'E2E', ok, c)
    hn = g('nan_member', '8_score', 'headline') or {}
    ok = (res['nan_member'].get('stopped_at') is None and hn.get('n_members_invalid') == 1 and
          0 in (hn.get('counts_by_member') or {}).values() and hn.get('reference_within_error_count') == 43 and
          hn.get('freeze_status') == 'FREEZE_COMPLETE')
    rec('B-E2E-nan_member', 'E2E', ok, res['nan_member'])
    rec('B-E2E-partial', 'E2E', res['partial'].get('stopped_at') == '5_write', res['partial'])
    ok = (res['partial_allow'].get('stopped_at') is None and
          g('partial_allow', '5_write', 'freeze_status') == 'FREEZE_INCOMPLETE' and
          g('partial_allow', '8_score', 'headline', 'freeze_status') == 'FREEZE_INCOMPLETE')
    rec('B-E2E-partial_allow', 'E2E', ok, res['partial_allow'])
    ok = (res['tampered_qm'].get('stopped_at') is None and g('tampered_qm', '7_verify', 'manifest') is False and
          g('tampered_qm', '8_score', 'ok') is False and g('tampered_qm', '8_score', 'echo', 'target_rows_sha256'))
    rec('B-E2E-tampered_qm', 'E2E', ok, res['tampered_qm'])
    e = g('tampered_manifest', '8_score', 'echo') or {}
    ok = (g('tampered_manifest', '8_score', 'ok') is False and e.get('target_rows_sha256') and
          e.get('manifest_file_sha256_actual') and e.get('manifest_file_sha256_actual') != e.get('manifest_file_sha256_expected'))
    rec('B-E2E-tampered_manifest', 'E2E', ok, res['tampered_manifest'])
    ok = (g('forged_registration', '7_verify', 'registration') is True and g('forged_registration', '8_score', 'ok') is False
          and (g('forged_registration', '8_score', 'echo') or {}).get('target_rows_sha256'))
    rec('B-E2E-forged_registration', 'E2E', ok, res['forged_registration'])
    r = res['ddo_1e307']
    ok = ('TIMEOUT' not in r and g('ddo_1e307', '1_engine', 'status') not in ('COMPLETE', None) and
          g('ddo_1e307', '1b_record', 'ok') is True and str(r.get('stopped_at', '')).startswith('1_engine'))
    rec('B-E2E-ddo_1e307', 'E2E', ok, r)
    r = res['ngc_1e307']
    ok = 'TIMEOUT' not in r and 'NO_RESULT' not in r and (
        r.get('stopped_at') is not None or (g('ngc_1e307', '7_verify', 'manifest') is True and g('ngc_1e307', '8_score', 'ok') is True))
    rec('B-E2E-ngc_1e307', 'E2E', ok, r)


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = os.path.join(HERE, 'runs', 'run_%s_%d' % (stamp, os.getpid()))
    os.makedirs(run_dir)
    meta = {'utc': stamp, 'python': sys.version, 'numpy': np.__version__, 'engine_sha256': sha(ENG_PATH),
            'freeze_sha256': sha(FRZ_PATH), 'fixtures_sha256': sha(os.path.realpath(__file__)),
            'plan_sha256': sha(os.path.join(HERE, 'BLIND_FIXTURE_PLAN.md')), 'query_manifest_sha256': sha(QM_REAL)}
    print(json.dumps(meta))
    B = Base(os.path.join(run_dir, 'base'))
    for name, fn in (('base', lambda: fx_base(B)), ('d4', lambda: fx_d4(B)), ('d1', lambda: fx_d1(B)),
                     ('p34_06', lambda: fx_p34_06(B)), ('d2', lambda: fx_d2(B)), ('d3', lambda: fx_d3(B)),
                     ('s8', lambda: fx_s8(B)), ('s10', lambda: fx_s10(B)), ('s11', lambda: fx_s11(B)),
                     ('p34_15', lambda: fx_p34_15(B)), ('p34_14', lambda: fx_p34_14(B)),
                     ('p34_16', lambda: fx_p34_16(B)), ('d8', lambda: fx_d8(B)),
                     ('s2', lambda: fx_s2(run_dir)), ('s1', lambda: fx_s1(run_dir)), ('e2e', lambda: fx_e2e(run_dir))):
        guard('X-' + name, name, fn)
    bad_calls = [c for c in NGC_CALLS if c != ['D_ngc', 'a', 'b', 'i_ngc', 'q']]
    rec('B-D10-calls', 'D10', not bad_calls and len(NGC_CALLS) > 0, {'n_calls': len(NGC_CALLS), 'bad': bad_calls[:3]})
    summary = {'meta': meta, 'n': len(RESULTS), 'n_fail': sum(1 for r in RESULTS if not r['pass'] and not r['id'].startswith('OBS')),
               'failed': [r['id'] for r in RESULTS if not r['pass']], 'results': RESULTS}
    with open(os.path.join(run_dir, 'CHECK_FIXTURE_RESULTS.json'), 'x') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True, default=str)
    print('TOTAL %d  FAIL %d  %s' % (summary['n'], summary['n_fail'], summary['failed']))
    print('RUN_DIR ' + run_dir)


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--sub':
        name, variant, d = sys.argv[2], sys.argv[3], sys.argv[4]
        (sub_s1 if name == 's1' else sub_e2e)(variant, d)
    else:
        main()
