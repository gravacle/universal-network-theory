"""Lens C helper: recompute V005 per-entry section sha256 (heading line to next '## ' line or EOF)
from the current bytes and compare with the pins quoted in PREREG_MISS_READING_R2.md section 11.
Read-only. Prints JSON."""
import hashlib, json, re, sys
v005_path, prereg_path = sys.argv[1], sys.argv[2]
raw = open(v005_path, 'rb').read()
lines = raw.split(b'\n')
# keep line terminators exactly
parts = raw.splitlines(keepends=True)
heads = [i for i, l in enumerate(parts) if l.startswith(b'## ')]
sections = {}
for k, i in enumerate(heads):
    m = re.match(rb'## (A\d+)[: ]', parts[i])
    j = heads[k + 1] if k + 1 < len(heads) else len(parts)
    body = b''.join(parts[i:j])
    if m:
        sections.setdefault(m.group(1).decode(), []).append(hashlib.sha256(body).hexdigest())
pre = open(prereg_path, encoding='utf-8').read()
pins = dict(re.findall(r'^\| (A\d+) \| [^|]+\| `([0-9a-f]{64})` \|$', pre, flags=re.M))
out = {'v005_sha256': hashlib.sha256(raw).hexdigest(), 'n_headings': len(heads), 'results': {}}
for a, pin in sorted(pins.items(), key=lambda x: int(x[0][1:])):
    cur = sections.get(a)
    out['results'][a] = {'pin': pin, 'current': cur, 'match': bool(cur) and len(cur) == 1 and cur[0] == pin}
out['entries_present'] = sorted(sections, key=lambda x: int(x[1:]))
print(json.dumps(out, indent=1))
