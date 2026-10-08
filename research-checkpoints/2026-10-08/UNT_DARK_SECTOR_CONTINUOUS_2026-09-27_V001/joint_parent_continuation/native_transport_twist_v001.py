"""Actual saved16D transport contact/current, stdout-only freeze/run."""
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

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
FREEZE = HERE / 'NATIVE_TRANSPORT_TWIST_V001_FROZEN.json'
OLD = HERE / 'RECORD_ADDITION_RESULTS.json'
OLD_FREEZE = HERE / 'RECORD_ADDITION_FROZEN.json'
CONFIG = dict(ages=[0., .25, .5, 1., 2.], small_angle=.001,
              angles=[0., -.001, .001, -math.pi/2, math.pi/2, math.pi],
              tolerance=2e-11, small_angle_tolerance=2e-9, hbar=1.,
              output_target_bytes=1048576)
PINS = {
    OLD: '2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a',
    OLD_FREEZE: '4d22da45549f2de78fc0477be6b5f23bc0f58b3598a312e2aa76d8f729ac9ff3',
    HERE / 'record_addition_compute.py': '4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10',
    HERE.parent / 'recovered_sources/BS_MICRO_ACTION.md': '00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec',
}


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    files = {}

    def add(path, expected=None):
        path = path.resolve(strict=True)
        if not path.is_relative_to(PROJECT):
            raise RuntimeError('Source outside project')
        digest = sha(path)
        if expected is not None and digest != expected:
            raise RuntimeError('Source checksum mismatch: '+str(path))
        files[str(path.relative_to(PROJECT))] = digest

    for path, digest in PINS.items():
        add(path, digest)
    for name, digest in json.loads(OLD_FREEZE.read_text())['files'].items():
        add(PROJECT / name, digest)
    old = json.loads(OLD.read_text())
    if (old['status'] != 'COMPLETE' or old['freeze_sha256'] != sha(OLD_FREEZE)
            or old['payload_sha256'] != hashlib.sha256(encode(old['payload'])).hexdigest()
            or not all(c['passed'] for c in old['payload']['checks'])):
        raise RuntimeError('Unqualified old result wrapper')
    cases = old['payload']['cases']
    if [c['name'] for c in cases] != ['native', 'feedback_off', 'copying_off']:
        raise RuntimeError('Preparation census differs')
    for case in cases:
        if [r['time'] for r in case['hold']] != CONFIG['ages'] or case['dimension'] != 16:
            raise RuntimeError('Held-state census differs')
    add(Path(__file__))
    add(HERE / 'NATIVE_TRANSPORT_TWIST_PROTOCOL_V001.md')
    return cases, dict(configuration=CONFIG, files=files)


def embed(a, position):
    out = np.ones((1, 1), complex)
    for j in range(4):
        out = np.kron(out, a if j == position else np.eye(2))
    return out


def comm(a, b):
    return a@b-b@a


def run():
    started = time.perf_counter()
    cases, snapshot = inputs()
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze mismatch')
    eye = np.eye(16, dtype=complex)
    x2 = np.array([[0., 1.], [1., 0.]])
    y2 = np.array([[0., -1j], [1j, 0.]])
    z2 = np.diag([1., -1.])
    n2 = np.diag([0., 1.])
    ql, qr, n, P = (embed(n2, j) for j in range(4))
    xa, za, T, J = embed(x2, 2), embed(z2, 2), embed(x2, 3), embed(y2, 3)
    R = ql+qr
    Rprojectors = [(eye-ql)@(eye-qr), ql@(eye-qr)+(eye-ql)@qr, ql@qr]
    raise_c = embed(np.array([[0., 0.], [1., 0.]]), 3)
    checks, rows, synthetic = [], [], []

    def check(name, left, right=0., tolerance=None, tag=''):
        residual = float(np.max(abs(np.asarray(left)-np.asarray(right))))
        tol = CONFIG['tolerance'] if tolerance is None else tolerance
        checks.append(dict(name=name, tag=tag, residual=residual, tolerance=tol,
                           passed=bool(math.isfinite(residual) and residual <= tol)))

    def ex(state, op, tag=''):
        value = np.vdot(state, op@state)
        check('expectation_real', value.imag, tag=tag)
        return float(value.real)

    for case in cases:
        name, p = case['name'], case['parameters']
        expected = dict(h=1., Delta=4., U_d=1., d_star=1., epsilon_psi=1.,
            epsilon_r=1., epsilon_w=0., t_hop=.5, lambda_R=.5, lambda_J=.25, g=1.)
        if name == 'feedback_off':
            expected['lambda_R'] = 0.
        if name == 'copying_off':
            expected['g'] = 0.
        if p != expected:
            raise RuntimeError('Native coefficients differ')
        t, lam = p['t_hop'], p['lambda_R']
        nonhop = (3*eye+R-xa+(2.25*eye-lam*R)@n)
        H = nonhop-t*n@T
        jop, Dop = t*n@J, t*n@T
        check('BS_current_sign', J, 1j*(raise_c-raise_c.conj().T), tag=name)
        check('carrier_continuity', 1j*comm(H, P), jop, tag=name)
        check('carrier_double_commutator', comm(P, comm(H, P)), Dop, tag=name)
        for label, op in (('Hamiltonian', H), ('current', jop), ('contact', Dop)):
            check('record_channel_commutes_'+label, comm(R, op), tag=name)
        projectors, energies, blocks = [], [], []
        for count in range(3):
            for s in (1, -1):
                x = 2.25-lam*count-t*s
                d = math.hypot(x, 2.)
                block = Rprojectors[count]@(eye+s*T)/2
                axis = (2*xa+x*za)/d
                blocks.append((3+count+x/2, d, block, axis))
                for sign in (-1, 1):
                    energy = 3+count+(x+sign*d)/2
                    projector = block@(eye-sign*axis)/2
                    projectors.append(projector)
                    energies.append(energy)
                    old = next(r for r in case['spectrum_and_actual_weights']
                               if (r['R'], r['s'], r['beta']) == (count, s, sign))
                    check('saved_spectral_energy', energy, old['energy'], tag=name)
                    check('held_projector', H@projector, energy*projector, tag=name)
                    check('idempotent_projector', projector@projector, projector, tag=name)
        check('projector_resolution', sum(projectors), eye, tag=name)
        check('spectral_reconstruction', sum(e*q for e, q in zip(energies, projectors)), H, tag=name)
        formed = np.asarray(case['formed_vector']['real'])+1j*np.asarray(case['formed_vector']['imag'])
        check('saved_formed_norm', np.vdot(formed, formed), 1., tag=name)

        def readout(state, tag):
            energy = ex(state, H, tag)
            direct_D, direct_j = ex(state, Dop, tag), ex(state, jop, tag)
            nmean, Tmean, Jmean = ex(state, n, tag), ex(state, T, tag), ex(state, J, tag)
            rho = np.outer(state, state.conj())
            dephased = sum(q@rho@q for q in Rprojectors)
            for label, op in (('energy', H), ('contact', Dop), ('current', jop)):
                check('record_dephasing_'+label, np.trace(dephased@op), np.trace(rho@op), tag=tag)
            angles = []
            works = {}
            for angle in CONFIG['angles']:
                sn, cs = math.sin(angle), math.cos(angle)
                interaction = t*n@(T*(1-cs)-J*sn)
                Hphi = H+interaction
                peierls = nonhop-t*n@(np.exp(1j*angle)*raise_c+np.exp(-1j*angle)*raise_c.conj().T)
                gauge = eye+(np.exp(1j*angle)-1)*P
                twisted_j = t*n@(J*cs-T*sn)
                twisted_D = t*n@(T*cs+J*sn)
                twisted_J = J*cs-T*sn
                check('Peierls_matrix', Hphi, peierls, tag=tag)
                check('gauge_similarity_no_eigensolve', Hphi, gauge@H@gauge.conj().T, tag=tag)
                check('current_square_unchanged', twisted_J@twisted_J, J@J, tag=tag)
                check('twisted_continuity', 1j*comm(Hphi, P), twisted_j, tag=tag)
                check('twisted_double_commutator', comm(P, comm(Hphi, P)), twisted_D, tag=tag)
                work = ex(state, interaction, tag)
                predicted = direct_D*(1-cs)-direct_j*sn
                full = ex(state, Hphi, tag)
                check('exact_fixed_state_work', work, predicted, tag=tag)
                check('full_energy_offset_retained', full, energy+work, tag=tag)
                check('gauge_rotated_state_energy', ex(gauge@state, Hphi, tag), energy, tag=tag)
                state_work = ex(state, gauge.conj().T@H@gauge-H, tag)
                check('fixed_H_state_twist_opposite_sign', state_work,
                      direct_D*(1-cs)+direct_j*sn, tag=tag)
                check('record_dephasing_twisted_energy', np.trace(dephased@Hphi), full, tag=tag)
                check('analytic_energy_first_derivative', -ex(state, twisted_j, tag),
                      direct_D*sn-direct_j*cs, tag=tag)
                check('analytic_energy_second_derivative', ex(state, twisted_D, tag),
                      direct_D*cs+direct_j*sn, tag=tag)
                works[angle] = work
                angles.append(dict(phi=angle, complete_fixed_state_energy=full,
                    interaction_work=work, energy_derivative=-ex(state, twisted_j, tag),
                    energy_second_derivative=ex(state, twisted_D, tag),
                    fixed_H_state_twist_work=state_work))
            eps = CONFIG['small_angle']
            first = (works[eps]-works[-eps])/(2*math.sin(eps))
            second = (works[eps]+works[-eps])/(4*math.sin(eps/2)**2)
            check('stable_centered_first', first, -direct_j, CONFIG['small_angle_tolerance'], tag)
            check('stable_centered_second', second, direct_D, CONFIG['small_angle_tolerance'], tag)
            return dict(complete_held_energy=energy, contact_t_nT=direct_D,
                current_t_nJ=direct_j, carrier_right_rate=direct_j/CONFIG['hbar'],
                incidence_mean=nmean, transfer_mean=Tmean, current_operator_mean=Jmean,
                factorized_contact=t*nmean*Tmean, factorized_current=t*nmean*Jmean,
                contact_factorization_error=direct_D-t*nmean*Tmean,
                current_factorization_error=direct_j-t*nmean*Jmean,
                contact_frequency_moment=direct_D/CONFIG['hbar']**2,
                small_angle_first=first, small_angle_second=second, angles=angles)

        for old_age in case['hold']:
            age = old_age['time']
            U = sum(np.exp(-1j*e*age)*q for e, q in zip(energies, projectors))
            block_U = sum(np.exp(-1j*center*age)*q@(math.cos(d*age/2)*eye
                          +1j*math.sin(d*age/2)*axis) for center, d, q, axis in blocks)
            check('held_block_exponential', U, block_U, tag=name)
            check('held_unitarity', U.conj().T@U, eye, tag=name)
            state = U@formed
            tag = name+':'+str(age)
            for label, op, value in (('norm', eye, 1.), ('record', R, old_age['record_count']),
                ('link', n, old_age['link_occupation']), ('carrier', P, old_age['carrier_right']),
                ('energy', H, case['held_energy'])):
                check('saved_'+label, ex(state, op, tag), value, tag=tag)
            result = readout(state, tag)
            check('saved_hopping_contact', result['contact_t_nT'],
                  -old_age['energy_terms']['carrier_hopping'], tag=tag)
            check('saved_component_energy_sum', sum(old_age['energy_terms'].values()),
                  result['complete_held_energy'], tag=tag)
            rows.append(dict(preparation=name, age=age, parameters=p, readout=result))
        if name == 'native':
            carrier_vectors = [('Xplus', [1, 1], t, 0.), ('Xminus', [1, -1], -t, 0.),
                ('Yplus', [1, 1j], 0., t), ('Yminus', [1, -1j], 0., -t),
                ('left', [1, 0], 0., 0.)]
            for label, pair, d_expected, j_expected in carrier_vectors:
                state = np.zeros(16, complex)
                state[2:4] = np.asarray(pair)/np.linalg.norm(pair)
                result = readout(state, 'synthetic:'+label)
                check('synthetic_contact', result['contact_t_nT'], d_expected, tag=label)
                check('synthetic_current', result['current_t_nJ'], j_expected, tag=label)
                synthetic.append(dict(label=label, incidence='on', readout=result))
            state = np.zeros(16, complex)
            state[:2] = 1/math.sqrt(2)
            result = readout(state, 'synthetic:incidence_off')
            check('synthetic_incidence_off_contact', result['contact_t_nT'])
            check('synthetic_incidence_off_current', result['current_t_nJ'])
            synthetic.append(dict(label='Xplus', incidence='off', readout=result))
    check('actual_state_census', len(rows), 15)
    check('synthetic_control_census', len(synthetic), 6)
    failures = [c for c in checks if not c['passed']]
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        peak *= 1024
    payload = dict(configuration=CONFIG, rows=rows, synthetic_controls=synthetic,
        checks=checks, check_count=len(checks), failure_count=len(failures),
        scope='Native fixed-state transport contact/current and pure-gauge controls; no relaxed modulus, continuum alpha, physical ruler or new formation.',
        seconds=time.perf_counter()-started, peak_rss_bytes=int(peak))
    payload['output_target_exceeded'] = len(encode(payload)) > CONFIG['output_target_bytes']
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS',
        freeze_sha256=sha(FREEZE), payload_sha256=hashlib.sha256(encode(payload)).hexdigest(), payload=payload)


def main():
    if sys.argv[1:] == ['freeze']:
        result = inputs()[1]
    elif sys.argv[1:] == ['run']:
        result = run()
    else:
        raise ValueError('usage: native_transport_twist_v001.py freeze|run')
    print(encode(result).decode())
    return 0 if result.get('status', 'COMPLETE') == 'COMPLETE' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(encode(dict(status='ERROR', error_type=type(exc).__name__, error=str(exc))).decode())
        sys.exit(1)
