"""Blank-state K2,2 formation and exact initial two-hop readout; --run only.

One no-overwrite numerical JSON result; compact stdout. No fits, quenches,
SWAP propagation or physical metric. Source-only until explicit --run.
The assigned 1e-10 allowance is NOT a certified floating-point error bound.
"""
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
import tempfile
import time
import numpy as np
import scipy
from scipy import sparse
from scipy.sparse.linalg import expm_multiply

HERE = Path(__file__).resolve().parent
AGES = (0., .25, .5, 1., 2.)
TOL, DIM = 1e-10, 1024
PARAMETERS = dict(N=2, hbar=1., Omega=1., Delta=4., U_d=1., d_star=1.,
                  epsilon_psi=1., epsilon_r=1., epsilon_w=0., t_hop=.5,
                  lambda_R=.5, lambda_J=.25, g_wr=1., g_psi_r=0., g_rb=0.)
PINS = {"../recovered_sources/BS_MICRO_ACTION.md":
        "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
        "native_carrier_ruler_v001.py":
        "00a09a8c3caffc0ffe8df76a54787ddc010ec4d5196bedf773c34258d656b252"}
EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))
MASKS = np.arange(16)
BITS = ((MASKS[:, None] >> np.arange(4)) & 1).astype(float)
DEG = np.zeros((16, 4))
for e, (u, v) in enumerate(EDGES):
    DEG[:, u] += BITS[:, e]
    DEG[:, v] += BITS[:, e]
M = BITS[:, 0]*BITS[:, 2]+BITS[:, 1]*BITS[:, 3]
INDEX = np.arange(DIM)
GG, RR, CC = INDEX//64, (INDEX//4) % 16, INDEX % 4
BLOCKS = [np.arange(256)*4+c for c in range(4)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cj(z):
    return dict(real=float(np.real(z)), imag=float(np.imag(z)))


def maximum(x):
    a = x.data if sparse.issparse(x) else np.asarray(x)
    return float(np.max(np.abs(a), initial=0.))


def model(p):
    """CSR components: index=((graph_mask*16+record_mask)*4+carrier)."""
    def diag(x):
        return sparse.diags(np.broadcast_to(x, (DIM,)), format="csr")
    def flip(shift, coefficient):
        return sparse.csr_matrix((np.full(DIM, coefficient),
                                  (INDEX, INDEX ^ (1 << shift))), shape=(DIM, DIM))
    terms = dict(incidence_gap=diag(p["Delta"]*BITS[GG].sum(axis=1)),
                 degree_penalty=diag(p["U_d"]*((DEG[GG]-p["d_star"])**2).sum(axis=1)),
                 carrier_storage=diag(p["epsilon_psi"]),
                 writer_storage=diag(4*p["epsilon_w"]),
                 record_storage=diag(p["epsilon_r"]*BITS[RR].sum(axis=1)),
                 current_square=diag(p["lambda_J"]*DEG[GG, CC]),
                 record_feedback=diag(-p["lambda_R"]*(DEG[GG]*BITS[RR]).sum(axis=1)))
    terms["incidence_flips"] = sum(flip(e+6, -p["Omega"]/p["N"]) for e in range(4))
    terms["writer_copy"] = sum(flip(v+2, p["g_wr"]) for v in range(4))
    hopping = sparse.csr_matrix((DIM, DIM))
    for e, (u, v) in enumerate(EDGES):
        rows = INDEX[(BITS[GG, e] == 1) & ((CC == u) | (CC == v))]
        cols = rows+np.where(CC[rows] == u, v-u, u-v)
        hopping += sparse.csr_matrix((np.full(len(rows), -p["t_hop"]), (rows, cols)),
                                     shape=(DIM, DIM))
    terms["carrier_hopping"] = hopping
    return sum(terms.values()).tocsr(), terms


def tensor_action(psi, p):
    """Independent bit/tensor implementation, adapted from carrier-ruler indexing."""
    x = psi.reshape(16, 16, 4)
    gd = p["Delta"]*BITS.sum(axis=1)+p["U_d"]*((DEG-p["d_star"])**2).sum(axis=1)
    diagonal = (gd[:, None, None]+p["epsilon_psi"]+4*p["epsilon_w"]
                +p["epsilon_r"]*BITS.sum(axis=1)[None, :, None]
                +p["lambda_J"]*DEG[:, None, :]
                -p["lambda_R"]*(DEG @ BITS.T)[:, :, None])
    y = diagonal*x
    for e, (u, v) in enumerate(EDGES):
        y -= (p["Omega"]/p["N"])*x[MASKS ^ (1 << e)]
        y += p["g_wr"]*x[:, MASKS ^ (1 << e)]
        y[:, :, u] -= p["t_hop"]*BITS[:, e, None]*x[:, :, v]
        y[:, :, v] -= p["t_hop"]*BITS[:, e, None]*x[:, :, u]
    return y.reshape(DIM)


def taylor(H, psi, age, hbar):
    """Gershgorin-shifted sparse Taylor; reported tail excludes roundoff."""
    if age == 0:
        return psi.copy(), dict(steps=0, order=0, exact_arithmetic_tail=0.)
    d = H.diagonal()
    off = np.asarray(abs(H).sum(axis=1)).ravel()-abs(d)
    lo, hi = float(np.min(d-off)), float(np.max(d+off))
    center, radius = (lo+hi)/2, (hi-lo)/2
    steps = max(1, math.ceil(abs(age)*radius/(.5*hbar)))
    dt, z = age/(steps*hbar), abs(age)*radius/(steps*hbar)
    for order in range(1, 128):
        log_tail = ((order+1)*math.log(z)-math.lgamma(order+2)
                    -math.log1p(-z/(order+2)))
        if log_tail < math.log(1e-19):
            break
    else:
        raise ArithmeticError("Taylor order guard")
    shifted = H-center*sparse.eye(DIM, format="csr")
    result = psi.copy()
    for _ in range(steps):
        term, total = result.copy(), result.copy()
        for k in range(1, order+1):
            term = (-1j*dt/k)*(shifted @ term)
            total += term
        result = total
    result *= np.exp(-1j*center*age/hbar)
    return result, dict(steps=steps, order=order, gershgorin=[lo, hi], substep_norm=z,
                        exact_arithmetic_tail=math.expm1(steps*math.log1p(math.exp(log_tail))))


def moments(psi):
    prob = abs(psi.reshape(16, 16, 4))**2
    pg = prob.sum(axis=(1, 2))
    return pg @ BITS, float(pg @ (M*M)), prob


def scalar_bound(p):
    return float((math.sqrt(p[0]*p[2])+math.sqrt(p[1]*p[3]))**2)


def run():
    started, cpu = time.perf_counter(), time.process_time()
    target = HERE/"native_formed_twohop_v001_results.json"
    if target.exists() or target.is_symlink():
        raise FileExistsError("Refusing to overwrite "+str(target))
    _, hard = resource.getrlimit(resource.RLIMIT_CPU)
    limit = 60 if hard == resource.RLIM_INFINITY else min(60, hard)
    resource.setrlimit(resource.RLIMIT_CPU, (limit, limit))
    source_sha = sha(Path(__file__))
    inputs = {name: sha(HERE/name) for name in PINS}
    if inputs != PINS:
        raise RuntimeError("Pinned native input changed")
    inputs["NATIVE_TWO_HOP_CORRELATION_GEOMETRY_V001.md"] = sha(HERE/"NATIVE_TWO_HOP_CORRELATION_GEOMETRY_V001.md")
    checks, rows, oracles = [], [], []
    def check(name, actual, expected=0., tol=TOL):
        err = maximum(actual-expected)
        checks.append(dict(name=name, residual=err, allowance=tol,
                           passed=bool(math.isfinite(err) and err <= tol)))
    def real(name, z):
        check(name+":imaginary", z.imag)
        return float(z.real)
    ensembles = dict(M={6: .5, 9: .5}, I={k: 1/16 for k in range(16)}, C={0: .5, 15: .5},
                     even={k: 1/8 for k in range(16) if k.bit_count() % 2 == 0},
                     odd={k: 1/8 for k in range(16) if k.bit_count() % 2 == 1})
    for (label, weights), m2, d2 in zip(ensembles.items(), (0., .625, 2., .75, .5), (4., 6., 8., 6., 6.)):
        pg = np.array([weights.get(k, 0.) for k in range(16)])
        check(label+":marginals", pg @ BITS, np.full(4, .5))
        check(label+":M2", pg @ (M*M), m2)
        check(label+":degree_squared", pg @ (DEG*DEG).sum(axis=1), d2)
        check(label+":scalar_upper", scalar_bound(pg @ BITS), 1.)
        oracles.append(dict(name=label, weights=pg.tolist(), M2=m2, degree_squared_sum=d2))
    for subset in range(15):
        product = np.prod(BITS[:, [e for e in range(4) if subset & (1 << e)]], axis=1)
        check("parity:proper_marginal:"+str(subset),
              sum((ensembles["even"].get(k, 0.)-ensembles["odd"].get(k, 0.))*product[k] for k in range(16)))
    initial = np.zeros(DIM, complex)
    initial[0] = 1.
    for name in ("native", "feedback_off", "copying_off"):
        p = dict(PARAMETERS)
        if name == "feedback_off": p["lambda_R"] = 0.
        if name == "copying_off": p["g_wr"] = 0.
        H, terms = model(p)
        check(name+":dimension", np.array(H.shape), np.array([DIM, DIM]), 0.)
        check(name+":term_sum", H-sum(terms.values()))
        for key, term in terms.items(): check(name+":Hermitian:"+key, term-term.getH())
        check(name+":Hermitian", H-H.getH())
        probe = np.exp(1j*INDEX)/math.sqrt(DIM)
        for j, vector in enumerate((initial, probe)):
            check(name+":tensor_action:"+str(j), H @ vector, tensor_action(vector, p))
        for oracle in oracles:
            expected = (p["epsilon_psi"]+4*p["epsilon_w"]+2*p["Delta"]+p["lambda_J"]
                        +p["U_d"]*(oracle["degree_squared_sum"]-8*p["d_star"]+4*p["d_star"]**2))
            check(name+":ensemble_energy:"+oracle["name"], np.array(oracle["weights"]) @ H.diagonal()[MASKS*64], expected)
            oracle["complete_initial_energy"] = expected
        H2 = H @ H
        block = H2[BLOCKS[1], :][:, BLOCKS[0]]
        check(name+":H_wu_zero", H[BLOCKS[1], :][:, BLOCKS[0]])
        check(name+":full_H2_wu", block-p["t_hop"]**2*sparse.diags(np.repeat(M, 16)))
        hops = [H[BLOCKS[v], :][:, BLOCKS[u]] for u, v in EDGES]
        for e, hop in enumerate(hops):
            check(name+":one_hop_block:"+str(e), hop+p["t_hop"]*sparse.diags(np.repeat(BITS[:, e], 16)))
        gap = math.sqrt(p["epsilon_r"]**2+4*p["g_wr"]**2)
        bd = p["g_wr"]*(1-2*BITS[RR, 0])/gap
        bo = (p["epsilon_r"]/gap+2*BITS[RR, 0]-1)/2
        B = sparse.diags(bd)+sparse.csr_matrix((bo, (INDEX, INDEX ^ 4)), shape=H.shape)
        check(name+":clock_nilpotent", B @ B)
        check(name+":clock_normalization", B @ B.getH()+B.getH() @ B-sparse.eye(DIM))
        Bdot = 1j*(H @ B-B @ H)/p["hbar"]
        local_clock = Bdot[BLOCKS[0], :][:, BLOCKS[0]]
        check(name+":clock_carrier_identity", Bdot-sparse.kron(local_clock, sparse.eye(4)))
        check(name+":blank_clock", np.vdot(initial, B @ initial), p["g_wr"]/gap)
        E0 = real(name+":initial_energy", np.vdot(initial, H @ initial))
        check(name+":initial_energy_oracle", E0, 5.)
        for age in AGES:
            tag = name+":"+str(age)
            psi = expm_multiply((-1j*age/p["hbar"])*H, initial) if age else initial.copy()
            alt, method = taylor(H, initial, age, p["hbar"])
            check(tag+":Taylor_exponential_vector", psi, alt)
            check(tag+":norm", np.vdot(psi, psi), 1.)
            probs, m2, prob = moments(psi)
            alt_p, alt_m2, _ = moments(alt)
            check(tag+":method_edge_moments", probs, alt_p)
            check(tag+":method_M2", m2, alt_m2)
            energy = real(tag+":energy", np.vdot(psi, H @ psi))
            energies = {key: real(tag+":"+key, np.vdot(psi, term @ psi)) for key, term in terms.items()}
            check(tag+":energy_conservation", energy, E0)
            check(tag+":energy_terms", sum(energies.values()), energy)
            beta, beta_dot = np.vdot(psi, B @ psi), np.vdot(psi, Bdot @ psi)
            nu = float((beta.conjugate()*beta_dot).imag/abs(beta)**2) if abs(beta)**2 > TOL else None
            clock_ok = nu is not None and abs(nu) > TOL
            if name == "copying_off": check(tag+":copying_off_clock_null", beta)
            if name == "feedback_off": check(tag+":feedback_off_clock", beta_dot, 1j*gap*beta/p["hbar"])
            env = psi.reshape(256, 4)
            dc = float(np.sum(prob*DEG[:, None, :]))
            work_hopping = -energies["carrier_hopping"]
            swap_work = []
            for sender in (0, 1):
                Hss = H[BLOCKS[sender], :][:, BLOCKS[sender]]
                after = sum(np.vdot(env[:, c], Hss @ env[:, c]) for c in range(4))
                ds = float(np.sum(prob*DEG[:, sender, None, None]))
                work_current = p["lambda_J"]*(ds-dc)
                check(tag+":SWAP_complete_work:"+str(sender), after-energy, work_current+work_hopping)
                swap_work.append(dict(sender=sender, current_square=work_current, hopping=work_hopping,
                                      total=work_current+work_hopping, direct_energy_change=cj(after-energy)))
            direct_twohop = float(np.sum(abs(block @ env)**2))/(4*p["hbar"]**4)
            check(tag+":post_SWAP_twohop_block", direct_twohop, p["t_hop"]**4*m2/(4*p["hbar"]**4))
            for e, hop in enumerate(hops):
                check(tag+":post_SWAP_onehop_block:"+str(e), float(np.sum(abs(hop @ env)**2))/p["hbar"]**2,
                      p["t_hop"]**2*probs[e]/p["hbar"]**2)
            s2 = scalar_bound(probs)
            lower = m2-TOL-scalar_bound(np.clip(probs+TOL, 0., 1.))
            upper = m2+TOL-scalar_bound(np.clip(probs-TOL, 0., 1.))
            decision = ("NUMERICAL_SCALAR_BOUND_VIOLATION_UNDER_ASSIGNED_ALLOWANCE" if lower > 0 else
                        "NECESSARY_ONLY_COMPATIBILITY_UNDER_ASSIGNED_ALLOWANCE" if upper < 0 else "INCONCLUSIVE_UNDER_ASSIGNED_ALLOWANCE")
            rows.append(dict(case=name, age=age, parameters=p, state=dict(real=psi.real.tolist(), imag=psi.imag.tolist()),
                             norm=float(np.vdot(psi, psi).real), energy=energy, component_energies=energies,
                             edge_means=probs.tolist(), M2=m2, S2=s2, F=m2-s2, assigned_F_interval=[lower, upper],
                             ratio=m2/s2 if s2 > 0 else None, scalar_test=decision,
                             clock=dict(beta=cj(beta), beta_dot=cj(beta_dot), nu=nu,
                                        status="DEFINED" if clock_ok else ("UNDEFINED_COPYING_OFF" if name == "copying_off" else
                                                                          "UNRESOLVED_UNDER_ASSIGNED_ALLOWANCE")),
                             K_edges=(p["t_hop"]**2*probs/(p["hbar"]**2*nu**2)).tolist() if clock_ok else None,
                             L=p["t_hop"]**4*m2/(4*p["hbar"]**4*nu**4) if clock_ok else None,
                             swap_work=swap_work,
                             methods=dict(vector_max_difference=maximum(psi-alt), vector_l2_difference=float(np.linalg.norm(psi-alt)),
                                          edge_max_difference=maximum(probs-alt_p), M2_difference=m2-alt_m2, taylor=method)))
    check("self_source_unchanged", float(sha(Path(__file__)) != source_sha), 0., 0.)
    passed = all(item["passed"] for item in checks)
    payload = dict(status="COMPLETE" if passed else "FAILED_CHECKS", source_sha256=source_sha,
                   input_sha256=inputs, parameters=PARAMETERS, ages=AGES, dimension=DIM,
                   indexing="((graph_mask*16+record_mask)*4+carrier); bits e=(L0R0,L0R1,L1R0,L1R1), records v=(L0,L1,R0,R1)",
                   allowance=TOL, allowance_is_certified_error=False, oracles=oracles, rows=rows, checks=checks,
                   check_counts=dict(total=len(checks), passed=sum(c["passed"] for c in checks)),
                   qualification=dict(finite_candidate_only=True, deterministic_original_edge_surrogate_only=True,
                                      physical_metric=False, gravity=False, continuum=False, irreversible_record_formation=False,
                                      pointer_preparation_and_readout_instantiated=False, complete_bulk_SWAP_work=True),
                   runtime=dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__, executable=sys.executable,
                                wall_seconds=time.perf_counter()-started, cpu_seconds=time.process_time()-cpu,
                                max_rss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                                max_rss_units="bytes" if sys.platform == "darwin" else "KiB", threads=1))
    data = json.dumps(payload, separators=(",", ":"), allow_nan=False).encode()
    fd, temporary = tempfile.mkstemp(prefix="native_formed_twohop_v001_", suffix=".tmp", dir=HERE)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, target)  # Atomic no-overwrite publication, including races.
    finally:
        os.unlink(temporary)
    result_sha = hashlib.sha256(data).hexdigest()
    if sha(target) != result_sha:
        raise RuntimeError("Published result hash mismatch")
    summaries = [{key: row[key] for key in ("case", "age", "M2", "S2", "F", "assigned_F_interval", "ratio", "scalar_test", "clock", "swap_work")}
                 for row in rows]
    print(json.dumps(dict(status=payload["status"], path=str(target), sha256=result_sha, bytes=len(data),
                          source_sha256=source_sha, check_counts=payload["check_counts"],
                          failures=[c for c in checks if not c["passed"]], rows=summaries,
                          runtime=payload["runtime"]), separators=(",", ":"), allow_nan=False))
    return 0 if passed else 1


if __name__ == "__main__":
    if sys.argv[1:] != ["--run"]:
        raise SystemExit("Explicit --run required; refuses an existing result")
    try:
        code = run()
    except Exception as error:
        print(json.dumps(dict(status="ERROR", error_type=type(error).__name__, error=str(error))))
        code = 1
    raise SystemExit(code)
