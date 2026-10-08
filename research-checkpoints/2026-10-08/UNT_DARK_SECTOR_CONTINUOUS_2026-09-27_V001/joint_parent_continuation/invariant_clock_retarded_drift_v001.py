"""Reuse completed linear transfers to test instantaneous stationarity.

NO evolution, new fit or compact-source solution. Turn each saved Fourier
mode into its exactly equivalent linear spherical j0/j1 mode. At fixed
background physical R=1/K, examine all saved epochs a>=.5, all previously
specified widths/k and BOTH preparations. This is a mode diagnostic, not
a localized/supported galaxy or a reconstruction of its exterior kernel.

Use Newtonian slicing and retain the metric-volume correction:
delta_m=m(pc-v-3H theta), Phi=Psi=-fb-H theta,
Ccharge=delta_m-3m Psi=m(pc-v+3fb).
Ccharge_dot+3H Ccharge+div J=0 holds exactly at linear order.
The zero-excess-flux approximation concerns F=J+HR Ccharge for this
coordinate-volume charge, not the saved baryon-proper-time pc-v readout.
Z has zero background, so its first-order fixed-R drift is gauge invariant.

Report |F|/(|J|+|HR Ccharge|) and the normalized fixed-R Z/charge drifts.
There is NO post-hoc scientific pass threshold: zero is the stationary
hypothesis, and ratios measure the cost of dropping terms. Freeze numerical
qualification now: final and late-window diagnostic differences between
4096/8192 histories <=1e-4 absolute; normalized algebraic charge continuity
defect <=1e-9. Failed derivative qualification stays failed; do not rerun
the original science automatically. A mode-level failure of stationarity
is not a no-go for all source histories or all locally stationary galaxies.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
import invariant_clock_transfer_v001 as core
import invariant_clock_depth_growth_v001 as depth

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_RETARDED_DRIFT_V001_RESULT.json'
NAMES=('INVARIANT_CLOCK_TRANSFER_V002_RESULT.json',
       'INVARIANT_CLOCK_SHORT_SCALE_V001_RESULT.json',
       'INVARIANT_CLOCK_DEPTH_GROWTH_V001_RESULT.json')


def safe_ratio(num,den):
    return np.abs(num)/np.maximum(den,1e-30)


def diagnose(m,K,history):
    records=[]
    for snap in history['snapshots']:
        a=snap['a']
        if a<.5:continue
        x=math.log(a);_,s,Q,n,Kfun,H,hx,qr=m.bg(x)
        y=np.array(snap['state']);A,T=core.matrix(m,x,K);dy=A@y
        theta=T[2]@y;kap=K/a;eta=m.C/m.KB;mu=n/Q
        fb,v,phase,sigma,Z,pc,dw=y
        p=-kap*phase+Q*sigma
        D=eta*(Z-2*p)
        wN=-kap*(phase+Q*theta)
        J=D-mu*wN
        Phi=-fb-H*theta
        delta=n*(pc-v-3*H*theta)
        charge=n*(pc-v+3*fb)
        charge_x=n*(dy[5]-dy[1]+3*dy[0])-3*charge
        residual=charge_x+3*charge+kap*J/H
        residual_scale=np.abs(charge_x)+3*np.abs(charge)+np.abs(kap*J/H)
        u=1/a;R=1/K
        j0=math.sin(u)/u;j1=math.sin(u)/u**2-math.cos(u)/u
        j1p=j0-2*j1/u
        jr=J*j1;adv=H*R*charge*j0;flux=jr+adv
        zdot=H*(dy[4]*j1-u*Z*j1p)
        zscale=np.abs(Q*D*j1)+2*H*np.abs(Z*j1)+H*np.abs(u*Z*j1p)
        cdot=H*(charge_x*j0+u*charge*j1)
        cscale=3*H*np.abs(charge*j0)+np.abs(kap*J*j0)+H*np.abs(u*charge*j1)
        diag=np.array([safe_ratio(flux,np.abs(jr)+np.abs(adv)),
                       safe_ratio(zdot,zscale),safe_ratio(cdot,cscale)])
        records.append(dict(a=a,u=u,diagnostics=diag.tolist(),
            continuity_normalized_defect=safe_ratio(residual,residual_scale).tolist(),
            Phi=Phi.tolist(),delta_m_Newtonian=delta.tolist(),
            coordinate_volume_charge=charge.tolist(),current=J.tolist(),
            fixed_radius_flux=flux.tolist(),fixed_radius_Z_dot=zdot.tolist(),
            fixed_radius_charge_dot=cdot.tolist()))
    return dict(steps=history['steps'],records=records)


def main():
    saved=json.loads(core.base.SOURCE.read_text())
    data={name:json.loads((BASE/name).read_text()) for name in NAMES}
    if not all(d['all_controls_passed'] for d in data.values()):
        raise ValueError('an inherited receipt is unqualified')
    small=data[NAMES[0]];short=data[NAMES[1]];wide=data[NAMES[2]]
    cases=[dict(eps=1e-6,k_Mpc_inverse=.01,histories=
        next(r for r in small['rows'] if r['Q0_over_H0']==100)['histories']),
        dict(eps=1e-6,k_Mpc_inverse=1.,histories=short['histories'])]
    cases.extend({k:r[k] for k in ('eps','k_Mpc_inverse','histories')} for r in wide['rows'])
    models={eps:depth.model(saved,eps)[0] for eps in (1e-6,6e-6)}
    rows=[]
    for case in cases:
        m=models[case['eps']];K=case['k_Mpc_inverse']*299792.458/m.p['H0_km_s_Mpc']
        hist=[diagnose(m,K,h) for h in case['histories'][-2:]]
        aa=np.array([s['diagnostics'] for s in hist[0]['records']])
        bb=np.array([s['diagnostics'] for s in hist[1]['records']])
        err=float(np.max(abs(aa-bb)))
        defect=max(max(r['continuity_normalized_defect']) for h in hist for r in h['records'])
        checks=dict(diagnostic_refinement=err<=1e-4,charge_identity=defect<=1e-9)
        row=dict(eps=case['eps'],k_Mpc_inverse=case['k_Mpc_inverse'],
            R_at_present_Mpc=1/case['k_Mpc_inverse'],histories=hist,
            diagnostic_absolute_error=err,maximum_continuity_defect=defect,
            final_diagnostics=hist[-1]['records'][-1]['diagnostics'],
            controls={k:bool(v) for k,v in checks.items()},all_controls_passed=bool(all(checks.values())))
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='histories'}),flush=True)
    deps=('invariant_clock_transfer_v001.py','invariant_clock_depth_growth_v001.py',
          'invariant_clock_short_scale_v001.py','plane_canonical_evolution_v001.py',
          'charged_clock_response_v001.py','bounded_clock_shared_prediction_v001.py')
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in NAMES},
        background_input_sha256=hashlib.sha256(core.base.SOURCE.read_bytes()).hexdigest(),
        dependencies_sha256={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in deps},
        diagnostic_order=['excess_flux_fraction','Z_stationarity_fraction','charge_stationarity_fraction'],
        preparation_order=['baryon_isocurvature','adiabatic_development'],rows=rows,
        all_controls_passed=bool(all(r['all_controls_passed'] for r in rows)))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
