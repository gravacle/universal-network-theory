#!/usr/bin/env python3
"""Hash-pinned hostile comparison of target and blind independent seed screens."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001"
TARGET_RESULT = TARGET / "RESULT.json"
INDEPENDENT_RESULT = HERE / "INDEPENDENT_RESULT.json"
OUT = HERE / "AUDIT_RESULT.json"

PINNED = {
    TARGET / "PROTOCOL.md": "3da9e74b0dcc2d8b65ce98cfb42735864cf3d045e41655082baa7a7a295cb334",
    TARGET / "compute_seed_screen.py": "d8a2369803340a69553cda58fdbb7643bbe896d4059f371b85992cc503093135",
    TARGET_RESULT: "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05",
    TARGET / "RESULT.md": "a1130b0912e424f240d170b5bc19e02a30a35d18842657f700dc3658046b8cfd",
    TARGET / "THEOREM.md": "19d02251ea0685f467cb731b329f88bceb0c9ff919dacccd3b21a28ae0dd6db3",
    TARGET / "README.md": "e7d4dafd57dac00292c06c96e6c5f71376367b57510e051a3e3ee00d7682fbbc",
    TARGET / "RUN_OBSERVATION.md": "6f54a8569007f5786d81d34a3de8ae78f2c1ffc0a069eb33446e34da7f4c202d",
    HERE / "METHODOLOGY.md": "301af100a7648d5773642aece6872bec647d0dceaaec83b79c96e3a5b060cae9",
    HERE / "independent_prescreen.py": "8cf6e3fd5c5e7cc27843bffe8dd1bb54895a980cc540a4379ed495d916295cd7",
    INDEPENDENT_RESULT: "39625068c0694f3e8e111fc1285af76269fceae6338fa99dc6723ab89b3c71d4",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = []


def check(condition: bool, label: str) -> None:
    checks.append((bool(condition), label))


for path, expected in PINNED.items():
    check(path.is_file(), f"pinned file exists: {path.name}")
    check(path.is_file() and digest(path) == expected, f"pinned hash: {path.name}")

target = json.loads(TARGET_RESULT.read_text())
independent = json.loads(INDEPENDENT_RESULT.read_text())

check(target["protocol_sha256"] == PINNED[TARGET / "PROTOCOL.md"], "target protocol custody")
check(independent["protocol_sha256"] == PINNED[TARGET / "PROTOCOL.md"], "independent protocol custody")
check(target["classification"] == "NO_CANDIDATE_L4_L8__STOP_NO_L10_L12", "target no-seed stop")
check(independent["classification"] == "NO_CANDIDATE_L4_L8", "independent no-seed stop")
check(target["checks_passed"] == target["checks_total"] == 36, "target 36/36")
check(not target["failures"] and not target["unresolved_rows"], "target has no failed or unresolved row")
check(independent["checks_passed"] == independent["checks_total"] == 18, "independent 18/18")
check(not independent["failed_checks"], "independent has no failed control")
check(all(not rows for rows in target["seeds_by_L"].values()), "target seed sets empty")
check(all(not rows for rows in independent["seeds"].values()), "independent seed sets empty")
check(not target["seed_interval_components"] and not target["qualifying_triplets"], "target interval empty")
check(not independent["candidate_intervals"] and not independent["candidate_triplets"], "independent interval empty")
check(target["larger_scale_status"] == "L10_L12_NOT_RUN__TARGET_STOPS_AFTER_L4_L8_SEED_CLASSIFICATION", "target larger-size stop")
check(independent["sizes_executed"] == [4, 6, 8], "independent size census")
check(independent["sizes_forbidden_and_not_executed"] == [10, 12], "independent larger-size stop")

target_structural = {str(row["L"]): row for row in target["structural_controls"]}
for length in (4, 6, 8):
    key = str(length)
    target_row = target_structural[key]
    independent_row = independent["structural"][key]
    check(target_row["sites"] == independent_row["sites"] == 2 * length, f"L{length} site agreement")
    check(target_row["edges"] == independent_row["owner_edges"] == 3 * length, f"L{length} owner agreement")
    check(target_row["degree_sequence"] == independent_row["degrees"] == [3] * (2 * length), f"L{length} degree agreement")
    check(target_row["H_independent_of_N"] and not independent_row["hamiltonian_has_write_count_argument"], f"L{length} H independent of N")
    check(target_row["particle_hole_map"].startswith("GLOBAL_BIT_COMPLEMENT") and independent_row["particle_hole"].startswith("EXACT"), f"L{length} particle-hole agreement")
    check(target_row["one_carrier_zero_count_at_1e-10"] == independent_row["exact_zero_multiplicity"], f"L{length} commensurate-zero agreement")
    check(max(target_row["one_carrier_band_linf"], independent_row["one_carrier_band_linf"]) < 4.0e-15, f"L{length} analytic band agreement")

metric_pairs = {
    "ground_energy": "ground_energy",
    "Delta_Q": "delta_Q",
    "Delta_act": "delta_act",
    "chi_tau": "chi_tau",
    "R_low": "R_low",
}
max_errors = {metric: 0.0 for metric in metric_pairs}
row_count = 0
for length in (4, 6, 8):
    key = str(length)
    target_rows = {row["q"]: row for row in target["sector_rows"][key] if row["q"] > 0}
    independent_rows = {row["q"]: row for row in independent["rows"][key]}
    check(set(target_rows) == set(independent_rows) == set(range(1, length + 1)), f"L{length} sector-row census")
    for charge in range(1, length + 1):
        trow = target_rows[charge]
        irow = independent_rows[charge]
        row_count += 1
        check(trow["dimension"] == irow["sector_dimension"], f"L{length} q{charge} dimension")
        check(trow["response_status"] == "RESOLVED" and not irow["unresolved_reasons"], f"L{length} q{charge} resolved")
        check(trow["threshold_stable"] and irow["threshold_stable"], f"L{length} q{charge} threshold stability")
        check(trow["R_low"] >= 1.0e-6 and irow["R_low"] >= 1.0e-6, f"L{length} q{charge} active residue")
        for target_key, independent_key in metric_pairs.items():
            error = abs(trow[target_key] - irow[independent_key])
            max_errors[target_key] = max(max_errors[target_key], error)
            check(error <= 1.0e-11, f"L{length} q{charge} {target_key} parity")
    ordered_target = [target_rows[q] for q in range(1, length + 1)]
    ordered_independent = [independent_rows[q] for q in range(1, length + 1)]
    check(all(a["Delta_act"] < b["Delta_act"] for a, b in zip(ordered_target, ordered_target[1:])), f"L{length} target gap monotone")
    check(all(a["chi_tau"] > b["chi_tau"] for a, b in zip(ordered_target, ordered_target[1:])), f"L{length} target chi monotone")
    check(all(a["delta_act"] < b["delta_act"] for a, b in zip(ordered_independent, ordered_independent[1:])), f"L{length} independent gap monotone")
    check(all(a["chi_tau"] > b["chi_tau"] for a, b in zip(ordered_independent, ordered_independent[1:])), f"L{length} independent chi monotone")

raw_files = sorted(path for path in (TARGET / "RAW").iterdir() if path.is_file())
check(len(raw_files) == 42, "target raw artifact census")
check(all("L10" not in path.name and "L12" not in path.name for path in raw_files), "no target L10/L12 raw artifact")
raw_hash_checks = 0
for length in (4, 6, 8):
    for row in target["sector_rows"][str(length)]:
        spectrum = TARGET / row["spectrum_file"]
        check(spectrum.is_file() and digest(spectrum) == row["spectrum_sha256"], f"L{length} q{row['q']} spectrum hash")
        raw_hash_checks += 1

failures = [label for passed, label in checks if not passed]
verdict = (
    "PASS_HOSTILE_NO_CANDIDATE_L4_L8__STOP_NO_L10_L12"
    if not failures
    else "FAIL_HOSTILE_COMPARISON"
)
result = {
    "schema": "AUDIT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001_FINAL",
    "verdict": verdict,
    "independence": "V002_METHOD_CODE_AND_RESULT_FROZEN_BEFORE_TARGET_RESULT_INSPECTION",
    "v001_failure_provenance": "PRESERVED__BACKEND_WARNING_BEFORE_RESULT__NO_PHYSICS_PROMOTED",
    "target_classification": target["classification"],
    "independent_classification": independent["classification"],
    "rows_compared": row_count,
    "metric_components_compared": row_count * len(metric_pairs),
    "maximum_target_independent_errors": max_errors,
    "raw_spectrum_hashes_checked": raw_hash_checks,
    "sizes_executed": [4, 6, 8],
    "larger_sizes_executed": [],
    "macro_followups_executed": [],
    "claim_boundary": "FINITE_ADOPTED_RESPONSE_CHANNEL_NULL_ONLY__NO_RHO_C__NO_CONTINUUM__NO_GRAVITY",
    "checks_passed": sum(passed for passed, _ in checks),
    "checks_total": len(checks),
    "failures": failures,
}
OUT.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
if failures:
    raise SystemExit(1)
