"""Post-hoc resource estimates for C5 (G5, 108^3 nodes) and C6 (G6, 120^3) from SAVED run outputs (read-only).
Measured inputs (all from bytes): route-A timestamps (request.json, iteration START/COMPLETED, attempt finish.json mtimes)
and residual/bound per iteration of the computed prefixes C2 (A2_ANCHOR_F10), C3, C4, R (V005 prefix runs) and the N=8
parallel deciding (ii) run; stage elapsed_seconds of the R3 runs; monitor receipt peak RSS split into route-A window and
the rest (STAGE_RSS_V001.json, same lane); peak output bytes.  Models (stated in the output, never fitted to C5/C6):
  time and memory: proportional to wave count n^3 from the G4 measurement (upper-ish), and linear in n^3 through G3,G4
  (lower-ish); route-A iteration count: residual/bound projected with the measured G4 contraction ratios extended by
  the measured G3->G4 drift per K step.  Prints and writes analysis/ESTIMATES_V001.json (must not exist)."""
import glob
import json
import os
from pathlib import Path

R = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
HERE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2/extension_c5c6')
NODES = {'G2': 72, 'G3': 84, 'G4': 96, 'GR': 92, 'G5': 108, 'G6': 120}
PREFIX = {'G2': 'A2_ANCHOR_F10_RUN_V001', 'G3': 'KMAX_A2F10_C3_V005_RUN_V001', 'G4': 'KMAX_A2F10_C4_V005_RUN_V001',
          'GR': 'KMAX_A2F10_R_V005_RUN_V001', 'G2_N8': 'DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001'}
RB = {'G2': 'KMAX_A2F10_C2R3_D7R3_RUN_V001', 'G3': 'KMAX_A2F10_C3R3_D7R3_RUN_V001', 'G4': 'KMAX_A2F10_C4R3_D7R3_RUN_V001'}
GIB = 1024 ** 3


def mt(p):
    return os.stat(p).st_mtime


def route_a_timing(run):
    d = R / run / 'stages/01_route_a'
    req = mt(d / 'request.json')
    its = sorted(glob.glob(str(d / 'checkpoint/iteration_*')))
    st = [mt(Path(i) / 'START.json') for i in its]
    co = [mt(Path(i) / 'COMPLETED.json') for i in its]
    fin = mt(d / 'attempt_000/finish.json')
    rb = []
    for i in its:
        c = json.loads((Path(i) / 'COMPLETED.json').read_text())
        rb.append(float.fromhex(c['gas_fourier_residual_J'][1]) / float.fromhex(c['bound_J'][1]))
    per = [b - a for a, b in zip(st, co)]
    return {'prep_and_unit_solve_s': round(st[0] - req, 1), 'iterations': len(its), 'per_iteration_s': [round(x, 1) for x in per],
            'mean_iteration_s': round(sum(per) / len(per), 1), 'post_s': round(fin - co[-1], 1), 'total_s': round(fin - req, 1),
            'residual_over_bound': [round(x, 3) for x in rb], 'contraction': [round(b / a, 3) for a, b in zip(rb, rb[1:])]}


def project_iterations(r0, ratios, max_it):
    seq, r = [r0], r0
    for q in ratios:
        r *= q
        seq.append(r)
        if r <= 1:
            break
    conv = next((i for i, x in enumerate(seq) if x <= 1), None)
    return {'projected_residual_over_bound': [round(x, 3) for x in seq], 'converged_at_iteration': conv,
            'within_seed_budget_8': conv is not None and conv <= 7, 'within_budget_%d' % max_it: conv is not None and conv <= max_it - 1}


def main():
    ra = {g: route_a_timing(run) for g, run in PREFIX.items()}
    rss = json.loads((HERE / 'analysis/STAGE_RSS_V001.json').read_text())
    n3 = {g: NODES[g] ** 3 for g in NODES}
    est = {'schema': 'UNT_KMAX_EXT_ESTIMATES_C2EXT_V001', 'measured_route_a': ra, 'wave_count': n3}
    # route-A iteration count projection
    c3, c4 = ra['G3'], ra['G4']
    r0_step = c4['residual_over_bound'][0] - c3['residual_over_bound'][0]
    drift = [b - a for a, b in zip(c3['contraction'], c4['contraction'])]
    proj = {}
    for k, g in ((1, 'G5'), (2, 'G6')):
        r0 = c4['residual_over_bound'][0] + k * r0_step
        base = c4['contraction'] + [c4['contraction'][-1] + (c4['contraction'][-1] - c4['contraction'][-2]) * j for j in range(1, 8)]
        ratios = [min(0.95, q + k * (drift[i] if i < len(drift) else drift[-1])) for i, q in enumerate(base)]
        proj[g] = project_iterations(r0, ratios, 12)
        proj[g]['initial_residual_over_bound'] = round(r0, 3)
        proj[g]['model'] = ('r0 = r0(G4) + k*(r0(G4)-r0(G3)); contraction ratios = G4 ratios (continued linearly past the last '
                            'measured one) + k * (G4-G3) per-iteration drift, capped 0.95; k = 1 (G5), 2 (G6)')
    est['route_a_iteration_projection'] = proj
    # route A wall time, serial and N=8
    n8 = ra['G2_N8']
    s_iter = ra['G2']['mean_iteration_s'] / n8['mean_iteration_s']
    est['route_a_parallel_measured'] = {'G2_serial_mean_iteration_s': ra['G2']['mean_iteration_s'],
                                        'G2_N8_mean_iteration_s': n8['mean_iteration_s'], 'iteration_speedup_N8': round(s_iter, 2),
                                        'note': 'deciding (ii) ran under machine load; prep/unit solve and the post-iteration rows stay serial'}
    out = {}
    for g in ('G5', 'G6'):
        f = n3[g] / n3['G4']
        it = proj[g]['converged_at_iteration']
        nit = (it + 1) if it is not None else 12
        prep = c4['prep_and_unit_solve_s'] * f
        per = c4['mean_iteration_s'] * f
        post = c4['post_s'] * f
        ser = prep + nit * per + post
        par = prep + nit * per / s_iter + post
        # route B (everything after route A): C4 reference+body (V005 prefix run) + C4R3 offset..end, proportional to n^3
        c4full = json.loads((R / PREFIX['G4'] / 'result.json').read_text())
        refbody = sum(s['elapsed_seconds'] for s in c4full['stage_records'] if s['name'] in ('reference', 'body'))
        rb_g4 = refbody + json.loads((R / RB['G4'] / 'result.json').read_text())['elapsed_seconds']
        c3full = json.loads((R / PREFIX['G3'] / 'result.json').read_text())
        rb_g3 = sum(s['elapsed_seconds'] for s in c3full['stage_records'] if s['name'] in ('reference', 'body')) + \
            json.loads((R / RB['G3'] / 'result.json').read_text())['elapsed_seconds']
        b = (rb_g4 - rb_g3) / (n3['G4'] - n3['G3'])
        rb_lin = rb_g4 + b * (n3[g] - n3['G4'])
        rb_prop = rb_g4 * f
        # memory
        ra_peak_g4 = rss[PREFIX['G4']]['route_a_peak_rss_bytes']
        ra_peak_g3 = rss[PREFIX['G3']]['route_a_peak_rss_bytes']
        rb_peak = {k: rss[v]['route_b_peak_rss_bytes'] for k, v in RB.items()}
        ra_ser_prop = ra_peak_g4 * f
        ra_ser_lin = ra_peak_g4 + (ra_peak_g4 - ra_peak_g3) / (n3['G4'] - n3['G3']) * (n3[g] - n3['G4'])
        rb_mem_prop = rb_peak['G4'] * f
        rb_mem_lin = rb_peak['G4'] + (rb_peak['G4'] - rb_peak['G3']) / (n3['G4'] - n3['G3']) * (n3[g] - n3['G4'])
        n8_extra_g2 = rss[PREFIX['G2_N8']]['route_a_peak_rss_bytes'] - rss[PREFIX['G2']]['route_a_peak_rss_bytes']
        n8_extra = n8_extra_g2 * n3[g] / n3['G2']
        outb_g4 = rss[PREFIX['G4']]['peak_output_bytes']  # C4 V005 prefix run (route A + reference/body/offset/fs) ...
        outb_c4r3 = rss[RB['G4']]['peak_output_bytes']    # ... plus the rest of route B (C4R3: offset..le3)
        out[g] = {
            'nodes_per_axis': NODES[g], 'wave_count_ratio_to_G4': round(f, 4),
            'route_a_iterations_assumed': nit,
            'route_a_serial_s': round(ser), 'route_a_N8_s': round(par),
            'route_b_s_linear': round(rb_lin), 'route_b_s_proportional': round(rb_prop),
            'call_serial_route_a_h': [round((ser + rb_lin) / 3600, 1), round((ser + rb_prop) / 3600, 1)],
            'call_N8_route_a_h': [round((par + rb_lin) / 3600, 1), round((par + rb_prop) / 3600, 1)],
            'route_a_serial_peak_rss_GiB': [round(ra_ser_prop / GIB, 2), round(ra_ser_lin / GIB, 2)],
            'route_a_N8_peak_rss_GiB': [round((ra_ser_prop + n8_extra) / GIB, 2), round((max(ra_ser_prop, ra_ser_lin) + n8_extra) / GIB, 2)],
            'route_b_peak_rss_GiB': [round(rb_mem_prop / GIB, 2), round(rb_mem_lin / GIB, 2)],
            'output_bytes_GiB_estimate': round((outb_g4 + outb_c4r3) * f / GIB, 1),
            'inputs': {'route_b_s_G4': round(rb_g4), 'route_b_s_G3': round(rb_g3), 'route_a_peak_rss_G4_GiB': round(ra_peak_g4 / GIB, 2),
                       'route_b_peak_rss_G4_GiB': round(rb_peak['G4'] / GIB, 2), 'N8_extra_rss_G2_GiB': round(n8_extra_g2 / GIB, 2),
                       'output_G4_prefix_plus_C4R3_GiB': round((outb_g4 + outb_c4r3) / GIB, 1)}}
    est['estimates'] = out
    est['models'] = {
        'time': 'route A = prep+unit solve + iterations x mean iteration + post, each x n^3 ratio to the G4 prefix run; N=8 divides the iteration phase by the measured G2 speedup only; route B = (G4 reference+body+C4R3) x n^3 ratio (proportional) or linear in n^3 through G3,G4',
        'memory': 'route A serial peak x n^3 ratio (proportional) or linear through G3,G4; N=8 adds the measured G2 N=8 excess scaled by n^3 (workers hold prepared response and waves, both ~n^3); route B peak proportional or linear through G3,G4',
        'load': 'all inputs were measured under machine load 10-14 with concurrent runs; wall times scale with load'}
    p = HERE / 'analysis/ESTIMATES_V001.json'
    with open(p, 'x') as fh:
        json.dump(est, fh, indent=1)
    print(json.dumps({'projection': proj, 'estimates': out, 'parallel': est['route_a_parallel_measured']}, indent=1))


if __name__ == '__main__':
    main()
