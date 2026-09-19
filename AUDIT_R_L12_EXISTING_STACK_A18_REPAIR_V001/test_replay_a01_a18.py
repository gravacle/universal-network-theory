#!/usr/bin/env python3
"""Focused nonphysical tests for the bounded A01--A18 replay primitives."""

from __future__ import annotations

import copy
import importlib.util
import inspect
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "replay_a01_a18.py"
SPEC = importlib.util.spec_from_file_location("replay_a01_a18_tested", SOURCE)
assert SPEC is not None and SPEC.loader is not None
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


class ReplayCoordinatorTests(unittest.TestCase):
    launcher_pointer = (
        "/sealed_dependencies/v012_dual_launch_coordinator_packet/"
        "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001~1"
        "production_dual_l12_launcher.py"
    )

    def a01(self) -> dict[str, object]:
        return {
            "files": {
                "build_target_cache.py": "d" * 64,
                "production_obligation_validators.py": "a" * 64,
                "unchanged.py": "b" * 64,
            },
            "sealed_dependencies": {
                "v012_dual_launch_coordinator_packet": {
                    "AUDIT_PREPARATION_R_L12_DUAL_LAUNCH_COORDINATOR_V001/"
                    "production_dual_l12_launcher.py": "e" * 64,
                },
            },
            "hard_locks": {"solver_formula": "FROZEN"},
        }

    def a01_updates(self) -> dict[str, object]:
        return {
            "/files/build_target_cache.py": "f" * 64,
            "/files/production_obligation_validators.py": "c" * 64,
            self.launcher_pointer: "9" * 64,
        }

    def get_pointer(self, record: object, pointer: str) -> object:
        current = record
        for part in replay._decode_pointer(pointer):
            if type(current) is list:
                current = current[int(part)]
            else:
                current = current[part]
        return current

    def test_retired_template_only_changes_complete_dynamic_census(self) -> None:
        source = self.a01()
        updated = replay.update_authenticated_template(
            "A01_FREEZE_AND_SOURCE_PACKET", source, self.a01_updates(),
        )
        self.assertEqual(
            updated["files"]["production_obligation_validators.py"], "c" * 64,
        )
        self.assertEqual(updated["files"]["build_target_cache.py"], "f" * 64)
        self.assertEqual(updated["files"]["unchanged.py"], "b" * 64)
        self.assertEqual(source["hard_locks"], updated["hard_locks"])

    def test_missing_extra_and_nonhash_dynamic_values_refuse(self) -> None:
        source = self.a01()
        with self.assertRaisesRegex(replay.Refusal, "dynamic binding census"):
            replay.update_authenticated_template(
                "A01_FREEZE_AND_SOURCE_PACKET", source, {},
            )
        with self.assertRaisesRegex(replay.Refusal, "dynamic binding census"):
            replay.update_authenticated_template(
                "A01_FREEZE_AND_SOURCE_PACKET", source,
                {
                    **self.a01_updates(),
                    "/hard_locks/solver_formula": "CHANGED",
                },
            )
        with self.assertRaisesRegex(replay.Refusal, "SHA-256"):
            replay.update_authenticated_template(
                "A01_FREEZE_AND_SOURCE_PACKET", source,
                {
                    **self.a01_updates(),
                    "/files/production_obligation_validators.py": "not-a-hash",
                },
            )

    def test_reconstruction_requires_sink_and_detects_sink_mutation(self) -> None:
        record = self.a01()
        with self.assertRaisesRegex(replay.Refusal, "lacks required"):
            replay.validate_with_sinks("A01_FREEZE_AND_SOURCE_PACKET", record, ())

        def mutating(_artifact: str, value: dict[str, object]) -> None:
            value["hard_locks"]["solver_formula"] = "MUTATED"

        with self.assertRaisesRegex(replay.Refusal, "mutated candidate"):
            replay.validate_with_sinks(
                "A01_FREEZE_AND_SOURCE_PACKET", record, (mutating,),
            )

    def test_existing_publisher_plan_is_exactly_bounded(self) -> None:
        hashes = {length: f"{length:064x}" for length in (4, 6, 8, 10, 12)}
        actions = replay.existing_publisher_actions(hashes)
        self.assertEqual(len(actions), 11)
        self.assertEqual(
            [action.artifact_id for action in actions].count("A05_FIVE_CACHE_SET"),
            5,
        )
        self.assertEqual(
            [action.artifact_id for action in actions].count("A10_CONTROL_HISTORIES"),
            3,
        )
        self.assertEqual(
            [action.artifact_id for action in actions].count("A14_L10_HISTORY"),
            1,
        )
        invoked: list[tuple[str, ...]] = []
        replay.run_existing_publisher(
            actions[0], lambda command: invoked.append(tuple(command)) or 0,
        )
        self.assertEqual(invoked, [actions[0].command])
        forged = replay.PublisherAction("A02_NONPHYSICAL_PREFLIGHT", 1, ("false",))
        with self.assertRaisesRegex(replay.Refusal, "unregistered"):
            replay.run_existing_publisher(forged, lambda _command: 0)

    def test_every_registered_template_pointer_exists_and_is_a_hash(self) -> None:
        self.assertEqual(
            set(replay.TEMPLATE_PATH_BY_ARTIFACT), set(replay.DYNAMIC_POINTERS),
        )
        for artifact_id, relative in replay.TEMPLATE_PATH_BY_ARTIFACT.items():
            record = replay.retirement.strict_json(
                (replay.ROOT / relative).read_bytes(), artifact_id,
            )
            updates = {
                pointer: self.get_pointer(record, pointer)
                for pointer in replay.DYNAMIC_POINTERS[artifact_id]
            }
            self.assertTrue(all(replay._sha256_text(value)
                                for value in updates.values()))
            self.assertEqual(
                replay.update_authenticated_template(artifact_id, record, updates),
                record,
            )

    def test_measured_update_maps_have_exact_registered_census(self) -> None:
        produced = {
            (artifact_id, instance): replay.hashlib.sha256(
                f"{artifact_id}/{instance}".encode("ascii")
            ).hexdigest()
            for _operation, artifact_id, instance in replay.REPLAY_SEQUENCE
        }
        produced[("A27_MUTATION_LEDGER", 1)] = "d" * 64
        measured = (
            replay.REPAIRED_CANONICAL_BUILDER_SHA256,
            replay.REPAIRED_CANONICAL_LAUNCHER_SHA256,
            replay.PINNED_LIVE_SOURCES["production_obligation_validators"][1],
        )
        with mock.patch.object(
            replay, "_measured_repaired_source_hashes", return_value=measured,
        ):
            for artifact_id in replay.TEMPLATE_PATH_BY_ARTIFACT:
                updates = replay.measured_template_updates(
                    replay.ROOT, artifact_id, produced,
                )
                self.assertEqual(
                    set(updates), set(replay.DYNAMIC_POINTERS[artifact_id]),
                )
                self.assertTrue(all(replay._sha256_text(value)
                                    for value in updates.values()))

    def test_live_module_census_is_hash_pinned(self) -> None:
        self.assertEqual(
            replay.PINNED_LIVE_SOURCES["build_target_cache"],
            (replay.OLD_CANONICAL_BUILDER_PATH,
             replay.REPAIRED_CANONICAL_BUILDER_SHA256),
        )
        self.assertEqual(
            replay.PINNED_REPAIRED_CANONICAL_SOURCES[
                "production_dual_l12_launcher"
            ],
            (replay.OLD_CANONICAL_LAUNCHER_PATH,
             replay.REPAIRED_CANONICAL_LAUNCHER_SHA256),
        )
        for name, (relative, expected) in (
            replay.PINNED_EXECUTABLE_DEPENDENCIES.items()
        ):
            if name == "build_target_cache":
                continue
            replay._read_pinned_source_bytes(
                replay.ROOT / relative, expected, name,
            )

    def test_executable_dependency_path_swap_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.py"
            alternate = root / "alternate.py"
            source.write_bytes(b"VALUE = 1\n")
            alternate.write_bytes(b"VALUE = 2\n")
            digest = replay.hashlib.sha256(source.read_bytes()).hexdigest()
            original_stat = replay.os.stat
            attacked = False

            def swap(path: object, *args: object, **kwargs: object):
                nonlocal attacked
                if Path(path) == source and not attacked:
                    attacked = True
                    os.replace(alternate, source)
                return original_stat(path, *args, **kwargs)

            with mock.patch.object(replay.os, "stat", side_effect=swap):
                with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
                    replay._read_pinned_source_bytes(source, digest, "synthetic")

    def test_preloaded_executable_dependency_alias_refuses(self) -> None:
        name = "compute_streamed_history"
        previous = replay.sys.modules.pop(name, None)
        replay.sys.modules[name] = replay.types.ModuleType(name)
        try:
            with self.assertRaisesRegex(RuntimeError, "name is aliased"):
                replay._load_authenticated_module(name)
        finally:
            replay.sys.modules.pop(name, None)
            if previous is not None:
                replay.sys.modules[name] = previous

    def test_owner_once_json_path_swap_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.json"
            alternate = root / "alternate.json"
            source.write_bytes(b'{"value":1}\n')
            alternate.write_bytes(b'{"value":2}\n')
            source.chmod(0o444)
            alternate.chmod(0o444)
            original_stat = replay.os.stat
            attacked = False

            def swap(path: object, *args: object, **kwargs: object):
                nonlocal attacked
                if Path(path) == source and not attacked:
                    attacked = True
                    os.replace(alternate, source)
                return original_stat(path, *args, **kwargs)

            with mock.patch.object(replay.os, "stat", side_effect=swap):
                with self.assertRaisesRegex(replay.Refusal, "owner-once"):
                    replay._stable_owner_once_json(source, "synthetic JSON")

    def test_a18_histories_use_descriptor_bound_json_reads(self) -> None:
        source = inspect.getsource(replay.measured_a18_updates)
        self.assertIn("_stable_owner_once_json", source)
        self.assertNotIn("read_bytes", source)

    def test_a18_constructor_preserves_policy_and_calls_two_sinks(self) -> None:
        template = replay.load_a18_candidate_template()
        updates = {
            pointer: self.get_pointer(template, pointer)
            for pointer in replay.A18_DYNAMIC_POINTERS
        }
        called: list[str] = []

        def target(artifact: str, _record: dict[str, object]) -> None:
            called.append("target:" + artifact)

        def independent(artifact: str, _record: dict[str, object]) -> None:
            called.append("independent:" + artifact)

        record = replay.construct_a18(
            updates, target, independent, template=template,
        )
        self.assertEqual(called, [
            "target:A18_L10_CROSS_GATE",
            "independent:A18_L10_CROSS_GATE",
        ])
        self.assertEqual(record["checks_total"], 65)
        self.assertEqual(record["checks_passed"], 65)
        self.assertEqual(record["checks"], template["checks"])
        self.assertEqual(
            record["comparison_policy"]["physical_abs_tolerance"], 1.0e-8,
        )

    def test_a18_constructor_refuses_incomplete_census_and_bad_path(self) -> None:
        template = replay.load_a18_candidate_template()
        updates = {
            pointer: self.get_pointer(template, pointer)
            for pointer in replay.A18_DYNAMIC_POINTERS
        }
        missing = dict(updates)
        missing.pop(next(iter(missing)))
        with self.assertRaisesRegex(replay.Refusal, "binding census"):
            replay.construct_a18(missing, lambda *_: None, lambda *_: None,
                                 template=template)
        bad = dict(updates)
        path_pointer = next(
            pointer for pointer in bad if pointer.endswith("/path")
        )
        bad[path_pointer] = "/synthetic/outside-repository"
        with self.assertRaisesRegex(replay.Refusal, "canonical path"):
            replay.construct_a18(bad, lambda *_: None, lambda *_: None,
                                 template=template)

    def test_live_entry_has_no_injected_runner_sink_path_or_binding_surface(self) -> None:
        signature = inspect.signature(replay.coordinate_canonical_a01_a18_replay)
        self.assertEqual(
            list(signature.parameters), ["expected_retirement_receipt_sha256"],
        )
        runner = replay._canonical_publisher_runner(replay.ROOT)
        with self.assertRaisesRegex(replay.Refusal, "authenticated entry"):
            runner(("python3", "-B", "/tmp/unregistered.py"))
        source = inspect.getsource(replay.coordinate_canonical_a01_a18_replay)
        self.assertLess(
            source.index("reconcile_or_publish_repaired_sources"),
            source.index("ExactLiveReview"),
        )

    def test_json_reconciliation_is_exact_and_never_replaces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            calls: list[str] = []

            def sink(artifact: str, _record: dict[str, object]) -> None:
                calls.append(artifact)

            digest, reconciled = replay._reconcile_or_publish_json(
                path, {"value": 1}, "SYNTHETIC", (sink,),
            )
            inode = os.stat(path).st_ino
            self.assertFalse(reconciled)
            same_digest, reconciled = replay._reconcile_or_publish_json(
                path, {"value": 1}, "SYNTHETIC", (sink,),
            )
            self.assertTrue(reconciled)
            self.assertEqual(same_digest, digest)
            self.assertEqual(os.stat(path).st_ino, inode)
            with self.assertRaisesRegex(replay.Refusal, "differs from replay"):
                replay._reconcile_or_publish_json(
                    path, {"value": 2}, "SYNTHETIC", (sink,),
                )
            self.assertEqual(os.stat(path).st_ino, inode)
            self.assertEqual(calls, ["SYNTHETIC", "SYNTHETIC"])

    def test_existing_publisher_completion_reconciles_without_rerun(self) -> None:
        class Review:
            def __init__(self) -> None:
                self.calls = 0

            def validate_completed_publisher(self, *_args, **_kwargs) -> None:
                self.calls += 1

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            action = replay.existing_publisher_actions()[0]
            output = root / replay.PUBLISHED_PATH_BY_INSTANCE[
                (action.artifact_id, action.instance)
            ]
            ledger = root / replay.MUTATION_LEDGER_PATH
            output.parent.mkdir(parents=True)
            invoked = 0

            def runner(_command: object) -> int:
                nonlocal invoked
                invoked += 1
                replay.retirement.publish_once(output, {"kind": "preflight"})
                replay.retirement.publish_once(ledger, {"kind": "ledger"})
                return 0

            review = Review()
            first = replay._reconcile_or_run_existing_publisher(
                root, review, action, runner,
            )
            second = replay._reconcile_or_run_existing_publisher(
                root, review, action, runner,
            )
            self.assertFalse(first[2])
            self.assertTrue(second[2])
            self.assertEqual(first[:2], second[:2])
            self.assertEqual(invoked, 1)
            self.assertEqual(review.calls, 2)

    def test_existing_publisher_partial_effects_refuse_without_runner(self) -> None:
        class Review:
            def validate_completed_publisher(self, *_args, **_kwargs) -> None:
                raise AssertionError("review must not run")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            action = replay.existing_publisher_actions()[0]
            ledger = root / replay.MUTATION_LEDGER_PATH
            ledger.parent.mkdir(parents=True)
            replay.retirement.publish_once(ledger, {"partial": True})
            with self.assertRaisesRegex(replay.Refusal, "partial publication"):
                replay._reconcile_or_run_existing_publisher(
                    root, Review(), action,
                    lambda _command: (_ for _ in ()).throw(
                        AssertionError("runner must not run")
                    ),
                )

    def test_partial_cache_and_history_workspaces_are_preserved(self) -> None:
        class Review:
            def validate_completed_publisher(self, *_args, **_kwargs) -> None:
                raise AssertionError("review must not run")

        hashes = {length: f"{length:064x}" for length in (4, 6, 8, 10, 12)}
        actions = replay.existing_publisher_actions(hashes)
        for action in (
            next(item for item in actions if item.artifact_id == "A05_FIVE_CACHE_SET"),
            next(item for item in actions if item.artifact_id == "A10_CONTROL_HISTORIES"),
        ):
            with self.subTest(artifact=action.artifact_id), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                primary = root / replay.PUBLISHED_PATH_BY_INSTANCE[
                    (action.artifact_id, action.instance)
                ]
                if action.artifact_id == "A05_FIVE_CACHE_SET":
                    primary.parent.mkdir(parents=True)
                else:
                    workspace = replay._publisher_workspace(root, action)
                    assert workspace is not None
                    workspace.mkdir(parents=True)
                with self.assertRaisesRegex(replay.Refusal, "partial"):
                    replay._reconcile_or_run_existing_publisher(
                        root, Review(), action,
                        lambda _command: (_ for _ in ()).throw(
                            AssertionError("runner must not run")
                        ),
                    )

    def make_source_transition_root(
        self, directory: str,
    ) -> tuple[Path, dict[str, object]]:
        root = Path(directory).resolve()
        custody = root / "custody"
        entries: list[dict[str, object]] = []
        for relative, live in (
            (replay.OLD_CANONICAL_LAUNCHER_PATH,
             replay.ROOT / replay.OLD_CANONICAL_LAUNCHER_PATH),
            (replay.OLD_CANONICAL_BUILDER_PATH,
             replay.ROOT / replay.OLD_CANONICAL_BUILDER_PATH),
        ):
            retired = custody.joinpath(*replay.PurePosixPath(relative).parts)
            retired.parent.mkdir(parents=True, exist_ok=True)
            retired.write_bytes(live.read_bytes())
            retired.chmod(0o444)
            entries.append({
                "kind": "file",
                **replay.retirement.file_row(retired, relative),
            })
            root.joinpath(*replay.PurePosixPath(relative).parts).parent.mkdir(
                parents=True, exist_ok=True,
            )
        candidate = root.joinpath(
            *replay.PurePosixPath(replay.REPAIRED_LAUNCHER_CANDIDATE_PATH).parts
        )
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_bytes(
            (replay.ROOT / replay.REPAIRED_LAUNCHER_CANDIDATE_PATH).read_bytes()
        )
        candidate.chmod(0o444)
        return root, {"custody_root": "custody", "entries": entries}

    def test_exact_launcher_and_builder_source_derivations(self) -> None:
        old_launcher = (
            replay.ROOT / replay.OLD_CANONICAL_LAUNCHER_PATH
        ).read_bytes()
        candidate = (
            replay.ROOT / replay.REPAIRED_LAUNCHER_CANDIDATE_PATH
        ).read_bytes()
        self.assertEqual(
            replay._apply_exact_launcher_replacements(old_launcher), candidate,
        )
        self.assertEqual(
            replay.hashlib.sha256(candidate).hexdigest(),
            replay.REPAIRED_CANONICAL_LAUNCHER_SHA256,
        )
        old_builder = (
            replay.ROOT / replay.OLD_CANONICAL_BUILDER_PATH
        ).read_bytes()
        self.assertEqual(
            old_builder.count(replay.OLD_CANONICAL_LAUNCHER_SHA256.encode()), 1,
        )
        repaired_builder = old_builder.replace(
            replay.OLD_CANONICAL_LAUNCHER_SHA256.encode(),
            replay.REPAIRED_CANONICAL_LAUNCHER_SHA256.encode(), 1,
        )
        self.assertEqual(
            replay.hashlib.sha256(repaired_builder).hexdigest(),
            replay.REPAIRED_CANONICAL_BUILDER_SHA256,
        )

    def test_repaired_source_pair_publishes_once_and_reconciles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, census = self.make_source_transition_root(directory)
            derived = replay.derive_repaired_source_bytes(root, census)
            first = replay.reconcile_or_publish_repaired_sources(root, census)
            self.assertFalse(first["reconciled"])
            second = replay.reconcile_or_publish_repaired_sources(root, census)
            self.assertTrue(second["reconciled"])
            for relative, raw in derived.items():
                path = root.joinpath(*replay.PurePosixPath(relative).parts)
                self.assertEqual(path.read_bytes(), raw)
                metadata = os.stat(path, follow_symlinks=False)
                self.assertEqual(metadata.st_nlink, 1)
                self.assertFalse(metadata.st_mode & 0o222)

    def test_interrupted_source_pair_is_preserved_and_refused_on_restart(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, census = self.make_source_transition_root(directory)
            original = replay._publish_owner_once_source
            calls = 0

            def interrupt(*args: object, **kwargs: object) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise replay.Refusal("injected source-pair interruption")
                original(*args, **kwargs)

            with mock.patch.object(
                replay, "_publish_owner_once_source", side_effect=interrupt,
            ):
                with self.assertRaisesRegex(replay.Refusal, "injected"):
                    replay.reconcile_or_publish_repaired_sources(root, census)
            launcher = root / replay.OLD_CANONICAL_LAUNCHER_PATH
            builder = root / replay.OLD_CANONICAL_BUILDER_PATH
            self.assertTrue(launcher.is_file())
            self.assertFalse(replay.retirement.path_exists(builder))
            with self.assertRaisesRegex(replay.Refusal, "partial repaired source"):
                replay.reconcile_or_publish_repaired_sources(root, census)
            self.assertEqual(
                replay.hashlib.sha256(launcher.read_bytes()).hexdigest(),
                replay.REPAIRED_CANONICAL_LAUNCHER_SHA256,
            )

    def test_repaired_source_publication_refuses_symlink_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            outside = root / "outside"
            outside.mkdir()
            (root / "alias").symlink_to(outside, target_is_directory=True)
            raw = (
                replay.ROOT / replay.REPAIRED_LAUNCHER_CANDIDATE_PATH
            ).read_bytes()
            with self.assertRaisesRegex(replay.Refusal, "parent chain"):
                replay._publish_owner_once_source(
                    root, root / "alias/source.py", raw,
                    replay.REPAIRED_CANONICAL_LAUNCHER_SHA256,
                )

    def test_repaired_source_destination_race_never_clobbers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            parent = root / "canonical"
            parent.mkdir()
            target = parent / "source.py"
            target.write_bytes(b"attacker-owned")
            raw = (
                replay.ROOT / replay.REPAIRED_LAUNCHER_CANDIDATE_PATH
            ).read_bytes()
            with self.assertRaisesRegex(replay.Refusal, "already exists"):
                replay._publish_owner_once_source(
                    root, target, raw,
                    replay.REPAIRED_CANONICAL_LAUNCHER_SHA256,
                )
            self.assertEqual(target.read_bytes(), b"attacker-owned")

    def test_repaired_source_parent_swap_race_never_writes_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            parent = root / "canonical"
            parent.mkdir()
            held = root / "held"
            raw = (
                replay.ROOT / replay.REPAIRED_LAUNCHER_CANDIDATE_PATH
            ).read_bytes()
            original = replay._retained_parent_chain
            swapped = False

            def swap(*args: object, **kwargs: object) -> list[int]:
                nonlocal swapped
                descriptors = original(*args, **kwargs)
                if not swapped:
                    swapped = True
                    parent.rename(held)
                    parent.mkdir()
                    (parent / "attacker.txt").write_bytes(b"preserved")
                return descriptors

            with mock.patch.object(
                replay, "_retained_parent_chain", side_effect=swap,
            ):
                with self.assertRaises(replay.Refusal):
                    replay._publish_owner_once_source(
                        root, parent / "source.py", raw,
                        replay.REPAIRED_CANONICAL_LAUNCHER_SHA256,
                    )
            self.assertEqual((parent / "attacker.txt").read_bytes(), b"preserved")
            self.assertFalse((parent / "source.py").exists())
            self.assertEqual((held / "source.py").read_bytes(), raw)

    def test_writable_launcher_candidate_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root, census = self.make_source_transition_root(directory)
            candidate = root / replay.REPAIRED_LAUNCHER_CANDIDATE_PATH
            candidate.chmod(0o644)
            with self.assertRaisesRegex(replay.Refusal, "source identity mismatch"):
                replay.derive_repaired_source_bytes(root, census)


class CompletedRetirementHostileRestoreTests(unittest.TestCase):
    def make_completed_retirement(
        self, root: Path,
    ) -> tuple[dict[str, object], dict[str, tuple[int, int]]]:
        entries: list[dict[str, object]] = []
        identities: dict[str, tuple[int, int]] = {}
        for ordinal, logical in enumerate(replay.HOSTILE_A17_RESTORE_PATHS):
            path = root.joinpath(*replay.PurePosixPath(logical).parts)
            if logical.endswith(("V004R4_CACHE_PAYLOADS", "V004R4_WORKSPACES",
                                 "V004R4_PHYSICAL_OUTPUTS")):
                path.mkdir(parents=True)
                payload = path / f"payload_{ordinal}.bin"
                payload.write_bytes(f"payload-{ordinal}".encode("ascii"))
                payload.chmod(0o444)
                entry = replay.retirement.directory_row(path, logical)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(("{\"ordinal\":%d}\n" % ordinal).encode("ascii"))
                path.chmod(0o444)
                entry = {"kind": "file", **replay.retirement.file_row(path, logical)}
            entries.append(entry)
            metadata = os.stat(path, follow_symlinks=False)
            identities[logical] = (metadata.st_dev, metadata.st_ino)
        census = {
            "schema": "V012_A01_A17_PRE_A18_RETIREMENT_CENSUS_V001",
            "classification": "EXACT_NONEXECUTED_OWNER_ONCE_RETIREMENT_CENSUS",
            "custody_root": "custody/retired",
            "entries": entries,
            "required_absent_paths": ["future/a18.json"],
            "entry_count": len(entries),
            "source_file_count": sum(
                1 if entry["kind"] == "file" else entry["file_count"]
                for entry in entries
            ),
            "source_total_bytes": sum(
                entry["bytes"] if entry["kind"] == "file" else entry["total_bytes"]
                for entry in entries
            ),
            "executed": False,
            "claim_boundary": "SYNTHETIC_TEST_ONLY",
        }
        (root / "custody").mkdir()
        census = replay.retirement.validate_census(census)
        replay.retirement.retire(root, census)
        return census, identities

    def assert_all_in_custody(
        self, root: Path, census: dict[str, object],
    ) -> None:
        custody = root / "custody/retired"
        for entry in census["entries"]:
            self.assertFalse(
                replay.retirement.path_exists(
                    root.joinpath(*replay.PurePosixPath(entry["path"]).parts)
                )
            )
            replay.retirement.inspect_entry(
                replay.retirement.destination(custody, entry), entry,
            )

    def make_interrupted_restore(
        self,
        root: Path,
        census: dict[str, object],
        moved_count: int,
        *,
        omit_last_event: bool = False,
    ) -> None:
        custody, _receipt, retirement_sha = replay._load_completed_retirement_receipt(
            root, census,
        )
        intent_path, event_root, _receipt_path = replay._restore_paths(custody)
        os.mkdir(event_root, 0o700)
        replay.retirement.fsync_directory(custody)
        replay.retirement.publish_once(
            intent_path, replay._expected_restore_intent(retirement_sha),
        )
        for ordinal, entry in enumerate(
            replay._hostile_entries(census)[:moved_count], start=1,
        ):
            source = replay.retirement.destination(custody, entry)
            target = root.joinpath(*replay.PurePosixPath(entry["path"]).parts)
            replay.retirement.make_parents_beneath(root, target)
            identity = replay.retirement.retained_entry_identity(source, entry)
            replay.retirement.rename_exclusive(source, target)
            replay.retirement.fsync_moved_entry(target, entry)
            replay.retirement.fsync_directory(source.parent)
            replay.retirement.fsync_directory(target.parent)
            if omit_last_event and ordinal == moved_count:
                continue
            replay.retirement.publish_once(
                event_root / f"EVENT_{ordinal:03d}.json",
                replay._expected_restore_event(
                    ordinal, entry, replay._identity_sha256(identity),
                ),
            )

    def test_completed_retirement_restore_preserves_identity_owner_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, identities = self.make_completed_retirement(root)
            result = replay.restore_completed_hostile_a17(root, census)
            self.assertEqual(result["restored_entry_count"], 7)
            self.assertTrue((root / "custody/retired" / replay.RESTORE_RECEIPT_NAME).is_file())
            for entry in census["entries"]:
                target = root.joinpath(*replay.PurePosixPath(entry["path"]).parts)
                replay.retirement.inspect_entry(target, entry)
                metadata = os.stat(target, follow_symlinks=False)
                self.assertEqual(
                    (metadata.st_dev, metadata.st_ino), identities[entry["path"]],
                )
                self.assertFalse(replay.retirement.path_exists(
                    replay.retirement.destination(root / "custody/retired", entry)
                ))

    def test_completed_restore_reconciles_without_moving_again(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, identities = self.make_completed_retirement(root)
            first = replay.restore_completed_hostile_a17(root, census)
            second = replay.restore_completed_hostile_a17(root, census)
            self.assertTrue(second["reconciled"])
            self.assertEqual(first["receipt_sha256"], second["receipt_sha256"])
            for entry in census["entries"]:
                target = root.joinpath(*replay.PurePosixPath(entry["path"]).parts)
                metadata = os.stat(target, follow_symlinks=False)
                self.assertEqual(
                    (metadata.st_dev, metadata.st_ino), identities[entry["path"]],
                )

    def test_restore_refuses_destination_without_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, _ = self.make_completed_retirement(root)
            logical = replay.HOSTILE_A17_RESTORE_PATHS[0]
            destination = root.joinpath(*replay.PurePosixPath(logical).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"do-not-clobber")
            with self.assertRaisesRegex(replay.Refusal, "not absent"):
                replay.restore_completed_hostile_a17(root, census)
            self.assertEqual(destination.read_bytes(), b"do-not-clobber")

    def test_interruption_rolls_back_every_restored_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, _ = self.make_completed_retirement(root)
            with self.assertRaisesRegex(replay.Refusal, "failed and rolled back"):
                replay.restore_completed_hostile_a17(root, census, inject_after=4)
            self.assert_all_in_custody(root, census)
            custody = root / "custody/retired"
            self.assertFalse((custody / replay.RESTORE_INTENT_NAME).exists())
            self.assertFalse((custody / replay.RESTORE_EVENT_DIRECTORY_NAME).exists())

    def test_restart_recovers_rename_event_gap_then_completes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, identities = self.make_completed_retirement(root)
            self.make_interrupted_restore(
                root, census, 4, omit_last_event=True,
            )
            result = replay.restore_completed_hostile_a17(root, census)
            self.assertEqual(result["restored_entry_count"], 7)
            for entry in census["entries"]:
                target = root.joinpath(*replay.PurePosixPath(entry["path"]).parts)
                metadata = os.stat(target, follow_symlinks=False)
                self.assertEqual(
                    (metadata.st_dev, metadata.st_ino), identities[entry["path"]],
                )

    def test_second_restart_finishes_interrupted_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, identities = self.make_completed_retirement(root)
            self.make_interrupted_restore(root, census, 4)
            original = replay.retirement.rename_exclusive
            moves = 0

            def interrupt_recovery(source: Path, target: Path) -> None:
                nonlocal moves
                moves += 1
                if moves == 2:
                    raise replay.Refusal("injected recovery interruption")
                original(source, target)

            with mock.patch.object(
                replay.retirement, "rename_exclusive",
                side_effect=interrupt_recovery,
            ):
                with self.assertRaisesRegex(replay.Refusal, "injected recovery"):
                    replay.recover_interrupted_hostile_a17_restore(root, census)
            result = replay.restore_completed_hostile_a17(root, census)
            self.assertEqual(result["restored_entry_count"], 7)
            for entry in census["entries"]:
                target = root.joinpath(*replay.PurePosixPath(entry["path"]).parts)
                metadata = os.stat(target, follow_symlinks=False)
                self.assertEqual(
                    (metadata.st_dev, metadata.st_ino), identities[entry["path"]],
                )

    def test_destination_race_refuses_without_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, _ = self.make_completed_retirement(root)
            logical = replay.HOSTILE_A17_RESTORE_PATHS[0]
            destination = root.joinpath(*replay.PurePosixPath(logical).parts)
            original = replay.retirement.make_parents_beneath
            attacked = False

            def race(custody: Path, target: Path) -> None:
                nonlocal attacked
                original(custody, target)
                if not attacked:
                    attacked = True
                    target.write_bytes(b"racing-destination")

            with mock.patch.object(
                replay.retirement, "make_parents_beneath", side_effect=race,
            ):
                with self.assertRaisesRegex(replay.Refusal, "rolled back"):
                    replay.restore_completed_hostile_a17(root, census)
            self.assertEqual(destination.read_bytes(), b"racing-destination")
            custody = root / "custody/retired"
            for entry in census["entries"]:
                replay.retirement.inspect_entry(
                    replay.retirement.destination(custody, entry), entry,
                )

    def test_restore_fsyncs_every_moved_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, _ = self.make_completed_retirement(root)
            original = replay.retirement.fsync_moved_entry
            observed: list[str] = []

            def record(path: Path, entry: dict[str, object]) -> None:
                observed.append(entry["path"])
                original(path, entry)

            with mock.patch.object(
                replay.retirement, "fsync_moved_entry", side_effect=record,
            ):
                replay.restore_completed_hostile_a17(root, census)
            self.assertEqual(observed, list(replay.HOSTILE_A17_RESTORE_PATHS))

    def test_tampered_retirement_receipt_and_intent_refuse(self) -> None:
        for name in (replay.retirement.RECEIPT_NAME, replay.retirement.INTENT_NAME):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                census, _ = self.make_completed_retirement(root)
                path = root / "custody/retired" / name
                raw = path.read_bytes()
                raw = (
                    raw.replace(b"PASS", b"FAIL", 1)
                    if b"PASS" in raw else raw + b" "
                )
                os.unlink(path)
                path.write_bytes(raw)
                path.chmod(0o444)
                with self.assertRaises(replay.Refusal):
                    replay.restore_completed_hostile_a17(root, census)

    def test_tampered_completed_restore_receipt_refuses_reconciliation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            census, _ = self.make_completed_retirement(root)
            replay.restore_completed_hostile_a17(root, census)
            path = root / "custody/retired" / replay.RESTORE_RECEIPT_NAME
            raw = path.read_bytes().replace(b"PASS", b"FAIL", 1)
            os.unlink(path)
            path.write_bytes(raw)
            path.chmod(0o444)
            with self.assertRaisesRegex(replay.Refusal, "receipt mismatch"):
                replay.restore_completed_hostile_a17(root, census)


if __name__ == "__main__":
    unittest.main(verbosity=2)
