"""One-method wrapper reusing the pinned independent kernel oracle controls.

Root alone runs after review; no ancestral main/run or quadrature execution.
"""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import signal
import struct
import sys
import tempfile
import time

ROOT = Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J = ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
THIS = J/'spherical_exact_kinetic_oracle_v001.py'
PROTOCOL = J/'SPHERICAL_EXACT_KINETIC_ORACLE_PROTOCOL_V001.md'
KERNEL = J/'spherical_exact_kinetic_v001.py'
HELPER = J/'spherical_consistent_kinetic_oracle_v001.py'
INTENT = J/'SPHERICAL_EXACT_KINETIC_ORACLE_V001_INTENT.json'
OUT = J/'SPHERICAL_EXACT_KINETIC_ORACLE_V001_RESULTS.json'
METHOD = 'closed_form_rational_polynomial_binary64_v001'
PINS = {
    KERNEL.name: '78765ef0e2d29c044642b1d944682a81ff5d48b22de9d0cb16b7bc47b9c7e11a',
    HELPER.name: 'a7cd9bfe6026ce2e664a804394009b32e5023d5b9cda43a84844ebd039bd4a66',
    'SPHERICAL_CONSISTENT_KINETIC_ORACLE_PROTOCOL_V001.md': 'c5b1dec4402aa5387a1aa3be8f76fc3e642c66ae0792b0a3ac5e28dc5098ae36',
    'SPHERICAL_EXACT_INERTIA_DERIVATION_V001.md': '3a60f43ea5e666e23bac8e478df74f38aeaac77f0cc4a86c15cae593a622a431',
    'spherical_consistent_kinetic_v001.py': 'c1b0c4268071687ebca7949e20a5d05df9750ed41e5cb601e03228b6bd488e0e',
    'SPHERICAL_CONSISTENT_KINETIC_ORACLE_V001_RESULTS.json': 'bb9810e5d392e2ce7ee3ae3d2bdf48abbe7576bd349c2d2928e77fb332228327',
    'SPHERICAL_CONSISTENT_KINETIC_ORACLE_V001_INTENT.json': 'c8231192d96b0983d49effb030dd20b822ab9b0883eae5f3e36b3900b3918ca0',
}
CONFIG = dict(arithmetic_tolerance=2e-11, derivative_tolerance=2e-6,
              derivative_steps=[1e-4, 5e-5, 2.5e-5], A=1.3, affine_rate=0.19,
              radius_scales=[0.5, 2.0], harmonic_kappa=1.7, U_kappa=0.7,
              W_kappa=-0.4, expansion_rate=0.07, outer_traction=0.03)
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
        need(not parent.is_symlink(), 'Symlink refused: '+str(parent))
    need(path.stat().st_size <= LIMITS['maximum_input_bytes'], 'Input byte limit')
    return path.read_bytes()


def pin(path, expected=None):
    data = read(path)
    digest = sha(data)
    need(expected is None or digest == expected, 'Changed input: '+str(path))
    inputs[str(path)] = dict(sha256=digest, bytes=len(data))
    return data


def publish(path, value):
    need(path in (INTENT, OUT) and not path.exists(), 'Exclusive fixed output required')
    data = enc(value)+b'\n'
    need(len(data) <= LIMITS['maximum_output_bytes'], 'Output byte limit')
    fd, name = tempfile.mkstemp(prefix=path.name+'.pending.', dir=J)
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
    need(time.monotonic()-started < LIMITS['wall_seconds'], 'Wall resource bound')
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= LIMITS['maximum_self_rss_bytes'], 'RSS resource bound')


def load_definitions(name, path):
    """Non-main module name: the predecessor's scientific entry points stay inert."""
    need(name != '__main__', 'Ancestral main cannot be loaded')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OneMethodAdapter:
    """Compatibility only: one fixed label, no numeric order reaches the kernel."""
    def __init__(self, implementation):
        self.implementation = implementation
        for name in ('shell_volumes', 'tridiagonal_matvec', 'solve_spd_tridiagonal',
                     'kinetic_energy', 'harmonic_potential_gradient'):
            setattr(self, name, getattr(implementation, name))

    def mass_matrix(self, faces, masses, order):
        need(order == METHOD, 'No quadrature/order selection exists')
        return self.implementation.mass_matrix(faces, masses)

    def geometric_force(self, faces, masses, velocity, order):
        need(order == METHOD, 'No quadrature/order selection exists')
        return self.implementation.geometric_force(faces, masses, velocity)

    def mass_matrix_and_geometric_force(self, faces, masses, velocity, order):
        need(order == METHOD, 'No quadrature/order selection exists')
        return self.implementation.mass_matrix_and_geometric_force(faces, masses, velocity)

    def canonical_kinematics(self, faces, masses, momentum, A=1.0, order=METHOD):
        need(order == METHOD, 'No quadrature/order selection exists')
        return self.implementation.canonical_kinematics(faces, masses, momentum, A=A)


def run():
    import numpy as np
    helper = load_definitions('owned_quadrature_oracle_definitions_only', HELPER)
    implementation = load_definitions('owned_exact_inertia_kernel', KERNEL)
    need(helper.CONFIG == dict(CONFIG, orders=[16, 32, 64]) and helper.CASES == CASES,
         'Pinned ancestral fixed tests/census do not match the unchanged controls')
    need(implementation.INERTIA_METHOD == METHOD, 'Exact method identity mismatch')
    helper.np = np
    helper.kernel = OneMethodAdapter(implementation)
    helper.guard = guard
    for case in CASES:
        item = dict(case=case, method=METHOD, checks=[], status='STARTED', error=None)
        records.append(item)
        try:
            helper.run_case(case, METHOD, item)
            item['status'] = 'COMPLETED'
        except Stop:
            raise
        except Exception as exc:
            item['status'] = 'FAILED_RETAINED'
            item['error'] = dict(type=type(exc).__name__, message=str(exc))
        guard()


def main():
    global started, inputs, records
    need(Path.cwd().resolve() == ROOT and Path(__file__).resolve() == THIS and sys.platform == 'darwin',
         'Fixed root/source/platform required')
    need(sys.argv[1:] == ['--run'] and not OUT.exists() and not INTENT.exists(), 'One exclusive root-owned invocation required')
    need(all(os.environ.get(key) == '1' for key in THREAD_KEYS), 'All five thread controls must be one before NumPy import')
    resource.setrlimit(resource.RLIMIT_CPU, (LIMITS['cpu_soft_seconds'], LIMITS['cpu_hard_seconds']))
    def halt(signum, frame):
        raise Stop('Wall/CPU signal bound')
    signal.signal(signal.SIGALRM, halt)
    signal.signal(signal.SIGXCPU, halt)
    inputs, records = {}, []
    started = time.monotonic()
    source_sha, protocol_sha = sha(pin(THIS)), sha(pin(PROTOCOL))
    for name, digest in PINS.items():
        pin(J/name, digest)
    publish(INTENT, dict(schema='SPHERICAL_EXACT_KINETIC_ORACLE_INTENT_V001', source_sha256=source_sha,
                         protocol_sha256=protocol_sha, input_pins=PINS, method=METHOD, config=CONFIG,
                         cases=CASES, limits=LIMITS, thread_environment={key: os.environ[key] for key in THREAD_KEYS},
                         argv=sys.argv, target=str(OUT)))
    pin(INTENT)
    sys.dont_write_bytecode = True
    signal.alarm(LIMITS['wall_seconds'])
    error, custody_end_error, custody_end_verified = None, None, False
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
    checks = [check for row in records for check in row['checks']]
    all_passed = error is None and custody_end_verified and len(records) == 4 and all(row['status'] == 'COMPLETED' for row in records) and all(check['passed'] for check in checks)
    status = 'COMPLETED_NUMERICAL_CONTROLS_PASSED' if all_passed else 'NUMERICAL_FAILURES_OR_INCOMPLETE_RETAINED'
    value = dict(schema='SPHERICAL_EXACT_KINETIC_ORACLE_V001', status=status, error=error,
                 custody_end_verified=custody_end_verified, custody_end_error=custody_end_error,
                 all_numerical_controls_passed=all_passed, numerical_entry_count=sum(check['count'] for check in checks),
                 failed_check_groups=sum(not check['passed'] for check in checks), source_sha256=source_sha,
                 protocol_sha256=protocol_sha, intent_sha256=sha(read(INTENT)), inputs=inputs,
                 method=METHOD, config=CONFIG, cases=CASES, records=records, limits=LIMITS,
                 inapplicable_controls=dict(quadrature_order_repetitions=True, adjacent_quadrature_order_comparisons=True,
                     reason='New runtime has one closed-form integration method and no quadrature order'),
                 predecessor_failures_waived=False,
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
