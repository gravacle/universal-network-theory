#!/usr/bin/env python3
"""Custody, warning, independent trajectory, tolerance, and scope audit."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; TARGET=HERE.parent/"DEVELOPMENT_R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY_V001"
EXPECTED={"README.md":"475524c4d545845f92afafc6a058a1752439ba0e2aa2922fba7b17bdf07c6fe3","RESULT.json":"7a8c747d3692c0f268694cdc29016b689be0ab8caf4d0f688f6047b091b0947d","THEOREM.md":"1690c349f64108dfc687146cde0dca5ef286e883eb444c52a545be4e0bede9d7","compute_depth_trajectory.py":"1a5c15f1c058058859d45eb68588748c7529adcfdc103b60686a3652e1c2af85"}
checks=0
def check(v,label):
 global checks
 if not v: raise AssertionError(label)
 checks+=1
for name,digest in EXPECTED.items(): check(hashlib.sha256((TARGET/name).read_bytes()).hexdigest()==digest,"custody "+name)
check("compute_depth_trajectory" not in (HERE/"independent_reconstruction.py").read_text(),"no target import")
env=os.environ.copy(); env["PYTHONWARNINGS"]="error"
t=subprocess.run([sys.executable,"-B",str(TARGET/"compute_depth_trajectory.py")],capture_output=True,text=True,check=True,env=env)
check("PASS__R_CONNECTED_L8_CIRCUIT_DEPTH_TRAJECTORY__12/12" in t.stdout,"warning-free target")
hard=json.loads((TARGET/"RESULT.json").read_text())
check(hashlib.sha256((TARGET/"RESULT.json").read_bytes()).hexdigest()==EXPECTED["RESULT.json"],"deterministic target")
i=subprocess.run([sys.executable,"-B",str(HERE/"independent_reconstruction.py")],capture_output=True,text=True,check=True,env=env)
check("PASS_CONTROLLED_NUMERICAL_DEPTH_TRAJECTORY__16/16" in i.stdout,"independent run")
r=json.loads((HERE/"INDEPENDENT_RESULT.json").read_text())
check((r["clusters"],r["heads"],r["supports"],r["gate_records"])==(16,256,24,192),"census")
fields=("L8_expected_retained","expected_retained_per_cluster","q_min","q_max","first_ring_expected_retained","second_ring_expected_retained","cumulative_net_edge_throughput","cumulative_net_ring_throughput","cumulative_net_inter_ring_throughput","gate_event_absolute_traffic","max_abs_connected_edge_correlation","record_ledger_residual_l1_per_cluster","record_ledger_residual_linf_per_cluster","norm_error","number_law_max_change")
check(len(r["trajectory"])==len(hard["trajectory"])==9,"nine depths")
for a,b in zip(r["trajectory"],hard["trajectory"]):
 check(a["depth"]==b["depth"] and a["active_cumulative_edge_count"]==b["active_cumulative_edge_count"] and a["active_cumulative_inter_ring_edge_count"]==b["active_cumulative_inter_ring_edge_count"],"depth integer fields")
 check(max(abs(a[k]-b[k]) for k in fields)<5e-13,"depth numeric fields")
check(max(abs(r["envelope"][k]-hard["envelope"][k]) for k in hard["envelope"])<5e-13,"envelopes")
check(all(x["active_cumulative_edge_count"]==24 and x["active_cumulative_inter_ring_edge_count"]==8 for x in r["trajectory"][1:]),"positive-depth activity")
check(all(b["gate_event_absolute_traffic"]>a["gate_event_absolute_traffic"] for a,b in zip(r["trajectory"],r["trajectory"][1:])),"event monotonicity")
check(r["trajectory"][3]["cumulative_net_ring_throughput"]<r["trajectory"][2]["cumulative_net_ring_throughput"],"net cancellation")
e=r["envelope"]; check(5e-13<e["max_abs_L8_retained_change"]<1e-12,"tolerance repair")
check(e["max_record_ledger_residual_l1_per_cluster"]<8e-14 and e["max_record_ledger_residual_linf_per_cluster"]<9e-15,"residual envelope")
check(e["max_norm_error"]<5e-14 and e["max_number_law_change"]<5e-14,"control envelope")
check(r["attachment"]=="INHERITED_ADOPTED_ALPHA_R0__NOT_BARE_F3_DERIVED" and r["read"]=="COMPLETE_FAILURE_INCLUSIVE_PRODUCT_PVM","custody")
check(r["coordinate_status"]=="FINITE_ENUMERATION__NOT_PHYSICAL_GRID" and r["grid_defect_continuum_critical_Ward_gravity"]=="NOT_PROMOTED","scope")
report=(HERE/"AUDIT_REPORT.md").read_text()
for token in ("No material defect","192 gate records","strictly increasing","not granted monotonicity","5e-13","1e-12","not a physical grid","not a bare-F3","Ward identity","gravity claim"): check(token in report,"report token "+token)
print(f"PASS__DEPTH_TRAJECTORY_HOSTILE_AUDIT__{checks}/{checks}")
