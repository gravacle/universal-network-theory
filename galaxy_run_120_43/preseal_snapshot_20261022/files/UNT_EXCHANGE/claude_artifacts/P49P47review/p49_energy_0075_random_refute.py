"""Claude independent randomized refutation attempts for P49-energy-0075 (own code, numpy)."""
import numpy as np, json, sys
rng = np.random.default_rng(20261012)
out = {}

def herm(d):
    A = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d)); return (A + A.conj().T)/2
def rand_state(d, rank=None):
    r = rank or d
    A = rng.normal(size=(d, r)) + 1j*rng.normal(size=(d, r)); R = A @ A.conj().T; return R/np.trace(R).real
def tn(X): return np.abs(np.linalg.eigvalsh((X + X.conj().T)/2)).sum()
def unitary(n):
    Q, R = np.linalg.qr(rng.normal(size=(n, n)) + 1j*rng.normal(size=(n, n))); return Q*(np.diag(R)/np.abs(np.diag(R)))

# ---- 1. criterion: random full H (degenerate), complex, seed subspace (non-coordinate too), word projectors ----
viol_iff = 0; max_resid_when_in_span = 0.0; min_gap_found = np.inf; n_fail_cases = 0; witness_ok = 0; witness_cases = 0
row_bound_ok = True; coherent_witness_cases = 0; in_span_cases = 0
for trial in range(400):
    n = rng.integers(3, 9); levels_vals = np.sort(rng.choice(np.arange(-4, 5), size=n))  # repeats -> degeneracy
    U = unitary(n); H = (U*levels_vals) @ U.conj().T
    distinct = np.unique(levels_vals)
    Pis = [U[:, levels_vals == e] @ U[:, levels_vals == e].conj().T for e in distinct]
    # words: partition of computational basis into 2..4 groups
    labels = rng.integers(0, rng.integers(2, 5), size=n)
    words = [np.diag((labels == k).astype(float)) for k in np.unique(labels)]
    Es = [sum(P @ Pw @ P for P in Pis) for Pw in words]
    assert np.allclose(sum(Es), np.eye(n))
    d = rng.integers(2, n)
    if trial % 2: Ps_basis = np.eye(n)[:, rng.choice(n, d, replace=False)]   # coordinate seed
    else: Ps_basis = unitary(n)[:, :d]                                       # general seed subspace
    K = Ps_basis.conj().T @ H @ Ps_basis
    kev = np.linalg.eigvalsh(K)
    if kev[-1] - kev[0] < 1e-6: continue
    for E in Es:
        C = Ps_basis.conj().T @ E @ Ps_basis
        t = np.trace(K).real; u = np.trace(K @ K).real; v = np.trace(C).real; z = np.trace(K @ C).real
        b = (d*z - t*v)/(d*u - t*t); a = (v - b*t)/d; W = C - a*np.eye(d) - b*K
        assert abs(np.trace(W)) < 1e-9 and abs(np.trace(K @ W)) < 1e-9
        R = np.abs(W).sum(axis=1).max(); op = np.abs(np.linalg.eigvalsh(W)).max()
        row_bound_ok &= bool(R >= op - 1e-12)
        # random interior E0, positive state at E0: mixture of eigenstates of K with positive weights
        E0 = kev[0] + (kev[-1] - kev[0])*rng.uniform(0.05, 0.95)
        w = rng.uniform(0.2, 1, size=d); w /= w.sum()
        # adjust weights to hit E0 exactly by mixing with two-point extreme mixture
        cur = w @ kev
        lo = np.zeros(d); lo[0] = 1; hi = np.zeros(d); hi[-1] = 1
        lam = (E0 - kev[-1])/(kev[0] - kev[-1]); ext = lam*lo + (1 - lam)*hi
        # convex combination s*w + (1-s)*ext has mean s*cur+(1-s)*E0; need E0 -> combine w-shift
        # simpler: find s so that s*w+(1-s)*target has mean E0 with target extreme on correct side
        tgt = lo if cur > E0 else hi; s = (E0 - tgt @ kev)/(cur - tgt @ kev); p = s*w + (1 - s)*tgt
        assert np.all(p > 0) and abs(p @ kev - E0) < 1e-9
        Vk = np.linalg.eigh(K)[1]; rho0 = (Vk*p) @ Vk.conj().T
        Wnorm = np.linalg.norm(W)
        if Wnorm < 1e-9:
            in_span_cases += 1
            # in span: probabilities over random tangent perturbations constant
            for _ in range(5):
                X = herm(d); # project out I and K in HS
                B = [np.eye(d), K]; G = np.array([[np.trace(x @ y).real for y in B] for x in B])
                c = np.linalg.solve(G, [np.trace(x @ X).real for x in B]); X = X - c[0]*B[0] - c[1]*B[1]
                sm = np.linalg.eigvalsh(rho0)[0]/np.abs(np.linalg.eigvalsh(X)).max()
                r1 = rho0 + sm*X
                max_resid_when_in_span = max(max_resid_when_in_span, abs(np.trace(r1 @ C).real - np.trace(rho0 @ C).real))
        else:
            n_fail_cases += 1
            s = np.linalg.eigvalsh(rho0)[0]/op
            rp, rm = rho0 + s*W, rho0 - s*W
            okE = abs(np.trace(rp @ K) - E0) < 1e-9 and abs(np.trace(rm @ K) - E0) < 1e-9
            okP = np.linalg.eigvalsh(rp)[0] > -1e-12 and np.linalg.eigvalsh(rm)[0] > -1e-12
            diff = np.trace((rp - rm) @ C).real
            if not (okE and okP and diff > 0): viol_iff += 1
            min_gap_found = min(min_gap_found, diff)
            # packet's own uniform-energy witness
            eps = 1/(2*d*R); wp = np.eye(d)/d + eps*W; wm = np.eye(d)/d - eps*W
            witness_cases += 1
            if (np.linalg.eigvalsh(wp)[0] >= 1/(2*d) - 1e-12 and np.linalg.eigvalsh(wm)[0] >= 1/(2*d) - 1e-12
                and abs(np.trace(wp @ K) - t/d) < 1e-9 and abs(np.trace(wm @ K) - t/d) < 1e-9
                and abs(np.trace((wp - wm) @ C).real - 2*eps*np.trace(W @ W).real) < 1e-9): witness_ok += 1
            if np.abs(W - np.diag(np.diag(W))).max() > 1e-9: coherent_witness_cases += 1
            # spread bound: any two states at mean E0 differ by <= 2R; check random extreme pair
            for _ in range(3):
                X = herm(d); B = [np.eye(d), K]; G = np.array([[np.trace(x @ y).real for y in B] for x in B])
                c = np.linalg.solve(G, [np.trace(x @ X).real for x in B]); X = X - c[0]*B[0] - c[1]*B[1]
                sm = np.linalg.eigvalsh(rho0)[0]/np.abs(np.linalg.eigvalsh(X)).max()
                r1 = rho0 + sm*X
                if abs(np.trace(r1 @ C).real - (a + b*E0)) > R + 1e-9: viol_iff += 1
out['criterion'] = dict(trials=400, nonzero_residual_word_cases=n_fail_cases, iff_or_bound_violations=viol_iff,
                        min_same_E0_probability_gap_at_random_interior_E0=float(min_gap_found),
                        max_prob_change_when_in_span=float(max_resid_when_in_span),
                        packet_uniform_witness_valid=f"{witness_ok}/{witness_cases}",
                        witness_cases_with_offdiagonal_W=coherent_witness_cases,
                        row_sum_bound_ge_opnorm=row_bound_ok, zero_residual_word_cases=in_span_cases)

# ---- 2. Cesaro bound: degenerate H, compare exact average to pairwise and uniform bounds ----
def cesaro_avg_formula(rho, Pis, evals, T, hbar):
    out_ = np.zeros_like(rho)
    for i, Pe in enumerate(Pis):
        for j, Pf in enumerate(Pis):
            om = evals[i] - evals[j]
            f = 1.0 if om == 0 else (1 - np.exp(-1j*om*T/hbar))/(1j*om*T/hbar)
            out_ += f*(Pe @ rho @ Pf)
    return out_
def cesaro_avg_quad(rho, H, T, hbar, N=4000):
    ev, V = np.linalg.eigh(H); ts = (np.arange(N) + 0.5)*T/N; acc = np.zeros_like(rho)
    for t in ts:
        Ut = (V*np.exp(-1j*ev*t/hbar)) @ V.conj().T; acc += Ut @ rho @ Ut.conj().T
    return acc/N
viol_pair = viol_unif = 0; max_ratio_unif = 0; max_ratio_pair = 0; quad_err = 0; fT_viol = 0
for trial in range(300):
    n = rng.integers(2, 8); m = rng.integers(1, n + 1)
    evals = np.sort(rng.choice(np.arange(-10, 11), size=m, replace=False)).astype(float)*rng.uniform(0.2, 2)
    mult = np.ones(m, int)
    for _ in range(n - m): mult[rng.integers(m)] += 1
    U = unitary(n); cols = np.repeat(np.arange(m), mult)
    Pis = [U[:, cols == k] @ U[:, cols == k].conj().T for k in range(m)]
    H = sum(e*P for e, P in zip(evals, Pis))
    rho = rand_state(n, rank=rng.integers(1, n + 1)); hbar = rng.uniform(0.3, 2.0)
    delta = np.inf if m == 1 else np.diff(evals).min()
    T = rng.choice([rng.uniform(0.01, 1), rng.uniform(1, 50)])/(1 if m == 1 else delta)
    DE = sum(P @ rho @ P for P in Pis)
    avg = cesaro_avg_formula(rho, Pis, evals, T, hbar)
    if trial < 40: quad_err = max(quad_err, tn(avg - cesaro_avg_quad(rho, H, T, hbar)))
    actual = tn(avg - DE)
    w = np.array([np.trace(P @ rho).real for P in Pis])
    pair = sum(min(1, 2*hbar/(T*abs(evals[i] - evals[j])))*np.sqrt(w[i]*w[j]) for i in range(m) for j in range(m) if i != j)
    unif = 0 if m == 1 else min(2, 2*hbar*(m - 1)/(T*delta))
    for i in range(m):
        for j in range(m):
            if i != j:
                om = evals[i] - evals[j]; f = abs((1 - np.exp(-1j*om*T/hbar))/(1j*om*T/hbar))
                if f > min(1, 2*hbar/(T*abs(om))) + 1e-12: fT_viol += 1
    if actual > pair + 1e-9: viol_pair += 1
    if actual > unif + 1e-9: viol_unif += 1
    if unif > 0: max_ratio_unif = max(max_ratio_unif, actual/unif)
    if pair > 0: max_ratio_pair = max(max_ratio_pair, actual/pair)
    # Born-law TV for a random complete projective word measurement <= half bound
out['cesaro'] = dict(trials=300, pairwise_bound_violations=viol_pair, uniform_bound_violations=viol_unif,
                     fT_modulus_bound_violations=fT_viol, max_actual_over_uniform=float(max_ratio_unif),
                     max_actual_over_pairwise=float(max_ratio_pair), formula_vs_quadrature_max_tracenorm=float(quad_err))

# ---- 3. Tightness probe: equal superposition pure state, two levels ----
best = 0
for T in np.linspace(0.05, 20, 4000):
    om = 1.0; f = abs((1 - np.exp(-1j*om*T))/(1j*om*T))
    # rho=|+><+| over 2 levels: ||offdiag||_1 = 2*|f|*1/2 = |f|; uniform bound 2/T
    best = max(best, f/min(2, 2/T))
out['tightness_two_level'] = float(best)

# ---- 4. single projector half factor ----
v = 0
for _ in range(500):
    d = rng.integers(2, 7); r1 = rand_state(d); r2 = rand_state(d); D = r1 - r2
    k = rng.integers(1, d); Q = unitary(d)[:, :k]; P = Q @ Q.conj().T
    if abs(np.trace(P @ D).real) > 0.5*tn(D) + 1e-12: v += 1
out['single_projector_half_violations'] = v

# ---- 5. full energy-weight matching: degenerate counterexample; nondegenerate automatic ----
Pe = np.diag([1., 1, 0]); Pw = np.zeros((3, 3)); Pw[0, 0] = 1  # word on basis 0
r1 = np.diag([1., 0, 0]); r2 = np.diag([0., 1, 0])
out['degenerate_energy_weight_counterexample'] = dict(weights=[np.trace(Pe @ r1), np.trace(Pe @ r2)],
    probs=[float(np.trace(r1 @ Pe @ Pw @ Pe)), float(np.trace(r2 @ Pe @ Pw @ Pe))])
# K2 vs K1^2 for noninvariant seed
H = np.array([[0., 1, 0], [1, 0, 1], [0, 1, 0]]); Ps = np.eye(3)[:, :2]
K1 = Ps.T @ H @ Ps; K2 = Ps.T @ H @ H @ Ps
out['K2_vs_K1sq'] = dict(K1sq=(K1 @ K1).tolist(), K2=K2.tolist())
json.dump(out, sys.stdout, indent=1, default=float)
