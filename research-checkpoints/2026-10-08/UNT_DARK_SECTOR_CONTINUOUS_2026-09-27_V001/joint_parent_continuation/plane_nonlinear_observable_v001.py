"""Invariant matter prediction from an ACCEPTED nonlinear trajectory only.

Require full acceptance of PLANE_CONSTRAINED_EVOLUTION_V002 first. Compare
all65 fixed dust-proper-time checkpoints, no selected fitting epoch and no
new initial condition. C=<rho_b²>_proper_volume/<rho_b>²−1; evaluate squared
contrasts stably. Linear C=.5(delta_b,N+3h Vb,N)² from the prior exact same
seed, not new observational evidence. Report nonlinear-minus-linear and
ratios without setting a physical success threshold. Require clumping
time/space refinements<=1e-4, absolute floor1e-20; report harmonics as
coordinate-profile diagnostics, not spatial-relabeling invariants.
No data fit, halo, source reset, nonlinear Newtonian gauge transform or
claim of galaxy formation. Inputs remain a single periodic plane mode.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import resource
import numpy as np
import plane_constrained_evolution_v001 as ev

BASE=Path(__file__).resolve().parent
FILES=['PLANE_CONSTRAINED_EVOLUTION_V002_RESULT.json','PLANE_CMC_INITIAL_DATA_V002_RESULT.json','CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json']
OUT=BASE/'PLANE_NONLINEAR_OBSERVABLE_V001_RESULT.json'


def main():
    started=time.monotonic();run,initial,lin=[json.loads((BASE/f).read_text()) for f in FILES]
    if not run['all_controls_passed']:raise ValueError('Full nonlinear trajectory not accepted; no score produced')
    rows=run['rows'];models=[ev.Model(initial,r['nodes']) for r in rows]
    lr=next(r for r in lin['rows'] if r['k_Mpc_inverse']==.01)
    ly=np.array(lr['trajectory_2048_scaled'])*np.array(lr['state_scales'])[None,:,None]
    records=[]
    for i in range(65):
        states=[np.array(r['snapshots'][i]['state']) for r in rows]
        a=rows[-1]['snapshots'][i]['a'];h=models[-1].bg(math.log(a))[5]
        values=[]
        for m,z in zip(models,states):
            v=z[0]+2*z[1];vv=np.exp(v);vm=np.mean(vv);wm=np.mean(m.dust_weight)
            delta=np.expm1(np.log(m.dust_weight)+math.log(vm/wm)-v)
            C=float(np.mean(vv*delta*delta)/vm)
            values.append(C)
        linear=float(.5*(ly[i,1,6]+3*h*ly[i,2,6])**2)
        e_time=abs(values[0]-values[1])/max(values[1],1e-20)
        e_space=abs(values[1]-values[2])/max(values[2],1e-20)
        m=models[-1];z=states[-1];g=m.unpack(math.log(a),z)
        # Constitutive margins computed without subtracting rounded Q from its cap.
        low=m.Q0*m.eps*g['s']/((1+g['s'])*(g['qroot']+1))
        upper=m.Q0*m.eps/((1+g['s'])*(math.sqrt(1+m.eps)+g['qroot']))
        v=z[0]+2*z[1];rho=m.dust_weight*np.exp(-v)
        harmonics=(2*abs(np.fft.rfft(rho/np.mean(rho)-1))/len(rho))[:9]
        records.append(dict(a=a,clumping_by_resolution=values,linear_clumping=linear,
            nonlinear_minus_linear=values[-1]-linear,nonlinear_to_linear=values[-1]/linear if linear else None,
            clumping_time_refinement=e_time,clumping_space_refinement=e_space,
            min_clock_lower_margin_H0=float(np.min(low)),min_clock_upper_margin_H0=float(np.min(upper)),
            min_schur_fraction=rows[-1]['minimum_schur_fraction'],
            max_density_contrast=float(np.max(abs(rho-1))),max_vector_tilt=float(np.max(abs(g['sig']))),
            max_JY=float(np.max(g['j'])),density_profile_harmonic_amplitudes=harmonics.tolist()))
    checks=dict(input_evolution_accepted=True,
        time=max(r['clumping_time_refinement'] for r in records)<=1e-4,
        space=max(r['clumping_space_refinement'] for r in records)<=1e-4,
        physical_branch=min(min(r['min_clock_lower_margin_H0'],r['min_clock_upper_margin_H0']) for r in records)>0)
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in FILES},
        dependencies_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in ('plane_constrained_evolution_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py')},
        checkpoints=records,controls=checks,all_controls_passed=all(checks.values()),
        elapsed_seconds=time.monotonic()-started,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(controls=checks,all_controls_passed=result['all_controls_passed'],
        selected_checkpoints=[records[j] for j in (0,16,32,48,56,64)],elapsed_seconds=result['elapsed_seconds']),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
