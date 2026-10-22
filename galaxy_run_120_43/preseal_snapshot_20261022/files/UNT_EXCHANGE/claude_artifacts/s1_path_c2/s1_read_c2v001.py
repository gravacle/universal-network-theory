"""S1 reading tool (s1_path_c2, c2v001). Target-free: it reads DDO154 model speeds only.

Loads s1_path_lib_c2v001.py from this folder by its sha256 and refuses on any mismatch. Computes the registered
statistic and reading (registration sections 5-8) from the two S1 results and the campaign's u_A result (K4'), reusing
the compare-of-record functions by sha (the manifest names the compare pin). Prints the reading; with --write-dir it
writes S1_READING_<theta16>.json there by exclusive create. Starts no process.
  --manifest P@S [--write-dir DIR]
Exit 0: a reading was computed (any code); 3: refused (an input is missing or does not bind; nothing is written).
"""
import argparse
import hashlib
import json
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE / 's1_path_lib_c2v001.py'
LIB_SHA = 'b461ac36f9f9124cc74992a469f74ed2b0d39de63fd6a551b7e0b73f4cd027bb'


def lib():
    raw = LIB.read_bytes()
    if hashlib.sha256(raw).hexdigest() != LIB_SHA:
        print(json.dumps({'refused': 'LIB_BYTES_CHANGED'}))
        raise SystemExit(3)
    m = types.ModuleType('s1_path_lib_c2v001')
    m.__file__ = str(LIB)
    exec(compile(raw, str(LIB), 'exec'), m.__dict__)
    return m


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--write-dir')
    a = ap.parse_args(argv)
    L = lib()
    path, _, sha = a.manifest.rpartition('@')
    try:
        out = L.read_reading({'path': path, 'sha256': sha}, write_dir=a.write_dir)
    except L.Refusal as exc:
        print(json.dumps({'refused': exc.code, 'detail': None if exc.detail is None else str(exc.detail)[:500]}))
        return 3
    print(json.dumps({k: out.get(k) for k in ('code', 'sub_code', 'label', 'step5_effect', 'next_step', 'statistic',
                                              'theta_key', 'written')}, indent=1, sort_keys=True, default=str))
    return 0


if __name__ == '__main__':
    sys.exit(main())
