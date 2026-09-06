#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent;R=H.parent;T=R/"DEVELOPMENT_R_CONNECTED_L4_L6_L8_TRAJECTORY_V001";P=R/"DEVELOPMENT_R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_V001"/"RESULT.json";A=R/"AUDIT_R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_V001"/"INDEPENDENT_RESULT.json";c=0
def ck(v,s):
 global c
 if not v:raise AssertionError(s)
 c+=1
X={"README.md":"68bb3ae88083d2d2c8aa5f8110db052b46380c435296de6fa4219185eaa10b69","RESULT.json":"9f3b90108842183b4eae557d77670c245cec14ca2d7dde071643acc7eecfb39f","THEOREM.md":"a2a4805fad74f0225c5e7c391d1e69d7746d366cf0c3658dadb6063b75110405","compute_l6_interpolation.py":"4caa68e5c828593865b7603ab85788d7f54ac6474f8c6282a3625f3f0ce7b085"}
for f,x in X.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==x,"custody")
ck(hashlib.sha256(P.read_bytes()).hexdigest()=="20b41e90161105ec76282373004905843de4c2db0383137e6a09338e97133630","parent");ck(hashlib.sha256(A.read_bytes()).hexdigest()=="8e49a32c52e4e01d001f94e58e20af838d93da7d13f230ec2eb6340707c56749","audit parent")
e=os.environ.copy();e["PYTHONWARNINGS"]="error";o=subprocess.run([sys.executable,"-B",str(T/"compute_l6_interpolation.py")],capture_output=True,text=True,check=True,env=e);ck("__15/15" in o.stdout,"target");o=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=e);ck("__6/6" in o.stdout,"independent")
h=json.loads((T/"RESULT.json").read_text());r=json.loads((H/"INDEPENDENT_RESULT.json").read_text());x=r["L6"];y=h["rows"][1];ck(max(abs(x[k]-y[k]) for k in y if isinstance(y[k],(int,float)))<5e-13,"L6 row")
p=json.loads(P.read_text());rows=[p["rows"][0],x,p["rows"][1]];tf=("cells","retained_heads","expected_retained_total","gate_event_absolute_traffic_total","cumulative_net_edge_throughput_total","cumulative_net_inter_cycle_throughput_total");pf=("gate_event_absolute_traffic_per_retained_head","cumulative_net_edge_throughput_per_retained_head","cumulative_net_inter_cycle_throughput_per_retained_head")
for label,a,b in (("L6_over_L4",rows[1],rows[0]),("L8_over_L6",rows[2],rows[1])):
 ck(max(abs(a[k]/b[k]-h["raw_adjacent_total_ratios"][label][k]) for k in tf)<5e-13,"total ratios");ck(max(abs(a[k]/b[k]-h["raw_adjacent_per_head_ratios"][label][k]) for k in pf)<5e-13,"head ratios")
ev=[z[pf[0]] for z in rows];net=[z[pf[1]] for z in rows];rg=[z[pf[2]] for z in rows];ck(ev[1]<ev[0] and ev[2]>ev[1] and rg[1]<rg[0] and rg[2]>rg[1] and net[0]<net[1]<net[2],"mixed monotonicity")
ck(r["partition"]=="9x12=108" and (x["active_cumulative_supports_per_component"],x["active_cumulative_inter_cycle_supports_per_component"],x["owner_once_gate_events_per_component"])==(18,6,54),"counts");ck("NO_INTERPOLATION_EXPONENT_CONVERGENCE_CRITICAL_GENERIC_LAW" in r["claim_boundary"] and "WARD_GRAVITY" in r["claim_boundary"],"scope");ck(r["selected_recipe"]=={"preparation_pattern":"reversed","gate_order":"forward","depth":3} and "ADOPTED_ALPHA" in r["attachment"],"labels")
print(f"PASS__L4_L6_L8_HOSTILE_AUDIT__{c}/{c}")
