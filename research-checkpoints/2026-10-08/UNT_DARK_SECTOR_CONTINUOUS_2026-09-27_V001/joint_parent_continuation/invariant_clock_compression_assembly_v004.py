"""Phase-resolved bounded continuation, unchanged model and numerical gates.

V003 reaches a fast-phase-per-step of order2pi and still fails full-state
refinement. Reuse its finest result, add262144 and524288 CF4 steps to
resolve that phase without filtering. One six-state/two-seed serial worker,
160s total wall bound, checkpoint every4096 accepted steps. SAME each-prefix
and adjacent-segment1e-4/floor1e-30, no physical/amplitude/parameter change.
Existing failed phase histories remain; passing this test is NOT a physical
finite-amplitude trajectory or a primordial/galaxy prediction.
"""
from pathlib import Path
import json,math,time
import numpy as np
import invariant_clock_compression_assembly_v003 as prev

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V004_RESULT.json'
CHECKPOINT=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V004_CHECKPOINT.json'
EXPECTED='c76974fdebc68f017b2947b5e2434cd0fff27b1eeabe4eeed25a44f7168c106c'
core=prev.prev

def main():
    if OUT.exists() or CHECKPOINT.exists():raise FileExistsError('exclusive run exists')
    if core.sha(prev.OUT)!=EXPECTED:raise ValueError('changed V003 evidence')
    result=json.loads(prev.OUT.read_text())
    if core.sha(Path(prev.__file__))!=result['producer_sha256']:raise ValueError('changed preceding producer')
    for p,d in result['dependencies'].items():
        if core.sha(Path(p))!=d:raise ValueError('changed dependency')
    saved=json.loads(core.old.linear.old.base.SOURCE.read_text());saved['inherited']=result['fixed']
    model=core.old.linear.old.base.Model(saved,1);hist=[result['histories'][-1]];error=None
    started=time.monotonic();cm=.5-math.sqrt(3)/6;cp=.5+math.sqrt(3)/6
    am=(3-2*math.sqrt(3))/12;ap=(3+2*math.sqrt(3))/12;x0=math.log(.01)
    try:
        for n in (262144,524288):
            run=core.old.Assembly(model);y=run.initial(x0);h=-x0/n;snaps=[]
            for i in range(n+1):
                x=x0+i*h
                if i%(n//64)==0:snaps.append(run.values(x,y))
                if i%4096==0:
                    with CHECKPOINT.open('w') as f:json.dump(dict(producer_sha256=core.sha(Path(__file__)),
                        parent_sha256=EXPECTED,steps=n,accepted_step=i,x=x,state=y.tolist(),
                        snapshots=snaps,completed_histories=hist),f,allow_nan=False)
                if i==n:break
                A=run.matrix(x+cm*h);B=run.matrix(x+cp*h)
                y=core.expm(h*(am*A+ap*B))@core.expm(h*(ap*A+am*B))@y
                if not np.all(np.isfinite(y)):raise ValueError('nonfinite transfer')
                if time.monotonic()-started>160:raise TimeoutError('160s serial bound; accepted checkpoint retained')
            hist.append(dict(steps=n,snapshots=snaps,Einstein_derivative=run.max_constraint))
            comp={k:core.errors(hist[-2],hist[-1],k) for k in ('state','observables')}
            print(json.dumps(dict(steps=n,elapsed=time.monotonic()-started,
                errors={k:{j:v for j,v in val.items() if j.endswith('max')} for k,val in comp.items()})),flush=True)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
    checks=[c for c in result['checks'] if c['name'].startswith('exponential_')];comp={}
    if len(hist)>1:
        for key in ('state','observables'):
            comp[key]=core.errors(hist[-2],hist[-1],key)
            for scope in ('all_prefix_max','all_segment_max'):
                e=comp[key][scope];checks.append(dict(name=scope+'_'+key,error=e,gate=1e-4,passed=bool(e<=1e-4)))
    e=max(r['Einstein_derivative'] for r in hist)
    checks.append(dict(name='Einstein_derivative',error=e,gate=1e-9,passed=bool(e<=1e-9)))
    result.update(protocol=__doc__,producer_sha256=core.sha(Path(__file__)),phase_repair_parent_sha256=EXPECTED,
        dependencies={**result['dependencies'],str(Path(prev.__file__)):core.sha(Path(prev.__file__))},
        histories=hist,comparisons=comp,checks=checks,error=error,elapsed_seconds=time.monotonic()-started,
        all_controls_passed=error is None and len(hist)==3 and all(c['passed'] for c in checks))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(all_pass=result['all_controls_passed'],checks=checks,error=error,sha256=core.sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
