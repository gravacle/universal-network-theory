"""Chi-primary formulation equivalence and initial-slice tidal readout.
Same frozen initial17/33, exact action, and all inherited component gates.
Additional prospective controls: at fixed retained coordinates/momenta,
independent centered H_chi and pi_b_chi derivatives at steps H*1e-6 and
H*5e-7, relative1e-7; tidal proper-time directional derivative refinements
1e-6/5e-7 in log a, relative1e-4. No evolution or new state selection.
Initial tidal signal is geodesic deviation, NOT rotation, lensing, native
formation or observational evidence. The ordinary/clock/metric preparation
is inherited; all sources of tidal curvature remain included. Original
formulation is an independent comparison, not used to recover accepted chi.
"""
from pathlib import Path
import json,time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial
import invariant_clock_periodic_reduced_chi_v001 as reduced

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_PERIODIC_COMPONENTS_V004_RESULT.json'
EXPECTED='f4bc4d6c9b5ace57b9d6848fd0b27a299e429eb3a5c4c1f8d3f5b2c99295e831'
OUT=ROOT/'INVARIANT_CLOCK_PERIODIC_CHI_COMPONENTS_V001_RESULT.json'
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
            change=run.initial_pairing_change
            check(f'{N}_initial_pairing',np.max(np.max(abs(change),axis=1)/np.maximum(np.max(abs(chart),axis=1),1e-30)),1e-12)
            from invariant_clock_periodic_exact_v002 import PeriodicExact
            fft=PeriodicExact(model,N,run.core.k)
            derivative_error=0.
            ph=2*np.pi*np.arange(N)/N
            for mode in range(1,N//2+1):
                for fn in (np.cos,np.sin):
                    field=fn(mode*ph)
                    derivative_error=max(derivative_error,float(np.max(abs(run.dx(field)-fft.dx(field)))/(mode*run.core.k)))
            check(f'{N}_independent_derivative',derivative_error,1e-12)
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
            # Independent finite-difference Jacobians of the canonical constraint.
            for dh in (1e-6*g['H'],5e-7*g['H']):
                gp=run.core.fields_chi(x,full,g['delta_chi']+dh,ds_guess=g['ds'])
                gm=run.core.fields_chi(x,full,g['delta_chi']-dh,ds_guess=g['ds'])
                cp=run.core.constraints(x,gp['state'],piT,fields=gp)
                cm=run.core.constraints(x,gm['state'],piT,fields=gm)
                expected=4*g['V']*g['c']*g['Kchi']
                numeric=(gp['state'][5]-gm['state'][5])/(2*dh)
                check(f'{N}_pb_chi_{dh}',np.max(abs(numeric-expected))/np.max(abs(expected)),1e-7)
                expected=expected*g['bdot']
                numeric=(cp['Hamiltonian']-cm['Hamiltonian'])/(2*dh)
                check(f'{N}_H_chi_{dh}',np.max(abs(numeric-expected))/np.max(abs(expected)),1e-7)
            tangent_rows=[];tidal=[]

            for eps in (1e-6,5e-7):
                rp=run.reconstruct(x+eps,chart+eps*f)
                rm=run.reconstruct(x-eps,chart-eps*f)
                plus,minus=rp['z'],rm['z']
                tfields=[]
                for key in ('delta_adot','delta_bdot'):
                    # d/dt = H*d/dlogabar along the exact reduced vector field.
                    ddt=g['H']*(rp['fields'][key]-rm['fields'][key])/(2*eps)
                    tfields.append(ddt+2*g['H']*g[key]+g[key]**2)
                tidal.append(np.array(tfields))

                deriv=(plus[4:6]-minus[4:6])/(2*eps)
                errors=np.max(abs(deriv-actual[4:6]),axis=1)/np.maximum(np.max(abs(actual[4:6]),axis=1),1e-30)
                check(f'{N}_eliminated_momentum_{eps}',np.max(errors),1e-4)
                tangent_rows.append(dict(increment=eps,error_by_momentum=errors,derivative=deriv,original_rhs=actual[4:6]))
            check(f'{N}_initial_tidal_refinement',np.max(abs(tidal[1]-tidal[0]))/max(np.max(abs(tidal[1])),1e-30),1e-4)
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
            rows.append(dict(nodes=N,x=x,tidal_excess_by_increment=tidal,chart=chart,full=full,piT=piT,roundtrip_errors=error_by_field,
                initial_pairing_change=change,independent_derivative_error=derivative_error,
                eliminated_momentum_tangents=tangent_rows,reconstruction_history=recon.get('history'),reflection_remainder_component_relative=recon.get('reflection_remainder_component_relative'),
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

