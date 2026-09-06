#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;T=H.parent/"DEVELOPMENT_R_CONNECTED_RECORD_TRAJECTORY_L4_L10_V001";n=0
def ck(v,m):
 global n
 if not v:raise AssertionError(m)
 n+=1
pins={"README.md":"04d473285f11196996c4d2218279a6659251131b46ec119637d0a9882e4ca9b6","RESULT.json":"1bb1ee2bceb242c32d97b89e45160d2983de18aaaa802a68034528df8d5db5df","THEOREM.md":"68600d89e8ace7bc69ff16143de24286a1e74b55b35cca5c0d790eef06e684d4","compile_trajectory.py":"57c5c5996fee00d4299b88f319d6250d4c68fe7e956d0739ba3425f0c3d4945d"}
for f,h in pins.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==h,"custody "+f)
env=os.environ.copy();env["PYTHONWARNINGS"]="error";r=subprocess.run([sys.executable,"-B",str(T/"compile_trajectory.py")],capture_output=True,text=True,check=True,env=env);ck("__33/33" in r.stdout,"target replay");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==pins["RESULT.json"],"canonical result")
r=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env);ck("PASS_TRAJECTORY_INDEPENDENT" in r.stdout,"independent replay");a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());ck([x["L"] for x in a["rows"]]==[4,6,8,10],"row selection")
for x,y in zip(a["rows"],b["rows"]):
 L=x["L"];ck((x["sites"],x["sites_per_F3_layer"],x["possible_F3_links"],x["connected_components"],x["selected_edges_owner_once"],x["prepared_source_lineages"])==(L**3,L**3//2,(L**3//2)**2,L**2//2,3*L**3//2,L**3//2),f"L{L} census")
 ck(set(x)==set(y) and all((abs(x[k]-y[k])<5e-15 if isinstance(y[k],float) else x[k]==y[k]) for k in y),f"L{L} raw row")
 ck(x["active_internal_edges_per_component"]==2*L and x["active_connector_edges_per_component"]==L,f"L{L} active supports")
ck(abs(a["rows"][0]["record_ledger_residual_l1_per_component"]-1.3600232051658168e-15)<1e-29,"active L4 residual")
for x,y in zip(a["adjacent_comparators"],b["adjacent_comparators"]):ck(all(abs(x[k]-y[k])<5e-15 for k in y if isinstance(y[k],float)) and all(x[k]==y[k] for k in y if not isinstance(y[k],float)),f"L{x['from_L']}/L{x['to_L']} comparator")
rep=a["repair_check"];ck(rep["strict_equality_fails"] and rep["tolerance_1e_12_passes"] and all(not x["strict_float_equal"] for x in a["adjacent_comparators"]),"float repair reproduced");read=(T/"README.md").read_text();src=(T/"compile_trajectory.py").read_text();ck("candidate\nwas deleted" in read and "1e-12" in read and "< 1.0e-12" in src,"repair custody wording")
ck(b["classification"]=="HOSTILE_AUDITED_INPUT_COMPILATION__FINITE_RAW_RECORD_TRAJECTORY" and b["scope"].endswith("NO_FIT_OR_EXTRAPOLATION"),"finite classification");ck(b["residual_status"]=="RAW_UNASSIGNED_NUMERICAL_RECORD_LEDGER_TERMS__NOT_CALLED_DEFECTS","residual class");ck(all(z in a["scope"] for z in ("NO_MONOTONICITY","LIMIT","EXPONENT","SCALING","AUTONOMOUS_SUPPORT","GRID","CONTINUUM","WARD","CRITICAL","PHASE","GRAVITON","GRAVITY")),"claim ceiling");ck("No correction required" in (H/"AUDIT_REPORT.md").read_text(),"disposition")
print(f"PASS__CONNECTED_RECORD_TRAJECTORY_HOSTILE_AUDIT__{n}/{n}")
