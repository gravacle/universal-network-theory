"""Only angular repair of two saved observer rows; retain failed V001."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE/'SOL_DUST_OBSERVER_COSMOGRAPHY_V002_REPAIR_RESULT.json'
if OUT.exists(): raise SystemExit('Refusing overwrite')
start=time.monotonic()
raw=(HERE/'SOL_DUST_OBSERVER_COSMOGRAPHY_V001_RESULT.json').read_bytes()
receipt=json.loads(raw); old=receipt['payload']
canonical=json.dumps(old,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
assert hashlib.sha256(canonical).hexdigest()==receipt['payload_sha256']
assert old['status']=='FAILED'
for name,digest in old['inputs'].items():
    assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest
assert hashlib.sha256((HERE/'sol_dust_observer_cosmography_v001.py').read_bytes()).hexdigest()==old['source_sha256']
assert hashlib.sha256((HERE/'SOL_DUST_OBSERVER_COSMOGRAPHY_V001.md').read_bytes()).hexdigest()==old['protocol_sha256']
expected=[f'T1000000_r7.0_fraction1.0_p{j}_quadrature_{metric}'
          for j in [7,9] for metric in ['qeff','q_rms']]
assert sorted(c['name'] for c in old['checks'] if not c['passed'])==sorted(expected)
states=json.loads((HERE/'SOL_REGIONAL_STATE_V001_RESULT.json').read_bytes())
source=next(s for s in states['rows'] if s['trace']==1000000 and s['mean_density_over_M2H2']==7)
state=next(s for s in old['rows'] if s['trace']==1000000 and s['r']==7 and s['amplitude_fraction']==1)
F,beta=old['F'],old['beta']
a=math.sqrt(state['a2_over_H2']); x=a*a; t=state['t']; h=source['h']
k=2*math.pi*a/source['aL']
Cs=(2*F/3)*h*t; Ds=2*F*math.sqrt(h*(1-h)/3)*t
checks,refined=[],[]
def check(name,value,limit=1e-10):
    value=float(value)
    checks.append(dict(name=name,value=value,limit=limit,
                       passed=bool(math.isfinite(value) and value<=limit)))
def err(a,b): return abs(float(a)-float(b))/max(1.,abs(float(a)),abs(float(b)))

for j in [7,9]:
    p=next(p for p in state['phases'] if p['phase_index']==j)
    theta=p['phase']; u,v=math.cos(theta),math.sin(theta)
    ki=np.array(p['K_eigenvalues_over_H']); K=sum(ki)
    kp=-k*t*v; cp=-k*Cs*v; ep=k*Ds*u
    kip=np.array([kp/3+(-cp+ep)/2,kp/3+(-cp-ep)/2,kp/3+cp])
    Ciso=(-2*beta*x+p['rho_over_M2H2'])/(2*F)
    b1=kip[0]+2*a*(ki[2]-ki[0])
    b2=kip[1]+2*a*(ki[1]-ki[2]); b3=kip[2]
    def azimuth(mu):
        transverse=1-mu*mu
        A=(ki[0]+ki[1])*transverse/2+ki[2]*mu*mu
        B=(ki[0]-ki[1])*transverse/2
        D=(A-B)*(A+B)
        I1=D**(-.5); I2=A*D**(-1.5)
        I3=(2*A*A+B*B)/(2*D**2.5)
        I4=A*(2*A*A+3*B*B)/(2*D**3.5)
        J2=-B/D**1.5; J3=-3*A*B/(2*D**2.5)
        J4=-B*(4*A*A+B*B)/(2*D**3.5)
        T4=A*(A*A+4*B*B)/(2*D**3.5)
        L=-2*x*mu*mu+K*A-Ciso+(ki[0]**2+ki[1]**2)*transverse+2*ki[2]**2*mu*mu
        M=K*B+(ki[0]**2-ki[1]**2)*transverse
        N=mu*(transverse*(b1+b2)/2+mu*mu*b3)
        O=mu*transverse*(b1-b2)/2
        return A,B,(I1,I2,I3,I4,J2,J3,J4,T4),(L,M,N,O)
    cphi=np.cos(2*math.pi*np.arange(8192)/8192)
    for mu in [0.,.3,.9]:
        A,B,values,_=azimuth(mu)
        hh=A+B*cphi
        numerical=[np.mean(hh**(-n)) for n in [1,2,3,4]]
        numerical += [np.mean(cphi*hh**(-n)) for n in [2,3,4]]
        numerical += [np.mean(cphi*cphi/hh**4)]
        for index,(exact,num) in enumerate(zip(values,numerical)):
            check(f'p{j}_mu{mu}_azimuth_identity{index}',err(exact,num))
    results=[]
    for nmu in [512,1024]:
        mu,w=np.polynomial.legendre.leggauss(nmu); w=w/2
        A,B,(I1,I2,I3,I4,J2,J3,J4,T4),(L,M,N,O)=azimuth(mu)
        invmean=float(np.dot(w,I1)); heff=1/invmean
        qeff=float(np.dot(w,L*I3+M*J3-3*I1))/invmean
        qmean=float(np.dot(w,L*I2+M*J2-3))
        square=(L*L+N*N)*I4+2*(L*M+N*O)*J4+(M*M+O*O)*T4-6*(L*I2+M*J2)+9
        qrms=math.sqrt(float(np.dot(w,square)))
        check(f'p{j}_nodes{nmu}_Heff_min',(min(ki)-heff)/max(1.,abs(heff)))
        check(f'p{j}_nodes{nmu}_Heff_max',(heff-max(ki))/max(1.,abs(heff)))
        check(f'p{j}_nodes{nmu}_odd_cancel',abs(np.dot(w,N*I3+O*J3))/max(1.,abs(qeff*invmean)))
        results.append(dict(polar_nodes=nmu,Heff_over_H=heff,qeff=qeff,
                            q_sky_mean=qmean,q_rms=qrms))
    for metric in ['Heff_over_H','qeff','q_rms']:
        check(f'p{j}_replacement_quadrature_{metric}',err(results[0][metric],results[1][metric]),2e-7)
    refined.append(dict(trace=1000000,r=7.,amplitude_fraction=1.,phase_index=j,
                        original_sky=p['sky'],refined_sky=results[1],coarse_polar_sky=results[0]))
qualified=all(c['passed'] for c in checks) and all(c['passed'] for c in old['checks'] if c['name'] not in expected)
combined=[]
for s in old['rows']:
    for p in s.get('phases',[]):
        if p['availability']!='ELIGIBLE_DUST_OBSERVER': continue
        sky=p['sky']
        replacement=next((v for v in refined if s['trace']==v['trace'] and s['r']==v['r'] and s['amplitude_fraction']==v['amplitude_fraction'] and p['phase_index']==v['phase_index']),None)
        if replacement: sky=replacement['refined_sky']
        combined.append(dict(trace=s['trace'],r=s['r'],amplitude_fraction=s['amplitude_fraction'],
                             phase_index=p['phase_index'],rho=p['rho_over_M2H2'],
                             Hmin=p['local_H_min_over_H'],Hmax=p['local_H_max_over_H'],**sky))
summary=dict(eligible_observer_count=len(combined),
             negative_qeff_count=sum(r['qeff']<0 for r in combined),
             low_density_negative_count=sum(r['qeff']<0 for r in combined if r['r']<=3),
             qeff_min=min(combined,key=lambda r:r['qeff']),
             qeff_max=max(combined,key=lambda r:r['qeff']),
             lowest_density_half_amplitude_examples=[r for r in combined if r['r']==.15 and r['amplitude_fraction']==.5 and r['phase_index'] in [0,8]])
payload=dict(status='QUALIFIED' if qualified else 'FAILED',
             original_status_retained='FAILED',original_raw_sha256=hashlib.sha256(raw).hexdigest(),
             original_payload_sha256=receipt['payload_sha256'],replaced_gate_names=expected,
             retained_original_pass_count=sum(c['passed'] for c in old['checks']),
             new_passed=sum(c['passed'] for c in checks),new_total=len(checks),
             combined_qualified_control_count=sum(c['passed'] for c in old['checks'])+sum(c['passed'] for c in checks),
             checks=checks,refined_rows=refined,summary=summary,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             protocol_sha256=hashlib.sha256((HERE/'SOL_DUST_OBSERVER_COSMOGRAPHY_V002_REPAIR.md').read_bytes()).hexdigest(),
             elapsed_seconds=time.monotonic()-start)
canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
with OUT.open('x') as stream:
    json.dump(dict(payload=payload,payload_sha256=hashlib.sha256(canonical).hexdigest()),stream,indent=2,allow_nan=False)
print(json.dumps(dict(status=payload['status'],new_passed=payload['new_passed'],new_total=payload['new_total'],
                     elapsed_seconds=payload['elapsed_seconds'],refined=refined,
                     summary=summary,failed=[c for c in checks if not c['passed']]),indent=2))
