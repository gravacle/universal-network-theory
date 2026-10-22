"""Claude independent re-implementation (no Codex imports) of canonical #7+admission
on the reviewed N2 four-parallel-channel quotient, fixed Q=1, active mask {0} (M=1).
Checks P49-Qpos-0070 claims: block dimension, reducing fragments, component census,
seed energy mean/variance, third moments, Hermiticity, cancellation robustness,
and the two-level energy-only toy.
"""
import json, sys, random
from fractions import Fraction as F
from itertools import product

# ---------- exact Gaussian rationals as (re, im) ----------
def cadd(a, b): return (a[0] + b[0], a[1] + b[1])
def cmul(a, b): return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def conj(a): return (a[0], -a[1])
def n2(a): return a[0] * a[0] + a[1] * a[1]
def nz(a): return a[0] != 0 or a[1] != 0
Z = (F(0), F(0))

# ---------- geometry (derived here, not copied) ----------
OLD_V, OLD_E = 2, [(0, 1)] * 4
CUTS = (0, 1, 2, 3)
STAR_A, STAR_B = OLD_V, OLD_V + 1
BORN_E, PATHS = [], []
for e in CUTS:
    u, v = OLD_E[e]
    PATHS.append((len(BORN_E), len(BORN_E) + 1))
    BORN_E += [(u, STAR_B), (STAR_A, v)]
BORN_V = 4
GRAPHS = [(OLD_V, OLD_E), (BORN_V, BORN_E)]

def pc(x): return bin(x).count("1")

def degrees(sector, inc):
    nv, E = GRAPHS[sector]
    d = [0] * nv
    for k, (u, v) in enumerate(E):
        if (inc >> k) & 1: d[u] += 1; d[v] += 1
    return d

def encode_inc(n):
    a = 0
    for e, (x, y) in zip(CUTS, PATHS):
        if (n >> e) & 1: a |= (1 << x) | (1 << y)
    return a

def column(st, P):
    sector, inc, p, q, r, s = st
    nv, E = GRAPHS[sector]
    d = degrees(sector, inc)
    R = P["real"]
    diag = (R["Delta"] * pc(inc) + R["Ud"] * sum((x - P["dstar"]) ** 2 for x in d)
            + R["epsilon_c"] * pc(p) + R["epsilon_r"] * pc(q)
            - R["lambda_R"] * sum(d[v] * ((q >> v) & 1) for v in range(nv))
            + R["lambda_J"] * sum(d[v] * ((p >> v) & 1) for v in range(nv))
            + R["E_I"] * (nv - pc(r | s)) + R["E_R"] * pc(r) + R["E_S"] * pc(s) + R["identity_offset"])
    out = {}
    def put(tgt, z):
        out[tgt] = cadd(out.get(tgt, Z), z)
    put(st, (diag, F(0)))
    phases = P["old_ph"] if sector == 0 else P["born_ph"]
    for k, (u, v) in enumerate(E):
        put((sector, inc ^ (1 << k), p, q, r, s), (-R["h"], F(0)))
        pu, pv = (p >> u) & 1, (p >> v) & 1
        if (inc >> k) & 1 and pu != pv:
            ph = conj(phases[k]) if pu else phases[k]
            put((sector, inc, p ^ (1 << u) ^ (1 << v), q, r, s), cmul((-R["t"], F(0)), ph))
    for v in range(nv):
        if (p >> v) & 1: put((sector, inc, p, q ^ (1 << v), r, s), (R["g"], F(0)))
        if (r >> v) & 1 and not (p >> v) & 1:
            put((sector, inc, p | (1 << v), q, r ^ (1 << v), s | (1 << v)), P["kappa"][v])
        if (s >> v) & 1 and (p >> v) & 1:
            put((sector, inc, p ^ (1 << v), q, r | (1 << v), s ^ (1 << v)), conj(P["kappa"][v]))
    if sector == 0:
        if sum((inc >> e) & 1 for e in CUTS) == 2:
            put((1, encode_inc(inc), p, q, r, s), P["epsB"])
    else:
        if not any(x >> OLD_V for x in (p, q, r, s)):
            n, ok = 0, True
            for e, (x, y) in zip(CUTS, PATHS):
                bx, by = (inc >> x) & 1, (inc >> y) & 1
                if bx != by: ok = False; break
                n |= bx << e
            if ok and sum((n >> e) & 1 for e in CUTS) == 2:
                put((0, n, p, q, r, s), conj(P["epsB"]))
    return {k: z for k, z in out.items() if nz(z)}

def basis():
    states = []
    for sector, (nv, E) in enumerate(GRAPHS):
        configs = []
        for v in range(nv): configs.append((1 << v, 0, 1))  # carrier, Spent0
        configs.append((0, 1, 0))                            # no carrier, Ready0
        for inc in range(1 << len(E)):
            for (p, r, s) in configs:
                for q in range(1 << nv):
                    states.append((sector, inc, p, q, r, s))
    return states

def label(st):
    sector, inc, p, q, r, s = st
    if sector != 1 or (r | s) != 1: return None
    if pc(p) + pc(r) != 1: return None
    right = (1 << 1) | (1 << 2)
    if p & right or r & right or not q & (1 << 2): return None
    return (q >> 1) & 1

def run(P, tag):
    states = basis()
    idx = {s: i for i, s in enumerate(states)}
    assert len(idx) == len(states)
    cols = []
    escape_domain = 0
    for s in states:
        c = column(s, P)
        for t in c:
            if t not in idx: escape_domain += 1
        cols.append({idx[t]: z for t, z in c.items() if t in idx})
    herm_fail = sum(1 for i, c in enumerate(cols) for j, z in c.items() if cols[j].get(i, Z) != conj(z))
    # union-find components
    par = list(range(len(states)))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for i, c in enumerate(cols):
        for j in c:
            a, b = f(i), f(j)
            if a != b: par[a] = b
    comps = {}
    for i in range(len(states)): comps.setdefault(f(i), []).append(i)
    comp_list = sorted(comps.values(), key=lambda m: (-len(m), m[0]))
    # fragment checks
    frag = {0: set(), 1: set()}
    for i, s in enumerate(states):
        l = label(s)
        if l is not None: frag[l].add(i)
    escapes = sum(1 for b in (0, 1) for i in frag[b] for j in cols[i] if j not in frag[b])
    frag_is_component = {b: any(set(m) == frag[b] for m in comp_list) for b in (0, 1)}
    # component census: size, sector content, frozen old q word?
    census = []
    for m in comp_list:
        sec = sorted(set(states[i][0] for i in m))
        words = sorted(set((states[i][3] & 1, (states[i][3] >> 1) & 1) for i in m))
        q2q3 = sorted(set(((states[i][3] >> 2) & 1, (states[i][3] >> 3) & 1) for i in m))
        census.append(dict(size=len(m), sectors=sec, old_q0q1_words=len(words),
                           old_q1_frozen=len(set(w[1] for w in words)) == 1,
                           q2q3_words=len(q2q3), contains_label=sorted(set(str(label(states[i])) for i in m))))
    # seed moments
    seeds = {"A": (1, 0, 1, 5, 0, 1), "B": (1, 0, 1, 6, 0, 1)}
    R = P["real"]
    kap0 = P["kappa"][0]
    formula_mean = 4 * R["Ud"] * P["dstar"] ** 2 + R["epsilon_c"] + 2 * R["epsilon_r"] + R["E_S"] + 3 * R["E_I"] + R["identity_offset"]
    formula_var = 8 * R["h"] ** 2 + R["g"] ** 2 + n2(kap0)
    seedrows = {}
    for name, s in seeds.items():
        i = idx[s]; c = cols[i]
        mean = c.get(i, Z)
        m2 = sum((n2(z) for z in c.values()), F(0))
        var = m2 - n2(mean)
        # third moment <H^3> = sum_{j,k} conj(H_ji) H_jk H_ki ... compute v=H e_i, then <v|H|v>
        v = c
        Hv = {}
        for j, a in v.items():
            for k, z in cols[j].items():
                Hv[k] = cadd(Hv.get(k, Z), cmul(z, a))
        m3 = Z
        for k, a in v.items():
            m3 = cadd(m3, cmul(conj(a), Hv.get(k, Z)))
        # 4th moment <H^4> = ||H^2 e_i||^2
        m4 = sum((n2(z) for z in Hv.values()), F(0))
        seedrows[name] = dict(index=i, label=label(s), mean=str(mean[0]), mean_im=str(mean[1]),
                              variance=str(var), third_raw_moment=str(m3[0]), fourth_raw_moment=str(m4),
                              offdiag_targets=len(c) - 1)
    out = dict(tag=tag, dimension=len(states), old=sum(1 for s in states if s[0] == 0),
               born=sum(1 for s in states if s[0] == 1), domain_escapes=escape_domain,
               hermitian_mate_failures=herm_fail, n_components=len(comp_list),
               component_sizes=[len(m) for m in comp_list],
               fragment_sizes={b: len(frag[b]) for b in (0, 1)}, fragment_escapes=escapes,
               fragment_is_exact_component=frag_is_component,
               formula_mean=str(formula_mean), formula_variance=str(formula_var),
               seeds=seedrows, census=census)
    return out

def params(rng, phase_mode="generic", lamR=None):
    def r(): return F(rng.randint(-40, 40) or 7, rng.randint(1, 13))
    keys = ('h', 'Delta', 'Ud', 'epsilon_c', 't', 'epsilon_r', 'g', 'lambda_R', 'lambda_J', 'E_I', 'E_R', 'E_S', 'identity_offset')
    real = {k: r() for k in keys}
    if lamR is not None: real["lambda_R"] = F(lamR)
    pyth = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(-8, 17), F(15, 17)), (F(7, 25), F(-24, 25)),
            (F(-20, 29), F(-21, 29)), (F(12, 37), F(35, 37)), (F(9, 41), F(40, 41)), (F(-28, 53), F(45, 53))]
    if phase_mode == "generic":
        old_ph = [pyth[(k + 3) % 8] for k in range(4)]
        born_ph = [pyth[k] for k in range(8)]
    else:  # adversarial: all four L channels (born edges 0,2,4,6) arranged to cancel pairwise
        one, mone = (F(1), F(0)), (F(-1), F(0))
        old_ph = [one, mone, one, mone]
        born_ph = [one, one, mone, one, one, one, mone, one]
    kappa = [(r(), r()) for _ in range(4)]
    return dict(real=real, dstar=r(), kappa=kappa, epsB=(r(), r()), old_ph=old_ph, born_ph=born_ph)

if __name__ == "__main__":
    rng = random.Random(70070)
    results = []
    results.append(run(params(rng, "generic"), "generic_rational_params"))
    results.append(run(params(rng, "cancel"), "adversarial_parallel_hop_cancelling_phases"))
    results.append(run(params(rng, "generic", lamR=0), "generic_lambda_R_zero"))
    # two-level energy-only toy, exact
    H = [[F(0), F(2)], [F(2), F(3)]]
    Pm = [[F(4, 5), F(-2, 5)], [F(-2, 5), F(1, 5)]]
    Pp = [[F(1) - Pm[0][0], -Pm[0][1]], [-Pm[1][0], F(1) - Pm[1][1]]]
    def mm(a, b): return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    def tr(a): return a[0][0] + a[1][1]
    toy = {}
    toy["HPm_eq_-Pm"] = mm(H, Pm) == [[-x for x in row] for row in Pm]
    toy["HPp_eq_4Pp"] = mm(H, Pp) == [[4 * x for x in row] for row in Pp]
    toy["Pm_idempotent"] = mm(Pm, Pm) == Pm
    toy["Pp_given_matches"] = Pp == [[F(1, 5), F(2, 5)], [F(2, 5), F(4, 5)]]
    for nm, rho in (("A", [[F(3, 4), F(3, 16)], [F(3, 16), F(1, 4)]]), ("B", [[F(1, 4), F(-3, 16)], [F(-3, 16), F(3, 4)]])):
        de = [[mm(mm(Pm, rho), Pm)[i][j] + mm(mm(Pp, rho), Pp)[i][j] for j in range(2)] for i in range(2)]
        E = tr(mm(rho, H)); V = tr(mm(rho, mm(H, H))) - E * E
        toy[nm] = dict(q_initial=str(rho[1][1]), det=str(rho[0][0] * rho[1][1] - rho[0][1] ** 2), energy=str(E),
                       variance=str(V), dephased=[[str(x) for x in row] for row in de], q_DE=str(de[1][1]))
    a, g, Om = F(3), F(2), F(5)
    toy["qDE_formula_at_E_3/2"] = str(F(1, 2) + a * (F(3, 2) - a / 2) / Om ** 2)
    toy["ground_q_formula"] = str((1 - a / Om) / 2)
    toy["ground_q_from_Pm"] = str(Pm[1][1])
    # generic-parameter check of q_DE formula on random 2x2 rational preparations
    ok = True
    for _ in range(200):
        a = F(rng.randint(1, 9)); gg = F(rng.choice([3, 4, 6, 8, 12]) * 0 + rng.randint(1, 9))
        # need rational Omega: use pythagorean pair a=k(m^2-n^2), 2g=k*2mn
        m, n = rng.randint(2, 6), 1
        a = F(m * m - n * n); gg = F(m * n); Om = F(m * m + n * n)
        Hg = [[F(0), gg], [gg, a]]
        lam_m = (a - Om) / 2
        # projector onto lam_m eigenvector (x,y): g y = lam_m x -> v = (g, lam_m)
        vx, vy = gg, lam_m; nn = vx * vx + vy * vy
        Pm_ = [[vx * vx / nn, vx * vy / nn], [vx * vy / nn, vy * vy / nn]]
        Pp_ = [[1 - Pm_[0][0], -Pm_[0][1]], [-Pm_[1][0], 1 - Pm_[1][1]]]
        x = F(rng.randint(0, 20), 20); c = F(rng.randint(-5, 5), 20)
        rho = [[1 - x, c], [c, x]]
        E = tr(mm(rho, Hg))
        de11 = mm(mm(Pm_, rho), Pm_)[1][1] + mm(mm(Pp_, rho), Pp_)[1][1]
        if de11 != F(1, 2) + a * (E - a / 2) / Om ** 2: ok = False
    toy["qDE_formula_random_200"] = ok
    json.dump(dict(native=results, toy=toy), sys.stdout, indent=1, default=str)
