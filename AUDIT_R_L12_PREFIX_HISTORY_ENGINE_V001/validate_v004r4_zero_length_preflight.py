#!/usr/bin/env python3
"""Isolated nonphysical V004R4 zero-length descriptor regression."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest import mock

import numpy as np

import v004r4_cache_io as cache_io


def _create(root_fd: int, name: str, payload: bytes) -> int:
    descriptor = os.open(
        name,
        os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o400,
        dir_fd=root_fd,
    )
    if payload:
        cursor = 0
        while cursor < len(payload):
            written = os.write(descriptor, payload[cursor:])
            if written <= 0:
                raise RuntimeError("short temporary descriptor write")
            cursor += written
    os.fsync(descriptor)
    os.fchmod(descriptor, 0o444)
    return descriptor


def _fingerprint(descriptor: int) -> tuple[int, int, int, int]:
    metadata = os.fstat(descriptor)
    return metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns


def _refuses(function) -> bool:
    try:
        function()
    except (cache_io.Refusal, ValueError):
        return True
    return False


def run() -> dict[str, object]:
    checks: list[str] = []

    def require(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)
        checks.append(label)

    with tempfile.TemporaryDirectory(prefix="v004r4-zero-length-") as temporary:
        root = Path(temporary)
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        descriptors: list[int] = []
        try:
            empty_fd = _create(root_fd, "q_00_sources.i32", b"")
            nonempty_values = np.asarray([7, 11], dtype="<i4")
            nonempty_fd = _create(root_fd, "q_01_sources.i32", nonempty_values.tobytes())
            malformed_fd = _create(root_fd, "malformed_empty.i32", b"\x00\x00\x00\x00")
            descriptors.extend((empty_fd, nonempty_fd, malformed_fd))

            empty_record = {
                "path": "q_00_sources.i32", "dtype": "<i4", "shape": [0],
                "bytes": 0, "kind": "operator", "q": 0, "role": "sources",
            }
            with mock.patch.object(np, "memmap", side_effect=AssertionError("mapped empty descriptor")):
                empty = cache_io.open_immutable_array(
                    empty_fd, empty_record, np.dtype("<i4"), _fingerprint(empty_fd)
                )
            require(type(empty) is np.ndarray, "zero record is ordinary ndarray")
            require(not isinstance(empty, np.memmap), "zero record is not memmap")
            require(empty.shape == (0,) and empty.nbytes == 0, "zero record exact shape/bytes")
            require(empty.dtype.str == "<i4", "zero record exact dtype")
            require(empty.flags.writeable is False, "zero record is immutable")
            require(_refuses(lambda: empty.__setitem__(slice(None), 1)), "zero record rejects writes")

            nonempty_record = dict(empty_record, path="q_01_sources.i32", shape=[2], bytes=8, q=1)
            mapped = cache_io.open_immutable_array(
                nonempty_fd, nonempty_record, np.dtype("<i4"), _fingerprint(nonempty_fd)
            )
            require(isinstance(mapped, np.memmap), "nonempty record remains descriptor memmap")
            require(mapped.flags.writeable is False, "nonempty mapping is immutable")
            require(np.array_equal(mapped, nonempty_values), "nonempty mapping exact contents")
            cache_mapping = getattr(mapped, "_mmap", None)
            if cache_mapping is not None:
                cache_mapping.close()

            require(_refuses(lambda: cache_io.open_immutable_array(
                malformed_fd, empty_record, np.dtype("<i4"), _fingerprint(malformed_fd)
            )), "zero record rejects nonzero descriptor")
            require(_refuses(lambda: cache_io.open_immutable_array(
                empty_fd, dict(empty_record, shape=[1]), np.dtype("<i4"), _fingerprint(empty_fd)
            )), "zero record rejects nonzero logical shape")
            require(_refuses(lambda: cache_io.open_immutable_array(
                empty_fd, empty_record, np.dtype("<u4"), _fingerprint(empty_fd)
            )), "zero record rejects dtype mismatch")
            drift = list(_fingerprint(empty_fd)); drift[-1] += 1
            require(_refuses(lambda: cache_io.open_immutable_array(
                empty_fd, empty_record, np.dtype("<i4"), tuple(drift)
            )), "zero record rejects descriptor drift")
            require(_refuses(lambda: cache_io.open_immutable_array(
                empty_fd, empty_record, np.dtype("<i4"), (0, 0, 0)
            )), "zero record rejects malformed descriptor fingerprint")
        finally:
            for descriptor in descriptors:
                os.close(descriptor)
            os.close(root_fd)

    return {
        "schema": "HOSTILE_V004R4_ZERO_LENGTH_DESCRIPTOR_PREFLIGHT_V001",
        "classification": "PASS_ZERO_LENGTH_ORDINARY_IMMUTABLE__NONEMPTY_DESCRIPTOR_MEMMAP",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "cache_payload_created": False,
        "physical_history_executed": False,
        "claim_boundary": "STORAGE_DESCRIPTOR_COMPATIBILITY_ONLY__NO_HISTORY_SPECTRUM_CONTINUUM_OR_GRAVITY",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
