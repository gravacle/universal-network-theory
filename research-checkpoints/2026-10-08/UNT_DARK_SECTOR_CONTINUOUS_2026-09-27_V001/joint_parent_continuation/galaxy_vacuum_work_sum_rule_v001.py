from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE/'GALAXY_VACUUM_WORK_SUM_RULE_V001_RESULT.json'
if OUT.exists():
    raise SystemExit('Refusing overwrite')
frozen_path=HERE/'GALAXY_RADIAL_TRANSFER_V001_FROZEN.json'
raw=frozen_path.read_bytes()
cal=json.loads(raw)['a0_si']
checks=[]
quadratures=[]
exact=2*math.pi**4/15

def check(name,value,limit):
    checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(value<=limit)))

def values(x):
    d=np.expm1(x)
    s=x*x/d
    sp=2*x/d-x*x*np.exp(x)/(d*d)
    return x*x+s,s,2*x+sp,sp

for order in [256,512]:
    nodes,weights=np.polynomial.legendre.leggauss(order)
    x=30*(nodes+1)
    f,s,fp,sp=values(x)
    direct=float(30*np.dot(weights,s*fp))
    parts=float(30*np.dot(weights,2*x*s))
    check(f'direct_{order}',abs(direct/exact-1),1e-10)
    check(f'parts_{order}',abs(parts/exact-1),1e-10)
    check(f'independent_{order}',abs(direct-parts)/exact,1e-10)
    quadratures.append(dict(order=order,direct=direct,parts=parts))
lo,hi=1.,2.
for _ in range(80):
    mid=(lo+hi)/2
    if (2-mid)*math.exp(mid)>2:
        lo=mid
    else:
        hi=mid
turnover=(lo+hi)/2
check('turnover',abs((2-turnover)*math.exp(turnover)-2),1e-12)
gturn=float(values(turnover)[0])
symbol=[]
for x in [.01,.1,.3,1.,2.,3.,10.,20.]:
    f,s,fp,sp=(float(t) for t in values(x))
    epsilon=sp/fp
    radial=2*x/fp
    check(f'static_radial_positive_{x}',-radial,0.)
    check(f'static_mu_positive_{x}',-(-math.expm1(-x)),0.)
    check(f'derivative_identity_{x}',abs(epsilon+radial-1),1e-12)
    for ellp in [0.,1.,10.]:
        filt=1/(1+ellp**2)
        omega2=(1/(filt*filt*epsilon)-1)/7
        symbol.append(dict(x=x,g_over_a0=f,epsilon=epsilon,
                           static_radial=radial,ell_p=ellp,
                           longitudinal_omega2_over_p2=omega2,
                           gradient_unstable=bool(omega2<0)))
predictions=[]
for key in ['rar_calibrated','inherited_calibrated']:
    a0=cal[key]
    acceleration_rate=a0/299792458*3.085677581491367e19
    Hvac=2*math.pi**2/math.sqrt(45)*acceleration_rate
    for Fbg in [1.,1.75]:
        predictions.append(dict(calibration=key,a0_si=a0,Fbg=Fbg,
                                H_infinity_km_s_Mpc=Hvac/math.sqrt(Fbg),
                                H_today_dust_illustration=math.sqrt((Hvac*Hvac+223.5)/Fbg),
                                unrescaled_endpoint_rate=Hvac))
tail=2*math.exp(-60)*(60**3+3*60**2+6*60+6)/(1-math.exp(-60))
out=dict(numerical_status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
         physical_status='DIRECT_CONSTANT_BETA_CLOCK_COMPLETION_HAS_NEGATIVE_PRINCIPAL_BRANCH',
         premise='RAR force plus physical W(infinity)=0; not adopted or native',
         work_over_a0_squared=exact, parts_tail_bound=tail,
         turnover_x=turnover,turnover_g_over_a0=gturn,
         quadratures=quadratures,principal_readouts=symbol,predictions=predictions,
         checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
         calibration_sha256=hashlib.sha256(raw).hexdigest(),
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         protocol_sha256=hashlib.sha256((HERE/'GALAXY_VACUUM_WORK_SUM_RULE_V001.md').read_bytes()).hexdigest())
with OUT.open('x') as stream:
    json.dump(out,stream,indent=2,allow_nan=False)
print(json.dumps({k:out[k] for k in ['numerical_status','physical_status','passed','total',
    'work_over_a0_squared','parts_tail_bound','turnover_x','turnover_g_over_a0','predictions']},indent=2))
