"""Saved-state diagnosis of the failed clock/current grid comparison.

No trajectory rerun. Compare numerical primitive chain rule with the exact
mixed-p equation on the SAME full saved state. It is a numerical-cause
diagnostic, not evidence for changing the action, tolerances or initial data.
"""
from pathlib import Path
import json
import hashlib
import numpy as np
import invariant_clock_polar_source_v004 as src

BASE=Path(__file__).resolve().parent


def audit(name):
    path=BASE/name;data=json.loads(path.read_text());cp=json.loads((BASE/data['checkpoint']).read_text())
    mm=src.Polar(json.loads(src.prev.inherited.SOURCE.read_text()),data['args']['nodes'],data['args']['extent'])
    mm.initial();z=np.array(cp['state']);t=cp['step']*cp['dt'];dz,g=mm.rhs(t,z,True)
    A=g['A'];N=g['N'];sig=g['sig'];c=g['c'];X=g['X'];Q=g['Q'];q=g['q'];w=g['w'];p=g['p'];m=g['m'];d=g['d']
    adot=N*mm.r*(-z[0]*g['divZ']+z[3]*z[1]-z[4]*z[5]-z[7]*z[8])/(2*A)
    st=dz[0]/A-sig*adot;wt=dz[1]/A-w*adot;zt=dz[2]
    Dp=-mm.C*(2/mm.KB+g['jt'])
    Mw=m*w/(X*q)+sig*Dp*Q/q;Ms=g['DD']+sig*Dp*Q/c
    mt=dz[3]/A-g['target']*adot
    xt=(mt-Mw*wt-Ms*st-sig*(mm.C/mm.KB)*zt)/g['inverse']
    pt_old=Q/c*st+Q/q*wt+sig*X/q*xt
    Xdiff=mm.Q0*mm.eps*g['s']/((1+g['s'])*(g['qr']+1))
    xr=mm.derivative(Xdiff);pr=mm.derivative(p,-1)
    sr=(mm.derivative(z[0],-1)-z[0]*g['ar'])/A
    FF=N*c*X*xr/(A*q)+N*w*pr/(A*q)-N*Q*p*sr/(A*q*c*c)+N*Q*g['e']/c-Q*p*adot/(q*c)
    Mx=d*q/X+m*(c/Q-q/X**2);Mp=m*w/(X*Q)+sig*Dp
    Ms2=g['DD']-m*w/(c*X)
    denom=Mx+Mp*sig*X/q
    xt_new=(mt-Mp*FF-Ms2*st-sig*(mm.C/mm.KB)*zt)/denom
    pt_new=FF+sig*X/q*xt_new
    q_discrete=mm.derivative(Xdiff+w*w/(q+X))
    q_chain=-w*sr/c+c*X*xr/Q+w*pr/Q
    mask=mm.mask
    mx=lambda x:float(np.max(abs(x[mask])))
    return dict(file=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        inverse_denominator_identity=mx((denom-g['inverse'])/g['inverse']),
        exact_variable_pt_discrepancy=mx(pt_old-pt_new),
        old_pt_scale=mx(pt_old),new_pt_scale=mx(pt_new),
        phase_gradient_chain_defect=mx(q_discrete-q_chain),
        relative_defect_to_new_pt=mx(pt_old-pt_new)/max(mx(pt_new),1e-30),
        clock_time_derivative_discrepancy=mx(xt-xt_new),
        old_clock_time_scale=mx(xt),new_clock_time_scale=mx(xt_new),
        max_physical_p=mx(p),point_of_max_defect_over_L=float(mm.r[mask][np.argmax(abs((pt_old-pt_new)[mask]))]/mm.L))


def main():
    rows=[audit('INVARIANT_CLOCK_POLAR_SOURCE_CENTRAL'+n+'_RESULT.json') for n in ('01','02')]
    out=BASE/'INVARIANT_CLOCK_POLAR_CHAIN_RULE_V001_RESULT.json'
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows)
    with out.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False),flush=True)


if __name__=='__main__':main()
