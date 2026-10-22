# Claude4 seal tools v003 (BUILD helper, work copy): smoke of the final tool 1 on prereg r5, its pinned read copy and a FROZEN-named copy of
# the open V005 written into dev/smoke2/<stamp>/. Run under the fence. Writes only there.
import json, sys, time
from pathlib import Path
DEV = Path(__file__).resolve().parent
sys.path.insert(0, str(DEV))
import seal_common_c4v003 as C
import check_frozen_addendum_c4v003 as T1
R5 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json')
RC = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md')
OPEN = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
d = DEV / 'smoke2' / time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
d.mkdir()
fz = d / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md'
with open(fz, 'xb') as f:
    f.write(OPEN.read_bytes())
print('frozen copy', C.sha(fz), fz.stat().st_size)
r = T1.run(str(R5), str(fz), None, (), True, None, str(RC))
print('no dispositions:', r['verdict'], sorted({x['code'] for x in r['failures']}), 'required', r['dispositions_required'], 'changed', r['changed_sections'])
secs = T1.sections(fz.read_bytes())
rows = [{'entry': e, 'disposition': 'no_change', 'reason': 'SMOKE ROW (not root\'s disposition of %s)' % e, 'section_sha256': C.sha_bytes(secs[int(e[1:])][0][1])}
        for e in r['dispositions_required']]
dp = d / 'DISP_SMOKE.json'
with open(dp, 'x') as f:
    f.write(json.dumps({'schema': C.DISPOSITIONS_SCHEMA, 'frozen_addendum_sha256': C.sha(fz), 'entries': rows}, indent=1) + '\n')
r = T1.run(str(R5), str(fz), None, (), True, (str(dp), C.sha(dp)), str(RC))
print('with dispositions:', r['verdict'], sorted({x['code'] for x in r['failures']}), sorted({x['code'] for x in r['notes']}), r['addendum_at_text_of_record'])
r = T1.run(str(R5), str(fz), None, (), True, (str(dp), C.sha(dp)), None)
print('no read copy:', r['verdict'], sorted({x['code'] for x in r['failures']}), sorted({x['code'] for x in r['notes']}))
r = T1.run(str(R5), str(fz), None, (), True, (str(dp), C.sha(dp)), str(fz))
print('frozen as read copy:', r['verdict'], sorted({x['code'] for x in r['failures']}))
