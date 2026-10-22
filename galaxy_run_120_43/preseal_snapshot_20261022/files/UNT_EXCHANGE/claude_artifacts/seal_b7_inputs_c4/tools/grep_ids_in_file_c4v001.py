# Claude4 helper (dispatch 0650): for one named file, print every line that names one of the given NEW ids (whole-id match),
# with its line number and the nearest preceding '## ' heading. Read-only; prints only. Run under tools/run_fenced_c4st2.py.
# usage: grep_ids_in_file_c4v001.py FILE NEW-4 NEW-7 ...
import hashlib, re, sys
from pathlib import Path
raw = Path(sys.argv[1]).read_bytes()
print('FILE', sys.argv[1], 'sha256', hashlib.sha256(raw).hexdigest())
lines = raw.decode('utf-8').split('\n')
ids = sys.argv[2:]
head = ''
for i, l in enumerate(lines, 1):
    if l.startswith('## '):
        head = l[:90]
    hit = [x for x in ids if re.search(r'(?<![A-Za-z0-9-])%s(?![0-9])' % re.escape(x), l)]
    if hit:
        print('L%d [%s] {%s}: %s' % (i, head, ','.join(hit), l[:900]))
