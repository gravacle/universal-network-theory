# dev smoke (work copy): compile the six v003 dev sources and run tool 1 on prereg r5 vs the fixtures V005 read copy (dry-run flags).
import json, py_compile, sys
from pathlib import Path
D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
for n in ('seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py', 'check_slot_fill_c4v003.py',
          'build_seal_record_c4v003.py', 'print_driver_build_record_c4v003.py'):
    compile((D / n).read_text(), str(D / n), 'exec')
import seal_common_c4v003 as C, check_frozen_addendum_c4v003 as T1
R5 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'
FZ = str(D.parent / 'fixtures/V005_ADDENDUM_READ_COPY_C4V003.md')
r = T1.run(R5, FZ, None, (), True)
print(r['verdict'], [f['code'] for f in r['failures']], r['dispositions_required'], [n['code'] for n in r['notes']])
r = T1.run(R5, FZ, None, ('A102',), True)
print(r['verdict'], [f['code'] for f in r['failures']])
print(C.strict_json_typed(b'{"a": ' + b'9' * 5000 + b'}', 'X')[2][0], C.strict_json_typed(b'{"a": NaN}', 'X')[2][0],
      C.strict_json_typed(b'{"a": 1, "a": 2}', 'X')[2][0], C.strict_json_typed(b'\xff', 'X')[2][0], C.strict_json_typed(b'\xef\xbb\xbf{}', 'X')[2][0],
      C.strict_json_typed(b'[' * 100000, 'X')[2][0])
