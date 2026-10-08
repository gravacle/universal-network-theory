"""One-step refinement of V002, same equations and numerical thresholds.

V002's 128-step row missed the charge gate by 22%; its 256/512 rows passed
all row gates. Preserve that failed receipt. Reuse those completed finer
rows and run only a new 1024-step event, then apply the identical gates to
the declared 256/512/1024 sequence. No refit, changed initial data or claim
that V002 passed. This is a resolution repair, not a physical revision.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import tilt_fold_event_v001 as core

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'TILT_FOLD_EVENT_V002_RESULT.json'
OUT=BASE/'TILT_FOLD_EVENT_V003_RESULT.json'

def scalar(x):
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)

def main():
    beg=time.monotonic();old=json.loads(SOURCE.read_text())
    src=json.loads(core.SOURCE.read_text());saved=json.loads(core.prior.base.SOURCE.read_text())
    snap=src['rows'][-1]['snapshots'][-1];z=np.array(snap['state']);x=math.log(snap['a'])
    m=core.ext.Model(saved);g=m.unpack(x,z);s0=float(g['s'][0])
    curve=core.Curve(m,float(g['piph'][0]))
    y0=np.array([x+z[0,0],x+z[1,0],g['pia'][0],g['sig'][0],g['Z'][0],0.,0.,x])
    steps=1024;y=y0.copy();s=s0;ds=(-.996-s0)/steps;snaps=[];maxF=0.;event=None
    for i in range(steps):
        gi=curve.physical(s,y);maxF=max(maxF,abs(gi['F']/gi['M']))
        if i%(steps//16)==0:snaps.append(curve.receipt(s,y))
        yn=curve.rk4(s,y,ds)
        if curve.physical(s+ds,yn)['Schur']<=0:
            lo=0.;hi=1.
            for _ in range(44):
                mid=(lo+hi)/2;ym=curve.rk4(s,y,ds*mid)
                if curve.physical(s+ds*mid,ym)['Schur']>0:lo=mid
                else:hi=mid
            se=s+ds*(lo+hi)/2;ye=curve.rk4(s,y,ds*(lo+hi)/2)
            event=curve.receipt(se,ye);snaps.append(event);maxF=max(maxF,abs(event['F_relative']));break
        s+=ds;y=yn
    if event is None:raise ValueError('event not bracketed')
    rows=old['rows'][1:]+[dict(steps=steps,event=event,snapshots=snaps,maximum_charge_residual=maxF,
        eliminated_momentum_tangent_error=old['rows'][-1]['eliminated_momentum_tangent_error'])]
    def compare(r1,r2):
        y1=np.array(r1['event']['state']);y2=np.array(r2['event']['state'])
        return float(max(np.max(abs(y1-y2)/np.maximum(abs(y2),1.)),abs(r1['event']['s']-r2['event']['s'])))
    checks=dict(rhs_dictionary=old['preflight_rhs_error']<=1e-8,
        charge_constraint=max(r['maximum_charge_residual'] for r in rows)<=1e-9,
        event_schur=max(abs(r['event']['Schur_relative']) for r in rows)<=1e-8,
        refinement=compare(rows[1],rows[2])<=1e-7,
        eliminated_momentum=max(r['eliminated_momentum_tangent_error'] for r in rows)<=1e-6,
        positive_rest_cone=all(r['event']['KQQ']>0 and r['event']['longitudinal_coefficient']>0 for r in rows))
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        parent_result_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        base_script_sha256=hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),
        inherited_inputs_sha256=old['inputs_sha256'],inherited_dependencies_sha256=old['dependencies_sha256'],
        reused_completed_steps=[256,512],newly_computed_steps=[1024],rows=rows,
        fine_refinement=compare(rows[1],rows[2]),controls=checks,all_controls_passed=all(checks.values()),
        elapsed_seconds=time.monotonic()-beg)
    with OUT.open('x') as f:json.dump(result,f,default=scalar,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','protocol')},default=scalar,indent=2))
    print(json.dumps(event,default=scalar,indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
