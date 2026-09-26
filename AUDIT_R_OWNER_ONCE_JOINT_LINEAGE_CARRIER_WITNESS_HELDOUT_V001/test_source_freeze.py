#!/usr/bin/env python3
"""Synthetic-only tests for the hostile held-out adapter.

No test opens a physical L10/L12 terminal shard and no test calls the physical
execution entry point.  Numerical tests use only constructed L2/L3 arrays.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import tempfile
import time
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest import mock

import numpy as np

import hostile_heldout_joint_witness as heldout


HERE = Path(__file__).resolve().parent


def two_term_accumulator(crossed: bool) -> dict[str, object]:
    length = 3
    q = 1
    lineage_words = np.asarray(heldout.physical.reverse_masks(length, q), dtype=np.uint32)
    carrier_words = np.asarray(heldout.physical.reverse_masks(2 * length, q), dtype=np.uint32)
    lineage_lookup = {int(word): index for index, word in enumerate(lineage_words)}
    carrier_lookup = {int(word): index for index, word in enumerate(carrier_words)}
    block = np.zeros((len(lineage_words), len(carrier_words)), dtype=np.complex128)
    amplitude = 1.0 / math.sqrt(2.0)
    pairs = (
        ((1 << 0), (1 << (1 if crossed else 0))),
        ((1 << 1), (1 << (0 if crossed else 1))),
    )
    for lineage, carrier in pairs:
        block[lineage_lookup[lineage], carrier_lookup[carrier]] = amplitude
    accumulator = heldout.SectorAccumulator(length, q, carrier_words)
    accumulator.consume(
        block,
        np.arange(len(lineage_words), dtype=np.int32),
        lineage_words,
    )
    return accumulator.finish()


class SyntheticCarrier(heldout.physical.CarrierBlock):
    def __init__(self, length: int, q: int, edges: list[tuple[int, int, str]]):
        super().__init__(length, q, edges)
        self.offsets = np.zeros(len(edges) + 1, dtype=np.uint64)

    def release(self) -> None:
        return None


class SyntheticCache:
    def __init__(self, length: int):
        self.length = length

    def carrier(self, q: int, edges: list[tuple[int, int, str]]) -> SyntheticCarrier:
        return SyntheticCarrier(self.length, q, edges)

    def admission(self, event: int, q: int) -> tuple[np.ndarray, np.ndarray]:
        new_words = heldout.physical.reverse_masks(2 * self.length, q)
        occupied = np.flatnonzero(((new_words >> event) & 1) != 0).astype(np.int32)
        old = np.fromiter(
            (
                heldout.v3.reverse_rank(
                    2 * self.length, q - 1, int(new_words[column]) & ~(1 << event)
                )
                for column in occupied
            ),
            dtype=np.int32,
            count=len(occupied),
        )
        return occupied, old


@dataclass
class DenseSource:
    blocks: list[np.ndarray]
    prefix: int

    def open_shard(self, q: int, mode: str = "r") -> np.ndarray:
        if mode != "r":
            raise AssertionError("synthetic source is read-only")
        return self.blocks[q]


class SourceFreezeTests(unittest.TestCase):
    def test_sealed_protocol_and_gate_hashes(self) -> None:
        self.assertEqual(
            heldout.sha256_file(heldout.PROTOCOL), heldout.EXPECTED_PROTOCOL_SHA256
        )
        self.assertEqual(
            heldout.sha256_file(heldout.MACHINE_GATE), heldout.EXPECTED_GATE_SHA256
        )
        self.assertEqual(
            heldout.sha256_file(heldout.SEED_DISPOSITION), heldout.EXPECTED_SEED_SHA256
        )

    def test_authenticated_v003_capacity_is_installed_without_physics_change(self) -> None:
        self.assertEqual(
            heldout.sha256_file(heldout.CAPACITY_REPAIR),
            heldout.EXPECTED_CAPACITY_REPAIR_SHA256,
        )
        self.assertEqual(heldout.HOSTILE_ROUGH.label, "rough")
        self.assertEqual(
            heldout.HOSTILE_ROUGH.checkpoints,
            (16, 24, 32, 48, 64, 80, 96, 112),
        )
        self.assertEqual(heldout.HOSTILE_ROUGH.gauss_order, 18)
        self.assertEqual(heldout.HOSTILE_ROUGH.tolerance, 3.0e-9)
        self.assertEqual(heldout.HOSTILE_SHARP.label, "sharp")
        self.assertEqual(
            heldout.HOSTILE_SHARP.checkpoints,
            (24, 32, 48, 64, 80, 96, 112, 128),
        )
        self.assertEqual(heldout.HOSTILE_SHARP.gauss_order, 28)
        self.assertEqual(heldout.HOSTILE_SHARP.tolerance, 8.0e-11)

        original_rough = heldout.physical.ROUGH
        original_sharp = heldout.physical.SHARP
        try:
            with mock.patch.object(heldout.legacy, "configure") as configure:
                heldout.configure_hostile(10, object(), time.perf_counter())
                configure.assert_called_once()
            self.assertIs(heldout.physical.ROUGH, heldout.HOSTILE_ROUGH)
            self.assertIs(heldout.physical.SHARP, heldout.HOSTILE_SHARP)
        finally:
            heldout.physical.ROUGH = original_rough
            heldout.physical.SHARP = original_sharp

    def test_authority_reads_only_hostile_history_rows(self) -> None:
        gate, hostile, dependencies = heldout.authenticate_authority()
        self.assertEqual(gate["status"], "FROZEN_PRE_HELDOUT_OUTPUT__READY_FOR_AUTHORIZED_EXACT_EXECUTION")
        self.assertEqual(set(hostile), {10, 12})
        self.assertEqual([len(hostile[length]["terminal_shards"]) for length in (10, 12)], [10, 12])
        self.assertIn("hostile_v004r4_consumer", dependencies)

    def test_synthetic_l3_nonidentifiability_pair(self) -> None:
        matched = two_term_accumulator(crossed=False)
        crossed = two_term_accumulator(crossed=True)
        expected = 1.0 / 6.0
        self.assertAlmostEqual(float(matched["witness"]), expected, places=15)
        self.assertAlmostEqual(float(crossed["witness"]), -expected, places=15)
        self.assertLess(float(matched["row_column_disagreement"]), 1.0e-15)
        self.assertLess(float(crossed["row_column_disagreement"]), 1.0e-15)
        self.assertEqual(matched["shuffle_expectation"], 0.0)
        self.assertEqual(matched["sham_negative_control_D"], 0.0)

    def test_streamed_accumulators_match_dense_reference(self) -> None:
        length = 4
        q = 2
        lineage_words = np.asarray(
            heldout.physical.reverse_masks(length, q), dtype=np.uint32
        )
        carrier_words = np.asarray(
            heldout.physical.reverse_masks(2 * length, q), dtype=np.uint32
        )
        generator = np.random.default_rng(0xA009A016)
        vector = (
            generator.normal(size=(len(lineage_words), len(carrier_words)))
            + 1.0j * generator.normal(size=(len(lineage_words), len(carrier_words)))
        )
        vector /= np.linalg.norm(vector)
        probability = np.abs(vector) ** 2
        lineage_bits = np.asarray(
            [[(int(word) >> event) & 1 for event in range(length)] for word in lineage_words],
            dtype=np.float64,
        )
        carrier_bits = np.asarray(
            [[(int(word) >> event) & 1 for event in range(length)] for word in carrier_words],
            dtype=np.float64,
        )
        scores = (lineage_bits - float(q) / float(length)) @ carrier_bits.T / float(length)
        observed = float(np.sum(probability * scores))
        lineage = np.sum(probability, axis=1)
        carrier = np.sum(probability, axis=0)
        weight = float(np.sum(probability))
        sham = float(np.sum(
            np.sum(lineage[:, None] * (lineage_bits - float(q) / float(length)), axis=0)
            * np.sum(carrier[:, None] * carrier_bits, axis=0)
        )) / (float(length) * weight)

        accumulator = heldout.SectorAccumulator(length, q, carrier_words)
        split = len(lineage_words) // 2
        accumulator.consume(
            vector[:split], np.arange(split, dtype=np.int32), lineage_words[:split]
        )
        accumulator.consume(
            vector[split:],
            np.arange(split, len(lineage_words), dtype=np.int32),
            lineage_words[split:],
        )
        result = accumulator.finish()
        for order in ("row_accumulator", "column_accumulator"):
            self.assertAlmostEqual(float(result[order]["observed"]), observed, places=14)
            self.assertAlmostEqual(float(result[order]["sham"]), sham, places=14)
            self.assertAlmostEqual(
                float(result[order]["witness"]), observed - sham, places=14
            )
        self.assertLess(float(result["row_column_disagreement"]), 1.0e-14)
        self.assertLess(float(result["sham_self_covariance_residual"]), 1.0e-14)

    def test_synthetic_l2_terminal_children_are_exact_and_orthogonal(self) -> None:
        length = 2
        event = 1
        old_words = np.asarray(heldout.physical.reverse_masks(2 * length, 0), dtype=np.uint32)
        source = np.asarray([[1.0 + 0.0j]], dtype=np.complex128)
        child0 = heldout.child0_window(source, old_words, event)
        self.assertAlmostEqual(float(child0[0, 0].real), math.cos(math.pi / 4.0), places=15)
        occupied = np.asarray([0], dtype=np.int32)
        old = np.asarray([0], dtype=np.int32)
        child1 = heldout.child1_window(source, 2, occupied, old)
        self.assertAlmostEqual(float(child1[0, 0].imag), -math.sin(math.pi / 4.0), places=15)
        self.assertEqual(child1[0, 1], 0.0j)
        self.assertAlmostEqual(
            float(np.vdot(child0, child0).real + np.vdot(child1, child1).real),
            1.0,
            places=15,
        )

    def test_synthetic_l2_terminal_stream_matches_dense_state_norm(self) -> None:
        length = 2
        basis = heldout.physical.PrefixBasis(length)
        state, _blocked = heldout.physical.admit_prefix(basis, basis.blank(), 0)
        heldout.physical.evolve_state(basis, state, heldout.physical.ROUGH)
        source = DenseSource(state.blocks, prefix=1)
        cache = SyntheticCache(length)
        previous = heldout.legacy.CACHE
        heldout.legacy.CACHE = cache
        heldout.v3.LENGTH = length
        heldout.v3.EXECUTION_STARTED = time.perf_counter()
        try:
            result = heldout.terminal_witness(
                length, source, heldout.physical.ROUGH, cache, time.perf_counter()
            )
            dense_observed = 0.0
            dense_sham = 0.0
            event = length - 1
            edges = heldout.physical.hostile_edges(length)
            for q in range(length + 1):
                carrier = cache.carrier(q, edges)
                lineage_words = np.asarray(
                    heldout.physical.reverse_masks(length, q), dtype=np.uint32
                )
                dense = np.zeros(
                    (len(lineage_words), len(carrier.words)), dtype=np.complex128
                )
                if q < length:
                    old_words = np.asarray(
                        heldout.physical.reverse_masks(length - 1, q), dtype=np.uint32
                    )
                    child = heldout.child0_window(source.blocks[q], carrier.words, event)
                    final, _flux, _record = heldout.replay.low_memory_evolve_batch(
                        carrier, child, heldout.physical.ROUGH
                    )
                    dense[heldout._row_indices(length, q, old_words)] = final
                if q > 0:
                    old_words = np.asarray(
                        heldout.physical.reverse_masks(length - 1, q - 1), dtype=np.uint32
                    )
                    full_words = old_words | np.uint32(1 << event)
                    occupied, old = cache.admission(event, q)
                    child = heldout.child1_window(
                        source.blocks[q - 1], len(carrier.words), occupied, old
                    )
                    final, _flux, _record = heldout.replay.low_memory_evolve_batch(
                        carrier, child, heldout.physical.ROUGH
                    )
                    dense[heldout._row_indices(length, q, full_words)] = final
                probability = np.abs(dense) ** 2
                lineage_bits = np.asarray(
                    [[(int(word) >> site) & 1 for site in range(length)]
                     for word in lineage_words],
                    dtype=np.float64,
                )
                carrier_bits = np.asarray(
                    [[(int(word) >> site) & 1 for site in range(length)]
                     for word in carrier.words],
                    dtype=np.float64,
                )
                scores = (
                    (lineage_bits - float(q) / float(length)) @ carrier_bits.T
                    / float(length)
                )
                dense_observed += float(np.sum(probability * scores))
                weight = float(np.sum(probability))
                if weight:
                    lineage_marginal = np.sum(probability, axis=1)
                    carrier_marginal = np.sum(probability, axis=0)
                    dense_sham += float(np.sum(
                        np.sum(
                            lineage_marginal[:, None]
                            * (lineage_bits - float(q) / float(length)),
                            axis=0,
                        )
                        * np.sum(carrier_marginal[:, None] * carrier_bits, axis=0)
                    )) / (float(length) * weight)
        finally:
            heldout.legacy.CACHE = previous
            heldout.v3.EXECUTION_STARTED = None
        self.assertLess(float(result["normalization_residual"]), 1.0e-10)
        self.assertLess(float(result["total_content_residual"]), 1.0e-10)
        self.assertLess(float(result["row_column_disagreement"]), 1.0e-12)
        self.assertAlmostEqual(float(result["w_L"]), dense_observed, places=15)
        self.assertAlmostEqual(float(result["w_L_sham"]), dense_sham, places=15)
        self.assertAlmostEqual(float(result["D_L"]), dense_observed - dense_sham, places=15)

    def test_synthetic_row_rank_matches_reversed_basis(self) -> None:
        for length in (2, 3, 4):
            for q in range(length + 1):
                words = heldout.physical.reverse_masks(length, q)
                ranks = heldout._row_indices(length, q, words)
                self.assertTrue(np.array_equal(ranks, np.arange(len(words), dtype=np.int32)))

    def test_stable_shard_custody_rejects_extra_member_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory(dir=heldout.ROOT) as temporary:
            root = Path(temporary)
            relative = root.relative_to(heldout.ROOT)
            records = []
            for q, shape in ((0, (1, 1)), (1, (1, 4))):
                path = root / f"q_{q:02d}.c128"
                array = np.zeros(shape, dtype="<c16")
                path.write_bytes(array.tobytes())
                records.append({
                    "bytes": path.stat().st_size,
                    "path": (relative / path.name).as_posix(),
                    "q": q,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "shape": list(shape),
                })
            authority = {"terminal_shard_root": relative.as_posix(), "terminal_shards": records}
            custody = heldout.RetainedShardSet(2, authority)
            try:
                self.assertEqual(np.asarray(custody.open_shard(1)).shape, (1, 4))
                custody.reauthenticate()
            finally:
                custody.close()
            (root / "extra").write_bytes(b"x")
            with self.assertRaises(heldout.Refusal):
                heldout.RetainedShardSet(2, authority)
            (root / "extra").unlink()
            (root / "q_01.c128").unlink()
            os.symlink(root / "q_00.c128", root / "q_01.c128")
            with self.assertRaises((heldout.Refusal, OSError)):
                heldout.RetainedShardSet(2, authority)

    def test_simple_resource_preflight(self) -> None:
        with tempfile.TemporaryDirectory(dir=heldout.ROOT) as temporary:
            base = Path(temporary)
            scratch = base / "hostile-scratch"
            output = base / "hostile-output.json"
            telemetry_path = base / "telemetry.json"
            gate = heldout.strict_json(heldout.MACHINE_GATE)
            captured = int(time.time())
            telemetry = {
                "schema": gate["fresh_telemetry"]["schema"],
                "selected_schedule": "SEQUENTIAL_TARGET_THEN_HOSTILE",
                "captured_epoch_seconds": captured,
                "total_host_memory_bytes": 1,
                "available_memory_bytes": 1,
                "memory_pressure": "NORMAL",
                "shared_filesystem_free_bytes": gate["resource_gate"]["combined_scratch_minimum_bytes"],
                "target_scratch_root": str(base / "target-scratch"),
                "hostile_scratch_root": str(scratch),
                "target_output_path": str(base / "target-output.json"),
                "hostile_output_path": str(output),
            }
            telemetry_path.write_text(json.dumps(telemetry, sort_keys=True) + "\n")
            observed = heldout.resource_preflight(
                gate, telemetry_path, scratch, output, now=captured
            )
            self.assertGreaterEqual(observed["free_bytes"], heldout.HOSTILE_SCRATCH_MINIMUM)
            output.write_bytes(b"occupied")
            with self.assertRaises(heldout.Refusal):
                heldout.resource_preflight(
                    gate, telemetry_path, scratch, output, now=captured
                )

    def test_atomic_output_is_all_or_nothing_and_non_overwriting(self) -> None:
        with tempfile.TemporaryDirectory(dir=heldout.ROOT) as temporary:
            output = Path(temporary) / "result.json"
            payload = {"schema": "SYNTHETIC", "sizes": [2, 3]}
            expected = hashlib.sha256(heldout.canonical_bytes(payload)).hexdigest()
            self.assertEqual(heldout.atomic_publish(output, payload), expected)
            self.assertEqual(output.read_bytes(), heldout.canonical_bytes(payload))
            with self.assertRaises(heldout.Refusal):
                heldout.atomic_publish(output, payload)
            self.assertEqual(list(Path(temporary).glob("*.partial-*")), [])

    def test_source_schema_is_deterministic_and_nonphysical(self) -> None:
        first = json.dumps(heldout.synthetic_schema_record(), sort_keys=True, allow_nan=False)
        second = json.dumps(heldout.synthetic_schema_record(), sort_keys=True, allow_nan=False)
        self.assertEqual(first, second)
        self.assertIn("PHYSICAL_VALUES_UNOPENED", first)
        self.assertNotIn("D_10", first)
        self.assertNotIn("D_12", first)

    def test_source_imports_only_hostile_engine_modules(self) -> None:
        source = (HERE / "hostile_heldout_joint_witness.py").read_text()
        self.assertNotIn("import target", source)
        self.assertNotIn("heldout_target", source)
        self.assertNotIn("TARGET_RESULT", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
