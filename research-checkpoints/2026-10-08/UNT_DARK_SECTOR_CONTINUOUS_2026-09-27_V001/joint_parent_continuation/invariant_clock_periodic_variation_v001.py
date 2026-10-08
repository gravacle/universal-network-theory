"""Independent canonical structure/variation checks, no dynamics or fit.

Use the original Lagrangian, not delta_core, for a direct integrated Hcan.
Test directional coordinate derivatives at fixed canonical momenta against
negative exact momentum RHS. A resolved off-constraint state is chosen:
zero metric offsets, u=1e-6 sin(kx),phase=1e-8 cos(kx),zero momenta offsets.
Variation directions [.1cos,.1cos,1e-6sin,1e-8cos], separately; eps1e-3,
5e-4. Frozen relative1e-4; fixed17/33 grids. Linear modal Hamiltonian
identity B^dagger Omega+Omega B=0, Omega=S^T J S, gate1e-10. Exclusive
receipt, same action, no change to scientific initial data or tolerances.
"""
from pathlib import Path
import json,time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial
import invariant_clock_periodic_exact_v001 as exact
import invariant_clock_periodic_linear_v001 as linear

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_PERIODIC_VARIATION_V001_RESULT.json'
sha=initial.sha

def energy(run,x,z):
    g=run.fields(x,z);A=g['A'];V=g['V'];sig=g['u']/A;c=np.hypot(1,sig)
    ax=run.dx(z[0]);bx=run.dx(z[1]);sigx=(run.dx(g['u'])-g['u']*ax)/A
    w=run.dx(z[3])/A;p=sig*g['q']+c*w;e=(g['udot']+sig*sigx/c)/A
    Theta=g['adot']/c+2*c*g['bdot']+sig*g['udot']/(A*c)+(sigx+2*sig*bx)/A
    zz=abs(p)/run.m.bs;JJ=run.m.lam*run.m.bs**2*(2*zz**3/3-zz**5/5+3*zz**7/28-5*zz**9/72)
    core=-4*g['adot']*g['bdot']-2*g['bdot']**2+run.KB*e*e+2*run.C*e*p-run.C*(p*p+JJ)+2*g['K']-run.cT*Theta**2
    L=V*core+2*(g['B']**2/A)*bx*bx
    return float(np.mean(g['pi_a']*g['adot']+g['pi_b']*g['bdot']+g['pi_u']*g['udot']+g['pi_phi']*g['q']-L))

def main():
    if OUT.exists():raise FileExistsError(OUT)
    model,parent=initial.load();checks=[];rows=[];error=None;t0=time.monotonic()
    def check(name,e,gate):checks.append(dict(name=name,error=float(e),gate=gate,passed=bool(e<=gate)))
    try:
        for N in (17,33):
            prep=initial.mapped_seed(model,parent,N);x=prep['x'];run=exact.PeriodicExact(model,N,prep['k'])
            S=np.diag(linear.scales(run));J=np.block([[np.zeros((4,4)),np.eye(4)],[-np.eye(4),np.zeros((4,4))]])
            Om=S.T@J@S;B=linear.matrices(run,x)
            terms=np.array([B.conj().transpose(0,2,1)@Om,Om@B]);defect=terms.sum(axis=0)
            check(f'{N}_modal_symplectic',np.max(abs(defect))/max(np.max(np.sum(abs(terms),axis=0)),1e-30),1e-10)
            ph=prep['spatial_grid'];z=np.zeros((8,N));z[2]=1e-6*np.sin(ph);z[3]=1e-8*np.cos(ph)
            f,g=run.rhs_proper(x,z,return_fields=True);pt=f[4:].copy();pt[0]+=g['pi_a_bar_dot'];pt[1]+=g['pi_b_bar_dot']
            directions=np.array([.1*np.cos(ph),.1*np.cos(ph),1e-6*np.sin(ph),1e-8*np.cos(ph)])
            details=[]
            for i in range(4):
                target=-float(np.mean(pt[i]*directions[i]))
                for eps in (1e-3,5e-4):
                    dz=np.zeros_like(z);dz[i]=eps*directions[i]
                    numerical=(energy(run,x,z+dz)-energy(run,x,z-dz))/(2*eps)
                    e=abs(numerical-target)/max(abs(numerical)+abs(target),1e-30)
                    check(f'{N}_H_coordinate_{i}_{eps}',e,1e-4)
                    details.append(dict(coordinate=i,increment=eps,expected=target,numerical=numerical,error=e))
            rows.append(dict(nodes=N,variations=details))
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
    result=dict(protocol=__doc__,producer_sha256=sha(__file__),dependencies={str(Path(p)):sha(p) for p in (initial.__file__,exact.__file__,linear.__file__)},
        checks=checks,rows=rows,error=error,all_controls_passed=error is None and len(rows)==2 and all(c['passed'] for c in checks),elapsed_seconds=time.monotonic()-t0)
    with OUT.open('x') as out:json.dump(result,out,indent=2,allow_nan=False)
    print(json.dumps(dict(checks=checks,error=error,all_pass=result['all_controls_passed'],sha256=sha(OUT)),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
