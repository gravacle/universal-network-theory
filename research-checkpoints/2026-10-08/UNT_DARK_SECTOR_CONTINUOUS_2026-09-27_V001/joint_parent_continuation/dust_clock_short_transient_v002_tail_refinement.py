"""Extend only the unresolved forced harmonic tails, with original criteria."""
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
import dust_clock_short_transient_v001 as original

HERE=Path(__file__).resolve().parent
OUT=HERE/'DUST_CLOCK_SHORT_TRANSIENT_V002_RESULT.json'
PROTOCOL=HERE/'DUST_CLOCK_SHORT_TRANSIENT_V002_TAIL_REFINEMENT.md'
PRIOR_SHA='489364c23fca12b5b9bbf3fa10774f4f36b1f574ccfe6a25af14bc6202d2ada7'
SOURCE_SHA='4e27beeae16b8e532835228a1b1cb65c23b2fec3a32155273b8a4064294836c0'


def compact(run):
    result={key:value for key,value in run.items() if key!='samples'}
    result['samples']=[]
    for i,row in enumerate(run['samples']):
        keep={key:value for key,value in row.items() if key!='corrections'}
        cc=np.asarray(row['corrections'])
        keep['correction_L1']=np.sum(abs(cc),axis=0).tolist()
        if i==len(run['samples'])-1:
            keep['corrections']=row['corrections']
        result['samples'].append(keep)
    return result


def main():
    if OUT.exists():
        raise SystemExit('Refusing overwrite')
    assert hashlib.sha256(original.OUTPUT.read_bytes()).hexdigest()==PRIOR_SHA
    assert hashlib.sha256(Path(original.__file__).read_bytes()).hexdigest()==SOURCE_SHA
    started=time.perf_counter()
    controls=[]
    cases=[]

    def check(name,error,tolerance):
        controls.append(dict(name=name,error=float(error),tolerance=tolerance,
                             passed=bool(math.isfinite(error) and error<=tolerance)))

    for k,mmax in ((.01,4095),(.1,511)):
        runs=[original.evolve(k,mmax,n) for n in (8192,16384)]
        medium,fine=runs
        ll=np.asarray([s['linear'] for s in fine['samples']])
        lm=np.asarray([s['linear'] for s in medium['samples']])
        cc=np.asarray([s['corrections'] for s in fine['samples']])
        cm=np.asarray([s['corrections'] for s in medium['samples']])
        half=cc.shape[1]//2
        for j,name in enumerate(original.READOUTS):
            scale=max(fine['correction_peak'][name],1e-300)
            check(f'linear_time:k={k}:{name}',
                  np.max(abs(ll[:,j]-lm[:,j]))/max(np.max(abs(ll[:,j])),1e-300),2e-5)
            check(f'correction_time:k={k}:{name}',
                  np.max(np.sum(abs(cc[:,:,j]-cm[:,:,j]),axis=1))/scale,5e-3)
            halfpeak=np.max(np.sum(abs(cc[:,:half,j]),axis=1))
            check(f'harmonic_tail:k={k}:{name}',abs(scale-halfpeak)/scale,.02)
            check(f'time_uniform_harmonic_tail:k={k}:{name}',
                  np.max(np.sum(abs(cc[:,half:,j]),axis=1))/scale,.02)
        cases.append(dict(k_Mpc_inverse=k,levels=[compact(r) for r in runs]))
        print(f'Completed fixed tail refinement k={k}, mmax={mmax}',flush=True)
    result=dict(status='QUALIFIED' if all(c['passed'] for c in controls) else 'FAILED',
                preserved_prior_sha256=PRIOR_SHA,original_source_sha256=SOURCE_SHA,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                controls=controls,cases=cases,elapsed_seconds=time.perf_counter()-started,
                scope='Only failed harmonic tails extended; k=1 result remains V001; no full nonlinear certificate')
    encoded=json.dumps(result,indent=2,allow_nan=False)
    with OUT.open('x') as handle:
        handle.write(encoded+'\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
                         failed=[c for c in controls if not c['passed']],
                         summaries=[dict(k=c['k_Mpc_inverse'],
                            corrections=c['levels'][-1]['estimated_correction_fraction'],
                            screens=c['levels'][-1]['screens'],
                            peaks=c['levels'][-1]['peak_bounds']) for c in cases],
                         elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':
    main()
