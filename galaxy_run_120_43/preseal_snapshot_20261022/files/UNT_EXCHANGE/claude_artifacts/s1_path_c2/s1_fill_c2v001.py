"""S1 template CLI for root (s1_path_c2, c2v001): fill | dry-plan | plan.

Loads s1_path_lib_c2v001.py from this folder by its sha256 and refuses on any mismatch. Writes only the named outputs,
by exclusive create; dry-plan writes nothing. Starts no process. Pins are given as PATH@SHA256.
  fill      --u-a P@S --base-spec P@S --campaign-config P@S --c3t-eps P@S --c3t-lo P@S --out-dir DIR
  dry-plan  --u-a P@S --base-spec P@S --campaign-config P@S [--c3t-eps P@S --c3t-lo P@S]
  plan      --fill-record P@S --case S1_UA_C3T|S1_UA_C4T --prelaunch P@S [--params P@S] [--attempt N] --out PATH [--dry]
Exit 0: done; 3: refused (the code is printed).
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
        p.add_argument('--c3t-eps')
        p.add_argument('--c3t-lo')
        if name == 'fill':
            p.add_argument('--out-dir', required=True)
    p = sub.add_parser('plan', allow_abbrev=False)
    p.add_argument('--fill-record', required=True)
    p.add_argument('--case', required=True)
    p.add_argument('--prelaunch')
    p.add_argument('--params')
    p.add_argument('--attempt', type=int, default=1)
    p.add_argument('--out')
    p.add_argument('--dry', action='store_true')
    a = ap.parse_args(argv)
    L = lib()
    try:
        if a.cmd in ('fill', 'dry-plan'):
            certs = None
            if a.c3t_eps or a.c3t_lo:
                certs = {'eps_certificate': pin(a.c3t_eps), 'lo_certificate': pin(a.c3t_lo)}
            rec = L.fill(pin(a.u_a), pin(a.base_spec), pin(a.campaign_config), c3t_certs=certs,
                         out_dir=getattr(a, 'out_dir', None), dry=(a.cmd == 'dry-plan'))
            print(json.dumps(rec, indent=1, sort_keys=True))
        else:
            r = L.make_plan(pin(a.fill_record), a.case, pin(a.prelaunch), params_ref=pin(a.params), attempt=a.attempt,
                            out_path=a.out, dry=a.dry)
            print(json.dumps({'sidecar': r['sidecar'], 'written': r['written'], 'plan': r['plan']}, indent=1, sort_keys=True))
            if not a.dry and r['written'] is None:
                return 3
        return 0
    except L.Refusal as exc:
        print(json.dumps({'refused': exc.code, 'detail': None if exc.detail is None else str(exc.detail)[:500]}))
        return 3


if __name__ == '__main__':
    sys.exit(main())
