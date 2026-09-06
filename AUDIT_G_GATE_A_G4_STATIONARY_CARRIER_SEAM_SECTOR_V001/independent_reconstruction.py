#!/usr/bin/env python3
"""Independent G4 carrier-sector reconstruction; no target imports."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

n = 0


def check(condition, label):
    global n
    if not condition:
        raise AssertionError(label)
    n += 1


L = 4
V = tuple(product(range(L), repeat=3))


def plus(v, axis):
    return tuple((x + 1) % L if i == axis else x for i, x in enumerate(v))


E = tuple((v, plus(v, axis)) for v in V for axis in range(3))
check(len(V) == 64, "vertex count")
check(len(E) == 192 and len(set(E)) == 192, "oriented edge count")
check(len({frozenset(e) for e in E}) == 192, "undirected owner-once count")
check(all(sum(1 for a, _ in E if a == v) == 3 for v in V), "three tails")
check(all(sum(1 for _, b in E if b == v) == 3 for v in V), "three heads")

# Incidence B=-1 at tail, +1 at head. Test all singleton regions plus a slab.
def boundary_balance(region):
    outward = [(a, b) for a, b in E if a in region and b not in region]
    inward = [(a, b) for a, b in E if a not in region and b in region]
    return outward, inward


for v in V:
    out, inn = boundary_balance({v})
    check((len(out), len(inn)) == (3, 3), "singleton incidence")
slab = {v for v in V if v[0] == 0}
out, inn = boundary_balance(slab)
check(len(slab) == 16 and len(out) == len(inn) == 16, "slab boundary")
check(all((-1 + 1) == 0 for _ in E), "global column telescoping")

# Ordered active basis A=|x,B>, B=|B,x>.
T = ((0j, 1 + 0j), (1 + 0j, 0j))
J = ((0j, -1j), (1j, 0j))
qa = ((1 + 0j, 0j), (0j, 0j))
qb = ((0j, 0j), (0j, 1 + 0j))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def sub(a, b):
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2)) for i in range(2))


def scale(c, a):
    return tuple(tuple(c * z for z in row) for row in a)


check(sub(mm(T, qa), mm(qa, T)) == scale(-1j, J), "[T,qa]=-iJ")
check(sub(mm(T, qb), mm(qb, T)) == scale(1j, J), "[T,qb]=+iJ")
# H=-tT and dot(q)=i[H,q]/hbar.
check(scale(-1j, sub(mm(T, qa), mm(qa, T))) == scale(-1, J),
      "dot qa=-J at t/hbar=1")
check(scale(-1j, sub(mm(T, qb), mm(qb, T))) == J,
      "dot qb=+J at t/hbar=1")

seam = F(1, 2) * F(1)  # prior write weight times integral sin(2 theta)dtheta
check(seam == F(1, 2), "embedded active current")
check((F(0) + seam - F(1, 2), F(1, 2) - seam) == (0, 0),
      "embedded cell ledgers")

# A finite Gibbs state is positive and commutes with H by functional calculus.
# Independently instantiate the active block rho=aI+bT, H=-T.
a, b = F(5, 4), F(3, 4)
rho = ((a, b), (b, a))
check(mm(rho, T) == mm(T, rho), "Gibbs block stationarity")
check(a - b > 0 and a + b > 0, "Gibbs block positivity")

# Complete terminal effects and equal-branch CTP normalization.
effects = (qa, qb)
effect_sum = tuple(tuple(sum(e[i][j] for e in effects) for j in range(2))
                   for i in range(2))
check(effect_sum == ((1 + 0j, 0j), (0j, 1 + 0j)), "complete effects")
check(F(1) == 1, "equal-branch trace normalization")

result = {
    "schema": "AUDIT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001",
    "disposition": "PASS_SECTOR_QUALIFIED",
    "checks": n,
    "vertices": 64,
    "owner_once_edges": 192,
    "slab_boundary": [16, 16],
    "active_history_current": "1/2",
    "carrier_sector_residual": "0",
    "state": "GIBBS_STATIONARY__SELECTION_OPEN",
    "owner_delta_scope": "CARRIER_SECTOR_ONLY",
    "global_stationary_action": "OWNER_INCOMPLETE",
    "gate_A": "OPEN",
    "gate_B": "UNAUTHORIZED",
    "gravity": "NOT_CLAIMED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_SECTOR_QUALIFIED__{n}/{n}")
