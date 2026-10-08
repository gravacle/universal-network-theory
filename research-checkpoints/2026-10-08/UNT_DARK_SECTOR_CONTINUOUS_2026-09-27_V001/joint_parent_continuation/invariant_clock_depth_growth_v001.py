"""One prospective shared-clock depth/growth trade-off, not a best fit.

The inherited eps=1e-6 cap has a necessary regular stationary center-to-
matched-outer lapse headroom Dmax=ln(Xcap/Xbar). It is independent of Q0.
For phi=omega t+phi_r, w(center)=w(outer)=0 gives Nc/No=Xouter/Xcenter;
therefore -ln(Nc/No)<Dmax. This is conditional on static state/matching,
not an exclusion of a time-dependent or differently prepared UNT universe.

Investigate ONE existing width freedom eps=6e-6, chosen before its growth
output as a nearby width exceeding the order2.1e-6 photospheric depth.
It is not adopted or optimized and does not demonstrate a whole stellar
interior, whose depth is larger, nor a galaxy solution. Retain Q0/H0=100,
KB,J,H0,a0 and today's .7/.049/.251 energy budgets. Recompute conserved
charge from the SAME .251 present energy constraint; count it as inherited
calibration, not new native formation. Changing eps changes H(a) slightly.

Primary solar source arxiv:2009.10558: line-core estimate639+-14m/s and
3D-corrected weak-line estimate638+-6m/s. Report both as lapse-difference
benchmarks under adopted minimal matter/photon coupling, not raw scalar
clock measurements, nor two independent precision likelihoods. Spectral
convective modeling is part of the source's inference. Central stellar
depth exceeds surface depth only under the stated attractive regular
spherical geometry; outer cosmic matching is an additional assumption.

New rows eps1e-6,k=.1/Mpc; eps6e-6,k=.1 and1/Mpc, same two development
preparations. Reuse (do not rerun) the completed eps1e-6,k1 receipt.
2048/4096/8192 Gauss steps per new row, unchanged state/error floor1e-30
and1e-4 refinement gates, same pressureless reference with today's budget.
Check new present energy normalization to1e-12 and propagation identities
to1e-12. No observed spectrum likelihood, all-mode stability, local GN
recalibration, native derivation, Stage completion or superiority follows.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_transfer_v001 as core
from invariant_clock_short_scale_v001 import scalar

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_DEPTH_GROWTH_V001_RESULT.json'
OLD=BASE/'INVARIANT_CLOCK_SHORT_SCALE_V001_RESULT.json'


def model(saved,eps):
    ss=json.loads(json.dumps(saved));p=ss['inherited'];p['eps']=eps;p['Q0_over_H0']=100.
    m=core.base.Model(ss,1)
    target=3*p['omega_clock_excess'];s=target/(m.Q0*m.mpref)
    for _ in range(8):
        X,n,d,K,dm,qr=m.constitutive(s)
        excess=X*n-(K+3*m.OA)
        s-=(excess-target)/(X*dm)
    X,n,d,K,dm,qr=m.constitutive(s)
    p['d0']=n*m.Q0/(3*m.OA);m=core.base.Model(ss,1)
    a,s,X,n,K,H,hx,qr=m.bg(0.);d=m.constitutive(s)[2]
    zeta=n/(m.C*X);cad=n/(X*d);cL=(2*m.C/m.KB+n/X)/d;gap=m.C/m.KB*X*X
    depth=.5*math.log1p(eps/(1+s)/(1+eps*s/(1+s)))
    identity=abs(zeta*cL-cad*(2/m.KB+zeta))/(cad*(2/m.KB+zeta))
    diag=dict(eps=eps,d0=p['d0'],s_present=s,maximum_log_lapse_depth=depth,
        equivalent_redshift_velocity_m_s=299792458*math.expm1(depth),
        c_clock_squared=cad,c_long_squared=cL,zeta=zeta,
        material_crossover_Mpc_inverse=math.sqrt(gap/cL)*p['H0_km_s_Mpc']/299792.458,
        high_k_lower_frequency_squared=n*X/(2+m.KB*zeta),cross_identity_error=identity,
        present_energy_error=abs((X*n-K)/3-(p['omega_A']+p['omega_clock_excess'])),
        H_by_a={str(a):m.bg(math.log(a))[5] for a in (.01,.1,1.)})
    return m,diag


def main():
    beg=time.monotonic();saved=json.loads(core.base.SOURCE.read_text());old=json.loads(OLD.read_text())
    if not old['all_controls_passed'] or old['Q0_over_H0']!=100 or old['k_Mpc_inverse']!=1:
        raise ValueError('completed reference receipt mismatch')
    rows=[];models={};params=[];references={1.:old['pressureless_reference']}
    for eps in (1e-6,6e-6):
        m,diag=model(saved,eps);models[eps]=m;params.append(diag)
    for eps,k in ((1e-6,.1),(6e-6,.1),(6e-6,1.)):
        m=models[eps];K=k*299792.458/m.p['H0_km_s_Mpc']
        hist=[core.integrate(m,K,n) for n in (2048,4096,8192)]
        if k not in references:references[k]=[core.reference(m,K,n) for n in (2048,4096)]
        refs=references[k]
        r0=np.array(refs[0]['snapshots']);r1=np.array(refs[1]['snapshots'])
        re=float(np.max(np.max(abs(r0-r1),axis=0)/np.maximum(np.max(abs(r1),axis=0),1e-30)))
        comps=[]
        for i in (32,48,64):
            ob=np.array(hist[-1]['snapshots'][i]['observables']);rat=ob[:3]/r1[i,:3]
            comps.append(dict(a=hist[-1]['snapshots'][i]['a'],ratios=rat.tolist(),
                potential_over_velocity_ratio=(rat[0]/rat[2]).tolist()))
        row=dict(eps=eps,k_Mpc_inverse=k,histories=hist,reference=refs,
            fine_state_error=core.error(hist[1],hist[2],'state'),
            fine_observable_error=core.error(hist[1],hist[2],'observables'),reference_error=re,
            comparisons=comps)
        rows.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ('histories','reference')},default=scalar),flush=True)
    solar=[dict(method='strong_line_core',velocity_m_s=639.,sigma_m_s=14.),
           dict(method='weak_line_3D_corrected',velocity_m_s=638.,sigma_m_s=6.)]
    for s in solar:s['log_lapse_depth']=math.log1p(s['velocity_m_s']/299792458)
    checks=dict(time_refinement=all(r['fine_state_error']<=1e-4 and r['fine_observable_error']<=1e-4 for r in rows),
        reference_refinement=all(r['reference_error']<=1e-4 for r in rows),
        normalization=all(p['present_energy_error']<=1e-12 for p in params),
        cross_identity=all(p['cross_identity_error']<=1e-12 for p in params))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (core.base.SOURCE,OLD)},
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in
            ('invariant_clock_transfer_v001.py','invariant_clock_short_scale_v001.py','plane_canonical_evolution_v001.py','charged_clock_response_v001.py','bounded_clock_shared_prediction_v001.py')},
        parameter_diagnostics=params,solar_benchmark_source='https://arxiv.org/abs/2009.10558',solar_benchmarks=solar,
        rows=rows,reused_eps1e_minus6_k1_comparisons=old['comparisons'],controls={k:bool(v) for k,v in checks.items()},
        all_controls_passed=bool(all(checks.values())),elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,default=scalar,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(parameters=params,controls=result['controls'],elapsed_seconds=result['elapsed_seconds']),default=scalar,indent=2),flush=True)


if __name__=='__main__':main()
