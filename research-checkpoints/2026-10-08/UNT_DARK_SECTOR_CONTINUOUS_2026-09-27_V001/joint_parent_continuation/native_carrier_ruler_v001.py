"""Native one-carrier subdivision census: explicit freeze/run, inert on import."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent.resolve()
FREEZE = HERE / "NATIVE_CARRIER_RULER_V001_FROZEN.json"
TIMES = (0., 1/32, 1/16, 1/8, 1/4, 1/2, 1., math.pi/2, 2., math.pi, 4.)
PARAMETERS = dict(hbar=1., Omega=1., U_d=1., d_star=1., Delta=4.,
                  epsilon_psi=1., t_hop=.5, lambda_J=.25)
CONFIG = dict(times=TIMES, sizes=(2, 3), graph_types=("cycle", "tree"),
              masks={"2": (15, 11), "3": (350, 342)},
              initial_vertex=0, reader="old R0", content=0,
              copying_couplings=0., chebyshev_tail=1e-18,
              taylor_substep_tail=1e-19, taylor_max_norm=.75,
              max_chebyshev_degree=4096, max_taylor_terms=256,
              operator_tolerance=2e-11, vector_tolerance=2e-9,
              energy_tolerance=2e-8)
SOURCES = (
    "native_carrier_ruler_v001.py",
    "NATIVE_CARRIER_RULER_NUMERICAL_PROTOCOL_V001.md",
    "NATIVE_CARRIER_RULER_PATHWAY_V001.md",
    "NATIVE_CARRIER_RULER_REVIEW_V001.md",
    "../recovered_sources/BS_MICRO_ACTION.md",
    "CONNECTED_SUBDIVISION_GROWTH_CANDIDATE_V001.md",
    "CONNECTED_SUBDIVISION_CANDIDATE_REVIEW_V001.md",
)
APPROVED_NOTE_SHA = "4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8"
APPROVED_REVIEW_SHA = "516f810a366fe9f1a381c0a74fc7bec51f74b4f40f5aeeb29c32c33b4ebd6fad"
APPROVED_BS_SHA = "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def snapshot():
    files = {}
    for name in SOURCES:
        path = (HERE/name).resolve()
        path.relative_to(PROJECT)  # reject any source route outside the project
        files[name] = digest(path)
    if files["NATIVE_CARRIER_RULER_PATHWAY_V001.md"] != APPROVED_NOTE_SHA:
        raise RuntimeError("Approved analytical note differs")
    if files["NATIVE_CARRIER_RULER_REVIEW_V001.md"] != APPROVED_REVIEW_SHA:
        raise RuntimeError("Approved analytical review differs")
    if files["../recovered_sources/BS_MICRO_ACTION.md"] != APPROVED_BS_SHA:
        raise RuntimeError("Approved native BS action differs")
    return dict(files=files, parameters=PARAMETERS, configuration=CONFIG)


def cjson(value):
    return dict(real=float(np.real(value)), imag=float(np.imag(value)))


def bound_record(log_bound):
    if log_bound == -math.inf:
        return dict(bound=0., log_bound=None, exact_zero=True, underflow=False)
    return dict(bound=math.exp(log_bound) if log_bound > -745 else 0.,
                log_bound=float(log_bound), exact_zero=False, underflow=log_bound <= -745)


def bessel_tail_log(z, first):
    """Geometric envelope on sum_(n>=first)|J_n(z)|, not roundoff."""
    z = abs(float(z))
    if z == 0:
        return -math.inf if first > 0 else 0.
    ratio = z/(2*(first+1))
    if ratio >= 1:
        return math.inf
    return (first*math.log(z/2)-math.lgamma(first+1)
            +z*z/(4*(first+1))-math.log1p(-ratio))


def chebyshev_action(action, initial, center, radius, age):
    if age == 0:
        return initial.copy(), dict(degree=0, fft_samples=0,
                                    truncation=bound_record(-math.inf),
                                    alias=bound_record(-math.inf))
    z = radius*age
    for degree in range(CONFIG["max_chebyshev_degree"]+1):
        log_tail = math.log(2)+bessel_tail_log(z, degree+1)
        if log_tail < math.log(CONFIG["chebyshev_tail"]):
            break
    else:
        raise RuntimeError("Chebyshev degree guard reached")
    samples = 1
    while samples < max(64, 4*(degree+1)):
        samples *= 2
    theta = 2*math.pi*np.arange(samples)/samples
    coefficients = np.fft.fft(np.exp(-1j*z*np.cos(theta)))/samples
    older = initial.copy()
    answer = coefficients[0]*older
    if degree:
        current = (action(older)-center*older)/radius
        answer = answer+2*coefficients[1]*current
        for n in range(2, degree+1):
            newer = 2*(action(current)-center*current)/radius-older
            answer += 2*coefficients[n]*newer
            older, current = current, newer
    log_alias = math.log(4*(degree+1))+bessel_tail_log(z, samples-degree)
    answer *= np.exp(-1j*center*age)
    return answer, dict(degree=degree, fft_samples=samples, z=float(z),
                        truncation=bound_record(log_tail), alias=bound_record(log_alias))


def taylor_action(action, initial, center, radius, age):
    if age == 0:
        return initial.copy(), dict(substeps=0, terms=0, substep_norm=0.,
                                    substep_tail=0., product_tail=0.)
    steps = max(1, math.ceil(abs(age)*radius/CONFIG["taylor_max_norm"]))
    dt = age/steps
    x = radius*abs(dt)
    for terms in range(1, CONFIG["max_taylor_terms"]+1):
        log_tail = ((terms+1)*math.log(x)-math.lgamma(terms+2)
                    -math.log1p(-x/(terms+2)))
        if log_tail < math.log(CONFIG["taylor_substep_tail"]):
            break
    else:
        raise RuntimeError("Taylor term guard reached")
    result = initial.copy()
    for _ in range(steps):
        term = result.copy()
        summed = term.copy()
        for n in range(1, terms+1):
            term = (-1j*dt/n)*(action(term)-center*term)
            summed += term
        result = summed
    result *= np.exp(-1j*center*age)
    epsilon = math.exp(log_tail)
    return result, dict(substeps=steps, terms=terms, substep_norm=float(x),
                        substep_tail=epsilon,
                        product_tail=math.expm1(steps*math.log1p(epsilon)))


class NativeCarrier:
    """Primary tensor/bit action and independently assembled row-sparse action."""
    def __init__(self, n):
        self.n, self.vertices, self.graphs = n, 2*n, 1 << (n*n)
        self.dimension = self.vertices*self.graphs
        self.h = PARAMETERS["Omega"]/n
        self.masks = np.arange(self.graphs, dtype=np.int64)
        self.edges = [(i, n+j) for i in range(n) for j in range(n)]
        self.bits = ((self.masks[:, None] >> np.arange(n*n)) & 1).astype(float)
        self.degrees = np.zeros((self.graphs, self.vertices))
        for edge, (u, v) in enumerate(self.edges):
            self.degrees[:, u] += self.bits[:, edge]
            self.degrees[:, v] += self.bits[:, edge]
        self.inc_diag = (PARAMETERS["Delta"]*np.sum(self.bits, axis=1)
                         +PARAMETERS["U_d"]*np.sum(
                             (self.degrees-PARAMETERS["d_star"])**2, axis=1))
        self.diagonal = (self.inc_diag[:, None]+PARAMETERS["epsilon_psi"]
                         +PARAMETERS["lambda_J"]*self.degrees)
        row_radius = self.h*n*n+abs(PARAMETERS["t_hop"])*self.degrees
        self.lower = float(np.min(self.diagonal-row_radius))
        self.upper = float(np.max(self.diagonal+row_radius))
        self.center = (self.lower+self.upper)/2
        self.radius = (self.upper-self.lower)/2
        self.connected = np.array([self._connected(mask) for mask in range(self.graphs)])
        self.row_columns, self.row_values = self._independent_rows()

    def _connected(self, mask):
        reached, todo = {0}, [0]
        while todo:
            vertex = todo.pop()
            for edge, (u, v) in enumerate(self.edges):
                if mask & (1 << edge) and vertex in (u, v):
                    other = v if vertex == u else u
                    if other not in reached:
                        reached.add(other)
                        todo.append(other)
        return len(reached) == self.vertices

    def action(self, matrix):
        psi = matrix.reshape(self.graphs, self.vertices, -1)
        result = self.diagonal[:, :, None]*psi
        for edge, (u, v) in enumerate(self.edges):
            result -= self.h*psi[self.masks ^ (1 << edge), :, :]
            factor = PARAMETERS["t_hop"]*self.bits[:, edge, None]
            result[:, u, :] -= factor*psi[:, v, :]
            result[:, v, :] -= factor*psi[:, u, :]
        return result.reshape(matrix.shape)

    def _independent_rows(self):
        # Deliberately build by explicit graph/vertex loops without reusing the
        # primary degree, bit or diagonal arrays.  A padded sparse row has at
        # most 1+N²+N nonzero entries, not D columns.
        width = 1+self.n*self.n+self.n
        columns = np.zeros((self.dimension, width), dtype=np.int64)
        values = np.zeros((self.dimension, width), dtype=float)
        for mask in range(self.graphs):
            neighbors = [[] for _ in range(self.vertices)]
            edge_count = 0
            for left in range(self.n):
                for right in range(self.n):
                    edge = left*self.n+right
                    if (mask >> edge) & 1:
                        neighbors[left].append(self.n+right)
                        neighbors[self.n+right].append(left)
                        edge_count += 1
            graph_energy = (PARAMETERS["Delta"]*edge_count+PARAMETERS["U_d"]*sum(
                (len(group)-PARAMETERS["d_star"])**2 for group in neighbors))
            for vertex in range(self.vertices):
                row = mask*self.vertices+vertex
                columns[row, 0] = row
                values[row, 0] = (graph_energy+PARAMETERS["epsilon_psi"]
                                  +PARAMETERS["lambda_J"]*len(neighbors[vertex]))
                for edge in range(self.n*self.n):
                    columns[row, edge+1] = (mask ^ (1 << edge))*self.vertices+vertex
                    values[row, edge+1] = -PARAMETERS["Omega"]/self.n
                for k, other in enumerate(neighbors[vertex], start=1+self.n*self.n):
                    columns[row, k] = mask*self.vertices+other
                    values[row, k] = -PARAMETERS["t_hop"]
        return columns, values

    def sparse_action(self, matrix):
        return np.sum(self.row_values[:, :, None]*matrix[self.row_columns], axis=1)

    def carrier_matrix(self, mask):
        h = np.diag(PARAMETERS["epsilon_psi"]+PARAMETERS["lambda_J"]*self.degrees[mask])
        for edge, (u, v) in enumerate(self.edges):
            if (mask >> edge) & 1:
                h[u, v] = h[v, u] = -PARAMETERS["t_hop"]
        return h

    def observables(self, psi, graph, initial_vector):
        p = psi.reshape(self.graphs, self.vertices)
        probabilities = np.abs(p)**2
        norm = float(np.sum(probabilities))
        hpsi = self.action(psi[:, None])[:, 0]
        energy = float(np.vdot(psi, hpsi).real)
        variance = float(np.vdot(hpsi, hpsi).real-energy*energy)
        currents, flow = [], np.zeros(self.vertices)
        hop_energy, flip_energy = 0., 0.
        for edge, (u, v) in enumerate(self.edges):
            coherence = np.sum(self.bits[:, edge]*np.conj(p[:, u])*p[:, v])
            current = 2*PARAMETERS["t_hop"]*float(coherence.imag)
            currents.append(dict(edge=edge, left=u, right=v, current=current,
                                 mean_nJ=2*float(coherence.imag)))
            flow[u] -= current
            flow[v] += current
            hop_energy -= 2*PARAMETERS["t_hop"]*float(coherence.real)
            flip_energy -= self.h*float(np.vdot(p, p[self.masks ^ (1 << edge)]).real)
        derivative = np.sum(2*np.real(np.conj(p)*(-1j*hpsi.reshape(p.shape))), axis=0)
        populations = np.sum(probabilities, axis=0)
        components = dict(
            incidence_diagonal=float(np.sum(probabilities*self.inc_diag[:, None])),
            incidence_flips=flip_energy, carrier_hopping=hop_energy,
            carrier_onsite=PARAMETERS["epsilon_psi"]*norm,
            current_square=float(PARAMETERS["lambda_J"]*np.sum(probabilities*self.degrees)))
        exact_graph = float(np.sum(probabilities[graph]))
        backbone = (self.masks & graph) == graph
        reader = self.n  # old R0 after the declared embedding
        new_population = float(populations[2]+populations[5]) if self.n == 3 else 0.
        return dict(norm=norm, energy=energy, energy_variance=variance,
                    component_energies=components,
                    component_energy_residual=float(sum(components.values())-energy),
                    carrier_populations=populations.tolist(),
                    population_derivative=derivative.tolist(), current_flow=flow.tolist(),
                    current_continuity_residual=float(np.max(abs(derivative-flow))),
                    edge_currents=currents, source_return=float(populations[0]),
                    reader_arrival=float(populations[reader]), new_carrier_population=new_population,
                    exact_graph_probability=exact_graph,
                    joint_exact_graph_reader_probability=float(probabilities[graph, reader]),
                    backbone_probability=float(np.sum(probabilities[backbone])),
                    connected_probability=float(np.sum(probabilities[self.connected])),
                    full_state_return_amplitude=cjson(np.vdot(initial_vector, psi)))


def run():
    started = time.perf_counter()
    current_inputs = snapshot()
    if encoded(json.loads(FREEZE.read_text())) != encoded(current_inputs):
        raise RuntimeError("Source/configuration freeze differs")
    checks, cases, method_rows, controls = [], [], [], []

    def check(name, actual, expected=0., tolerance=CONFIG["operator_tolerance"]):
        error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=error, tolerance=tolerance,
                           passed=bool(math.isfinite(error) and error <= tolerance)))

    systems = {n: NativeCarrier(n) for n in CONFIG["sizes"]}
    initial_energies = {}
    for n, system in systems.items():
        masks = CONFIG["masks"][str(n)]
        initial = np.zeros((system.dimension, 2), dtype=complex)
        for col, graph in enumerate(masks):
            initial[graph*system.vertices, col] = 1.
        label = np.arange(1, system.dimension+1, dtype=float)
        probes = np.column_stack((np.sin(.37*label)+1j*np.cos(.19*label),
                                  np.cos(.23*label)+1j*np.sin(.41*label),
                                  (-1.)**np.arange(system.dimension))).astype(complex)
        probes /= np.linalg.norm(probes, axis=0)
        check(f'N{n}:independent_operator', system.action(probes), system.sparse_action(probes))
        gram = probes.conj().T@system.action(probes)
        check(f'N{n}:Hermiticity_probes', gram, gram.conj().T)
        check(f'N{n}:initial_operator', system.action(initial), system.sparse_action(initial))
        h1, h2 = system.action(initial), system.action(system.action(initial))
        h3 = system.action(h2)
        initial_energies[n] = [float(np.vdot(initial[:, i], h1[:, i]).real) for i in range(2)]
        check(f'N{n}:initial_energy', initial_energies[n], [21.5, 15.5] if n == 2 else [31.5, 25.5])
        check(f'N{n}:initial_variance', np.sum(abs(h1)**2, axis=0)-np.square(initial_energies[n]), 1.5)
        small_eigen = None
        if n == 2:
            full = system.sparse_action(np.eye(system.dimension, dtype=complex))
            check('N2:dense_Hermitian', full, full.conj().T)
            values, vectors = np.linalg.eigh(full)
            small_eigen = (values, vectors, vectors.conj().T@initial)
        frozen = []
        for col, (name, graph) in enumerate(zip(CONFIG["graph_types"], masks)):
            car = system.carrier_matrix(graph)
            values, vectors = np.linalg.eigh(car)
            frozen.append((values, vectors, vectors[0].conj(), car))
            reader = n
            if n == 3:
                q3 = 2 if name == "cycle" else 1
                expected_h2 = system.h*PARAMETERS["t_hop"]
                expected_h3 = -PARAMETERS["t_hop"]*(q3*PARAMETERS["t_hop"]**2+system.h**2)
                check(f'{name}:H2_flip_hop', h2[(graph ^ 1)*system.vertices+reader, col], expected_h2)
                check(f'{name}:H2_reader_norm', np.sum(abs(h2[:, col].reshape(system.graphs, system.vertices)[:, reader])**2), expected_h2**2)
                check(f'{name}:H3_joint', h3[graph*system.vertices+reader, col], expected_h3)
                check(f'{name}:frozen_H3', np.linalg.matrix_power(car, 3)[reader, 0], -q3*PARAMETERS["t_hop"]**3)
            else:
                check(f'{name}:old_H1_reader', h1[graph*system.vertices+reader, col], -PARAMETERS["t_hop"])
            expected_spectrum = ([.5, 1.5, 1.5, 2.5] if n == 2 else [.5, 1., 1., 2., 2., 2.5])
            if name == "cycle":
                check(f'N{n}:cycle_spectrum', values, expected_spectrum)
            controls.append(dict(n=n, graph_type=name, mask=graph,
                                 frozen_carrier_spectrum=values.tolist(),
                                 incidence_baseline=float(system.inc_diag[graph])))
        for age in TIMES:
            primary, cheb = chebyshev_action(system.action, initial, system.center, system.radius, age)
            independent, taylor = taylor_action(system.sparse_action, initial, system.center, system.radius, age)
            agreement = np.linalg.norm(primary-independent, axis=0)
            check(f'N{n}:dual:{age}', agreement, 0., CONFIG["vector_tolerance"])
            if small_eigen is not None:
                values, vectors, weights = small_eigen
                oracle = vectors@(np.exp(-1j*values*age)[:, None]*weights)
                check(f'N2:eigh:{age}', np.linalg.norm(primary-oracle, axis=0), 0., CONFIG["vector_tolerance"])
            method_rows.append(dict(n=n, age=age, gershgorin=[system.lower, system.upper],
                                    center=system.center, radius=system.radius,
                                    chebyshev=cheb, taylor=taylor,
                                    dual_vector_errors=agreement.tolist()))
            for col, (name, graph) in enumerate(zip(CONFIG["graph_types"], masks)):
                obs = system.observables(primary[:, col], graph, initial[:, col])
                prefix = f'N{n}:{name}:{age}'
                check(prefix+':norm', obs["norm"], 1.)
                check(prefix+':continuity', obs["current_continuity_residual"])
                check(prefix+':energy_components', obs["component_energy_residual"])
                check(prefix+':energy', obs["energy"], initial_energies[n][col], CONFIG["energy_tolerance"])
                check(prefix+':variance', obs["energy_variance"], 1.5, CONFIG["energy_tolerance"])
                graph_bound = min(1., (PARAMETERS["Omega"]*age)**2)
                backbone_bound = min(1., system.h**2*graph.bit_count()*age*age)
                check(prefix+':graph_leakage_bound', max(0., 1-obs["exact_graph_probability"]-graph_bound))
                check(prefix+':backbone_bound', max(0., 1-obs["backbone_probability"]-backbone_bound))
                check(prefix+':connection_contains_backbone', max(0., obs["backbone_probability"]-obs["connected_probability"]))
                values, vectors, weights, car = frozen[col]
                fixed = vectors@(np.exp(-1j*(values+system.inc_diag[graph])*age)*weights)
                fixed_full = np.zeros(system.dimension, dtype=complex)
                fixed_full[graph*system.vertices:(graph+1)*system.vertices] = fixed
                state_error = float(np.linalg.norm(primary[:, col]-fixed_full))
                check(prefix+':fixed_graph_state_bound', max(0., state_error-PARAMETERS["Omega"]*age), 0., CONFIG["vector_tolerance"])
                if name == "cycle":
                    s = PARAMETERS["t_hop"]*age
                    phase = np.exp(-1j*(system.inc_diag[graph]+PARAMETERS["epsilon_psi"]+2*PARAMETERS["lambda_J"])*age)
                    arrival = .5j*math.sin(2*s) if n == 2 else 1j*(math.sin(2*s)-2*math.sin(s))/3
                    returned = math.cos(s)**2 if n == 2 else (math.cos(2*s)+2*math.cos(s))/3
                    check(prefix+':cycle_arrival_oracle', fixed[n], phase*arrival)
                    check(prefix+':cycle_return_oracle', fixed[0], phase*returned)
                frozen_output = dict(carrier_populations=(abs(fixed)**2).tolist(),
                                     source_return=float(abs(fixed[0])**2),
                                     reader_arrival=float(abs(fixed[n])**2),
                                     full_state_return_amplitude=cjson(fixed[0]),
                                     native_state_error=state_error)
                ratios = None
                if n == 3 and age > 0:
                    ratios = dict(arrival_over_tau4=obs["reader_arrival"]/age**4,
                                  joint_arrival_over_tau6=obs["joint_exact_graph_reader_probability"]/age**6,
                                  frozen_arrival_over_tau6=frozen_output["reader_arrival"]/age**6)
                cases.append(dict(n=n, graph_type=name, mask=graph, age=age,
                                  readout=obs, frozen_control=frozen_output,
                                  graph_leakage_upper_bound=graph_bound,
                                  backbone_leakage_upper_bound=backbone_bound,
                                  dual_vector_error=float(agreement[col]),
                                  finite_time_asymptotic_ratios=ratios))
    check('localized_subdivision_work', np.array(initial_energies[3])-initial_energies[2], 10.)
    # Native energy-dependent Schur controls use carrier energy, not a shifted
    # incidence baseline, and keep every old endpoint degree correction.
    schur_rows = []
    target = systems[3]
    old_indices, internal_indices = [0, 1, 3, 4], [5, 2]  # internal order b_R,b_L
    for name, old_graph, new_graph in zip(CONFIG["graph_types"], CONFIG["masks"]["2"], CONFIG["masks"]["3"]):
        old = systems[2].carrier_matrix(old_graph)
        new = target.carrier_matrix(new_graph)
        hb = new[np.ix_(old_indices, old_indices)]
        hi = new[np.ix_(internal_indices, internal_indices)]
        hbi = new[np.ix_(old_indices, internal_indices)]
        removed = np.zeros((4, 4)); removed[0, 2] = removed[2, 0] = PARAMETERS["t_hop"]
        check(name+':Schur_boundary', hb, old+removed)
        check(name+':Schur_internal_poles', np.linalg.eigvalsh(hi), [1., 2.])
        for energy in (-1., 0., 3.):
            z = energy-PARAMETERS["epsilon_psi"]-2*PARAMETERS["lambda_J"]
            hop = PARAMETERS["t_hop"]
            formula = hop**2/(z*z-hop*hop)*np.array([[z, -hop], [-hop, z]])
            sigma = hbi@np.linalg.solve(energy*np.eye(2)-hi, hbi.T)
            expected = np.zeros((4, 4)); expected[np.ix_([0, 2], [0, 2])] = formula
            check(f'{name}:Schur_self_energy:{energy}', sigma, expected)
            full_resolvent = np.linalg.inv(energy*np.eye(6)-new)[np.ix_(old_indices, old_indices)]
            effective_resolvent = np.linalg.inv(energy*np.eye(4)-hb-sigma)
            check(f'{name}:Schur_resolvent:{energy}', full_resolvent, effective_resolvent)
            schur_rows.append(dict(graph_type=name, carrier_energy=energy,
                                   endpoint_self_energy=formula.tolist()))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    payload = dict(checks=checks, cases=cases, method_diagnostics=method_rows,
                   frozen_spectral_controls=controls, schur_controls=schur_rows,
                   initial_energies=initial_energies, parameters=PARAMETERS,
                   configuration=CONFIG, wall_seconds=time.perf_counter()-started,
                   peak_rss_bytes=int(peak),
                   scope="prepared native one-carrier transfer; no physical metric or photon claim")
    result = dict(status="COMPLETE" if all(c["passed"] for c in checks) else "FAILED_CHECKS",
                  freeze_sha256=digest(FREEZE), payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
                  payload=payload)
    return result


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("freeze", "run"):
        raise ValueError("usage: native_carrier_ruler_v001.py freeze|run")
    if sys.argv[1] == "freeze":
        report = snapshot()
    else:
        report = run()
    print(json.dumps(report, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status="ERROR", error_type=type(exc).__name__, error=str(exc))))
        sys.exit(1)
