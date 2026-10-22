# xwrite.py -- exclusive-create writer for r5_check (Claude4 helper).
# usage: python3 -I -B xwrite.py <path> [--append]  < content
# Without --append the file is created with open(path,'x') and refuses if it exists.
# --append is allowed only for files whose basename is PARTIAL.md.
import sys, os
ROOT = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check/'
p = os.path.abspath(sys.argv[1])
if not p.startswith(ROOT):
    sys.exit('REFUSED: outside r5_check: ' + p)
data = sys.stdin.read()
if len(sys.argv) > 2 and sys.argv[2] == '--append':
    if os.path.basename(p) != 'PARTIAL.md':
        sys.exit('REFUSED: append only for PARTIAL.md')
    with open(p, 'a') as f:
        f.write(data)
else:
    with open(p, 'x') as f:
        f.write(data)
print('wrote', p, len(data.encode()), 'bytes')
