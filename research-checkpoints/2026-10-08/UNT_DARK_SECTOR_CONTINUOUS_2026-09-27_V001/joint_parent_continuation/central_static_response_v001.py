"""Same saved states: central scalar static response; stdout-only freeze/run."""
import os
for _key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
FREEZE = HERE / 'CENTRAL_STATIC_RESPONSE_V001_FROZEN.json'
CONFIG = dict(orders=[64, 128], simpson_panels=1024,
              arithmetic_tolerance=2e-11, quadrature_tolerance=2e-8,
              inherited_tolerance=2e-8, underflow_floor=1e-300,
              output_target_bytes=1048576,
              synthetic_gaps=[.25, 1., 128.],
              synthetic_quartic_amplitudes=[.25, 1., 3.])
PINS = {
    'PREPARED_ACTION_RETURN_V001_RESULTS.json': 'b8a0efd517e9492aa2546f83eb7cc81bb3a5553e22ff847f5c6f736b545b9678',
    'COMMON_HISTORY_MECHANISM_V001_RESULTS.json': 'e57f1f93254a610abc9b08ef5df355d74035efa762079ffd43e89205bc0f715a',
    'PREPARED_SUSCEPTIBILITY_V001_RESULTS.json': '0ce518ac17c84f0d116272597f9abb0ee5ab7bd41db8372699203ec9b7b21f40',
    'PREPARED_COMPRESSION_V001_RESULTS.json': 'a6fa29a21272c173d7cd3f8c2fa89894f1a3fce482c7ac6818991bff52392a2f',
    'HOMOGENEOUS_DILUTION_V001_RESULTS.json': '779ea9498572dc8bcbd3f9dc40b7610b097427dde9eb534dcb14345e1d8beb58',
    'HIGH_GAP_PULSE_V001_RESULTS.json': '3ff381351716259c36d3ef1cca01431e40a73c3deeabcf0bb24df27696617140',
    'POLARIZED_STATIC_RADIAL_REDUCTION_V001.md': 'fbfcf8ac1b4a2d9c9e15a95512d026231376a1f42ca6d4714f156ba828064b5f',
    'FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md': '51be129096bcb58641d0788a6a5af9d8e69b10232796e88ba8d1d4cddaa93bbb',
}


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(row):
    return tuple(row[k] for k in ('gap', 'mode_order', 'dt', 'duration', 'g'))


def inputs():
    files, seen = {}, set()

    def add(path, expected=None):
        path = path.resolve(strict=True)
        if not path.is_relative_to(PROJECT):
            raise RuntimeError('Source outside project: '+str(path))
        digest = sha(path)
        if expected is not None and digest != expected:
            raise RuntimeError('Source checksum differs: '+str(path))
        files[str(path.relative_to(PROJECT))] = digest
        return path

    def manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, expected in json.loads(path.read_text())['files'].items():
            target = Path(name)
            if not target.is_absolute():
                target = (PROJECT / target if target.parts[0] == HERE.parent.name
                          else path.parent / target)
            target = add(target, expected)
            if target.name.endswith('_FROZEN.json'):
                manifest(target)

    def wrapper(name):
        path = add(HERE / name, PINS[name])
        frozen = path.with_name(name.replace('_RESULTS.json', '_FROZEN.json'))
        manifest(frozen)
        value = json.loads(path.read_text())
        payload = value['payload']
        if (value['freeze_sha256'] != sha(frozen)
                or value['payload_sha256'] != hashlib.sha256(encode(payload)).hexdigest()):
            raise RuntimeError('Result wrapper mismatch: '+name)
        if value.get('status', 'COMPLETE') != 'COMPLETE' or payload.get('failures'):
            raise RuntimeError('Unqualified saved result: '+name)
        checks = payload.get('checks')
        if isinstance(checks, dict) and not all(v is True for v in checks.values()):
            raise RuntimeError('Inherited boolean check failed: '+name)
        if isinstance(checks, list) and not all(c['passed'] for c in checks):
            raise RuntimeError('Inherited numerical check failed: '+name)
        return payload

    data = {name: wrapper(name) for name in PINS if name.endswith('_RESULTS.json')}
    for name, digest in PINS.items():
        if not name.endswith('_RESULTS.json'):
            add(HERE / name, digest)
    add(Path(__file__))
    add(HERE / 'CENTRAL_STATIC_RESPONSE_PROTOCOL_V001.md')
    old = data['PREPARED_ACTION_RETURN_V001_RESULTS.json']
    expected = {(gap, order, dt, duration, g) for gap in (.001, .002)
                for order, dt in ((64, .01), (128, .01), (128, .005))
                for duration in (8, 16) for g in (.0025, .01, .04)}
    if len(old['rows']) != 36 or {identity(r) for r in old['rows']} != expected:
        raise RuntimeError('Original 36-state census differs')
    state_index = {(c['gap'], c['order'], c['dt'], c['duration']): c
                   for c in data['COMMON_HISTORY_MECHANISM_V001_RESULTS.json']['cases']}
    susceptibility = data['PREPARED_SUSCEPTIBILITY_V001_RESULTS.json']['rows']
    compression = data['PREPARED_COMPRESSION_V001_RESULTS.json']['rows']
    if (len(susceptibility) != 36 or len(compression) != 36
            or [identity(r) for r in susceptibility] != [identity(r) for r in old['rows']]
            or [identity(r) for r in compression] != [identity(r) for r in old['rows']]):
        raise RuntimeError('Inherited readout state identities differ')
    templates = []
    for index, row in enumerate(old['rows']):
        prior = state_index[(row['gap'], row['mode_order'], row['dt'], row['duration'])]
        md = row['mode_data']
        fine = [q for q in compression[index]['quadratures'] if q['order'] == 128]
        if len(fine) != 1:
            raise RuntimeError('Compression quadrature census differs')
        templates.append(dict(family='original_soft', input_index=index,
            identity={k: row[k] for k in ('gap', 'mode_order', 'dt', 'duration', 'g')},
            delta=prior['delta'], weights=prior['weights'], action=md['action'],
            energy=md['zero_source_energy'], pressure=md['zero_source_pressure'],
            omega=[2*math.pi/t for t in md['zero_source_period']],
            Kb=prior['Kb'], DeltaU=None, inherited_q=susceptibility[index]['modal_q'],
            inherited_eII=fine[0]['energy_curvature'],
            inherited_mu=susceptibility[index]['mu_linear']))
    pulse = data['HIGH_GAP_PULSE_V001_RESULTS.json']['cases']
    if (len(pulse) != 6 or {(r['gap'], r['amplitude']) for r in pulse}
            != {(r, a) for r in (32, 64, 128) for a in (1, 4)}):
        raise RuntimeError('Six-pulse census differs')
    for index, row in enumerate(pulse):
        md = row['fine_end_state']
        templates.append(dict(family='soft_plus_hard_pulse', input_index=index,
            identity={k: row[k] for k in ('gap', 'amplitude', 'cycles')},
            delta=md['delta'], weights=md['weights'], action=md['action'],
            energy=md['energy'], pressure=md['pressure'], omega=md['frequency'],
            Kb=row['finite_spectrum']['Kb'], DeltaU=row['finite_spectrum']['DeltaU'],
            inherited_q=md['contact_defect'], inherited_eII=None,
            inherited_mu=row['orbit_averaged']['mu_linear']))
    dilution = [r for r in data['HOMOGENEOUS_DILUTION_V001_RESULTS.json']['rows']
                if r['inverse_scale_factor'] == 1]
    if len(dilution) != 42 or [r['template_index'] for r in dilution] != list(range(42)):
        raise RuntimeError('Dilution present-state census differs')
    for index, (t, d) in enumerate(zip(templates, dilution)):
        if any(t[k] != d[k] for k in ('family', 'input_index', 'identity', 'Kb')):
            raise RuntimeError('Not the same dilution state: '+str(index))
        if t['DeltaU'] != d['unchanged_DeltaU']:
            raise RuntimeError('Finite-spectrum baseline differs')
        count = len(t['delta'])
        if any(len(t[k]) != count for k in ('weights', 'action', 'energy', 'pressure', 'omega', 'inherited_q')):
            raise RuntimeError('Modal shape mismatch')
        for key in ('delta', 'weights', 'action', 'energy', 'omega'):
            if not all(math.isfinite(v) and v > 0 for v in t[key]):
                raise RuntimeError('Nonpositive actual saved '+key)
        t['dilution'] = d
    return templates, dict(configuration=CONFIG, files=files,
        original_baseline=old['baseline'], census='36 returned plus six pulse, A=1 only')


def rule(order=None):
    if order is not None:
        z, w = leggauss(order)
        theta, weight = (z+1)*math.pi/4, w*math.pi/4
    else:
        n = CONFIG['simpson_panels']
        theta = np.linspace(0., math.pi/2, n+1)
        weight = np.ones(n+1)
        weight[1:-1:2] = 4
        weight[2:-1:2] = 2
        weight *= (math.pi/2/n)/3
    return weight, np.sin(theta)**2, np.cos(theta)**2


def orbit(delta, b2, quadrature, u=1.):
    weight, sine, cosine = quadrature
    k = delta[:, None]**2
    q = k+u*b2[:, None]*(1+sine)/2
    measure = weight/np.sqrt(q)
    j = np.sum(measure, axis=1)
    ell = np.sum(weight*(1+sine)/q**1.5, axis=1)
    omega = math.pi/(2*j)
    action = 2/math.pi*b2*np.sum(weight*cosine*np.sqrt(q), axis=1)
    energy = delta**2*b2/2+u*b2*b2/4
    pressure = u*b2*b2/4*np.sum(measure*sine*sine, axis=1)/j
    mean2 = b2*np.sum(measure*sine, axis=1)/j
    curvature = omega*omega*u*ell/(2*j*(delta**2+u*b2))
    return dict(action=action, omega=omega, energy=energy, pressure=pressure,
                mean2=mean2, eII=curvature)


def run():
    started = time.perf_counter()
    templates, snapshot = inputs()
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective source freeze differs')
    counts, maxima, absolute, failures = {}, {}, {}, []

    def check(name, left, right=0., scale=1., tolerance=None, tag=''):
        a, b, s = np.asarray(left), np.asarray(right), np.asarray(scale)
        error = np.abs(a-b)
        normalized = error/np.maximum(np.abs(s), CONFIG['underflow_floor'])
        worst = float(np.max(normalized))
        raw = float(np.max(error))
        tol = CONFIG['arithmetic_tolerance'] if tolerance is None else tolerance
        counts[name] = counts.get(name, 0)+int(normalized.size)
        maxima[name] = max(maxima.get(name, 0.), worst)
        absolute[name] = max(absolute.get(name, 0.), raw)
        if not np.all(np.isfinite(normalized)) or worst > tol:
            failures.append(dict(check=name, tag=tag, normalized_error=worst,
                                 absolute_error=raw, tolerance=tol))

    qlow, qhigh, qsimpson = rule(64), rule(128), rule()
    d = np.asarray(CONFIG['synthetic_gaps'])
    empty = orbit(d, np.zeros_like(d), qhigh)
    check('empty_positive_quartic_curvature', empty['eII'], 3/(4*d*d), 3/(4*d*d))
    harmonic = orbit(d, np.ones_like(d), qhigh, u=0.)
    check('harmonic_curvature', harmonic['eII'])
    check('harmonic_frequency', harmonic['omega'], d, d)
    b = np.asarray(CONFIG['synthetic_quartic_amplitudes'])
    quartic = orbit(np.zeros_like(b), b*b, qhigh)
    beta = math.gamma(.25)*math.gamma(1.5)/math.gamma(1.75)
    ia = math.sqrt(2)*beta*b**3/(4*math.pi)
    check('pure_quartic_action', quartic['action'], ia, ia)
    check('pure_quartic_pressure', quartic['pressure'], quartic['energy']/3, quartic['energy'])
    check('pure_quartic_curvature', quartic['eII'], quartic['omega']/(3*ia), quartic['eII'])
    check('pure_quartic_static_J', quartic['omega']**2/quartic['eII']+3*ia*quartic['omega'],
          8*quartic['energy'], 8*quartic['energy'])
    rows = []
    for index, t in enumerate(templates):
        delta, weight, action, e, p = (np.asarray(t[k]) for k in
            ('delta', 'weights', 'action', 'energy', 'pressure'))
        b2 = 4*e/(delta**2+np.sqrt(delta**4+4*e))
        high = orbit(delta, b2, qhigh)
        qdef = 3*(e+high['pressure'])/(delta**4+4*e)
        chi_B = delta**2*(delta**2+high['mean2'])/(delta**4+4*e)
        modal_J = high['omega']**2/high['eII']+3*action*high['omega']
        Kb, Kcal, J = t['Kb'], float(weight@qdef), float(weight@modal_J)
        E, Pi = float(weight@e), float(weight@p)
        tag = str(index)
        check('contact_weight', np.sum(weight), Kb, Kb, tag=tag)
        check('energy_reconstruction', high['energy'], e, e, tag=tag)
        check('virial', delta**2*high['mean2']+3*high['pressure'], e, e, tag=tag)
        check('action_pressure', high['action']*high['omega'], e+high['pressure'], e, tag=tag)
        check('source_sum_rule', qdef+chi_B, 1., tag=tag)
        check('positive_curvature', np.minimum(high['eII'], 0.), tag=tag)
        check('defect_lower', np.minimum(qdef-b2/(delta**2+b2), 0.), tag=tag)
        upper = b2*(2*delta**2+b2)/(delta**2+b2)**2
        check('defect_upper', np.maximum(qdef-upper, 0.), tag=tag)
        tol = CONFIG['inherited_tolerance']
        for name, actual, saved, scale in (
            ('action', high['action'], action, action),
            ('pressure', high['pressure'], p, e),
            ('frequency', high['omega'], t['omega'], high['omega']),
            ('deficit', qdef, t['inherited_q'], qdef)):
            check('inherited_'+name, actual, saved, scale, tol, tag)
        check('inherited_mu', Kcal/Kb, t['inherited_mu'], Kcal/Kb, tol, tag)
        if t['inherited_eII'] is not None:
            check('inherited_compression_curvature', high['eII'], t['inherited_eII'], high['eII'], tol, tag)
        prior = t['dilution']
        for name, actual, saved in (('E', E, prior['E']), ('P', Pi, prior['P'])):
            check('dilution_'+name, actual, saved, E, tol, tag)
        check('dilution_frequency', high['omega'], prior['modal_frequency'], high['omega'], tol, tag)
        comparisons = []
        for label, quadrature in (('GL64', qlow), ('Simpson1024', qsimpson)):
            other = orbit(delta, b2, quadrature)
            other_q = 3*(e+other['pressure'])/(delta**4+4*e)
            other_J = other['omega']**2/other['eII']+3*action*other['omega']
            errors = {}
            for name in ('action', 'omega', 'eII', 'pressure'):
                scale = e if name == 'pressure' else high[name]
                check(label+'_'+name, other[name], high[name], scale, CONFIG['quadrature_tolerance'], tag)
                errors[name] = dict(absolute=float(np.max(abs(other[name]-high[name]))),
                    normalized=float(np.max(abs(other[name]-high[name])/scale)))
            check(label+'_deficit', other_q, qdef, qdef, CONFIG['quadrature_tolerance'], tag)
            check(label+'_J', other_J, modal_J, modal_J, CONFIG['quadrature_tolerance'], tag)
            comparisons.append(dict(rule=label, errors=errors, E=float(weight@other['energy']),
                Pi=float(weight@other['pressure']), Kcal=float(weight@other_q),
                J_static=float(weight@other_J)))
        component_masks = [('all', np.ones(len(delta), dtype=bool))]
        if t['family'] == 'soft_plus_hard_pulse':
            component_masks.extend([('soft', delta <= 1), ('hard', delta > 1)])
        components = {name: dict(weight=float(np.sum(weight[mask])),
            E=float(weight[mask]@e[mask]), Pi=float(weight[mask]@p[mask]),
            Kcal=float(weight[mask]@qdef[mask]), J_static=float(weight[mask]@modal_J[mask]))
            for name, mask in component_masks}
        center = None
        if t['DeltaU'] is not None:
            du = t['DeltaU']
            source = E+3*Pi-2*du
            a1 = source/(3*Kcal)
            s2 = -a1+(Pi-du)/Kb
            fa = float(weight@chi_B)
            rho = E+du+3*fa*a1
            check('center_mass_constraint', rho, -3*Kb*s2,
                  max(abs(rho), abs(3*Kb*s2), E+du), tag=tag)
            center = dict(DeltaU=du, active_center_source=source, a1=a1, s2=s2,
                          rho_center_over_C=rho, ordinary_matter='absent')
        rows.append(dict(template_index=index, family=t['family'], input_index=t['input_index'],
            identity=t['identity'], modal_count=len(delta), Kb=Kb, E=E, Pi=Pi, Pi_over_E=Pi/E,
            excitation_active_source=E+3*Pi, Kcal=Kcal, mu_linear=Kcal/Kb,
            J_static=J, static_wavenumber_squared=J/Kcal, center=center,
            center_unavailable_reason=None if center is not None else 'No numeric same-finite-spectrum DeltaU in selected returned-state inputs; no baseline substituted.',
            components=components, quadrature_controls=comparisons,
            modal_eII=high['eII'].tolist(), modal_contact_defect=qdef.tolist(),
            modal_J_static=modal_J.tolist()))
    indexed = {identity(r['identity']): r for r in rows if r['family'] == 'original_soft'}
    sensitivities = []
    for gap in (.001, .002):
        for duration in (8, 16):
            for g in (.0025, .01, .04):
                for left, right, label in (((64, .01), (128, .01), 'saved_spectral_order'),
                                           ((128, .01), (128, .005), 'saved_preparation_step')):
                    a, b = indexed[(gap, *left, duration, g)], indexed[(gap, *right, duration, g)]
                    sensitivities.append(dict(gap=gap, duration=duration, g=g, label=label,
                        left_template=a['template_index'], right_template=b['template_index'],
                        signed_right_minus_left={k: b[k]-a[k] for k in
                            ('E', 'Pi', 'Kcal', 'J_static', 'static_wavenumber_squared')}))
    check('state_census', len(rows), 42)
    check('owned_center_census', sum(r['center'] is not None for r in rows), 6)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        peak *= 1024
    payload = dict(configuration=CONFIG, rows=rows, sensitivity_comparisons=sensitivities,
        check_counts=counts, maximum_normalized_errors=maxima, maximum_absolute_errors=absolute,
        failures=failures, original_baseline=snapshot['original_baseline'],
        scope='Same-action zero-source scalar static diagnostic; not a vector galaxy solution, selected radius, dynamical growth rate or phase equilibration.',
        zero_action_rule='Exactly unoccupied copies have no repopulation J; the occupied I->0+ limit differs. No saved action is dropped.',
        seconds=time.perf_counter()-started, peak_rss_bytes=int(peak))
    payload['output_target_exceeded'] = len(encode(payload)) > CONFIG['output_target_bytes']
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS',
        freeze_sha256=sha(FREEZE), payload_sha256=hashlib.sha256(encode(payload)).hexdigest(), payload=payload)


def main():
    if sys.argv[1:] == ['freeze']:
        output = inputs()[1]
    elif sys.argv[1:] == ['run']:
        output = run()
    else:
        raise ValueError('usage: central_static_response_v001.py freeze|run')
    print(encode(output).decode())
    return 0 if output.get('status', 'COMPLETE') == 'COMPLETE' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(encode(dict(status='ERROR', error_type=type(exc).__name__, error=str(exc))).decode())
        sys.exit(1)
