"""Inherited-reference pressure bound; stdlib, no fits, stdout-only publication."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
WORKSPACE = PACKET.parent
OLD = HERE / 'COSMOLOGY_CLOSURE_ARITHMETIC.json'
PRODUCER = HERE / 'cosmology_closure_arithmetic.py'
SHAPE = PACKET / 'joint_parent_dynamics' / 'SHAPE_REFERENCE_RESULTS.json'
SHAPE_FREEZE = SHAPE.with_name('SHAPE_REFERENCE_FROZEN.json')
FREEZE = HERE / 'PRESSURE_BOUND_REFERENCE_V001_FROZEN.json'
OLD_SHA = '258097f5a80c8cfb4891d93e02a1f6224eb54b73014c276683f05c8b3989f153'
CONFIG = dict(epsilon=.001, c_m_s=299792458., mpc_km=3.085677581491367e19,
              wmax=[.001, .01, .1], tolerance=2e-12,
              synthetic_energies=[0., 1e-12, 1e-6, .01, 1., 10., 1000.],
              synthetic_w=[1e-6, .001, .01, .1, .3])


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    files, seen = {}, set()

    def add(path, expected=None):
        path = path.resolve(strict=True)
        if not path.is_relative_to(WORKSPACE):
            raise RuntimeError('Input outside the project: ' + str(path))
        digest = sha(path)
        if expected is not None and digest != expected:
            raise RuntimeError('Input identity mismatch: ' + str(path))
        files[str(path.relative_to(WORKSPACE))] = digest
        return path

    def authenticate_manifest(path):
        path = add(path)
        if path in seen:
            return
        seen.add(path)
        for name, digest in json.loads(path.read_text())['files'].items():
            child = add(path.parent / name, digest)
            if child.name.endswith('_FROZEN.json'):
                authenticate_manifest(child)

    add(OLD, OLD_SHA)
    old = json.loads(OLD.read_text())
    if old['status'] != 'AUTHENTICATED_REFERENCE_CLOSURE_DIAGNOSTIC':
        raise RuntimeError('Unexpected closure status')
    add(PRODUCER, old['script_sha256'])
    for rel, digest in old['input_sha256'].items():
        add(PACKET / rel, digest)
    authenticate_manifest(SHAPE_FREEZE)
    reference = json.loads(SHAPE.read_text())
    add(SHAPE)
    if (reference['freeze_sha256'] != sha(SHAPE_FREEZE)
            or reference['payload_sha256'] != hashlib.sha256(
                encoded(reference['payload'])).hexdigest()
            or not all(c['passed'] for c in reference['payload']['checks'])):
        raise RuntimeError('Unqualified shape-reference wrapper')
    for path in (Path(__file__), HERE / 'PRESSURE_BOUND_REFERENCE_PROTOCOL_V001.md',
                 HERE / 'SHARED_MODE_INFERENCE_AND_STATIC_CLOSURE_V001.md',
                 HERE / 'SHARED_MODE_INFERENCE_STATIC_REVIEW_V001.md',
                 HERE / 'COSMOLOGY_CLOSURE_TEST_V001.md'):
        add(path)
    wanted = {(i, name) for i in range(9) for name in
              ('Cooke2018_Marcucci_rate_eq12', 'Cooke2018_empirical_rate_eq14')}
    actual = [(r['reference_case'], r['bbn']['name']) for r in old['rows']]
    if len(actual) != 18 or set(actual) != wanted or len(reference['payload']['cases']) != 9:
        raise RuntimeError('Reference row census changed')
    return old, reference['payload']['cases'], dict(config=CONFIG, files=files)


def pressure_floor(energy, s4):
    if energy < 0 or s4 <= 0:
        raise ValueError('Pressure bound requires nonnegative energy and positive S4')
    return energy**2 / (math.sqrt(s4 + 3*energy) + math.sqrt(s4))**2


def energy_capacity(w, s4):
    if not 0 < w < 1/3:
        raise ValueError('Capacity requires 0<w<1/3')
    return 4*s4*w/(1-3*w)**2


def run():
    start = time.perf_counter()
    old, reference, snapshot = inputs()
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze differs')
    checks, failures, synthetic = [], [], []

    def check(name, left, right, inequality=False):
        scale = max(abs(left), abs(right)) or 1.
        difference = left-right
        error = (max(0., difference) if inequality else abs(difference))/scale
        passed = math.isfinite(error) and error <= CONFIG['tolerance']
        record = dict(name=name, normalized_error=error, scale=scale,
                      passed=passed, inequality=inequality)
        checks.append(record)
        if not passed:
            failures.append(dict(record, left=left, right=right))

    eps = CONFIG['epsilon']
    s4 = (1-eps**6)/6
    for energy in CONFIG['synthetic_energies']:
        pressure = pressure_floor(energy, s4)
        label = 'synthetic_E_' + str(energy)
        check(label+'_quadratic_identity', 2*math.sqrt(s4*pressure)+3*pressure, energy)
        check(label+'_nonnegative', 0., pressure, True)
        check(label+'_upper', pressure, energy/3, True)
        synthetic.append(dict(kind='bound_identity', E=energy, P_floor=pressure))
    for w in CONFIG['synthetic_w']:
        energy = energy_capacity(w, s4)
        check('synthetic_inverse_'+str(w), pressure_floor(energy, s4)/energy, w)
        synthetic.append(dict(kind='inverse_capacity', w=w, E_capacity=energy))
    weights, gaps = [.2, .3, .5], [.05, .4, .9]
    fixtures = [('saturated_moments', [d*d for d in gaps], [d**4 for d in gaps]),
                ('strict_moments', [.04, .25, 2.25], [.0064, .125, 10.125])]
    for name, second, fourth in fixtures:
        moment = math.fsum(w*d**4 for w, d in zip(weights, gaps))
        v2 = math.fsum(w*d*d*x/2 for w, d, x in zip(weights, gaps, second))
        pressure = math.fsum(w*x/4 for w, x in zip(weights, fourth))
        energy = 2*v2+3*pressure
        for i, (x, y) in enumerate(zip(second, fourth)):
            check(name+'_Jensen_'+str(i), x*x, y, True)
        check(name+'_Cauchy', v2, math.sqrt(moment*pressure), True)
        check(name+'_pressure_bound', pressure_floor(energy, moment), pressure, True)
        if name == 'saturated_moments':
            check(name+'_equality', pressure_floor(energy, moment), pressure)
        synthetic.append(dict(kind=name, weights=weights, gaps=gaps,
                              second_moments=second, fourth_moments=fourth,
                              S4=moment, V2=v2, P=pressure, E=energy))
    check('Hubble_conversion_km_vs_m', 73.6/CONFIG['mpc_km'],
          73.6*1000/(CONFIG['mpc_km']*1000))

    rows = []
    for index, row in enumerate(old['rows']):
        tag = 'row_'+str(index)
        ref = reference[row['reference_case']]
        if row['reference_input'] != ref['input']:
            raise RuntimeError('Original shape-reference input mismatch: '+tag)
        h0 = row['reference_input']['H0_km_s_Mpc']
        vacuum = row['reference_input']['Omega_Lambda_ref']
        a0 = row['reference_input']['a0_m_s2']
        omega_b = row['bbn']['omega_b']
        h_si = h0/CONFIG['mpc_km']
        gstar = a0/(8/(3*math.pi))
        coefficient = h0*h0*(1-vacuum)-10000*omega_b
        omega_required = coefficient/(h0*h0)
        check(tag+'_old_coefficient', coefficient,
              row['reference_H0_missing_coefficient_kmsMpc_squared'])
        check(tag+'_old_Omega', omega_required, row['reference_H0_missing_Omega'])
        check(tag+'_old_omega', coefficient/10000, row['reference_H0_missing_omega'])
        check(tag+'_vacuum', h0*h0*vacuum, row['vacuum_coefficient_kmsMpc_squared'])
        factor = .75*(1-eps*eps)*(CONFIG['c_m_s']*h_si/gstar)**2
        energy = factor*omega_required
        positive = energy > 0
        pressure = pressure_floor(energy, s4) if positive else None
        floor = pressure/energy if positive else None
        if positive:
            check(tag+'_bound_identity', 2*math.sqrt(s4*pressure)+3*pressure, energy)
            check(tag+'_pressure_upper', pressure, energy/3, True)
        capacities = []
        for wmax in CONFIG['wmax']:
            capacity = energy_capacity(wmax, s4)
            omega_capacity = capacity/factor
            ratio = energy/capacity if positive else None
            check(tag+'_capacity_inverse_'+str(wmax),
                  pressure_floor(capacity, s4)/capacity, wmax)
            if positive:
                check(tag+'_capacity_ratio_'+str(wmax), ratio,
                      omega_required/omega_capacity)
            capacities.append(dict(wmax_definition_not_observation=wmax,
                E_capacity=capacity, Omega_capacity=omega_capacity,
                positive_required_to_capacity=ratio))
        rows.append(dict(row_index=index, reference_case=row['reference_case'],
            reference_input=row['reference_input'], bbn=row['bbn'],
            inherited_reference_r=row['reference_r'], H0_s_inverse=h_si,
            inherited_relaxed_gstar_m_s2=gstar,
            baryon_Omega_at_reference_H0=10000*omega_b/(h0*h0),
            required_Omega_excitation=omega_required,
            E_per_unit_Omega=factor, required_dimensionless_energy=energy,
            positive_required_energy=positive,
            bound_applicable_to_positive_required_energy=positive,
            P_lower_bound=pressure, w_lower_bound=floor, capacities=capacities))
    check('output_row_census', len(rows), 18.)
    check('output_capacity_census', sum(len(r['capacities']) for r in rows), 54.)
    payload = dict(config=CONFIG, S4=s4, checks=checks, failures=failures,
        synthetic_controls=synthetic, rows=rows,
        source_scope=old['scope'], source_primary=old['external_primary'],
        scope=('Inherited relaxed calibration and standard-BBN reference diagnostic, '
               'not a new observation fit or an exclusion of all shared-state models. '
               'The three w thresholds are illustrative definitions, not data. '
               'A new excited-state inference must recompute its galaxy response and gstar.'),
        pressure_domain='Rapidly averaged bounded zero-source positive quartic modes; real excitation stress.')
    output = dict(status='COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
        freeze_sha256=sha(FREEZE), payload=payload,
        payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
        seconds=time.perf_counter()-start,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(output, allow_nan=False))
    return 1 if failures else 0


if __name__ == '__main__':
    if sys.argv[1:] == ['freeze']:
        print(json.dumps(inputs()[2], indent=2, allow_nan=False))
    elif sys.argv[1:]:
        raise SystemExit('Use freeze or no arguments')
    else:
        raise SystemExit(run())
