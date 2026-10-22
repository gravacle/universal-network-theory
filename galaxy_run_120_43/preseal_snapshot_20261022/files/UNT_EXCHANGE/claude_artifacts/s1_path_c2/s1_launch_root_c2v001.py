"""S1 root launch path (s1_path_c2, c2v001). Root only.

Loads s1_path_lib_c2v001.py from this folder by its sha256 and refuses on any mismatch. Order, all fail closed:
  1. S1 checks: registration in force (its sha in the pinned V006 bytes), launch config, POST_S1 one-call plan on
     guard011/launcher012, driver r5, tail ON, spec = the filled spec, template replay byte-equal;
  2. the four 0620 controls through guard011 (spec_structure + allowlist, adoption, validate with native preflight),
     before any process (guard011's fence refuses process creation);
  3. machine gate v003: hold_check, then Gate.decide for the S1 head after the warm-up; A133's root memory rule;
  4. --launch only: the exclusive pre-launch record, then launcher012 (which re-validates and detaches its worker).
The published admission is read from UNT_STEP4_ADMISSION_PATH / UNT_STEP4_ADMISSION_SHA256 (as launcher012).
Default mode is dry: nothing is launched. --launch also needs --confirm <plan sha256> and --record PATH.
  --plan P@S --registration P@S --v6 P@S --launch-config P@S [--record PATH] [--launch --confirm SHA]
Exit 0: admitted (dry) or launched; 3: refused (the code and stage are printed).
"""
import argparse
import hashlib
import json
import os
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
    path, _, sha = s.rpartition('@')
    return {'path': path, 'sha256': sha}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    for a in ('--plan', '--registration', '--v6', '--launch-config'):
        ap.add_argument(a, required=True)
    ap.add_argument('--record')
    ap.add_argument('--launch', action='store_true')
    ap.add_argument('--confirm')
    a = ap.parse_args(argv)
    L = lib()
    p, h = os.environ.get('UNT_STEP4_ADMISSION_PATH', ''), os.environ.get('UNT_STEP4_ADMISSION_SHA256', '')
    admission = {'path': p, 'sha256': h} if (p and h) else None
    out = L.launch(pin(a.plan), admission, pin(a.registration), pin(a.v6), pin(a.launch_config),
                   mode='launch' if a.launch else 'dry', confirm=a.confirm, record_path=a.record, disk_batch=True)
    print(json.dumps(out, indent=1, sort_keys=True, default=str))
    return 0 if out['decision'] in ('ADMITTED', 'LAUNCHED') else 3


if __name__ == '__main__':
    sys.exit(main())
