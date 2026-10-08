"""Frozen-epoch source Green function for the current K(X) comparison.

Purpose: validate elimination of the fast mode without deleting slow
history or imposing zero flux. NOT a new galaxy, source-formation model,
cosmological trajectory or observational score. Use the two already tested
widths at Q100, unchanged budgets and two k=1/R scales R=5,50 kpc. This is
an infinitesimal Fourier response kernel, not a positive-density cosine
galaxy. Constant ordinary source forcing is a local susceptibility probe;
any finite supported source must obey the separate conserved shell model.

Freeze background for a SHORT interval. Let d=KXX,m=KX,Q=X,eta=C/KB,
S=delta_m+divZ/Q, Y=divZ/Q, 2lapPhi=rho_b+QS. In the linear weak-metric
subhorizon limit, Sdd=(J-W)S+W Y+f, Ydd=B S-(M2+B)Y,
J=mQ/2,W=m k^2/(Qd),B=2eta k^2/d,M2=eta Q^2,f=m rho_b/2.
Take zero material initial data and a constant source for t>=0. Hubble,
coefficient-drift, nonlinear/convective, stress and relativistic corrections
are NOT zero in the full model. Report Ht and H/nu; no Hubble-age extension.

The positive root lambda2 is a Jeans direction, NOT a ghost. The other root
is -nu2. Compute both without subtracting nearly equal large numbers. The
analytic exact frozen response is independently checked against RK4 over
two FAST periods (2048/4096 steps, fixed error gate1e-7), characteristic
identities and full second-order equations (gates2e-11), and initial data.
Report the fast-mode weight and its analytic envelope, not a new scientific
pass threshold. No numerical integration of a stiff Hubble-long system.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
import invariant_clock_depth_growth_v001 as inherited

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_LOCAL_SOURCE_KERNEL_V001_RESULT.json'


def exact(t,J,W,B,M2):
    O2=M2+B;F=O2+W-J
    root=math.hypot(F,2*math.sqrt(J*M2))
    l2=2*J*M2/(root+F);n2=F+l2;den=l2+n2
    # b=(n2-O2)/den would lose significant digits at large k.
    b=(W-J+l2)/den;a=1-b
    ll=math.sqrt(l2);nn=math.sqrt(n2)
    cs=2*(math.sinh(ll*t/2)/ll)**2
    cf=2*(math.sin(nn*t/2)/nn)**2
    ss=math.sinh(ll*t)/ll;sf=math.sin(nn*t)/nn
    ch=math.cosh(ll*t);co=math.cos(nn*t)
    S=a*cs+b*cf;Y=B/den*(cs-cf)
    Sd=a*ss+b*sf;Yd=B/den*(ss-sf)
    Sdd=a*ch+b*co;Ydd=B/den*(ch-co)
    dm=((M2+l2)*cs+(n2-M2)*cf)/den
    return dict(lambda_squared=l2,nu_squared=n2,slow_weight=a,fast_weight=b,
        S_over_f=S,Y_over_f=Y,Sdot_over_f=Sd,Ydot_over_f=Yd,
        Sddot_over_f=Sdd,Yddot_over_f=Ydd,delta_m_over_f=dm,
        slow_S_over_f=a*cs,fast_S_envelope_over_f=2*abs(b)/n2)


def rk4(J,W,B,M2,nu,steps):
    # tau=nu*t, and state=(S nu²/f,Y nu²/f,Sdot nu/f,Ydot nu/f).
    n2=nu*nu;h=4*math.pi/steps;y=np.zeros(4)
    def rhs(z):
        s,v,sd,vd=z
        return np.array([sd,vd,(J-W)/n2*s+W/n2*v+1,
                         B/n2*s-(M2+B)/n2*v])
    for _ in range(steps):
        aa=rhs(y);bb=rhs(y+h*aa/2);cc=rhs(y+h*bb/2);dd=rhs(y+h*cc)
        y+=h*(aa+2*bb+2*cc+dd)/6
    return y


def main():
    saved=json.loads(inherited.core.base.SOURCE.read_text())
    prior=BASE/'INVARIANT_CLOCK_DEPTH_GROWTH_V001_RESULT.json'
    if not json.loads(prior.read_text())['all_controls_passed']:
        raise ValueError('unqualified inherited calibration')
    controls=[];rows=[]
    def ck(name,value,gate):
        controls.append(dict(name=name,error=float(value),tolerance=gate,passed=bool(value<=gate)))
    L=.005*saved['inherited']['H0_km_s_Mpc']/299792.458
    tdyn=L/math.sqrt(1e-7) # inherited core/mass normalization, not fitted age
    for eps in (1e-6,6e-6):
        model,diag=inherited.model(saved,eps)
        aa,ss,Q,m,K,H,hx,qr=model.bg(0.);d=float(model.constitutive(ss)[2])
        eta=model.C/model.KB;J=m*Q/2;M2=eta*Q*Q
        for radius in (.005,.05):
            k=299792.458/(model.p['H0_km_s_Mpc']*radius)
            W=m*k*k/(Q*d);B=2*eta*k*k/d
            origin=exact(0.,J,W,B,M2);n2=origin['nu_squared'];l2=origin['lambda_squared']
            nu=math.sqrt(n2);tag=f'{eps}_{radius}'
            ck(tag+'_root_product',abs(l2*n2/(J*M2)-1),2e-11)
            ck(tag+'_root_sum',abs((n2-l2)/(M2+B+W-J)-1),2e-11)
            ck(tag+'_initial',max(abs(origin[x]) for x in
                ('S_over_f','Y_over_f','Sdot_over_f','Ydot_over_f')),2e-11)
            ck(tag+'_initial_acceleration',max(abs(origin['Sddot_over_f']-1),abs(origin['Yddot_over_f'])),2e-11)
            tcheck=4*math.pi/nu;sol=exact(tcheck,J,W,B,M2)
            zz=np.array([sol['S_over_f']*n2,sol['Y_over_f']*n2,
                         sol['Sdot_over_f']*nu,sol['Ydot_over_f']*nu])
            r1=rk4(J,W,B,M2,nu,2048);r2=rk4(J,W,B,M2,nu,4096)
            denom=max(float(np.max(abs(zz))),1.)
            ck(tag+'_RK4_exact',float(np.max(abs(r2-zz)))/denom,1e-7)
            ck(tag+'_RK4_refinement',float(np.max(abs(r2-r1)))/denom,1e-7)
            samples=[]
            for t in (tcheck,tdyn/10,tdyn):
                v=exact(t,J,W,B,M2);S=v['S_over_f'];Y=v['Y_over_f'];dm=v['delta_m_over_f']
                t1=J*S;t2=-W*dm;rhs=t1+t2+1
                # Reconstruct the Y equation through delta_m to avoid S-Y cancellation.
                y1=B*dm;y2=-M2*Y
                ck(tag+f'_S_equation_{t}',abs(v['Sddot_over_f']-rhs)/max(abs(t1)+abs(t2)+1,1),2e-11)
                ck(tag+f'_Y_equation_{t}',abs(v['Yddot_over_f']-y1-y2)/max(abs(y1)+abs(y2),1),2e-11)
                ck(tag+f'_charge_reconstruction_{t}',abs(S-Y-dm)/max(abs(S),abs(Y),abs(dm),1e-30),2e-11)
                v.update(t_H0=t,Ht=H*t,H_over_nu=H/nu,
                    source_potential_enhancement=J*S,
                    leading_t_squared_enhancement=J*t*t/2,
                    slow_enhancement=J*v['slow_S_over_f'],
                    fast_enhancement_envelope=J*v['fast_S_envelope_over_f'])
                samples.append(v)
            rows.append(dict(eps=eps,radius_Mpc=radius,k_Mpc_inverse=1/radius,
                background=dict(Q=Q,m=m,d=d,H=H,Hprime_over_H=hx),
                coefficients=dict(J=J,W=W,B=B,M_squared=M2),samples=samples))
    deps=('invariant_clock_depth_growth_v001.py','invariant_clock_transfer_v001.py',
          'plane_canonical_evolution_v001.py','bounded_clock_shared_prediction_v001.py')
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (prior,inherited.core.base.SOURCE)},
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in deps},
        inherited_core_dynamical_time_H0=tdyn,rows=rows,controls=controls,
        all_controls_passed=all(c['passed'] for c in controls))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],
        maximum_numerical_error=max(c['error'] for c in controls),
        rows=[dict(eps=r['eps'],radius_Mpc=r['radius_Mpc'],last=r['samples'][-1]) for r in rows],
        failed=[c for c in controls if not c['passed']]),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
