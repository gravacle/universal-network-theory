"""Bounded CF4 phase refinement after preserved V002 failure.

Unchanged source-free physical model, seeds, interval, retained fields and
all-prefix/adjacent-segment1e-4 floor1e-30 gates. Reuse completed V002
16384-step evidence; add32768/65536/131072 in ONE serial worker,55s cap.
Save all completed resolutions even if the cap or a control fails. No mode
filter, coefficient fitting, or nonlinear/observational interpretation.
"""
from pathlib import Path
import json,math,time
import numpy as np
import invariant_clock_compression_assembly_v002 as prev

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V003_RESULT.json'
EXPECTED='e3b6a9eed1f3b6230958abe4aff625a2545f54913a1d5981514bafb93eaba9e4'

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if prev.sha(prev.OUT)!=EXPECTED:raise ValueError('changed previous result')
    result=json.loads(prev.OUT.read_text())
    if prev.sha(Path(prev.__file__))!=result['producer_sha256']:raise ValueError('changed CF4 producer')
    for p,d in result['dependencies'].items():
        if prev.sha(Path(p))!=d:raise ValueError('changed dependency')
    saved=json.loads(prev.old.linear.old.base.SOURCE.read_text());saved['inherited']=result['fixed']
    model=prev.old.linear.old.base.Model(saved,1);hist=[result['histories'][-1]];error=None
    started=time.monotonic();cm=.5-math.sqrt(3)/6;cp=.5+math.sqrt(3)/6
    am=(3-2*math.sqrt(3))/12;ap=(3+2*math.sqrt(3))/12;x0=math.log(.01)
    try:
        for n in (32768,65536,131072):
            run=prev.old.Assembly(model);y=run.initial(x0);h=-x0/n;snaps=[]
            for i in range(n+1):
                x=x0+i*h
                if i%(n//64)==0:snaps.append(run.values(x,y))
                if i==n:break
                A=run.matrix(x+cm*h);B=run.matrix(x+cp*h)
                y=prev.expm(h*(am*A+ap*B))@prev.expm(h*(ap*A+am*B))@y
                if not np.all(np.isfinite(y)):raise ValueError('nonfinite transfer')
                if time.monotonic()-started>55:raise TimeoutError('55s serial bound')
            hist.append(dict(steps=n,snapshots=snaps,Einstein_derivative=run.max_constraint))
            comp={k:prev.errors(hist[-2],hist[-1],k) for k in ('state','observables')}
            print(json.dumps(dict(steps=n,elapsed=time.monotonic()-started,
                errors={k:{j:v for j,v in val.items() if j.endswith('max')} for k,val in comp.items()})),flush=True)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
    checks=[c for c in result['checks'] if c['name'].startswith('exponential_')]
    comp={}
    if len(hist)>1:
        for key in ('state','observables'):
            comp[key]=prev.errors(hist[-2],hist[-1],key)
            for scope in ('all_prefix_max','all_segment_max'):
                e=comp[key][scope];checks.append(dict(name=scope+'_'+key,error=e,gate=1e-4,passed=bool(e<=1e-4)))
    e=max(r['Einstein_derivative'] for r in hist)
    checks.append(dict(name='Einstein_derivative',error=e,gate=1e-9,passed=bool(e<=1e-9)))
    result.update(protocol=__doc__,producer_sha256=prev.sha(Path(__file__)),phase_repair_parent_sha256=EXPECTED,
        dependencies={**result['dependencies'],str(Path(prev.__file__)):prev.sha(Path(prev.__file__))},
        histories=hist,comparisons=comp,checks=checks,error=error,elapsed_seconds=time.monotonic()-started,
        all_controls_passed=error is None and len(hist)==4 and all(c['passed'] for c in checks))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(all_pass=result['all_controls_passed'],checks=checks,error=error,sha256=prev.sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
