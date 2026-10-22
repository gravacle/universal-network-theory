import sys, importlib.util, numpy as np
from fractions import Fraction as F
sp=importlib.util.spec_from_file_location("nf",sys.argv[1]); nf=importlib.util.module_from_spec(sp); sp.loader.exec_module(nf)
rng=np.random.default_rng(7)
defects=[0,0,1,1,2,2]; d=len(defects)
V=rng.integers(-3,4,(d,d)); V=(V+V.T)
Vf=[[F(int(x),8) for x in row] for row in V]
out=nf.normal_form(defects,Vf,order=8)
D=out["normal_form"]; f=lambda M: np.array([[float(x) for x in r] for r in M])
for eps in (0.08,0.04,0.02):
    H=np.diag(defects).astype(float)+eps*f(Vf)
    ex=np.sort(np.linalg.eigvalsh(H))[:2]
    Heff=sum(eps**n*f(D[n]) for n in range(9)); kept=out["zero_defect_indices"]
    ap=np.sort(np.linalg.eigvalsh(Heff[np.ix_(kept,kept)]))
    print(f"eps={eps}: max err of the 2 zero-defect levels = {np.abs(ex-ap).max():.3e}")
