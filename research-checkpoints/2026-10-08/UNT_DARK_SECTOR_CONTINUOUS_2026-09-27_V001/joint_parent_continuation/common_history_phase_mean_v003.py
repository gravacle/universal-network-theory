"""Complete the scalar-only repair for both saved JSON and console output."""
import json
from pathlib import Path
from types import SimpleNamespace
import common_history_phase_mean_v002 as repaired

base = repaired.base
parent_sources = base.sources
parent_freeze = base.FREEZE
assert json.loads(parent_freeze.read_text())['files'] == parent_sources()


def sources():
    result = parent_sources()
    for path in (Path(__file__), parent_freeze,
                 base.ROOT/'COMMON_HISTORY_PHASE_MEAN_V002_PUBLICATION_NOTE.md'):
        result[str(path)] = repaired.original_law.sha(path)
    return result


base.json = SimpleNamespace(loads=json.loads,
    dumps=lambda value, **kwargs: json.dumps(repaired.normalize(value), **kwargs))
base.sources = sources
base.FREEZE = base.ROOT/'COMMON_HISTORY_PHASE_MEAN_V003_FROZEN.json'
base.OUTPUT = base.ROOT/'COMMON_HISTORY_PHASE_MEAN_V003_RESULTS.json'

if __name__ == '__main__':
    base.main()
