"""Synthetic tests for values_writer_c2v003a (python3 -I -B; numpy). No solver runs and no real NGC field is computed:
every TailState, call tree, rotation array, column-mean record, acceptance record and query manifest used for values
here is synthetic. Real files read, read-only: the S0 certificate files in ngc_point_producer_c4/s0/build_c4v001/out
(certificate checks only); the V006 addendum (the A152 pin and line evidence; A136 G5 and A153 line evidence for B1);
the NGC target-free query manifest (sha, ids and the radii parse only -- A152 C-1); the pinned source files whose cited
lines the report relies on; the phase1 consumer modules v003 / v003a and the orchestrator they pin (theta_key only);
values_writer_c2v003 (dd9456bc), loaded by sha for the B1 differential tests (T45) only.
v003a changes against the v003 suite (70001d1f): T32b inverted and T32c / T37b member_valid now false (B1); T45 new
(B1: evidence, the P3 reproduction against v003, refusal of a G5-shaped record, Phase-1 unaffected, and the W-3
truth table with a test-only producer pin); the result file and the two module-copy names say v003a.

Usage: python3 -I -B test_values_writer_c2v003a.py --module <writer.py> --work <new dir>
"""
import argparse
import ast
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
PHASE1_V003A = (ART + '/phase1_c2/phase1_c2v003a.py', '385b287c68c3e4bbbcc2fa954cbba9bb7565846b1462dea32de9c79f36552d7d')
SRB_ADAPTER = (ART + '/s4rc1_c3/proof_side_c3v003/srb_rot_adapter_c3v003.py',
               '08e9ac0a12cf1829f79f6df8a82c9ec6a7d174fc4bb25be76d3c049525dfae6a')
LIB_V003 = (ART + '/tail_scheme_impl_c2/driver_r6/module/owned_uv_tail_lapse_v003.py',
            'e733eb1ebfe2137a6f58d0e35caa345525756e3896ca729c1ba15a39204c7155')
ROT_STAGE = (ART + '/ngc_route_tail_readiness_cx3/v011/cx3v005/sources/'
             'ngc_free_surface_rotation_root_v005_gal_c2v005_uvt_cx3v006_r5cx3v001_cx3v005.py',
             'e22e79e80a63825458ca659dd32c81bef473e170ba81486ef9db86929007249f')
DRIVER = (ART + '/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
          '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377')
HANDOFF = (ART + '/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',
           '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8')
V006 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
        'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md')
A152_SHA = '5aee4cc0f3ae64e5ea630d5a6459fdccc4cf2e3d55061d57e9214b1f002b074f'
WRITER_V003 = (ART + '/values_writer_c2/values_writer_c2v003.py',
               'dd9456bc50d04a31f2cfff4b8b58717656a85470e11efaaeaaa49768ab8ab47b')     # B1 differential only
G5_ROUTE = 'NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE'                               # A136 G5
KPC = 3.085677581491367e19
C = 299792458.0
PRODUCER_SHA = '8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235'
LO_PIN = {'path': '/synthetic/LO_TEST_ONLY.json', 'sha256': 'e' * 64}
RESULTS = []
_N = [0]


def uniq(prefix):
    _N[0] += 1
    return '%s_%03d' % (prefix, _N[0])


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


def replace_json(path, obj):
    path = Path(path)
    path.unlink()
    return wjson(path, obj)


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


def guarded(name, fn):
    try:
        fn()
    except Exception as exc:     # noqa: BLE001
        record(name, False, 'raised %s: %s' % (type(exc).__name__, exc))


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


QIDS = ['SYN-Q%02d' % i for i in range(43)]
RADII = [0.5 * KPC] + [KPC * (1.0 + 8.0 * i / 40.0) for i in range(41)] + [9.6 * KPC]


def call_finish(res, out, over=None):
    raw = (Path(out) / 'result.json').read_bytes()
    fin = {'status': res.get('status'), 'valid': res.get('valid'), 'result_path': str(Path(out) / 'result.json'),
           'result_sha256': sha_bytes(raw), 'elapsed_seconds': 1.0, 'reasons': res.get('reasons', []), 'retries': 0,
           'partial_outputs_preserved': True}
    return over(fin) if over else fin


def build_point(W, work, tag, key, *, cert=None, hooks=None, kmin=32.0, beyond=False, empty=False, incl=(1.2, 1.2),
                omega_sign=1.0, lapse_scale=1.0):
    """A synthetic point: certificate, call tree <work>/<tag>/call/out (result.json + finish.json, driver form), and
    its le2_rotation TailState files."""
    lib, _rows = W.modules()
    hooks = hooks or {}
    h = lambda k, x: hooks[k](x) if k in hooks else x      # noqa: E731
    root = Path(work) / tag
    cert_pin, cert_rec = cert if cert is not None else make_cert(root, tag, key)
    out = root / 'call' / 'out'
    rot = out / 'stages' / '07_le2_rotation' / 'rotation'
    obs = out / 'stages' / '08_le2_column_mean' / 'observation'
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
    positive = bool(np.all(np.asarray(rot_arrays['rotation_Omega_squared']) > 0))
    arrays_pin = wnpz(rot / 'rotation_base_arrays.npz', rot_arrays)
    st_arr = {} if empty else state_arrays(kmin, beyond=beyond)
    st_rec = h('state_record', {'schema': lib.STATE_SCHEMA, 'stage_kind': 'le_rotation', 'c_m_s': C, 'empty': empty,
                                'eps_certificate': dict(cert_pin), 'lo_certificate': dict(LO_PIN), 'roster_digest': 'ab' * 32,
                                'config_sha256': 'cd' * 32, 'kept': {'shape': 'cube', 'K_inverse_kpc': kmin}})
    st = lib.TailState(empty=empty, record=st_rec, arrays=st_arr)
    tail = {'record': wjson(root / 'tail' / 'TAIL_STATE_RECORD.json', st_rec),
            'arrays': wnpz(root / 'tail' / 'TAIL_STATE_ARRAYS.npz', h('state_arrays', st_arr))}
    fin = h('finish', {'status': 'LAGGED_M0_ROTATION_EVALUATED_NOT_FULL_FLOW', 'arrays_path': arrays_pin['path'],
                       'arrays_sha256': arrays_pin['sha256'], 'positive_rotation_square': positive,
                       'uv_tail': {'schema': 'UNT_UV_TAIL_ROUTE_B_STAGE_RECORD_C2V001', 'stage_kind': 'le_rotation',
                                   'state_digest': st.digest, 'roster_digest': st_rec['roster_digest'],
                                   'config_sha256': st_rec['config_sha256'],
                                   'config': {'eps_certificate': dict(cert_pin), 'lo_certificate': dict(LO_PIN)}}})
    wjson(rot / 'finish.json', fin)
    rows, sup = [], []
    for i, (q, r) in enumerate(zip(QIDS, RADII)):
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
                       'galaxy': 'NGC3198', 'call_spec_sha256': spec_sha, 'valid': positive,
                       'status': 'COMPLETED' if positive else 'COMPLETED_INVALID',
                       'reasons': [] if positive else ['final pass column failures or nonpositive rotation'],
                       'normalized_spec': {'galaxy': 'NGC3198', 'numerics': {'uv_tail': {
                           'eps_certificate': dict(cert_pin), 'lo_certificate': dict(LO_PIN)}}},
                       'final_pass': 2,
                       'passes': [{'pass': 1, 'rotation': str(out / 'stages' / '04_le1_rotation' / 'rotation')},
                                  {'pass': 2, 'rotation': str(rot), 'rotation_arrays': dict(arrays_pin),
                                   'rotation_positive': positive,
                                   'column_mean': {'path': cm_pin['path'], 'sha256': cm_pin['sha256'],
                                                   'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'},
                                   'rows': rows}],
                       'rows': rows, 'speeds_km_s': {r['id']: r['speed_km_s'] for r in rows}})
    wjson(out / 'result.json', res)
    wjson(out / 'finish.json', call_finish(res, out, hooks.get('finish_call')))
    return {'cert_pin': cert_pin, 'cert_rec': cert_rec, 'call_dir': str(root / 'call'), 'tail': tail,
            'spec_sha': spec_sha, 'qids': list(QIDS), 'R': R, 'omega': omega, 'fields': fields, 'sup': sup,
            'state': st, 'state_arrays': st_arr, 'key': key, 'out': out}


def rewrite_result(p, fn, finish_too=True):
    """Rewrite a built call's result.json with fn(result); finish.json is rewritten to match (driver form)."""
    rp = Path(p['out']) / 'result.json'
    r = fn(json.loads(rp.read_bytes()))
    replace_json(rp, r)
    if finish_too:
        replace_json(Path(p['out']) / 'finish.json', call_finish(r, p['out']))


def run_point(W, p, role='u_A', qids=None, log_index=None, **kw):
    return W.point_record(role=role, theta_key=p['key'], query_ids=qids or p['qids'], certificate=p['cert_pin'],
                          call_dir=p['call_dir'], tail_state_pins=p['tail'], call_spec_sha256=p['spec_sha'],
                          log_index=log_index, **kw)


def make_acceptance(work, tag, p, reading='ACCEPTED', over=None):
    call = Path(p['call_dir']).resolve()
    rp = (call / 'out' / 'result.json').resolve()
    rec = {'schema': 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001', 'label': 'SYNTHETIC TEST ACCEPTANCE RECORD',
           'call_dir': str(call), 'mode': 'guard', 'reading': reading, 'blockers': [], 'states': [],
           'result': {'path': str(rp), 'sha256': sha_bytes(rp.read_bytes())},
           'handoff': {'path': HANDOFF[0], 'sha256': HANDOFF[1]}}
    if over:
        rec = over(rec)
    return wjson(Path(work) / ('acceptance_%s.json' % tag), rec)


def make_manifest(work, tag='manifest', qids=None, radii=None, over=None):
    rows = [{'query_id': q, 'Rad_text': repr(r / KPC), 'Rad_unit': 'kpc'} for q, r in zip(qids or QIDS, radii or RADII)]
    m = {'schema': 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001', 'label': 'SYNTHETIC TEST MANIFEST', 'rad_unit': 'kpc',
         'rows': rows}
    if over:
        m = over(m)
    return wjson(Path(work) / ('%s.json' % tag), m)


def spec_of(p, role, *, acceptance=None, log_index=None, certificate='own', tail='own'):
    d = {'role': role, 'theta_key': p['key'], 'call_dir': p['call_dir'], 'call_spec_sha256': p['spec_sha'],
         'certificate': p['cert_pin'] if certificate == 'own' else certificate,
         'tail_state_pins': p['tail'] if tail == 'own' else tail, 'acceptance': acceptance}
    if log_index is not None:
        d['log_index'] = log_index
    return d


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


def gap(W):
    return getattr(W, 'PRODUCER_GAP', 'PRODUCER_GAP_ABSENT_IN_MODULE')


def fdump(path, name):
    for n in ast.parse(Path(path).read_text()).body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return ast.dump(n)


# ------------------------------------------------------------------------------------------------ v002 tests, ported
def tests_v002(W, work, consumers):
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
    rewrite_result(q, lambda r: dict(r, passes=[r['passes'][0], dict(r['passes'][1], rotation=str(outside))]))
    expect_refused(W, 'T11 refused: rotation finish outside the call own out dir', 'OUTSIDE_OWN_CALL', lambda: run_point(W, q))
    expect_refused(W, 'T12 refused: 42 query ids', 'QUERY_IDS', lambda: run_point(W, p, qids=p['qids'][:42]))
    expect_refused(W, 'T12 refused: duplicate query id', 'QUERY_IDS', lambda: run_point(W, p, qids=p['qids'][:42] + [p['qids'][0]]))
    sw_ = list(p['qids'])
    sw_[3], sw_[4] = sw_[4], sw_[3]
    expect_refused(W, 'T12 refused: values query order differs from the call rows (no reorder)', 'QUERY_ORDER_MISMATCH',
                   lambda: run_point(W, p, qids=sw_))
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
    q = build_point(W, work, 'cols', key(1), hooks={'support': lambda s: [dict(x, column_indices=[0, 1]) if i == 7 else x
                                                                          for i, x in enumerate(s)]})
    expect_refused(W, 'T14 refused: row columns differ from the column-mean support', 'ROW_COLUMNS_DIFFER_FROM_COLUMN_MEAN_SUPPORT',
                   lambda: run_point(W, q))
    q = build_point(W, work, 'supp', key(1), hooks={'support': lambda s: [dict(x, radius_m=50 * KPC) if i == 7 else x
                                                                          for i, x in enumerate(s)]})
    expect_refused(W, 'T15 refused: a valid row outside the radial support', 'ROTATION_ROWS_UNAVAILABLE', lambda: run_point(W, q))
    # T16 (W-3 change, disclosed): v002 refused a nonpositive rotation square (ROTATION_ROWS_UNAVAILABLE). Under A152
    # W-3 (v <= 0 -> eps None with the call's reason) the call that records it (COMPLETED_INVALID) gets 43 None.
    q = build_point(W, work, 'negom', key(1), omega_sign=-1.0)
    rq = run_point(W, q)
    record('T16 (W-3) nonpositive rotation square recorded by the call: 43 None with the call reason, no state read',
           rq['eps_km_s'] == [None] * 43 and all(w.startswith('NONPOSITIVE_ROTATION_IN_CALL (W-3, v <= 0)') and
                                                  'COMPLETED_INVALID' in w and 'nonpositive rotation' in w
                                                  for w in rq['eps_row_reason'])
           and rq['state'] is None and rq['call']['status'] == 'COMPLETED_INVALID', rq['eps_row_reason'][0][:160])
    vdoc = {'schema': 'PHASE1_NGC_VALUES_C2V001', 'query_ids': p['qids'], 'points': []}
    saved = W.ROOT_RULING
    W.ROOT_RULING = None
    try:
        expect_refused(W, 'T17 attach refused while ROOT_RULING is None (W-1 stop kept in code)', 'ROOT_RULING_PENDING',
                       lambda: W.attach_eps(vdoc, [rec], 'phase1_values'))
    finally:
        W.ROOT_RULING = saved
    P1 = consumers['v003']
    roles = ['u_A', 'F0', 'F1', 'F2']
    pts = [build_point(W, work, 'v_%s' % r_, key(10 + i), cert=make_cert(Path(work) / ('v_%s' % r_), 'v_%s' % r_,
                                                                         key(10 + i), scale=1.0 + 0.25 * i))
           for i, r_ in enumerate(roles)]
    recs = [run_point(W, x, role=r_) for x, r_ in zip(pts, roles)]
    vdoc = {'schema': 'PHASE1_NGC_VALUES_C2V001', 'query_ids': p['qids'],
            'points': [{'role': r_, 'theta_key': x['key'], 'valid': [i not in (0, 42) for i in range(43)],
                        'speeds_km_s': [None if i in (0, 42) else 100.0 + i for i in range(43)]} for x, r_ in zip(pts, roles)]}
    new = W.attach_eps(vdoc, recs, 'phase1_values')
    fd = {'u_A': {'log_index': 0}, 'members': [{'key': pts[0]['key'], 'log_index': 0}],
          'F': [{'role': r_, 'key': x['key']} for x, r_ in zip(pts[1:], roles[1:])]}
    P1.check_values(new, fd)
    ptsd = {x['role']: x for x in new['points']}
    ok_eps = all(ptsd[r_]['eps_km_s'] == rc['eps_km_s'] for r_, rc in zip(roles, recs))
    band_ok = True
    for q_ in range(43):
        es = [(ptsd[r_].get('eps_km_s') or [None] * 43)[q_] for r_ in roles]
        fin = all(isinstance(e, (int, float)) and not isinstance(e, bool) and math.isfinite(e) and e >= 0 for e in es)
        band_ok &= (fin == (q_ not in (0, 42)))
    record('T18a Phase-1 values: attached, phase1_c2v003 check_values accepts, band eps rule finite on valid rows only',
           ok_eps and band_ok and all('eps_km_s_custody' in x for x in new['points']) and 'eps_km_s' not in vdoc['points'][0]
           and all(x['eps_km_s_custody']['root_ruling'] == W.ROOT_RULING for x in new['points']))
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
    # T20 (port): the CLI gate, on a copy of the module with ROOT_RULING None
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'HOME')}
    gate = Path(work) / 'gate_copy'
    gate.mkdir()
    src = Path(W.__file__).read_text()
    old = "ROOT_RULING = {'path': V006, 'section': 'A152',"
    gp = gate / 'values_writer_c2v003a_ROOT_RULING_NONE.py'
    with open(gp, 'x') as f:
        f.write(src.replace(old, "ROOT_RULING = None and {'path': V006, 'section': 'A152',", 1))
    cp = subprocess.run([sys.executable, '-I', '-B', str(gp), 'point', '--args', '/nonexistent', '--args-sha256', '0' * 64,
                         '--out-dir', str(work)], capture_output=True, text=True, env=env)
    record('T20 CLI refuses while ROOT_RULING is None (exit 3; module copy with the pin removed)',
           src.count(old) == 1 and cp.returncode == 3 and 'ROOT_RULING_PENDING' in cp.stdout, cp.stdout.strip()[:200])
    od = Path(work) / 'writes'
    od.mkdir()
    pin1 = W.write_new(rec, od, 'R.json')
    try:
        W.write_new(rec, od, 'R.json')
        record('T21 exclusive create (a second write of the same name fails)', False)
    except FileExistsError:
        record('T21 exclusive create (a second write of the same name fails)',
               sha_bytes(Path(pin1['path']).read_bytes()) == pin1['sha256'])
    pi_ = build_point(W, work, 'incl', key(1), incl=(1.2, 1.1))
    ri = run_point(W, pi_)
    record('T23 sin(i_phys)/sin(i_released) printed from the call own packet, not applied (list unchanged)',
           ri['inclination']['applied'] is False and ri['inclination']['sin_ratio'] == math.sin(1.2) / math.sin(1.1)
           and ri['eps_km_s'] == eps and rec['inclination']['sin_ratio'] == 1.0)

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
    p2 = ART + '/phase1_c2/phase1_c2v002.py'
    record('T27 consumer: check_values, members_values and band_rows are AST-identical in phase1_c2v002 (d64351ec) '
           'and phase1_c2v003, so T18 covers both',
           sha_bytes(Path(p2).read_bytes()).startswith('d64351ec') and sha_bytes(Path(PHASE1_V003[0]).read_bytes()) == PHASE1_V003[1]
           and all(fdump(p2, f) is not None and fdump(p2, f) == fdump(PHASE1_V003[0], f)
                   for f in ('check_values', 'members_values', 'band_rows')))
    return p


# ------------------------------------------------------------------------------------------------ v003 tests
def section_of(raw, head):
    """Independent extraction for T30b: from '\\n## <head>' to the next '\\n## '."""
    i = raw.index(b'\n## ' + head.encode()) + 1
    j = raw.find(b'\n## ', i)
    return raw[i:(j + 1) if j >= 0 else len(raw)]


def tests_ruling(W, work):
    r = W.ROOT_RULING
    record('T30a ROOT_RULING pinned to V006 A152 (path, section, section sha 5aee4cc0) and the gate passes on the bytes',
           r == {'path': V006, 'section': 'A152', 'sha256': A152_SHA} and W.check_root_ruling() == r, repr(r)[:200])
    raw = Path(V006).read_bytes()
    sec = section_of(raw, 'A152')
    record('T30b independent extraction: one "## A152" heading; section sha256 == the pin; ends before "## A108 continued"',
           raw.count(b'\n## A152') == 1 and sha_bytes(sec) == A152_SHA and sec.startswith(b'## A152: how eps_km_s')
           and raw[raw.index(b'\n## A152') + 1 + len(sec):].startswith(b'## '), '%d bytes' % len(sec))
    d = Path(work) / 'ruling'
    d.mkdir()
    body = (b'# DECISIONS (synthetic)\n\n## A151: earlier\n\ntext\n\n## A152: the ruling (synthetic)\n\nW-1 text.\n\n'
            b'## A108 continued\n\ntail\n')
    syn_sec = section_of(body, 'A152')

    def put(name, b):
        p = d / name
        with open(p, 'xb') as f:
            f.write(b)
        return str(p)
    saved = W.ROOT_RULING
    try:
        base = put('base.md', body)
        W.ROOT_RULING = {'path': base, 'section': 'A152', 'sha256': sha_bytes(syn_sec)}
        record('T30c synthetic decisions file: the section pin passes', W.check_root_ruling() == W.ROOT_RULING)
        W.ROOT_RULING = {'path': put('appended.md', body.replace(b'## A108 continued', b'## A153: later\n\nmore\n\n## A108 continued')),
                         'section': 'A152', 'sha256': sha_bytes(syn_sec)}
        record('T30c a later section appended after A152: the pin still passes (section, not file, is pinned)',
               W.check_root_ruling() == W.ROOT_RULING)
        W.ROOT_RULING = {'path': put('a1520.md', body + b'\n## A1520: not A152\n\nx\n'), 'section': 'A152',
                         'sha256': sha_bytes(syn_sec)}
        record('T30c a "## A1520" heading is not the A152 heading (passes)', W.check_root_ruling() == W.ROOT_RULING)
        W.ROOT_RULING = {'path': put('edited.md', body.replace(b'W-1 text.', b'W-1 test.')), 'section': 'A152',
                         'sha256': sha_bytes(syn_sec)}
        expect_refused(W, 'T30c MUST_FAIL one byte changed inside A152', 'ROOT_RULING_SECTION_MISMATCH', W.check_root_ruling)
        W.ROOT_RULING = {'path': put('dup.md', body + b'\n## A152: a second one\n'), 'section': 'A152',
                         'sha256': sha_bytes(syn_sec)}
        expect_refused(W, 'T30c MUST_FAIL a duplicate A152 heading', 'ROOT_RULING_SECTION_NOT_UNIQUE', W.check_root_ruling)
        W.ROOT_RULING = {'path': str(d / 'missing.md'), 'section': 'A152', 'sha256': sha_bytes(syn_sec)}
        expect_refused(W, 'T30c MUST_FAIL ruling file unreadable', 'ROOT_RULING_UNREADABLE', W.check_root_ruling)
        W.ROOT_RULING = {'path': base, 'sha256': sha_bytes(syn_sec)}
        expect_refused(W, 'T30c MUST_FAIL ruling pin without its section', 'ROOT_RULING_INVALID', W.check_root_ruling)
        W.ROOT_RULING = dict(saved, sha256='0' * 64)
        expect_refused(W, 'T30c MUST_FAIL the real V006 with a wrong section sha', 'ROOT_RULING_SECTION_MISMATCH',
                       W.check_root_ruling)
        W.ROOT_RULING = None
        expect_refused(W, 'T30c MUST_FAIL ROOT_RULING None', 'ROOT_RULING_PENDING', W.check_root_ruling)
    finally:
        W.ROOT_RULING = saved
    t = sec.decode()
    ev = {
        'A152 W-1 rule text': "eps_km_s[q] = `srb_rot(S, C, rows)['bound_km_s'][q]`" in t,
        'A152 rows computed from own outputs': 'N_min, v_c, column radii and row_columns are all computed from the call' in t,
        'A152 not adopted A-1, A-2, A-3': '**Not adopted:** A-1 (v = speeds), A-2 (R_q in place of the column maximum) and '
                                          'A-3 (a declared N_min)' in t,
        'A152 W-3 valid rule': "valid[q] = the row's `valid` ∧ the call's `valid` ∧ status COMPLETED" in t,
        'A152 W-3 member_valid rule': 'member_valid = the call\'s `valid` ∧ COMPLETED ∧ the call\'s post-run per-state '
                                      'acceptance' in t and 'reading ACCEPTED or LO_UNCERTIFIED_TRANSIENT' in t,
        'A152 W-3 result_pin rule': 'result_pin = {`out/result.json` path, `finish.result_sha256`}' in t,
        'A152 W-3 speed None or v <= 0 -> eps None': 'A row with speed None, or with v ≤ 0, gets eps None and keeps the '
                                                     "call's reason (C-2)" in t,
        'A152 C-1..C-10 adopted; manifest a2936517 named read-only': 'C-1 to C-10 are adopted as built' in t
        and 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json` (`a2936517`) is **named, read-only**' in t,
        'A152 does not name A-4 (inclination factor): open item for root': 'A-4' not in t,
    }
    for k_, v_ in ev.items():
        record('T30d evidence: ' + k_, v_)


def tests_assemble(W, work, consumers):
    O = consumers['v003'].mod('O')
    aw = Path(work) / 'asm'
    man = make_manifest(aw)
    saved_man = W.MANIFEST
    W.MANIFEST = man
    try:
        _tests_assemble(W, aw, consumers, O)
    finally:
        W.MANIFEST = saved_man
    # T39d the real manifest (A152: named, read-only, ids and radii only)
    raw = Path(saved_man['path']).read_bytes()
    ids = [r['query_id'] for r in json.loads(raw)['rows']]
    ok_rad = None
    try:
        rad = W.check_manifest(ids)
        ok_rad = len(rad) == 43 and all(v > 0 for v in rad.values())
    except Exception as exc:     # noqa: BLE001
        ok_rad = False
        record('T39d real manifest check raised', False, repr(exc))
    record('T39d real query manifest: pin a2936517 == bytes (driver NGC_DATA); 43 ids NGC3198-Q01..Q43 in order; '
           'check_manifest passes (ids and radii only)',
           sha_bytes(raw) == saved_man['sha256'] and saved_man['sha256'].startswith('a2936517')
           and ids == ['NGC3198-Q%02d' % i for i in range(1, 44)] and ok_rad)
    expect_refused(W, 'T39d MUST_FAIL real manifest against a reversed id list', 'MANIFEST_ORDER_MISMATCH',
                   lambda: W.check_manifest(list(reversed(ids))))


def _tests_assemble(W, aw, consumers, O):
    P3, P3a = consumers['v003'], consumers.get('v003a')
    roles = ['u_A', 'F0', 'F1', 'F2']
    # ------------------------------------------------------------------ T31 Phase-1 MUST_PASS
    pts = {}
    for i, r_ in enumerate(roles):
        k = key(40 + i)
        pts[r_] = build_point(W, aw, 'p1_%s' % r_, k, cert=make_cert(aw / ('p1_%s' % r_), r_, k, scale=1.0 + 0.3 * i))
    acc = {r_: make_acceptance(aw, 'p1_%s' % r_, pts[r_], 'ACCEPTED' if r_ != 'F2' else 'INCOMPLETE') for r_ in roles}
    specs = [spec_of(pts[r_], r_, acceptance=acc[r_]) for r_ in roles]
    doc, recs = W.assemble('phase1_values', list(QIDS), specs)
    doc2, _r2 = W.assemble('phase1_values', list(QIDS), specs)
    fd = {'u_A': {'log_index': 0}, 'members': [{'key': pts['u_A']['key'], 'log_index': 0}],
          'F': [{'role': r_, 'key': pts[r_]['key']} for r_ in roles[1:]]}
    okc = []
    for name, P in (('v003', P3), ('v003a', P3a)):
        if P is None:
            continue
        try:
            P.check_values(doc, fd)
            okc.append(name)
        except Exception as exc:     # noqa: BLE001
            record('T31a consumer %s check_values raised' % name, False, repr(exc))
    record('T31a Phase-1 assemble: phase1 check_values accepts (%s)' % '+'.join(okc),
           okc == ['v003', 'v003a'][:len(okc)] and len(okc) == (2 if P3a is not None else 1) and doc['schema'] == W.VALUES_SCHEMA)
    byrole = {x['role']: x for x in doc['points']}
    rpin_ok = True
    for r_ in roles:
        rp = (Path(pts[r_]['call_dir']).resolve() / 'out' / 'result.json').resolve()
        fin = json.loads((rp.parent / 'finish.json').read_bytes())
        rpin_ok &= byrole[r_]['result_pin'] == {'path': str(rp), 'sha256': fin['result_sha256']} \
            and fin['result_sha256'] == sha_bytes(rp.read_bytes())
    record('T31b result_pin per W-3 = {resolved out/result.json, finish.result_sha256} (== sha of the bytes)', rpin_ok)
    record('T31c speeds_km_s = the call rows in query_ids order; valid = row valid (rows 0, 42 false); no member_valid on '
           'Phase-1 points; no log_index',
           all(byrole[r_]['speeds_km_s'] == [None] + [100.0 + i for i in range(1, 42)] + [None]
               and byrole[r_]['valid'] == [i not in (0, 42) for i in range(43)]
               and 'member_valid' not in byrole[r_] and 'log_index' not in byrole[r_] for r_ in roles))
    direct = {r_: run_point(W, pts[r_], role=r_) for r_ in roles}
    record('T31d eps_km_s per W-1 = the point record (and the oracle) for every role; rows 0 and 42 None with the call reason',
           all(byrole[r_]['eps_km_s'] == direct[r_]['eps_km_s'] for r_ in roles)
           and all(max(abs(a - b) / b for a, b in zip([e for e in byrole[r_]['eps_km_s'] if e is not None], oracle(pts[r_])))
                   <= 1e-12 for r_ in roles)
           and all(rc['eps_row_reason'][0] == 'ROW_INVALID_IN_CALL: QUERY_INSIDE_INNERMOST_NODE' for rc in recs))
    record('T31e Phase-1 acceptance is printed, not gated (W-3 names acceptance only in member_valid): F2 INCOMPLETE '
           'keeps its row valid flags',
           byrole['F2']['acceptance']['reading'] == 'INCOMPLETE' and byrole['F2']['valid'] == byrole['u_A']['valid'])
    record('T31f custody: root_ruling A152 pin on the document and every point; manifest order equal; radius diff <= 1e-9; '
           'deterministic (two assemblies, equal canonical bytes)',
           doc['assembly']['root_ruling'] == W.ROOT_RULING and all(x['eps_km_s_custody']['root_ruling'] == W.ROOT_RULING
                                                                   for x in doc['points'])
           and doc['assembly']['manifest']['order_equal'] is True
           and doc['assembly']['manifest']['max_rel_radius_difference'] <= 1e-9
           and W.canonical(doc) == W.canonical(doc2) and recs[0]['schema'] == 'UNT_POINT_EPS_KM_S_C2V003')
    # ------------------------------------------------------------------ T32 Phase-2 MUST_PASS (members_values)
    readings = [('ACCEPTED', True), ('LO_UNCERTIFIED_TRANSIENT', True), ('INCOMPLETE', False),
                ('NON_LAPSE_TAIL_MATERIAL', False), ('ACCEPTED_PASS_FLAGGED', False), ('BOUND_INSUFFICIENT', False),
                ('UNDECIDABLE_FLAGGED', False), (None, False)]
    thetas = [{'syn_a': 0.1 * (i + 1), 'syn_b': 0.2 * (i + 1)} for i in range(len(readings) + 1)]
    mkeys = [O.theta_key(t) for t in thetas]
    mspecs, mpts = [], []
    for i, (rd, _want) in enumerate(readings):
        q = build_point(W, aw, 'm_%d' % i, mkeys[i], cert=make_cert(aw / ('m_%d' % i), 'm_%d' % i, mkeys[i], role='member'))
        mpts.append(q)
        mspecs.append(spec_of(q, 'member', log_index=200 + i,
                              acceptance=make_acceptance(aw, 'm_%d' % i, q, rd) if rd else None))
    nc = build_point(W, aw, 'm_nocert', mkeys[-1])
    mspecs.append(spec_of(nc, 'member', log_index=299, acceptance=make_acceptance(aw, 'm_nocert', nc, 'ACCEPTED'),
                          certificate=None, tail=None))
    run2 = {'exploration': {'admitted_points': [{'log_index': 200 + i, 'theta_natural': thetas[i]}
                                                for i in range(len(readings))]
                            + [{'log_index': 299, 'theta_natural': thetas[-1]}]}}
    mdoc, mrecs = W.assemble('phase2_members', list(QIDS), mspecs)
    okm = []
    for name, P in (('v003', P3), ('v003a', P3a)):
        if P is None:
            continue
        try:
            mv = P.members_values(mdoc, run2)
            P.check_member_eps(mv, 43)
            okm.append((name, sorted(mv)))
        except Exception as exc:     # noqa: BLE001
            record('T32a consumer %s members_values/check_member_eps raised' % name, False, repr(exc))
    want_li = sorted([200 + i for i in range(len(readings))] + [299])
    record('T32a Phase-2 assemble: phase1 members_values (theta key = orchestrator theta_key of the admitted point) and '
           'check_member_eps accept (%s)' % '+'.join(n for n, _l in okm),
           len(okm) == (2 if P3a is not None else 1) and all(li == want_li for _n, li in okm))
    mv = {x['log_index']: x for x in mdoc['points']}
    got = {rd: mv[200 + i]['member_valid'] for i, (rd, _w) in enumerate(readings)}
    printed = all((mv[200 + i]['acceptance'] is None) if rd is None else (
        mv[200 + i]['acceptance']['reading'] == rd and mv[200 + i]['acceptance']['counts_for_member_valid'] is False
        and mv[200 + i]['acceptance'].get('g5_producer') is False and mv[200 + i]['acceptance'].get('basis') == gap(W))
        for i, (rd, _w) in enumerate(readings))
    basis = all(mv[200 + i].get('member_valid_basis') == (['NO_ACCEPTANCE_RECORD'] if rd is None else [gap(W)])
                for i, (rd, _w) in enumerate(readings))
    gate = mdoc['assembly'].get('member_valid_gate')
    record('T32b (B1, inverted from v003) member_valid false for every reading of the c2v004 (DDO154) record, ACCEPTED and '
           'LO_UNCERTIFIED_TRANSIENT included, and with no record: no A136 G5 producer is pinned (A153 "no NGC member is '
           'valid"); each reading printed with counts_for_member_valid false; member_valid_basis names the producer gap '
           '(UNTESTED, not a null); the members document prints the empty gate',
           all(got[rd] is False for rd, _w in readings) and printed and basis
           and gate == {'producers': [], 'route_required': G5_ROUTE, 'basis': gap(W)}
           and 'UNTESTED, not a null' in gap(W) and G5_ROUTE in gap(W), repr(got))
    reads = [P3.member_eps(mv[299]['eps_km_s'], q_) for q_ in range(43)]
    record('T32c uncertified member with an ACCEPTED c2v004 record: member_valid false (B1), eps 43 None -> member_eps '
           'MEMBER_EPS_NONE on every row (A144 R3 flags the pairs); speeds and valid still per W-3',
           mv[299]['member_valid'] is False and mv[299].get('member_valid_basis') == [gap(W)]
           and all(x == (None, 'MEMBER_EPS_NONE') for x in reads)
           and mv[299]['speeds_km_s'][5] == 105.0 and mv[299]['valid'][5] is True
           and [r_ for r_ in mrecs if r_['theta_key'] == mkeys[-1]][0]['eps_row_reason'] == ['NO_POINT_CERTIFICATE'] * 43)
    record('T32d members carry log_index, member_valid, result_pin, valid, speeds_km_s, eps_km_s (A133 contract)',
           all({'role', 'log_index', 'theta_key', 'member_valid', 'result_pin', 'valid', 'speeds_km_s', 'eps_km_s'}
               <= set(x) for x in mdoc['points']))
    # at0b re-bind: the u_A call as a Phase-2 member carries the same result_pin sha as Phase-1 u_A
    k_u = pts['u_A']['key']
    udoc, _ur = W.assemble('phase2_members', list(QIDS), [spec_of(pts['u_A'], 'member', log_index=0, acceptance=acc['u_A'])])
    record('T32e at0b re-bind: the u_A call assembled as member 0 carries the Phase-1 u_A result_pin sha',
           udoc['points'][0]['result_pin']['sha256'] == byrole['u_A']['result_pin']['sha256']
           and udoc['points'][0]['theta_key'] == k_u)
    # ------------------------------------------------------------------ T33 order
    perm = list(QIDS)
    perm[3], perm[4] = perm[4], perm[3]
    expect_refused(W, 'T33a MUST_FAIL values query_ids differ from the manifest order', 'MANIFEST_ORDER_MISMATCH',
                   lambda: W.assemble('phase1_values', perm, specs))
    sw = build_point(W, aw, 'swap', key(60), hooks={'rows': lambda rs: rs[:3] + [rs[4], rs[3]] + rs[5:]})
    sw_specs = [spec_of(sw, 'u_A', acceptance=None)] + specs[1:]
    expect_refused(W, 'T33b MUST_FAIL the call rows in another order (certified point)', 'QUERY_ORDER_MISMATCH',
                   lambda: W.assemble('phase1_values', list(QIDS), sw_specs))
    expect_refused(W, 'T33c MUST_FAIL the call rows in another order (uncertified member: final_rows alone)',
                   'QUERY_ORDER_MISMATCH',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(sw, 'member', log_index=1, certificate=None,
                                                                             tail=None)]))
    # ------------------------------------------------------------------ T34 status / call valid
    ci = build_point(W, aw, 'colfail', key(61), hooks={'result': lambda r: dict(
        r, valid=False, status='COMPLETED_INVALID', reasons=['final pass column failures or nonpositive rotation'])})
    d1, r1 = W.assemble('phase2_members', list(QIDS), [spec_of(ci, 'member', log_index=1,
                                                               acceptance=make_acceptance(aw, 'colfail', ci, 'ACCEPTED'))])
    p_ = d1['points'][0]
    record('T34a MUST_FAIL flags: call invalid (COMPLETED_INVALID, valid false, rotation positive) -> valid all false and '
           'member_valid false despite ACCEPTED; speeds kept as recorded; eps per W-1 on the own outputs',
           p_['valid'] == [False] * 43 and p_['member_valid'] is False and p_['speeds_km_s'][1] == 101.0
           and p_.get('member_valid_basis') == ['CALL_NOT_VALID', 'STATUS_NOT_COMPLETED: COMPLETED_INVALID', gap(W)]
           and p_['eps_km_s'] == run_point(W, ci, role='member', log_index=1)['eps_km_s'] and p_['eps_km_s'][1] is not None)
    fs = build_point(W, aw, 'failrows', key(62), hooks={'result': lambda r: dict(r, status='FAILED')})
    d2, _r = W.assemble('phase2_members', list(QIDS), [spec_of(fs, 'member', log_index=2,
                                                               acceptance=make_acceptance(aw, 'failrows', fs, 'ACCEPTED'))])
    p_ = d2['points'][0]
    record('T34b MUST_FAIL flags: status FAILED with valid true and final rows, acceptance ACCEPTED -> valid all false, '
           'member_valid false (status not COMPLETED)',
           p_['valid'] == [False] * 43 and p_['member_valid'] is False and p_['call']['result_valid'] is True
           and p_.get('member_valid_basis') == ['STATUS_NOT_COMPLETED: FAILED', gap(W)]
           and p_['speeds_km_s'][2] == 102.0)
    nr = build_point(W, aw, 'norows', key(63), hooks={'result': lambda r: {k: v for k, v in dict(
        r, status='FAILED_AT_STAGE', valid=False, reasons=['stage le2_column_mean failed (synthetic)']).items()
        if k not in ('rows', 'speeds_km_s')}})
    d3, r3 = W.assemble('phase2_members', list(QIDS), [spec_of(nr, 'member', log_index=3)])
    p_ = d3['points'][0]
    P3.check_member_eps({3: p_}, 43)
    record('T34c status FAILED_AT_STAGE with no final rows: speeds 43 None, valid 43 false, member_valid false, eps 43 None '
           'with the call status and reasons; check_member_eps accepts',
           p_['speeds_km_s'] == [None] * 43 and p_['valid'] == [False] * 43 and p_['member_valid'] is False
           and p_.get('member_valid_basis') == ['CALL_NOT_VALID', 'STATUS_NOT_COMPLETED: FAILED_AT_STAGE', 'NO_ACCEPTANCE_RECORD']
           and p_['eps_km_s'] == [None] * 43
           and all(w.startswith('CALL_HAS_NO_FINAL_ROWS (W-3, speed None): status FAILED_AT_STAGE') and 'synthetic' in w
                   for w in r3[0]['eps_row_reason']))
    nr2 = build_point(W, aw, 'norows_otherpin', key(74), hooks={'result': lambda r: {k: v for k, v in dict(
        r, status='FAILED_AT_STAGE', valid=False, reasons=['synthetic'], normalized_spec={'numerics': {'uv_tail': {
            'eps_certificate': {'path': '/synthetic/o.json', 'sha256': 'f' * 64}}}}).items() if k not in ('rows', 'speeds_km_s')}})
    expect_refused(W, 'T34e MUST_FAIL no final rows, but the call ran with another certificate (spec eps pin)',
                   'CALL_EPS_PIN_NOT_THE_POINT_CERTIFICATE',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(nr2, 'member', log_index=3)]))
    for name, hk, code in (
            ('status COMPLETED with valid false', {'result': lambda r: dict(r, valid=False)}, 'CALL_STATUS_VALID_INCONSISTENT'),
            ('status COMPLETED_INVALID with valid true', {'result': lambda r: dict(r, status='COMPLETED_INVALID')},
             'CALL_STATUS_VALID_INCONSISTENT'),
            ('unknown status', {'result': lambda r: dict(r, status='DONE')}, 'CALL_STATUS_UNKNOWN'),
            ('status COMPLETED without final rows', {'result': lambda r: {k: v for k, v in r.items() if k != 'rows'}},
             'COMPLETED_WITHOUT_FINAL_ROWS'),
            ('result.speeds_km_s differs from result.rows',
             {'result': lambda r: dict(r, speeds_km_s=dict(r['speeds_km_s'], **{'SYN-Q05': 1.0}))},
             'SPEEDS_DICT_DIFFERS_FROM_ROWS'),
            ('43 rows required (42 rows)', {'result': lambda r: dict(r, rows=r['rows'][:42])}, 'FINAL_ROWS_SHAPE')):
        q = build_point(W, aw, uniq('st'), key(64), hooks=hk)
        expect_refused(W, 'T34d MUST_FAIL ' + name, code,
                       lambda q=q: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=4)]))
    # ------------------------------------------------------------------ T35 acceptance refusals
    a0 = mpts[0]
    for name, over, code in (
            ('unknown reading PASS', lambda r: dict(r, reading='PASS'), 'ACCEPTANCE_READING_UNKNOWN'),
            ('another call result pin', lambda r: dict(r, result={'path': r['result']['path'], 'sha256': '0' * 64}),
             'ACCEPTANCE_NOT_OF_THIS_CALL'),
            ('another call directory', lambda r: dict(r, call_dir=r['call_dir'] + '_other'), 'ACCEPTANCE_NOT_OF_THIS_CALL'),
            ('schema not the handoff record', lambda r: dict(r, schema='DDO154_TAIL_ACCEPTANCE_RECORD_C2V000'),
             'ACCEPTANCE_SCHEMA'),
            ('handoff not reviewed', lambda r: dict(r, handoff={'path': '/x/handoff.py', 'sha256': '1' * 64}),
             'ACCEPTANCE_PRODUCER_NOT_REVIEWED')):
        ap = make_acceptance(aw, uniq('bad'), a0, over=over)
        expect_refused(W, 'T35 MUST_FAIL acceptance: ' + name, code,
                       lambda ap=ap: W.assemble('phase2_members', list(QIDS),
                                                [spec_of(a0, 'member', log_index=7, acceptance=ap)]))
    other_acc = make_acceptance(aw, 'm1_for_m0', mpts[1], 'ACCEPTED')
    expect_refused(W, 'T35 MUST_FAIL acceptance record of another member call', 'ACCEPTANCE_NOT_OF_THIS_CALL',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(a0, 'member', log_index=7, acceptance=other_acc)]))
    good_acc = make_acceptance(aw, 'm0_good', a0, 'ACCEPTED')
    expect_refused(W, 'T35 MUST_FAIL acceptance pin sha mismatch', 'PIN_SHA_MISMATCH',
                   lambda: W.assemble('phase2_members', list(QIDS),
                                      [spec_of(a0, 'member', log_index=7, acceptance=dict(good_acc, sha256='0' * 64))]))
    # ------------------------------------------------------------------ T36 finish / result pin
    for name, hk, code in (
            ('finish.result_sha256 not the result bytes', {'finish_call': lambda f: dict(f, result_sha256='0' * 64)},
             'FINISH_RESULT_SHA_MISMATCH'),
            ('finish.result_path another file', {'finish_call': lambda f: dict(f, result_path=f['result_path'].replace(
                'out/result.json', 'out/stages/08_le2_column_mean/observation/result.json'))}, 'FINISH_RESULT_PATH'),
            ('finish.status differs from result.status', {'finish_call': lambda f: dict(f, status='COMPLETED_INVALID')},
             'FINISH_RESULT_INCONSISTENT'),
            ('finish.valid differs from result.valid', {'finish_call': lambda f: dict(f, valid=False)},
             'FINISH_RESULT_INCONSISTENT')):
        q = build_point(W, aw, uniq('fin'), key(65), hooks=hk)
        expect_refused(W, 'T36 MUST_FAIL ' + name, code,
                       lambda q=q: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=8)]))
    q = build_point(W, aw, 'fin_altered', key(66))
    rewrite_result(q, lambda r: dict(r, reasons=['edited after the run']), finish_too=False)
    expect_refused(W, 'T36 MUST_FAIL result.json bytes altered after finish.json was written', 'FINISH_RESULT_SHA_MISMATCH',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=8)]))
    q = build_point(W, aw, 'fin_missing', key(67))
    (Path(q['out']) / 'finish.json').unlink()
    expect_refused(W, 'T36 MUST_FAIL out/finish.json missing', 'CALL_RESULT_MISSING',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=8)]))
    # ------------------------------------------------------------------ T37 speed None / v <= 0
    vz = build_point(W, aw, 'vle0', key(68), hooks={'rows': lambda rs: [dict(r, speed_km_s=0.0) if i == 5 else
                                                                         dict(r, speed_km_s=-3.0) if i == 9 else r
                                                                         for i, r in enumerate(rs)]})
    d4, r4 = W.assemble('phase2_members', list(QIDS), [spec_of(vz, 'member', log_index=9,
                                                               acceptance=make_acceptance(aw, 'vle0', vz, 'ACCEPTED'))])
    p_ = d4['points'][0]
    rd4 = r4[0]
    record('T37a MUST_PASS speed None -> eps None with the call reason (rows 0 and 42), valid false; member_eps flags '
           'MEMBER_EPS_NONE',
           p_['speeds_km_s'][0] is None and p_['eps_km_s'][0] is None and p_['valid'][0] is False
           and rd4['eps_row_reason'][0] == 'ROW_INVALID_IN_CALL: QUERY_INSIDE_INNERMOST_NODE'
           and rd4['eps_row_reason'][42] == 'ROW_INVALID_IN_CALL: QUERY_BEYOND_OUTER_GAS_CUT'
           and P3.member_eps(p_['eps_km_s'], 0) == (None, 'MEMBER_EPS_NONE'))
    record('T37b W-3 v <= 0: rows with speed 0.0 and -3.0 get eps None with ROW_SPEED_NONPOSITIVE_IN_CALL; their valid '
           'flags stay per W-3 (row valid, call valid, COMPLETED); other rows bounded; member_valid false (B1 gap only)',
           p_['eps_km_s'][5] is None and p_['eps_km_s'][9] is None
           and rd4['eps_row_reason'][5] == 'ROW_SPEED_NONPOSITIVE_IN_CALL (W-3, v <= 0): speed_km_s 0.0'
           and rd4['eps_row_reason'][9] == 'ROW_SPEED_NONPOSITIVE_IN_CALL (W-3, v <= 0): speed_km_s -3.0'
           and p_['valid'][5] is True and p_['member_valid'] is False and p_.get('member_valid_basis') == [gap(W)]
           and p_['eps_km_s'][6] is not None
           and sum(e is not None for e in p_['eps_km_s']) == 39)
    # ------------------------------------------------------------------ T38 nonpositive rotation (W-3 v <= 0)
    ng = build_point(W, aw, 'negom', key(69), omega_sign=-1.0)
    d5, r5 = W.assemble('phase2_members', list(QIDS), [spec_of(ng, 'member', log_index=10,
                                                               acceptance=make_acceptance(aw, 'negom', ng, 'ACCEPTED'))])
    p_ = d5['points'][0]
    record('T38a nonpositive rotation recorded by the call (COMPLETED_INVALID): eps 43 None with the call reason, valid '
           'false, member_valid false',
           p_['eps_km_s'] == [None] * 43 and p_['valid'] == [False] * 43 and p_['member_valid'] is False
           and p_.get('member_valid_basis') == ['CALL_NOT_VALID', 'STATUS_NOT_COMPLETED: COMPLETED_INVALID', gap(W)]
           and r5[0]['eps_row_reason'][3].startswith('NONPOSITIVE_ROTATION_IN_CALL'))
    for name, kw, hk, code in (
            ('arrays nonpositive but the call records rotation_positive true', {'omega_sign': -1.0},
             {'result': lambda r: dict(r, valid=True, status='COMPLETED', reasons=[], passes=[r['passes'][0], dict(
                 r['passes'][1], rotation_positive=True)]), 'finish': lambda f: dict(f, positive_rotation_square=True)},
             'ROTATION_POSITIVITY_INCONSISTENT'),
            ('call records nonpositive rotation but its arrays are positive', {},
             {'result': lambda r: dict(r, valid=False, status='COMPLETED_INVALID', passes=[r['passes'][0], dict(
                 r['passes'][1], rotation_positive=False)]), 'finish': lambda f: dict(f, positive_rotation_square=False)},
             'ROTATION_POSITIVITY_INCONSISTENT'),
            ('rotation_positive not recorded', {},
             {'result': lambda r: dict(r, passes=[r['passes'][0], {k: v for k, v in r['passes'][1].items()
                                                                   if k != 'rotation_positive'}])},
             'ROTATION_POSITIVITY_UNRECORDED'),
            ('passes[-1].rotation_positive differs from the stage finish', {},
             {'finish': lambda f: dict(f, positive_rotation_square=False)}, 'ROTATION_POSITIVITY_UNRECORDED')):
        q = build_point(W, aw, uniq('rot'), key(70), hooks=hk, **kw)
        expect_refused(W, 'T38b MUST_FAIL ' + name, code,
                       lambda q=q: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=11)]))
    # ------------------------------------------------------------------ T39 manifest radii
    q = build_point(W, aw, 'radsup', key(71), hooks={'support': lambda s: [dict(x, radius_m=x['radius_m'] * (1 + 1e-6))
                                                                           if i == 11 else x for i, x in enumerate(s)]})
    expect_refused(W, 'T39a MUST_FAIL a valid row support radius differs from the manifest (1e-6 relative)',
                   'MANIFEST_RADIUS_MISMATCH',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=12)]))
    q = build_point(W, aw, 'radrow', key(72), hooks={'rows': lambda rs: [dict(r, radius_m=r['radius_m'] * 1.01) if i == 42
                                                                         else r for i, r in enumerate(rs)]})
    expect_refused(W, 'T39b MUST_FAIL an invalid row radius_m differs from the manifest (uncertified member)',
                   'MANIFEST_RADIUS_MISMATCH',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=13, certificate=None,
                                                                             tail=None)]))
    q = build_point(W, aw, 'radboth', key(73), hooks={'rows': lambda rs: [dict(r, radius_m=RADII[i] * 1.01) if i == 12 else r
                                                                          for i, r in enumerate(rs)]})
    expect_refused(W, 'T39e MUST_FAIL a valid row radius_m differs from the manifest while its support radius agrees '
                   '(both are cross-checked)', 'MANIFEST_RADIUS_MISMATCH',
                   lambda: W.assemble('phase2_members', list(QIDS), [spec_of(q, 'member', log_index=14)]))
    saved = W.MANIFEST
    try:
        W.MANIFEST = dict(saved, sha256='0' * 64)
        expect_refused(W, 'T39c MUST_FAIL manifest pin sha mismatch', 'PIN_SHA_MISMATCH',
                       lambda: W.assemble('phase1_values', list(QIDS), specs))
        W.MANIFEST = make_manifest(aw, 'manifest_m', over=lambda m: dict(m, rad_unit='m'))
        expect_refused(W, 'T39c MUST_FAIL manifest rad_unit not kpc', 'MANIFEST_SCHEMA',
                       lambda: W.assemble('phase1_values', list(QIDS), specs))
    finally:
        W.MANIFEST = saved
    # ------------------------------------------------------------------ T40 assemble inputs
    for name, kind, sp, code in (
            ('Phase-1 without F2', 'phase1_values', specs[:3], 'PHASE1_ROLES'),
            ('Phase-1 with a member', 'phase1_values', specs + [mspecs[0]], 'PHASE1_ROLES'),
            ('Phase-1 point with a log_index', 'phase1_values', [dict(specs[0], log_index=0)] + specs[1:], 'PHASE1_ROLES'),
            ('members with a u_A role', 'phase2_members', [dict(mspecs[0], role='u_A')], 'MEMBERS_ROLE'),
            ('members duplicate log_index', 'phase2_members', [mspecs[0], dict(mspecs[1], log_index=200)],
             'MEMBERS_LOG_INDEX'),
            ('members bool log_index', 'phase2_members', [dict(mspecs[0], log_index=True)], 'MEMBERS_LOG_INDEX'),
            ('members missing log_index', 'phase2_members', [{k: v for k, v in mspecs[0].items() if k != 'log_index'}],
             'MEMBERS_LOG_INDEX'),
            ('unknown point field', 'phase2_members', [dict(mspecs[0], speeds_km_s=[1.0] * 43)], 'POINT_FIELDS'),
            ('duplicate theta key', 'phase2_members', [mspecs[0], dict(mspecs[1], theta_key=mspecs[0]['theta_key'])],
             'THETA_KEY_DUPLICATE'),
            ('kind', 'phase3', specs, 'KIND'),
            ('call spec sha not the point custody spec', 'phase2_members', [dict(mspecs[0], call_spec_sha256='0' * 64)],
             'CALL_SPEC_SHA'),
            ('empty point list', 'phase2_members', [], 'POINTS')):
        expect_refused(W, 'T40 MUST_FAIL assemble input: ' + name, code,
                       lambda kind=kind, sp=sp: W.assemble(kind, list(QIDS), sp))
    saved = W.ROOT_RULING
    W.ROOT_RULING = None
    try:
        expect_refused(W, 'T40 MUST_FAIL assemble while ROOT_RULING is None', 'ROOT_RULING_PENDING',
                       lambda: W.assemble('phase1_values', list(QIDS), specs))
    finally:
        W.ROOT_RULING = saved
    # ------------------------------------------------------------------ T41 the post-attach W-3 guard
    real_pr = W.point_record

    def tampered(**kw):
        r_ = real_pr(**kw)
        if kw['role'] == 'F1':
            r_ = dict(r_, eps_km_s=[1.0] + r_['eps_km_s'][1:], eps_row_reason=[None] + r_['eps_row_reason'][1:])
        return r_
    W.point_record = tampered
    try:
        expect_refused(W, 'T41 MUST_FAIL a record with eps on a speed-None row (tampered point_record) is refused after attach',
                       'EPS_WITHOUT_SPEED', lambda: W.assemble('phase1_values', list(QIDS), specs))
    finally:
        W.point_record = real_pr
    # ------------------------------------------------------------------ T42 CLI (module copy with the synthetic manifest)
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'HOME')}
    cdir = aw / 'cli'
    cdir.mkdir()
    src = Path(W.__file__).read_text()
    cp_mod = cdir / 'values_writer_c2v003a_SYNTHETIC_MANIFEST.py'
    with open(cp_mod, 'x') as f:
        f.write(src.replace("\nif __name__ == '__main__':", "\nMANIFEST = %r  # TEST COPY ONLY\n\nif __name__ == '__main__':"
                            % (W.MANIFEST,), 1))
    args = {'kind': 'phase1_values', 'query_ids': list(QIDS), 'points': specs, 'name': 'PHASE1_VALUES_SYNTHETIC.json'}
    ap = wjson(cdir / 'assemble_args.json', args)
    od = cdir / 'out'
    od.mkdir()
    cmd = [sys.executable, '-I', '-B', str(cp_mod), 'assemble', '--args', ap['path'], '--args-sha256', ap['sha256'],
           '--out-dir', str(od)]
    c1 = subprocess.run(cmd, capture_output=True, text=True, env=env)
    ok = False
    try:
        pin = json.loads(c1.stdout.strip().splitlines()[-1])
        vd = json.loads(Path(pin['path']).read_bytes())
        P3.check_values(vd, fd)
        ok = (c1.returncode == 0 and sha_bytes(Path(pin['path']).read_bytes()) == pin['sha256'] and len(pin['records']) == 4
              and all(sha_bytes(Path(x['path']).read_bytes()) == x['sha256'] for x in pin['records'])
              and [x['eps_km_s'] for x in vd['points']] == [x['eps_km_s'] for x in doc['points']])
    except Exception as exc:     # noqa: BLE001
        record('T42a CLI assemble raised', False, '%r | %s' % (exc, c1.stdout[-300:]))
    record('T42a CLI assemble (python3 -I -B): exit 0; 4 point records and the values document written by exclusive '
           'create, shas from bytes; check_values accepts; eps equal to the in-process assembly', ok, c1.stdout[-200:])
    c2 = subprocess.run(cmd, capture_output=True, text=True, env=env)
    record('T42b CLI assemble a second time into the same out dir: refused (exclusive create), exit 3',
           c2.returncode == 3 and 'REFUSED' in c2.stdout and 'File exists' in c2.stdout, c2.stdout[-200:])
    c3 = subprocess.run([sys.executable, str(cp_mod), 'assemble', '--args', ap['path'], '--args-sha256', ap['sha256'],
                         '--out-dir', str(od)], capture_output=True, text=True, env=env)
    record('T42c CLI without -I -B refused (ISOLATED_INTERPRETER_REQUIRED)',
           c3.returncode == 3 and 'ISOLATED_INTERPRETER_REQUIRED' in c3.stdout, c3.stdout[-200:])
    pa = wjson(cdir / 'point_args.json', {'role': 'u_A', 'theta_key': pts['u_A']['key'], 'query_ids': list(QIDS),
                                          'certificate': pts['u_A']['cert_pin'], 'call_dir': pts['u_A']['call_dir'],
                                          'tail_state_pins': pts['u_A']['tail'], 'call_spec_sha256': pts['u_A']['spec_sha']})
    od2 = cdir / 'out_point'
    od2.mkdir()
    c4 = subprocess.run([sys.executable, '-I', '-B', str(cp_mod), 'point', '--args', pa['path'], '--args-sha256',
                         pa['sha256'], '--out-dir', str(od2)], capture_output=True, text=True, env=env)
    ok4 = False
    try:
        pin4 = json.loads(c4.stdout.strip().splitlines()[-1])
        ok4 = c4.returncode == 0 and json.loads(Path(pin4['path']).read_bytes())['eps_km_s'] == byrole['u_A']['eps_km_s']
    except Exception:     # noqa: BLE001
        ok4 = False
    record('T42d CLI point (now ungated by the pinned ruling): exit 0, eps equal to the assembled u_A', ok4, c4.stdout[-200:])


def tests_b1(W, work, consumers):
    """T45 (v003a, review blocker B1): member_valid admits no acceptance producer until the A136 G5 NGC handoff is
    pinned (A153). Synthetic calls and records; v003 (dd9456bc) is loaded by sha for the differential only."""
    raw6 = Path(V006).read_bytes()
    a136, a153, a155 = (section_of(raw6, h).decode() for h in ('A136', 'A153', 'A155'))
    v6 = raw6.decode().splitlines()
    ln = {k: [i + 1 for i, x in enumerate(v6) if k in x] for k in (
        '| G5 | Route string `%s`' % G5_ROUTE, 'and no NGC member is valid.** That is UNTESTED, not a null.',
        'member_valid needs this verdict before the freeze (A152 W-3)',
        'A root workflow builds the NGC per-state adapter, enumerator and handoff')}
    hb = Path(HANDOFF[0]).read_bytes()
    record('T45a B1 evidence from bytes: A136 G5 route string (V006 L%s); A153 "no NGC member is valid" (L%s), '
           '"member_valid needs this verdict" (L%s), NGC adapter/enumerator/handoff a root build (L%s); A155 closure: NGC '
           'states reach the gate only once the reviewed NGC adapter is in place; handoff c2v004 (5ff464cc) has no G5 route '
           'string, no NGC_LO_TOLERANCE_NOT_DECLARED and no TI_B_SCALE_R_V001, and its record schema is DDO154; v003a '
           'MEMBER_ACCEPTANCE_PRODUCERS is empty and NGC_ACCEPTANCE_ROUTE is the G5 string'
           % tuple(','.join(map(str, v)) for v in ln.values()),
           all(len(v) == 1 for v in ln.values()) and G5_ROUTE in a136 and 'no NGC member is valid' in a153
           and 'once the reviewed NGC adapter and the contract review are in place' in a155
           and sha_bytes(hb) == HANDOFF[1] and G5_ROUTE.encode() not in hb and b'NGC_LO_TOLERANCE_NOT_DECLARED' not in hb
           and b'TI_B_SCALE_R_V001' not in hb and b"RECORD_SCHEMA = 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'" in hb
           and getattr(W, 'MEMBER_ACCEPTANCE_PRODUCERS', None) == () and getattr(W, 'NGC_ACCEPTANCE_ROUTE', None) == G5_ROUTE,
           repr(ln))
    raw3 = Path(WRITER_V003[0]).read_bytes()
    if sha_bytes(raw3) != WRITER_V003[1]:
        record('T45 v003 writer dd9456bc unavailable for the differential', False, sha_bytes(raw3))
        return
    V3 = load(WRITER_V003[0], 'vw3_values_writer_c2v003_for_b1')
    bw = Path(work) / 'b1'
    man = make_manifest(bw)
    saved = (W.MANIFEST, V3.MANIFEST, getattr(W, 'MEMBER_ACCEPTANCE_PRODUCERS', ()))
    W.MANIFEST = V3.MANIFEST = man
    try:
        _tests_b1(W, V3, bw, consumers)
    finally:
        W.MANIFEST, V3.MANIFEST, W.MEMBER_ACCEPTANCE_PRODUCERS = saved


def _tests_b1(W, V3, bw, consumers):
    # ------------------------------------------------------------------ T45b the P3 reproduction, v003 vs v003a
    pa = build_point(W, bw, 'p3', key(80))
    sp = {rd: [spec_of(pa, 'member', log_index=500, acceptance=make_acceptance(bw, 'p3_%s' % rd, pa, rd))]
          for rd in ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT')}
    d3 = {rd: V3.assemble('phase2_members', list(QIDS), s)[0]['points'][0] for rd, s in sp.items()}
    da = {rd: W.assemble('phase2_members', list(QIDS), s)[0]['points'][0] for rd, s in sp.items()}
    record('T45b MUST_FAIL (B1 P3 reproduced): a c2v004 (DDO154) record reading ACCEPTED or LO_UNCERTIFIED_TRANSIENT, '
           'bound to a COMPLETED valid NGC call: v003 (dd9456bc) gives member_valid true, v003a gives false with the '
           'producer gap; the reading is printed; speeds, valid, eps and result_pin equal between the two',
           all(d3[rd]['member_valid'] is True and da[rd]['member_valid'] is False
               and da[rd].get('member_valid_basis') == [gap(W)] and da[rd]['acceptance']['reading'] == rd
               and all(da[rd][k] == d3[rd][k] for k in ('speeds_km_s', 'valid', 'eps_km_s', 'result_pin', 'theta_key',
                                                        'log_index', 'call'))
               for rd in sp), repr({rd: (d3[rd]['member_valid'], da[rd]['member_valid']) for rd in sp}))
    fwd = make_acceptance(bw, 'p3_route', pa, 'ACCEPTED', over=lambda r: dict(r, route=G5_ROUTE))
    pr = W.assemble('phase2_members', list(QIDS), [spec_of(pa, 'member', log_index=500, acceptance=fwd)])[0]['points'][0]
    record('T45b a c2v004 record that carries the G5 route string in an added field still does not count (the producer '
           'pin decides, not a string in the record)', pr['member_valid'] is False and pr.get('member_valid_basis') == [gap(W)])
    # ------------------------------------------------------------------ T45c a G5 / A153-shaped NGC record is refused
    for name, over, code in (
            ('NGC-shaped record schema (synthetic), route G5, unpinned handoff',
             lambda r: dict(r, schema='NGC_POINT_LO_ACCEPTANCE_RECORD_SYNTHETIC_TEST_ONLY', route=G5_ROUTE,
                            handoff={'path': '/synthetic/ngc_handoff.py', 'sha256': '2' * 64}), 'ACCEPTANCE_SCHEMA'),
            ('c2v004 schema with route G5 from an unpinned handoff',
             lambda r: dict(r, route=G5_ROUTE, handoff={'path': '/synthetic/ngc_handoff.py', 'sha256': '2' * 64}),
             'ACCEPTANCE_PRODUCER_NOT_REVIEWED')):
        ap = make_acceptance(bw, uniq('g5'), pa, over=over)
        expect_refused(W, 'T45c MUST_FAIL (fail-closed until the successor pins it): ' + name, code,
                       lambda ap=ap: W.assemble('phase2_members', list(QIDS),
                                                [spec_of(pa, 'member', log_index=501, acceptance=ap)]))
    # ------------------------------------------------------------------ T45d Phase-1 unaffected
    roles = ['u_A', 'F0', 'F1', 'F2']
    pts = {r_: build_point(W, bw, 'q1_%s' % r_, key(81 + i), cert=make_cert(bw / ('q1_%s' % r_), r_, key(81 + i),
                                                                           scale=1.0 + 0.2 * i))
           for i, r_ in enumerate(roles)}
    specs = [spec_of(pts[r_], r_, acceptance=make_acceptance(bw, 'q1_%s' % r_, pts[r_],
                                                             'ACCEPTED' if r_ != 'F1' else 'INCOMPLETE')) for r_ in roles]
    (doc3, rec3), (doca, reca) = V3.assemble('phase1_values', list(QIDS), specs), W.assemble('phase1_values', list(QIDS), specs)
    same = all(x[k] == y[k] for x, y in zip(doc3['points'], doca['points'])
               for k in ('role', 'theta_key', 'speeds_km_s', 'valid', 'result_pin', 'call', 'eps_km_s'))
    acc_ok = all({k: v for k, v in y['acceptance'].items() if k not in ('counts_for_member_valid', 'g5_producer', 'basis')}
                 == {k: v for k, v in x['acceptance'].items() if k != 'counts_for_member_valid'}
                 and y['acceptance']['counts_for_member_valid'] is False and y['acceptance'].get('basis') == gap(W)
                 and 'member_valid' not in y and 'member_valid_basis' not in y
                 for x, y in zip(doc3['points'], doca['points']))
    recs_ok = all({k: v for k, v in a_.items() if k not in ('module', 'producer')} == {k: v for k, v in b_.items()
                                                                                     if k not in ('module', 'producer')}
                  for a_, b_ in zip(rec3, reca))
    okc = []
    for name, P in (('v003', consumers.get('v003')), ('v003a', consumers.get('v003a'))):
        if P is not None:
            P.check_values(doca, {'u_A': {'log_index': 0}, 'members': [{'key': pts['u_A']['key'], 'log_index': 0}],
                                  'F': [{'role': r_, 'key': pts[r_]['key']} for r_ in roles[1:]]})
            okc.append(name)
    record('T45d Phase-1 unaffected: v003a and v003 give equal role, theta_key, speeds, valid, result_pin, call and eps '
           'on every point, equal point records apart from module/producer, and equal printed acceptance apart from '
           'counts_for_member_valid (now false) and the added g5_producer/basis; no member_valid on Phase-1 points; '
           'phase1 check_values accepts (%s); no members gate on a Phase-1 document' % '+'.join(okc),
           same and acc_ok and recs_ok and len(okc) == 2 and 'member_valid_gate' not in doca['assembly']
           and doca['assembly']['module'] == 'values_writer_c2v003a')
    # ------------------------------------------------------------------ T45e W-3 truth table with a test-only producer pin
    cases = []
    for i, rd in enumerate(('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT', 'INCOMPLETE', 'NON_LAPSE_TAIL_MATERIAL',
                            'ACCEPTED_PASS_FLAGGED', 'BOUND_INSUFFICIENT', 'UNDECIDABLE_FLAGGED', None)):
        q = build_point(W, bw, 'tt_%d' % i, key(90 + i))
        cases.append(('reading %s' % rd, spec_of(q, 'member', log_index=600 + i,
                                                 acceptance=make_acceptance(bw, 'tt_%d' % i, q, rd) if rd else None),
                      rd in ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT'),
                      [] if rd in ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT') else
                      ['NO_ACCEPTANCE_RECORD'] if rd is None else ['ACCEPTANCE_READING_NOT_ACCEPTED_OR_TRANSIENT: %s' % rd]))
    ci = build_point(W, bw, 'tt_colfail', key(98), hooks={'result': lambda r: dict(
        r, valid=False, status='COMPLETED_INVALID', reasons=['final pass column failures or nonpositive rotation'])})
    cases.append(('COMPLETED_INVALID + ACCEPTED', spec_of(ci, 'member', log_index=610,
                                                          acceptance=make_acceptance(bw, 'tt_colfail', ci, 'ACCEPTED')),
                  False, ['CALL_NOT_VALID', 'STATUS_NOT_COMPLETED: COMPLETED_INVALID']))
    fs = build_point(W, bw, 'tt_failed', key(99), hooks={'result': lambda r: dict(r, status='FAILED')})
    cases.append(('FAILED (valid true) + ACCEPTED', spec_of(fs, 'member', log_index=611,
                                                            acceptance=make_acceptance(bw, 'tt_failed', fs, 'ACCEPTED')),
                  False, ['STATUS_NOT_COMPLETED: FAILED']))
    nc = build_point(W, bw, 'tt_nocert', key(100))
    cases.append(('uncertified member + ACCEPTED', spec_of(nc, 'member', log_index=612, certificate=None, tail=None,
                                                           acceptance=make_acceptance(bw, 'tt_nocert', nc, 'ACCEPTED')),
                  True, []))
    specs_tt = [c[1] for c in cases]
    v3_mv = {x['log_index']: x['member_valid'] for x in V3.assemble('phase2_members', list(QIDS), specs_tt)[0]['points']}
    W.MEMBER_ACCEPTANCE_PRODUCERS = ((W.ACCEPTANCE_SCHEMAS[0], W.ACCEPTANCE_HANDOFFS[0]),)     # TEST ONLY, in-process
    try:
        tdoc = W.assemble('phase2_members', list(QIDS), specs_tt)[0]
    finally:
        W.MEMBER_ACCEPTANCE_PRODUCERS = ()
    got = {x['log_index']: x for x in tdoc['points']}
    bad = [n for n, s, want, b in cases if got[s['log_index']]['member_valid'] is not want
           or got[s['log_index']].get('member_valid_basis') != b or v3_mv[s['log_index']] is not want]
    record('T45e W-3 truth table kept for the successor (test-only in-process pin of a producer pair): ACCEPTED and '
           'LO_UNCERTIFIED_TRANSIENT true; the 5 other readings and no record false; COMPLETED_INVALID and FAILED false; '
           'uncertified member true; basis per conjunct; equal to v003 member_valid on the same inputs; gate printed',
           not bad and (tdoc['assembly'].get('member_valid_gate') or {}).get('producers') == [[W.ACCEPTANCE_SCHEMAS[0], W.ACCEPTANCE_HANDOFFS[0]]]
           and (tdoc['assembly'].get('member_valid_gate') or {}).get('basis', 0) is None
           and got[600]['acceptance'].get('basis', 0) is None
           and got[600]['acceptance'].get('g5_producer') is True, repr(bad))
    W.MEMBER_ACCEPTANCE_PRODUCERS = (('NGC_POINT_LO_ACCEPTANCE_RECORD_SYNTHETIC_TEST_ONLY', W.ACCEPTANCE_HANDOFFS[0]),)
    try:
        t2 = W.assemble('phase2_members', list(QIDS), specs_tt[:1])[0]['points'][0]
    finally:
        W.MEMBER_ACCEPTANCE_PRODUCERS = ()
    record('T45e the producer pin is the (schema, handoff sha) pair: a pin with the c2v004 handoff sha but another schema '
           'does not admit the c2v004 record', t2['member_valid'] is False and t2.get('member_valid_basis') == [gap(W)])
    after = W.assemble('phase2_members', list(QIDS), specs_tt[:1])[0]['points'][0]
    record('T45e after the test-only pin is removed, the same ACCEPTED member reads false again',
           after['member_valid'] is False and getattr(W, 'MEMBER_ACCEPTANCE_PRODUCERS', None) == ())


def tests_evidence(W, consumers):
    dl = Path(DRIVER[0]).read_text().splitlines()
    hb = Path(HANDOFF[0]).read_bytes()
    hl = hb.decode().splitlines()
    ev = {
        'driver L6135-6136 call finish.json: status, valid, result_path, result_sha256 (L9101 strict clone)':
        "_write_x(out / 'finish.json', {'status': status, 'valid': result['valid'], 'result_path': str(out / 'result.json')," in dl[6134]
        and "'result_sha256': rsha" in dl[6135] and "'result_sha256': rsha" in dl[9100],
        'driver L6099 status COMPLETED iff valid, else COMPLETED_INVALID (L9058 strict clone)':
        "status = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'" in dl[6098]
        and "status = 'COMPLETED' if result['valid'] else 'COMPLETED_INVALID'" in dl[9057],
        'driver L6101-6114 the other statuses (REFUSED, BLOCKED, ROUTE_A_NO_FIXED_POINT, FAILED_AT_STAGE, FAILED)':
        all("status = '%s'" % s in dl[n - 1] for s, n in (('REFUSED', 6101), ('BLOCKED', 6104), ('ROUTE_A_NO_FIXED_POINT', 6107),
                                                          ('FAILED_AT_STAGE', 6110), ('FAILED', 6114)))
        and set(W.CALL_STATUSES) == {'COMPLETED', 'COMPLETED_INVALID', 'REFUSED', 'BLOCKED', 'ROUTE_A_NO_FIXED_POINT',
                                     'FAILED_AT_STAGE', 'FAILED'},
        'driver L6073-6074 result.rows = final rows; result.speeds_km_s = {id: speed}':
        "result['rows'] = final['rows']" in dl[6072]
        and "result['speeds_km_s'] = {r['id']: r['speed_km_s'] for r in final['rows']}" in dl[6073],
        'driver L5939 passes[-1].rotation_positive = rotation finish positive_rotation_square':
        "pass_rec.update(rotation_positive=rfj['positive_rotation_square']" in dl[5938],
        'driver L6082 result.valid needs rotation_positive is True':
        "result['valid'] = (not final['column_failures']) and final.get('rotation_positive') is True" in dl[6081],
        'driver L183 KPC_M and L5215 radius_m = float(Rad_text) * KPC_M':
        dl[182].startswith('KPC_M = 3.085677581491367e19') and W.KPC_M == 3.085677581491367e19
        and "float(r['Rad_text'])*KPC_M" in dl[5214],
        'driver NGC_DATA manifest pin a2936517 == W.MANIFEST':
        "'manifest': (C1 / 'NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json', 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494')"
        in dl[4296] and W.MANIFEST['sha256'] == 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494',
        'acceptance handoff c2v004 sha 5ff464cc (A151) == W.ACCEPTANCE_HANDOFFS':
        sha_bytes(hb) == HANDOFF[1] and W.ACCEPTANCE_HANDOFFS == (HANDOFF[1],),
        'handoff L50 RECORD_SCHEMA == W.ACCEPTANCE_SCHEMAS':
        "RECORD_SCHEMA = 'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001'" in hl[49] and W.ACCEPTANCE_SCHEMAS == (
            'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001',),
        'handoff L78-85 READINGS == W.ACCEPTANCE_READINGS':
        all(("'%s'" % rd) in hl[77 + i] for i, rd in enumerate(('NON_LAPSE_TAIL_MATERIAL', 'BOUND_INSUFFICIENT',
                                                               'UNDECIDABLE_FLAGGED', 'LO_UNCERTIFIED_TRANSIENT')))
        and "'INCOMPLETE'" in hl[82] and "'ACCEPTED_PASS_FLAGGED'" in hl[83] and "'ACCEPTED')" in hl[84]
        and W.ACCEPTANCE_READINGS == ('NON_LAPSE_TAIL_MATERIAL', 'BOUND_INSUFFICIENT', 'UNDECIDABLE_FLAGGED',
                                      'LO_UNCERTIFIED_TRANSIENT', 'INCOMPLETE', 'ACCEPTED_PASS_FLAGGED', 'ACCEPTED'),
        'handoff L344-345 record call_dir and handoff pin; L368-369 record result = resolved out/result.json pin':
        "rec = {'schema': RECORD_SCHEMA, 'call_dir': str(call)" in hl[343] and "'handoff': {'path': str(Path(__file__).resolve())" in hl[344]
        and "result_ref = {'path': str((out / 'result.json').resolve()), 'sha256': hashlib.sha256(result_raw).hexdigest()}" in hl[367]
        and "rec['result'] = result_ref" in hl[368],
        'W-3 member readings exactly ACCEPTED and LO_UNCERTIFIED_TRANSIENT':
        W.MEMBER_ACCEPTANCE_READINGS == ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT'),
    }
    for k_, v_ in ev.items():
        record('T43 evidence: ' + k_, v_)
    p3, p3a = PHASE1_V003[0], PHASE1_V003A[0]
    have_a = Path(p3a).is_file()
    record('T44 consumer: check_values, members_values, check_member_eps and band_rows AST-identical in phase1_c2v003 '
           '(149ed4cb) and phase1_c2v003a (385b287c); member_eps differs (A149 item 1, expected)',
           have_a and sha_bytes(Path(p3a).read_bytes()) == PHASE1_V003A[1]
           and all(fdump(p3, f) is not None and fdump(p3, f) == fdump(p3a, f)
                   for f in ('check_values', 'members_values', 'check_member_eps', 'band_rows'))
           and fdump(p3, 'member_eps') != fdump(p3a, 'member_eps') and 'v003a' in consumers)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--module', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--results', default=None)
    a = ap.parse_args()
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=False)
    W = load(os.path.abspath(a.module), 'vw3_under_test')
    consumers = {}
    try:
        consumers['v003'] = load(PHASE1_V003[0], 'vw3_phase1_c2v003') if sha_bytes(
            Path(PHASE1_V003[0]).read_bytes()) == PHASE1_V003[1] else None
        if Path(PHASE1_V003A[0]).is_file() and sha_bytes(Path(PHASE1_V003A[0]).read_bytes()) == PHASE1_V003A[1]:
            consumers['v003a'] = load(PHASE1_V003A[0], 'vw3_phase1_c2v003a')
        tests_v002(W, work / 'v002', consumers)
        tests_ruling(W, work)
        tests_assemble(W, work, consumers)
        tests_b1(W, work, consumers)
        tests_evidence(W, consumers)
    except Exception as exc:     # noqa: BLE001
        import traceback
        record('SUITE CRASH', False, '%s: %s | %s' % (type(exc).__name__, exc, traceback.format_exc()[-600:]))
    n_ok = sum(r['ok'] for r in RESULTS)
    summary = {'module': os.path.abspath(a.module), 'module_sha256': sha_bytes(Path(a.module).read_bytes()),
               'test_file_sha256': sha_bytes(Path(__file__).read_bytes()), 'python': sys.version.split()[0],
               'numpy': np.__version__, 'flags_isolated': sys.flags.isolated, 'flags_dont_write_bytecode':
               sys.flags.dont_write_bytecode, 'consumers': sorted(consumers), 'n': len(RESULTS), 'passed': n_ok,
               'results': RESULTS}
    rp = Path(a.results) if a.results else work / 'RESULTS_TEST_VALUES_WRITER_C2V003A.json'
    with open(rp, 'xb') as f:
        f.write(json.dumps(summary, indent=1).encode())
    for r in RESULTS:
        if not r['ok']:
            print('FAIL', r['test'], '|', r['detail'])
    print('%d/%d passed; results %s' % (n_ok, len(RESULTS), rp))
    return 0 if n_ok == len(RESULTS) else 1


if __name__ == '__main__':
    sys.exit(main())
