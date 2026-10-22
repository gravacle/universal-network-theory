"""Claude independent table: 6th-order hexagon ring coefficient for all 64 binary Record words (own code, exact Fractions).
Hexagon edges 0..5 alternate occupied/empty starting with `start` (0: edge0 empty->dn=+1? see dn); vertex v between edges v and v+1.
Intermediate energy = sum_v [Ud*d_v^2 - lamR*d_v*q_v] (zero detuning, no carriers). Coefficient of h^6 = -(sum over 720 orderings prod 1/E_k).
Reported as |coefficient| (positive), so blank = 63/8 at Ud=1."""
import itertools, json, sys
from fractions import Fraction as F
def coeff(Ud, lamR, q, start):
    dn=[(-1 if (i+start)%2==0 else 1) for i in range(6)]
    tot=F(0)
    for perm in itertools.permutations(range(6)):
        p=F(1); fl=set()
        for k in range(5):
            fl.add(perm[k]); E=F(0)
            for v in range(6):
                d=(dn[v] if v in fl else 0)+(dn[(v+1)%6] if (v+1)%6 in fl else 0)
                if d: E+=Ud*d*d-lamR*d*q[v]
            p*=1/E
        tot+=p
    return tot
out={}
for lam in (F(1,8),F(1,2)):
    for start in (0,1):
        for w in range(64):
            q=[(w>>v)&1 for v in range(6)]
            out[f"lamR={lam} start={start} word={''.join(map(str,q))}"]=str(coeff(F(1),lam,q,start))
json.dump(out,open(sys.argv[1],'w'),indent=0)
print("blank lam=1/8:",out["lamR=1/8 start=0 word=000000"],"| all-written lam=1/2:",out["lamR=1/2 start=0 word=111111"])
vals=set(out.values()); print("distinct values:",len(vals))
