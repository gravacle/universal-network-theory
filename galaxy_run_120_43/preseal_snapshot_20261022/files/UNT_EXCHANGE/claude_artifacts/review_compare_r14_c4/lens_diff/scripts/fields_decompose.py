# Claude4 lens_diff (3): decompose FIELDS_R14_CX1V002 into (r14 preamble) + (r13 FIELDS-of-record explanation part) + (generated r14
# contract FIELDS_R14_CX1V001) and test each part against bytes.  Read-only on author files; one exclusive write here.
import hashlib, json
from pathlib import Path
C = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2')
OUT = Path(__file__).resolve().parent.parent / 'out' / 'FIELDS_DECOMPOSE_C4.json'
v2 = (C / 'r14/FIELDS_R14_CX1V002.md').read_bytes()
v1 = (C / 'r14/FIELDS_R14_CX1V001.md').read_bytes()
r13 = (C / 'r13/FIELDS_R13_CX3V001.md').read_bytes()
r12g = (C / 'r12/FIELDS_R12_CX3V002.md').read_bytes()
H = lambda b: hashlib.sha256(b).hexdigest()
res = {'sha': {'v2': H(v2), 'v1': H(v1), 'r13_fields_of_record': H(r13), 'r12_generated': H(r12g)}}
# r13 FIELDS of record = r13 explanation + 'The inherited field specification follows verbatim.\n\n' + r12 generated contract?
marker13 = b'The inherited field specification follows verbatim.\n\n'
i = r13.find(marker13)
res['r13_tail_after_marker_eq_r12_generated'] = r13[i + len(marker13):] == r12g
r13_expl = r13[:i]
# r14 V002 = preamble + r13 explanation (minus its sha block) + '## Current generated contract\n\n' + v1 ?
marker14 = b'## Current generated contract\n\n'
j = v2.find(marker14)
res['v2_tail_after_marker_eq_v1'] = v2[j + len(marker14):] == v1
k = v2.find(b'# FIELDS R13')
pre14 = v2[:k]
mid14 = v2[k:j]
res['r14_preamble'] = pre14.decode()
# r13 explanation with the sha block removed
sb_start = r13_expl.find(b'SHA256 from bytes:')
sb_end = r13_expl.find(b'---\n', sb_start) + len(b'---\n')
removed = r13_expl[sb_start:sb_end]
res['r13_sha_block_removed_text'] = removed.decode()
res['mid14_eq_r13_expl_minus_sha_block'] = mid14 == r13_expl[:sb_start] + r13_expl[sb_end:]
res['mid14_eq_r13_expl_minus_sha_block_and_trailing'] = None
if not res['mid14_eq_r13_expl_minus_sha_block']:
    a = r13_expl[:sb_start] + r13_expl[sb_end:]
    p = 0
    while p < min(len(a), len(mid14)) and a[p] == mid14[p]:
        p += 1
    res['first_difference_at'] = p
    res['r13_side'] = a[max(0, p - 40):p + 80].decode('utf-8', 'replace')
    res['r14_side'] = mid14[max(0, p - 40):p + 80].decode('utf-8', 'replace')
# v1 vs r12 generated: exactly the ', I4' insertion?
res['v1_minus_r12g_bytes'] = len(v1) - len(r12g)
res['v1_eq_r12g_plus_I4'] = v1 == r12g.replace(b'HARMONICS, SR_K; every other gate', b'HARMONICS, SR_K, I4; every other gate', 1) and \
    r12g.count(b'HARMONICS, SR_K; every other gate') == 1
# other places in the generated contract that name I4 or SR_K with the token (wording that may now be incomplete)
lines = v1.decode().splitlines()
res['v1_lines_naming_token_or_A88'] = [[n + 1, l[:240]] for n, l in enumerate(lines) if 'A88' in l or 'PRODUCED_AFTER_THE_SEAL' in l]
res['v1_lines_naming_I4'] = [[n + 1, l[:240]] for n, l in enumerate(lines) if 'I4' in l]
with open(OUT, 'x') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))
