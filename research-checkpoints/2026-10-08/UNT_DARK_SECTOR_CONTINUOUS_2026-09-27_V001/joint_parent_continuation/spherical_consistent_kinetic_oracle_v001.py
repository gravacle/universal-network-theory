"""Prospective fixed-census oracle for the unchanged quadrature kernel.

Root alone executes after review. No trajectory or physical-model qualification.
Exact Fraction references apply to the literal binary64 input values.
"""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from fractions import Fraction as F
import resource
import signal
import struct
import sys
import tempfile
import time

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT / 'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
THIS = J / 'spherical_consistent_kinetic_oracle_v001.py'
PROTOCOL = J / 'SPHERICAL_CONSISTENT_KINETIC_ORACLE_PROTOCOL_V001.md'
INTENT = J / 'SPHERICAL_CONSISTENT_KINETIC_ORACLE_V001_INTENT.json'
OUT = J / 'SPHERICAL_CONSISTENT_KINETIC_ORACLE_V001_RESULTS.json'
KERNEL = J / 'spherical_consistent_kinetic_v001.py'
PINS = {
    KERNEL.name: 'c1b0c4268071687ebca7949e20a5d05df9750ed41e5cb601e03228b6bd488e0e',
    'SPHERICAL_CONSISTENT_KINETIC_REPAIR_V001.md': '24309d3602ee4724a975ad61ffaca1903cdb3a73d6a5149b8a10b7e73e711353',
    'SPHERICAL_EXACT_INERTIA_DERIVATION_V001.md': '3a60f43ea5e666e23bac8e478df74f38aeaac77f0cc4a86c15cae593a622a431',
    'SPHERICAL_TWO_CURRENT_RESULT_AUDIT_V001.md': '33eb42c0f30a644b69580e43a17abc77ef5f3394786a2bc70e5055b2764367f5',
    '../FRONTIER_UPDATE_V067.md': 'b4be745a5cd2239f3da946872d98e4e65e1b1c63bbe57e71661ec72e827e0a37',
}
CONFIG = dict(orders=[16, 32, 64], arithmetic_tolerance=2e-11,
              derivative_tolerance=2e-6, derivative_steps=[1e-4, 5e-5, 2.5e-5],
              A=1.3, affine_rate=0.19, radius_scales=[0.5, 2.0],
              harmonic_kappa=1.7, U_kappa=0.7, W_kappa=-0.4,
              expansion_rate=0.07, outer_traction=0.03)
CASES = [
    dict(name='single_origin', faces=[0., 1.25], masses=[0.7], velocity=[0.37], momentum=[0.23]),
    dict(name='uniform', faces=[0., 0.5, 1., 1.5, 2.]),
    dict(name='graded', faces=[0., 0.125, 0.5, 1.25, 2.]),
    dict(name='thin_annuli', faces=[0., 1., 1.+1/1024, 1.+2/1024, 1.+4/1024]),
]
for case in CASES[1:]:
    case.update(masses=[0.7, 1.1, 0.9, 1.3], velocity=[0.17, -0.11, 0.23, -0.07],
                momentum=[0.29, -0.13, 0.19, -0.17])
LIMITS = dict(wall_seconds=60, cpu_soft_seconds=60, cpu_hard_seconds=65,
              maximum_self_rss_bytes=536870912, maximum_input_bytes=2097152,
              maximum_output_bytes=8388608)
THREAD_KEYS = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


class Stop(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise Stop(message)


def sanitize(value):
    if isinstance(value, float) and not math.isfinite(value):
        return dict(nonfinite=repr(value), binary64_hex=struct.pack('>d', value).hex())
    if isinstance(value, dict):
        return {str(k): sanitize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize(v) for v in value]
    return value


def enc(value):
    return json.dumps(sanitize(value), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    path = Path(path).absolute()
    path.resolve().relative_to(ROOT.resolve())
    for parent in (path, *path.parents):
        if parent == ROOT.parent:
            break
        need(not parent.is_symlink(), 'Symlink refused: ' + str(parent))
    need(path.stat().st_size <= LIMITS['maximum_input_bytes'], 'Input byte limit')
    return path.read_bytes()


def pin(path, expected=None):
    data = read(path)
    digest = sha(data)
    need(expected is None or digest == expected, 'Changed input: ' + str(path))
    inputs[str(path)] = dict(sha256=digest, bytes=len(data))
    return data


def publish(path, value):
    need(path in (INTENT, OUT) and not path.exists(), 'Exclusive fixed output required')
    data = enc(value) + b'\n'
    need(len(data) <= LIMITS['maximum_output_bytes'], 'Output byte limit')
    fd, name = tempfile.mkstemp(prefix=path.name + '.pending.', dir=J)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.link(name, path)
    fd = os.open(J, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    Path(name).unlink()


def guard():
    need(time.monotonic() - started < LIMITS['wall_seconds'], 'Wall resource bound')
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= LIMITS['maximum_self_rss_bytes'], 'RSS resource bound')


def q(value):
    return F.from_float(float(value))


def rational(value):
    return dict(numerator=str(value.numerator), denominator=str(value.denominator), approximate=float(value))


def poly(coefficients, x):
    return sum((coefficient * x**i for i, coefficient in enumerate(coefficients)), F(0))


def shell_reference(left, right, mass):
    """Exact rational M/m entries and independent quotient-rule derivatives."""
    t = left/right
    s = 1+t+t*t
    entries = []
    derivatives = []
    for factor, coefficients in (
        (F(3, 5), [0, 0, 0, 5, 6, 3, 1]),
        (F(9, 10), [0, 0, 1, 3, 1]),
        (F(3, 5), [1, 3, 6, 5]),
    ):
        numerator = poly(coefficients, t)
        derivative = poly([i*coefficients[i] for i in range(1, len(coefficients))], t)
        entries.append(mass*factor*numerator/s**3)
        derivatives.append(mass*factor*(derivative*s-3*numerator*(1+2*t))/s**4)
    return t, entries, derivatives


def exact_matrix_and_force(faces, masses, velocity):
    n = len(masses)
    matrix = [[F(0) for _ in range(n)] for _ in range(n)]
    force = [F(0) for _ in range(n)]
    for i, mass in enumerate(masses):
        if i == 0:
            matrix[0][0] += F(3, 5)*mass
            continue
        t, (ll, lr, rr), (dll, dlr, drr) = shell_reference(faces[i], faces[i+1], mass)
        matrix[i-1][i-1] += ll
        matrix[i-1][i] += lr
        matrix[i][i-1] += lr
        matrix[i][i] += rr
        vl, vr = velocity[i-1], velocity[i]
        left_force = (dll*vl*vl+2*dlr*vl*vr+drr*vr*vr)/(2*faces[i+1])
        force[i-1] += left_force
        force[i] -= t*left_force
    return matrix, force


def harmonic_reference(faces, masses, kappa):
    """Direct quotient derivatives, independent of M and of kernel polynomials."""
    gradient = [F(0) for _ in masses]
    potential = F(0)
    for i, mass in enumerate(masses):
        left, right = faces[i:i+2]
        d3, d5 = right**3-left**3, right**5-left**5
        prefactor = F(3, 10)*kappa*mass
        potential += prefactor*d5/d3
        dl = prefactor*(-5*left**4*d3+3*left**2*d5)/d3**2
        dr = prefactor*(5*right**4*d3-3*right**2*d5)/d3**2
        if i:
            gradient[i-1] += dl
        gradient[i] += dr
    return potential, gradient


def mv(matrix, vector):
    return [sum((a*b for a, b in zip(row, vector)), F(0)) for row in matrix]


def norm_inf_matrix(matrix):
    return max(sum(map(abs, row), F(0)) for row in matrix)


def exact_ldl(matrix):
    n = len(matrix)
    lower = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    diagonal = []
    for i in range(n):
        for j in range(i):
            lower[i][j] = (matrix[i][j]-sum((lower[i][k]*lower[j][k]*diagonal[k] for k in range(j)), F(0)))/diagonal[j]
        pivot = matrix[i][i]-sum((lower[i][k]**2*diagonal[k] for k in range(i)), F(0))
        if pivot <= 0:
            raise ValueError('Exact nonpositive LDL pivot of assembled matrix')
        diagonal.append(pivot)
    return lower, diagonal


def exact_solve(factors, rhs):
    lower, diagonal = factors
    n = len(rhs)
    y = []
    for i in range(n):
        y.append(rhs[i]-sum((lower[i][j]*y[j] for j in range(i)), F(0)))
    z = [y[i]/diagonal[i] for i in range(n)]
    result = [F(0) for _ in rhs]
    for i in range(n-1, -1, -1):
        result[i] = z[i]-sum((lower[j][i]*result[j] for j in range(i+1, n)), F(0))
    return result


def exact_inverse(factors):
    n = len(factors[1])
    columns = [exact_solve(factors, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def flist(values):
    return [float(v) for v in values]


def fmatrix(values):
    return [flist(row) for row in values]


def check(records, name, left, right=0., normalization=1., tolerance=None):
    tolerance = CONFIG['arithmetic_tolerance'] if tolerance is None else tolerance
    a, b = np.broadcast_arrays(np.asarray(left, dtype=float), np.asarray(right, dtype=float))
    a, b = a/normalization, b/normalization
    with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
        scale = np.maximum(1., np.maximum(abs(a), abs(b)))
        signed = (a-b)/scale
    good = bool(np.all(np.isfinite(signed)))
    maximum = float(np.max(abs(signed))) if good else None
    passed = good and maximum <= tolerance
    records.append(dict(name=name, left=a.tolist(), right=b.tolist(), normalization=normalization,
                        signed_normalized_residual=signed.tolist(), maximum_absolute_normalized_residual=maximum,
                        count=int(signed.size), tolerance=tolerance, passed=passed))
    return passed


def dense(diagonal, off):
    n = len(diagonal)
    result = np.diag(diagonal)
    if n > 1:
        result += np.diag(off, 1)+np.diag(off, -1)
    return result


def kinetic_at(faces, masses, momentum, A, order):
    state = kernel.canonical_kinematics(faces, masses, momentum, A=A, order=order)
    return state['kinetic_energy']


def run_case(case, order, item):
    checks = item['checks']
    faces, masses, velocity, momentum = [np.asarray(case[key], dtype=float) for key in ('faces', 'masses', 'velocity', 'momentum')]
    originals = [x.copy() for x in (faces, masses, velocity, momentum)]
    fq, mq, vq, pq = [list(map(q, values)) for values in (faces, masses, velocity, momentum)]
    n, total_mass, length = len(masses), float(sum(mq)), float(faces[-1])
    force_unit = total_mass/length
    exact_m, exact_g = exact_matrix_and_force(fq, mq, vq)
    d, o, g = kernel.mass_matrix_and_geometric_force(faces, masses, velocity, order)
    matrix = dense(d, o)
    item.update(matrix=matrix.tolist(), exact_integral_matrix=fmatrix(exact_m), geometric_force=g.tolist(),
                exact_integral_geometric_force=flist(exact_g))
    check(checks, 'matrix_exact_integral', matrix, fmatrix(exact_m), total_mass)
    check(checks, 'force_exact_integral', g, flist(exact_g), force_unit)
    check(checks, 'matrix_symmetry', matrix, matrix.T, total_mass)
    separate_d, separate_o = kernel.mass_matrix(faces, masses, order)
    check(checks, 'separate_matrix_api', dense(separate_d, separate_o), matrix, total_mass)
    check(checks, 'separate_force_api', kernel.geometric_force(faces, masses, velocity, order), g, force_unit)
    literal_m = [[q(value) for value in row] for row in matrix]
    check(checks, 'independent_matvec', kernel.tridiagonal_matvec(d, o, velocity), flist(mv(literal_m, vq)), total_mass)
    exact_volumes = [float(F(4, 3)*q(math.pi)*(fq[i+1]**3-fq[i]**3)) for i in range(n)]
    volumes = kernel.shell_volumes(faces)
    check(checks, 'positive_exact_volumes', volumes/np.asarray(exact_volumes), 1.)
    if n == 1:
        check(checks, 'origin_three_fifths', d[0], float(F(3, 5)*mq[0]), total_mass)
        check(checks, 'origin_force_zero', g, 0., force_unit)
    factors = exact_ldl(literal_m)
    inverse = exact_inverse(factors)
    matrix_norm, inverse_norm = norm_inf_matrix(literal_m), norm_inf_matrix(inverse)
    solution = kernel.solve_spd_tridiagonal(d, o, momentum)
    exact_solution = exact_solve(factors, pq)
    solution_q = list(map(q, solution))
    residual = [a-b for a, b in zip(mv(literal_m, solution_q), pq)]
    residual_norm = max(map(abs, residual))
    relative_residual = residual_norm/(matrix_norm*max(map(abs, solution_q))+max(map(abs, pq)))
    forward_bound = inverse_norm*residual_norm
    relative_bound = forward_bound/max(map(abs, exact_solution))
    item['assembled_matrix_certificate'] = dict(
        scope='Exact rational certificate for literal assembled binary64 matrix only',
        positive_LDL_pivots=[rational(v) for v in factors[1]],
        matrix_infinity_norm=rational(matrix_norm), inverse_infinity_norm=rational(inverse_norm),
        condition_infinity=rational(matrix_norm*inverse_norm), exact_residual=[rational(v) for v in residual],
        relative_residual=rational(relative_residual), forward_error_bound=rational(forward_bound),
        relative_forward_error_bound=rational(relative_bound))
    for label, value in [('solve_exact_relative_residual', relative_residual), ('solve_exact_relative_forward_bound', relative_bound)]:
        checks.append(dict(name=label, count=1, exact_value=rational(value), tolerance=CONFIG['arithmetic_tolerance'],
                           passed=bool(value <= q(CONFIG['arithmetic_tolerance']))))
    for factor in CONFIG['radius_scales']:
        sd, so = kernel.mass_matrix(factor*faces, masses, order)
        check(checks, 'radius_scale_matrix_'+str(factor), dense(sd, so), matrix, total_mass)
        check(checks, 'radius_scale_force_'+str(factor), factor*kernel.geometric_force(factor*faces, masses, velocity, order), g, force_unit)
    check(checks, 'force_homogeneity', float(np.dot(faces[1:], g)), 0., total_mass)
    check(checks, 'affine_force_zero', kernel.geometric_force(faces, masses, CONFIG['affine_rate']*faces[1:], order), 0., force_unit)
    potential, gradient = harmonic_reference(fq, mq, q(CONFIG['harmonic_kappa']))
    kv, kg = kernel.harmonic_potential_gradient(faces, masses, CONFIG['harmonic_kappa'])
    item['harmonic'] = dict(reference_potential=float(potential), reference_gradient=flist(gradient), kernel_potential=kv, kernel_gradient=kg.tolist())
    check(checks, 'independent_harmonic_potential', kv, float(potential), total_mass*length**2)
    check(checks, 'independent_harmonic_gradient', kg, flist(gradient), total_mass*length)
    check(checks, 'harmonic_mass_identity', CONFIG['harmonic_kappa']*kernel.tridiagonal_matvec(d, o, faces[1:]), flist(gradient), total_mass*length)
    acceleration = kernel.solve_spd_tridiagonal(d, o, -np.asarray(flist(gradient)))
    check(checks, 'harmonic_acceleration_all_faces', acceleration, -CONFIG['harmonic_kappa']*faces[1:], length)
    state = kernel.canonical_kinematics(faces, masses, momentum, A=CONFIG['A'], order=order)
    A = q(CONFIG['A'])
    reference_inverse_p = exact_solve(exact_ldl(exact_m), pq)
    reference_v = [v/A for v in reference_inverse_p]
    reference_K = sum((p*v for p, v in zip(pq, reference_inverse_p)), F(0))/(2*A*A)
    _, reference_g = exact_matrix_and_force(fq, mq, reference_v)
    item['canonical'] = {key: value.tolist() if isinstance(value, np.ndarray) else value for key, value in state.items()}
    item['canonical_reference'] = dict(peculiar_velocity=flist(reference_v), kinetic_energy=float(reference_K), geometric_force=flist(reference_g))
    check(checks, 'canonical_peculiar_velocity', state['peculiar_velocity'], flist(reference_v))
    check(checks, 'canonical_coordinate_velocity', state['coordinate_velocity'], flist([v/A for v in reference_v]))
    check(checks, 'canonical_kinetic_energy', state['kinetic_energy'], float(reference_K), total_mass)
    check(checks, 'canonical_geometric_force', state['geometric_force'], flist(reference_g), force_unit)
    check(checks, 'supplied_velocity_kinetic_energy', kernel.kinetic_energy(d, o, velocity),
          float(sum((v*w for v, w in zip(vq, mv(exact_m, vq))), F(0))/2), total_mass)
    fd_rows = []
    item['fixed_p_derivatives'] = fd_rows
    gaps = np.diff(faces)
    for epsilon in CONFIG['derivative_steps']:
        derivatives, samples = [], []
        for i in range(n):
            local_width = gaps[i] if i == n-1 else min(gaps[i], gaps[i+1])
            step = epsilon*local_width
            plus, minus = faces.copy(), faces.copy()
            plus[i+1] += step
            minus[i+1] -= step
            ep = kinetic_at(plus, masses, momentum, CONFIG['A'], order)
            em = kinetic_at(minus, masses, momentum, CONFIG['A'], order)
            derivatives.append((ep-em)/(2*step))
            samples.append(dict(face=i+1, requested_step=float(step), actual_plus_displacement=float(plus[i+1]-faces[i+1]),
                                actual_minus_displacement=float(faces[i+1]-minus[i+1]), plus_energy=ep, minus_energy=em))
            guard()
        fd_rows.append(dict(epsilon=epsilon, gradient=derivatives, samples=samples))
        check(checks, 'fixed_p_centered_'+str(epsilon), derivatives, -state['geometric_force'], force_unit, CONFIG['derivative_tolerance'])
    estimates = [(f'centered_{row["epsilon"]}', row['gradient']) for row in fd_rows]
    item['fixed_p_richardson'] = []
    for i in range(2):
        estimate = (4*np.asarray(fd_rows[i+1]['gradient'])-np.asarray(fd_rows[i]['gradient']))/3
        item['fixed_p_richardson'].append(dict(coarse=fd_rows[i]['epsilon'], fine=fd_rows[i+1]['epsilon'], gradient=estimate.tolist()))
        check(checks, 'fixed_p_richardson_'+str(i), estimate, -state['geometric_force'], force_unit, CONFIG['derivative_tolerance'])
        estimates.append(('richardson_'+str(i), estimate.tolist()))
    U, gradU = harmonic_reference(fq, mq, q(CONFIG['U_kappa']))
    W, gradW = harmonic_reference(fq, mq, q(CONFIG['W_kappa']))
    gradU, gradW = np.asarray(flist(gradU)), np.asarray(flist(gradW))
    w = state['coordinate_velocity']
    traction = np.zeros(n)
    traction[-1] = CONFIG['outer_traction']
    pdot = state['geometric_force']-gradU-gradW/CONFIG['A']+traction
    H, kinetic = CONFIG['expansion_rate'], state['kinetic_energy']
    common = dict(momentum_work=float(np.dot(w, pdot)), expansion_kinetic=-2*H*kinetic,
                  U_coordinate_work=float(np.dot(gradU, w)), W_coordinate_work=float(np.dot(gradW, w))/CONFIG['A'],
                  W_expansion_work=-H*float(W)/CONFIG['A'])
    expected = float(np.dot(traction, w))-2*H*kinetic-H*float(W)/CONFIG['A']
    item['work_chain'] = dict(coordinate_velocity=w.tolist(), momentum_derivative=pdot.tolist(),
                              U=float(U), W=float(W), common_terms=common, expected_total_rate=expected, estimates=[])
    need(bool(np.any(w != 0.)), 'Nonzero-velocity work test required')
    for name, gradient_values, tolerance in [('independent_exact', [-float(v) for v in reference_g], CONFIG['arithmetic_tolerance'])]+[(name, values, CONFIG['derivative_tolerance']) for name, values in estimates]:
        coordinate_work = float(np.dot(gradient_values, w))
        total = math.fsum([coordinate_work, *common.values()])
        item['work_chain']['estimates'].append(dict(name=name, kinetic_coordinate_work=coordinate_work, total_rate=total, signed_defect=total-expected))
        check(checks, 'nonzero_velocity_work_'+name, total, expected, total_mass, tolerance)
    for label, current, original in zip(('faces', 'masses', 'velocity', 'momentum'), (faces, masses, velocity, momentum), originals):
        check(checks, 'input_immutable_'+label, current, original, tolerance=0.)
    guard()


def run():
    global np, kernel
    import numpy as np
    spec = importlib.util.spec_from_file_location('owned_spherical_consistent_kinetic_v001', KERNEL)
    kernel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kernel)
    for case in CASES:
        for order in CONFIG['orders']:
            item = dict(case=case, order=order, checks=[], status='STARTED', error=None)
            records.append(item)
            try:
                run_case(case, order, item)
                item['status'] = 'COMPLETED'
            except Stop:
                raise
            except Exception as exc:
                item['status'] = 'FAILED_RETAINED'
                item['error'] = dict(type=type(exc).__name__, message=str(exc))
            guard()
    for case in CASES:
        selected = [row for row in records if row['case']['name'] == case['name']]
        for left, right in zip(selected, selected[1:]):
            row = dict(case=case['name'], left_order=left['order'], right_order=right['order'], checks=[], status='UNAVAILABLE')
            order_pairs.append(row)
            if left['status'] == right['status'] == 'COMPLETED':
                total_mass, length = sum(case['masses']), case['faces'][-1]
                check(row['checks'], 'adjacent_order_matrix', left['matrix'], right['matrix'], total_mass)
                check(row['checks'], 'adjacent_order_geometric_force', left['geometric_force'], right['geometric_force'], total_mass/length)
                check(row['checks'], 'adjacent_order_canonical_velocity', left['canonical']['peculiar_velocity'], right['canonical']['peculiar_velocity'])
                row['status'] = 'COMPLETED'
    guard()


def main():
    global started, inputs, records, order_pairs
    need(Path.cwd().resolve() == ROOT and Path(__file__).resolve() == THIS and sys.platform == 'darwin', 'Fixed root/source/platform required')
    need(sys.argv[1:] == ['--run'] and not OUT.exists() and not INTENT.exists(), 'One exclusive root-owned invocation required')
    need(all(os.environ.get(key) == '1' for key in THREAD_KEYS), 'All five thread controls must be one before NumPy import')
    resource.setrlimit(resource.RLIMIT_CPU, (LIMITS['cpu_soft_seconds'], LIMITS['cpu_hard_seconds']))
    def halt(signum, frame):
        raise Stop('Wall/CPU signal bound')
    signal.signal(signal.SIGALRM, halt)
    signal.signal(signal.SIGXCPU, halt)
    inputs, records, order_pairs = {}, [], []
    started = time.monotonic()
    source_sha, protocol_sha = sha(pin(THIS)), sha(pin(PROTOCOL))
    for name, digest in PINS.items():
        pin(J/name, digest)
    publish(INTENT, dict(schema='SPHERICAL_CONSISTENT_KINETIC_ORACLE_INTENT_V001', source_sha256=source_sha,
                         protocol_sha256=protocol_sha, input_pins=PINS, config=CONFIG, cases=CASES, limits=LIMITS,
                         thread_environment={key: os.environ[key] for key in THREAD_KEYS}, argv=sys.argv, target=str(OUT)))
    pin(INTENT)
    signal.alarm(LIMITS['wall_seconds'])
    error = None
    custody_end_error = None
    custody_end_verified = False
    try:
        run()
    except BaseException as exc:
        error = dict(type=type(exc).__name__, message=str(exc))
    finally:
        signal.alarm(0)
    try:
        for path, meta in inputs.items():
            data = read(path)
            need(sha(data) == meta['sha256'] and len(data) == meta['bytes'], 'Custody changed during run')
        custody_end_verified = True
    except BaseException as exc:
        custody_end_error = dict(type=type(exc).__name__, message=str(exc))
    checks = [check for row in records+order_pairs for check in row['checks']]
    all_passed = error is None and custody_end_verified and len(records) == 12 and len(order_pairs) == 8 and all(row['status'] == 'COMPLETED' for row in records+order_pairs) and all(check['passed'] for check in checks)
    status = 'COMPLETED_NUMERICAL_CONTROLS_PASSED' if all_passed else 'NUMERICAL_FAILURES_OR_INCOMPLETE_RETAINED'
    value = dict(schema='SPHERICAL_CONSISTENT_KINETIC_ORACLE_V001', status=status, error=error,
                 custody_end_verified=custody_end_verified, custody_end_error=custody_end_error,
                 all_numerical_controls_passed=all_passed, numerical_entry_count=sum(check['count'] for check in checks),
                 failed_check_groups=sum(not check['passed'] for check in checks), source_sha256=source_sha,
                 protocol_sha256=protocol_sha, intent_sha256=sha(read(INTENT)), inputs=inputs, config=CONFIG,
                 cases=CASES, records=records, order_pairs=order_pairs, limits=LIMITS,
                 resources_analysis_phase=dict(elapsed_seconds=time.monotonic()-started, maximum_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
                 qualification=dict(kernel=False, trajectory=False, continuum=False, full_metric=False,
                                    observations=False, native_source_formation=False, Stage3_complete=False),
                 mandatory_lanes_open=11)
    publish(OUT, dict(payload_sha256=sha(enc(value)), payload=value))
    print(enc(dict(path=str(OUT), sha256=sha(OUT.read_bytes()), status=status, all_numerical_controls_passed=all_passed)).decode())
    if not all_passed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
