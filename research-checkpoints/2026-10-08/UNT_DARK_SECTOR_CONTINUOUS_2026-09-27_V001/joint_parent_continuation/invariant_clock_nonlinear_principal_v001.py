"""Coupled local longitudinal principal audit of existing K(X)+J+compression.

Not a trajectory or galaxy fit. Two independent lapse/shift reductions
give the stated principal polynomial. Evaluate on qualified exact initial
fields and on explicitly prescribed frozen-epoch constitutive probes.
Keep aether-frame q_U distinct from coordinate q. Include K(X) tilt, not
just positive J. Ordinary dust's advected/zero-speed principal sector and
all finite-k/source/Jeans terms are outside this strict local symbol.

Frozen gates BEFORE execution: polynomial normalized residual1e-10;
p=0 existing quadratic roots1e-10; q_U frame identity1e-12; positive-energy
certified states real roots1e-10; independent K Hessian boost identity1e-12;
jt/j in[1,2] up to1e-12; certificate-boundary equation1e-12. These are
arithmetic checks, not observational criteria. No coefficient is fitted.
mu_eff=0 marks only the sufficient positive-energy certificate boundary,
not necessarily hyperbolicity loss. Report complete roots beyond it.
"""
from pathlib import Path
import json,math,time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial
import invariant_clock_periodic_reduced_v003 as reduced

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_PERIODIC_REDUCED_COMPONENTS_V003_RESULT.json'
EXPECTED='ec7d78567d50cf486698ea1e57aa17869ce84cd09c29f53971f36ebf3bf6e8ab'
OUT=ROOT/'INVARIANT_CLOCK_NONLINEAR_PRINCIPAL_V001_RESULT.json'
sha=initial.sha

def clean(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    raise TypeError(type(v).__name__)

def coefficients(model,X,m,d,p):
    mu=m/X;q=math.hypot(X,p);C=model.C;eta=C/model.KB;B=406.
    jt=model.lam*abs(p)*(p*p+2*model.bs**2)/(p*p+model.bs**2)**1.5
    j=model.lam*abs(p)/math.hypot(p,model.bs)
    tilt=(d-mu)*p*p/(X*X)
    a=d+tilt;b=(d-mu)*q*p/(X*X);me=mu+C*jt-tilt
    polynomial=np.array([a*B,2*b*B,-(2*eta*a+(2*eta+me)*B),-4*eta*b,2*eta*me])
    roots=np.roots(polynomial)
    residual=max(float(abs(np.polyval(polynomial,v))/max(np.polyval(abs(polynomial),abs(v)),1e-30)) for v in roots)
    # Independent Lorentz boost of the K-only quadratic form.
    boost=np.array([[q/X,-p/X],[-p/X,q/X]])
    KH=boost.T@np.diag([d,-mu])@boost
    direct=np.array([[a,-b],[-b,-mu+tilt]])
    boost_error=float(np.max(abs(KH-direct))/max(np.max(abs(direct)),1e-30))
    G=np.array([[2*eta+me,2*eta],[2*eta,2*eta]])
    white=G/np.sqrt(np.outer([a,B],[a,B]))
    return dict(X=X,p=p,q_aether=q,mu=mu,d=d,a=a,b=b,B=B,eta=eta,j=j,jt=jt,
        Cj_over_mu=C*j/mu,Cjt_over_mu=C*jt/mu,tilt_penalty=tilt,
        tilt_fraction=tilt/(mu+C*jt),mu_eff=me,
        positive_energy_certificate=bool(a>0 and B>0 and me>0),
        gradient_whitened_eigenvalues=np.linalg.eigvalsh(white),
        characteristic_speeds=[dict(real=float(v.real),imag=float(v.imag)) for v in sorted(roots,key=lambda r:r.real)],
        polynomial=polynomial,polynomial_residual=residual,
        boost_identity_error=boost_error,maximum_imaginary_speed=float(np.max(abs(roots.imag))))

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed qualified initial data')
    source=json.loads(SOURCE.read_text())
    if not source['all_controls_passed']:raise ValueError('unqualified initial components')
    model,parent=initial.load();checks=[];local=[];probes=[];error=None;t0=time.monotonic()
    def check(name,e,gate):checks.append(dict(name=name,error=float(e),gate=gate,passed=bool(e<=gate)))
    try:
        for row in source['rows']:
            run=reduced.Reduced(model,row['nodes'],initial.linear.Assembly(model).k)
            rec=run.reconstruct(row['x'],np.array(row['chart']));g=rec['fields']
            local_rows=[coefficients(model,*map(float,(g['X'][i],g['m'][i],g['d'][i],g['p'][i]))) for i in range(run.n)]
            qu=g['c']*g['q']+g['sigma']*g['w']
            check(f'{run.n}_aether_frame',np.max(abs(qu-np.hypot(g['X'],g['p']))/abs(qu)),1e-12)
            local.append(dict(nodes=run.n,x=row['x'],a=g['abar'],points=local_rows,
                largest_tilt_fraction=max(r['tilt_fraction'] for r in local_rows),
                largest_Cj_over_mu=max(r['Cj_over_mu'] for r in local_rows),
                all_positive_energy=all(r['positive_energy_certificate'] for r in local_rows)))
        for epoch in (54,55,56,57):
            x=math.log(parent['histories'][-1]['snapshots'][epoch]['a'])
            bg=run.core.background(x);X=bg['Qbar'];m=bg['mbar'];d=bg['dbar'];mu=m/X
            samples=[]
            for ratio in (0.,.01,.1,1.,10.,100.,1000.):
                wanted=ratio*mu/model.C
                if wanted>=model.lam:raise ValueError('probe outside bounded J range')
                p=model.bs*wanted/math.sqrt(model.lam**2-wanted**2)
                samples.append(coefficients(model,X,m,d,p))
            # Locate the first sufficient-energy boundary by deterministic
            # positive bracket and bisection; this is no model calibration.
            lo=0.;hi=X
            while coefficients(model,X,m,d,hi)['mu_eff']>0:hi*=2
            for _ in range(80):
                mid=(lo+hi)/2
                if coefficients(model,X,m,d,mid)['mu_eff']>0:lo=mid
                else:hi=mid
            boundary=coefficients(model,X,m,d,(lo+hi)/2)
            check(f'epoch{epoch}_certificate_boundary',abs(boundary['mu_eff'])/(mu+model.C*boundary['jt']),1e-12)
            beyond=[coefficients(model,X,m,d,factor*(lo+hi)/2) for factor in (.5,2.)]
            zero=samples[0];eta=zero['eta'];B=zero['B'];bb=B*(2*eta+mu)+2*eta*d
            disc=math.sqrt(bb*bb-8*d*B*eta*mu);fast=(bb+disc)/(2*d*B);slow=(2*eta*mu)/(d*B*fast)
            expected=np.sort([-math.sqrt(fast),-math.sqrt(slow),math.sqrt(slow),math.sqrt(fast)])
            actual=np.sort([r['real'] for r in zero['characteristic_speeds']])
            check(f'epoch{epoch}_aligned_quadratic',np.max(abs(actual-expected)/np.maximum(abs(expected),1e-30)),1e-10)
            probes.append(dict(epoch=epoch,a=bg['abar'],source='prescribed local constitutive points, NOT evolved states',samples=samples,
                sufficient_energy_boundary=boundary,boundary_side_probes=beyond))
        all_points=[p for r in local for p in r['points']]+[p for r in probes for p in r['samples']+r['boundary_side_probes']]
        check('polynomial_residual',max(r['polynomial_residual'] for r in all_points),1e-10)
        check('K_Hessian_boost_identity',max(r['boost_identity_error'] for r in all_points),1e-12)
        certified=[r for r in all_points if r['positive_energy_certificate']]
        check('certified_real_characteristics',max(r['maximum_imaginary_speed'] for r in certified),1e-10)
        ratios=[r['jt']/r['j'] for r in all_points if r['j']>0]
        check('jt_j_interval',max(0.,1-min(ratios),max(ratios)-2),1e-12)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc),diagnostics=getattr(exc,'diagnostics',None))
    result=dict(protocol=__doc__,producer_sha256=sha(__file__),source_sha256=EXPECTED,
        dependencies={str(Path(p)):sha(p) for p in (reduced.__file__,initial.__file__)},
        cTheta=.01,local_initial_states=local,constitutive_probes=probes,checks=checks,error=error,
        all_controls_passed=error is None and all(c['passed'] for c in checks),
        nonlinear_saturation_established=False,full_3D_hyperbolicity=False,
        galaxy_prediction=False,observational_superiority=False,elapsed_seconds=time.monotonic()-t0)
    with OUT.open('x') as out:json.dump(result,out,indent=2,allow_nan=False,default=clean)
    print(json.dumps(dict(checks=checks,error=error,all_pass=result['all_controls_passed'],sha256=sha(OUT),
        initial_summary=[{k:v for k,v in r.items() if k!='points'} for r in local],
        ratio_one=[r['samples'][3] for r in probes]),indent=2,default=clean),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
