# verify_targetfree_1: replay of generator v003's no-change complement (its L16-31 CITED numbers, L62-75 logic, re-implemented here)
# on each V005 snapshot, then this folder's independent T7 test on the result. Shows whether "re-run T7 at r3 assembly" can fail
# when the list is still generated. Synthetic: no object file is changed; one JSON is written (exclusive create).
# usage: python3 -I -B complement_replay_vtf1.py OUT.json V005_SNAPSHOT.md [...]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fence_vtf1  # noqa: F401
import hashlib, json, re

CITED_N = {48, 50, 52, 56, 60, 62, 63, 64, 65, 66, 70, 81, 82, 90}   # generator v003 L16-31, as read from its bytes

def heads(b):
    return sorted({int(m.group(1)) for m in re.finditer(rb'^## A(\d{1,3})\b', b, re.M)})

def complement_text(nums):
    unc = [n for n in nums if n >= 47 and n not in CITED_N]
    runs, cur = [], []
    for n in unc:
        if cur and n == cur[-1] + 1:
            cur.append(n)
        else:
            if cur:
                runs.append(cur)
            cur = [n]
    if cur:
        runs.append(cur)
    return ', '.join(('A%d' % r[0]) if len(r) == 1 else ('A%d–A%d' % (r[0], r[-1])) for r in runs)

def expand(txt):
    s = set()
    for part in txt.split(','):
        m = re.fullmatch(r'A(\d+)(?:–A(\d+))?', part.strip())
        a = int(m.group(1)); s.update(range(a, int(m.group(2) or a) + 1))
    return s

out = []
for sp in sys.argv[2:]:
    b = open(sp, 'rb').read()
    hs = heads(b)
    txt = complement_text(hs)
    nc = expand(txt)
    later = [n for n in hs if n >= 47 and n not in CITED_N and n not in nc]
    out.append({'path': sp, 'sha256': hashlib.sha256(b).hexdigest(), 'generated_no_change_list': txt,
                'A98_in_generated_no_change': 98 in nc, 't7_later_with_generated_list': ['A%d' % n for n in later],
                't7_pass_with_generated_list': not later})
with open(sys.argv[1], 'x') as f:
    f.write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
for r in out:
    print(r['sha256'][:8], r['generated_no_change_list'], '| A98 in list:', r['A98_in_generated_no_change'], '| T7 pass:', r['t7_pass_with_generated_list'])
