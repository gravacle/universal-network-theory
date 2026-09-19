#!/usr/bin/env python3
"""Audit a proposed Gaussian reduction for the relational mass ledger.

This module tests whether number-sector probabilities can be reduced to a
small carrier covariance.  Such a reduction would be exact for genuinely
quadratic fermionic hopping plus the fresh-source partial swaps.  The frozen
many-body engine instead implements sign-free hard-core hopping on a graph
with loops, so the proposition must be tested rather than assumed.  This
module never replaces the many-body response calculation used to obtain
Delta_act, chi_tau, z, or y.

Two internally equivalent Gaussian constructions are evaluated:

* ``reduced`` applies the induced covariance channel directly on 2L modes;
* ``global`` evolves all 3L carrier/source one-particle modes and traces the
  source block only when observables are requested.

Their agreement is necessary but not sufficient.  The candidate must also
reproduce every preserved L4--L12 many-body sector ledger.  A failed
regression publishes only a reduction-obstruction record; its L14 candidate
numbers are never exposed as physical sector masses.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LENGTH = 14
PHI = math.pi / 4.0
DWELL = math.pi / 2.0
REPORTING_MASS = 0.99
COMPARISON_TOLERANCE = 2.0e-8
SCRATCH_LIMIT_BYTES = 20 * 2**30
SCHEMA = "L14_MASS_LEDGER_REDUCTION_AUDIT_V001"

PHYSICS_SOURCE = (
    ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "compute_streamed_history.py"
)
PROTOCOL_SOURCE = (
    ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "PROTOCOL.md"
)

REFERENCE_HISTORIES = {
    4: ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "RAW_HISTORY"
    / "HISTORY_L4.json",
    6: ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "RAW_HISTORY"
    / "HISTORY_L6.json",
    8: ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "RAW_HISTORY"
    / "HISTORY_L8.json",
    10: ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "RAW_HISTORY"
    / "STREAMED_HISTORY_L10_V002.json",
    12: ROOT
    / "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012"
    / "PHYSICAL_OUTPUTS"
    / "HISTORY_L12_PROCESS_PARALLEL_V003R1.json",
}


class LedgerRefusal(RuntimeError):
    """The exact-reduction identity or evidence contract failed closed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def graph(length: int) -> list[tuple[int, int, str]]:
    """Reproduce the frozen periodic-prism carrier graph."""

    edges: list[tuple[int, int, str]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append(
                (offset + site, offset + (site + 1) % length, f"rail_{rail + 1}")
            )
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def one_particle_transport(length: int) -> np.ndarray:
    """Return exp(-i * DWELL * h) for the frozen hopping Hamiltonian."""

    sites = 2 * length
    hamiltonian = np.zeros((sites, sites), dtype=np.float64)
    for left, right, _kind in graph(length):
        hamiltonian[left, right] -= 1.0
        hamiltonian[right, left] -= 1.0
    values, vectors = np.linalg.eigh(hamiltonian)
    return np.einsum(
        "ik,k,jk->ij",
        vectors,
        np.exp(-1.0j * DWELL * values),
        vectors,
        optimize=False,
    )


def similarity(unitary: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    """Compute U C U^dagger without dispatching to threaded BLAS."""

    return np.einsum(
        "ia,ab,jb->ij", unitary, covariance, unitary.conj(), optimize=False
    )


def sector_probabilities(covariance: np.ndarray) -> np.ndarray:
    """Full counting statistics of a gauge-invariant Gaussian state."""

    eigenvalues = np.linalg.eigvalsh((covariance + covariance.conj().T) / 2.0)
    if float(np.min(eigenvalues)) < -5.0e-12 or float(np.max(eigenvalues)) > 1.0 + 5.0e-12:
        raise LedgerRefusal("carrier covariance eigenvalue left [0,1]")
    eigenvalues = np.clip(eigenvalues, 0.0, 1.0)
    probabilities = np.array([1.0], dtype=np.float64)
    for value in eigenvalues:
        updated = np.zeros(len(probabilities) + 1, dtype=np.float64)
        updated[:-1] += probabilities * (1.0 - value)
        updated[1:] += probabilities * value
        probabilities = updated
    probabilities[np.abs(probabilities) < 5.0e-16] = 0.0
    return probabilities


def _row(event: int, covariance: np.ndarray, maximum_particles: int) -> dict[str, Any]:
    all_probabilities = sector_probabilities(covariance)
    discarded = float(np.sum(np.abs(all_probabilities[maximum_particles + 1 :])))
    if discarded > 5.0e-12:
        raise LedgerRefusal("number distribution exceeds available source particles")
    probabilities = all_probabilities[: maximum_particles + 1]
    eigenvalues = np.linalg.eigvalsh((covariance + covariance.conj().T) / 2.0)
    return {
        "event": event + 1,
        "cursor_vertex": event,
        "sector_weights": probabilities.tolist(),
        "sector_norm_error": abs(float(np.sum(probabilities)) - 1.0),
        "mean_retained_number": float(
            np.dot(np.arange(len(probabilities), dtype=np.float64), probabilities)
        ),
        "covariance_trace": float(np.trace(covariance).real),
        "covariance_min_eigenvalue": float(np.min(eigenvalues)),
        "covariance_max_eigenvalue": float(np.max(eigenvalues)),
    }


def reduced_history(length: int) -> list[dict[str, Any]]:
    """Direct 2L-mode covariance-channel construction."""

    sites = 2 * length
    transport = one_particle_transport(length)
    covariance = np.zeros((sites, sites), dtype=np.complex128)
    cosine = math.cos(PHI)
    sine_squared = math.sin(PHI) ** 2
    rows: list[dict[str, Any]] = []
    for event in range(length):
        attenuation = np.ones(sites, dtype=np.float64)
        attenuation[event] = cosine
        covariance = attenuation[:, None] * covariance * attenuation[None, :]
        covariance[event, event] += sine_squared
        rows.append(_row(event, covariance, length))
        covariance = similarity(transport, covariance)
    return rows


def global_history(length: int) -> list[dict[str, Any]]:
    """Independent 3L-mode unitary construction with an explicit source."""

    carrier_sites = 2 * length
    total_sites = 3 * length
    carrier_transport = one_particle_transport(length)
    transport = np.eye(total_sites, dtype=np.complex128)
    transport[:carrier_sites, :carrier_sites] = carrier_transport
    covariance = np.zeros((total_sites, total_sites), dtype=np.complex128)
    covariance[carrier_sites:, carrier_sites:] = np.eye(length)
    cosine = math.cos(PHI)
    sine = math.sin(PHI)
    rows: list[dict[str, Any]] = []
    for event in range(length):
        source = carrier_sites + event
        beam_splitter = np.eye(total_sites, dtype=np.complex128)
        beam_splitter[event, event] = cosine
        beam_splitter[source, source] = cosine
        beam_splitter[event, source] = -1.0j * sine
        beam_splitter[source, event] = -1.0j * sine
        covariance = similarity(beam_splitter, covariance)
        rows.append(
            _row(event, covariance[:carrier_sites, :carrier_sites], length)
        )
        covariance = similarity(transport, covariance)
    return rows


def maximum_row_difference(
    left: Sequence[Mapping[str, Any]], right: Sequence[Mapping[str, Any]]
) -> float:
    if len(left) != len(right):
        raise LedgerRefusal("history row census mismatch")
    maximum = 0.0
    for left_row, right_row in zip(left, right):
        left_weights = np.asarray(left_row["sector_weights"], dtype=np.float64)
        right_weights = np.asarray(right_row["sector_weights"], dtype=np.float64)
        width = max(len(left_weights), len(right_weights))
        left_weights = np.pad(left_weights, (0, width - len(left_weights)))
        right_weights = np.pad(right_weights, (0, width - len(right_weights)))
        maximum = max(maximum, float(np.max(np.abs(left_weights - right_weights))))
    return maximum


def late_average(rows: Sequence[Mapping[str, Any]], length: int) -> np.ndarray:
    first = math.ceil(length / 2) - 1
    weights = np.asarray(
        [row["sector_weights"] for row in rows[first:]], dtype=np.float64
    )
    return np.mean(weights, axis=0)


def shortest_interval(probabilities: Sequence[float], target: float) -> tuple[int, int, float]:
    candidates: list[tuple[int, float, int, int]] = []
    for lower in range(len(probabilities)):
        mass = 0.0
        for upper in range(lower, len(probabilities)):
            mass += float(probabilities[upper])
            if mass + 1.0e-15 >= target:
                candidates.append((upper - lower, -mass, lower, upper))
                break
    if not candidates:
        raise LedgerRefusal("no contiguous sector interval reaches reporting mass")
    _width, negative_mass, lower, upper = min(candidates)
    return lower, upper, -negative_mass


def legacy_state_bytes(length: int, prefix: int, maximum_q: int | None = None) -> int:
    upper = prefix if maximum_q is None else min(prefix, maximum_q)
    return 16 * sum(
        math.comb(prefix, q) * math.comb(2 * length, q) for q in range(upper + 1)
    )


def resource_comparison(length: int) -> dict[str, Any]:
    previous_prefix = length - 2
    terminal_prefix = length - 1
    modes = 2 * length
    return {
        "legacy_full_terminal_prefix_bytes": legacy_state_bytes(length, terminal_prefix),
        "legacy_full_admission_peak_lower_bound_bytes": (
            legacy_state_bytes(length, previous_prefix)
            + legacy_state_bytes(length, terminal_prefix)
        ),
        "legacy_q0_through_q7_terminal_prefix_bytes": legacy_state_bytes(
            length, terminal_prefix, 7
        ),
        "legacy_q0_through_q7_admission_peak_lower_bound_bytes": (
            legacy_state_bytes(length, previous_prefix, 7)
            + legacy_state_bytes(length, terminal_prefix, 7)
        ),
        "legacy_q0_through_q9_terminal_prefix_bytes": legacy_state_bytes(
            length, terminal_prefix, 9
        ),
        "legacy_q0_through_q9_admission_peak_lower_bound_bytes": (
            legacy_state_bytes(length, previous_prefix, 9)
            + legacy_state_bytes(length, terminal_prefix, 9)
        ),
        "frozen_l12_scratch_limit_bytes": SCRATCH_LIMIT_BYTES,
        "reduced_covariance_payload_bytes": modes * modes * 16,
        "global_covariance_payload_bytes": (3 * length) ** 2 * 16,
    }


def regression_validation() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    overall = 0.0
    for length, path in REFERENCE_HISTORIES.items():
        if not path.is_file():
            raise LedgerRefusal(f"preserved reference history absent: {path}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        observed = payload.get("rows")
        if not isinstance(observed, list):
            raise LedgerRefusal(f"reference history rows absent: {path}")
        expected = reduced_history(length)
        difference = maximum_row_difference(expected, observed)
        overall = max(overall, difference)
        records.append(
            {
                "L": length,
                "path": str(path.resolve()),
                "sha256": sha256_file(path),
                "maximum_sector_weight_difference": difference,
                "passed": difference <= COMPARISON_TOLERANCE,
            }
        )
    return {
        "tolerance": COMPARISON_TOLERANCE,
        "maximum_sector_weight_difference": overall,
        "histories": records,
        "passed": all(record["passed"] for record in records),
    }


def owner_once_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        encoded = (
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")
        offset = 0
        while offset < len(encoded):
            written = os.write(descriptor, encoded[offset:])
            if written <= 0:
                raise LedgerRefusal("owner-once output write made no progress")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
    finally:
        os.close(descriptor)


def build_audit() -> dict[str, Any]:
    reduced = reduced_history(LENGTH)
    global_rows = global_history(LENGTH)
    construction_difference = maximum_row_difference(reduced, global_rows)
    if construction_difference > 2.0e-12:
        raise LedgerRefusal(
            "reduced/global Gaussian constructions disagree: "
            f"{construction_difference:.17g}"
        )
    regression = regression_validation()
    passed = bool(regression["passed"])
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "classification": (
            "EXACT_GAUSSIAN_MASS_REDUCTION_VALIDATED"
            if passed
            else "GAUSSIAN_MASS_REDUCTION_REFUTED_BY_PRESERVED_HISTORY"
        ),
        "L": LENGTH,
        "authentication": {
            "reduced_global_maximum_sector_weight_difference": construction_difference,
            "reduced_global_tolerance": 2.0e-12,
            "passed": True,
        },
        "regression_validation": regression,
        "resource_comparison": resource_comparison(LENGTH),
        "source": {
            "physics_path": str(PHYSICS_SOURCE.resolve()),
            "physics_sha256": sha256_file(PHYSICS_SOURCE),
            "protocol_path": str(PROTOCOL_SOURCE.resolve()),
            "protocol_sha256": sha256_file(PROTOCOL_SOURCE),
            "implementation_sha256": sha256_file(Path(__file__)),
        },
        "decision": (
            "ELIGIBLE_AS_EXACT_L14_MASS_LEDGER"
            if passed
            else "REJECT_REDUCTION__DO_NOT_USE_FOR_L14_MASS_OR_GATE"
        ),
        "claim_boundary": "REDUCTION_AUDIT_ONLY__NO_L14_PHYSICAL_MASS_SPECTRUM_Z_Y_OR_GRAVITY",
    }
    if passed:
        pbar = late_average(reduced, LENGTH)
        q_lower, q_upper, interval_mass = shortest_interval(pbar, REPORTING_MASS)
        result.update(
            {
                "events": LENGTH,
                "reporting_window_events": list(
                    range(math.ceil(LENGTH / 2), LENGTH + 1)
                ),
                "rows": reduced,
                "pbar": pbar.tolist(),
                "sector_masses": {
                    str(q): float(value) for q, value in enumerate(pbar)
                },
                "shortest_contiguous_99pct_interval": {
                    "q_lower": q_lower,
                    "q_upper": q_upper,
                    "mass": interval_mass,
                    "density_interval": [
                        [2 * q_lower - 1, 4 * LENGTH],
                        [2 * q_upper + 1, 4 * LENGTH],
                    ],
                },
            }
        )
    return result


def print_summary(payload: Mapping[str, Any]) -> None:
    regression = payload["regression_validation"]
    print(
        "L14_MASS_REDUCTION_AUDIT "
        f"classification={payload['classification']} "
        f"passed={str(regression['passed']).lower()} "
        f"max_difference={regression['maximum_sector_weight_difference']:.17g}"
    )
    for record in regression["histories"]:
        print(
            f"L{record['L']}_REGRESSION "
            f"difference={record['maximum_sector_weight_difference']:.17g} "
            f"passed={str(record['passed']).lower()}"
        )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(list(argv) if argv is not None else None)
    try:
        payload = build_audit()
        print_summary(payload)
        if arguments.output is not None:
            owner_once_json(arguments.output.resolve(), payload)
            print(f"L14_MASS_LEDGER_OUTPUT {arguments.output.resolve()}")
        else:
            print("L14_MASS_LEDGER_OUTPUT none")
        return 0 if payload["regression_validation"]["passed"] else 20
    except (LedgerRefusal, OSError, ValueError, np.linalg.LinAlgError) as error:
        print(f"L14_MASS_LEDGER_REFUSAL {type(error).__name__}: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
