#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_CONNECTED_FINITE_ORBIT_REDUCTION_V001";n=0
def ck(v,m):
 global n
 if not v:raise AssertionError(m)
 n+=1
pins={"README.md":"dc8b32689f232f562fa3f8ddaa3ab12f0a5491087e61868472f9f241a2a175d8","RESULT.json":"d53d63b510a61553e4c7fbeac5b66def64cbbc626b961fef8153bb6f86b0f927","THEOREM.md":"aab729e93256aaebf2092e878ae72defe85bbd4379c30586dcd08aa655d18237","validate_orbit_reduction.py":"a119f9de374caf16f6c183f931532b5bf0fb4e446a44db66cd39476520344b72"}
for f,h in pins.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"custody "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error";r=subprocess.run([sys.executable,"-B",str(T/"validate_orbit_reduction.py")],capture_output=True,text=True,check=True,env=env);ck("__27/27" in r.stdout,"target replay");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical result")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env);ck("PASS_ORBIT_INDEPENDENT" in r.stdout,"independent replay")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());ck([x["L"] for x in a["rows"]]==[4,6,8],"sizes")
expected={4:(256,4,76,{"1":4,"2":18,"4":54},340),6:(4096,6,720,{"1":4,"2":6,"3":60,"6":650},5948),8:(65536,8,8356,{"1":4,"2":18,"4":294,"8":8040},97684)}
for x,y in zip(a["rows"],b["rows"]):
 D,g,o,hist,nz=expected[x["L"]];ck((x["full_dimension"],x["group_order"],x["orbit_dimension"],x["orbit_size_histogram"],x["reduced_nonzero_entries"])==(D,g,o,hist,nz),f"L{x['L']} orbit census")
 ck(x["group_relations"] and x["support_and_source_parity_invariant"],f"L{x['L']} group invariance")
 ck(x["formula_error"]<2e-15 and x["hermiticity_error"]==0 and x["edge_orbit_representatives"]==[0,1,2*x["L"]],f"L{x['L']} quotient/oriented edge orbits")
 ck(x["q_target_linf"]<2e-12 and x["current_target_linf"]<2e-12,f"L{x['L']} full-state comparison")
 ck(max(abs(u-v) for u,v in zip(x["q_after"],y["q_after"]))<2e-12 and max(abs(u-v) for u,v in zip(x["integrated_oriented_currents"],y["integrated_oriented_currents"]))<2e-12,f"L{x['L']} target quotient comparison")
 ck(x["residual_l1"]<2e-11 and x["residual_linf"]<2e-12 and x["norm_error"]<2e-12 and x["energy_error"]<2e-12 and x["number_law"]<2e-12,f"L{x['L']} controls")
 ck(abs(x["max_abs_connected_edge_correlation"]-y["max_abs_connected_edge_correlation"])<2e-12,f"L{x['L']} correlation")
ck(b["classification"]=="EXACT_FINITE_AUTOMORPHISM_ORBIT_BASIS__NUMERICAL_EVOLUTION_CROSSCHECK","classification");ck(b["scope"]=="COMPUTATIONAL_COMPRESSION_OF_DECLARED_FINITE_SUPPORT__NO_NEW_PHYSICS","compression only");ck(a["conditional"]=="SUPPORT_KAPPA_T_TAU_CLOCK_CONTENT_ROUTING_READ","conditional inputs");ck("NUMERICAL_EVOLUTION_QUADRATURE" in a["scope"] and all(z in a["scope"] for z in ("NO_AUTONOMOUS_SUPPORT","GRID","CONTINUUM","WARD","CRITICAL","PHASE","GRAVITY")),"claim ceiling");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"disposition")
print(f"PASS__CONNECTED_FINITE_ORBIT_HOSTILE_AUDIT__{n}/{n}")
