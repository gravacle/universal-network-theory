"""Frozen algebraic identifiability audit, not a fit or new evolution.

Change only physical a0 by factors .5,1,2 at fixed Hunit, measured ordinary
normalization, K, KB, lambda, cTheta, clock charge and vacuum budget.
Dust-background epochs .01,.1,epoch54,1; linear homogeneous-background
assembly matrices at each epoch. Prospective relative identity gate 1e-13.
Nonlinear j evaluated at the SAME physical gradients .01,.1,1 times the
original bs. Independent derivative identity gate 1e-8, central relative
parameter increment 1e-4. Tests parameter sensitivity, NOT observations,
radiation history, native derivation, or a formed galaxy. One small worker.
"""
from pathlib import Path
import copy
import json
import math
import time
import numpy as np
import invariant_clock_periodic_initial_v002 as initial

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_SHARED_SCALE_AUDIT_V001_RESULT.json'

def main():
    if OUT.exists(): raise FileExistsError(OUT)
    start=time.monotonic()
    model,parent=initial.load()
    points=[.01,.1,parent['histories'][-1]['snapshots'][54]['a'],1.]
    reference=initial.linear.Assembly(model)
    checks=[]; rows=[]
    def check(name,error,gate):
        checks.append(dict(name=name,error=float(error),gate=gate,passed=bool(error<=gate)))
    for factor in (.5,1.,2.):
        saved=copy.deepcopy(model.saved)
        saved['inherited']['a0']=factor*model.p['a0']
        other=type(model)(saved,1)
        run=initial.linear.Assembly(other)
        for a in points:
            x=math.log(a)
            b0=np.array(reference.bg(x)); b1=np.array(run.bg(x))
            m0=reference.matrix(x); m1=run.matrix(x)
            be=np.max(abs(b1-b0)/np.maximum(abs(b0),1e-30))
            me=np.max(abs(m1-m0))/max(np.max(abs(m0)),1e-30)
            check(f'{factor}_{a}_background',be,1e-13)
            check(f'{factor}_{a}_linear_matrix',me,1e-13)
            rows.append(dict(factor=factor,a=a,background_relative_error=float(be),
                             linear_matrix_relative_error=float(me)))
    gradients=[]
    for ratio in (.01,.1,1.):
        p=ratio*model.bs
        def j(f): return model.lam*abs(p)/math.hypot(p,f*model.bs)
        derivative=(math.log(j(1.0001))-math.log(j(.9999)))/(math.log(1.0001)-math.log(.9999))
        expected=-model.bs**2/(p*p+model.bs**2)
        check(f'nonlinear_j_sensitivity_{ratio}',abs(derivative-expected),1e-8)
        gradients.append(dict(p_over_original_bs=ratio,j_by_factor={str(f):j(f) for f in (.5,1.,2.)},
                              dlogj_dloga0_numeric=derivative,dlogj_dloga0_exact=expected))
    result=dict(protocol=__doc__,producer_sha256=initial.sha(__file__),
        dependencies={str(Path(p)):initial.sha(p) for p in
            (initial.__file__, initial.linear.__file__, initial.linear.linear.__file__,
             initial.linear.linear.old.__file__, initial.linear.linear.old.base.__file__, initial.SOURCE)},
        inherited=model.p,cTheta=.01,epochs=points,checks=checks,background_and_linear=rows,
        nonlinear_gradients=gradients,
        conclusion='a0 is an independent nonlinear interaction scale; this homogeneous and linear sector does not predict it',
        no_observational_validation=True,all_controls_passed=all(c['passed'] for c in checks),
        elapsed_seconds=time.monotonic()-start)
    with OUT.open('x') as out: json.dump(result,out,indent=2,allow_nan=False)
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],checks=checks,
                         nonlinear_gradients=gradients,sha256=initial.sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']: raise SystemExit(1)

if __name__=='__main__': main()
