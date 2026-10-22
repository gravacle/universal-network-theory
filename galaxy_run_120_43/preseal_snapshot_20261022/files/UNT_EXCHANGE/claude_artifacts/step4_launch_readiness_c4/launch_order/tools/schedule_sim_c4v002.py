# Claude4 helper, dispatch 0587 part (3)/(d): deterministic schedule arithmetic for the step-4 runs.
# v002 = v001 + (1) the per-wave cap metric now counts calls whose START would fall after campaign_wall_cap_s (172800 s;
# campaign_c2v005 starts nothing after the cap, running calls continue), (2) campaign scenarios with a process budget
# above the hard-coded 17 (would need a successor), (3) a mixed queue (9 headline then 18 sensitivity) with the
# headline-subset completion time. v001's record is kept.
# NOT a measurement and NOT a launch: it reads the measured timing records from bytes, builds per-call segment
# models from them, and replays admission rules on a simulated clock (processor-sharing fluid model).
# Every output number is a projection (UNTESTED); only the arithmetic is TESTED (deterministic, re-runnable).
# Usage: python3 -I -B schedule_sim_c4v001.py <new output json>
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_c4v001 as F  # audit hook first
import hashlib, json, math, datetime

TIMING = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/kbig_timing_v003/TIMING_V003.json'
TIMING_SHA = '3e3fb60081acf19c6247bda056ebcb92a4cfb4439dbe912b8b6213da4f9ec925'
PROJ = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/results/projection_c2v001.json'
PROJ_SHA = 'cffa3150a2aac120bad1fdb045a93f645b938f76f22c3e8ff0bce56f387eaad2'
COSTW = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/COST_WAVES_CX2V002.json'
COSTW_SHA = '8301e37953c3231fc04a9d0333d623116abfd3c135d1fef38e47181a440a0ce7'
COSTM = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/certificate_analysis/COST_MODEL_CX2V001.json'
COSTM_SHA = '06f9f528024f90335ec6e55011b68fa70d4d1926ce85beae43d64d2e2f123862'

# Modelled memory (A61 text, modelled not measured; UNTESTED for tail-ON route A): route-A baseline about 10.5 GB at 96 nodes
# plus about 0.40 GiB of tail state per worker at K_big 128; after route A, C4R3's admitted-route-A peak 3.01 GB plus the
# measured K128 route-B build peak 1.29 GiB (TIMING_V003). All treated as GiB (conservative).
MEM_RA_TAIL_ON = 10.5 + 8 * 0.40
MEM_RA_TAIL_OFF = 10.5
MEM_AFTER_TAIL_ON = 3.01 + 1.29
MEM_AFTER_TAIL_OFF = 3.01
MEM_TOTAL = 128.0
MEM_BACKGROUND = 17.0   # 13% used at the 19:32Z memory_pressure reading (87% free), rounded up; transient (TESTED once)


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load_pinned(p, want):
    got = sha_file(p)
    if got != want:
        raise SystemExit('PIN_MISMATCH %s %s' % (p, got))
    with open(p, 'rb') as f:
        return json.loads(f.read())


def call_model(T, P, kind, scen, w8):
    """Segments (name, solo_seconds, busy_processes). kind: TAIL_ON (C4T-like K128 M_s128) or TAIL_OFF.
    scen: E (I=7,P=3), U_AS_IS (I=32,P=6, TIMING_V003 baseline unscaled), U_ADJ (route-A baseline scaled to I=32)."""
    m = T['measured']['128']['route_a']['solo_estimate']
    a_cold, a_warm = m['cold_s'], m['warm_s']
    bt = T['baseline_tail_off']
    ra8_lo, ra8_hi = bt['route_a_8_workers_s_PROJECTION_UNTESTED']
    I = 7 if scen == 'E' else 32
    # prep derived from the projection: route_a_8_workers = prep + 7 x per-iteration(N=8)
    prep = ra8_lo - 7 * w8['low']
    w = (w8['low'] + w8['high']) / 2.0
    base_route_b = bt['C4R3_receipt_offset_to_le3_s'] + (0 if scen == 'E' else 3 * T['baseline_extra_pass_s']) \
        + bt['C4_V005_reference_s'] + bt['C4_V005_body_s']
    segs = [('prep', prep, 1)]
    if kind == 'TAIL_ON':
        sc = T['scenarios']['C4T_expected_I7_P3' if scen == 'E' else 'C4T_upper_I32_P6']
        tail_b = sc['tail_solo_estimate']['route_b_side_s']
        segs.append(('A_cold', a_cold, 1))
        for i in range(I):
            segs.append(('A_wave', w, 8))
            segs.append(('A_warm', a_warm, 1))
        segs.append(('manifest', a_cold, 1))
        route_b = base_route_b + tail_b
    else:
        for i in range(I):
            segs.append(('A_wave', w, 8))
        route_b = base_route_b
    if scen == 'U_AS_IS':
        # TIMING_V003 kept the I=7 route-A baseline in its I=32 total; reproduce that total by shortening nothing:
        # report it separately (as_is_total) but simulate with the scaled route A (the adjusted model).
        pass
    segs.append(('route_b', route_b, P))
    return segs


def totals(segs):
    return sum(s[1] for s in segs)


class Call:
    def __init__(self, name, segs, kind):
        self.name, self.segs, self.kind = name, [list(s) for s in segs], kind
        self.i = 0
        self.rem = self.segs[0][1]
        self.start = None
        self.end = None
        self.first_iter_t = None
        self.ra_done_t = None
        self.n_waves_done = 0

    def in_route_a(self):
        return self.start is not None and self.end is None and self.ra_done_t is None

    def busy(self):
        if self.start is None or self.end is not None:
            return 0
        return self.segs[self.i][2]

    def weight(self):  # campaign_c2v005 accounting: peak 8 until route A finished (or a later stage started), then 2
        return 8 if self.in_route_a() else 2

    def mem(self):
        if self.start is None or self.end is not None:
            return 0.0
        if self.in_route_a():
            return MEM_RA_TAIL_ON if self.kind == 'TAIL_ON' else MEM_RA_TAIL_OFF
        return MEM_AFTER_TAIL_ON if self.kind == 'TAIL_ON' else MEM_AFTER_TAIL_OFF

    def advance(self, dt_solo, t_now):
        while dt_solo > 1e-12 and self.end is None:
            take = min(dt_solo, self.rem)
            self.rem -= take
            dt_solo -= take
            if self.rem <= 1e-9:
                name = self.segs[self.i][0]
                if name == 'A_wave':
                    self.n_waves_done += 1
                    if self.first_iter_t is None:
                        self.first_iter_t = t_now
                self.i += 1
                if self.i >= len(self.segs):
                    self.end = t_now
                    break
                nxt = self.segs[self.i][0]
                if self.ra_done_t is None and nxt in ('manifest', 'route_b'):
                    self.ra_done_t = t_now
                self.rem = self.segs[self.i][1]


def simulate(calls, policy, cores, dt=30.0, poll=60.0, waves=None, max_t=3.0e7):
    """policy: dict(kind='ramp', ra_cap=int|None, budget=int|None, mem_gate=25|None) for direct batches, or
    dict(kind='campaign', m=int, budget=17) for campaign_c2v005's FIFO budget rule (no ramp, no memory gate).
    waves: list of lists of Call for the campaign (a wave starts when the previous wave has fully finished)."""
    t = 0.0
    if waves is None:
        waves = [calls]
    stats = {'max_route_a': 0, 'max_demand': 0.0, 'max_accounted': 0, 'min_free_percent': 100.0, 'max_running': 0}
    wave_spans = []
    late_starts = []
    for wcalls in waves:
        pending = list(wcalls)
        active = []
        prev = None
        next_poll = t
        w0 = t
        while pending or active:
            if t >= next_poll and pending:
                while pending:
                    head = pending[0]
                    ra = sum(1 for c in active if c.in_route_a())
                    acc = sum(c.weight() for c in active)
                    used = MEM_BACKGROUND + sum(c.mem() for c in active)
                    free_pct = 100.0 * (MEM_TOTAL - used) / MEM_TOTAL
                    if policy['kind'] == 'campaign':
                        ok = (acc + 8 <= policy['budget']) and (len(active) < policy['m'])
                    else:
                        if prev is None:
                            ok = True
                        else:
                            ramp = prev.first_iter_t is not None
                            ok = ramp
                            if policy.get('ra_cap') is not None:
                                ok = ok and ra < policy['ra_cap']
                            if policy.get('budget') is not None:
                                ok = ok and acc + 8 <= policy['budget']
                            if policy.get('mem_gate') is not None:
                                ok = ok and free_pct >= policy['mem_gate']
                    if not ok:
                        break
                    pending.pop(0)
                    head.start = t
                    active.append(head)
                    prev = head
                    if policy['kind'] != 'campaign':
                        break   # the V005 worker starts at most one case per poll
                next_poll = t + poll
            demand = sum(c.busy() for c in active)
            rate = 1.0 if demand <= cores else cores / demand
            stats['max_route_a'] = max(stats['max_route_a'], sum(1 for c in active if c.in_route_a()))
            stats['max_demand'] = max(stats['max_demand'], demand)
            stats['max_accounted'] = max(stats['max_accounted'], sum(c.weight() for c in active))
            stats['max_running'] = max(stats['max_running'], len(active))
            used = MEM_BACKGROUND + sum(c.mem() for c in active)
            stats['min_free_percent'] = min(stats['min_free_percent'], 100.0 * (MEM_TOTAL - used) / MEM_TOTAL)
            t += dt
            for c in list(active):
                c.advance(dt * rate, t)
                if c.end is not None:
                    active.remove(c)
            if t > max_t:
                raise SystemExit('SIM_TIMEOUT')
        wave_spans.append(t - w0)
        late_starts.append(sum(1 for c in wcalls if c.start - w0 > 172800.0))
    allc = [c for w in waves for c in w]
    return {
        'makespan_h': round(t / 3600.0, 2),
        'wave_spans_h': [round(x / 3600.0, 2) for x in wave_spans] if len(waves) > 1 else None,
        'calls_starting_after_48h_wave_cap': sum(late_starts) if len(waves) > 1 else None,
        'per_call_wall_h': [round((c.end - c.start) / 3600.0, 2) for c in allc] if len(allc) <= 24 else None,
        'per_call_wall_h_min_max': [round(min((c.end - c.start) for c in allc) / 3600.0, 2), round(max((c.end - c.start) for c in allc) / 3600.0, 2)],
        'starts_h': [round(c.start / 3600.0, 2) for c in allc] if len(allc) <= 24 else None,
        'first_iteration_after_start_min': round(min(c.first_iter_t - c.start for c in allc) / 60.0, 1),
        **stats,
    }


def main(out):
    T = load_pinned(TIMING, TIMING_SHA)
    PJ = load_pinned(PROJ, PROJ_SHA)
    CW = load_pinned(COSTW, COSTW_SHA)
    CM = load_pinned(COSTM, COSTM_SHA)
    n8 = [r for r in PJ['DDO154_KMAX_A2F10_C4_measured']['rows'] if r['N'] == 8][0]
    w8 = {'low': n8['seconds_low'], 'high': n8['seconds_high']}
    utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    rec = {'schema': 'STEP4_SCHEDULE_SIM_C4V002', 'utc': utc,
           'label': 'UNTESTED projections; TESTED arithmetic (deterministic replay of stated inputs); not launch authorization',
           'inputs': {'timing_v003': {'path': TIMING, 'sha256': TIMING_SHA}, 'projection_c2v001': {'path': PROJ, 'sha256': PROJ_SHA},
                      'cost_waves_cx2v002': {'path': COSTW, 'sha256': COSTW_SHA}, 'cost_model_cx2v001': {'path': COSTM, 'sha256': COSTM_SHA}},
           'assumptions': {
               'route_a_per_iteration_N8_s': w8, 'route_a_prep_s': T['baseline_tail_off']['route_a_8_workers_s_PROJECTION_UNTESTED'][0] - 7 * w8['low'],
               'tail_builds_K128_solo_s': {'A_cold': T['measured']['128']['route_a']['solo_estimate']['cold_s'], 'A_warm': T['measured']['128']['route_a']['solo_estimate']['warm_s']},
               'scenarios': {'E': 'I=7 route-A iterations, P=3 Picard passes (both MEASURED on the tail-OFF lineage, tail-ON UNTESTED)',
                             'U_ADJ': 'I=32, P=6 (spec maxima) with the route-A 8-worker baseline scaled to 32 iterations; TIMING_V003 itself kept the I=7 route-A baseline in its I=32 total'},
               'route_b_busy_processes': 'fluid model: P=1.5 (assumed mean of 1-process stages and 2-process column waves); accounting weight 2 as campaign_c2v005',
               'memory_model_GiB': {'route_a_tail_on': MEM_RA_TAIL_ON, 'route_a_tail_off': MEM_RA_TAIL_OFF, 'after_tail_on': MEM_AFTER_TAIL_ON,
                                    'after_tail_off': MEM_AFTER_TAIL_OFF, 'total': MEM_TOTAL, 'background_used': MEM_BACKGROUND},
               'cores_available': '18 (whole machine; other work at background QoS) or 12 (other work keeps about 6 cores busy at equal priority)',
               'not_modelled': ['P/E core heterogeneity', 'memory bandwidth', 'TailState IPC to 8 route-A workers (UNMEASURED in TIMING_V003)',
                                'tail evaluation costs inside stage solves (not in the baseline)', 'orchestrator ingest/plan time between waves',
                                'root work between batches', 'failures, halts, retries'],
           }}
    # per-call solo totals
    per_call = {}
    for kind in ('TAIL_ON', 'TAIL_OFF'):
        for scen in ('E', 'U_ADJ'):
            segs = call_model(T, 1.5, kind, scen, w8)
            per_call['%s_%s' % (kind, scen)] = {'solo_h': round(totals(segs) / 3600.0, 2),
                                                 'route_a_phase_h': round(sum(s[1] for s in segs if s[0] in ('prep', 'A_cold', 'A_wave', 'A_warm')) / 3600.0, 2),
                                                 'first_iteration_solo_min': round((segs[0][1] + (segs[1][1] if kind == 'TAIL_ON' else 0) + segs[2 if kind == 'TAIL_ON' else 1][1]) / 60.0, 1)}
    sc = T['scenarios']
    per_call['TIMING_V003_as_is'] = {
        'C4T_E_solo_h': sc['C4T_expected_I7_P3']['hours_solo_full_baseline'], 'C4T_U_solo_h': sc['C4T_upper_I32_P6']['hours_solo_full_baseline'],
        'tail_off_E_solo_h': [round(x / 3600.0, 2) for x in sc['C4T_expected_I7_P3']['baseline_tail_off_full_call_s']],
        'tail_off_U_solo_h': [round(x / 3600.0, 2) for x in sc['C4T_upper_I32_P6']['baseline_tail_off_full_call_s']],
        'cached_r6_C4T_E_solo_h_UNTESTED': sc['C4T_expected_I7_P3']['hours_solo_full_baseline_if_cached_UNTESTED'],
        'cached_r6_C4T_U_solo_h_UNTESTED': sc['C4T_upper_I32_P6']['hours_solo_full_baseline_if_cached_UNTESTED'],
        'wall_ratio_under_load_rows': [r['wall_ratio'] for r in T['calibration']['rows']], 'mean_wall_ratio': T['calibration']['mean_wall_ratio'],
    }
    per_call['route_a_tail_build_per_call_6_iterations_V002'] = {
        'K64_s': CM['timings']['64']['projection_A_build_only'][0]['seconds'], 'K128_s': CM['timings']['128']['projection_A_build_only'][0]['seconds'],
        'note': 'COST_MODEL_CX2V001 (M_s 64 V002 rows): 4.5 min at K_big 64 and 15.1 min at 128; superseded for M_s 128 by TIMING_V003 (same cost, TESTED there)'}
    rec['per_call'] = per_call

    policies = {
        'V005_AS_IS': {'kind': 'ramp', 'ra_cap': 6, 'budget': None, 'mem_gate': 25},
        'RAMP_RA3': {'kind': 'ramp', 'ra_cap': 3, 'budget': None, 'mem_gate': 25},
        'RAMP_RA2': {'kind': 'ramp', 'ra_cap': 2, 'budget': None, 'mem_gate': 25},
        'RAMP_BUDGET16': {'kind': 'ramp', 'ra_cap': 2, 'budget': 16, 'mem_gate': 25},
        'NO_GATE_ALL_AT_ONCE': {'kind': 'ramp_none'},
    }

    def batch(n, kind, scen, pol, cores):
        calls = [Call('c%02d' % i, call_model(T, 1.5, kind, scen, w8), kind) for i in range(n)]
        if pol['kind'] == 'ramp_none':
            p = {'kind': 'campaign', 'm': 10 ** 6, 'budget': 10 ** 6}
        else:
            p = pol
        return simulate(calls, p, cores)

    batches = {}
    for label, n, kind in (('HEADLINE_9', 9, 'TAIL_ON'), ('HEADLINE_10', 10, 'TAIL_ON'), ('HEADLINE_11', 11, 'TAIL_ON'),
                           ('SENS_9_ONE_D', 9, 'TAIL_ON'), ('SENS_18_BOTH_D', 18, 'TAIL_ON'), ('DIII_4', 4, 'TAIL_OFF'),
                           ('POST_S1_2', 2, 'TAIL_ON')):
        for scen in ('E', 'U_ADJ'):
            for pn, pol in policies.items():
                for cores in (18, 12):
                    batches['%s|%s|%s|cores%d' % (label, scen, pn, cores)] = batch(n, kind, scen, pol, cores)
    rec['batches'] = batches

    # campaign: 120 calls in waves [1] + 19x[6] + [5] (coordinate spec: "120 = 20 batches of 6"; seed wave of 1 TESTED by the dry plans)
    sizes = [1] + [6] * 19 + [5]
    camp = {}
    for scen in ('E', 'U_ADJ'):
        for m in (1, 2, 3, 6):
            for cores in (18, 12):
                waves = [[Call('w%02dc%d' % (wi, j), call_model(T, 1.5, 'TAIL_ON', scen, w8), 'TAIL_ON') for j in range(sz)] for wi, sz in enumerate(sizes)]
                r = simulate(None, {'kind': 'campaign', 'm': m, 'budget': 17}, cores, waves=waves)
                r['n_calls'] = sum(sizes)
                r['n_waves'] = len(sizes)
                r['makespan_days'] = round(r['makespan_h'] / 24.0, 1)
                r['max_wave_span_h'] = max(r['wave_spans_h'])
                r['waves_spanning_over_48h'] = sum(1 for x in r['wave_spans_h'] if x > 48.0)
                camp['%s|max_concurrent%d|budget17|cores%d' % (scen, m, cores)] = r
    # (2) process budget above the hard-coded PROCESS_BUDGET_MAX = 17 (v005 L171): what a successor would buy
    for scen in ('E', 'U_ADJ'):
        for bud in (24, 48):
            for cores in (18, 12):
                waves = [[Call('w%02dc%d' % (wi, j), call_model(T, 1.5, 'TAIL_ON', scen, w8), 'TAIL_ON') for j in range(sz)] for wi, sz in enumerate(sizes)]
                r = simulate(None, {'kind': 'campaign', 'm': 6, 'budget': bud}, cores, waves=waves)
                r['n_calls'] = sum(sizes)
                r['makespan_days'] = round(r['makespan_h'] / 24.0, 1)
                r['max_wave_span_h'] = max(r['wave_spans_h'])
                r['needs_successor'] = 'PROCESS_BUDGET_MAX 17 is hard-coded (v005 L171; config validation L1727-1728)'
                camp['%s|max_concurrent6|budget%d|cores%d|SUCCESSOR_ONLY' % (scen, bud, cores)] = r
    rec['campaign'] = camp
    # (3) mixed queue: 9 headline first, then 18 sensitivity, one ramp-gated queue
    mixed = {}
    for scen in ('E', 'U_ADJ'):
        for pn in ('RAMP_RA3', 'RAMP_BUDGET16'):
            for cores in (18, 12):
                calls = [Call('h%02d' % i, call_model(T, 1.5, 'TAIL_ON', scen, w8), 'TAIL_ON') for i in range(9)] + \
                        [Call('s%02d' % i, call_model(T, 1.5, 'TAIL_ON', scen, w8), 'TAIL_ON') for i in range(18)]
                r = simulate(calls, policies[pn], cores)
                r['headline_subset_done_h'] = round(max(c.end for c in calls[:9]) / 3600.0, 2)
                r['per_call_wall_h'] = None
                r['starts_h'] = None
                mixed['MIXED_9H_18S|%s|%s|cores%d' % (scen, pn, cores)] = r
    rec['mixed_queue'] = mixed
    rec['fence_blocked'] = F.BLOCKED
    rec['producer'] = {'path': os.path.abspath(__file__), 'sha256': sha_file(os.path.abspath(__file__))}
    with open(out, 'x') as f:
        json.dump(rec, f, indent=1, sort_keys=True)
        f.write('\n')
    keyb = ['HEADLINE_9|E|RAMP_BUDGET16|cores18', 'HEADLINE_9|E|RAMP_RA3|cores18', 'HEADLINE_9|E|V005_AS_IS|cores18',
            'HEADLINE_9|E|NO_GATE_ALL_AT_ONCE|cores18', 'HEADLINE_9|U_ADJ|RAMP_BUDGET16|cores18', 'HEADLINE_9|U_ADJ|RAMP_RA3|cores18']
    print(json.dumps({'out': out, 'per_call': {k: v for k, v in per_call.items() if k.startswith('TAIL')},
                      'sample': {k: {kk: batches[k][kk] for kk in ('makespan_h', 'max_route_a', 'max_demand', 'min_free_percent')} for k in keyb},
                      'campaign_sample': {k: {kk: v.get(kk) for kk in ('makespan_h', 'makespan_days', 'max_wave_span_h', 'calls_starting_after_48h_wave_cap')} for k, v in camp.items()},
                      'mixed': {k: {kk: v[kk] for kk in ('makespan_h', 'headline_subset_done_h', 'max_route_a', 'min_free_percent')} for k, v in mixed.items()},
                      'blocked': F.BLOCKED}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
