# Claude4 lens_diff: is SOURCE_DELTA_CX1V001.diff exactly difflib.unified_diff(r13, r14) (n=3, empty names)?  Read-only.
import difflib, json
from pathlib import Path
C = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2')
a = (C / 'r13/kmax_tail_compare_c2v007_r13_cx3v001.py').read_text().splitlines(True)
b = (C / 'r14/kmax_tail_compare_c2v007_r14_cx1v001.py').read_text().splitlines(True)
d = ''.join(difflib.unified_diff(a, b))
sd = json.loads((C / 'r14/SOURCE_DELTA_CX1V001.json').read_bytes())
print('SOURCE_DELTA.diff equals difflib.unified_diff(r13, r14) n=3:', sd['diff'] == d, len(sd['diff']), len(d))
print('parent/candidate pins:', sd['parent']['sha256'][:8], sd['candidate']['sha256'][:8], 'exact_inverse_restores_parent:', sd['exact_inverse_restores_parent'])
