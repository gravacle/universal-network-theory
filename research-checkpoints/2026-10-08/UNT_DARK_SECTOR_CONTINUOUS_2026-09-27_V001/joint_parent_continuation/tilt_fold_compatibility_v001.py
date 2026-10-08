"""Saved-state invariant compatibility at the homogeneous inverse fold.

No new evolution. Schur zero need not destroy covariant hyperbolicity:
rest-frame longitudinal coefficients d=KQQ and A=C(2/KB+jt) can remain
positive. But differentiate F=c m+sigma Dp-M=0 along actual homogeneous
flow: Qdot=-c N/Schur, with the fixed-Q derivative N computed below.
Nonzero limiting N prevents a smooth classical homogeneous crossing in
ANY coordinates; a refoliation alone cannot remove U.gradQ=c Qdot.

Evaluate all three saved captured fold states. They lie slightly beyond
the last accepted stage, with F_fold>0, NOT exactly on the solution.
Report that residual and refinement explicitly; no singularity theorem
from one floating-point state. Verify N by centered fixed-Q directional
differences at two steps (1e-7/H,5e-8/H),relative<=1e-7. Check positive
rest-frame cone and characteristic relation v²A/d=1 at the fold1e-8.
Also evaluate saved regular checkpoints. No branchjump, changed model,
new free parameter, causal-number interpretation or full Stage3 closure.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import homogeneous_tilt_saturation_v001 as prior
import homogeneous_tilt_extended_branch_v001 as extended

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'HOMOGENEOUS_TILT_EXTENDED_BRANCH_V001_RESULT.json'
OUT=BASE/'TILT_FOLD_COMPATIBILITY_V001_RESULT.json'


def evaluate(model,a,z,s):
    x=math.log(a);h=model.bg(x)[5];fa,fb,un,phase,pa,pb,pu,pc=z[:,0]
    ev=math.exp(fa+2*fb);V=a**3*ev;sig=un*math.exp(-fa);c=math.sqrt(1+sig*sig)
    Z=pu*math.exp(-2*fb);M=model.pcbar*(1+pc)/(2*V)
    Q,m,d,Kfun,dm,qroot=model.constitutive(s);p=sig*Q/c;e=(Z-model.C*p)/model.KB
    root=math.sqrt(p*p+model.bs**2);j=model.lam*abs(p)/root
    jt=model.lam*abs(p)*(p*p+2*model.bs**2)/root**3
    J=model.lam*(abs(p)*root-model.bs**2*math.asinh(abs(p)/model.bs))
    E=V*(model.KB*e*e+model.C*p*p+model.C*J-2*Kfun)+model.pcbar*(1+pc)*Q/c+6*model.OB
    pia=-4*a**3*h*(1+pa);pib=pia/2+4*V*E/pia
    k=(pia-pib)/(4*V);l=-pia/(4*V)
    Dp=model.C*(e-(1+j)*p);A=model.C*(2/model.KB+jt);eta=model.C/model.KB
    S=Q*Dp+m*p;sigmadot=e-k*sig;Zdot=S/c-2*l*Z;Mdot=-(k+2*l)*M
    N=(sig*m/c+Dp-sig*A*Q/c**3)*sigmadot+sig*eta*Zdot-Mdot
    def F(sg,zz,mm):
        cc=math.sqrt(1+sg*sg);pp=sg*Q/cc
        jj=model.lam*abs(pp)/math.sqrt(pp*pp+model.bs**2)
        return cc*m+sg*model.C*((zz-model.C*pp)/model.KB-(1+jj)*pp)-mm
    errors=[]
    for dt in (1e-7/h,5e-8/h):
        fd=(F(sig+dt*sigmadot,Z+dt*Zdot,M+dt*Mdot)-F(sig-dt*sigmadot,Z-dt*Zdot,M-dt*Mdot))/(2*dt)
        errors.append(abs(fd-N)/max(abs(N),1e-300))
    schur=c*c*d-sig*sig*A
    return dict(a=a,s=s,Q=float(Q),KQ=float(m),KQQ=float(d),longitudinal_coefficient=float(A),
        physical_tilt=sig,vector_relative_speed=sig/c,rest_longitudinal_speed_squared=float(A/d),
        characteristic_product=float((sig/c)**2*A/d),Schur=float(schur),
        F=float(F(sig,Z,M)),F_relative_to_slice_charge=float(F(sig,Z,M)/M),
        N_fixed_Q_derivative=float(N),N_finite_difference_relative_errors=errors,
        mean_expansion=(k+2*l)/3,shear=k-l,scalar_Qdot=float(-c*N/schur) if schur else None)


def main():
    beg=time.monotonic();src=json.loads(SOURCE.read_text());saved=json.loads(prior.base.SOURCE.read_text())
    model=prior.Model(saved);rows=[]
    for row in src['rows']:
        cap=row['failure']['capture']
        out=evaluate(model,cap['a'],np.array(cap['state_reduced']),cap['s_fold'])
        out['source_steps']=row['steps'];rows.append(out)
    regular=[]
    for snap in src['rows'][-1]['snapshots'][-4:]:
        regular.append(evaluate(model,snap['a'],np.array(snap['state']),snap['min_aux_s']))
    checks=dict(compatibility_identity=max(max(r['N_finite_difference_relative_errors']) for r in rows+regular)<=1e-7,
        rest_frame_cone=all(r['KQQ']>0 and r['longitudinal_coefficient']>0 for r in rows),
        characteristic_fold=max(abs(r['characteristic_product']-1) for r in rows)<=1e-8)
    deps=['homogeneous_tilt_saturation_v001.py','homogeneous_tilt_extended_branch_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in deps},
        captured_fold_rows=rows,regular_rows=regular,controls=checks,all_controls_passed=all(checks.values()),
        elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(result,indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
