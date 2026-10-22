# make_report_r5chk.py -- writes REPORT_R5CHK_C4V001.md (r5_check helper, Claude4). Every sha is computed from bytes at write time:
# a token {S:path} becomes the full sha256 of that file (path relative to r5_check/ or absolute), {P:path} its 8-hex prefix.
# usage: python3 -I -B make_report_r5chk.py UTC
import sys, os, re, hashlib
D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check'
UTC = sys.argv[1]
def full(p):
    q = p if p.startswith('/') else os.path.join(D, p)
    return hashlib.sha256(open(q, 'rb').read()).hexdigest()
T = open(os.path.join(D, 'tools', 'report_template_r5chk.md')).read()
out = re.sub(r'\{S:([^}]+)\}', lambda m: full(m.group(1)), T)
out = re.sub(r'\{P:([^}]+)\}', lambda m: full(m.group(1))[:8], out)
out = out.replace('{UTC}', UTC)
p = os.path.join(D, 'REPORT_R5CHK_C4V001.md')
with open(p, 'x') as f:
    f.write(out)
print('wrote', p, hashlib.sha256(out.encode()).hexdigest())
