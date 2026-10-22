"""Stage-0 analysis library (PREREG_STAGE0_V001). numpy only; imports no program module.
Transcriptions (cited): S4 = helpers/coefficient_method/owned_collective_worldline_static_response_pairallk_v004.py (7d079892)
  _sokal_tau :3722-3743, _rhat :3746-3759, _analyze column statuses :3793-3843, _estimate :3707-3716,
  _allk_analyze block projection :4320-4352 (Mandel sqrt2 once, profile-major, NN contact positions).
Grid / gate / distances: BIRTHK_PILOT_EVALUATION_2026-10-17_V001/scripts/b7_gate_coeff.py (grid_arr, gate, rel).
Background C-bar: b7 bgC / Claude3 cbar_anisotropy_c3v001.py moments."""
import glob, math, os
import numpy as np

RHAT_MAX = 1.1; RATIO_MIN = 5.0; C_WIN = 5.0; N_BATCH = 8
FLAT_FACTOR = 2.91          # PREREG section 2: 3.36 * sqrt(3/4), Bonferroni over 64 quarter tests
MA_GUARD = 2.0              # PREREG section 2: per-chain tau <= 2 * blen / 5 in R-MA
BG_LABELS = [['background_cell_sum_whitened_R', 0], ['background_cell_sum_whitened_R', 1], ['background_cell_sum_whitened_R', 2],
             ['background_cell_sum_whitened_S', 0, 0], ['background_cell_sum_whitened_S', 1, 1], ['background_cell_sum_whitened_S', 2, 2],
             ['background_cell_sum_whitened_S', 1, 2], ['background_cell_sum_whitened_S', 0, 2], ['background_cell_sum_whitened_S', 0, 1]]


# ---------------- S4 estimators (exact transcriptions) ----------------
def sokal_tau(series, c_window=C_WIN):
    x = np.asarray(series, dtype=np.float64); n = x.shape[0]
    if n < 2: return 'unassessable', None
    xc = x - x.mean(); var0 = float(np.einsum('i,i->', xc, xc, optimize=False)) / n
    if var0 == 0.0: return 'constant', None
    f = np.fft.rfft(xc, 2 * n); acov = np.fft.irfft(f * np.conj(f), 2 * n)[:n] / n
    rho = acov / acov[0]; taus = 0.5 + np.cumsum(rho[1:]); windows = np.arange(1, n, dtype=np.float64)
    hit = np.flatnonzero(windows >= c_window * taus)
    if hit.size == 0: return 'unassessable', None
    tau = float(taus[hit[0]])
    if not tau > 0.0: return 'unassessable', None
    return 'assessed', tau


def rhat(columns):
    columns = np.asarray(columns, dtype=np.float64); c, m = columns.shape
    if c < 2 or m < 2: return 'unassessable', None
    means = columns.mean(axis=1); within = float(np.mean(columns.var(axis=1, ddof=1)))
    if within == 0.0:
        if float(means.max() - means.min()) == 0.0: return 'constant', None
        return 'failed', math.inf
    between = m * float(means.var(ddof=1)); var_plus = (m - 1.0) / m * within + between / m
    return 'assessed', math.sqrt(var_plus / within)


def pooled_acf_tau(X, c_window=C_WIN):
    """R-MA: Sokal window on the chain-averaged normalized autocovariance (each chain centred on its own mean)."""
    X = np.asarray(X, dtype=np.float64); C, n = X.shape; rhos = []
    for x in X:
        xc = x - x.mean(); var0 = float(np.dot(xc, xc)) / n
        if var0 == 0.0: continue
        f = np.fft.rfft(xc, 2 * n); acov = np.fft.irfft(f * np.conj(f), 2 * n)[:n] / n; rhos.append(acov / acov[0])
    if not rhos: return 'constant', None
    rho = np.mean(rhos, axis=0); taus = 0.5 + np.cumsum(rho[1:]); windows = np.arange(1, n, dtype=np.float64)
    hit = np.flatnonzero(windows >= c_window * taus)
    if hit.size == 0: return 'unassessable', None
    tau = float(taus[hit[0]])
    return ('assessed', tau) if tau > 0.0 else ('unassessable', None)


def column_verdict(X, exact_invariant_if_constant=False):
    """X (C chains, M rows) of one column. Returns S4 status (R-LIT) and the R-MA verdict."""
    X = np.asarray(X, dtype=np.float64); C, M = X.shape; blen = M // N_BATCH
    rs, rv = rhat(X)
    if rs == 'constant':
        st = 'exact_invariant' if exact_invariant_if_constant else 'unassessable'
        return {'status_lit': st, 'status_ma': st, 'rhat': None, 'tau': [None] * C, 'tau_pooled': None,
                'lit_pass': st == 'exact_invariant', 'ma_pass': st == 'exact_invariant', 'rhat_pass': True, 'lit_tau_pass': True}
    status = 'passed'
    if rs == 'unassessable': status = 'unassessable'
    elif rs == 'failed' or rv > RHAT_MAX: status = 'failed'
    rhat_ok = rs == 'assessed' and rv <= RHAT_MAX
    taus = []; tau_ok = True; tau_unass = False
    for c in range(C):
        ts, t = sokal_tau(X[c]); taus.append(t)
        if ts == 'assessed':
            if blen < RATIO_MIN * t: status = 'failed'; tau_ok = False
        else:
            tau_unass = True
            if status != 'failed': status = 'unassessable'
    ps, tp = pooled_acf_tau(X)
    ma_tau = ps == 'assessed' and blen >= RATIO_MIN * tp and all(t is not None and blen >= RATIO_MIN * t / MA_GUARD for t in taus)
    ma = 'passed' if (rhat_ok and ma_tau) else ('failed' if (rs == 'failed' or (rv is not None and rv > RHAT_MAX) or (ps == 'assessed' and not ma_tau)) else 'unassessable')
    return {'status_lit': status, 'status_ma': ma, 'rhat': rv, 'tau': taus, 'tau_pooled': tp,
            'lit_pass': status == 'passed', 'ma_pass': ma == 'passed', 'rhat_pass': rhat_ok, 'lit_tau_pass': tau_ok and not tau_unass}


def flat_quarters(x):
    """PREREG section 2: max_j |Q_j - xbar| <= 2.91 sqrt(2 tau s^2 / (n/4)); unassessable tau fails."""
    x = np.asarray(x, dtype=np.float64); n = x.shape[0]; q = n // 4
    ts, t = sokal_tau(x)
    Q = [float(x[j * q:(j + 1) * q].mean()) for j in range(4)]; xb = float(x[:4 * q].mean())
    if ts != 'assessed':
        return {'flat': ts == 'constant', 'tau': t, 'quarter_means': Q, 'mean': xb, 'max_dev_over_se': None}
    se = math.sqrt(2.0 * t * float(np.var(x)) / q); dev = max(abs(v - xb) for v in Q)
    return {'flat': dev <= FLAT_FACTOR * se, 'tau': t, 'quarter_means': Q, 'mean': xb, 'se_q': se, 'max_dev_over_se': dev / se}


def flat_quarters_wc(x, c=C_WIN):
    """ADDENDUM FQ-WC (calib/calib_flat_v003.py): within-quarter SE with the first-order demeaning-bias correction."""
    x = np.asarray(x, dtype=np.float64); q = x.shape[0] // 4
    Q = np.array([x[j * q:(j + 1) * q].mean() for j in range(4)]); r = x[:4 * q] - np.repeat(Q, q)
    ts, tw = sokal_tau(r)
    if ts != 'assessed' or 2 * c * tw >= q:
        return {'flat': False, 'tau_w': tw, 'max_dev_over_se': None}
    tc = tw / (1 - 2 * c * tw / q); s2 = float(np.var(r)) / (1 - 2 * tc / q)
    if not (s2 > 0 and tc > 0): return {'flat': False, 'tau_w': tw, 'max_dev_over_se': None}
    se = math.sqrt(2 * tc * s2 / q); dev = float(np.max(np.abs(Q - Q.mean())))
    return {'flat': dev <= FLAT_FACTOR * se, 'tau_w': tw, 'tau_c': tc, 'se_q': se, 'max_dev_over_se': dev / se}


def split_rhat(X, parts=4):
    """ADDENDUM descriptive: Rhat over the parts x C contiguous segments of every chain (split-Rhat)."""
    X = np.asarray(X, dtype=np.float64); C, n = X.shape; m = n // parts
    return rhat(X[:, :parts * m].reshape(C * parts, m))


# ---------------- capture loading ----------------
def load_capture(capdir, keys):
    """Returns {chain_id: {key: array sorted by measurement_id}} from durability V002 blocks."""
    files = sorted(glob.glob(os.path.join(capdir, 'block_*.npz'))); parts = {}
    for f in files:
        with np.load(f) as z:
            for k in set(keys) | {'chain_id', 'measurement_id'}:
                parts.setdefault(k, []).append(z[k])
    arr = {k: np.concatenate(v) for k, v in parts.items()}; out = {}
    for ch in sorted(set(arr['chain_id'].tolist())):
        sel = np.flatnonzero(arr['chain_id'] == ch); order = sel[np.argsort(arr['measurement_id'][sel], kind='stable')]
        d = {k: v[order] for k, v in arr.items()}
        if not np.array_equal(d['measurement_id'], np.arange(order.size)): raise ValueError('non-contiguous measurement ids in ' + capdir)
        out[ch] = d
    return out, files


def iter_keys(files, chain_id):
    """Yields (measurement_id, seven-int key) per row, block by block (low memory)."""
    for f in files:
        with np.load(f) as z:
            cid, mid, kb, kn = z['chain_id'], z['measurement_id'], z['reference_key_bytes'], z['reference_key_nbytes']
            for r in range(cid.shape[0]):
                if int(cid[r]) == chain_id:
                    yield int(mid[r]), tuple(int.from_bytes(bytes(kb[r, fld, :int(kn[r, fld])]), 'little') for fld in range(7))


def int_bits(x, n):
    nb = (n + 7) // 8
    return np.unpackbits(np.frombuffer(int(x).to_bytes(nb, 'little'), dtype=np.uint8), bitorder='little')[:n].astype(bool)


# ---------------- blocks (S4 LK3 / _allk_analyze) ----------------
def blocks_meta(md):
    out = []
    for b in md['blocks']:
        pv = np.asarray(b['profile_values'], float); d = int(b.get('dimension', 10 * pv.shape[0]))
        assert d == 10 * pv.shape[0]
        nn = list(b.get('nn_positions', [0] if d == 10 else [0, 10]))
        out.append({'index': b['index'], 'k': tuple(b['k']), 'pv': pv, 'd': d, 'nn': nn,
                    'off': int(b['contact_offset']), 'ent': [tuple(e) for e in b['contact_entries']]})
    return out


MAND = np.ones(10); MAND[7:10] = np.sqrt(2.0)


def block_scores(score_cells, n_cells, blk):
    sc = score_cells.reshape(-1, n_cells, 10) * MAND
    return np.einsum('pc,mcf->mpf', blk['pv'], sc, optimize=False).reshape(sc.shape[0], -1)


def block_contacts(allk_contacts, blk):
    return np.asarray(allk_contacts[:, blk['off']:blk['off'] + len(blk['ent'])], dtype=np.float64)


# ---------------- estimates, grid, gate (b7) ----------------
def sums_for(X, Tcols, blk):
    """Plug-in sums of one block over rows: (n, sum s, s^T s, T matrix)."""
    T = np.zeros((blk['d'], blk['d']))
    for col, (pa, pb) in enumerate(blk['ent']):
        v = float(Tcols[:, col].sum()); ia, ib = blk['nn'][pa], blk['nn'][pb]; T[ia, ib] = v; T[ib, ia] = v
    return (X.shape[0], X.sum(0), X.T @ X, T)


def estimate(sum_list, nblk):
    o = []
    for bi in range(nblk):
        n = sum(s[bi][0] for s in sum_list); S = sum(s[bi][1] for s in sum_list); SS = sum(s[bi][2] for s in sum_list); T = sum(s[bi][3] for s in sum_list)
        g = S / n; cov = SS / n - np.outer(g, g); o.append({'H': cov + T / n, 'T': T / n, 'g': g})
    return o


def grid_arr(BLK, Hs, L, beta=1.0):
    C = L ** 3; g = np.zeros((L, L, L, 10, 10), complex)
    for b, e in zip(BLK, Hs):
        F = -e['H'] / beta; k = b['k']; partner = tuple((-v) % L for v in k)
        if k == partner: h = F / C + 0j
        else:
            S = C / 2; cc, cs, scb, ss = F[:10, :10] / S, F[:10, 10:] / S, F[10:, :10] / S, F[10:, 10:] / S
            h = (cc + ss) / 2 + 1j * (cs - scb) / 2
        g[k] = h
        if k != partner: g[partner] = h.conj()
    return g


def gate(BLK, Hs, L, tol=1e-10):
    nb = 0; lmin = np.inf; schur = np.inf; vk = []; singular = 0
    for b, e in zip(BLK, Hs):
        H = e['H']; w = np.linalg.eigvalsh(0.5 * (H + H.T)); sc = max(1.0, float(np.abs(w).max()))
        if w[0] < -tol * sc: nb += 1; vk.append(b['k'])
        lmin = min(lmin, float(w[0])); jj = [i for i in range(b['d']) if i not in b['nn']]; nn = b['nn']
        try:
            Sch = H[np.ix_(nn, nn)] - H[np.ix_(nn, jj)] @ np.linalg.solve(H[np.ix_(jj, jj)], H[np.ix_(jj, nn)])
            schur = min(schur, float(np.linalg.eigvalsh(0.5 * (Sch + Sch.T))[0]))
        except np.linalg.LinAlgError:
            singular += 1
    g = grid_arr(BLK, Hs, L); nv = 0; lmax = -np.inf; gnn = np.inf; ng = 0
    for k in np.ndindex(L, L, L):
        hh = 0.5 * (g[k] + g[k].conj().T); w = np.linalg.eigvalsh(hh); sc = max(1.0, float(np.abs(w).max()))
        if w[-1] > tol * sc: nv += 1
        lmax = max(lmax, float(w[-1])); Fjj = hh[1:, 1:]
        try:
            G = float(np.real(-hh[0, 0] + hh[0, 1:] @ np.linalg.solve(Fjj, hh[1:, 0]))); gnn = min(gnn, G); ng += G < 0
        except np.linalg.LinAlgError:
            singular += 1
    return {'blocks_violating': nb, 'violating_k': vk, 'min_lambda_min_d2logZ': lmin, 'min_lapse_schur': schur,
            'grid_nodes_violating': nv, 'max_lambda_max_h': lmax, 'min_Gamma_nn': gnn, 'n_Gamma_nn_negative': int(ng), 'singular_solves': singular}


def violates(g): return g['blocks_violating'] > 0 or g['grid_nodes_violating'] > 0 or g['singular_solves'] > 0


def rel(a, b, L):
    r = np.array([np.linalg.norm(a[i] - b[i]) / np.linalg.norm(b[i]) for i in np.ndindex(L, L, L)])
    return {'global': float(np.linalg.norm(a - b) / np.linalg.norm(b)), 'nodewise_median': float(np.median(r)), 'nodewise_max': float(r.max()),
            'k0_node': float(r[0])}


# ---------------- background C-bar and anisotropy ----------------
def cbar_from_mean_row(bg_mean, n_cells):
    a = np.asarray(bg_mean, float) / n_cells; mu = a[:3]; M = np.zeros((3, 3))
    for p, (i, j) in enumerate(((0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)), 3): M[i, j] = M[j, i] = a[p]
    return M - np.outer(mu, mu)


def s_vec(C): return np.array([C[0, 0] - C[1, 1], 2 * C[0, 1]]) / (C[0, 0] + C[1, 1])


def axis_deg(C):
    w, V = np.linalg.eigh(C[:2, :2]); maj = V[:, 1]; return float(math.degrees(math.atan2(maj[1], maj[0])) % 180.0)


def uniax(C, a):
    i = 'xyz'.index(a); o = [j for j in range(3) if j != i]
    return float((C[i, i] - (C[o[0], o[0]] + C[o[1], o[1]]) / 2) / (np.trace(C) / 3))


def memory_test(Cs, axes):
    """PREREG section 4: exact randomization over all 3^n reassignments of start axes, plus m = #(largest diag == start axis)."""
    import itertools
    n = len(Cs); obs = float(np.mean([uniax(C, a) for C, a in zip(Cs, axes)]))
    U = np.array([[uniax(C, a) for a in 'xyz'] for C in Cs]); cnt = 0; tot = 0
    for assign in itertools.product(range(3), repeat=n):
        tot += 1; cnt += float(np.mean([U[i, assign[i]] for i in range(n)])) >= obs - 1e-15
    m = sum(1 for C, a in zip(Cs, axes) if 'xyz'[int(np.argmax(np.diag(C)))] == a)
    from math import comb
    p_m = sum(comb(n, j) * (1 / 3) ** j * (2 / 3) ** (n - j) for j in range(m, n + 1))
    return {'U_bar': obs, 'u_per_chain': [float(U[i, 'xyz'.index(a)]) for i, a in enumerate(axes)], 'p_randomization': cnt / tot,
            'assignments': tot, 'm_largest_diag_equals_start_axis': m, 'p_m_ge_observed_binomial': p_m}


def overlap_memory_test(C_chain, C_start):
    """ADDENDUM A2: mean cosine between traceless parts of chain and start C-bar; exact permutation p over n! pairings."""
    import itertools
    dev = lambda C: (C - np.trace(C) / 3 * np.eye(3)).ravel()
    A = [dev(C) for C in C_chain]; B = [dev(C) for C in C_start]
    cos = np.array([[float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))) for b in B] for a in A])
    n = len(A); obs = float(np.mean([cos[i, i] for i in range(n)])); cnt = 0; tot = 0
    for perm in itertools.permutations(range(n)):
        tot += 1; cnt += float(np.mean([cos[i, perm[i]] for i in range(n)])) >= obs - 1e-15
    return {'mean_cos_chain_vs_own_start': obs, 'cos_per_chain': [float(cos[i, i]) for i in range(n)], 'p_permutation': cnt / tot, 'permutations': tot}
