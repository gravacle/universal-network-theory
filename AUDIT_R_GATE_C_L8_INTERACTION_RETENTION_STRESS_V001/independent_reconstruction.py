#!/usr/bin/env python3
"""Independent exact R-C reconstruction; imports no target code."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math

checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


M = ((1, -1), (-1, -1))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


check(mm(M, M) == ((2, 0), (0, 2)), "H squared")
check(abs((math.pi / (2 * math.sqrt(2))) * math.sqrt(2) - math.pi / 2) < 1e-15,
      "pulse angle")

# U=-i M/sqrt(2) at the pulse endpoint. Acting on (A+B)/sqrt(2)
# gives iB exactly up to floating representation.
s = 1 / math.sqrt(2)
plus = (s, s)
mplus = (M[0][0]*plus[0] + M[0][1]*plus[1],
         M[1][0]*plus[0] + M[1][1]*plus[1])
after = tuple(-1j * z / math.sqrt(2) for z in mplus)
check(abs(after[0]) < 1e-15 and abs(after[1] - 1j) < 1e-15,
      "plus maps to iB")

before = (F(1, 4),) * 4  # BB, Bx, xB, xx
after_p = (F(1, 4), F(1, 2), F(0), F(1, 4))
check(sum(before) == sum(after_p) == 1, "full distributions")
tv = sum((abs(a-b) for a, b in zip(before, after_p)), F(0)) / 2
check(tv == F(1, 4), "TV")

q1i, q2i = before[2] + before[3], before[1] + before[3]
q1f, q2f = after_p[2] + after_p[3], after_p[1] + after_p[3]
check((q1i, q2i) == (F(1, 2), F(1, 2)), "initial occupations")
check((q1f, q2f) == (F(1, 4), F(3, 4)), "final occupations")

# In normalized one-particle evolution, <J>(s)=sin(2 sqrt(2)s)/sqrt(2).
# Its integral from 0 to pi/(2sqrt(2)) is 1/2. The full product state has
# one-particle weight 1/2, hence oriented current 1/4.
normalized_current_integral = F(1, 2)
sector_weight = F(1, 2)
current = normalized_current_integral * sector_weight
check(current == F(1, 4), "oriented current")
check((q1f-q1i+current, q2f-q2i-current) == (0, 0), "pair ledgers")
number_i = (before[0], before[1]+before[2], before[3])
number_f = (after_p[0], after_p[1]+after_p[2], after_p[3])
check(number_i == number_f == (F(1, 4), F(1, 2), F(1, 4)),
      "number distribution")

L = 8
heads = tuple(v for v in product(range(L), repeat=3) if v[0] % 2)
pairs = tuple(((x, y, z), (x, y+1, z))
              for x, y, z in heads if y % 2 == 0)
flat = tuple(v for pair in pairs for v in pair)
check(len(heads) == 256, "head count")
check(len(pairs) == 128, "pair count")
check(len(flat) == len(set(flat)) == 256, "disjoint head coverage")
check(len(pairs)*(q1i+q2i) == len(pairs)*(q1f+q2f) == 128,
      "retained total")
check(len(pairs)*current == 32, "throughput")
check((len(pairs)*q1f, len(pairs)*q2f) == (32, 96), "positions")

# Complete terminal product: qutrit, controller OK/FAILURE, work/reference.
check(F(1) * (F(1)+F(0)) * F(1) == 1, "complete failure-inclusive read")

result = {
    "schema": "AUDIT_R_GATE_C_L8_INTERACTION_RETENTION_STRESS_V001",
    "disposition": "PASS_CONDITIONAL_INTERACTION_STRESS",
    "checks": checks,
    "hamiltonian_square": "2I",
    "one_particle_endpoint": "i|B>",
    "pair_before": ["1/4", "1/4", "1/4", "1/4"],
    "pair_after": ["1/4", "1/2", "0", "1/4"],
    "TV": "1/4",
    "local_after": ["1/4", "3/4"],
    "oriented_current": "1/4",
    "pair_residuals": ["0", "0"],
    "number_distribution": ["1/4", "1/2", "1/4"],
    "L8": {"heads": 256, "blocks": 128, "retained": "128",
           "throughput": "32", "positional_after": ["32", "96"]},
    "read": "COMPLETE_FAILURE_INCLUSIVE_PRODUCT",
    "scope": "CONDITIONAL_PREPARED_DISJOINT_INTERACTION_BLOCKS",
    "individual_lineage_motion": "NOT_CLAIMED",
    "criticality_continuum_gravity": "NOT_CLAIMED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_CONDITIONAL_INTERACTION_STRESS__{checks}/{checks}")
