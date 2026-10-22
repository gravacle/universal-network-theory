"""P-88 k_max / truncation-shape comparison and pre-registered decision, V002 (Claude2 lane, c2v002).

Supersedes kmax_compare_c2v001.py (925b7010...).  Applies KMAX_MATRIX_PREREG_V003.json (sha pinned
below): per-row tau_i = 0.25 sigma_i, normalized statistic Dhat, contraction q <= 1/2 (CHECK D1),
shape-spread term in u_i (D2), V5 nonzero-row gate (D3), per-gate next steps (D6), bracket recovery
block (D7), V3 against the REGISTERED block with the modal block reported (D8), m4 at the row window
(D13), driver allowance by grid (root c) and the C2 Picard-equivalence exception (root d).
Read-only on all inputs; writes only into a NEW --outdir.  numpy only, single thread.
It never opens observed velocities: sigma values are taken from the pre-registration.

usage:
  python3 -I -B kmax_compare_c2v002.py --prereg KMAX_MATRIX_PREREG_V003.json \
      --cases CASES.json --outdir NEW_DIR [--bracket-recovery RECOVERY.json] [--no-field-diagnostic]
CASES.json: {"C2": "<A2_ANCHOR_F3_RUN_V001>/result.json", "C3": "...", ...}  (missing cases allowed;
the decision then reports INCOMPLETE naming them).
RECOVERY.json (only after a declared D7 recovery): {"brackets": {<normalized brackets block>}, "reason": "..."}

The ONLY schema-dependent code is adapt_result() (driver schema UNT_GALAXY_M0_FORWARD_RESULT_C2V001,
unchanged in v003).
"""
import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

PREREG_SHA256 = '8e36b64355f75a49a40c15f3e842f089740aae94547d66a709033bd9d66cddab'
RESULT_SCHEMA = 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001'
KPC = 3.085677581491367e19
C2 = 299792458.0 ** 2
BASE_SPEC = {'breaks_inverse_kpc': [-2, -1, -0.3, -0.1, -0.03, -0.01, 0, 0.01, 0.03, 0.1, 0.3, 1, 2], 'panel_orders': [6] * 12}
SHAPES = ('cube', 'sphere', 'cylinder')
KS = (2, 3, 4)
M4_WINDOW_KPC = (0.4, 6.0)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


# --------------------------------------------------------------------------- the single adapter
def adapt_result(result_path):
    """Map one driver result.json (+ the stage files it points to) onto the fields this script uses."""
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
    m4w = None
    prm, rad = harm.get('per_radius_max'), harm.get('radial_nodes_m')
    if isinstance(prm, list) and isinstance(rad, list) and len(prm) == len(rad):
        vals = [x.get('m4') for x, R in zip(prm, rad)
                if M4_WINDOW_KPC[0] <= R / KPC <= M4_WINDOW_KPC[1] and isinstance(x.get('m4'), (int, float)) and math.isfinite(x['m4'])]
        m4w = max(vals) if vals else None
    return {
        'result_path': str(rp), 'result_sha256': sha256_file(rp), 'schema': r.get('schema'),
        'status': r.get('status'), 'valid': r.get('valid'), 'reasons': r.get('reasons'),
        'driver_sha256': r.get('driver_sha256'), 'call_spec_sha256': r.get('call_spec_sha256'),
        'rows': {x['id']: x['speed_km_s'] for x in (r.get('rows') or [])},
        'normalized_spec': ns,
        'grid_spec': num.get('composite_grid_spec'), 'truncation': num.get('truncation'), 'picard': num.get('picard'),
        'final_pass': r.get('final_pass'), 'last_change_km_s': last.get('max_abs_change_km_s'),
        'per_pass_rows': [{'pass': p.get('pass'), 'max_abs_change_km_s': p.get('max_abs_change_km_s')} for p in passes],
        'field_packet': packet, 'route_a_identity_sha256': ident.get('identity_sha256'),
        'harm_m4_global': (harm.get('global_max') or {}).get('m4'), 'harm_m8_global': (harm.get('global_max') or {}).get('m8'),
        'm4_row_window': m4w, 'base_K_values_SI': base_K, 'elapsed_seconds': r.get('elapsed_seconds')}


# --------------------------------------------------------------------------- grid / mask helpers
def expected_axis(grid_spec):
    spec = grid_spec or BASE_SPEC
    parts = []
    for lo, hi, n in zip(spec['breaks_inverse_kpc'][:-1], spec['breaks_inverse_kpc'][1:], spec['panel_orders']):
        x, _ = np.polynomial.legendre.leggauss(n)
        parts.append(((lo + hi) / 2 + (hi - lo) * x / 2) / KPC)
    return np.concatenate(parts)


def driver_mask(k, shape, kmax_inverse_m):
    """Identical expression to galaxy_m0_forward_c2v001/v003 truncation_mask (|k| or k_perp <= kmax)."""
    if shape == 'cube':
        return np.ones(len(k), dtype=bool)
    if shape == 'sphere':
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1] + k[:, 2] * k[:, 2])
    else:
        r = np.sqrt(k[:, 0] * k[:, 0] + k[:, 1] * k[:, 1])
    return r <= kmax_inverse_m


def packet_checks(a, case, grid_spec, radii_m, field_diag):
    """V4 (grid), V5 (mask, incl. the D3 nonzero-row gate) and the gravity-only ring diagnostic."""
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
    g = np.stack(np.meshgrid(ax, ax, ax, indexing='ij'), -1).reshape(-1, 3)
    expect_kept = int(np.count_nonzero(driver_mask(g, case['shape'], kmax_kpc / KPC)))
    kept_nonzero = int(np.count_nonzero(np.any(w.reshape(len(w), -1) != 0, axis=1)))
    chk = {'V4': v4, 'V5': bool(outside_zero and kept_nonzero == expect_kept), 'outside_rows_all_zero': outside_zero,
           'nodes': int(len(k)), 'axis_nodes_expected': n, 'mask_kept_expected': expect_kept, 'mask_kept_in_packet': int(m.sum()),
           'nonzero_rows_in_packet': kept_nonzero, 'packet_sha256': pk['sha256']}
    diag = ring_diagnostic(k, w[:, 0, 0], radii_m) if field_diag else None
    return chk, diag


def ring_diagnostic(k, amp, radii_m, nphi=32, batch=8):
    """Gravity-only indicator (unchanged from c2v001): delta N field of the final packet at the 12 row radii,
    midplane, nphi azimuths; g_R = c^2 dR(dN)/(1+dN); azimuthal m0 and m2/m4/m8 ratios.  DIAGNOSTIC ONLY."""
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


def diffs(va, vb, ids, tau):
    d = [vb[i] - va[i] for i in ids]
    D = max(abs(x) for x in d)
    Dhat = max(abs(x) / tau[i] for x, i in zip(d, ids))
    return D, Dhat, d


def common_block(ns):
    num = ns.get('numerics') or {}
    pc = dict(num.get('picard') or {})
    return {'galaxy': ns.get('galaxy'), 'physical': ns.get('physical'), 'coefficients': ns.get('coefficients'),
            'brackets': num.get('brackets'), 'picard_bound': pc.get('speed_change_bound_km_s'),
            'picard_observe_every_pass': pc.get('observe_every_pass'), 'picard_passes': pc.get('passes')}


def evaluate(pre, adapted, packets, bracket_block):
    crit = pre['criterion']
    tau_p = crit['tau_picard_km_s']
    ids = pre['row_ids']
    sig = dict(zip(ids, pre['quoted_sigma_km_s']))
    tau = dict(zip(ids, pre['tau_km_s']))
    cases = {c['id']: c for c in pre['cases']}
    anc = pre['anchor']
    drivers = {k: v['sha256'] for k, v in pre['binding_inputs']['drivers'].items()}
    sha2drv = {v: k for k, v in drivers.items()}
    reg = {'galaxy': 'DDO154', 'physical': anc['physical'], 'coefficients': anc['coefficients'],
           'brackets': bracket_block, 'picard_bound': anc['picard']['speed_change_bound_km_s'],
           'picard_observe_every_pass': anc['picard']['observe_every_pass']}
    # modal block (diagnostic, D8)
    blocks = {cid: canon({k: v for k, v in common_block(a['normalized_spec']).items() if k != 'picard_passes'}) for cid, a in adapted.items()}
    cnt = Counter(blocks.values())
    modal = cnt.most_common(1)[0][0] if cnt else None
    modal_info = {'n_distinct_blocks': len(cnt), 'modal_count': cnt.most_common(1)[0][1] if cnt else 0,
                  'modal_equals_registered': modal == canon(reg) if modal else None,
                  'cases_off_modal': sorted(c for c, b in blocks.items() if b != modal)}
    gates = {}
    for cid, c in cases.items():
        if cid not in adapted:
            gates[cid] = {'present': False, 'valid_all': False, 'failed': ['missing'], 'notes': []}
            continue
        a = adapted[cid]
        ns = a['normalized_spec']
        g = {'notes': []}
        g['V1'] = bool(a['schema'] == RESULT_SCHEMA and a['status'] == 'COMPLETED' and a['valid'] is True
                       and sorted(a['rows']) == sorted(ids) and all(isinstance(a['rows'][i], (int, float)) and math.isfinite(a['rows'][i]) for i in ids))
        g['V2'] = bool(a['last_change_km_s'] is not None and a['last_change_km_s'] <= tau_p)
        reg_grid = pre['grids'][c['grid']]['composite_grid_spec']
        tr = a['truncation'] or {}
        shape_ok = tr.get('shape') == c['shape'] and tr.get('kmax_inverse_kpc') == c['kmax_inverse_kpc']
        cb = common_block(ns)
        mism = [k for k in reg if canon(cb.get(k)) != canon(reg[k])]
        passes = cb['picard_passes']
        if passes == anc['picard']['passes']:
            picard_ok = True
        elif cid == 'C2' and passes == cases['C2']['bound_call']['picard_passes'] and a['last_change_km_s'] is not None \
                and a['last_change_km_s'] <= anc['picard']['speed_change_bound_km_s']:
            picard_ok = True
            g['notes'].append('C2 passes %d admitted under picard_equivalence (final change %.4g <= bound)' % (passes, a['last_change_km_s']))
        else:
            picard_ok = False
            mism.append('PICARD_CAP_NOT_EQUIVALENT' if cid == 'C2' else 'picard_passes')
        drv = sha2drv.get(a['driver_sha256'])
        driver_ok = drv in c['drivers_allowed']
        if not driver_ok:
            mism.append('driver %s not in %s' % (drv or a['driver_sha256'], c['drivers_allowed']))
        if a['grid_spec'] != reg_grid:
            mism.append('grid')
        if not shape_ok:
            mism.append('truncation')
        g['V3'] = bool(not mism and picard_ok and driver_ok)
        g['V3_mismatch'] = mism
        g['driver'] = drv
        if cid == 'C2':
            bc = c['bound_call']
            g['notes'].append('C2 call_spec_sha256 %s bound call spec (%s)' % ('==' if a['call_spec_sha256'] == bc['call_spec_sha256'] else '!=', bc['call_spec_sha256'][:16]))
        pk = packets.get(cid) or {}
        g['V4'] = bool(pk.get('V4'))
        g['V5'] = bool(pk.get('V5'))
        if c['prefix'].startswith('admit:'):
            cube = c['prefix'].split(':')[1]
            g['V6'] = bool(cube in adapted and a['route_a_identity_sha256'] is not None
                           and a['route_a_identity_sha256'] == adapted[cube]['route_a_identity_sha256']
                           and a['driver_sha256'] == adapted[cube]['driver_sha256'])
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
                D, Dh, d = diffs(v[a_], v[b_], ids, tau)
                tag = '%d_%d' % (K1, K2)
                entry['D_' + tag] = D
                entry['Dhat_' + tag] = Dh
                entry['delta_' + tag] = dict(zip(ids, d))
                entry['delta_over_tau_' + tag] = {i: d[j] / tau[i] for j, i in enumerate(ids)}
                entry['delta_over_sigma_' + tag] = {i: d[j] / sig[i] for j, i in enumerate(ids)}
                entry['rel_' + tag] = {i: d[j] / v[b_][i] for j, i in enumerate(ids)}
        need = [cid[K] for K in KS]
        if not all(x in ok for x in need):
            entry['pass'] = None
            entry['why'] = 'INCOMPLETE: invalid or missing %s' % [x for x in need if x not in ok]
        else:
            d23, d34 = entry['delta_2_3'], entry['delta_3_4']
            tail = {}
            for i in ids:
                q = abs(d34[i]) / abs(d23[i]) if d23[i] != 0 else float('inf')
                tail[i] = {'q': q if math.isfinite(q) else None,
                           'tail_km_s': abs(d34[i]) * q / (1 - q) if q < 1 else None,
                           'tail_over_tau': abs(d34[i]) * q / (1 - q) / tau[i] if q < 1 else None,
                           'non_contracting': not q < 1}
            qs = entry['Dhat_3_4'] / entry['Dhat_2_3'] if entry['Dhat_2_3'] > 0 else float('inf')
            entry['tail_diagnostic'] = {'per_row': tail, 'q_sequence': qs if math.isfinite(qs) else None,
                                        'tail_sequence_Dhat': entry['Dhat_3_4'] * qs / (1 - qs) if qs < 1 else None,
                                        'scope': 'diagnostic only; never adopted'}
            p = entry['Dhat_3_4'] <= 1.0 and entry['Dhat_3_4'] <= 0.5 * entry['Dhat_2_3']
            entry['pass'] = bool(p)
            entry['why'] = 'Dhat_3_4=%.4g (<=1: %s), Dhat_2_3=%.4g, q=%.4g (<=0.5: %s)' % (
                entry['Dhat_3_4'], entry['Dhat_3_4'] <= 1.0, entry['Dhat_2_3'], qs, entry['Dhat_3_4'] <= 0.5 * entry['Dhat_2_3'])
        seq[A] = entry
    inner = {'cases': ['C2', 'R']}
    if 'C2' in ok and 'R' in ok:
        D, Dh, d = diffs(v['C2'], v['R'], ids, tau)
        inner.update(D_R=D, Dhat_R=Dh, delta=dict(zip(ids, d)), delta_over_tau={i: d[j] / tau[i] for j, i in enumerate(ids)}, pass_=bool(Dh <= 1.0))
    else:
        inner.update(pass_=None, why='INCOMPLETE: %s' % [x for x in ('C2', 'R') if x not in ok])
    shapes_k4 = {}
    for i, A in enumerate(SHAPES):
        for B in SHAPES[i + 1:]:
            a_, b_ = key[(A, 4)], key[(B, 4)]
            if a_ in ok and b_ in ok:
                D, Dh, _ = diffs(v[a_], v[b_], ids, tau)
                shapes_k4[A + '_vs_' + B] = {'D_km_s': D, 'Dhat': Dh}
    # ---------------- decision (pre-registered order)
    steps = crit['gate_next_steps']
    dec = {'outcome': None, 'reasons': [], 'next_step': None}
    passing = [A for A in SHAPES if seq[A]['pass'] is True]
    bad_cases = sorted(cid for cid, g in gates.items() if not g['valid_all'])
    if bad_cases:   # rule 1
        nxt = {}
        for cid in bad_cases:
            dec['reasons'].append('%s failed %s%s' % (cid, gates[cid]['failed'],
                                  (' V3:%s' % gates[cid].get('V3_mismatch')) if 'V3' in gates[cid]['failed'] else ''))
            nxt[cid] = {gt: (steps.get(gt) if gt != 'missing' else 'Run the registered case (spec from this directory).') for gt in gates[cid]['failed']}
        dec.update(outcome='INCOMPLETE', next_step=nxt)
    elif inner.get('pass_') is False:
        dec.update(outcome='INNER_UNRESOLVED', next_step=pre['criterion']['decision_rule'][1])
        dec['reasons'].append('Dhat_R=%.4g > 1' % inner['Dhat_R'])
    elif not passing:
        best = min(SHAPES, key=lambda A: seq[A].get('Dhat_3_4', float('inf')))
        dec.update(outcome='NOT_CONVERGED', extend_shape=best,
                   next_step='Extend %s to 5 and 6 /kpc with order-6 unit outer panels (108/120 nodes per axis); needs a prep successor with node budget >= 120 and a per-call cap >= 6 GiB, under separate review.' % best)
        dec['reasons'] += ['%s: %s' % (A, seq[A]['why']) for A in SHAPES]
    else:
        bad = [(A, B, shapes_k4[A + '_vs_' + B]['Dhat']) for i, A in enumerate(SHAPES) for B in SHAPES[i + 1:]
               if A in passing and B in passing and shapes_k4[A + '_vs_' + B]['Dhat'] > 2.0]
        if bad:
            best = min(passing, key=lambda A: seq[A]['Dhat_3_4'])
            dec.update(outcome='NOT_CONVERGED', subtype='SHAPE_DISAGREEMENT', extend_shape=best,
                       next_step='SHAPE_DISAGREEMENT: extend %s to 5 and 6 /kpc (prep successor node budget >= 120, cap >= 6 GiB, separate review).' % best)
            dec['reasons'] += ['%s vs %s differ by Dhat %.4g > 2 at K=4' % b for b in bad]
        else:
            m4 = {A: adapted[key[(A, 4)]]['m4_row_window'] for A in passing}
            if any(x is None for x in m4.values()):
                cand = list(passing)
                dec['reasons'].append('m4 row-window statistic missing for %s: candidates = all passing shapes' % [A for A in passing if m4[A] is None])
            else:
                lo = min(m4.values())
                cand = [A for A in passing if m4[A] <= 1.10 * lo]
            star = sorted(cand, key=lambda A: (seq[A]['Dhat_3_4'], SHAPES.index(A)))[0]
            spread = {i: max(abs(v[key[(A, 4)]][i] - v[key[(star, 4)]][i]) for A in passing) for i in ids}
            u = {i: abs(seq[star]['delta_3_4'][i]) + abs(inner['delta'][i]) + spread[i] for i in ids}
            dec.update(outcome='ADOPT', adopted_shape=star, adopted_kmax_inverse_kpc=4.0, adopted_grid='G4',
                       m4_row_window_at_K4=m4, m4_candidates=cand,
                       carried_numerical_uncertainty_km_s=u,
                       carried_terms={'K34': {i: abs(seq[star]['delta_3_4'][i]) for i in ids}, 'inner': {i: abs(inner['delta'][i]) for i in ids},
                                      'shape_spread': spread},
                       u_over_tau={i: u[i] / tau[i] for i in ids}, u_over_sigma={i: u[i] / sig[i] for i in ids},
                       next_step='Run calibration calls with truncation %s K=4 on grid G4 (96/axis, driver v003, prep v008); carry u_i; S1 transfer test at the calibrated point before prediction.' % star)
            dec['reasons'].append('passing shapes %s; m4 candidates %s; adopted %s by smallest Dhat_3_4' % (passing, cand, star))
    return {'gates': gates, 'modal_common_block': modal_info, 'sequences': seq, 'inner_control': inner, 'shape_spread_K4': shapes_k4, 'decision': dec}


def table_text(pre, adapted, ok, field):
    ids = pre['row_ids']
    order = [c['id'] for c in pre['cases']]
    lines = ['row      tau_i  ' + ' '.join('%9s' % c for c in order)]
    for i, t in zip(ids, pre['tau_km_s']):
        lines.append('%-8s %6.3f ' % (i[-2:], t) + ' '.join(('%9.4f' % adapted[c]['rows'][i]) if c in ok else '%9s' % '-' for c in order))
    if field:
        lines.append('')
        lines.append('gravity-only ring g0 relative to C2 (diagnostic):')
        if field.get('C2'):
            base = [r['g0_m_s2'] for r in field['C2']['rows']]
            for j, i in enumerate(ids):
                lines.append('%-15s ' % i[-2:] + ' '.join(('%+9.4f' % (field[c]['rows'][j]['g0_m_s2'] / base[j] - 1)) if field.get(c) else '%9s' % '-' for c in order))
    return '\n'.join(lines) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--prereg', required=True)
    ap.add_argument('--cases', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--bracket-recovery')
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
    bracket_block, recovery = pre['anchor']['brackets'], None
    if a.bracket_recovery:
        rec = json.loads(Path(a.bracket_recovery).read_text())
        if set(rec) != {'brackets', 'reason'} or rec['brackets'].get('mode') != 'rule':
            print('REFUSED: bracket recovery file must be {"brackets": {rule block}, "reason": str}', file=sys.stderr)
            return 2
        bracket_block = rec['brackets']
        recovery = {'path': str(Path(a.bracket_recovery).resolve()), 'sha256': sha256_file(a.bracket_recovery), 'reason': rec['reason'],
                    'changed_rule_keys': sorted(k for k in set(bracket_block['rule']) | set(pre['anchor']['brackets']['rule'])
                                                if canon(bracket_block['rule'].get(k)) != canon(pre['anchor']['brackets']['rule'].get(k)))}
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
    ev = evaluate(pre, adapted, packets, bracket_block)
    ok = {c for c, g in ev['gates'].items() if g['valid_all']}
    k0 = {}
    for c in adapted:
        K = adapted[c]['base_K_values_SI']
        if K and adapted.get('C2', {}).get('base_K_values_SI'):
            b = np.asarray(adapted['C2']['base_K_values_SI'], float)
            k0[c] = float(np.max(np.abs(np.asarray(K, float) / b - 1)))
    report = {'schema': 'UNT_KMAX_COMPARISON_C2_V002', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'test_mode': bool(psha != PREREG_SHA256), 'prereg': {'path': str(Path(a.prereg).resolve()), 'sha256': psha},
              'script_sha256': sha256_file(__file__), 'cases_file': {'path': str(Path(a.cases).resolve()), 'sha256': sha256_file(a.cases)},
              'bracket_recovery': recovery,
              'inputs': {c: {'result': adapted[c]['result_path'], 'result_sha256': adapted[c]['result_sha256'],
                             'driver_sha256': adapted[c]['driver_sha256'], 'call_spec_sha256': adapted[c]['call_spec_sha256'],
                             'final_pass': adapted[c]['final_pass'], 'last_change_km_s': adapted[c]['last_change_km_s'],
                             'm4_row_window': adapted[c]['m4_row_window'], 'harm_m4_global': adapted[c]['harm_m4_global'],
                             'harm_m8_global': adapted[c]['harm_m8_global'], 'elapsed_seconds': adapted[c]['elapsed_seconds']} for c in adapted},
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
