"""Schedule simulation for steps 4 and 5 (Claude2 sched_s45_c2, c2v001).  Deterministic; launches nothing.

Model (processor-sharing fluid, as LAUNCH_ORDER_C4V002's schedule_sim_c4v003, so its 209.75 h is reproducible):
  * time steps of DT s; a running call advances its current segment by DT x rate, rate = min(1, 18 / sum of busy cores
    of the running segments).  Measured segment lengths are co-loaded walls, so this double-counts load (conservative);
  * a campaign wave starts when the previous one has ended (orchestrator barrier); admission is checked at POLL s;
  * the NEW rule calls machine_gate_s45_c2v001.evaluate() itself (pinned bytes), so the simulated rule is the code's;
  * memory: per-call footprint by phase plus per-iteration transfer spikes (DDO) or state-build transients (NGC).
Per-call costs come from the measured basis (SCHED_S45_MEASURED_BASIS JSON, pinned by sha256 on the command line):
  low / expected / high = min / median / max of the step-2 R2 K_big-128 runs where MEASURED; else DERIVED or ASSUMED,
  each labelled in the output.
Cross-check: LAUNCH_ORDER_C4V002's own per-call segments (TIMING_V003-based, 5.19 h E / 8.75 h U) under the c2v005
budget rule with max_concurrent 6 must reproduce its 209.75 h E and 356.49 h U.
usage: python3 -I -B sim_s45_c2v001.py MEASURED_BASIS.json BASIS_SHA256 OUT.json [EXTRA_LIVE_MEASURE.json ...]
       (extra live files contribute route-A footprint peaks only)
"""
import copy
import hashlib
import json
import math
import statistics
import sys
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE_PATH = HERE / 'machine_gate_s45_c2v001.py'
CORES = 18.0
DT = 30.0
POLL = 60.0
WAVE_CAP_S = 172800.0
GiB = 2.0 ** 30


def load_gate():
    raw = GATE_PATH.read_bytes()
    m = types.ModuleType('gate_sim')
    exec(compile(raw, str(GATE_PATH), 'exec'), m.__dict__)
    return m, hashlib.sha256(raw).hexdigest()


G, GATE_SHA = load_gate()


# ----------------------------------------------------------------------------------------------------- segments
# segment = [name, solo_seconds, busy_cores, phase('route_a'|'after'), mem_gb, spike(dict|None)]
def ddo_on_segments(c, label):
    segs = [['setup', c['setup_s'], 1.0, 'route_a', 3.0, None]]
    for n in range(c['iterations']):
        steady = c['ra_steady_gb'] + c['vf_gb_per_iter'] * max(0, n - 6)
        segs.append(['iter', c['cycle_s'], c['w_ra'], 'route_a', steady,
                     {'start': c['spike_start_s'], 'len': c['spike_len_s'], 'gb': c['spike_gb']}])
    segs.append(['post', c['post_s'], 1.0, 'route_a', 3.8, None])
    segs.append(['route_b', c['route_b_s'], c['w_rb'], 'after', c['rb_gb'], None])
    return segs


def ddo_off_segments(c):
    segs = [['setup', c['setup_s'], 1.0, 'route_a', 3.0, None]]
    for n in range(c['iterations']):
        segs.append(['iter', c['cycle_s'], c['w_ra'], 'route_a', 10.47, None])
    segs.append(['route_b', c['route_b_s'], c['w_rb'], 'after', 3.0, None])
    return segs


def ngc_segments(T_s, c):
    ra = c['route_a_fraction'] * T_s
    setup = c['setup_s']
    cyc = (ra - setup) / c['iterations']
    segs = [['setup', setup, 1.0, 'route_a', c['steady_gb'], None]]
    for n in range(c['iterations']):
        segs.append(['iter', cyc, 1.0, 'route_a', c['steady_gb'],
                     {'start': 0.0, 'len': c['vf_s_per_n'] * (n + 1), 'gb': c['vf_gb_per_n'] * (n + 1)}])
    segs.append(['route_b', T_s - ra, c['w_rb'], 'after', 4.4, None])
    return segs


def lo_segments(T, scen):
    """LAUNCH_ORDER_C4V002 / schedule_sim_c4v003 call_model, TAIL_ON, from TIMING_V003 (3e3fb600) numbers."""
    I = 7 if scen == 'E' else 32
    prep = 1014.9 - 7 * 91.4
    w = (91.4 + 95.1) / 2.0
    base_b = 10702.177100833971 + (0 if scen == 'E' else 3 * 2116.9) + 2786.0871093340684 + 600.1894180830568
    tail_b = 2234.0 if scen == 'E' else 3587.6
    segs = [['prep', prep, 1, 'route_a', 0, None], ['A_cold', 285.0, 1, 'route_a', 0, None]]
    for _ in range(I):
        segs.append(['A_wave', w, 8, 'route_a', 0, None])
        segs.append(['A_warm', 111.0, 1, 'route_a', 0, None])
    segs.append(['manifest', 285.0, 1, 'after', 0, None])
    segs.append(['route_b', base_b + tail_b, 1.5, 'after', 0, None])
    return segs


class Call:
    def __init__(self, name, segs, cls, kind, group=None, requires=()):
        self.name, self.segs, self.cls, self.kind = name, [list(s) for s in segs], cls, kind
        self.group, self.requires = group, tuple(requires)
        self.i = 0
        self.rem = self.segs[0][1]
        self.start = self.end = None
        self.ra_done_t = None
        self.iter_start_t = None
        self.iters_done = 0
        self.first_iter_t = None
        self.killed = None
        self.peak_mem = 0.0

    def running(self):
        return self.start is not None and self.end is None

    def seg(self):
        return self.segs[self.i]

    def phase(self):
        return self.seg()[3]

    def busy(self):
        return self.seg()[2] if self.running() else 0.0

    def old_weight(self):                                       # campaign_c2v005: 8 until route A finished, then 2
        return 8 if self.ra_done_t is None else 2

    def mem(self, t):
        if not self.running():
            return 0.0, False
        s = self.seg()
        m = s[4]
        sp = s[5]
        hit = False
        if sp and self.iter_start_t is not None and sp['start'] <= t - self.iter_start_t < sp['start'] + sp['len']:
            m += sp['gb']
            hit = True
        return m, hit

    def advance(self, dts, t):
        while dts > 1e-12 and self.end is None:
            take = min(dts, self.rem)
            self.rem -= take
            dts -= take
            if self.rem <= 1e-9:
                nm = self.segs[self.i][0]
                if nm in ('iter', 'A_wave'):
                    self.iters_done += 1
                    if self.first_iter_t is None:
                        self.first_iter_t = t
                self.i += 1
                if self.i >= len(self.segs):
                    self.end = t
                    break
                if self.ra_done_t is None and self.segs[self.i][3] == 'after':
                    self.ra_done_t = t
                if self.segs[self.i][0] == 'iter':
                    self.iter_start_t = t
                self.rem = self.segs[self.i][1]


# ----------------------------------------------------------------------------------------------------- engine
def simulate(waves, policy, background=(), dt=DT, poll=POLL, max_t=2.0e7, kill=None):
    """waves: list of lists of Call (barrier between waves).  background: Calls started at t=0 outside the waves
    (foreign to the admission rule's owned set, but counted by the gate).  policy: dict(kind=...)."""
    t = 0.0
    stats = {'max_total_mem_gb': 0.0, 'max_busy_demand': 0.0, 'max_route_a_pooled': 0, 'max_running': 0,
             'time_ge2_spikes_h': 0.0, 'time_ge3_spikes_h': 0.0, 'time_mem_over_100_h': 0.0, 'gate_wait_reasons': {}}
    spans, last_off, late = [], [], []
    for c in background:
        c.start = 0.0
        if c.segs[0][0] == 'iter':
            c.iter_start_t = 0.0
    bg = list(background)
    for wcalls in waves:
        pending = list(wcalls)
        active = []
        w0 = t
        next_poll = t
        last_start = None
        prev = None
        while pending or active:
            if t >= next_poll and pending:
                while pending:
                    head = pending[0]
                    if head.requires and not all(c.end is not None and not c.killed for c in wcalls if c.group in head.requires):
                        if any(c.killed for c in wcalls if c.group in head.requires):
                            pending.pop(0)
                            head.killed = 'REQUIRED_GROUP_FAILED'
                            continue
                        break
                    ok, why = admit(policy, head, active, bg, t, last_start, prev, wcalls)
                    for r in why:
                        stats['gate_wait_reasons'][r] = stats['gate_wait_reasons'].get(r, 0) + 1
                    if not ok:
                        break
                    pending.pop(0)
                    head.start = t
                    if head.segs[0][0] == 'iter':
                        head.iter_start_t = t
                    active.append(head)
                    last_start, prev = t, head
                    if policy['kind'] != 'old_budget':
                        break
                next_poll = t + poll
            run = active + [c for c in bg if c.running()]
            demand = sum(c.busy() for c in run)
            rate = 1.0 if demand <= CORES else CORES / demand
            mems = [c.mem(t) for c in run]
            tot = sum(m for m, _ in mems)
            nsp = sum(1 for _, h in mems if h)
            for c, (m, _) in zip(run, mems):
                c.peak_mem = max(c.peak_mem, m)
            stats['max_total_mem_gb'] = max(stats['max_total_mem_gb'], tot)
            stats['max_busy_demand'] = max(stats['max_busy_demand'], demand)
            stats['max_running'] = max(stats['max_running'], len(active))
            stats['max_route_a_pooled'] = max(stats['max_route_a_pooled'],
                                              sum(1 for c in run if c.phase() == 'route_a' and c.seg()[0] != 'post'
                                                  and c.cls and c.cls['pooled']))
            if nsp >= 2:
                stats['time_ge2_spikes_h'] += dt / 3600.0
            if nsp >= 3:
                stats['time_ge3_spikes_h'] += dt / 3600.0
            if tot > 100.0:
                stats['time_mem_over_100_h'] += dt / 3600.0
            t += dt
            for c in run:
                c.advance(dt * rate, t)
                if kill and c.end is None and c.killed is None:
                    k = kill(c, t)
                    if k:
                        c.killed, c.end = k, t
            active = [c for c in active if c.end is None]
            if t > max_t:
                raise SystemExit('SIM_TIMEOUT %s' % policy)
        spans.append(t - w0)
        offs = [c.start - w0 for c in wcalls if c.start is not None]
        last_off.append(max(offs) if offs else 0.0)
        late.append(sum(1 for o in offs if o >= WAVE_CAP_S))
    for k in ('time_ge2_spikes_h', 'time_ge3_spikes_h', 'time_mem_over_100_h', 'max_total_mem_gb', 'max_busy_demand'):
        stats[k] = round(stats[k], 2)
    allc = [c for w in waves for c in w]
    return {'makespan_h': round(t / 3600.0, 2), 'wave_spans_h': [round(x / 3600.0, 2) for x in spans],
            'max_start_offset_in_wave_h': round(max(last_off) / 3600.0, 2) if last_off else None,
            'last_start_offset_per_wave_h': [round(x / 3600.0, 2) for x in last_off],
            'late_starts_ge_48h_NOT_STARTED_in_campaign': sum(late),
            'killed': sum(1 for c in allc if c.killed), 'n_calls': len(allc),
            'call_wall_h_min_max': [round(min((c.end - c.start) for c in allc if c.end is not None) / 3600.0, 2),
                                    round(max((c.end - c.start) for c in allc if c.end is not None) / 3600.0, 2)],
            **stats}


def admit(policy, head, active, bg, t, last_start, prev, wcalls):
    k = policy['kind']
    if k == 'old_budget':
        acc = sum(c.old_weight() for c in active)
        ok = acc + 8 <= policy['budget'] and len(active) < policy['m']
        return ok, ([] if ok else ['OLD_BUDGET'])
    if k == 'ramp':                                             # direct-batch launcher (guard/launcher v010/v011)
        ra = sum(1 for c in active if c.ra_done_t is None)
        ok = (prev is None or prev.first_iter_t is not None) and ra < policy['max_active']
        return ok, ([] if ok else ['RAMP'])
    if k == 'serial_k':                                         # RI45-12 as proposed: first to completion, then k
        first = [c for c in wcalls if c.kind == 'NGC' and c.start is not None]
        if head.kind == 'NGC' and first and first[0].end is None:
            return False, ['SOLO_FIRST_TO_COMPLETION']
        ok = sum(1 for c in active if c.kind == 'NGC') < policy['k'] or head.kind != 'NGC'
        return ok, ([] if ok else ['K_AT_A_TIME'])
    if k == 'gate':
        if policy.get('solo_iterations') and head.kind == 'NGC':
            firsts = [c for c in wcalls if c.kind == 'NGC' and c.start is not None]
            if firsts and firsts[0].end is None and firsts[0].iters_done < policy['solo_iterations']:
                return False, ['SOLO_FIRST']
        runs = []
        for c in active + [b for b in bg if b.running()]:
            m, _ = c.mem(t)
            owned = c in active
            r = {'key': c.name, 'owned': owned, 'phase': c.phase(), 'footprint_gb': m,
                 'pool_closed': c.seg()[0] == 'post'}               # route-A post-loop: the worker pool has exited
            if owned:
                r['class'] = c.cls
            else:
                r['cores_measured'] = c.busy()
                r['nproc'] = 11 if (c.cls and c.cls['pooled']) else 2
            runs.append(r)
        n_owned_kind = sum(1 for c in active if c.kind == head.kind) if policy.get('per_kind_count') else len(active)
        since = None if last_start is None else t - last_start
        P = dict(G.PARAMS)
        P.update(policy.get('params') or {})
        if head.kind == 'NGC':
            P['spacing_s'] = policy.get('ngc_spacing_s', 600.0)
        d = G.evaluate(runs=runs, head=head.cls, n_running=n_owned_kind, max_concurrent=policy['m'], swap_gb=1.8,
                       since_last_start_s=since, history_s=1e9, params=P)
        return d['admit'], d['reasons']
    raise ValueError(k)


# ----------------------------------------------------------------------------------------------------- inputs
K128_MEM_RUNS = ('C2T', 'C3T', 'C4T', 'C4T_A', 'C4T_D5', 'S4T')     # K_big 128 runs (C6T: larger grid; KHI: K_big 256)


def basis_params(B, extra_live=None):
    """Per-call cost tables from the measured basis.  Returns (tables, provenance, labels)."""
    tm = B['timing']
    k128 = [n for n in ('C4T', 'S4T', 'C4T_A', 'C4T_D5') if n in tm]
    k128c6 = k128 + [n for n in ('C6T',) if n in tm]
    setups = [tm[n]['setup_to_first_prepared_s'] for n in k128 if tm[n]['setup_to_first_prepared_s']]
    setups_all = [r['setup_to_first_prepared_s'] for r in tm.values() if r['setup_to_first_prepared_s']]
    cyc = [x for n in k128 for x in tm[n]['cycle_prepared_to_prepared_s']]
    cyc6 = [x for n in k128c6 for x in tm[n]['cycle_prepared_to_prepared_s']]
    its = [tm[n]['iterations_completed'] for n in k128c6 if tm[n].get('route_a_finished_s') or tm[n].get('post_loop_running_at_least_s')]
    post = []
    for n in k128c6:
        r = tm[n]
        pl = r['post_loop_s'] if r['post_loop_s'] is not None else r.get('post_loop_running_at_least_s')
        mf = r['manifest_s'] if r['manifest_s'] is not None else (r.get('manifest_running_at_least_s') or 0.0)
        if pl is not None:
            post.append(pl + mf)
    fb = B['footprint_by_phase_gb']
    steady = [fb[n]['iterating']['median_gb'] for n in k128 if 'iterating' in fb.get(n, {})]
    steady_max = max(fb[n]['iterating_outside_spike_windows']['max_gb'] for n in K128_MEM_RUNS
                     if 'iterating_outside_spike_windows' in fb.get(n, {}))
    incs = [s['increment_gb'] for n in k128c6 for s in fb.get(n, {}).get('transfer_spikes', [])]
    fast = B.get('fast_spikes') or {}
    peaks = {'watch_iterating_max': max(fb[n]['iterating']['max_gb'] for n in K128_MEM_RUNS if 'iterating' in fb.get(n, {})),
             'fast_sampler_peak': max([e['peak_gb'] for e in fast.get('events') or []] or [0.0])}
    for i, L in enumerate(extra_live or []):
        peaks['live_%d_route_a_footprint_max' % i] = max([v['footprint_gb_max'] for k, v in (L.get('summary') or {}).items()
                                                          if any(('_%s_MS128' % n) in k for n in K128_MEM_RUNS)
                                                          and v['phases'] == ['route_a']] or [0.0])
    peak = max(peaks.values())
    spike = round(peak - steady_max, 2)                          # MEASURED peak above the MEASURED steady maximum
    w_ra = G.PARAMS['w_route_a_8']                              # the gate constant (MEASURED 3.25 while iterating)
    live = B.get('live_cores') or {}
    pooled_means = [v['cores_mean'] for k, v in live.items() if v['nproc_max'] >= 4 and v['phases'] == ['route_a']]
    prov = {'k128_runs': k128, 'k128_plus_c6t': k128c6, 'setup_s': setups, 'setup_s_all_runs': setups_all,
            'cycle_s_k128': cyc, 'cycle_s_k128_c6t': cyc6, 'iterations_seen': its, 'post_plus_manifest_s': post,
            'iterating_median_gb': steady, 'steady_max_gb_outside_spike_windows': steady_max,
            'spike_increments_gb_watch_30_40s': incs, 'k128_peak_footprint_gb_by_source': peaks, 'spike_gb_used': spike,
            'live_pooled_route_a_cores_means_10min_incl_setup_postloop': pooled_means, 'w_route_a_used': w_ra}
    common = {'w_ra': w_ra, 'w_rb': 1.5, 'ra_steady_gb': steady_max, 'spike_gb': spike,
              'spike_start_s': 30.0, 'spike_len_s': 60.0, 'vf_gb_per_iter': 0.2228, 'rb_gb': 4.4}
    tab = {
        'low': dict(common, setup_s=min(setups), iterations=min(its) if its else 6, cycle_s=min(cyc),
                    post_s=min(post), route_b_s=4.0 * 3600),
        'expected': dict(common, setup_s=statistics.median(setups), iterations=7, cycle_s=statistics.median(cyc),
                         post_s=statistics.median(post), route_b_s=16322.45),
        'high': dict(common, setup_s=max(setups_all), iterations=32, cycle_s=max(cyc6), post_s=max(post),
                     route_b_s=24026.76),
    }
    labels = {'setup_s': 'MEASURED: low/expected = min/median of the K128 runs; high = max over every R2 run (KHI included)',
              'iterations': 'MEASURED low = min seen (route A ended); expected 7 (median of 6-8 seen); high 32 = spec max (FORMAL)',
              'cycle_s': 'MEASURED iteration_prepared to iteration_prepared: min/median of K128 runs; high = max of K128 + C6T',
              'post_s': 'MEASURED post-loop + tail manifest (a running stage counts as a lower bound)',
              'route_b_s': 'DERIVED (no tail-ON route B has finished): TIMING_V003 E 16,322 s and U 24,027 s (the LAUNCH_ORDER '
                           'route-B segments); low 4.0 h ASSUMED',
              'w_ra': 'the gate constant 3.25 (MEASURED iterating mean, C4T/S4T; re-measured 2.77 on C3T, 10 min)', 'w_rb': 'DERIVED 1.5 '
              '(LAUNCH_ORDER fluid P; MEASURED reference stage 0.8-1.0 is lower)',
              'ra_steady_gb': 'MEASURED max iterating footprint outside transfer windows, K_big-128 runs',
              'spike_gb': 'MEASURED largest K_big-128 peak footprint (watch, fast sampler, live sampler) minus ra_steady_gb',
              'spike window': 'ASSUMED 30-90 s after '
              'iteration_prepared (MEASURED single 30-45 s samples)', 'vf_gb_per_iter': 'DERIVED u4 (32 x 51,200 x 136 B) beyond '
              'the 6 measured iterations', 'rb_gb': 'DERIVED model 4.095 GiB (route B not measured)'}
    return tab, prov, labels


DIII = {'low': {'setup_s': 300.0, 'iterations': 7, 'cycle_s': 105.0, 'route_b_s': 4.20 * 3600 - 300 - 7 * 105, 'w_ra': 3.25, 'w_rb': 1.5},
        'expected': {'setup_s': 300.0, 'iterations': 7, 'cycle_s': 150.0, 'route_b_s': 4.72 * 3600 - 300 - 7 * 150, 'w_ra': 3.25, 'w_rb': 1.5},
        'high': {'setup_s': 300.0, 'iterations': 32, 'cycle_s': 96.0, 'route_b_s': 6.61 * 3600 - 300 - 32 * 96, 'w_ra': 3.25, 'w_rb': 1.5}}
NGC_T_H = {'low': 11.7, 'expected': 17.6, 'high': 56.3}     # DERIVED (root's measured-basis estimate)
NGC_C = {'route_a_fraction': 0.7, 'iterations': 16, 'setup_s': 960.0, 'steady_gb': 5.0, 'vf_gb_per_n': 0.6367,
         'vf_s_per_n': 27.3, 'w_rb': 1.5}


def cls_ddo(G_):
    return G_.make_class('DDO_K128_TAIL_ON', pooled=True, w_route_a=G_.PARAMS['w_route_a_8'], w_after=2.0,
                         res_route_a_gb=G_.PARAMS['res_route_a_gb'], res_after_gb=G_.PARAMS['res_after_gb'])


def cls_ngc(res):
    return G.make_class('NGC_K32_SERIAL', pooled=False, w_route_a=1.0, w_after=2.0, res_route_a_gb=res, res_after_gb=6.0)


def ngc_res_measured():
    rss0 = NGC_C['steady_gb'] + NGC_C['vf_gb_per_n']
    slope = NGC_C['vf_gb_per_n']
    proj16 = NGC_C['steady_gb'] + 2 * slope + 14 * slope
    return round((rss0 + proj16) / 2.0, 2)


# ----------------------------------------------------------------------------------------------------- scenarios
ENGINE_WAVES = [1, 8, 2, 1, 1, 1, 10, 10, 24, 8, 2, 1, 10, 10, 24, 7]
LO_WAVES = [1] + [6] * 19 + [5]


def campaign(tab, scen, waves, policy, background=(), w_ra=None):
    c = tab[scen]
    cls = cls_ddo(G)
    ws = [[Call('w%02dc%02d' % (wi, j), ddo_on_segments(c, scen), cls, 'DDO') for j in range(n)] for wi, n in enumerate(waves)]
    return simulate(ws, policy, background=background)


def direct(tab, scen, n, policy, kind='DDO'):
    if kind == 'DDO':
        calls = [Call('d%02d' % j, ddo_on_segments(tab[scen], scen), cls_ddo(G), 'DDO') for j in range(n)]
    else:
        calls = [Call('x%02d' % j, ddo_off_segments(DIII[scen]), cls_ddo(G), 'DDO') for j in range(n)]
    return simulate([calls], policy)


def step5(tab, scen, M, S, rule, original_k=False, probe=False):
    """FINAL_SUMMARY -> last NGC call ends.  S4-POST-S1 (2 DDO tail-ON calls) first; NGC headline M, ORIGINAL_K M
    (optional), sensitivity S (after every headline member: D1)."""
    T = NGC_T_H[scen] * 3600.0
    res = ngc_res_measured() if (probe or rule == 'new') else 11.0
    calls = [Call('post_s1_%d' % j, ddo_on_segments(tab[scen], scen), cls_ddo(G), 'DDO_POST') for j in range(2)]
    ncls_first = cls_ngc(11.0 if not probe else res)
    ncls = cls_ngc(res)
    for j in range(M):
        calls.append(Call('h%02d' % j, ngc_segments(T, NGC_C), ncls_first if j == 0 else ncls, 'NGC', group='HEADLINE'))
    if original_k:
        for j in range(M):
            calls.append(Call('k%02d' % j, ngc_segments(T, NGC_C), ncls, 'NGC', group='ORIGINAL_K'))
    for j in range(S):
        calls.append(Call('s%02d' % j, ngc_segments(T, NGC_C), ncls, 'NGC', group='SENS', requires=('HEADLINE',)))
    kill = None
    if rule == 'proposed_caps':
        pol = {'kind': 'serial_k', 'k': 1}

        def kill(c, t):                                         # 12 h wall, 5 GiB RSS (ps ~ footprint x 1.0 here)
            if c.kind != 'NGC':
                return None
            m, _ = c.mem(t)
            if m * 1e9 > 5 * GiB:
                return 'RSS_CAP_5GiB'
            if t - c.start > 12 * 3600:
                return 'WALL_CAP_12h'
            return None
    elif rule in ('serial_1', 'serial_2'):
        pol = {'kind': 'serial_k', 'k': int(rule[-1])}
    elif rule == 'new':
        pol = {'kind': 'gate', 'm': 16, 'solo_iterations': 0 if probe else 2, 'ngc_spacing_s': 600.0}
    else:
        raise ValueError(rule)
    r = simulate([calls], pol, kill=kill)
    r['res_route_a_gb_ngc'] = res
    return r


def disk_check(waves, per_call_gb, guard_gib, free0_gib, reserve_gib=20.0, pre_calls=0):
    """Orchestrator disk guard before each wave: free >= n x per_call_bytes_guard + reserve; nothing is deleted."""
    used = pre_calls * per_call_gb * 1e9 / GiB
    out = []
    for wi, n in enumerate(waves):
        free = free0_gib - used
        need = n * guard_gib + reserve_gib
        out.append({'wave': wi + 1, 'n': n, 'free_GiB': round(free, 1), 'need_GiB': round(need, 1), 'fits': free >= need})
        used += n * per_call_gb * 1e9 / GiB
    first_halt = next((o for o in out if not o['fits']), None)
    return {'first_halt': first_halt, 'final_free_GiB': round(free0_gib - used, 1)}


def main(basis_path, basis_sha, out_path, *extra_live_paths):
    raw = Path(basis_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != basis_sha:
        raise SystemExit('BASIS_PIN_MISMATCH')
    B = json.loads(raw)
    extra = [json.loads(Path(p).read_text()) for p in extra_live_paths]
    tab, prov, labels = basis_params(B, extra)
    gate_spike_covers_measured = G.PARAMS['spike_headroom_gb'] >= prov['spike_gb_used']
    rec = {'schema': 'SCHED_S45_SIM_C2V001', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           'label': 'Projections (UNTESTED as forecasts); the arithmetic is TESTED (deterministic replay of stated inputs)',
           'inputs': {'measured_basis': {'path': str(basis_path), 'sha256': basis_sha}, 'gate': {'path': str(GATE_PATH), 'sha256': GATE_SHA},
                      'extra_live_footprint': [{'path': str(p), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}
                                               for p in extra_live_paths]},
           'model': {'cores': CORES, 'dt_s': DT, 'poll_s': POLL, 'wave_cap_s': WAVE_CAP_S,
                     'per_call_tables': tab, 'labels': labels, 'basis_provenance': prov,
                     'diii_table_DERIVED': DIII, 'ngc_T_h_DERIVED_root': NGC_T_H, 'ngc_model': NGC_C,
                     'ngc_res_route_a_gb_after_measurement': ngc_res_measured(),
                     'gate_params': dict(G.PARAMS), 'gate_spike_headroom_covers_measured_spike': gate_spike_covers_measured}}
    # 1. cross-check against LAUNCH_ORDER_C4V002 section 7.5
    xc = {}
    for scen, want in (('E', 209.75), ('U', 356.49)):
        ws = [[Call('w%02dc%d' % (wi, j), lo_segments(None, scen), None, 'DDO') for j in range(n)] for wi, n in enumerate(LO_WAVES)]
        r = simulate(ws, {'kind': 'old_budget', 'm': 6, 'budget': 17})
        xc[scen] = {'makespan_h': r['makespan_h'], 'launch_order_h': want, 'reproduced': abs(r['makespan_h'] - want) <= 0.05,
                    'first_wave_spans_h': r['wave_spans_h'][:3]}
    rec['cross_check_launch_order'] = xc
    # 2. campaign
    camp = {}
    for wname, waves in (('LAUNCH_ORDER_[1]+19x[6]+[5]', LO_WAVES), ('ENGINE_SHAPED_ASSUMED', ENGINE_WAVES)):
        for scen in ('low', 'expected', 'high'):
            for pname, pol in (('OLD_max_concurrent1_budget17', {'kind': 'old_budget', 'm': 1, 'budget': 17}),
                               ('OLD_max_concurrent6_budget17', {'kind': 'old_budget', 'm': 6, 'budget': 17}),
                               ('NEW_gate_max_concurrent12', {'kind': 'gate', 'm': 12}),
                               ('VARIANT_gate_two_spike_headroom', {'kind': 'gate', 'm': 12,
                                                                    'params': {'spike_headroom_gb': 2 * G.PARAMS['spike_headroom_gb']}}),
                               ('VARIANT_gate_route_a_cap4', {'kind': 'gate', 'm': 12, 'params': {'route_a_cap': 4}}),
                               ('VARIANT_gate_route_a_cap5', {'kind': 'gate', 'm': 12, 'params': {'route_a_cap': 5}}),
                               ('VARIANT_gate_route_a_cap6', {'kind': 'gate', 'm': 12, 'params': {'route_a_cap': 6}})):
                camp['%s|%s|%s' % (wname, scen, pname)] = campaign(tab, scen, waves, pol)
            # new + a target-free NGC probe on idle cores for its whole length (foreign to the campaign)
            T = NGC_T_H[scen] * 3600.0
            probe = Call('ngc_probe', ngc_segments(T, NGC_C), cls_ngc(11.0), 'NGC')
            camp['%s|%s|NEW_gate_max_concurrent12+NGC_probe' % (wname, scen)] = campaign(tab, scen, waves, {'kind': 'gate', 'm': 12},
                                                                                         background=[probe])
    rec['campaign'] = camp
    # 3. direct batches
    dirb = {}
    chosen = {}
    MEM_CRITERION_GB = 120.0                                    # peak total footprint in the expected and 32-iteration rows
    for bname, n, kind in (('HEADLINE11', 11, 'DDO'), ('SENS9', 9, 'DDO'), ('DIII4', 4, 'OFF'), ('POST_S1_2', 2, 'DDO')):
        for scen in ('low', 'expected', 'high'):
            for k in range(1, min(G.PARAMS['route_a_cap'], n) + 1):
                dirb['%s|%s|RAMP_max_active%d' % (bname, scen, k)] = direct(tab, scen, n, {'kind': 'ramp', 'max_active': k}, kind)
            dirb['%s|%s|PLANNED_shared_gate_guard_v011' % (bname, scen)] = direct(tab, scen, n, {'kind': 'gate', 'm': n}, kind)
        ok = [k for k in range(1, min(G.PARAMS['route_a_cap'], n) + 1)
              if all(dirb['%s|%s|RAMP_max_active%d' % (bname, s, k)]['max_total_mem_gb'] <= MEM_CRITERION_GB for s in ('expected', 'high'))]
        chosen[bname] = max(ok) if ok else 1
    rec['direct_batches'] = dirb
    rec['direct_batches_chosen_max_active'] = {
        'rule': 'the largest max_active (<= the gate route-A cap, <= n) whose simulated peak total footprint is <= %.0f GB in the '
                'expected and the 32-iteration (high) rows: the packet\'s memory check (memory_pressure) is blind, so max_active '
                'is its only memory lever; the low rows combine D5 cycle lengths with C4T footprints and are not used' % MEM_CRITERION_GB,
        'chosen': chosen, 'codex1_template_proposal': 3}
    # 4. step 5
    s5 = {}
    for scen in ('low', 'expected', 'high'):
        for M in (4, 6, 8, 10):
            for S in (2, 6):
                for rule in ('proposed_caps', 'serial_1', 'serial_2', 'new'):
                    s5['M%d_S%d|%s|%s' % (M, S, scen, rule)] = step5(tab, scen, M, S, rule)
                s5['M%d_S%d|%s|new+probe' % (M, S, scen)] = step5(tab, scen, M, S, 'new', probe=True)
        for rule in ('serial_1', 'serial_2', 'new'):
            s5['M6_S6_ORIGINAL_K|%s|%s' % (scen, rule)] = step5(tab, scen, 6, 6, rule, original_k=True)
        s5['M6_S6_ORIGINAL_K|%s|new+probe' % scen] = step5(tab, scen, 6, 6, 'new', original_k=True, probe=True)
    rec['step5'] = s5
    # 5. disk guard
    free0 = B['free_GiB'].get('/Volumes/External1')
    dk = {}
    for wname, waves in (('LAUNCH_ORDER', LO_WAVES), ('ENGINE_SHAPED', ENGINE_WAVES)):
        for gb in (13.9, 20.2, 26.5):
            for guard in (48.0, 56.0):
                dk['%s|%.1fGB_per_call|guard%dGiB' % (wname, gb, guard)] = disk_check(waves, gb, guard, free0)
                dk['%s|%.1fGB_per_call|guard%dGiB|+HEADLINE11_on_External1' % (wname, gb, guard)] = disk_check(waves, gb, guard, free0, pre_calls=11)
    rec['disk_guard'] = {'free0_GiB_External1_MEASURED': free0, 'rows': dk}
    # 6. end to end (compute only; root steps, certificates, acceptance not modelled)
    e2e = {}
    for scen in ('low', 'expected', 'high'):
        h_old = dirb['HEADLINE11|%s|RAMP_max_active3' % scen]['makespan_h']
        h_new = dirb['HEADLINE11|%s|RAMP_max_active%d' % (scen, chosen['HEADLINE11'])]['makespan_h']
        h_planned = dirb['HEADLINE11|%s|PLANNED_shared_gate_guard_v011' % scen]['makespan_h']
        for wname in ('LAUNCH_ORDER_[1]+19x[6]+[5]', 'ENGINE_SHAPED_ASSUMED'):
            c1 = camp['%s|%s|OLD_max_concurrent1_budget17' % (wname, scen)]['makespan_h']
            c6 = camp['%s|%s|OLD_max_concurrent6_budget17' % (wname, scen)]['makespan_h']
            cn = camp['%s|%s|NEW_gate_max_concurrent12' % (wname, scen)]['makespan_h']
            cp = camp['%s|%s|NEW_gate_max_concurrent12+NGC_probe' % (wname, scen)]['makespan_h']
            s_old1 = s5['M6_S6|%s|serial_1' % scen]['makespan_h']
            s_old2 = s5['M6_S6|%s|serial_2' % scen]['makespan_h']
            s_new = s5['M6_S6|%s|new' % scen]['makespan_h']
            s_probe = s5['M6_S6|%s|new+probe' % scen]['makespan_h']
            e2e['%s|%s' % (wname, scen)] = {
                'OLD_as_shipped_mc1_then_serial1_h': round(h_old + c1 + s_old1, 1),
                'OLD_proposed_mc6_then_serial2_h': round(h_old + c6 + s_old2, 1),
                'OLD_proposed_mc6_then_serial1_h': round(h_old + c6 + s_old1, 1),
                'NEW_h': round(h_new + cn + s_new, 1), 'NEW_with_probe_h': round(h_new + cp + s_probe, 1),
                'NEW_with_planned_guard_v011_headline_h': round(h_planned + cn + s_new, 1),
                'parts': {'headline_old': h_old, 'headline_new': h_new, 'headline_planned_guard_v011': h_planned,
                          'campaign_mc1': c1, 'campaign_mc6': c6, 'campaign_new': cn,
                          'campaign_new_probe': cp, 'step5_serial1': s_old1, 'step5_serial2': s_old2, 'step5_new': s_new,
                          'step5_new_probe': s_probe}}
    rec['end_to_end_M6_S6'] = e2e
    with open(out_path, 'x') as f:
        json.dump(rec, f, indent=1)
        f.write('\n')
    print(json.dumps({'cross_check': xc, 'end_to_end': {k: {kk: vv for kk, vv in v.items() if kk != 'parts'} for k, v in e2e.items()}}, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:])
