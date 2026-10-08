"""Explicit analytic-branch extension, NOT acceptance of the frozen branch.

The completed boundary audit proves loss of the selected s>=0 root near
a=.15604. The action itself is smooth at s0. Test its larger real analytic
branch, permitting negative KQ ONLY as a field Noether charge, not a
future-causal particle-number/record-count current. Keep Q>0 and the full
positive Legendre Schur complement. No new action or fitted coefficient.
This new admissibility premise does NOT repair the old failed result.

Restart the SAME fine checkpoint a=.15399265; continue only to a=.157,
256/512/1024 steps. At each homogeneous inverse find the Schur-zero fold
between KQQ-zero s_crit and s0. Solve F(s)=0 on the upper regular sheet
by safeguarded bisection; stop if F at the fold is positive. Capture the
event, current norm, Q and all conserved state. Never step onto a negative
Schur sheet or reset charge. Positive-sheet equivalence preflight with
old solver<=1e-9 relative/floor1e-12; inverse residual<=2e-12. Report
time/event refinement and full-history failure, not a thermal/galaxy pass.
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
OUT=BASE/'HOMOGENEOUS_TILT_EXTENDED_BRANCH_V001_RESULT.json'


class Model(prior.Model):
    def unpack(self,x,z):
        if not np.all(np.isfinite(z)):raise ValueError('nonfinite state')
        abar,sbar,Qbar,mbar,Kbar,h,hx,qbar=self.bg(x)
        fa,fb,un,phase,pa,pb,pu,pc=z
        ev=np.exp(fa+2*fb);A=abar*np.exp(fa);B=abar*np.exp(fb);V=abar**3*ev
        pia=-4*abar**3*h*(1+pa);pib=-8*abar**3*h*(1+pb)
        piu=2*abar**2*pu;piph=self.pcbar*(1+pc)
        sig=un*np.exp(-fa);c=np.sqrt(1+sig*sig);w=np.zeros(1);Z=pu*np.exp(-2*fb)
        target=piph/(2*V);ss=float(sig[0]);cc=float(c[0]);zz=float(Z[0]);M=float(target[0])
        def local(s):
            Q,m,d,Kfun,dm,qroot=self.constitutive(s)
            pp=ss*Q/cc;ee=(zz-self.C*pp)/self.KB
            rt=math.sqrt(pp*pp+self.bs*self.bs)
            jj=self.lam*abs(pp)/rt
            jt=self.lam*abs(pp)*(pp*pp+2*self.bs*self.bs)/rt**3
            sch=cc*cc*d-self.C*ss*ss*(2/self.KB+jt)
            dp=self.C*(ee-(1+jj)*pp)
            return cc*m+ss*dp-M,sch
        scrit=(-(4+3*self.eps)+math.sqrt(self.eps*(8+9*self.eps)))/(4*(1+self.eps))
        low=scrit;high=0.
        if local(high)[1]<=0:raise ValueError('positive-s Schur domain unavailable')
        for _ in range(48):
            mid=(low+high)/2
            if local(mid)[1]>0:high=mid
            else:low=mid
        fold=high;ff=local(fold)[0]
        if ff>0:
            self.failure_capture=dict(a=abar,kind='upper_regular_sheet_root_absent',s_fold=fold,
                F_at_fold=float(ff),target_charge_density=M,physical_tilt=ss,
                state_reduced=z.tolist())
            raise ValueError('no root on positive-Schur analytic sheet')
        low=fold;high=max(1.,M/(cc*self.mpref))
        for _ in range(20):
            if local(high)[0]>0:break
            high=2*high+1
        else:raise ValueError('upper bracket unavailable')
        for _ in range(64):
            mid=(low+high)/2
            if local(mid)[0]>0:high=mid
            else:low=mid
        s=np.array([(low+high)/2])
        Q,m,d,Kfun,dm,qroot=self.constitutive(s);p=sig*Q/c;e=(Z-self.C*p)/self.KB
        root=np.sqrt(p*p+self.bs*self.bs);j=self.lam*abs(p)/root
        jt=self.lam*abs(p)*(p*p+2*self.bs*self.bs)/root**3
        Dp=self.C*(e-(1+j)*p);schur=c*c*d-self.C*sig*sig*(2/self.KB+jt)
        resid=c*m+sig*Dp-target;err=float(np.max(abs(resid)/target))
        self.max_inverse=max(self.max_inverse,err)
        self.min_schur_fraction=min(self.min_schur_fraction,float(np.min(schur/(c*c*d))))
        if err>2e-12 or np.any(schur<=0):raise ValueError('extended inverse regularity/residual failed')
        zz=abs(p)/self.bs
        J=self.lam*self.bs**2*(zz*np.sqrt(1+zz*zz)-np.arcsinh(zz))
        small=zz<.01
        J[small]=self.lam*self.bs**2*(2*zz[small]**3/3-zz[small]**5/5+3*zz[small]**7/28-5*zz[small]**9/72)
        q=Q/c
        qdiff=(self.Q0*self.eps*(s-sbar)/((1+s)*(1+sbar)*(qroot+qbar))-Qbar*sig*sig/(c+1))/c
        ax=bx=piux=np.zeros(1);Lx=self.KB*e*e+2*self.C*e*p-self.C*p*p-self.C*J+2*Kfun
        S=Dp*Q+m*p;cur=sig*m+c*Dp;kin=pia*(pia-2*pib)/(8*V)
        return locals()

    def diagnostics(self,x,z):
        out=super().diagnostics(x,z);g=self.unpack(x,self.reconstruct(x,z))
        out['orthonormal_current_norm_squared']=float((g['Dp']**2-g['m']**2)[0])
        out['current_time_component']=float((g['c']*g['m']+g['sig']*g['Dp'])[0])
        out['KQ']=float(g['m'][0]);out['schur_fraction']=float((g['schur']/(g['c']**2*g['d']))[0])
        return out


def main():
    saved=json.loads(prior.base.SOURCE.read_text());start=json.loads(SOURCE.read_text())
    x0=math.log(start['diagnostics']['a']);xf=math.log(.157);z0=np.array(start['state_reduced'])
    a=Model(saved).rhs(x0,z0);b=prior.Model(saved).rhs(x0,z0)
    pre=float(np.max(abs(a-b)/np.maximum(abs(b),1e-12)))
    if pre>1e-9:raise ValueError(f'positive sheet equivalence failed {pre}')
    rows=[];beg=time.monotonic()
    for steps in (256,512,1024):
        m=Model(saved);z=z0.copy();dx=(xf-x0)/steps;xgood=x0;failure=None;snap=[]
        try:
            for i in range(steps+1):
                x=x0+i*dx
                if i%(steps//32)==0:snap.append(m.diagnostics(x,z))
                if i==steps:break
                a=m.rhs(x,z);b=m.rhs(x+dx/2,z+dx*a/2)
                c=m.rhs(x+dx/2,z+dx*b/2);d=m.rhs(x+dx,z+dx*c)
                z+=dx*(a+2*b+2*c+d)/6;xgood=x+dx
        except ValueError as e:
            failure=dict(error=str(e),capture=getattr(m,'failure_capture',None))
        rows.append(dict(steps=steps,last_completed_a=math.exp(xgood),completed=failure is None,
            failure=failure,snapshots=snap,maximum_inverse_error=m.max_inverse,
            minimum_schur_fraction=m.min_schur_fraction))
    deps=['homogeneous_tilt_saturation_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in deps},
        positive_sheet_equivalence_error=pre,rows=rows,elapsed_seconds=time.monotonic()-beg,
        scope='Broadened field-current admissibility diagnostic; not the original positive-charge model.')
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({**{k:v for k,v in result.items() if k not in ('protocol','rows')},
        'row_summaries':[{k:v for k,v in row.items() if k!='snapshots'} for row in rows]},indent=2))


if __name__=='__main__':main()
