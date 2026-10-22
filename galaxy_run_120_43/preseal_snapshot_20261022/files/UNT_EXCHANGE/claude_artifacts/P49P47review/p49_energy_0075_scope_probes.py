"""Claude scope probes: P50 reference shift alpha across Q sectors; finite-T floor dip. Own code."""
from fractions import Fraction as F
import math, json
out = {}
# (A) Cesaro uniform bound fed a two-sector H: Q0 levels {0,2}, Q1 levels {1,3}+alpha
def unif(levels, T=F(1), hbar=F(1)):
    ls = sorted(set(levels)); m = len(ls)
    if m == 1: return m, None, F(0)
    d = min(ls[i+1] - ls[i] for i in range(m-1)); return m, d, min(F(2), 2*hbar*(m-1)/(T*d))
rows = {}
for a in (F(0), F(-999, 1000), F(-1)):
    m, d, B = unif([F(0), F(2), F(1)+a, F(3)+a], T=F(1))
    rows[str(a)] = dict(m=m, delta=str(d), trace_bound_T1=str(B), T_sufficient_eta_1_10=str(F(m-1)/(d*F(1,10))))
rows['sector_restricted_any_alpha'] = dict(zip(('m', 'delta', 'trace_bound_T1'), map(str, unif([F(0), F(2)])))); rows['sector_restricted_any_alpha']['T_sufficient_eta_1_10'] = str(F(1)/(F(2)*F(1,10)))
out['cesaro_multisector_alpha'] = rows
# (B) energy-mean criterion on a seed spanning Q sectors: |a> in Q0 (E=0, word0), |b> in Q1 (E=1+alpha, word1)
def crit(Ka, Kb, Ca, Cb):
    d = 2; t = Ka+Kb; u = Ka*Ka+Kb*Kb; v = Ca+Cb; z = Ka*Ca+Kb*Cb; den = d*u - t*t
    if den: b = (d*z - t*v)/den; a = (v - b*t)/d
    else: b = F(0); a = v/d
    return dict(K=[str(Ka), str(Kb)], a=str(a), b=str(b), W=[str(Ca-a-b*Ka), str(Cb-a-b*Kb)])
out['criterion_multisector_alpha'] = {str(al): crit(F(0), F(1)+al, F(1), F(0)) for al in (F(0), F(-1))}
# (C) finite-T average below the DE floor: H = sigma_x/2 (energies +-1/2, delta=1), rho=|0><0|, word=basis
T = math.pi/2
p_avg = 0.5 + math.sin(T)/(2*T)          # avg of cos^2(t/2)
p_DE = 0.5; target = p_avg
out['floor_dip_example'] = dict(T='pi/2', p_avg_word0=p_avg, p_DE_word0=p_DE, target_word0=target,
    TV_DE_target=abs(p_DE-target), TV_avg_target=abs(p_avg-target), half_uniform_bound=0.5*min(2, 2/T))
print(json.dumps(out, indent=1))
