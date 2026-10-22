# noop_r5chk.py -- smoke target for run_fenced_r5chk.py: opens two allowed files read-only and one in-folder write.
import sys, os, hashlib
add = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
print('V005 open read (exception b):', hashlib.sha256(open(add, 'rb').read()).hexdigest())
v4 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM.md'
print('V004 read (exception b):', hashlib.sha256(open(v4, 'rb').read()).hexdigest())
try:
    open(add, 'ab')
    print('ADDENDUM WRITE OPEN: NOT REFUSED (BAD)')
except PermissionError as e:
    print('addendum write open refused:', str(e)[:60])
EOF
