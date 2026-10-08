"""Post-run saved-state audit plus one independent velocity-Verlet control."""
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np

ROOT=Path(__file__).resolve().parent
INPUT=ROOT/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json'
FREEZE=ROOT/'COMMON_HISTORY_MECHANISM_V001_FROZEN.json'
count=0
worst=0.


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a,b,scale=1.,tol=2e-10):
    global count,worst
    err=abs(a-b)/scale
    assert math.isfinite(err) and err<=tol,(a,b,err)
    count+=1;worst=max(worst,err)


def root_bisection(delta,h):
    lo=np.zeros_like(delta);hi=np.ones_like(delta)
    assert np.all(hi**3+delta**2*hi>=delta*h)
    for _ in range(70):
        mid=(lo+hi)/2
        low=mid**3+delta**2*mid<delta*h
        lo=np.where(low,mid,lo);hi=np.where(low,hi,mid)
    return (lo+hi)/2


def state(delta,weights,kb,g,gs,y,v):
    h=g/math.sqrt(1+(g/gs)**2);hp=(1+(g/gs)**2)**-1.5
    B=math.fsum(float(w*d*q) for w,d,q in zip(weights,delta,y))
    kin=math.fsum(float(w*p*p/2) for w,p in zip(weights,v))
    energy=kb*g*g/2+math.fsum(float(w*(p*p/2+d*d*q*q/2+q**4/4))
        for w,d,q,p in zip(weights,delta,y,v))-h*B
    return dict(B=B,kinetic=kin,energy=energy,D=g-hp*B/kb)


def bump_values(times,T):
    # Independent 128-node integral, with explicit endpoints and no production import.
    z,w=np.polynomial.legendre.leggauss(128);v=(z+1)/2;w=w/2
    norm=math.fsum(float(a*math.exp(-1/(b*(1-b)))) for a,b in zip(w,v))
    result=np.zeros_like(times)
    inside=(times>0)&(times<T)
    s=times[inside]/T
    u=s[:,None]*v[None,:]
    result[inside]=s*np.sum(w[None,:]*np.exp(-1/(u*(1-u))),axis=1)/norm
    result[times>=T]=1.
    return result


def verlet(case,gs,dt):
    delta=np.asarray(case['delta']);weights=np.asarray(case['weights']);kb=case['Kb']
    G=.04;T=8.;end=24.;n=round(end/dt)
    times=np.arange(n+1)*dt;g=G*bump_values(times,T);h=g/np.sqrt(1+(g/gs)**2)
    hp=(1+(g/gs)**2)**-1.5
    y=np.zeros_like(delta);v=np.zeros_like(delta);a=delta*h[0]
    force=kb*g[0]-hp[0]*np.sum(weights*delta*y);work=0.
    snapshots=[];wanted={round(t/dt) for t in (8.,16.,24.)}
    started=time.perf_counter()
    for i in range(n):
        half=v+a*dt/2
        y=y+half*dt
        next_a=delta*h[i+1]-delta**2*y-y**3
        v=half+next_a*dt/2
        next_force=kb*g[i+1]-hp[i+1]*np.sum(weights*delta*y)
        work+=(force+next_force)*(g[i+1]-g[i])/2
        a=next_a;force=next_force
        if i+1 in wanted:
            out=state(delta,weights,kb,G,gs,y,v)
            out.update(time=float(times[i+1]),hold=float(times[i+1]-T),work=float(work),
                y=y.tolist(),v=v.tolist())
            snapshots.append(out)
    return dict(integrator='independently implemented velocity Verlet',G=G,T=T,
        gap=case['gap'],order=case['order'],dt=dt,seconds=time.perf_counter()-started,
        work_rule='Trapezoidal F dg; no production RK stages or ramp routine reused.',
        observations=snapshots)


def main():
    f=json.loads(FREEZE.read_text())
    for name,digest in f['files'].items():assert sha(ROOT/name)==digest,name
    wrapper=json.loads(INPUT.read_text())
    assert wrapper['freeze_sha256']==sha(FREEZE)
    raw=json.dumps(wrapper['payload'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    assert hashlib.sha256(raw).hexdigest()==wrapper['payload_sha256']
    p=wrapper['payload'];assert all(p['checks'].values())
    a0=p['parameters']['a0_internal'];gs=p['parameters']['gs_internal']
    assert len(p['cases'])==12
    expected={(gap,T,n,dt) for gap in (.001,.002) for T in (8,16)
        for n,dt in ((64,.01),(128,.01),(128,.005))}
    assert {(c['gap'],c['duration'],c['order'],c['dt']) for c in p['cases']}==expected
    main_rows=[];cutoff={}
    fullnodes,fullweights=np.polynomial.legendre.leggauss(256)
    full_delta=(fullnodes+1)/2;full_weights=fullweights*full_delta/2
    for case in p['cases']:
        gap=case['gap'];delta=np.array(case['delta']);weights=np.array(case['weights'])
        kb=(1-gap*gap)/2;close(case['Kb'],kb,tol=0.)
        assert np.all(delta>gap) and np.all(delta<1) and np.all(weights>0)
        assert len(delta)==case['order'] and len(case['observations'])==9
        assert all(case['checks'].values())
        for degree in range(7):
            close(math.fsum(float(w*d**degree) for w,d in zip(weights,delta)),
                (1-gap**(degree+2))/(degree+2),tol=2e-14)
        for i,G in enumerate((.0025,.01,.04)):
            h=G/math.sqrt(1+(G/gs)**2)
            eq=root_bisection(delta,h)
            relaxed=state(delta,weights,kb,G,gs,eq,np.zeros_like(eq))
            full_eq=root_bisection(full_delta,h)
            full=state(full_delta,full_weights,.5,G,gs,full_eq,np.zeros_like(full_eq))
            close((relaxed['D']-full['D'])/G,
                case['relaxed_force_difference_from_full_band_over_g'][i],tol=2e-12)
            for hold in (0,8,16):
                saved=[r for r in case['observations'] if abs(r['g_over_a0']*a0-G)<1e-16 and r['hold']==hold]
                assert len(saved)==1
                r=saved[0];close(r['time'],case['duration']+hold,tol=0.)
                y=np.array(r['y']);v=np.array(r['v'])
                assert len(y)==len(v)==case['order']
                s=state(delta,weights,kb,G,gs,y,v)
                for key in ('B','kinetic','energy','D'):
                    close(s[key],r[key],scale=G if key in ('D','B') else kb*G*G)
                close(relaxed['D'],r['D_relaxed'],scale=G)
                close(relaxed['energy'],r['relaxed_energy'],scale=kb*G*G)
                exc=s['energy']-relaxed['energy']
                close(exc,r['excitation'],scale=kb*G*G)
                close(s['energy'],r['work'],scale=kb*G*G,tol=2e-7)
                close(s['D']/G,r['D_over_g'])
                close((s['D']-relaxed['D'])/G,r['signed_departure_over_g'])
                assert exc>=-2e-7*kb*G*G and exc<=kb*h*h/2*(1+2e-7)
                assert abs(s['D']-relaxed['D'])<=h*(1+(G/gs)**2)**-1.5*(1+2e-7)
                if case['order']==128 and case['dt']==.005:
                    cutoff[(gap,case['duration'],G,hold)]=s['D']/G
                    if gap==.001:main_rows.append(dict(G=G,T=case['duration'],hold=hold,
                        D_over_G=s['D']/G,relaxed_D_over_G=relaxed['D']/G,
                        signed_departure_over_G=(s['D']-relaxed['D'])/G))
    representative=next(c for c in p['cases'] if(c['gap'],c['duration'],c['order'],c['dt'])==(.001,8,128,.005))
    independent=[verlet(representative,gs,dt) for dt in (.0025,.00125)]
    comparisons=[]
    for left,right in zip(independent[0]['observations'],independent[1]['observations']):
        r=next(s for s in representative['observations'] if s['hold']==left['hold'] and abs(s['g_over_a0']*a0-.04)<1e-16)
        scales={'D':.04,'energy':representative['Kb']*.04**2,'work':representative['Kb']*.04**2}
        errors={key:{'coarse_scaled_error':abs(left[key]-r[key])/scale,
            'fine_scaled_error':abs(right[key]-r[key])/scale,
            'richardson_scaled_error':abs((4*right[key]-left[key])/3-r[key])/scale}
            for key,scale in scales.items()}
        assert all(e['fine_scaled_error']<2e-6 for e in errors.values())
        comparisons.append(dict(hold=r['hold'],errors=errors,
            maximum_fine_y_difference=float(np.max(abs(np.asarray(right['y'])-np.asarray(r['y'])))),
            maximum_fine_v_difference=float(np.max(abs(np.asarray(right['v'])-np.asarray(r['v']))))))
    result=dict(role='Independent post-existing-result audit, not a new native or galaxy prediction.',
        source_sha256=sha(Path(__file__)),input_sha256=sha(INPUT),freeze_sha256=sha(FREEZE),
        saved_state_count=108,arithmetic_comparisons=count,maximum_scaled_arithmetic_residual=worst,
        main_observations=main_rows,independent_integrations=independent,integrator_comparisons=comparisons,
        maximum_cutoff_change_in_D_over_G=max(abs(cutoff[(.001,T,G,H)]-cutoff[(.002,T,G,H)])
            for T in (8,16) for G in (.0025,.01,.04) for H in (0,8,16)))
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))


if __name__=='__main__':main()
