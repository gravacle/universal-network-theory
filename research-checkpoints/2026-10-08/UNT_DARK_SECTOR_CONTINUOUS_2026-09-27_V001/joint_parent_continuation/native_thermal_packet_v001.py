"""Owned native64 transport/probe packet. Inert definitions; stdout freeze/run only."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ('OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'OMP_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE / 'NATIVE_THERMAL_PACKET_V001_FROZEN.json'
TIMES = [0., 1/32, 1/16, 1/8, .25, .5, 1., math.pi/2, 2., math.pi, 4.]
PARAMETERS = dict(hbar=1., Omega=1., U_d=1., d_star=1., Delta=4.,
                  epsilon_psi=1., t_hop=.5, lambda_J=.25)
RECORD_PARAMETERS = dict(epsilon_r=1., lambda_R=.5)
CONFIG = dict(dimension_per_sector=64, record_occupations=[0, 1],
              masks=[15, 11], labels=['cycle', 'tree'],
              initial_vertex=0, times=TIMES, node_labels=['L0', 'L1', 'R0', 'R1'],
              patch_nodes=[0, 1], probe_ages=[0., .5, 2.],
              frequencies=[.75, 1.5, 3.], durations=[.25, 1., 2.],
              frequency_signs=[1, -1], quadrature_orders=[32, 64],
              operator_tolerance=2e-11, state_tolerance=2e-9,
              energy_tolerance=2e-8, probe_tolerance=1e-9,
              psd_scaled_tolerance=1e-10, energy_group_tolerance=1e-10,
              line_reporting_floor=1e-12, taylor_scaled_norm=.5,
              taylor_local_tail=1e-19, taylor_max_terms=256)
PINS = {
    'NATIVE_CARRIER_RULER_V001_RESULTS.json': 'f170be1dc580c2c0c2f3ebfd1740d1e728a69970c5ba4acf1d3dfc0a25b5713b',
    'NATIVE_CARRIER_RULER_V001_FROZEN.json': 'e507c9efbf07d5a3106cf96c4bbaa4f6940e68dd93d308a5e79ccc8b13c43abb',
    'NATIVE_CARRIER_RULER_V001_RESULT_REVIEW.md': '6c1dd76087d452af58f5c69c42e4ce2579a7fb71dc9869240f9c69d9341dd5ec',
    'NATIVE_THERMAL_CONNECTIVITY_DISCRIMINATOR_V001.md': '45ba0ee0b5f043e4e00d86082dfba267a2341a3f6c40fbddcb66bd40f7ecdd4b',
    'NATIVE_PHOTON_PROBE_PROTOCOL_V001.md': '53c92206a2351a45d119fdc80c75e190c27061e2788ff9991495be7ba9477598',
    'record_addition_compute.py': '4df3bbc8b38ad6b602841b7b28a7a59d37e69d60286f7a2ef11c37ddc150ce10',
}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cjson(value):
    value = np.asarray(value)
    return dict(real=value.real.tolist(), imag=value.imag.tolist())


def inputs():
    files = {}
    for name, expected in PINS.items():
        path = (HERE / name).resolve()
        path.relative_to(ROOT)
        if sha(path) != expected:
            raise RuntimeError('Pinned input differs: ' + name)
        files[str(path.relative_to(ROOT))] = expected
    old = json.loads((HERE / 'NATIVE_CARRIER_RULER_V001_RESULTS.json').read_text())
    frozen = json.loads((HERE / 'NATIVE_CARRIER_RULER_V001_FROZEN.json').read_text())
    if old['status'] != 'COMPLETE' or not all(c['passed'] for c in old['payload']['checks']):
        raise RuntimeError('Unqualified owned native result')
    if (old['payload_sha256'] != hashlib.sha256(encoded(old['payload'])).hexdigest()
            or old['freeze_sha256'] != PINS['NATIVE_CARRIER_RULER_V001_FROZEN.json']):
        raise RuntimeError('Owned result envelope mismatch')
    if old['payload']['parameters'] != PARAMETERS or frozen['parameters'] != PARAMETERS:
        raise RuntimeError('Native parameter mismatch')
    if old['payload']['configuration']['times'] != TIMES:
        raise RuntimeError('Owned time census mismatch')
    for name, expected in frozen['files'].items():
        path = (HERE / name).resolve()
        path.relative_to(ROOT)
        if sha(path) != expected:
            raise RuntimeError('Native ancestor differs: ' + name)
        files[str(path.relative_to(ROOT))] = expected
    for name in ('native_thermal_packet_v001.py', 'NATIVE_THERMAL_PACKET_PROTOCOL_V001.md'):
        path = HERE / name
        files[str(path.relative_to(ROOT))] = sha(path)
    return old, dict(files=files, parameters=PARAMETERS, record_parameters=RECORD_PARAMETERS, config=CONFIG)


def comm(a, b):
    return a @ b - b @ a


def operators(record_occupation):
    """Node partition (primary) versus a separately assembled full row operator."""
    edges = [(i, 2+j) for i in range(2) for j in range(2)]
    masks = np.arange(16)
    bits = ((masks[:, None] >> np.arange(4)) & 1).astype(float)
    deg = np.zeros((16, 4))
    n, flips, hop, carrier_current = [], [], [], []
    ident4 = np.eye(4)
    p = [np.kron(np.eye(16), np.diag(ident4[v])) for v in range(4)]
    for edge, (u, v) in enumerate(edges):
        deg[:, u] += bits[:, edge]
        deg[:, v] += bits[:, edge]
        n.append(np.diag(np.repeat(bits[:, edge], 4)))
        x = np.zeros((16, 16))
        x[masks ^ (1 << edge), masks] = 1.
        flips.append(np.kron(x, ident4))
        transfer = np.zeros((4, 4))
        transfer[u, v] = transfer[v, u] = 1.
        current = np.zeros((4, 4), dtype=complex)
        current[v, u], current[u, v] = 1j, -1j
        hop.append(np.kron(np.diag(bits[:, edge]), transfer))
        carrier_current.append(PARAMETERS['t_hop'] * np.kron(np.diag(bits[:, edge]), current))
    hv = []
    for v in range(4):
        local = np.diag(np.repeat(PARAMETERS['U_d'] * (deg[:, v]-PARAMETERS['d_star'])**2, 4))
        local += PARAMETERS['epsilon_psi'] * p[v]
        local += RECORD_PARAMETERS['epsilon_r'] * record_occupation * np.eye(64)
        for edge, ends in enumerate(edges):
            if v in ends:
                local += (PARAMETERS['Delta'] * n[edge] / 2
                          - PARAMETERS['Omega'] * flips[edge] / 4
                          - PARAMETERS['t_hop'] * hop[edge] / 2
                          + PARAMETERS['lambda_J'] * n[edge] @ p[v]
                          - RECORD_PARAMETERS['lambda_R'] * record_occupation * n[edge])
        hv.append(local.astype(complex))
    h = sum(hv)
    row = np.zeros((64, 64), dtype=complex)
    for mask in range(16):
        occupied = [(mask >> edge) & 1 for edge in range(4)]
        degrees = [sum(occupied[e] for e, ends in enumerate(edges) if v in ends) for v in range(4)]
        baseline = PARAMETERS['Delta'] * sum(occupied) + PARAMETERS['U_d'] * sum((d-PARAMETERS['d_star'])**2 for d in degrees)
        baseline += (4*RECORD_PARAMETERS['epsilon_r']*record_occupation
                     -2*RECORD_PARAMETERS['lambda_R']*record_occupation*sum(occupied))
        for v in range(4):
            index = 4*mask+v
            row[index, index] = baseline + PARAMETERS['epsilon_psi'] + PARAMETERS['lambda_J'] * degrees[v]
            for edge, (left, right) in enumerate(edges):
                row[index, 4*(mask ^ (1 << edge))+v] -= PARAMETERS['Omega']/2
                if occupied[edge] and v in (left, right):
                    other = right if v == left else left
                    row[index, 4*mask+other] -= PARAMETERS['t_hop']
    return h, row, hv, n, p, carrier_current, edges


def taylor_unitary(h, age, center, radius):
    """Independent shifted/scaled Taylor plus squaring; tail excludes roundoff."""
    if age == 0:
        return np.eye(len(h), dtype=complex), dict(squarings=0, terms=0, tail=0.)
    norm = abs(age)*radius
    power = max(0, math.ceil(math.log2(norm/CONFIG['taylor_scaled_norm']))) if norm else 0
    a = -1j*age*(h-center*np.eye(len(h))) / 2**power
    x = norm/2**power
    result = np.eye(len(h), dtype=complex)
    term = result.copy()
    for order in range(1, CONFIG['taylor_max_terms']+1):
        term = term @ a / order
        result += term
        tail = math.exp(x+(order+1)*math.log(x)-math.lgamma(order+2)) if x else 0.
        if tail < CONFIG['taylor_local_tail']:
            break
    else:
        raise ArithmeticError('Taylor guard reached')
    for _ in range(power):
        result = result @ result
    result *= np.exp(-1j*center*age)
    return result, dict(squarings=power, terms=order,
                        tail=math.expm1(2**power*math.log1p(tail)))


def time_integral(z, duration):
    return duration*np.sinc(z*duration/(2*np.pi))*np.exp(.5j*z*duration)


def run_sector(record_occupation, old):
    started = time.perf_counter()
    maxima, counts, failures = {}, {}, []

    def check(name, actual, expected=0., tol=None, tag=''):
        err = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        limit = CONFIG['operator_tolerance'] if tol is None else tol
        maxima[name] = max(maxima.get(name, 0.), err)
        counts[name] = counts.get(name, 0)+1
        if not math.isfinite(err) or err > limit:
            failures.append(dict(check=name, tag=tag, error=err, tolerance=limit))

    def gram_control(name, matrix, tag=''):
        check(name+'_Hermitian', matrix, matrix.conj().T, CONFIG['state_tolerance'], tag)
        eig = np.linalg.eigvalsh((matrix+matrix.conj().T)/2)
        scale = max(1., float(np.trace(matrix).real))
        check(name+'_PSD', max(0., -float(eig[0]))/scale, tol=CONFIG['psd_scaled_tolerance'], tag=tag)
        schwarz = abs(matrix)**2 - np.outer(np.diag(matrix).real, np.diag(matrix).real)
        check(name+'_Schwarz', max(0., float(np.max(schwarz)))/scale**2,
              tol=CONFIG['psd_scaled_tolerance'], tag=tag)
        return dict(eigenvalues=eig.tolist(), trace_scale=scale,
                    negative_eigenvalue_absolute=max(0., -float(eig[0])))

    h, row, hv, incidence, population, ccurrent, edges = operators(record_occupation)
    identity = np.eye(64)
    check('independent_full_operator', h, row)
    check('Hamiltonian_Hermitian', h, h.conj().T)
    check('node_partition', sum(hv), h)
    blank_h = operators(0)[0]
    check('full_record_storage_feedback', h-blank_h,
          record_occupation*(4*RECORD_PARAMETERS['epsilon_r']*identity
                             -2*RECORD_PARAMETERS['lambda_R']*sum(incidence)))
    pairs = [(u, v) for u in range(4) for v in range(u+1, 4)]
    currents = [1j*comm(hv[u], hv[v])/PARAMETERS['hbar'] for u, v in pairs]
    incidence_matrix = np.zeros((4, 6))
    for j, (u, v) in enumerate(pairs):
        incidence_matrix[u, j], incidence_matrix[v, j] = -1., 1.
        check('current_antisymmetry', currents[j], -1j*comm(hv[v], hv[u])/PARAMETERS['hbar'], tag=str((u, v)))
        check('current_Hermitian', currents[j], currents[j].conj().T, tag=str((u, v)))
    derivatives = [1j*comm(h, local)/PARAMETERS['hbar'] for local in hv]
    for v in range(4):
        check('full_current_continuity', derivatives[v], sum(incidence_matrix[v, j]*currents[j] for j in range(6)), tag=str(v))
    check('total_energy_derivative', sum(derivatives))
    patch = hv[0]+hv[1]
    patchdot = derivatives[0]+derivatives[1]
    check('patch_crossing_current', patchdot, -sum(currents[j] for j, (u, v) in enumerate(pairs) if u < 2 <= v))
    for v in range(4):
        check('carrier_continuity', 1j*comm(h, population[v]),
              sum((1 if v == b else -1 if v == a else 0)*ccurrent[e] for e, (a, b) in enumerate(edges)))
    observable = hv+currents
    incidence_moment = [comm(n, comm(h, n)) for n in incidence]
    labels = ['energy_'+name for name in CONFIG['node_labels']]+[f'J_{u}_to_{v}' for u, v in pairs]
    values, vectors = np.linalg.eigh(h)
    check('eigensystem_residual', h @ vectors, vectors*values, CONFIG['state_tolerance'])
    check('eigensystem_unitarity', vectors.conj().T @ vectors, identity)
    groups = []
    for j, energy in enumerate(values):
        if not groups or abs(energy-values[groups[-1][0]]) > CONFIG['energy_group_tolerance']:
            groups.append([j])
        else:
            groups[-1].append(j)
    energies = np.array([np.mean(values[g]) for g in groups])
    for e, group in zip(energies, groups):
        check('group_energy_resolution', values[group], e, CONFIG['energy_group_tolerance'])
    oe = np.array([vectors.conj().T @ o @ vectors for o in observable])
    ne = np.array([vectors.conj().T @ n @ vectors for n in incidence])
    diag = np.diag(h).real
    row_radius = np.sum(abs(h), axis=1)-abs(np.diag(h))
    lower, upper = float(np.min(diag-row_radius)), float(np.max(diag+row_radius))
    center, radius = (lower+upper)/2, (upper-lower)/2
    check('Gershgorin_enclosure', max(0., lower-values[0], values[-1]-upper))
    old_rows = {(c['graph_type'], c['age']): c['readout'] for c in old['payload']['cases'] if c['n'] == 2}
    initial = np.zeros((64, 2), dtype=complex)
    for j, mask in enumerate(CONFIG['masks']):
        initial[4*mask, j] = 1.
    initial_e = vectors.conj().T @ initial
    holds, methods, two_time, stationary_rows = [], [], [], []
    state_cache = {}
    taylor_cache = {}
    for age in TIMES:
        tay, info = taylor_unitary(row, age, center, radius)
        taylor_cache[age] = tay
        methods.append(dict(age=age, **info))
        primary = vectors @ (np.exp(-1j*values*age)[:, None]*initial_e)
        check('held_two_method_vector', primary, tay @ initial, CONFIG['state_tolerance'], str(age))
        state_cache[age] = primary
    for col, (name, mask) in enumerate(zip(CONFIG['labels'], CONFIG['masks'])):
        psi0, ce = initial[:, col], initial_e[:, col]
        energy0 = float(np.vdot(psi0, h @ psi0).real)
        expected_energy = [21.5, 15.5][col]+record_occupation*(4*RECORD_PARAMETERS['epsilon_r']-2*RECORD_PARAMETERS['lambda_R']*mask.bit_count())
        check('initial_absolute_energy', energy0, expected_energy)
        check('initial_variance', np.vdot(h @ psi0, h @ psi0).real-energy0**2, 1.5)
        columns, derivative_columns, means_all, patchdot_means = [], [], [], []
        for age in TIMES:
            tag = f'{name}:{age}'
            psi = state_cache[age][:, col]
            phase = np.exp(-1j*values*age)
            q = (oe @ (phase*ce)).T*phase.conj()[:, None]
            columns.append(q)
            qt = taylor_cache[age].conj().T @ np.column_stack([o @ (taylor_cache[age] @ psi0) for o in observable])
            check('Heisenberg_vectors_independent', vectors @ q, qt, CONFIG['state_tolerance'], tag)
            derivative_columns.append(vectors.conj().T @ taylor_cache[age].conj().T @
                                      np.column_stack([d @ (taylor_cache[age] @ psi0) for d in derivatives]))
            means = ce.conj() @ q
            check('Hermitian_readout_real', means.imag, tol=CONFIG['state_tolerance'], tag=tag)
            means = means.real
            means_all.append(means)
            dot_means = np.array([np.vdot(psi, d @ psi).real for d in derivatives])
            check('actual_energy_continuity', dot_means, incidence_matrix @ means[4:], CONFIG['state_tolerance'], tag)
            check('actual_energy_conserved', sum(means[:4]), energy0, CONFIG['energy_tolerance'], tag)
            norm = float(np.vdot(psi, psi).real)
            variance = float(np.vdot(h @ psi, h @ psi).real-sum(means[:4])**2)
            check('held_norm', norm, 1., CONFIG['state_tolerance'], tag)
            check('held_variance', variance, 1.5, CONFIG['energy_tolerance'], tag)
            edge_means = np.array([np.vdot(psi, n @ psi).real for n in incidence])
            pop = np.array([np.vdot(psi, p @ psi).real for p in population])
            carrier_flux = np.array([np.vdot(psi, j @ psi).real for j in ccurrent])
            if record_occupation == 0:
                saved = old_rows[(name, age)]
                check('saved_carrier_populations', pop, saved['carrier_populations'], CONFIG['state_tolerance'], tag)
                check('saved_carrier_currents', carrier_flux, [e['current'] for e in saved['edge_currents']], CONFIG['state_tolerance'], tag)
                check('saved_total_energy', sum(means[:4]), saved['energy'], CONFIG['energy_tolerance'], tag)
                check('saved_state_return', np.vdot(psi0, psi), complex(saved['full_state_return_amplitude']['real'], saved['full_state_return_amplitude']['imag']), CONFIG['state_tolerance'], tag)
            patchdot_means.append(float(dot_means[:2].sum()))
            local_gram = q.conj().T @ q
            covariance = local_gram-np.outer(means, means)
            cov_control = gram_control('equal_time_connected', covariance, tag)
            holds.append(dict(preparation=name, age=age, state_vector=cjson(psi), norm=norm,
                              energy=float(sum(means[:4])), initial_energy=energy0, energy_variance=variance,
                              node_energy=means[:4].tolist(), edge_occupation=edge_means.tolist(),
                              incidence_source_moment=[float(np.vdot(psi, m @ psi).real) for m in incidence_moment],
                              record_storage_energy=4*RECORD_PARAMETERS['epsilon_r']*record_occupation*norm,
                              record_feedback_energy=-2*RECORD_PARAMETERS['lambda_R']*record_occupation*float(edge_means.sum()),
                              energy_current=means[4:].tolist(), node_energy_derivative=dot_means.tolist(),
                              left_patch_energy=float(means[:2].sum()), left_patch_flux=float(dot_means[:2].sum()),
                              carrier_population=pop.tolist(), carrier_current=carrier_flux.tolist(),
                              connected_equal_time_covariance=cjson(covariance), covariance_control=cov_control))
        qfull = np.concatenate(columns, axis=1)
        means = np.concatenate(means_all)
        gram = qfull.conj().T @ qfull
        connected = gram-np.outer(means, means)
        corr_control = gram_control('two_time_Gram', gram, name)
        conn_control = gram_control('two_time_connected_Gram', connected, name)
        kernels = []
        for ti, age_t in enumerate(TIMES):
            for si, age_s in enumerate(TIMES[:ti+1]):
                block = gram[ti*10:(ti+1)*10, si*10:(si+1)*10]
                chi = -2*block.imag/PARAMETERS['hbar']
                total_patch = float(chi[:4, :2].sum())
                check('nonstationary_source_work_Ward', total_patch, patchdot_means[si], CONFIG['energy_tolerance'], f'{name}:{ti}:{si}')
                # The time derivative of an energy row equals its exact current divergence.
                dotchi = -2*(derivative_columns[ti].conj().T @ columns[si]).imag/PARAMETERS['hbar']
                check('retarded_continuity_Ward', dotchi, incidence_matrix @ chi[4:], CONFIG['energy_tolerance'], f'{name}:{ti}:{si}')
                check('conserved_energy_covariance', block[:4, :4].sum()-energy0**2,
                      1.5, CONFIG['energy_tolerance'], f'{name}:{ti}:{si}')
                kernels.append(dict(t_index=ti, s_index=si, chi=chi.tolist(),
                                    total_energy_response_to_left_patch=total_patch))
        two_time.append(dict(preparation=name, means=means.tolist(), correlation=cjson(gram),
                             Gram_control=corr_control, connected_Gram_control=conn_control,
                             retarded_blocks=kernels,
                             connected_reconstruction='correlation - outer(conjugate(means),means)',
                             work_scope='Derivative coefficient of a hypothetical -eta*h_left impulse; no source was applied.'))
        pc = np.zeros((64, len(groups)), dtype=complex)
        for a, group in enumerate(groups):
            pc[group, a] = ce[group]
        stationary = pc @ pc.conj().T
        check('dephased_trace', np.trace(stationary), 1.)
        check('dephased_stationarity', values[:, None]*stationary-stationary*values[None, :], tol=CONFIG['state_tolerance'], tag=name)
        for age in CONFIG['probe_ages']:
            phase = np.exp(-1j*values*age)
            check('dephased_age_invariance', phase[:, None]*stationary*phase.conj()[None, :],
                  stationary, CONFIG['state_tolerance'], f'{name}:{age}')
        line_values = np.zeros((len(groups), len(groups), 4))
        elastic = np.zeros(4)
        for edge in range(4):
            transfer = ne[edge] @ pc
            for a in range(len(groups)):
                for b, group in enumerate(groups):
                    line_values[b, a, edge] = float(np.vdot(transfer[group, a], transfer[group, a]).real)
                elastic[edge] += line_values[a, a, edge]
            zeroth = np.trace(stationary @ ne[edge] @ ne[edge]).real
            first = np.trace(stationary @ comm(ne[edge], comm(np.diag(values), ne[edge]))).real
            check('spectral_zeroth_moment', line_values[:, :, edge].sum(), zeroth, CONFIG['state_tolerance'], f'{name}:{edge}')
            gapmatrix = energies[:, None]-energies[None, :]
            check('spectral_first_moment', 2*np.sum(gapmatrix*line_values[:, :, edge]), first, CONFIG['state_tolerance'], f'{name}:{edge}')
        lines = []
        for a in range(len(groups)):
            for b in range(a+1, len(groups)):
                wa, we = line_values[b, a], line_values[a, b]
                beta, labels_line = [], []
                for absorb, emit in zip(wa, we):
                    floor = CONFIG['line_reporting_floor']
                    beta.append(math.log(absorb/emit)/(energies[b]-energies[a]) if min(absorb, emit) > floor else None)
                    labels_line.append('numerically_absent' if max(absorb, emit) <= floor else
                                       'absorption_only_at_resolution' if emit <= floor else
                                       'emission_only_at_resolution' if absorb <= floor else
                                       'balanced_at_resolution' if abs(absorb-emit) <= floor else
                                       'inverted' if emit > absorb else 'positive_ratio')
                lines.append(dict(low=a, high=b, gap=float(energies[b]-energies[a]),
                                  absorption=wa.tolist(), emission=we.tolist(), beta_eff=beta, status=labels_line))
        stationary_rows.append(dict(preparation=name, group_population=np.sum(abs(pc)**2, axis=0).tolist(),
                                    elastic_weight=elastic.tolist(), lines=lines,
                                    scope='Whole-energy-projector dephasing diagnostic only; not a prepared Gibbs state.'))
    # All windows use the inherited probe census. No actual probe or heat source is evolved.
    probes, quad_rows = [], []
    gaps = values[:, None]-values[None, :]
    for duration in CONFIG['durations']:
        quadratures = {}
        for order in CONFIG['quadrature_orders']:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            sample = (nodes+1)*duration/2
            weight = weights*duration/2
            quadratures[order] = (sample, weight, [])
            for age in sample:
                if order == 32:
                    u, info = taylor_unitary(row, float(age), center, radius)
                    bt = np.array([u.conj().T @ n @ u for n in incidence])
                else:
                    phase = np.exp(-1j*values*age)
                    bt = np.array([vectors @ (phase.conj()[:, None]*o*phase[None, :]) @ vectors.conj().T for o in ne])
                quadratures[order][2].append(bt)
        for omega in CONFIG['frequencies']:
            exact = {}
            for sign in CONFIG['frequency_signs']:
                fe = ne*time_integral(gaps+sign*omega, duration)[None, :, :]
                exact[sign] = fe
                f = np.array([vectors @ x @ vectors.conj().T for x in fe])
                for order, (sample, weights, bt) in quadratures.items():
                    quad = sum(w*np.exp(sign*1j*omega*s)*o for s, w, o in zip(sample, weights, bt))
                    err = float(np.max(abs(f-quad)))
                    check('finite_window_independent_integral_'+str(order), err, tol=CONFIG['probe_tolerance'], tag=f'{duration}:{omega}:{sign}')
                    quad_rows.append(dict(duration=duration, omega=omega, sign=sign, order=order, operator_max_error=err,
                                          propagation='shifted Taylor' if order == 32 else 'spectral'))
            check('opposite_sign_adjoint', exact[-1], exact[1].conj().transpose(0, 2, 1), CONFIG['probe_tolerance'])
            for col, name in enumerate(CONFIG['labels']):
                pc = np.zeros((64, len(groups)), dtype=complex)
                for a, group in enumerate(groups):
                    pc[group, a] = initial_e[group, col]
                for age in CONFIG['probe_ages']:
                    ce = np.exp(-1j*values*age)*initial_e[:, col]
                    for sign in CONFIG['frequency_signs']:
                        f = exact[sign]
                        z = (f @ ce).T
                        mean = ce.conj() @ z
                        k = z.conj().T @ z
                        kc = k-np.outer(mean.conj(), mean)
                        projected = f @ pc
                        kd = np.einsum('ega,fga->ef', projected.conj(), projected)
                        check('probe_norm_bound', max(0., float(np.max(np.diag(k).real))-duration**2), tol=CONFIG['probe_tolerance'])
                        control = gram_control('probe_Gram', k, name)
                        conn_control = gram_control('probe_connected_Gram', kc, name)
                        gram_control('probe_dephased_Gram', kd, name)
                        probes.append(dict(preparation=name, age=age, duration=duration, omega=omega, sign=sign,
                                           label='emission' if sign == 1 else 'absorption', mean=cjson(mean),
                                           K=cjson(k), connected_K=cjson(kc), dephased_K=cjson(kd),
                                           coherent_minus_dephased=cjson(k-kd), Gram_control=control,
                                           connected_Gram_control=conn_control))
    check('hold_census', len(holds), 22, 0.)
    check('two_time_block_census', sum(len(row['retarded_blocks']) for row in two_time), 132, 0.)
    check('probe_census', len(probes), 108, 0.)
    check('quadrature_census', len(quad_rows), 36, 0.)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        rss *= 1024
    payload = dict(record_occupation=record_occupation, holds=holds, two_time=two_time,
                   probe_grams=probes, stationary_spectra=stationary_rows,
                   energy_eigenvalues=values.tolist(), energy_groups=[dict(energy=float(e), indices=g) for e, g in zip(energies, groups)],
                   operator_labels=labels, time_flattening='time-major then operator', edges=edges,
                   energy_current_pairs=pairs, energy_current_incidence=incidence_matrix.tolist(),
                   exact_partition='Eq(1), NATIVE_THERMAL_CONNECTIVITY_DISCRIMINATOR_V001.md plus epsilon_r*q per node and -lambda_R*q*n per incident edge.',
                   gershgorin=[lower, upper], Taylor_methods=methods, quadrature_controls=quad_rows,
                   maximum_errors=maxima, check_counts=counts, failures=failures,
                   elapsed_seconds=time.perf_counter()-started, peak_self_rss_bytes=int(rss),
                   preparation_scope='Owned old blank-record preparations' if record_occupation == 0 else 'Prospectively declared uniform occupied-record comparison states; not formed states or a loading trajectory.',
                   status='COMPLETE' if not failures else 'FAILED_CHECKS')
    return payload


def run():
    started = time.perf_counter()
    old, snapshot = inputs()
    if json.loads(FREEZE.read_text()) != snapshot:
        raise RuntimeError('Prospective freeze mismatch')
    sectors = [run_sector(record_occupation, old) for record_occupation in CONFIG['record_occupations']]
    failures = [dict(record_occupation=sector['record_occupation'], **failure)
                for sector in sectors for failure in sector['failures']]
    payload = dict(config=CONFIG, parameters=PARAMETERS, record_parameters=RECORD_PARAMETERS,
                   sectors=sectors, failures=failures, elapsed_seconds=time.perf_counter()-started,
                   record_preparation_energy_difference=[4*RECORD_PARAMETERS['epsilon_r']-2*RECORD_PARAMETERS['lambda_R']*mask.bit_count() for mask in CONFIG['masks']],
                   census=dict(states=4, holds=sum(len(s['holds']) for s in sectors),
                               retarded_blocks=sum(len(r['retarded_blocks']) for s in sectors for r in s['two_time']),
                               probe_grams=sum(len(s['probe_grams']) for s in sectors)),
                   scope='Closed native energy/current/correlation packet with explicit uniform record-loading contrast. No loading trajectory, source pulse, Gibbs reset, Markov law, photon identification, physical seconds, or CMB fit.')
    return dict(status='COMPLETE' if not failures else 'FAILED_CHECKS', payload=payload,
                payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(), freeze_sha256=sha(FREEZE))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('freeze', 'run'):
        raise ValueError('usage: native_thermal_packet_v001.py freeze|run')
    result = inputs()[1] if sys.argv[1] == 'freeze' else run()
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status='ERROR', error_type=type(exc).__name__, error=str(exc))))
        sys.exit(1)
