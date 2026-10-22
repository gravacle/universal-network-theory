"""Shared machine admission gate for step-4 / step-5 launches (Claude2 sched_s45_c2, c2v001).

One rule for every launcher that adopts it (campaign_s45_c2v001, ngc_admission_s45_c2v001; the direct-batch packet
successors when built).  It replaces the process-budget rule of campaign_c2v005 (route A counted as 8 busy processes,
budget 17: at most 2 calls in route A) and never reads memory_pressure (blind to private anonymous memory: it read
85-86 % free while the run footprint was 40.9 GB, MEASURED 2026-10-19).

The head of the queue starts only when ALL of these hold (FIFO: the head is never skipped):
  a. count     fewer than max_concurrent calls of this launcher run (the launcher's own wave wall cap stays its own);
  b. route-A   at most ROUTE_A_CAP pooled (parallel-worker) calls in route A machine-wide, the head included;
  c. cores     sum of busy-core weights of every run tree + the head's route-A weight <= CORE_LIMIT;
  d. memory    sum over every run tree of max(live footprint, reservation for its phase)
               + the head's route-A reservation + SPIKE_HEADROOM_GB <= MEM_LIMIT_GB;
  e. swap      swap used <= SWAP_STOP_GB;
  f. spacing   >= SPACING_S since the youngest root monitor on the machine (any launcher) and since this launcher's
               own last start;
  g. warm-up   the CPU sampler holds >= WARMUP_S of history (foreign runs are weighed by measured cores);
  h. probe     ps and swap could be read (fail closed).
A run tree = one root monitor process (argv matches MONITOR_PATTERN and carries --driver) plus the process group of its
driver child (the A130 metric of memory_watch_root_c2v002.sh).  Live footprint = sum of top MEM over that process group
(fallback: ps RSS x PS_TO_FOOTPRINT_MAX, flagged).  Phase = the driver's own <outdir>/progress.jsonl (route_a finished,
or any later stage started -> after route A), exactly the rule of campaign_c2v005.route_a_done; unreadable -> route A.
Route-A post-loop: a tree that once held a worker pool (>= POOLED_MIN_PROCS processes) and no longer does is still in
route A (the driver has not logged route_a finished) but no longer pooled; it is weighed and reserved as after route A
(MEASURED post-loop: 0.8-1.0 busy core, <= 3.8 GB, 18-40 min per call).

Owned runs (started by the calling launcher) are weighed by their declared class; foreign runs (any other root monitor)
by max(class default for their phase, measured cores over the last WINDOW_S).

Reads: ps, top, sysctl vm.swapusage, and the stage/event fields of progress.jsonl.  Writes nothing.  Launches nothing.
Numbers carry their basis: MEASURED (2026-10-19 step-2 R2 runs, sched_s45_c2/measured/), DERIVED, ASSUMED.
Importing this module does nothing.
"""
import json
import math
import re
import subprocess
import time
from pathlib import Path

MODULE_NAME = 'machine_gate_s45_c2v001'

PARAMS = {
    'n_cores': 18,                      # MEASURED hw.ncpu
    'mem_total_bytes': 137438953472,    # MEASURED hw.memsize
    'core_limit': 24.0,                 # DERIVED: owned after-route-A weights are upper bounds (2 vs MEASURED 0.9-1.0),
                                        #   so at the limit the mean busy cores stay <= ~1.25 x 18
    'route_a_cap': 4,                   # DERIVED (memory, not cores): with the MEASURED 11.8 GB steady + 18.7 GB transfer
                                        #   spikes, 6 pooled calls in route A reach a simulated 127 GB (expected) and 141 GB
                                        #   (32-iteration) total footprint; 4 keep it at 85-104 / 88-118 GB, and cost 0-9 %
                                        #   of the expected campaign (SIM_S45_C2V001.json VARIANT rows).  MEASURED: the
                                        #   compressor grew 13 -> 60 GB when the run footprint reached 77-83 GB.  Cores:
                                        #   4 x 3.25 = 13 mean busy cores leave room for after-route-A calls
    'w_route_a_8': 3.25,                # MEASURED mean busy cores of one 8-worker route A while iterating (max 8.0)
    'w_serial': 1.0,                    # MEASURED serial route A / setup / post-loop / reference stage: 0.9-1.0
    'w_after_default': 1.0,             # MEASURED foreign after-route-A floor (reference stage 0.9-1.0)
    'mem_limit_gb': 100.0,              # DERIVED: 137.4 GB physical - ~37 GB for the system, compressor and other lanes
                                        #   (MEASURED: an 83.2 GB run-footprint coincidence ran with swap flat at 1.8 GB)
    'res_route_a_gb': 11.0,             # MEASURED: K128 tail-ON 8-worker route-A steady footprint, median 9.7-9.9 GB,
                                        #   max 10.1-11.8 GB outside transfer windows (C4T, S4T, C4T_A)
    'res_after_gb': 4.4,                # DERIVED: the after-route-A tail-ON model 4.095 GiB (LAUNCH_ORDER 6.1);
                                        #   MEASURED reference stage 0.6-1.6 GB (later route-B stages not yet measured)
    'spike_headroom_gb': 20.0,          # MEASURED: per-iteration TailState transfer increment +16.8 to +19.9 GB above
                                        #   steady (15 s and 2.8 s sampling, C4T_A, C3T; peak 30.5 GB), lasting 37-41 s;
                                        #   30-40 s sampling had read 12.8 GB
    'swap_stop_gb': 8.0,                # the A130 watch alert level (memory_watch_root_c2v002.sh L22)
    'spacing_s': 120.0,                 # DERIVED: same-class calls reach their first transfer spike at ~ the same age
    'warmup_s': 60.0,
    'window_s': 60.0,
    'sample_min_interval_s': 10.0,
    'ps_to_footprint_max': 1.27,        # MEASURED ps tree RSS / top MEM ratio 0.94-1.27 (KHI_R2_FOOTPRINT_V001.csv)
    'pooled_min_procs': 4,              # a tree with >= 4 processes in route A is a worker pool (DDO 8-worker: 11)
}
MONITOR_PATTERN = re.compile(r'root_monitor_c2v\d+\.py')
PS = ['/bin/ps', '-A', '-o', 'pid=,ppid=,pgid=,etime=,time=,rss=,command=']
TOP = '/usr/bin/top'
SYSCTL = '/usr/sbin/sysctl'
REASONS = ('COUNT_MAX_CONCURRENT', 'ROUTE_A_CAP', 'CORE_LIMIT', 'MEMORY_LIMIT', 'SWAP_STOP', 'SPACING', 'WARMUP',
           'PROBE_FAILED')


# --------------------------------------------------------------------------------------------- call classes
def make_class(name, *, pooled, w_route_a, w_after, res_route_a_gb, res_after_gb):
    return {'name': name, 'pooled': bool(pooled), 'w_route_a': float(w_route_a), 'w_after': float(w_after),
            'res_route_a_gb': float(res_route_a_gb), 'res_after_gb': float(res_after_gb)}


def class_from_numerics(numerics, admitted_route_a=False, params=PARAMS, name='DDO_SPEC'):
    """Gate class of one driver call from its numerics (the same fields campaign_c2v005.spec_weights reads).
    Route-A weight: MEASURED 3.25 mean busy cores for 8 workers, 1.0 for a serial route A; other worker counts are
    scaled linearly between those two (DERIVED).  After route A: numerics.column_workers (an upper bound: MEASURED
    0.9-1.0 busy cores in the reference stage)."""
    num = numerics or {}
    cw = num.get('column_workers', 1)
    ra = (num.get('route_a') or {}).get('column_workers', 1)
    if type(cw) is not int or cw < 1 or type(ra) is not int or ra < 1:
        raise ValueError('numerics.column_workers / numerics.route_a.column_workers must be positive ints')
    w_ra = max(params['w_serial'], params['w_route_a_8'] * ra / 8.0)
    if admitted_route_a:
        w_ra = float(cw)
    return make_class(name, pooled=(ra > 1 and not admitted_route_a), w_route_a=w_ra, w_after=float(cw),
                      res_route_a_gb=params['res_route_a_gb'], res_after_gb=params['res_after_gb'])


def class_from_spec_bytes(raw, params=PARAMS):
    spec = json.loads(raw)
    admitted = (spec.get('admit') or {}).get('route_a') is not None
    return class_from_numerics(spec.get('numerics'), admitted_route_a=admitted, params=params)


# --------------------------------------------------------------------------------------------- parsers
def parse_cputime(s):
    """ps 'time' column -> seconds.  Forms: 'M:SS.ss', 'MMM:SS.ss', 'H:MM:SS.ss', 'D-HH:MM:SS'."""
    s = s.strip()
    days = 0
    if '-' in s:
        d, s = s.split('-', 1)
        days = int(d)
    parts = [float(p) for p in s.split(':')]
    sec = 0.0
    for p in parts:
        sec = sec * 60.0 + p
    return days * 86400.0 + sec


def parse_etime(s):
    """ps 'etime' column -> seconds.  Forms: 'MM:SS', 'HH:MM:SS', 'D-HH:MM:SS'."""
    return parse_cputime(s)


_MEM_RE = re.compile(r'^\s*(\d+)\s+([0-9.]+)([BKMGT])[+-]?\s*$')
_MEM_UNIT = {'B': 1.0, 'K': 1024.0, 'M': 1024.0 ** 2, 'G': 1024.0 ** 3, 'T': 1024.0 ** 4}


def parse_top_mem(text):
    """`top -l 1 -stats pid,mem -pid ...` output -> {pid: bytes}."""
    out = {}
    for ln in text.splitlines():
        m = _MEM_RE.match(ln)
        if m:
            out[int(m.group(1))] = float(m.group(2)) * _MEM_UNIT[m.group(3)]
    return out


def parse_swap_used_gb(text):
    """`sysctl -n vm.swapusage` -> used, in GB (1e9 B), as memory_watch_root_c2v002 reports it (MiB/1024)."""
    m = re.search(r'used\s*=\s*([0-9.]+)([MGK])', text)
    if not m:
        raise ValueError('swap usage unparseable')
    v, u = float(m.group(1)), m.group(2)
    return {'K': v / 1024.0 / 1024.0, 'M': v / 1024.0, 'G': v}[u]


_OUTDIR_RE = re.compile(r'--outdir (.+?) --(?:receipt|wall-cap-s|rss-cap-bytes|output-cap-bytes|poll-s|python|spec)\b')


def parse_outdir(command):
    m = _OUTDIR_RE.search(command)
    return m.group(1) if m else None


def parse_ps(text):
    procs = {}
    for ln in text.splitlines():
        f = ln.split(None, 6)
        if len(f) < 7:
            continue
        try:
            pid, ppid, pgid = int(f[0]), int(f[1]), int(f[2])
            procs[pid] = {'pid': pid, 'ppid': ppid, 'pgid': pgid, 'etime_s': parse_etime(f[3]),
                          'cpu_s': parse_cputime(f[4]), 'rss_bytes': int(f[5]) * 1024, 'command': f[6]}
        except ValueError:
            continue
    return procs


# --------------------------------------------------------------------------------------------- phase
def route_a_done_path(progress_path):
    """campaign_c2v005.route_a_done, on an explicit progress.jsonl path (stage/event fields only)."""
    try:
        raw = Path(progress_path).read_bytes()
    except OSError:
        return False
    for ln in raw.split(b'\n'):
        if not ln.strip():
            continue
        try:
            d = json.loads(ln.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            continue
        st, ev = d.get('stage'), d.get('event')
        if st == 'route_a' and ev == 'finished':
            return True
        if isinstance(st, str) and st != 'route_a' and ev == 'started':
            return True
    return False


# --------------------------------------------------------------------------------------------- probe
def probe(run=subprocess.run, params=PARAMS):
    """One read-only snapshot of the machine: every root-monitor run tree, its process group, CPU times, footprint,
    plus swap used.  -> {'ok', 'reasons', 'runs': [...], 'swap_gb', 'procs_cpu': {pid: cpu_s}}."""
    snap = {'ok': True, 'reasons': [], 'runs': [], 'swap_gb': None, 'procs_cpu': {}, 'footprint_source': 'top'}
    try:
        r = run(PS, capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise OSError('ps exit %d' % r.returncode)
        procs = parse_ps(r.stdout)
    except Exception as exc:                                    # noqa: BLE001 -- fail closed
        snap['ok'] = False
        snap['reasons'].append('ps: %s: %s' % (type(exc).__name__, exc))
        return snap
    try:
        snap['swap_gb'] = parse_swap_used_gb(run([SYSCTL, '-n', 'vm.swapusage'], capture_output=True, text=True,
                                                 timeout=10).stdout)
    except Exception as exc:                                    # noqa: BLE001
        snap['ok'] = False
        snap['reasons'].append('swap: %s: %s' % (type(exc).__name__, exc))
    children = {}
    for p in procs.values():
        children.setdefault(p['ppid'], []).append(p['pid'])
    runs = []
    for p in procs.values():
        cmd = p['command']
        if not (MONITOR_PATTERN.search(cmd) and '--driver' in cmd):
            continue
        # the driver child runs in a session (process group) of its own; the monitor's transient `ps` children share
        # the monitor's group and must not be taken for it (a lower recycled pid would otherwise win)
        kids = sorted(k for k in children.get(p['pid'], []) if procs[k]['pgid'] != p['pgid'])
        members = []
        if kids:
            pg = procs[kids[0]]['pgid']
            members = sorted(q['pid'] for q in procs.values() if q['pgid'] == pg)
        runs.append({'monitor_pid': p['pid'], 'age_s': p['etime_s'], 'outdir': parse_outdir(cmd), 'members': members,
                     'nproc': len(members), 'cpu_s': {q: procs[q]['cpu_s'] for q in members},
                     'rss_bytes': sum(procs[q]['rss_bytes'] for q in members)})
    all_members = [q for rr in runs for q in rr['members']]
    mem = {}
    if all_members:
        args = [TOP, '-l', '1', '-stats', 'pid,mem']
        for q in all_members:
            args += ['-pid', str(q)]
        try:
            t = run(args, capture_output=True, text=True, timeout=60)
            mem = parse_top_mem(t.stdout) if t.returncode == 0 else {}
        except Exception:                                       # noqa: BLE001 -- fall back to ps RSS (flagged)
            mem = {}
    for rr in runs:
        got = [mem[q] for q in rr['members'] if q in mem]
        if rr['members'] and len(got) == len(rr['members']):
            rr['footprint_gb'] = sum(got) / 1e9
            rr['footprint_source'] = 'top'
        else:
            rr['footprint_gb'] = rr['rss_bytes'] * params['ps_to_footprint_max'] / 1e9
            rr['footprint_source'] = 'ps_rss_x%.2f' % params['ps_to_footprint_max']
            if rr['members']:
                snap['footprint_source'] = 'mixed'
        snap['procs_cpu'].update(rr['cpu_s'])
    snap['runs'] = runs
    return snap


# --------------------------------------------------------------------------------------------- decision (pure)
def evaluate(*, runs, head, n_running, max_concurrent, swap_gb, since_last_start_s, history_s, probe_ok=True,
             params=PARAMS):
    """Pure admission decision.  runs: list of {'key', 'owned', 'class' (owned only), 'phase' ('route_a'|'after'),
    'footprint_gb' (None if not visible yet), 'cores_measured' (None if unknown), 'nproc'}.  head: a class dict."""
    P = params
    reasons = []
    cores = 0.0
    mem = 0.0
    pooled_ra = 0
    rows = []
    for r in runs:
        ph = r.get('phase') or 'route_a'
        fp = r.get('footprint_gb')
        closed = ph == 'route_a' and bool(r.get('pool_closed'))  # route-A post-loop: its worker pool has exited
        if r.get('owned'):
            c = r['class']
            if closed:                                          # MEASURED post-loop: 0.9-1.0 core, <= 3.8 GB; weighed as
                w, res, pooled = c['w_after'], c['res_after_gb'], False     # after route A, so weights never rise
            else:
                w = c['w_route_a'] if ph == 'route_a' else c['w_after']
                res = c['res_route_a_gb'] if ph == 'route_a' else c['res_after_gb']
                pooled = c['pooled'] and ph == 'route_a'
        else:
            pooled = ph == 'route_a' and not closed and (r.get('nproc') or 0) >= P['pooled_min_procs']
            dflt = P['w_route_a_8'] if pooled else (P['w_serial'] if ph == 'route_a' else P['w_after_default'])
            cm = r.get('cores_measured')
            w = max(dflt, cm) if isinstance(cm, (int, float)) and math.isfinite(cm) else dflt
            res = P['res_route_a_gb'] if (ph == 'route_a' and not closed) else P['res_after_gb']
        m = max(fp, res) if isinstance(fp, (int, float)) else res
        cores += w
        mem += m
        pooled_ra += 1 if pooled else 0
        rows.append({'key': r.get('key'), 'owned': bool(r.get('owned')), 'phase': 'route_a_post_loop' if closed else ph,
                     'cores': round(w, 3), 'mem_gb': round(m, 2), 'pooled_route_a': pooled})
    head_pooled = bool(head['pooled'])
    cores_after = cores + head['w_route_a']
    mem_after = mem + head['res_route_a_gb'] + P['spike_headroom_gb']
    if not probe_ok:
        reasons.append('PROBE_FAILED')
    if n_running >= max_concurrent:
        reasons.append('COUNT_MAX_CONCURRENT')
    if head_pooled and pooled_ra + 1 > P['route_a_cap']:
        reasons.append('ROUTE_A_CAP')
    if cores_after > P['core_limit'] + 1e-9:
        reasons.append('CORE_LIMIT')
    if mem_after > P['mem_limit_gb'] + 1e-9:
        reasons.append('MEMORY_LIMIT')
    if swap_gb is None or swap_gb > P['swap_stop_gb']:
        reasons.append('SWAP_STOP')
    if since_last_start_s is not None and since_last_start_s < P['spacing_s']:
        reasons.append('SPACING')
    if history_s < P['warmup_s']:
        reasons.append('WARMUP')
    return {'admit': not reasons, 'reasons': reasons, 'cores_now': round(cores, 3), 'cores_after_admit': round(cores_after, 3),
            'mem_now_gb': round(mem, 2), 'mem_after_admit_gb': round(mem_after, 2), 'pooled_route_a_now': pooled_ra,
            'swap_gb': swap_gb, 'since_last_start_s': since_last_start_s, 'runs': rows, 'head': head['name']}


# --------------------------------------------------------------------------------------------- stateful gate
class Gate:
    """Sampling wrapper around evaluate().  probe_fn and clock are injectable for synthetic tests only."""

    def __init__(self, params=None, probe_fn=None, clock=time.monotonic):
        self.P = dict(PARAMS)
        if params:
            self.P.update(params)
        self.probe_fn = probe_fn or (lambda: probe(params=self.P))
        self.clock = clock
        self.hist = []                  # [(t, {pid: cpu_s})]
        self.last = None
        self.last_t = None
        self.t_first = None
        self.n_probes = 0
        self.max_nproc = {}             # monitor pid -> largest process count seen (pool opened)

    def sample(self, force=False):
        now = self.clock()
        if not force and self.last is not None and now - self.last_t < self.P['sample_min_interval_s']:
            return self.last
        snap = self.probe_fn()
        self.n_probes += 1
        self.last, self.last_t = snap, now
        if snap.get('ok'):
            if self.t_first is None:
                self.t_first = now
            self.hist.append((now, dict(snap.get('procs_cpu') or {})))
            keep = self.P['window_s'] * 3
            self.hist = [h for h in self.hist if now - h[0] <= keep] or self.hist[-1:]
            live = set()
            for r in snap.get('runs') or []:
                mp = r['monitor_pid']
                live.add(mp)
                self.max_nproc[mp] = max(self.max_nproc.get(mp, 0), r['nproc'])
            self.max_nproc = {k: v for k, v in self.max_nproc.items() if k in live}
        return snap

    def pool_closed(self, run):
        """True when this run tree once had a worker pool (>= pooled_min_procs processes) and no longer has one."""
        n = self.P['pooled_min_procs']
        return self.max_nproc.get(run['monitor_pid'], 0) >= n and run['nproc'] < n

    def history_s(self):
        if self.t_first is None:
            return 0.0
        return self.clock() - self.t_first

    def cores_measured(self, run):
        """Busy cores of one run tree over >= window_s (None when the history is shorter)."""
        if not self.hist:
            return None
        t_now, cpu_now = self.hist[-1]
        old = [h for h in self.hist if t_now - h[0] >= self.P['window_s']]
        if not old:
            return None
        t_old, cpu_old = old[-1]
        dt = t_now - t_old
        if dt <= 0:
            return None
        tot = 0.0
        for pid in run['members']:
            if pid in cpu_now:
                tot += max(0.0, cpu_now[pid] - cpu_old.get(pid, 0.0))
        return tot / dt

    def decide(self, *, owned, head, n_running, max_concurrent, last_own_start=None):
        """owned: {monitor_pid: {'class': cls, 'progress': path}} for the calls this launcher runs.
        last_own_start: clock() time of this launcher's last start (None if none)."""
        snap = self.sample()
        now = self.clock()
        runs = []
        seen = set()
        for r in snap.get('runs') or []:
            mp = r['monitor_pid']
            o = owned.get(mp)
            if o is not None:
                ph = 'after' if route_a_done_path(o['progress']) else 'route_a'
                runs.append({'key': mp, 'owned': True, 'class': o['class'], 'phase': ph, 'pool_closed': self.pool_closed(r),
                             'footprint_gb': r.get('footprint_gb'), 'nproc': r['nproc']})
                seen.add(mp)
            else:
                ph = 'after' if (r.get('outdir') and route_a_done_path(Path(r['outdir']) / 'progress.jsonl')) else 'route_a'
                runs.append({'key': mp, 'owned': False, 'phase': ph, 'pool_closed': self.pool_closed(r),
                             'footprint_gb': r.get('footprint_gb'), 'cores_measured': self.cores_measured(r),
                             'nproc': r['nproc']})
        for mp, o in owned.items():                         # owned but not (yet / any more) visible in ps
            if mp not in seen:
                ph = 'after' if route_a_done_path(o['progress']) else 'route_a'
                runs.append({'key': mp, 'owned': True, 'class': o['class'], 'phase': ph, 'footprint_gb': None, 'nproc': 0})
        ages = [r['age_s'] for r in (snap.get('runs') or [])]
        since = min(ages) if ages else None
        if last_own_start is not None:
            own = now - last_own_start
            since = own if since is None else min(since, own)
        d = evaluate(runs=runs, head=head, n_running=n_running, max_concurrent=max_concurrent,
                     swap_gb=snap.get('swap_gb'), since_last_start_s=since, history_s=self.history_s(),
                     probe_ok=bool(snap.get('ok')), params=self.P)
        d['probe_reasons'] = list(snap.get('reasons') or [])
        d['footprint_source'] = snap.get('footprint_source')
        return d


def describe():
    return {'module': MODULE_NAME, 'params': dict(PARAMS), 'monitor_pattern': MONITOR_PATTERN.pattern,
            'reasons': list(REASONS)}
