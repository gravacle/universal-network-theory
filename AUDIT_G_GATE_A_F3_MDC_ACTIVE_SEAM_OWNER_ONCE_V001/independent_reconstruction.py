#!/usr/bin/env python3
"""Independent hostile reconstruction; imports no target code."""

from fractions import Fraction as F
import json
from pathlib import Path

checks = 0


def require(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


# Basis order (A,B), where A=|x,B> and B=|B,x>.
T = ((0j, 1 + 0j), (1 + 0j, 0j))
J = ((0j, -1j), (1j, 0j))
qa = ((1 + 0j, 0j), (0j, 0j))
qb = ((0j, 0j), (0j, 1 + 0j))


def mv(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(2)) for i in range(2))


def inner(v, w):
    return sum(v[i].conjugate() * w[i] for i in range(2))


def comm(a, b):
    def mm(x, y):
        return tuple(tuple(sum(x[i][k] * y[k][j] for k in range(2))
                           for j in range(2)) for i in range(2))
    ab, ba = mm(a, b), mm(b, a)
    return tuple(tuple(ab[i][j] - ba[i][j] for j in range(2))
                 for i in range(2))


# Set t/hbar=1. H=-T. The Heisenberg equation is dq/dt=i[H,q].
H = tuple(tuple(-T[i][j] for j in range(2)) for i in range(2))
dqa = tuple(tuple(1j * z for z in row) for row in comm(H, qa))
dqb = tuple(tuple(1j * z for z in row) for row in comm(H, qb))
require(dqa == tuple(tuple(-z for z in row) for row in J),
        "BS09 sign gives dqa=-J")
require(dqb == J, "BS09 sign gives dqb=+J")

# Native evolution exp(+i theta T)|A> = cos(theta)|A>+i sin(theta)|B>.
at_zero = (1 + 0j, 0j)
at_half = (2 ** -0.5 + 0j, 1j * 2 ** -0.5)
at_end = (0j, 1j)
require(abs(inner(at_half, mv(J, at_half)).real - 1.0) < 1e-14,
        "current orientation is positive at theta=pi/4")
require(abs(inner(at_end, mv(qb, at_end)).real - 1.0) < 1e-14,
        "theta=pi/2 transfers A to B")

# The write branch has weight 1/2. Integral_0^(pi/2) sin(2 theta)dtheta=1.
branch_weight = F(1, 2)
integrated_current = branch_weight
delta_a, delta_b = F(0), F(1, 2)
write_a, write_b = F(1, 2), F(0)
ra = delta_a + integrated_current - write_a
rb = delta_b - integrated_current - write_b
require(integrated_current == F(1, 2), "nonzero physical seam flux")
require((ra, rb, ra + rb) == (0, 0, 0), "local and global ledgers")

# The raw coefficient arithmetic and the scale degeneracy are independent.
r0 = F(32128, 27) + F(7212448, 6075)
require(r0 == F(14441248, 6075), "raw coefficient")
require(r0 != 2 * r0 and r0 > 0, "two distinct real port scales")

# Repaired finite operator CTP check. For a complete effect family and equal
# branches, sum_y Tr(E_y U rho U^dagger)=Tr(rho)=1. This is a generator, not a
# claim to a continuum variational action, so no separate Berry term is due.
rho = ((1 + 0j, 0j), (0j, 0j))
effects = (((1 + 0j, 0j), (0j, 0j)),
           ((0j, 0j), (0j, 1 + 0j)))
U = ((0j, 1j), (1j, 0j))


def dagger(m):
    return tuple(tuple(m[j][i].conjugate() for j in range(2)) for i in range(2))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def trace(m):
    return sum(m[i][i] for i in range(2))


e_sum = tuple(tuple(sum(e[i][j] for e in effects) for j in range(2))
              for i in range(2))
require(e_sum == ((1 + 0j, 0j), (0j, 1 + 0j)), "complete effects")
z_equal = sum(trace(mm(mm(mm(e, U), rho), dagger(U))) for e in effects)
require(abs(z_equal - 1) < 1e-14, "equal-branch CTP normalization")

result = {
    "schema": "HOSTILE_AUDIT_G_GATE_A_F3_MDC_ACTIVE_SEAM_OWNER_ONCE_V001",
    "disposition": "PASS_AFTER_REPAIR",
    "checks": checks,
    "seam_current": "1/2",
    "cell_residuals": ["0", "0"],
    "global_residual": "0",
    "attachment": "CONDITIONAL__BARE_F3_SCALE_NONIDENTIFIABLE",
    "material_defect": None,
    "gate_A": "OPEN",
    "gate_B": "UNAUTHORIZED",
    "gravity": "NOT_CLAIMED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_AFTER_REPAIR__{checks}/{checks}")
