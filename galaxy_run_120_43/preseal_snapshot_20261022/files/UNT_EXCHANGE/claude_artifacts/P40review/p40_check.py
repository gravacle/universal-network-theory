"""Claude independent cross-check of Codex2 P40 V001 claims (own code; no Codex source used).
Hexagon edges alternate occupied/empty; flipping edges gives vertex defects d_v in {-1,0,1}.
Intermediate energy (Ud=1) = sum_v (d_v^2 + x d_v)  [sum_v d_v = 2 dN, mu dN = 2 Ud x dN].
T(x) = sum over 720 orderings of prod_k 2/E_k, so T(0)=252.  Exact Fractions, no sympy."""
import itertools
from fractions import Fraction as F
from collections import Counter
dn=[-1 if i%2==0 else 1 for i in range(6)]
terms=Counter()   # key: tuple of (a,b) factors for 2/(a+b x)
for perm in itertools.permutations(range(6)):
    fl=set(); fac=[]
    for k in range(5):
        fl.add(perm[k]); a=b=0
        for v in range(6):
            d=(dn[v] if v in fl else 0)+(dn[(v+1)%6] if (v+1)%6 in fl else 0)
            a+=d*d; b+=d
        fac.append((a,b))
    terms[tuple(sorted(fac))]+=1
poles={F(-a,b) for t in terms for a,b in t if b}; print("pole locations:",sorted(poles))
def T(x): 
    s=F(0)
    for t,m in terms.items():
        p=F(m)
        for a,b in t: p*=F(2)/(a+b*x)
        s+=p
    return s
N=16
def series():
    tot=[F(0)]*N
    for t,m in terms.items():
        s=[F(m)]+[F(0)]*(N-1)
        for a,b in t:
            g=[F(2,a)*F(-b,a)**n for n in range(N)]
            s=[sum(s[i]*g[n-i] for i in range(n+1)) for n in range(N)]
        tot=[u+v for u,v in zip(tot,s)]
    return tot
c=series()
print("T(0)=",T(F(0)),"| odd coeffs zero:",all(c[i]==0 for i in range(1,N,2)))
print("even coeffs:",[str(c[i]) for i in range(0,N,2)])
print("all even coeffs positive:",all(c[i]>0 for i in range(0,N,2)),"| c2/c0 =",c[2]/c[0])
xs=[F(i,1000) for i in range(-990,991,5)]; h=F(1,1000)
print("T'' > 0 on grid |x|<=0.99:",all(T(z+h)-2*T(z)+T(z-h)>0 for z in xs))
print("T increasing in x>0:",all(T(z+h)>T(z) for z in xs if z>0))
print("1-252/T(1/16)=",float(1-252/T(F(1,16)))," >= 33/1825=",float(F(33,1825)),":",1-252/T(F(1,16))>=F(33,1825))
r=F(1,1000); print("L(r=1/1000,x0=0)=",float(T(r)/252)," <= 200/199:",T(r)/252<=F(200,199))
print("T/252 <= (1-|x|)^-5 on grid:",all(T(z)/252<=1/(1-abs(z))**5 for z in xs))
for f in (F(0),F(1,8),F(1,4),F(1,2),F(1)):
    x0=f/4; print(f"benchmark f={f}: ell(1) = {float(T(x0-F(1,8))/T(x0)-1):+.6f}")
