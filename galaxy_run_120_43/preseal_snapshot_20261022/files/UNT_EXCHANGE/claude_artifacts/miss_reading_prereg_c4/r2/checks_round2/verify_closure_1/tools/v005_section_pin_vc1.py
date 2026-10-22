# verify_closure_1: section sha256 of cited V005 entries in a snapshot, per PREREG r2 [C-11] L564
# ("the bytes from its `## A<n>:` heading line up to the next `## ` heading line, or up to the end-marker shown").
import hashlib, sys

path = sys.argv[1]
want = {'A63': '8cbe65538dc03ffe1c7f8c84088ce5e7c05791c9b36471ed7f1f2631330f169f',
        'A48': '526cfceacade31d16dc4f5c7fd023573515898692d4f40d22bfebc9216008ee6'}
raw = open(path, 'rb').read()
print('file sha256', hashlib.sha256(raw).hexdigest())
lines = raw.split(b'\n')
offs, pos = [], 0
for ln in lines:
    offs.append(pos)
    pos += len(ln) + 1
for name, pin in want.items():
    start = [i for i, ln in enumerate(lines) if ln.startswith(('## ' + name + ':').encode())]
    if len(start) != 1:
        print(name, 'heading count', len(start))
        continue
    s = start[0]
    e = next((j for j in range(s + 1, len(lines)) if lines[j].startswith(b'## ')), len(lines))
    sec = raw[offs[s]:offs[e]] if e < len(lines) else raw[offs[s]:]
    got = hashlib.sha256(sec).hexdigest()
    print(name, 'lines %d-%d' % (s + 1, e), got, 'MATCH' if got == pin else 'DIFFERS (pin %s)' % pin)
