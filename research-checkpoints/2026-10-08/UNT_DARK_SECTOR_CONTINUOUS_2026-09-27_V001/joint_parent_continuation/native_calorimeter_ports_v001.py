"""Explicit independent calorimeter ports; inert definitions, stdout freeze/run."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE / 'NATIVE_CALORIMETER_PORTS_V001_FROZEN.json'
CONFIG = dict(record_occupations=[0, 1], native_preparations=['cycle', 'tree'],
              ages=[0., .5, 2.], frequencies=[.75, 1.5, 3.], durations=[.25, 1., 2.],
              couplings=[.01, .005], probe_edges=[0, 3],
              probe_inputs=['00', '10', '01'], dimension=256, hbar=1.,
              operator_tolerance=2e-11, state_tolerance=2e-9,
              energy_tolerance=2e-8, weak_bound_roundoff_allowance=2e-9)
PINS = {
    'NATIVE_THERMAL_PACKET_V001_RESULTS.json': '8531cd6f2cf7d60e4b981428c9f80b55ee76b23f17bd4ab91c0e435894010538',
    'NATIVE_THERMAL_PACKET_V001_FROZEN.json': '4a6ed3c387bc87961264806ef630f988199bfdde0b3f9d81fb53b11a2c40f0b3',
}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cjson(value):
    value = np.asarray(value)
    return dict(real=value.real.tolist(), imag=value.imag.tolist())


def complex_array(value):
    return np.asarray(value['real'])+1j*np.asarray(value['imag'])


def inputs():
    files = {}
    for name, expected in PINS.items():
        path = (HERE/name).resolve()
        path.relative_to(ROOT)
        if sha(path) != expected:
            raise RuntimeError('Pinned packet differs: '+name)
        files[str(path.relative_to(ROOT))] = expected
    old = json.loads((HERE/'NATIVE_THERMAL_PACKET_V001_RESULTS.json').read_text())
    frozen = json.loads((HERE/'NATIVE_THERMAL_PACKET_V001_FROZEN.json').read_text())
    if old['status'] != 'COMPLETE' or old['payload']['failures'] or any(s['status'] != 'COMPLETE' or s['failures'] for s in old['payload']['sectors']):
        raise RuntimeError('Unqualified native packet')
    if old['payload_sha256'] != hashlib.sha256(encoded(old['payload'])).hexdigest() or old['freeze_sha256'] != PINS['NATIVE_THERMAL_PACKET_V001_FROZEN.json']:
        raise RuntimeError('Native packet envelope differs')
    for name, expected in frozen['files'].items():
        path = (ROOT/name).resolve()
        path.relative_to(ROOT)
        if sha(path) != expected:
            raise RuntimeError('Native ancestor differs: '+name)
        files[name] = expected
    oldcfg = old['payload']['config']
    for new, prior in [('ages', 'probe_ages'), ('frequencies', 'frequencies'),
                       ('durations', 'durations'), ('record_occupations', 'record_occupations'),
                       ('native_preparations', 'labels')]:
        if CONFIG[new] != oldcfg[prior]:
            raise RuntimeError('Inherited census differs: '+new)
    for name in ('native_calorimeter_ports_v001.py', 'NATIVE_CALORIMETER_PORTS_PROTOCOL_V001.md',
                 'NATIVE_THERMAL_PACKET_MECHANISM_AND_PORT_TEST_V001.md'):
        path = (HERE/name).resolve()
        files[str(path.relative_to(ROOT))] = sha(path)
    return old['payload'], dict(files=files, config=CONFIG)


def load_definitions(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    started = time.perf_counter()
    parent, snapshot = inputs()
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze mismatch')
    native = load_definitions('calorimeter_native_packet_definitions', 'native_thermal_packet_v001.py')
    numerical = load_definitions('calorimeter_owned_chebyshev_definitions', 'native_carrier_ruler_v001.py')
    failures, maxima, counts = [], {}, {}

    def check(name, actual, expected=0., tolerance=None, tag=''):
        error = float(np.max(abs(np.asarray(actual)-np.asarray(expected))))
        limit = CONFIG['operator_tolerance'] if tolerance is None else tolerance
        counts[name] = counts.get(name, 0)+1
        maxima[name] = max(maxima.get(name, 0.), error)
        if not math.isfinite(error) or error > limit:
            failures.append(dict(check=name, case=tag, error=error, tolerance=limit))

    identity64, identity4, identity2 = np.eye(64), np.eye(4), np.eye(2)
    lower = np.array([[0., 1.], [0., 0.]])
    number = lower.T @ lower
    spinx = lower+lower.T
    nprobe = [np.kron(number, identity2), np.kron(identity2, number)]
    aprobe = [np.kron(lower, identity2), np.kron(identity2, lower)]
    xprobe = [np.kron(spinx, identity2), np.kron(identity2, spinx)]
    cross = aprobe[0].conj().T @ aprobe[1]
    rows, methods, spectra, controls = [], [], [], []
    for q in CONFIG['record_occupations']:
        saved = next(s for s in parent['sectors'] if s['record_occupation'] == q)
        h, independent, hv, incidence, population, current, edges = native.operators(q)
        check('native_operator_reconstruction', h, independent)
        hnative = np.kron(h, identity4)
        interaction = sum(np.kron(incidence[e], xp) for e, xp in zip(CONFIG['probe_edges'], xprobe))
        check('independent_probe_commutation', xprobe[0] @ xprobe[1], xprobe[1] @ xprobe[0])
        check('port_Hermitian', interaction, interaction.conj().T)
        # Each incidence projector has norm1 and each Pauli-X norm1: ||V||<=2.
        check('port_row_norm_bound', max(0., float(np.max(np.sum(abs(interaction), axis=1)))-2.))
        columns, metadata = [], []
        for name in CONFIG['native_preparations']:
            for age in CONFIG['ages']:
                hold = next(r for r in saved['holds'] if r['preparation'] == name and r['age'] == age)
                psi = complex_array(hold['state_vector'])
                check('saved_native_norm', np.vdot(psi, psi), 1., CONFIG['state_tolerance'])
                check('saved_native_energy', np.vdot(psi, h @ psi), hold['energy'], CONFIG['energy_tolerance'])
                for label in CONFIG['probe_inputs']:
                    probe = np.zeros(4)
                    probe[int(label, 2)] = 1.
                    columns.append(np.kron(psi, probe))
                    metadata.append(dict(preparation=name, age=age, probe_input=label,
                                         native_energy=hold['energy']))
        initial = np.column_stack(columns)
        check('initial_port_mean', np.sum(initial.conj()*(interaction @ initial), axis=0))
        for omega in CONFIG['frequencies']:
            hprobe4 = omega*(nprobe[0]+nprobe[1])
            hprobe = np.kron(identity64, hprobe4)
            hfree = hnative+hprobe
            initial_free_energy = np.sum(initial.conj()*(hfree @ initial), axis=0).real
            for coupling in CONFIG['couplings']:
                hon = hfree+coupling*interaction
                check('on_Hamiltonian_Hermitian', hon, hon.conj().T)
                values, vectors = np.linalg.eigh(hon)
                check('on_eigensystem', hon @ vectors, vectors*values, CONFIG['state_tolerance'])
                check('on_eigenvectors_unitary', vectors.conj().T @ vectors, np.eye(256), CONFIG['state_tolerance'])
                initial_e = vectors.conj().T @ initial
                diag = np.diag(hon).real
                rad = np.sum(abs(hon), axis=1)-abs(np.diag(hon))
                low, high = float(np.min(diag-rad)), float(np.max(diag+rad))
                center, radius = (low+high)/2, (high-low)/2
                check('Gershgorin_enclosure', max(0., low-values[0], values[-1]-high))
                spectra.append(dict(record_occupation=q, omega=omega, coupling=coupling,
                                    eigenvalues=values.tolist(), gershgorin=[low, high]))
                for duration in CONFIG['durations']:
                    tagbase = f'{q}:{omega}:{coupling}:{duration}'
                    final = vectors @ (np.exp(-1j*values*duration)[:, None]*initial_e)
                    oracle, info = numerical.chebyshev_action(lambda x: hon @ x, initial, center, radius, duration)
                    agreement = np.linalg.norm(final-oracle, axis=0)
                    check('independent_Chebyshev_state', agreement, tolerance=CONFIG['state_tolerance'], tag=tagbase)
                    methods.append(dict(record_occupation=q, omega=omega, coupling=coupling, duration=duration,
                                        dual_vector_errors=agreement.tolist(), Chebyshev=info))
                    beta = 2*abs(coupling)*duration
                    remainder2 = math.cosh(beta)-1.
                    remainder3 = math.sinh(beta)-beta
                    prob_bound = 2*beta*remainder3+remainder3**2+remainder2**2
                    cross_bound = 2*beta*remainder3+remainder3**2
                    mean_bound = remainder3+2*remainder2*math.sinh(beta)
                    connected_bound = cross_bound+2*beta*mean_bound+mean_bound**2
                    for col, meta in enumerate(metadata):
                        tag = tagbase+':'+str(col)
                        psi = final[:, col]
                        native_e = float(np.vdot(psi, hnative @ psi).real)
                        probe_e = float(np.vdot(psi, hprobe @ psi).real)
                        interaction_e = coupling*float(np.vdot(psi, interaction @ psi).real)
                        total = native_e+probe_e+interaction_e
                        initial_probe_e = omega*sum(int(x) for x in meta['probe_input'])
                        switch_on = 0.
                        switch_off = -interaction_e
                        delta_native = native_e-meta['native_energy']
                        delta_probe = probe_e-initial_probe_e
                        ledger_error = delta_native+delta_probe-switch_on-switch_off
                        check('state_norm', np.vdot(psi, psi), 1., CONFIG['state_tolerance'], tag)
                        check('on_energy_conserved', total, initial_free_energy[col], CONFIG['energy_tolerance'], tag)
                        check('switch_work_ledger', ledger_error, tolerance=CONFIG['energy_tolerance'], tag=tag)
                        shaped = psi.reshape(64, 4)
                        rho = shaped.T @ shaped.conj()
                        check('probe_density_Hermitian', rho, rho.conj().T)
                        check('probe_density_trace', np.trace(rho), 1., CONFIG['state_tolerance'], tag)
                        check('probe_density_PSD', max(0., -float(np.linalg.eigvalsh(rho).min())), tolerance=CONFIG['state_tolerance'], tag=tag)
                        occupations = np.array([np.trace(rho @ n).real for n in nprobe])
                        mean = np.array([np.trace(rho @ a) for a in aprobe])
                        coherence = complex(np.trace(rho @ cross))
                        connected = coherence-mean[0].conjugate()*mean[1]
                        check('probe_energy_from_occupations', omega*sum(occupations), probe_e, CONFIG['state_tolerance'], tag)
                        inherited = {}
                        for sign in (1, -1):
                            inherited[sign] = next(r for r in saved['probe_grams']
                                if r['preparation'] == meta['preparation'] and r['age'] == meta['age']
                                and r['omega'] == omega and r['duration'] == duration and r['sign'] == sign)
                        flip, weak_coeff, coefficient_error = [], [], []
                        for j, edge in enumerate(CONFIG['probe_edges']):
                            occupied = int(meta['probe_input'][j])
                            measured = 1-occupations[j] if occupied else occupations[j]
                            reference = inherited[-1 if occupied else 1]['K']['real'][edge][edge]
                            difference = measured-coupling**2*reference
                            check('population_Dyson_bound', max(0., abs(difference)-prob_bound),
                                  tolerance=CONFIG['weak_bound_roundoff_allowance'], tag=tag+':'+str(j))
                            flip.append(float(measured))
                            weak_coeff.append(float(reference))
                            coefficient_error.append(float(measured/coupling**2-reference))
                        weak_vacuum = None
                        if meta['probe_input'] == '00':
                            plus = inherited[1]
                            expected_mean = -1j*coupling*np.exp(-1j*omega*duration)*complex_array(plus['mean'])[CONFIG['probe_edges']]
                            expected_cross = coupling**2*complex_array(plus['K'])[0, 3]
                            expected_connected = coupling**2*complex_array(plus['connected_K'])[0, 3]
                            check('coherent_mean_Dyson_bound', max(0., float(np.max(abs(mean-expected_mean)))-mean_bound),
                                  tolerance=CONFIG['weak_bound_roundoff_allowance'], tag=tag)
                            check('cross_coherence_Dyson_bound', max(0., abs(coherence-expected_cross)-cross_bound),
                                  tolerance=CONFIG['weak_bound_roundoff_allowance'], tag=tag)
                            check('connected_coherence_Dyson_bound', max(0., abs(connected-expected_connected)-connected_bound),
                                  tolerance=CONFIG['weak_bound_roundoff_allowance'], tag=tag)
                            weak_vacuum = dict(expected_mean=cjson(expected_mean), expected_cross=cjson(expected_cross),
                                               expected_connected=cjson(expected_connected),
                                               mean_error=cjson(mean-expected_mean),
                                               cross_coefficient_error=cjson(coherence/coupling**2-expected_cross/coupling**2),
                                               connected_coefficient_error=cjson(connected/coupling**2-expected_connected/coupling**2))
                        rows.append(dict(record_occupation=q, omega=omega, coupling=coupling, duration=duration,
                                         **meta, native_energy_final=native_e, probe_energy_initial=initial_probe_e,
                                         probe_energy_final=probe_e, interaction_energy_before_off=interaction_e,
                                         total_on_energy=total, switch_on_work=switch_on, switch_off_work=switch_off,
                                         delta_native_energy=delta_native, delta_probe_energy=delta_probe,
                                         work_ledger_residual=ledger_error, probe_density=cjson(rho),
                                         probe_occupation=occupations.tolist(), mean_lowering=cjson(mean),
                                         cross_coherence=cjson(coherence), connected_cross=cjson(connected),
                                         flip_probability=flip, weak_flip_coefficient=weak_coeff,
                                         flip_coefficient_error=coefficient_error, vacuum_weak_comparison=weak_vacuum,
                                         rigorous_Dyson_bounds=dict(beta=beta, probability=prob_bound, cross=cross_bound,
                                                                   mean=mean_bound, connected=connected_bound),
                                         dual_state_error=float(agreement[col])))
    coarse = {tuple(r[k] for k in ('record_occupation','preparation','age','omega','duration','probe_input')):r
              for r in rows if r['coupling'] == CONFIG['couplings'][0]}
    for fine in (r for r in rows if r['coupling'] == CONFIG['couplings'][1]):
        key = tuple(fine[k] for k in ('record_occupation','preparation','age','omega','duration','probe_input'))
        old = coarse[key]
        controls.append(dict(key=list(key), coarse_error=old['flip_coefficient_error'],
                             fine_error=fine['flip_coefficient_error'],
                             normalized_coefficient_difference=(np.array(fine['flip_coefficient_error'])-old['flip_coefficient_error']).tolist(),
                             scope='Reported g-halving correction, not a demanded asymptotic ratio or thermal-success gate.'))
    check('full_row_census', len(rows), 648, 0.)
    check('spectral_census', len(spectra), 12, 0.)
    check('method_census', len(methods), 36, 0.)
    check('coupling_pair_census', len(controls), 324, 0.)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        rss *= 1024
    payload = dict(config=CONFIG, rows=rows, spectra=spectra, methods=methods, coupling_refinement=controls,
                   maximum_errors=maxima, check_counts=counts, failures=failures,
                   elapsed_seconds=time.perf_counter()-started, peak_self_rss_bytes=int(rss),
                   scope='Explicit new two-level calorimeter ports with full switch work; not a Gibbs bath, physical photon model, temperature fit, or source-contact/volume calibration.')
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS', payload=payload,
                payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(), freeze_sha256=sha(FREEZE))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('freeze', 'run'):
        raise ValueError('usage: native_calorimeter_ports_v001.py freeze|run')
    result = inputs()[1] if sys.argv[1] == 'freeze' else run()
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status='ERROR', error_type=type(exc).__name__, error=str(exc))))
        sys.exit(1)
