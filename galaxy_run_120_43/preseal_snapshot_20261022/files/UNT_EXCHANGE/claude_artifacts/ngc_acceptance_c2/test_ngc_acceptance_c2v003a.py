"""Synthetic suite for NGC acceptance c2v003a = c2v003 + A167 (the adapter c2v003a: C4b on the spec route, the theta
route a diagnostic; Claude3 NGC rho c3v003 schema strings *_C3V003; the handoff c2v003a pins it). Every c2v003 test is
ported; F06 and P20 follow A167; P35 and F42 are the A167 additions. The c2v003 suite text follows.

Synthetic suite for NGC acceptance c2v003 (V006 A162 items 1-6 on A153 + A155): the route-A iterate reader, the S5
rebuild-export tool, the NGC row contract and its builder, the handoff c2v003 (execution facts, SRB-ROT report-only, S2
pins), and the unchanged adapter c2v002 and enumerator c2v001. Every c2v002 test is ported (P01-P24, F01-F33); P25-P34
and F34-F41 are the A162 additions.

SYNTHETIC ONLY. Every call, state, roster, sidecar, rho record, slot proof, certificate, S0 point, spec, manifest,
addendum and recipe is fabricated under a SYNTHETIC_TEST registry (refused at every registered input). The states are
built by the pinned library owned_uv_tail_lapse_v002 (2026f2b6) build() from synthetic rosters (a test-only recipe file),
so that the S5 tool can rebuild them from their own rosters. The REGISTERED-registry tests run the public entries on a
fabricated call whose result names the registered driver sha as a string and whose spec label carries no theta key: they
pass the root gate on the real V006 A153 and A155 sections and the text of record and stop at S1 point custody. The real
files read: the V006 A153/A155/A162 sections, the text of record, the target-free query manifest a2936517 (ids and radii
only, for the contract tests) and the built contract NGC_ROW_CONTRACT_C2V001.json. No other NGC3198-named file is opened.

Usage: python3 -I -B test_ngc_acceptance_c2v003a.py --run-dir <new dir> [--module-dir <dir>]
Writes SUITE_RESULTS_C2V003A.json in the run dir (exclusive create). Exit 0 iff every MUST_PASS passes and every MUST_FAIL
fails closed.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import math
import os
import random
import sys
import time
import traceback

KPC_M = 3.085677581491367e19
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
NAMES = {'E': 'ngc_consumed_states_c2v001.py', 'A': 'ngc_lo_state_adapter_c2v003a.py', 'H': 'ngc_acceptance_handoff_c2v003a.py',
         'R': 'ngc_route_a_iterates_c2v003.py', 'S': 'ngc_s5_rebuild_export_c2v003.py', 'C': 'ngc_row_contract_c2v003.py'}
CONTRACT_FILE = 'NGC_ROW_CONTRACT_C2V001.json'
ROW_PRODUCER = (ART + '/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py',
                '67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e')
REAL_DRIVER_SHA = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'
CERT_PRODUCER = '8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235'   # named as a string (A148)
A155_PIN = {'heading': '## A155', 'section_sha256': 'ed6b144b66837069c4febf81a4feaf11c160f9be5f26d914d4c40041b60f3c9d'}
SIDECAR_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_SIDECAR_C2V001'
ROUTE_A_RECORD_SCHEMA = 'UNT_UV_TAIL_ROUTE_A_RECORD_C2V001'
CONV = 'CONVERGED_FINITE_FIXED_POINT'
CURRENT = 'current_begin_inferred_from_completion'
NEXT = 'next_built_and_monitor_consumed'
N = 43
IDS = ['SYNQ-%02d' % (i + 1) for i in range(N)]
RAD_TEXT = ['%.3f' % (1.0 + 0.8 * i) for i in range(N)]
R_M = [float(x) * KPC_M for x in RAD_TEXT]
BASE_V = [100.0 + 2.0 * i for i in range(N)]
RHO_USED = [0.5, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05, 0.02]
PARTITION = [[2.0, 3.0], [3.0, 4.0], [4.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
             [64.0, 91.0]]
EVAL_R = [0.05 * KPC_M]
TARGET_MAX_G = 0.001
STATES = 'ABIN'          # A accepted route A (iteration 1), B route-B le3_rotation, I iterate 0, N monitor next of iteration 1

SYN_RECIPE_SRC = r'''"""Synthetic S5 roster recipe (TEST ONLY; NGC acceptance c2v003 suite). It rebuilds a synthetic state's roster from
the synthetic call's own outputs: a route-A state from the sidecar element rosters (controller semantics: iteration n
current = elements[:n], monitor next = elements[:n+1]), a route-B stage state from its stage's synthetic_roster.json."""
import hashlib
import json
import os
import numpy as np

KPC_M = 3.085677581491367e19
NEXT = 'next_built_and_monitor_consumed'


def _canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _adig(a):
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest()


class SynRoster:
    kind = 'registered'
    gas = None
    stars = None

    def __init__(self, scale, rec):
        self.scale = float(scale)
        self.rec = dict(rec, scale_hex=float(scale).hex())

    def extent(self):
        return {'R_src_max_m': 0.05 * KPC_M, 'gas_z_abs_max_m': 0.01 * KPC_M, 'stars_24h_m': 0.02 * KPC_M}

    def radial_factors(self, k, j0):
        return np.full((len(k), 1), self.scale)

    def vertical_factors(self, kz, c):
        return np.full((len(kz), 1), 1.0 + 0.5j)

    def record(self):
        return dict(self.rec)

    def digest(self):
        return hashlib.sha256(_canon(self.rec).encode()).hexdigest()


def route_a_roster(base_hex, elements):
    s = float.fromhex(base_hex)
    for e in elements:
        s = s + float(np.sum(e['integrated_J']))
    return SynRoster(s, {'kind': 'synthetic_route_a', 'base_hex': base_hex,
                         'elements': [[_adig(e['positions_m']), _adig(e['integrated_J'])] for e in elements]})


def stage_roster(spec):
    return SynRoster(float.fromhex(spec['scale_hex']), {'kind': 'synthetic_stage', 'label': spec['label']})


def roster_for_state(*, call_dir, out_dir, result, target, lib, provider):
    with open(os.path.join(out_dir, 'inputs', 'synthetic_build_inputs.json')) as f:
        inp = json.load(f)
    og = target['origin']
    if og['kind'] == 'ROUTE_A_ITERATE':
        sdir = result['uv_tail']['route_a_record']['sidecar']['directory']
        with open(os.path.join(sdir, 'iteration_%04d.json' % og['iteration'])) as f:
            p = json.load(f)['payload']
        n = og['iteration'] + (1 if og['role'] == NEXT else 0)
        els = []
        for m in range(n):
            with np.load(os.path.join(sdir, 'elements_%04d.npz' % m), allow_pickle=False) as z:
                els.append({'positions_m': z['positions_m'].copy(), 'integrated_J': z['integrated_J'].copy()})
        roster = route_a_roster(inp['route_a_base_scale_hex'], els)
        i1t = p['next_i1t'] if og['role'] == NEXT else p['i1t']
        kind = 'route_a'
    else:
        rec = [r for r in result['stage_records'] if r.get('name') == og['stage']][0]
        d = rec['argv'][rec['argv'].index('--outdir') + 1]
        with open(os.path.join(d, 'synthetic_roster.json')) as f:
            roster = stage_roster(json.load(f))
        with open(os.path.join(d, 'finish.json')) as f:
            u = json.load(f)['uv_tail']
        i1t, kind = u['i1t'], u['stage_kind']
    ph = result['normalized_spec']['physical']
    return {'roster': roster, 'build': {'config': inp['config'], 'kept': inp['kept'],
                                        'gamma_eff': ph['common_scale_s'] * ph['gamma'], 'c_m_s': inp['c_m_s'],
                                        'eval_radii_m': inp['eval_radii_m'], 'i1t': i1t, 'stage_kind': kind},
            'provenance': {'recipe': 'synthetic (test only)', 'origin': og}}
'''

RAISING_RECIPE_SRC = ('"""Synthetic recipe that raises (TEST ONLY)."""\n\n\ndef roster_for_state(**kw):\n'
                      '    raise RuntimeError("synthetic recipe failure")\n')


def oracle_g(v_km_s, R_m, rho, b1, c, theta):
    """Independent A155 TI_B_SCALE_R_V001 ratio form for one row and shell (plain Python floats)."""
    return (abs(v_km_s) * 1000.0) ** 2 * R_m * rho * b1 / (2.0 * c * c * theta)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(path, name):
    with open(path, 'rb') as f:
        raw = f.read()
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def put_bytes(path, raw):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}


def put_json(path, obj):
    return put_bytes(path, (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode())


def npz_bytes(**arrays):
    import numpy as np
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    return buf.getvalue()


def put_npz(path, arrays):
    return put_bytes(path, npz_bytes(**arrays))


def adig(a):
    import numpy as np
    a = np.ascontiguousarray(a)
    h = hashlib.sha256()
    h.update(('%s|%s|' % (a.dtype.str, a.shape)).encode())
    h.update(a.tobytes())
    return h.hexdigest()


def read_json(pin):
    with open(pin['path'], 'rb') as f:
        return json.loads(f.read())


def load_npz(path):
    import numpy as np
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k].copy() for k in z.files}


def floats_outside_flags(obj, path=''):
    """S12 check: every non-integer number outside a coverage_flags block."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k != 'coverage_flags':
                out += floats_outside_flags(v, path + '/' + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += floats_outside_flags(v, '%s[%d]' % (path, i))
    elif isinstance(obj, float):
        out.append(path)
    return out


class Fx:
    """Fixture factory: one synthetic registry per run; one synthetic call per make_call()."""

    def __init__(self, root, A, E, H, U, R, S, PV):
        import numpy as np
        self.np, self.root, self.A, self.E, self.H, self.U, self.R, self.S, self.PV = np, root, A, E, H, U, R, S, PV
        reg = os.path.join(root, 'registry')
        self.reg = reg
        v006 = '\n'.join(['# synthetic addendum (test only; not a root decision)', '', '## A152: synthetic', '', 'x', '',
                          '## A153: synthetic A153 (test only)', '', '- ' + A.SCOPE_DISCLOSURE, '',
                          '## A999: synthetic t_i entry (test only)', '',
                          'synthetic declared rule %s, theta hex %s.' % (A.RULE_ID, A.THETA_HEX), '',
                          '**PASS now reads:** "%s"' % A.PASS_MEANING, '',
                          '## A998: synthetic t_i entry without the rule (test only)', '', 'nothing declared here', '',
                          '## A1000: end', '']).encode()
        v_pin = put_bytes(os.path.join(reg, 'syn_addendum.md'), v006)
        a153 = {'path': v_pin['path'], 'heading': '## A153',
                'section_sha256': hashlib.sha256(A.section_bytes(v006, '## A153')).hexdigest()}
        tie = {'path': v_pin['path'], 'heading': '## A999',
               'section_sha256': hashlib.sha256(A.section_bytes(v006, '## A999')).hexdigest()}
        self.tie_without_rule = {'path': v_pin['path'], 'heading': '## A998',
                                 'section_sha256': hashlib.sha256(A.section_bytes(v006, '## A998')).hexdigest()}
        tor = put_bytes(os.path.join(reg, 'syn_text_of_record.md'),
                        ('synthetic text of record\n> "' + A.FAIL_TEXT + '"\n').encode())
        drv = put_bytes(os.path.join(reg, 'syn_driver.py'), b'# synthetic driver (test only)\n')
        self.launch = put_bytes(os.path.join(reg, 'syn_launch_pin.bin'), b'NOT JSON: synthetic launch pin (never parsed)\n')
        man = {'schema': 'SYNTHETIC_TARGET_FREE_MANIFEST', 'rows': [
            {'query_id': q, 'Rad_text': RAD_TEXT[i], 'Rad_unit': 'kpc', 'data_row_index': i, 'source_line_number': i + 1}
            for i, q in enumerate(IDS)]}
        self.manifest = put_json(os.path.join(reg, 'syn_manifest.json'), man)
        rnd = random.Random(20261019)
        while True:                                            # a theta triple whose two gamma routes differ in bits
            s, ge, EB = (rnd.uniform(0.3, 3.0) for _ in range(3))
            if (s * (ge * EB)).hex() != ((s * ge) * EB).hex():
                break
        self.thetas = [
            {'common_scale_s': 2.0, 'gamma_over_Eref': 1.5, 'ell_F_m': 1.0e19, 'Eref_base_J': 3.0, 'distance_Mpc': 13.8},
            {'common_scale_s': s, 'gamma_over_Eref': ge, 'ell_F_m': 1.0e19, 'Eref_base_J': EB, 'distance_Mpc': 13.8},
            {'common_scale_s': 1.0, 'gamma_over_Eref': 1.25, 'ell_F_m': 2.0e19, 'Eref_base_J': 4.0, 'distance_Mpc': 13.8},
            {'common_scale_s': 4.0, 'gamma_over_Eref': 0.5, 'ell_F_m': 3.0e19, 'Eref_base_J': 2.0, 'distance_Mpc': 13.8}]
        self.keys = [A.theta_key(t) for t in self.thetas]
        roles = ('seed', 'jacobian_first_attempt_0', 'jacobian_first_attempt_1', 'jacobian_first_attempt_2')
        s0 = {'schema': 'PHASE1_S0_C2V001', 'module': 'phase1_c2v001', 'points': [
            {'role': r, 'key': k, 'theta_hex': {a: float(b).hex() for a, b in t.items()}, 'theta_natural': t}
            for r, k, t in zip(roles, self.keys, self.thetas)]}
        s0p = put_json(os.path.join(reg, 'syn_s0.json'), s0)
        self.registry = {'kind': 'SYNTHETIC_TEST', 'a153': a153, 'text_of_record': tor, 't_i_entry': tie,
                         'driver': drv, 's0': s0p, 'launch': self.launch, 'manifest': self.manifest}
        self.rule_id = A.RULE_ID
        self.rebuild_producer = put_bytes(os.path.join(reg, 'syn_rebuild_producer.py'), b'# synthetic rebuild exporter\n')
        self.sidecar_reader = put_bytes(os.path.join(reg, 'syn_sidecar_reader.py'), b'# synthetic sidecar reader\n')
        self.slot_proof_producer = put_bytes(os.path.join(reg, 'syn_slot_proof_producer.py'), b'# synthetic slot proof\n')
        self.recipe = put_bytes(os.path.join(reg, 'syn_s5_roster_recipe.py'), SYN_RECIPE_SRC.encode())
        self.raising_recipe = put_bytes(os.path.join(reg, 'syn_s5_raising_recipe.py'), RAISING_RECIPE_SRC.encode())
        self.rc = load(self.recipe['path'], 'suite_syn_recipe')
        self.certs = [self.make_cert(os.path.join(reg, 'syn_eps_cert_p%d.json' % i), self.keys[i]) for i in range(4)]
        self.cfg_cache = {}
        self.n = 0

    # ---------------------------------------------------------------- certificates, config, tail states
    def make_cert(self, path, key, *, scale=1.0, producer=CERT_PRODUCER, role='seed'):
        shells = []
        for k in range(2, 91):
            e = 1.0e-6 * (1.0 + 0.01 * k) * scale
            shells.append({'lo_inverse_kpc': float(k), 'hi_inverse_kpc': float(k + 1), 'eps': e,
                           'flat': {'eps_envelope': 0.5 * e}, 'envelope': {'eps_envelope': 0.9 * e}})
        return put_json(path, {
            'schema': 'UNT_CLAUDE4_S0_POINT_EPS_C4V002', 'mode': 'point', 'point': {'key': key, 'role': role},
            'key_check': {'equals_point_key': True, 'from_theta_hex': key, 'from_theta_natural': key},
            'producer': {'path': '/synthetic/eps_ngc_point_c4v002.py (test only; the sha is named as a string)',
                         'sha256': producer},
            'gate': 'EPS', 'verdict': 'CERTIFIED', 'certificate': True, 'summary': {'rule_verdict': 'CERTIFIED'},
            'coverage_inverse_kpc': {'NGC': [2.0, 91.0]}, 'shells': shells})

    def cfg(self, cert):
        k = cert['sha256']
        if k not in self.cfg_cache:
            raw = {'enabled': True, 'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 32.0}, 'source_rule': 'continuum_v001',
                   'gas': {'interp': 'lagrange3_s_gl4', 'M_s': 4},
                   'stars': {'segment_rule': 'max16_ceil_kdr_plus8', 'tail_rule': 't_panels_40a_phase1p5_gl12'},
                   'quadrature': {'order': 2, 'w_perp_max_inverse_kpc': 4.0, 'w_z_max_inverse_kpc': 4.0},
                   'domain': {'R_eval_max_kpc': 0.1, 'z_eval_max_kpc': 0.1, 'z_src_max_kpc': 0.1},
                   'asymptote': 'EH_exact_minus_quarter', 'lapse_only': True,
                   'jet_order': {'route_a': 1, 'route_b': 1, 'ngc_eval': 1}, 'lambda_scale': 1.0,
                   'eps_certificate': dict(cert), 'lo_certificate': dict(self.launch)}
            self.cfg_cache[k] = self.U.normalize_config(raw)
        return self.cfg_cache[k]

    def b1_unit(self, arrays, record):
        """Independent copy of the node-quadrature B1 (lo_core L118-129 arithmetic), for an edges override."""
        np, U = self.np, self.U
        kp, kz, edges = arrays['kp'], arrays['kz'], arrays['shell_edges_inverse_kpc']
        out = np.zeros(len(edges) - 1)
        S = arrays['P'] @ arrays['F'].T
        c0 = U._c0_D(record['kept'], record['outer'], kp * U.KPC_M, kz * U.KPC_M)
        km = np.sqrt(kp[:, None] ** 2 + kz[None, :] ** 2)
        fac = (record['pref'] * arrays['wkp'] * kp)[:, None] * arrays['wz'][None, :] / km ** 2
        w = 2 * np.abs(S) * fac * c0 * km
        idx = np.clip(np.searchsorted(edges, km * U.KPC_M, side='right') - 1, 0, len(out) - 1)
        out += np.bincount(idx.ravel(), weights=w.ravel(), minlength=len(out))
        return out

    def tail(self, roster, gamma, i1t, kind, cfg, overrides=None, edges=None):
        """A TailState built by the pinned library from a synthetic roster; overrides / edges make it unrebuildable."""
        np = self.np
        st = self.U.build(config=cfg, kept=dict(self.A.KEPT), roster=roster, gamma_eff=gamma, c_m_s=self.A.C_M_S,
                          eval_radii_m=np.asarray(EVAL_R), jn_provider=self.PV.create_provider(), i1t=i1t, stage_kind=kind)
        record = json.loads(json.dumps(st.record))
        arrays = st.to_arrays()
        if edges is not None:
            arrays['shell_edges_inverse_kpc'] = np.asarray(edges, float)
            b1 = self.b1_unit(arrays, record)
            si = np.zeros((len(edges) - 1, 3))
            si[:, 0], si[:, 1], si[:, 2] = 0.5 * b1, b1, 2.0 * b1
            arrays['shell_integrals'] = si
        record.update(overrides or {})
        d = self.U.TailState(empty=False, record=record, arrays=arrays).digest
        if edges is None and not overrides:
            assert d == st.digest
        return record, arrays, d, np.asarray(arrays['shell_integrals'])[:, 1].copy()

    def s4_b1(self, b1, edges=None):
        np = self.np
        e = self.A.expected_unit_edges() if edges is None else np.asarray(edges)
        top = float(e[-1])
        out = []
        for lo, hi in PARTITION:
            if lo >= top:
                out.append(0.0)
            else:
                h = min(hi, top)
                take = (e[:-1] >= lo) & (e[1:] <= h)
                out.append(float(b1[take].sum()))
        return out

    # ---------------------------------------------------------------- one call
    def row_speeds(self, o):
        X = o.get('X') or {}
        zero = set(o.get('zero_speed') or ())
        npass = 3
        rows_by_pass, vmax = [], [None] * N
        for p in range(npass):
            rows = []
            for i, q in enumerate(IDS):
                if q in X:
                    e = X[q].get('earlier')
                    if p == 0 and e is not None:
                        rows.append({'id': q, 'speed_km_s': e, 'valid': True})
                    else:
                        rows.append({'id': q, 'speed_km_s': None, 'valid': False, 'reason': X[q]['reason'],
                                     'radius_m': R_M[i]})
                elif i in zero:
                    rows.append({'id': q, 'speed_km_s': 0.0 if p % 2 == 0 else -0.0, 'valid': True})
                else:
                    v = BASE_V[i] * (1.0 - 0.01 * (npass - 1 - p))
                    if p == 0 and i == 5:
                        v = -(BASE_V[i] + 30.0)
                    rows.append({'id': q, 'speed_km_s': v, 'valid': True})
            for (pp, ii) in o.get('missing_readout') or ():
                if pp == p:
                    rows[ii] = {'id': IDS[ii], 'speed_km_s': None, 'valid': True}
            if o.get('eps_rows'):
                rows = [dict(r, eps_km_s=1.0e-9) for r in rows]
            for i, r in enumerate(rows):
                if isinstance(r.get('speed_km_s'), float):
                    a = abs(r['speed_km_s'])
                    vmax[i] = a if vmax[i] is None or a > vmax[i] else vmax[i]
            rows_by_pass.append(rows)
        return rows_by_pass, vmax, X

    def calibrate(self, gamma, vmax, X, cfg):
        A = self.A
        unit = self.rc.stage_roster({'scale_hex': (1.0).hex(), 'label': 'unit'})
        b1u = self.s4_b1(self.tail(unit, gamma, {'verdict': 'PASS', 'unit': True}, 'le_rotation', cfg)[3])
        vcal = [BASE_V[i] if (IDS[i] in X or vmax[i] is None) else vmax[i] for i in range(N)]
        g_unit = max(oracle_g(vcal[i], R_M[i], RHO_USED[s], b1u[s], A.C_M_S, A.THETA)
                     for i in range(N) for s in range(len(PARTITION)))
        return TARGET_MAX_G / g_unit, b1u

    def make_call(self, name, **o):
        np, A = self.np, self.A
        self.n += 1
        base = os.path.join(self.root, 'calls', name)
        out = os.path.join(base, 'call', 'out')
        point = o.get('point', 0)
        th, key = self.thetas[point], self.keys[point]
        s, ge, EB = th['common_scale_s'], th['gamma_over_Eref'], th['Eref_base_J']
        cert = self.certs[point]
        if o.get('cert_eps_scale') is not None:
            cert = self.make_cert(os.path.join(base, 'cert_scaled.json'), key, scale=o['cert_eps_scale'])
        spec = {'galaxy': 'NGC3198', 'label': 'step5 A_K32_A2_HEADLINE theta_key=' + key,
                'physical': {'Eref_J': EB, 'ell_F_m': th['ell_F_m'], 'gamma': ge * EB, 'common_scale_s': s},
                'numerics': {'uv_tail': {'lo_certificate': dict(self.launch), 'outer': dict(A.OUTER), 'lambda_scale': 1.0,
                                         'eps_certificate': dict(cert)},
                             'route_a': {'column_workers': 1}}}
        spec.update(o.get('spec_overrides') or {})
        spec_ref = put_json(os.path.join(base, 'spec.json'), spec)
        gamma = s * (ge * EB) if o.get('gamma_route') != 'theta' else (s * ge) * EB   # spec route (driver); theta: A167 test
        rows_by_pass, vmax, X = self.row_speeds(o)
        cfg = self.cfg(cert)
        s0, b1u = self.calibrate(gamma, vmax, X, cfg)
        mult = dict({'A': 1.0, 'B': 1.0, 'I': 0.9, 'N': 0.95}, **(o.get('scales') or {}))
        sI, sA, sN, sB = (s0 * mult[k] for k in 'IANB')
        e0 = {'positions_m': np.array([[1.0e19, 0.0, 0.0]]), 'integrated_J': np.array([sA - sI])}
        e1 = {'positions_m': np.array([[2.0e19, 0.0, 0.0]]), 'integrated_J': np.array([sN - sA])}
        base_hex = float(sI).hex()
        ros = {'I': self.rc.route_a_roster(base_hex, []), 'A': self.rc.route_a_roster(base_hex, [e0]),
               'N': self.rc.route_a_roster(base_hex, [e0, e1]),
               'B': self.rc.stage_roster({'scale_hex': float(sB).hex(), 'label': name + '-B'})}
        i1ts = {'I': {'verdict': 'PASS', 'iteration_source': 0, 'synthetic': True},
                'A': {'verdict': 'PASS', 'iteration_source': 1, 'synthetic': True},
                'N': {'verdict': 'PASS', 'iteration_source': 2, 'synthetic': True},
                'B': {'verdict': 'PASS', 'parts': ['synthetic'], 'synthetic': True}}
        kinds = {'A': 'route_a', 'I': 'route_a', 'N': 'route_a', 'B': 'le_rotation'}
        st = {}
        for k in STATES:
            g = gamma + o.get('gamma_ulp', {}).get(k, 0) * math.ulp(gamma)
            st[k] = self.tail(ros[k], g, i1ts[k], kinds[k], cfg, (o.get('record_overrides') or {}).get(k),
                              (o.get('edges') or {}).get(k))
        d = {k: st[k][2] for k in STATES}
        rost = {k: st[k][0].get('roster_digest') for k in STATES}
        sv = o.get('sidecar') or ''
        ev = o.get('exec') or ''
        stages = os.path.join(out, 'stages')
        os.makedirs(os.path.join(out, 'inputs'))
        put_json(os.path.join(out, 'inputs', 'synthetic_build_inputs.json'), {
            'config': cfg, 'kept': dict(A.KEPT), 'c_m_s': A.C_M_S, 'eval_radii_m': list(EVAL_R),
            'route_a_base_scale_hex': base_hex})
        # ---- route A: stage dir, sidecar (controller format)
        ra = os.path.join(stages, '01_route_a')
        att, cpd = os.path.join(ra, 'attempt_000'), os.path.join(ra, 'checkpoint')
        sdir = os.path.join(ra, 'uv_tail_sidecar') if sv != 'outside' else os.path.join(stages, '99_elsewhere', 'uv_tail_sidecar')
        os.makedirs(sdir)
        relax = 0.5
        req_sha = sha_bytes(('synthetic request ' + name).encode())
        cp_id = sha_bytes(('synthetic checkpoint ' + name).encode())
        ident = {'schema': SIDECAR_SCHEMA, 'request_sha256': req_sha, 'config_sha256': cfg['sha256'], 'kept': dict(A.KEPT),
                 'outer': dict(A.OUTER), 'gamma_eff': gamma, 'c_m_s': A.C_M_S, 'relaxation': relax,
                 'checkpoint_identity_sha256': cp_id, 'synthetic': True}
        files = {}

        def side(fname, raw):
            p = put_bytes(os.path.join(sdir, fname), raw)
            files[fname] = p['sha256']
            return p
        side('SIDECAR_IDENTITY.json', canonical({'identity': ident, 'identity_sha256': (
            sha_bytes(canonical(ident)) if sv != 'identity_sha' else '0' * 64)}))
        els, seq, summaries = [e0, e1], ([('I', 'A'), ('A', 'N')] if sv != 'last_current' else [('I', 'A'), ('N', 'N')]), []
        for n, (cur, nxt) in enumerate(seq):
            e = els[n]
            side('elements_%04d.npz' % n, npz_bytes(positions_m=e['positions_m'], integrated_J=e['integrated_J']))
            summ = {'iteration': n, 'state_digest': d[cur], 'next_state_digest': d[nxt], 'M_T': 0.01, 'M_T_rows': [0.01],
                    'M_T_units': 'TAU_UNITS (synthetic)', 'M_K': None, 'M_K_rows': None, 'M_K_units': None,
                    'M_K_status': 'synthetic', 'converged': n == 1, 'i1t_max_rel': 0.0, 'production_admissible': True,
                    'empty': False}
            payload = {'schema': SIDECAR_SCHEMA, 'iteration': n, 'state_digest': d[cur], 'next_state_digest': d[nxt],
                       'i1t': i1ts[cur], 'next_i1t': i1ts[nxt], 'relaxation': relax,
                       'elements': {'file': 'elements_%04d.npz' % n, 'count': 1,
                                    'positions_digest': adig(e['positions_m']) if not (sv == 'elements_digest' and n == 0)
                                    else '0' * 64, 'J_digest': adig(e['integrated_J'])},
                       'summary': summ}
            side('iteration_%04d.json' % n, canonical({'payload': payload, 'diagnostics': {'synthetic': True}}))
            summaries.append(dict(summ, reloaded=True) if (sv == 'reloaded' and n == 0) else summ)
        if sv == 'extra_iteration':
            side('iteration_0002.json', canonical({'payload': {'iteration': 2}}))
        if sv == 'gap':
            files.pop('iteration_0000.json')
        if sv == 'file_bytes':
            files['iteration_0001.json'] = sha_bytes(b'other bytes')
        frec = {'schema': ROUTE_A_RECORD_SCHEMA, 'outcome': CONV, 'request_sha256': req_sha, 'config_sha256': cfg['sha256'],
                'admissibility': 'production', 'kept': dict(A.KEPT), 'outer': dict(A.OUTER),
                'checkpoint_identity_sha256': cp_id, 'boundary_state_digest_at_return': d['A'], 'production_admissible': True,
                'iterations': summaries, 'accepted_iteration': 1, 'M_T_accepted': 0.01, 'M_T_threshold': 0.25,
                'monitor_status': 'M_T_WITHIN_THRESHOLD', 'flags': [], 'E_A_rows_km_s_accepted': None}
        fin_rec = dict(frec, flags=['SYNTHETIC_DIFFERENT']) if sv == 'record_differs' else frec
        fpin = put_bytes(os.path.join(sdir, 'finish_%03d.json' % (1 if sv == 'finish_index' else 0)),
                         canonical({'record': fin_rec, 'files': files}))
        sc = {'directory': sdir, 'finish': fpin if sv != 'finish_sha' else dict(fpin, sha256='0' * 64), 'files': dict(files)}
        rar = {k: frec[k] for k in self.R.COPIED_KEYS}
        rar.update(sidecar=sc, probe_R_m=[R_M[0]], probe_phi_rad=[0.0], probe_source='synthetic')
        if sv == 'boundary':
            rar['boundary_state_digest_at_return'] = d['I']
        if sv == 'outcome':
            rar['outcome'] = 'NO_ACCEPTED_ITERATION'
        ra_argv = ['--seed', 'synthetic', '--seed-sha256', '0' * 64, '--outdir', att, '--checkpoint-directory', cpd,
                   '--start-iteration', '1' if ev == 'start_iter1' else '0', '--uv-tail-config', 'synthetic',
                   '--uv-tail-config-sha256', cfg['sha256'], '--uv-tail-sidecar-directory', sdir]
        if ev == 'resume_flag':
            ra_argv += ['--resume-from', 'x']
        if ev == 'ckpt_resume':
            ra_argv += ['--checkpoint-mode', 'resume']
        # ---- route-A tail manifest stage
        ms = os.path.join(stages, '02_route_a_tail_manifest')
        mdir = os.path.join(ms, 'manifest')
        arr_pin = put_npz(os.path.join(mdir, 'route_a_tail_state.npz'), st['A'][1])
        mpin = put_json(os.path.join(mdir, 'ROUTE_A_TAIL_MANIFEST.json'), {
            'schema': 'UNT_UV_TAIL_ROUTE_A_MANIFEST_C2V001',
            'route_a': {'identity_sha256': cp_id, 'accepted_iteration': 1, 'iteration_start_payload_sha256': '0' * 64},
            'config_sha256': cfg['sha256'], 'state': {'digest': d['A'], 'record': st['A'][0], 'arrays': arr_pin},
            'i1t': i1ts['A']})
        mfin = put_json(os.path.join(mdir, 'finish.json'), {'status': 'ROUTE_A_TAIL_MANIFEST_WRITTEN', 'manifest': mpin['path'],
                                                            'manifest_sha256': mpin['sha256'], 'state_digest': d['A'],
                                                            'empty': False, 'production_admissible': True})
        # ---- reference stage (inherits the accepted state)
        rs = os.path.join(stages, '03_reference')
        rdir = os.path.join(rs, 'reference')
        rfin = put_json(os.path.join(rdir, 'finish.json'), {'uv_tail': {
            'state_digest': d['A'], 'roster_digest': rost['A'], 'stage_kind': 'reference', 'kept': dict(A.KEPT),
            'empty': False, 'config_sha256': cfg['sha256']}})
        # ---- final rotation stage le3_rotation (route-B state B)
        rot_stage = os.path.join(stages, '20_le3_rotation')
        bdir = os.path.join(rot_stage, 'rotation')
        put_json(os.path.join(bdir, 'synthetic_roster.json'), {'scale_hex': float(sB).hex(), 'label': name + '-B'})
        Rn = np.asarray(R_M)
        vc = 1.5e5 + 1.0e3 * np.arange(N)
        omega = np.stack([(vc / Rn) ** 2, 1.01 * (vc / Rn) ** 2], axis=1)
        fields = np.zeros((N, 1, 2, 10), dtype=complex)
        fields[..., 0] = -1.0e-7
        rot_arr = put_npz(os.path.join(bdir, 'rotation_base_arrays.npz'),
                          {'radial_nodes_m': Rn, 'rotation_Omega_squared': omega, 'full_fields_complex': fields})
        bkept = (o.get('kept_claim') or {}).get('B', dict(A.KEPT))
        bfin = put_json(os.path.join(bdir, 'finish.json'), {
            'uv_tail': {'schema': 'UNT_UV_TAIL_ROUTE_B_STAGE_RECORD_C2V001', 'stage_kind': 'le_rotation', 'enabled': True,
                        'state_digest': d['B'], 'roster_digest': rost['B'], 'kept': bkept, 'empty': False, 'config': cfg,
                        'config_sha256': cfg['sha256'], 'i1t': i1ts['B']},
            'arrays_path': rot_arr['path'], 'arrays_sha256': rot_arr['sha256'], 'positive_rotation_square': True,
            'minimum_rotation_square': float(omega.min()), 'nonpositive_indices': []})
        ctx = [{'name': 'route_a', 'kind': 'route_a', 'executed': True, 'exit_code': 1 if ev == 'exit1' else 0,
                'stage_dir': ra, 'argv': ra_argv},
               {'name': 'route_a_tail_manifest', 'kind': 'route_a_tail_manifest', 'executed': True, 'exit_code': 0,
                'stage_dir': ms, 'argv': ['--seed', 'synthetic', '--outdir', mdir]},
               {'name': 'reference', 'kind': 'reference', 'executed': True, 'exit_code': 0, 'stage_dir': rs,
                'argv': ['--outdir', rdir]},
               {'name': 'le3_rotation', 'kind': 'rotation_v005', 'executed': True, 'exit_code': 0, 'stage_dir': rot_stage,
                'argv': ['--outdir', bdir]}]
        if ev == 'two_route_a':
            ctx.append(dict(ctx[0], name='route_a_retry'))
        if ev == 'argv_missing':
            ctx[0] = {k: v for k, v in ctx[0].items() if k != 'argv'}
        srec = [{'stage': 'route_a_tail_manifest', 'kind': 'route_a_tail_manifest', 'finish_sha256': mfin['sha256'],
                 'state_digest': d['A'], 'empty': False},
                {'stage': 'reference', 'kind': 'reference', 'finish_sha256': rfin['sha256'], 'state_digest': d['A']},
                {'stage': 'le3_rotation', 'kind': 'rotation_v005', 'finish_sha256': bfin['sha256'], 'state_digest': d['B']}]
        # ---- passes and rows
        npass = len(rows_by_pass)
        passes = []
        for p, rows in enumerate(rows_by_pass):
            last = p == npass - 1
            inv_ids = [r['id'] for r in rows if r.get('valid') is False]
            cdir = os.path.join(stages, '%02d_le%d_column_mean' % (30 + p, p + 1), 'observation')
            support = [{'id': r['id'], 'radius_m': R_M[i], 'column_indices': [i]} for i, r in enumerate(rows)
                       if r.get('valid') is not False]
            if o.get('support_radius_off') and last:
                support[0] = dict(support[0], radius_m=support[0]['radius_m'] * (1 + 1e-9))
            cm = put_json(os.path.join(cdir, 'result.json'), {
                'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION', 'rotation_array_pin': rot_arr if last else None,
                'prediction': {'rows': rows, 'query_support': support}})
            pr = {'pass': p + 1, 'columns': ['c'],
                  'rotation': bdir if last else os.path.join(stages, '%02d_le%d_rotation' % (10 + p, p + 1), 'rotation'),
                  'column_mean': {'path': cm['path'], 'sha256': cm['sha256'],
                                  'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'},
                  'rows': rows, 'invalid_rows': inv_ids}
            if last:
                pr.update(rotation_arrays=dict(rot_arr), rotation_positive=True, column_failures=[])
            if p in (o.get('missing_pass_rows') or ()):
                pr.pop('rows')
                pr.pop('invalid_rows')
                pr['column_mean'] = 'NOT_OBSERVED (multi-run parallel pass or observe_every_pass false)'
            passes.append(pr)
        final = passes[-1]['rows']
        outcome = {'classification': 'CONVERGED', 'converged_finite_fixed_point': True, 'outcome': CONV,
                   'converged_iteration': 1}
        if ev == 'not_converged':
            outcome = {'classification': 'ROUTE_A_NO_FIXED_POINT', 'converged_finite_fixed_point': False,
                       'outcome': 'NO_FIXED_POINT', 'converged_iteration': None}
        if ev == 'conv_int':
            outcome = dict(outcome, converged_finite_fixed_point=1)
        status, valid = ('COMPLETED_INVALID', False) if ev == 'finish_invalid' else ('COMPLETED', True)
        result = {'driver_sha256': o.get('driver_sha256', self.registry['driver']['sha256']), 'galaxy': 'NGC3198',
                  'call_spec_sha256': spec_ref['sha256'], 'status': status, 'valid': valid, 'final_pass': npass,
                  'passes': passes, 'rows': final, 'speeds_km_s': {r['id']: r.get('speed_km_s') for r in final},
                  'invalid_rows': [r['id'] for r in final if r.get('valid') is False], 'stage_records': ctx,
                  'route_a_outcome': outcome,
                  'identity': {'route_a': {'mode': 'admitted_ngc_route_a_lane' if ev == 'mode_admitted' else 'computed',
                                           'attempt': att, 'checkpoint': cpd}},
                  'normalized_spec': spec,
                  'uv_tail': {'stage_records': srec, 'manifest': {'path': mpin['path'], 'sha256': mpin['sha256'],
                                                                  'state_digest': d['A'], 'empty': False,
                                                                  'production_admissible': True},
                              'route_a_record': rar}}
        rp = put_json(os.path.join(out, 'result.json'), result)
        if ev != 'no_start':
            put_json(os.path.join(out, 'start.json'), {'schema': 'synthetic start', 'driver_sha256': result['driver_sha256'],
                                                       'call_spec_sha256': spec_ref['sha256']})
        put_json(os.path.join(out, 'finish.json'), {
            'status': status, 'valid': valid,
            'result_path': rp['path'] if ev != 'result_path' else os.path.join(out, 'other_result.json'),
            'result_sha256': rp['sha256'], 'reasons': [], 'retries': 1 if ev == 'retries1' else 0,
            'partial_outputs_preserved': True})
        receipt = put_json(os.path.join(base, 'receipt.json'), {'status': 'FINISHED', 'driver_status': 'COMPLETED',
                                                                'result': {'sha256': rp['sha256']}})
        # ---- adapter-level inputs (direct, as in c2v002): iterate list and rebuild exports by synthetic producers
        iters = None
        if o.get('iterates', True):
            iters = put_json(os.path.join(base, 'iterates.json'), {
                'schema': 'UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001', 'producer': dict(self.sidecar_reader), 'call_result': rp,
                'occurrences': [
                    {'iteration': 0, 'role': CURRENT, 'state_sha256': d['I'], 'source_sha256': rost['I']},
                    {'iteration': 0, 'role': NEXT, 'state_sha256': d['A'], 'source_sha256': rost['A']},
                    {'iteration': 1, 'role': CURRENT, 'state_sha256': d['A'], 'source_sha256': rost['A']},
                    {'iteration': 1, 'role': NEXT, 'state_sha256': d['N'], 'source_sha256': rost['N']}]})
        exports = {}
        for k in 'BIN':
            rec_k, arr_k = st[k][0], dict(st[k][1])
            if k in (o.get('tamper_arrays') or ()):
                arr_k = dict(arr_k, ring_radii_m=arr_k['ring_radii_m'] * 2.0)
            if k in (o.get('b1_perturb') or ()):
                si = arr_k['shell_integrals'].copy()
                nz = np.flatnonzero(si[:, 1])[0]
                si[nz, 1] *= (1 + 1e-9)
                arr_k = dict(arr_k, shell_integrals=si)
            ra_ = put_npz(os.path.join(base, 'rebuild', '%s_arrays.npz' % k), arr_k)
            rr = put_json(os.path.join(base, 'rebuild', '%s_record.json' % k), rec_k)
            exports[d[k]] = put_json(os.path.join(base, 'rebuild', '%s_state_input.json' % k), {
                'schema': 'UNT_NGC_LO_STATE_INPUT_C2V001',
                'state': {'state_sha256': d[k], 'source_sha256': rost[k], 'stage_kind': rec_k['stage_kind']},
                'call_result': rp, 'source': 'POST_RUN_REBUILD', 'producer': dict(self.rebuild_producer),
                'tail_state': {'record': rr, 'arrays': ra_}})
        rho = self.make_rho(base, key, spec_ref, th, o.get('rho', 'same'))
        contract = {'schema': 'UNT_NGC_LO_ROW_CONTRACT_C2V002', 'query_ids': list(IDS), 'manifest': dict(self.manifest),
                    'manifest_radius_scale': 1.0, 'R_m': list(R_M), 'rule_id': self.rule_id, 'theta_hex': A.THETA_HEX,
                    'c_hex': A.C_HEX, 'binding': None}
        cv = o.get('contract', 'ok')
        if cv == 'sigma':
            contract['sigma_km_s'] = [1.0] * N
        elif cv == 'tau':
            contract['tau_km_s'] = [1.0] * N
        elif cv == 't_values':
            contract['t_km_s'] = [1.0e3] * N
        elif cv == 't_none_values':
            contract['t_km_s'] = [None] * N
        elif cv == 'c2v001_shape':
            contract = {'schema': 'UNT_NGC_LO_ROW_CONTRACT_C2V001', 'query_ids': list(IDS),
                        'manifest': dict(self.manifest), 'manifest_radius_scale': 1.0, 'R_m': list(R_M),
                        't_km_s': [1.0e3] * N, 't_rule_id': '## A155@' + A155_PIN['section_sha256'], 'binding': None}
        elif cv == 't_plain':
            contract['t'] = [1.0e3] * N
        elif cv == 'velocity':
            contract['v_reference_km_s'] = [100.0] * N
        elif cv == 'nmin':
            contract['N_min'] = 1.0e3
        elif cv == 'ks':
            contract['per_shell_scale'] = [1.0 / lo for lo, hi in PARTITION]
        elif cv == 'eps':
            contract['eps_km_s'] = [1.0e-9] * N
        elif cv == 'no_rule':
            for k in ('rule_id', 'theta_hex', 'c_hex'):
                contract.pop(k)
        elif cv == 'rule_other':
            contract['rule_id'] = 'A134_Q4C_TAU_0P25_SIGMA'
        elif cv == 'rule_partial':
            contract.pop('theta_hex')
        elif cv == 'theta_ulp':
            contract['theta_hex'] = math.nextafter(A.THETA, 1.0).hex()
        elif cv == 'c_ulp':
            contract['c_hex'] = math.nextafter(A.C_M_S, math.inf).hex()
        elif cv == 'theta_noncanonical':
            contract['theta_hex'] = A.THETA_HEX.replace('p-29', '0p-29')
        elif cv == 'order':
            contract['query_ids'] = list(reversed(IDS))
        elif cv == 'R_off':
            contract['R_m'] = [x * (1 + 1e-9) for x in R_M]
        cpin = put_json(os.path.join(base, 'row_contract.json'), contract)
        review = put_json(os.path.join(base, 'row_review.json'), {'schema': 'UNT_NGC_LO_ROW_POLICY_REVIEW_C2V002',
                                                                  'verdict': 'APPROVED', 'row_contract_sha256': cpin['sha256']})
        return {'name': name, 'base': base, 'call_dir': os.path.join(base, 'call'), 'out': os.path.realpath(out),
                'spec_ref': spec_ref, 'result': rp, 'receipt': receipt, 'iterates': iters, 'exports': exports, 'rho': rho,
                'contract': cpin, 'review': review, 'digests': d, 'rosters': rost, 'key': key,
                'b1A_s4': self.s4_b1(st['A'][3]), 's0': s0, 'states': st, 'vmax': vmax, 'cert': cert, 'cfg': cfg,
                'rot_arrays': rot_arr, 'point': point}

    def make_rho(self, base, key, spec_ref, th, variant):
        A = self.A
        rdir = os.path.join(base, 'rho')
        old = variant == 'c3v001_schemas'                       # A167: the c3v001 schema strings, refused by c2v003a
        idn = {'schema': 'UNT_NGC_POINT_RHO_IDENTITY_C3V001' if old else A.RHO_IDENTITY_SCHEMA, 'theta_key': key, 's0_record_sha256': self.registry['s0']['sha256'],
               'driver_sha256': self.registry['driver']['sha256'], 'spec_sha256': spec_ref['sha256'],
               'route_a_column_workers': 1,
               'theta_binding_hex': {'s': float(th['common_scale_s']).hex(), 'gamma_over_Eref': float(th['gamma_over_Eref']).hex(),
                                     'ell_F_m': float(th['ell_F_m']).hex(), 'Eref_base_J': float(th['Eref_base_J']).hex()}}
        psha = digest(idn)
        recompute_path = os.path.join(rdir, 'recompute_record.json')
        prod = put_bytes(os.path.join(rdir, 'syn_ngc_rho_producer.py'), (
            '"""synthetic NGC rho producer (test only)"""\nimport json\nRECORD = %r\n\n\n'
            'def produce(spec_ref, theta_key):\n    with open(RECORD) as f:\n        return json.load(f)\n'
            % recompute_path).encode())
        rec = {'schema': 'UNT_NGC_POINT_RHO_NUMERICAL_C3V001' if old else A.RHO_SCHEMA, 'gate': 'RHO_G', 'status': 'TESTED', 'verdict': 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED',
               'identity': idn, 'point_sha256': psha,
               'custody': {'schema': 'UNT_NGC_POINT_RHO_CUSTODY_C3V003', 'registry_kind': 'SYNTHETIC_TEST',
                           'symbol_route': 'SYNTHETIC_TEST_SYMBOL', 'theta_key': key, 'point_sha256': psha},
               'settings': 'registered', 'coverage_complete': True, 'required_coverage_inverse_kpc': [2.0, 91.0],
               'full_registered_search_executed': True,
               'shells': [{'range_inverse_kpc': list(r), 'rho_used': float(u)} for r, u in zip(PARTITION, RHO_USED)],
               'producer': prod}
        slot = dict(rec)
        if variant == 'ddo_schema':
            slot = dict(rec, schema='UNT_POINT_RHO_NUMERICAL_CX2V001')
        spin = put_json(os.path.join(rdir, 'slot_rho_record.json'), slot)
        recompute = dict(rec)
        if variant == 'ulp':
            sh = [dict(x) for x in rec['shells']]
            sh[3]['rho_used'] = math.nextafter(sh[3]['rho_used'], 1.0)
            recompute = dict(rec, shells=sh)
        elif variant == 'recompute_ddo':
            recompute = dict(rec, schema='UNT_POINT_RHO_NUMERICAL_CX2V001')
        put_json(recompute_path, recompute)
        proof = {'schema': 'UNT_NGC_POINT_LO_SLOT_PROOF_C3V001' if old else A.SLOT_PROOF_SCHEMA, 'gate': A.SLOT_GATE, 'status': 'TESTED', 'verdict': 'PASS',
                 'theta_key': key, 'point_sha256': psha, 'producer': dict(self.slot_proof_producer),
                 'driver_certificate': dict(self.launch), 'lo_certificate_launch_pin': dict(self.launch),
                 'rho_record': spin, 'rho_producer': prod,
                 'rho_bitwise_canonical_sha256': hashlib.sha256(A.rho_bitwise_canonical(slot)).hexdigest(),
                 'seed_rho_reproducibility': {'bitwise_equal_10_key': variant != 'g4false'},
                 'lo_route': A.ROUTE, 'lo_certified': False}
        if variant == 'cert':
            proof['rho_record'] = dict(self.launch)
        elif variant == 'covers':
            proof['covers_all_consumed_states'] = True
        elif variant == 'ddo_producer':
            proof['rho_producer'] = {'path': prod['path'], 'sha256': A.DDO_RESPONSE_SHA}
        ppin = put_json(os.path.join(rdir, 'slot_proof.json'), proof)
        return {'proof': ppin, 'producer': prod, 'slot': spin, 'approved_rho': [prod['sha256']] +
                ([A.DDO_RESPONSE_SHA] if variant == 'ddo_producer' else [])}


class Suite:
    def __init__(self, run_dir, module_dir):
        self.run_dir, self.module_dir = run_dir, module_dir
        self.paths = {k: os.path.join(module_dir, v) for k, v in NAMES.items()}
        self.paths['CONTRACT'] = os.path.join(module_dir, CONTRACT_FILE)
        self.shas = {k: sha_file(p) for k, p in self.paths.items()}
        self.E = load(self.paths['E'], 'suite_ngc_consumed_states')
        self.A = load(self.paths['A'], 'suite_ngc_lo_state_adapter')
        self.H = load(self.paths['H'], 'suite_ngc_acceptance_handoff')
        self.R = load(self.paths['R'], 'suite_ngc_route_a_iterates')
        self.S = load(self.paths['S'], 'suite_ngc_s5_rebuild_export')
        self.C = load(self.paths['C'], 'suite_ngc_row_contract')
        self.U = load(self.A.LIBRARY[0], 'suite_uvt_lapse_v002')
        assert sha_file(self.A.LIBRARY[0]) == self.A.LIBRARY[1]
        self.PV = load(self.S.PROVIDER[0], 'suite_jn_provider')
        assert sha_file(self.S.PROVIDER[0]) == self.S.PROVIDER[1]
        assert sha_file(ROW_PRODUCER[0]) == ROW_PRODUCER[1]
        self.rowmod = load(ROW_PRODUCER[0], 'suite_row_reference_producer_c2v003')
        self.art_patched = not run_dir.startswith(self.H.ART + os.sep)
        if self.art_patched:                                       # dev runs outside claude_artifacts only
            self.H.ART = os.path.dirname(run_dir)
        self.fx = Fx(run_dir, self.A, self.E, self.H, self.U, self.R, self.S, self.PV)
        self.results = []

    # ---------------------------------------------------------------- runners
    def env(self, call, registry=None):
        return self.A.make_env(registry or self.fx.registry, rho_producer_ref=call['rho']['producer'],
                               approved_rho_producer_sha256=call['rho']['approved_rho'])

    def inventory(self, call, driver=None):
        return self.E.enumerate_call(call['call_dir'], route_a_iterates_ref=call['iterates'],
                                     approved_iterate_producer_sha256=[self.fx.sidecar_reader['sha256']],
                                     driver_sha256=driver or self.fx.registry['driver']['sha256'])

    def state_inputs(self, call, inv, out_root, exports=None):
        si = dict(call['exports'] if exports is None else exports)
        man = read_json(inv['manifest'])
        acc = [s for s in inv['states'] if s['state_sha256'] == inv['accepted_state_sha256']][0]
        rr = put_json(os.path.join(out_root, 'ACC_RECORD.json'), man['state']['record'])
        si[acc['state_sha256']] = put_json(os.path.join(out_root, 'ACC_INPUT.json'), {
            'schema': 'UNT_NGC_LO_STATE_INPUT_C2V001', 'state': acc, 'call_result': inv['call_result'],
            'source': 'ROUTE_A_TAIL_MANIFEST', 'tail_state': {'record': rr, 'arrays': man['state']['arrays']}})
        return si

    def adapt(self, call, *, registry=None, approved=None, review=True, rebuild_ok=True, inv=None, state_inputs=None,
              tag='adapt', rebuild=None):
        A = self.A
        inv = inv if inv is not None else self.inventory(call)
        out_root = os.path.join(call['base'], tag)
        os.makedirs(out_root)
        si = state_inputs if state_inputs is not None else self.state_inputs(call, inv, out_root)
        if rebuild is None:
            rebuild = [self.fx.rebuild_producer['sha256']] if rebuild_ok else []
        rec = A._adapt_call(
            call_dir=call['call_dir'], spec_ref=call['spec_ref'], inventory=inv, state_inputs=si,
            row_contract_ref=call['contract'], row_policy_review_ref=call['review'] if review else None,
            slot_proof_ref=call['rho']['proof'],
            approved_producer_sha256=[self.shas['A']] if approved is None else approved,
            approved_slot_proof_producer_sha256=[self.fx.slot_proof_producer['sha256']],
            approved_rho_producer_sha256=call['rho']['approved_rho'],
            approved_rebuild_producer_sha256=rebuild,
            trusted_row_policy_review_sha256=[call['review']['sha256']] if review else [], out_root=out_root,
            env=self.env(call, registry))
        return rec, inv

    def by_state(self, rec, call):
        m = {s['state']['state_sha256']: s for s in rec['states']}
        return {k: m.get(d) for k, d in call['digests'].items()}

    def prep(self, call, tag='s5', driver=None, recipe=None):
        return self.H.prepare_acceptance_inputs(
            call_dir=call['call_dir'], recipe_ref=recipe or self.fx.recipe,
            approved_recipe_sha256=[(recipe or self.fx.recipe)['sha256']], out_dir=os.path.join(call['base'], tag),
            driver_sha256=driver or self.fx.registry['driver']['sha256'], modules=(self.E, self.A, self.R, self.S))

    def policy(self, call, prep=None, **kw):
        p = {'receipt': call['receipt'], 'row_policy_review': call['review'],
             'trusted_row_policy_review_sha256': [call['review']['sha256']], 'slot_proof': call['rho']['proof'],
             'rho_producer': call['rho']['producer'], 'approved_producer_sha256': [self.shas['A']],
             'eps_certificate': call['cert']}
        if prep is not False:
            pr = prep or self.prep(call)
            p.update(route_a_iterates=pr['route_a_iterates'], rebuild_exports=pr['rebuild_exports'])
        p.update(kw)
        return {k: v for k, v in p.items() if v is not None}

    def s2_synthetic(self, call):
        return {'rho_producer_sha256': call['rho']['producer']['sha256'],
                'slot_proof_producer_sha256': self.fx.slot_proof_producer['sha256']}

    def handoff(self, call, *, adapter_fn=None, policy=None, tag='handoff', s2=None, contract=None, registry=None,
                approvals=None):
        H, A = self.H, self.A
        env = self.env(call)

        def fn(**kw):
            kw.pop('rho_producer_ref')
            return A._adapt_call(env=env, **kw)
        return H._accept(call_dir=call['call_dir'], spec_ref=call['spec_ref'],
                         policy=self.policy(call) if policy is None else policy,
                         records_dir=os.path.join(call['base'], tag), enumerate_fn=self.E.enumerate_call,
                         adapter_fn=adapter_fn or fn, A=A, registry=registry or self.fx.registry, R=self.R, S=self.S,
                         s2_pins=self.s2_synthetic(call) if s2 is None else s2,
                         contract_pin=call['contract'] if contract is None else contract, lib=self.U, rowmod=self.rowmod,
                         approvals=approvals or {'reader': dict(H.ITERATE_READER), 's5': dict(H.S5_TOOL)})

    def record(self, rid, kind, ok, detail):
        self.results.append({'id': rid, 'kind': kind, 'ok': bool(ok), 'detail': detail})

    def run(self, rid, kind, fn):
        t0 = time.monotonic()
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, 'EXCEPTION %s: %s | %s' % (type(exc).__name__, exc, traceback.format_exc()[-1500:])
        self.record(rid, kind, ok, detail)
        self.results[-1]['seconds'] = round(time.monotonic() - t0, 3)

    # ---------------------------------------------------------------- helpers
    def oracle_mismatch(self, rec_file):
        A = self.A
        r = read_json(rec_file)
        rows = {x['id']: x for x in r['rows']['rows']}
        bad = []
        for sh in r['shells']:
            for j, q in enumerate(r['rows_in_arithmetic']):
                v, R = rows[q]['v_reference_km_s'], rows[q]['R_m']
                want = oracle_g(v, R, sh['rho_used'], sh['B1_per_m'], A.C_M_S, A.THETA)
                got = sh['per_row_g'][j]
                if not (math.isfinite(got) and abs(got - want) <= 1e-12 * max(abs(want), 1e-300)):
                    bad.append([sh['range_inverse_kpc'], q, got, want])
                if v > 0 and sh['B1_per_m'] > 0 and got > 0:
                    t = A.C_M_S ** 2 * A.THETA / (2e6 * v)
                    if abs(sh['per_row_d_km_s'][j] / got - t) > 1e-12 * t:
                        bad.append(['d/g != t_i', sh['range_inverse_kpc'], q])
        return bad

    def agg(self, rows, b1=None, edges=None, rho=1.0):
        np, A = self.fx.np, self.A
        e = A.expected_unit_edges() if edges is None else np.asarray(edges, float)
        b = np.ones(len(e) - 1) if b1 is None else np.asarray(b1, float)
        sh = [{'range_inverse_kpc': r, 'rho_used': rho} for r in PARTITION]
        g = A.aggregate(sh, e, b, rows, c=A.C_M_S, theta=A.THETA)
        return g, A.decide(g, rows)

    @staticmethod
    def codes(entry):
        return entry['codes'] if entry else None

    def all_codes(self, rec, code):
        return bool(rec['states']) and all(s['codes'] == [code] for s in rec['states']) and rec['call_lo_reading'] == 'INCOMPLETE'

    def refused(self, fn, cls):
        try:
            fn()
            return False, None
        except cls as exc:
            return True, str(exc)[:160]

    # ================================================================ MUST_PASS (ported c2v002)
    def p01(self):
        c = self.fx.make_call('p01')
        inv = self.inventory(c)
        cl = {x['state']['state_sha256']: x['class'] for x in inv['classes']}
        d = c['digests']
        want = {d['A']: 'ACCEPTED_ROUTE_A', d['B']: 'ROUTE_B_STAGE', d['I']: 'ROUTE_A_PRE_ACCEPTANCE_ITERATE',
                d['N']: 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'}
        roles_a = [x['roles'] for x in inv['classes'] if x['state']['state_sha256'] == d['A']][0]
        ok = inv['complete'] and cl == want and 'inherited_route_a' in roles_a and len(inv['states']) == 4
        return ok, {'complete': inv['complete'], 'classes': sorted(cl.values()), 'roles_A': roles_a, 'blockers': inv['blockers']}

    def p02(self):
        np, A = self.fx.np, self.A
        e = A.expected_unit_edges()
        b1 = np.zeros(len(e) - 1)
        b1[0], b1[5], b1[30], b1[40], b1[44] = 1.0, 2.0, 3.0, 4.0, 5.0
        rows = [{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 1.0, 'R': 1.0}]
        agg, dec = self.agg(rows, b1, e)
        dom = [s['domain'] for s in agg['shells']]
        b = [s['B1_per_m'] for s in agg['shells']]
        ok = (float(e[-1]) == 47.0 and dom == ['TILED'] * 7 + ['PARTIAL_TO_E_TOP', 'NOT_IN_STATE_DOMAIN']
              and b == [1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 12.0, 0.0] and agg['shells'][8]['max_g'] == 0.0
              and agg['G'] == sum(s['max_g'] for s in agg['shells']) and len(agg['shells']) == 9
              and agg['coverage_problem'] is None and dec[0] in ('PASS', 'FAIL'))
        return ok, {'E_top': float(e[-1]), 'domains': dom, 'B1_s': b, 'decision': dec[:2]}

    def p03(self):
        np, A = self.fx.np, self.A
        out = {}
        for top in (64.0, 91.0):
            e = np.arange(2.0, top + 1.0)
            agg, _ = self.agg([{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 1.0, 'R': 1.0}], np.ones(len(e) - 1), e)
            out[top] = ([s['domain'] for s in agg['shells']], [s['B1_per_m'] for s in agg['shells']], agg['coverage_problem'])
        ok = (out[64.0][0] == ['TILED'] * 8 + ['NOT_IN_STATE_DOMAIN'] and out[64.0][1][7] == 32.0 and out[64.0][2] is None
              and out[91.0][0] == ['TILED'] * 9 and out[91.0][1][8] == 27.0 and out[91.0][2] is None)
        return ok, {str(k): v for k, v in out.items()}

    def readouts(self, **o):
        c = self.fx.make_call('ro_%d' % self.fx.n, **o)
        result = read_json(c['result'])
        return c, self.A.own_call_readouts(result, IDS)

    def p04(self):
        c, ro = self.readouts()
        v = [r['v'] for r in ro['rows']]
        want = [BASE_V[i] if i != 5 else BASE_V[5] + 30.0 for i in range(N)]
        ok = ro['call_problem'] is None and v == want and all(r['status'] == 'INCLUDED' for r in ro['rows'])
        return ok, {'row5': v[5], 'statuses': sorted({r['status'] for r in ro['rows']})}

    def p05(self):
        c, ro = self.readouts(X={'SYNQ-01': {'reason': 'QUERY_INSIDE_INNERMOST_NODE', 'earlier': None}})
        r = ro['rows'][0]
        ok = r['status'] == 'EXCLUDED_REGISTERED_MISS' and r['reason'] == 'QUERY_INSIDE_INNERMOST_NODE' and r['v'] is None
        return ok, r

    def p06(self):
        c, ro = self.readouts(X={'SYNQ-43': {'reason': 'QUERY_BEYOND_OUTER_GAS_CUT', 'earlier': -777.0}})
        r = ro['rows'][42]
        return r['status'] == 'INCLUDED' and r['v'] == 777.0, r

    def p07(self):
        c, ro = self.readouts()
        result = read_json(c['result'])
        plain = [max(abs(p['rows'][i]['speed_km_s']) for p in result['passes']) for i in range(N)]
        return ro['X'] == [] and [r['v'] for r in ro['rows']] == plain, {'X': ro['X']}

    def p08(self):
        c = self.fx.make_call('p08', missing_readout=[(1, 3)], scales={'B': 10.0})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        b = read_json(s['B']['record'])
        ok = (s['B']['verdict'] == 'FAIL' and b['monotone_fail_decided'] is True and s['A']['codes'] == ['READOUT_NOT_RECORDED']
              and rec['call_lo_reading'] == 'NON_LAPSE_TAIL_MATERIAL' and b['fail_text'] == self.A.FAIL_TEXT)
        return ok, {'B': s['B']['verdict'], 'A': s['A']['codes'], 'call': rec['call_lo_reading']}

    def p09(self):
        c = self.fx.make_call('p09', missing_readout=[(1, 3)])
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        ok = all(s[k]['verdict'] == 'UNAVAILABLE' and s[k]['codes'] == ['READOUT_NOT_RECORDED'] for k in STATES) \
            and rec['call_lo_reading'] == 'INCOMPLETE'
        return ok, {k: s[k]['codes'] for k in STATES}

    def p10(self):
        c, ro = self.readouts(X={'SYNQ-43': {'reason': 'QUERY_BEYOND_OUTER_GAS_CUT', 'earlier': 50.0}})
        d = ro['diagnostic']['pass_invalid_rows_equal_X']
        return d == [False, True, True], d

    def p11(self):
        A = self.A
        c = self.fx.make_call('p11')
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        recs = {k: read_json(s[k]['record']) for k in STATES}
        numbers_in_call = floats_outside_flags(rec)
        top = max(range(len(PARTITION)), key=lambda i: RHO_USED[i] * c['b1A_s4'][i])
        t_keys = [k for r in recs.values() for k in A._keys_named(r, A.T_VALUE_KEYS)]
        ok = (rec['call_lo_reading'] == 'PASS' and all(s[k]['verdict'] == 'PASS' for k in STATES)
              and all(r['scope_disclosure'] == A.SCOPE_DISCLOSURE and r['pass_meaning'] == A.PASS_MEANING
                      and r['t_rule_id'] == A.RULE_ID for r in recs.values())
              and not numbers_in_call and not t_keys and abs(recs['A']['shells'][top]['max_g'] - TARGET_MAX_G) < 1e-12
              and recs['A']['shells'][8]['domain'] == 'NOT_IN_STATE_DOMAIN' and recs['A']['shells'][7]['domain'] == 'PARTIAL_TO_E_TOP'
              and len(recs['A']['rows_in_arithmetic']) == N and recs['A']['G'] < 0.05 and rec['pass_meaning'] == A.PASS_MEANING)
        return ok, {'call': rec['call_lo_reading'], 'states': {k: s[k]['verdict'] for k in STATES},
                    'numeric_keys_in_call_record': numbers_in_call, 't_keys_in_records': t_keys,
                    'max_g_A_minus_target': recs['A']['shells'][top]['max_g'] - TARGET_MAX_G}

    def p12(self):
        c = self.fx.make_call('p12', scales={'B': 10.0})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        b = read_json(s['B']['record'])
        ok = (s['B']['verdict'] == 'FAIL' and s['B']['reading'] == 'NON_LAPSE_TAIL_MATERIAL' and s['A']['verdict'] == 'PASS'
              and rec['call_lo_reading'] == 'NON_LAPSE_TAIL_MATERIAL' and b['fail_text'] == self.A.FAIL_TEXT
              and b['scope_disclosure'] == self.A.SCOPE_DISCLOSURE and b['monotone_fail_decided'] is False)
        return ok, {'B': s['B']['reading'], 'call': rec['call_lo_reading']}

    def p13(self):
        c = self.fx.make_call('p13', scales={'I': 10.0})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        ok = (s['I']['verdict'] == 'FAIL' and s['I']['reading'] == 'LO_UNCERTIFIED_TRANSIENT'
              and s['A']['verdict'] == s['B']['verdict'] == s['N']['verdict'] == 'PASS'
              and rec['call_lo_reading'] == 'LO_UNCERTIFIED_TRANSIENT')
        return ok, {'call': rec['call_lo_reading'], 'states': {k: s[k]['verdict'] for k in STATES}}

    def p14(self):
        c = self.fx.make_call('p14', scales={'I': 10.0})
        inv = self.inventory(c)
        out_root = os.path.join(c['base'], 'si')
        os.makedirs(out_root)
        si = self.state_inputs(c, inv, out_root)
        si.pop(c['digests']['B'])
        rec, _ = self.adapt(c, inv=inv, state_inputs=si)
        s = self.by_state(rec, c)
        ok = (s['I']['verdict'] == 'FAIL' and s['B']['verdict'] == 'UNAVAILABLE' and rec['call_lo_reading'] == 'INCOMPLETE'
              and rec['class_reading'] == 'INCOMPLETE' and rec['transient_candidate_unconfirmed'])
        return ok, {'call': rec['call_lo_reading'], 'B': s['B']['codes']}

    def p15(self):
        c = self.fx.make_call('p15', scales={'B': 10.0})
        inv = self.inventory(c)
        out_root = os.path.join(c['base'], 'si')
        os.makedirs(out_root)
        si = self.state_inputs(c, inv, out_root)
        si.pop(c['digests']['I'])
        rec, _ = self.adapt(c, inv=inv, state_inputs=si)
        s = self.by_state(rec, c)
        ok = s['B']['verdict'] == 'FAIL' and s['I']['verdict'] == 'UNAVAILABLE' and rec['call_lo_reading'] == 'NON_LAPSE_TAIL_MATERIAL'
        return ok, {'call': rec['call_lo_reading']}

    def real_call(self, name):
        """A fabricated call naming the registered driver sha (a string). Its spec label carries no theta key."""
        return self.fx.make_call(name, driver_sha256=REAL_DRIVER_SHA,
                                 spec_overrides={'label': 'step5 A_K32_A2_HEADLINE theta_key=NOT_A_REAL_KEY'})

    def gate_precheck(self):
        A = self.A
        return (A.T_I_ENTRY == dict(A155_PIN, path=A.V006) and A.t_rule_id(A.real_registry()) == A.RULE_ID
                and A.real_registry()['t_i_entry'] == A.T_I_ENTRY)

    def p16(self):
        A = self.A
        if not self.gate_precheck():
            return False, 'T_I_ENTRY is not the A155 section pin in this module: the public entry is not run'
        c = self.real_call('p16')
        inv = self.inventory(c, driver=REAL_DRIVER_SHA)
        out_root = os.path.join(c['base'], 'public')
        os.makedirs(out_root)
        si = self.state_inputs(c, inv, out_root)
        rec = A.adapt_call_ngc_lo(call_dir=c['call_dir'], spec_ref=c['spec_ref'], inventory=inv, state_inputs=si,
                                  row_contract_ref=c['contract'], row_policy_review_ref=c['review'],
                                  slot_proof_ref=c['rho']['proof'], rho_producer_ref=c['rho']['producer'],
                                  approved_producer_sha256=[self.shas['A']],
                                  approved_slot_proof_producer_sha256=[self.fx.slot_proof_producer['sha256']],
                                  approved_rho_producer_sha256=c['rho']['approved_rho'],
                                  approved_rebuild_producer_sha256=[self.fx.rebuild_producer['sha256']],
                                  trusted_row_policy_review_sha256=[c['review']['sha256']], out_root=out_root)
        recs = [read_json(s['record']) for s in rec['states'] if s.get('record')]
        numeric = [k for r in recs for k in ('shells', 'rows', 'G', 'gamma_c4b', 'B1_recomputed', 'rho') if k in r]
        ok = (rec['registry_kind'] == 'REGISTERED' and rec['t_rule_id'] == A.RULE_ID and rec['t_i_declared'] is True
              and rec['t_i_entry'] == A.T_I_ENTRY and A.T_I_ENTRY in rec['root_rulings']
              and len(rec['states']) == 4 and all(s['codes'] == ['NGC_POINT_CUSTODY_MISMATCH'] for s in rec['states'])
              and any('SPEC_LABEL_HAS_NO_THETA_KEY' in b for b in rec['blockers'])
              and rec['call_lo_reading'] == 'INCOMPLETE' and not numeric and len(recs) == 4 and 'point_sha256' not in rec
              and all(r['scope_disclosure'] == A.SCOPE_DISCLOSURE and r['pass_meaning'] == A.PASS_MEANING for r in recs))
        return ok, {'call': rec['call_lo_reading'], 'codes': [s['codes'] for s in rec['states']], 'numeric_keys': numeric,
                    't_rule_id': rec.get('t_rule_id'), 'blockers': rec['blockers'][:2]}

    def p17(self):
        c = self.fx.make_call('p17')
        rec, pin = self.handoff(c)
        summ = read_json(rec['root_summary'])
        leaks = floats_outside_flags(summ) + floats_outside_flags(rec)
        ok = (rec['reading'] == 'ACCEPTED' and rec['member_lo_ok'] is True and len(rec['states']) == 4
              and all(e['verdict'] == 'PASS' for e in rec['states']) and not leaks and summ['reading'] == 'ACCEPTED'
              and summ['pass_meaning'] == self.A.PASS_MEANING and summ['t_rule_id'] == self.A.RULE_ID
              and rec['blockers'] == [])
        return ok, {'reading': rec['reading'], 'blockers': rec['blockers'], 'value_leaks': leaks[:5]}

    def p18(self):
        H, A = self.H, self.A
        if not self.gate_precheck():
            return False, 'T_I_ENTRY is not the A155 section pin in this module: the public entry is not run'
        c = self.real_call('p18')
        pr = self.prep(c, driver=REAL_DRIVER_SHA)
        rec, pin = H.accept_call_ngc(call_dir=c['call_dir'], spec_ref=c['spec_ref'], policy=self.policy(c, prep=pr),
                                     records_dir=os.path.join(c['base'], 'handoff_public'))
        ok = (rec['reading'] == 'INCOMPLETE' and rec['member_lo_ok'] is False and len(rec['states']) == 4
              and all(e['codes'] == ['NGC_POINT_CUSTODY_MISMATCH'] for e in rec['states'])
              and rec['registry_kind'] == 'REGISTERED' and rec['pins']['lo_adapter']['sha256'] == self.shas['A']
              and rec['pins']['enumerator']['sha256'] == self.shas['E'] and rec['t_rule_id'] == A.RULE_ID
              and rec['pins']['iterate_reader']['sha256'] == self.shas['R'] and rec['pins']['s5_tool']['sha256'] == self.shas['S']
              and rec['pins']['row_contract'] == H.ROW_CONTRACT and rec['s2'] == 'PENDING'
              and any(b.startswith('S2_RHO_PINS_PENDING') for b in rec['blockers']))
        return ok, {'reading': rec['reading'], 'codes': [e['codes'] for e in rec['states']], 'blockers': rec['blockers'][:4]}

    def p19(self):
        c = self.fx.make_call('p19', scales={'B': 10.0})
        rec, pin = self.handoff(c)
        ok = rec['reading'] == 'NON_LAPSE_TAIL_MATERIAL' and rec['member_lo_ok'] is False and rec['rows_are_model_output'] is False
        return ok, {'reading': rec['reading']}

    def p20(self):
        c = self.fx.make_call('p20')
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        g = read_json(s['A']['record'])['gamma_c4b']
        ok = (g['bits_equal'] is True and g['state_gamma_eff_hex'] == g['spec_route_gamma_eff_hex'] == g['theta_route_gamma_eff_hex']
              and g['theta_route_bits_equal_diagnostic'] is True and g['rule'] == self.A.C4B_RULE)
        return ok, g

    def p21(self):
        c = self.fx.make_call('p21')
        rec, _ = self.adapt(c)
        r = read_json(self.by_state(rec, c)['B']['record'])
        b = r['B1_recomputed']
        return (r['rho_bitwise_equal_to_slot'] is True and b['max_relative_difference'] <= 1e-10), \
            {'rho_equal': r['rho_bitwise_equal_to_slot'], 'b1': b}

    def p22(self):
        c = self.fx.make_call('p22')
        rec, pin = self.handoff(c, policy=self.policy(c, high_qinf_admitted=True))
        return rec['reading'] == 'ACCEPTED' and rec['high_qinf_ngc_lo_flagged'] is True, {'reading': rec['reading']}

    def p23(self):
        c = self.fx.make_call('p23')
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        bad = {k: self.oracle_mismatch(s[k]['record'])[:3] for k in STATES}
        return rec['call_lo_reading'] == 'PASS' and not any(bad.values()), {'call': rec['call_lo_reading'],
                                                                            'oracle_mismatches': bad}

    def p24(self):
        A = self.A
        rows1 = [{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 150.0, 'R': 3.0e20}]
        rows2 = [{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 300.0, 'R': 3.0e20}]
        a1, _ = self.agg(rows1)
        a2, _ = self.agg(rows2)
        ratios = [b['max_g'] / a['max_g'] for a, b in zip(a1['shells'], a2['shells']) if a['max_g'] > 0]
        ok = bool(ratios) and all(r == 4.0 for r in ratios) and a2['G'] == 4.0 * a1['G']
        return ok, {'ratios': sorted(set(ratios)), 'G_ratio': a2['G'] / a1['G']}

    # ================================================================ MUST_PASS (A162 additions)
    def p25(self):
        """A162 item 1: the reader enumerates the sidecar (controller format) from the call's own bytes."""
        c = self.fx.make_call('p25')
        d = c['digests']
        enum = self.R.enumerate_sidecar(c['call_dir'], driver_sha256=self.fx.registry['driver']['sha256'])
        want = [{'iteration': 0, 'role': CURRENT, 'state_sha256': d['I']}, {'iteration': 0, 'role': NEXT, 'state_sha256': d['A']},
                {'iteration': 1, 'role': CURRENT, 'state_sha256': d['A']}, {'iteration': 1, 'role': NEXT, 'state_sha256': d['N']}]
        tg = self.R.s5_targets(enum)
        ok = (enum['occurrences'] == want and enum['accepted_state_sha256'] == d['A'] and enum['accepted_iteration'] == 1
              and enum['states'] == [d['I'], d['A'], d['N']] and enum['chain_next_equals_next_current'] == [True]
              and enum['sidecar']['finish_index'] == 0 and enum['reloaded_iterations'] == []
              and enum['accepted_stage_kind'] == 'route_a' and enum['converged_flags'] == [False, True]
              and [t['state']['state_sha256'] for t in tg] == [d['I'], d['N']]
              and all(t['state']['source_sha256'] is None and t['origin']['kind'] == 'ROUTE_A_ITERATE' for t in tg))
        return ok, {'occurrences_equal': enum['occurrences'] == want, 'targets': len(tg), 'finish_index': enum['sidecar']['finish_index']}

    def p26(self):
        """A162 item 1: the iterate list written by the reader from S5 admissions is the enumerator's input of record."""
        c = self.fx.make_call('p26')
        d, r = c['digests'], c['rosters']
        pr = self.prep(c)
        lst = read_json(pr['route_a_iterates'])
        inv = self.E.enumerate_call(c['call_dir'], route_a_iterates_ref=pr['route_a_iterates'],
                                    approved_iterate_producer_sha256=[self.shas['R']],
                                    driver_sha256=self.fx.registry['driver']['sha256'])
        cl = {x['state']['state_sha256']: x['class'] for x in inv['classes']}
        v = self.R.verify_iterate_list(pr['route_a_iterates'], c['call_dir'], driver_sha256=self.fx.registry['driver']['sha256'])
        ok = (inv['complete'] is True and cl == {d['A']: 'ACCEPTED_ROUTE_A', d['B']: 'ROUTE_B_STAGE',
                                                 d['I']: 'ROUTE_A_PRE_ACCEPTANCE_ITERATE', d['N']: 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'}
              and [o['source_sha256'] for o in lst['occurrences']] == [r['I'], r['A'], r['A'], r['N']]
              and lst['producer']['sha256'] == self.shas['R'] and v['list'] == pr['route_a_iterates']
              and lst['source_basis'][d['A']]['kind'] == 'ACCEPTED_ROUTE_A_TAIL_MANIFEST'
              and lst['source_basis'][d['I']]['kind'] == lst['source_basis'][d['N']]['kind'] == 'S5_ADMISSION')
        return ok, {'complete': inv['complete'], 'blockers': inv['blockers'], 'classes': sorted(cl.values())}

    def p27(self):
        """A162 item 2: S5 rebuilds B, I and N from their own rosters through the pinned library; each is admitted only
        on digest equality; the timing is recorded (U4); the exports pass the adapter (every state PASS)."""
        c = self.fx.make_call('p27')
        d = c['digests']
        pr = self.prep(c)
        adms = {k: read_json(p) for k, p in pr['admissions'].items()}
        inv = self.E.enumerate_call(c['call_dir'], route_a_iterates_ref=pr['route_a_iterates'],
                                    approved_iterate_producer_sha256=[self.shas['R']],
                                    driver_sha256=self.fx.registry['driver']['sha256'])
        out_root = os.path.join(c['base'], 'si')
        os.makedirs(out_root)
        si = self.state_inputs(c, inv, out_root, exports=pr['rebuild_exports'])
        rec, _ = self.adapt(c, inv=inv, state_inputs=si, rebuild=[self.shas['S']], tag='adapt_s5')
        s = self.by_state(rec, c)
        timing_ok = all(isinstance(a['timing_seconds'][k], float) and a['timing_seconds'][k] >= 0
                        for a in adms.values() for k in ('recipe', 'build', 'export', 'total'))
        exp = {k: read_json(p) for k, p in pr['rebuild_exports'].items()}
        ok = (set(adms) == {d['B'], d['I'], d['N']} and all(a['admitted'] is True and a['digest_equal'] is True
                                                           and a['codes'] == [] for a in adms.values())
              and adms[d['B']]['roster']['equal'] is True and adms[d['I']]['roster']['recorded_source_sha256'] is None
              and timing_ok and set(exp) == {d['B'], d['I'], d['N']}
              and all(e['producer']['sha256'] == self.shas['S'] and e['source'] == 'POST_RUN_REBUILD' for e in exp.values())
              and rec['call_lo_reading'] == 'PASS' and all(s[k]['verdict'] == 'PASS' for k in STATES))
        return ok, {'call': rec['call_lo_reading'], 'states': {k: (s[k] or {}).get('codes') for k in STATES},
                    'admitted': {k[:12]: a['admitted'] for k, a in adms.items()}, 'timing_ok': timing_ok}

    def p28(self):
        """A162 chain end to end: reader + S5 + enumerator + adapter + handoff: ACCEPTED; pins, exports and iterate list
        recorded; execution facts established; SRB-ROT report computed (report-only)."""
        c = self.fx.make_call('p28')
        rec, pin = self.handoff(c)
        d = c['digests']
        ex = rec['execution']
        ok = (rec['reading'] == 'ACCEPTED' and rec['member_lo_ok'] is True and rec['blockers'] == []
              and set(rec['rebuild_exports']) == {d['B'], d['I'], d['N']} and is_pin_(rec.get('route_a_iterates'))
              and rec['pins']['iterate_reader']['sha256'] == self.shas['R'] and rec['pins']['s5_tool']['sha256'] == self.shas['S']
              and rec['s2'] == 'PINNED' and ex['fresh_call'] is True and ex['resumed'] is False and ex['retried'] is False
              and ex['route_a_completed_normally'] is True and ex['run_root'] == c['out']
              and rec['srb_rot_report']['status'] == 'COMPUTED' and rec['srb_rot_report']['gates'] is False)
        return ok, {'reading': rec['reading'], 'blockers': rec['blockers'][:3], 'execution': {k: ex.get(k) for k in
                    ('fresh_call', 'resumed', 'retried', 'route_a_completed_normally')}, 'srb': rec['srb_rot_report']}

    def p29(self):
        """A162 item 3: the built NGC row contract: the pinned sha from bytes; the manifest a2936517 ids and order; R_i =
        float(Rad_text) * KPC_M bit for bit; rule id, theta and c hex; no velocity, t_i or sigma; the adapter's own S8
        check reads BOUND on the REGISTERED registry; the builder reproduces it."""
        H, A, C = self.H, self.A, self.C
        cp = dict(H.ROW_CONTRACT)
        with open(cp['path'], 'rb') as f:
            raw = f.read()
        doc = json.loads(raw)
        with open(C.MANIFEST['path'], 'rb') as f:
            mraw = f.read()
        man = json.loads(mraw)
        reg = A.real_registry()
        status = A.check_row_contract(cp, reg, A.make_reader(reg), None, None, A.RULE_ID)[2]
        ok = (sha_bytes(raw) == cp['sha256'] and sha_bytes(mraw) == C.MANIFEST['sha256'] == A.MANIFEST['sha256']
              and os.path.basename(cp['path']) == CONTRACT_FILE and sorted(doc) == sorted(A.CONTRACT_KEYS)
              and doc['query_ids'] == [r['query_id'] for r in man['rows']] == ['NGC3198-Q%02d' % i for i in range(1, 44)]
              and all(float(x).hex() == (float(r['Rad_text']) * KPC_M).hex() for x, r in zip(doc['R_m'], man['rows']))
              and len(doc['R_m']) == 43 and doc['rule_id'] == 'TI_B_SCALE_R_V001' and doc['theta_hex'] == '0x1.ce9660bc22098p-29'
              and doc['c_hex'] == (299792458.0).hex() and doc['manifest'] == A.MANIFEST and doc['binding'] is None
              and doc['manifest_radius_scale'] == 1.0 and A._keys_with_tokens(doc) == [] and status == 'BOUND'
              and C.build_contract() == doc)
        return ok, {'contract_sha256': sha_bytes(raw), 'adapter_check': status, 'keys': sorted(doc)}

    def p30(self):
        """A162 item 4: execution facts recorded from the call's own records (fresh, not resumed, not retried, completed
        normally, run_root), and the blinded summary carries them as booleans."""
        c = self.fx.make_call('p30')
        rec, pin = self.handoff(c)
        summ = read_json(rec['root_summary'])
        ex = rec['execution']
        ok = (rec['reading'] == 'ACCEPTED' and all(ex[k] is v for k, v in self.H.EXECUTION_REQUIRED.items())
              and ex['run_root'] == c['out'] and summ['execution'] == {k: ex[k] for k in self.H.EXECUTION_KEYS}
              and ex['basis']['rule'] == self.H.NGC_EXECUTION_RULE and ex['basis']['route_a_stage_records'] == 1
              and ex['basis']['sidecar_finish_index'] == 0 and ex['basis']['start_present'] is True)
        return ok, {'execution': summ['execution']}

    def srb_oracle(self, c, prep_or_exports):
        """Independent SRB-ROT bound: R c^2 sum_s eps_s B_s^(1) / (2 N_min v_c) / 1e3 at each row's own column."""
        np = self.fx.np
        si = read_json(prep_or_exports[c['digests']['B']])
        arrays = load_npz(si['tail_state']['arrays']['path'])
        record = read_json(si['tail_state']['record'])
        cert = read_json(c['cert'])
        eps = {float(s['lo_inverse_kpc']): float(s['eps']) for s in cert['shells']}
        edges = arrays['shell_edges_inverse_kpc']
        B1 = arrays['shell_integrals'][:, 1]
        Btot = sum(eps[float(edges[i])] * float(B1[i]) for i in range(len(B1)))
        rot = load_npz(c['rot_arrays']['path'])
        R, om, fl = rot['radial_nodes_m'], rot['rotation_Omega_squared'], rot['full_fields_complex']
        nmin = float(np.min(1 + fl[..., 0].real))
        v = R * np.sqrt(np.min(om, axis=1))
        col = R * record['c_m_s'] ** 2 * Btot / (2 * nmin * v) / 1e3
        return [float(x) for x in col]

    def p31(self):
        """A162 item 5: SRB-ROT for NGC is computed with the pinned srb_rot and rotation_rows, equals an independent
        oracle, is labelled report-only, and is written only to SRB_ROT_REPORT.json (no value in the record or summary)."""
        c = self.fx.make_call('p31')
        pr = self.prep(c)
        rec, pin = self.handoff(c, policy=self.policy(c, prep=pr))
        st = rec['srb_rot_report']
        rep = read_json(st['report']) if st.get('report') else {}
        want = self.srb_oracle(c, pr['rebuild_exports'])
        got = rep.get('bound_km_s') or []
        close = len(got) == N and all(g is not None and abs(g - w) <= 1e-12 * w for g, w in zip(got, want))
        summ = read_json(rec['root_summary'])
        banned = [k for k in ('ratio_to_tau', 'pass_tau_over_10', 'verdict', 'reading', 'pass') if k in rep]
        ok = (st['status'] == 'COMPUTED' and st['label'] == 'report-only: no registered NGC tau' and st['gates'] is False
              and rep.get('label') == st['label'] and rep.get('gates') is False and close and not banned
              and rec['reading'] == 'ACCEPTED' and not floats_outside_flags(rec) and not floats_outside_flags(summ)
              and summ['srb_rot_report'] == {'label': st['label'], 'gates': False, 'status': 'COMPUTED', 'code': None}
              and rep['library']['sha256'] == self.A.LIBRARY[1] and rep['row_producer']['sha256'] == ROW_PRODUCER[1])
        return ok, {'status': st['status'], 'close': close, 'banned_keys': banned,
                    'first': [got[:2], want[:2]] if got else None}

    def p32(self):
        """A162 item 5: SRB-ROT never gates: a bound 1e12 times larger, and a missing certificate, leave the reading
        ACCEPTED and member_lo_ok true."""
        out = {}
        c = self.fx.make_call('p32_big', cert_eps_scale=1.0e12)
        rec, _ = self.handoff(c)
        rep = read_json(rec['srb_rot_report']['report']) if rec['srb_rot_report'].get('report') else {}
        out['huge_bound'] = (rec['reading'] == 'ACCEPTED' and rec['member_lo_ok'] is True
                             and rec['srb_rot_report']['status'] == 'COMPUTED'
                             and max(b for b in rep.get('bound_km_s', [0.0]) if b is not None) > 1.0e3)
        c2 = self.fx.make_call('p32_nocert')
        rec2, _ = self.handoff(c2, policy=self.policy(c2, eps_certificate=None))
        out['no_certificate'] = (rec2['reading'] == 'ACCEPTED' and rec2['srb_rot_report']['status'] == 'UNAVAILABLE'
                                 and 'NO_POINT_CERTIFICATE' in str(rec2['srb_rot_report']['code']))
        return all(out.values()), out

    def p33(self):
        """A162 item 6: the S2 constants read PENDING in the module; with root-pinned (here synthetic) producer shas the
        S2 interface accepts the slot proof and rho producer and the call reads ACCEPTED."""
        c = self.fx.make_call('p33')
        rec, _ = self.handoff(c)
        ok = (self.H.S2_PINS == {'rho_producer_sha256': 'PENDING', 'slot_proof_producer_sha256': 'PENDING'}
              and rec['s2'] == 'PINNED' and rec['reading'] == 'ACCEPTED'
              and rec['pins']['s2'] == self.s2_synthetic(c))
        return ok, {'module_s2': self.H.S2_PINS, 'reading': rec['reading']}

    def p34(self):
        """A162 item 2 / A153 S5: the accepted state is never rebuilt; its input comes from the call's own manifest, and
        every other consumed state's from a verified S5 export (one each)."""
        c = self.fx.make_call('p34')
        pr = self.prep(c)
        d = c['digests']
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr))
        call_rec = read_json(rec['lo_adapter_call_record'])
        ok = (d['A'] not in pr['admissions'] and d['A'] not in pr['rebuild_exports'] and rec['reading'] == 'ACCEPTED'
              and all(rec['rebuild_exports'][x]['admission'] == pr['admissions'][x] for x in (d['B'], d['I'], d['N']))
              and call_rec['call_lo_reading'] == 'PASS')
        return ok, {'admissions': len(pr['admissions']), 'exports': len(pr['rebuild_exports'])}

    def p35(self):
        """A167: at a point whose theta route (s*ge)*EB differs from the spec route s*(ge*EB) in the last bit, the honest
        states (at the spec route, the gamma the call runs at) read PASS; the theta-route bits are a recorded diagnostic."""
        c = self.fx.make_call('p35', point=1)
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        gs = [read_json(s[k]['record'])['gamma_c4b'] for k in STATES]
        ok = (rec['call_lo_reading'] == 'PASS' and all(s[k]['verdict'] == 'PASS' for k in STATES)
              and all(g['bits_equal'] is True and g['theta_route_bits_equal_diagnostic'] is False
                      and g['state_gamma_eff_hex'] == g['spec_route_gamma_eff_hex'] != g['theta_route_gamma_eff_hex'] for g in gs))
        return ok, {'call': rec['call_lo_reading'], 'c4b': gs[0]}

    # ================================================================ MUST_FAIL (ported c2v002)
    def f01(self):
        out = {}
        for v in ('ddo_schema', 'ddo_producer', 'recompute_ddo'):
            c = self.fx.make_call('f01_' + v, rho=v)
            rec, _ = self.adapt(c)
            out[v] = (self.all_codes(rec, 'NGC_RHO_RECORD_MISMATCH'), [s['codes'] for s in rec['states']][:1],
                      (rec['blockers'] or [None])[0])
        return all(x[0] for x in out.values()), out

    def f02(self):
        c = self.fx.make_call('f02', rho='cert')
        rec, _ = self.adapt(c)
        ok = self.all_codes(rec, 'NGC_RHO_RECORD_MISMATCH') and 'CERTIFICATE_PARSED_AS_RHO_REFUSED' in rec['blockers'][0]
        return ok, rec['blockers']

    def f03(self):
        e91 = [float(x) for x in range(2, 92)]
        c = self.fx.make_call('f03', edges={'B': e91})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        c2 = self.fx.make_call('f03b', edges={'B': e91}, record_overrides={'B': {'outer': {'shape': 'cylinder',
                                                                                         'K_big_inverse_kpc': 64.0}}})
        rec2, _ = self.adapt(c2)
        s2 = self.by_state(rec2, c2)
        ok = (s['B']['codes'] == ['STATE_GEOMETRY_MISMATCH'] and s2['B']['codes'] == ['STATE_GEOMETRY_MISMATCH']
              and rec['call_lo_reading'] == 'INCOMPLETE' and rec2['call_lo_reading'] == 'INCOMPLETE')
        return ok, {'outer32_edges_to_91': s['B']['codes'], 'outer64': s2['B']['codes']}

    def f04(self):
        np, A = self.fx.np, self.A
        e = np.arange(2.0, 96.0)
        b1 = np.zeros(len(e) - 1)
        b1[91] = 1.0
        rows = [{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 1.0, 'R': 1.0}]
        agg, v1 = self.agg(rows, b1, e)
        e2 = np.asarray([2.0, 2.5, 3.5, 4.0, 6.0, 8.0, 12.0, 16.0, 32.0, 47.0])
        agg2, v2 = self.agg(rows, np.ones(len(e2) - 1), e2)
        ok = (v1[:2] == ('UNAVAILABLE', ['LO_SHELL_COVERAGE_INCOMPLETE']) and agg['coverage_flags']['nonzero_B1_above_91']
              and v2[:2] == ('UNAVAILABLE', ['LO_SHELL_COVERAGE_INCOMPLETE']))
        return ok, {'above91': [v1[0], v1[1], agg['coverage_problem']], 'straddle': [v2[0], v2[1], agg2['coverage_problem']]}

    def f05(self):
        c = self.fx.make_call('f05', record_overrides={'B': {'outer': {'shape': 'cylinder', 'K_big_inverse_kpc': 16.0}},
                                                       'I': {'kept': {'shape': 'cube', 'K_inverse_kpc': 4.0}}})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        ok = s['B']['codes'] == ['STATE_GEOMETRY_MISMATCH'] and s['I']['codes'] == ['STATE_GEOMETRY_MISMATCH'] \
            and s['A']['verdict'] == 'PASS' and rec['call_lo_reading'] == 'INCOMPLETE'
        return ok, {k: s[k]['codes'] for k in STATES}

    def f06(self):
        c = self.fx.make_call('f06', gamma_ulp={'B': 1})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        c2 = self.fx.make_call('f06b', point=1, gamma_route='theta')   # A167: the theta route never substitutes
        rec2, _ = self.adapt(c2)
        ok = (s['B']['codes'] == ['NGC_GAMMA_ROUTE_BITS_DIFFER'] and s['A']['verdict'] == 'PASS'
              and all(x['codes'] == ['NGC_GAMMA_ROUTE_BITS_DIFFER'] for x in rec2['states'])
              and rec['call_lo_reading'] == rec2['call_lo_reading'] == 'INCOMPLETE')
        return ok, {'state_ulp': s['B']['codes'], 'states_at_theta_route': [x['codes'] for x in rec2['states']]}

    def f07(self):
        c = self.fx.make_call('f07', X={'SYNQ-43': {'reason': 'QUERY_BEYOND_OUTER_GAS_CUT', 'earlier': BASE_V[42] * 50.0}})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        r = read_json(s['A']['record'])
        row = [x for x in r['rows']['rows'] if x['id'] == 'SYNQ-43'][0]
        ok = (row['status'] == 'INCLUDED' and s['A']['verdict'] == 'FAIL' and rec['call_lo_reading'] == 'NON_LAPSE_TAIL_MATERIAL'
              and 'SYNQ-43' in r['rows_in_arithmetic'])
        return ok, {'row': row['status'], 'A': s['A']['verdict'], 'call': rec['call_lo_reading']}

    def f08(self):
        c = self.fx.make_call('f08', missing_pass_rows=[1])
        rec, _ = self.adapt(c)
        st = rec['readout_diagnostic']['pass_row_list_status']
        ok = (self.all_codes(rec, 'READOUT_NOT_RECORDED') and rec['call_lo_reading'] != 'PASS'
              and st == ['RECORDED', 'NOT_OBSERVED', 'RECORDED'])
        return ok, {'codes': [s['codes'] for s in rec['states']], 'call': rec['call_lo_reading'], 'pass_status': st}

    def f09(self):
        out = {}
        for v in ('sigma', 'tau'):
            c = self.fx.make_call('f09_' + v, contract=v)
            rec, _ = self.adapt(c)
            out[v] = (self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
                      and 'CARRIES_VELOCITY_SIGMA_OR_TAU' in (rec['blockers'] or [''])[0], rec['blockers'][:1])
        return all(x[0] for x in out.values()), out

    def f10(self):
        out = {}
        for v in ('no_rule', 'rule_other'):
            c = self.fx.make_call('f10_' + v, contract=v)
            rec, _ = self.adapt(c)
            out[v] = self.all_codes(rec, 'NGC_LO_TOLERANCE_NOT_DECLARED') and rec['t_rule_id'] == self.A.RULE_ID
        c = self.fx.make_call('f10_noentry')
        rec, _ = self.adapt(c, registry=dict(self.fx.registry, t_i_entry=None))
        det = [read_json(s['record'])['detail'] for s in rec['states']]
        out['no_root_entry'] = (self.all_codes(rec, 'NGC_LO_TOLERANCE_NOT_DECLARED') and rec['t_rule_id'] is None
                                and 'point_sha256' not in rec and 'row_contract' not in rec
                                and all(any('no root t_i entry is pinned' in x for x in d) for d in det))
        c = self.fx.make_call('f10_entry_without_rule')
        rec, _ = self.adapt(c, registry=dict(self.fx.registry, t_i_entry=dict(self.fx.tie_without_rule)))
        out['entry_without_the_rule'] = (rec['call_lo_reading'] == 'INCOMPLETE' and not rec['states']
                                         and 'not found verbatim' in (rec['blockers'] or [''])[0])
        return all(out.values()), out

    def f11(self):
        A = self.A
        c = self.fx.make_call('f11')
        rec, _ = self.adapt(c)
        base = read_json(self.by_state(rec, c)['A']['record'])
        refused = {}
        for name, mut in (('reading', {'reading': 'ANCHOR_LO_FAILURE_PRESERVED_STEP4_STOPS_FOR_ROOT', 'verdict': 'FAIL',
                                       'fail_text': A.FAIL_TEXT}),
                          ('class', {'state_class': 'ANCHOR'}), ('is_anchor', {'is_anchor': True})):
            try:
                A.guard_state_record(dict(base, **mut))
                refused[name] = False
            except A.Refusal:
                refused[name] = True

        def anchor_adapter(**kw):
            r = A._adapt_call(env=self.env(c), **{k: v for k, v in kw.items() if k != 'rho_producer_ref'})
            r['call_lo_reading'] = 'ANCHOR_LO_FAILURE_PRESERVED_STEP4_STOPS_FOR_ROOT'
            return r
        hrec, _ = self.handoff(c, adapter_fn=anchor_adapter, tag='handoff_anchor')
        refused['handoff'] = hrec['reading'] == 'INCOMPLETE' and any('ANCHOR_CLASS_EMITTED' in b for b in hrec['blockers'])
        return all(refused.values()), refused

    def f12(self):
        A = self.A
        c = self.fx.make_call('f12', scales={'B': 10.0})
        rec, _ = self.adapt(c)
        b = read_json(self.by_state(rec, c)['B']['record'])
        refused = {}
        for name, mut in (('no_scope', {'scope_disclosure': None}), ('scope_altered', {'scope_disclosure': A.SCOPE_DISCLOSURE[:-1]}),
                          ('no_fail_text', {'fail_text': None}), ('no_pass_meaning', {'pass_meaning': None})):
            try:
                A.guard_state_record(dict(b, **mut))
                refused[name] = False
            except A.Refusal:
                refused[name] = True
        try:
            A.write_state_record(dict(b, scope_disclosure=None), os.path.join(c['base'], 'adapt'))
            refused['writer'] = False
        except A.Refusal:
            refused['writer'] = True

        def strip_adapter(**kw):
            r = A._adapt_call(env=self.env(c), **{k: v for k, v in kw.items() if k != 'rho_producer_ref'})
            for s in r['states']:
                if s['verdict'] == 'FAIL':
                    body = read_json(s['record'])
                    body.pop('scope_disclosure')
                    s['record'] = put_json(os.path.join(c['base'], 'stripped_%s.json' % s['state']['state_sha256'][:8]), body)
            return r
        hrec, _ = self.handoff(c, adapter_fn=strip_adapter, tag='handoff_strip')
        refused['handoff'] = (hrec['reading'] == 'INCOMPLETE' and
                              any(e['codes'] == ['NGC_LO_ADAPTER_NOT_ADMITTED'] and e['verdict'] == 'UNAVAILABLE'
                                  for e in hrec['states']))
        c2 = self.fx.make_call('f12_meaning')

        def meaning_adapter(**kw):
            r = A._adapt_call(env=self.env(c2), **{k: v for k, v in kw.items() if k != 'rho_producer_ref'})
            r.pop('pass_meaning')
            return r
        hrec2, _ = self.handoff(c2, adapter_fn=meaning_adapter, tag='handoff_meaning')
        refused['handoff_pass_meaning'] = (hrec2['reading'] == 'INCOMPLETE' and hrec2['member_lo_ok'] is False
                                           and any('E_A155_1_PASS_MEANING' in x for x in hrec2['blockers']))
        return all(refused.values()), refused

    def f13(self):
        c = self.fx.make_call('f13')
        rec, _ = self.adapt(c, review=False)
        return self.all_codes(rec, 'ROW_REFERENCE_POLICY_NOT_REVIEWED'), [s['codes'] for s in rec['states']]

    def f14(self):
        c = self.fx.make_call('f14', rho='ulp')
        rec, _ = self.adapt(c)
        return self.all_codes(rec, 'NGC_RHO_RECORD_MISMATCH'), [s['codes'] for s in rec['states']]

    def f15(self):
        out = {}
        for v in ('order', 'R_off'):
            c = self.fx.make_call('f15_' + v, contract=v)
            rec, _ = self.adapt(c)
            out[v] = self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
        c = self.fx.make_call('f15_support', support_radius_off=True)
        rec, _ = self.adapt(c)
        out['own_support'] = self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
        return all(out.values()), out

    def f16(self):
        c = self.fx.make_call('f16', tamper_arrays=['B'])
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        det = read_json(s['B']['record'])['detail']
        ok = (s['B']['codes'] == ['NGC_STATE_INPUT_UNAVAILABLE'] and rec['call_lo_reading'] == 'INCOMPLETE'
              and any('TAILSTATE_DIGEST_NOT_THE_RECORDED_DIGEST' in x for x in det))
        return ok, {'codes': s['B']['codes'], 'detail': det[:1]}

    def f17(self):
        c = self.fx.make_call('f17')
        rec, _ = self.adapt(c, rebuild_ok=False)
        s = self.by_state(rec, c)
        ok = (s['B']['codes'] == s['I']['codes'] == s['N']['codes'] == ['NGC_STATE_INPUT_UNAVAILABLE']
              and s['A']['verdict'] == 'PASS')
        return ok, {k: s[k]['codes'] for k in STATES}

    def f18(self):
        c = self.fx.make_call('f18', iterates=False)
        inv = self.inventory(c)
        out_root = os.path.join(c['base'], 'adapt')
        os.makedirs(out_root)
        rec = self.A._adapt_call(call_dir=c['call_dir'], spec_ref=c['spec_ref'], inventory=inv, state_inputs={},
                                 row_contract_ref=c['contract'], row_policy_review_ref=c['review'],
                                 slot_proof_ref=c['rho']['proof'], approved_producer_sha256=[self.shas['A']],
                                 approved_slot_proof_producer_sha256=[], approved_rho_producer_sha256=[],
                                 approved_rebuild_producer_sha256=[], trusted_row_policy_review_sha256=[],
                                 out_root=out_root, env=self.env(c))
        ok = (inv['complete'] is False and rec['call_lo_reading'] == 'INCOMPLETE' and not rec['states']
              and any('COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED' in b for b in rec['blockers']))
        return ok, {'inventory_blockers': inv['blockers'], 'call': rec['call_lo_reading']}

    def f19(self):
        c = self.fx.make_call('f19')
        rec, _ = self.adapt(c, approved=[])
        return rec['call_lo_reading'] == 'INCOMPLETE' and not rec['states'] and 'NOT_APPROVED' in rec['blockers'][0], \
            rec['blockers'][:1]

    def f20(self):
        A = self.A
        out = {}
        for k in ('driver', 's0', 'launch', 'manifest'):
            reg = dict(self.fx.registry)
            reg[k] = dict(A.real_registry()[k])
            try:
                A.check_registry(reg)
                out[k] = False
            except A.Refusal:
                out[k] = True
        for k, v in (('a153', dict(A.A153)), ('t_i_entry', dict(A.T_I_ENTRY))):
            try:
                A.check_registry(dict(self.fx.registry, **{k: v}))
                out[k] = False
            except A.Refusal:
                out[k] = True
        return all(out.values()), out

    def f21(self):
        c = self.fx.make_call('f21', b1_perturb=['B'])
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        np, A, U = self.fx.np, self.A, self.U
        record, arrays = c['states']['B'][0], dict(c['states']['B'][1])
        si = arrays['shell_integrals'].copy()
        si[np.flatnonzero(si[:, 1])[0], 1] *= (1 + 1e-9)
        arrays['shell_integrals'] = si
        try:
            A.recompute_b1(arrays, record, U)
            direct = False
        except A.Refusal as exc:
            direct = exc.code == 'NGC_STATE_INPUT_UNAVAILABLE' and 'does not reproduce' in str(exc)
        ok = s['B']['codes'] == ['NGC_STATE_INPUT_UNAVAILABLE'] and direct
        return ok, {'state': s['B']['codes'], 'direct_check': direct}

    def f22(self):
        out = {}
        for v in ('covers', 'g4false'):
            c = self.fx.make_call('f22_' + v, rho=v)
            rec, _ = self.adapt(c)
            out[v] = self.all_codes(rec, 'NGC_RHO_RECORD_MISMATCH')
        return all(out.values()), out

    def f23(self):
        c = self.fx.make_call('f23')
        bad = put_json(os.path.join(c['base'], 'receipt_running.json'), {'status': 'RUNNING', 'driver_status': 'COMPLETED',
                                                                         'result': {'sha256': c['result']['sha256']}})
        rec, pin = self.handoff(c, policy=self.policy(c, prep=False, receipt=bad))
        return rec['reading'] == 'INCOMPLETE' and 'FINISHED_RECEIPT_REQUIRED' in rec['blockers'], rec['blockers'][:2]

    def f24(self):
        c = self.fx.make_call('f24', kept_claim={'B': {'shape': 'cube', 'K_inverse_kpc': 4.0}})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        return s['B']['codes'] == ['STATE_GEOMETRY_MISMATCH'], s['B']['codes']

    def f25(self):
        c = self.fx.make_call('f25')
        old = os.environ.get('OMP_NUM_THREADS')
        os.environ['OMP_NUM_THREADS'] = '4'
        try:
            rec, _ = self.adapt(c)
        finally:
            os.environ['OMP_NUM_THREADS'] = old
        ok = self.all_codes(rec, 'NGC_RHO_RECORD_MISMATCH') and all('BLAS_NOT_SINGLE_THREAD' in read_json(s['record'])['detail'][0]
                                                                      for s in rec['states'])
        return ok, [s['codes'] for s in rec['states']]

    def f26(self):
        A = self.A
        out = {}
        allx = {q: {'reason': A.AUTHORIZED_INVALID_REASONS[i % 3], 'earlier': None} for i, q in enumerate(IDS)}
        for v, extra, layer in (('t_values', {}, 'CARRIES_VELOCITY_SIGMA_OR_TAU'),
                                ('t_none_values', {'X': allx}, 'CARRIES_VELOCITY_SIGMA_OR_TAU'),
                                ('velocity', {}, 'CARRIES_VELOCITY_SIGMA_OR_TAU'),
                                ('c2v001_shape', {}, 'CARRIES_VELOCITY_SIGMA_OR_TAU'),
                                ('t_plain', {}, 'ROW_CONTRACT_FIELDS')):
            c = self.fx.make_call('f26_' + v, contract=v, **extra)
            rec, _ = self.adapt(c)
            out[v] = (self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH') and layer in (rec['blockers'] or [''])[0],
                      (rec['blockers'] or [None])[0])
        c = self.fx.make_call('f26_record')
        rec, _ = self.adapt(c)
        body = read_json(self.by_state(rec, c)['A']['record'])
        rows = body['rows']['rows']
        try:
            A.guard_state_record(dict(body, rows=dict(body['rows'], rows=[dict(rows[0], t_km_s=1.0)] + rows[1:])))
            out['record_with_t_km_s'] = False
        except A.Refusal:
            out['record_with_t_km_s'] = True
        return all(x if isinstance(x, bool) else x[0] for x in out.values()), out

    def f27(self):
        out = {}
        c = self.fx.make_call('f27_theta', contract='theta_ulp')
        rec, _ = self.adapt(c)
        out['theta_ulp'] = (self.all_codes(rec, 'NGC_LO_TOLERANCE_RULE_MISMATCH')
                            and 'contract theta bits' in (rec['blockers'] or [''])[0])
        c = self.fx.make_call('f27_c', contract='c_ulp')
        rec, _ = self.adapt(c)
        out['contract_c_ulp'] = (self.all_codes(rec, 'NGC_LO_TOLERANCE_RULE_MISMATCH')
                                 and 'contract c bits' in (rec['blockers'] or [''])[0])
        c = self.fx.make_call('f27_state_c', record_overrides={'B': {'c_m_s': math.nextafter(self.A.C_M_S, math.inf)}})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        out['state_c_ulp'] = (s['B']['codes'] == ['NGC_LO_TOLERANCE_RULE_MISMATCH'] and s['A']['verdict'] == 'PASS'
                              and rec['call_lo_reading'] == 'INCOMPLETE')
        c = self.fx.make_call('f27_noncanonical', contract='theta_noncanonical')
        rec, _ = self.adapt(c)
        out['theta_noncanonical_hex'] = self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
        c = self.fx.make_call('f27_partial', contract='rule_partial')
        rec, _ = self.adapt(c)
        out['rule_keys_partial'] = self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
        return all(out.values()), out

    def f28(self):
        out = {}
        c = self.fx.make_call('f28_contract', contract='nmin')
        rec, _ = self.adapt(c)
        out['contract_N_min'] = self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
        c = self.fx.make_call('f28_oracle')
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        bad = self.oracle_mismatch(s['A']['record'])
        out['g_equals_oracle_no_factor'] = rec['call_lo_reading'] == 'PASS' and not bad
        return all(out.values()), dict(out, oracle_mismatches=bad[:3])

    def f29(self):
        out = {}
        c = self.fx.make_call('f29_contract', contract='ks')
        rec, _ = self.adapt(c)
        out['contract_per_shell_scale'] = (self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
                                           and 'ROW_CONTRACT_FIELDS' in (rec['blockers'] or [''])[0])
        c = self.fx.make_call('f29_oracle', scales={'B': 3.0})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        bad = [x for k in STATES for x in self.oracle_mismatch(s[k]['record'])]
        out['per_shell_g_equals_oracle'] = not bad
        return all(out.values()), dict(out, oracle_mismatches=bad[:3])

    def f30(self):
        out = {}
        c = self.fx.make_call('f30_contract', contract='eps')
        rec, _ = self.adapt(c)
        out['contract_eps'] = self.all_codes(rec, 'NGC_ROW_CONTRACT_MISMATCH')
        c = self.fx.make_call('f30_rows', eps_rows=True)
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        bad = self.oracle_mismatch(s['A']['record'])
        out['eps_rows_never_read'] = rec['call_lo_reading'] == 'PASS' and not bad
        return all(out.values()), dict(out, oracle_mismatches=bad[:3])

    def f31(self):
        A = self.A
        out = {}
        zero = [0, 1, 2, 3, 4]
        c = self.fx.make_call('f31', zero_speed=zero)
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        r = read_json(s['A']['record'])
        ids = [IDS[i] for i in zero]
        pos = [r['rows_in_arithmetic'].index(q) for q in ids if q in r['rows_in_arithmetic']]
        zg = [sh['per_row_g'][j] for sh in r['shells'] for j in pos]
        out['call'] = (rec['call_lo_reading'] == 'PASS' and len(pos) == len(ids) and zg and all(x == 0.0 for x in zg)
                       and all(math.isfinite(x) for sh in r['shells'] for x in sh['per_row_g'])
                       and r['zero_speed_rows'] == ids and r['diagnostic_flags'] == ['ZERO_SPEED_ROW']
                       and all(read_json(s[k]['record'])['diagnostic_flags'] == ['ZERO_SPEED_ROW'] for k in STATES))
        rows = [{'id': 'z%d' % i, 'status': A.ROW_INCLUDED, 'v': 0.0, 'R': 1.0e21} for i in range(3)]
        try:
            agg, dec = self.agg(rows, edges=None)
            out['aggregate_all_zero'] = dec[:2] == ('PASS', []) and agg['G'] == 0.0 and agg['zero_speed_rows'] == ['z0', 'z1', 'z2']
        except Exception as exc:
            out['aggregate_all_zero'] = 'RAISED %s: %s' % (type(exc).__name__, exc)
        return all(x is True for x in out.values()), out

    def f32(self):
        A = self.A
        out = {}
        allx = {q: {'reason': A.AUTHORIZED_INVALID_REASONS[i % 3], 'earlier': None} for i, q in enumerate(IDS)}
        c = self.fx.make_call('f32_allx', X=allx)
        rec, _ = self.adapt(c)
        recs = [read_json(s['record']) for s in rec['states']]
        out['adapter_all_rows_excluded'] = (self.all_codes(rec, 'LO_ROW_SET_EMPTY') and rec['row_statuses'] ==
                                            {'INCLUDED': 0, 'EXCLUDED_REGISTERED_MISS': N, 'MISSING': 0}
                                            and all(r['G'] is None and r['rows_in_arithmetic'] == [] for r in recs))
        hrec, _ = self.handoff(c, tag='handoff_allx')
        out['handoff_not_accepted'] = hrec['reading'] == 'INCOMPLETE' and hrec['member_lo_ok'] is False
        rows = [{'id': q, 'status': A.ROW_EXCLUDED, 'v': None, 'R': 1.0e20} for q in IDS]
        agg, dec = self.agg(rows)
        out['aggregate_decide'] = dec[:2] == ('UNAVAILABLE', ['LO_ROW_SET_EMPTY']) and agg['G'] is None
        agg0, dec0 = self.agg([])
        out['aggregate_no_rows_at_all'] = dec0[:2] == ('UNAVAILABLE', ['LO_ROW_SET_EMPTY'])
        c2 = self.fx.make_call('f32_guard')
        rec2, _ = self.adapt(c2)
        body = read_json(self.by_state(rec2, c2)['A']['record'])
        for name, mut in (('pass_with_empty_arithmetic', {'rows_in_arithmetic': []}), ('pass_without_G', {'G': None}),
                          ('pass_with_G_zero_and_no_rows', {'rows_in_arithmetic': [], 'G': 0.0})):
            try:
                A.guard_state_record(dict(body, **mut))
                out['guard_' + name] = False
            except A.Refusal:
                out['guard_' + name] = True
        return all(out.values()), out

    def f33(self):
        A = self.A
        out = {}
        c = self.fx.make_call('f33', scales={'A': 1.0e6})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        out['large_state_A'] = (s['A']['verdict'] == 'FAIL' and s['A']['reading'] == 'NON_LAPSE_TAIL_MATERIAL'
                                and rec['call_lo_reading'] == 'NON_LAPSE_TAIL_MATERIAL')
        rows = [{'id': 'big', 'status': A.ROW_INCLUDED, 'v': 200.0, 'R': 1.0e21}]
        np = self.fx.np
        e = A.expected_unit_edges()
        b1 = np.zeros(len(e) - 1)
        b1[0] = 1.0e-18
        agg, dec = self.agg(rows, b1, e)
        out['large_R_rho_B1_aggregate'] = dec[0] == 'FAIL' and agg['shells'][0]['max_g'] > A.PER_SHELL_MAX
        return all(out.values()), out

    # ================================================================ MUST_FAIL (A162 additions)
    def f34(self):
        """A162 item 1: the reader refuses every sidecar custody gap (and the handoff then reads INCOMPLETE)."""
        R = self.R
        out = {}
        for v in ('gap', 'file_bytes', 'extra_iteration', 'elements_digest', 'identity_sha', 'record_differs', 'boundary',
                  'outside', 'outcome', 'finish_sha', 'last_current'):
            c = self.fx.make_call('f34_' + v, sidecar=v)
            ok, why = self.refused(lambda: R.enumerate_sidecar(c['call_dir'], driver_sha256=self.fx.registry['driver']['sha256']),
                                   R.Refusal)
            out[v] = (ok and 'ROUTE_A_SIDECAR_CUSTODY' in str(why), why)
        c = self.fx.make_call('f34_handoff', sidecar='gap')
        rec, _ = self.handoff(c, policy=self.policy(c, prep=False))
        out['handoff'] = (rec['reading'] == 'INCOMPLETE' and rec['member_lo_ok'] is False
                          and any(b.startswith('ROUTE_A_SIDECAR') for b in rec['blockers'])
                          and 'lo_adapter_call_record' not in rec, rec['blockers'][:2])
        return all(x[0] for x in out.values()), out

    def forged_list(self, c, pr, tag, mutate):
        lst = read_json(pr['route_a_iterates'])
        mutate(lst)
        return put_json(os.path.join(c['base'], 'forged_%s.json' % tag), lst)

    def f35(self):
        """A162 item 1: a forged iterate list (an iterate dropped, a wrong source, another producer) is refused, and the
        handoff then reads INCOMPLETE with the inventory incomplete."""
        R = self.R
        c = self.fx.make_call('f35')
        pr = self.prep(c)
        d = c['digests']
        drv = self.fx.registry['driver']['sha256']
        out = {}
        dropped = self.forged_list(c, pr, 'dropped', lambda x: x.update(occurrences=x['occurrences'][:3]))
        out['dropped_iterate'] = self.refused(lambda: R.verify_iterate_list(dropped, c['call_dir'], driver_sha256=drv), R.Refusal)
        wrong = self.forged_list(c, pr, 'wrong_source', lambda x: x['occurrences'][0].update(source_sha256=c['rosters']['N']))
        out['wrong_source'] = self.refused(lambda: R.verify_iterate_list(wrong, c['call_dir'], driver_sha256=drv), R.Refusal)
        other = self.forged_list(c, pr, 'other_producer', lambda x: x.update(producer=dict(self.fx.sidecar_reader)))
        out['other_producer'] = self.refused(lambda: R.verify_iterate_list(other, c['call_dir'], driver_sha256=drv), R.Refusal)
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr, route_a_iterates=dropped), tag='handoff_dropped')
        out['handoff'] = (rec['reading'] == 'INCOMPLETE' and rec['member_lo_ok'] is False and rec['inventory_complete'] is False
                          and any(b.startswith('ROUTE_A_ITERATE_LIST') for b in rec['blockers']), rec['blockers'][:2])
        _ = d
        return all(x[0] for x in out.values()), out

    def f36(self):
        """A162 item 1: no iterate list is written without an ADMITTED S5 admission for every non-accepted iterate."""
        R, S = self.R, self.S
        c = self.fx.make_call('f36')
        d = c['digests']
        drv = self.fx.registry['driver']['sha256']
        sdir = os.path.join(c['base'], 's5_f36')
        os.mkdir(sdir)
        enum = R.enumerate_sidecar(c['call_dir'], driver_sha256=drv)
        adm = {t['state']['state_sha256']: S.rebuild_admit(call_dir=c['call_dir'], target=t, recipe_ref=self.fx.recipe,
                                                           approved_recipe_sha256=[self.fx.recipe['sha256']], out_dir=sdir,
                                                           driver_sha256=drv) for t in R.s5_targets(enum)}
        out = {}
        out['missing_admission'] = self.refused(lambda: R.write_iterate_list(c['call_dir'], {d['I']: adm[d['I']]}, sdir,
                                                                             driver_sha256=drv), R.Refusal)
        sdir2 = os.path.join(c['base'], 's5_f36_bad')
        os.mkdir(sdir2)
        bad = S.rebuild_admit(call_dir=c['call_dir'], target=R.s5_targets(enum)[1], recipe_ref=self.fx.recipe,
                              approved_recipe_sha256=[], out_dir=sdir2, driver_sha256=drv)
        out['not_admitted_admission'] = self.refused(lambda: R.write_iterate_list(c['call_dir'], {d['I']: adm[d['I']],
                                                                                                  d['N']: bad}, sdir2,
                                                                                  driver_sha256=drv), R.Refusal)
        out['swapped_admission'] = self.refused(lambda: R.write_iterate_list(c['call_dir'], {d['I']: adm[d['N']],
                                                                                             d['N']: adm[d['I']]}, sdir2,
                                                                             driver_sha256=drv), R.Refusal)
        return all(x[0] for x in out.values()), out

    def f37(self):
        """A162 item 2: S5 admits nothing it cannot reproduce from the recorded roster; forged exports are dropped by
        the handoff and the call reads INCOMPLETE."""
        S, R = self.S, self.R
        drv = self.fx.registry['driver']['sha256']
        out = {}
        c = self.fx.make_call('f37')
        d, r = c['digests'], c['rosters']
        sdir = os.path.join(c['base'], 's5_f37')
        os.mkdir(sdir)
        tb = {'state': {'state_sha256': d['B'], 'source_sha256': r['B'], 'stage_kind': 'le_rotation'},
              'origin': {'kind': 'ROUTE_B_STAGE', 'stage': 'le3_rotation'}}

        def adm(target, recipe=None, approved=None, tag=None):
            p = os.path.join(sdir, tag)
            os.mkdir(p)
            return read_json(S.rebuild_admit(call_dir=c['call_dir'], target=target, recipe_ref=recipe or self.fx.recipe,
                                             approved_recipe_sha256=[(recipe or self.fx.recipe)['sha256']] if approved is None
                                             else approved, out_dir=p, driver_sha256=drv))
        a = adm(dict(tb, state=dict(tb['state'], source_sha256=r['I'])), tag='roster')
        out['roster_not_recorded'] = (a['admitted'] is False and a['codes'] == ['S5_ROSTER_NOT_THE_RECORDED_ROSTER'], a['codes'])
        a = adm(tb, approved=[], tag='recipe')
        out['recipe_not_approved'] = (a['admitted'] is False and a['codes'] == ['S5_RECIPE_NOT_APPROVED'], a['codes'])
        a = adm({'state': {'state_sha256': d['A'], 'source_sha256': r['A'], 'stage_kind': 'route_a'},
                 'origin': {'kind': 'ROUTE_A_ITERATE', 'iteration': 1, 'role': CURRENT}}, tag='accepted')
        out['accepted_state'] = (a['admitted'] is False and a['codes'] == ['S5_TARGET_IS_THE_ACCEPTED_STATE'], a['codes'])
        a = adm(tb, recipe=self.fx.raising_recipe, tag='raising')
        out['recipe_raises'] = (a['admitted'] is False and a['codes'] == ['S5_RECIPE_FAILED'], a['codes'])
        c2 = self.fx.make_call('f37_unrepro', record_overrides={'B': {'synthetic_override': 1}})
        sdir2 = os.path.join(c2['base'], 's5_unrepro')
        os.mkdir(sdir2)
        tb2 = dict(tb, state={'state_sha256': c2['digests']['B'], 'source_sha256': c2['rosters']['B'], 'stage_kind': 'le_rotation'})
        p = S.rebuild_admit(call_dir=c2['call_dir'], target=tb2, recipe_ref=self.fx.recipe,
                            approved_recipe_sha256=[self.fx.recipe['sha256']], out_dir=sdir2, driver_sha256=drv)
        a = read_json(p)
        refused_export = self.refused(lambda: S.export_state_input(admission_ref=p, state=tb2['state'], out_dir=sdir2), S.Refusal)
        out['unreproducible_state'] = (a['admitted'] is False and a['codes'] == ['S5_REBUILD_DIGEST_MISMATCH']
                                       and a['digest_equal'] is False and refused_export[0], a['codes'])
        # forged exports at the handoff: a direct (non-S5) export, and an S5-labelled input carrying another state's admission
        pr = self.prep(c)
        forged = dict(pr['rebuild_exports'])
        forged[d['B']] = c['exports'][d['B']]
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr, rebuild_exports=forged), tag='handoff_direct_export')
        s = self.by_state(rec, c)
        out['handoff_non_s5_export'] = (rec['reading'] == 'INCOMPLETE' and s['B']['codes'] == ['NGC_STATE_INPUT_UNAVAILABLE']
                                        and any(b.startswith('REBUILD_EXPORT_REFUSED') for b in rec['blockers']), s['B']['codes'])
        body = read_json(pr['rebuild_exports'][d['B']])
        body['admission'] = pr['admissions'][d['I']]
        swapped = put_json(os.path.join(c['base'], 'forged_s5_input_B.json'), body)
        forged2 = dict(pr['rebuild_exports'], **{d['B']: swapped})
        rec2, _ = self.handoff(c, policy=self.policy(c, prep=pr, rebuild_exports=forged2), tag='handoff_swapped_admission')
        out['handoff_wrong_admission'] = (rec2['reading'] == 'INCOMPLETE'
                                          and any('ADMISSION_NOT_THIS_STATE' in b or 'ADMISSION_TARGET' in b
                                                  for b in rec2['blockers']), rec2['blockers'][:1])
        body = read_json(pr['rebuild_exports'][d['B']])
        body.pop('admission')
        noadm = put_json(os.path.join(c['base'], 'forged_s5_input_B_noadm.json'), body)
        out['export_without_admission'] = self.refused(lambda: S.verify_export(noadm, call_result=c['result'], state=tb['state']),
                                                       S.Refusal)
        xdir = os.path.join(c['base'], 's5_f37_identity')
        os.mkdir(xdir)
        out['export_identity_mismatch'] = self.refused(
            lambda: S.export_state_input(admission_ref=pr['admissions'][d['I']], state=tb['state'], out_dir=xdir), S.Refusal)
        _ = R
        return all(x[0] for x in out.values()), out

    def f38(self):
        """A162 item 3: the contract refuses a velocity, t_i or sigma key, a moved radius and another order; the handoff
        refuses any contract other than the pinned one; the builder refuses a manifest that is not the target-free shape."""
        A, H, C = self.A, self.H, self.C
        out = {}
        base = read_json(dict(H.ROW_CONTRACT))
        reg = A.real_registry()
        reader = A.make_reader(reg)
        d = os.path.join(self.run_dir, 'f38')
        os.mkdir(d)

        def check(name, doc):
            pin = put_json(os.path.join(d, 'contract_%s.json' % name), doc)
            try:
                st = A.check_row_contract(pin, reg, reader, None, None, A.RULE_ID)[2]
                return False, st
            except A.Refusal as exc:
                return exc.code == 'NGC_ROW_CONTRACT_MISMATCH', str(exc)[:120]
        out['t_km_s'] = check('t', dict(base, t_km_s=[1.0e3] * 43))
        out['sigma'] = check('sigma', dict(base, sigma_km_s=[1.0] * 43))
        out['velocity'] = check('velocity', dict(base, v_reference_km_s=[100.0] * 43))
        out['radius_moved'] = check('radius', dict(base, R_m=[x * (1 + 1e-9) for x in base['R_m']]))
        out['order'] = check('order', dict(base, query_ids=list(reversed(base['query_ids']))))
        c = self.fx.make_call('f38_handoff')
        other = put_json(os.path.join(d, 'contract_copy.json'), base)
        rec, _ = self.handoff(c, policy=self.policy(c, prep=False), registry=reg, contract=other, s2=dict(H.S2_PINS),
                              tag='handoff_registered_contract')
        out['handoff_registered_other_contract'] = (rec['reading'] == 'INCOMPLETE'
                                                    and any('NOT_THE_PINNED' in b for b in rec['blockers']), rec['blockers'][:1])
        rec2, _ = self.handoff(c, policy=self.policy(c, prep=False, row_contract=other), tag='handoff_policy_contract')
        out['handoff_policy_other_contract'] = (rec2['reading'] == 'INCOMPLETE'
                                                and any('ROW_CONTRACT_NOT_THE_PINNED_CONTRACT' in b for b in rec2['blockers']),
                                                rec2['blockers'][:1])
        rows = [{'query_id': 'NGC3198-Q%02d' % (i + 1), 'Rad_text': RAD_TEXT[i], 'Rad_unit': 'kpc', 'data_row_index': i,
                 'source_line_number': i + 1} for i in range(43)]
        good = {'schema': C.MANIFEST_SCHEMA, 'emitted_columns': list(C.MANIFEST_COLUMNS), 'no_other_columns_emitted': True,
                'rows': rows}
        okm = put_json(os.path.join(d, 'syn_tfm_good.json'), good)
        built = C.build_contract(okm)
        out['builder_control_builds'] = (built['R_m'] == [float(x) * KPC_M for x in RAD_TEXT] and built['manifest'] == okm, None)
        for name, doc in (('velocity_column', dict(good, emitted_columns=list(C.MANIFEST_COLUMNS) + ['Vobs'])),
                          ('order', dict(good, rows=list(reversed(rows)))),
                          ('unit', dict(good, rows=[dict(rows[0], Rad_unit='arcsec')] + rows[1:])),
                          ('row_count', dict(good, rows=rows[:42]))):
            p = put_json(os.path.join(d, 'syn_tfm_%s.json' % name), doc)
            out['builder_' + name] = self.refused(lambda: C.build_contract(p), C.Refusal)
        out['builder_sha_mismatch'] = self.refused(lambda: C.build_contract(dict(okm, sha256='0' * 64)), C.Refusal)
        return all(x[0] for x in out.values()), out

    def f39(self):
        """A162 item 4: every execution fact not established, or established but disqualifying, refuses before the
        inventory (no LO number is computed) and the call reads INCOMPLETE."""
        out = {}
        cases = {'retries1': ('retried', True), 'two_route_a': ('retried', True), 'start_iter1': ('resumed', True),
                 'resume_flag': ('resumed', True), 'ckpt_resume': ('resumed', True), 'exit1': ('route_a_completed_normally', False),
                 'not_converged': ('route_a_completed_normally', False), 'conv_int': ('route_a_completed_normally', False),
                 'mode_admitted': ('fresh_call', False), 'finish_invalid': ('fresh_call', False), 'no_start': ('fresh_call', None),
                 'result_path': ('fresh_call', False), 'argv_missing': ('resumed', None)}
        for ev, (key, want) in cases.items():
            c = self.fx.make_call('f39_' + ev, exec=ev)
            rec, _ = self.handoff(c, policy=self.policy(c, prep=False), tag='handoff_exec')
            ex = rec['execution'] or {}
            out[ev] = (rec['reading'] == 'INCOMPLETE' and rec['member_lo_ok'] is False and ex.get(key) is want
                       and any('EXECUTION_FACTS_REFUSE' in b for b in rec['blockers']) and 'inventory' not in rec
                       and 'lo_adapter_call_record' not in rec, {key: ex.get(key)})
        for sv, key in (('reloaded', 'resumed'), ('finish_index', 'resumed')):
            c = self.fx.make_call('f39_side_' + sv, sidecar=sv)
            rec, _ = self.handoff(c, policy=self.policy(c, prep=False), tag='handoff_exec')
            ex = rec['execution'] or {}
            out['sidecar_' + sv] = (rec['reading'] == 'INCOMPLETE' and ex.get(key) is True
                                    and any('EXECUTION_FACTS_REFUSE' in b for b in rec['blockers']), {key: ex.get(key)})
        c = self.fx.make_call('f39_spec_admit', spec_overrides={'admit': {'route_a': 'x'}})
        rec, _ = self.handoff(c, policy=self.policy(c, prep=False), tag='handoff_exec')
        out['spec_admit'] = (rec['reading'] == 'INCOMPLETE' and (rec['execution'] or {}).get('fresh_call') is False,
                             (rec['execution'] or {}).get('fresh_call'))
        return all(x[0] for x in out.values()), out

    def f40(self):
        """A162 item 5: an SRB-ROT input that does not hold reads UNAVAILABLE in the report and never changes the
        reading (it never gates in either direction); the report carries no tau ratio or pass flag."""
        out = {}
        c = self.fx.make_call('f40')
        pr = self.prep(c)
        alt = os.path.join(c['base'], 'alt_certs')
        variants = {
            'other_point': (self.fx.make_cert(os.path.join(alt, 'other.json'), self.fx.keys[2]), 'CERT_OTHER_POINT'),
            'bad_producer': (self.fx.make_cert(os.path.join(alt, 'prod.json'), c['key'], producer='0' * 64),
                             'CERT_PRODUCER_NOT_REVIEWED'),
            'not_the_state_certificate': (self.fx.make_cert(os.path.join(alt, 'same_point.json'), c['key'], scale=2.0),
                                          'STAGE_EPS_PIN_NOT_THE_POINT_CERTIFICATE'),
            'anchor_role': (self.fx.make_cert(os.path.join(alt, 'anchor.json'), c['key'], role='anchor'),
                            'CERT_NOT_A_POINT_RECORD')}
        for name, (cert, code) in variants.items():
            rec, _ = self.handoff(c, policy=self.policy(c, prep=pr, eps_certificate=cert), tag='handoff_srb_' + name)
            st = rec['srb_rot_report']
            out[name] = (rec['reading'] == 'ACCEPTED' and st['status'] == 'UNAVAILABLE' and code in str(st['code'])
                         and st['report'] is None and st['gates'] is False, st['code'])
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr), tag='handoff_srb_ok')
        rep = read_json(rec['srb_rot_report']['report'])
        out['no_tau_ratio_or_pass_flag'] = (not any(k in rep for k in ('ratio_to_tau', 'pass_tau_over_10', 'verdict', 'reading'))
                                            and rep['discarded'] == ['ratio_to_tau', 'pass_tau_over_10'], sorted(rep)[:6])
        return all(x[0] for x in out.values()), out

    def f41(self):
        """A162 item 6: S2 PENDING reads UNAVAILABLE; S2 approvals cannot come from policy; under the REGISTERED registry
        the S2 pins must be the module constants; a producer other than the pinned one is refused."""
        H = self.H
        out = {}
        c = self.fx.make_call('f41')
        pr = self.prep(c)
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr), s2=dict(H.S2_PINS), tag='handoff_s2_pending')
        out['pending'] = (rec['reading'] == 'INCOMPLETE' and rec['s2'] == 'PENDING'
                          and all(e['codes'] == ['NGC_RHO_RECORD_MISMATCH'] for e in rec['states'])
                          and any(b.startswith('S2_RHO_PINS_PENDING') for b in rec['blockers']), rec['blockers'][:1])
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr), s2=dict(self.s2_synthetic(c), rho_producer_sha256='0' * 64),
                              tag='handoff_s2_other')
        out['other_rho_producer'] = (rec['reading'] == 'INCOMPLETE'
                                     and all(e['codes'] == ['NGC_RHO_RECORD_MISMATCH'] for e in rec['states']), rec['blockers'][:1])
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr, approved_rho_producer_sha256=[c['rho']['producer']['sha256']]),
                              tag='handoff_s2_policy')
        out['policy_s2_approvals'] = (rec['reading'] == 'INCOMPLETE' and any('POLICY_KEYS' in b for b in rec['blockers']),
                                      rec['blockers'][:1])
        rec, _ = self.handoff(c, policy=self.policy(c, prep=False), registry=self.A.real_registry(),
                              contract=dict(H.ROW_CONTRACT), tag='handoff_s2_registered')
        out['registered_non_constant_s2'] = (rec['reading'] == 'INCOMPLETE'
                                             and any('S2_PINS_NOT_THE_MODULE_CONSTANTS' in b for b in rec['blockers']),
                                             rec['blockers'][:1])
        rec, _ = self.handoff(c, policy=self.policy(c, prep=pr), s2={'rho_producer_sha256': 'x', 'slot_proof_producer_sha256': 'y'},
                              tag='handoff_s2_malformed')
        out['malformed_s2'] = (rec['reading'] == 'INCOMPLETE' and any('S2_PINS_NOT_SHA_OR_PENDING' in b for b in rec['blockers']),
                               rec['blockers'][:1])
        return all(x[0] for x in out.values()), out

    def f42(self):
        """A167: the S2 interface pins Claude3's NGC rho c3v003 schema strings; c3v001-schema slot proof and rho records are
        refused (every state NGC_RHO_RECORD_MISMATCH)."""
        A = self.A
        c = self.fx.make_call('f42', rho='c3v001_schemas')
        rec, _ = self.adapt(c)
        consts = (A.SLOT_PROOF_SCHEMA, A.RHO_SCHEMA, A.RHO_IDENTITY_SCHEMA) == (
            'UNT_NGC_POINT_LO_SLOT_PROOF_C3V003', 'UNT_NGC_POINT_RHO_NUMERICAL_C3V003', 'UNT_NGC_POINT_RHO_IDENTITY_C3V003')
        ok = consts and self.all_codes(rec, 'NGC_RHO_RECORD_MISMATCH')
        return ok, {'constants_c3v003': consts, 'blockers': rec['blockers'][:1]}

    # ---------------------------------------------------------------- run
    def all(self):
        P = [('P01', 'enumerator: complete inventory, Q5 classes, inherited merged (4 states)', self.p01),
             ('P02', 'S4 at E_top 47: 7 tiled, (32,64] partial over (32,47], (64,91] NOT_IN_STATE_DOMAIN, G sums 9', self.p02),
             ('P03', 'S4 hi <= E_top exact tiling at E_top 64 and 91 (pure aggregate)', self.p03),
             ('P04', 'S6 |v_i| = max |speed| over every pass (negative readout)', self.p04),
             ('P05', 'S6 X row, authorized reason, no finite readout: excluded with reason', self.p05),
             ('P06', 'S6 X row with a finite readout in an earlier pass: included at that max', self.p06),
             ('P07', 'S6 X empty: the unchanged own_call_vmax', self.p07),
             ('P08', 'S6 monotone-FAIL: missing readout, present rows decide FAIL', self.p08),
             ('P09', 'S6 missing readout, no decided FAIL: READOUT_NOT_RECORDED', self.p09),
             ('P10', 'S6 set(pass.invalid_rows) == X recorded as a diagnostic', self.p10),
             ('P11', 'adapter PASS at every state; call PASS; no values or t_i in records; PASS meaning carried', self.p11),
             ('P12', 'route-B FAIL: NON_LAPSE_TAIL_MATERIAL with scope and FAIL text', self.p12),
             ('P13', 'iterate-only FAIL, others PASS: LO_UNCERTIFIED_TRANSIENT', self.p13),
             ('P14', 'iterate FAIL with a non-iterate UNAVAILABLE: INCOMPLETE', self.p14),
             ('P15', 'route-B FAIL decisive with another state UNAVAILABLE', self.p15),
             ('P16', 'public adapter entry (REGISTERED, A155 pinned): S1 refuses the fabricated label, nothing computed', self.p16),
             ('P17', 'handoff c2v003 end to end (reader + S5 inputs): ACCEPTED, member_lo_ok, blinded summary', self.p17),
             ('P18', 'handoff c2v003 public entry: INCOMPLETE at S1 custody, S2 PENDING, pins recorded', self.p18),
             ('P19', 'handoff NON_LAPSE_TAIL_MATERIAL: member invalid, rows not model output', self.p19),
             ('P20', 'C4b: state, spec-route and theta-route gamma bits recorded equal', self.p20),
             ('P21', 'rho 10-key equal and the B1 1e-10 check recorded', self.p21),
             ('P22', 'high-Q-inf flag recorded, reading unchanged', self.p22),
             ('P23', 'A155 ratio form equals an independent oracle at every row, shell and state; d/g = t_i', self.p23),
             ('P24', 'A155 monotone: g grows exactly as |v|^2', self.p24),
             ('P25', 'A162-1 reader: sidecar enumeration (current and monitor-next per iteration; accepted last)', self.p25),
             ('P26', 'A162-1 iterate list from S5 admissions: enumerator complete, classes, established sources', self.p26),
             ('P27', 'A162-2 S5: rebuilt from own rosters, admitted on digest equality, timed (U4), adapter PASS', self.p27),
             ('P28', 'A162 chain end to end: ACCEPTED with exports, list, execution facts and the SRB-ROT report', self.p28),
             ('P29', 'A162-3 the built NGC row contract: a2936517 radii/order, rule/theta/c hex, adapter BOUND', self.p29),
             ('P30', 'A162-4 execution facts recorded from the call own records and carried in the summary', self.p30),
             ('P31', 'A162-5 SRB-ROT computed via pinned srb_rot + rotation_rows, equals the oracle, report-only', self.p31),
             ('P32', 'A162-5 SRB-ROT never gates: a huge bound or a missing certificate leaves ACCEPTED', self.p32),
             ('P33', 'A162-6 S2 constants PENDING in the module; pinned producers accepted by sha', self.p33),
             ('P34', 'A162-2 the accepted state is never rebuilt; every other state has one verified S5 export', self.p34),
             ('P35', 'A167 C4b on the spec route: theta-route-differing point reads PASS; theta bits a diagnostic', self.p35)]
        F = [('F01', 'S13 rho from a1dcdea8 (slot schema, proof producer, recompute)', self.f01),
             ('F02', 'S13 the certificate parsed as a rho record', self.f02),
             ('F03', 'S13 the cylinder-64 partition assumed at outer 32 without S4', self.f03),
             ('F04', 'S13 nonzero B1 above 91 / outside exactly one rho shell', self.f04),
             ('F05', 'S13 outer != 32 or kept != {cube, 2.0}', self.f05),
             ('F06', 'S13 gamma bits differ (A167: state 1 ulp off the spec route; states at the theta route)', self.f06),
             ('F07', 'S13 a row in X with a finite readout excluded', self.f07),
             ('F08', 'S13 a missing pass row list read as PASS', self.f08),
             ('F09', 'S13 sigma or DDO tau present in the row contract', self.f09),
             ('F10', 'S13 t_i absent (contract without the rule, foreign rule id, no root entry, entry without the rule)', self.f10),
             ('F11', 'S13 an anchor class emitted', self.f11),
             ('F12', 'S13 a FAIL record without the scope text (and the PASS meaning)', self.f12),
             ('F13', 'S10 no row-policy review', self.f13),
             ('F14', 'S2 recompute 1 ulp off the slot rho', self.f14),
             ('F15', 'S7/S8 manifest order, contract R, own query support', self.f15),
             ('F16', 'S5 rebuild export digest mismatch', self.f16),
             ('F17', 'S5 rebuild producer not approved', self.f17),
             ('F18', 'S9 incomplete inventory (no iterate list)', self.f18),
             ('F19', 'adapter not in the approved list', self.f19),
             ('F20', 'synthetic registry touching a registered input', self.f20),
             ('F21', 'stored B1 does not reproduce (1e-9)', self.f21),
             ('F22', 'slot proof covers_all_consumed_states / G4 unproven', self.f22),
             ('F23', 'handoff without the FINISHED receipt', self.f23),
             ('F24', 'inventory kept claim not cube 2', self.f24),
             ('F25', 'rho recompute without single-thread BLAS', self.f25),
             ('F26', 'A155 t_i values or any velocity in the contract (and a record storing t_i)', self.f26),
             ('F27', 'A155 theta or c bits that differ from the contract (contract theta, contract c, state c)', self.f27),
             ('F28', 'A155 an N_min factor present (contract field; g against the oracle)', self.f28),
             ('F29', 'A155 a per-shell 1/k_s scale (contract field; per-shell g against the oracle)', self.f29),
             ('F30', 'A155 eps_km_s used as t_i (contract field; eps on the rows never read)', self.f30),
             ('F31', 'A155 |v_i| = 0 raising an error or producing a non-finite value', self.f31),
             ('F32', 'A155 an empty row set reading PASS (all 43 rows excluded; handoff; guard)', self.f32),
             ('F33', 'A155 a synthetic state with a large R*rho*B1 that does not FAIL', self.f33),
             ('F34', 'A162-1 sidecar custody gaps refused by the reader (and the handoff INCOMPLETE)', self.f34),
             ('F35', 'A162-1 forged iterate list (dropped iterate, wrong source, other producer)', self.f35),
             ('F36', 'A162-1 no iterate list without an ADMITTED S5 admission per iterate', self.f36),
             ('F37', 'A162-2 S5 refusals (roster, recipe, accepted state, unreproducible state, forged exports)', self.f37),
             ('F38', 'A162-3 contract with velocity/t_i/sigma, moved radius, other order, other contract; builder refusals', self.f38),
             ('F39', 'A162-4 execution facts not established or disqualifying refuse before the inventory', self.f39),
             ('F40', 'A162-5 SRB-ROT input refusals read UNAVAILABLE and never change the reading', self.f40),
             ('F41', 'A162-6 S2 PENDING, policy approvals, REGISTERED non-constant pins, another producer', self.f41),
             ('F42', 'A167 S2 schema strings *_C3V003: c3v001-schema slot proof and rho records refused', self.f42)]
        for rid, name, fn in P:
            self.run(rid + ' ' + name, 'MUST_PASS', fn)
        for rid, name, fn in F:
            self.run(rid + ' ' + name, 'MUST_FAIL', fn)
        return P, F


def is_pin_(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--module-dir', default=os.path.dirname(os.path.realpath(__file__)))
    ap.add_argument('--only', default=None, help='dev: comma-separated test ids')
    a = ap.parse_args(argv)
    for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        os.environ[k] = '1'
    run_dir = os.path.realpath(a.run_dir)
    os.mkdir(run_dir)
    t0 = time.monotonic()
    s = Suite(run_dir, os.path.realpath(a.module_dir))
    if a.only:
        want = set(a.only.split(','))
        orig = s.run
        s.run = lambda rid, kind, fn: orig(rid, kind, fn) if rid.split()[0] in want else None
    P, F = s.all()
    mp = [r for r in s.results if r['kind'] == 'MUST_PASS']
    mf = [r for r in s.results if r['kind'] == 'MUST_FAIL']
    out = {'schema': 'NGC_ACCEPTANCE_C2V003A_SUITE_RESULTS', 'synthetic_only': True, 'module_shas': s.shas,
           'library_sha256': s.A.LIBRARY[1], 'T_I_ENTRY_of_record_module': s.A.T_I_ENTRY, 'rule_id': s.A.RULE_ID,
           'theta_hex': s.A.THETA_HEX, 'handoff_pins': {'iterate_reader': s.H.ITERATE_READER, 's5_tool': s.H.S5_TOOL,
                                                       'row_contract': s.H.ROW_CONTRACT, 's2': s.H.S2_PINS},
           'art_patched_for_dev_run': s.art_patched, 'python': sys.version.split()[0],
           'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode},
           'only': a.only,
           'must_pass': '%d/%d' % (sum(r['ok'] for r in mp), len(mp)), 'must_fail': '%d/%d' % (sum(r['ok'] for r in mf), len(mf)),
           'results': s.results, 'seconds': round(time.monotonic() - t0, 3)}
    pin = put_json(os.path.join(run_dir, 'SUITE_RESULTS_C2V003A.json'), out)
    print(json.dumps({'must_pass': out['must_pass'], 'must_fail': out['must_fail'], 'results': pin,
                      'failed': [r['id'] for r in s.results if not r['ok']]}))
    return 0 if all(r['ok'] for r in s.results) else 1


if __name__ == '__main__':
    sys.exit(main())
