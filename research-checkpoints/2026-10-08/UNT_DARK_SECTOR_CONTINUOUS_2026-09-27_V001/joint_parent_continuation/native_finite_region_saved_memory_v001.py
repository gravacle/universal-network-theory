"""Exploratory low-rank diagnostics of eight already saved finite-region states.

Explicit --run only. No source imports, propagation, producer invocation, dense
native density matrices, SciPy, or renormalization of evolved state vectors.
The conditional-state divisions below define the stated population-only null;
they do not replace, edit, or normalize a saved physical history.

Two further operator readouts were fixed before this diagnostic was executed:
Bout=||Pdis (-h sum Xe) Pconn psi||^2 and Bin with projectors reversed,
with coherent sums taken before the norm; these are not escape rates, d2C,
or protection certificates. The held A+=|1><0| phase candidate obeys
z'=i(z-.5<d0 A+>); its instantaneous rate is reported only for |z|>1e-10.
This is neither the earlier B0 clock nor an established physical clock;
no trajectory-wide phase claim or normalization by that rate is performed.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import tempfile
import time

HERE = Path(__file__).resolve().parent
INPUT = "native_finite_region_formation_v001_results.json"
OUTPUT = HERE / "native_finite_region_saved_memory_v001_results.json"
PINS = {
    "native_finite_region_formation_v001.py": "8434042c9e74ef42b292436d59d7b3601dda941ef33c20241d382c34c3487056",
    INPUT: "2a52ba3a029c2aa6d6a421d942837cb78035e935c61a0ae60ababe5237862c91",
    "NATIVE_FINITE_REGION_GEOMETRY_RESULT_V001.md": "b3749553fe621a8c0c5f2011675b10e1d501483b0cd15215ab04b6cfaf9a1596",
}
SHAPE, DIM = (512, 6, 2, 2, 2), 24576
EDGES = tuple((i, j+3) for i in range(3) for j in range(3))
TOL, PROBABILITY_GUARD, H_FLIP = 1e-10, 1e-10, 1/3
MAX_SECONDS, MAX_BYTES = 120., 256*1024*1024
THREAD_KEYS = ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
np = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def peak_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == "darwin" else value*1024


def connected(mask):
    reached, pending = {0}, [0]
    while pending:
        vertex = pending.pop()
        for edge, (a, b) in enumerate(EDGES):
            if mask & (1 << edge) and vertex in (a, b):
                other = b if vertex == a else a
                if other not in reached:
                    reached.add(other)
                    pending.append(other)
    return len(reached) == 6


class ResourceStop(Exception):
    pass


def run():
    global np
    started = time.perf_counter()
    if OUTPUT.exists() or OUTPUT.is_symlink():
        raise FileExistsError("Refusing to overwrite "+str(OUTPUT))
    for relative, expected in PINS.items():
        if expected is None:
            raise RuntimeError("Required prospective note hash is not pinned: "+relative)
        if (HERE/relative).is_symlink() or sha(HERE/relative) != expected:
            raise RuntimeError("Pinned input differs: "+relative)
    source_sha = sha(Path(__file__))
    for key in THREAD_KEYS:
        os.environ[key] = "1"
    import numpy as np
    if any(os.environ.get(key) != "1" for key in THREAD_KEYS):
        raise RuntimeError("Single-thread numerical configuration changed")
    checks, states, on_off, preparation_pairs, invariants = [], [], [], [], []
    factors, blocks, summaries = {}, {}, {}
    stopped = None

    def check(name, actual, expected=0.):
        residual = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
        checks.append(dict(name=name, residual=residual if math.isfinite(residual) else None,
            assigned_allowance=TOL, passed=math.isfinite(residual) and residual <= TOL))

    def limit_check():
        elapsed, memory = time.perf_counter()-started, peak_bytes()
        if elapsed > MAX_SECONDS or memory > MAX_BYTES:
            raise ResourceStop("Frozen resource ceiling: seconds="+str(elapsed)+", peak_bytes="+str(memory))

    def spectrum(factor, label):
        gram = factor.conj().T @ factor
        check(label+":gram_Hermitian", gram, gram.conj().T)
        eig = np.linalg.eigvalsh(gram)
        trace = float(np.trace(gram).real)
        purity = float(np.sum(np.abs(gram)**2))
        check(label+":spectrum_trace", eig.sum(), trace)
        check(label+":spectrum_purity", np.dot(eig, eig), purity)
        check(label+":PSD_allowance", max(0., -float(eig.min())))
        return dict(trace=trace, purity=purity, gram_eigenvalues=eig.tolist(),
            additional_exact_zero_eigenvalues=factor.shape[0]-4)

    def distance(left, right, label):
        stacked = np.concatenate((left, right), axis=1)
        q, rr = np.linalg.qr(stacked, mode="reduced")
        check(label+":QR_reconstruction", q @ rr, stacked)
        check(label+":QR_orthogonality", q.conj().T @ q, np.eye(8))
        signs = np.array([1.]*4+[-1.]*4)
        small = (rr*signs[None, :]) @ rr.conj().T
        check(label+":reduced_Hermitian", small, small.conj().T)
        eig = np.linalg.eigvalsh(small)
        lt, rt = float(np.vdot(left, left).real), float(np.vdot(right, right).real)
        value = float(np.abs(eig).sum()/2)
        check(label+":difference_trace", eig.sum(), lt-rt)
        check(label+":trace_norm_lower_bound", max(0., abs(lt-rt)/2-value))
        check(label+":trace_norm_upper_bound", max(0., value-(lt+rt)/2))
        return dict(half_trace_norm=value, left_trace=lt, right_trace=rt,
            reduced_difference_eigenvalues=eig.tolist(),
            distance_to_unit_trace_interpretation_bound=(abs(lt-1)+abs(rt-1))/2)

    masks = np.arange(512)
    conn = np.array([connected(mask) for mask in range(512)])
    conn5 = conn & np.array([mask.bit_count() == 5 for mask in range(512)])
    d0 = np.array([sum(bool(mask & (1 << edge)) for edge in range(3)) for mask in range(512)])

    def complex_parts(value):
        return dict(real=float(value.real), imag=float(value.imag))

    def boundary_activity(psi, current, label):
        c = conn.reshape(512, 1, 1, 1, 1)
        outgoing, incoming, cut_amplitude = np.zeros_like(psi), np.zeros_like(psi), 0j
        for edge in range(9):
            flipped = masks ^ (1 << edge)
            cflip = conn[flipped].reshape(512, 1, 1, 1, 1)
            outgoing -= H_FLIP*(~c)*cflip*psi[flipped]
            incoming -= H_FLIP*c*(~cflip)*psi[flipped]
            cut_amplitude += np.vdot(c*psi, (~cflip)*psi[flipped])
        cut_current = float(-2*H_FLIP*cut_amplitude.imag)
        check(label+":current_cut_identity", current, cut_current)
        return dict(outward_coherent_activity=float(np.vdot(outgoing, outgoing).real),
            inward_coherent_activity=float(np.vdot(incoming, incoming).real),
            cut_amplitude=complex_parts(cut_amplitude), cut_current=cut_current,
            not_escape_rates_or_actual_second_derivative=True)

    def record_phase(psi, original_row, label):
        coherence_terms = psi[:, :, 1, :, :].conj()*psi[:, :, 0, :, :]
        z = coherence_terms.sum()
        zd = (d0[:, None, None, None]*coherence_terms).sum()
        derivative = 1j*(z-.5*zd)
        direct_derivative = (1j*(1-.5*d0)[:, None, None, None]*coherence_terms).sum()
        degree = float(np.sum(d0[:, None, None, None, None]*np.abs(psi)**2))
        check(label+":saved_record_coherence", z,
            complex(original_row["record_coherence"]["real"], original_row["record_coherence"]["imag"]))
        check(label+":phase_derivative_identity", derivative, direct_derivative)
        defined = abs(z) > PROBABILITY_GUARD
        rate = float((derivative/z).imag) if defined else None
        naive = 1-.5*degree
        correction = float(-.5*((zd-degree*z)/z).real) if defined else None
        if defined:
            check(label+":phase_rate_decomposition", rate, naive+correction)
        return dict(z=complex_parts(z), degree_weighted_z=complex_parts(zd),
            dz_dx=complex_parts(derivative), coherence_magnitude=float(abs(z)),
            raw_degree_expectation=degree, naive_degree_rate=naive,
            instantaneous_Aplus_phase_rate=rate, covariance_correction=correction,
            undefined_reason=None if defined else "Coherence magnitude is not above the fixed guard",
            physical_clock_established=False, full_hold_monotonicity_established=False)

    def observables(tensor, label):
        # First axis is graph; all other indices are spectators for these readouts.
        shape = (512,)+(1,)*(tensor.ndim-1)
        graph_weight = np.sum(np.abs(tensor)**2, axis=tuple(range(1, tensor.ndim)))
        commutator_expectation, xp_expectation = 0j, 0j
        for edge in range(9):
            flipped = masks ^ (1 << edge)
            commutator_expectation += np.vdot(tensor,
                (conn[flipped].astype(float)-conn.astype(float)).reshape(shape)*tensor[flipped])
            xp_expectation += np.vdot(tensor, conn[flipped].reshape(shape)*tensor[flipped])
        derivative = -1j*H_FLIP*commutator_expectation
        check(label+":current_real", derivative.imag)
        check(label+":current_flux_identity", derivative.real, 2*H_FLIP*xp_expectation.imag)
        return dict(probability=float(graph_weight.sum()),
            connected_joint=float(graph_weight[conn].sum()),
            connected_and_five_edges_joint=float(graph_weight[conn5].sum()),
            connected_current_joint=float(derivative.real))

    try:
        payload = json.loads((HERE/INPUT).read_text())
        if payload["status"] != "COMPLETE" or payload["failures"]:
            raise ValueError("Source history run is not complete with all arithmetic checks passed")
        if payload["source_sha256"] != PINS["native_finite_region_formation_v001.py"]:
            raise ValueError("Result producer identity mismatch")
        if payload["complete_state_shape"] != list(SHAPE):
            raise ValueError("Unexpected source tensor ordering")
        if len(payload["histories"]) != 4:
            raise ValueError("Expected exactly four complete histories")
        for history in payload["histories"]:
            graph, coupling = history["initial_graph_mask"], history["fragment_coupling"]
            if graph not in (115, 283) or coupling not in (0., 1.) or history["status"] != "COMPLETE":
                raise ValueError("Unexpected or incomplete history")
            if sorted(s["time"] for s in history["saved_states"]) != [2., 4.]:
                raise ValueError("Exactly the two declared saved ages are required")
            for saved in history["saved_states"]:
                age = saved["time"]
                key, label = (graph, coupling, age), history["id"]+":x="+str(age)
                expected_side = "after" if age == 2. else "mesh"
                if key in factors or saved["shape"] != list(SHAPE) or saved["stage"] != "hold" or saved["boundary_side"] != expected_side:
                    raise ValueError("Duplicate or mislabelled saved state")
                psi = (np.array(saved["real"])+1j*np.array(saved["imag"])).reshape(SHAPE)
                if not np.all(np.isfinite(psi)):
                    raise ValueError("Nonfinite saved state")
                native = psi.reshape(6144, 4)
                factors[key] = native
                spectral = spectrum(native, label+":native")
                full = observables(psi, label+":full")
                check(label+":native_trace", spectral["trace"], full["probability"])
                rows = [row for row in history["rows"] if row["time"] == age and row["boundary_side"] == expected_side]
                if len(rows) != 1:
                    raise ValueError("Saved vector has no unique original observation")
                row = rows[0]
                weights = np.abs(psi)**2
                check(label+":saved_norm", full["probability"], row["norm"])
                check(label+":unit_norm_drift", full["probability"], 1.)
                check(label+":saved_connected", full["connected_joint"], row["connected_probability"])
                check(label+":saved_connected_M5", full["connected_and_five_edges_joint"], row["connected_and_five_edges_probability"])
                check(label+":saved_carrier", weights.sum(axis=(0, 2, 3, 4)), row["carrier_probabilities"])
                fragment_q = [float(weights[:, :, :, 1, :].sum()), float(weights[:, :, :, :, 1].sum())]
                check(label+":saved_fragments", fragment_q, [row["fragment1_occupation"], row["fragment2_occupation"]])
                record_rows = []
                for record in (0, 1):
                    block = psi[:, :, record, :, :].reshape(3072, 4)
                    blocks[key+(record,)] = block
                    block_spectrum = spectrum(block, label+":r="+str(record))
                    obs = observables(psi[:, :, record, :, :], label+":r="+str(record))
                    probability = obs["probability"]
                    check(label+":block_trace:"+str(record), block_spectrum["trace"], probability)
                    conditional = {field: obs[field]/probability for field in
                        ("connected_joint", "connected_and_five_edges_joint", "connected_current_joint")} if probability > PROBABILITY_GUARD else None
                    record_rows.append(dict(record=record, **obs, spectrum=block_spectrum,
                        conditional=conditional,
                        conditional_undefined_reason=None if conditional is not None else "Record probability is not above the fixed guard"))
                check(label+":record_occupation", record_rows[1]["probability"], row["record_occupation"])
                for field in ("probability", "connected_joint", "connected_and_five_edges_joint", "connected_current_joint"):
                    check(label+":block_sum:"+field, sum(r[field] for r in record_rows), full[field])
                if coupling == 0:
                    check(label+":no_fragment_coupling_pure_native", spectral["purity"], spectral["trace"]**2)
                summary = dict(history_id=history["id"], initial_graph_mask=graph, fragment_coupling=coupling,
                    time=age, boundary_side=expected_side, native_spectrum=spectral,
                    norm_drift=full["probability"]-1., **full, record_blocks=record_rows,
                    topology_boundary_activity=boundary_activity(psi, full["connected_current_joint"], label),
                    held_record_phase_candidate=record_phase(psi, row, label),
                    original_energy=dict(native=row["native_energy"], fragments=row["fragment_energy"],
                        complete=row["complete_energy"], accumulated_switch_work=row["accumulated_switch_work"]))
                states.append(summary)
                summaries[key] = summary
                limit_check()
        del payload, psi, weights
        check("exact_saved_state_count", len(factors), 8)
        for graph in (115, 283):
            for age in (2., 4.):
                kon, koff = (graph, 1., age), (graph, 0., age)
                label = "on_off:"+str(graph)+":x="+str(age)
                full_distance = distance(factors[kon], factors[koff], label+":native")
                record_distances, predictions = [], {field: 0. for field in
                    ("connected_joint", "connected_and_five_edges_joint", "connected_current_joint")}
                all_defined = True
                bound = 0.
                for record in (0, 1):
                    ron, roff = summaries[kon]["record_blocks"][record], summaries[koff]["record_blocks"][record]
                    pon, poff = ron["probability"], roff["probability"]
                    defined = pon > PROBABILITY_GUARD and poff > PROBABILITY_GUARD
                    conditional_distance = None
                    if defined:
                        conditional_distance = distance(blocks[kon+(record,)]/math.sqrt(pon),
                            blocks[koff+(record,)]/math.sqrt(poff), label+":conditional_r="+str(record))
                        check(label+":conditional_trace:"+str(record),
                            [conditional_distance["left_trace"], conditional_distance["right_trace"]], [1., 1.])
                        bound += pon*conditional_distance["half_trace_norm"]
                        for field in predictions:
                            predictions[field] += pon*roff[field]/poff
                    else:
                        all_defined = False
                    record_distances.append(dict(record=record, on_probability=pon, off_probability=poff,
                        conditional_distance=conditional_distance,
                        undefined_reason=None if defined else "At least one record probability is not above the fixed guard"))
                residuals = {field: summaries[kon][field]-predictions[field] for field in predictions} if all_defined else None
                if all_defined:
                    for field in ("connected_joint", "connected_and_five_edges_joint"):
                        check(label+":projector_distance_bound:"+field, max(0., abs(residuals[field])-bound))
                on_off.append(dict(initial_graph_mask=graph, time=age, native_distance=full_distance,
                    record_conditional_distances=record_distances,
                    reweighted_off_prediction=predictions if all_defined else None,
                    on_minus_population_only_null=residuals,
                    weighted_conditional_distance_bound=bound if all_defined else None,
                    null_is_a_scientific_hypothesis_not_an_arithmetic_pass_requirement=True))
                limit_check()
        for coupling in (0., 1.):
            for age in (2., 4.):
                pair = distance(factors[(115, coupling, age)], factors[(283, coupling, age)],
                    "different_preparations:lambda="+str(coupling)+":x="+str(age))
                preparation_pairs.append(dict(fragment_coupling=coupling, time=age, native_distance=pair))
                limit_check()
        for graph in (115, 283):
            for coupling in (0., 1.):
                early, late = summaries[(graph, coupling, 2.)], summaries[(graph, coupling, 4.)]
                label = "hold:"+str(graph)+":lambda="+str(coupling)
                for field in ("trace", "purity", "gram_eigenvalues"):
                    check(label+":native_"+field, late["native_spectrum"][field], early["native_spectrum"][field])
                for record in (0, 1):
                    for field in ("trace", "purity", "gram_eigenvalues"):
                        check(label+":r="+str(record)+":"+field,
                            late["record_blocks"][record]["spectrum"][field],
                            early["record_blocks"][record]["spectrum"][field])
                spectrum_change = np.array(late["native_spectrum"]["gram_eigenvalues"])-early["native_spectrum"]["gram_eigenvalues"]
                invariants.append(dict(initial_graph_mask=graph, fragment_coupling=coupling,
                    native_purity_change=late["native_spectrum"]["purity"]-early["native_spectrum"]["purity"],
                    native_spectrum_max_change=float(np.max(np.abs(spectrum_change))),
                    connected_probability_change=late["connected_joint"]-early["connected_joint"]))
            early, late = [row for row in on_off if row["initial_graph_mask"] == graph]
            check("hold:on_off_distance:"+str(graph), late["native_distance"]["half_trace_norm"], early["native_distance"]["half_trace_norm"])
            for record in (0, 1):
                e, l = early["record_conditional_distances"][record]["conditional_distance"], late["record_conditional_distances"][record]["conditional_distance"]
                if e is not None and l is not None:
                    check("hold:conditional_distance:"+str(graph)+":"+str(record), l["half_trace_norm"], e["half_trace_norm"])
        for coupling in (0., 1.):
            early, late = [row for row in preparation_pairs if row["fragment_coupling"] == coupling]
            check("hold:preparation_distance:"+str(coupling), late["native_distance"]["half_trace_norm"], early["native_distance"]["half_trace_norm"])
        limit_check()
    except ResourceStop as error:
        stopped = str(error)

    for relative, expected in PINS.items():
        if sha(HERE/relative) != expected:
            raise RuntimeError("Pinned input changed during diagnostic: "+relative)
    if sha(Path(__file__)) != source_sha:
        raise RuntimeError("Diagnostic source changed during run")
    failures = [entry for entry in checks if not entry["passed"]]
    status = "STOPPED_RESOURCE_CEILING" if stopped else ("COMPLETE" if not failures else "FAILED_ARITHMETIC_CHECKS")
    result = dict(status=status, source_sha256=source_sha, input_sha256=PINS,
        saved_state_diagnostics=states, on_off_comparisons=on_off,
        different_preparation_comparisons=preparation_pairs, hold_invariants=invariants,
        checks=checks, failures=failures, check_counts=dict(total=len(checks), passed=len(checks)-len(failures)),
        method=dict(native_factor_shape=[6144, 4], record_block_factor_shape=[3072, 4],
            maximum_reduced_difference_shape=[8, 8], no_dense_native_density_matrix=True,
            eigenvalues_not_clipped=True, assigned_arithmetic_allowance=TOL,
            conditional_probability_guard=PROBABILITY_GUARD, roundoff_certified=False,
            current_definition="d<Pconn>/dx=-i h <[sum_e X_e,Pconn]>, x=tau/hbar, h=1/3",
            population_only_null="rho_on,r=(p_on,r/p_off,r) rho_off,r for both record blocks",
            null_does_not_constrain_cross_record_coherence=True,
            conditional_projector_bound="|C_on-sum_r p_on,r C_off|r| <= sum_r p_on,r D(rho_on|r,rho_off|r)",
            hold_invariance_reason="Hhold=Hnative tensor Ifragments+I tensor Hfragments and [Hnative,Qr]=0; same Hnative for both lambda preparations",
            state_renormalization=False, conditional_division_only_for_defined_conditional_states=True),
        qualifications=dict(exploratory_diagnostic_of_already_known_histories=True,
            preparation_graphs_supplied_not_natively_formed=True, no_evolution_or_new_work=True,
            fragment_storage_and_preparation_work_remain_in_original_ledger=True,
            partial_trace_is_diagnostic_not_a_physical_reset=True,
            raw_half_trace_norm_is_operational_trace_distance_only_for_unit_trace_states=True,
            normalization_interpretation_error_bound="Difference from unit-trace conventional D is at most (|tr_left-1|+|tr_right-1|)/2, without replacing input states",
            no_physical_clock_metric_gravity_or_thermal_bath_claim=True,
            population_only_null_failure_is_not_numerical_failure=True),
        resource_stop=stopped, resource_limits=dict(seconds=MAX_SECONDS, peak_rss_bytes=MAX_BYTES),
        threading=dict(configured={key: os.environ[key] for key in THREAD_KEYS},
            set_before_numpy_import=True, actual_native_thread_count_measured=False),
        runtime=dict(wall_seconds=time.perf_counter()-started, peak_rss_bytes=peak_bytes()))
    data = (json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()
    elapsed, memory = time.perf_counter()-started, peak_bytes()
    if not stopped and (elapsed > MAX_SECONDS or memory > MAX_BYTES):
        stopped = "Resource ceiling reached during result serialization"
        result["resource_stop"], result["status"], status = stopped, "STOPPED_RESOURCE_CEILING", "STOPPED_RESOURCE_CEILING"
    result["runtime"] = dict(wall_seconds=elapsed, peak_rss_bytes=memory)
    data = (json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=HERE, prefix=OUTPUT.name+".partial.", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, OUTPUT)
    finally:
        if temporary is not None:
            temporary.unlink()
    result_sha = hashlib.sha256(data).hexdigest()
    if sha(OUTPUT) != result_sha:
        raise RuntimeError("Published result hash differs")
    print(json.dumps(dict(status=status, path=str(OUTPUT), sha256=result_sha,
        source_sha256=source_sha, bytes=len(data), check_counts=result["check_counts"],
        resource_stop=stopped, runtime=result["runtime"]), separators=(",", ":"), allow_nan=False))
    return 2 if stopped else (0 if not failures else 1)


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; saved-state diagnostic only")
    try:
        code = run()
    except Exception as error:
        print(json.dumps(dict(status="ERROR", error_type=type(error).__name__, error=str(error))))
        code = 1
    raise SystemExit(code)
