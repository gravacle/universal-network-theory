#!/usr/bin/env python3
"""Synthetic-only tests for the blind independent scaling audit."""

from __future__ import annotations

import hashlib
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import independent_scaling_audit as audit  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def descriptor(root: Path, path: Path, provenance: str | None = None) -> dict[str, object]:
    return {
        "path": provenance or path.relative_to(root).as_posix(),
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size,
    }


def random_unitary(rng: np.random.Generator, dimension: int) -> np.ndarray:
    if dimension == 1:
        return np.ones((1, 1), dtype=np.complex128)
    raw = rng.normal(size=(dimension, dimension)) + 1.0j * rng.normal(
        size=(dimension, dimension)
    )
    q_basis, r_factor = np.linalg.qr(raw)
    phases = np.diag(r_factor)
    phases = np.where(np.abs(phases) > 0.0, phases / np.abs(phases), 1.0)
    return q_basis * phases.conj()[None, :]


def synthetic_checkpoint(length: int, seed: int = 927) -> dict[int, np.ndarray]:
    rng = np.random.default_rng(seed)
    blocks: dict[int, np.ndarray] = {}
    norm = 0.0
    for q in range(length + 1):
        shape = (math.comb(length, q), math.comb(2 * length, q))
        matrix = rng.normal(size=shape) + 1.0j * rng.normal(size=shape)
        # Make the example non-generic enough to exercise rank compression too.
        if q == length // 2 and min(shape) > 1:
            matrix[-1] = matrix[0] - 0.25j * matrix[1]
        blocks[q] = np.asarray(matrix, dtype=np.complex128)
        norm += float(np.vdot(matrix, matrix).real)
    scale = math.sqrt(norm)
    return {q: matrix / scale for q, matrix in blocks.items()}


def explicit_joint_difference(
    checkpoint: dict[int, np.ndarray], length: int
) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    states: list[tuple[int, int, int]] = []
    slices: dict[int, slice] = {}
    cursor = 0
    for q in range(length + 1):
        lineage = audit.fixed_weight_words(length, q)
        carrier = audit.fixed_weight_words(2 * length, q)
        start = cursor
        for s_word in lineage:
            for c_word in carrier:
                states.append((q, int(s_word), int(c_word)))
                cursor += 1
        slices[q] = slice(start, cursor)
    actual = np.zeros((cursor, cursor), dtype=np.complex128)
    product = np.zeros_like(actual)
    for q in range(length + 1):
        matrix = checkpoint[q]
        flat = matrix.reshape(-1)
        block_slice = slices[q]
        actual[block_slice, block_slice] = np.outer(flat, flat.conj())
        p_q = float(np.vdot(flat, flat).real)
        if p_q > 0.0:
            rho_s = matrix @ matrix.conj().T
            rho_c = matrix.T @ matrix.conj()
            product[block_slice, block_slice] = np.kron(rho_s, rho_c) / p_q
    return actual - product, states


def explicit_revisit_unitary(
    states: list[tuple[int, int, int]], length: int, event: int
) -> np.ndarray:
    positions = {state: index for index, state in enumerate(states)}
    unitary = np.eye(len(states), dtype=np.complex128)
    bit = 1 << event
    cosine = math.cos(audit.ANGLE)
    sine = math.sin(audit.ANGLE)
    for source, (q, lineage, carrier) in enumerate(states):
        if (lineage & bit) or (carrier & bit) or q >= length:
            continue
        target_state = (q + 1, lineage | bit, carrier | bit)
        target = positions[target_state]
        unitary[source, source] = cosine
        unitary[target, target] = cosine
        unitary[source, target] = -1.0j * sine
        unitary[target, source] = -1.0j * sine
    return unitary


def explicit_carrier_reduction(
    density: np.ndarray,
    states: list[tuple[int, int, int]],
    length: int,
) -> tuple[np.ndarray, list[tuple[int, int]], dict[int, slice]]:
    carrier_basis: list[tuple[int, int]] = []
    slices: dict[int, slice] = {}
    cursor = 0
    for q in range(length + 1):
        start = cursor
        for word in audit.fixed_weight_words(2 * length, q):
            carrier_basis.append((q, int(word)))
            cursor += 1
        slices[q] = slice(start, cursor)
    carrier_position = {item: index for index, item in enumerate(carrier_basis)}
    reduced = np.zeros((cursor, cursor), dtype=np.complex128)
    lineage_groups: dict[int, list[int]] = {}
    for index, (_, lineage, _) in enumerate(states):
        lineage_groups.setdefault(lineage, []).append(index)
    for indices in lineage_groups.values():
        for first in indices:
            q_first, _, carrier_first = states[first]
            row = carrier_position[(q_first, carrier_first)]
            for second in indices:
                q_second, _, carrier_second = states[second]
                column = carrier_position[(q_second, carrier_second)]
                reduced[row, column] += density[first, second]
    return reduced, carrier_basis, slices


def signed_blocks_dense_global(
    blocks: dict[int, audit.SignedCarrierBlock], length: int
) -> tuple[np.ndarray, dict[int, slice]]:
    sizes = [math.comb(2 * length, q) for q in range(length + 1)]
    total = sum(sizes)
    dense = np.zeros((total, total), dtype=np.complex128)
    slices: dict[int, slice] = {}
    cursor = 0
    for q, size in enumerate(sizes):
        block_slice = slice(cursor, cursor + size)
        slices[q] = block_slice
        dense[block_slice, block_slice] = blocks[q].dense()
        cursor += size
    return dense, slices


def explicit_observables(
    density: np.ndarray, length: int, slices: dict[int, slice]
) -> dict[str, object]:
    hermitian = 0.5 * (density + density.conj().T)
    diagonal = np.real(np.diag(hermitian))
    delta_n = np.zeros(2 * length)
    cursor = 0
    sector_traces = []
    for q in range(length + 1):
        words = audit.fixed_weight_words(2 * length, q)
        local = diagonal[cursor:cursor + len(words)]
        sector_traces.append(float(np.sum(local)))
        for site in range(2 * length):
            delta_n[site] += float(np.sum(local[((words >> site) & 1) != 0]))
        cursor += len(words)
    return {
        "carrier_trace_distance": 0.5 * float(np.sum(np.abs(np.linalg.eigvalsh(hermitian)))),
        "carrier_configuration_tv": 0.5 * float(np.sum(np.abs(diagonal))),
        "carrier_number_sector_tv": 0.5 * float(np.sum(np.abs(sector_traces))),
        "occupation_rms": float(np.sqrt(np.mean(delta_n * delta_n))),
        "delta_n": delta_n,
        "signed_trace": float(np.trace(hermitian).real),
    }


class CompactAlgebraTests(unittest.TestCase):
    def test_signed_svd_revisit_matches_explicit_density_and_transport(self) -> None:
        length = 3
        event = 1
        checkpoint = synthetic_checkpoint(length)
        blocks, diagnostics = audit.build_revisit_signed_blocks(checkpoint, length, event)
        joint, states = explicit_joint_difference(checkpoint, length)
        revisit = explicit_revisit_unitary(states, length, event)
        evolved = revisit @ joint @ revisit.conj().T
        explicit, _, slices = explicit_carrier_reduction(evolved, states, length)
        compact, compact_slices = signed_blocks_dense_global(blocks, length)
        self.assertEqual(slices, compact_slices)
        self.assertLess(float(np.max(np.abs(explicit - compact))), 2.0e-12)
        self.assertLess(abs(float(diagnostics["checkpoint_norm"]) - 1.0), 2.0e-13)
        self.assertLess(abs(float(diagnostics["signed_trace_after_admission"])), 2.0e-12)
        self.assertLess(
            float(diagnostics["maximum_checkpoint_svd_reconstruction_frobenius"]),
            2.0e-13,
        )

        observed = audit.summarize_observables(blocks, length)
        expected = explicit_observables(explicit, length, slices)
        for key in (
            "carrier_trace_distance",
            "carrier_configuration_tv",
            "carrier_number_sector_tv",
            "occupation_rms",
            "signed_trace",
        ):
            self.assertAlmostEqual(float(observed[key]), float(expected[key]), places=11)
        np.testing.assert_allclose(observed["delta_n"], expected["delta_n"], atol=2.0e-12)

        rng = np.random.default_rng(55)
        unitaries = {
            q: random_unitary(rng, math.comb(2 * length, q))
            for q in range(length + 1)
        }
        transported, residual = audit.apply_carrier_unitaries(blocks, unitaries)
        self.assertLess(residual, 2.0e-14)
        global_transport = np.zeros_like(explicit)
        for q, block_slice in slices.items():
            global_transport[block_slice, block_slice] = unitaries[q]
        explicit_after = global_transport @ explicit @ global_transport.conj().T
        compact_after, _ = signed_blocks_dense_global(transported, length)
        self.assertLess(float(np.max(np.abs(explicit_after - compact_after))), 3.0e-12)
        after = audit.summarize_observables(transported, length)
        self.assertAlmostEqual(
            float(after["carrier_trace_distance"]),
            float(observed["carrier_trace_distance"]),
            places=11,
        )

    def test_rank_one_matched_product_has_no_false_signal(self) -> None:
        length = 3
        rng = np.random.default_rng(81)
        checkpoint = {
            q: np.zeros((math.comb(length, q), math.comb(2 * length, q)), dtype=np.complex128)
            for q in range(length + 1)
        }
        q = 1
        left = rng.normal(size=math.comb(length, q)) + 1.0j * rng.normal(
            size=math.comb(length, q)
        )
        right = rng.normal(size=math.comb(2 * length, q)) + 1.0j * rng.normal(
            size=math.comb(2 * length, q)
        )
        matrix = np.outer(left, right)
        checkpoint[q] = matrix / np.linalg.norm(matrix)
        blocks, diagnostics = audit.build_revisit_signed_blocks(checkpoint, length, 0)
        observed = audit.summarize_observables(blocks, length)
        self.assertLess(float(observed["carrier_trace_distance"]), 2.0e-12)
        self.assertLess(abs(float(observed["signed_trace"])), 2.0e-12)
        self.assertEqual(diagnostics["checkpoint_schmidt_ranks"][str(q)], 1)

    def test_nonunitary_transport_is_refused(self) -> None:
        checkpoint = synthetic_checkpoint(2, seed=17)
        blocks, _ = audit.build_revisit_signed_blocks(checkpoint, 2, 0)
        unitaries = {
            q: np.eye(math.comb(4, q), dtype=np.complex128) for q in range(3)
        }
        unitaries[1][0, 0] = 2.0
        with self.assertRaises(audit.AuditFailure):
            audit.apply_carrier_unitaries(blocks, unitaries)


class CustodyTests(unittest.TestCase):
    def _make_census(self, root: Path) -> tuple[dict[str, object], dict[str, object]]:
        history = {
            "schema": "INDEPENDENT_PREFIX_LINEAGE_HISTORY_CONTROL_V002",
            "L": 4,
            "implementation_sha256": audit.PINNED_HOSTILE_V002[
                "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py"
            ],
            "methodology_sha256": audit.PINNED_HOSTILE_V002[
                "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/V002_LOW_MEMORY_SUPPLEMENT.md"
            ],
            "claim_boundary": "INDEPENDENT_FINITE_PREFIX_HISTORY_V002_CONTROL_ONLY",
            "comparison": {"resolved": True},
        }
        history_path = root / "history.json"
        history_path.write_bytes(audit.canonical_json_bytes(history))
        history_entry = descriptor(root, history_path)

        shard_entries = []
        shard_dir = root / "shards"
        shard_dir.mkdir()
        rng = np.random.default_rng(9)
        for q in range(4):
            array = rng.normal(size=(math.comb(3, q), math.comb(8, q))).astype(np.float64)
            array = np.asarray(array + 1.0j * (0.5 * array), dtype=np.complex128)
            path = shard_dir / f"q_{q:02d}.npy"
            with path.open("wb") as stream:
                np.save(stream, array, allow_pickle=False)
            provenance = (
                f"/legacy/audited/shards/{path.name}" if q == 0 else path.relative_to(root).as_posix()
            )
            entry = descriptor(root, path, provenance)
            entry.update({"q": q, "shape": list(array.shape), "dtype": array.dtype.str})
            shard_entries.append(entry)
        census = {
            "schema": "AUDIT_LINEAGE_RESPONSE_PRETERMINAL_SHARD_CENSUS_V001",
            "L": 4,
            "prefix": 3,
            "accuracy": "sharp",
            "engine_sha256": audit.PINNED_HOSTILE_V002[
                "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py"
            ],
            "history": history_entry,
            "shards": shard_entries,
        }
        census_path = root / "census.json"
        census_path.write_bytes(audit.canonical_json_bytes(census))
        return census, descriptor(root, census_path)

    def test_shard_history_authentication_and_exact_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            census, census_entry = self._make_census(root)
            observed, arrays = audit.load_authenticated_shard_census(
                root, census_entry, legacy_roots=(Path("/legacy/audited"),)
            )
            self.assertEqual(observed["schema"], census["schema"])
            self.assertEqual([array.shape for array in arrays], [
                (math.comb(3, q), math.comb(8, q)) for q in range(4)
            ])

            corrupt = root / "shards/q_02.npy"
            payload = bytearray(corrupt.read_bytes())
            payload[-1] ^= 1
            corrupt.write_bytes(bytes(payload))
            with self.assertRaises(audit.AuditFailure):
                audit.load_authenticated_shard_census(
                    root, census_entry, legacy_roots=(Path("/legacy/audited"),)
                )

    def test_unknown_roots_traversal_symlinks_and_target_lane_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            safe = root / "safe.json"
            safe.write_text("{}\n")
            with self.assertRaises(audit.AuditFailure):
                audit.resolve_custody_path(root, "../safe.json", legacy_roots=())
            with self.assertRaises(audit.AuditFailure):
                audit.resolve_custody_path(root, "/unknown/root/safe.json", legacy_roots=())
            with self.assertRaises(audit.AuditFailure):
                audit.resolve_custody_path(
                    root,
                    f"{audit.FORBIDDEN_TARGET_COMPONENT}/result.json",
                    legacy_roots=(),
                )
            link = root / "link.json"
            link.symlink_to(safe)
            with self.assertRaises(audit.AuditFailure):
                audit.resolve_custody_path(root, "link.json", legacy_roots=())

    def test_checkpoint_identity_and_receipt_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            census, _ = self._make_census(root)
            freeze_hash = "a" * 64
            stage = "PRETERMINAL_SHARP"
            identity = audit.checkpoint_identity(census, freeze_hash, stage)
            receipt = {
                "schema": "AUDIT_LINEAGE_RESPONSE_CHECKPOINT_RECEIPT_V001",
                "stage": stage,
                "checkpoint_identity_sha256": identity,
                "complete": True,
                "unblinded_to_target": False,
            }
            audit.verify_checkpoint_receipt(receipt, census, freeze_hash)
            changed = json.loads(json.dumps(census))
            changed["shards"][0]["sha256"] = "b" * 64
            with self.assertRaises(audit.AuditFailure):
                audit.verify_checkpoint_receipt(receipt, changed, freeze_hash)
            bad_receipt = dict(receipt, unblinded_to_target=True)
            with self.assertRaises(audit.AuditFailure):
                audit.verify_checkpoint_receipt(bad_receipt, census, freeze_hash)

    def test_atomic_create_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "custody.json"
            digest = audit.atomic_create(path, b"{\"status\":\"synthetic\"}\n")
            self.assertEqual(digest, sha256(path))
            with self.assertRaises(audit.AuditFailure):
                audit.atomic_create(path, b"replacement\n")

    def test_strict_json_rejects_nan_and_duplicate_keys(self) -> None:
        with self.assertRaises(audit.AuditFailure):
            audit.strict_json_bytes(b'{"x":NaN}\n', "nan")
        with self.assertRaises(audit.AuditFailure):
            audit.strict_json_bytes(b'{"x":1,"x":2}\n', "duplicate")

    def test_pinned_census_and_safe_module_load(self) -> None:
        observed = audit.authenticate_pinned_inputs(ROOT)
        self.assertEqual(
            observed[
                "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/independent_prefix_history_v002.py"
            ],
            "e6b1be915a4d490939799e79efc017ab4e3808f1beeb3d984448b2508fb0522b",
        )
        modules = audit.load_pinned_hostile_v002(ROOT)
        self.assertIs(modules.wrapper.base, modules.base)
        self.assertEqual(modules.base.SHARP.label, "sharp")


if __name__ == "__main__":
    unittest.main(verbosity=2)
