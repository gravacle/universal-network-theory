#!/usr/bin/env python3
"""Read-only z=1 diagnostics from hash-pinned finite spectral rows.

This script defines no adjudication rule and consumes no earlier verdict.  It
checks the A009--A016 sector data directly, then compares two distinct
finite-size diagnostics at q=L/2:

  * the authenticated m=1 density-response gap; and
  * the neighboring-charge curvature E(q+1)+E(q-1)-2E(q).

For all selected L10/L12 sectors, the independently implemented Target and
Blind rows must agree numerically.  Every consumed input is checked against a
digest pinned in this script.  Positive finite-L spectral weight is reported
as numerical evidence; it is not promoted to an all-L theorem.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOW_RESULT = (
    ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json"
)
TARGET_RUN = (
    ROOT
    / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001"
    / "RUN_V002_L12_V003R1_STAGE6R2"
)
BLIND_RUN = (
    ROOT
    / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_COMPATIBILITY_V001"
    / "RUN_V002_L12_V003R1_STAGE6R2"
)
TARGET = TARGET_RUN / "RAW"
BLIND = BLIND_RUN / "RAW"
TARGET_INDEX = TARGET_RUN / "SPECTRUM_INDEX.json"
BLIND_INDEX = BLIND_RUN / "SPECTRUM_INDEX.json"
MANIFEST = (
    ROOT
    / "DEVELOPMENT_R_L4_L12_SECTOR_MANIFEST_BRIDGE_V003"
    / "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V003R1.json"
)
# This is a local consistency guard, not an imported classification threshold.
NUMERICAL_AGREEMENT_TOLERANCE = 1.0e-10
EXPECTED_MANIFEST_SHA256 = (
    "292124df4e1d349827753145ce1dd4be32e073db6d657f30737227edd488184a"
)
EXPECTED_LOW_RESULT_SHA256 = (
    "ebd522411a0e7f67e37d5023fbdea01bc63bdd796ca23020b0d749b414146a05"
)
EXPECTED_TARGET_INDEX_SHA256 = (
    "157e9ae1a54a77dfeef51287dd0d479bc4126a3181388ea2a4bafc22728de749"
)
EXPECTED_BLIND_INDEX_SHA256 = (
    "f57488d2286df964599885d42556f1ea509ca41ab69f46dfaa78125efcf66994"
)
BAND_ATOM_IDS = tuple(f"A{index:03d}" for index in range(9, 17))
BAND_INTERVAL = (Fraction(7, 48), Fraction(13, 48))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_sha256(path: Path, expected: str, label: str) -> str:
    actual = sha256(path)
    if actual != expected:
        raise RuntimeError(
            f"{label} SHA-256 mismatch: expected {expected}, found {actual}"
        )
    return actual


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise RuntimeError(f"expected a JSON object at {path}")
    return value


def response_weight(value: dict[str, object]) -> float:
    if "response_total_excited_weight" in value:
        return float(value["response_total_excited_weight"])
    sequence = value.get("response_sequence")
    if isinstance(sequence, list) and sequence and isinstance(sequence[-1], dict):
        total_weight = sequence[-1].get("total_weight")
        if total_weight is not None:
            return float(total_weight)
    return float(value["response_full_norm_squared"])


def require_row_evidence(
    value: dict[str, object], length: int, charge: int, label: str
) -> None:
    if value.get("L") != length or value.get("q") != charge:
        raise RuntimeError(f"{label} row identity mismatch at L={length}, q={charge}")
    for field in ("ground_energy", "Delta_act", "R_low", "chi_tau"):
        number = float(value[field])
        if not math.isfinite(number):
            raise RuntimeError(
                f"{label} row has non-finite {field} at L={length}, q={charge}"
            )
    if float(value["Delta_act"]) <= 0.0:
        raise RuntimeError(f"{label} row has non-positive gap at L={length}, q={charge}")
    if not 0.0 < float(value["R_low"]) <= 1.0:
        raise RuntimeError(f"{label} row has invalid residue at L={length}, q={charge}")
    if float(value["chi_tau"]) <= 0.0 or response_weight(value) <= 0.0:
        raise RuntimeError(f"{label} row has non-positive response at L={length}, q={charge}")

    # Validate numerical diagnostics directly rather than trusting a historical
    # status string.  The two data formats expose different residual names.
    if "unresolved_reasons" in value and value["unresolved_reasons"] != []:
        raise RuntimeError(f"{label} row records unresolved numerical checks")
    if value.get("threshold_stable") is not True:
        raise RuntimeError(f"{label} row has an unstable active-pole threshold")
    for field in (
        "ground_residual",
        "active_actual_residual",
        "active_pole_residual_max",
        "response_projection_error",
    ):
        if field in value:
            residual = float(value[field])
            if not math.isfinite(residual) or residual > 1.0e-9:
                raise RuntimeError(
                    f"{label} row has excessive {field} at L={length}, q={charge}"
                )


def sealed_low_row(
    low_result: dict[str, object], length: int, charge: int
) -> dict[str, object]:
    sector_rows = low_result.get("sector_rows")
    if not isinstance(sector_rows, dict):
        raise RuntimeError("sealed low-size result has no sector_rows object")
    rows = sector_rows.get(str(length))
    if not isinstance(rows, list) or not 0 <= charge < len(rows):
        raise RuntimeError(f"sealed low-size row is missing at L={length}, q={charge}")
    value = rows[charge]
    if not isinstance(value, dict):
        raise RuntimeError(f"sealed low-size row is malformed at L={length}, q={charge}")
    require_row_evidence(value, length, charge, "sealed low-size")
    return value


def indexed_row(
    index: dict[str, object], directory: Path, length: int, charge: int, label: str
) -> dict[str, object]:
    rows = index.get("rows")
    if not isinstance(rows, dict):
        raise RuntimeError(f"{label} index has no rows object")
    entry = rows.get(f"{length}:{charge}")
    if not isinstance(entry, dict):
        raise RuntimeError(f"{label} index is missing L={length}, q={charge}")
    expected_path = (directory / f"SECTOR_L{length}_Q{charge}.json").resolve()
    recorded_path = entry.get("path")
    if not isinstance(recorded_path, str):
        raise RuntimeError(f"{label} index row path is malformed")
    path = (ROOT / recorded_path).resolve()
    if path != expected_path:
        raise RuntimeError(
            f"{label} index path mismatch at L={length}, q={charge}: {path}"
        )
    expected_sha = entry.get("sha256")
    if not isinstance(expected_sha, str):
        raise RuntimeError(f"{label} index row digest is malformed")
    require_sha256(path, expected_sha, f"{label} row L={length}, q={charge}")
    value = read_json(path)
    require_row_evidence(value, length, charge, label)
    return value


def validated_atoms(
    manifest: dict[str, object],
    atom_ids: tuple[str, ...],
    expected_interval: tuple[Fraction, Fraction],
    label: str,
) -> list[dict[str, object]]:
    raw_atoms = manifest.get("atoms")
    if not isinstance(raw_atoms, list):
        raise RuntimeError("authenticated manifest has no atoms list")
    by_id = {
        atom.get("atom_id"): atom
        for atom in raw_atoms
        if isinstance(atom, dict) and isinstance(atom.get("atom_id"), str)
    }
    if any(atom_id not in by_id for atom_id in atom_ids):
        raise RuntimeError(f"authenticated manifest is missing a {label} atom")
    atoms = [by_id[atom_id] for atom_id in atom_ids]
    intervals: list[tuple[Fraction, Fraction]] = []
    for atom in atoms:
        interval = atom.get("density_interval")
        if (
            not isinstance(interval, list)
            or len(interval) != 2
            or any(not isinstance(endpoint, list) or len(endpoint) != 2 for endpoint in interval)
        ):
            raise RuntimeError(f"{label} atom has a malformed density interval")
        lower = Fraction(int(interval[0][0]), int(interval[0][1]))
        upper = Fraction(int(interval[1][0]), int(interval[1][1]))
        if not lower < upper:
            raise RuntimeError(f"{label} atom has a non-positive density interval")
        intervals.append((lower, upper))
    if intervals[0][0] != expected_interval[0] or intervals[-1][1] != expected_interval[1]:
        raise RuntimeError(f"{label} envelope endpoints do not match the frozen declaration")
    if any(left[1] != right[0] for left, right in zip(intervals, intervals[1:])):
        raise RuntimeError(f"{label} atoms are not a contiguous manifest envelope")
    return atoms


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def power_exponent(lengths: list[int], values: list[float]) -> float:
    if len(lengths) != len(values) or len(lengths) < 2:
        raise ValueError("power fit requires equal-length inputs with at least two rows")
    if any(length <= 0 for length in lengths):
        raise ValueError("power fit lengths must be positive")
    if any(not math.isfinite(value) or value <= 0.0 for value in values):
        raise ValueError("power fit values must be finite and positive")
    xs = [math.log(length) for length in lengths]
    ys = [math.log(value) for value in values]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / sum(
        (x - xbar) ** 2 for x in xs
    )
    return -slope


def relative_range(values: list[float]) -> float:
    if not values or any(not math.isfinite(value) or value <= 0.0 for value in values):
        raise ValueError("relative-range values must be finite and positive")
    return (max(values) - min(values)) / (math.fsum(values) / len(values))


def response_support_diagnostics(
    center: dict[str, object], length: int
) -> dict[str, float]:
    spectral_weight = response_weight(center)
    residue = float(center["R_low"])
    chi_tau = float(center["chi_tau"])
    if not math.isfinite(spectral_weight) or spectral_weight <= 0.0:
        raise RuntimeError(f"response weight S is not finite and positive at L={length}")
    if not math.isfinite(residue) or not 0.0 < residue <= 1.0:
        raise RuntimeError(f"R_low is outside (0,1] at L={length}")
    if not math.isfinite(chi_tau) or chi_tau <= 0.0:
        raise RuntimeError(f"chi_tau is not finite and positive at L={length}")
    lowest_pole_weight = spectral_weight * residue
    m_minus2_over_l2 = spectral_weight * (chi_tau / length) ** 2
    if not math.isfinite(lowest_pole_weight) or lowest_pole_weight <= 0.0:
        raise RuntimeError(f"w_star is not finite and positive at L={length}")
    if not math.isfinite(m_minus2_over_l2) or m_minus2_over_l2 <= 0.0:
        raise RuntimeError(f"m_minus2/L^2 is not finite and positive at L={length}")
    return {
        "response_weight_S": spectral_weight,
        "R_low": residue,
        "lowest_pole_weight_w_star": lowest_pole_weight,
        "chi_tau_over_L": chi_tau / length,
        "m_minus2_over_L2": m_minus2_over_l2,
    }


def main() -> None:
    lengths = [4, 6, 8, 10, 12]
    manifest_sha = require_sha256(
        MANIFEST, EXPECTED_MANIFEST_SHA256, "A009--A016 source manifest"
    )
    low_result_sha = require_sha256(
        LOW_RESULT, EXPECTED_LOW_RESULT_SHA256, "L4--L8 finite-spectrum data"
    )
    target_index_sha = require_sha256(
        TARGET_INDEX, EXPECTED_TARGET_INDEX_SHA256, "L10/L12 Target index"
    )
    blind_index_sha = require_sha256(
        BLIND_INDEX, EXPECTED_BLIND_INDEX_SHA256, "L10/L12 Blind index"
    )

    manifest = read_json(MANIFEST)
    if manifest.get("schema") != "AUTHENTICATED_RELATIONAL_SECTOR_MANIFEST_V001":
        raise RuntimeError("unexpected A009--A016 source-manifest schema")
    low_result = read_json(LOW_RESULT)
    if low_result.get("schema") != "R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001":
        raise RuntimeError("unexpected L4--L8 finite-spectrum data schema")

    target_index = read_json(TARGET_INDEX)
    blind_index = read_json(BLIND_INDEX)
    for index, role in ((target_index, "target"), (blind_index, "blind")):
        if index.get("schema") != "RELATIONAL_INTERVAL_SPECTRUM_INDEX_V001":
            raise RuntimeError(f"unexpected {role} spectrum-index schema")
        if index.get("role") != role:
            raise RuntimeError(f"{role} spectrum-index role mismatch")
        if index.get("manifest_sha256") != manifest_sha:
            raise RuntimeError(f"{role} spectrum-index source-manifest mismatch")

    atoms = validated_atoms(manifest, BAND_ATOM_IDS, BAND_INTERVAL, "record-band")
    records: list[dict[str, float | int]] = []
    selected_sector_rows: list[dict[str, object]] = []
    maximum_disagreement = {
        field: 0.0
        for field in (
            "ground_energy",
            "Delta_act",
            "R_low",
            "chi_tau",
            "response_full_norm_squared",
        )
    }
    target_cache: dict[tuple[int, int], dict[str, object]] = {}
    blind_cache: dict[tuple[int, int], dict[str, object]] = {}
    low_cache: dict[tuple[int, int], dict[str, object]] = {}

    def finite_row(length: int, charge: int) -> dict[str, object]:
        key = (length, charge)
        if length <= 8:
            if key not in low_cache:
                low_cache[key] = sealed_low_row(low_result, length, charge)
            return low_cache[key]

        if key not in target_cache:
            target_cache[key] = indexed_row(
                target_index, TARGET, length, charge, "Target"
            )
            blind_cache[key] = indexed_row(
                blind_index, BLIND, length, charge, "Blind"
            )
            for field in maximum_disagreement:
                disagreement = relative_difference(
                    float(target_cache[key][field]), float(blind_cache[key][field])
                )
                maximum_disagreement[field] = max(
                    maximum_disagreement[field], disagreement
                )
                if disagreement > NUMERICAL_AGREEMENT_TOLERANCE:
                    raise RuntimeError(
                        f"Target/Blind {field} mismatch at L={length}, q={charge}: "
                        f"{disagreement:.3e}"
                    )
        return target_cache[key]

    for length in lengths:
        charge = length // 2
        center = finite_row(length, charge)
        below = finite_row(length, charge - 1)
        above = finite_row(length, charge + 1)

        curvature = (
            float(above["ground_energy"])
            + float(below["ground_energy"])
            - 2.0 * float(center["ground_energy"])
        )
        gap = float(center["Delta_act"])
        if not math.isfinite(curvature) or curvature <= 0.0:
            raise RuntimeError(f"charge curvature is not finite and positive at L={length}")
        if not math.isfinite(gap) or gap <= 0.0:
            raise RuntimeError(f"density-response gap is not finite and positive at L={length}")
        velocity_estimator = length * gap / (2.0 * math.pi)
        compressibility_estimator = 1.0 / (2.0 * length * curvature)
        k_s_estimator = math.pi * compressibility_estimator * velocity_estimator
        support = response_support_diagnostics(center, length)
        band_charges = sorted({int(atom["q_by_L"][str(length)]) for atom in atoms})
        pbar = manifest["histories"][str(length)]["pbar_q"]
        if band_charges != list(range(band_charges[0], band_charges[-1] + 1)):
            raise RuntimeError(f"record-band sectors are not contiguous at L={length}")
        band_mass = math.fsum(float(pbar[q]) for q in band_charges)

        for selected_charge in band_charges:
            row = finite_row(length, selected_charge)
            row_support = response_support_diagnostics(row, length)
            selected_sector_rows.append(
                {
                    "L": length,
                    "q": selected_charge,
                    "density_per_site": selected_charge / (2.0 * length),
                    "atoms": [
                        str(atom["atom_id"])
                        for atom in atoms
                        if int(atom["q_by_L"][str(length)]) == selected_charge
                    ],
                    "Delta_act": float(row["Delta_act"]),
                    "chi_tau": float(row["chi_tau"]),
                    **row_support,
                }
            )

        records.append(
            {
                "L": length,
                "q": charge,
                "density_per_site": charge / (2.0 * length),
                "density_gap": gap,
                "L_density_gap": length * gap,
                "charge_curvature": curvature,
                "L_charge_curvature": length * curvature,
                "velocity_estimator_from_density_gap": velocity_estimator,
                "compressibility_estimator_from_charge_curvature": (
                    compressibility_estimator
                ),
                # With rho=N/(2L), Delta_Q^{-1}/(2L) estimates kappa;
                # the ladder hydrodynamic convention is K_s=pi*kappa*v.
                "K_s_estimator": k_s_estimator,
                **support,
                "band_q_min": band_charges[0],
                "band_q_max": band_charges[-1],
                "band_pbar_mass": band_mass,
            }
        )

    gaps = [float(record["density_gap"]) for record in records]
    curvatures = [float(record["charge_curvature"]) for record in records]
    scaled_gaps = [float(record["L_density_gap"]) for record in records]
    scaled_curvatures = [
        float(record["L_charge_curvature"]) for record in records
    ]
    result = {
        "schema": "Z1_NATIVE_FINITE_EVIDENCE_V001",
        "status": "FINITE_NUMERICAL_EVIDENCE_ONLY__NO_THERMODYNAMIC_VERDICT",
        "source_integrity": {
            "manifest_sha256": manifest_sha,
            "L4_L8_result_sha256": low_result_sha,
            "target_index_sha256": target_index_sha,
            "blind_index_sha256": blind_index_sha,
            "indexed_target_rows_verified": len(target_cache),
            "indexed_blind_rows_verified": len(blind_cache),
            "low_rows_consumed": len(low_cache),
        },
        "record_band": {
            "atoms": list(BAND_ATOM_IDS),
            "density_interval": [[7, 48], [13, 48]],
            "masses_by_L": {
                str(record["L"]): record["band_pbar_mass"] for record in records
            },
            "all_sizes_cross_half": all(
                float(record["band_pbar_mass"]) > 0.5 for record in records
            ),
        },
        "finite_selected_sector_visibility": {
            "interpretation": (
                "direct finite-size spectral observations; not an all-L residue bound"
            ),
            "all_selected_rows_positive": all(
                float(row["lowest_pole_weight_w_star"]) > 0.0
                for row in selected_sector_rows
            ),
            "minimum_R_low": min(
                float(row["R_low"]) for row in selected_sector_rows
            ),
            "minimum_w_star": min(
                float(row["lowest_pole_weight_w_star"])
                for row in selected_sector_rows
            ),
            "rows": selected_sector_rows,
        },
        "centerline_records": records,
        "finite_size_fits": {
            "density_gap_power_exponent": power_exponent(lengths, gaps),
            "charge_curvature_power_exponent": power_exponent(
                lengths, curvatures
            ),
            "tail_L_density_gap_relative_range": relative_range(scaled_gaps[2:]),
            "tail_L_charge_curvature_relative_range": relative_range(
                scaled_curvatures[2:]
            ),
        },
        "maximum_L10_L12_target_blind_relative_difference_by_field": (
            maximum_disagreement
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
