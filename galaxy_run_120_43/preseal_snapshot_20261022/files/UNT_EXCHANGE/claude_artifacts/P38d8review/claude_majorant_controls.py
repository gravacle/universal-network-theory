import sys, importlib.util
from fractions import Fraction as F
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
m1=load("m1",sys.argv[1]+"/m1.py"); m2=load("m2",sys.argv[1]+"/m2.py")
ok=True
for (u,v,m0,mm1,hc,hw) in [(F(1,10),F(1,20),2,2,5,6),(F(1,5),F(1,7),3,2,4,4),(F(1,30),F(0),2,2,5,5)]:
    a=m1.majorants(u,v,m0=m0,m1=mm1,halo_cardinality=hc,halo_weight=hw)
    b6=m2.majorants(u,v,m0=m0,m1=mm1,halo_cardinality=hc,halo_weight=hw,order=6)
    b8=m2.majorants(u,v,m0=m0,m1=mm1,halo_cardinality=hc,halo_weight=hw,order=8)
    same6=all(a[k]==b6[k] for k in ("T_bounds","S_bounds","D_bounds","S_support","max_support","rho","x_rho","B_rho"))
    low=all(b8[k][n]==b6[k][n] for k in ("T_bounds","S_bounds","D_bounds","S_support") for n in range(1,7))
    r8=m2.remainder(b8,b8["rho"]/4,F(1)); r6=m2.remainder(b6,b6["rho"]/4,F(1))
    print(f"inputs u={u} v={v}: v001==v002(order6) {same6}; n<=6 unchanged at order8 {low}; x_rho<=1/4 {b8['x_rho']<=F(1,4)}; R8 = B/196608 {r8==b8['B_rho']/196608}; R6 = B/12288 {r6==b6['B_rho']/12288}; eps=0 -> {m2.remainder(b8,F(0),F(1))}")
    ok &= same6 and low and r8==b8['B_rho']/196608 and r6==b6['B_rho']/12288
    if v==0: print("  v=0 generator majorants zero?", all(x==0 for n,x in b8['S_bounds'].items() if n>=1) is False and "(S_n include u-terms; check T at v=0)" or "")
print("ALL CORE CONTROLS:", "PASS" if ok else "FAIL")
