"""New constrained GR coefficients; retain the existing UNT half states."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
HERE=Path(__file__).resolve().parent
OUT=HERE/'SOL_GR_MATCHED_COSMOGRAPHY_V001_RESULT.json'
if OUT.exists(): raise SystemExit('Refusing overwrite')
start=time.monotonic(); inputs={}
def receipt(name):
    raw=(HERE/name).read_bytes(); inputs[name]=hashlib.sha256(raw).hexdigest()
    d=json.loads(raw); p=d['payload']
    assert hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==d['payload_sha256']
    return p
old=receipt('SOL_DUST_OBSERVER_COSMOGRAPHY_V001_RESULT.json')
repair=receipt('SOL_DUST_OBSERVER_COSMOGRAPHY_V002_REPAIR_RESULT.json')
assert repair['status']=='QUALIFIED' and repair['original_raw_sha256']==inputs['SOL_DUST_OBSERVER_COSMOGRAPHY_V001_RESULT.json']
assert all(c['passed'] for c in repair['checks'])
assert all(c['passed'] for c in old['checks'] if c['name'] not in repair['replaced_gate_names'])
for name,digest in old['inputs'].items():
    assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest
    inputs[name]=digest
for name,key in [('sol_dust_observer_cosmography_v001.py','source_sha256'),
                 ('SOL_DUST_OBSERVER_COSMOGRAPHY_V001.md','protocol_sha256')]:
    assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==old[key]
    inputs[name]=old[key]
seeds=json.loads((HERE/'SOL_REGIONAL_STATE_V001_RESULT.json').read_bytes())
checks,states,pairs=[],[],[]
def err(x,y): return abs(float(x)-float(y))/max(1.,abs(float(x)),abs(float(y)))
def check(name,val,limit=1e-10):
    val=float(val); checks.append(dict(name=name,value=val,limit=limit,passed=bool(math.isfinite(val) and val<=limit)))
def grid(nu,nv):
    u,w=np.polynomial.legendre.leggauss(nu); phi=2*math.pi*np.arange(nv)/nv
    ns=np.stack(np.broadcast_arrays(np.sqrt(1-u[:,None]**2)*np.cos(phi),
                np.sqrt(1-u[:,None]**2)*np.sin(phi),u[:,None]),axis=-1).reshape(-1,3)
    weights=np.broadcast_to(w[:,None]/(2*nv),(nu,nv)).reshape(-1)
    return ns,weights
grids=[grid(64,128),grid(128,256)]
for seed in seeds['rows']:
    trace,r,h=seed['trace'],seed['mean_density_over_M2H2'],seed['h']
    oldstate=next(s for s in old['rows'] if s['trace']==trace and s['r']==r and s['amplitude_fraction']==.5)
    t=oldstate['t']; q=(1-h)/3; A=1+h-2*h*h
    x=3-r+q*t*t/2; tag=f'T{trace}_r{r}'
    state=dict(trace=trace,r=r,t=t,GR_a2_over_H2=x,UNT_a2_over_H2=oldstate['a2_over_H2'])
    candidate_u=[-1.,1.]
    if A>0 and t>0 and abs(-3/(A*t))<1: candidate_u.append(-3/(A*t))
    density_min=min(r+2*t*u+A*t*t*(2*u*u-1)/6 for u in candidate_u)
    state['GR_exact_all_phase_density_min']=density_min
    if x<=0:
        state['availability']='GR_CURVATURE_INADMISSIBLE'; states.append(state); continue
    a=math.sqrt(x); k=2*math.pi*a/seed['aL']
    Cs=2*h*t/3; Ds=2*math.sqrt(h*(1-h)/3)*t
    state['GR_all_phase_all_direction_Hmin']=min(1-math.hypot(t/3-Cs/2,Ds/2),1-abs(t/3+Cs))
    state['phases']=[]
    for j in range(16):
        theta=2*math.pi*j/16; u,v=math.cos(theta),math.sin(theta)
        K=3+t*u; Kp=-k*t*v; c,e=Cs*u,Ds*v; cp,ep=-k*Cs*v,k*Ds*u
        ki=np.array([K/3+(-c+e)/2,K/3+(-c-e)/2,K/3+c])
        kip=np.array([Kp/3+(-cp+ep)/2,Kp/3+(-cp-ep)/2,Kp/3+cp])
        rho=r+2*t*u+A*t*t*(2*u*u-1)/6; C=rho/2
        sigma2=float(np.sum((ki-K/3)**2)); trk2=float(np.dot(ki,ki))
        check(tag+f'_p{j}_Hamilton',err(rho,K*K/3-x-sigma2/2))
        check(tag+f'_p{j}_trace',err(2*x-K*K+3*C,-rho/2-sigma2-K*K/3))
        check(tag+f'_p{j}_momentum',abs(cp-a*e-2*Kp/3)/max(1.,k*t))
        Ricll=-2*x+K*K-trk2-2*C
        check(tag+f'_p{j}_GR_null_dust',err(Ricll,rho))
        p=dict(phase_index=j,rho_over_M2H2=rho,K_eigenvalues_over_H=ki.tolist(),Ricll_over_H2=Ricll)
        op=next((p for p in oldstate.get('phases',[]) if p['phase_index']==j),None)
        if abs(rho)<=1e-12: p['availability']='GR_ZERO_OR_UNRESOLVED_DUST'
        elif rho<0: p['availability']='GR_NEGATIVE_DUST'
        elif min(ki)<=0: p['availability']='GR_NONPOSITIVE_DIRECTIONAL_H'
        elif not op or op['availability']!='ELIGIBLE_DUST_OBSERVER': p['availability']='UNT_UNAVAILABLE'
        else:
            p['availability']='PAIRED_ELIGIBLE'
            results=[]
            for ig,(ns,w) in enumerate(grids):
                sq=ns*ns; hn=sq@ki
                grad=ns[:,2]*(sq@kip+2*a*((ki[2]-ki[0])*sq[:,0]+(ki[1]-ki[2])*sq[:,1]))
                even=-2*x*sq[:,2]+K*hn-C+2*(sq@(ki*ki))
                epp=even+grad; qn=epp/hn**2-3
                invmean=float(np.dot(w,1/hn)); heff=1/invmean
                qeff=float(np.dot(w,qn/hn))/invmean
                qrms=math.sqrt(float(np.dot(w,qn*qn)))
                check(tag+f'_p{j}_grid{ig}_Hmoment',err(np.dot(w,hn),K/3))
                check(tag+f'_p{j}_grid{ig}_Eppmoment',err(np.dot(w,epp),-2*x/3+K*K/3-C+2*trk2/3))
                check(tag+f'_p{j}_grid{ig}_antipodal_cancel',abs(np.dot(w,grad/hn**3))/max(1.,abs(qeff*invmean)))
                check(tag+f'_p{j}_grid{ig}_Heff_bounds',max(min(ki)-heff,heff-max(ki))/max(1.,abs(heff)))
                results.append(dict(Heff_over_H=heff,qeff=qeff,q_rms=qrms))
            for metric in ['Heff_over_H','qeff','q_rms']:
                check(tag+f'_p{j}_quadrature_{metric}',err(results[0][metric],results[1][metric]),2e-7)
            p['GR_sky']=results[1]; p['GR_coarse_sky']=results[0]; p['UNT_saved_sky']=op['sky']
            pairs.append(dict(trace=trace,r=r,phase_index=j,t=t,
                              GR_rho=rho,UNT_rho=op['rho_over_M2H2'],
                              GR_Hmin=float(min(ki)),UNT_Hmin=op['local_H_min_over_H'],
                              GR_qeff=results[1]['qeff'],UNT_qeff=op['sky']['qeff'],
                              GR_q_rms=qrms,UNT_q_rms=op['sky']['q_rms'],GR_Ricll=Ricll))
        state['phases'].append(p)
    states.append(state)
summary=dict(state_count=len(states),paired_observer_count=len(pairs),
             unavailable_GR_curvature_states=sum(s['availability']=='GR_CURVATURE_INADMISSIBLE' for s in states if 'availability' in s),
             GR_negative_qeff_count=sum(p['GR_qeff']<0 for p in pairs),
             UNT_negative_qeff_count=sum(p['UNT_qeff']<0 for p in pairs),
             both_negative_count=sum(p['GR_qeff']<0 and p['UNT_qeff']<0 for p in pairs),
             clean_interior=next(p for p in pairs if p['trace']==3 and p['r']==.15 and p['phase_index']==8))
payload=dict(status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
             scope='matched construction rule on constrained one-slice GR versus beta.5, not observed or joint likelihood',
             inputs=inputs,summary=summary,states=states,paired_rows=pairs,checks=checks,
             passed=sum(c['passed'] for c in checks),total=len(checks),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             protocol_sha256=hashlib.sha256((HERE/'SOL_GR_MATCHED_COSMOGRAPHY_V001.md').read_bytes()).hexdigest(),
             elapsed_seconds=time.monotonic()-start)
canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
with OUT.open('x') as stream:
    json.dump(dict(payload=payload,payload_sha256=hashlib.sha256(canonical).hexdigest()),stream,indent=2,allow_nan=False)
print(json.dumps(dict(status=payload['status'],passed=payload['passed'],total=payload['total'],
                     elapsed_seconds=payload['elapsed_seconds'],summary=summary,
                     failed=[c for c in checks if not c['passed']]),indent=2))
