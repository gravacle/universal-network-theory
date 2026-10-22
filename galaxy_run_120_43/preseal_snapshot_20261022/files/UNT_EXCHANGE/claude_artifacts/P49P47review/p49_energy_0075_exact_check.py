"""Claude independent exact check of P49-energy-0075 controls and formulas.
Own code; does not import or execute any Codex-authored source.
"""
from fractions import Fraction as F
import json, sys

def Z(n): return [[F(0)]*n for _ in range(n)]
def I(n): return [[F(int(i == j)) for j in range(n)] for i in range(n)]
def mm(a, b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def add(a, b, s=1): return [[x + s*y for x, y in zip(r, q)] for r, q in zip(a, b)]
def sc(a, c): return [[x*c for x in r] for r in a]
def tr(a): return sum((a[i][i] for i in range(len(a))), F(0))
def sub(a, idx): return [[a[i][j] for j in idx] for i in idx]
def fmt(a): return [[str(x) for x in r] for r in a] if isinstance(a, list) else str(a)

def ldl_psd(a):
    """exact PSD test via symmetric Gaussian elimination (own)"""
    a = [r[:] for r in a]
    while a:
        n = len(a)
        if any(a[i][i] < 0 for i in range(n)): return False
        p = next((i for i in range(n) if a[i][i] > 0), None)
        if p is None: return all(v == 0 for r in a for v in r)
        idx = [j for j in range(n) if j != p]; piv = a[p][p]
        a = [[a[j][k] - a[j][p]*a[p][k]/piv for k in idx] for j in idx]
    return True

def check_levels(H, levels):
    n = len(H); tot = Z(n); prev = None
    for e, P in levels:
        assert mm(P, P) == P and P == [list(r) for r in zip(*P)]
        assert mm(H, P) == sc(P, e)
        if prev is not None: assert e > prev
        prev = e; tot = add(tot, P)
    assert tot == I(n)

def dephased_effect(levels, diag):
    n = len(diag); O = [[diag[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    E = Z(n)
    for e, P in levels: E = add(E, mm(mm(P, O), P))
    return E

def decompose(K, C):
    d = len(K); t = tr(K); u = tr(mm(K, K)); v = tr(C); z = tr(mm(K, C)); den = d*u - t*t
    if den: b = (d*z - t*v)/den; a = (v - b*t)/d
    else: b = F(0); a = v/d
    W = add(C, add(sc(I(d), a), sc(K, b)), -1)
    return a, b, W, den

out = {}
# Control 1
H = [[F(0), F(2)], [F(2), F(3)]]
L = [(F(-1), [[F(4,5), F(-2,5)], [F(-2,5), F(1,5)]]), (F(4), [[F(1,5), F(2,5)], [F(2,5), F(4,5)]])]
check_levels(H, L)
E1 = dephased_effect(L, [F(0), F(1)]); E0 = dephased_effect(L, [F(1), F(0)])
a, b, W, den = decompose(H, E1)
assert add(E0, E1) == I(2)
out['control1'] = dict(E_word1=fmt(E1), a=str(a), b=str(b), W=fmt(W), den=str(den),
                       matches_8I_plus_3H_over_25=(E1 == add(sc(I(2), F(8,25)), sc(H, F(3,25)))))
# Control 3: fragment fixture H=diag(0,1,1,2), levels {0},{1,2},{3}
n = 4
def proj(idx): return [[F(int(i == j and i in idx)) for j in range(n)] for i in range(n)]
Hf = [[F((0,1,1,2)[i]) if i == j else F(0) for j in range(n)] for i in range(n)]
Lf = [(F(0), proj({0})), (F(1), proj({1,2})), (F(2), proj({3}))]
check_levels(Hf, Lf)
words = [(0,0), (0,1), (1,0), (1,1)]
res3 = {}
for seed in ([1,2], [0,1,2], [0,1,2,3]):
    K = sub(Hf, seed); d = len(seed); tot = Z(d); rows = {}
    for w in words:
        diag = [F(int(words[i] == w)) for i in range(n)]
        C = sub(dephased_effect(Lf, diag), seed); tot = add(tot, C)
        a, b, W, den = decompose(K, C)
        R = max(sum(abs(x) for x in r) for r in W)
        row = dict(C=fmt(C), a=str(a), b=str(b), W=fmt(W), R=str(R))
        if R:
            eps = F(1, 2*d)/R
            rp = add(sc(I(d), F(1, d)), sc(W, eps)); rm = add(sc(I(d), F(1, d)), sc(W, -eps))
            row.update(rho_plus=fmt(rp), rho_minus=fmt(rm),
                       tr_plus=str(tr(rp)), tr_minus=str(tr(rm)),
                       E_plus=str(tr(mm(rp, K))), E_minus=str(tr(mm(rm, K))),
                       psd_plus=ldl_psd(rp), psd_minus=ldl_psd(rm),
                       floor_plus=ldl_psd(add(rp, sc(I(d), F(-1, 2*d)))), floor_minus=ldl_psd(add(rm, sc(I(d), F(-1, 2*d)))),
                       p_plus=str(tr(mm(rp, C))), p_minus=str(tr(mm(rm, C))),
                       direct_diff=str(tr(mm(rp, C)) - tr(mm(rm, C))), formula_diff=str(2*eps*tr(mm(W, W))),
                       trW=str(tr(W)), trKW=str(tr(mm(K, W))))
        rows['word_%d%d' % w] = row
    assert tot == I(d)
    res3[str(seed)] = dict(K=fmt(K), den=str(decompose(K, K)[3]), words=rows)
out['fragment'] = res3
# Control 4 and 5
def cesaro(levels_e, T, hbar=F(1)):
    m = len(levels_e)
    if m == 1: return None, F(0)
    gap = min(levels_e[i+1] - levels_e[i] for i in range(m-1))
    return gap, min(F(2), 2*hbar*(m-1)/(T*gap))
g, b4 = cesaro([F(-1), F(4)], F(10)); out['control4'] = dict(gap=str(g), trace_bound=str(b4), TV=str(b4/2))
g, b5 = cesaro([F(1)], F(1)); out['control5'] = dict(gap=g, trace_bound=str(b5))
json.dump(out, sys.stdout, indent=1)

# Proposed extra control (Claude): nonscalar K, off-diagonal residual (coherent witness)
u = [[F(1,3), F(2,3), F(2,3)], [F(2,3), F(1,3), F(-2,3)], [F(2,3), F(-2,3), F(1,3)]]
Lc = [(F(e), [[ui*uj for uj in vec] for ui in vec]) for e, vec in zip((0, 1, 2), u)]
Hc = Z(3)
for e, P in Lc: Hc = add(Hc, sc(P, e))
check_levels(Hc, Lc)
seed = [0, 1]; K = sub(Hc, seed); d = 2; prop = dict(H=fmt(Hc), K=fmt(K), words={})
for name, diag in (('word_0', [F(1), F(0), F(0)]), ('word_1', [F(0), F(1), F(1)])):
    C = sub(dephased_effect(Lc, diag), seed); a, b, W, den = decompose(K, C)
    R = max(sum(abs(x) for x in r) for r in W); row = dict(C=fmt(C), a=str(a), b=str(b), W=fmt(W), R=str(R))
    if R:
        eps = F(1, 2*d)/R; rp = add(sc(I(d), F(1, d)), sc(W, eps)); rm = add(sc(I(d), F(1, d)), sc(W, -eps))
        row.update(rho_plus=fmt(rp), rho_minus=fmt(rm), E_plus=str(tr(mm(rp, K))), E_minus=str(tr(mm(rm, K))),
                   psd=[ldl_psd(rp), ldl_psd(rm)], p_plus=str(tr(mm(rp, C))), p_minus=str(tr(mm(rm, C))),
                   diag_plus_equals_diag_minus=all(rp[i][i] == rm[i][i] for i in range(d)))
    prop['words'][name] = row
print('\nPROPOSED_COHERENT_CONTROL', json.dumps(prop))
