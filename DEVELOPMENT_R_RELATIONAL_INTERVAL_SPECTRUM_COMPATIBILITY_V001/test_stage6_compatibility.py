#!/usr/bin/env python3
"""Non-physical contract and custody tests for the Stage 6 successor."""

from __future__ import annotations

import ast
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

import blind_adjudication_entrypoint as adjudication
import blind_contract_control as control
import blind_index_publisher as publisher
from contract_common import (
    ACCUMULATION_PROTOCOL_SHA256,
    FREEZE_SCHEMA,
    INDEX_SCHEMA,
    MANIFEST_SCHEMA,
    MANIFEST_STATUS,
    SIZES,
    atomic_owner_once_json,
    canonical_json,
    exact_atom_partition,
    sha256_file,
)


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
CONTROL = PACKET / "blind_contract_control.py"
FILES = (
    "blind_adjudication_entrypoint.py",
    "blind_contract_control.py",
    "blind_index_publisher.py",
    "blind_interval_worker.py",
    "contract_common.py",
    "METHODOLOGY.md",
    "test_stage6_compatibility.py",
)
DEPENDENCIES = {
    "independent_blind_engine": ROOT / "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001" / "independent_centerline.py",
    "independent_blind_method": ROOT / "AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001" / "METHODOLOGY.md",
    "public_interval_protocol": ROOT / "DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001" / "PROTOCOL.md",
    "public_accumulation_protocol": ROOT / "DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001" / "PROTOCOL.md",
    "sealed_low_spectra": ROOT / "DEVELOPMENT_R_GATE_C_HYDRO_CRITICALITY_PRESCREEN_V001" / "RESULT.json",
}


def run(*arguments: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(CONTROL), *(str(item) for item in arguments)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def write_json(path: Path, value: object, mode: int = 0o644) -> None:
    path.write_text(canonical_json(value), encoding="utf-8")
    path.chmod(mode)


def synthetic_row(length: int, charge: int) -> dict[str, object]:
    energy = -float(length)
    anchors = {
        10: (1.0191692872474647, 0.8893563670009239, 0.7891533299283149),
        12: (0.8522662221431041, 1.0784652119862503, 0.8251471862764426),
    }
    delta, chi, residue = anchors[length]
    ground = {
        "krylov_dimension": 16,
        "energy": energy,
        "residual_estimate": 0.0,
        "lowest_five_ritz_values": [energy, energy + 1, energy + 2, energy + 3, energy + 4],
    }
    response = {
        "krylov_dimension": 16,
        "lowest_five_ritz_values": [
            energy + delta,
            energy + delta + 1,
            energy + delta + 2,
            energy + delta + 3,
            energy + delta + 4,
        ],
        "Delta_act": delta,
        "chi_tau": chi,
        "R_low": residue,
        "active_ritz_index": 0,
        "active_residual_estimate": 0.0,
        "total_weight": 1.0,
        "weight_floor": 1.0e-12,
        "threshold_stable": True,
        "threshold_indices": [0, 0, 0],
        "resolved": True,
    }
    return {
        "L": length,
        "q": charge,
        "rho": charge / (2 * length),
        "sector_dimension": __import__("math").comb(2 * length, charge),
        "translation_orbits": 2,
        "ground_block_dimension": 2,
        "ground_block_nnz": 2,
        "response_block_dimension": 2,
        "response_block_nnz": 2,
        "ground_energy": energy,
        "ground_residual": 0.0,
        "ground_block_hermiticity_error": 0.0,
        "ground_krylov_orthogonality": 0.0,
        "response_full_norm_squared": 1.0,
        "response_projected_norm_squared": 1.0,
        "response_projection_error": 0.0,
        "active_actual_residual": 0.0,
        "Delta_act": delta,
        "chi_tau": chi,
        "R_low": residue,
        "response_block_hermiticity_error": 0.0,
        "response_krylov_orthogonality": 0.0,
        "ground_sequence": [ground],
        "response_sequence": [response],
        "response_convergence": {
            "Delta_act_relative": 0.0,
            "chi_tau_relative": 0.0,
            "R_low_relative": 0.0,
            "resolved": True,
            "exact_krylov_termination": True,
        },
        "threshold_stable": True,
        "ground_matvecs": 16,
        "response_matvecs": 16,
        "total_matvecs": 32,
        "wall_seconds": 0.0,
        "max_rss_bytes": 1,
        "memory_guards": [],
        "unresolved_reasons": [],
        "status": "RESOLVED",
    }


class Stage6CompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=PACKET)
        self.base = Path(self.temporary.name)
        self.histories: dict[str, object] = {}
        for length in SIZES:
            target = self.base / f"target_L{length}.json"
            blind = self.base / f"blind_L{length}.json"
            history = {"L": length, "synthetic_nonphysical_fixture": True}
            write_json(target, history)
            write_json(blind, history)
            audit = self.base / f"audit_L{length}.txt"
            audit.write_text(
                f"PASS synthetic nonphysical fixture\ntarget {sha256_file(target)}\nblind {sha256_file(blind)}\n",
                encoding="utf-8",
            )
            self.histories[str(length)] = {
                "target_history_path": target.relative_to(ROOT).as_posix(),
                "target_history_sha256": sha256_file(target),
                "blind_history_path": blind.relative_to(ROOT).as_posix(),
                "blind_history_sha256": sha256_file(blind),
                "hostile_audit_path": audit.relative_to(ROOT).as_posix(),
                "hostile_audit_sha256": sha256_file(audit),
                "hostile_verdict": "PASS",
            }
        self.atoms = exact_atom_partition(Fraction(1, 4), Fraction(251, 1000))
        stage2_auxiliary: dict[str, Path] = {}
        for label in ("control_audit", "l10_audit", "a18_cross_gate"):
            path = self.base / f"{label}.json"
            write_json(path, {"synthetic_nonphysical_fixture": label})
            stage2_auxiliary[label] = path
        stage2_paths = {
            "target_L4": self.base / "target_L4.json",
            "target_L6": self.base / "target_L6.json",
            "target_L8": self.base / "target_L8.json",
            "target_L10": self.base / "target_L10.json",
            "hostile_L10": self.base / "blind_L10.json",
            **stage2_auxiliary,
        }
        self.stage2_lineage = {
            "policy": (
                "AUDITED_SCALABLE_L4_L10_HISTORIES_BRIDGED_TO_CURRENT_STAGE2_AND_A18"
            ),
            "authorities": {
                label: {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": sha256_file(path),
                }
                for label, path in stage2_paths.items()
            },
            "chosen_history_comparisons": {
                label: {
                    "max_sector_weight_difference": 0.0,
                    "max_history_observable_difference": 0.0,
                }
                for label in ("4", "6", "8", "10", "hostile_L10")
            },
            "tolerance": 1.0e-8,
        }
        self.manifest = self.base / "MANIFEST.json"
        self.manifest_payload = {
            "schema": MANIFEST_SCHEMA,
            "status": MANIFEST_STATUS,
            "accumulation_protocol_sha256": ACCUMULATION_PROTOCOL_SHA256,
            "histories": self.histories,
            "stage2_benchmark_lineage": self.stage2_lineage,
            "I_acc": [[1, 4], [251, 1000]],
            "atoms": self.atoms,
        }
        write_json(self.manifest, self.manifest_payload)
        self.manifest_sha = sha256_file(self.manifest)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def produce_plan(self) -> Path:
        output = self.base / "SECTOR_PLAN.json"
        completed = run(
            "produce-plan",
            "--manifest", self.manifest,
            "--manifest-sha256", self.manifest_sha,
            "--output", output,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return output

    def source_freeze(self) -> Path:
        path = self.base / "SOURCE_FREEZE.json"
        payload = {
            "schema": "RELATIONAL_INTERVAL_BLIND_COMPATIBILITY_SOURCE_FREEZE_V001",
            "status": "CANDIDATE_SOURCES_FROZEN__NO_PHYSICAL_SPECTRUM_EXECUTED",
            "physical_spectrum_executed": False,
            "files": {name: sha256_file(PACKET / name) for name in FILES},
            "dependencies": {
                name: {
                    "path": dependency.relative_to(ROOT).as_posix(),
                    "sha256": sha256_file(dependency),
                }
                for name, dependency in DEPENDENCIES.items()
            },
        }
        write_json(path, payload, 0o444)
        return path

    def produce_freeze(self, plan: Path) -> Path:
        source = self.source_freeze()
        output = self.base / "BLIND_FREEZE.json"
        completed = run(
            "produce-freeze",
            "--manifest", self.manifest,
            "--manifest-sha256", self.manifest_sha,
            "--sector-plan", plan,
            "--sector-plan-sha256", sha256_file(plan),
            "--source-freeze", source,
            "--source-freeze-sha256", sha256_file(source),
            "--output", output,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return output

    def issue_credentials(
        self, freeze: Path, rows: Path,
    ) -> tuple[Path, dict[tuple[int, int], dict[str, object]]]:
        credentials = self.base / "CREDENTIALS"
        credentials.mkdir()
        bindings: dict[tuple[int, int], dict[str, object]] = {}
        for length, charge in ((10, 5), (12, 6)):
            physical_output = rows / f"SECTOR_L{length}_Q{charge}.json"
            credential = credentials / f"SECTOR_L{length}_Q{charge}.json"
            completed = run(
                "issue-credential",
                "--freeze", freeze,
                "--freeze-sha256", sha256_file(freeze),
                "--L", length,
                "--q", charge,
                "--physical-output", physical_output,
                "--output", credential,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            bindings[(length, charge)] = control.validate_execution_credential(
                credential, sha256_file(credential), length, charge,
                physical_output,
            )
        return credentials, bindings

    def test_01_exact_plan_cli(self) -> None:
        plan = self.produce_plan()
        payload = json.loads(plan.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], "BLIND_RELATIONAL_INTERVAL_SECTOR_PLAN_V001")
        self.assertEqual(payload["planned_sectors"], [[10, 5], [12, 6]])
        self.assertEqual(payload["atoms"], self.atoms)

    def test_02_plan_owner_once_no_clobber(self) -> None:
        plan = self.produce_plan()
        original = sha256_file(plan)
        stat = plan.stat()
        self.assertEqual(stat.st_mode & 0o777, 0o444)
        self.assertEqual(stat.st_nlink, 1)
        completed = run(
            "produce-plan", "--manifest", self.manifest,
            "--manifest-sha256", self.manifest_sha, "--output", plan,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(sha256_file(plan), original)

    def test_03_old_protocol_field_refused(self) -> None:
        altered = copy.deepcopy(self.manifest_payload)
        altered["scalable_accumulation_protocol_sha256"] = altered.pop(
            "accumulation_protocol_sha256"
        )
        path = self.base / "OLD_FIELD.json"
        output = self.base / "MUST_NOT_EXIST.json"
        write_json(path, altered)
        completed = run(
            "produce-plan", "--manifest", path,
            "--manifest-sha256", sha256_file(path), "--output", output,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertFalse(output.exists())

    def test_04_incomplete_atom_partition_refused(self) -> None:
        altered = copy.deepcopy(self.manifest_payload)
        altered["atoms"] = altered["atoms"][:-1]
        path = self.base / "INCOMPLETE_ATOMS.json"
        output = self.base / "MUST_NOT_EXIST.json"
        write_json(path, altered)
        completed = run(
            "produce-plan", "--manifest", path,
            "--manifest-sha256", sha256_file(path), "--output", output,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertFalse(output.exists())

    def test_05_freeze_matches_adjudicator_contract(self) -> None:
        freeze = self.produce_freeze(self.produce_plan())
        payload = json.loads(freeze.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], FREEZE_SCHEMA)
        self.assertEqual(payload["status"], "BLIND_METHOD_FROZEN_BEFORE_TARGET_SPECTRUM")
        self.assertEqual(payload["manifest_sha256"], self.manifest_sha)
        self.assertEqual(payload["planned_sectors"], [[10, 5], [12, 6]])
        self.assertIs(payload["target_code_or_matrices_imported"], False)
        self.assertEqual(freeze.stat().st_mode & 0o777, 0o444)
        self.assertEqual(freeze.stat().st_nlink, 1)

    def test_06_stale_source_freeze_refused(self) -> None:
        plan = self.produce_plan()
        source = self.source_freeze()
        payload = json.loads(source.read_text(encoding="utf-8"))
        source.chmod(0o644)
        payload["files"]["blind_interval_worker.py"] = "0" * 64
        write_json(source, payload)
        output = self.base / "MUST_NOT_EXIST.json"
        completed = run(
            "produce-freeze", "--manifest", self.manifest,
            "--manifest-sha256", self.manifest_sha,
            "--sector-plan", plan, "--sector-plan-sha256", sha256_file(plan),
            "--source-freeze", source,
            "--source-freeze-sha256", sha256_file(source), "--output", output,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertFalse(output.exists())

    def test_07_index_storage_contract(self) -> None:
        freeze = self.produce_freeze(self.produce_plan())
        rows = self.base / "ROWS"
        rows.mkdir()
        credentials, authorizations = self.issue_credentials(freeze, rows)
        for length, charge in ((10, 5), (12, 6)):
            row = synthetic_row(length, charge)
            row["execution_authorization"] = authorizations[(length, charge)]
            atomic_owner_once_json(
                ROOT, rows / f"SECTOR_L{length}_Q{charge}.json",
                row,
            )
        output = self.base / "SPECTRUM_INDEX.json"
        arguments = argparse_namespace(
            freeze=freeze,
            freeze_sha256=sha256_file(freeze),
            rows_dir=rows,
            credentials_dir=credentials,
            output=output,
        )
        publisher.publish(arguments)
        payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], INDEX_SCHEMA)
        self.assertEqual(payload["manifest_sha256"], self.manifest_sha)
        self.assertEqual(set(payload["rows"]), {"10:5", "12:6"})
        self.assertIn("method_freeze_path", payload)
        self.assertEqual(
            set(payload["execution_authorizations"]), {"10:5", "12:6"},
        )
        self.assertNotIn("pre_target_method_freeze_path", payload)
        self.assertTrue(all(set(value) == {"path", "sha256"} for value in payload["rows"].values()))

    def test_08_index_rejects_embedded_or_non_owner_row(self) -> None:
        freeze = self.produce_freeze(self.produce_plan())
        rows = self.base / "ROWS"
        rows.mkdir()
        credentials, authorizations = self.issue_credentials(freeze, rows)
        for length, charge in ((10, 5), (12, 6)):
            row = synthetic_row(length, charge)
            row["execution_authorization"] = authorizations[(length, charge)]
            write_json(rows / f"SECTOR_L{length}_Q{charge}.json", row, 0o644)
        with self.assertRaisesRegex(Exception, "owner-once custody"):
            publisher.publish(
                argparse_namespace(
                    freeze=freeze,
                    freeze_sha256=sha256_file(freeze),
                    rows_dir=rows,
                    credentials_dir=credentials,
                    output=self.base / "MUST_NOT_EXIST.json",
                )
            )

    def test_09_independent_classifier_shape(self) -> None:
        rows = [
            {"L": length, "Delta_act": 1 / length, "chi_tau": length, "R_low": 0.5}
            for length in SIZES
        ]
        result = publisher.classify(rows)
        required = {
            "checks", "passes", "classification", "chi_power_exponent_y",
            "fixed_z1_heldout_sse_relative", "gapless_heldout_sse_relative",
            "positive_gap_heldout_sse_relative", "L_times_Delta", "chi_over_L",
            "gap_power_fit", "fixed_z1_fit", "fixed_z1_heldout_rows",
            "gapless_heldout_rows", "positive_gap_heldout_rows",
            "tail_scaled_gap_relative_range", "tail_scaled_chi_relative_range",
            "tail_residue_relative_range", "rows",
        }
        self.assertEqual(set(result), required)
        self.assertTrue(result["passes"])

    def test_10_no_target_code_or_matrix_import(self) -> None:
        inspected = [
            PACKET / "blind_adjudication_entrypoint.py",
            PACKET / "blind_contract_control.py",
            PACKET / "blind_index_publisher.py",
            PACKET / "blind_interval_worker.py",
            PACKET / "contract_common.py",
        ]
        forbidden_modules = {
            "compute_phase_screen", "target_interval_worker",
            "interval_spectrum_driver", "compare_and_classify",
        }
        forbidden_matrix_terms = ("np.load", "numpy.load", ".npy", ".npz")
        for path in inspected:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[0])
            self.assertFalse(imported & forbidden_modules, path.name)
            self.assertTrue(all(term not in source for term in forbidden_matrix_terms), path.name)

    def test_11_worker_refuses_without_token_before_solver(self) -> None:
        output = self.base / "MUST_NOT_EXIST.json"
        completed = subprocess.run(
            [
                sys.executable, "-B", str(PACKET / "blind_interval_worker.py"),
                "--L", "10", "--q", "5", "--run-token", "WRONG",
                "--output", str(output),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(completed.returncode, 2)
        self.assertFalse(output.exists())
        self.assertIn("literal blind execution token absent", completed.stderr)

    def test_12_syntax_census(self) -> None:
        for name in FILES:
            path = PACKET / name
            if path.suffix == ".py":
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_13_source_dependency_census_and_bindings_refuse(self) -> None:
        plan = self.produce_plan()
        source = self.source_freeze()
        original = json.loads(source.read_text(encoding="utf-8"))
        mutations = {}
        missing = copy.deepcopy(original)
        missing["dependencies"].pop("sealed_low_spectra")
        mutations["missing"] = missing
        extra = copy.deepcopy(original)
        extra["dependencies"]["unregistered"] = copy.deepcopy(
            extra["dependencies"]["sealed_low_spectra"]
        )
        mutations["extra"] = extra
        swapped = copy.deepcopy(original)
        left = swapped["dependencies"]["independent_blind_engine"]
        right = swapped["dependencies"]["public_interval_protocol"]
        swapped["dependencies"]["independent_blind_engine"] = right
        swapped["dependencies"]["public_interval_protocol"] = left
        mutations["swapped"] = swapped
        wrong_path = copy.deepcopy(original)
        wrong_path["dependencies"]["sealed_low_spectra"]["path"] = (
            wrong_path["dependencies"]["public_interval_protocol"]["path"]
        )
        mutations["wrong_path"] = wrong_path
        wrong_hash = copy.deepcopy(original)
        wrong_hash["dependencies"]["sealed_low_spectra"]["sha256"] = "0" * 64
        mutations["wrong_hash"] = wrong_hash
        for label, payload in mutations.items():
            with self.subTest(label=label):
                altered = self.base / f"SOURCE_FREEZE_{label}.json"
                output = self.base / f"MUST_NOT_EXIST_{label}.json"
                write_json(altered, payload, 0o444)
                completed = run(
                    "produce-freeze", "--manifest", self.manifest,
                    "--manifest-sha256", self.manifest_sha,
                    "--sector-plan", plan,
                    "--sector-plan-sha256", sha256_file(plan),
                    "--source-freeze", altered,
                    "--source-freeze-sha256", sha256_file(altered),
                    "--output", output,
                )
                self.assertEqual(completed.returncode, 2, completed.stderr)
                self.assertFalse(os.path.lexists(output))

    def test_14_owner_once_refuses_symlink_destinations(self) -> None:
        for label, target_exists in (("broken", False), ("target_alias", True)):
            with self.subTest(label=label):
                target = self.base / f"{label}-target.json"
                if target_exists:
                    write_json(target, {"owner": "preexisting"}, 0o444)
                    original = sha256_file(target)
                output = self.base / f"{label}-output.json"
                output.symlink_to(target)
                with self.assertRaisesRegex(
                    Exception, "already exists or is aliased",
                ):
                    atomic_owner_once_json(ROOT, output, {"must": "refuse"})
                self.assertTrue(output.is_symlink())
                self.assertEqual(target.exists(), target_exists)
                if target_exists:
                    self.assertEqual(sha256_file(target), original)

    def test_15_owner_once_refuses_symlink_parent(self) -> None:
        actual_parent = self.base / "actual-parent"
        actual_parent.mkdir()
        aliased_parent = self.base / "aliased-parent"
        aliased_parent.symlink_to(actual_parent, target_is_directory=True)
        output = aliased_parent / "must-not-exist.json"
        with self.assertRaisesRegex(Exception, "parent is aliased or special"):
            atomic_owner_once_json(ROOT, output, {"must": "refuse"})
        self.assertFalse((actual_parent / output.name).exists())

    def test_16_publisher_refuses_cross_sector_row_authorization(self) -> None:
        freeze = self.produce_freeze(self.produce_plan())
        rows = self.base / "ROWS"
        rows.mkdir()
        credentials, authorizations = self.issue_credentials(freeze, rows)
        for length, charge in ((10, 5), (12, 6)):
            row = synthetic_row(length, charge)
            wrong_pair = (12, 6) if length == 10 else (10, 5)
            row["execution_authorization"] = authorizations[wrong_pair]
            atomic_owner_once_json(
                ROOT, rows / f"SECTOR_L{length}_Q{charge}.json", row,
            )
        with self.assertRaisesRegex(Exception, "execution authorization mismatch"):
            publisher.publish(
                argparse_namespace(
                    freeze=freeze,
                    freeze_sha256=sha256_file(freeze),
                    rows_dir=rows,
                    credentials_dir=credentials,
                    output=self.base / "MUST_NOT_EXIST.json",
                )
            )

    def test_17_publisher_refuses_substituted_credential_authority(self) -> None:
        freeze = self.produce_freeze(self.produce_plan())
        rows = self.base / "ROWS"
        rows.mkdir()
        credentials, authorizations = self.issue_credentials(freeze, rows)
        for length, charge in ((10, 5), (12, 6)):
            row = synthetic_row(length, charge)
            row["execution_authorization"] = authorizations[(length, charge)]
            atomic_owner_once_json(
                ROOT, rows / f"SECTOR_L{length}_Q{charge}.json", row,
            )
        substituted = credentials / "SECTOR_L10_Q5.json"
        payload = json.loads(substituted.read_text(encoding="utf-8"))
        substituted.chmod(0o644)
        payload["authorities"]["blind_worker"]["sha256"] = "0" * 64
        write_json(substituted, payload, 0o444)
        with self.assertRaisesRegex(Exception, "blind credential blind_worker"):
            publisher.publish(
                argparse_namespace(
                    freeze=freeze,
                    freeze_sha256=sha256_file(freeze),
                    rows_dir=rows,
                    credentials_dir=credentials,
                    output=self.base / "MUST_NOT_EXIST.json",
                )
            )

    def test_18_adjudication_refuses_substituted_row_path(self) -> None:
        freeze = self.produce_freeze(self.produce_plan())
        rows = self.base / "ROWS"
        rows.mkdir()
        credentials, authorizations = self.issue_credentials(freeze, rows)
        for length, charge in ((10, 5), (12, 6)):
            row = synthetic_row(length, charge)
            row["execution_authorization"] = authorizations[(length, charge)]
            atomic_owner_once_json(
                ROOT, rows / f"SECTOR_L{length}_Q{charge}.json", row,
            )
        index = self.base / "SPECTRUM_INDEX.json"
        publisher.publish(
            argparse_namespace(
                freeze=freeze,
                freeze_sha256=sha256_file(freeze),
                rows_dir=rows,
                credentials_dir=credentials,
                output=index,
            )
        )
        publisher.validate_execution_bound_index(
            index, sha256_file(index), self.manifest_sha,
        )
        arbitrary_row = synthetic_row(10, 5)
        arbitrary_row["execution_authorization"] = authorizations[(10, 5)]
        arbitrary_row["Delta_act"] *= 0.99
        substituted_row = self.base / "ARBITRARY_SUBSTITUTED_L10_Q5.json"
        atomic_owner_once_json(ROOT, substituted_row, arbitrary_row)
        altered = json.loads(index.read_text(encoding="utf-8"))
        altered["rows"]["10:5"] = {
            "path": substituted_row.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(substituted_row),
        }
        altered_index = self.base / "ALTERED_INDEX.json"
        write_json(altered_index, altered, 0o444)
        with self.assertRaisesRegex(Exception, "output binding mismatch"):
            publisher.validate_execution_bound_index(
                altered_index, sha256_file(altered_index), self.manifest_sha,
            )
        with mock.patch.object(adjudication.subprocess, "run") as launched:
            with self.assertRaisesRegex(Exception, "output binding mismatch"):
                adjudication.adjudicate(
                    argparse_namespace(
                        manifest=self.manifest,
                        manifest_sha256=self.manifest_sha,
                        target_index=self.base / "UNUSED_TARGET_INDEX.json",
                        target_index_sha256="0" * 64,
                        blind_index=altered_index,
                        blind_index_sha256=sha256_file(altered_index),
                        output=self.base / "MUST_NOT_EXIST.json",
                    )
                )
            launched.assert_not_called()


def argparse_namespace(**values: object):
    return type("Arguments", (), values)()


if __name__ == "__main__":
    unittest.main(verbosity=2)
