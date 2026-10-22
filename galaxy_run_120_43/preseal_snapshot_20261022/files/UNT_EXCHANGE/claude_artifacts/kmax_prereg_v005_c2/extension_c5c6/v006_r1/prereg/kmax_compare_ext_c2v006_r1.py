"""P-88 k_max EXTENSION comparison and pre-registered decision (prereg V006 R1), Claude2 lane extension_c5c6.

Successor of kmax_compare_ext_c2v006.py (e6475f38, which pinned the V006 draft f90ab96c).  Applies
KMAX_MATRIX_PREREG_V006_R1.json (sha pinned below; --test-allow-unpinned-prereg for synthetic tests only, output marked TEST).
Changes against e6475f38, each one finding of extension_c5c6/check/CHECK_V001.md (849d1b8d) and nothing else:
  M1  no code change: the V3 route-A term reads cases[].route_a_numerics from the prereg, which R1 sets to max_iterations 32.
  L1  for every prefix 'bound' case (C4, C3, C2, R) the adapted result_sha256 must equal cases[].bound.result.sha256 when the
      --bracket-recovery block equals the registered R3 block (V3 mismatch 'bound_result_sha256 ...'); under a later R(n)
      the bound sha is reported, not enforced (C4 is then rerun as C4R(n)).
  L2  V005's v005-admissibility condition (V005 amendment_v005.driver.admissibility_condition) is executed at comparison
      time with the pinned V005 compare's v005_admissibility(V005 prereg); a v005 case (C4, C3, R) that is not admissible
      fails V3 with V005_INADMISSIBLE:<reason> and gets V005's inadmissible_next_step, as in V005.
  L3  V005's diagnostics are carried: K0_max_rel_diff_vs_C2 and field_diagnostic (the gravity-only ring indicator of each
      final field packet, V005 packet_checks/ring_diagnostic), reported, never decided; --no-field-diagnostic now disables
      the ring diagnostic and its table block (in e6475f38 the flag was a no-op).
  L4  reported only: for C5/C6, which registered outdir (primary_N8 / alternate_N1) the result lies in.
Unchanged from e6475f38: V005's statistics (tau_i = 0.25 sigma_i, Dhat(K1,K2) = max_i |v_i(K2)-v_i(K1)|/tau_i, pass iff
Dhat(5,6) <= 1 and Dhat(5,6) <= 0.5 Dhat(4,5), Picard gate 0.0125 km/s; per-row tail diagnostic reported, never adopted),
gates V1-V5 and V7, the v009 admissibility condition, the decision order X1-X4.  The pinned V005 compare script supplies
adapt_result, packet_checks, ring_diagnostic, diffs, validate_recovery and v005_admissibility unchanged.
Read-only on all inputs; writes only into a NEW --outdir.  numpy only.  Never opens observed velocities (sigma is in the prereg).

usage:
  python3 -I -B kmax_compare_ext_c2v006_r1.py --prereg KMAX_MATRIX_PREREG_V006_R1.json --cases CASES_EXT.json --outdir NEW_DIR \
      --bracket-recovery <R3 or a later R(n) recovery file> [--no-field-diagnostic]
CASES_EXT.json: {"C4": "<C4 result.json>", "C5": "...", "C6": "...", "C3": "...", "C2": "...", "R": "..."}; C3, C2, R are the
R3 results (diagnostic / carried inner control); a missing C4/C5/C6 makes the decision INCOMPLETE naming it.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

PREREG_SHA256 = '807fc5bfcb24ee779137746db3536f41dd97c16bd5f367f79ad5a1b8c3ec067c'
SHAPE = 'cube'
EXT_IDS = ('C4', 'C5', 'C6')
DIAG_IDS = ('C3', 'C2', 'R')
TABLE_ORDER = ('C2', 'C3', 'C4', 'C5', 'C6', 'R')


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load_pinned(path, sha, name):
    if sha256_file(path) != sha:
        raise SystemExit('REFUSED: pin mismatch %s' % path)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def v009_admissibility(pre):
    """binding_inputs.v009_admissibility, executed from bytes at comparison time (unchanged from e6475f38)."""
    adm = pre['binding_inputs']['v009_admissibility']
    out = {'admissible': False, 'checks': {}}
    rv = adm['review']
    p = Path(rv['path'])
    if not p.is_file():
        out['reason'] = 'review record absent (%s)' % p
        return out
    try:
        r = json.loads(p.read_text())
    except Exception as exc:
        out['reason'] = 'review record unreadable: %s' % exc
        return out
    out['review_sha256'] = sha256_file(p)
    ok_v = r.get('verdict') in rv['accepted_verdicts']
    ok_d = r.get('driver_sha256') == adm['driver_sha256']
    ok_p = r.get('prep_sha256') == adm['prep_sha256']
    out['checks']['review'] = {'verdict': r.get('verdict'), 'verdict_ok': ok_v, 'driver_pin_ok': ok_d, 'prep_pin_ok': ok_p}
    for e in adm['evidence']:
        q = Path(e['path'])
        good = q.is_file() and sha256_file(q) == e['sha256']
        if good:
            v = json.loads(q.read_text()).get('verdict')
            good = v == e['required_verdict']
        out['checks'][e['name']] = good
    bad = [k for k, v in out['checks'].items() if (v is False) or (isinstance(v, dict) and not all(x for kk, x in v.items() if kk.endswith('_ok')))]
    if bad:
        out['reason'] = 'V009 admissibility failed: %s' % bad
    else:
        out['admissible'] = True
        out['reason'] = 'review %s with pinned driver and prep; prep reproduction evidence verified' % r.get('verdict')
    return out


def route_a_inputs_gate(pre, cid, result_path):
    """V7 (C5/C6): the case's route-A checkpoint IDENTITY.inputs_sha256 and iteration_0000/START digests equal the
    registered expectation (prep v009 operator evaluation of the registered per-call seed).  Unchanged from e6475f38."""
    exp_reg = pre['route_a_expected_inputs'].get(cid)
    if exp_reg is None:
        return {'V7': None, 'reason': 'no expectation registered for %s' % cid}
    q = Path(exp_reg['path'])
    if not q.is_file() or sha256_file(q) != exp_reg['sha256']:
        return {'V7': False, 'reason': 'registered expectation file missing or sha mismatch'}
    exp = json.loads(q.read_text())
    r = json.loads(Path(result_path).read_text())
    cp = Path((((r.get('identity') or {}).get('route_a') or {}).get('checkpoint')) or '')
    if not (cp / 'IDENTITY.json').is_file():
        return {'V7': False, 'reason': 'route-A checkpoint IDENTITY.json not found from result identity.route_a.checkpoint'}
    ident = json.loads((cp / 'IDENTITY.json').read_text())['identity']['inputs_sha256']
    e = exp['expected_identity_inputs_sha256']
    diff = [k for k in e if k != 'fourier_arguments' and ident.get(k) != e[k]]
    diff += ['fourier_arguments.' + k for k in set(e['fourier_arguments']) | set(ident.get('fourier_arguments', {}))
             if ident.get('fourier_arguments', {}).get(k) != e['fourier_arguments'].get(k)]
    st = json.loads((cp / 'iteration_0000/START.json').read_text())
    es = exp['expected_start_iteration_0000']
    sd = [k for k in es if (st.get(k) if k == 'prepared_metric_response_sha256' else (st.get(k) or {}).get('array_sha256')) != es[k]]
    return {'V7': not diff and not sd, 'identity_inputs_differing': sorted(diff), 'start_differing': sorted(sd), 'checkpoint': str(cp)}


def registered_outdir(case, result_path):
    """L4 (reported only): which registered outdir of C5/C6 holds this result (None if neither)."""
    rp = str(Path(result_path).parent)
    for k, v in (case.get('outdirs') or {}).items():
        if isinstance(v, dict) and rp == v.get('outdir'):   # outdirs also carries a 'note' string
            return k
    return None


def evaluate_ext(pre, pre5, C5M, adapted, packets, bracket_block, v9adm, v7, v5adm, bracket_is_r3):
    crit = pre5['criterion']
    tau_p = crit['tau_picard_km_s']
    ids = pre5['row_ids']
    sig = dict(zip(ids, pre5['quoted_sigma_km_s']))
    tau = dict(zip(ids, pre5['tau_km_s']))
    anc = pre5['anchor']
    cases = {c['id']: c for c in pre['cases']}
    drivers = {k: v['sha256'] for k, v in pre['binding_inputs']['drivers'].items()}
    sha2drv = {v: k for k, v in drivers.items()}
    reg = {'galaxy': 'DDO154', 'physical': anc['physical'], 'coefficients': anc['coefficients'], 'brackets': bracket_block,
           'picard_bound': anc['picard']['speed_change_bound_km_s'], 'picard_observe_every_pass': anc['picard']['observe_every_pass']}
    canon = C5M.canon
    gates = {}
    for cid in EXT_IDS + DIAG_IDS:
        c = cases[cid]
        if cid not in adapted:
            gates[cid] = {'present': False, 'valid_all': False, 'failed': ['missing'], 'role': c['role']}
            continue
        a = adapted[cid]
        ns = a['normalized_spec']
        g = {'notes': [], 'role': c['role']}
        g['V1'] = bool(a['schema'] == C5M.RESULT_SCHEMA and a['status'] == 'COMPLETED' and a['valid'] is True
                       and sorted(a['rows']) == sorted(ids) and all(isinstance(a['rows'][i], (int, float)) and math.isfinite(a['rows'][i]) for i in ids))
        g['V2'] = bool(a['last_change_km_s'] is not None and a['last_change_km_s'] <= tau_p)
        cb = C5M.common_block(ns)
        mism = [k for k in reg if canon(cb.get(k)) != canon(reg[k])]
        passes = cb['picard_passes']
        if not (passes == anc['picard']['passes'] or (cid == 'C2' and passes == 4 and a['last_change_km_s'] is not None
                                                       and a['last_change_km_s'] <= anc['picard']['speed_change_bound_km_s'])):
            mism.append('picard_passes')
        drv = sha2drv.get(a['driver_sha256'])
        if drv not in c['drivers_allowed']:
            mism.append('driver %s not in %s' % (drv or a['driver_sha256'], c['drivers_allowed']))
        elif drv == 'v009' and not v9adm.get('admissible'):
            mism.append('V009_INADMISSIBLE: %s' % v9adm.get('reason'))
        elif drv == 'v005' and not (v5adm or {}).get('admissible'):          # L2: V005 amendment_v005.driver.admissibility_condition
            mism.append('V005_INADMISSIBLE: %s' % (v5adm or {}).get('reason', 'admissibility not evaluated'))
        reg_grid = pre['grids'][c['grid']]['composite_grid_spec']
        if a['grid_spec'] != reg_grid:
            mism.append('grid')
        tr = a['truncation'] or {}
        if not (tr.get('shape') == SHAPE and tr.get('kmax_inverse_kpc') is None):
            mism.append('truncation')
        if 'route_a_numerics' in c:
            ra = (ns.get('numerics') or {}).get('route_a') or {}
            rr = c['route_a_numerics']
            if ra.get('max_iterations') != rr['max_iterations'] or ra.get('column_workers', 1) not in rr['column_workers_allowed']:
                mism.append('route_a numerics %s not %s' % (ra, rr))
        if c['prefix'] == 'bound':                                           # L1
            bsha = c['bound']['result']['sha256']
            g['bound_result_sha256'] = {'registered': bsha, 'actual': a['result_sha256'], 'equal': a['result_sha256'] == bsha,
                                        'enforced': bool(bracket_is_r3)}
            if bracket_is_r3 and a['result_sha256'] != bsha:
                mism.append('bound_result_sha256 %s != registered %s' % (a['result_sha256'], bsha))
        g['V3'] = not mism
        g['V3_mismatch'] = mism
        g['driver'] = drv
        pk = packets.get(cid) or {}
        g['V4'] = bool(pk.get('V4'))
        g['V5'] = bool(pk.get('V5'))
        if cid in ('C5', 'C6'):
            g['V7'] = bool((v7.get(cid) or {}).get('V7'))
            g['V7_detail'] = v7.get(cid)
            g['registered_outdir'] = registered_outdir(c, a['result_path'])  # L4, reported only
        g['present'] = True
        g['failed'] = [k for k in ('V1', 'V2', 'V3', 'V4', 'V5', 'V7') if k in g and not g[k]]
        g['valid_all'] = not g['failed']
        gates[cid] = g
    ok = {cid for cid, g in gates.items() if g['valid_all']}
    v = {cid: adapted[cid]['rows'] for cid in ok}

    def pair(c1, c2):
        if c1 in ok and c2 in ok:
            D, Dh, d = C5M.diffs(v[c1], v[c2], ids, tau)
            return {'cases': [c1, c2], 'D_km_s': D, 'Dhat': Dh, 'delta': dict(zip(ids, d)),
                    'delta_over_tau': {i: d[j] / tau[i] for j, i in enumerate(ids)}, 'delta_over_sigma': {i: d[j] / sig[i] for j, i in enumerate(ids)},
                    'rel': {i: d[j] / v[c2][i] for j, i in enumerate(ids)}}
        return None
    seq = {'4_5': pair('C4', 'C5'), '5_6': pair('C5', 'C6'), '3_4_diagnostic': pair('C3', 'C4'), '2_3_diagnostic': pair('C2', 'C3')}
    reg34 = pre['carried_from_r3']['cube_Dhat_3_4']
    if seq['3_4_diagnostic'] is not None:
        seq['3_4_diagnostic']['equals_registered_R3_value'] = abs(seq['3_4_diagnostic']['Dhat'] - reg34) <= 1e-9 * reg34
    tail = None
    if seq['4_5'] and seq['5_6']:
        d45, d56 = seq['4_5']['delta'], seq['5_6']['delta']
        per = {}
        for i in ids:
            q = abs(d56[i]) / abs(d45[i]) if d45[i] != 0 else float('inf')
            per[i] = {'q': q if math.isfinite(q) else None, 'tail_km_s': abs(d56[i]) * q / (1 - q) if q < 1 else None,
                      'tail_over_tau': abs(d56[i]) * q / (1 - q) / tau[i] if q < 1 else None, 'non_contracting': not q < 1}
        qs = seq['5_6']['Dhat'] / seq['4_5']['Dhat'] if seq['4_5']['Dhat'] > 0 else float('inf')
        tail = {'per_row': per, 'q_sequence': qs if math.isfinite(qs) else None,
                'tail_sequence_Dhat': seq['5_6']['Dhat'] * qs / (1 - qs) if qs < 1 else None, 'scope': 'diagnostic only; never adopted'}
    ksequence = {cid: v[cid] for cid in ('C2', 'C3', 'C4', 'C5', 'C6') if cid in v}
    inner = pre['carried_from_r3']['inner_control']
    # ---------------- decision (V006 decision_rule, in order; unchanged)
    rules = pre['criterion']['decision_rule']
    steps = pre['criterion']['gate_next_steps']
    dec = {'outcome': None, 'reasons': [], 'next_step': None}
    bad = [cid for cid in EXT_IDS if not gates[cid]['valid_all']]
    if bad:                                                     # X1
        nxt = {}
        for cid in bad:
            g = gates[cid]
            dec['reasons'].append('%s failed %s%s' % (cid, g['failed'], (' V3:%s' % g.get('V3_mismatch')) if 'V3' in g['failed'] else ''))
            nxt[cid] = {gt: steps.get(gt, 'Run the registered case (spec in extension_c5c6/v006_r1/specs).') for gt in g['failed']}
            if 'V3' in g['failed'] and any(str(m).startswith('V009_INADMISSIBLE') for m in g.get('V3_mismatch', [])):
                nxt[cid]['V3'] = pre['binding_inputs']['v009_admissibility']['inadmissible_next_step']
            if 'V3' in g['failed'] and any(str(m).startswith('V005_INADMISSIBLE') for m in g.get('V3_mismatch', [])):   # L2
                nxt[cid]['V3'] = pre5['amendment_v005']['driver']['inadmissible_next_step']
        dec.update(outcome='INCOMPLETE', next_step=nxt, rule=rules[0])
    elif inner.get('pass') is not True:                         # X2 (carried; registered PASS)
        dec.update(outcome='INNER_UNRESOLVED', next_step=pre5['criterion']['decision_rule'][1], rule=rules[1])
    else:
        d45, d56 = seq['4_5']['Dhat'], seq['5_6']['Dhat']
        contracting = d56 <= 0.5 * d45
        why = 'cube: Dhat_5_6=%.4g (<=1: %s), Dhat_4_5=%.4g, q=%.4g (<=0.5: %s)' % (d56, d56 <= 1.0, d45, d56 / d45 if d45 > 0 else float('inf'), contracting)
        dec['reasons'].append(why)
        if d56 <= 1.0 and contracting:                          # X3
            u = {i: abs(seq['5_6']['delta'][i]) + abs(inner['delta'][i]) for i in ids}
            dec.update(outcome='ADOPT', adopted_shape=SHAPE, adopted_kmax_inverse_kpc=6.0, adopted_grid='G6', rule=rules[2],
                       carried_numerical_uncertainty_km_s=u,
                       carried_terms={'K56': {i: abs(seq['5_6']['delta'][i]) for i in ids}, 'inner': {i: abs(inner['delta'][i]) for i in ids},
                                      'shape_spread': None},
                       shape_spread_status=pre['criterion']['shape_spread_untested'],
                       u_over_tau={i: u[i] / tau[i] for i in ids}, u_over_sigma={i: u[i] / sig[i] for i in ids},
                       m4_row_window_at_K6=adapted['C6']['m4_row_window'],
                       next_step=pre['criterion']['adopt_next_step'])
        elif contracting:                                       # X4 (a)
            dec.update(outcome='NOT_CONVERGED_EXT', subtype='CONTRACTING_ABOVE_TAU', rule=rules[3], next_step=pre['criterion']['next_step_contracting'])
        elif d45 <= 1.0 and d56 <= 1.0:                         # X4 (c)
            dec.update(outcome='NOT_CONVERGED_EXT', subtype='FLOOR_LIKE', rule=rules[3], next_step=pre['criterion']['next_step_floor_like'])
        else:                                                   # X4 (b)
            dec.update(outcome='NOT_CONVERGED_EXT', subtype='NOT_CONTRACTING', rule=rules[3], next_step=pre['criterion']['next_step_not_contracting'])
    return {'gates': gates, 'sequences': seq, 'tail_diagnostic': tail, 'k_sequence_rows_km_s': ksequence,
            'inner_control_carried': inner, 'decision': dec}


def k0_drift(adapted):
    """L3: V005's K0_max_rel_diff_vs_C2 (same expression as kmax_compare_c2v005.main); reported, not decided."""
    k0 = {}
    base = (adapted.get('C2') or {}).get('base_K_values_SI')
    for c in adapted:
        K = adapted[c]['base_K_values_SI']
        if K and base:
            b = np.asarray(base, float)
            k0[c] = float(np.max(np.abs(np.asarray(K, float) / b - 1)))
    return k0


def table_text(pre5, adapted, field):
    ids = pre5['row_ids']
    lines = ['row      tau_i  ' + ''.join('%10s' % c for c in TABLE_ORDER)]
    for i, rid in enumerate(ids):
        lines.append('%s  %7.3f  ' % (rid[-2:], pre5['tau_km_s'][i]) + ''.join(
            '%10.4f' % adapted[c]['rows'][rid] if c in adapted and rid in adapted[c]['rows'] else '%10s' % '-' for c in TABLE_ORDER))
    if field:   # L3: V005's ring-indicator block (g0 relative to C2), diagnostic
        lines.append('')
        lines.append('gravity-only ring g0 relative to C2 (diagnostic):')
        if field.get('C2'):
            base = [r['g0_m_s2'] for r in field['C2']['rows']]
            for j, rid in enumerate(ids):
                lines.append('%s  %7s  ' % (rid[-2:], '') + ''.join(('%+10.4f' % (field[c]['rows'][j]['g0_m_s2'] / base[j] - 1)) if field.get(c) else '%10s' % '-'
                                                                   for c in TABLE_ORDER))
        else:
            lines.append('(C2 field diagnostic absent)')
    return '\n'.join(lines) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--prereg', required=True)
    ap.add_argument('--cases', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--bracket-recovery', required=True)
    ap.add_argument('--no-field-diagnostic', action='store_true')
    ap.add_argument('--test-allow-unpinned-prereg', action='store_true')
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
    bi = pre['binding_inputs']
    pre5_path, pre5_sha = bi['prereg_v005']['path'], bi['prereg_v005']['sha256']
    if sha256_file(pre5_path) != pre5_sha:
        print('REFUSED: V005 prereg pin', file=sys.stderr)
        return 2
    pre5 = json.loads(Path(pre5_path).read_text())
    C5M = load_pinned(bi['v005_compare']['path'], bi['v005_compare']['sha256'], 'kmax_compare_c2v005')
    rec = json.loads(Path(a.bracket_recovery).read_text())
    why = C5M.validate_recovery(pre5, rec.get('brackets'))
    r3 = json.loads(Path(bi['r3_recovery']['path']).read_text()) if sha256_file(bi['r3_recovery']['path']) == bi['r3_recovery']['sha256'] else None
    if r3 is None:
        why.append('R3 recovery pin mismatch')
    else:
        for key in ('fs_absolute_overrides', 'rfs_factor_overrides'):
            for idx, e in r3['brackets']['rule'][key].items():
                if not C5M._contains(rec['brackets']['rule'][key].get(idx), e):
                    why.append('R3 entry %s[%s] not contained' % (key, idx))
    if why:
        print('REFUSED: recovery block is not R3 or a cumulative D7 widening of it: %s' % why, file=sys.stderr)
        return 2
    bracket_block = rec['brackets']
    bracket_is_r3 = C5M.canon(bracket_block) == C5M.canon(r3['brackets'])
    v9adm = v009_admissibility(pre)
    v5adm = C5M.v005_admissibility(pre5)                                    # L2
    rb = pre5['binding_inputs']['row_binding']
    radii = None
    if Path(rb['path']).is_file() and sha256_file(rb['path']) == rb['sha256']:
        q = json.loads(Path(rb['path']).read_text())['query_rows']
        if [x['id'] for x in q] == pre5['row_ids']:
            radii = [x['radius_m'] for x in q]
    field_on = (not a.no_field_diagnostic) and radii is not None               # L3
    cases_map = json.loads(Path(a.cases).read_text())
    cases = {c['id']: c for c in pre['cases']}
    unknown = sorted(set(cases_map) - set(cases))
    if unknown:
        print('REFUSED: unregistered case ids %s' % unknown, file=sys.stderr)
        return 2
    adapted, packets, field, errors, v7 = {}, {}, {}, {}, {}
    for cid, path in cases_map.items():
        try:
            adapted[cid] = C5M.adapt_result(path)
        except Exception as exc:
            errors[cid] = '%s: %s' % (type(exc).__name__, exc)
            continue
        c = dict(cases[cid], shape=SHAPE, kmax_inverse_kpc=None)
        grid_spec = pre['grids'][cases[cid]['grid']]['composite_grid_spec']
        try:
            chk, diag = C5M.packet_checks(adapted[cid], c, grid_spec, radii, field_on)
        except Exception as exc:
            chk, diag = {'V4': False, 'V5': False, 'reason': '%s: %s' % (type(exc).__name__, exc)}, None
        packets[cid], field[cid] = chk, diag
        if cid in ('C5', 'C6'):
            try:
                v7[cid] = route_a_inputs_gate(pre, cid, path)
            except Exception as exc:
                v7[cid] = {'V7': False, 'reason': '%s: %s' % (type(exc).__name__, exc)}
    ev = evaluate_ext(pre, pre5, C5M, adapted, packets, bracket_block, v9adm, v7, v5adm, bracket_is_r3)
    report = {'schema': 'UNT_KMAX_EXT_COMPARISON_C2V006_R1', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'test_mode': bool(psha != PREREG_SHA256), 'prereg': {'path': str(Path(a.prereg).resolve()), 'sha256': psha},
              'script_sha256': sha256_file(__file__), 'cases_file': {'path': str(Path(a.cases).resolve()), 'sha256': sha256_file(a.cases)},
              'bracket_recovery': {'path': str(Path(a.bracket_recovery).resolve()), 'sha256': sha256_file(a.bracket_recovery),
                                   'equals_R3': bracket_is_r3},
              'v009_admissibility': v9adm, 'v005_admissibility': v5adm,
              'inputs': {c: {k: adapted[c][k] for k in ('result_path', 'result_sha256', 'driver_sha256', 'call_spec_sha256', 'final_pass',
                                                          'last_change_km_s', 'm4_row_window', 'harm_m4_global', 'harm_m8_global',
                                                          'elapsed_seconds')} for c in adapted},
              'read_errors': errors, 'packet_checks': packets, 'route_a_inputs_V7': v7,
              'rows_km_s': {c: adapted[c]['rows'] for c in adapted},
              'K0_max_rel_diff_vs_C2': k0_drift(adapted),
              'field_diagnostic_enabled': field_on,
              'field_diagnostic': field if field_on else None,
              'diagnostics_scope': 'K0_max_rel_diff_vs_C2 and field_diagnostic are V005 diagnostics carried by V006 R1 (CHECK_V001 L3): reported, not decided',
              **ev}
    out.mkdir(parents=True)
    with open(out / 'KMAX_EXT_COMPARISON.json', 'x') as f:
        json.dump(report, f, indent=1, allow_nan=False, default=float)
        f.write('\n')
    txt = table_text(pre5, adapted, field if field_on else None)
    txt += '\nDECISION: %s\n' % json.dumps(ev['decision'], indent=1, default=float)
    with open(out / 'KMAX_EXT_COMPARISON_TABLE.txt', 'x') as f:
        f.write(txt)
    print(txt)
    return 0


if __name__ == '__main__':
    sys.exit(main())
