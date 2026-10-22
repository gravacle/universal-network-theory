"""G2 deciding test (ks_k3_chain_c2 G-wave c2v001; wave-1 README section 7 G2; root A175): do library 2026f2b6's
field_bound and srb_rot work on a K=3 TailState with an EPS certificate on [3,182]?

  python3 -I -B g2_deciding_test_c2v001.py --out-dir DIR      (DIR must not exist; it is created)

SYNTHETIC only: a synthetic two-term source roster (kind 'synthetic', I1-T NOT_APPLICABLE_SYNTHETIC) is built by the
library's own build() at the le_rotation stage with the kept region kept_region('le_rotation', {'shape': 'cube'},
3/KPC_M) (a mask stage takes the cube K: the S1_UA_C3T final-rotation state), outer cylinder K_big 128, coarse synthetic
quadrature. Then field_bound and srb_rot run with synthetic EPS certificates over [3,182] (the KS2 / G2 coverage) and over
[4,182] (the 08e9ac0a coverage). Library 2026f2b6 and its pinned jn provider d6c55b55 are loaded by path and sha. Nothing
else is read; the only write is the result JSON (exclusive create). Labels: TESTED = shown here.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

import numpy as np

MOD = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/module'
LIB = (MOD + '/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')
PROVIDER = (MOD + '/posix_libm_bessel_jn_provider_c2v001.py', 'd6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171')


def load(path, sha, name):
    with open(path, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise SystemExit('PIN MISMATCH ' + path)
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, path, 'exec'), m.__dict__)
    return m


class SyntheticRoster:
    """Two smooth synthetic source terms (not a galaxy): P(kp) = J0(kp R_j), F(kz) = exp(-(kz h_j)^2). kind 'synthetic'."""
    kind = 'synthetic'
    gas = None
    stars = None

    def __init__(self, kpc):
        self.R = np.array([0.05, 0.15]) * kpc
        self.h = np.array([0.02, 0.04]) * kpc
        self.amp = np.array([1.0e30, 5.0e29])

    def extent(self):
        return {'R_src_max_m': float(self.R.max()), 'gas_z_abs_max_m': float(self.h.max()), 'stars_24h_m': 0.0}

    def radial_factors(self, kp, j0):
        return np.stack([a * j0(np.asarray(kp) * r) for a, r in zip(self.amp, self.R)], axis=1)

    def vertical_factors(self, kz, c_m_s):
        return np.stack([np.exp(-(np.asarray(kz) * h) ** 2) + 0j for h in self.h], axis=1)

    def record(self):
        return {'kind': 'synthetic', 'R_m': self.R.tolist(), 'h_m': self.h.tolist(), 'amp': self.amp.tolist()}

    def digest(self):
        return hashlib.sha256(json.dumps(self.record(), sort_keys=True).encode()).hexdigest()


def eps_cert(lo, hi, eps=1.0e-6):
    return {'shells': [{'lo_inverse_kpc': float(n), 'hi_inverse_kpc': float(n + 1), 'eps': eps} for n in range(lo, hi)]}


def outcome(fn):
    try:
        return 'PASS', fn()
    except Exception as exc:
        return '%s: %s' % (type(exc).__name__, exc), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', required=True)
    a = ap.parse_args()
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        raise SystemExit('REFUSED: python3 -I -B required')
    out = os.path.abspath(a.out_dir)
    os.mkdir(out)
    t0 = time.time()
    U = load(LIB[0], LIB[1], 'g2d_uvt_lapse_v002')
    PV = load(PROVIDER[0], PROVIDER[1], 'g2d_jn_provider')
    jn = PV.create_provider()
    raw = {'enabled': True, 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 128.0}, 'source_rule': 'continuum_v001',
           'gas': {'interp': 'lagrange3_s_gl4', 'M_s': 8},
           'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'},
           'quadrature': {'order': 4, 'w_perp_max_inverse_kpc': 2.0, 'w_z_max_inverse_kpc': 2.0},
           'domain': {'R_eval_max_kpc': 0.2, 'z_eval_max_kpc': 0.2, 'z_src_max_kpc': 0.2},
           'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True, 'jet_order': {'route_a': 1, 'route_b': 1, 'ngc_eval': 1},
           'lambda_scale': 1.0, 'eps_certificate': U.TEST_ONLY_CERT, 'lo_certificate': U.TEST_ONLY_CERT}
    config = U.normalize_config(raw)
    res = {'schema': 'KS_GWAVE_G2_DECIDING_TEST_C2V001', 'library': {'path': LIB[0], 'sha256': LIB[1]},
           'provider': {'path': PROVIDER[0], 'sha256': PROVIDER[1]}, 'synthetic_config': raw, 'cases': {}}
    states = {}
    for K in (3, 4):
        kept = U.kept_region('le_rotation', {'shape': 'cube'}, K / U.KPC_M)
        st = U.build(config=config, kept=kept, roster=SyntheticRoster(U.KPC_M), gamma_eff=2.0e-17, c_m_s=299792458.0,
                     eval_radii_m=[0.1 * U.KPC_M], jn_provider=jn, i1t={'verdict': 'NOT_APPLICABLE_SYNTHETIC'},
                     stage_kind='le_rotation')
        states[K] = st
        e = st._a['shell_edges_inverse_kpc']
        si = st._a['shell_integrals']
        res['cases']['state_K%d' % K] = {'kept': kept, 'empty': bool(st.empty), 'shell_edge_first': float(e[0]),
                                         'shell_edge_last': float(e[-1]), 'n_shells': int(len(e) - 1),
                                         'first_shell_B1_nonzero': bool(si[0, 1] != 0),
                                         'N_perp': st.record['quadrature']['N_perp'], 'N_z_plus': st.record['quadrature']['N_z_plus']}
    st3 = states[3]
    rows = {'column_R_m': [0.05 * U.KPC_M, 0.1 * U.KPC_M], 'v_c_m_s': [3.0e4, 4.0e4], 'row_columns': [[0], [0, 1]],
            'N_min': 1.0, 'tau_km_s': [1.0, 1.0]}
    for tag, (lo, hi) in (('eps_3_182', (3, 182)), ('eps_4_182', (4, 182))):
        cert = eps_cert(lo, hi)
        fb = outcome(lambda: U.field_bound(st3, cert))
        sr = outcome(lambda: U.srb_rot(st3, cert, rows))
        res['cases']['K3_state_' + tag] = {
            'field_bound': fb[0], 'srb_rot': sr[0],
            'field_bound_eps_first_shell': None if fb[1] is None else fb[1]['eps'][0],
            'field_bound_total_B1': None if fb[1] is None else fb[1]['total'][1],
            'srb_rot_bound_km_s': None if sr[1] is None else sr[1]['bound_km_s'],
            'srb_rot_pass_tau_over_10': None if sr[1] is None else sr[1]['pass_tau_over_10']}
    # The K=4 state with the [4,182] certificate (08e9ac0a's case) for contrast.
    fb4 = outcome(lambda: U.field_bound(states[4], eps_cert(4, 182)))
    res['cases']['K4_state_eps_4_182'] = {'field_bound': fb4[0]}
    c = res['cases']
    deciding = (c['state_K3']['shell_edge_first'] == 3.0 and c['state_K3']['first_shell_B1_nonzero']
                and c['K3_state_eps_3_182']['field_bound'] == 'PASS' and c['K3_state_eps_3_182']['srb_rot'] == 'PASS'
                and 'UV_TAIL_EPS_COVERAGE' in c['K3_state_eps_4_182']['field_bound']
                and 'UV_TAIL_EPS_COVERAGE' in c['K3_state_eps_4_182']['srb_rot']
                and c['state_K4']['shell_edge_first'] == 4.0 and c['K4_state_eps_4_182']['field_bound'] == 'PASS')
    res['result'] = ('TESTED: library 2026f2b6 field_bound/srb_rot WORK at shells from 3: a K=3 le_rotation TailState has '
                     'unit shell edges from min(K) = 3 with a nonzero [3,4) shell; both run with an EPS certificate on '
                     '[3,182]; with one on [4,182] (08e9ac0a EPS_COVERAGE) both refuse UV_TAIL_EPS_COVERAGE at [3,4). '
                     'The library needs no change; the SRB adapter needs the kept-K coverage (and KS1, the G6c enumerator).'
                     if deciding else 'UNEXPECTED: see cases')
    res['deciding_test_passed'] = bool(deciding)
    res['seconds'] = round(time.time() - t0, 2)
    res['python'] = sys.version.split()[0]
    res['numpy'] = np.__version__
    with open(os.path.join(out, 'G2_DECIDING_TEST_C2V001.json'), 'xb') as f:
        f.write(json.dumps(res, sort_keys=True, indent=1, default=str).encode() + b'\n')
    print(json.dumps({'deciding_test_passed': res['deciding_test_passed'], 'cases': res['cases']}, indent=1, default=str))
    return 0 if deciding else 1


if __name__ == '__main__':
    sys.exit(main())
