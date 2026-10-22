"""P-88 k_max / truncation-shape comparison and pre-registered decision (Claude2 lane, dispatch 0470, c2v001).

Reads the driver result.json of every registered case, applies the validity gates V1-V6 and the
decision rule of KMAX_MATRIX_PREREG_V001.json (sha pinned below), and writes the row table,
the K-sequence differences, a gravity-only field diagnostic and the decision.
Read-only on all inputs; writes only into a NEW --outdir.  numpy only, single thread.
It never opens observed velocities: sigma values are taken from the pre-registration.

usage:
  python3 -I -B kmax_compare_c2v001.py --prereg KMAX_MATRIX_PREREG_V001.json \
      --cases CASES.json --outdir NEW_DIR [--no-field-diagnostic]
CASES.json: {"C4": "/.../call_0000/out/result.json", "S4": "...", ...}  (missing cases allowed;
the decision then reports INCOMPLETE for the steps that need them).

The ONLY schema-dependent code is adapt_result() (driver schema UNT_GALAXY_M0_FORWARD_RESULT_C2V001,
INTERFACE_C2_0466_V001 s8).  If the driver schema changes, change that function only.
"""
import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

PREREG_SHA256 = 'd5acfc2fea1c99adf7709ab509eb95bf966c0b3d6db7398b091ec2bd305538be'
RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001'
KPC = 3.085677581491367e19
C2 = 299792458.0 ** 2
BASE_SPEC = {'breaks_inverse_kpc': [-2, -1, -0.3, -0.1, -0.03, -0.01, 0, 0.01, 0.03, 0.1, 0.3, 1, 2], 'panel_orders': [6] * 12}
A2_SHA = '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'
COMMON_KEYS = ('galaxy', 'physical', 'coefficients')
COMMON_NUMERICS = ('picard', 'brackets')
SHAPES = ('cube', 'sphere', 'cylinder')
KS = (2, 3, 4)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# --------------------------------------------------------------------------- the single adapter
def adapt_result(result_path):
    """Map one driver result.json (+ the stage files it points to) onto the fields this script uses.
    Returns a dict; missing optional items are None.  Raises only on unreadable JSON."""
    rp = Path(result_path)
    r = json.loads(rp.read_text())
    passes = r.get('passes') or []
    last = passes[-1] if passes else {}
    ns = r.get('normalized_spec') or {}
    num = ns.get('numerics') or {}
    harm = ((r.get('residual_diagnostics') or {}).get('azimuthal_harmonics'))
    harm = harm if isinstance(harm, dict) else {}
    ident = (((r.get('identity') or {}).get('route_a') or {}).get('custody') or {})
    field_dir = last.get('field')
    rot_dir = last.get('rotation')
    packet = None
    if field_dir and (Path(field_dir) / 'finish.json').is_file():
        ff = json.loads((Path(field_dir) / 'finish.json').read_text())
        packet = (ff.get('outputs') or {}).get('refreshed_prepared.npz')
    base_K = None
    if rot_dir and (Path(rot_dir) / 'finish.json').is_file():
        base_K = json.loads((Path(rot_dir) / 'finish.json').read_text()).get('base_K_values_SI')
    return {
        'result_path': str(rp), 'result_sha256': sha256_file(rp), 'schema': r.get('schema'),
        'status': r.get('status'), 'valid': r.get('valid'), 'reasons': r.get('reasons'),
        'driver_sha256': r.get('driver_sha256'), 'call_spec_sha256': r.get('call_spec_sha256'),
        'rows': {x['id']: x['speed_km_s'] for x in (r.get('rows') or [])},
        'normalized_spec': ns,
        'grid_spec': num.get('composite_grid_spec'), 'truncation': num.get('truncation'),
        'final_pass': r.get('final_pass'), 'last_change_km_s': last.get('max_abs_change_km_s'),
        'per_pass_rows': [{'pass': p.get('pass'), 'max_abs_change_km_s': p.get('max_abs_change_km_s')} for p in passes],
        'field_packet': packet, 'route_a_identity_sha256': ident.get('identity_sha256'),
        'harm_m4': (harm.get('global_max') or {}).get('m4'), 'harm_m8': (harm.get('global_max') or {}).get('m8'),
        'base_K_values_SI': base_K, 'elapsed_seconds': r.get('elapsed_seconds')}


# --------------------------------------------------------------------------- grid / mask helpers
def expected_axis(grid_spec):
    spec = grid_spec or BASE_SPEC
    parts = []
    for lo, hi, n in zip(spec['breaks_inverse_kpc'][:-1], spec['breaks_inverse_kpc'][1:], spec['panel_orders']):
        x, _ = np.polynomial.legendre.leggauss(n)
        parts.append(((lo + hi) / 2 + (hi - lo) * x / 2) / KPC)
    return np.concatenate(parts)


def driver_mask(k, shape, kmax_inverse_m):
    """Identical expression to galaxy_m0_forward_c2v001.truncation_mask (|k| or k_perp <= kmax)."""
    if shape == 'cube':
        return np.ones(len(k), dtype=bool)
    if shape == 'sphere':
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1] + k[:, 2] * k[:, 2])
    else:
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1])
    return r <= kmax_inverse_m


def packet_checks(a, case, grid_spec, radii_m, field_diag):
    """V4 (grid), V5 (mask) and the gravity-only m0 ring diagnostic from the final field packet."""
    pk = a['field_packet']
    if not pk:
        return {'V4': False, 'V5': False, 'reason': 'no final field packet recorded'}, None
    p = Path(pk['path'])
    if not p.is_file() or sha256_file(p) != pk['sha256']:
        return {'V4': False, 'V5': False, 'reason': 'field packet missing or sha mismatch'}, None
    with np.load(p, allow_pickle=False) as f:
        k = f['wavevectors'].copy()
        w = f['weighted_responses'].copy()
    ax = expected_axis(grid_spec)
    n = len(ax)
    uniq = [np.unique(k[:, i]) for i in range(3)]
    v4 = bool(len(k) == n ** 3 and all(len(u) == n and np.array_equal(u, ax) for u in uniq))
    kmax_kpc = case['kmax_inverse_kpc'] if case['kmax_inverse_kpc'] is not None else float((grid_spec or BASE_SPEC)['breaks_inverse_kpc'][-1])
    m = driver_mask(k, case['shape'], kmax_kpc / KPC)
    outside_zero = bool(np.all(w[~m] == 0))
    # expected kept count from the registered axis (independent of the packet)
    g = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
    expect_kept = int(np.count_nonzero(driver_mask(g, case['shape'], kmax_kpc / KPC)))
    kept_nonzero = int(np.count_nonzero(np.any(w.reshape(len(w), -1) != 0, axis=1)))
    chk = {'V4': v4, 'V5': bool(outside_zero and int(m.sum()) == expect_kept), 'nodes': int(len(k)), 'axis_nodes_expected': n,
           'mask_kept_expected': expect_kept, 'mask_kept_in_packet': int(m.sum()), 'nonzero_rows_in_packet': kept_nonzero,
           'packet_sha256': pk['sha256']}
    diag = None
    if field_diag:
        diag = ring_diagnostic(k, w[:, 0, 0], radii_m)
    return chk, diag


def ring_diagnostic(k, amp, radii_m, nphi=32, batch=8):
    """Gravity-only indicator (same method as the reviewed cutoff_test / r02): delta N field of the final
    packet at the 12 row radii, midplane, nphi azimuths; g_R = c^2 dR(dN)/(1+dN); returns azimuthal m0
    and m2/m4/m8 ratios.  Ignores pressure and the observation map: DIAGNOSTIC ONLY."""
    ph = 2 * np.pi * np.arange(nphi) / nphi
    P = np.array([[R * math.cos(t), R * math.sin(t), 0.0] for R in radii_m for t in ph])
    val = np.zeros(len(P), complex)
    gx = np.zeros(len(P), complex)
    gy = np.zeros(len(P), complex)
    ax_ = amp * (1j * k[:, 0])
    ay_ = amp * (1j * k[:, 1])
    for s in range(0, len(P), batch):
        e = np.exp(1j * (P[s:s + batch] @ k.T))
        val[s:s + batch] = e @ amp
        gx[s:s + batch] = e @ ax_
        gy[s:s + batch] = e @ ay_
    out = []
    imag_frac = float(np.max(np.abs(val.imag)) / max(np.max(np.abs(val.real)), 1e-300))
    for i, R in enumerate(radii_m):
        sl = slice(i * nphi, (i + 1) * nphi)
        g = C2 * (gx[sl].real * np.cos(ph) + gy[sl].real * np.sin(ph)) / (1 + val[sl].real)
        c = np.fft.fft(g) / nphi
        g0 = float(c[0].real)
        a = 2 * np.abs(c)
        den = abs(g0) if g0 != 0 else float('nan')
        rat = [float(a[m] / den) if math.isfinite(a[m] / den) else None for m in (2, 4, 8)]
        out.append({'R_kpc': R / KPC, 'g0_m_s2': g0, 'm2_over_m0': rat[0], 'm4_over_m0': rat[1], 'm8_over_m0': rat[2]})
    return {'rows': out, 'max_imag_over_real': imag_frac, 'scope': 'gravity-only ring indicator of the final field packet; diagnostic, not a gate'}


# --------------------------------------------------------------------------- comparison
def grid_edge(pre, gid):
    spec = pre['grids'][gid]['composite_grid_spec'] or BASE_SPEC
    return float(spec['breaks_inverse_kpc'][-1])


def dmax(va, vb, ids):
    d = [vb[i] - va[i] for i in ids]
    return max(abs(x) for x in d), d


def evaluate(pre, adapted, packets):
    crit = pre['criterion']
    tau, tau_p, tau_in, tau_sh = crit['tau_km_s'], crit['tau_picard_km_s'], crit['tau_inner_km_s'], crit['tau_shape_agreement_km_s']
    ids = pre['row_ids']
    sig = dict(zip(ids, pre['quoted_sigma_km_s']))
    cases = {c['id']: c for c in pre['cases']}
    gates = {}
    # common block reference = first available case in registered order
    ref = next((adapted[c['id']] for c in pre['cases'] if c['id'] in adapted), None)
    for cid, c in cases.items():
        if cid not in adapted:
            gates[cid] = {'present': False, 'valid_all': False, 'failed': ['missing']}
            continue
        a = adapted[cid]
        ns = a['normalized_spec']
        g = {}
        g['V1'] = bool(a['schema'] == RESULT_SCHEMA and a['status'] == 'COMPLETED' and a['valid'] is True
                       and sorted(a['rows']) == sorted(ids) and all(isinstance(a['rows'][i], (int, float)) and math.isfinite(a['rows'][i]) for i in ids))
        g['V2'] = bool(a['last_change_km_s'] is not None and a['last_change_km_s'] <= tau_p)
        reg_grid = pre['grids'][c['grid']]['composite_grid_spec']
        tr = a['truncation'] or {}
        shape_ok = tr.get('shape') == c['shape'] and (tr.get('kmax_inverse_kpc') == c['kmax_inverse_kpc'])
        common_ok = ref is not None and all(ns.get(k) == ref['normalized_spec'].get(k) for k in COMMON_KEYS) and \
            all((ns.get('numerics') or {}).get(k) == (ref['normalized_spec'].get('numerics') or {}).get(k) for k in COMMON_NUMERICS) and \
            a['driver_sha256'] == ref['driver_sha256'] and (ns.get('coefficients') or {}).get('sha256') == A2_SHA
        g['V3'] = bool(a['grid_spec'] == reg_grid and shape_ok and common_ok)
        pk = packets.get(cid) or {}
        g['V4'] = bool(pk.get('V4'))
        g['V5'] = bool(pk.get('V5'))
        if c['prefix'].startswith('admit:'):
            cube = c['prefix'].split(':')[1]
            g['V6'] = bool(cube in adapted and a['route_a_identity_sha256'] is not None
                           and a['route_a_identity_sha256'] == adapted[cube]['route_a_identity_sha256'])
        g['present'] = True
        g['failed'] = [k for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V6') if k in g and not g[k]]
        g['valid_all'] = not g['failed']
        gates[cid] = g
    ok = {cid for cid, g in gates.items() if g['valid_all']}
    v = {cid: adapted[cid]['rows'] for cid in ok}
    key = {(c['shape'], int(round(c['kmax_inverse_kpc'] or grid_edge(pre, c['grid'])))): cid
           for cid, c in cases.items() if c['grid'] in ('G2', 'G3', 'G4')}
    seq = {}
    for A in SHAPES:
        cid = {K: key[(A, K)] for K in KS}
        entry = {'cases': cid}
        for K1, K2 in ((2, 3), (3, 4)):
            a_, b_ = cid[K1], cid[K2]
            if a_ in ok and b_ in ok:
                D, d = dmax(v[a_], v[b_], ids)
                entry['D_%d_%d' % (K1, K2)] = D
                entry['delta_%d_%d' % (K1, K2)] = dict(zip(ids, d))
                entry['rel_%d_%d' % (K1, K2)] = {i: d[j] / v[b_][i] for j, i in enumerate(ids)}
                entry['delta_over_sigma_%d_%d' % (K1, K2)] = {i: d[j] / sig[i] for j, i in enumerate(ids)}
        need = [cid[K] for K in KS]
        if not all(x in ok for x in need):
            entry['pass'] = None
            entry['why'] = 'INCOMPLETE: invalid or missing %s' % [x for x in need if x not in ok]
        else:
            p = entry['D_3_4'] <= tau and entry['D_3_4'] < entry['D_2_3']
            entry['pass'] = bool(p)
            entry['why'] = 'D_3_4=%.4g (tau %.4g), D_2_3=%.4g, contracting=%s' % (entry['D_3_4'], tau, entry['D_2_3'], entry['D_3_4'] < entry['D_2_3'])
        seq[A] = entry
    inner = {'cases': ['C2', 'R']}
    if 'C2' in ok and 'R' in ok:
        D, d = dmax(v['C2'], v['R'], ids)
        inner.update(D_R=D, delta=dict(zip(ids, d)), pass_=bool(D <= tau_in))
    else:
        inner.update(pass_=None, why='INCOMPLETE: %s' % [x for x in ('C2', 'R') if x not in ok])
    shapes_k4 = {}
    for i, A in enumerate(SHAPES):
        for B in SHAPES[i + 1:]:
            a_, b_ = key[(A, 4)], key[(B, 4)]
            if a_ in ok and b_ in ok:
                shapes_k4[A + '_vs_' + B] = dmax(v[a_], v[b_], ids)[0]
    # ---------------- decision (pre-registered order)
    dec = {'outcome': None, 'reasons': [], 'next_step': None}
    passing = [A for A in SHAPES if seq[A]['pass'] is True]
    bad_cases = sorted(cid for cid, g in gates.items() if not g['valid_all'])
    if bad_cases:   # rule 1: every registered case is needed by rules 2-5
        dec.update(outcome='INCOMPLETE', next_step='Rerun only the named cases (same spec, fresh outdir); no threshold or rule change.')
        dec['reasons'] += ['%s failed %s' % (cid, gates[cid]['failed']) for cid in bad_cases]
    elif inner.get('pass_') is False:
        dec.update(outcome='INNER_UNRESOLVED', next_step='Raise inner panel orders on the adopted grid (needs prep node budget > 96 and review).')
        dec['reasons'].append('D_R=%.4g > tau_inner=%.4g' % (inner['D_R'], tau_in))
    elif not passing:
        best = min(SHAPES, key=lambda A: seq[A].get('D_3_4', float('inf')))
        dec.update(outcome='NOT_CONVERGED',
                   next_step='Extend %s to 5 and 6 /kpc with order-6 unit outer panels (108/120 nodes per axis); needs a reviewed prep successor with node budget >= 120 and a per-call cap >= 6 GiB.' % best)
        dec['reasons'] += ['%s: %s' % (A, seq[A]['why']) for A in SHAPES]
    else:
        bad = [(A, B, shapes_k4[A + '_vs_' + B]) for i, A in enumerate(SHAPES) for B in SHAPES[i + 1:]
               if A in passing and B in passing and shapes_k4.get(A + '_vs_' + B, 0.0) > tau_sh]
        if bad:
            best = min(passing, key=lambda A: seq[A]['D_3_4'])
            dec.update(outcome='NOT_CONVERGED', next_step='SHAPE_DISAGREEMENT: extend %s to 5 and 6 /kpc (prep budget >= 120).' % best)
            dec['reasons'] += ['%s vs %s differ by %.4g > %.4g at K=4' % (b[0], b[1], b[2], tau_sh) for b in bad]
        else:
            m4 = {A: adapted[key[(A, 4)]]['harm_m4'] for A in passing}
            if any(x is None for x in m4.values()):
                order = sorted(passing, key=lambda A: seq[A]['D_3_4'])
                dec['reasons'].append('m4 harmonic missing for some passing shape; ordered by D_3_4')
            else:
                order = sorted(passing, key=lambda A: m4[A])
                if len(order) > 1 and m4[order[1]] <= 1.1 * m4[order[0]]:
                    order[:2] = sorted(order[:2], key=lambda A: seq[A]['D_3_4'])
                    dec['reasons'].append('m4 of %s and %s within 10%%: tie broken by smaller D_3_4' % (order[0], order[1]))
            star = order[0]
            u = {i: abs(seq[star]['delta_3_4'][i]) + abs(inner['delta'][i]) for i in ids}
            dec.update(outcome='ADOPT', adopted_shape=star, adopted_kmax_inverse_kpc=4.0, adopted_grid='G4',
                       carried_numerical_uncertainty_km_s=u, m4_at_K4=m4,
                       next_step='Run calibration calls with truncation %s K=4 on grid G4 (96/axis, prep v008); carry u_i.' % star)
            dec['reasons'].append('passing shapes %s; adopted %s by smallest measured m4 at K=4' % (passing, star))
    return {'gates': gates, 'sequences': seq, 'inner_control': inner, 'shape_spread_K4_km_s': shapes_k4, 'decision': dec}


def table_text(pre, adapted, ok, field):
    ids = pre['row_ids']
    order = [c['id'] for c in pre['cases']]
    lines = ['row               ' + ' '.join('%9s' % c for c in order)]
    for i in ids:
        lines.append('%-17s ' % i[-8:] + ' '.join(('%9.4f' % adapted[c]['rows'][i]) if c in ok else '%9s' % '-' for c in order))
    if field:
        lines.append('')
        lines.append('gravity-only ring g0 relative to C2 (diagnostic):')
        if 'C2' in field and field['C2']:
            base = [r['g0_m_s2'] for r in field['C2']['rows']]
            for j, i in enumerate(ids):
                lines.append('%-17s ' % i[-8:] + ' '.join(('%+9.4f' % (field[c]['rows'][j]['g0_m_s2'] / base[j] - 1)) if field.get(c) else '%9s' % '-' for c in order))
    return '\n'.join(lines) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--prereg', required=True)
    ap.add_argument('--cases', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--no-field-diagnostic', action='store_true')
    ap.add_argument('--test-allow-unpinned-prereg', action='store_true', help='synthetic tests only; output is marked TEST')
    a = ap.parse_args(argv)
    out = Path(a.outdir)
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    psha = sha256_file(a.prereg)
    if psha != PREREG_SHA256 and not a.test_allow_unpinned_prereg:
        print('REFUSED: prereg sha %s is not the pinned %s' % (psha, PREREG_SHA256), file=sys.stderr)
        return 2
    pre = json.loads(Path(a.prereg).read_text())
    rb = pre['binding_inputs']['row_binding']
    radii = None
    if Path(rb['path']).is_file() and sha256_file(rb['path']) == rb['sha256']:
        q = json.loads(Path(rb['path']).read_text())['query_rows']
        if [x['id'] for x in q] == pre['row_ids']:
            radii = [x['radius_m'] for x in q]
    cases_map = json.loads(Path(a.cases).read_text())
    cases = {c['id']: c for c in pre['cases']}
    unknown = sorted(set(cases_map) - set(cases))
    if unknown:
        print('REFUSED: unregistered case ids %s' % unknown, file=sys.stderr)
        return 2
    adapted, packets, field, errors = {}, {}, {}, {}
    for cid, path in cases_map.items():
        try:
            adapted[cid] = adapt_result(path)
        except Exception as exc:
            errors[cid] = '%s: %s' % (type(exc).__name__, exc)
            continue
        grid_spec = pre['grids'][cases[cid]['grid']]['composite_grid_spec']
        try:
            chk, diag = packet_checks(adapted[cid], cases[cid], grid_spec, radii, (not a.no_field_diagnostic) and radii is not None)
        except Exception as exc:
            chk, diag = {'V4': False, 'V5': False, 'reason': '%s: %s' % (type(exc).__name__, exc)}, None
        packets[cid], field[cid] = chk, diag
    ev = evaluate(pre, adapted, packets)
    ok = {c for c, g in ev['gates'].items() if g['valid_all']}
    k0 = {}
    for c in adapted:
        K = adapted[c]['base_K_values_SI']
        if K and adapted.get('C2', {}).get('base_K_values_SI'):
            b = np.asarray(adapted['C2']['base_K_values_SI'], float)
            k0[c] = float(np.max(np.abs(np.asarray(K, float) / b - 1)))
    report = {'schema': 'UNT_KMAX_COMPARISON_C2_0470_V001', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'test_mode': bool(psha != PREREG_SHA256), 'prereg': {'path': str(Path(a.prereg).resolve()), 'sha256': psha},
              'script_sha256': sha256_file(__file__), 'cases_file': {'path': str(Path(a.cases).resolve()), 'sha256': sha256_file(a.cases)},
              'inputs': {c: {'result': adapted[c]['result_path'], 'result_sha256': adapted[c]['result_sha256'],
                             'final_pass': adapted[c]['final_pass'], 'last_change_km_s': adapted[c]['last_change_km_s'],
                             'harm_m4': adapted[c]['harm_m4'], 'harm_m8': adapted[c]['harm_m8'],
                             'elapsed_seconds': adapted[c]['elapsed_seconds']} for c in adapted},
              'read_errors': errors, 'packet_checks': packets,
              'rows_km_s': {c: adapted[c]['rows'] for c in adapted},
              'K0_max_rel_diff_vs_C2': k0,
              'field_diagnostic': field, **ev}
    out.mkdir(parents=True)
    with open(out / 'KMAX_COMPARISON.json', 'x') as f:
        json.dump(report, f, indent=1, allow_nan=False, default=float)
        f.write('\n')
    txt = table_text(pre, adapted, ok, field if not a.no_field_diagnostic else None)
    txt += '\nDECISION: %s\n' % json.dumps(ev['decision'], indent=1, default=float)
    with open(out / 'KMAX_COMPARISON_TABLE.txt', 'x') as f:
        f.write(txt)
    print(txt)
    return 0


if __name__ == '__main__':
    sys.exit(main())
