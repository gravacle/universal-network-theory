"""Fixed-A Q1/M2 sector (old A=(1,1), Born A=(1,1,0,0)) numeric checks with the
reviewer's own model: census, closure, Hermiticity, [U,H]=0 in-sector, coordinate
connectivity, moment equality, gauge-evenness, and numerical short-time ratios.
Own code; no Codex import."""
import json, os, sys
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p47_c2sham_0114_model import G, params, owners, U, sector_states, pc

S0 = (0, 3, 1, 3, 0, 3)


def build(P, states):
    idx = {s: i for i, s in enumerate(states)}
    rows, cols, vals = [], [], []
    closed = True
    for j, st in enumerate(states):
        agg = {}
        for _, _, tg, a in owners(st, P):
            agg[tg] = agg.get(tg, G()) + a
        for tg, a in agg.items():
            if not a:
                continue
            if tg not in idx:
                closed = False
                continue
            rows.append(idx[tg]); cols.append(j); vals.append(a.c())
    return idx, np.array(rows), np.array(cols), np.array(vals), closed


def matvec(rows, cols, vals, n, x):
    w = vals * x[cols]
    return np.bincount(rows, weights=w.real, minlength=n) + 1j * np.bincount(rows, weights=w.imag, minlength=n)


def evolve(rows, cols, vals, n, psi, hbar, tau, nsteps, order=30):
    dt = tau / nsteps
    for _ in range(nsteps):
        term = psi.copy(); acc = psi.copy()
        for k in range(1, order + 1):
            term = matvec(rows, cols, vals, n, term) * (-1j * dt / hbar) / k
            acc = acc + term
            if np.max(np.abs(term)) < 1e-18:
                break
        psi = acc
    return psi


def components(rows, cols, n):
    parent = np.arange(n)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for r, c in zip(rows.tolist(), cols.tolist()):
        if r != c:
            a, b = find(r), find(c)
            if a != b:
                parent[a] = b
    roots = np.array([find(i) for i in range(n)])
    return roots


def main():
    out = {}
    states = sector_states()
    nold = sum(1 for s in states if s[0] == 0); nborn = len(states) - nold
    out['census'] = dict(old=nold, born=nborn, total=len(states))
    P = params()
    hb = float(P['hbar']); g = float(P['g']); k0 = P['kappa'][0].c()
    idx, rows, cols, vals, closed = build(P, states)
    n = len(states)
    out['closed_under_H'] = closed
    out['nnz'] = int(len(vals))
    # Hermiticity
    Hd = {}
    for r, c, v in zip(rows.tolist(), cols.tolist(), vals.tolist()):
        Hd[(r, c)] = Hd.get((r, c), 0) + v
    out['hermitian'] = all(abs(Hd.get((c, r), 0) - np.conj(v)) == 0 for (r, c), v in Hd.items())
    # U within sector
    Uidx = np.array([idx[U(s)] for s in states])
    out['U_maps_sector_to_itself'] = True
    out['U2_identity'] = bool(np.array_equal(Uidx[Uidx], np.arange(n)))
    HU = {(Uidx[r], Uidx[c]): v for (r, c), v in Hd.items()}
    out['UHU_equals_H_exact_float'] = (HU.keys() == Hd.keys()) and all(HU[k] == Hd[k] for k in Hd)
    i0 = idx[S0]; i1 = idx[U(S0)]
    out['s0_index'] = i0; out['s1'] = list(U(S0))
    out['H_s1_s0'] = str(Hd.get((i1, i0), 0)); out['minus_2t'] = -2 * float(P['t'])
    # connectivity of literal nonzero coordinate-transition graph
    roots = components(rows, cols, n)
    uniq, counts = np.unique(roots, return_counts=True)
    out['coordinate_components_generic'] = dict(count=int(uniq.size), sizes=sorted(counts.tolist(), reverse=True)[:5],
                                                s0_s1_same=bool(roots[i0] == roots[i1]))
    # g=0 fragmentation contrast
    P0 = params(g=F(0))
    _, r0, c0, v0, _ = build(P0, states)
    roots0 = components(r0, c0, n)
    u0, cnt0 = np.unique(roots0, return_counts=True)
    out['coordinate_components_g0'] = dict(count=int(u0.size), s0_s1_same=bool(roots0[i0] == roots0[i1]))
    # moments
    e0 = np.zeros(n, complex); e0[i0] = 1
    e1 = np.zeros(n, complex); e1[i1] = 1
    a, b = e0.copy(), e1.copy(); mom = []
    for k in range(1, 31):
        a = matvec(rows, cols, vals, n, a); b = matvec(rows, cols, vals, n, b)
        m0 = np.vdot(e0, a); m1 = np.vdot(e1, b)
        mom.append(abs(m0 - m1) / max(1.0, abs(m0)))
    out['moment_rel_diff_max_k1_30'] = float(max(mom))
    # numeric short-time ratios
    q0 = np.array([(s[3] >> 0) & 1 for s in states], float)
    q1 = np.array([(s[3] >> 1) & 1 for s in states], float)
    S0o = np.array([(s[5] >> 0) & 1 for s in states], float)
    S1o = np.array([(s[5] >> 1) & 1 for s in states], float)
    ratios = []
    for tau in (1e-3, 1e-2, 5e-2):
        pa = evolve(rows, cols, vals, n, e0, hb, tau, 1)
        pb = evolve(rows, cols, vals, n, e1, hb, tau, 1)
        A = lambda o, ps: float(np.sum(o * np.abs(ps) ** 2))
        dq0 = A(q0, pa) - 0.5 * (A(q0, pa) + A(q0, pb))
        dq1 = A(q1, pa) - 0.5 * (A(q1, pa) + A(q1, pb))
        dS0 = A(S0o, pa) - 0.5 * (A(S0o, pa) + A(S0o, pb))
        ratios.append(dict(tau=tau, Dq0_over_tau2=dq0 / tau ** 2, Dq1_over_tau2=dq1 / tau ** 2,
                           DS0_over_tau2=dS0 / tau ** 2, Dq0_plus_Dq1=dq0 + dq1))
    out['numeric_short_time'] = ratios
    out['predicted_Dq0_tau2'] = -g * g / (2 * hb * hb)
    out['predicted_DS0_tau2'] = -abs(k0) ** 2 / (2 * hb * hb)
    # gauge-evenness: complex kappa/epsB vs |kappa|,|epsB| (same moduli) give identical diagonal reads
    Pabs = params(kappa01=G(F(2, 3), F(1, 5)), kappa23=G(F(-1, 7), F(3, 4)), epsB=G(F(1, 2), F(-2, 3)))
    # replace by moduli (float) using a float-valued model: build complex H then rephase
    kmod = abs(P['kappa'][0].c()); emod = abs(P['epsilon_B'].c())
    vals_abs = vals.copy()
    th_k = np.angle(P['kappa'][0].c()); th_e = np.angle(P['epsilon_B'].c())
    Ns = np.array([pc(s[5]) for s in states]); sec = np.array([s[0] for s in states])
    W = np.exp(1j * (th_k * Ns + th_e * sec))  # diagonal gauge
    vals_g = np.conj(W[rows]) * vals * W[cols]
    out['gauge_removes_all_complex_parts_max_imag'] = float(np.max(np.abs(vals_g.imag)))
    traj = []
    psiA = e0.copy(); psiB = e1.copy(); psiAg = e0.copy()
    tgrid = [0.5 * k for k in range(1, 25)]
    last = 0.0
    for tt in tgrid:
        psiA = evolve(rows, cols, vals, n, psiA, hb, tt - last, 20)
        psiB = evolve(rows, cols, vals, n, psiB, hb, tt - last, 20)
        last = tt
        A = lambda o, ps: float(np.sum(o * np.abs(ps) ** 2))
        traj.append(dict(tau=tt, Dq0=A(q0, psiA) - 0.5 * (A(q0, psiA) + A(q0, psiB)),
                         DS0=A(S0o, psiA) - 0.5 * (A(S0o, psiA) + A(S0o, psiB)),
                         norm=float(np.linalg.norm(psiA))))
    out['manufactured_param_history_Dq0_DS0'] = traj
    # time-reversal: real gauge-transformed H -> <O(-t)> = <O(t)>
    psi_p = evolve(rows, cols, vals, n, e0, hb, 0.7, 20)
    psi_m = evolve(rows, cols, vals, n, e0, hb, -0.7, 20)
    out['evenness_q0_t0.7_vs_minus0.7_absdiff'] = abs(float(np.sum(q0 * np.abs(psi_p) ** 2)) - float(np.sum(q0 * np.abs(psi_m) ** 2)))
    out['evenness_S0_t0.7_vs_minus0.7_absdiff'] = abs(float(np.sum(S0o * np.abs(psi_p) ** 2)) - float(np.sum(S0o * np.abs(psi_m) ** 2)))
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p47_c2sham_0114_sector_numeric_out.json')
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != 'manufactured_param_history_Dq0_DS0'}, indent=1, default=str))
    print('history', [(d['tau'], round(d['Dq0'], 4), round(d['DS0'], 4)) for d in traj])


if __name__ == '__main__':
    main()
