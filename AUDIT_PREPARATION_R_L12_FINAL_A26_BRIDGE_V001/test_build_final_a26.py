#!/usr/bin/env python3
"""Positive, adverse, and owner-once tests for the live A26 bridge."""

from __future__ import annotations

import copy
import hashlib
import math
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRODUCTION = (
    ROOT / "AUDIT_PREPARATION_R_L12_PRODUCTION_DAG_REFINEMENT_V001"
)
for path in (HERE, PRODUCTION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import build_final_a26 as bridge  # noqa: E402
import independent_final_auditor as auditor  # noqa: E402
from synthetic_upstream_authority_fixtures import fixture  # noqa: E402


auditor._install_synthetic_upstream_fixture(fixture)
auditor._positive_fixture_bundle_cached.cache_clear()


class FinalA26BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = auditor.positive_fixture_bundle()

    def candidate(self) -> dict[str, object]:
        expected = self.bundle["A26_FINAL_L12_AUDIT"]
        return bridge.construct_a26_record(
            self.bundle["A24_TARGET_L12_HISTORY"],
            self.bundle["A25_HOSTILE_L12_HISTORY"],
            copy.deepcopy(expected["authority_bindings"]),
            terminal_errors=[
                row["linf_abs_error"]
                for row in expected["terminal_comparisons"]
            ],
            projection_errors=(0.0, 0.0),
        )

    def test_positive_candidate_is_exact_119_of_119(self) -> None:
        candidate = self.candidate()
        accepted = auditor.validate_final_l12_audit(
            candidate, fixture_mode=True,
        )
        self.assertEqual(accepted["checks_total"], 119)
        self.assertEqual(accepted["checks_passed"], 119)
        self.assertEqual(len(accepted["authority_bindings"]), 42)

    def test_adverse_terminal_error_is_refused(self) -> None:
        candidate = self.candidate()
        candidate["terminal_comparisons"][6]["linf_abs_error"] = 2.0e-8
        with self.assertRaisesRegex(
            auditor.Refusal, "terminal comparison tolerance exceeded",
        ):
            auditor.validate_final_l12_audit(candidate, fixture_mode=True)

    def test_owner_once_authority_census_refuses_duplicate(self) -> None:
        candidate = self.candidate()
        candidate["authority_bindings"][-1] = copy.deepcopy(
            candidate["authority_bindings"][-2]
        )
        with self.assertRaisesRegex(
            auditor.Refusal, "authority binding instance/path alias",
        ):
            auditor.validate_final_l12_audit(candidate, fixture_mode=True)

    def test_builder_has_no_test_fixture_import(self) -> None:
        source = Path(bridge.__file__).read_text()
        self.assertNotIn("synthetic_upstream_authority_fixtures", source)
        self.assertNotIn("positive_fixture", source)

    def test_permutation_hash_matches_independent_auditor(self) -> None:
        for width, charges in ((11, range(12)), (24, range(12))):
            for charge in charges:
                self.assertEqual(
                    bridge.basis_permutation_sha256(width, charge),
                    auditor.basis_permutation_sha256(width, charge),
                )

    def test_wrong_permutation_hash_is_refused_by_independent_sink(self) -> None:
        candidate = self.candidate()
        candidate["terminal_comparisons"][5][
            "carrier_target_to_hostile_permutation_sha256"
        ] = "a" * 63 + "b"
        with self.assertRaisesRegex(auditor.Refusal, "basis permutation hash"):
            auditor.validate_final_l12_audit(candidate, fixture_mode=True)

    def test_live_row_projection_agrees_and_detects_mutation(self) -> None:
        target = copy.deepcopy(self.bundle["A24_TARGET_L12_HISTORY"])
        hostile = copy.deepcopy(self.bundle["A25_HOSTILE_L12_HISTORY"])
        self.assertEqual(
            bridge.history_projection_errors(target, hostile),
            auditor._history_projection_errors(
                target, hostile, "A26_FINAL_L12_AUDIT",
            ),
        )
        hostile["rows"][0]["W_n"] += 2.0e-8
        first = bridge.history_projection_errors(target, hostile)
        second = auditor._history_projection_errors(
            target, hostile, "A26_FINAL_L12_AUDIT",
        )
        self.assertEqual(first, second)
        self.assertGreater(first[0], auditor.TOLERANCE)

    @staticmethod
    def _terminal_pair(
        directory: Path, charge: int, delta: float,
    ) -> tuple[dict[str, object], dict[str, object]]:
        shape = (math.comb(11, charge), math.comb(24, charge))
        target = bridge.np.fromfunction(
            lambda row, column: (
                (row + 1.0) / 31.0 + 1j * (column + 1.0) / 37.0
            ),
            shape, dtype=float,
        ).astype("<c16")
        hostile = bridge.np.zeros(shape, dtype="<c16")
        lineage = bridge.basis_permutation(11, charge)
        carrier = bridge.basis_permutation(24, charge)
        for target_row in range(shape[0]):
            hostile[int(lineage[target_row]), carrier] = target[target_row]
        hostile[int(lineage[0]), int(carrier[0])] += delta
        target_path = directory / f"target_q{charge:02d}.npy"
        hostile_path = directory / f"hostile_q{charge:02d}.c128"
        bridge.np.save(target_path, target, allow_pickle=False)
        hostile.tofile(hostile_path)
        target_path.chmod(0o444)
        hostile_path.chmod(0o444)
        target_binding = {
            "path": str(target_path),
            "sha256": hashlib.sha256(target_path.read_bytes()).hexdigest(),
            "shape": list(shape),
            "bytes": target_path.stat().st_size,
        }
        hostile_binding = {
            "path": str(hostile_path),
            "sha256": hashlib.sha256(hostile_path.read_bytes()).hexdigest(),
            "shape": list(shape),
            "bytes": hostile_path.stat().st_size,
        }
        return target_binding, hostile_binding

    def test_live_terminal_dual_implementations_agree_and_detect_amplitude(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".a26-terminal-", dir=HERE) as raw:
            directory = Path(raw).resolve()
            for delta in (0.0, 2.0e-8):
                target, hostile = self._terminal_pair(directory, 1, delta)
                first = bridge.terminal_linf(target, hostile, 1)
                second = auditor._compare_terminal_files(target, hostile, 1)
                self.assertEqual(first, second)
                self.assertAlmostEqual(first, abs(delta), places=15)
                if delta:
                    self.assertGreater(first, auditor.TOLERANCE)
                for binding in (target, hostile):
                    Path(binding["path"]).unlink()

    def test_retained_raw_json_refuses_writable_and_path_swap(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".a26-json-", dir=HERE) as raw:
            directory = Path(raw).resolve()
            path = directory / "A23.json"
            payload = bridge._canonical_json_bytes_local({"exact": True})
            path.write_bytes(payload)
            digest = hashlib.sha256(payload).hexdigest()
            with self.assertRaisesRegex(bridge.BridgeRefusal, "writable"):
                bridge.RetainedInput.open(path, digest, "writable A23")
            path.chmod(0o444)
            record, retained = bridge.open_canonical_record(path, digest, "A23")
            self.assertEqual(record, {"exact": True})
            aside = directory / "held.json"
            path.replace(aside)
            path.write_bytes(payload)
            path.chmod(0o444)
            try:
                with self.assertRaisesRegex(
                    bridge.BridgeRefusal, "retained input changed",
                ):
                    retained.verify()
            finally:
                retained.close()

    def test_temporary_owner_once_publication_is_no_clobber(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".a26-publish-", dir=HERE) as raw:
            output = Path(raw).resolve() / "A26.json"
            payload = bridge._canonical_json_bytes_local({"A26": "fixture"})
            digest = bridge.evidence._atomic_publish_once(
                str(output), payload, str(output),
            )
            metadata = os.stat(output, follow_symlinks=False)
            self.assertEqual(digest, hashlib.sha256(payload).hexdigest())
            self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o444)
            self.assertEqual(metadata.st_nlink, 1)
            with self.assertRaises(bridge.evidence.OrchestrationRefusal):
                bridge.evidence._atomic_publish_once(
                    str(output), b'{"changed":true}\n', str(output),
                )
            self.assertEqual(output.read_bytes(), payload)

    def test_authenticated_source_closure_remains_frozen(self) -> None:
        bridge.verify_frozen_source_closure()
        self.assertEqual(len(bridge._SOURCE_GUARD), 5)
        for retained in bridge._SOURCE_GUARD:
            metadata = os.fstat(retained.descriptor)
            self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o444)
            self.assertEqual(metadata.st_nlink, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
