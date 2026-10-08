"""One finite-k amplification diagnostic, no spatial/physical parameter sweep.

Use the already identified n218 harmonic of the N513 constrained V002
trajectory, k=2.18/Mpc. Propagate its actual saved a=.01 and a=.1 Fourier
vectors with the independently derived FULL finite-d linear geodesic
system. Source is the Fourier coefficient of the historical dust weight.
No arbitrary amplified seed, filter or altered action. Propagate to a=1,
but compare physical proper-density/charge and Bardeen potential, not pc
alone. Agreement/disagreement with saved nonlinear Fourier coefficients
is diagnostic only; it does not accept the failed nonlinear trajectory.

Numerical checks fixed before running: 512/1024/2048 Gauss steps,1e-4
relative state convergence with1e-35 absolute denominator floor. Verify
time-dependent gauge dictionary against the OLD seven-state Newtonian
equations at five epochs, fourth-order derivative with1e-4/2e-4 ln-a steps,
relative matrix identity<=1e-7. Report all results and failures. A frozen
matrix eigenvalue is not a time-dependent stability theorem.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import plane_canonical_evolution_v001 as base
import plane_source_precision_v001 as precise
import charged_clock_response_v001 as newton

BASE=Path(__file__).resolve().parent
INPUT=BASE/'PLANE_CONSTRAINED_EVOLUTION_V002_RESULT.json'
OUT=BASE/'PLANE_HIGH_MODE_TRANSFER_V001_RESULT.json'
NMODE=218
E=np.eye(7)


def operator(m,x,K):
    a,s,Q,qm,kfun,H,hx,q=m.bg(x);d=m.constitutive(s)[2]
    R=3*m.OB/a**3;eta=m.C/m.KB;r=eta*Q;b=qm-2*r
    A=np.zeros((7,7)) # fb,v,phase,sigma,z,pc,dust_weight_contrast
    A[0,2]=-qm/(2*H)
    A[1,0]=-K*K/(a*a*H*H);A[1,1]=-(Q*qm+R)/(2*H*H)
    A[1,4]=K/(2*a*H*H);A[1,5]=Q*qm/(2*H*H);A[1,6]=R/(2*H*H)
    A[2,1]=-qm/(d*H);A[2,5]=qm/(d*H)
    A[3,2]=m.C*K/(m.KB*a*H);A[3,3]=-r/H-1;A[3,4]=1/(m.KB*H)
    A[4,2]=-b*K/(a*H);A[4,3]=b*Q/H;A[4,4]=r/H-2
    A[5,2]=-2*eta*K*K/(a*a*qm*H);A[5,3]=-b*K/(a*qm*H);A[5,4]=-eta*K/(a*qm*H)
    theta=a*a*(H*A[1]+1.5*qm*E[2])/(K*K)
    T=np.array([-E[0]-H*theta,E[6]-E[1]-3*H*theta,theta,
        E[5]-E[1]-3*H*theta+K*E[4]/(a*Q*qm),E[2]/Q+theta,
        -a*E[4]/K,-a*E[3]/K-theta])
    return A,T


def initial_from_snapshot(m,snap):
    z=np.array(snap['state']);f=np.fft.rfft(z,axis=-1)*2/z.shape[-1]
    dust=np.fft.rfft(m.dust_weight-1)*2/m.N
    return np.array([f[1,NMODE].real,(f[0,NMODE]+2*f[1,NMODE]).real,
        f[3,NMODE].real,-f[2,NMODE].imag,-f[6,NMODE].imag,
        f[7,NMODE].real,dust[NMODE].real])


def observables(m,x,K,z):
    A,T=operator(m,x,K);nn=T@z
    return dict(a=math.exp(x),pc=float(z[5]),dust_comoving_density=float(z[6]-z[1]),
        proper_clock_charge=float(z[5]-z[1]),Bardeen_potential=float(nn[0]))


def integrate(m,K,z0,ai,steps):
    scale=np.array([1.,1.,1/K**2,1/K,1/K,1.,1.]);z=z0/scale
    x0=math.log(ai);dx=-x0/steps;snaps=[]
    def matrix(x):return operator(m,x,K)[0]*scale[None,:]/scale[:,None]
    for i in range(steps+1):
        x=x0+i*dx
        if i%(steps//64)==0:snaps.append(dict(state=(z*scale).tolist(),**observables(m,x,K,z*scale)))
        if i==steps:break
        z=newton.gauss_step(z,x,dx,matrix)
    return dict(steps=steps,initial_a=ai,snapshots=snaps)


def main():
    started=time.monotonic();saved=json.loads(base.SOURCE.read_text());old=json.loads(INPUT.read_text())
    m=base.Model(saved,513);K=NMODE*m.K;p=saved['inherited']
    newton.KB=m.KB;newton.C=m.C;newton.OB=m.OB;newton.OA=m.OA
    newton.OC=p['omega_clock_excess'];newton.D0=p['d0'];newton.Q0=m.Q0
    newton.EPS=m.eps;newton.WAVENUMBER=K
    identities=[];spectra=[]
    for a in (.01,.03,.1,math.sqrt(.1),1.):
        x=math.log(a);A,T=operator(m,x,K);An,b=newton.matrix(x)
        for step in (1e-4,2e-4):
            Ts=[operator(m,x+j*step,K)[1] for j in (-2,-1,1,2)]
            deriv=(Ts[0]-8*Ts[1]+8*Ts[2]-Ts[3])/(12*step)
            lhs=deriv+T@A;rhs=An@T
            identities.append(dict(a=a,step=step,relative=float(np.linalg.norm(lhs-rhs)/max(np.linalg.norm(rhs),1e-300))))
        scale=np.array([1.,1.,1/K**2,1/K,1/K,1.,1.]);B=A*scale[None,:]/scale[:,None]
        ev,vec=np.linalg.eig(B)
        residual=np.linalg.norm(B@vec-vec*ev[None,:])/(np.linalg.norm(B)*np.linalg.norm(vec))
        spectra.append(dict(a=a,eigenvalues_per_ln_a=[[float(v.real),float(v.imag)] for v in ev],relative_residual=float(residual)))
    cases=[]
    for index in (0,32):
        snap=old['rows'][-1]['snapshots'][index];z0=initial_from_snapshot(m,snap)
        histories=[integrate(m,K,z0,snap['a'],n) for n in (512,1024,2048)]
        zz=[np.array([s['state'] for s in h['snapshots']]) for h in histories]
        err=np.max(abs(zz[1]-zz[2]),axis=0)/np.maximum(np.max(abs(zz[2]),axis=0),1e-35)
        comparisons=[]
        for oldindex in (32,48,64):
            ss=old['rows'][-1]['snapshots'][oldindex]
            if ss['a']<snap['a']*(1-1e-12):continue
            target=min(histories[-1]['snapshots'],key=lambda s:abs(math.log(s['a']/ss['a'])))
            actual=observables(m,math.log(ss['a']),K,initial_from_snapshot(m,ss))
            comparisons.append(dict(predicted=target,saved_nonlinear=actual))
        cases.append(dict(initial_a=snap['a'],initial_state=z0.tolist(),convergence_per_variable=err.tolist(),
            max_convergence=float(max(err)),histories=histories,comparison=comparisons))
    checks=dict(gauge_identity=max(s['relative'] for s in identities)<=1e-7,
        transfer_convergence=all(c['max_convergence']<=1e-4 for c in cases),
        eigenpair_residual=max(s['relative_residual'] for s in spectra)<=1e-10)
    dependencies=['plane_canonical_evolution_v001.py','charged_clock_response_v001.py','bounded_clock_shared_prediction_v001.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (base.SOURCE,INPUT)},
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in dependencies},
        physical_k_Mpc_inverse=NMODE*.01,variables=['fb','v','phase','sigma','z','pc','dust_weight_contrast'],
        gauge_identities=identities,frozen_spectra=spectra,cases=cases,controls=checks,
        all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-started)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(controls=checks,gauge_identity=max(s['relative'] for s in identities),
        convergence=[c['max_convergence'] for c in cases],spectra=spectra,
        comparisons=[c['comparison'] for c in cases],elapsed_seconds=result['elapsed_seconds']),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
