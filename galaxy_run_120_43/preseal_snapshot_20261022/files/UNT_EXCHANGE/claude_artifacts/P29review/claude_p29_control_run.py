import sys, importlib.util
from fractions import Fraction as F
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
se=load("se",sys.argv[1]+"/se.py"); ci=load("ci",sys.argv[1]+"/ci.py")
adm={k:True for k in ("matched_filling","response_modes","simultaneous_error_domain","mode_qualification")}
base=None; rates={}
for case in ci.cases():
    rs=[]
    for ch,cfg in zip(case["channels"],case["configs"]):
        r=se.extract(ch,cfg); rs.append((r["status"],r["rate"]))
    ok=all(s==case["expected"] for s,_ in rs) and (case.get("expected_rates") is None or all(r==e for (_,r),e in zip(rs,case["expected_rates"])))
    print(f'{case["id"]:18s} statuses={[s for s,_ in rs]} rates={[str(r) for _,r in rs]} {"OK" if ok else "MISMATCH"}')
    if case.get("expected_rates"): rates[case["id"]]=case["expected_rates"]
b=rates["lapse_1"]
def box(r0,r1): return [(x,x) for x in list(r0)+list(r1)]
for cid in ["lapse_1/2","lapse_2","medium_axis1_1","medium_axis1_-1","medium_axis2_1","medium_axis2_-1"]:
    out=se.compare_joint_rate_box(box(b,rates[cid]),F(1,100),F(1,20),adm); print(f"compare base vs {cid:16s} -> {out['status']}  shifts={[(str(a),str(c)) for a,c in out['shifts']]}")
gray=(F(2),F(3)*(1+F(3,200)),F(5))
out=se.compare_joint_rate_box(box(b,gray),F(1,100),F(1,20),adm); print("GRAY shift 3/200 (between eq 1/100 and min 1/20) ->",out["status"])
# joint error control
tgt=(F(2),F(3)*(1+F(1,200)),F(5))
wide=[(x*(1-F(1,100)),x*(1+F(1,100))) for x in list(b)+list(tgt)]
print("joint error control wide ->",se.compare_joint_rate_box(wide,F(1,100),F(1,20),adm)["status"]," point ->",se.compare_joint_rate_box(box(b,tgt),F(1,100),F(1,20),adm)["status"])
for name,fn in (("two_pole",ci.two_pole_case),("cancellation",ci.cancellation_case),("no_clock",ci.no_clock_case),("complex_cross",ci.complex_cross_case)):
    p,c=fn(); r=se.extract(p,c); print(f"{name:14s} -> {r['status']}  groups+={ {str(k):(round(v['W'],6),v['C']) for k,v in r['groups'].items() if k>0} }")
