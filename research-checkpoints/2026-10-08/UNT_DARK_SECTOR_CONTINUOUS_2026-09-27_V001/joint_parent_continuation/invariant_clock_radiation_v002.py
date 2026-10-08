"""Refine ONLY the failed k=.1 perfect-radiation row; reuse k=.01.

V001 misses the1e-4 time gate in both candidate and reference radiation
oscillations (.00035636), not in constraints or gauge identities. Add
4096-step candidate/reference and earlier-start controls, reuse their
saved2048 states. Same model, benchmark, fields, criteria and endpoints.
No new fit, CMB spectrum or observational interpretation.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_radiation_v001 as prev

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_RADIATION_V002_RESULT.json'


def main():
    beg=time.monotonic();prior=json.loads(prev.OUT.read_text())
    expected=prior['hashes'][Path(prev.__file__).name]
    if hashlib.sha256(Path(prev.__file__).read_bytes()).hexdigest()!=expected:
        raise ValueError('frozen V001 source changed')
    saved=json.loads(prev.old.base.SOURCE.read_text())
    saved['inherited']['Q0_over_H0']=100.
    model=prev.old.base.Model(saved,1);K=.1*299792.458/model.p['H0_km_s_Mpc']
    row=next(r for r in prior['rows'] if r['k_Mpc_inverse']==.1)
    fine=prev.integrate(model,K,4096)
    ref=prev.integrate(model,K,4096,dust=True)
    half=prev.integrate(model,K,4096,ai=5e-8)
    controls=[]
    def check(name,error,gate):
        controls.append(dict(name=name,error=error,tolerance=gate,passed=bool(error<=gate)))
    check('time_refinement_0.1',prev.error(row['histories'][-1],fine),1e-4)
    check('reference_refinement_0.1',prev.error(row['references'][-1],ref,[0,1,2,3,4,7,8]),1e-4)
    check('constraint_trajectory_0.1',fine['maximum_constraint'],1e-6)
    end=np.array(fine['snapshots'][-1]['state']);he=np.array(half['snapshots'][-1]['state'])
    norm=np.maximum(np.max(abs(np.array([r['state'] for r in half['snapshots']])),axis=0),1e-30)
    check('initial_time_control_0.1',float(np.max(abs(end-he)/norm)),1e-4)
    r=np.array(ref['snapshots'][-1]['state'])
    comparison=dict(potential_ratio=float(end[0]/r[0]),ordinary_density_ratio=float(end[1]/r[1]),
        clock_to_reference_matter_density_ratio=float((end[3]-end[6])/r[3]),
        radiation_density_difference=float(end[7]-r[7]),radiation_velocity_difference=float(end[8]-r[8]))
    replaced={c['name'] for c in controls}
    reused=[c for c in prior['controls'] if c['name'] not in replaced]
    result=dict(protocol=__doc__,k_Mpc_inverse=.1,fine=fine,reference=ref,half_start=half,
        controls=controls,reused_controls=reused,comparison=comparison,
        all_controls_passed=all(c['passed'] for c in controls+reused),
        elapsed_seconds=time.monotonic()-beg,
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                (Path(__file__),Path(prev.__file__),prev.OUT)})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('fine','reference','half_start','protocol')}))


if __name__=='__main__':main()
