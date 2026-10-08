"""Prospective global-gap LIMIT calibration; stdout only, no mode evolution."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE / 'GLOBAL_GAP_LIMIT_CALIBRATION_V001_FROZEN.json'
PINS = {
    'COMMON_HISTORY_MECHANISM_V001_RESULTS.json':
        'e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a',
    'ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json':
        '1b155c6caf7ceb721db2f8766fa282b456b8c5f40d49555052ab4b0dc9a06abd',
    'COSMOLOGY_CLOSURE_ARITHMETIC.json':
        '258097f5a80c8cfb4891d93e02a1f6224eb54b73014c276683f05c8b3989f153',
    'GLOBAL_HARD_GAP_SHARED_FEASIBILITY_V001.md':
        '683bf955a6f70b39cb4a247c01c309db0580faae5b8b06acdd742ca9510bb08d',
}
CONFIG = dict(beta=.005, cycles=8, exposed_a0_m_s2=1.2e-10,
    c_m_s=299792458., mpc_km=3.085677581491367e19,
    gaps=[.001, .002], orders=[64, 128],
    physical_field_probes_m_s2=[1e-12, 1e-10, 1e-8],
    bisections=80, relative_tolerance=2e-11, zero_tolerance=2e-12,
    synthetic_delta=[.001, .2, 1.], synthetic_source=[0., .01, 1.],
    expected_spectra=4, expected_references=18, expected_branches=72,
    output_target_bytes=1048576)


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(x):
    return hashlib.sha256(encode(x)).hexdigest()


def sha(path):
    path = path.resolve(strict=True)
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authenticate():
    files, seen = {}, set()

    def add(path, expected=None):
        path = path.resolve(strict=True)
        value = sha(path)
        if expected is not None and value != expected:
            raise RuntimeError('Inherited identity differs: ' + str(path))
        files[str(path.relative_to(ROOT))] = value
        return path

    def resolve(name, parent):
        value = Path(name)
        if value.is_absolute():
            return add(value)
        matches = set()
        for base in (parent, ROOT):
            candidate = (base / value).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                continue
            if candidate.is_file():
                matches.add(candidate)
        if len(matches) != 1:
            raise RuntimeError('Missing or ambiguous frozen member: ' + name)
        return matches.pop()

    def manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, expected in json.loads(path.read_text())['files'].items():
            member = add(resolve(name, path.parent), expected)
            if member.name.endswith('_FROZEN.json'):
                manifest(member)

    def result(name):
        path = add(HERE / name, PINS[name])
        value = json.loads(path.read_text())
        freeze = path.with_name(name.replace('_RESULTS.json', '_FROZEN.json'))
        manifest(freeze)
        p = value['payload']
        if value['freeze_sha256'] != sha(freeze) or value['payload_sha256'] != digest(p):
            raise RuntimeError('Result wrapper differs: ' + name)
        checks = p['checks']
        valid = (checks['failed'] == 0 and not checks['failure_names']) if 'failed' in checks else all(
            isinstance(v, bool) and v for v in checks.values())
        if not valid or p.get('status', 'COMPLETE') != 'COMPLETE':
            raise RuntimeError('Unqualified inherited result: ' + name)
        return p

    history = result('COMMON_HISTORY_MECHANISM_V001_RESULTS.json')
    calibration = result('ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json')
    name = 'COSMOLOGY_CLOSURE_ARITHMETIC.json'
    closure = json.loads(add(HERE / name, PINS[name]).read_text())
    if closure['status'] != 'AUTHENTICATED_REFERENCE_CLOSURE_DIAGNOSTIC':
        raise RuntimeError('Reference status differs')
    add(HERE / 'cosmology_closure_arithmetic.py', closure['script_sha256'])
    for name, expected in closure['input_sha256'].items():
        path = add(HERE.parent / name, expected)
        if path.name.endswith('_FROZEN.json'):
            manifest(path)
    for name in (Path(__file__).name, 'GLOBAL_GAP_LIMIT_CALIBRATION_PROTOCOL_V001.md',
                 'GLOBAL_HARD_GAP_SHARED_FEASIBILITY_V001.md',
                 'HIGH_GAP_SHARED_SPECTRUM_CANDIDATE_V001.md',
                 'HIGH_GAP_PULSE_PROTOCOL_V001.md'):
        add(HERE / name, PINS.get(name))
    spectra = {}
    expected_cases = {(eps, n, dt, t) for eps in CONFIG['gaps']
        for n, dt in ((64, .01), (128, .01), (128, .005)) for t in (8, 16)}
    actual = {(c['gap'], c['order'], c['dt'], c['duration']) for c in history['cases']}
    if actual != expected_cases or len(history['cases']) != 12:
        raise RuntimeError('History source census differs')
    for c in history['cases']:
        key = c['gap'], c['order']
        values = dict(delta=c['delta'], weights=c['weights'])
        if len(c['delta']) != c['order'] or len(c['weights']) != c['order']:
            raise RuntimeError('Spectrum length differs')
        if not all(math.isfinite(v) and v > 0 for a in values.values() for v in a):
            raise RuntimeError('Nonpositive spectrum')
        if key in spectra:
            if spectra[key]['spectrum'] != values:
                raise RuntimeError('Old dt/duration copies have distinct spectra')
        else:
            spectra[key] = dict(gap=key[0], order=key[1], spectrum=values, copies=[])
        spectra[key]['copies'].append(dict(dt=c['dt'], duration=c['duration']))
    if set(spectra) != {(e, n) for e in CONFIG['gaps'] for n in CONFIG['orders']}:
        raise RuntimeError('Distinct spectrum census differs')
    refs = calibration['references']
    if len(refs) != 18 or {r['reference'] for r in refs} != set(range(18)) or len(closure['rows']) != 18:
        raise RuntimeError('Reference census differs')
    for r in refs:
        old = closure['rows'][r['reference']]
        if r['inherited_reference_input'] != old['reference_input'] or r['bbn'] != old['bbn']:
            raise RuntimeError('Reference metadata differs')
    snapshot = dict(configuration=CONFIG, files=files,
        spectrum_identities={f'{e}:{n}': digest(s['spectrum']) for (e, n), s in sorted(spectra.items())},
        reference_scope=closure['scope'], reference_assumptions=closure['assumptions'])
    return [spectra[k] for k in sorted(spectra)], refs, closure, snapshot


def cubic(delta, h):
    return 2 * delta / math.sqrt(3) * math.sinh(
        math.asinh(3 * math.sqrt(3) * h / (2 * delta * delta)) / 3)


def cubic_bisect(delta, h):
    if h == 0:
        return 0.
    sign = 1. if h > 0 else -1.
    h = abs(h)
    lo, hi = 0., min(h / delta, (delta * h) ** (1 / 3))
    for _ in range(CONFIG['bisections']):
        mid = (lo + hi) / 2
        if mid * (delta * delta + mid * mid) < delta * h:
            lo = mid
        else:
            hi = mid
    return sign * (lo + hi) / 2


def endpoint(delta, weights, h, oracle=False):
    ys = [(cubic_bisect if oracle else cubic)(d, h) for d in delta]
    q = math.fsum(w * (.5*d*d*y*y + .75*y**4) for d, w, y in zip(delta, weights, ys))
    return q + CONFIG['beta'] * h*h / 2, ys


def solve(delta, weights, target):
    lo, hi = 0., math.sqrt(2 * target / CONFIG['beta'])
    for _ in range(CONFIG['bisections']):
        mid = (lo + hi) / 2
        if endpoint(delta, weights, mid)[0] < target:
            lo = mid
        else:
            hi = mid
    s = (lo + hi) / 2
    return s, (hi - lo) / s


def run(spectra, refs, closure):
    start = time.perf_counter()
    counts, maxima, failures, rows = {}, {}, [], []

    def check(name, a, b=0., zero=False):
        scale = max(1., abs(a), abs(b)) if zero else max(abs(a), abs(b), 1e-300)
        error = abs(a - b) / scale
        tol = CONFIG['zero_tolerance'] if zero else CONFIG['relative_tolerance']
        counts[name] = counts.get(name, 0) + 1
        maxima[name] = max(maxima.get(name, 0.), error)
        if not math.isfinite(error) or error > tol:
            failures.append(dict(check=name, error=error, tolerance=tol))

    def check_modes(delta, ys, h):
        for d, y in zip(delta, ys):
            check('cubic_residual', y*(d*d+y*y), d*h, zero=(h == 0))
            check('independent_cubic', y, cubic_bisect(d, h), zero=(h == 0))

    for d in CONFIG['synthetic_delta']:
        for h in CONFIG['synthetic_source']:
            y = cubic(d, h)
            check_modes([d], [y], h)
            check('cubic_parity', cubic(d, -h), -y, zero=True)
    beta = CONFIG['beta']
    cp = math.pi**2 * CONFIG['cycles']**2 / 8
    for spectrum_index, spec in enumerate(spectra):
        delta, weights = (spec['spectrum'][key] for key in ('delta', 'weights'))
        ws = math.fsum(weights)
        kb = ws + beta
        a0dim = 16 * kb / (3 * math.pi)
        gstar = CONFIG['exposed_a0_m_s2'] / a0dim
        check('soft_measure_mass', ws, (1-spec['gap']**2)/2)
        check('calibrated_exposed_coefficient', gstar*a0dim, CONFIG['exposed_a0_m_s2'])
        for ref in refs:
            h0 = ref['H0_s_inverse']
            oe, ol = ref['Omega_exc'], ref['Omega_Lambda']
            check('inherited_H0_units', h0,
                  ref['inherited_reference_input']['H0_km_s_Mpc']/CONFIG['mpc_km'])
            if min(h0, oe, ol) <= 0:
                rows.append(dict(spectrum_index=spectrum_index, reference=ref['reference'],
                                 status='NONPOSITIVE_REFERENCE_DOMAIN'))
                continue
            ch = CONFIG['c_m_s']*h0
            energy = 3*kb*oe*ch*ch/(2*gstar*gstar)
            hp = math.sqrt(energy/(beta*cp))
            target = energy*ol/oe
            s, width = solve(delta, weights, target)
            q, ys = endpoint(delta, weights, s)
            qhp, yhp = endpoint(delta, weights, hp)
            check_modes(delta, ys, s)
            check_modes(delta, yhp, hp)
            wel = math.fsum(w*(.5*(s-d*y)**2 + .25*y**4) for d, w, y in zip(delta, weights, ys))
            base = kb*s*s/2
            defect = wel/base
            derivative = math.fsum(w*d*y for d, w, y in zip(delta, weights, ys)) + beta*s
            check('endpoint_target', q, target)
            check('endpoint_bracket', width, 0., zero=True)
            check('contact_endpoint_identity', q+wel, base)
            check('excitation_reconstruction', 2*gstar*gstar*energy/(3*kb*ch*ch), oe)
            check('vacuum_reconstruction', 2*gstar*gstar*q/(3*kb*ch*ch), ol)
            check('pulse_limit_energy', beta*cp*hp*hp, energy)
            check('gs_identity', (gstar*s)**2*(1-defect), 3*ol*ch*ch)
            check('source_ordering_identity', float(hp < s), float(qhp < target), zero=True)
            exact_source = hp < s
            upper_scales = dict(soft_upper_G=1., bounded_source_G=s,
                saturation_quadratic_crossover_G=s*s/(2*a0dim),
                upper_cutoff_cubic_crossover_G=3*math.pi/8)
            probes = []
            for physical in CONFIG['physical_field_probes_m_s2']:
                g = physical/gstar
                z = (g/s)**2
                h, hp_g = g/math.sqrt(1+z), (1+z)**-1.5
                yy = [cubic(d, h) for d in delta]
                check_modes(delta, yy, h)
                fs = math.fsum(w*y**3/d for d, w, y in zip(delta, weights, yy))
                pol = math.fsum(w*d*y for d, w, y in zip(delta, weights, yy))
                contact = g*z*(2+z)/(1+z)**2
                response = contact + hp_g*fs/kb
                direct = g-hp_g*(pol+beta*h)/kb
                check('source_deficit_identity', fs+pol, ws*h)
                check('constitutive_direct_identity', response, direct)
                predicted = gstar*response
                probes.append(dict(g_m_s2=physical, G=g, h=h, hprime=hp_g,
                    gN_m_s2=predicted, D=response, mu=response/g,
                    g_over_gN=g/response if response != 0 else None,
                    D_over_formal_quadratic=response/(g*g/a0dim),
                    bounded_source_contact=contact, soft_deficit_term=hp_g*fs/kb,
                    window_ratios=dict(lower_cutoff_epsilon2_over_h=spec['gap']**2/h,
                        actual_node_min2_over_h=min(delta)**2/h, soft_upper_h=h,
                        G_over_S=g/s, saturation_cubic_over_quadratic=2*a0dim*g/(s*s),
                        upper_cutoff_cubic_over_quadratic=a0dim*g/(2*kb)),
                    continuum_lower_cutoff_deficit_bound=spec['gap']**2*h*hp_g/(2*kb),
                    scope='Exact scalar limiting-parent field probe; not observed rotation or isotropic-vector closure'))
            rows.append(dict(spectrum_index=spectrum_index, reference=ref['reference'],
                status='CALIBRATED_SOURCE_REALIZABLE' if exact_source else 'CALIBRATED_SOURCE_UNREALIZABLE',
                Kb=kb, soft_weight=ws, a0_dimensionless=a0dim, gstar_m_s2=gstar,
                exposed_a0_m_s2=CONFIG['exposed_a0_m_s2'], E_required=energy,
                Hp=hp, S=s, gs_m_s2=gstar*s, Hp_over_S=hp/s,
                DeltaU_limit=q, target_DeltaU=target,
                endpoint_relative_bracket_width=width, endpoint_relative_condition=target/(s*derivative),
                matched_vacuum_deficit_fraction=defect,
                source_certificate=dict(exact_target_minus_Q_at_Hp=target-qhp,
                    exact_Hp_less_than_S=exact_source,
                    sufficient_margin=beta*cp*ol/oe-kb/2,
                    sufficient_condition=beta*cp*ol/oe > kb/2),
                window=dict(lower_continuum_scale_G=spec['gap']**2,
                    strict_discrete_smallest_node_squared=min(delta)**2,
                    upper_scales_G=upper_scales, nominal_upper_G=min(upper_scales.values()),
                    nominal_upper_over_lower=min(upper_scales.values())/spec['gap']**2,
                    physical_lower_scale_m_s2=gstar*spec['gap']**2,
                    physical_nominal_upper_m_s2=gstar*min(upper_scales.values()),
                    qualification='Much-less-than asymptotic scales, not a tolerance-certified field interval'),
                strict_discrete_zero_field_cubic=2/(s*s)+math.fsum(w/d**4 for d, w in zip(delta, weights))/kb,
                ordered_continuum_cubic=2/(s*s)-1/(2*kb), field_probes=probes,
                preparation='Formal R->infinity common-pulse family; no finite-R state has been generated'))
    check('branch_census', len(rows), CONFIG['expected_branches'], zero=True)
    comparisons = []
    for eps in CONFIG['gaps']:
        ids = {s['order']:i for i, s in enumerate(spectra) if s['gap'] == eps}
        for ref in refs:
            pair = [next(r for r in rows if r['spectrum_index'] == ids[n] and r['reference'] == ref['reference']) for n in CONFIG['orders']]
            if any('S' not in r for r in pair):
                comparisons.append(dict(gap=eps, reference=ref['reference'], status='NONPOSITIVE_REFERENCE_DOMAIN'))
                continue
            a, b = pair
            comparisons.append(dict(gap=eps, reference=ref['reference'],
                S_fine_minus_coarse=b['S']-a['S'], Hp_fine_minus_coarse=b['Hp']-a['Hp'],
                field_response_relative_differences=[(v['D']-u['D'])/v['D'] for u, v in zip(a['field_probes'], b['field_probes'])],
                qualification='Complete64/128 comparison; descriptive, no resolution selected'))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        peak *= 1024
    return dict(status='COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
        configuration=CONFIG, Cp=cp, spectra=spectra, references=refs, rows=rows,
        resolution_comparisons=comparisons, check_counts=counts, maximum_errors=maxima, failures=failures,
        inherited_reference_scope=closure['scope'], inherited_reference_assumptions=closure['assumptions'],
        external_primary=closure['external_primary'],
        scope='Exposed formal-acceleration calibration of a NEW limiting family; not unused observational evidence, finite-R preparation, isotropic-vector closure, clock qualification or galaxy fit',
        seconds=time.perf_counter()-start, peak_self_rss_bytes=int(peak))


def main():
    if sys.argv[1:] not in (['freeze'], ['run']):
        raise SystemExit('Use freeze or run; stdout only')
    spectra, refs, closure, snapshot = authenticate()
    if sys.argv[1:] == ['freeze']:
        print(encode(snapshot).decode())
        return
    if encode(json.loads(FREEZE.read_text())) != encode(snapshot):
        raise RuntimeError('Prospective source freeze differs')
    payload = run(spectra, refs, closure)
    output = dict(freeze_sha256=sha(FREEZE), payload_sha256=digest(payload), payload=payload,
                  within_output_target=len(encode(payload)) <= CONFIG['output_target_bytes'])
    print(encode(output).decode())
    if payload['status'] != 'COMPLETE':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
