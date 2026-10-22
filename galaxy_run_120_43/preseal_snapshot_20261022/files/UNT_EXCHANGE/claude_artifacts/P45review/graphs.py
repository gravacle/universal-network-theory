"""Independent graph builders and ice-state tools (Claude, P45 review).
No Codex code is imported. Plain python3 + fractions.
"""
import random
from itertools import product


def diamond_primitive(L):
    """Diamond on an L x L x L torus of primitive FCC cells (2L^3 vertices).
    A(i,j,k) bonds to B(i,j,k), B(i-1,j,k), B(i,j-1,k), B(i,j,k-1).
    Bond direction labels 0..3 (d0=(1,1,1), d1=(1,-1,-1), d2=(-1,1,-1), d3=(-1,-1,1))."""
    idx = {}
    for i, j, k in product(range(L), repeat=3):
        idx[('A', i, j, k)] = len(idx)
    for i, j, k in product(range(L), repeat=3):
        idx[('B', i, j, k)] = len(idx)
    edges, dirs = [], []
    for i, j, k in product(range(L), repeat=3):
        a = idx[('A', i, j, k)]
        for d, (di, dj, dk) in enumerate([(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]):
            b = idx[('B', (i + di) % L, (j + dj) % L, (k + dk) % L)]
            edges.append((a, b))
            dirs.append(d)
    return len(idx), edges, dirs


def diamond_conventional(L):
    """Diamond on an L x L x L torus of conventional cubic cells (8L^3 vertices).
    Coordinates in units a/4, torus side 4L."""
    S = 4 * L
    fcc = [(0, 0, 0), (0, 2, 2), (2, 0, 2), (2, 2, 0)]
    A = []
    for i, j, k in product(range(L), repeat=3):
        for f in fcc:
            A.append(((f[0] + 4 * i) % S, (f[1] + 4 * j) % S, (f[2] + 4 * k) % S))
    pos = {}
    for r in A:
        pos[('A', r)] = len(pos)
    for r in A:
        pos[('B', tuple((x + 1) % S for x in r))] = len(pos)
    edges, dirs = [], []
    vecs = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    for r in A:
        a = pos[('A', r)]
        for d, v in enumerate(vecs):
            rb = tuple((r[t] + v[t]) % S for t in range(3))
            b = pos[('B', rb)]
            edges.append((a, b))
            dirs.append(d)
    return len(pos), edges, dirs


def pg23_incidence():
    """Incidence graph of PG(2,3): 26 vertices, 4-regular, girth 6 (the (4,6)-cage)."""
    pts = []
    for v in product(range(3), repeat=3):
        if v == (0, 0, 0):
            continue
        # normalize: first nonzero coordinate = 1
        for c in v:
            if c:
                inv = 1 if c == 1 else 2
                break
        w = tuple((x * inv) % 3 for x in v)
        if w not in pts:
            pts.append(w)
    assert len(pts) == 13
    edges = []
    for i, p in enumerate(pts):
        for j, l in enumerate(pts):
            if sum(a * b for a, b in zip(p, l)) % 3 == 0:
                edges.append((i, 13 + j))
    return 26, edges, None


def incidence(nv, edges):
    inc = [[] for _ in range(nv)]
    for e, (u, v) in enumerate(edges):
        inc[u].append(e)
        inc[v].append(e)
    return inc


def edge_adjacency(nv, edges):
    inc = incidence(nv, edges)
    adj = [set() for _ in edges]
    for v in range(nv):
        for e in inc[v]:
            for f in inc[v]:
                if e != f:
                    adj[e].add(f)
    return adj


def girth(nv, edges):
    nbr = [[] for _ in range(nv)]
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    # multi-edge check
    for u in range(nv):
        if len(set(nbr[u])) != len(nbr[u]):
            return 2
    best = 10 ** 9
    from collections import deque
    for s in range(nv):
        dist = {s: 0}
        par = {s: -1}
        dq = deque([s])
        while dq:
            x = dq.popleft()
            for y in nbr[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    par[y] = x
                    dq.append(y)
                elif par[x] != y:
                    best = min(best, dist[x] + dist[y] + 1)
    return best


def cycles_of_length(nv, edges, length):
    """All elementary cycles of given length, as frozensets of edge indices."""
    nbr = [[] for _ in range(nv)]
    for e, (u, v) in enumerate(edges):
        nbr[u].append((v, e))
        nbr[v].append((u, e))
    found = set()

    def dfs(start, cur, visited, path_edges):
        if len(path_edges) == length:
            return
        for (y, e) in nbr[cur]:
            if y == start and len(path_edges) == length - 1:
                found.add(frozenset(path_edges + [e]))
            elif y not in visited and y > start:
                visited.add(y)
                dfs(start, y, visited, path_edges + [e])
                visited.discard(y)
    for s in range(nv):
        dfs(s, s, {s}, [])
    return [c for c in found if len(c) == length]


def euler_ice(nv, edges):
    """Ice state for any 4-regular graph: alternate occupation along an Euler circuit."""
    inc = incidence(nv, edges)
    used = [False] * len(edges)
    ptr = [0] * nv
    stack = [(0, None)]
    circuit = []
    while stack:
        v, e_in = stack[-1]
        while ptr[v] < len(inc[v]) and used[inc[v][ptr[v]]]:
            ptr[v] += 1
        if ptr[v] == len(inc[v]):
            stack.pop()
            if e_in is not None:
                circuit.append(e_in)
        else:
            e = inc[v][ptr[v]]
            used[e] = True
            u, w = edges[e]
            stack.append((w if u == v else u, e))
    assert len(circuit) == len(edges) and len(edges) % 2 == 0
    n = [0] * len(edges)
    for t, e in enumerate(circuit):
        n[e] = t % 2
    check_ice(nv, edges, n)
    return n


def check_ice(nv, edges, n):
    deg = [0] * nv
    for e, (u, v) in enumerate(edges):
        deg[u] += n[e]
        deg[v] += n[e]
    assert all(d == 2 for d in deg), deg


def loop_update(nv, edges, n, rng):
    """Flip one random alternating closed loop (bipartite graph => even loops)."""
    inc = incidence(nv, edges)
    v0 = rng.randrange(nv)
    path_v = [v0]
    path_e = []
    pos = {v0: 0}
    want = 1  # first edge occupied
    cur = v0
    while True:
        cands = [e for e in inc[cur] if n[e] == want and (not path_e or e != path_e[-1])]
        e = rng.choice(cands)
        u, w = edges[e]
        nxt = w if u == cur else u
        path_e.append(e)
        if nxt in pos:
            j = pos[nxt]
            loop = path_e[j:]
            assert len(loop) % 2 == 0
            for f in loop:
                n[f] ^= 1
            check_ice(nv, edges, n)
            return len(loop)
        pos[nxt] = len(path_v)
        path_v.append(nxt)
        cur = nxt
        want ^= 1
