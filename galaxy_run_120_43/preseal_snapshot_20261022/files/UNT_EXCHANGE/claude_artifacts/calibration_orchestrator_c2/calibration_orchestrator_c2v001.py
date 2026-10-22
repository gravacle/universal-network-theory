"""calibration_orchestrator_c2v001 -- DDO154 calibration orchestrator (Claude2 lane).

Connects
  * the calibration engine calibration_region_engine_c2v003a (193841fa...) and the freeze module
    prediction_freeze_c2v003a (5ee3e5dc...), both loaded from pinned bytes;
  * the route-B forward driver (galaxy_m0_forward_c2v003c, ed326130..., by default) run through the pinned
    root monitor (root_monitor_c2v001, ba031c23...) and campaign launcher (campaign_c2v001, 71274ceb...);
  * the coordinate spec DDO154_CALIBRATION_COORDINATE_SPEC_V001.json (theta -> call spec);
  * the completed A2 factor-10 anchor run, reused as the engine's seed evaluation through an ANCHOR ALIAS.

Algorithm (one wave per loop):
  1. PROBE. Run the frozen engine (run_calibration_region, unmodified) with a cache-backed forward. Cached theta
     return their recorded forward result. On the FIRST miss the request is exactly the engine's next real
     request. To batch further requests the probe identifies, by read-only frame inspection, the engine stage
     ("family") and the independent sub-sequence ("branch") of the request: Jacobian column, march side
     (round 0, linearised-polytope ray of round r, axis march of round r), local+global Halton design point,
     pre-march global design point. Inside one family branches are independent: a branch's requests depend only
     on that branch's own outcomes and on state fixed when the family began (code map in INDEPENDENCE below).
     The probe answers a miss with a PLACEHOLDER (an invalid outcome) so that the engine moves on to the next
     branch, records the first miss of every branch, ignores later misses of a placeholder branch, and raises
     the STOP sentinel (_ProbeStop, a BaseException) as soon as the engine leaves the family. The engine's
     fail-closed wrappers and its forward guard catch Exception only, so STOP propagates out of the engine and
     the probe run is discarded: nothing is logged, nothing is recorded, no budget is spent on a real run.
     A sibling is recorded only if the budget cannot be exhausted before the real engine reaches it: probe
     count + sum over placeholder branches of (branch bound - calls the probe made in it) < budget; otherwise
     the probe stops there. Repair and seed are single-request families.
  2. WAVE. The misses become one campaign (call specs from the mapper; only declared fields change), launched
     through the pinned campaign/monitor with max_concurrent x column_workers <= 12.
  3. INGEST. Receipts are verified (self-hash, spec and driver pins, result.json bytes); the forward result is
     stored in the cache under the canonical theta hash. VALID and INVALID (model/solver outcome) entries are
     final: an invalid evaluation stays invalid and is never relaunched. Infrastructure failures (monitor caps,
     missing/unverifiable receipts, spec refusals) halt the orchestrator for a recorded root decision
     (resolve --decision invalid | retry); nothing is retried automatically.
  4. Repeat until the probe completes with no miss. Then REPLAY: the real engine run with the full cache, twice;
     both must make ZERO uncached calls and give identical canonical bytes. The run is written as a calibration
     record and appended to the registry (write_calibration_record / verify_calibration_record, v003a).

INDEPENDENCE (engine line numbers, calibration_region_engine_c2v003a.py):
  jacobian    L1167-1257: column j's requests depend on u0, rel_step, min_step, max_halvings and column j's own
              validity only; a failed column does not stop later columns.
  march0      L2256-2263: march_side(a, +-V[k]) uses a, V, march_step and its own admitted flags (L1912-1997);
              boundary[] written by a side is not read by any other side.
  design      L2266-2300: local Halton points depend on a, V and the round-0 boundary (fixed before the family),
              global Halton points on rng_seed and n; duplicate skips depend on logged u only.
  gd_pre      L2008-2027 (run_before_march): Halton positions only.
  lp (rnd)    L2350-2391: rays from ext0 / hull_before / LP solutions computed at round start; rays_done
              holds directions only.
  axis (rnd)  L2393-2418: cands and extremes fixed at the start of part (b).
  repair, seed: sequential -> single-request families.

Writes only under the configured work_dir. numpy only (through the engine), single thread. Never opens any
NGC3198 file. Python: codex runtime, -I -B.

CLI:
  calibration_orchestrator_c2v001.py plan    --config CONFIG.json
  calibration_orchestrator_c2v001.py run     --config CONFIG.json [--max-waves N]
  calibration_orchestrator_c2v001.py resolve --config CONFIG.json --wave W (--key PREFIX | --all)
                                             --decision invalid|retry --reason TEXT
  calibration_orchestrator_c2v001.py status  --config CONFIG.json
Exit codes: 0 complete/ok, 3 refused, 4 HALTED_INFRA, 5 HALTED_DISK, 6 MAX_WAVES, 7 HALTED_UNRESOLVED,
8 LOCKED, 9 REPLAY_FAILED, 10 ORPHANS_STILL_RUNNING.
Importing this module does nothing.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import argparse
import copy
import datetime
import hashlib
import importlib.util
import json
import math
import shutil
import socket
import sys
import time
import types
from pathlib import Path

MODULE_NAME = 'calibration_orchestrator_c2v001'
SCHEMA_CONFIG = 'DDO154_CALIBRATION_ORCHESTRATOR_CONFIG_C2V001'
SCHEMA_SPEC = 'DDO154_CALIBRATION_COORDINATE_SPEC_C2V001'
SCHEMA_THETA_KEY = 'DDO154_CALIBRATION_THETA_KEY_C2V001'
SCHEMA_CACHE_ID = 'DDO154_CALIBRATION_CACHE_ID_C2V001'
SCHEMA_CACHE_ENTRY = 'DDO154_CALIBRATION_CACHE_ENTRY_C2V001'
SCHEMA_WAVE_PLAN = 'DDO154_CALIBRATION_WAVE_PLAN_C2V001'
SCHEMA_WAVE_RESULT = 'DDO154_CALIBRATION_WAVE_RESULT_C2V001'
SCHEMA_SUMMARY = 'DDO154_CALIBRATION_ORCHESTRATION_SUMMARY_C2V001'
MAPPING_ID = 'C2V001_PHYS4_GAMMA_EQ_GE_TIMES_EREF'
ANCHOR_ALIAS_RTOL = 1e-14
DECLARED_CHANGED_PATHS = ('label', 'physical.common_scale_s', 'physical.gamma', 'physical.ell_F_m',
                          'physical.distance_Mpc')
VARYING_EXPECTED = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'distance_Mpc')
FIXED_TEMPLATE_CHECKS = (('Eref_J', 'Eref_base_J'), ('entropy_K_factor', 'entropy_K_factor'))
MODEL_INVALID_DRIVER_STATUSES = ('COMPLETED_INVALID', 'FAILED_AT_STAGE', 'BLOCKED', 'ROUTE_A_NO_FIXED_POINT', 'FAILED')
PLACEHOLDER_REASON = 'ORCHESTRATOR_PROBE_PLACEHOLDER_NOT_AN_EVALUATION'
SINGLE_FAMILIES = ('seed', 'repair')
EXIT = {'COMPLETE': 0, 'OK': 0, 'REFUSED': 3, 'HALTED_INFRA': 4, 'HALTED_DISK': 5, 'MAX_WAVES': 6,
        'HALTED_UNRESOLVED': 7, 'LOCKED': 8, 'REPLAY_FAILED': 9, 'ORPHANS_STILL_RUNNING': 10}
CONFIG_KEYS = {'schema', 'synthetic_test', 'work_dir', 'coordinate_spec', 'observation_region', 'numerics',
               'ngc3198_slots', 'anchor', 'driver', 'monitor', 'campaign', 'python', 'max_concurrent', 'per_call',
               'campaign_wall_cap_s', 'disk_guard', 'orphan_wait', 'engine_parameters_override', 'executor', 'notes'}


class OrchestratorError(Exception):
    """Refusal: configuration, pin or consistency failure (exit 3)."""


class _ProbeStop(BaseException):
    """STOP sentinel. A BaseException on purpose: the engine's forward guard (_evaluate_point L1048-1053) and its
    fail-closed wrappers (_fail_closed L185-201) catch Exception only, so STOP leaves the engine at once, before
    the request is logged; the aborted run is discarded and never recorded."""

    def __init__(self, reason):
        BaseException.__init__(self, reason)
        self.reason = reason


# --------------------------------------------------------------------------------------------- small helpers
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def utc_compact():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def write_json_x(path, obj):
    raw = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    with open(path, 'xb') as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())
    return sha256_bytes(raw)


def append_jsonl(path, obj):
    line = canonical(obj) + b'\n'
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, line)
        os.fsync(fd)
    finally:
        os.close(fd)


def read_jsonl(path):
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, 'rb') as fh:
        for ln in fh.read().split(b'\n'):
            if ln.strip():
                out.append(json.loads(ln.decode('utf-8')))
    return out


def pid_alive(pid):
    try:
        os.kill(int(pid), 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except (TypeError, ValueError, OverflowError):
        return False
    return True


def read_pinned(pin, label):
    if not isinstance(pin, dict) or not isinstance(pin.get('path'), str) or not isinstance(pin.get('sha256'), str):
        raise OrchestratorError('%s: {path, sha256} required' % label)
    try:
        raw = Path(pin['path']).read_bytes()
    except OSError as exc:
        raise OrchestratorError('%s: unreadable %s: %s' % (label, pin['path'], exc))
    if sha256_bytes(raw) != pin['sha256']:
        raise OrchestratorError('%s: sha256 mismatch for %s' % (label, pin['path']))
    return raw


def load_pinned_module(pin, name, label):
    read_pinned(pin, label)
    sp = importlib.util.spec_from_file_location(name, pin['path'])
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    if sha256_file(pin['path']) != pin['sha256']:
        raise OrchestratorError('%s changed while loading' % label)
    return m


def theta_key(theta):
    """Canonical theta hash: sha256 of the canonical JSON of every engine coordinate's float value (repr is exact)."""
    th = {str(k): float(v) for k, v in theta.items()}
    for k, v in th.items():
        if not math.isfinite(v):
            raise OrchestratorError('non-finite theta[%s]' % k)
    return sha256_bytes(canonical({'schema': SCHEMA_THETA_KEY, 'theta': th}))


def diff_paths(a, b, prefix=''):
    """Dotted paths at which two JSON objects differ (dict keys recursed; anything else compared whole)."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = (prefix + '.' + k) if prefix else k
            if k not in a or k not in b:
                out.append(p)
            else:
                out.extend(diff_paths(a[k], b[k], p))
        return out
    return [] if canonical(a) == canonical(b) else [prefix or '$']


# --------------------------------------------------------------------------------------------- context
class Context:
    """Everything derived from the configuration and the pinned inputs (no side effects on disk)."""

    def __init__(self, config):
        if isinstance(config, (str, Path)):
            self.config_path = str(config)
            raw = Path(config).read_bytes()
            self.config_sha256 = sha256_bytes(raw)
            config = json.loads(raw.decode('utf-8'))
        else:
            self.config_path = None
            self.config_sha256 = sha256_bytes(canonical(config))
        self.cfg = cfg = config
        extra = set(cfg) - CONFIG_KEYS
        if cfg.get('schema') != SCHEMA_CONFIG or extra:
            raise OrchestratorError('config schema must be %s with keys %s (extra: %s)'
                                    % (SCHEMA_CONFIG, sorted(CONFIG_KEYS), sorted(extra)))
        self.synthetic = cfg.get('synthetic_test') is True
        self.work_dir = Path(cfg['work_dir'])
        if not self.work_dir.is_absolute():
            raise OrchestratorError('work_dir must be absolute')
        # coordinate spec
        spec_raw = read_pinned(cfg['coordinate_spec'], 'coordinate_spec')
        self.spec = spec = json.loads(spec_raw.decode('utf-8'))
        if spec.get('schema') != SCHEMA_SPEC:
            raise OrchestratorError('coordinate spec schema must be %s' % SCHEMA_SPEC)
        if spec['call_spec_mapping']['mapping_id'] != MAPPING_ID:
            raise OrchestratorError('coordinate spec mapping_id %r is not this module\'s %r'
                                    % (spec['call_spec_mapping']['mapping_id'], MAPPING_ID))
        # engine and freeze modules from pinned bytes (spec pins them)
        self.E = load_pinned_module(spec['engine'], 'orch_engine_c2v003a', 'engine')
        self.F = load_pinned_module(spec['freeze'], 'orch_freeze_c2v003a', 'freeze')
        # observation region
        reg_pin = cfg['observation_region']
        read_pinned(reg_pin, 'observation_region')
        if reg_pin['sha256'] != spec['observation_region']['sha256'] and not self.synthetic:
            raise OrchestratorError('observation region differs from the coordinate spec pin (only a synthetic_test '
                                    'config may use another region)')
        self.region_pin = reg_pin
        self.region = self.E.load_observation_region(path=reg_pin['path'], expected_sha256=reg_pin['sha256'])
        if not self.region['ok']:
            raise OrchestratorError('observation region: %s' % self.region['reasons'])
        self.row_ids = list(self.region['row_ids'])
        # engine coordinates through the freeze module (D4), NGC slots never reach the engine
        ngc = cfg.get('ngc3198_slots') or spec['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation']
        self.ngc_slots_placeholder = cfg.get('ngc3198_slots') is None
        fs = self.F.make_freeze_coordinate_spec(coordinates=list(spec['coordinates']) + list(ngc))
        if not fs['ok']:
            raise OrchestratorError('make_freeze_coordinate_spec: %s' % fs['reasons'])
        self.freeze_spec = fs
        self.engine_coordinates = fs['engine_coordinates']
        if canonical(self.engine_coordinates) != canonical(spec['engine_coordinates']):
            raise OrchestratorError('engine coordinates differ from the coordinate spec record')
        self.es = self.E.make_coordinate_spec(coordinates=self.engine_coordinates)
        if not self.es['ok']:
            raise OrchestratorError('engine make_coordinate_spec: %s' % self.es['reasons'])
        if tuple(self.es['varying_names']) != VARYING_EXPECTED:
            raise OrchestratorError('varying coordinates %r are not the mapping\'s %r' % (self.es['varying_names'],
                                                                                          VARYING_EXPECTED))
        self.n_varying = self.es['n_varying']
        # engine parameters
        params = copy.deepcopy(spec['engine_parameters'])
        if cfg.get('engine_parameters_override'):
            if not self.synthetic:
                raise OrchestratorError('engine_parameters_override is allowed only in a synthetic_test config')
            params.update(copy.deepcopy(cfg['engine_parameters_override']))
        self.params = params
        # call-spec template and numerics
        mp = spec['call_spec_mapping']
        self.template_raw = read_pinned(mp['template'], 'call-spec template')
        self.template = json.loads(self.template_raw.decode('utf-8'))
        self.template_sha256 = mp['template']['sha256']
        self.numerics = copy.deepcopy(cfg['numerics']) if cfg.get('numerics') is not None else \
            copy.deepcopy(self.template['numerics'])
        self.numerics_is_template = canonical(self.numerics) == canonical(self.template['numerics'])
        self.inclination_deg = float(spec['ddo154_forward_constants']['inclination_deg']['value'])
        if float(self.template['physical']['inclination_deg']) != self.inclination_deg:
            raise OrchestratorError('template inclination differs from the declared DDO154 constant')
        # launcher pins
        self.driver = cfg['driver']
        read_pinned(self.driver, 'driver')
        self.python = cfg['python']
        self.executor_kind = cfg.get('executor', 'campaign')
        if self.executor_kind not in ('campaign', 'in_process_test'):
            raise OrchestratorError('executor must be campaign or in_process_test')
        if self.executor_kind == 'in_process_test' and not self.synthetic:
            raise OrchestratorError('in_process_test executor requires synthetic_test')
        self.M = self.C = None
        if self.executor_kind == 'campaign':
            self.M = load_pinned_module(cfg['monitor'], 'orch_monitor_c2v001', 'monitor')
            self.C = load_pinned_module(cfg['campaign'], 'orch_campaign_c2v001', 'campaign')
            workers = int(self.numerics.get('column_workers', 1))
            mc = cfg['max_concurrent']
            if type(mc) is not int or mc < 1 or mc * workers > 12:
                raise OrchestratorError('max_concurrent (%r) x column_workers (%d) must be <= 12' % (mc, workers))
        self.max_concurrent = cfg.get('max_concurrent', 1)
        self.mapper = Mapper(self)
        self.cache_id = sha256_bytes(canonical({
            'schema': SCHEMA_CACHE_ID, 'mapping_id': MAPPING_ID, 'template_sha256': self.template_sha256,
            'numerics': self.numerics, 'driver_sha256': self.driver['sha256'], 'row_ids': self.row_ids,
            'engine_names': list(self.es['names']), 'ddo154_inclination_deg': self.inclination_deg}))
        # family bounds for the sibling guard
        P = self.params
        # one march side: <= floor(log2(sqrt(n)/march_step)) + 1 doubling evaluations (a unit direction crosses the
        # unit box within sqrt(n)), + 1 edge evaluation, + bisection_steps; +1 margin for rounding at the edge
        self.side_bound = int(math.floor(math.log2(math.sqrt(self.n_varying) / float(P['march_step'])))) + 3 + \
            int(P['bisection_steps'])
        self.trial_u = self._engine_trial_u()

    def _engine_trial_u(self):
        """trial_u exactly as run_calibration_region computes it (engine L2621-2625)."""
        E, es = self.E, self.es
        tu = []
        for nm in es['varying_names']:
            tr = es['transforms'][nm]
            x_lo, x_hi = E._x_of(tr, es['lower'][nm]), E._x_of(tr, es['upper'][nm])
            tu.append((E._x_of(tr, es['trial_values'][nm]) - x_lo) / (x_hi - x_lo))
        return tu

    def run_kwargs(self):
        P = self.params
        return dict(coordinates=self.engine_coordinates, observation_region_path=self.region_pin['path'],
                    observation_region_sha256=self.region_pin['sha256'], u_seed=P['u_seed'], budget=P['budget'],
                    rel_step=P['rel_step'], min_step=P['min_step'], max_halvings=P['max_halvings'],
                    null_tolerance=P['null_tolerance'], repair_iterations=P['repair_iterations'],
                    max_repair_step=P['max_repair_step'], march_step=P['march_step'],
                    bisection_steps=P['bisection_steps'], design_count=P['design_count'],
                    global_design_count=P['global_design_count'], max_march_rounds=P['max_march_rounds'],
                    hull_growth_tol=P['hull_growth_tol'], ddo154_distance=P['ddo154_distance'],
                    rng_seed=P['rng_seed'])

    def branch_bound(self, family):
        """Maximum number of forward calls one branch of this family can make (sibling guard)."""
        P = self.params
        name = family[0]
        if name == 'jacobian':
            return 2 * (int(P['max_halvings']) + 1)
        if name in ('march0', 'lp', 'axis'):
            return self.side_bound
        return 1


# --------------------------------------------------------------------------------------------- theta -> call spec
class Mapper:
    """theta (every engine coordinate) -> forward call spec; only the declared fields change."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.names = list(ctx.es['names'])
        self.fixed = {nm: ctx.es['trial_values'][nm] for nm in ctx.es['fixed_names']}
        self.lower, self.upper = dict(ctx.es['lower']), dict(ctx.es['upper'])

    def build(self, theta):
        ctx = self.ctx
        if not isinstance(theta, dict) or sorted(theta) != sorted(self.names):
            raise OrchestratorError('theta must carry exactly the engine coordinates %s' % self.names)
        th = {k: float(v) for k, v in theta.items()}
        for nm, v in th.items():
            if not math.isfinite(v):
                raise OrchestratorError('theta[%s] not finite' % nm)
            if not (self.lower[nm] <= v <= self.upper[nm]):
                raise OrchestratorError('theta[%s] = %r outside the computational box' % (nm, v))
        for nm, tv in self.fixed.items():
            if th[nm] != tv:
                raise OrchestratorError('fixed coordinate %s = %r differs from its trial value %r' % (nm, th[nm], tv))
        spec = copy.deepcopy(ctx.template)
        ph = spec['physical']
        for field, nm in FIXED_TEMPLATE_CHECKS:
            if float(ph[field]) != th[nm]:
                raise OrchestratorError('template physical.%s %r != theta %s %r' % (field, ph[field], nm, th[nm]))
        if float(ph['inclination_deg']) != ctx.inclination_deg:
            raise OrchestratorError('template inclination is not the declared DDO154 constant')
        key = theta_key(th)
        ph['common_scale_s'] = th['common_scale_s']
        ph['gamma'] = th['gamma_over_Eref'] * th['Eref_base_J']
        ph['ell_F_m'] = th['ell_F_m']
        ph['distance_Mpc'] = th['distance_Mpc']
        spec['label'] = 'DDO154 calibration orchestrator c2v001 theta %s; template %s' % (key[:16],
                                                                                        ctx.template_sha256[:8])
        spec['numerics'] = copy.deepcopy(ctx.numerics)
        changed = diff_paths(ctx.template, spec)
        for p in changed:
            if p in DECLARED_CHANGED_PATHS:
                continue
            if p.startswith('numerics') and not ctx.numerics_is_template:
                continue
            raise OrchestratorError('undeclared call-spec change at %s' % p)
        raw = (json.dumps(spec, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
        return {'key': key, 'spec': spec, 'raw': raw, 'sha256': sha256_bytes(raw), 'changed_paths': changed}


# --------------------------------------------------------------------------------------------- cache
class Cache:
    """theta-keyed cache: one immutable JSON file per canonical theta hash; never overwritten."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.dir = ctx.work_dir / 'cache' / ctx.cache_id
        self.entries_dir = self.dir / 'entries'
        self.entries = {}

    def open(self, create):
        if create:
            self.entries_dir.mkdir(parents=True, exist_ok=True)
            hdr = self.dir / 'CACHE_HEADER.json'
            body = {'schema': SCHEMA_CACHE_ID, 'cache_id': self.ctx.cache_id, 'mapping_id': MAPPING_ID,
                    'template_sha256': self.ctx.template_sha256, 'driver_sha256': self.ctx.driver['sha256'],
                    'numerics': self.ctx.numerics, 'row_ids': self.ctx.row_ids,
                    'engine_names': list(self.ctx.es['names'])}
            if hdr.exists():
                if json.loads(hdr.read_text())['cache_id'] != self.ctx.cache_id:
                    raise OrchestratorError('cache header id mismatch')
            else:
                write_json_x(hdr, body)
        self.entries = {}
        if not self.entries_dir.is_dir():
            return self
        for p in sorted(self.entries_dir.glob('*.json')):
            e = json.loads(p.read_bytes().decode('utf-8'))
            self._verify(e, p.stem)
            self.entries[e['key']] = e
        return self

    def _verify(self, e, stem):
        body = {k: v for k, v in e.items() if k != 'entry_sha256'}
        if sha256_bytes(canonical(body)) != e.get('entry_sha256'):
            raise OrchestratorError('cache entry %s self-hash mismatch' % stem)
        if e.get('schema') != SCHEMA_CACHE_ENTRY or e.get('cache_id') != self.ctx.cache_id or e.get('key') != stem:
            raise OrchestratorError('cache entry %s does not belong to this cache' % stem)
        if theta_key(e['theta']) != e['key']:
            raise OrchestratorError('cache entry %s key does not hash its theta' % stem)
        pv = e.get('provenance') or {}
        if pv.get('result_path') and pv.get('result_sha256'):
            if not os.path.isfile(pv['result_path']) or sha256_file(pv['result_path']) != pv['result_sha256']:
                raise OrchestratorError('cache entry %s: result.json bytes no longer verify' % stem)
        f = e.get('forward')
        if not isinstance(f, dict) or not isinstance(f.get('valid'), bool) or not isinstance(f.get('speeds_km_s'), dict):
            raise OrchestratorError('cache entry %s: malformed forward record' % stem)
        if (e['classification'] == 'VALID') != (f['valid'] is True):
            raise OrchestratorError('cache entry %s: classification inconsistent with forward.valid' % stem)

    def forward(self, key):
        e = self.entries.get(key)
        return copy.deepcopy(e['forward']) if e is not None else None

    def put(self, *, key, theta, classification, failure_class, source, provenance, forward):
        if classification not in ('VALID', 'INVALID'):
            raise OrchestratorError('classification must be VALID or INVALID')
        e = {'schema': SCHEMA_CACHE_ENTRY, 'cache_id': self.ctx.cache_id, 'key': key,
             'theta': {k: float(v) for k, v in theta.items()}, 'classification': classification,
             'failure_class': failure_class, 'source': source, 'provenance': provenance, 'forward': forward,
             'ingested_utc': utc()}
        if theta_key(e['theta']) != key:
            raise OrchestratorError('cache put: key does not hash theta')
        e['entry_sha256'] = sha256_bytes(canonical(e))
        path = self.entries_dir / (key + '.json')
        if path.exists():
            old = json.loads(path.read_bytes().decode('utf-8'))
            strip = lambda d: {k: v for k, v in d.items() if k not in ('ingested_utc', 'entry_sha256')}  # noqa: E731
            if canonical(strip(old)) != canonical(strip(e)):
                raise OrchestratorError('cache entry %s exists with different content (never overwritten)' % key)
            self.entries[key] = old
            return old, False
        self._verify(e, key)
        tmp = self.entries_dir / ('.%s.%d.tmp' % (key, os.getpid()))
        write_json_x(tmp, e)
        os.link(tmp, path)          # exclusive: fails if the entry appeared meanwhile
        os.unlink(tmp)              # the orchestrator's own temporary file
        self.entries[key] = e
        return e, True


# --------------------------------------------------------------------------------------------- engine probe
class Probe:
    """Runs the unmodified engine against the cache; see the module docstring for the probe rules."""

    def __init__(self, ctx):
        E = ctx.E
        self.ctx = ctx
        self.code_eval = E._evaluate_point.__code__
        self.code_jac = E.finite_difference_jacobian.__wrapped__.__code__
        self.code_explore = E._explore_impl.__code__
        nested = {c.co_name: c for c in self.code_explore.co_consts if isinstance(c, types.CodeType)}
        self.code_march = nested['march_side']
        self.code_gd = nested['global_design']
        self.code_evaluate = nested['evaluate']

    def context(self, f):
        """Read-only inspection of the engine frame that called forward: family, branch, purpose, u, counter."""
        if f is None or f.f_code is not self.code_eval:
            return {'family': ('unknown',), 'branch': ('unknown',), 'purpose': None, 'u': None, 'counter': None,
                    'm_id': 0}
        L = f.f_locals
        out = {'purpose': L.get('purpose'), 'u': list(L.get('u_list') or []), 'counter': L.get('counter'), 'm_id': 0}
        g = f.f_back
        if g is not None and g.f_code is self.code_jac:
            if out['purpose'] == 'seed':
                out.update(family=('seed',), branch=('seed',))
            else:
                out.update(family=('jacobian',), branch=('jac', int(g.f_locals['j'])))
            return out
        if g is None or g.f_code is not self.code_evaluate:
            out.update(family=('unknown',), branch=('unknown',))
            return out
        h = g.f_back
        x = h
        while x is not None and x.f_code is not self.code_explore:
            x = x.f_back
        if x is None:
            out.update(family=('unknown',), branch=('unknown',))
            return out
        XL = x.f_locals
        out['m_id'] = len(XL.get('ident') or [])
        purpose = out['purpose']
        if h.f_code is self.code_march:
            HL = h.f_locals
            rec = HL['rec']
            if HL.get('round0_k') is not None:
                out.update(family=('march0',), branch=('m0', int(HL['round0_k']), HL['round0_side']))
            else:
                rnd = int(XL['rnd'])
                if rec.get('kind') == 'lp_ray':
                    out.update(family=('lp', rnd), branch=('lp', rnd, int(rec['direction']), rec['side']))
                else:
                    out.update(family=('axis', rnd), branch=('ax', rnd, int(rec['anchor_log_index']),
                                                              int(rec['direction']), rec['side']))
        elif h.f_code is self.code_gd:
            HL = h.f_locals
            fam = ('gd_pre',) if HL['run_before_march'] else ('design',)
            out.update(family=fam, branch=('gd', int(HL['jj'])))
        elif h.f_code is self.code_explore and purpose == 'design':
            out.update(family=('design',), branch=('d', int(XL['jj'])))
        elif h.f_code is self.code_explore and purpose == 'repair':
            out.update(family=('repair',), branch=('repair', int(XL['it'])))
        else:
            out.update(family=('explore_%s' % purpose,), branch=(str(purpose),))
        return out

    def run(self, cache, mode, exclude=None):
        """mode 'probe' (record misses, placeholders inside one family) or 'replay' (any miss is a failure).
        exclude: keys treated as uncached (used to re-derive the plan of an interrupted, partly ingested wave)."""
        ctx = self.ctx
        exclude = set(exclude or ())
        st = {'misses': [], 'fake_family': None, 'faked': set(), 'entry': {}, 'branch_calls': {}, 'calls': 0, 'hits': 0,
              'placeholders': 0, 'families': [], 'keys_requested': [], 'stop': None}

        def fwd(theta):
            st['calls'] += 1
            c = self.context(sys._getframe(1))
            fam = c['family']
            if fam not in st['entry']:
                cnt = c['counter']
                st['entry'][fam] = (cnt['used'] - 1, cnt['budget']) if isinstance(cnt, dict) else (None, None)
                st['families'].append(fam)
            if st['fake_family'] is not None and fam != st['fake_family']:
                raise _ProbeStop('FAMILY_BOUNDARY_AFTER_PLACEHOLDERS')
            key = theta_key(theta)
            st['keys_requested'].append(key)
            if st['fake_family'] is not None:
                b0 = tuple(c['branch'])
                st['branch_calls'][b0] = st['branch_calls'].get(b0, 0) + 1
            got = None if key in exclude else cache.forward(key)
            if got is not None:
                st['hits'] += 1
                return got
            miss = {'key': key, 'theta': {k: float(v) for k, v in theta.items()}, 'family': list(fam),
                    'branch': list(c['branch']), 'purpose': c['purpose'], 'u': c['u'],
                    'sibling': st['fake_family'] is not None}
            br = tuple(c['branch'])
            if mode == 'replay':
                st['misses'].append(miss)
                raise _ProbeStop('REPLAY_MISS')
            if st['fake_family'] is None:
                # the first miss follows only real (cached) outcomes: it is exactly the engine's next request
                st['misses'].append(miss)
                if fam[0] in SINGLE_FAMILIES or fam[0] == 'unknown' or fam[0].startswith('explore_'):
                    raise _ProbeStop('SINGLE_REQUEST_FAMILY')
                st['fake_family'] = fam
                st['branch_calls'] = {}
            elif br not in st['faked']:
                # sibling guard: the real engine reaches this request only if the budget is not exhausted before it.
                # Upper bound on the real count before it: the probe count, plus, for every placeholder branch, the
                # calls it may still make in reality (branch bound minus the calls the probe made in it).
                cnt = c['counter']
                extra = sum(max(0, ctx.branch_bound(fam) - st['branch_calls'].get(b, 0)) for b in st['faked'])
                if not isinstance(cnt, dict) or (cnt['used'] - 1) + extra >= cnt['budget']:
                    raise _ProbeStop('SIBLING_BUDGET_GUARD')
                st['misses'].append(miss)
            st['faked'].add(br)
            st['placeholders'] += 1
            return {'valid': False, 'speeds_km_s': {}, 'reasons': [PLACEHOLDER_REASON]}

        run = None
        try:
            run = ctx.E.run_calibration_region(forward=fwd, **ctx.run_kwargs())
        except _ProbeStop as stop:
            st['stop'] = stop.reason
        res = {'mode': mode, 'stop_reason': st['stop'], 'misses': st['misses'], 'calls': st['calls'],
               'hits': st['hits'], 'placeholders': st['placeholders'],
               'families': [list(f) for f in st['families']], 'keys_requested': st['keys_requested']}
        res['complete'] = st['stop'] is None and not st['misses'] and st['placeholders'] == 0
        res['run'] = run if res['complete'] else None
        return res


# --------------------------------------------------------------------------------------------- executors
class CampaignExecutor:
    """One wave = one campaign of the pinned campaign launcher in <wave_dir>/campaign."""

    def __init__(self, ctx):
        self.ctx = ctx

    def campaign_dict(self, plan):
        cfg = self.ctx.cfg
        return {'calls': [{'spec': c['spec']} for c in plan['calls']], 'max_concurrent': cfg['max_concurrent'],
                'per_call': cfg['per_call'], 'campaign_wall_cap_s': cfg['campaign_wall_cap_s'],
                'driver': cfg['driver'], 'monitor': cfg['monitor']}

    def orphans(self, campaign_dir):
        """Call dirs of an interrupted campaign without a receipt. alive: True (driver child alive), False (dead),
        None (no launch record yet: the monitor may still be starting)."""
        out = []
        if not campaign_dir.is_dir():
            return out
        for d in sorted(campaign_dir.glob('call_*')):
            if (d / 'RECEIPT.json').exists():
                continue
            lp = d / 'RECEIPT.json.launch.json'
            pid = None
            if lp.is_file():
                try:
                    pid = json.loads(lp.read_text())['child_pid']
                except Exception:
                    pid = None
            out.append({'call_dir': str(d), 'child_pid': pid, 'alive': (pid_alive(pid) if pid else None)})
        return out

    def wait_orphans(self, campaign_dir, log):
        ow = self.ctx.cfg.get('orphan_wait') or {}
        poll, cap, grace = float(ow.get('poll_s', 30.0)), float(ow.get('cap_s', 21600.0)), float(ow.get('receipt_grace_s', 120.0))
        t0 = time.monotonic()
        dead_since = {}
        seen = self.orphans(campaign_dir)
        while True:
            pend = self.orphans(campaign_dir)
            if not pend:
                return {'orphans_seen': len(seen), 'waited_s': time.monotonic() - t0, 'still_running': []}
            now = time.monotonic()
            waiting = []
            for o in pend:
                if o['alive'] is True:
                    waiting.append(o)
                else:
                    dead_since.setdefault(o['call_dir'], now)
                    if now - dead_since[o['call_dir']] < grace:
                        waiting.append(o)
            if not waiting:
                return {'orphans_seen': len(seen), 'waited_s': now - t0, 'still_running': [],
                        'dead_without_receipt': [o['call_dir'] for o in pend]}
            if now - t0 > cap:
                return {'orphans_seen': len(seen), 'waited_s': now - t0, 'still_running': waiting}
            log('waiting for %d orphaned call(s) of an interrupted wave' % len(waiting))
            time.sleep(poll)

    def execute(self, wave_dir, plan, resume, log):
        cdir = wave_dir / 'campaign'
        orph = {'orphans_seen': 0, 'waited_s': 0.0, 'still_running': []}
        if resume and cdir.exists():
            orph = self.wait_orphans(cdir, log)
            if orph['still_running']:
                return None, {'status': 'ORPHANS_STILL_RUNNING', 'orphans': orph}
        out = self.ctx.C.run_campaign(campaign=self.campaign_dict(plan), campaign_dir=str(cdir),
                                      resume=bool(resume and cdir.exists()), python=self.ctx.python)
        if not out.get('ok'):
            raise OrchestratorError('campaign refused: %s' % out.get('reasons'))
        meta = {k: out.get(k) for k in ('status', 'launched', 'max_concurrent_observed', 'n_ok', 'n_failed',
                                        'n_resumed', 'n_not_started', 'n_unverified', 'campaign_wall_used_s',
                                        'summary_path')}
        meta['orphans'] = orph
        return out['calls'], meta

    def classify(self, plan_call, rec):
        """-> ('VALID'|'INVALID', failure_class, forward, provenance) or ('INFRA', reason, None, provenance)."""
        ctx = self.ctx
        prov = {'call_dir': rec.get('call_dir'), 'campaign_status': rec.get('status'), 'spec_sha256': plan_call['spec_sha256']}
        st = rec.get('status')
        if st not in ('OK', 'FAILED', 'RESUMED_OK', 'RESUMED_FAILED'):
            return 'INFRA', 'CAMPAIGN_%s' % st, None, prov
        d = Path(rec['call_dir'])
        rp = d / 'RECEIPT.json'
        if not rp.is_file():
            return 'INFRA', 'NO_RECEIPT', None, prov
        v = ctx.M.verify_receipt(rp, spec_sha256=plan_call['spec_sha256'], driver_sha256=ctx.driver['sha256'])
        if not v['ok']:
            return 'INFRA', 'RECEIPT_UNVERIFIED: %s' % v['reasons'], None, prov
        r = v['receipt']
        prov.update({'receipt_path': str(rp), 'receipt_file_sha256': sha256_file(rp),
                     'receipt_sha256_self': r.get('receipt_sha256'), 'monitor_status': r.get('status'),
                     'driver_status': r.get('driver_status'), 'exit_code': r.get('exit_code'),
                     'stop_reason': r.get('stop_reason'), 'elapsed_seconds': r.get('elapsed_seconds'),
                     'peak_rss_bytes': r.get('peak_rss_bytes'), 'final_output_bytes': r.get('final_output_bytes'),
                     'driver_sha256': ctx.driver['sha256']})
        if not (d / 'spec.json').is_file() or sha256_file(d / 'spec.json') != plan_call['spec_sha256']:
            return 'INFRA', 'SPEC_FILE_MISMATCH', None, prov
        if str(r.get('status', '')).startswith('STOPPED_'):
            return 'INFRA', 'MONITOR_%s' % r['status'], None, prov
        pin = r.get('result')
        if not pin:
            return 'INFRA', 'NO_RESULT_JSON', None, prov
        raw = Path(pin['path']).read_bytes()
        if sha256_bytes(raw) != pin['sha256']:
            return 'INFRA', 'RESULT_HASH', None, prov
        prov.update({'result_path': pin['path'], 'result_sha256': pin['sha256']})
        res = json.loads(raw.decode('utf-8'))
        if res.get('call_spec_sha256') != plan_call['spec_sha256'] or res.get('driver_sha256') != ctx.driver['sha256']:
            return 'INFRA', 'RESULT_NOT_BOUND_TO_SPEC_OR_DRIVER', None, prov
        ds = r.get('driver_status')
        if ds != res.get('status'):
            return 'INFRA', 'DRIVER_STATUS_MISMATCH %r/%r' % (ds, res.get('status')), None, prov
        reasons = [str(x) for x in (res.get('reasons') or [])][:8]
        if ds == 'COMPLETED' and res.get('valid') is True:
            sp = res.get('speeds_km_s')
            if not isinstance(sp, dict) or any(rid not in sp for rid in ctx.row_ids):
                return 'INFRA', 'ROW_IDS_MISSING', None, prov
            speeds = {rid: sp[rid] for rid in ctx.row_ids}
            if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
                       for x in speeds.values()):
                return 'INFRA', 'NONFINITE_SPEED_IN_VALID_RESULT', None, prov
            return 'VALID', None, {'valid': True, 'speeds_km_s': speeds, 'reasons': []}, prov
        if ds in MODEL_INVALID_DRIVER_STATUSES:
            sp = res.get('speeds_km_s') if isinstance(res.get('speeds_km_s'), dict) else {}
            return 'INVALID', ds, {'valid': False, 'speeds_km_s': {k: sp[k] for k in sp if k in ctx.row_ids},
                                   'reasons': ['DRIVER_STATUS %s' % ds] + reasons}, prov
        return 'INFRA', 'DRIVER_STATUS_%s' % ds, None, prov


class InProcessExecutor:
    """SYNTHETIC TESTS ONLY: evaluates a Python forward(call_spec) in process (no monitor, no receipts)."""

    def __init__(self, ctx, spec_forward):
        if not ctx.synthetic:
            raise OrchestratorError('InProcessExecutor requires synthetic_test')
        self.ctx = ctx
        self.spec_forward = spec_forward

    def execute(self, wave_dir, plan, resume, log):
        recs = []
        for c in plan['calls']:
            recs.append({'status': 'IN_PROCESS', 'forward': self.spec_forward(c['spec'])})
        return recs, {'status': 'IN_PROCESS', 'launched': len(recs), 'orphans': None}

    def classify(self, plan_call, rec):
        f = rec['forward']
        prov = {'executor': 'IN_PROCESS_TEST_ONLY', 'spec_sha256': plan_call['spec_sha256']}
        if not isinstance(f, dict):
            return 'INFRA', 'IN_PROCESS_NON_DICT', None, prov
        if f.get('valid') is True:
            return 'VALID', None, copy.deepcopy(f), prov
        return 'INVALID', 'IN_PROCESS_INVALID', copy.deepcopy(f), prov


# --------------------------------------------------------------------------------------------- orchestrator
class Lock:
    def __init__(self, work_dir):
        self.path = Path(work_dir) / 'ORCHESTRATOR.lock'
        self.held = False
        self.stale = None

    def acquire(self):
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                try:
                    old = json.loads(self.path.read_text())
                except Exception:
                    old = {}
                if pid_alive(old.get('pid')) and old.get('host') == socket.gethostname():
                    return False
                self.stale = str(self.path) + '.stale_%s_%s' % (utc_compact(), old.get('pid'))
                os.rename(self.path, self.stale)
                continue
            os.write(fd, canonical({'pid': os.getpid(), 'utc': utc(), 'host': socket.gethostname(),
                                    'module': MODULE_NAME}))
            os.close(fd)
            self.held = True
            return True
        return False

    def release(self):
        if self.held:
            try:
                if json.loads(self.path.read_text()).get('pid') == os.getpid():
                    os.unlink(self.path)   # the orchestrator's own lock file
            except OSError:
                pass
            self.held = False


class Orchestrator:
    def __init__(self, ctx, executor=None, log=None):
        self.ctx = ctx
        self.executor = executor if executor is not None else (
            CampaignExecutor(ctx) if ctx.executor_kind == 'campaign' else None)
        if self.executor is None:
            raise OrchestratorError('in_process_test configs need an explicit InProcessExecutor')
        self.cache = Cache(ctx)
        self.probe = Probe(ctx)
        self.waves_dir = ctx.work_dir / 'waves'
        self.ledger_path = ctx.work_dir / 'LAUNCH_LEDGER.jsonl'
        self.retry_path = ctx.work_dir / 'RETRY_AUTHORISED.jsonl'
        self.resolution_path = ctx.work_dir / 'RESOLUTIONS.jsonl'
        self.events_path = ctx.work_dir / 'EVENTS.jsonl'
        self._log = log or (lambda m: print('[%s] %s' % (utc(), m), file=sys.stderr, flush=True))
        self.alias = None

    def log(self, msg, **kw):
        self._log(msg)
        if self.ctx.work_dir.is_dir():
            append_jsonl(self.events_path, dict({'utc': utc(), 'pid': os.getpid(), 'msg': msg}, **kw))

    # ---------------------------------------------------------------- setup
    def prepare(self, create):
        if create:
            self.ctx.work_dir.mkdir(parents=True, exist_ok=True)
            cfg_copy = self.ctx.work_dir / ('CONFIG_COPY_%s.json' % self.ctx.config_sha256[:16])
            if not cfg_copy.exists():
                write_json_x(cfg_copy, self.ctx.cfg)
        self.cache.open(create=create)
        self.alias = self.install_anchor_alias(write=create)
        return self.alias

    def install_anchor_alias(self, write):
        ctx = self.ctx
        an = ctx.cfg.get('anchor')
        if not an or not an.get('use'):
            return {'used': False, 'reason': 'ANCHOR_DISABLED_IN_CONFIG'}
        if not ctx.numerics_is_template:
            return {'used': False, 'reason': 'NUMERICS_DIFFER_FROM_ANCHOR (seed will be computed)'}
        if an['spec_sha256'] != ctx.template_sha256:
            raise OrchestratorError('anchor spec sha is not the template sha')
        if an['driver_sha256'] != ctx.driver['sha256'] and an.get('accept_driver_equivalence') is not True:
            return {'used': False, 'reason': 'ANCHOR_DRIVER_DIFFERS_AND_EQUIVALENCE_NOT_ACCEPTED'}
        rraw = read_pinned(an['receipt'], 'anchor receipt')
        mon = ctx.M if ctx.M is not None else load_pinned_module(ctx.cfg['monitor'], 'orch_monitor_alias', 'monitor')
        v = mon.verify_receipt(an['receipt']['path'], spec_sha256=an['spec_sha256'], driver_sha256=an['driver_sha256'])
        if not v['ok']:
            raise OrchestratorError('anchor receipt does not verify: %s' % v['reasons'])
        rec = v['receipt']
        if rec.get('status') != 'FINISHED' or rec.get('driver_status') != 'COMPLETED' or \
                (rec.get('result') or {}).get('sha256') != an['result']['sha256']:
            raise OrchestratorError('anchor receipt is not a FINISHED/COMPLETED receipt of the pinned result')
        res = json.loads(read_pinned(an['result'], 'anchor result').decode('utf-8'))
        if res.get('call_spec_sha256') != ctx.template_sha256 or res.get('driver_sha256') != an['driver_sha256'] or \
                res.get('valid') is not True or res.get('status') != 'COMPLETED':
            raise OrchestratorError('anchor result does not bind to the template spec / anchor driver or is not valid')
        sp = res.get('speeds_km_s') or {}
        if any(rid not in sp or not math.isfinite(sp[rid]) for rid in ctx.row_ids):
            raise OrchestratorError('anchor result lacks finite speeds for the region rows')
        nat = ctx.E.to_natural(spec=ctx.es, u=ctx.trial_u)
        if not nat['ok']:
            raise OrchestratorError('to_natural at trial_u: %s' % nat['reasons'])
        theta = nat['theta_natural']
        built = ctx.mapper.build(theta)
        tp, bp = ctx.template['physical'], built['spec']['physical']
        dev = {}
        for k in tp:
            dev[k] = 0.0 if tp[k] == bp[k] else abs(bp[k] - tp[k]) / abs(tp[k])
        if max(dev.values()) > ANCHOR_ALIAS_RTOL:
            raise OrchestratorError('anchor alias: mapped seed physical deviates beyond %g: %r' % (ANCHOR_ALIAS_RTOL, dev))
        other = [p for p in diff_paths({k: v for k, v in ctx.template.items() if k != 'physical'},
                                       {k: v for k, v in built['spec'].items() if k != 'physical'}) if p != 'label']
        if other:
            raise OrchestratorError('anchor alias: non-physical fields differ: %s' % other)
        prov = {'anchor_receipt_path': an['receipt']['path'], 'anchor_receipt_file_sha256': an['receipt']['sha256'],
                'anchor_receipt_sha256_self': rec.get('receipt_sha256'), 'result_path': an['result']['path'],
                'result_sha256': an['result']['sha256'], 'anchor_spec_sha256': an['spec_sha256'],
                'anchor_driver_sha256': an['driver_sha256'], 'calibration_driver_sha256': ctx.driver['sha256'],
                'driver_equivalence_accepted': an['driver_sha256'] != ctx.driver['sha256'],
                'alias_spec_sha256_not_launched': built['sha256'], 'relative_deviation': dev,
                'alias_rtol': ANCHOR_ALIAS_RTOL, 'elapsed_seconds': rec.get('elapsed_seconds')}
        fwd = {'valid': True, 'speeds_km_s': {rid: float(sp[rid]) for rid in ctx.row_ids}, 'reasons': []}
        if write:
            self.cache.put(key=built['key'], theta=theta, classification='VALID', failure_class=None,
                           source='ANCHOR_ALIAS', provenance=prov, forward=fwd)
        elif built['key'] not in self.cache.entries:
            self.cache.entries[built['key']] = {'key': built['key'], 'forward': fwd, 'classification': 'VALID',
                                                'source': 'ANCHOR_ALIAS(unwritten)'}
        del rraw
        return {'used': True, 'key': built['key'], 'max_relative_deviation': max(dev.values()),
                'driver_equivalence_accepted': prov['driver_equivalence_accepted']}

    # ---------------------------------------------------------------- waves
    def wave_dirs(self):
        if not self.waves_dir.is_dir():
            return []
        return sorted(p for p in self.waves_dir.glob('wave_*') if p.is_dir())

    def launches(self):
        n = {}
        for ln in read_jsonl(self.ledger_path):
            n[ln['key']] = n.get(ln['key'], 0) + 1
        return n

    def authorised(self):
        n = {}
        for ln in read_jsonl(self.retry_path):
            n[ln['key']] = n.get(ln['key'], 0) + 1
        return n

    def make_plan(self, wave_no, misses):
        calls, seen = [], set()
        for m in misses:
            if m['key'] in seen:
                continue
            seen.add(m['key'])
            b = self.ctx.mapper.build(m['theta'])
            if b['key'] != m['key']:
                raise OrchestratorError('mapper key differs from probe key')
            calls.append({'call_index': len(calls), 'key': m['key'], 'theta': m['theta'], 'family': m['family'],
                          'branch': m['branch'], 'purpose': m['purpose'], 'u': m['u'], 'sibling': m['sibling'],
                          'spec': b['spec'], 'spec_sha256': b['sha256'], 'changed_paths': b['changed_paths']})
        return {'schema': SCHEMA_WAVE_PLAN, 'wave': wave_no, 'created_utc': utc(), 'cache_id': self.ctx.cache_id,
                'module': MODULE_NAME, 'calls': calls, 'n_calls': len(calls),
                'families': sorted(set(tuple(c['family']) for c in calls)),
                'batches': int(math.ceil(len(calls) / float(max(1, self.ctx.max_concurrent))))}

    def disk_ok(self, n_calls):
        dg = self.ctx.cfg.get('disk_guard') or {}
        per = int(dg.get('per_call_bytes', (self.ctx.cfg.get('per_call') or {}).get('output_cap_bytes', 0)))
        need = n_calls * per + int(dg.get('reserve_bytes', 0))
        free = shutil.disk_usage(str(self.ctx.work_dir)).free
        return free >= need, {'free_bytes': free, 'needed_bytes': need, 'per_call_bytes': per, 'n_calls': n_calls}

    def ingest(self, wave_dir, plan, records, meta):
        n = {'VALID': 0, 'INVALID': 0, 'INFRA': 0, 'already_cached': 0}
        infra = []
        out_calls = []
        for c, rec in zip(plan['calls'], records):
            cls, fc, fwd, prov = self.executor.classify(c, rec)
            prov = dict(prov, wave=plan['wave'], call_index=c['call_index'])
            if cls == 'INFRA':
                n['INFRA'] += 1
                infra.append({'key': c['key'], 'call_index': c['call_index'], 'reason': fc, 'provenance': prov})
                out_calls.append({'key': c['key'], 'classification': 'INFRA', 'reason': fc})
                continue
            src = 'WAVE' if isinstance(self.executor, CampaignExecutor) else 'IN_PROCESS_TEST'
            _, new = self.cache.put(key=c['key'], theta=c['theta'], classification=cls, failure_class=fc, source=src,
                                    provenance=prov, forward=fwd)
            n[cls] += 1
            if not new:
                n['already_cached'] += 1
            out_calls.append({'key': c['key'], 'classification': cls, 'failure_class': fc,
                              'elapsed_seconds': prov.get('elapsed_seconds'), 'peak_rss_bytes': prov.get('peak_rss_bytes')})
        result = {'schema': SCHEMA_WAVE_RESULT, 'wave': plan['wave'], 'utc': utc(), 'counts': n, 'calls': out_calls,
                  'campaign': meta, 'infra': infra}
        if infra:
            write_json_x(wave_dir / 'INFRA_HALT.json', {'wave': plan['wave'], 'utc': utc(), 'infra': infra,
                                                        'rule': 'never retried automatically; root resolves each key '
                                                                'with: resolve --decision invalid|retry'})
        write_json_x(wave_dir / 'WAVE_RESULT.json', result)
        return result

    def run_wave(self, wave_dir, plan, resume):
        t0 = time.monotonic()
        records, meta = self.executor.execute(wave_dir, plan, resume, self.log)
        if records is None:
            return None, meta
        res = self.ingest(wave_dir, plan, records, meta)
        res['wall_s'] = time.monotonic() - t0
        return res, meta

    # ---------------------------------------------------------------- main loop
    def run(self, max_waves=None):
        ctx = self.ctx
        ctx.work_dir.mkdir(parents=True, exist_ok=True)
        lock = Lock(ctx.work_dir)
        if not lock.acquire():
            return {'status': 'LOCKED'}
        try:
            self.prepare(create=True)
            self.log('orchestrator start', cache_id=ctx.cache_id, alias=self.alias, stale_lock=lock.stale)
            final = ctx.work_dir / 'FINAL_SUMMARY.json'
            if final.exists():
                return dict(json.loads(final.read_text()), status='COMPLETE', note='already complete')
            # resume an interrupted wave
            for wd in self.wave_dirs():
                if (wd / 'WAVE_PLAN.json').is_file() and not (wd / 'WAVE_RESULT.json').exists():
                    plan = json.loads((wd / 'WAVE_PLAN.json').read_text())
                    pr = self.probe.run(self.cache, 'probe', exclude=[c['key'] for c in plan['calls']])
                    if [m['key'] for m in self._dedup(pr['misses'])] != [c['key'] for c in plan['calls']]:
                        raise OrchestratorError('interrupted wave %s: the probe no longer predicts its calls '
                                                '(determinism failure)' % wd.name)
                    self.log('resuming interrupted wave %s (%d calls)' % (wd.name, plan['n_calls']))
                    res, meta = self.run_wave(wd, plan, resume=True)
                    if res is None:
                        return {'status': 'ORPHANS_STILL_RUNNING', 'wave': wd.name, 'meta': meta}
                    if res['infra']:
                        return {'status': 'HALTED_INFRA', 'wave': wd.name, 'infra': res['infra']}
            waves_run = 0
            while True:
                pr = self.probe.run(self.cache, 'probe')
                if pr['complete']:
                    break
                misses = self._dedup(pr['misses'])
                if not misses:
                    raise OrchestratorError('probe stopped (%s) without a miss' % pr['stop_reason'])
                launched, auth = self.launches(), self.authorised()
                again = [m['key'] for m in misses if launched.get(m['key'], 0) >= 1 + auth.get(m['key'], 0)]
                if again:
                    self.log('halt: %d requested theta were launched before and are unresolved' % len(again))
                    return {'status': 'HALTED_UNRESOLVED', 'keys': again,
                            'rule': 'an earlier launch of these theta ended with an infrastructure failure; resolve them'}
                if max_waves is not None and waves_run >= max_waves:
                    return {'status': 'MAX_WAVES', 'next_wave_calls': len(misses)}
                ok, disk = self.disk_ok(len(misses))
                if not ok:
                    self.log('halt: disk guard', disk=disk)
                    return {'status': 'HALTED_DISK', 'disk': disk}
                wave_no = len(self.wave_dirs()) + 1
                wd = self.waves_dir / ('wave_%04d' % wave_no)
                wd.mkdir(parents=True, exist_ok=False)
                plan = self.make_plan(wave_no, misses)
                plan['probe'] = {k: pr[k] for k in ('stop_reason', 'calls', 'hits', 'placeholders', 'families')}
                plan['disk'] = disk
                write_json_x(wd / 'WAVE_PLAN.json', plan)
                for c in plan['calls']:
                    append_jsonl(self.ledger_path, {'wave': wave_no, 'call_index': c['call_index'], 'key': c['key'],
                                                    'spec_sha256': c['spec_sha256'], 'utc': utc()})
                self.log('wave %d: %d calls, families %s, batches %d' % (wave_no, plan['n_calls'], plan['families'],
                                                                         plan['batches']))
                res, meta = self.run_wave(wd, plan, resume=False)
                waves_run += 1
                if res is None:
                    return {'status': 'ORPHANS_STILL_RUNNING', 'wave': wd.name, 'meta': meta}
                self.log('wave %d ingested: %s' % (wave_no, res['counts']))
                if res['infra']:
                    return {'status': 'HALTED_INFRA', 'wave': wd.name, 'infra': res['infra']}
            return self.finalise()
        finally:
            lock.release()

    @staticmethod
    def _dedup(misses):
        out, seen = [], set()
        for m in misses:
            if m['key'] not in seen:
                seen.add(m['key'])
                out.append(m)
        return out

    # ---------------------------------------------------------------- replay, record, summary
    def finalise(self):
        ctx = self.ctx
        r1 = self.probe.run(self.cache, 'replay')
        r2 = self.probe.run(self.cache, 'replay')
        replay = {'calls': r1['calls'], 'hits': r1['hits'], 'uncached_calls': len(r1['misses']),
                  'complete': r1['complete'] and r2['complete'], 'stop_reason': r1['stop_reason']}
        if not (r1['complete'] and r2['complete']) or r1['misses'] or r2['misses'] or r1['calls'] != r1['hits']:
            self.log('REPLAY FAILED', replay=replay)
            return {'status': 'REPLAY_FAILED', 'replay': replay}
        b1, b2 = ctx.E._canonical_bytes(r1['run']), ctx.E._canonical_bytes(r2['run'])
        replay['deterministic'] = b1 == b2
        replay['run_canonical_sha256'] = sha256_bytes(b1)
        if not replay['deterministic']:
            return {'status': 'REPLAY_FAILED', 'replay': replay}
        run = r1['run']
        rec_dir = ctx.work_dir / 'records'
        rec_dir.mkdir(exist_ok=True)
        rec_path = rec_dir / ('CALIBRATION_RECORD_%s_%s.json' % (run['status'], utc_compact()))
        reg_path = rec_dir / 'CALIBRATION_REGISTRY.jsonl'
        w = ctx.E.write_calibration_record(run=run, record_path=str(rec_path), registry_path=str(reg_path))
        if not w['ok']:
            raise OrchestratorError('write_calibration_record: %s' % w['reasons'])
        vr = ctx.E.verify_calibration_record(record_path=str(rec_path), registry_path=str(reg_path))
        summary = self.summary(run, replay, w, vr)
        summary['summary_file_sha256'] = write_json_x(ctx.work_dir / 'FINAL_SUMMARY.json', summary)
        self.log('orchestration complete: engine status %s, record %s' % (run['status'], w['record_file_sha256']))
        return dict(summary, status='COMPLETE')

    def summary(self, run, replay, w, vr):
        ctx = self.ctx
        used = []
        for e in run.get('evaluation_log') or []:
            if isinstance(e.get('theta_natural'), dict):
                used.append(theta_key(e['theta_natural']))
        used_set = set(used)
        launched = self.launches()
        waste = sorted(k for k in launched if k not in used_set and k in self.cache.entries)
        waves = []
        for wd in self.wave_dirs():
            p = json.loads((wd / 'WAVE_PLAN.json').read_text())
            r = json.loads((wd / 'WAVE_RESULT.json').read_text()) if (wd / 'WAVE_RESULT.json').exists() else {}
            waves.append({'wave': p['wave'], 'n_calls': p['n_calls'], 'batches': p['batches'], 'families': p['families'],
                          'counts': r.get('counts'), 'wall_s': r.get('wall_s')})
        ex = run.get('exploration') or {}
        side_recs = []
        for k, sides in (ex.get('boundary_detail') or {}).items():
            for sd, rec in (sides or {}).items():
                if rec:
                    side_recs.append(('round0', rec))
        for rr in ex.get('march_rounds') or []:
            for ray in rr.get('lp_rays') or []:
                if ray.get('side_record'):
                    side_recs.append(('round%d_lp' % rr['round'], ray['side_record']))
            for an in rr.get('anchors') or []:
                for rec in an.get('sides') or []:
                    side_recs.append(('round%d_axis' % rr['round'], rec))
        validity_limited = [{'where': wh, 'anchor_log_index': r.get('anchor_log_index'), 'direction': r.get('direction'),
                             'side': r.get('side'), 'kind': r.get('kind'), 'boundary_cause': r.get('boundary_cause')}
                            for wh, r in side_recs if str(r.get('boundary_cause', '')).startswith('INVALID_EVALUATION')]
        edge_limited = []
        names = list(ctx.es['varying_names'])
        for pt in ex.get('admitted_points') or []:
            for j, x in enumerate(pt['u']):
                if x <= 1e-9:
                    edge_limited.append((names[j], 'lower'))
                elif x >= 1.0 - 1e-9:
                    edge_limited.append((names[j], 'upper'))
        edge_limited = sorted(set(edge_limited))
        inv = {}
        for k in used_set:
            e = self.cache.entries.get(k)
            if e and e['classification'] == 'INVALID':
                inv[e.get('failure_class')] = inv.get(e.get('failure_class'), 0) + 1
        jac = run.get('jacobian') or {}
        return {
            'schema': SCHEMA_SUMMARY, 'module': MODULE_NAME, 'utc': utc(), 'synthetic_test': ctx.synthetic,
            'config_sha256': ctx.config_sha256, 'cache_id': ctx.cache_id,
            'pins': {'coordinate_spec': ctx.cfg['coordinate_spec'], 'observation_region': ctx.region_pin,
                     'engine': ctx.spec['engine'], 'freeze': ctx.spec['freeze'], 'driver': ctx.driver,
                     'monitor': ctx.cfg.get('monitor'), 'campaign': ctx.cfg.get('campaign'),
                     'template': ctx.spec['call_spec_mapping']['template'],
                     'orchestrator': {'path': os.path.realpath(__file__), 'sha256': sha256_file(os.path.realpath(__file__))}},
            'numerics_is_template': ctx.numerics_is_template, 'anchor_alias': self.alias,
            'engine_parameters': ctx.params, 'ngc_slots_placeholder': ctx.ngc_slots_placeholder,
            'engine_status': run['status'], 'engine_ok': run['ok'], 'stage_reached': run.get('stage_reached'),
            'n_admitted': (ex.get('n_admitted') if ex else None), 'region_possibly_truncated': run.get('region_possibly_truncated'),
            'truncation_causes': run.get('truncation_causes'), 'exploration_fingerprint': run.get('exploration_fingerprint'),
            'refinement_status': ex.get('refinement_status') if ex else None,
            'jacobian_steps_detail': jac.get('steps_detail'),
            'evaluations_in_run': len(used), 'distinct_theta_in_run': len(used_set),
            'invalid_evaluations_in_run_by_class': inv,
            'replay': replay,
            'record': {'record_path': w['record_path'], 'record_file_sha256': w['record_file_sha256'],
                       'record_sha256': w['record_sha256'], 'registry_path': w['registry_path'],
                       'registry_line_sha256': w['registry_line_sha256'], 'exploration_fingerprint': w['exploration_fingerprint'],
                       'verify_ok': vr['ok'], 'registry_chain_ok': vr['registry_chain_ok'], 'verify_reasons': vr['reasons']},
            'waves': waves, 'n_waves': len(waves), 'n_batches': sum(x['batches'] for x in waves),
            'n_launched': sum(launched.values()), 'n_launched_distinct': len(launched),
            'unused_launched_theta': waste, 'n_unused_launched_theta': len(waste),
            'validity_limited_sides_D6': validity_limited, 'edge_limited_D7': [list(x) for x in edge_limited],
            'freeze_gate': ('ROOT_CALL_ORDER step 2 may start (record pinned at step 5)' if run['status'] == 'COMPLETE'
                            else 'NO FREEZE: engine status %s is a result to register, not to retry silently' % run['status']),
        }

    # ---------------------------------------------------------------- resolve / plan / status
    def resolve(self, wave, key_prefix, decision, reason):
        ctx = self.ctx
        wd = self.waves_dir / ('wave_%04d' % int(wave))
        halt = json.loads((wd / 'INFRA_HALT.json').read_text())
        plan = json.loads((wd / 'WAVE_PLAN.json').read_text())
        by_key = {c['key']: c for c in plan['calls']}
        done = []
        self.cache.open(create=True)
        for item in halt['infra']:
            if key_prefix != '*' and not item['key'].startswith(key_prefix):
                continue
            c = by_key[item['key']]
            if item['key'] in self.cache.entries:
                done.append({'key': item['key'], 'note': 'already resolved/cached'})
                continue
            line = {'utc': utc(), 'wave': int(wave), 'key': item['key'], 'decision': decision, 'reason': reason,
                    'infra_reason': item['reason']}
            if decision == 'invalid':
                self.cache.put(key=item['key'], theta=c['theta'], classification='INVALID',
                               failure_class='ROOT_DECLARED_INVALID_AFTER_%s' % item['reason'].split(':')[0],
                               source='ROOT_RESOLUTION', provenance=dict(item['provenance'], root_reason=reason),
                               forward={'valid': False, 'speeds_km_s': {},
                                        'reasons': ['ROOT_DECLARED_INVALID after infrastructure failure %s: %s'
                                                    % (item['reason'], reason)]})
            elif decision == 'retry':
                append_jsonl(self.retry_path, {'key': item['key'], 'utc': utc(), 'wave': int(wave), 'reason': reason})
            else:
                raise OrchestratorError('decision must be invalid or retry')
            append_jsonl(self.resolution_path, line)
            done.append(line)
        return {'status': 'OK', 'resolved': done}

    def plan_only(self):
        self.prepare(create=False)
        pr = self.probe.run(self.cache, 'probe')
        if pr['complete']:
            return {'status': 'OK', 'next_wave': None, 'note': 'probe complete: the next run step is the replay',
                    'alias': self.alias}
        misses = self._dedup(pr['misses'])
        plan = self.make_plan(len(self.wave_dirs()) + 1, misses)
        ok, disk = self.disk_ok(len(misses)) if self.ctx.work_dir.exists() else (None, None)
        return {'status': 'OK', 'alias': self.alias, 'cache_id': self.ctx.cache_id, 'n_cached': len(self.cache.entries),
                'probe': {k: pr[k] for k in ('stop_reason', 'calls', 'hits', 'placeholders', 'families')},
                'next_wave': {'n_calls': plan['n_calls'], 'batches': plan['batches'], 'families': plan['families'],
                              'calls': [{'key': c['key'][:16], 'family': c['family'], 'branch': c['branch'],
                                         'purpose': c['purpose'], 'u': c['u'], 'sibling': c['sibling'],
                                         'spec_sha256': c['spec_sha256'],
                                         'physical': {k: c['spec']['physical'][k] for k in
                                                      ('common_scale_s', 'gamma', 'ell_F_m', 'distance_Mpc')}}
                                        for c in plan['calls']]},
                'disk': disk}


# --------------------------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('command', choices=('plan', 'run', 'resolve', 'status'))
    ap.add_argument('--config', required=True)
    ap.add_argument('--max-waves', type=int, default=None)
    ap.add_argument('--wave', type=int)
    ap.add_argument('--key')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--decision', choices=('invalid', 'retry'))
    ap.add_argument('--reason')
    a = ap.parse_args(argv)
    try:
        ctx = Context(a.config)
        orch = Orchestrator(ctx)
        if a.command == 'plan':
            out = orch.plan_only()
        elif a.command == 'run':
            out = orch.run(max_waves=a.max_waves)
        elif a.command == 'resolve':
            if a.wave is None or a.decision is None or not a.reason or not (a.key or a.all):
                raise OrchestratorError('resolve needs --wave, --decision, --reason and --key PREFIX or --all')
            out = orch.resolve(a.wave, '*' if a.all else a.key, a.decision, a.reason)
        else:
            orch.cache.open(create=False)
            out = {'status': 'OK', 'cache_id': ctx.cache_id, 'n_cached': len(orch.cache.entries),
                   'waves': [p.name for p in orch.wave_dirs()],
                   'final': (ctx.work_dir / 'FINAL_SUMMARY.json').exists(),
                   'infra_halts': [str(p) for p in ctx.work_dir.glob('waves/wave_*/INFRA_HALT.json')]}
    except OrchestratorError as exc:
        out = {'status': 'REFUSED', 'reasons': [str(exc)]}
    print(json.dumps({k: v for k, v in out.items() if k not in ('waves',)} if a.command == 'run' else out,
                     indent=1, sort_keys=True, default=str))
    return EXIT.get(out.get('status'), 3)


if __name__ == '__main__':
    sys.exit(main())
