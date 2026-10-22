import math,json
from fractions import Fraction as F
c=299792458.; theta=math.log1p((5/3)*11000.**2/((5/3)-1)/(c*c))
checks={}
for v in (1.,10.,100.,1000.):
 u=v*1000; R=7.;rho=.2;B=3.
 d=u*R*rho*B/4;t=c*c*theta/(2*u)
 g=u*u*R*rho*B/(2*c*c*theta)
 assert math.isclose(d/t,g,rel_tol=3e-16)
 assert math.isclose(t/1000,c*c*theta/(2*1e6*v),rel_tol=3e-16)
checks['ratio_and_units_4_cases']=True
# Analytic derivatives checked by symmetric finite differences, inert SI values.
C=10.; L=2.;P=1.;Gp=3.;R=2.; v=math.sqrt(C*C*(L+P)/Gp);e=1e-5
f=lambda l,g:math.sqrt(C*C*(l+P)/g)
a=(f(L+e,Gp)-f(L-e,Gp))/(2*e); b=(f(L,Gp+e)-f(L,Gp-e))/(2*e)
assert math.isclose(a,C*C/(2*v*Gp),rel_tol=1e-9)
assert math.isclose(abs(a/b),(C/v)**2,rel_tol=1e-9)
checks['derivatives']=True
# Bound |R hprime| <= M, |h| <= epsilon.
eps=F(1,1000000);M=eps
for h in (-eps,F(0),eps):
 for rh in (-M,F(0),M):assert abs(rh/(2*(1+h)))<=M/(2*(1-eps))
# h=eps*sin(k*log(R/R0)); at R0, h=0 and R hprime=eps*k.
k=2000000; remainder=eps*k/2
assert remainder==1
checks['conditional_bound_and_amplitude_counterexample']=True
# Linear response t versus finite positive perturbation, normalized synthetic values.
u=F(1);ctheta=F(3);linear=ctheta/(2*u);finite=math.sqrt(float(u*u+ctheta))-float(u)
assert linear==F(3,2) and finite==1.
checks['finite_change_counterexample']=True
# Independent specification oracle, NOT production implementation.
base={'query_ids':['synthetic'], 'R_i':[1.], 'rule_id':'TI_B_SCALE_R_V001', 'theta_hex':theta.hex(),'c_hex':c.hex()}
def contract_ok(x):return set(x)==set(base) and x==base
for field in ('t_i','velocity','sigma','N_min','scale_1_over_k','eps_km_s'):
 mutant=dict(base);mutant[field]=1
 assert not contract_ok(mutant)
for field in ('theta_hex','c_hex'):
 mutant=dict(base);mutant[field]='0x1.0p+0';assert not contract_ok(mutant)
checks['8_contract_mutants_rejected']=True
def ratio(v,factor):return (abs(v)*1000)**2*factor/(2*c*c*theta)
def verdict(rows,factor):
 if not rows:return 'UNAVAILABLE'
 g=max(ratio(v,factor) for v in rows)
 return 'FAIL' if g>.005 else 'PASS'
assert ratio(0,10)==0 and math.isfinite(ratio(0,10))
assert ratio(2,10)==4*ratio(1,10)
assert verdict([],10)=='UNAVAILABLE'
assert verdict([1],1e6)=='FAIL'
checks['zero_quadratic_empty_large_factor']=True
# Mutated behaviors disagree with oracle.
assert float('inf')!=ratio(0,10)
assert 'PASS'!=verdict([],10) and 'PASS'!=verdict([1],1e6)
checks['3_behavior_mutants_detected']=True
print(json.dumps({'checks':checks,'theta_hex':theta.hex(),'c_hex':c.hex(),'theta':theta,'amplitude_counterexample_remainder':str(remainder),'linear_change':str(linear),'finite_change':finite},indent=2))
