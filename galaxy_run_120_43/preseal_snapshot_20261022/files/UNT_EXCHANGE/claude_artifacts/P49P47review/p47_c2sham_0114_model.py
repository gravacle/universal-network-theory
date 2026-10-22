"""Claude reviewer's own implementation of canonical #7+admission on the N2
four-parallel-channel quotient (old) and its one-Born join, written from the
TEXT of the operator rules (no Codex code imported or executed).

State = (sector, inc, p, q, r, s); sector 0 old (V=2, E=4), 1 Born (V=4, E=8).
Old edges: e=0..3 all (0,1). All four cut. Born edges: 2e=(0,3), 2e+1=(2,1).
Hopping channel T_e = phi_e b_u^dag b_v + conj(phi_e) b_v^dag b_u, H term -t T_e.
"""
from fractions import Fraction as F

OLD_V, OLD_E = 2, 4
BORN_V, BORN_E = 4, 8
OLD_EDGES = [(0, 1)] * 4
BORN_EDGES = []
for _e in range(4):
    BORN_EDGES += [(0, 3), (2, 1)]
CUTS = (0, 1, 2, 3)


def pc(x):
    return bin(x).count('1')


class G:
    """Gaussian rational."""
    __slots__ = ('re', 'im')

    def __init__(self, re=0, im=0):
        self.re = F(re)
        self.im = F(im)

    def __add__(self, o):
        o = cg(o)
        return G(self.re + o.re, self.im + o.im)
    __radd__ = __add__

    def __sub__(self, o):
        o = cg(o)
        return G(self.re - o.re, self.im - o.im)

    def __neg__(self):
        return G(-self.re, -self.im)

    def __mul__(self, o):
        o = cg(o)
        return G(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)
    __rmul__ = __mul__

    def conj(self):
        return G(self.re, -self.im)

    def __eq__(self, o):
        o = cg(o)
        return self.re == o.re and self.im == o.im

    def __hash__(self):
        return hash((self.re, self.im))

    def __bool__(self):
        return bool(self.re or self.im)

    def __repr__(self):
        return f"({self.re}{'+' if self.im >= 0 else ''}{self.im}i)"

    def c(self):
        return complex(float(self.re), float(self.im))


def cg(x):
    return x if isinstance(x, G) else G(x)


def graph(sector):
    return (OLD_V, OLD_E, OLD_EDGES) if sector == 0 else (BORN_V, BORN_E, BORN_EDGES)


def degrees(sector, inc):
    V, E, edges = graph(sector)
    d = [0] * V
    for e, (u, v) in enumerate(edges):
        if (inc >> e) & 1:
            d[u] += 1
            d[v] += 1
    return d


def birth_encode(inc_old):
    a = 0
    for e in CUTS:
        if (inc_old >> e) & 1:
            a |= (1 << (2 * e)) | (1 << (2 * e + 1))
    return a


def T(state):
    sec, inc, p, q, r, s = state
    assert sec == 0
    if sum((inc >> e) & 1 for e in CUTS) != 2:
        return None
    return (1, birth_encode(inc), p, q, r, s)


def Tdag(state):
    sec, inc, p, q, r, s = state
    assert sec == 1
    if any(x >> OLD_V for x in (p, q, r, s)):
        return None
    n = 0
    for e in CUTS:
        x = (inc >> (2 * e)) & 1
        y = (inc >> (2 * e + 1)) & 1
        if x != y:
            return None
        n |= x << e
    if sum((n >> e) & 1 for e in CUTS) != 2:
        return None
    return (0, n, p, q, r, s)


def owners(state, P):
    """Yield (owner, index, target, amplitude) for H[target, state]."""
    sec, inc, p, q, r, s = state
    V, E, edges = graph(sec)
    d = degrees(sec, inc)
    dg = (P['Delta'] * pc(inc)
          + P['Ud'] * sum((x - P['dstar']) ** 2 for x in d)
          + P['epsilon_c'] * pc(p) + P['epsilon_r'] * pc(q)
          - P['lambda_R'] * sum(d[v] * ((q >> v) & 1) for v in range(V))
          + P['lambda_J'] * sum(d[v] * ((p >> v) & 1) for v in range(V))
          + P['E_I'] * (V - pc(r | s)) + P['E_R'] * pc(r) + P['E_S'] * pc(s)
          + P['offset'])
    yield ('diag', 0, state, cg(dg))
    phases = P['old_phase'] if sec == 0 else P['born_phase']
    for e, (u, v) in enumerate(edges):
        yield ('flip', e, (sec, inc ^ (1 << e), p, q, r, s), cg(-P['h']))
        pu, pv = (p >> u) & 1, (p >> v) & 1
        if (inc >> e) & 1 and pu != pv:
            amp = -P['t'] * (phases[e].conj() if pu else phases[e])
            yield ('hop', e, (sec, inc, p ^ (1 << u) ^ (1 << v), q, r, s), amp)
    for v in range(V):
        if (p >> v) & 1:
            yield ('bind', v, (sec, inc, p, q ^ (1 << v), r, s), cg(P['g']))
        if (r >> v) & 1 and not (p >> v) & 1:
            yield ('adm_f', v, (sec, inc, p | (1 << v), q, r ^ (1 << v), s | (1 << v)), P['kappa'][v])
        if (s >> v) & 1 and (p >> v) & 1:
            yield ('adm_r', v, (sec, inc, p ^ (1 << v), q, r | (1 << v), s ^ (1 << v)), P['kappa'][v].conj())
    if sec == 0:
        tg = T(state)
        if tg is not None:
            yield ('birth', 0, tg, P['epsilon_B'])
    else:
        tg = Tdag(state)
        if tg is not None:
            yield ('unbirth', 0, tg, P['epsilon_B'].conj())


def column(state, P):
    out = {}
    for _, _, tg, a in owners(state, P):
        out[tg] = out.get(tg, G()) + a
    return {k: v for k, v in out.items() if v}


# C2 action
def perm_bits(x, perm):
    y = 0
    for i, j in enumerate(perm):
        if (x >> i) & 1:
            y |= 1 << j
    return y


SITE_PERM = {0: (1, 0), 1: (1, 0, 3, 2)}
BORN_EDGE_PERM = tuple(2 * (k // 2) + (1 - k % 2) for k in range(8))  # 2e<->2e+1
OLD_EDGE_PERM = (0, 1, 2, 3)


def U(state, born_edge_perm=BORN_EDGE_PERM):
    sec, inc, p, q, r, s = state
    sp = SITE_PERM[sec]
    ep = OLD_EDGE_PERM if sec == 0 else born_edge_perm
    return (sec, perm_bits(inc, ep), perm_bits(p, sp), perm_bits(q, sp), perm_bits(r, sp), perm_bits(s, sp))


def owner_index_map(owner, sec, idx, born_edge_perm=BORN_EDGE_PERM):
    if owner in ('flip', 'hop'):
        return (OLD_EDGE_PERM if sec == 0 else born_edge_perm)[idx]
    if owner in ('bind', 'adm_f', 'adm_r'):
        return SITE_PERM[sec][idx]
    return idx


def sector_states(Aold=(1, 1), Q=1):
    """Fixed per-site active pattern: old A=(1,1); Born A=(1,1,0,0)."""
    out = []
    for sec in (0, 1):
        V, E, _ = graph(sec)
        act = [v for v in range(V) if v < 2 and Aold[v]]
        for inc in range(1 << E):
            for p in range(1 << V):
                for q in range(1 << V):
                    for rmask in range(1 << len(act)):
                        r = sum(1 << act[i] for i in range(len(act)) if (rmask >> i) & 1)
                        s = sum(1 << v for v in act) ^ r
                        if pc(p) + pc(r) == Q:
                            out.append((sec, inc, p, q, r, s))
    return out


def params(kappa01=G(F(2, 3), F(1, 5)), kappa23=G(F(-1, 7), F(3, 4)), epsB=G(F(1, 2), F(-2, 3)),
           g=F(5, 7), hbar=F(3, 2), real_only=False, **over):
    P = dict(h=F(3, 11), Delta=F(1, 3), Ud=F(2, 9), dstar=F(2), epsilon_c=F(-1, 4), t=F(4, 5),
             epsilon_r=F(1, 6), g=g, lambda_R=F(3, 8), lambda_J=F(-2, 5), E_I=F(7, 10),
             E_R=F(1, 9), E_S=F(-3, 7), offset=F(1, 13), hbar=hbar,
             kappa=[kappa01, kappa01, kappa23, kappa23], epsilon_B=epsB,
             old_phase=[G(1)] * 4, born_phase=[G(1)] * 8)
    if real_only:
        P['kappa'] = [G(k.re) for k in P['kappa']]
        P['epsilon_B'] = G(P['epsilon_B'].re)
    P.update(over)
    return P
