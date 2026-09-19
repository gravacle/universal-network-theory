#!/usr/bin/env python3
"""Draft V004R4 immutable cache-array opening primitive.

This module is control-plane/storage code only.  It deliberately contains no
history evolution.  A zero-byte record is represented by an ordinary,
read-only ndarray because NumPy cannot memory-map an empty file.  Every
nonempty record remains a read-only mapping of a duplicated, already-held
descriptor.
"""

from __future__ import annotations

import math
import os
import stat
from typing import Any

import numpy as np


class Refusal(RuntimeError):
    """The descriptor or manifest record failed an exact storage check."""


def _shape(value: Any) -> tuple[int, ...]:
    if not isinstance(value, list) or any(type(axis) is not int or axis < 0 for axis in value):
        raise Refusal("cache record shape is not an exact nonnegative integer list")
    return tuple(value)


def open_immutable_array(
    descriptor: int,
    record: dict[str, Any],
    expected_dtype: np.dtype[Any] | str,
    expected_identity: tuple[int, int, int, int],
) -> np.ndarray:
    """Open one exact record without mapping an empty descriptor.

    ``expected_identity`` is the mandatory stable-open fingerprint
    ``(st_dev, st_ino, st_size, st_mtime_ns)`` captured when descriptor custody
    began.
    """

    if type(descriptor) is not int or descriptor < 0:
        raise Refusal("cache descriptor is invalid")
    if (not isinstance(expected_identity, tuple) or len(expected_identity) != 4
            or any(type(value) is not int for value in expected_identity)):
        raise Refusal("cache descriptor fingerprint is invalid")
    if not isinstance(record, dict):
        raise Refusal("cache record is not an object")
    dtype = np.dtype(expected_dtype)
    if record.get("dtype") != dtype.str:
        raise Refusal("cache record dtype mismatch")
    shape = _shape(record.get("shape"))
    byte_count = record.get("bytes")
    if type(byte_count) is not int or byte_count < 0:
        raise Refusal("cache record byte count is invalid")
    if byte_count != math.prod(shape) * dtype.itemsize:
        raise Refusal("cache record shape/dtype/byte identity mismatch")

    metadata = os.fstat(descriptor)
    identity = (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns)
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & 0o222:
        raise Refusal("cache descriptor is non-ordinary or writable")
    if metadata.st_size != byte_count:
        raise Refusal("cache descriptor byte size mismatch")
    if identity != expected_identity:
        raise Refusal("cache descriptor identity drift")

    if byte_count == 0:
        array = np.empty(shape, dtype=dtype)
        array.flags.writeable = False
        return array

    with os.fdopen(os.dup(descriptor), "rb", closefd=True) as stream:
        array = np.memmap(stream, dtype=dtype, mode="r", shape=shape)
    if array.nbytes != byte_count or array.flags.writeable:
        raise Refusal("nonempty cache mapping identity/writeability mismatch")
    return array
