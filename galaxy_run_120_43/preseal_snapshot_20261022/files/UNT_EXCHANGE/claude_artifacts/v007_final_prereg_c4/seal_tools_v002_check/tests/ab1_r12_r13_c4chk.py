# Claude4 helper: A102 A-B1 class on r12 vs r13, and on seal tools r2 (json_or_text). Writes fixtures only into a new run folder here.
import json, os, sys, time, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
CA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
sys.path.insert(0, str(CA / 'v007_final_prereg_c4/seal_tools_v002/r2'))
import seal_common_c4v002 as C
import print_driver_build_record_c4v002 as T5
R12 = (str(CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'), '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28')
R13 = (str(CA / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'), 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157')
DSHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
run = HERE / ('ab1_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()))
run.mkdir()
big = '9' * 5000
cases = {
    'A_B1_bigint_dup': '{"driver": "%s", "verdict": "PASS", "n": %s, "verdict": "FAIL"}\n' % (DSHA, big),
    'dup_plain': '{"driver": "%s", "verdict": "PASS", "verdict": "FAIL"}\n' % DSHA,
    'truncated_json_dup': '{"driver": "%s", "verdict": "PASS", "verdict": "FAIL"\n' % DSHA,
    'nan_constant': '{"driver": "%s", "verdict": "PASS", "x": NaN}\n' % DSHA,
    'utf8_bom_dup': '﻿{"driver": "%s", "verdict": "PASS", "verdict": "FAIL"}\n' % DSHA,
    'prose_fail_mentions_PASS': 'Check of driver %s: verdict FAIL (the PASS criteria were not met).\n' % DSHA,
}
out = {}
M12, M13 = C.load_reviewed_compare(*R12), C.load_reviewed_compare(*R13)
for name, text in cases.items():
    p = run / ('CHECK_%s.txt' % name)
    with open(p, 'x', encoding='utf-8') as f:
        f.write(text)
    try:
        C.json_or_text(p.read_bytes())
        tools = 'ACCEPTED (json or text)'
    except Exception as e:
        tools = 'REFUSED %s' % type(e).__name__
    r5res, _ = T5.record_bytes(R13[0], R13[1], str(p))
    out[name] = {'r12_check_record_codes': M12.check_record_codes(str(p), DSHA), 'r13_check_record_codes': M13.check_record_codes(str(p), DSHA),
                 'seal_tools_json_or_text': tools, 'tool5_on_r13': [f['code'] for f in r5res['failures']] or 'PASS'}
print(json.dumps(out, indent=1))
with open(run / 'AB1_RESULTS_C4CHK.json', 'x') as f:
    json.dump(out, f, indent=1)
