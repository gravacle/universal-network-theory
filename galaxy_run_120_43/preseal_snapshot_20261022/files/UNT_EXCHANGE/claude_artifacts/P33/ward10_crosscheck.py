"""Claude P-33: independent 10-component (spacetime) Ward / gauge-null cross-check harness.
Numerical (float64) known-answer controls for the P-32 V003 Section-8 spec; no native kernel.
Convention: eta=diag(-1,1,1,1); h_mu_nu symmetric; gauge mode h=p_mu xi_nu + p_nu xi_mu.
Coordinates h_A=(h00,h01,h02,h03,h11,h22,h33,h12,h13,h23); multiplicities w_A=(1,2,2,2,1,1,1,2,2,2)."""
import numpy as np
eta=np.diag([-1.,1,1,1]); IDX=[(0,0),(0,1),(0,2),(0,3),(1,1),(2,2),(3,3),(1,2),(1,3),(2,3)]
W=np.array([1,2,2,2,1,1,1,2,2,2.])
def up(t): return eta@t@eta
def fp(p,h,m2=0.0,spatial_only=False,temporal_defect=0.0):
    """Fierz-Pauli operator E(h)_mu_nu (linearized Einstein, up to overall sign), optional controls."""
    pu=eta@p; p2=p@pu; tr=np.trace(eta@h); php=pu@h@pu
    E=(p2*h - np.outer(p,h@pu) - np.outer(h@pu,p) + np.outer(p,p)*tr + eta*(php - p2*tr))
    E=E + m2*(h - eta*tr)                       # Fierz-Pauli mass term: breaks gauge invariance
    if spatial_only:                            # symmetric spatial-only embedding: static 3D FP on h_ij,
        k=p[1:]; hs=h[1:,1:]; k2=k@k; trs=np.trace(hs); khk=k@hs@k   # ignores h00,h0i entirely
        E3=(k2*hs-np.outer(k,hs@k)-np.outer(hs@k,k)+np.outer(k,k)*trs+np.eye(3)*(khk-k2*trs))
        E=np.zeros((4,4)); E[1:,1:]=E3
    if temporal_defect: E[0,0]+=temporal_defect*p2*h[0,0]
    return E
def coords(t): return np.array([t[i,j] for i,j in IDX])
def tensor(c):
    t=np.zeros((4,4))
    for (i,j),v in zip(IDX,c): t[i,j]=t[j,i]=v
    return t
def K_coord(p,**kw):
    """10x10 coordinate Hessian K_AB = w_A * contraction, built column by column."""
    K=np.zeros((10,10))
    for B in range(10):
        e=np.zeros(10); e[B]=1; E=fp(p,tensor(e),**kw)
        K[:,B]=W*coords(up(E))*0+W*coords(E)   # covariant components times multiplicity
    return K
def ward_violation(trials=200,seed=1,**kw):
    rng=np.random.default_rng(seed); worst=0.0
    for _ in range(trials):
        p=rng.normal(size=4); xi=rng.normal(size=4)
        g=np.outer(p,xi)+np.outer(xi,p)          # gauge mode (covariant)
        E=fp(p,g,**kw); worst=max(worst,np.abs(E).max()/max(1,np.abs(g).max()*np.abs(p).max()**2))
    return worst
def symmetric_check(trials=50,seed=2,**kw):
    rng=np.random.default_rng(seed); worst=0.0
    for _ in range(trials):
        p=rng.normal(size=4); a=tensor(rng.normal(size=10)); b=tensor(rng.normal(size=10))
        x=np.sum(up(b)*fp(p,a,**kw)); y=np.sum(up(a)*fp(p,b,**kw)); worst=max(worst,abs(x-y))
    return worst
def null_rank(p,**kw):
    K=K_coord(p,**kw); return 10-np.linalg.matrix_rank(K,tol=1e-9)
if __name__=="__main__":
    # Gate A: gauge null (Ward). Gate B: exactly 4 nulls (the 4 gauge modes) at generic p, i.e. no extra
    # missing directions. Ward PASS is necessary, not sufficient (P-32 V003 spatial-embedding control).
    cases=[("Fierz-Pauli (linearized Einstein)",{},(True,True)),("FP + mass m2=0.7",{"m2":0.7},(False,False)),
           ("spatial-only symmetric embedding",{"spatial_only":True},(True,False)),("temporal defect 0.3",{"temporal_defect":0.3},(False,False))]
    p=np.array([0.3,1.1,-0.4,0.8])
    for name,kw,(eA,eB) in cases:
        v=ward_violation(**kw); A=v<1e-10; nn=null_rank(p,**kw); B=(nn==4)
        ok=(A==eA and B==eB)
        print(f"{name:34s} ward={'PASS' if A else 'FAIL'}({v:.1e})  nulls={nn}  4-null={'PASS' if B else 'FAIL'}  expected=({'PASS' if eA else 'FAIL'},{'PASS' if eB else 'FAIL'})  {'OK' if ok else 'MISMATCH'}")
    print("FP bilinear symmetry violation:",f"{symmetric_check():.2e}")
