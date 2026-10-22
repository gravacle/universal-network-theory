# Claude4 r6 refute helper (r6_check): apply a unified diff to its "from" file in memory and check that the result hashes to the
# "to" file's sha (and that every context/removed line matches). Read-only; prints a JSON verdict, writes nothing.
# usage: python3 -I -B apply_udiff_r6chk.py DIFF FROM FROM_SHA TO_SHA
import hashlib, json, re, sys

dp, fp, fsha, tsha = sys.argv[1:5]
src = open(fp, 'rb').read()
assert hashlib.sha256(src).hexdigest() == fsha, 'from sha'
a = src.decode('utf-8').splitlines(keepends=True)
d = open(dp, 'rb').read().decode('utf-8').splitlines(keepends=True)
out = []
pos = 0
i = 0
hunks = 0
bad = []
while i < len(d):
    ln = d[i]
    if ln.startswith('---') or ln.startswith('+++'):
        i += 1
        continue
    m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', ln)
    if not m:
        i += 1
        continue
    hunks += 1
    start = int(m.group(1)) - (1 if (m.group(2) is None or int(m.group(2)) > 0) else 0)
    out.extend(a[pos:start])
    pos = start
    i += 1
    while i < len(d) and not d[i].startswith('@@'):
        t = d[i]
        if t.startswith('\\'):
            i += 1
            continue
        tag, body = t[0], t[1:]
        if tag == ' ':
            if a[pos] != body:
                bad.append(('context', pos + 1))
            out.append(a[pos]); pos += 1
        elif tag == '-':
            if a[pos] != body:
                bad.append(('removed', pos + 1))
            pos += 1
        elif tag == '+':
            out.append(body)
        i += 1
out.extend(a[pos:])
res = ''.join(out).encode('utf-8')
got = hashlib.sha256(res).hexdigest()
print(json.dumps({'hunks': hunks, 'mismatched_lines': bad[:10], 'result_sha256': got, 'equals_to_sha': got == tsha}))
