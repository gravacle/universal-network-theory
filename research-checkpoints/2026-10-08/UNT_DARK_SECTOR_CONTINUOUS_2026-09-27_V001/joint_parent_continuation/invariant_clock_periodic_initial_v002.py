"""Numerical constraint stopping repair, V001 failure retained.

Explicit nonlinear completion of a qualified FIRST-ORDER assembly seed.

No integration, automatic execution, fit, adopted native state or galaxy.
The source is fixed assemblyV004 epoch54, equal-contrast column times1e-12.
Use initial Newtonian-to-synchronous spatial shift L=0. Normalize proper
spatial volume and integrated ordinary/scalar charges to background totals.
Choose zero proper-volume mean shear to close the exact metric constraints.
Mapped velocities are only a guess: NEVER reimpose them after constraint
solution. This source module prepares the free data; constraints are solved
separately. The auxiliary-s map preserves positive K(X) charge without
subtracting nearly equal numbers near X~100.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
import invariant_clock_compression_assembly_v001 as linear

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V004_RESULT.json'
EXPECTED='7ed429224a93aaef44c97dc2bdaedce5c2f3fc7b685ceb863ae99c91fc9f304b'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load():
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed qualified seed history')
    parent=json.loads(SOURCE.read_text())
    if not parent['all_controls_passed']:raise ValueError('unqualified assembly history')
    for path,digest in parent['dependencies'].items():
        if sha(path)!=digest:raise ValueError('changed assembly dependency '+path)
    saved=json.loads(linear.linear.old.base.SOURCE.read_text())
    saved['inherited']=parent['fixed']
    return linear.linear.old.base.Model(saved,1),parent

def mapped_seed(model,parent,n,epoch=54,amplitude=1e-12):
    if n<5 or n%2!=1:raise ValueError('odd periodic grid required')
    snap=parent['histories'][-1]['snapshots'][epoch]
    x=math.log(snap['a']);lin=linear.Assembly(model)
    abar,Qbar,mbar,dbar,H,Hdot,_,rb,kphys2=lin.bg(x)
    sb=model.bg(x)[1];Vbar=abar**3;cT=.01;F=1+1.5*cT
    phasegrid=2*np.pi*np.arange(n)/n;co=np.cos(phasegrid)
    modes=np.fft.fftfreq(n,1/n)
    def dx(f):return np.fft.ifft(1j*lin.k*modes*np.fft.fft(f-np.mean(f))).real
    dm,phi,alpha,Z,db,theta=np.array(snap['state'])[:,1]*amplitude
    Phi=snap['observables'][0][1]*amplitude
    Phidot=snap['Phi_dot'][1]*amplitude
    E=(Z-model.C*(phi+Qbar*alpha))/model.KB
    f=(-Phi-H*theta)*co
    # log1p/expm1 retains the O(f^2) mean correction at small amplitude.
    shift=-np.log1p(np.mean(np.expm1(3*f)))/3
    fa=f+shift;fb=f+shift;u=dx((alpha+theta)*co)
    phase=(phi-Qbar*theta)*co
    A=abar*np.exp(fa);B=abar*np.exp(fb);V=Vbar*np.exp(fa+2*fb)
    dV=Vbar*np.expm1(fa+2*fb)
    ax=dx(fa);bx=dx(fb);sigma=u/A;c=np.sqrt(1+sigma*sigma)
    sx=(dx(u)-u*ax)/A;cx=sigma*sx/c;w=dx(phase)/A
    dl=(-Phidot-Hdot*theta-H*Phi)*co
    dk=dl+kphys2*theta*co;udot=dx(E*co)
    target=mbar+(dm+3*H*mbar*theta)*co
    if np.any(target<=0):raise ValueError('mapped charge leaves positive sheet')
    s=target/(model.mpref*math.sqrt(1+model.eps))
    for _ in range(6):
        X,m,d,K,ms,qr=model.constitutive(s)
        step=(m-target)/ms;s-=step
        if np.max(abs(step)/s)<2e-15:break
    X,m,d,K,ms,qr=model.constitutive(s)
    q=np.sqrt(X*X+w*w);p=sigma*q+c*w;e=(udot+cx)/A
    j=model.lam*abs(p)/np.sqrt(p*p+model.bs**2)
    D=model.C*(e-(1+j)*p);ZZ=model.KB*e+model.C*p
    dc=sigma*sigma/(c+1)
    dTheta=dk/c+2*c*dl+H*dc*(2-1/c)+sigma*udot/(A*c)+(sx+2*sigma*bx)/A
    chibar=-3*cT*H;dchi=-cT*dTheta;chi=chibar+dchi
    dpa=-4*V*dl+2*V*dchi/c-2*V*chibar*dc/c+(-4*H+2*chibar)*dV
    dpb=-4*V*(dk+dl)+4*V*c*dchi+4*V*chibar*dc+(-8*H+4*chibar)*dV
    piu=2*B*B*(ZZ+sigma*chi/c)
    # Normalize canonical scalar charge, not an assumed gravitating mass.
    pcbar=2*Vbar*mbar
    qrbar=model.bg(x)[7]
    Xdiff=model.Q0*model.eps*(s-sb)/((1+s)*(1+sb)*(qr+qrbar))
    mdiff=model.mpref*(qr*(s-sb)+sb*Xdiff/model.Q0)
    dpc=2*(mbar*dV+V*(mdiff+m*w*w/(X*(q+X))+sigma*D))
    dpc-=np.mean(dpc)
    delta_b=(db+3*H*theta)*co
    dustweight=V*(1+delta_b);dustweight/=np.mean(dustweight)
    piT=2*Vbar*rb*dustweight
    z=np.array([fa,fb,u,phase,dpa,dpb,piu,dpc])
    return dict(x=x,z=z,piT=piT,k=lin.k,epoch=epoch,amplitude=amplitude,
        preparation='volume-normalized mapped free data; conserved total ordinary/scalar charge; metric momenta not yet constrained',
        mapped_velocities=np.array([H+dk,H+dl,udot,q]),auxiliary_s=s,
        mapped_delta_b=delta_b,volume_shift=float(shift),background=dict(a=abar,Q=Qbar,m=mbar,H=H,Hdot=Hdot,rho_b=rb,
        pa=-4*Vbar*F*H,pb=-8*Vbar*F*H,pc=pcbar),spatial_grid=phasegrid)

def solve_constraints(run,prep):
    """Reduced cosine Newton solve with a counted zero-volume-mean-shear row.

    Changes only metric canonical momenta. No density, field charge, spatial
    metric or subsequent velocity projection. Fixed branch/iteration bounds;
    failure is returned to the producer as an exception, never a new profile.
    """
    x=prep['x'];z=prep['z'].copy();piT=prep['piT'];N=z.shape[1]
    phase=2*np.pi*np.arange(N)/N;nm=np.arange(N//2+1)
    cosine=np.cos(nm[:,None]*phase);sine=np.sin(nm[1:,None]*phase)
    dxcos=-run.k*nm[:,None]*np.sin(nm[:,None]*phase)
    bg=run.background(x);scale=abs(bg['pi_a_bar'])
    history=[]
    def local_h(state):
        state=state.copy()
        for iteration in range(16):
            g=run.fields(x,state);cc=run.constraints(x,state,piT,fields=g)
            error=np.max(abs(cc['Hamiltonian']))/(6*bg['Vbar']*bg['H']**2)
            if error<=5e-14:return state,g,cc,iteration,error
            if np.any(g['bdot']<=0):raise ValueError('initial expanding transverse branch lost')
            step=cc['Hamiltonian']/g['bdot'];accepted=False
            for halv in range(16):
                trial=state.copy();trial[5]-=step*.5**halv
                gt=run.fields(x,trial);ct=run.constraints(x,trial,piT,fields=gt)
                if np.max(abs(ct['Hamiltonian']))<np.max(abs(cc['Hamiltonian'])):
                    state=trial;accepted=True;break
            if not accepted:raise ValueError('initial local Hamiltonian line search failed')
        raise ValueError('initial Hamiltonian iteration cap')
    def residual(g,cc):
        shear=np.mean((2*g['state'][4]-g['state'][5])/4+g['V']*g['sigma']**2*g['chi']/g['c'])
        return np.r_[shear,2*np.mean(sine*cc['momentum'],axis=1)/run.k]
    for iteration in range(16):
        z,g,cc,li,he=local_h(z);r=residual(g,cc)
        momentum_scale=max(np.max(np.sum(abs(cc['momentum_terms']),axis=0))/run.k,1e-30)
        error=float(np.max(abs(r))/momentum_scale)
        history.append(dict(iteration=iteration,reduced_residual=error,Hamiltonian=he,local_iterations=li))
        if error<=1e-8:break
        ratio=g['adot']/g['bdot']
        momjac=(g['ax']-ratio*g['bx'])*cosine-dxcos
        sw=(2+ratio)/4+g['sigma']**2*g['qq_entry']*(1+2*g['sigma']**2-ratio)/(4*g['c']**2*g['determinant'])
        jac=np.vstack((np.mean(sw*cosine,axis=1),2*(sine@momjac.T)/N/run.k))
        change=np.linalg.solve(jac,-r)@cosine
        accepted=False
        for halv in range(16):
            trial=z.copy();trial[4]+=change*.5**halv
            trial,gt,ct,_,_=local_h(trial)
            if np.max(abs(residual(gt,ct)))<np.max(abs(r)):
                z=trial;accepted=True;break
        if not accepted:raise ValueError('initial momentum/shear line search failed')
    else:raise ValueError('initial reduced constraint iteration cap')
    return dict(z=z,piT=piT,x=x,history=history,fields=g,constraints=cc,
        momenta_correction=z[4:6]-prep['z'][4:6],mean_volume=float(np.mean(g['V'])),
        mean_shear=float(np.mean((2*z[4]-z[5])/4+g['V']*g['sigma']**2*g['chi']/g['c'])))
