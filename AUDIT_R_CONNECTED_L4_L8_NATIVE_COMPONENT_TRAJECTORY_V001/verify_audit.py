#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).parent; T=H.parent/"DEVELOPMENT_R_CONNECTED_L4_L8_NATIVE_COMPONENT_TRAJECTORY_V001"; D=H.parent/"DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001"
X={"README.md":"1fd2de98bf88ea04c82740280458e706be9af18721f896413315e92ff03618c6","RESULT.json":"20b41e90161105ec76282373004905843de4c2db0383137e6a09338e97133630","THEOREM.md":"64e863f52a6722baab2d225144c76297ca66b5156095502b6a38b2bbc61cd4a7","compute_connected_scale_trajectory.py":"c45b467930ccba76a4775388800ee3e3db0d28dcb2bcd63c98047c46dafaceee"};c=0
def ck(v,s):
 global c
 if not v:raise AssertionError(s)
 c+=1
for f,x in X.items():ck(hashlib.sha256((T/f).read_bytes()).hexdigest()==x,"custody")
env=os.environ.copy();env["PYTHONWARNINGS"]="error";o=subprocess.run([sys.executable,"-B",str(T/"compute_connected_scale_trajectory.py")],capture_output=True,text=True,check=True,env=env);ck("__14/14" in o.stdout,"target");ck(hashlib.sha256((T/"RESULT.json").read_bytes()).hexdigest()==X["RESULT.json"],"determinism");o=subprocess.run([sys.executable,"-B",str(H/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env);ck("PASS_CONNECTED_FINITE_SIZE__11/11" in o.stdout,"independent")
a=json.loads((H/"INDEPENDENT_RESULT.json").read_text());b=json.loads((T/"RESULT.json").read_text());
for x,y in zip(a["rows"],b["rows"]):
 ck(set(y).issubset(x) and max(abs(x[k]-y[k]) for k in y if isinstance(y[k],(int,float)))<5e-13,"row")
ck(max(abs(a["raw_L8_over_L4_ratios"][k]-b["raw_L8_over_L4_ratios"][k]) for k in b["raw_L8_over_L4_ratios"])<5e-13,"ratios");ck(max(abs(a["raw_L8_over_L4_per_head_ratios"][k]-b["raw_L8_over_L4_per_head_ratios"][k]) for k in b["raw_L8_over_L4_per_head_ratios"])<5e-13,"head ratios")
d=json.loads((D/"RESULT.json").read_text())["trajectory"][3];l8=a["rows"][1];mp={"expected_retained_per_component":"expected_retained_per_cluster","expected_retained_total":"L8_expected_retained","gate_event_absolute_traffic_per_component":"gate_event_absolute_traffic","cumulative_net_edge_throughput_per_component":"cumulative_net_edge_throughput","cumulative_net_inter_cycle_throughput_per_component":"cumulative_net_inter_ring_throughput","max_abs_connected_edge_correlation":"max_abs_connected_edge_correlation","record_ledger_residual_l1_per_component":"record_ledger_residual_l1_per_cluster","record_ledger_residual_linf_per_component":"record_ledger_residual_linf_per_cluster","norm_error":"norm_error","number_law_max_change":"number_law_max_change"};ck(max(abs(l8[k]-d[v]) for k,v in mp.items())<5e-13,"L8 consistency")
ck(a["selected_recipe"]=={"preparation_pattern":"reversed","gate_order":"forward","depth":3},"labels");ck(a["terminal_instrument"]=="COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM" and "ADOPTED_ALPHA" in a["attachment"],"custody labels");ck("NO_FORCED_FACTOR_8_EXPONENT_LIMIT_OR_GENERIC_LAW" in a["claim_boundary"] and "WARD_GRAVITY" in a["claim_boundary"],"scope")
print(f"PASS__NATIVE_COMPONENT_TRAJECTORY_HOSTILE_AUDIT__{c}/{c}")
