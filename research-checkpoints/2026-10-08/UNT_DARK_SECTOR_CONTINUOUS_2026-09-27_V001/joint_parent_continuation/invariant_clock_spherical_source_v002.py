"""Same physical source/duration and numerical gates as failed V001.

Replace unconstrained radial ADM with exact momentum-reduced variables:
R,l=Rdot/R,F=Rr/A and four canonical matter fields. The radial momentum
constraint gives T=(u piur-piph phir)/(4 A R Rr), Fdot/F=T and
k=l+R l_r/Rr-T. Reconstruct A=Rr/F and both metric momenta. This is an
analytic constraint reduction, not a post-step constraint projection.
The remaining Hamiltonian and eliminated pi_b evolution are independent
checks. logF=(r/L)^2 chi enforces central elementary flatness. In vacuum
Fdot=0 exactly, avoiding the ill-resolved ADM Jordan cancellation of V001.

Use identical ordinary Plummer mass/size, clocks, branch, boundary tail,
two spatial/time/domain sequences and tolerances; no repaired physical
parameter or selected initial mode. Add eliminated-pi_b tangent gate1e-3
at two finite-difference increments (1e-11,5e-12) in x, using a denominator
max absolute canonical RHS or1e-4. Preserve V001 as numerical failure.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_spherical_source_v001 as old

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_SPHERICAL_SOURCE_V002_RESULT.json'


class Model(old.Model):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        y=self.rghost/self.L
        ug=-2*self.tlam*y*y/(1+y*y)**1.5/np.exp(self.lpg)
        self.chig=np.log1p(ug)/(y*y)

    def initial(self,homogeneous=False):
        z=np.zeros((7,self.N));z[0]=2*self.lp
        y=self.r/self.L;u=-2*self.tlam*y*y/(1+y*y)**1.5/np.exp(self.lp)
        z[1]=np.log1p(u)/(y*y);z[6]=np.expm1(6*self.lp)
        return z

    def unpack(self,x,z):
        b,chi,ell,un,phase,pu,pc=z;r=self.r;y=r/self.L
        br=self.deriv(b,outer=self.tail[1]);brr=self.deriv(b,outer=self.tail[1],order=2)
        ch_r=self.deriv(chi,outer=self.chig)
        logF=y*y*chi;logFr=2*r*chi/self.L**2+y*y*ch_r
        fa=b+np.log1p(r*br)-logF
        ev=np.exp(fa+2*b);pa=ev*(1+ell)-1
        # Constitutive inverse is independent of the yet-reconstructed pi_b.
        full=np.array([fa,b,un,phase,pa,pa,pu,pc])
        g=super().unpack(x,full)
        g['full']=full;g['F']=np.exp(logF);g['omF2']=-np.expm1(2*logF)
        g['Fr']=g['F']*logFr
        g['ax']=br+(br+r*brr)/(1+r*br)-logFr
        g['R3']=2*g['omF2']/g['R']**2-4*g['Fr']/(g['A']*g['R'])
        g['curvA']=2*g['A']*g['omF2'];g['curvB']=-4*g['R']*g['Fr']
        ell_r=self.deriv(ell,outer=np.zeros(2))
        T=(g['abar']*un*g['piur']-g['piph']*g['phir'])/(4*g['A']**2*g['R']*g['F'])
        k=g['h']*(1+ell+r*ell_r/(1+r*br))-T
        l=g['h']*(1+ell)
        g['pib']=-4*g['V']*(k+l);full[5]=g['ev']*(k+l)/(2*g['h'])-1
        g['kin']=g['pia']*(g['pia']-2*g['pib'])/(8*g['V'])
        g.update(T=T,k=k,l=l,logF=logF)
        return g

    def rhs(self,x,z,return_g=False):
        g=self.unpack(x,z);a=g['abar'];h=g['h'];r=self.r;V=g['V'];A=g['A']
        b,chi,ell,un,phase,pu,pc=z;sig=g['sig'];c=g['c'];S=g['S'];cur=g['cur']
        sd=g['s']-g['sbar'];dK=3*self.OA/self.D*(np.log1p(sd/(1+g['sbar']))-sd/((1+g['s'])*(1+g['sbar'])))
        vec=-g['Lvec']/4+g['Z']*g['e']/2+(sig*S/c+g['w']*cur)/2-sig*sig*g['piur']/(4*c*V)
        out=np.empty_like(z)
        out[0]=ell
        out[1]=g['T']/(h*(r/self.L)**2)
        out[2]=-(3+g['hx'])*ell-1.5*ell*ell-g['omF2']/(2*g['R']**2*h*h)-dK/(2*h*h)+vec/(h*h)
        sr=np.exp(-g['full'][0])*(self.deriv(un,parity=-1,outer=np.zeros(2))-un*g['ax'])
        out[3]=(A*g['e']-sig*sr/c)/(a*h)-un
        out[4]=g['qdiff']/h
        out[5]=np.exp(2*b)*S/(c*h)-sig*(g['pur']+2*pu/r)/(A*c*h)-2*pu
        out[6]=-2*a*a*np.exp(2*b)/(self.pcbar*h)*(self.deriv(cur,parity=-1)+(2*g['bx']+2/r)*cur)
        return (out,g) if return_g else out

    def diagnose(self,x,z):
        dz,g=self.rhs(x,z,True);h=g['h'];a=g['abar'];r=self.r;V=g['V'];mask=self.mask
        HH=g['kin']/V-g['R3']+self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J']-2*g['Kfun']+g['piph']*g['q']/V+g['c']*g['piur']/V+self.piT/V
        full=g['full'];pa=full[4];pb=full[5]
        terms=np.array([self.deriv(pa,outer=self.tail[4]),-(1+pa)*g['ax'],-2*(1+pb)*g['bx'],
            2*(pa-pb)/r,-z[3]*(g['pur']+2*z[5]/r)/(2*h),self.pcbar*(1+z[6])*g['phir']/(4*a**3*h)])
        DD=terms.sum(axis=0);dscale=max(float(np.max(abs(terms[:,mask]))),max(self.kappa,1e-30)/self.L)
        acc=h*h*(dz[2]+g['hx']*(1+z[2])+(1+z[2])**2)*g['R']
        bgacc=h*h*(1+g['hx'])*g['R'];inward=bgacc-acc
        y=r/self.L;uu=-2*self.tlam*y*y/(1+y*y)**1.5/np.exp(self.lp)
        initialg=-np.expm1(2*np.log1p(uu))/(2*np.exp(2*self.lp)*r)
        sample=[]
        for rr in (.5,1.,2.,5.,10.):
            at=lambda f:float(np.interp(rr*self.L,r,f))
            sample.append(dict(r_over_L=rr,R=at(g['R']),inward=at(inward),initial_inward=at(initialg),
                acceleration_ratio_to_initial=at(inward)/at(initialg),tilt=at(g['sig']),JY=at(g['j']),
                clock_s=at(g['s']),dust_density=at(self.piT/(2*V)),clock_current=at(g['cur'])))
        tangent=[]
        rpb=2*g['kin']+g['curvB']+2*V*(g['Lvec']+2*g['Kfun'])
        for dd in (1e-11,5e-12):
            plus=self.unpack(x+dd,z+dd*dz)['pib'];minus=self.unpack(x-dd,z-dd*dz)['pib']
            fd=(plus-minus)/(2*dd)*h
            den=max(float(np.max(abs(rpb[mask]))),1e-4*self.L**2)
            tangent.append(float(np.max(abs(fd[mask]-rpb[mask])))/den)
        return dict(x=x,a=a,Hamiltonian_source_normalized=float(np.max(abs(HH[mask]))/max(2*np.max(self.excess),6*h*h)),
            momentum_normalized=float(np.max(abs(DD[mask]))/dscale),eliminated_pib_tangent=tangent,
            initial_acceleration_error=float(np.max(abs(inward[mask]-initialg[mask]))/max(np.max(abs(initialg)),1e-30)),
            minimum_inverse_fraction=float(np.min(g['schur']/g['d'])),min_s=float(np.min(g['s'])),
            max_tilt=float(np.max(abs(g['sig'][mask]))),max_JY=float(np.max(g['j'][mask])),
            min_Rr_over_A=float(np.min(g['F'])),samples=sample,
            material_max_speed=float(np.max(np.sqrt((2*self.C/self.KB+g['m']/g['X'])/g['d']))),
            charge_excess_integral=float(self.pcbar*np.sum(r*r*(z[6]-self.initial()[6]))*self.dr),
            outer_charge_flux=float(2*g['R'][-1]**2*g['cur'][-1]),state=z[:,mask].tolist(),radial_centers=r[mask].tolist())


def main():
    np.seterr(over='raise',invalid='raise',divide='raise');beg=time.monotonic()
    saved=json.loads(old.inherited.SOURCE.read_text());rows=[];old.Model=Model
    for N,extent,steps in ((512,50.,2048),(1024,50.,4096),(1024,50.,8192),(1638,80.,6552)):
        row=old.integrate(saved,N,extent,steps);rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='snapshots'},default=lambda x:x.item()),flush=True)
    rr=dict(space=old.compare(rows[0],rows[1]),time=old.compare(rows[1],rows[2]),domain=old.compare(rows[1],rows[3]))
    samples=[s for row in rows for s in row['snapshots']]
    checks=dict(completed=all(r['completed'] for r in rows),homogeneous=max(r['homogeneous_rhs'] for r in rows)<=1e-10,
        initial_acceleration=max(r['snapshots'][0]['initial_acceleration_error'] for r in rows)<=1e-3,
        Hamiltonian=max(s['Hamiltonian_source_normalized'] for s in samples)<=1e-3,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-3,
        eliminated_pib_tangent=max(max(s['eliminated_pib_tangent']) for s in samples)<=1e-3,
        inverse=max(r['max_inverse'] for r in rows)<=2e-12,positive_Rr=all(s['min_Rr_over_A']>0 for s in samples),
        refinement=all(v is not None and v['maximum']<=1e-3 for v in rr.values()))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in ('invariant_clock_spherical_source_v001.py','plane_canonical_evolution_v001.py')},
        input_sha256=hashlib.sha256(old.inherited.SOURCE.read_bytes()).hexdigest(),rows=rows,refinement=rr,
        controls={k:bool(v) for k,v in checks.items()},all_controls_passed=bool(all(checks.values())),elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False,default=lambda x:x.item());f.write('\n')
    print(json.dumps(dict(refinement=rr,controls=result['controls'],elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
