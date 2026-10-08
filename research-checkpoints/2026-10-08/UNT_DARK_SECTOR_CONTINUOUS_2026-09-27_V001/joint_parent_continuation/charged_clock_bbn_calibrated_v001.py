"""Fixed new calibration in SHARED_GRAVITY_NORMALIZATION_RESULT_V001.md.
No point search or changed numerical tolerances. Old failures preserved.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time
import numpy as np
import charged_clock_response_v001 as model
import charged_clock_transfer_band_v002 as solver

BASE=Path(__file__).resolve().parent
OUTPUT=BASE/'CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json'
PROTOCOL=BASE/'SHARED_GRAVITY_NORMALIZATION_RESULT_V001.md'


def main():
    started=time.monotonic()
    model.KB=.02
    model.C=2-model.KB
    rG=.98
    model.LAMBDA_S=rG/(1-model.KB/2-rG)
    model.OB=.05*rG
    model.OC=1-model.OA-model.OB
    model.D0=model.calibrated_charge()
    rows=[]
    for k in (.01,.03,.1,.3,1.):
        model.WAVENUMBER=k*model.C_KMS/model.H0_KMS_MPC
        inv=1/model.WAVENUMBER**2
        model.SCALE=np.array([inv,1.,inv,1.,inv,inv,inv])
        algebra=solver.check_metric_derivative()
        history={n:solver.integrate(n) for n in (512,1024,2048)}
        ref1024=model.integrate(1024,dust=True)
        ref2048=model.integrate(2048,dust=True)
        conv=model.convergence(history[1024],history[2048])
        refconv=model.convergence(ref1024,ref2048)
        dg=model.diagnostics(history[2048])
        raw=history[2048]*model.SCALE[None,:,None]
        ref=ref2048*model.SCALE[None,:5,None]
        quads=np.zeros((65,2))
        for i,x in enumerate(np.linspace(model.X0,0,65)):
            b=model.background(float(x)); kp=model.WAVENUMBER**2/b['a']**2
            yy=raw[i,:,6:]; rate=np.array(dg['series']['actual_rate_fraction'][i])
            quads[i]=np.maximum(abs(.5*yy[0]**2-yy[0]*rate),abs(kp*(.5*yy[6]**2+yy[6]*yy[4])))/dg['series']['rate_margin_fraction'][i]
        comps=[]
        for j,label in enumerate(('baryon_isocurvature','adiabatic_development')):
            phi,vb=raw[-1,0,j+6],raw[-1,2,j+6]
            h=model.background(0.)['h']
            num,den=-2*model.WAVENUMBER**2*phi/3,-model.WAVENUMBER**2*vb/h
            rnum,rden=-2*model.WAVENUMBER**2*ref[-1,0,j]/3,-model.WAVENUMBER**2*ref[-1,2,j]
            comps.append(dict(preparation=label,density_ratio=float(raw[-1,1,j+6]/ref[-1,1,j]),
                              potential_ratio=float(phi/ref[-1,0,j]),velocity_ratio=float(den/rden),
                              E_theory=float(num/den) if den else None,E_reference=float(rnum/rden),
                              E_ratio=float((num/den)/(rnum/rden)) if den else None,
                              signed_E_numerator=float(num),signed_velocity_convergence=float(den),
                              sampled_quadratic_kinematic_rate_margin=float(np.max(quads[:,j]))))
        controls=dict(metric_identity=algebra<=1e-10,trajectory=conv['max_normalized']<=1e-4,
                      comparator=refconv['max_normalized']<=1e-4,constraint=dg['max_normalized_constraint']<=1e-6)
        row=dict(k_Mpc_inverse=k,K=model.WAVENUMBER,comparisons=comps,controls=controls,
                 all_numerical_controls_passed=all(controls.values()),metric_identity_error=algebra,
                 convergence_512_1024=model.convergence(history[512],history[1024]),
                 convergence_1024_2048=conv,comparator_convergence=refconv,diagnostics=dg,
                 trajectory_2048_scaled=history[2048].tolist(),state_scales=model.SCALE.tolist(),
                 comparator_2048_scaled=ref2048.tolist())
        rows.append(row)
        print(json.dumps({key:row[key] for key in ('k_Mpc_inverse','all_numerical_controls_passed','comparisons')}),flush=True)
    result=dict(protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependencies_sha256={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in
                                     ('charged_clock_response_v001.py','charged_clock_transfer_band_v002.py','bounded_clock_shared_prediction_v001.py')},
                adopted=dict(KB=model.KB,lambda_s=model.LAMBDA_S,rG=rG,eps=model.EPS,Q0_over_H0=model.Q0,
                             omega_A=model.OA,omega_b_cos=model.OB,omega_clock_excess=model.OC,d0=model.D0,
                             baryon_GN_normalization=.05,a0=model.A0,H0_km_s_Mpc=model.H0_KMS_MPC),
                scope='Transparent calibration plus fixed prediction; no nuclear likelihood or projected observed lensing/growth score.',
                rows=rows,all_numerical_controls_passed=all(r['all_numerical_controls_passed'] for r in rows),
                elapsed_seconds=time.monotonic()-started,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({key:result[key] for key in ('all_numerical_controls_passed','elapsed_seconds','peak_RSS_bytes')}))
    if not result['all_numerical_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
