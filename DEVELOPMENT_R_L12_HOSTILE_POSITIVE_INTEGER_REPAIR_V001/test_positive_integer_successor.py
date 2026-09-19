#!/usr/bin/env python3
"""Focused non-live tests for the missing hostile positive-integer helper."""

from __future__ import annotations

import ast
import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "AUDIT_R_L12_PREFIX_HISTORY_ENGINE_V001/consume_cache_v004r4.py"
PATCH = Path(__file__).resolve().parent / "consume_cache_v004r4_positive_integer.patch"
CANONICAL_SHA256 = "700dce18ec8f50008a9e3022394a55c8d689268e21b80982896d37b92add7b74"
SUCCESSOR_SHA256 = "0242ae1b318f47a89fbfe84bcf83e92b57fe67ea4f6230a0b5538ab64db5fd3b"
ANCHOR = "def _lower_sha256(value: object, label: str) -> str:\n"
HELPER = (
    "def positive_integer(value: object) -> bool:\n"
    "    return type(value) is int and value > 0\n\n\n"
)

# These are the semantic schedule/session/release fields validated by the
# eight syntactic positive_integer calls in authenticate_context.
VALIDATION_SITES = (
    "schedule.created_epoch",
    "schedule.expires_epoch",
    "schedule.resource_snapshot.captured_epoch",
    "schedule.resource_snapshot.host_physical_memory_bytes",
    "schedule.resource_snapshot.available_memory_bytes",
    "schedule.resource_snapshot.workspace_free_disk_bytes",
    "schedule.resource_snapshot.workspace_filesystem_device",
    "handshake.created_epoch.initial",
    "workers.target_v012.process_id",
    "workers.hostile_v004r4.process_id",
    "workers.target_v012.ready_epoch",
    "workers.hostile_v004r4.ready_epoch",
    "handshake.created_epoch.aggregate",
    "release_epoch_by_role.target_v012",
    "release_epoch_by_role.hostile_v004r4",
)

EXPECTED_CALL_EXPRESSIONS = (
    "created",
    "expires",
    "snapshot[key]",
    "handshake['created_epoch']",
    "ready['process_id']",
    "ready['ready_epoch']",
    "handshake['created_epoch']",
    "epoch",
)


def successor_source() -> str:
    source = CANONICAL.read_text(encoding="utf-8")
    if source.count(ANCHOR) != 1 or "def positive_integer(" in source:
        raise AssertionError("canonical source no longer matches the preregistered delta")
    return source.replace(ANCHOR, HELPER + ANCHOR)


def load_successor_helper():
    tree = ast.parse(successor_source())
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "positive_integer"
    ]
    if len(functions) != 1:
        raise AssertionError("successor must contain exactly one positive_integer helper")
    namespace: dict[str, object] = {}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(CANONICAL), "exec"), namespace)
    return namespace["positive_integer"]


class PositiveIntegerSuccessorTests(unittest.TestCase):
    def test_exact_source_delta_and_hashes(self) -> None:
        canonical = CANONICAL.read_bytes()
        successor = successor_source().encode("utf-8")
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), CANONICAL_SHA256)
        self.assertEqual(hashlib.sha256(successor).hexdigest(), SUCCESSOR_SHA256)
        self.assertEqual(len(successor) - len(canonical), len(HELPER.encode("utf-8")))
        self.assertEqual(successor.replace(HELPER.encode("utf-8"), b"", 1), canonical)
        compile(successor, str(CANONICAL), "exec")

    def test_patch_contains_only_the_preregistered_helper(self) -> None:
        patch = PATCH.read_text(encoding="utf-8")
        added = [
            line[1:] for line in patch.splitlines(keepends=True)
            if line.startswith("+") and not line.startswith("+++")
        ]
        self.assertEqual("".join(added), HELPER)

    def test_all_hostile_integer_call_expressions_are_censused(self) -> None:
        tree = ast.parse(successor_source())
        calls = [
            ast.unparse(node.args[0])
            for node in ast.walk(tree)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "positive_integer"
            )
        ]
        calls.sort(key=lambda value: EXPECTED_CALL_EXPRESSIONS.index(value))
        self.assertCountEqual(calls, EXPECTED_CALL_EXPRESSIONS)
        self.assertEqual(len(VALIDATION_SITES), 15)

    def test_every_semantic_call_site_accepts_only_exact_positive_int(self) -> None:
        predicate = load_successor_helper()
        invalid = (True, False, 0, -1, 1.0, -1.0, "1", None)
        for site in VALIDATION_SITES:
            with self.subTest(site=site, value=1):
                self.assertIs(predicate(1), True)
            for value in invalid:
                with self.subTest(site=site, value=value):
                    self.assertIs(predicate(value), False)

    def test_exact_equivalence_to_target_predicate(self) -> None:
        predicate = load_successor_helper()

        def target_positive_integer(value: object) -> bool:
            return type(value) is int and value > 0

        values = (True, False, -2, -1, 0, 1, 2, -1.0, 0.0, 1.0, "1", None, [], {})
        for value in values:
            with self.subTest(value=value):
                self.assertIs(predicate(value), target_positive_integer(value))


if __name__ == "__main__":
    unittest.main()
