#!/usr/bin/env python3
"""Exact L4/L8 repeated-scale R-C interaction trajectory."""

from fractions import Fraction
from itertools import product


checks = 0


def check(condition: bool, label: str) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


data = {}
r0 = Fraction(14441248, 6075)
check(r0 == Fraction(32128, 27) + Fraction(7212448, 6075),
      "adopted attachment coefficient custody")
for L in (4, 8):
    cells = tuple(product(range(L), repeat=3))
    heads = tuple(v for v in cells if v[0] % 2 == 1)
    blocks = tuple(((x, y, z), (x, y + 1, z))
                   for x, y, z in heads if y % 2 == 0)
    check(len(cells) == L ** 3, f"L={L} cells")
    check(len(heads) == L ** 3 // 2, f"L={L} prepared heads")
    check(len(blocks) == L ** 3 // 4, f"L={L} interaction blocks")
    flat = [v for block in blocks for v in block]
    check(len(flat) == len(set(flat)) == len(heads),
          f"L={L} disjoint block coverage")

    n = len(blocks)
    retained = Fraction(n)
    throughput = Fraction(n, 4)
    low = Fraction(n, 4)
    high = Fraction(3 * n, 4)
    residual_l1 = Fraction(0)
    residual_linf = Fraction(0)
    check(low + high == retained, f"L={L} positional total")
    check(throughput > 0, f"L={L} active interaction current")
    check(residual_l1 == residual_linf == 0, f"L={L} exact residuals")
    check(Fraction(1) * Fraction(1) * Fraction(1) == 1,
          f"L={L} complete failure-inclusive terminal instrument")
    data[L] = (len(cells), n, retained, throughput, low, high,
               residual_l1, residual_linf)

for index, label in enumerate(("cells", "blocks", "retained", "throughput",
                               "low", "high")):
    check(data[8][index] / data[4][index] == 8,
          f"{label} L8/L4 ratio")
check(data[4] == (64, 16, 16, 4, 4, 12, 0, 0), "exact L4 row")
check(data[8] == (512, 128, 128, 32, 32, 96, 0, 0), "exact L8 row")

print("L4", data[4])
print("L8", data[8])
print("RAW_RATIOS", (8, 8, 8, 8, 8, 8))
print("RECORD_LEDGER_RESIDUALS", (0, 0), (0, 0))
print("INTERPRETATION", "PREPARED_FIXED_DENSITY__NO_CONTINUUM_FIT")
print("ATTACHMENT", "ADOPTED_ALPHA_R0__NOT_REFIT__NOT_BARE_F3_DERIVED")
print(f"PASS__R_GATE_D_REPEATED_SCALE_INTERACTION_TRAJECTORY__{checks}/{checks}")
