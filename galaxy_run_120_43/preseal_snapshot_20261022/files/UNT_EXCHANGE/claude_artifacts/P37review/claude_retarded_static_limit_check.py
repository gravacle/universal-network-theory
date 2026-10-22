import sys, importlib.util, numpy as np
sp=importlib.util.spec_from_file_location("rr",sys.argv[1]); rr=importlib.util.module_from_spec(sp); sp.loader.exec_module(rr)
rng=np.random.default_rng(11); d=6
def herm(): M=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); return (M+M.conj().T)/2
H0=herm(); V=[herm(),herm()]; C=[[herm(),None],[None,herm()]]; C[0][1]=C[1][0]=herm()
e,U=np.linalg.eigh(H0); tr=lambda M: U.conj().T@M@U
Vb=[tr(v).tolist() for v in V]; Cb=[[tr(C[i][j]).tolist() for j in range(2)] for i in range(2)]
p=[1.0]+[0.0]*(d-1)
out=rr.assemble(e.tolist(),p,Vb,Cb,z_energy=1e-9j,coordinates=("a","b"),domain_scope="COMPLETE_FINITE_DOMAIN",matrix_element_cap=10**6,contraction_cap=10**6)
def E0(ja,jb): H=H0+ja*V[0]+jb*V[1]+0.5*(ja*ja*C[0][0]+2*ja*jb*C[0][1]+jb*jb*C[1][1]); return np.linalg.eigvalsh(H)[0]
h=1e-4; fd=np.zeros((2,2))
for i in range(2):
  for j in range(2):
    s=lambda a,b: E0(*( [a,b] ))
    ei=np.eye(2)[i]*h; ej=np.eye(2)[j]*h
    fd[i,j]=(E0(*(ei+ej))-E0(*(ei-ej))-E0(*(-ei+ej))+E0(*(-ei-ej)))/(4*h*h)
resp=np.array([[out["response"][i][j].real for j in range(2)] for i in range(2)])
print("T=0 static Hessian: max|response - FD d2E/dj2| =",f"{np.abs(resp-fd).max():.2e}"); print(resp); print(fd)
