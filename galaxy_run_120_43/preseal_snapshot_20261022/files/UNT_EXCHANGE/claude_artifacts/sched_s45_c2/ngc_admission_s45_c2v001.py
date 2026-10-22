"""INERT step-5 admission loop for the NGC K_big 32 integrated calls (Claude2 sched_s45_c2, ngc_admission_s45_c2v001).

Replaces the RI45-12 schedule as proposed (first point solo to completion, then 1-2 at a time) and the proposed per-point
caps (12 h wall, 5 GiB RSS, 32 GiB output: every call would be killed; the DERIVED call length is 11.7-56.3 h) with rules
set from measurement:
  * order: the root launch plan's order (root writes: S4-POST-S1 goes through its own path first; then NGC headline
    members, ORIGINAL_K, NGC sensitivity).  FIFO; the head is never skipped.  A call may name groups that must be
    complete before it starts (requires_groups_complete, e.g. the sensitivity calls after every headline member: D1);
  * first call solo until it has completed SOLO_ITERATIONS route-A iterations (or has ended), unless the plan carries a
    measured basis from a target-free probe (RI45-12 (i)); then the caps and the admission reservation are COMPUTED
    from that measurement, never below the wave-1 caps;
  * every start passes the shared machine gate machine_gate_s45_c2v001 (pinned by sha256) with an NGC class: route A
    1.0 busy core (MEASURED serial analog N1: 0.91-1.0), after route A 2.0 (numerics.column_workers, upper bound),
    route-A reservation = iteration-0 peak + half the projected state-build transient (DERIVED 11 GB until measured),
    spacing 600 s, <= 16 running;
  * a disk guard before each start: free >= sum over running calls of (their output cap - output so far) + the head's
    output cap + 20 GiB.
Reads: ps/top/sysctl (gate), the stage/event/iteration/elapsed_seconds fields of each owned call's progress logs, the
owned calls' monitor receipts (status, elapsed, peak RSS, output bytes only) and directory sizes.  It never opens a
result, array, node-diagnostic or target file.  Writes only inside plan.work_dir (exclusive create).
Nothing here is a launch authorization: root launches, under a V006 entry.
CLI:  ngc_admission_s45_c2v001.py --plan PLAN.json   (refuses unless the plan pins are verified from bytes)
Importing this module does nothing.
"""
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

MODULE_NAME = 'ngc_admission_s45_c2v001'
GATE_PATH = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sched_s45_c2/machine_gate_s45_c2v001.py'
GATE_SHA256 = '6d0c45f8948d54d208809671af6ffa96197f5079aa73100991c7fa9d04cb93fa'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'BLIS_NUM_THREADS')
GiB = 1 << 30
PARAMS = {
    'max_concurrent': 16,
    'spacing_s': 600.0,                 # DERIVED: serial calls with ~16-min setups; staggers their state builds
    'solo_iterations': 2,               # first call alone until 2 route-A iterations completed (or it ended)
    'max_iterations': 16,               # NGC numerics.route_a.max_iterations (FORMAL, cx3r008 templates)
    'wave1': {'wall_cap_s': 259200,                     # 72 h = 1.28 x root's DERIVED upper 56.3 h
              'rss_cap_bytes': 32 * GiB,                # >= 1.5 x the DERIVED serial peak 15-20 GB (u4 map: vf 10.2 GB
                                                        #    at state 16, q = 17 ASSUMED, + TailState/prepared/caches)
              'output_cap_bytes': 136 * GiB},           # 1.5 x the DERIVED 89.7 GiB (16 iterations x 6.02 GB: the
                                                        #    MEASURED DDO K128 per-iteration output scaled by NGC columns
                                                        #    (x 8.67) and waves (x 1.30); see README)
    'cap_margin': 1.5,                  # A61 rule (RSS caps >= 1.5 x the modelled peak), used for all three caps
    'load_factor': 1.25,                # DERIVED: mean load at the gate's core limit (24 / 18 weights, owned upper bounds)
    'route_a_fraction': 0.7,            # DERIVED (root): T_A ~ 0.7 T
    'route_b_output_allowance_bytes': 10 * 10 ** 9,     # ASSUMED (MEASURED DDO route-B outputs are MBs; margin)
    'w_route_a': 1.0, 'w_after': 2.0,
    'res_route_a_gb_initial': 11.0,     # DERIVED: 5 GB steady + half the 10.2 GB state-16 vf transient (u4 map, q = 17
                                        #   ASSUMED), rounded up to the DDO route-A reservation
    'res_after_gb': 6.0,                # ASSUMED (as the gate)
    'disk_reserve_bytes': 20 * GiB,
    'poll_s': 30.0,
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _load_pinned(path, sha, name):
    import types
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError('%s pin mismatch' % name)
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def dir_bytes(path):
    total = 0
    for root, _, files in os.walk(path):
        for n in files:
            try:
                total += os.lstat(os.path.join(root, n)).st_size
            except OSError:
                pass
    return total


def iteration_events(outdir):
    """[(iteration, kind, elapsed_s)] from <outdir>/stages/*/attempt_*/progress.jsonl -- stage/iteration/elapsed only."""
    ev = []
    for p in sorted(Path(outdir).glob('stages/*/attempt_*/progress.jsonl')):
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        for ln in raw.split(b'\n'):
            try:
                d = json.loads(ln)
            except ValueError:
                continue
            if isinstance(d, dict) and d.get('stage') in ('iteration_prepared', 'iteration_completed') \
                    and type(d.get('iteration')) is int:
                ev.append((d['iteration'], d['stage'], float(d.get('elapsed_seconds') or 0.0)))
    return ev


def receipt_fields(path):
    """Only the resource fields of a monitor receipt (never its result block)."""
    try:
        r = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return None
    return {k: r.get(k) for k in ('status', 'stop_reason', 'exit_code', 'driver_status', 'elapsed_seconds',
                                  'peak_rss_bytes', 'peak_output_bytes', 'final_output_bytes')}


def compute_caps(basis, P=PARAMS):
    """basis: {'rss_by_iter': [B at it 0, it 1, ...], 'out_by_iter': [B after it 0, 1, ...], 'prep_s', 't_iter_s'}
    (MEASURED on the first call or the probe).  -> caps (never below wave 1) and the admission reservation."""
    w1 = P['wave1']
    n = P['max_iterations']
    m = P['cap_margin']
    rss = [float(x) for x in basis['rss_by_iter']]
    out = [float(x) for x in basis['out_by_iter']]
    k = len(rss)
    slope = max(0.0, rss[-1] - rss[-2]) if k >= 2 else 0.0
    proj_rss = rss[-1] + (n - k) * slope
    dout = max(0.0, out[-1] - out[-2]) if len(out) >= 2 else out[-1]
    proj_out = out[-1] + (n - len(out)) * dout + P['route_b_output_allowance_bytes']
    proj_wall = P['load_factor'] * (float(basis['prep_s']) + n * float(basis['t_iter_s'])) / P['route_a_fraction']
    caps = {'wall_cap_s': int(max(w1['wall_cap_s'], math.ceil(m * proj_wall))),
            'rss_cap_bytes': int(max(w1['rss_cap_bytes'], math.ceil(m * proj_rss))),
            'output_cap_bytes': int(max(w1['output_cap_bytes'], math.ceil(m * proj_out)))}
    # admission reservation: steady (iteration-0 peak) + half the projected state-build transient (DERIVED: the
    # transient lasts ~27 s per iteration index of a ~46-min cycle, so at most about half the calls' transients
    # coincide; one full transient sits in the gate's spike headroom)
    return {'caps': caps, 'res_route_a_gb': max(5.0, (rss[0] + proj_rss) / 2.0 / 1e9),
            'projection': {'rss_iter16_bytes': proj_rss, 'rss_slope_bytes_per_iteration': slope,
                           'output_bytes': proj_out, 'output_bytes_per_iteration': dout, 'wall_s': proj_wall},
            'basis': basis}


def ngc_class(G, res_route_a_gb, P=PARAMS):
    return G.make_class('NGC_K32_SERIAL', pooled=False, w_route_a=P['w_route_a'], w_after=P['w_after'],
                        res_route_a_gb=res_route_a_gb, res_after_gb=P['res_after_gb'])


def run_plan(plan, *, python=PY, _gate=None, _params=None, _free_bytes=None):
    """SYNTHETIC-test hooks: _gate (an injected Gate), _params (overrides of PARAMS), _free_bytes (callable)."""
    P = json.loads(json.dumps(PARAMS))
    if _params:
        P.update(_params)
    reasons = []
    wd = Path(plan.get('work_dir') or '')
    calls = plan.get('calls')
    drv, mon = plan.get('driver') or {}, plan.get('monitor') or {}
    if not wd.is_absolute():
        reasons.append('work_dir must be absolute')
    if wd.exists():
        reasons.append('work_dir exists (exclusive): %s' % wd)
    if not isinstance(calls, list) or not calls:
        reasons.append('calls must be a non-empty list')
    else:
        ids = [c.get('id') for c in calls]
        if len(set(ids)) != len(ids) or not all(isinstance(i, str) and i for i in ids):
            reasons.append('call ids must be unique non-empty strings')
        groups = set(c.get('group') for c in calls)
        for c in calls:
            for g in c.get('requires_groups_complete') or []:
                if g not in groups or g == c.get('group'):
                    reasons.append('call %s requires an unknown or its own group %r' % (c.get('id'), g))
    try:
        if sha256_file(drv['path']) != drv['sha256']:
            reasons.append('driver pin mismatch')
        if sha256_file(mon['path']) != mon['sha256']:
            reasons.append('monitor pin mismatch')
        for c in calls or []:
            if sha256_file(c['spec_path']) != c['spec_sha256']:
                reasons.append('spec pin mismatch: %s' % c.get('id'))
        G = _load_pinned(GATE_PATH, GATE_SHA256, 's45_machine_gate_ngc')
    except Exception as exc:                                    # noqa: BLE001
        reasons.append('%s: %s' % (type(exc).__name__, exc))
    if reasons:
        return {'ok': False, 'status': 'REFUSED', 'reasons': reasons}
    gate = _gate if _gate is not None else G.Gate(params={'spacing_s': P['spacing_s']})
    free_bytes = _free_bytes or (lambda: shutil.disk_usage(str(wd.parent)).free)
    wd.mkdir(parents=False)
    basis = plan.get('measured_basis')                          # from a probe (RI45-12 (i)), or None
    derived = compute_caps(basis, P) if basis else None
    caps = derived['caps'] if derived else dict(P['wave1'])
    res_gb = derived['res_route_a_gb'] if derived else P['res_route_a_gb_initial']
    pending = list(range(len(calls)))
    running, records, log = {}, {}, []
    first = None
    solo_done = basis is not None
    first_obs = {'rss_by_iter': {}, 'out_by_iter': {}}
    last_start = None
    t0 = time.monotonic()

    def group_complete(g):
        return all(records.get(j, {}).get('status') in ('FINISHED',) for j, c in enumerate(calls) if c.get('group') == g)

    def group_failed(g):
        return any(j in records and records[j].get('status') != 'FINISHED' for j, c in enumerate(calls) if c.get('group') == g)

    while pending or running:
        while pending and any(group_failed(g) for g in calls[pending[0]].get('requires_groups_complete') or []):
            k = pending.pop(0)                                  # a required group can no longer complete: root decides
            records[k] = {'id': calls[k]['id'], 'status': 'NOT_STARTED', 'reason': 'REQUIRED_GROUP_NOT_FINISHED_ROOT_DECIDES'}
            log.append({'t': round(time.monotonic() - t0, 2), 'event': 'not_started', 'call': calls[k]['id']})
        snap = gate.sample()
        # measure the first call (ps RSS of its tree = the monitor's own RSS metric; output bytes; iteration timing)
        if first is not None and not solo_done and first in running:
            p, d = running[first]['proc'], running[first]['dir']
            ev = iteration_events(d / 'out')
            done_its = sorted(set(i for i, k, _ in ev if k == 'iteration_completed'))
            cur_it = len(done_its)
            for r in snap.get('runs') or []:
                if r['monitor_pid'] == p.pid:
                    first_obs['rss_by_iter'][cur_it] = max(first_obs['rss_by_iter'].get(cur_it, 0), r['rss_bytes'])
            first_obs['out_by_iter'].setdefault(cur_it, dir_bytes(d / 'out'))   # first poll after cur_it iterations
            if cur_it >= P['solo_iterations']:
                ns = P['solo_iterations']
                prep = min((e for i, k, e in ev if k == 'iteration_prepared' and i == 0), default=0.0)
                comp = {i: e for i, k, e in ev if k == 'iteration_completed'}
                t_iter = (comp[ns - 1] - prep) / float(ns)       # mean cycle, gaps included
                b = {'rss_by_iter': [first_obs['rss_by_iter'].get(i, 0) for i in range(ns)],
                     'out_by_iter': [first_obs['out_by_iter'].get(i, 0) for i in range(1, ns + 1)],
                     'prep_s': prep, 't_iter_s': t_iter, 'source': 'first call, %d iterations' % ns}
                derived = compute_caps(b, P)
                caps, res_gb, solo_done = derived['caps'], derived['res_route_a_gb'], True
                log.append({'t': round(time.monotonic() - t0, 2), 'event': 'caps_computed', 'derived': derived})
        # finished calls
        for j in [j for j, r in running.items() if r['proc'].poll() is not None]:
            r = running.pop(j)
            for f in r['files']:
                f.close()
            rf = receipt_fields(r['dir'] / 'RECEIPT.json')
            records[j] = dict(rf or {'status': 'NO_RECEIPT'}, id=calls[j]['id'], caps=r['caps'], call_dir=str(r['dir']))
            log.append({'t': round(time.monotonic() - t0, 2), 'event': 'finish', 'call': calls[j]['id'],
                        'status': records[j].get('status')})
            if j == first and not solo_done:                    # ended before 2 iterations: caps from its receipt
                rf = rf or {}
                if rf.get('status') == 'FINISHED':
                    m = P['cap_margin']
                    caps = {'wall_cap_s': int(max(P['wave1']['wall_cap_s'], m * P['load_factor'] * float(rf.get('elapsed_seconds') or 0))),
                            'rss_cap_bytes': int(max(P['wave1']['rss_cap_bytes'], m * float(rf.get('peak_rss_bytes') or 0))),
                            'output_cap_bytes': int(max(P['wave1']['output_cap_bytes'], m * float(rf.get('final_output_bytes') or 0)))}
                    res_gb = max(5.0, float(rf.get('peak_rss_bytes') or 0) / 1e9)
                    solo_done = True
                    log.append({'t': round(time.monotonic() - t0, 2), 'event': 'caps_from_first_receipt', 'caps': caps})
                else:
                    log.append({'t': round(time.monotonic() - t0, 2), 'event': 'first_call_not_finished_halt'})
                    for k in pending:
                        records[k] = {'id': calls[k]['id'], 'status': 'NOT_STARTED', 'reason': 'FIRST_CALL_FAILED_ROOT_DECIDES'}
                    pending = []
        # admission of the head
        if pending:
            i = pending[0]
            c = calls[i]
            why = []
            if first is not None and not solo_done:
                why.append('SOLO_FIRST')
            for g in c.get('requires_groups_complete') or []:
                if not group_complete(g):
                    why.append('REQUIRES_%s' % g)
            cls = ngc_class(G, res_gb, P)
            owned = {r['proc'].pid: {'class': r['class'], 'progress': r['dir'] / 'out' / 'progress.jsonl'} for r in running.values()}
            dec = gate.decide(owned=owned, head=cls, n_running=len(running), max_concurrent=P['max_concurrent'],
                              last_own_start=last_start)
            why += dec['reasons']
            need = sum(max(0, r['caps']['output_cap_bytes'] - dir_bytes(r['dir'] / 'out')) for r in running.values()) \
                + caps['output_cap_bytes'] + P['disk_reserve_bytes']
            if free_bytes() < need:
                why.append('DISK_GUARD')
            if why:
                if not log or log[-1].get('event') != 'wait' or log[-1].get('reasons') != why:
                    log.append({'t': round(time.monotonic() - t0, 2), 'event': 'wait', 'call': c['id'], 'reasons': why})
            else:
                pending.pop(0)
                d = wd / ('call_%03d_%s' % (i, c['id']))
                d.mkdir()
                spec_raw = Path(c['spec_path']).read_bytes()
                if hashlib.sha256(spec_raw).hexdigest() != c['spec_sha256']:
                    raise RuntimeError('spec changed after validation: %s' % c['id'])
                with open(d / 'spec.json', 'xb') as f:
                    f.write(spec_raw)
                    f.flush()
                    os.fsync(f.fileno())
                cmd = [python, '-I', '-B', mon['path'], '--driver', drv['path'], '--driver-sha256', drv['sha256'],
                       '--spec', str(d / 'spec.json'), '--outdir', str(d / 'out'), '--receipt', str(d / 'RECEIPT.json'),
                       '--wall-cap-s', repr(float(caps['wall_cap_s'])), '--rss-cap-bytes', str(int(caps['rss_cap_bytes'])),
                       '--output-cap-bytes', str(int(caps['output_cap_bytes'])), '--poll-s', '2.0', '--python', python]
                env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
                for k in THREAD_ENV:
                    env[k] = '1'
                so, se = open(d / 'monitor.stdout.txt', 'x'), open(d / 'monitor.stderr.txt', 'x')
                proc = subprocess.Popen(cmd, stdout=so, stderr=se, env=env, start_new_session=True)
                last_start = time.monotonic()
                running[i] = {'proc': proc, 'dir': d, 'files': (so, se), 'caps': dict(caps), 'class': cls}
                if first is None:
                    first = i
                log.append({'t': round(last_start - t0, 2), 'event': 'start', 'call': c['id'], 'caps': dict(caps),
                            'res_route_a_gb': round(res_gb, 2), 'cores_after_admit': dec['cores_after_admit'],
                            'mem_after_admit_gb': dec['mem_after_admit_gb']})
        if pending or running:
            time.sleep(P['poll_s'])
    summary = {'schema': 'NGC_ADMISSION_SUMMARY_S45_C2V001', 'module': MODULE_NAME, 'ok': True,
               'status': 'COMPLETE' if all(r.get('status') == 'FINISHED' for r in records.values()) else 'INCOMPLETE',
               'calls': [records.get(j, {'id': c['id'], 'status': 'NOT_STARTED'}) for j, c in enumerate(calls)],
               'final_caps': caps, 'final_res_route_a_gb': res_gb, 'derived': derived, 'log': log,
               'gate': {'module': G.MODULE_NAME, 'sha256': GATE_SHA256, 'params': dict(gate.P), 'injected_for_test': _gate is not None},
               'params': P}
    sp = wd / ('NGC_ADMISSION_SUMMARY_%d.json' % time.time_ns())
    with open(sp, 'x') as f:
        json.dump(summary, f, indent=1, default=str)
        f.write('\n')
    summary['summary_path'] = str(sp)
    return summary


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--plan', required=True)
    ap.add_argument('--python', default=PY)
    a = ap.parse_args(argv)
    out = run_plan(json.loads(Path(a.plan).read_text()), python=a.python)
    print(json.dumps({k: v for k, v in out.items() if k not in ('calls', 'log')}, indent=1, default=str))
    return 0 if out.get('ok') else 2


if __name__ == '__main__':
    sys.exit(main())
