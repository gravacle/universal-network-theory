# make_report_v2_r5chk.py -- writes REPORT_R5CHK_C4V002.md from tools/report_template_v2_r5chk.md (shas from bytes at write time).
import sys, os, re, hashlib
D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check'
UTC = sys.argv[1]
def full(p):
    q = p if p.startswith('/') else os.path.join(D, p)
    return hashlib.sha256(open(q, 'rb').read()).hexdigest()
T = open(os.path.join(D, 'tools', 'report_template_v2_r5chk.md')).read()
out = re.sub(r'\{S:([^}]+)\}', lambda m: full(m.group(1)), T)
out = re.sub(r'\{P:([^}]+)\}', lambda m: full(m.group(1))[:8], out)
out = out.replace('{UTC}', UTC)
assert '{S:' not in out and '{P:' not in out and '{UTC}' not in out
p = os.path.join(D, 'REPORT_R5CHK_C4V002.md')
with open(p, 'x') as f:
    f.write(out)
print('wrote', p, hashlib.sha256(open(p, 'rb').read()).hexdigest())
