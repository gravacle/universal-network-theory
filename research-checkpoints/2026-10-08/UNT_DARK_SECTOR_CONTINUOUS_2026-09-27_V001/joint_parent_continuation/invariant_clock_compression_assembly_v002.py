"""Full-phase CF4 repair of assembly V001, not a changed physical model.

V001 endpoint-normalized refinement masked early fast-mode phase error;
its saved all-prefix audit FAILS. Retain the same full six fields, source-
free matter evolution, two seeds, background, parameters, a=.01..1 and
65 retained epochs. No damping/filtering of fast modes, no retuned seed.
Replace A-stable Gauss by existing CF4 Magnus/Pade13 exponential. Serial
4096/8192/16384 steps. SAME1e-4 floor1e-30 gate applied to EACH prefix and
adjacent retained-epoch segment, not just endpoint-normalized history.
Independent exponential controls1e-10 and Einstein identity1e-9. Bounded
45s wall time; completed resolutions saved even on a numerical failure.
Linear unit-seed transfers are never finite physical densities. This is
not primordial mode selection, nonlinear formation or observational proof.
"""
from pathlib import Path
import hashlib,json,math,time
import numpy as np
import invariant_clock_compression_assembly_v001 as old

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'INVARIANT_CLOCK_COMPRESSION_ASSEMBLY_V002_RESULT.json'
AUDIT=ROOT/'INVARIANT_CLOCK_ASSEMBLY_AUDIT_V001_RESULT.json'
AUDITSHA='d8d1995600ab987f2aa8e1aa6363fe3608f67a6b1ea53160aee3565861f48596'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expm=old.linear.old.expm

def errors(left,right,key):
    a=np.array([s[key] for s in left['snapshots']]);b=np.array([s[key] for s in right['snapshots']])
    pre=[];seg=[]
    for i in range(1,len(a)):
        pre.append(float(np.max(np.max(abs(a[:i+1]-b[:i+1]),axis=0)/np.maximum(np.max(abs(b[:i+1]),axis=0),1e-30))))
        seg.append(float(np.max(np.max(abs(a[i-1:i+1]-b[i-1:i+1]),axis=0)/np.maximum(np.max(abs(b[i-1:i+1]),axis=0),1e-30))))
    return dict(all_prefix_max=max(pre),all_segment_max=max(seg),prefix=pre,segment=seg)

def main():
    if OUT.exists():raise FileExistsError(OUT)
    if sha(AUDIT)!=AUDITSHA:raise ValueError('changed failed audit')
    prior=json.loads(old.OUT.read_text())
    if sha(old.OUT)!='b2043bf559fb5aed6b22386183a389062e7b2698bc9e9575083ead6825121f10':raise ValueError('changed assembly')
    if sha(Path(old.__file__))!=prior['producer_sha256']:raise ValueError('changed equations')
    for p,d in prior['dependencies'].items():
        if sha(Path(p))!=d:raise ValueError('changed dependency')
    saved=json.loads(old.linear.old.base.SOURCE.read_text());saved['inherited']=prior['fixed']
    model=old.linear.old.base.Model(saved,1);checks=[];histories=[];comparisons={};error=None;started=time.monotonic()
    def check(name,err,gate):checks.append(dict(name=name,error=float(err),gate=gate,passed=bool(err<=gate)))
    rot=np.array([[0.,-181.3],[181.3,0.]])
    exact=np.array([[math.cos(181.3),-math.sin(181.3)],[math.sin(181.3),math.cos(181.3)]])
    check('exponential_rotation',np.max(abs(expm(rot)-exact)),1e-10)
    nil=np.zeros((3,3));nil[0,1]=1.7;nil[1,2]=-.3
    check('exponential_nilpotent',np.max(abs(expm(nil)-np.eye(3)-nil-nil@nil/2)),1e-10)
    cm=.5-math.sqrt(3)/6;cp=.5+math.sqrt(3)/6
    am=(3-2*math.sqrt(3))/12;ap=(3+2*math.sqrt(3))/12
    x0=math.log(.01)
    try:
        for n in (4096,8192,16384):
            run=old.Assembly(model);y=run.initial(x0);h=-x0/n;snaps=[]
            for i in range(n+1):
                x=x0+i*h
                if i%(n//64)==0:snaps.append(run.values(x,y))
                if i==n:break
                A=run.matrix(x+cm*h);B=run.matrix(x+cp*h)
                y=expm(h*(am*A+ap*B))@expm(h*(ap*A+am*B))@y
                if not np.all(np.isfinite(y)):raise ValueError('nonfinite transfer')
                if time.monotonic()-started>45:raise TimeoutError('45 second serial bound')
            histories.append(dict(steps=n,snapshots=snaps,Einstein_derivative=run.max_constraint))
            print(json.dumps(dict(steps=n,elapsed=time.monotonic()-started,final_delta_b=snaps[-1]['observables'][1])),flush=True)
        for key in ('state','observables'):
            comparisons[key]=errors(histories[-2],histories[-1],key)
            for scope in ('all_prefix_max','all_segment_max'):check(scope+'_'+key,comparisons[key][scope],1e-4)
        check('Einstein_derivative',max(r['Einstein_derivative'] for r in histories),1e-9)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
    result=dict(protocol=__doc__,producer_sha256=sha(Path(__file__)),parent_sha256=sha(old.OUT),failed_audit_sha256=AUDITSHA,
        dependencies={str(p):sha(p) for p in (Path(old.__file__),Path(old.linear.__file__),Path(old.linear.old.__file__))},
        fixed=prior['fixed'],cTheta=.01,width_kpc=20.,preparations=prior['preparations'],
        state_order=prior['state_order'],observable_order=prior['observable_order'],histories=histories,
        comparisons=comparisons,checks=checks,error=error,elapsed_seconds=time.monotonic()-started,
        all_controls_passed=error is None and len(histories)==3 and all(c['passed'] for c in checks),
        selected_native_growing_mode=False,nonlinear_formation=False,observational_superiority=False)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(all_pass=result['all_controls_passed'],checks=checks,error=error,sha256=sha(OUT)),indent=2),flush=True)
    if not result['all_controls_passed']:raise SystemExit(1)

if __name__=='__main__':main()
