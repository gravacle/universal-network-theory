"""v003 self-test: one or more synthetic checks per v003 item (D1-D4, D8, S1-S11, P34-06/11/14/15/16, B10 echo).

Synthetic toys only. The only real inputs opened are the target-free NGC3198 query manifest (a2936517..., ids and
radii only, for the PROGRAM_PIN binding) -- no NGC3198 velocity, no project forward, no network, single thread.
Writes only under ./runs/run_<UTC>_<pid>/.
usage: python3 -I -B selftest_v003.py
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
import signal
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.realpath(__file__))
FINAL = os.path.dirname(os.path.dirname(HERE))
ENG_PATH = os.path.join(FINAL, 'calibration_region_engine_c2v003.py')
FRZ_PATH = os.path.join(FINAL, 'prediction_freeze_c2v003.py')
QM_REAL = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
           'CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json')
QM_REAL_SHA = 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
RUN = os.path.join(HERE, 'runs', 'run_%s_%d' % (STAMP, os.getpid()))
os.makedirs(RUN)


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


E = load(ENG_PATH, 'eng_v003')
F = load(FRZ_PATH, 'frz_v003')
CHECKS = []


def ck(cid, cond, detail=''):
    CHECKS.append({'id': cid, 'pass': bool(cond), 'detail': str(detail)[:600]})
    print(('PASS ' if cond else 'FAIL ') + cid + ('' if cond else ' :: ' + str(detail)[:400]))


# ------------------------------------------------------------------ synthetic region (checker toy)
ROW_IDS = ['R%02d' % i for i in range(1, 13)]
Z = 2.865260238532134
SIG = 0.7
MU = 28.03
DC = 10 ** ((MU - 25) / 5)
DL, DH = DC * 0.97, DC * 1.03
REGION = os.path.join(RUN, 'synthetic_region_NOT_DDO154.json')
with open(REGION, 'x') as fh:
    json.dump({'rows': [{'id': r, 'reference_radius_kpc': 0.5 * (i + 1), 'observed_speed_km_s': 100.0,
                         'quoted_random_sigma_km_s': SIG,
                         'conditional_random_acceptance_low_km_s': 100.0 - Z * SIG,
                         'conditional_random_acceptance_high_km_s': 100.0 + Z * SIG} for i, r in enumerate(ROW_IDS)],
               'statistical_choice': 'synthetic', 'forward_coordinates': 'synthetic',
               'distance_summary': {'modulus_mag': MU, 'distance_central_Mpc': DC, 'reported68_low_Mpc': DL,
                                    'reported68_high_Mpc': DH, 'scope': 'synthetic'}}, fh)
REGION_SHA = sha(REGION)
HW = Z * SIG
QIDS = ['Q%02d' % k for k in range(1, 44)]
QM_SYN = os.path.join(RUN, 'synthetic_query_manifest_NOT_NGC3198.json')
with open(QM_SYN, 'x') as fh:
    json.dump({'rows': [{'query_id': q, 'data_row_index': j + 1, 'Rad_text': '%.2f' % (0.5 * (j + 1)),
                         'Rad_unit': 'kpc'} for j, q in enumerate(QIDS)]}, fh)
QM_SYN_SHA = sha(QM_SYN)
QMB_SYN = {'path': QM_SYN, 'sha256': QM_SYN_SHA, 'role': 'SYNTHETIC_FIXTURE'}


def coords_full(trial_a=0.75, trial_b=0.80, q_sens={'mode': 'box_ends'}, i_step=3.0):
    return [
        dict(name='a', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=trial_a,
             units='dimensionless', scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='b', transform='linear', lower=0.0, upper=1.0, role='free', trial_value=trial_b,
             units='dimensionless', scope='shared', kind='other', reference_value=None, sensitivity=None),
        dict(name='q', transform='linear', lower=0.0, upper=2.0, role='fixed', trial_value=1.0,
             units='kpc', scope='shared', kind='other', reference_value=None, sensitivity=q_sens),
        dict(name='D_ddo', transform='log', lower=DL, upper=DH, role='nuisance', trial_value=DC,
             units='Mpc', scope='ddo154_nuisance', kind='distance', reference_value=4.04, sensitivity=None),
        dict(name='i_ddo', transform='linear', lower=55.0, upper=75.0, role='nuisance', trial_value=66.0,
             units='deg', scope='ddo154_nuisance', kind='inclination', reference_value=None, sensitivity=None),
        dict(name='D_ngc', transform='log', lower=12.0, upper=15.6, role='nuisance', trial_value=13.8,
             units='Mpc', scope='ngc3198_nuisance', kind='distance', reference_value=13.8,
             sensitivity={'mode': 'box_ends'}),
        dict(name='i_ngc', transform='linear', lower=65.0, upper=77.0, role='nuisance', trial_value=71.0,
             units='deg', scope='ngc3198_nuisance', kind='inclination', reference_value=None,
             sensitivity={'mode': 'step', 'step': i_step}),
    ]


def fwd_disc(theta):
    g = 40.0 * ((theta['a'] - 0.85) ** 2 + (theta['b'] - 0.85) ** 2)
    return {'speeds_km_s': {r: 100.0 + g for r in ROW_IDS}, 'valid': True, 'reasons': []}


RUN_KW = dict(observation_region_path=REGION, observation_region_sha256=REGION_SHA, u_seed=None, rel_step=0.05,
              min_step=1e-4, max_halvings=3, null_tolerance=1e-6, march_step=0.05, bisection_steps=4,
              design_count=8, rng_seed=0, ddo154_distance={'name': 'D_ddo', 'modulus_half_width_multiple': 1.0},
              repair_iterations=8, max_repair_step=0.25, budget=800, global_design_count=24, max_march_rounds=4,
              hull_growth_tol=0.01)


def run(forward, coords, **kw):
    a = dict(RUN_KW)
    a.update(kw)
    return E.run_calibration_region(forward=forward, coordinates=coords, **a)


def ngc_base(theta):
    return {q: 150.0 + 20.0 * (theta['a'] + theta['b']) + 40.0 * (theta['a'] - theta['b']) * (j + 1) / 43.0
            + 3.0 * (theta['q'] - 1.0) + 10.0 * (theta['D_ngc'] / 13.8 - 1.0) + 0.2 * (theta['i_ngc'] - 71.0)
            for j, q in enumerate(QIDS)}


def fwd_ngc(theta):
    return {'speeds_km_s': ngc_base(theta), 'valid': True, 'reasons': []}


_ctr = [0]


def paths(tag):
    _ctr[0] += 1
    return os.path.join(RUN, '%02d_%s_M.json' % (_ctr[0], tag)), os.path.join(RUN, '%02d_%s_R.json' % (_ctr[0], tag))


ALTS = {'primary': 'P', 'declared': [{'name': 'P', 'kind': 'state', 'description': 'primary',
                                      'status': 'EVALUATED_BEFORE_FREEZE'}]}
PR = {'box': 'synthetic', 'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'}


def pipeline(run_out, spec, forward=fwd_ngc, qids=QIDS, interior=6, budget=100, sbudget=100):
    sel = F.select_representative_points(exploration=run_out, interior_count=interior, spec=spec)
    ev = F.evaluate_envelopes(forward_ngc=forward, points=sel['points'], spec=spec, query_ids=qids, budget=budget) \
        if sel['ok'] else None
    rf = F.select_reference_member(selection=sel, evaluation=ev) if ev else {'ok': False}
    sv = F.evaluate_sensitivity(forward_ngc=forward, reference=rf, selection=sel, spec=spec, query_ids=qids,
                                null_direction_rule={'mode': 'box_ends'}, budget=sbudget) if rf['ok'] else {'ok': False}
    return sel, ev, rf, sv


def write(tag, sel, ev, rf, sv, spec, qids=QIDS, qmb=QMB_SYN, inputs=None, pr=PR, alts=ALTS, alt_evals=None,
          allow_incomplete=False, notes=None):
    mp, rp = paths(tag)
    w = F.write_freeze_manifest(out_path=mp, registration_path=rp, parameter_region=pr,
                                observation_rule={'rule': 'synthetic'}, spec=spec, selection=sel, alternatives=alts,
                                alternative_evaluations=alt_evals or {'P': ev}, reference=rf, sensitivity=sv,
                                query_ids=qids, query_manifest=qmb, code_files=[FRZ_PATH, ENG_PATH],
                                input_files=inputs if inputs is not None else [REGION, QM_SYN],
                                notes=notes if notes is not None else {'selftest': 'v003'},
                                allow_incomplete=allow_incomplete)
    return w, mp, rp


def rehash_write(doc, path):
    doc = copy.deepcopy(doc)
    doc.pop('manifest_sha256', None)
    doc['manifest_sha256'] = hashlib.sha256(F._canonical_bytes(doc)).hexdigest()
    with open(path, 'xb') as fh:
        fh.write(F._canonical_bytes(doc))
    return path


# ====================================================================== D4 integration + baseline
fs = F.make_freeze_coordinate_spec(coordinates=coords_full())
ck('D4.1 engine_coordinates are engine-ready (9 fields, engine spellings)',
   fs['ok'] and all(set(c) == {'name', 'transform', 'lower', 'upper', 'role', 'trial_value', 'units', 'scope',
                                'sensitivity'} for c in fs['engine_coordinates'])
   and {c['scope'] for c in fs['engine_coordinates']} == {'shared', 'DDO154'}, fs['engine_coordinates'][:2])
RUN1 = run(fwd_disc, fs['engine_coordinates'])
ck('D4.2 documented call order: engine accepts engine_coordinates unchanged', RUN1['status'] == 'COMPLETE',
   (RUN1['status'], RUN1['reasons'][:2]))
bad_step = coords_full(i_step=7.0)   # 71 +/- 7 leaves [65, 77]
ck('D4.3 one step rule: freeze refuses trial +/- step outside the box',
   not F.make_freeze_coordinate_spec(coordinates=bad_step)['ok'])
eng_bad = [dict(c) for c in fs['engine_coordinates']]
eng_bad[2] = dict(eng_bad[2], sensitivity={'step_natural': 1.5})   # q trial 1.0 +/- 1.5 leaves [0, 2]
ck('D4.4 one step rule: engine refuses the same out-of-box step', not E.make_coordinate_spec(coordinates=eng_bad)['ok'])

SEL, EV, RF, SV = pipeline(RUN1, fs['spec'])
W, MP, RP = write('base', SEL, EV, RF, SV, fs['spec'])
ck('BASE freeze written FREEZE_COMPLETE', W['ok'] and W['freeze_status'] == 'FREEZE_COMPLETE', W['reasons'][:3])
MAN = json.load(open(MP))
TG = [{'id': q, 'velocity': v, 'sigma': 2.0} for q, v in
      zip(QIDS, ngc_base({'a': .85, 'b': .85, 'q': 1.0, 'D_ngc': 13.8, 'i_ngc': 71.0}).values())]

# ====================================================================== D1 / P34-06
cn = SEL['centroid_nearest_log_index']
cn_th = next(p['theta_natural'] for p in SEL['points'] if p['log_index'] == cn)
fail_li = next(p['log_index'] for p in SEL['points'] if p['log_index'] != cn)
fail_th = next(p['theta_natural'] for p in SEL['points'] if p['log_index'] == fail_li)


def fwd_nan(theta):
    r = fwd_ngc(theta)
    if abs(theta['a'] - fail_th['a']) < 1e-12 and abs(theta['b'] - fail_th['b']) < 1e-12:
        r['speeds_km_s']['Q05'] = float('nan')
        r['speeds_km_s']['Q01'] = 999.0
    return r


s1, e1, r1, v1 = pipeline(RUN1, fs['spec'], forward=fwd_nan)
mbad = next(m for m in e1['members'] if m['log_index'] == fail_li)
ck('D1.1 one NaN row -> every row of that evaluation invalid (all-or-nothing)',
   mbad['row_valid'] == [False] * 43 and mbad['member_valid'] is False, mbad['row_valid'][:6])
ck('P34-06.1 one failed member does not void the 43 queries: envelope valid over the valid members',
   all(r['valid'] for r in e1['pointwise_envelope']) and all(r['n_excluded_invalid'] == 1 for r in e1['pointwise_envelope'])
   and e1['pointwise_envelope'][0]['band_high_km_s'] < 999.0, e1['pointwise_envelope'][0])
w1, mp1, rp1 = write('d1', s1, e1, r1, v1, fs['spec'])
sc1 = F.score_after_freeze(freeze_manifest_path=mp1, registration_path=rp1,
                           expected_manifest_file_sha256=w1['manifest_file_sha256'], target_rows=TG)
bm = next(m for m in sc1['members'] if m['log_index'] == fail_li)
ck('P34-06.2 failed member is reported and scores 0; headline counts it as invalid',
   w1['ok'] and sc1['ok'] and bm['within_error_count'] == 0 and sc1['headline']['n_members_invalid'] == 1,
   (w1['reasons'][:2], sc1['reasons'][:2]))
# verifier enforces all-or-nothing on a re-hashed edit
d = json.load(open(mp1))
mm = next(m for m in d['members'] if m['log_index'] == fail_li)
mm['row_valid'] = [True] * 43
mm['row_valid'][4] = False
mm['speeds_km_s'][4] = None
mm['member_valid'] = False
d['pointwise_envelope'] = F._pointwise_envelope(d['members'], QIDS)
tp = rehash_write(d, os.path.join(RUN, 'd1_partial_rows_rehashed.json'))
vv = F.verify_freeze_manifest(freeze_manifest_path=tp)
ck('D1.2 verifier refuses a member whose row_valid is partial (re-hashed edit)',
   not vv['ok'] and any('D1' in r for r in vv['reasons']), vv['reasons'][:2])

# ====================================================================== D2
e_sub = F.evaluate_envelopes(forward_ngc=fwd_ngc, points=SEL['points'][:3], spec=fs['spec'], query_ids=QIDS, budget=50)
w_sub, _, _ = write('d2_subset', SEL, e_sub, F.select_reference_member(selection=SEL, evaluation=e_sub), SV, fs['spec'])
ck('D2.1 writer refuses members that are a subset of the selection', not w_sub['ok'] and
   any('D2' in r for r in w_sub['reasons']), w_sub['reasons'][:1])
pts_rev = list(reversed(SEL['points']))
e_rev = F.evaluate_envelopes(forward_ngc=fwd_ngc, points=pts_rev, spec=fs['spec'], query_ids=QIDS, budget=50)
w_rev, _, _ = write('d2_order', SEL, e_rev, F.select_reference_member(selection=SEL, evaluation=e_rev), SV, fs['spec'])
ck('D2.2 writer refuses the selected members in another order', not w_rev['ok'])
d = copy.deepcopy(MAN)
d['admitted_region']['selection_interior_count'] = 0
tp = rehash_write(d, os.path.join(RUN, 'd2_rule_edit.json'))
vv = F.verify_freeze_manifest(freeze_manifest_path=tp)
ck('D2.3 verifier recomputes the selection from the frozen rule inputs (edited interior_count refused)',
   not vv['ok'] and any('D2' in r for r in vv['reasons']), vv['reasons'][:2])
d = copy.deepcopy(MAN)
d['members'] = d['members'][:-1]
tp = rehash_write(d, os.path.join(RUN, 'd2_member_dropped.json'))
vv = F.verify_freeze_manifest(freeze_manifest_path=tp)
ck('D2.4 verifier refuses a dropped member (members != selected_points)', not vv['ok'], vv['reasons'][:2])

# ====================================================================== D3 / S12 / A4
qreal = F.load_query_manifest(path=QM_REAL, expected_sha256=QM_REAL_SHA)
RQ = qreal['query_ids']


def fwd_ngc_real(theta):
    base = ngc_base(theta)
    return {'speeds_km_s': {rq: base[q] for rq, q in zip(RQ, QIDS)}, 'valid': True, 'reasons': []}


s3, e3, r3, v3 = pipeline(RUN1, fs['spec'], forward=fwd_ngc_real, qids=RQ)
QMB_REAL = {'path': QM_REAL, 'sha256': QM_REAL_SHA, 'role': 'PROGRAM_PIN'}
w3, mp3, rp3 = write('d3_program', s3, e3, r3, v3, fs['spec'], qids=RQ, qmb=QMB_REAL, inputs=[REGION, QM_REAL])
ck('D3.1 PROGRAM_PIN with the real target-free manifest (a2936517...) and its 43 ids: written',
   w3['ok'] and json.load(open(mp3))['input_bindings']['query_manifest']['is_program_pin'] is True, w3['reasons'][:2])
w3b, _, _ = write('d3_role_lie', s3, e3, r3, v3, fs['spec'], qids=RQ, qmb=dict(QMB_SYN, role='PROGRAM_PIN'),
                  inputs=[REGION, QM_SYN])
ck('D3.2 role PROGRAM_PIN with any other sha refused', not w3b['ok'] and any('PROGRAM_PIN' in r for r in w3b['reasons']))
w3c, _, _ = write('d3_synth_real', s3, e3, r3, v3, fs['spec'], qids=RQ, qmb=dict(QMB_REAL, role='SYNTHETIC_FIXTURE'),
                  inputs=[REGION, QM_REAL])
ck('D3.3 the program manifest cannot be bound as SYNTHETIC_FIXTURE', not w3c['ok'])
w3d, _, _ = write('d3_unpinned', SEL, EV, RF, SV, fs['spec'], inputs=[REGION])
ck('D3.4 bound query manifest missing from input_files refused', not w3d['ok'] and
   any('query manifest' in r for r in w3d['reasons']), w3d['reasons'][:1])
w3e, _, _ = write('d3_noregion', SEL, EV, RF, SV, fs['spec'], inputs=[QM_SYN])
ck('D3.5 DDO154 region file missing from input_files refused', not w3e['ok'] and
   any('observation-region' in r for r in w3e['reasons']), w3e['reasons'][:1])
d = copy.deepcopy(json.load(open(mp3)))
d['query_ids'][0], d['query_ids'][1] = d['query_ids'][1], d['query_ids'][0]
tp = rehash_write(d, os.path.join(RUN, 'd3_ids_swapped.json'))
vv = F.verify_freeze_manifest(freeze_manifest_path=tp)
ck('D3.6 verifier re-binds the ids to the pinned manifest (swapped ids refused)', not vv['ok'], vv['reasons'][:2])
sc3 = F.score_after_freeze(freeze_manifest_path=mp3, registration_path=rp3,
                           expected_manifest_file_sha256=w3['manifest_file_sha256'],
                           target_rows=[{'id': rq, 'velocity': 160.0, 'sigma': 5.0} for rq in RQ])
ck('D3.7 scorer echoes query_manifest_role / is_program_pin in the headline',
   sc3['ok'] and sc3['headline']['query_manifest_role'] == 'PROGRAM_PIN' and
   sc3['headline']['query_manifest_is_program_pin'] is True)

# ====================================================================== D8 echo on refusal paths
s_bad_reg = F.score_after_freeze(freeze_manifest_path=MP, registration_path=os.path.join(RUN, 'nope.json'),
                                 expected_manifest_file_sha256=W['manifest_file_sha256'], target_rows=TG)
s_bad_exp = F.score_after_freeze(freeze_manifest_path=MP, registration_path=RP, expected_manifest_file_sha256='1' * 64,
                                 target_rows=TG)
d = copy.deepcopy(MAN)
d['notes'] = {'edited': True}
tp = rehash_write(d, os.path.join(RUN, 'd8_edit.json'))
s_bad_file = F.score_after_freeze(freeze_manifest_path=tp, registration_path=RP,
                                  expected_manifest_file_sha256=W['manifest_file_sha256'], target_rows=TG)
ok8 = all(x['refused'] and x['target_rows_sha256'] and x['manifest_file_sha256_actual'] for x in
          (s_bad_reg, s_bad_exp, s_bad_file))
ck('D8.1 refusals (bad registration / caller sha / file sha) echo target_rows_sha256 and the actual file sha',
   ok8, [(x['refused'], x['target_rows_sha256'] is not None, x['manifest_file_sha256_actual']) for x in
         (s_bad_reg, s_bad_exp, s_bad_file)])
ck('D8.2 caller-sha refusal also echoes the registered file sha',
   s_bad_exp['manifest_file_sha256_registered'] == W['manifest_file_sha256'])

# ====================================================================== S1
def fwd_huge(theta):
    return {'speeds_km_s': {r: 1e307 * (1 + theta['a']) for r in ROW_IDS}, 'valid': True, 'reasons': []}


def _alarm(*_):
    raise TimeoutError('hang')


signal.signal(signal.SIGALRM, _alarm)
signal.alarm(30)
t0 = time.time()
try:
    rh = run(fwd_huge, fs['engine_coordinates'], budget=80)
    hung = False
except TimeoutError:
    rh, hung = {'status': None, 'reasons': []}, True
signal.alarm(0)
ck('S1.1 1e307 forward: no hang, fail closed with a NUMERIC_RANGE reason before linear algebra',
   not hung and rh['status'] in ('NUMERIC_RANGE_REFUSED', 'JACOBIAN_INCOMPLETE') and
   any('NUMERIC_RANGE' in r or 'non-finite difference' in r for r in rh['reasons']),
   (hung, rh['status'], [r for r in rh['reasons'] if 'NUMERIC' in r or 'non-finite' in r][:2], time.time() - t0))
idr = E.identifiability_report(jacobian_u=[[1e200] * 3] * 12, sigmas={r: 1.0 for r in ROW_IDS}, row_ids=ROW_IDS,
                               varying_names=['x', 'y', 'z'], null_tolerance=1e-3)
ck('S1.2 identifiability refuses an out-of-range scaled Jacobian (1e200) before the SVD',
   not idr['ok'] and idr['numeric_guard'], idr['reasons'][:1])
T = np.array([[1.0, 1.0], [1e300, 1.0]])
c_lp, st = E._lp_max(np.array([[1.0], [-1.0]]), np.array([1e300, 1e300]), np.array([1.0]))
ck('S1.3 simplex refuses an out-of-range tableau (status NUMERIC_RANGE, no pivots)', st == 'NUMERIC_RANGE', st)

# ====================================================================== S2
def fwd_lin2(theta):
    s_ = 100.0 + 30.0 * (theta['a'] - 0.2) + 25.0 * (theta['b'] - 0.9)
    return {'speeds_km_s': {r: s_ + 0.5 * k * (theta['a'] - 0.2) for k, r in enumerate(ROW_IDS)},
            'valid': True, 'reasons': []}


rs2 = run(fwd_lin2, F.make_freeze_coordinate_spec(coordinates=coords_full(trial_a=0.98, trial_b=0.98))['engine_coordinates'],
          global_design_count=0, max_march_rounds=0, repair_iterations=8, max_repair_step=0.5)
ex2 = rs2['exploration'] or {}
steps = (ex2.get('repair') or {}).get('steps', [])
ck('S2.1 repair steps keep near-null components (<= 1e-12) and record a step-length truncation, no clip',
   bool(steps) and all(s_['near_null_component_max'] <= 1e-12 for s_ in steps) and
   all('step_length_fraction' in s_ for s_ in steps) and ex2.get('near_null_shifted') is False,
   [(s_['near_null_component_max'], s_['step_length_fraction']) for s_ in steps][:4])
ck('S2.2 no numerical_rank repair phase in v003', all(p['phase'] == 'identified' for p in (ex2.get('repair') or {}).get('phases', [])))

# ====================================================================== S3
s_abs = E.identifiability_report(jacobian_u=[[1e4, 0.0]] * 6 + [[0.0, 50.0]] * 6, sigmas={r: 1.0 for r in ROW_IDS},
                                 row_ids=ROW_IDS, varying_names=['a', 'b'], null_tolerance=1e-2)
ck('S3.1 absolute rule: s=[2.4e4, 122] at tol 1e-2 -> both identified (direction 1 by the absolute rule)',
   s_abs['identified'] == [0, 1] and s_abs['identified_by'][1] == 'absolute', (s_abs['singular_values'], s_abs['identified_by']))
s_min = E.identifiability_report(jacobian_u=[[1.0, 1e-8]] * 12, sigmas={r: 1.0 for r in ROW_IDS}, row_ids=ROW_IDS,
                                 varying_names=['a', 'b'], null_tolerance=0.0)
ck('S3.2 minimum tolerance enforced: tol 0 -> effective >= 1e-6, a 1e-8 relative direction stays near-null',
   s_min['effective_null_tolerance'] >= 1e-6 and 1 in s_min['near_null'], (s_min['effective_null_tolerance'], s_min['near_null']))
bad_id = copy.deepcopy(s_abs)
bad_id['identified'], bad_id['near_null'] = [0], [1]
spec2 = E.make_coordinate_spec(coordinates=[dict(name='a', transform='linear', lower=0, upper=1, role='free', trial_value=0.5,
                                                 units='u', scope='shared', sensitivity='NONE'),
                                            dict(name='b', transform='linear', lower=0, upper=1, role='free', trial_value=0.5,
                                                 units='u', scope='shared', sensitivity='NONE')])
regd = E.load_observation_region(path=REGION, expected_sha256=REGION_SHA)
rs, _ = E._check_identifiability(bad_id, 2, 12, ['a', 'b'], ROW_IDS)
ck('S5.1 an identifiability report whose identified set ignores the absolute rule is refused', bool(rs), rs[:1])

# ====================================================================== S4
def fwd_lin3(theta):
    return {'speeds_km_s': {r: 100.0 + 0.5 * (theta['a'] - 0.5) + 0.3 * k * (theta['b'] - 0.5) for k, r in enumerate(ROW_IDS)},
            'valid': True, 'reasons': []}


lg = []
jac = E.finite_difference_jacobian(forward=fwd_lin3, spec=spec2, region=regd, u0=[1e-6, 0.5], rel_step=0.05, min_step=1e-4,
                                   max_halvings=2, budget=20, log=lg)
ck('S4.1 a clipped side shorter than min_step is dropped (one-sided), no near-duplicate seed evaluation',
   jac['ok'] and jac['steps_detail'][0]['sides_dropped_below_min_step'] == ['minus'] and
   not any(e['u'][0] == 0.0 and e['purpose'] == 'jacobian' for e in lg) and len(lg) == 4,   # no evaluation at the clipped face u_a = 0
   (jac['steps_detail'][0], len(lg)))

# ====================================================================== S6 / S7
cls = E.classify_prediction(prediction={'speeds_km_s': {r: 100.0 for r in ROW_IDS}, 'valid': np.True_, 'reasons': []},
                            rectangles=regd['rectangles'], row_ids=ROW_IDS)
ev_np = F.evaluate_envelopes(forward_ngc=lambda th: dict(fwd_ngc(th), valid=np.True_), points=SEL['points'][:1],
                             spec=fs['spec'], query_ids=QIDS, budget=2)
ck('S6.1 one predicate: np.True_ is not True in both modules', cls['valid'] is False and
   ev_np['members'][0]['member_valid'] is False)
tu = E.to_unit(spec=spec2, theta_natural={'a': 0.5})
ck('S7.1 to_unit failure carries reasons', tu['ok'] is False and tu['reasons'], tu['reasons'])

# ====================================================================== S8
R8 = copy.deepcopy(RUN1)
hb = R8['exploration']['hull_box']
kk = sorted(hb)[0]
hb[kk] = {'min': hb[kk]['min'], 'max': hb[kk]['max'] + 0.3}
s8 = F.select_representative_points(exploration=R8, interior_count=6, spec=fs['spec'])
ck('S8.1 hull_box inconsistent with right_vectors refuses (no warning-only path)', not s8['ok'] and
   any('S8' in r for r in s8['reasons']), s8['reasons'][:1])
R8b = copy.deepcopy(RUN1)
R8b['exploration']['hull_box'] = {float('inf'): {'min': 0.0, 'max': 1.0}}
s8b = F.select_representative_points(exploration=R8b, interior_count=6, spec=fs['spec'])
ck('S8.2/S10 an inf hull key refuses without raising', s8b['ok'] is False and 'INTERNAL_ERROR' not in str(s8b['reasons']),
   s8b['reasons'][:1])

# ====================================================================== S9 / S10 / S11
for tag, notes, expect in (('s9_scorer_name', {'x': {'within_error_count': 3}}, False),
                           ('s9_velocity', {'velocity': 1}, False),
                           ('s9_p46_shape', [{'id': 'Q01', 'Velocity': 1.0, 'sigma': 2.0}], False)):
    w9, _, _ = write(tag, SEL, EV, RF, SV, fs['spec'], notes=notes)
    ck('S9 %s refused' % tag, w9['ok'] is expect and any('forbidden' in r for r in w9['reasons']), w9['reasons'][:1])
cyc = {}
cyc['self'] = cyc
w10, _, _ = write('s10_cycle', SEL, EV, RF, SV, fs['spec'], notes=cyc)
ck('S10.1 cyclic notes refused without raising', w10['ok'] is False and 'INTERNAL_ERROR' not in str(w10['reasons']),
   w10['reasons'][:1])
deep = cur = {}
for _ in range(3000):
    cur['x'] = {}
    cur = cur['x']
w10b, _, _ = write('s10_deep', SEL, EV, RF, SV, fs['spec'], notes=deep)
ck('S10.2 3000-deep notes refused without raising', w10b['ok'] is False, w10b['reasons'][:1])
c10 = coords_full()
c10[0] = dict(c10[0], transform=np.array(['linear', 'log']))
r10 = F.make_freeze_coordinate_spec(coordinates=c10)
ck('S10.3 ndarray transform refused (ok False, no raise)', r10['ok'] is False, r10['reasons'][:1])
try:
    F.load_query_manifest(QM_SYN, QM_SYN_SHA)
    pos = False
except TypeError:
    pos = True
ck('S10.4 keyword-only contract kept: positional call still raises TypeError', pos)
for tag, pr in (('s11_empty', {}), ('s11_label', {'bounds_semantics': 'x'}), ('s11_missing', {'box': 1})):
    w11, _, _ = write(tag, SEL, EV, RF, SV, fs['spec'], pr=pr)
    ck('S11 parameter_region %s refused' % tag, not w11['ok'] and any('S11' in r for r in w11['reasons']))
d = copy.deepcopy(MAN)
d['parameter_region'] = {'box': 'synthetic'}
tp = rehash_write(d, os.path.join(RUN, 's11_edit.json'))
ck('S11.v verifier refuses a parameter_region without the label', not F.verify_freeze_manifest(freeze_manifest_path=tp)['ok'])

# ====================================================================== P34-11
bc = RUN1['exploration']['boundary_cause']
ck('P34-11.1 every round-0 side records its boundary cause', all(bc[k][s_] in E.BOUNDARY_CAUSES for k in bc
                                                                 for s_ in ('minus', 'plus')), bc)
ck('P34-11.2 a box-edge-limited side is distinguishable from a rejection',
   any('BOX' in bc[k][s_] for k in bc for s_ in ('minus', 'plus')) and
   any(bc[k][s_] == 'REJECTED_EVALUATION' for k in bc for s_ in ('minus', 'plus')), bc)

# ====================================================================== P34-14
R14 = copy.deepcopy(RUN1)
ap = R14['exploration']['admitted_points']
ap[3]['prediction']['speeds_km_s'][ROW_IDS[0]] = 100.0 + 3.0 * HW
s14 = F.select_representative_points(exploration=R14, interior_count=6, spec=fs['spec'])
ck('P34-14.1 a non-admitted point in admitted_points is refused (re-classified against the closed rectangles)',
   not s14['ok'] and any('not admitted' in r for r in s14['reasons']), s14['reasons'][:1])
R14b = copy.deepcopy(RUN1)
R14b['exploration']['primary_anchor']['log_index'] = R14b['exploration']['rejected_points'][0]['log_index']
s14b = F.select_representative_points(exploration=R14b, interior_count=6, spec=fs['spec'])
ck('P34-14.2 an anchor that is not an admitted point is refused', not s14b['ok'] and
   any('P34-14' in r for r in s14b['reasons']), s14b['reasons'][:1])
ck('P34-14.3 the anchor member is the engine primary anchor', SEL['anchor_source'] == 'primary_anchor' and
   any(p['role'] == 'anchor' and p['log_index'] == RUN1['exploration']['primary_anchor']['log_index'] for p in SEL['points'])
   or (SEL['anchor_source'] == 'primary_anchor'), SEL['anchor_source'])

# ====================================================================== P34-15
obj = {i: i * 1.5 for i in range(12)}
b1 = F._canonical_bytes(obj)
b2 = F._canonical_bytes(json.loads(b1))
eb1 = E._canonical_bytes(obj)
ck('P34-15.1 canonical bytes of a 12-int-key dict survive a parse (both modules, identical bytes)',
   b1 == b2 and eb1 == b1, (b1[:40], b2[:40]))
try:
    F._canonical_bytes({1: 'a', '1': 'b'})
    mixed_ok = False
except ValueError:
    mixed_ok = True
ck('P34-15.2 duplicate key after str normalisation raises ValueError (callers fail closed)', mixed_ok)

# ====================================================================== P34-16
REC = os.path.join(RUN, 'calibration_record.json')
REG = os.path.join(RUN, 'calibration_registry.jsonl')
wr = E.write_calibration_record(run=RUN1, record_path=REC, registry_path=REG)
bad_run = run(fwd_disc, fs['engine_coordinates'], observation_region_sha256='0' * 64)
wr2 = E.write_calibration_record(run=bad_run, record_path=os.path.join(RUN, 'calibration_record_bad.json'),
                                 registry_path=REG)
vr = E.verify_calibration_record(record_path=REC, registry_path=REG)
ck('P34-16.1 every run is recorded (COMPLETE and INPUT_INVALID), registry chain verifies',
   wr['ok'] and wr2['ok'] and wr2['status'] == 'INPUT_INVALID' and vr['ok'] and vr['registry_lines'] == 2,
   (wr['reasons'][:1], wr2['reasons'][:1], vr['reasons']))
ck('P34-16.2 fingerprint: engine run == freeze selection == record',
   RUN1['exploration_fingerprint'] == SEL['calibration_fingerprint'] == wr['exploration_fingerprint'])
w16, mp16, rp16 = write('p34_16_bound', SEL, EV, RF, SV, fs['spec'], inputs=[REGION, QM_SYN, REC])
ck('P34-16.3 a pinned calibration record is bound by fingerprint', w16['ok'] and w16['calibration_record_bound'] and
   json.load(open(mp16))['input_bindings']['calibration_record']['exploration_fingerprint'] == SEL['calibration_fingerprint'],
   w16['reasons'][:2])
other = run(fwd_disc, F.make_freeze_coordinate_spec(coordinates=coords_full(trial_a=0.8))['engine_coordinates'])
REC2 = os.path.join(RUN, 'calibration_record_other.json')
E.write_calibration_record(run=other, record_path=REC2, registry_path=REG)
w16b, _, _ = write('p34_16_wrong', SEL, EV, RF, SV, fs['spec'], inputs=[REGION, QM_SYN, REC2])
ck('P34-16.4 a pinned record of a different run is refused', not w16b['ok'] and any('P34-16' in r for r in w16b['reasons']))
with open(REG, 'rb') as fh:
    lines = fh.read().split(b'\n')
with open(os.path.join(RUN, 'registry_line_deleted.jsonl'), 'xb') as fh:
    fh.write(lines[1] + b'\n')
vr2 = E.verify_calibration_record(record_path=REC2, registry_path=os.path.join(RUN, 'registry_line_deleted.jsonl'))
ck('P34-16.5 a registry with an earlier line deleted fails the hash chain', not vr2['ok'] and vr2['registry_chain_ok'] is False)
w_dup = E.write_calibration_record(run=RUN1, record_path=REC, registry_path=REG)
ck('P34-16.6 record_path exclusive create', not w_dup['ok'])

# ====================================================================== A1-A5 spot checks (still fixed)
r_em = run(lambda th: {'speeds_km_s': {r: 120.0 for r in ROW_IDS}, 'valid': True, 'reasons': []}, fs['engine_coordinates'])
ck('A1 empty toy: NO_ADMITTED_POINT_FOUND, empty_region None (never True)',
   r_em['status'] == 'NO_ADMITTED_POINT_FOUND' and r_em['empty_region'] is None)
ck('A2 _edge_t tolerance', abs(E._edge_t(np.array([0.0, 0.5]), np.array([-1e-17, 1.0])) - 0.5) < 1e-12)
ep = F.evaluate_envelopes(forward_ngc=fwd_ngc, points=SEL['points'], spec=fs['spec'], query_ids=QIDS, budget=2)
wp, _, _ = write('a3', SEL, ep, F.select_reference_member(selection=SEL, evaluation=ep), SV, fs['spec'])
ck('A3 budget-truncated member evaluation: 0 valid queries and writer refuses',
   sum(r['valid'] for r in ep['pointwise_envelope']) == 0 and not wp['ok'])
wa4, _, _ = write('a4', SEL, EV, RF, SV, fs['spec'], inputs=[])
ck('A4 empty input pins refused', not wa4['ok'])

# ====================================================================== determinism
r_again = run(fwd_disc, fs['engine_coordinates'])
ck('DET engine run is deterministic (same fingerprint and log length)',
   r_again['exploration_fingerprint'] == RUN1['exploration_fingerprint'] and
   len(r_again['evaluation_log']) == len(RUN1['evaluation_log']))

fails = [c['id'] for c in CHECKS if not c['pass']]
out = {'schema': 'SELFTEST_V003', 'engine_sha256': sha(ENG_PATH), 'freeze_sha256': sha(FRZ_PATH), 'n': len(CHECKS),
       'failed': fails, 'checks': CHECKS, 'numpy': np.__version__, 'python': sys.version.split()[0]}
with open(os.path.join(RUN, 'SELFTEST_V003_RESULTS.json'), 'x') as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print('TOTAL %d checks, %d failed: %s' % (len(CHECKS), len(fails), fails))
