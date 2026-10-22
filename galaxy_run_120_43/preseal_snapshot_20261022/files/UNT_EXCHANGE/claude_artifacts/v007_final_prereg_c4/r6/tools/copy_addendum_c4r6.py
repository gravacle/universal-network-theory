# Claude4 r6 helper: make the exclusive byte copy of the OPEN V005 addendum that prereg r6 is generated from.
# usage: python3 -I -B copy_addendum_c4r6.py OUT_DIR
# Writes OUT_DIR/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md by exclusive create (never overwrites), reads it back,
# refuses unless the bytes read back equal the bytes read from the open file, and prints sha256, size and the entry headings.
# OUT_DIR must be the r6 folder or a folder inside it. Read-only on the addendum; writes nothing else.
import hashlib, json, re, sys
from pathlib import Path

R6D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6')
V005 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
            'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
COPY_REL = 'addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md'

out = Path(sys.argv[1]).resolve()
if not (out == R6D or str(out).startswith(str(R6D) + '/')):
    raise SystemExit('OUT_DIR must be inside r6: %s' % out)
(out / 'addendum_read').mkdir(parents=True, exist_ok=True)
b = V005.read_bytes()
dst = out / COPY_REL
with open(dst, 'xb') as f:
    f.write(b)
back = dst.read_bytes()
if back != b:
    raise SystemExit('the byte copy does not read back equal')
heads = [m.group(1).decode() for m in re.finditer(rb'(?m)^## (A\d+):', b)]
print(json.dumps({'copy': str(dst), 'sha256': hashlib.sha256(back).hexdigest(), 'bytes': len(back), 'entries': len(heads),
                  'newest': 'A%d' % max(int(h[1:]) for h in heads), 'first_in_file_order': heads[:6]}))
