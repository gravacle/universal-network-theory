"""Exact source-free FLRW polar slice versus the old R^2 preparation.

No evolution, new physical coefficient, or change to frozen source scripts.
Old no-radiation calibration only. RK4 max steps extent/1024,extent/2048;
state convergence1e-11, analytic identities1e-10, inverse2e-12.
Discrete residuals are measurements, not a newly invented acceptance gate.
The characteristic reach is a frozen-background estimate, NOT a nonlinear
domain-of-dependence proof for the supported galaxy calculation.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_polar_source_v006 as buffered

mixed=buffered.mixed
BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_FLRW_POLAR_AUDIT_V001_RESULT.json'


def radial(model,r,subdivisions):
    def rhs(rr,y):
        H,hx=model.bg(float(y[0]))[5:7]
        B=1-H*H*rr*rr
        return np.array([-H*H*rr/B,-H*H*hx*rr*(1+H*H*rr*rr)/B**2])
    y=np.zeros(2);last=0.;rows=[]
    for end in r:
        count=max(1,math.ceil((end-last)/(model.extent/subdivisions)))
        h=(end-last)/count
        for j in range(count):
            rr=last+j*h
            a=rhs(rr,y);b=rhs(rr+h/2,y+h*a/2)
            c=rhs(rr+h/2,y+h*b/2);d=rhs(rr+h,y+h*c)
            y+=h*(a+2*b+2*c+d)/6
        rows.append(y.copy());last=end
    return np.array(rows).T


def exact(model,x,lnJ):
    r=model.r
    bg=np.array([model.bg(float(xx)) for xx in x]).T
    a,s,Q,m,K,H,hx,qr=bg
    dd=model.constitutive(s)[2]
    Hd=H*H*hx;B=1-H*H*r*r;A=1/np.sqrt(B);J=np.exp(lnJ);N=J/A
    sig=H*r*A;c=A;u=H*r/B;phir=-Q*u
    rb=3*model.OB/a**3
    z=np.array([u,np.zeros(len(r)),np.zeros(len(r)),m/B,
                np.zeros(len(r)),np.zeros(len(r)),np.zeros(len(r)),rb/B,u])
    tr=-H*r/B;Hr=Hd*tr;Br=-2*H*H*r-2*H*Hr*r*r
    ar=-Br/(2*B);g=-H*H*r/B-Hd*r/B**2
    sr=(H+Hr*r)*A-H*r*Br*A/(2*B)
    q=Q*A;Qt=-3*H*m/dd;Qr=Qt*tr
    qR=Qr*A-Q*Br*A/(2*B)
    cur=m*sig;mr=-3*H*m*tr
    curR=mr*sig+m*sr
    rho=3*H*H-2*Hd*H*H*r*r/B
    Pr=-2*Hd/B-3*H*H
    mass=H*H*r**3/2
    # Time derivatives at fixed areal radius; cosmic dt/dT=J.
    ut=r*Hd*J*(1+H*H*r*r)/B**2
    phirt=-r*J*((Qt*H+Q*Hd)/B+2*Q*H*H*Hd*r*r/B**2)
    cpt=-3*H*m*J/B+2*m*H*Hd*J*r*r/B**2
    nbt=-3*H*rb*J/B+2*rb*H*Hd*J*r*r/B**2
    zt=np.array([ut,np.zeros(len(r)),np.zeros(len(r)),cpt,
                 np.zeros(len(r)),np.zeros(len(r)),np.zeros(len(r)),nbt,ut])
    return locals()


def maximum(v,mask=None):
    return float(np.max(np.abs(v if mask is None else v[mask])))


def main():
    if OUT.exists():raise FileExistsError(OUT)
    started=time.monotonic();saved=json.loads(mixed.prev.inherited.SOURCE.read_text())
    checks=[];rows=[]
    def check(name,error,tol):
        checks.append(dict(name=name,error=float(error),tolerance=tol,passed=bool(error<=tol)))
    for kind,n,buffer in [('original',320,None),('original',640,None),
                          ('buffer',960,600.),('buffer',960,800.)]:
        model=(mixed.Polar(saved,n,.012) if kind=='original'
               else buffered.Polar(saved,n,.012,.125,buffer))
        label=f'{kind}_{n}_{buffer}';r=model.r
        lo=radial(model,r,1024);hi=radial(model,r,2048)
        check(label+'_radial_x',maximum(lo[0]-hi[0])/maximum(hi[0]),1e-11)
        check(label+'_radial_lnJ',maximum(lo[1]-hi[1])/maximum(hi[1]),1e-11)
        g=exact(model,*hi);A,N,B=g['A'],g['N'],g['B']
        # Analytic Einstein constraints, canonical scalar/vector evolution,
        # and ordinary geodesic time update, independent of mesh derivatives.
        normalrho=g['Q']*g['m']/B-g['K']+g['rb']/B
        normalP=g['K']+(g['Q']*g['m']+g['rb'])*g['H']**2*r*r/B
        check(label+'_normal_density',maximum(normalrho-g['rho'])/maximum(g['rho']),1e-10)
        check(label+'_normal_pressure',maximum(normalP-g['Pr'])/maximum(g['Pr']),1e-10)
        check(label+'_mass_constraint',maximum(g['ar']-A*A*(r*g['rho']/2-g['mass']/r**2))/maximum(g['ar']),1e-10)
        check(label+'_lapse_constraint',maximum(g['g']-A*A*(g['mass']/r**2+r*g['Pr']/2))/maximum(g['g']),1e-10)
        urhs=-N*(g['g']*g['c']+g['sig']*g['sr']/g['c'])
        phrhs=N*(g['qR']+g['g']*g['q'])
        cprhs=-N*(g['curR']+2*g['cur']/r+g['g']*g['cur'])
        check(label+'_vector_time',maximum(urhs-g['ut'])/maximum(g['ut']),1e-10)
        check(label+'_scalar_time',maximum(phrhs-g['phirt'])/maximum(g['phirt']),1e-10)
        check(label+'_charge_time',maximum(cprhs-g['cpt'])/maximum(g['cpt']),1e-10)
        model.Aguess=A.copy()
        dz,geometry=model.rhs(0.,g['z'],True)
        check(label+'_inverse',model.max_inverse,2e-12)
        # Old code normalizes time at the outer radius with R^2 FLRW lapse.
        H0,hx0=model.bg0[5:7]
        norm=math.exp(-.5*H0*H0*(1+hx0)*r[-1]**2)/N[-1]
        old_kappa=model.kappa;model.kappa=0.
        old=model.initial();model.kappa=old_kappa
        old_rhs,oldgeom=model.rhs(0.,old,True)
        m0=model.bg0[3];Q0=model.bg0[2];d0=float(model.constitutive(model.bg0[1])[2])
        speed=math.sqrt((2*model.C/model.KB+m0/Q0)/d0)
        time_span=.25*model.tdyn
        reach=10*model.L+speed*time_span
        regions={'core':r<=10*model.L,'frozen_fast_reach':r<=reach,'whole':np.ones(len(r),dtype=bool)}
        metrics={}
        for name,mask in regions.items():
            metrics[name]=dict(
                max_radius_over_L=float(np.max(r[mask])/model.L),
                initial_charge_relative=maximum(old[3]-g['z'][3],mask)/m0,
                initial_vector_relative=maximum(old[0]-g['z'][0],mask)/maximum(g['z'][0],mask),
                old_x_approx_error=maximum(-.5*r*r-hi[0],mask),
                exact_metric_relative=maximum(geometry['A']/A-1,mask),
                exact_lapse_relative_after_normalization=maximum(geometry['N']/(norm*N)-1,mask),
                exact_charge_rhs_relative=maximum(dz[3]-norm*g['zt'][3],mask)/(3*H0*m0),
                old_charge_rhs_relative=maximum(old_rhs[3]-norm*g['zt'][3],mask)/(3*H0*m0),
                exact_spurious_p_rhs=maximum(dz[1],mask),
                old_spurious_p_rhs=maximum(old_rhs[1],mask),
                charge_state_error_over_old_floor=maximum(old[3]-g['z'][3],mask)/(m0*1e-8),
                ordinary_rhs_relative=maximum(dz[7]-norm*g['zt'][7],mask)/(9*H0*model.OB))
        rows.append(dict(mesh=label,actual_nodes=model.n,radial_last=float(r[-1]),
                         lapse_normalization_relative=norm-1,
                         frozen_fast_speed=speed,quarter_orbit_time=time_span,
                         frozen_fast_reach_over_L=reach/model.L,metrics=metrics))
        print(json.dumps(rows[-1]),flush=True)
    files=[Path(__file__),Path(buffered.__file__),Path(mixed.__file__),
           Path(mixed.src.__file__),Path(mixed.prev.__file__),
           Path(mixed.prev.inherited.__file__),mixed.prev.inherited.SOURCE]
    result=dict(protocol=__doc__,elapsed_seconds=time.monotonic()-started,rows=rows,checks=checks,
                all_controls_passed=all(c['passed'] for c in checks),
                identity={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                scope='source-free initial consistency only; not a galaxy trajectory or cure',
                technical_attempts=['First invocation stopped before work: local time variable shadowed time module; renamed to time_span. No scientific criteria or result changed.'])
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','protocol')}),flush=True)


if __name__=='__main__':main()
