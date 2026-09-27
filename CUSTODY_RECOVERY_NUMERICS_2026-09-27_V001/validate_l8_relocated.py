#!/usr/bin/env python3
"""Run the unchanged historical L8 validator with a strictly bounded Path adapter.

Only its eight authenticated historical precursor filenames are mapped. The
historical JSON and Python files are never edited or reserialized. No evolution
is performed; the original validator recomputes the exact permutation statistic.
"""
import json
import math
from pathlib import Path
import types

import numpy as np

from restore_l8_manifest import (ROOT, FREEZE, FREEZE_SHA, authenticated_bytes,
                                 require, safe_path)

VALIDATOR = "DEVELOPMENT_R_L8_LINEAGE_ORDER_OLLIVIER_RICCI_V001/validate_result.py"
VALIDATOR_SHA = "f39e36e435aa9b51b5b752168f58760a2ea67bab436c65b57aef17767aa39f31"
HISTORY = "DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/PHYSICAL_OUTPUTS/HISTORY_L8.json"
HISTORY_SHA = "ff55ddd70c3f5e3664e1a61384f211a86e9fcc5bcec2d7e02251d387bd17c786"
PREFIX = "/Users/brianmulconrey/PerInfo/where-atoms-come-from/audited-386ee2c/"

def strict_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result

def strict_json(data):
    def reject(value):
        raise ValueError("nonfinite JSON: " + value)
    return json.loads(data, object_pairs_hook=strict_object, parse_constant=reject)

def relocation_map(root):
    history = strict_json(authenticated_bytes(safe_path(root, HISTORY), HISTORY_SHA))
    records = history["terminal_shards"]
    require([record["q"] for record in records] == list(range(8)), "L8 q census")
    mapped = {}
    for q, record in enumerate(records):
        suffix = ("DEVELOPMENT_R_L12_TARGET_STORAGE_CACHE_V012/WORKSPACES/L8/sharp/"
                  "prefix_07/q_%02d.npy" % q)
        require(record["path"] == PREFIX + suffix, "historical exact prefix/suffix mismatch")
        require(record["shape"] == [math.comb(7, q), math.comb(16, q)], "shape binding")
        local = safe_path(root, suffix)
        raw = authenticated_bytes(local, record["sha256"])
        require(len(raw) == record["bytes"], "shard byte count")
        with local.open("rb") as stream:
            version = np.lib.format.read_magic(stream)
            require(version == (1, 0), "NPY format version")
            shape, fortran, dtype = np.lib.format.read_array_header_1_0(stream)
            require(list(shape) == record["shape"] and not fortran and dtype.str == "<c16",
                    "NPY shape/dtype/order")
            require(len(raw) == stream.tell() + math.prod(shape) * dtype.itemsize,
                    "NPY payload byte census")
        authenticated_bytes(local, record["sha256"])
        mapped[record["path"]] = local
    return mapped

def mapped_path(value, mapping):
    require(isinstance(value, str) and value in mapping, "unregistered historical path")
    return mapping[value]

def load_validator(root=ROOT):
    path = safe_path(root, VALIDATOR)
    source = authenticated_bytes(path, VALIDATOR_SHA)
    freeze = strict_json(authenticated_bytes(safe_path(root, FREEZE), FREEZE_SHA))
    require(freeze["inputs"]["history"] == {"path": HISTORY, "sha256": HISTORY_SHA},
            "frozen history binding")
    # Preflight every dependency and shard before executing the frozen source.
    inputs = [freeze["inputs"][name] for name in ("history", "cache_manifest", "joint_witness")]
    inputs += freeze["inputs"]["representation_sources"]
    for item in inputs:
        authenticated_bytes(safe_path(root, item["path"]), item["sha256"])
    mapping = relocation_map(root)
    module = types.ModuleType("unt_frozen_l8_curvature_validator")
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    # In the authenticated source this symbol is used during validation only
    # for the eight historical filenames in expected_shards. ROOT/HERE/RESULT
    # were already constructed with the original pathlib.Path at module load.
    module.Path = lambda value: mapped_path(value, mapping)
    return module

def run():
    validator = load_validator()
    count = validator.validate(validator.read_json(validator.RESULT))
    relocation_map(ROOT)  # post-use raw digest/shape recheck
    authenticated_bytes(safe_path(ROOT, VALIDATOR), VALIDATOR_SHA)
    return {"status": "PASS_HISTORICAL_L8_VALIDATOR_WITH_EXACT_PATH_ADAPTER",
            "checks": count, "shards": 8, "historical_validator_sha256": VALIDATOR_SHA,
            "new_evolution": False, "historical_bytes_modified": False}

if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, AssertionError) as error:
        print(json.dumps({"status": "REFUSED", "error": str(error)}, sort_keys=True))
        raise SystemExit(1)
