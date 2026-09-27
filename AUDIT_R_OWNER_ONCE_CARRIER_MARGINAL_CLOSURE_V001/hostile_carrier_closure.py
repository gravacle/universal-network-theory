#!/usr/bin/env python3
"""Independent hostile reconstruction of owner-once carrier closure.

This module deliberately does not import the target verifier or any historical
matrix/basis implementation.  It uses descending integer-word bases, a
connector-first reversed edge traversal, direct joint-amplitude evolution, and
an independently constructed Kraus-trajectory carrier ensemble.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_OUTPUT = HERE / "HOSTILE_RESULT.json"

PHI = math.pi / 4.0
DWELL = math.pi / 2.0
TAYLOR_ORDER = 12
TRANSPORT_SUBSTEPS = 16
MANDATORY_LENGTHS = (4, 6)
EQUIVALENCE_TOLERANCE = 2.0e-10
CONTROL_TOLERANCE = 2.0e-10

DEPENDENCIES = {
    "candidate_protocol": ROOT
    / "DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001"
    / "PROTOCOL.md",
    "candidate_theorem": ROOT
    / "DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001"
    / "THEOREM.md",
    "historical_accumulation_protocol": ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "PROTOCOL.md",
    "historical_prefix_protocol": ROOT
    / "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001"
    / "PROTOCOL.md",
    "historical_prefix_theorem": ROOT
    / "DEVELOPMENT_R_L12_PREFIX_LINEAGE_BLOCK_REDUCTION_V001"
    / "THEOREM.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def descending_words(width: int, weight: int) -> tuple[int, ...]:
    """Enumerate fixed-weight words in descending numerical order."""

    # ``int.bit_count`` is unavailable in the repository's oldest supported
    # Python runtime, so keep this hostile executable compatible with that
    # environment as well as current Python versions.
    return tuple(
        word
        for word in range((1 << width) - 1, -1, -1)
        if bin(word).count("1") == weight
    )


def hostile_edges(length: int) -> tuple[tuple[int, int, str], ...]:
    """Same prism, deliberately different traversal from the historical code."""

    edges: list[tuple[int, int, str]] = []
    for site in range(length - 1, -1, -1):
        edges.append((site, length + ((site + 1) % length), f"connector_{site}"))
    for rail in (1, 0):
        offset = rail * length
        for site in range(length - 1, -1, -1):
            edges.append(
                (offset + site, offset + ((site + 1) % length), f"rail_{rail}_{site}")
            )
    return tuple(edges)


@dataclass(frozen=True)
class CarrierSector:
    words: tuple[int, ...]
    lookup: dict[int, int]
    edge_pairs: tuple[tuple[np.ndarray, np.ndarray], ...]


@dataclass(frozen=True)
class FiniteParent:
    length: int
    sites: int
    edges: tuple[tuple[int, int, str], ...]
    lineage_words: tuple[tuple[int, ...], ...]
    lineage_lookup: tuple[dict[int, int], ...]
    sectors: tuple[CarrierSector, ...]


def build_parent(length: int) -> FiniteParent:
    sites = 2 * length
    edges = hostile_edges(length)
    lineage_words = tuple(descending_words(length, q) for q in range(length + 1))
    lineage_lookup = tuple({word: i for i, word in enumerate(words)} for words in lineage_words)
    sectors: list[CarrierSector] = []
    for q in range(length + 1):
        words = descending_words(sites, q)
        lookup = {word: i for i, word in enumerate(words)}
        all_pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for u, v, _ in edges:
            left_words = [word for word in words if ((word >> u) & 1) and not ((word >> v) & 1)]
            left = np.array([lookup[word] for word in left_words], dtype=np.int32)
            right = np.array(
                [lookup[word ^ (1 << u) ^ (1 << v)] for word in left_words], dtype=np.int32
            )
            all_pairs.append((left, right))
        sectors.append(CarrierSector(words, lookup, tuple(all_pairs)))
    return FiniteParent(
        length,
        sites,
        edges,
        lineage_words,
        lineage_lookup,
        tuple(sectors),
    )


def initial_joint(parent: FiniteParent) -> list[np.ndarray]:
    blocks = [
        np.zeros((len(parent.lineage_words[q]), len(parent.sectors[q].words)), dtype=np.complex128)
        for q in range(parent.length + 1)
    ]
    blocks[0][0, 0] = 1.0
    return blocks


def initial_carrier(parent: FiniteParent) -> list[np.ndarray]:
    factors = [
        np.zeros((0, len(parent.sectors[q].words)), dtype=np.complex128)
        for q in range(parent.length + 1)
    ]
    factors[0] = np.ones((1, 1), dtype=np.complex128)
    return factors


def copy_blocks(blocks: Iterable[np.ndarray]) -> list[np.ndarray]:
    return [block.copy() for block in blocks]


def factor_norm(blocks: Iterable[np.ndarray]) -> float:
    return float(sum(np.vdot(block, block).real for block in blocks))


def joint_admission(parent: FiniteParent, blocks: list[np.ndarray], event: int) -> list[np.ndarray]:
    """Apply the full two-child rotation in a joint lineage/carrier basis."""

    result = copy_blocks(blocks)
    c = math.cos(PHI)
    s = math.sin(PHI)
    for q in range(parent.length):
        carrier_words = parent.sectors[q].words
        blank_columns = [i for i, word in enumerate(carrier_words) if not ((word >> event) & 1)]
        destination_columns = np.array(
            [parent.sectors[q + 1].lookup[carrier_words[i] | (1 << event)] for i in blank_columns],
            dtype=np.int32,
        )
        source_columns = np.array(blank_columns, dtype=np.int32)
        for source_row, lineage_word in enumerate(parent.lineage_words[q]):
            if (lineage_word >> event) & 1:
                continue
            destination_row = parent.lineage_lookup[q + 1][lineage_word | (1 << event)]
            left = blocks[q][source_row, source_columns].copy()
            right = blocks[q + 1][destination_row, destination_columns].copy()
            result[q][source_row, source_columns] = c * left - 1j * s * right
            result[q + 1][destination_row, destination_columns] = c * right - 1j * s * left
    return result


def carrier_channel(parent: FiniteParent, factors: list[np.ndarray], event: int) -> list[np.ndarray]:
    """Apply K0/K1 as an unread Kraus split, with no lineage representation."""

    c = math.cos(PHI)
    s = math.sin(PHI)
    parts: list[list[np.ndarray]] = [[] for _ in range(parent.length + 1)]

    # Append jump factors first and in descending q order.  This is intentionally
    # unlike the joint lineage-row ordering.
    for q in range(parent.length - 1, -1, -1):
        block = factors[q]
        if block.shape[0] == 0:
            continue
        destination = np.zeros(
            (block.shape[0], len(parent.sectors[q + 1].words)), dtype=np.complex128
        )
        for column, word in enumerate(parent.sectors[q].words):
            if not ((word >> event) & 1):
                target = parent.sectors[q + 1].lookup[word | (1 << event)]
                destination[:, target] = -1j * s * block[:, column]
        parts[q + 1].append(destination)

    for q in range(parent.length, -1, -1):
        block = factors[q]
        if block.shape[0] == 0:
            continue
        scale = np.array(
            [1.0 if ((word >> event) & 1) else c for word in parent.sectors[q].words],
            dtype=float,
        )
        parts[q].append(block * scale[np.newaxis, :])

    result: list[np.ndarray] = []
    for q, contributions in enumerate(parts):
        if contributions:
            result.append(np.vstack(contributions))
        else:
            result.append(np.zeros((0, len(parent.sectors[q].words)), dtype=np.complex128))
    return result


def h_action(parent: FiniteParent, blocks: list[np.ndarray]) -> list[np.ndarray]:
    result = [np.zeros_like(block) for block in blocks]
    for q, block in enumerate(blocks):
        if block.shape[0] == 0:
            continue
        for left, right in parent.sectors[q].edge_pairs:
            result[q][:, left] -= block[:, right]
            result[q][:, right] -= block[:, left]
    return result


def taylor_step(
    parent: FiniteParent, blocks: list[np.ndarray], elapsed: float
) -> list[np.ndarray]:
    updated = copy_blocks(blocks)
    term = copy_blocks(blocks)
    for order in range(1, TAYLOR_ORDER + 1):
        acted = h_action(parent, term)
        factor = -1j * elapsed / order
        term = [factor * block for block in acted]
        for q in range(parent.length + 1):
            updated[q] += term[q]
    return updated


def currents(parent: FiniteParent, blocks: list[np.ndarray]) -> np.ndarray:
    answer = np.zeros(len(parent.edges), dtype=float)
    for q, block in enumerate(blocks):
        if block.shape[0] == 0:
            continue
        for edge, (left, right) in enumerate(parent.sectors[q].edge_pairs):
            answer[edge] += 2.0 * float(np.imag(np.vdot(block[:, left], block[:, right])))
    return answer


def transport(
    parent: FiniteParent, blocks: list[np.ndarray]
) -> tuple[list[np.ndarray], np.ndarray, float]:
    dt = DWELL / TRANSPORT_SUBSTEPS
    evolved = copy_blocks(blocks)
    initial_norm = factor_norm(blocks)
    maximum_norm_drift = 0.0
    integrated = currents(parent, evolved)
    for step in range(1, TRANSPORT_SUBSTEPS + 1):
        evolved = taylor_step(parent, evolved, dt)
        maximum_norm_drift = max(maximum_norm_drift, abs(factor_norm(evolved) - initial_norm))
        weight = 1 if step == TRANSPORT_SUBSTEPS else (4 if step % 2 else 2)
        integrated += weight * currents(parent, evolved)
    integrated *= dt / 3.0
    return evolved, integrated, maximum_norm_drift


def sector_weights(blocks: list[np.ndarray]) -> np.ndarray:
    return np.array([float(np.vdot(block, block).real) for block in blocks], dtype=float)


def occupations(parent: FiniteParent, blocks: list[np.ndarray]) -> np.ndarray:
    answer = np.zeros(parent.sites, dtype=float)
    for q, block in enumerate(blocks):
        if block.shape[0] == 0:
            continue
        probabilities = np.sum(np.abs(block) ** 2, axis=0)
        for column, word in enumerate(parent.sectors[q].words):
            probability = float(probabilities[column])
            if probability == 0.0:
                continue
            for site in range(parent.sites):
                if (word >> site) & 1:
                    answer[site] += probability
    return answer


def reduced_blocks(blocks: list[np.ndarray]) -> list[np.ndarray]:
    # Rows contain ket coefficients; rho[c,d] = sum_s A[s,c] conj(A[s,d]).
    # Construct empty sectors explicitly and use an index contraction.  The
    # latter also avoids platform-BLAS floating-point-status noise from dense
    # products whose unused rows are exactly zero.
    return [
        np.einsum("sc,sd->cd", block, block.conj(), optimize=False)
        if block.shape[0]
        else np.zeros((block.shape[1], block.shape[1]), dtype=np.complex128)
        for block in blocks
    ]


def factor_singular_values(block: np.ndarray) -> np.ndarray:
    if block.shape[0] == 0:
        return np.zeros(0, dtype=float)
    return np.linalg.svd(block, compute_uv=False)


def padded_max_difference(left: np.ndarray, right: np.ndarray) -> float:
    size = max(len(left), len(right))
    if size == 0:
        return 0.0
    a = np.zeros(size, dtype=float)
    b = np.zeros(size, dtype=float)
    a[: len(left)] = left
    b[: len(right)] = right
    return float(np.max(np.abs(a - b)))


def compare_states(
    parent: FiniteParent,
    joint: list[np.ndarray],
    carrier: list[np.ndarray],
    include_trace_distance: bool,
) -> dict[str, float | None]:
    joint_rho = reduced_blocks(joint)
    carrier_rho = reduced_blocks(carrier)
    maximum_entry = 0.0
    hilbert_schmidt_squared = 0.0
    trace_distance = 0.0
    trace_bound = 0.0
    factor_residual = 0.0
    for q, (left, right) in enumerate(zip(joint_rho, carrier_rho)):
        delta = left - right
        maximum_entry = max(maximum_entry, float(np.max(np.abs(delta))) if delta.size else 0.0)
        frobenius = float(np.linalg.norm(delta))
        hilbert_schmidt_squared += frobenius * frobenius
        trace_bound += 0.5 * math.sqrt(delta.shape[0]) * frobenius
        if include_trace_distance and delta.size:
            hermitian_delta = 0.5 * (delta + delta.conj().T)
            trace_distance += 0.5 * float(np.sum(np.abs(np.linalg.eigvalsh(hermitian_delta))))
        factor_residual = max(
            factor_residual,
            padded_max_difference(
                factor_singular_values(joint[q]), factor_singular_values(carrier[q])
            ),
        )

    joint_q = sector_weights(joint)
    carrier_q = sector_weights(carrier)
    return {
        "factor_singular_value_residual": factor_residual,
        "instantaneous_current_max_abs": float(
            np.max(np.abs(currents(parent, joint) - currents(parent, carrier)))
        ),
        "occupation_max_abs": float(
            np.max(np.abs(occupations(parent, joint) - occupations(parent, carrier)))
        ),
        "reduced_carrier_entry_max_abs": maximum_entry,
        "reduced_carrier_hilbert_schmidt": math.sqrt(hilbert_schmidt_squared),
        "reduced_carrier_trace_distance": trace_distance if include_trace_distance else None,
        "reduced_carrier_trace_distance_upper_bound": trace_bound,
        "sector_weight_max_abs": float(np.max(np.abs(joint_q - carrier_q))),
        "trace_residual": abs(factor_norm(joint) - factor_norm(carrier)),
    }


def fresh_lineage_probability(
    parent: FiniteParent, joint: list[np.ndarray], event: int
) -> float:
    probability = 0.0
    for q, block in enumerate(joint):
        rows = [i for i, word in enumerate(parent.lineage_words[q]) if (word >> event) & 1]
        if rows:
            probability += float(np.vdot(block[rows, :], block[rows, :]).real)
    return probability


def blank_probability(parent: FiniteParent, blocks: list[np.ndarray], event: int) -> float:
    probability = 0.0
    for q, block in enumerate(blocks):
        if block.shape[0] == 0:
            continue
        columns = [i for i, word in enumerate(parent.sectors[q].words) if not ((word >> event) & 1)]
        if columns:
            probability += float(np.vdot(block[:, columns], block[:, columns]).real)
    return probability


def occupied_probability(parent: FiniteParent, blocks: list[np.ndarray], event: int) -> float:
    return factor_norm(blocks) - blank_probability(parent, blocks, event)


def numerical_tail_bound() -> float:
    # The prism hopping norm is bounded by its maximum degree, three.
    x = 3.0 * (DWELL / TRANSPORT_SUBSTEPS)
    one_step = math.exp(x) * (x ** (TAYLOR_ORDER + 1)) / math.factorial(TAYLOR_ORDER + 1)
    return TRANSPORT_SUBSTEPS * one_step


def finite_values(record: object) -> bool:
    if isinstance(record, dict):
        return all(finite_values(value) for value in record.values())
    if isinstance(record, list):
        return all(finite_values(value) for value in record)
    if isinstance(record, float):
        return math.isfinite(record)
    return True


def run_length(length: int) -> dict[str, object]:
    parent = build_parent(length)
    joint = initial_joint(parent)
    carrier = initial_carrier(parent)
    include_trace = length == 4

    checkpoints: list[dict[str, object]] = [
        {"stage": "initial", **compare_states(parent, joint, carrier, include_trace)}
    ]
    events: list[dict[str, object]] = []
    discrepancy_values: list[float] = []
    control_values: list[float] = [numerical_tail_bound(), abs(math.cos(PHI) ** 2 + math.sin(PHI) ** 2 - 1.0)]
    maximum_fresh = 0.0

    def add_discrepancies(record: dict[str, object]) -> None:
        for key, value in record.items():
            if isinstance(value, float) and value is not None and (
                "residual" in key or "max_abs" in key or "distance" in key
            ):
                discrepancy_values.append(abs(value))

    add_discrepancies(checkpoints[0])

    for event in range(length):
        pre_fresh = fresh_lineage_probability(parent, joint, event)
        maximum_fresh = max(maximum_fresh, pre_fresh)
        allow_joint = blank_probability(parent, joint, event)
        allow_carrier = blank_probability(parent, carrier, event)
        blocked_joint = occupied_probability(parent, joint, event)
        blocked_carrier = occupied_probability(parent, carrier, event)
        q_before_joint = float(np.dot(np.arange(length + 1), sector_weights(joint)))
        q_before_carrier = float(np.dot(np.arange(length + 1), sector_weights(carrier)))

        admitted_joint = joint_admission(parent, joint, event)
        admitted_carrier = carrier_channel(parent, carrier, event)
        q_after_joint = float(np.dot(np.arange(length + 1), sector_weights(admitted_joint)))
        q_after_carrier = float(np.dot(np.arange(length + 1), sector_weights(admitted_carrier)))

        admission_checkpoint = {
            "stage": f"event_{event}_after_admission",
            **compare_states(parent, admitted_joint, admitted_carrier, include_trace),
        }
        checkpoints.append(admission_checkpoint)
        add_discrepancies(admission_checkpoint)

        actual_joint, actual_current_joint, actual_joint_drift = transport(parent, admitted_joint)
        actual_carrier, actual_current_carrier, actual_carrier_drift = transport(
            parent, admitted_carrier
        )
        null_joint, null_current_joint, null_joint_drift = transport(parent, joint)
        null_carrier, null_current_carrier, null_carrier_drift = transport(parent, carrier)
        delta_joint = actual_current_joint - null_current_joint
        delta_carrier = actual_current_carrier - null_current_carrier

        integrated_actual = float(np.max(np.abs(actual_current_joint - actual_current_carrier)))
        integrated_null = float(np.max(np.abs(null_current_joint - null_current_carrier)))
        integrated_delta = float(np.max(np.abs(delta_joint - delta_carrier)))
        discrepancy_values.extend(
            [
                abs(allow_joint - allow_carrier),
                abs(blocked_joint - blocked_carrier),
                abs((q_after_joint - q_before_joint) - (q_after_carrier - q_before_carrier)),
                integrated_actual,
                integrated_null,
                integrated_delta,
            ]
        )
        event_controls = {
            "actual_carrier_absolute_norm_error": abs(factor_norm(actual_carrier) - 1.0),
            "actual_carrier_norm_drift": actual_carrier_drift,
            "actual_joint_absolute_norm_error": abs(factor_norm(actual_joint) - 1.0),
            "actual_joint_norm_drift": actual_joint_drift,
            "admitted_carrier_absolute_norm_error": abs(
                factor_norm(admitted_carrier) - 1.0
            ),
            "admitted_joint_absolute_norm_error": abs(factor_norm(admitted_joint) - 1.0),
            "null_carrier_absolute_norm_error": abs(factor_norm(null_carrier) - 1.0),
            "null_carrier_norm_drift": null_carrier_drift,
            "null_joint_absolute_norm_error": abs(factor_norm(null_joint) - 1.0),
            "null_joint_norm_drift": null_joint_drift,
        }
        control_values.extend(event_controls.values())

        joint = actual_joint
        carrier = actual_carrier
        transport_checkpoint = {
            "stage": f"event_{event}_after_transport",
            **compare_states(parent, joint, carrier, include_trace),
        }
        checkpoints.append(transport_checkpoint)
        add_discrepancies(transport_checkpoint)
        events.append(
            {
                "allow_probability_disagreement": abs(allow_joint - allow_carrier),
                "blocked_probability_disagreement": abs(blocked_joint - blocked_carrier),
                "event": event,
                "fresh_lineage_probability": pre_fresh,
                "integrated_actual_current_max_abs": integrated_actual,
                "integrated_delta_current_max_abs": integrated_delta,
                "integrated_null_current_max_abs": integrated_null,
                "norm_controls": event_controls,
                "write_disagreement": abs(
                    (q_after_joint - q_before_joint) - (q_after_carrier - q_before_carrier)
                ),
            }
        )

    maximum_disagreement = max(discrepancy_values, default=0.0)
    maximum_control = max(control_values, default=0.0)
    passed = (
        maximum_disagreement <= EQUIVALENCE_TOLERANCE
        and maximum_control <= CONTROL_TOLERANCE
        and maximum_fresh <= EQUIVALENCE_TOLERANCE
        and len(events) == length
    )
    return {
        "basis": {
            "carrier_order": "descending_integer_fixed_weight",
            "edge_order": "connectors_first_then_rails__each_reverse_site_order",
            "joint_dimension": sum(
                len(parent.lineage_words[q]) * len(parent.sectors[q].words)
                for q in range(length + 1)
            ),
            "lineage_order": "descending_integer_fixed_weight",
        },
        "checkpoints": checkpoints,
        "events": events,
        "length": length,
        "maximum_absolute_norm_control_error": maximum_control,
        "maximum_fresh_lineage_probability": maximum_fresh,
        "maximum_full_reduced_disagreement": maximum_disagreement,
        "passed": passed,
    }


def build_result() -> dict[str, object]:
    dependencies = {
        name: {"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path)}
        for name, path in DEPENDENCIES.items()
    }
    dependencies["hostile_source"] = {
        "path": str(Path(__file__).resolve().relative_to(ROOT)),
        "sha256": sha256_file(Path(__file__).resolve()),
    }
    results = [run_length(length) for length in MANDATORY_LENGTHS]
    passed = all(bool(result["passed"]) for result in results)
    payload: dict[str, object] = {
        "claim_boundary": (
            "FINITE_OWNER_ONCE_ACCUMULATION_CARRIER_MARGINAL_ONLY__"
            "NO_LINEAGE_POSTSELECTION_REVISIT_RECORD_READER_GATE_RGRL_OR_GRAVITY"
        ),
        "dependencies": dependencies,
        "disposition": (
            "PASS_EXACT_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE__FINITE_ACCUMULATION_SCOPE_ONLY"
            if passed
            else "OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_REJECTED_OR_UNRESOLVED"
        ),
        "independence": {
            "historical_matrix_imports": False,
            "target_matrix_imports": False,
            "target_result_values_read": False,
            "target_verifier_imports": False,
        },
        "parameters": {
            "control_tolerance": CONTROL_TOLERANCE,
            "dwell": DWELL,
            "equivalence_tolerance": EQUIVALENCE_TOLERANCE,
            "lengths": list(MANDATORY_LENGTHS),
            "phi": PHI,
            "taylor_order": TAYLOR_ORDER,
            "transport_substeps": TRANSPORT_SUBSTEPS,
            "transport_taylor_error_bound": numerical_tail_bound(),
        },
        "results": results,
        "schema": "HOSTILE_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001",
    }
    if not finite_values(payload):
        raise AssertionError("nonfinite value in deterministic result")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build_result()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(result["disposition"])
    for item in result["results"]:
        print(
            f"L={item['length']} disagreement={item['maximum_full_reduced_disagreement']:.3e} "
            f"control={item['maximum_absolute_norm_control_error']:.3e} "
            f"fresh={item['maximum_fresh_lineage_probability']:.3e}"
        )
    return 0 if result["disposition"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
