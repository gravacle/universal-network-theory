# Claude4 helper (dispatch 0650): print named entries (e.g. A113, A59) of a root decision addendum file, with the file's sha256.
# Read-only; prints only. Run under tools/run_fenced_c4st2.py. usage: print_addendum_entries_c4v001.py FILE ENTRY [ENTRY ...]
import hashlib, re, sys
from pathlib import Path

raw = Path(sys.argv[1]).read_bytes()
print('FILE', sys.argv[1], 'sha256', hashlib.sha256(raw).hexdigest(), 'bytes', len(raw))
text = raw.decode('utf-8')
lines = text.split('\n')
heads = [(i, l) for i, l in enumerate(lines) if re.match(r'^#{1,4} ', l)]
for want in sys.argv[2:]:
    rx = re.compile(r'^#{1,4} .*\b%s\b' % re.escape(want))
    hit = [(j, i) for j, (i, l) in enumerate(heads) if rx.match(l)]
    if not hit:
        print('=== %s: NO HEADING FOUND' % want)
        continue
    for j, i in hit:
        lvl = len(heads[j][1]) - len(heads[j][1].lstrip('#'))
        end = len(lines)
        for i2, l2 in heads[j + 1:]:
            if len(l2) - len(l2.lstrip('#')) <= lvl:
                end = i2
                break
        print('=== %s: lines %d-%d' % (want, i + 1, end))
        print('\n'.join(lines[i:end])[:12000])
