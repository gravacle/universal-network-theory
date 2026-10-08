"""Prospective shorter-scale discriminator, not another clock-parameter fit.

Keep proposed K(X), Q0/H0=100 and every other constant from the first test.
Move ONLY k from .01 to1/Mpc, a new development consequence. This probes
where the clock acoustic scale can affect growth; it is not an observed
likelihood. Same two linear preparations, same2048/4096/8192 step sequence,
same full-state relative convergence1e-4 (floor1e-30), same reference gate.
Report all failures. Do not recalibrate abundance, epsilon, Q0 or a0.
No completion, galaxy, native-formation or superiority claim.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_transfer_v001 as core

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_SHORT_SCALE_V001_RESULT.json'

def scalar(x):
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)

def main():
    beg=time.monotonic();saved=json.loads(core.base.SOURCE.read_text())
    saved['inherited']['Q0_over_H0']=100.;m=core.base.Model(saved,1)
    K=299792.458/saved['inherited']['H0_km_s_Mpc']
    hist=[core.integrate(m,K,n) for n in (2048,4096,8192)]
    coarse=core.error(hist[0],hist[1],'state');fine=core.error(hist[1],hist[2],'state')
    obs_err=core.error(hist[1],hist[2],'observables')
    ref=[core.reference(m,K,n) for n in (2048,4096)]
    ra=np.array(ref[0]['snapshots']);rb=np.array(ref[1]['snapshots'])
    re=float(np.max(np.max(abs(ra-rb),axis=0)/np.maximum(np.max(abs(rb),axis=0),1e-30)))
    comparisons=[]
    for index in (32,48,64):
        snap=hist[-1]['snapshots'][index];obs=np.array(snap['observables'])
        comparisons.append(dict(a=snap['a'],ratios=(obs[:3]/rb[index,:3]).tolist()))
    checks=dict(full_state_refinement=bool(fine<=1e-4),reference_refinement=bool(re<=1e-4))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256=hashlib.sha256(core.base.SOURCE.read_bytes()).hexdigest(),
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in
            ['invariant_clock_transfer_v001.py','plane_canonical_evolution_v001.py','charged_clock_response_v001.py','bounded_clock_shared_prediction_v001.py']},
        Q0_over_H0=100.,k_Mpc_inverse=1.,K=K,histories=hist,pressureless_reference=ref,
        coarse_error=coarse,fine_error=fine,observable_error=obs_err,reference_error=re,
        comparison_order=['Phi','Newtonian_delta_b','theta_b'],preparations=['isocurvature','adiabatic'],
        comparisons=comparisons,controls=checks,all_controls_passed=bool(all(checks.values())),
        elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,default=scalar,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('histories','pressureless_reference','protocol')},default=scalar,indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
