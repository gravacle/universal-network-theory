#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;R=H.parent;T=R/"DEVELOPMENT_R_AUTONOMOUS_KAPPA_TRAJECTORY_V001";B=R/"DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001"/"RESULT.json";c=0
def ck(v,s):
 global c
 if not v:raise AssertionError(s)
 c+=1
X={"README.md":"d1ede156a488479e4ba54bb2cf3cac1f94e01e605b29fe4bf7e281f9d846c007","RESULT.json":"26706555cb9f84aa9e6c49e7d7b92d5b23bd7ddfaec39ccfb6a31ac0b6626d91","THEOREM.md":"1b4b86b5ee8d2f2782d0fde8fed5788aa8f2eb5983a73784a8a5f0ed5460df57","compute_kappa_trajectory.py":"d255bdcb6e81f6a9f338634ee42a1920e6588bbc876d0e7d5cd9a160e25b27be"}
for f,x in X.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==x,"custody")
e=os.environ.copy();e["PYTHONWARNINGS"]="error";o=subprocess.run([sys.executable,"-B",str(T/"compute_kappa_trajectory.py")],capture_output=True,text=True,check=True,env=e);ck("__15/15" in o.stdout,"target");o=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=e);ck("PASS_KAPPA_INDEPENDENT__9/9" in o.stdout,"independent")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());ck(len(a["rows"])==len(b["rows"])==30,"rows")
for x,y in zip(sorted(a["rows"],key=lambda z:(z["kappa"],z["L"])),b["rows"]):ck(x["L"]==y["L"] and abs(x["kappa"]-y["kappa"])<1e-15 and max(abs(x[k]-y[k]) for k in y if isinstance(y[k],(int,float)))<8e-12 and max(abs(u-v) for k in ("q_after","integrated_oriented_currents") for u,v in zip(x[k],y[k]))<8e-12,"row")
for x,y in zip(a["ratios"],b["ratios"]):ck(x["kappa"]==y["kappa"] and all((x[k] is None and y[k] is None) or abs(x[k]-y[k])<8e-12 for k in ("L8_over_L4_throughput_total","L8_over_L4_throughput_per_retained_record")),"ratio")
base=json.loads(B.read_text());scan={r["L"]:r for r in a["rows"] if r["kappa"]==__import__('math').pi/2}
for z in (4,8):
 p=next(r for r in base["rows"] if r["L"]==z);q=scan[z];ck(abs(q["expected_retained_total"]-p["expected_retained_after_total"])<8e-12 and abs(q["absolute_oriented_throughput_total"]-p["absolute_oriented_throughput_total"])<8e-12 and max(abs(u-v) for u,v in zip(q["integrated_oriented_currents"],p["integrated_oriented_currents"]))<8e-12,"baseline")
ck("KAPPA_ONLY" in a["uniform_onsite_algebra"] and a["conditional"]=="SUPPORT__KAPPA_SAMPLES__SEPARATE_T_TAU_CLOCK__CONTENT__COMPLETE_READ","algebra/custody");ck("FINITE_GATE_ORDER__STAGGER__COEFFICIENT_SELECTION__DEFECT__PHYSICAL_GRID__CONTINUUM__WARD__GRAVITY"==a["not_claimed"],"scope");ck("No correction is required before promotion" in (H/"AUDIT_REPORT.md").read_text(),"report")
print(f"PASS__AUTONOMOUS_KAPPA_HOSTILE_AUDIT__{c}/{c}")
