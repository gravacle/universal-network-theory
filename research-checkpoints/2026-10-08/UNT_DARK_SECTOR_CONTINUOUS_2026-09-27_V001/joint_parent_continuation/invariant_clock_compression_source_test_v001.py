"""Bounded ordinary-source test of the proposed compression completion.

Same5kpc finite Plummer rest-density preparation, Gbare*M/L=1e-7 and300L
ordinary compensation as the earlier source test. No halo, incoming phase
fit, held density or replacement linearized J. Positive ordinary particles
are initially circular in the solved lapse, then their restweight, radial
and angular momentum evolve. This is specified Cauchy preparation, NOT a
native galaxy assembly law. Equal coordinate compensation is not assumed
to cancel actual canonical rest/kinetic/gravitating energy; all are reported.

Current two-coordinate calibration supplies original K(X), J and budgets;
the additional cTheta=.01 changes H by1/sqrt(1.015). Former BBN/CMB/BAO
fits are NOT inherited. Exact no-radiation compressed FLRW polar data set
initial cosmic scalar/ordinary fields and the external chi/lapse history.
No independent chi_t boundary is clamped. Matching defects are measured.

Numerical acceptance remains1e-3 for independent Hamiltonian, full-flow
mass/chi tangency and tangent-step controls; inverse2e-12; positivity and
positive Schur/multiplier branch. Boundary RK64/128 error1e-10. Initial
circular-preparation iteration relative1e-9, up to30. Refine space/time and
domain BEFORE calling any trajectory qualified. No physical success gate.
One bounded worker, exclusive result/checkpoint; no auto-relaunch.
"""
from pathlib import Path
from functools import lru_cache
import argparse
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_compression_source_v001 as source
import invariant_clock_compression_components_v001 as oracle

ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
maximum=lambda v:float(np.max(np.abs(v)))

class Boundary:
    def __init__(self,model):self.model=model;self.radius=None
    def at(self,t,n=64):
        # Central proper time defines the polar coordinate normalization.
        x=0.;dt=t/8
        for _ in range(8):
            a=oracle.background(self.model,x)[5]
            b=oracle.background(self.model,x+dt*a/2)[5]
            c=oracle.background(self.model,x+dt*b/2)[5]
            d=oracle.background(self.model,x+dt*c)[5]
            x+=dt*(a+2*b+2*c+d)/6
        y=np.array([x,0.]);step=self.radius/n
        def rhs(r,v):
            H,hx=oracle.background(self.model,v[0])[5:7];B=1-H*H*r*r
            return np.array([-H*H*r/B,-H*H*hx*r*(1+H*H*r*r)/B**2])
        for i in range(n):
            r=i*step;a=rhs(r,y);b=rhs(r+step/2,y+step*a/2)
            c=rhs(r+step/2,y+step*b/2);d=rhs(r+step,y+step*c)
            y+=step*(a+2*b+2*c+d)/6
        H=oracle.background(self.model,y[0])[5]
        return -3*oracle.CT*H,math.exp(y[1])*math.sqrt(1-H*H*self.radius**2)
    @lru_cache(maxsize=128)
    def __call__(self,t):return self.at(t)

def initial(model,reference):
    r=model.r;bg=oracle.oracle(reference,r,oracle.polar_slice(reference,r,2048))
    yy=r/model.L;shape=(1+yy*yy)**-2.5*np.maximum(1-(yy/20)**2,0)**4
    physical_source=shape*2*model.kappa*model.L/(model.massint@shape)[-1]
    comp=np.exp(-(r/(300*model.L))**2)
    comp*=(model.massint@physical_source)[-1]/(model.massint@comp)[-1]
    if np.any(bg['rb']-comp<=0):raise ValueError('nonpositive compensated cosmic ordinary density')
    A=bg['A'].copy();ell2=np.zeros(model.n)
    for iteration in range(30):
        sig=A*bg['H']*r;c=np.sqrt(1+sig*sig)
        z=np.array([A*sig,np.zeros(model.n),np.zeros(model.n),A*bg['m']*c,
            A*physical_source,np.zeros(model.n),np.sqrt(ell2),A*(bg['rb']-comp)*c,A*sig])
        g=model.geometry(0.,z)
        nextell=np.where(physical_source>0,r**3*g['g']/(1-r*g['g']),0.)
        if np.any(nextell<0):raise ValueError('source cannot have circular initial support in solved lapse')
        err=max(maximum(g['A']-A),maximum(nextell-ell2)/max(maximum(nextell),1e-80))
        if err<1e-9:break
        A=g['A'].copy();ell2=nextell
    else:raise ValueError('initial ordinary support iteration failed')
    model.initial_peak=float(np.max(physical_source));model.physical_source=physical_source
    model.comp=comp;model.initial_background=bg
    return z,dict(iterations=iteration+1,error=err,
        coordinate_source_integral=float((model.massint@physical_source)[-1]),
        coordinate_compensation_integral=float((model.massint@comp)[-1]),
        canonical_supported_rest=float(2*np.dot(model.volumes,z[4])),
        canonical_background_rest_excess=float(2*np.dot(model.volumes,z[7]-bg['rb']/bg['B'])),
        gravitational_mass_excess=float(g['mass'][-1]-bg['H'][-1]**2*r[-1]**3/2),
        background_j_outer=float(bg['j0'][-1]),actual_j_outer=float(g['j_total'][-1]))

def diagnose(model,t,z,independent=True):
    dz,g=model.rhs(t,z,True);r=model.r;mask=model.mask
    N,A=g['N'],g['A'];mr3=g['mass']/r**3
    ham=6*mr3+2*r*model.derivative(mr3)-g['rho_total']
    wdot=g['q']/g['Q']*dz[1]-g['sig']*g['X']/g['Q']*g['Xt']-g['q']/g['c']*g['sigt']
    fdot=A*wdot+g['phir']*g['adot']
    direct=N*(g['q_R']+g['q']*g['g'])
    integrability=maximum((fdot-direct)[mask])/max(maximum(direct[mask]),1e-12)
    controls=dict(Hamiltonian=maximum(ham[mask])/model.initial_peak,
                  phase_integrability=integrability,
                  inverse=model.max_inverse,
                  chi_state=maximum(g['chi_constraint_defect'])/maximum(g['chi']))
    if independent:
        old=(model.Aguess.copy(),model.chiguess.copy(),model.chirguess.copy());tangents=[]
        for fac in (1e-6,5e-7):
            dt=fac*model.tdyn
            gp=model.geometry(t+dt,z+dt*dz);gm=model.geometry(t-dt,z-dt*dz)
            at=A*A*(gp['mass']-gm['mass'])/(2*dt*r)
            ct=(gp['chi']-gm['chi'])/(2*dt)
            tangents.append((at,ct))
        model.Aguess,model.chiguess,model.chirguess=old
        ascale=max(maximum(g['adot'][mask]),model.kappa/model.tdyn)
        cscale=max(maximum(g['chi_t'][mask]),3*model.cTheta*model.bg0[5]**2)
        controls.update(mass_flow=maximum((tangents[-1][0]-g['adot'])[mask])/ascale,
            mass_tangent_step=maximum((tangents[0][0]-tangents[1][0])[mask])/ascale,
            chi_flow=maximum((tangents[-1][1]-g['chi_t'])[mask])/cscale,
            chi_tangent_step=maximum((tangents[0][1]-tangents[1][1])[mask])/cscale)
    bg=model.initial_background
    source_mass=model.massint@(model.physical_source/2)
    bareg=source_mass/r**2
    delta_g=g['g']-bg['exactg']
    cap_margin=(1+bg['s'])*(math.sqrt(1+model.eps)+bg['qr'])/((1+g['s'])*(math.sqrt(1+model.eps)+g['qr']))
    rbflux=[]
    for ni,pi,energy in ((4,5,g['es']),(7,8,g['eb'])):
        deriv,flux=model.rest_flux(z[ni],N*z[pi]/(A*A*energy))
        rbflux.append(dict(rest=float(2*np.dot(model.volumes,z[ni])),outer_flux=float(2*flux[-1]),
            flux_algebra_residual=float(2*np.dot(model.volumes,deriv)+2*flux[-1])))
    outerdt=1e-6*model.tdyn
    outer_ct=(model.outer_callback(t+outerdt)[0]-model.outer_callback(t-outerdt)[0])/(2*outerdt)
    diagnostics=dict(time=t,time_over_tdyn=t/model.tdyn,controls=controls,
        minimum_clock_margin_ratio=float(np.min(cap_margin)),minimum_clock_s=float(np.min(g['s'])),
        minimum_scalar_inverse_fraction=float(np.min(g['inverse']/g['d'])),
        minimum_multiplier_denominator=float(np.min(g['multiplier']['denominator'])),
        maximum_Cj_over_mu=float(np.max((model.C*g['j']*g['X']/g['m'])[mask])),
        maximum_relative_phase=float(np.max(abs(g['p'][mask]))),
        maximum_tilt=float(np.max(abs(g['sig'][mask]))),
        outer_chi_time_difference=float(g['chi_t'][-1]-outer_ct),
        geometry_iteration=g['geometry_iteration'],ordinary=rbflux,
        radius_over_L=(r[mask]/model.L).tolist(),gravity_excess=delta_g[mask].tolist(),
        ordinary_bare_reference=bareg[mask].tolist(),
        force_ratio_to_bare_ordinary=(delta_g[mask]/bareg[mask]).tolist(),
        caveat='force at one Cauchy slice; not rotation-curve prediction or native formation')
    return diagnostics,g

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--nodes',type=int,default=128)
    ap.add_argument('--extent',type=float,default=.002)
    ap.add_argument('--steps',type=int,default=0);ap.add_argument('--dt-factor',type=float,default=.12)
    ap.add_argument('--wall-seconds',type=float,default=45.);ap.add_argument('--tag',required=True)
    args=ap.parse_args();out=ROOT/('INVARIANT_CLOCK_COMPRESSION_SOURCE_'+args.tag+'_RESULT.json')
    cp=ROOT/('INVARIANT_CLOCK_COMPRESSION_SOURCE_'+args.tag+'_CHECKPOINT.json')
    if out.exists() or cp.exists():raise FileExistsError('exclusive source result/checkpoint already exists')
    if sha(oracle.CAL)!=oracle.CALSHA:raise ValueError('changed calibration')
    cal=json.loads(oracle.CAL.read_text());saved=json.loads(oracle.base.SOURCE.read_text());saved['inherited']=cal['fixed']
    reference=oracle.base.Model(saved,1);boundary=Boundary(reference)
    np.seterr(over='raise',divide='raise',invalid='raise')
    model=source.Polar(saved,args.nodes,args.extent,outer_callback=boundary);boundary.radius=model.r[-1]
    hashes={str(p):sha(p) for p in (Path(__file__),Path(source.__file__),Path(source.old.__file__),
        Path(source.radial.__file__),Path(source.multiplier.__file__),Path(oracle.__file__),oracle.CAL)}
    started=time.monotonic();snaps=[];z=None;step=0;error=None;reason='requested_steps_completed';prep=None
    dt=args.dt_factor*(model.r[1]-model.r[0]);fluxint=np.zeros(2)
    boundary_error=maximum(np.array(boundary.at(0.,64))-np.array(boundary.at(0.,128)))
    def state_checkpoint():
        if z is not None:
            with cp.open('w') as file:json.dump(dict(hashes=hashes,args=vars(args),step=step,dt=dt,
                state=z.tolist(),ordinary_flux_integral=fluxint.tolist(),snapshots=snaps),file,allow_nan=False)
    def flux(y,g):
        return np.array([2*model.rest_flux(y[ni],g['N']*y[pi]/(g['A']**2*g[en]))[1][-1]
                         for ni,pi,en in ((4,5,'es'),(7,8,'eb'))])
    try:
        z,prep=initial(model,reference)
        first,g=diagnose(model,0.,z);snaps.append(first)
        failed=[k for k,v in first['controls'].items() if v>(2e-12 if k=='inverse' else 1e-3)]
        if boundary_error>1e-10:failed.append('boundary_RK')
        if failed:reason='initial_control_failure';raise ValueError(', '.join(failed))
        for step in range(1,args.steps+1):
            if time.monotonic()-started>args.wall_seconds:
                step-=1;reason='bounded_wall_checkpoint';break
            t=(step-1)*dt
            aa,ga=model.rhs(t,z,True);ya=z+dt*aa/2
            bb,gb=model.rhs(t+dt/2,ya,True);yb=z+dt*bb/2
            cc,gc=model.rhs(t+dt/2,yb,True);yc=z+dt*cc
            dd,gd=model.rhs(t+dt,yc,True)
            fluxint+=dt*(flux(z,ga)+2*flux(ya,gb)+2*flux(yb,gc)+flux(yc,gd))/6
            z+=dt*(aa+2*bb+2*cc+dd)/6
            if step%64==0:
                snaps.append(diagnose(model,step*dt,z,False)[0]);state_checkpoint()
        if step>0:snaps.append(diagnose(model,step*dt,z,True)[0])
    except Exception as exc:
        error=dict(type=type(exc).__name__,message=str(exc),diagnostics=getattr(exc,'diagnostics',None))
        if reason=='requested_steps_completed':reason='technical_or_branch_failure'
    state_checkpoint()
    result=dict(protocol=__doc__,args=vars(args),hashes=hashes,reason=reason,error=error,
        steps=step,dt=dt,elapsed_seconds=time.monotonic()-started,preparation=prep,
        boundary_RK_error=boundary_error,snapshots=snaps,ordinary_flux_integral=fluxint.tolist(),
        trajectory_qualified=False,
        outstanding='independent spatial/time/domain convergence, complete constraints and boundary-work accounting')
    with out.open('x') as file:json.dump(result,file,indent=2,allow_nan=False)
    print(json.dumps(dict(reason=reason,error=error,steps=step,elapsed_seconds=result['elapsed_seconds'],
        preparation=prep,summaries=[{k:v for k,v in s.items() if k not in
        ('radius_over_L','gravity_excess','ordinary_bare_reference','force_ratio_to_bare_ordinary')} for s in snaps],
        result_sha256=sha(out)),indent=2),flush=True)
    if error:raise SystemExit(1)

if __name__=='__main__':main()
