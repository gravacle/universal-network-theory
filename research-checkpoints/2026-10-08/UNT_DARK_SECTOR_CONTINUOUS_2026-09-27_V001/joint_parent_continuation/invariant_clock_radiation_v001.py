"""Perfect-radiation prerequisite for the SAME K(X) comparison action.

This is NOT a CMB spectrum, photon-baryon plasma, neutrino hierarchy,
thermal-origin calculation or observational score. Add ideal separately
conserved radiation OR=9e-5 to the existing cosmic budgets in both models,
without refitting charge: H(1)=sqrt(1+OR) in the inherited H0 units.
The ideal fluid is a declared benchmark, not a new physical radiation law.

Two fixed k=.01,.1/Mpc; a=1e-7 to .01. Initial common curvature1e-5,
zero relative entropy and Phi_dot=0, no independent vector/charge seed.
Finite-k growing-mode purity is checked by starting at half ai, not
assumed from a superhorizon formula. Use512/1024/2048 Gauss steps and
the existing1e-4 full-trajectory relative gate (floor1e-30), constraint
gate1e-6, identities1e-10, analytic pure-radiation potential1e-6.
Report linear clock-margin/spatial-gradient screens, not nonlinear proof.
No clipping, noise filter, discarded field, spectrum normalization fit,
recombination approximation or observational accept/reject threshold.

States: Psi, delta_b, H theta_b, F=delta_m/m, H theta_clock,
B=H(theta_clock+alpha), Zhat=kphys² Z/(Qm), delta_r, H theta_r.
B is evolved directly, an exact linear variable transformation which
avoids subtracting two nearly identical velocities. All fields retained.
Ordinary perfect-fluid conventions checked against Ma & Bertschinger,
https://arxiv.org/html/astro-ph/9506072v1 ; not their gravitational model.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_transfer_v001 as old
from charged_clock_response_v001 import gauss_step

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_RADIATION_V001_RESULT.json'
OR=9e-5
E=np.eye(9)
SEED=1e-5
AF=.01


def background(model,x,radiation=OR,dust=False):
    a,s,Q,m,Kfun,_,_,qr=model.bg(x)
    d=float(model.constitutive(s)[2]); cs=m/(Q*d)
    rb=3*model.OB/a**3; rr=3*radiation/a**4
    W=Q*m; rho=Q*m-Kfun
    if dust:
        W=3*model.p['omega_clock_excess']/a**3
        Q=model.Q0; m=W/Q; rho=W+3*model.OA; cs=0.
    H2=(rho+rb+rr)/3
    H=math.sqrt(H2); hx=-(W+rb+4*rr/3)/(2*H2)
    return dict(a=a,s=s,Q=Q,m=m,d=d,qr=qr,cs=cs,W=W,rb=rb,rr=rr,H=H,H2=H2,hx=hx)


def matrix(model,x,K,radiation=OR,dust=False):
    b=background(model,x,radiation,dust)
    Q,m,W,rb,rr,H,H2,hx,cs=(b[n] for n in ('Q','m','W','rb','rr','H','H2','hx','cs'))
    kp=(K/b['a'])**2; ratio=kp/H2; eta=model.C/model.KB
    psi,db,ub,F,uc,B,Z,dr,ur=E
    A=np.zeros((9,9))
    A[0]=-psi+(rb*ub+W*uc+4*rr*ur/3)/(2*H2)
    A[1]=3*A[0]-ratio*ub
    A[2]=hx*ub+psi
    coupling=2*eta*Q*kp/(m*H2)
    A[3]=3*A[0]+eta*Q/H*Z-coupling*B-ratio*uc
    A[4]=(hx+3*cs)*uc+cs*F+psi
    A[5]=(hx-eta*Q/H)*B+cs*F+3*cs*uc+W/(model.KB*kp)*Z
    A[6]=(3*cs+eta*Q/H)*Z-coupling*B
    A[7]=4*A[0]-4*ratio*ur/3
    A[8]=(hx+1)*ur+dr/4+psi
    return A,b


def constraint(b,K):
    kp=(K/b['a'])**2; H2=b['H2']; hx=b['hx']; cs=b['cs']
    wb=b['rb']/H2; wc=b['W']/H2; wr=b['rr']/H2
    terms=np.array([2*kp/H2,wb,3*wb,wc,3*wc,0.,-wc,wr,4*wr])
    deriv=terms*np.array([-2-2*hx,-3-2*hx,-3-2*hx,
        -3*(1+cs)-2*hx,-3*(1+cs)-2*hx,0.,-3*(1+cs)-2*hx,-4-2*hx,-4-2*hx])
    return terms,deriv


def initial(model,K,ai,radiation=OR,dust=False):
    b=background(model,math.log(ai),radiation,dust)
    enthalpy=b['W']+b['rb']+4*b['rr']/3
    psi=SEED/(1+2*b['H2']/enthalpy)
    vel=2*b['H2']*psi/enthalpy
    contrast=-2*((K/ai)**2+3*b['H2'])*psi/enthalpy
    return np.array([psi,contrast,vel,contrast,vel,0.,0.,4*contrast/3,vel])


def integrate(model,K,steps,ai=1e-7,dust=False):
    x0=math.log(ai); dx=math.log(AF/ai)/steps
    keep=np.array([0,1,2,3,4,7,8]) if dust else np.arange(9)
    z=initial(model,K,ai,dust=dust)[keep]; snapshots=[]
    max_constraint=0.; max_cap=0.; max_spatial=0.
    def mm(x):return matrix(model,x,K,dust=dust)[0][np.ix_(keep,keep)]
    for i in range(steps+1):
        x=x0+i*dx
        if i%(steps//64)==0:
            state=np.zeros(9); state[keep]=z
            _,b=matrix(model,x,K,dust=dust); cr,_=constraint(b,K)
            error=abs(cr@state)/max(float(abs(cr)@abs(state)),1e-30)
            max_constraint=max(max_constraint,error)
            if not dust:
                gap=model.Q0*model.eps/((1+b['s'])*(math.sqrt(1+model.eps)+b['qr']))
                low=model.Q0*model.eps*b['s']/((1+b['s'])*(b['qr']+1))
                max_cap=max(max_cap,abs(b['Q']*b['cs']*state[3])/min(low,gap))
                max_spatial=max(max_spatial,abs(K/b['a']*b['Q']*state[5]/b['H'])/model.bs)
            snapshots.append(dict(a=b['a'],state=state.tolist(),constraint=error))
        if i==steps:break
        z=gauss_step(z[:,None],x,dx,mm)[:,0]
    return dict(steps=steps,ai=ai,snapshots=snapshots,maximum_constraint=max_constraint,
                linear_clock_margin_ratio=max_cap,linear_spatial_ratio=max_spatial)


def error(left,right,indices=None):
    aa=np.array([r['state'] for r in left['snapshots']]);bb=np.array([r['state'] for r in right['snapshots']])
    if indices is not None:aa=aa[:,indices];bb=bb[:,indices]
    scale=np.maximum(np.max(abs(bb),axis=0),1e-30)
    return float(np.max(np.max(abs(aa-bb),axis=0)/scale))


def gauge_map(model,x,K):
    b=background(model,x,0.); Q,m,W,rb,H,hx,cs=(b[n] for n in ('Q','m','W','rb','H','hx','cs'))
    kp=(K/b['a'])**2; kap=math.sqrt(kp); eye=np.eye(7)
    fb,v,phase,sigma,z,pc,dw=eye
    T=-fb/H-(W+rb)*v/(2*H*kp)+z/(2*H*kap)+W*pc/(2*H*kp)+rb*dw/(2*H*kp)+1.5*m*phase/kp
    Tx=hx*fb/H-(W+rb)*v/(2*H*kp)*((-3*(1+cs)*W-3*rb)/(W+rb)-hx+2)
    Tx+=z/(2*H*kap)*(1-hx)+W*pc/(2*H*kp)*(-1-3*cs-hx)
    Tx+=rb*dw/(2*H*kp)*(-1-hx)-1.5*m*phase/kp
    HT=H*T; HTx=H*(hx*T+Tx)
    G=np.array([-fb-HT,dw-v-3*HT,HT,pc-v-3*HT,H*phase/Q+HT,
                H*(phase/Q-sigma/kap),-kap*z/W])
    Gx=np.array([-HTx,-3*HTx,HTx,-3*HTx,H*(hx+3*cs)*phase/Q+HTx,
                 H*((hx+3*cs)*phase/Q-(hx+1)*sigma/kap),(2+3*cs)*(-kap*z/W)])
    return G,Gx


def pure_radiation_control(K,steps=2048):
    ai=1e-7;af=.001;x0=math.log(ai);dx=math.log(af/ai)/steps
    def exact(a):
        yy=K*a/math.sqrt(3*OR)
        if abs(yy)<.05:
            phi=1-yy**2/10+yy**4/280-yy**6/15120
            deriv=-yy**2/5+yy**4/70-yy**6/2520
        else:
            phi=3*(math.sin(yy)-yy*math.cos(yy))/yy**3
            deriv=3*math.sin(yy)/yy-3*phi
        U=(deriv+phi)/2
        delta=-(2*(K*a)**2/OR*phi+12*U)/3
        return np.array([phi,delta,U])
    def mat(x):
        a=math.exp(x);ratio=(K*a)**2/OR
        return np.array([[-1.,0.,2.],[-4.,0.,8.-4*ratio/3],[1.,.25,-1.]])
    z=exact(ai);maxerr=0.
    for i in range(steps+1):
        if i%(steps//64)==0:
            maxerr=max(maxerr,abs(z[0]-exact(ai*math.exp(i*dx))[0]))
        if i<steps:z=gauss_step(z[:,None],x0+i*dx,dx,mat)[:,0]
    return float(maxerr)


def main():
    beg=time.monotonic(); saved=json.loads(old.base.SOURCE.read_text())
    saved['inherited']['Q0_over_H0']=100.
    model=old.base.Model(saved,1); controls=[]; identities=[]; results=[]
    def check(name,value,gate):
        controls.append(dict(name=name,error=float(value),tolerance=gate,passed=bool(value<=gate)))
    for kval in (.01,.1):
        K=kval*299792.458/model.p['H0_km_s_Mpc']
        for a in (1e-7,1e-5,.001,.01):
            A,b=matrix(model,math.log(a),K);cr,crx=constraint(b,K)
            residual=crx+cr@A+(3+2*b['hx'])*cr
            scale=np.maximum(abs(crx)+abs(cr)@abs(A)+abs((3+2*b['hx'])*cr),1e-30)
            check(f'constraint_identity_{kval}_{a}',np.max(abs(residual)/scale),1e-10)
        for a in (.01,.1,1.):
            x=math.log(a);As=old.matrix(model,x,K)[0];G,Gx=gauge_map(model,x,K)
            An=matrix(model,x,K,0.)[0][:7,:7]
            residual=Gx+G@As-An@G
            scale=max(float(np.max(abs(Gx)+abs(G)@abs(As)+abs(An)@abs(G))),1e-30)
            ee=float(np.max(abs(residual)))/scale
            identities.append(dict(k_Mpc_inverse=kval,a=a,dust_gauge_matrix_error=ee))
            check(f'dust_gauge_map_{kval}_{a}',ee,1e-10)
        check(f'pure_radiation_potential_{kval}',pure_radiation_control(K),1e-6)
        hist=[integrate(model,K,n) for n in (512,1024,2048)]
        fine=error(hist[1],hist[2]);check(f'time_refinement_{kval}',fine,1e-4)
        check(f'constraint_trajectory_{kval}',hist[-1]['maximum_constraint'],1e-6)
        half=integrate(model,K,2048,ai=5e-8)
        end=np.array(hist[-1]['snapshots'][-1]['state']);he=np.array(half['snapshots'][-1]['state'])
        norm=np.maximum(np.max(abs(np.array([r['state'] for r in half['snapshots']])),axis=0),1e-30)
        start_error=float(np.max(abs(end-he)/norm));check(f'initial_time_control_{kval}',start_error,1e-4)
        refs=[integrate(model,K,n,dust=True) for n in (1024,2048)]
        re=error(refs[0],refs[1],[0,1,2,3,4,7,8]);check(f'reference_refinement_{kval}',re,1e-4)
        rc=np.array(refs[-1]['snapshots'][-1]['state'])
        comparison=dict(potential_ratio=float(end[0]/rc[0]),ordinary_density_ratio=float(end[1]/rc[1]),
            clock_to_reference_matter_density_ratio=float((end[3]-end[6])/rc[3]),
            radiation_density_difference=float(end[7]-rc[7]),radiation_velocity_difference=float(end[8]-rc[8]))
        results.append(dict(k_Mpc_inverse=kval,histories=hist,half_start=half,references=refs,
                            coarse_error=error(hist[0],hist[1]),fine_error=fine,
                            initial_time_error=start_error,reference_error=re,final_comparison=comparison))
        print(json.dumps(dict(k_Mpc_inverse=kval,fine_error=fine,initial_time_error=start_error,
                   comparison=comparison)),flush=True)
    result=dict(protocol=__doc__,radiation_omega=OR,unchanged_clock_charge=model.p['d0'],
                H_at_one=background(model,0.)['H'],fixed=model.p,identities=identities,
                rows=results,controls=controls,all_controls_passed=all(c['passed'] for c in controls),
                elapsed_seconds=time.monotonic()-beg,
                hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                  (Path(__file__),Path(old.__file__),Path(old.base.__file__),old.base.SOURCE,
                   BASE/'charged_clock_response_v001.py')})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','protocol','fixed')}),flush=True)


if __name__=='__main__':main()
