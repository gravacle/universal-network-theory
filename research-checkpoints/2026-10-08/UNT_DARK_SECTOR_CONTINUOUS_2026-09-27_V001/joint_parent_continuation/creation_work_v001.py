"""Small clamped-port creation test: authenticated inputs, stdout results only."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CONFIG = dict(Omega=1., Delta=4., Ud=1., dstar=1., Kg=2., Kv=3., C=.5,
              gamma=1., vcell=.25, supply_gap=3., epsilon=.2, hbar=1.,
              gs=[0., .4], volumes=[.5, .8], times=[0., .25, .5, 1., 2.],
              derivative_step=.125, tol=1e-10, nested_tol=1e-9)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    paths = [Path(__file__).resolve(), HERE/'CREATION_WORK_PROTOCOL_V001.md',
             HERE/'NATIVE_AUTONOMOUS_CONTROLLER_CANDIDATE_V001.md',
             HERE/'NATIVE_VOLUME_INCREMENT_PATHWAY.md',
             HERE.parent/'recovered_sources/BS_MICRO_ACTION.md']
    return dict(config=CONFIG, files={str(p.relative_to(ROOT)): sha(p) for p in paths})


def incidence(n):
    dim = 2**(n*n)
    states = np.arange(dim)
    occupied = np.array([(states >> e) & 1 for e in range(n*n)]).T
    ns = [np.diag(occupied[:, e]).astype(complex) for e in range(n*n)]
    xs = []
    for e in range(n*n):
        x = np.zeros((dim, dim), complex)
        x[states ^ (1 << e), states] = 1
        xs.append(x)
    degree = occupied.reshape(dim, n, n)
    energy = CONFIG['Delta']*occupied.sum(axis=1)
    energy += CONFIG['Ud']*((degree.sum(axis=1)-CONFIG['dstar'])**2).sum(axis=1)
    energy += CONFIG['Ud']*((degree.sum(axis=2)-CONFIG['dstar'])**2).sum(axis=1)
    h = np.diag(energy).astype(complex)-CONFIG['Omega']/n*sum(xs)
    connected = []
    for bits in occupied:
        seen = {0}
        pending = [0]
        while pending:
            vertex = pending.pop()
            neighbors = ([n+j for j in range(n) if bits[vertex*n+j]] if vertex < n
                         else [i for i in range(n) if bits[i*n+vertex-n]])
            for nxt in neighbors:
                if nxt not in seen:
                    seen.add(nxt)
                    pending.append(nxt)
        connected.append(len(seen) == 2*n)
    return h, sum(ns), xs, np.diag(connected).astype(complex)


def block(a, b):
    result = np.zeros((len(a)+len(b), len(a)+len(b)), complex)
    result[:len(a), :len(a)] = a
    result[len(a):, len(a):] = b
    return result


def comm(a, b):
    return a @ b - b @ a


def taylor(h, t):
    a = -1j*t*h/CONFIG['hbar']
    norm = float(np.linalg.norm(a, ord=np.inf))
    scale = max(0, math.ceil(math.log2(norm/.5))) if norm else 0
    a /= 2**scale
    norm = float(np.linalg.norm(a, ord=np.inf))
    total = np.eye(len(h), dtype=complex)
    term, magnitude = total.copy(), 1.
    for k in range(1, 201):
        term = term @ a/k
        total += term
        magnitude *= norm/k
        if math.exp(norm)*magnitude*norm/(k+1) <= 1e-18:
            break
    else:
        raise ArithmeticError('Taylor remainder failed')
    for _ in range(scale):
        total = total @ total
    return total


def run():
    started = time.perf_counter()
    freeze = HERE/'CREATION_WORK_V001_FROZEN.json'
    if json.loads(freeze.read_text()) != snapshot():
        raise RuntimeError('Prospective input freeze differs')
    h1, b1, x1, conn1 = incidence(1)
    h2, b2, x2, conn2 = incidence(2)
    inc = np.zeros((16, 2), complex)
    inc[0, 0] = inc[1, 1] = 1
    ident = np.eye(36)
    nat = block(h1, h2)
    bnat = block(b1, b2)
    n_native = block(np.eye(2), 2*np.eye(16))
    j = np.zeros((18, 18), complex)
    j[2:, :2] = inc
    lower = np.array([[0., 1.], [0., 0.]])
    supply_n = np.diag([0., 1.])
    full_n = np.kron(n_native, np.eye(2))
    full_b = np.kron(bnat, np.eye(2))
    full_supply = np.kron(np.eye(18), supply_n)
    charge = full_n + full_supply
    creation = np.kron(j, lower)
    target_projector = full_n-ident
    connectivity = np.kron(block(conn1, conn2), np.eye(2))
    maxima, counts, failures, cases, summaries = {}, {}, [], [], []

    def check(name, value, expected=0., tol=None, tag=''):
        tolerance = CONFIG['tol'] if tol is None else tol
        error = float(np.max(np.abs(np.asarray(value)-np.asarray(expected))))
        maxima[name] = max(maxima.get(name, 0.), error)
        counts[name] = counts.get(name, 0)+1
        if not math.isfinite(error) or error > tolerance:
            failures.append(dict(check=name, error=error, tolerance=tolerance, case=tag))
        return error

    def expect(state, operator):
        answer = np.vdot(state, operator @ state)
        check('hermitian_expectation_imaginary', answer.imag)
        return float(answer.real)

    def elastic(n, g, volume):
        z = volume-2*n*CONFIG['vcell']
        return .5*CONFIG['Kg']*g*g+CONFIG['C']*g*z+.5*CONFIG['Kv']*z*z

    def components(g, volume):
        return [np.kron(nat, np.eye(2)), -CONFIG['gamma']*g*full_b,
                np.kron(block(elastic(1,g,volume)*np.eye(2),
                              elastic(2,g,volume)*np.eye(16)), np.eye(2)),
                CONFIG['supply_gap']*full_supply,
                CONFIG['epsilon']*(creation+creation.conj().T)]

    def ham(g, volume):
        return sum(components(g, volume))

    check('inclusion_isometry', inc.conj().T @ inc, np.eye(2))
    check('bare_stiffness_positive', max(0., CONFIG['C']**2-CONFIG['Kg']*CONFIG['Kv']))
    check('inclusion_source_intertwiner', b2 @ inc, inc @ b1)
    check('native_source_creation_commutator', comm(full_b, creation))
    for g in CONFIG['gs']:
        for volume in CONFIG['volumes']:
            tag = f'g{g}:V{volume}'
            parts = components(g, volume)
            h = sum(parts)
            check('hermiticity', h, h.conj().T, tag=tag)
            check('full_charge_commutator', comm(h, charge), tag=tag)
            expected_strength = np.kron(block(CONFIG['Omega']*sum(x1),
                                             CONFIG['Omega']/2*sum(x2)), np.eye(2))
            check('native_strength', comm(full_b, comm(h, full_b)), expected_strength, tag=tag)
            p1 = -(CONFIG['C']*g+CONFIG['Kv']*(volume-2*CONFIG['vcell']))
            p2 = -(CONFIG['C']*g+CONFIG['Kv']*(volume-4*CONFIG['vcell']))
            d = 2*CONFIG['vcell']
            check('pressure_jump', p2-p1, CONFIG['Kv']*d, tag=tag)
            a = h1-CONFIG['gamma']*g*b1+(elastic(1,g,volume)+CONFIG['supply_gap'])*np.eye(2)
            dmat = h2-CONFIG['gamma']*g*b2+elastic(2,g,volume)*np.eye(16)
            detuning = (2*CONFIG['Ud']*CONFIG['dstar']**2-CONFIG['supply_gap']+
                        d*p1+.5*CONFIG['Kv']*d*d)*np.eye(2)+CONFIG['Omega']/2*x1[0]
            defect = dmat @ inc-inc @ a
            leakage = -CONFIG['Omega']/2*sum(x2[1:]) @ inc
            check('compressed_creation_work', inc.conj().T @ defect, detuning, tag=tag)
            check('full_creation_work', defect, inc @ detuning+leakage, tag=tag)
            check('leakage_orthogonal', inc.conj().T @ leakage, tag=tag)
            check('leakage_singular_values', np.linalg.svd(leakage, compute_uv=False),
                  CONFIG['Omega']*math.sqrt(3)/2, tag=tag)
            check('native_charge_current', 1j*comm(h, full_n),
                  1j*CONFIG['epsilon']*(creation.conj().T-creation), tag=tag)
            z = volume*ident-2*CONFIG['vcell']*full_n
            step = CONFIG['derivative_step']
            dg = (ham(g+step,volume)-ham(g-step,volume))/(2*step)
            dv = (ham(g,volume+step)-ham(g,volume-step))/(2*step)
            check('source_force', dg, CONFIG['Kg']*g*ident+CONFIG['C']*z-CONFIG['gamma']*full_b, tag=tag)
            check('volume_force', dv, CONFIG['C']*g*ident+CONFIG['Kv']*z, tag=tag)
            check('source_contact', (ham(g+step,volume)-2*h+ham(g-step,volume))/step**2,
                  CONFIG['Kg']*ident, tag=tag)
            check('volume_contact', (ham(g,volume+step)-2*h+ham(g,volume-step))/step**2,
                  CONFIG['Kv']*ident, tag=tag)
            mixed = (ham(g+step,volume+step)-ham(g+step,volume-step)
                     -ham(g-step,volume+step)+ham(g-step,volume-step))/(4*step**2)
            check('mixed_contact', mixed, CONFIG['C']*ident, tag=tag)
            current_parts = [1j*comm(h, part) for part in parts]
            check('component_current_operator_sum', sum(current_parts), tag=tag)
            values, vectors = np.linalg.eigh(h)
            propagators = {}
            for t in CONFIG['times']:
                ut = taylor(h,t)
                ue = (vectors*np.exp(-1j*t*values)) @ vectors.conj().T
                check('cross_propagator', ut, ue, tag=f'{tag}:t{t}')
                check('unitarity', ut.conj().T @ ut, ident, tag=f'{tag}:t{t}')
                propagators[t] = ut
            old_states = [('blank',np.array([1.,0.],complex)),
                          ('plus',np.array([1.,1.],complex)/math.sqrt(2)),
                          ('phase',np.array([1.,1j],complex)/math.sqrt(2))]
            for state_name, psi in old_states:
                s = np.kron(np.concatenate((psi, np.zeros(16))), np.array([0.,1.]))
                target = np.kron(np.concatenate((np.zeros(2), inc @ psi)), np.array([1.,0.]))
                derivative = full_n.copy()
                expected_derivatives = [0.,2*CONFIG['epsilon']**2,0.]
                for order, expected in enumerate(expected_derivatives,1):
                    derivative = 1j*comm(h,derivative)
                    check(f'initial_creation_derivative_{order}', expect(s,derivative), expected,
                          CONFIG['nested_tol'] if order==3 else None, f'{tag}:{state_name}')
                preparations = [('source',s),('target',target),
                                ('phase_plus',(s+1j*target)/math.sqrt(2)),
                                ('phase_minus',(s-1j*target)/math.sqrt(2))]
                for prep_name, initial in preparations:
                    prep_tag = f'{tag}:{state_name}:{prep_name}'
                    initial_energies = [expect(initial, part) for part in parts]
                    if prep_name.startswith('phase_'):
                        sign = -1 if prep_name=='phase_plus' else 1
                        check('opposite_coherent_currents', expect(initial,1j*comm(h,full_n)),
                              sign*CONFIG['epsilon'],tag=prep_tag)
                    summaries.append(dict(g=g, V=volume, old_state=state_name, preparation=prep_name,
                                          initial_energies=initial_energies))
                    for t, ut in propagators.items():
                        final = ut @ initial
                        energies = [expect(final, part) for part in parts]
                        currents = [expect(final, part) for part in current_parts]
                        check('state_normalization', np.vdot(final,final),1.,tag=prep_tag)
                        check('conserved_energy', sum(energies),sum(initial_energies),tag=prep_tag)
                        check('conserved_charge', expect(final,charge),2.,tag=prep_tag)
                        check('component_energy_sum',sum(energies),expect(final,h),tag=prep_tag)
                        check('component_current_sum',sum(currents),tag=prep_tag)
                        current = expect(final,1j*comm(h,full_n))
                        check('coherence_current',current,2*CONFIG['epsilon']*np.vdot(final,creation @ final).imag,tag=prep_tag)
                        prob_target = expect(final,target_projector)
                        prob_connected = expect(final,connectivity)
                        larger_connected = expect(final,target_projector @ connectivity)
                        check('probability_range', max(0.,-prob_target,prob_target-1.,-prob_connected,prob_connected-1.,
                                                       -larger_connected,larger_connected-prob_target),tag=prep_tag)
                        cases.append(dict(g=g,V=volume,old_state=state_name,preparation=prep_name,t=t,
                                          target_probability=prob_target,connected_probability=prob_connected,
                                          larger_connected_probability=larger_connected,creation_current=current,
                                          energies=energies,currents=currents))
    check('case_census',len(cases),240,0.)
    payload = dict(config=CONFIG, scope='Clamped finite source-work candidate, not physical geometry or cosmological expansion.',
                   component_order=['native','source','elastic','supply','creation'],initial=summaries,cases=cases,
                   check_counts=counts,maximum_errors=maxima,failures=failures)
    result = dict(status='COMPLETE' if not failures else 'FAILED',payload=payload,
                  payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),freeze_sha256=sha(freeze),
                  seconds=time.perf_counter()-started,peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result,allow_nan=False))
    return 1 if failures else 0


if __name__ == '__main__':
    if sys.argv[1:] == ['freeze']:
        print(json.dumps(snapshot(),indent=2))
    elif sys.argv[1:]:
        raise SystemExit('Use freeze or no arguments')
    else:
        raise SystemExit(run())
