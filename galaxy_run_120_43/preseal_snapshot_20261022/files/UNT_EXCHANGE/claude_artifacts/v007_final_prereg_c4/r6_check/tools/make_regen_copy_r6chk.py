# Claude4 r6 refute helper (r6_check): reproduction copy of the r6 generator. Byte-copies make_v007_final_draft_c4v006_r2.py
# (9d77a181, pinned) into r6_check/scratch/regen/tools/ with exactly ONE anchored edit: the OUT_DIR guard accepts only
# r6_check/scratch/regen/... (the original accepts only r6 or r6/scratch, which this stage may not write). Refuses unless the
# source hashes to the pin and the anchor occurs exactly once. Exclusive create.
# usage: python3 -I -B make_regen_copy_r6chk.py SRC SRC_SHA DST
import hashlib, sys

src, want, dst = sys.argv[1:4]
raw = open(src, 'rb').read()
if hashlib.sha256(raw).hexdigest() != want:
    print('REFUSED: generator sha')
    sys.exit(2)
old = (b"    if not (out == R6D or str(out).startswith(str(R6D / 'scratch') + '/')):\n"
       b"        raise SystemExit('OUT_DIR must be the r6 folder, or a folder inside r6/scratch for a dry run')\n")
new = (b"    if not str(out).startswith('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6_check/scratch/regen/'):  # r6_check: the only edit\n"
       b"        raise SystemExit('OUT_DIR must be inside r6_check/scratch/regen (r6_check reproduction copy)')\n")
if raw.count(old) != 1:
    print('REFUSED: anchor count %d' % raw.count(old))
    sys.exit(2)
out = raw.replace(old, new)
with open(dst, 'xb') as fh:
    fh.write(out)
print('regen copy', hashlib.sha256(out).hexdigest(), 'from', want, 'one edit')
