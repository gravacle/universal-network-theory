"""Claude: second-order (h^2) diagonal energy on the ice manifold with a binary Record pattern.
Flip of edge e=(u,v) from ice (all d=2): E = 2Ud + Delta*(delta - lamR*s_e), Delta = 1-2n_e, s_e=q_u+q_v.
E2 = -h^2 sum_e [n_e/E_occ(s_e) + (1-n_e)/E_emp(s_e)] = const - h^2 sum_e n_e g(s_e), g=1/E_occ-1/E_emp.
Any f(s) on {0,1,2}: f(0)+(f1-f0)(q_u+q_v)+(f2-2f1+f0) q_u q_v; sum_e n_e(q_u+q_v)=sum_v q_v d_v = 2 sum q (ice),
so the ONLY configuration-dependent piece is  -h^2 * gamma * sum_e n_e q_u q_v,  gamma = g(2)-2g(1)+g(0)  (all orders in lamR).
Brute-force check on random small ice states of a 4-regular graph confirms."""
from fractions import Fraction as F
import itertools, random
def g(s,Ud,dl,lam): return 1/(2*Ud-(dl-lam*s)) - 1/(2*Ud+(dl-lam*s))
Ud,dl,lam=F(1),F(0),F(1,8)
gam=g(2,Ud,dl,lam)-2*g(1,Ud,dl,lam)+g(0,Ud,dl,lam)
for hr in (F(1,5),F(1,10)):
    field=-hr**2*gam; ring=F(63,8)*hr**6
    print(f"h/Ud={hr}: ww-edge field per occupied ww edge = {float(field):.3e} Ud; ring 63/8 h^6/Ud^5 = {float(ring):.3e} Ud; ratio = {float(field/ring):.3f}")
# brute force: K5 is 4-regular (5 vertices, 10 edges); ice = every vertex has exactly 2 occupied edges
V=range(5); E=list(itertools.combinations(V,2)); random.seed(1)
ice=[c for c in itertools.product((0,1),repeat=10) if all(sum(c[i] for i,e in enumerate(E) if v in e)==2 for v in V)]
q=[1,1,0,1,0]
def E2(c):
    t=F(0)
    for i,(u,v) in enumerate(E):
        s=q[u]+q[v]; D=1-2*c[i]; t+= -1/(2*Ud+D*(dl-lam*s))
    return t
def pred(c): return -gam*sum(c[i] for i,(u,v) in enumerate(E) if q[u] and q[v])
vals={(E2(c)-pred(c)) for c in ice}
print("ice states:",len(ice),"| E2 minus predicted ww term constant across all ice states:",len(vals)==1)
print("E2 spread across ice states (units h^2/Ud):",float(max(map(E2,ice))-min(map(E2,ice))))
