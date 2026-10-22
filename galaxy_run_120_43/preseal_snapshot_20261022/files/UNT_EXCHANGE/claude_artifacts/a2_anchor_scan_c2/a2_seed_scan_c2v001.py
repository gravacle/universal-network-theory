"""INERT fixed-source gamma-factor seed scan for a declared coefficient grid (Claude2 lane, c2v001).

Versioned wrapper/copy of the reviewed root scan ddo_fixed_source_gamma_scan_v004.py (fc8abd7b).
NOT a calibration, fit, velocity prediction or gas equilibrium. Importing this module does nothing.

Modes (scan spec field `mode`):
  g2_route_a_kernel        Build the iteration-0 source and the complete kernel EXACTLY as the route-B
                           driver's route-A stage does for the declared coefficient grid {path, sha256}:
                           pinned driver normalize_spec/per_call_seed -> seed numerical_inputs (G2, cube),
                           prep V007 with the driver's COEFFICIENT/COEFFICIENT_SHA patch (non-default grid
                           only), solver fixed+gas iteration-0 source, scalar-lapse cache facade over
                           quadrature v005 (the route-A Fourier module). Per gamma factor f the kernel is
                           rebuilt at every node with gamma = f * gamma_seed and Eref = Eref_seed (v004 rule).
                           v004 reads are repeated verbatim (641-row failure column via line v001 + metric
                           evaluator, 96 DDO midplane radial diagnostics via evaluate_prepared).  Added: the
                           same legacy read and the route-A stable read (line v002 lapse_difference) on the
                           route-A search roster for a radius sweep of columns.
  v004_ir64_reproduction   Executes the pinned v004 worker itself with the arguments of the saved launch
                           (IR64 source package, V004 coefficients), then the analysis below, then a
                           bitwise comparison against the saved scan and seed V002.
  synthetic_selftest       No project computation; exercises analysis/selection/output files (monitor test).

Declared seed rule (seed V002 seed_method/scope), applied per factor, in list order:
  inward    : all 96 sampled signed c^2 R dlnN/dR > 0 (radial_available == 96)
  scale     : s = median(96 values) / v_cal^2, v_cal = median observed speed of the pinned
              calibration region file (= 43300 m/s, asserted)
  margin    : estimated two-sided enthalpy margin after amplitude normalization at the failure
              column: for each side, max over sampled 0 < +-z <= search_limit of (logN/N0)/s minus
              threshold log1p(G sig^2/((G-1) c^2)) must be > 0.  (Fields scale exactly as 1/s at
              fixed source because K = Eref*native + gamma*EH; the log read is linear to O(1e-9).)
  candidate : Eref' = s*Eref_eval, gamma' = s*gamma_eval, ell_F unchanged.
The first factor meeting the rule is selected; the next one is the alternative.  If none meets it,
nothing is selected and that is a registered result.

CLI:
  a2_seed_scan_c2v001.py run      --spec SCAN_SPEC.json --outdir OUT     (project computation; root launches)
  a2_seed_scan_c2v001.py dry-run  --spec SCAN_SPEC.json --outdir OUT     (pins/headers/plan only)
  a2_seed_scan_c2v001.py analyze-saved --scan-dir DIR --out FILE.json    (read-only on DIR)
  a2_seed_scan_c2v001.py replay-v004-reads --candidate-dir D --outdir O --launch L --launch-sha256 H
                                                (reads only, saved prepared waves; ~1 min; root launches)
"""
import argparse
import hashlib
import importlib.util
import json
import math
import statistics
import sys
import time
from pathlib import Path

SCHEMA = 'UNT_A2_SEED_SCAN_CALL_C2V001'
RESULT_SCHEMA = 'UNT_A2_SEED_SCAN_RESULT_C2V001'
R = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
HR = R / 'helpers/recovered_packet_audit'
HC = R / 'helpers/coefficient_method'
C1 = R / 'CODEX1'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
PINS = {
    'driver': (EX / 'galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py', '75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22'),
    'v004_worker': (HR / 'ddo_fixed_source_gamma_scan_v004.py', 'fc8abd7b3129784a4cb8eb85c21265c32d1b9fd4296d7dd1aa6334384fad3d7d'),
    'prep': (HC / 'ddo_actual_initial_source_preparation_v007.py', 'ac905597b1aa06da3a0178bfa629f6256b78cc87e8b1b05fcea22b3f6df25a42'),
    'cache': (HR / 'owned_scalar_lapse_inverse_cache_v001.py', '7b9816aea218d638c2eece184df22e29ca18b68547f3d04193780c2eff96a529'),
    'base': (HR / 'owned_physical_fourier_metric_quadrature_v005.py', '7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491'),
    'line_v001': (HR / 'owned_fixed_xy_fourier_line_v001.py', '5c0ab4f6dcd14b79d5ec012f3eee6f58704b8e2982657ac58862b94b9429dfb4'),
    'line_v002': (HR / 'owned_fixed_xy_fourier_line_v002.py', '3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18'),
    'metric': (HC / 'owned_fourier_physical_metric_evaluator_v002.py', '8f01bd5b352a5ec5f74f6c19ed8ad4295c55ff80ba895dac93628f62bace73a4'),
    'complex': (HC / 'owned_complex_symbol_metric_binding_v002.py', '701095f9c3cbe90f28605ef3676ae7889dbaa6e4686630c424f79a1feea9cdcc'),
    'solver': (EX / 'resumable_coupled_gas_0422/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py', '44d9c23c47d6beb52b7539802fcf0f284c1a2c7eea7662536f04b184523e3644'),
    'hi_v003': (HR / 'hi_two_sided_free_boundary_v003.py', 'b176c7a604079027cbca565aae81d0ec69ea9b3f47430d7e58c03cd21a7838f9'),
    'seed_v002': (C1 / 'DDO154_STABLE_CACHED_COUPLED_TRIAL_SEED_V002.json', '694eaaaab38547a369ac85c3c3d0b5550d8878753ccafe7bc0e5cdcb79be6680'),
}
V004_COEFF = (C1 / 'PROVISIONAL_L4_COEFFICIENT_FREEZE_V001/coefficients.npz', 'fe5a2f065dec8f120c573eeeb6edc0a24a945d2a0fd70e3f29a66cb986e53e4f')
DDO_RADII_KPC = (.49, .99, 1.48, 1.97, 2.47, 2.96, 3.46, 3.95, 4.44, 4.94, 5.43, 5.92)  # v004 roster, verbatim
DECLARED_V_CAL_M_S = 43300.0
SPEC_KEYS = ('schema', 'label', 'mode', 'coefficients', 'route_b_template', 'route_a_reference', 'failure_column_index',
             'gamma_factors', 'sweep', 'calibration_region', 'keep_weighted_responses', 'v004_launch', 'synthetic')
COST_PER_FACTOR_S_G2 = 260.0     # 150 s unit solve (A2 route-A receipt) + eigen diagnostics + reads; estimate
PREP_COST_S_G2 = 60.0
OUTPUT_PER_FACTOR_BYTES_G2 = 700 * 2 ** 20


class Refusal(Exception):
    pass


# ----------------------------------------------------------------------------- utilities
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def serial(x):
    import numpy as np
    if isinstance(x, np.ndarray):
        return serial(x.tolist())
    if isinstance(x, np.generic):
        return serial(x.item())
    if isinstance(x, complex):
        return dict(real=x.real, imag=x.imag)
    if isinstance(x, Path):
        return str(x)
    if isinstance(x, float) and not math.isfinite(x):
        return None if math.isnan(x) else ('+inf' if x > 0 else '-inf')
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def write_x(path, obj, indent=1):
    """Exclusive create; returns sha256 of the written bytes."""
    raw = (json.dumps(serial(obj), indent=indent, allow_nan=False) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
        f.flush()
    return sha256_bytes(raw)


def verified(key_or_pair):
    path, sha = PINS[key_or_pair] if isinstance(key_or_pair, str) else key_or_pair
    path = Path(path)
    if not path.is_file() or sha256_file(path) != sha:
        raise Refusal('pin mismatch or missing: %s' % path)
    return path, sha


def load_module(key, tag='a2scan_'):
    path, sha = verified(key)
    raw = path.read_bytes()
    if sha256_bytes(raw) != sha:
        raise Refusal('pin changed while loading: %s' % path)
    spec = importlib.util.spec_from_file_location(tag + path.stem, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if sha256_file(path) != sha:
        raise Refusal('pin changed after loading: %s' % path)
    return m


def threshold_v004(g, sig, c):
    return math.log1p(g * sig * sig / ((g - 1) * c * c))


def threshold_hi_v003(g, sig, c):
    h0 = g * sig * sig / (g - 1)
    return math.log1p(h0 / (c * c))


def search_roster(step, limit):
    """Positive distances visited by hi_two_sided_free_boundary_v003.root (same accumulation)."""
    if not (math.isfinite(step) and math.isfinite(limit) and step > 0 and limit > 0):
        raise ValueError('positive finite step/limit required')
    out, distance = [], 0.0
    while distance < limit:
        nd = min(limit, distance + step)
        if nd <= distance:
            raise ValueError('SEARCH_FLOAT_RESOLUTION_LIMIT')
        distance = nd
        out.append(distance)
    return out


def calibration_speed(region):
    path, sha = Path(region['path']), region['sha256']
    if not path.is_file() or sha256_file(path) != sha:
        raise Refusal('calibration region pin mismatch')
    d = json.loads(path.read_text())
    v = statistics.median([float(r['observed_speed_km_s']) for r in d['rows']]) * 1000.0
    if len(d['rows']) != 12 or v != DECLARED_V_CAL_M_S:
        raise Refusal('declared calibration median must be exactly 43300 m/s from the 12-row region; got %r' % v)
    return v


# ----------------------------------------------------------------------------- the declared rule (pure)
def side_margin(z_m, lr, s, threshold, limit, sign):
    """max over 0 < sign*z <= limit of lr/s - threshold, plus first sampled crossing.  Unavailable lr
    (None/nan) rows are skipped, as v004 skips unavailable vertical rows."""
    best, first, n = None, None, 0
    pairs = sorted(((abs(z), z, v) for z, v in zip(z_m, lr)
                    if v is not None and math.isfinite(v) and 0 < sign * z <= limit), key=lambda t: t[0])
    for _, z, v in pairs:
        n += 1
        m = v / s - threshold
        best = m if best is None or m > best else best
        if first is None and m >= 0:
            first = z
    return {'margin': best, 'first_crossing_z_m': first, 'samples': n}


def two_sided(z_m, lr, s, threshold, limit):
    plus = side_margin(z_m, lr, s, threshold, limit, +1)
    minus = side_margin(z_m, lr, s, threshold, limit, -1)
    ok = plus['margin'] is not None and minus['margin'] is not None and plus['margin'] > 0 and minus['margin'] > 0
    two = None if (plus['margin'] is None or minus['margin'] is None) else min(plus['margin'], minus['margin'])
    return {'plus': plus, 'minus': minus, 'two_sided_margin': two, 'positive': ok}


def apply_rule(radial, v_cal):
    """Inward count and scale exactly as the seed procedure: s = median(96 values)/v_cal^2."""
    finite = [v for v in radial if v is not None and math.isfinite(v)]
    inward = sum(v > 0 for v in finite)
    out = {'radial_available': len(finite), 'radial_inward_positive': inward,
           'radial_outward_or_zero': len(finite) - inward,
           'radial_min': min(finite, default=None), 'radial_max': max(finite, default=None),
           'radial_median': statistics.median(finite) if finite else None}
    out['all_96_inward'] = len(finite) == 96 and len(radial) == 96 and inward == 96
    s = None
    if out['all_96_inward']:
        s = out['radial_median'] / (v_cal * v_cal)
        if not (math.isfinite(s) and s > 0):
            s = None
    out['scale_s'] = s
    return out


def select(candidates):
    """candidates: ordered list of dicts with 'factor' and 'rule_pass'.  First and next passing."""
    passing = [c for c in candidates if c.get('rule_pass') is True]
    return {'first': passing[0]['factor'] if passing else None,
            'next': passing[1]['factor'] if len(passing) > 1 else None,
            'passing_factors': [c['factor'] for c in passing],
            'status': 'SELECTED' if passing else 'NO_CANDIDATE_MEETS_DECLARED_RULE'}


def candidate_seed(base, factor, s):
    E, g, ell = base['Eref_J'], base['gamma'], base['ell_F_m']
    g_eval = g * factor
    return {'factor': factor, 'Eref_eval_J': E, 'gamma_eval': g_eval, 'ell_F_m': ell, 'scale_s': s,
            'Eref_J': s * E, 'gamma': s * g_eval, 'gamma_over_Eref': (s * g_eval) / (s * E)}


# ----------------------------------------------------------------------------- spec
def _hex64(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def _pathsha(d, label):
    if not isinstance(d, dict) or set(d) != {'path', 'sha256'} or not isinstance(d['path'], str) or not _hex64(d['sha256']):
        raise Refusal(label + ': {path, sha256} required')
    return {'path': d['path'], 'sha256': d['sha256']}


def normalize_scan_spec(spec):
    if not isinstance(spec, dict):
        raise Refusal('spec must be an object')
    extra = set(spec) - set(SPEC_KEYS)
    if extra:
        raise Refusal('unknown keys %s' % sorted(extra))
    if spec.get('schema') != SCHEMA:
        raise Refusal('schema must be ' + SCHEMA)
    mode = spec.get('mode')
    if mode not in ('g2_route_a_kernel', 'v004_ir64_reproduction', 'synthetic_selftest'):
        raise Refusal('mode must be g2_route_a_kernel, v004_ir64_reproduction or synthetic_selftest')
    f = spec.get('gamma_factors')
    if not isinstance(f, list) or not f or any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in f):
        raise Refusal('gamma_factors: nonempty list of numbers required')
    f = [float(v) for v in f]
    if any(not math.isfinite(v) or v <= 0 for v in f):
        raise Refusal('gamma_factors must be finite and > 0')
    if len(set(f)) != len(f):
        raise Refusal('duplicate gamma factors')
    out = {'schema': SCHEMA, 'label': str(spec.get('label', '')), 'mode': mode, 'gamma_factors': f,
           'calibration_region': _pathsha(spec.get('calibration_region'), 'calibration_region')}
    if mode == 'g2_route_a_kernel':
        out['coefficients'] = _pathsha(spec.get('coefficients'), 'coefficients')
        out['route_b_template'] = _pathsha(spec.get('route_b_template'), 'route_b_template')
        ref = spec.get('route_a_reference')
        if ref is not None:
            if not isinstance(ref, dict) or set(ref) != {'attempt_directory', 'result_sha256'} or not _hex64(ref['result_sha256']):
                raise Refusal('route_a_reference: {attempt_directory, result_sha256} or null')
        out['route_a_reference'] = ref
        fc = spec.get('failure_column_index')
        if fc is not None and (type(fc) is not int or fc < 0):
            raise Refusal('failure_column_index: nonnegative int or null')
        if fc is None and ref is None:
            raise Refusal('failure column required: give route_a_reference or failure_column_index')
        out['failure_column_index'] = fc
        sw = spec.get('sweep', {'columns': 'failure_phi'})
        if not isinstance(sw, dict) or set(sw) - {'columns'}:
            raise Refusal('sweep: {columns}')
        cols = sw.get('columns', 'failure_phi')
        if cols != 'failure_phi' and not (isinstance(cols, list) and all(type(i) is int and i >= 0 for i in cols)
                                          and len(set(cols)) == len(cols) and len(cols) <= 576):
            raise Refusal('sweep.columns: "failure_phi" or a list of distinct column indices')
        out['sweep'] = {'columns': cols}
        k = spec.get('keep_weighted_responses', True)
        if type(k) is not bool:
            raise Refusal('keep_weighted_responses must be bool')
        out['keep_weighted_responses'] = k
        for key in ('v004_launch', 'synthetic'):
            if spec.get(key) is not None:
                raise Refusal(key + ' not used in this mode')
    elif mode == 'v004_ir64_reproduction':
        out['v004_launch'] = _pathsha(spec.get('v004_launch'), 'v004_launch')
        out['route_b_template'] = _pathsha(spec.get('route_b_template'), 'route_b_template')
        for key in ('coefficients', 'route_a_reference', 'failure_column_index', 'sweep', 'synthetic'):
            if spec.get(key) is not None:
                raise Refusal(key + ' not used in reproduction mode (v004 fixes them)')
        out['keep_weighted_responses'] = True
    else:
        syn = spec.get('synthetic')
        if not isinstance(syn, dict) or set(syn) - {'radial_by_factor', 'lr_peak_by_factor', 'sleep_s'}:
            raise Refusal('synthetic: {radial_by_factor, lr_peak_by_factor, sleep_s}')
        out['synthetic'] = syn
    return out


# ----------------------------------------------------------------------------- route-B call specs
def build_route_b_call(drv, template_obj, coefficients, seed_row, label):
    call = json.loads(json.dumps(template_obj))
    call['label'] = label
    call['coefficients'] = dict(coefficients)
    call['physical']['Eref_J'] = seed_row['Eref_eval_J']
    call['physical']['gamma'] = seed_row['gamma_eval']
    call['physical']['ell_F_m'] = seed_row['ell_F_m']
    call['physical']['common_scale_s'] = seed_row['scale_s']
    nspec = drv.normalize_spec(call)
    seed, changed, reusable = drv.per_call_seed(nspec)
    ni = seed['numerical_inputs']
    check = {'driver_seed_Eref_J': ni['Eref_J'], 'driver_seed_gamma': ni['gamma'], 'driver_seed_ell_F_m': ni['ell_F_m'],
             'equals_candidate_bitwise': ni['Eref_J'] == seed_row['Eref_J'] and ni['gamma'] == seed_row['gamma']
             and ni['ell_F_m'] == seed_row['ell_F_m'],
             'seed_changed_fields': changed, 'base_seed_v002_reused_bitwise': reusable}
    if not check['equals_candidate_bitwise']:
        raise Refusal('driver seed differs from the rule candidate')
    return call, check


def template_base(drv, template_obj, coefficients):
    call = json.loads(json.dumps(template_obj))
    call['coefficients'] = dict(coefficients)
    nspec = drv.normalize_spec(call)
    seed, changed, reusable = drv.per_call_seed(nspec)
    return nspec, seed, changed, reusable


def write_specs(out, drv, template_obj, coefficients, sel, rows, prefix):
    specs = {}
    d = out / 'route_b_specs'
    for role in ('first', 'next'):
        f = sel[role]
        if f is None:
            continue
        row = next(r for r in rows if r['factor'] == f)
        label = '%s seed-scan %s candidate: gamma factor %r (rule c2v001), s=%r' % (prefix, role, f, row['scale_s'])
        call, check = build_route_b_call(drv, template_obj, coefficients, row, label)
        d.mkdir(exist_ok=True)
        p = d / ('CALL_%s_SEEDSCAN_%s_C2V001.json' % (prefix, role.upper()))
        sha = write_x(p, call)
        specs[role] = {'path': str(p), 'sha256': sha, 'factor': f, 'driver_check': check}
    return specs


# ----------------------------------------------------------------------------- shared analysis of a v004-format candidate
def analyze_v004_candidate(folder, threshold, limit_m, v_cal):
    """Read-only analysis of a v004-format candidate folder (points.jsonl + report.json)."""
    rows = [json.loads(l) for l in open(Path(folder) / 'points.jsonl')]
    report = json.loads((Path(folder) / 'report.json').read_text())
    col = rows[:641]
    ddo = rows[641:]
    if len(ddo) != 96 or any(r['kind'] != 'DDO_query_midplane' for r in ddo):
        raise ValueError('not a v004 roster')
    radial = [r['signed_c2_R_dlnN_dR'] if r['status'] == 'available' else None for r in ddo]
    rule = apply_rule(radial, v_cal)
    vertical = []
    if col[320]['status'] == 'available':
        log0 = math.log(col[320]['metric']['N'])
        for r in col:
            if r['status'] == 'available':
                vertical.append((r['z_m'], math.log(r['metric']['N']) - log0, r['z_kpc']))
    same_as_report = [v[1] for v in vertical] == [v['logN_over_N0'] for v in report['vertical']]
    z = [v[0] for v in vertical]
    lr = [v[1] for v in vertical]
    out = {'factor': report['factor'], 'gamma_eval': report['gamma'], 'rule': rule,
           'vertical_recomputed_equals_report_bitwise': same_as_report,
           'report_radial_negative': report['radial_negative'], 'report_radial_min': report['radial_min'],
           'report_radial_max': report['radial_max'], 'report_sampled_logratio_max': report['sampled_logratio_max'],
           'threshold_v004': threshold, 'search_limit_m': limit_m}
    if rule['scale_s'] is not None:
        out['failure_column_margin_within_limit'] = two_sided(z, lr, rule['scale_s'], threshold, limit_m)
        out['failure_column_margin_full_roster'] = two_sided(z, lr, rule['scale_s'], threshold, float('inf'))
    else:
        out['failure_column_margin_within_limit'] = None
        out['failure_column_margin_full_roster'] = None
    out['unnormalized_margin_within_limit'] = two_sided(z, lr, 1.0, threshold, limit_m)
    m = out['failure_column_margin_within_limit']
    out['rule_pass'] = bool(rule['all_96_inward'] and rule['scale_s'] is not None and m is not None and m['positive'])
    return out


def analyze_saved_scan(scan_dir, v_cal=DECLARED_V_CAL_M_S):
    scan_dir = Path(scan_dir)
    start = json.loads((scan_dir / 'start.json').read_text())
    fail = start['source_failure']
    col = fail['column_inputs']
    ho = col['hi_options']
    c = 299792458.0
    m = fail['message']
    if 'c_m_s' in fail:
        c = float(fail['c_m_s'])
    thr = threshold_v004(ho['gamma'], ho['sigma0_m_s'], c)
    limit = float(ho['search_limit_m'])
    cands = []
    for i, _ in enumerate(start['gamma_factors']):
        folder = scan_dir / ('candidate_%03d' % i)
        if not (folder / 'report.json').is_file():
            break
        cands.append(analyze_v004_candidate(folder, thr, limit, v_cal))
    sel = select(cands)
    return {'scan_dir': str(scan_dir), 'start_sha256': sha256_file(scan_dir / 'start.json'),
            'failure_message': m, 'failure_column_R_m': col['R_m'], 'failure_column_phi': col['phi'],
            'candidates': cands, 'selection': sel,
            'file_sha256': {str(p.relative_to(scan_dir)): sha256_file(p) for i in range(len(cands))
                            for p in [scan_dir / ('candidate_%03d' % i) / n for n in ('points.jsonl', 'report.json', 'input.json')]}}


# ----------------------------------------------------------------------------- g2 route-A kernel mode
class DiagnosticBinding:
    """Numerically transparent wrapper of the reviewed complex binding (v004 DiagnosticBinding idea):
    records Hermitian-part eigenvalues/inertia per bound node, compactly (no JSONL stream).
    `__file__` is the wrapped module's file so the route-A cache identity is that of the real binding."""

    def __init__(self, module, n):
        import numpy as np
        self._m = module
        self.__file__ = module.__file__
        self.eig = np.full((n, 10), np.nan)
        self.anti = np.full(n, np.nan)
        self.knorm = np.full(n, np.nan)
        self.count = 0

    def bind_symbol(self, **arguments):
        import numpy as np
        bound = self._m.bind_symbol(**arguments)
        K = np.asarray(bound['kernel_density'])
        ev = np.linalg.eigvalsh((K + K.conj().T) / 2)
        anti = float(np.linalg.norm(K - K.conj().T))
        if not np.all(np.isfinite(ev)) or not math.isfinite(anti):
            raise ValueError('Nonfinite kernel eigen diagnostic')
        i = self.count
        self.eig[i] = ev
        self.anti[i] = anti
        self.knorm[i] = float(np.linalg.norm(K))
        self.count += 1
        return bound

    def solve_symbol(self, **arguments):
        return self._m.solve_symbol(**arguments)


def _reality_ok(v, atol, rtol):
    import numpy as np
    im = float(np.linalg.norm(v.imag))
    bound = atol + rtol * float(np.linalg.norm(v.real))
    return math.isfinite(im) and math.isfinite(bound) and im <= bound, im, bound


def read_reference(ref):
    att = Path(ref['attempt_directory'])
    if sha256_file(att / 'result.json') != ref['result_sha256']:
        raise Refusal('route_a_reference result.json pin mismatch')
    fin = json.loads((att / 'finish.json').read_text())
    if fin.get('result_sha256') != ref['result_sha256']:
        raise Refusal('route_a_reference finish/result mismatch')
    res = json.loads((att / 'result.json').read_text())
    sfp = res['result']['result']['source_fixed_point']
    failure = sfp.get('failure')
    start = json.loads((att / 'start.json').read_text())
    arrays = None
    for line in open(att / 'progress.jsonl'):
        ev = json.loads(line)
        if ev.get('stage') == 'iteration_prepared' and ev.get('iteration') == 0:
            arrays = {'metric_source_fourier_J': ev['metric_source_fourier_J'],
                      'wavevectors': ev['prepared_metric_response']['wavevectors'],
                      'weighted_responses': ev['prepared_metric_response']['weighted_responses']}
            break
    request = None
    rq = att.parent / 'request.json'
    if rq.is_file():
        request = json.loads(rq.read_text())
    return {'attempt': str(att), 'failure': failure, 'seed_numerical_inputs': start['seed']['numerical_inputs'],
            'iteration0_arrays': arrays, 'request': request, 'converged': sfp.get('converged_finite_fixed_point')}


def _ref_array(entry):
    import numpy as np
    p = Path(entry['array_file'])
    if sha256_file(p) != entry['sha256']:
        raise Refusal('reference array pin mismatch: %s' % p)
    with np.load(p, allow_pickle=False) as z:
        return z[entry['member']].copy()


def _parse_residual(message):
    for part in message.split(';'):
        part = part.strip()
        if part.startswith('actual_log_residual='):
            return float(part.split('=', 1)[1])
    return None


def v004_reads(prepared, rows, positions, l1, basem, mm, Cbar, mubar, c, atol, rtol, thr, folder):
    """The v004 read sequence verbatim: 641-row column via line v001 then 96 DDO points via evaluate_prepared;
    writes complex_field_jet.npz and points.jsonl (v004 row format) into folder.  Returns (rows, vertical, radial)."""
    import numpy as np
    nl = sum(1 for r in rows if r['kind'] == 'failure_column')
    R0, phi0 = rows[0]['R_m'], rows[0]['phi']
    line = l1.prepare_line(prepared=prepared, x_m=R0 * math.cos(phi0), y_m=R0 * math.sin(phi0))
    parts = []
    for row in rows[:nl]:
        parts.append(l1.evaluate_line(line=line, z_m=row['z_m'], boundary_fields=np.zeros((1, 10, 1)),
                                      boundary_gradient=np.zeros((1, 10, 1, 3)), boundary_hessian=np.zeros((1, 10, 1, 3, 3))))
    nq = len(rows) - nl
    parts.append(basem.evaluate_prepared(prepared=prepared, physical_positions=positions[nl:],
                                         boundary_fields=np.zeros((nq, 10, 1)), boundary_gradient=np.zeros((nq, 10, 1, 3)),
                                         boundary_hessian=np.zeros((nq, 10, 1, 3, 3))))
    packet = {name: np.concatenate([p[name] for p in parts], axis=0) for name in ('fields', 'gradient', 'hessian')}
    del parts, line
    with open(Path(folder) / 'complex_field_jet.npz', 'xb') as f:
        np.savez(f, positions=positions, fields=packet['fields'], gradient=packet['gradient'], hessian=packet['hessian'])
    actual = []
    with open(Path(folder) / 'points.jsonl', 'x') as f:
        for i, b in enumerate(rows):
            row = dict(b)
            try:
                d = packet['fields'][i, :, 0]
                grad = packet['gradient'][i, :, 0, :]
                hes = packet['hessian'][i, :, 0, :, :]
                dg = {}
                for name, v in [('fields', d), ('gradient', grad), ('hessian', hes)]:
                    ok, im, bound = _reality_ok(v, atol, rtol)
                    dg[name] = dict(imaginary_norm=im, bound=bound)
                    if not ok:
                        raise ValueError('NONREAL_' + name)
                m = mm.evaluate_point(delta_fields=d.real, delta_gradient_physical=grad.real, Cbar=Cbar,
                                      mubar=mubar, R=row['R_m'], phi=row['phi'], z=row['z_m'])
                radial = c * c * row['R_m'] * m['dlnN_dR']
                if not math.isfinite(radial):
                    raise ValueError('Nonfinite signed radial diagnostic')
                row.update(status='available', metric=serial(m), reality=dg, signed_c2_R_dlnN_dR=radial)
            except ValueError as exc:
                row.update(status='unavailable', reason=str(exc))
            actual.append(row)
            f.write(json.dumps(serial(row), allow_nan=False) + '\n')
            f.flush()
    vertical = []
    mid = nl // 2
    if actual[mid]['status'] == 'available':
        log0 = math.log(actual[mid]['metric']['N'])
        for row in actual[:nl]:
            if row['status'] == 'available':
                lr = math.log(row['metric']['N']) - log0
                vertical.append(dict(z_kpc=row['z_kpc'], z_m=row['z_m'], logN_over_N0=lr, threshold=thr, residual=lr - thr))
    radial = [r['signed_c2_R_dlnN_dR'] if r['status'] == 'available' else None for r in actual[nl:]]
    return actual, vertical, radial


def sweep_reads(prepared, cols, sweep_ids, zs_route, i0, l1, l2, mm, Cbar, mubar, atol, rtol):
    """Per swept column: legacy read (line v001 + metric evaluator; log N(z) - log N(0)) and the route-A
    stable read (line v002 lapse_difference, zero boundary) at every z of zs_route (zs_route[i0] == 0)."""
    import numpy as np
    nz = len(zs_route)
    if zs_route[i0] != 0.0:
        raise ValueError('roster midplane index')
    legacy = np.full((len(sweep_ids), nz), np.nan)
    stable = np.full((len(sweep_ids), nz), np.nan)
    sweep_notes = []
    zero = np.zeros(1)
    for jcol, ci in enumerate(sweep_ids):
        cc = cols[ci]
        Rj, pj = float(cc['R_m']), float(cc['phi'])
        pos = np.array([[Rj * math.cos(pj), Rj * math.sin(pj), 0.0]])
        xm, ym = float(pos[0, 0]), float(pos[0, 1])      # exactly the route-A metric_point transverse point
        la = l1.prepare_line(prepared=prepared, x_m=xm, y_m=ym)
        lb = l2.prepare_line(prepared=prepared, x_m=xm, y_m=ym)
        notes = []
        N = np.full(nz, np.nan)
        for iz, z in enumerate(zs_route):
            try:
                pk = l1.evaluate_line(line=la, z_m=z, boundary_fields=np.zeros((1, 10, 1)),
                                      boundary_gradient=np.zeros((1, 10, 1, 3)), boundary_hessian=np.zeros((1, 10, 1, 3, 3)))
                d, grad, hes = pk['fields'][0, :, 0], pk['gradient'][0, :, 0, :], pk['hessian'][0, :, 0, :, :]
                for name, v in [('fields', d), ('gradient', grad), ('hessian', hes)]:
                    if not _reality_ok(v, atol, rtol)[0]:
                        raise ValueError('NONREAL_' + name)
                N[iz] = mm.evaluate_point(delta_fields=d.real, delta_gradient_physical=grad.real, Cbar=Cbar,
                                          mubar=mubar, R=Rj, phi=pj, z=z)['N']
            except ValueError as exc:
                notes.append({'z_m': z, 'read': 'legacy', 'reason': str(exc)})
            try:
                st = l2.lapse_difference(line=lb, z_m=z, boundary_lapse_at_zero=zero, boundary_lapse_difference=zero,
                                         reality_atol=atol, reality_rtol=rtol)
                stable[jcol, iz] = float(st['log_lapse_ratio_from_midplane'][0])
            except ValueError as exc:
                notes.append({'z_m': z, 'read': 'stable', 'reason': str(exc)})
        if math.isfinite(N[i0]) and N[i0] > 0:
            with np.errstate(invalid='ignore', divide='ignore'):
                legacy[jcol] = np.log(N) - math.log(N[i0])
        sweep_notes.append(notes)
        del la, lb
    return legacy, stable, sweep_notes


def run_g2(nspec, out, progress):
    import numpy as np
    t0 = time.monotonic()
    v_cal = calibration_speed(nspec['calibration_region'])
    drv = load_module('driver')
    tpath = Path(nspec['route_b_template']['path'])
    traw = tpath.read_bytes()
    if sha256_bytes(traw) != nspec['route_b_template']['sha256']:
        raise Refusal('route_b_template pin mismatch')
    template = json.loads(traw)
    coeff = nspec['coefficients']
    cpath = Path(coeff['path'])
    if not cpath.is_file() or sha256_file(cpath) != coeff['sha256']:
        raise Refusal('coefficient grid pin mismatch')
    call_nspec, seed, changed, reusable = template_base(drv, template, coeff)
    if call_nspec['numerics']['truncation']['shape'] != 'cube':
        raise Refusal('route-A kernel is cube-truncated; template must be cube (route-A is never masked)')
    ni = seed['numerical_inputs']
    base = {'Eref_J': ni['Eref_J'], 'gamma': ni['gamma'], 'ell_F_m': ni['ell_F_m']}
    progress(stage='seed_resolved', base=base, seed_changed=changed, base_seed_reused=reusable)
    default = (str(cpath) == str(V004_COEFF[0]) and coeff['sha256'] == V004_COEFF[1])
    prep = load_module('prep')
    patch = None
    if not default:
        for name in ('COEFFICIENT', 'COEFFICIENT_SHA'):
            if not hasattr(prep, name):
                raise Refusal('prep patch target absent: ' + name)
        prep.COEFFICIENT = Path(str(cpath))
        prep.COEFFICIENT_SHA = coeff['sha256']
        patch = {'COEFFICIENT': str(cpath), 'COEFFICIENT_SHA': coeff['sha256']}
    if ni['analytic_initial_azimuth'] is not True or ni['composite_grid_spec'] is None:
        raise Refusal('declared analytic initial source and composite grid required (route-A binding guard)')
    ref = read_reference(nspec['route_a_reference']) if nspec['route_a_reference'] else None
    if ref is not None:
        for k in ('Eref_J', 'gamma', 'ell_F_m', 'fourier_points_per_axis', 'composite_grid_spec', 'kmax_inverse_kpc'):
            if canonical(ref['seed_numerical_inputs'][k]) != canonical(ni[k]):
                raise Refusal('route_a_reference seed differs from this call seed: ' + k)
        if ref['request'] is not None:
            pr = [p for p in ref['request'].get('module_patches', []) if p['path'] == str(PINS['prep'][0])]
            ref_sha = pr[0]['set']['COEFFICIENT_SHA'] if pr else V004_COEFF[1]
            if ref_sha != coeff['sha256']:
                raise Refusal('route_a_reference used a different coefficient grid')
    cache = load_module('cache')
    basem = load_module('base')
    l1 = load_module('line_v001')
    l2 = load_module('line_v002')
    solver = load_module('solver')
    progress(stage='prep_start')
    data = prep.prepare_inputs(**ni)
    progress(stage='prep_done', seconds=time.monotonic() - t0)
    mm = data['modules']['metric']
    if sha256_file(mm.__file__) != PINS['metric'][1] or sha256_file(data['modules']['complex'].__file__) != PINS['complex'][1]:
        raise Refusal('prep metric/complex module differs from the v004 pins')
    fa = data['fourier_arguments']
    if fa['Eref'] != base['Eref_J'] or fa['gamma'] != base['gamma'] or fa['ell_F'] != base['ell_F_m']:
        raise Refusal('prepared Fourier arguments differ from seed')
    waves = fa['k_physical']
    fixed = solver._supplied_fixed_source(data['fixed_source_fourier_J'], len(waves))
    gas = np.asarray(data['initial_gas_fourier_J'], dtype=complex)
    current = fixed + gas
    custody = {'coefficient_patch': patch, 'node_count': int(len(waves)), 'source_pins': data['source_pins'],
               'quadrature_weight_sum': data['quadrature_weight_sum'],
               'quadrature_weight_sum_expected': data['quadrature_weight_sum_expected'],
               'current_source_sha256': sha256_bytes(np.ascontiguousarray(current).tobytes()),
               'wavevectors_sha256': sha256_bytes(np.ascontiguousarray(waves).tobytes())}
    if ref is not None and ref['iteration0_arrays']:
        a = ref['iteration0_arrays']
        rs = _ref_array(a['metric_source_fourier_J'])
        rw = _ref_array(a['wavevectors'])
        custody['reference_source_bitwise_equal'] = rs.dtype == current.dtype and rs.shape == current.shape and rs.tobytes() == current.tobytes()
        custody['reference_wavevectors_bitwise_equal'] = rw.shape == waves.shape and rw.tobytes() == np.ascontiguousarray(waves).tobytes()
        del rs, rw
        if not (custody['reference_source_bitwise_equal'] and custody['reference_wavevectors_bitwise_equal']):
            raise Refusal('iteration-0 source/wavevectors differ from the route-A reference')
    cols = data['gas_columns']
    if ref is not None and ref['failure']:
        fidx = ref['failure']['column_index']
        if nspec['failure_column_index'] is not None and nspec['failure_column_index'] != fidx:
            raise Refusal('failure_column_index differs from route_a_reference failure')
    else:
        fidx = nspec['failure_column_index']
    if fidx is None:
        raise Refusal('reference has no failure; failure_column_index must be declared')
    if not 0 <= fidx < len(cols):
        raise Refusal('failure column index out of roster')
    fcol = cols[fidx]
    if ref is not None and ref['failure']:
        ci = ref['failure']['column_inputs']
        if ci['R_m'] != fcol['R_m'] or ci['phi'] != fcol['phi']:
            raise Refusal('reference failure column inputs differ from prepared roster')
    if nspec['sweep']['columns'] == 'failure_phi':
        sweep_ids = [i for i, cc in enumerate(cols) if cc['phi'] == fcol['phi']]
    else:
        sweep_ids = list(nspec['sweep']['columns'])
        if any(i >= len(cols) for i in sweep_ids):
            raise Refusal('sweep column out of roster')
    kpc = ni['kpc_m']
    c = data['c_m_s']
    ho = fcol['hi_options']
    thr = threshold_v004(ho['gamma'], ho['sigma0_m_s'], c)
    thr_hi = threshold_hi_v003(ho['gamma'], ho['sigma0_m_s'], c)
    limit = float(ho['search_limit_m'])
    step = float(ho['search_step_m'])
    roster = search_roster(step, limit)
    zs_route = [-d for d in reversed(roster)] + [0.0] + roster
    R0, phi0 = float(fcol['R_m']), float(fcol['phi'])
    rows = [dict(kind='failure_column', R_m=R0, phi=phi0, z_m=(i - 320) * .2 * kpc, z_kpc=(i - 320) * .2) for i in range(641)]
    rows += [dict(kind='DDO_query_midplane', query_index=i, R_m=r * kpc, phi=2 * math.pi * j / 8, z_m=0., azimuth_index=j)
             for i, r in enumerate(DDO_RADII_KPC) for j in range(8)]
    positions = np.array([[r['R_m'] * math.cos(r['phi']), r['R_m'] * math.sin(r['phi']), r['z_m']] for r in rows])
    cand_root = out / 'candidates'
    cand_root.mkdir()
    with open(out / 'wavevectors.npz', 'xb') as f:
        np.savez(f, wavevectors=np.asarray(waves), dk_weights=np.asarray(fa['dk_weights']))
    write_x(out / 'scan_context.json', {
        'base': base, 'v_cal_m_s': v_cal, 'failure_column_index': fidx, 'failure_column': fcol,
        'threshold_v004': thr, 'threshold_hi_v003': thr_hi, 'search_limit_m': limit, 'search_step_m': step,
        'route_roster_z_m': zs_route, 'sweep_column_indices': sweep_ids,
        'sweep_columns': [{'index': i, 'R_m': cols[i]['R_m'], 'R_kpc': cols[i]['R_m'] / kpc, 'phi': cols[i]['phi']} for i in sweep_ids],
        'custody': custody, 'route_b_call_seed_changed': changed, 'route_b_base_seed_reused': reusable})
    opts = ni
    results = []
    previous_inertia = None
    failed = None
    for index, factor in enumerate(nspec['gamma_factors']):
        tf = time.monotonic()
        folder = cand_root / ('candidate_%03d' % index)
        folder.mkdir()
        gamma_c = base['gamma'] * factor
        write_x(folder / 'input.json', dict(factor=factor, gamma=gamma_c, Eref_J=base['Eref_J'], ell_F_m=base['ell_F_m'],
                                            coefficients=coeff, current_source_sha256=custody['current_source_sha256']))
        progress(stage='candidate_start', index=index, factor=factor)
        try:
            if not math.isfinite(gamma_c) or gamma_c <= 0:
                raise ValueError('Nonfinite/nonpositive candidate gamma')
            diag = DiagnosticBinding(fa['complex_binding_module'], len(waves))
            args = dict(fa)
            args['gamma'] = gamma_c
            args['complex_binding_module'] = diag
            facade = cache.make_fourier_module(base_module=basem, log_directory=folder / 'node_diagnostics', start_iteration=0)
            prepared = facade.prepare(**args, source_density_fourier=current)
            if diag.count != len(waves):
                raise ValueError('diagnostic binding saw %d of %d nodes' % (diag.count, len(waves)))
            neg = np.sum(diag.eig < 0, axis=1)
            zer = np.sum(diag.eig == 0, axis=1)
            pos = np.sum(diag.eig > 0, axis=1)
            inertia = np.stack([neg, zer, pos], axis=1).astype(np.int16)
            changed_nodes = None if previous_inertia is None else np.flatnonzero(np.any(previous_inertia != inertia, axis=1))
            with open(folder / 'kernel_diagnostics.npz', 'xb') as f:
                np.savez(f, hermitian_part_eigenvalues=diag.eig, antihermitian_residual=diag.anti,
                         kernel_density_norm=diag.knorm, inertia_neg_zero_pos=inertia)
            wr = prepared['weighted_responses']
            wr_sha = sha256_bytes(np.ascontiguousarray(wr).tobytes())
            if nspec['keep_weighted_responses']:
                with open(folder / 'weighted_responses.npz', 'xb') as f:
                    np.savez(f, weighted_responses=wr)
            ref_check = None
            if ref is not None and ref['iteration0_arrays'] and factor == 1.0 and gamma_c == ref['seed_numerical_inputs']['gamma'] \
                    and base['Eref_J'] == ref['seed_numerical_inputs']['Eref_J']:
                rr = _ref_array(ref['iteration0_arrays']['weighted_responses'])
                ref_check = {'weighted_responses_bitwise_equal_route_a_iteration0': rr.shape == wr.shape and rr.tobytes() == np.ascontiguousarray(wr).tobytes()}
                del rr
            # ---- v004 reads, verbatim structure
            actual, vertical, radial = v004_reads(prepared, rows, positions, l1, basem, mm, fa['Cbar'], fa['mubar'], c,
                                                  opts['reality_atol'], opts['reality_rtol'], thr, folder)
            # ---- radius sweep: legacy read (line v001 + metric evaluator, log N - log N0) and route-A stable
            # read (line v002 lapse_difference) on the exact route-A search roster.
            legacy, stable, sweep_notes = sweep_reads(prepared, cols, sweep_ids, zs_route, len(roster), l1, l2, mm,
                                                      fa['Cbar'], fa['mubar'], opts['reality_atol'], opts['reality_rtol'])
            with open(folder / 'sweep_reads.npz', 'xb') as f:
                np.savez(f, column_indices=np.array(sweep_ids), R_m=np.array([cols[i]['R_m'] for i in sweep_ids]),
                         phi=np.array([cols[i]['phi'] for i in sweep_ids]), z_m=np.array(zs_route),
                         legacy_logN_over_N0=legacy, stable_log_lapse_ratio=stable)
            # ---- declared rule
            rule = apply_rule(radial, v_cal)
            s = rule['scale_s']
            zf = [v['z_m'] for v in vertical]
            lf = [v['logN_over_N0'] for v in vertical]
            fmargin = two_sided(zf, lf, s, thr, limit) if s is not None else None
            fmargin_full = two_sided(zf, lf, s, thr, float('inf')) if s is not None else None
            unnorm = two_sided(zf, lf, 1.0, thr, limit)
            sweep_rows = []
            for jcol, ci in enumerate(sweep_ids):
                lg = [None if not math.isfinite(v) else float(v) for v in legacy[jcol]]
                sb = [None if not math.isfinite(v) else float(v) for v in stable[jcol]]
                row = {'column_index': ci, 'R_kpc': cols[ci]['R_m'] / kpc, 'phi': cols[ci]['phi'],
                       'unavailable_reads': len(sweep_notes[jcol]), 'first_unavailable': sweep_notes[jcol][:3],
                       'unnormalized_stable': two_sided(zs_route, sb, 1.0, thr_hi, limit)}
                if s is not None:
                    row['legacy_normalized'] = two_sided(zs_route, lg, s, thr, limit)
                    row['stable_normalized'] = two_sided(zs_route, sb, s, thr_hi, limit)
                sweep_rows.append(row)
            sweep_summary = None
            if s is not None:
                lm_ = [r['legacy_normalized']['two_sided_margin'] for r in sweep_rows]
                sm_ = [r['stable_normalized']['two_sided_margin'] for r in sweep_rows]
                sweep_summary = {
                    'legacy_negative_or_missing_columns': [r['column_index'] for r in sweep_rows if not r['legacy_normalized']['positive']],
                    'stable_negative_or_missing_columns': [r['column_index'] for r in sweep_rows if not r['stable_normalized']['positive']],
                    'legacy_min_two_sided_margin': min((v for v in lm_ if v is not None), default=None),
                    'stable_min_two_sided_margin': min((v for v in sm_ if v is not None), default=None)}
                sweep_summary['all_swept_columns_positive_legacy'] = not sweep_summary['legacy_negative_or_missing_columns']
                sweep_summary['all_swept_columns_positive_stable'] = not sweep_summary['stable_negative_or_missing_columns']
            crosscheck = None
            if ref is not None and ref['failure'] and factor == 1.0 and fidx in sweep_ids:
                jf = sweep_ids.index(fidx)
                rmsg = ref['failure']['message']
                side = 'plus' if 'side=plus' in rmsg else ('minus' if 'side=minus' in rmsg else None)
                zl = limit if side == 'plus' else -limit
                iz = zs_route.index(zl)
                crosscheck = {'route_a_actual_log_residual': _parse_residual(rmsg), 'route_a_side': side,
                              'stable_residual_at_limit': float(stable[jf, iz]) - thr_hi,
                              'legacy_residual_at_limit': float(legacy[jf, iz]) - thr,
                              'scope': 'factor 1 at the reference seed reproduces route-A iteration 0; stable read is the route-A HI read'}
                crosscheck['stable_bitwise_equal'] = crosscheck['stable_residual_at_limit'] == crosscheck['route_a_actual_log_residual']
            seed_row = candidate_seed(base, factor, s) if s is not None else None
            rule_pass = bool(rule['all_96_inward'] and s is not None and fmargin is not None and fmargin['positive'])
            rep = {'status': 'FIXED_SOURCE_PARAMETER_SEARCH_C2V001', 'factor': factor, 'gamma': gamma_c, 'Eref_J': base['Eref_J'],
                   'validated': False, 'accepted_for_calibration': False, 'vertical': vertical,
                   'sampled_logratio_min': min((v['logN_over_N0'] for v in vertical), default=None),
                   'sampled_logratio_max': max((v['logN_over_N0'] for v in vertical), default=None),
                   'radial_available': rule['radial_available'], 'radial_negative': sum(1 for v in radial if v is not None and v < 0),
                   'radial_min': rule['radial_min'], 'radial_max': rule['radial_max'], 'rule': rule,
                   'failure_column_margin_within_limit': fmargin, 'failure_column_margin_full_roster': fmargin_full,
                   'failure_column_unnormalized_margin_within_limit': unnorm,
                   'sweep': sweep_rows, 'sweep_summary': sweep_summary, 'route_a_crosscheck': crosscheck,
                   'reference_check': ref_check, 'candidate_seed': seed_row, 'rule_pass': rule_pass,
                   'kernel': {'weighted_responses_sha256': wr_sha,
                              'inertia_counts': {str(tuple(int(x) for x in k)): int(n) for k, n in zip(*np.unique(inertia, axis=0, return_counts=True))},
                              'min_abs_hermitian_eigenvalue': float(np.min(np.abs(diag.eig))),
                              'max_antihermitian_residual': float(np.max(diag.anti)),
                              'inertia_changed_nodes_vs_previous': None if changed_nodes is None else int(len(changed_nodes)),
                              'inertia_changed_first_indices': None if changed_nodes is None else changed_nodes[:200].tolist(),
                              'interpretation': 'Changed inertia indicates an intervening Hermitian-part zero crossing; unchanged inertia does NOT exclude intervening poles; no stability claim.'},
                   'seconds': time.monotonic() - tf,
                   'scope': 'Signed radial lapse-gradient diagnostic, NOT speed; sampled vertical values not extrema certificates; '
                            'fixed iteration-0 source; amplitude normalization is a linear estimate; no HI re-equilibration or calibration.'}
            write_x(folder / 'report.json', rep, indent=None)
            previous_inertia = inertia
            results.append(rep)
            progress(stage='candidate_done', index=index, factor=factor, rule_pass=rule_pass, scale_s=s,
                     seconds=rep['seconds'])
            del prepared, facade, diag, wr, actual, legacy, stable
        except Exception as exc:
            write_x(folder / 'failure.json', dict(status='FAILED_CANDIDATE', type=type(exc).__name__, message=str(exc),
                                                  factor=factor, gamma=gamma_c))
            failed = {'index': index, 'factor': factor, 'type': type(exc).__name__, 'message': str(exc)}
            break   # preserve completed prefix; never skip or retry
    summary = [{'factor': r['factor'], 'rule_pass': r['rule_pass'], 'scale_s': r['rule']['scale_s'],
                'radial_inward': r['rule']['radial_inward_positive'], 'radial_available': r['rule']['radial_available'],
                'failure_column_two_sided_margin': None if r['failure_column_margin_within_limit'] is None else r['failure_column_margin_within_limit']['two_sided_margin'],
                'sweep_all_positive_legacy': None if r['sweep_summary'] is None else r['sweep_summary']['all_swept_columns_positive_legacy'],
                'sweep_all_positive_stable': None if r['sweep_summary'] is None else r['sweep_summary']['all_swept_columns_positive_stable'],
                'candidate_seed': r['candidate_seed']} for r in results]
    sel = select(summary)
    specs = {}
    if failed is None and sel['first'] is not None:
        specs = write_specs(out, drv, template, coeff, sel, [s_['candidate_seed'] for s_ in summary if s_['candidate_seed']],
                            'A2' if not default else 'V004')
    status = ('FAILED_AT_CANDIDATE' if failed else ('COMPLETED_SELECTED' if sel['first'] is not None else 'COMPLETED_NO_CANDIDATE'))
    return {'status': status, 'mode': 'g2_route_a_kernel', 'base': base, 'v_cal_m_s': v_cal, 'custody': custody,
            'failure_column_index': fidx, 'failure_column_R_kpc': fcol['R_m'] / kpc, 'threshold_v004': thr,
            'threshold_hi_v003': thr_hi, 'search_limit_m': limit, 'candidates': summary, 'selection': sel,
            'route_b_specs': specs, 'failed_candidate': failed, 'elapsed_seconds': time.monotonic() - t0,
            'registered_result': None if sel['first'] is not None or failed else
            'No gamma factor in the declared list meets the declared seed rule; nothing selected.'}


# ----------------------------------------------------------------------------- v004 reproduction mode
def _launch_args(launch):
    cmd = launch['command']
    a = {}
    i = 0
    while i < len(cmd):
        if cmd[i].startswith('--') and cmd[i] != '--gamma-factors':
            a[cmd[i][2:]] = cmd[i + 1]
            i += 2
        elif cmd[i] == '--gamma-factors':
            j = i + 1
            vals = []
            while j < len(cmd) and not cmd[j].startswith('--'):
                vals.append(float(cmd[j]))
                j += 1
            a['gamma-factors'] = vals
            i = j
        else:
            i += 1
    return a


def run_repro(nspec, out, progress):
    t0 = time.monotonic()
    v_cal = calibration_speed(nspec['calibration_region'])
    lp = Path(nspec['v004_launch']['path'])
    if sha256_file(lp) != nspec['v004_launch']['sha256']:
        raise Refusal('v004 launch pin mismatch')
    launch = json.loads(lp.read_text())
    if launch['worker_sha256'] != PINS['v004_worker'][1] or Path(launch['command'][3]) != PINS['v004_worker'][0]:
        raise Refusal('launch is not the pinned v004 worker')
    a = _launch_args(launch)
    saved_dir = Path(a['outdir'])
    if any(f not in a['gamma-factors'] for f in nspec['gamma_factors']):
        raise Refusal('reproduction factors must be a subset of the saved launch factors %s' % a['gamma-factors'])
    if nspec['gamma_factors'] != a['gamma-factors'][:len(nspec['gamma_factors'])]:
        raise Refusal('reproduction factors must be a prefix of the saved launch order (candidate_NNN indices)')
    drv = load_module('driver')
    traw = Path(nspec['route_b_template']['path']).read_bytes()
    if sha256_bytes(traw) != nspec['route_b_template']['sha256']:
        raise Refusal('route_b_template pin mismatch')
    template = json.loads(traw)
    v004 = load_module('v004_worker')
    progress(stage='v004_start', factors=nspec['gamma_factors'])
    new_dir = out / 'v004_scan'
    v004.run(a['input-result'], a['pinned-sha256'], str(new_dir), nspec['gamma_factors'], a['source-directory'],
             a['source-sha256'], a['identity-sha256'])
    progress(stage='v004_done', seconds=time.monotonic() - t0)
    new = analyze_saved_scan(new_dir, v_cal)
    saved = analyze_saved_scan(saved_dir, v_cal)
    cmp = {'files_bitwise_equal': {k: (new['file_sha256'].get(k) == v) for k, v in saved['file_sha256'].items()
                                   if k.split('/')[0] in ['candidate_%03d' % i for i in range(len(nspec['gamma_factors']))]},
           'analysis_equal': canonical(new['candidates']) == canonical(saved['candidates'][:len(new['candidates'])])}
    return finish_v004_analysis(new, cmp, drv, template, v_cal, out, t0, 'v004_ir64_reproduction')


def finish_v004_analysis(an, cmp, drv, template, v_cal, out, t0, mode):
    seed_raw = verified('seed_v002')[0].read_bytes()
    seed = json.loads(seed_raw)
    base = {'Eref_J': 9.243506372672262e58, 'gamma': 1.856569929503051e41,
            'ell_F_m': seed['numerical_inputs']['ell_F_m']}       # v004's hard-coded current base
    rows = []
    for cnd in an['candidates']:
        s = cnd['rule']['scale_s']
        rows.append({'factor': cnd['factor'], 'rule_pass': cnd['rule_pass'], 'scale_s': s,
                     'candidate_seed': candidate_seed(base, cnd['factor'], s) if s is not None else None,
                     'gamma_eval_equals_report': (base['gamma'] * cnd['factor']) == cnd['gamma_eval']})
    sel = select(rows)
    seedcheck = None
    if sel['first'] is not None:
        r0 = next(r for r in rows if r['factor'] == sel['first'])['candidate_seed']
        seedcheck = {'scale_s': r0['scale_s'], 'seed_v002_scale_seed': seed['scale_seed'],
                     'scale_bitwise_equal': r0['scale_s'] == seed['scale_seed'],
                     'Eref_bitwise_equal': r0['Eref_J'] == seed['numerical_inputs']['Eref_J'],
                     'gamma_bitwise_equal': r0['gamma'] == seed['numerical_inputs']['gamma'],
                     'first_factor_is_10': sel['first'] == 10.0,
                     'next_factor_is_100': sel['next'] == 100.0 if len(rows) > 1 else None}
    specs = {}
    if sel['first'] is not None:
        coeff = {'path': str(V004_COEFF[0]), 'sha256': V004_COEFF[1]}
        specs = write_specs(out, drv, template, coeff, sel, [r['candidate_seed'] for r in rows if r['candidate_seed']], 'V004REPRO')
        if specs.get('first'):
            seedcheck['route_b_first_spec_reuses_seed_v002_bitwise'] = specs['first']['driver_check']['base_seed_v002_reused_bitwise']
    ok = bool(seedcheck and all(v for k, v in seedcheck.items() if k.endswith('equal') or k.startswith('first_factor')
                                or k.startswith('route_b'))
              and (cmp is None or (all(cmp['files_bitwise_equal'].values()) and cmp['analysis_equal'])))
    return {'status': 'REPRODUCED' if ok else 'NOT_REPRODUCED', 'mode': mode, 'analysis': an, 'comparison': cmp,
            'candidates': rows, 'selection': sel, 'seed_v002_check': seedcheck, 'route_b_specs': specs,
            'v_cal_m_s': v_cal, 'elapsed_seconds': time.monotonic() - t0}


# ----------------------------------------------------------------------------- synthetic selftest mode
def run_synthetic(nspec, out, progress):
    t0 = time.monotonic()
    v_cal = calibration_speed(nspec['calibration_region'])
    syn = nspec['synthetic']
    time.sleep(float(syn.get('sleep_s', 0)))
    thr = threshold_v004(5 / 3, 11000., 299792458.0)
    limit = 32 * 3.085677581491367e19
    z = [(i - 320) * .2 * 3.085677581491367e19 for i in range(641)]
    rows = []
    for f in nspec['gamma_factors']:
        radial = syn['radial_by_factor'][repr(f)]
        rule = apply_rule(radial, v_cal)
        peak = syn['lr_peak_by_factor'][repr(f)]
        lr = [peak * min(1.0, abs(zz) / (8 * 3.085677581491367e19)) for zz in z]
        m = two_sided(z, lr, rule['scale_s'], thr, limit) if rule['scale_s'] else None
        rp = bool(rule['all_96_inward'] and m and m['positive'])
        rows.append({'factor': f, 'rule': rule, 'margin': m, 'rule_pass': rp})
        progress(stage='synthetic_candidate', factor=f, rule_pass=rp)
    sel = select(rows)
    return {'status': 'COMPLETED_SELECTED' if sel['first'] is not None else 'COMPLETED_NO_CANDIDATE', 'mode': 'synthetic_selftest',
            'candidates': rows, 'selection': sel, 'elapsed_seconds': time.monotonic() - t0}


# ----------------------------------------------------------------------------- run / dry-run
def cmd_run(spec_path, outdir):
    out = Path(outdir).resolve()
    raw = Path(spec_path).read_bytes()
    spec_sha = sha256_bytes(raw)
    nspec = normalize_scan_spec(json.loads(raw))
    out.mkdir(exist_ok=False)
    with open(out / 'call_spec.json', 'xb') as f:
        f.write(raw)
    write_x(out / 'start.json', {'schema': RESULT_SCHEMA, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                 'script': str(Path(__file__).resolve()), 'script_sha256': sha256_file(__file__),
                                 'spec_sha256': spec_sha, 'normalized_spec': nspec,
                                 'static_pins': {k: {'path': str(p), 'sha256': s} for k, (p, s) in PINS.items()}})
    log = open(out / 'progress.jsonl', 'x')
    t0 = time.monotonic()

    def progress(**kw):
        kw['elapsed_seconds'] = time.monotonic() - t0
        log.write(json.dumps(serial(kw), allow_nan=False) + '\n')
        log.flush()
    try:
        if nspec['mode'] == 'g2_route_a_kernel':
            result = run_g2(nspec, out, progress)
        elif nspec['mode'] == 'v004_ir64_reproduction':
            result = run_repro(nspec, out, progress)
        else:
            result = run_synthetic(nspec, out, progress)
    except Refusal as exc:
        result = {'status': 'REFUSED', 'reason': str(exc)}
    except Exception as exc:
        result = {'status': 'FAILED', 'type': type(exc).__name__, 'message': str(exc)}
    result.update(schema=RESULT_SCHEMA, spec_sha256=spec_sha, script_sha256=sha256_file(__file__),
                  validated=False, accepted_for_calibration=False)
    rsha = write_x(out / 'result.json', result)
    write_x(out / 'finish.json', {'status': result['status'], 'result_sha256': rsha, 'retries': 0,
                                  'result_path': str((out / 'result.json').resolve()),
                                  'elapsed_seconds': time.monotonic() - t0})
    log.close()
    print(json.dumps({'status': result['status'], 'selection': result.get('selection'), 'result_sha256': rsha}))
    return 0 if result['status'] in ('COMPLETED_SELECTED', 'COMPLETED_NO_CANDIDATE', 'REPRODUCED') else 1


def cmd_dry_run(spec_path, outdir):
    import numpy as np
    out = Path(outdir).resolve()
    raw = Path(spec_path).read_bytes()
    rep = {'schema': RESULT_SCHEMA + '_DRYRUN', 'spec': str(spec_path), 'spec_sha256': sha256_bytes(raw),
           'executed_project_computation': False, 'checks': [], 'problems': []}

    def check(name, ok, detail=None):
        rep['checks'].append({'check': name, 'ok': bool(ok), 'detail': detail})
        if not ok:
            rep['problems'].append(name)
    try:
        nspec = normalize_scan_spec(json.loads(raw))
        rep['normalized_spec'] = nspec
        for k, (p, s) in PINS.items():
            check('pin ' + k, Path(p).is_file() and sha256_file(p) == s, str(p))
        v_cal = calibration_speed(nspec['calibration_region'])
        check('calibration median is 43300 m/s', v_cal == DECLARED_V_CAL_M_S, v_cal)
        drv = load_module('driver')
        tpath = Path(nspec.get('route_b_template', {}).get('path', '')) if nspec['mode'] != 'synthetic_selftest' else None
        if tpath is not None:
            traw = tpath.read_bytes()
            check('route_b_template pin', sha256_bytes(traw) == nspec['route_b_template']['sha256'], str(tpath))
            template = json.loads(traw)
        if nspec['mode'] == 'g2_route_a_kernel':
            coeff = nspec['coefficients']
            check('coefficient grid pin', Path(coeff['path']).is_file() and sha256_file(coeff['path']) == coeff['sha256'], coeff['path'])
            with np.load(coeff['path'], allow_pickle=False) as z:
                hdr = {k: [list(z[k].shape), z[k].dtype.str] for k in ('source_hessian_grid', 'background_C', 'background_mu')}
            rep['coefficient_headers'] = hdr
            cn, seed, changed, reusable = template_base(drv, template, coeff)
            ni = seed['numerical_inputs']
            rep['seed'] = {'Eref_J': ni['Eref_J'], 'gamma': ni['gamma'], 'ell_F_m': ni['ell_F_m'],
                           'fourier_points_per_axis': ni['fourier_points_per_axis'], 'composite_grid_spec': ni['composite_grid_spec'],
                           'changed_vs_seed_v002': changed, 'seed_v002_reused_bitwise': reusable}
            check('template truncation cube', cn['numerics']['truncation']['shape'] == 'cube')
            check('G2 72-node composite grid', ni['fourier_points_per_axis'] == 72 and ni['composite_grid_spec']['total_axis_nodes'] == 72)
            nodes = ni['fourier_points_per_axis'] ** 3
            rep['node_count'] = nodes
            default = (coeff['path'] == str(V004_COEFF[0]) and coeff['sha256'] == V004_COEFF[1])
            rep['prep_patch'] = None if default else {'COEFFICIENT': coeff['path'], 'COEFFICIENT_SHA': coeff['sha256']}
            if nspec['route_a_reference']:
                ref = read_reference(nspec['route_a_reference'])
                f = ref['failure']
                rep['reference_failure'] = None if f is None else {
                    'column_index': f['column_index'], 'iteration': f['iteration'], 'R_m': f['column_inputs']['R_m'],
                    'R_kpc': f['column_inputs']['R_m'] / ni['kpc_m'], 'phi': f['column_inputs']['phi'], 'message': f['message'],
                    'threshold_v004': threshold_v004(f['column_inputs']['hi_options']['gamma'], f['column_inputs']['hi_options']['sigma0_m_s'], f['c_m_s']),
                    'threshold_hi_v003': threshold_hi_v003(f['column_inputs']['hi_options']['gamma'], f['column_inputs']['hi_options']['sigma0_m_s'], f['c_m_s']),
                    'actual_log_residual': _parse_residual(f['message'])}
                for k in ('Eref_J', 'gamma', 'ell_F_m', 'composite_grid_spec'):
                    check('reference seed %s equals call seed' % k, canonical(ref['seed_numerical_inputs'][k]) == canonical(ni[k]))
                a = ref['iteration0_arrays']
                check('reference iteration-0 arrays recorded', a is not None)
                if a:
                    for name, e in a.items():
                        ok = Path(e['array_file']).is_file() and sha256_file(e['array_file']) == e['sha256']
                        check('reference array pin ' + name, ok, e['shape'])
                        check('reference array node count ' + name, e['shape'][0] == nodes, e['shape'])
                if ref['request'] is not None:
                    pr = [p for p in ref['request'].get('module_patches', []) if p['path'] == str(PINS['prep'][0])]
                    rsha = pr[0]['set']['COEFFICIENT_SHA'] if pr else V004_COEFF[1]
                    check('reference coefficient grid equals call grid', rsha == coeff['sha256'], rsha)
                if f is not None:
                    check('reference failure at iteration 0', f['iteration'] == 0)
                    if nspec['failure_column_index'] is not None:
                        check('declared failure column equals reference failure', nspec['failure_column_index'] == f['column_index'])
                else:
                    check('reference without failure: failure column declared', nspec['failure_column_index'] is not None,
                          {'reference_converged': ref['converged']})
            nf = len(nspec['gamma_factors'])
            rep['plan'] = {'factors': nspec['gamma_factors'],
                           'gamma_eval': [ni['gamma'] * f for f in nspec['gamma_factors']],
                           'gamma_over_Eref_eval': [ni['gamma'] * f / ni['Eref_J'] for f in nspec['gamma_factors']],
                           'sweep': nspec['sweep'],
                           'estimated_seconds': PREP_COST_S_G2 + nf * COST_PER_FACTOR_S_G2,
                           'estimated_output_bytes': nf * OUTPUT_PER_FACTOR_BYTES_G2,
                           'estimated_peak_rss_bytes': int(1.3 * 2 ** 30),
                           'suggested_caps': {'wall_cap_s': max(1800.0, 2.0 * (PREP_COST_S_G2 + nf * COST_PER_FACTOR_S_G2)),
                                              'rss_cap_bytes': 3 * 2 ** 30,
                                              'output_cap_bytes': max(4 * 2 ** 30, int(1.5 * nf * OUTPUT_PER_FACTOR_BYTES_G2))}}
        elif nspec['mode'] == 'v004_ir64_reproduction':
            lp = Path(nspec['v004_launch']['path'])
            check('v004 launch pin', lp.is_file() and sha256_file(lp) == nspec['v004_launch']['sha256'], str(lp))
            launch = json.loads(lp.read_text())
            a = _launch_args(launch)
            check('launch worker is pinned v004', launch['worker_sha256'] == PINS['v004_worker'][1])
            check('factors prefix of saved launch', nspec['gamma_factors'] == a['gamma-factors'][:len(nspec['gamma_factors'])], a['gamma-factors'])
            for k, pk in (('input-result', 'pinned-sha256'),):
                check('input result pin', sha256_file(a[k]) == a[pk], a[k])
            sd = Path(a['source-directory'])
            check('source.npz pin', sha256_file(sd / 'source.npz') == a['source-sha256'])
            check('source_identity.json pin', sha256_file(sd / 'source_identity.json') == a['identity-sha256'])
            check('V004 coefficients pin', sha256_file(V004_COEFF[0]) == V004_COEFF[1])
            for k, sha in launch['extra_dependency_pins'].items():
                check('v004 dependency pin ' + Path(k).name, sha256_file(k) == sha)
            saved = analyze_saved_scan(a['outdir'])
            rep['saved_scan_analysis_preview'] = {'selection': saved['selection'],
                                                  'scales': [c['rule']['scale_s'] for c in saved['candidates']]}
            rep['plan'] = {'factors': nspec['gamma_factors'], 'saved_scan': a['outdir'],
                           'estimated_seconds': 135.0 * len(nspec['gamma_factors']) + 10,
                           'estimated_output_bytes': 860 * 2 ** 20 * len(nspec['gamma_factors']),
                           'suggested_caps': {'wall_cap_s': 1800.0, 'rss_cap_bytes': 2 * 2 ** 30, 'output_cap_bytes': 4 * 2 ** 30},
                           'measured_original': 'receipt: 266.46 s, combined peak 433618944 B, 2 factors'}
        else:
            rep['plan'] = {'factors': nspec['gamma_factors'], 'synthetic': True}
    except Refusal as exc:
        rep['problems'].append('REFUSED: ' + str(exc))
    rep['ok'] = not rep['problems']
    out.mkdir(parents=True, exist_ok=False)
    sha = write_x(out / 'DRYRUN_REPORT.json', rep)
    print(json.dumps({'ok': rep['ok'], 'problems': rep['problems'], 'report_sha256': sha}))
    return 0 if rep['ok'] else 1


def cmd_analyze_saved(scan_dir, out_file):
    an = analyze_saved_scan(scan_dir)
    drv = load_module('driver')
    template_path = EX / 'calibration_prep_c2_0470/kmax_convergence/specs/wave1/CALL_KMAX_C2_C2V001.json'
    template = json.loads(template_path.read_bytes())
    outp = Path(out_file).resolve()
    tmp_out = outp.parent / (outp.stem + '_specs')
    tmp_out.mkdir(exist_ok=False)
    res = finish_v004_analysis(an, None, drv, template, DECLARED_V_CAL_M_S, tmp_out, time.monotonic(), 'analyze_saved_read_only')
    res['template'] = {'path': str(template_path), 'sha256': sha256_file(template_path)}
    sha = write_x(outp, res)
    print(json.dumps({'status': res['status'], 'selection': res['selection'], 'seed_v002_check': res['seed_v002_check'], 'sha256': sha}))
    return 0 if res['status'] == 'REPRODUCED' else 1


def cmd_replay_v004_reads(candidate_dir, outdir, launch_path, launch_sha):
    """Re-run ONLY the v004 read sequence (no kernel build) on a saved v004 candidate's prepared_waves.npz
    through this file's v004_reads, and compare points.jsonl bytes and jet arrays with the saved ones.
    About 1 minute single thread (96 positions x 262144 waves).  Root/Claude2 runs it; read-only on inputs."""
    import numpy as np
    t0 = time.monotonic()
    cand = Path(candidate_dir)
    out = Path(outdir).resolve()
    if sha256_file(launch_path) != launch_sha:
        raise Refusal('launch pin mismatch')
    launch = json.loads(Path(launch_path).read_text())
    a = _launch_args(launch)
    if Path(a['outdir']).resolve() != cand.parent.resolve():
        raise Refusal('candidate is not inside the launch outdir')
    raw = Path(a['input-result']).read_bytes()
    if sha256_bytes(raw) != a['pinned-sha256']:
        raise Refusal('input result pin mismatch')
    x = json.loads(raw)
    opts, phys = x['numerical_inputs'], x['physical_inputs']
    del x, raw
    start = json.loads((cand.parent / 'start.json').read_text())
    fail = start['source_failure']
    col = fail['column_inputs']
    R0, phi0, c, kpc = float(col['R_m']), float(col['phi']), float(fail['c_m_s']), phys['kpc_m']
    g, sig = col['hi_options']['gamma'], col['hi_options']['sigma0_m_s']
    thr = threshold_v004(g, sig, c)
    rows = [dict(kind='failure_column', R_m=R0, phi=phi0, z_m=(i - 320) * .2 * kpc, z_kpc=(i - 320) * .2) for i in range(641)]
    rows += [dict(kind='DDO_query_midplane', query_index=i, R_m=r * kpc, phi=2 * math.pi * j / 8, z_m=0., azimuth_index=j)
             for i, r in enumerate(DDO_RADII_KPC) for j in range(8)]
    positions = np.array([[r['R_m'] * math.cos(r['phi']), r['R_m'] * math.sin(r['phi']), r['z_m']] for r in rows])
    with np.load(cand / 'prepared_waves.npz', allow_pickle=False) as z:
        prepared = {'wavevectors': z['wavevectors'].copy(), 'weighted_responses': z['weighted_responses'].copy(),
                    'grid_diagnostics': None, 'node_diagnostics': [], 'finite_domain_description': 'replay',
                    'boundary_description': 'replay', 'node_convention': 'full_signed'}
        Cbar, mubar = z['Cbar'].copy(), z['mubar'].copy()
    with np.load(verified(V004_COEFF)[0], allow_pickle=False) as z:
        if not (np.array_equal(z['background_C'], Cbar) and np.array_equal(z['background_mu'], mubar)):
            raise Refusal('saved prepared background differs from V004 coefficients')
    l1, l2, basem, mm = (load_module(k) for k in ('line_v001', 'line_v002', 'base', 'metric'))
    out.mkdir(exist_ok=False)
    actual, vertical, radial = v004_reads(prepared, rows, positions, l1, basem, mm, Cbar, mubar, c,
                                          opts['reality_atol'], opts['reality_rtol'], thr, out)
    roster = search_roster(float(col['hi_options']['search_step_m']), float(col['hi_options']['search_limit_m']))
    zs = [-d for d in reversed(roster)] + [0.0] + roster
    legacy, stable, notes = sweep_reads(prepared, [col], [0], zs, len(roster), l1, l2, mm, Cbar, mubar,
                                        opts['reality_atol'], opts['reality_rtol'])
    with np.load(cand / 'complex_field_jet.npz', allow_pickle=False) as z1, np.load(out / 'complex_field_jet.npz', allow_pickle=False) as z2:
        jets = {k: bool(z1[k].shape == z2[k].shape and z1[k].tobytes() == z2[k].tobytes()) for k in ('positions', 'fields', 'gradient', 'hessian')}
    saved_report = json.loads((cand / 'report.json').read_text())
    res = {'status': None, 'candidate_dir': str(cand), 'factor': saved_report['factor'],
           'points_sha256_saved': sha256_file(cand / 'points.jsonl'), 'points_sha256_replay': sha256_file(out / 'points.jsonl'),
           'jet_arrays_bitwise_equal': jets,
           'vertical_equal_saved_report': [v['logN_over_N0'] for v in vertical] == [v['logN_over_N0'] for v in saved_report['vertical']],
           'radial_equal_saved': [r for r in radial] == [json.loads(l)['signed_c2_R_dlnN_dR'] for l in list(open(cand / 'points.jsonl'))[641:]],
           'route_roster_legacy_vs_stable_max_abs_diff': float(np.nanmax(np.abs(legacy - stable))),
           'route_roster_lr_at_plus_limit': {'legacy': float(legacy[0, -1]), 'stable': float(stable[0, -1])},
           'elapsed_seconds': time.monotonic() - t0}
    res['points_bitwise_equal'] = res['points_sha256_saved'] == res['points_sha256_replay']
    res['status'] = 'REPLAY_BITWISE_EQUAL' if (res['points_bitwise_equal'] and all(jets.values()) and res['vertical_equal_saved_report']
                                               and res['radial_equal_saved']) else 'REPLAY_DIFFERS'
    sha = write_x(out / 'REPLAY_REPORT.json', res)
    print(json.dumps({'status': res['status'], 'report_sha256': sha}))
    return 0 if res['status'] == 'REPLAY_BITWISE_EQUAL' else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('run', 'dry-run'):
        p = sub.add_parser(name)
        p.add_argument('--spec', required=True)
        p.add_argument('--outdir', required=True)
    p = sub.add_parser('analyze-saved')
    p.add_argument('--scan-dir', required=True)
    p.add_argument('--out', required=True)
    p = sub.add_parser('replay-v004-reads')
    p.add_argument('--candidate-dir', required=True)
    p.add_argument('--outdir', required=True)
    p.add_argument('--launch', required=True)
    p.add_argument('--launch-sha256', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'replay-v004-reads':
        return cmd_replay_v004_reads(a.candidate_dir, a.outdir, a.launch, a.launch_sha256)
    if a.cmd == 'run':
        return cmd_run(a.spec, a.outdir)
    if a.cmd == 'dry-run':
        return cmd_dry_run(a.spec, a.outdir)
    return cmd_analyze_saved(a.scan_dir, a.out)


if __name__ == '__main__':
    sys.exit(main())
