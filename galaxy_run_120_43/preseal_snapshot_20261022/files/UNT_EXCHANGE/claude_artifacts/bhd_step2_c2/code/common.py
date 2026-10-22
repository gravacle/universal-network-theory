"""BH-D step 2: shared graph, read and combination routines (PREREG_BHD_STEP2_V001, 2563b31c).

Read terms: level 0 = pinned step-1 read_terms (F_C on the old graph). Level 1 = rule R1: same six edges
if none is a cut bond, gate from the Born graph's own off-cycle incident edges (children replace cut bonds);
otherwise no level-1 term (F_C = 0 there). Rule R0 = no level-1 terms.
Edges in level-1 terms are labelled ('k', e) for a kept old edge e and ('c', i, j) for child j of cut i.
"""
import sys
from itertools import product
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/pinned')
from graph_roster import roster, graph  # noqa: E402
from bhd_step1_coeffs import read_terms, series, free_factor, pmul, cadd, cmul, CZ, C1  # noqa: E402
import canonical_join_backend_v002 as BK  # noqa: E402


def setup(L):
    meta, cycles = roster(L)
    _, _, edges, inc = graph(L)
    w0 = {e: 0 for e in edges}; w0[meta['e_vu']] = 1; w0[meta['e_ab']] = 1
    ends = {e: (x, y) for e, (x, y, s) in edges.items()}
    old, cuts = BK.periodic_q4(L)
    bm = BK.BirthMap(old, cuts)
    assert list(cuts) == meta['cut_bonds']
    for e in edges:
        assert old.edges[e] == ends[e]
    born_inc = {}
    for e in bm.keep:
        for x in ends[e]:
            born_inc.setdefault(x, []).append(('k', e))
    for i, e in enumerate(cuts):
        a_i, b_i = ends[e]
        born_inc.setdefault(a_i, []).append(('c', i, 0)); born_inc.setdefault(bm.star_B, []).append(('c', i, 0))
        born_inc.setdefault(bm.star_A, []).append(('c', i, 1)); born_inc.setdefault(b_i, []).append(('c', i, 1))
    return dict(meta=meta, cycles=cycles, edges=edges, inc=inc, w0=w0, ends=ends, cuts=list(cuts), bm=bm,
                born_inc=born_inc)


def read_terms_R1(cyc, G):
    es, vs = cyc['edges'], cyc['vertices']
    if set(es) & set(G['cuts']):
        return []
    cyck = {('k', e) for e in es}
    gate = sorted({f for x in vs for f in G['born_inc'][x] if f not in cyck}, key=str)
    a = [1, 0, 1, 0, 1, 0]
    b = [1 - t for t in a]
    configs = []
    for bits in product((0, 1), repeat=len(gate)):
        occ = dict(zip(gate, bits))
        if all(sum(occ[f] for f in G['born_inc'][x] if f not in cyck) == 1 for x in vs):
            configs.append(occ)
    terms = []
    for (Lw, Rw) in ((a, b), (b, a)):
        cyc_ops = {('k', e): 'S%d%d' % (Lw[i], Rw[i]) for i, e in enumerate(es)}
        for occ in configs:
            t = dict(cyc_ops)
            t.update({f: 'P%d' % occ[f] for f in gate})
            terms.append(t)
    return terms


def level0_as_labelled(terms):
    return [{('k', e): op for e, op in t.items()} for t in terms]


def ext_poly(term, cl_edges, G, D, S, cutblock, level, free_cache):
    """External factor of one labelled term at `level`: product of free-edge series (h only) times the
    cut-block factor (h, e). Returns {(m, edeg): complex Fraction} with m <= D.
    level 0: cut bonds ('k', cut) go to the cut block; level 1: children ('c', i, j) go to it.
    If cutblock is None (epsilon^0 families) cut bonds are ordinary free edges at level 0."""
    cutpos = {e: i for i, e in enumerate(G['cuts'])}
    clset = {('k', e) for e in cl_edges}
    free_key, bitops = [], []
    for lab, op in term.items():
        if lab in clset:
            continue
        if lab[0] == 'c':
            assert level == 1 and cutblock is not None
            bitops.append((2 * lab[1] + lab[2], op))
        elif cutblock is not None and lab[1] in cutpos:
            assert level == 0
            bitops.append((cutpos[lab[1]], op))
        else:
            free_key.append((G['w0'][lab[1]], op))
    fk = (tuple(sorted(free_key)), D)
    if fk not in free_cache:
        poly = [C1] + [CZ] * D
        for (n, op) in fk[0]:
            poly = pmul(poly, free_factor(n, op, D, S), D)
        free_cache[fk] = poly
    poly = free_cache[fk]
    if cutblock is None:
        return {(m, 0): x for m, x in enumerate(poly) if x != CZ}
    K = cutblock.expect(level, bitops)
    out = {}
    for (m3, ed), kv in K.items():
        for m2 in range(0, D + 1 - m3):
            f = poly[m2]
            if f == CZ:
                continue
            k = (m2 + m3, ed)
            out[k] = cadd(out.get(k, CZ), cmul(f, kv))
    return out


def arm_series(terms, cl, cl_edges, G, D, S, cutblock, level, free_cache, extra_cache=None):
    """sum over labelled terms of cluster(term) * ext(term); returns {(m, a, b, ..., edeg): complex Fr}."""
    by_op = {}
    clmap = [('k', e) for e in cl_edges]
    for t in terms:
        edge_ops = tuple(t.get(lab, 'I') for lab in clmap)
        ext = ext_poly(t, cl_edges, G, D, S, cutblock, level, free_cache)
        acc = by_op.setdefault(edge_ops, {})
        for k, x in ext.items():
            acc[k] = cadd(acc.get(k, CZ), x)
    out = {}
    for edge_ops, ext in by_op.items():
        if not ext:
            continue
        K = cl.expect(list(edge_ops))
        for sig, kv in K.items():
            if sig[0] > D:
                continue
            for (m2, ed), f in ext.items():
                if sig[0] + m2 > D or f == CZ:
                    continue
                tot = (sig[0] + m2,) + tuple(sig[1:]) + (ed,)
                out[tot] = cadd(out.get(tot, CZ), cmul(f, kv))
    return {k: x for k, x in out.items() if x != CZ}


def sub(A, B):
    out = {}
    for k in set(A) | set(B):
        x = A.get(k, CZ); y = B.get(k, CZ)
        z = (x[0] - y[0], x[1] - y[1])
        if z != CZ:
            out[k] = z
    return out


def add(A, B):
    out = dict(A)
    for k, y in B.items():
        z = cadd(out.get(k, CZ), y)
        if z != CZ:
            out[k] = z
        else:
            out.pop(k, None)
    return out


def fmt(x):
    return {'re': str(x[0]), 'im': str(x[1])}
