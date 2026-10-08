"""Rerun an interrupted small diagnostic with JSON scalar conversion only."""
import hashlib
import json
from pathlib import Path

import numpy as np
import dust_clock_local_poles_v001 as original

HERE = Path(__file__).resolve().parent
SOURCE_SHA = '6a6cf2d38c3c9f59dc82a1329082348705480b65273676cc41311f2b487dcef6'
PARTIAL_SHA = 'aa2c47d787de77e3673d60da4856305725ff92b60e4b86282ea25ea954bd110d'


def convert(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f'Unexpected JSON type: {type(value).__name__}')


class ScalarJSON:
    @staticmethod
    def dump(value, handle, **options):
        value['serialization_repair'] = dict(
            original_source_sha256=SOURCE_SHA,
            preserved_partial_sha256=PARTIAL_SHA,
            repair_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            changes='Output path and NumPy-to-Python JSON scalar conversion only')
        return json.dump(value, handle, default=convert, **options)

    @staticmethod
    def dumps(value, **options):
        return json.dumps(value, default=convert, **options)


if __name__ == '__main__':
    assert hashlib.sha256(Path(original.__file__).read_bytes()).hexdigest() == SOURCE_SHA
    assert hashlib.sha256(original.OUTPUT.read_bytes()).hexdigest() == PARTIAL_SHA
    original.OUTPUT = HERE/'DUST_CLOCK_LOCAL_POLES_V002_RESULT.json'
    original.json = ScalarJSON
    original.main()
