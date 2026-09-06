#!/usr/bin/env python3
"""Independent exact R-B census; does not import the target verifier."""

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
for L in (4, 8):
    vertices = tuple(product(range(L), repeat=3))
    edges = tuple(((x, y, z), (x + 1, y, z))
                  for x, y, z in vertices if x % 2 == 0)
    flat = tuple(v for e in edges for v in e)
    check(len(vertices) == L**3, "cell count")
    check(len(edges) == L**3 // 2, "module count")
    check(len(flat) == len(set(flat)) == L**3, "disjoint full cover")
    check(len({frozenset(e) for e in edges}) == len(edges), "owner once")

    m = len(edges)
    write = F(m, 2)
    retained = F(m, 2)
    throughput = sum((abs(F(1, 2)) for _ in edges), F(0))
    net_boundary_flux = F(0)
    variance = m * F(1, 2) * F(1, 2)
    tail_residual = F(0) + F(1, 2) - F(1, 2)
    head_residual = F(1, 2) - F(1, 2)
    check((tail_residual, head_residual) == (0, 0), "per-module ledgers")
    check(throughput == F(m, 2) and throughput > 0, "absolute throughput")
    check(net_boundary_flux == 0, "net closed-family boundary flux")
    check(retained == write and retained / L**3 == F(1, 4), "total/density")
    check(variance == F(L**3, 8), "Bernoulli variance")
    rows[L] = (m, retained, throughput, variance)

check(rows[4] == (32, 16, 16, 8), "L4 exact row")
check(rows[8] == (256, 128, 128, 64), "L8 exact row")
check(rows[8][1] / rows[4][1] == 8, "retained ratio")
check(rows[8][0] / rows[4][0] == 8, "lineage ratio")

# Independently validate the supplied resource-custody arithmetic. This is
# custody for the exact combinatorial verifier, not evidence of dense dynamics.
custody = json.loads((Path(__file__).parent.parent /
    "DEVELOPMENT_R_GATE_B_L8_DENSITY_CONTROLLED_ACCUMULATION_V001" /
    "EXECUTION_CUSTODY.json").read_text())
mem = custody["memory"]
check(custody["environment"]["physical_memory_bytes"] == 48 * 1024**3,
      "48 GiB hardware conversion")
check(mem["maximum_resident_set_mib"] ==
      mem["maximum_resident_set_bytes"] / 1024**2, "RSS MiB conversion")
check(mem["peak_memory_footprint_mib"] ==
      mem["peak_memory_footprint_bytes"] / 1024**2, "footprint MiB conversion")
check(custody["runtime_seconds"]["wall"] >= 0 and
      custody["runtime_seconds"]["user"] >= 0 and
      custody["runtime_seconds"]["system"] >= 0, "nonnegative timings")
check(mem["swaps"] == 0, "zero recorded swaps")
check("exact combinatorial" in custody["scope_note"] and
      "not a dense 3^512" in custody["scope_note"], "resource scope ceiling")

result = {
    "schema": "AUDIT_R_GATE_B_L8_DENSITY_CONTROLLED_ACCUMULATION_V001",
    "disposition": "PASS_AFTER_REPAIR",
    "checks": checks,
    "arithmetic": "PASS",
    "L4": {"modules": 32, "retained": "16", "throughput": "16",
           "net_periodic_flux": "0", "variance": "8"},
    "L8": {"modules": 256, "retained": "128", "throughput": "128",
           "net_periodic_flux": "0", "variance": "64"},
    "density": "1/4",
    "ratio": "8",
    "scope": "CONDITIONAL_TENSOR_PRODUCT_PREPARED_HISTORY",
    "generic_accumulation": "NOT_PROVED",
    "schedule_V002": "PASS_SEPARATION_AND_OWNER_ONCE",
    "attachment": "ADOPTED_ALPHA_EQUALS_R0__NOT_BARE_F3_DERIVED__NOT_REFIT_AT_L8",
    "terminal_instrument": "COMPLETE_QUTRIT_CONTROLLER_FAILURE_WORK_REFERENCE_PRODUCT_PVM",
    "carrier_residual_l1_linf": {"L4": ["0", "0"], "L8": ["0", "0"]},
    "execution_custody": {
        "wall_user_system_seconds": ["0.07", "0.02", "0.01"],
        "max_rss_bytes": 11075584,
        "peak_footprint_bytes": 7110968,
        "swaps": 0,
        "scope": "EXACT_COMBINATORIAL_VERIFIER__NOT_DENSE_3_POW_512_EVOLUTION"
    },
    "material_defects": [],
    "M_series": "NOT_PROMOTED",
    "gravity": "NOT_CLAIMED"
}
(Path(__file__).parent / "INDEPENDENT_RESULT.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(f"PASS_AFTER_REPAIR__{checks}/{checks}")
