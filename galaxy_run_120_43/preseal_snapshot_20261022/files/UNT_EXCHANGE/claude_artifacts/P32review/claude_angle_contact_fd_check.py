import sys, importlib.util, itertools, numpy as np
from fractions import Fraction as F
sp=importlib.util.spec_from_file_location("ac",sys.argv[1]); ac=importlib.util.module_from_spec(sp); sp.loader.exec_module(ac)
S=np.array(ac.SIGNS,float)
def cos(g,a,b): return S[a]@g@S[b]/np.sqrt((S[a]@g@S[a])*(S[b]@g@S[b]))
rng=np.random.default_rng(3); worst1=worst2=0
for trial in range(40):
    X=rng.integers(-3,4,(3,3)); X=X+X.T; Y=rng.integers(-3,4,(3,3)); Y=Y+Y.T
    Xf=[[F(int(v)) for v in r] for r in X]; Yf=[[F(int(v)) for v in r] for r in Y]
    for a,b in itertools.combinations(range(4),2):
        h=1e-4; I=np.eye(3)
        d1=(cos(I+h*X,a,b)-cos(I-h*X,a,b))/(2*h)
        d2=(cos(I+h*X+h*Y,a,b)-cos(I+h*X-h*Y,a,b)-cos(I-h*X+h*Y,a,b)+cos(I-h*X-h*Y,a,b))/(4*h*h)
        worst1=max(worst1,abs(d1-float(ac.angle_first(a,b,Xf)))); worst2=max(worst2,abs(d2-float(ac.angle_second(a,b,Xf,Yf))))
print("max |D_exact - D_fd|  =",f"{worst1:.2e}"); print("max |E_exact - E_fd|  =",f"{worst2:.2e}  (mixed second derivative d2cos/dx dy)")
A=ac.analytic_inputs(); I3=A["I"]; E=A["E"]
print("controls: D01(E)=",ac.angle_first(0,1,E)," D02(E)=",ac.angle_first(0,2,E)," D(I)=",ac.angle_first(0,1,I3)," E(I,I)=",ac.angle_second(0,1,I3,I3)," E(I,E)=",ac.angle_second(0,1,I3,E)," E(E,E)=",ac.angle_second(0,1,E,E))
