"""New full instantaneous null-screen tide, with magnetic cancellation."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
HERE=Path(__file__).resolve().parent
OUT=HERE/'SOL_NULL_SCREEN_WEYL_V001_RESULT.json'
if OUT.exists(): raise SystemExit('Refusing overwrite')
start=time.monotonic(); inputs={}
def load(name):
    raw=(HERE/name).read_bytes(); inputs[name]=hashlib.sha256(raw).hexdigest()
    doc=json.loads(raw); p=doc['payload']
    assert hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()==doc['payload_sha256']
    return p
focus=load('SOL_AFFINE_RICCI_FOCUSING_V001_RESULT.json')
old=load('SOL_DUST_OBSERVER_COSMOGRAPHY_V001_RESULT.json')
assert focus['status']=='QUALIFIED'
for name,digest in focus['input_hashes'].items():
    assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest; inputs[name]=digest
for name,key in [('sol_affine_ricci_focusing_v001.py','source_sha256'),('SOL_AFFINE_RICCI_FOCUSING_V001.md','protocol_sha256')]:
    digest=hashlib.sha256((HERE/name).read_bytes()).hexdigest(); assert digest==focus[key]; inputs[name]=digest
seeds=json.loads((HERE/'SOL_REGIONAL_STATE_V001_RESULT.json').read_bytes())
u,w=np.polynomial.legendre.leggauss(6); phi=2*math.pi*np.arange(12)/12
ns=np.stack(np.broadcast_arrays(np.sqrt(1-u[:,None]**2)*np.cos(phi),np.sqrt(1-u[:,None]**2)*np.sin(phi),u[:,None]),axis=-1).reshape(-1,3)
weights=np.broadcast_to(w[:,None]/24,(6,12)).reshape(-1)
Ps=np.eye(3)[None,:,:]-ns[:,:,None]*ns[:,None,:]
checks,rows=[],[]
def err(x,y): return abs(float(x)-float(y))/max(1.,abs(float(x)),abs(float(y)))
def check(name,value):
    value=float(value); checks.append(dict(name=name,value=value,limit=1e-10,passed=bool(math.isfinite(value) and value<=1e-10)))
beta,F=old['beta'],old['F']
for state in old['rows']:
    if 'phases' not in state: continue
    seed=next(s for s in seeds['rows'] if s['trace']==state['trace'] and s['mean_density_over_M2H2']==state['r'])
    x=state['a2_over_H2']; a=math.sqrt(x); t=state['t']; k=2*math.pi*a/seed['aL']
    Cs=2*F*seed['h']*t/3; Ds=2*F*math.sqrt(seed['h']*(1-seed['h'])/3)*t
    for p in state['phases']:
        if p['availability']!='ELIGIBLE_DUST_OBSERVER': continue
        j=p['phase_index']; theta=p['phase']; co,si=math.cos(theta),math.sin(theta)
        ki=np.array(p['K_eigenvalues_over_H']); K=sum(ki); sigma=ki-K/3
        Kp=-k*t*si; cp=-k*Cs*si; ep=k*Ds*co
        kip=np.array([Kp/3+(-cp+ep)/2,Kp/3+(-cp-ep)/2,Kp/3+cp])
        curvature=np.array([0.,0.,-2*x]); rawE=curvature+K*ki-ki*ki
        Ei=rawE-np.mean(rawE)
        Ei2=curvature-np.mean(curvature)+(K/3)*sigma-(sigma*sigma-np.mean(sigma*sigma))
        E=np.diag(Ei); E2=float(np.dot(Ei,Ei)); scale=max(1.,math.sqrt(E2))
        tag=f"T{state['trace']}_r{state['r']}_fraction{state['amplitude_fraction']}_p{j}"
        check(tag+'_E_two_forms',np.max(abs(Ei-Ei2))/scale)
        check(tag+'_trace_E',abs(sum(Ei))/scale)
        curl12=a*(ki[1]-ki[2])-kip[1]
        curl21=kip[0]+a*(ki[0]-ki[2])
        magnetic=(curl12+curl21)/2
        check(tag+'_magnetic_zero',abs(magnetic)/max(1.,abs(curl12),abs(curl21)))
        check(tag+'_magnetic_independent',err(magnetic,(ep-3*a*Cs*co)/2))
        check(tag+'_curl_Codazzi',err(curl12-curl21,beta*Kp))
        check(tag+'_minimum_shear_cancellation',err(k*Ds,3*a*Cs))
        Enn=(ns*ns)@Ei
        CC=2*(Ps@E@Ps)+Enn[:,None,None]*Ps
        norms=np.einsum('nij,nji->n',CC,CC)
        norm_exact=4*E2-8*((ns*ns)@(Ei*Ei))+2*Enn*Enn
        check(tag+'_screen_norm_formula',np.max(abs(norms-norm_exact))/max(1.,E2))
        check(tag+'_screen_trace',np.max(abs(np.trace(CC,axis1=1,axis2=2)))/scale)
        check(tag+'_screen_null_projection',np.max(abs(np.einsum('nij,nj->ni',CC,ns)))/scale)
        check(tag+'_sky_screen_norm',err(np.dot(weights,norms),8*E2/5))
        amplitude=float(max(Ei)-min(Ei))
        check(tag+'_all_direction_max_bound',(float(max(norms))/2-amplitude*amplitude)/max(1.,E2))
        axis_amplitudes=[]
        for ia in range(3):
            remaining=[i for i in range(3) if i!=ia]
            axis_amplitudes.append(abs(float(Ei[remaining[0]]-Ei[remaining[1]])))
        check(tag+'_max_axis_attainment',err(max(axis_amplitudes),amplitude))
        fr=next(fr for fr in focus['rows'] if fr['trace']==state['trace'] and fr['r']==state['r'] and fr['amplitude_fraction']==state['amplitude_fraction'] and fr['phase_index']==j)
        Rll=fr['ricci_monopole_over_H2']+fr['ricci_dipole_over_H2']*ns[:,2]
        total=CC+(Rll/2)[:,None,None]*Ps
        check(tag+'_total_screen_trace',np.max(abs(np.trace(total,axis1=1,axis2=2)-Rll))/max(1.,scale,max(abs(Rll))))
        # The projection and electric contraction depend only on n n^T.
        minusP=np.eye(3)[None,:,:]-(-ns)[:,:,None]*(-ns)[:,None,:]
        minusCC=2*(minusP@E@minusP)+Enn[:,None,None]*minusP
        check(tag+'_antipodal_Weyl',np.max(abs(minusCC-CC))/scale)
        if t==0:
            check(tag+'_zero_E',np.max(abs(Ei-np.array([2*x/3,2*x/3,-4*x/3])))/scale)
            check(tag+'_zero_screen_amplitude',np.max(abs(norms/2-(2*x*(1-ns[:,2]**2))**2))/max(1.,E2))
            check(tag+'_zero_q_RMS',err(p['sky']['q_rms']**2,(state['r']/(6*F))**2+16*x*x/45))
        rows.append(dict(trace=state['trace'],r=state['r'],amplitude_fraction=state['amplitude_fraction'],phase_index=j,
                         electric_Weyl_eigenvalues_over_H2=Ei.tolist(),magnetic_Weyl_12_over_H2=magnetic,
                         electric_norm_squared_over_H4=E2,sky_screen_norm_squared_over_H4=8*E2/5,
                         max_screen_Weyl_eigenvalue_magnitude_over_H2=amplitude,
                         max_leading_normalized_image_shear_coefficient_over_H2=amplitude/6,
                         Ricll_min_over_H2=fr['ricci_min_over_H2'],Ricll_max_over_H2=fr['ricci_max_over_H2']))
assert len(rows)==1139
summary=dict(eligible_phases=len(rows),magnetic_zero_qualified=True,
             clean_interior=next(r for r in rows if r['trace']==3 and r['r']==.15 and r['amplitude_fraction']==.5 and r['phase_index']==8))
payload=dict(status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
             scope='full instantaneous optical tide and leading local image shear, no integrated observed lensing',
             input_hashes=inputs,summary=summary,rows=rows,checks=checks,
             passed=sum(c['passed'] for c in checks),total=len(checks),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             protocol_sha256=hashlib.sha256((HERE/'SOL_NULL_SCREEN_WEYL_V001.md').read_bytes()).hexdigest(),
             elapsed_seconds=time.monotonic()-start)
canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
with OUT.open('x') as stream:
    json.dump(dict(payload=payload,payload_sha256=hashlib.sha256(canonical).hexdigest()),stream,indent=2,allow_nan=False)
print(json.dumps(dict(status=payload['status'],passed=payload['passed'],total=payload['total'],elapsed_seconds=payload['elapsed_seconds'],summary=summary,failed=[c for c in checks if not c['passed']]),indent=2))
