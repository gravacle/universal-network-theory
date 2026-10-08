"""NumPy-only runtime alternative to preserved, import-failed V001; --run only.

Same physics, ages, scalar criterion and assigned 1e-10 allowance. Imports only
inert numerical definitions from the pinned carrier-ruler source, never run().
One atomic no-overwrite numerical JSON result; compact stdout. No metric claim.
"""
import os
import sys
sys.dont_write_bytecode = True
for key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import tempfile
import time
import numpy as np

HERE = Path(__file__).resolve().parent
AGES = (0., .25, .5, 1., 2.)
TOL, DIM = 1e-10, 1024
PARAMETERS = dict(N=2, hbar=1., Omega=1., Delta=4., U_d=1., d_star=1.,
                  epsilon_psi=1., epsilon_r=1., epsilon_w=0., t_hop=.5,
                  lambda_R=.5, lambda_J=.25, g_wr=1., g_psi_r=0., g_rb=0.)
PINS = {"../recovered_sources/BS_MICRO_ACTION.md":
        "00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec",
        "native_carrier_ruler_v001.py":
        "00a09a8c3caffc0ffe8df76a54787ddc010ec4d5196bedf773c34258d656b252",
        "native_formed_twohop_v001.py":
        "c88015012df42230452424b75f4d8d54ed391560403132167a2791f2adb015f4"}
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
    return float(np.max(np.abs(np.asarray(x)), initial=0.))


class NativeFormation:
    """Direct tensor terms versus independently assembled width-11 sparse rows."""
    def __init__(self, p):
        self.p = p
        self.diagonals = dict(
            incidence_gap=p["Delta"]*BITS[GG].sum(axis=1),
            degree_penalty=p["U_d"]*((DEG[GG]-p["d_star"])**2).sum(axis=1),
            carrier_storage=np.full(DIM, p["epsilon_psi"]),
            writer_storage=np.full(DIM, 4*p["epsilon_w"]),
            record_storage=p["epsilon_r"]*BITS[RR].sum(axis=1),
            current_square=p["lambda_J"]*DEG[GG, CC],
            record_feedback=-p["lambda_R"]*(DEG[GG]*BITS[RR]).sum(axis=1))
        self.diagonal = sum(self.diagonals.values()).reshape(16, 16, 4, 1)
        self.columns = np.zeros((DIM, 11), dtype=np.int64)
        self.values = np.zeros((DIM, 11))
        # This builder intentionally does not reuse BITS, DEG or self.diagonals.
        for mask in range(16):
            neighbors = [[] for _ in range(4)]
            for left in range(2):
                for right in range(2):
                    if (mask >> (2*left+right)) & 1:
                        neighbors[left].append(2+right)
                        neighbors[2+right].append(left)
            degrees = [len(group) for group in neighbors]
            graph_energy = p["Delta"]*mask.bit_count()+p["U_d"]*sum((d-p["d_star"])**2 for d in degrees)
            for record in range(16):
                feedback = -p["lambda_R"]*sum(degrees[v]*((record >> v) & 1) for v in range(4))
                for carrier in range(4):
                    row = (mask*16+record)*4+carrier
                    self.columns[row, 0] = row
                    self.values[row, 0] = (graph_energy+p["epsilon_psi"]+4*p["epsilon_w"]
                                           +p["epsilon_r"]*record.bit_count()+feedback+p["lambda_J"]*degrees[carrier])
                    for e in range(4):
                        self.columns[row, 1+e] = ((mask ^ (1 << e))*16+record)*4+carrier
                        self.values[row, 1+e] = -p["Omega"]/p["N"]
                        self.columns[row, 5+e] = (mask*16+(record ^ (1 << e)))*4+carrier
                        self.values[row, 5+e] = p["g_wr"]
                    for slot, other in enumerate(neighbors[carrier], start=9):
                        self.columns[row, slot] = (mask*16+record)*4+other
                        self.values[row, slot] = -p["t_hop"]
        radius = np.sum(abs(self.values[:, 1:]), axis=1)
        self.lower = float(np.min(self.values[:, 0]-radius))
        self.upper = float(np.max(self.values[:, 0]+radius))
        self.center, self.radius = (self.lower+self.upper)/2, (self.upper-self.lower)/2

    def action(self, matrix):
        x = matrix.reshape(16, 16, 4, -1)
        y = self.diagonal*x
        for e, (u, v) in enumerate(EDGES):
            y -= (self.p["Omega"]/self.p["N"])*x[MASKS ^ (1 << e)]
            y += self.p["g_wr"]*x[:, MASKS ^ (1 << e)]
            factor = self.p["t_hop"]*BITS[:, e, None, None]
            y[:, :, u] -= factor*x[:, :, v]
            y[:, :, v] -= factor*x[:, :, u]
        return y.reshape(matrix.shape)

    def sparse_action(self, matrix):
        x = matrix.reshape(DIM, -1)
        return np.sum(self.values[:, :, None]*x[self.columns], axis=1).reshape(matrix.shape)

    def dense_static(self):
        H = np.zeros((DIM, DIM))
        for slot in range(11):
            H[INDEX, self.columns[:, slot]] += self.values[:, slot]
        return H

    def term_actions(self, psi):
        terms = {key: value*psi for key, value in self.diagonals.items()}
        terms["incidence_flips"] = -self.p["Omega"]/self.p["N"]*sum(psi[INDEX ^ (1 << (e+6))] for e in range(4))
        terms["writer_copy"] = self.p["g_wr"]*sum(psi[INDEX ^ (1 << (v+2))] for v in range(4))
        x, hopping = psi.reshape(16, 16, 4), np.zeros((16, 16, 4), complex)
        for e, (u, v) in enumerate(EDGES):
            hopping[:, :, u] -= self.p["t_hop"]*BITS[:, e, None]*x[:, :, v]
            hopping[:, :, v] -= self.p["t_hop"]*BITS[:, e, None]*x[:, :, u]
        terms["carrier_hopping"] = hopping.ravel()
        return terms


def moments(psi):
    prob = abs(psi.reshape(16, 16, 4))**2
    pg = prob.sum(axis=(1, 2))
    return pg @ BITS, float(pg @ (M*M)), prob


def scalar_bound(p):
    return float((math.sqrt(p[0]*p[2])+math.sqrt(p[1]*p[3]))**2)


def run():
    started, cpu = time.perf_counter(), time.process_time()
    target = HERE/"native_formed_twohop_v002_results.json"
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
    spec = importlib.util.spec_from_file_location("formed_twohop_inert_ruler_helpers", HERE/"native_carrier_ruler_v001.py")
    helpers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helpers)  # Definitions only: never helpers.run/main/snapshot.
    checks, rows, oracles, early_controls = [], [], [], []
    def check(name, actual, expected=0., tol=TOL):
        err = maximum(np.asarray(actual)-np.asarray(expected))
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
    initial = np.zeros((DIM, 1), complex)
    initial[0, 0] = 1.
    for name in ("native", "feedback_off", "copying_off"):
        p = dict(PARAMETERS)
        if name == "feedback_off": p["lambda_R"] = 0.
        if name == "copying_off": p["g_wr"] = 0.
        system = NativeFormation(p)
        H = system.dense_static()  # Static controls only; never used for propagation/eigensolve.
        check(name+":dimension", H.shape, (DIM, DIM), 0.)
        check(name+":Hermitian", H, H.T)
        for sender in range(4):
            basis = np.zeros((DIM, 256))
            basis[BLOCKS[sender], np.arange(256)] = 1.
            check(name+":full_tensor_columns:"+str(sender), system.action(basis), H[:, BLOCKS[sender]])
            if sender == 0:
                h1 = system.sparse_action(basis)
                block = system.sparse_action(h1)[BLOCKS[1], :]
                check(name+":H_wu_zero", h1[BLOCKS[1]])
                check(name+":full_H2_wu", block, p["t_hop"]**2*np.diag(np.repeat(M, 16)))
        for oracle in oracles:
            expected = (p["epsilon_psi"]+4*p["epsilon_w"]+2*p["Delta"]+p["lambda_J"]
                        +p["U_d"]*(oracle["degree_squared_sum"]-8*p["d_star"]+4*p["d_star"]**2))
            check(name+":ensemble_energy:"+oracle["name"], np.array(oracle["weights"]) @ H.diagonal()[MASKS*64], expected)
            oracle["complete_initial_energy"] = expected
        hops = [H[np.ix_(BLOCKS[v], BLOCKS[u])] for u, v in EDGES]
        for e, hop in enumerate(hops):
            check(name+":one_hop_block:"+str(e), hop, -p["t_hop"]*np.diag(np.repeat(BITS[:, e], 16)))
        gap = math.sqrt(p["epsilon_r"]**2+4*p["g_wr"]**2)
        bd = p["g_wr"]*(1-2*BITS[RR, 0])/gap
        bo = (p["epsilon_r"]/gap+2*BITS[RR, 0]-1)/2
        def b_action(x):
            return bd*x+bo*x[INDEX ^ 4]
        def bdot_action(x):
            return 1j*(system.action(b_action(x))-b_action(system.action(x)))/p["hbar"]
        small_b = np.array([[bd[0], bo[0]], [bo[4], bd[4]]])
        check(name+":clock_nilpotent", small_b @ small_b)
        check(name+":clock_normalization", small_b @ small_b.T+small_b.T @ small_b, np.eye(2))
        # Multiplication by the two-entry clock uses only permutations/scaling.
        Bdot = 1j*(H*bd[None, :]+H[:, INDEX ^ 4]*bo[INDEX ^ 4][None, :]
                    -bd[:, None]*H-bo[:, None]*H[INDEX ^ 4, :])/p["hbar"]
        local_clock = Bdot[np.ix_(BLOCKS[0], BLOCKS[0])]
        for a in range(4):
            for b in range(4):
                check(name+":clock_carrier_identity:"+str((a, b)),
                      Bdot[np.ix_(BLOCKS[a], BLOCKS[b])], local_clock if a == b else 0.)
        check(name+":blank_clock", np.vdot(initial[:, 0], b_action(initial[:, 0])), p["g_wr"]/gap)
        E0 = real(name+":initial_energy", np.vdot(initial, system.action(initial)))
        check(name+":initial_energy_oracle", E0, 5.)
        h1_initial = system.sparse_action(initial[:, 0])
        h2_initial = system.sparse_action(h1_initial)
        early_p = moments(h1_initial)[0]/p["hbar"]**2
        early_m2 = moments(h2_initial)[1]/(4*p["hbar"]**4)
        flip_rate = p["Omega"]/(p["N"]*p["hbar"])
        check(name+":early_edge_t2", early_p, np.full(4, flip_rate**2))
        for e in range(4):
            for f in range(e+1, 4):
                joint = float(np.sum(abs(h2_initial)**2*BITS[GG, e]*BITS[GG, f]))/(4*p["hbar"]**4)
                check(name+":early_joint_t4:"+str((e, f)), joint, flip_rate**4)
        check(name+":early_M2_t4", early_m2, 2*flip_rate**4)
        check(name+":early_F_t4", early_m2-scalar_bound(early_p), -2*flip_rate**4)
        early_controls.append(dict(case=name, edge_t2=early_p.tolist(), M2_t4=early_m2,
                                   S2_t4=scalar_bound(early_p), F_t4=early_m2-scalar_bound(early_p)))
        for age in AGES:
            tag = name+":"+str(age)
            primary, cheb = helpers.chebyshev_action(system.action, initial, system.center, system.radius, age/p["hbar"])
            independent, taylor = helpers.taylor_action(system.sparse_action, initial, system.center, system.radius, age/p["hbar"])
            psi, alt = primary[:, 0], independent[:, 0]
            check(tag+":Chebyshev_Taylor_vector", psi, alt)
            check(tag+":Chebyshev_Taylor_l2", np.linalg.norm(psi-alt))
            check(tag+":norm", np.vdot(psi, psi), 1.)
            probs, m2, prob = moments(psi)
            alt_p, alt_m2, _ = moments(alt)
            check(tag+":method_edge_moments", probs, alt_p)
            check(tag+":method_M2", m2, alt_m2)
            hpsi, terms = system.action(psi), system.term_actions(psi)
            check(tag+":full_term_action", sum(terms.values()), hpsi)
            energy = real(tag+":energy", np.vdot(psi, hpsi))
            energies = {key: real(tag+":"+key, np.vdot(psi, value)) for key, value in terms.items()}
            check(tag+":energy_conservation", energy, E0)
            check(tag+":energy_terms", sum(energies.values()), energy)
            beta, beta_dot = np.vdot(psi, b_action(psi)), np.vdot(psi, bdot_action(psi))
            check(tag+":clock_dense_oracle", bdot_action(psi), Bdot @ psi)
            nu = float((beta.conjugate()*beta_dot).imag/abs(beta)**2) if abs(beta)**2 > TOL else None
            clock_ok = nu is not None and abs(nu) > TOL
            if name == "copying_off": check(tag+":copying_off_clock_null", beta)
            if name == "feedback_off": check(tag+":feedback_off_clock", beta_dot, 1j*gap*beta/p["hbar"])
            env = psi.reshape(256, 4)
            dc, work_hopping = float(np.sum(prob*DEG[:, None, :])), -energies["carrier_hopping"]
            swap_work = []
            for sender in (0, 1):
                Hss = H[np.ix_(BLOCKS[sender], BLOCKS[sender])]
                after = np.vdot(env, Hss @ env)
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
                                          edge_max_difference=maximum(probs-alt_p), M2_difference=m2-alt_m2,
                                          gershgorin=[system.lower, system.upper], center=system.center, radius=system.radius,
                                          chebyshev=cheb, taylor=taylor)))
    check("self_source_unchanged", float(sha(Path(__file__)) != source_sha), 0., 0.)
    passed = all(item["passed"] for item in checks)
    payload = dict(status="COMPLETE" if passed else "FAILED_CHECKS", source_sha256=source_sha,
                   input_sha256=inputs, parameters=PARAMETERS, ages=AGES, dimension=DIM,
                   indexing="((graph_mask*16+record_mask)*4+carrier); bits e=(L0R0,L0R1,L1R0,L1R1), records v=(L0,L1,R0,R1)",
                   prior_attempt=dict(source="native_formed_twohop_v001.py", source_sha256=PINS["native_formed_twohop_v001.py"],
                                      root_reported_error="ModuleNotFoundError: No module named 'scipy'", stage="import before scientific calculation"),
                   runtime_alternative="NumPy-only pinned Chebyshev tensor action versus independently assembled row-sparse Taylor action",
                   inherited_propagator_configuration={key: helpers.CONFIG[key] for key in
                                                       ("chebyshev_tail", "taylor_substep_tail", "taylor_max_norm",
                                                        "max_chebyshev_degree", "max_taylor_terms")},
                   allowance=TOL, allowance_is_certified_error=False, oracles=oracles,
                   early_time_coefficients=early_controls, rows=rows, checks=checks,
                   check_counts=dict(total=len(checks), passed=sum(c["passed"] for c in checks)),
                   qualification=dict(finite_candidate_only=True, deterministic_original_edge_surrogate_only=True,
                                      physical_metric=False, gravity=False, continuum=False, irreversible_record_formation=False,
                                      pointer_preparation_and_readout_instantiated=False, complete_bulk_SWAP_work=True,
                                      numerical_tail_and_alias_exclude_roundoff=True),
                   runtime=dict(python=sys.version, numpy=np.__version__, executable=sys.executable,
                                wall_seconds=time.perf_counter()-started, cpu_seconds=time.process_time()-cpu,
                                max_rss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                                max_rss_units="bytes" if sys.platform == "darwin" else "KiB", threads=1))
    data = json.dumps(payload, separators=(",", ":"), allow_nan=False).encode()
    fd, temporary = tempfile.mkstemp(prefix="native_formed_twohop_v002_", suffix=".tmp", dir=HERE)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, target)
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
