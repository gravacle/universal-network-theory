"""Refine only the V001 failed 5kpc cTheta=0 numerical control.

Preserve all four scientific rows and the failed V001 receipt. Reuse three
qualified rows. Same equations, source, endpoint and1e-4 acceptance gate;
add1024 subdivisions to the failed row, compare the full retained state
and all observables with saved512. No tolerance, physical parameter,
preparation or amplitude change. The proposed elastic rows are not rerun.
"""
from pathlib import Path
import hashlib
import json
import time
import invariant_clock_compression_response_v001 as old

ROOT=Path(__file__).resolve().parent
PREV=ROOT/'INVARIANT_CLOCK_COMPRESSION_RESPONSE_V001_RESULT.json'
PREVSHA='6c87ff722533db05d66a75cc3eb06c6cc07cb41c2a5ff0c5a3691b64ede1509a'
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_RESPONSE_V002_RESULT.json'

def main():
    started=time.monotonic()
    if OUT.exists():raise RuntimeError('no overwrite/duplicate worker')
    if old.sha(PREV)!=PREVSHA:raise ValueError('changed failed receipt')
    result=json.loads(PREV.read_text())
    if old.sha(Path(old.__file__))!=result['source_sha256']:raise ValueError('changed original source')
    if old.sha(old.CAL)!=result['calibration_sha256']:raise ValueError('changed calibration')
    for path,digest in result['dependencies'].items():
        if old.sha(Path(path))!=digest:raise ValueError('changed dependency')
    saved=json.loads(old.base.SOURCE.read_text());saved['inherited']=result['fixed']
    model=old.base.Model(saved,1);run=old.Response(model,5.,0.)
    new=run.integrate(1024)
    row=next(r for r in result['rows'] if r['width_kpc']==5. and r['cTheta']==0.)
    prior=row['histories'][-1];row['histories'].append(new)
    values={'5.0kpc_cT0.0_state_refinement':old.discrepancy(prior,new,'state'),
            '5.0kpc_cT0.0_observable_refinement':old.discrepancy(prior,new,'observables'),
            '5.0kpc_cT0.0_Einstein_derivative':new['constraint_defect'],
            '5.0kpc_cT0.0_source_conservation':new['source_defect']}
    for control in result['controls']:
        if control['name'] in values:
            control['error']=values[control['name']]
            control['passed']=bool(control['error']<=control['gate'])
    snaps=new['snapshots'];row['final']=snaps[-1];row['one_formation']=snaps[32]
    row['peak_abs_observables']=old.np.max(abs(old.np.array([r['observables'] for r in snaps])),axis=0).tolist()
    row['maximum_physical_extrapolation']={key:max(r['physical_depth_linear_extrapolation'][key] for r in snaps)
        for key in snaps[0]['physical_depth_linear_extrapolation']}
    result.update(refinement_protocol=__doc__,previous_result_sha256=PREVSHA,
        refinement_source_sha256=old.sha(Path(__file__)),refinement_elapsed_seconds=time.monotonic()-started,
        all_controls_passed=all(c['passed'] for c in result['controls']))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(all_controls_passed=result['all_controls_passed'],refined_errors=values,
        failed=[c for c in result['controls'] if not c['passed']],
        elapsed_seconds=result['refinement_elapsed_seconds'],result_sha256=old.sha(OUT)),indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
