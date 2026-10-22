# Claude4 r5 helper: derive make_v007_final_draft_c4v005_p2.py from make_v007_final_draft_c4v005.py (whose dry run refused before writing
# anything: its row/edit consistency check compared 'seal_record_requirements[2]' with the logged 'seal_record_requirements.2', and two log
# entries combine clause names). Anchored edits only (each anchor exactly once); exclusive create; prints the diff sha.
import difflib, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC, DST = HERE / 'make_v007_final_draft_c4v005.py', HERE / 'make_v007_final_draft_c4v005_p2.py'
t0 = SRC.read_bytes().decode()
t = t0
EDITS = [
    # 1. a name normalizer and an expander for combined log names (placed after cl())
    ("def sections(b):\n",
     "def norm(c):\n"
     "    \"\"\"clause names: 'x.2' -> 'x[2]' (list indices), as the rows write them.\"\"\"\n"
     "    return re.sub(r'\\.(\\d+)(?=\\.|$)', r'[\\1]', c)\n"
     "\n"
     "\n"
     "def expand(c):\n"
     "    \"\"\"a logged clause name may combine names ('a.b / c', 'a.X, Y'); bare names inherit the first name's prefix.\"\"\"\n"
     "    parts = [q for part in c.split(' / ') for q in part.split(', ')]\n"
     "    head = parts[0]\n"
     "    pre = head.rsplit('.', 1)[0] + '.' if '.' in head else ''\n"
     "    keep = ('status', 'assembly', 'decision_pins_pending_at_seal', 'cites_by_name')\n"
     "    return [norm(q if ('.' in q or not pre or q.startswith(keep)) else pre + q) for q in parts]\n"
     "\n"
     "\n"
     "def sections(b):\n"),
    # 2. drop the no-op loop
    ("    for e in ['A%d' % n for n in range(47, max(nums) + 1) if n not in (76, 65) or True]:\n        pass\n", ""),
    # 3. strict consistency check on normalized, expanded names
    ("    changed = {c['clause'] for c in changes}\n",
     "    changed = {x for c in changes for x in expand(c['clause'])}\n"),
    ("            if not any(c == x or x.startswith(c) or c.startswith(x.split(' ')[0]) for x in changed):\n",
     "            if norm(c) not in changed:\n"),
    # 4. the clause map's 'changed in r5' column uses the same normalized set
    ("    M += ['| `%s` | %s | %s |' % (k, '; '.join(s), 'yes' if any(k == c or k.startswith(c.split(' ')[0]) or c.startswith(k) for c in changed | {'entries_after_A81'}) else '')\n",
     "    changed_all = {x for c in changes for x in expand(c['clause'])}\n"
     "    M += ['| `%s` | %s | %s |' % (k, '; '.join(s), 'yes' if (norm(k) in changed_all or k.startswith('entries_after_A81')) else '')\n"),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, (n, old[:70])
    t = t.replace(old, new)
with open(DST, 'x') as f:
    f.write(t)
d = ''.join(difflib.unified_diff(t0.splitlines(True), t.splitlines(True), SRC.name, DST.name))
print('p2 sha256', hashlib.sha256(DST.read_bytes()).hexdigest(), '| diff lines', len(d.splitlines()), '| diff sha256', hashlib.sha256(d.encode()).hexdigest())
