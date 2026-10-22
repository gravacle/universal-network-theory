"""S1 template CLI for root (s1_successors_c2, c2v002a): fill | dry-plan | plan.

Loads s1_path_lib_c2v002a.py from this folder by its sha256 and refuses on any mismatch. c2v002a changes only the
library pin (BLK-1: the library's replay re-derives every consumed fill-record field). Writes only the named outputs,
by exclusive create; dry-plan writes nothing. Starts no process. Pins are given as PATH@SHA256.
  fill      --u-a P@S --base-spec P@S --campaign-config P@S --c3t-registry P@S --out-dir DIR
  dry-plan  --u-a P@S --base-spec P@S --campaign-config P@S [--c3t-registry P@S]
  plan      --fill-record P@S --case S1_UA_C3T|S1_UA_C4T --prelaunch P@S [--params P@S] [--attempt N] [--overlap]
            --out PATH [--dry]
  c3t-cp1-spec --u-a P@S --base-spec P@S --campaign-config P@S (--out-dir DIR | --dry)
            the S1_UA_C3T spec in CP-1's input form (certificate slots PENDING), for the CP-1 point extension
The u_A point file pins the Phase-1 snapshot (phase1_snapshot); --c3t-registry is the certificate registry that holds
point_identity(S1_UA_C3T) (note 10). --overlap writes guard012's S1 overlap admission fields into the plan sidecar.
Exit 0: done; 3: refused (the code is printed; an unexpected error prints INTERNAL_ERROR).
"""
import argparse
import hashlib
import json
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE / 's1_path_lib_c2v002a.py'
LIB_SHA = 'f961839b2dd1ef27c6225badedcc199db3f6515776b5e7e5c08ecede3e769a9e'


def lib():
    raw = LIB.read_bytes()
    if hashlib.sha256(raw).hexdigest() != LIB_SHA:
        print(json.dumps({'refused': 'LIB_BYTES_CHANGED'}))
        raise SystemExit(3)
    m = types.ModuleType('s1_path_lib_c2v002a')
    m.__file__ = str(LIB)
    exec(compile(raw, str(LIB), 'exec'), m.__dict__)
    return m


def pin(s):
    if s is None:
        return None
    path, _, sha = s.rpartition('@')
    return {'path': path, 'sha256': sha}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('fill', 'dry-plan'):
        p = sub.add_parser(name, allow_abbrev=False)
        for a in ('--u-a', '--base-spec', '--campaign-config'):
            p.add_argument(a, required=True)
        p.add_argument('--c3t-registry', required=(name == 'fill'))
        if name == 'fill':
            p.add_argument('--out-dir', required=True)
    c = sub.add_parser('c3t-cp1-spec', allow_abbrev=False)
    for a in ('--u-a', '--base-spec', '--campaign-config'):
        c.add_argument(a, required=True)
    c.add_argument('--out-dir')
    c.add_argument('--dry', action='store_true')
    p = sub.add_parser('plan', allow_abbrev=False)
    p.add_argument('--fill-record', required=True)
    p.add_argument('--case', required=True)
    p.add_argument('--prelaunch')
    p.add_argument('--params')
    p.add_argument('--attempt', type=int, default=1)
    p.add_argument('--overlap', action='store_true')
    p.add_argument('--out')
    p.add_argument('--dry', action='store_true')
    a = ap.parse_args(argv)
    L = lib()
    try:
        if a.cmd == 'c3t-cp1-spec':
            print(json.dumps(L.write_c3t_cp1_spec(pin(a.u_a), pin(a.base_spec), pin(a.campaign_config), out_dir=a.out_dir,
                                                  dry=a.dry), indent=1, sort_keys=True))
        elif a.cmd in ('fill', 'dry-plan'):
            rec = L.fill(pin(a.u_a), pin(a.base_spec), pin(a.campaign_config), c3t_registry=pin(a.c3t_registry),
                         out_dir=getattr(a, 'out_dir', None), dry=(a.cmd == 'dry-plan'))
            print(json.dumps(rec, indent=1, sort_keys=True))
        else:
            r = L.make_plan(pin(a.fill_record), a.case, pin(a.prelaunch), params_ref=pin(a.params), attempt=a.attempt,
                            out_path=a.out, dry=a.dry, overlap=a.overlap)
            print(json.dumps({'sidecar': r['sidecar'], 'written': r['written'], 'plan': r['plan']}, indent=1, sort_keys=True))
            if not a.dry and r['written'] is None:
                return 3
        return 0
    except L.Refusal as exc:
        print(json.dumps({'refused': exc.code, 'detail': None if exc.detail is None else str(exc.detail)[:500]}))
        return 3
    except Exception as exc:                                             # note 6: never a traceback without a code
        print(json.dumps({'refused': 'INTERNAL_ERROR', 'stage': a.cmd, 'detail': ('%s: %s' % (type(exc).__name__, exc))[:500]}))
        return 3


if __name__ == '__main__':
    sys.exit(main())
