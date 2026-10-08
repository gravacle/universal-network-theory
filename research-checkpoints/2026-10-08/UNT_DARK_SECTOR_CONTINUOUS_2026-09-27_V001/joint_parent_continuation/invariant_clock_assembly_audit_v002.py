"""Qualified V004 saved-state interpretation; no new numerical evolution.

Reuse the identical algebraic decomposition and illustrative amplitudes of
the preserved failed V001 audit, now on full-phase-qualified histories.
Additional norm/Bernoulli error diagnostic d*|grad(varphi)|²/(2Q|dm|)
is an asymptotic relative scale, NOT a new accepted physical approximation.
Separate numerical qualification from finite-amplitude/primordial claims.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
import invariant_clock_compression_assembly_v001 as core
import invariant_clock_compression_assembly_v002 as methods

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V004_RESULT.json'
OUT=ROOT/'INVARIANT_CLOCK_ASSEMBLY_AUDIT_V002_RESULT.json'
EXPECTED='7ed429224a93aaef44c97dc2bdaedce5c2f3fc7b685ceb863ae99c91fc9f304b'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(SOURCE)!=EXPECTED:raise ValueError('changed qualified receipt')
    src=json.loads(SOURCE.read_text())
    if not src['all_controls_passed']:raise ValueError('unqualified phase')
    for p,dig in src['dependencies'].items():
        if sha(Path(p))!=dig:raise ValueError('changed dependency')
    saved=json.loads(core.linear.old.base.SOURCE.read_text());saved['inherited']=src['fixed']
    model=core.linear.old.base.Model(saved,1);run=core.Assembly(model)
    rows=[];checks=[];err_cur=0.;err_phi=0.;amplitudes=(1e-5,1e-9,1e-12)
    for s in src['histories'][-1]['snapshots']:
        x=math.log(s['a']);a,Q,m,d,H,Hd,Hdx,rb,k2=run.bg(x)
        dm,phi,alpha,Z,db,theta=np.array(s['state']);rel=phi+Q*alpha
        y=np.vstack((dm,rel,alpha,Z,db,theta))/run.scale[:,None]
        rhs=run.rhs(x,np.vstack((y,np.zeros(2))))[:6]*run.scale[:,None]*H
        E=(Z-model.C*rel)/model.KB;D=model.C*(E-rel)
        Jr=D-m/Q*(phi-Q*theta);Sdot=rhs[0]/m+3*H*dm/m-rhs[4];target=k2/m*Jr
        err_cur=max(err_cur,float(np.max(abs(Sdot-target)/np.maximum(abs(rhs[0]/m)+abs(3*H*dm/m)+abs(rhs[4])+abs(target),1e-100))))
        pieces=np.array([Z/2,-Q*dm/(2*k2),-rb*db/(2*k2),-3*H*(m*phi+rb*theta)/(2*k2)])
        Phi=np.array(s['observables'][0]);err_phi=max(err_phi,float(np.max(abs(pieces.sum(axis=0)-Phi)/np.maximum(np.sum(abs(pieces),axis=0),1e-100))))
        vals=np.linalg.eigvals(run.matrix(x))
        domains={}
        for amp in amplitudes:
            dom={k:(amp*np.array(v)).tolist() for k,v in s['linear_unit_seed_domain'].items()}
            p=amp*np.sqrt(k2)*abs(rel)
            dom['Cj_over_mu']=(model.C*model.lam*p/np.sqrt(p*p+model.bs**2)/(m/Q)).tolist()
            num=d*amp*k2*phi*phi/(2*Q)
            ratio=np.divide(num,abs(dm),out=np.zeros(2),where=dm!=0)
            dom['norm_correction_relative_to_charge']=ratio.tolist()
            domains[str(amp)]=dom
        rows.append(dict(a=a,background=dict(Q=Q,m=m,d=d,H=H,rho_b=rb,kphys2=k2),
            potential_pieces=pieces.tolist(),potential_piece_fractions=(pieces/Phi).tolist(),
            force_enhancement_over_bare_baryons=(Phi/pieces[2]).tolist(),
            rest_slice_clock_contrast=(dm/m+3*H*theta).tolist(),rest_slice_baryon_contrast=(db+3*H*theta).tolist(),
            relative_charge=(dm/m-db).tolist(),relative_current=Jr.tolist(),
            frozen_eigenvalues_per_log_a=[[float(v.real),float(v.imag)] for v in vals],domains=domains))
    for name,e in (('relative_current',err_cur),('metric_source_sum',err_phi)):
        checks.append(dict(name=name,error=e,gate=1e-12,passed=bool(e<=1e-12)))
    crossings=[]
    for amp in amplitudes:
        for seed in (0,1):
            for threshold in (.1,1.):
                found=None
                for i,row in enumerate(rows):
                    vals={k:v[seed] for k,v in row['domains'][str(amp)].items()}
                    if max(vals.values())>=threshold:
                        found=dict(last_below_a=rows[i-1]['a'] if i else None,first_above_a=row['a'],
                            trigger=max(vals,key=vals.get),values=vals)
                        break
                crossings.append(dict(illustrative_amplitude=amp,seed=seed,threshold=threshold,crossing=found))
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),source_sha256=EXPECTED,
        checks=checks,all_controls_passed=all(c['passed'] for c in checks),rows=rows,
        potential_piece_order=['Z_over_2','clock_density','ordinary_density','momentum'],crossings=crossings,
        full_phase_numerically_qualified=True,physical_formation=False,observational_superiority=False)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(checks=checks,crossings=crossings,
        selected_rows=[{k:v for k,v in rows[i].items() if k!='domains'} for i in (32,48,64)],sha256=sha(OUT)),indent=2),flush=True)

if __name__=='__main__':main()
