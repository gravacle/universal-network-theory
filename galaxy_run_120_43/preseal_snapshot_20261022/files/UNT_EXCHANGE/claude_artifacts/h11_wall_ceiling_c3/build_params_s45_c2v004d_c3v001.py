"""Builder for DIRECT_BATCH_PARAMS_S45_C2V004D (Claude3, V006 A284, root dispatch 0844).

DIRECT_BATCH_PARAMS_S45_C2V004C (ce9cbef8; the verdict-day object, left unchanged) with exactly one
data change: the two POST_S1 caps_per_case.<entry>.wall_cap_s leaves move from 100800 to W, the
whole seconds from --fill-utc to the Phase-2 ceiling 2026-12-01T05:59:00Z (C2V004C's fill rule;
A246, A249). The DBP names the two entries ROOT_NAMES_AT_REGISTRATION_K3 and _K4; root registers
them as S1_UA_C3T and S1_UA_C4T. C2V004C's 11 HEADLINE walls are kept as they are.
Provenance leaves also change: schema, supersedes.{path,sha256,what_changes} and a new note_a284.

Against C2V004B (e239d21e) the changes are therefore the 13 walls plus the provenance leaves
(schema, supersedes.*, note_a271, note_a284). Every rss_cap_bytes (physical RAM, A166), every
output_cap_bytes, every DIII/SENS_LO/SENS_HI wall and every non-cap byte is asserted unchanged.
The fill may not precede C2V004C's own fill (the ceiling minus its wall), and W must exceed 100800.

No code consumer changes. The S1 pair guard (1274a39a) binds each call's caps to the parent
admission's cfg.caps[case] (ROOT_CAPS_BINDING, L428), to its child admission's caps (L377) and to
its child plan's call bytes (L381); the launcher passes the call's wall to the pinned monitor,
which takes any wall > 0. Root copies caps_per_case into those records, as for C2V004B.

Reads only the pinned C2V004B and C2V004C bytes. Writes, by exclusive create, into --out-dir (it must
not exist; its parent must exist): DIRECT_BATCH_PARAMS_S45_C2V004D.json and LEAF_DIFF_S45_C2V004D.json.
usage: python3 -I -B build_params_s45_c2v004d_c3v001.py --fill-utc YYYY-MM-DDTHH:MM:SSZ --out-dir NEW_DIR
"""
import argparse
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

BASE_B = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/sched_s45_c2/v004b/DIRECT_BATCH_PARAMS_S45_C2V004B.json')
BASE_B_SHA = 'e239d21e8f29e4711ec20c28c335bc25340fb8780253ceb1e57f037624e99205'
BASE_C = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h11_wall_ceiling_c3/C2V004C_FILL_20261022T093000Z/DIRECT_BATCH_PARAMS_S45_C2V004C.json')
BASE_C_SHA = 'ce9cbef8caaef8120377f302647c71d80387353d192d25d7d0b7e13e5872e809'
PHASE2_CEILING_UTC = '2026-12-01T05:59:00Z'
OLD_WALL = 100800
RAM_BYTES = 137438953472
POST_S1_OUTPUT_CAP = 85899345920
POST_S1_ENTRIES = ('ROOT_NAMES_AT_REGISTRATION_K3', 'ROOT_NAMES_AT_REGISTRATION_K4')
SCHEMA = 'DIRECT_BATCH_PARAMS_S45_C2V004D'
OUT_NAME = 'DIRECT_BATCH_PARAMS_S45_C2V004D.json'
DIFF_NAME = 'LEAF_DIFF_S45_C2V004D.json'
FMT = '%Y-%m-%dT%H:%M:%SZ'
PROVENANCE_C = {'schema', 'supersedes.path', 'supersedes.sha256', 'supersedes.what_changes', 'note_a271'}
PROVENANCE_D = {'schema', 'supersedes.path', 'supersedes.sha256', 'supersedes.what_changes', 'note_a284'}


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


def changed_leaves(fa, fb):
    return sorted(k for k in set(fa) | set(fb) if fa.get(k, '<absent>') != fb.get(k, '<absent>'))


def build(b_raw, c_raw, fill_utc):
    if sha_b(b_raw) != BASE_B_SHA:
        refuse('BASE_B_PIN_MISMATCH')
    if sha_b(c_raw) != BASE_C_SHA:
        refuse('BASE_C_PIN_MISMATCH')
    b, c = json.loads(b_raw), json.loads(c_raw)
    if b.get('schema') != 'DIRECT_BATCH_PARAMS_S45_C2V004B' or c.get('schema') != 'DIRECT_BATCH_PARAMS_S45_C2V004C':
        refuse('BASE_SCHEMA')
    if c.get('supersedes', {}).get('sha256') != BASE_B_SHA:
        refuse('C2V004C_NOT_FROM_C2V004B')
    fbase, fc = flat(b), flat(c)
    head = c['batches']['HEADLINE']['case_order']
    hwalls = sorted('batches.HEADLINE.caps_per_case.%s.wall_cap_s' % k for k in head)
    if len(head) != 11 or set(changed_leaves(fbase, fc)) != set(hwalls) | PROVENANCE_C:
        refuse('C2V004C_SCOPE')                 # C2V004C must be exactly C2V004B plus its 11 walls
    c_walls = {fc[k] for k in hwalls}
    c_wall = c_walls.pop() if len(c_walls) == 1 else None
    if type(c_wall) is not int or c_wall <= OLD_WALL:
        refuse('C2V004C_WALLS')
    fill, ceiling = utc(fill_utc, 'fill'), utc(PHASE2_CEILING_UTC, 'ceiling')
    wall = int((ceiling - fill).total_seconds())
    if wall <= OLD_WALL:
        refuse('FILL_TOO_LATE')                 # the successor must never shorten a wall
    if wall > c_wall:
        refuse('FILL_BEFORE_C2V004C_FILL')      # no POST_S1 fill precedes the direct batch's fill
    post = c['batches']['POST_S1']
    if post.get('case_order') != list(POST_S1_ENTRIES) or set(post.get('caps_per_case', {})) != set(POST_S1_ENTRIES) \
            or post.get('n_calls') != 2:
        refuse('POST_S1_ENTRIES')
    doc = copy.deepcopy(c)
    for e in POST_S1_ENTRIES:
        caps = doc['batches']['POST_S1']['caps_per_case'][e]
        if caps != {'output_cap_bytes': POST_S1_OUTPUT_CAP, 'rss_cap_bytes': RAM_BYTES, 'wall_cap_s': OLD_WALL}:
            refuse('UNEXPECTED_BASE_CAPS ' + e)
        caps['wall_cap_s'] = wall
    c_fill = (ceiling - dt.timedelta(seconds=c_wall)).strftime(FMT)
    doc['schema'] = SCHEMA
    doc['supersedes'] = {'path': str(BASE_C), 'sha256': BASE_C_SHA,
                         'what_changes': 'V006 A284 (0844): the 2 POST_S1 caps_per_case wall_cap_s leaves (%s, %s; root '
                                         'registers them as S1_UA_C3T, S1_UA_C4T) 100800 -> %d, the whole seconds from %s '
                                         'to the Phase-2 ceiling %s; schema, supersedes and note_a284; nothing else. '
                                         'C2V004C\'s 11 HEADLINE walls (%d s, fill %s) are kept.'
                                         % (POST_S1_ENTRIES + (wall, fill_utc, PHASE2_CEILING_UTC, c_wall, c_fill))}
    doc['note_a284'] = ('V006 A284 (0844): the S1 pair runs concurrently (A284), so a 100800 s wall stop became more likely '
                        'and would be an uncounted rerun (Claude3 0285 N8; A246: no wall cap ends a run). The two POST_S1 '
                        'walls are W = %d s from the fill time %s, by C2V004C\'s fill rule. For the POST_S1 walls this '
                        'replaces note_a271\'s statement that the other batches are C2V004B\'s; every other cap and byte is '
                        'still C2V004B\'s or C2V004C\'s. C2V004C remains the verdict-day object; C2V004D is for S8 onward.'
                        % (wall, fill_utc))
    fd = flat(doc)
    pwalls = sorted('batches.POST_S1.caps_per_case.%s.wall_cap_s' % e for e in POST_S1_ENTRIES)
    vs_c, vs_b = changed_leaves(fc, fd), changed_leaves(fbase, fd)
    if set(vs_c) != set(pwalls) | PROVENANCE_D:
        refuse('LEAF_DIFF_SCOPE_VS_C2V004C')
    if set(vs_b) != set(hwalls) | set(pwalls) | PROVENANCE_C | PROVENANCE_D:
        refuse('LEAF_DIFF_SCOPE_VS_C2V004B')
    for k, v in fd.items():
        if k.endswith(('.rss_cap_bytes', '.output_cap_bytes')) and v != fbase.get(k):
            refuse('RSS_OR_OUTPUT_CAP_CHANGED')
        if k.endswith('.wall_cap_s') and k not in hwalls and k not in pwalls and v != fbase.get(k):
            refuse('OTHER_WALL_CHANGED')
        if k in hwalls and v != fc[k]:
            refuse('HEADLINE_WALL_NOT_C2V004C')
    raw = (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode()

    def leaves(fa, changed, walls):
        return {k: ({'from': fa.get(k, '<absent>'), 'to': fd.get(k, '<absent>')} if k in walls or k in ('schema', 'supersedes.sha256')
                    else {'changed': 'text', 'to_sha256': sha_b(json.dumps(fd.get(k)).encode())}) for k in changed}
    diff = {'schema': 'LEAF_DIFF_S45_C2V004D', 'phase2_ceiling_utc': PHASE2_CEILING_UTC, 'fill_utc': fill_utc,
            'post_s1_wall_cap_s': wall, 'headline_wall_cap_s': c_wall, 'c2v004c_fill_utc': c_fill,
            'against_c2v004c': {'base': {'path': str(BASE_C), 'sha256': BASE_C_SHA},
                                'changed_leaves': leaves(fc, vs_c, pwalls), 'n_changed': len(vs_c)},
            'against_c2v004b': {'base': {'path': str(BASE_B), 'sha256': BASE_B_SHA},
                                'changed_leaves': leaves(fbase, vs_b, hwalls + pwalls), 'n_changed': len(vs_b)},
            'asserted_unchanged': 'every other leaf: every rss_cap_bytes and output_cap_bytes, every DIII/SENS_LO/SENS_HI '
                                  'wall, C2V004C\'s HEADLINE walls and every non-cap byte',
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
    raw, draw, wall = build(BASE_B.read_bytes(), BASE_C.read_bytes(), a.fill_utc)
    os.mkdir(out)
    with open(out / OUT_NAME, 'xb') as f:
        f.write(raw)
    with open(out / DIFF_NAME, 'xb') as f:
        f.write(draw)
    print(json.dumps({'dbp_c2v004d': {'path': str(out / OUT_NAME), 'sha256': sha_b(raw)},
                      'leaf_diff': {'path': str(out / DIFF_NAME), 'sha256': sha_b(draw)}, 'post_s1_wall_cap_s': wall},
                     sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
