#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;R=H.parent;T=R/"DEVELOPMENT_R_PHYSICAL_PARENT_AUTONOMOUS_RING_SELECTION_V001";c=0
def ck(v,s):
 global c
 if not v:raise AssertionError(s)
 c+=1
X={"README.md":"e558a77b83601cc71e974f4b27c8a24b54bcf57df6677145fde4677d5aa8626f","RESULT.json":"d5c12520518c54dce228e9aa28b860980685276f84aa52aa065b8c6e1e8d0bb4","THEOREM.md":"c4d1661b2ee337562da3afd8a28e9446d7e3f88a58580b1218413220ea713336","compute_autonomous_ring.py":"f3a1fb97d82ab9876eecfdfd217e660708dc192d787413d80774230ae60f24e0"}
for f,x in X.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==x,"custody")
e=os.environ.copy();e["PYTHONWARNINGS"]="error";o=subprocess.run([sys.executable,"-B",str(T/"compute_autonomous_ring.py")],capture_output=True,text=True,check=True,env=e);ck("__16/16" in o.stdout,"target");o=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=e);ck("PASS_AUTONOMOUS_RING_INDEPENDENT__8/8" in o.stdout,"independent")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());ck(abs(a["source_preparation_vector_error"]-b["source_preparation_vector_error"])<1e-15,"prep")
for x,y in zip(a["rows"],b["rows"]):ck(max(abs(x[k]-y[k]) for k in y if isinstance(y[k],(int,float)))<5e-12 and max(abs(u-v) for k in ("q_before","q_after","integrated_oriented_currents") for u,v in zip(x[k],y[k]))<5e-12,"rows")
ck(max(abs(a["raw_L8_over_L4"][k]-b["raw_L8_over_L4"][k]) for k in b["raw_L8_over_L4"])<5e-12,"ratios");ck("NO_FINITE_GATE_ORDER" in a["literal_BS09"] and "ADOPTED_ALPHA" in a["attachment"],"parent");ck(a["conditional"]=="SUPPORT_PROGRAM__T__TAU__CONTENT__READ" and "AUTONOMOUS_SUPPORT" in a["open"],"conditional open")
ledger=(R/"GRAVITY_VERIFICATION_LEDGER.md").read_text();cont=(R/"CURRENT_CONTINUATION.md").read_text();plan=(R/"RECORD_FIRST_ACCUMULATION_GATE_PLAN_V002.md").read_text();old=("explicit ordered circuit is the selected finite parent","selected-parent record data","necessary parent data","physical selection rule")
ck(not any(p in ledger or p in cont or p in plan for p in old),"old authority phrases rejected")
ck("Authoritative physical-parent reclassification" in ledger and "programmed-control records" in ledger and "not autonomous BS09" in ledger and "declared finite programmed-controller history" in ledger,"ledger correction")
ck("conditional programmed-control" in cont and "supplied node-dependent control absent from" in cont and "literal BS09" in cont and "not autonomous physical-parent histories" in cont,"continuation correction")
ck("programmed-control records" in plan and "node-dependent stagger nor a finite gate order" in plan and "autonomous BS09 exponential" in plan,"governing plan correction")
rep=(H/"AUDIT_REPORT.md").read_text();ck("PROMOTION CONDITION SATISFIED" in rep and "conditional programmed-control records" in rep and "not autonomous BS09 selection" in rep,"repair report");ck("NO_GRID_DEFECT_CONTINUUM_WARD_GRAVITY" in a["scope"],"scope")
print(f"PASS__AUTONOMOUS_RING_HOSTILE_AUDIT__{c}/{c}")
