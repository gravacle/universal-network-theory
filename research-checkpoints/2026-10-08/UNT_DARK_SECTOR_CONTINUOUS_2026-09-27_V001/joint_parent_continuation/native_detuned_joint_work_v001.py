"""Frozen K3,3/Q2 experiment: actual record memory and complete cyclic work."""
import os
import sys

sys.dont_write_bytecode = True
for key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "NATIVE_DETUNED_JOINT_WORK_PROTOCOL_V001.md"
PARENT = HERE.parent / "recovered_sources/BS_MICRO_ACTION.md"
OUTPUT = HERE / "NATIVE_DETUNED_JOINT_WORK_V001_RESULT.json"
CHECKPOINT = HERE / "NATIVE_DETUNED_JOINT_WORK_V001_CHECKPOINT.json"
PINS = {PROTOCOL: "adaa07698f920303718d0861316a32d128f4cbd0488efdc37c96ff2c547017dc",
        PARENT: "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec"}
EDGES = [(u, v) for u in range(3) for v in range(3, 6)]
PERIOD = 2 * math.pi / math.sqrt(5)
DELAY = PERIOD / 2
TOL, SIGN_TOL, FD_TOL = 1e-9, 1e-8, 2e-6
TIME_LIMIT, RSS_LIMIT = 180., 512 * 2**20


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss():
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(raw if sys.platform == "darwin" else raw * 1024)


def main():
    if OUTPUT.exists() or CHECKPOINT.exists():
        raise RuntimeError("Evidence or checkpoint already exists; refusing overwrite")
    for path, pin in PINS.items():
        if sha(path) != pin:
            raise RuntimeError(f"Frozen source changed: {path.name}")
    start = time.perf_counter()
    maxima, failures, stages = {}, [], []
    evidence = {path.name: sha(path) for path in (*PINS, Path(__file__))}
    result = dict(status="RUNNING", evidence_hashes=evidence,
                  controls=dict(maxima=maxima, failures=failures))

    def check(name, value, expected=0., tol=TOL):
        err = float(np.max(np.abs(np.asarray(value) - expected)))
        maxima[name] = max(maxima.get(name, 0.), err)
        if not math.isfinite(err) or err > tol:
            failures.append(dict(name=name, error=err, tolerance=tol))

    def stage(name):
        sample = dict(stage=name, seconds=time.perf_counter() - start, peak_rss_bytes=rss())
        stages.append(sample)
        result["resources"] = dict(stages=stages, **sample)
        CHECKPOINT.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
        print(json.dumps(sample), flush=True)
        if sample["seconds"] > TIME_LIMIT or sample["peak_rss_bytes"] > RSS_LIMIT:
            result["status"] = "RESOURCE_STOP"
            OUTPUT.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
            raise SystemExit(2)

    masks = [m for m in range(64) if m.bit_count() == 2]
    ci = {m: k for k, m in enumerate(masks)}
    n, rank = 960, 15
    occ = np.array([[(m >> v) & 1 for m in masks] for v in range(6)], dtype=float)
    pd = np.repeat(occ[0], 64)
    hv = np.zeros((6, n, n))
    record_masks = np.arange(64)
    for v in range(6):
        neighbors = [b if a == v else a for a, b in EDGES if v in (a, b)]
        for k, m in enumerate(masks):
            ids = k * 64 + record_masks
            hv[v, ids, ids] = (10 + 1.75 * occ[v, k]
                - .25 * occ[v, k] * sum(occ[u, k] for u in neighbors)
                - .5 * ((record_masks >> v) & 1))
            hv[v, ids ^ (1 << v), ids] = 1 + occ[v, k]
        for a, b in EDGES:
            if v not in (a, b):
                continue
            for k, m in enumerate(masks):
                if ((m >> a) & 1) != ((m >> b) & 1):
                    row = ci[m ^ (1 << a) ^ (1 << b)] * 64 + record_masks
                    col = k * 64 + record_masks
                    hv[v, row, col] = -.25
    H, F = hv.sum(axis=0), hv[0].copy()
    # Independent direct energy: storage + current-square + records + hopping.
    direct = np.zeros_like(H)
    for k, m in enumerate(masks):
        ids = k * 64 + record_masks
        unequal = sum(((m >> a) & 1) != ((m >> b) & 1) for a, b in EDGES)
        direct[ids, ids] = 62 + .25 * unequal - .5 * np.array([r.bit_count() for r in range(64)])
        for v in range(6):
            direct[ids ^ (1 << v), ids] = 1 + occ[v, k]
        for a, b in EDGES:
            if ((m >> a) & 1) != ((m >> b) & 1):
                direct[ci[m ^ (1 << a) ^ (1 << b)] * 64 + record_masks, ids] = -.5
    check("complete_allocation", H, direct)
    check("H_Hermitian", H, H.T)
    check("F_Hermitian", F, F.T)
    diffp = pd[:, None] - pd[None, :]
    D = -H * diffp**2
    I = -1j * H * diffp
    check("phase_contact", -F * diffp**2, D / 2)
    check("current_contact", -1j * F * diffp, I / 2)
    incident = np.zeros_like(H)
    for k, m in enumerate(masks):
        for a, b in EDGES:
            if 0 in (a, b) and ((m >> a) & 1) != ((m >> b) & 1):
                incident[ci[m ^ (1 << a) ^ (1 << b)] * 64 + record_masks,
                         k * 64 + record_masks] = .5
    check("phase_double_commutator", D, incident)
    A0 = np.zeros((n, rank))
    A0[np.arange(rank) * 64, np.arange(rank)] = 1 / math.sqrt(rank)
    check("initial_rank_factor", A0.T @ A0, np.eye(rank) / rank)
    initial_energy = float(np.sum(A0 * (H @ A0)))
    check("initial_complete_energy", initial_energy, 316 / 5)
    check("initial_local_energy", np.sum(A0 * (F @ A0)), 158 / 15)

    # Sparse row action is used independently of the eigensolver.
    Hc, Fc = H - 62 * np.eye(n), F - 10 * np.eye(n)
    nz = [np.flatnonzero((Hc[row] != 0) | (Fc[row] != 0)) for row in range(n)]
    width = max(map(len, nz))
    rows = np.zeros((n, width), dtype=int)
    hs, fs = np.zeros((n, width)), np.zeros((n, width))
    for row, ids in enumerate(nz):
        rows[row, :len(ids)] = ids
        hs[row, :len(ids)] = Hc[row, ids]
        fs[row, :len(ids)] = Fc[row, ids]
    norm_h = float(np.max(np.sum(np.abs(hs), axis=1)))
    norm_f = float(np.max(np.sum(np.abs(fs), axis=1)))
    check("centered_H_row_bound", max(0., norm_h - 12.5))
    check("sparse_H_action", np.sum(hs[:, :, None] * A0[rows], axis=1) + 62 * A0, H @ A0)
    check("sparse_F_action", np.sum(fs[:, :, None] * A0[rows], axis=1) + 10 * A0, F @ A0)

    def centered_action(y, alpha=0.):
        return np.sum((hs + alpha * fs)[:, :, None] * y[rows], axis=1)

    def h_action(y):
        return centered_action(y) + 62 * y

    def f_action(y):
        return np.sum(fs[:, :, None] * y[rows], axis=1) + 10 * y

    def i_action(y):
        return 1j * (h_action(pd[:, None] * y) - pd[:, None] * h_action(y))

    def d_action(y):
        py = pd[:, None] * y
        return 2 * pd[:, None] * h_action(py) - pd[:, None] * h_action(y) - h_action(py)

    def expect_action(y, action):
        return float(np.vdot(y, action(y)).real)

    def taylor(y, duration, alpha=0.):
        steps = max(1, math.ceil(abs(duration) / .1))
        dt = duration / steps
        scalar = np.exp(-1j * (62 + 10 * alpha) * dt)
        out = y.astype(complex).copy()
        for _ in range(steps):
            term = out.copy()
            total = out.copy()
            for order in range(1, 25):
                term = (-1j * dt / order) * centered_action(term, alpha)
                total += term
            out = scalar * total
        return out

    result["configuration"] = dict(V=6, Q=2, dimension=n, rank=rank, edges=EDGES,
        graph_baseline=60., initial_energy=initial_energy, local_source="h0",
        phase_generator="p0", phase_sign=1, source_off_before_phase=True,
        period=PERIOD, pulse_duration=DELAY, windows=[[0., PERIOD], [PERIOD, 2 * PERIOD]],
        age_step=PERIOD / 128, unique_ages=257, numerical_tolerance=TOL,
        sign_tolerance=SIGN_TOL, fd_step=2**-14, fd_tolerance=FD_TOL,
        cluster_anchor_width=1e-9, minimum_resolved_gap=1e-7,
        soft_seconds=TIME_LIMIT, soft_rss_bytes=RSS_LIMIT,
        sparse_width=width, centered_H_row_bound=norm_h, centered_F_row_bound=norm_f,
        taylor_terms=24, taylor_max_step=.1,
        no_graph_formation_or_physical_ruler_claim=True)
    del hv, direct, incident, Hc, Fc, diffp, nz
    stage("operators")

    E, S = np.linalg.eigh(H)
    check("eigen_residual", H @ S, S * E)
    check("eigen_orthonormal", S.T @ S, np.eye(n))
    B = S.T @ A0
    rho = B @ B.T
    FE = S.T @ F @ S
    DE = S.T @ D @ S
    IE = S.T @ I @ S
    PE = S.T @ (pd[:, None] * S)
    del H, F, D, I
    check("rho_trace", np.trace(rho), 1.)
    check("rho_purity", np.sum(rho**2), 1 / rank)
    gaps = E[:, None] - E[None, :]
    u = np.exp(-1j * E * DELAY)
    du = (-1j * DELAY * np.exp(-.5j * (E[:, None] + E[None, :]) * DELAY)
          * np.sinc(gaps * DELAY / (2 * np.pi)) * FE)
    unitarity_derivative = u.conj()[:, None] * du
    check("unitarity_derivative", unitarity_derivative + unitarity_derivative.T.conj())
    del unitarity_derivative

    def evolved(op):
        return u.conj()[:, None] * op * u[None, :]

    def response(op):
        one = (u.conj()[:, None] * op) @ du
        return one + one.T.conj()

    ops = dict(kappa=evolved(DE), R_DF_off=response(DE), R_IF=response(IE),
               W_F2=-response(FE), F_start=FE, F_end=evolved(FE),
               I_end=evolved(IE), P_start=PE)
    kh_one = (u.conj() * E)[:, None] * du
    check("complete_source_energy_identity", kh_one + kh_one.T.conj() + ops["F_end"] - FE)
    del kh_one
    for name, op in ops.items():
        check("response_Hermitian_" + name, op, op.T.conj())
    stage("spectral_response")

    # Validate propagation and derivatives on actual unreset age PERIOD.
    yage_e = np.exp(-1j * E * PERIOD)[:, None] * B
    yage = S @ yage_e
    check("independent_age_action", taylor(A0, PERIOD), yage)
    yend = S @ (u[:, None] * yage_e)
    check("independent_pulse_action", taylor(yage, DELAY), yend)
    dy = S @ (du @ yage_e)
    fd_step = 2**-14
    yplus, yminus = taylor(yage, DELAY, fd_step), taylor(yage, DELAY, -fd_step)
    check("Frechet_action_central_difference", (yplus - yminus) / (2 * fd_step), dy, FD_TOL)
    actions = dict(D=d_action, I=i_action, F=f_action)
    response_names = dict(D="R_DF_off", I="R_IF", F="W_F2")
    for name, action in actions.items():
        derivative = 2 * np.vdot(yend, action(dy)).real
        finite = (expect_action(yplus, action) - expect_action(yminus, action)) / (2 * fd_step)
        check("observable_derivative_" + name, derivative, finite, FD_TOL)
        predicted = np.vdot(yage_e, ops[response_names[name]] @ yage_e).real
        check("effective_derivative_" + name, derivative, -predicted if name == "F" else predicted)
    for alpha, yf in [(fd_step, yplus), (-fd_step, yminus)]:
        work = alpha * (expect_action(yage, f_action) - expect_action(yf, f_action))
        check("source_switch_work", expect_action(yf, h_action) - initial_energy, work)
        check("source_on_energy_conservation", expect_action(yf, h_action) + alpha * expect_action(yf, f_action),
              initial_energy + alpha * expect_action(yage, f_action))
    result["independent_propagation"] = dict(
        taylor_tail_per_step_upper=math.exp(.1 * (norm_h + norm_f / 64))
            * (.1 * (norm_h + norm_f / 64))**25 / math.factorial(25),
        note="Centered row-norm tail per step; actual numerical controls also reported")
    del yplus, yminus, dy, yend, yage, yage_e, du, DE, IE
    stage("independent_controls")

    ages = np.linspace(0., 2 * PERIOD, 257)
    V = np.exp(-1j * E[:, None] * ages[None, :])
    histories, b2 = {}, {}
    for name, op in ops.items():
        coeff = rho * op  # rho is real symmetric in this real eigenbasis.
        values = np.sum(V.conj() * (coeff @ V), axis=0)
        check("real_history_" + name, values.imag)
        histories[name] = values.real
        b2[name] = float(np.sum(np.abs(coeff) * gaps**2))
    check("all_age_local_energy_start", histories["F_start"], 158 / 15)
    check("all_age_local_energy_end", histories["F_end"], 158 / 15)
    check("all_age_p0", histories["P_start"], 1 / 3)
    check("all_age_current", histories["I_end"])
    for age in [0., PERIOD, 2 * PERIOD]:
        ya = np.exp(-1j * E * age)[:, None] * B
        check("actual_rank_factor", ya.T.conj() @ ya, np.eye(rank) / rank)
        check("actual_total_energy", np.sum(np.abs(ya)**2 * E[:, None]), initial_energy)
        vi = np.exp(-1j * E * age)
        for name in ("kappa", "W_F2", "R_IF"):
            check("factor_trace_" + name, np.vdot(ya, ops[name] @ ya).real,
                  np.vdot(vi, (rho * ops[name]) @ vi).real)

    def matrix(values):
        return np.array([[2 * values["W_F2"], values["R_IF"]],
                         [values["R_IF"], values["kappa"]]])

    rows_out = []
    for k, age in enumerate(ages):
        values = {name: float(h[k]) for name, h in histories.items()}
        values["R_DF_on"] = values["R_DF_off"] + values["kappa"] / 2
        M = matrix(values)
        rows_out.append(dict(age=float(age), clock_phase=float(math.sqrt(5) * age),
                             **values, work_matrix=M.tolist(), eigenvalues=np.linalg.eigvalsh(M).tolist()))
    result["actual_age_rows"] = rows_out

    labels = np.empty(n, dtype=int)
    cluster_list = []
    left = 0
    while left < n:
        right = left + 1
        while right < n and E[right] - E[left] <= 1e-9:
            right += 1
        labels[left:right] = len(cluster_list)
        cluster_list.append(dict(start=left, size=right-left, energy_min=float(E[left]),
                                 energy_max=float(E[right-1]), width=float(E[right-1]-E[left])))
        left = right
    same = labels[:, None] == labels[None, :]
    minimum_gap = min(cluster_list[k+1]["energy_min"] - cluster_list[k]["energy_max"]
                      for k in range(len(cluster_list)-1))
    resolved = minimum_gap > 1e-7
    rho_diag = rho * same
    diag_values = {name: float(np.sum(rho_diag * op.T).real) for name, op in ops.items()}
    diag_values["R_DF_on"] = diag_values["R_DF_off"] + diag_values["kappa"] / 2
    result["bulk_diagonal_comparator"] = dict(resolved=resolved,
        minimum_intercluster_gap=minimum_gap, clusters=cluster_list, **diag_values,
        work_matrix=matrix(diag_values).tolist(), eigenvalues=np.linalg.eigvalsh(matrix(diag_values)).tolist(),
        not_a_prepared_state=True, running_clock_not_averaged=True)
    envelope = np.ones_like(gaps)
    np.divide(2., PERIOD * np.abs(gaps), out=envelope, where=~same)
    np.minimum(envelope, 1., out=envelope)
    envelope[same] = 0.
    # Add numerical within-cluster splittings: these are not exactly zero gaps.
    intra_envelope = np.minimum(2., np.abs(gaps) * (2 * PERIOD)) * same
    average_bounds = {name: float(np.sum(np.abs(rho * op.T) * (envelope + intra_envelope)))
                      for name, op in ops.items()}
    interpolation = {name: value * (PERIOD / 128)**2 / 8 for name, value in b2.items()}
    matrix_error = math.sqrt((2 * interpolation["W_F2"])**2
                            + 2 * interpolation["R_IF"]**2 + interpolation["kappa"]**2)
    average_matrix_error = math.sqrt((2 * average_bounds["W_F2"])**2
                            + 2 * average_bounds["R_IF"]**2 + average_bounds["kappa"]**2)
    windows = []
    for wi, a0 in enumerate([0., PERIOD]):
        rho_average = rho * np.exp(-1j * gaps * (a0 + PERIOD / 2)) * np.sinc(gaps * PERIOD / (2 * np.pi))
        av = {name: float(np.sum(rho_average * op.T).real) for name, op in ops.items()}
        av["R_DF_on"] = av["R_DF_off"] + av["kappa"] / 2
        errors = {name: av[name] - diag_values[name] for name in ops}
        for name in ops:
            check("average_envelope_" + name, max(0., abs(errors[name]) - average_bounds[name]))
        sl = rows_out[wi*128:wi*128+129]
        minimum = min(row["eigenvalues"][0] for row in sl)
        if minimum < -SIGN_TOL:
            decision = "NEGATIVE_ACTUAL_WORK_WITNESS"
        elif minimum > matrix_error + SIGN_TOL:
            decision = "QUADRATIC_FAMILY_POSITIVE_ENTIRE_WINDOW"
        else:
            decision = "UNCERTIFIED"
        windows.append(dict(interval=[a0, a0+PERIOD], average=av,
            averaged_matrix=matrix(av).tolist(), averaged_eigenvalues=np.linalg.eigvalsh(matrix(av)).tolist(),
            average_minus_comparator=errors, observable_average_bounds=average_bounds,
            sampled_minimum_eigenvalue=minimum, interpolation_matrix_error_bound=matrix_error,
            negative_sample_count=sum(row["eigenvalues"][0] < -SIGN_TOL for row in sl), decision=decision))
    result["windows"] = windows
    result["bounds"] = dict(second_derivative=b2, entry_interpolation=interpolation,
        matrix_interpolation=matrix_error, average_matrix_error=average_matrix_error,
        near_degenerate_comparator_correction_included=True)
    del V, coeff, rho_average, rho_diag, envelope, intra_envelope, same, gaps, ops, FE, PE
    stage("age_census_and_averages")

    worst_index = min(range(len(rows_out)), key=lambda k: rows_out[k]["eigenvalues"][0])
    worst = rows_out[worst_index]
    witness = dict(age_row_index=worst_index, age=worst["age"], checks=[])
    result["finite_control_witness"] = witness
    if worst["eigenvalues"][0] < -SIGN_TOL:
        vals, vecs = np.linalg.eigh(np.array(worst["work_matrix"]))
        direction = vecs[:, 0]
        witness.update(eigenvalue=float(vals[0]), direction=direction.tolist(),
                       status="NEGATIVE_QUADRATIC_DIRECTION_TESTED")
        ya = S @ (np.exp(-1j * E * worst["age"])[:, None] * B)
        ea = expect_action(ya, h_action)
        for amplitude in [1/64, -1/64, 1/128, -1/128, 1/256, -1/256]:
            alpha, phase = amplitude * direction
            ys = taylor(ya, DELAY, float(alpha))
            yk = np.exp(1j * phase * pd)[:, None] * ys
            won = float(alpha * expect_action(ya, f_action))
            woff = float(-alpha * expect_action(ys, f_action))
            kick = float((1 - math.cos(phase)) * expect_action(ys, d_action)
                         + math.sin(phase) * expect_action(ys, i_action))
            exact = expect_action(yk, h_action) - ea
            prediction = .5 * amplitude**2 * vals[0]
            check("finite_cycle_work_closure", exact, won + woff + kick, SIGN_TOL)
            check("finite_kick_work", expect_action(yk, h_action) - expect_action(ys, h_action), kick, SIGN_TOL)
            check("finite_source_energy", expect_action(ys, h_action) + alpha * expect_action(ys, f_action),
                  ea + alpha * expect_action(ya, f_action))
            check("finite_factor_norm", np.vdot(yk, yk).real, 1.)
            # If the kick were source-on, its extra contact cancels in switch-off.
            off_after = float(-alpha * expect_action(yk, f_action))
            check("source_on_contact_cancellation", (1 + alpha/2) * kick + off_after,
                  kick + woff, SIGN_TOL)
            witness["checks"].append(dict(amplitude=amplitude, alpha=float(alpha), phase=float(phase),
                work_on=won, work_off=woff, phase_work=kick, exact_work=exact,
                quadratic_prediction=float(prediction), absolute_quadratic_discrepancy=float(abs(exact-prediction)),
                relative_quadratic_discrepancy=float(abs((exact-prediction)/prediction)),
                negative_work_beyond_guard=bool(exact < -SIGN_TOL)))
            stage("finite_witness_" + str(amplitude))
    else:
        witness["status"] = "NO_NEGATIVE_ROW_TO_TEST"
    result["status"] = "COMPLETE_CONTROLS_PASS" if not failures else "COMPLETE_CONTROLS_FAILED"
    result["scientific_scope"] = "Finite supplied-graph work and response only; no metric, BTFR, expansion or observational promotion"
    stage("complete")
    OUTPUT.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(dict(status=result["status"], controls_failed=len(failures),
        window_decisions=[w["decision"] for w in windows], witness=witness["status"])), flush=True)


if __name__ == "__main__":
    main()
