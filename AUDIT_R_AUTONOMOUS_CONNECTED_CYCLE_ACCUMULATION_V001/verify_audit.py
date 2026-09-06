#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001";c=0
def ck(v,s):
 global c
 if not v:raise AssertionError(s)
 c+=1
X={"README.md":"12586e701b66251abd2b6833c921fa067e4614f50c4329f86a80ea86bd4eefc3","RESULT.json":"043c85675cfc4956fa2e5216a324e941bf84523bf4abd0054ed2be07f378bbdc","THEOREM.md":"705d611de3efb33f75e7afd77686261a5c60e76cc83dc8e0a2adcba1f3688a3c","compute_connected_cycle.py":"9dfde7317f39283169fda9ef01158004096dcd6fdbd5cf4c704c0bceac0bf38b"}
for f,x in X.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==x,"custody")
e=os.environ.copy();e["PYTHONWARNINGS"]="error"
for _ in range(2):o=subprocess.run([sys.executable,"-B",str(T/"compute_connected_cycle.py")],capture_output=True,text=True,check=True,env=e);ck("__18/18" in o.stdout and hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==X["RESULT.json"],"canonical")
o=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=e);ck("__10/10" in o.stdout,"independent");a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());ck(a["census"]["selected_edges_global_owner_once"]==b["census"]["selected_edges_global_owner_once"]==96,"census")
for x,y in zip(a["rows"],b["rows"]):ck(max(abs(x[k]-y[k]) for k in y if isinstance(y[k],(int,float)))<8e-12 and max(abs(u-v) for k in ("q_before","q_after","integrated_oriented_currents") for u,v in zip(x[k],y[k]))<8e-12,"rows")
ck(abs(a["ratio"]-b["pi_over_2_connected_over_disjoint_throughput_total"])<8e-12,"ratio");ck("NOT_1PI_OR_WARD" in a["ctp"] and "SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ"==a["conditional"],"ctp scope");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"report");print(f"PASS__CONNECTED_CYCLE_HOSTILE_AUDIT__{c}/{c}")
