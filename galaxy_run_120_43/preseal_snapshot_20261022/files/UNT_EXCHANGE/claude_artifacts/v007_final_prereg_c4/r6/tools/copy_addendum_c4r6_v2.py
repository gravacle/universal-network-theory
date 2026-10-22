# Claude4 r6 helper, continuation run 2: make the exclusive byte copy of the CLOSED V005 addendum (closed at A106, A106.3)
# that prereg r6 is generated from. Supersedes copy_addendum_c4r6.py before any use (v1 was never run; it did not pin the sha).
# usage: python3 -I -B copy_addendum_c4r6_v2.py OUT_DIR EXPECTED_SHA256
# Reads the V005 file ONCE, hashes those bytes and refuses (writing nothing) unless the sha equals EXPECTED_SHA256; V005 is
# closed, so any other sha is a defect for root. Then writes OUT_DIR/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md by
# exclusive create (never overwrites), reads it back, refuses unless the bytes read back equal the bytes hashed, and prints sha256,
# size, the entry headings and the newest entry. OUT_DIR must be the r6 folder. Read-only on the addendum; writes nothing else.
import hashlib, json, re, sys
from pathlib import Path

R6D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6')
V005 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
            'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
COPY_REL = 'addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md'

out = Path(sys.argv[1]).resolve()
expected = sys.argv[2]
if out != R6D:
    raise SystemExit('OUT_DIR must be the r6 folder: %s' % out)
if not re.fullmatch(r'[0-9a-f]{64}', expected):
    raise SystemExit('EXPECTED_SHA256 must be 64 lowercase hex characters')
b = V005.read_bytes()
got = hashlib.sha256(b).hexdigest()
if got != expected:
    print(json.dumps({'refused': 'V005_LIVE_SHA_DIFFERS', 'live_sha256': got, 'live_bytes': len(b), 'expected': expected}))
    raise SystemExit(4)
dst = out / COPY_REL
if not dst.parent.is_dir():
    raise SystemExit('missing folder %s' % dst.parent)
with open(dst, 'xb') as f:
    f.write(b)
back = dst.read_bytes()
if back != b:
    raise SystemExit('the byte copy does not read back equal')
heads = [m.group(1).decode() for m in re.finditer(rb'(?m)^## (A\d+):', back)]
nums = [int(h[1:]) for h in heads]
print(json.dumps({'copy': str(dst), 'sha256': hashlib.sha256(back).hexdigest(), 'bytes': len(back), 'entries': len(heads),
                  'distinct_entries': len(set(heads)), 'newest': 'A%d' % max(nums), 'oldest': 'A%d' % min(nums),
                  'first_in_file_order': heads[:8], 'last_in_file_order': heads[-4:]}))
