"""Builder for DIRECT_BATCH_PARAMS_S45_C2V004C (Claude3, V006 A271, root dispatch 0836).

DIRECT_BATCH_PARAMS_S45_C2V004B (e239d21e) with exactly one data change: the 11 HEADLINE
caps_per_case.<case>.wall_cap_s leaves move from 100800 to W, the whole seconds remaining from
--fill-utc to the Phase-2 ceiling 2026-12-01T05:59:00Z (A246, A249; Mon Nov 30 23:59 CST).
Provenance leaves also change: schema, supersedes.{path,sha256,what_changes} and a new note_a271.
Every other leaf is asserted unchanged, including every rss_cap_bytes (physical RAM, A166),
every output_cap_bytes and every non-HEADLINE wall.

No code consumer changes. guard014 (6efdca01) only binds a plan call's caps to the admission's
cfg.caps[case] and requires positive integers (L388-392); launcher015 (cd987edd) passes the call's
wall to the pinned monitor (L19); the monitor (ba031c23) takes any wall > 0 (L116, L163, L232).
Root copies batches.HEADLINE.caps_per_case into the plan calls and cfg.caps, as for C2V004B
(DBP scope text).

Reads only the pinned C2V004B bytes. Writes, by exclusive create, into --out-dir (it must not
exist; its parent must exist): DIRECT_BATCH_PARAMS_S45_C2V004C.json and LEAF_DIFF_S45_C2V004C.json.
usage: python3 -I -B build_params_s45_c2v004c_c3v001.py --fill-utc YYYY-MM-DDTHH:MM:SSZ --out-dir NEW_DIR
"""
import argparse
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

BASE = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json')
BASE_SHA = 'e239d21e8f29e4711ec20c28c335bc25340fb8780253ceb1e57f037624e99205'
PHASE2_CEILING_UTC = '2026-12-01T05:59:00Z'
OLD_WALL = 100800
RAM_BYTES = 137438953472
SCHEMA = 'DIRECT_BATCH_PARAMS_S45_C2V004C'
OUT_NAME = 'DIRECT_BATCH_PARAMS_S45_C2V004C.json'
DIFF_NAME = 'LEAF_DIFF_S45_C2V004C.json'
FMT = '%Y-%m-%dT%H:%M:%SZ'


def refuse(code):
    raise SystemExit('REFUSED ' + code)


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def utc(s, label):
    try:
        t = dt.datetime.strptime(s, FMT).replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        refuse('BAD_UTC ' + label)
    if t.strftime(FMT) != s:
        refuse('NONCANONICAL_UTC ' + label)
    return t


def flat(o, pre=''):
    if isinstance(o, dict) and o:
        out = {}
        for k, v in o.items():
            out.update(flat(v, pre + k + '.'))
        return out
    return {pre[:-1]: o}


def build(base_raw, fill_utc):
    if sha_b(base_raw) != BASE_SHA:
        refuse('BASE_PIN_MISMATCH')
    base = json.loads(base_raw)
    if base.get('schema') != 'DIRECT_BATCH_PARAMS_S45_C2V004B':
        refuse('BASE_SCHEMA')
    fill, ceiling = utc(fill_utc, 'fill'), utc(PHASE2_CEILING_UTC, 'ceiling')
    wall = int((ceiling - fill).total_seconds())
    if wall <= OLD_WALL:
        refuse('FILL_TOO_LATE')                 # the successor must never shorten the wall
    head = base['batches']['HEADLINE']
    order = head['case_order']
    if len(order) != 11 or len(set(order)) != 11 or set(order) != set(head['caps_per_case']):
        refuse('HEADLINE_CASES')
    doc = copy.deepcopy(base)
    for case in order:
        caps = doc['batches']['HEADLINE']['caps_per_case'][case]
        if caps != {'output_cap_bytes': 85899345920, 'rss_cap_bytes': RAM_BYTES, 'wall_cap_s': OLD_WALL}:
            refuse('UNEXPECTED_BASE_CAPS ' + case)
        caps['wall_cap_s'] = wall
    doc['schema'] = SCHEMA
    doc['supersedes'] = {'path': str(BASE), 'sha256': BASE_SHA,
                         'what_changes': 'V006 A271 (0836): the 11 HEADLINE caps_per_case wall_cap_s leaves 100800 -> %d, '
                                         'the whole seconds from %s to the Phase-2 ceiling %s; schema, supersedes and '
                                         'note_a271; nothing else' % (wall, fill_utc, PHASE2_CEILING_UTC)}
    doc['note_a271'] = ('V006 A271 (0836): HEADLINE11 first attempts run with wall = the time remaining to the Phase-2 '
                        'ceiling %s (A246: no wall cap ends a run; A249: the Phase-1 ceiling is a reporting boundary). '
                        'W = %d s from the plan fill time %s. A call whose monitor starts later than the fill can run '
                        'past the ceiling by at most its start delay; the ceiling freezes the score either way. RSS and '
                        'output caps, all other batches and every non-cap byte are C2V004B\'s.'
                        % (PHASE2_CEILING_UTC, wall, fill_utc))
    fa, fb = flat(base), flat(doc)
    changed = sorted(k for k in set(fa) | set(fb) if fa.get(k, '<absent>') != fb.get(k, '<absent>'))
    walls = sorted('batches.HEADLINE.caps_per_case.%s.wall_cap_s' % c for c in order)
    allowed = set(walls) | {'schema', 'supersedes.path', 'supersedes.sha256', 'supersedes.what_changes', 'note_a271'}
    if not set(walls) <= set(changed) or not set(changed) <= allowed:
        refuse('LEAF_DIFF_SCOPE')
    for k, v in fb.items():
        if k.endswith('.rss_cap_bytes') and v != fa.get(k):
            refuse('RSS_CHANGED')
        if k.endswith('.output_cap_bytes') and v != fa.get(k):
            refuse('OUTPUT_CAP_CHANGED')
        if k.endswith('.wall_cap_s') and k not in walls and v != fa.get(k):
            refuse('NON_HEADLINE_WALL_CHANGED')
    raw = (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode()
    diff = {'base': {'path': str(BASE), 'sha256': BASE_SHA}, 'schema': 'LEAF_DIFF_S45_C2V004C',
            'phase2_ceiling_utc': PHASE2_CEILING_UTC, 'fill_utc': fill_utc, 'wall_cap_s': wall,
            'changed_leaves': {k: ({'from': fa.get(k, '<absent>'), 'to': fb.get(k, '<absent>')} if k in walls or k == 'schema' or k == 'supersedes.sha256'
                                   else {'changed': 'text', 'to_sha256': sha_b(json.dumps(fb.get(k)).encode())}) for k in changed},
            'n_changed': len(changed), 'n_wall_leaves': len(walls),
            'asserted_unchanged': 'every other leaf, every rss_cap_bytes and output_cap_bytes, every non-HEADLINE wall',
            'successor_sha256': sha_b(raw)}
    draw = (json.dumps(diff, indent=1, sort_keys=True) + '\n').encode()
    return raw, draw, wall


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fill-utc', required=True)
    ap.add_argument('--out-dir', required=True)
    a = ap.parse_args(argv)
    out = Path(a.out_dir)
    if not out.is_absolute() or out.exists() or not out.parent.is_dir():
        refuse('OUT_DIR_MUST_BE_NEW_ABSOLUTE_WITH_PARENT')
    raw, draw, wall = build(BASE.read_bytes(), a.fill_utc)
    os.mkdir(out)
    with open(out / OUT_NAME, 'xb') as f:
        f.write(raw)
    with open(out / DIFF_NAME, 'xb') as f:
        f.write(draw)
    print(json.dumps({'dbp_c2v004c': {'path': str(out / OUT_NAME), 'sha256': sha_b(raw)},
                      'leaf_diff': {'path': str(out / DIFF_NAME), 'sha256': sha_b(draw)}, 'wall_cap_s': wall}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
