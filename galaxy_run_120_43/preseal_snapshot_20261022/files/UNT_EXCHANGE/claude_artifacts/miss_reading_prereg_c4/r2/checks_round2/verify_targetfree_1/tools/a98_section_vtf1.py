# verify_targetfree_1: section sha256 of A97..A100 (and A77, whose section precedes the insertion point) in each V005 snapshot,
# to test whether per-entry pins of the new entries are stable under root's insertions. Writes one JSON (exclusive create).
# usage: python3 -I -B a98_section_vtf1.py OUT.json V005_SNAPSHOT.md [...]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_vtf1  # noqa: F401
import hashlib, json
from recheck_t7_vtf1 import section_bytes

out = {'snapshots': []}
for sp in sys.argv[2:]:
    b = open(sp, 'rb').read()
    row = {'path': sp, 'sha256': hashlib.sha256(b).hexdigest(), 'sections': {}}
    for n in (77, 96, 97, 98, 99, 100):
        sb, cnt = section_bytes(b, n, 'next heading')
        row['sections']['A%d' % n] = None if sb is None else {'sha256': hashlib.sha256(sb).hexdigest(), 'n_bytes': len(sb), 'count': cnt}
    out['snapshots'].append(row)
with open(sys.argv[1], 'x') as f:
    f.write(json.dumps(out, indent=1) + '\n')
for r in out['snapshots']:
    print(r['sha256'][:8], {k: (v['sha256'][:12] if v else None) for k, v in r['sections'].items()})
