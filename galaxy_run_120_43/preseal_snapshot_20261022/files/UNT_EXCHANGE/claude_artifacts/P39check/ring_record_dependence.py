"""Claude independent cross-check for P-39(a): record-dependent sixth-order ring coefficient.
Hexagon edges 0..5 alternating occupied/empty; vertex v sits between edges v and v+1.
Intermediate energy = sum over defect vertices of [Ud*d^2 - lamR*d*q_v] (p=0, only -lamR d q kept).
Coefficient multiplies h^6: g = -(sum over 720 orderings of prod_{k=1..5} 1/E_k)."""
import itertools
from fractions import Fraction as F
dn=[-1 if i%2==0 else +1 for i in range(6)]
def ring_coeff(Ud,lamR,q):
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
    return -tot
if __name__=="__main__":
    base=ring_coeff(F(1),F(0),[0]*6); print("blank:",base)
    for lam in (F(1,8),F(1,4)):
        for name,q in (("all written",[1]*6),("one written vertex",[1,0,0,0,0,0])):
            g=ring_coeff(F(1),lam,q); print(f"lamR={lam} {name}: {float(g):.6f}  rel {float(g/base-1):+.5f}")
