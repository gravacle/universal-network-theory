"""Prospective finite-band compensated-clock transfer; stdout only."""
import os
for _thread in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_thread] = '1'
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE / 'COSMOLOGICAL_CLOCK_EVOLUTION_V001_FROZEN.json'
HELPER = HERE / 'global_gap_limit_calibration_v001.py'
HELPER_SHA = '7bb8bbd452b68b460720342e0e0b4043096c746ad5a3bfbcba1e30ee1e502e24'
PINS = {
    'HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md':
        'c501fc2aeebe0cf389ad9c21c5c7fdd3240209a1d9dd0ae710ed45d67bb8003d',
    'PAIRED_HARD_MODE_STATE_V001.md':
        '7461324e5c40de23f796c9e438a9d1cbecd88ffcc9bdb2c21c8e05fd54a38c91',
}
CONFIG = dict(reference=0, beta=.005, etas=[.001, .1, 1.],
    a_start=.001, a_end=2., log_samples=61,
    full_state_scale_factors=[.001, .01, .1, 1., 2.],
    primary_rtol=2e-10, primary_atol=2e-12,
    repeat_rtol=5e-11, repeat_atol=5e-13,
    dopri_max_log_step=.025, dopri_max_coupled_phase=.35,
    rk4_max_log_step=.0025, rk4_max_coupled_phase=.02,
    arithmetic_tolerance=2e-12, repeat_tolerance=2e-7,
    independent_tolerance=2e-5, expected_cases=12,
    linear_tilt_display_threshold=.01, output_target_bytes=8388608)


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(x):
    return hashlib.sha256(encode(x)).hexdigest()


def sha(path):
    path = path.resolve(strict=True)
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authenticate():
    if sha(HELPER) != HELPER_SHA:
        raise RuntimeError('Reviewed custody helper changed')
    spec = importlib.util.spec_from_file_location('clock_custody_only', HELPER)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    # Only its read-only authentication function is called; no old run function.
    spectra, refs, closure, inherited = helper.authenticate()
    ref = next(r for r in refs if r['reference'] == CONFIG['reference'])
    if ref['reference_case'] != 0 or ref['Omega_b'] <= 0:
        raise RuntimeError('Prespecified central reference differs')
    files = dict(inherited['files'])
    for name in (Path(__file__).name, 'COSMOLOGICAL_CLOCK_EVOLUTION_PROTOCOL_V001.md',
                 'HARD_LIMIT_NONVACUUM_SCALAR_INTERFACE_V001.md',
                 'HARD_LIMIT_DUST_INTERFACE_WITH_ORDINARY_RADIATION_V001.md',
                 'PAIRED_HARD_MODE_STATE_V001.md',
                 'HARD_LIMIT_NONVACUUM_INTERFACE_SECOND_REVIEW_V001.md',
                 'PAIRED_HARD_MODE_STATE_REVIEW_V001.md'):
        path = HERE / name
        value = sha(path)
        if name in PINS and value != PINS[name]:
            raise RuntimeError('Reviewed analytical source differs: ' + name)
        files[str(path.relative_to(ROOT))] = value
    cases = [dict(case=i, spectrum_index=j, gap=s['gap'], order=s['order'], eta=eta)
             for i, (j, s, eta) in enumerate(
                 (j, s, eta) for j, s in enumerate(spectra) for eta in CONFIG['etas'])]
    if len(cases) != CONFIG['expected_cases']:
        raise RuntimeError('Case census differs')
    snapshot = dict(configuration=CONFIG, files=files, cases=cases, reference=ref,
        spectrum_identities=inherited['spectrum_identities'],
        inherited_reference_scope=closure['scope'],
        inherited_reference_assumptions=closure['assumptions'])
    return spectra, ref, snapshot


class Checks:
    def __init__(self):
        self.counts, self.maxima, self.failures = {}, {}, []

    def add(self, name, error, tolerance):
        error = float(error)
        self.counts[name] = self.counts.get(name, 0) + 1
        self.maxima[name] = max(self.maxima.get(name, 0.), error)
        if not math.isfinite(error) or error > tolerance:
            self.failures.append(dict(check=name, error=error, tolerance=tolerance))

    def arithmetic(self, name, a, b, scale=None):
        a, b = np.asarray(a), np.asarray(b)
        denominator = np.maximum(1., np.maximum(np.abs(a), np.abs(b))) if scale is None else scale
        self.add(name, np.max(np.abs(a-b)/denominator), CONFIG['arithmetic_tolerance'])

    def output(self):
        return dict(counts=self.counts, maximum_errors=self.maxima, failures=self.failures)


def background(loga, ref):
    a = math.exp(loga)
    matter = (ref['Omega_b']+ref['Omega_exc'])/a**3
    h = math.sqrt(matter+ref['Omega_Lambda'])
    d = -1.5*matter/(h*h)  # d ln(H/H0)/d ln a = Hdot/H^2.
    return a, h, d


def rhs_factory(delta, weights, eta, ref, transformed=False, slow=False):
    n = len(delta)
    beta = CONFIG['beta']
    kb = float(np.sum(weights))+beta
    freq0sq = (delta/eta)**2

    def rhs(loga, state):
        a, h, d = background(loga, ref)
        out = np.empty_like(state)
        u, w = state[0], state[1]
        out[0] = w
        if slow:
            mass = 1.5*ref['Omega_exc']/(a**3*h*h)
            out[1] = -(3+d)*w-(d+2-mass)*u
            return out
        z, zn = state[2:2+n], state[2+n:]
        total = weights @ (zn+2*z)
        mass = 1.5*kb*ref['Omega_exc']/(beta*a**3*h*h)
        freq2 = freq0sq/(h*h)
        if transformed:
            # Independently integrate Vc=a*u and its ln(a) derivative.
            out[1] = -(1+d)*w+mass*u-a*total/(beta*h)
            source = h*w/a
        else:
            out[1] = -(3+d)*w-(d+2-mass)*u-total/(beta*h)
            source = h*(w+u)
        out[2:2+n] = zn
        out[2+n:] = -(3+d)*zn-freq2[:, None]*z+freq2[:, None]*source
        return out
    return rhs


# Dormand-Prince 5(4), with the embedded fourth-order endpoint retained.
DP_C = (0., 1/5, 3/10, 4/5, 8/9, 1., 1.)
DP_A = ((), (1/5,), (3/40, 9/40),
    (44/45, -56/15, 32/9),
    (19372/6561, -25360/2187, 64448/6561, -212/729),
    (9017/3168, -355/33, 46732/5247, 49/176, -5103/18656),
    (35/384, 0., 500/1113, 125/192, -2187/6784, 11/84))
DP_B4 = (5179/57600, 0., 7571/16695, 393/640,
         -92097/339200, 187/2100, 1/40)


def dopri(rhs, initial, nodes, cap, rtol, atol):
    state, x = initial.copy(), float(nodes[0])
    saved, counts = [state.copy()], dict(accepted=0, rejected=0, rhs_evaluations=0)
    step = min(.001, cap(x, float(nodes[-1])))
    for target in nodes[1:]:
        target = float(target)
        while x < target:
            step = min(step, target-x, cap(x, target))
            if x+step == x or not math.isfinite(step) or step <= 0:
                raise RuntimeError('DOPRI step reached floating-point resolution')
            stages = []
            for c, row in zip(DP_C, DP_A):
                trial = state.copy()
                for coefficient, k in zip(row, stages):
                    trial += step*coefficient*k
                stages.append(rhs(x+c*step, trial))
            counts['rhs_evaluations'] += 7
            high = state.copy()
            low = state.copy()
            for coefficient, k in zip(DP_A[-1], stages):
                high += step*coefficient*k
            for coefficient, k in zip(DP_B4, stages):
                low += step*coefficient*k
            scale = atol+rtol*np.maximum(np.abs(state), np.abs(high))
            error = float(np.max(np.abs(high-low)/scale))
            if not math.isfinite(error) or not np.all(np.isfinite(high)):
                raise RuntimeError('Nonfinite DOPRI trial')
            factor = 5. if error == 0 else min(5., max(.2, .9*error**(-.2)))
            if error <= 1:
                state = high
                x = target if step == target-x else x+step
                counts['accepted'] += 1
            else:
                counts['rejected'] += 1
            step *= factor
        saved.append(state.copy())
    return np.asarray(saved), counts


def rk4(rhs, initial, nodes, cap):
    state, x = initial.copy(), float(nodes[0])
    saved, steps = [state.copy()], 0
    for target in nodes[1:]:
        target = float(target)
        subdivisions = max(1, math.ceil((target-x)/cap(x, target)))
        step = (target-x)/subdivisions
        for j in range(subdivisions):
            here = x+j*step
            k1 = rhs(here, state)
            k2 = rhs(here+step/2, state+step*k1/2)
            k3 = rhs(here+step/2, state+step*k2/2)
            k4 = rhs(here+step, state+step*k3)
            state += (step/6)*(k1+2*k2+2*k3+k4)
            steps += 1
            if not np.all(np.isfinite(state)):
                raise RuntimeError('Nonfinite independent RK4 state')
        x = target
        saved.append(state.copy())
    return np.asarray(saved), dict(steps=steps, rhs_evaluations=4*steps)


def compare(checks, name, a, b, tolerance):
    # Every state coordinate/basis column has its own full sampled-trajectory scale.
    scales = np.maximum(1., np.maximum(np.max(np.abs(a), axis=0), np.max(np.abs(b), axis=0)))
    errors = np.abs(a-b)/scales[None, :, :]
    checks.add(name, np.max(errors), tolerance)
    return dict(maximum_scaled_error=float(np.max(errors)),
        per_coordinate_and_basis_maximum_errors=np.max(errors, axis=0).tolist(),
        scale_definition='max(1, peak absolute coordinate over all saved times in either solve)')


def numerical_controls(ref, nodes, checks):
    for c, row in zip(DP_C, DP_A):
        checks.arithmetic('dopri_row_sums', math.fsum(row), c)
    for power in range(5):
        checks.arithmetic('dopri_fifth_order_moment',
            math.fsum(b*c**power for b, c in zip(DP_A[-1], DP_C)), 1/(power+1))
    checks.arithmetic('dopri_embedded_weight_sum', math.fsum(DP_B4), 1.)
    # Same hard fraction, exact pressureless-era power-law oracle.
    fraction = ref['Omega_exc']/(ref['Omega_exc']+ref['Omega_b'])
    roots = ((-3+math.sqrt(1+24*fraction))/4,
             (-3-math.sqrt(1+24*fraction))/4)
    initial = np.eye(2)
    def matter_rhs(x, y):
        return np.stack((y[1], -1.5*y[1]-(.5-1.5*fraction)*y[0]))
    positive, negative = roots
    cplus = (initial[1]-negative*initial[0])/(positive-negative)
    cminus = (positive*initial[0]-initial[1])/(positive-negative)
    oracle = []
    for x in nodes:
        shift = float(x-nodes[0])
        plus, minus = math.exp(positive*shift), math.exp(negative*shift)
        oracle.append(np.stack((cplus*plus+cminus*minus,
            positive*cplus*plus+negative*cminus*minus)))
    primary, dpwork = dopri(matter_rhs, initial, nodes, lambda x, target: .025,
        CONFIG['primary_rtol'], CONFIG['primary_atol'])
    independent, rkwork = rk4(matter_rhs, initial, nodes, lambda x, target: .0025)
    compare(checks, 'exact_matter_power_DOPRI', primary, np.asarray(oracle), CONFIG['repeat_tolerance'])
    compare(checks, 'exact_matter_power_RK4', independent, np.asarray(oracle), CONFIG['repeat_tolerance'])
    # Non-growing oscillator checks phase, embedded error and independent RK4.
    osc_nodes = np.linspace(0., 2*math.pi, 65)
    def oscillator(x, y):
        return np.stack((y[1], -y[0]))
    exact = np.asarray([[[math.cos(x), math.sin(x)], [-math.sin(x), math.cos(x)]] for x in osc_nodes])
    d, dw = dopri(oscillator, initial, osc_nodes, lambda x, target: .025,
        CONFIG['primary_rtol'], CONFIG['primary_atol'])
    r, rw = rk4(oscillator, initial, osc_nodes, lambda x, target: .0025)
    compare(checks, 'exact_oscillator_DOPRI', d, exact, CONFIG['repeat_tolerance'])
    compare(checks, 'exact_oscillator_RK4', r, exact, CONFIG['repeat_tolerance'])
    return dict(hard_fraction=fraction, physical_tilt_log_a_roots=list(roots),
        matter_controls=dict(dopri=dpwork, rk4=rkwork), oscillator_controls=dict(dopri=dw, rk4=rw))


def solve_case(case, spectrum, ref, nodes, checks):
    start = time.perf_counter()
    delta = np.asarray(spectrum['spectrum']['delta'])
    weights = np.asarray(spectrum['spectrum']['weights'])
    n, eta, beta = len(delta), case['eta'], CONFIG['beta']
    kb = float(np.sum(weights))+beta
    coupled_frequency_numerator = math.sqrt(float(np.max(delta*delta)+weights @ (delta*delta)/beta))
    initial = np.zeros((2+2*n, 2))
    initial[:2] = np.eye(2)
    transformed_initial = initial.copy()
    astart = CONFIG['a_start']
    transformed_initial[0] = astart*initial[0]
    transformed_initial[1] = astart*(initial[1]+initial[0])
    rhs = rhs_factory(delta, weights, eta, ref)
    other = rhs_factory(delta, weights, eta, ref, transformed=True)
    def cap(phase, maximum):
        # H decreases; use the endpoint and full frozen coupled frequency bound,
        # not the largest bare soft frequency (which underestimates the top mode).
        return lambda x, target: min(maximum, phase*background(target, ref)[1]*eta/coupled_frequency_numerator)
    # Algebraic variable-transformation checks at every owned milestone.
    witness = np.arange(initial.size, dtype=float).reshape(initial.shape)/(initial.size+1)
    for scale_factor in CONFIG['full_state_scale_factors']:
        x = math.log(scale_factor)
        transformed = witness.copy()
        transformed[0] = scale_factor*witness[0]
        transformed[1] = scale_factor*(witness[0]+witness[1])
        f, g = rhs(x, witness), other(x, transformed)
        expected = f.copy()
        expected[0] = scale_factor*(witness[0]+witness[1])
        expected[1] = scale_factor*(witness[0]+2*witness[1]+f[1])
        checks.arithmetic('independent_coordinate_rhs', g, expected)
    primary, work1 = dopri(rhs, initial, nodes,
        cap(CONFIG['dopri_max_coupled_phase'], CONFIG['dopri_max_log_step']),
        CONFIG['primary_rtol'], CONFIG['primary_atol'])
    repeat, work2 = dopri(rhs, initial, nodes,
        cap(CONFIG['dopri_max_coupled_phase'], CONFIG['dopri_max_log_step']),
        CONFIG['repeat_rtol'], CONFIG['repeat_atol'])
    independent, work3 = rk4(other, transformed_initial, nodes,
        cap(CONFIG['rk4_max_coupled_phase'], CONFIG['rk4_max_log_step']))
    for i, x in enumerate(nodes):
        a = math.exp(float(x))
        independent[i, 0] /= a
        independent[i, 1] = independent[i, 1]/a-independent[i, 0]
    comparisons = dict(
        tighter_repeat=compare(checks, 'tighter_DOPRI', primary, repeat, CONFIG['repeat_tolerance']),
        independent_coordinates_RK4=compare(checks, 'independent_RK4', primary, independent, CONFIG['independent_tolerance']))
    checks.arithmetic('exact_initial_state', primary[0], initial)
    rows, full = [], []
    milestone_logs = {math.log(a): a for a in CONFIG['full_state_scale_factors']}
    for x, state in zip(nodes, primary):
        a, h, d = background(float(x), ref)
        u, un = state[:2]
        z, zn = state[2:2+n], state[2+n:]
        flow = rhs(float(x), state)
        q = weights @ z+beta*h*(u+un)
        qn = weights @ zn+beta*h*(d*(u+un)+un+flow[1])
        right = 1.5*kb*ref['Omega_exc']*u/(a**3*h)
        cancellation_scale = np.maximum(1., np.abs(qn)+2*np.abs(q)+np.abs(right))
        checks.arithmetic('clock_flux_identity', qn+2*q, right, cancellation_scale)
        density = 2*a*a*q/(3*kb*ref['Omega_exc'])
        checks.arithmetic('compensated_density_reconstruction', density-density, np.zeros(2))
        checks.arithmetic('hard_normal_current', 2*a*a*(qn+2*q)/(3*kb*ref['Omega_exc']),
            u/(a*h), np.maximum(1., 2*a*a*cancellation_scale/(3*kb*ref['Omega_exc'])))
        rows.append(dict(a=a, H_over_H0=h, u=u.tolist(), u_log_a=un.tolist(),
            clock_source_Q=q.tolist(), acceleration_over_H0=(h*(u+un)).tolist(),
            unitary_lapse_times_k_over_H0=(a*h*(u+un)).tolist(),
            H0_clock_pi_times_k_over_H0=(-a*u).tolist(),
            hard_density_contrast_per_k_over_H0=density.tolist(),
            polarization_contrast_per_k_over_H0=(-density).tolist(),
            soft_frequency_over_H_range=[float(np.min(delta)/(eta*h)), float(np.max(delta)/(eta*h))]))
        if float(x) in milestone_logs:
            full.append(dict(a=milestone_logs[float(x)], state=state.tolist(),
                layout='rows u,u_N,z[0:Nmode],z_N[0:Nmode]; two initial clock basis columns'))
    maximum_tilt = np.max(np.abs(primary[:, 0]), axis=0)
    checks.arithmetic('full_state_milestone_census', len(full), len(CONFIG['full_state_scale_factors']))
    return dict(**case, status='EVOLVED', Kb=kb, delta=delta.tolist(), weights=weights.tolist(),
        tau_star_seconds=eta/ref['H0_s_inverse'], initial_state=initial.tolist(),
        coupled_frequency_bound_over_H0=coupled_frequency_numerator/eta,
        coupled_bound_scope='Frozen undamped oscillatory spectrum; expansion and growth also controlled numerically by log-step cap and independent solves',
        sample_rows=rows, full_states=full, comparisons=comparisons,
        sampled_maximum_absolute_tilt_transfer=maximum_tilt.tolist(),
        initial_amplitude_for_sampled_tilt_below_display_threshold=
            (CONFIG['linear_tilt_display_threshold']/maximum_tilt).tolist(),
        amplitude_qualification='Sampled tilt-only linear rescaling; not a full lapse, density or nonlinear validity certificate',
        work=dict(primary=work1, tighter_repeat=work2, independent_RK4=work3),
        seconds=time.perf_counter()-start)


def run(spectra, ref, snapshot, selected=None):
    start = time.perf_counter()
    checks = Checks()
    nodes = np.unique(np.concatenate((np.linspace(math.log(CONFIG['a_start']), math.log(CONFIG['a_end']),
        CONFIG['log_samples']), np.asarray([math.log(a) for a in CONFIG['full_state_scale_factors']]))))
    controls = numerical_controls(ref, nodes, checks)
    # Complete slow-response reference on the same dust+Lambda background.
    empty = np.asarray([], dtype=float)
    slow = rhs_factory(empty, empty, 1., ref, slow=True)
    initial = np.eye(2)
    sp, sw1 = dopri(slow, initial, nodes, lambda x, target: .025,
        CONFIG['primary_rtol'], CONFIG['primary_atol'])
    st, sw2 = dopri(slow, initial, nodes, lambda x, target: .025,
        CONFIG['repeat_rtol'], CONFIG['repeat_atol'])
    sr, sw3 = rk4(slow, initial, nodes, lambda x, target: .0025)
    compare(checks, 'slow_reference_repeat', sp, st, CONFIG['repeat_tolerance'])
    compare(checks, 'slow_reference_RK4', sp, sr, CONFIG['independent_tolerance'])
    cases = snapshot['cases'] if selected is None else [snapshot['cases'][selected]]
    rows = [solve_case(c, spectra[c['spectrum_index']], ref, nodes, checks) for c in cases]
    comparisons = []
    if selected is None:
        for gap in (.001, .002):
            for eta in CONFIG['etas']:
                pair = [next(c for c in rows if c['gap'] == gap and c['eta'] == eta and c['order'] == n) for n in (64, 128)]
                a = np.asarray([r['u'] for r in pair[0]['sample_rows']])
                b = np.asarray([r['u'] for r in pair[1]['sample_rows']])
                scale = np.maximum(1., np.maximum(np.max(np.abs(a), axis=0), np.max(np.abs(b), axis=0)))
                comparisons.append(dict(gap=gap, eta=eta, fine_minus_coarse_tilt=(b-a).tolist(),
                    peak_normalized_difference=np.max(np.abs(b-a)/scale, axis=0).tolist(),
                    qualification='All 64/128 contrasts retained; descriptive, no quadrature outcome selected'))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    return dict(status='COMPLETE' if not checks.failures else 'FAILED_NUMERICAL_CONTROLS',
        configuration=CONFIG, reference=ref, initial_basis=['unit initial physical tilt, zero logarithmic tilt derivative',
            'zero initial physical tilt, unit logarithmic tilt derivative'],
        scope='Defined two-dimensional clock-initial-data subspace with every soft mode initially zero; not the full state transfer matrix, formation history, observed perturbation amplitude or all-sector stability proof',
        physical_time_assumption='Common positive inertia m=tau_star^2, kappa=1; eta=H0*tau_star is illustrative and is not fixed by the acceleration calibration',
        background_scope='Inherited central late dust+Lambda reference with its baryon fraction; radiation deliberately omitted, a=.001 is a synthetic initial epoch, not a qualified recombination history',
        compensated_scope='Phi=Psi=V=0 and ordinary Newtonian baryon perturbations zero; hard and polarization densities reconstructed with opposite signs',
        selected_case=selected, rows=rows, quadrature_comparisons=comparisons,
        integrator_controls=controls, checks=checks.output(),
        slow_reference=dict(rows=[dict(a=math.exp(float(x)), state=y.tolist()) for x, y in zip(nodes, sp)],
            work=dict(primary=sw1, tighter_repeat=sw2, RK4=sw3),
            qualification='Same hard matter fraction; comparison approximation, not assumed valid for slow soft modes'),
        runtime=dict(python=sys.version, numpy=np.__version__), seconds=time.perf_counter()-start,
        peak_self_rss_bytes=int(peak))


def main():
    args = sys.argv[1:]
    valid = args in (['freeze'], ['run']) or (len(args) == 2 and args[0] == 'run-case' and args[1].isdigit())
    if not valid:
        raise SystemExit('Use freeze, run, or run-case INDEX; stdout only')
    spectra, ref, snapshot = authenticate()
    if args == ['freeze']:
        print(encode(snapshot).decode())
        return
    if encode(json.loads(FREEZE.read_text())) != encode(snapshot):
        raise RuntimeError('Prospective source freeze differs')
    selected = int(args[1]) if args[0] == 'run-case' else None
    if selected is not None and not 0 <= selected < CONFIG['expected_cases']:
        raise RuntimeError('Unknown fixed case')
    global np
    import numpy as np
    payload = run(spectra, ref, snapshot, selected)
    wrapper = dict(freeze_sha256=sha(FREEZE), payload_sha256=digest(payload), payload=payload,
        within_output_target=len(encode(payload)) <= CONFIG['output_target_bytes'])
    print(encode(wrapper).decode())
    if payload['status'] != 'COMPLETE':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
