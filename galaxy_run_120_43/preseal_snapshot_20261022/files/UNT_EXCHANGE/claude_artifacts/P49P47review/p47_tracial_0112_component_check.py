"""Claude: per-h0-component readouts of the uniform state (own code)."""
import json, sys
from fractions import Fraction as F
from collections import Counter, defaultdict
PLAN = "/Users/bgm/Research/UNT_EXCHANGE/lanes/P44_CODEX3/ROOT_COMPLETE_NATIVE_REBLOCK_V001/COMPLETE_REBLOCK_PLAN.json"
plan = json.load(open(PLAN))
by = defaultdict(list)
for p in plan["pieces"]:
    for s in p["states"]: by[p["component"]].append(tuple(s))
res = {}
b = lambda x, i: (x >> i) & 1
for c, S in sorted(by.items()):
    n = len(S); born = [t for t in S if t[0] == 1]
    W = Counter("%d%d" % (b(t[3], 2), b(t[3], 3)) for t in born)
    pa = [t for t in S if b(t[2], 0)]
    res[c] = dict(n=n, old=n - len(born), born=len(born),
                  new_word_given_present={k: str(F(W[k], len(born))) for k in ("00", "01", "10", "11")},
                  q_c=str(F(sum(b(t[3], 2) for t in S), n)), q_d=str(F(sum(b(t[3], 3) for t in S), n)),
                  q_a=str(F(sum(b(t[3], 0) for t in S), n)), q_b=str(F(sum(b(t[3], 1) for t in S), n)),
                  center_p=str(F(len(pa), n)),
                  q_c_given_pa=(str(F(sum(b(t[3], 2) for t in pa), len(pa))) if pa else "UNDEFINED"),
                  C_ab=str(F(sum(b(t[3],0)*b(t[3],1) for t in S), n) - F(sum(b(t[3],0) for t in S), n)*F(sum(b(t[3],1) for t in S), n)),
                  C_cd=str(F(sum(b(t[3],2)*b(t[3],3) for t in S), n) - F(sum(b(t[3],2) for t in S), n)*F(sum(b(t[3],3) for t in S), n)))
# old-only sanity: old states' q words in component 0
json.dump(res, open(sys.argv[1], "w"), indent=1, sort_keys=True)
print(json.dumps(res, indent=1, sort_keys=True))
