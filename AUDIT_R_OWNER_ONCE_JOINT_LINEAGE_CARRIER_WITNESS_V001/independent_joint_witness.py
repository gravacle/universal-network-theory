#!/usr/bin/env python3
"""Independent hostile reconstruction for the owner-once joint witness.

This source is frozen before any L4/L6/L8 witness output is generated or any
target implementation/result is inspected.  It deliberately uses a reversed
fixed-weight basis, connector-first reversed edge order, block amplitudes, and
separate row/column probability accumulators.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTOCOL = (
    ROOT
    / "DEVELOPMENT_R_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001"
    / "PROTOCOL.md"
)
EXPECTED_PROTOCOL_SHA256 = (
    "70984a927c30585704622dfd03ee91bf516cd9a5d14474a228d231144e5e513e"
)

MANDATORY_LENGTHS = (4, 6, 8)
PHI = math.pi / 4.0
DWELL = math.pi / 2.0
TAYLOR_ORDER = 12
COARSE_SUBSTEPS = 64
FINE_SUBSTEPS = 128
TARGET_INDEPENDENT_TOLERANCE = 1.0e-8
NORM_CONTENT_TOLERANCE = 1.0e-10
MARGINAL_TOLERANCE = 1.0e-10
SHUFFLE_TOLERANCE = 1.0e-12
SHAM_TOLERANCE = 1.0e-12
L4_EXHAUSTIVE_TOLERANCE = 1.0e-12
AUTHORIZATION = "AUTHORIZE_L4_L6_L8_JOINT_WITNESS"
DEFAULT_OUTPUT = HERE / "HOSTILE_RESULT.json"

HISTORICAL_DEPENDENCIES = {
    "frozen_witness_protocol": PROTOCOL,
    "historical_accumulation_protocol": ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "PROTOCOL.md",
    "historical_prefix_protocol": ROOT
    / "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001"
    / "PROTOCOL.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def descending_fixed_weight_words(width: int, weight: int) -> tuple[int, ...]:
    """Independent descending integer ordering of fixed-weight bit words."""

    return tuple(
        word
        for word in range((1 << width) - 1, -1, -1)
        if bin(word).count("1") == weight
    )


def bit_table(words: Sequence[int], width: int) -> np.ndarray:
    table = np.empty((len(words), width), dtype=np.float64)
    for row, word in enumerate(words):
        for bit in range(width):
            table[row, bit] = float((word >> bit) & 1)
    return table


def hostile_prism_edges(length: int) -> tuple[tuple[int, int, str], ...]:
    """Reconstruct the prism with an order unlike the historical target."""

    answer: list[tuple[int, int, str]] = []
    for site in range(length - 1, -1, -1):
        answer.append((site, length + ((site + 1) % length), "connector"))
    for rail in (1, 0):
        offset = rail * length
        for site in range(length - 1, -1, -1):
            answer.append(
                (offset + site, offset + ((site + 1) % length), f"rail_{rail}")
            )
    return tuple(answer)


@dataclass(frozen=True)
class Sector:
    lineage_words: tuple[int, ...]
    lineage_lookup: dict[int, int]
    carrier_words: tuple[int, ...]
    carrier_lookup: dict[int, int]
    edge_pairs: tuple[tuple[np.ndarray, np.ndarray], ...]
    lineage_bits: np.ndarray
    active_carrier_bits: np.ndarray


@dataclass(frozen=True)
class Parent:
    length: int
    sites: int
    edges: tuple[tuple[int, int, str], ...]
    sectors: tuple[Sector, ...]


def build_parent(length: int) -> Parent:
    sites = 2 * length
    edges = hostile_prism_edges(length)
    sectors: list[Sector] = []
    for q in range(length + 1):
        lineage_words = descending_fixed_weight_words(length, q)
        carrier_words = descending_fixed_weight_words(sites, q)
        lineage_lookup = {word: index for index, word in enumerate(lineage_words)}
        carrier_lookup = {word: index for index, word in enumerate(carrier_words)}
        edge_pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for left_site, right_site, _ in edges:
            sources = [
                word
                for word in carrier_words
                if ((word >> left_site) & 1) and not ((word >> right_site) & 1)
            ]
            left = np.array([carrier_lookup[word] for word in sources], dtype=np.int32)
            right = np.array(
                [
                    carrier_lookup[word ^ (1 << left_site) ^ (1 << right_site)]
                    for word in sources
                ],
                dtype=np.int32,
            )
            edge_pairs.append((left, right))
        sectors.append(
            Sector(
                lineage_words=lineage_words,
                lineage_lookup=lineage_lookup,
                carrier_words=carrier_words,
                carrier_lookup=carrier_lookup,
                edge_pairs=tuple(edge_pairs),
                lineage_bits=bit_table(lineage_words, length),
                active_carrier_bits=bit_table(carrier_words, length),
            )
        )
    return Parent(length=length, sites=sites, edges=edges, sectors=tuple(sectors))


def blank_state(parent: Parent) -> list[np.ndarray]:
    blocks = [
        np.zeros(
            (len(sector.lineage_words), len(sector.carrier_words)),
            dtype=np.complex128,
        )
        for sector in parent.sectors
    ]
    blocks[0][0, 0] = 1.0
    return blocks


def copy_blocks(blocks: Iterable[np.ndarray]) -> list[np.ndarray]:
    return [block.copy() for block in blocks]


def state_norm(blocks: Sequence[np.ndarray]) -> float:
    return float(sum(np.vdot(block, block).real for block in blocks))


def admit(parent: Parent, blocks: Sequence[np.ndarray], event: int) -> list[np.ndarray]:
    """Apply the owner-once admission rotation in independent block order."""

    out = copy_blocks(blocks)
    cosine = math.cos(PHI)
    sine = math.sin(PHI)
    for q in range(parent.length):
        source_sector = parent.sectors[q]
        target_sector = parent.sectors[q + 1]
        rows = np.array(
            [
                row
                for row, word in enumerate(source_sector.lineage_words)
                if not ((word >> event) & 1)
            ],
            dtype=np.int32,
        )
        columns = np.array(
            [
                column
                for column, word in enumerate(source_sector.carrier_words)
                if not ((word >> event) & 1)
            ],
            dtype=np.int32,
        )
        if len(rows) == 0 or len(columns) == 0:
            continue
        target_rows = np.array(
            [
                target_sector.lineage_lookup[
                    source_sector.lineage_words[row] | (1 << event)
                ]
                for row in rows
            ],
            dtype=np.int32,
        )
        target_columns = np.array(
            [
                target_sector.carrier_lookup[
                    source_sector.carrier_words[column] | (1 << event)
                ]
                for column in columns
            ],
            dtype=np.int32,
        )
        left_index = np.ix_(rows, columns)
        right_index = np.ix_(target_rows, target_columns)
        left = blocks[q][left_index].copy()
        right = blocks[q + 1][right_index].copy()
        out[q][left_index] = cosine * left - 1j * sine * right
        out[q + 1][right_index] = cosine * right - 1j * sine * left
    return out


def hopping_action(parent: Parent, blocks: Sequence[np.ndarray]) -> list[np.ndarray]:
    out = [np.zeros_like(block) for block in blocks]
    for q, block in enumerate(blocks):
        for left, right in parent.sectors[q].edge_pairs:
            out[q][:, left] -= block[:, right]
            out[q][:, right] -= block[:, left]
    return out


def taylor_substep(
    parent: Parent, blocks: Sequence[np.ndarray], elapsed: float
) -> list[np.ndarray]:
    out = copy_blocks(blocks)
    term = copy_blocks(blocks)
    for order in range(1, TAYLOR_ORDER + 1):
        acted = hopping_action(parent, term)
        factor = -1j * elapsed / float(order)
        term = [factor * block for block in acted]
        for q in range(parent.length + 1):
            out[q] += term[q]
    return out


def transport(
    parent: Parent, blocks: Sequence[np.ndarray], substeps: int
) -> tuple[list[np.ndarray], float, float]:
    elapsed = DWELL / float(substeps)
    out = copy_blocks(blocks)
    initial_norm = state_norm(blocks)
    maximum_drift = 0.0
    for _ in range(substeps):
        out = taylor_substep(parent, out, elapsed)
        maximum_drift = max(maximum_drift, abs(state_norm(out) - initial_norm))
    return out, maximum_drift, abs(state_norm(out) - 1.0)


def _sector_row_accumulator(
    sector: Sector, probability: np.ndarray, length: int, q: int
) -> dict[str, object]:
    p_s = np.sum(probability, axis=1)
    p_c = np.zeros(probability.shape[1], dtype=np.float64)
    observed = 0.0
    centered = sector.lineage_bits - float(q) / float(length)
    for row in range(probability.shape[0]):
        row_probability = probability[row, :]
        p_c += row_probability
        scores = np.sum(
            sector.active_carrier_bits * centered[row, :], axis=1
        )
        observed += float(np.sum(row_probability * scores)) / float(length)
    sector_weight = float(np.sum(p_s))
    lineage_vector = np.sum(p_s[:, None] * centered, axis=0)
    carrier_vector = np.sum(p_c[:, None] * sector.active_carrier_bits, axis=0)
    sham = 0.0
    if sector_weight > 0.0:
        sham = float(np.sum(lineage_vector * carrier_vector)) / (
            float(length) * sector_weight
        )
    return {
        "carrier_marginal": p_c,
        "lineage_marginal": p_s,
        "observed": observed,
        "sector_weight": sector_weight,
        "sham": sham,
        "witness": observed - sham,
    }


def _sector_column_accumulator(
    sector: Sector, probability: np.ndarray, length: int, q: int
) -> dict[str, object]:
    p_c = np.sum(probability, axis=0)
    p_s = np.zeros(probability.shape[0], dtype=np.float64)
    observed = 0.0
    centered = sector.lineage_bits - float(q) / float(length)
    for column in range(probability.shape[1]):
        column_probability = probability[:, column]
        p_s += column_probability
        scores = np.sum(
            centered * sector.active_carrier_bits[column, :], axis=1
        )
        observed += float(np.sum(column_probability * scores)) / float(length)
    sector_weight = float(np.sum(p_c))
    lineage_vector = np.sum(p_s[:, None] * centered, axis=0)
    carrier_vector = np.sum(p_c[:, None] * sector.active_carrier_bits, axis=0)
    sham = 0.0
    if sector_weight > 0.0:
        sham = float(np.sum(lineage_vector * carrier_vector)) / (
            float(length) * sector_weight
        )
    return {
        "carrier_marginal": p_c,
        "lineage_marginal": p_s,
        "observed": observed,
        "sector_weight": sector_weight,
        "sham": sham,
        "witness": observed - sham,
    }


def _sham_self_residual(
    sector: Sector, row_record: dict[str, object], length: int, q: int
) -> float:
    sector_weight = float(row_record["sector_weight"])
    if sector_weight == 0.0:
        return 0.0
    p_s = np.asarray(row_record["lineage_marginal"], dtype=np.float64)
    p_c = np.asarray(row_record["carrier_marginal"], dtype=np.float64)
    centered = sector.lineage_bits - float(q) / float(length)
    direct = 0.0
    for row in range(len(p_s)):
        score = np.sum(
            sector.active_carrier_bits * centered[row, :], axis=1
        )
        direct += (
            float(p_s[row])
            * float(np.sum(p_c * score))
            / (float(length) * sector_weight)
        )
    return abs(direct - float(row_record["sham"]))


def evaluate_witness(
    parent: Parent,
    blocks: Sequence[np.ndarray],
    include_negative_controls: bool = False,
    exhaustive_l4_shuffle: bool = False,
) -> dict[str, object]:
    row_observed: list[float] = []
    row_sham: list[float] = []
    row_witness: list[float] = []
    column_observed: list[float] = []
    column_sham: list[float] = []
    column_witness: list[float] = []
    sector_weights: list[float] = []
    marginal_residual = 0.0
    q_identity_residual = 0.0
    sham_self_residual = 0.0
    total_carrier_content = 0.0
    total_lineage_content = 0.0

    for q, (sector, block) in enumerate(zip(parent.sectors, blocks)):
        probability = np.abs(block) ** 2
        direct_sector_weight = float(np.sum(probability))
        row = _sector_row_accumulator(sector, probability, parent.length, q)
        column = _sector_column_accumulator(sector, probability, parent.length, q)
        row_observed.append(float(row["observed"]))
        row_sham.append(float(row["sham"]))
        row_witness.append(float(row["witness"]))
        column_observed.append(float(column["observed"]))
        column_sham.append(float(column["sham"]))
        column_witness.append(float(column["witness"]))
        sector_weights.append(float(row["sector_weight"]))
        lineage_marginal = np.asarray(row["lineage_marginal"], dtype=np.float64)
        carrier_marginal = np.asarray(row["carrier_marginal"], dtype=np.float64)
        lineage_counts = np.sum(sector.lineage_bits, axis=1)
        carrier_counts = np.array(
            [bin(word).count("1") for word in sector.carrier_words],
            dtype=np.float64,
        )
        lineage_q = float(np.sum(lineage_marginal * lineage_counts))
        carrier_q = float(np.sum(carrier_marginal * carrier_counts))
        sector_weight = float(row["sector_weight"])
        expected_q = float(q) * sector_weight
        q_identity_residual = max(
            q_identity_residual,
            abs(lineage_q - expected_q),
            abs(carrier_q - expected_q),
            abs(lineage_q - carrier_q),
        )
        total_lineage_content += lineage_q + float(parent.length - q) * sector_weight
        total_carrier_content += carrier_q + float(parent.length - q) * sector_weight
        marginal_residual = max(
            marginal_residual,
            abs(float(row["sector_weight"]) - direct_sector_weight),
            abs(float(column["sector_weight"]) - direct_sector_weight),
            abs(
                float(np.sum(np.asarray(row["lineage_marginal"])))
                - direct_sector_weight
            ),
            abs(
                float(np.sum(np.asarray(row["carrier_marginal"])))
                - direct_sector_weight
            ),
            abs(float(row["sector_weight"]) - float(column["sector_weight"])),
            float(
                np.max(
                    np.abs(
                        np.asarray(row["lineage_marginal"])
                        - np.asarray(column["lineage_marginal"])
                    )
                )
            ),
            float(
                np.max(
                    np.abs(
                        np.asarray(row["carrier_marginal"])
                        - np.asarray(column["carrier_marginal"])
                    )
                )
            ),
        )
        if include_negative_controls:
            sham_self_residual = max(
                sham_self_residual,
                _sham_self_residual(sector, row, parent.length, q),
            )

    row_column_disagreement = max(
        max(abs(a - b) for a, b in zip(row_observed, column_observed)),
        max(abs(a - b) for a, b in zip(row_sham, column_sham)),
        max(abs(a - b) for a, b in zip(row_witness, column_witness)),
        marginal_residual,
    )
    total_probability = float(sum(sector_weights))
    total_content_residual = max(
        abs(total_lineage_content - float(parent.length)),
        abs(total_carrier_content - float(parent.length)),
    )
    exhaustive_shuffle_value: Optional[float] = None
    exhaustive_direct: Optional[dict[str, float]] = None
    exhaustive_direct_residual: Optional[float] = None
    if exhaustive_l4_shuffle:
        if parent.length != 4:
            raise ValueError("exhaustive protocol shuffle is frozen only at L4")
        exhaustive_shuffle_value = exhaustive_shuffle_expectation(parent, blocks)
        exhaustive_direct = exhaustive_direct_controls(parent, blocks)

    row_total_observed = float(sum(row_observed))
    row_total_sham = float(sum(row_sham))
    row_total_witness = float(sum(row_witness))
    if exhaustive_direct is not None:
        exhaustive_direct_residual = max(
            abs(exhaustive_direct["observed"] - row_total_observed),
            abs(exhaustive_direct["sham"] - row_total_sham),
            abs(exhaustive_direct["witness"] - row_total_witness),
        )
    return {
        "D_L": row_total_witness,
        "column_accumulator": {
            "observed": float(sum(column_observed)),
            "q_observed": column_observed,
            "q_sham": column_sham,
            "q_witness": column_witness,
            "sham": float(sum(column_sham)),
            "witness": float(sum(column_witness)),
        },
        "controls": {
            "analytic_shuffle_expectation": 0.0,
            "exhaustive_direct": exhaustive_direct,
            "exhaustive_direct_residual": exhaustive_direct_residual,
            "exhaustive_shuffle_expectation": exhaustive_shuffle_value,
            "sham_self_covariance_residual": sham_self_residual,
        },
        "marginal_reconstruction_residual": marginal_residual,
        "normalization_residual": abs(total_probability - 1.0),
        "q_identity_residual": q_identity_residual,
        "total_content_residual": total_content_residual,
        "row_accumulator": {
            "observed": row_total_observed,
            "q_observed": row_observed,
            "q_sham": row_sham,
            "q_witness": row_witness,
            "sham": row_total_sham,
            "witness": row_total_witness,
        },
        "row_column_disagreement": row_column_disagreement,
        "sector_weights": sector_weights,
        "w_L": row_total_observed,
        "w_L_sham": row_total_sham,
        "w_L_shuffle": 0.0,
    }


def permute_word(word: int, permutation: Sequence[int]) -> int:
    out = 0
    for source, destination in enumerate(permutation):
        if (word >> source) & 1:
            out |= 1 << destination
    return out


def exhaustive_direct_controls(
    parent: Parent, blocks: Sequence[np.ndarray]
) -> dict[str, float]:
    """Dense direct sums independent of row/column streaming accumulators."""

    observed = 0.0
    sham = 0.0
    for q, (sector, block) in enumerate(zip(parent.sectors, blocks)):
        probability = np.abs(block) ** 2
        centered = sector.lineage_bits - float(q) / float(parent.length)
        scores = np.sum(
            centered[:, None, :] * sector.active_carrier_bits[None, :, :],
            axis=2,
        ) / float(parent.length)
        observed += float(np.sum(probability * scores))
        sector_weight = float(np.sum(probability))
        if sector_weight > 0.0:
            p_s = np.sum(probability, axis=1)
            p_c = np.sum(probability, axis=0)
            sham_probability = np.outer(p_s, p_c) / sector_weight
            sham += float(np.sum(sham_probability * scores))
    return {
        "observed": observed,
        "sham": sham,
        "witness": observed - sham,
    }


def exhaustive_shuffle_expectation(
    parent: Parent, blocks: Sequence[np.ndarray]
) -> float:
    """Enumerate the full lineage-label twirl (mandatory on physical L4)."""

    permutations = tuple(itertools.permutations(range(parent.length)))
    total = 0.0
    for q, (sector, block) in enumerate(zip(parent.sectors, blocks)):
        probability = np.abs(block) ** 2
        for row, word in enumerate(sector.lineage_words):
            if not np.any(probability[row, :]):
                continue
            for permutation in permutations:
                moved = permute_word(word, permutation)
                centered = np.array(
                    [
                        float((moved >> event) & 1)
                        - float(q) / float(parent.length)
                        for event in range(parent.length)
                    ],
                    dtype=np.float64,
                )
                scores = np.sum(
                    sector.active_carrier_bits * centered, axis=1
                )
                total += float(np.sum(probability[row, :] * scores)) / (
                    float(parent.length) * float(len(permutations))
                )
    return total


def _checkpoint(
    parent: Parent,
    blocks: Sequence[np.ndarray],
    event: int,
    stage: str,
    terminal_controls: bool = False,
) -> dict[str, object]:
    return {
        "event": event,
        "stage": stage,
        "witness": evaluate_witness(
            parent,
            blocks,
            include_negative_controls=terminal_controls,
            exhaustive_l4_shuffle=terminal_controls and parent.length == 4,
        ),
    }


def run_resolution(length: int, substeps: int) -> dict[str, object]:
    """Generate one prospective physical history; never called by source tests."""

    parent = build_parent(length)
    blocks = blank_state(parent)
    checkpoints: list[dict[str, object]] = []
    maximum_transport_drift = 0.0
    maximum_absolute_norm_error = abs(state_norm(blocks) - 1.0)
    for event in range(length):
        checkpoints.append(_checkpoint(parent, blocks, event, "before_admission"))
        blocks = admit(parent, blocks, event)
        checkpoints.append(_checkpoint(parent, blocks, event, "after_admission"))
        blocks, drift, norm_error = transport(parent, blocks, substeps)
        maximum_transport_drift = max(maximum_transport_drift, drift)
        maximum_absolute_norm_error = max(maximum_absolute_norm_error, norm_error)
        checkpoints.append(
            _checkpoint(
                parent,
                blocks,
                event,
                "after_transport",
                terminal_controls=event == length - 1,
            )
        )
    return {
        "checkpoints": checkpoints,
        "length": length,
        "maximum_absolute_norm_error": maximum_absolute_norm_error,
        "maximum_transport_norm_drift": maximum_transport_drift,
        "substeps": substeps,
    }


def _flatten_numeric(record: object, prefix: str = "") -> dict[str, float]:
    flat: dict[str, float] = {}
    if isinstance(record, dict):
        for key in sorted(record):
            child = f"{prefix}.{key}" if prefix else str(key)
            flat.update(_flatten_numeric(record[key], child))
    elif isinstance(record, list):
        for index, value in enumerate(record):
            flat.update(_flatten_numeric(value, f"{prefix}[{index}]"))
    elif isinstance(record, (float, int)) and not isinstance(record, bool):
        flat[prefix] = float(record)
    return flat


def compare_resolutions(coarse: dict[str, object], fine: dict[str, object]) -> float:
    left = _flatten_numeric(coarse["checkpoints"])
    right = _flatten_numeric(fine["checkpoints"])
    if set(left) != set(right):
        raise AssertionError("coarse/fine checkpoint schema mismatch")
    return max(abs(left[key] - right[key]) for key in left)


def _maximum_internal_residual(record: dict[str, object]) -> float:
    values: list[float] = [
        float(record["maximum_absolute_norm_error"]),
        float(record["maximum_transport_norm_drift"]),
    ]
    for checkpoint in record["checkpoints"]:
        witness = checkpoint["witness"]
        values.extend(
            [
                float(witness["marginal_reconstruction_residual"]),
                float(witness["normalization_residual"]),
                float(witness["q_identity_residual"]),
                float(witness["total_content_residual"]),
                float(witness["row_column_disagreement"]),
            ]
        )
        controls = witness["controls"]
        values.extend(
            [
                abs(float(controls["analytic_shuffle_expectation"])),
                abs(float(controls["sham_self_covariance_residual"])),
            ]
        )
        for key in ("exhaustive_direct_residual", "exhaustive_shuffle_expectation"):
            if controls[key] is not None:
                values.append(abs(float(controls[key])))
    return max(values, default=0.0)


def _maximum_checkpoint_value(record: dict[str, object], key: str) -> float:
    return max(
        abs(float(checkpoint["witness"][key]))
        for checkpoint in record["checkpoints"]
    )


def _maximum_terminal_control(record: dict[str, object], key: str) -> float:
    value = record["checkpoints"][-1]["witness"]["controls"][key]
    return 0.0 if value is None else abs(float(value))


def run_size(length: int) -> dict[str, object]:
    coarse = run_resolution(length, COARSE_SUBSTEPS)
    fine = run_resolution(length, FINE_SUBSTEPS)
    coarse_fine = compare_resolutions(coarse, fine)
    internal_residual = max(
        _maximum_internal_residual(coarse), _maximum_internal_residual(fine)
    )
    internal_tau_lower_bound = max(
        1.0e-9, 50.0 * coarse_fine, 100.0 * internal_residual
    )
    final_witness = fine["checkpoints"][-1]["witness"]
    internal_conditions = {
        "coarse_fine_within_1e_8": coarse_fine <= TARGET_INDEPENDENT_TOLERANCE,
        "l4_exhaustive_direct_within_1e_12": (
            True
            if length != 4
            else max(
                _maximum_terminal_control(coarse, "exhaustive_direct_residual"),
                _maximum_terminal_control(fine, "exhaustive_direct_residual"),
            )
            <= L4_EXHAUSTIVE_TOLERANCE
        ),
        "l4_exhaustive_shuffle_within_1e_12": (
            True
            if length != 4
            else max(
                _maximum_terminal_control(coarse, "exhaustive_shuffle_expectation"),
                _maximum_terminal_control(fine, "exhaustive_shuffle_expectation"),
            )
            <= SHUFFLE_TOLERANCE
        ),
        "marginals_within_1e_10": max(
            _maximum_checkpoint_value(coarse, "marginal_reconstruction_residual"),
            _maximum_checkpoint_value(fine, "marginal_reconstruction_residual"),
        )
        <= MARGINAL_TOLERANCE,
        "norm_within_1e_10": max(
            float(coarse["maximum_absolute_norm_error"]),
            float(fine["maximum_absolute_norm_error"]),
        )
        <= NORM_CONTENT_TOLERANCE,
        "normalization_within_1e_10": max(
            _maximum_checkpoint_value(coarse, "normalization_residual"),
            _maximum_checkpoint_value(fine, "normalization_residual"),
        )
        <= MARGINAL_TOLERANCE,
        "q_identity_within_1e_10": max(
            _maximum_checkpoint_value(coarse, "q_identity_residual"),
            _maximum_checkpoint_value(fine, "q_identity_residual"),
            _maximum_checkpoint_value(coarse, "total_content_residual"),
            _maximum_checkpoint_value(fine, "total_content_residual"),
        )
        <= NORM_CONTENT_TOLERANCE,
        "sham_negative_control_within_1e_12": max(
            _maximum_terminal_control(coarse, "sham_self_covariance_residual"),
            _maximum_terminal_control(fine, "sham_self_covariance_residual"),
        )
        <= SHAM_TOLERANCE,
    }
    return {
        "coarse": coarse,
        "fine": fine,
        "internal_coarse_fine_disagreement": coarse_fine,
        "internal_residual": internal_residual,
        "internal_tau_lower_bound": internal_tau_lower_bound,
        "internal_conditions": internal_conditions,
        "internal_conditions_pass": all(internal_conditions.values()),
        "length": length,
        "primary_fine_terminal": final_witness,
        "target_comparison": "PENDING_SEPARATE_ADJUDICATION",
    }


def finite_values(record: object) -> bool:
    if isinstance(record, dict):
        return all(finite_values(value) for value in record.values())
    if isinstance(record, list):
        return all(finite_values(value) for value in record)
    if isinstance(record, float):
        return math.isfinite(record)
    return True


def deterministic_dependencies() -> dict[str, dict[str, str]]:
    dependencies = {
        name: {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path),
        }
        for name, path in HISTORICAL_DEPENDENCIES.items()
    }
    dependencies["hostile_source"] = {
        "path": str(Path(__file__).resolve().relative_to(ROOT)),
        "sha256": sha256_file(Path(__file__).resolve()),
    }
    return dependencies


def build_result() -> dict[str, object]:
    if sha256_file(PROTOCOL) != EXPECTED_PROTOCOL_SHA256:
        raise AssertionError("frozen witness protocol hash mismatch")
    results = [run_size(length) for length in MANDATORY_LENGTHS]
    payload: dict[str, object] = {
        "claim_boundary": (
            "FINITE_OWNER_ONCE_TERMINAL_JOINT_LINEAGE_CARRIER_WITNESS_ONLY__"
            "NO_GATE_RGRL_ALPHA_GL6T_THERMODYNAMIC_CONTINUUM_OR_GRAVITY"
        ),
        "dependencies": deterministic_dependencies(),
        "disposition": "HOSTILE_SEED_CALCULATION_COMPLETE__TARGET_ADJUDICATION_REQUIRED",
        "independence": {
            "target_arrays_read": False,
            "target_code_imported": False,
            "target_matrices_read": False,
            "target_result_values_read": False,
        },
        "parameters": {
            "coarse_substeps": COARSE_SUBSTEPS,
            "dwell": DWELL,
            "fine_substeps": FINE_SUBSTEPS,
            "l4_exhaustive_tolerance": L4_EXHAUSTIVE_TOLERANCE,
            "lengths": list(MANDATORY_LENGTHS),
            "marginal_tolerance": MARGINAL_TOLERANCE,
            "norm_content_tolerance": NORM_CONTENT_TOLERANCE,
            "phi": PHI,
            "sham_tolerance": SHAM_TOLERANCE,
            "shuffle_tolerance": SHUFFLE_TOLERANCE,
            "target_independent_tolerance": TARGET_INDEPENDENT_TOLERANCE,
            "taylor_order": TAYLOR_ORDER,
        },
        "results": results,
        "schema": "HOSTILE_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001",
    }
    if not finite_values(payload):
        raise AssertionError("nonfinite value in hostile result")
    return payload


def synthetic_schema_record() -> dict[str, object]:
    """Small deterministic non-physical record for source-freeze testing."""

    return {
        "authorization_required": AUTHORIZATION,
        "mandatory_lengths": list(MANDATORY_LENGTHS),
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256,
        "schema": "HOSTILE_OWNER_ONCE_JOINT_LINEAGE_CARRIER_WITNESS_V001",
        "source_sha256": sha256_file(Path(__file__).resolve()),
        "status": "HOSTILE_SOURCE_FROZEN_READY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--print-source-schema", action="store_true")
    parser.add_argument("--authorize-seed", default="")
    args = parser.parse_args()

    if args.print_source_schema:
        print(json.dumps(synthetic_schema_record(), indent=2, sort_keys=True))
        return 0
    if args.authorize_seed != AUTHORIZATION:
        parser.error(
            "physical L4/L6/L8 execution is locked; pass the exact frozen authorization"
        )
    result = build_result()
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )
    print(result["disposition"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
