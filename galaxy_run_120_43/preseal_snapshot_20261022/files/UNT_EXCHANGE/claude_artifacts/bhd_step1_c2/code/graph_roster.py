"""BH-D step 1: graph-only roster of simple six-cycles touching the writer/control sites.

Graph-only. Reads no response, runs no dynamics. Indexing follows
FIRST_CHUNK_PREMISE_CARD_V006.md Packet A (A(r)=idx(r), B(r)=L^3+idx(r),
bond 4*idx(r)+s joins A(r) to B(r+e_s)); W/C sites follow
NATIVE_WRITE_EVACUATION_INTERFACE_PROPOSED_V002.md:19 (v=A(1,1,1), u=B(1,1,1),
a=A(1,1,0), b=B(1,1,0); initially n_vu=n_ab=1, all other n_e=0).
"""
from fractions import Fraction as Fr
from itertools import product
import json, sys

DELTA = [(Fr(1, 4), Fr(1, 4), Fr(1, 4)), (Fr(1, 4), Fr(-1, 4), Fr(-1, 4)),
         (Fr(-1, 4), Fr(1, 4), Fr(-1, 4)), (Fr(-1, 4), Fr(-1, 4), Fr(1, 4))]
STEP = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]


def graph(L):
    idx = lambda r: L * L * (r[0] % L) + L * (r[1] % L) + (r[2] % L)
    nA = L ** 3
    edges = {}  # e -> (A, B, s)
    for r in product(range(L), repeat=3):
        for s in range(4):
            rb = tuple(r[i] + STEP[s][i] for i in range(3))
            edges[4 * idx(r) + s] = (idx(r), nA + idx(rb), s)
    inc = {}
    for e, (x, y, s) in edges.items():
        inc.setdefault(x, []).append(e)
        inc.setdefault(y, []).append(e)
    return idx, nA, edges, inc


def other(edges, e, x):
    a, b, _ = edges[e]
    return b if x == a else a


def disp(edges, e, frm):
    a, b, s = edges[e]
    d = DELTA[s]
    return d if frm == a else tuple(-t for t in d)


def six_cycles(edges, inc):
    """All simple 6-cycles as frozensets of edges, with one cyclic edge order."""
    found = {}
    for start in sorted(inc):
        def walk(path_v, path_e):
            x = path_v[-1]
            for e in inc[x]:
                if path_e and e == path_e[-1]:
                    continue
                y = other(edges, e, x)
                if len(path_e) == 5:
                    if y == start and e not in path_e:
                        es = path_e + [e]
                        key = frozenset(es)
                        if len(key) == 6 and key not in found:
                            found[key] = (list(path_v), es)
                    continue
                if y in path_v or e in path_e:
                    continue
                walk(path_v + [y], path_e + [e])
        walk([start], [])
    return found


def roster(L):
    idx, nA, edges, inc = graph(L)
    v, u, a, b = idx((1, 1, 1)), nA + idx((1, 1, 1)), idx((1, 1, 0)), nA + idx((1, 1, 0))
    e_vu = 4 * idx((1, 1, 1)) + 0
    e_ab = 4 * idx((1, 1, 0)) + 0
    assert edges[e_vu][:2] == (v, u) and edges[e_ab][:2] == (a, b)
    w0 = {e: 0 for e in edges}
    w0[e_vu] = 1
    w0[e_ab] = 1
    Ev, Ea = set(inc[v]), set(inc[a])
    cuts = [4 * idx(r) + 0 for r in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]]
    out = []
    for key, (vs, es) in six_cycles(edges, inc).items():
        cyc = set(es)
        gate = sorted({f for x in vs for f in inc[x] if f not in cyc})
        supp = cyc | set(gate)
        if not (supp & (Ev | Ea)):
            continue
        tot = [Fr(0)] * 3
        for x, e in zip(vs, es):
            d = disp(edges, e, x)
            tot = [tot[i] + d[i] for i in range(3)]
        contractible = all(t == 0 for t in tot)
        # minimal pure-incidence flip degree for nonzero <F_C>: 6 + 2*min gate distance
        best = None
        for bits in product((0, 1), repeat=len(gate)):
            occ = dict(zip(gate, bits))
            if all(sum(occ[f] for f in inc[x] if f not in cyc) == 1 for x in vs):
                dist = sum(1 for f in gate if occ[f] != w0[f])
                best = dist if best is None else min(best, dist)
        out.append({
            'L': L, 'vertices': vs, 'edges': es, 'gate_edges': gate,
            'contains_v': v in vs, 'contains_a': a in vs, 'contains_u': u in vs, 'contains_b': b in vs,
            'touches_Ev': bool(supp & Ev), 'touches_Ea': bool(supp & Ea),
            'Ev_on_cycle': sorted(cyc & Ev), 'Ea_on_cycle': sorted(cyc & Ea),
            'contains_cut_bond': bool(cyc & set(cuts)), 'gate_contains_cut_bond': bool(set(gate) & set(cuts)),
            'displacement_sum_cubic': [str(t) for t in tot], 'contractible': contractible,
            'm_min_pure_incidence': None if best is None else 6 + 2 * best,
        })
    out.sort(key=lambda c: (not c['contains_v'], not c['contains_a'], c['m_min_pure_incidence'] or 99, c['edges']))
    meta = {'L': L, 'v': v, 'u': u, 'a': a, 'b': b, 'e_vu': e_vu, 'e_ab': e_ab,
            'E_v': sorted(Ev), 'E_a': sorted(Ea), 'cut_bonds': cuts,
            'n_sites': 2 * nA, 'n_bonds': len(edges)}
    return meta, out


if __name__ == '__main__':
    res = {}
    for L in (2, 3, 4):
        meta, cyc = roster(L)
        res[str(L)] = {'meta': meta, 'cycles': cyc}
        print(L, meta['n_sites'], meta['n_bonds'], len(cyc),
              'contains_v', sum(c['contains_v'] for c in cyc),
              'contains_a', sum(c['contains_a'] for c in cyc),
              'noncontractible', sum(not c['contractible'] for c in cyc),
              'm_min set', sorted({c['m_min_pure_incidence'] for c in cyc}))
    json.dump(res, open(sys.argv[1], 'w'), indent=1)
