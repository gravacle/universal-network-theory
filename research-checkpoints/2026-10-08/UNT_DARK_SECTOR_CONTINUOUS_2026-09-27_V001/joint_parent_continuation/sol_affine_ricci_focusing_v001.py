"""Exact new affine Ricci monopole/dipole on saved eligible dust phases."""
from pathlib import Path
import hashlib
import json
import math
import time
HERE=Path(__file__).resolve().parent
OUT=HERE/'SOL_AFFINE_RICCI_FOCUSING_V001_RESULT.json'
if OUT.exists(): raise SystemExit('Refusing overwrite')
start=time.monotonic(); input_hashes={}
def load_receipt(name):
    raw=(HERE/name).read_bytes(); input_hashes[name]=hashlib.sha256(raw).hexdigest()
    doc=json.loads(raw); p=doc['payload']
    canonical=json.dumps(p,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    assert hashlib.sha256(canonical).hexdigest()==doc['payload_sha256']
    return p
old=load_receipt('SOL_DUST_OBSERVER_COSMOGRAPHY_V001_RESULT.json')
repair=load_receipt('SOL_DUST_OBSERVER_COSMOGRAPHY_V002_REPAIR_RESULT.json')
assert old['status']=='FAILED' and repair['status']=='QUALIFIED'
assert repair['original_raw_sha256']==input_hashes['SOL_DUST_OBSERVER_COSMOGRAPHY_V001_RESULT.json']
for name,digest in old['inputs'].items():
    raw=(HERE/name).read_bytes(); assert hashlib.sha256(raw).hexdigest()==digest
    input_hashes[name]=digest
for obj,source,protocol in [(old,'sol_dust_observer_cosmography_v001.py','SOL_DUST_OBSERVER_COSMOGRAPHY_V001.md'),
                            (repair,'sol_dust_observer_cosmography_v002_repair.py','SOL_DUST_OBSERVER_COSMOGRAPHY_V002_REPAIR.md')]:
    for name,key in [(source,'source_sha256'),(protocol,'protocol_sha256')]:
        digest=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        assert digest==obj[key]; input_hashes[name]=digest
assert all(c['passed'] for c in repair['checks'])
assert all(c['passed'] for c in old['checks'] if c['name'] not in repair['replaced_gate_names'])
seeds=json.loads((HERE/'SOL_REGIONAL_STATE_V001_RESULT.json').read_bytes())
beta,F=old['beta'],old['F']; checks,rows=[],[]
def err(x,y): return abs(x-y)/max(1.,abs(x),abs(y))
def check(name,value):
    checks.append(dict(name=name,value=float(value),limit=1e-10,
                       passed=bool(math.isfinite(value) and value<=1e-10)))
check('flat_GR_dust_Rll',err(0+9-3-2*1.5,3))
for r in [.15,.3,1.,3.]:
    # beta0, F1, Sol isotropic K=3, curvature x=3-r.
    xgr=3-r; Cgr=r/2
    check(f'curved_GR_r{r}_Rll',err(-2*xgr+9-3-2*Cgr,r))
    x=3*F-r; C=(-2*beta*x+r)/(2*F)
    check(f't0_r{r}_Ricll',err(-2*x+9-3-2*C,-3*beta+(1+beta)*r/F))
for state in old['rows']:
    if 'phases' not in state: continue
    seed=next(s for s in seeds['rows'] if s['trace']==state['trace'] and s['mean_density_over_M2H2']==state['r'])
    x=state['a2_over_H2']; a=math.sqrt(x); t=state['t']
    k=2*math.pi*a/seed['aL']; Cs=(2*F/3)*seed['h']*t
    Ds=2*F*math.sqrt(seed['h']*(1-seed['h'])/3)*t
    for p in state['phases']:
        if p['availability']!='ELIGIBLE_DUST_OBSERVER': continue
        j=p['phase_index']; theta=p['phase']; u,v=math.cos(theta),math.sin(theta)
        rho=p['rho_over_M2H2']; ki=p['K_eigenvalues_over_H']; K=sum(ki)
        C=(-2*beta*x+rho)/(2*F); trk2=sum(z*z for z in ki)
        P=-2*x+K*K-trk2-2*C; Kp=-k*t*v; B=-2*beta*Kp
        constrained=(1+3*beta)*rho/F-beta*K*K+2*beta*x/F
        poly=-3*beta+(1+beta)*state['r']/F+2*t*u+t*t*(beta*seed['q']-(1+3*beta)*seed['A']/6+((1+3*beta)*seed['A']/3-beta)*u*u)
        tag=f"T{state['trace']}_r{state['r']}_fraction{state['amplitude_fraction']}_p{j}"
        check(tag+'_Hamiltonian_Rll',err(P,constrained))
        check(tag+'_phase_polynomial_Rll',err(P,poly))
        divK=Kp/3-k*Cs*v-a*Ds*v
        check(tag+'_Codazzi',err(divK-Kp,beta*Kp))
        values=[P,P,P,P,P+B,P-B]
        check(tag+'_six_axes_mean',err(sum(values)/6,P))
        check(tag+'_six_axes_square',err(sum(z*z for z in values)/6,P*P+B*B/3))
        check(tag+'_antipodal',err((values[4]+values[5])/2,P))
        minimum,maximum=P-abs(B),P+abs(B)
        check(tag+'_min_max',max(minimum-min(values),max(values)-maximum))
        fraction=max(0.,min(1.,(abs(B)-P)/(2*abs(B)))) if B!=0 else (1. if P<0 else 0.)
        check(tag+'_fraction_range',max(-fraction,fraction-1))
        sigma2=trk2-K*K/3
        Ruu=rho/(2*F)+sigma2/F+K*K/3-trk2
        if t==0:
            check(tag+'_zero_amplitude_Rll',err(P,-3*beta+(1+beta)*state['r']/F))
            check(tag+'_zero_amplitude_Ruu',err(Ruu,state['r']/(2*F)))
        rows.append(dict(trace=state['trace'],r=state['r'],amplitude_fraction=state['amplitude_fraction'],
                         phase_index=j,rho_over_M2H2=rho,ricci_monopole_over_H2=P,
                         ricci_dipole_over_H2=B,ricci_min_over_H2=minimum,ricci_max_over_H2=maximum,
                         defocusing_sky_fraction=fraction,timelike_Ruu_over_H2=Ruu,
                         DA_affine_cubic_min_over_H2=-maximum/12,
                         DA_affine_cubic_max_over_H2=-minimum/12))
assert len(rows)==old['summary']['eligible_observer_count']==1139
summary=dict(eligible_phases=len(rows),all_direction_defocusing_count=sum(r['ricci_max_over_H2']<0 for r in rows),
             some_direction_defocusing_count=sum(r['ricci_min_over_H2']<0 for r in rows),
             zero_amplitude_low_r_null_defocusing_ceiling=3*beta*F/(1+beta),
             clean_interior=next(r for r in rows if r['trace']==3 and r['r']==.15 and r['amplitude_fraction']==.5 and r['phase_index']==8))
payload=dict(status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
             scope='local affine cubic area coefficient and metric null convergence only',
             beta=beta,F=F,input_hashes=input_hashes,summary=summary,rows=rows,checks=checks,
             passed=sum(c['passed'] for c in checks),total=len(checks),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             protocol_sha256=hashlib.sha256((HERE/'SOL_AFFINE_RICCI_FOCUSING_V001.md').read_bytes()).hexdigest(),
             elapsed_seconds=time.monotonic()-start)
canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
with OUT.open('x') as stream:
    json.dump(dict(payload=payload,payload_sha256=hashlib.sha256(canonical).hexdigest()),stream,indent=2,allow_nan=False)
print(json.dumps(dict(status=payload['status'],passed=payload['passed'],total=payload['total'],
                     elapsed_seconds=payload['elapsed_seconds'],summary=summary,
                     failed=[c for c in checks if not c['passed']]),indent=2))
