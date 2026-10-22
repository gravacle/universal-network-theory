"""Shared machine admission gate for step-4 / step-5 launches (Claude2 sched_s45_c2, c2v003).

c2v003 = machine_gate_s45_c2v002 (6e8f2159) with two changes only, ruled in A140 (0706) on Claude4's review 0192:
  * N1, foreign run trees classed by driver.  A foreign tree whose monitor command line carries --driver-sha256 of the
    NGC driver cx3r008 (577f8c94) is no longer the generic class (route-A reservation 11 GB + one 20 GB spike, pooled
    with 5.79 GB growth when it has >= 4 processes or is young):
      NGC_SERIAL  spec numerics.route_a.column_workers 1: reservation 6.0 GB + spike 16.4 GB in route A (res + spike
                  22.4 GB >= Claude4 RI45-12 corrected U peak 20.11 GB; E 7.73 GB; steady 3.12-3.72 GB), 10.0 GB after
                  route A, serial (not pooled), 1.0 busy core in route A (the ngc_admission wave-1 class);
      NGC_TWIN    column_workers > 1 (the cw8 identity twin): reservation 11.0 GB + spike 50.3 GB = Claude4's U transfer
                  peak 61.3 GB (E 45.2 GB), pooled, 3.25 busy cores;
      NGC_UNIDENTIFIED  the NGC driver but the spec leaf unreadable: sized as the twin (fail closed).
    The spec leaf is read once per tree (numerics.route_a.column_workers only, the cx3r008 default 1 when absent).  Every
    other driver keeps the v002 generic class unchanged.  The class sizes are checked against Claude4's U peaks
    (check_foreign_classes): an undersized NGC class refuses at Gate() construction.
  * N2, the twin hold.  While a twin is in route A (its planned stop is the 22,752 s wall cap), every head of family DDO
    (the campaign's calls) is refused with TWIN_HOLD; NGC_SERIAL heads are not held (memory decides).  twin_hold() and
    the read-only CLI `--hold-check` are the predicate root uses to hold direct batches (the packet does not read this
    gate).  twin_start_check() / `--twin-start-check` is step5_path L146 as a gate rule: the twin head passes the memory
    rule and no DDO route-A call (an owned DDO-family run or a generic foreign run, in route A and not post-loop) and no
    other twin is in flight.  An NGC_UNIDENTIFIED tree holds only while younger than the twin wall cap + 600 s.
Nothing else changes: limits, reservations, spikes, growth, route-A cap, cores, swap, spacing, warm-up, probe and phase
rules are c2v002's, and a machine with no cx3r008 tree decides exactly as c2v002 (SIM_S45_C2V003 regression rows).

c2v002 = machine_gate_s45_c2v001 (6d0c45f8) with the memory check (d) replaced, after verifier 2's blocking item B1
(route-A cap 4 / 100 GB was not memory-safe once spike phases drift: random-phase replay of the v001 rule, SIM_S45_C2V002
'V001_gate_cap4_100GB_one_spike' rows, peaks 130-168 GB):
  * two limits instead of a fixed 100 GB, both MEASURED on this machine (watch CSV, 2026-10-19):
      knee = 72 GB  the largest run footprint seen with the compressor flat (08:42:39Z, 72.0 GB, compressor 16.2 GB);
                    compression began at 76.7 GB (08:18:41Z, compressor 13.0 -> 45.6 GB);
      hard = 83 GB  the largest run footprint seen (08:19:19Z, 83.2 GB); swap stayed flat at 1.8 GB;
    both lowered live when other memory use grows: pool = sum of live run-tree footprints + vm_stat free + file-backed
    pages; knee_eff = min(knee, pool - POOL_MARGIN_GB); hard_eff = min(hard, knee_eff + (hard - knee));
  * simultaneous spikes are counted and growth is reserved.  Each class carries spike_gb (its largest transient above
    its route-A reservation: DDO pooled 20 GB transfer spike, NGC serial 16.4 GB state build) and growth_gb (steady growth a
    pooled call may still add: VF_GB_PER_ITER x (max_iterations - 6) = 5.79 GB at 32 iterations).
      d1 MEMORY_HARD  counted + head reservation + the SPIKE_COUNT_CAP (2) largest spikes among route-A calls and the
                      head + the growth of pooled route-A calls and a pooled head <= hard_eff;
      d2 MEMORY_KNEE  counted + head reservation + the largest single spike <= knee_eff;
    counted = sum over run trees of max(live footprint, phase reservation);
  * the after-route-A reservation is set from measurement: 3.5 GB (MEASURED K128 post-loop max 3.5 GB, after route A max
    2.7 GB; v001 used the 4.4 GB model);
  * a foreign run tree in route A younger than SETUP_MAX_S without a worker pool yet is counted as pooled (verifier 2
    note 10), and any foreign route-A tree carries one 20 GB spike;
  * ROUTE_A_CAP 2: the parameter set selected by SIM_S45_C2V002 against criteria declared before the runs (time above
    83 GB <= 0.1 %, peak < 110 GB, time above 72 GB <= 2 % in every seed of the expected and all-32-iteration rows).
Everything else (a-c, e-h, the probe, phase rule, post-loop rule, owned / foreign weights) is c2v001's.

The head of the queue starts only when ALL of these hold (FIFO: the head is never skipped):
  a. count     fewer than max_concurrent calls of this launcher run (the launcher's own wave wall cap stays its own);
  b. route-A   at most ROUTE_A_CAP pooled (parallel-worker) calls in route A machine-wide, the head included;
  c. cores     sum of busy-core weights of every run tree + the head's route-A weight <= CORE_LIMIT;
  d1/d2 memory (above);
  e. swap      swap used <= SWAP_STOP_GB;
  f. spacing   >= SPACING_S since the youngest root monitor on the machine (any launcher) and since this launcher's
               own last start;
  g. warm-up   the CPU sampler holds >= WARMUP_S of history (foreign runs are weighed by measured cores);
  h. probe     ps, swap and vm_stat could be read (fail closed);
  i. twin hold (c2v003) a head of family DDO waits while twin_hold() holds.
A run tree = one root monitor process (argv matches MONITOR_PATTERN and carries --driver) plus the process group of its
driver child (the A130 metric of memory_watch_root_c2v002.sh).  Live footprint = sum of top MEM over that process group
(fallback: ps RSS x PS_TO_FOOTPRINT_MAX, flagged).  Phase = the driver's own <outdir>/progress.jsonl (route_a finished,
or any later stage started -> after route A), exactly the rule of campaign_c2v005.route_a_done; unreadable -> route A.
Route-A post-loop: a tree that once held a worker pool (>= POOLED_MIN_PROCS processes) and no longer does is still in
route A (the driver has not logged route_a finished) but no longer pooled; it is weighed and reserved as after route A.

Reads: ps, top, sysctl vm.swapusage, vm_stat, the stage/event fields of progress.jsonl, and (c2v003) the
numerics.route_a.column_workers leaf of the spec named on the command line of a cx3r008 tree.  Writes nothing.
Launches nothing.  memory_pressure is never read.  Numbers carry their basis: MEASURED (2026-10-19 step-2 R2 runs,
sched_s45_c2/measured/ and sched_s45_c2/v002/measured/), DERIVED, ASSUMED, FORMAL.
Importing this module does nothing.  CLI (read-only):  machine_gate_s45_c2v003.py --hold-check | --twin-start-check
"""
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

MODULE_NAME = 'machine_gate_s45_c2v003'

PARAMS = {
    'n_cores': 18,                      # MEASURED hw.ncpu
    'mem_total_bytes': 137438953472,    # MEASURED hw.memsize
    'core_limit': 24.0,                 # DERIVED: owned after-route-A weights are upper bounds (2 vs MEASURED 0.9-1.0),
                                        #   so at the limit the mean busy cores stay <= ~1.25 x 18
    'route_a_cap': 2,                   # SIM_S45_C2V002 variant selection (V6): cap 3 never binds under d1 (V7 = V6), cap
                                        #   3 without the growth reserve reaches 113.7 GB (V2)
    'w_route_a_8': 3.25,                # MEASURED mean busy cores of one 8-worker route A while iterating (max 8.0)
    'w_serial': 1.0,                    # MEASURED serial route A / setup / post-loop / reference stage: 0.9-1.0
    'w_after_default': 1.0,             # MEASURED foreign after-route-A floor (reference stage 0.9-1.0)
    'knee_static_gb': 72.0,             # MEASURED: largest watch run footprint with the compressor flat (08:42:39Z 72.0 GB,
                                        #   compressor 16.2 GB); compression began at 76.7 GB (08:18:41Z: 13.0 -> 45.6 GB)
    'hard_static_gb': 83.0,             # MEASURED: largest watch run footprint, 83.2 GB (08:19:19Z), swap flat at 1.8 GB
    'pool_margin_gb': 2.0,              # ASSUMED: kept free below the live pool (free + file-backed + run footprints)
    'res_route_a_gb': 11.0,             # MEASURED: K128 tail-ON 8-worker route-A steady footprint, median 9.5-9.8 GB,
                                        #   max 10.1-11.8 GB outside transfer windows (C4T, S4T, C4T_A)
    'res_after_gb': 3.5,                # MEASURED: K128 post-loop max 3.5 GB (C4T_A), after route A max 2.7 GB (C4T; D5
                                        #   through 05_offset and 06/07 fs_columns 1.5 GB); refresh 2026-10-19T11:00Z
    'spike_headroom_gb': 20.0,          # MEASURED per transfer spike: +16.8 to +18.6 GB above steady at 2.8 s sampling
                                        #   (37-41 s long), +20.6 GB the largest K128 watch increment (S4T)
    'spike_count_cap': 2,               # d1 reserves the 2 largest spikes of the route-A calls + head (SIM_S45_C2V002 V6)
    'growth_reserve': True,             # d1 reserves the steady growth pooled route-A calls may still add: without it every
                                        #   variant exceeds 83 GB > 0.1 % of the all-32-iteration rows (V1, V2)
    'vf_gb_per_iter': 0.2228,           # DERIVED u4 (32 x 51,200 x 136 B): K128 tail-ON route-A growth per iteration
    'growth_free_iters': 6,             # MEASURED: K128 steady footprint flat over the 6-8 iterations seen
    'foreign_spike_gb': 20.0,           # a foreign route-A tree of unknown class: one transfer spike (conservative)
    'foreign_growth_gb': 5.79,          # a foreign pooled route-A tree: 0.2228 x (32 - 6) (spec maximum, conservative)
    'swap_stop_gb': 8.0,                # the A130 watch alert level (memory_watch_root_c2v002.sh L22)
    'spacing_s': 120.0,                 # DERIVED: same-class calls reach their first transfer spike at ~ the same age
    'warmup_s': 60.0,
    'window_s': 60.0,
    'sample_min_interval_s': 10.0,
    'ps_to_footprint_max': 1.27,        # MEASURED ps tree RSS / top MEM ratio 0.94-1.27 (KHI_R2_FOOTPRINT_V001.csv)
    'pooled_min_procs': 4,              # a tree with >= 4 processes in route A is a worker pool (DDO 8-worker: 11)
    'setup_max_s': 1500.0,              # MEASURED longest setup before the first pool: 1293 s (KHI); a younger foreign
                                        #   route-A tree without a pool yet is counted as pooled
    # ---- c2v003 (A140 N1 / N2): foreign trees classed by driver; the cw8 twin hold
    'ngc_driver_sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377',
                                        # FORMAL: POLICY_C2V001 drivers.cx3r008 (step5_path_c2), the only NGC driver
    'ngc_serial_class': {'w_route_a': 1.0, 'w_after': 2.0, 'res_route_a_gb': 6.0, 'spike_gb': 16.4, 'res_after_gb': 10.0},
                                        # DERIVED (Claude4 RI45-12 V002 e686637e, = ngc_admission wave-1 class): steady
                                        #   E 3.12 / U 3.72 GB, readout 4.5-5.2 GB -> 6.0; peak E 7.73, U 14.06-20.11 GB
                                        #   -> spike 20.11 - 3.72 = 16.4; route-B pairs <= 10.0 GB; serial route A 1 core
    'ngc_twin_class': {'w_route_a': 3.25, 'w_after': 2.0, 'res_route_a_gb': 11.0, 'spike_gb': 50.3, 'res_after_gb': 10.0},
                                        # DERIVED: Claude4 cw8 transfer peak E 45.2 / U 61.3 GB = 11.0 (the 8-worker
                                        #   route-A reservation, MEASURED on DDO, ASSUMED here) + 50.3; 3.25 cores as DDO 8w
    'ngc_serial_peak_floor_gb': 20.11,  # Claude4 RI45-12 V002 serial peak_footprint_GB.U_with_DDO_excess
    'ngc_serial_steady_floor_gb': 3.72, # Claude4 RI45-12 V002 serial steady_footprint_GB.U
    'ngc_twin_peak_floor_gb': 61.3,     # Claude4 RI45-12 V002 column_workers_8.transfer_peak_GB.U
    'twin_wall_cap_s': 22752.0,         # FORMAL: CAPS_FIRST_NGC_POINT_C2V001 identity_twin.wall_cap_s (2 x U 3.16 h)
    'twin_hold_grace_s': 600.0,         # ASSUMED: an unidentified cx3r008 tree holds until twin wall cap + 600 s
    'spec_read_max_bytes': 16777216,    # a spec larger than 16 MiB is not read (unidentified)
}
MONITOR_PATTERN = re.compile(r'root_monitor_c2v\d+\.py')
FOREIGN_KINDS = ('GENERIC', 'NGC_SERIAL', 'NGC_TWIN', 'NGC_UNIDENTIFIED')
HELD_FAMILIES = ('DDO',)                # A140 N2: heads of these families wait while a twin is in route A
PS = ['/bin/ps', '-A', '-o', 'pid=,ppid=,pgid=,etime=,time=,rss=,command=']
TOP = '/usr/bin/top'
SYSCTL = '/usr/sbin/sysctl'
VM_STAT = '/usr/bin/vm_stat'
REASONS = ('COUNT_MAX_CONCURRENT', 'ROUTE_A_CAP', 'CORE_LIMIT', 'MEMORY_HARD', 'MEMORY_KNEE', 'SWAP_STOP', 'SPACING', 'WARMUP',
           'PROBE_FAILED', 'TWIN_HOLD', 'DDO_ROUTE_A_IN_FLIGHT', 'TWIN_ALREADY_RUNNING')


# --------------------------------------------------------------------------------------------- call classes
def make_class(name, *, pooled, w_route_a, w_after, res_route_a_gb, res_after_gb, spike_gb=None, growth_gb=0.0, params=PARAMS,
               family='DDO'):
    """spike_gb: the call's largest transient above its route-A reservation (default: the transfer spike for a pooled
    call, 0 for a serial DDO call).  growth_gb: steady growth it may still add in route A after admission.
    family (c2v003): 'DDO' (held while a twin is in route A), 'NGC_SERIAL' or 'NGC_TWIN'."""
    if spike_gb is None:
        spike_gb = params['spike_headroom_gb'] if pooled else 0.0
    return {'name': name, 'pooled': bool(pooled), 'w_route_a': float(w_route_a), 'w_after': float(w_after),
            'res_route_a_gb': float(res_route_a_gb), 'res_after_gb': float(res_after_gb), 'spike_gb': float(spike_gb),
            'growth_gb': float(growth_gb), 'family': str(family)}


def foreign_class(kind, params=PARAMS):
    """c2v003 (A140 N1): the gate class of a foreign cx3r008 tree.  NGC_UNIDENTIFIED is sized as the twin (fail closed)."""
    if kind == 'NGC_SERIAL':
        c = params['ngc_serial_class']
        return make_class('FOREIGN_NGC_K32_SERIAL', pooled=False, w_route_a=c['w_route_a'], w_after=c['w_after'],
                          res_route_a_gb=c['res_route_a_gb'], res_after_gb=c['res_after_gb'], spike_gb=c['spike_gb'],
                          growth_gb=0.0, params=params, family='NGC_SERIAL')
    if kind in ('NGC_TWIN', 'NGC_UNIDENTIFIED'):
        c = params['ngc_twin_class']
        return make_class('FOREIGN_NGC_K32_CW8_TWIN' if kind == 'NGC_TWIN' else 'FOREIGN_NGC_UNIDENTIFIED_AS_TWIN',
                          pooled=True, w_route_a=c['w_route_a'], w_after=c['w_after'], res_route_a_gb=c['res_route_a_gb'],
                          res_after_gb=c['res_after_gb'], spike_gb=c['spike_gb'], growth_gb=0.0, params=params,
                          family='NGC_TWIN')
    raise ValueError('no foreign class for kind %r' % (kind,))


def check_foreign_classes(params=PARAMS):
    """c2v003 (A140 N1 sizing): raises ValueError when an NGC class reserves less than Claude4's RI45-12 U figures:
    serial reservation + spike >= the U peak 20.11 GB and reservation >= the U steady 3.72 GB; twin reservation + spike
    >= the U transfer peak 61.3 GB.  The v002 generic sizing of the twin (11 + 20 + 5.79 = 36.8 GB) fails this check."""
    P = params
    s, t = P['ngc_serial_class'], P['ngc_twin_class']
    for nm, c in (('ngc_serial_class', s), ('ngc_twin_class', t)):
        for k in ('w_route_a', 'w_after', 'res_route_a_gb', 'spike_gb', 'res_after_gb'):
            v = c.get(k)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
                raise ValueError('%s.%s must be a finite number >= 0' % (nm, k))
    if s['res_route_a_gb'] + s['spike_gb'] < P['ngc_serial_peak_floor_gb'] - 1e-9:
        raise ValueError('NGC serial class %.2f GB < the RI45-12 U peak %.2f GB' % (s['res_route_a_gb'] + s['spike_gb'],
                                                                               P['ngc_serial_peak_floor_gb']))
    if s['res_route_a_gb'] < P['ngc_serial_steady_floor_gb'] - 1e-9:
        raise ValueError('NGC serial reservation %.2f GB < the RI45-12 U steady %.2f GB' % (s['res_route_a_gb'],
                                                                                       P['ngc_serial_steady_floor_gb']))
    if t['res_route_a_gb'] + t['spike_gb'] < P['ngc_twin_peak_floor_gb'] - 1e-9:
        raise ValueError('NGC twin class %.2f GB < the RI45-12 cw8 U transfer peak %.2f GB' % (
            t['res_route_a_gb'] + t['spike_gb'], P['ngc_twin_peak_floor_gb']))
    return True


def classify_foreign(driver_sha256, spec_route_a_workers, params=PARAMS):
    """c2v003 (A140 N1): the class kind of a foreign run tree from its monitor's --driver-sha256 and its spec leaf."""
    if driver_sha256 != params['ngc_driver_sha256']:
        return 'GENERIC'
    w = spec_route_a_workers
    if type(w) is int and w == 1:
        return 'NGC_SERIAL'
    if type(w) is int and w > 1:
        return 'NGC_TWIN'
    return 'NGC_UNIDENTIFIED'


def read_spec_route_a_workers(path, params=PARAMS):
    """numerics.route_a.column_workers of the spec named on a cx3r008 monitor's command line (1 when route_a or the leaf
    is absent: the cx3r008 driver default, step5_path D05).  None when the path is not absolute, the file is unreadable,
    larger than spec_read_max_bytes, not JSON, or the leaf is not a positive int.  Only that leaf is used."""
    try:
        p = Path(path)
        if not p.is_absolute():
            return None
        lim = int(params['spec_read_max_bytes'])
        with open(p, 'rb') as f:
            raw = f.read(lim + 1)
        if len(raw) > lim:
            return None
        spec = json.loads(raw)
        num = spec.get('numerics')
        if not isinstance(num, dict):
            return None
        ra = num.get('route_a')
        if ra is None:
            ra = {}
        if not isinstance(ra, dict):
            return None
        w = ra.get('column_workers', 1)
        return w if (type(w) is int and w >= 1) else None
    except (OSError, ValueError, TypeError, AttributeError):
        return None


def class_from_numerics(numerics, admitted_route_a=False, params=PARAMS, name='DDO_SPEC'):
    """Gate class of one driver call from its numerics (the same fields campaign_c2v005.spec_weights reads).
    Route-A weight: MEASURED 3.25 mean busy cores for 8 workers, 1.0 for a serial route A; other worker counts are
    scaled linearly between those two (DERIVED).  After route A: numerics.column_workers (an upper bound: MEASURED
    0.9-1.0 busy cores in the reference stage).  Growth (pooled calls): VF_GB_PER_ITER x (route_a.max_iterations -
    GROWTH_FREE_ITERS), route_a.max_iterations absent -> 32 (the spec maximum)."""
    num = numerics or {}
    cw = num.get('column_workers', 1)
    ra_num = num.get('route_a') or {}
    ra = ra_num.get('column_workers', 1)
    mi = ra_num.get('max_iterations', 32)
    if type(cw) is not int or cw < 1 or type(ra) is not int or ra < 1 or type(mi) is not int or mi < 1:
        raise ValueError('numerics.column_workers / numerics.route_a.column_workers / max_iterations must be positive ints')
    w_ra = max(params['w_serial'], params['w_route_a_8'] * ra / 8.0)
    if admitted_route_a:
        w_ra = float(cw)
    pooled = ra > 1 and not admitted_route_a
    growth = params['vf_gb_per_iter'] * max(0, mi - params['growth_free_iters']) if pooled else 0.0
    return make_class(name, pooled=pooled, w_route_a=w_ra, w_after=float(cw), res_route_a_gb=params['res_route_a_gb'],
                      res_after_gb=params['res_after_gb'], growth_gb=growth, params=params)


def class_from_spec_bytes(raw, params=PARAMS):
    spec = json.loads(raw)
    admitted = (spec.get('admit') or {}).get('route_a') is not None
    return class_from_numerics(spec.get('numerics'), admitted_route_a=admitted, params=params)


def never_admissible(cls, params=PARAMS):
    """A reason string when a call of this class could not pass the gate even on an empty machine with the static
    limits (so a launcher refuses up front instead of waiting forever), else None."""
    P = params
    if cls['w_route_a'] > P['core_limit'] + 1e-9:
        return 'route-A weight %.2f > core_limit %.2f' % (cls['w_route_a'], P['core_limit'])
    grow = cls.get('growth_gb', 0.0) if P['growth_reserve'] else 0.0
    one = cls['res_route_a_gb'] + cls.get('spike_gb', 0.0)
    if one > P['knee_static_gb'] + 1e-9 or one + grow > P['hard_static_gb'] + 1e-9:
        return 'route-A reservation %.1f GB + spike %.1f GB (+ growth %.1f GB) > the static memory limits' % (
            cls['res_route_a_gb'], cls.get('spike_gb', 0.0), grow)
    return None


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


_VM_PAGE_RE = re.compile(r'page size of (\d+) bytes')
_VM_ROW_RE = re.compile(r'^\s*"?([A-Za-z][A-Za-z \-]*?)"?:\s+(\d+)\.?\s*$')
_VM_KEYS = {'Pages free': 'free', 'Pages speculative': 'speculative', 'Pages wired down': 'wired',
            'File-backed pages': 'file_backed', 'Anonymous pages': 'anonymous', 'Pages occupied by compressor': 'compressor'}


def parse_vm_stat(text):
    """`vm_stat` output -> GB (1e9 B) for free, speculative, wired, file_backed, anonymous, compressor, and
    pool_free_gb = free + file-backed (file-backed includes the speculative pages: MEASURED active + inactive +
    speculative = anonymous + file-backed).  Raises ValueError when the page size or a required row is missing."""
    m = _VM_PAGE_RE.search(text)
    if not m:
        raise ValueError('vm_stat page size unparseable')
    page = int(m.group(1))
    got = {}
    for ln in text.splitlines():
        r = _VM_ROW_RE.match(ln)
        if r and r.group(1) in _VM_KEYS:
            got[_VM_KEYS[r.group(1)]] = int(r.group(2)) * page / 1e9
    for k in ('free', 'file_backed'):
        if k not in got:
            raise ValueError('vm_stat row missing: %s' % k)
    got['page_size'] = page
    got['pool_free_gb'] = got['free'] + got['file_backed']
    return got


_OUTDIR_RE = re.compile(r'--outdir (.+?) --(?:receipt|wall-cap-s|rss-cap-bytes|output-cap-bytes|poll-s|python|spec)\b')


def parse_outdir(command):
    m = _OUTDIR_RE.search(command)
    return m.group(1) if m else None


_MON_FLAGS = 'driver|driver-sha256|spec|outdir|receipt|wall-cap-s|rss-cap-bytes|output-cap-bytes|poll-s|python'
_DRIVER_SHA_RE = re.compile(r'--driver-sha256 ([0-9a-f]{64})(?=\s|$)')
_SPEC_RE = re.compile(r'--spec (.+?)(?= --(?:%s)(?=\s|$)|$)' % _MON_FLAGS)


def parse_driver_sha256(command):
    """c2v003: the --driver-sha256 value on a root monitor command line (64 lowercase hex), else None."""
    m = _DRIVER_SHA_RE.search(command)
    return m.group(1) if m else None


def parse_spec(command):
    """c2v003: the --spec path on a root monitor command line (spaces allowed), else None."""
    m = _SPEC_RE.search(command)
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
    plus swap used and the vm_stat pool.  -> {'ok', 'reasons', 'runs': [...], 'swap_gb', 'vm', 'pool_free_gb',
    'procs_cpu': {pid: cpu_s}}."""
    snap = {'ok': True, 'reasons': [], 'runs': [], 'swap_gb': None, 'vm': None, 'pool_free_gb': None, 'procs_cpu': {},
            'footprint_source': 'top'}
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
    try:
        v = run([VM_STAT], capture_output=True, text=True, timeout=10)
        if v.returncode != 0:
            raise OSError('vm_stat exit %d' % v.returncode)
        snap['vm'] = parse_vm_stat(v.stdout)
        snap['pool_free_gb'] = snap['vm']['pool_free_gb']
    except Exception as exc:                                    # noqa: BLE001 -- fail closed
        snap['ok'] = False
        snap['reasons'].append('vm_stat: %s: %s' % (type(exc).__name__, exc))
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
                     'rss_bytes': sum(procs[q]['rss_bytes'] for q in members),
                     'driver_sha256': parse_driver_sha256(cmd), 'spec': parse_spec(cmd)})       # c2v003 (N1)
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
def memory_limits(live_runs_gb, pool_free_gb, params=PARAMS):
    """(knee_eff, hard_eff, pool_gb).  pool_free_gb None -> the static limits (pure / simulated callers)."""
    P = params
    knee, hard = P['knee_static_gb'], P['hard_static_gb']
    pool = None
    if pool_free_gb is not None:
        pool = float(live_runs_gb) + float(pool_free_gb)
        knee = min(knee, pool - P['pool_margin_gb'])
        hard = min(hard, knee + (P['hard_static_gb'] - P['knee_static_gb']))
    return knee, hard, pool


def evaluate(*, runs, head, n_running, max_concurrent, swap_gb, since_last_start_s, history_s, probe_ok=True,
             pool_free_gb=None, params=PARAMS):
    """Pure admission decision.  runs: list of {'key', 'owned', 'class' (owned only), 'phase' ('route_a'|'after'),
    'footprint_gb' (None if not visible yet), 'cores_measured' (None if unknown), 'nproc', 'age_s' (foreign)}.
    head: a class dict.  pool_free_gb: vm_stat free + file-backed (None: static limits only).
    Memory: counted = sum over runs of max(live footprint, phase reservation);
      d1 counted + head reservation + the SPIKE_COUNT_CAP largest spikes among route-A runs and the head
         (+ the growth pooled route-A runs and a pooled head may still add, when GROWTH_RESERVE) <= hard_eff;
      d2 counted + head reservation + the largest single spike among route-A runs and the head <= knee_eff."""
    P = params
    reasons = []
    cores = 0.0
    mem = 0.0
    live = 0.0
    pooled_ra = 0
    spikes = [float(head.get('spike_gb', 0.0))]
    growth = float(head.get('growth_gb', 0.0)) if head['pooled'] else 0.0
    rows = []
    for r in runs:
        ph = r.get('phase') or 'route_a'
        fp = r.get('footprint_gb')
        closed = ph == 'route_a' and bool(r.get('pool_closed'))  # route-A post-loop: its worker pool has exited
        sp = gr = 0.0
        if r.get('owned'):
            c = r['class']
            if closed:                                          # MEASURED post-loop: 0.9-1.0 core, <= 3.5 GB; weighed as
                w, res, pooled = c['w_after'], c['res_after_gb'], False     # after route A, so weights never rise
            else:
                w = c['w_route_a'] if ph == 'route_a' else c['w_after']
                res = c['res_route_a_gb'] if ph == 'route_a' else c['res_after_gb']
                pooled = c['pooled'] and ph == 'route_a'
                if ph == 'route_a':
                    sp = float(c.get('spike_gb', 0.0))
                    gr = float(c.get('growth_gb', 0.0)) if pooled else 0.0
        elif (r.get('foreign_kind') or 'GENERIC') != 'GENERIC':  # c2v003 (A140 N1): a cx3r008 tree, classed by driver
            c = foreign_class(r['foreign_kind'], P)
            if closed:
                w, res, pooled = c['w_after'], c['res_after_gb'], False
            else:
                w = c['w_route_a'] if ph == 'route_a' else c['w_after']
                res = c['res_route_a_gb'] if ph == 'route_a' else c['res_after_gb']
                pooled = c['pooled'] and ph == 'route_a'
                if ph == 'route_a':
                    sp = float(c['spike_gb'])
            cm = r.get('cores_measured')
            w = max(w, cm) if isinstance(cm, (int, float)) and math.isfinite(cm) else w
        else:                                                   # every other driver: the v002 generic class, unchanged
            age = r.get('age_s')
            young = isinstance(age, (int, float)) and age < P['setup_max_s']
            pooled = ph == 'route_a' and not closed and ((r.get('nproc') or 0) >= P['pooled_min_procs'] or young)
            dflt = P['w_route_a_8'] if pooled else (P['w_serial'] if ph == 'route_a' else P['w_after_default'])
            cm = r.get('cores_measured')
            w = max(dflt, cm) if isinstance(cm, (int, float)) and math.isfinite(cm) else dflt
            res = P['res_route_a_gb'] if (ph == 'route_a' and not closed) else P['res_after_gb']
            if ph == 'route_a' and not closed:
                sp = P['foreign_spike_gb']
                gr = P['foreign_growth_gb'] if pooled else 0.0
        m = max(fp, res) if isinstance(fp, (int, float)) else res
        if isinstance(fp, (int, float)):
            live += fp
        cores += w
        mem += m
        pooled_ra += 1 if pooled else 0
        if sp > 0:
            spikes.append(sp)
        growth += gr
        rows.append({'key': r.get('key'), 'owned': bool(r.get('owned')), 'phase': 'route_a_post_loop' if closed else ph,
                     'cores': round(w, 3), 'mem_gb': round(m, 2), 'pooled_route_a': pooled, 'spike_gb': round(sp, 2),
                     'growth_gb': round(gr, 2),
                     'kind': (r['class'].get('family', 'DDO') if r.get('owned') else (r.get('foreign_kind') or 'GENERIC'))})
    head_pooled = bool(head['pooled'])
    n_pooled_after = pooled_ra + (1 if head_pooled else 0)
    spikes.sort(reverse=True)
    k = int(P['spike_count_cap'])
    spike_hard = sum(spikes[:k])
    spike_knee = spikes[0] if spikes else 0.0
    grow = growth if P['growth_reserve'] else 0.0
    knee, hard, pool = memory_limits(live, pool_free_gb, P)
    cores_after = cores + head['w_route_a']
    mem_hard_after = mem + head['res_route_a_gb'] + spike_hard + grow
    mem_knee_after = mem + head['res_route_a_gb'] + spike_knee
    if not probe_ok:
        reasons.append('PROBE_FAILED')
    if n_running >= max_concurrent:
        reasons.append('COUNT_MAX_CONCURRENT')
    if head_pooled and n_pooled_after > P['route_a_cap']:
        reasons.append('ROUTE_A_CAP')
    if cores_after > P['core_limit'] + 1e-9:
        reasons.append('CORE_LIMIT')
    if mem_hard_after > hard + 1e-9:
        reasons.append('MEMORY_HARD')
    if mem_knee_after > knee + 1e-9:
        reasons.append('MEMORY_KNEE')
    if swap_gb is None or swap_gb > P['swap_stop_gb']:
        reasons.append('SWAP_STOP')
    if since_last_start_s is not None and since_last_start_s < P['spacing_s']:
        reasons.append('SPACING')
    if history_s < P['warmup_s']:
        reasons.append('WARMUP')
    hold = twin_hold(runs, P)                                   # c2v003 (A140 N2)
    if head.get('family', 'DDO') in HELD_FAMILIES and hold['hold']:
        reasons.append('TWIN_HOLD')
    return {'admit': not reasons, 'reasons': reasons, 'cores_now': round(cores, 3), 'cores_after_admit': round(cores_after, 3),
            'mem_now_gb': round(mem, 2), 'mem_after_admit_gb': round(mem_hard_after, 2),
            'mem_knee_after_admit_gb': round(mem_knee_after, 2), 'spikes_reserved_gb': [round(x, 2) for x in spikes[:k]],
            'growth_reserved_gb': round(grow, 2), 'knee_gb': round(knee, 2), 'hard_gb': round(hard, 2),
            'pool_gb': None if pool is None else round(pool, 2), 'live_runs_gb': round(live, 2), 'pooled_route_a_now': pooled_ra,
            'swap_gb': swap_gb, 'since_last_start_s': since_last_start_s, 'runs': rows, 'head': head['name'],
            'head_family': head.get('family', 'DDO'), 'twin_hold': hold}


def twin_hold(runs, params=PARAMS):
    """c2v003 (A140 N2): the hold predicate.  hold is True while a foreign NGC_TWIN tree is in route A (its planned stop
    is the twin wall cap, 22,752 s), or an NGC_UNIDENTIFIED tree is in route A and younger than the twin wall cap + grace
    (unknown age: holds).  A twin older than that limit still holds and is listed as overdue (its monitor should have
    stopped it).  Same run dicts as evaluate().  -> {'hold', 'twins', 'overdue', 'limit_s'}"""
    P = params
    lim = float(P['twin_wall_cap_s']) + float(P['twin_hold_grace_s'])
    tw, od = [], []
    for r in runs:
        if r.get('owned') or (r.get('phase') or 'route_a') != 'route_a':
            continue
        kind = r.get('foreign_kind') or 'GENERIC'
        age = r.get('age_s')
        known = isinstance(age, (int, float)) and math.isfinite(age)
        if kind == 'NGC_TWIN':
            tw.append(r.get('key'))
            if known and age > lim:
                od.append(r.get('key'))
        elif kind == 'NGC_UNIDENTIFIED' and (not known or age <= lim):
            tw.append(r.get('key'))
    return {'hold': bool(tw), 'twins': tw, 'overdue': od, 'limit_s': lim}


def twin_start_check(*, runs, swap_gb, since_last_start_s, history_s, probe_ok=True, pool_free_gb=None, params=PARAMS):
    """c2v003 (A140 N2; step5_path L146 as a gate rule): may root start the cw8 twin now?  The twin class as the head of
    evaluate() (memory d1 / d2, cores, route-A cap, swap, spacing, warm-up, probe), plus two refusals:
      DDO_ROUTE_A_IN_FLIGHT  an owned run of family DDO, or a GENERIC foreign run, in route A and not post-loop;
      TWIN_ALREADY_RUNNING   twin_hold() holds already.
    Root also starts the twin only when no direct batch has a call pending (the packet does not read this gate)."""
    head = dict(foreign_class('NGC_TWIN', params), name='NGC_K32_CW8_TWIN_HEAD')
    d = evaluate(runs=runs, head=head, n_running=0, max_concurrent=1, swap_gb=swap_gb, since_last_start_s=since_last_start_s,
                 history_s=history_s, probe_ok=probe_ok, pool_free_gb=pool_free_gb, params=params)
    inflight = []
    for r in runs:
        if (r.get('phase') or 'route_a') != 'route_a' or r.get('pool_closed'):
            continue
        if r.get('owned'):
            if (r.get('class') or {}).get('family', 'DDO') == 'DDO':
                inflight.append(r.get('key'))
        elif (r.get('foreign_kind') or 'GENERIC') == 'GENERIC':
            inflight.append(r.get('key'))
    if inflight:
        d['reasons'].append('DDO_ROUTE_A_IN_FLIGHT')
    if d['twin_hold']['hold']:
        d['reasons'].append('TWIN_ALREADY_RUNNING')
    d['admit'] = not d['reasons']
    d['ddo_route_a_in_flight'] = inflight
    return d


# --------------------------------------------------------------------------------------------- stateful gate
class Gate:
    """Sampling wrapper around evaluate().  probe_fn, clock and spec_reader are injectable for synthetic tests only."""

    def __init__(self, params=None, probe_fn=None, clock=time.monotonic, spec_reader=None):
        self.P = dict(PARAMS)
        if params:
            self.P.update(params)
        check_foreign_classes(self.P)   # c2v003: an undersized NGC class refuses here
        self.probe_fn = probe_fn or (lambda: probe(params=self.P))
        self.clock = clock
        self.spec_reader = spec_reader or (lambda path: read_spec_route_a_workers(path, self.P))
        self.spec_cache = {}            # c2v003: (monitor pid, spec path) -> route_a.column_workers (read once per tree)
        self.n_spec_reads = 0
        self.hist = []                  # [(t, {pid: cpu_s})]
        self.last = None
        self.last_t = None
        self.t_first = None
        self.n_probes = 0
        self.max_nproc = {}             # monitor pid -> largest process count seen (pool opened)

    def foreign_kind(self, run):
        """c2v003 (A140 N1): GENERIC unless the monitor names the cx3r008 driver sha; then the spec leaf decides."""
        sha = run.get('driver_sha256')
        if sha != self.P['ngc_driver_sha256']:
            return 'GENERIC'
        key = (run.get('monitor_pid'), run.get('spec'))
        if key not in self.spec_cache:
            self.n_spec_reads += 1
            self.spec_cache[key] = self.spec_reader(run.get('spec')) if run.get('spec') else None
        return classify_foreign(sha, self.spec_cache[key], self.P)

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
            self.spec_cache = {k: v for k, v in self.spec_cache.items() if k[0] in live}
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

    def runs_view(self, snap, owned, last_own_start=None):
        """The run dicts evaluate() reads (c2v002's decide body; c2v003 adds foreign_kind) and since_last_start_s."""
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
                             'nproc': r['nproc'], 'age_s': r.get('age_s'), 'foreign_kind': self.foreign_kind(r)})
        for mp, o in owned.items():                         # owned but not (yet / any more) visible in ps
            if mp not in seen:
                ph = 'after' if route_a_done_path(o['progress']) else 'route_a'
                runs.append({'key': mp, 'owned': True, 'class': o['class'], 'phase': ph, 'footprint_gb': None, 'nproc': 0})
        ages = [r['age_s'] for r in (snap.get('runs') or [])]
        since = min(ages) if ages else None
        if last_own_start is not None:
            own = now - last_own_start
            since = own if since is None else min(since, own)
        return runs, since

    def decide(self, *, owned, head, n_running, max_concurrent, last_own_start=None):
        """owned: {monitor_pid: {'class': cls, 'progress': path}} for the calls this launcher runs.
        last_own_start: clock() time of this launcher's last start (None if none)."""
        snap = self.sample()
        runs, since = self.runs_view(snap, owned, last_own_start)
        d = evaluate(runs=runs, head=head, n_running=n_running, max_concurrent=max_concurrent,
                     swap_gb=snap.get('swap_gb'), since_last_start_s=since, history_s=self.history_s(),
                     probe_ok=bool(snap.get('ok')), pool_free_gb=snap.get('pool_free_gb'), params=self.P)
        d['probe_reasons'] = list(snap.get('reasons') or [])
        d['footprint_source'] = snap.get('footprint_source')
        return d

    def hold_check(self, force=True):
        """c2v003 (A140 N2): the predicate root reads before starting (or letting continue) a direct batch.
        hold_or_probe_failed is True when a twin holds or the probe failed (fail closed)."""
        snap = self.sample(force=force)
        runs, _ = self.runs_view(snap, {})
        h = twin_hold(runs, self.P)
        return dict(h, probe_ok=bool(snap.get('ok')), probe_reasons=list(snap.get('reasons') or []),
                    hold_or_probe_failed=bool(h['hold'] or not snap.get('ok')),
                    runs=[{'key': r['key'], 'phase': r['phase'], 'kind': r.get('foreign_kind'), 'age_s': r.get('age_s')}
                          for r in runs])

    def twin_start(self):
        """c2v003 (A140 N2): twin_start_check() on a fresh snapshot (no owned runs: root starts the twin)."""
        snap = self.sample()
        runs, since = self.runs_view(snap, {})
        d = twin_start_check(runs=runs, swap_gb=snap.get('swap_gb'), since_last_start_s=since, history_s=self.history_s(),
                             probe_ok=bool(snap.get('ok')), pool_free_gb=snap.get('pool_free_gb'), params=self.P)
        d['probe_reasons'] = list(snap.get('reasons') or [])
        return d


def describe():
    return {'module': MODULE_NAME, 'params': dict(PARAMS), 'monitor_pattern': MONITOR_PATTERN.pattern,
            'reasons': list(REASONS), 'foreign_kinds': list(FOREIGN_KINDS), 'held_families': list(HELD_FAMILIES)}


def main(argv=None):
    """Read-only predicates for root (c2v003, A140 N2).  Exit 0: clear; 3: hold / refuse; 2: probe failed (hold)."""
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--hold-check', action='store_true', help='twin hold predicate (hold direct batches while true)')
    g.add_argument('--twin-start-check', action='store_true', help='may root start the cw8 twin now (samples warmup_s)')
    a = ap.parse_args(argv)
    gate = Gate()
    if a.hold_check:
        d = gate.hold_check()
        print(json.dumps(d, indent=1, default=str))
        return 2 if not d['probe_ok'] else (3 if d['hold'] else 0)
    gate.sample(force=True)
    time.sleep(gate.P['warmup_s'])
    gate.sample(force=True)
    d = gate.twin_start()
    print(json.dumps({k: v for k, v in d.items() if k != 'runs'}, indent=1, default=str))
    return 0 if d['admit'] else 3


if __name__ == '__main__':
    sys.exit(main())
