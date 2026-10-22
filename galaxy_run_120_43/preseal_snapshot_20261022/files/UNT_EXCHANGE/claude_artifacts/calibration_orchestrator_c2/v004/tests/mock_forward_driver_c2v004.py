"""SYNTHETIC mock of the galaxy_m0_forward c2v008 driver, for calibration_orchestrator_c2v004 tests ONLY.
c2v004: byte copy of tests/mock_forward_driver_c2v003.py (8b1706fe) plus two outcomes for the S1 tests:
nonpositive_rotation_all (every Picard pass rotation_positive false) and nonpositive_rotation_history_unreadable (an
earlier pass without a bool rotation_positive); 'nonpositive_rotation' keeps its v003 meaning (positive passes, then a
nonpositive final pass).  Nothing else changed.
Marker: CAL_ORCH_SYNTHETIC_MOCK_DRIVER (the orchestrator refuses synthetic_test without it, C7).

CLI (as c2v008):  mock_forward_driver_c2v004.py run --spec SPEC --outdir OUTDIR
                  mock_forward_driver_c2v004.py dry-run --spec SPEC --report-dir DIR   (no stage, DRYRUN_REPORT.json)
In process:       normalize_spec(spec) -- a REDUCED mirror of c2v008 normalize_spec for DDO154 (strict keys incl.
                  numerics.route_a {column_workers 1..64}, finite numbers, inclination 66, canonical override keys,
                  column_workers 1..12, absolute coefficients path).
Two capability constants: DISTANCE_POLICY ('ANY' = c2v008 normalize_spec; 'REGISTERED_ONLY' = c2v006/7) and
STAGE_BINDING_POLICY ('ANY' = a stage set that admits per-call geometry; 'REGISTERED_ONLY' = c2v008 with the gal_c2v004
stages: run mode BLOCKED 'geometry [GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING]' at D != 4.04, dry-run reports
stage_binding_admits_geometry false).

Run mode computes a 12-row TOY speed vector (the c2v001 toy) and writes the c2v008 call-directory layout with the REAL
c2v008 status / reason vocabulary:
  out/inputs/{call_spec.json, seed_c2v001.json (numerical_inputs.max_iterations 8)}, out/progress.jsonl (stage
  started/finished events, as c2v008 Ctx.event), out/stages/01_route_a/{request.json, attempt_000/{finish.json |
  failure.json}, checkpoint/{IDENTITY.json, attempts/<tok>.end.json, iteration_NNNN/{START.json, COMPLETED.json
  (gas_fourier_residual_J / bound_J in the ['f', hex] encoding), FAILURE.<tok>.json}}}, NN_<tag>_columns_MM/columns/
  finish.json, NN_<tag>_rotation/rotation/failure.json, out/result.json (route_a_outcome, picard_bound_met, passes with
  rotation_positive / max_abs_change_km_s), out/finish.json.  Exit 0 for COMPLETED / COMPLETED_INVALID, else 3.
Outcome selection: env CAL_ORCH_MOCK_CONTROL -> JSON {row_ids, radii_kpc, anchor, sleep_s, route_a_s, rest_s,
force_outcome, outcome_rules [{if, value, outcome}], route_a_iteration_rules, hang_rules, timeline}.
Outcomes: ok | picard_bound_not_met | route_a_budget | route_a_budget_noncontracting | route_a_fsp:<TOKEN> |
route_a_cap_no_end | route_a_nonfinite | route_a_relaxed_nonfinite | route_a_pool_failure | fs_column:<TOKEN> |
rfs_column:<TOKEN> | nonpositive_rotation | nonpositive_rotation_all | nonpositive_rotation_history_unreadable |
colmean_invalid_rotation | enospc | custody | unknown_stage | weird_status |
two_converged_ends | hang.  fs_column outcomes are cured when fs_absolute_overrides['5'][0] == 1.5125e8 (the D7 R1
recovery bracket).  The toy is NOT the project forward; no project data is read; numpy is not used.
"""
import hashlib
import json
import math
import os
import re
import sys
import time
from pathlib import Path

DISTANCE_POLICY = 'ANY'
STAGE_BINDING_POLICY = 'ANY'
SCHEMA_CALL = 'UNT_GALAXY_M0_FORWARD_CALL_C2V001'
SCHEMA_RESULT = 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001'
PHYS_KEYS = ('Eref_J', 'ell_F_m', 'gamma', 'common_scale_s', 'entropy_K_factor', 'distance_Mpc', 'inclination_deg')
REGISTERED_DISTANCE = 4.04
MAX_ITERATIONS = 8
RECOVERY_LO = 151250000.0
KEY_RE = re.compile('0|[1-9][0-9]*')
IDENT = 'f' * 64
TOKEN = '01799999999999999999-1-mock'


class Refusal(ValueError):
    pass


def _num(x, label, positive=True):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(float(x)):
        raise Refusal(label + ' must be a finite number')
    x = float(x)
    if positive and x <= 0:
        raise Refusal(label + ' must be > 0')
    return x


def _strict(d, allowed, label):
    if not isinstance(d, dict):
        raise Refusal(label + ' must be an object')
    extra = set(d) - set(allowed)
    if extra:
        raise Refusal('%s: unknown keys %s' % (label, sorted(extra)))


def normalize_spec(spec):
    _strict(spec, ('schema', 'galaxy', 'label', 'physical', 'coefficients', 'numerics', 'admit', 'reference_compare'), 'spec')
    if spec.get('schema') != SCHEMA_CALL or spec.get('galaxy') != 'DDO154':
        raise Refusal('schema/galaxy')
    phys = spec.get('physical', {})
    _strict(phys, PHYS_KEYS, 'physical')
    p = {k: _num(phys.get(k), k) for k in PHYS_KEYS}
    if p['inclination_deg'] != 66.0:
        raise Refusal('UNSUPPORTED inclination')
    if DISTANCE_POLICY == 'REGISTERED_ONLY' and p['distance_Mpc'] != REGISTERED_DISTANCE:
        raise Refusal('UNSUPPORTED geometry: only the registered distance 4.04 Mpc and inclination 66 deg are supported. '
                      '(MOCK of c2v006/c2v007)')
    coeff = spec.get('coefficients') or {}
    if not isinstance(coeff.get('path'), str) or not os.path.isabs(coeff['path']):
        raise Refusal('coefficients.path must be an absolute path')
    num = spec.get('numerics', {})
    _strict(num, ('composite_grid_spec', 'truncation', 'picard', 'brackets', 'column_workers', 'k_domain', 'route_a'), 'numerics')
    bk = num.get('brackets', {'mode': 'rule'})
    rule = bk.get('rule', {})
    for key in ('fs_absolute_overrides', 'rfs_factor_overrides'):
        for idx, pair in (rule.get(key) or {}).items():
            if not (KEY_RE.fullmatch(idx) and 0 <= int(idx) < 72 and isinstance(pair, list) and len(pair) == 2):
                raise Refusal('%s entries must be "index": [lo, hi]' % key)
    for ps, table in (rule.get('le_factor_overrides') or {}).items():
        if not KEY_RE.fullmatch(ps) or not isinstance(table, dict):
            raise Refusal('le_factor_overrides keys must be pass numbers')
    w = num.get('column_workers', 1)
    if type(w) is not int or not 1 <= w <= 12:
        raise Refusal('column_workers must be int 1..12')
    if 'route_a' in num:
        _strict(num['route_a'], ('column_workers',), 'numerics.route_a')
        n = num['route_a'].get('column_workers', 1)
        if type(n) is not int or not 1 <= n <= 64:
            raise Refusal('numerics.route_a.column_workers must be an int in 1..64')
    adm = spec.get('admit', {}) or {}
    _strict(adm, ('route_a', 'reference', 'body'), 'admit')
    return {'schema': SCHEMA_CALL, 'galaxy': 'DDO154', 'label': spec.get('label', ''), 'physical': p,
            'coefficients': {'path': coeff['path'], 'sha256': coeff.get('sha256')},
            'numerics': json.loads(json.dumps(num)), 'admit': adm, 'reference_compare': bool(spec.get('reference_compare'))}


def weights(ns):
    num = ns['numerics']
    cw = num.get('column_workers', 1)
    ra = (num.get('route_a') or {}).get('column_workers', 1)
    return max(ra, cw), cw


# ----------------------------------------------------------------------------------------------- toy (c2v001 mock)
def toy_coordinates(physical, control):
    a = control['anchor']
    ge = physical['gamma'] / physical['Eref_J']
    return {'x': math.log(ge / a['g0']), 'y': math.log(physical['common_scale_s'] / a['s0']),
            'z': math.log(physical['ell_F_m'] / a['ell0']), 'w': math.log(physical['distance_Mpc'] / 4.04)}


def toy_speeds_from_xyzw(c, control):
    A = 50.0 * math.exp(-0.5 * (c['x'] + c['y'])) * math.exp(0.03 * c['y'])
    r0 = 1.6 * math.exp(0.4 * c['z'])
    out = {}
    for rid, r in zip(control['row_ids'], control['radii_kpc']):
        rp = r * math.exp(c['w'])
        out[rid] = A * (1.0 - math.exp(-rp / r0)) * (1.0 + 0.02 * rp / 6.0)
    return out


def _rule_hit(rule, c):
    var, op = rule['if'].split('_')
    return c[var] < rule['value'] if op == 'lt' else c[var] > rule['value']


def choose(physical, control):
    c = toy_coordinates(physical, control)
    if control.get('force_outcome'):
        oc = control['force_outcome']
    else:
        oc = 'ok'
        for rule in control.get('hang_rules', []):
            if _rule_hit(rule, c):
                oc = 'hang'
                break
        else:
            for rule in control.get('outcome_rules', []):
                if _rule_hit(rule, c):
                    oc = rule['outcome']
                    break
    k = control.get('force_converged_iteration', 4)
    for rule in control.get('route_a_iteration_rules', []):
        if _rule_hit(rule, c):
            k = int(rule['converged_iteration'])
            break
    return oc, k, c


# ----------------------------------------------------------------------------------------------- layout writers
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _wx(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return hashlib.sha256(raw).hexdigest()


def ckf(x):
    return ['f', float(x).hex()]


class Progress:
    def __init__(self, out, control, w):
        self.f = open(out / 'progress.jsonl', 'x')
        self.t0 = time.monotonic()
        self.control, self.w = control, w

    def event(self, **kw):
        kw['elapsed_seconds'] = time.monotonic() - self.t0
        self.f.write(json.dumps(kw) + '\n')
        self.f.flush()

    def timeline(self, event, weight):
        tl = self.control.get('timeline')
        if tl:
            with open(tl, 'a') as fh:
                fh.write(json.dumps({'t': time.time(), 'event': event, 'pid': os.getpid(), 'weight': weight}) + '\n')


def residual_schedule(kind, k):
    """residual/bound per iteration (bound fixed at 2.7e56 J, the anchor's order of magnitude)."""
    if kind in ('converged', 'two_converged'):
        return [0.9 * 0.48 ** (i - k) for i in range(k + 1)]
    if kind in ('budget', 'cap_no_end'):
        return [400.0 * 0.48 ** i for i in range(MAX_ITERATIONS)]
    if kind == 'budget_noncontracting':
        return [20.0, 12.0, 9.0, 8.0, 8.2, 8.5, 8.7, 9.0]
    return [5.0 * 0.6 ** i for i in range(k + 1)]


def write_route_a(out, seed_path, kind, k, token_msg=None):
    """kind: converged | budget | budget_noncontracting | fsp | cap_no_end | nonfinite | relaxed_nonfinite | pool |
    two_converged.  Returns the iterations written."""
    sd = out / 'stages' / '01_route_a'
    cp, att = sd / 'checkpoint', sd / 'attempt_000'
    _wx(sd / 'request.json', {'name': 'route_a', 'kind': 'route_a', 'argv': ['--seed', str(seed_path), '--seed-sha256',
                                                                            sha(seed_path), '--outdir', str(att)]})
    _wx(cp / 'IDENTITY.json', {'identity_sha256': IDENT, 'kind': 'identity', 'mock': True})
    sched = residual_schedule(kind, k)
    if kind in ('converged', 'two_converged'):
        its, conv, outcome = list(range(k + 1)), k, 'CONVERGED_FINITE_FIXED_POINT'
    elif kind in ('budget', 'budget_noncontracting', 'cap_no_end'):
        its, conv, outcome = list(range(MAX_ITERATIONS)), None, 'ITERATION_BUDGET_EXHAUSTED'
    elif kind == 'fsp':
        its, conv, outcome = list(range(k + 1)), None, 'FAILED_SOURCE_PREPARATION'
    elif kind in ('nonfinite', 'relaxed_nonfinite', 'pool'):
        its, conv, outcome = list(range(k + 1)), None, None
    else:
        raise ValueError(kind)
    bound = 2.7e56
    for i in its:
        d = cp / ('iteration_%04d' % i)
        _wx(d / 'START.json', {'kind': 'iteration_start', 'iteration': i, 'identity_sha256': IDENT, 'payload_sha256': 'a' * 64})
        last = i == its[-1]
        if kind == 'fsp' and last:
            _wx(d / ('FAILURE.%s.json' % TOKEN), {'kind': 'failure', 'iteration': i, 'column_index': 17,
                                                  'failure': ['d', [['message', ['s', '%s; radius_m=1.0e19; side=1' % token_msg]],
                                                                    ['type', ['s', 'ValueError']]]]})
            continue
        if kind in ('nonfinite', 'relaxed_nonfinite', 'pool') and last:
            continue
        _wx(d / 'COMPLETED.json', {'kind': 'iteration_completed', 'iteration': i, 'identity_sha256': IDENT,
                                   'iteration_start_sha256': 'a' * 64, 'attempt': TOKEN,
                                   'converged': bool(conv is not None and i == conv),
                                   'gas_fourier_residual_J': ckf(sched[i] * bound), 'bound_J': ckf(bound)})
    if kind in ('converged', 'budget', 'budget_noncontracting', 'fsp', 'two_converged'):
        _wx(cp / 'attempts' / (TOKEN + '.end.json'), {'kind': 'attempt_end', 'identity_sha256': IDENT, 'attempt': TOKEN,
                                                      'outcome': outcome})
        if kind == 'two_converged':
            _wx(cp / 'attempts' / (TOKEN + 'b.end.json'), {'kind': 'attempt_end', 'identity_sha256': IDENT,
                                                           'attempt': TOKEN + 'b', 'outcome': outcome})
        _wx(att / 'finish.json', {'status': 'RETURNED_ACTUAL_RESULT'})
    elif kind == 'cap_no_end':
        _wx(att / 'finish.json', {'status': 'RETURNED_ACTUAL_RESULT'})
    elif kind == 'nonfinite':
        _wx(att / 'failure.json', {'status': 'FAILED', 'type': 'ValueError', 'message': 'Nonfinite coupling residual'})
    elif kind == 'relaxed_nonfinite':
        _wx(att / 'failure.json', {'status': 'FAILED', 'type': 'ValueError', 'message': 'relaxed gas: nonfinite'})
    elif kind == 'pool':
        _wx(att / 'failure.json', {'status': 'FAILED', 'type': 'ColumnPoolError', 'message': 'UNSHIPPABLE bare code object'})
    return its, outcome


def outcome_record(its, outcome, conv_k=None, failure=None):
    rec = {'result_path': '<mock>', 'outcome': outcome, 'converged_finite_fixed_point': conv_k is not None,
           'predictions_available': conv_k is not None, 'iterations_completed': its if conv_k is not None or failure is None
           else its[:-1], 'last_completed_iteration': None, 'reason': None}
    if conv_k is not None:
        rec.update(classification='CONVERGED', converged_iteration=conv_k)
    else:
        rec.update(classification='ROUTE_A_NO_FIXED_POINT', converged_iteration=None)
    if failure:
        rec['failure'] = failure
    return rec


def write_columns(out, n, tag, failures, nrun=2):
    for j in range(nrun):
        d = out / 'stages' / ('%02d_%s_columns_%02d' % (n + j, tag, j))
        fl = [f for f in failures if f['index'] % nrun == j]
        _wx(d / 'columns' / 'finish.json', {'status': 'LAGGED_FREE_SURFACE_COLUMNS_ONLY', 'completed': [], 'failures': fl})
    return n + nrun


def passes_ok(ns, bound_met=True):
    pc = (ns['numerics'].get('picard') or {})
    bound = pc.get('speed_change_bound_km_s')
    P = pc.get('passes', 3)
    n = min(3, P) if bound_met else P
    out = []
    for p in range(1, n + 1):
        rec = {'pass': p, 'rotation_positive': True, 'column_failures': [],
               'column_mean': {'path': '<mock>', 'sha256': 'b' * 64, 'status': 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'}}
        if p > 1:
            if bound is None:
                rec['max_abs_change_km_s'] = 0.5 / p
            else:
                rec['max_abs_change_km_s'] = (bound * 0.5 if p == n else bound * 3.0) if bound_met else bound * 3.0
        out.append(rec)
    return out, bound


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == 'dry-run':
        assert len(sys.argv) == 6 and sys.argv[2] == '--spec' and sys.argv[4] == '--report-dir'
        return dry_run(sys.argv[3], sys.argv[5])
    assert len(sys.argv) == 6 and cmd == 'run' and sys.argv[2] == '--spec' and sys.argv[4] == '--outdir'
    out = Path(os.path.abspath(sys.argv[5]))
    if out.exists():
        print('REFUSED: outdir exists', file=sys.stderr)
        return 2
    out.mkdir(parents=True)
    raw = Path(sys.argv[3]).read_bytes()
    (out / 'inputs').mkdir()
    (out / 'inputs' / 'call_spec.json').write_bytes(raw)
    control = json.loads(Path(os.environ['CAL_ORCH_MOCK_CONTROL']).read_text())
    result = {'schema': SCHEMA_RESULT, 'call_spec_sha256': hashlib.sha256(raw).hexdigest(), 'driver_sha256': sha(__file__),
              'accepted_for_calibration': False, 'scored': False, 'valid': False, 'reasons': [], 'mock': True}
    status = 'FAILED'
    prog = None
    try:
        spec = json.loads(raw)
        try:
            ns = normalize_spec(spec)
        except Refusal as exc:
            status = 'REFUSED'
            result['reasons'].append(str(exc))
            raise StopIteration
        peak, after = weights(ns)
        prog = Progress(out, control, (peak, after))
        prog.timeline('start', peak)
        ph = ns['physical']
        result['normalized_spec'] = ns
        oc, k, c = choose(ph, control)
        if STAGE_BINDING_POLICY == 'REGISTERED_ONLY' and ph['distance_Mpc'] != REGISTERED_DISTANCE:
            status = 'BLOCKED'
            result['reasons'].append('geometry [GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING]: distance_Mpc %r != registered 4.04 '
                                     '(MOCK of c2v008 L2184-2190); no stage is run.' % ph['distance_Mpc'])
            result['geometry'] = {'distance_Mpc': ph['distance_Mpc'], 'stage_admission_probe': {'admitted': False}}
            raise StopIteration
        seed_path = out / 'inputs' / 'seed_c2v001.json'
        _wx(seed_path, {'numerical_inputs': {'max_iterations': MAX_ITERATIONS, 'Eref_J': ph['Eref_J'] * ph['common_scale_s']}})
        prog.event(stage='route_a', event='started', pid=os.getpid())
        time.sleep(float(control.get('route_a_s', float(control.get('sleep_s', 0.3)) / 2)))
        if oc == 'hang':
            time.sleep(3600)
        fs_over = ((ns['numerics'].get('brackets') or {}).get('rule') or {}).get('fs_absolute_overrides') or {}
        if oc.startswith('fs_column:') and (fs_over.get('5') or [None])[0] == RECOVERY_LO:
            oc = 'ok'
        result['passes'] = []

        def route_a_done():
            prog.timeline('phase', after)
            prog.event(stage='route_a', event='finished', exit_code=0)
            prog.event(stage='reference', event='started')
            time.sleep(float(control.get('rest_s', float(control.get('sleep_s', 0.3)) / 2)))

        if oc in ('ok', 'picard_bound_not_met'):
            its, outc = write_route_a(out, seed_path, 'converged', k)
            result['route_a_outcome'] = outcome_record(its, outc, conv_k=k)
            route_a_done()
            result['passes'], bound = passes_ok(ns, bound_met=(oc == 'ok'))
            result['speeds_km_s'] = toy_speeds_from_xyzw(c, control)
            chg = result['passes'][-1].get('max_abs_change_km_s')
            result['picard_bound_met'] = None if bound is None or chg is None else bool(chg <= bound)
            result['valid'] = True
            result['final_pass'] = result['passes'][-1]['pass']
            status = 'COMPLETED'
        elif oc in ('route_a_budget', 'route_a_budget_noncontracting'):
            its, outc = write_route_a(out, seed_path, 'budget' if oc == 'route_a_budget' else 'budget_noncontracting', k)
            result['route_a_outcome'] = outcome_record(its, outc)
            status = 'ROUTE_A_NO_FIXED_POINT'
            result['reasons'].append('ROUTE_A_NO_FIXED_POINT: route-A outcome ITERATION_BUDGET_EXHAUSTED after iterations %s '
                                     '(a result at this parameter point, not a tooling gap)' % its)
        elif oc.startswith('route_a_fsp:'):
            tok = oc.split(':', 1)[1]
            its, outc = write_route_a(out, seed_path, 'fsp', k, token_msg=tok)
            fail = {'type': 'ValueError', 'message': '%s; radius_m=1.0e19; side=1' % tok, 'iteration': its[-1],
                    'column_index': 17, 'stage': 'hi_column'}
            result['route_a_outcome'] = outcome_record(its, outc, failure=fail)
            status = 'ROUTE_A_NO_FIXED_POINT'
            result['reasons'].append('ROUTE_A_NO_FIXED_POINT: route-A outcome FAILED_SOURCE_PREPARATION after iterations %s'
                                     % its[:-1])
        elif oc == 'route_a_cap_no_end':
            its, outc = write_route_a(out, seed_path, 'cap_no_end', k)
            result['route_a_outcome'] = outcome_record(its, outc)
            status = 'REFUSED'
            result['reasons'].append('ROUTE_A_ATTEMPT_NOT_OF_THIS_CHECKPOINT: attempt token %r has no %s/attempts/<token>.end.json'
                                     % (TOKEN, out / 'stages' / '01_route_a' / 'checkpoint'))
        elif oc == 'two_converged_ends':
            its, outc = write_route_a(out, seed_path, 'two_converged', k)
            result['route_a_outcome'] = outcome_record(its, outc, conv_k=k)
            status = 'BLOCKED'
            result['reasons'].append('ROUTE_A_ITERATION_AMBIGUOUS: 2 attempt_end records report CONVERGED_FINITE_FIXED_POINT '
                                     '(exactly one required)')
        elif oc in ('route_a_nonfinite', 'route_a_relaxed_nonfinite', 'route_a_pool_failure'):
            write_route_a(out, seed_path, {'route_a_nonfinite': 'nonfinite', 'route_a_relaxed_nonfinite': 'relaxed_nonfinite',
                                           'route_a_pool_failure': 'pool'}[oc], k)
            status = 'FAILED_AT_STAGE'
            result['reasons'].append("stage(s) exited nonzero: ['route_a']")
        elif oc.startswith('fs_column:'):
            its, outc = write_route_a(out, seed_path, 'converged', k)
            result['route_a_outcome'] = outcome_record(its, outc, conv_k=k)
            route_a_done()
            tokm = oc.split(':', 1)[1]
            fails = [{'index': i, 'type': 'ValueError', 'message': '%s: supply a resolved compact-support bracket' % tokm
                      if tokm == 'MASS_ENTHALPY_NOT_BRACKETED' else '%s: mock' % tokm} for i in (5, 6, 50)]
            n = write_columns(out, 5, 'fs', fails)
            _wx(out / 'stages' / ('%02d_fs_rotation' % n) / 'rotation' / 'failure.json',
                {'type': 'ValueError', 'message': 'Missing complete72 successful columns'})
            status = 'FAILED_AT_STAGE'
            result['reasons'].append("stage(s) exited nonzero: ['fs_rotation']")
        elif oc.startswith('rfs_column:'):
            its, outc = write_route_a(out, seed_path, 'converged', k)
            result['route_a_outcome'] = outcome_record(its, outc, conv_k=k)
            route_a_done()
            tokm = oc.split(':', 1)[1]
            write_columns(out, 5, 'fs', [])
            write_columns(out, 11, 'rfs', [{'index': 70, 'type': 'ValueError', 'message': '%s: numerical search limit is '
                                            'not an edge' % tokm}])
            status = 'FAILED_AT_STAGE'
            result['reasons'].append('rfs column(s) [70] failed; no bracket source')
        elif oc in ('nonpositive_rotation', 'nonpositive_rotation_all', 'nonpositive_rotation_history_unreadable',
                    'colmean_invalid_rotation'):
            its, outc = write_route_a(out, seed_path, 'converged', k)
            result['route_a_outcome'] = outcome_record(its, outc, conv_k=k)
            route_a_done()
            ps, bound = passes_ok(ns, bound_met=False)
            if oc in ('nonpositive_rotation_all', 'nonpositive_rotation_history_unreadable'):
                for q in ps:
                    q.update(rotation_positive=False, column_mean={'path': '<mock>', 'sha256': 'c' * 64,
                                                                   'status': 'FAILED_NO_PREPARATION_OUTPUT'},
                             column_mean_failure={'type': 'ValueError', 'message': 'Complete positive lagged preparation required'})
                    q.pop('max_abs_change_km_s', None)
                if oc == 'nonpositive_rotation_history_unreadable' and len(ps) > 1:
                    ps[0].pop('rotation_positive', None)
                result['reasons'].append("final column mean did not return 12 rows: {'status': 'FAILED_NO_PREPARATION_OUTPUT'}")
            elif oc == 'nonpositive_rotation':
                ps[-1].update(rotation_positive=False, column_mean={'path': '<mock>', 'sha256': 'c' * 64,
                                                                    'status': 'FAILED_NO_PREPARATION_OUTPUT'},
                              column_mean_failure={'type': 'ValueError', 'message': 'Complete positive lagged preparation required'})
                ps[-1].pop('max_abs_change_km_s', None)
                result['reasons'].append("final column mean did not return 12 rows: {'status': 'FAILED_NO_PREPARATION_OUTPUT'}")
            else:
                ps[-1].update(column_mean={'path': '<mock>', 'sha256': 'c' * 64, 'status': 'FAILED_NO_PREPARATION_OUTPUT'},
                              column_mean_failure={'type': 'ValueError', 'message': 'Invalid finite positive rotation'})
                ps[-1].pop('max_abs_change_km_s', None)
                result['reasons'].append("final column mean did not return 12 rows: {'status': 'FAILED_NO_PREPARATION_OUTPUT'}")
            result['passes'] = ps
            status = 'COMPLETED_INVALID'
        elif oc == 'enospc':
            status = 'FAILED'
            result['reasons'].append('OSError: [Errno 28] No space left on device')
        elif oc == 'custody':
            write_route_a(out, seed_path, 'converged', k)
            status = 'BLOCKED'
            result['reasons'].append('checkpoint identity self-hash mismatch')
        elif oc == 'unknown_stage':
            its, outc = write_route_a(out, seed_path, 'converged', k)
            result['route_a_outcome'] = outcome_record(its, outc, conv_k=k)
            status = 'FAILED_AT_STAGE'
            result['reasons'].append('something unexpected happened in a stage: MOCK_NEW_REASON')
        elif oc == 'weird_status':
            status = 'WEIRD_NEW_STATUS'
            result['reasons'].append('MOCK: a status c2v008 never emits')
        else:
            raise ValueError('unknown mock outcome %r' % oc)
    except StopIteration:
        pass
    except ValueError as exc:
        status = 'FAILED'
        result['reasons'].append('%s: %s' % (type(exc).__name__, exc))
    result['status'] = status
    if control.get('extra_result'):            # deciding-test fixtures: fields merged into result.json before it is written
        _merge(result, control['extra_result'])
        for k in control.get('drop_result_keys') or []:
            result.pop(k, None)
    rsha = _wx(out / 'result.json', result)
    _wx(out / 'finish.json', {'status': status, 'valid': result['valid'], 'result_path': str(out / 'result.json'),
                              'result_sha256': rsha, 'reasons': result['reasons'], 'retries': 0})
    if prog is not None:
        prog.timeline('finish', 0)
        prog.f.close()
    return 0 if status in ('COMPLETED', 'COMPLETED_INVALID') else 3


def _merge(dst, src):
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _merge(dst[k], v)
        else:
            dst[k] = v


def dry_run(spec_path, report_dir):
    rd = Path(os.path.abspath(report_dir))
    if rd.exists():
        print('REFUSED: report dir exists', file=sys.stderr)
        return 2
    rd.mkdir(parents=True)
    raw = Path(spec_path).read_bytes()
    ns = normalize_spec(json.loads(raw))
    D = ns['physical']['distance_Mpc']
    summary = {'binding_blockers': [], 'pin_problems': [], 'refusals_beyond_pending_inputs': [],
               'remaining_refusals_by_class': {'PRODUCED_BY_THIS_CALL': ['custody.checkpoint_identity_sha256']},
               'stages_planned': 12}
    if D != REGISTERED_DISTANCE:
        ok = STAGE_BINDING_POLICY == 'ANY'
        summary['geometry'] = {'distance_Mpc': D, 'stage_binding_admits_geometry': ok,
                               'refused_by': {} if ok else {'reference': 'source.profile (MOCK)'}}
        if not ok:
            summary['remaining_refusals_by_class']['GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING'] = ['geometry']
            summary['refusals_beyond_pending_inputs'] = ['GEOMETRY_NOT_ADMITTED_BY_STAGE_BINDING: geometry']
    _wx(rd / 'DRYRUN_REPORT.json', {'schema': 'MOCK_DRYRUN_REPORT', 'call_spec_sha256': hashlib.sha256(raw).hexdigest(),
                                    'driver_sha256': sha(__file__), 'normalized_spec': ns, 'executed_stages': 0,
                                    'summary': summary})
    return 0


if __name__ == '__main__':
    sys.exit(main())
