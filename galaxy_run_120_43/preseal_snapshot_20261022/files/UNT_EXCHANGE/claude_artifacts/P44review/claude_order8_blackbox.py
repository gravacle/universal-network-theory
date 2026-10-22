"""Claude black-box check of P44 complex_riccati_order8_v002.series (author code run only on Claude's random test inputs,
in a scratch copy; oracle = exact eigvalsh of the full Hermitian H(h)=[[A,hB],[hB^+,D+hC]]).
Expect max eigenvalue error ~ h^9 for the P-block-connected eigenvalues (ordered and interleaved cases)."""
import sys, importlib.util, numpy as np
sp=importlib.util.spec_from_file_location("a",sys.argv[1]); a=importlib.util.module_from_spec(sp); sp.loader.exec_module(a)
rng=np.random.default_rng(11)
def herm(k,s): M=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k)); return s*(M+M.conj().T)/2
def run(label,A,D,B,C):
    out=a.series(A,D,B,C,order=8); K=out["K"]; n=A.shape[0]
    print(label,"target:",out["target_kind"],"| max Hermiticity resid:",max(out["Hermiticity_residuals"]))
    evA=np.linalg.eigvalsh(A); prev=None
    for h in (0.08,0.04,0.02,0.01):
        H=np.block([[A,h*B],[h*B.conj().T,D+h*C]]); ex=np.linalg.eigvalsh(H)
        # P-connected eigenvalues: nearest exact eigenvalue to each continued P level (follow from unperturbed A spectrum)
        ap=np.sort(np.linalg.eigvalsh(sum(h**k*K[k] for k in range(9))))
        sel=np.sort([ex[np.argmin(np.abs(ex-v))] for v in ap])
        err=np.abs(sel-ap).max()
        print(f"  h={h}: max err {err:.3e}" + (f"  ratio {prev/err:.1f} (h^9 -> 512)" if prev else "")); prev=err
n,q=3,5
A=herm(n,0.5); D=herm(q,0.5)+6*np.eye(q); B=rng.normal(size=(n,q))+1j*rng.normal(size=(n,q)); C=herm(q,1.0)
run("ordered",A,D,B,C)
D2=np.diag([-6.0,-5.5,6.0,6.5,7.0]).astype(complex)+0.1*herm(q,1.0); A2=herm(n,0.3)
run("interleaved",A2,D2,B,C)
