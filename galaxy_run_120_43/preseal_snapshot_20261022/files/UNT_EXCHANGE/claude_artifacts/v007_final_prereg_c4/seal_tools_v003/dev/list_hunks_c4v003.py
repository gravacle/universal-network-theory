# dev helper (work copy): list the non-rename hunks of dev/ v003 sources vs r2, with their first changed line
import difflib, sys
from pathlib import Path
R2 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
D = Path(__file__).resolve().parent
for n in ('seal_common', 'check_frozen_addendum', 'check_sealed_compare', 'check_slot_fill', 'build_seal_record', 'print_driver_build_record'):
    a = (R2 / (n + '_c4v002.py')).read_text().splitlines()
    b = (D / (n + '_c4v003.py')).read_text().splitlines()
    k = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        k += 1
        al, bl = a[i1:i2], b[j1:j2]
        if len(al) == len(bl) and al and all(x.replace('c4v002', 'c4v003') == y for x, y in zip(al, bl)):
            continue
        first = (bl[0] if bl else al[0]).strip()
        print('%s_c4v003.py | %d | -%d +%d | %s' % (n, k, len(al), len(bl), first[:150]))
