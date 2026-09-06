#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys,time,resource
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_AUTONOMOUS_L10_ACCUMULATION_V001";c=0
def ck(v,s):
 global c
 if not v:raise AssertionError(s)
 c+=1
X={"EXECUTION_RECORD.json":"12634e99e0a41b1be3f6becb11c6b7ee485a1cb5e2c1a846c115ad41e6286b08","README.md":"cde89b8ec4e94c8d67907e31ac37d3ef71abdb72bfa63caa0e94c07178ac1afe","RESULT.json":"d5bed03d36dce36b93d5058405a856ab452aeeb774783975cc93008c90db341d","THEOREM.md":"1a1fc9f3a3b9e5a2a65ceb3fa855504703c26e69677a7043bf72ca4f292efaa6","compute_l10_accumulation.py":"1df2307cc46b9a720234069f5f3ef54895fd341cd547e6ac7f6fd0cec9d69688"}
for f,x in X.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==x,"custody")
e=os.environ.copy();e["PYTHONWARNINGS"]="error";start=time.perf_counter()
for _ in range(2):
 o=subprocess.run([sys.executable,"-B",str(T/"compute_l10_accumulation.py")],capture_output=True,text=True,check=True,env=e);ck("__18/18" in o.stdout,"target replay");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==X["RESULT.json"],"canonical preserved")
elapsed=time.perf_counter()-start
o=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=e);ck("PASS_L10_INDEPENDENT__6/6" in o.stdout,"independent")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());ck(len(a["rows"])==10,"ten")
for x,y in zip(a["rows"],b["rows"]):ck(max(abs(x[k]-y[k]) for k in y if isinstance(y[k],(int,float)))<8e-12 and max(abs(u-v) for k in ("q_after","integrated_oriented_currents") for u,v in zip(x[k],y[k]))<8e-12,"row")
for x,y in zip(a["ratios"],b["ratios"]):ck(all((x[k] is None and y[k] is None) or abs(x[k]-y[k])<8e-12 for k in y),"ratio")
rec=json.loads((T/"EXECUTION_RECORD.json").read_text());ck(rec["observed_runtime_seconds"]>0 and rec["observed_maximum_resident_set_mib"]>0 and elapsed>0,"execution observations");ck(a["conditional"]=="SUPPORT__KAPPA__T__TAU__CLOCK__CONTENT__SOURCE_ROUTING__COMPLETE_READ" and "PHYSICAL_GRID" in a["not_claimed"],"scope");ck("No correction is required" in (H/"AUDIT_REPORT.md").read_text(),"report")
print(f"PASS__L10_HOSTILE_AUDIT__{c}/{c}__REPLAY_SECONDS={elapsed:.6f}")
