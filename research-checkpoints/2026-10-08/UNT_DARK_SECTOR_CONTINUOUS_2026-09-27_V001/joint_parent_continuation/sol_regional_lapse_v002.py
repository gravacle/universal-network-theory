"""Extend saved constraint states by their derived instantaneous lapse rate."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE/'SOL_REGIONAL_LAPSE_V002_RESULT.json'
if OUT.exists():
    raise SystemExit('Refusing overwrite')
start = time.monotonic()
src = HERE/'SOL_REGIONAL_STATE_V001_RESULT.json'
raw = src.read_bytes()
source_hash = hashlib.sha256(raw).hexdigest()
assert source_hash == 'a1ef4649fb2e108132bbcc18eb42da5e921918b00e9bfc5574c703294acda9f7'
old = json.loads(raw)
assert old['status'] == 'QUALIFIED'
F, beta = old['Fbg'], .5
epsilon = .0001 * 100 / 299792.458
uv_bound = 4.5*F*(2+(2*math.pi/math.acosh(1.5))**2)
inverse_filter2_bound = (1+epsilon**2*uv_bound)**2
full_coefficient_bound = 1/3+beta*inverse_filter2_bound/4
u = np.cos(2*math.pi*np.arange(4096)/4096)
checks, rows, uniform = [], [], []

def check(name, value, limit=1e-11):
    checks.append(dict(name=name, value=float(value), limit=limit, passed=bool(value<=limit)))

for saved in old['rows']:
    row = dict(saved)
    x = row['a2_over_H2_at_max']
    t = row['t_density_max']
    r = row['mean_density_over_M2H2']
    tag = f"T{row['trace']}_r{r}"
    if x <= 0:
        row['lapse_at_saved_endpoint'] = None
        row['reason'] = 'saved density endpoint is not a positive-curvature-scale Sol state'
        rows.append(row)
        continue
    h = row['h']
    p2 = x*(2*math.pi/row['aL'])**2
    inverse_filter2 = (1+epsilon**2*(p2+2*x))**2
    f2 = 1/inverse_filter2
    ndot = beta*t*inverse_filter2/2
    time_term = beta*t*t*inverse_filter2/4
    direct_mean = float(np.mean((3+t*u)*(ndot*u)))
    check(tag+'_lapse_preservation', abs(2*f2*ndot-beta*t)/max(1.,t))
    check(tag+'_clock_average', abs(direct_mean-time_term)/max(1.,time_term))
    check(tag+'_filter_upper', inverse_filter2-inverse_filter2_bound)
    check(tag+'_positive_clock', -time_term)
    row['lapse_at_saved_endpoint'] = dict(
        ndot_cosine_over_H=ndot, inverse_filter_squared=inverse_filter2,
        clock_term_over_H2=time_term,
        full_3acceleration_over_H2=row['Q_over_H2_at_max']+time_term-r/(2*F),
        mean_lapse_clock=True)
    rows.append(row)

coefficient = 2-(1+F/8)/2
for b in old['all_trace_necessary_bounds']:
    r = b['r']
    bound = full_coefficient_bound*b['amplitude_upper']**2-r/(2*F)
    uniform.append(dict(r=r, t_upper=b['amplitude_upper'],
                        full_3acceleration_upper=bound,
                        excludes_positive_initial_domain_acceleration=bool(bound<0)))

payload = dict(status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
               scope='instantaneous mean-lapse domain acceleration for declared minimum-shear Sol family',
               source_result_sha256=source_hash,
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               protocol_sha256=hashlib.sha256((HERE/'SOL_REGIONAL_LAPSE_V002.md').read_bytes()).hexdigest(),
               H_km_s_Mpc=100., ell_pc=100., ell_H_over_c=epsilon,
               universal_inverse_filter_squared_upper=inverse_filter2_bound,
               universal_full_coefficient_upper=full_coefficient_bound,
               low_density_exclusion_r_ceiling=F*coefficient**2/(2*full_coefficient_bound),
               rows=rows, all_trace_bounds=uniform, checks=checks,
               passed=sum(c['passed'] for c in checks), total=len(checks),
               elapsed_seconds=time.monotonic()-start)
with OUT.open('x') as stream:
    json.dump(payload, stream, indent=2, allow_nan=False)
print(json.dumps({k:payload[k] for k in ['status','passed','total','elapsed_seconds',
                 'ell_H_over_c','universal_inverse_filter_squared_upper',
                 'low_density_exclusion_r_ceiling','all_trace_bounds']}, indent=2))
