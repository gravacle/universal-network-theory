#!/usr/bin/env python3
"""Finite verifier for the owner-once lineage carrier-reduction theorem.

The target evolution is the historical joint pure-state implementation in
``compute_seed_history.py``.  The comparison evolution is independently
implemented here as a carrier-only completely positive map, represented by
its Kraus ensemble.  Kraus outcome labels are retained only to evaluate the
reduced density matrix; they are never read by the carrier dynamics.

No historical file is modified.  The JSON output deliberately excludes wall
times, timestamps, host names, and absolute paths so identical inputs produce
identical bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET_SOURCE = (
    ROOT
    / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001"
    / "compute_seed_history.py"
)
CLOSURE_ROOT = ROOT / "DEVELOPMENT_R_OWNER_ONCE_CARRIER_MARGINAL_CLOSURE_V001"
FROZEN_DOCUMENTS = {
    "theorem": (
        CLOSURE_ROOT / "THEOREM.md",
        "2850e32eae9c84a194047877219de681995850e5c4c86c24690654d202524584",
    ),
    "protocol": (
        CLOSURE_ROOT / "PROTOCOL.md",
        "81010287548dc44ddfa291765727a6a5bca001570d6a93accd78ff0dd151c76d",
    ),
}
DEFAULT_OUTPUT = HERE / "CARRIER_REDUCTION_RESULT_V001.json"
SCHEMA = "LINEAGE_CARRIER_REDUCTION_VERIFIER_V001"
PHI = math.pi / 4.0
DWELL = math.pi / 2.0
TAYLOR_ORDER = 12
DEFAULT_STEPS = 16
DEFAULT_LENGTHS = (4, 6)
SUPPORTED_LENGTHS = (4, 6, 8)
ABS_TOLERANCE = 2.0e-10


class VerificationFailure(RuntimeError):
    """A fail-closed verifier predicate was violated."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def authenticate_frozen_documents() -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    for label, (path, expected) in FROZEN_DOCUMENTS.items():
        if not path.is_file():
            raise VerificationFailure(f"frozen {label} is absent: {path}")
        actual = sha256_file(path)
        if actual != expected:
            raise VerificationFailure(
                f"frozen {label} SHA-256 mismatch: expected={expected} actual={actual}"
            )
        records[label] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": actual,
        }
    return records


def fixed_words(width: int, weight: int) -> np.ndarray:
    dtype = np.uint32 if width <= 32 else np.uint64
    words = np.empty(math.comb(width, weight), dtype=dtype)
    for index, positions in enumerate(itertools.combinations(range(width), weight)):
        word = 0
        for position in positions:
            word |= 1 << position
        words[index] = word
    return words


def prism_edges(length: int) -> list[tuple[int, int, str]]:
    edges: list[tuple[int, int, str]] = []
    for rail in range(2):
        offset = rail * length
        for site in range(length):
            edges.append((offset + site, offset + (site + 1) % length, f"rail_{rail + 1}"))
    for site in range(length):
        edges.append((site, length + (site + 1) % length, "connector"))
    return edges


def load_target_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("historical_seed_history_target", TARGET_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load target source: {TARGET_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@dataclass
class CarrierSector:
    """One exact sharp-carrier-number block of the prism ladder."""

    words: np.ndarray
    lookup: dict[int, int]
    pairs: list[tuple[np.ndarray, np.ndarray]]

    @classmethod
    def build(
        cls, length: int, q: int, edges: Sequence[tuple[int, int, str]]
    ) -> "CarrierSector":
        words = fixed_words(2 * length, q)
        lookup = {int(word): index for index, word in enumerate(words)}
        pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for u, v, _ in edges:
            left = np.flatnonzero(
                (((words >> u) & 1) == 1) & (((words >> v) & 1) == 0)
            ).astype(np.int32)
            if len(left):
                mask = np.array((1 << u) | (1 << v), dtype=words.dtype)
                right = np.fromiter(
                    (lookup[int(words[index] ^ mask)] for index in left),
                    dtype=np.int32,
                    count=len(left),
                )
            else:
                right = np.empty(0, dtype=np.int32)
            pairs.append((left, right))
        return cls(words=words, lookup=lookup, pairs=pairs)

    def h_action(self, rows: np.ndarray) -> np.ndarray:
        out = np.zeros_like(rows)
        for left, right in self.pairs:
            out[:, left] -= rows[:, right]
            out[:, right] -= rows[:, left]
        return out

    def currents(self, rows: np.ndarray) -> np.ndarray:
        answer = np.zeros(len(self.pairs), dtype=float)
        for edge, (left, right) in enumerate(self.pairs):
            answer[edge] = 2.0 * float(np.imag(np.vdot(rows[:, left], rows[:, right])))
        return answer


class CarrierChannel:
    """Carrier-only channel with an unread Kraus-outcome purification.

    A row label records which forward Kraus outcomes occurred.  No operation
    conditions on that label.  Consequently the row arrays are only a compact
    purification of the reduced carrier density matrix.
    """

    def __init__(self, length: int):
        self.length = length
        self.sites = 2 * length
        self.edges = prism_edges(length)
        self.sectors = [
            CarrierSector.build(length, q, self.edges) for q in range(length + 1)
        ]
        self.labels = [fixed_words(length, q) for q in range(length + 1)]
        self.label_lookup = [
            {int(word): index for index, word in enumerate(words)} for words in self.labels
        ]
        self.admission_maps = self._build_admission_maps()

    def _build_admission_maps(
        self,
    ) -> list[list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]]:
        maps_by_event = []
        for event in range(self.length):
            event_maps = []
            for q in range(self.length):
                source_rows = np.flatnonzero(((self.labels[q] >> event) & 1) == 0).astype(
                    np.int32
                )
                destination_rows = np.fromiter(
                    (
                        self.label_lookup[q + 1][int(self.labels[q][row]) | (1 << event)]
                        for row in source_rows
                    ),
                    dtype=np.int32,
                    count=len(source_rows),
                )
                source_columns = np.flatnonzero(
                    ((self.sectors[q].words >> event) & 1) == 0
                ).astype(np.int32)
                destination_columns = np.fromiter(
                    (
                        self.sectors[q + 1].lookup[
                            int(self.sectors[q].words[column]) | (1 << event)
                        ]
                        for column in source_columns
                    ),
                    dtype=np.int32,
                    count=len(source_columns),
                )
                event_maps.append(
                    (source_rows, source_columns, destination_rows, destination_columns)
                )
            maps_by_event.append(event_maps)
        return maps_by_event

    def initial(self) -> list[np.ndarray]:
        blocks = [
            np.zeros((len(self.labels[q]), len(self.sectors[q].words)), dtype=np.complex128)
            for q in range(self.length + 1)
        ]
        blocks[0][0, 0] = 1.0
        return blocks

    @staticmethod
    def norm(blocks: Sequence[np.ndarray]) -> float:
        return float(sum(np.vdot(block, block).real for block in blocks))

    def apply_channel(self, blocks: Sequence[np.ndarray], event: int) -> list[np.ndarray]:
        """Apply K0/K1 without reading any earlier Kraus label."""
        cosine = math.cos(PHI)
        sine = math.sin(PHI)
        result = [block.copy() for block in blocks]

        # K0 = P_occupied + cos(phi) P_blank.
        for q, sector in enumerate(self.sectors):
            blank = np.flatnonzero(((sector.words >> event) & 1) == 0)
            result[q][:, blank] *= cosine

        # K1 = -i sin(phi) a_event^dagger P_blank.  The row is an
        # environmental outcome label only; later dynamics never reads it.
        for q, mapping in enumerate(self.admission_maps[event]):
            source_rows, source_columns, destination_rows, destination_columns = mapping
            source = np.ix_(source_rows, source_columns)
            destination = np.ix_(destination_rows, destination_columns)
            result[q + 1][destination] += -1j * sine * blocks[q][source]
        return result

    def taylor_step(self, block: np.ndarray, q: int, step: float) -> np.ndarray:
        updated = block.copy()
        term = block.copy()
        for order in range(1, TAYLOR_ORDER + 1):
            term = (-1j * step / order) * self.sectors[q].h_action(term)
            updated += term
        return updated

    def transport(
        self, blocks: Sequence[np.ndarray], steps: int
    ) -> tuple[list[np.ndarray], np.ndarray]:
        result = [block.copy() for block in blocks]
        step = DWELL / steps
        integrated = self.currents(result)
        for index in range(1, steps + 1):
            for q in range(self.length + 1):
                result[q] = self.taylor_step(result[q], q, step)
            weight = 1 if index == steps else (4 if index % 2 else 2)
            integrated += weight * self.currents(result)
        integrated *= step / 3.0
        return result, integrated

    def sector_weights(self, blocks: Sequence[np.ndarray]) -> np.ndarray:
        return np.array([float(np.vdot(block, block).real) for block in blocks])

    def occupations(self, blocks: Sequence[np.ndarray]) -> np.ndarray:
        answer = np.zeros(self.sites, dtype=float)
        for q, block in enumerate(blocks):
            probabilities = np.sum(np.abs(block) ** 2, axis=0)
            for site in range(self.sites):
                occupied = ((self.sectors[q].words >> site) & 1) == 1
                answer[site] += float(np.sum(probabilities[occupied]))
        return answer

    def currents(self, blocks: Sequence[np.ndarray]) -> np.ndarray:
        answer = np.zeros(len(self.edges), dtype=float)
        for q, block in enumerate(blocks):
            answer += self.sectors[q].currents(block)
        return answer


class JointProjection:
    """Map the historical joint basis into (Kraus label, carrier) blocks."""

    def __init__(self, target_parent: object, channel: CarrierChannel):
        length = channel.length
        loaded_mask = (1 << length) - 1
        words = target_parent.words
        carrier_words = target_parent.carrier_words
        carrier_counts = target_parent.carrier_counts
        self.maps: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for q in range(length + 1):
            indices = np.flatnonzero(carrier_counts == q).astype(np.int64)
            spent = np.bitwise_xor(
                np.bitwise_and(words[indices], np.array(loaded_mask, dtype=words.dtype)),
                np.array(loaded_mask, dtype=words.dtype),
            )
            row = np.fromiter(
                (channel.label_lookup[q][int(word)] for word in spent),
                dtype=np.int64,
                count=len(indices),
            )
            column = np.fromiter(
                (channel.sectors[q].lookup[int(word)] for word in carrier_words[indices]),
                dtype=np.int64,
                count=len(indices),
            )
            self.maps.append((indices, row, column))

    def blocks(self, state: np.ndarray, channel: CarrierChannel) -> list[np.ndarray]:
        result = [
            np.zeros((len(channel.labels[q]), len(channel.sectors[q].words)), dtype=np.complex128)
            for q in range(channel.length + 1)
        ]
        for q, (indices, rows, columns) in enumerate(self.maps):
            result[q][rows, columns] = state[indices]
        return result


def explicit_trace_distance(
    full: Sequence[np.ndarray], reduced: Sequence[np.ndarray]
) -> float:
    """Exact trace distance between block-diagonal reduced carrier states."""
    distance = 0.0
    for q, (left, right) in enumerate(zip(full, reduced)):
        require_finite_array(left, f"explicit trace target q={q}")
        require_finite_array(right, f"explicit trace comparison q={q}")
        # Explicit Einstein contraction keeps this small L4 audit independent
        # of platform BLAS status flags while expressing the partial trace
        # directly: rho[c,d] = sum_s psi[s,c] psi[s,d]^*.
        rho_left = np.einsum("sc,sd->cd", left, left.conjugate(), optimize=False)
        rho_right = np.einsum("sc,sd->cd", right, right.conjugate(), optimize=False)
        delta = rho_left - rho_right
        delta = 0.5 * (delta + delta.conjugate().T)
        contribution = 0.5 * float(np.sum(np.abs(np.linalg.eigvalsh(delta))))
        distance += finite_residual(contribution, f"explicit trace distance q={q}")
    return finite_residual(distance, "explicit trace distance total")


def require_finite_array(array: np.ndarray, label: str) -> None:
    if not bool(np.all(np.isfinite(array))):
        raise VerificationFailure(f"nonfinite array in {label}")


def finite_residual(value: object, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise VerificationFailure(f"nonnumeric residual {label}: {value!r}") from error
    if not math.isfinite(result):
        raise VerificationFailure(f"nonfinite residual {label}: {result!r}")
    return abs(result)


def validated_nonnegative(value: float, scale: float, label: str) -> float:
    """Accept only a roundoff-sized negative squared-norm expression."""
    raw = float(value)
    reference = float(scale)
    if not math.isfinite(raw) or not math.isfinite(reference):
        raise VerificationFailure(
            f"nonfinite nonnegative check {label}: value={raw!r} scale={reference!r}"
        )
    roundoff_floor = -128.0 * np.finfo(float).eps * max(1.0, abs(reference))
    if raw < roundoff_floor:
        raise VerificationFailure(
            f"invalid negative squared residual {label}: value={raw:.17g} "
            f"roundoff_floor={roundoff_floor:.17g}"
        )
    return max(0.0, raw)


def carrier_hilbert_schmidt_residual(
    full: Sequence[np.ndarray], reduced: Sequence[np.ndarray]
) -> float:
    """Exact reduced-density Frobenius residual via small environment Grams."""
    squared = 0.0
    for q, (left, right) in enumerate(zip(full, reduced)):
        require_finite_array(left, f"Hilbert-Schmidt target q={q}")
        require_finite_array(right, f"Hilbert-Schmidt comparison q={q}")
        left_gram = np.einsum("sc,tc->st", left, left.conjugate(), optimize=False)
        right_gram = np.einsum("sc,tc->st", right, right.conjugate(), optimize=False)
        cross_gram = np.einsum("sc,tc->st", left, right.conjugate(), optimize=False)
        left_squared = float(np.vdot(left_gram, left_gram).real)
        right_squared = float(np.vdot(right_gram, right_gram).real)
        cross_squared = float(np.vdot(cross_gram, cross_gram).real)
        term = left_squared + right_squared - 2.0 * cross_squared
        scale = left_squared + right_squared + 2.0 * cross_squared
        squared += validated_nonnegative(term, scale, f"Hilbert-Schmidt q={q}")
    return math.sqrt(validated_nonnegative(squared, squared, "Hilbert-Schmidt total"))


def purification_metrics(
    full: Sequence[np.ndarray], reduced: Sequence[np.ndarray]
) -> dict[str, float]:
    for q, (left, right) in enumerate(zip(full, reduced)):
        require_finite_array(left, f"purification target q={q}")
        require_finite_array(right, f"purification comparison q={q}")
    differences = [left - right for left, right in zip(full, reduced)]
    l2 = math.sqrt(sum(float(np.vdot(item, item).real) for item in differences))
    linf = max((float(np.max(np.abs(item))) for item in differences if item.size), default=0.0)
    norm_left = sum(float(np.vdot(item, item).real) for item in full)
    norm_right = sum(float(np.vdot(item, item).real) for item in reduced)
    overlap = sum(np.vdot(left, right) for left, right in zip(full, reduced))
    denominator = math.sqrt(max(0.0, norm_left * norm_right))
    if denominator:
        phase = np.conjugate(overlap) / abs(overlap) if abs(overlap) else 1.0 + 0.0j
        normalized_l2_squared = sum(
            float(
                np.vdot(
                    left / math.sqrt(norm_left) - phase * right / math.sqrt(norm_right),
                    left / math.sqrt(norm_left) - phase * right / math.sqrt(norm_right),
                ).real
            )
            for left, right in zip(full, reduced)
        )
        # Contractivity of trace distance plus the pure-state inequality
        # D <= ||psi-phi|| gives a stable bound without subtracting two
        # nearly equal floating-point numbers from one.
        trace_upper = math.sqrt(max(0.0, normalized_l2_squared))
    else:
        trace_upper = 0.0
    return {
        "purification_l2": l2,
        "purification_linf": linf,
        "reduced_trace_distance_upper_bound": trace_upper,
        "full_norm_error": abs(norm_left - 1.0),
        "carrier_channel_norm_error": abs(norm_right - 1.0),
    }


def compare_stage(
    target_parent: object,
    channel: CarrierChannel,
    projection: JointProjection,
    full_state: np.ndarray,
    carrier_blocks: Sequence[np.ndarray],
    explicit_trace: bool,
) -> dict[str, float | None]:
    full_blocks = projection.blocks(full_state, channel)
    metrics: dict[str, float | None] = purification_metrics(full_blocks, carrier_blocks)
    metrics["reduced_carrier_hilbert_schmidt"] = carrier_hilbert_schmidt_residual(
        full_blocks, carrier_blocks
    )
    metrics["sector_weight_linf"] = float(
        np.max(
            np.abs(
                np.asarray(target_parent.sector_weights(full_state))[: channel.length + 1]
                - channel.sector_weights(carrier_blocks)
            )
        )
    )
    metrics["occupation_linf"] = float(
        np.max(
            np.abs(
                np.asarray(target_parent.occupations(full_state))
                - channel.occupations(carrier_blocks)
            )
        )
    )
    metrics["current_linf"] = float(
        np.max(
            np.abs(
                np.asarray(target_parent.currents(full_state))
                - channel.currents(carrier_blocks)
            )
        )
    )
    metrics["reduced_carrier_trace_distance"] = (
        explicit_trace_distance(full_blocks, carrier_blocks) if explicit_trace else None
    )
    return metrics


def freshness_probability(
    blocks: Sequence[np.ndarray], channel: CarrierChannel, event: int
) -> float:
    total = 0.0
    for q, block in enumerate(blocks):
        spent_rows = ((channel.labels[q] >> event) & 1) == 1
        if np.any(spent_rows):
            view = block[spent_rows]
            total += float(np.vdot(view, view).real)
    return total


CONTROL_KEYS = frozenset(("full_norm_error", "carrier_channel_norm_error"))


def stage_maxima(record: dict[str, object]) -> tuple[float, float]:
    equivalence: list[float] = []
    controls: list[float] = []
    for stage_name in ("after_admission", "after_transport"):
        stage = record[stage_name]
        if not isinstance(stage, dict):
            raise AssertionError("malformed stage record")
        for key, value in stage.items():
            if key == "reduced_carrier_trace_distance" and value is None:
                continue
            destination = controls if key in CONTROL_KEYS else equivalence
            destination.append(finite_residual(value, f"{stage_name}.{key}"))
    controls.append(
        finite_residual(
            record["fresh_lineage_probability_before_admission"],
            "fresh_lineage_probability_before_admission",
        )
    )
    return max(equivalence, default=0.0), max(controls, default=0.0)


def metric_maxima(stage: dict[str, float | None]) -> tuple[float, float]:
    equivalence = [
        finite_residual(value, key)
        for key, value in stage.items()
        if value is not None and key not in CONTROL_KEYS
    ]
    controls = [
        finite_residual(value, key)
        for key, value in stage.items()
        if value is not None and key in CONTROL_KEYS
    ]
    return max(equivalence, default=0.0), max(controls, default=0.0)


def verify_length(length: int, steps: int, explicit_trace: bool) -> dict[str, object]:
    if length not in SUPPORTED_LENGTHS:
        raise ValueError(f"unsupported L={length}; choose from {SUPPORTED_LENGTHS}")
    target_module = load_target_module()
    target_parent = target_module.Parent(length)
    channel = CarrierChannel(length)
    projection = JointProjection(target_parent, channel)
    full_state = target_parent.initial_state()
    carrier_blocks = channel.initial()
    events: list[dict[str, object]] = []

    initial = compare_stage(
        target_parent, channel, projection, full_state, carrier_blocks, explicit_trace
    )
    for event in range(length):
        freshness = freshness_probability(carrier_blocks, channel, event)
        full_admitted = target_parent.apply_admission(full_state, event)
        carrier_admitted = channel.apply_channel(carrier_blocks, event)
        admission = compare_stage(
            target_parent,
            channel,
            projection,
            full_admitted,
            carrier_admitted,
            explicit_trace,
        )

        _, full_null_integrated = target_parent.transport(full_state, steps)
        _, carrier_null_integrated = channel.transport(carrier_blocks, steps)
        full_state, full_integrated = target_parent.transport(full_admitted, steps)
        carrier_blocks, carrier_integrated = channel.transport(carrier_admitted, steps)
        transport = compare_stage(
            target_parent,
            channel,
            projection,
            full_state,
            carrier_blocks,
            explicit_trace,
        )
        transport["integrated_current_linf"] = float(
            np.max(np.abs(full_integrated - carrier_integrated))
        )
        transport["null_integrated_current_linf"] = float(
            np.max(np.abs(full_null_integrated - carrier_null_integrated))
        )
        transport["delta_integrated_current_linf"] = float(
            np.max(
                np.abs(
                    (full_integrated - full_null_integrated)
                    - (carrier_integrated - carrier_null_integrated)
                )
            )
        )
        record: dict[str, object] = {
            "event": event + 1,
            "fresh_lineage_probability_before_admission": freshness,
            "after_admission": admission,
            "after_transport": transport,
        }
        equivalence, controls = stage_maxima(record)
        record["maximum_equivalence_disagreement"] = equivalence
        record["maximum_numerical_control_error"] = controls
        events.append(record)

    initial_equivalence, initial_controls = metric_maxima(initial)
    maximum_equivalence = max(
        [initial_equivalence]
        + [float(event["maximum_equivalence_disagreement"]) for event in events]
    )
    maximum_controls = max(
        [initial_controls]
        + [float(event["maximum_numerical_control_error"]) for event in events]
    )
    passed = maximum_equivalence <= ABS_TOLERANCE and maximum_controls <= ABS_TOLERANCE
    return {
        "L": length,
        "joint_dimension": int(target_parent.dimension),
        "carrier_sector_dimensions": [len(sector.words) for sector in channel.sectors],
        "events": events,
        "explicit_trace_distance_computed": explicit_trace,
        "initial": initial,
        "maximum_equivalence_disagreement": maximum_equivalence,
        "maximum_numerical_control_error": maximum_controls,
        "passed": passed,
    }


def build_result(lengths: Sequence[int], steps: int) -> dict[str, object]:
    if steps <= 0:
        raise ValueError("steps must be positive")
    unique_lengths = tuple(dict.fromkeys(int(length) for length in lengths))
    frozen_documents = authenticate_frozen_documents()
    rows = [verify_length(length, steps, explicit_trace=(length == 4)) for length in unique_lengths]
    row_checks_passed = bool(rows) and all(bool(row["passed"]) for row in rows)
    length_set = set(unique_lengths)
    mandatory_coverage = {4, 6}.issubset(length_set)
    supplemental_l8_only = length_set == {8}
    if not rows:
        classification = "INVALID_EMPTY_LENGTH_SET"
        passed = False
    elif mandatory_coverage and row_checks_passed:
        classification = "CARRIER_REDUCTION_VERIFIED_FINITE"
        passed = True
    elif supplemental_l8_only and row_checks_passed:
        classification = "SUPPLEMENTAL_L8_CARRIER_REDUCTION_VERIFIED_FINITE"
        passed = True
    elif row_checks_passed:
        classification = "INCOMPLETE_MANDATORY_PROTOCOL_COVERAGE"
        passed = False
    else:
        classification = "CARRIER_REDUCTION_MISMATCH"
        passed = False
    return {
        "schema": SCHEMA,
        "classification": classification,
        "passed": passed,
        "row_checks_passed": row_checks_passed,
        "primary_protocol_passed": mandatory_coverage and row_checks_passed,
        "supplemental_l8_passed": supplemental_l8_only and row_checks_passed,
        "mandatory_protocol_lengths": [4, 6],
        "parameters": {
            "lengths": list(unique_lengths),
            "phi": PHI,
            "dwell": DWELL,
            "taylor_order": TAYLOR_ORDER,
            "transport_steps": steps,
            "equivalence_tolerance": ABS_TOLERANCE,
            "numerical_control_tolerance": ABS_TOLERANCE,
        },
        "theorem_under_test": {
            "domain": "fresh owner-once one-pass histories",
            "target": "joint lineage-carrier pure-state evolution",
            "comparison": "carrier-only K0/K1 channel with unread Kraus labels",
            "K0": "P_occupied + cos(phi) P_blank",
            "K1": "-i sin(phi) a_event^dagger P_blank",
        },
        "dependencies": {
            "frozen_documents": frozen_documents,
            "historical_target": {
                "path": str(TARGET_SOURCE.relative_to(ROOT)),
                "sha256": sha256_file(TARGET_SOURCE),
            },
            "verifier_sha256": sha256_file(Path(__file__)),
        },
        "rows": rows,
        "claim_boundary": {
            "established_if_passed": (
                "finite numerical equivalence of the joint implementation and the "
                "matched carrier-only channel at the listed L values"
            ),
            "not_established": [
                "an all-L analytic proof",
                "absence of lineage-carrier correlations",
                "absence of a future lineage-reading operation",
                "a gravity theorem",
                "an experimental distinction from standard physics",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lengths", type=int, nargs="+", default=list(DEFAULT_LENGTHS))
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build_result(args.lengths, args.steps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(result["classification"])
    for row in result["rows"]:
        print(
            f"L={row['L']} D={row['joint_dimension']} "
            f"equivalence={row['maximum_equivalence_disagreement']:.6e} "
            f"controls={row['maximum_numerical_control_error']:.6e} "
            f"passed={row['passed']}"
        )


if __name__ == "__main__":
    main()
