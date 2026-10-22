"""S1 reading tool (s1_successors_c2, c2v002c). Target-free: it reads DDO154 model speeds only.

Loads s1_path_lib_c2v002c.py from this folder by its sha256 and refuses on any mismatch (c2v002c changes only this pin). Computes the registered
statistic and reading (registration sections 5-8) from the two S1 results and the campaign's u_A result (K4'), reusing
the functions of a REVIEWED compare of record only (r11 a5d10cb1 or r14 f3f9ba7e; default r14). Prints the reading; with
--write-dir it writes S1_READING_<theta16>.json there by exclusive create. Starts no process.
  --manifest P@S [--write-dir DIR]
c2v002a (BLK-1): the manifest's fill record is replayed first (u_A re-bound to the Phase-1 primary anchor, both specs
replayed, the C3T slots re-looked up, branch / theta_key / physical_u_A and every consumed field re-derived).
Exit 0: a reading was computed (any code); 3: refused (an input is missing or does not bind, including a fill record
that does not replay, or an internal error; nothing is written).
"""
import argparse
import hashlib
import json
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE / 's1_path_lib_c2v002c.py'
LIB_SHA = '99e2be175e546992c70984435bc480e1eddb90b052fda65ddcbfe8780bdbd27e'


def lib():
    raw = LIB.read_bytes()
    if hashlib.sha256(raw).hexdigest() != LIB_SHA:
        print(json.dumps({'refused': 'LIB_BYTES_CHANGED'}))
        raise SystemExit(3)
    m = types.ModuleType('s1_path_lib_c2v002c')
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
    except Exception as exc:                                             # note 6: never a traceback without a code
        print(json.dumps({'refused': 'INTERNAL_ERROR', 'stage': 'read', 'detail': ('%s: %s' % (type(exc).__name__, exc))[:500]}))
        return 3
    print(json.dumps({k: out.get(k) for k in ('code', 'sub_code', 'label', 'step5_effect', 'next_step', 'statistic',
                                              'theta_key', 'written')}, indent=1, sort_keys=True, default=str))
    return 0


if __name__ == '__main__':
    sys.exit(main())
