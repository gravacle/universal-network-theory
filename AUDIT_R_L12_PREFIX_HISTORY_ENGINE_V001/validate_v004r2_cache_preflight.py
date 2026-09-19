#!/usr/bin/env python3
"""Bounded nonphysical adversarial preflight for hostile V004R2."""

from __future__ import annotations

import ast
import copy
import json
import math
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

import build_hostile_v004r2_cache as builder
import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import independent_prefix_history_v004r2 as consumer
import v004r2_common as common


OUTPUT = common.HERE / "V004R2_CACHE_PREFLIGHT_RESULT.json"


class Counter:
    def __init__(self) -> None:
        self.value = 0

    def require(self, condition: bool, label: str) -> None:
        self.value += 1
        if not condition:
            raise AssertionError(label)

    def refuses(self, function, label: str) -> None:
        self.value += 1
        try:
            function()
        except (common.Refusal, OSError):
            return
        raise AssertionError(label)


COUNT = Counter()


def freeze_syntax_and_dependencies() -> dict[str, object]:
    freeze = common.validate_freeze()
    for role, path in common.FREEZE_FILE_PATHS.items():
        COUNT.require(common.sha256(path) == freeze["files"][role], f"frozen hash {role}")
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            COUNT.require(True, f"syntax {role}")
    for relative, expected in common.SEALED_DEPENDENCIES.items():
        COUNT.require(common.sha256(common.REPO / relative) == expected, f"dependency {relative}")
    return {"status": "PASS", "freeze_sha256": common.sha256(common.FREEZE),
            "frozen_file_roles": len(common.FREEZE_FILE_PATHS),
            "sealed_dependencies": len(common.SEALED_DEPENDENCIES)}


def exhaustive_rank_and_hamiltonian() -> dict[str, object]:
    rank_checks = 0
    for width in range(17):
        for q in range(width + 1):
            words = physical.reverse_masks(width, q)
            COUNT.require(len(words) == math.comb(width, q), f"basis census w{width}q{q}")
            for index, word in enumerate(words):
                COUNT.require(v3.reverse_rank(width, q, int(word)) == index,
                              f"rank w{width}q{q}i{index}")
                rank_checks += 1
    rng = np.random.default_rng(14441248)
    edges = physical.hostile_edges(4)
    differential_checks = 0
    for q in range(5):
        words, offsets, sources, targets = builder.operator_arrays(4, q, edges)
        direct = physical.CarrierBlock(4, q, edges)
        cached = consumer.legacy.CachedCarrier(4, q, edges, words, offsets, sources, targets)
        vector = rng.normal(size=(3, len(words))) + 1j * rng.normal(size=(3, len(words)))
        COUNT.require(np.array_equal(words, direct.words.astype("<u4")), f"L4 q{q} words")
        COUNT.require(np.array_equal(cached.multiply(vector), direct.multiply(vector)), f"L4 q{q} H differential")
        COUNT.require(np.array_equal(cached.currents(vector), direct.currents(vector)), f"L4 q{q} J differential")
        differential_checks += 3
    return {"status": "PASS", "rank_checks": rank_checks,
            "hamiltonian_current_differential_checks": differential_checks,
            "differential_tolerance": 0.0}


def exact_storage_and_sector_census() -> dict[str, object]:
    rows: dict[str, object] = {}
    for length in common.SUPPORTED:
        calculated = common.calculated_storage(length)
        COUNT.require(calculated == common.FROZEN_STORAGE[str(length)], f"L{length} exact storage")
        specs = common.expected_specs(length)
        COUNT.require(len(specs) == 2 * (length + 1) ** 2, f"L{length} array count closed form")
        COUNT.require(len(specs) + 1 == common.FROZEN_STORAGE[str(length)]["array_file_count"] + 1,
                      f"L{length} manifest-inclusive count")
        COUNT.require({row["q"] for row in specs if row["kind"] == "operator"} == set(range(length + 1)),
                      f"L{length} operator sector census")
        COUNT.require({(row["event"], row["q"]) for row in specs if row["kind"] == "admission"}
                      == {(event, q) for event in range(length) for q in range(1, event + 2)},
                      f"L{length} admission sector census")
        COUNT.require({(row["event"], row["q"]) for row in specs if row["kind"] == "lineage"}
                      == {(event, q) for event in range(length - 1) for q in range(event + 1)},
                      f"L{length} lineage sector census")
        rows[str(length)] = calculated
    COUNT.require(rows["12"]["state_cache_plus_reserve_bytes"] == 9_600_935_128, "L12 reserve arithmetic")
    COUNT.require(rows["12"]["maximum_q12_cache_plus_admission_bytes"] == 224_797_960, "L12 q12 mapping")
    COUNT.require(rows["12"]["terminal_mapping_bytes"] == 234_782_536, "L12 terminal mapping")
    COUNT.require(rows["12"]["authentication_peak_bytes"] == 252_944_080, "L12 auth peak")
    COUNT.require(rows["12"]["state_cache_plus_reserve_bytes"] < common.SCRATCH_LIMIT, "L12 scratch guard")
    return {"status": "PASS", "sizes": rows, "L12_manifest_inclusive_files": 339}


def adversarial_dual_gate() -> dict[str, object]:
    template = common.valid_dual_gate_template()
    common.validate_dual_gate_data(template)
    COUNT.require(True, "valid dual gate")
    mutations = []
    for label, mutate in (
        ("classification", lambda x: x.update(classification="PASS")),
        ("authorized_lengths", lambda x: x.update(authorized_lengths=[4, 6, 8, 10])),
        ("duplicate_role", lambda x: x["obstruction_records"][1].update(role="target")),
        ("obstruction_hash", lambda x: x["obstruction_records"][0].update(sha256="0" * 64)),
        ("obstruction_path", lambda x: x["obstruction_records"][0].update(path="../escape")),
        ("custody", lambda x: x["preserved_workspace_custody"].update(use="CONSUME")),
        ("consumer_pin", lambda x: x.update(consumer_sha256="0" * 64)),
        ("extra_key", lambda x: x.update(unfrozen=True)),
    ):
        bad = copy.deepcopy(template); mutate(bad)
        COUNT.refuses(lambda value=bad: common.validate_dual_gate_data(value), f"dual gate mutation accepted: {label}")
        mutations.append(label)
    return {"status": "PASS", "valid_cases": 1, "rejected_mutations": mutations}


def adversarial_manifest_census() -> dict[str, object]:
    length = 4
    specs = common.expected_specs(length)
    records = [dict(row, sha256="0" * 64) for row in specs]
    template = {"files": records, "array_file_count": len(records),
                "manifest_inclusive_file_count": len(records) + 1,
                "payload": common.FROZEN_STORAGE[str(length)]}
    common.validate_manifest_record_census(template, length)
    COUNT.require(True, "valid manifest census")
    mutations = []
    mutators = (
        ("extra", lambda x: x["files"].append(copy.deepcopy(x["files"][0]))),
        ("omission", lambda x: x["files"].pop()),
        ("reorder", lambda x: x["files"].__setitem__(slice(0, 2), list(reversed(x["files"][:2])))),
        ("path", lambda x: x["files"][0].update(path="../escape.u32")),
        ("dtype", lambda x: x["files"][0].update(dtype="<u8")),
        ("shape", lambda x: x["files"][0].update(shape=[2])),
        ("bytes", lambda x: x["files"][0].update(bytes=8)),
        ("hash", lambda x: x["files"][0].update(sha256="g" * 64)),
        ("total", lambda x: x.update(array_file_count=49)),
        ("payload", lambda x: x.update(payload={})),
    )
    for label, mutate in mutators:
        bad = copy.deepcopy(template); mutate(bad)
        COUNT.refuses(lambda value=bad: common.validate_manifest_record_census(value, length),
                      f"manifest mutation accepted: {label}")
        mutations.append(label)
    return {"status": "PASS", "valid_cases": 1, "rejected_mutations": mutations}


def stable_open_and_path_controls() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="v004r2-stable-open-") as temporary:
        root = Path(temporary)
        original = root / "member"
        original.write_bytes(b"authenticated")
        original.chmod(0o444)
        context = consumer.SecureCacheContext.__new__(consumer.SecureCacheContext)
        context.root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        context.fds = {}; context.fingerprints = {}
        fd = context._stable_open("member", len(b"authenticated"))
        before = consumer._fd_sha256(fd, len(b"authenticated"))
        replacement = root / "replacement"
        replacement.write_bytes(b"replacement!!")
        os.replace(replacement, original)
        after = consumer._fd_sha256(fd, len(b"authenticated"))
        COUNT.require(before == after, "stable fd changed after path replacement")
        context._verify_fd("member"); COUNT.require(True, "stable fingerprint")
        writable = root / "writable"; writable.write_bytes(b"x"); writable.chmod(0o644)
        COUNT.refuses(lambda: context._stable_open("writable", 1), "writable cache member accepted")
        symlink = root / "link"; symlink.symlink_to(original)
        COUNT.refuses(lambda: context._stable_open("link", len(b"replacement!!")), "symlink cache member accepted")
        os.close(fd); os.close(context.root_fd)
    COUNT.refuses(lambda: common.require_canonical(common.HERE / "elsewhere", common.cache_root(4), "cache"),
                  "noncanonical path accepted")
    return {"status": "PASS", "hash_then_replace_fd_stable": True,
            "writable_member_rejected": True, "symlink_member_rejected": True,
            "noncanonical_path_rejected": True}


def hard_lock_and_source_guards() -> dict[str, object]:
    gates = (common.DUAL_GATE, common.CONTROL_EXECUTION_GATE, common.CONTROL_GATE,
             common.L10_EXECUTION_GATE, common.L10_GATE, common.L12_EXECUTION_GATE)
    COUNT.require(all(not path.exists() for path in gates), "future successor gate exists at freeze")
    cache_root = common.cache_root(4)
    output = common.history_output(4)
    workspace = common.workspace_root(4)
    before = (cache_root.exists(), output.exists(), workspace.exists())
    built = subprocess.run([sys.executable, str(common.BUILDER), "--length", "4"],
                           cwd=common.HERE, text=True, capture_output=True, check=False)
    consumed = subprocess.run([sys.executable, str(common.CONSUMER), "execute", "--length", "4"],
                              cwd=common.HERE, text=True, capture_output=True, check=False)
    after = (cache_root.exists(), output.exists(), workspace.exists())
    COUNT.require(built.returncode == 2 and consumed.returncode == 2, "hard-lock return codes")
    COUNT.require(before == after == (False, False, False), "hard lock created payload/history/workspace")
    source = common.CONSUMER.read_text(encoding="utf-8")
    COUNT.require(source.index("started = time.perf_counter()") < source.index("common.validate_freeze()", source.index("def execute")),
                  "timer does not precede authentication")
    COUNT.require(source.index("if not passed:") < source.index("descriptor = os.open(output"),
                  "failed resource result can write physical output")
    COUNT.require("--output" not in source and "--workspace" not in source and "--cache-root" not in source,
                  "consumer exposes noncanonical CLI path")
    builder_source = common.BUILDER.read_text(encoding="utf-8")
    COUNT.require("--output" not in builder_source, "builder exposes noncanonical CLI path")
    return {"status": "PASS", "future_gate_absence_count": len(gates),
            "builder_returncode": built.returncode, "consumer_returncode": consumed.returncode,
            "cache_or_history_created": False, "timer_includes_authentication": True,
            "resource_failure_precedes_output_write": True}


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError("refuse to overwrite canonical V004R2 preflight result")
    result: dict[str, object] = {
        "schema": "HOSTILE_V004R2_STORAGE_CACHE_NONPHYSICAL_PREFLIGHT",
        "cache_payload_created": False, "physical_history_executed": False,
        "preserved_workspaces_consumed_or_mutated": False, "tests": {},
    }
    try:
        result["tests"] = {
            "freeze_syntax_dependencies": freeze_syntax_and_dependencies(),
            "exhaustive_rank_H_current": exhaustive_rank_and_hamiltonian(),
            "exact_storage_sector_census": exact_storage_and_sector_census(),
            "adversarial_dual_gate": adversarial_dual_gate(),
            "adversarial_manifest_census": adversarial_manifest_census(),
            "stable_open_path_controls": stable_open_and_path_controls(),
            "hard_lock_source_guards": hard_lock_and_source_guards(),
        }
        result["checks_passed"] = COUNT.value
        result["checks_total"] = COUNT.value
        result["classification"] = "PASS_V004R2_NONPHYSICAL_PREFLIGHT__ALL_CACHE_AND_HISTORY_MODES_LOCKED"
    except Exception as error:
        result["checks_passed"] = max(0, COUNT.value - 1)
        result["checks_total"] = COUNT.value
        result["classification"] = "FAIL_V004R2_NONPHYSICAL_PREFLIGHT"
        result["error"] = f"{type(error).__name__}: {error}"
    descriptor = os.open(OUTPUT, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0 if result["classification"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
