# Claude4 r6 helper, continuation run 2: unified diffs of the r6 generator against r5's generator and against the first r6 builder's draft.
# usage: python3 -I -B make_diffs_c4r6.py GENERATOR_SHA256
# Every input is verified from bytes (r5 p3 ef00666c, the draft 8787e164, the r6 generator = GENERATOR_SHA256); writes, by exclusive create:
#   tools/DIFF_GEN_R5P3_TO_C4V006_R2.diff  (r5 make_v007_final_draft_c4v005_p3.py -> r6 make_v007_final_draft_c4v006_r2.py)
#   tools/DIFF_GEN_C4V006_DRAFT_TO_R2.diff (the first builder's make_v007_final_draft_c4v006.py -> make_v007_final_draft_c4v006_r2.py)
import difflib, hashlib, json, sys
from pathlib import Path

R6T = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/tools')
R5P3 = (Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/tools/make_v007_final_draft_c4v005_p3.py'),
        'ef00666cd85ba280f781d8bbb16223573d915bec4f9b4fe503d20e4c23026a30')
DRAFT = (R6T / 'make_v007_final_draft_c4v006.py', '8787e164d5eecb90da281ef69edb113131de442d8635eea6f26803fc39518cbe')
GEN = R6T / 'make_v007_final_draft_c4v006_r2.py'


def read(p, want):
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    if h != want:
        raise SystemExit('%s hashes to %s, not %s' % (p, h, want))
    return b.decode('utf-8').splitlines(keepends=True)


gen_sha = sys.argv[1]
g = read(GEN, gen_sha)
outs = {}
for name, (p, h) in (('DIFF_GEN_R5P3_TO_C4V006_R2.diff', R5P3), ('DIFF_GEN_C4V006_DRAFT_TO_R2.diff', DRAFT)):
    a = read(p, h)
    d = ''.join(difflib.unified_diff(a, g, fromfile='%s (sha256 %s)' % (p, h), tofile='%s (sha256 %s)' % (GEN, gen_sha), n=3))
    if not d.endswith('\n'):
        d += '\n'
    outs[name] = d.encode('utf-8')
for name in outs:
    if (R6T / name).exists():
        raise SystemExit('exists: %s' % name)
res = {}
for name, data in outs.items():
    with open(R6T / name, 'xb') as f:
        f.write(data)
    res[name] = {'sha256': hashlib.sha256((R6T / name).read_bytes()).hexdigest(), 'bytes': len(data),
                 'lines_added': sum(1 for ln in data.decode().split('\n') if ln.startswith('+') and not ln.startswith('+++')),
                 'lines_removed': sum(1 for ln in data.decode().split('\n') if ln.startswith('-') and not ln.startswith('---'))}
print(json.dumps(res, indent=1))
