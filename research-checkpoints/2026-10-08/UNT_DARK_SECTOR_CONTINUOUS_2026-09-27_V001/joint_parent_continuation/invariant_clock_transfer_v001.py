"""One fixed finite-k cross-domain clock-scale test for proposed K(X).

At k=.01/Mpc, propagate two declared development preparations at ai=.01:
baryon isocurvature at rest and adiabatic initial Phi_dot=0. Use the SAME
background density, clock function, KB,J and scale calibration; compare
Q0/H0=1,10,100, the existing universal clock freedom, not a galaxy fit.
Conserved phase charge changes inversely with Q0 to preserve Qm; count
this as background-equivalent parameter variation, not a native selection.
Numerical 2048/4096/8192 Gauss steps, all seven retained linear states,
metric/velocity/proper density observables at65 epochs. Freeze relative
fine-state gate1e-4 with1e-30 floor (no omitted fast oscillations).
Report failed rows without acceptance or post-hoc changes of tolerance.

The independently reviewed finite-k equations below retain expansion and
gravity. Fixed initial contrasts1e-5 are LINEAR tangent preparations, not
a certification of exact nonlinear clock-domain admissibility or population.
Use a common pressureless-component comparator with the same .7/.049/.251
normalizations, no fit or data scoring. Neither this reference nor inherited
GN labels validate the revised action's local Newton calibration.

Check the fixed-coefficient material dispersion by characteristic polynomial
at three epochs; it is not the full gravitating FLRW normal-mode spectrum.
Also verify zeta*cL²=cad²(2/KB+zeta) and unchanged H(a) across Q0.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import plane_canonical_evolution_v001 as base
import charged_clock_response_v001 as solver

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_TRANSFER_V001_RESULT.json'
E=np.eye(7)


def matrix(m,x,K):
    a,s,Q,qm,Kfun,H,hx,qr=m.bg(x);d=float(m.constitutive(s)[2])
    R=3*m.OB/a**3;eta=m.C/m.KB;kap=K/a
    A=np.zeros((7,7))
    A[0,2]=-qm/(2*H)
    A[1,0]=-kap*kap/(H*H);A[1,1]=-(Q*qm+R)/(2*H*H)
    A[1,4]=kap/(2*H*H);A[1,5]=Q*qm/(2*H*H);A[1,6]=R/(2*H*H)
    A[2,1]=-qm/(d*H);A[2,5]=qm/(d*H)
    A[3,2]=eta*kap/H;A[3,3]=-eta*Q/H-1;A[3,4]=1/(m.KB*H)
    A[4,2]=2*eta*Q*kap/H;A[4,3]=-2*eta*Q*Q/H;A[4,4]=eta*Q/H-2
    A[5,2]=-(2*eta+qm/Q)*kap*kap/(qm*H)
    A[5,3]=2*eta*Q*kap/(qm*H);A[5,4]=-eta*kap/(qm*H)
    theta=a*a*(H*A[1]+1.5*qm*E[2])/(K*K)
    T=np.array([-E[0]-H*theta,E[6]-E[1]-3*H*theta,theta,
                E[5]-E[1],E[6]-E[1]])
    return A,T


def initial(m,K):
    a,s,Q,qm,Kfun,H,hx,qr=m.bg(math.log(.01));kap2=(K/a)**2
    W=Q*qm/3;rb=m.OB/a**3;seed=1e-5
    z=np.zeros((7,2))
    # v=0 fixes residual spatial-coordinate gauge, not density evolution.
    phi=-1.5*rb*seed/kap2;z[0,0]=-phi;z[6,0]=seed
    phi=-1.5*(W+rb)*seed/(kap2+3*H*H);theta=2*H*phi/(3*(W+rb))
    z[0,1]=-phi-H*theta;z[5,1]=z[6,1]=seed+3*H*theta
    return z


def integrate(m,K,steps):
    scale=np.array([1/K**2,1.,m.Q0/K**2,1/K,1/K,1.,1.])
    x0=math.log(.01);dx=-x0/steps;z=initial(m,K)/scale[:,None];snaps=[]
    def mm(x):return matrix(m,x,K)[0]*scale[None,:]/scale[:,None]
    for i in range(steps+1):
        x=x0+i*dx
        if i%(steps//64)==0:
            state=z*scale[:,None];obs=matrix(m,x,K)[1]@state
            snaps.append(dict(a=math.exp(x),state=state.tolist(),observables=obs.tolist()))
        if i==steps:break
        z=solver.gauss_step(z,x,dx,mm)
    return dict(steps=steps,snapshots=snaps)


def reference(m,K,steps):
    oa=m.OA;ob=m.OB;oc=m.p['omega_clock_excess'];x0=math.log(.01);dx=-x0/steps
    scale=np.array([1/K**2,1.,1/K**2,1.,1/K**2])
    def bg(x):
        a=math.exp(x);rb=ob/a**3;rc=oc/a**3;H=math.sqrt(oa+rb+rc)
        return a,rb,rc,H
    def mat(x):
        a,rb,rc,H=bg(x);kp=K*K/(a*a);A=np.zeros((5,5))
        A[0]=[-1.,0.,1.5*rb/H,0.,1.5*rc/H]
        A[1]=3*A[0];A[1,2]-=kp/H;A[2,0]=1/H
        A[3]=3*A[0];A[3,4]-=kp/H;A[4,0]=1/H
        return A*scale[None,:]/scale[:,None]
    a,rb,rc,H=bg(x0);kp=K*K/(a*a);seed=1e-5;y=np.zeros((5,2))
    y[0,0]=-1.5*rb*seed/kp;y[1,0]=seed
    ph=-1.5*(rb+rc)*seed/(kp+3*H*H);theta=2*H*ph/(3*(rb+rc))
    y[:,1]=[ph,seed,theta,seed,theta];y/=scale[:,None];snaps=[]
    for i in range(steps+1):
        if i%(steps//64)==0:snaps.append((y*scale[:,None]).tolist())
        if i==steps:break
        y=solver.gauss_step(y,x0+i*dx,dx,mat)
    return dict(steps=steps,snapshots=snaps)


def error(a,b,key):
    za=np.array([s[key] for s in a['snapshots']]);zb=np.array([s[key] for s in b['snapshots']])
    return float(np.max(np.max(abs(za-zb),axis=0)/np.maximum(np.max(abs(zb),axis=0),1e-30)))


def main():
    beg=time.monotonic();saved=json.loads(base.SOURCE.read_text());K=saved['fixed']['K'];rows=[];identities=[]
    models=[]
    for Q0 in (1.,10.,100.):
        copy=json.loads(json.dumps(saved));copy['inherited']['Q0_over_H0']=Q0;m=base.Model(copy,1);models.append(m)
        hist=[integrate(m,K,n) for n in (2048,4096,8192)]
        rows.append(dict(Q0_over_H0=Q0,histories=hist,coarse_error=error(hist[0],hist[1],'state'),
                         fine_error=error(hist[1],hist[2],'state'),observable_error=error(hist[1],hist[2],'observables')))
        for a in (.01,.1,1.):
            x=math.log(a);aa,s,Q,qm,Kfun,H,hx,qr=m.bg(x);d=float(m.constitutive(s)[2]);eta=m.C/m.KB
            zeta=qm/(m.C*Q);cad=qm/(Q*d);cL=(2*eta+qm/Q)/d;kap=K/a
            B=np.array([[0.,0.,0.,1/d],[eta*kap,-eta*Q,1/m.KB,0.],
                        [2*eta*Q*kap,-2*eta*Q*Q,eta*Q,0.],
                        [-(2*eta+qm/Q)*kap*kap,2*eta*Q*kap,-eta*kap,0.]])
            gap=eta*Q*Q;speed=math.sqrt(gap+cL*kap*kap)
            poly=np.poly(B/speed).real;target=np.array([1.,0.,1.,0.,gap*cad*kap*kap/speed**4])
            identities.append(dict(Q0=Q0,a=a,zeta=zeta,c_clock_squared=cad,c_long_squared=cL,
                gap_squared=gap,high_k_lower_frequency_squared=qm*Q/(2+m.KB*zeta),
                material_polynomial_absolute_error=float(max(abs(poly-target))),
                cross_identity_relative_error=abs(zeta*cL-cad*(2/m.KB+zeta))/(cad*(2/m.KB+zeta)),H=H))
        print(json.dumps({k:v for k,v in rows[-1].items() if k!='histories'}),flush=True)
    ref=[reference(models[0],K,n) for n in (2048,4096)]
    ra=np.array(ref[0]['snapshots']);rb=np.array(ref[1]['snapshots'])
    re=float(np.max(np.max(abs(ra-rb),axis=0)/np.maximum(np.max(abs(rb),axis=0),1e-30)))
    for row in rows:
        obs=np.array(row['histories'][-1]['snapshots'][-1]['observables'])
        row['final_ratios_to_pressureless_reference']=(obs[:3]/rb[-1,:3]).tolist()
    hh=np.array([r['H'] for r in identities]).reshape(3,3)
    checks=dict(time_refinement=all(r['fine_error']<=1e-4 for r in rows),reference_refinement=re<=1e-4,
        material_polynomial=max(r['material_polynomial_absolute_error'] for r in identities)<=1e-8,
        cross_identity=max(r['cross_identity_relative_error'] for r in identities)<=1e-12,
        same_background=float(np.max(abs(hh/hh[0]-1)))<=1e-12)
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(base.SOURCE.read_bytes()).hexdigest(),
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in
            ['plane_canonical_evolution_v001.py','charged_clock_response_v001.py','bounded_clock_shared_prediction_v001.py']},
        k_Mpc_inverse=.01,K=K,preparations=['baryon_isocurvature','adiabatic_development'],
        observables=['Bardeen_Phi','Newtonian_delta_b','theta_b','proper_clock_charge','proper_dust_density'],
        rows=rows,identities=identities,pressureless_reference=ref,reference_error=re,
        controls=checks,all_controls_passed=bool(all(checks.values())),elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(controls=checks,elapsed_seconds=result['elapsed_seconds'],comparisons=
        [{k:v for k,v in r.items() if k!='histories'} for r in rows]),indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
