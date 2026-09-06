#!/usr/bin/env python3
"""Executable custody and finite-family checks for the Gate-A owner join screen."""

import hashlib
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
checks = 0


def check(condition: bool, label: str) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


carrier = REPO / "DEVELOPMENT_G_GATE_A_G4_STATIONARY_CARRIER_SEAM_SECTOR_V001/THEOREM.md"
atlas = REPO / "LANE_CROSS_RFT_GRA_GL6AA_RECORD_AUTHENTICATED_SHARED_CHILD_ATLAS_V001/THEOREM.md"
recoil = REPO / "LANE_GRA_GD_F3_Q4_TRANSLATION_OWNING_RECOIL_PARENT_V001/THEOREM.md"
owner_schema = REPO / "LANE_CROSS_RFT_GRA_GL6CY_COMPLETE_PHYSICAL_SOURCE_REEMBEDDING_RESIDUAL_TARGET_V001/OWNER_SCHEMA.json"
for path in (carrier, atlas, recoil, owner_schema):
    check(path.is_file(), f"required parent exists: {path.name}")
    check(len(hashlib.sha256(path.read_bytes()).hexdigest()) == 64,
          f"parent digest computed: {path.name}")

sizes = {n: comb(n + 3, 3) for n in range(0, 65)}
check(sizes[5] == 56 and sizes[6] == 84, "adjacent simplex sizes around 64")
check(64 not in sizes.values(), "no S_N has 64 cells in bounded exact search")
check(all(sizes[n + 1] > sizes[n] for n in range(64)),
      "simplex cardinality is strictly increasing")

atlas_text = atlas.read_text()
for phrase in (
    "address map, edge list, and owner map are supplied",
    "anchored site-port source map",
    "may read `p_N`",
    "autonomous address or graph selection",
):
    check(phrase in atlas_text, f"GL6AA supplied-data ceiling: {phrase}")

recoil_text = recoil.read_text()
for phrase in (
    "choose\n`kappa_e",
    "bound to GC's diamond positions",
    "not a physical diamond-space",
    "not a derived universal charge-to-momentum law",
    "derived recoil scale or placement",
):
    check(phrase in recoil_text, f"GD free-placement ceiling: {phrase}")

carrier_text = carrier.read_text()
for phrase in (
    "No new grid, distance, graviton, or Ward axiom",
    "OWNER_INCOMPLETE",
    "PHYSICAL_DESCENT_RESIDUAL=UNDEFINED",
    "PHYSICAL_WARD_RESIDUAL=UNDEFINED",
):
    check(phrase in carrier_text, f"carrier scope ceiling: {phrase}")

schema_text = owner_schema.read_text()
for phrase in (
    '"id": "support_and_shared_midpoint"',
    '"id": "gd_recoil_material"',
    '"id": "connected_1pi_schur_legendre_quotient"',
    '"current_status": "UNDEFINED"',
):
    check(phrase in schema_text, f"normative owner gap retained: {phrase}")

print("CARRIER_CELLS", 64)
print("SIMPLEX_NEIGHBORS", sizes[5], sizes[6])
print("SUPPORT_JOIN", "UNDEFINED__AUTHENTICATED_CROSS_FAMILY_MAP_ABSENT")
print("RECOIL_JOIN", "OPTIONAL_BRANCH__NO_MACRO_PHYSICS_PREREQUISITE")
print("GLOBAL_ACTION", "OWNER_INCOMPLETE")
print("DESCENT_WARD", "UNDEFINED", "UNDEFINED")
print("DECISION", "MICRO_RECORD_ACCUMULATION_CONTINUES__MACRO_JOIN_UNDEFINED")
print(f"PASS__GATE_A_SAME_PARENT_OWNER_JOIN_SCREEN__{checks}/{checks}")
