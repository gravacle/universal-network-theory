import itertools, numpy as np
pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
P=np.array([[1 if a in A else 0 for a in range(4)] for A in pairs],float)  # 6x4 pair-port incidence
# irreps on pair space
one=np.ones(6)/np.sqrt(6)
U,s,Vt=np.linalg.svd(P.T); ker=Vt[np.sum(s>1e-9):].T  # ker P^T = E (dim2)
imP=np.linalg.qr(P)[0]   # A1+T2 (dim4)
PE=ker@ker.T; PA=np.outer(one,one); PT=imP@imP.T-PA
sig=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)
print("d=2 ice states: occupied pair, e, T2(ZZ), E(ZZ), T2(nn)")
for occ in pairs:
    n=np.zeros(4); n[list(occ)]=1; Z=1-2*n
    ZZ=np.array([Z[a]*Z[b] for a,b in pairs]); nn=np.array([n[a]*n[b] for a,b in pairs])
    e=(n[:,None]*sig).sum(0)
    print(occ, e, np.round(PT@ZZ,6).tolist(), np.round(PE@ZZ,3).tolist(), np.round(PT@nn,3).tolist())
# check: T2(nn) linear in e? map T2 coords to e via least squares
X=[];Y=[]
for occ in pairs:
    n=np.zeros(4); n[list(occ)]=1
    nn=np.array([n[a]*n[b] for a,b in pairs]); e=(n[:,None]*sig).sum(0)
    X.append(e); Y.append(PT@nn)
X=np.array(X);Y=np.array(Y)
C,res,rk,_=np.linalg.lstsq(X,Y,rcond=None)
print("T2(nn) = e @ C exactly? residual", np.abs(X@C-Y).max())
