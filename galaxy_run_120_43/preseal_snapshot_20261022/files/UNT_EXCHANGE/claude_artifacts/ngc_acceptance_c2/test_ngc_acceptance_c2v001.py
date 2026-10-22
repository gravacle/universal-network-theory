"""Synthetic suite for the NGC per-state LO adapter, enumerator and handoff c2v001 (V006 A153; text of record 9916cb6f S13).

SYNTHETIC ONLY. Every call, state, rho record, slot proof, S0 point, spec, manifest, addendum and row contract here is
fabricated under a SYNTHETIC_TEST registry (refused at every registered input). The REGISTERED-registry tests run the
public entries on a fabricated call whose result names the registered driver sha as a string; they stop at the t_i gate
(T_I_ENTRY is None), so they read only the V006 A153 section and the text of record (both named), never a real call,
rho, S0 point, manifest row or target. No NGC3198-named file other than the V006 addendum is opened.

Usage: python3 -I -B test_ngc_acceptance_c2v001.py --run-dir <new dir> [--module-dir <dir>]
Writes SUITE_RESULTS_C2V001.json in the run dir (exclusive create). Exit 0 iff every MUST_PASS passes and every MUST_FAIL
fails closed.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import random
import sys
import time
import traceback

KPC_M = 3.085677581491367e19
NAMES = {'E': 'ngc_consumed_states_c2v001.py', 'A': 'ngc_lo_state_adapter_c2v001.py', 'H': 'ngc_acceptance_handoff_c2v001.py'}
REAL_DRIVER_SHA = '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'
N = 43
IDS = ['SYNQ-%02d' % (i + 1) for i in range(N)]
RAD_TEXT = ['%.3f' % (1.0 + 0.8 * i) for i in range(N)]
R_M = [float(x) * KPC_M for x in RAD_TEXT]
BASE_V = [100.0 + 2.0 * i for i in range(N)]
RHO_USED = [0.5, 0.4, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05, 0.02]
PARTITION = [[2.0, 3.0], [3.0, 4.0], [4.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
             [64.0, 91.0]]
KP_KPC = [0.5, 1.5, 2.5, 3.5, 5.0, 7.0, 10.0, 14.0, 20.0, 25.0, 30.0]
KZ_KPC = [0.5, 1.5, 2.5, 5.0, 10.0, 20.0, 25.0, 30.0]
TARGET_MAX_RATIO = 0.001


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


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


def put_npz(path, arrays):
    import numpy as np
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'wb') as f:
        np.savez(f, **arrays)
    return {'path': path, 'sha256': sha_file(path)}


def read_json(pin):
    with open(pin['path'], 'rb') as f:
        return json.loads(f.read())


def floats_outside_flags(obj, path=''):
    """S12 check: every non-integer number outside a coverage_flags block (whose only numbers are geometry: E_top and
    the registered shell ranges). Integers (counts) and booleans are not values."""
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

    def __init__(self, root, A, E, H, U):
        import numpy as np
        self.np, self.root, self.A, self.E, self.H, self.U = np, root, A, E, H, U
        reg = os.path.join(root, 'registry')
        v006 = '\n'.join(['# synthetic addendum (test only; not a root decision)', '', '## A152: synthetic', '', 'x', '',
                          '## A153: synthetic A153 (test only)', '', '- ' + A.SCOPE_DISCLOSURE, '',
                          '## A999: synthetic t_i entry (test only)', '', 'synthetic declared t_i', '',
                          '## A1000: end', '']).encode()
        v_pin = put_bytes(os.path.join(reg, 'syn_addendum.md'), v006)
        a153 = {'path': v_pin['path'], 'heading': '## A153',
                'section_sha256': hashlib.sha256(A.section_bytes(v006, '## A153')).hexdigest()}
        tie = {'path': v_pin['path'], 'heading': '## A999',
               'section_sha256': hashlib.sha256(A.section_bytes(v006, '## A999')).hexdigest()}
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
        self.rule_id = '%s@%s' % (tie['heading'], tie['section_sha256'])
        self.rebuild_producer = put_bytes(os.path.join(reg, 'syn_rebuild_producer.py'), b'# synthetic rebuild exporter\n')
        self.sidecar_reader = put_bytes(os.path.join(reg, 'syn_sidecar_reader.py'), b'# synthetic sidecar reader\n')
        self.slot_proof_producer = put_bytes(os.path.join(reg, 'syn_slot_proof_producer.py'), b'# synthetic slot proof\n')
        self.n = 0

    # ---------------------------------------------------------------- tail states
    def b1_unit(self, arrays, record):
        """Independent copy of the node-quadrature B1 (library build L757-783 / lo_core L118-129 arithmetic)."""
        np, U = self.np, self.U
        kp, kz, edges = arrays['kp'], arrays['kz'], arrays['shell_edges_inverse_kpc']
        pref = record['pref']
        out = np.zeros(len(edges) - 1)
        S = arrays['P'] @ arrays['F'].T
        c0 = U._c0_D(record['kept'], record['outer'], kp * U.KPC_M, kz * U.KPC_M)
        km = np.sqrt(kp[:, None] ** 2 + kz[None, :] ** 2)
        fac = (pref * arrays['wkp'] * kp)[:, None] * arrays['wz'][None, :] / km ** 2
        w = 2 * np.abs(S) * fac * c0 * km
        idx = np.clip(np.searchsorted(edges, km * U.KPC_M, side='right') - 1, 0, len(out) - 1)
        out += np.bincount(idx.ravel(), weights=w.ravel(), minlength=len(out))
        return out

    def tail(self, kind, roster, scale, gamma, overrides=None, edges=None):
        np, A = self.np, self.A
        kp = np.asarray(KP_KPC) / KPC_M
        kz = np.asarray(KZ_KPC) / KPC_M
        arrays = {'kp': kp, 'kz': kz, 'wkp': np.full(len(kp), 0.5 / KPC_M), 'wz': np.full(len(kz), 0.5 / KPC_M),
                  'P': np.full((len(kp), 1), float(scale)), 'F': np.full((len(kz), 1), 1.0 + 0.5j),
                  'shell_edges_inverse_kpc': A.expected_unit_edges() if edges is None else np.asarray(edges, float),
                  'ring_radii_m': np.asarray([1.0e20])}
        record = {'schema': 'UNT_UV_TAIL_STATE_C2V001', 'empty': False, 'kept': dict(A.KEPT), 'outer': dict(A.OUTER),
                  'stage_kind': kind, 'roster_digest': roster, 'lambda_scale': 1.0, 'gamma_eff': gamma,
                  'c_m_s': A.C_M_S, 'pref': 1.0 / (4 * gamma * (2 * math.pi) ** 3), 'lo_certificate': dict(self.launch),
                  'eps_certificate': 'SYNTHETIC', 'i1t': {'verdict': 'PASS'}, 'config_sha256': '0' * 64}
        record.update(overrides or {})
        b1 = self.b1_unit(arrays, record)
        si = np.zeros((len(arrays['shell_edges_inverse_kpc']) - 1, 3))
        si[:, 0], si[:, 1], si[:, 2] = 0.5 * b1, b1, 2.0 * b1
        arrays['shell_integrals'] = si
        d = self.U.TailState(empty=False, record=record, arrays=arrays).digest
        return record, arrays, d, b1

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
    def make_call(self, name, **o):
        np, A = self.np, self.A
        self.n += 1
        base = os.path.join(self.root, 'calls', name)
        out = os.path.join(base, 'call', 'out')
        point = o.get('point', 0)
        th, key = self.thetas[point], self.keys[point]
        s, ge, EB = th['common_scale_s'], th['gamma_over_Eref'], th['Eref_base_J']
        spec = {'galaxy': 'NGC3198', 'label': 'step5 A_K32_A2_HEADLINE theta_key=' + key,
                'physical': {'Eref_J': EB, 'ell_F_m': th['ell_F_m'], 'gamma': ge * EB, 'common_scale_s': s},
                'numerics': {'uv_tail': {'lo_certificate': dict(self.launch), 'outer': dict(A.OUTER), 'lambda_scale': 1.0},
                             'route_a': {'column_workers': 1}}}
        spec.update(o.get('spec_overrides') or {})
        spec_ref = put_json(os.path.join(base, 'spec.json'), spec)
        gamma = s * (ge * EB)                                    # the spec route (driver)
        rost = {k: hashlib.sha256(('%s-%s' % (name, k)).encode()).hexdigest() for k in 'ABI'}
        kinds = {'A': 'route_a', 'B': 'le_rotation', 'I': 'route_a'}
        scales = dict({'A': 1.0, 'B': 1.0, 'I': 0.9}, **(o.get('scales') or {}))
        st = {}
        for k in 'ABI':
            g = gamma + o.get('gamma_ulp', {}).get(k, 0) * math.ulp(gamma)
            st[k] = self.tail(kinds[k], rost[k], scales[k], g, (o.get('record_overrides') or {}).get(k),
                              (o.get('edges') or {}).get(k))
        dA, dB, dI = st['A'][2], st['B'][2], st['I'][2]
        # ---- stages
        mdir = os.path.join(out, '01_route_a_tail_manifest', 'manifest')
        arr_pin = put_npz(os.path.join(mdir, 'state_arrays.npz'), st['A'][1])
        mpin = put_json(os.path.join(mdir, 'ROUTE_A_TAIL_MANIFEST.json'),
                        {'state': {'digest': dA, 'record': st['A'][0], 'arrays': arr_pin}})
        mfin = put_json(os.path.join(mdir, 'finish.json'), {'state_digest': dA, 'empty': False, 'manifest': mpin})
        rdir = os.path.join(out, '02_reference', 'reference')
        rfin = put_json(os.path.join(rdir, 'finish.json'), {'uv_tail': {'state_digest': dA, 'roster_digest': rost['A'],
                                                                         'stage_kind': 'route_a', 'kept': dict(A.KEPT),
                                                                         'empty': False}})
        bdir = os.path.join(out, '20_le3_rotation', 'rotation')
        bkept = (o.get('kept_claim') or {}).get('B', dict(A.KEPT))
        bfin = put_json(os.path.join(bdir, 'finish.json'), {'uv_tail': {'state_digest': dB, 'roster_digest': rost['B'],
                                                                         'stage_kind': 'le_rotation', 'kept': bkept,
                                                                         'empty': False}})
        ctx = [{'name': '00_route_a', 'kind': 'route_a', 'executed': True, 'argv': ['--start-iteration', '0']},
               {'name': '01_route_a_tail_manifest', 'kind': 'route_a_tail_manifest', 'executed': True,
                'argv': ['--seed', 'x', '--outdir', mdir]},
               {'name': '02_reference', 'kind': 'reference', 'executed': True, 'argv': ['--outdir', rdir]},
               {'name': '20_le3_rotation', 'kind': 'rotation_v005', 'executed': True, 'argv': ['--outdir', bdir]}]
        srec = [{'stage': '01_route_a_tail_manifest', 'kind': 'route_a_tail_manifest', 'finish_sha256': mfin['sha256'],
                 'state_digest': dA},
                {'stage': '02_reference', 'kind': 'reference', 'finish_sha256': rfin['sha256'], 'state_digest': dA},
                {'stage': '20_le3_rotation', 'kind': 'rotation_v005', 'finish_sha256': bfin['sha256'], 'state_digest': dB}]
        # ---- passes and rows
        X = o.get('X') or {}                                     # id -> {'reason', 'earlier'}
        npass = 3
        passes, vmax = [], [None] * N
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
                else:
                    v = BASE_V[i] * (1.0 - 0.01 * (npass - 1 - p))
                    if p == 0 and i == 5:
                        v = -(BASE_V[i] + 30.0)                  # a negative readout: |v| counts (Q4(a))
                    rows.append({'id': q, 'speed_km_s': v, 'valid': True})
            for (pp, ii) in o.get('missing_readout') or ():
                if pp == p:
                    rows[ii] = {'id': IDS[ii], 'speed_km_s': None, 'valid': True}
            for i, r in enumerate(rows):
                if isinstance(r.get('speed_km_s'), float):
                    a = abs(r['speed_km_s'])
                    vmax[i] = a if vmax[i] is None or a > vmax[i] else vmax[i]
            inv_ids = [r['id'] for r in rows if r.get('valid') is False]
            cdir = os.path.join(out, '%02d_le%d_column_mean' % (30 + p, p + 1), 'observation')
            support = [{'id': r['id'], 'radius_m': R_M[i], 'column_indices': [0]} for i, r in enumerate(rows)
                       if r.get('valid') is not False]
            if o.get('support_radius_off') and p == npass - 1:
                support[0] = dict(support[0], radius_m=support[0]['radius_m'] * (1 + 1e-9))
            cm = put_json(os.path.join(cdir, 'result.json'), {'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION',
                                                              'prediction': {'rows': rows, 'query_support': support}})
            pr = {'pass': p + 1, 'columns': ['c'], 'rotation': os.path.join(out, 'r%d' % p, 'rotation'),
                  'column_mean': {'path': cm['path'], 'sha256': cm['sha256'],
                                  'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'},
                  'rows': rows, 'invalid_rows': inv_ids}
            if p in (o.get('missing_pass_rows') or ()):
                pr.pop('rows')
                pr.pop('invalid_rows')
                pr['column_mean'] = 'NOT_OBSERVED (multi-run parallel pass or observe_every_pass false)'
            passes.append(pr)
        final = passes[-1]['rows']
        result = {'driver_sha256': o.get('driver_sha256', self.registry['driver']['sha256']), 'galaxy': 'NGC3198',
                  'call_spec_sha256': spec_ref['sha256'], 'status': 'COMPLETED', 'valid': True, 'final_pass': npass,
                  'passes': passes, 'rows': final, 'invalid_rows': [r['id'] for r in final if r.get('valid') is False],
                  'stage_records': ctx,
                  'uv_tail': {'stage_records': srec, 'manifest': {'path': mpin['path'], 'sha256': mpin['sha256'],
                                                                  'state_digest': dA, 'empty': False},
                              'route_a_record': {'boundary_state_digest_at_return': dA, 'sidecar': 'SYNTHETIC',
                                                 'flags': []}}}
        rp = put_json(os.path.join(out, 'result.json'), result)
        put_json(os.path.join(out, 'finish.json'), {'status': 'COMPLETED', 'valid': True, 'result_path': rp['path'],
                                                    'result_sha256': rp['sha256'], 'retries': 0})
        receipt = put_json(os.path.join(base, 'receipt.json'), {'status': 'FINISHED', 'driver_status': 'COMPLETED',
                                                                'result': {'sha256': rp['sha256']}})
        iters = None
        if o.get('iterates', True):
            iters = put_json(os.path.join(base, 'iterates.json'), {
                'schema': 'UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001', 'producer': dict(self.sidecar_reader), 'call_result': rp,
                'occurrences': [
                    {'iteration': 0, 'role': 'current_begin_inferred_from_completion', 'state_sha256': dI,
                     'source_sha256': rost['I']},
                    {'iteration': 0, 'role': 'next_built_and_monitor_consumed', 'state_sha256': dA, 'source_sha256': rost['A']},
                    {'iteration': 1, 'role': 'current_begin_inferred_from_completion', 'state_sha256': dA,
                     'source_sha256': rost['A']}]})
        # ---- rebuild exports (open interface) for B and I
        exports = {}
        for k, d in (('B', dB), ('I', dI)):
            rec_k, arr_k = st[k][0], dict(st[k][1])
            if k in (o.get('tamper_arrays') or ()):              # outside the B1 arithmetic: only S5's digest sees it
                arr_k = dict(arr_k, ring_radii_m=arr_k['ring_radii_m'] * 2.0)
            if k in (o.get('b1_perturb') or ()):
                si = arr_k['shell_integrals'].copy()
                nz = np.flatnonzero(si[:, 1])[0]
                si[nz, 1] *= (1 + 1e-9)
                arr_k = dict(arr_k, shell_integrals=si)
                rec_k = dict(rec_k)
            ra = put_npz(os.path.join(base, 'rebuild', '%s_arrays.npz' % k), arr_k)
            rr = put_json(os.path.join(base, 'rebuild', '%s_record.json' % k), rec_k)
            exports[d] = put_json(os.path.join(base, 'rebuild', '%s_state_input.json' % k), {
                'schema': 'UNT_NGC_LO_STATE_INPUT_C2V001',
                'state': {'state_sha256': d, 'source_sha256': rost[k], 'stage_kind': kinds[k]},
                'call_result': rp, 'source': 'POST_RUN_REBUILD', 'producer': dict(self.rebuild_producer),
                'tail_state': {'record': rr, 'arrays': ra}})
        # ---- rho fixtures (S2 interface)
        rho = self.make_rho(base, key, spec_ref, th, o.get('rho', 'same'))
        # ---- row contract and review (S8, S10)
        b1A = self.s4_b1(st['A'][3])
        g_unit = max(r * b for r, b in zip(RHO_USED, b1A))
        c = g_unit / (4 * TARGET_MAX_RATIO)
        vcal = [vmax[i] if vmax[i] is not None else BASE_V[i] for i in range(N)]
        t = [c * vcal[i] * R_M[i] for i in range(N)]
        for q in X:
            t[IDS.index(q)] = c * BASE_V[IDS.index(q)] * R_M[IDS.index(q)]
        contract = {'schema': 'UNT_NGC_LO_ROW_CONTRACT_C2V001', 'query_ids': list(IDS), 'manifest': dict(self.manifest),
                    'manifest_radius_scale': 1.0, 'R_m': list(R_M), 't_km_s': t, 't_rule_id': self.rule_id,
                    'binding': None}
        cv = o.get('contract', 'ok')
        if cv == 'sigma':
            contract['sigma_km_s'] = [1.0] * N
        elif cv == 'tau':
            contract['tau_km_s'] = [1.0] * N
        elif cv == 'no_t':
            contract.pop('t_km_s')
        elif cv == 'rule_other':
            contract['t_rule_id'] = 'A134_Q4C_TAU_0P25_SIGMA'
        elif cv == 'order':
            contract['query_ids'] = list(reversed(IDS))
        elif cv == 'R_off':
            contract['R_m'] = [x * (1 + 1e-9) for x in R_M]
        cpin = put_json(os.path.join(base, 'row_contract.json'), contract)
        review = put_json(os.path.join(base, 'row_review.json'), {'schema': 'UNT_NGC_LO_ROW_POLICY_REVIEW_C2V001',
                                                                  'verdict': 'APPROVED', 'row_contract_sha256': cpin['sha256']})
        return {'name': name, 'base': base, 'call_dir': os.path.join(base, 'call'), 'spec_ref': spec_ref, 'result': rp,
                'receipt': receipt, 'iterates': iters, 'exports': exports, 'rho': rho, 'contract': cpin,
                'review': review, 'digests': {'A': dA, 'B': dB, 'I': dI}, 'rosters': rost, 'key': key,
                'b1A_s4': b1A, 'c': c, 'states': st}

    def make_rho(self, base, key, spec_ref, th, variant):
        A = self.A
        rdir = os.path.join(base, 'rho')
        idn = {'schema': A.RHO_IDENTITY_SCHEMA, 'theta_key': key, 's0_record_sha256': self.registry['s0']['sha256'],
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
        rec = {'schema': A.RHO_SCHEMA, 'gate': 'RHO_G', 'status': 'TESTED', 'verdict': 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED',
               'identity': idn, 'point_sha256': psha,
               'custody': {'schema': 'UNT_NGC_POINT_RHO_CUSTODY_C3V001', 'registry_kind': 'SYNTHETIC_TEST',
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
        proof = {'schema': A.SLOT_PROOF_SCHEMA, 'gate': A.SLOT_GATE, 'status': 'TESTED', 'verdict': 'PASS',
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
        self.shas = {k: sha_file(p) for k, p in self.paths.items()}
        self.E = load(self.paths['E'], 'suite_ngc_consumed_states')
        self.A = load(self.paths['A'], 'suite_ngc_lo_state_adapter')
        self.H = load(self.paths['H'], 'suite_ngc_acceptance_handoff')
        self.U = load(self.A.LIBRARY[0], 'suite_uvt_lapse_v002')
        assert sha_file(self.A.LIBRARY[0]) == self.A.LIBRARY[1]
        self.art_patched = not run_dir.startswith(self.H.ART + os.sep)
        if self.art_patched:                                       # dev runs outside claude_artifacts only
            self.H.ART = os.path.dirname(run_dir)
        self.fx = Fx(run_dir, self.A, self.E, self.H, self.U)
        self.results = []

    # ---------------------------------------------------------------- runners
    def env(self, call, registry=None):
        return self.A.make_env(registry or self.fx.registry, rho_producer_ref=call['rho']['producer'],
                               approved_rho_producer_sha256=call['rho']['approved_rho'])

    def inventory(self, call, driver=None):
        return self.E.enumerate_call(call['call_dir'], route_a_iterates_ref=call['iterates'],
                                     approved_iterate_producer_sha256=[self.fx.sidecar_reader['sha256']],
                                     driver_sha256=driver or self.fx.registry['driver']['sha256'])

    def state_inputs(self, call, inv, out_root):
        si = dict(call['exports'])
        man = read_json(inv['manifest'])
        acc = [s for s in inv['states'] if s['state_sha256'] == inv['accepted_state_sha256']][0]
        rr = put_json(os.path.join(out_root, 'ACC_RECORD.json'), man['state']['record'])
        si[acc['state_sha256']] = put_json(os.path.join(out_root, 'ACC_INPUT.json'), {
            'schema': 'UNT_NGC_LO_STATE_INPUT_C2V001', 'state': acc, 'call_result': inv['call_result'],
            'source': 'ROUTE_A_TAIL_MANIFEST', 'tail_state': {'record': rr, 'arrays': man['state']['arrays']}})
        return si

    def adapt(self, call, *, registry=None, approved=None, review=True, rebuild_ok=True, inv=None, state_inputs=None,
              tag='adapt'):
        A = self.A
        inv = inv if inv is not None else self.inventory(call)
        out_root = os.path.join(call['base'], tag)
        os.makedirs(out_root)
        si = state_inputs if state_inputs is not None else self.state_inputs(call, inv, out_root)
        rec = A._adapt_call(
            call_dir=call['call_dir'], spec_ref=call['spec_ref'], inventory=inv, state_inputs=si,
            row_contract_ref=call['contract'], row_policy_review_ref=call['review'] if review else None,
            slot_proof_ref=call['rho']['proof'],
            approved_producer_sha256=[self.shas['A']] if approved is None else approved,
            approved_slot_proof_producer_sha256=[self.fx.slot_proof_producer['sha256']],
            approved_rho_producer_sha256=call['rho']['approved_rho'],
            approved_rebuild_producer_sha256=[self.fx.rebuild_producer['sha256']] if rebuild_ok else [],
            trusted_row_policy_review_sha256=[call['review']['sha256']] if review else [], out_root=out_root,
            env=self.env(call, registry))
        return rec, inv

    def by_state(self, rec, call):
        m = {s['state']['state_sha256']: s for s in rec['states']}
        return {k: m.get(d) for k, d in call['digests'].items()}

    def policy(self, call, **kw):
        p = {'receipt': call['receipt'], 'route_a_iterates': call['iterates'],
             'approved_iterate_producer_sha256': [self.fx.sidecar_reader['sha256']], 'rebuild_exports': call['exports'],
             'row_contract': call['contract'], 'row_policy_review': call['review'], 'slot_proof': call['rho']['proof'],
             'rho_producer': call['rho']['producer'], 'approved_producer_sha256': [self.shas['A']],
             'approved_slot_proof_producer_sha256': [self.fx.slot_proof_producer['sha256']],
             'approved_rho_producer_sha256': call['rho']['approved_rho'],
             'approved_rebuild_producer_sha256': [self.fx.rebuild_producer['sha256']],
             'trusted_row_policy_review_sha256': [call['review']['sha256']]}
        p.update(kw)
        return p

    def handoff(self, call, *, adapter_fn=None, policy=None, tag='handoff'):
        H, A = self.H, self.A
        env = self.env(call)

        def fn(**kw):
            kw.pop('rho_producer_ref')
            return A._adapt_call(env=env, **kw)
        return H._accept(call_dir=call['call_dir'], spec_ref=call['spec_ref'], policy=policy or self.policy(call),
                         records_dir=os.path.join(call['base'], tag), enumerate_fn=self.E.enumerate_call,
                         adapter_fn=adapter_fn or fn, A=A, registry=self.fx.registry)

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

    @staticmethod
    def codes(entry):
        return entry['codes'] if entry else None

    # ---------------------------------------------------------------- MUST_PASS
    def p01(self):
        c = self.fx.make_call('p01')
        inv = self.inventory(c)
        cl = {x['state']['state_sha256']: x['class'] for x in inv['classes']}
        want = {c['digests']['A']: 'ACCEPTED_ROUTE_A', c['digests']['B']: 'ROUTE_B_STAGE',
                c['digests']['I']: 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'}
        roles_a = [x['roles'] for x in inv['classes'] if x['state']['state_sha256'] == c['digests']['A']][0]
        ok = inv['complete'] and cl == want and 'inherited_route_a' in roles_a and len(inv['states']) == 3
        return ok, {'complete': inv['complete'], 'classes': sorted(cl.values()), 'roles_A': roles_a,
                    'blockers': inv['blockers']}

    def p02(self):
        np, A = self.fx.np, self.A
        e = A.expected_unit_edges()
        b1 = np.zeros(len(e) - 1)
        b1[0], b1[5], b1[30], b1[40], b1[44] = 1.0, 2.0, 3.0, 4.0, 5.0      # (2,3] (7,8] (32,33] (42,43] (46,47]
        rows = [{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 1.0, 'R': 1.0, 't': 1.0}]
        rho = [{'range_inverse_kpc': r, 'rho_used': 1.0} for r in PARTITION]
        agg = A.aggregate(rho, e, b1, rows)
        dom = [s['domain'] for s in agg['shells']]
        b = [s['B1_per_m'] for s in agg['shells']]
        ok = (float(e[-1]) == 47.0 and dom == ['TILED'] * 7 + ['PARTIAL_TO_E_TOP', 'NOT_IN_STATE_DOMAIN']
              and b == [1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 12.0, 0.0] and agg['shells'][8]['max_over_t'] == 0.0
              and agg['G'] == sum(s['max_over_t'] for s in agg['shells']) and len(agg['shells']) == 9
              and agg['coverage_problem'] is None)
        return ok, {'E_top': float(e[-1]), 'domains': dom, 'B1_s': b, 'G': agg['G']}

    def p03(self):
        np, A = self.fx.np, self.A
        out = {}
        for top in (64.0, 91.0):
            e = np.arange(2.0, top + 1.0)
            b1 = np.ones(len(e) - 1)
            rho = [{'range_inverse_kpc': r, 'rho_used': 1.0} for r in PARTITION]
            agg = A.aggregate(rho, e, b1, [{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 1.0, 'R': 1.0, 't': 1.0}])
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
        ok = r['status'] == 'INCLUDED' and r['v'] == 777.0
        return ok, r

    def p07(self):
        c, ro = self.readouts()
        result = read_json(c['result'])
        plain = [max(abs(p['rows'][i]['speed_km_s']) for p in result['passes']) for i in range(N)]
        ok = ro['X'] == [] and [r['v'] for r in ro['rows']] == plain
        return ok, {'X': ro['X']}

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
        ok = all(s[k]['verdict'] == 'UNAVAILABLE' and s[k]['codes'] == ['READOUT_NOT_RECORDED'] for k in 'ABI') \
            and rec['call_lo_reading'] == 'INCOMPLETE'
        return ok, {k: s[k]['codes'] for k in 'ABI'}

    def p10(self):
        c, ro = self.readouts(X={'SYNQ-43': {'reason': 'QUERY_BEYOND_OUTER_GAS_CUT', 'earlier': 50.0}})
        d = ro['diagnostic']['pass_invalid_rows_equal_X']
        return d == [False, True, True], d

    def p11(self):
        c = self.fx.make_call('p11')
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        recs = {k: read_json(s[k]['record']) for k in 'ABI'}
        numbers_in_call = floats_outside_flags(rec)
        ok = (rec['call_lo_reading'] == 'PASS' and all(s[k]['verdict'] == 'PASS' for k in 'ABI')
              and all(r['scope_disclosure'] == self.A.SCOPE_DISCLOSURE for r in recs.values())
              and not numbers_in_call and abs(recs['A']['shells'][[i for i, x in enumerate(c['b1A_s4'])
                                                                    if x * RHO_USED[i] == max(a * b for a, b in zip(RHO_USED, c['b1A_s4']))][0]]['max_over_t'] - TARGET_MAX_RATIO) < 1e-12
              and recs['A']['shells'][8]['domain'] == 'NOT_IN_STATE_DOMAIN' and recs['A']['shells'][7]['domain'] == 'PARTIAL_TO_E_TOP')
        return ok, {'call': rec['call_lo_reading'], 'states': {k: s[k]['verdict'] for k in 'ABI'},
                    'numeric_keys_in_call_record': numbers_in_call, 'G_A_below_0.05': recs['A']['G'] < 0.05}

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
              and s['A']['verdict'] == s['B']['verdict'] == 'PASS' and rec['call_lo_reading'] == 'LO_UNCERTIFIED_TRANSIENT')
        return ok, {'call': rec['call_lo_reading']}

    def p14(self):
        c = self.fx.make_call('p14', scales={'I': 10.0})
        inv = self.inventory(c)
        out_root = os.path.join(c['base'], 'si')
        os.makedirs(out_root)
        si = self.state_inputs(c, inv, out_root)
        si.pop(c['digests']['B'])                                 # route-B state input missing -> UNAVAILABLE
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
        """A fabricated call naming the registered driver sha (a string). Its spec label carries no theta key, so even a
        module whose t_i gate were broken would refuse at the label, before any registered S0 point is read."""
        return self.fx.make_call(name, driver_sha256=REAL_DRIVER_SHA,
                                 spec_overrides={'label': 'step5 A_K32_A2_HEADLINE theta_key=NOT_A_REAL_KEY'})

    def gate_precheck(self):
        A = self.A
        return A.T_I_ENTRY is None and A.t_rule_id(A.real_registry()) is None

    def p16(self):
        A = self.A
        if not self.gate_precheck():
            return False, 'T_I_ENTRY or t_rule_id is not None in this module: the public entry is not run'
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
        ok = (A.T_I_ENTRY is None and rec['registry_kind'] == 'REGISTERED' and rec['t_rule_id'] is None
              and len(rec['states']) == 3 and all(s['codes'] == ['NGC_LO_TOLERANCE_NOT_DECLARED'] for s in rec['states'])
              and rec['call_lo_reading'] == 'INCOMPLETE' and not numeric and len(recs) == 3
              and all(r['scope_disclosure'] == A.SCOPE_DISCLOSURE for r in recs))
        return ok, {'call': rec['call_lo_reading'], 'codes': [s['codes'] for s in rec['states']], 'numeric_keys': numeric,
                    'blockers': rec['blockers']}

    def p17(self):
        c = self.fx.make_call('p17')
        rec, pin = self.handoff(c)
        summ = read_json(rec['root_summary'])
        leaks = floats_outside_flags(summ) + floats_outside_flags(rec)
        ok = (rec['reading'] == 'ACCEPTED' and rec['member_lo_ok'] is True and len(rec['states']) == 3
              and all(e['verdict'] == 'PASS' for e in rec['states']) and not leaks and summ['reading'] == 'ACCEPTED')
        return ok, {'reading': rec['reading'], 'blockers': rec['blockers'], 'value_leaks': leaks[:5]}

    def p18(self):
        H = self.H
        if not self.gate_precheck():
            return False, 'T_I_ENTRY or t_rule_id is not None in this module: the public entry is not run'
        c = self.real_call('p18')
        rec, pin = H.accept_call_ngc(call_dir=c['call_dir'], spec_ref=c['spec_ref'], policy=self.policy(c),
                                     records_dir=os.path.join(c['base'], 'handoff_public'))
        ok = (rec['reading'] == 'INCOMPLETE' and rec['member_lo_ok'] is False and len(rec['states']) == 3
              and all(e['codes'] == ['NGC_LO_TOLERANCE_NOT_DECLARED'] for e in rec['states'])
              and rec['registry_kind'] == 'REGISTERED' and rec['pins']['lo_adapter']['sha256'] == self.shas['A']
              and rec['pins']['enumerator']['sha256'] == self.shas['E'])
        return ok, {'reading': rec['reading'], 'codes': [e['codes'] for e in rec['states']], 'blockers': rec['blockers'][:3]}

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
        return g['bits_equal'] is True and len(set(v for k, v in g.items() if k != 'bits_equal')) == 1, g

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

    # ---------------------------------------------------------------- MUST_FAIL (S13 and more)
    def all_codes(self, rec, code):
        return bool(rec['states']) and all(s['codes'] == [code] for s in rec['states']) and rec['call_lo_reading'] == 'INCOMPLETE'

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
        A = self.A
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
        b1[91] = 1.0                                               # unit shell (93,94]: above 91
        rows = [{'id': 'r', 'status': A.ROW_INCLUDED, 'v': 1.0, 'R': 1.0, 't': 1.0}]
        rho = [{'range_inverse_kpc': r, 'rho_used': 1.0} for r in PARTITION]
        agg = A.aggregate(rho, e, b1, rows)
        v1 = A.decide(agg, rows)
        e2 = np.asarray([2.0, 2.5, 3.5, 4.0, 6.0, 8.0, 12.0, 16.0, 32.0, 47.0])
        agg2 = A.aggregate(rho, e2, np.ones(len(e2) - 1), rows)
        v2 = A.decide(agg2, rows)
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
        return ok, {k: s[k]['codes'] for k in 'ABI'}

    def f06(self):
        c = self.fx.make_call('f06', gamma_ulp={'B': 1})
        rec, _ = self.adapt(c)
        s = self.by_state(rec, c)
        c2 = self.fx.make_call('f06b', point=1)
        rec2, _ = self.adapt(c2)
        ok = (s['B']['codes'] == ['NGC_GAMMA_ROUTE_BITS_DIFFER'] and s['A']['verdict'] == 'PASS'
              and all(x['codes'] == ['NGC_GAMMA_ROUTE_BITS_DIFFER'] for x in rec2['states'])
              and rec['call_lo_reading'] == rec2['call_lo_reading'] == 'INCOMPLETE')
        return ok, {'state_ulp': s['B']['codes'], 'route_bits': [x['codes'] for x in rec2['states']]}

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
        for v in ('no_t', 'rule_other'):
            c = self.fx.make_call('f10_' + v, contract=v)
            rec, _ = self.adapt(c)
            out[v] = self.all_codes(rec, 'NGC_LO_TOLERANCE_NOT_DECLARED')
        c = self.fx.make_call('f10_noentry')
        reg = dict(self.fx.registry, t_i_entry=None)
        rec, _ = self.adapt(c, registry=reg)
        out['no_root_entry'] = self.all_codes(rec, 'NGC_LO_TOLERANCE_NOT_DECLARED') and rec['t_rule_id'] is None
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
                          ('no_fail_text', {'fail_text': None})):
            try:
                A.guard_state_record(dict(b, **mut))
                refused[name] = False
            except A.Refusal:
                refused[name] = True
        try:                                                       # the writer refuses too
            A.write_state_record(dict(b, scope_disclosure=None), os.path.join(c['base'], 'adapt'))
            refused['writer'] = False
        except A.Refusal:
            refused['writer'] = True

        def strip_adapter(**kw):                                   # a FAIL record file without the scope text
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
        ok = s['B']['codes'] == s['I']['codes'] == ['NGC_STATE_INPUT_UNAVAILABLE'] and s['A']['verdict'] == 'PASS'
        return ok, {k: s[k]['codes'] for k in 'ABI'}

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
        reg = dict(self.fx.registry, a153=dict(A.A153))
        try:
            A.check_registry(reg)
            out['a153'] = False
        except A.Refusal:
            out['a153'] = True
        return all(out.values()), out

    def f21(self):
        c = self.fx.make_call('f21', b1_perturb=['B'])
        # the perturbed stored B1 changes the digest: re-key the inventory occurrence would hide it, so check both layers
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
        rec, pin = self.handoff(c, policy=self.policy(c, receipt=bad))
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

    # ---------------------------------------------------------------- run
    def all(self):
        P = [('P01', 'enumerator: complete inventory, Q5 classes, inherited merged', self.p01),
             ('P02', 'S4 at E_top 47: 7 tiled, (32,64] partial over (32,47], (64,91] NOT_IN_STATE_DOMAIN, G sums 9', self.p02),
             ('P03', 'S4 hi <= E_top exact tiling at E_top 64 and 91 (pure aggregate)', self.p03),
             ('P04', 'S6 |v_i| = max |speed| over every pass (negative readout)', self.p04),
             ('P05', 'S6 X row, authorized reason, no finite readout: excluded with reason', self.p05),
             ('P06', 'S6 X row with a finite readout in an earlier pass: included at that max', self.p06),
             ('P07', 'S6 X empty: the unchanged own_call_vmax', self.p07),
             ('P08', 'S6 monotone-FAIL: missing readout, present rows decide FAIL', self.p08),
             ('P09', 'S6 missing readout, no decided FAIL: READOUT_NOT_RECORDED', self.p09),
             ('P10', 'S6 set(pass.invalid_rows) == X recorded as a diagnostic', self.p10),
             ('P11', 'adapter PASS at every state; call PASS; no values in the call record', self.p11),
             ('P12', 'route-B FAIL: NON_LAPSE_TAIL_MATERIAL with scope and FAIL text', self.p12),
             ('P13', 'iterate-only FAIL, others PASS: LO_UNCERTIFIED_TRANSIENT', self.p13),
             ('P14', 'iterate FAIL with a non-iterate UNAVAILABLE: INCOMPLETE', self.p14),
             ('P15', 'route-B FAIL decisive with another state UNAVAILABLE', self.p15),
             ('P16', 'public entry (REGISTERED, T_I_ENTRY None): every state NGC_LO_TOLERANCE_NOT_DECLARED, nothing computed', self.p16),
             ('P17', 'handoff end to end: ACCEPTED, member_lo_ok, blinded summary', self.p17),
             ('P18', 'handoff public entry: INCOMPLETE, every state NGC_LO_TOLERANCE_NOT_DECLARED', self.p18),
             ('P19', 'handoff NON_LAPSE_TAIL_MATERIAL: member invalid, rows not model output', self.p19),
             ('P20', 'C4b: state, spec-route and theta-route gamma bits recorded equal', self.p20),
             ('P21', 'rho 10-key equal and the B1 1e-10 check recorded', self.p21),
             ('P22', 'high-Q-inf flag recorded, reading unchanged', self.p22)]
        F = [('F01', 'S13 rho from a1dcdea8 (slot schema, proof producer, recompute)', self.f01),
             ('F02', 'S13 the certificate parsed as a rho record', self.f02),
             ('F03', 'S13 the cylinder-64 partition assumed at outer 32 without S4', self.f03),
             ('F04', 'S13 nonzero B1 above 91 / outside exactly one rho shell', self.f04),
             ('F05', 'S13 outer != 32 or kept != {cube, 2.0}', self.f05),
             ('F06', 'S13 gamma bits differ (state ulp; spec route vs theta route)', self.f06),
             ('F07', 'S13 a row in X with a finite readout excluded', self.f07),
             ('F08', 'S13 a missing pass row list read as PASS', self.f08),
             ('F09', 'S13 sigma or DDO tau present in the row contract', self.f09),
             ('F10', 'S13 t_i absent (no t, foreign rule id, no root entry)', self.f10),
             ('F11', 'S13 an anchor class emitted', self.f11),
             ('F12', 'S13 a FAIL record without the scope text', self.f12),
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
             ('F25', 'rho recompute without single-thread BLAS', self.f25)]
        for rid, name, fn in P:
            self.run(rid + ' ' + name, 'MUST_PASS', fn)
        for rid, name, fn in F:
            self.run(rid + ' ' + name, 'MUST_FAIL', fn)
        return P, F


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--module-dir', default=os.path.dirname(os.path.realpath(__file__)))
    a = ap.parse_args(argv)
    for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        os.environ[k] = '1'                                        # before numpy loads (the library imports it)
    run_dir = os.path.realpath(a.run_dir)
    os.mkdir(run_dir)
    t0 = time.monotonic()
    s = Suite(run_dir, os.path.realpath(a.module_dir))
    P, F = s.all()
    mp = [r for r in s.results if r['kind'] == 'MUST_PASS']
    mf = [r for r in s.results if r['kind'] == 'MUST_FAIL']
    out = {'schema': 'NGC_ACCEPTANCE_C2V001_SUITE_RESULTS', 'synthetic_only': True, 'module_shas': s.shas,
           'library_sha256': s.A.LIBRARY[1], 'T_I_ENTRY_of_record_module': s.A.T_I_ENTRY,
           'art_patched_for_dev_run': s.art_patched, 'python': sys.version.split()[0],
           'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode},
           'must_pass': '%d/%d' % (sum(r['ok'] for r in mp), len(mp)), 'must_fail': '%d/%d' % (sum(r['ok'] for r in mf), len(mf)),
           'results': s.results, 'seconds': round(time.monotonic() - t0, 3)}
    pin = put_json(os.path.join(run_dir, 'SUITE_RESULTS_C2V001.json'), out)
    print(json.dumps({'must_pass': out['must_pass'], 'must_fail': out['must_fail'], 'results': pin,
                      'failed': [r['id'] for r in s.results if not r['ok']]}))
    return 0 if all(r['ok'] for r in s.results) else 1


if __name__ == '__main__':
    sys.exit(main())
