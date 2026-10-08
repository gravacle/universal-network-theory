"""Additive JSON scalar repair; all V001 numerical methods are reused."""
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import common_history_phase_mean_v001 as base

original_law = base.law
original_sources = base.sources
original_freeze = base.FREEZE
assert json.loads(original_freeze.read_text())['files'] == original_sources()


def normalize(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {k: normalize(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(v) for v in value]
    return value


def sources():
    result = original_sources()
    for path in (Path(__file__), original_freeze,
                 base.ROOT/'COMMON_HISTORY_PHASE_MEAN_V001_FAILURE.md'):
        result[str(path)] = original_law.sha(path)
    return result


base.law = SimpleNamespace(sha=original_law.sha, SHAPE_PATH=original_law.SHAPE_PATH,
    encode=lambda value: original_law.encode(normalize(value)),
    save_new=lambda path, value: original_law.save_new(path, normalize(value)))
base.sources = sources
base.FREEZE = base.ROOT/'COMMON_HISTORY_PHASE_MEAN_V002_FROZEN.json'
base.OUTPUT = base.ROOT/'COMMON_HISTORY_PHASE_MEAN_V002_RESULTS.json'

if __name__ == '__main__':
    base.main()
