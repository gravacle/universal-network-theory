# Claude4 r6 helper, continuation run 2: write r6/HASHES_R6.txt (exclusive create): "sha256  absolute path" for every file of record of
# prereg r6, each hashed from bytes, in a fixed order, so that `shasum -a 256 -c HASHES_R6.txt` re-verifies the set.
# usage: python3 -I -B make_hashes_c4r6.py
import hashlib, json
from pathlib import Path

R6D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6')
R5D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5')
FILES = [R5D / 'case_block/CASE_BLOCK_V007_C4V001.json', R5D / 'out/CASE_BLOCK_BUILD_C4V001.json',
         R6D / 'addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md',
         R6D / 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json', R6D / 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.md', R6D / 'ENTRY_TABLE_R6.md',
         R6D / 'SEAL_CHECKLIST_R6.md', R6D / 'ROOT_ITEMS_R6.md', R6D / 'CLAUSE_SOURCE_MAP_R6.md', R6D / 'DELTA_R5_R6.md',
         R6D / 'out/VERIFY_R6_C4R6.json',
         R6D / 'tools/make_v007_final_draft_c4v006_r2.py', R6D / 'tools/verify_r6_c4r6.py', R6D / 'tools/copy_addendum_c4r6_v2.py',
         R6D / 'tools/run_fenced_c4r6_v2.py', R6D / 'tools/fence_c4v002.py', R6D / 'tools/make_diffs_c4r6.py', R6D / 'tools/make_hashes_c4r6.py',
         R6D / 'tools/DIFF_GEN_R5P3_TO_C4V006_R2.diff', R6D / 'tools/DIFF_GEN_C4V006_DRAFT_TO_R2.diff']
out = R6D / 'HASHES_R6.txt'
if out.exists():
    raise SystemExit('HASHES_R6.txt exists')
missing = [str(p) for p in FILES if not p.is_file()]
if missing:
    raise SystemExit('missing: %s' % missing)
lines = ['%s  %s' % (hashlib.sha256(p.read_bytes()).hexdigest(), p) for p in FILES]
data = ('\n'.join(lines) + '\n').encode('utf-8')
with open(out, 'xb') as f:
    f.write(data)
if out.read_bytes() != data:
    raise SystemExit('HASHES_R6.txt does not read back equal')
print(json.dumps({'written': str(out), 'sha256': hashlib.sha256(data).hexdigest(), 'entries': len(lines)}, indent=1))
