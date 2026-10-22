import sys, importlib.util, numpy as np
from fractions import Fraction as F
sp=importlib.util.spec_from_file_location("rs",sys.argv[1]); rs=importlib.util.module_from_spec(sp); sp.loader.exec_module(rs)
rng=np.random.default_rng(5); p,q=3,5
def rmat(r,c,s): return [[F(int(x),4) for x in row] for row in rng.integers(-s,s+1,(r,c))]
A=rmat(p,p,1); A=[[ (A[i][j]+A[j][i])/2 for j in range(p)] for i in range(p)]
D=rmat(q,q,1); D=[[ (D[i][j]+D[j][i])/2 + (F(12) if i==j else 0) for j in range(q)] for i in range(q)]
B=rmat(p,q,2); C=rmat(q,q,2); C=[[ (C[i][j]+C[j][i])/2 for j in range(q)] for i in range(q)]
out=rs.coefficients(A,D,B,C); K=out["coefficients"]
f=lambda M: np.array([[float(x) for x in r] for r in M])
for h in (0.2,0.1,0.05):
    H=np.block([[f(A),h*f(B)],[h*f(B).T,f(D)+h*f(C)]])
    ex=np.sort(np.linalg.eigvalsh(H))[:p]
    Kh=sum(h**n*f(K[n]) for n in range(7)); ap=np.sort(np.linalg.eigvalsh(Kh))
    print(f"h={h}: max|eig err| = {np.abs(ex-ap).max():.3e}")
print("gap lower:",float(out["certified_sylvester_gap_lower"]))
