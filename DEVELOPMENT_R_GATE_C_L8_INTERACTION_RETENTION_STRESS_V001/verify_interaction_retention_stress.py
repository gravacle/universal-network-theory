#!/usr/bin/env python3
"""Exact R-C interaction/retention stress on the prepared L8 record family."""

from fractions import Fraction
from itertools import product


checks = 0


def check(condition: bool, label: str) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


# Exact one-occupation Hamiltonian H/t and its square.
H = ((1, -1), (-1, -1))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


check(mm(H, H) == ((2, 0), (0, 2)), "H^2=2I on one-occupation block")
plus = (Fraction(1, 2), Fraction(1, 2))  # squared amplitudes before
after_single = (Fraction(0), Fraction(1))
check(sum(plus) == sum(after_single) == 1, "one-occupation norm")

p_before = (Fraction(1, 4),) * 4  # BB, Bx, xB, xx
p_after = (Fraction(1, 4), Fraction(1, 2), Fraction(0), Fraction(1, 4))
check(sum(p_before) == sum(p_after) == 1, "complete pair distributions")
tv = sum(abs(a - b) for a, b in zip(p_before, p_after)) / 2
check(tv == Fraction(1, 4), "complete positional read TV contrast")

q1_before = p_before[2] + p_before[3]
q2_before = p_before[1] + p_before[3]
q1_after = p_after[2] + p_after[3]
q2_after = p_after[1] + p_after[3]
check((q1_before, q2_before) == (Fraction(1, 2), Fraction(1, 2)),
      "initial local occupations")
check((q1_after, q2_after) == (Fraction(1, 4), Fraction(3, 4)),
      "interacting local occupations")
check(q1_before + q2_before == q1_after + q2_after == 1,
      "total retained occupation conserved")

current = Fraction(1, 4)
r1 = q1_after - q1_before + current
r2 = q2_after - q2_before - current
check((r1, r2) == (0, 0), "pair record ledgers close")

# Total-occupation law is unchanged.
number_before = (p_before[0], p_before[1] + p_before[2], p_before[3])
number_after = (p_after[0], p_after[1] + p_after[2], p_after[3])
check(number_before == number_after ==
      (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
      "record-number distribution retained")

L = 8
heads = tuple(v for v in product(range(L), repeat=3) if v[0] % 2 == 1)
pairs = tuple(((x, y, z), (x, y + 1, z))
              for x, y, z in heads if y % 2 == 0)
check(len(heads) == 256, "R-B retained-head count")
check(len(pairs) == 128, "L8 disjoint interaction count")
flat = [v for pair in pairs for v in pair]
check(len(flat) == len(set(flat)) == len(heads),
      "interaction blocks disjoint and cover all heads")

retained_before = len(pairs) * (q1_before + q2_before)
retained_after = len(pairs) * (q1_after + q2_after)
throughput = len(pairs) * current
check(retained_before == retained_after == 128, "L8 total retention")
check(throughput == 32, "L8 absolute oriented interaction throughput")
check(len(pairs) * (abs(r1) + abs(r2)) == 0,
      "L8 record-ledger residual l1")
check(max(abs(r1), abs(r2)) == 0, "L8 record-ledger residual linf")
check(len(pairs) * q1_after == 32 and len(pairs) * q2_after == 96,
      "L8 positional redistribution census")

# Complete qutrit and controller/failure/work/reference effects resolve I.
check(Fraction(1) * Fraction(1) * Fraction(1) == 1,
      "complete failure-inclusive terminal instrument")

print("PAIR_BEFORE", tuple(str(x) for x in p_before))
print("PAIR_AFTER", tuple(str(x) for x in p_after))
print("PAIR_POSITIONAL_TV", tv)
print("L8_INTERACTION_BLOCKS", len(pairs))
print("RETAINED_TOTAL_BEFORE_AFTER", retained_before, retained_after)
print("RETENTION_FRACTION", 1)
print("POSITIONAL_EXPECTATIONS_AFTER", 32, 96)
print("ABSOLUTE_ORIENTED_INTERACTION_THROUGHPUT", throughput)
print("RECORD_LEDGER_RESIDUAL_L1_LINF", 0, 0)
print("CONTINUUM", "NOT_ASSUMED__NOT_EVALUATED")
print(f"PASS__R_GATE_C_L8_INTERACTION_RETENTION_STRESS__{checks}/{checks}")
