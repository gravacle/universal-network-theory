"""One declared finite supplied-geometry/copy experiment; explicit --run only.

State (graph,carrier,r,b1,b2)=(512,6,2,2,2), not a density-product closure.
The single active site and piecewise copy ports are declared new boundary
choices, not a projection of uniform active BS copying. Used fragments stay
in the state. No resets, traces, eigensolves, dense H, source imports, SciPy,
new dependencies, state normalization, or physical record-clock assignment.
Every identity/storage energy and both switch works remain in the ledger.
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
OUTPUT = HERE / "native_finite_region_formation_v001_results.json"
PINS = {
    "../recovered_sources/BS_MICRO_ACTION.md": "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
    "NATIVE_FINITE_REGION_GEOMETRY_FORMATION_V001.md": "49db143bee98adc6077640f162401baaca9d8851adc3947bd77fda031aa2a8ee",
}
EDGES = tuple((i, j+3) for i in range(3) for j in range(3))
SHAPE, DIM = (512, 6, 2, 2, 2), 24576
TOL, CENTER, MAX_SCALED, LOCAL_TAIL = 1e-10, 35., .75, 1e-19
RADII = {"pulse1": 37.25, "pulse2": 37.25, "hold": 34.25}
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
        v = pending.pop()
        for e, (a, b) in enumerate(EDGES):
            if mask & (1 << e) and v in (a, b):
                other = b if v == a else a
                if other not in reached:
                    reached.add(other)
                    pending.append(other)
    return len(reached) == 6


def taylor_plan(stage):
    duration, radius = 1/16, RADII[stage]
    steps = math.ceil(duration*radius/MAX_SCALED)
    dt, scaled = duration/steps, radius*duration/steps
    for order in range(1, 257):
        log_tail = ((order+1)*math.log(scaled)-math.lgamma(order+2)
                    -math.log1p(-scaled/(order+2)))
        if log_tail < math.log(LOCAL_TAIL):
            break
    else:
        raise ArithmeticError("Fixed Taylor order guard exhausted")
    tail = math.exp(log_tail)
    return dict(interval=duration, substeps=steps, substep_duration=dt,
                scaled_norm=scaled, terms=order, substep_tail=tail,
                interval_log_product_bound=steps*math.log1p(tail),
                interval_product_bound=math.expm1(steps*math.log1p(tail)))


class ResourceStop(Exception):
    pass


class FiniteRegion:
    def __init__(self):
        self.masks = np.arange(512)
        self.bits = ((self.masks[:, None] >> np.arange(9)) & 1).astype(float)
        self.degrees = np.zeros((512, 6))
        for e, (u, v) in enumerate(EDGES):
            self.degrees[:, u] += self.bits[:, e]
            self.degrees[:, v] += self.bits[:, e]
        index = np.arange(DIM)
        gg, cc, rr, b1, b2 = index//48, (index//8) % 6, (index//4) % 2, (index//2) % 2, index % 2
        self.diagonals = dict(incidence_gap=4*self.bits[gg].sum(axis=1),
            complete_degree_penalty=((self.degrees[gg]-1)**2).sum(axis=1),
            carrier_storage=np.ones(DIM), writer_storage=np.zeros(DIM),
            current_square=.25*self.degrees[gg, cc], record_storage=rr.astype(float),
            record_feedback=-.5*rr*self.degrees[gg, 0],
            fragment1_storage=b1.astype(float), fragment2_storage=b2.astype(float))
        self.diagonal = sum(self.diagonals.values()).reshape(SHAPE)
        self.record_factor = (1+(np.arange(6) == 0).astype(float))[None, :, None, None, None]
        self.record_projector = np.arange(2)[None, None, :, None, None]
        self.is_connected = np.array([connected(mask) for mask in range(512)])
        self.five_links = self.bits.sum(axis=1) == 5
        # Independent scalar/basis sparse rows, never used for propagation.
        self.columns = np.zeros((DIM, 13), dtype=np.int32)
        self.values = np.zeros((DIM, 13))
        for mask in range(512):
            neighbors = [[] for _ in range(6)]
            for i in range(3):
                for j in range(3):
                    if mask & (1 << (3*i+j)):
                        neighbors[i].append(j+3)
                        neighbors[j+3].append(i)
            degree = [len(group) for group in neighbors]
            graph_energy = 4*mask.bit_count()+sum((d-1)**2 for d in degree)
            for c in range(6):
                for local in range(8):
                    r, f1, f2 = (local >> 2) & 1, (local >> 1) & 1, local & 1
                    row = mask*48+c*8+local
                    self.columns[row, 0] = row
                    self.values[row, 0] = graph_energy+1+.25*degree[c]+r-.5*r*degree[0]+f1+f2
                    for e in range(9):
                        self.columns[row, 1+e] = (mask ^ (1 << e))*48+c*8+local
                        self.values[row, 1+e] = -1/3
                    for slot, other in enumerate(neighbors[c], start=10):
                        self.columns[row, slot] = mask*48+other*8+local
                        self.values[row, slot] = -.5
        self.index, self.cc, self.rr = index, cc, rr

    def offdiagonal(self, x):
        y = np.zeros_like(x)
        for e, (u, v) in enumerate(EDGES):
            y -= x[self.masks ^ (1 << e)]/3
            factor = .5*self.bits[:, e, None, None, None]
            y[:, u] -= factor*x[:, v]
            y[:, v] -= factor*x[:, u]
        return y

    def record_copy(self, x):
        return self.record_factor*x[:, :, ::-1, :, :]

    def fragment_copy(self, x, which, coupling):
        if which == 1:
            return coupling*self.record_projector*x[:, :, :, ::-1, :]
        return coupling*self.record_projector*x[:, :, :, :, ::-1]

    def action(self, x, stage, coupling, centered=False):
        y = (self.diagonal-(CENTER if centered else 0))*x+self.offdiagonal(x)
        if stage != "hold":
            y += self.record_copy(x)
            y += self.fragment_copy(x, 1 if stage == "pulse1" else 2, coupling)
        return y

    def independent(self, x, stage, coupling):
        flat = x.ravel()
        out = np.sum(self.values*flat[self.columns], axis=1)
        if stage != "hold":
            out += (1+(self.cc == 0))*flat[self.index ^ 4]
            out += coupling*self.rr*flat[self.index ^ (2 if stage == "pulse1" else 1)]
        return out.reshape(SHAPE)

    def components(self, x):
        flat = x.ravel()
        energy = {key: float(np.vdot(flat, val*flat).real) for key, val in self.diagonals.items()}
        flips, hopping = np.zeros_like(x), np.zeros_like(x)
        for e, (u, v) in enumerate(EDGES):
            flips -= x[self.masks ^ (1 << e)]/3
            factor = .5*self.bits[:, e, None, None, None]
            hopping[:, u] -= factor*x[:, v]
            hopping[:, v] -= factor*x[:, u]
        energy["incidence_flips"] = float(np.vdot(x, flips).real)
        energy["carrier_hopping"] = float(np.vdot(x, hopping).real)
        return energy


def run():
    global np
    started = time.perf_counter()
    if OUTPUT.exists() or OUTPUT.is_symlink():
        raise FileExistsError("Refusing to overwrite "+str(OUTPUT))
    for relative, expected in PINS.items():
        if (HERE/relative).is_symlink() or sha(HERE/relative) != expected:
            raise RuntimeError("Pinned input differs: "+relative)
    source_sha = sha(Path(__file__))
    for key in THREAD_KEYS:
        os.environ[key] = "1"
    import numpy as np
    if any(os.environ.get(key) != "1" for key in THREAD_KEYS):
        raise RuntimeError("Single-thread numerical configuration changed")
    checks, histories, comparisons = [], [], []

    def check(name, a, b=0.):
        residual = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
        checks.append(dict(name=name, residual=residual if math.isfinite(residual) else None,
            assigned_allowance=TOL, passed=math.isfinite(residual) and residual <= TOL))

    def limit_check():
        elapsed, memory = time.perf_counter()-started, peak_bytes()
        if elapsed > MAX_SECONDS or memory > MAX_BYTES:
            raise ResourceStop("Frozen resource ceiling: seconds="+str(elapsed)+", peak_bytes="+str(memory))

    system = FiniteRegion()
    plans = {stage: taylor_plan(stage) for stage in RADII}
    rng = np.random.default_rng(20261003)
    u = (rng.normal(size=SHAPE)+1j*rng.normal(size=SHAPE))
    v = (rng.normal(size=SHAPE)+1j*rng.normal(size=SHAPE))
    u /= np.linalg.norm(u.ravel())
    v /= np.linalg.norm(v.ravel())  # Diagnostic vectors only, never evolved states.
    check("dimension", u.size, DIM)
    check("independent_diagonal", system.diagonal.ravel(), system.values[:, 0])
    check("centered_diagonal_bound", max(0., float(np.max(np.abs(system.diagonal-CENTER)))-29.75))
    for coupling in (0., 1.):
        for stage in RADII:
            label = "source_algebra:"+stage+":lambda="+str(coupling)
            hu, hv = system.action(u, stage, coupling), system.action(v, stage, coupling)
            check(label+":independent_action", hu, system.independent(u, stage, coupling))
            check(label+":hermiticity", np.vdot(u, hv), np.vdot(hu, v))
            check(label+":centering", system.action(u, stage, coupling, True)+CENTER*u, hu)
            parts = system.components(u)
            copies = 0. if stage == "hold" else float(np.vdot(u,
                system.record_copy(u)+system.fragment_copy(u, 1 if stage == "pulse1" else 2, coupling)).real)
            check(label+":component_reconstruction", math.fsum(parts.values())+copies, np.vdot(u, hu).real)
    del u, v, hu, hv
    for mask, expected in ((115, True), (283, False)):
        check("initial_connectivity:"+str(mask), int(system.is_connected[mask]), int(expected))
        check("initial_degrees:"+str(mask), system.degrees[mask], [2, 2, 1, 2, 2, 1])
        check("initial_edge_count:"+str(mask), mask.bit_count(), 5)
        check("single_flip_connectivity_onset:"+str(mask),
            sum(int(system.is_connected[mask ^ (1 << e)])-int(expected) for e in range(9)),
            -5 if expected else 4)

    psi, current, current_time, stage, side, work = None, None, 0., "pulse1", "after", 0.
    log_error, stopped, checkpoint = 0., None, None

    def observe(x, tau, active_stage, boundary_side, coupling, work_sum, conserved):
        tag = current["id"]+":"+str(tau)+":"+boundary_side
        weights = (x.conjugate()*x).real
        graph_weights = weights.sum(axis=(1, 2, 3, 4))
        norm = float(graph_weights.sum())
        carrier = weights.sum(axis=(0, 2, 3, 4))
        record_q = float(weights[:, :, 1, :, :].sum())
        b1 = float(weights[:, :, :, 1, :].sum())
        b2 = float(weights[:, :, :, :, 1].sum())
        coherence = np.vdot(x[:, :, 1, :, :], x[:, :, 0, :, :])
        energies = system.components(x)
        fragment_energy = energies["fragment1_storage"]+energies["fragment2_storage"]
        native_energy = math.fsum(value for key, value in energies.items() if not key.startswith("fragment"))
        vr = float(np.vdot(x, system.record_copy(x)).real)
        vb1 = float(np.vdot(x, system.fragment_copy(x, 1, coupling)).real)
        vb2 = float(np.vdot(x, system.fragment_copy(x, 2, coupling)).real)
        active_copy = 0. if active_stage == "hold" else vr+(vb1 if active_stage == "pulse1" else vb2)
        energy = native_energy+fragment_energy+active_copy
        direct = np.vdot(x, system.action(x, active_stage, coupling))
        check(tag+":norm", norm, 1.)
        check(tag+":one_carrier_sector", carrier.sum(), norm)
        check(tag+":energy_component_reconstruction", energy, direct.real)
        check(tag+":Hermitian_energy", direct.imag)
        check(tag+":inclusive_energy_work", energy, 25.5+work_sum)
        if tau <= 1:
            check(tag+":untouched_fragment2", b2)
        if coupling == 0:
            check(tag+":fragments_off_null", [b1, b2])
        for key, actual in (("b1", b1), ("b2", b2), ("record", record_q)):
            if key in conserved:
                check(tag+":conserved_"+key, actual, conserved[key])
        return dict(time=tau, boundary_side=boundary_side, stage=active_stage,
            norm=norm, connected_probability=float(graph_weights[system.is_connected].sum()),
            connected_and_five_edges_probability=float(graph_weights[system.is_connected & system.five_links].sum()),
            link_count=float(np.dot(graph_weights, system.bits.sum(axis=1))),
            carrier_probabilities=carrier.tolist(), record_occupation=record_q,
            record_coherence=dict(real=float(coherence.real), imag=float(coherence.imag)),
            fragment1_occupation=b1, fragment2_occupation=b2,
            native_energy=native_energy, fragment_energy=fragment_energy, active_copy_energy=active_copy,
            complete_energy=energy, component_energies=energies,
            Vrecord_expectation=vr, Vfragment1_expectation=vb1, Vfragment2_expectation=vb2,
            accumulated_switch_work=work_sum, inclusive_energy_work_residual=energy-25.5-work_sum,
            accumulated_analytic_truncation_bound=math.expm1(log_error),
            actual_elapsed_seconds=time.perf_counter()-started, actual_peak_rss_bytes=peak_bytes())

    try:
        for mask, name in ((115, "connected_path"), (283, "cycle_plus_edge")):
            for coupling in (0., 1.):
                current = dict(id=name+":lambda="+str(int(coupling)), initial_graph_mask=mask,
                    graph_name=name, fragment_coupling=coupling, status="RUNNING", rows=[], switches=[], saved_states=[])
                histories.append(current)
                psi = np.zeros(SHAPE, complex)
                psi[mask, 0, 0, 0, 0] = 1.
                current_time, stage, side, work, log_error = 0., "hold", "before", 0., 0.
                conserved = {}
                hp = system.action(psi, "pulse1", coupling)
                mean = float(np.vdot(psi, hp).real)
                variance = float(np.vdot(hp, hp).real-mean*mean)
                check(current["id"]+":initial_complete_energy", mean, 25.5)
                check(current["id"]+":initial_pulse_variance", variance, 5.5)
                current["initial_pulse_energy"], current["initial_pulse_variance"] = mean, variance
                before = observe(psi, 0., "hold", "before", coupling, work, conserved)
                current["rows"].append(before)
                won = before["Vrecord_expectation"]+before["Vfragment1_expectation"]
                check(current["id"]+":switch_on_mean_work", won)
                work += won
                stage, side = "pulse1", "after"
                after = observe(psi, 0., stage, side, coupling, work, conserved)
                current["rows"].append(after)
                current["switches"].append(dict(time=0., from_stage="hold", to_stage=stage,
                    work=won, before_energy=before["complete_energy"], after_energy=after["complete_energy"]))
                limit_check()
                for mesh in range(1, 65):
                    plan = plans[stage]
                    for _ in range(plan["substeps"]):
                        term, answer = psi.copy(), psi.copy()
                        for order in range(1, plan["terms"]+1):
                            term = (-1j*plan["substep_duration"]/order)*system.action(term, stage, coupling, True)
                            answer += term
                        psi = answer
                    psi *= np.exp(-1j*CENTER/16)
                    log_error += plan["interval_log_product_bound"]
                    current_time, side = mesh/16, "before" if mesh in (16, 32) else "mesh"
                    row = observe(psi, current_time, stage, side, coupling, work, conserved)
                    current["rows"].append(row)
                    if mesh == 64:
                        current["saved_states"].append(dict(time=current_time, stage=stage,
                            boundary_side=side, shape=SHAPE,
                            real=psi.real.ravel().tolist(), imag=psi.imag.ravel().tolist()))
                    limit_check()
                    if mesh in (16, 32):
                        old_stage = stage
                        if mesh == 16:
                            change = row["Vfragment2_expectation"]-row["Vfragment1_expectation"]
                            check(current["id"]+":fresh_fragment2_switch_expectation", row["Vfragment2_expectation"])
                            stage, conserved["b1"] = "pulse2", row["fragment1_occupation"]
                        else:
                            change = -row["Vrecord_expectation"]-row["Vfragment2_expectation"]
                            stage, conserved["b2"], conserved["record"] = "hold", row["fragment2_occupation"], row["record_occupation"]
                        work, side = work+change, "after"
                        after = observe(psi, current_time, stage, side, coupling, work, conserved)
                        current["rows"].append(after)
                        check(current["id"]+":switch_energy_jump:"+str(mesh),
                              after["complete_energy"]-row["complete_energy"], change)
                        current["switches"].append(dict(time=current_time, from_stage=old_stage,
                            to_stage=stage, work=change, before_energy=row["complete_energy"],
                            after_energy=after["complete_energy"]))
                        if mesh == 32:
                            current["saved_states"].append(dict(time=current_time, stage=stage,
                                boundary_side=side, shape=SHAPE,
                                real=psi.real.ravel().tolist(), imag=psi.imag.ravel().tolist()))
                        limit_check()
                current["status"] = "COMPLETE"
                current["final_truncation_bound"] = math.expm1(log_error)
                check(current["id"]+":complete_reporting_rows", len(current["rows"]), 68)
                check(current["id"]+":fixed_saved_state_ages", [s["time"] for s in current["saved_states"]], [2., 4.])
    except ResourceStop as error:
        stopped = str(error)
        if current is not None:
            current["status"] = "RESOURCE_STOP"
            checkpoint = dict(history_id=current["id"], time=current_time, stage=stage,
                boundary_side=side, accumulated_switch_work=work,
                accumulated_log_truncation_bound=log_error, shape=SHAPE,
                conserved_readout_reference=conserved,
                real=psi.real.ravel().tolist(), imag=psi.imag.ravel().tolist())

    fields = ("connected_probability", "connected_and_five_edges_probability", "link_count",
              "record_occupation", "fragment1_occupation", "fragment2_occupation", "native_energy",
              "fragment_energy", "active_copy_energy", "complete_energy", "accumulated_switch_work")
    for mask in (115, 283):
        available = {h["fragment_coupling"]: h for h in histories if h["initial_graph_mask"] == mask}
        if 0. not in available or 1. not in available:
            comparisons.append(dict(initial_graph_mask=mask, status="MISSING_HISTORY", rows=[]))
            continue
        off = {(r["time"], r["boundary_side"]): r for r in available[0.]["rows"]}
        differences = []
        for on in available[1.]["rows"]:
            key = on["time"], on["boundary_side"]
            if key not in off:
                continue
            baseline = off[key]
            delta = {field: on[field]-baseline[field] for field in fields}
            delta["carrier_probabilities"] = [a-b for a, b in zip(on["carrier_probabilities"], baseline["carrier_probabilities"])]
            delta["record_coherence"] = {part: on["record_coherence"][part]-baseline["record_coherence"][part] for part in ("real", "imag")}
            differences.append(dict(time=key[0], boundary_side=key[1], on_minus_off=delta))
        sign_changes = []
        for previous, following in zip(differences, differences[1:]):
            for field in fields:
                a, b = previous["on_minus_off"][field], following["on_minus_off"][field]
                if (a > 0 > b) or (a < 0 < b):
                    sign_changes.append(dict(field=field, from_time=previous["time"],
                        from_side=previous["boundary_side"], to_time=following["time"],
                        to_side=following["boundary_side"], from_value=a, to_value=b))
        complete = all(available[value]["status"] == "COMPLETE" for value in (0., 1.))
        if complete:
            check("full_on_off_mesh:"+str(mask), len(differences), 68)
        comparisons.append(dict(initial_graph_mask=mask, status="COMPLETE" if complete else "PARTIAL",
            rows=differences, raw_floating_sign_changes=sign_changes,
            sign_changes_are_not_roundoff_certified=True,
            final_mesh_difference=differences[-1] if differences else None))

    for relative, expected in PINS.items():
        if sha(HERE/relative) != expected:
            raise RuntimeError("Pinned input changed during run: "+relative)
    if sha(Path(__file__)) != source_sha:
        raise RuntimeError("Worker source changed during run")
    failures = [c for c in checks if not c["passed"]]
    status = "STOPPED_RESOURCE_CEILING" if stopped else ("COMPLETE" if not failures else "FAILED_ARITHMETIC_CHECKS")
    result = dict(status=status, source_sha256=source_sha, input_sha256=PINS,
        complete_state_shape=SHAPE, dimension=DIM, edge_order=EDGES,
        parameters=dict(N=3, Omega=1., h=1/3, Delta=4., U_d=1., d_star=1.,
            epsilon_psi=1., epsilon_r=1., epsilon_w=0., epsilon_b1=1., epsilon_b2=1.,
            t_hop=.5, lambda_J=.25, lambda_R=.5, local_g_wr=1., local_g_psi_r=1.),
        protocol_time="x=tau/hbar", record_coherence_definition="A=|1><0|; sum conj(psi_r1)*psi_r0",
        full_state_saved_ages=(2., 4.),
        histories=histories, comparisons=comparisons, checks=checks, failures=failures,
        check_counts=dict(total=len(checks), passed=len(checks)-len(failures)),
        resource_stop=stopped, checkpoint=checkpoint,
        method=dict(name="Matrix-free centered scaled Taylor", center=CENTER,
            fixed_centered_norm_bounds=RADII, plans=plans, norm_bound_spectral_radius_measured=False,
            bound_proof="Diagonal in [6.5,64.75], hence |diagonal-35|<=29.75; off-diagonal row sums <=4.5 hold and <=7.5 pulse; real Hermiticity gives the stated 2-norm bounds.",
            tail_proof="First omitted exponential term divided by 1-x/(K+2); compose exact-unitary step errors by exp(sum log(1+tail))-1.",
            deterministic_probe_seed=20261003, assigned_arithmetic_allowance=TOL,
            source_algebra_checks_are_finite_probes_not_full_operator_proof=True,
            analytic_truncation_excludes_roundoff=True, roundoff_certified=False, no_state_renormalization=True),
        qualifications=dict(supplied_not_formed_initial_graphs=True,
            site_selective_copy_ports_explicit=True, finite_switched_supply_not_autonomous_bath=True,
            no_fragment_reset_trace_or_postselection=True, switching_work_included=True,
            physical_record_clock_assumed=False, physical_metric_or_gravity_established=False,
            scientific_connectivity_pass_threshold=None, observed_samples_not_continuous_window_certificate=True),
        resource_limits=dict(seconds=MAX_SECONDS, peak_rss_bytes=MAX_BYTES, checked_at_report_mesh=True),
        threading=dict(configured={key: os.environ[key] for key in THREAD_KEYS},
            set_before_numpy_import=True, actual_native_thread_count_measured=False),
        runtime=dict(wall_seconds=time.perf_counter()-started, peak_rss_bytes=peak_bytes()))
    data = (json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()
    serialization_elapsed, serialization_peak = time.perf_counter()-started, peak_bytes()
    result["serialization_resource_observation"] = dict(elapsed_seconds=serialization_elapsed,
        peak_rss_bytes=serialization_peak, first_encoded_bytes=len(data))
    if not stopped and (serialization_elapsed > MAX_SECONDS or serialization_peak > MAX_BYTES):
        stopped = "Resource ceiling reached during result serialization"
        status = "STOPPED_RESOURCE_CEILING"
        result["resource_stop"], result["status"] = stopped, status
    result["runtime"] = dict(wall_seconds=serialization_elapsed, peak_rss_bytes=serialization_peak)
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
        resource_stop=stopped, runtime=result["runtime"],
        histories=[dict(id=h["id"], status=h["status"], rows=len(h["rows"])) for h in histories]),
        separators=(",", ":"), allow_nan=False))
    return 2 if stopped else (0 if not failures else 1)


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; one frozen finite-region experiment")
    try:
        code = run()
    except Exception as error:
        print(json.dumps(dict(status="ERROR", error_type=type(error).__name__, error=str(error))))
        code = 1
    raise SystemExit(code)
