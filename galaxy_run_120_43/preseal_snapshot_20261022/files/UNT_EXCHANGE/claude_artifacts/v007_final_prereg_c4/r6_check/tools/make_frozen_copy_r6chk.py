# Claude4 r6 refute helper (r6_check), check (6) input: a FROZEN-named byte copy of the live, closed V005 addendum inside
# r6_check/scratch, for a seal-tool-1 DRY RUN only (never a seal input; not at path_to_be). Refuses before writing unless the
# live bytes hash to the closed sha; exclusive create; re-reads and re-hashes the copy.
# usage: python3 -I -B make_frozen_copy_r6chk.py LIVE_V005 CLOSED_SHA OUT_COPY
import hashlib, sys

live, want, out = sys.argv[1:4]
raw = open(live, 'rb').read()
got = hashlib.sha256(raw).hexdigest()
if got != want:
    print('REFUSED: live V005 is %s, expected %s' % (got, want))
    sys.exit(2)
with open(out, 'xb') as fh:
    fh.write(raw)
back = open(out, 'rb').read()
print('copy', hashlib.sha256(back).hexdigest(), len(back), 'equal_to_live', back == raw)
sys.exit(0 if back == raw and hashlib.sha256(back).hexdigest() == want else 3)
