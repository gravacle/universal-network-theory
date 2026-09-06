#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L12_V001";n=0
def ck(v,m):
 global n
 if not v:raise AssertionError(m)
 n+=1
pins={"README.md":"d4305fac605614f1eafa3ce097340c7ac37af5366ddda27e79392a8b9f3e75b3","RESULT.json":"8fe9697c833542812bbda78ea5528265b048d1775ace43a7203e1c583c7b5759","THEOREM.md":"0f4008d6797d44587f8c66061f0c2e80bf56d9f561e7a52ab67ca0667b07ab3d","compile_trajectory.py":"0fbc0ebbaeaaeb285908d1cc1544cb41134f61f2e265f4964e8b670d39d313ec"}
for f,h in pins.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"custody "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error";r=subprocess.run([sys.executable,"-B",str(T/"compile_trajectory.py")],capture_output=True,text=True,check=True,env=env);ck("__16/16" in r.stdout,"target replay");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical result")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env);ck("PASS_TRAJECTORY_L12_INDEPENDENT" in r.stdout,"independent replay");a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text())
ck(a["base_trajectory_sha256"]==b["base_trajectory_sha256"]=="1bb1ee2bceb242c32d97b89e45160d2983de18aaaa802a68034528df8d5db5df" and a["l12_sha256"]==b["rows"][-1]["input_sha256"],"input pins");ck(a["base_rows"]==b["rows"][:4],"append-only rows");ck(a["base_adjacent_comparators"]==b["adjacent_comparators"][:3],"append-only comparators")
def same(x,y):return set(x)==set(y) and all((abs(x[k]-y[k])<2e-15 if isinstance(y[k],float) else x[k]==y[k]) for k in y)
ck(same(a["L12_row"],b["rows"][-1]),"complete L12 row");ck(same(a["L10_to_L12"],b["adjacent_comparators"][-1]),"L10/L12 comparator")
row=a["L12_row"];ck((row["sites"],row["sites_per_F3_layer"],row["possible_F3_links"],row["connected_components"],row["selected_edges_owner_once"],row["prepared_source_lineages"])==(1728,864,746496,72,2592,864),"L12 census");ck((row["active_internal_edges_per_component"],row["active_connector_edges_per_component"])==(24,12),"active supports")
res=a["residual_distinction"];ck(res["L12_per_component_L1"]==1.430063845120344e-10 and res["base_per_component_L1"]==[1.3600232051658168e-15,4.7398196478809496e-12,6.321498879913179e-12,7.76556596804312e-12] and res["classification"].endswith("NOT_DEFECTS"),"residual separation")
rd=(T/"README.md").read_text();th=(T/"THEOREM.md").read_text();ck(all(s in rd+th for s in ("225.1993457748","0.5212947819","0.1681544187","0.0360485022","1.7279838016","0.9999906259","1.7279870255","0.9999924916","1.430e-10","5.960e-12","1.030e-8")),"documented numbers")
ck(b["classification"]=="HOSTILE_AUDITED_INPUT_APPEND__FINITE_RAW_RECORD_TRAJECTORY" and b["scope"].endswith("NO_FIT_OR_EXTRAPOLATION"),"classification");ck(b["residual_status"]=="RAW_UNASSIGNED_NUMERICAL_RECORD_LEDGER_TERMS__NOT_CALLED_DEFECTS","residual class");ck(all(s in a["scope"] for s in ("NO_MONOTONICITY","CONVERGENCE","LIMIT","EXPONENT","FIT","SCALING","GRID","CONTINUUM","WARD","CRITICAL","PHASE","GRAVITON","GRAVITY")),"claim ceiling");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"disposition")
print(f"PASS__CONNECTED_TRAJECTORY_L12_HOSTILE_AUDIT__{n}/{n}")
