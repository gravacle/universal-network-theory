# noop_r5chk_v2.py -- smoke target for run_fenced_r5chk.py (supersedes noop_r5chk.py, which ends in a stray heredoc line).
# Opens the open V005 and the frozen V004 addenda read-only (exception b) and tries a write-open of V005 (must be refused).
import hashlib
C2 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
add = C2 + 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
v4 = C2 + 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md'
print('V005 open read (exception b):', hashlib.sha256(open(add, 'rb').read()).hexdigest())
print('V004 read (exception b):', hashlib.sha256(open(v4, 'rb').read()).hexdigest())
try:
    open(add, 'ab')
    print('ADDENDUM WRITE OPEN: NOT REFUSED (BAD)')
except PermissionError as e:
    print('addendum write open refused:', str(e)[:70])
