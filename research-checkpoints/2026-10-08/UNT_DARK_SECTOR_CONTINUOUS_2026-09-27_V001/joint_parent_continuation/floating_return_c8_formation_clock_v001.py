#!/usr/bin/env python3
"""NEW fixed C8 reference. Execute only after root static review/ownership check."""
import os
for _key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_key] = "1"
import sys, json, math, hashlib, time, resource, traceback
from pathlib import Path
from fractions import Fraction as F
import numpy as np

J = Path(__file__).resolve().parent
ROOT = J.parent.parent
NAME = "FLOATING_RETURN_C8_FORMATION_CLOCK_V001"
PROTO = J / (NAME + ".md")
CP = J / "floating_return_c8_formation_clock_v001_checkpoints"
RESULT = J / (NAME + "_RESULT.json")
REPORT = J / (NAME + "_RESULT.md")
RECEIPT = J / (NAME + "_RECEIPT.json")
ERROR = J / (NAME + "_ERROR.json")
PINS = {
    NAME + ".md": "eb04c848f360295df81c18240a2617c18a152190c1b6caa1a38abba3d2a08cbc",
    "LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md": "255ea0ca5f86cc711cae2ff5e746d8e9b005c2156b934818ded7789f9461f2a4",
    "LOCAL_RECORD_FEEDBACK_FIVE_ISLAND_PASSIVE_COMPLETION_V001.md": "124f68b600130afcb3935e11c43c1f939a804892b2794c25f89c29a0892f8693",
    "LOCAL_RECORD_FEEDBACK_DRESSED_RECORD_CHARGE_V001.md": "e1742a5a3f7f68734f91c563fe04696b8d7664522e830ed8e261c708b7c83cb1",
    "NATIVE_DETUNED_LOCAL_STATE_FORMATION_V001.md": "9921170957bac4400d40a3515cf523723c5b28e9710c2819f7f468cfb87af516",
    "NATIVE_ACTIVE_RECORD_LOCALITY_AND_CLOCK_V001.md": "25ef80eef4d6225d362f7d256d59956bbe399ad59055e3f0d5e358568f6ff595",
    "NATIVE_CARRIER_CONTROLLED_CLOCK_V001.md": "55e7514ecdc636bc2817d78d44ca5a50422f8be2002877e96c92fca04636108b",
    "NATIVE_RESERVOIR_FORMATION_CHANNEL_V001.md": "6db32da99d6d346736e193b34b34cb270c242821051296de1be3bf7d86031a39",
    "NATIVE_FINITE_MEMORY_TRANSPORT_REALIZATION_V001.md": "5ffeccf4fe4041348a3e3b74571be43f607cb89908bc65940d68deb10781e64c",
    "NATIVE_MIDPOINT_SOURCE_CLOCK_CONSTRAINT_V001.md": "1c0cf577cbc9124b8c3f28fa6d639c8e06dfea25426bf015c9340215f571723a",
}
ARS = (F(0), F(1, 8), F(7, 40), F(1, 4))
GAMMAS = (F(0), F(1, 10))
TIMES = (F(0), F(1, 10), F(1, 5), F(2, 5), F(4, 5), F(1), F(2),
         F(4), F(8), F(12), F(16), F(24), F(32))
T = F(1, 10)
BASE = F(19, 2)
RHO = F(1, 8)
CYCLE = (0, 4, 3, 7, 2, 6, 1, 5)
CHECKS = []
INPUTS = {}
ACTIVE = {"case": None, "time": None, "stage": "unstarted"}
CREATED_CP = False

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def clean(v):
    if isinstance(v, np.ndarray):
        return clean(v.tolist())
    if isinstance(v, np.generic):
        return clean(v.item())
    if isinstance(v, dict):
        return {str(k): clean(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [clean(x) for x in v]
    if isinstance(v, float) and not math.isfinite(v):
        return {"nonfinite": repr(v)}
    if isinstance(v, complex):
        return [clean(float(v.real)), clean(float(v.imag))]
    return v

def blob(v):
    return json.dumps(clean(v), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()

def write_json(p, v):
    with Path(p).open("xb") as f:
        f.write(json.dumps(clean(v), indent=2, sort_keys=True, allow_nan=False).encode() + b"\n")
        f.flush()
        os.fsync(f.fileno())
    return sha(p)

def event(v):
    with (CP / "journal.jsonl").open("ab") as f:
        f.write(blob(v) + b"\n")
        f.flush()
        os.fsync(f.fileno())

def npz(p, **arrays):
    with Path(p).open("xb") as f:
        np.savez(f, **arrays)
        f.flush()
        os.fsync(f.fileno())
    return sha(p)

def gate(name, actual, expected=0.0, tol=1e-9):
    a, b = np.asarray(actual), np.asarray(expected)
    finite = bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
    error = float(np.max(np.abs(a - b))) if finite else float("inf")
    CHECKS.append({"name": name, "error": clean(error), "tolerance": tol,
                   "passed": finite and error <= tol})

def exact(name, condition):
    CHECKS.append({"name": name, "passed": bool(condition), "exact": True})

def rotate(r, j):
    j %= 8
    return ((int(r) << j) | (int(r) >> ((8 - j) % 8))) & 255 if j else int(r)

WORDS = np.arange(256, dtype=np.int64)
BITS = np.array([[(r >> v) & 1 for r in range(256)] for v in range(8)], dtype=np.int64)
POP = BITS.sum(axis=0)
ZSIG = 1 - 2 * BITS
FLIPS = np.array([WORDS ^ (1 << v) for v in range(8)])
REL = np.array([[rotate(r, -j) for r in WORDS] for j in range(8)])
RMINUS = np.array([rotate(r, -1) for r in WORDS])
RPLUS = np.array([rotate(r, 1) for r in WORDS])
PHASE = np.exp(2j * np.pi * np.outer(np.arange(8), np.arange(8)) / 8)
ETA = np.array([1 if CYCLE[v] < 4 else -1 for v in range(8)])
KWORD = ETA @ BITS

def authenticate():
    for name, digest in PINS.items():
        p = J / name
        if sha(p) != digest:
            raise RuntimeError("frozen input mismatch: " + name)
        INPUTS[str(p.relative_to(ROOT))] = digest
    floating = J / "LOCAL_RECORD_FEEDBACK_FLOATING_RETURN_COMPLETION_V001.md"
    count = 0
    for line in floating.read_text().splitlines():
        parts = [x.strip().strip(chr(96)) for x in line.split("|")]
        if len(parts) == 4 and len(parts[2]) == 64 and all(c in "0123456789abcdef" for c in parts[2]):
            p = ROOT / parts[1]
            if sha(p) != parts[2]:
                raise RuntimeError("floating ancestor mismatch: " + parts[1])
            INPUTS[parts[1]] = parts[2]
            count += 1
    if count != 7:
        raise RuntimeError("floating ancestor census")
    INPUTS[str(Path(__file__).resolve().relative_to(ROOT))] = sha(__file__)

def discrete_controls():
    occupied = {(i, 4 + i) for i in range(4)} | {(i, 4 + ((i + 1) % 4)) for i in range(4)}
    ce = {tuple(sorted((CYCLE[j], CYCLE[(j + 1) % 8]))) for j in range(8)}
    exact("literal_K44_C8_edges", ce == occupied and len(ce) == 8)
    exact("degrees_all_two", all(sum(v in e for e in ce) == 2 for v in range(8)))
    exact("eligibility_q4", all(len({(i, 4+j) for j in range(4)}) == 4 for i in range(4)))
    exact("rotation_inverse", all(rotate(rotate(r, j), -j) == r for r in range(256) for j in range(8)))
    for v in range(8):
        for r in range(256):
            target = int(FLIPS[v, r])
            q = int(BITS[v, r])
            delta_k = int(ETA[v]) * (1 - 2*q)
            exact("return_code_%d_%d" % (v, r),
                  int(KWORD[target]) == int(KWORD[r]) + delta_k
                  and -4 <= -int(KWORD[r]) - delta_k <= 4)
    gate("full_Fourier_unitarity", PHASE.conj().T @ PHASE / 8, np.eye(8), 5e-10)
    for ar in ARS[1:]:
        em, ed, gc, er = F(1,2), F(1,2), F(1,4), 2*ar
        r = ed+4*em
        sr = er-4*gc*gc/r
        weights = ((em*er-gc*gc)/(ed*r*sr), gc/(r*sr),
                   (er-gc)/(r*sr), (r-4*gc)/(r*sr))
        exact("passive_%s" % ar, sr > 0 and all(w >= 0 for w in weights))
        exact("native_matching_%s" % ar, 2*em == 1 and 2*gc == F(1,2) and er/2 == ar)

def full_apply(a, ar, gamma, centered=False):
    shape = a.shape
    s = a.reshape(8, 256, -1)
    base = 0.0 if centered else float(BASE)
    out = (base + ar*POP)[None, :, None] * s
    for j in range(8):
        out[j] = out[j] - float(T)*(s[(j-1)%8]+s[(j+1)%8]) + gamma*s[j, FLIPS[j]]
    return out.reshape(shape)

def block(k, ar, gamma):
    h = np.diag(float(BASE) + ar*POP).astype(np.complex128)
    h[WORDS ^ 1, WORDS] += gamma
    h[RMINUS, WORDS] -= float(T)*np.exp(-2j*np.pi*k/8)
    h[RPLUS, WORDS] -= float(T)*np.exp(2j*np.pi*k/8)
    return h

def modes(k, vectors):
    out = np.empty((8, 256, vectors.shape[1]), dtype=np.complex128)
    for j in range(8):
        out[j] = PHASE[j,k]*vectors[REL[j]]/math.sqrt(8)
    return out.reshape(2048, -1)

def reconstruct(v):
    out = np.empty((8, 256, 8), dtype=np.complex128)
    for j in range(8):
        for k in range(8):
            out[j,:,k] = PHASE[j,k]*v[k, REL[j]]/8
    return out.reshape(2048, 8)

def record_action(a, v, kind):
    if kind == "X":
        return a[:, FLIPS[v]]
    if kind == "Y":
        return -1j * ZSIG[v][None,:,None] * a[:, FLIPS[v]]
    if kind == "Z":
        return ZSIG[v][None,:,None] * a
    if kind == "q":
        return BITS[v][None,:,None] * a
    raise ValueError(kind)

def expect(a, o):
    return float(np.vdot(a, o).real)

def rate(z, dz):
    den = float(abs(z)**2)
    return None if den == 0 else float((np.conj(z)*dz).imag/den)

def frame(a, ad, ar, gamma, label):
    s, sd = a.reshape(8,256,8), ad.reshape(8,256,8)
    prob = np.sum(abs(s)**2, axis=2)
    prob_dot = 2*np.real(np.sum(np.conj(s)*sd, axis=2))
    p, pd = prob.sum(axis=1), prob_dot.sum(axis=1)
    record_prob, record_prob_dot = prob.sum(axis=0), prob_dot.sum(axis=0)
    q, qd = BITS @ record_prob, BITS @ record_prob_dot
    qq = (BITS*record_prob[None,:]) @ BITS.T
    vals = {kind: [] for kind in ("X","Y","Z")}
    dots = {kind: [] for kind in ("X","Y","Z")}
    joint = {kind: [] for kind in ("X","Y","Z")}
    joint_dot = {kind: [] for kind in ("X","Y","Z")}
    j_o = {kind: [] for kind in ("X","Y","Z")}
    for v in range(8):
        for kind in ("X","Y","Z"):
            oa, od = record_action(s,v,kind), record_action(sd,v,kind)
            vals[kind].append(expect(s,oa))
            dots[kind].append(2*expect(s,od))
            joint[kind].append(expect(s[v],oa[v]))
            joint_dot[kind].append(2*expect(s[v],od[v]))
            flow = sum(-2*float(T)*np.vdot(s[v],oa[u]).imag for u in ((v-1)%8,(v+1)%8))
            j_o[kind].append(float(flow))
    vals = {k: np.asarray(v) for k,v in vals.items()}
    dots = {k: np.asarray(v) for k,v in dots.items()}
    joint = {k: np.asarray(v) for k,v in joint.items()}
    joint_dot = {k: np.asarray(v) for k,v in joint_dot.items()}
    j_o = {k: np.asarray(v) for k,v in j_o.items()}
    hop, currents = [], []
    divergence = np.zeros(8)
    for u in range(8):
        v = (u+1)%8
        hop.append(2*float(np.vdot(s[u],s[v]).real))
        current = -2*float(T)*float(np.vdot(s[v],s[u]).imag)
        currents.append(current)
        divergence[u] -= current
        divergence[v] += current
    beta = vals["Z"]-1j*vals["Y"]
    beta_dot = dots["Z"]-1j*dots["Y"]
    pb = joint["Z"]-1j*joint["Y"]
    pbd = joint_dot["Z"]-1j*joint_dot["Y"]
    conditional, conditional_dot, conditional_rate = [], [], []
    for v in range(8):
        if p[v] == 0:
            conditional.append(None); conditional_dot.append(None); conditional_rate.append(None)
        else:
            b = pb[v]/p[v]
            db = (pbd[v]*p[v]-pb[v]*pd[v])/(p[v]*p[v])
            conditional.append(b); conditional_dot.append(db); conditional_rate.append(rate(b,db))
    n = float(prob.sum())
    rhoc = np.einsum("cri,dri->cd",s,np.conj(s))
    ehop = -float(T)*sum(hop)
    erecord = ar*float(sum(q))
    ecopy = gamma*float(sum(joint["X"]))
    efull = float(BASE)*n+ehop+erecord+ecopy
    gate(label+"_norm", n, 1)
    gate(label+"_p_continuity", pd, divergence)
    gate(label+"_record_Xdot", dots["X"], ar*vals["Y"])
    gate(label+"_record_Ydot", dots["Y"], -ar*vals["X"]-2*gamma*joint["Z"])
    gate(label+"_record_Zdot", dots["Z"], 2*gamma*joint["Y"])
    gate(label+"_joint_Xdot", joint_dot["X"], j_o["X"]+ar*joint["Y"])
    gate(label+"_joint_Ydot", joint_dot["Y"], j_o["Y"]-ar*joint["X"]-2*gamma*joint["Z"])
    gate(label+"_joint_Zdot", joint_dot["Z"], j_o["Z"]+2*gamma*joint["Y"])
    gate(label+"_q_Pauli", vals["Z"], n-2*q)
    gate(label+"_qdot", qd, -dots["Z"]/2)
    gate(label+"_second_diagonal", np.diag(qq), q)
    gate(label+"_energy", efull, float(BASE))
    gate(label+"_spectral_energy", float(np.vdot(a,1j*ad).real), efull)
    gate(label+"_carrier_trace", np.trace(rhoc), n)
    gate(label+"_source_state_dot", np.linalg.norm(ad+1j*full_apply(a,ar,gamma)), 0, 5e-10)
    if gamma == 0:
        gate(label+"_copyoff_blank", q, 0)
        gate(label+"_copyoff_beta", beta, 1)
        gate(label+"_copyoff_rate_derivative", beta_dot, 0)
    if ar == 0:
        gate(label+"_resonant_carrier_tracial", rhoc, np.eye(8)/8)
        gate(label+"_resonant_copy_contact", joint["X"], 0)
        gate(label+"_resonant_hopping", hop, 0)
    retention_current = -float(ETA @ qd)
    return_dist = np.array([record_prob[KWORD == k].sum() for k in range(-4,5)])
    return_dot = np.array([record_prob_dot[KWORD == k].sum() for k in range(-4,5)])
    gate(label+"_neutral_return_current", -np.dot(np.arange(-4,5),return_dot), retention_current)
    hold_a = full_apply(a,ar,0)
    hold_errors = []
    for v in range(8):
        qa = record_action(s,v,"q").reshape(a.shape)
        qha = record_action(hold_a.reshape(8,256,8),v,"q").reshape(a.shape)
        hold_errors.append(np.linalg.norm(full_apply(qa,ar,0)-qha))
    gate(label+"_all_record_hold_commutator",hold_errors,0,5e-10)
    blank = float(record_prob[0])
    return {
        "carrier_p":p, "carrier_p_dot":pd, "record_q":q, "record_q_dot":qd,
        "record_qq":qq, "record_Pauli":vals, "record_Pauli_dot":dots,
        "joint_pPauli":joint, "joint_pPauli_dot":joint_dot, "current_Pauli":j_o,
        "carrier_density":rhoc, "edge_T":hop, "edge_current_cycle_forward":currents,
        "beta":beta, "beta_dot":beta_dot, "beta_amplitude":np.abs(beta),
        "beta_dot_charging_piece":1j*ar*vals["X"],
        "beta_dot_copy_piece":2*gamma*joint["Y"]+2j*gamma*joint["Z"],
        "beta_principal_argument":np.angle(beta), "beta_rate_x":[rate(z,dz) for z,dz in zip(beta,beta_dot)],
        "conditional_beta":conditional, "conditional_beta_dot":conditional_dot,
        "conditional_beta_rate_x":conditional_rate, "unnormalized_pB":pb, "unnormalized_pB_dot":pbd,
        "pB_dot_transport_piece":j_o["Z"]-1j*j_o["Y"],
        "pB_dot_record_piece":2*gamma*joint["Y"]+1j*(ar*joint["X"]+2*gamma*joint["Z"]),
        "correlation_p_minus_rho_X":joint["X"]-float(RHO)*vals["X"],
        "bare_return_traced_X":np.zeros(8), "bare_return_traced_Y":np.zeros(8),
        "bare_return_traced_beta":vals["Z"], "return_charge_number_probabilities":return_dist[::-1],
        "return_charge_number_probability_dot":return_dot[::-1],
        "return_charge_dot":retention_current, "record_charge_dot":ETA*qd,
        "full_energy":efull, "field_self_energy":8*n, "record_charging_energy":erecord,
        "carrier_storage_current_energy":1.5*n, "hopping_energy":ehop, "copy_energy":ecopy,
        "all_age_copy_off_work":-ecopy, "all_age_post_quench_energy":efull-ecopy,
        "local_classical_content_trace_distance":q, "both_occupied_alphabet_probabilities":qq,
        "all_records_blank_probability":blank, "special_two_content_squared_fidelity":blank*blank,
        "clock_status":"STRUCTURAL_COPY_OFF_BLANK_CLOCK_NULL" if gamma == 0 else "RAW_INSTANTANEOUS_SAMPLED_CLOCK_ONLY",
        "retention_status":"EXACT_IDEAL_COPY_OFF_VALUE_HOLD_WITH_SWITCH_WORK",
    }

def derivative(a0, ar, gamma, op, n):
    powers = [a0]
    for _ in range(n):
        powers.append(full_apply(powers[-1],ar,gamma,centered=True))
    z = sum(((-1)**j)*math.comb(n,j)*np.vdot(powers[n-j],op(powers[j])) for j in range(n+1))
    return (1j**n)*z

def onset_controls(a0, ar, gamma, label):
    def rx(a):
        s = a.reshape(8,256,8)
        return record_action(s,0,"X").reshape(a.shape)
    def corr(a):
        out = -float(RHO)*rx(a).reshape(8,256,8)
        out[0] += rx(a).reshape(8,256,8)[0]
        return out.reshape(a.shape)
    def edge(a):
        s = a.reshape(8,256,8)
        out = np.zeros_like(s)
        out[0], out[1] = s[1], s[0]
        return out.reshape(a.shape)
    def beta(a):
        s = a.reshape(8,256,8)
        return (record_action(s,0,"Z")-1j*record_action(s,0,"Y")).reshape(a.shape)
    expected_beta = (1, 2j*gamma*float(RHO), -4*gamma*gamma*float(RHO),
                     -2j*gamma*float(RHO)*(ar*ar+4*gamma*gamma))
    observed = [derivative(a0,ar,gamma,beta,n) for n in range(4)]
    for n in range(4):
        gate(label+"_initial_beta_derivative%d"%n, observed[n], expected_beta[n])
    dc = derivative(a0,ar,gamma,corr,2)
    dt = derivative(a0,ar,gamma,edge,4)
    gate(label+"_detuned_correlation_second",dc,-2*ar*gamma*float(RHO)*(1-float(RHO)))
    gate(label+"_detuned_edge_fourth",dt,16*gamma*gamma*float(T)*float(RHO)*ar)
    variance = float(np.vdot(full_apply(a0,ar,gamma,True),full_apply(a0,ar,gamma,True)).real)
    gate(label+"_initial_variance",variance,2*float(T)**2+gamma**2)
    return {"beta_derivatives_x":observed,"correlation_second_x":dc,
            "edge_T_fourth_x":dt,"initial_variance":variance}

def run_case(index, arf, gf):
    start = time.monotonic()
    check_start = len(CHECKS)
    ar, gamma = float(arf), float(gf)
    label = "case%02d"%index
    ACTIVE.update(case=label,time=None,stage="eigensystem")
    ev = np.empty((8,256))
    vv = np.empty((8,256,256),dtype=np.complex128)
    coefficients = np.empty((8,256),dtype=np.complex128)
    for k in range(8):
        h = block(k,ar,gamma)
        gate(label+"_block_Hermitian_%d"%k,h,h.conj().T,5e-10)
        e,v = np.linalg.eigh(h)
        ev[k],vv[k],coefficients[k] = e,v,np.conj(v[0,:])
        gate(label+"_block_orthogonal_%d"%k,v.conj().T@v,np.eye(256),5e-10)
        gate(label+"_block_residual_%d"%k,h@v,v*e[None,:],5e-10)
        for m in range(0,256,16):
            full = modes(k,v[:,m:m+16])
            gate(label+"_full_mode_action_%d_%d"%(k,m),full_apply(full,ar,gamma),
                 full*e[None,m:m+16],5e-10)
    seed = np.zeros((8,256),dtype=np.complex128)
    seed[:,0] = 1
    a0 = reconstruct(seed)
    initial = a0.reshape(8,256,8)
    gate(label+"_initial_blank_carrier_density",initial[:,0,:]@initial[:,0,:].conj().T,
         np.eye(8)/8,5e-10)
    gate(label+"_initial_nonblank_support",np.linalg.norm(initial[:,1:,:]),0,5e-10)
    gate(label+"_initial_column_Gram",a0.conj().T@a0,np.eye(8)/8,5e-10)
    onset = onset_controls(a0,ar,gamma,label)
    meta = {"case":label,"AR_rational":str(arf),"gamma_rational":str(gf),
            "input_sha256":dict(INPUTS),"PID":os.getpid(),"full_dimension":2048,
            "all_block_trajectories_initial_norm":1,"rank8_reconstruction_denominator":8}
    eigenfile = CP/(label+"_eigensystem.npz")
    eigenhash = npz(eigenfile,eigenvalues=ev,eigenvectors=vv,blank_coefficients=coefficients,
                    initial_columns=a0,relative_record_maps=REL,cycle_nodes=np.asarray(CYCLE),
                    metadata_json=np.array(json.dumps(meta,sort_keys=True)))
    event({"event":"eigensystem_saved","case":label,"file":eigenfile.name,"sha256":eigenhash})
    rows = []
    for ti, xf in enumerate(TIMES):
        x = float(xf)
        ACTIVE.update(time=str(xf),stage="frame")
        vk = np.empty((8,256),dtype=np.complex128)
        dvk = np.empty_like(vk)
        for k in range(8):
            amp = np.exp(-1j*ev[k]*x)*coefficients[k]
            vk[k] = vv[k]@amp
            dvk[k] = vv[k]@(-1j*ev[k]*amp)
            gate(label+"_block_state_norm_%d_%d"%(ti,k),np.vdot(vk[k],vk[k]),1)
        a,ad = reconstruct(vk),reconstruct(dvk)
        values = frame(a,ad,ar,gamma,label+"_x%d"%ti)
        row = {"case":label,"time_index":ti,"x_rational":str(xf),"x":x,"observables":values,
               "input_sha256":dict(INPUTS),"eigensystem_sha256":eigenhash}
        filename = CP/(label+"_frame%02d.npz"%ti)
        ah = npz(filename,psi=a,psi_dot_x=ad,block_states=vk,block_dot_x=dvk,
                 metadata_json=np.array(json.dumps(clean({k:v for k,v in row.items() if k!="observables"}),sort_keys=True)))
        row["state_file"] = filename.name
        row["state_sha256"] = ah
        rh = write_json(CP/(label+"_frame%02d.json"%ti),row)
        event({"event":"frame_saved","case":label,"time_index":ti,"state":filename.name,
               "state_sha256":ah,"row":label+"_frame%02d.json"%ti,"row_sha256":rh})
        rows.append(clean(row))
    summary = {"case":label,"AR_rational":str(arf),"gamma_rational":str(gf),
               "branch":"OLD_RESONANT_NONPASSIVE_CONTROL" if arf==0 else "DECLARED_PASSIVE_COMPUTATIONAL_CANDIDATE",
               "eigensystem_sha256":eigenhash,"initial_onset":clean(onset),"rows":rows,
               "elapsed_seconds":time.monotonic()-start,"peakRSS_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "checks":list(CHECKS[check_start:]),"input_sha256":dict(INPUTS)}
    ch = write_json(CP/(label+"_complete.json"),summary)
    event({"event":"case_complete","case":label,"file":label+"_complete.json","sha256":ch})
    print(json.dumps({"case":label,"completed_frames":len(rows),"elapsed_seconds":summary["elapsed_seconds"],
                      "passed":sum(c["passed"] for c in CHECKS),"failed":sum(not c["passed"] for c in CHECKS)}),flush=True)
    return summary

def main():
    global CREATED_CP
    if sys.argv[1:] != ["--execute"]:
        raise SystemExit("Requires exact --execute after root preflight; no calculation performed.")
    authenticate()
    for p in (CP,RESULT,REPORT,RECEIPT,ERROR):
        if p.exists():
            raise RuntimeError("reserved output exists; preserve/recover first: "+str(p))
    CP.mkdir()
    CREATED_CP = True
    started = time.monotonic()
    manifest = {"PID":os.getpid(),"input_sha256":dict(INPUTS),"argv":["--execute"],
                "AR_rational":[str(x) for x in ARS],"gamma_rational":[str(x) for x in GAMMAS],
                "x_rational":[str(x) for x in TIMES],"Python":sys.version,"NumPy":np.__version__,
                "threads":{k:os.environ[k] for k in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","VECLIB_MAXIMUM_THREADS")}}
    mh = write_json(CP/"manifest.json",manifest)
    event({"event":"started","PID":os.getpid(),"manifest_sha256":mh,"input_sha256":dict(INPUTS)})
    discrete_controls()
    cases = []
    for ar in ARS:
        for gamma in GAMMAS:
            cases.append(run_case(len(cases),ar,gamma))
    exact("full_frozen_census",len(cases)==8 and all(len(c["rows"])==13 for c in cases))
    for name,digest in INPUTS.items():
        exact("input_unchanged_"+name,sha(ROOT/name)==digest)
    passed,failed = sum(c["passed"] for c in CHECKS),sum(not c["passed"] for c in CHECKS)
    status = "QUALIFIED_ARITHMETIC_NO_PHASE_OR_CLOCK_ADOPTION" if failed==0 else "ARITHMETIC_FAILED"
    result = {"status":status,"passed":passed,"failed":failed,"checks":list(CHECKS),"cases":cases,
              "input_sha256":dict(INPUTS),"manifest_sha256":mh,"PID":os.getpid(),
              "elapsed_seconds":time.monotonic()-started,"peakRSS_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "scope":"All8 cases/104 ages; fixed supplied C8; complete code; no physical calibration, source/strain adoption or retained-clock success gate."}
    canonical = hashlib.sha256(blob(result)).hexdigest()
    raw = write_json(RESULT,result)
    event({"event":"result_saved","raw_sha256":raw,"canonical_sha256":canonical})
    lines = ["# Floating-return C8 formation and clock result V001","",
             "%s: %d/%d arithmetic checks; all8 cases and104 frames."%(status,passed,len(CHECKS)),"",
             "Unwrapped/continuous/proper clocks are not qualified. All raw instantaneous rates and full states remain saved.",
             "Return-traced bare local X/Y are zero; joint dressed clock and gauge-invariant content readout are distinct.",
             "Every age has its ideal gamma-off work and exact retained-value hold; no best-age choice or free controller.",
             "","| Case | AR | gamma | x | sum q | Ecopy | Woff | beta0 amplitude | raw nu0 | max disjoint pair occupancy |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    def fmt(z):
        return "%.10g"%z if isinstance(z,(float,int)) else json.dumps(z,sort_keys=True)
    for case in cases:
        for row in case["rows"]:
            o = row["observables"]
            lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"%(
                case["case"],case["AR_rational"],case["gamma_rational"],row["x_rational"],
                fmt(sum(o["record_q"])),fmt(o["copy_energy"]),fmt(o["all_age_copy_off_work"]),
                fmt(o["beta_amplitude"][0]),fmt(o["beta_rate_x"][0]),
                fmt(max(o["record_qq"][i][j] for i in range(8) for j in range(i+1,8)))))
    lines += ["","Raw result SHA256: "+raw,"Canonical result SHA256: "+canonical,
              "No reservoir cooling, phase selection, physical proper-clock calibration, metric or expansion evidence is inferred."]
    with REPORT.open("x") as f:
        f.write("\n".join(lines)+"\n");f.flush();os.fsync(f.fileno())
    reporthash = sha(REPORT)
    event({"event":"report_saved","sha256":reporthash,"data_rows":104})
    cpmap = {p.name:sha(p) for p in sorted(CP.iterdir()) if p.name!="journal.jsonl"}
    receipt = {"status":status,"passed":passed,"failed":failed,"input_sha256":dict(INPUTS),
               "result_raw_sha256":raw,"result_canonical_sha256":canonical,"report_sha256":reporthash,
               "checkpoint_sha256":cpmap,"journal_prefix_sha256":sha(CP/"journal.jsonl"),"PID":os.getpid(),
               "elapsed_seconds":result["elapsed_seconds"],"peakRSS_bytes":result["peakRSS_bytes"]}
    rr = write_json(RECEIPT,receipt)
    event({"event":"receipt_saved","sha256":rr})
    print(json.dumps({"status":status,"passed":passed,"failed":failed,"raw_sha256":raw,
                      "receipt_sha256":rr,"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
    return 0 if failed==0 else 3

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        if not CREATED_CP:
            print(json.dumps({"status":"PREFLIGHT_REJECTED_NO_OUTPUT_MUTATION","error":repr(exc)}),flush=True)
            raise SystemExit(3)
        detail = {"error":repr(exc),"traceback":traceback.format_exc(),"active":dict(ACTIVE),
                  "PID":os.getpid(),"checks":list(CHECKS),"input_sha256":dict(INPUTS),
                  "checkpoint_sha256":{p.name:sha(p) for p in CP.iterdir() if p.is_file()} if CP.exists() else {}}
        if not ERROR.exists():
            write_json(ERROR,detail)
        if CP.exists():
            event({"event":"error","error_sha256":sha(ERROR),"active":dict(ACTIVE)})
        print(json.dumps({"status":"ERROR_PRESERVED","error":repr(exc),"active":ACTIVE}),flush=True)
        raise SystemExit(3)
