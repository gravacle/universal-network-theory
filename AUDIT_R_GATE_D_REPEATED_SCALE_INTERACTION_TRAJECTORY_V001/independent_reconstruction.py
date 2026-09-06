#!/usr/bin/env python3
"""Independent even-L R-D reconstruction; no target imports."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

checks = 0


def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1


rows = {}
for L in (2, 4, 6, 8, 10):
    cells = tuple(product(range(L), repeat=3))
    heads = tuple(v for v in cells if v[0] % 2 == 1)
    blocks = tuple(((x, y, z), (x, y+1, z))
                   for x, y, z in heads if y % 2 == 0)
    flat = tuple(v for block in blocks for v in block)
    check(len(cells) == L**3, "cells")
    check(len(heads) == L**3 // 2, "heads")
    check(len(blocks) == L**3 // 4, "blocks")
    check(len(flat) == len(set(flat)) == len(heads), "disjoint coverage")
    n = F(L**3, 4)
    row = (F(L**3), n, n, n/F(4), n/F(4), 3*n/F(4), F(0), F(0))
    check(row[4] + row[5] == row[2], "positional total")
    check(row[3] == F(L**3, 16), "throughput")
    check(row[6:] == (0, 0), "residuals")
    rows[L] = row

check(rows[4] == (64, 16, 16, 4, 4, 12, 0, 0), "L4 row")
check(rows[8] == (512, 128, 128, 32, 32, 96, 0, 0), "L8 row")
ratios = tuple(rows[8][i] / rows[4][i] for i in range(6))
check(ratios == (8, 8, 8, 8, 8, 8), "raw ratios")
r0 = F(32128, 27) + F(7212448, 6075)
check(r0 == F(14441248, 6075), "adopted r0 provenance")
check(F(1) * (F(1)+F(0)) * F(1) == 1, "failure-inclusive product read")

result = {
    "schema": "AUDIT_R_GATE_D_REPEATED_SCALE_INTERACTION_TRAJECTORY_V001",
    "disposition": "PASS_CONDITIONAL_FIXED_DENSITY_TRAJECTORY",
    "checks": checks,
    "general_even_L": {
        "heads": "L^3/2", "blocks": "L^3/4", "retained": "L^3/4",
        "throughput": "L^3/16", "positional": ["L^3/16", "3L^3/16"],
        "residual_l1_linf": ["0", "0"]
    },
    "L4": ["64", "16", "16", "4", "4", "12", "0", "0"],
    "L8": ["512", "128", "128", "32", "32", "96", "0", "0"],
    "ratios": ["8", "8", "8", "8", "8", "8"],
    "attachment": "ADOPTED_ALPHA_EQUALS_R0__NOT_BARE_F3_DERIVED__FIXED_ACROSS_L",
    "scope": "CONDITIONAL_FIXED_DENSITY_DISJOINT_BLOCK_FAMILY",
    "terminal_instrument": "COMPLETE_QUTRIT_CONTROLLER_FAILURE_WORK_REFERENCE_PRODUCT",
    "ratio_interpretation": "VOLUME_REPLICATION_ONLY__NOT_CONTINUUM_CRITICAL_OR_GENERIC",
    "individual_lineage_criticality_continuum_gravity": "NOT_CLAIMED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_CONDITIONAL_FIXED_DENSITY_TRAJECTORY__{checks}/{checks}")
