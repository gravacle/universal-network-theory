#!/usr/bin/env python3
"""Target implementation of the frozen owner-once joint witness protocol.

This source may import the historical dense seed engine for dynamics.  All
witness, sham, shuffle, marginal, and streaming accumulators are implemented
locally from the frozen equations.  Execution is deliberately guarded: source
and synthetic tests can be frozen before any mandatory L4/L6/L8 output is
opened.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Mapping, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = HERE / "PROTOCOL.md"
PROTOCOL_SHA256 = "70984a927c30585704622dfd03ee91bf516cd9a5d14474a228d231144e5e513e"
HISTORICAL_TARGET = (
    ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "compute_seed_history.py"
)
DEFAULT_OUTPUT = HERE / "TARGET_WITNESS_RESULT_V001.json"
SCHEMA = "OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_TARGET_V001"
MANDATORY_LENGTHS = (4, 6, 8)
COARSE_STEPS = 64
FINE_STEPS = 128
TAYLOR_ORDER = 12
PHI = math.pi / 4.0
DWELL = math.pi / 2.0

COARSE_FINE_TOLERANCE = 1.0e-8
NORM_TOLERANCE = 1.0e-10
MARGINAL_TOLERANCE = 1.0e-10
CHARGE_TOLERANCE = 1.0e-10
SHUFFLE_TOLERANCE = 1.0e-12
SHAM_TOLERANCE = 1.0e-12
L4_EXHAUSTIVE_TOLERANCE = 1.0e-12


class WitnessFailure(RuntimeError):
    """A frozen input, finite arithmetic, or audit predicate failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def authenticate_protocol() -> dict[str, str]:
    actual = sha256_file(PROTOCOL)
    if actual != PROTOCOL_SHA256:
        raise WitnessFailure(
            f"frozen protocol SHA-256 mismatch: expected={PROTOCOL_SHA256} actual={actual}"
        )
    return {"path": str(PROTOCOL.relative_to(ROOT)), "sha256": actual}


def finite(value: Any, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise WitnessFailure(f"nonnumeric {label}: {value!r}") from error
    if not math.isfinite(result):
        raise WitnessFailure(f"nonfinite {label}: {result!r}")
    return result


def nonnegative(value: Any, label: str, tolerance: float = 1.0e-15) -> float:
    result = finite(value, label)
    if result < -tolerance:
        raise WitnessFailure(f"negative {label}: {result:.17g}")
    return max(0.0, result)


def require_finite(array: np.ndarray, label: str) -> None:
    if not bool(np.all(np.isfinite(array))):
        raise WitnessFailure(f"nonfinite array: {label}")


def fixed_words(width: int, weight: int) -> np.ndarray:
    dtype = np.uint32 if width <= 32 else np.uint64
    values = np.empty(math.comb(width, weight), dtype=dtype)
    for index, positions in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        values[index] = word
    return values


def bitcount(word: int) -> int:
    # The repository's pinned system Python predates ``int.bit_count``.
    # Binary-string counting is exact for these nonnegative basis words and
    # keeps the frozen combinatorial map portable across the supported host.
    return bin(int(word)).count("1")


def bits(words: np.ndarray, width: int) -> np.ndarray:
    return np.column_stack([((words >> bit) & 1).astype(float) for bit in range(width)])


def load_historical_target() -> ModuleType:
    spec = importlib.util.spec_from_file_location("historical_joint_witness_seed", HISTORICAL_TARGET)
    if spec is None or spec.loader is None:
        raise WitnessFailure(
            "cannot load historical target: "
            f"{HISTORICAL_TARGET.relative_to(ROOT)}"
        )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name, expected in (
        ("PHI", PHI),
        ("KAPPA", DWELL),
        ("TAYLOR_ORDER", TAYLOR_ORDER),
    ):
        actual = finite(getattr(module, name), f"historical {name}")
        if actual != expected:
            raise WitnessFailure(f"historical {name} mismatch: expected={expected} actual={actual}")
    return module


@dataclass(frozen=True)
class SectorGeometry:
    length: int
    q: int
    lineage_words: np.ndarray
    carrier_words: np.ndarray
    lineage_bits: np.ndarray
    carrier_first_rail_bits: np.ndarray
    kernel: np.ndarray

    @classmethod
    def build(cls, length: int, q: int) -> "SectorGeometry":
        lineage_words = fixed_words(length, q)
        carrier_words = fixed_words(2 * length, q)
        lineage_bits = bits(lineage_words, length)
        carrier_first = bits(carrier_words, length)
        # Keep the registered kernel on a fixed, explicit contraction path.
        # This also avoids platform BLAS status-flag warnings for these small
        # binary matrices without changing the arithmetic being registered.
        overlap = np.einsum("se,ce->sc", lineage_bits, carrier_first, optimize=False)
        first_rail_number = np.sum(carrier_first, axis=1)
        kernel = (overlap - (q / length) * first_rail_number[np.newaxis, :]) / length
        require_finite(kernel, f"registered kernel L={length} q={q}")
        return cls(
            length=length,
            q=q,
            lineage_words=lineage_words,
            carrier_words=carrier_words,
            lineage_bits=lineage_bits,
            carrier_first_rail_bits=carrier_first,
            kernel=kernel,
        )


class JointBasis:
    """Independent basis map from dense loaded-bit words to (S,C) blocks."""

    def __init__(self, length: int):
        self.length = length
        self.geometries = [SectorGeometry.build(length, q) for q in range(length + 1)]
        self.lineage_lookup = [
            {int(word): index for index, word in enumerate(geometry.lineage_words)}
            for geometry in self.geometries
        ]
        self.carrier_lookup = [
            {int(word): index for index, word in enumerate(geometry.carrier_words)}
            for geometry in self.geometries
        ]
        self.global_words = fixed_words(3 * length, length)
        loaded_mask = (1 << length) - 1
        by_q: list[list[tuple[int, int, int]]] = [[] for _ in range(length + 1)]
        maximum_charge_mismatch = 0
        maximum_content_mismatch = 0
        for index, raw_word in enumerate(self.global_words):
            word = int(raw_word)
            loaded = word & loaded_mask
            spent = loaded_mask ^ loaded
            carrier = word >> length
            q_s = bitcount(spent)
            q_c = bitcount(carrier)
            maximum_charge_mismatch = max(maximum_charge_mismatch, abs(q_s - q_c))
            maximum_content_mismatch = max(
                maximum_content_mismatch, abs(bitcount(loaded) + q_c - length)
            )
            if q_s != q_c:
                raise WitnessFailure(f"basis charge mismatch at global index {index}")
            by_q[q_s].append(
                (
                    index,
                    self.lineage_lookup[q_s][spent],
                    self.carrier_lookup[q_s][carrier],
                )
            )
        self.maps = [
            (
                np.array([item[0] for item in records], dtype=np.int64),
                np.array([item[1] for item in records], dtype=np.int64),
                np.array([item[2] for item in records], dtype=np.int64),
            )
            for records in by_q
        ]
        self.maximum_charge_mismatch = maximum_charge_mismatch
        self.maximum_content_mismatch = maximum_content_mismatch

    def validate_target_basis(self, parent: object) -> None:
        if not np.array_equal(np.asarray(parent.words), self.global_words):
            raise WitnessFailure("historical dense basis order differs from independent reconstruction")

    def probability_blocks(self, state: np.ndarray) -> list[np.ndarray]:
        require_finite(state, "joint state")
        if state.shape != (len(self.global_words),):
            raise WitnessFailure(
                f"joint state shape mismatch: expected={(len(self.global_words),)} actual={state.shape}"
            )
        probability = np.abs(state) ** 2
        require_finite(probability, "joint probabilities")
        blocks: list[np.ndarray] = []
        for geometry, (indices, rows, columns) in zip(self.geometries, self.maps):
            block = np.zeros(
                (len(geometry.lineage_words), len(geometry.carrier_words)), dtype=float
            )
            block[rows, columns] = probability[indices]
            blocks.append(block)
        return blocks


def _sham_formula(
    geometry: SectorGeometry, lineage_marginal: np.ndarray, carrier_marginal: np.ndarray, p_q: float
) -> float:
    if p_q <= 0.0:
        return 0.0
    centered_lineage = geometry.lineage_bits - geometry.q / geometry.length
    lineage_moments = np.einsum(
        "s,se->e", lineage_marginal, centered_lineage, optimize=False
    )
    carrier_moments = np.einsum(
        "c,ce->e", carrier_marginal, geometry.carrier_first_rail_bits, optimize=False
    )
    return finite(
        np.dot(lineage_moments, carrier_moments) / (geometry.length * p_q),
        f"sham formula q={geometry.q}",
    )


def _sham_direct(
    geometry: SectorGeometry, lineage_marginal: np.ndarray, carrier_marginal: np.ndarray, p_q: float
) -> float:
    if p_q <= 0.0:
        return 0.0
    total = 0.0
    for row in range(len(lineage_marginal)):
        sham_row = (lineage_marginal[row] / p_q) * carrier_marginal
        total += float(np.dot(sham_row, geometry.kernel[row]))
    return finite(total, f"direct sham q={geometry.q}")


def _shuffle_identity(geometry: SectorGeometry, carrier_marginal: np.ndarray) -> tuple[float, float]:
    q = geometry.q
    length = geometry.length
    if q == 0:
        orbit_mean = Fraction(0, 1)
    else:
        orbit_mean = Fraction(math.comb(length - 1, q - 1), math.comb(length, q))
    centered = orbit_mean - Fraction(q, length)
    # The exact Fraction must vanish.  The floating expectation is retained as
    # a reported implementation control rather than assigned by assertion.
    expectation = float(centered) * float(
        np.sum(carrier_marginal[:, np.newaxis] * geometry.carrier_first_rail_bits)
    ) / length
    return finite(expectation, f"shuffle q={q}"), abs(float(centered))


def accumulate_sector_rows(probability: np.ndarray, geometry: SectorGeometry) -> dict[str, Any]:
    require_finite(probability, f"row probability q={geometry.q}")
    if probability.shape != geometry.kernel.shape:
        raise WitnessFailure(f"row block shape mismatch q={geometry.q}")
    if float(np.min(probability)) < 0.0:
        raise WitnessFailure(f"negative row probability q={geometry.q}")
    lineage = np.zeros(probability.shape[0], dtype=float)
    carrier = np.zeros(probability.shape[1], dtype=float)
    observed = 0.0
    for row in range(probability.shape[0]):
        values = probability[row]
        lineage[row] = float(np.sum(values))
        carrier += values
        observed += float(np.dot(values, geometry.kernel[row]))
    p_q = float(np.sum(lineage))
    sham = _sham_formula(geometry, lineage, carrier, p_q)
    sham_direct = _sham_direct(geometry, lineage, carrier, p_q)
    shuffle, shuffle_identity = _shuffle_identity(geometry, carrier)
    return {
        "p_q": finite(p_q, f"row p_q={geometry.q}"),
        "w_q": finite(observed, f"row w_q={geometry.q}"),
        "w_sham_q": sham,
        "D_q": finite(observed - sham, f"row D_q={geometry.q}"),
        "w_shuffle_q": shuffle,
        "lineage_marginal": lineage,
        "carrier_marginal": carrier,
        "sham_direct": sham_direct,
        "sham_self_covariance_residual": abs(sham_direct - sham),
        "shuffle_identity_residual": shuffle_identity,
    }


def accumulate_sector_columns(probability: np.ndarray, geometry: SectorGeometry) -> dict[str, Any]:
    require_finite(probability, f"column probability q={geometry.q}")
    if probability.shape != geometry.kernel.shape:
        raise WitnessFailure(f"column block shape mismatch q={geometry.q}")
    if float(np.min(probability)) < 0.0:
        raise WitnessFailure(f"negative column probability q={geometry.q}")
    lineage = np.zeros(probability.shape[0], dtype=float)
    carrier = np.zeros(probability.shape[1], dtype=float)
    observed = 0.0
    for column in range(probability.shape[1]):
        values = probability[:, column]
        carrier[column] = float(np.sum(values))
        lineage += values
        observed += float(np.dot(values, geometry.kernel[:, column]))
    p_q = float(np.sum(carrier))
    sham = _sham_formula(geometry, lineage, carrier, p_q)
    sham_direct = _sham_direct(geometry, lineage, carrier, p_q)
    shuffle, shuffle_identity = _shuffle_identity(geometry, carrier)
    return {
        "p_q": finite(p_q, f"column p_q={geometry.q}"),
        "w_q": finite(observed, f"column w_q={geometry.q}"),
        "w_sham_q": sham,
        "D_q": finite(observed - sham, f"column D_q={geometry.q}"),
        "w_shuffle_q": shuffle,
        "lineage_marginal": lineage,
        "carrier_marginal": carrier,
        "sham_direct": sham_direct,
        "sham_self_covariance_residual": abs(sham_direct - sham),
        "shuffle_identity_residual": shuffle_identity,
    }


def permute_word(word: int, permutation: Sequence[int]) -> int:
    answer = 0
    for source, destination in enumerate(permutation):
        if (word >> source) & 1:
            answer |= 1 << destination
    return answer


def exhaustive_controls(
    blocks: Sequence[np.ndarray], geometries: Sequence[SectorGeometry]
) -> dict[str, Any]:
    length = geometries[0].length
    if length != 4:
        raise WitnessFailure("exhaustive permutation control is frozen only at L4")
    permutations = tuple(itertools.permutations(range(length)))
    direct_w = direct_sham = permutation_shuffle = 0.0
    sectors: dict[str, dict[str, float]] = {}
    for q, (probability, geometry) in enumerate(zip(blocks, geometries)):
        row = accumulate_sector_rows(probability, geometry)
        p_q = float(row["p_q"])
        ps = np.asarray(row["lineage_marginal"])
        pc = np.asarray(row["carrier_marginal"])
        sector_w = 0.0
        sector_sham = 0.0
        sector_shuffle = 0.0
        for s_index, s_word_raw in enumerate(geometry.lineage_words):
            s_word = int(s_word_raw)
            for c_index, c_word_raw in enumerate(geometry.carrier_words):
                c_word = int(c_word_raw)
                probability_value = float(probability[s_index, c_index])
                kernel_value = float(geometry.kernel[s_index, c_index])
                sector_w += probability_value * kernel_value
                if p_q > 0.0:
                    sector_sham += (ps[s_index] * pc[c_index] / p_q) * kernel_value
                if probability_value:
                    for permutation in permutations:
                        permuted = permute_word(s_word, permutation)
                        overlap = sum(
                            ((permuted >> event) & 1) * ((c_word >> event) & 1)
                            for event in range(length)
                        )
                        first_rail_number = sum((c_word >> event) & 1 for event in range(length))
                        value = (
                            overlap - (q / length) * first_rail_number
                        ) / length
                        sector_shuffle += probability_value * value / len(permutations)
        direct_w += sector_w
        direct_sham += sector_sham
        permutation_shuffle += sector_shuffle
        sectors[str(q)] = {
            "p_q": p_q,
            "w_q": finite(sector_w, f"L4 exhaustive w q={q}"),
            "w_sham_q": finite(sector_sham, f"L4 exhaustive sham q={q}"),
            "D_q": finite(sector_w - sector_sham, f"L4 exhaustive D q={q}"),
            "w_shuffle_q": finite(sector_shuffle, f"L4 exhaustive shuffle q={q}"),
        }
    return {
        "permutation_count": len(permutations),
        "w": finite(direct_w, "L4 exhaustive w"),
        "w_sham": finite(direct_sham, "L4 exhaustive sham"),
        "D": finite(direct_w - direct_sham, "L4 exhaustive D"),
        "w_shuffle": finite(permutation_shuffle, "L4 permutation shuffle"),
        "sectors": sectors,
    }


def public_accumulator(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in record.items()
        if key not in ("lineage_marginal", "carrier_marginal", "sham_direct")
    }


def evaluate_probability_blocks(
    blocks: Sequence[np.ndarray], geometries: Sequence[SectorGeometry], *, l4_exhaustive: bool = False
) -> dict[str, Any]:
    if len(blocks) != len(geometries):
        raise WitnessFailure("probability block count mismatch")
    row_records = [
        accumulate_sector_rows(probability, geometry)
        for probability, geometry in zip(blocks, geometries)
    ]
    column_records = [
        accumulate_sector_columns(probability, geometry)
        for probability, geometry in zip(blocks, geometries)
    ]

    def totals(records: Sequence[Mapping[str, Any]]) -> dict[str, float]:
        return {
            "probability": finite(sum(float(item["p_q"]) for item in records), "probability"),
            "w": finite(sum(float(item["w_q"]) for item in records), "w"),
            "w_sham": finite(sum(float(item["w_sham_q"]) for item in records), "w_sham"),
            "D": finite(sum(float(item["D_q"]) for item in records), "D"),
            "w_shuffle": finite(
                sum(float(item["w_shuffle_q"]) for item in records), "w_shuffle"
            ),
        }

    row_totals = totals(row_records)
    column_totals = totals(column_records)
    audit_disagreement = 0.0
    registered_disagreement = 0.0
    marginal_error = 0.0
    sham_residual = 0.0
    shuffle_residual = 0.0
    for row, column in zip(row_records, column_records):
        for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q"):
            audit_disagreement = max(
                audit_disagreement, abs(float(row[key]) - float(column[key]))
            )
        for key in ("p_q", "D_q"):
            registered_disagreement = max(
                registered_disagreement, abs(float(row[key]) - float(column[key]))
            )
        marginal_error = max(
            marginal_error,
            float(np.max(np.abs(row["lineage_marginal"] - column["lineage_marginal"]))),
            float(np.max(np.abs(row["carrier_marginal"] - column["carrier_marginal"]))),
            abs(float(np.sum(row["lineage_marginal"])) - float(row["p_q"])),
            abs(float(np.sum(row["carrier_marginal"])) - float(row["p_q"])),
        )
        sham_residual = max(
            sham_residual,
            float(row["sham_self_covariance_residual"]),
            float(column["sham_self_covariance_residual"]),
        )
        shuffle_residual = max(
            shuffle_residual,
            abs(float(row["w_shuffle_q"])),
            abs(float(column["w_shuffle_q"])),
            float(row["shuffle_identity_residual"]),
            float(column["shuffle_identity_residual"]),
        )
    for key in row_totals:
        audit_disagreement = max(
            audit_disagreement, abs(row_totals[key] - column_totals[key])
        )
    for key in ("w", "w_sham", "D"):
        registered_disagreement = max(
            registered_disagreement, abs(row_totals[key] - column_totals[key])
        )

    sham_replacement_D = finite(
        sum(float(item["sham_direct"]) - float(item["w_sham_q"]) for item in row_records),
        "sham replacement D",
    )

    result: dict[str, Any] = {
        "registered": row_totals,
        "row_stream": {
            "totals": row_totals,
            "sectors": {str(q): public_accumulator(item) for q, item in enumerate(row_records)},
        },
        "column_stream": {
            "totals": column_totals,
            "sectors": {str(q): public_accumulator(item) for q, item in enumerate(column_records)},
        },
        "q_contributions": {
            str(q): {
                "p_q": float(item["p_q"]),
                "w_q": float(item["w_q"]),
                "w_sham_q": float(item["w_sham_q"]),
                "D_q": float(item["D_q"]),
                "w_shuffle_q": float(item["w_shuffle_q"]),
            }
            for q, item in enumerate(row_records)
        },
        "residuals": {
            "row_column_accumulator": finite(
                audit_disagreement, "row/column audit disagreement"
            ),
            "row_column_d_inputs": finite(
                registered_disagreement, "row/column registered disagreement"
            ),
            "probability_normalization": abs(row_totals["probability"] - 1.0),
            "marginal_reconstruction": finite(marginal_error, "marginal reconstruction"),
            "sham_self_covariance": finite(sham_residual, "sham self covariance"),
            "shuffle_expectation": finite(shuffle_residual, "shuffle expectation"),
        },
        "negative_controls": {
            "sham_replacement_D": sham_replacement_D,
            "sham_replacement_max_sector_D": finite(
                sham_residual, "sham replacement maximum sector D"
            ),
            "shuffle_replacement_w": finite(row_totals["w_shuffle"], "shuffle replacement w"),
        },
    }
    if l4_exhaustive:
        exhaustive = exhaustive_controls(blocks, geometries)
        exhaustive_error = max(
            abs(exhaustive["w"] - row_totals["w"]),
            abs(exhaustive["w_sham"] - row_totals["w_sham"]),
            abs(exhaustive["D"] - row_totals["D"]),
            abs(exhaustive["w_shuffle"] - row_totals["w_shuffle"]),
            *(
                abs(exhaustive["sectors"][str(q)][key] - result["q_contributions"][str(q)][key])
                for q in range(len(geometries))
                for key in ("p_q", "w_q", "w_sham_q", "D_q", "w_shuffle_q")
            ),
        )
        exhaustive["streamed_agreement"] = finite(
            exhaustive_error, "L4 exhaustive/streamed agreement"
        )
        result["l4_exhaustive"] = exhaustive
        result["residuals"]["l4_exhaustive_streamed"] = exhaustive_error
        result["residuals"]["l4_permutation_shuffle"] = abs(exhaustive["w_shuffle"])
    return result


def evaluate_state(state: np.ndarray, basis: JointBasis) -> dict[str, Any]:
    blocks = basis.probability_blocks(state)
    result = evaluate_probability_blocks(
        blocks, basis.geometries, l4_exhaustive=(basis.length == 4)
    )
    state_norm = float(np.vdot(state, state).real)
    result["residuals"].update(
        {
            "state_norm": abs(state_norm - 1.0),
            "total_content": float(basis.maximum_content_mismatch),
            "sharp_sector_QS_minus_QC": float(basis.maximum_charge_mismatch),
        }
    )
    return result


def run_resolution(length: int, steps: int) -> dict[str, Any]:
    target = load_historical_target()
    parent = target.Parent(length)
    basis = JointBasis(length)
    basis.validate_target_basis(parent)
    state = parent.initial_state()
    events: list[dict[str, Any]] = []
    for event in range(length):
        before = evaluate_state(state, basis)
        admitted = parent.apply_admission(state, event)
        after_admission = evaluate_state(admitted, basis)
        state, _ = parent.transport(admitted, steps)
        after_transport = evaluate_state(state, basis)
        events.append(
            {
                "event": event + 1,
                "zero_based_event": event,
                "before_admission": before,
                "after_admission": after_admission,
                "after_transport": after_transport,
            }
        )
    return {
        "L": length,
        "steps": steps,
        "events": events,
        "terminal": events[-1]["after_transport"],
    }


def terminal_disagreement(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    disagreement = 0.0
    for key in ("w", "w_sham", "D"):
        disagreement = max(
            disagreement,
            abs(float(left["registered"][key]) - float(right["registered"][key])),
        )
    for q in left["q_contributions"]:
        if q not in right["q_contributions"]:
            raise WitnessFailure(f"missing q contribution {q}")
        for key in ("p_q", "D_q"):
            disagreement = max(
                disagreement,
                abs(
                    float(left["q_contributions"][q][key])
                    - float(right["q_contributions"][q][key])
                ),
            )
    return finite(disagreement, "coarse/fine disagreement")


def all_evaluations(run: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    answer: list[Mapping[str, Any]] = []
    for event in run["events"]:
        answer.extend(
            (event["before_admission"], event["after_admission"], event["after_transport"])
        )
    return answer


def maximum_residual(runs: Sequence[Mapping[str, Any]], keys: Sequence[str]) -> float:
    maximum = 0.0
    for run in runs:
        for evaluation in all_evaluations(run):
            residuals = evaluation["residuals"]
            for key in keys:
                if key in residuals:
                    maximum = max(maximum, abs(finite(residuals[key], f"residual {key}")))
    return maximum


def adjudicate_target_size(coarse: Mapping[str, Any], fine: Mapping[str, Any]) -> dict[str, Any]:
    if int(coarse["L"]) != int(fine["L"]):
        raise WitnessFailure("coarse/fine L mismatch")
    length = int(fine["L"])
    coarse_fine = terminal_disagreement(coarse["terminal"], fine["terminal"])
    row_column = max(
        finite(
            coarse["terminal"]["residuals"]["row_column_d_inputs"],
            "coarse terminal row/column registered disagreement",
        ),
        finite(
            fine["terminal"]["residuals"]["row_column_d_inputs"],
            "fine terminal row/column registered disagreement",
        ),
    )
    diagnostic_row_column = maximum_residual(
        (coarse, fine), ("row_column_accumulator",)
    )
    target_d = max(coarse_fine, row_column)
    norm_content = maximum_residual((coarse, fine), ("state_norm", "total_content"))
    probability_marginal = maximum_residual(
        (coarse, fine), ("probability_normalization", "marginal_reconstruction")
    )
    charge = maximum_residual((coarse, fine), ("sharp_sector_QS_minus_QC",))
    shuffle = maximum_residual(
        (coarse, fine), ("shuffle_expectation", "l4_permutation_shuffle")
    )
    sham = maximum_residual((coarse, fine), ("sham_self_covariance",))
    l4_exhaustive = maximum_residual(
        (coarse, fine), ("l4_exhaustive_streamed", "l4_permutation_shuffle")
    ) if length == 4 else 0.0
    r_l = max(norm_content, probability_marginal, charge)
    tau_target = max(1.0e-9, 50.0 * target_d, 100.0 * r_l)
    conditions = {
        "target_coarse_fine": coarse_fine <= COARSE_FINE_TOLERANCE,
        "row_column_accumulators": row_column <= COARSE_FINE_TOLERANCE,
        "norm_and_total_content": norm_content <= NORM_TOLERANCE,
        "probability_and_marginals": probability_marginal <= MARGINAL_TOLERANCE,
        "sharp_sector_QS_minus_QC": charge <= CHARGE_TOLERANCE,
        "shuffle_control": shuffle <= SHUFFLE_TOLERANCE,
        "sham_control": sham <= SHAM_TOLERANCE,
        "l4_exhaustive": length != 4 or l4_exhaustive <= L4_EXHAUSTIVE_TOLERANCE,
    }
    passed = all(conditions.values())
    return {
        "L": length,
        "passed": passed,
        "conditions": conditions,
        "target_coarse_fine_disagreement": coarse_fine,
        "row_column_disagreement": row_column,
        "maximum_diagnostic_row_column_disagreement": diagnostic_row_column,
        "target_d_component": target_d,
        "r_L": r_l,
        "tau_L_target_component": tau_target,
        "maximum_norm_total_content_residual": norm_content,
        "maximum_probability_marginal_residual": probability_marginal,
        "maximum_charge_residual": charge,
        "maximum_shuffle_residual": shuffle,
        "maximum_sham_residual": sham,
        "maximum_l4_exhaustive_residual": l4_exhaustive,
        "coarse": coarse,
        "fine": fine,
    }


def classify_target(rows: Sequence[Mapping[str, Any]]) -> tuple[str, bool]:
    lengths = [int(row["L"]) for row in rows]
    if tuple(lengths) != MANDATORY_LENGTHS:
        return "TARGET_OWNER_ONCE_JOINT_WITNESS_INVALID_MANDATORY_SIZE_SET", False
    if not all(bool(row["passed"]) for row in rows):
        return "TARGET_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED", False
    return (
        "TARGET_OWNER_ONCE_JOINT_WITNESS_NUMERICALLY_RESOLVED__AWAITING_INDEPENDENT",
        True,
    )


def build_target_result() -> dict[str, Any]:
    protocol = authenticate_protocol()
    dependencies = {
        "protocol": protocol,
        "historical_target": {
            "path": str(HISTORICAL_TARGET.relative_to(ROOT)),
            "sha256": sha256_file(HISTORICAL_TARGET),
        },
        "target_source": {
            "path": str(Path(__file__).relative_to(ROOT)),
            "sha256": sha256_file(Path(__file__)),
        },
    }
    rows: list[dict[str, Any]] = []
    failure: dict[str, str] | None = None
    try:
        for length in MANDATORY_LENGTHS:
            coarse = run_resolution(length, COARSE_STEPS)
            fine = run_resolution(length, FINE_STEPS)
            rows.append(adjudicate_target_size(coarse, fine))
    except WitnessFailure as error:
        classification = "TARGET_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_UNRESOLVED"
        passed = False
        failure = {"type": type(error).__name__, "message": str(error)}
    else:
        classification, passed = classify_target(rows)
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "classification": classification,
        "passed": passed,
        "final_physical_disposition_authorized": False,
        "requires_frozen_independent_implementation_and_result": True,
        "parameters": {
            "mandatory_lengths": list(MANDATORY_LENGTHS),
            "coarse_steps": COARSE_STEPS,
            "fine_steps": FINE_STEPS,
            "taylor_order": TAYLOR_ORDER,
            "phi": PHI,
            "dwell": DWELL,
            "tolerances": {
                "coarse_fine": COARSE_FINE_TOLERANCE,
                "norm": NORM_TOLERANCE,
                "marginal": MARGINAL_TOLERANCE,
                "charge": CHARGE_TOLERANCE,
                "shuffle": SHUFFLE_TOLERANCE,
                "sham": SHAM_TOLERANCE,
                "l4_exhaustive": L4_EXHAUSTIVE_TOLERANCE,
            },
        },
        "dependencies": dependencies,
        "rows": rows,
        "claim_boundary": {
            "target_only": "finite target numerical readiness for independent comparison",
            "not_decided": [
                "the frozen T_4:8 statistic",
                "a resolved or falsified physical witness",
                "held-out L10 or L12",
                "future lineage back-reaction",
                "entanglement",
                "thermodynamic or continuum behavior",
                "gravity",
            ],
        },
    }
    if failure is not None:
        result["failure"] = failure
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--authorize-frozen-seed",
        action="store_true",
        help="required guard; do not use until the independent source is frozen",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if not args.authorize_frozen_seed:
        parser.error(
            "mandatory seed execution is locked until the hostile source is frozen; "
            "then pass --authorize-frozen-seed"
        )
    result = build_target_result()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(result["classification"])


if __name__ == "__main__":
    main()
