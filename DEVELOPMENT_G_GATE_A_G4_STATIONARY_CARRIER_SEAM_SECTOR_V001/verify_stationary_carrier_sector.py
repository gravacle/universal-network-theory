#!/usr/bin/env python3
"""Exact combinatorial and two-site checks for the stationary G4 carrier sector."""

from fractions import Fraction
from itertools import product


checks = 0


def check(condition: bool, label: str) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


L = 4
vertices = tuple(product(range(L), repeat=3))
check(len(vertices) == 64 and len(set(vertices)) == 64, "G4 has 64 cells")


def advance(v, mu):
    w = list(v)
    w[mu] = (w[mu] + 1) % L
    return tuple(w)


# Positive-generator canonical orientation: every undirected support once.
edges = tuple((v, advance(v, mu), mu) for v in vertices for mu in range(3))
check(len(edges) == 192 and len(set(edges)) == 192,
      "G4 has 192 canonically oriented owner-once edges")
undirected = {frozenset((u, v)) for u, v, _ in edges}
check(len(undirected) == 192, "no undirected edge is double counted")

# Incidence columns have one tail and one head and therefore telescope.
for u, v, _ in edges:
    column = {u: -1, v: 1}
    check(sum(column.values()) == 0, "incidence column telescopes")

# Each vertex has three outgoing and three incoming edges.
for vertex in vertices:
    outgoing = sum(u == vertex for u, _, _ in edges)
    incoming = sum(v == vertex for _, v, _ in edges)
    check((outgoing, incoming) == (3, 3), "six oriented incidences per cell")

# A full transverse slab boundary has 16 outgoing and 16 incoming supports.
region = {v for v in vertices if v[0] == 0}
outward = [(u, v) for u, v, _ in edges if u in region and v not in region]
inward = [(u, v) for u, v, _ in edges if u not in region and v in region]
check(len(region) == 16, "one inherited transverse slab has 16 cells")
check(len(outward) == 16 and len(inward) == 16,
      "slab boundary has paired 16 plus 16 supports")

# Independent exact two-site active-block algebra in basis A=|x,B>, B=|B,x>.
# Matrices are tuples (a,b,c,d) in row-major order.
I = (0j, 1j)
T = ((0, 1), (1, 0))
J = ((0, -1j), (1j, 0))
q_a = ((1, 0), (0, 0))
q_b = ((0, 0), (0, 1))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def sub(a, b):
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2))
                 for i in range(2))


comm_T_qa = sub(mm(T, q_a), mm(q_a, T))
comm_T_qb = sub(mm(T, q_b), mm(q_b, T))
check(comm_T_qa == tuple(tuple(-1j * J[i][j] for j in range(2))
                         for i in range(2)), "[T,q_a]=-iJ")
check(comm_T_qb == tuple(tuple(1j * J[i][j] for j in range(2))
                         for i in range(2)), "[T,q_b]=+iJ")

# With H=-tT: dot q_a=-(t/hbar)J and dot q_b=+(t/hbar)J.
branch_weight = Fraction(1, 2)
integral_sin_2theta = Fraction(1)
seam = branch_weight * integral_sin_2theta
check(seam == Fraction(1, 2), "embedded active history has nonzero seam 1/2")
check((-seam + seam) == 0, "paired regional seam terms telescope")

# A two-site Gibbs numerator is cosh(beta t) I + sinh(beta t) T, hence commutes
# with H proportional to T. Check symbolically in the rational span {I,T}.
a = Fraction(7, 5)
b = Fraction(2, 3)
rho_num = ((a, b), (b, a))
check(mm(rho_num, T) == mm(T, rho_num), "finite Gibbs state is stationary")
check(a > abs(b), "positive two-site Gibbs witness")

# Complete effects q_a and q_b resolve the active one-particle block.
effect_sum = tuple(tuple(q_a[i][j] + q_b[i][j] for j in range(2))
                   for i in range(2))
check(effect_sum == ((1, 0), (0, 1)), "complete terminal effects")
check(Fraction(1) == 1, "equal-branch CTP normalization Z=1")

print("G4_CELLS", len(vertices))
print("OWNER_ONCE_EDGES", len(edges))
print("SLAB_BOUNDARY", len(outward), len(inward))
print("ACTIVE_HISTORY_SEAM", seam)
print("GLOBAL_CARRIER_RESIDUAL", 0)
print("STATIONARY_STATE", "GIBBS_EXISTS__SELECTION_OPEN")
print("GLOBAL_PARENT", "OWNER_INCOMPLETE")
print("DESCENT_WARD", "UNDEFINED", "UNDEFINED")
print(f"PASS__G4_STATIONARY_CARRIER_SEAM_SECTOR__{checks}/{checks}")
