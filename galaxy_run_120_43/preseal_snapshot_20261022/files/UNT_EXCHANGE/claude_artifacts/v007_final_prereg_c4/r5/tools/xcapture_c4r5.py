# Claude4 r5 helper: copy stdin to a NEW file (exclusive create) and echo it. usage: CMD 2>&1 | python3 -I -B xcapture_c4r5.py FILE
import sys
data = sys.stdin.read()
with open(sys.argv[1], 'x') as f:
    f.write(data)
sys.stdout.write(data)
