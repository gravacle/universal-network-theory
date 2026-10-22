"""Independent classifier-B input primitives. Preparation only; not a classifier.
No production inputs, automatic traversal, or CLI entry point.
"""
import hashlib
import json
import math
import re

class InputDefect(ValueError):
    pass

def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputDefect("DUPLICATE_KEY")
        result[key] = value
    return result

def _constant(value):
    raise InputDefect("NONFINITE_NUMBER")

def _float(value):
    result = float(value)
    if not math.isfinite(result):
        raise InputDefect("NONFINITE_NUMBER")
    return result

def parse_json(raw):
    if not isinstance(raw, bytes):
        raise InputDefect("BYTES_REQUIRED")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_object,
                          parse_constant=_constant, parse_float=_float)
    except (UnicodeError, ValueError, RecursionError) as error:
        if isinstance(error, InputDefect):
            raise
        raise InputDefect("JSON_SYNTAX") from error

def parse_pinned_json(raw, expected_sha256):
    # Verify original bytes before decoding or parsing. No filesystem access.
    if not isinstance(raw, bytes):
        raise InputDefect("BYTES_REQUIRED")
    if not isinstance(expected_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise InputDefect("PIN_FORMAT")
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise InputDefect("SHA256_MISMATCH")
    return parse_json(raw)

def canonical_json(value):
    try:
        return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
    except (TypeError, ValueError, RecursionError) as error:
        raise InputDefect("OUTPUT_NOT_JSON") from error
