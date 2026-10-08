"""Signed finite-field reconstruction of SAVED accepted modes, not a new IVP.

Freeze before execution. Keep every original constant and finite preparation.
Read the accepted V002 repair for the four original low-k rows, the other
five accepted V001 rows, and the five declared calibrated rows. Do not fit,
clip a rate, change a seed, or use a failed numerical trajectory as evidence.
For each saved time, interpret the linear metric/phase/spatial-vector fields
as one explicit finite-field ansatz and normalize the vector exactly. Compare
its signed Q to both clock boundaries. Also inspect X=-grad(phi)^2: where
the gradient is future timelike and X>Qmax^2, NO future unit vector can repair
the saved phase+metric ansatz. This is not a nonlinear solution or exclusion.

Cosine-coordinate grids of1025 and2049 include both crests and the sine peak.
A violating sampled witness is meaningful; no sampled pass proves continuous
validity. Grid-extrema agreement <=5e-4 relative to the full extrema scale;
direct-versus-cancellation-resistant identities <=2e-12 normalized to the
larger of unity and the direct Q/X value; vector normalization <=2e-12.
Zero perturbation must be exact.
All controls are numerical, never an observational or nonlinear threshold.
Keep failed controls separately. One standard small local worker, no ODEs.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time
import numpy as np
import charged_clock_response_v001 as model

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'CHARGED_CLOCK_EXACT_DOMAIN_V001_RESULT.json'
INPUTS = ('CHARGED_CLOCK_TRANSFER_BAND_V001_RESULT.json',
          'CHARGED_CLOCK_TRANSFER_BAND_V002_RESULT.json',
          'CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json')


def exact_fields(A, rate, v, w, y):
    s2 = 1-y*y
    lapse, space = 1+2*A*y, 1-2*A*y
    b = A+rate
    t = 1+b*y
    vector_part = v*v*s2/space
    root = np.sqrt((1+vector_part)/lapse)
    R = t*root
    # R^2-1, without subtracting nearly equal unit numbers.
    r2minus1 = (2*rate*y+b*b*y*y+t*t*vector_part)/lapse
    delta_R = np.empty_like(R)
    regular = abs(R+1) >= .25
    delta_R[regular] = r2minus1[regular]/(R[regular]+1)
    # If R is negative, R-1 has no near-unit cancellation.
    delta_R[~regular] = R[~regular]-1
    delta_Q = delta_R+v*w*s2/space
    delta_X = (2*rate*y+b*b*y*y)/lapse-w*w*s2/space
    direct_Q = R+v*w*s2/space
    direct_X = t*t/lapse-w*w*s2/space
    unit_error = np.max(abs(-lapse*root*root+vector_part+1))
    # The stable quotient needs R+1 nonzero; all future branch rows satisfy it.
    return delta_Q, delta_X, t, float(unit_error), direct_Q, direct_X


def inspect(row, column, grid_count):
    K = row['K']
    raw = np.asarray(row['trajectory_2048_scaled'])*np.asarray(row['state_scales'])[None,:,None]
    yy = raw[:,:,column+6]
    rates = np.asarray(row['diagnostics']['series']['actual_rate_fraction'])[:,column]
    y = np.linspace(-1.,1.,grid_count)
    summaries = []
    identity_error = unit_error = 0.
    for i,x in enumerate(np.linspace(model.X0,0.,len(yy))):
        bg = model.background(float(x))
        a, ss, q = bg['a'], bg['s'], bg['q']
        A = float(yy[i,0]); v = K/a*float(yy[i,6]); w = K/a*float(yy[i,4])
        common = dict(a=a, metric_Phi=A, vector_component=v, phase_gradient=w)
        if 2*abs(A) >= 1:
            summaries.append(dict(**common, metric_domain_valid=False))
            continue
        dq, dx, t, eu, q_direct, x_direct = exact_fields(A,float(rates[i]),v,w,y)
        identity_error = max(identity_error,float(np.max(abs(1+dq-q_direct)/np.maximum(1.,abs(q_direct)))),
                             float(np.max(abs(1+dx-x_direct)/np.maximum(1.,abs(x_direct)))))
        unit_error = max(unit_error,eu)
        low = model.EPS*ss/((1+ss)*q*(q+1))
        high = model.EPS/((1+ss)*q*(math.sqrt(1+model.EPS)+q))
        high_x = model.EPS/((1+ss)*q*q)
        future_timelike = (t>0)&(1+dx>0)
        witness = np.where(future_timelike,dx-high_x,-np.inf)
        jlo,jhi,jx = int(np.argmin(dq)),int(np.argmax(dq)),int(np.argmax(witness))
        summaries.append(dict(**common,metric_domain_valid=True,
                              min_delta_Q=float(dq[jlo]), max_delta_Q=float(dq[jhi]),
                              min_delta_X=float(np.min(dx)), max_delta_X=float(np.max(dx)),
                              Q_lower_margin_fraction=low,Q_upper_margin_fraction=high,
                              Q_lower_violation=bool(dq[jlo]<-low),
                              Q_upper_violation=bool(dq[jhi]>high),
                              min_Q_y=float(y[jlo]),max_Q_y=float(y[jhi]),
                              invariant_upper_violation=bool(witness[jx]>0),
                              invariant_witness_y=float(y[jx]),
                              invariant_witness_X_excess=float(witness[jx]) if math.isfinite(witness[jx]) else None,
                              invariant_upper_margin_fraction=high_x,
                              all_phase_points_future_timelike=bool(np.all(future_timelike))))
    return summaries, identity_error, unit_error


def first(rows,key):
    return next((dict(checkpoint=i,**r) for i,r in enumerate(rows) if r.get(key,False)),None)


def main():
    started = time.monotonic()
    stored = [json.loads((BASE/p).read_text()) for p in INPUTS]
    original = [r for r in stored[0]['rows'] if r['all_numerical_controls_passed']]+stored[1]['rows']
    assert len(original)==9 and all(r['all_numerical_controls_passed'] for r in original)
    assert len(stored[2]['rows'])==5 and stored[2]['all_numerical_controls_passed']
    zero=exact_fields(0.,0.,0.,0.,np.linspace(-1.,1.,2049))
    controls=dict(zero_perturbation=bool(np.all(zero[0]==0)&np.all(zero[1]==0)))
    rows=[]
    for label,calibration,data in (
        ('original_development',dict(KB=1.,OB=.0125,OC=.2875),sorted(original,key=lambda r:r['K'])),
        ('standard_thermal_calibration',dict(KB=.02,OB=.049,OC=.251),stored[2]['rows']),
    ):
        for key,value in calibration.items(): setattr(model,key,value)
        model.C=2-model.KB
        model.D0=model.calibrated_charge()
        for row in data:
            for col,preparation in enumerate(('baryon_isocurvature','adiabatic_development')):
                coarse,ec,uc=inspect(row,col,1025)
                fine,ef,uf=inspect(row,col,2049)
                discrepancy=0.
                for old,new in zip(coarse,fine):
                    if not new['metric_domain_valid']: continue
                    keys=('min_delta_Q','max_delta_Q','min_delta_X','max_delta_X')
                    scale=max(max(abs(new[k]) for k in keys),1e-30)
                    discrepancy=max(discrepancy,max(abs(new[k]-old[k]) for k in keys)/scale)
                gates=dict(grid_extrema=discrepancy<=5e-4,algebra=max(ec,ef)<=2e-12,
                           vector_normalization=max(uc,uf)<=2e-12)
                result=dict(normalization=label,k_Mpc_inverse=row['k_Mpc_inverse'],preparation=preparation,
                            controls=gates,all_numerical_controls_passed=all(gates.values()),
                            grid_extrema_error=discrepancy,algebra_error=max(ec,ef),unit_error=max(uc,uf),
                            first_Q_lower_violation=first(fine,'Q_lower_violation'),
                            first_Q_upper_violation=first(fine,'Q_upper_violation'),
                            first_invariant_upper_violation=first(fine,'invariant_upper_violation'),
                            metric_invalid_checkpoints=sum(not r['metric_domain_valid'] for r in fine),
                            sampled_rows=fine)
                rows.append(result)
                print(json.dumps({k:result[k] for k in ('normalization','k_Mpc_inverse','preparation',
                     'all_numerical_controls_passed','grid_extrema_error','metric_invalid_checkpoints')}|
                     {k:(result[k]['a'] if result[k] else None) for k in
                      ('first_Q_lower_violation','first_Q_upper_violation','first_invariant_upper_violation')}),flush=True)
    controls['all_rows']=all(r['all_numerical_controls_passed'] for r in rows)
    result=dict(self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                input_sha256={p:hashlib.sha256((BASE/p).read_bytes()).hexdigest() for p in INPUTS},
                dependency_sha256={p:hashlib.sha256((BASE/p).read_bytes()).hexdigest() for p in
                                   ('charged_clock_response_v001.py','bounded_clock_shared_prediction_v001.py')},
                scope='Exact kinematics of saved-field ansatz; not an evolved nonlinear solution or observational score.',
                controls=controls,all_numerical_controls_passed=all(controls.values()),rows=rows,
                elapsed_seconds=time.monotonic()-started,
                peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUTPUT.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:result[k] for k in ('controls','all_numerical_controls_passed','elapsed_seconds','peak_RSS_bytes')}))
    if not result['all_numerical_controls_passed']: raise SystemExit(1)


if __name__=='__main__': main()
