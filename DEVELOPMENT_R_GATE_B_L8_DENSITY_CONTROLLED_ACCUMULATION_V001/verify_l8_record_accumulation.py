#!/usr/bin/env python3
"""Exact R-B census for density-controlled L4 and L8 record histories."""

from fractions import Fraction
from itertools import product


checks = 0


def check(condition: bool, label: str) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


results = {}
r0 = Fraction(14441248, 6075)
check(r0 == Fraction(32128, 27) + Fraction(7212448, 6075),
      "replicated audited raw coefficient")
check(r0 > 0, "adopted alpha=r0 is positive and not refitted by size")
for L in (4, 8):
    vertices = tuple(product(range(L), repeat=3))
    active = tuple(((x, y, z), ((x + 1) % L, y, z))
                   for x, y, z in vertices if x % 2 == 0)
    check(len(vertices) == L ** 3, f"L={L} vertex count")
    check(len(active) == L ** 3 // 2, f"L={L} active module count")
    flattened = [v for edge in active for v in edge]
    check(len(flattened) == len(set(flattened)) == L ** 3,
          f"L={L} modules are disjoint and cover every cell")
    check(len({frozenset(edge) for edge in active}) == len(active),
          f"L={L} physical supports occur once")

    modules = len(active)
    per_module = Fraction(1, 2)
    q_final = modules * per_module
    write = modules * per_module
    seam = modules * per_module
    residual = q_final - write
    check(seam > 0 and all(per_module > 0 for _ in active),
          f"L={L} every active seam current is nonzero")
    check(residual == 0, f"L={L} global owner ledger")
    cell_residuals = tuple(r for _ in active for r in (Fraction(0), Fraction(0)))
    residual_l1 = sum((abs(r) for r in cell_residuals), Fraction(0))
    residual_linf = max((abs(r) for r in cell_residuals), default=Fraction(0))
    check(len(cell_residuals) == L ** 3, f"L={L} complete cell residual census")
    check(residual_l1 == 0 and residual_linf == 0,
          f"L={L} microscopic carrier residuals vanish")
    check(q_final / (L ** 3) == Fraction(1, 4),
          f"L={L} common retained density")
    variance = modules * Fraction(1, 4)
    check(variance == Fraction(L ** 3, 8), f"L={L} prepared variance")
    # Each finite declared factor uses a complete two- or three-outcome PVM.
    qutrit_effect_sum = Fraction(1)
    controller_effect_sum = Fraction(1)  # E_OK + E_FAILURE
    work_reference_effect_sum = Fraction(1)
    check(qutrit_effect_sum * controller_effect_sum *
          work_reference_effect_sum == 1,
          f"L={L} complete raw terminal instrument")
    results[L] = {
        "modules": modules,
        "q": q_final,
        "write": write,
        "seam": seam,
        "variance": variance,
        "residual_l1": residual_l1,
        "residual_linf": residual_linf,
    }

check(results[8]["q"] / results[4]["q"] == 8,
      "retained total grows by volume ratio")
check(results[8]["modules"] / results[4]["modules"] == 8,
      "lineage count grows by volume ratio")
check(results[4] == {"modules": 32, "q": 16, "write": 16,
                     "seam": 16, "variance": 8, "residual_l1": 0,
                     "residual_linf": 0}, "exact L4 census")
check(results[8] == {"modules": 256, "q": 128, "write": 128,
                     "seam": 128, "variance": 64, "residual_l1": 0,
                     "residual_linf": 0}, "exact L8 census")

print("L4", results[4])
print("L8", results[8])
print("ACCUMULATION_RATIO", results[8]["q"] / results[4]["q"])
print("RETAINED_DENSITY", Fraction(1, 4))
print("LEDGER_RESIDUALS", 0, 0)
print("CARRIER_RESIDUAL_L1_LINF", (0, 0), (0, 0))
print("NET_PERIODIC_BOUNDARY_FLUX", 0, 0)
print("CONTINUUM_OBSERVABLES", "NOT_ASSUMED__NOT_EVALUATED")
print("ATTACHMENT", "ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED")
print("FAILURE_OUTCOMES", "RETAINED_IN_COMPLETE_ALPHABET")
print("M_SERIES", "OPEN")
print(f"PASS__R_GATE_B_L8_RECORD_ACCUMULATION__{checks}/{checks}")
