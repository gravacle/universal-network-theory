"""Audit saved failed trajectories only; no new evolution or fitted tolerance.

Retain failures of BOTH full interval runs. Identify the largest contiguous
checkpoint prefix satisfying the original Hamiltonian, momentum, inverse,
charge and 1e-4 trajectory-refinement criteria. Refinement normalization is
stricter here: instantaneous fine amplitude (floor1e-8), not a later global
maximum from an unresolved state. A prefix is not a continuous-time proof
or acceptance of the original full-interval task. No branch/seed changes.

Compute the spatially invariant ordinary-density clumping at fixed dust
proper time, including all harmonics: C=<rho²>_V/<rho>_V²−1, evaluated by
weighted squared density contrast. The linear comparison is
C_lin=.5(delta_b,Newton+3 h Vb,Newton)² for the SAME isocurvature seed.
Compare all65 checkpoints, not a selected epoch. Add a 1e-4 relative
observable-refinement gate with absolute1e-20 floor before using the prefix
clumping difference. This is numerical accuracy, not observational success.
Inspect saved spectral tails and unprojected local constraints to distinguish
resolved nonlinear response from growing spatial error. No trajectory is
repaired by this postprocessing. Exclusive result, pinned inputs.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import resource
import numpy as np
import plane_canonical_evolution_v002 as ev

BASE=Path(__file__).resolve().parent
FILES=['PLANE_CANONICAL_EVOLUTION_V002_RESULT.json','PLANE_CMC_INITIAL_DATA_V002_RESULT.json','CHARGED_CLOCK_BBN_CALIBRATED_V001_RESULT.json']
OUT=BASE/'PLANE_SAVED_TRAJECTORY_AUDIT_V001_RESULT.json'


def constraint_arrays(m,a,z):
    g=m.unpack(math.log(a),z);A=g['A'];V=g['V'];h=g['h'];fg=g['B']**2/A
    curv=fg*(4*m.dx(g['bx'])+6*g['bx']**2-4*g['ax']*g['bx'])
    HH=g['kin']+curv+V*(m.KB*g['e']**2+m.C*g['p']**2+m.C*g['J']-2*g['Kfun'])+g['piph']*g['q']+g['c']*g['piux']+m.piT
    DD=g['pia']*g['ax']+g['pib']*g['bx']-m.dx(g['pia'])-g['abar']*z[2]*g['piux']+g['piph']*m.dx(z[3])
    defect=4*(m.dx(fg*g['bx'])-fg*m.dx(g['bx'])-fg*(-g['ax']+2*g['bx'])*g['bx'])
    return HH/(6*V*h*h),DD,defect/(6*V*h*h),g['p']


def main():
    started=time.monotonic();data=[json.loads((BASE/f).read_text()) for f in FILES]
    run,initial,lin=data;rows=run['rows'];models=[ev.Model(initial,r['nodes']) for r in rows]
    lr=next(r for r in lin['rows'] if r['k_Mpc_inverse']==.01)
    ly=np.array(lr['trajectory_2048_scaled'])*np.array(lr['state_scales'])[None,:,None]
    checkpoints=[];prefix=True;last_valid=None
    for i in range(65):
        states=[np.array(r['snapshots'][i]['state']) for r in rows]
        a=rows[-1]['snapshots'][i]['a'];h=models[-1].bg(math.log(a))[5]
        cl=[]
        for m,z in zip(models,states):
            v=z[0]+2*z[1];vv=np.exp(v);vm=np.mean(vv);wm=np.mean(m.dust_weight)
            delta=np.expm1(np.log(m.dust_weight)+math.log(vm/wm)-v)
            cl.append(float(np.mean(vv*delta*delta)/vm))
        clin=.5*(ly[i,1,6]+3*h*ly[i,2,6])**2
        scales_t=np.maximum(np.max(abs(states[2]),axis=1),1e-8)
        scales_s=np.maximum(np.max(abs(states[3]),axis=1),1e-8)
        et=float(np.max(np.max(abs(states[1]-states[2]),axis=1)/scales_t))
        es=float(np.max(np.max(abs(ev.prolong(states[2],rows[3]['nodes'])-states[3]),axis=1)/scales_s))
        snapshots=[r['snapshots'][i] for r in rows[1:]]
        checks=dict(time=et<=1e-4,space=es<=1e-4,
            H_background=max(s['Hamiltonian_background_normalized'] for s in snapshots)<=1e-9,
            H_perturbation=max(s['Hamiltonian_perturbation_normalized'] for s in snapshots)<=1e-4,
            momentum=max(s['momentum_normalized'] for s in snapshots)<=1e-4,
            charge=max(abs(s['mean_charge_change']) for s in snapshots)<=2e-12,
            clumping_time=abs(cl[1]-cl[2])/max(cl[2],1e-20)<=1e-4,
            clumping_space=abs(cl[2]-cl[3])/max(cl[3],1e-20)<=1e-4)
        passed=all(checks.values())
        if prefix and passed:last_valid=i
        else:prefix=False
        checkpoints.append(dict(index=i,a=a,checks=checks,passed=passed,
            instantaneous_time_refinement=et,instantaneous_space_refinement=es,
            clumping_by_resolution=cl,linear_clumping=float(clin),
            finest_minus_linear=float(cl[-1]-clin),finest_to_linear=float(cl[-1]/clin) if clin else None))
    first_fail={key:next((r['a'] for r in checkpoints if not r['checks'][key]),None) for key in checkpoints[0]['checks']}
    final_spatial=[]
    for m,row in zip(models,rows):
        z=np.array(row['snapshots'][-1]['state']);HH,DD,defect,p=constraint_arrays(m,1.,z)
        n=row['nodes'];spec=2*abs(np.fft.rfft(z,axis=-1))/n
        hspec=2*abs(np.fft.rfft(HH))/n
        ix=int(np.argmax(abs(HH)))
        final_spatial.append(dict(nodes=n,H_max=float(np.max(abs(HH))),
            H_at_max_coordinate=float(m.y[ix]),phase_gradient_at_H_max=float(p[ix]),
            phase_gradient_max=float(np.max(abs(p))),curvature_product_defect_max=float(np.max(abs(defect))),
            state_spectra=spec.tolist(),H_spectrum=hspec.tolist(),
            sampled_H=HH.tolist(),sampled_D=DD.tolist(),sampled_p=p.tolist()))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in FILES},
        dependencies_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in ('plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py')},
        original_full_interval_accepted=False,last_contiguous_valid_checkpoint=last_valid,
        last_valid=(checkpoints[last_valid] if last_valid is not None else None),
        first_failure_a_by_gate=first_fail,checkpoints=checkpoints,final_spatial=final_spatial,
        elapsed_seconds=time.monotonic()-started,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','checkpoints','final_spatial')},indent=2))
    for r in final_spatial:
        print(json.dumps({k:v for k,v in r.items() if not isinstance(v,list)}))


if __name__=='__main__':main()
