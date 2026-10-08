"""Saved-only limitations audit of the FAILED semilinear saturation test.

No new trajectory, fit, tolerance relaxation or physics qualification.
Add the independently identified next-order current terms, compare3N/6N
quadrature of the nonpolynomial flux, and expose early prefix errors rather
than quote only its stable fundamental. All asymptotic ratios remain partial
ESTIMATES, not complete bounds on the original action.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
import invariant_clock_semilinear_assembly_v001 as old

ROOT=Path(__file__).resolve().parent
SOURCE=old.OUT
OUT=ROOT/'INVARIANT_CLOCK_SEMILINEAR_SAVED_AUDIT_V001_RESULT.json'
EXPECTED='0cabe0b6636312b7bf7b4c665912bc033552c8f08cde5384d0c842efc7f928ca'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed failed receipt')
    src=json.loads(SOURCE.read_text())
    if sha(Path(old.__file__))!=src['producer_sha256']:raise ValueError('changed producer')
    saved=json.loads(old.linear.linear.old.base.SOURCE.read_text());saved['inherited']=src['fixed']
    model=old.linear.linear.old.base.Model(saved,1);reports=[]
    for row in src['rows'][-2:]:
        N=row['nodes'];run=old.Periodic(model,N);records=[]
        for i,snap in enumerate(row['snapshots']):
            a,Q,m,d,H,Hd,Hdx,rb,k2=run.bg(math.log(snap['a']));wave=np.sqrt(k2)*run.n
            dm,phi,alpha,Z,db,theta=np.array(snap['state'])
            ff=np.fft.rfft(np.array([dm,phi,alpha,Z,db,theta]),axis=1)/N
            df,pf,af,zf,bf,tf=ff;rel=pf+Q*af;Ef=(zf-model.C*rel)/model.KB
            flux=[];details=None
            for pad in (3*N,6*N):
                g=lambda f:run.grid(f,pad)
                p=g(1j*wave*rel);w=g(1j*wave*pf);v=g(1j*wave*af);e=g(1j*wave*Ef)
                j=model.lam*abs(p)/np.sqrt(p*p+model.bs**2)
                jt=model.lam*abs(p)*(p*p+2*model.bs**2)/(p*p+model.bs**2)**1.5
                NJ=-model.C*j*p;flux.append((np.fft.rfft(NJ)/pad)[:run.M])
                if pad==6*N:
                    dmf=g(df);dx=dmf/d;D=model.C*(e-(1+j)*p);current=D-m/Q*w
                    terms=np.array([-dmf*w/Q,m*dx*w/Q**2,-model.C*(2/model.KB+jt)*v*dx,(v*v/2)*D])
                    denom=max(float(np.max(abs(current))),1e-100)
                    details=dict(additional_current_term_norms=(np.max(abs(terms),axis=1)/denom).tolist(),
                        signed_combination_ratio=float(np.max(abs(terms.sum(axis=0))))/denom,
                        sum_of_term_norms=float(np.sum(np.max(abs(terms),axis=1)))/denom)
            discrepancy=run.grid(-1j*wave*(flux[0]-flux[1]),6*N)
            source=run.grid(-1j*wave*flux[1],6*N)
            alias=float(np.max(abs(discrepancy)))/max(float(np.max(abs(source))),1e-100)
            records.append(dict(index=i,a=snap['a'],quadrature_current_divergence_relative_error=alias,
                partial_asymptotic_estimates_not_bounds=details,original_proxy_screen=snap['within_declared_asymptotic_ceiling']))
        reports.append(dict(nodes=N,records=records))
    pref={key:old.compare(src['rows'][-2],src['rows'][-1],key) for key in ('state','observables')}
    firstbad=next(i for i,s in enumerate(src['rows'][-1]['snapshots']) if not s['within_declared_asymptotic_ceiling'])
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),source_sha256=EXPECTED,reports=reports,
        original_proxy_first_fail=firstbad,early_spatial_prefix_errors={k:max(v['prefix'][:firstbad-1]) for k,v in pref.items()},
        all_spatial_prefix_errors=pref,original_numerical_test_passed=False,full_action_error_bounded=False,
        exact_next='Exact conserved-source canonical action and constrained initialization; do not promote a semilinear fundamental.')
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(early_spatial_prefix_errors=result['early_spatial_prefix_errors'],
        selected=[dict(nodes=r['nodes'],records=[r['records'][i] for i in (0,16,21,22,32)]) for r in reports],sha256=sha(OUT)),indent=2))

if __name__=='__main__':main()
