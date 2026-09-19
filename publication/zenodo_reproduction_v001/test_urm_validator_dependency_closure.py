#!/usr/bin/env python3
"""Tests for the publication-only URM-validator dependency closure."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path, PurePosixPath
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE_LAYOUT = (HERE / "build_urm_validator_dependency_closure.py").is_file()
if SOURCE_LAYOUT:
    REPO_ROOT = HERE.parents[1]
    BUILDER_PATH = HERE / "build_urm_validator_dependency_closure.py"
    VERIFIER_PATH = HERE / "verify_urm_validator_dependency_closure.py"
    SPEC_PATH = HERE / "urm_validator_dependency_closure.json"
else:  # Extracted layout: tests/, tools/, inventory/, and urm/ are siblings.
    REPO_ROOT = HERE.parent
    BUILDER_PATH = HERE.parent / "tools" / "build_urm_validator_dependency_closure.py"
    VERIFIER_PATH = HERE.parent / "tools" / "verify_urm_validator_dependency_closure.py"
    SPEC_PATH = HERE.parent / "inventory" / "URM_VALIDATOR_DEPENDENCY_CLOSURE.json"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = _load_module("build_urm_validator_dependency_closure", BUILDER_PATH)
verifier = _load_module("verify_urm_validator_dependency_closure", VERIFIER_PATH)


class UrmValidatorDependencyClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = verifier.load_and_validate_spec(SPEC_PATH)

    def test_generated_spec_is_current(self) -> None:
        if not SOURCE_LAYOUT:
            self.skipTest("private repository inventory is intentionally absent after extraction")
        expected = builder.canonical_bytes(builder.build_spec(REPO_ROOT))
        self.assertEqual(SPEC_PATH.read_bytes(), expected)

    def test_repository_exact_closure_passes_without_importing_validators(self) -> None:
        if not SOURCE_LAYOUT:
            self.skipTest("private exact relational inputs are intentionally absent after extraction")
        count, total = verifier.verify_root(self.spec, REPO_ROOT, "repository")
        self.assertEqual(
            count,
            self.spec["closure_entry_count"] + self.spec["runtime_artifact_count"],
        )
        self.assertEqual(
            total,
            self.spec["closure_total_bytes"]
            + self.spec["runtime_artifact_total_bytes"],
        )

    def test_missing_dependency_refuses(self) -> None:
        row = self.spec["entries"][0]
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(verifier.ClosureVerificationError):
                verifier.verify_root(
                    {"entries": [row], "runtime_artifacts": []},
                    Path(temporary),
                    "archive",
                )

    def test_tampered_dependency_refuses(self) -> None:
        row = self.spec["entries"][0]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root.joinpath(*PurePosixPath(row["archive_path"]).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            source_relative = (
                row["repository_path"] if SOURCE_LAYOUT else row["archive_path"]
            )
            source = REPO_ROOT.joinpath(*PurePosixPath(source_relative).parts)
            target.write_bytes(source.read_bytes() + b"\ntampered\n")
            with self.assertRaises(verifier.ClosureVerificationError):
                verifier.verify_root(
                    {"entries": [row], "runtime_artifacts": []},
                    root,
                    "archive",
                )

    def test_symlink_dependency_refuses(self) -> None:
        row = self.spec["entries"][0]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root.joinpath(*PurePosixPath(row["archive_path"]).parts)
            target.parent.mkdir(parents=True)
            source_relative = (
                row["repository_path"] if SOURCE_LAYOUT else row["archive_path"]
            )
            source = REPO_ROOT.joinpath(*PurePosixPath(source_relative).parts)
            target.symlink_to(source)
            with self.assertRaises(verifier.ClosureVerificationError):
                verifier.verify_root(
                    {"entries": [row], "runtime_artifacts": []},
                    root,
                    "archive",
                )

    def test_symlinked_parent_directory_refuses(self) -> None:
        row = self.spec["entries"][0]
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as outside:
            root = Path(temporary)
            archive = PurePosixPath(row["archive_path"])
            linked_parent = root / archive.parts[0]
            linked_parent.symlink_to(Path(outside), target_is_directory=True)
            target = Path(outside).joinpath(*archive.parts[1:])
            target.parent.mkdir(parents=True, exist_ok=True)
            source_relative = (
                row["repository_path"] if SOURCE_LAYOUT else row["archive_path"]
            )
            source = REPO_ROOT.joinpath(*PurePosixPath(source_relative).parts)
            target.write_bytes(source.read_bytes())
            with self.assertRaises(verifier.ClosureVerificationError):
                verifier.verify_root(
                    {"entries": [row], "runtime_artifacts": []},
                    root,
                    "archive",
                )

    def test_focused_closure_has_only_three_pinned_public_projections(self) -> None:
        self.assertEqual(self.spec["sanitized_conflict_count"], 3)
        self.assertEqual(
            {row["exact_repository_path"] for row in self.spec["sanitized_conflicts"]},
            verifier.PUBLIC_PROJECTION_PATHS,
        )
        for row in self.spec["sanitized_conflicts"]:
            self.assertEqual(
                row["existing_public_archive_path"], row["exact_archive_path"]
            )
            self.assertNotEqual(row["public_substitute_sha256"], row["exact_sha256"])

    def test_cache_projections_authenticate_raw_manifest_pins(self) -> None:
        if not SOURCE_LAYOUT:
            self.skipTest("repository-only projection sources are absent after extraction")
        for row in self.spec["sanitized_conflicts"]:
            if not row["exact_repository_path"].endswith("CACHE_MANIFEST.json"):
                continue
            public = json.loads(
                (REPO_ROOT / row["public_substitute_repository_path"]).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                public["public_projection"]["source_manifest_sha256"],
                row["exact_sha256"],
            )
            self.assertNotIn("/Users/", json.dumps(public, sort_keys=True))

    def test_spec_count_tamper_refuses(self) -> None:
        tampered = copy.deepcopy(self.spec)
        tampered["closure_entry_count"] += 1
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"
            path.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaises(verifier.ClosureVerificationError):
                verifier.load_and_validate_spec(path)

    def test_spec_path_escape_refuses(self) -> None:
        tampered = copy.deepcopy(self.spec)
        tampered["entries"][0]["repository_path"] = "../escape"
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"
            path.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaises(verifier.ClosureVerificationError):
                verifier.load_and_validate_spec(path)

    def test_spec_unknown_field_refuses(self) -> None:
        tampered = copy.deepcopy(self.spec)
        tampered["unexpected"] = True
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "spec.json"
            path.write_text(json.dumps(tampered), encoding="utf-8")
            with self.assertRaises(verifier.ClosureVerificationError):
                verifier.load_and_validate_spec(path)


if __name__ == "__main__":
    unittest.main()
