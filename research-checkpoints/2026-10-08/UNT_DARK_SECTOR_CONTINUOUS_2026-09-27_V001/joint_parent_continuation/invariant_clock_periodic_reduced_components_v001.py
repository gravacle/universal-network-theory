"""Independent reduced-chart qualification before any reduced trajectory.

Same componentV004 exact initial states,17/33 nodes, no physical changes.
Prospective gates: homogeneous RHS1e-10; initial constraints same1e-9
background/1e-4 perturbation; roundtrip physical-state1e-4; retained-field
RHS1e-12; eliminated metric-momentum tangent1e-4 at two increments1e-6,
5e-7; scalar/dust totals1e-12; reduced matrix/full RHS tangent1e-4 at
two amplitudes1e-5,5e-6. Record reconstruction Jacobian conditioning and
branch variables, no physical conclusion from chart failure. Exclusive
receipt, no iteration/filter/projection or criterion adjustment afterward.
"""
from pathlib import Path
import json,time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial
import invariant_clock_periodic_reduced_v001 as reduced

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_PERIODIC_COMPONENTS_V004_RESULT.json'
EXPECTED='f4bc4d6c9b5ace57b9d6848fd0b27a299e429eb3a5c4c1f8d3f5b2c99295e831'
OUT=ROOT/'INVARIANT_CLOCK_PERIODIC_REDUCED_COMPONENTS_V001_RESULT.json'
sha=initial.sha

def clean(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v).__name__)

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed exact initial receipt')
    saved=json.loads(SOURCE.read_text());model,parent=initial.load();checks=[];rows=[];error=None;t0=time.monotonic()
    def check(name,e,gate):checks.append(dict(name=name,error=float(e),gate=gate,passed=bool(e<=gate)))
    try:
        for row in saved['rows']:
            N=row['nodes'];x=row['x'];z=np.array(row['state']);piT=np.array(row['piT'])
            run=reduced.Reduced(model,N,initial.linear.Assembly(model).k)
            chart=run.from_full(x,z,piT)
            f,recon=run.rhs(x,chart,return_fields=True)
            full=recon['z'];g=recon['fields'];cc=recon['constraints'];bg=run.core.background(x)
            actual=run.core.rhs(x,full)
            error_by_field=np.max(abs(full-z),axis=1)/np.maximum(np.max(abs(z),axis=1),1e-30)
            check(f'{N}_full_roundtrip',np.max(error_by_field),1e-4)
            indices=[0,1,2,3,6,7]
            check(f'{N}_retained_RHS',np.max(abs(f[indices]-actual[indices]))/max(np.max(abs(actual[indices])),1e-30),1e-12)
            check(f'{N}_homogeneous_RHS',np.max(abs(run.rhs(x,np.zeros_like(chart),return_fields=False))),1e-10)
            hbg=6*bg['Vbar']*bg['H']**2
            hp=max(np.max(abs(piT-bg['pi_T_bar'])),np.max(abs(run.core.dx(cc['boundary']))),1e-30)
            dp=max(np.max(np.sum(abs(cc['momentum_terms']),axis=0)),1e-30)
            check(f'{N}_Hamiltonian_background',np.max(abs(cc['Hamiltonian']))/hbg,1e-9)
            check(f'{N}_Hamiltonian_perturbation',np.max(abs(cc['Hamiltonian']))/hp,1e-4)
            check(f'{N}_momentum',np.max(abs(cc['momentum']))/dp,1e-4)
            check(f'{N}_mean_scalar_RHS',abs(np.mean(f[7]))/max(np.max(abs(f[7])),1e-30),1e-12)
            check(f'{N}_fixed_dust_RHS',np.max(abs(f[5])),1e-12)
            tangent_rows=[]
            for eps in (1e-6,5e-7):
                plus=run.reconstruct(x+eps,chart+eps*f)['z']
                minus=run.reconstruct(x-eps,chart-eps*f)['z']
                deriv=(plus[4:6]-minus[4:6])/(2*eps)
                errors=np.max(abs(deriv-actual[4:6]),axis=1)/np.maximum(np.max(abs(actual[4:6]),axis=1),1e-30)
                check(f'{N}_eliminated_momentum_{eps}',np.max(errors),1e-4)
                tangent_rows.append(dict(increment=eps,error_by_momentum=errors,derivative=deriv,original_rhs=actual[4:6]))
            scale=np.array([1.,1/run.core.k**2,1/run.core.k,model.Q0/run.core.k**2,1.,bg['pi_T_bar'],1/run.core.k,run.core.pi_phi_bar])
            matrices=run.matrices(x);ph=2*np.pi*np.arange(N)/N
            direction=np.array([.7*np.cos(ph),.3*np.cos(ph),.2*np.sin(ph),.5*np.cos(ph),np.zeros(N),.4*np.cos(ph),-.3*np.sin(ph),.6*np.cos(ph)])*scale[:,None]
            for eps in (1e-5,5e-6):
                act=(run.rhs(x,eps*direction,return_fields=False)-run.rhs(x,-eps*direction,return_fields=False))/2
                coeff=np.fft.rfft(eps*direction,axis=1).T/N
                predicted=np.fft.irfft((matrices@coeff[...,None])[...,0].T*N,n=N,axis=1)
                norms=np.maximum(np.max(abs(predicted),axis=1),1e-30)
                # Row4 starts quadratically at nonzero mode and row5 is
                # identically fixed; qualify their exact identities separately.
                ee=np.max(np.max(abs(act[indices]-predicted[indices]),axis=1)/norms[indices])
                check(f'{N}_reduced_tangent_{eps}',ee,1e-4)
            rows.append(dict(nodes=N,x=x,chart=chart,full=full,piT=piT,roundtrip_errors=error_by_field,
                eliminated_momentum_tangents=tangent_rows,reconstruction_history=recon.get('history'),
                min_bdot=float(np.min(g['bdot'])),min_s=float(np.min(g['s'])),min_schur_fraction=float(np.min(g['schur']/g['d']))))
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc),diagnostics=getattr(exc,'diagnostics',None))
    result=dict(protocol=__doc__,producer_sha256=sha(__file__),source_sha256=EXPECTED,
        dependencies={str(Path(p)):sha(p) for p in (reduced.__file__,initial.__file__)},checks=checks,rows=rows,error=error,
        all_controls_passed=error is None and len(rows)==2 and all(c['passed'] for c in checks),elapsed_seconds=time.monotonic()-t0,
        physical_saturation_established=False,observational_superiority=False)
    with OUT.open('x') as out:json.dump(result,out,indent=2,allow_nan=False,default=clean)
    print(json.dumps(dict(checks=checks,error=error,all_pass=result['all_controls_passed'],sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
