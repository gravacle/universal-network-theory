#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_CONNECTED_PRISM_ORBIT_REDUCTION_V001";R=H.parent;n=0
def ck(v,m):
 global n
 if not v:raise AssertionError(m)
 n+=1
def vmax(a,b):return max(abs(float(x)-float(y)) for x,y in zip(a,b))
pins={"README.md":"839edbec8c25bbf260a98b6d6b9c944784980e5e25166b56376da767f3809503","RESULT.json":"f4b7079f085d63de94fa3f35f5e862e05b94b482386d999818d0a33c86821af1","THEOREM.md":"d7608c1dca4f44a70e2695596cba6bf0049cdd4c79919c5131ea705c20514a71","validate_prism_reduction.py":"e741f42649147169478fdf25e008be5464cc2759e21d6fdf2272513a42390c02"}
for f,h in pins.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"custody "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error";r=subprocess.run([sys.executable,"-B",str(T/"validate_prism_reduction.py")],capture_output=True,text=True,check=True,env=env);ck("__40/40" in r.stdout,"target replay");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical result")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env);ck("PASS_PRISM_INDEPENDENT" in r.stdout,"independent replay");a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());ck(a["support_and_source_parity_preserved"] and "X_EQUALS_I_MINUS_A" in a["group_definition_verified"],"group definition/invariance")
targets={4:R/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_CYCLE_ACCUMULATION_V001"/"RESULT.json",6:R/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L6_ACCUMULATION_V001"/"RESULT.json",8:R/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L8_ACCUMULATION_V001"/"RESULT.json",10:R/"DEVELOPMENT_R_AUTONOMOUS_CONNECTED_L10_ACCUMULATION_V001"/"RESULT.json"}
expected={4:(55,{"1":4,"2":6,"4":30,"8":15},184),6:(430,{"1":4,"2":6,"3":12,"6":142,"12":266},3044),8:(4435,{"1":4,"2":6,"4":30,"8":615,"16":3780},49076),10:(53764,{"1":4,"2":6,"5":60,"10":2562,"20":51132},786300)}
for x,y in zip(a["rows"],b["rows"]):
 L=x["L"];o,hist,nz=expected[L];ck((x["finite_group_order"],x["full_dimension"],x["orbit_dimension"],x["orbit_size_histogram"],x["quotient_nonzero_entries"],x["quotient_hermiticity_error"],x["signed_edge_orbits"])==(2*L,1<<(2*L),o,hist,nz,0,2),f"L{L} structure")
 tar=json.loads(targets[L].read_text());tar=next(z for z in tar["rows"] if z["kappa"]==3.141592653589793/2) if L==4 else tar;ck(vmax(x["q_after"],tar["q_after"])<3e-12 and vmax(x["integrated_oriented_currents"],tar["integrated_oriented_currents"])<2e-12,f"L{L} every q/current")
 ck(x["record_ledger_residual_l1"]<3e-11 and x["record_ledger_residual_linf"]<3e-12 and x["norm_error"]<3e-12 and x["energy_error"]<3e-12 and x["number_law_max_change"]<3e-12,f"L{L} controls")
z=a["L12_structural_screen"];hist={"1":4,"2":6,"3":12,"4":30,"6":142,"8":15,"12":10316,"24":693845};ck((z["full_dimension"],z["orbit_dimension"],z["orbit_size_histogram"],z["quotient_nonzero_entries"],z["operator_bytes"],z["evolution_performed"])==(16777216,704370,hist,12582508,201320128,False),"L12 structural screen");ck(abs(z["operator_MiB"]-191.99383544921875)<1e-12,"L12 operator MiB")
th=(T/"THEOREM.md").read_text();ck(all(s in th for s in ("0.013946 s","1,703,739,392","1.58673 GiB","unpromoted feasibility observations","not an L12 evolution result or\ncomplexity law")),"L12 observation boundary")
ck(b["classification"].startswith("EXACT_ORDER_2L_SOURCE_PRESERVING_FINITE_PRISM_GROUP") and b["scope"].endswith("NO_NEW_PHYSICS"),"classification");ck(all(s in a["scope"] for s in ("NO_MAXIMALITY","PHYSICAL_GEOMETRY","GRID","CONTINUUM","WARD","CRITICAL","PHASE","GRAVITON","GRAVITY")),"claim ceiling");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"disposition")
print(f"PASS__CONNECTED_PRISM_HOSTILE_AUDIT__{n}/{n}")
