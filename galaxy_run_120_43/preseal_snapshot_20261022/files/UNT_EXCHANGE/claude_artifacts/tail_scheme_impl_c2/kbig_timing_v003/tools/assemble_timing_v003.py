"""Assemble TIMING_V003.json from the measured out/*.json rows (kbig_build_timing_c2v003 + load calibrations), the cited
plan/driver build counts, and the tail-OFF receipts.  Arithmetic only (no tail arithmetic).  Writes TIMING_V003.json
(exclusive create) next to out/.

Normalization: every V003 row ran under heavy, varying machine load.  Two digest-equal re-runs of the V002 reference row
(route_b le_rotation K128 M_s64; 232.75 s wall = CPU in 0d1365b9) give the session's inflation factors.  SOLO estimate of a
build = measured CPU / mean CPU ratio (ASSUMED stationary over the session; the two CPU ratios agree to ~1%); cross-check =
measured wall / mean wall ratio.  Measured walls are kept as 'under_load' (what the builds actually took today)."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
OUT = D / 'out'
X = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cite(p):
    return dict(path=str(p), sha256=sha(p))


def calib():
    rows = [json.loads(p.read_text()) | {'file': cite(p)} for p in sorted(OUT.glob('LOAD_CALIB_*_V003.json'))]
    if not rows or not all(r['state_digest_equal_reference'] for r in rows):
        raise SystemExit('calibration rows missing or not digest-equal')
    cr = sum(r['cpu_ratio'] for r in rows) / len(rows); wr = sum(r['wall_ratio'] for r in rows) / len(rows)
    return dict(rows=[dict(file=r['file'], wall_s=r['cold_build_wall_seconds'], cpu_s=r['cold_build_cpu_seconds'], wall_ratio=r['wall_ratio'],
                           cpu_ratio=r['cpu_ratio']) for r in rows], mean_cpu_ratio=round(cr, 4), mean_wall_ratio=round(wr, 4))


def row(kind, K, cal, mode='st'):
    p = OUT / ('TIMING_%s_KB%04d_MS128_%s_V003.json' % (kind, K, mode))
    if not p.is_file():
        return None
    d = json.loads(p.read_text())
    w = d['warm_build'] or {}
    cr, wr = cal['mean_cpu_ratio'], cal['mean_wall_ratio']
    r = dict(file=cite(p), status=d['status'], refusal=d['refusal'], mode=mode, n_eval_radii=d['n_eval_radii'], grid=d['grid'],
             rank=d['record'].get('rank'), memory_estimate_GiB=round(d['record'].get('memory_estimate_bytes', 0) / 2 ** 30, 3),
             peak_rss_GiB_after_cold=round(d['peak_rss_bytes_after_cold_build'] / 2 ** 30, 2), peak_rss_GiB_end=round(d['peak_rss_bytes_end'] / 2 ** 30, 2),
             i1t=d['i1t']['verdict'], warm_digest_equal_cold=w.get('state_digest_equal_cold'),
             under_load=dict(cold_wall_s=d['cold_build_wall_seconds'], cold_cpu_s=d['cold_build_cpu_seconds'],
                             warm_wall_s=w.get('build_wall_seconds'), warm_cpu_s=w.get('build_cpu_seconds')),
             lapse_pair_later_mean_s=d['evaluation']['lapse_pair_later_s']['mean'], jet_per_point_mean_s=d['evaluation']['jet_per_point_s']['mean'])
    r['solo_estimate'] = dict(cold_s=round(d['cold_build_cpu_seconds'] / cr, 1), warm_s=round(w['build_cpu_seconds'] / cr, 1),
                              cold_s_wall_crosscheck=round(d['cold_build_wall_seconds'] / wr, 1),
                              warm_s_wall_crosscheck=round(w['build_wall_seconds'] / wr, 1))
    return r


def progress(path):
    ev = [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    return {e['stage']: e['elapsed'] for e in ev if e.get('event') == 'finished'}


def main():
    cal = calib()
    meas = {K: dict(route_a=row('route_a', K, cal), route_b_rot=row('route_b_rot', K, cal), route_b_cols=row('route_b_cols', K, cal))
            for K in (128, 256)}
    mt = row('route_b_rot', 256, cal, 'mt')
    v002 = {}
    for name in ('TIMING_route_a_KB0128_n6_V002.json', 'TIMING_route_b_KB0128_V002.json'):
        p = X / 'tail_scheme_impl_c2/kbig_proxy_v002/out/timing' / name
        d = json.loads(p.read_text())
        v002[name] = dict(file=cite(p), cold_wall_s=d['cold_build_wall_seconds'], warm_wall_s=(d['warm_build'] or {}).get('build_wall_seconds'),
                          rank=d['record']['rank'], M_s=64)
    # ---------------- tail-OFF baseline (C4 lineage receipts, measured)
    c4r3 = RUNS / 'KMAX_A2F10_C4R3_D7R3_RUN_V001'; c4v5 = RUNS / 'KMAX_A2F10_C4_V005_RUN_V001'
    r3 = json.loads(Path(str(c4r3) + '.receipt.json').read_text())
    p3 = progress(c4r3 / 'progress.jsonl'); p5 = progress(c4v5 / 'progress.jsonl')
    per_pass = [round(sum(v for k, v in p3.items() if k.startswith('le%d_' % p)), 1) for p in (1, 2, 3)]
    proj = json.loads((X / 'parallel_route_a_c2/results/projection_c2v001.json').read_text())['DDO154_KMAX_A2F10_C4_measured']
    n8 = [r for r in proj['rows'] if r['N'] == 8][0]
    ra_prep = 375.09  # C4_V005 attempt_000 progress.jsonl: first column_completed at 375.09 s
    ra8 = [round(ra_prep + 7 * n8['seconds_low'], 1), round(ra_prep + 7 * n8['seconds_high'], 1)]
    base = dict(C4R3_receipt_offset_to_le3_s=r3['elapsed_seconds'], C4R3_le_pass_s=per_pass,
                C4_V005_route_a_serial_s=p5['route_a'], C4_V005_reference_s=p5['reference'], C4_V005_body_s=p5['body'],
                route_a_8_workers_s_PROJECTION_UNTESTED=ra8,
                sources=dict(C4R3_receipt=cite(Path(str(c4r3) + '.receipt.json')), C4R3_progress=cite(c4r3 / 'progress.jsonl'),
                             C4_V005_receipt=cite(Path(str(c4v5) + '.receipt.json')), C4_V005_progress=cite(c4v5 / 'progress.jsonl'),
                             parallel_route_a_projection=cite(X / 'parallel_route_a_c2/results/projection_c2v001.json')))
    extra_pass = sum(per_pass) / 3.0

    def tail(K, I, P, which, cache):
        a, b, c = meas[K]['route_a'], meas[K]['route_b_rot'], meas[K]['route_b_cols']
        if None in (a, b, c):
            return None
        g = (lambda r, k: r['solo_estimate'][k]) if which == 'solo' else (lambda r, k: r['under_load'][k.replace('_s', '_wall_s')])
        A_c, A_w = g(a, 'cold_s'), g(a, 'warm_s')
        B = g(b, 'warm_s' if cache else 'cold_s'); Cc = g(c, 'warm_s' if cache else 'cold_s')
        ra = A_c + I * A_w + (A_w if cache else A_c)          # begin(0) cold + I complete() warm + manifest-stage rebuild
        rb = B * (2 + 2 * P) + Cc * 2                          # offset + fs_rotation + P x (le_columns + le_rotation) | fs pair + rfs pair
        return dict(route_a_side_s=round(ra, 1), route_b_side_s=round(rb, 1), total_s=round(ra + rb, 1))

    scen = {}
    for K, case in ((256, 'C4T-KHI'), (128, 'C4T')):
        for name, I, P in (('expected_I7_P3', 7, 3), ('upper_I32_P6', 32, 6)):
            t_solo = tail(K, I, P, 'solo', False)
            if t_solo is None:
                continue
            t_load = tail(K, I, P, 'load', False); t_cache = tail(K, I, P, 'solo', True)
            b_rb = base['C4R3_receipt_offset_to_le3_s'] + (P - 3) * extra_pass
            b_full = [b_rb + base['C4_V005_reference_s'] + base['C4_V005_body_s'] + x for x in ra8]
            scen['%s_%s' % (case, name)] = dict(
                K_big=K, I_route_a_iterations=I, P_le_passes=P,
                builds=dict(route_a=dict(cold=2, warm=I), route_b_total=6 + 2 * P, route_b_critical_path=4 + 2 * P),
                tail_solo_estimate=t_solo, tail_under_today_load=t_load, tail_solo_if_cached_UNTESTED=t_cache,
                baseline_tail_off_route_b_s=round(b_rb, 1), baseline_tail_off_full_call_s=b_full,
                hours_solo_task_baseline=round((b_rb + t_solo['total_s']) / 3600, 2),
                hours_solo_full_baseline=[round((x + t_solo['total_s']) / 3600, 2) for x in b_full],
                hours_solo_full_baseline_if_cached_UNTESTED=[round((x + t_cache['total_s']) / 3600, 2) for x in b_full],
                tail_hours_solo=round(t_solo['total_s'] / 3600, 2), tail_hours_under_today_load=round(t_load['total_s'] / 3600, 2),
                saving_if_cached_hours_UNTESTED=round((t_solo['total_s'] - t_cache['total_s']) / 3600, 2))
    prev = json.loads((X / 'v007_launch_packet_cx1/P128/CONCURRENT_COST_PREVIEW_V003.json').read_text())
    prev_rows = {c['case']: dict(solo_h=c['solo_hours_UNTESTED'], all_concurrent_h=c['all_concurrent_hours_UNTESTED'])
                 for c in prev['calls'] if c['case'] in ('C4T', 'C4T-KHI')}
    out = dict(schema='UVT_KBIG_TIMING_V003_SUMMARY', label='measured single r5 tail builds + cited counts + projection arithmetic; not a T statistic',
               producer=cite(Path(__file__)), calibration=cal, measured=meas, measured_mt_variant_NON_PRODUCTION_ENV=mt,
               v002_reference_rows_M_s64=v002, baseline_tail_off=base, baseline_extra_pass_s=round(extra_pass, 1), scenarios=scen,
               previous_preview=dict(rows=prev_rows, source=cite(X / 'v007_launch_packet_cx1/P128/CONCURRENT_COST_PREVIEW_V003.json'),
                                     its_rule='M_s64 K128 V002 timings x2 (M_s128) x4 (K256); 32 warm A + 32 cold B + 1 cold A; baseline 11883 s'))
    p = D / 'TIMING_V003.json'
    raw = (json.dumps(out, indent=1, allow_nan=False) + '\n').encode()
    with open(p, 'xb') as f:
        f.write(raw)
    print(hashlib.sha256(raw).hexdigest())
    print(json.dumps(dict(cal=cal, scen=scen, extra_pass=extra_pass, base={k: v for k, v in base.items() if k != 'sources'},
                          solo={K: {k: (v or {}).get('solo_estimate') for k, v in m.items()} for K, m in meas.items()},
                          mt=mt and dict(under_load=mt['under_load'], solo=mt['solo_estimate'])), indent=1))


if __name__ == '__main__':
    main()
