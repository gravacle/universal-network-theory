"""Short inverse-boundary discrimination, unchanged positive-s branch.

Restart the saved fine homogeneous checkpoint a=.15399265, not the whole
trajectory. Continue only to a=.157 at256/512/1024 RK4 steps, capture the
first failed inverse evaluation. Compute its exact F(s=0) and the analytic
global lower bound c²KQQ(0)−C sigma²(2/KB+2lambda_s) on the Schur term
for s>=0. If both positive, F(s) is increasing and no s>=0 root exists:
this identifies a declared branch exit rather than Newton overshoot.
No root is clipped/continued onto negative s. Report only event brackets
and captured states; no full-history or universal physical exclusion.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import homogeneous_tilt_saturation_v001 as prior

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'HOMOGENEOUS_TILT_SATURATION_V001_S16384_CHECKPOINT.json'
OUT=BASE/'HOMOGENEOUS_TILT_BOUNDARY_V001_RESULT.json'


class Model(prior.Model):
    def unpack(self,x,z):
        try:return super().unpack(x,z)
        except ValueError as err:
            a=math.exp(x);v=z[0]+2*z[1];V=a**3*np.exp(v)
            sig=z[2]*np.exp(-z[0]);c=np.sqrt(1+sig*sig);Z=z[6]*np.exp(-2*z[1])
            M=self.pcbar*(1+z[7])/(2*V);p=sig*self.Q0/c
            j=self.lam*abs(p)/np.sqrt(p*p+self.bs*self.bs)
            F0=sig*self.C*((Z-self.C*p)/self.KB-(1+j)*p)-M
            d0=float(self.constitutive(np.array([0.]))[2][0])
            bound=c*c*d0-self.C*sig*sig*(2/self.KB+2*self.lam)
            self.failed=dict(a=a,error=str(err),state_reduced=z.tolist(),physical_tilt=float(sig[0]),
                F_at_s_zero=float(F0[0]),target_charge_density=float(M[0]),
                Schur_lower_bound_for_nonnegative_s=float(bound[0]),
                no_nonnegative_s_root=bool(F0[0]>0 and bound[0]>0))
            raise


def main():
    saved=json.loads(prior.base.SOURCE.read_text());start=json.loads(SOURCE.read_text())
    x0=math.log(start['diagnostics']['a']);xf=math.log(.157);rows=[];beg=time.monotonic()
    for steps in (256,512,1024):
        m=Model(saved);z=np.array(start['state_reduced']);dx=(xf-x0)/steps
        xgood=x0;failure=None
        try:
            for i in range(steps):
                x=x0+i*dx
                a=m.rhs(x,z);b=m.rhs(x+dx/2,z+dx*a/2)
                c=m.rhs(x+dx/2,z+dx*b/2);d=m.rhs(x+dx,z+dx*c)
                z+=dx*(a+2*b+2*c+d)/6;xgood=x+dx
        except ValueError:failure=m.failed
        rows.append(dict(steps=steps,last_completed_a=math.exp(xgood),failure=failure))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in
          ('homogeneous_tilt_saturation_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py')},
        rows=rows,elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
