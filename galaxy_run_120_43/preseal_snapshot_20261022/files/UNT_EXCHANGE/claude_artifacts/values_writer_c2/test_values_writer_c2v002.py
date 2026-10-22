"""Synthetic tests for values_writer_c2v002 (python3 -I -B; numpy). No solver runs and no real NGC field is computed:
every TailState, call tree, rotation array and column-mean record here is synthetic. The only real records read are
the S0 certificate files in ngc_point_producer_c4/s0/build_c4v001/out (read-only; certificate checks only) and the
pinned source files whose cited lines the report relies on (byte and line evidence only).

Usage: python3 -I -B test_values_writer_c2v002.py --module <writer.py> --work <new dir> [--quick]
"""
import argparse
import bisect
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
S0_OUT = ART + '/ngc_point_producer_c4/s0/build_c4v001/out/'
REAL_EPS = {  # file name -> sha256 (Claude4 0199; A148)
    'S0_POINT_EPS_968c915bece706ea_C4V002_s0seed.json': 'efdc430a561ae936d860f85ec050f22a10f17c03aad7ad17fc2150744dcde563',
    'S0_POINT_EPS_3d7785669b549d6f_C4V002_s0j0.json': '8270b6b3eb9daddd01e32f7c6cc0fd143afd6b751ff9ced310ac92ca365586da',
    'S0_POINT_EPS_ab7bf95317b37652_C4V002_s0j1.json': 'bfac8f57233e904aed30f68594645b5b9c97697e47ce088e9d18e7a8fe4aff1e',
    'S0_POINT_EPS_4b9b4ec88eb2d94c_C4V002_s0j2.json': '5dd9900a7db31003cb1b1054c156f6ac73b062375bae3a423990e782a2ccfdfc'}
REAL_REFUSED = ('BIND_CHECK_S0_968c915bece706ea_C4V002_bind1.json', 'BIND_CHECK_S0_3d7785669b549d6f_C4V002_bind2.json',
                'BIND_CHECK_S0_ab7bf95317b37652_C4V002_bind3.json', 'BIND_CHECK_S0_4b9b4ec88eb2d94c_C4V002_bind4.json',
                'SMOKE_ANCHOR_POINT_EPS_C4V002_smoke1.json', 'S0_POINT_EPS_968c915bece706ea_C4V002_s0seed_RUN_START.json')
PHASE1_V003 = (ART + '/phase1_c2/phase1_c2v003.py', '149ed4cbe1ad96e941ce01ad4cff46369dd559a9eee4356e155ad069f4a7b406')
SRB_ADAPTER = (ART + '/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py',
               '08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a')
LIB_V003 = (ART + '/tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py',
            'e733eb1ebfe2137a6f58d0e35caa345525756e3896ca729c1ba15a39204c7155')
ROT_STAGE = (ART + '/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/'
             'ngc_free_surface_rotation_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py',
             'e22e79e80a63825458ca659dd32c81bef473e170ba81486ef9db86929007249f')
DRIVER = (ART + '/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
          '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377')
V006 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
        'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md')
KPC = 3.085677581491367e19
C = 299792458.0
PRODUCER_SHA = '8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235'
LO_PIN = {'path': '/synthetic/LO_TEST_ONLY.json', 'sha256': 'e' * 64}
RESULTS = []


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def load(path, name):
    raw = Path(path).read_bytes()
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    m.__file__ = path
    exec(compile(raw, path, 'exec'), m.__dict__)
    return m


def wjson(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'xb') as f:
        f.write(json.dumps(obj, indent=1).encode())
    return {'path': str(path), 'sha256': sha_bytes(path.read_bytes())}


def wnpz(path, arrays):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'xb') as f:
        np.savez(f, **arrays)
    return {'path': str(path), 'sha256': sha_bytes(path.read_bytes())}


def record(name, ok, detail=''):
    RESULTS.append({'test': name, 'ok': bool(ok), 'detail': str(detail)[:400]})


def expect_refused(W, name, code, fn):
    try:
        fn()
    except W.Refused as exc:
        record(name, exc.code == code, 'refused %s (want %s): %s' % (exc.code, code, exc))
        return
    except Exception as exc:     # noqa: BLE001 (a crash is not the stated refusal)
        record(name, False, 'raised %s: %s (want Refused %s)' % (type(exc).__name__, exc, code))
        return
    record(name, False, 'no refusal (want %s)' % code)


# ------------------------------------------------------------------------------------------------ fixtures
def cert_shells(scale=1.0, env_ratio=0.9):
    out = []
    for lo in range(2, 91):
        e = scale * 8e-4 * (lo / 2.0) ** -1.4
        out.append({'range_inverse_kpc': [float(lo), float(lo + 1)], 'lo_inverse_kpc': float(lo),
                    'hi_inverse_kpc': float(lo + 1), 'eps': e, 'eps_source': 'envelope',
                    'flat': {'eps_envelope': e * env_ratio, 'eps_actual_set': e * 0.5},
                    'envelope': {'eps_envelope': e * env_ratio}})
    return out


def make_cert(work, tag, key, role='seed', over=None, scale=1.0, eps_max=123.0):
    rec = {'schema': 'UNT_CLAUDE4_S0_POINT_EPS_C4V002', 'label': 'SYNTHETIC TEST CERTIFICATE', 'mode': 'point',
           'gate': 'EPS', 'verdict': 'CERTIFIED', 'certificate': True, 'coverage_inverse_kpc': {'NGC': [2.0, 91.0]},
           'summary': {'rule_verdict': 'CERTIFIED', 'n_shells': 89}, 'eps_max': eps_max,
           'point': {'key': key, 'role': role},
           'key_check': {'equals_point_key': True, 'from_theta_hex': key, 'from_theta_natural': key},
           'producer': {'path': '/synthetic/eps_ngc_point_c4v002.py', 'sha256': PRODUCER_SHA},
           'shells': cert_shells(scale)}
    if over:
        rec = over(rec)
    return wjson(Path(work) / ('cert_%s.json' % tag), rec), rec


def state_arrays(kmin=32.0, nshell=60, beyond=False):
    edges = kmin + np.arange(0, nshell + 1, dtype=float)
    B = np.zeros((nshell, 3))
    for i in range(nshell):
        if edges[i] < 90.51 or beyond:
            B[i] = [1e-7 * (1 + 0.01 * i), 3e-27 * (1 + 0.02 * i), 1e-46 * (1 + 0.03 * i)]
    return {'shell_edges_inverse_kpc': edges, 'shell_integrals': B}


def build_point(W, work, tag, key, *, cert=None, hooks=None, kmin=32.0, beyond=False, empty=False, incl=(1.2, 1.2),
                omega_sign=1.0, lapse_scale=1.0):
    """A synthetic point: certificate, call tree <work>/<tag>/call/out, and its le2_rotation TailState files."""
    lib, _rows = W.modules()
    hooks = hooks or {}
    h = lambda k, x: hooks[k](x) if k in hooks else x      # noqa: E731
    root = Path(work) / tag
    cert_pin, cert_rec = cert if cert is not None else make_cert(root, tag, key)
    out = root / 'call' / 'out'
    rot = out / 'stages' / '07_le2_rotation' / 'rotation'
    obs = out / 'stages' / '08_le2_column_mean' / 'observation'
    # rotation arrays (the stage's own rotation_base_arrays.npz)
    NR, NPHI, NZ = 9, 3, 4
    R = KPC * np.arange(1, NR + 1, dtype=float)
    vz = 1.5e5 * (1 + 0.05 * np.arange(NZ))[None, :] * (1 + 0.1 * np.arange(NR))[:, None]
    omega = omega_sign * (vz / R[:, None]) ** 2
    rng = np.random.default_rng(7)
    fields = (rng.normal(0, 1e-7, (NR, NPHI, NZ, 10)) + 0j)
    fields[..., 0] = lapse_scale * (-1e-6 * (1 + 0.3 * np.arange(NR))[:, None, None] * (1 + 0.1 * np.arange(NZ))[None, None, :]
                                    * (1 + 0.05 * np.arange(NPHI))[None, :, None]) + 0j
    rot_arrays = h('rot_arrays', {'radial_nodes_m': R, 'rotation_Omega_squared': omega, 'full_fields_complex': fields,
                                  'z': np.zeros((NR, NPHI, NZ))})
    arrays_pin = wnpz(rot / 'rotation_base_arrays.npz', rot_arrays)
    # tail state (record + arrays) of that stage
    st_arr = {} if empty else state_arrays(kmin, beyond=beyond)
    st_rec = h('state_record', {'schema': lib.STATE_SCHEMA, 'stage_kind': 'le_rotation', 'c_m_s': C, 'empty': empty,
                                'eps_certificate': dict(cert_pin), 'lo_certificate': dict(LO_PIN), 'roster_digest': 'ab' * 32,
                                'config_sha256': 'cd' * 32, 'kept': {'shape': 'cube', 'K_inverse_kpc': kmin}})
    st = lib.TailState(empty=empty, record=st_rec, arrays=st_arr)
    tail = {'record': wjson(root / 'tail' / 'TAIL_STATE_RECORD.json', st_rec),
            'arrays': wnpz(root / 'tail' / 'TAIL_STATE_ARRAYS.npz', h('state_arrays', st_arr))}
    fin = h('finish', {'status': 'LAGGED_M0_ROTATION_EVALUATED_NOT_FULL_FLOW', 'arrays_path': arrays_pin['path'],
                       'arrays_sha256': arrays_pin['sha256'],
                       'uv_tail': {'schema': 'UNT_UV_TAIL_ROUTE_B_STAGE_RECORD_C2V001', 'stage_kind': 'le_rotation',
                                   'state_digest': st.digest, 'roster_digest': st_rec['roster_digest'],
                                   'config_sha256': st_rec['config_sha256'],
                                   'config': {'eps_certificate': dict(cert_pin), 'lo_certificate': dict(LO_PIN)}}})
    wjson(rot / 'finish.json', fin)
    # 43 query rows: row 0 inside the innermost node, row 42 beyond the outer cut, the rest valid
    qids = ['SYN-Q%02d' % i for i in range(43)]
    radii = [0.5 * KPC] + [KPC * (1.0 + 8.0 * i / 40.0) for i in range(41)] + [9.6 * KPC]
    rows, sup = [], []
    for i, (q, r) in enumerate(zip(qids, radii)):
        if i == 0:
            rows.append({'id': q, 'speed_km_s': None, 'valid': False, 'reason': 'QUERY_INSIDE_INNERMOST_NODE',
                         'radius_m': r, 'innermost_radial_node_m': float(R[0])})
        elif i == 42:
            rows.append({'id': q, 'speed_km_s': None, 'valid': False, 'reason': 'QUERY_BEYOND_OUTER_GAS_CUT',
                         'radius_m': r, 'first_unconfined_R_m': 9.5 * KPC})
        else:
            rows.append({'id': q, 'speed_km_s': 100.0 + i, 'valid': True})
            j = bisect.bisect_left(list(R), r)
            cols = [j] if j < len(R) and R[j] == r else [j - 1, j]
            sup.append({'id': q, 'radius_m': r, 'column_indices': cols, 'radial_support_m': [float(R[c]) for c in cols]})
    rows = h('rows', rows)
    sup = h('support', sup)
    cmr = h('colmean', {'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION', 'rotation_array_pin': dict(arrays_pin),
                        'prediction': {'rows': rows, 'query_support': sup, 'physical_inclination_rad': incl[0],
                                       'released_inclination_rad': incl[1], 'units': 'km/s'}})
    cm_pin = wjson(obs / 'result.json', cmr)
    spec_sha = sha_bytes(('synthetic spec ' + tag).encode())
    res = h('result', {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'driver_sha256': W.DRIVER_SHA256,
                       'galaxy': 'NGC3198', 'call_spec_sha256': spec_sha, 'valid': True,
                       'normalized_spec': {'galaxy': 'NGC3198', 'numerics': {'uv_tail': {
                           'eps_certificate': dict(cert_pin), 'lo_certificate': dict(LO_PIN)}}},
                       'final_pass': 2,
                       'passes': [{'pass': 1, 'rotation': str(out / 'stages' / '04_le1_rotation' / 'rotation')},
                                  {'pass': 2, 'rotation': str(rot), 'rotation_arrays': dict(arrays_pin),
                                   'column_mean': {'path': cm_pin['path'], 'sha256': cm_pin['sha256'],
                                                   'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'},
                                   'rows': rows}],
                       'rows': rows})
    wjson(out / 'result.json', res)
    return {'cert_pin': cert_pin, 'cert_rec': cert_rec, 'call_dir': str(root / 'call'), 'tail': tail,
            'spec_sha': spec_sha, 'qids': qids, 'R': R, 'omega': omega, 'fields': fields, 'sup': sup,
            'state': st, 'state_arrays': st_arr, 'key': key}


def run_point(W, p, role='u_A', qids=None, log_index=None, **kw):
    return W.point_record(role=role, theta_key=p['key'], query_ids=qids or p['qids'], certificate=p['cert_pin'],
                          call_dir=p['call_dir'], tail_state_pins=p['tail'], call_spec_sha256=p['spec_sha'],
                          log_index=log_index, **kw)


def oracle(p):
    """Independent arithmetic of the V001 sec 1.4 / SRB-ROT bound (no library call)."""
    shells = p['cert_rec']['shells']
    if not p['state_arrays']:
        return [0.0] * len(p['sup'])
    edges, B = p['state_arrays']['shell_edges_inverse_kpc'], p['state_arrays']['shell_integrals']
    B1 = 0.0
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        vals = [s['eps'] for s in shells if s['lo_inverse_kpc'] < hi and s['hi_inverse_kpc'] > lo]
        B1 += (max(vals) if vals else 0.0) * B[i, 1]
    nmin = float(np.min(1 + p['fields'][..., 0].real))
    R = p['R']
    vc = [R[i] * math.sqrt(float(np.min(p['omega'][i]))) for i in range(len(R))]
    return [max(R[j] * C * C * B1 / (2 * nmin * vc[j]) / 1e3 for j in s['column_indices']) for s in p['sup']]


def key(i):
    return hashlib.sha256(('synthetic theta %d' % i).encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ tests
def tests(W, work, quick=False):
    lib, rowmod = W.modules()
    p = build_point(W, work, 'base', key(1))
    rec = run_point(W, p)
    eps = rec['eps_km_s']
    ora = oracle(p)
    valid = [e for e in eps if e is not None]
    rel = max(abs(a - b) / b for a, b in zip(valid, ora))
    record('T01a 43 entries; 41 finite nonnegative; rows 0 and 42 None with the call reason',
           len(eps) == 43 and len(valid) == 41 and all(math.isfinite(e) and e >= 0 for e in valid)
           and eps[0] is None and eps[42] is None
           and rec['eps_row_reason'][0] == 'ROW_INVALID_IN_CALL: QUERY_INSIDE_INNERMOST_NODE'
           and rec['eps_row_reason'][42] == 'ROW_INVALID_IN_CALL: QUERY_BEYOND_OUTER_GAS_CUT'
           and all(w is None for w in rec['eps_row_reason'][1:42]), '%d valid' % len(valid))
    record('T01b equals the independent oracle (rel <= 1e-12)', rel <= 1e-12, 'max rel %.3e' % rel)
    cert, _c = W.check_certificate(p['cert_pin'], p['key'])
    rows = rowmod.rotation_rows(p['R'], p['omega'], p['fields'], [s['radius_m'] for s in p['sup']])
    direct = lib.srb_rot(p['state'], cert, dict(rows, tau_km_s=[1.0] * 41))['bound_km_s']
    record('T01c bitwise equal to the pinned srb_rot on the same inputs', direct == valid)
    record('T01d record pins: field_bound / srb_rot library 2026f2b6, rows 67fddd24, driver 577f8c94, state stage le2',
           rec['field_bound']['pin']['sha256'].startswith('2026f2b6') and rec['srb_rot']['pin']['sha256'].startswith('2026f2b6')
           and rec['rows_input']['pin']['sha256'].startswith('67fddd24') and rec['call']['driver_sha256'].startswith('577f8c94')
           and rec['state']['stage'] == 'le2_rotation' and rec['state']['final_pass'] == 2
           and rec['certificate'] == p['cert_pin'] and rec['certificate_checks']['point_key'] == p['key'])
    record('T01e N_min, v_c and columns are the call own rotation_rows values',
           rec['rows_input']['N_min'] == float(np.min(1 + p['fields'][..., 0].real))
           and rec['rows_input']['row_columns'] == [s['column_indices'] for s in p['sup']]
           and rec['rows_input']['N_min'] != 1.0)
    rec2 = run_point(W, p)
    record('T02 deterministic (canonical bytes equal)', W.canonical(rec) == W.canonical(rec2))
    taus = [lib.srb_rot(p['state'], cert, dict(rows, tau_km_s=t))['bound_km_s']
            for t in ([1.0] * 41, list(np.linspace(0.3, 9.0, 41)), [1e9] * 41)]
    record('T03 bound_km_s does not depend on tau (pinned srb_rot L866-869)', taus[0] == taus[1] == taus[2])
    pd = build_point(W, work, 'decoy', key(1), cert=make_cert(Path(work) / 'decoy', 'decoy', key(1), eps_max=1e9))
    record('T04 eps_max is never read (decoy eps_max 1e9 gives the same list)', run_point(W, pd)['eps_km_s'] == eps)
    ps = build_point(W, work, 'sens', key(1), cert=make_cert(
        Path(work) / 'sens', 'sens', key(1),
        over=lambda r: dict(r, shells=[dict(s, eps=s['eps'] * 2) if s['lo_inverse_kpc'] == 40.0 else s for s in r['shells']])))
    e2 = run_point(W, ps)['eps_km_s']
    record('T05 one doubled certificate shell (40,41] raises every valid entry',
           all(b > a for a, b in zip(valid, [x for x in e2 if x is not None])))
    pe = build_point(W, work, 'empty', key(1), empty=True)
    re_ = run_point(W, pe)
    record('T06 empty tail state: valid rows 0.0, state.empty true',
           re_['state']['empty'] is True and [x for x in re_['eps_km_s'] if x is not None] == [0.0] * 41)
    rn = W.point_record(role='member', theta_key=key(9), query_ids=p['qids'], certificate=None, log_index=17)
    record('T07 no certificate: 43 None with NO_POINT_CERTIFICATE, nothing read',
           rn['eps_km_s'] == [None] * 43 and rn['eps_row_reason'] == ['NO_POINT_CERTIFICATE'] * 43
           and rn['certificate'] is None and rn['log_index'] == 17)
    # T08 certificate refusals (synthetic)
    cw = Path(work) / 'certs'
    bad = {
        'schema BIND_CHECK': (lambda r: dict(r, schema='UNT_CLAUDE4_S0_POINT_EPS_C4V002_BIND_CHECK'), 'CERT_SCHEMA'),
        'schema SMOKE_ANCHOR': (lambda r: dict(r, schema='UNT_CLAUDE4_S0_POINT_EPS_C4V002_SMOKE_ANCHOR'), 'CERT_SCHEMA'),
        'mode smoke': (lambda r: dict(r, mode='smoke'), 'CERT_NOT_A_POINT_RECORD'),
        'role anchor': (lambda r: dict(r, point=dict(r['point'], role='anchor_F10 (SMOKE)')), 'CERT_NOT_A_POINT_RECORD'),
        'other point key': (lambda r: dict(r, point=dict(r['point'], key=key(2))), 'CERT_OTHER_POINT'),
        'key_check false': (lambda r: dict(r, key_check=dict(r['key_check'], equals_point_key=False)), 'CERT_KEY_CHECK'),
        'producer not reviewed': (lambda r: dict(r, producer={'path': '/x', 'sha256': '0' * 64}), 'CERT_PRODUCER_NOT_REVIEWED'),
        'verdict': (lambda r: dict(r, verdict='NOT_CERTIFIED'), 'CERT_NOT_CERTIFIED'),
        'certificate false': (lambda r: dict(r, certificate=False), 'CERT_NOT_CERTIFIED'),
        'rule_verdict': (lambda r: dict(r, summary={'rule_verdict': 'NOT_CERTIFIED'}), 'CERT_NOT_CERTIFIED'),
        'coverage [2,9]': (lambda r: dict(r, coverage_inverse_kpc={'NGC': [2.0, 9.0]}), 'CERT_COVERAGE'),
        'shell gap': (lambda r: dict(r, shells=r['shells'][:10] + r['shells'][11:]), 'CERT_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS'),
        'shells from 3': (lambda r: dict(r, shells=r['shells'][1:]), 'CERT_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS'),
        'shells end at 90': (lambda r: dict(r, shells=r['shells'][:-1]), 'CERT_COVERAGE'),
        'eps below envelope': (lambda r: dict(r, shells=[dict(s, envelope={'eps_envelope': s['eps'] * 1.01}) if i == 5 else s
                                                         for i, s in enumerate(r['shells'])]), 'CERT_EPS_NOT_THE_LARGER_VALUE'),
        'negative eps': (lambda r: dict(r, shells=[dict(s, eps=-1e-4) if i == 3 else s for i, s in enumerate(r['shells'])]),
                         'CERT_EPS_NOT_THE_LARGER_VALUE'),
        'nan eps': (lambda r: dict(r, shells=[dict(s, eps=float('nan')) if i == 3 else s for i, s in enumerate(r['shells'])]),
                    'CERT_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS'),
    }
    for i, (name, (fn, code)) in enumerate(bad.items()):
        pin, _r = make_cert(cw, 'bad%02d' % i, key(1), over=fn)
        expect_refused(W, 'T08 certificate refused: ' + name, code, lambda pin=pin: W.check_certificate(pin, key(1)))
    good, _r = make_cert(cw, 'good', key(1))
    expect_refused(W, 'T08 certificate refused: file sha mismatch', 'PIN_SHA_MISMATCH',
                   lambda: W.check_certificate(dict(good, sha256='0' * 64), key(1)))
    # T09 the real S0 certificates (read-only)
    keys = {}
    for fn, sh in REAL_EPS.items():
        pin = {'path': S0_OUT + fn, 'sha256': sh}
        k = json.loads(Path(pin['path']).read_bytes())['point']['key']
        keys[fn] = (pin, k)
        cf, ck = W.check_certificate(pin, k)
        raw = json.loads(Path(pin['path']).read_bytes())
        record('T09a real certificate passes with its own key: ' + fn,
               len(cf['shells']) == 89 and cf['shells'][0]['lo_inverse_kpc'] == 2.0 and cf['shells'][-1]['hi_inverse_kpc'] == 91.0
               and [s['eps'] for s in cf['shells']] == [s['eps'] for s in raw['shells']] and ck['point_key'] == k, k[:16])
    for fn, (pin, k) in keys.items():
        for fn2, (_p2, k2) in keys.items():
            if fn2 != fn:
                expect_refused(W, 'T09b real certificate %s refused for key %s' % (fn[13:29], k2[:16]), 'CERT_OTHER_POINT',
                               lambda pin=pin, k2=k2: W.check_certificate(pin, k2))
    for fn in REAL_REFUSED:
        b = Path(S0_OUT + fn).read_bytes()
        expect_refused(W, 'T09c real non-point record refused: ' + fn, 'CERT_SCHEMA',
                       lambda b=b, fn=fn: W.check_certificate({'path': S0_OUT + fn, 'sha256': sha_bytes(b)}, key(1)))
    # T10 state binding refusals
    sw = Path(work) / 'state'
    cases = [
        ('finish state_digest altered', {'finish': lambda f: dict(f, uv_tail=dict(f['uv_tail'], state_digest='1' * 64))},
         'TAIL_STATE_NOT_THE_CALL_STATE'),
        ('digest-consistent state of stage_kind le_columns', {'state_record': lambda r: dict(r, stage_kind='le_columns')},
         'TAIL_STATE_STAGE_SOURCE_OR_CONFIG_MISMATCH'),
        ('state record eps pin of another certificate',
         {'state_record': lambda r: dict(r, eps_certificate={'path': '/synthetic/other.json', 'sha256': 'f' * 64})},
         'TAIL_STATE_DID_NOT_RUN_WITH_THE_POINT_CERTIFICATE'),
        ('finish config eps pin of another certificate',
         {'finish': lambda f: dict(f, uv_tail=dict(f['uv_tail'], config={'eps_certificate': {'path': '/synthetic/o.json',
                                                                                                'sha256': 'f' * 64}}))},
         'STAGE_EPS_PIN_NOT_THE_POINT_CERTIFICATE'),
        ('spec eps pin of another certificate',
         {'result': lambda r: dict(r, normalized_spec={'numerics': {'uv_tail': {'eps_certificate': {
             'path': '/synthetic/o.json', 'sha256': 'f' * 64}}}})}, 'CALL_EPS_PIN_NOT_THE_POINT_CERTIFICATE'),
        ('roster digest mismatch', {'finish': lambda f: dict(f, uv_tail=dict(f['uv_tail'], roster_digest='9' * 64))},
         'TAIL_STATE_STAGE_SOURCE_OR_CONFIG_MISMATCH'),
        ('config sha mismatch', {'finish': lambda f: dict(f, uv_tail=dict(f['uv_tail'], config_sha256='9' * 64))},
         'TAIL_STATE_STAGE_SOURCE_OR_CONFIG_MISMATCH'),
    ]
    for i, (name, hooks, code) in enumerate(cases):
        q = build_point(W, sw, 's%02d' % i, key(1), hooks=hooks)
        expect_refused(W, 'T10 refused: ' + name, code, lambda q=q: run_point(W, q))
    expect_refused(W, 'T10 refused: tail record pin sha mismatch', 'PIN_SHA_MISMATCH',
                   lambda: W.point_record(role='u_A', theta_key=p['key'], query_ids=p['qids'], certificate=p['cert_pin'],
                                          call_dir=p['call_dir'], call_spec_sha256=p['spec_sha'],
                                          tail_state_pins={'record': dict(p['tail']['record'], sha256='0' * 64),
                                                           'arrays': p['tail']['arrays']}))
    other = build_point(W, sw, 'other', key(3))
    expect_refused(W, 'T10 refused: another point state (its digest) fed to this call', 'TAIL_STATE_NOT_THE_CALL_STATE',
                   lambda: W.point_record(role='u_A', theta_key=p['key'], query_ids=p['qids'], certificate=p['cert_pin'],
                                          call_dir=p['call_dir'], call_spec_sha256=p['spec_sha'],
                                          tail_state_pins=other['tail']))
    # T11 call binding refusals
    cwk = Path(work) / 'call'
    outside = Path(work) / 'outside' / '07_le2_rotation' / 'rotation'
    cases = [
        ('driver sha', {'result': lambda r: dict(r, driver_sha256='0' * 64)}, 'DRIVER_NOT_CX3R008'),
        ('galaxy', {'result': lambda r: dict(r, galaxy='DDO154')}, 'CALL_GALAXY'),
        ('final_pass 3 with 2 passes', {'result': lambda r: dict(r, final_pass=3)}, 'FINAL_PASS_UNAVAILABLE'),
        ('rotation stage le1 for final pass 2', {'result': lambda r: dict(r, passes=[r['passes'][0], dict(
            r['passes'][1], rotation=r['passes'][1]['rotation'].replace('07_le2_rotation', '07_le1_rotation'))])},
         'FINAL_ROTATION_STAGE'),
        ('finish arrays pin differs from passes[-1].rotation_arrays', {'finish': lambda f: dict(f, arrays_sha256='0' * 64)},
         'FINAL_PASS_ROTATION_ARRAYS_MISMATCH'),
        ('column mean status', {'result': lambda r: dict(r, passes=[r['passes'][0], dict(
            r['passes'][1], column_mean=dict(r['passes'][1]['column_mean'], status='FAILED_NO_PREPARATION_OUTPUT'))])},
         'COLUMN_MEAN_UNAVAILABLE'),
        ('column mean sha', {'result': lambda r: dict(r, passes=[r['passes'][0], dict(
            r['passes'][1], column_mean=dict(r['passes'][1]['column_mean'], sha256='0' * 64))])}, 'OWN_CALL_SHA_MISMATCH'),
        ('column mean of another rotation', {'colmean': lambda c: dict(c, rotation_array_pin={'path': '/x', 'sha256': '0' * 64})},
         'COLUMN_MEAN_NOT_OF_THIS_ROTATION'),
        ('result rows differ from final rows', {'result': lambda r: dict(r, rows=r['rows'][:-1] + [dict(r['rows'][-1], radius_m=1.0)])},
         'FINAL_ROWS_NOT_THE_COLUMN_MEAN_ROWS'),
        ('valid row with null speed', {'rows': lambda rs: [dict(r, speed_km_s=None) if i == 5 else r for i, r in enumerate(rs)]},
         'ROW_STATE_INCONSISTENT'),
        ('query support ids differ', {'support': lambda s: s[:-1]}, 'QUERY_SUPPORT_NOT_THE_VALID_ROWS'),
    ]
    for i, (name, hooks, code) in enumerate(cases):
        q = build_point(W, cwk, 'c%02d' % i, key(1), hooks=hooks)
        expect_refused(W, 'T11 refused: ' + name, code, lambda q=q: run_point(W, q))
    q = build_point(W, cwk, 'spec', key(1))
    expect_refused(W, 'T11 refused: call spec sha is not the point custody spec', 'CALL_SPEC_SHA',
                   lambda: W.point_record(role='u_A', theta_key=q['key'], query_ids=q['qids'], certificate=q['cert_pin'],
                                          call_dir=q['call_dir'], tail_state_pins=q['tail'], call_spec_sha256='0' * 64))
    q = build_point(W, cwk, 'arr', key(1))
    npz = Path(q['call_dir']) / 'out' / 'stages' / '07_le2_rotation' / 'rotation' / 'rotation_base_arrays.npz'
    b = npz.read_bytes()
    npz.unlink()
    with open(npz, 'xb') as f:
        f.write(b[:-8] + bytes(8))
    expect_refused(W, 'T11 refused: rotation arrays bytes altered after the run', 'OWN_CALL_SHA_MISMATCH', lambda: run_point(W, q))
    q = build_point(W, cwk, 'out', key(1))
    src = Path(q['call_dir']) / 'out' / 'stages' / '07_le2_rotation' / 'rotation'
    outside.mkdir(parents=True)
    for fn in ('finish.json', 'rotation_base_arrays.npz'):
        (outside / fn).write_bytes((src / fn).read_bytes())
    rp = Path(q['call_dir']) / 'out' / 'result.json'
    r = json.loads(rp.read_bytes())
    r['passes'][1]['rotation'] = str(outside)
    rp.unlink()
    wjson(rp, r)
    expect_refused(W, 'T11 refused: rotation finish outside the call own out dir', 'OUTSIDE_OWN_CALL', lambda: run_point(W, q))
    # T12 query ids
    expect_refused(W, 'T12 refused: 42 query ids', 'QUERY_IDS', lambda: run_point(W, p, qids=p['qids'][:42]))
    expect_refused(W, 'T12 refused: duplicate query id', 'QUERY_IDS', lambda: run_point(W, p, qids=p['qids'][:42] + [p['qids'][0]]))
    sw_ = list(p['qids'])
    sw_[3], sw_[4] = sw_[4], sw_[3]
    expect_refused(W, 'T12 refused: values query order differs from the call rows (no reorder)', 'QUERY_ORDER_MISMATCH',
                   lambda: run_point(W, p, qids=sw_))
    # T13 coverage
    q = build_point(W, work, 'beyond', key(1), beyond=True)
    expect_refused(W, 'T13 refused: state k-range beyond 91 /kpc', 'CERT_COVERAGE_DOES_NOT_COVER_STATE', lambda: run_point(W, q))
    try:
        lib.field_bound(q['state'], W.check_certificate(q['cert_pin'], q['key'])[0])
        record('T13b the pinned library also refuses that state (UV_TAIL_EPS_COVERAGE)', False, 'no refusal')
    except lib.Refusal as exc:
        record('T13b the pinned library also refuses that state (UV_TAIL_EPS_COVERAGE)', exc.code == 'UV_TAIL_EPS_COVERAGE', exc.code)
    q = build_point(W, work, 'kmin1', key(1), kmin=1.0)
    expect_refused(W, 'T13 refused: state k-range starting below 2 /kpc', 'CERT_COVERAGE_DOES_NOT_COVER_STATE', lambda: run_point(W, q))
    record('T13c coverage printed for the base point', rec['coverage'] == {'k_range_nonzero_inverse_kpc': [32.0, 91.0],
                                                                           'covered': True, 'state_empty': False},
           repr(rec['coverage']))
    # T14-T16 rows
    q = build_point(W, work, 'cols', key(1), hooks={'support': lambda s: [dict(x, column_indices=[0, 1]) if i == 7 else x
                                                                          for i, x in enumerate(s)]})
    expect_refused(W, 'T14 refused: row columns differ from the column-mean support', 'ROW_COLUMNS_DIFFER_FROM_COLUMN_MEAN_SUPPORT',
                   lambda: run_point(W, q))
    q = build_point(W, work, 'supp', key(1), hooks={'support': lambda s: [dict(x, radius_m=50 * KPC) if i == 7 else x
                                                                          for i, x in enumerate(s)]})
    expect_refused(W, 'T15 refused: a valid row outside the radial support', 'ROTATION_ROWS_UNAVAILABLE', lambda: run_point(W, q))
    q = build_point(W, work, 'negom', key(1), omega_sign=-1.0)
    expect_refused(W, 'T16 refused: nonpositive rotation square', 'ROTATION_ROWS_UNAVAILABLE', lambda: run_point(W, q))
    # T17-T19 attach
    vdoc = {'schema': 'PHASE1_NGC_VALUES_C2V001', 'query_ids': p['qids'], 'points': []}
    expect_refused(W, 'T17 attach refused while ROOT_RULING is None (W-1 stop)', 'ROOT_RULING_PENDING',
                   lambda: W.attach_eps(vdoc, [rec], 'phase1_values'))
    P1 = load(PHASE1_V003[0], 'vw2_phase1_c2v003')
    roles = ['u_A', 'F0', 'F1', 'F2']
    pts = [build_point(W, work, 'v_%s' % r_, key(10 + i), cert=make_cert(Path(work) / ('v_%s' % r_), 'v_%s' % r_,
                                                                         key(10 + i), scale=1.0 + 0.25 * i))
           for i, r_ in enumerate(roles)]
    recs = [run_point(W, x, role=r_) for x, r_ in zip(pts, roles)]
    vdoc = {'schema': 'PHASE1_NGC_VALUES_C2V001', 'query_ids': p['qids'],
            'points': [{'role': r_, 'theta_key': x['key'], 'valid': [i not in (0, 42) for i in range(43)],
                        'speeds_km_s': [None if i in (0, 42) else 100.0 + i for i in range(43)]} for x, r_ in zip(pts, roles)]}
    W.ROOT_RULING = {'path': '/synthetic/ROOT_RULING_TEST_ONLY.md', 'sha256': '0' * 64}
    try:
        new = W.attach_eps(vdoc, recs, 'phase1_values')
        fd = {'u_A': {'log_index': 0}, 'members': [{'key': pts[0]['key'], 'log_index': 0}],
              'F': [{'role': r_, 'key': x['key']} for x, r_ in zip(pts[1:], roles[1:])]}
        P1.check_values(new, fd)
        ptsd = {x['role']: x for x in new['points']}
        ok_eps = all(ptsd[r_]['eps_km_s'] == rc['eps_km_s'] for r_, rc in zip(roles, recs))
        band_ok = True
        for q_ in range(43):     # band_rows L870 rule (v003; v002 L791): all four finite nonnegative -> eps_q = max
            es = [(ptsd[r_].get('eps_km_s') or [None] * 43)[q_] for r_ in roles]
            fin = all(isinstance(e, (int, float)) and not isinstance(e, bool) and math.isfinite(e) and e >= 0 for e in es)
            band_ok &= (fin == (q_ not in (0, 42)))
        record('T18a Phase-1 values: attached, phase1_c2v003 check_values accepts, band eps rule finite on valid rows only',
               ok_eps and band_ok and all('eps_km_s_custody' in x for x in new['points']) and 'eps_km_s' not in vdoc['points'][0])
        mpts = [build_point(W, work, 'm%d' % i, key(20 + i)) for i in range(2)]
        mrecs = [run_point(W, x, role='member', log_index=100 + i) for i, x in enumerate(mpts)]
        mrecs.append(W.point_record(role='member', theta_key=key(29), query_ids=p['qids'], certificate=None, log_index=109))
        mdoc = {'schema': 'PHASE1_NGC_VALUES_C2V001', 'query_ids': p['qids'],
                'points': [{'role': 'member', 'log_index': r_['log_index'], 'theta_key': r_['theta_key'],
                            'valid': [True] * 43, 'speeds_km_s': [1.0] * 43} for r_ in mrecs]}
        mnew = W.attach_eps(mdoc, mrecs, 'phase2_members')
        mv = {x['log_index']: x for x in mnew['points']}
        P1.check_member_eps(mv, 43)
        reads = [[P1.member_eps(mv[li]['eps_km_s'], q_) for q_ in range(43)] for li in (100, 101, 109)]
        record('T18b Phase-2 members: phase1_c2v003 check_member_eps accepts; member_eps reads numbers on valid rows, '
               'MEMBER_EPS_NONE on invalid rows and on the uncertified member',
               all(reads[0][q_][1] is None for q_ in range(1, 42)) and reads[0][0] == (None, 'MEMBER_EPS_NONE')
               and reads[0][42] == (None, 'MEMBER_EPS_NONE') and all(x == (None, 'MEMBER_EPS_NONE') for x in reads[2])
               and reads[0][5][0] == mrecs[0]['eps_km_s'][5])
        record('T22 never another point values: four points, four distinct lists',
               len({json.dumps(r_['eps_km_s']) for r_ in recs}) == 4)
        # T19 attach refusals
        expect_refused(W, 'T19 attach refused: a point without a record', 'NO_RECORD_FOR_POINT',
                       lambda: W.attach_eps(vdoc, recs[:3], 'phase1_values'))
        expect_refused(W, 'T19 attach refused: duplicate theta key', 'RECORDS_DUPLICATE_THETA_KEY',
                       lambda: W.attach_eps(vdoc, recs + [recs[0]], 'phase1_values'))
        expect_refused(W, 'T19 attach refused: an unused record', 'RECORDS_UNUSED',
                       lambda: W.attach_eps(vdoc, recs + [mrecs[0]], 'phase1_values'))
        expect_refused(W, 'T19 attach refused: eps already present (no overwrite)', 'EPS_ALREADY_PRESENT',
                       lambda: W.attach_eps(new, recs, 'phase1_values'))
        expect_refused(W, 'T19 attach refused: record query ids differ', 'RECORD_QUERY_IDS',
                       lambda: W.attach_eps(vdoc, [dict(recs[0], query_ids=list(reversed(p['qids'])))] + recs[1:], 'phase1_values'))
        expect_refused(W, 'T19 attach refused: role mismatch', 'RECORD_ROLE_OR_LOG_INDEX',
                       lambda: W.attach_eps(vdoc, [dict(recs[0], role='F0')] + recs[1:], 'phase1_values'))
        expect_refused(W, 'T19 attach refused: member log_index mismatch', 'RECORD_ROLE_OR_LOG_INDEX',
                       lambda: W.attach_eps(mdoc, [dict(mrecs[0], log_index=5)] + mrecs[1:], 'phase2_members'))
        expect_refused(W, 'T19 attach refused: record bound to another theta (tampered)', 'RECORD_NOT_BOUND_TO_ITS_THETA',
                       lambda: W.attach_eps(vdoc, [dict(recs[0], certificate_checks=dict(recs[0]['certificate_checks'],
                                                                                           point_key=key(99)))] + recs[1:],
                                            'phase1_values'))
        expect_refused(W, 'T19 attach refused: values without a certificate (tampered)', 'RECORD_VALUES_WITHOUT_CERTIFICATE',
                       lambda: W.attach_eps(mdoc, mrecs[:2] + [dict(mrecs[2], eps_km_s=[1.0] * 43,
                                                                    eps_row_reason=[None] * 43)], 'phase2_members'))
        expect_refused(W, 'T19 attach refused: negative entry (tampered)', 'RECORD_EPS_SHAPE',
                       lambda: W.attach_eps(vdoc, [dict(recs[0], eps_km_s=[-1.0] + recs[0]['eps_km_s'][1:],
                                                        eps_row_reason=[None] + recs[0]['eps_row_reason'][1:])] + recs[1:],
                                            'phase1_values'))
    finally:
        W.ROOT_RULING = None
    # T20-T21 CLI and writes
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'HOME')}
    cp = subprocess.run([sys.executable, '-I', '-B', W.__file__, 'point', '--args', '/nonexistent', '--args-sha256', '0' * 64,
                         '--out-dir', str(work)], capture_output=True, text=True, env=env)
    record('T20 CLI refuses while ROOT_RULING is None (exit 3)', cp.returncode == 3 and 'ROOT_RULING_PENDING' in cp.stdout,
           cp.stdout.strip()[:200])
    od = Path(work) / 'writes'
    od.mkdir()
    pin1 = W.write_new(rec, od, 'R.json')
    try:
        W.write_new(rec, od, 'R.json')
        record('T21 exclusive create (a second write of the same name fails)', False)
    except FileExistsError:
        record('T21 exclusive create (a second write of the same name fails)',
               sha_bytes(Path(pin1['path']).read_bytes()) == pin1['sha256'])
    # T23 inclination printed, never applied
    pi_ = build_point(W, work, 'incl', key(1), incl=(1.2, 1.1))
    ri = run_point(W, pi_)
    record('T23 sin(i_phys)/sin(i_released) printed from the call own packet, not applied (list unchanged)',
           ri['inclination']['applied'] is False and ri['inclination']['sin_ratio'] == math.sin(1.2) / math.sin(1.1)
           and ri['eps_km_s'] == eps and rec['inclination']['sin_ratio'] == 1.0)
    # T24-T26 byte and line evidence for the report
    def lines(path, a, b):
        return Path(path).read_text().splitlines()[a - 1:b]
    record('T24 writer pins equal the bytes on disk (library 2026f2b6, rows 67fddd24, driver 577f8c94)',
           sha_bytes(Path(W.LIBRARY[0]).read_bytes()) == W.LIBRARY[1]
           and sha_bytes(Path(W.ROW_PRODUCER[0]).read_bytes()) == W.ROW_PRODUCER[1]
           and sha_bytes(Path(DRIVER[0]).read_bytes()) == DRIVER[1] == W.DRIVER_SHA256)
    v3 = Path(LIB_V003[0]).read_bytes()
    record('T25a B2: owned_uv_tail_lapse_v003 exists at driver_r6/module, e733eb1e, 1211 lines',
           sha_bytes(v3) == LIB_V003[1] and len(v3.decode().splitlines()) == 1211)
    record('T25b B2: v002 L664-688 (hash-check + state record) == v003 L962-986, byte-identical',
           lines(W.LIBRARY[0], 664, 688) == lines(LIB_V003[0], 962, 986))
    record('T25c B2: v002 L830-885 (_eps_per_shell, field_bound, srb_rot, monitor_MT) == v003 L1144-1199',
           lines(W.LIBRARY[0], 830, 885) == lines(LIB_V003[0], 1144, 1199))
    dl = Path(DRIVER[0]).read_text().splitlines()
    ad = lines(SRB_ADAPTER[0], 1, 600)
    rs = lines(ROT_STAGE[0], 1, 400)
    rp_ = lines(W.ROW_PRODUCER[0], 1, 300)
    v6 = Path(V006).read_text().splitlines()
    ev = {
        'adapter sha 08e9ac0a': sha_bytes(Path(SRB_ADAPTER[0]).read_bytes()) == SRB_ADAPTER[1],
        'adapter L434 eps pin check': "record.get('eps_certificate') != eps_pin" in ad[433],
        'adapter L439 field_bound': 'U.field_bound(st, eps_cert)' in ad[438],
        'adapter L440 srb_rot': 'U.srb_rot(st, eps_cert, rows)' in ad[439],
        'adapter L53-54 library v002 2026f2b6': 'owned_uv_tail_lapse_v002.py' in ad[52] and '2026f2b6' in ad[53],
        'rows L171 def rotation_rows': rp_[170].startswith('def rotation_rows(R, omega, fields, radii):'),
        'rows L183 N_min, L186 v_c, L193 return': 'n_min = float(np.min(1 + fields[..., 0].real))' in rp_[182]
        and 'v = R * np.sqrt(np.min(omega, axis=1))' in rp_[185] and "'N_min': n_min}" in rp_[192],
        'rotation stage e22e79e8': sha_bytes(Path(ROT_STAGE[0]).read_bytes()) == ROT_STAGE[1],
        'rotation stage L294 full_fields_complex, L295 rotation_, L302 savez': 'full_fields_complex=fields' in rs[293]
        and "arrays['rotation_'+name]" in rs[294] and "np.savez(out/'rotation_base_arrays.npz'" in rs[301],
        'driver L310-311 library v002': dl[309].startswith('UVT_LIB = {') and 'owned_uv_tail_lapse_v002.py' in dl[310]
        and '2026f2b6' in dl[310],
        'driver L354 rotation_v005 -> le_rotation': "'rotation_v005': 'le_rotation'" in dl[353],
        'driver L907-912 nodes branch; the NGC refusal is L911-912 (review cited L909-910)':
        dl[906].startswith("    if sr != 'continuum_v001'") and 'if ngc:' in dl[910] and 'DDO154_ONLY' in dl[911],
        'driver L5940 rotation_arrays': "rotation_arrays={'path': rfj['arrays_path']" in dl[5939],
        'driver L6062 final_pass': "result['final_pass'] = final['pass']" in dl[6061],
        'V006 L525 SRB-ROT target': 'own_source_state at `le{final_pass}_rotation`' in v6[524],
        'V006 A146 SRB adapter 08e9ac0a adopted': any('SRB adapter `08e9ac0a`' in x for x in v6),
        'V006 A148 text does not name srb_rot': not any('srb_rot' in x for x in v6[933:956]),
    }
    for k_, v_ in ev.items():
        record('T26 evidence: ' + k_, v_)
    import ast

    def fdump(path, name):
        for n in ast.parse(Path(path).read_text()).body:
            if isinstance(n, ast.FunctionDef) and n.name == name:
                return ast.dump(n)
    p2 = ART + '/phase1_c2/phase1_c2v002.py'
    record('T27 consumer: check_values, members_values and band_rows are AST-identical in phase1_c2v002 (d64351ec) '
           'and phase1_c2v003, so T18 covers both',
           sha_bytes(Path(p2).read_bytes()).startswith('d64351ec') and sha_bytes(Path(PHASE1_V003[0]).read_bytes()) == PHASE1_V003[1]
           and all(fdump(p2, f) is not None and fdump(p2, f) == fdump(PHASE1_V003[0], f)
                   for f in ('check_values', 'members_values', 'band_rows')))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--module', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--results', default=None)
    a = ap.parse_args()
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=False)
    W = load(os.path.abspath(a.module), 'vw2_under_test')
    try:
        tests(W, work)
    except Exception as exc:     # noqa: BLE001
        import traceback
        record('SUITE CRASH', False, '%s: %s | %s' % (type(exc).__name__, exc, traceback.format_exc()[-600:]))
    n_ok = sum(r['ok'] for r in RESULTS)
    summary = {'module': os.path.abspath(a.module), 'module_sha256': sha_bytes(Path(a.module).read_bytes()),
               'test_file_sha256': sha_bytes(Path(__file__).read_bytes()), 'python': sys.version.split()[0],
               'numpy': np.__version__, 'flags_isolated': sys.flags.isolated, 'flags_dont_write_bytecode':
               sys.flags.dont_write_bytecode, 'n': len(RESULTS), 'passed': n_ok, 'results': RESULTS}
    rp = Path(a.results) if a.results else work / 'RESULTS_TEST_VALUES_WRITER_C2V002.json'
    with open(rp, 'xb') as f:
        f.write(json.dumps(summary, indent=1).encode())
    for r in RESULTS:
        if not r['ok']:
            print('FAIL', r['test'], '|', r['detail'])
    print('%d/%d passed; results %s' % (n_ok, len(RESULTS), rp))
    return 0 if n_ok == len(RESULTS) else 1


if __name__ == '__main__':
    sys.exit(main())
