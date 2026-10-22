# patch tests/test_c4chk_v2.py -> tests/test_c4chk_v3_r13.py: the same checks with compare r13 f5adfd11 (A102 fix round, frozen
# 21:22:22Z, delta reviews pending) as the reviewed source; every replacement must match exactly once, else exit 1
import ast, sys
from pathlib import Path
T = Path(__file__).resolve().parent.parent / 'tests'
src = (T / 'test_c4chk_v2.py').read_text(encoding='utf-8')
R = [
    ("R12 = CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'\n", "R12 = CA / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'   # r13 in the R12 slot of this harness\n"),
    ("R12_IMPL = CA / 'v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md'\n", "R12_IMPL = CA / 'v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md'\n"),
    ("R12: '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28', R12_IMPL: 'ef0db32dc5d8c099d9346bb33cfabdc52cd73bdcd5ffdc91dc7cc922c3b9484c',",
     "R12: 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157', R12_IMPL: '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3',"),
    ("'harness': 'test_c4chk_v2.py'", "'harness': 'test_c4chk_v3_r13.py'"),
    ("'run_v2_' + stamp", "'run_v3_r13_' + stamp"),
    ("'TEST_RESULTS_C4CHK_V2.json'", "'TEST_RESULTS_C4CHK_V3_R13.json'"),
]
for old, new in R:
    n = src.count(old)
    if n != 1:
        print('REPLACEMENT_COUNT', n, repr(old[:70])); sys.exit(1)
    src = src.replace(old, new)
ast.parse(src)
if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
    print('DRY_RUN_OK', len(src)); sys.exit(0)
with open(T / 'test_c4chk_v3_r13.py', 'x', encoding='utf-8') as f:
    f.write(src)
print('WROTE test_c4chk_v3_r13.py')
