"""Small analytic-state diagnostic; no evolution, fit, or overwritten output."""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / 'SOL_REGIONAL_STATE_V001_RESULT.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite existing result')
START = time.monotonic()
F = 1.75
TRACES = [3, 10, 24, 50, 1000, 1000000]
DENSITIES = [.15, .3, 1., 3., 7.]
phase = 2 * math.pi * np.arange(4096) / 4096
u = np.cos(phase)
v = np.sin(phase)
checks = []
rows = []

def check(name, value, limit):
    checks.append(dict(name=name, value=float(value), limit=limit,
                       passed=bool(value <= limit)))

def density_min(r, t, A):
    candidates = [-1., 1.]
    if A > 0 and t > 0:
        vertex = -3. / (A * t)
        if abs(vertex) < 1:
            candidates.append(vertex)
    values = [r + 2*F*t*x + F*A*t*t*(2*x*x-1)/6 for x in candidates]
    i = int(np.argmin(values))
    return values[i], candidates[i]

for trace in TRACES:
    length_ratio = math.acosh(trace / 2)
    h = (2*math.pi)**2 / ((2*math.pi)**2 + 3*length_ratio**2)
    q = (1-F*h)/3
    A = 1+F*h-2*F*h*h
    for r in DENSITIES:
        lo, hi = 0., 3.
        if density_min(r, hi, A)[0] >= 0:
            lo = hi
        else:
            for _ in range(80):
                mid = (lo+hi)/2
                if density_min(r, mid, A)[0] >= 0:
                    lo = mid
                else:
                    hi = mid
        tmax = lo
        minimum, location = density_min(r, tmax, A)
        x = 3*F-r+F*q*tmax*tmax/2
        Q = q*tmax*tmax
        tag = f'T{trace}_r{r}'
        if tmax < 3:
            check(tag+'_density_root', abs(minimum), 1e-10)
        C = (2*F/3)*h*tmax
        D = 2*F*math.sqrt(h*(1-h)/3)*tmax
        shear = 1.5*(C*u)**2 + .5*(D*v)**2
        K = 3+tmax*u
        rho_action = F*K*K/3-x-shear/2
        rho_poly = r+2*F*tmax*u+F*A*tmax*tmax*(2*u*u-1)/6
        scale = max(1., r, float(np.max(abs(rho_action))))
        check(tag+'_Hamiltonian', np.max(abs(rho_action-rho_poly))/scale, 1e-11)
        # Momentum divided by k; a/k is fixed by monodromy.
        momentum = -C*v-(length_ratio/(2*math.pi))*D*v+(2*F/3)*tmax*v
        check(tag+'_momentum', np.max(abs(momentum))/max(1., tmax), 1e-11)
        check(tag+'_mass_mean', abs(float(np.mean(rho_action))-r)/max(1.,r), 1e-11)
        Q_sample = 2*float(np.var(K))/3-float(np.mean(shear))/F
        check(tag+'_Q_mean', abs(Q_sample-Q)/max(1.,abs(Q)), 1e-11)
        sampled_min = float(np.min(rho_poly))
        check(tag+'_minimum_upper', minimum-sampled_min, 1e-11)
        check(tag+'_minimum_sampling', sampled_min-minimum, 1e-5)
        favorable_upper = Q-r/(2*F) if q>0 else -r/(2*F)
        # For q>0 curvature increases with t; if nonpositive at tmax,
        # no state in its full admissible amplitude interval has a>0.
        exists = bool(x>0) if q>0 else bool(3*F-r>0)
        rows.append(dict(trace=trace, mean_density_over_M2H2=r,
                         aL=length_ratio, h=h, q=q, A=A,
                         t_density_max=tmax, min_density=minimum,
                         min_density_cosine=location, a2_over_H2_at_max=x,
                         K_min_over_H_at_max=3-tmax,
                         Q_over_H2_at_max=Q,
                         kinematic_margin_upper=favorable_upper,
                         positive_curvature_scale_state_exists=exists,
                         favorable_minimum_shear_budget_available=bool(exists and q>0 and favorable_upper>0),
                         endpoint_is_supremum=bool(tmax==3)))

# A uniform necessary low-density bound, not fitted to the discrete traces.
# A<=1+F/8 and t<3 => rho(-1)<=r-F*t*(2-(1+F/8)/2).
coefficient = 2-(1+F/8)/2
uniform = []
for r in DENSITIES:
    t_bound = min(3., r/(F*coefficient))
    Q_bound = t_bound*t_bound/3
    uniform.append(dict(r=r, amplitude_upper=t_bound,
                        Q_upper=Q_bound, kinematic_margin_upper=Q_bound-r/(2*F)))

payload = dict(status='QUALIFIED' if all(c['passed'] for c in checks) else 'FAILED',
               scope='instantaneous constraint state, not acceleration or observations',
               Fbg=F, Lambda=0., assumptions='compact Sol; N=1; j=0; minimum shear; one sinusoidal K; t<3',
               rows=rows, all_trace_necessary_bounds=uniform,
               checks=checks, passed=sum(c['passed'] for c in checks), total=len(checks),
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               protocol_sha256=hashlib.sha256((HERE/'SOL_REGIONAL_STATE_V001.md').read_bytes()).hexdigest(),
               elapsed_seconds=time.monotonic()-START)
with OUT.open('x') as stream:
    json.dump(payload, stream, indent=2, allow_nan=False)
print(json.dumps(dict(status=payload['status'], passed=payload['passed'], total=payload['total'],
                     elapsed_seconds=payload['elapsed_seconds'],
                     favorable=[r for r in rows if r['favorable_minimum_shear_budget_available']],
                     all_trace_bounds=uniform), indent=2))
