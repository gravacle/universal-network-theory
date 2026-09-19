#!/usr/bin/env python3

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "aws"))

from durable_evidence import EvidenceError, canonical_json_bytes, sha256_bytes, sha256_file
from package_source import build_file_set, safe_archive_path
from stack_parameters import build_parameters
from verify_bundle import verify_files


def project_path(path):
    return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()


def binding_record(source, archive):
    return {
        "source_path": project_path(source),
        "archive_path": archive,
        "sha256": sha256_file(source),
    }


def synthetic_bindings():
    kernel = ROOT / "tests" / "fixture_kernel.py"
    dependency = ROOT / "tests" / "fixture_process.py"
    regression = ROOT / "L4_L12_EXACT_REGRESSION_LINUX_X86_64.json"
    readme = ROOT / "README.md"
    return {
        "schema": "L14_EXACT_KERNEL_BINDINGS_V002",
        "status": "BOUND_AND_REGRESSION_AUTHENTICATED",
        "target": {
            "status": "BOUND",
            "module_path": project_path(kernel),
            "module_archive_path": "kernel/target_exact_kernel.py",
            "sha256": sha256_file(kernel),
            "bundle_files": [binding_record(dependency, "kernel_support/target_dependency.py")],
        },
        "hostile": {
            "status": "BOUND",
            "module_path": project_path(kernel),
            "module_archive_path": "kernel/hostile_exact_kernel.py",
            "sha256": sha256_file(kernel),
            "bundle_files": [binding_record(dependency, "kernel_support/hostile_dependency.py")],
        },
        "runtime": {
            "status": "BOUND_AND_REGRESSION_AUTHENTICATED",
            "platform": "manylinux_x86_64",
            "python_version": "3.9.0",
            "numpy_version": "2.0.2",
            "mpmath_version": "1.3.0",
            "requirements_archive_path": "runtime/requirements.lock",
            "wheelhouse_archive_path": "runtime/wheelhouse",
            "python_archive_path": "runtime/python/cpython-test.tar.gz",
            "bundle_files": [
                binding_record(readme, "runtime/requirements.lock"),
                binding_record(readme, "runtime/wheelhouse/numpy-test.whl"),
                binding_record(readme, "runtime/python/cpython-test.tar.gz"),
            ],
        },
        "frozen_runtime": {
            "status": "BOUND",
            "bundle_files": [
                binding_record(
                    readme,
                    "frozen/audited-386ee2c/DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/"
                    "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json",
                ),
                binding_record(
                    readme,
                    "frozen/audited-386ee2c/DEVELOPMENT_R_GATE_C_EXTENDED_PHASE_SCREEN_V001/PROTOCOL.md",
                ),
                binding_record(
                    readme,
                    "frozen/audited-386ee2c/AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/METHODOLOGY.md",
                ),
                binding_record(
                    readme,
                    "frozen/audited-386ee2c/AUDIT_R_GATE_C_EXTENDED_CENTERLINE_V001/POST_OUTPUT_METHOD.md",
                ),
                binding_record(
                    readme,
                    "frozen/audited-386ee2c/DEVELOPMENT_R_SCALABLE_RELATIONAL_ACCUMULATION_V001/PROTOCOL.md",
                ),
                binding_record(
                    readme,
                    "frozen/audited-386ee2c/DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/PROTOCOL.md",
                ),
            ],
        },
        "regression": {
            "status": "PASS",
            "report_path": project_path(regression),
            "sha256": sha256_file(regression),
        },
    }


class PackagingTests(unittest.TestCase):
    def test_bundle_contract_includes_runtime_kernel_dependencies_and_regression(self):
        files, manifest = build_file_set(synthetic_bindings())
        self.assertIn("runtime/requirements.lock", files)
        self.assertIn("runtime/wheelhouse/numpy-test.whl", files)
        self.assertIn("runtime/python/cpython-test.tar.gz", files)
        self.assertIn("kernel_support/target_dependency.py", files)
        self.assertIn("kernel_support/hostile_dependency.py", files)
        self.assertIn("evidence/L4_L12_EXACT_REGRESSION.json", files)
        self.assertIn(
            "frozen/audited-386ee2c/DEVELOPMENT_R_RELATIONAL_INTERVAL_SPECTRUM_V001/"
            "ADJUDICATION_V002_L12_V003R1_STAGE6R2.json",
            files,
        )
        self.assertEqual(manifest["runtime"]["numpy_version"], "2.0.2")

    def test_frozen_runtime_must_include_prior_and_mathematical_definitions(self):
        bindings = synthetic_bindings()
        bindings["frozen_runtime"]["bundle_files"] = []
        with self.assertRaises(EvidenceError):
            build_file_set(bindings)

    def test_unsafe_archive_path_fails_closed(self):
        with self.assertRaises(EvidenceError):
            safe_archive_path("../escape", "test path")

    def test_extracted_bundle_file_verifier_detects_change(self):
        files, manifest = build_file_set(synthetic_bindings())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, data in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            (root / "BUNDLE_MANIFEST.json").write_bytes(canonical_json_bytes(manifest))
            verify_files(root, manifest)
            (root / "kernel" / "target_exact_kernel.py").write_text("changed", encoding="utf-8")
            with self.assertRaises(Exception):
                verify_files(root, manifest)

    def test_no_compute_stack_parameters_are_fully_derived(self):
        bindings = synthetic_bindings()
        _files, manifest = build_file_set(bindings)
        config = json.loads((ROOT / "AWS_RUN_CONFIG.example.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "bundle.tar.gz"
            archive.write_bytes(b"authenticated synthetic archive")
            manifest["archive"] = {
                "path": str(archive),
                "sha256": sha256_file(archive),
                "bytes": archive.stat().st_size,
            }
            parameters, evidence = build_parameters(
                config,
                bindings,
                manifest,
                "test-run",
                "source/bootstrap.sh",
                "source/bundle.tar.gz",
            )
        values = {record["ParameterKey"]: record["ParameterValue"] for record in parameters}
        self.assertEqual(values["ReviewedTemplateSha256"], sha256_file(ROOT / "aws" / "cloudformation.yaml"))
        self.assertEqual(values["AmiId"], config["observed_ami_id"])
        self.assertEqual(values["WorkersPerBranch"], "180")
        self.assertEqual(values["ScratchVolumeGiB"], "1000")
        self.assertEqual(values["ScratchVolumeIops"], "80000")
        self.assertEqual(values["ScratchVolumeThroughput"], "2000")
        self.assertEqual(values["RuntimeAdvisoryMinutes"], "835")
        self.assertEqual(evidence["claim_boundary"], "PARAMETER_GENERATION_ONLY__NO_AWS_CALL_AND_NO_RESOURCE_CREATION")
        self.assertEqual(evidence["bootstrap"]["bytes"], (ROOT / "aws" / "bootstrap.sh").stat().st_size)


if __name__ == "__main__":
    unittest.main()
