# Claude4 r6 refute helper (r6_check): sha256 of every file in r6_check (sorted; walks r6_check only, no links followed),
# written by exclusive create as HASHES_R6CHK.txt in shasum format (absolute paths), so `shasum -a 256 -c` re-verifies it.
# usage: python3 -I -B make_hashes_r6chk.py
import hashlib, os

ROOT = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6_check'
OUT = os.path.join(ROOT, 'HASHES_R6CHK.txt')
rows = []
for dp, dn, fn in os.walk(ROOT):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        if p == OUT or os.path.islink(p):
            continue
        with open(p, 'rb') as fh:
            rows.append('%s  %s' % (hashlib.sha256(fh.read()).hexdigest(), p))
rows.sort(key=lambda r: r.split('  ', 1)[1])
with open(OUT, 'x') as fh:
    fh.write('\n'.join(rows) + '\n')
print(len(rows), 'files hashed ->', OUT)
