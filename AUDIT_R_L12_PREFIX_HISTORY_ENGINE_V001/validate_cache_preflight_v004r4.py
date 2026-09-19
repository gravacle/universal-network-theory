#!/usr/bin/env python3
"""Nonphysical frozen-source and storage preflight for hostile V004R4.

This executable performs only deterministic source, combinatorial, cache-layout,
and refusal checks.  It cannot build a cache or execute a physical history.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import math
import os
import stat
import sys
from pathlib import Path

import numpy as np

import build_cache_v004r4 as builder
import consume_cache_v004r4 as contract
import independent_prefix_history as physical
import independent_prefix_history_v003 as v3
import validate_v004r4_zero_length_preflight as zero_length


OUTPUT = contract.PREFLIGHT_RESULT
SUPPORTED = (4, 6, 8, 10, 12)
EXPECTED_STORAGE = {
    4: (6_076, 3_360, 50, 2_808, 2_956),
    6: (118_408, 128_128, 98, 47_000, 50_176),
    8: (2_333_420, 5_116_320, 162, 807_864, 867_436),
    10: (44_508_856, 209_969_760, 242, 13_818_936, 14_874_736),
    12: (826_221_912, 8_773_664_640, 338, 234_782_536, 252_944_080),
}
FORBIDDEN = (
    contract.HERE / "CACHE_BUILD_AUTHORIZATION_GATE_V004R4.json",
    contract.HERE / "CACHED_L10_GATE_V004R4.json",
    contract.HERE / "HOSTILE_POSTBUILD_PAYLOAD_AUDIT_V004R4.json",
    contract.HERE / "HOSTILE_L12_EXECUTION_GATE_V004R4.json",
    contract.HERE / "V004R4_CACHE_PAYLOADS",
    contract.HERE / "V004R4_WORKSPACES",
    contract.HERE / "V004R4_PHYSICAL_OUTPUTS",
    contract.SHARED,
)


class Counter:
    def __init__(self) -> None:
        self.groups: dict[str, int] = {}

    def require(self, group: str, condition: bool, label: str) -> None:
        self.groups[group] = self.groups.get(group, 0) + 1
        if not condition:
            raise contract.Refusal(label)


def source_packet(
    counter: Counter, custody: contract.AuthorityCustody,
) -> tuple[dict[str, object], dict[str, str], str]:
    freeze, hashes, freeze_hash = builder.read_frozen_sources(custody)
    expected_sources = {
        contract.METHOD.name: contract.METHOD,
        contract.BUILDER.name: contract.BUILDER,
        contract.CONSUMER.name: contract.CONSUMER,
        Path(__file__).name: contract.PREFLIGHT,
        **contract.EXECUTED_DEPENDENCIES,
    }
    counter.require(
        "frozen_sources", set(hashes) == set(expected_sources),
        "frozen source census mismatch",
    )
    for name, path in expected_sources.items():
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        counter.require("frozen_sources", hashes.get(name) == freeze["files"].get(name),
                        f"frozen source mismatch: {name}")
    return freeze, hashes, freeze_hash


def absence_screen(counter: Counter) -> None:
    counter.require("absence", not OUTPUT.exists() and not OUTPUT.is_symlink(),
                    "refuse to overwrite V004R4 preflight result")
    for path in FORBIDDEN:
        counter.require("absence", not path.exists() and not path.is_symlink(),
                        f"prepayload artifact exists before preflight: {path}")


def independently_reconstructed_specs(length: int) -> list[dict[str, object]]:
    specs: list[dict[str, object]] = []
    edges = 3 * length
    for q in range(length + 1):
        words = math.comb(2 * length, q)
        pairs = edges * (math.comb(2 * length - 2, q - 1) if q else 0)
        specs.extend([
            {"path": f"q_{q:02d}_words.u32", "dtype": "<u4", "shape": [words],
             "bytes": 4 * words, "kind": "operator", "q": q, "role": "words"},
            {"path": f"q_{q:02d}_offsets.u64", "dtype": "<u8", "shape": [edges + 1],
             "bytes": 8 * (edges + 1), "kind": "operator", "q": q, "role": "offsets"},
        ])
        if q:
            for role in ("sources", "targets"):
                specs.append({
                    "path": f"q_{q:02d}_{role}.i32", "dtype": "<i4", "shape": [pairs],
                    "bytes": 4 * pairs, "kind": "operator", "q": q, "role": role,
                })
    for event in range(length):
        for q in range(1, event + 2):
            count = math.comb(2 * length - 1, q - 1)
            for role in ("occupied", "old"):
                specs.append({
                    "path": f"event_{event:02d}_q_{q:02d}_{role}.i32",
                    "dtype": "<i4", "shape": [count], "bytes": 4 * count,
                    "kind": "admission", "event": event, "q": q, "role": role,
                })
    for event in range(length - 1):
        for q in range(event + 1):
            count = math.comb(event, q)
            for role in ("same", "added"):
                specs.append({
                    "path": f"prefix_{event:02d}_q_{q:02d}_{role}.i32",
                    "dtype": "<i4", "shape": [count], "bytes": 4 * count,
                    "kind": "lineage", "event": event, "q": q, "role": role,
                })
    return specs


def storage_screen(counter: Counter) -> None:
    for length in SUPPORTED:
        specs = contract.cache_specs(length)
        census = contract.storage_census(length)
        actual, state, files, terminal, authentication = EXPECTED_STORAGE[length]
        counter.require("storage", specs == independently_reconstructed_specs(length),
                        f"L={length} independent cache-spec disagreement")
        counter.require("storage", len(specs) == files, f"L={length} file census")
        counter.require("storage", sum(int(row["bytes"]) for row in specs) == actual,
                        f"L={length} cache bytes")
        counter.require("storage", census["maximum_live_state_bytes"] == state,
                        f"L={length} state bytes")
        counter.require("storage", census["terminal_mapping_bytes"] == terminal,
                        f"L={length} terminal mapping")
        counter.require("storage", census["authentication_peak_bytes"] == authentication,
                        f"L={length} authentication peak")
        counter.require(
            "storage",
            census["state_cache_plus_reserve_bytes"]
            == state + actual + contract.OVERHEAD_RESERVE,
            f"L={length} scratch arithmetic",
        )


def index_screen(counter: Counter) -> None:
    for width in range(13):
        for q in range(width + 1):
            words = physical.reverse_masks(width, q)
            counter.require("rank", len(words) == math.comb(width, q),
                            f"width={width},q={q} basis census")
            for index, word in enumerate(words):
                counter.require(
                    "rank", v3.reverse_rank(width, q, int(word)) == index,
                    f"width={width},q={q},index={index} reverse-rank identity",
                )

    rng = np.random.default_rng(14_441_248)
    edges = physical.hostile_edges(4)
    for q in range(5):
        words, offsets, sources, targets = builder.operator_arrays(4, q, edges)
        direct = physical.CarrierBlock(4, q, edges)
        cached = contract.r2consumer.legacy.CachedCarrier(
            4, q, edges, words, offsets, sources, targets,
        )
        counter.require("operator", np.array_equal(words, direct.words.astype("<u4")),
                        f"q={q} hostile word order")
        counter.require("operator", offsets[-1] == len(sources) == len(targets),
                        f"q={q} operator pair census")
        vector = rng.normal(size=(2, len(words))) + 1j * rng.normal(size=(2, len(words)))
        counter.require("operator", np.array_equal(cached.multiply(vector), direct.multiply(vector)),
                        f"q={q} exact Hamiltonian differential")
        counter.require("operator", np.array_equal(cached.currents(vector), direct.currents(vector)),
                        f"q={q} exact current differential")


def descriptor_screen(counter: Counter) -> None:
    result = zero_length.run()
    counter.require(
        "descriptor",
        result.get("classification")
        == "PASS_ZERO_LENGTH_ORDINARY_IMMUTABLE__NONEMPTY_DESCRIPTOR_MEMMAP",
        "zero-length descriptor classification",
    )
    counter.require("descriptor", result.get("checks_passed") == result.get("checks_total"),
                    "zero-length descriptor checks")
    counter.require("descriptor", result.get("cache_payload_created") is False,
                    "zero-length descriptor created cache")
    counter.require("descriptor", result.get("physical_history_executed") is False,
                    "zero-length descriptor executed history")


def publish(record: dict[str, object], custody: contract.AuthorityCustody) -> str:
    """Publish through the same retained-parent, no-clobber primitive as a history."""
    return contract.atomic_publish(OUTPUT, record, custody)


def run(*, write: bool) -> dict[str, object]:
    counter = Counter()
    custody = contract.AuthorityCustody()
    try:
        freeze, hashes, freeze_hash = source_packet(counter, custody)
        absence_screen(counter)
        storage_screen(counter)
        index_screen(counter)
        descriptor_screen(counter)
        files = {
            "method_sha256": hashes[contract.METHOD.name],
            "builder_sha256": hashes[contract.BUILDER.name],
            "consumer_sha256": hashes[contract.CONSUMER.name],
            "preflight_sha256": hashes[contract.PREFLIGHT.name],
            "freeze_sha256": freeze_hash,
        }
        record: dict[str, object] = {
            "schema": "HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT_V001",
            "classification": "PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT",
            "files": files,
            "checks": counter.groups,
            "checks_passed": sum(counter.groups.values()),
            "checks_total": sum(counter.groups.values()),
            "failures": [],
            "cache_payload_created": False,
            "physical_history_executed": False,
            "claim_boundary": "NONPHYSICAL_V004R4_PREFLIGHT_ONLY__NO_CACHE_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
        }
        contract.canonical_json_bytes(record)
        if write:
            digest = publish(record, custody)
            print(f"PASS_HOSTILE_V004R4_NONPHYSICAL_PREFLIGHT sha256={digest}")
        return record
    finally:
        custody.close()


def self_test() -> None:
    for length, expected in EXPECTED_STORAGE.items():
        census = contract.storage_census(length)
        if contract.cache_specs(length) != independently_reconstructed_specs(length):
            raise contract.Refusal(f"L={length} preflight cache-spec self-test")
        observed = (
            census["actual_cache_array_bytes"],
            census["maximum_live_state_bytes"],
            census["array_file_count"],
            census["terminal_mapping_bytes"],
            census["authentication_peak_bytes"],
        )
        if observed != expected:
            raise contract.Refusal(f"L={length} preflight frozen census self-test")
    descriptor = zero_length.run()
    if descriptor["checks_passed"] != descriptor["checks_total"]:
        raise contract.Refusal("zero-length preflight self-test")
    print("PASS_V004R4_PREFLIGHT_SOURCE_SELF_TEST")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("run", "self-test"))
    arguments = parser.parse_args()
    try:
        if arguments.mode == "self-test":
            self_test()
        else:
            run(write=True)
        return 0
    except (AssertionError, KeyError, OSError, TypeError, ValueError, contract.Refusal) as error:
        print(f"REFUSE: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
