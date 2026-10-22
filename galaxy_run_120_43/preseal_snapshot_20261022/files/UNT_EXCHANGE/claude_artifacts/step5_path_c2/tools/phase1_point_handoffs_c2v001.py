"""phase1_point_handoffs_c2v001.py -- one Phase-1 point handoff per S0 / F point (A133 1.4; RI45-09/RI45-10 shape).

phase1_c2v001 hands off admitted v003g members (its `handoff` command, the RI45-10 export path).  The S0 set (`fdplan
--s0-only`: the seed and its three Jacobian plus points, fixed now) and the FD points F (`fdplan`) are not admitted
points, so they get this handoff schema instead: UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001, ten fields, the RI45-10 shape
with source_pin / point_key in place of source_export_pin / log_index.  This tool only writes the handoffs; it decides
nothing.  fill_step5_c2v001 does every check (policy, coordinate mode, theta key, driver, certificates) and root
publishes each handoff sha before the filler runs (RI45-09).  launch_authorized is false throughout.

Root fields (schema PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001): mode, root_admission, policy_pin, v007_adoption_pin,
driver_branch, driver_acceptance_pin, certificate_pins_by_point {theta_key: {eps_certificate, lo_certificate}}.
Every point of the source needs its own certificate entry (RI45-06: certificates are per point); the sentinel
PENDING_UV_TAIL_CERTIFICATE is allowed and keeps run mode BLOCKED in the driver.

  PY -I -B phase1_point_handoffs_c2v001.py --source S0_C2V001.json --source-sha256 H --root-fields R
       --root-fields-sha256 H --out-dir NEW_DIR
Exit: 0 written, 2 refused (nothing written).
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

SCHEMA = 'UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001'
ROOT_SCHEMA = 'PHASE1_POINT_HANDOFF_ROOT_FIELDS_C2V001'
LISTS = {'PHASE1_S0_C2V001': 'points', 'PHASE1_FDPLAN_C2V001': 'F'}
PENDING = 'PENDING_UV_TAIL_CERTIFICATE'


class Refusal(ValueError):
    pass


def need(ok, why):
    if not ok:
        raise Refusal(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def strict(b, what):
    def pairs(ps):
        d = {}
        for k, v in ps:
            need(k not in d, 'DUPLICATE_JSON_KEY ' + what)
            d[k] = v
        return d
    try:
        return json.loads(b.decode('utf-8'), object_pairs_hook=pairs)
    except (UnicodeDecodeError, ValueError) as exc:
        raise Refusal('UNPARSEABLE_JSON %s (%s)' % (what, type(exc).__name__)) from None


def pinned(path, digest, what):
    need(isinstance(path, str) and os.path.isabs(path), 'ABSOLUTE_PATH_REQUIRED ' + what)
    b = Path(path).read_bytes()
    need(sha(b) == digest, 'PIN_MISMATCH ' + what)
    return b


def is_pin(x):
    return type(x) is dict and set(x) == {'path', 'sha256'}


def build(source, source_sha, root_fields, root_sha):
    src = strict(pinned(source, source_sha, 'source'), 'source')
    need(type(src) is dict and src.get('schema') in LISTS, 'SOURCE_SCHEMA')
    points = src.get(LISTS[src['schema']])
    need(type(points) is list and points, 'SOURCE_POINTS')
    rf = strict(pinned(root_fields, root_sha, 'root fields'), 'root fields')
    want = {'schema', 'mode', 'root_admission', 'policy_pin', 'v007_adoption_pin', 'driver_branch', 'driver_acceptance_pin',
            'certificate_pins_by_point'}
    need(type(rf) is dict and set(rf) == want and rf['schema'] == ROOT_SCHEMA, 'ROOT_FIELDS_KEYS')
    need(rf['mode'] in ('PHASE1_POINT', 'SYNTHETIC_DRY_ONLY'), 'ROOT_FIELDS_MODE')
    need(is_pin(rf['policy_pin']), 'ROOT_FIELDS_POLICY_PIN')
    for k in ('v007_adoption_pin', 'driver_acceptance_pin'):
        need(rf[k] is None or is_pin(rf[k]), 'ROOT_FIELDS_' + k.upper())
    cb = rf['certificate_pins_by_point']
    need(type(cb) is dict, 'ROOT_FIELDS_CERTIFICATES')
    keys = [p.get('key') if type(p) is dict else None for p in points]
    need(all(type(k) is str and len(k) == 64 for k in keys) and len(set(keys)) == len(keys), 'SOURCE_POINT_KEYS')
    need(set(cb) == set(keys), 'CERTIFICATES_NOT_ONE_ENTRY_PER_POINT')
    out = []
    for p in points:
        c = cb[p['key']]
        need(type(c) is dict and set(c) == {'eps_certificate', 'lo_certificate'} and
             all(v == PENDING or is_pin(v) for v in c.values()), 'CERTIFICATE_ENTRY ' + p['key'][:16])
        h = {'schema': SCHEMA, 'mode': rf['mode'], 'source_pin': {'path': source, 'sha256': source_sha}, 'point_key': p['key'],
             'policy_pin': rf['policy_pin'], 'driver_branch': rf['driver_branch'], 'driver_acceptance_pin': rf['driver_acceptance_pin'],
             'v007_adoption_pin': rf['v007_adoption_pin'], 'root_admission': rf['root_admission'], 'certificate_pins': c}
        out.append((p.get('role'), p['key'], h))
    return src, out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ('source', 'source-sha256', 'root-fields', 'root-fields-sha256', 'out-dir'):
        ap.add_argument('--' + k, required=True)
    a = ap.parse_args(argv)
    try:
        src, out = build(a.source, a.source_sha256, a.root_fields, a.root_fields_sha256)
        d = Path(a.out_dir)
        need(d.is_absolute() and not os.path.lexists(d) and d.parent.is_dir(), 'OUT_DIR must be absolute, absent, with a parent')
        d.mkdir()
        rows = []
        for role, key, h in out:
            b = (json.dumps(h, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
            name = 'HANDOFF_%s_%s_C2V001.json' % (role, key[:16])
            with open(d / name, 'xb') as f:
                f.write(b)
            rows.append({'role': role, 'point_key': key, 'path': str(d / name), 'sha256': sha(b)})
        rec = {'schema': 'UNT_STEP5_PHASE1_POINT_HANDOFF_RECEIPT_C2V001', 'launch_authorized': False,
               'source': {'path': a.source, 'sha256': a.source_sha256, 'schema': src['schema']},
               'root_fields': {'path': a.root_fields, 'sha256': a.root_fields_sha256}, 'handoffs': rows,
               'next': 'root publishes each handoff sha (RI45-09), then runs fill_step5_c2v001 --handoff H --expected-sha256 <published>'}
        with open(d / 'HANDOFF_RECEIPT_C2V001.json', 'xb') as f:
            f.write((json.dumps(rec, indent=2, sort_keys=True) + '\n').encode())
    except (Refusal, OSError, KeyError, TypeError) as exc:
        print('REFUSED: %s' % exc, file=sys.stderr)
        return 2
    print(json.dumps({'status': 'WRITTEN', 'handoffs': len(rows), 'launch_authorized': False}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
