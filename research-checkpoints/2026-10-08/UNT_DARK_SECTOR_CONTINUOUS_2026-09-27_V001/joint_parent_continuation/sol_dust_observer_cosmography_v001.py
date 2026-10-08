"""New one-slice dust optics; JSON-only recovery, no old driver execution."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE/'SOL_DUST_OBSERVER_COSMOGRAPHY_V001_RESULT.json'
if OUT.exists():
    raise SystemExit('Refusing overwrite of any prior attempt')
START = time.monotonic()
inputs = {}
def read_saved(name, expected=None):
    raw = (HERE/name).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    inputs[name] = digest
    if expected:
        assert digest == expected, (name, digest)
    return json.loads(raw)

old = read_saved('SOL_REGIONAL_STATE_V001_RESULT.json',
                'a1ef4649fb2e108132bbcc18eb42da5e921918b00e9bfc5574c703294acda9f7')
lapse = read_saved('SOL_REGIONAL_LAPSE_V002_RESULT.json',
                  '5cd1b67d2b74da10f0e179ab5106cab242de5d0f6050d4ac452e1ebc9bace13e')
assert old['status'] == lapse['status'] == 'QUALIFIED'
assert lapse['source_result_sha256'] == inputs['SOL_REGIONAL_STATE_V001_RESULT.json']
assert len(old['rows']) == 30 and old['Fbg'] == 1.75
F, beta = 1.75, .5
checks, rows = [], []
def check(name, value, limit=1e-10):
    value = float(value)
    checks.append(dict(name=name, value=value, limit=limit,
                       passed=bool(math.isfinite(value) and value <= limit)))
def err(x, y):
    return abs(float(x)-float(y))/max(1., abs(float(x)), abs(float(y)))

def grid(nu, nv):
    u, w = np.polynomial.legendre.leggauss(nu)
    phi = 2*math.pi*np.arange(nv)/nv
    ns = np.stack(np.broadcast_arrays(
        np.sqrt(1-u[:, None]**2)*np.cos(phi),
        np.sqrt(1-u[:, None]**2)*np.sin(phi),
        u[:, None]), axis=-1).reshape(-1, 3)
    weights = np.broadcast_to(w[:, None]/(2*nv), (nu, nv)).reshape(-1)
    return ns, weights
grids = [grid(64, 128), grid(128, 256)]

def optics(ki, kip, a, Ciso, ns):
    sq = ns*ns
    hn = sq@ki
    even = -2*a*a*sq[:, 2]+sum(ki)*hn-Ciso+2*(sq@(ki*ki))
    grad = ns[:, 2]*(sq@kip+2*a*((ki[2]-ki[0])*sq[:, 0]
                                +(ki[1]-ki[2])*sq[:, 1]))
    epp = even+grad
    qn = epp/(hn*hn)-3
    return hn, qn, epp, grad

# Exact controls independent of Sol's particular state amplitudes.
axis = np.eye(3)
flat_h, flat_q, _, _ = optics(np.ones(3), np.zeros(3), 0., 1.5, axis)
check('flat_GR_dust_q_half', np.max(abs(flat_q-.5)))
check('flat_GR_dust_H_one', np.max(abs(flat_h-1)))
for ig, (ns, weights) in enumerate(grids):
    check(f'grid{ig}_normalization', abs(sum(weights)-1))
    for i in range(3):
        check(f'grid{ig}_angular_second_{i}', abs(np.dot(weights, ns[:,i]**2)-1/3))
        check(f'grid{ig}_angular_fourth_{i}', abs(np.dot(weights, ns[:,i]**4)-1/5))

for saved in old['rows']:
    r, h = saved['mean_density_over_M2H2'], saved['h']
    for fraction in [0., .5, 1.]:
        t = fraction*saved['t_density_max']
        x = 3*F-r+F*saved['q']*t*t/2
        tag = f"T{saved['trace']}_r{r}_fraction{fraction}"
        state = dict(trace=saved['trace'], r=r, amplitude_fraction=fraction,
                     t=t, a2_over_H2=x, source_endpoint_is_supremum=bool(t>=3))
        if x <= 0:
            state['availability'] = 'CURVATURE_INADMISSIBLE'
            rows.append(state)
            continue
        a = math.sqrt(x)
        k = 2*math.pi*a/saved['aL']
        Cs = (2*F/3)*h*t
        Ds = 2*F*math.sqrt(h*(1-h)/3)*t
        all_min = min(1-math.hypot(t/3-Cs/2, Ds/2), 1-abs(t/3+Cs))
        state['all_phase_all_direction_H_min_over_H'] = all_min
        state['availability'] = 'TRACE_SUPREMUM' if t>=3 else 'ADMITTED_SLICE'
        phase_rows = []
        for j in range(16):
            theta = 2*math.pi*j/16
            u, v = math.cos(theta), math.sin(theta)
            K, Kp = 3+t*u, -k*t*v
            c, e = Cs*u, Ds*v
            cp, ep = -k*Cs*v, k*Ds*u
            ki = np.array([K/3+(-c+e)/2, K/3+(-c-e)/2, K/3+c])
            kip = np.array([Kp/3+(-cp+ep)/2, Kp/3+(-cp-ep)/2, Kp/3+cp])
            rho = r+2*F*t*u+F*saved['A']*t*t*(2*u*u-1)/6
            Ciso = (-2*beta*x+rho)/(2*F)
            sigma2 = float(np.sum((ki-K/3)**2))
            check(tag+f'_p{j}_Hamilton', err(rho, F*K*K/3-x-sigma2/2))
            kdot = np.array([0.,0.,2*x])-K*ki+Ciso
            check(tag+f'_p{j}_trace', err(sum(kdot), -rho/(2*F)-sigma2/F-K*K/3))
            check(tag+f'_p{j}_momentum', abs(cp-a*e-(2*F/3)*Kp)/max(1.,k*t))
            check(tag+f'_p{j}_exact_min', all_min-float(min(ki)))
            prow = dict(phase_index=j, phase=theta, rho_over_M2H2=rho,
                        K_eigenvalues_over_H=ki.tolist(),
                        local_H_min_over_H=float(min(ki)),
                        local_H_max_over_H=float(max(ki)))
            axis_rows = []
            for ia in range(3):
                n = np.zeros((2,3)); n[0,ia]=1; n[1,ia]=-1
                hh, qq, _, _ = optics(ki,kip,a,Ciso,n)
                axis_rows.append(dict(axis=ia+1,H_over_H=float(hh[0]),
                                      q_plus=float(qq[0]) if hh[0]>0 else None,
                                      q_minus=float(qq[1]) if hh[1]>0 else None))
            prow['principal_axes'] = axis_rows
            if abs(rho)<=1e-12:
                prow['availability'] = 'ZERO_OR_UNRESOLVED_DUST_DENSITY'
            elif rho<0:
                prow['availability'] = 'NEGATIVE_DUST_DENSITY'
            elif t>=3:
                prow['availability'] = 'TRACE_SUPREMUM'
            elif min(ki)<=0:
                prow['availability'] = 'NONPOSITIVE_DIRECTIONAL_H'
            else:
                prow['availability'] = 'ELIGIBLE_DUST_OBSERVER'
                results = []
                for ig,(ns,w) in enumerate(grids):
                    hn, qn, epp, grad = optics(ki,kip,a,Ciso,ns)
                    check(tag+f'_p{j}_grid{ig}_Hmoment', err(np.dot(w,hn),K/3))
                    exact_epp = -2*x/3+K*K/3-Ciso+2*float(np.dot(ki,ki))/3
                    check(tag+f'_p{j}_grid{ig}_Eppmoment', err(np.dot(w,epp),exact_epp))
                    check(tag+f'_p{j}_grid{ig}_odd_mean', abs(np.dot(w,grad))/max(1.,abs(exact_epp)))
                    hm,qm,_,gm = optics(ki,kip,a,Ciso,-ns)
                    check(tag+f'_p{j}_grid{ig}_Hparity', np.max(abs(hm-hn))/max(1.,max(abs(hn))))
                    check(tag+f'_p{j}_grid{ig}_qparity', np.max(abs(qn-qm-2*grad/(hn*hn)))/max(1.,max(abs(qn))))
                    invmean = float(np.dot(w,1/hn))
                    heff = 1/invmean
                    qeff = float(np.dot(w,qn/hn))/invmean
                    qmean = float(np.dot(w,qn))
                    qrms = math.sqrt(float(np.dot(w,qn*qn)))
                    even_q = (epp-grad)/(hn*hn)-3
                    check(tag+f'_p{j}_grid{ig}_qeff_odd_cancel', err(qeff,np.dot(w,even_q/hn)/invmean))
                    check(tag+f'_p{j}_grid{ig}_Heff_min', (min(ki)-heff)/max(1.,abs(heff)))
                    check(tag+f'_p{j}_grid{ig}_Heff_max', (heff-max(ki))/max(1.,abs(heff)))
                    if t==0:
                        exact_q = r/(6*F)+(2*x/3)*(1-3*ns[:,2]**2)
                        check(tag+f'_p{j}_grid{ig}_zero_amplitude_direction', np.max(abs(qn-exact_q))/max(1.,max(abs(exact_q))))
                        check(tag+f'_p{j}_grid{ig}_zero_amplitude_monopole', err(qeff,r/(6*F)))
                    results.append(dict(Heff_over_H=heff,qeff=qeff,q_sky_mean=qmean,
                                        q_rms=qrms,q_direction_sample_min=float(min(qn)),
                                        q_direction_sample_max=float(max(qn))))
                for metric in ['Heff_over_H','qeff','q_rms']:
                    check(tag+f'_p{j}_quadrature_{metric}', err(results[0][metric],results[1][metric]),2e-7)
                prow['sky'] = results[1]
                prow['coarse_grid_sky'] = results[0]
            phase_rows.append(prow)
        state['phases'] = phase_rows
        rows.append(state)

eligible = [(s,p) for s in rows for p in s.get('phases',[])
            if p['availability']=='ELIGIBLE_DUST_OBSERVER']
availability = {}
for s in rows:
    for p in s.get('phases',[dict(availability=s['availability'])]):
        key = p['availability']; availability[key] = availability.get(key,0)+1
summary = dict(state_count=len(rows), eligible_observer_count=len(eligible),
               availability_counts=availability,
               negative_qeff_count=sum(p['sky']['qeff']<0 for s,p in eligible),
               qeff_min=min(p['sky']['qeff'] for s,p in eligible),
               qeff_max=max(p['sky']['qeff'] for s,p in eligible),
               low_density_qeff_min=min(p['sky']['qeff'] for s,p in eligible if s['r']<=3),
               low_density_negative_qeff_count=sum(p['sky']['qeff']<0 for s,p in eligible if s['r']<=3))
payload = dict(status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
               scope='local second-order geodesic-dust distance coefficients only',
               inputs=inputs, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               protocol_sha256=hashlib.sha256((HERE/'SOL_DUST_OBSERVER_COSMOGRAPHY_V001.md').read_bytes()).hexdigest(),
               beta=beta,F=F,H_development_km_s_Mpc=100.,
               quadratures=[[64,128],[128,256]],phase_count=16,
               summary=summary,rows=rows,checks=checks,
               passed=sum(c['passed'] for c in checks),total=len(checks),
               elapsed_seconds=time.monotonic()-START)
canonical = json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
receipt = dict(payload=payload,payload_sha256=hashlib.sha256(canonical).hexdigest())
with OUT.open('x') as stream:
    json.dump(receipt,stream,indent=2,allow_nan=False)
print(json.dumps(dict(status=payload['status'],summary=summary,passed=payload['passed'],
                     total=payload['total'],elapsed_seconds=payload['elapsed_seconds'],
                     failed=[c for c in checks if not c['passed']]),indent=2))
