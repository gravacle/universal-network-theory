#!/usr/bin/env python3
"""Synthetic-only tests for the held-out target streamed adapter."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

import heldout_target_adapter as heldout


def initial_shards(length: int) -> list[np.ndarray]:
    blocks = [
        np.zeros(
            (len(heldout.fixed_words(length - 1, q)), len(heldout.fixed_words(2 * length, q))),
            dtype=np.complex128,
        )
        for q in range(length)
    ]
    blocks[0][0, 0] = 1.0
    return blocks


class StreamedAccumulatorTests(unittest.TestCase):
    def test_frozen_protocol_and_gate_are_hash_bound(self) -> None:
        record = heldout.authenticate_heldout_protocol()
        self.assertEqual(record["sha256"], heldout.HELDOUT_PROTOCOL_SHA256)
        self.assertEqual(record["gate_sha256"], heldout.HELDOUT_GATE_SHA256)

    def test_physical_entry_refuses_without_exact_role_authorization(self) -> None:
        with self.assertRaises(heldout.HeldoutRefusal):
            heldout.run_fine_terminal_from_retained(
                10,
                authorization=None,
                telemetry_path=Path("does-not-exist.json"),
                now_epoch_seconds=0,
            )

    def test_seed_authority_is_authenticated_without_heldout_values(self) -> None:
        record = heldout.authenticate_seed_authority()
        self.assertEqual(record["classification"], heldout.SEED_CLASSIFICATION)
        self.assertGreater(record["T_4_8"], 1.0)

    def test_history_headers_authenticate_without_reading_payload_values(self) -> None:
        for length in (10, 12):
            history = heldout.authenticate_retained_history(
                length, verify_payload_hashes=False
            )
            self.assertEqual(len(history.shards), length)
            self.assertEqual(history.shards[-1].shape[0], 1)

    def test_blank_state_terminal_stream_is_normalized_and_null_witness(self) -> None:
        length = 3
        backend = heldout.SyntheticBackend(length)
        result = heldout.stream_terminal_children(
            length=length,
            shards=initial_shards(length),
            backend=backend,
            resolution="synthetic",
        )
        self.assertAlmostEqual(result["registered"]["probability"], 1.0, places=14)
        self.assertAlmostEqual(result["registered"]["D"], 0.0, places=14)
        self.assertLessEqual(result["residuals"]["row_column_accumulator"], 1.0e-14)
        self.assertLessEqual(result["residuals"]["marginal_reconstruction"], 1.0e-14)
        self.assertFalse(result["streaming"]["full_terminal_array_allocated"])

    def test_streamed_children_match_explicit_small_terminal_state(self) -> None:
        length = 3
        backend = heldout.SyntheticBackend(length)
        shards = initial_shards(length)
        # A normalized H_(L-1) superposition across q=0 and q=1.
        shards[0][0, 0] = np.sqrt(0.4)
        q1 = shards[1]
        q1[0, 0] = np.sqrt(0.2)
        q1[1, 2] = 1.0j * np.sqrt(0.4)
        result = heldout.stream_terminal_children(
            length=length,
            shards=shards,
            backend=backend,
            resolution="synthetic",
        )

        # Build the full H_L probability blocks directly for an independent
        # small-state comparison.  Identity evolution makes the reconstruction
        # transparent while still exercising both terminal children.
        full: list[np.ndarray] = [
            np.zeros(
                (len(heldout.fixed_words(length, q)), len(heldout.fixed_words(2 * length, q))),
                dtype=float,
            )
            for q in range(length + 1)
        ]
        event = length - 1
        cosine = np.cos(heldout.PHI)
        sine = np.sin(heldout.PHI)
        for old_q, old in enumerate(shards):
            old_lineages = backend.lineage_words(length - 1, old_q)
            full_lineages = backend.lineage_words(length, old_q)
            lineage_lookup = {int(word): index for index, word in enumerate(full_lineages)}
            blank, destination = backend.admission(event, old_q)
            stay_probability = np.abs(old) ** 2
            stay_probability[:, blank] *= cosine * cosine
            for row, raw_word in enumerate(old_lineages):
                full[old_q][lineage_lookup[int(raw_word)]] += stay_probability[row]
            if len(blank):
                accepted_lineages = backend.lineage_words(length, old_q + 1)
                accepted_lookup = {
                    int(word): index for index, word in enumerate(accepted_lineages)
                }
                for row, raw_word in enumerate(old_lineages):
                    target_row = accepted_lookup[int(raw_word) | (1 << event)]
                    full[old_q + 1][target_row, destination] += (
                        sine * sine * np.abs(old[row, blank]) ** 2
                    )

        explicit = []
        for q, probability in enumerate(full):
            accumulator = heldout.SectorMomentAccumulator(
                length, q, backend.carrier_words(q)
            )
            accumulator.consume(backend.lineage_words(length, q), np.sqrt(probability))
            explicit.append(accumulator)
        expected = heldout.finalize_accumulators(explicit)
        for key in ("probability", "w", "w_sham", "D", "w_shuffle"):
            self.assertAlmostEqual(
                result["registered"][key], expected["registered"][key], places=14
            )

    def test_registered_match_and_cross_controls_have_opposite_witness(self) -> None:
        length = 2
        backend = heldout.SyntheticBackend(length)
        lineages = backend.lineage_words(length, 1)
        carriers = backend.carrier_words(1)
        lineage_lookup = {int(word): index for index, word in enumerate(lineages)}
        carrier_lookup = {int(word): index for index, word in enumerate(carriers)}
        observed: list[float] = []
        for pairs in (
            ((1, 1), (2, 2)),
            ((1, 2), (2, 1)),
        ):
            amplitude = np.zeros((len(lineages), len(carriers)), dtype=np.complex128)
            for lineage, carrier in pairs:
                amplitude[lineage_lookup[lineage], carrier_lookup[carrier]] = np.sqrt(0.5)
            accumulator = heldout.SectorMomentAccumulator(
                length, 1, carriers
            )
            accumulator.consume(lineages, amplitude)
            record = accumulator.finalize()
            self.assertAlmostEqual(record["w_sham_q"], 0.0, places=15)
            self.assertLessEqual(record["residuals"]["row_column"], 1.0e-15)
            observed.append(record["D_q"])
        self.assertAlmostEqual(observed[0], 1.0 / (2 * length), places=15)
        self.assertAlmostEqual(observed[1], -1.0 / (2 * length), places=15)

    def test_accumulator_matches_independent_nested_formula(self) -> None:
        length = 3
        q = 1
        backend = heldout.SyntheticBackend(length)
        lineages = backend.lineage_words(length, q)
        carriers = backend.carrier_words(q)
        raw = np.arange(1, len(lineages) * len(carriers) + 1, dtype=float).reshape(
            len(lineages), len(carriers)
        )
        amplitude = raw.astype(np.complex128) * (1.0 + 0.25j)
        amplitude /= np.linalg.norm(amplitude)
        probability = np.abs(amplitude) ** 2

        observed = 0.0
        for row, lineage in enumerate(lineages):
            for column, carrier in enumerate(carriers):
                kernel = sum(
                    ((((int(lineage) >> event) & 1) - q / length)
                     * ((int(carrier) >> event) & 1))
                    for event in range(length)
                ) / length
                observed += float(probability[row, column]) * kernel
        lineage_marginal = np.sum(probability, axis=1)
        carrier_marginal = np.sum(probability, axis=0)
        sham = 0.0
        for row, lineage in enumerate(lineages):
            for column, carrier in enumerate(carriers):
                kernel = sum(
                    ((((int(lineage) >> event) & 1) - q / length)
                     * ((int(carrier) >> event) & 1))
                    for event in range(length)
                ) / length
                sham += (
                    float(lineage_marginal[row])
                    * float(carrier_marginal[column])
                    * kernel
                )

        accumulator = heldout.SectorMomentAccumulator(length, q, carriers)
        accumulator.consume(lineages, amplitude)
        record = accumulator.finalize()
        self.assertAlmostEqual(record["p_q"], 1.0, places=14)
        self.assertAlmostEqual(record["w_q"], observed, places=14)
        self.assertAlmostEqual(record["w_sham_q"], sham, places=14)
        self.assertAlmostEqual(record["D_q"], observed - sham, places=14)
        self.assertLessEqual(record["residuals"]["row_column"], 1.0e-14)

    def test_nonfinite_terminal_amplitudes_fail_closed(self) -> None:
        length = 2
        backend = heldout.SyntheticBackend(length)
        shards = initial_shards(length)
        shards[0][0, 0] = np.nan
        with self.assertRaises(heldout.HeldoutRefusal):
            heldout.stream_terminal_children(
                length=length,
                shards=shards,
                backend=backend,
                resolution="synthetic",
            )

    def test_strict_json_rejects_duplicate_and_nonfinite_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            duplicate = Path(directory) / "duplicate.json"
            duplicate.write_text('{"a": 1, "a": 2}\n', encoding="utf-8")
            with self.assertRaises(heldout.HeldoutRefusal):
                heldout.strict_json(duplicate)
            nonfinite = Path(directory) / "nonfinite.json"
            nonfinite.write_text('{"a": NaN}\n', encoding="utf-8")
            with self.assertRaises(heldout.HeldoutRefusal):
                heldout.strict_json(nonfinite)


if __name__ == "__main__":
    unittest.main()
