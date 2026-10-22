# Claude4 helper: the builder's copied blinding constants equal r12's and r13's own (FORMAL claim "copied verbatim", checked from objects)
import sys
from pathlib import Path
CA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
sys.path.insert(0, str(CA / 'v007_final_prereg_c4/seal_tools_v002/r2'))
import seal_common_c4v002 as C
import build_seal_record_c4v002 as T4
import check_slot_fill_c4v002 as T3
for tag, p, h in (('r12', CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py', '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28'),
                  ('r13', CA / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157')):
    M = C.load_reviewed_compare(str(p), h)
    print(tag, 'NUMBER_RX equal:', T4.NUMBER_RX.pattern == M._RE_NUMBER.pattern, '| ALLOWED tokens equal:', T4.ALLOWED_NUMBER_TOKENS == M.ALLOWED_NUMBER_TOKENS,
          '| HEX64 equal:', T4.HEX64_ANY.pattern == M._RE_HEX64.pattern, '| SCHEMA_REPORT', M.SCHEMA_REPORT, '| GATE_SCHEMA', M.GATE_SCHEMA,
          '| COMPARE_API present:', all(hasattr(M, a) for a in T3.COMPARE_API), '| NGC/DDO M_s', M.NGC_GAS_M_S_A57, M.PRODUCTION_GAS_M_S_A57)
