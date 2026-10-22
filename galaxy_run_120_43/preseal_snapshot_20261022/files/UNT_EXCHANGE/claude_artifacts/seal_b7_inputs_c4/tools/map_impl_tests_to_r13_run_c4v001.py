# Claude4 helper (dispatch 0650, A113 P6): map each C-08 NEW id and each IMPL-named test to the r13 author run of record
# (v007_compare_c2/r13/out/author_cx3v001/TEST_SUMMARY.json, the 706/706 run named by AUTHOR_706_MAPPING_CX3V001.json).
# Read-only; prints one JSON object. Run under tools/run_fenced_c4st2.py.
# usage: map_impl_tests_to_r13_run_c4v001.py SUMMARY.json SUMMARY_SHA256 COMPARE_SHA256 --ids NEW-4 ... --names NAME ...
import hashlib, json, re, sys
from pathlib import Path


def pairs(ps):
    out = {}
    for k, v in ps:
        if k in out:
            raise ValueError('DUPLICATE_JSON_KEY %r' % k)
        out[k] = v
    return out


argv = sys.argv[1:]
summ, want, cmp_sha = argv[0], argv[1], argv[2]
i_ids, i_names = argv.index('--ids'), argv.index('--names')
ids, names = argv[i_ids + 1:i_names], argv[i_names + 1:]
raw = Path(summ).read_bytes()
got = hashlib.sha256(raw).hexdigest()
if got != want:
    print(json.dumps({'refused': 'SUMMARY_SHA_MISMATCH', 'got': got}))
    raise SystemExit(2)
d = json.loads(raw, object_pairs_hook=pairs)
tests = d['tests']
head = {'summary': summ, 'sha256': got, 'schema': d.get('schema'), 'script_sha256': d.get('script_sha256'),
        'script_is_the_reviewed_compare': d.get('script_sha256') == cmp_sha, 'tests_sha256': d.get('tests_sha256'),
        'n': d.get('n'), 'n_pass': d.get('n_pass'), 'n_fail': d.get('n_fail'), 'n_rows': len(tests),
        'names_unique': len({x['test'] for x in tests}) == len(tests)}


def tag_hits(nid, covers):
    rx = re.compile(r'(?<![0-9A-Za-z])%s(?![0-9])' % re.escape(nid))
    return [c for c in covers if isinstance(c, str) and rx.search(c)]


by_id = {}
for nid in ids:
    rows = []
    for x in tests:
        h = tag_hits(nid, x.get('covers') or [])
        if h:
            rows.append({'test': x['test'], 'tags': h, 'pass': x.get('pass'), 'expected': x.get('expected')})
    by_id[nid] = rows


def segments(s):
    return [p for p in re.split(r'[…*]', s) if p]


def matches_name(n, a):
    if not re.search(r'[…*]', n):
        return a == n
    segs, pos = segments(n), 0
    if not segs:
        return False
    if not re.match(r'[…*]', n):
        if not a.startswith(segs[0]):
            return False
        pos, segs = len(segs[0]), segs[1:]
    for sg in segs:
        j = a.find(sg, pos)
        if j < 0:
            return False
        pos = j + len(sg)
    return True


named = {}
for n in names:
    hit = [x for x in tests if matches_name(n, x['test'])]
    longer = [x for x in tests if not re.search(r'[…*]', n) and x['test'].startswith(n) and x['test'] != n]
    named[n] = {'exact': any(x['test'] == n for x in tests), 'matched': [{'test': x['test'], 'pass': x.get('pass')} for x in hit],
                'longer_with_this_prefix': [{'test': x['test'], 'pass': x.get('pass')} for x in longer]}
print(json.dumps({'head': head, 'by_id': by_id, 'impl_named': named}, indent=1, sort_keys=True))
