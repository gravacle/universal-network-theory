# Claude4 seal tools v002 helper: copy SRC bytes to a NEW file DST (exclusive create, never overwrite); print the sha256 of DST.
# usage: python3 -I -B xwrite_c4st2.py SRC DST
import hashlib, sys
src, dst = sys.argv[1], sys.argv[2]
b = open(src, 'rb').read()
with open(dst, 'xb') as f:
    f.write(b)
print(hashlib.sha256(open(dst, 'rb').read()).hexdigest(), len(b), dst)
