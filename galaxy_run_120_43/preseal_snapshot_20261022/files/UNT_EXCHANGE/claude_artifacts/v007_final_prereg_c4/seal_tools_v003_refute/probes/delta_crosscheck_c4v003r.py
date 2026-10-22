# Claude4 v003 refuter: mechanical cross-check of DELTA_V002R2_TO_V003.md against difflib opcodes over the r2 and v003 source lines
# (read-only; prints a JSON summary). Every DELTA hunk header must match one non-equal opcode, and every opcode one header.
import difflib, hashlib, json, re, sys
from pathlib import Path

V3 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v003')
R2 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
D = (V3 / 'DELTA_V002R2_TO_V003.md').read_text()
names = ('seal_common', 'check_frozen_addendum', 'check_sealed_compare', 'check_slot_fill', 'build_seal_record', 'print_driver_build_record')
hdr = re.compile(r'^### (\S+) hunk (\d+): r2 (?:L(\d+)-(\d+)|after L(\d+)), v003 (?:L(\d+)-(\d+)|after L(\d+)) -- \*\*(.+?)\*\*$', re.M)
heads = {}
for m in hdr.finditer(D):
    f = m.group(1)
    r2r = (int(m.group(3)), int(m.group(4))) if m.group(3) else ('after', int(m.group(5)))
    v3r = (int(m.group(6)), int(m.group(7))) if m.group(6) else ('after', int(m.group(8)))
    heads.setdefault(f, []).append((r2r, v3r, m.group(9)))
out = {'files': {}, 'delta_sha256': hashlib.sha256((V3 / 'DELTA_V002R2_TO_V003.md').read_bytes()).hexdigest()}
allok = True
for n in names:
    a = (R2 / (n + '_c4v002.py')).read_text().splitlines(keepends=True)
    b = (V3 / (n + '_c4v003.py')).read_text().splitlines(keepends=True)
    ops = [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op[0] != 'equal']
    mine = []
    for tag, i1, i2, j1, j2 in ops:
        r2r = (i1 + 1, i2) if i2 > i1 else ('after', i1)
        v3r = (j1 + 1, j2) if j2 > j1 else ('after', j1)
        mine.append((r2r, v3r))
    theirs = [(x[0], x[1]) for x in heads.get(n + '_c4v003.py', [])]
    added = sum(j2 - j1 for _, i1, i2, j1, j2 in ops)
    removed = sum(i2 - i1 for _, i1, i2, j1, j2 in ops)
    ok = mine == theirs
    allok &= ok
    out['files'][n] = {'opcodes': len(ops), 'delta_hunks': len(theirs), 'ranges_equal': ok, 'lines_added': added, 'lines_removed': removed,
                       'reasons': sorted({x[2] for x in heads.get(n + '_c4v003.py', [])})}
out['all_ranges_equal'] = allok
out['reason_counts'] = {}
for f, hs in heads.items():
    for h in hs:
        out['reason_counts'][h[2]] = out['reason_counts'].get(h[2], 0) + 1
print(json.dumps(out, indent=1))
